# Änderungsantrag `CR-2026-174`

| Feld | Inhalt |
|---|---|
| Titel | Lehren aus der ersten Veröffentlichung ohne Token und die offenen Zellen |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-10-02 |
| Betroffene Artefakte | `governance/RELEASE_PROCESS.md` (Abschnitt 4.2), `.github/workflows/publish.yml`, `tests/scripts/sonden/teil17_paketquellen.py`, `framework/skills/koolie-docs-update`, `koolie-error-analyze`, `koolie-mr-description`, `koolie-review-support`, `koolie-tests` (SKILL, CHANGELOG, TESTS), `framework/skills/koolie-plan/TESTS.md`, `framework/skills/koolie-refactor/TESTS.md`, `framework/skills/koolie-change-analyze/TESTS.md`, `clients/devin-desktop/CLIENT_PACK.md`, Pilot-CHANGELOG, Übungsrepositorium (Rule 20), `docs/ROADMAP.md` |
| Ebene laut Entscheidungsbaum 6 | Framework Core (Skills, Testblätter, Release-Prozess, Workflow), Client Pack `devin-desktop` |
| Art | MINOR-Release: Anweisungsänderung in fünf Skills mit Nachlauf, neue Zellen, Berichtigung des Release-Prozesses |
| Dringlichkeit | geplant (Owner 2026-10-02: Zuschnitt nach Abschluss von `2.0.0`, kein Patch `2.0.1`) |
| Status | 🟢 **entschieden am 2026-10-02** (E1 bis E7); in Umsetzung |

---

## 1. Anlass

`2.0.0` ist als erstes Release über Trusted Publishing auf PyPI und npm gegangen. Der Lauf war nur im letzten Prüfschritt rot, die Einrichtung brauchte drei Handgriffe, die `RELEASE_PROCESS.md` nicht nennt, und Abschnitt 4.2 beschreibt den Abgleich der Prüfsummen falsch. Dazu kommen offene Punkte aus früheren Releases.

## 2. Vorprüfung

- **Erster Workflow-Lauf:** (a) Der Gitea-Push-Spiegel braucht ein GitHub-Token mit Scope `workflow`, sonst lehnt GitHub `main` und die Marke ab. (b) Kommen eine neue Workflow-Datei und die Marke im selben Spiegel-Push, startet kein Lauf. (c) Der npm Trusted Publisher braucht den Haken „Allow npm publish“. (d) Der Prüfschritt fragte npm sofort ab. (e) Abschnitt 4.2 sagt, die Prüfsumme des Workflows stimme mit Schritt 8 überein; über Maschinen gleich ist nur der Inhalt. (f) Die Einrichtungstabelle fehlt um (a) und (c). (g) npm trägt die Version zuerst in die Metadaten ein; die Paketdatei war am 2026-10-02 rund vier Minuten später abrufbar.
- **Externe Suche:** Drei Zellen hielten im Nachlauf von `1.25.0` nicht (`SK-003-P04`, `SK-004-P03`, `SK-004-P02`).
- **K3-Auslöser:** Fünf Skills knüpfen Anhalten und Meldung noch an einen K3-*Fund*; ihre Testblätter haben zusammen 31 Zellen.
- **Planablage und Stufe hoch:** Keine Zelle prüft sie.
- **`devin-desktop`:** Eine Regel mit `trigger: glob` lud 2026-09-26 nicht; die Tech Packs laden darüber.
- **Übung:** Rule 20 hat 6.173 Zeichen, die SOLL-Grenze liegt bei 6.000.
- **Sondenlauf unter Linux:** In WSL-Ubuntu 24.04 fielen 101 Einheiten, weil der Sondenapparat seine Präparationen mit festem `\r\n` sucht; Git checkt dort mit LF aus. Der Validator läuft unter Linux mit 0 Fehlern.
- **Links:** Gemeldet war, dass Links der README auf GitHub nicht öffnen. Alle relativen Links des Repositoriums treffen versionierte Dateien in exakter Schreibung, alle Anker stimmen; GitHub lieferte am 2026-10-02 Dateiseiten auch fremder Repositorien ohne Anmeldung mit 429 oder 503 aus. Kein Bauposten.

## 3. Vorlage zur Entscheidung

