# Checkliste FW-CL-11 – Framework-Release

| Attribut | Wert |
|---|---|
| ID | `FW-CL-11` |
| Version | `0.1.0` |
| Status | `entwurf` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Wann | vor jedem Framework-Release (auch Patch-Releases) |
| Wer | Framework Owner; Zuarbeit Modul-Owner |
| Dauer (Richtwert, Erläuterung) | abhängig vom Änderungsumfang – keine verbindlichen Aufwände |
| Nachweis | Release-Eintrag in `devin-core-framework/CHANGELOG.md`; abgelegte Checkliste; Testkatalog-Protokoll |

## Zweck

Sichert, dass ein Release konsistent, projektneutral, getestet und für übernehmende Projekte nachvollziehbar ist (`devin-core-framework/governance/RELEASE_PROCESS.md`).

Die mit **(ab 1.0.0, D-11)** gekennzeichneten Prüfpunkte gelten erst für das Release 1.0.0 und darüber; sie bilden die Kriterien aus Decision Record D-11 ab (`CR-2026-001`). Pilot, Onboarding und organisatorische Freigabe sind **keine** Prüfpunkte dieser Checkliste – sie liegen projektseitig (`devin-core-framework/checklists/10-project-adoption.md`).

## Prüfpunkte

### Inhalt und Konsistenz

- [ ] **MUSS** Alle für das Release vorgesehenen Änderungsanträge sind abgeschlossen oder ausdrücklich verschoben (`devin-core-framework/governance/DECISION_LOG.md` aktualisiert).
- [ ] **MUSS** Konsistenz Core ↔ Laufzeitfassung geprüft: `devin-core-framework/framework/core/*` gegen die Wurzel-Anweisungsdatei und die Regelablage `00-*, 10-*, 15-*` **jedes Client Packs** (Stichproben je geändertem Modul; keine widersprüchlichen Anweisungen).
- [ ] **MUSS** Skills konsistent zum Skill-Standard (`devin-core-framework/framework/core/08-skill-conventions.md`); Versionen, Status und CHANGELOG je geändertem Skill gepflegt; Deprecations mit Nachfolger dokumentiert.
- [ ] **MUSS** Prioritätshierarchie unverändert oder Änderung begründet und in `devin-core-framework/governance/PRIORITY_HIERARCHY.md` nachgezogen.
- [ ] **SOLL** Templates, Checklisten und Entscheidungsbäume gegen geänderte Module abgeglichen (Querverweise, Begriffe).

### Projektneutralität

- [ ] **MUSS** `python3 devin-core-framework/tests/scripts/validate-framework.py` ohne Fehler; Warnungen bewertet.
- [ ] **MUSS** `project-overlay/forbidden-terms.txt` ist im Release leer (projektlokale Sperrlisten verbleiben in den Projekten).
- [ ] **MUSS** Manuelle Stichprobe auf projekt-, kunden- oder personenspezifische Inhalte in geänderten Dateien (zusätzlich zur automatischen Prüfung).
- [ ] **MUSS** Beispiele sind synthetisch gekennzeichnet; Platzhalterregister aktuell.

### Produktstand Devin

- [ ] **MUSS** Aktualitätsprüfung gegen die offizielle Devin-Dokumentation durchgeführt (Changelog des Produkts gesichtet; betroffene `[DOK]`-Aussagen und `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>`-Marker aktualisiert; Quellenliste im Hauptdokument nachgezogen).
- [ ] **MUSS** Produktänderungen mit Regelwirkung (neue Berechtigungen, geänderte Pfade, entfallene Mechanismen) sind als Änderungsanträge behandelt (`devin-core-framework/governance/RELEASE_PROCESS.md`, Abschnitt Produktbeobachtung).

### Tests

- [ ] **MUSS** Testkatalog vollständig ausgeführt (`devin-core-framework/tests/TEST_CATALOG.md`): Konsistenz-, Positiv-, Negativ-, Datenschutz-, Prompt-Injection-, Scope-, Fehlende-Informationen-, Zugriffs- und Regressionstests; Ergebnisse je Test-ID dokumentiert.
- [ ] **MUSS** (ab 1.0.0, D-11) Kein Testfall des Katalogs steht auf Ergebnisstatus `offen`; jeder trägt `bestanden`, `fehlgeschlagen (Referenz)` oder `nicht anwendbar (Begründung)`.
- [ ] **MUSS** Skill-Testfälle (`TESTS.md` je Skill) für alle geänderten Skills erneut ausgeführt.
- [ ] **MUSS** Hook- und Validierungsskripte laufen fehlerfrei (Selbsttest der Skripte).
- [ ] **SOLL** Mindestens ein vollständiger Durchlauf des Standardarbeitsablaufs auf dem Übungsrepository (M1 → M2 → M3 → M4) ohne Regelverstoß.

### Abschluss

- [ ] **MUSS** `devin-core-framework/VERSION` nach Semantic Versioning erhöht; `devin-core-framework/CHANGELOG.md` mit Änderungen, Migrationshinweisen für Overlays und bekannten Einschränkungen ergänzt.
- [ ] **MUSS** Release-Archiv erzeugt und abgelegt; übernehmende Projekte informiert (Migrationshinweise, betroffene Overlay-Felder).
- [ ] **MUSS** Freigabe des Releases durch den Framework Owner dokumentiert.
- [ ] **MUSS** (ab 1.0.0, D-11) Alle Core-Module, Skills und Packs tragen einen Status oberhalb von `entwurf`.
- [ ] **MUSS** (ab 1.0.0, D-11) Kein Decision Record in `devin-core-framework/governance/DECISION_LOG.md` trägt den Status `entschieden (Vorschlag)`.
- [ ] **MUSS** (ab 1.0.0, D-11) Übernahme in mindestens ein zweites Projekt nach `devin-core-framework/checklists/10-project-adoption.md` nachgewiesen.

## Abbruch- und Eskalationskriterien

Fehlschläge im Testkatalog, offene Konsistenzbefunde oder Projektneutralitätsverstöße stoppen das Release (E4). Sicherheitsrelevante Befunde folgen `devin-core-framework/governance/INCIDENT_HANDLING.md`.

## Ergebnis und Nachweis

Release-Eintrag im `devin-core-framework/CHANGELOG.md`, Testkatalog-Protokoll, abgelegte Checkliste und Archivreferenz bilden zusammen den Audit-Nachweis des Releases.
