# Paketquellen

Dieser Ordner baut Koolie für Paketquellen. Veröffentlicht wird auf **PyPI** (`koolie`) und **npm** (`@renoxar/koolie`); das übernimmt der Workflow `.github/workflows/publish.yml` an der signierten Marke, nach Freigabe durch den Owner (`RELEASE_PROCESS.md` Abschnitt 4.2, Schritt 9). Scoop und Homebrew werden gebaut, aber nicht veröffentlicht.

| Datei | Zweck |
|---|---|
| `koolie_befehl.py` | Der Befehl `koolie`: ohne Argumente der Installationsdialog mit dem aktuellen Verzeichnis als Vorgabe, mit Argumenten `install.py`, davor das Banner; `koolie --version` |
| `koolie.cmd` | Hülle für Windows aus dem entpackten Release-Archiv (Scoop) |
| `npm/koolie.js` | Hülle für npm: sucht Python ab 3.8 und erbt das Terminal |
| `bauen.py` | Baut aus dem Release-Archiv Wheel, npm-Paket, Scoop-Manifest und Homebrew-Formel und prüft sie nach |

## Bauen

```
python paketquellen/bauen.py --archiv <koolie-X.Y.Z.tar.gz> --aus <ablage>
```

Das Archiv entsteht nach `RELEASE_PROCESS.md` Abschnitt 4.1, Schritt 5. Die Manifeste laden vom GitHub-Release der Marke; `--url-basis` setzt eine andere Adresse, etwa einen lokalen Server.

Eine Vorabversion für TestPyPI (`<V>.devN`, npm `<V>-dev.N`) entsteht vor der Signatur aus dem Arbeitsbaum:

```
git -c core.eol=lf -c core.autocrlf=input archive --format=tar.gz --prefix=koolie-<V>/ -o <ablage>/koolie-<V>.tar.gz $(git stash create)
python paketquellen/bauen.py --archiv <ablage>/koolie-<V>.tar.gz --aus <ablage> --vorab 1
```

Als Beschreibung auf PyPI und npm dient `README.en.md`, mit absoluten Links auf die Marke im GitHub-Spiegel. npm bekommt sie über das Feld `readme` der `package.json`; die Dateien im Paket sind die des Archivs.

## Warum das Banner im Befehl steht

Beim Installieren aus einer Paketquelle gibt es kein verlässliches Terminal: pip führt nichts aus, npm verschluckt die Ausgabe, Chocolatey gibt kein Terminal. Der Befehl `koolie` läuft dagegen immer im Terminal des Nutzers – und erst er bringt Koolie ins Projekt.

## Stand je Paketquelle

| Paketquelle | Stand |
|---|---|
| PyPI (pip, pipx, uv) | veröffentlicht als `koolie` |
| npm | veröffentlicht als `@renoxar/koolie` – der Name `koolie` ist auf npm gesperrt |
| Scoop | gebaut, lokal geprüft (`7zip` wird mitinstalliert), nicht veröffentlicht |
| Homebrew | gebaut, nicht geprüft, nicht veröffentlicht |
| Chocolatey, winget | nicht geplant |
