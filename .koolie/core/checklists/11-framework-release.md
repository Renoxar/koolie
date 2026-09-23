# Checkliste FW-CL-11 – Framework-Release

| Attribut | Wert |
|---|---|
| ID | `FW-CL-11` |
| Version | `0.4.0` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Wann | vor jedem Framework-Release (auch Patch-Releases) |
| Wer | Framework Owner; Zuarbeit Modul-Owner |
| Dauer (Richtwert, Erläuterung) | abhängig vom Änderungsumfang – keine verbindlichen Aufwände |
| Nachweis | Release-Eintrag in `.koolie/core/CHANGELOG.md`; abgelegte Checkliste; Testkatalog-Protokoll |

## Zweck

Sichert, dass ein Release konsistent, projektneutral, getestet und für übernehmende Projekte nachvollziehbar ist (`.koolie/core/governance/RELEASE_PROCESS.md`).

Die mit **(ab 1.0.0, D-11)** gekennzeichneten Prüfpunkte gelten erst für das Release 1.0.0 und darüber; sie bilden die Kriterien aus Decision Record D-11 ab (`CR-2026-001`). Pilot, Onboarding und organisatorische Freigabe sind **keine** Prüfpunkte dieser Checkliste – sie liegen projektseitig (`.koolie/core/checklists/10-project-adoption.md`).

## Prüfpunkte

### Inhalt und Konsistenz

- [ ] **MUSS** Alle für das Release vorgesehenen Änderungsanträge sind abgeschlossen oder ausdrücklich verschoben (`.koolie/core/governance/DECISION_LOG.md` aktualisiert).
- [ ] **MUSS** Konsistenz Core ↔ Laufzeitfassung geprüft: `.koolie/core/framework/core/*` gegen die Wurzel-Anweisungsdatei und die Regelablage `00-*, 10-*, 15-*` **jedes Client Packs** (Stichproben je geändertem Modul; keine widersprüchlichen Anweisungen).
- [ ] **MUSS** Skills konsistent zum Skill-Standard (`.koolie/core/framework/core/08-skill-conventions.md`); Versionen, Status und CHANGELOG je geändertem Skill gepflegt; Deprecations mit Nachfolger dokumentiert.
- [ ] **MUSS** Version je geänderter Checkliste und je geändertem Prompt gepflegt (Metadatentabelle, Semantic Versioning wie in `.koolie/core/governance/RELEASE_PROCESS.md` Abschnitt 1). Bis 0.12.0 galt diese Pflicht nur für Skills; deshalb standen elf Checklisten und zwölf Prompts über zwölf Releases unverändert auf `0.1.0`, obwohl sie sich geändert hatten (`FW-VN-01`). **Ein reiner Statuswechsel ist keine Änderung im Sinne dieses Prüfpunkts** (`.koolie/core/framework/core/01-governance.md` Abschnitt 5 Punkt 5, D-106): Er ändert keine Anweisung, und eine angehobene Version behauptete eine Inhaltsänderung, die es nicht gibt.
- [ ] **MUSS** Prioritätshierarchie unverändert oder Änderung begründet und in `.koolie/core/governance/PRIORITY_HIERARCHY.md` nachgezogen.
- [ ] **SOLL** Templates, Checklisten und Entscheidungsbäume gegen geänderte Module abgeglichen (Querverweise, Begriffe).

### Projektneutralität

- [ ] **MUSS** `python3 .koolie/core/tests/scripts/validate-framework.py` ohne Fehler; Warnungen bewertet.
- [ ] **MUSS** `.koolie/project-overlay/forbidden-terms.txt` ist im Release leer (projektlokale Sperrlisten verbleiben in den Projekten).
- [ ] **MUSS** Manuelle Stichprobe auf projekt-, kunden- oder personenspezifische Inhalte in geänderten Dateien (zusätzlich zur automatischen Prüfung).
- [ ] **MUSS** Beispiele sind synthetisch gekennzeichnet; Platzhalterregister aktuell.

### Produktstand der KI-Client

- [ ] **MUSS** Aktualitätsprüfung gegen die offizielle Clientdokumentation durchgeführt (Changelog des Produkts gesichtet; betroffene `[DOK]`-Aussagen und Belegzellen mit `BELEG OFFEN` aktualisiert; Quellenliste im Hauptdokument nachgezogen).
- [ ] **MUSS** Produktänderungen mit Regelwirkung (neue Berechtigungen, geänderte Pfade, entfallene Mechanismen) sind als Änderungsanträge behandelt (`.koolie/core/governance/RELEASE_PROCESS.md`, Abschnitt Produktbeobachtung).

### Tests

- [ ] **MUSS** Testkatalog vollständig ausgeführt (`.koolie/core/tests/TEST_CATALOG.md`): Konsistenz-, Positiv-, Negativ-, Datenschutz-, Prompt-Injection-, Scope-, Fehlende-Informationen-, Zugriffs- und Regressionstests; Ergebnisse je Test-ID dokumentiert.
- [ ] **MUSS** (ab 1.0.0, D-11) Kein Testfall des Katalogs steht auf Ergebnisstatus `offen`; jeder trägt `bestanden`, `fehlgeschlagen (Referenz)` oder `nicht anwendbar (Begründung)`.
- [ ] **MUSS** Skill-Testfälle (`TESTS.md` je Skill) für alle geänderten Skills erneut ausgeführt.
- [ ] **MUSS** Hook- und Validierungsskripte laufen fehlerfrei (Selbsttest der Skripte).
- [ ] **MUSS** Jedes **Abnahmeprotokoll des Testkatalogs** trägt einen Abschnitt *Gegenzeichnung* ohne offenes `<TBD>` (**Prüfung 80**). 🔴 **Die Pflicht gilt ausschließlich für diese Protokolle** – Dateiname `JJJJ-MM-TT-FW-<Klasse>-<NN>.md` –, nicht für Arbeits- und Meßprotokolle (D-319, `CR-2026-127` E1). *Eine Gegenzeichnung bestätigt eine Abnahme; ein Meßprotokoll trägt seinen Beleg in sich.* ⚠️ **Ist keine zweite Rolle vorhanden, wird selbst gegengezeichnet und der Abschnitt weist das ausdrücklich als „Selbstgegenzeichnung“ aus** – die Zusage der zweiten Rolle ist damit zurückgenommen, nicht erfüllt.
- [ ] **SOLL** Mindestens ein vollständiger Durchlauf des Standardarbeitsablaufs auf dem Übungsrepository (M1 → M2 → M3 → M4) ohne Regelverstoß.

