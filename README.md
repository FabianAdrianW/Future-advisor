# Future Advisor

Aplikacja mobilna (PWA) dla młodych ludzi: drzewo zawodów, opisy pracy, potrzebne umiejętności i plan dojścia do zawodu. Działa offline, bez serwera.

- `docs/` – gotowa aplikacja (do hostowania, np. GitHub Pages: Settings → Pages → branch `main`, folder `/docs`).
- `source/` – dane i skrypty budujące (`build_tree.py` → `decorate.py` → `build_pwa.py`), szablon `page2.tmpl.html`, opisy zawodów w `gen/out/`.

## Źródła i licencje
- Dane o zawodach: ESCO v1.0.8, Komisja Europejska (zmodyfikowane i uzupełnione).
- Ilustracje: Fluent Emoji, Microsoft (MIT).
- Czcionki: Figtree, Bricolage Grotesque (SIL OFL 1.1).

Opisy zawodów i listy umiejętności zostały napisane z pomocą AI i nie były weryfikowane przez praktyków.

## Umiejętności per zawód
`source/skills/` – „Musisz umieć” i „Warto umieć” dla 300 zawodów (lista w `jobs.json`, treść w `out/*.txt`, format w `INSTRUKCJA.md`, kontrola: `python3 skills/validate.py`). Pozostałe zawody pokazują cechy swojej grupy. Build: `python3 source/build_pwa.py` (pisze do `docs/`).

## Zarobki
Widełki to szacunek: mediana płac GUS dla grupy zawodów („Struktura wynagrodzeń według zawodów", październik 2024, w przeliczeniu na 2025 wg kalkulatory-place.pl) × korekta miasta (połowa różnicy między przeciętną płacą w mieście wojewódzkim a średnią krajową, GUS, marzec 2026, wg wynagrodzenia.pl). Widełki: od −20% do +25% wokół mediany, nie mniej niż płaca minimalna.
