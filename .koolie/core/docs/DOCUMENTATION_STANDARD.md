# Dokumentationsstandard – Klassen, Kriterien, Schreibregeln und Prüfungen

| Attribut | Wert |
|---|---|
| ID | `FW-DOC-STANDARD` |
| Version | `0.3.2` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |

## Zweck

Dieses Dokument legt fest, wann ein Dokument von Koolie in Ordnung ist: welche Arten von Dokumenten es gibt, welche Kriterien für sie gelten, wie sie geschrieben werden und was davon eine Maschine prüft. Es gilt für jedes Release; die Release-Checkliste `.koolie/core/checklists/11-framework-release.md` verweist darauf.

## 1. Die vier Klassen

Jedes Markdown-Dokument des Kerns gehört genau einer Klasse an, oder es ist Nachweis. Die Zuordnung steht an einer einzigen Stelle: in der Funktion `dokumentklasse()` von `.koolie/core/tests/scripts/validate-framework.py`.

| Klasse | Was | Beispiele |
|---|---|---|
| **A – Einstieg** | was jemand liest, der Koolie zum ersten Mal einsetzt | `README.md`, `QUICKSTART.md` und ihre englischen Fassungen (nur im Framework-Repositorium), `onboarding/`, `examples/`, `pilot/`, `docs/ADOPTION_GUIDE.md`, `docs/RUNTIME_GLOSSARY.md`, `clients/README.md`, die `CLIENT_PACK.md` der Packs |
| **B – Regeln** | was gilt | Core-Module, Laufzeitschicht, Governance-Prozesse, Checklisten, Entscheidungsbäume, Prompts, Vorlagen, Skills, dieses Dokument |
| **C – Register** | Belege und Verzeichnisse | `CHANGELOG.md`, `governance/DECISION_LOG.md`, `docs/ROADMAP.md`, `tests/TEST_CATALOG.md`, `tests/EDGE_CASES.md`, `docs/PLACEHOLDER_REGISTRY.md`, `governance/ADOPTION_REGISTRY.md`, die `TESTS.md`, `EXAMPLES.md` und `CHANGELOG.md` der Skills |
| **D – Hauptdokument** | die Kapitelquellen unter `build/doc/` | `00-kopf.md` bis `32-abschluss.md` |

**Nachweis** sind Änderungsanträge, Protokolle, Erhebungen und `build/`. Sie werden nicht umgeschrieben. Ausnahme: `build/doc/` liegt zwar unter `build/`, ist aber das Hauptdokument und damit Klasse D.

## 2. Die Kriterien je Klasse

| Kriterium | A Einstieg | B Regeln | C Register | D Hauptdokument |
|---|---|---|---|---|
| **aktuell** | voll | voll | nur die laufenden Zeilen | voll |
| **schlüssig** | voll | voll | maschinell | voll, gegen A und B |
| **verständlich** | voll, mit Kaltleser-Probe | Stichprobe | – | voll |
| **Form** | voll | voll | voll | voll |

### 2.1 Aktuell

Keine Aussage in Gegenwartsform widerspricht dem Stand in `.koolie/core/VERSION`. Datierte Aussagen wie *„gemessen am 2026-09-13“* veralten nicht; sie müssen nur für ihr Datum stimmen. Hinweise *„🆕 neu mit x.y.z“* entfallen nach dem nächsten MINOR-Release.

Eine Zahl in Gegenwartsform wird entweder ausgerechnet – vom Validator verlangt oder beim Bau eingesetzt – oder weggelassen. Eine von Hand gepflegte Gegenwartszahl veraltet mit dem nächsten Release.

### 2.2 Schlüssig

Ein Dokument widerspricht weder sich selbst noch einem Dokument höherer Verbindlichkeit (`governance/PRIORITY_HIERARCHY.md`). Bei einem Widerspruch gilt das Regeldokument, und der Einstiegstext wird angeglichen. Findet die Durchsicht zwei Regeln, die einander widersprechen, entscheidet sie nichts, sondern legt einen Änderungsantrag an.

### 2.3 Verständlich

Wie ein verständlicher Text aussieht, regelt Abschnitt 3. Für Klasse A misst das zusätzlich eine **Kaltleser-Probe**: Eine frische Sitzung ohne weiteren Kontext bekommt nur das Dokument und beantwortet feste Fragen; die Antworten werden gegen ein Soll gezählt. Fragen, Soll und Ergebnis stehen im Protokoll des Releases.

### 2.4 Form

- **Rechtschreibung nach dem geltenden Duden** in den Klassen A, B und D: *dass, muss, misst, lässt*. Register bleiben, wie sie geschrieben wurden. Code ist Zitat und bleibt.
- **Gestalt:** genau eine Hauptüberschrift, keine übersprungene Ebene, jeder Codeblock geschlossen, jede Tabellenzeile mit der Spaltenzahl ihres Kopfes.
- **Steckbrief:** Klassen A und B tragen vor dem ersten Abschnitt eine Tabelle `| Attribut | Wert |` mit Kennung, Version und Status. Ausgenommen sind README-Verzeichnisse, die Laufzeitschicht, Ausfüllvorlagen und Beispielausgaben. Wer ein Dokument ändert, erhöht seine Version nach `governance/RELEASE_PROCESS.md` Abschnitt 1.
- **Zeilenenden** wie der Rest des Repositoriums.

