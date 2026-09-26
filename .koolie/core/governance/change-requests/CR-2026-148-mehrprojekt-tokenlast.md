# Änderungsantrag `CR-2026-148`

| Feld | Inhalt |
|---|---|
| Titel | Der Mehrprojektfall und die Token-Last – gemessen, und die Regelablage, die nicht lud |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-26 |
| Betroffene Artefakte | Messapparat: `tests/scripts/validate-output.py`, `tests/erhebungen/mcp-waechter.py`, `tests/erhebungen/cc-overlay-fuellen.py`, `tests/scripts/probe-pruefungen.py` (Bündel `sonden_messapparat`); Client Packs `claude-code`, `devin-desktop`, `openai-codex` (Vorbemerkung des B-Blocks, Zeilen `R2`/`R6` bzw. `B4`); `docs/ADOPTION_GUIDE.md` (Abschnitte 4 und 7); `templates/project-overlay/OVERLAY.md` (Ausfüllhinweis Abschnitt 3); Hauptdokument Kapitel 1; Register: Decision Log, Roadmap, Bestandsliste, Kopf des Hauptdokuments, `VERSION`, Changelog |
| Ebene laut Entscheidungsbaum 6 | **Core** – Messapparat, Client Packs, Übernahmeleitfaden, Overlay-Vorlage |
| Art | **MINOR** nach `RELEASE_PROCESS.md` Abschnitt 1: ein neuer Abschnitt des Übernahmeleitfadens und eine neue Einsatzbedingung in drei Matrizen; kein Overlay muss sich anpassen |
| Dringlichkeit | Posten `1.12.0` nach D-406 |
| Status | 🟢 **entschieden am 2026-09-26** (E1 bis E9), umgesetzt mit `1.12.0` |

---

## 1. Anlass

Der Planabschnitt der Roadmap führte für `1.12.0` zuerst `K-154` (der Messapparat war seit der
Umbenennung an drei Stellen gebrochen), dann `K-138` (den Mehrprojektfall je Pack messen) und
`K-144` (die Token-Last mit und ohne Framework je Pack messen) und daraus den Kostenabschnitt für
Entscheider.

## 2. Vorlage zur Entscheidung

Vorgelegt am 2026-09-26 als Fragen (a) bis (g) mit einer Schätzung von rund 69 Läufen und 10 bis
15 USD, angenommen mit *„Passt alles“*; zu (f) die Angabe des Owners: Devin Pro, Modell
*Claude Opus 5 Medium*.

