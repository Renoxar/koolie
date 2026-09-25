# Protokoll: Der wählbare Lieferumfang – und die Liste, die sich nicht ableiten ließ

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-25 |
| Release | `1.8.0` |
| Änderungsantrag | `CR-2026-141` |
| Art | Neue Wahl beim Übernehmen (`install.py --target --lieferumfang`), neue Prüfung, neue Ausgabeform, Vorprüfung der Pfadgrenze – **keine Sitzung, kein Kontingent, kein Modelllauf** |
| Gegenstand | Die Ableitung des Nötigen an sechs frischen Installationen; die reduzierte Installation in allen drei Packs gegen die volle; Heben mit und ohne Wechsel; Prüfung 90; die Windows-Pfadgrenze; der Dateimodus des Archivs von `v1.7.0` |
| Ergebnis | 🟢 **Entschieden, `D-367` bis `D-370`.** 🔴 **Beide Ableitungen des Nötigen scheitern gemessen** – aufgezählt ist die Nachweisschicht. 🟢 **Reduziert und voll melden in jedem Pack dasselbe**, bis auf die `HINWEIS`-Zeilen. 🔴 **`--target` brach an der Pfadgrenze mit falscher Begründung ab**, 🔴 **das Archiv von `v1.7.0` trug `0775`** – beides behoben |

---

## 1. Was gefragt war

Wiederaufnahmepunkt von `1.7.0`, Punkt 3: der wählbare Lieferumfang (D-366, `K-75`), erste
Frage: wie die Liste des *„zur Nutzung Nötigen“* **abgeleitet statt aufgezählt** wird. Vor
dem Bau vorgelegt als Fragen (a) bis (j), angenommen. Während des Baus fragte der Owner nach
einem Qualitätssicherungsrelease (E10). `CR-2026-141` E1 bis E10.

## 2. Messungen vor dem Bau

Sechs frische Installationen – drei Packs, je ohne und mit Muster `general` – über
`install.py --target` aus dem Arbeitsbaum, unter einem kurzen Pfad außerhalb des
Benutzerprofils.

| Messung | Ergebnis | Folge |
|---|---|---|
| **Lesespur**: jede Datei, die `install.py --target`, der Validator (mit und ohne `--strict-overlay`), `--check` und `--list-skills` im Projekt öffnen (Audit-Hook) | **549 von 549** Kerndateien | taugt nicht als Ableitung |
| **Verweishülle** über Prüfung 12, ab den installierten Trägern und den Werkzeugen, mit Verzeichnisverweisen | **548 von 548** | taugt nicht |
| dieselbe, ohne Verzeichnisverweise und ohne die Werkzeuge als Einstieg | 39 Protokolle, 5 Anträge, 6 `build`-Träger **drin**; 46 Skillquellen, 7 Laufzeitträger, 17 Overlay-Vorlagen **draußen** | zu groß und zu klein zugleich |
| **Weglassen**: ohne `governance/change-requests`, `tests/protocols`, `tests/erhebungen`, `build` (350 von 550 Dateien), Validatorausgabe gegen die volle | **+70** *„Pfadangabe existiert nicht“*, alle nach `tests/protocols/` (33 Ziele); **+3** Gegenstandsverluste (76, 77, 80); **sonst nichts** – in allen drei Packs gleich | die Nachweisschicht ist wegzulassen, der Validator ist das Orakel |
| Anteil an den Bytes des Kerns | Anträge 19,7 %, Protokolle 20,9 %, Erhebungen 4,4 %, `build` 2,0 %; `CHANGELOG` 8,4 %, `DECISION_LOG` 8,6 %, `ROADMAP` 3,9 %, Sondenskript 5,4 % | Einzelträger offen (`K-122`) |
| 🔴 `--target` in ein Projekt im Ablagebereich der Sitzung | Abbruch beim Kopieren, `[Errno 2]` an einem Pfad mit 264 Zeichen; Rückbau gehalten; Meldung *„Ist eine Datei darin geöffnet?“* | Vorprüfung (D-368) |
| 🔴 Tar-Einträge von `koolie-1.7.0.tar.gz` nach Schritt 5 | `install.command` **`0775`**, jede Datei `0664` | `-c tar.umask=022` (D-369) |

## 3. Wirkungsnachweis – Sonden und Gegenproben, mit Gegenbeweis

