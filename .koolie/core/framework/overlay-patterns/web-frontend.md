# Overlay-Muster „Web-Frontend“

| Attribut | Wert |
|---|---|
| ID | `FW-OVL-WEB-FRONTEND` |
| Name | `web-frontend` |
| Version | `0.1.0` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Baut auf | `general` |
| Im Dialog | für Web-Frontends mit npm, baut auf general auf |
| Gewählt über | `python .koolie/core/install.py --overlay web-frontend` – **nur bei der Erstinstallation** |
| Wirkung | alles aus `general`, dazu weitere Sperrwerte für diesen Projekttyp |

## Zweck

Für Web-Frontends, die mit npm, pnpm oder Yarn gebaut werden.

Gewählt wird genau ein Muster. Dieses Muster baut auf `general` auf: Es übernimmt dessen Werte
und Dokumente und ergänzt Werte, die für diesen Projekttyp ohne weitere Kenntnis des Projekts
sicher sind. Es gilt derselbe Grundsatz wie dort: **Das Muster sperrt, es gibt nichts frei.**
Jeder Wert steht ausschließlich in einem `deny`-Eintrag; passt einer nicht, sperrt er eine
Datei, die es im Projekt nicht gibt.

## Die Werte

Zusätzlich zu den Werten von `general`. Gelesen wird die Tabelle wie bei `general`.

| Platzhalter | Werte | Warum ohne Kenntnis des Projekts sicher |
|---|---|---|
| `<QUALITY_GATE_CONFIG_PATHS>` | `.husky/**`, `.lintstagedrc*`, `lint-staged.config.*`, `commitlint.config.*`, `.commitlintrc*`, `.size-limit*`, `lighthouserc.*`, `.lighthouserc*` | Prüfungen vor dem Commit, Commit-Regeln und Grenzen für Paketgröße und Seitenleistung sind Qualitätsschranken. `package.json` bleibt offen, weil es auch Abhängigkeiten trägt |
| `<EXCLUDED_PATHS>` | `**/.env.local`, `**/.env.*.local`, `**/.npmrc` | Lokale Umgebungsdateien und `.npmrc` tragen oft Zugangsdaten für Dienste und Paketquellen (K3) |

Wie die Werte in Overlay, Laufzeitfassung und Berechtigungsdatei kommen und was danach dem
Projekt gehört, steht in `general.md`. Eigene Dokumente bringt dieses Muster nicht mit.

## Änderungsverlauf

| Version | Datum | Änderung |
|---|---|---|
| `0.1.0` | 2026-10-06 | Erstfassung |
