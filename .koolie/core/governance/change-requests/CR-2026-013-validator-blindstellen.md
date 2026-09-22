# Änderungsantrag `CR-2026-013`

| Feld | Inhalt |
|---|---|
| Titel | Vier Blindstellen des Validators, gefunden beim Ausführen von `FW-KO-01` |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | `tests/scripts/validate-framework.py`; `tests/TEST_CATALOG.md`; `docs/ROADMAP.md`; neu: `tests/protocols/2026-09-10-FW-KO-01.md`, `tests/protocols/2026-09-10-FW-DS-03.md` |
| Ebene laut Entscheidungsbaum 6 | Core (Werkzeug) |
| Art | Fehlerbehebung und Verschärfung |
| Dringlichkeit | regulär (Review-Zyklus) |

## 1. Anlass und Problem

`FW-KO-01` („Struktur- und Formatkonsistenz", Basistest, Prüfmethode `skript`) verlangt
`0 Fehler` aus `validate-framework.py`. Der Testfall war seit der Erstfassung `offen`. Beim
Ausführen zeigte sich, was ein grüner Lauf allein nicht zeigt: **Von 22 gezielt eingebrachten
Defekten blieben sechs unbemerkt.** Zwei gingen auf falsch gesetzte Sonden zurück. Vier waren
echte Blindstellen.

**Die Pfadvergleiche der Inhaltsprüfung liefen unter Windows ins Leere.**
`os.path.relpath` liefert dort Backslashes; verglichen wurde gegen Präfixe mit Schrägstrich.
Folge: Prüfung 11 (Codeblöcke mit vier oder mehr Backticks) hat unter Windows **nie**
ausgelöst – auf dem Betriebssystem, auf dem das Framework entwickelt wird. Ebenso griff die
Ausnahme für `project-overlay/forbidden-terms.txt` nicht. In diesem Repository fiel das nicht
auf, weil die Sperrbegriffsliste des Übungsrepositorys leer ist; in einem echten Projekt
stehen dort die realen Kunden-, Produkt- und Systemnamen, und der Validator hätte die Datei
gegen sich selbst geprüft – ein Fehler je Begriff. `check_links` normalisiert den Pfad seit
jeher, `check_content` nicht.

**Die Quellen des Hauptdokuments waren von der Inhaltsprüfung ausgenommen.** `build` steht in
der Überspringliste, weil dort die Erzeugnisse eines Projekts liegen. Unter dem Kern liegen
darunter aber die 33 handgeschriebenen Kapitelquellen – ungeprüft auf Secrets, E-Mail-Adressen,
IP-Adressen, Sperrbegriffe und vier Backticks. Das ist die unangenehmste Stelle für diese
Lücke: Vier Backticks brechen genau dort die Assemblierung, und ein Secret erschiene im
ausgelieferten Dokument.

**Die Statusprüfung kannte nur eine von zwei Schreibweisen.** Ein Overlay erklärt seinen
Status zweimal – als Zeile im Projektsteckbrief und als Aussage im Aktivierungsabschnitt.
`--strict-overlay` suchte nur die zweite Form. Der Steckbrief konnte `inaktiv` sagen, während
die Prüfung grün meldete.

**Die Secret-Muster des Validators waren enger als die des Schutz-Hooks.** Der Hook blockiert
sechs Kategorien in einer Werkzeugeingabe, der Validator suchte drei im Bestand. Was der Hook
im Vorbeigehen verhindert – `api_key = …`, Bearer-Token, Verbindungszeichenfolge mit
Anmeldedaten –, durfte versioniert im Repository stehen. Dieselbe Zusage war an zwei Stellen
unterschiedlich streng, ohne dass irgendwo stand, warum.

**Nebenbefund zur Aussagekraft.** Der erste Durchgang lief ohne PyYAML. Die Prüfungen 4, 5
und 8 prüfen dann nur, ob ein Frontmatter vorhanden ist, nicht was darin steht – eine
entfernte `description` blieb unbemerkt, das Overlay-Manifest wurde gar nicht geprüft. Der
Validator schwieg dazu. Ein Release-Nachweis unter dieser Bedingung behauptet mehr, als er
geprüft hat.

## 2. Vorgeschlagene Änderung

**Pfade normalisieren.** `check_content` normalisiert den relativen Pfad wie `check_links`
seit jeher (`.replace(os.sep, "/")`). Eine Zeile.

**Die Quellen des Hauptdokuments prüfen, das Erzeugnis nicht.** `build` bleibt in der
Überspringliste – dort liegen die Build-Verzeichnisse eines Projekts. `<CORE_DIR>/build/doc`
wird zusätzlich durchlaufen. Das Werkzeug daneben (`assemble.py`, `build/README.md`) bleibt
außen vor: Es führt eigene Marker in spitzen Klammern, die keine Framework-Platzhalter sind
und sonst als unregistriert gemeldet würden.

**Jede Statuserklärung prüfen.** Beide Schreibweisen werden erfasst, aber nur am Zeilenanfang:
eine Erwähnung im Fließtext oder in einem Ausnahmeregister ist keine Erklärung. Fehlt jede
Angabe, ist auch das ein Fehler – bisher galt „nicht gefunden" wie „nicht `aktiv`", was
zufällig dasselbe Ergebnis lieferte, aber nicht dasselbe meint.

**Die Secret-Muster angleichen.** Der Validator übernimmt die drei fehlenden Kategorien des
Hooks. Ein Wert in spitzen Klammern ist ausgenommen: Ein Platzhalter ist konstruktionsbedingt
kein Secret, und das Framework schreibt seine Beispiele durchgehend so.

Die naheliegende Gegenthese – die engeren Muster seien Absicht, weil das Repository
Zugangsdaten-Muster *beschreibt* und sich sonst selbst melden würde – wurde geprüft und
widerlegt: Über beide Repositorys ergeben die breiteren Muster **einen** Treffer, und der ist
ein als synthetisch gekennzeichneter Platzhalter. Die Ausnahme für spitze Klammern deckt ihn
ab; eine Ausnahmeliste braucht es nicht.

Die umgekehrte Angleichung – dem Hook die Platzhalterausnahme zu geben – unterbleibt
bewusst. Beim Hook ist die strengere Auslegung die sichere: Ein Falschalarm blockiert eine
Operation, die der Mensch anders formuliert. Beim Validator hielte derselbe Falschalarm jeden
Release-Lauf an. Der Unterschied ist begründet und im Protokoll zu `FW-DS-03` festgehalten.

**Sagen, wenn eingeschränkt geprüft wird.** Fehlt PyYAML, meldet der Validator eine Warnung
und benennt die drei betroffenen Prüfungen.

**Zwei kleinere Ergänzungen im selben Zug:** Das Overlay-Manifest wird auch auf seine
Kopfschlüssel geprüft (`manifest_version`, `project_code`, `overlay_version`) – bisher nur die
Dokumenteinträge, während die Kurzbeschreibung „YAML-Schema" versprach. Und der Name des
Kernverzeichnisses steht im Skript einmal statt an drei Stellen.

## 3. Prüffragen (durch Owner auszufüllen)

- [x] Richtige Ebene nach Entscheidungsbaum 6? — Ja. Keine Regel ändert sich; betroffen ist das Prüfwerkzeug. Die Kernregelmenge, die Client Packs und die Laufzeitschicht bleiben unberührt.
- [x] Verschärfungsprinzip eingehalten? — Ja. Jede Änderung erweitert, was gemeldet wird; keine hebt eine bestehende Meldung auf. Die einzige neue Ausnahme (Platzhalter in spitzen Klammern) betrifft ein Muster, das es vorher gar nicht gab.
- [x] Widerspruchsfreiheit geprüft? — Die Kurzbeschreibung des Skripts nannte für die Prüfungen 6, 8, 9 und 11 einen größeren Umfang, als tatsächlich geprüft wurde; sie ist nachgezogen. Validator, `FW-KO-04` und `install.py --check`: 0 Fehler.
- [x] Laufzeitfassungen betroffen? — Nein. Kein installiertes Artefakt ändert sich; der Validator liegt im Kern und wird von `--update` mitgeführt.
- [x] Belegstatus korrekt? — `FW-KO-01` und `FW-DS-03` sind mit Protokoll belegt. Beide prüfen Skripte, nicht das Verhalten eines Clients; das bleibt AP2.
- [x] Test- und Validierungsbedarf? — Zwei Testfälle ausgeführt, siehe Abschnitt 5.
- [x] Auswirkungen auf Overlays und laufende Onboardings? — Ein bestehendes Projekt kann nach dem Wechsel Fehler sehen, die es vorher nicht sah: vier Backticks in geschützten Ablagen, ein widersprüchlicher Overlay-Status, ein Secret-Muster im Bestand. Das sind keine neuen Regeln, sondern Regeln, die vorher nicht durchgesetzt wurden. Migrationshinweis im CHANGELOG.
- [x] Dokumentation? — CHANGELOG, Decision Log, Roadmap, Testkatalog, zwei Testprotokolle.

## 4. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | angenommen |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Eine Prüfung, die nichts findet, weil sie nichts prüft, ist schlimmer als keine Prüfung: Sie erzeugt Vertrauen, das sie nicht deckt. Prüfung 11 hat auf dem Entwicklungsbetriebssystem nie ausgelöst, die Quellen des Hauptdokuments waren ausgenommen, ein Overlay konnte sich widersprechen, und derselbe Schutz war an zwei Stellen unterschiedlich streng. Alle vier Befunde stammen aus dem Wirksamkeitsnachweis eines Testfalls, der ohne ihn grün gewesen wäre. |
| Ziel-Release | 0.11.0 |
| Decision-Log-Eintrag | D-23 |

## 5. Umsetzung (nach Annahme)

- [x] `check_content` normalisiert den relativen Pfad wie `check_links`
- [x] `iter_text_files` durchläuft zusätzlich `<CORE_DIR>/build/doc`; `build/out` und das Werkzeug daneben bleiben außen vor
- [x] `_overlay_status_angaben` erfasst beide Schreibweisen am Zeilenanfang; fehlende Angabe ist ein eigener Fehler
- [x] `SECRET_PATTERNS` um Bearer-Token, Zugangsdaten-Zuweisung und Verbindungszeichenfolge erweitert, Platzhalter in spitzen Klammern ausgenommen
- [x] Warnung, wenn PyYAML fehlt, mit Nennung der drei eingeschränkten Prüfungen
- [x] Kopfschlüssel des Overlay-Manifests werden geprüft; `KERN` steht einmal statt dreimal
- [x] Sammelnennungen mit Auslassungszeichen (`framework/core/…`) gelten nicht mehr als Pfadangabe – ein Falschalarm, den erst die neue Abdeckung von `build/doc` sichtbar gemacht hat
- [x] **`FW-KO-01` (skript) bestanden**: 22 von 22 Sonden gemeldet, nachdem im ersten Durchgang sechs unbemerkt blieben. Protokoll: `leitwerk-core/tests/protocols/2026-09-10-FW-KO-01.md`
- [x] **`FW-DS-03` (skript) bestanden**: zehn synthetische Werkzeugeingaben, alle sechs Musterkategorien abgedeckt. Protokoll: `leitwerk-core/tests/protocols/2026-09-10-FW-DS-03.md`
- [x] Validator gegen beide Repositorys: 0 Fehler, 0 Warnungen. `install.py --check` ohne Abweichung; Hauptdokument baut für beide Client Packs
- [ ] **Bewusst offen:** Die Sonden sind nicht Teil des Repositorys. Ein Wiederholungslauf folgt der Tabelle im Protokoll. Ein fester Sondenlauf wäre eine eigene Änderung – er erzeugt ein Werkzeug, das selbst gepflegt und selbst geprüft werden will
- [ ] **Bewusst offen:** Prüfung 10 (Mermaid) bleibt ungeprüft, weil `mmdc` in dieser Umgebung fehlt. Sie ist optional und nicht Teil des Standardlaufs
