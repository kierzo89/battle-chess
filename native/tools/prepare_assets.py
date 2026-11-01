"""Authenticate published assets; write a simple indexed-frame stream for SDL.
Playback rate in the viewer is illustrative, not the original task timing.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import os

def prepare(root, output):
    manifest = json.loads((root/'verification/asset-snapshot.json').read_text())
    hashes = {r['path']: r['sha256'] for r in manifest['files']}
    def read(path):
        content = path.read_bytes()
        relative = path.relative_to(root).as_posix()
        if hashlib.sha256(content).hexdigest() != hashes.get(relative):
            raise ValueError('Unauthenticated asset: '+relative)
        return content
    recovered = root/'assets/recovered'
    palette = json.loads(read(recovered/'images/palette.json'))['rgb6']
    frames = []
    sequences = sorted((recovered/'animations').glob('*/sequence.json'))
    for seq in sequences:
        meta = json.loads(read(seq))
        for frame in meta['frames']:
            pixels = read(seq.parent/frame['indices_file'])
            w,h = frame['storage_width'],frame['height']
            if len(pixels)!=w*h or max(pixels,default=0)>15:
                raise ValueError('Invalid indexed image')
            header = struct.pack('<HHHHHhh',meta['pair'],meta['list'],frame['step'],w,h,
                                 frame['anchor_x'],frame['anchor_y'])
            frames.append(header+pixels)
    content = b'BCF1'+struct.pack('<I',len(frames))+bytes((v<<2)|(v>>4) for v in palette)
    output.parent.mkdir(parents=True,exist_ok=True)
    temporary = output.with_suffix('.tmp')
    temporary.write_bytes(content+b''.join(frames))
    os.replace(temporary,output)
    print(f'Authenticated {len(sequences)} sequences / {len(frames)} frames -> {output}')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    prepare(a.root.resolve(),a.output.resolve())