## 3. Schreibregeln

Die Produktdokumentation spricht zu Menschen, die Koolie einsetzen. Die Nachweisschicht spricht zu denen, die nachvollziehen wollen, warum etwas so ist. Beides bleibt getrennt.

- **Keine Kennungen.** `CR-`, `D-` und `K-`-Kennungen stehen in der Nachweisschicht: Decision Log, Änderungsanträge, `CHANGELOG`, Roadmap, Protokolle, Erhebungen. In der Produktdokumentation stehen sie nur dort, wo das Dokument selbst Beleg ist – in den Ergebnis- und Belegspalten der Testblätter und der Grenzfälle, in der Belegspalte der Fähigkeitsmatrix, in den Zeilen eines Versionsverlaufs und in drei Kapiteln des Hauptdokuments: Grenzen und offene Entscheidungen, Anhänge, Abschluss.
- **Keine Entscheidungsgeschichte.** Was vorher galt, was verworfen wurde und welcher Lauf etwas gezeigt hat, gehört in den Decision Log. Die Produktdokumentation sagt, was gilt und was zu tun ist.
- **Erst die Sache, dann der Grund.** Ein Satz sagt die Regel oder den Schritt; eine Begründung folgt nur, wenn ohne sie ein Fehler naheliegt – in einem Satz.
- **Kurz.** Ein Gedanke je Satz. Keine Vorankündigung („Im Folgenden …“), keine Wiederholung dessen, was gerade gesagt wurde, kein Fülltext.
- **Sparsam hervorheben.** Fett für das Wort, auf das es ankommt; ein Warnzeichen nur für eine echte Gefahr. Ein Absatz trägt höchstens eine Hervorhebung.
- **Zeigen statt beschreiben.** Ein Befehl, eine Dateizeile oder eine Ausgabe ersetzt einen Absatz Beschreibung.
- **Anweisungstexte bleiben, wie sie gemessen sind.** Die Anweisungen in Skills und Laufzeitregeln sind gegen ihre Testblätter gemessen. Wer einen Satz darin ändert, öffnet die Zellen des Testblatts, und sie werden nachgemessen. Ein Verweis darf ohne Nachmessung fallen, solange kein Satz sich ändert.

## 4. Was eine Maschine prüft – und was nicht

| Prüfung | Gegenstand | Klassen |
|---|---|---|
| 13 | Form jedes Versionsfeldes | A, B |
| 46 | die Standzeile der Roadmap, ausgerechnet | C |
| 55 | das Statusvokabular | A, B |
| 77 | die Dokumentversion des Hauptdokuments gegen `VERSION` | D |
| 78 | der Satz über den Prüfapparat, ausgerechnet | D |
| 83, 85 | Chronikspanne und Zielangaben der Roadmap | C |
| 91 | die Standüberschrift der Roadmap gegen `VERSION` | C |
| 92 | Rechtschreibung nach dem geltenden Duden | A, B, D |
| 93 | Gestalt: Codeblöcke, Hauptüberschrift, Ebenen, Tabellenspalten | A, B, C, D |
| 94 | Steckbrief mit Kennung, Version und Status | A, B |
| 113 | keine Kennung außerhalb der Nachweisschicht | A, B, C |

Keine Maschine prüft, ob eine Gegenwartsaussage stimmt, ob zwei Dokumente einander widersprechen, ob ein Text verständlich ist und ob er Geschichte statt Regel erzählt. Muster für Geschichte träfen datierte Belege genauso. Diese Kriterien bleiben Sache der Durchsicht.

## 5. Die Durchsicht

- **Bei jedem Release:** Wer ein Dokument ändert, hält es gegen die Kriterien seiner Klasse und gegen die Schreibregeln. Die Prüfungen laufen mit dem Validator.
- **Bei jedem MINOR-Release:** Die Hinweise *„🆕 neu mit …“* des vorletzten MINOR-Releases entfallen.
- **Eine vollständige Durchsicht** einer Klasse ist ein eigener Posten der Roadmap mit Ziel-Release.

## 6. Sprachen

Deutsch ist die maßgebliche Sprache der gesamten Dokumentation. Englisch gibt es nur für den Einstieg: `README.en.md` und `QUICKSTART.en.md` in der Wurzel des Framework-Repositoriums.

- **Beide Fassungen verweisen aufeinander**, und die englische nennt die deutsche maßgeblich. Ein Verweis aus einer englischen Fassung auf ein deutsches Dokument trägt den Zusatz *(German)*.
- **Eine englische Fassung sagt nicht mehr zu als die deutsche.** Sie darf kürzen, aber keine Fähigkeit, keinen Reifegrad und kein Ergebnis nennen, das die deutsche nicht trägt.
- **Wer `README.md` oder `QUICKSTART.md` ändert, zieht im selben Release die englische Fassung nach** oder hält im Änderungsantrag fest, warum nicht. Keine Maschine prüft, ob sich die Fassungen decken.
