# 20 Referenz-Skills

Die dreizehn Referenz-Skills decken die geforderten Aufgaben ab und bilden zusammen den Standardweg jeder Änderung (verstehen → bewerten → planen → umsetzen → testen → prüfen → beschreiben). Jeder Skill ist projektneutral, verlangt Rückfragen bei Unklarheiten, macht Annahmen sichtbar, begrenzt den Scope, definiert Prüfungen, besitzt ein festes Ausgabeformat und bringt Positiv- wie Negativtestfälle mit: mindestens zwei Positiv- und drei Negativtestfälle je Skill.

Alle dreizehn stehen im Status `pilot`, Owner `<FRAMEWORK_OWNER>`; sie durchlaufen den Lebenszyklus aus Kapitel 18, und ihre Versionen stehen in der Metadatentabelle jeder SKILL.md. Ihre Testzellen werden in einer laufenden Sitzung abgenommen; der Ergebnisstatus jeder Zelle nennt Protokoll, Client Pack und Produktstand.

Ein vierzehnter Skill liegt außerhalb dieses Kapitels: `koolie-ticket` gehört zum Role Pack Requirements Engineering (Ebene 6, Kap. 7.3) und wird nicht mit dem Kern installiert, sondern mit dem Pack aktiviert. Er bringt fünf Positiv- und zehn Negativtestfälle mit.

| ID | Skill (`/aufruf`) | Auftragspunkt | Modus | Werkzeuge | Trigger |
|---|---|---|---|---|---|
| FW-SK-001 | `koolie-repo-analyze` | Repository analysieren | M1 | read, grep, glob | user, model |
| FW-SK-002 | `koolie-code-explain` | Bestehenden Code erklären | M1 | read, grep, glob | user, model |
| FW-SK-003 | `koolie-change-analyze` | Änderung fachlich und technisch analysieren | M1 | read, grep, glob | user, model |
| FW-SK-004 | `koolie-plan` | Implementierungsplan erzeugen | M2 | read, grep, glob | user, model |
| FW-SK-005 | `koolie-change-small` | Kleine Codeänderung umsetzen | M3 | read, grep, glob, edit, exec | user |
| FW-SK-006 | `koolie-tests` | Unit Tests erstellen oder erweitern | M4 | read, grep, glob, edit, exec | user |
| FW-SK-007 | `koolie-refactor` | Code refaktorieren | M3 | read, grep, glob, edit, exec | user |
| FW-SK-008 | `koolie-error-analyze` | Fehler analysieren | M1 | read, grep, glob | user, model |
| FW-SK-009 | `koolie-bugfix-prepare` | Bugfix vorbereiten | M2 | read, grep, glob | user, model |
| FW-SK-010 | `koolie-review-support` | Code Review unterstützen | M1 | read, grep, glob, exec (nur lesende Git-Befehle) | user |
| FW-SK-011 | `koolie-docs-update` | Dokumentation aktualisieren | M5 | read, grep, glob, edit | user |
| FW-SK-012 | `koolie-mr-description` | Merge-Request-Beschreibung erstellen | M5 | read, grep, glob, exec (nur lesende Git-Befehle) | user |
| FW-SK-013 | `koolie-overlay-pflege` | Entscheidungen in das Overlay eintragen (Einrichtung, Framework-Update, Eintrag) | M6 | read, grep, glob, edit, exec (Prüfbefehle, lesende Git-Befehle) | user |

Nachfolgend die normativen Skill-Dateien (SKILL.md) aller dreizehn Skills. Die Begleitdateien (EXAMPLES.md mit synthetischen Positiv- und Negativbeispielen, TESTS.md mit den Testfällen, CHANGELOG.md) liegen je Skill im Repository; stellvertretend ist für FW-SK-001 der vollständige Satz wiedergegeben (Abschnitt 20.14).

## 20.1 FW-SK-001 `koolie-repo-analyze`

{{EMBED:<SKILLS_DIR>/koolie-repo-analyze/SKILL.md}}
## 20.2 FW-SK-002 `koolie-code-explain`

{{EMBED:<SKILLS_DIR>/koolie-code-explain/SKILL.md}}
## 20.3 FW-SK-003 `koolie-change-analyze`

{{EMBED:<SKILLS_DIR>/koolie-change-analyze/SKILL.md}}
## 20.4 FW-SK-004 `koolie-plan`

{{EMBED:<SKILLS_DIR>/koolie-plan/SKILL.md}}
## 20.5 FW-SK-005 `koolie-change-small`

{{EMBED:<SKILLS_DIR>/koolie-change-small/SKILL.md}}
## 20.6 FW-SK-006 `koolie-tests`

{{EMBED:<SKILLS_DIR>/koolie-tests/SKILL.md}}
## 20.7 FW-SK-007 `koolie-refactor`

{{EMBED:<SKILLS_DIR>/koolie-refactor/SKILL.md}}
## 20.8 FW-SK-008 `koolie-error-analyze`

{{EMBED:<SKILLS_DIR>/koolie-error-analyze/SKILL.md}}
## 20.9 FW-SK-009 `koolie-bugfix-prepare`

{{EMBED:<SKILLS_DIR>/koolie-bugfix-prepare/SKILL.md}}
## 20.10 FW-SK-010 `koolie-review-support`

{{EMBED:<SKILLS_DIR>/koolie-review-support/SKILL.md}}
## 20.11 FW-SK-011 `koolie-docs-update`

{{EMBED:<SKILLS_DIR>/koolie-docs-update/SKILL.md}}
## 20.12 FW-SK-012 `koolie-mr-description`

{{EMBED:<SKILLS_DIR>/koolie-mr-description/SKILL.md}}
## 20.13 FW-SK-013 `koolie-overlay-pflege`

{{EMBED:<SKILLS_DIR>/koolie-overlay-pflege/SKILL.md}}
## 20.14 Begleitdateien am Beispiel FW-SK-001 (vollständiger Satz)

{{EMBED:<SKILLS_DIR>/koolie-repo-analyze/EXAMPLES.md}}
{{EMBED:<SKILLS_DIR>/koolie-repo-analyze/TESTS.md}}
{{EMBED:<SKILLS_DIR>/koolie-repo-analyze/CHANGELOG.md}}