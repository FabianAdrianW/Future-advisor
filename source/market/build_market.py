# Składa source/market-2026.json z danych źródłowych. Co rok: podmień dane Barometru
# (BAR, MAP), plik ILO (jeśli wyjdzie nowy) i YEAR, uruchom, sprawdź wynik.
# Zasada: w pliku jest tylko to, co da się podeprzeć źródłem. Gdzie źródło milczy, piszemy to wprost.
import json, csv, pathlib, collections
B = pathlib.Path(__file__).resolve().parent
YEAR = 2026
POW = 380

SOURCES = {
    'barometr': {'n': 'Barometr zawodów 2026', 'o': 'WUP w Krakowie na zlecenie MRPiPS', 'd': 'prognoza na 2026 r., panele ekspertów VIII–X 2025',
                 'u': 'https://barometrzawodow.pl/forecast-card-zip/2026/report_pl/raport_ogolnopolski_2026.pdf'},
    'ilo': {'n': 'Indeks ekspozycji zawodów na generatywną AI', 'o': 'ILO i NASK (Gmyrek i in., ILO Working Paper 140)', 'd': '2025',
            'u': 'https://www.ilo.org/publications/generative-ai-and-jobs-refined-global-index-occupational-exposure'},
    'nask': {'n': 'Generatywna sztuczna inteligencja a polski rynek pracy', 'o': 'NASK-PIB i ILO', 'd': 'czerwiec 2025',
             'u': 'https://www.nask.pl/media/2025/06/Generatywna-sztuczna-inteligencja-a-polski-rynek-pracy.pdf'},
    'gus': {'n': 'Struktura wynagrodzeń według zawodów za październik 2024 r.', 'o': 'GUS', 'd': 'publikacja 14.10.2025',
            'u': 'https://stat.gov.pl/obszary-tematyczne/rynek-pracy/pracujacy-zatrudnieni-wynagrodzenia-koszty-pracy/struktura-wynagrodzen-wedlug-zawodow-za-pazdziernik-2024-r-,5,9.html'},
    'wef': {'n': 'Future of Jobs Report 2025', 'o': 'Światowe Forum Ekonomiczne', 'd': 'styczeń 2025, ankieta ponad 1000 pracodawców z 55 gospodarek',
            'u': 'https://www.weforum.org/publications/the-future-of-jobs-report-2025/digest/'},
}

# --- Barometr zawodów 2026, poziom kraju: 17 deficytów, 151 w równowadze, 0 nadwyżek ---
# D: [powiaty z deficytem 2026, 2025]
D = {
    'Kierowcy samochodów ciężarowych i ciągników siodłowych': [326, 331], 'Lekarze': [323, 315], 'Psycholodzy i terapeuci': [309, 334],
    'Pielęgniarki i położne': [287, 300], 'Spawacze': [274, 297], 'Pracownicy służb mundurowych': [260, 293], 'Elektrycy i energetycy': [258, 294],
    'Nauczyciele praktycznej nauki zawodu': [256, 246], 'Nauczyciele przedmiotów zawodowych': [252, 267],
    'Operatorzy i mechanicy sprzętu do robót ziemnych': [252, 263], 'Nauczyciele szkół specjalnych i oddziałów integracyjnych': [243, 251],
    'Kierowcy autobusów': [232, 271], 'Samodzielni księgowi': [226, 256], 'Opiekunowie osoby starszej lub z niepełnosprawnością': [202, 197],
    'Magazynierzy': [198, 213], 'Monterzy instalacji budowlanych': [196, 210], 'Nauczyciele przedmiotów ogólnokształcących i języków obcych': [196, 207],
}
# Deficyt w 2025, równowaga w 2026: [powiaty z równowagą 2026, 2025]
MOVED = {'Robotnicy budowlani': [238, 187], 'Murarze i tynkarze': [213, 183], 'Pracownicy ds. rachunkowości i księgowości': [209, 185],
         'Dekarze i blacharze budowlani': [194, 189], 'Mechanicy pojazdów samochodowych': [194, 169], 'Nauczyciele przedszkoli': [189, 163]}
# Równowaga w kraju, ale nadwyżka chętnych w co najmniej 20 powiatach: [2026, 2025]
SUR = {'Technicy ekonomiści': [88, 118], 'Technicy informatycy': [64, 51], 'Pracownicy administracyjni i biurowi': [48, 45],
       'Specjaliści ds. badań społeczno-ekonomicznych i analizy danych': [39, 23], 'Specjaliści nauk humanistycznych': [35, 38],
       'Pracownicy biur podróży i obsługi turystycznej': [30, 35], 'Technicy mechanicy': [29, 33], 'Technolodzy żywności i żywienia': [27, 33],
       'Fryzjerzy': [25, 28], 'Mechanicy pojazdów samochodowych': [20, 17], 'Spedytorzy i logistycy': [20, 15], 'Sprzedawcy i kasjerzy': [20, 23]}
