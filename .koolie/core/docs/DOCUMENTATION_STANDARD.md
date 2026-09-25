# Dokumentationsstandard – Klassen, Kriterien und Prüfungen

| Attribut | Wert |
|---|---|
| ID | `FW-DOC-STANDARD` |
| Version | `0.1.0` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Entscheidungen | D-371 bis D-380 (`CR-2026-142`) |

## Zweck

Dieses Dokument legt fest, **wann ein Dokument des Frameworks in Ordnung ist**: welche Dokumente es gibt, welche Kriterien je Dokument gelten und welche davon eine Maschine prüft. Es gilt für jedes Release; `.koolie/core/checklists/11-framework-release.md` verweist darauf.

Ohne vorab festgelegte Kriterien hat eine Durchsicht kein Ende (D-370) – und ohne Prüfung ist derselbe Befund in drei Releases wieder da.

## 1. Die vier Klassen (D-371)

Jedes Markdown-Dokument des Kerns gehört genau einer Klasse an, oder es ist Nachweis. **Die Zuordnung steht an einer Stelle:** in der Funktion `dokumentklasse()` von `.koolie/core/tests/scripts/validate-framework.py`. Dieses Dokument beschreibt sie, es zählt sie nicht ein zweites Mal auf.

| Klasse | Was | Beispiele |
|---|---|---|
| **A – Einstieg** | was jemand liest, der das Framework zum ersten Mal einsetzt | Wurzel-README (nur im Framework-Repositorium), `onboarding/`, `examples/`, `pilot/`, `docs/ADOPTION_GUIDE.md`, `docs/RUNTIME_GLOSSARY.md`, `clients/README.md`, die `CLIENT_PACK.md` der Packs |
| **B – Regeln** | was gilt | Core-Module, Laufzeitschicht, Governance-Prozesse, Checklisten, Entscheidungsbäume, Prompts, Vorlagen, Skills, dieses Dokument |
| **C – Register** | Belege und Verzeichnisse | `CHANGELOG.md`, `governance/DECISION_LOG.md`, `docs/ROADMAP.md`, `tests/TEST_CATALOG.md`, `tests/EDGE_CASES.md`, `docs/PLACEHOLDER_REGISTRY.md`, `governance/ADOPTION_REGISTRY.md`, die `TESTS.md`, `EXAMPLES.md` und `CHANGELOG.md` der Skills |
| **D – Hauptdokument** | die Kapitelquellen unter `build/doc/` | `00-kopf.md` bis `32-abschluss.md` |

**Nachweis** sind Änderungsanträge, Protokolle, Erhebungen und `build/` (`clientmap.NACHWEIS_ABLAGEN`, D-367). Sie werden nicht umgeschrieben. **Einzige Ausnahme:** `build/doc/` liegt in der Nachweisschicht, weil `build/` nicht zur Nutzung gehört – und ist doch das Hauptdokument, also Klasse D.

## 2. Die Kriterien je Klasse

| Kriterium | A Einstieg | B Regeln | C Register | D Hauptdokument |
|---|---|---|---|---|
| **aktuell** | voll | voll | nur die laufenden Zeilen | voll |
| **schlüssig** | voll | voll | maschinell | voll, gegen A und B |
| **verständlich** | voll, mit Kaltleser-Probe | Stichprobe | – | voll |
| **Form** | voll | voll | voll | voll |

### 2.1 Aktuell

Keine Aussage **in Gegenwartsform** widerspricht dem Stand in `.koolie/core/VERSION`. **Datierte Aussagen** – *„gemessen am 2026-09-13“*, *„Stand Release 0.89.0“* – veralten nicht; sie müssen nur für ihr Datum stimmen (D-318). Hinweise *„🆕 neu mit x.y.z“* entfallen nach dem nächsten MINOR-Release.

**Zahlen:** Eine Zahl in Gegenwartsform wird entweder **ausgerechnet** (vom Validator verlangt wie in Prüfung 46 und 78, oder beim Bau eingesetzt wie in Kapitel 31, D-377) oder **weggelassen**. Eine von Hand gepflegte Gegenwartszahl veraltet mit dem nächsten Release.

### 2.2 Schlüssig

