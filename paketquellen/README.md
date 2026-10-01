# Paketquellen

Dieser Ordner baut Koolie für Paketquellen (`CR-2026-168`, D-518 bis D-521). **Veröffentlicht wird auf PyPI und npm** – seit `1.24.0`, als Schritt 9 von `RELEASE_PROCESS.md` 4.2 mit der Signatur der Marke als Freigabe (D-530). Scoop und Homebrew sind gebaut, nicht veröffentlicht (`K-209`).

| Datei | Zweck |
|---|---|
| `koolie_befehl.py` | Der Befehl `koolie`: ohne Argumente der Installationsdialog mit dem aktuellen Verzeichnis als Vorgabe (D-532), mit Argumenten `install.py`, davor das Banner (D-519); `koolie --version` |
| `koolie.cmd` | Hülle für Windows aus dem entpackten Release-Archiv (Scoop) |
| `npm/koolie.js` | Hülle für npm: sucht Python ab 3.8 und erbt das Terminal |
| `bauen.py` | Baut aus dem Release-Archiv Wheel, npm-Paket, Scoop-Manifest und Homebrew-Formel und prüft sie nach |

## Bauen

```
python paketquellen/bauen.py --archiv <koolie-X.Y.Z.tar.gz> --aus <ablage>
```

Das Archiv ist das aus `RELEASE_PROCESS.md` 4.1, Schritt 5. Die Download-Adresse der Manifeste ist das GitHub-Release der Marke; `--url-basis` setzt eine andere, etwa für eine Messung mit einem lokalen Server.

`--vorab N` baut eine Vorabversion für TestPyPI (`<V>.devN`, npm `<V>-dev.N`), vor der Signatur aus dem Arbeitsbaum (D-529):

```
git -c core.eol=lf -c core.autocrlf=input archive --format=tar.gz --prefix=koolie-<V>/ -o <ablage>/koolie-<V>.tar.gz $(git stash create)
python paketquellen/bauen.py --archiv <ablage>/koolie-<V>.tar.gz --aus <ablage> --vorab 1
```

Die Beschreibung auf PyPI und npm ist `README.en.md` mit absoluten Links auf die Marke im GitHub-Spiegel; npm bekommt sie über das Feld `readme` der `package.json`, die Dateien im Paket bleiben die des Archivs (D-528).

## Warum das Banner im Befehl steht

Gemessen am 2026-09-30 (Protokoll `.koolie/core/tests/protocols/2026-09-30-paketquellen.md`): pip führt beim Installieren nichts aus, npm verschluckt die Ausgabe eines Installationsskripts, Chocolatey gibt ihm kein Terminal. Der Befehl `koolie` läuft dagegen immer im Terminal des Nutzers – und erst er bringt Koolie ins Projekt.

## Stand je Paketquelle

| Paketquelle | Stand |
|---|---|
| PyPI (pip, pipx, uv) | **veröffentlicht** seit `1.24.1` (TestPyPI zuerst, D-529; `1.24.0` nur auf TestPyPI, D-534) |
| npm | **veröffentlicht** seit `1.24.1` |
| Scoop | gebaut, lokal gemessen (`7zip` wird mitinstalliert, `K-206`), nicht veröffentlicht (`K-209`) |
| Homebrew | gebaut, nicht gemessen (`K-205`), nicht veröffentlicht (`K-209`) |
| Chocolatey, winget | ohne Ziel (`K-204`) |
