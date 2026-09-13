# Framework Core 05 – Sicheres Arbeitsmodell: Standardarbeitsablauf und Betriebsmodi

| Attribut | Wert |
|---|---|
| Modul-ID | FW-CORE-05 |
| Ebene | 1 – Framework Core |
| Verbindlichkeit | normativ (Abschnitte 1–3), Erläuterung (Abschnitt 4) |
| Owner | `<FRAMEWORK_OWNER>` |
| Version | 0.1.6 |

## 1. Standardarbeitsablauf (normativ)

Jede KI-Aufgabe folgt den vierzehn Schritten. Schritte DÜRFEN NICHT übersprungen werden; bei Kontrollstufe niedrig KÖNNEN die Schritte 7 bis 9 in einer einzigen kurzen Interaktion zusammengefasst werden, sofern jeder Schritt erkennbar bleibt.

| Nr. | Schritt | Verantwortung | Mindestinhalt | Referenz |
|---|---|---|---|---|
| 1 | Aufgabe verstehen | Mensch, dann KI-Client | Aufgabenziel, Erfolgskriterium, betroffener Bereich in eigenen Worten wiedergeben | `leitwerk-core/prompts/`, `leitwerk-core/checklists/01-preflight.md` |
| 2 | Scope und Grenzen bestimmen | Mensch | Erlaubte Pfade, ausgeschlossene Pfade, Betriebsmodus, Kontrollstufe (`09-risk-model.md`) | `leitwerk-core/decision-trees/02-may-ai-do-task.md`, `03-analyze-or-modify.md` |
| 3 | Datenschutz und Kontextfreigabe prüfen | Mensch | Kontextklassen aller vorgesehenen Quellen prüfen (`02-privacy.md`); K3-Inhalte ausschließen | `leitwerk-core/checklists/02-privacy-context.md`, `leitwerk-core/decision-trees/01-context-allowed.md` |
| 4 | Rückfragen und offene Punkte erfassen | KI-Client | Liste der Unklarheiten mit Auswirkung; keine Bearbeitung ungeklärter Punkte (P3) | – |
| 5 | Relevanten Ist-Zustand analysieren | KI-Client | Nur die für die Aufgabe relevanten Dateien lesen; keine Änderungen (P4) | Skill `fw-repo-analyze` |
| 6 | Befunde mit Fundstellen darstellen | KI-Client | Jede Aussage mit `pfad/datei:zeile` oder Suchmuster belegen | – |
| 7 | Lösungsoptionen bewerten | KI-Client, Entscheidung Mensch | Mindestens zwei Optionen bei Stufe mittel/hoch; Kriterien: Risiko, Aufwand, Reversibilität, Konsistenz mit Architektur | Skill `fw-change-analyze` |
| 8 | Vorgehen oder Änderungsplan vorschlagen | KI-Client | Schrittfolge, betroffene Dateien, Tests, Abbruchkriterien | Skill `fw-plan` |
| 9 | Freigabepunkt vor risikoreichen Änderungen | Mensch | Bestätigung des Plans (Stufe mittel) oder dokumentierte Freigabe `<APPROVAL_ROLE>` (Stufe hoch) | `09-risk-model.md` |
| 10 | Änderung in kleinen, nachvollziehbaren Schritten umsetzen | KI-Client unter Beobachtung | Ein logischer Schritt je Änderung; nach jedem Schritt Zwischenstand berichten (P7) | Skill `fw-change-small`, `leitwerk-core/checklists/03-before-code-change.md` |
| 11 | Tests und Qualitätsprüfungen ausführen | KI-Client, Bewertung Mensch | Nur im Overlay freigegebene Befehle (`<BUILD_COMMAND>`, `<TEST_COMMAND>`, `<LINT_COMMAND>`); Ergebnisse unverändert berichten | `leitwerk-core/checklists/05-testing.md` |
| 12 | Ergebnis, Abweichungen und Restrisiken dokumentieren | KI-Client | Ergebnisbericht nach Standardformat (Abschnitt 3.6) | – |
| 13 | Menschliche Prüfung ermöglichen | KI-Client, dann Mensch | Diff, Fundstellen, Testprotokoll, offene Punkte bereitstellen; Review anhand `leitwerk-core/checklists/04-review-ai-code.md` | Skill `fw-review-support` |
| 14 | Übernahme über den bestehenden Review- und Freigabeprozess | Mensch | Merge Request mit KI-Nutzungsvermerk; reguläre Quality Gates und Review (P5, P6) | `leitwerk-core/checklists/08-merge-request.md`, Skill `fw-mr-description` |

