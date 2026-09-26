# Framework Core 05 – Sicheres Arbeitsmodell: Standardarbeitsablauf und Betriebsmodi

| Attribut | Wert |
|---|---|
| Modul-ID | FW-CORE-05 |
| Ebene | 1 – Framework Core |
| Verbindlichkeit | normativ (Abschnitte 1–3), Erläuterung (Abschnitt 4) |
| Owner | `<FRAMEWORK_OWNER>` |
| Version | 0.1.12 |
| Status | `pilot` |

## 1. Standardarbeitsablauf (normativ)

Jede KI-Aufgabe folgt den vierzehn Schritten. Schritte DÜRFEN NICHT übersprungen werden; bei Kontrollstufe niedrig KÖNNEN die Schritte 7 bis 9 in einer einzigen kurzen Interaktion zusammengefasst werden, sofern jeder Schritt erkennbar bleibt.

| Nr. | Schritt | Verantwortung | Mindestinhalt | Referenz |
|---|---|---|---|---|
| 1 | Aufgabe verstehen | Mensch, dann KI-Client | Aufgabenziel, Erfolgskriterium, betroffener Bereich in eigenen Worten wiedergeben | `.koolie/core/prompts/`, `.koolie/core/checklists/01-preflight.md` |
| 2 | Scope und Grenzen bestimmen | Mensch | Erlaubte Pfade, ausgeschlossene Pfade, Betriebsmodus, Kontrollstufe (`09-risk-model.md`) | `.koolie/core/decision-trees/02-may-ai-do-task.md`, `03-analyze-or-modify.md` |
| 3 | Datenschutz und Kontextfreigabe prüfen | Mensch | Kontextklassen aller vorgesehenen Quellen prüfen (`02-privacy.md`); K3-Inhalte ausschließen | `.koolie/core/checklists/02-privacy-context.md`, `.koolie/core/decision-trees/01-context-allowed.md` |
| 4 | Rückfragen und offene Punkte erfassen | KI-Client | Liste der Unklarheiten mit Auswirkung; keine Bearbeitung ungeklärter Punkte (P3) | – |
| 5 | Relevanten Ist-Zustand analysieren | KI-Client | Nur die für die Aufgabe relevanten Dateien lesen; keine Änderungen (P4) | Skill `fw-repo-analyze` |
| 6 | Befunde mit Fundstellen darstellen | KI-Client | Jede Aussage mit `pfad/datei:zeile` oder Suchmuster belegen | – |
| 7 | Lösungsoptionen bewerten | KI-Client, Entscheidung Mensch | Mindestens zwei Optionen bei Stufe mittel/hoch; Kriterien: Risiko, Aufwand, Reversibilität, Konsistenz mit Architektur | Skill `fw-change-analyze` |
| 8 | Vorgehen oder Änderungsplan vorschlagen | KI-Client | Schrittfolge, betroffene Dateien, Tests, Abbruchkriterien | Skill `fw-plan` |
| 9 | Freigabepunkt vor Änderungen am Produktivcode (Schritt 10, M3) | Mensch | Bestätigung des Plans (Stufe mittel) oder dokumentierte Freigabe `<APPROVAL_ROLE>` (Stufe hoch) | `09-risk-model.md` |
| 10 | Änderung in kleinen, nachvollziehbaren Schritten umsetzen | KI-Client unter Beobachtung | Ein logischer Schritt je Änderung; nach jedem Schritt Zwischenstand berichten (P7) | Skill `fw-change-small`, `.koolie/core/checklists/03-before-code-change.md` |
| 11 | Tests und Qualitätsprüfungen ausführen | KI-Client, Bewertung Mensch | Nur im Overlay freigegebene Befehle (`<BUILD_COMMAND>`, `<TEST_COMMAND>`, `<LINT_COMMAND>`); Ergebnisse unverändert berichten | `.koolie/core/checklists/05-testing.md` |
| 12 | Ergebnis, Abweichungen und Restrisiken dokumentieren | KI-Client | Ergebnisbericht nach Standardformat (Abschnitt 3.6) | – |
| 13 | Menschliche Prüfung ermöglichen | KI-Client, dann Mensch | Diff, Fundstellen, Testprotokoll, offene Punkte bereitstellen; Review anhand `.koolie/core/checklists/04-review-ai-code.md` | Skill `fw-review-support` |
| 14 | Übernahme über den bestehenden Review- und Freigabeprozess | Mensch | Merge Request mit KI-Nutzungsvermerk; reguläre Quality Gates und Review (P5, P6) | `.koolie/core/checklists/08-merge-request.md`, Skill `fw-mr-description` |

