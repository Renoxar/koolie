# Änderungsantrag `CR-2026-140`

| Feld | Inhalt |
|---|---|
| Titel | Der Installer je Zielsystem – und die Prüfung, die ohne PyYAML Fehler erfand |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-25 |
| Betroffene Artefakte | `install.cmd`, `install.command` (neu, Wurzel); `install_dialog.py` (neu); `install.py` (`--target`, `PYTHON_MINDEST`); `tests/scripts/validate-framework.py` (Prüfung 33, `TEXT_EXT`); `tests/scripts/probe-pruefungen.py` (Bündel `sonden_kopierweg`, `sonden_ohne_pyyaml`, Sonden `6s`); `docs/ADOPTION_GUIDE.md`, `README.md`; `governance/RELEASE_PROCESS.md` (Schritt 2); `docs/ROADMAP.md`; `governance/DECISION_LOG.md` (**D-362** bis **D-366**); `governance/ADOPTION_REGISTRY.md`; `build/doc/00-kopf.md`, `15-referenzstruktur.md`, `26-qs-test.md`; `VERSION`, `CHANGELOG.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Installationswerkzeug, Auslieferbestand, Prüfapparat |
| Art | **MINOR** nach `RELEASE_PROCESS.md` Abschnitt 1: neuer Übernahmeweg neben dem bisherigen, erweiterte Prüfung; kein Overlay-Feld geändert |
| Dringlichkeit | Vorgabe des Owners vom 2026-09-25; Ziel-Release `1.7.0` nach D-361 |
| Status | 🟢 **entschieden am 2026-09-25** (E1 bis E11), umgesetzt mit `1.7.0` |

---

## 1. Anlaß

Ein Zielprojekt bekam das Framework bis `1.6.0` über einen Handgriff: den Kern aus Archiv
oder Klon ins Projekt kopieren, dann `install.py` dort aufrufen (`CR-2026-098`, `K-75`).
Der `<FRAMEWORK_OWNER>` hat am 2026-09-25 vorgegeben: **ein Installer je Zielsystem, im
Fokus Windows und macOS**; wer Linux oder ein anderes Unix nutzt, bleibt beim bisherigen
Weg. Der Posten war dreimal gerückt (D-339, D-341, D-361).

## 2. Die Gegenprüfung

### 2.1 Woran der Handweg zweimal gebrochen ist

Wer ganz `.koolie/` kopiert, nimmt das Kennzeichen des Quellrepositoriums und aus einem
Klon dessen Overlay mit (D-354); wer mit `git archive HEAD` hebt, liefert den Stand von
vorhin (D-333). **Beides sind Fehler des Handgriffs, nicht des Werkzeugs** – ein Werkzeug,
das nur den Kern kopiert, kann sie nicht machen.

### 2.2 Was der Zielrechner mitbringen muß

`install.py`, der Validator und die Hooks sind Python. Die Hooks laufen in jeder Sitzung;
**ein Installer ohne Python-Voraussetzung verschöbe die Frage in die erste Sitzung.**
Gemessen am 2026-09-25 mit Python 3.8.20 neben 3.14: Installationen aller drei Packs
byteweise gleich, der Validator mit PyYAML zeilengleich, alle 41 Python-Träger
kompilieren. 3.7 war auf dem Meßplatz nicht beschaffbar.

### 2.3 Die Startbedingungen der beiden Systeme

| System | Befund | Folge |
|---|---|---|
| Windows | `Get-ExecutionPolicy -List`: `LocalMachine AllSigned`, `CurrentUser RemoteSigned` – ein heruntergeladenes `.ps1` startet per Doppelklick nicht | Starter als `.cmd` |
| Windows | `WindowsApps\python.exe` liegt im Suchpfad und startet ohne installiertes Python kein Python | Versionsprobe statt Namensprobe; `clientmap.python_interpreter()` kennt die Falle schon |
| Windows | Das Archiv liefert mit ausdrücklicher Zeilenendeform LF (D-328); `cmd.exe` findet Sprungmarken in LF-Dateien nicht zuverlässig | Starter ohne Sprungmarke, Sonde `T365` |
| macOS | Ein `.command` öffnet sich per Doppelklick im Terminal, **wenn** es ausführbar ist; kein Träger des Repositoriums trug `100755` | Modus gesetzt, Sonde `T365` |
| macOS | `/usr/bin/python3` ist ohne Command Line Tools ein Platzhalter | Versionsprobe |

### 2.4 🔴 Prüfung 33 erfand ohne PyYAML Fehler

Beim Messen der Mindestversion: Ohne PyYAML meldete der Validator an **jeder**
`claude-code`-Installation neun Skills mit leerem `disallowed-tools` – Prüfung 33 las aus
dem Rohtext des Frontmatters mit `.get()` nichts. Die Warnung dazu sagte, die Prüfungen
4, 5 und 8 liefen *„eingeschränkt“*; Prüfung 33 nannte sie nicht, und sie lief nicht
eingeschränkt, sondern falsch. **Das trifft den Installer:** Der Starter installiert kein
PyYAML nach.

### 2.5 🔴 Die Starter lagen außerhalb des Prüfapparats

`TEXT_EXT` führte weder `.cmd` noch `.command`. Nach der Aufnahme meldete die
Inhaltsprüfung in beiden Startern sofort eine URL außerhalb der Allowlist.

### 2.6 Der Lieferumfang

Die Roadmap nannte einen **wählbaren Lieferumfang** (*„alles oder nur das zur Nutzung
Nötige“*). Gemessen: Hooks und Validator liegen unter `tests/scripts/`. Der naheliegende
Schnitt *„ohne `tests/`“* bräche jede Installation.

## 3. Vorlage zur Entscheidung

Vorgelegt am 2026-09-25 als Fragen (a) bis (j), angenommen mit *„a – i passt“*.

| # | Frage | Wege und ihre Preise |
|---|---|---|
| **E1** | **Python voraussetzen?** (a) | **Ja, dünne Starter je System**, eine Installationslogik. **Verworfen:** eigenständige Programme – Bau je System, Signatur und Notarisierung, und die Hooks brauchten trotzdem Python |
| **E2** | **Mindestversion** (b) | **Messen, nicht setzen:** 3.8 (2.2). ⚠️ **Preis:** unter Windows gemessen, auf macOS übertragen |
| **E3** | **Starter unter Windows** (c) | **`install.cmd`** (2.3); unter macOS **`install.command`** |
| **E4** | **Ort der Kopierlogik** (d) | **`install.py --target`**; die Starter suchen nur Python |
| **E5** | **Bedienung** (e) | **Die Starter fragen**, `install.py` bleibt parametergesteuert. Die Fragen stehen in `install_dialog.py`, nicht in den Starterdateien – zwei Shell-Dialekte wären zwei Dialoge |
| **E6** | **Heben** (f) | **Derselbe Starter hebt**, wenn im Projekt ein Kern liegt (`--target --update`); `RELEASE_PROCESS.md` Schritt 2 nennt den Befehl |
| **E7** | **Prüfbarkeit der Starter** (aus der Umsetzung, 2.3 und 2.5) | **`TEXT_EXT` um `.cmd`, `.command`**; Sonde `T365` für Sprungmarke und Modus, `T363` für die Mindestversion an drei Stellen |
| **E8** | **Nachinstallieren** (h) | **Nein** – weder Python noch PyYAML; der Starter nennt den Weg und hält an |
| **E9** | **Ablage** (i) | **Wurzel des Archivs** |
| **E10** | **Prüfung 33 ohne PyYAML** (aus der Messung, 2.4) | **Zeilenweiser Rückfall** für das einzeilige Feld. **Verworfen:** aussetzen – das schaltete die Prüfung gegen B01 genau auf den Zielrechnern ab |
| **E11** | **Lieferumfang** (g) | **Nicht in `1.7.0`**, eigener Posten `1.8.0` (2.6) |
| (j) | **Abnahme auf macOS** | ⚠️ **Offen.** Geprüft unter Git Bash und Linux (`dash`); die Abnahme auf macOS liegt beim Owner |

> **Empfehlung der Vorbereitung:** E1 bis E11 wie vorgelegt.

---

## 4. Umsetzung

1. `install.py`: `--target <projekt>` (nur mit `--update`, `--client`, `--overlay`,
   `--dry-run`), `quelle_kerndateien()` (Klon: `git ls-files`, nur wenn die Klonwurzel die
   Quellwurzel ist; sonst Verzeichnis ohne `__pycache__` und `build/out`), Kopie über
   `core.koolie-neu`, Tausch über `core.koolie-alt`, Aufruf des kopierten `install.py`,
   Rückbau bei dessen Scheitern; `PYTHON_MINDEST` und Prüfung beim Start.
2. `install_dialog.py`: Projektverzeichnis (hineingezogener Pfad), bei vorhandenem Kern
   Heben, sonst Client und Muster; Befehl zeigen, bestätigen, ausführen; `q` bricht ab.
3. `install.cmd`, `install.command` in der Wurzel; `install.command` mit `100755`.
4. Validator: `_flaches_feld()` für Prüfung 33; `TEXT_EXT` um `.cmd`, `.command`.
5. Sonden: Bündel `sonden_kopierweg` (`T362` bis `T362h`, `T363`, `T365`), Bündel
   `sonden_ohne_pyyaml` (`S364`, `S364a`), Sonden `6s` an beiden Startern.
6. Leitfaden, README, Schritt 2 des Release-Prozesses, Roadmap, Decision Log,
   Bestandsliste, Kopf, Kapitel 15 und 26, `VERSION`, Changelog.
7. Beide Projekte heben – **zum ersten Mal mit `--target --update`**.

## 5. Abnahme

Steht im Protokoll `tests/protocols/2026-09-25-installer-je-zielsystem.md`.

## 6. Entscheidung

**E1 bis E11 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-25; (a) bis (i) vor
dem Bau vorgelegt und angenommen, E7 und E10 aus der Umsetzung – der Owner hat vorab
erklärt, den Empfehlungen der Vorbereitung zu folgen). (j) bleibt offen. Decision Records
**D-362** bis **D-366**. Alle vier zählbaren Kriterien von D-11 bleiben **0**.
