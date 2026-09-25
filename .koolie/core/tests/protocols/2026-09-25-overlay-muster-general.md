# Protokoll: Das Overlay-Muster „General Development“ – und die Prüfung, die von fünf Pfadwerten einen sah

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-25 |
| Release | `1.5.0` |
| Änderungsantrag | `CR-2026-138` |
| Art | Neue Funktion des Installationswerkzeugs, neue Prüfung, neuer Schlitz der Kernquelle – **keine Sitzung, kein Kontingent, kein Modelllauf** |
| Gegenstand | Der Füllschritt aus `install.py --overlay general` an Erstinstallationen aller drei Packs; Prüfung 89 an beiden übernehmenden Projekten; Prüfung 59 an `openai-codex` |
| Ergebnis | 🟢 **Entschieden, `D-355` bis `D-358`.** Das Muster füllt drei Pfadplatzhalter in allen drei Trägern und nichts, was freigibt. 🔴 **Prüfung 89 findet im Übungsrepositorium vier ersetzte statt gebundene Werte.** 🔴 **Prüfung 59 übersprang ihren dritten Gegenstand bei `openai-codex` still** |

---

## 1. Was gefragt war

Wiederaufnahmepunkt von `1.4.4`, Punkt 2: der Posten `1.5.0` mit dem Umfang aus D-353.
Vor dem Bau vorgelegt und mit *„wie empfohlen“* entschieden: `CR-2026-138` E1 bis E8.

## 2. Messungen

Alle Messungen an Wegwerf-Verzeichnissen im Ablagebereich der Sitzung; der Kern kommt
über `git ls-files -z .koolie/core | tar` aus dem Arbeitsbaum.

### 2.1 Prüfung 59 an `openai-codex` – der Vorstand

Wegwerf-Installation `openai-codex` aus dem Stand vor diesem Release; in `OVERLAY.md`
und `.codex/rules/20-project-overlay.md` `<EXCLUDED_PATHS>` auf `deploy/**` gesetzt,
Berechtigungsdatei unverändert.

| Gegenstand | Ergebnis |
|---|---|
| `.codex/config.toml` enthält `EXCLUDED` oder `deploy` | **nein** (`grep`, 0 Treffer) |
| `--strict-overlay`, Meldungen mit `EXCLUDED`, `ausgeschlossen` oder `deploy` | 🔴 **keine** (17 Fehler insgesamt, sämtlich offene Schlitze) |

➡️ **Gegenstand (c) kehrte an `json.loads` still zurück** – E9, D-358.

### 2.2 Der Füllschritt – je Pack

`install.py --client <pack> --overlay general` in ein leeres Repositorium.

| Pack | Ergebnis |
|---|---|
| `claude-code` | Exit 0; `deny` 78 Einträge; `Read`/`Edit` für die drei `<EXCLUDED_PATHS>`-Werte, `Edit` für jeden CI- und Prüfkonfigurationswert; **kein** Schlitz der drei mehr wörtlich; `Edit(<READ_ONLY_PATHS>)` steht (D-356) |
| `devin-desktop` | Exit 0; `deny` 77 Einträge; einziger verbliebener Schlitz `Write(<READ_ONLY_PATHS>)` |
| `openai-codex` | Exit 0; in `.codex/config.toml` u. a. `":workspace/.github/workflows" = "read"`, `":workspace/Jenkinsfile" = "read"`, `":workspace/.editorconfig" = "read"`; **kein** Namensmuster mit `*` |

In allen drei: Laufzeitfassung trägt `` (`<EXCLUDED_PATHS>`): `**/*.tfstate`, `**/*.tfstate.*`, `**/*.dump` ``,
`OVERLAY.md` die drei Wertzeilen und im Änderungsverlauf *„Overlay angelegt aus dem Muster
`general` `0.1.0`“*.

| Validatorlauf an der Muster-Installation `claude-code` | gegenüber der Installation ohne Muster |
|---|---|
| Standardlauf | nur neu: `D-355` ohne Registerzeile (vor dem Eintrag) und ein Kommentar in `install.py`, der ein Wort in spitzen Klammern wie einen Platzhalter schrieb (berichtigt) |
| `--strict-overlay` | nur neu: dieselbe Registermeldung; **Prüfung 59 schweigt** |
| `--check-overlay-ready` | nicht bestanden (17 Fehler) – gewollt, E4 |

