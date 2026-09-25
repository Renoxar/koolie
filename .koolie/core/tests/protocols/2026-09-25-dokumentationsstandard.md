# Protokoll: Der Dokumentationsstandard – und die Roadmap, die zu zwei Dritteln Rückblick war

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-25 |
| Release | `1.9.0` |
| Änderungsantrag | `CR-2026-142` |
| Art | Qualitätssicherungsrelease der Dokumentation: Kriterien, vier neue Prüfungen, eine Bauform des Hauptdokuments, Durchsicht der Klassen A und D, Kürzung der Roadmap – **keine Sitzung mit einem Client, kein Kontingent**; die Kaltleser-Probe lief mit fünf kurzen Modellläufen |
| Gegenstand | Bestand und Merkmale aller Dokumente; die Prüfungen 91 bis 94 gegen den Bestand `v1.8.0`; die Kennungen der gestrichenen Roadmap-Blöcke; die Kaltleser-Probe an README, Übernahmeleitfaden und Quick-Start |
| Ergebnis | 🟢 **Entschieden, `D-371` bis `D-380`.** Vier Klassen mit Kriterien; die Prüfungen 91 bis 94 melden gegen den Bestand `v1.8.0` 26 Befunde und laufen nach der Durchsicht still; Klassen A und D durchgesehen; Roadmap 337 → rund 114 KB ohne verlorene Kennung; die Kaltleser-Probe fand fünf unerklärte Begriffe und kein falsch |

---

## 1. Was gefragt war

Wiederaufnahmepunkt von `1.8.0`, Punkt 2: das Qualitätssicherungsrelease der Dokumentation
(D-370). Zuerst der Vorbedingungsdurchgang, dann die Entscheidungsfragen (a) bis (l),
vorgelegt am 2026-09-25 und angenommen (*„Passt, fahre so fort“*). `CR-2026-142` E1 bis E12.

## 2. Messungen vor dem Bau

| Messung | Ergebnis | Folge |
|---|---|---|
| Bestand | 559 versionierte Dateien, 352 Nachweisschicht; 181 Markdown-Dokumente außerhalb (3,2 MB) und 34 Kapitelquellen | vier Klassen (D-371) |
| Wörter mit „ß“ | 308 verschiedene; **603** Treffer der Schreibung vor 1996 gegen **1.192** geltende; **19** Dokumente mischen beide; außerhalb der Register **74** in 14 Dokumenten | Prüfung 92, Umstellung (D-373) |
| Geschichtsmarken | 316, davon 180 im Decision Log | Regel D-376, keine Prüfung |
| Steckbrief | 99 von 215; ohne 116, nach begründeten Ausnahmen **5** | Prüfung 94 (D-375) |
| Form | Codeblöcke, Ebenen, Tabellen sauber; **1** Datei mit drei Hauptüberschriften (`fw-reviewer.md`) | Prüfung 93 (D-374) |
| Roadmap | 337 KB, davon rund 200 KB Rückblicke vor `1.0.0` | Kürzung (D-378) |
| Kapitel 31 | *„502 Dateien, 123 Anträge“* zu `0.89.0`; *„78 Dateien, bei beiden Packs“* | Bau setzt ein (D-377) |

**Gegenbeweis der Prüfungen gegen den Bestand `v1.8.0`:** Der neue Validator meldete am
unveränderten Baum **26 Fehler** – 14 Dokumente mit alter Schreibung (74 Wörter), eine Datei
mit drei Hauptüberschriften, fünf ohne Steckbrief, dazu die erwarteten Registerbefunde.

## 3. Wirkungsnachweis – Sonden und Gegenproben, mit Gegenbeweis

| Einheit | Stand `1.9.0` | Gegenbeweis (Validator aus `v1.8.0`) |
|---|---|---|
| `91a`, `91b` (Sonden) | OK | **je FEHL** |
| `92a`, `92b` (Sonden) | OK | **je FEHL** |
| `93a` bis `93d` (Sonden) | OK | **je FEHL** |
| `94a`, `94b` (Sonden) | OK | **je FEHL** |
| Gegenproben `91a`, `92a`–`92c`, `93a`, `93b`, `94a` | OK | OK – **erwartet**: der alte Validator meldet nichts davon |
| Bau mit `assemble.py` aus `v1.8.0` | – | läuft durch und lässt **23** `{{ZAHL:…}}`, **2** `{{VERSION}}`, **2** `{{CLIENT}}` unaufgelöst im Dokument stehen |

Der Gegenbeweis lief an einer vollständigen Kopie des Arbeitsbaums außerhalb des
Repositoriums, die danach gelöscht wurde.

## 4. Die Kaltleser-Probe (D-379)

Je Dokument eine frische Sitzung (kleinstes verfügbares Modell), die **nur** das eine
Dokument lesen durfte und fünf feste Fragen eines Erstlesers beantwortete. Das Soll ist vor
den Läufen aus den Dokumenten geschrieben worden.

