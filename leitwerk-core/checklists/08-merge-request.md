# Checkliste FW-CL-08 – Merge Request

| Attribut | Wert |
|---|---|
| ID | `FW-CL-08` |
| Version | `0.1.1` |
| Status | `entwurf` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Wann | vor dem Erstellen und vor dem Mergen eines Merge Requests mit Devin-Beteiligung |
| Wer | Bearbeiterin oder Bearbeiter (Erstellen); Reviewerinnen, Reviewer und freigebende Rollen (Mergen) |
| Dauer (Richtwert, Erläuterung) | wenige Minuten zusätzlich zum Review – keine verbindlichen Aufwände |
| Nachweis | Merge Request selbst (Beschreibung, Vermerk, Befunde, Freigaben) |

## Zweck

Sichert Schritt 14 des Standardarbeitsablaufs: Übernahme ausschließlich über den bestehenden Review- und Freigabeprozess, mit vollständiger Nachvollziehbarkeit der Devin-Beteiligung.

## Prüfpunkte

### Vor dem Erstellen (Bearbeiterin oder Bearbeiter)

- [ ] **MUSS** Der Merge Request verfolgt genau ein Ziel (Q1); vermischte Änderungen sind aufgeteilt.
- [ ] **MUSS** Beschreibung liegt vor (Skill `fw-mr-description` oder manuell) und folgt `<MR_TEMPLATE_PATH>`; Ticket-Bezug hergestellt.
- [ ] **MUSS** KI-Nutzungsvermerk enthalten (`leitwerk-core/templates/MR_AI_DISCLOSURE.md`): Kurzform bei Stufe niedrig, Langform ab Stufe mittel (mit Plan-Referenz, Kontextliste, Befehlen, Abweichungen, Restrisiken).
- [ ] **MUSS** Selbstreview nach `leitwerk-core/checklists/04-review-ai-code.md` durchgeführt und im Vermerk bestätigt.
- [ ] **MUSS** Lokale Prüfungen grün (`<LINT_COMMAND>`, `<TEST_COMMAND>`); Tests für geänderte Logik vorhanden (Q2, `leitwerk-core/checklists/05-testing.md`).
- [ ] **MUSS** Keine K3-Inhalte und keine Personennamen in Beschreibung, Commits, Kommentaren oder Anhängen; Rollen statt Personen.
- [ ] **MUSS** Abhängigkeiten, Lockfiles, CI/CD- und Quality-Gate-Konfiguration unverändert oder über den regulären Prozess begründet (RV6, RV9, `leitwerk-core/checklists/07-new-dependency.md`).
- [ ] **MUSS** Push und Erstellung des Merge Requests erfolgen durch den Menschen (V2).
- [ ] **SOLL** Commit-Nachrichten folgen `<COMMIT_CONVENTION>`; Änderungsschritte sind einzeln nachvollziehbar (P7).
- [ ] **SOLL** Offene Punkte und Annahmen aus dem Ergebnisbericht sind im Merge Request sichtbar gemacht.

### Vor dem Mergen (Review und Freigabe)

- [ ] **MUSS** Alle Quality Gates der Pipeline sind erfolgreich (`<QUALITY_GATE>`, P6); keine deaktivierten Prüfungen.
- [ ] **MUSS** Review-Tiefe entspricht der Kontrollstufe: niedrig – vollständiges Lesen des Diffs; mittel – unabhängiges Review aller RV-Punkte und Planabgleich; hoch – zusätzlich Architektur-/Security-Review und Prüfung des Sitzungsprotokolls (`leitwerk-core/framework/core/07-review-rules.md` Abschnitt 3).
- [ ] **MUSS** Erforderliche Freigaben liegen vor (Stufe hoch: `<APPROVAL_ROLE>`, bei R3/R10 `<SECURITY_CONTACT>`); Devin hat keine Freigabe erteilt (V1).
- [ ] **MUSS** Alle Review-Befunde sind aufgelöst oder mit Begründung zurückgestellt.
- [ ] **SOLL** Metrikdaten für den Pilot erfasst (Kontrollstufe, Modus, Review-Iterationen, verworfene Vorschläge – `leitwerk-core/pilot/METRICS.md`).

## Abbruch- und Eskalationskriterien

Fehlender Nutzungsvermerk, rote Gates, unaufgelöste MUSS-Befunde oder fehlende Freigaben blockieren den Merge (E1/E2). Nachträglich entdeckte K3-Inhalte: E3 (`leitwerk-core/framework/core/02-privacy.md` Abschnitt 5) und Bereinigung vor jeder weiteren Verarbeitung.

## Ergebnis und Nachweis

Der Merge Request dokumentiert Beschreibung, Vermerk, Befunde, Freigaben und Pipeline-Ergebnisse; er ist damit der zentrale Audit-Nachweis je Änderung (`leitwerk-core/framework/core/01-governance.md` Abschnitt 4).
