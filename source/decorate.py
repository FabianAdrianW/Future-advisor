"""Dokleja do drzewa ilustracje, krotsze nazwy i gotowe opisy zawodow.
Uzycie: python3 -I decorate.py tree.json details.json app.json images.txt
"""
import json, re, sys

SRC, DETAILS, OUT, IMGS = sys.argv[1:5]
tree = json.load(open(SRC, encoding="utf-8"))
details = json.load(open(DETAILS, encoding="utf-8"))

# dwa rozne zawody ESCO maja po polsku te sama nazwe: rozrozniamy je
def _dedupe(nodes):
    for n in nodes:
        if "c" in n:
            _dedupe(n["c"])
        elif n["n"] == "Konserwator dzieł sztuki" and n.get("d", "").startswith("Konserwatorzy prowadzą działania korygujące"):
            n["a"] = ["konserwator dzieł sztuki"] + n.get("a", [])
            n["n"] = "Restaurator dzieł sztuki"
_dedupe(tree["areas"])

# ---- profile grup zawodow (groups.txt): umiejetnosci, plusy, minusy i drogi dla kazdego zawodu ----
import os
HERE = os.path.dirname(os.path.abspath(DETAILS))
STEP_TYPES = {"szkola", "studia", "kurs", "projekt", "praktyka", "egzamin"}

def macro_route(kind, arg):
    arg = (arg or "").strip()
    years = None
    m = re.match(r"^(.*?) (\d+(?:\.\d+)?)$", arg)
    if m and kind in ("ST", "KU"):
        arg, years = m.group(1), float(m.group(2))
    if kind == "BR":
        return {"n": "Szkoła branżowa", "s": [["szkola", "Szkoła branżowa I stopnia: " + arg, 3], ["praktyka", "Praktyki u pracodawcy w trakcie szkoły", 0], ["egzamin", "Egzamin zawodowy", 0]]}
    if kind == "TE":
        return {"n": "Technikum", "s": [["szkola", "Technikum: " + arg, 5], ["praktyka", "Praktyki zawodowe w trakcie szkoły", 0], ["egzamin", "Egzaminy zawodowe i matura", 0]]}
    if kind == "ST":
        return {"n": "Przez studia", "s": [["szkola", "Liceum", 4], ["studia", "Studia: " + arg, years or 3], ["praktyka", "Staż lub praktyki w zawodzie", 0.5]]}
    if kind == "PO":
        return {"n": "Szkoła policealna", "s": [["szkola", "Szkoła średnia", 4], ["kurs", "Szkoła policealna: " + arg, 2], ["egzamin", "Egzamin zawodowy", 0]]}
    if kind == "KU":
        return {"n": "Kurs i praktyka", "s": [["kurs", arg, years or 0.5], ["praktyka", "Pierwsza praca pod okiem doświadczonej osoby", 0.5]]}
    if kind == "PR":
        return {"n": "Od razu do pracy", "s": [["praktyka", arg or "Przyuczenie na stanowisku u pracodawcy", 0.5]]}
    if kind == "AW":
        return {"n": "Studia i awans", "s": [["szkola", "Szkoła średnia", 4], ["studia", "Studia: " + arg, 3], ["praktyka", "Kilka lat pracy w branży", 4], ["praktyka", "Awans na stanowisko kierownicze", 0]]}
    raise ValueError(kind)

def parse_route(rest):
    m = re.match(r"^(BR|TE|ST|PO|KU|PR|AW)(?: (.*))?$", rest)
    if m:
        return macro_route(m.group(1), m.group(2))
    name, sep, body = rest.partition(": ")
    assert sep, rest
    steps = []
    for part in body.split(" > "):
        t, title, years = part.split("=")
        assert t in STEP_TYPES, (t, rest)
        y = float(years)
        steps.append([t, title.strip(), int(y) if y == int(y) else y])
    return {"n": name.strip(), "s": steps}

def parse_groups(path):
    raw, cur = {}, None
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.strip() or line.startswith("# "):
            continue
        if line.startswith("#"):
            m = re.match(r"^#(\S+)(?: =(\S+))? (.+)$", line)
            assert m, line
            assert m.group(1) not in raw, line
            cur = {"n": m.group(3).strip(), "base": m.group(2), "R": []}
            raw[m.group(1)] = cur
        else:
            tag, _, rest = line.partition(" ")
            assert tag in "SPMR" and len(tag) == 1, line
            if tag == "R":
                cur["R"].append(rest.strip())
            else:
                cur[tag] = rest.strip()
    out = {}
    def resolve(key):
        if key in out:
            return out[key]
        g = raw[key]
        b = resolve(g["base"]) if g["base"] else {}
        res = {"n": g["n"]}
        if "S" in g:
            res["s"] = []
            for item in g["S"].split(", "):
                name, root = item.rsplit("/", 1)
                assert root in "LSPRNO", (key, item)
                res["s"].append([name, root])
            assert len(res["s"]) == 6, (key, len(res["s"]))
        else:
            res["s"] = b["s"]
        for tag, k in (("P", "p"), ("M", "m")):
            if tag in g:
                res[k] = [x.strip() for x in g[tag].split(";")]
                assert len(res[k]) == 3, (key, tag)
            else:
                res[k] = b[k]
        res["r"] = [parse_route(r) for r in g["R"]] if g["R"] else b["r"]
        assert len({r["n"] for r in res["r"]}) == len(res["r"]), (key, "powtorzona nazwa drogi")
        out[key] = res
        return res
    for key in raw:
        resolve(key)
    return out

G = parse_groups(os.path.join(HERE, "groups.txt"))
USED_G = set()

def gkey(u):
    if not u:
        return "251"
    k = u if u in G else u[:3]
    assert k in G, u
    return k

# zawody dopisane recznie: do ktorego profilu grupy naleza
OWN_G = {
    "Twórca internetowy": "X-tworca", "Streamer": "X-tworca", "Podcaster": "X-tworca", "Specjalista ds. mediów społecznościowych": "243",
    "Zawodnik e-sportowy": "X-esport", "Trener e-sportowy": "X-esport", "Monter pomp ciepła": "712", "Technik elektromobilności": "723",
    "Założyciel startupu": "X-startup", "Scrum master": "242", "Specjalista ds. ESG": "242", "Operator drona": "X-dron", "Doula": "X-doula",
    "Podolog": "325", "Instruktor jogi": "342", "Florysta": "X-florysta", "Technik cyberbezpieczeństwa": "252", "Inspektor ochrony danych": "242",
}