## 2. Betriebsmodi (normativ)

Jede Aufgabe wird genau einem Betriebsmodus zugeordnet. Ein Moduswechsel innerhalb einer Sitzung ist zulässig, MUSS aber ausdrücklich durch den Menschen angewiesen werden und wird vom KI-Client im Ergebnisbericht vermerkt.

### 2.1 Übersicht

| Modus | Kurzzweck | Schreibzugriff auf Dateien | Befehlsausführung | Zulässig bis Kontrollstufe |
|---|---|---|---|---|
| M1 Read-only Analysis | Verstehen und Befunde liefern | nein | nur lesende Analysebefehle, falls im Overlay freigegeben | hoch |
| M2 Guided Planning | Änderungsplan erarbeiten | nur Plan-Datei außerhalb des Quellcodes | wie M1 (nur lesende Analysebefehle) | hoch |
| M3 Controlled Modification | Freigegebene Änderung umsetzen | ja, innerhalb des freigegebenen Scopes | freigegebene Build-, Test- und Lint-Befehle | hoch (nur mit Freigabe und Pairing) |
| M4 Test and Validation | Tests erstellen, ausführen, Ergebnisse bewerten | ja, nur in Testverzeichnissen | freigegebene Testbefehle | hoch (ohne Produktivcode-Änderung) |
| M5 Documentation Support | Dokumentation erstellen oder aktualisieren | ja, nur in Dokumentationspfaden | nur lesende Git-Befehle (status, diff, log, show, blame) | hoch |

### 2.2 Modusbeschreibungen

#### M1 Read-only Analysis

| Aspekt | Festlegung |
|---|---|
| Zweck | Ist-Zustand verstehen, Fragen beantworten, Befunde mit Fundstellen liefern, Wissen an neue Teammitglieder vermitteln |
| Zulässige Aktionen | Dateien im freigegebenen Arbeitsbereich lesen und durchsuchen; Struktur, Abhängigkeiten und Aufrufpfade erklären; Befunde mit Pfad- und Zeilenangaben ausgeben |
| Verbotene Aktionen | Jede Datei erzeugen, ändern, verschieben oder löschen; Befehle mit Seiteneffekten ausführen; externe Quellen ohne Freigabe abrufen; ausgeschlossene Pfade lesen |
| Benötigter Kontext | Aufgabenfrage; relevante Verzeichnisse oder Dateien; Project Overlay (Kurzfassung) |
| Prüfpflichten | Mensch prüft Befunde stichprobenartig an den angegebenen Fundstellen; unbelegte Aussagen gelten als unbestätigt |
| Abbruchkriterien | Zugriff auf K3-Inhalte erforderlich; Fundstellen nicht auffindbar; Frage erfordert Informationen außerhalb des Repositorys, die nicht freigegeben sind |
| Erwartete Ausgabe | Strukturierter Analysebericht: Fragestellung, untersuchte Bereiche, Befunde mit Fundstellen, offene Punkte, ausdrückliche Kennzeichnung von Vermutungen |
| Umsetzung im Werkzeug | **Die Modusgrenze gilt normativ; technisch durchgesetzt ist sie nicht.** Kennt der KI-Client einen eigenen Nur-Lese-Modus oder ein rein lesendes Agentenprofil, ist dieser Weg vorzuziehen – welcher das ist, steht in der Fähigkeitsmatrix seines Client Packs (S3, A1) `[DOK]` je Pack. **Die Skill-`permissions` tragen sie nicht:** `allowed-tools` ist bei mindestens einem Pack keine Werkzeugbeschränkung, sondern eine Vorabfreigabe, und das Feld `permissions` kennt dieser Client für Skills nicht – gemessen am 2026-09-12 (`tests/protocols/2026-09-12-B01-allowed-tools.md`, B01) `[KONZ]`. **Seit 0.31.0 benennt jedes Pack, was an die Stelle eines so verworfenen Feldes tritt**, und die Installation bricht ab, wenn es das nicht tut (`CR-2026-050`, D-50); der Ersatz steht in der Fähigkeitsmatrix bei S3. Unabhängig vom Modus wirken die Sperren auf Secret- und Kernpfade `[DOK]` |

