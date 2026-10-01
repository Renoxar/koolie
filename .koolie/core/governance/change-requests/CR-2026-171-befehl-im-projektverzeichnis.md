# Änderungsantrag `CR-2026-171`

| Feld | Inhalt |
|---|---|
| Titel | Der Befehl im Projektverzeichnis – und die Probe, die nur fragte, ob er startet |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-10-01 |
| Betroffene Artefakte | `install_dialog.py` (`--vorgabe`), `paketquellen/koolie_befehl.py`, `paketquellen/README.md`, `README.md`, `README.en.md`, `QUICKSTART.md`, `QUICKSTART.en.md`, `governance/RELEASE_PROCESS.md` (Abschnitt 4.2), `tests/scripts/pruefungen/werkzeuge.py` (Prüfung 112), `tests/scripts/validate-framework.py`, `tests/scripts/sonden/teil17_paketquellen.py`, `docs/ROADMAP.md` |
| Ebene laut Entscheidungsbaum 6 | Framework Core (Installer, Werkzeuge, Validator, Release-Prozess) und Einstieg des Repositoriums |
| Art | PATCH-Release: Bedienung des Befehls und Dokumentation; die Laufzeitschicht im Projekt ändert sich nicht |
| Dringlichkeit | sofort – vor der ersten Veröffentlichung auf PyPI und npm |
| Status | 🟢 **entschieden am 2026-10-01** (E1 bis E5) |

---

## 1. Anlass

Vor dem Hochladen von `1.24.0` auf PyPI probierte der Owner die Version aus TestPyPI in einem eigenen Projektverzeichnis aus: `pip install -i <Index von TestPyPI> koolie==1.24.0`. Er erwartete, dass Koolie damit in das Verzeichnis kommt, in dem er steht. pip installierte nur den Befehl, und zwar in einen Ordner außerhalb des `PATH` (*„The script koolie.exe is installed in … which is not on PATH“*). Der Owner hielt an: *„Stop, ich habe mir das mit dem package installer anders vorgestellt.“*

## 2. Vorprüfung

- **Ein Paket führt beim Installieren keinen Code aus** – gemessen mit `1.22.0` (D-519); das bleibt.
- **`uvx koolie` und `npx koolie`** starten den Befehl im Verzeichnis des Aufrufs, ohne dauerhafte Installation (gemessen). Bis `1.24.0` fragte der Dialog dort trotzdem nach dem Projektverzeichnis, ohne Vorgabe.
- **`python -m koolie`** startet denselben Befehl, auch wenn der Ordner der Skripte nicht im `PATH` steht (gemessen).
- **Beifund:** Das Archiv der Vorabversion `1.24.0.dev1` trug CRLF in jeder Textdatei; der dokumentierte Befehl lief ohne `core.eol=lf`.

Vorgelegt im Chat mit Schätzung: rund 1,5 bis 2 Stunden, kein Sitzungslauf, 0 USD. Der Owner: *„ja, so vorgehen mit 1.24.1“*.

## 3. Vorlage zur Entscheidung

| # | Frage | Entscheidung | Preis |
|---|---|---|---|
| E1 | Was tut `koolie` ohne Argumente? | Der Dialog nimmt das Verzeichnis des Aufrufs als Vorgabe, Enter übernimmt es; nicht im Framework selbst; die Starter unverändert (D-532) | Ein Enter weniger bis zur Installation – nach Anzeige des Befehls und Bestätigung |
| E2 | Was steht zuerst in README und Quickstart? | `uvx koolie`, `pipx run koolie`, `npx koolie` im Projektverzeichnis; `pip install` als „nur der Befehl“ mit `python -m koolie` (D-533) | `pipx run` ungemessen |
| E3 | Was wird veröffentlicht? | `1.24.1` als erste Version auf PyPI und npm; `1.24.0` nicht (D-534) | Eine Marke ohne Paket |
| E4 | Wie läuft die Probe? | Vorabversion auf TestPyPI, die der Owner im eigenen Projekt ausprobiert (D-533) | Eine Rückfrage mehr vor der Signatur |
| E5 | Befehl für das Vorabarchiv | `core.eol=lf`, `core.autocrlf=input` wie das Release-Archiv (D-534) | – |

## 4. Umsetzung

1. `install_dialog.py --vorgabe <verzeichnis>`; `koolie_befehl.py` übergibt `os.getcwd()`.
2. Prüfung 112 startet den Befehl ohne Argumente in einem Wegwerfverzeichnis und verlangt, dass Enter zur nächsten Frage führt; Sonde `112i`.
3. README und Quickstart, deutsch und englisch; `paketquellen/README.md`; Release-Prozess 4.2.

## 5. Entscheidung

🟢 **Angenommen am 2026-10-01.**

| # | Entscheidung | Decision Record |
|---|---|---|
| E1 | Die Vorgabe im Dialog | D-532 |
| E2, E4 | Der Einbefehl-Weg und die Probe beim Owner | D-533 |
| E3, E5 | Erste Version `1.24.1`, das Vorabarchiv | D-534 |

## 6. Messung und Belege

Protokoll `tests/protocols/2026-10-01-befehl-im-projektverzeichnis.md`. Kein Sitzungslauf, 0 USD. Erhebungsablage `leitwerk-erhebungen-2026-10-01-1240` außerhalb des Repositoriums.
