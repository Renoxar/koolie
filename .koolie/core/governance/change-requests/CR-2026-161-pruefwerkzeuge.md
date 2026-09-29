# Änderungsantrag `CR-2026-161`

| Feld | Inhalt |
|---|---|
| Titel | Die Prüfwerkzeuge in Modulen – und die Konstante, die einer anderen Prüfung gehörte |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-29 |
| Betroffene Artefakte | `tests/scripts/validate-framework.py`, `tests/scripts/pruefungen/` (neu), `tests/scripts/probe-pruefungen.py`, `tests/scripts/sonden/` (neu); `governance/DECISION_LOG.md`, `docs/ROADMAP.md`, `tests/TEST_CATALOG.md`, `CHANGELOG.md`, `VERSION`, Hauptdokument |
| Ebene laut Entscheidungsbaum 6 | Framework Core (Prüfapparat) |
| Art | Wartung ohne Overlay-Bruch; PATCH-Release ohne Kontingent |
| Dringlichkeit | geplant (`K-174` Teil 2, D-473) |
| Status | 🟢 **entschieden am 2026-09-29** (E1 bis E6) |

---

## 1. Anlass

`K-174` Teil 2 (D-473): Validator und Sondenskript waren je rund 11.500 Zeilen in einer Datei – 117 Prüffunktionen und 378 Einheiten. Aufzuteilen, ohne eine Prüfung zu verlieren, und das zeilengleich zu belegen. Dazu die vier Klärungspunkte, die die Triage (D-466) und `1.19.0` (D-473) diesem Release zugeordnet haben: `K-38`, `K-40`, `K-51`, `K-98`.

## 2. Vorprüfung

Vorgelegt am 2026-09-29 mit Schätzung: 0 Läufe, 0 USD, ein bis zwei Sitzungen, rund sechs Sondenläufe. Die Vorlage liegt außerhalb des Repositoriums. Der Owner folgt den Empfehlungen.

## 3. Vorlage zur Entscheidung

| # | Frage | Entscheidung | Preis |
|---|---|---|---|
| E1 | Wie wird geteilt, und wie wird belegt, dass keine Prüfung verloren geht? | Einstieg und Paket: Dateinamen und Schalter bleiben, das Register bleibt im Kopfkommentar des Einstiegs. Der Validator wird nach Gegenstand geteilt, das Sondenskript in der Reihenfolge der Anmeldung. Belegt dreifach: Syntaxbaum je Knoten, Ausgabe des Validators, Sondenlauf in beiden Kodierungen. Zwei Commits – erst die Aufteilung, dann der Inhalt (D-479) | Die Sondenteile folgen der Laufreihenfolge, nicht streng dem Gegenstand |
| E2 | Was tun mit den Mehrfachbindungen, die die Aufteilung zeigt? | Tote Bindungen fallen im Schnitt, das Verhalten bleibt; danach bekommt Prüfung 25 ihr eigenes Muster (D-480) | – |
| E3 | Dauerhafter Schutz gegen eine verschobene, aber nicht verdrahtete Prüfung | Prüfung 104 (D-481) | Sie prüft die Verdrahtung, nicht, was eine Prüfung tut |
| E4 | `K-40`: Clientversion in der Zielspanne | Prüfung 105 als Warnung (D-482) | Eine Aussage über die Schreibweise, nicht über das Verhalten |
| E5 | `K-38` und `K-98`: Meldetext und Zählbereich von Prüfung 46 | Beide Lesarten im Meldetext; die Markerform außerhalb des Zählbereichs als eigener Gegenstand, ohne die Zählung von Kriterium 1 zu ändern (D-483) | – |
| E6 | `K-51` | Geschlossen, D-49 bleibt (D-484) | – |

## 4. Umsetzung

1. **Commit 1, die Aufteilung.** Schnittwerkzeug außerhalb des Repositoriums (Symboltabelle statt Raten: jedes Modul importiert, was es liest); angepasst vorher in der Einzeldatei nur die Selbstbezüge – Prüfung 40 liest Einstieg und Paket, Prüfung 75 die Module mit dem alten Namen, Prüfung 76 die Kernlage in `pruefungen/gemeinsam.py`, die Sonden `D398`, `71`, `75c` und `87` ihren Gegenstand im Modul.
2. **Commit 2, der Inhalt.** Prüfung 25 mit eigenem Muster, Sonde `25b`; Prüfung 104 mit Sonden und Gegenprobe; Prüfung 105 mit Sonden und Gegenprobe; Prüfung 46 mit dem Meldetext (`K-38`) und dem Gegenstand außerhalb des Zählbereichs (`K-98`), Sonden und Gegenproben; Sondenfunktionen `_anker_verlieren` nach ihrer Prüfung benannt.
3. Register, Roadmap, Testkatalog, CHANGELOG, `VERSION`, Bestandsliste, Hauptdokument; Hebung beider Projekte.

## 5. Entscheidung

🟢 **Angenommen am 2026-09-29.**

| # | Entscheidung | Decision Record |
|---|---|---|
| E1 | Einstieg und Paket | D-479 |
| E2 | Die Mehrfachbindungen | D-480 |
| E3 | Prüfung 104 | D-481 |
| E4 | Prüfung 105 (`K-40`) | D-482 |
| E5 | Prüfung 46 (`K-38`, `K-98`) | D-483 |
| E6 | `K-51` geschlossen | D-484 |
