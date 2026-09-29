# Protokoll: Die Aufteilung der Prüfwerkzeuge zu `1.19.1` – und wie belegt ist, dass keine Prüfung verloren ging

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-29 |
| Release | `1.19.1` (`CR-2026-161`, D-479 bis D-484) |
| Gegenstand | Aufteilung von `validate-framework.py` und `probe-pruefungen.py` in Einstieg und Paket (`K-174` Teil 2); Prüfungen 104 und 105; Prüfung 46 (`K-38`, `K-98`) |
| Client Pack | keines – kein Sitzungslauf, ohne Kontingent |
| Messort | das Hauptverzeichnis (Ausgangslauf, danach Commit 1) und ein zweiter Arbeitsbaum des Repositoriums (`git worktree`) für den Inhalt |
| Belege | Erhebungsablage `leitwerk-erhebungen-2026-09-29-1191` außerhalb des Repositoriums: Schnittwerkzeug `schnitt.py` mit `steuer_validator.py`, `steuer_sonden.py`, `anpassen.py`, `inventar.py` und `bauen.sh`; die Inhaltsschritte `inhalt_*.py`; alle Ausgaben der Läufe |
| Kosten | keine |

## 1. Das Werkzeug

Geschnitten hat ein Werkzeug, nicht die Hand. Es liest die Datei als Syntaxbaum, ordnet jeden Knoten der obersten Ebene samt der Kommentare davor genau einem Modul zu und lässt ihn **unverändert**. Welche Namen ein Modul aus einem anderen liest, sagt die Symboltabelle des Interpreters; daraus entsteht je Modul ein ausdrücklicher Import. Im Validator ordnet eine Liste die 117 Prüffunktionen einem Gegenstand zu, Hilfsfunktionen und Konstanten folgen ihren Nutzern, was mehr als ein Gegenstand braucht, geht nach `gemeinsam.py`. Im Sondenskript schneidet es an Abschnittsbannern in der Reihenfolge der Datei, weil die Reihenfolge der Anmeldung die Reihenfolge der Ausgabe ist (D-49); Filter, Läufer und zwei Helfer, die fast jeder Teil braucht, wandern in den Apparat.

Ergebnis: zehn Prüfmodule zwischen 632 und 1.502 Zeilen, der Apparat und zehn Sondenteile zwischen 505 und 1.491 Zeilen; keine Zyklen, jedes Themenmodul liest nur aus `gemeinsam.py`, kein Sondenteil aus einem späteren.

## 2. Was die Analyse vor dem Schnitt fand

| # | Befund | Folge |
|---|---|---|
| 1 | 🔴 `MATRIXZEILE_RE` stand zweimal im Validator, mit `[A-Z]{1,2}\d+` (Prüfung 25) und `[A-Z]\d+` (Prüfung 31). Der Modulraum wird ganz ausgeführt, bevor `main()` läuft – die spätere Bindung galt für beide | Latent: kein Pack führt eine zweibuchstabige Kennung. Der Schnitt lässt die tote Bindung fallen (Verhalten unverändert); Commit 2 gibt Prüfung 25 ihr eigenes Muster, Sonde `25b` (D-480) |
| 2 | `ZELLTRENNER_RE` stand zweimal gleich | Die zweite Bindung entfällt |
| 3 | Die Sonden zu den Prüfungen 29 und 32 teilten den Funktionsnamen `_anker_verlieren` | Harmlos, weil jede Sonde ihre Funktion beim Laden anmeldet; in Commit 2 nach der Prüfung benannt |

## 3. Beleg 1 – der Syntaxbaum

`inventar.py` vergleicht je Knoten der obersten Ebene den normalisierten Syntaxbaum, getrennt davon die Importe.

| | vorher | nachher | nur vorher | nur nachher |
|---|---|---|---|---|
| Validator | 474 | 472 | die zwei toten Bindungen | – |
| Sondenskript | 1.278 | 1.279 | – | die Pfadzeile des Einstiegs |

Die Selbstbezüge sind **vor** dem Schnitt in der Einzeldatei angepasst (24 bzw. 13 Zeilen), damit der Schnitt selbst rein mechanisch bleibt: Prüfung 40 liest Einstieg und Paket, Prüfung 75 die Module mit dem alten Namen, Prüfung 76 die Kernlage in `pruefungen/gemeinsam.py`, die Sonden `D398`, `71`, `75c` und `87` ihren Gegenstand im Modul. **Gegenprobe:** Der alte Validator meldet am geteilten Baum genau diese drei Selbstbezüge (Prüfungen 40, 75, 76) und nichts sonst – die Prüfungen haben den Umbau bemerkt.

