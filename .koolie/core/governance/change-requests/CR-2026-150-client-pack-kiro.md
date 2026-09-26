# Änderungsantrag `CR-2026-150`

| Feld | Inhalt |
|---|---|
| Titel | Das Client Pack für Kiro – mit Zugang gebaut, und der Schutz-Hook, der ohne Grund nicht sperrte |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-26 |
| Betroffene Artefakte | `.koolie/core/clients/kiro/**` (neu); `.koolie/core/clientmap.py`; `.koolie/core/install.py`; `.koolie/core/framework/runtime/client-settings.json` (neu); `.koolie/core/framework/runtime/rules/16-plan-spezifikation.md` (neu); `.koolie/core/tests/scripts/hook-check-secrets.py`; `.koolie/core/tests/scripts/validate-framework.py` (**Prüfung 96**, Prüfungen 37, 42, 43, 54, 72, 73, 86, 87); `.koolie/core/tests/scripts/probe-pruefungen.py`; `.koolie/core/clients/README.md`; `.koolie/core/clients/openai-codex/CLIENT_PACK.md`; `.koolie/core/OWNERS.md`; `.koolie/core/build/doc/31-anhaenge.md`; `.koolie/core/build/doc/00-kopf.md`; `.koolie/core/build/doc/26-qs-test.md`; `.koolie/core/docs/ROADMAP.md`; `.koolie/core/governance/DECISION_LOG.md` (**D-414** bis **D-418**, `K-147` beantwortet, `K-162` bis `K-164`); `.koolie/core/tests/TEST_CATALOG.md`; `.koolie/core/CHANGELOG.md`; `.koolie/core/VERSION`; `.koolie/core/governance/ADOPTION_REGISTRY.md`; `.gitignore` |
| Ebene laut Entscheidungsbaum 6 | Abbildungsschicht und Prüfapparat |
| Art | **Änderung.** MINOR-Release nach `RELEASE_PROCESS.md` Abschnitt 1 – ein neues Modul und eine neue Prüfung, **ohne Overlay-Bruch** |
| Dringlichkeit | regulär – eingeplant mit D-401 und D-406 |
| Status | 🟢 **entschieden am 2026-09-26** (E1 bis E8) |

---

## 1. Anlass

Der nächste Posten des Plans: das Client Pack für Kiro, **aus der Dokumentation** (D-401). Die Fragen dazu lagen mit einer Schätzung vor – dann hat der Owner während der Sitzung **die Kommandozeile und die IDE installiert und ein Konto im Free-Tarif angelegt**. Die Empfehlung änderte sich daraufhin: Bau und Messung in einem Release, und angenommen mit *„Ja, schalte die Weitergabe ab und leg los“*.

🔴 **Die Messung hat die beiden schwersten Befunde erst gezeigt.** Ein Pack aus der Dokumentation hätte einen Schutz-Hook ausgeliefert, der läuft und nichts sperrt (D-417), und eine Berechtigungsschicht, die bei einem kaputten Profil still verschwindet (D-414).

## 2. Der Vorbedingungsdurchgang

