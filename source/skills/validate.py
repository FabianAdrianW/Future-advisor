import json,glob,re,pathlib
B=pathlib.Path(__file__).resolve().parent
BAN=re.compile(r'komunikatywn|praca w zespole|odporność na stres|dokładność|kreatywność|cierpliwość|empati|organizacja pracy',re.I)
def parse():
    out={}
    for f in sorted(glob.glob(str(B/'out/*.txt'))):
        for m in re.finditer(r'^@(\d+)\s*\n(.*?)(?=^@\d+|\Z)',open(f,encoding='utf-8').read(),re.M|re.S):
            d={}
            for line in m.group(2).splitlines():
                mm=re.match(r'([MW]):\s*(.*)',line.strip())
                if mm: d[mm.group(1)]=[[y.strip() for y in x.split('::')] for x in mm.group(2).split('|') if x.strip()]
            out[int(m.group(1))]=d
    return out
def ok(d):
    m,w=d.get('M',[]),d.get('W',[])
    if not(4<=len(m)<=5 and 3<=len(w)<=4): return 'liczba'
    names=[]
    for it in m+w:
        if len(it)!=2 or not it[0] or not it[1]: return 'format'
        n,t=it; names.append(n.lower())
        if len(n.split())>6 or len(n)>48: return 'nazwa: '+n
        if not 5<=len(t.split())<=24: return 'zdanie: '+t
        if BAN.search(n): return 'ogólnik: '+n
    if len(set(names))!=len(names): return 'powtórka'
    return ''
if __name__=='__main__':
    jobs=json.load(open(B/'jobs.json')); bl=parse()
    bad=[(j['id'],ok(bl[j['id']])) for j in jobs if j['id'] in bl and ok(bl[j['id']])]
    miss=[j['id'] for j in jobs if j['id'] not in bl]
    print('gotowe',len(bl),'/',len(jobs),'| brak',len(miss),miss[:30],'| wadliwe',len(bad),bad[:20])
