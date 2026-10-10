"""Buduje drzewo zawodow: 6 korzeni -> obszary -> grupy ISCO -> zawody ESCO.
Uzycie: python3 -I build_tree.py <katalog labourR/data-raw> <plik wyjsciowy .json>
"""
import csv, json, sys, re, collections, statistics

csv.field_size_limit(10**9)
RAW, OUT = sys.argv[1], sys.argv[2]

ROOTS = ["L", "S", "P", "R", "N", "O"]  # Liczby, Slowo, Ludzie, Rece, Natura, Obraz

AREAS = {
    "it": "Informatyka i dane",
    "nauka": "Nauki ścisłe",
    "przyr": "Przyroda i środowisko",
    "inz": "Inżynieria i technika",
    "bud": "Budownictwo i architektura",
    "prod": "Przemysł i produkcja",
    "mech": "Mechanika i elektryka",
    "rzem": "Rzemiosło",
    "trans": "Transport i logistyka",
    "roln": "Rolnictwo, las i zwierzęta",
    "zdrowie": "Medycyna i zdrowie",
    "opieka": "Opieka i pomoc ludziom",
    "edu": "Edukacja",
    "spol": "Człowiek, społeczeństwo, kultura",
    "prawo": "Prawo i urzędy",
    "biznes": "Zarządzanie i biznes",
    "fin": "Finanse",
    "sprzed": "Sprzedaż i marketing",
    "biuro": "Biuro i administracja",
    "media": "Media, język i literatura",
    "sztuka": "Sztuka, scena i film",
    "design": "Projektowanie i grafika",
    "gastro": "Gastronomia, hotele, turystyka",
    "uslugi": "Uroda, dom i usługi osobiste",
    "sport": "Sport i rekreacja",
    "bezp": "Bezpieczeństwo i wojsko",
}

