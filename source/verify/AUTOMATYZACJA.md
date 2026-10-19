# Instrukcje dla automatyzacji (uruchamiana co kilka godzin)

Pracujesz w repozytorium `FabianAdrianW/Future-advisor` na gałęzi `verify-all`. Najpierw:
```
git fetch origin && git checkout verify-all 2>/dev/null || git checkout -b verify-all origin/main
git pull --ff-only origin verify-all 2>/dev/null; cat source/verify/STATE.md
```

## Zasady (nienegocjowalne)
- Nie pushuj na `main`. Tylko `verify-all`. Nie merguj PR.
- Nie zmieniaj `appId`, adresu kontaktowego, kont sklepów, polityki prywatności ani landingu.
- Nie wysyłaj wiadomości do nikogo i nie kontaktuj użytkowników ani firm.
- Nie wymyślaj źródeł. Gdy nie da się potwierdzić, zostaw werdykt NIE WIEM i opisz to w pliku.
- Każda zmiana danych przechodzi przez `source/decorate.py` (PAY_FIX, ROUTE_FIX, DISPLAY_FIX), `groups.txt` albo `gen/out/*.txt`, nigdy przez ręczną edycję `app.json`.
- Przed każdym commitem: `python3 source/validate_pay.py`, `cd source/gen && python3 validate.py` (oczekiwane 2349/2349), `python3 source/skills/validate.py` (2370/2370).

## Jedna sesja (uruchomienie)
1. Faza A: otwórz `source/verify/results/result_*.md`. Dla każdej pozycji POPRAW, której nie ma w `source/verify/fixes_applied.md`, wprowadź poprawkę przez właściwy mechanizm. Dopisz zrobione pozycje do `fixes_applied.md` z jednym zdaniem o tym, co zmieniono. Nie wprowadzaj zmian bez źródła; jeśli poprawka wymaga źródła, której nie znasz, zostaw ją w `source/verify/open_questions.md`.
2. Faza B: uruchom `python3 source/verify/make_batches.py 4`. Dla każdej nowej partii `source/verify/batches/NNN.json` uruchom jednego agenta (general-purpose), który:
   - czyta partię i sprawdza każdy zawód: nazwę, opis (hook/tasks/day), umiejętności, trasy edukacji (długości zgodne z prawem: liceum 4, technikum 5, branżowa I st. 3, policealna 1–2.5, licencjat 3, inżynierskie 3.5, magisterskie po licencjacie 2, jednolite magisterskie 5 (medycyna 6, weterynaria 5.5), aplikacja radcowska/adwokacka ~3.5), grupę wynagrodzeń (musi istnieć w GUS KZiS i pasować do zawodu) oraz medianę,
   - werdykt dla każdego zawodu: OK, POPRAW (dokładna zmiana), NIE WIEM (czego nie da się sprawdzić),
   - zapisuje tabelę do `source/verify/results/NNN.md` (nazwa | werdykt | uzasadnienie | źródło) i zwraca krótkie podsumowanie.
   Agenci nie zmieniają plików repozytorium. Limit wyszukiwań: 8 na agenta.
3. Po zakończeniu agentów: zastosuj poprawki POPRAW z nowych partii tak jak w fazie A, przebuduj (`python3 source/build_pwa.py`), uruchom walidatory, dopisz nazwy z partii do `source/verify/done.txt` (wszystkie 20 nazw partii, także NIE WIEM), dopisz wpisy do `STATE.md` (liczniki) i zrób commit + push na `verify-all`.
4. Commit: wiadomość po polsku, np. "Weryfikacja: partie 101–104, poprawki X", na końcu linie:
   Co-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>
   Claude-Session: https://claude.ai/code/session_01NCXnVTqT37LnVQpD8hENgW

## Faza C — audyt (gdy `make_batches.py 1` nie tworzy nowej partii)
1. Walidatory (jak wyżej) muszą przejść.
2. Skan `source/gen/out/*.txt` pod kątem słów: prąd, napięcie, ogień, wysokość, chemikalia, ruch drogowy, broń, leki. Zanotuj trafienia i ręcznie oceń.
3. Losowe 100 zawodów (seed 20261019) sprawdź nowymi agentami w partiach po 20, wynik do `source/verify/results/audyt_NN.md`.
4. Napisz `source/verify/AUDYT.md`: liczby OK/POPRAW/NIE WIEM dla całego zbioru, co naprawiono, co zostaje do decyzji człowieka. Próg akceptacji: zero błędów krytycznych (trasy prawne, wiek, zdrowie, grupy wynagrodzeń nieistniejące w GUS), poniżej 5% pozostałych błędów.
5. Otwórz PR z `verify-all` do `main` z opisem z `AUDYT.md`. Nie merguj.
