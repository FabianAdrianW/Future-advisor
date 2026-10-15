import json
F = 'chrome_partia.json'
def load():
    return json.load(open(F, encoding='utf-8'))
def add(nazwa, kod, oferty, strona=None):
    d = load()
    d['zawody'][nazwa] = {'kod_gus': kod, 'n_ogloszen_strona': strona, 'oferty': oferty}
    json.dump(d, open(F, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def med(nazwa):
    import statistics
    v = [ (int(o[1]) + int(o[2])) / 2 for o in load()['zawody'][nazwa]['oferty'] ]
    return len(v), round(statistics.median(v))
