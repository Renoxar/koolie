# Beispiel (synthetisch): Merge-Request-Beschreibung mit Devin-Nutzungsvermerk

> Synthetisches Beispiel nach Skill `fw-mr-description` und `templates/MR_AI_DISCLOSURE.md` (Kurzform, Stufe niedrig). Projekt, Ticket und Inhalte sind erfunden.

```markdown
## Fehlermeldung bei ungültiger Menge nennt jetzt den gültigen Bereich

**Ticket:** BSV-Ticket (Platzhalter) · **Kategorie:** Fehlerbehebung · **Ziel-Branch:** main

### Was und warum
Die Validierungsmeldung für ungültige Bestellmengen nannte den zulässigen Bereich nicht; Nutzerinnen und Nutzer konnten den Fehler nicht selbst beheben. Die Meldung nennt jetzt den Bereich aus den bestehenden Konstanten (keine fachliche Logikänderung).

### Änderungen
- src/ordering/domain/OrderValidator.ext: Meldungstext um Bereich ergänzt (Zeile 47)
- test/ordering/OrderValidatorTest.ext: neuer Testfall „Meldung nennt Bereich" (Zeilen 88–95)

### Testnachweis
- build-tool lint: erfolgreich · build-tool test: 214 Tests, 0 Fehlschläge (lokal; CI siehe Pipeline)

### Risiken und Hinweise für das Review
- Reine Textänderung plus Test; bitte RV2 (Fundstellen) und RV4 (Testaussagekraft) kurz gegenprüfen.
- Offener Punkt aus dem Ergebnisbericht: Falls Meldungstexte fachlich abgestimmt werden, bitte PO-Bestätigung.

### KI-Unterstützung (Devin Desktop)
- Kontrollstufe: niedrig (Faktor R1) · Betriebsmodus: M3
- Verwendete Skills: fw-change-analyze v0.1.0, fw-change-small v0.1.0
- Verwendeter Kontext: OrderValidator.ext, OrderValidatorTest.ext, bsv-guidelines.md (alle K1)
- Selbstreview nach checklists/04-review-ai-code.md: durchgeführt
- Verworfene Vorschläge: 1 (erster Vorschlag formatierte die gesamte Datei um – Scope-Verstoß, verworfen)
```