# kod ISCO (3 cyfry = grupa, 4 cyfry = nadpisanie) | obszar | wagi L S P R N O | krotka nazwa (tylko 3 cyfry)
MAP = """
011 bezp 0 1 5 3 1 0 | Oficerowie
021 bezp 0 0 5 4 1 0 | Podoficerowie
031 bezp 0 0 3 5 2 0 | Żołnierze
111 prawo 1 4 5 0 0 0 | Politycy i wyżsi urzędnicy
112 biznes 4 1 5 0 0 0 | Dyrektorzy generalni
121 biznes 5 1 4 0 0 0 | Kierownicy administracji i strategii
1211 fin 7 0 3 0 0 0
122 sprzed 2 3 5 0 0 0 | Kierownicy sprzedaży i marketingu
1223 biznes 5 0 3 2 0 0
131 roln 2 0 3 2 3 0 | Kierownicy w rolnictwie i rybactwie
132 prod 3 0 3 4 0 0 | Kierownicy produkcji
1323 bud 2 0 3 5 0 0
1324 trans 4 0 3 3 0 0
133 it 6 0 3 1 0 0 | Kierownicy IT
134 biznes 4 2 4 0 0 0 | Kierownicy usług profesjonalnych
1341 opieka 1 0 7 0 2 0
1342 zdrowie 2 0 3 0 5 0
1343 opieka 1 0 6 0 3 0
1344 opieka 1 1 7 0 1 0
1345 edu 1 3 6 0 0 0
1346 fin 7 0 3 0 0 0
141 gastro 3 0 6 1 0 0 | Kierownicy hoteli i restauracji
142 sprzed 3 1 6 0 0 0 | Kierownicy sklepów i hurtowni
143 sport 2 0 5 0 3 0 | Kierownicy sportu, rekreacji i kultury
1439 uslugi 2 0 6 2 0 0
211 nauka 5 0 0 1 4 0 | Fizycy, chemicy i geolodzy
212 nauka 10 0 0 0 0 0 | Matematycy i statystycy
213 przyr 3 0 0 0 7 0 | Biolodzy i specjaliści środowiska
214 inz 6 0 0 4 0 0 | Inżynierowie
2142 bud 5 0 0 4 0 1
2143 przyr 5 0 0 2 3 0
215 inz 6 0 0 4 0 0 | Inżynierowie elektrycy i elektronicy
216 design 2 0 2 0 0 6 | Architekci i projektanci
2161 bud 3 0 1 2 0 4
2162 bud 2 0 1 1 2 4
2163 design 2 0 1 2 0 5
2164 bud 4 1 2 1 0 2
2165 bud 6 0 0 2 1 1
221 zdrowie 2 0 3 0 5 0 | Lekarze
222 zdrowie 0 0 4 1 5 0 | Pielęgniarki i położne
223 zdrowie 0 1 3 1 5 0 | Medycyna komplementarna
224 zdrowie 0 0 4 1 5 0 | Ratownicy medyczni
225 roln 2 0 1 1 6 0 | Lekarze weterynarii
226 zdrowie 2 0 3 1 4 0 | Dentyści, farmaceuci, fizjoterapeuci
231 edu 2 4 4 0 0 0 | Nauczyciele akademiccy
232 edu 0 2 5 3 0 0 | Nauczyciele zawodu
233 edu 1 4 5 0 0 0 | Nauczyciele szkół średnich
234 edu 0 3 6 0 0 1 | Nauczyciele szkół podstawowych i przedszkoli
235 edu 0 3 6 0 0 1 | Pedagodzy, lektorzy i instruktorzy
241 fin 8 0 2 0 0 0 | Księgowi, doradcy i analitycy finansowi
242 biznes 4 2 4 0 0 0 | Specjaliści HR i organizacji
243 sprzed 1 3 5 0 0 1 | Specjaliści marketingu, PR i sprzedaży
251 it 8 0 1 1 0 0 | Programiści i analitycy
2513 design 4 0 1 0 0 5
252 it 8 0 0 2 0 0 | Bazy danych i sieci
261 prawo 2 6 2 0 0 0 | Prawnicy
262 spol 2 6 1 0 0 1 | Archiwiści, muzealnicy, bibliotekarze
263 spol 2 4 4 0 0 0 | Nauki społeczne i religia
2631 fin 7 1 2 0 0 0
2634 spol 2 2 6 0 0 0
2635 opieka 0 2 8 0 0 0
2636 spol 0 5 5 0 0 0
264 media 0 8 1 0 0 1 | Pisarze, dziennikarze, tłumacze
265 sztuka 0 2 1 0 0 7 | Artyści i twórcy
2656 media 0 6 3 0 0 1
311 inz 4 0 0 6 0 0 | Technicy
3111 nauka 5 0 0 3 2 0
3112 bud 3 0 0 6 0 1
3118 inz 4 0 0 3 0 3
312 prod 2 0 3 5 0 0 | Mistrzowie produkcji
3123 bud 2 0 3 5 0 0
313 prod 4 0 0 6 0 0 | Energetyka i sterowanie procesami
314 przyr 3 0 0 2 5 0 | Technicy biologii, rolnictwa i leśnictwa
315 trans 4 0 1 5 0 0 | Piloci, oficerowie statków, kontrolerzy lotów
321 zdrowie 3 0 1 2 4 0 | Technicy medyczni i farmaceutyczni
322 zdrowie 0 0 4 1 5 0 | Asystenci pielęgniarstwa i położnictwa
323 zdrowie 0 1 3 1 5 0 | Asystenci medycyny komplementarnej
324 roln 1 0 1 2 6 0 | Technicy weterynarii
325 zdrowie 1 0 3 2 4 0 | Asystenci i technicy ochrony zdrowia
3257 przyr 3 1 2 1 3 0
331 fin 7 0 3 0 0 0 | Maklerzy, kredyty, rachunkowość
332 sprzed 2 2 6 0 0 0 | Agenci, handlowcy i zaopatrzeniowcy
333 sprzed 2 2 6 0 0 0 | Agenci usług biznesowych
3331 trans 4 1 3 2 0 0
3332 gastro 2 1 5 0 0 2
3333 biznes 2 2 6 0 0 0
334 biuro 3 4 3 0 0 0 | Kierownicy biura i sekretarze
335 prawo 3 4 3 0 0 0 | Urzędnicy kontroli i nadzoru
3351 bezp 2 2 4 2 0 0
3355 bezp 3 1 4 2 0 0
341 opieka 0 2 7 0 1 0 | Pomoc społeczna, prawo, religia
3411 prawo 2 6 2 0 0 0
3412 opieka 0 1 8 0 1 0
3413 spol 0 5 5 0 0 0
342 sport 0 0 4 0 6 0 | Sportowcy, trenerzy, instruktorzy
343 sztuka 0 1 1 3 0 5 | Technicy sztuki i kultury
3431 design 1 0 1 2 0 6
3432 design 1 0 2 1 0 6
3434 gastro 1 0 3 4 0 2
351 it 5 0 2 3 0 0 | Technicy IT i wsparcie użytkowników
352 sztuka 2 0 0 3 0 5 | Technicy dźwięku, obrazu i nadawania
3522 it 5 0 0 5 0 0
411 biuro 3 4 3 0 0 0 | Pracownicy biurowi
412 biuro 2 5 3 0 0 0 | Sekretarze
413 biuro 4 4 0 2 0 0 | Wprowadzanie danych
421 fin 6 0 4 0 0 0 | Kasjerzy, krupierzy, windykatorzy
422 biuro 1 3 6 0 0 0 | Recepcja i informacja
4221 gastro 1 2 6 0 1 0
4224 gastro 1 2 7 0 0 0
431 fin 8 1 1 0 0 0 | Pracownicy księgowości i statystyki
432 trans 4 0 1 5 0 0 | Magazyn i ewidencja transportu
441 biuro 2 5 2 1 0 0 | Inni pracownicy biurowi
511 trans 0 1 6 3 0 0 | Stewardzi i konduktorzy
5113 gastro 0 4 5 0 1 0
512 gastro 0 0 2 6 0 2 | Kucharze
513 gastro 0 0 7 3 0 0 | Kelnerzy i barmani
514 uslugi 0 0 5 3 0 2 | Fryzjerzy i kosmetyczki
515 uslugi 1 0 4 5 0 0 | Gospodarze budynków i domów
516 uslugi 0 1 6 2 1 0 | Inne usługi osobiste
5164 roln 0 0 2 2 6 0
5165 trans 0 0 6 4 0 0
521 sprzed 1 0 7 2 0 0 | Sprzedawcy uliczni i targowi
522 sprzed 1 1 7 1 0 0 | Sprzedawcy w sklepach
523 sprzed 3 0 6 1 0 0 | Kasjerzy i sprzedawcy biletów
524 sprzed 1 2 6 0 0 1 | Inni sprzedawcy
5241 sztuka 0 0 3 0 1 6
5246 gastro 0 0 6 4 0 0
531 opieka 0 1 8 0 1 0 | Opieka nad dziećmi
5312 edu 0 2 7 0 0 1
532 zdrowie 0 0 5 1 4 0 | Opiekunowie medyczni
541 bezp 0 0 4 4 2 0 | Strażacy, policjanci, ochrona
611 roln 1 0 0 4 5 0 | Rolnicy, sadownicy, ogrodnicy
612 roln 1 0 0 3 6 0 | Hodowcy zwierząt
613 roln 1 0 0 4 5 0 | Rolnicy upraw i hodowli
621 roln 0 0 0 5 5 0 | Robotnicy leśni
622 roln 0 0 0 5 5 0 | Rybacy i hodowcy ryb
711 bud 1 0 0 8 0 1 | Murarze, betoniarze, cieśle
712 bud 1 0 0 8 0 1 | Wykończenia i instalacje
713 bud 0 0 0 7 0 3 | Malarze i lakiernicy
721 mech 1 0 0 9 0 0 | Spawacze, blacharze, monterzy konstrukcji
722 mech 2 0 0 8 0 0 | Kowale, ślusarze, operatorzy obrabiarek
723 mech 2 0 0 8 0 0 | Mechanicy maszyn i pojazdów
731 rzem 1 0 0 5 0 4 | Rzemieślnicy artystyczni i precyzyjni
732 rzem 1 1 0 5 0 3 | Poligrafia i druk
741 mech 3 0 0 7 0 0 | Elektrycy i elektromonterzy
742 mech 3 0 0 7 0 0 | Elektronicy i monterzy telekomunikacji
751 prod 0 0 0 7 2 1 | Przetwórstwo spożywcze
7512 gastro 0 0 1 7 0 2
752 rzem 1 0 0 7 0 2 | Stolarze i obróbka drewna
753 rzem 0 0 0 6 0 4 | Krawcy, szewcy, tapicerzy
754 prod 2 0 0 6 2 0 | Kontrolerzy jakości i inni
811 prod 1 0 0 8 1 0 | Górnictwo i wydobycie
812 prod 1 0 0 9 0 0 | Obróbka metalu
813 prod 2 0 0 7 1 0 | Produkcja chemiczna
814 prod 1 0 0 9 0 0 | Guma, tworzywa i papier
815 prod 0 0 0 9 0 1 | Tekstylia, skóra i obuwie
816 prod 0 0 0 8 2 0 | Maszyny przemysłu spożywczego
817 prod 0 0 0 9 1 0 | Obróbka drewna i produkcja papieru
818 prod 1 0 0 9 0 0 | Inne maszyny przetwórcze
821 prod 2 0 0 8 0 0 | Monterzy maszyn i sprzętu
831 trans 2 0 1 7 0 0 | Kolej
832 trans 0 0 4 6 0 0 | Kierowcy aut osobowych i motocykli
833 trans 0 0 3 7 0 0 | Kierowcy ciężarówek i autobusów
834 bud 1 0 0 9 0 0 | Operatorzy koparek, dźwigów i maszyn
8341 roln 0 0 0 6 4 0
835 trans 0 0 2 7 1 0 | Marynarze
911 uslugi 0 0 3 7 0 0 | Sprzątanie domów, hoteli i biur
912 uslugi 0 0 2 8 0 0 | Mycie pojazdów, okien i pranie
921 roln 0 0 0 5 5 0 | Pomocnicy w rolnictwie i leśnictwie
931 bud 0 0 0 10 0 0 | Pomocnicy w budownictwie i górnictwie
932 prod 0 0 1 9 0 0 | Pakowacze i prace proste w przemyśle
933 trans 0 0 1 9 0 0 | Ładowacze i pomocnicy transportu
941 gastro 0 0 3 7 0 0 | Pomoce kuchenne
951 uslugi 0 0 6 4 0 0 | Usługi uliczne
952 sprzed 1 0 7 2 0 0 | Sprzedawcy uliczni
961 przyr 0 0 1 6 3 0 | Odpady i recykling
962 uslugi 1 0 4 5 0 0 | Kurierzy i prace dorywcze
"""

