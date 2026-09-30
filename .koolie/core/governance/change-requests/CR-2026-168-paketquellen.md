# Änderungsantrag `CR-2026-168`

| Feld | Inhalt |
|---|---|
| Titel | Installation über Paketquellen mit dem Banner – und die Gegenprobe, die zehn Fehler für null hielt |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-30 |
| Betroffene Artefakte | `paketquellen/` (neu: `bauen.py`, `koolie_befehl.py`, `koolie.cmd`, `npm/koolie.js`, `README.md`), `governance/RELEASE_PROCESS.md` (Abschnitt 4.2), `tests/scripts/pruefungen/werkzeuge.py` (Prüfung 112), `tests/scripts/validate-framework.py`, `tests/scripts/sonden/teil17_paketquellen.py` (neu), `tests/scripts/sonden/apparat.py`, `tests/scripts/probe-pruefungen.py`, `docs/ROADMAP.md` |
| Ebene laut Entscheidungsbaum 6 | Framework Core (Werkzeuge, Validator, Release-Prozess) |
| Art | Neuer Lieferweg und neue Prüfung; MINOR-Release ohne Kontingent, ohne Änderung der Laufzeitschicht |
| Dringlichkeit | geplant (`K-155`, Auftrag des Owners vom 2026-09-30) |
| Status | 🟢 **entschieden am 2026-09-30** (E1 bis E9) |

---

## 1. Anlass

Der Owner nimmt `K-155` wieder auf, mit D-467 ohne Ziel zurückgestellt: Koolie soll über Paketquellen installierbar werden – winget, npm, PyPI mit pipx, Scoop, Homebrew, Chocolatey. Bedingung: Auch auf diesen Wegen erscheint das Banner aus `1.20.3` (`banner.py`, D-506, `CR-2026-165`). Veröffentlicht wird nichts ohne ausdrückliche Freigabe des Owners.

## 2. Vorprüfung

Vorgelegt am 2026-09-30 mit Schätzung: 0 Sitzungsläufe, 0 USD, rund 24 lokale Installationsläufe, Deckel 40. Die Vorlage liegt außerhalb des Repositoriums. Der Owner folgt den Empfehlungen. Vor der Vorlage erhoben:

- **Download-Adresse:** Der GitHub-Spiegel trägt 13 Releases mit Archiv und Prüfsumme; die SHA-256 von `v1.21.0` dort ist die des lokalen Archivs.
- **Namen:** `koolie` ist auf PyPI, TestPyPI, npm, Chocolatey, Homebrew, Scoop (Main, Extras) und winget frei.
- **Terminal beim Installieren**, gemessen mit einer Sonde in einer echten, verborgenen Konsole: pip führt beim Installieren eines Wheels nichts aus; npm gibt `postinstall` kein Terminal und verschluckt die Ausgabe; Chocolatey gibt seinem Skript kein Terminal, zeigt die Ausgabe aber als Text; der installierte Befehl hat bei pip und npm ein Terminal. winget installiert still und verlangt für den Typ „portable“ eine `.exe`.

## 3. Vorlage zur Entscheidung

| # | Frage | Entscheidung | Preis |
|---|---|---|---|
| E1 | Welche Paketquellen? | PyPI, npm und Scoop bauen und messen, Homebrew bauen; Chocolatey und winget ohne Ziel (`K-204`) (D-518) | Windows bleibt bei pip, npm und Scoop |
| E2 | Wo erscheint das Banner? | Im Befehl `koolie`; kein Code im Installationsschritt der Paketquelle (D-519) | Wer nur installiert, sieht es erst beim ersten Aufruf |
| E3 | Was tut der Befehl? | Ohne Argumente der Dialog, mit Argumenten Banner und `install.py` unverändert, `--version`; Prüfung 112 (D-519) | Ein zweiter Einstieg neben den Startern |
| E4 | Wo liegen Befehl und Bau? | `paketquellen/` in der Wurzel, nicht im Kern; kein `pyproject.toml` (D-520) | Ein neuer Ordner in der Wurzel des Frameworks |
| E5 | Was tragen die Pakete? | Genau den Baum des Release-Archivs; Scoop und Homebrew laden das Archiv und prüfen die SHA-256 (D-520) | Wheel rund 4 MB |
| E6 | Lieferkette? | Später Trusted Publishing aus GitHub Actions am Spiegel; jetzt keine Workflow-Datei (D-521) | Keine Veröffentlichung bis zur Freigabe |
| E7 | Release-Prozess? | Bauen und Nachprüfen der Pakete in jedem Release; Veröffentlichen als ruhender Schritt (D-521) | Ein Schritt mehr je Release |
| E8 | Roadmap und Namen? | `1.22.0` = Paketquellen, Modusbindung auf `1.23.0`, erste Veröffentlichung als eigener Posten; Name überall `koolie` (D-518) | Der Name ist nicht reserviert |
| E9 | Befund am Sondenapparat | Die Gegenprobe liest die Ergebniszeile (D-522) | – |

## 4. Umsetzung

1. **Befehl:** `paketquellen/koolie_befehl.py` (Dialog, Banner vor `install.py`, `--version`, `--no-banner`); Hüllen `paketquellen/koolie.cmd` (Scoop) und `paketquellen/npm/koolie.js` (npm, sucht Python ab 3.8, erbt das Terminal).
2. **Bau:** `paketquellen/bauen.py` baut aus dem Release-Archiv Wheel, npm-Paket, Scoop-Manifest und Homebrew-Formel mit `SHA256SUMS`, bytegleich wiederholbar, und prüft selbst nach: Dateimenge gleich dem Archiv, Version, `RECORD`, Ziele der Befehle, kein npm-Installationsskript, Prüfsumme in beiden Manifesten.
3. **Prüfung 112** in `pruefungen/werkzeuge.py`, nur im Quellrepositorium; Sondenteil 17 (`112a` bis `112f`).
4. **Befund am Apparat:** `apparat.fehlerfrei()` liest die Ergebniszeile (D-522).
5. **Release-Prozess** Abschnitt 4.2, **Roadmap**, `paketquellen/README.md`.

## 5. Entscheidung

🟢 **Angenommen am 2026-09-30.**

| # | Entscheidung | Decision Record |
|---|---|---|
| E1, E8 | Umfang, Roadmap, Namen | D-518 |
| E2, E3 | Das Banner im Befehl, Prüfung 112 | D-519 |
| E4, E5 | Ort, Bau und Inhalt | D-520 |
| E6, E7 | Lieferkette und Release-Prozess | D-521 |
| E9 | Die Gegenprobe liest die Ergebniszeile | D-522 |

## 6. Messung und Belege

Protokoll `tests/protocols/2026-09-30-paketquellen.md`. Kein Sitzungslauf, 0 USD. Lokal: 13 Paketinstallationen (Sonden und Pakete), 40 Aufrufe des Befehls in vier Wegen, 4 Ende-zu-Ende-Installationen in ein Wegwerfprojekt. Erhebungsablage `leitwerk-erhebungen-2026-09-30-1220` außerhalb des Repositoriums.
