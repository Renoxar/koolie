# Protokoll: Der Befehl im Projektverzeichnis zu `1.24.1`

| Feld | Inhalt |
|---|---|
| Datum | 2026-10-01 |
| Release | `1.24.1` (`CR-2026-171`, D-532 bis D-534) |
| Gegenstand | Was ein Nutzer erlebt, der Koolie aus einer Paketquelle in sein Projektverzeichnis holen will |
| Arbeitsplatz | Windows 11, Python 3.14, pip 26.0.1, uv 0.11.9, Node mit npm 11.12.1; `pipx` nicht installiert |
| Messort | `C:\lw-1240\` und ein Projektverzeichnis des Owners |
| Belege | Erhebungsablage `leitwerk-erhebungen-2026-10-01-1240` außerhalb des Repositoriums, Unterordner `vorab1241/` |
| Kosten | Kein Sitzungslauf, 0 USD |

## 1. Die Probe des Owners mit `1.24.0`

`pip install -i <Index von TestPyPI> koolie==1.24.0` in einem Projektverzeichnis, ohne Administratorrechte: Installation für den Benutzer, Hinweis von pip *„The script koolie.exe is installed in '…\Python314\Scripts' which is not on PATH“*. Ins Projekt kam nichts – erwartet hatte der Owner das. Danach am Arbeitsplatz: `python -m koolie --version` meldet `koolie 1.24.0`; der Befehl ist also da, nur nicht unter seinem Namen erreichbar.

## 2. Die Vorgabe im Dialog

| Aufruf | Erste Frage | Ergebnis |
|---|---|---|
| `koolie_befehl.py` ohne Argumente in einem Wegwerfverzeichnis | `Projektverzeichnis [Enter = <verzeichnis>]` | Enter führt zur Frage nach dem Client |
| derselbe Aufruf in der Wurzel des Frameworks | `Projektverzeichnis (Ordner hier hineinziehen oder Pfad eingeben)` | keine Vorgabe – das Framework ist kein Projekt |
| Starter (`install_dialog.py` ohne `--vorgabe`) | wie bisher | unverändert |

## 3. Der Einbefehl-Weg aus der Vorabversion `1.24.1.dev1`

Archiv mit `git -c core.eol=lf -c core.autocrlf=input archive … $(git stash create)`: 0 Dateien mit CRLF (die Vorabversion von `1.24.0` trug sie in jeder Textdatei, D-534). `bauen.py --vorab 1` ohne Befund, `twine check` bestanden.

| Weg, im leeren Projektverzeichnis | Vorgabe | Installation |
|---|---|---|
| `uvx --from <whl> koolie`, Antworten: Enter, Client 1, Enter, Enter, `j` | das Projektverzeichnis | Exit 0, 83 Dateien angelegt |
| `npx --package <tgz> koolie`, dieselben Antworten | das Projektverzeichnis | Exit 0, 83 Dateien angelegt |
| `uvx --index-url <Index von TestPyPI> --prerelease allow koolie==1.24.1.dev1` | das Projektverzeichnis | mit `q` abgebrochen, nichts installiert (gewollt) |

## 4. TestPyPI und die Probe des Owners

`1.24.1.dev1` hochgeladen und vom Owner im eigenen Projektverzeichnis ausprobiert:

| Weg | Ergebnis beim Owner |
|---|---|
| `uvx --index-url <Index von TestPyPI> --prerelease allow koolie==1.24.1.dev1` | *„Der uvx Weg schaut super aus“* |
| `pip install --user … --pre koolie==1.24.1.dev1`, dann `python -m koolie` | ersetzt `1.24.0`; Hinweis von pip, dass der Ordner der Skripte nicht im `PATH` steht (erwartet, D-533); danach Banner in der Vollvariante mit `v1.24.1` und `Projektverzeichnis [Enter = <das Projekt>]` |

## 5. Grenzen

- `pipx run koolie` ist ungemessen – `pipx` fehlt am Arbeitsplatz; es ist nach der Dokumentation von `pipx` dieselbe Bauform wie `uvx`.
- Ob der Ordner der Skripte im `PATH` steht, hängt an der Python-Installation; `python -m koolie` trägt in jedem Fall.