# Korekty grupy płacowej (GUS) dla zawodów z błędnym przypisaniem z tabeli kodów (wykryte w weryfikacji próbki 100 zawodów).
PAY_FIX = {
    "Specjalista zooterapii": "323", "Koordynator programu oświatowego": "235", "Koordynator ds. publikacji": "264",
    "Preparator zwierząt": "731", "Cegielnik": "754", "Dziekan": "231", "Dyrektor elektrowni": "132", "Dyrektor kopalni": "132",
    "Dyrektor archiwum": "262", "Genealog": "262", "Metrolog": "311", "Asystent ds. nieruchomości": "333",
    "Dyspozytor medyczny": "321", "Operator kamery": "343", "Annotator danych": "351", "Kierownik urzędu pracy": "335",
    "Fotoedytor": "265", "Analityk ds. efektywności energetycznej": "214", "Kontroler urządzeń koksowniczych": "313",
    "Operator zautomatyzowanej linii produkcyjnej": "812", "Operator prasy brykietowej": "812",
    "Operator urządzeń do utylizacji odpadów płynnych": "818", "Specjalista w zakresie substancji roślinnych": "314",
    "Technik przenoszenia zarodków zwierzęcych": "324", "Projektant makiet scenograficznych": "265",
    "Wykonawca mebli wyplatanych": "752", "Specjalista ds. sprzedaży egzekucyjnej nieruchomości": "244",
    "Pracownik ds. wsparcia dla osób z zaburzeniami psychicznym": "532", "Asystent nauczyciela dla dzieci o specjalnych potrzebach edukacyjnych": "531",
    "Nauczyciel nauczania przedszkolnego dzieci ze specjalnymi potrzebami edukacyjnymi/nauczycielka nauczania przedszkolnego dzieci ze specjalnymi potrzebami edukacyjnymi": "234", "Doradca edukacyjny": "263", "Konsultant podróży": "332",
    "Operator centralnej sterowni w rafinerii ropy naftowej": "813", "Koordynator programów zatrudnienia": "242",
    "Artysta sztuki ulicznej / artystka sztuki ulicznej": "343", "Operator maszyn do produkcji obuwia": "753",
}
PAY_FIX_USED = set()

def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

AREA_IMG = {
    "it": ("Laptop", "Robot"), "nauka": ("Microscope", "Atom symbol"), "przyr": ("Deciduous tree", "Globe showing europe-africa"),
    "inz": ("Gear", "Triangular ruler"), "bud": ("Building construction", "Brick"), "prod": ("Factory", "Nut and bolt"),
    "mech": ("Wrench", "High voltage"), "rzem": ("Carpentry saw", "Sewing needle"), "trans": ("Delivery truck", "Airplane"),
    "roln": ("Tractor", "Cow face"), "zdrowie": ("Stethoscope", "Pill"), "opieka": ("People hugging", "Teddy bear"),
    "edu": ("Graduation cap", "Open book"), "spol": ("Brain", "Classical building"), "prawo": ("Balance scale", "Scroll"),
    "biznes": ("Briefcase", "Chart increasing"), "fin": ("Coin", "Bar chart"), "sprzed": ("Shopping bags", "Megaphone"),
    "biuro": ("Clipboard", "Paperclip"), "media": ("Newspaper", "Microphone"), "sztuka": ("Performing arts", "Clapper board"),
    "design": ("Paintbrush", "Framed picture"), "gastro": ("Fork and knife with plate", "Bellhop bell"),
    "uslugi": ("Barber pole", "Lotion bottle"), "sport": ("Soccer ball", "Running shoe"), "bezp": ("Shield", "Fire engine"),
}

IMG3 = {
    "011": "Military medal", "021": "Military helmet", "031": "Military helmet", "111": "Ballot box with ballot", "112": "Necktie",
    "121": "Briefcase", "122": "Megaphone", "131": "Sheaf of rice", "132": "Factory", "133": "Desktop computer", "134": "Office building",
    "141": "Hotel", "142": "Convenience store", "143": "Stadium", "211": "Atom symbol", "212": "Abacus", "213": "Dna", "214": "Gear",
    "215": "High voltage", "216": "Artist palette", "221": "Stethoscope", "222": "Syringe", "223": "Herb", "224": "Ambulance",
    "225": "Dog face", "226": "Tooth", "231": "Graduation cap", "232": "Toolbox", "233": "Teacher", "234": "Crayon", "235": "Open book",
    "241": "Chart increasing", "242": "Identification card", "243": "Bullseye", "251": "Technologist", "252": "Globe with meridians",
    "261": "Balance scale", "262": "Amphora", "263": "Brain", "264": "Fountain pen", "265": "Performing arts", "311": "Nut and bolt",
    "312": "Safety vest", "313": "Electric plug", "314": "Petri dish", "315": "Airplane", "321": "X-ray", "322": "Adhesive bandage",
    "323": "Lotus", "324": "Cat face", "325": "Thermometer", "331": "Coin", "332": "Handshake", "333": "Ledger", "334": "Clipboard",
    "335": "Magnifying glass tilted left", "341": "People hugging", "342": "Sports medal", "343": "Film projector", "351": "Keyboard",
    "352": "Control knobs", "411": "File folder", "412": "Telephone", "413": "Computer mouse", "421": "Credit card", "422": "Bellhop bell",
    "431": "Receipt", "432": "Package", "441": "Envelope", "511": "Luggage", "512": "Cook", "513": "Hot beverage", "514": "Scissors",
    "515": "Key", "516": "Sparkles", "521": "Basket", "522": "Shopping cart", "523": "Ticket", "524": "Label", "531": "Teddy bear",
    "532": "Manual wheelchair", "541": "Fire engine", "611": "Ear of corn", "612": "Cow face", "613": "Farmer", "621": "Evergreen tree",
    "622": "Fish", "711": "Brick", "712": "Ladder", "713": "Bucket", "721": "Goggles", "722": "Hammer", "723": "Mechanic",
    "731": "Gem stone", "732": "Printer", "741": "Light bulb", "742": "Mobile phone", "751": "Bread", "752": "Carpentry saw",
    "753": "Sewing needle", "754": "Magnifying glass tilted right", "811": "Pick", "812": "Magnet", "813": "Test tube", "814": "Wheel",
    "815": "Thread", "816": "Canned food", "817": "Wood", "818": "Mechanical arm", "821": "Screwdriver", "831": "Locomotive",
    "832": "Taxi", "833": "Articulated lorry", "834": "Construction", "835": "Anchor", "911": "Broom", "912": "Sponge", "921": "Carrot",
    "931": "Construction worker", "932": "Package", "933": "Pickup truck", "941": "Bowl with spoon", "951": "Bicycle", "952": "Basket",
    "961": "Recycling symbol", "962": "Motor scooter",
}

