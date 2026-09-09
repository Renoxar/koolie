# Ausnahmeprozess

| Attribut | Wert |
|---|---|
| ID | `FW-GOV-EXC` |
| Version | `0.1.0` |
| Status | `entwurf` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |

## 1. Geltung (normativ)

1. Ausnahmen sind befristete, begründete, kompensierte Abweichungen von MUSS-Regeln des Frameworks oder eines Overlays.
2. **Nicht ausnahmefähig sind:** die Delegationsverbote V1–V12, die K3-Definition und ihre Bereitstellungsverbote, das Verbot des Bypass-Modus außerhalb dieses Prozesses sowie Ebene-1/2-Vorgaben (Gesetz, Organisation) – Letztere können nur ihre Urheber ändern.
3. SOLL-Regeln benötigen keine Ausnahme, sondern eine dokumentierte Begründung am Ort der Abweichung.

## 2. Verfahren (normativ)

| Schritt | Inhalt | Verantwortung |
|---|---|---|
| 1 Antrag | Regel (Modul, Abschnitt), gewünschte Abweichung, Grund, Dauer, kompensierende Maßnahme, Risikoeinschätzung | antragstellende Rolle |
| 2 Prüfung | Risiko und Kompensation bewerten; bei Sicherheits-/Datenschutzbezug `<SECURITY_CONTACT>` / `<DATA_PROTECTION_CONTACT>` einbeziehen | genehmigende Rolle |
| 3 Genehmigung | Core-Regeln: Framework Owner. Overlay-Regeln: Overlay Owner (`<APPROVAL_ROLE>`). Beide schriftlich, mit Befristung (Datum oder Ereignis) | laut RACI |
| 4 Registrierung | Eintrag im Ausnahmeregister des Projekts (`project-overlay/exceptions/EXCEPTIONS.md`); framework-weite Ausnahmen zusätzlich im Decision Log | antragstellende Rolle |
| 5 Überprüfung | Jede Ausnahme wird spätestens zum Befristungsende und bei jedem Overlay-/Framework-Review geprüft: verlängern (neuer Antrag), in eine Regeländerung überführen (Änderungsantrag) oder beenden | genehmigende Rolle |

## 3. Grundsätze (normativ)

1. Eine Ausnahme ohne Befristung oder ohne kompensierende Maßnahme ist ungültig.
2. Häufen sich gleichartige Ausnahmen, ist das ein Regelmangel: Der Owner MUSS einen Änderungsantrag anstoßen, statt weiter zu genehmigen (Lessons Learned).
3. Devin wird über aktive Ausnahmen ausschließlich über die versionierten Regeldateien informiert (Overlay-Abschnitt 18 beziehungsweise angepasste Laufzeitregel) – nie über mündliche „gilt heute nicht"-Anweisungen.
4. Auditierbarkeit: Register, Genehmigung und Ablauf jeder Ausnahme sind jederzeit nachweisbar.
