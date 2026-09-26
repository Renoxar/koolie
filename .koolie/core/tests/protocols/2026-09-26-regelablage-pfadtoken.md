# Protokoll: Die Regelablage, die nur mit Windsurf lädt, und das Sonderziel, das umbenannt wurde

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-26 |
| Release | `1.12.1` |
| Änderungsantrag | `CR-2026-149` |
| Art | Patch-Release mit Kontingent – **24 Sitzungsläufe über zwei Clients, 0,65 USD nach Listenpreis**, dazu Messungen ohne Modellaufruf |
| Gegenstand | Regelablage von `devin-desktop` (`K-156`), Pfadeinträge des Rechteprofils von `openai-codex` (`K-157`) |
| Ergebnis | 🟢 **Entschieden, `D-411` bis `D-413`.** `K-156` und `K-157` beantwortet, `K-160` und `K-161` neu. 🔴 **Mit `windsurf: false` lädt auch Devin CLI 3000.11.3 die eigene Regelablage nicht** – das Pack lässt Windsurf-Quellen zu und meldet sie; **mit der alten Pfadform war unter Codex 0.157 der ganze Arbeitsbereich schreibgeschützt** |

---

## 1. Was gefragt war

Wiederaufnahmepunkt von `1.12.0`, Punkt 2: der Posten `1.12.1` – `K-156` (Abwägung gegen D-290)
und `K-157` (aktuelle Schreibweise der Pfadschlüssel). Vorher ohne Kontingent die
Herstellerdokumentation beider Clients gelesen; Fragen (a) bis (f) mit einer Schätzung von rund
30 Läufen und 3 bis 5 USD vorgelegt und angenommen (*„Ich stimme zu“*). Der Owner hat vor dem Bau
beide Clients aktualisiert: Devin CLI **3000.11.3**, Codex **0.157.1**.

## 2. `K-156`: die Regelablage von `devin-desktop` (D-411)

**Herstellerdokumentation** (abgerufen am 2026-09-26, `docs.devin.ai/cli/extensibility/rules` und
`…/reference/configuration/read-config-from`): `.devin/rules/*.md` ist ein eigener Ablageort und
*„takes precedence over `.windsurf/`“*; die Importsteuerung nennt ihn nicht. `windsurf` importiert
Regeln aus `.windsurf/rules/` und `.windsurf/global_rules.md`, Skills und MCP-Server; `copilot`
(`.github/skills/`, `~/.copilot/skills/`), `opencode` und `zed` (je MCP) sind dokumentiert, alle mit
Standard `true`.

**Minimalbaum**, fünf Varianten unter `C:\lw-1121\k156-*`, je ein Kennwort in jedem Kanal; die
Anweisungsdatei im Benutzerprofil trug für diese fünf Läufe ein Kennwort und war vorher und nachher
leer. Prompt: alle Kennworte nennen, kein Werkzeug. Gezählt in Antwort **und** Mitschrift, beide
deckungsgleich, kein Werkzeugaufruf:

| Variante (`read_config_from`) | `AGENTS.md` | `.devin/rules/` | `.windsurf/rules/` | Benutzerprofil | `.github/skills/` |
|---|---|---|---|---|---|
| ohne `config.json` | ja | ja | ja | ja | nein |
| wie `1.12.0` (`windsurf: false`) | ja | **nein** | nein | nein | nein |
| nur `windsurf: true` | ja | ja | ja | ja | nein |
| neu (`windsurf: true`, `copilot`/`opencode`/`zed`: `false`) | ja | ja | ja | ja | nein |
| neu, aber `windsurf: false` | ja | **nein** | nein | nein | nein |

➡️ **Der Befund besteht in 3000.11.3 fort**, und der Schalter ist der einzige Unterschied.
`.github/skills/` lud in **keiner** Variante, auch ohne abschaltenden Schalter; die Wirkung von
`copilot: false` ist damit nicht messbar (Abweichung E3). Die Skills erscheinen im Schritt
`<available_skills>`; der Testskill stand dort nie.

**Die Ladebedingungen mit der neuen Einstellung** (`C:\lw-1121\k156-r2`, fünf Läufe): Eine Regel mit
`trigger: always_on` lädt; eine mit `model_decision` steht mit ihrer Beschreibung unter
`<available_rules>`, ihr Inhalt nicht (das Modell hatte keinen Anlass). 🔴 **Eine Regel mit
`trigger: glob` und `globs: "**/*.java"` lädt nicht** – weder aufgeführt noch nach dem Lesen von
`Foo.java` im Kontext, zwei Läufe; ohne Anführungszeichen um das Muster ebenso, ein Lauf (`K-161`).

**Feste Last** im committeten Stand des Übungsrepositoriums (`C:\lw-1121\ueb-dd-mit` mit der neuen
Einstellung, `ueb-dd-ohne` ohne jeden Träger des Frameworks, synthetischer Autor und Committer),
Aufgabe *„Antworte nur mit OK“*, je dreimal: Eingabe je **31.900** gegen je **23.556** Token,
also **8.344** – deckungsgleich mit der Variante *„Regelablage geladen“* aus `1.12.0` (8.357). Die
Mitschrift führt die Regeln `00`, `10` und `20` im Kontext.

**Abhilfe:** `windsurf: true`; `install.py` nennt nach Installation und Hebung die Kanäle aus
`import_channels_report`, die belegt sind. Wirkungsnachweis: Bündel `sonden_importkanaele` – Sonde
`D411` (Ersatz-Benutzerprofil mit nicht leerer Datei und `.windsurf/` im Projekt: beide genannt, bei
Installation und Hebung), Gegenprobe `D411a` (leer, kein `.windsurf/`: kein Hinweis). Die Sonde zu
Prüfung 22 verfälschte bisher `windsurf` von `false` auf `true` – sie verfälscht jetzt `cursor`.