| # | Frage | Entscheidung und Preis |
|---|---|---|
| **E1** | **`K-154`** (a) | Die drei Werkzeuge berichtigen, dazu den Verweis `DOC-001` beim Packwechsel; je Sonde und Gegenprobe (D-407). **Preis:** Die Sonden messen den Abgleich der Platzhalter, nicht den Lauf des Füllskripts |
| **E2** | **`K-138` – welche Packs** (b) | Alle drei, `claude-code` mit der aktuellen Clientversion nachgemessen; Startort Wurzel und Unterprojekt, Positivkontrolle, verschachtelte Installation, Hook-Nachweis und Textschicht (D-408). 🔴 **Abweichungen:** Bei `devin-desktop` hat das Modell jeden Lesezugriff auf eine `.env` von sich aus verweigert; der Gegenstand im Unterprojekt ist deshalb ein Schreibverbot (`Write(**/*.lock)`, Modus `accept-edits`), und ein Kontrolllauf für genau diese Regel in der Wurzel fehlt – dort hielt das Framework selbst den Lauf lesend. `openai-codex` zuerst ohne Modellaufruf (`codex doctor`, `codex debug prompt-input`), nach dem Hinweis des Owners auf `--no-daemon` auch mit Läufen |
| **E3** | **`K-144` – wie messen** (c) | Drei Aufgaben (T1 Fixlast, T2 kleine Änderung, T3 Analyse), je dreimal, mit und ohne Installation, Eingabe, Cache und Ausgabe getrennt (D-409). 🔴 **Abweichung:** T2 verlangt die Änderung **als Diff in der Antwort** und keine geänderte Datei – eine Schreibaufgabe hätte mit Framework am Freigabepunkt und am `ask`-Korb gehalten und ohne nicht, gemessen wäre der Korb. **Zusätzlich** eine Variante `devin-desktop` mit geladener Regelablage (`K-156`), damit der Kostenabschnitt die Last des Packs nennt, wie es gemeint ist |
| **E4** | **Die Senkung aus `K-144` (2)** (d) | Nicht in `1.12.0` – ein Messrelease, das die gemessene Laufzeitschicht ändert, misst danach etwas anderes. `K-144` (2) bleibt offen, ohne Ziel-Release |
| **E5** | **USD im Kostenabschnitt** (e) | Listenpreis mit Datum und Quelle: `claude-code` die Kostenangabe des Clients (Grundlage Listenpreis), `devin-desktop` die Preisliste des Clients für das gemessene Modell, `openai-codex` dieselbe Preisliste für dasselbe Modell als **Ersatzquelle**, weil der Client keinen Preis nennt. Ein Abo rechnet anders ab; der Abschnitt sagt es |
| **E6** | **Devin-Konto** (f) | Pro, Modell `claude-opus-5-medium` |
| **E7** | **Alte Messbäume** (g) | Gelöscht (`C:\lw-1100`, `C:\lw-1110`, `C:\lw-k148`), Verbindungen einzeln gelöst, geteilter Bestand gegengezählt |
| **E8** | **Befunde des Messtages** (während des Baus) | `K-156` bis `K-159` neu; `K-156` und `K-157` als Patch-Release `1.12.1` vor Kiro eingeplant, `K-158` und `K-159` ohne Ziel-Release (D-410). Die Einplanung folgt der stehenden Anweisung des Owners, Empfehlungen zu folgen – er kann umplanen |
| **E9** | **Projekte heben** | Ja, vor dem Commit, dort committet, nicht gepusht |

> **Empfehlung der Vorbereitung:** (a) bis (g) wie vorgelegt – mit den Abweichungen in E2 und E3.

---

## 3. Umsetzung

1. `K-154`: Kernsuche zwei Ebenen tief in `validate-output.py` und `mcp-waechter.py`;
   `cc-overlay-fuellen.py` mit `<READ_ONLY_PATHS>`, erhaltenen Zeilenenden und übertragenen
   Regelerweiterungen samt Verweis im Overlay-Manifest; Bündel `sonden_messapparat`, Gegenbeweis
   gegen `v1.11.0`.
2. Messung mit dem Übungsrepositorium auf `1.11.0`; die Laufzeitschicht von `1.12.0` unterscheidet
   sich davon nicht. Messbäume unter `C:\lw-1120`, Werkzeuge und Belege außerhalb des Repositoriums
   (`devpacks/leitwerk-erhebungen-2026-09-26-1120/`).
3. Übernahmeleitfaden Abschnitt 4 (Startort, Einsatzszenarien) und Abschnitt 7 (Kosten), Kapitel 1
   des Hauptdokuments, Overlay-Vorlage, die Vorbemerkung des B-Blocks in allen drei Packs, die
   Vorbehalte `K-156` und `K-157` an ihren Zeilen.
4. Register: D-407 bis D-410, `K-138`, `K-144` (1) und (3), `K-154` beantwortet, `K-156` bis `K-159`
   neu; Roadmap; Bestandsliste; `VERSION`.
5. Beide Projekte mit `--target --update` heben.

## 4. Abnahme

Steht im Protokoll `tests/protocols/2026-09-26-mehrprojekt-tokenlast.md`.

## 5. Entscheidung

**E1 bis E9 entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-26; (a) bis (g) vor dem Bau vorgelegt und
angenommen, E2 und E3 mit den benannten Abweichungen, E8 nach der stehenden Anweisung). Decision
Records **D-407** bis **D-410**. Die vier zählbaren Kriterien von D-11 bleiben unverändert
(Kriterium 2 = 1).