| Einheit | Stand `1.8.0` | Gegenbeweis |
|---|---|---|
| `L367` | OK | mit dem Validator aus `1.7.0`: **FEHL** – je Pack 74 Zeilen nur reduziert (die 70 Verweise, die drei Gegenstandsverluste, das Ergebnis), keine `HINWEIS`-Zeile; mit `install.py` aus `1.7.0`: **FEHL** (Exit 2, `--lieferumfang` unbekannt), danach bricht das Bündel ab |
| `90`, `90b`, `90c` | OK | mit dem Validator aus `1.7.0`: **je FEHL** – er kennt die Datei nicht |
| `90a` | OK | mit dem Validator aus `1.7.0`: OK – **erwartet**: Die Sonde bewacht, daß die Lockerung nicht ins Quellrepositorium durchschlägt, und der alte Validator lockert nirgends |
| `L367a` bis `L367e` | OK | mit `install.py` aus `1.7.0`: nicht mehr erreicht – das Bündel bricht nach `L367` ab |
| `T368` | OK | mit `install.py` aus `1.7.0` nicht erreicht (Bündelabbruch); das alte Verhalten ist in Abschnitt 2 gemessen: Abbruch beim Kopieren, Meldung ohne Grund |
| `T362` (angepaßt) | OK | am Stand vor der Anpassung **FEHL**: *„Kern: 1 zu viel“* – die neue Datei `LIEFERUMFANG` |

Der Gegenbeweis läuft an einer **vollständigen** Kopie des Arbeitsbaums mit den
Werkzeugen aus `v1.7.0`.

## 4. Abnahme

| Lauf | Ergebnis |
|---|---|
| Validator | **0 Fehler, 0 Warnungen**, beide Kodierungsumgebungen |
| Sondenlauf | **337 Einheiten, alle bestanden** (vorher 334; neu das Bündel `sonden_lieferumfang` und die Sonden `90`, `90a`), beide Kodierungsumgebungen Exit 0 und oberhalb der Trennlinie zeilengleich (571 Zeilen), rund 615 s Wanduhr je Lauf; **Abnahmelauf gegen den fertigen Baum zeilengleich** |
| Pilot / Übungsrepo `--strict-overlay` nach der Hebung | beide mit `--target --update`, **552 Kerndateien, 0 abweichend**, keine Zwischenverzeichnisse, `LIEFERUMFANG` = `voll` (zum ersten Mal angelegt). Pilot **1 Fehler, 2 Warnungen**, alle im projekteigenen `CHANGELOG.md`, unverändert; Übungsrepo **0 Fehler, 1 Warnung** (Laufzeitfassung 6.095 Zeichen, unverändert); Auskunft im Pilot weiterhin **38**. Overlay `0.3.13` bzw. `1.4.7` |
| Bau | alle drei Word-Fassungen `v1.8.0` in `build/out/` (2.066.045 / 2.067.363 / 2.062.035 Bytes für `devin-desktop` / `claude-code` / `openai-codex`), im Erzeugnis nachgezählt: Dokumentversion `1.8.0`, *„90 Prüfungen“*, je achtmal `--lieferumfang`, zehnmal `LIEFERUMFANG`, zehnmal `D-367`, dreimal `1.9.0` |

## 5. Nebenhandlungen außerhalb des Kerns

- Signierte Marke `v1.7.0` (vom Owner gesetzt, `Good "git" signature`) **vor** dem
  Gitea-Release gepusht, remote annotiert. Schritte 5 bis 7 aus `RELEASE_PROCESS.md` 4.1:
  `koolie-1.7.0.tar.gz`, **557 Dateien** = `git ls-tree` der Marke, kein CRLF, Lizenz an
  beiden Stellen gleich, kein `build/out/`, `install.command` `0755`, `install.cmd` mit LF;
  wegen des Befunds in Abschnitt 2 mit `-c tar.umask=022` erzeugt, zweimal bytegleich.
  Gitea-Release mit Archiv und Prüfsumme, beide Anhänge bytegleich zurückgelesen.

## 6. Offen und benannt

- Nur `--target` kennt den Lieferumfang; ein Heben von Hand macht ein reduziertes Projekt
  wieder `voll`.
- Die großen Einzelträger mit Entwicklungsbezug gehen auch mit `nutzung` mit (`K-122`).
- Ein Werkzeug, das zur Laufzeit aus der Nachweisschicht liest, fiele nur in Sonde `L367`
  auf – und nur, soweit der Validator es aufruft.
- Die Abnahme des macOS-Starters auf macOS (aus `1.7.0`).
