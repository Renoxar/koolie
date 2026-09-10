# Checkliste FW-CL-03 – Vor Codeänderungen (Modi M3, M4, M5)

| Attribut | Wert |
|---|---|
| ID | `FW-CL-03` |
| Version | `0.1.0` |
| Status | `entwurf` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Wann | nach Preflight und Analyse, unmittelbar bevor Devin erstmals schreiben oder Befehle ausführen soll |
| Wer | Bearbeiterin oder Bearbeiter |
| Dauer (Richtwert, Erläuterung) | wenige Minuten – keine verbindlichen Aufwände |
| Nachweis | bestätigter Plan (ab mittel), Schrittprotokoll im Ergebnisbericht |

## Zweck

Sichert die Voraussetzungen aus Schritt 9–10 des Standardarbeitsablaufs, bevor die erste Änderung entsteht: Freigaben, belegter Ist-Zustand, sauberer Ausgangspunkt, klare Grenzen.

## Prüfpunkte

### Freigaben und Plan

- [ ] **MUSS** Stufe niedrig: Aufgabe klar abgegrenzt (Ziel, Scope, Akzeptanzkriterien). Stufe mittel: Plan nach `leitwerk-core/templates/PLAN_TEMPLATE.md` liegt vor und ist schriftlich bestätigt. Stufe hoch: dokumentierte Freigabe `<APPROVAL_ROLE>` (bei R3/R10 zusätzlich `<SECURITY_CONTACT>`) und begleitende Person vorhanden.
- [ ] **MUSS** Der Plan beziehungsweise die Aufgabe berührt keine Delegationsverbote (V1–V12).

### Ist-Zustand und Auswirkungen

- [ ] **MUSS** Relevanter Ist-Zustand ist analysiert; Befunde mit Fundstellen liegen vor (P4; Skills `fw-repo-analyze`, `fw-change-analyze`).
- [ ] **MUSS** Verwender der zu ändernden Elemente sind ermittelt (Aufrufer, Konfigurationsreferenzen, Schnittstellen).
- [ ] **MUSS** Tests des betroffenen Bereichs sind vor der Änderung ausgeführt; Ausgangsergebnis dokumentiert („grün vorher"; bei rotem Stand zuerst `fw-error-analyze`).

### Arbeitsumgebung

- [ ] **MUSS** Eigener Arbeitsbranch nach `<BRANCHING_MODEL>`/`<BRANCH_PREFIX>`; niemals ein geschützter Branch.
- [ ] **MUSS** Arbeitsstand sauber (kein fremder Diff); Devin-Änderungen bleiben dadurch einzeln zurechenbar (P7).
- [ ] **MUSS** Nur freigegebene Befehle vorgesehen (`<BUILD_COMMAND>`, `<TEST_COMMAND>`, `<LINT_COMMAND>`, Overlay Abschnitt 6).
- [ ] **MUSS** Schreibgrenzen benannt: M3 nur `<ALLOWED_PATHS>` abzüglich `<READ_ONLY_PATHS>`; M4 nur `<TEST_PATHS>`; M5 nur `<DOC_PATHS>`.

### Grenzen der Änderung

- [ ] **MUSS** Keine Änderungen an Abhängigkeiten, Lockfiles, Paketquellen, CI/CD- oder Quality-Gate-Konfiguration vorgesehen; sonst Abbruch und regulärer Prozess (`leitwerk-core/checklists/07-new-dependency.md`, Änderungsantrag).
- [ ] **MUSS** Abbruchkriterien der Sitzung sind vereinbart (Planabweichung, Scope-Verlassen, steigende Stufe, rote Tests außerhalb des Scopes).
- [ ] **SOLL** Erwarteter Umfang unter `<CHANGE_SIZE_THRESHOLD>` Dateien; sonst Aufteilung (Q8).
- [ ] **SOLL** Zeitpunkt so gewählt, dass die Sitzung beobachtet zu Ende geführt werden kann (M3 wird nicht unbeaufsichtigt fortgesetzt).

## Abbruch- und Eskalationskriterien

Nicht beginnen bei fehlender Bestätigung oder Freigabe (E1/E2), rotem Ausgangsstand (E0, erst Ursache klären), unklaren Verwendern kritischer Elemente (E1 an `<ARCHITECT_ROLE>`) oder wenn die Änderung nur außerhalb der Schreibgrenzen möglich wäre (E1, Scope-Entscheidung durch Menschen; `leitwerk-core/framework/core/10-error-escalation.md`).

## Ergebnis und Nachweis

Bestätigter Plan (Referenz), Ausgangs-Testergebnis und vereinbarte Grenzen werden im Ergebnisbericht und ab Stufe mittel im Devin-Nutzungsvermerk dokumentiert.
