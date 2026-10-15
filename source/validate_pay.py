"""Sprawdza dane zarobków przed buildem. Uruchom: python3 source/validate_pay.py"""
import json, sys, os
here = os.path.dirname(os.path.abspath(__file__))
errs, warns = [], []
codes = {}
for pair in open(os.path.join(here, 'pay_codes.txt'), encoding='utf-8').read().replace('\n', '|').split('|'):
    p = pair.split()
    if len(p) == 2:
        codes[p[0]] = int(p[1])
gus = json.load(open(os.path.join(here, 'pay_gus2024.json'), encoding='utf-8'))
f = gus['przelicznik_2025']
for c, v in codes.items():
    if v < 4806:
        warns.append(f'kod {c}: {v} zł poniżej płacy minimalnej 4806 zł (aplikacja podnosi do minimum przy wyświetlaniu)')
    g = gus['grupy'].get(c) if isinstance(gus.get('grupy'), dict) else None
    if g and abs(g['med'] * f - v) > 2:
        warns.append(f'kod {c}: {v} zł różni się od GUS×przelicznik ({round(g["med"]*f)} zł)')
for c, g in (gus.get('grupy') or {}).items():
    if c in codes and g.get('p25') and g.get('p75') and not (g['p25'] <= g['med'] <= g['p75']):
        errs.append(f'grupa {c}: mediana poza przedziałem P25–P75')
ods = os.path.join(here, 'pay_ogloszenia_pilot.json')
if os.path.exists(ods):
    pilot = json.load(open(ods, encoding='utf-8'))
    if 'partia2_wygasle' not in pilot:
        warns.append('brak oznaczenia partii wygasłych ogłoszeń')
ch = os.path.join(here, 'pay', 'chrome_partia.json')
if os.path.exists(ch):
    d = json.load(open(ch, encoding='utf-8'))['zawody']
    for name, v in d.items():
        for o in v['oferty']:
            if int(o[1]) > int(o[2]):
                errs.append(f'{name}: od > do ({o[1]} > {o[2]})')
        if len(v['oferty']) < 3:
            warns.append(f'{name}: n={len(v["oferty"])} (poniżej 3, nie porównywać)')
for w in warns: print('UWAGA:', w)
for e in errs: print('BŁĄD:', e)
print(f'{len(errs)} błędów, {len(warns)} uwag')
sys.exit(1 if errs else 0)
