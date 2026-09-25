# Protokoll: Die Durchsicht der Klasse B, erster Bereich – und die Grenze ohne Sonde

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-25 |
| Release | `1.9.1` |
| Änderungsantrag | `CR-2026-143` |
| Art | Durchsicht der Regeldokumente (Core-Module und Laufzeitschicht) nach `docs/DOCUMENTATION_STANDARD.md`, zwei Klärungspunkte beantwortet, Sonden für die Zeichengrenze – **keine Sitzung mit einem Client, kein Kontingent** |
| Gegenstand | die elf Core-Module, die neun Dateien der Laufzeitschicht, die Modusbegriffe außerhalb der Register, die `.gitignore` des Quellrepositoriums, die installierte Länge der Wurzel-Anweisung je Pack |
| Ergebnis | 🟢 **Entschieden, `D-381` bis `D-384`.** Kein Regelinhalt geändert; zehn Core-Module und eine Laufzeitdatei überarbeitet, keine Laufzeitdatei länger; sieben Befunde als Klärungspunkte; `K-124` und `K-126` beantwortet; die Zeichengrenze der Prüfung 4 hat Sonden je Pack |

---

## 1. Was gefragt war

Wiederaufnahmepunkt von `1.9.0`, Punkt 2: die Durchsicht der Klasse B, erster Bereich
(D-380). Vorher zu klären war, wie eine Änderung an der Laufzeitschicht die Projekte
erreicht und die Zeichengrenze einhält, und welche der Klärungspunkte `K-123` bis `K-129` in
dieses Release gehören. Fragen (a) bis (i) vorgelegt am 2026-09-25 und angenommen; zu (c)
fragte der Owner, woher die Grenze kommt und ob sie sich anheben lässt – beantwortet
(Vorgabe des Frameworks seit `CR-2026-027` E3, kein technischer Grund) und als `K-130`
eingeplant. `CR-2026-143` E1 bis E8.

## 2. Messungen vor dem Bau

Je eine Testinstallation je Pack (`install.py --client <pack> --root <leer>`), Zeichen, nicht
Bytes.

| Träger | `claude-code` | `devin-desktop` | `openai-codex` |
|---|---|---|---|
| Wurzel-Anweisung | 11.894 | 11.887 | 12.516 (Grenze gilt nicht) |
| `00-framework-core.md` | 5.142 | 4.853 | 5.090 |
| `10-privacy-security.md` | 5.168 | 4.801 | 5.160 |
| `15-development-rules.md` | 3.670 | 3.303 | 3.662 |
| `20-project-overlay.md` | 3.899 | 3.609 | 3.846 |

Die Quelle `framework/runtime/root-instruction.md` hat 11.924 Zeichen. **Nach dem Bau sind
die Werte der Wurzel-Anweisung unverändert** (Bündel `sonden_zeichengrenze`, siehe
Abschnitt 4); die Laufzeitregeln sind unverändert, `fw-reviewer.md` hat 1.610 statt 1.612
Zeichen.

## 3. Die Durchsicht

Fünf parallele Durchgänge nach einem gemeinsamen schriftlichen Auftrag (Kriterien der Klasse
B, harte Grenzen: kein Regelinhalt, keine Nummer, kein Anker, keine längere Laufzeitdatei;
Validator nach jeder Datei). Registereinträge, Sonden und Versionen danach in einem Schritt.

