# Änderungsantrag `CR-2026-088`

| Feld | Inhalt |
|---|---|
| Titel | Die Vorbedingungen der dreizehn Testblätter durchgegangen – 21 von 81 Zellen tragen nicht, und das Overlay bindet seine Pflichtplatzhalter nicht |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-18 |
| Betroffene Artefakte | `tests/scripts/validate-framework.py` (**Prüfung 55 und 56**, Kopfkommentar), `tests/scripts/probe-pruefungen.py` (vier Sonden, fünf Gegenproben), `templates/project-overlay/OVERLAY.md` (`<CHANGE_SIZE_THRESHOLD>`), dreizehn `TESTS.md` (21 Zellen mit Vermerk), `tests/TEST_CATALOG.md` (Sondenmenge), `governance/DECISION_LOG.md` (D-160 bis D-162, `K-66`, `K-67`), `docs/ROADMAP.md`, `tests/protocols/2026-09-18-vorbedingungen-testblaetter.md`, `CHANGELOG.md`, `VERSION`; **außerhalb des Repositoriums:** das Übungs-Overlay (acht Bindungen, eingeengte Sperre) |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind der Prüfapparat, die Overlay-Vorlage und dreizehn Testblätter |
| Art | Erhebung, Befundbehebung, zwei neue Prüfungen |
| Dringlichkeit | **Regulär, mit einem Vorbehalt:** In der geladenen Laufzeitschicht des Übungsrepositoriums standen 65 Fundstellen von Pflichtplatzhaltern, die kein Leser auflösen kann – darunter Regeln, die eine Meldung an eine nicht benannte Stelle verlangen |

## 1. Anlass

Der Releaseplan sah für 0.63.0 den fünften Sitzungstest vor. **Vor dem ersten Lauf sind
die Vorbedingungen durchgegangen worden** – zum siebten Mal in Folge, und zum siebten Mal
war es der billigste Befund des Releases. Diesmal galt der Durchgang nicht zehn Zellen
einer Klasse, sondern **allen 81 offenen Zellen der dreizehn Testblätter**: dem Posten,
der 88 % des Restbestands von Kriterium 2 ausmacht.

## 2. Die Trennlinie, die vorher niemand gezogen hatte (D-162)

Eine Vorbedingung beschreibt entweder **einen Eingabetext**, den der Lauf selbst
mitbringt (Stacktrace, Aufgabenbeschreibung, Fehlerbericht) – oder **einen Zustand des
Repositoriums**, der vorher da sein muss. Nur die zweite Gattung braucht eine
registrierte Präparation.

**Die Zahl verändert sich dadurch in beide Richtungen.** `K-42` zählte 82 von 83
Blattzellen als *ohne Präparation*; gemessen sind **25 von 81** gar kein
Repositoriumszustand. Die echte Lücke ist kleiner und schärfer.

| Klasse | Bedeutung | Zellen |
|---|---|---|
| A | Gegenstand ist der Eingabetext des Laufs | 25 |
| B | registrierte Präparation, vorhanden | 3 |
| C | Zustand des Repositoriums, gemessen vorhanden | 17 |
| D | je Lauf herzustellen, in keinem Register | 15 |
| **E** | **Gegenstand fehlt oder widerspricht dem Overlay** | **21** |

## 3. Der erste Befund: 21 Zellen ohne Gegenstand

🔴 **`fw-docs-update` ist vollständig unfahrbar – sechs von sechs.** Alle Zellen
verlangen ein Übungsdokument in `<DOC_PATHS>`; `docs/` enthält **genau eine Datei**, und
das ist das Aufgabenblatt mit den Auflösungen.

Dazu: keine Test-Fixture mit K3-Inhalt (3 Zellen), keine Berechtigungsprüfung im
Übungscode (2), keine dokumentierten Akzeptanzkriterien (1 – der Begriff kommt im ganzen
Übungsrepositorium kein einziges Mal vor), kein Glossar (1), keine zwei gleichnamigen
Module (1), kein Duplikat **innerhalb einer Datei** (1), und zwei Duplikate, die sich in
einer Randbedingung **unterscheiden** (1) – `UEB-03` trägt absichtlich **dieselbe**
falsche Grenze an beiden Stellen, weil das die Scope-Falle ausmacht.