In sich widerspruchsfrei und nicht im Widerspruch zu einem Dokument höherer Verbindlichkeit (`governance/PRIORITY_HIERARCHY.md`). Bei einem Widerspruch gilt das Regeldokument; der Einstiegstext wird angeglichen. Findet die Durchsicht zwei Regeln, die einander widersprechen, **entscheidet sie nichts**, sondern legt einen Änderungsantrag an.

### 2.3 Verständlich (D-376)

Regeltext nennt **die geltende Regel mit Verweis auf ihren Decision Record**, nicht ihre Herleitung. Sätze wie *„Bis `1.0.0` stand hier das Gegenteil“* oder *„berichtigt mit …“* gehören in `governance/DECISION_LOG.md` und `CHANGELOG.md`. **Belegzellen bleiben:** die Einstufung `[TECHNISCH]` oder `[DOK]`, der Protokollverweis, die datierte Messung. Eine Warnung darf auffallen – gestapelte Hervorhebungen in jedem zweiten Satz tun es nicht mehr.

Für Klasse A misst das eine **Kaltleser-Probe** (D-379): Eine frische Sitzung ohne weiteren Kontext bekommt nur das Dokument und beantwortet feste Fragen; die Antworten werden gegen ein Soll gezählt. Fragen, Soll und Ergebnis stehen im Protokoll des Releases.

### 2.4 Form

- **Rechtschreibung nach dem geltenden Duden** in den Klassen A, B und D (D-373): *dass, muss, misst, lässt, Messbaum*. Register bleiben, wie sie geschrieben wurden. Code ist Zitat und bleibt.
- **Gestalt** (D-374): genau eine Hauptüberschrift, keine übersprungene Ebene, jeder Codeblock geschlossen, jede Tabellenzeile mit der Spaltenzahl ihres Kopfes.
- **Steckbrief** (D-375): Klassen A und B tragen vor dem ersten Abschnitt eine Tabelle `| Attribut | Wert |` mit Kennung, Version und Status. Ausgenommen sind README-Verzeichnisse, die Laufzeitschicht, Ausfüllvorlagen und Beispielausgaben. Wer ein Dokument ändert, hebt seine Version nach `governance/RELEASE_PROCESS.md` Abschnitt 1.
- **Zeilenenden** wie der Rest des Repositoriums (Prüfung 81).

## 3. Was eine Maschine prüft – und was nicht

| Prüfung | Gegenstand | Klassen |
|---|---|---|
| 13 | Form jedes Versionsfeldes | A, B |
| 46 | die D-11-Standzeile der Roadmap, ausgerechnet | C |
| 55 | das Statusvokabular | A, B |
| 77 | die Dokumentversion des Hauptdokuments gegen `VERSION` | D |
| 78 | der Satz über den Prüfapparat, ausgerechnet | D |
| 83, 85 | Chronikspanne und Zielangaben der Roadmap | C |
| **91** | die Standüberschrift der Roadmap gegen `VERSION` (D-372) | C |
| **92** | Rechtschreibung nach dem geltenden Duden (D-373) | A, B, D |
| **93** | Gestalt: Codeblöcke, Hauptüberschrift, Ebenen, Tabellenspalten (D-374) | A, B, C, D |
| **94** | Steckbrief mit Kennung, Version und Status (D-375) | A, B |

**Keine Maschine prüft:** ob eine Gegenwartsaussage stimmt, ob zwei Dokumente einander widersprechen, ob ein Text verständlich ist und ob er Geschichte statt Regel erzählt. Eine Prüfung auf Geschichtsmarken ist verworfen, weil ihre Muster datierte Belege genauso träfen (D-376). Diese Kriterien bleiben Durchsicht – nach Abschnitt 4.

## 4. Die Durchsicht

- **Bei jedem Release:** Wer ein Dokument ändert, hält es gegen die Kriterien seiner Klasse. Die Prüfungen 91 bis 94 laufen mit dem Validator.
- **Bei jedem MINOR-Release:** Entfallen die *„🆕 neu mit …“*-Hinweise des vorletzten MINOR-Releases.
- **Eine vollständige Durchsicht** einer Klasse ist ein eigener Posten der Roadmap mit Ziel-Release. `1.9.0` hat die Klassen A und D durchgesehen und die Roadmap gekürzt (D-378); die Klasse B folgt je Bereich (D-380).
