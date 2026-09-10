# Pilotkonzept

| Attribut | Wert |
|---|---|
| ID | `FW-PILOT` |
| Version | `0.1.1` |
| Status | `entwurf` |
| Owner (Rolle) | Projektleitung des Pilotprojekts mit `<FRAMEWORK_OWNER>` |
| Metriken | `METRICS.md` |

## 1. Ziel und Grundsätze (normativ)

1. Der Pilot prüft unter realen Bedingungen, ob das Framework sicheren, effizienten und akzeptierten KI-Einsatz ermöglicht – und liefert die Entscheidungsgrundlage für Fortführung, Anpassung oder Beendigung. Er ist ein Experiment mit Abbruchrecht, kein Rollout mit Umweg.
2. Produktivität, Ergebnisqualität, Sicherheit und Nutzerakzeptanz werden **gemeinsam** betrachtet; einzelne Metriken erlauben keine belastbare Aussage über den Gesamtnutzen (Wechselwirkungen: schnellere Bearbeitung bei steigendem Review-Aufwand ist kein Gewinn).
3. Befragungen sind freiwillig; Auswertung erfolgt aggregiert und nicht personenbeziehbar; Metriken dienen der Framework- und Prozessbewertung, niemals der Leistungsbewertung von Personen (V7). Diese Zusage steht in der Pilot-Kommunikation an das Team.

## 2. Aufbau (normativ, Parameter projektspezifisch)

| Element | Festlegung | Parameter |
|---|---|---|
| Referenzbasis | Vor dem Start werden die Vergleichswerte der Metriken aus dem Bestandsprozess erhoben (gleiche Definitionen, Zeitraum `<TBD: Referenzzeitraum>`); wo keine Historie existiert, wird die Basis in den ersten Pilotwochen ohne KI-Anteil miterhoben | `<TBD>` |
| Pilotgruppe | `<TBD: Anzahl>` Entwicklerinnen und Entwickler nach abgeschlossenem Onboarding; freiwillige Teilnahme; Mischung aus Erfahrungsstufen SOLL | `<TBD>` |
| Pilotzeitraum | `<PILOT_DURATION>` (konfigurierbar; lang genug für mindestens zwei Review-Punkte) | `<PILOT_DURATION>` |
| Ausgewählte Anwendungsfälle | Start mit den Skills FW-SK-001…004, 006, 008, 012 (Analyse, Plan, Tests, Fehleranalyse, MR-Texte) und `fw-change-small` auf Kontrollstufe niedrig/mittel; Stufe hoch bleibt im Pilot außen vor, sofern der Overlay Owner nichts anderes freigibt | `<TBD: Fallliste>` |
| Vergleichbarkeit von Aufgaben | Aufgaben werden bei der Planung mit Kategorie (Fehlerbehebung/Feature/Refactoring/Doku), Kontrollstufe und Größenklasse etikettiert; verglichen wird nur innerhalb gleicher Etiketten; keine künstlichen A/B-Zuteilungen gegen den Teamfluss | `<TBD: Etikettierung im <ISSUE_TRACKER>>` |
| Erhebung | Automatisch aus `<ISSUE_TRACKER>`/`<CI_CD_PLATFORM>`/MR-Vermerken, wo möglich; manuelle Angaben minimal (Selbsteinschätzungskategorien im Nutzungsvermerk) | `METRICS.md` |
| Review-Punkte | Regelmäßig (`<TBD: z. B. alle zwei Wochen>`): Metrikdurchsprache, Feedback, Vorfälle, Anpassungsentscheidungen; Ergebnisse an `<FRAMEWORK_OWNER>` | `<TBD>` |
| Kommunikation | Teaminfo zu Zweck, Freiwilligkeit, Datenumgang vor dem Start; Zwischenstände nach jedem Review-Punkt | `<TBD>` |

## 3. Abbruchkriterien (normativ)

Der Pilot wird unterbrochen und neu bewertet, wenn eines eintritt:

1. Sicherheits- oder Datenschutzvorfall der Stufe E3 mit Ursache im Framework oder Werkzeug (nicht in einem Einzelfehler, der durch Regeln aufgefangen wurde).
2. Wiederholte Umgehung zentraler Regeln trotz Nachsteuerung (Bypass-Nutzung, K3-Bereitstellungen).
3. Deutliche, anhaltende Verschlechterung der Qualitätssignale gegenüber der Referenzbasis (Fehlerquote, Wiedereröffnungen, Pipeline-Fehlschläge) über mehr als einen Review-Punkt.
4. Breite, begründete Ablehnung durch die Pilotgruppe (Akzeptanzsignale, Feedback) – Werkzeuge gegen das Team einzuführen ist kein Ziel des Frameworks.
5. Produktänderung, die zentrale Kontrollmechanismen bricht, ohne kurzfristige Abhilfe (Release-Prozess Abschnitt 6).

## 4. Entscheidung am Pilotende (normativ)

Auf Basis des Abschlussberichts (Metriken gegen Referenz, qualitative Auswertung, Vorfälle, Aufwand) entscheidet die Projektleitung mit `<FRAMEWORK_OWNER>` und den beteiligten Rollen: **Fortführung** (Rollout-Plan, Version 1.0.0-Pfad), **Anpassung** (gezielte Änderungsanträge, Pilotverlängerung) oder **Beendigung** (dokumentierte Gründe, Rückbau der Freigaben). Die Entscheidung samt Begründung geht in das Decision Log; kein Ergebnis wird durch Weglassen unbequemer Metriken geschönt.
