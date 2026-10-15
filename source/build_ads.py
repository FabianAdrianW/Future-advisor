"""Buduje ads.json (porównanie z ogłoszeniami) i sprawdza awanse.json. Uruchom przed build_pwa.py."""
import json, statistics, os
here = os.path.dirname(os.path.abspath(__file__))
# nazwa z aplikacji -> nazwa próbki (tylko dopasowania, które są tym samym zawodem)
ALIAS = {'Kelner/kelnerka': 'Kelner', 'Fryzjer/fryzjerka': 'Fryzjer',
         'Sprzedawca/sprzedawczyni': 'Sprzedawca', 'Elektryk': 'Elektryk', 'Magazynier': 'Magazynier',
         'Hydraulik': 'Hydraulik', 'Spawacz': 'Spawacz', 'Murarz': 'Murarz',
         'Operator wózka widłowego': 'Operator wózka widłowego'}
d = json.load(open(os.path.join(here, 'pay', 'chrome_partia.json'), encoding='utf-8'))['zawody']
out = {}
for app_name, sample in ALIAS.items():
    v = d.get(sample)
    if not v or len(v['oferty']) < 3:
        continue
    vals = sorted((int(o[1]) + int(o[2])) / 2 for o in v['oferty'])
    dates = sorted(o[3] for o in v['oferty'])
    q = statistics.quantiles(vals, n=4) if len(vals) >= 4 else [vals[0], vals[-1]]
    out[app_name] = {'n': len(vals), 'med': round(statistics.median(vals)),
                     'lo': round(q[0]), 'hi': round(q[-1]),
                     'od': dates[0][8:10] + '.' + dates[0][5:7], 'do': dates[-1][8:10] + '.' + dates[-1][5:7]}
json.dump(out, open(os.path.join(here, 'ads.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ads:', len(out))
awanse = json.load(open(os.path.join(here, 'awanse.json'), encoding='utf-8'))
tree = open(os.path.join(here, 'tree.json'), encoding='utf-8').read()
bad = [t for k, v in awanse.items() for t in v['do'] if ('"n":"%s"' % t) not in tree]
for b in bad: print('UWAGA: nie ma w drzewie zawodów:', b)
print('awanse:', len(awanse))