IMG4 = {
    "1211": "Bank", "1223": "Light bulb", "1323": "Building construction", "1324": "Delivery truck", "1341": "Teddy bear",
    "1342": "Hospital", "1343": "House with garden", "1344": "People hugging", "1345": "School", "1346": "Bank", "1439": "Sparkles",
    "2142": "Building construction", "2143": "Leaf fluttering in wind", "2161": "House", "2162": "National park", "2163": "Chair",
    "2164": "Cityscape", "2165": "World map", "2513": "Desktop computer", "2631": "Chart increasing", "2634": "Brain",
    "2635": "People hugging", "2636": "Place of worship", "2656": "Studio microphone", "3111": "Test tube", "3112": "Straight ruler",
    "3118": "Triangular ruler", "3123": "Safety vest", "3257": "Rescue workers helmet", "3331": "Ship", "3332": "Party popper",
    "3333": "Identification card", "3351": "Passport control", "3355": "Detective", "3411": "Scroll", "3412": "People hugging",
    "3413": "Place of worship", "3431": "Camera", "3432": "Couch and lamp", "3434": "Cook", "3522": "Satellite antenna",
    "4221": "Beach with umbrella", "4224": "Hotel", "5113": "Compass", "5164": "Paw prints", "5165": "Automobile",
    "5241": "Camera with flash", "5246": "Hot beverage", "5312": "Backpack", "7512": "Croissant", "8341": "Tractor",
}

# slowa kluczowe w nazwie -> ilustracja (pierwsze trafienie wygrywa)
KEY = [
    (r"pilot wyciecz|przewodni", "Compass"), (r"pilot|lotnic|samolot|śmigłow", "Airplane"), (r"kosmo|astronaut", "Rocket"),
    (r"\bgier\b|gry komput|gier komput|gier cyfr", "Video game"), (r"animac|animator", "Film frames"),
    (r"interfejs|stron internet|web", "Desktop computer"), (r"programist|oprogramowan|aplikacj", "Technologist"),
    (r"cyberbezp|bezpieczeństwa (system|inform|teleinf)", "Locked"), (r"robot|automatyk", "Robot"), (r"danych|statysty", "Bar chart"),
    (r"grafik|ilustrator|rysowni", "Artist palette"), (r"fotograf", "Camera"), (r"film|kamer|reżyser|wideo", "Movie camera"),
    (r"dźwięk|audio|akusty|nagra", "Headphone"), (r"śpiewa|piosenk|wokal", "Singer"), (r"muzy|kompozytor|dyrygent|instrument", "Guitar"),
    (r"tance|choreograf|balet", "Ballet shoes"), (r"aktor|teatr|performer|cyrk", "Performing arts"),
    (r"pisar|poet|scenarzyst|autor|copywriter", "Fountain pen"), (r"dziennikar|redaktor|reporter|korespondent", "Newspaper"),
    (r"vloger|bloger|prezenter|spiker", "Studio microphone"), (r"tłumacz|lingwist|filolog|lektor", "Speech balloon"),
    (r"bibliote", "Books"), (r"muze|archiw|zabytk|kustosz", "Amphora"),
    (r"przedszkol|opiekun.*dzie|niani", "Teddy bear"), (r"nauczyciel|wykładowc|korepetytor", "Teacher"),
    (r"psycholog|psychoterap|terapeut", "Brain"), (r"dentyst|stomatolog|ortodont", "Tooth"), (r"farmaceut|aptek|farmac", "Pill"),
    (r"pielęgniar|położn", "Syringe"), (r"weteryna", "Dog face"), (r"ratownik med|paramedyk", "Ambulance"),
    (r"fizjoterap|masaży|rehabilit", "Person getting massage"), (r"dietet|żywieni", "Green salad"), (r"optyk|optometr|okulist", "Glasses"),
    (r"lekarz|chirurg|medycyn", "Stethoscope"), (r"pszczel", "Honeybee"), (r"koni|jeździec", "Horse face"), (r"psów|\bpsa\b|treser", "Dog face"),
    (r"zwierz|zoo", "Paw prints"), (r"ryb|akwakult|rybak", "Fish"), (r"ogrodni|sadowni|kwiat|florys|szkółk", "Tulip"),
    (r"leśni|drzew|drwal", "Evergreen tree"), (r"winoro|winiar|enolog|sommelier", "Grapes"), (r"rolni|upraw|plon", "Ear of corn"),
    (r"piekar|cukiern|czekolad", "Croissant"), (r"barman|barist|kelner|sommelier", "Hot beverage"), (r"kuchar|kuchni|kucharz", "Cook"),
    (r"fryzjer", "Person getting haircut"), (r"kosmety|wizaż|makijaż|manicur|paznok", "Lipstick"),
    (r"fitness|siłown|kulturyst", "Person lifting weights"), (r"piłk", "Soccer ball"), (r"tenis", "Tennis"), (r"pływa|ratownik wodn|nurek|nurk", "Ring buoy"),
    (r"trener|sportow|instruktor sport|zawodni", "Sports medal"), (r"strażak|pożar", "Firefighter"), (r"policj|detektyw", "Police officer"),
    (r"żołnierz|wojsk|oficer|saper", "Military helmet"), (r"ochron|strażnik|porządkow", "Shield"),
    (r"sędzi", "Judge"), (r"prawni|adwokat|radca prawn|prokurat|notarius|komornik", "Balance scale"),
    (r"księgow|audytor|podatk|rachunk", "Receipt"), (r"bank|kredyt|pożycz", "Bank"), (r"ubezpiecz", "Umbrella"),
    (r"makler|inwest|giełd|papier.*wartość", "Chart increasing"), (r"ekonomi", "Bar chart"),
    (r"marketing|reklam|promocj", "Megaphone"), (r"nieruchomo", "House"), (r"hurtown", "Package"), (r"sklep", "Convenience store"),
    (r"sprzedaw|handlow|ekspedient", "Shopping bags"), (r"taksów|kierowca samochodu osob|szofer", "Taxi"), (r"ciężarów", "Articulated lorry"),
    (r"autobus|tramwaj|motornicz", "Bus"), (r"maszynista|kolej|pociąg|dyżurny ruchu", "Locomotive"),
    (r"statk|marynar|żeglug|okręt|kapitan|bosman|sternik", "Ship"), (r"logisty|spedy|import|eksport|magazyn", "Package"),
    (r"rower", "Bicycle"), (r"samochod|pojazd|lakiernik", "Automobile"), (r"mechanik", "Mechanic"),
    (r"elektryk|elektro|energet|elektrown", "High voltage"), (r"spawacz|spawaln", "Goggles"), (r"hydraulik|kanaliz|wodoci|gazown", "Wrench"),
    (r"stolar|cieśl|drewn|meblow", "Carpentry saw"), (r"dekarz|dach", "House"), (r"murar|betoniar|zbrojar|budowl|brygadzista", "Brick"),
    (r"architekt krajobraz", "National park"), (r"architekt wnętrz|wnętrz", "Couch and lamp"), (r"architekt|urbanist", "Triangular ruler"),
    (r"geodet|kartograf|mierni", "World map"), (r"projektant mody|mody|odzież|krawiec|krawc|szwacz|tkanin|kostium", "T-shirt"),
    (r"obuw|szewc|cholew", "Mans shoe"), (r"jubiler|złotni|biżuter", "Ring"), (r"zegarm", "Watch"), (r"cerami|garncar|szkł|szkla", "Amphora"),
    (r"chemi|laborant|laborator", "Test tube"), (r"biolog|biotech|genet|mikrobio|botani|zoolog", "Dna"), (r"astronom", "Telescope"),
    (r"fizyk", "Atom symbol"), (r"geolog|geofiz|sejsmo|hydrolog", "Mountain"), (r"meteorolog|klimat", "Sun behind cloud"),
    (r"matemat|aktuari", "Abacus"), (r"sieci|administrator system|baz danych|informaty", "Desktop computer"),
    (r"drukar|poligraf|introlig", "Printer"), (r"górni|kopal|wiertni|wydobyw", "Pick"), (r"sprzątacz|sprzątając|czyszcz", "Broom"),
    (r"kurier|doręczy|listonosz|poczt", "Envelope"), (r"recepcj", "Bellhop bell"), (r"hotel", "Hotel"), (r"turyst|podróż|biur.* podróży", "Luggage"),
    (r"socjaln|opiekun", "People hugging"), (r"duchown|relig|zakon|pastor", "Place of worship"),
    (r"polity|parlament|dyplomat|ambasad|konsul|burmistrz", "Classical building"), (r"bibliot", "Books"),
    (r"odpad|recykl|śmieci", "Recycling symbol"), (r"środowisk|ekolog", "Leaf fluttering in wind"), (r"wod", "Droplet"),
]
KEY = [(re.compile(p), img) for p, img in KEY]