m3, m4 = {}, {}
for line in MAP.strip().splitlines():
    left, _, short = line.partition("|")
    p = left.split()
    code, area, w = p[0], p[1], [int(x) for x in p[2:8]]
    assert area in AREAS, area
    assert len(w) == 6 and sum(w) == 10, (code, w)
    (m3 if len(code) == 3 else m4)[code] = (area, w, short.strip())

def cap(s):
    s = s.strip()
    return s[:1].upper() + s[1:]

def clean_group(s):
    s = re.sub(r"\s+gdzie indziej niesklasyfikowan[iey]", " (pozostali)", s.strip())
    return cap(s)

def short_desc(s, limit=640):
    s = re.sub(r"\s+", " ", s.strip())
    if len(s) <= limit:
        return s
    cut = s[:limit]
    i = max(cut.rfind(". "), cut.rfind("; "))
    if i > 120:
        return cut[: i + 1]
    return cut[: cut.rfind(" ")] + "…"

occ = list(csv.DictReader(open(f"{RAW}/esco_bundle_occupations_1.0.8/occupations_pl.csv", encoding="utf-8")))
isco = {r["code"]: r["preferredLabel"] for r in csv.DictReader(open(f"{RAW}/isco_bundle_occupations_1.0.8/ISCOGroups_pl.csv", encoding="utf-8"))}

