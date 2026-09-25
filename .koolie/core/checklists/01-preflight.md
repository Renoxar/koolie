# Checkliste FW-CL-01 – Preflight-Check vor jeder KI-Aufgabe

| Attribut | Wert |
|---|---|
| ID | `FW-CL-01` |
| Version | `0.1.7` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Wann | vor jeder KI-Sitzung, nach Zuschnitt der Aufgabe |
| Wer | Bearbeiterin oder Bearbeiter |
| Dauer (Richtwert, Erläuterung) | wenige Minuten – keine verbindlichen Aufwände |
| Nachweis | Kontrollstufe, Faktor und Modus in der Aufgabenanweisung; ab Stufe mittel im Ergebnisbericht |

## Zweck

Stellt vor dem ersten Prompt sicher, dass die Aufgabe delegierbar, richtig eingestuft, sauber abgegrenzt und der Kontext zulässig ist. Ohne abgeschlossenen Preflight-Check beginnt keine KI-Aufgabe (`.koolie/core/framework/core/05-working-model.md`, Schritt 1–4).

## Prüfpunkte

### Aufgabe und Delegierbarkeit

- [ ] **MUSS** Ziel und Akzeptanzkriterien der Aufgabe liegen schriftlich vor (ein Ziel je Aufgabe).
- [ ] **MUSS** Die Aufgabe steht nicht auf der Delegationsverbotsliste V1–V12 (`.koolie/core/framework/core/09-risk-model.md` Abschnitt 4); andernfalls Abbruch (nur menschliche Bearbeitung, der KI-Client höchstens vorbereitende Analyse, sofern zulässig).
- [ ] **MUSS** Der Entscheidungsbaum `.koolie/core/decision-trees/02-may-ai-do-task.md` wurde bei Unsicherheit durchlaufen.
- [ ] **SOLL** Die Aufgabe ist klein genug für eine Sitzung; sonst zerlegen (Analyse → Plan → Umsetzung).

### Einstufung

- [ ] **MUSS** Kontrollstufe nach `.koolie/core/framework/core/09-risk-model.md` bestimmt (alle Faktoren R1–R13 durchgegangen, Maximumprinzip) und der auslösende Faktor notiert (zum Beispiel „mittel wegen R8").
- [ ] **MUSS** Betriebsmodus M1–M5 festgelegt (`.koolie/core/decision-trees/03-analyze-or-modify.md`).
- [ ] **MUSS** Bei Stufe mittel: Planbestätigung vor Umsetzung eingeplant. Bei Stufe hoch: dokumentierte Freigabe `<APPROVAL_ROLE>` liegt vor und eine begleitende Person ist benannt.
- [ ] **MUSS** Im Zweifel zwischen zwei Stufen wurde die höhere gewählt.

### Scope und Kontext

- [ ] **MUSS** Erlaubte Pfade für diese Aufgabe benannt; `<EXCLUDED_PATHS>` und `<READ_ONLY_PATHS>` bekannt.
- [ ] **MUSS** Kontextquellen gelistet und je Quelle die Kontextklasse bestimmt (`.koolie/core/checklists/02-privacy-context.md`); K2 nur mit Freigabe, K3 nie.
- [ ] **MUSS** Overlay-Status ist `aktiv` (Ausnahme: Onboarding-Übung auf dem Übungsrepository; am Quellrepositorium des Frameworks gilt stattdessen `.koolie/core/governance/FRAMEWORK_DEV_PROFILE.md`, das **keine** technische Berechtigung erteilt und dessen Geltung der KI-Client nicht selbst feststellt – D-253).
- [ ] **SOLL** Passender Skill als vorgesehener Weg gewählt (`/fw-…`); ein anderer Weg MUSS im Ergebnisbericht benannt und begründet werden (`.koolie/core/framework/core/05-working-model.md` Abschnitt 1; `.koolie/core/prompts/README.md` Abschnitt 2). Die Wahl liegt **nicht allein** hier: Der KI-Client prüft sie vor jedem Schritt selbst.

### Sitzung und Werkzeug

- [ ] **MUSS** Neue Sitzung für diese Aufgabe; rückfragender Standardmodus; weder der Modus ohne Rückfragen noch ein Modus mit selbsttätiger Übernahme aktiv (D-05; wie der Modus im Client heißt, nennt die Fähigkeitsmatrix des Client Packs).
- [ ] **MUSS** Freigaben werden nur einmalig oder sitzungsweise erteilt; keine projekt- oder globalen Freigaben.
- [ ] **SOLL** Arbeitsstand sauber (kein offener Diff fremder Arbeit im Arbeitsbereich).
- [ ] **KANN** Bei M3/M4: `.koolie/core/checklists/03-before-code-change.md` bereitgelegt.

## Abbruch- und Eskalationskriterien

Aufgabe nicht beginnen und gemäß `.koolie/core/framework/core/10-error-escalation.md` behandeln, wenn: die Aufgabe unter ein Delegationsverbot fällt (E0/E2), die Einstufung unklar bleibt (E1), erforderliche Freigaben fehlen (E2), benötigter Kontext nur als K3 verfügbar wäre (E0, gegebenenfalls E3) oder das Overlay nicht aktiv ist (E1 an Overlay Owner).

## Ergebnis und Nachweis

Kontrollstufe (mit Faktor), Modus, Scope und verwendete Kontextquellen werden in die Aufgabenanweisung übernommen (Pflichtelemente nach `.koolie/core/framework/core/06-prompting-rules.md`) und erscheinen im Ergebnisbericht sowie ab Stufe mittel im KI-Nutzungsvermerk des Merge Requests.