**Alle 21 standen als `offen`, also als fahrbar.** Seit diesem Release sagen sie es in
ihrer eigenen Zeile.

## 4. Der zweite Befund, und er ist größer: das Overlay bindet nicht, es ersetzt (D-160)

🔴 **Acht von neunundzwanzig Pflichtplatzhaltern waren im aktiven Übungs-Overlay
ungebunden.** Das Overlay hatte ihre Werte in den Text gesetzt – `| Tickets aus GitHub
Issues |` statt `| Tickets aus <ISSUE_TRACKER> |` – und den Platzhalter damit verloren.

**Für das Overlay selbst ist das folgenlos; für jeden Kerntext, der denselben
Platzhalter trägt, nicht.** In der geladenen Laufzeitschicht standen **65 Fundstellen**
von fünf Pflichtplatzhaltern, die kein Leser auflösen kann – `<ISSUE_TRACKER>` allein in
**vierzehn Trägern**, `<PROJECT_RULES_PATH>` in elf. Darunter Regeln wie *„Aus
`<ISSUE_TRACKER>` nur Titel, technische Beschreibung und Akzeptanzkriterien verwenden"*.

**Der Validator meldete 0 Fehler, 0 Warnungen.**

🔴 **Und die Vorlage selbst hatte eine Lücke:** `<CHANGE_SIZE_THRESHOLD>` ist Pflicht vor
der Aktivierung und kam in der Overlay-Vorlage **überhaupt nicht** vor. Ein Projekt, das
die Vorlage ausfüllt, begegnete ihm nie. **Prüfung 55 hat das beim ersten Lauf gemeldet.**

## 5. Der dritte Befund – und er hat sich beim Gegenprüfen umgedreht (D-161)

`SK-012-P01` verlangt `<MR_TEMPLATE_PATH>`, und das Übungs-Overlay sperrte den Wert über
`.github/**`. **Der erste Verdacht war, die Zelle sei falsch.** Gegen den Träger
gehalten ist es umgekehrt: `fw-mr-description` führt `<MR_TEMPLATE_PATH>` ausdrücklich
als **zulässige Kontextquelle** und verlangt in seiner Abschlussprüfung, die Vorlage in
Struktur und Pflichtfeldern einzuhalten.

**Ein Skill, der eine Datei lesen muss, und ein Overlay, das sie sperrt – das Overlay ist
die falsche Stelle.** Die Sperre ist auf `.github/workflows/**` eingeengt: ihren eigenen
Gegenstand laut Overlay, die Steuerung des Quality Gates. Übungsaufgabe E bleibt
unberührt.