**Die Spalte „Referenz“ nennt bei sechs Schritten einen Skill (5, 7, 8, 10, 13, 14). Wo sie einen nennt, ist er der vorgesehene Weg des Schrittes** – keine Leseempfehlung. Ein anderer Weg ist zulässig, MUSS aber im Ergebnisbericht benannt und begründet werden (Abschnitt 3.6). **Ein abgewiesener Skill-Aufruf ist keine Verwendung:** Wer die `SKILL.md` ersatzweise liest und ihren Ablauf von Hand nacharbeitet, arbeitet ohne die Werkzeugbeschränkung des Skills. Gemessen am 2026-09-14 `[MESS]` (`.koolie/core/tests/protocols/2026-09-14-erhebung-skillaufruf.md`, D-83): In zwei von zwei nachgearbeiteten Läufen wies die Sitzung den Skill im Bericht als verwendet oder aufgerufen aus, und in einem davon verwendete sie ein Werkzeug, das der Skill sperrt.

## 2. Betriebsmodi (normativ)

Jede Aufgabe wird genau einem Betriebsmodus zugeordnet. Den Modus gibt der Mensch vor; ohne Angabe gilt M1 (D-390). Ein Moduswechsel innerhalb einer Sitzung ist zulässig, MUSS aber ausdrücklich durch den Menschen angewiesen werden und wird vom KI-Client im Ergebnisbericht vermerkt.

### 2.1 Übersicht

| Modus | Kurzzweck | Schreibzugriff auf Dateien | Befehlsausführung | Zulässig bis Kontrollstufe |
|---|---|---|---|---|
| M1 Read-only Analysis | Verstehen und Befunde liefern | nein | nur lesende Analysebefehle, falls im Overlay freigegeben | hoch |
| M2 Guided Planning | Änderungsplan erarbeiten | nur Plan-Datei außerhalb des Quellcodes | wie M1 (nur lesende Analysebefehle) | hoch |
| M3 Controlled Modification | Freigegebene Änderung umsetzen | ja, innerhalb des freigegebenen Scopes | freigegebene Build-, Test- und Lint-Befehle; lesende Git-Befehle (status, diff, log, show, blame) | hoch (nur mit Freigabe und Pairing) |
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
| Umsetzung im Werkzeug | **Die Modusgrenze gilt normativ; technisch durchgesetzt ist sie nicht.** Kennt der KI-Client einen eigenen Nur-Lese-Modus oder ein rein lesendes Agentenprofil, ist dieser Weg vorzuziehen – welcher das ist, steht in der Fähigkeitsmatrix seines Client Packs (Zeilen S3 und A1) `[DOK]` je Pack. Die Skill-`permissions` tragen die Modusgrenze teilweise, ersetzen sie aber nicht `[MESS]`: Bei `claude-code` ist die Quelle `permissions.deny` auf `disallowed-tools` abgebildet, und das entfernt die Schreibwerkzeuge wirklich – gemessen am 2026-09-13 (`tests/protocols/2026-09-13-erhebung-disallowed-tools.md`, D-64). **Die Sperre gilt aber nur für den aufrufenden Turn;** mit der nächsten Nachricht der Person ist das Werkzeug zurück – gemessen. Ein „nur lesender" Skill ist damit nur während seines Turns nur lesend und trägt M1 nicht als Betriebsmodus einer Sitzung. Wer M1 über einen Turn hinaus braucht, braucht die globale Berechtigungsschicht oder einen Nur-Lese-Modus des Clients. Innerhalb des Turns gilt die Entfernung auch für einen Unteragenten, den der Skill startet – gemessen am 2026-09-13 (`tests/protocols/2026-09-13-erhebung-unteragent.md`, D-67) `[MESS]`, mit Kontrolllauf –, sie reicht dort aber genauso weit wie oben: Mit gesperrtem `Write, Edit` schrieb der Unteragent über `Bash`. Das rein lesende Agentenprofil ist der belastbarere Weg zu M1, gemessen am 2026-09-13 (D-68) `[MESS]`: Ein Profil mit `tools: Read, Grep, Glob` hatte kein Schreibwerkzeug im Vorrat; es hängt nicht am Turn, sondern am Profil. Es kann sich nicht selbst erweitern (D-73) `[MESS]`: Ihm fehlt das Werkzeug, um eine zweite, weniger beschränkte Ebene zu starten. Bei Widerspruch gewinnt die restriktivere Liste (D-72) `[MESS]` – ein Profil, das ein Werkzeug ausdrücklich erlaubt, bekommt es unter einem Skill, der es sperrt, nicht; die Liste lässt sich nur enger machen, nie weiter. `allowed-tools` trägt die Grenze nicht: Es ist eine Vorabfreigabe und keine Beschränkung – gemessen am 2026-09-12 (`tests/protocols/2026-09-12-B01-allowed-tools.md`, B01) `[MESS]`. Jedes Pack benennt, was an die Stelle eines verworfenen Feldes tritt, sonst bricht die Installation ab (`CR-2026-050`, D-50); der Ersatz steht in Zeile S3 der Fähigkeitsmatrix. Unabhängig vom Modus wirken die Sperren auf Secret- und Kernpfade `[DOK]` |

