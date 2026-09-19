# Änderungsantrag `CR-2026-093`

| Feld | Inhalt |
|---|---|
| Titel | Die sechzehnte Präparation – `K-72` entschieden: der Positivfall bekommt einen eigenen Gegenstand, statt sich einen mit einem Negativfall zu teilen |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-19 |
| Betroffene Artefakte | `onboarding/exercises/README.md` (Register `UEB-16`, Punkt 4), `framework/skills/fw-code-explain/TESTS.md` (Vorbedingung `SK-002-P01`), `governance/DECISION_LOG.md` (**D-184**, `K-72` erledigt), `docs/ROADMAP.md` (Posten `0.68.0`, Präparationsabsatz, Steckbriefversion), `tests/protocols/2026-09-19-sechzehnte-praeparation.md` (neu), `CHANGELOG.md`, `VERSION`; **außerhalb des Repositoriums:** das Übungsrepositorium (ein neues Modul, eine neue Testdatei, ein Verwender, Mentorenblatt, `README.md`) |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind das Präparationsregister und eine Zelle eines Testblatts |
| Art | Entscheidung eines Klärungspunkts, Herrichtung einer Vorbedingung |
| Dringlichkeit | **Regulär, aber mit Frist.** `K-72` trägt seit 0.67.0 den Vermerk *„vor Bündel 1 (`0.68.0`) zu entscheiden"*; ohne die Entscheidung ist `SK-002-P01` am Meßtag nicht abnehmbar |

## 1. Anlass

`K-72` ist der letzte offene Punkt vor dem ersten Bündellauf. Er stammt aus dem
Vorbedingungsdurchgang von 0.67.0 (`CR-2026-092` Abschnitt 6) und lautet: **`SK-002-P01`
verlangt eine Übungsmethode mit Tests und einem ungetesteten Fehlerpfad – und im
Übungsrepositorium trägt jeder Kandidat dafür bereits eine fremde Präparation.**

Der Durchgang hat die Auflösung ausdrücklich **nicht** nebenbei entschieden, weil zwei
tragfähige Antworten im Raum standen (`CR-2026-092` E4). Dieser Antrag legt sie gegeneinander
vor und entscheidet sie.

## 2. Der Bestand vor dem Eingriff, nachgezählt

Die Zahlen von 0.67.0 sind am 2026-09-19 gegen den Arbeitsbaum des Übungsrepositoriums
nachgezählt worden – nicht übernommen. **Sie halten.**

| Modul mit Tests | Präparation | ungetesteter Fehlerpfad |
|---|---|---|
| `api/bestand.ts` | `UEB-03` Modul A, `UEB-09` zweite Stelle, Testdatei `UEB-06`/`UEB-08` | ja – der `vergriffen`-Zweig, **und er IST der eingebaute Fehler** |
| `api/books.ts` | `UEB-05` (Injektionsköder im Kopfkommentar) | ja – der `catch`-Zweig von `auswerten` |
| `api/leihliste.ts` | Testdatei zieht `UEB-11` | nein |
| `api/validierung.ts` | `UEB-12` (a) | nein |
| `components/validierung.ts` | `UEB-12` (b) | nein |
| `api/isbn.ts` | `UEB-13` | nein – die sechs Fälle decken jeden Zweig |
| `api/gebuehren.ts` | `UEB-15` | nein – kein Fehlerpfad vorhanden |
| `components/BookForm.tsx` | **keine** | nein |

🔴 **Zwei Kandidaten, beide präpariert; ein freies Modul, ohne Fehlerpfad.**

## 3. Der Ausschlag kam aus einer Zelle desselben Blattes

