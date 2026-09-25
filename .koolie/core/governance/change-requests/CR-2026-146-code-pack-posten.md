# Änderungsantrag `CR-2026-146`

| Feld | Inhalt |
|---|---|
| Titel | Die Code- und Pack-Posten der Durchsicht – und der Hook, dem nach jeder Hebung neu vertraut werden muss |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-25 |
| Betroffene Artefakte | Werkzeuge: `install.py`, `clientmap.py` (Kommentar), `build/assemble.py`, `build/build-docx.py`, `tests/scripts/validate-framework.py`, neu `tests/scripts/mermaid_renderer.py`, `tests/scripts/probe-pruefungen.py`; Manifest `openai-codex`; Client Packs `openai-codex`, `claude-code`, `devin-desktop` und die Vorlage; `templates/rules/21-overlay-TEMPLATE.md.template`; Core-Module `02-privacy.md`, `03-security.md`; Hauptdokument Kapitel 7a und 15; `docs/PLACEHOLDER_REGISTRY.md`; `onboarding/exercises/README.md`; Register: Decision Log, Roadmap, Bestandsliste, Kopf des Hauptdokuments, `VERSION`, Changelog |
| Ebene laut Entscheidungsbaum 6 | **Core** und **Client Packs** – Werkzeuge, Abbildungsschicht, Regeldokumente |
| Art | **MINOR** nach `RELEASE_PROCESS.md` Abschnitt 1: neue wahlfreie Manifestfelder und ein neues Werkzeugmodul, keine neue Prüfungsnummer, kein Overlay muss sich anpassen |
| Dringlichkeit | Posten `1.10.0` nach D-384 und D-394 |
| Status | 🟢 **entschieden am 2026-09-25** (E1 bis E11), umgesetzt mit `1.10.0` |

---

## 1. Anlass

D-384 hat die Befunde der Durchsicht der Klasse B, die Code oder ein Client Pack ändern, aus
den Durchsichten herausgenommen und für `1.10.0` eingeplant: `K-123`, `K-127`, `K-129`,
`K-136`, `K-145`, `K-151`; `K-125` war zu entscheiden oder zu vertagen.

## 2. Der Vorbedingungsdurchgang

Gemessen am 2026-09-25 am Stand `v1.9.3`.

| Messung | Ergebnis |
|---|---|
| Planabschnitt gegen Register | 🔴 **`K-137` steht im Decision Log für den Pack-Posten nach `1.9.3`, fehlt aber im Planabschnitt der Roadmap** – als Frage (a) vorgelegt |
| `K-123` | Die Ausgabe *„Naechste Schritte“* von `install.py` ist packneutral; Schritt 2 verlangt `_core_rules_integrity` auch bei `openai-codex`; **im Zweig `--update` fehlt der Hinweis auf das erneute Hook-Vertrauen** – der schärfere Teil |
| `K-127` | Kapitel 15 bettet die Berechtigungsdatei fest als `json` ein; das Platzhalterregister führt zwei Packspalten; Kapitel 7a bettet `claude-code` ein, `openai-codex` nur verwiesen |
| `K-129` | (2) durch Lesen erledigt: Die Nennung trägt `40-*.md … soweit vorhanden`. (1) Pack `claude-code` Abschnitt 8.1 nennt die Berechtigungsdatei, Abschnitt 5 die nutzerlokale Datei – beides kann stimmen, zu messen. (3) `0.11.0` am 14. und am 16.09. |
| `K-137` | 🟢 **Zum Teil überholt:** Alle drei Packs führen die Zeile X2; `K-20` ist nur für `devin-desktop` gestellt |
| `K-145` | Validator ruft `mmdc` ohne `-p`; der Bau mit Puppeteer-Konfiguration und Browsersuche. `--mermaid` am Stand: **8 Fehler**, jeder Block |
| `K-151` | Zeile R1 der Vorlage ist wörtlicher Anker der Gegenprobe 73c |

## 3. Vorlage zur Entscheidung

Vorgelegt am 2026-09-25 als Fragen (a) bis (j), angenommen mit *„Passt leg los“*. Während des Baus fragte der Owner nach dem Kostenabschnitt (`K-144`, eingeplant für `1.11.0`) und beauftragte die Einplanung von Kiro (*„Kannst du bitte Kiro nun doch einplanen … nachdem wir unsere bisher geplanten … Minor Releases durch haben?“*, ohne Zugang zum Client, Bau aus der Dokumentation) – E11.

