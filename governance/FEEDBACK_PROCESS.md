# Feedbackprozess

| Attribut | Wert |
|---|---|
| ID | `FW-GOV-FB` |
| Version | `0.1.0` |
| Status | `entwurf` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |

## 1. Zweck und Grundsatz (normativ)

Feedback ist der Hauptsensor des Frameworks: Regelungslücken, unpraktikable Regeln, Skill-Schwächen und gute Muster erreichen den Framework Owner strukturiert statt als Flurfunk oder stille Umgehung. Grundsatz: **Melden ist immer richtig; Umgehen nie.** Feedback bewertet Regeln und Werkzeuge, nicht Personen.

## 2. Kanäle und Erfassung (normativ)

| Quelle | Weg | Mindestinhalt |
|---|---|---|
| Entwicklerinnen und Entwickler, Reviewer | Feedback-Eintrag im vom Projekt festgelegten Kanal (`<TBD: Feedbackkanal, z. B. Ticket-Typ im <ISSUE_TRACKER>>`) | Betroffenes Artefakt (Pfad, Version), Situation, Problem oder Vorschlag, Häufigkeit |
| Systematische Review-Befunde (RV) | Meldung durch Reviewer gemäß `framework/core/07-review-rules.md` Abschnitt 4 | Muster, Beispiele (bereinigt), betroffene Skills/Regeln |
| Onboarding | Sammel-Feedback der Mentorinnen und Mentoren nach jedem Durchlauf | Stolperstellen je Modul, Materialmängel |
| Pilot | Metriken und Befragungen (`pilot/METRICS.md`; Befragungen freiwillig und anonym auswertbar) | aggregierte Signale |
| Eskalationen E0–E4 | automatisch als Feedback gewertet, wenn Ursache eine Regel- oder Skill-Schwäche ist | Eskalationsgrund |

Beispiele in Feedback-Einträgen sind bereinigt (Kontextklassenregeln gelten auch hier); Personen werden nicht genannt.

## 3. Auswertung (normativ)

1. Der Framework Owner sichtet Feedback laufend (Hotfix-würdig?) und systematisch im Review-Zyklus (`RELEASE_PROCESS.md` Abschnitt 2).
2. Jeder Eintrag erhält einen Status: `angenommen (Änderungsantrag CR-…)`, `beobachten`, `abgelehnt mit Begründung`. Rückmeldung an die meldende Rolle SOLL erfolgen.
3. Kennzahlen des Prozesses selbst (Einträge, Durchlaufzeit, Umsetzungsquote) fließen in die Pilotauswertung und den Lessons-Learned-Punkt.

## 4. Erläuterung

Ein Framework, das nur Regeln sendet, veraltet in Monaten. Die niedrigste Hürde zählt: Ein Zwei-Zeilen-Eintrag „Skill fw-tests schlägt bei parametrisierten Tests unpassende Benennung vor, Beispiel anbei" ist wertvoller als eine perfekte Analyse, die nie geschrieben wird.