#### M2 Guided Planning

| Aspekt | Festlegung |
|---|---|
| Zweck | Umsetzbaren, prüfbaren Änderungsplan vor jeder Modifikation erarbeiten |
| Zulässige Aktionen | Alles aus M1; Optionen bewerten; Plan mit Schritten, betroffenen Dateien, Tests, Risiken und Abbruchkriterien erstellen; Plan-Datei außerhalb des Quellcodes schreiben |
| Verbotene Aktionen | Änderungen an Quellcode, Konfiguration, Tests oder Dokumentation; Befehle mit Seiteneffekten; Annahmen über ungeklärte Anforderungen |
| Benötigter Kontext | Aufgabenbeschreibung mit Akzeptanzkriterien; Analyseergebnis aus M1; Overlay-Regeln zu Architektur, Conventions, Definition of Done |
| Prüfpflichten | Mensch bestätigt oder verwirft den Plan schriftlich (Stufe mittel) beziehungsweise `<APPROVAL_ROLE>` gibt frei (Stufe hoch); jede Planänderung nach Freigabe erfordert erneute Bestätigung |
| Abbruchkriterien | Anforderungen widersprüchlich; Plan würde Delegationsverbotsliste berühren; Plan erfordert Kontext außerhalb der Freigabe |
| Erwartete Ausgabe | Plan nach `leitwerk-core/templates/PLAN_TEMPLATE.md`: Ziel, Annahmen (gekennzeichnet), offene Fragen, Schritte, betroffene Dateien, Teststrategie, Risiken, Rollback |
| Umsetzung im Werkzeug | **Die Beschränkung des Schreibrechts auf die Plan-Datei gilt normativ; technisch durchgesetzt ist sie nicht** – kein Mechanismus des Frameworks kennt sie `[KONZ]`. Kennt der KI-Client einen eigenen Planungsmodus mit persistenter Plan-Datei, ist dieser vorzuziehen (Fähigkeitsmatrix des Client Packs) `[DOK]` je Pack. Liegt die Plan-Datei außerhalb des Repositorys, wird sie für die Nachvollziehbarkeit in das im Overlay festgelegte Ablageformat übernommen (`<TBD: Ablage von Plänen im Projekt>`) |

#### M3 Controlled Modification