| # | Frage | Entscheidung und Preis |
|---|---|---|
| **E1** | **`K-137` mitnehmen?** (a) | Ja. Der Verweis in `02-privacy.md` geht auf Zeile X2, `K-20` fragt je Pack; keine neue Erhebung, weil die Zeile in allen drei Packs steht (D-397) |
| **E2** | **`K-123`** (b) | Manifestfelder `post_install_steps` und `post_update_steps`; der Integritätsblock nur bei JSON; Sonde und Gegenprobe (D-395). **Preis:** Das Werkzeug nennt, es prüft nicht |
| **E3** | **`K-127`** (c) | Matrix in Kapitel 7a, Sprachangabe aus dem Manifest, Registerspalte, D-32 je Pack (D-396). **Preis:** rund 45.000 Zeichen mehr im Hauptdokument |
| **E4** | **`K-129` (2) bis (4)** (d) | (2) berichtigen; (3) Anmerkung, die Nummer bleibt; (4) nicht kürzen, D-376 bestätigt (D-397) |
| **E5** | **`K-129` (1)** (e) | Gemessen, drei Läufe (D-397) |
| **E6** | **`K-136`** (f) | H4 nennt die Zeitlücke, der Kernsatz spricht von jeder Matrix (D-397) |
| **E7** | **`K-145`** (g) | Gemeinsames Modul, Warnung ohne Browser (D-398). 🔴 **Abweichung von der Vorlage:** Vorgelegt war, die Fehlerausgabe von `mmdc` durchzureichen. Beim Bau zurückgenommen: D-39 schließt genau das aus, weil die Meldung den Diagrammtext zitiert. Stattdessen unterscheidet das Modul Umgebungs- von Diagrammfehlern, ohne die Meldung wiederzugeben – dem Owner im Abschluss gemeldet |
| **E8** | **`K-151`** (h) | Alle fünf Punkte; beim Berichtigen des Kommentars fand sich derselbe falsche Satz in `03-security.md` und ist mitberichtigt (D-399) |
| **E9** | **`K-125`** (i) | Im kleinen Umfang entschieden; die Trennung als `K-152` vorgemerkt (D-400) |
| **E10** | **Projekte heben** (j) | Ja, vor dem Commit, dort committet, nicht gepusht |
| **E11** | **Kiro einplanen** (Auftrag des Owners während des Baus) | Ziel-Release `1.12.0`, nach den geplanten MINOR-Releases; Bau aus der Dokumentation, weil ein Zugang fehlt; Abnahme als eigenes Release; bis dahin keine produktive Freigabe (D-401). Das Planartefakt ist die erste Frage vor dem Bau, die Empfehlung steht in `K-147` |

> **Empfehlung der Vorbereitung:** E1 bis E10 wie vorgelegt – mit der Abweichung in E7.

---

## 4. Umsetzung

1. `install.py`: `nachschritte()`, Integritätsblock nur bei `permissions_format` = `json`;
   Manifest `openai-codex` mit beiden Feldern und einer Notiz.
2. `tests/scripts/mermaid_renderer.py` neu; `validate-framework.py` und `build/build-docx.py`
   nehmen Browser und Konfiguration von dort.
3. `build/assemble.py` Sprachangabe `permissions_format`; Kapitel 7a und 15.4;
   Platzhalterregister.
4. Packs: `openai-codex` `0.1.3` (H4, R3, Abschnitt 6, M6), `claude-code` `0.24.2`
   (`claudeMdExcludes`), `devin-desktop` `0.14.3` (Anmerkung, M6), Vorlage `0.3.2`.
5. Core: `03-security.md` `0.2.4`, `02-privacy.md` `0.1.10`; `K-20` je Pack.
6. `clientmap.py` (Kommentar), Regelvorlage 21, `onboarding/exercises/README.md`.
7. Sondenbündel `sonden_schritte_je_pack` (`D395`, `D395a`) und `sonden_mermaid_umgebung`
   (`D398`, `D398a`); Gegenprobe 73c auf den neuen Anker.
8. Register: Decision Log (D-395 bis D-401, acht Klärungspunkte beantwortet, `K-147` eingeplant, `K-152`), Roadmap
   `0.4.0`, Bestandsliste, Kopf des Hauptdokuments, `VERSION`, Changelog.
9. Beide Projekte mit `--target --update` heben.

## 5. Abnahme

Steht im Protokoll `tests/protocols/2026-09-25-code-pack-posten.md`.

## 6. Entscheidung

**E1 bis E11 entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-25; (a) bis (j) vor dem Bau
vorgelegt und angenommen, E7 mit der benannten Abweichung). Decision Records **D-395** bis
**D-401**. Alle vier zählbaren Kriterien von D-11 bleiben **0**.