| Durchgang | Geändert | Sachlich berichtigt |
|---|---|---|
| `00`, `01`, `04`, `06`, `07` | alle fünf; `01` drei Herleitungen durch D-105, D-291, D-114 ersetzt; Anführungszeichen in `04`, `06`, `07` | `00`: Verweis auf Anhang 31.4 (der alte Anhangtitel existiert nicht mehr); `06`: der Aufrufweg eines Skills galt als werkzeugneutral `/skill-name` `[DOK]`, bei `openai-codex` steht er auf `BELEG OFFEN` – jetzt Verweis auf Zeile S2 der Fähigkeitsmatrix |
| `02`, `03` | beide; `03` Herleitungen zu D-59, D-76, D-22 ersetzt, `K-126` an vier Stellen | `02`: der Schutz-Hook prüft Lese-, Such-, Schreib- und Ausführungsanfragen (D-33, `hooks.json`), nicht nur die letzten beiden; *„und war es nie“* war falsch (D-59); `03`: ein Querverweis, *„beider Fachmatrizen“* bei drei Packs |
| `05`, `10` | `05`; `10` unverändert | `05`: *„der eine Client“* durch den Verweis auf `skill_frontmatter.drop_fields` ersetzt |
| `08`, `09` | beide; `08` Herleitung zu D-303 gestrichen, `09` Herleitung zu D-54 | `08`: der Ablagepfad je Client steht im Laufzeitglossar, Alternativpfade im Pack |
| Laufzeitschicht | nur `agents/fw-reviewer.md` | der Herkunftskommentar nannte `allowed-tools` als Feld des Clients; `install.py` setzt den Feldnamen je Pack (`agent_frontmatter.tools_field`) |

**Befunde, die eine Entscheidung brauchen** – als Klärungspunkte angelegt, nicht behoben
(D-381 (b)):

| Kennung | Fundstelle | Befund |
|---|---|---|
| `K-131` | `08-skill-conventions.md` Abschnitt 3 | *„ausschließlich belegte Felder“* beschreibt die gerenderte Fassung, nicht die Quelle |
| `K-132` | `09-risk-model.md` R12 | *„erweiterte Permission-Modi“* als hoch – nicht abgegrenzt gegen D-05 und D-35 |
| `K-133` | `rules/00-framework-core.md` | M1 als Standardmodus ohne Grundlage im Core-Modul |
| `K-134` | `10-error-escalation.md`, `05-working-model.md` | Kennung S3 doppelt belegt; S2 ohne Bereitstellung ohne Eskalationsstufe |
| `K-135` | `rules/10-privacy-security.md` | pauschal hoch, wo R3/R4 mittel sagen |
| `K-136` | `clients/openai-codex/CLIENT_PACK.md` H4 | die Grenze des Hooks (D-63) nicht genannt |
| `K-137` | `02-privacy.md` Abschnitt 1.2 | Verweis auf `K-20`, das nur ein Pack betrifft |

**Modusbegriffe (`K-126`, D-382):** umgestellt an 16 Stellen in 13 Dokumenten außerhalb der
Register (`03` drei, `05`, `09`, das Onboarding fünf, sechs weitere je eine); der Testkatalog (`FW-NE-03`), das Testblatt von `fw-change-small` und das Decision
Log bleiben, wie sie geschrieben wurden. Die Kapitelquellen des Hauptdokuments nennen die
Namen schon ausdrücklich als die von `devin-desktop` (`05-glossar.md`, `09-betriebsmodi.md`).

## 4. Wirkungsnachweis – Sonden und Gegenproben, mit Gegenbeweis

| Einheit | Gegenstand | Ergebnis |
|---|---|---|
| Sonde 45e | `/.codex/` fehlt in der `.gitignore` des Quellrepositoriums | gemeldet |
| Gegenprobe 45c | `.codex` statt `/.codex/` | unbeanstandet |
| Sonde 4a | Wurzel-Anweisung einer `claude-code`-Installation auf 12.001 Zeichen verlängert | gemeldet |
| Gegenproben 4a, 4b, 4c | frische Installation je Pack | unbeanstandet; `openai-codex` bei 12.516 Zeichen, weil die Grenze dort nicht gilt |

**Gegenbeweis (Gegenstand 3 der Prüfung 45):** Der neue Validator gegen die `.gitignore` von
`v1.9.0` meldet **fünf** Befunde – `/.claude`, `/.codex`, `/.mcp.json.example`,
`/CLAUDE.local.md.example`, `/CLAUDE.md`. Und
der Validator aus `v1.9.0` gegen eine Kopie des fertigen Baums ohne die Zeile `/.codex/`:
**0 Fehler** – er kennt den Gegenstand nicht; der neue gegen dieselbe Kopie: **1 Fehler**,
genau diese Zeile (die vier Warnungen beider Läufe kommen aus der Kopie ohne Repositorium).