def by_keyword(name):
    low = name.lower()
    for rx, img in KEY:
        if rx.search(low):
            return img
    return None

LABELS = {
    "Cechowacze skal i znaków na szkle oraz na wyrobach z metali, zdobnicy ceramiki i szkła, grawerzy i trawiacze": "Zdobnicy szkła i ceramiki, grawerzy",
    "Specjaliści do spraw sprzedaży produktów technicznych i medycznych (z wyłączeniem technologii informacyjno-komunikacyjnych)": "Sprzedaż produktów technicznych i medycznych",
    "Specjaliści do spraw sprzedaży z dziedziny technologii informacyjno-komunikacyjnych": "Sprzedaż w branży IT",
    "Pozostały średni personel w dziedzinie kultury i sztuki": "Zaplecze sceny, filmu i kultury",
    "Średni personel ochrony zdrowia (pozostali)": "Inni asystenci ochrony zdrowia",
    "Średni personel w dziedzinie statystyki, matematyki i w dziedzinach pokrewnych": "Asystenci statystyki i matematyki",
    "Klasyfikatorzy i testerzy produktów (z wyłączeniem żywności i napojów)": "Kontrolerzy jakości produktów",
    "Operatorzy maszyn i urządzeń do produkcji betonu, asfaltobetonu, elementów betonowych i kamiennych i pokrewni": "Maszyny do produkcji betonu i elementów kamiennych",
    "Twórca oprogramowania komputerowego technologii informacyjno-telekomunikacyjnych": "Twórcy oprogramowania specjalistycznego",
    "Piloci statków powietrznych i średni personel w dziedzinach pokrewnych": "Piloci samolotów i śmigłowców",
    "Maszyniści i operatorzy maszyn i urządzeń dźwigowo-transportowych i pokrewni": "Operatorzy dźwigów i suwnic",
    "Technicy nauk fizycznych, chemicznych i technicznych (pozostali)": "Inni technicy",
    "Operatorzy maszyn do produkcji wyrobów włókienniczych, futrzarskich i skórzanych (pozostali)": "Inne maszyny włókiennicze i skórzane",
    "Monterzy aparatury, maszyn i sprzętu elektrycznego i sprzętu elektronicznego": "Monterzy sprzętu elektrycznego i elektronicznego",
    "Opiekunowie zwierząt domowych i pracownicy zajmujący się zwierzętami": "Opiekunowie zwierząt",
    "Inspektorzy ochrony środowiska, medycyny pracy i bezpieczeństwa i higieny pracy": "Inspektorzy BHP i ochrony środowiska",
    "Operatorzy maszyn i urządzeń przemysłu spożywczego i pokrewni": "Operatorzy maszyn w przemyśle spożywczym",
    "Technicy w dziedzinie dokumentacji medycznej i informacji zdrowotnej": "Dokumentacja medyczna",
    "Pracownicy do spraw statystycznych, finansowych i ubezpieczeniowych": "Statystyka, finanse i ubezpieczenia: obsługa",
    "Odczytywacze liczników i wybieracze monet (żetonów) z automatów": "Odczyt liczników i obsługa automatów",
    "Operatorzy urządzeń pakujących, do napełniania butelek i urządzeń znakujących": "Maszyny pakujące i rozlewnicze",
}

def clean_label(s):
    if s in LABELS:
        return LABELS[s]
    s = re.sub(r"technologii informacyjno-(tele)?komunikacyjn(ych|ej)", "IT", s)
    s = re.sub(r"informacyjno-telekomunikacyjn(ych|ej|ego)", "IT", s)
    s = re.sub(r",? i (specjaliści )?(w )?(nauk|dziedzin(ach)?) pokrewn(ych|e)", "", s)
    s = re.sub(r",? i pokrewni\b", "", s)
    s = re.sub(r"\bdo spraw\b", "ds.", s)
    m = re.match(r"^Operatorzy (maszyn i urządzeń|maszyn|urządzeń) do (.+)$", s)
    if m:
        s = ("Urządzenia do " if m.group(1) == "urządzeń" else "Maszyny do ") + m.group(2)
    m = re.match(r"^(.+) \(pozostali\)$", s)
    if m:
        s = "Inne: " + m.group(1)[0].lower() + m.group(1)[1:]
    return s

def short_name(s):
    """Krotsza nazwa na karty: przy dlugich nazwach dwurodzajowych zostaje pierwsza forma."""
    if len(s) > 34 and "/" in s:
        first = re.split(r"\s*/\s*", s)[0].strip()
        if len(first) >= 5:
            return first
    return s

