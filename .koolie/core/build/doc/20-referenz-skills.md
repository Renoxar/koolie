# 20 Referenz-Skills

Die zwölf Referenz-Skills decken die geforderten Aufgaben ab und bilden zusammen den Standardweg jeder Änderung (verstehen → bewerten → planen → umsetzen → testen → prüfen → beschreiben). Jeder Skill ist projektneutral, verlangt Rückfragen bei Unklarheiten, macht Annahmen sichtbar, begrenzt den Scope, definiert Prüfungen, besitzt ein festes Ausgabeformat und bringt Positiv- wie Negativtestfälle mit (mindestens zwei beziehungsweise drei je Skill; gezählt am 2026-09-22: **je zwei Positiv- und drei bis fünf Negativtestfälle**, zusammen 72 Zellen).

**Alle zwölf stehen im Status `pilot`**, mit Versionen zwischen `0.1.3` und `0.1.7`, Owner `<FRAMEWORK_OWNER>`; sie durchlaufen den Lebenszyklus aus Kapitel 18. Die Versionen sind nicht kosmetisch: **Jede Anhebung hat einen Meßbefund als Anlass**, und ihre Testzellen sind an einer laufenden Sitzung abgenommen, nicht abgezeichnet – der Ergebnisstatus jeder Zelle nennt sein Protokoll und das gemessene Client Pack mit Produktstand.

**Ein dreizehnter Skill liegt außerhalb dieses Kapitels:** `role-re-ticket` gehört zum Role Pack Requirements Engineering (Ebene 6, Kap. 7.3) und wird nicht mit dem Kern installiert, sondern mit dem Pack aktiviert. Er bringt fünf Positiv- und zehn Negativtestfälle mit.

| ID | Skill (`/aufruf`) | Auftragspunkt | Modus | Werkzeuge | Trigger |
|---|---|---|---|---|---|
| FW-SK-001 | `fw-repo-analyze` | Repository analysieren | M1 | read, grep, glob | user, model |
| FW-SK-002 | `fw-code-explain` | Bestehenden Code erklären | M1 | read, grep, glob | user, model |
| FW-SK-003 | `fw-change-analyze` | Änderung fachlich und technisch analysieren | M1 | read, grep, glob | user |
| FW-SK-004 | `fw-plan` | Implementierungsplan erzeugen | M2 | read, grep, glob | user |
| FW-SK-005 | `fw-change-small` | Kleine Codeänderung umsetzen | M3 | read, grep, glob, edit, exec | user |
| FW-SK-006 | `fw-tests` | Unit Tests erstellen oder erweitern | M4 | read, grep, glob, edit, exec | user |
| FW-SK-007 | `fw-refactor` | Code refaktorieren | M3 | read, grep, glob, edit, exec | user |
| FW-SK-008 | `fw-error-analyze` | Fehler analysieren | M1 | read, grep, glob | user, model |
| FW-SK-009 | `fw-bugfix-prepare` | Bugfix vorbereiten | M2 | read, grep, glob | user |
| FW-SK-010 | `fw-review-support` | Code Review unterstützen | M1 | read, grep, glob, exec (nur lesende Git-Befehle) | user |
| FW-SK-011 | `fw-docs-update` | Dokumentation aktualisieren | M5 | read, grep, glob, edit | user |
| FW-SK-012 | `fw-mr-description` | Merge-Request-Beschreibung erstellen | M5 | read, grep, glob, exec (nur lesende Git-Befehle) | user |

Nachfolgend die normativen Skill-Dateien (SKILL.md) aller zwölf Skills. Die Begleitdateien (EXAMPLES.md mit synthetischen Positiv- und Negativbeispielen, TESTS.md mit den Testfällen, CHANGELOG.md) liegen je Skill im Repository; stellvertretend ist für FW-SK-001 der vollständige Satz wiedergegeben (Abschnitt 20.13).

## 20.1 FW-SK-001 `fw-repo-analyze`

{{EMBED:<SKILLS_DIR>/fw-repo-analyze/SKILL.md}}
## 20.2 FW-SK-002 `fw-code-explain`

{{EMBED:<SKILLS_DIR>/fw-code-explain/SKILL.md}}
## 20.3 FW-SK-003 `fw-change-analyze`

{{EMBED:<SKILLS_DIR>/fw-change-analyze/SKILL.md}}
## 20.4 FW-SK-004 `fw-plan`

{{EMBED:<SKILLS_DIR>/fw-plan/SKILL.md}}
## 20.5 FW-SK-005 `fw-change-small`

{{EMBED:<SKILLS_DIR>/fw-change-small/SKILL.md}}
## 20.6 FW-SK-006 `fw-tests`

{{EMBED:<SKILLS_DIR>/fw-tests/SKILL.md}}
## 20.7 FW-SK-007 `fw-refactor`

{{EMBED:<SKILLS_DIR>/fw-refactor/SKILL.md}}
## 20.8 FW-SK-008 `fw-error-analyze`

{{EMBED:<SKILLS_DIR>/fw-error-analyze/SKILL.md}}
## 20.9 FW-SK-009 `fw-bugfix-prepare`

{{EMBED:<SKILLS_DIR>/fw-bugfix-prepare/SKILL.md}}
## 20.10 FW-SK-010 `fw-review-support`

{{EMBED:<SKILLS_DIR>/fw-review-support/SKILL.md}}
## 20.11 FW-SK-011 `fw-docs-update`

{{EMBED:<SKILLS_DIR>/fw-docs-update/SKILL.md}}
## 20.12 FW-SK-012 `fw-mr-description`

{{EMBED:<SKILLS_DIR>/fw-mr-description/SKILL.md}}
## 20.13 Begleitdateien am Beispiel FW-SK-001 (vollständiger Satz)

{{EMBED:<SKILLS_DIR>/fw-repo-analyze/EXAMPLES.md}}
{{EMBED:<SKILLS_DIR>/fw-repo-analyze/TESTS.md}}
{{EMBED:<SKILLS_DIR>/fw-repo-analyze/CHANGELOG.md}}