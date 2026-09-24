# Protokoll: Die Auskunft, die unter Windows nur Verzeichnisse sah – und drei Prüfungen, denen ein Umlaut den Pfad nahm

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-24 |
| Release | `1.4.2` |
| Änderungsantrag | `CR-2026-135` |
| Art | Korrektur an `install.py` und am Prüfapparat – **keine Sitzung, kein Kontingent, kein Modelllauf** |
| Gegenstand | Die Auskunft über ignorierte Kerndateien (D-349) und die Lesestellen von `git ls-files` im Validator |
| Ergebnis | 🟢 **Entschieden und umgesetzt, `D-352`.** 🔴 **Die Auskunft zählte unter Windows jedes Dateimuster als null** – gemessen, 0 gegen 476. 🔴 **Und drei Prüfungen gingen an einem Pfad mit Umlaut leise vorbei** – gemessen mit Gegenbeweis. 🔴 **Und das Hauptdokument war für das dritte Pack nicht baubar** |

---

## 1. Was gefragt war

Der Befund stand am Ende von `1.4.1` offen: Beim Heben gab die Auskunft aus D-349 Pfade der
Form `".koolie/core/build/doc/03-ziele-nichtziele.md/r"` aus. Berichtigen, mit Sonde und
Gegenprobe, und danach erneut heben. Dazu Schritt 3 aus `RELEASE_PROCESS.md` Abschnitt 4.1,
der in `1.4.1` ausgelassen war.

## 2. Gegenprüfung

### 2.1 Der Befund – nachgestellt, bevor eine Zeile geändert wurde

Ein Wegwerf-Repositorium mit drei Dateien unter `.koolie/core/` (`docs/A.md`,
`build/doc/B.md`, `docs/C.txt`), `git init`, `.gitignore` mit einer Zeile:

| `.gitignore` | `git check-ignore` direkt | `ignorierte_kerndateien()` `1.4.1` | neu |
|---|---|---|---|
| `*.md` | 2 | 🔴 **0** | 🟢 2 |
| `*.md`, dazu eine Datei mit U-Umlaut im Namen | 3 | 🔴 **1, verfälscht:** `".koolie/core/docs//334bersicht.md"` | 🟢 3, Pfad unverfälscht |
| `build/` | 1 | 1 | 🟢 1 |
| ein Muster, das nichts trifft | 0 | 0 | 🟢 0 |

**Die Ursache:** Python schreibt mit `text=True` unter Windows `\r\n`; git bekommt jeden Pfad
mit angehängtem `\r` und vergleicht ihn **so** gegen die Muster. Ein Verzeichnismuster greift
am Elternverzeichnis und trifft trotzdem – **das war der Anlaßfall von `K-117`**, und deshalb
hat es beim Bau niemand gesehen. Ein Dateimuster trifft nie – **bis auf den letzten Pfad
der Eingabe**, dem `"\n".join()` kein Zeilenende anhängt. In der zweiten Zeile war das
zufällig die Datei mit Umlaut, und sie kam doppelt verfälscht zurück: `text=True` schreibt
in der Locale-Kodierung (`cp1252`, das `Ü` als Byte `\334`), git quotet das Byte, und
`replace("\\", "/")` macht aus dem Escape einen Schrägstrich.

🔴 **Die Auskunft hatte keine Sonde.** Sie ist keine Prüfung, und die Sondenpflicht aus D-23
hat sie deshalb nicht erreicht.

### 2.2 🔴 Die zweite Stelle in derselben Richtung

Gesucht nach der Lehre aus `0.57.0`: Wo liest der Kern sonst eine Pfadliste von git als
Text? Alle `input=`-Aufrufe (neun) und alle `ls-files`-Aufrufe (fünf: zwei im Validator,
drei in Meßskripten unter `tests/erhebungen/`, die synthetische Bäume ohne solche Namen
lesen) gezählt. Die übrigen `input=`-Aufrufe geben JSON an Hooks – dort ist `\r\n`
unschädlich. **Die beiden Lesestellen des Validators** lesen `git ls-files` zeilenweise, und
ohne `-z` quotet git jeden Pfad mit Nicht-ASCII-Zeichen (`core.quotePath`, Vorgabe an; auf
diesem Arbeitsplatz nicht verstellt).

| Prüfung | Was sie mit `"docs/\303\234bersicht.md"` tat |
|---|---|
| 81 | keine Datei unter dem Namen – `continue`, **leise** |
| 75 | Endung `.md"`, also kein Text – übersprungen, **leise** |
| 78 | gezählt, aber **nicht als Markdown** |
| 45 | unberührt – sie sucht `__pycache__` im Pfad |

**Gegenbeweis:** Arbeitsbaumkopie, `git init`, `git add -A`, dazu ein Träger
`Übersicht-probe.md` mit einer LF-Zeile zwischen CRLF-Zeilen:

