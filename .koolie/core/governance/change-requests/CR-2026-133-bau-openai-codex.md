# Änderungsantrag `CR-2026-133`

| Feld | Inhalt |
|---|---|
| Titel | Der Bau des Client Packs `openai-codex` – und der Schutz-Hook, der lief und nichts verhinderte |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-23 |
| Betroffene Artefakte | `.koolie/core/clients/openai-codex/**` (neu); `.koolie/core/clientmap.py`; `.koolie/core/install.py`; `.koolie/core/tests/scripts/hook-check-secrets.py`; `.koolie/core/tests/scripts/validate-framework.py` (**Prüfungen 86, 87, 88**); `.koolie/core/tests/scripts/probe-pruefungen.py`; `.koolie/core/clients/README.md`; `.koolie/core/OWNERS.md`; `.koolie/core/docs/ROADMAP.md`; `.koolie/core/governance/DECISION_LOG.md` (**D-346** bis **D-349**, `K-117` beantwortet, `K-118`, `K-119`); `.koolie/core/tests/TEST_CATALOG.md`; `.koolie/core/build/doc/00-kopf.md`, `.koolie/core/build/doc/26-qs-test.md`; `.koolie/core/VERSION`; `.koolie/core/CHANGELOG.md`; `.koolie/core/governance/ADOPTION_REGISTRY.md`; `UEBERGABE.md` |
| Ebene laut Entscheidungsbaum 6 | Abbildungsschicht und Prüfapparat |
| Art | **Änderung.** MINOR-Release nach `RELEASE_PROCESS.md` Abschnitt 1 – ein neues Modul und drei neue Prüfungen, **ohne Overlay-Bruch**: Kein Träger des Overlays ändert seine Gestalt |
| Dringlichkeit | regulär – der Posten steht seit dem 2026-09-12 im Plan und ist mit `1.3.0` auf diese Nummer gerückt (D-341) |
| Status | 🟢 **entschieden am 2026-09-23** (E1 bis E5) |

---

## 1. Anlass

**Der Bau des dritten Client Packs.** Die Erhebung ist mit `1.3.0` gefahren (`CR-2026-132`), und sie hat fünf Fragen hinterlassen, die vor dem ersten geschriebenen Trägerbyte stehen (Abschnitt 7 des dortigen Protokolls). Dieses Release beantwortet sie – **und hat dabei drei Befunde erzeugt, die in keiner der fünf standen.**

🔴 **Der schwerste davon ist keiner des Packs, sondern des Kerns:** Der ausgelieferte Schutz-Hook lief bei diesem Client, gab seine Sperre aus und **verhinderte nichts.**

## 2. Der Vorbedingungsdurchgang

| # | Befund | gemessen an |
|---|---|---|
| **V1** | 🟢 Die Tabelle *Nächste freie Kennungen* stimmt – **zum dritten Mal in Folge** | 345 `D`-Registerzeilen bis `D-345`, 115 `K`-Zeilen bis `K-117` (Lücken 95 und 99), 132 Anträge bis `CR-2026-132`, 20 `G`-Zeilen bis `G-20`, `UEB-31`; alle fünf Gattungen nachgezählt, nicht gelistet (D-345) |
| **V2** | 🟢 Die geprüfte Clientversion ist **vor** dem Bauen festgeschrieben: `0.156.1`, unverändert seit der Erhebung | `codex --version`, `codex doctor` |
| **V3** | 🟢 **Die Word-Fassung steht auf `v1.3.0`** – Schritt 3 von Abschnitt 4.1 hat bei `1.3.0` gehalten. **Gezählt, nicht gelistet** (D-345): 16 Einträge in `build/out/`, beide Fassungen darunter | `ls … \| wc -l`, dann vollständig gelesen |
| **V4** | 🟢 Bestandsliste in allen drei Trägern byte-gleich auf `1.3.0`; **beide** Projekte tragen die Hebung als Commit (`e35b8fc`, `5d7de8d`) | `cmp`, `git log` |
| **V5** | 🟢 Validator `0 Fehler, 0 Warnungen` über **85** Prüfungen; Arbeitsbaum sauber, kein offener Antrag, kein Restbranch | `validate-framework.py`, `git` |
| **V6** | 🔴 **`K-117` besteht fort und ist erneut gemessen: 38 von 525 Kerndateien in `devpacks/otp-generator` sind nicht versioniert** (zuvor 42) | `find` gegen `git ls-files` |
| **V7** | ⚠️ Die Benutzerkonfiguration des Clients führt weiter den Vertrauenseintrag auf den **alten** Projektnamen – **und einen auf das Benutzerprofil selbst** | gelesen; unverändert seit `1.3.0` |