| Aspekt | Festlegung |
|---|---|
| Zweck | Eine freigegebene, klar abgegrenzte Änderung in kleinen Schritten umsetzen |
| Zulässige Aktionen | Dateien innerhalb `<ALLOWED_PATHS>` ändern; freigegebene Build-, Test- und Lint-Befehle ausführen; nach jedem Schritt Zwischenstand berichten |
| Verbotene Aktionen | Änderungen außerhalb des Scopes; Änderungen an `<EXCLUDED_PATHS>`; neue Abhängigkeiten ohne Freigabe; Git-Operationen mit Fernwirkung (push, merge, tag, rebase auf geteilten Branches); Löschen von Dateien ohne ausdrückliche Einzelfreigabe; Deaktivieren oder Löschen von Tests; Anpassen von Quality-Gate-Konfigurationen |
| Benötigter Kontext | Bestätigter Plan; betroffene Dateien; Coding Conventions; Test- und Build-Befehle aus dem Overlay |
| Prüfpflichten | Mensch beobachtet die Sitzung und bestätigt Schreib- und Ausführungsanfragen einzeln (Modus Normal); vollständiger Diff-Review vor Commit; Quality Gates |
| Abbruchkriterien | Abweichung vom Plan erforderlich; unerwartete Berührung weiterer Komponenten; fehlgeschlagene Tests ohne klare Ursache; Fund von Secrets oder personenbezogenen Echtdaten; Anstieg der Kontrollstufe |
| Erwartete Ausgabe | Änderungssatz (Diff) mit Schrittprotokoll, ausgeführten Befehlen und Ergebnissen, Abweichungen vom Plan, Restrisiken, Vorschlag für Commit-Nachricht |
| Umsetzung im Werkzeug | Rückfragender Standardmodus (Schreib- und Ausführungsanfragen werden einzeln bestätigt) `[DOK]`; Berechtigungsdatei mit Verweigerung für ausgeschlossene Pfade und Fernwirkungs-Befehle, Rückfrage für Schreiben und Ausführen `[DOK]`; ein Modus ohne Rückfragen DARF NICHT verwendet werden (D-05) `[KONZ]`; sitzungsweite Freigaben nur für die im Overlay freigegebenen Testbefehle `[EMPF]` |

#### M4 Test and Validation

| Aspekt | Festlegung |
|---|---|
| Zweck | Tests erstellen oder erweitern, Tests ausführen, Ergebnisse und Abdeckung bewerten |
| Zulässige Aktionen | Dateien in `<TEST_PATHS>` erstellen und ändern; `<TEST_COMMAND>` und `<LINT_COMMAND>` ausführen; Testergebnisse unverändert berichten; Testlücken benennen |
| Verbotene Aktionen | Produktivcode ändern, um Tests bestehen zu lassen; Tests abschwächen, ignorieren, löschen oder als erwartet fehlschlagend markieren; Testdaten mit personenbezogenen Echtdaten erzeugen; Zugriff auf externe Systeme oder Produktionsdaten |
| Benötigter Kontext | Zu testende Komponente; bestehende Tests und Testkonventionen; `<TEST_FRAMEWORK>`; Akzeptanzkriterien |
| Prüfpflichten | Mensch prüft, ob Tests das fachliche Verhalten und nicht die Implementierung zementieren; prüft synthetische Testdaten; prüft Aussagekraft fehlschlagender Tests |
| Abbruchkriterien | Test erfordert Änderung am Produktivcode (dann Wechsel nach M2/M3 durch den Menschen); Testinfrastruktur nicht verfügbar; Testdaten nur aus Echtdaten ableitbar |
| Erwartete Ausgabe | Testdateien, Testprotokoll (Befehl, Ergebnis, Dauer), Liste nicht abgedeckter Fälle, Bewertung der Aussagekraft |
| Umsetzung im Werkzeug | **Die Beschränkung auf `<TEST_PATHS>` gilt normativ; technisch durchgesetzt ist sie nicht** `[KONZ]`. Der Schutz-Hook kennt weder den Betriebsmodus noch eine Liste erlaubter Schreibpfade und entscheidet innerhalb und außerhalb des Scopes gleich – gemessen am 2026-09-12 (`leitwerk-core/tests/protocols/2026-09-12-B04-B05-gegenpruefung.md`, B05) `[DOK]` für den Befund. Die Skill-`permissions` tragen sie ebenfalls nicht (B01, siehe M1); welcher Mechanismus stattdessen trägt, steht seit 0.31.0 bei S3 des jeweiligen Packs. Getragen wird sie von der Regelschicht und der Prüfpflicht dieses Modus; unabhängig davon wirken die Sperren auf Secret- und Kernpfade `[DOK]` |

#### M5 Documentation Support

