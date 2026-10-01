# Änderungsantrag `CR-2026-170`

| Feld | Inhalt |
|---|---|
| Titel | Die erste Veröffentlichung auf PyPI und npm – und die beiden Tokens, die eines waren |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-10-01 |
| Betroffene Artefakte | `paketquellen/bauen.py`, `paketquellen/README.md`, `README.md`, `README.en.md`, `QUICKSTART.md`, `QUICKSTART.en.md`, `governance/RELEASE_PROCESS.md` (Abschnitt 4.2, Schritt 9), `tests/scripts/pruefungen/werkzeuge.py` (Prüfung 112), `tests/scripts/validate-framework.py`, `tests/scripts/sonden/teil17_paketquellen.py`, `docs/ROADMAP.md` |
| Ebene laut Entscheidungsbaum 6 | Framework Core (Werkzeuge, Validator, Release-Prozess) und Einstieg des Repositoriums |
| Art | Erste Veröffentlichung über Paketquellen; MINOR-Release ohne Kontingent, ohne Änderung der Laufzeitschicht |
| Dringlichkeit | geplant (`K-155`, Freigabe des Owners vom 2026-09-30, verkleinert am 2026-10-01) |
| Status | 🟢 **entschieden am 2026-10-01** (E1 bis E7) |

---

## 1. Anlass

`1.22.0` hat die Pakete gebaut und nichts veröffentlicht (D-521); die Zugänge des Owners fehlten am Arbeitsplatz. Am 2026-10-01 sind `PYPI_TOKEN`, `TESTPYPI_TOKEN` und `NPM_TOKEN` als Benutzervariablen gesetzt. Der Owner verkleinert die Freigabe: *„Die anderen Paketquellen würde ich gern nochmal zurückstellen“* – veröffentlicht werden nur PyPI und npm, TestPyPI zuerst mit Installationsprobe, vor dem ersten echten Hochladen je Quelle eine Rückfrage.

## 2. Vorprüfung

Vorgelegt am 2026-10-01 mit Schätzung: 0 Sitzungsläufe, 0 USD, rund 3,5 bis 4 Stunden Arbeit, dazu zwei Freigaben und die Signatur des Owners. Der Owner folgt den Empfehlungen. Vor der Vorlage erhoben:

- **Namen:** `koolie` ist auf PyPI, TestPyPI und npm frei (HTTP 404 auf die Paketadressen).
- **Zugänge:** Alle drei Benutzervariablen sind gesetzt; `npm whoami` mit dem Token meldet das Konto des Owners. Für PyPI gibt es keine Anmeldeprobe ohne Hochladen.
- **Die Pakete von `1.23.0`:** Metadaten richtig; die Beschreibung trägt 32 relative Links, die auf pypi.org ins Leere führen, und das npm-Paket zeigt die deutsche `README.md`.
- **Werkzeuge:** npm 11.12.1, uv 0.11.9 (`uv publish`); `twine` fehlt am Arbeitsplatz und läuft für `twine check` aus einer Wegwerfumgebung.

## 3. Vorlage zur Entscheidung

| # | Frage | Entscheidung | Preis |
|---|---|---|---|
| E1 | Wie wird hochgeladen? | Mit den Tokens des Owners vom Arbeitsplatz (`uv publish`, `npm publish`); Trusted Publishing ohne Ziel (`K-210`) (D-527) | Keine Attestierung, keine Provenienz |
| E2 | Welche Version zuerst? | `1.24.0`, neu gebaut – nicht die Pakete von `1.23.0` (D-527) | Ein Release mehr vor der ersten Veröffentlichung |
| E3 | Wie läuft die Probe auf TestPyPI? | Vor der Signatur `1.24.0.dev1` aus dem Arbeitsbaum mit Installationsprobe; nach der Signatur das endgültige Wheel auf TestPyPI, dann dieselben Bytes auf PyPI. npm: Trockenlauf und Installation aus der `.tgz` (D-529) | Vorabversionen bleiben auf TestPyPI |
| E4 | Was zeigen die Paketseiten? | `README.en.md` mit absoluten Links auf die Marke; npm über das Feld `readme` (D-528) | Die Links tragen erst mit der Marke auf dem Spiegel |
| E5 | Was sagen README und Quickstart? | Die Paketquellen als gleichwertiger Weg neben dem Starter (D-531) | Zwei Wege in der Dokumentation |
| E6 | Release-Prozess? | Schritt 9 für PyPI und npm ab `1.25.0` mit der Signatur freigegeben; Scoop und Homebrew ruhen (D-530) | Signieren heißt veröffentlichen |
| E7 | Roadmap und Zugänge | Posten auf PyPI und npm verkleinert; Scoop und Homebrew `K-209`, Trusted Publishing `K-210`. Empfehlung an den Owner: das PyPI-Token nach dem ersten Hochladen durch eines nur für das Projekt `koolie` ersetzen, für npm ein granulares Token mit Ablauf (D-527) | – |

## 4. Umsetzung

1. **Bau:** `paketquellen/bauen.py` schreibt die Links der Beschreibung absolut (`beschreibung()`), gibt sie npm im Feld `readme` mit und baut mit `--vorab N` eine Vorabversion; die Nachprüfung meldet einen relativen Link in METADATA oder `readme` und eine Vorabversion, die die Version der Marke trüge.
2. **Prüfung 112** baut zusätzlich mit `--vorab 1`; Sondenteil 17 um `112g` und `112h` erweitert.
3. **Einstieg:** README und Quickstart, deutsch und englisch.
4. **Release-Prozess** Abschnitt 4.2 Schritt 9, **Roadmap**, `paketquellen/README.md`.

## 5. Entscheidung

🟢 **Angenommen am 2026-10-01.**

| # | Entscheidung | Decision Record |
|---|---|---|
| E1, E2, E7 | Zuschnitt, Zugänge, Version | D-527 |
| E4 | Die Beschreibung auf den Paketseiten | D-528 |
| E3 | TestPyPI zuerst, mit Vorabversion | D-529 |
| E6 | Schritt 9 mit der Signatur freigegeben | D-530 |
| E5 | README und Quickstart | D-531 |

## 6. Messung und Belege

Protokoll `tests/protocols/2026-10-01-erste-veroeffentlichung.md`. Kein Sitzungslauf, 0 USD. Erhebungsablage `leitwerk-erhebungen-2026-10-01-1240` außerhalb des Repositoriums. 🔴 Befund vor dem ersten Hochladen: `TESTPYPI_TOKEN` und `PYPI_TOKEN` trugen dasselbe Token für pypi.org; TestPyPI wies es mit 403 ab.