## 4. Beleg 2 – die Ausgabe des Validators

Vorher und nachher `0 Fehler, 0 Warnungen`, zeilengleich in beiden Kodierungen. Die vier Lader, die den Validator als Modul holen (`mandat.py`, `apparat/stand.py`, `mcp-waechter.py`, `zaehlen46.py`), finden ihre Namen über den Einstieg; der Selbsttest des Messapparats trägt 10 von 10.

## 5. Beleg 3 – der Sondenlauf

| Lauf | Einheiten | Zeilen oberhalb der Trennlinie | Ergebnis | Wanduhr cp1252 / UTF-8 |
|---|---|---|---|---|
| Ausgangslauf `9e7cb52` | 384 | 729, beide Kodierungen zeilengleich | alle bestanden | 1.161 s / 1.475 s |
| Commit 1 `3d6089e` (Schnitt) | 384 | 729, beide Kodierungen zeilengleich, **zeilengleich zum Ausgangslauf** | alle bestanden | 1.667 s / 1.782 s |
| Commit 2 (Inhalt) | 399 | 744, beide Kodierungen zeilengleich | alle bestanden | 1.738 s / 1.840 s |

Die längeren Wanduhren der Commits 1 und 2 kommen daher, dass beide Läufe gleichzeitig fuhren. Gegenüber dem Ausgangslauf trägt Commit 2 genau die 15 neuen Einheiten (`25b`, `46g`, `46h`, Gegenprobe `46d`, `104a` bis `104e`, Gegenprobe `104a`, `105a` bis `105c`, Gegenproben `105a` und `105b`); geändert sind nur zwei Zeilen, die Zahlen nennen (Selbstprobe `B1`: 384 → 399 Einheiten, Gegenprobe `85a`: die geltende Version).

🔴 **Ein erster Lauf des Schnitts fiel an Gegenprobe `78a`:** Sie baut aus der Kopie ein Repositorium und zählt die versionierten Dateien – mit den neuen Modulen 641 statt 618. Der Schnitt ändert also den gezählten Satz des Hauptdokuments; Commit 1 trägt ihn mit.

## 6. Die neuen Prüfungen

- **Prüfung 104** (D-481): Der erste Entwurf verlangte den Aufruf jeder Prüfung aus `main()`. `check_skills_in` wird aber von `check_skills` gerufen – die Regel lautet deshalb „gerufen, in `main()` höchstens einmal“.
- **Prüfung 105** (D-482, `K-40`): Der erste Entwurf warnte bei `devin-desktop`, die Spanne `3.10.x` sei durch keine Messung belegt. Die Zelle erwähnt sie nur: *„wird ohne Messung gegen 3.10.x nicht gehoben“*. Seither zählen nur Spannen in Backticks; die Stelle ist Gegenprobe `105b`. Bei `kiro` stehen Nebenversionen in derselben Zelle – geprüft wird die erste Version, und jede Spanne muss belegt sein.
- **Prüfung 46** (D-483): der Meldetext mit beiden Lesarten (`K-38`); die Markerform außerhalb des Zählbereichs als eigener Gegenstand vor der Zählung, weil die Prüfung bei einer stimmenden Standzeile früh zurückkehrt (`K-98`).

## 7. Nebenbefunde und Arbeitsweise

- Zwei Klärungspunkte neu: `K-196` (Doppelungen innerhalb der Prüfungen) und `K-197` (Kopie je Bahn statt je Einheit – ein Abnahmelauf kostet rund 20 Minuten Wanduhr, und D-49 verlangt ihn zweimal; auf Wunsch des Owners).
- `pyflakes` über beide Pakete, einmalig und ohne Installation ins Projekt: keine ungenutzten Importe, keine ungebundenen Namen. Ungenutzt sind im Einstieg nur die Schnittstelle der Lader und die Sondenteile, die beim Laden ihre Einheiten anmelden – beides mit Absicht.
- Der zweite Arbeitsbaum braucht die ignorierten Erzeugnisse des Hauptverzeichnisses (`.devin/`, `.koolie/project-overlay/`, `AGENTS.md`); ohne sie meldet der Validator 75 Fehler, die keine sind.
