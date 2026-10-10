"""Sklada strone z szablonu i danych. Uzycie: python3 -I assemble.py"""
import pathlib
base = pathlib.Path(__file__).resolve().parent
raw = (base / 'app.json').read_text(encoding='utf-8')
tmpl = (base / 'page2.tmpl.html').read_text(encoding='utf-8')
assert tmpl.count('__DATA__') == 1
html = tmpl.replace('__DATA__', raw.replace('</', '<\\/').replace('<!--', '<\\u0021--'))
(base / 'drzewo-zawodow.html').write_text(html, encoding='utf-8')
js = tmpl[tmpl.rindex('<script>') + 8: tmpl.rindex('</script>')]
(base / 'check.js').write_text(js, encoding='utf-8')
mock = """<script>
window.claude = { use: function (name) {
  if (name !== 'sample') return Promise.resolve(null);
  var f = function () { return Promise.resolve({ text: '' }); };
  f.json = function () { return new Promise(function (ok) { setTimeout(function () { ok({ hook: 'Testowy opis: sprawdzasz, czy generowany profil dobrze się układa.', tasks: ['Pierwsza czynność', 'Druga czynność', 'Trzecia czynność', 'Czwarta czynność'], day: [['8:00', 'Początek dnia'], ['10:00', 'Główne zadanie'], ['13:00', 'Praca z ludźmi'], ['15:30', 'Podsumowanie']], skills: [['Dokładność', 'L'], ['Rozmowa', 'P'], ['Zręczność', 'R'], ['Pisanie', 'S'], ['Obserwacja', 'N'], ['Estetyka', 'O']], plus: ['Zaleta jeden', 'Zaleta dwa', 'Zaleta trzy'], minus: ['Wada jeden', 'Wada dwa', 'Wada trzy'], routes: [{ n: 'Droga testowa', s: [['szkola', 'Szkoła testowa', 3], ['kurs', 'Kurs testowy', 0.5], ['egzamin', 'Egzamin testowy', 0]] }], try: 'Zadanie testowe na dziś.' }); }, 500); }); };
  return Promise.resolve(f);
} };
</script>"""
skel = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>'
(base / 'site' / 'preview.html').write_text(skel + mock + html + '</body></html>', encoding='utf-8')
print(len(html) // 1024, 'KB')
