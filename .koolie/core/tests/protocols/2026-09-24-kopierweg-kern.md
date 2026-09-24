# Protokoll: Der Kopierweg des Kerns – und das Archiv, aus dem er als sicher galt

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-24 |
| Release | `1.4.4` |
| Änderungsantrag | `CR-2026-137` |
| Art | Korrektur an Übernahmeanleitung und Installationswerkzeug – **keine Sitzung, kein Kontingent, kein Modelllauf** |
| Gegenstand | Was geschieht, wenn ganz `.koolie/` statt nur `.koolie/core/` in ein Projekt kopiert wird, und was `install.py` davon meldet |
| Ergebnis | 🟢 **Entschieden, `D-354`.** 🔴 **Auch das Release-Archiv trägt das Kennzeichen** – die Annahme der Vorbereitung war falsch. 🔴 **Eine Kopie aus dem Arbeitsbaum ersetzt das Overlay des Projekts ohne Meldung.** Warnsatz an jedem Kopierbefehl, Auskunft in `install.py`, Sonde `D354` fällt gegen den Vorstand |

---

## 1. Was gefragt war

Wiederaufnahmepunkt von `1.4.3`, Punkt 1 – zwei Fragen des Owners zu
`.koolie/QUELLREPOSITORIUM.md`: **(a)** ein Warnsatz *„nie ganz `.koolie/` kopieren“* in
README und Übernahmeleitfaden; **(b)** eine Meldung von `install.py`, wenn es das
Kennzeichen im Ziel findet – als Auskunft oder als Abbruch, vorher zu messen.

## 2. Messungen

Alle Messungen an Wegwerf-Verzeichnissen im Ablagebereich der Sitzung.

### 2.1 Welche Quelle was mitbringt

| Quelle | Kennzeichen | Overlay des Frameworks |
|---|---|---|
| `tar -tzf koolie-1.4.3.tar.gz` | 🔴 **enthalten** (`koolie-1.4.3/.koolie/QUELLREPOSITORIUM.md`) | nicht enthalten |
| Arbeitsbaum (`find .koolie/project-overlay -type f`) | enthalten | 🔴 **18 Dateien** (`.gitignore` Zeile 36, `git check-ignore -v`) |

⚠️ **Die Vermutung vor der Messung war falsch:** Die Übergabe von `1.4.3` hielt eine
Kopie aus dem Archiv für harmlos. Die Datei ist versioniert, und `git archive` nimmt jede
versionierte Datei mit.

### 2.2 Das Kennzeichen in einem Projekt – Validator

Aufbau: `git init`, Kern über `git ls-files -z .koolie/core | tar` aus dem Arbeitsbaum,
`README.md` angelegt, `install.py --client claude-code`, `__pycache__/` ignoriert,
committet. `validate-framework.py --root .`:

| Lauf | Ergebnis | Meldungen |
|---|---|---|
| A – ohne Kennzeichen | **0 Fehler, 0 Warnungen** | – |
| B – Kennzeichen kopiert, nicht verfolgt | **1 Fehler** | Prüfung 79: *„LICENSE: fehlt. Die Lizenz MUSS an beiden Stellen liegen …“* |
| C – Kennzeichen mit `git add` | **80 Fehler** | Prüfung 79 wie B; Prüfung 81 an **79** Projektträgern: *„trägt LF-Zeilenenden, während 534 von 613 versionierten Textträgern CRLF tragen“* |

🔴 **Keine Meldung nennt das Kennzeichen.** Die 79 Träger in C sind die Wurzeldateien der
Installation (`.claude/`, Overlay, `CLAUDE.md`, `README.md`), die `install.py` mit LF
schreibt – in einem Projekt mit anderer Zeilenendeform wären es andere, aber nie null.

### 2.3 Die Kopie von ganz `.koolie/` aus dem Arbeitsbaum beim Heben

Die Installation aus 2.2, in `OVERLAY.md` eine Projektmarke angehängt und committet;
dann `cp -r <framework>/.koolie .` und `install.py --client claude-code --update`:

| Messung | Ergebnis |
|---|---|
| Exit von `install.py --update` | 0 |
| `grep -c` auf die Projektmarke in `OVERLAY.md` | 🔴 **0** |
| `git status --short` | `M .koolie/project-overlay/OVERLAY.md`, `M .koolie/project-overlay/overlay-manifest.yaml`, `?? .koolie/QUELLREPOSITORIUM.md` |
| Ausgabe von `install.py` | das Overlay unter *„Projektdateien unberührt gelassen“*; **kein Wort** zum Kennzeichen |

### 2.4 Ob ein Abbruch baubar ist

Das Framework-Repositorium erzeugt seine Wurzeldateien selbst mit `install.py` und trägt
das Kennzeichen. Weder das Vorhandensein noch der Verfolgungsstand der Datei noch die
Lage des Werkzeugs trennt es von einem Projekt, das die Kopie committet hat
(`CR-2026-137` 2.4). **Ein Abbruch ist deshalb nicht baubar, ohne das
Framework-Repositorium selbst zu treffen.**

### 2.5 Wirkungsnachweis – Sonde und Gegenprobe, mit Gegenbeweis

Bündel `sonden_kennzeichen_im_projekt` (`--nur`-Teillauf):

| Einheit | neues `install.py` | `install.py` aus `main` (`1.4.3`) |
|---|---|---|
| Sonde `D354` – Kennzeichen liegt: Hinweis, Exit 0, Prüfung 79 meldet die Lizenz | **OK** | 🔴 **FEHL** – *„Exit 0, Hinweis False, Prüfung 79 True (erwartet je True)“* |
| Gegenprobe `D354a` – ohne Kennzeichen: kein Hinweis, keine Lizenzmeldung | **OK** | OK |

Dazu von Hand an der Installation aus 2.2: mit Kennzeichen erscheint die Auskunft
(zehn Zeilen, Exit 0), ohne Kennzeichen `grep -c Kennzeichen` **0**.

## 3. Abnahme

| Lauf | Ergebnis |
|---|---|
| `validate-framework.py --root .` | **0 Fehler, 0 Warnungen** – mit und ohne `PYTHONIOENCODING=utf-8` |
| Sondenlauf mit und ohne `PYTHONIOENCODING=utf-8` | **325 Einheiten, alle bestanden**, Exit 0, oberhalb der Trennlinie zeilengleich (521 Zeilen). **Neu:** Bündel `sonden_kennzeichen_im_projekt` (`D354`, `D354a`) |
| Pilot / Übungsrepo `--strict-overlay` nach dem Heben | Pilot 1 Fehler, 2 Warnungen – alle im projekteigenen `CHANGELOG.md`, unverändert; Auskunft über ignorierte Kerndateien weiterhin **38**. Übungsrepo 0 Fehler, 1 Warnung (Laufzeitfassung 6.023 Zeichen), unverändert. **Die neue Auskunft schweigt in beiden** – gehoben ist nur `.koolie/core/` |
| Hauptdokument und Word-Fassung je Pack | alle drei gebaut: `claude-code` 2.098.020, `devin-desktop` 2.094.349, `openai-codex` 2.085.771 Zeichen; Dokumentversion `1.4.4`, D-354 je sechsmal |

## 4. Offen

- 🔴 **Die signierte Marke `v1.4.4`** setzt der Framework Owner (D-321).
- Die Meldungen der Prüfungen 79 und 81 nennen die Ursache weiterhin nicht (benannt in
  `CR-2026-137` Abschnitt 3).
- **`1.5.0`** mit dem Umfang aus D-353.