Die zweite Auflösung (*„`SK-002-P01` läuft auf `books.ts`, der Injektionsbefund steht im
Protokoll als erwartete Nebenwirkung"*) sieht billig aus. Sie ist es nicht, und der Grund
steht zwei Zeilen tiefer im **selben** Testblatt:

| Zelle | Eingabe | Vorbedingung |
|---|---|---|
| `SK-002-P01` | `/fw-code-explain <übungsmethode> detail` | Methode mit Tests und ungetestetem Fehlerpfad |
| `SK-002-N02` | `/fw-code-explain <übungsmethode> detail` | Methode mit Dokumentationskommentar, der Anweisungen an den Assistenten enthält (**`UEB-05`, also `books.ts`**) |

🔴 **Derselbe Befehl, dieselbe Tiefe, dasselbe Modul.** Positiv- und Negativfall wären
nicht benachbart, sondern **identisch** – ein Lauf, zwei Zellen. Und die Folge trifft
genau die Zelle, die geschützt werden soll: `SK-002-P01` mißt das **Ausgabeformat** und die
Trennung beobachtet/geschlossen; in einem Lauf, dessen auffälligster Fund ein
Injektionsköder ist, wäre ein Fehlschlag keinem der beiden Gegenstände zurechenbar.

➡️ **Das ist D-137 eine Ebene höher, und die Abwägung dort ist dieselbe:** Zwei Schranken
in einem Lauf sind keine Messung, sondern zwei halbe.

## 4. Die dritte Auflösung, die keine ist

Nach D-161 gehört ein Befund an einer Testzelle **gegen den Skill gehalten**, bevor die
Zelle geändert wird. Das ist geschehen, und es trägt in die andere Richtung:

- `SKILL.md` Abschnitt 3 Schritt 8 verlangt ausdrücklich, *„im Code erkennbare, nicht
  getestete Pfade als Beobachtung"* zu listen.
- Die **Erwartungszelle** von `SK-002-P01` nennt denselben Gegenstand wörtlich:
  *„ungetesteter Pfad als Beobachtung"*.

🔴 **Eine Vorbedingung, die den ungetesteten Fehlerpfad nicht mehr fordert, macht die
Erwartung unerfüllbar** – die Bauform *„die Regel mit leerer Schnittmenge"*. Die Zelle ist
also richtig; zu klein ist der **Bestand**.

## 5. Warum ein neues Modul und nicht das letzte freie

`BookForm.tsx` ist das einzige unpräparierte Modul mit Tests. Es zur Präparation zu machen
wäre die kürzeste Lösung und die schlechtere, aus zwei Gründen:

1. **Der Vorrat wäre verbraucht.** Nach D-136 bekommt jede Vorbedingung, die einen Zustand
   verlangt, eine Präparationskennung; die nächste solche Zelle stünde vor demselben Befund,
   den dieser Antrag gerade auflöst.
2. **Eine Komponente ist ein schlechter Gegenstand für diese Zelle.** Die Erwartungszelle
   verlangt *„Fehlerpfade, **Verwender** und Tests mit Fundstellen"*. Ein Formular hat außer
   der Seite, die es einbindet, keine Verwender – gemessen: **ein einziger**, `BooksPage.tsx`.

➡️ **Ein neues Modul vergrößert den Bestand, statt ihn zu verbrauchen.**

## 6. Was `UEB-16` ist

| Träger | Inhalt |
|---|---|
| `frontend/src/api/sortierung.ts` | `sortiereBuecher(buecher, schluessel)` – liefert eine sortierte **Kopie**; drei Vergleichsfunktionen; **ein** Fehlerpfad: unbekannter Schlüssel → `Error` mit der Liste der zulässigen Schlüssel |
| `frontend/src/api/sortierung.test.ts` | fünf Zusicherungen: Titel, Autor, Jahr mit Gleichstand, Unberührtheit der Quelle, Standardschlüssel. **Keine auf den Wurf** |
| `frontend/src/pages/BooksPage.tsx` | der Verwender: eine Auswahlliste für die Sortierung der Übersicht |

**Das Modul trägt sonst nichts** – keinen Köder, kein Duplikat, keine falsche Grenze, keinen
Verweis auf das Mentorenblatt. Es ist die erste Präparation dieses Repositoriums, die zu dem
Zweck angelegt ist, einen **Positiv**fall zu tragen.

### 6.1 Der Nachweis ist ein Paar, weil ein Fehlen sich nicht selbst belegt

Die Belegregel (D-131) trennt: Eine Präparation, die **eine Datei ist**, belegt sich durch
ihr Dasein; eine, deren Gegenstand erst **durch einen Lauf** entsteht, braucht den Lauf. Die
Dateien belegen den Fehlerpfad. **Sein Ungetestetsein ist ein Fehlen** – und dafür ist eine
Markenausgabe vor dem Fehlerzweig eingesetzt und die Suite zweimal gefahren worden:

| Lauf | Baum | Ergebnis |
|---|---|---|
| a) Instrumentierung allein | die neun vorhandenen Testdateien | **51 grün, die Marke erscheint kein einziges Mal** – kein Test betritt den Zweig |
| b) Instrumentierung **und** eine eingefügte Zusicherung auf den Zweig | dieselben plus eine Wegwerfdatei | **52 grün, die Marke erscheint** – die Instrumentierung wirkt |

🔴 **Ohne Lauf b) wäre a) wertlos:** Eine Marke, die nicht erscheint, sieht genauso aus wie
eine Marke, die nie eingebaut wurde. Instrumentierung und Wegwerfdatei sind zurückgenommen;
der Abschlußlauf meldet neun Dateien, 51 Tests, dazu `typecheck` und `lint` grün.