| Aspekt | Festlegung |
|---|---|
| Zweck | Technische Dokumentation aus dem tatsächlichen Code-Stand ableiten, aktualisieren und konsistent halten |
| Zulässige Aktionen | Dateien in `<DOC_PATHS>` erstellen und ändern; Code lesen; lesende Git-Befehle (status, diff, log, show, blame) für Änderungsübersichten ausführen; Abweichungen zwischen Code und Dokumentation benennen |
| Verbotene Aktionen | Quellcode ändern; Befehle mit Schreib- oder Fernwirkung; Dokumentation von nicht existierendem Verhalten erzeugen; Kundennamen, Personen, interne Adressen oder Umgebungsdetails ergänzen; Entscheidungen erfinden oder nachträglich begründen |
| Benötigter Kontext | Betroffene Dokumente; zugehöriger Code; Dokumentationskonventionen aus dem Overlay |
| Prüfpflichten | Fachliche Prüfung durch eine Person mit Domänenwissen; Prüfung auf vertrauliche Inhalte vor Ablage in `<DOCUMENTATION_PLATFORM>` |
| Abbruchkriterien | Dokumentierter Sachverhalt aus dem Code nicht belegbar; Widerspruch zwischen Code und bestehender Dokumentation, der eine fachliche Entscheidung erfordert |
| Erwartete Ausgabe | Geänderte Dokumentationsdateien, Änderungsübersicht, Liste belegter Quellen, Liste offener fachlicher Klärungen |
| Umsetzung im Werkzeug | **Die Beschränkung auf `<DOC_PATHS>` gilt normativ; technisch durchgesetzt ist sie nicht** `[KONZ]`. Eine Beschränkung auf `<DOC_PATHS>` unter Ausschluss aller übrigen Pfade ist über Skill-`permissions` nicht ausdrückbar (`<DOC_PATHS>` ist Teilmenge von `<ALLOWED_PATHS>`, und `deny` gewinnt gegen `allow`) `[DOK]`, und das Feld `permissions` kennt der eine Client für Skills ohnehin nicht (B01) – was an seine Stelle tritt, benennt seit 0.31.0 die Zeile S3 seiner Fähigkeitsmatrix. Der Schutz-Hook trägt sie nicht – er kennt den Modus nicht (`leitwerk-core/tests/protocols/2026-09-12-B04-B05-gegenpruefung.md`, B05) `[DOK]` für den Befund. Getragen wird sie von der Regelschicht und der fachlichen Prüfpflicht dieses Modus |

## 3. Querschnittsregeln für alle Modi (normativ)

### 3.1 Sitzungsdisziplin

