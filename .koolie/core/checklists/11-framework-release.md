# Checkliste FW-CL-11 – Framework-Release

| Attribut | Wert |
|---|---|
| ID | `FW-CL-11` |
| Version | `0.5.0` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Wann | vor jedem Framework-Release (auch Patch-Releases) |
| Wer | Framework Owner; Zuarbeit Modul-Owner |
| Dauer (Richtwert, Erläuterung) | abhängig vom Änderungsumfang – keine verbindlichen Aufwände |
| Nachweis | Release-Eintrag in `.koolie/core/CHANGELOG.md`; abgelegte Checkliste; Testkatalog-Protokoll |

## Zweck

Sichert, dass ein Release konsistent, projektneutral, getestet und für übernehmende Projekte nachvollziehbar ist (`.koolie/core/governance/RELEASE_PROCESS.md`).

Die mit **(ab 1.0.0)** gekennzeichneten Prüfpunkte gelten für jedes Release ab 1.0.0. Pilot, Onboarding und organisatorische Freigabe sind keine Prüfpunkte dieser Checkliste; sie liegen projektseitig (`.koolie/core/checklists/10-project-adoption.md`).

## Prüfpunkte

### Inhalt und Konsistenz

- [ ] **MUSS** Alle für das Release vorgesehenen Änderungsanträge sind abgeschlossen oder ausdrücklich verschoben (`.koolie/core/governance/DECISION_LOG.md` aktualisiert).
- [ ] **MUSS** Konsistenz Core ↔ Laufzeitfassung geprüft: `.koolie/core/framework/core/*` gegen die Wurzel-Anweisungsdatei und die Regelablage `00-*, 10-*, 15-*` **jedes Client Packs** (Stichproben je geändertem Modul; keine widersprüchlichen Anweisungen).
- [ ] **MUSS** Skills konsistent zum Skill-Standard (`.koolie/core/framework/core/08-skill-conventions.md`); Versionen, Status und CHANGELOG je geändertem Skill gepflegt; Deprecations mit Nachfolger dokumentiert.
- [ ] **MUSS** Version je geänderter Checkliste und je geändertem Prompt gepflegt (Metadatentabelle, Semantic Versioning wie in `.koolie/core/governance/RELEASE_PROCESS.md` Abschnitt 1; Testfall `FW-VN-01`). Ein reiner Statuswechsel ist keine Änderung im Sinne dieses Prüfpunkts (`.koolie/core/framework/core/01-governance.md` Abschnitt 5 Punkt 5).
- [ ] **MUSS** Prioritätshierarchie unverändert oder Änderung begründet und in `.koolie/core/governance/PRIORITY_HIERARCHY.md` nachgezogen.
- [ ] **SOLL** Templates, Checklisten und Entscheidungsbäume gegen geänderte Module abgeglichen (Querverweise, Begriffe).
- [ ] **MUSS** Jedes geänderte Dokument gegen die Kriterien seiner Klasse gehalten (`.koolie/core/docs/DOCUMENTATION_STANDARD.md`); die Prüfungen 91 bis 94 laufen mit dem Validator.
- [ ] **SOLL** Bei einem wesentlich geänderten Dokument der Klasse A (Einstieg) die Kaltleser-Probe gefahren und im Protokoll festgehalten.

### Projektneutralität

- [ ] **MUSS** `python3 .koolie/core/tests/scripts/validate-framework.py` ohne Fehler; Warnungen bewertet.
- [ ] **MUSS** `.koolie/project-overlay/forbidden-terms.txt` ist im Release leer (projektlokale Sperrlisten verbleiben in den Projekten).
- [ ] **MUSS** Manuelle Stichprobe auf projekt-, kunden- oder personenspezifische Inhalte in geänderten Dateien (zusätzlich zur automatischen Prüfung).
- [ ] **MUSS** Beispiele sind synthetisch gekennzeichnet; Platzhalterregister aktuell.

### Produktstand der KI-Client

- [ ] **MUSS** Aktualitätsprüfung gegen die offizielle Clientdokumentation durchgeführt (Changelog des Produkts gesichtet; betroffene `[DOK]`-Aussagen und Belegzellen mit `BELEG OFFEN` aktualisiert; Quellenliste im Hauptdokument nachgezogen).
- [ ] **MUSS** Produktänderungen mit Regelwirkung (neue Berechtigungen, geänderte Pfade, entfallene Mechanismen) sind als Änderungsanträge behandelt (`.koolie/core/governance/RELEASE_PROCESS.md` Abschnitt 6).

### Tests

