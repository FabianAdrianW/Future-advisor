# Kompas karier

Aplikacja mobilna (PWA) dla młodych ludzi: drzewo zawodów, opisy pracy, potrzebne umiejętności i plan dojścia do zawodu. Działa offline, bez serwera.

- `docs/` – gotowa aplikacja (do hostowania, np. GitHub Pages: Settings → Pages → branch `main`, folder `/docs`).
- `docs/landing/` – strona informacyjna aplikacji (pod adresem `.../landing/`), osobny plik HTML bez bundlera, przyciski prowadzą do aplikacji w `docs/`.
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

## Rynek pracy
`source/market-2026.json` – karta „Rynek pracy w 2026” dla 163 grup zawodów i 7 zawodów własnych. Co rok podmienia się ten jeden plik (build bierze najnowszy `market-<rok>.json`). Plik składa `source/market/build_market.py` z:
- Barometru zawodów 2026 (popyt i etykieta: deficyt → Rośnie, równowaga → Stabilnie, lokalne nadwyżki → Trudniej, brak oceny → Brak oceny),
- komunikatu GUS „Struktura wynagrodzeń według zawodów za październik 2024 r.” (kierunek płac, tylko wielkie grupy),
- indeksu ILO–NASK 2025 ekspozycji na generatywną AI (`source/market/ilo-genai-2025.csv`, Gmyrek i in., ILO Working Paper 140),
- WEF Future of Jobs 2025 (tylko dla kilku zawodów własnych, perspektywa globalna).

Przypisanie naszych grup do zawodów z Barometru (`MAP` w skrypcie) zrobiono ręcznie i nie było weryfikowane. Gdzie źródło milczy, karta mówi to wprost.

## Aplikacja Android (Capacitor)
Opakowanie PWA z `docs/` w natywną aplikację. Plik `capacitor.config.json` ma `appId` `pl.kompaskarier.app` (placeholder): trzeba go ustalić przed pierwszą publikacją, bo późniejsza zmiana jest niemożliwa.
- Po każdej zmianie w `docs/`: `npm run sync`.
- Otwórz w Android Studio: `npm run open:android`, potem Build → Build APK / Generate Signed Bundle.
- iOS: `npx cap add ios` wymaga macOS z Xcode (jeszcze nie dodane).
