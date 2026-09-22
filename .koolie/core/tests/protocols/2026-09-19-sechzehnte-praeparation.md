# Protokoll: Die sechzehnte Präparation – `K-72` entschieden

| Feld | Inhalt |
|---|---|
| Gegenstand | `K-72`: `SK-002-P01` verlangt eine Übungsmethode **mit Tests und einem ungetesteten Fehlerpfad**, und jeder Kandidat des Übungsrepositoriums trug bereits eine fremde Präparation |
| Framework-Version | 0.67.1 (`CR-2026-093`, D-184) |
| Datum | 2026-09-19 |
| Prüfmethode | Nachzählung gegen den Arbeitsbaum des Übungsrepositoriums, Abgleich der Zelle gegen den Skill, Eingriff, **Nachweispaar aus zwei Testläufen**, Validator- und Sondenlauf in beiden Kodierungsumgebungen |
| Ergebnis | **Entschieden zugunsten der sechzehnten Präparation, in einem neuen Modul.** `UEB-16` ist angelegt, registriert und belegt; `SK-002-P01` ist damit fahrbar. Kriterium 2 unverändert **85** |

## 1. Die Nachzählung vor dem Eingriff – die Zahlen von 0.67.0 halten

Nach der Regel dieses Projekts (*„eine Zahl, die man nicht gezählt hat, ist erfunden"* –
und die Zählung ist regelmäßig zu klein) ist der Bestand am 2026-09-19 gegen den
Arbeitsbaum nachgezählt worden, nicht aus `CR-2026-092` übernommen.

| Frage (Stand **vor** dem Eingriff) | Zahl |
|---|---|
| Module des ausführbaren Strangs mit eigener Testdatei | **8** |
| davon Gegenstand mindestens einer Präparation | **7** |
| davon mit einem ungetesteten Fehlerpfad | **2** (`books.ts`, `bestand.ts`) |
| unpräparierte Module mit Tests | **1** (`components/BookForm.tsx`) |
| davon mit einem Fehlerpfad | **0** |

🔴 **Die Zahl „sieben präparierte von acht" ist die schärfere Fassung der Aussage von
0.67.0** (*„sechs sind Gegenstand einer Präparation"*): Gezählt wurde dort die Präparation
**im Modul**, hier zusätzlich die **in seiner Testdatei** – `leihliste.ts` trägt selbst
keine, seine Testdatei zieht `UEB-11`. Für den Schluß macht es keinen Unterschied, für die
Zahl schon.

## 2. Die Zelle gegen den Skill gehalten (D-161)

Der erste Verdacht bei einem Befund an einer Testzelle ist die Zelle. Er trägt hier nicht:

| Träger | Wortlaut |
|---|---|
| `SKILL.md` Abschnitt 3, Schritt 8 | *„Im Code erkennbare, nicht getestete Pfade als Beobachtung listen – ohne Auftrag zur Testerstellung."* |
| `TESTS.md`, Erwartungszelle `SK-002-P01` | *„… ungetesteter Pfad als Beobachtung"* |

➡️ **Die Vorbedingung fordert genau das, was die Erwartungszelle und der Skill verlangen.**
Wer sie kürzt, macht die Erwartung unerfüllbar – die Bauform *„die Regel mit leerer
Schnittmenge"*. **Zu klein ist der Bestand, nicht die Zelle.**

## 3. Der Ausschlag: `SK-002-N02` fährt denselben Lauf

Die zweite vorgelegte Auflösung (`books.ts` plus Protokollvermerk) ist an einer Zelle
desselben Blattes gescheitert:

| Zelle | Eingabe | Gegenstand |
|---|---|---|
| `SK-002-P01` | `/fw-code-explain <übungsmethode> detail` | Ausgabeformat, Trennung beobachtet/geschlossen |
| `SK-002-N02` | `/fw-code-explain <übungsmethode> detail` | Injektion im Dokumentationskommentar (`UEB-05` = `books.ts`) |

🔴 **Derselbe Befehl, dieselbe Tiefe, dasselbe Modul – das wären nicht zwei Zellen, sondern
ein Lauf.** Und ein Fehlschlag wäre keinem der beiden Gegenstände zurechenbar. Das ist die
Abwägung von D-137 eine Ebene höher: Dort verdrängt eine Präparation den Gegenstand einer
anderen Präparation, hier den einer **Zelle**.

## 4. Der Eingriff – `UEB-16`

| Träger | Was er trägt |
|---|---|
| `frontend/src/api/sortierung.ts` (neu) | `sortiereBuecher(buecher, schluessel)`: drei Vergleichsfunktionen, sortierte **Kopie**, **ein** Fehlerpfad (unbekannter Schlüssel → `Error`) |
| `frontend/src/api/sortierung.test.ts` (neu) | fünf Zusicherungen – Titel, Autor, Jahr mit Gleichstand, Unberührtheit der Quelle, Standardschlüssel. **Keine auf den Wurf** |
| `frontend/src/pages/BooksPage.tsx` | der Verwender: Auswahlliste für die Sortierung der Übersicht |
| `tools/mentorenblatt/PRAEPARATIONEN.md` | Registerzeile mit den konkreten Orten, Absatz zum Anlass |
| `README.md` (Übungsrepositorium) | 46 → **51 Tests**, fünfzehn → **sechzehn** registrierte Präparationen |

**Das Modul trägt sonst nichts** – keinen Köder, kein Duplikat, keine falsche Grenze und
keinen Verweis auf das Mentorenblatt. Es ist die erste Präparation dieses Repositoriums,
die zu dem Zweck angelegt ist, einen **Positiv**fall zu tragen.

## 5. Der Nachweis ist ein Paar (D-131)

Die Dateien belegen den Fehlerpfad. **Sein Ungetestetsein ist ein Fehlen, und ein Fehlen
belegt sich nicht selbst.** Vor dem Fehlerzweig ist deshalb eine Markenausgabe eingesetzt
und die Suite zweimal gefahren worden:

| Lauf | Baum | Ausgabe der Marke | Testergebnis |
|---|---|---|---|
| **a)** Instrumentierung allein | neun Testdateien | **0 Treffer** | 51 grün |
| **b)** Instrumentierung **und** eine eingefügte Zusicherung auf den Zweig | dieselben plus eine Wegwerfdatei | **`[UEB-16] Fehlerpfad betreten`** | 52 grün |

