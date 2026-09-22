# Änderungsantrag `CR-2026-022`

| Feld | Inhalt |
|---|---|
| Titel | Prüfung 13 sagte mehr zu, als sie prüfte – die Versionsfelder der Kernartefakte |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | `tests/scripts/validate-framework.py` (Prüfung 13 erweitert) |
| Ebene laut Entscheidungsbaum 6 | Prüfung; keine Regeländerung |
| Art | Behebung einer Blindstelle; Folgearbeit zu `CR-2026-020` |
| Dringlichkeit | regulär |

## 1. Anlass und Problem

Der Kopfkommentar des Validators sagte zu Prüfung 13 seit 0.13.0 zu: „Versionsfelder in der
Form `MAJOR.MINOR.PATCH`". Tatsächlich deckte sie drei Dinge ab – die Overlay-Version an ihren
drei Ablageorten, `<CORE_DIR>/VERSION` und die Steckbriefangabe zur kompatiblen
Framework-Version. **Die Versionsfelder der rund sechzig Kernartefakte prüfte sie nicht.**

Belegt durch die Regressionsprobe R1 zu `CR-2026-020`: `| Version | 0.1 |` und
`| Version | abc |` in `checklists/01-preflight.md` liefen beide mit **0 Fehlern** durch.

**Der Zeitpunkt des Fundes ist der eigentliche Punkt.** Er fiel an, während `CR-2026-020`
**62 Versionsfelder von Hand um eine PATCH-Stelle hob** – ohne dass irgendetwas geprüft hätte,
ob das Ergebnis gültig ist. Ein Tippfehler in einem der 62 wäre unbemerkt geblieben, in genau
dem Release, das die Versionspflege zum Thema hatte.

Derselbe Befundtyp wie `FW-KO-01` (eine grüne Prüfung, die sechs von 22 Defekten durchließ) und
`AP2-CC-13` (ein Hook, dessen Anwesenheit geprüft war, nie seine Wirkung): **eine Prüfung, die
mehr zusagt, als sie leistet.** Das Muster ist inzwischen das häufigste im Fehlerbild dieses
Frameworks.

## 2. Vorgeschlagene Änderung

Prüfung 13 erfasst zusätzlich das Versionsfeld **jedes Kernartefakts** und prüft es gegen
`MAJOR.MINOR.PATCH`. Ausgenommen bleiben:

- **Historische Dokumente** – dieselbe Abgrenzung, die Prüfung 14 seit D-28 verwendet
  (`CHANGELOG.md` überall, `change-requests/`, `DECISION_LOG.md`, `tests/protocols/`).
- **Client Packs** – sie führen eigene Versionsangaben mit eigener Bedeutung.
- **Nicht ausgefüllte Vorlagen** (`<TBD: …>`) – eine Vorlage erklärt noch nichts.

Erkannt wird die **Steckbriefzeile**, also genau zwei Spalten. Die Verankerung auf das
Zeilenende ist notwendig: Der Änderungsverlauf eines Overlays beginnt mit der Kopfzeile
`| Version | Datum | Änderung | … |`, und die ist kein Steckbrief. Ohne die Verankerung meldete
die erste Fassung genau dort einen Fehlalarm.

## 3. Was dieser Antrag nicht ändert

- **Keine neue Entscheidung.** D-25 steht bereits: Ein Versionsfeld wird auf Stimmigkeit
  geprüft, nicht auf Anwesenheit. Dieser Antrag löst die Zusage ein, er stellt sie nicht auf.
- **Keine Prüfung, ob eine Version sich bewegt hat.** Das war der tragende Befund von
  `FW-VN-01` – alle 13 Skills standen unverändert auf `0.1.0`, obwohl alle 13 geändert worden
  waren. Diese Frage braucht die Versionsgeschichte, nicht die Datei; ein Validator, der `git`
  voraussetzt, prüfte etwas anderes als die Struktur. Sie bleibt beim Release-Prozess
  (`checklists/11-framework-release.md`).
- **Kein Artefakt wird geändert.** Alle Versionsfelder des aktuellen Stands sind gültig.

## 4. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Auch prüfen, ob die Version sich bei einer Änderung bewegt hat? | **Nein**, siehe 3. Der Validator prüft Struktur, nicht Historie | Der tragende Befund aus `FW-VN-01` bleibt außerhalb der Reichweite jeder Prüfung und hängt weiter am Release-Prozess |
| E2 | Fehler oder Warnung? | **Fehler** – konsistent mit den übrigen Teilen von Prüfung 13, die Semantic Versioning ebenfalls als Fehler führen | Ein Artefakt mit unsauberem Versionsfeld blockiert das Release. Das ist die Aussage |

## 5. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | `<TBD: angenommen / abgelehnt / mit Auflagen>` |
| Datum | `<TBD>` |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | `<TBD: E1 und E2 einzeln entscheiden>` |