| # | Befund | gemessen an |
|---|---|---|
| **V1** | 🟢 Nächste freie Kennungen gezählt, nicht gelistet: `CR-2026-150`, `D-414`, `K-162`, Prüfung 96 | Register gezählt |
| **V2** | 🟢 Validator `0 Fehler, 0 Warnungen` am Ausgangsstand, Arbeitsbaum sauber | `validate-framework.py` |
| **V3** | 🟢 Clientversion **vor** dem Messen festgeschrieben: Kommandozeile `2.24.1` (KAS `0.66.8`), IDE `1.1.70` | `kiro-cli --version`, Produktdatei der IDE |
| **V4** | 🟢 Weitergabe der Inhalte und Telemetrie **vor** den Messläufen abgeschaltet (Kommandozeile durch diese Sitzung, IDE durch den Owner) | `~/.kiro/settings/cli.json` |
| **V5** | ⚠️ Kein Messbaum unterhalb des Benutzerprofils – Messpfad `C:\lw-kiro\` | Lehre aus `UEBERGABE.local.md` |

## 3. Die Messungen

**Drei Messmittel, zwei davon fast kostenlos:** der Lauf ohne Rückfragen mit JSON-Ausgabe (je Lauf 0,02 bis 0,3 Credits, mit Aufschlüsselung der Kontextdateien), die interaktive Sitzung über ein Pseudo-Terminal (Mitschrift unter `~/.kiro/sessions/`) – und der **Programmcode des Clients**, der im Klartext mitgeliefert wird. Die Befunde stehen einzeln im Protokoll (`tests/protocols/2026-09-26-bau-kiro.md`). **Vier haben den Bau geändert:**

| # | Befund | Folge |
|---|---|---|
| **K15/K16** | 🔴 **Fehlt das Agentenprofil oder ist es kaputt, fällt der Client still auf seinen eingebauten Agenten zurück**; `.env` war lesbar | Prüfung 96 (D-414) |
| **K5** | 🔴 **Im Betrieb ohne Rückfragen laufen keine Hooks** – der Agentenserver aktiviert sie nur, wenn die Terminaloberfläche es meldet | Bedingung in H1 bis H3 und in Abschnitt 1b des Packs |
| **T2b/T3** | 🔴 **Der Schutz-Hook sperrte mit der Standardform nichts** – Exit 2, Grund auf stdout, Köderinhalt gelesen; mit Grund auf stderr drei von drei abgewiesen | Sperrform `stderr-grund` (D-417) |
| **A2** | 🔴 **Die Kernregel `write <RUNTIME_DIR>/**` sperrte das Planartefakt**; mit `exclude` fällt es in die Rückfrage | `permission_rule_exclude` (D-415) |

## 4. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | Aus der Dokumentation (D-401) oder mit Zugang? | 🟢 **Mit Zugang, Bau und Messung in einem Release, Status `pilot`** (D-414) | Die IDE ist nicht an Sitzungen gemessen (`K-162`) |
| **E2** | Wo stehen die Berechtigungen? | 🟢 **Im Agentenprofil `.kiro/agents/koolie.json`, gewählt durch `.kiro/settings/cli.json`** (D-414) | Wer `--agent` wählt, arbeitet ohne die Regeln; stiller Rückfall bei kaputtem Profil – Prüfung 96 fängt die Dateiseite, nicht den Start |
| **E3** | Welches Planartefakt? | 🟢 **Weg B – die Spezifikationen des Clients**, mit Regel `16-plan-spezifikation.md` und Ausnahme für `.kiro/specs/**` (D-415) | Das Befolgen ist Modellverhalten |
| **E4** | Wie wird der Schutz-Hook abgebildet? | 🟢 **Hook-Datei `version: v1`, Matcher als regulärer Ausdruck, Sperrform `stderr-grund`** (D-417) | Nur interaktiv |
| **E5** | Die formatgebundenen Prüfungen | 🟢 **Je Eintrag die erreichten Formen; 72 statt 76; ausdrückliche Schutzabfragen** (D-416) | Abschnitt 5 von `openai-codex` war sieben Releases falsch |
| **E6** | Eine eigene Prüfung für das Profil? | 🟢 **Prüfung 96** (D-414) | Sie misst Dateien, nicht den Start |
| **E7** | Cursor (Auftrag des Owners während des Baus) | 🟢 **`1.16.0` am Ende des Plans**, gebaut mit Zugang (D-418) | – |
| **E8** | Einstufung | **MINOR** – ein neues Modul und eine neue Prüfung, kein Overlay-Bruch | – |

## 5. Umsetzung

1. `clients/kiro/`: `CLIENT_PACK.md` (35 Matrixzeilen), `manifest.json`, `root-template/.kiro/README.md`.
2. `clientmap.py`: `render_permissions_kiro`, `render_client_settings`, `render_hooks_kiro`, `KIRO_FAEHIGKEITEN`, `permission_rule_exclude`.
3. `install.py`: Weiche der Ausgabeformen; feste Frontmatter-Felder je Ladetrigger; Hinweistext je Pack.
4. `hook-check-secrets.py`: Sperrform `stderr-grund`, `.kiro` in den Strukturmustern.
5. `validate-framework.py`: **Prüfung 96**; Prüfung 87 je Form; Schutzabfragen in 37, 42, 43, 54, 72; Prüfung 72 liest das Profil; Prüfung 73 kennt `QK-`; Prüfung 86 kennt die neue Form; `_hook_kommandos` liest die Hook-Liste.
6. `probe-pruefungen.py`: Bündel `sonden_kiro` mit vierzehn Einheiten.
7. Register, Roadmap, Anhang 31.4.4, CHANGELOG, `VERSION`, Bestandsliste; Hebung beider Projekte (Schritt 2) und Bau der Erzeugnisse (Schritt 3).

## 6. Entscheidung

🟢 **Angenommen am 2026-09-26, E1 bis E8 wie vorgelegt** – der Owner folgt den Empfehlungen (Auftrag der Sitzung) und hat E1 ausdrücklich bestätigt (*„Ja, schalte die Weitergabe ab und leg los“*); E7 ist sein Auftrag.

| # | Entscheidung | Decision Record |
|---|---|---|
| E1, E2, E6 | Pack mit Zugang, Agentenprofil, Prüfung 96 | D-414 |
| E3 | Weg B | D-415 |
| E5 | formatgebundene Prüfungen je Form | D-416 |
| E4 | Sperrform `stderr-grund` | D-417 |
| E7 | Cursor | D-418 |
