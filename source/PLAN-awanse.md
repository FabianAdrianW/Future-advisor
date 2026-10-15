# Plan: kafelki „Dalej możesz” (awanse) — stan i sposób

## Stan
- Kafelki działają, ale tylko dla 2 zawodów (Magazynier, Operator wózka widłowego) — `source/awanse.json`.
- Drzewo zawodów (2334 zawody) nie zawiera ścieżek awansu. Stanowiska nadzorcze (Kierownik, Starszy, Główny) rzadko leżą w tej samej grupie co zawód bazowy: w grupach 9 zawodów z danymi z ogłoszeń znalazłem jedno takie stanowisko.
- Naiwne łączenie po nazwach daje ~3000 par, z czego większość błędnych. Nie używam go.

## Metoda
1. Zakres: zawody, które mają realną ścieżkę awansu (ok. 60–100 z pierwszych 300 najpopularniejszych).
2. Dla każdego zawodu 1–3 kroki awansu, wybrane ręcznie z listy stanowisk istniejących w `tree.json`.
3. Każdy wpis: `do` (nazwy z `tree.json`), `zrodlo` (np. „propozycja, do sprawdzenia przez praktyka” lub link do opisu zawodu), `pewnosc` (wysoka / średnia / niska).
4. Walidacja: każda nazwa z `do` musi być liściem w `tree.json` (sprawdza `build_ads.py`).
5. UI: kafelki z etykietą źródła i pewności; przy niskiej pewności dopisek „warto samemu sprawdzić”.
6. Research: opisy zawodów i stanowisk z ogłoszeń (liczba ogłoszeń na stanowisko), bez zewnętrznych stron agregujących wynagrodzenia.

## Szacunek
- Ręczne dobranie awansów dla ~60–100 zawodów: kilka godzin pracy, z weryfikacją ogłoszeń.
- Kod i UI są gotowe; dochodzi tylko weryfikacja i build.

## Pytanie
Czy zakres ~60–100 zawodów z najpopularniejszych jest w porządku, czy wolisz mniejszy pilotaż (np. 20 zawodów z danymi z ogłoszeń)?