## 6. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | **Wie wird eine Vorbedingung eingestuft?** | **Danach, WER ihren Gegenstand herstellt** – Eingabetext des Laufs oder Repositorium (D-162) | **Die Einstufung liest Prosa und ist Ermessen.** Deshalb steht die **Aufzählung** im Protokoll und die Zahl daneben. Ohne die Trennlinie zählte `K-42` 82 von 83 und war damit zu pessimistisch |
| **E2** | **Werden die 21 Gegenstände in diesem Release hergestellt?** | **Nein – eigener Posten `0.64.0`** (`K-66`) | **Sieben Gegenstände in einem Zug zu erfinden ist die Bauform, gegen die D-156 entschieden hat.** Jeder braucht einen eigenen Entwurf und eine registrierte Präparation. **Preis der Vertagung:** Die 21 Zellen bleiben unfahrbar – aber sie sagen es jetzt |
| **E3** | **Bekommt der Platzhalterbefund eine Prüfung?** | **Ja, Prüfung 55 mit zwei Gegenständen:** (a) die Vorlage bietet jeden Pflichtplatzhalter an, (b) das aktive Overlay bindet jeden, den ein Träger der geladenen Schicht nennt | **(b) prüft, ob der Name VORKOMMT, nicht ob der Wert daneben richtig ist.** Die Vorlage kennt drei Bindungsformen; eine verbindliche zu erzwingen hieße, jede bestehende Overlay-Datei umzubauen (`K-67`) |
| **E4** | **Und der Widerspruch um die MR-Vorlage?** | **Prüfung 56**, und **das Overlay** wird berichtigt, nicht die Zelle | **Verworfen: die Sperre ganz zu streichen** – Übungsaufgabe E hängt an ihr. 🔴 **Die Prüfung hat in EINEM Release zweimal zu breit gemeldet:** erst bei drei Zellen, die `<EXCLUDED_PATHS>` selbst zum Gegenstand haben, dann beim Vergleich von Pfad**anfängen** statt Pfaden. Beide Zuschnitte sind jetzt durch eine Gegenprobe belegt |
| **E5** | **Wie wird das Release geschnitten?** | **`0.63.0`, Sitzungstest 5 rückt auf `0.64.0`**, die Herrichtung wird `0.65.0` | **Die exakten Nummern verschieben sich zum vierten Mal in vier Releases.** Dieselbe Entscheidung wie `CR-2026-087` E9. Prüfung 53 rechnet die Kette nach |

## 7. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle fünf Fragen wie vorgelegt.** |
| Datum | 2026-09-18 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | **D-160** (Overlay bindet statt zu ersetzen; Prüfung 55), **D-161** (keine Vorbedingung verlangt einen gesperrten Träger; Prüfung 56), **D-162** (die Trennlinie Eingabetext ↔ Repositoriumszustand) |
| Neue Klärungspunkte | `K-66` (21 Zellen ohne Gegenstand – Herrichtung als eigener Posten), `K-67` (die Vorlage kennt drei Bindungsformen) |
| Auflagen | **Wer eine Vorbedingung liest, fragt zuerst, WER ihren Gegenstand herstellt.** Und: **Ein Overlay, das einen Platzhalter durch seinen Wert ersetzt, lässt jeden Kerntext unauflösbar, der ihn trägt** |
| Ziel-Release | `0.63.0` |
| Umsetzung | umgesetzt mit `0.63.0` |

## 8. Abnahme

- Validator `0 Fehler, 0 Warnungen`, **beide Kodierungsumgebungen**.
- Sondenlauf: **vier neue Sonden** (`55a` bis `55c`, `56a`) und **fünf neue Gegenproben**
  (`55a` bis `55c`, `56a`, `56b`); Spanne `6, 14 und 18 bis 56` in allen drei Trägern
  **ausgerechnet**.
- 🔴 **Zwei Sonden maßen zuerst nichts, und beide Male war die Sonde schuld, nicht die
  Prüfung:** `55b` ersetzte `| ja |` und ließ die eine Registerzeile stehen, die
  `ja (oder „keine")` trägt; `55c` ließ den Platzhalter in der Prosa der Vorlage stehen
  und machte ihn damit „gebunden". **Der Baumhash-Wächter hat beide gemeldet, statt sie
  leise bestehen zu lassen.**
- **Die wichtigeren Hälften sind die Gegenproben:** `55b` (ein Platzhalter, den das
  Register nicht im Overlay verortet, muss in der Vorlage nicht stehen), `55c` (ein
  Overlay, das bindet, bleibt unbeanstandet) und `56b` (dieselbe Pfadwurzel, ein anderer
  Pfad – `deploy/pull_request_template.md` gegen `deploy/gen/**` – bleibt zulässig).
- **Prüfung 50 hat gegriffen:** `K-66` stand in acht Trägern, bevor es im Register stand.
- **Prüfung 55 hat beim ersten Lauf gegen den eigenen Bestand gemeldet**
  (`<CHANGE_SIZE_THRESHOLD>` fehlt in der Vorlage).
