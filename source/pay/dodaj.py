import json,sys
F='chrome_partia.json'
d=json.load(open(F,encoding='utf-8'))
def add(nazwa,kod,oferty,strona=None):
    d['zawody'][nazwa]={'kod_gus':kod,'n_ogloszen_strona':strona,'oferty':oferty}
add('Kierowca C+E','833',[
 ["Kierowca kat. C+E (transport krajowy i międzynarodowy), Rybnik","9000","12000","2026-10-12"],
 ["Kierowca C+E - wywrotka, Kościerzyna","6000","10000","2026-09-30"],
 ["Kierowca krajowy kat. C+E, Wrocław","10000","11000","2026-10-14"],
 ["Kierowca kat. C+E z ADR, DUHABEX (8 lok.)","8200","8500","2026-10-14"],
 ["Kierowca asenizacyjny C, C+E, WC SERWIS Łódź","6400","9350","2026-10-14"],
 ["Kierowca asenizacyjny C, C+E, WC SERWIS Warszawa","7000","9900","2026-10-14"],
 ["Kierowca międzynarodowy kat. C+E, Roos Spedition","14450","14450","2026-10-14"],
 ["Kierowca kat. C+E trasy lokalne, TVM","9700","11200","2026-10-13"],
 ["Kierowca C+E podwójna obsada, TVM","11200","15000","2026-10-13"],
 ["Kierowca C+E Polska-Francja-Polska, DST","14500","16000","2026-10-12"],
 ["Kierowca C+E Polska-Włochy-Polska, DST","14200","15700","2026-10-12"],
 ["Kierowca / Kierowczyni C+E, Jan de Rijk","11000","16000","2026-10-11"],
 ["Kierowca kat. C+E transport międzyn. i krajowy, SK SYSTEM","12000","16000","2026-10-11"],
 ["Kierowca C+E, RAFICARGO","10000","11000","2026-10-10"],
 ["Kierowca kat. C+E, TOMASZ MASŁOŃ","6500","7200","2026-10-07"],
 ["Kierowca C+E, Breslauer Optimum","13000","19000","2026-10-07"],
 ["Kierowca kat. C+E dystrybucja, OMD","7000","8000","2026-10-07"],
 ["Kierowca C+E chłodnia, COLD-TRANSPORT","9000","9500","2026-10-10"],
 ["Kierowca kat. C+E międzynarodowy i krajowy, SEB-MAL","15300","20600","2026-10-09"],
 ["Kierowca kat. C+E w ruchu krajowym, TRANS HOL","9000","12000","2026-10-09"]
],'strona: 1006 ofert')
json.dump(d,open(F,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
import statistics
def med(nm):
    o=d['zawody'][nm]['oferty']; m=[(int(a)+int(b))/2 for _,a,b,_ in o]; return len(m), round(statistics.median(m))
print('Kierowca', med('Kierowca C+E'))

d=json.load(open(F,encoding='utf-8'))
add('Magazynier','933',[
 ["Magazynier (K/M), ACTIVESHOP Wrocław","6000","6800","2026-10-14"],
 ["Magazynier (K/M) Dział składowania, Militaria.pl Wrocław","5545","7000","2026-10-14"],
 ["Magazynier (K/M), GRUPA KAPITAŁOWA SPECJAŁ Wrocław","6850","8000","2026-10-14"],
 ["Magazynier z UDT (k/m), Nagel Polska Wrocław","6500","7000","2026-10-14"],
 ["Magazynier/ka, Job Impulse Łódź","5150","6000","2026-10-14"],
 ["Magazynier / Magazynierka, Randstad Wrocław","5350","8805","2026-10-14"],
 ["Magazynier / Operator Wózka Widłowego, PMI Wrocław","5100","6300","2026-10-14"],
 ["Pracownik Magazynu, FAMCARE Warszawa","5500","6000","2026-10-14"],
 ["Magazynier (K/M) Dział Wysyłkowy, Militaria.pl Wrocław","5545","7300","2026-10-14"],
 ["Magazynier, KOMTEC Białystok","4900","5300","2026-09-25"]
],'strona: 4360 ofert')
json.dump(d,open(F,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('Magazynier', med('Magazynier'))

d=json.load(open(F,encoding='utf-8'))
add('Pielęgniarka','222',[
 ["Pielęgniarka / Pielęgniarz, Medicus Wrocław","9000","13000","2026-10-13"],
 ["Pielęgniarka POZ, ZDROWA RODZINA Warszawa","9000","11000","2026-10-12"],
 ["Pielęgniarka, CENTRUM MEDYCZNE HiH Wrocław","11500","13000","2026-10-06"],
 ["Pielęgniarka do punktu pobrań, HEMATIQ Warszawa","10400","11200","2026-10-05"],
 ["Pielęgniarka środowiska nauczania, MPZ Zielonka (część etatu)","5770","7920","2026-10-13"],
 ["Near Patient Nurse, International SOS (Wrocław)","8750","8750","2026-10-10"],
 ["Pielęgniarz oddziałowy, CARE Zgierz","10000","15000","2026-10-13"]
],'strona: 145 ofert (35 z widełkami)')
json.dump(d,open(F,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('Pielęgniarka', med('Pielęgniarka'))

d=json.load(open(F,encoding='utf-8'))
add('Fryzjer','514',[
 ["Fryzjer/Fryzjerka, NEWME Warszawa","5000","8000","2026-10-12"],
 ["Fryzjer/Fryzjerka, STUDIO URODY AVANTI Warszawa","5200","6240","2026-10-07"],
 ["Fryzjer stylista, Hayk Hair Warszawa","10000","15000","2026-10-09"],
 ["Fryzjer, STUDIO S Piaseczno","4806","10000","2026-10-14"],
 ["Fryzjer stylista, MAVI HAIR Boguszów-Gorce","4860","8000","2026-10-14"],
 ["Fryzjer stylista, S&I EUROPE Biskupice","9000","10000","2026-10-14"],
 ["Barber / Fryzjer, KUŹNIA JĘDRUSIA Zgierz","4806","10000","2026-10-10"],
 ["Fryzjer stylista, Salon Urody A. Mikołajczyk Wrocław","5000","10000","2026-09-30"],
 ["Barber - Fryzjer, BARBERSKY Wrocław (zlecenie)","4000","8000","2026-10-06"],
 ["Fryzjer, STUDIO FRYZUR Brody","6100","7100","2026-10-14"],
 ["Fryzjer, GOSHKA Gliwice","4800","14000","2026-10-13"],
 ["Fryzjer, RENATA Pszczyna","5000","6500","2026-10-11"],
 ["Fryzjer, KOLOROVE Białystok","4806","8000","2026-10-12"],
 ["Fryzjer stylista, Luxury For Your Hair Toruń (zlecenie)","5000","6000","2026-10-12"],
 ["Fryzjer damsko-męski, CONES Lublin","5000","8000","2026-10-12"],
 ["Fryzjer (m/k), Health Resort Panorama Jarosławiec","6500","7500","2026-10-11"],
 ["Fryzjer na dział męski, Zakład Fryzjerski Kolbudy","5000","11000","2026-10-09"],
 ["Barber / Fryzjer, KUISIM Gliwice (zlecenie)","5000","10000","2026-10-09"],
 ["Fryzjer damski, Klinika Estetyki Kielce","5000","15000","2026-10-11"]
],'strona: 68 ofert (48 z widełkami)')
json.dump(d,open(F,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('Fryzjer', med('Fryzjer'))

d=json.load(open(F,encoding='utf-8'))
add('Kelner','512',[
 ["Kelner/Kelnerka, WAPO Warszawa","8500","9500","2026-10-13"],
 ["Kelner, Radisson Blu Sobieski Warszawa","5406","5756","2026-10-12"],
 ["Kelner, VARI Wrocław (zlecenie)","6000","10000","2026-10-12"],
 ["Kelner, PIEROGOWE BAJE Warszawa (zlecenie)","5000","11000","2026-10-11"],
 ["Kelner, Polski Holding Hotelowy Warszawa","4900","5500","2026-10-11"],
 ["Kelner, IZUMI SUSHI Warszawa","7000","9000","2026-10-10"],
 ["Kelner, THAI GROUP Warszawa (zlecenie)","6000","14000","2026-10-09"],
 ["Barman, MOON Warsaw (część etatu)","6000","8000","2026-10-13"]
],'strona: 227 ofert (131 z widełkami)')
json.dump(d,open(F,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('Kelner', med('Kelner'))

d=json.load(open(F,encoding='utf-8'))
add('Kucharz','512',[
 ["Kucharz/Kucharka, PAPILOTKA Warszawa","7000","7500","2026-10-14"],
 ["Kucharz/Pizzerman, GT PIZZA Warszawa (zlecenie)","5000","8000","2026-10-14"],
 ["Kucharz, Masters Catering Warszawa","8000","10000","2026-10-14"],
 ["Kucharka/Kucharz, Polski Holding Hotelowy Warszawa","5900","6500","2026-10-13"],
 ["Kucharz kuchnia gorąca, YOUR CATERING GROUP Łódź","5200","6240","2026-10-08"]
],'strona: 378 ofert (238 z widełkami)')
json.dump(d,open(F,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('Kucharz', med('Kucharz'))
