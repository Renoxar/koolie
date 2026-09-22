# Änderungsantrag `CR-2026-124`

| Feld | Inhalt |
|---|---|
| Titel | `AP11`: Das Hauptdokument gegen den geltenden Stand – und der Erzeuger, der seit der Umbenennung nicht mehr lief |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-22 |
| Betroffene Artefakte | `.koolie/core/build/assemble.py`; **15 der 34 Kapitelquellen** unter `.koolie/core/build/doc/`; `.koolie/core/tests/scripts/validate-framework.py` (**Prüfung 77**, Neutralitätsausnahme); `.koolie/core/tests/scripts/probe-pruefungen.py` (Sonden 77a–c, Gegenprobe 77a); `.koolie/core/tests/TEST_CATALOG.md`; `.koolie/core/docs/RUNTIME_GLOSSARY.md`; `.koolie/core/clients/README.md`; **sieben Änderungsanträge** (`CR-2026-020`, `-021`, `-023`, `-025`, `-026`, `-029`, `-030`, je Abschnitt 6); `README.md`; `.koolie/core/governance/DECISION_LOG.md` (**D-309** bis **D-312**, `K-103` geschlossen, `K-104` neu); `.koolie/core/docs/ROADMAP.md`; `.koolie/core/CHANGELOG.md`; `.koolie/core/VERSION`; `UEBERGABE.md`; `.koolie/core/tests/protocols/2026-09-22-hauptdokument-ap11.md` |
| Ebene laut Entscheidungsbaum 6 | Core (Dokumentquellen, Prüfapparat, Governance-Aufzeichnungen). Kein Projektwert, keine neue Verhaltensregel |
| Art | Änderung (Berichtigung eines Werkzeugs, Fortschreibung eines Dokuments, eine neue Prüfung, eine Ausnahme neu zugeschnitten) |
| Dringlichkeit | hoch. Das Hauptdokument ist **Bestandteil der Lieferung**, und es stand auf einem Stand von vor zweiundvierzig Releases |

---

## 1. Anlass und Problem

### 1.1 Der Befund, der vor dem ersten Handgriff fiel: Das Dokument ließ sich nicht bauen

Der Posten heißt *„das Hauptdokument gegen den geltenden Stand setzen"*. Der erste
Handgriff eines solchen Postens ist, den Meßgegenstand herzustellen – also das Dokument zu
bauen. **Der Bau scheitert seit `0.88.0` an der ersten Einbettungsdirektive:**

```text
FEHLER: eingebettete Datei fehlt (Repository): .koolie/core/framework/core/00-principles.md
```

Die Datei ist da. Was fehlt, ist die Wurzel, gegen die `assemble.py` sie sucht:

```python
CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(CORE)          # ← zählt EINE Ebene
```

🔴 **Das ist die Bauform aus D-299 an einer siebten Stelle.** `0.88.0` hat sechs Stellen
gefunden, die den Kernpfad für ein Verzeichnissegment hielten – vier über
`os.path.basename()`, zwei über gezählte Verzeichnisebenen. Diese hier ist die zweite
Gattung, und sie lag in `build/`. Seit der Kern zwei Segmente tief liegt, liefert der
Ausdruck `.koolie/` statt der Projektwurzel, und **jede** der Einbettungen schlägt fehl.

🔴 **Prüfung 76 hat es nicht gemeldet, und das ist kein Versehen, sondern ihre Grenze.**
Sie hält **vier** Werkzeuge gegeneinander – `clientmap.py`, den Validator, den Schutz-Hook
und `ablage.py`. `assemble.py` ist keines davon. *Eine Prüfung, die eine abgezählte Menge
vergleicht, kann nur so vollständig sein wie ihre Menge* – und die Menge stand in `0.88.0`
fest, bevor jemand den Bau des Hauptdokuments probiert hatte.

⚠️ **Und die Übergabe zu `0.88.1` hat die Folge falsch gebucht.** Sie schrieb, die
Fundstellen des alten Namens im Erzeugnis *„löst der nächste Bau"*. Gemessen: Es gab
keinen nächsten Bau. Und die Fundstellen, die nach der Berichtigung im Erzeugnis bleiben,
stammen aus der **eingebetteten Chronik** – Decision Log und Roadmap – und bleiben dort
nach D-273 ausdrücklich stehen. *Eine Zusage über einen Vorgang, den man nicht ausgeführt
hat, ist eine Vermutung mit Zeitform.*