## 3. `K-157`: das Sonderziel von `openai-codex` (D-412)

**Herstellerdokumentation** (abgerufen am 2026-09-26, `learn.chatgpt.com/docs/permissions`):
Sonderziele `:root`, `:minimal`, `:workspace_roots`, `:tmpdir`, `:slash_tmp`; Unterpfade als Tabelle
`[permissions.<profil>.filesystem.":workspace_roots"]` mit `"." = "write"` für die Wurzel;
`deny` vor `write` vor `read`; `deny`-Globs dort dokumentiert (`K-160`).

**Ohne Modellaufruf**, zwei Bäume mit derselben Aussage in beiden Formen, als vertraut eingetragen:

| Form | Startwarnungen (`codex doctor --all`) | `codex sandbox`: freie Datei | `.koolie/core` | `.codex` | `AGENTS.md` |
|---|---|---|---|---|---|
| alt (`:workspace/<pfad>`) | 4 – *„not recognized … will be ignored“* | **abgewiesen** | abgewiesen | abgewiesen | abgewiesen |
| neu (`:workspace_roots`) | keine | geschrieben | abgewiesen | abgewiesen | abgewiesen |

🔴 **Mit der alten Form war der ganze Arbeitsbereich schreibgeschützt** – übrig blieb `:root = read`.
Dieselbe Probe an einer frischen Installation des Packs (`C:\lw-1121\cx-inst`): freie Datei
geschrieben, `.koolie/core`, `.koolie/project-overlay`, `.codex` und `AGENTS.md` abgewiesen.

**In Sitzungen** (`C:\lw-1121\cx-roh`: die Installation ohne Regeltexte, Befehlsregeln bleiben; der
Hook trägt kein Vertrauen und läuft deshalb nicht – zugerechnet wird dem Sandkasten):

| Lauf | Auftrag | Ergebnis |
|---|---|---|
| `cx-b4-1`, `cx-b4-2` | `Set-Content -Path .koolie/core/notiz.txt` | *„Der Zugriff auf den Pfad … wurde verweigert“*, keine Datei |
| `cx-b4k-1`, `cx-b4k-2` | `Set-Content -Path frei.txt` (Kontrolle) | geschrieben |
| `cx-b1-1` | `git push origin main` | abgewiesen: *„rejected: Framework-Regel (forbidden)“* |
| `cx-t1-1` bis `-3` | *„Antworte nur mit OK“* in `cx-inst` | je 19.749 Token, keine Startwarnung |

Seit 0.157.1 laufen die Sitzungen ohne `--no-daemon` (Angabe des Owners, bestätigt). Wirkungsnachweis:
Bündel `sonden_pfadtoken_codex` – Sonde `D412` (die erzeugte `config.toml` einer echten Installation
führt die Tabelle mit `"." = "write"` und dem Kern als `"read"`, keinen Schlüssel der alten Form),
Gegenprobe `D412a` (`:root = read` bleibt in der Dateisystemtabelle).

## 4. Was bestehende Installationen tun müssen

`install.py --update` fasst die Berechtigungsdatei nicht an. **`devin-desktop`:** `read_config_from`
in `.devin/config.json` nachziehen – Prüfung 22 meldet den alten Wert. **`openai-codex`:** die
Einträge `:workspace…` in `.codex/config.toml` durch die Tabelle ersetzen; keine Prüfung sieht die
alte Form. Im Übungsrepositorium ist `read_config_from` bei der Hebung von Hand nachgezogen; eine
Installation von `openai-codex` führt die Bestandsliste nicht.

## 5. Abnahme

| Lauf | Ergebnis |
|---|---|
| Validator | 0 Fehler, 0 Warnungen, mit und ohne `PYTHONIOENCODING=utf-8` |
| Sondenlauf | **350 Einheiten** (348 + zwei Bündel), alle bestanden, Exit 0, beide Kodierungsumgebungen zeilengleich (624 Zeilen), je rund 610 s |
| Gegenbeweis | Baum aus `v1.12.0` mit dem neuen Sondenskript: `D411` und `D412` fallen, `D411a` und `D412a` bestehen |
| Pilot (`claude-code`) | gehoben, `--strict-overlay` 1 Fehler, 2 Warnungen – unverändert, projekteigene Befunde |
| Übungsrepositorium (`devin-desktop`) | gehoben, `read_config_from` von Hand nachgezogen, `--strict-overlay` 0 Fehler, 1 Warnung – unverändert; kein Importkanal belegt |

## 6. Aufbau, Belege, Kontingent

Werkzeuge, Prompts, Belege in `devpacks/leitwerk-erhebungen-2026-09-26-1121/` (`baum-k156.py`,
`global-k156.py`, `baum-fixlast.py`, `lauf-1120.py`, `codex-vertrauen.py`). Messbäume unter
`C:\lw-1121`, nicht unterhalb des Benutzerprofils. Die Anweisungsdatei im Benutzerprofil ist nach
den fünf Läufen wieder leer (0 Bytes); die Vertrauenseinträge für `openai-codex` sind nach dem
letzten Lauf gezielt entfernt.

| Client | Läufe | Token | USD nach Listenpreis |
|---|---|---|---|
| `devin-desktop` | 16 | 478.881 | 0,55 |
| `openai-codex` | 8 | 229.022 | 0,11 |
| **Summe** | **24** | **707.903** | **0,65** |

Preise wie in `1.12.0`: `devin-desktop` die Preisliste des Clients für `claude-opus-5-medium`,
`openai-codex` dieselbe Preisliste für `gpt-5.6-sol` als Ersatzquelle.