# ---- warstwa uzupelniajaca: zawody, ktorych klasyfikacja ESCO jeszcze nie ma ----
AI_KW = "ai sztuczna inteligencja uczenie maszynowe machine learning ml"
OWN = [
    ("Inżynier AI", [7, 1, 1, 1, 0, 0], "Robot", ["inżynier sztucznej inteligencji", "AI engineer", "LLM engineer", "programista AI"],
     "Inżynierowie AI budują aplikacje i narzędzia, które korzystają z gotowych modeli sztucznej inteligencji, np. modeli językowych. Łączą model z danymi firmy, piszą dla niego instrukcje, testują jakość odpowiedzi i pilnują kosztów oraz bezpieczeństwa."),
    ("Inżynier uczenia maszynowego", [8, 0, 0, 2, 0, 0], "Brain", ["machine learning engineer", "ML engineer", "inżynier ML"],
     "Inżynierowie uczenia maszynowego trenują modele, które uczą się na danych: rozpoznają obrazy, przewidują popyt, polecają filmy. Przygotowują dane, dobierają metodę, sprawdzają trafność modelu i wdrażają go do działającego produktu."),
    ("Inżynier danych", [8, 0, 0, 2, 0, 0], "Gear", ["data engineer"],
     "Inżynierowie danych budują systemy, które zbierają, czyszczą i dostarczają dane analitykom oraz modelom AI. Dbają o to, żeby dane były aktualne, kompletne i dostępne na czas."),
    ("Inżynier MLOps", [7, 0, 1, 2, 0, 0], "Desktop computer", ["MLOps engineer", "inżynier wdrożeń modeli AI"],
     "Inżynierowie MLOps odpowiadają za to, żeby modele AI działały stabilnie po wdrożeniu. Automatyzują trenowanie i aktualizacje modeli, monitorują ich jakość i reagują, gdy model zaczyna się mylić."),
    ("Badacz AI", [9, 1, 0, 0, 0, 0], "Microscope", ["AI researcher", "naukowiec ds. sztucznej inteligencji", "research scientist"],
     "Badacze AI opracowują nowe metody uczenia maszynowego i sprawdzają je w eksperymentach. Czytają i piszą publikacje naukowe, a ich wyniki trafiają potem do produktów."),
    ("Inżynier wizji komputerowej", [7, 0, 0, 1, 0, 2], "Camera", ["computer vision engineer", "inżynier widzenia komputerowego"],
     "Inżynierowie wizji komputerowej uczą komputery rozumieć obrazy i wideo. Tworzą systemy, które rozpoznają wady produktów na taśmie, znaki drogowe albo zmiany na zdjęciach medycznych."),
    ("Inżynier promptów", [4, 5, 1, 0, 0, 0], "Keyboard", ["prompt engineer", "projektant promptów"],
     "Inżynierowie promptów projektują i testują instrukcje dla modeli językowych, tak żeby odpowiadały trafnie, bezpiecznie i w określonym stylu. Coraz częściej jest to część pracy inżyniera AI lub specjalisty od treści niż osobne stanowisko."),
    ("Specjalista ds. etyki i regulacji AI", [3, 5, 2, 0, 0, 0], "Balance scale", ["AI governance specialist", "specjalista ds. zgodności AI", "AI ethics officer"],
     "Specjaliści ds. etyki i regulacji AI sprawdzają, czy systemy sztucznej inteligencji są zgodne z prawem i nie krzywdzą ludzi. Oceniają ryzyko, piszą zasady korzystania z AI w firmie i współpracują z prawnikami oraz inżynierami."),
    ("Annotator danych", [5, 3, 0, 0, 0, 2], "Label", ["data annotator", "trener danych AI", "data labeler"],
     "Annotatorzy danych przygotowują przykłady, na których uczą się modele AI: opisują zdjęcia, oznaczają obiekty, oceniają odpowiedzi modeli. To jedna z prostszych dróg wejścia do branży AI."),
    ("Specjalista ds. automatyzacji AI", [6, 1, 2, 1, 0, 0], "Mechanical arm", ["AI automation specialist", "specjalista automatyzacji procesów"],
     "Specjaliści ds. automatyzacji AI łączą narzędzia sztucznej inteligencji z codzienną pracą firmy. Budują automatyczne procesy, np. sortowanie zgłoszeń czy przygotowanie raportów, często w narzędziach bez pisania kodu."),
]
# zawody z ESCO, ktore sa o AI, ale maja nazwy, po ktorych nikt ich nie znajdzie
RENAME = {
    "Specjalista ds. zarządzania danymi": ("Data scientist", "Bar chart", "data scientist badacz danych " + AI_KW),
    "Projektant inteligentnych systemów technologii informacyjno-telekomunikacyjnych": ("Projektant systemów AI", "Sparkles", AI_KW),
    "Inżynier wiedzy": ("Inżynier wiedzy", "Books", "systemy eksperckie " + AI_KW),
    "Inżynier języka naturalnego": ("Inżynier języka naturalnego", "Speech balloon", "nlp przetwarzanie języka naturalnego " + AI_KW),
}
details["Inżynier AI"] = {
    "hook": "Budujesz aplikacje, które korzystają z gotowych modeli AI: czaty, wyszukiwarki, asystentów. Twoja praca to sprawić, żeby model odpowiadał trafnie i bezpiecznie.",
    "tasks": ["Łączysz model AI z danymi i narzędziami firmy", "Piszesz i testujesz instrukcje dla modelu", "Mierzysz, jak często model się myli", "Pilnujesz kosztów, szybkości i bezpieczeństwa"],
    "day": [["9:30", "Przegląd błędów: asystent źle odpowiedział klientowi"], ["10:30", "Zmieniasz instrukcję i sposób wyszukiwania dokumentów"], ["13:00", "Uruchamiasz test na dwustu przykładowych pytaniach"], ["16:00", "Wynik jest lepszy, wdrażasz zmianę i opisujesz ją zespołowi"]],
    "skills": [["Programowanie w Pythonie", "L"], ["Rozumienie, jak działają modele", "L"], ["Precyzyjne pisanie", "S"], ["Eksperymentowanie i pomiar", "L"], ["Angielski techniczny", "S"], ["Rozmowa z użytkownikami", "P"]],
    "plus": ["Pracujesz z najnowszą technologią", "Efekt widać szybko", "Przydaje się w każdej branży"],
    "minus": ["Narzędzia zmieniają się co kilka miesięcy", "Model bywa nieprzewidywalny", "Dużo testowania i poprawek"],
    "path": ["Naucz się podstaw programowania w Pythonie", "Zbuduj prostego asystenta na własnych notatkach i pokaż go w sieci", "Studia informatyczne lub pokrewne pomagają, ale liczą się działające projekty"],
    "try": "Napisz dla czata AI instrukcję, po której wytłumaczy ułamki jak dziesięciolatkowi. Popraw ją trzy razy i porównaj odpowiedzi."
}

# drogi do zawodu (szkola, studia, kursy, projekty, praktyki, egzaminy) dla zawodow z pelnym opisem
import os
ROUTES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(DETAILS)), "routes.json"), encoding="utf-8"))
for name, routes in ROUTES.items():
    assert name in details, name
    details[name]["routes"] = routes
assert all("routes" in d for d in details.values()), [k for k, d in details.items() if "routes" not in d]