### 1.2 Der Abstand des Dokuments, als Zahl

| Angabe im Dokument | gemessen am 2026-09-22 |
|---|---|
| Dokumentversion `0.9.0`, Stand 2026-09-10 | Release `0.89.0`, **zweiundvierzig Releases** |
| *„Alle Module im Status `entwurf`"* | **null** auf `entwurf`; 81 Träger mit Steckbriefzeile, **77 auf `pilot`**, vier Ausfüllschlitze |
| *„Kein Mechanismus wurde bislang in einer Zielinstallation ausgeführt"* | `AP2` ist gefahren und für `devin-desktop` mit `0.86.0` **zu Ende geführt**; neun Matrixzeilen sind an einer Installation beobachtet |
| *„Alle dynamischen Tests stehen auf `offen`"* | **keiner**. 38 Katalogzellen und 87 Testblattzellen tragen `bestanden` |
| *„26 technische Zusagen"* (vier Fundstellen) | **31** bei `claude-code`, **36** bei `devin-desktop` |
| *„24 von 34"* / *„25 von 29"* `[TECHNISCH]` | **21 von 36** und **22 von 31**, von Prüfung 31 nachgerechnet |
| *„8 von 34"* / *„2 von 29"* ohne Beleg | **1 von 36** (dauerhaft) und **0 von 31** |
| *„Ein Client Pack enthält vier Dateien"* (vier Fundstellen) | **drei** – seit D-36 (`0.26.0`), und die Aufzählung daneben nennt auch drei |
| *„80 Dateien … 79 bei `claude-code`"* | **78 und 78.** Die Begründung – *„ein Client kennt keine eigene Hook-Datei"* – ist seit D-32 für **beide** Packs hinfällig |
| *„Allgemeingültige Regeln in zehn Modulen: FW-CORE-00 … 10"* | **elf** – die Aufzählung in derselben Zeile nennt elf |
| *„233 versionierte Dateien im Kern"* | **502** |
| *„33 Kapitelquellen"* | **34** |
| *„rund 8.700 Zeichen"* (Wurzel-Anweisungsdatei) | **11.887**, an der erzeugten Datei gemessen – 113 unter der Grenze |
| *„155 Markdown-Dateien"* (zwei Fundstellen) | **450** im Kern |
| *„K-01 bis K-20, D-01 bis D-10"* | **K-01 bis K-103**, **D-01 bis D-308** |

🔴 **Keine dieser Zahlen war falsch geschrieben.** Alle waren bei ihrer Einführung richtig
und sind stehen geblieben, während ihr Gegenstand weiterlief. *Das ist die Bauform von
Prüfung 40 an einem größeren Gegenstand* – und der Grund, warum die Behebung eine Prüfung
braucht und nicht nur eine Textänderung (`E6`).

### 1.3 Zwei Aufzählungen, die ihre eigene Zahl widerlegen

- **„vier Dateien"** – der Satz daneben nennt `manifest.json`, `CLIENT_PACK.md` und die
  README der Laufzeitschicht. **Drei.** Die vierte war die README der Regelablage; sie ist
  mit D-36 in die erste aufgegangen, und die Zahl ist stehen geblieben.
- **„zehn Modulen"** – die Aufzählung in derselben Zeile führt `00` bis `10`. **Elf.**

### 1.4 Der Baum der Referenzstruktur zeigte einen Client und drei überholte Stände

Kapitel 15.2 heißt *„Repository-Struktur"* und zeigte die eines einzigen Client Packs.
Darin: eine **eigene Hook-Datei**, die seit D-32 für kein Pack erzeugt wird; eine **README
der Regelablage**, die es seit D-36 nicht gibt; und `.koolie/core/` sowie
`.koolie/project-overlay/` als zwei **Wurzeleinträge**, obwohl sie seit `0.88.0`
Geschwister unter `.koolie/` sind. Derselbe Baum steht in der Wurzel-README.

