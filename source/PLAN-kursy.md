# Plan: kursy przy zawodach (monetyzacja)

Status: miejsce w aplikacji gotowe, ukryte dopóki `source/kursy.json` jest puste. Zero reklam bez partnera.

## Zasada nadrzędna
Wiarygodność przed zarobkiem. Kurs pokazujemy tylko tam, gdzie zawód realnie wymaga uprawnień lub kursu (np. operator wózka widłowego, spawacz, kierowca C+E, fryzjer, kosmetolog, opiekun medyczny), zawsze z oznaczeniem „Reklama · partner" i bez wpływu na treść opisu zawodu, zarobków czy kolejności zawodów.

## Co dostaje użytkownik
- Krótka informacja: „Do tej pracy zwykle potrzebny jest kurs/uprawnienia: …" (to jest treść merytoryczna, bez reklamy).
- Pod spodem 1–3 oferty partnerów: nazwa, miasto/online, czas, cena „od", link. Oznaczone jako reklama.
- Zawsze też link do darmowej/oficjalnej ścieżki (np. urząd pracy, UDT), jeśli istnieje, żeby oferta nie wyglądała na jedyną.

## Modele przychodu (od najbezpieczniejszego)
1. **Opłata za wpis (stała, miesięczna)** — firma płaci za obecność przy konkretnych zawodach. Prosta, nie zależy od kliknięć. Hipoteza startowa: niska kwota dla pierwszych partnerów (do dogadania), rosnąca z ruchem.
2. **Prowizja afiliacyjna od zapisu** — płatność tylko za realnego kursanta. Warunek: partner potrafi śledzić źródło zapisu. Stawki w branży są różne i **nie mam zweryfikowanych liczb** — trzeba je wynegocjować na pilotażu.
3. **Płatność za kliknięcie** — najmniej atrakcyjna dla firm szkoleniowych, bo koszt pozyskania kursanta jest wysoki.

Rekomendacja: start od modelu 1 z 3–5 lokalnymi partnerami, model 2 jako opcja, gdy aplikacja ma ruch, który da się pokazać.

## Jak być atrakcyjnym dla firm
- Dopasowanie: użytkownik ogląda dany zawód, więc kurs jest odpowiedzią na jego pytanie, a nie banerem.
- Dane do pokazania firmie: liczba wyświetleń strony zawodu, kliknięć w ofertę, regiony. Trzeba zacząć je liczyć (bez danych osobowych).
- Pakiet pilotażowy: pierwsze 2–3 miesiące taniej lub za darmo, w zamian za opinię i zgodę na raport wyników.
- Oferta „zawód + region": kurs z miasta użytkownika bije ogólny kurs online.

## Prawo i zaufanie
- Oznaczenie „Reklama" widoczne przy każdej płatnej ofercie (UOKiK wymaga jasnego oznaczania treści reklamowych; linki do omówień w wynikach wyszukiwania: ifirma.pl, infor.pl, instalki.pl).
- Polityka prywatności musi opisywać, co się dzieje po kliknięciu w ofertę partnera.
- Do konsultacji z prawnikiem przed pierwszą umową.

## Czego nie wiem (do ustalenia przed startem)
- Ile realnie zapłacą pierwsi partnerzy (test: 3–5 rozmów).
- Które zawody mają największy popyt na kursy (kolejność wdrażania).
- Czy partnerzy chcą wpisu w stałej opłacie czy prowizji.

## Następne kroki
1. Lista ok. 15 zawodów wymagających kursu/uprawnień (z weryfikacją w opisach zawodów).
2. Lista 10–15 potencjalnych partnerów (szkoły, centra szkoleniowe, UDT, ośrodki OSK).
3. Krótki one-pager dla firm + 3–5 rozmów.
4. Dopiero potem wpisy w `source/kursy.json`.