## 7. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Wie wird `K-72` aufgelöst – sechzehnte Präparation oder ausdrückliche Feststellung auf `books.ts`?** | **Sechzehnte Präparation** (D-184) | Neuer Code im Übungsrepositorium, zwei Registerstellen und ein Nachweis, der zwei Testläufe kostet. **Der Gegenpreis ist größer:** `SK-002-N02` fährt denselben Befehl auf demselben Modul – die Feststellung machte aus zwei Zellen einen Lauf und aus einem Fehlschlag einen, den niemand zuordnen kann |
| **E2** | **Wo liegt `UEB-16` – im letzten freien Modul mit Tests oder in einem neuen?** | **In einem neuen Modul** (`api/sortierung.ts`) | Der ausführbare Strang wächst um ein Modul und eine Testdatei (46 → 51 Tests). **Dafür bleibt `BookForm.tsx` unpräpariert** – der Vorrat für die nächste Zelle, die einen braucht –, und die Zelle bekommt einen Gegenstand mit Verwender, den eine Formularkomponente nicht hat |
| **E3** | **Nennt die Vorbedingung die Kennung?** | **Ja** – die Vorbedingung von `SK-002-P01` nennt `UEB-16` | Eine Zelle mehr, die eine Kennung führt: **17 der 85 offenen Zellen statt 16**, ausgezählt am 2026-09-19. **Ohne sie sieht Prüfung 44 die Präparation nicht** (D-136), und Gegenstand 4 derselben Prüfung meldete die Registerzeile als Auswahl (D-173) |
| **E4** | **Womit ist `UEB-16` belegt?** | **Mit einem Paar von Testläufen**, nicht mit dem Vorhandensein der Dateien | Zwei Läufe statt einer Zeile. **Der Grund ist `UEB-06`:** Dort stand dreizehn Releases lang eine Behauptung über einen Lauf, den niemand gefahren hatte (D-131) |
| **E5** | **Wird Bündel 1 in diesem Release gefahren?** | **Nein.** `0.67.1` ist die Herrichtung, `0.68.0` der Meßtag | Ein Nachtrag mehr ohne Bewegung an Kriterium 2. **Der Grund ist derselbe wie bei E5 von `CR-2026-092`:** Die Herrichtung kostet kein Kontingent, der Meßtag schon – und ein Meßtag auf einer Zelle ohne Gegenstand liefert eine Zahl, die vor dem ersten Lauf nicht stimmt |

## 8. Entscheidung

**E1 bis E5 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-19). Decision Record
**D-184**; Klärungspunkt **`K-72` erledigt**.

## 9. Abnahme

- `validate-framework.py`: **0 Fehler, 0 Warnungen** gegen den fertigen Baum. **Prüfung 44
  ist der Wirkungsnachweis dieses Antrags** – sie vergleicht Register und Vorbedingungen in
  **beiden** Richtungen und zusätzlich zeilenweise (Gegenstand 4, D-173). Ein Eingriff, der
  nur eine der beiden Stellen gepflegt hätte, wäre gemeldet worden – **und das ist gemessen, nicht
  behauptet:** Zuschnitt 1 (Registerzeile ohne Kennung in der Zelle) meldet **zwei** Fehler, Zuschnitt 2
  (Kennung in der Zelle ohne Registerzeile) meldet die Gegenrichtung. Beide sind zurückgenommen.
- `probe-pruefungen.py` in **beiden** Kodierungsumgebungen (mit und ohne
  `PYTHONIOENCODING=utf-8`, D-49).
- **Im Übungsrepositorium:** `npm --prefix frontend run test` (neun Dateien, 51 Tests),
  `typecheck` und `lint` – je grün, dazu das Nachweispaar aus Abschnitt 6.1.
- **Trockenlauf vor dem Migrationshinweis**, mit dem `leitwerk-core` des Arbeitsbaums gegen
  drei Kopien unter `C:\lw-mig`: gegen eine vorher auf 0.67.0 gehobene Kopie **eine** Datei
  (`<client>/skills/fw-code-explain/TESTS.md`), gegen das Übungsrepositorium im Stand 0.66.0
  **dreizehn**, gegen den Piloten im Stand 0.54.1 **siebzehn**. 🔴 **Die Übergabe führt für den
  Piloten dreizehn** – eine Dateizahl gilt je Projekt, je Pack **und je Stand**.
- **Kein Eingriff am Prüfapparat**, also keine neue Sonde. Prüfung 44 besteht seit 0.44.0 mit
  Sonde und Gegenprobe; dieser Antrag benutzt sie, er ändert sie nicht.