### 1.5 Fünf Querverweise auf die Anhänge zeigen auf den falschen Abschnitt

Gemessen: `00-kopf.md` verweist für die Quellen auf `31.3` (richtig: `31.4`) und für das
Platzhalterregister auf `31.2` (richtig: `31.3`); `05-glossar.md` und `08-trennung.md`
ebenso auf `31.2`; `32-abschluss.md` nennt für V2–V10 den Anhang `31.4` statt `31.5`;
`29-grenzen.md` die Quellen unter `31.3`. **Prüfung 12 liest Pfad-Token in Backticks und
keine Abschnittsnummern in Prosa**; Prüfung 63 löst Nummernverweise auf, hatte `build/`
aber über dieselbe Frist ausgenommen wie die Neutralitätsregel.

### 1.6 Ein Kodierungsrest aus `0.9.0`

`29-grenzen.md` trägt seit dem Release, das dieses Dokument erzeugt hat, den Satz
*„Regeln in der Wurzel-Anweisungsdatei und der Regelablage `` wirken …"* – **leere
Backticks**, dreiundvierzig Releases lang.

### 1.7 Nachbarträger, die das Hauptdokument einbettet

- 🔴 **`docs/RUNTIME_GLOSSARY.md` widerspricht sich im selben Träger.** Die Tabelle sagt,
  die Hook-Konfiguration stehe bei **beiden** Packs in der Berechtigungsdatei (D-32); acht
  Zeilen darunter sagt der erläuternde Absatz, sie sei bei `devin-desktop` *„eine eigene
  Datei"*. **Der Absatz, der die Tabelle erklärt, widerspricht ihr** – seit `0.26.0`.
- 🔴 **`clients/README.md` führt `claude-code` als Status `entwurf`**, während das Pack
  selbst `pilot` sagt, und nennt **vier** gemessene Zeilen, wo das Pack **sechs** führt.
  *Zwei Träger desselben Hauses, zwei Zahlen* – die Bauform, die `0.88.1` schon einmal
  bezahlt hat.
- 🔴 **`docs/ROADMAP.md` trägt die Überschrift „Stand nach Release 0.56.0"**, direkt über
  dem Satz *„Wird mit jedem Release fortgeschrieben"*. Gemessen mit `git log -S`: seit
  `0.56.0`, **zweiunddreißig Releases**. Und `29-grenzen.md` schickt seine Leser genau
  dorthin, um den aktuellen Stand zu erfahren.

### 1.8 Zwei Zahlen des Releaseplans für diesen Posten selbst

Der Plan nannte *„`CR-2026-029` und `-030` Abschnitt 6 nachtragen"*. **Gezählt: sieben**
Änderungsanträge haben einen Abschnitt 6 mit `<TBD>` – `CR-2026-020`, `-021`, `-023`,
`-025`, `-026`, `-029` und `-030`.

Und er nannte *„zwölf offene und fünf fehlende Protokollabschnitte"*. Gezählt nach der
Regel *„ein Abschnitt mit `Gegenzeichnung` in der Überschrift, ohne `<TBD>`"*: von 122
Protokollen **13 gegengezeichnet, 45 offen, 64 ohne Abschnitt**; auf die zehn
FW-Testprotokolle eingegrenzt **drei, zwei und fünf**. *„Fünf ganz ohne"* trifft;
*„zwölf mit offenem Abschnitt"* trifft keine der beiden Abgrenzungen.

---

## 2. Vorgeschlagene Änderung

1. **`assemble.py`** leitet die Projektwurzel über `clientmap.projektwurzel(CORE)` ab –
   dieselbe benannte Ableitung wie die vier Werkzeuge aus D-299.
2. **Das Hauptdokument wird gegen den gemessenen Stand gesetzt**; jede Zahl trägt ihr
   Meßdatum oder ihre Fundstelle. **Gemessen: 15 der 34 Kapitelquellen sind geändert** –
   die übrigen 19 tragen ihren Inhalt über Einbettungen und folgen dem Kern.
3. **Der Namensabsatz** aus der Wurzel-README (D-305) kommt in `00-kopf.md`.
4. **Der Baum in Kapitel 15.2 und in der Wurzel-README** steht in Platzhaltern und zeigt
   die Struktur, die eine frische Installation wirklich erzeugt.
