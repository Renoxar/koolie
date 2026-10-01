# Protokoll: Die erste Veröffentlichung auf PyPI und npm zu `1.24.0`

| Feld | Inhalt |
|---|---|
| Datum | 2026-10-01 |
| Release | `1.24.0` (`CR-2026-170`, D-527 bis D-531) |
| Gegenstand | Die Pakete für PyPI und npm vor dem ersten Hochladen: Beschreibung, Vorabversion, Installation aus TestPyPI und aus den Paketdateien (`K-155`) |
| Arbeitsplatz | Windows 11, Python 3.14, pip 26.0.1, uv 0.11.9, Node mit npm 11.12.1; `twine` 6 in einer Wegwerfumgebung |
| Messort | `C:\lw-1240\` – außerhalb des Benutzerprofils; uv und npm dort in eigene Präfixe installiert |
| Belege | Erhebungsablage `leitwerk-erhebungen-2026-10-01-1240` außerhalb des Repositoriums: Vorabpakete unter `vorab1/`, Ausgaben der Installationen |
| Kosten | Kein Sitzungslauf, 0 USD |

## 1. Vor der Vorlage

| Frage | Ergebnis |
|---|---|
| Ist `koolie` frei? | PyPI, TestPyPI und npm: HTTP 404 auf die Paketadresse |
| Sind die Zugänge gesetzt? | `PYPI_TOKEN`, `TESTPYPI_TOKEN`, `NPM_TOKEN` als Benutzervariablen gesetzt; geprüft wurde nur die Länge, kein Wert ausgegeben |
| Meldet sich das npm-Token an? | ja – `npm whoami` über eine Konfigurationsdatei, die das Token aus der Umgebung liest, nennt das Konto des Owners |
| Was zeigten die Pakete von `1.23.0`? | 32 relative Links in der Beschreibung des Wheels; im npm-Paket liegen `README.md` (deutsch) und `README.en.md`, npm nähme die deutsche |

## 2. Die Beschreibung und die Vorabversion

`bauen.py` aus dem Arbeitsbaum, zuerst gegen das Archiv von `1.23.0`, dann gegen ein Archiv des Arbeitsbaums (`git archive … $(git stash create)`, Präfix `koolie-1.24.0`):

| Prüfung | Ergebnis |
|---|---|
| Links der Beschreibung | 32 von 32 absolut auf `https://github.com/Renoxar/koolie/blob/v<V>/…`; Anker und Adressen unverändert |
| `--vorab 1` | Wheel `1.24.0.dev1`, npm `1.24.0-dev.1`; Nachprüfung ohne Befund, zweimal bytegleich |
| `--vorab 0` | abgewiesen, Exit 2 |
| `twine check` | bestanden (endgültig und Vorabversion) |
| `npm publish --dry-run` | ohne Befund für die endgültige Version; die Vorabversion verlangt `--tag` (npm setzt sonst `latest` auf eine Vorabversion) |
| Feld `readme` | `@npmcli/package-json` liest die README-Datei nur, wenn das Feld fehlt – das Feld gewinnt |

## 3. Installation aus den Paketdateien

| Weg | `koolie --version` | Banner vor `install.py` | Projektinstallation |
|---|---|---|---|
| `uv tool install <whl>` | `koolie 1.24.0` | ja (Textvariante, keine Konsole) | Exit 0, Kern 670 Dateien |
| `npm install -g --prefix … <tgz>` | `koolie 1.24.0` | ja | Exit 0; gleich der über uv bis auf `__pycache__` |
| `pip install <whl>` in eine venv | `koolie 1.24.0` | – | – (`pip show`: `1.24.0.dev1`) |

Die Version im Befehl ist die des Baums (`VERSION`), nicht die des Pakets – eine Vorabversion meldet deshalb `1.24.0`. Das ist so gewollt (D-529): Der Baum im Paket ist der des Archivs.

## 4. TestPyPI

🔴 **Das erste Hochladen wurde mit 403 abgewiesen** (*„Invalid or non-existent authentication information“*). Ursache, ohne Ausgabe eines Wertes ermittelt: `TESTPYPI_TOKEN` und `PYPI_TOKEN` waren gleich, und der Ort im Token war `pypi.org`. Ein Token von pypi.org gilt auf TestPyPI nicht – beide Dienste haben getrennte Konten. Veröffentlicht war dabei nichts. Der Owner hat ein Token von TestPyPI nachgetragen (Ort im Token: `test.pypi.org`, verschieden von `PYPI_TOKEN`).

| Prüfung | Ergebnis |
|---|---|
| `uv publish` von `1.24.0.dev1` | angenommen |
| JSON-Schnittstelle von TestPyPI | Version `1.24.0.dev1`, Lizenz `GPL-3.0-only`; die Beschreibung ohne relativen Link; SHA-256 des Wheels gleich der lokalen Datei |
| Projektseite | HTTP 200; die gerenderte Seite liest ein Abruf ohne Browser nicht (Bot-Abfrage des Dienstes) |
| `uv tool install --index-url <Index von TestPyPI> --prerelease allow koolie==1.24.0.dev1` | `koolie --version` = `koolie 1.24.0`; Projektinstallation Exit 0, Banner vor `install.py`, **gleich der Installation aus der Paketdatei** bis auf `__pycache__` |

## 5. Grenzen

- Die Darstellung der Seiten ist nach dem Hochladen gelesen, nicht vorher geprüft; `twine check` prüft nur, ob die Beschreibung sich darstellen lässt.
- Ob die Links tragen, hängt an der Marke `v1.24.0` auf dem GitHub-Spiegel.
- npm hat kein Testverzeichnis; der Trockenlauf prüft das Paket, nicht die Anmeldung beim Hochladen.