| # | Frage | Entscheidung | Preis |
|---|---|---|---|
| E1 | Lehren (a) bis (g) | Alle: Einrichtungstabelle, Reihenfolge von Workflow-Datei und Marke, Abschnitt 4.2 berichtigt; Prüfschritt wartet auf die Paketdatei und vergleicht sha512 mit dem lokal gebauten Paket | 2–2,5 h, 0 Läufe |
| E2 | Scoop und Homebrew (`K-209`) | Zurückgestellt, ohne Ziel-Release | – |
| E3 | Offene Zellen der externen Suche (`K-211`, `K-212`) | Stufe 1: jede Zelle zweimal wiederholen; eine Anweisungsänderung erst nach neuer Vorlage | 1 h, 6 Läufe, ~5 USD |
| E4 | Rule 20 der Übung | Redaktionell unter 6.000 Zeichen, Bedeutung gleich | 0,5 h |
| E5 | Pilot-CHANGELOG mit gesperrtem Begriff | Der Agent ersetzt den Begriff | 0,25 h |
| E6 | `K-161`, `K-165`, `K-170` | Alle drei in `2.1.0` | 8–11 h, ~48 Läufe, ~35 USD und Devin-Guthaben |
| E7 | Ideen `K-213` bis `K-215` | Zurückgestellt | – |
| E8 | Sondenlauf nur auf CRLF (`K-216`, nachgetragen 2026-10-03) | In `2.1.0` beheben, auf dem Ubuntu-Ausweichrechner; Abnahme unter Windows und Linux | 2–4 h, 0 Läufe |
| E9 | Stufe 2 der externen Suche (`K-211`, `K-212`), nachgetragen 2026-10-03 nach F3 | Noch in `2.1.0`: Grenze als Wert im Aufruf, Versionshinweis als eigene Zeile, Suchmuster im Ist-Zustand; Nachlauf aller Zellen der betroffenen Skills (D-303). Deckel angehoben (Owner 2026-10-03: *„lass uns alles in diesem release machen. Hebe ruhig den deckel“*) | rund 30 Läufe, ~30 USD |

Deckel: `claude-code` 80 Läufe und 75 USD nach Listenpreis (bis 2026-10-03: 55 Läufe und 50 USD), `devin-desktop` 8 Läufe.

## 4. Umsetzung

1. **E1:** `RELEASE_PROCESS.md` 0.5.1 – Abschnitt 4.2: Abgleich mit Schritt 8 inhaltlich, Gitea-Anhänge sind die veröffentlichten Bytes; Workflow-Datei und Marke nicht im selben Spiegel-Push; npm braucht nach dem Hochladen einige Minuten; Einrichtungstabelle um den Scope `workflow` des Push-Spiegels und den Haken „Allow npm publish“ ergänzt. `publish.yml`: Der Job `release` wartet bis zu zehn Minuten auf die Paketdatei von npm und vergleicht sie bytegenau mit dem Hochgeladenen; `actionlint` 1.7.12 ohne Befund, der Block gegen `2.0.0` mit Gegenprobe ausprobiert. Prüfung 112 Gegenstand d verlangt das Warten, Sonde `112o`.
2. **E4:** Übung Overlay 1.4.39 – `.devin/rules/20-project-overlay.md` redaktionell von 6.095 auf 5.969 Zeichen.
3. **E5:** Pilot-CHANGELOG: Der gesperrte Begriff ist durch eine neutrale Beschreibung ersetzt; die Git-Historie des Pilots enthält ihn weiter.
4. **E8 (`K-216`, D-542):** Der Sondenapparat liest und schreibt in der Form des Baums. Im Speicher bleibt CRLF, die rund 210 Suchtexte sind unverändert; `roh=True` für erzeugte Dateien und für die Sonden zu Prüfung 81 und Gegenprobe 66b, Sonde 32 außerhalb von Windows ausgelassen und gezählt. Auf dem Ubuntu-Ausweichrechner Teilläufe auf LF und CRLF grün; die Abnahme ist der volle Lauf am Ende von `2.1.0` (Owner 2026-10-03: auf diesem Rechner während der Arbeit nur gezielte Sonden).
5. **E3 (`K-211`, `K-212`), Stufe 1:** Die drei Zellen je zweimal wiederholt (`tests/protocols/2026-10-03-f3-wiederholung.md`, 8 Läufe, 8,25 USD). Keines der drei Kriterien hält verlässlich: der Versionshinweis fehlte in vier von sechs Läufen mit einer Seite, das Suchmuster in einem von zwei, und einer von vier gleichen Analyseläufen forderte wieder 50 Treffer an. Weiter mit E9.


## 5. Entscheidung

🟢 **Angenommen am 2026-10-02** (Owner: *„Mit dem Rest bin ich einverstanden“*, Deckel *„Das passt für mich“*).
