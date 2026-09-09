# Framework Core 01 – Governance-Grundsätze

| Attribut | Wert |
|---|---|
| Modul-ID | FW-CORE-01 |
| Ebene | 1 – Framework Core |
| Verbindlichkeit | normativ |
| Owner | `<FRAMEWORK_OWNER>` |
| Version | 0.1.0 |

## 1. Gegenstand und Geltung (normativ)

1. Das Framework regelt den Einsatz von Devin Desktop (und strukturell weiterer KI-gestützter Entwicklungswerkzeuge) in Softwareentwicklungsprojekten. Es gilt für alle Personen, die im Geltungsbereich eines Project Overlays mit Devin arbeiten.
2. Das Framework ergänzt bestehende Entwicklungs-, Review- und Freigabeprozesse. Es ersetzt sie nicht und hat im Konfliktfall keinen Vorrang vor rechtlichen, regulatorischen oder organisationsweiten Vorgaben (`devin-core-framework/governance/PRIORITY_HIERARCHY.md`).
3. Ohne ein freigegebenes Project Overlay (Status `aktiv` im Overlay-Steckbrief) DARF Devin in einem Projekt NICHT produktiv eingesetzt werden; zulässig sind nur Onboarding-Übungen auf synthetischen Übungsrepositorys.

## 2. Rollen des Frameworks (normativ)

| Rolle | Verantwortung | Besetzung |
|---|---|---|
| Framework Owner | Gesamtverantwortung für Core, Release, Prioritätshierarchie, Testkatalog, Produktbeobachtung | `<FRAMEWORK_OWNER>` (generische Rolle, keine Person) |
| Modul-Owner | Fachliche und technische Verantwortung für ein Role Pack, Technology Pack oder eine Skill-Gruppe | je Modul im `devin-core-framework/OWNERS.md` |
| Project Overlay Owner | Pflege und Freigabe des Overlays eines Projekts | `<APPROVAL_ROLE>` des Projekts |
| Security-Kontakt | Sicherheitsfreigaben, Vorfallbehandlung | `<SECURITY_CONTACT>` |
| Datenschutzkontakt | Datenschutzfreigaben, Prüfung von Kontextklassen | `<DATA_PROTECTION_CONTACT>` |
| Mentorin oder Mentor | Begleitung des Onboardings, Freigabe zur selbstständigen Nutzung | vom Projekt benannt |
| Anwenderin oder Anwender | Einhaltung der Regeln, Meldung von Abweichungen, Feedback | alle Entwicklerinnen und Entwickler |

Die detaillierte RACI-Zuordnung liegt in `devin-core-framework/governance/RACI.md`.

## 3. Änderungsgrundsätze (normativ)

1. Änderungen am Framework Core erfolgen ausschließlich über Änderungsanträge (`devin-core-framework/governance/CHANGE_REQUEST_TEMPLATE.md`) und Releases (`devin-core-framework/governance/RELEASE_PROCESS.md`).
2. Änderungen am Project Overlay erfolgen über den Prozess des Projekts, MÜSSEN aber die Validierung (`devin-core-framework/tests/scripts/validate-framework.py`) bestehen und DÜRFEN NICHT Core-Dateien verändern.
3. Jede Änderung ist im `devin-core-framework/CHANGELOG.md` (Framework) beziehungsweise im Overlay-Änderungsverlauf dokumentiert.
4. Skills durchlaufen den Lebenszyklus `entwurf → pilot → aktiv → veraltet → zurückgezogen` (`08-skill-conventions.md`).

## 4. Auditierbarkeit (normativ)

Für jeden Zeitpunkt MUSS nachvollziehbar sein: welche Framework-Version, welches Overlay (Version), welche Skills (Version) und welche Berechtigungskonfiguration galten. Dies wird erreicht durch Versionierung im Repository, `devin-core-framework/VERSION`-Datei, Overlay-Steckbrief mit Version und den Devin-Nutzungsvermerk je Merge Request.