BALANCE = """Administratorzy stron internetowych; Agenci ubezpieczeniowi; Analitycy, testerzy i operatorzy systemów komputerowych; Animatorzy kultury i organizatorzy imprez; Architekci i urbaniści; Architekci krajobrazu; Archiwiści i muzealnicy; Asystenci w edukacji; Betoniarze i zbrojarze; Bibliotekoznawcy, bibliotekarze i specjaliści informacji naukowej; Biolodzy i biotechnolodzy; Blacharze i lakiernicy samochodowi; Brukarze; Ceramicy; Chemicy; Cieśle i stolarze budowlani; Cukiernicy; Dekarze i blacharze budowlani; Dentyści; Diagności laboratoryjni medyczni; Diagności samochodowi; Dziennikarze i redaktorzy; Elektronicy, automatycy i robotycy; Farmaceuci; Filolodzy i tłumacze; Fizjoterapeuci i masażyści; Fizycy i matematycy; Floryści; Fotografowie; Fryzjerzy; Geodeci i kartografowie; Gospodarze obiektów, portierzy, woźni i dozorcy; Górnicy i operatorzy maszyn i urządzeń wydobywczych; Graficy komputerowi; Inspektorzy nadzoru budowlanego; Instruktorzy nauki jazdy; Instruktorzy rekreacji i sportu; Inżynierowie budownictwa; Inżynierowie elektrycy i energetycy; Inżynierowie inżynierii środowiska; Kadra kierownicza, menadżerowie; Kamieniarze; Kelnerzy i barmani; Kierowcy samochodów osobowych; Kierownicy budowy; Krawcy i pracownicy produkcji odzieży; Kucharze; Kurierzy i listonosze; Lakiernicy; Logopedzi i audiofonolodzy; Marynarze, pracownicy obsługi statków i portów; Maszyniści; Mechanicy pojazdów samochodowych; Mechanicy-monterzy maszyn, urządzeń i instrumentów; Meteorolodzy, geolodzy, geografowie; Monterzy elektronicy; Monterzy konstrukcji metalowych; Monterzy okien i szklarze; Murarze i tynkarze; Nauczyciele nauczania wczesnoszkolnego; Nauczyciele przedszkoli; Obuwnicy; Ogrodnicy i sadownicy; Operatorzy aparatury medycznej; Operatorzy maszyn do produkcji i przetwórstwa papieru; Operatorzy maszyn do produkcji wyrobów cementowych i kamiennych; Operatorzy maszyn do produkcji wyrobów chemicznych; Operatorzy maszyn do produkcji wyrobów z gumy i tworzyw sztucznych; Operatorzy maszyn rolniczych i ogrodniczych; Operatorzy maszyn włókienniczych; Operatorzy obrabiarek skrawających; Operatorzy urządzeń dźwigowo-transportowych; Opiekunki dziecięce; Opiekunowie wspomagający opiekę nad pacjentem; Optycy i pracownicy wytwarzający protezy; Pedagodzy i nauczyciele wspierający; Personel sprzątający; Personel związany z produkcją filmową, teatralną, telewizyjną i radiową; Piekarze; Plastycy, dekoratorzy wnętrz i konserwatorzy zabytków; Pomoce kuchenne; Pomoce w gospodarstwie domowym; Pozostali specjaliści edukacji; Pracownicy administracyjni i biurowi; Pracownicy biur podróży i obsługi turystycznej; Pracownicy ds. BHP i zarządzania kryzysowego; Pracownicy ds. budownictwa drogowego i kolejowego; Pracownicy ds. jakości i organizacji produkcji; Pracownicy ds. ochrony środowiska i zrównoważonego rozwoju; Pracownicy ds. rachunkowości i księgowości; Pracownicy ds. techniki dentystycznej; Pracownicy fizyczni w produkcji i pracach prostych; Pracownicy myjni, pralni i prasowalni; Pracownicy obróbki szkła, kamieni i metali szlachetnych; Pracownicy obsługi ruchu lotniczego; Pracownicy obsługi ruchu szynowego; Pracownicy ochrony fizycznej; Pracownicy poczty; Pracownicy poligraficzni; Pracownicy przetwórstwa metali; Pracownicy przetwórstwa spożywczego; Pracownicy robót wykończeniowych w budownictwie; Pracownicy socjalni i mediatorzy; Pracownicy sprzedaży internetowej; Pracownicy telefonicznej i elektronicznej obsługi klienta, ankieterzy, teleankieterzy; Pracownicy usług kosmetycznych; Pracownicy usług pogrzebowych; Pracownicy zajmujący się zwierzętami; Praktykujący niekonwencjonalne metody terapii; Prawnicy; Programiści; Projektanci wzornictwa przemysłowego i operatorzy CAD; Przedstawiciele handlowi; Przetwórcy mięsa i ryb; Ratownicy medyczni; Recepcjoniści i rejestratorzy; Robotnicy budowlani; Robotnicy leśni; Robotnicy obróbki drewna i stolarze; Robotnicy obróbki skóry; Rolnicy i hodowcy; Rybacy; Sekretarki i asystenci; Specjaliści ds. administracji; Specjaliści ds. badań społeczno-ekonomicznych i analizy danych; Specjaliści ds. baz danych i sieci komputerowych; Specjaliści ds. finansowych; Specjaliści ds. PR, reklamy, marketingu i sprzedaży; Specjaliści ds. rynku nieruchomości; Specjaliści ds. zarządzania i konsultanci biznesu; Specjaliści ds. zarządzania zasobami ludzkimi i rekrutacji; Specjaliści mechanicy; Specjaliści nauk humanistycznych; Specjaliści rolnictwa i leśnictwa; Specjaliści technologii produkcyjnych; Specjaliści telekomunikacji; Specjaliści zdrowia publicznego; Spedytorzy i logistycy; Sprzedawcy i kasjerzy; Szefowie kuchni; Ślusarze; Tapicerzy; Technicy budownictwa; Technicy ekonomiści; Technicy informatycy; Technicy mechanicy; Technolodzy żywności i żywienia; Weterynarze; Windykatorzy; Wychowawcy w placówkach oświatowych i opiekuńczych; Zaopatrzeniowcy i dostawcy"""
BAL = [x.strip() for x in BALANCE.replace('\n', ' ').split(';')]
assert len(BAL) == 151 and len(D) == 17, (len(BAL), len(D))
assert all(k in BAL for k in list(MOVED) + list(SUR))