### Abschluss

- [ ] **MUSS** `.koolie/core/VERSION` nach Semantic Versioning erhöht; `.koolie/core/CHANGELOG.md` mit Änderungen, Migrationshinweisen für Overlays und bekannten Einschränkungen ergänzt.
- [ ] **MUSS** **Als letzter Eingriff in den Kern, vor dem Release-Commit:** Übernehmende Projekte gehoben – Kern aus dem **Arbeitsbaum** kopiert, beschränkt auf das Verfolgte (D-333), dann `install.py --update`, Overlay-Wert in **drei** Trägern nachgezogen, `validate-framework.py --strict-overlay` dort gefahren **und im übernehmenden Projekt committet** (D-343) – und die Bestandsliste `.koolie/core/governance/ADOPTION_REGISTRY.md` **vorher** auf den Zielstand fortgeschrieben (**Prüfung 82**). 🔴 **Ausnahmslos, auch bei einem Patch-Release, das kein ausgeliefertes Artefakt berührt** (D-330). ➡️ *Das Heben ist ein Lauf gegen eine fremde Installation und nicht die Fortschreibung einer Tabelle* – in `1.0.0` hat **es** zwei Prüfungen gefunden, die in jeder Installation rot waren, und kein Validatorlauf.
- [ ] **MUSS** **Vor dem Release-Commit:** Erzeugnisse der Lieferung gebaut – Hauptdokument und Word-Fassung **je Client Pack** – und **im Erzeugnis nachgezählt** (D-332). ⚠️ **Keine Prüfung erreicht sie:** Sie liegen unter `build/out/` und stehen in der `.gitignore` (`K-110`). *Die Word-Fassung blieb deshalb in `1.0.1` auf `v1.0.0` stehen, während der Dokumentkopf `1.0.1` trug.* 🟢 **MIT `1.2.0` HAT ER GEHALTEN** – und der Vorbedingungsdurchgang von `1.3.0` hat das Gegenteil gemeldet, weil er eine beschnittene Verzeichnisliste gelesen hat (D-345). ➡️ *Wer eine Liste beschneidet, mißt die Beschneidung.*
- [ ] **MUSS** **Nach dem Release-Commit:** Release-Archiv aus der signierten Marke erzeugt, **im Erzeugnis nachgezählt** und samt Prüfsumme außerhalb des Repositoriums abgelegt; Mitteilung mit Migrationshinweisen und betroffenen Overlay-Feldern an die übernehmenden Projekte. 🔴 **Das Archiv kann vor dem Commit nicht erzeugt werden** – es entsteht aus der Marke, und die sitzt auf dem Release-Commit. *Bis `1.0.1` stand das mit dem Heben in EINEM Prüfpunkt, und der war zum Zeitpunkt des Abhakens in seiner ersten Hälfte nie erfüllbar* (D-329). Ablauf: `.koolie/core/governance/RELEASE_PROCESS.md` Abschnitt 4.1.
- [ ] **MUSS** Freigabe des Releases durch den Framework Owner dokumentiert – **in der Nachricht der signierten Marke** (`RELEASE_PROCESS.md` Abschnitt 4.1 Schritt 4). 🔴 **Die Marke trägt die Unterschrift, der Release-Commit nicht** (D-334); deshalb setzt sie der Mensch und nicht ein Werkzeug. ⚠️ **Keine Prüfung erreicht den Markentext** – er liegt im Tag-Objekt, nicht im Arbeitsbaum (`K-111`).
- [ ] **MUSS** (ab 1.0.0, D-11) Alle Core-Module, Skills und Packs tragen einen Status oberhalb von `entwurf`. **Seit 0.51.0 hat dieser Prüfpunkt seinen Gegenstand:** Bis dahin führte keines der elf Core-Module überhaupt eine Statuszeile – ein Prüfpunkt ohne Gegenstand in der Checkliste, die 1.0.0 freigibt (`K-36`, D-105).
- [ ] **MUSS** (ab 1.0.0, D-11) Kein Decision Record in `.koolie/core/governance/DECISION_LOG.md` trägt den Status `entschieden (Vorschlag)`.
- [ ] **MUSS** (ab 1.0.0, D-11) Übernahme in mindestens ein zweites Projekt nach `.koolie/core/checklists/10-project-adoption.md` nachgewiesen.

## Abbruch- und Eskalationskriterien

Fehlschläge im Testkatalog, offene Konsistenzbefunde oder Projektneutralitätsverstöße stoppen das Release (E4). Sicherheitsrelevante Befunde folgen `.koolie/core/governance/INCIDENT_HANDLING.md`.

## Ergebnis und Nachweis

Release-Eintrag im `.koolie/core/CHANGELOG.md`, Testkatalog-Protokoll, abgelegte Checkliste und Archivreferenz bilden zusammen den Audit-Nachweis des Releases.