1. Eine Sitzung bearbeitet eine Aufgabe. Neue Aufgaben MÜSSEN in neuen Sitzungen begonnen werden (Least Context, Nachvollziehbarkeit).
2. Sitzungsweite Freigaben („für diese Sitzung erlauben") SOLLEN nur für die im Overlay freigegebenen Test- und Build-Befehle erteilt werden. Projektweite oder globale Freigaben `[DOK]` DÜRFEN NICHT durch einzelne Entwicklerinnen oder Entwickler erteilt werden; sie erfordern einen Änderungsantrag an die Berechtigungsdatei.
3. Parallel laufende Agentensitzungen `[DOK]` sind an **Voraussetzungen** gebunden, nicht an eine Kontrollstufe der Aufgabe: Die Aufgaben MÜSSEN voneinander unabhängig sein, die Schreibziele disjunkt – sie DÜRFEN NICHT auf denselben Dateien arbeiten –, eine Person MUSS die Aufsicht führen, und jede Sitzung MUSS ihre eigene Aufgabe und ihren eigenen Ergebnisbericht haben. Die Einstufung dieser Arbeitsweise leistet R12 (`leitwerk-core/framework/core/09-risk-model.md`, Abschnitt 2): rein lesende Parallelarbeit unter Aufsicht niedrig, schreibende auf getrennten Zielen mittel, gemeinsame Schreibziele hoch und damit ausgeschlossen. Jede parallel bearbeitete Aufgabe bleibt an die Betriebsmodi **ihrer eigenen** Kontrollstufe gebunden (D-54).
4. Hintergrund-Subagenten DÜRFEN NICHT für Modus M3 verwendet werden. Für M1 KANN ein rein lesendes Agentenprofil genutzt werden, sofern der KI-Client eines kennt (Fähigkeitsmatrix des Client Packs, A1).

### 3.2 Befehlsausführung

1. Der KI-Client führt nur Befehle aus, die im Overlay als freigegeben gelistet sind (`<BUILD_COMMAND>`, `<TEST_COMMAND>`, `<LINT_COMMAND>`, weitere in `project-overlay/OVERLAY.md` Abschnitt 6).
2. Verboten sind in jedem Modus: Befehle mit Fernwirkung (`git push`, `git merge` auf geteilte Branches, Deployments, Paketveröffentlichung), destruktive Dateisystembefehle außerhalb des Arbeitsbereichs, Rechteausweitung (`sudo`), Installation von Software außerhalb der Projektabhängigkeiten, Netzwerkzugriffe auf nicht freigegebene Ziele.
3. Jeder ausgeführte Befehl und sein Ergebnis werden im Ergebnisbericht aufgeführt.

### 3.3 Umgang mit Fehlern

Schlägt ein Befehl oder Test fehl, MUSS der KI-Client das unveränderte Ergebnis berichten, eine Ursachenhypothese mit Fundstelle nennen und – sofern die Behebung außerhalb des bestätigten Scopes liegt – anhalten. Der KI-Client DARF NICHT eigenständig Tests anpassen, Prüfungen deaktivieren oder den Scope erweitern, um einen Fehler zu umgehen.

### 3.4 Umgang mit fehlendem Kontext

Fehlt Kontext, fragt der KI-Client gezielt nach (was fehlt, wozu es benötigt wird, welche Auswirkung das Fehlen hat) und bearbeitet nur die Teile, die ohne diesen Kontext belastbar sind. Der KI-Client DARF NICHT selbstständig auf Quellen außerhalb des freigegebenen Arbeitsbereichs zugreifen, um Kontext zu beschaffen.

### 3.5 Nachvollziehbarkeit

Jede Sitzung endet mit einem Ergebnisbericht (Abschnitt 3.6). Bei Kontrollstufe mittel und hoch wird der Bericht im Merge Request oder an der im Overlay festgelegten Stelle abgelegt (`<TBD: Ablageort für Ergebnisberichte>`).

### 3.6 Standardformat Ergebnisbericht

```markdown
## Ergebnisbericht

- Aufgabe: <Ticket-Referenz oder Kurzbeschreibung>
- Betriebsmodus: <M1–M5>  |  Kontrollstufe: <niedrig|mittel|hoch> (auslösender Faktor: <R#>)
- Verwendete Skills: <Skill-IDs und Versionen>
- Verwendeter Kontext: <Dateien/Verzeichnisse/Dokumente, jeweils mit Kontextklasse>

### Befunde und Änderungen
<Liste mit Fundstellen `pfad/datei:zeile`>

### Ausgeführte Befehle und Ergebnisse
<Befehl → Ergebnis (unverändert)>

### Abweichungen vom Plan
<keine | Liste mit Begründung>

### Annahmen (gekennzeichnet) und offene Fragen
<Liste>

### Restrisiken und empfohlene Prüfungen
<Liste>
```

## 4. Hinweise zur Anwendung (Erläuterung)

Der Ablauf wirkt umfangreich, ist in der Praxis aber vor allem eine Reihenfolge: erst verstehen, dann eingrenzen, dann prüfen, dann planen, dann ändern, dann testen, dann dokumentieren, dann prüfen lassen. Bei Kontrollstufe niedrig dauert der Vorlauf (Schritte 1–4) meist nur wenige Minuten. Der Aufwand verlagert sich vom Schreiben des Codes zum Abgrenzen der Aufgabe und zum Prüfen des Ergebnisses – genau dort, wo menschliche Verantwortung liegt.