| Validator | Treffer auf `mischt CRLF- und LF-Zeilen` |
|---|---|
| aus `1.4.1` | 🔴 **0** |
| aus `1.4.2` | 🟢 **1** |

**Gezählt, nicht geschätzt:** In keinem der drei Bestände steht heute ein solcher Pfad –
Quellrepositorium 535 verfolgte Dateien, Pilot 622, Übungsrepositorium 719, je **0** mit
Nicht-ASCII-Zeichen (`git ls-files -z`, Bytes über 127 gezählt).

## 3. Umsetzung

Wie in `CR-2026-135` Abschnitt 4.

| Einheit | Was sie mißt | gegen den Vorstand |
|---|---|---|
| **Sonde `D349`** | `*.md` im Projekt-`.gitignore`: die Zahl im Hinweis gleich der Zahl der Markdown-Dateien des Kerns (`os.walk`) | 🔴 **fällt** – *gemeldet 0, gezählt 476* |
| **Gegenprobe `D349a`** | `build/`: genau die Dateien unter `build/` | besteht |
| **Gegenprobe `D349b`** | ein Muster, das nichts trifft: kein Hinweis | besteht |
| **Sonde 81e** | ein Träger mit Umlaut im Namen und einer eingeschleppten Zeile wird gemeldet | 🔴 **fällt** |

Beide Gegenbeweise sind im Sondenapparat selbst gefahren: `install.py` und Validator auf den
Stand von `1.4.1` zurückgesetzt, die beiden Bündel mit `--nur` gefahren, danach die neuen
Fassungen wieder eingespielt.

### 3.1 🔴 Schritt 3 aus Abschnitt 4.1 – das Hauptdokument für drei Packs

In `1.4.1` ausgelassen, hier gefahren – und für `openai-codex` **zum ersten Mal überhaupt**:

| Lauf | Ergebnis |
|---|---|
| `assemble.py --client openai-codex`, Stand `1.4.1` | 🔴 **Abbruch:** `eingebettete Datei fehlt (Referenzinstallation openai-codex): AGENTS.override.md.example` |
| danach `build-docx.py` | 🔴 **Erfolg gemeldet** – gebaut aus dem `hauptdokument.md` des vorigen Laufs, unter dem Namen `Koolie_v1.4.2_devin-desktop.docx` |
| `assemble.py` nach dem Eingriff, `claude-code` | 2.085.504 Zeichen – **zeichengleich** zum Bau davor |
| `devin-desktop` | 2.081.833 Zeichen – **zeichengleich** |
| `openai-codex` | 🟢 2.073.255 Zeichen; die Erklärung statt der Einbettung steht genau **einmal**, keine unaufgelöste Direktive |
| Word-Fassungen | `Koolie_v1.4.2_claude-code.docx`, `…_devin-desktop.docx`, `…_openai-codex.docx`, je 8 Diagramme |

➡️ Kapitel 16 kannte die Entscheidung aus D-341 nicht, die das Pack traf. Die Weiche ist
jetzt das Manifestfeld `root_instruction_override` (`CR-2026-135` E4). ⚠️ **Der Bau hat
keine Sonde** – er braucht `pandoc` und `mmdc`, und kein Prüflauf fährt ihn.

**Nachbarfund im Manifest von `openai-codex`:** Die Notiz nannte Prüfung 86 als die, die
`AGENTS.override.md` meldet; es ist Prüfung 88.

**Nachbarfund am Sondenapparat:** Der Kopf des Bündels zu Prüfung 81 sagte *„VIER
EINHEITEN"*; es waren seit `1.4.1` sechs. Berichtigt auf sieben.

## 4. Abnahme

| Lauf | Ergebnis |
|---|---|
| `validate-framework.py --root .` | **0 Fehler, 0 Warnungen** |
| `probe-pruefungen.py .` mit `PYTHONIOENCODING=utf-8` | 🟢 **alle Sonden und Gegenproben bestanden**, 324 Einheiten, Exit 0 |
| `probe-pruefungen.py .` ohne | 🟢 **alle Sonden und Gegenproben bestanden**, 324 Einheiten, Exit 0 |
| Ergebniszeilen oberhalb der Trennlinie, beide Läufe | 🟢 **zeilengleich** (518 Zeilen bis zur Trennlinie; darunter nur Laufzeiten, D-94) |

## 5. Was offen bleibt

- ⚠️ **Die Auskunft bleibt eine Auskunft** (D-349): ohne Git keine Aussage, und kein Lauf
  wird rot, wenn sie etwas meldet.
- ⚠️ **`K-120` und `K-121`** – zwei Fragen des Framework Owners, mit diesem Release als
  Klärungspunkte eingetragen, nicht entschieden.
