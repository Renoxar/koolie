# Änderungsantrag `CR-2026-142`

| Feld | Inhalt |
|---|---|
| Titel | Der Dokumentationsstandard – und die Roadmap, die zu zwei Dritteln Rückblick war |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-25 |
| Betroffene Artefakte | `docs/DOCUMENTATION_STANDARD.md` (neu); `tests/scripts/validate-framework.py` (**Prüfungen 91 bis 94**, `dokumentklasse()`, Ausnahme von Prüfung 75); `tests/scripts/probe-pruefungen.py` (Bündel `sonden_roadmapstand`, `sonden_rechtschreibung`, `sonden_dokumentform`, `sonden_steckbrief`); `build/assemble.py` (Direktiven `{{ZAHL:…}}`, `{{VERSION}}`, `{{CLIENT}}`); `docs/ROADMAP.md` (Kürzung, `1.9.0`, Planabschnitt `1.9.1`); die Dokumente der Klassen A und D (Durchsicht); 14 Dokumente der Klassen A, B, D (Rechtschreibung); `OWNERS.md`, `onboarding/QUICKSTART.md`, `onboarding/REFERENCE.md`, `onboarding/exercises/EXERCISES.md`, `framework/overlay-patterns/general.md` (Steckbrief); `framework/runtime/agents/fw-reviewer.md` (Überschriften); `checklists/11-framework-release.md`; `tests/TEST_CATALOG.md`; `governance/DECISION_LOG.md` (**D-371** bis **D-380**); `governance/ADOPTION_REGISTRY.md`; `VERSION`, `CHANGELOG.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Dokumentation, Prüfapparat, Bauwerkzeug |
| Art | **MINOR** nach `RELEASE_PROCESS.md` Abschnitt 1: vier neue Prüfungen, ein neues Regeldokument, eine neue Bauform des Hauptdokuments; keine Regel des Arbeitsmodells geändert, kein Overlay-Feld |
| Dringlichkeit | Posten `1.9.0` nach D-370 |
| Status | 🟢 **entschieden am 2026-09-25** (E1 bis E12), umgesetzt mit `1.9.0` |

---

## 1. Anlass

D-370 hat nach `1.8.0` ein Qualitätssicherungsrelease der Dokumentation eingeplant: alle
Dokumente auf Aktualität, Schlüssigkeit, Verständlichkeit und Form. Seine Vorbedingung war,
**vor** der Durchsicht festzulegen, welche Dokumente es gibt, was je Dokument „in Ordnung“
heißt und was davon eine Maschine prüfen kann.

## 2. Der Vorbedingungsdurchgang

Gemessen am 2026-09-25 am Stand `v1.8.0`.

| Messung | Ergebnis |
|---|---|
| Bestand | 559 versionierte Dateien, davon 352 Nachweisschicht; **181 Markdown-Dokumente außerhalb (3,2 MB)**, dazu **34 Kapitelquellen unter `build/doc/`** – die liegen in der Nachweisschicht und sind doch das Hauptdokument |
| Größte Träger | `DECISION_LOG` 745 KB, `CHANGELOG` 729 KB, `ROADMAP` 337 KB – davon rund 200 KB Rückblicke *„Was 0.x gebracht hat“* |
| Rechtschreibung | **603** Wörter in der Schreibung vor 1996 gegen **1.192** geltende; **19 Dokumente mischen beide**. Außerhalb der Register: 74 in 14 Dokumenten |
| Geschichte im Regeltext | 316 Marken (*„stand hier“*, *„bis `x.y.z`“*, *„berichtigt mit“*), davon 180 im Decision Log |
| Steckbrief | 99 von 215 Dokumenten; nach begründeten Ausnahmen fehlten fünf |
| Form | bis auf eine Datei sauber (`fw-reviewer.md`: drei Hauptüberschriften) |
| Kapitel 31 | *„502 Dateien, 123 Anträge“*, gezählt zu `0.89.0`; *„78 Dateien, bei beiden Client Packs“* bei drei Packs |

## 3. Vorlage zur Entscheidung

Vorgelegt am 2026-09-25 als Fragen (a) bis (l), angenommen mit *„Passt, fahre so fort“*.

| # | Frage | Entscheidung und Preis |
|---|---|---|
| **E1** | **Gegenstand** (a) | Alle 181 Dokumente und die 34 Kapitelquellen; die Ausnahme der Nachweisschicht gilt für Anträge, Protokolle, Erhebungen – nicht für `build/doc/` (D-371) |
| **E2** | **Tiefe je Dokument** (b) | Vier Klassen A Einstieg, B Regeln, C Register, D Hauptdokument, mit Kriterien je Klasse; die Zuordnung an einer Stelle, `dokumentklasse()` (D-371) |
| **E3** | **Register** (c) | Werden nicht umgeschrieben – weder Inhalt noch Rechtschreibung; nur Form und laufende Zeilen (D-371) |
| **E4** | **„Aktuell“** (d) | Keine Gegenwartsaussage widerspricht `VERSION`; datierte Aussagen bleiben (D-318); *„🆕 neu mit …“* entfällt nach dem nächsten MINOR (D-371, D-376) |
| **E5** | **Geschichte im Regeltext** (e) | Regel mit Verweis statt Herleitung; Belegzellen bleiben (D-376) |
| **E6** | **Rechtschreibung** (f) | Geltender Duden in A, B, D (D-373) |
| **E7** | **„Verständlich“ messbar** (g) | Kaltleser-Probe für Klasse A (D-379) |
| **E8** | **Neue Prüfungen** (h) | 91 Standüberschrift, 92 Rechtschreibung, 93 Form, 94 Steckbrief (D-372 bis D-375) |
| **E9** | **Keine Prüfung** (i) | Geschichtsmarken und Schlüssigkeit bleiben Durchsicht (D-376) |
| **E10** | **Zahlen in Kapitel 31** (j) | Beim Bau erzeugt, nicht geprüft (D-377) |
| **E11** | **Roadmap-Rückblicke** (k) | Gekürzt, nach Messung der Kennungen (D-378) |
| **E12** | **Zuschnitt** (l) | `1.9.0`: Kriterien, Prüfungen, Klassen A und D, Rechtschreibung, Roadmap; Klasse B als `1.9.1` ff.; Status `pilot` bleibt – eine Anhebung ist Freigabe (D-380) |

> **Empfehlung der Vorbereitung:** E1 bis E12 wie vorgelegt.

---

## 4. Umsetzung

1. Validator: `dokumentklasse()`, `_dokumente()`, **Prüfungen 91 bis 94**, Register und
   Sondenmenge bis 94; die Ausnahme `docs/ROADMAP.md` in `P75_AUSNAHMEN` entfernt (sie nahm
   nach der Kürzung nichts mehr aus).
2. Sonden: vier Bündel mit je einer Gegenprobe, die den erlaubten Nachbarfall trägt – Zitat
   und Register (92b), die Wurzel eines Projekts (92c), Striche und Rauten im Code (93b),
   die Ausnahmen des Steckbriefs (94a).
3. Rechtschreibung: 74 Fundstellen in 14 Dokumenten umgestellt, mit derselben Stammliste,
   die prüft; nur außerhalb von Code.
4. Form und Steckbrief: `fw-reviewer.md` auf Ebene 2; fünf Steckbriefe nachgetragen.
5. `assemble.py`: Direktiven `{{ZAHL:…}}`, `{{VERSION}}`, `{{CLIENT}}`; Kapitel 31.1 darauf
   umgestellt.
6. Roadmap: Rückblicke vor `1.0.0` gestrichen, *„Bewusst offen gelassen“* berichtigt,
   `1.9.0` eingetragen, Planabschnitt `1.9.1` für die Klasse B.
7. Durchsicht der Klassen A und D (Regel mit Verweis statt Herleitung, veraltete Aussagen
   berichtigt); Kaltleser-Probe.
8. `docs/DOCUMENTATION_STANDARD.md`, Checkliste 11, Decision Log, Testkatalog,
   Bestandsliste, `VERSION`, Changelog.
9. Beide Projekte mit `--target --update` heben.

## 5. Abnahme

Steht im Protokoll `tests/protocols/2026-09-25-dokumentationsstandard.md`.

## 6. Entscheidung

**E1 bis E12 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-25; (a) bis (l) vor
dem Bau vorgelegt und angenommen – der Owner hat vorab erklärt, den Empfehlungen der
Vorbereitung zu folgen). Decision Records **D-371** bis **D-380**. Alle vier zählbaren
Kriterien von D-11 bleiben **0**.