def leaf(r, w):
    alts = [a.strip() for a in r["altLabels"].split("\n") if a.strip()]
    return {"n": cap(r["preferredLabel"]), "w": w, "d": short_desc(r["description"]), "a": alts[:6], "code": r["code"], "u": r["iscoGroup"]}

def first_word(name):
    return re.split(r"[\s/\-–]+", name.lower())[0]

def similar(names, share=0.6):
    """Czy nazwy to odmiany jednego zawodu (wspolne pierwsze slowo)."""
    c = collections.Counter(first_word(n) for n in names)
    return c.most_common(1)[0][1] / len(names) >= share

BUNDLE_MIN = 8   # od tylu podobnych odmian zwijamy je w jeden wezel ("pek")
FLAT = 9         # grupa o tylu lub mniej zawodach nie dostaje podgrup

def spec(l):
    return {"n": l["n"], "d": short_desc(l["d"], 300)}

def level5_nodes(leaves):
    """Zawody poziomu 5 ESCO; wezsze zawody staja sie odmianami albo galezia."""
    by5 = collections.defaultdict(list)
    for l in leaves:
        by5[".".join(l["code"].split(".")[:2])].append(l)
    out = []
    for key, ls in by5.items():
        head = next((l for l in ls if l["code"] == key), None)
        rest = sorted((l for l in ls if l is not head), key=lambda l: l["n"])
        if head is None:
            out.extend(rest)
        elif not rest:
            out.append(head)
        elif len(rest) >= BUNDLE_MIN and similar([l["n"] for l in rest]):
            head["s"] = [spec(l) for l in rest]          # pek odmian
            out.append(head)
        else:
            general = dict(head); general["g"] = 1        # "ogolnie"
            out.append({"n": head["n"], "c": [general] + rest, "job": 1})
    return out