🔴 **Keine Prüfung erreicht V7**, und sie kann es auch nicht: Der Träger liegt außerhalb des Repositoriums (`K-118`).

## 3. Die Erhebung des Baus – dreißig Messungen, davon sechsundzwanzig kostenfrei

**Vier Meßmittel, drei davon ohne Kontingent:** `codex debug prompt-input` (der Kontext, ohne eine Anfrage zu stellen), `codex doctor --all` (das wirksame Profil und jeder unbekannte Konfigurationsschlüssel **mit Namen**), `codex execpolicy check` (der Regelauswerter der Engine selbst) – und **25 Sitzungsläufe** an einer realen Installation für das, was nur ein Lauf zeigt.

🔴 **Die Isolation war wieder Bedingung, nicht Vorsicht:** Alle Messungen liefen gegen ein eigenes Benutzerverzeichnis im Ablagebereich; die Konfiguration des Arbeitsplatzes ist nicht angefaßt worden.

Die dreißig Befunde stehen im Protokoll (`tests/protocols/2026-09-23-bau-openai-codex.md`). **Drei davon haben den Bau geändert:**

| # | Befund | Folge |
|---|---|---|
| **M22** | 🔴 **Die Sperrform des Schutz-Hooks ist clientgebunden – und die ausgelieferte wirkt hier nicht.** `{"decision": "block"}` und Exit 2: Der Client meldet *PreToolUse Failed* und **führt die Operation aus**; Gegenlauf mit Köderinhalt. `hookSpecificOutput.permissionDecision = "deny"` blockiert, auch im Modus ohne Rückfragen und ohne Sandkasten | **D-347**, `--sperrform`, **Prüfung 86** |
| **M21/B4** | 🔴 **Das Schreibwerkzeug führt keinen Pfad in einem Feld**, sondern einen **Patchtext** – der Pfad steht darin hinter einem Leerzeichen, und die Pfadmuster des Hooks kannten als Grenze nur den Schrägstrich. Die Datei im Kernverzeichnis wurde angelegt | **D-347**, erweiterte Grenze, **Verschärfung für alle drei Packs** |
| **M9/M11** | 🔴 **`B3` fällt an zwei Enden zugleich:** Ein Muster verlangt einen absoluten Vorsatz (nicht versionierbar), ein projektrelativer Schlüssel nimmt kein Muster – **und** ein `deny`-Leserecht verlangt den erhöhten Windows-Sandkasten, ohne den der Client gar nicht läuft | **D-346**, `[NICHT ABBILDBAR]`, Abschnitt 4 des Packs |

## 4. Die fünf Fragen aus `1.3.0` – beantwortet