# --- Nasze grupy -> zawody z Barometru. Pusta lista = Barometr nie ocenia tej grupy. ---
KADRA = 'Kadra kierownicza, menadżerowie'
MUND = 'Pracownicy służb mundurowych'
FILM = 'Personel związany z produkcją filmową, teatralną, telewizyjną i radiową'
PLAST = 'Plastycy, dekoratorzy wnętrz i konserwatorzy zabytków'
BIURO = 'Pracownicy administracyjni i biurowi'
JAK = 'Pracownicy ds. jakości i organizacji produkcji'
FIZ = 'Pracownicy fizyczni w produkcji i pracach prostych'
MAP = {
    '011': [MUND], '021': [MUND], '031': [MUND], '111': [], '112': [KADRA], '121': [KADRA], '122': [KADRA], '131': [KADRA], '132': [KADRA],
    '133': [KADRA], '134': [KADRA], '141': [KADRA], '142': [KADRA], '143': [KADRA],
    '211': ['Chemicy', 'Meteorolodzy, geolodzy, geografowie', 'Fizycy i matematycy'], '212': ['Fizycy i matematycy'],
    '213': ['Biolodzy i biotechnolodzy', 'Pracownicy ds. ochrony środowiska i zrównoważonego rozwoju', 'Specjaliści rolnictwa i leśnictwa'],
    '214': ['Specjaliści technologii produkcyjnych', 'Specjaliści mechanicy', 'Inżynierowie budownictwa', 'Inżynierowie inżynierii środowiska'],
    '215': ['Inżynierowie elektrycy i energetycy', 'Elektronicy, automatycy i robotycy', 'Specjaliści telekomunikacji'],
    '216': ['Architekci i urbaniści', 'Projektanci wzornictwa przemysłowego i operatorzy CAD'], '2161': ['Architekci i urbaniści'],
    '2162': ['Architekci krajobrazu'], '2164': ['Architekci i urbaniści'], '2165': ['Geodeci i kartografowie'], '2166': ['Graficy komputerowi'],
    '221': ['Lekarze'], '222': ['Pielęgniarki i położne'], '223': ['Praktykujący niekonwencjonalne metody terapii'], '225': ['Weterynarze'],
    '226': ['Dentyści', 'Farmaceuci', 'Fizjoterapeuci i masażyści', 'Logopedzi i audiofonolodzy'],
    '231': [], '232': ['Nauczyciele przedmiotów zawodowych', 'Nauczyciele praktycznej nauki zawodu'],
    '233': ['Nauczyciele przedmiotów ogólnokształcących i języków obcych'],
    '234': ['Nauczyciele przedmiotów ogólnokształcących i języków obcych', 'Nauczyciele nauczania wczesnoszkolnego', 'Nauczyciele przedszkoli'],
    '235': ['Nauczyciele szkół specjalnych i oddziałów integracyjnych', 'Pedagodzy i nauczyciele wspierający', 'Pozostali specjaliści edukacji'],
    '241': ['Samodzielni księgowi', 'Specjaliści ds. finansowych'],
    '242': ['Specjaliści ds. zarządzania zasobami ludzkimi i rekrutacji', 'Specjaliści ds. zarządzania i konsultanci biznesu', 'Specjaliści ds. administracji'],
    '243': ['Specjaliści ds. PR, reklamy, marketingu i sprzedaży'],
    '251': ['Programiści', 'Analitycy, testerzy i operatorzy systemów komputerowych'], '2513': ['Administratorzy stron internetowych', 'Graficy komputerowi'],
    '252': ['Specjaliści ds. baz danych i sieci komputerowych'], '261': ['Prawnicy'],
    '262': ['Archiwiści i muzealnicy', 'Bibliotekoznawcy, bibliotekarze i specjaliści informacji naukowej'],
    '263': ['Specjaliści nauk humanistycznych', 'Specjaliści ds. badań społeczno-ekonomicznych i analizy danych'],
    '2631': ['Specjaliści ds. badań społeczno-ekonomicznych i analizy danych'], '2634': ['Psycholodzy i terapeuci'],
    '2635': ['Pracownicy socjalni i mediatorzy'], '2636': [], '264': ['Dziennikarze i redaktorzy', 'Filolodzy i tłumacze'],
    '265': [PLAST, FILM], '2656': [FILM],
    '311': ['Technicy mechanicy', 'Elektronicy, automatycy i robotycy', 'Projektanci wzornictwa przemysłowego i operatorzy CAD', JAK],
    '3111': [], '3112': ['Technicy budownictwa', 'Inspektorzy nadzoru budowlanego', 'Geodeci i kartografowie'], '312': [JAK],
    '313': ['Elektrycy i energetycy', 'Operatorzy maszyn do produkcji wyrobów chemicznych'], '314': ['Specjaliści rolnictwa i leśnictwa'],
    '315': ['Pracownicy obsługi ruchu lotniczego', 'Marynarze, pracownicy obsługi statków i portów'],
    '321': ['Operatorzy aparatury medycznej', 'Diagności laboratoryjni medyczni', 'Pracownicy ds. techniki dentystycznej', 'Optycy i pracownicy wytwarzający protezy'],
    '322': ['Opiekunowie wspomagający opiekę nad pacjentem'], '323': ['Praktykujący niekonwencjonalne metody terapii'], '324': [],
    '325': ['Ratownicy medyczni', 'Fizjoterapeuci i masażyści', 'Optycy i pracownicy wytwarzający protezy', 'Opiekunowie wspomagający opiekę nad pacjentem'],
    '3257': ['Pracownicy ds. BHP i zarządzania kryzysowego', 'Pracownicy ds. ochrony środowiska i zrównoważonego rozwoju'],
    '331': ['Technicy ekonomiści', 'Pracownicy ds. rachunkowości i księgowości', 'Specjaliści ds. finansowych'],
    '332': ['Agenci ubezpieczeniowi', 'Przedstawiciele handlowi', 'Zaopatrzeniowcy i dostawcy'],
    '333': ['Specjaliści ds. rynku nieruchomości', 'Animatorzy kultury i organizatorzy imprez'], '3331': ['Spedytorzy i logistycy'],
    '3332': ['Animatorzy kultury i organizatorzy imprez'], '334': ['Sekretarki i asystenci', BIURO], '335': [], '3355': [MUND],
    '341': ['Pracownicy socjalni i mediatorzy', 'Wychowawcy w placówkach oświatowych i opiekuńczych'], '3411': [], '3413': [],
    '342': ['Instruktorzy rekreacji i sportu'], '343': [FILM, PLAST], '3431': ['Fotografowie'], '3432': [PLAST], '3434': ['Szefowie kuchni'],
    '351': ['Technicy informatycy'], '352': [FILM, 'Specjaliści telekomunikacji'],
    '411': [BIURO], '412': ['Sekretarki i asystenci', BIURO], '413': [BIURO], '421': ['Windykatorzy'],
    '422': ['Recepcjoniści i rejestratorzy', 'Pracownicy telefonicznej i elektronicznej obsługi klienta, ankieterzy, teleankieterzy'],
    '4221': ['Pracownicy biur podróży i obsługi turystycznej'], '4224': ['Recepcjoniści i rejestratorzy'],
    '431': ['Pracownicy ds. rachunkowości i księgowości'], '432': ['Magazynierzy'], '441': [BIURO, 'Pracownicy poczty'],
    '511': ['Pracownicy obsługi ruchu szynowego'], '5113': ['Pracownicy biur podróży i obsługi turystycznej'], '512': ['Kucharze'],
    '513': ['Kelnerzy i barmani'], '514': ['Fryzjerzy', 'Pracownicy usług kosmetycznych'], '515': ['Gospodarze obiektów, portierzy, woźni i dozorcy'],
    '516': ['Pracownicy usług pogrzebowych'], '5164': ['Pracownicy zajmujący się zwierzętami'], '5165': ['Instruktorzy nauki jazdy'],
    '521': [], '522': ['Sprzedawcy i kasjerzy'], '523': ['Sprzedawcy i kasjerzy'],
    '524': ['Pracownicy sprzedaży internetowej', 'Pracownicy telefonicznej i elektronicznej obsługi klienta, ankieterzy, teleankieterzy'],
    '5241': [], '5246': [], '531': ['Opiekunki dziecięce'], '5312': ['Asystenci w edukacji'],
    '532': ['Opiekunowie osoby starszej lub z niepełnosprawnością', 'Opiekunowie wspomagający opiekę nad pacjentem'],
    '541': [MUND, 'Pracownicy ochrony fizycznej'], '611': ['Ogrodnicy i sadownicy', 'Rolnicy i hodowcy'], '612': ['Rolnicy i hodowcy'],
    '613': ['Rolnicy i hodowcy'], '621': ['Robotnicy leśni'], '622': ['Rybacy'],
    '711': ['Murarze i tynkarze', 'Robotnicy budowlani', 'Betoniarze i zbrojarze', 'Cieśle i stolarze budowlani', 'Kamieniarze', 'Brukarze'],
    '712': ['Monterzy instalacji budowlanych', 'Dekarze i blacharze budowlani', 'Pracownicy robót wykończeniowych w budownictwie', 'Monterzy okien i szklarze'],
    '713': ['Lakiernicy', 'Blacharze i lakiernicy samochodowi', 'Pracownicy robót wykończeniowych w budownictwie'],
    '721': ['Spawacze', 'Monterzy konstrukcji metalowych', 'Blacharze i lakiernicy samochodowi'],
    '722': ['Ślusarze', 'Operatorzy obrabiarek skrawających', 'Pracownicy przetwórstwa metali'],
    '723': ['Mechanicy pojazdów samochodowych', 'Mechanicy-monterzy maszyn, urządzeń i instrumentów', 'Diagności samochodowi'],
    '731': ['Pracownicy obróbki szkła, kamieni i metali szlachetnych', 'Ceramicy'], '732': ['Pracownicy poligraficzni'],
    '741': ['Elektrycy i energetycy'], '742': ['Monterzy elektronicy', 'Specjaliści telekomunikacji'],
    '751': ['Przetwórcy mięsa i ryb', 'Pracownicy przetwórstwa spożywczego'], '7512': ['Piekarze', 'Cukiernicy'],
    '752': ['Robotnicy obróbki drewna i stolarze'], '753': ['Krawcy i pracownicy produkcji odzieży', 'Obuwnicy', 'Tapicerzy', 'Robotnicy obróbki skóry'],
    '754': [JAK], '811': ['Górnicy i operatorzy maszyn i urządzeń wydobywczych', 'Operatorzy maszyn do produkcji wyrobów cementowych i kamiennych'],
    '812': ['Pracownicy przetwórstwa metali'], '813': ['Operatorzy maszyn do produkcji wyrobów chemicznych'],
    '814': ['Operatorzy maszyn do produkcji wyrobów z gumy i tworzyw sztucznych', 'Operatorzy maszyn do produkcji i przetwórstwa papieru'],
    '815': ['Operatorzy maszyn włókienniczych', 'Robotnicy obróbki skóry'], '816': ['Pracownicy przetwórstwa spożywczego'],
    '817': ['Robotnicy obróbki drewna i stolarze', 'Operatorzy maszyn do produkcji i przetwórstwa papieru'], '818': [FIZ],
    '821': ['Mechanicy-monterzy maszyn, urządzeń i instrumentów', 'Monterzy elektronicy'], '831': ['Maszyniści', 'Pracownicy obsługi ruchu szynowego'],
    '832': ['Kierowcy samochodów osobowych', 'Kurierzy i listonosze'], '833': ['Kierowcy samochodów ciężarowych i ciągników siodłowych', 'Kierowcy autobusów'],
    '834': ['Operatorzy i mechanicy sprzętu do robót ziemnych', 'Operatorzy urządzeń dźwigowo-transportowych'],
    '8341': ['Operatorzy maszyn rolniczych i ogrodniczych'], '835': ['Marynarze, pracownicy obsługi statków i portów'],
    '911': ['Personel sprzątający', 'Pomoce w gospodarstwie domowym'], '912': ['Pracownicy myjni, pralni i prasowalni'], '921': [],
    '931': ['Robotnicy budowlani', 'Pracownicy ds. budownictwa drogowego i kolejowego'], '932': [FIZ], '933': [FIZ], '941': ['Pomoce kuchenne'],
    '951': [], '952': [], '961': [], '962': ['Kurierzy i listonosze'],
    'X-doula': [], 'X-dron': [], 'X-esport': [], 'X-florysta': ['Floryści'], 'X-startup': [], 'X-tworca': [],
}