def unit_node(label, leaves, w):
    nodes = level5_nodes(leaves)
    plain = [n for n in nodes if "c" not in n and "s" not in n]
    if len(nodes) == 1:
        return nodes[0]
    if len(plain) >= 12 and len(plain) == len(nodes) and similar([n["n"] for n in plain]):
        return {"n": label, "w": w, "d": "", "a": [], "s": [spec(l) for l in sorted(plain, key=lambda l: l["n"])], "fam": 1, "u": plain[0]["u"]}
    return {"n": label, "c": nodes}

# area -> minor(3) -> unit(4) -> [occupations]
tree = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))
for r in occ:
    u = r["iscoGroup"]
    area, w, _ = m4.get(u) or m3[u[:3]]
    tree[area][u[:3]][u].append(leaf(r, w))

def count(n):
    if "c" in n:
        return sum(count(c) for c in n["c"])
    return 1 + len(n.get("s", [])) - (1 if n.get("fam") else 0)

def mean_w(n):
    if "c" not in n:
        return n["w"]
    acc, tot = [0.0] * 6, 0
    for c in n["c"]:
        k, w = count(c), mean_w(c)
        tot += k
        for i in range(6):
            acc[i] += w[i] * k
    return [a / tot for a in acc]

areas = []
for aid, minors in tree.items():
    groups = []
    for m, units in minors.items():
        unit_nodes = []
        before = len(groups)
        for u, leaves in units.items():
            w = (m4.get(u) or m3[u[:3]])[1]
            unit_nodes.append(unit_node(clean_group(isco[u]), leaves, w))
            unit_nodes[-1].setdefault("u", u)
        label = m3[m][2] or clean_group(isco[m])
        if m3[m][0] != aid:
            # grupy przeniesione z innego obszaru: nazwa grupy nadrzednej by myliła
            groups.extend(unit_nodes)
            continue
        total = sum(count(x) for x in unit_nodes)
        kids = sum(len(x["c"]) if "c" in x else 1 for x in unit_nodes)
        if len(unit_nodes) == 1:
            x = unit_nodes[0]
            groups.append({"n": label, "c": x["c"]} if "c" in x else x)
        elif kids <= FLAT:
            flat = []
            for x in unit_nodes:
                flat.extend(x["c"] if "c" in x else [x])
            groups.append({"n": label, "c": flat})
        else:
            groups.append({"n": label, "c": unit_nodes})
        for g in groups[before:]:
            g.setdefault("m", m)
    areas.append({"n": AREAS[aid], "id": aid, "c": groups})