#### M2 Guided Planning

| Aspekt | Festlegung |
|---|---|
| Zweck | Umsetzbaren, prüfbaren Änderungsplan vor jeder Modifikation erarbeiten |
| Zulässige Aktionen | Alles aus M1; Optionen bewerten; Plan mit Schritten, betroffenen Dateien, Tests, Risiken und Abbruchkriterien erstellen; Plan-Datei außerhalb des Quellcodes schreiben |
| Verbotene Aktionen | Änderungen an Quellcode, Konfiguration, Tests oder Dokumentation; Befehle mit Seiteneffekten; Annahmen über ungeklärte Anforderungen |
| Benötigter Kontext | Aufgabenbeschreibung mit Akzeptanzkriterien; Analyseergebnis aus M1; Overlay-Regeln zu Architektur, Conventions, Definition of Done |
| Prüfpflichten | Mensch bestätigt oder verwirft den Plan schriftlich (Stufe mittel) beziehungsweise `<APPROVAL_ROLE>` gibt frei (Stufe hoch); jede Planänderung nach Freigabe erfordert erneute Bestätigung |
| Abbruchkriterien | Anforderungen widersprüchlich; Plan würde Delegationsverbotsliste berühren; Plan erfordert Kontext außerhalb der Freigabe |
| Erwartete Ausgabe | Plan nach `.koolie/core/templates/PLAN_TEMPLATE.md`: Ziel, Annahmen (gekennzeichnet), offene Fragen, Schritte, betroffene Dateien, Teststrategie, Risiken, Rollback |
| Umsetzung im Werkzeug | **Die Beschränkung des Schreibrechts auf die Plan-Datei gilt normativ; technisch durchgesetzt ist sie nicht** – kein Mechanismus des Frameworks kennt sie `[KONZ]`. Kennt der KI-Client einen eigenen Planungsmodus mit persistenter Plan-Datei, ist dieser vorzuziehen (Fähigkeitsmatrix des Client Packs) `[DOK]` je Pack. Liegt die Plan-Datei außerhalb des Repositorys, wird sie für die Nachvollziehbarkeit in das im Overlay festgelegte Ablageformat übernommen (`<TBD: Ablage von Plänen im Projekt>`) |

#### M3 Controlled Modification

| Aspekt | Festlegung |
|---|---|
| Zweck | Eine freigegebene, klar abgegrenzte Änderung in kleinen Schritten umsetzen |
| Zulässige Aktionen | Dateien innerhalb `<ALLOWED_PATHS>` ändern; freigegebene Build-, Test- und Lint-Befehle ausführen; lesende Git-Befehle (status, diff, log, show, blame) zur Aufnahme des eigenen Änderungsstands ausführen; nach jedem Schritt Zwischenstand berichten |
| Verbotene Aktionen | Änderungen außerhalb des Scopes; Änderungen an `<EXCLUDED_PATHS>`; neue Abhängigkeiten ohne Freigabe; Git-Operationen mit Fernwirkung (push, merge, tag, rebase auf geteilten Branches); Löschen von Dateien ohne ausdrückliche Einzelfreigabe; Deaktivieren oder Löschen von Tests; Anpassen von Quality-Gate-Konfigurationen |
| Benötigter Kontext | Bestätigter Plan; betroffene Dateien; Coding Conventions; Test- und Build-Befehle aus dem Overlay |
| Prüfpflichten | Mensch beobachtet die Sitzung im rückfragenden Standardmodus (D-05; wie der Modus im Client heißt, nennt die Fähigkeitsmatrix des Client Packs) und bestätigt Schreib- und Ausführungsanfragen einzeln; vollständiger Diff-Review vor Commit; Quality Gates |
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
| Umsetzung im Werkzeug | **Die Beschränkung auf `<TEST_PATHS>` gilt normativ; technisch durchgesetzt ist sie nicht** `[KONZ]`. Der Schutz-Hook kennt weder den Betriebsmodus noch eine Liste erlaubter Schreibpfade und entscheidet innerhalb und außerhalb des Scopes gleich – gemessen am 2026-09-12 (`.koolie/core/tests/protocols/2026-09-12-B04-B05-gegenpruefung.md`, B05) `[DOK]` für den Befund. Die Skill-`permissions` tragen sie ebenfalls nicht (B01, siehe M1); welcher Mechanismus stattdessen trägt, steht in Zeile S3 der Fähigkeitsmatrix des jeweiligen Packs. Getragen wird sie von der Regelschicht und der Prüfpflicht dieses Modus; unabhängig davon wirken die Sperren auf Secret- und Kernpfade `[DOK]` |

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
| Umsetzung im Werkzeug | **Die Beschränkung auf `<DOC_PATHS>` gilt normativ; technisch durchgesetzt ist sie nicht** `[KONZ]`. Eine Beschränkung auf `<DOC_PATHS>` unter Ausschluss aller übrigen Pfade ist über Skill-`permissions` nicht ausdrückbar (`<DOC_PATHS>` ist Teilmenge von `<ALLOWED_PATHS>`, und `deny` gewinnt gegen `allow`) `[DOK]`, und das Feld `permissions` kennt nicht jeder Client für Skills (`skill_frontmatter.drop_fields` im Manifest des Packs, B01) – was an seine Stelle tritt, benennt die Zeile S3 seiner Fähigkeitsmatrix. Der Schutz-Hook trägt sie nicht – er kennt den Modus nicht (`.koolie/core/tests/protocols/2026-09-12-B04-B05-gegenpruefung.md`, B05) `[DOK]` für den Befund. Getragen wird sie von der Regelschicht und der fachlichen Prüfpflicht dieses Modus |