# Dodatkowe „dlaczego” – tylko to, co raport Barometru mówi wprost.
WHY_OCC = {
    'Lekarze': 'Barometr wiąże rosnący niedobór lekarzy ze starzeniem się społeczeństwa i przechodzeniem praktyk do sektora prywatnego.',
    'Opiekunowie osoby starszej lub z niepełnosprawnością': 'Barometr wiąże rosnące braki w zawodach medyczno-opiekuńczych ze starzeniem się społeczeństwa.',
    'Pielęgniarki i położne': 'Barometr wiąże braki w zawodach medyczno-opiekuńczych ze starzeniem się społeczeństwa.',
    'Psycholodzy i terapeuci': 'To trzeci największy deficyt w kraju, choć mniejszy niż rok wcześniej.',
    'Nauczyciele praktycznej nauki zawodu': 'Według Barometru brakuje doświadczonych praktyków, którzy chcą uczyć w szkole.',
    'Kierowcy samochodów ciężarowych i ciągników siodłowych': 'To największy deficyt w kraju według liczby powiatów.',
    'Kierowcy autobusów': 'Deficyt kierowców autobusów zmalał najmocniej ze wszystkich zawodów (o 39 powiatów).',
    'Elektrycy i energetycy': 'Deficyt nadal jest duży, ale zmalał o 36 powiatów.',
    'Pracownicy służb mundurowych': 'Deficyt nadal jest duży, ale zmalał o 33 powiaty.',
    'Robotnicy budowlani': 'Barometr tłumaczy mniejsze braki w budownictwie spadkiem produkcji budowlano-montażowej.',
    'Murarze i tynkarze': 'Barometr tłumaczy mniejsze braki w budownictwie spadkiem produkcji budowlano-montażowej.',
    'Dekarze i blacharze budowlani': 'Barometr tłumaczy mniejsze braki w budownictwie spadkiem produkcji budowlano-montażowej.',
    'Monterzy instalacji budowlanych': 'To jeden z zawodów budowlanych, w których deficyt utrzymuje się od lat.',
    'Operatorzy i mechanicy sprzętu do robót ziemnych': 'To jeden z zawodów budowlanych, w których deficyt utrzymuje się od lat.',
    'Technicy informatycy': 'Liczba powiatów z nadwyżką techników informatyków wzrosła w ciągu roku z 51 do 64.',
    'Technicy ekonomiści': 'To zawód z największą lokalną nadwyżką chętnych, choć mniejszą niż rok wcześniej.',
}
GEN_DEF = 'Najczęstsze powody deficytów według Barometru to brak kandydatów (47%), niespełnianie wymagań (32%) i niechęć do pracy w zawodzie (18%).'
GEN_SUR = 'Barometr łączy nadwyżki kandydatów w części zawodów z tym, że proste czynności łatwo zastąpić AI.'