⚠️ **Zwei Befunde am eigenen Bau, beide vor der Auslieferung gefangen:**
(1) Der Wächter aus E1 schlug beim ersten Lauf an – an der Tabelle *„Wie die Werte in das
Projekt kommen“*, deren erste Spalte `<PERMISSIONS_FILE>` nennt. Gelesen wird seither nur
der Abschnitt *„Die Werte“*. (2) Die Musterdatei behauptete, bei `openai-codex` erreiche
kein Globwert die Datei; gemessen kommen Teilbäume und Dateinamen an.

### 2.3 Prüfung 89 an beiden Projekten – vor der Hebung

Validator dieses Standes mit `--root` gegen den Arbeitsbaum des Projekts, `--strict-overlay`:

| Projekt | Meldungen von Prüfung 89 |
|---|---|
| Pilot (`otp-generator`) | **keine** – alle vier gebunden; `<DOC_PATHS>` `nicht vorhanden` gegen `keine`, beides leer; `Edit(./pom.xml)` und `Edit(./start.ps1)` im Korb |
| Übungsrepositorium (`test-devin-framework`) | 🔴 **vier:** *„nennt `<ALLOWED_PATHS>` nicht“*, dasselbe für `<TEST_PATHS>`, `<DOC_PATHS>`, `<READ_ONLY_PATHS>` |

### 2.4 Wirkungsnachweis – Sonden und Gegenproben, mit Gegenbeweis

| Einheit | Stand `1.5.0` | Gegenbeweis |
|---|---|---|
| Gegenproben `89`, `89k` | OK | mit Validator aus `1.4.4`: OK |
| Sonden `89a` bis `89d` | OK | mit Validator aus `1.4.4`: **je FEHL** |
| `M355` bis `M355e` | OK | mit `install.py` und Kernquelle aus `1.4.4`: Bündel bricht ab (`muster_laden` fehlt; der Wächter von `_89_fuellen` meldet den fehlenden Schlitz aus D-356) |
| Bündel zu Prüfung 59 | unverändert OK | – |

## 3. Abnahme

| Lauf | Ergebnis |
|---|---|
| Validator | **0 Fehler, 0 Warnungen**, beide Kodierungsumgebungen |
| Sondenlauf | **327 Einheiten, alle bestanden** (vorher 325; neu die Bündel `sonden_overlay_pfadabgleich` und `sonden_overlay_muster`), beide Kodierungsumgebungen Exit 0 und oberhalb der Trennlinie zeilengleich (535 Zeilen), rund 510 s Wanduhr je Lauf; **Abnahmelauf gegen den fertigen Baum zeilengleich** |
| Pilot / Übungsrepo `--strict-overlay` nach der Hebung | Pilot **1 Fehler, 2 Warnungen**, alle im projekteigenen `CHANGELOG.md`, unverändert; Übungsrepo **0 Fehler, 1 Warnung** – die Laufzeitfassung steht mit den vier Bindungen auf 6.095 statt 6.023 Zeichen (SOLL-Grenze 6.000, dieselbe Warnung wie vorher). Prüfung 89 meldet in beiden nichts; Auskunft über ignorierte Kerndateien im Pilot weiterhin **38** |

## 4. Nebenhandlungen außerhalb des Kerns

- Signierte Marke `v1.4.4` (vom Owner gesetzt) gepusht, Schritte 5 bis 7 aus
  `RELEASE_PROCESS.md` 4.1: 541 Dateien, kein CRLF, Lizenz an beiden Stellen gleich.
- Auf dem Remote war `v1.2.0` eine leichte Marke, lokal die signierte; die signierte ist
  auf Entscheidung des Owners nachgeschoben, das Gitea-Release hängt unverändert daran.

## 5. Offen

- Ob eine weitere Prüfung still an der Ausgabeform scheitert, **ohne** sich auf
  `FORMATGEBUNDENE_PRUEFUNGEN` zu berufen, sagt keine Stelle (D-358).
- `1.6.0`: ob der Installer Python voraussetzen darf (Planabschnitt der Roadmap).
