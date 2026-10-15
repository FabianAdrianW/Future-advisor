# Plan: dokładne zarobki w Kompasie karier

Stan na 2026-10-15. Plan jest pisany tak, żeby większość wykonał Claude w repo; poniżej zaznaczono, co wymaga Fabiana.

## 1. Diagnoza (zrobiona)

Zarobki liczone są z mediany GUS dla **grupy zawodów** (kody ISCO 2–3 cyfry w `pay_codes.txt`), potem × korekta miasta, a widełki to sztywne −20% / +25% wokół mediany.

| Miara | Wynik |
|---|---|
| Zawody w aplikacji (liście drzewa) | 2368 |
| Różne mediany płac | **119** |
| Zawody dzielące medianę z innym zawodem | 2364 (prawie wszystkie) |
| Największa grupa z jedną medianą | 106 zawodów (8 607 zł) |
| Dopasowanie do kodu 3-cyfrowego / 2-cyfrowego / brak | 2248 / 90 / 30 |

Wniosek: identyczne widełki u różnych zawodów to nie błąd pojedynczych wpisów, tylko konstrukcja modelu. Poprawienie kilku liczb nic nie da, trzeba zmienić poziom szczegółowości danych i sposób liczenia widełek.

Sprostowanie do wcześniejszej rekomendacji: Barometr zawodów opisuje popyt na zawody, nie wynagrodzenia. Używamy go dalej w karcie „Rynek pracy”, ale nie jako źródła płac.

## 2. Zasady

- Każda liczba ma poziom pewności: `zawód` (dane dla tego zawodu), `podgrupa` (4 cyfry ISCO), `grupa` (3 cyfry), `szeroka` (2 cyfry). Aplikacja pokazuje go użytkownikowi.
- Zakres to prawdziwe kwartyle (P25–P75) z danych, nie stałe −20/+25%. Gdy kwartyli brak, zakres jest oznaczony jako szacunek.
- Brak danych oznacza „brak danych”, nie przybliżenie z grupy nadrzędnej bez oznaczenia.
- Robimy małymi rundami, po każdej: walidator, build, test w przeglądarce, commit.

## 3. Rundy

**Runda 1: zejście z grup na podgrupy ISCO (4 cyfry).**
- Claude: znaleźć w GUS („Struktura wynagrodzeń według zawodów”, edycja 2024) tablice na poziomie 4 cyfr, wczytać mediany i kwartyle, zapisać do `pay_isco4.json` z rokiem i źródłem.
- Ograniczenie: shell w środowisku Claude może nie sięgać stat.gov.pl. Jeśli tak, Fabian wrzuca pobrany plik XLSX do czatu, resztę robi Claude.
- Efekt: z ok. 119 do kilkuset różnych median.

**Runda 2: dziury i zawody o małej próbie.**
- Claude: wypisać zawody, dla których 4-cyfrowy kod ma za małą próbę lub brak. Dla nich dodać zakresy z jawnych widełek w ogłoszeniach (od końca 2025 pracodawcy w Polsce mają podawać wynagrodzenie; Claude sprawdzi dokładne przepisy i dostępność danych przed użyciem) oraz z publicznych raportów płacowych.
- Zawody budżetowe (nauczyciele, policja, straż, wojsko, lekarze rezydenci itp.): płace z ustawowych siatek, nie z szacunku. Istniejąca lista `nocity` zostaje.

**Runda 3: nowy model danych.**
- Claude: `pay.json` w formacie `{klucz: {med, p25, p75, src, rok, poziom, n}}` i plik `pay_override.json` na ręczne poprawki per zawód (Fabian lub Claude).
- `build_pwa.py` czyta oba pliki; override wygrywa. Usunąć stałe −20/+25%.

**Runda 4: korekta miasta z danych.**
- Claude: sprawdzić, czy „połowa różnicy między miastem a średnią krajową” ma uzasadnienie w danych (np. GUS wg województw i sekcji). Jeśli tak, zostawić i opisać; jeśli nie, zastąpić współczynnikami wg zawodu/branży tam, gdzie dane są.
- Test: dla 20 zawodów porównać wynik dla Warszawy z ogłoszeniami z Warszawy.

**Runda 5: interfejs.**
- Claude: przy zarobkach pokazać poziom pewności („dla tego zawodu” / „dla grupy zawodów”), rok i źródło, brutto/netto, zakres P25–P75. Filtr zarobków pomija lub oznacza zawody z niską pewnością. Zaktualizować opis w „O aplikacji” i w README.

**Runda 6: walidator `validate_pay.py`.**
- Claude: reguły: min < max, rok i źródło obecne, korekta miasta zgodna z tabelą, brak zawodów z identycznymi widełkami bez wyjaśnienia (próg do ustalenia), płaca nie niższa niż minimalna.
- Metryki sukcesu: liczba różnych median z 119 do ponad 1000; największa grupa z jednakową medianą poniżej 10 zawodów; 100% wpisów ze źródłem i poziomem pewności.

**Runda 7: spot-check z ludźmi (Fabian).**
- Claude przygotowuje arkusz 40 zawodów (po kilka z każdej branży) z liczbami i źródłami. Fabian lub osoby z branż oceniają, czy wynik jest wiarygodny; rozbieżności trafiają do `pay_override.json`.

## 4. Co robi kto

| Kto | Co |
|---|---|
| Claude | rundy 1–6 w całości (runda 1 może wymagać wgrania pliku GUS) |
| Fabian | decyzja o progu pewności w filtrze, runda 7, ewentualne wgranie plików, które shell Claude nie pobierze |

## 5. Roczna aktualizacja

Co roku: podmienić pliki źródłowe (`pay_isco4.json`, siatki budżetowe), uruchomić walidator i build. Rok danych jest w każdym wpisie, więc przeterminowane widać od razu.