# --- ILO–NASK 2025: ekspozycja na generatywną AI, ISCO-08 4-cyfrowe ---
ILO = {}
for r in csv.DictReader(open(B / 'ilo-genai-2025.csv', encoding='utf-8')):
    ILO[r['isco08']] = (float(r['mean_score_2025']), r['category'])

def ai_of(gk):
    rows = [v for c, v in ILO.items() if c.startswith(gk)] if gk.isdigit() else []
    if not rows:
        return {'lvl': None, 't': 'Indeks ILO–NASK nie obejmuje tej grupy, więc nie oceniamy wpływu AI.'}
    n = len(rows); hi = sum(1 for _, c in rows if c in ('Exposed: Gradient 3', 'Exposed: Gradient 4'))
    ex = sum(1 for _, c in rows if c.startswith('Exposed')); mi = sum(1 for _, c in rows if c == 'Minimal Exposure')
    mean = round(sum(m for m, _ in rows) / n, 2)
    lvl = 3 if hi * 2 >= n else 2 if ex * 2 >= n else 1 if (ex + mi) * 2 >= n else 0
    of = 'jedynej podgrupy' if n == 1 else f'{n} podgrup'
    if lvl == 3: t = f'Duży. W indeksie ILO–NASK {hi} z {of} tej grupy zawodów jest w dwóch najwyższych stopniach ekspozycji: AI może wspierać lub przejąć dużą część zadań.'
    elif lvl == 2: t = f'Średni. W indeksie ILO–NASK {ex} z {of} tej grupy zawodów ma podwyższoną ekspozycję: AI może wspierać część zadań.'
    elif lvl == 1: t = f'Niewielki. W indeksie ILO–NASK większość z {of} tej grupy zawodów ma ekspozycję minimalną lub podwyższoną tylko w części zadań.'
    else: t = f'Znikomy. W indeksie ILO–NASK większość z {of} tej grupy zawodów nie jest eksponowana na generatywną AI.'
    if n == 1: t = t.replace('większość z jedynej podgrupy tej grupy zawodów', 'ta grupa zawodów').replace('1 z jedynej podgrupy tej grupy zawodów', 'ta grupa zawodów').replace('W indeksie ILO–NASK ta grupa zawodów jest w dwóch najwyższych stopniach', 'W indeksie ILO–NASK ta grupa zawodów jest w jednym z dwóch najwyższych stopni')
    return {'lvl': lvl, 't': t, 'n': n, 'exp': ex, 'high': hi, 'mean': mean}

