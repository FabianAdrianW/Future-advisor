# Zadanie
Dla każdego zawodu z pliku wejściowego wypisz KONKRETNE umiejętności zawodowe dla polskich nastolatków (15–18 lat), którzy chcą wiedzieć, czego naprawdę trzeba się nauczyć.

## Wejście
Plik JSON: lista obiektów {id, name, desc, path, tasks}.
- name: nazwa zawodu; desc: opis; path: obszar > grupa; tasks: typowe czynności (mogą być puste).

## Wyjście
Plik tekstowy UTF-8. Dla KAŻDEGO id dokładnie taki blok (3 linie, potem pusta linia):

@<id>
M: <nazwa> :: <zdanie> | <nazwa> :: <zdanie> | <nazwa> :: <zdanie> | <nazwa> :: <zdanie>
W: <nazwa> :: <zdanie> | <nazwa> :: <zdanie> | <nazwa> :: <zdanie>

- M = „Musisz umieć”: 4 albo 5 umiejętności, bez których nie da się wykonywać tej pracy.
- W = „Warto umieć”: 3 albo 4 umiejętności, które dają przewagę lub otwierają specjalizację.

## Zasady treści
- Umiejętność to coś, czego można się NAUCZYĆ i co da się sprawdzić: technika, narzędzie, metoda, dział wiedzy, uprawnienie. NIE cecha charakteru. Zakazane: „komunikatywność”, „praca w zespole”, „odporność na stres”, „dokładność”, „kreatywność”, „cierpliwość”, „empatia”, „organizacja pracy” i podobne ogólniki.
- Mają być charakterystyczne dla TEGO zawodu, na poziomie szczegółu jak: Inżynier AI → „RAG”, „Ewaluacja modeli”; Spawacz → „Spawanie metodą TIG”; Księgowy → „Rozliczanie VAT”; Pielęgniarka → „Zakładanie wkłuć dożylnych”.
- Nazwa: 1–4 słowa, z wielkiej litery, bez kropki. Skróty branżowe są OK, jeśli zdanie je tłumaczy.
- Zdanie: jedno, 8–18 słów, po ludzku, mówi co to jest lub do czego służy w tej pracy. Laik ma zrozumieć. 2. osoba liczby pojedynczej w czasie teraźniejszym lub forma bezosobowa; bez form zdradzających płeć. Kończy się kropką.
- Wolno podać nazwę technologii, języka programowania, normy lub narzędzia, gdy jest to powszechny standard w zawodzie (np. Python, SQL, Git, CAD, prawo jazdy kat. C). Bez nazw firm, uczelni i marek produktów konsumenckich.
- Uczciwie i ostrożnie: tylko to, co jest powszechnie uznane w zawodzie w Polsce. Nie zmyślaj uprawnień, numerów norm ani przepisów. Gdy nie masz pewności co do szczegółu, wybierz ogólniejszą, ale wciąż zawodową umiejętność.
- Bez zarobków i statystyk. Umiejętności w M i W nie powtarzają się.
- Zawody podobne do siebie mają się różnić: pokaż, co wyróżnia każdy z nich.
- W treści nie używaj znaków „|”, „@” ani „::” poza separatorami. Nie łam linii w środku pola. Bez cudzysłowów wokół pól, bez numeracji, bez Markdown.

## Przykład

@7
M: Podstawy modeli językowych :: Wiesz, jak działają duże modele językowe, co potrafią i gdzie się mylą. | Python :: Piszesz w nim kod, który łączy model z danymi i resztą aplikacji. | RAG :: Podłączasz model do firmowych dokumentów, żeby odpowiadał na ich podstawie, a nie zgadywał. | Ewaluacja modeli :: Budujesz zestawy testów i mierzysz, czy odpowiedzi są trafne po każdej zmianie. | Praca z API :: Wysyłasz zapytania do modeli przez interfejs programistyczny i obsługujesz błędy oraz limity.
W: Fine-tuning :: Dotrenowujesz gotowy model na własnych przykładach, gdy same instrukcje nie wystarczają. | Bazy wektorowe :: Przechowujesz teksty jako liczby, żeby szybko wyszukiwać fragmenty podobne znaczeniem. | Agenci AI :: Projektujesz systemy, w których model sam planuje kroki i używa narzędzi. | Optymalizacja kosztów :: Dobierasz model i długość zapytań tak, żeby rachunek za użycie nie rósł bez potrzeby.

## Jak pracować
1. Przeczytaj plik wejściowy narzędziem Read.
2. Napisz bloki dla wszystkich id, w kolejności z pliku. Nie pomijaj żadnego.
3. Zapisz wynik narzędziem Write do DWÓCH plików: pierwsze 30 id do wskazanego pliku wyjściowego, pozostałe do tego samego z końcówką `_b.txt` zamiast `.txt`.
4. Sprawdź poleceniem `grep -c '^@'`, że łączna liczba bloków równa się liczbie obiektów w pliku wejściowym. Jeśli nie, dopisz brakujące.
5. Odpowiedz jednym zdaniem: ile bloków zapisano.

Nie rób nic poza tym zadaniem i nie twórz innych plików.