def take(nodes, name):
    """Wyjmuje zawod o danej nazwie z drzewa (takze z listy odmian)."""
    for n in list(nodes):
        if "c" in n:
            got = take(n["c"], name)
            if got:
                if not n["c"]:
                    nodes.remove(n)
                return got
        elif n["n"] == name:
            nodes.remove(n)
            return n
        else:
            for s in n.get("s", []):
                if s["n"] == name:
                    n["s"].remove(s)
                    return {"n": s["n"], "d": s["d"], "a": [], "w": n["w"]}
    return None

# Kolejne braki znalezione w sieci (WEF, LinkedIn, klasyfikacja MRPiPS, nowe zawody MEN).
# (obszar, nazwa nowej grupy albo None, ilustracja grupy,
#  [zawody z ESCO do przeniesienia: (nazwa ESCO, nowa nazwa, ilustracja, slowa kluczowe)],
#  [nowe zawody: (nazwa, wagi L S P R N O, ilustracja, inne nazwy, opis, slowa kluczowe)])
EXTRA = [
    ("it", "Sztuczna inteligencja", "Robot",
     [(old, new, img, kw) for old, (new, img, kw) in RENAME.items()],
     [(n, w, img, alts, desc, AI_KW) for n, w, img, alts, desc in OWN] + [
         ("Konsultant ds. AI", [5, 2, 3, 0, 0, 0], "Light bulb", ["AI consultant", "doradca ds. sztucznej inteligencji", "strateg AI"],
          "Konsultanci ds. AI pomagają firmom zdecydować, gdzie sztuczna inteligencja naprawdę się przyda. Analizują procesy, dobierają narzędzia, liczą koszty i szkolą pracowników.", AI_KW)]),
    ("it", "Chmura i nowe technologie", "Globe with meridians", [], [
        ("Specjalista ds. chmury obliczeniowej", [8, 0, 1, 1, 0, 0], "Globe with meridians", ["cloud engineer", "architekt chmury", "inżynier chmury"],
         "Specjaliści ds. chmury obliczeniowej przenoszą systemy firm na serwery wynajmowane przez internet i dbają, żeby działały szybko, bezpiecznie i tanio. Projektują architekturę, automatyzują uruchamianie usług i pilnują kosztów.", "cloud chmura"),
        ("Inżynier DevOps", [8, 0, 1, 1, 0, 0], "Gear", ["DevOps engineer"],
         "Inżynierowie DevOps łączą pracę programistów i administratorów. Automatyzują testowanie i wdrażanie oprogramowania, tak żeby nowe wersje trafiały do użytkowników szybko i bez awarii.", "devops"),
        ("Inżynier Internetu rzeczy", [6, 0, 0, 4, 0, 0], "Satellite antenna", ["IoT engineer", "inżynier IoT"],
         "Inżynierowie Internetu rzeczy tworzą urządzenia podłączone do sieci: czujniki, inteligentne liczniki, sprzęt domowy. Łączą elektronikę, oprogramowanie i przesyłanie danych.", "iot internet rzeczy smart home"),
        ("Specjalista ds. technologii blockchain", [8, 1, 1, 0, 0, 0], "Coin", ["blockchain developer", "programista blockchain"],
         "Specjaliści ds. technologii blockchain budują systemy oparte na rozproszonych rejestrach, w których zapisów nie da się po cichu zmienić. Piszą i testują tzw. inteligentne kontrakty oraz dbają o ich bezpieczeństwo.", "blockchain kryptowaluty"),
        ("Projektant VR i AR", [4, 0, 1, 1, 0, 4], "Glasses", ["specjalista ds. wirtualnej rzeczywistości", "VR developer", "projektant rozszerzonej rzeczywistości"],
         "Projektanci VR i AR tworzą trójwymiarowe światy i nakładki na rzeczywistość do gier, szkoleń, medycyny i handlu. Projektują przestrzeń i sposób poruszania się w niej, tak żeby korzystanie było wygodne.", "vr ar wirtualna rzeczywistosc rozszerzona"),
    ]),
    ("it", "Cyberbezpieczeństwo", "Locked", [
        ("Tester odporności oprogramowania", "Etyczny haker (pentester)", "Locked", "pentester tester penetracyjny ethical hacker cyberbezpieczenstwo cybersecurity"),
        ("Administrator bezpieczeństwa systemów informacyjno-telekomunikacyjnych", "Administrator bezpieczeństwa IT", "Locked", "cyberbezpieczenstwo cybersecurity"),
        ("Konsultant ds. bezpieczeństwa technologii informacyjno-telekomunikacyjnych", "Konsultant ds. cyberbezpieczeństwa", "Shield", "cyberbezpieczenstwo cybersecurity"),
        ("Technik ds. bezpieczeństwa systemów informacyjno-telekomunikacyjnych", "Technik bezpieczeństwa IT", "Locked", "cyberbezpieczenstwo cybersecurity"),
    ], [
        ("Technik cyberbezpieczeństwa", [7, 0, 1, 2, 0, 0], "Locked", ["specjalista ds. cyberbezpieczeństwa"],
         "Technicy cyberbezpieczeństwa chronią sieci i komputery przed włamaniami. Konfigurują zabezpieczenia, obserwują ruch w sieci i reagują na incydenty. Od września 2026 r. to nowy zawód w polskich technikach.", "cyberbezpieczenstwo cybersecurity"),
        ("Inspektor ochrony danych", [3, 5, 2, 0, 0, 0], "Shield", ["IOD", "data protection officer", "specjalista ds. RODO"],
         "Inspektorzy ochrony danych pilnują, żeby firma lub urząd przetwarzały dane osobowe zgodnie z prawem. Doradzają, szkolą pracowników, sprawdzają procedury i kontaktują się z urzędem nadzorczym.", "rodo gdpr dpo iod prywatnosc"),
    ]),
    ("media", "Twórcy internetowi", "Studio microphone", [
        ("Vloger / vlogerka", "Vloger / vlogerka", "Movie camera", "youtuber youtube wideo"),
        ("Bloger / blogerka", "Bloger / blogerka", "Fountain pen", "blog"),
    ], [
        ("Twórca internetowy", [0, 4, 3, 0, 0, 3], "Camera with flash", ["influencer", "youtuber", "tiktoker", "twórca treści", "content creator"],
         "Twórcy internetowi regularnie publikują filmy, zdjęcia lub teksty i budują wokół nich społeczność. Planują treści, nagrywają, montują, rozmawiają z odbiorcami i współpracują z markami.", "influencer youtuber tiktok instagram content creator"),
        ("Streamer", [1, 3, 3, 0, 0, 3], "Video game", ["streamer gier", "twórca transmisji na żywo"],
         "Streamerzy prowadzą transmisje na żywo, najczęściej z gier, i na bieżąco rozmawiają z widzami. Dbają o stałe godziny nadawania, jakość obrazu i dźwięku oraz o atmosferę na czacie.", "twitch streaming transmisje na zywo"),
        ("Podcaster", [0, 6, 2, 0, 0, 2], "Studio microphone", ["twórca podcastów", "prowadzący podcast"],
         "Podcasterzy tworzą audycje do słuchania w internecie. Wybierają tematy, zapraszają gości, nagrywają rozmowy, montują odcinki i je promują.", "podcast"),
        ("Specjalista ds. mediów społecznościowych", [2, 4, 3, 0, 0, 1], "Megaphone", ["social media manager", "social media specialist"],
         "Specjaliści ds. mediów społecznościowych prowadzą profile firm i instytucji. Planują publikacje, piszą posty, odpowiadają na komentarze i sprawdzają w statystykach, co działa.", "social media facebook instagram tiktok"),
    ]),
    ("sport", "E-sport", "Video game", [], [
        ("Zawodnik e-sportowy", [3, 0, 3, 0, 2, 2], "Video game", ["gracz zawodowy", "e-sportowiec", "pro gamer"],
         "Zawodnicy e-sportowi zawodowo rywalizują w grach komputerowych, zwykle w drużynie. Trenują wiele godzin dziennie, analizują mecze rywali i startują w turniejach.", "esport e-sport gaming"),
        ("Trener e-sportowy", [3, 1, 5, 0, 1, 0], "Sports medal", ["coach e-sportowy", "analityk e-sportowy"],
         "Trenerzy e-sportowi przygotowują drużyny graczy do turniejów. Układają taktykę, analizują nagrania meczów, planują treningi i dbają o współpracę oraz formę psychiczną zawodników.", "esport e-sport gaming"),
    ]),
    ("mech", "Zielona energia", "Leaf fluttering in wind", [
        ("Monter paneli fotowoltaicznych", "Monter paneli fotowoltaicznych", "Sun behind cloud", "fotowoltaika oze zielona energia instalator"),
        ("Technik turbin wiatrowych", "Technik turbin wiatrowych", "Leaf fluttering in wind", "wiatraki oze zielona energia"),
    ], [
        ("Monter pomp ciepła", [1, 0, 1, 8, 0, 0], "Wrench", ["instalator pomp ciepła", "serwisant pomp ciepła"],
         "Monterzy pomp ciepła instalują i serwisują urządzenia, które ogrzewają budynki energią z powietrza lub gruntu. Dobierają moc urządzenia, podłączają instalację, uruchamiają ją i uczą właścicieli obsługi.", "pompy ciepla pompa ciepla oze zielona energia ogrzewanie"),
        ("Technik elektromobilności", [3, 0, 0, 7, 0, 0], "Automobile", ["mechanik pojazdów elektrycznych", "serwisant samochodów elektrycznych"],
         "Technicy elektromobilności diagnozują i naprawiają samochody elektryczne i hybrydowe oraz stacje ładowania. Pracują z instalacjami wysokiego napięcia, więc ściśle trzymają się zasad bezpieczeństwa. Zawód jest w klasyfikacji szkolnictwa branżowego od 2025 r.", "samochody elektryczne ev ladowarki"),
    ]),
    ("biznes", "Startupy i nowe role", "Rocket", [], [
        ("Założyciel startupu", [4, 1, 5, 0, 0, 0], "Rocket", ["founder", "przedsiębiorca", "startupowiec"],
         "Założyciele startupów tworzą własną firmę wokół nowego produktu lub usługi. Szukają klientów i pieniędzy, budują zespół i na początku sami robią niemal wszystko.", "startup founder przedsiebiorca wlasna firma"),
        ("Scrum master", [3, 1, 6, 0, 0, 0], "Clipboard", ["agile coach", "lider zespołu zwinnego"],
         "Scrum masterzy pomagają zespołom, najczęściej programistów, pracować w krótkich, regularnych etapach. Prowadzą spotkania, usuwają przeszkody i pilnują, żeby zespół nie brał na siebie za dużo naraz.", "scrum agile"),
        ("Specjalista ds. ESG", [3, 3, 2, 0, 2, 0], "Leaf fluttering in wind", ["specjalista ds. zrównoważonego rozwoju", "sustainability specialist"],
         "Specjaliści ds. ESG sprawdzają, jak firma wpływa na środowisko i ludzi, i pomagają ten wpływ poprawić. Zbierają dane, np. o emisjach, przygotowują raporty i proponują zmiany.", "esg zrownowazony rozwoj sustainability csr"),
    ]),
    ("trans", None, None, [], [
        ("Operator drona", [3, 0, 0, 5, 0, 2], "Airplane", ["pilot drona", "operator bezzałogowych statków powietrznych"],
         "Operatorzy dronów sterują bezzałogowymi statkami powietrznymi. Filmują z powietrza, robią pomiary terenu, sprawdzają stan linii energetycznych i pomagają w akcjach ratowniczych. Loty zawodowe wymagają odpowiednich uprawnień.", "dron drony bsp"),
    ]),
    ("opieka", None, None, [], [
        ("Doula", [0, 1, 7, 0, 2, 0], "People hugging", ["asystentka porodowa"],
         "Doule wspierają kobietę i jej bliskich w ciąży, podczas porodu i po nim. Dają wsparcie emocjonalne i praktyczne, ale nie wykonują czynności medycznych, bo to zadanie położnej i lekarza.", "doula porod"),
    ]),
    ("zdrowie", None, None, [], [
        ("Podolog", [0, 0, 4, 3, 3, 0], "Adhesive bandage", ["specjalista pielęgnacji stóp"],
         "Podolodzy zajmują się zdrowiem stóp: usuwają odciski i modzele, pomagają przy wrastających paznokciach, dobierają wkładki. Przy poważniejszych zmianach kierują do lekarza.", "stopy podologia"),
    ]),
    ("sport", None, None, [], [
        ("Instruktor jogi", [0, 1, 5, 0, 4, 0], "Sports medal", ["nauczyciel jogi"],
         "Instruktorzy jogi prowadzą zajęcia łączące ćwiczenia ciała, oddech i koncentrację. Dobierają pozycje do możliwości grupy, poprawiają ustawienie ciała i dbają o bezpieczeństwo.", "joga yoga"),
    ]),
    ("roln", None, None, [], [
        ("Florysta", [0, 0, 2, 3, 2, 3], "Tulip", ["bukieciarz", "asystent florystyczny"],
         "Floryści układają kompozycje z kwiatów i roślin: bukiety, dekoracje ślubne, wystrój wnętrz. Dobierają rośliny do okazji, dbają o ich świeżość i doradzają klientom.", "kwiaciarnia kwiaty bukiety"),
    ]),
    ("design", None, None, [], [
        ("Projektant poziomów gier", [4, 2, 0, 0, 0, 4], "Video game", ["level designer"],
         "Projektanci poziomów gier budują plansze, misje i zagadki, przez które przechodzi gracz. Rozmieszczają przeszkody, przeciwników i nagrody tak, żeby gra była ciekawa i miała dobre tempo.", "level design gamedev gry"),
    ]),
]
# zawody z ESCO, ktore zostaja na miejscu, ale dostaja zrozumiala nazwe i slowa kluczowe
RETAG = {
    "Analityk środowiska użytkownika": ("Badacz UX", "ux researcher user experience analityk ux"),
    "Specjalista ds. optymalizacji aparatu wyszukiwania": ("Specjalista SEO", "seo pozycjonowanie google"),
    "Autor tekstów i sloganów reklamowych": ("Copywriter", "copywriter teksty reklamowe"),
    "Artysta sztuki ciała": ("Tatuażysta", "tatuaz tatuator piercing piercer"),
    "Fryzjer męski / fryzjerka męska": ("Fryzjer męski / fryzjerka męska", "barber"),
    "Chirurg pielęgniarz drzew": ("Arborysta", "arborysta pielegnacja drzew"),
    "Operator obrabiarki sterowanej numerycznie": ("Operator CNC", "cnc obrabiarka"),
    "Autor programów nauczania przez internet": ("Twórca kursów online", "e-learning kursy online"),
    "Kierownik ds. społeczności internetowych": ("Community manager", "community manager moderator spolecznosci"),
    "Operator centrum danych": ("Operator centrum danych", "data center datacenter serwerownia"),
    "Kierownik ds. odpowiedzialności społecznej przedsiębiorstw": ("Kierownik ds. odpowiedzialności społecznej (CSR)", "csr esg zrownowazony rozwoj"),
    "Dyspozytor medyczny": ("Dyspozytor medyczny", "operator numerow alarmowych 112 999"),
}