# --- GUS: zmiana wynagrodzeń X 2022 -> X 2024 wg wielkich grup ---
def pay_of(gk):
    if not gk.isdigit(): return {'dir': None, 't': 'Brak danych GUS: dochody w tym zawodzie nie są ujęte w badaniu wynagrodzeń według zawodów.'}
    if gk[0] == '0': return {'dir': None, 't': 'Brak danych: badanie GUS wynagrodzeń według zawodów nie obejmuje żołnierzy zawodowych.'}
    if gk[0] == '1': return {'dir': 'up', 't': 'W górę, ale najwolniej ze wszystkich: +21% nominalnie między X 2022 a X 2024 w całej grupie kierowników (GUS).'}
    if gk[0] == '9': return {'dir': 'up', 't': 'W górę, najszybciej ze wszystkich: +33,4% nominalnie między X 2022 a X 2024 w pracach prostych (GUS). To wciąż najniższe płace.'}
    return {'dir': 'up', 't': 'W górę: między X 2022 a X 2024 płace wzrosły nominalnie we wszystkich wielkich grupach zawodów, o 21–33% (GUS). Dokładnej liczby dla tej grupy GUS w komunikacie nie podaje.'}

LABELS = {'up': 'Rośnie', 'flat': 'Stabilnie', 'down': 'Trudniej', None: 'Brak oceny'}

