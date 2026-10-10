import json,glob,re,sys
jobs=json.load(open('jobs.json'))
blocks={}
for f in sorted(glob.glob('out/*.txt')):
    for m in re.finditer(r'^@(\d+)\s*\n(.*?)(?=^@\d+|\Z)',open(f).read(),re.M|re.S):
        d={}
        for line in m.group(2).splitlines():
            mm=re.match(r'([HTDY]):\s*(.*)',line.strip())
            if mm: d[mm.group(1)]=mm.group(2).strip()
        blocks[int(m.group(1))]=d
bad=[]
for j in jobs:
    b=blocks.get(j['id'])
    if not b: continue
    t=[x.strip() for x in b.get('T','').split('|') if x.strip()]
    dd=[x.strip() for x in b.get('D','').split('|') if x.strip()]
    ok=b.get('H') and b.get('Y') and len(t)==4 and len(dd)==4 and all(re.match(r'\d{1,2}[:.]\d\d\s',x) for x in dd)
    if not ok: bad.append(j['id'])
miss=[j['id'] for j in jobs if j['id'] not in blocks]
print('gotowe',len(blocks),'/',len(jobs),'| brak',len(miss),'| wadliwe',len(bad),bad[:20])
json.dump({'miss':miss,'bad':bad},open('status.json','w'))
