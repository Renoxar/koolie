# Testprotokolle

Ablage der Ergebnisse aus `.koolie/core/tests/TEST_CATALOG.md` (Verfahren Punkt 4).

| Regel | Inhalt |
|---|---|
| Dateiname | `JJJJ-MM-TT-<Test-ID>.md` für einen einzelnen Testfall, `JJJJ-MM-TT-release-<Version>.md` für einen vollständigen Lauf |
| Pflichtangaben | Framework-Version, Datum, Prüfmethode, ausgeführter Befehl oder Testblatt, unverändertes Ergebnis, Bewertung |
| Zusätzlich bei einem Nachweis aus dem **Ausbleiben** einer Wirkung | der Beleg des Laufs selbst – Ausgabe, Aufzeichnung oder Positivkontrolle im selben Lauf –, der Ausweis aufgehobener Schutzvorkehrungen des Clients und, wenn die Abwesenheit über ein Suchwerkzeug belegt wird, eine **Anwesenheitsprobe desselben Gegenstandstyps** (Verfahren Punkt 7) |
| Zusätzlich bei `sitzung` | Version des KI-Clients, Modell (falls wählbar) – Verfahren Punkt 5 |
| Aufbewahrung | Protokolle werden nicht überschrieben; ein Wiederholungslauf erhält ein eigenes Protokoll |
| **Gegenzeichnung** | **Nur Abnahmeprotokolle des Testkatalogs** (`JJJJ-MM-TT-FW-…`) tragen einen Abschnitt *Gegenzeichnung*; **Prüfung 80** verlangt ihn ohne offenes `<TBD>`. **Arbeits- und Meßprotokolle bekommen ihn nicht** (D-319): *Eine Gegenzeichnung bestätigt eine Abnahme; ein Meßprotokoll trägt seinen Beleg in sich.* 🔴 **Ältere Meßprotokolle führen den Abschnitt noch mit offenem `<TBD>`, und das bleibt so** – sie sind Chronik (D-273) und halten fest, daß dort einmal eine Gegenzeichnung vorgesehen war. *Wer eine Aufzeichnung nachträglich glattzieht, verliert genau die Angabe, die sie trägt.* |

Ein Ergebnisstatus außer `offen` im Testkatalog MUSS auf ein Protokoll in diesem Verzeichnis verweisen.
