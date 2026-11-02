"""Authenticate and pack original board backgrounds and standing sprites."""
from pathlib import Path
import argparse,json,hashlib,struct
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
pins={r['path']:r['sha256'] for r in json.loads((a.root/'verification/asset-snapshot.json').read_text())['files']}
def read(name):
 data=(a.root/name).read_bytes()
 if hashlib.sha256(data).hexdigest()!=pins[name]:raise ValueError('Asset identity: '+name)
 return data
base='assets/recovered/'
meta=json.loads(read(base+'setups/report.json'));palette=json.loads(read(base+'images/palette.json'))['rgb6']
out=b'BCP5'+bytes((v<<2)|(v>>4) for v in palette)
for setup,background in ((0,0),(2,1)):
 packed=read(base+f'bank1/startup-{background:02d}.background-packed.bin')
 if len(packed)!=32000:raise ValueError('Background extent')
 out+=bytes(n for b in packed for n in (b>>4,b&15))
 frames=sorted((f for f in meta['frames'] if f['setup']==setup),key=lambda f:f['frame'])
 out+=struct.pack('<H',len(frames))
 for f in frames:
  data=read(base+'setups/'+f['indices_file'])
  if len(data)!=f['storage_width']*f['height'] or max(data)>15:raise ValueError('Sprite extent/palette')
  out+=struct.pack('<HHHHhh',f['native_global_index'],f['width'],f['storage_width'],f['height'],f['anchor_x'],f['anchor_y'])+data
timing=json.loads(read(base+'metadata/timing/timelines.json'))
keys=sorted({(item['frames'][0]['bank_pair'],item['frames'][0]['list_index']) for item in timing['move_sequences']})
keys=sorted(set(keys)|{(f['bank_pair'],f['list_index']) for item in timing['capture_sequences'] for f in item['frames']})
records=[]
for pair,seq in keys:
 folder=base+f'animations/pair-{pair:02d}-list-{seq:02d}/'
 data=json.loads(read(folder+'sequence.json'))
 for f in data['frames']:
  pixels=read(folder+f['indices_file'])
  if len(pixels)!=f['storage_width']*f['height'] or max(pixels)>15:raise ValueError('Walking frame extent')
  records.append(struct.pack('<HHHHHhh',pair,seq,f['step'],f['storage_width'],f['height'],f['anchor_x'],f['anchor_y'])+pixels)
out+=struct.pack('<H',len(records))+b''.join(records)
rawbase=base+'metadata/bank2-records/'
rawrecords=[r for r in json.loads(read(rawbase+'report.json'))['records'] if r['pair']<6]
out+=struct.pack('<H',len(rawrecords))
for r in rawrecords:
 pixels=read(rawbase+r['indices_file'])
 if len(pixels)!=r['storage_width']*r['height'] or (pixels and max(pixels)>15):raise ValueError('Delta plane extent')
 out+=struct.pack('<HHHHhh',r['pair'],r['record'],r['width'],r['height'],r['anchor_x'],r['anchor_y'])+pixels
# Generated output is not an original asset or matching-credit claim.
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(out)
print(f'Authenticated two backgrounds, 53 setup frames and {len(records)} walking frames')
