# Protokoll: Installation über Paketquellen mit dem Banner zu `1.22.0`

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-30 |
| Release | `1.22.0` (`CR-2026-168`, D-518 bis D-522) |
| Gegenstand | Wie jede Paketquelle Code startet und ob sie dabei ein Terminal bereitstellt; der Befehl `koolie` mit dem Banner; die Pakete aus dem Release-Archiv (`K-155`) |
| Arbeitsplatz | Windows 11, Python 3.14.4, pip 26.0.1, uv 0.11.9, Node 24.15 mit npm 11.12.1, Chocolatey 2.7.1, winget 1.29, Scoop (für die Messung in ein Wegwerfverzeichnis installiert) |
| Messort | `C:\lw-1220\` – außerhalb des Benutzerprofils; npm, uv und Scoop dort in eigene Präfixe installiert |
| Belege | Erhebungsablage `leitwerk-erhebungen-2026-09-30-1220` außerhalb des Repositoriums: Sonde `sonde_terminal.py` mit ihren Ergebnissen, Messskript `messen.ps1`, Konsolenpuffer je Fall, Scoop-Ausgaben |
| Kosten | Kein Sitzungslauf, 0 USD. 13 Paketinstallationen, 40 Aufrufe des Befehls, 4 Ende-zu-Ende-Installationen in ein Wegwerfprojekt |

## 1. Der Messaufbau

Eine Konsole, die das Werkzeug der Sitzung startet, ist kein Terminal. Gemessen wurde deshalb in einer **echten, verborgenen Konsole** (`Start-Process powershell -WindowStyle Hidden`), und gelesen wurde der **Konsolenpuffer** nach jedem Fall – Zeichen und Vordergrundfarben –, nicht eine umgeleitete Ausgabe. Die Umgebung wurde vorher bereinigt: Die Sitzung setzt `NO_COLOR=1` und `PYTHONIOENCODING`, beides hätte die Farbmessung verfälscht.

Die Sonde `sonde_terminal.py` ruft `banner.variante_waehlen` und `banner.farbstufe` mit dem, was sie vorfindet, und schreibt Terminal-Zustand von stdin, stdout und stderr, Kodierung, Breite und die gewählte Variante in eine Datei. Sie lief als Installationsskript jeder Paketquelle, die eines kennt, und als installierter Befehl.

## 2. Der Installationsschritt – wer führt Code aus, mit welchem Terminal

| Weg | Code beim Installieren? | stdout ein Terminal | Banner-Auswahl | sichtbar |
|---|---|---|---|---|
| `pip install` (Wheel) | nein | – | – | – |
| `npm install`, `postinstall` | ja | nein | Textvariante | nein – npm verschluckt die Ausgabe |
| `npm install --foreground-scripts` | ja | ja | Vollvariante | ja |
| `choco install`, `chocolateyInstall.ps1` → Python | ja | nein | Textvariante | ja, als Text |
| `scoop install`, `post_install` | ja | ja | Vollvariante | ja |
| winget | nach der Dokumentation still; der Typ „portable“ führt nichts aus und verlangt eine `.exe` | – | – | – |
| Homebrew | hier nicht messbar (macOS) | – | – | – |

➡️ Nur Scoop gibt seinem Installationsskript verlässlich ein Terminal. **Der installierte Befehl** hatte dagegen bei pip, npm (`bin`, `npx`) und Scoop ein Terminal. Deshalb steht das Banner im Befehl (D-519).

## 3. Der Befehl `koolie` auf vier Wegen

Gebaut mit `paketquellen/bauen.py` aus einem Archiv des Arbeitsbaums (`git archive` über einen temporären Index, 678 Dateien); das Scoop-Manifest zeigte auf einen lokalen HTTP-Server. Installiert: Wheel mit pip in eine venv und mit `uv tool install`, npm-Paket mit `npm install -g --prefix`, Scoop mit dem Manifest als Datei. Je Weg zehn Fälle:

| Fall | Ergebnis auf allen vier Wegen |
|---|---|
| `koolie --version` | `koolie 1.22.0`, Exit 0, kein Banner |
| `koolie --help` in der alten Konsole (120 Spalten) | Vollvariante mit Hund, einfarbig (alte Konsole ohne Farbangabe), danach die Hilfe von `install.py` |
| mit `COLORTERM=truecolor` | Vollvariante, die Zonen farbig im Puffer |
| mit `COLORTERM=truecolor` und `NO_COLOR=1` | Vollvariante ohne Farbe |
| mit `COLUMNS=70` | Kompaktvariante ohne Hund, URL ohne Schema |
| mit `KOOLIE_NO_BANNER=1` | kein Banner, Hilfe vollständig |
| `koolie --no-banner --help` | kein Banner, Hilfe vollständig |
| `koolie --help` über eine Pipe | Textvariante, keine Steuerzeichen, kein Rahmenzeichen |
| `koolie` ohne Argumente, Eingabe leer | Banner, dann der Dialog; „Nichts installiert (keine Eingabe mehr)“, Exit 1 |
| `koolie --target <projekt> --client claude-code` | Banner, dann die Installation: 83 Dateien angelegt, Kern 664 Dateien |

Die vier Projektinstallationen sind **bytegleich** (gleiche Dateimenge, gleicher Inhalt).

## 4. Der Bau

- Zweimal gebaut bytegleich; Wheel `koolie-1.22.0-py3-none-any.whl` rund 4,1 MB, npm-Paket rund 3,2 MB.
- `twine check`: bestanden. `check-wheel-contents`: W002 (doppelte Dateien – der Baum trägt gleiche Dateien an mehreren Stellen) und W004 (Dateien außerhalb importierbarer Pfade – der Baum ist Datenbestand), beide erwartet.
- Die Dateimenge im Wheel nach der Installation ist die des Archivs. **Beifund npm:** Beim Entpacken wird die `.gitignore` der Paketwurzel zu `.npmignore`; der Kern ist davon nicht berührt.
- **Beifund Scoop:** Ein `.tar.gz` entpackt Scoop nur mit `7zip`, das es beim ersten Mal selbst installiert (`K-206`). Die Notiz des Manifests erscheint nach der Installation; `python` wird nur vorgeschlagen.

## 5. Der Befund am Sondenapparat

Die Gegenprobe zu Prüfung 112 bestand, bevor die Buchhaltung des Releases stand – an einem Baum mit zehn offenen Fehlern. Ursache: `"0 Fehler" in ausgabe` trifft auch „10 Fehler“. Die Gegenprobe liest jetzt die Ergebniszeile (`apparat.fehlerfrei`, D-522); danach fiel sie an demselben Baum, wie sie sollte. Sonde `112f` hält die Unterscheidung.

## 6. Rückbau

Scoop lag nur unter `C:\lw-1220\scoop`; sein Eintrag im Benutzerpfad ist nach der Messung auf den gesicherten Stand zurückgesetzt (verglichen: gleich), eine Variable `SCOOP` hatte der Installer nicht dauerhaft gesetzt. npm und uv lagen in eigenen Präfixen unter `C:\lw-1220`. `C:\lw-1220` ist löschbar.
