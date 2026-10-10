import json,re,glob,pathlib,shutil,hashlib
from PIL import Image
B=pathlib.Path(__file__).resolve().parent
# 1. opisy
jobs={j['id']:j['name'] for j in json.load(open(B/'gen/jobs.json'))}
gen={}
for f in sorted(glob.glob(str(B/'gen/out/*.txt'))):
    for m in re.finditer(r'^@(\d+)\s*\n(.*?)(?=^@\d+|\Z)',open(f,encoding='utf-8').read(),re.M|re.S):
        d={}
        for line in m.group(2).splitlines():
            mm=re.match(r'([HTDY]):\s*(.*)',line.strip())
            if mm: d[mm.group(1)]=mm.group(2).strip()
        day=[]
        for x in d['D'].split('|'):
            t=re.match(r'\s*(\d{1,2})[:.](\d\d)\s+(.*)',x); day.append([t.group(1)+':'+t.group(2),t.group(3).strip()])
        gen[jobs[int(m.group(1))]]={'hook':d['H'],'tasks':[x.strip() for x in d['T'].split('|') if x.strip()],'day':day,'try':d['Y']}
assert len(gen)==len(jobs),(len(gen),len(jobs))
data=json.loads((B/'app.json').read_text(encoding='utf-8')); data['gen']=gen
raw=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/').replace('<!--','<\\u0021--')
# 2. szablon bez AI
t=(B/'page2.tmpl.html').read_text(encoding='utf-8')
def sub(a,b):
    global t
    assert t.count(a)==1,a; t=t.replace(a,b)
sub("  var GEN = {};\n  var genGet = function (name) { if (GEN[name]) return GEN[name]; try { var g = JSON.parse(localStorage.getItem('fa.gen.' + name)); if (g) GEN[name] = g; return g; } catch (e) { return null; } };",
    "  var GEN = JSON.parse(document.getElementById('data').textContent).gen || {};\n  var genGet = function (name) { return GEN[name] || null; };")
a=t.index("  var sampleState = 'unknown', sampleP"); b=t.index("  function paintDetails()")
t=t[:a]+"  var sampleState = 'none', sampleP = Promise.resolve(null);\n"+t[b:]
sub('<title>Prototyp drzewa zawodów</title>','<title>Future Advisor</title>')
art=t.replace('__DATA__',raw)
(B/'drzewo-zawodow.html').write_text(art,encoding='utf-8')
# 3. PWA
P=B/'pwa'; shutil.rmtree(P,ignore_errors=True); (P/'img').mkdir(parents=True); (P/'fonts').mkdir()
for f in (B/'site/img').glob('*.webp'): shutil.copy(f,P/'img')
F=B/'fonts/node_modules/@fontsource-variable'
ff=[('Figtree','figtree','wght','400 800'),('Bricolage Grotesque','bricolage-grotesque','opsz','400 800')]
LAT='U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD'
EXT='U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF'
css=''
for fam,slug,ax,w in ff:
    for sub_,ur in (('latin',LAT),('latin-ext',EXT)):
        n=f'{slug}-{sub_}-{ax}-normal.woff2'; shutil.copy(F/slug/'files'/n,P/'fonts'/n)
        css+=f"@font-face{{font-family:'{fam}';font-style:normal;font-display:swap;font-weight:{w};src:url(fonts/{n}) format('woff2');unicode-range:{ur}}}\n"
link=re.search(r'<link rel="stylesheet" href="https://fonts.googleapis[^>]+>',t).group(0)
page=t.replace(link,'<style>\n'+css+'</style>').replace('__DATA__',raw)
src=Image.open(B/'site/img/compass.webp').convert('RGBA')
for s,name,pad in ((192,'icon-192.png',.16),(512,'icon-512.png',.16),(512,'icon-maskable.png',.26),(180,'apple-touch-icon.png',.16)):
    im=Image.new('RGBA',(s,s),'#3A66F5'); k=int(s*(1-2*pad)); e=src.resize((k,k),Image.LANCZOS); im.paste(e,((s-k)//2,(s-k)//2),e); im.convert('RGB').save(P/name)
json.dump({"name":"Future Advisor","short_name":"Future Advisor","description":"Drzewo zawodów: sprawdź, co można robić w życiu i zaplanuj drogę.","lang":"pl","start_url":"./","scope":"./","display":"standalone","orientation":"portrait","background_color":"#F4F5FA","theme_color":"#F4F5FA",
 "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"},{"src":"icon-maskable.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]},open(P/'manifest.webmanifest','w'),ensure_ascii=False)
head='<!doctype html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#F4F5FA"><meta name="description" content="Drzewo zawodów: sprawdź, co można robić w życiu i zaplanuj drogę."><link rel="manifest" href="manifest.webmanifest"><link rel="icon" href="icon-192.png"><link rel="apple-touch-icon" href="apple-touch-icon.png"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="default"><style>body{margin:0}[hidden]{display:none!important}.app{padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom);box-sizing:border-box}html,body{overscroll-behavior:none}</style></head><body>'
tail="<script>if('serviceWorker' in navigator)addEventListener('load',function(){navigator.serviceWorker.register('sw.js')});</script></body></html>"
(P/'index.html').write_text(head+page+tail,encoding='utf-8')
files=['./','index.html','manifest.webmanifest']+sorted(str(p.relative_to(P)) for p in P.rglob('*') if p.is_file() and p.name not in('index.html','manifest.webmanifest','sw.js'))
ver=hashlib.md5((P/'index.html').read_bytes()).hexdigest()[:8]
(P/'sw.js').write_text("var C='fa-"+ver+"',F="+json.dumps(files)+""";
self.addEventListener('install',function(e){e.waitUntil(caches.open(C).then(function(c){return c.addAll(F)}).then(function(){return self.skipWaiting()}))});
self.addEventListener('activate',function(e){e.waitUntil(caches.keys().then(function(k){return Promise.all(k.filter(function(x){return x!==C}).map(function(x){return caches.delete(x)}))}).then(function(){return self.clients.claim()}))});
self.addEventListener('fetch',function(e){if(e.request.method!=='GET')return;e.respondWith(caches.match(e.request,{ignoreSearch:true}).then(function(r){return r||fetch(e.request)}))});
""")
(P/'LICENCJE.txt').write_text("Dane o zawodach: ESCO v1.0.8, Komisja Europejska (zmodyfikowane i uzupełnione). Wykorzystanie zgodne z warunkami ESCO, z podaniem źródła.\nIlustracje: Fluent Emoji, Microsoft, licencja MIT.\nCzcionki: Figtree, Bricolage Grotesque, licencja SIL OFL 1.1.\n",encoding='utf-8')
shutil.make_archive(str(B/'future-advisor-pwa'),'zip',P)
print(len(gen),len(page)//1024,'KB', sum(p.stat().st_size for p in P.rglob('*') if p.is_file())//1024,'KB razem')
