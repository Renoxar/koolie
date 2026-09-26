# Änderungsantrag `CR-2026-155`

| Feld | Inhalt |
|---|---|
| Titel | Das Client Pack für Cursor – die Datei, mit der der Client nicht startet, und das Muster, das nie traf |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-26 |
| Betroffene Artefakte | `.koolie/core/clients/cursor/**` (neu); `.koolie/core/clientmap.py`; `.koolie/core/install.py`; `.koolie/core/tests/scripts/hook-check-secrets.py`; `.koolie/core/tests/scripts/hook-overlay-status.py`; `.koolie/core/tests/scripts/validate-framework.py` (**Prüfung 97**, Prüfungen 4, 45, 73, 86 und die Stellen der Regelablage); `.koolie/core/tests/scripts/probe-pruefungen.py` (Bündel `sonden_cursor`); `.koolie/core/clients/README.md`; `.koolie/core/docs/PLACEHOLDER_REGISTRY.md`; `.koolie/core/docs/RUNTIME_GLOSSARY.md`; `.koolie/core/OWNERS.md`; `.koolie/core/build/assemble.py`; `.koolie/core/build/doc/00-kopf.md`, `01-executive-summary.md`, `26-qs-test.md`, `31-anhaenge.md`; `.koolie/core/docs/ROADMAP.md`; `.koolie/core/governance/DECISION_LOG.md` (**D-440** bis **D-444**, `K-108` und `K-164` beantwortet, `K-175` bis `K-177`); `.koolie/core/tests/TEST_CATALOG.md`; `.koolie/core/tests/protocols/2026-09-26-bau-cursor.md` (neu); `.koolie/core/CHANGELOG.md`; `.koolie/core/VERSION`; `.koolie/core/governance/ADOPTION_REGISTRY.md`; `README.md`, `README.en.md`; `.gitignore` |
| Ebene laut Entscheidungsbaum 6 | Abbildungsschicht und Prüfapparat |
| Art | **Änderung.** MINOR-Release nach `RELEASE_PROCESS.md` Abschnitt 1 – ein neues Modul und eine neue Prüfung, **ohne Overlay-Bruch** |
| Dringlichkeit | regulär – eingeplant mit D-418 und D-422 |
| Status | 🟢 **entschieden am 2026-09-26** (E1 bis E9) |

---

## 1. Anlass

Der nächste Posten des Plans: das Client Pack für Cursor, gebaut mit Zugang zum Client (D-418). Die Entscheidungsfragen lagen mit einer Schätzung vor (35 bis 50 Läufe, 0 USD im Free-Tarif); der Owner hat alle Empfehlungen angenommen (*„Passt alles.“*). Den geführten IDE-Block und die globale Abschaltung der Commit-Attribution übernimmt er später – die IDE bleibt deshalb ungemessen (`K-175`).

🔴 **Wie bei `kiro` hat erst die Messung die schwersten Befunde gezeigt.** Ein Pack aus der Dokumentation hätte eine Berechtigungsdatei ausgeliefert, mit der der Client nicht startet, Pfadverbote, die unter Windows nichts sperren, und einen Schutz-Hook, der jede Operation sperrt.

## 2. Der Vorbedingungsdurchgang

| # | Befund | gemessen an |
|---|---|---|
| **V1** | 🟢 Nächste freie Kennungen gezählt: `CR-2026-155`, `D-440`, `K-175`, Prüfung 97 | Register gezählt |
| **V2** | 🟢 Validator `0 Fehler, 0 Warnungen` am Ausgangsstand (`9b84a2b`) | `validate-framework.py` |
| **V3** | 🟢 Clientversion **vor** dem Messen festgeschrieben: Kommandozeile `2026.09.26-dd393fe`, IDE `3.22.7`; Tarif Free, Modell `auto` | `cursor-agent about`, `cursor --version` |
| **V4** | 🟢 Privacy Mode auf dem Konto eingeschaltet (`privacyMode 2`) | `~/.cursor/cli-config.json` |
| **V5** | ⚠️ Gemessen mit einem **eigenen Messprofil** (`USERPROFILE` auf einen leeren Ordner mit der Konfiguration der Kommandozeile): Im echten Profil liegen Hooks von Claude Code, die der Client mitlädt. Eine Gegenprobe mit dem echten Profil ist gefahren | Befund P2, Gegenprobe E1 |
| **V6** | ⚠️ Gemessen ohne die Variable `SHELL`, wie bei einem Start aus PowerShell: Mit ihr scheitern alle Hook-Kommandos | Befund H1 |

## 3. Die Messungen

**Drei Messmittel:** der Lauf ohne Rückfragen mit `stream-json`-Mitschrift (Werkzeugaufrufe, Ergebnisse, Tokennutzung), ein Aufzeichnungs-Hook für die Eingabeschemata – und der **Programmcode der Kommandozeile**, der im Klartext mitgeliefert wird. Die Befunde stehen einzeln im Protokoll (`tests/protocols/2026-09-26-bau-cursor.md`). **Sechs haben den Bau geändert:**

