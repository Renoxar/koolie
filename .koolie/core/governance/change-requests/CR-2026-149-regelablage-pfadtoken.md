# Änderungsantrag `CR-2026-149`

| Feld | Inhalt |
|---|---|
| Titel | Die Regelablage, die nur mit Windsurf lädt, und das Sonderziel, das umbenannt wurde |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-26 |
| Betroffene Artefakte | Client Pack `devin-desktop` (Manifest `import_control`, `import_channels_report`; Matrix `R2`, `R6`, Abschnitt 7.1, Skillzeile); Client Pack `openai-codex` (Manifest `permission_path_special`, `permission_path_base`; Matrix `B3`, `B4`, Abbildungstabelle); `clientmap.py` (Rechteprofil); `install.py` (Meldung der Importkanäle); `tests/scripts/probe-pruefungen.py` (Bündel `sonden_importkanaele`, `sonden_pfadtoken_codex`, Sonde zu Prüfung 22); `docs/ADOPTION_GUIDE.md` Abschnitt 7; Hauptdokument Kapitel 1 und 29; Register: Decision Log, Roadmap, Bestandsliste, Kopf des Hauptdokuments, `VERSION`, Changelog |
| Ebene laut Entscheidungsbaum 6 | **Core** – Client Packs, Abbildungswerkzeug, Installer |
| Art | **PATCH** nach `RELEASE_PROCESS.md` Abschnitt 1: zwei Befunde an Packs behoben, die ihre ausgelieferte Zusage nicht hielten; keine neue Prüfung, kein Overlay-Feld |
| Dringlichkeit | Posten `1.12.1` nach D-410, vor Kiro |
| Status | 🟢 **entschieden am 2026-09-26** (E1 bis E8), umgesetzt mit `1.12.1` |

---

## 1. Anlass

Der Messtag von `1.12.0` fand zwei Befunde an Packs (D-410): Bei `devin-desktop` lädt die
Regelablage `.devin/rules/` mit der ausgelieferten Einstellung `read_config_from.windsurf: false`
nicht (`K-156`); `openai-codex` 0.157.0 ignoriert die `:workspace`-Pfadeinträge seines
Rechteprofils (`K-157`).

## 2. Vorlage zur Entscheidung

Vorher ohne Kontingent recherchiert: Die Herstellerdokumentation von Devin CLI führt `.devin/rules/`
als eigenen Ablageort, **unabhängig** von der Importsteuerung – `K-156` widerspricht ihr. Der
Schlüssel `windsurf` importiert Regeln aus `.windsurf/rules/` und `.windsurf/global_rules.md`,
Skills und MCP-Server; dazu sind `copilot`, `opencode` und `zed` dokumentiert, alle mit Standard
`true`. Bei Codex heißt das Sonderziel seit 0.157 `:workspace_roots`, mit den Unterpfaden als
eigener Tabelle. Vorgelegt am 2026-09-26 als Fragen (a) bis (f) mit einer Schätzung von rund
30 Läufen und 3 bis 5 USD, angenommen mit *„Ich stimme zu“*; dazu die Angabe des Owners: Devin und
Codex aktualisiert, Codex läuft wieder ohne `--no-daemon`.

| # | Frage | Entscheidung und Preis |
|---|---|---|
| **E1** | **Abhilfe für `K-156`** (a) | `windsurf: true`; `install.py` meldet die Kanäle, die das öffnet, wenn sie belegt sind (D-411). **Preis:** Der Kanal aus D-290 ist offen, gemeldet wird er nur beim Lauf des Installers |
| **E2** | **Devin zuerst aktualisieren und nachmessen** (b) | Ja – 3000.11.3; der Befund besteht fort, (a) bleibt nötig |
| **E3** | **`copilot`, `opencode`, `zed`** (c) | Auf `false`, in derselben Zeile `R6`. 🔴 **Abweichung:** Die Wirkung von `copilot: false` ist nicht messbar – `.github/skills/` lud auch ohne Schalter nicht |
| **E4** | **Umfang von `K-157`** (e) | Eng: die Tabelle `:workspace_roots`, `B4` und `B1` nachgemessen (D-412). **Zusätzlich**, weil ohne Kontingent möglich: die Pfadseite mit `codex sandbox` ohne Modellaufruf |
| **E5** | **`B3`** (e) | Nicht in diesem Release; die dokumentierten `deny`-Globs werden `K-160` (D-413) |
| **E6** | **Meldung an den Hersteller** (d) | Der Owner meldet den Fehler an der Regelablage; Reproduktion ist der Minimalbaum (D-413) |
| **E7** | **Befund während des Baus** | Eine Regel mit `trigger: glob` lädt nicht → `K-161`, ohne Ziel-Release (D-413) |
| **E8** | **Modelle und Projekte** (f) | Devin Pro, `claude-opus-5-medium`; Codex mit der Voreinstellung des Kontos. Beide Projekte heben, vor dem Commit, dort committen, nicht pushen |

> **Empfehlung der Vorbereitung:** (a) bis (f) wie vorgelegt – mit der Abweichung in E3.

---

## 3. Umsetzung

1. `devin-desktop`: Manifest `import_control` (`windsurf: true`, `copilot`/`opencode`/`zed`: `false`)
   und `import_channels_report`; `install.py` meldet belegte Kanäle nach Installation und Hebung;
   Bündel `sonden_importkanaele`; die Sonde zu Prüfung 22 verfälscht `cursor` statt `windsurf`.
2. `openai-codex`: `clientmap.py` erzeugt die Tabelle `":workspace_roots"`, das Manifest führt das
   Sonderziel; Bündel `sonden_pfadtoken_codex`.
3. Messung in Minimalbäumen und einer Installation unter `C:\lw-1121`, Werkzeuge und Belege außerhalb
   des Repositoriums (`devpacks/leitwerk-erhebungen-2026-09-26-1121/`).
4. Matrizen, Kostenabschnitt, Kapitel 1 und 29; Register: D-411 bis D-413, `K-156` und `K-157`
   beantwortet, `K-160` und `K-161` neu; Roadmap; Bestandsliste; `VERSION`.
5. Beide Projekte mit `--target --update` heben; im Übungsrepositorium `read_config_from` von Hand
   nachziehen – `install.py` fasst die Berechtigungsdatei nicht an.

## 4. Abnahme

Steht im Protokoll `tests/protocols/2026-09-26-regelablage-pfadtoken.md`.

## 5. Entscheidung

**E1 bis E8 entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-26; (a) bis (f) vor dem Bau vorgelegt und
angenommen, E3 mit der benannten Abweichung, E7 nach der stehenden Anweisung). Decision Records
**D-411** bis **D-413**. Die vier zählbaren Kriterien von D-11 bleiben unverändert (Kriterium 2 = 1).
