# Stan weryfikacji zawodów (automatyzacja)

Cel: sprawdzić wszystkie zawody (2370) pod kątem nazwy, opisu, umiejętności, tras, grupy wynagrodzeń i mediany GUS, poprawić błędy i zrobić audyt końcowy.

Gałąź robocza: `verify-all` (NIE pushować na `main`; wynik to PR do przeglądu).

## Status (2026-10-19)
- Automatyzacja łańcuchowa WSTRZYMANA (zadanie wyłączone) z powodu limitu tygodniowego (87% zużyte, reset środa 17:00).
- Wznowienie: po resecie limitu, zgodnie z AUTOMATYZACJA.md.

## Liczniki
- zweryfikowane (done.txt): 700 (próbka 100 + 600 z partii 01–30)
- partie z automatyzacji: 0 (następna: 101)
- do zrobienia: 1670

## Faza A — zaległe poprawki z 600 (results/result_01..30.md)
Status: NIE ZROBIONE (poza: grupy dentystów i 8 tras, commit c814064 na main).
Do zrobienia: pozycje POPRAW z results/*.md, które nie są jeszcze w fixes_applied.md.

## Faza B — partie
Kolejne: `python3 verify/make_batches.py 4` (tworzy 4 partie po 20 w verify/batches/).

## Faza C — audyt
Po zakończeniu: walidatory, skan tekstów kart pod kątem niebezpiecznych zadań, ponowna weryfikacja losowych 100 zawodów przez nowych agentów, raport końcowy.