def find(nodes, name):
    for n in nodes:
        if "c" in n:
            got = find(n["c"], name)
            if got:
                return got
        elif n["n"] == name:
            return n
        else:
            for s in n.get("s", []):
                if s["n"] == name:
                    return s
    return None

def rename(n, old, new):
    if new != old:
        if "a" in n:
            n["a"] = [old[0].lower() + old[1:]] + n["a"]
        n["n"] = new

for old, (new, kw) in RETAG.items():
    n = find(tree["areas"], old)
    assert n, old
    rename(n, old, new)
    n["kw"] = kw

OWN_COUNT = 0
for area_id, gname, gimg, moved, new_jobs in EXTRA:
    leaves = []
    for old, new, img, kw in moved:
        n = take(tree["areas"], old)
        assert n, old
        n.setdefault("a", [])
        rename(n, old, new)
        n["img"], n["kw"] = img, kw
        n["gk"] = gkey(n.get("u"))
        for k in ("u", "m", "g"):
            n.pop(k, None)
        leaves.append(n)
    for name, w, img, alts, desc, kw in new_jobs:
        assert not find(tree["areas"], name), name
        leaves.append({"n": name, "w": w, "d": desc, "a": alts, "img": img, "kw": kw, "own": 1, "gk": OWN_G.get(name, "251")})
        OWN_COUNT += 1
    area = next(a for a in tree["areas"] if a["id"] == area_id)
    if gname:
        area["c"].append({"n": gname, "img": gimg, "c": leaves})
    else:
        area["c"].extend(leaves)