## 3. Querschnittsregeln für alle Modi (normativ)

### 3.1 Sitzungsdisziplin

1. Eine Sitzung bearbeitet eine Aufgabe. Neue Aufgaben MÜSSEN in neuen Sitzungen begonnen werden (Least Context, Nachvollziehbarkeit).
2. Sitzungsweite Freigaben („für diese Sitzung erlauben") SOLLEN nur für die im Overlay freigegebenen Testbefehle erteilt werden. Projektweite oder globale Freigaben `[DOK]` DÜRFEN NICHT durch einzelne Entwicklerinnen oder Entwickler erteilt werden; sie erfordern einen Änderungsantrag an die Berechtigungsdatei.
3. Parallel laufende Agentensitzungen `[DOK]` sind an **Voraussetzungen** gebunden, nicht an eine Kontrollstufe der Aufgabe: Die Aufgaben MÜSSEN voneinander unabhängig sein, die Schreibziele disjunkt – sie DÜRFEN NICHT auf denselben Dateien arbeiten –, eine Person MUSS die Aufsicht führen, und jede Sitzung MUSS ihre eigene Aufgabe und ihren eigenen Ergebnisbericht haben. Die Einstufung dieser Arbeitsweise leistet R12 (`.koolie/core/framework/core/09-risk-model.md`, Abschnitt 2): rein lesende Parallelarbeit unter Aufsicht niedrig, schreibende auf getrennten Zielen mittel, gemeinsame Schreibziele hoch und damit ausgeschlossen. Jede parallel bearbeitete Aufgabe bleibt an die Betriebsmodi **ihrer eigenen** Kontrollstufe gebunden (D-54).
4. Hintergrund-Subagenten DÜRFEN NICHT für Modus M3 verwendet werden. **Diese Grenze gilt normativ; technisch abbildbar ist sie nicht** `[MESS]`: Sperrbar ist nur das Startwerkzeug ganz – gemessen am 2026-09-13, `disallowed-tools: Agent` weist den Start ab, und die zweite Schreibweise `Task` ebenso (`tests/protocols/2026-09-13-erhebung-unteragent.md`, D-70). „Nur im Hintergrund" ist dagegen ein Argument (`run_in_background`), und ein Argumentmuster in der Werkzeugsperre wirkt nach D-66 lautlos gar nicht. Wer diese Regel technisch durchsetzen will, sperrt Unteragenten vollständig – das ist mehr, als die Regel sagt, und deshalb bleibt sie eine Anweisung. Was ein Skill sperrt, ist auch im Hintergrund gesperrt – gemessen am 2026-09-13 mit Kontrolllauf (D-72) `[MESS]`. Ein Hintergrund-Unteragent ist also kein Weg, ein entferntes Werkzeug zurückzubekommen, sondern ein Weg, unbeaufsichtigt zu arbeiten – und das untersagt die Regel. Für M1 KANN ein rein lesendes Agentenprofil genutzt werden, sofern der KI-Client eines kennt (Fähigkeitsmatrix des Client Packs, A1); bei `claude-code` ist seine Wirkung gemessen (D-68).

### 3.2 Befehlsausführung

1. Der KI-Client führt nur Befehle aus, die im Overlay als freigegeben gelistet sind (`<BUILD_COMMAND>`, `<TEST_COMMAND>`, `<LINT_COMMAND>`, weitere in `.koolie/project-overlay/OVERLAY.md` Abschnitt 6).
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
- Verwendete Skills: <Skill-IDs und Versionen | keiner: welcher Skill in Frage kam und warum ohne ihn gearbeitet wurde | abgewiesen und von Hand nachgearbeitet: welcher>
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