5. **Die befristete Neutralitätsausnahme für `build/`** fällt und wird durch eine
   Dauerausnahme über drei benannte Träger ersetzt.
6. **Prüfung 77** hält die Dokumentversion gegen `<CORE_DIR>/VERSION`, mit drei Sonden und
   einer Gegenprobe.
7. **`K-103`** wird geschlossen: Wurzel-README und Hauptdokument nennen den gemessenen
   Status, die Akteursnennungen heißen *„der KI-Client"*.
8. **Abschnitt 6 der sieben Änderungsanträge** wird aus Decision Log und `CHANGELOG.md`
   nachgetragen – nachgetragen, nicht neu entschieden.
9. **Die drei Nachbarträger** aus 1.7 werden berichtigt.

---

## 3. Prüffragen (durch Owner ausgefüllt)

- [x] Richtige Ebene: Core (Dokumentquellen, Prüfapparat, Governance). Kein Projektwert, keine neue Regel.
- [x] Verschärfungsprinzip: unberührt. Prüfung 77 verschärft den Prüfapparat, nicht die Rechte eines Clients.
- [x] Widerspruchsfreiheit geprüft gegen D-02, D-11, D-23, D-32, D-36, D-49, D-112, D-128, D-129, D-216, D-273, D-291, D-299, D-302, D-305 sowie `CR-2026-025` E3.
- [x] Laufzeitfassungen: **nicht betroffen.** Keine Quelle unter `framework/runtime/` und kein Skill geändert; die Referenzinstallation ist vor und nach dem Lauf byte-gleich.
- [x] Belegstatus: Jede neue Zahl im Dokument trägt ihr Meßdatum; keine Produktaussage neu eingeführt.
- [x] Test- und Validierungsbedarf: **Prüfung 77** mit Sonden 77a–c und Gegenprobe 77a; Validator und Sondenlauf in beiden Kodierungsumgebungen als Abnahme.
- [x] Auswirkungen auf Overlays: keine. **Migrationshinweis: keiner** – kein ausgeliefertes Laufzeitartefakt geändert.
- [x] Dokumentation: `CHANGELOG.md`, `DECISION_LOG.md`, `ROADMAP.md`, `RUNTIME_GLOSSARY.md`, `UEBERGABE.md`, Protokoll.

---

## 4. Vorlage zur Entscheidung

