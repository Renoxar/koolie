# Paketquellen

Dieser Ordner baut Koolie für Paketquellen (`CR-2026-168`, D-518 bis D-521). **Veröffentlicht ist noch nichts** – das gibt der Framework Owner je Paketquelle frei (D-521).

| Datei | Zweck |
|---|---|
| `koolie_befehl.py` | Der Befehl `koolie`: ohne Argumente der Installationsdialog, mit Argumenten `install.py`, davor das Banner (D-519); `koolie --version` |
| `koolie.cmd` | Hülle für Windows aus dem entpackten Release-Archiv (Scoop) |
| `npm/koolie.js` | Hülle für npm: sucht Python ab 3.8 und erbt das Terminal |
| `bauen.py` | Baut aus dem Release-Archiv Wheel, npm-Paket, Scoop-Manifest und Homebrew-Formel und prüft sie nach |

## Bauen

```
python paketquellen/bauen.py --archiv <koolie-X.Y.Z.tar.gz> --aus <ablage>
```

Das Archiv ist das aus `RELEASE_PROCESS.md` 4.1, Schritt 5. Die Download-Adresse der Manifeste ist das GitHub-Release der Marke; `--url-basis` setzt eine andere, etwa für eine Messung mit einem lokalen Server.

## Warum das Banner im Befehl steht

Gemessen am 2026-09-30 (Protokoll `.koolie/core/tests/protocols/2026-09-30-paketquellen.md`): pip führt beim Installieren nichts aus, npm verschluckt die Ausgabe eines Installationsskripts, Chocolatey gibt ihm kein Terminal. Der Befehl `koolie` läuft dagegen immer im Terminal des Nutzers – und erst er bringt Koolie ins Projekt.

## Stand je Paketquelle

| Paketquelle | Stand |
|---|---|
| PyPI (pip, pipx, uv) | gebaut, lokal gemessen |
| npm | gebaut, lokal gemessen |
| Scoop | gebaut, lokal gemessen (`7zip` wird mitinstalliert, `K-206`) |
| Homebrew | gebaut, nicht gemessen (`K-205`) |
| Chocolatey, winget | ohne Ziel (`K-204`) |
