# Checkliste FW-CL-01 – Preflight-Check vor jeder Devin-Aufgabe

| Attribut | Wert |
|---|---|
| ID | `FW-CL-01` |
| Version | `0.1.0` |
| Status | `entwurf` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Wann | vor jeder Devin-Sitzung, nach Zuschnitt der Aufgabe |
| Wer | Bearbeiterin oder Bearbeiter |
| Dauer (Richtwert, Erläuterung) | wenige Minuten – keine verbindlichen Aufwände |
| Nachweis | Kontrollstufe, Faktor und Modus in der Aufgabenanweisung; ab Stufe mittel im Ergebnisbericht |

## Zweck

Stellt vor dem ersten Prompt sicher, dass die Aufgabe delegierbar, richtig eingestuft, sauber abgegrenzt und der Kontext zulässig ist. Ohne abgeschlossenen Preflight-Check beginnt keine Devin-Aufgabe (`framework/core/05-working-model.md`, Schritt 1–4).

## Prüfpunkte

### Aufgabe und Delegierbarkeit

- [ ] **MUSS** Ziel und Akzeptanzkriterien der Aufgabe liegen schriftlich vor (ein Ziel je Aufgabe).
- [ ] **MUSS** Die Aufgabe steht nicht auf der Delegationsverbotsliste V1–V12 (`framework/core/09-risk-model.md` Abschnitt 4); andernfalls Abbruch (nur menschliche Bearbeitung, Devin höchstens vorbereitende Analyse, sofern zulässig).
- [ ] **MUSS** Der Entscheidungsbaum `decision-trees/02-may-devin-do-task.md` wurde bei Unsicherheit durchlaufen.
- [ ] **SOLL** Die Aufgabe ist klein genug für eine Sitzung; sonst zerlegen (Analyse → Plan → Umsetzung).

### Einstufung

- [ ] **MUSS** Kontrollstufe nach `framework/core/09-risk-model.md` bestimmt (alle Faktoren R1–R13 durchgegangen, Maximumprinzip) und der auslösende Faktor notiert (zum Beispiel „mittel wegen R8").
- [ ] **MUSS** Betriebsmodus M1–M5 festgelegt (`decision-trees/03-analyze-or-modify.md`).
- [ ] **MUSS** Bei Stufe mittel: Planbestätigung vor Umsetzung eingeplant. Bei Stufe hoch: dokumentierte Freigabe `<APPROVAL_ROLE>` liegt vor und eine begleitende Person ist benannt.
- [ ] **MUSS** Im Zweifel zwischen zwei Stufen wurde die höhere gewählt.

### Scope und Kontext

- [ ] **MUSS** Erlaubte Pfade für diese Aufgabe benannt; `<EXCLUDED_PATHS>` und `<READ_ONLY_PATHS>` bekannt.
- [ ] **MUSS** Kontextquellen gelistet und je Quelle die Kontextklasse bestimmt (`checklists/02-privacy-context.md`); K2 nur mit Freigabe, K3 nie.
- [ ] **MUSS** Overlay-Status ist `aktiv` (Ausnahme: Onboarding-Übung auf dem Übungsrepository).
- [ ] **SOLL** Passender Skill gewählt (`/fw-…`); freier Prompt nur, wenn kein Skill passt (`prompts/README.md`).

### Sitzung und Werkzeug

- [ ] **MUSS** Neue Sitzung für diese Aufgabe; Permission-Modus Normal; Bypass und Smart nicht aktiv (D-05).
- [ ] **MUSS** Freigaben werden nur einmalig oder sitzungsweise erteilt; keine projekt- oder globalen Freigaben.
- [ ] **SOLL** Arbeitsstand sauber (kein offener Diff fremder Arbeit im Arbeitsbereich).
- [ ] **KANN** Bei M3/M4: `checklists/03-before-code-change.md` bereitgelegt.

## Abbruch- und Eskalationskriterien

Aufgabe nicht beginnen und gemäß `framework/core/10-error-escalation.md` behandeln, wenn: die Aufgabe unter ein Delegationsverbot fällt (E0/E2), die Einstufung unklar bleibt (E1), erforderliche Freigaben fehlen (E2), benötigter Kontext nur als K3 verfügbar wäre (E0, gegebenenfalls E3) oder das Overlay nicht aktiv ist (E1 an Overlay Owner).

## Ergebnis und Nachweis

Kontrollstufe (mit Faktor), Modus, Scope und verwendete Kontextquellen werden in die Aufgabenanweisung übernommen (Pflichtelemente nach `framework/core/06-prompting-rules.md`) und erscheinen im Ergebnisbericht sowie ab Stufe mittel im Devin-Nutzungsvermerk des Merge Requests.