- [ ] **MUSS** Testkatalog vollständig ausgeführt (`.koolie/core/tests/TEST_CATALOG.md`): Konsistenz-, Positiv-, Negativ-, Datenschutz-, Prompt-Injection-, Scope-, Fehlende-Informationen-, Zugriffs-, Regressions-, Versions- und Aktualitätstests; Ergebnisse je Test-ID dokumentiert.
- [ ] **MUSS** (ab 1.0.0) Kein Testfall des Katalogs steht auf Ergebnisstatus `offen`; jeder trägt `bestanden`, `fehlgeschlagen (Referenz)` oder `nicht anwendbar (Begründung)`.
- [ ] **MUSS** Skill-Testfälle (`TESTS.md` je Skill) für alle geänderten Skills erneut ausgeführt.
- [ ] **MUSS** Hook- und Validierungsskripte laufen fehlerfrei (Selbsttest der Skripte).
- [ ] **MUSS** Jedes Abnahmeprotokoll des Testkatalogs (Dateiname `JJJJ-MM-TT-FW-<Klasse>-<NN>.md`) trägt einen Abschnitt *Gegenzeichnung* ohne offenes `<TBD>` (Prüfung 80). Arbeits- und Messprotokolle brauchen keinen: Sie tragen ihren Beleg in sich. Ist keine zweite Rolle vorhanden, wird selbst gegengezeichnet, und der Abschnitt weist das ausdrücklich als „Selbstgegenzeichnung“ aus.
- [ ] **SOLL** Mindestens ein vollständiger Durchlauf des Standardarbeitsablaufs auf dem Übungsrepository (M1 → M2 → M3 → M4) ohne Regelverstoß.

### Abschluss

- [ ] **MUSS** `.koolie/core/VERSION` nach Semantic Versioning erhöht; `.koolie/core/CHANGELOG.md` mit Änderungen, Migrationshinweisen für Overlays und bekannten Einschränkungen ergänzt.
- [ ] **MUSS** Als letzter Eingriff in den Kern, vor dem Release-Commit: Bestandsliste `.koolie/core/governance/ADOPTION_REGISTRY.md` auf den Zielstand fortgeschrieben (Prüfung 82), dann übernehmende Projekte gehoben – `install.py --target <projekt> --update` aus dem Arbeitsbaum, Overlay-Wert in den drei Trägern nachgezogen, `validate-framework.py --strict-overlay` dort gefahren und die Hebung im übernehmenden Projekt committet. Ausnahmslos, auch bei einem Patch-Release ohne berührtes Artefakt (`RELEASE_PROCESS.md` Abschnitt 4.1 Schritte 1 und 2).
- [ ] **MUSS** Vor dem Release-Commit: Hauptdokument und Word-Fassung je Client Pack gebaut und im Erzeugnis nachgezählt. Keine Prüfung erreicht sie, weil sie unter `build/out/` liegen.
- [ ] **MUSS** Freigabe des Releases durch den Framework Owner in der Nachricht der signierten Marke dokumentiert (`RELEASE_PROCESS.md` Abschnitt 4.1 Schritt 4). Die Marke trägt die Unterschrift, deshalb setzt sie der Mensch. Keine Prüfung erreicht den Markentext.
- [ ] **MUSS** Nach dem Release-Commit: Release-Archiv aus der signierten Marke erzeugt, im Erzeugnis nachgezählt und samt Prüfsumme außerhalb des Repositoriums abgelegt; Mitteilung mit Migrationshinweisen und betroffenen Overlay-Feldern an die übernehmenden Projekte (`.koolie/core/governance/RELEASE_PROCESS.md` Abschnitt 4.1 Schritte 5 bis 7).
- [ ] **MUSS** (ab 1.0.0) Alle Core-Module, Skills und Packs tragen einen Status oberhalb von `entwurf`; die Statuszeile jedes Modulträgers setzt Prüfung 47 durch.
- [ ] **MUSS** (ab 1.0.0) Kein Decision Record in `.koolie/core/governance/DECISION_LOG.md` trägt den Status `entschieden (Vorschlag)`.
- [ ] **MUSS** (ab 1.0.0) Übernahme in mindestens ein zweites Projekt nach `.koolie/core/checklists/10-project-adoption.md` nachgewiesen.

## Abbruch- und Eskalationskriterien

Fehlschläge im Testkatalog, offene Konsistenzbefunde oder Projektneutralitätsverstöße stoppen das Release (E4). Sicherheitsrelevante Befunde folgen `.koolie/core/governance/INCIDENT_HANDLING.md`.

## Ergebnis und Nachweis

Release-Eintrag im `.koolie/core/CHANGELOG.md`, Testkatalog-Protokoll, abgelegte Checkliste und Archivreferenz bilden zusammen den Audit-Nachweis des Releases.
