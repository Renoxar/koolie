# Änderungsantrag `CR-2026-159`

| Feld | Inhalt |
|---|---|
| Titel | Das zweite Befehlswerkzeug – und die Sperre, die es erst sichtbar machte |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-29 |
| Betroffene Artefakte | `clients/claude-code/manifest.json` (`permission_tools.exec`, `hook_tools.exec`), `CLIENT_PACK.md` (Zeilen `exec`, B3, B6); `tests/TEST_CATALOG.md` (`FW-ZA-07`, `FW-ZA-08`); `governance/DECISION_LOG.md`; `docs/ROADMAP.md`; `CHANGELOG.md`, `VERSION`; Protokoll `tests/protocols/2026-09-29-powershell.md` |
| Ebene laut Entscheidungsbaum 6 | Client Pack |
| Art | **Korrektur mit Migrationshinweis** für die Berechtigungsdatei von `claude-code`; PATCH-Release mit Kontingent |
| Dringlichkeit | vorgezogen mit D-467 |
| Status | 🟢 **entschieden am 2026-09-29** (E1 bis E4) |

---

## 1. Anlass

`K-70`, bestätigt beim Release `1.18.1`: Die Berechtigungsdatei von `claude-code` sperrt Befehle nur als `Bash(…)`, der Hook-Matcher kennt `PowerShell` nicht – und der Client bietet unter Windows ein eigenes PowerShell-Werkzeug an.

## 2. Vorprüfung

Dokumentation des Herstellers: Das Werkzeug heißt `PowerShell`, seine Regeln haben die Form der Bash-Regeln, verkettete Befehle werden zerlegt, der Hook bekommt `tool_input.command`; ob Leseverbote auch für PowerShell-Befehle gelten, ist nicht dokumentiert. Im Framework: `clientmap.py` und der Hook folgen den Werkzeuglisten des Manifests – ein zweiter Eintrag genügt. Der Hook erkannte `Get-Content .env` in einer nachgebauten Eingabe schon.

## 3. Vorlage zur Entscheidung

Vorgelegt am 2026-09-29 mit Empfehlung und Schätzung (8 bis 12 Läufe, 4 bis 7 USD); der Owner folgt der Empfehlung.

| # | Frage | Entscheidung | Preis |
|---|---|---|---|
| E1 | Weg | Gleichstellen: `PowerShell` in beide Werkzeuglisten des Manifests | Das Werkzeug wird angeboten, wo es vorher ausgeblendet war |
| E2 | Regelform und Cmdlets | Die Form der Kernquelle trägt (`:*`); keine eigenen Regeln für Cmdlets – `Remove-Item` und `curl` wurden ohne sie abgewiesen | `Invoke-WebRequest` ungemessen |
| E3 | Nachweis | `FW-ZA-07`, `FW-ZA-08`, gemessen; keine neue Prüfung – die bestehenden halten die Werkzeuglisten und die installierte Datei gegen die Kernquelle | – |
| E4 | Die Ausblendung | **Beim Messen gefunden:** ein Befund über den Client, kein Schutz des Frameworks | Windows ohne Git Bash offen (`K-188`) |

## 4. Umsetzung

1. Manifest `claude-code`: `PowerShell` in `permission_tools.exec` und `hook_tools.exec`.
2. Pack-Dokument 0.25.1: Zeilen `exec`, B3, B6 mit den Messwerten und dem Befund.
3. Testkatalog: `FW-ZA-07`, `FW-ZA-08`; Sonden zu den Prüfungen 33 und 42 für zwei Befehlswerkzeuge angepasst.
4. Register, Roadmap, CHANGELOG, `VERSION`, Bestandsliste, Hauptdokument; Hebung beider Projekte, im Piloten die Berechtigungsdatei von Hand.

## 5. Entscheidung

🟢 **Angenommen am 2026-09-29.**

| # | Entscheidung | Decision Record |
|---|---|---|
| E1 bis E3 | Gleichstellung | D-469 |
| E4 | Die Ausblendung | D-470 |
