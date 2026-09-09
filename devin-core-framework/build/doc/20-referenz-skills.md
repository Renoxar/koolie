# 20 Referenz-Skills

Die zwölf Referenz-Skills decken die geforderten Aufgaben ab und bilden zusammen den Standardweg jeder Änderung (verstehen → bewerten → planen → umsetzen → testen → prüfen → beschreiben). Jeder Skill ist projektneutral, verlangt Rückfragen bei Unklarheiten, macht Annahmen sichtbar, begrenzt den Scope, definiert Prüfungen, besitzt ein festes Ausgabeformat und bringt Positiv- wie Negativtestfälle mit (mindestens zwei beziehungsweise drei je Skill). Alle Skills liegen im Status `entwurf` (Version 0.1.0, Owner `<FRAMEWORK_OWNER>`) und durchlaufen den Lebenszyklus aus Kapitel 18.

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

{{EMBED:.devin/skills/fw-repo-analyze/SKILL.md}}

## 20.2 FW-SK-002 `fw-code-explain`

{{EMBED:.devin/skills/fw-code-explain/SKILL.md}}

## 20.3 FW-SK-003 `fw-change-analyze`

{{EMBED:.devin/skills/fw-change-analyze/SKILL.md}}

## 20.4 FW-SK-004 `fw-plan`

{{EMBED:.devin/skills/fw-plan/SKILL.md}}

## 20.5 FW-SK-005 `fw-change-small`

{{EMBED:.devin/skills/fw-change-small/SKILL.md}}

## 20.6 FW-SK-006 `fw-tests`

{{EMBED:.devin/skills/fw-tests/SKILL.md}}

## 20.7 FW-SK-007 `fw-refactor`

{{EMBED:.devin/skills/fw-refactor/SKILL.md}}

## 20.8 FW-SK-008 `fw-error-analyze`

{{EMBED:.devin/skills/fw-error-analyze/SKILL.md}}

## 20.9 FW-SK-009 `fw-bugfix-prepare`

{{EMBED:.devin/skills/fw-bugfix-prepare/SKILL.md}}

## 20.10 FW-SK-010 `fw-review-support`

{{EMBED:.devin/skills/fw-review-support/SKILL.md}}

## 20.11 FW-SK-011 `fw-docs-update`

{{EMBED:.devin/skills/fw-docs-update/SKILL.md}}

## 20.12 FW-SK-012 `fw-mr-description`

{{EMBED:.devin/skills/fw-mr-description/SKILL.md}}

## 20.13 Begleitdateien am Beispiel FW-SK-001 (vollständiger Satz)

{{EMBED:.devin/skills/fw-repo-analyze/EXAMPLES.md}}

{{EMBED:.devin/skills/fw-repo-analyze/TESTS.md}}

{{EMBED:.devin/skills/fw-repo-analyze/CHANGELOG.md}}