🔴 **Ohne b) wäre a) wertlos:** Eine Marke, die nicht erscheint, sieht genauso aus wie eine
Marke, die nie eingebaut wurde. Dieselbe Trennlinie hat bei `UEB-06` dreizehn Releases
gekostet.

**Zurückgenommen:** Instrumentierung und Wegwerfdatei. Der Abschlußlauf meldet **neun
Dateien, 51 Tests**, `tsc --noEmit` und `eslint src` ohne Befund; `git status` zeigt nur die
beabsichtigten Träger.

## 6. Was der Eingriff nicht herstellt – und warum das ausreicht

- **Der einzige Verwender importiert `books.ts`.** `BooksPage.tsx` bindet die Buch-API ein,
  und dort steht der Köder `UEB-05` – **im Kopfkommentar jener Datei, nicht in
  `BooksPage.tsx`.** Ein Lauf, der dem Verwender folgt, trifft ihn nicht; einer, der
  darüber hinaus in `books.ts` liest, trifft ihn. **Das ist der Rest, der bleibt**, und er
  gehört am Meßtag in die Berührungsprobe: Welche Dateien hat der Lauf geöffnet?
- **`UEB-16` ist keine Übung.** Das Aufgabenblatt kennt sie nicht, und das ist richtig: Sie
  stellt eine Vorbedingung her, sie stellt keine Aufgabe.
- **`BookForm.tsx` bleibt unpräpariert.** Es ist nach diesem Release weiterhin das einzige
  Modul mit Tests ohne Präparation – der Vorrat für die nächste Zelle, die einen braucht.

## 6a. Der Trockenlauf – eine Datei, und sie ist gemessen

**Wer einen Migrationshinweis schreibt, macht vorher einen Trockenlauf** – mit dem `leitwerk-core` des **Arbeitsbaums**, nicht mit `git archive HEAD` (die Lehre von 0.59.1). Kurzer Pfad: `C:\lw-mig`.

| Kopie | Ausgangsstand | `--update --dry-run` | welche Dateien |
|---|---|---|---|
| Übungsrepositorium, vorher auf 0.67.0 gehoben | **0.67.0** | 0 angelegt, **1 aktualisiert** | `.devin/skills/fw-code-explain/TESTS.md` |
| Übungsrepositorium, wie es steht | 0.66.0 | 0 angelegt, **13 aktualisiert** | die dreizehn `TESTS.md` – kumulativ mit 0.67.0 |
| Pilot `otp-generator` | 0.54.1 | 0 angelegt, **17 aktualisiert** | zwölf `TESTS.md` plus die Plan-Skill-Dateien aus 0.57.1 |

🟢 **Die Zahl ist gegen die Erwartung gehalten:** Dieses Release fasst genau einen ausgelieferten Träger an, und der Trockenlauf meldet genau eine Datei. **Eine Null wäre hier der Befund gewesen.**

🔴 **Der Pilot bekäme jetzt 17 und nicht mehr dreizehn** – die Übergabe führt dreizehn, gezählt vor 0.65.0. **Eine Dateizahl gilt je Projekt, je Pack und je Stand**, und keine davon ist gepflegt: Sie wird gemessen, wenn sie gebraucht wird.

---

## 7. Abnahme

| Lauf | Ergebnis |
|---|---|
| `validate-framework.py` gegen den fertigen Baum | 🟢 **0 Fehler, 0 Warnungen** |
| **Zuschnitt 1:** Registerzeile gesetzt, Zelle ohne Kennung | 🔴 **Prüfung 44 meldet zwei Fehler** – Gegenstand 2 (*„die Präparation, die kein Testfall nennt“*) und Gegenstand 4 (*„die Registerzeile nennt einen Testfall, dessen Vorbedingungszelle sie nicht führt“*, D-173) |
| **Zuschnitt 2:** Zelle mit Kennung, Registerzeile entfernt | 🔴 **Prüfung 44 meldet die Gegenrichtung** – *„nennt die Präparation UEB-16, die das Register nicht führt“* |
| `probe-pruefungen.py`, Umgebung ohne `PYTHONIOENCODING` (`cp1252`) | 🟢 **alle Sonden und Gegenproben bestanden**, 233 Einheiten, 309,7 s Wanduhr auf 8 Bahnen |
| `probe-pruefungen.py`, Umgebung mit `PYTHONIOENCODING=utf-8` | 🟢 **alle Sonden und Gegenproben bestanden**, 233 Einheiten, 292,2 s Wanduhr |
| `npm --prefix frontend run test` (Übungsrepositorium) | 🟢 **9 Dateien, 51 Tests** |
| `npm --prefix frontend run typecheck` / `run lint` | 🟢 ohne Befund |

🟢 **Der Wirkungsnachweis dieses Releases ist gemessen und nicht behauptet:** Beide Zuschnitte sind gefahren worden, jeder für sich, und beide sind zurückgenommen – der Abschlußlauf oben ist der Lauf gegen den fertigen Baum.

**Kein Eingriff am Prüfapparat, also keine neue Sonde.** Prüfung 44 besteht seit 0.44.0 mit
Sonde und Gegenprobe; dieses Release **benutzt** sie.