| # | Frage (Protokoll `1.3.0`, Abschnitt 7) | Antwort |
|---|---|---|
| **1** | Zweite Ausgabeform für `clientmap.py`? | 🟢 **Ja, und es sind zwei Erzeugnisse:** `render_permissions_toml()` für die Pfadseite, `render_exec_policy()` für die Befehlsseite. **Das Ziel entscheidet über die Abbildung**, nicht mehr die Quelle allein (D-346) |
| **2** | Wie steht das Vertrauensmodell im B-Block? | 🟢 **Als zweite Vorbemerkung des Blocks** – es betrifft die ganze projektlokale Schicht, nicht einzelne Zeilen – **und als Bedingung in `B1`, `H1` und `H2`.** Dazu ein eigener Abschnitt 1b des Packs und ein Schritt in `install.py` |
| **3** | Wie steht die verdrängbare Wurzel-Anweisung in `R1`? | 🟢 **`[TECHNISCH]` mit benannter Bedingung**, dazu **drei** Maßnahmen: Schreibschutz im `deny`-Korb, Aufnahme in die Muster des Schutz-Hooks und **Prüfung 88**, die die Datei meldet |
| **4** | Abbildung der Ladetrigger, wenn es keine gibt? | 🟢 **`rule_frontmatter: "comment"` und `root_instruction_imports`** – zwei Mechaniken aus 0.15.0 bekommen ihren ersten Gegenstand. Kein Trigger wird ersatzlos verworfen (D-26, D-27); der Ersatz ist die **Nennung**, und er ist schwächer (D-348) |
| **5** | Eine oder beide Skillablagen? | 🟢 **Beide werden genannt, eine wird geschrieben.** Das Framework schreibt `.codex/skills/`; `.agents/skills/` steht in der Pfadabbildung und in Abschnitt 7 als Auskunft nach D-34 |

## 5. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | Bekommt `clientmap.py` eine zweite Ausgabeform – und was geschieht mit den Prüfungen, die nur die erste lesen? | 🟢 **Ja, zwei Erzeugnisse aus einer Quelle** – und die betroffenen Prüfungen stehen **benannt** in `FORMATGEBUNDENE_PRUEFUNGEN`; **Prüfung 87** verlangt ihre Nennung in Abschnitt 5 des Packs, in beide Richtungen. Sie still zu überspringen wäre die Bauform von `0.57.0` | ⚠️ **Sechs Prüfungen erreichen dieses Pack nicht** (2, 37, 42, 43, 54, 76). Die Lücke ist erklärt und gezählt, aber sie ist da. ⚠️ **Zweiter Preis:** `install.py` rendert dieselbe Quelle zweimal; wer eine dritte Form baut, faßt `render_for_client` erneut an |
| **E2** | Was folgt aus der wirkungslosen Sperrform des Schutz-Hooks? | 🔴 **Das Skript kennt zwei Formen, das Pack sagt seine, die Abbildung hängt sie ans Kommando** – dieselbe Begründung wie bei `--fail-closed` (D-31). **Prüfung 86** mißt die **Kette** und nicht das Manifestfeld. **Und die Pfadgrenze des Hooks wird erweitert** – für alle drei Packs, weil es eine Verschärfung ist | ⚠️ **Der Standard bleibt die alte Form.** Ein Pack, das eine neue braucht, muß sie sagen – wer es vergißt, bekommt einen Hook, der nichts sperrt. **Genau das fängt Prüfung 86 nur, wenn das Pack die Form nennt**; ein Pack, das schweigt, läuft durch. ➡️ *Die Grenze ist benannt und sie bleibt* |
| **E3** | Wie werden Regeldateien abgebildet, wenn der Client keine Ladebedingung kennt? | 🟢 **Über die Nennung in der Wurzel-Anweisung** (`root_instruction_imports`), und die Prüfung darauf verlangt die **Nennung** statt der geratenen `@`-Form | 🔴 **Der Ersatz ist schwächer, und das ist der Preis:** `R2` und `R3` stehen auf `[NICHT ABBILDBAR]` statt auf `[TECHNISCH]`. ⚠️ **Verworfen: die Regeltexte einbetten** – das erzeugte eine zweite Schrift derselben Regel und hätte die Overlay-Laufzeitregel in eine Datei geschrieben, die `--update` überschreibt |
| **E4** | `K-117` – die drei Fragen | 🟢 **(1) ja, (2) ja, (3) nein.** `install.py` meldet am Ende, welche der geschriebenen Kerndateien das Projekt ignoriert; der Übernahmeleitfaden nennt die Negativregel. Bauform von D-34 | ⚠️ **Eine Auskunft, keine Schranke** – das `.gitignore` gehört dem Projekt. ⚠️ **Ohne Git gibt sie eine leere Liste**; eine Auskunft, die nicht erhoben werden kann, wird nicht behauptet |
| **E5** | Einstufung | **MINOR.** Ein neues Modul und drei neue Regeln, **kein Overlay-Bruch** – kein Träger des Overlays ändert seine Gestalt | – |

