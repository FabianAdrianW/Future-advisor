# Zadanie
Dla każdego zawodu z pliku wejściowego napisz krótką, konkretną kartę dla polskich nastolatków (15–18 lat), którzy nie wiedzą, jak wygląda ta praca.

## Wejście
Plik JSON: lista obiektów {id, name, desc, alt, path, fam}.
- name: nazwa zawodu; desc: opis z klasyfikacji zawodów (może być pusty); alt: inne nazwy;
- path: gdzie zawód leży w drzewie (obszar > grupa);
- fam: true oznacza rodzinę podobnych zawodów, wtedy pisz o typowym przedstawicielu.

## Wyjście
Plik tekstowy UTF-8. Dla KAŻDEGO id dokładnie taki blok (5 linii, potem pusta linia):

@<id>
H: <1–2 zdania w 2. osobie: na czym polega ta praca>
T: <czynność 1> | <czynność 2> | <czynność 3> | <czynność 4>
D: <godz> <co się dzieje> | <godz> <co się dzieje> | <godz> <co się dzieje> | <godz> <co się dzieje>
Y: <jedno zadanie „spróbuj dziś”>

## Zasady treści
- Po polsku, prosto, konkretnie, uczciwie. Bez zachwalania i bez ogólników typu „rozwijasz się”, „pracujesz w zespole”, „dbasz o jakość”.
- H i T w 2. osobie liczby pojedynczej, w czasie teraźniejszym („Naprawiasz…”, „Sprawdzasz…”). Unikaj form zdradzających płeć (bez czasu przeszłego, bez „sam/sama”).
- T: dokładnie 4 czynności, każda 3–9 słów, charakterystyczne dla TEGO zawodu. Opieraj się na desc.
- D: dokładnie 4 momenty realistycznego dnia, po kolei. Godzina w formacie G:MM (np. 7:00, 13:30). Każdy opis 4–11 słów i pokazuje konkretną scenę: co robisz, z kim lub z czym. Uwzględnij prawdziwe godziny pracy w tym zawodzie (zmiany, noce, wczesne poranki, wieczory).
- Y: jedno zadanie na dziś, ok. 15 minut, bez wydawania pieniędzy, bezpieczne i wykonalne dla ucznia w domu lub okolicy, wyraźnie związane z zawodem; 8–20 słów. Żadnych zadań z prądem, ogniem, chemikaliami, wysokością, ruchem drogowym ani cudzymi danymi.
- Nie podawaj zarobków, statystyk, nazw firm, uczelni, marek ani programów komputerowych z nazwy.
- Gdy desc jest pusty lub niejasny, pisz ostrożniej i ogólniej, ale nadal o tym zawodzie. Nie zmyślaj szczegółów technicznych.
- Zawody podobne do siebie w jednym pliku mają się różnić treścią: pokaż, co wyróżnia każdy z nich.
- W treści nie używaj znaków „|” ani „@”, nie łam linii w środku pola. Bez cudzysłowów wokół pól, bez numeracji, bez Markdown.

## Przykłady

@12
H: Znajdujesz, co się zepsuło w samochodzie, i to naprawiasz. Łączysz pracę rąk z diagnostyką komputerową.
T: Podłączasz komputer i czytasz kody usterek | Wymieniasz zużyte części | Robisz przeglądy i wymiany oleju | Tłumaczysz klientowi, co było nie tak
D: 8:00 Auto nie odpala, zaczynasz od akumulatora | 10:00 Wymiana klocków i tarcz hamulcowych | 13:00 Dziwny stuk w zawieszeniu, jazda próbna | 16:00 Oddajesz samochód i pokazujesz starą część
Y: Znajdź w instrukcji rodzinnego samochodu, jakie ciśnienie powinny mieć opony, i zapisz je.

@13
H: Jesteś najbliżej pacjenta: podajesz leki, robisz zabiegi i jako pierwsza osoba zauważasz, że coś jest nie tak.
T: Podajesz leki i zakładasz kroplówki | Mierzysz ciśnienie i pobierasz krew | Zmieniasz opatrunki | Rozmawiasz z pacjentami i ich rodzinami
D: 7:00 Przejęcie zmiany, co działo się w nocy | 8:00 Poranne leki i pomiary na całym oddziale | 11:00 Przygotowanie pacjenta do zabiegu | 15:00 Pacjent słabnie, wzywasz lekarza
Y: Naucz się mierzyć tętno na nadgarstku i zmierz je trzem osobom w domu.

## Jak pracować
1. Przeczytaj plik wejściowy narzędziem Read.
2. Napisz bloki dla wszystkich id, w kolejności z pliku. Nie pomijaj żadnego.
3. Zapisz wynik narzędziem Write do wskazanego pliku wyjściowego. Jeśli wynik jest długi, podziel go na dwa pliki: wskazany plik oraz ten sam z końcówką `_b.txt` zamiast `.txt` (druga połowa id).
4. Sprawdź poleceniem `grep -c '^@'`, że łączna liczba bloków równa się liczbie obiektów w pliku wejściowym. Jeśli nie, dopisz brakujące.
5. Odpowiedz jednym zdaniem: ile bloków zapisano.

Nie rób nic poza tym zadaniem i nie twórz innych plików.