| # | Frage | Vorschlag mit Auflösung **und Preis** |
|---|---|---|
| **E1** | **Wird `assemble.py` in diesem Release berichtigt, oder ist das ein eigener Posten?** | **Vorschlag: in diesem Release, als erster Handgriff.** 🔴 **Ohne den Bau gibt es keinen Meßgegenstand:** Ein Dokument, das man nicht erzeugen kann, kann man auch nicht gegen den Stand setzen – jede Aussage über sein Erzeugnis wäre eine Vermutung. **Preis:** Der Posten trägt eine Werkzeugänderung, die nicht in seiner Beschreibung stand. *Das ist der übliche Preis eines Vorbedingungsdurchgangs und war fünfzehnmal in Folge der billigste Befund des Releases.* |
| **E2** | **Bekommt `assemble.py` eine Prüfung – etwa als fünfte Stelle in Prüfung 76?** | **Vorschlag: nein.** 🔴 **Prüfung 76 mißt eine Lageangabe;** `assemble.py` trägt keine, sondern leitet die Wurzel aus dem Kern ab. Eine fünfte Stelle wäre ein anderer Gegenstand in derselben Prüfung, und eine Prüfung mit zwei Gegenständen ist die Bauform, an der `0.85.0` die Quellenzuordnung zerlegt hat. 🟢 **Was statt dessen trägt:** Der Bau ist ab jetzt Teil des Abnahmelaufs und im Protokoll belegt – für **beide** Client Packs. **Preis, benannt:** Ein Bau, der nicht gefahren wird, fällt weiterhin nicht auf. Der Abnahmelauf ist eine Anweisung, keine Schranke. |
| **E3** | **Fällt die befristete Neutralitätsausnahme für `build/`, wie der Releaseplan es verlangt?** | **Vorschlag: sie fällt – aber in eine benannte Dauerausnahme über DREI Träger, nicht in nichts.** 🔴 **Gemessen: 36 Fundstellen, davon 27 in den Anhang- und Abschlußträgern.** Das ist die Gattung, die `NEUTRAL_ABBILDUNG` seit `0.57.1` **dauerhaft** ausnimmt: eine Quellenliste **je Client Pack** und ein Verifikationsbedarf **eines** Packs müssen den Client nennen. 🔴 **Und `CR-2026-025` E3 hat das am 2026-09-10 ausdrücklich so entschieden** – *„die Anhänge beschreiben teils Prüfpunkte gegen die Dokumentation eines konkreten Clients"*. **Die Frist stand zwanzig Releases lang über einer Entscheidung, die sie aufhob.** Verworfen: ersatzlos streichen – das hätte den Beleg verboten und nicht die Bindung. Verworfen: verlängern – *eine Entscheidung, deren Voraussetzung sich ändert, wird neu gestellt* (D-302). **Preis, benannt:** Drei Träger des Hauptdokuments prüfen 14 und 48 dauerhaft nicht; die Grenze steht als Menge im Quelltext, mit Begründung je Träger, und im Laufzeitglossar. |
| **E4** | **Steht der Baum der Referenzstruktur konkret oder in Platzhaltern?** | **Vorschlag: Platzhalter.** 🔴 **Der Baum heißt „Repository-Struktur" und zeigte die eines Clients** – er behauptete für jede Installation, was für eine galt. Verworfen: zwei Bäume, einen je Pack – *zwei Stellen, die einander decken*, laufen auseinander, sobald jemand einen pflegt. ⚠️ **Preis, ein echter:** Der Baum liest sich abstrakter. Anhang 31.2 löst ihn auf, und die Lesehinweise des Deckblatts sagen es. |
| **E5** | **Wird `29-grenzen.md` angefaßt – es ist ein ausdrückliches Zeitdokument?** | **Vorschlag: nur dort, wo kein Zeitdokument steht.** 🟢 Der **Hinweiskasten** darüber ist ausdrücklich der fortgeschriebene Teil und wird fortgeschrieben; die **leeren Backticks** und der **falsche Anhangsverweis** sind Defekte der Wiedergabe und keine historischen Aussagen; **Abschnitt 29.2** steht außerhalb des Kastens und nennt die heutigen Registergrößen. 🔴 **Der Fließtext von 29.1 bleibt unberührt** – *wer ein Zeitdokument glättet, zerstört den Beleg, für den es steht* (D-273). |
| **E6** | **Bekommt der Abstand des Hauptdokuments eine Prüfung?** | **Vorschlag: ja – Prüfung 77, Dokumentversion gegen `VERSION`.** 🔴 **Der Prüfkandidat steht seit `0.53.0` in Abschnitt 3 der Übergabe und ist seither nicht gefahren worden; der Abstand ist in derselben Zeit auf zweiundvierzig Releases gewachsen.** *Ein Kandidat, den man zwei Dutzend Releases nicht anfaßt, ist keine Vertagung, sondern eine Entscheidung ohne Aufzeichnung.* 🟢 **Der Gegenstand ist mechanisch:** Das Dokument wird assembliert und hat keinen eigenen Stand – seine Kopfzeile sagt das selbst (*„entspricht Framework-Release"*), und die Prüfung mißt genau diese Zusage. ⚠️ **Preis, benannt und nicht klein:** Jedes Release faßt diese Zeile an – derselbe Preis, den Prüfung 67 für die Übergabe verlangt, und dort trägt er. **Grenze, ebenso benannt:** Sie mißt die **Version**, nicht den **Inhalt**. Wer die Zeile mitzieht, ohne die Zahlen nachzusehen, läuft durch; dagegen hilft der Durchgang vor dem Commit und keine Prüfung. |
| **E7** | **Wird `K-103` geschlossen – und bekommt die Wurzel-README doch eine Prüfung?** | **Vorschlag: `K-103` schließen, keine Prüfung, aber die Frage neu stellen (`K-104`).** 🟢 **Beide Befunde sind berichtigt**, und dabei sind die eigenen Zahlen des Punktes gefallen: `K-103` nannte *„80 Träger, 73 auf `pilot`"*; gemessen über den Zählbereich von Kriterium 3 sind es **81, 77 und vier Ausfüllschlitze**. 🆕 **Der Grund, aus dem `0.88.1` eine Prüfung abgelehnt hat (`E5`), ist acht Stunden später an anderer Stelle entfallen:** Prüfung 75 unterscheidet am Vorhandensein von `UEBERGABE.md`, ob sie im Framework-Repositorium oder in einer Installation läuft. Damit ist *„grün im Framework, rot in jeder Installation"* kein Hindernis mehr. **Preis:** `K-104` ist ein weiterer offener Punkt, und die Frage bleibt in der Sache schwer – eine Statuszeile ist Prosa, und eine Prüfung auf Prosa trifft die Schreibweise (`K-41`). |
| **E8** | **Wird die Word-Fassung gebaut, wie der Posten es verlangt?** | **Vorschlag: nein, und der Grund ist gemessen.** 🔴 **`pandoc` und das Mermaid-Kommandozeilenwerkzeug sind auf diesem Arbeitsplatz nicht installiert** (`which pandoc`, `which mmdc`, 2026-09-22, beide ohne Treffer). *Eine Word-Fassung, die niemand erzeugt hat, ist kein Lieferbestandteil, sondern eine Zusage.* 🟢 **Der Weg dorthin ist mit diesem Release überhaupt erst frei:** `build-docx.py` liest `build/out/hauptdokument.md`, und das entstand seit `0.88.0` nicht mehr. **Preis:** Der Posten `AP11` ist nicht vollständig abgearbeitet; der Rest bekommt einen eigenen Plan-Posten mit den beiden fehlenden Werkzeugen als benannte Vorbedingung. |
| **E9** | **Wird die Gegenzeichnung der Protokolle nachgezogen?** | **Vorschlag: nein, und das ist keine Vertagung, sondern eine Abgrenzung.** 🔴 **Eine Gegenzeichnung ist die Handlung einer zweiten Rolle** – sie sagt *„ich habe das gelesen und trage es mit"*. Ein Werkzeug, das `<TBD: Rolle>` durch einen Rollennamen ersetzt, **fälscht sie**. 🟢 **Was dieses Release statt dessen leistet:** Die Zahl ist nachgezählt und trägt ihre Zählregel (Abschnitt 1.8). **Preis:** 45 Protokolle behalten einen offenen Abschnitt, 64 haben keinen. |
| **E10** | **Wird Abschnitt 6 der sieben Anträge nachgetragen – und darf ein Nachtrag eine Entscheidung schreiben?** | **Vorschlag: ja, als Nachtrag mit Fundstelle.** 🟢 **Es wird nichts entschieden:** Jede der sieben Entscheidungen steht datiert im Decision Log (`D-28` bis `D-33`) beziehungsweise im `CHANGELOG.md`, und die Auflösungen stehen im Antrag selbst, in seinem Abschnitt „Vorlage zur Entscheidung". Der Nachtrag überträgt, er urteilt nicht – und jeder Block sagt in einem eigenen Satz, daß er nachgetragen ist und woher. **Preis, benannt:** Ein nachgetragener Abschnitt sieht aus wie ein zeitgleich geschriebener. Der Satz darunter ist die einzige Trennlinie, und er steht dort deshalb sichtbar. |
| **E11** | **Welche Version?** | **Vorschlag: `0.89.0` (MINOR).** Nach `governance/RELEASE_PROCESS.md` Abschnitt 1 ist MINOR die Klasse für *„neue Prüfungen und erweiterte Module"*: Prüfung 77 ist neu, die Neutralitätsausnahme ist neu zugeschnitten, und 15 Kapitelquellen sind inhaltlich gesetzt. **Preis:** Der Freigabelauf `1.0.0` rückt eine Nummer weiter; der Rest von `AP11` bekommt `~0.90.0`. |

---

## 5. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** – `E1` bis `E11` in der vorgeschlagenen Auflösung |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Das Hauptdokument ist Bestandteil der Lieferung und stand auf einem Stand von vor zweiundvierzig Releases; sein Erzeuger lief seit der Umbenennung nicht mehr. Die befristete Ausnahme war über zwei Gegenstände gespannt und konnte für einen nie ablaufen – sie wird neu gestellt statt verlängert. Prüfung 77 kostet je Release eine Zeile und ersetzt einen Prüfkandidaten, der zwei Dutzend Releases nicht gefahren wurde. Word-Fassung und Gegenzeichnung sind **benannt und nicht gefahren**, beide mit gemessenem Grund. |
| Ziel-Release | `0.89.0` |
| Decision-Log-Einträge | **D-309** bis **D-312**; `K-103` geschlossen; `K-104` neu |

---

## 6. Umsetzung

- [x] `assemble.py`: Projektwurzel über `clientmap.projektwurzel()`; Bau für **beide** Packs belegt (`E1`, `E2`)
- [x] **15 der 34 Kapitelquellen geändert** – die übrigen 19 tragen ihren Inhalt über Einbettungen und folgen dem Kern ohne eigenen Eingriff; Namensabsatz in `00-kopf.md`
- [x] Baum der Referenzstruktur in Platzhaltern, in Kapitel 15.2 **und** in der Wurzel-README (`E4`, D-310)
- [x] Fünf falsche Anhangsverweise und der Kodierungsrest aus `0.9.0` berichtigt (`E5`)
- [x] Neutralitätsausnahme neu zugeschnitten – Validator **und** Laufzeitglossar (`E3`, D-311)
- [x] **Prüfung 77** samt Sonden 77a–c und Gegenprobe 77a; Register und Sondenmenge an allen drei Stellen nachgezogen (`E6`, D-312)
- [x] `K-103` geschlossen: Wurzel-README und Hauptdokument (`E7`); `K-104` eröffnet
- [x] Abschnitt 6 der **sieben** Anträge nachgetragen, je mit Fundstelle (`E10`)
- [x] `RUNTIME_GLOSSARY.md`, `clients/README.md` und die Standüberschrift der Roadmap berichtigt
- [x] `VERSION`, `CHANGELOG.md`, `ROADMAP.md`, `UEBERGABE.md`, Protokoll
- [x] Validator ohne Fehler; Sondenlauf in **beiden** Kodierungsumgebungen; zeilengleicher Vergleich nach D-49
- [ ] **Word-Fassung: nicht gefahren** (`E8`) – `pandoc` und `mmdc` fehlen; eigener Plan-Posten `~0.90.0`
- [ ] **Gegenzeichnung der Protokolle: nicht nachgezogen** (`E9`) – eine Unterschrift ist eine menschliche Handlung
- [ ] Kommunikation an Projekte: **nicht erforderlich** – kein ausgeliefertes Laufzeitartefakt geändert

---

## 7. Nachbarfunde, gemeldet und behoben

Anders als in den letzten Releases sind die Nachbarfunde hier **behoben** und nicht nur
gemeldet – sie liegen sämtlich in Trägern, die das Hauptdokument **einbettet**, und wären
damit Teil der Lieferung geworden:

1. **`docs/RUNTIME_GLOSSARY.md`**: Der erläuternde Absatz widersprach der Tabelle acht
   Zeilen darüber – seit D-32 (`0.26.0`). Das Beispiel steht jetzt auf der
   MCP-Konfiguration, wo der Unterschied zwischen den Packs wirklich liegt.
2. **`clients/README.md`**: `claude-code` stand auf Status `entwurf`, das Pack selbst auf
   `pilot`; und die Zeile nannte vier gemessene Matrixzeilen statt sechs.
3. **`docs/ROADMAP.md`**: Die Überschrift *„Stand nach Release 0.56.0"* stand direkt über
   dem Satz *„Wird mit jedem Release fortgeschrieben"* – zweiunddreißig Releases lang.

🔴 **Alle drei haben dieselbe Bauform wie der Hauptbefund dieses Antrags:** eine Aussage,
die bei ihrer Einführung richtig war, deren Gegenstand weitergelaufen ist und die niemand
nachgezählt hat, weil keine Prüfung sie erreicht.
