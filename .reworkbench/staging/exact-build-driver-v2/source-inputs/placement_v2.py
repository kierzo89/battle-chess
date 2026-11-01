"""Diagnostic reversible source-only emitter; no binary payload inputs."""
import re,hashlib
H=lambda b:hashlib.sha256(b).hexdigest()
def compose(source,listing,ordered_sites):
 text=source.decode('ascii');lines=text.splitlines(keepends=True);assert ''.join(lines)==text
 positions={};cursor=0;mapping=[]
 normalize=lambda x:' '.join(x.strip().split())
 for line in listing.decode('cp437').splitlines():
  m=re.match(r'^\s*(\d+)(?:\s+([0-9A-F]{4}))?\s',line)
  if not m:continue
  expanded=line.expandtabs(8);shown=normalize(expanded[40:])
  if not shown:continue
  hits=[n for n in range(cursor,len(lines)) if normalize(lines[n])==shown or (len(shown)>=16 and normalize(lines[n]).startswith(shown))]
  if not hits:continue
  n=hits[0];cursor=n+1
  if m[2]:positions.setdefault(n,set()).add(int(m[2],16));mapping.append((int(m[1]),n+1))
 procs=[];start=None
 for n,line in enumerate(lines):
  if re.search(r'\bPROC\s+(NEAR|FAR)',line,re.I):assert start is None;start=n
  if re.search(r'\bENDP\b',line,re.I):
   assert start is not None and len(positions.get(n,set()))==1;procs.append((start,n,next(iter(positions[n]))));start=None
 assert start is None and len(ordered_sites)==len(set(ordered_sites))
 selected={};owners={};replacements={};insertions={};audit=[]
 for site in ordered_sites:
  candidates=[]
  for n,aa in positions.items():
   line=lines[n].split(';')[0].strip()
   if len(aa)!=1:continue
   addr=next(iter(aa));size=None
   if re.match(r'call\s',line,re.I) and addr+3==site:size=5
   elif re.match(r'mov\s+(?:ax|bx|cx|dx|si|di|bp),\s*SEG\s',line,re.I)and addr+1==site:size=3
   elif re.match(r'add\s+(?:ax|bx|cx|dx|si|di|bp),\s*SEG\s',line,re.I)and addr+2==site:size=4
   elif re.match(r'mov\s+WORD PTR [^,]+,\s*SEG\s',line,re.I)and addr+4==site:size=6
   if size:candidates.append((n,addr,size))
  assert len(candidates)==1,('unique supported segment operand',site,candidates)
  n,addr,size=candidates[0];assert n not in selected;owner=next((x for x in procs if x[0]<n<x[1]),None);assert owner is not None
  selected[n]=(addr,size);owners[site]=owner;replacements[n]=f'    ORG 0{addr+size:X}h\r\n';audit.append({'site':site,'line':n+1,'instruction_offset':addr,'size':size,'procedure_line':owner[0]+1})
  insertions.setdefault(owner[1],[]).append((n,addr,lines[n]))
 # Order is expressed within procedure; never move symbols/instructions across procedures.
 assert [owners[s][0]for s in ordered_sites]==sorted(owners[s][0]for s in ordered_sites)
 out=[];edits=[];length=0
 def emit(value,original):
  nonlocal length
  if value!=original:edits.append((length,value,original))
  out.append(value);length+=len(value)
 for n,line in enumerate(lines):
  if n in insertions:
   inserted=''.join(f'    ORG 0{addr:X}h\r\n'+instruction for original,addr,instruction in insertions[n])
   end=next(x[2]for x in procs if x[1]==n);inserted+=f'    ORG 0{end:X}h\r\n';emit(inserted,'')
  emit(replacements.get(n,line),line)
 combined=''.join(out);inverse=combined
 for at,new,old in reversed(edits):
  assert inverse[at:at+len(new)]==new
  inverse=inverse[:at]+old+inverse[at+len(new):]
 assert inverse==text
 result=combined.encode()

 return result,{'source_sha256':H(source),'listing_sha256':H(listing),'result_sha256':H(result),'placements':audit,'all_source_lines_accounted_once_except_explicit_placement_directives':True,'exact_inverse_reconstructs_complete_source':True,'canonical_credit_added':0}