def group(gk, name):
    occ = MAP[gk]; src = []
    lines = []; why = []
    hasD = any(o in D for o in occ)
    hasS = any(o in SUR and o not in MOVED for o in occ)
    for o in occ:
        if o in D:
            a, b = D[o]; lines.append(f'{o}: brakuje pracowników w {a} z {POW} powiatów (rok wcześniej {b}).')
        elif o in SUR and o not in MOVED:
            a, b = SUR[o]; lines.append(f'{o}: w kraju równowaga, ale w {a} powiatach chętnych jest więcej niż ofert (rok wcześniej {b}).')
        elif o in MOVED:
            a, b = MOVED[o]; s = f'{o}: rok temu deficyt, teraz równowaga w {a} powiatach.'
            if o in SUR: s = s[:-1] + f', a w {SUR[o][0]} nadwyżka chętnych.'
            lines.append(s)
        else: lines.append(f'{o}: równowaga, liczba chętnych jest zbliżona do liczby ofert.')
        if o in WHY_OCC and WHY_OCC[o] not in why: why.append(WHY_OCC[o])
    if occ:
        src.append('barometr'); label = 'up' if hasD else 'down' if hasS else 'flat'
        head = {'up': 'Pracodawcom brakuje ludzi w co najmniej jednym zawodzie z tej grupy.', 'down': 'W skali kraju jest równowaga, ale lokalnie chętnych bywa więcej niż ofert.',
                'flat': 'Barometr ocenia tę grupę jako zrównoważoną: nie ma ani deficytu, ani nadwyżki w skali kraju.'}[label]
        if label == 'up' and len(why) < 2: why.append(GEN_DEF)
        ai = ai_of(gk)
        if label == 'down' and ai['lvl'] is not None and ai['lvl'] >= 2 and len(why) < 2: why.append(GEN_SUR)
        why = [head] + why[:2]
    else:
        label = None; lines = ['Barometr zawodów 2026 nie ocenia tej grupy osobno, więc nie wiemy, czy pracowników brakuje, czy jest ich za dużo.']
        why = ['Nie mamy wiarygodnego źródła o popycie na ten zawód w Polsce, dlatego nie dajemy etykiety.']
    ai = ai_of(gk); pay = pay_of(gk)
    if ai['lvl'] is not None: src.append('ilo')
    if pay['dir']: src.append('gus')
    if ai['lvl'] == 3 and len(why) < 3: why.append('Wysoka ekspozycja na AI nie oznacza, że zawód zniknie: autorzy indeksu podkreślają, że zmienia się głównie zakres zadań.')
    return {'n': name, 'label': label, 'demand': lines, 'pay': pay, 'ai': ai, 'why': ' '.join(why), 'src': src}

