# Batch 24 verification result

Scope: 20 professions from batch_24.json. Checked name, hook/tasks/day, skills (plausibility only), route steps and durations against the Polish law table, and pay_group against the profession's GUS group. No repository files were modified.

| name | verdict | reason | source |
|---|---|---|---|
| Kierownik kas | OK | Real shop-management role. Routes match: branżowa I st. 3 y, technikum 5 y, przyuczenie 0.5 y. Day detail is neutral. Pay group "Pracownicy sprzedaży w sklepach" fits. | — |
| Arborysta | OK | Real profession (arborysta/arborist). Branżowa 3 y (rolnik/ogrodnik) and technikum 5 y (technik ogrodnik, rolnik, agrobiznesu) are consistent. Climbing is described with asekuracja, so no unsafe instruction. Pay group "Rolnicy produkcji roślinnej" is a reasonable fit. | — |
| Operator urządzeń do formowania wyrobów ceramicznych | OK | Slip-casting description (wypełnianie form glinem) is accurate. Branżowa 3 y and szkolenie stanowiskowe 0.5 y are consistent. Pay group "Operatorzy innych maszyn i urządzeń przetwórczych" fits. | — |
| Technik laboratorium filmowego | POPRAW | Title says "Technik" (technikum level), but the only routes are branżowa operator (3 y) and on-the-job training (0.5 y). Those routes do not lead to a technik qualification. Fix: replace the routes with a technikum route, e.g. "Technikum: technik fotografii i multimediów", 5 y, plus praktyki and egzaminy zawodowe (the same pattern as Pirotechnik). Alternatively rename to "Operator laboratorium filmowego". | Internal consistency check; no external source needed |
| Technik ds. chowu sadzowego | NIE WIEM | "Technik ds. chowu sadzowego" is not a recognised school profession title. The zpe.gov.pl page for "technik rybactwa śródlądowego" describes it as a 3-year branżowa I st. programme and a 2-year branżowa II st. programme with matura. I found no technikum version, so the technikum route (5 y) is unconfirmed. "rybak śródlądowy" as a branżowa I st. profession was not confirmed by the search. Pay group "Rybacy" is unverified. | https://zpe.gov.pl/a/drogi-do-zawodu/Ds9sh6rSt |
| Dekorator powierzchni drewnianych | POPRAW | Route 1 label is wrong. "Szkoła branżowa w zawodzie, np. złotnik-jubiler lub zegarmistrz" names metal and watch trades, not wood decoration. Fix: "Szkoła branżowa I stopnia: stolarz" (3 y, years correct). Liceum plastyczne 5 y is correct per the rule. | Internal consistency check; no external source |
| Technik optomechanik | OK | Policealna 2 y after liceum 4 y, and technikum 5 y, are both consistent. Labels "zawód techniczny zgodny z branżą" are vague but not wrong. Optional: name a technikum profession such as "technik optyk". | — |
| Specjalista ds. przeprowadzek | OK | Liceum 4 y plus studia 3 y (licencjat) plus staż 0.5 y is consistent. Sales route 4 y + 1 y is consistent. Pay group "Pośrednicy usług biznesowych" fits. | — |
| Operator automatów do formowania wyrobów szklanych | OK | Accurate glass-forming machine description. Branżowa 3 y and szkolenie 0.5 y are consistent. Pay group fits. | — |
| Licytator | OK | Real occupation (auctioneer). Sales route and studia (licencjat 3 y) durations are consistent. No regulatory issue in the text. | — |
| Pirotechnik | NIE WIEM | The 2016 MSWiA/MR regulation (Dz.U. 2016 poz. 818) sets no certificate or licence for individuals handling pyrotechnics. The 2002 Act on civil explosives, which the regulation refers to, was not checked, so a licence requirement for stage operators is unconfirmed. Given the hook calls it "zawód wysokiego ryzyka", add a route step on any required certification once confirmed. Technikum route (5 y) is consistent. | https://eli.gov.pl/eli/DU/2016/818/ogl/pol/pdf |
| Projektant systemów informacyjno-telekomunikacyjnych | OK | Route durations are consistent: liceum 4 + studia inżynierskie 3.5 + staż 0.5; technikum 5 + staż 0.5; self-taught route. Pay group "Analitycy systemów komputerowych i programiści" fits. Median 15107 is plausible for this group. | — |
| Konserwator sprzętu telekomunikacyjnego | OK | Branżowa 3 y and technikum 5 y match the listed qualifications. Pay group "Monterzy-elektronicy i monterzy instalacji i urządzeń telekomunikacyjnych" fits. | — |
| Inżynier inżynierii środowiska - oczyszczanie miast i gospodarka odpadami | OK | Liceum 4 + studia inżynierskie 3.5 + praktyki 0.5 is consistent. Technikum 5 + studia 3.5 is consistent. Pay group "Inżynierowie (z wyłączeniem elektrotechnologii)" fits. | — |
| Parlamentarzysta | OK | Liceum 4 + studia 5 (prawo is jednolite magisterskie, 5 y) is consistent. Other route steps are plausible. Note: age and citizenship requirements for MPs are not shown. | — |
| Analityk inwestycyjny | OK | Liceum 4 + studia licencjat 3 + staż 0.5 is consistent. Economics profile route plus kurs and 1 y in a bureau is consistent. Pay group "Specjaliści do spraw finansowych" fits. | — |
| Dyrektor sądu | OK | Real title (dyrektor sądu okręgowego/apelacyjnego). Route durations are consistent. Pay group is broad but acceptable. | — |
| Serwisant pojazdów | POPRAW | Route labels and durations are correct. Pay group "Mechanicy maszyn i urządzeń" corresponds to ISCO 7233 (agricultural and industrial machinery), not to motor-vehicle mechanics (ISCO 7231). Fix: change pay_group to "Mechanicy pojazdów silnikowych" or the closest GUS label for motor-vehicle mechanics. GUS label not confirmed by search. | Search did not return the GUS group list; ISCO-08 codes from general knowledge |
| Operator przędzarki do włókien sztucznych | OK | Branżowa 3 y and szkolenie 0.5 y are consistent. Pay group "Operatorzy maszyn do produkcji wyrobów włókienniczych, futrzarskich i skórzanych" fits. | — |
| Literaturoznawca | POPRAW | Route 1 "Przez studia" lists only 3 y (licencjat) but the tasks (researching, writing scholarly work, teaching students) require a magister. Fix: split the study step into "Studia I stopnia: filologia" 3 y plus "Studia II stopnia (magisterskie)" 2 y, total 5 y. Doctorate is needed for academic teaching, which the route does not mention. | Rule-based check (licencjat 3 + magisterskie 2) |

## Counts

- OK: 14
- POPRAW: 4 (Technik laboratorium filmowego, Dekorator powierzchni drewnianych, Serwisant pojazdów, Literaturoznawca)
- NIE WIEM: 2 (Technik ds. chowu sadzowego, Pirotechnik)

## Searches used

3 WebSearch and 2 WebFetch calls (5 of 8 budget).