| # | Befund | Folge |
|---|---|---|
| **P1** | 🔴 **Mit einem Kommentarschlüssel in `.cursor/cli.json` startet der Client nicht** (Exit 1, *„Unrecognized key(s)"*); ebenso mit kaputtem JSON | Ausgabeform ohne Kommentar und Integritätsliste, Prüfung 97 (D-440) |
| **P1/P3** | 🔴 **`Read(.env)` und `Read(**/.env)` sperrten unter Windows nichts** – der Client vergleicht verankert mit dem absoluten Pfad | Jedes Pfadmuster in zwei Schreibweisen mit führendem `*` (D-440) |
| **H1b/H1c** | 🔴 **Die Hook-Eingabe beginnt mit einem BOM**, und mit `failClosed` gilt ein Hook **ohne Ausgabe** als gescheitert – der Schutz-Hook sperrte jede Operation | BOM-feste Eingabe, Sperrform `permission-json` (D-441) |
| **H1d** | 🔴 **Eine Suche über den Ordner `secrets` traf das Muster nicht** | Ordnermuster ohne Pflicht-Trenner (D-442) |
| **X1** | 🔴 **Das Suchwerkzeug beachtet kein `Read`-Verbot** | `.cursorignore` (D-443) |
| **P2b/S1** | 🔴 **Dateien im Arbeitsbereich schreibt der Client ohne Rückfrage**, auch ohne `--force` | `B7` `[NICHT ABBILDBAR]` mit Ersatz |

## 4. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | Messumfang | 🟢 **Kommandozeile gemessen, IDE als geführter Block beim Owner**; Status `pilot` (D-440) | Die IDE ist nicht gemessen (`K-175`) |
| **E2** | Regelablage | 🟢 **`.cursor/rules/*.mdc` mit `alwaysApply` und `globs`, Wurzelanweisung `AGENTS.md`**; Endung je Pack (`rule_file_ext`) | Eigene Regeln des Projekts brauchen die Endung `.mdc` |
| **E3** | Berechtigungen | 🟢 **`.cursor/cli.json` in der Ausgabeform `cursor-json`, Prüfung 97** (D-440) | Kein Rückfragekorb; die Muster sind breiter als die der Kernquelle |
| **E4** | Fremde Konfigurationen und Commit-Attribution | 🟢 **Auskunft durch `install.py` nach dem Inhalt der Dateien**, Nachschritte zur IDE-Einstellung und zur globalen Attribution (D-440) | Eine Auskunft ist keine Schranke |
| **E5** | Schutz-Hook | 🟢 **`failClosed`, Sperrform `permission-json`, BOM-feste Eingabe für alle Packs** (D-441) | Ein Start aus Git Bash sperrt jede Operation |
| **E6** | Das Ordnermuster für Secrets | 🟢 **Für alle Packs ohne Pflicht-Trenner** (D-442) | Eine Datei `secret` ist ebenfalls gesperrt |
| **E7** | Die Lesesperre für die Suche | 🟢 **`.cursorignore` aus den Leseverboten, als Saat** (D-443) | Eine dritte Datei, die das Projekt ergänzt |
| **E8** | Einstufung | **MINOR** – ein neues Modul und eine neue Prüfung, kein Overlay-Bruch | – |
| **E9** | `K-108` (Entscheidung des Owners während des Baus) | 🟢 **Die öffentliche Historie bleibt** (D-444) | Klarname und Adresse bleiben öffentlich |

## 5. Umsetzung

1. `clients/cursor/`: `CLIENT_PACK.md` (35 Matrixzeilen), `manifest.json`, `root-template/.cursor/README.md`.
2. `clientmap.py`: `render_permissions_cursor`, `cursor_koerbe`, `cursor_kernregeln`, `cursor_pfadmuster`, `render_ignore_cursor`, `cursor_ignore_muster`, `render_hooks_cursor`, `regeldatei`.
3. `install.py`: Weiche der Ausgabeform und der Ausschlussdatei; Endung der Regeldateien beim Kopieren der Packs; `readonly` im Agentenprofil; Kanäle nach Inhalt (`json_key`, `json_not`).
4. `hook-check-secrets.py`: BOM-feste Eingabe, Sperrform `permission-json`, `.cursor` in den Strukturmustern, Ordnermuster für Secrets. `hook-overlay-status.py`: Laufzeitregel `.mdc`.
5. `validate-framework.py`: **Prüfung 97**; Prüfung 86 misst bei `permission-json` Sperre und Durchlass; Prüfung 73 kennt `QU-`; die Stellen der Regelablage fragen die Endung des Packs.
6. `probe-pruefungen.py`: Bündel `sonden_cursor` mit neunzehn Einheiten.
7. Register, Roadmap, Anhang 31.4.5, CHANGELOG, `VERSION`, Bestandsliste; Hebung beider Projekte (Schritt 2) und Bau der Erzeugnisse (Schritt 3).

## 6. Entscheidung

🟢 **Angenommen am 2026-09-26, E1 bis E9 wie vorgelegt** – der Owner folgt den Empfehlungen (*„Passt alles.“*); E9 ist seine Entscheidung (*„Historie wird beibehalten“*).

| # | Entscheidung | Decision Record |
|---|---|---|
| E1 bis E4, E8 | Pack mit Zugang, Ausgabeform `cursor-json`, Prüfung 97, Auskunft über fremde Quellen | D-440 |
| E5 | BOM-feste Eingabe und Sperrform `permission-json` | D-441 |
| E6 | Ordnermuster für Secrets | D-442 |
| E7 | `.cursorignore` | D-443 |
| E9 | `K-108` | D-444 |