app = json.load(open(B.parent / 'app.json', encoding='utf-8'))
assert set(MAP) == set(app['groups']), set(MAP) ^ set(app['groups'])
for k, v in MAP.items():
    for o in v: assert o in D or o in BAL, (k, o)
groups = {k: group(k, app['groups'][k]['n']) for k in sorted(app['groups'])}

# --- Zawody własne z osobnym źródłem (WEF: perspektywa globalna, nie polska) ---
def wef(role, pl):
    return {'label': 'up', 'demand': [f'Na świecie: „{role}” ({pl}) są wśród najszybciej rosnących ról do 2030 r. w ankiecie pracodawców WEF.',
                                       'W Polsce: Barometr nie ocenia tego zawodu osobno; „Programiści” są w równowadze.'],
            'why': 'Etykieta opiera się na globalnej ankiecie pracodawców, a nie na polskich danych, więc traktuj ją ostrożnie. To oczekiwania firm, a nie pomiar rynku.', 'src': ['wef', 'barometr'],
            'legend': 'Rośnie oznacza tu: rola rośnie w globalnej ankiecie pracodawców WEF. W polskim Barometrze nie ma dla niej osobnej oceny.'}
AIML = wef('AI and Machine Learning Specialists', 'specjaliści AI i uczenia maszynowego')
jobs = {n: AIML for n in ['Inżynier AI', 'Inżynier uczenia maszynowego', 'Badacz AI', 'Inżynier wizji komputerowej', 'Inżynier MLOps']}
jobs['Inżynier danych'] = wef('Big Data Specialists', 'specjaliści big data')
ev = wef('Autonomous and Electric Vehicle Specialists', 'specjaliści pojazdów autonomicznych i elektrycznych')
ev['demand'][1] = 'W Polsce: Barometr nie ocenia tego zawodu osobno; „Mechanicy pojazdów samochodowych” są w równowadze.'
jobs['Technik elektromobilności'] = ev

out = {'year': YEAR, 'updated': '2026-10', 'labels': {k or 'none': v for k, v in LABELS.items()},
       'legend': 'Rośnie: pracodawcom brakuje ludzi (deficyt w Barometrze). Stabilnie: równowaga. Trudniej: lokalnie więcej chętnych niż ofert.',
       'sources': SOURCES, 'groups': groups, 'jobs': jobs}
p = B.parent / f'market-{YEAR}.json'
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
c = collections.Counter(g['label'] for g in groups.values()); a = collections.Counter(g['ai']['lvl'] for g in groups.values())
print(p.name, len(groups), 'grup |', dict(c), '| AI', dict(a), '|', p.stat().st_size // 1024, 'KB')