| Lauf | Dokument | richtig | teilweise | falsch | Befund am Dokument → Abhilfe |
|---|---|---|---|---|---|
| 1 | Wurzel-README | 4 | 1 | 0 | Aktivierung und *„bis dahin nur lesend“* fehlten im Installationsweg → Schritt 4 ergänzt; Kennungen unerklärt → Satz ergänzt |
| 1 | Übernahmeleitfaden | 4 | 1 | 0 | Commit im Projekt (D-343) fehlte in der Aktualisierung → Schritt 6; Kennungen unerklärt → Satz ergänzt |
| 1 | Quick-Start | 5 | 0 | 0 | Kürzel P, R, M unerklärt → Verweis auf ihre Fundstellen |
| 2 | Wurzel-README | 5 | 0 | 0 | *„Overlay-Muster“* unerklärt → Satz ergänzt |
| 2 | Übernahmeleitfaden | 4 | 1 | 0 | Commit jetzt genannt (unter Frage 1); *„Laufzeitschicht“* unerklärt → Erklärung beim ersten Auftreten |

**Kein *„falsch“*.** Jeder *„Unklar“*-Hinweis war ein Begriff, der beim ersten Auftreten
nicht erklärt war – dieselbe Bauform in allen fünf Läufen.

## 5. Abnahme

| Lauf | Ergebnis |
|---|---|
| Validator | **0 Fehler, 0 Warnungen**, beide Kodierungsumgebungen |
| Sondenlauf | **341 Einheiten, alle bestanden** (vorher 337; neu die Bündel `sonden_roadmapstand`, `sonden_rechtschreibung`, `sonden_dokumentform`, `sonden_steckbrief`), beide Kodierungsumgebungen Exit 0 und oberhalb der Trennlinie zeilengleich (592 Zeilen), rund 645 s Wanduhr je Lauf; **Abnahmelauf gegen den fertigen Baum** zeilengleich |
| Pilot / Übungsrepo `--strict-overlay` nach der Hebung | beide mit `--target --update`, **555 Kerndateien, 0 abweichend**, `LIEFERUMFANG` = `voll`; aktualisiert nur das Reviewprofil `fw-reviewer`. Pilot **1 Fehler, 2 Warnungen**, alle im projekteigenen `CHANGELOG.md`; Übungsrepo **0 Fehler, 1 Warnung** (Länge der eigenen Regeldatei) – beide unverändert zum Vorstand. Die Prüfungen 91 bis 94 laufen in beiden still |
| Bau | alle drei Word-Fassungen `v1.9.0` in `build/out/` (1.944.424 / 1.945.737 / 1.940.322 Bytes für `devin-desktop` / `claude-code` / `openai-codex`), im Erzeugnis nachgezählt: Dokumentversion `1.9.0`, *„94 Prüfungen“*, Kapitel 31.1 mit **555** Dateien und **78** installierten Dateien je Pack, eingesetzt vom Bau; die vier verbliebenen `{{` sind Zitate aus dem Decision Log, die 84 *„daß“* stehen in eingebetteten Registern |

## 6. Nebenhandlungen außerhalb des Kerns

- Signierte Marke `v1.8.0` (vom Owner gesetzt, `Good "git" signature`) **vor** dem
  Gitea-Release gepusht. Schritte 5 bis 7 aus `RELEASE_PROCESS.md` 4.1, **zum ersten Mal mit
  `-c tar.umask=022` aus dem Prozesstext**: `koolie-1.8.0.tar.gz`, **559 Dateien** = `git
  ls-tree` der Marke, kein CRLF, `install.command` `0755`, alle übrigen 558 Dateien `0644`,
  Lizenz an beiden Stellen gleich, kein `build/out/`; zweimal erzeugt, bytegleich.
  Gitea-Release mit Archiv und Prüfsumme, beide Anhänge bytegleich zurückgelesen.

## 7. Befunde während des Baus

- **Prüfung 93 fand in ihrer ersten Stunde zwei Präparationen des Sondenapparats** (zu
  Prüfung 31), die Tabellenzeilen mit einer Spalte zu viel einfügten. Die Gegenprobe 31 lief
  bis dahin grün, weil keine Prüfung die Spaltenzahl kannte.
- **Prüfung 75** führte die Roadmap als erklärte Fundstelle des alten Namens; nach der
  Kürzung nahm die Ausnahme nichts mehr aus und meldete sich selbst (0.57.1).
- Ein Bearbeitungswerkzeug mit Zeilenstrom (`sed -i`) stellte eine Kapitelquelle auf LF um,
  ein Ersetzungsskript erzeugte im README zwei Wagenrückläufe ohne Zeilenvorschub – beide
  meldeten Prüfung 81 bzw. die Prüfung auf verirrte Steuerzeichen sofort.
- Die Durchsicht hat Befunde geliefert, die eine Entscheidung brauchen: `K-123` bis `K-129`.

## 8. Offen und benannt

- Die inhaltliche Durchsicht der Klasse B (`1.9.1` ff., D-380).
- `K-123` bis `K-129`.
- Die Abnahme des macOS-Starters auf macOS (aus `1.7.0`).