## 6. Umsetzung

1. `clients/openai-codex/`: `CLIENT_PACK.md` (34 Matrixzeilen), `manifest.json`, `root-template/.codex/README.md`.
2. `clientmap.py`: die zweite Ausgabeform, `hook_block_form`, `hook_handler_extra`, `hook_project_dir_expr`, `hooks_file_wrapper`.
3. `install.py`: zielabhängige Abbildung; die Schlußmeldung über ignorierte Kerndateien.
4. `hook-check-secrets.py`: `--sperrform`, erweiterte Pfadgrenze, `.codex/` und `AGENTS.override.md` in den Mustern.
5. `validate-framework.py`: `FORMATGEBUNDENE_PRUEFUNGEN`, `formatgebunden()`, **Prüfungen 86, 87, 88**; Prüfung 21 mißt die Nennung statt der `@`-Form.
6. `probe-pruefungen.py`: sechs neue Einheiten, je Prüfung eine Sonde und **zwei** Gegenproben.
7. `clients/README.md` (0.7.0), `OWNERS.md`, `docs/ROADMAP.md`, `DECISION_LOG.md`, `TEST_CATALOG.md`, `build/doc/00-kopf.md`, `build/doc/26-qs-test.md`, `CHANGELOG.md`, `VERSION`, `ADOPTION_REGISTRY.md`.
8. Protokoll mit allen dreißig Messungen und ihren Gegenproben.
9. 🔴 **Der Bau faßt die Konfiguration des Arbeitsplatzes nicht an** – alle Messungen gegen ein eigenes Benutzerverzeichnis im Ablagebereich.
10. 🔴 **Die Übergabe wird VOR dem Abnahmelauf gehoben** (Falle 1 aus `1.2.0`); nur die Laufzeiten stehen unterhalb der Trennlinie (D-94).
11. Validator und Sondenlauf in **beiden** Kodierungsumgebungen (D-49).
12. 🔴 **Nicht gefahren, und ausdrücklich entschieden:** Das Heben der übernehmenden Projekte (Schritt 2) und der Bau der Erzeugnisse (Schritt 3) sind am 2026-09-23 auf Entscheidung des Framework Owners **verschoben** worden. ⚠️ **Der Preis ist benannt:** Die Bestandsliste steht damit für einen Tag auf einer Zahl, die im Projekt noch nicht angekommen ist – die Grenze von D-331. **Beides steht als erster Punkt des Wiederaufnahmepunkts.**

## 7. Entscheidung

🟢 **Angenommen am 2026-09-23, E1 bis E5 wie vorgelegt.**

| # | Entscheidung | Decision Record |
|---|---|---|
| E1 | Zwei Ausgabeformen, und die formatgebundenen Prüfungen stehen benannt | **D-346** |
| E2 | Die Sperrform des Schutz-Hooks ist clientgebunden und wird gesagt | **D-347** |
| E3 | Regeln über die Nennung; die Prüfung mißt die Nennung statt der `@`-Form | **D-348** |
| E4 | `install.py` meldet die ignorierten Kerndateien – Auskunft, keine Schranke | **D-349** |
| E5 | MINOR | – |

Beantwortet: `K-117`. Neue Klärungspunkte: **`K-118`** (kann eine Prüfung den Vertrauenseintrag erreichen?) und **`K-119`** (welche Seite gewinnt zwischen Arbeitsplatz- und Projektregel?).