def cnt(n):
    if "c" in n:
        return sum(cnt(c) for c in n["c"])
    return 1 + len(n.get("s", [])) - (1 if n.get("fam") else 0)

def recalc(n):
    if "c" not in n:
        return
    acc, tot = [0.0] * 6, 0
    for c in n["c"]:
        recalc(c)
        k = cnt(c)
        tot += k
        for i in range(6):
            acc[i] += c["w"][i] * k
    n["k"], n["w"] = tot, [round(a / tot, 1) for a in acc]

for a in tree["areas"]:
    recalc(a)
tree["stats"]["total"] = sum(a["k"] for a in tree["areas"])
tree["stats"]["own"] = OWN_COUNT

used = set()
missing_details = set(details)

def deco(n, parent_img):
    is_branch = "c" in n
    full = n["n"]
    img = None
    if "id" in n:                       # obszar
        img, img2 = AREA_IMG[n["id"]]
        n["i2"] = slug(img2); used.add(img2)
    elif "m" in n and is_branch:
        img = IMG3[n["m"]]
    elif is_branch:
        img = IMG4.get(n.get("u", "")) or by_keyword(full)
    else:
        img = by_keyword(full) or IMG4.get(n.get("u", "")) or (IMG3.get(n["m"]) if "m" in n else None)
    img = n.pop("img", None) or img or parent_img
    used.add(img)
    n["i"] = slug(img)
    if is_branch:
        if "id" not in n and "m" not in n:
            n["n"] = clean_label(full)
        elif "m" in n and "u" in n:
            n["n"] = clean_label(full)
        for c in n["c"]:
            deco(c, img)
    else:
        _pf = next((k for k in (full, n.get("n")) if k in PAY_FIX), None)
        if _pf: PAY_FIX_USED.add(_pf)
        n["gk"] = n.get("gk") or gkey(n.get("u"))
        if _pf: n["pk"] = PAY_FIX[_pf]
        assert n["gk"] in G, n["gk"]
        USED_G.add(n["gk"])
        if n.get("fam"):
            n["n"] = clean_label(full)
        else:
            sn = short_name(full)
            if sn != full:
                n["n"], n["fn"] = sn, full
        if full in details:
            n["x"] = details[full]
            missing_details.discard(full)
    for k in ("m", "u"):
        n.pop(k, None)

for a in tree["areas"]:
    deco(a, None)

assert not missing_details, missing_details
print("korekty grup niedopasowane:", sorted(set(PAY_FIX) - PAY_FIX_USED))
tree["stats"]["detailed"] = len(details)
tree["groups"] = {k: G[k] for k in sorted(USED_G)}
tree["stats"]["groups"] = len(USED_G)

EXTRA = ["Puzzle piece", "Abacus", "Laptop", "Books", "Speech balloon", "Classical building", "Handshake", "Graduation cap", "Megaphone",
         "Hammer and wrench", "Racing car", "Brick", "Paw prints", "Stethoscope", "Soccer ball", "Artist palette", "Headphone", "Camera",
         "Seedling", "Student", "Sparkles", "Compass", "Red heart", "Magnifying glass tilted left", "Waving hand", "Bullseye", "Light bulb", "Pushpin"]
used.update(EXTRA)
open(IMGS, "w", encoding="utf-8").write("\n".join(sorted(used)) + "\n")
json.dump(tree, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("ilustracje:", len(used), "| zawody z gotowym opisem:", len(details))
