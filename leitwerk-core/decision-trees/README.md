# Entscheidungsbäume

Sechs operative Entscheidungshilfen des Frameworks. Jeder Baum besteht aus einer normativen Textbeschreibung (maßgeblich) und einem Mermaid-Diagramm (Veranschaulichung). Bei Abweichungen gilt der Text; beide werden gemeinsam gepflegt. Die Diagramme sind syntaktisch validiert (`python3 leitwerk-core/tests/scripts/validate-framework.py --mermaid`).

| Nr. | Datei | Frage | Wichtigste Quelle |
|---|---|---|---|
| 1 | `01-context-allowed.md` | Darf dieser Inhalt als Kontext verwendet werden? | `leitwerk-core/framework/core/02-privacy.md` |
| 2 | `02-may-devin-do-task.md` | Darf der KI-Client diese Aufgabe bearbeiten? | `leitwerk-core/framework/core/09-risk-model.md` |
| 3 | `03-analyze-or-modify.md` | Muss der KI-Client nur analysieren oder darf er ändern? | `leitwerk-core/framework/core/05-working-model.md` |
| 4 | `04-required-review.md` | Welche menschliche Prüfung ist erforderlich? | `leitwerk-core/framework/core/07-review-rules.md`, `09-risk-model.md` |
| 5 | `05-stop-or-escalate.md` | Wann muss abgebrochen oder eskaliert werden? | `leitwerk-core/framework/core/10-error-escalation.md` |
| 6 | `06-rule-placement.md` | Wohin gehört eine Regel? | `leitwerk-core/framework/core/00-principles.md` (P10), `leitwerk-core/governance/PRIORITY_HIERARCHY.md` |

Verwendung: Bäume 1–3 gehören zum Preflight (`leitwerk-core/checklists/01-preflight.md`), Baum 4 zum Review, Baum 5 gilt während jeder Sitzung, Baum 6 bei der Pflege des Frameworks und der Overlays.
