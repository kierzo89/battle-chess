"""Rebuild compressed bank records from exported symbols and preserved codec metadata.

The original tree shape, ignored separator bits, header and final padding remain
metadata; compressed symbol payload is regenerated. No original bank is read.
"""
from pathlib import Path
import hashlib,json,struct,argparse
H=lambda b:hashlib.sha256(b).hexdigest()
def need(ok,message):
 if not ok:raise ValueError(message)
def bit_string(data):return ''.join(f'{x:08b}'for x in data)
def codebook(bits):
 need(isinstance(bits,str)and set(bits)<=set('01'),'Tree must contain bits');at=0;codes={}
 def tree(code=''):
  nonlocal at
  need(len(code)<=16 and at<len(bits),'Tree bound exceeded');leaf=bits[at];at+=1
  if leaf=='1':
   need(at+8<=len(bits),'Truncated leaf');symbol=int(bits[at:at+8],2);at+=8
   need(symbol not in codes,'Duplicate leaf');codes[symbol]=code;return
  tree(code+'0');need(at<len(bits),'Missing separator');at+=1;tree(code+'1')
 tree();need(at==len(bits)and len(codes)>1,'Tree remainder or degenerate code');return codes

def encode(symbols,codec):
 header=bytes.fromhex(codec['header_hex']);need(len(header)==8,'Eight-byte native header required');need(struct.unpack_from('<I',header)[0]==len(symbols),'Changed symbol count requires reviewed layout update')
 tree=codec['tree_bits'];codes=codebook(tree);tail=codec['padding_bits'];need(isinstance(tail,str)and set(tail)<=set('01')and len(tail)<16,'Invalid final padding')
 try:payload=''.join(codes[s]for s in symbols)
 except KeyError as e:raise ValueError('Symbol absent from retained original tree')from e
 bits=tree+payload+tail;need(len(bits)%8==0,'Encoded record is not byte aligned');return header+bytes(int(bits[i:i+8],2)for i in range(0,len(bits),8))

def rebuild(folder,output):
 folder=Path(folder);recipe=json.loads((folder/'repack-recipe.json').read_text());parts=[];cursor=0
 for row in recipe['records']:
  need(row['offset']==cursor,'Record layout gap/overlap')
  if row['encoding']=='huffman':
   symbols=(folder/row['symbols_file']).read_bytes();need(H(symbols)==row['symbols_sha256'],'Decoded symbols changed');codec=json.loads((folder/row['codec_file']).read_text());raw=encode(symbols,codec)
  elif row['encoding']=='raw':raw=(folder/row['raw_file']).read_bytes()
  else:raise ValueError('Unknown encoding')
  need(len(raw)==row['size']and H(raw)==row['sha256'],'Repacked record differs');parts.append(raw);cursor+=len(raw)
 bank=b''.join(parts);need(len(bank)==recipe['bank_size']and H(bank)==recipe['bank_sha256'],'Whole bank differs');need(not Path(output).exists(),'Do not overwrite');Path(output).write_bytes(bank);return {'status':'EXACT_SYMBOL_REENCODE_AND_RAW_RECORD_ROUNDTRIP','bank_sha256':H(bank),'bank_bytes':len(bank),'compressed_symbol_payloads_regenerated':sum(r['encoding']=='huffman'for r in recipe['records']),'original_bank_read':False}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);ap.add_argument('--output',required=True,type=Path);a=ap.parse_args();print(json.dumps(rebuild(a.folder,a.output),indent=2))
