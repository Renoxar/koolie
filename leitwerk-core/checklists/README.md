# Checklisten

Operative Prüf- und Arbeitslisten des Frameworks. Checklisten sind normative Kurzform der Core-Regeln für einen konkreten Moment im Arbeitsablauf; bei Widerspruch gilt das jeweilige Core-Modul. Prüfpunkte tragen die Verbindlichkeit **MUSS** oder **SOLL**; die Nachweisführung steht je Liste im Kopf.

| ID | Datei | Wann | Wer |
|---|---|---|---|
| FW-CL-01 | `01-preflight.md` | vor jeder Devin-Aufgabe | Bearbeiterin oder Bearbeiter |
| FW-CL-02 | `02-privacy-context.md` | im Preflight und vor jeder Kontextbereitstellung | Bearbeiterin oder Bearbeiter; Freigaben `<APPROVAL_ROLE>` / `<DATA_PROTECTION_CONTACT>` |
| FW-CL-03 | `03-before-code-change.md` | vor dem ersten Schreib- oder Ausführungsschritt (M3/M4/M5) | Bearbeiterin oder Bearbeiter |
| FW-CL-04 | `04-review-ai-code.md` | Selbstreview vor Commit; unabhängiges Review im Merge Request | Bearbeiter und Reviewer |
| FW-CL-05 | `05-testing.md` | nach Testerstellung; vor Merge Requests mit Logikänderung | Bearbeiter; Reviewer (RV4) |
| FW-CL-06 | `06-security.md` | bei R3/R10/R11-Bezug; ergänzend bei Stufe hoch | Bearbeiter; `<SECURITY_CONTACT>` |
| FW-CL-07 | `07-new-dependency.md` | vor Einführung neuer Abhängigkeiten oder Major-Updates | Mensch (nie Devin); Freigaben `<APPROVAL_ROLE>` / `<SECURITY_CONTACT>` |
| FW-CL-08 | `08-merge-request.md` | vor Erstellen und vor Mergen eines Merge Requests | Bearbeiter; Reviewer und freigebende Rollen |
| FW-CL-09 | `09-onboarding.md` | während des Onboardings bis zur Freigabe | Mentorin oder Mentor mit der oder dem Neuen |
| FW-CL-10 | `10-project-adoption.md` | Übernahme in ein neues Projekt, vor Overlay-Aktivierung | Overlay Owner mit Framework Owner |
| FW-CL-11 | `11-framework-release.md` | vor jedem Framework-Release | Framework Owner |

## Verwendung

1. Die Liste wird zum genannten Zeitpunkt vollständig durchgegangen; nicht zutreffende Punkte werden als „n. z." markiert, nicht übersprungen.
2. Unerfüllte MUSS-Punkte stoppen den jeweiligen Schritt; die Abbruch- und Eskalationskriterien der Liste verweisen auf `leitwerk-core/framework/core/10-error-escalation.md`.
3. Der Nachweis erfolgt an der im Kopf der Liste genannten Stelle (Ergebnisbericht, Merge Request, Protokoll) – Checklisten werden nicht als Kopien im Repository abgelegt.
4. Projekte KÖNNEN Punkte ergänzen (Verschärfung über das Overlay), DÜRFEN aber keine MUSS-Punkte entfernen.

## Pflege

Checklisten sind versioniert (Metadatentabelle) und folgen dem Framework-Release-Prozess. Verbesserungsvorschläge laufen über `leitwerk-core/governance/FEEDBACK_PROCESS.md`.
