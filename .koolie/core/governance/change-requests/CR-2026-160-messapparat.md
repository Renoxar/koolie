# Änderungsantrag `CR-2026-160`

| Feld | Inhalt |
|---|---|
| Titel | Der Messapparat als Paket – und der Cache, den kein fester Pfad teilte |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-29 |
| Betroffene Artefakte | `tests/erhebungen/messen.py`, `tests/erhebungen/apparat/` (neu); `tests/erhebungen/README.md`, `cc-overlay-fuellen.py`, `umgebungen-bauen-b4.py`, `messbaum-schnitt.py`; `install.py` (Testblätter); `tests/scripts/validate-framework.py` (Prüfung 103), `probe-pruefungen.py`; `framework/skills/fw-refactor/TESTS.md` (`SK-007-N04`, `SK-007-N06`), `fw-review-support/TESTS.md`, `fw-docs-update/TESTS.md`, `fw-mr-description/TESTS.md` (Ergebniszellen `K-86`); `tests/TEST_CATALOG.md`; `governance/DECISION_LOG.md`; `docs/ROADMAP.md`; `CHANGELOG.md`, `VERSION`; Protokoll `tests/protocols/2026-09-29-messapparat.md` |
| Ebene laut Entscheidungsbaum 6 | Framework Core (Prüfapparat) |
| Art | Erweiterung ohne Overlay-Bruch; MINOR-Release mit Kontingent |
| Dringlichkeit | geplant (`K-174`, D-436, D-467) |
| Status | 🟢 **entschieden am 2026-09-29** (E1 bis E8) |

---

## 1. Anlass

`K-174`, Auftrag des Owners vom 2026-09-26 (D-436): Nachläufe gezielter und günstiger, die Werkzeuge wartbar. Gemessen: 67 kopierte Skripte in elf Erhebungsablagen ohne einen Test; 10 von 40 Läufen von `1.17.0` wegen des Messaufbaus verworfen; im Median 0,53 bis 0,59 USD je Lauf, davon rund 35.000 Token neu angelegter Cache. Die Triage (D-466) hat dem Posten zehn Klärungspunkte zugeordnet.

## 2. Vorprüfung

Vorgelegt am 2026-09-29 mit dem Brainstorming zum Marktvergleich (Vorlage außerhalb des Repositoriums), Schätzung ca. 26 Läufe und 13 USD, Deckel 40 Läufe und 25 USD. Der Owner folgt allen Empfehlungen, auch denen zum Marktvergleich.

## 3. Vorlage zur Entscheidung

| # | Frage | Entscheidung | Preis |
|---|---|---|---|
| E1 | Ein Release oder zwei? | Zwei: `1.19.0` Messapparat, `1.19.1` Prüfwerkzeuge (Aufteilung von Validator und Sondenskript, `K-38`, `K-40`, `K-51`, `K-98`) | `K-174` bleibt bis `1.19.1` teilweise offen |
| E2 | Form des Apparats | Paket `tests/erhebungen/apparat/` mit `messen.py`: Reihe als Daten, generischer Läufer, Kontingentbuch je Lauf, Selbsttest gegen eine Attrappe; Adapter `claude-code` und `cursor`, die übrigen Packs sagen *unerhoben* | Bäume aus dem Übungsrepositorium baut er noch nicht (`K-190`) |
| E3 | Vorprüfung | Vor jedem bezahlten Lauf, Abbruch statt Lauf: Baum-Hash, `HEAD`, Prompt, Kontingent, Vertrauen, Schutz-Hook, optional die Werkzeuge der Startmeldung | Sie prüft den Aufbau, nicht die Aufgabe |
| E4 | Geteilter Cache | Gemessen statt angenommen – **der feste Pfad spart nichts** (D-475) | Die Annahme der Vorlage war falsch |
| E5 | Kleineres Modell | Nicht als Standard; das Feld `modell` steht in jeder Reihe und in jedem Beleg | – |
| E6 | Klärungspunkte des Apparats | `K-56` (D-471), `K-61` (D-472, Prüfung 103), `K-76` (D-474), `K-86` (D-476), `K-172` (D-477) | – |
| E7 | Alte Werkzeuge | Bleiben liegen und bauen weiter ihre Bäume; zwei hatte `1.18.2` still gebrochen, berichtigt (D-473) | – |
| E8 | Marktvergleich | Festlegungen zur Positionierung und Einplanung (D-478) | – |

## 4. Umsetzung

1. Paket `apparat/` (acht Module) und `messen.py`; Selbsttest zehn Fälle, darunter drei Gegenfälle.
2. `install.py`: Ergebniszellen der Testblätter in der Laufzeitschicht durch `offen` mit Verweis auf den Kern ersetzt; Abbruch bei einer Zeile mit falscher Strichzahl. Sonden `D471`, `D471b`, Gegenprobe `D471a`.
3. Validator: Prüfung 103 (Standmarke einer Ergebniszelle). Sonden `103a`, `103b`, Gegenprobe `103a`.
4. `cc-overlay-fuellen.py`, `umgebungen-bauen-b4.py`: Hüllen der Befehlsschlitze aus dem Korb abgeleitet; `messbaum-schnitt.py aufzeichnungen --tools-bleiben` für den Baumbau von Bündel 4.
5. Messung: Gleichwertigkeit und Cache (16 Läufe), `K-86` und `K-172` (sechs Läufe); Protokoll `2026-09-29-messapparat.md`.
6. Register, Roadmap, CHANGELOG, `VERSION`, Bestandsliste, Hauptdokument; Hebung beider Projekte.

## 5. Entscheidung

🟢 **Angenommen am 2026-09-29.**

| # | Entscheidung | Decision Record |
|---|---|---|
| E6 (`K-56`) | Testblätter ohne fremde Ergebnisse ausgeliefert | D-471 |
| E6 (`K-61`) | Standmarke und Prüfung 103 | D-472 |
| E1 bis E3, E5, E7 | Der Messapparat als Paket | D-473 |
| E6 (`K-76`) | Die Rücknahme als `review`-Zelle | D-474 |
| E4 | Der Cache und der feste Pfad | D-475 |
| E6 (`K-86`) | Die Zurechnung der drei Positivfälle | D-476 |
| E6 (`K-172`) | Schreibende Zellen auf einem Arbeitsbranch | D-477 |
| E8 | Der Marktvergleich | D-478 |