## 5. Abnahme

| Lauf | Ergebnis |
|---|---|
| Validator | **0 Fehler, 0 Warnungen**, beide Kodierungsumgebungen |
| Sondenlauf | **344 Einheiten, alle bestanden** (vorher 341; neu Sonde 45e, Gegenprobe 45c und das Bündel `sonden_zeichengrenze`), beide Kodierungsumgebungen Exit 0 und oberhalb der Trennlinie zeilengleich (600 Zeilen), rund 660 s Wanduhr je Lauf; **Abnahmelauf gegen den fertigen Baum** zeilengleich |
| Gegenbeweis | Validator aus `v1.9.0` gegen den Baum ohne `/.codex/`: 0 Fehler; der neue: 1 Fehler (Abschnitt 4) |
| Pilot / Übungsrepo `--strict-overlay` nach der Hebung | beide mit `--target --update`, **557 Kerndateien**, `LIEFERUMFANG` = `voll`; aktualisiert nur `fw-reviewer` und `fw-change-small` (`SKILL.md`, `CHANGELOG.md`). Pilot **1 Fehler, 2 Warnungen**, alle im projekteigenen `CHANGELOG.md`; Übungsrepo **0 Fehler, 1 Warnung** (Länge der eigenen Regeldatei) – beide unverändert zum Vorstand. Overlay `0.3.15` bzw. `1.4.9`, lokal committet |
| Bau | alle drei Word-Fassungen `v1.9.1` in `build/out/` (1.949.550 / 1.950.830 / 1.945.428 Bytes für `devin-desktop` / `claude-code` / `openai-codex`), im Erzeugnis nachgezählt: Dokumentversion `1.9.1`, *„94 Prüfungen über 557 versionierte Dateien“* (Prüfung 78), Kapitel 31.1 mit **557** Dateien und **78** installierten Dateien je Pack, eingesetzt vom Bau; die eingebetteten Core-Module führen den Sachbegriff des Modus |

## 6. Nebenhandlungen außerhalb des Kerns

- Signierte Marke `v1.9.0` (vom Owner gesetzt, `Good "git" signature`) **vor** dem
  Gitea-Release gepusht. Schritte 5 bis 7 aus `RELEASE_PROCESS.md` 4.1 mit
  `-c tar.umask=022`: `koolie-1.9.0.tar.gz`, **562 Dateien** = `git ls-tree` der Marke, kein
  CRLF, `install.command` `0755`, alle übrigen 561 Dateien `0644`, Lizenz an beiden Stellen
  gleich, kein `build/out/`; zweimal erzeugt, bytegleich. Gitea-Release mit Archiv und
  Prüfsumme, beide Anhänge bytegleich zurückgelesen.

## 7. Befunde während des Baus

- **Die Zeichengrenze der Prüfung 4 hatte keine Sonde** – weder für den Fehler noch für den
  ausgelieferten Stand je Pack. Gefunden beim Vorbereiten von (c).
- **Ein Durchgang hat in drei seiner Dateien mit einem Ersetzungsskript Text zerstört** und die
  Dateien vor dem Neuaufbringen aus dem Repositorium zurückgesetzt; der Endstand ist gültiges
  UTF-8 mit CRLF und validiert still. Die Harte Regel *„Ersetzungen mit Python und
  `newline=""`“* hat den Schaden nicht verhindert, die Rücksetzung auf den Index hat ihn
  begrenzt.
- **Ein Durchgang setzte einen Packnamen als Handelnden in den Kern** (*„kennt `claude-code`
  für Skills nicht“*). Prüfung 14 erkennt Produktnamen, nicht Packkennungen in Backticks; die
  Stelle verweist jetzt auf das Manifestfeld.

## 8. Offen und benannt

- `K-130` bis `K-137`; `K-128` für `1.9.2`, `K-123`, `K-125`, `K-127`, `K-129`, `K-136` für
  `1.10.0` (D-384).
- Die Abnahme des macOS-Starters auf macOS (aus `1.7.0`).