def finalize(n):
    if "c" in n:
        for c in n["c"]:
            finalize(c)
        n["k"] = count(n)
        n["w"] = [round(x, 1) for x in mean_w(n)]
        n["c"].sort(key=lambda c: (-c.get("k", 0), c["n"]))
        us = [c["u"] for c in n["c"]]
        pre = us[0]
        for x in us[1:]:
            while not x.startswith(pre):
                pre = pre[:-1]
        n["u"] = pre
    n.pop("code", None)

for a in areas:
    finalize(a)
areas.sort(key=lambda a: -a["k"])

# ---- statystyki ----
depths, fan, bundles = [], [], []
def walk(n, d):
    if "c" in n:
        fan.append((len(n["c"]), n["n"]))
        for c in n["c"]:
            walk(c, d + 1)
    else:
        depths.append(d)                       # zawod albo pek
        if n.get("s"):
            bundles.append((len(n["s"]), n["n"]))
            depths.extend([d + 1] * len(n["s"]))
            if n.get("fam"):
                depths.pop()
for a in areas:
    walk(a, 2)  # korzen = 1 dotkniecie, obszar = 2
total = sum(a["k"] for a in areas)
print("zawody:", total, "obszary:", len(areas), "galezie:", len(fan), "peki odmian:", len(bundles), "zawodow w pekach:", sum(b for b, _ in bundles))
print("dotkniecia do zawodu:", sorted(collections.Counter(depths).items()), "srednio", round(statistics.mean(depths), 2))
fs = sorted(f for f, _ in fan)
print("dzieci na galaz: mediana", statistics.median(fs), "p90", fs[int(len(fs) * 0.9)], "max", fs[-1])
print("galezie >7 dzieci:", sum(1 for f in fs if f > 7), "/", len(fs), " >14:", sum(1 for f in fs if f > 14), " >21:", sum(1 for f in fs if f > 21))
print("najszersze:", sorted(fan, reverse=True)[:10])
print("najwieksze peki:", sorted(bundles, reverse=True)[:8])
for a in areas:
    w = a["w"]
    mem = "".join(ROOTS[i] for i in range(6) if w[i] >= 2.5)
    print(f"{a['n']:<34} {a['k']:>4}  dzieci {len(a['c']):>2}  wagi {w}  korzenie {mem}")
per_root, prim = collections.Counter(), collections.Counter()
for a in areas:
    prim[ROOTS[a["w"].index(max(a["w"]))]] += 1
    for i in range(6):
        if a["w"][i] >= 2.5:
            per_root[ROOTS[i]] += 1
print("obszary na korzen:", dict(per_root), "glowny korzen:", dict(prim))
STATS = {"total": total, "areas": len(areas), "branches": len(fan), "bundles": len(bundles),
         "avgTaps": round(statistics.mean(depths), 1), "maxTaps": max(depths),
         "wide": sum(1 for f in fs if f > 7), "median": int(statistics.median(fs)), "bundled": sum(b for b, _ in bundles)}

json.dump({"areas": areas, "stats": STATS}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
import os
print("rozmiar JSON:", os.path.getsize(OUT) // 1024, "KB")
