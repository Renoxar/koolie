# Overlay-Muster „General Development“

| Attribut | Wert |
|---|---|
| Name | `general` |
| Version | `0.1.0` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Gewählt über | `python .koolie/core/install.py --overlay general` – **nur bei der Erstinstallation** (D-126) |
| Wirkung | füllt drei Pfadplatzhalter einmal in Overlay, Laufzeitfassung und Berechtigungsdatei (D-355) |
| Nachweis | Sonden `M355` bis `M355e` in `.koolie/core/tests/scripts/probe-pruefungen.py` |

## Zweck

Ein Projekt, das das Framework übernimmt, beginnt ohne diesen Parameter mit einem
**leeren** Overlay: Jeder Platzhalter ist ein Schlitz, und bis ein Mensch ihn füllt,
sperrt die Berechtigungsdatei an seiner Stelle nichts. Dieses Muster füllt die Schlitze,
deren Wert sich **ohne Kenntnis des Projekts** sicher angeben läßt – und nur diese.

## Der Grundsatz: Das Muster sperrt, es gibt nichts frei

🔴 **Ein mitgeliefertes Muster schlägt Projektwerte vor, und der Kern darf keine
enthalten** (Entscheidungsbaum 6, Prüfungen 6 und 14). Die Grenze ist deshalb keine
Auswahl nach Geschmack, sondern eine Richtung: **Jeder Wert dieses Musters verschärft.**
Er steht ausschließlich in einem `deny`-Eintrag; ein Wert, der auf ein Projekt nicht
paßt, sperrt eine Datei, die es dort nicht gibt, und kostet nichts.

➡️ **Nicht gefüllt wird deshalb alles, was etwas FREIGIBT oder das Projekt BESCHREIBT:**
`<ALLOWED_PATHS>`, `<TEST_PATHS>`, `<DOC_PATHS>`, `<READ_ONLY_PATHS>`, die drei
Befehlsschlitze, Rollen, Status, Freigaben und die Ergebnisse der Datenschutz- und
Vertragsprüfung. `install.py` nimmt aus dieser Datei **nur** die drei Platzhalter der
Tabelle unten an und bricht ab, wenn sie einen anderen führt – die Grenze steht im
Werkzeug, nicht nur in diesem Satz.

## Die Werte

Gelesen wird diese Tabelle – über die Platzhalterzelle, nicht über eine Spaltennummer.
Jeder Wert steht in einer eigenen Codespanne.

| Platzhalter | Werte | Warum ohne Kenntnis des Projekts sicher |
|---|---|---|
| `<CI_CONFIG_PATHS>` | `.github/workflows/**`, `.gitlab-ci.yml`, `.gitea/workflows/**`, `Jenkinsfile`, `azure-pipelines.yml`, `bitbucket-pipelines.yml`, `.circleci/**` | Die üblichen Ablagen der verbreiteten CI-Werkzeugklassen. Gesperrt wird nur das **Schreiben**; eine Merge-Request-Vorlage neben `.github/workflows/` bleibt lesbar (D-161) |
| `<QUALITY_GATE_CONFIG_PATHS>` | `.editorconfig`, `.eslintrc*`, `eslint.config.*`, `.prettierrc*`, `.stylelintrc*`, `sonar-project.properties`, `codecov.yml`, `.codecov.yml`, `.coveragerc`, `.pylintrc`, `.flake8`, `ruff.toml`, `.golangci.yml`, `checkstyle.xml` | Eigenständige Konfigurationsdateien von Linter, Formatierer, Analyse und Abdeckung – Schwellenwerte ändert der KI-Client nie (`OVERLAY.md` Abschnitt 7). ⚠️ **Bewußt nicht:** Sammeldateien wie `pyproject.toml` oder `package.json`, die neben der Prüfkonfiguration auch Abhängigkeiten tragen – sie zu sperren, wäre eine Aussage über das Projekt |
| `<EXCLUDED_PATHS>` | `**/*.tfstate`, `**/*.tfstate.*`, `**/*.dump` | Zustandsdateien einer Infrastrukturbeschreibung tragen Zugangsdaten im Klartext, Datenbankabzüge echte Daten (K3). ⚠️ **Bewußt nicht:** `deploy/**`, `infra/**` oder `config/prod/**` aus dem Beispiel der Vorlage – sie setzen ein Verzeichnislayout voraus, und eine Lesesperre auf ein Verzeichnis, in dem das Projekt arbeitet, ist keine Verschärfung, sondern ein Hindernis |

## Wie die Werte in das Projekt kommen

`install.py --overlay general` schreibt bei der Erstinstallation **drei** Träger aus dieser
Tabelle, und zwar genau einmal (D-353, D-355):

| Träger | Was gefüllt wird |
|---|---|
| `.koolie/project-overlay/OVERLAY.md` | die Spalte **Wert** der drei Zeilen in Abschnitt 4; ein Eintrag im Änderungsverlauf nennt Muster und Version |
| `<RULES_DIR>/20-project-overlay.md` | der Wert hinter `<EXCLUDED_PATHS>` – die beiden anderen Platzhalter führt die Laufzeitfassung nicht |
| `<PERMISSIONS_FILE>` | jeder `deny`-Eintrag der Kernquelle, der einen der drei Platzhalter trägt, wird zu einem Eintrag je Wert – **dieselben Schlitze, keiner mehr** |

⚠️ **Abgrenzung zu D-76.** Gelesen wird ein Träger des Kerns, nicht des Projekts, und
zugesagt ist der **Anfangszustand**, kein Kanal. Danach gehören alle drei Dateien dem
Projekt wie ohne Muster; `install.py --update` liest dieses Muster nie wieder. Ein
Projekt, das einen Wert später ändert, zieht ihn wie jeden anderen Wert von Hand nach –
**und Prüfung 59 findet die Abweichung für `<EXCLUDED_PATHS>`.**

⚠️ **Bei einem Client Pack, dessen Berechtigungsschicht keine Musterform kennt**
(`openai-codex`, B3 und B5 `[NICHT ABBILDBAR]`), kommt nur ein Teil an – gemessen an
einer Wegwerf-Installation: Ein Teilbaum (`.github/workflows/**`) und ein einzelner
Dateiname (`Jenkinsfile`) werden zu einem Pfad mit Zugriffsart `read`, ein Namensmuster
mit `*` (`**/*.tfstate`, `.eslintrc*`) erreicht die Datei nicht. Das Muster ändert daran
nichts, und das Pack sagt es in Abschnitt 5 selbst.

## Die Grenze zur Aktivierungsreife

🔴 **Ein Overlay aus diesem Muster ist nicht aktivierungsreif, und das ist gewollt**
(D-57). Es läßt die Pflichtwerte der Abschnitte 1, 5, 6, 13, 14 und 15 offen; ein Overlay,
das die Prüfung `--check-overlay-ready` von selbst bestünde, wäre ein aktivierungsreifer
Zustand, den niemand geprüft hat. **Die Sonde `M355b` hält fest, daß eine frische
Installation mit diesem Muster die Prüfung nicht besteht.**

## Änderungsverlauf

| Version | Datum | Änderung |
|---|---|---|
| `0.1.0` | 2026-09-25 | Erstfassung mit Framework-Release `1.5.0` (`CR-2026-138`, D-355) |
