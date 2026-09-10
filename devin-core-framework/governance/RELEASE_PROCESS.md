# Betriebsmodell: Review-Zyklus, Versionierung, Release und Produktbeobachtung

| Attribut | Wert |
|---|---|
| ID | `FW-GOV-REL` |
| Version | `0.1.0` |
| Status | `entwurf` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |

## 1. Versionierung (normativ)

1. Das Framework folgt Semantic Versioning (`devin-core-framework/VERSION`, `devin-core-framework/CHANGELOG.md`): **MAJOR** bei Struktur- oder Hierarchieänderungen, die Overlays anpassen müssen; **MINOR** bei neuen Modulen, Skills oder Regeln ohne Overlay-Bruch; **PATCH** bei Korrekturen und Formulierungen.
2. Skills, Packs, Checklisten, Prompts und Overlays tragen eigene Versionen (Metadatentabellen) und referenzieren die kompatible Framework-Version.
3. Jede Auslieferung erfolgt als Release-Archiv mit Stand aus dem Framework-Repository; Projekte übernehmen nur Releases, keine Zwischenstände.

## 2. Review-Zyklus (normativ)

1. Regelmäßiger Review-Termin des Frameworks: `<TBD: Prüfzyklus, Vorschlag quartalsweise>` – Inhalte: offene Änderungsanträge, Feedback- und Lessons-Learned-Einträge, Vorfallauswertung, Metrik-Signale aus Piloten, Ergebnis der Produktbeobachtung.
2. Zwischen den Terminen sind Hotfix-Releases zulässig für: Sicherheits- oder Datenschutzlücken im Framework, gebrochene Devin-Mechanismen, fehlerhafte Skills mit Schadenspotenzial.

## 3. Änderungsanträge (normativ)

1. Jede Änderung an Core, Packs, Skills, Checklisten, Prompts, Bäumen oder Templates beginnt als Änderungsantrag (`CHANGE_REQUEST_TEMPLATE.md`) an den zuständigen Owner (RACI).
2. Der Owner prüft: Zuordnung nach Entscheidungsbaum 6, Verschärfungsprinzip, Auswirkungen auf Laufzeitfassungen, Test- und Dokumentationsbedarf.
3. Angenommene Anträge werden umgesetzt, validiert (`devin-core-framework/tests/scripts/validate-framework.py`), im Testkatalog abgedeckt und im Decision Log sowie `devin-core-framework/CHANGELOG.md` dokumentiert.

## 4. Release-Prozess (normativ)

1. Release-Vorbereitung nach `devin-core-framework/checklists/11-framework-release.md` (Konsistenz, Projektneutralität, Produktstand, Testkatalog).
2. Freigabe durch den Framework Owner; Archiv erzeugen; Version und Changelog veröffentlichen.
3. Kommunikation an alle übernehmenden Projekte mit Migrationshinweisen (betroffene Overlay-Felder, neue Pflichtprüfungen, deprecatete Skills).
4. Projekte übernehmen Releases über `devin-core-framework/docs/ADOPTION_GUIDE.md` Abschnitt „Aktualisierung"; der Framework Owner führt eine Bestandsliste der Projekte mit eingesetzter Version (Auditierbarkeit).

## 5. Freigabe und Deprecation von Skills (normativ)

Lebenszyklus und Kriterien: `devin-core-framework/framework/core/08-skill-conventions.md` Abschnitt 7. Ergänzend: Deprecation wird mindestens ein MINOR-Release vor der Zurückziehung angekündigt; die Hinweisdatei im Skill-Verzeichnis nennt Nachfolger und Migrationsweg; Projekte mit eigenen `prj-*`-Skills prüfen bei jedem Release die Kompatibilität.

## 6. Umgang mit Produktänderungen von Devin (normativ)

1. **Beobachtung:** Der Framework Owner sichtet im Review-Zyklus (und anlassbezogen) die offiziellen Quellen: Produkt-Changelog und Dokumentation von Devin Desktop. Quellenliste: Hauptdokument, Anhang „Quellen und Verifikationsbedarf".
2. **Bewertung:** Jede relevante Änderung wird klassifiziert: (a) kosmetisch – keine Aktion; (b) erweiternd – Chance, als Änderungsantrag bewerten; (c) brechend – betroffene `[DOK]`-Aussagen, Pfade, Berechtigungen oder Skills identifizieren.
3. **Reaktion auf brechende Änderungen:** Sofortmaßnahme kommunizieren (zum Beispiel betroffenen Mechanismus nicht nutzen), Änderungsantrag mit Priorität, gegebenenfalls Hotfix-Release; `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>`-Marker aktualisieren; Testkatalog-Klasse AK (Aktualität) erneut ausführen.
4. **Werkzeugwechsel:** Dank Tool Independence (P8) beschränkt sich ein Wechsel oder Parallelbetrieb eines anderen KI-Werkzeugs auf ein neues Client Pack (`devin-core-framework/clients/README.md`); die kanonischen Regeln in `devin-core-framework/framework/` bleiben unverändert. Vor dem Wechsel ist die Fähigkeitsmatrix des Zielclients auszuwerten. Ein solcher Schritt ist ein MAJOR-Release.

## 7. Behandlung von Sicherheitsvorfällen, Lessons Learned, Feedback, Ausnahmen (Verweise)

- Vorfälle: `INCIDENT_HANDLING.md` (Erfassung, Auswertung, Rückfluss in Regeln).
- Feedback: `FEEDBACK_PROCESS.md` (niederschwellig, ausgewertet im Review-Zyklus).
- Ausnahmen: `EXCEPTION_PROCESS.md` (befristet, kompensiert, registriert).
- Lessons Learned: fester Tagesordnungspunkt des Review-Zyklus; Ergebnisse fließen als Änderungsanträge ein und werden im Decision Log nachgewiesen.

## 8. Auditierbarkeit (normativ)

Nachweiskette je Zeitpunkt: Framework-Version (`devin-core-framework/VERSION`, Release-Archiv) → Overlay-Version (Overlay-Steckbrief) → Skill-Versionen (Metadaten) → Berechtigungsstand (Berechtigungsdatei im Repository-Verlauf) → Nutzung je Änderung (KI-Nutzungsvermerk im Merge Request) → Vorfälle und Ausnahmen (Register). Alle Nachweise liegen in versionierten Repositories oder im Merge-Request-System; gesonderte Schattenablagen sind unzulässig.
