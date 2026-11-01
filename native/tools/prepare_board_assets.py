"""Export six recovered setup-02 pieces for the initial native board UI.
This is a host square-board presentation, not the original projection renderer.
"""
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
frames=sorted((f for f in meta['frames'] if f['setup']==2),key=lambda f:f['frame'])
assert len(frames)==6
out=b'BCP1'+bytes((v<<2)|(v>>4) for v in palette)
# Visually identified authenticated sprites: bishop, king, knight, pawn, queen, rook.
# Engine kinds are king, queen, rook, bishop, knight, pawn. Archive order is not
# engine-kind order; the recovered renderer has additional representation mapping.
for frame in (1,4,5,0,2,3):
 f=frames[frame]
 assert f['native_global_index']==17+frame
 data=read(base+'setups/'+f['indices_file']);assert len(data)==f['storage_width']*f['height']
 out+=struct.pack('<HH',f['storage_width'],f['height'])+data
# This host mapping does not claim the original projection/renderer is ported.
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(out)
print('Authenticated six recovered board-piece frames')
