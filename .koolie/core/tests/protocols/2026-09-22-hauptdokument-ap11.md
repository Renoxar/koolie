# Protokoll: `AP11` – das Hauptdokument gegen den geltenden Stand, und der Erzeuger, der nicht mehr lief

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-22 |
| Release | `0.89.0` |
| Änderungsantrag | `CR-2026-124` |
| Art | Vorbedingungsdurchgang, Werkzeugberichtigung, Textarbeit an 32 Trägern, eine neue Prüfung – **keine Sitzung, kein Kontingent, kein Modelllauf** |
| Gegenstand | Das Hauptdokument (`.koolie/core/build/doc/`, 34 Kapitelquellen) gegen den Stand `0.89.0` setzen; die befristete Neutralitätsausnahme für `build/` auflösen; `K-103` schließen |
| Ergebnis | 🔴 **Der Meßgegenstand ließ sich nicht herstellen: Das Dokument war seit `0.88.0` nicht baubar** (D-309). **Zweiundvierzig Releases Abstand, vierzehn falsche Zahlen, zwei Aufzählungen, die ihre eigene Zahl widerlegen.** 🟢 **Prüfung 77**, `K-103` geschlossen, `K-104` neu, drei Nachbarträger berichtigt |

---

## 1. Der Vorbedingungsdurchgang – zum fünfzehnten Mal in Folge der billigste Befund

**Die erste Frage jedes Vorbedingungsdurchgangs lautet: Ist der Gegenstand da, oder
entsteht er erst?** Hier entsteht er: Das Hauptdokument ist ein **Erzeugnis**, und der
Posten heißt, es gegen den geltenden Stand zu setzen. Also war der erste Handgriff, es zu
bauen.

```text
$ python .koolie/core/build/assemble.py
FEHLER: eingebettete Datei fehlt (Repository): .koolie/core/framework/core/00-principles.md
```

Die Datei ist da. Was fehlt, ist die Wurzel:

```python
CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # richtig
REPO = os.path.dirname(CORE)                                          # zaehlt EINE Ebene
```

**Gemessen:**

| Wert | ergibt |
|---|---|
| `CORE` | `…\koolie\.koolie\core` ✅ |
| `REPO` (bis `0.88.1`) | `…\koolie\.koolie` ❌ |
| Projektwurzel | `…\koolie` |

🔴 **Das ist die Bauform aus D-299 an einer siebten Stelle.** `0.88.0` hat sechs gefunden –
vier über `os.path.basename()`, zwei über gezählte Verzeichnisebenen. Diese hier ist die
zweite Gattung und lag in `build/`, also genau dort, wohin dieser Posten zeigt.

🔴 **Prüfung 76 hat es nicht gemeldet, und das ist ihre Grenze und kein Versehen.** Sie
hält **vier** Werkzeuge gegeneinander: `clientmap.py`, den Validator, den Schutz-Hook und
`ablage.py`. `assemble.py` ist keines davon.
➡️ *Eine Prüfung, die eine abgezählte Menge vergleicht, kann nur so vollständig sein wie
ihre Menge – und die Menge stand fest, bevor jemand den Bau probiert hatte.*

**Behoben mit `clientmap.projektwurzel(CORE)`** – derselben benannten Ableitung, die die
vier Werkzeuge aus D-299 verwenden. Gegengeprüft für **beide** Client Packs:

| Lauf | Ergebnis |
|---|---|
| `assemble.py` (Referenzclient `devin-desktop`) | 🟢 geschrieben, 12.840 Zeilen |
| `assemble.py --client claude-code` | 🟢 geschrieben, 12.758 Zeilen |

⚠️ **Und dabei fiel eine Buchung von `0.88.1`.** Die Übergabe schrieb, die Fundstellen des
alten Namens im Erzeugnis *„löst der nächste Bau"*. **Es gab keinen nächsten Bau** – und
die Fundstellen, die nach der Berichtigung im Erzeugnis bleiben, stammen aus der
**eingebetteten Chronik** (Decision Log, Roadmap) und bleiben dort nach D-273 stehen.
➡️ *Eine Zusage über einen Vorgang, den man nicht ausgeführt hat, ist eine Vermutung mit
Zeitform.*

---

## 2. Der Abstand, als Zahl – vierzehn Angaben nachgezählt

**Keine dieser Zahlen war falsch geschrieben.** Alle waren bei ihrer Einführung richtig und
sind stehen geblieben, während ihr Gegenstand weiterlief.

| Angabe im Dokument | gemessen am 2026-09-22 | wie gemessen |
|---|---|---|
| Dokumentversion `0.9.0`, Stand 2026-09-10 | Release `0.89.0` | `VERSION` |
| *„Alle Module im Status `entwurf`"* | **0** auf `entwurf`; 81 Träger mit Steckbriefzeile, **77 auf `pilot`**, 4 Ausfüllschlitze | Zählbereich von Kriterium 3 (Prüfung 46) nachgefahren |
| *„Kein Mechanismus wurde bislang in einer Zielinstallation ausgeführt"* | `AP2` mit `0.86.0` zu Ende gefahren; **9** Matrixzeilen beobachtet | `clients/devin-desktop/CLIENT_PACK.md` Abschnitt 3 |
| *„Alle dynamischen Tests stehen auf `offen`"* | **0** offen; 38 Katalogzellen + 87 Testblattzellen `bestanden` | Baumdurchlauf über `TEST_CATALOG.md` und alle `TESTS.md` |
| *„26 technische Zusagen"* (4 Fundstellen) | **31** (`claude-code`) und **36** (`devin-desktop`) | Matrixzeilen je Pack ausgezählt |
| *„24 von 34"* / *„25 von 29"* `[TECHNISCH]` | **21 von 36** / **22 von 31** | Zusammenfassung je Pack, von Prüfung 31 nachgerechnet |
| *„8 von 34"* / *„2 von 29"* ohne Beleg | **1 von 36** (dauerhaft) / **0 von 31** | Belegspalte je Pack |
| *„vier Dateien" je Client Pack* (4 Fundstellen) | **3** | `git ls-files .koolie/core/clients/` |
| *„80 / 79 installierte Dateien"* | **78 / 78** | je eine frische Referenzinstallation |
| *„zehn Modulen: FW-CORE-00 … 10"* | **11** | `ls framework/core/` |
| *„233 versionierte Dateien im Kern"* | **502** | `git ls-files` |
| *„33 Kapitelquellen"* | **34** | `ls build/doc/` |
| *„rund 8.700 Zeichen"* (Wurzel-Anweisungsdatei) | **11.887** (`devin-desktop`), 11.894 (`claude-code`) | an der **erzeugten** Datei gezählt |
| *„155 Markdown-Dateien"* (2 Fundstellen) | **450** im Kern | `git ls-files '.koolie/core/*.md'` |
| *„K-01 bis K-20, D-01 bis D-10"* | **K-01 bis K-103**, **D-01 bis D-308** | Register nachgezählt, lückenlos bis auf zwei belegte synthetische Kennungen |

🔴 **Die Zeichenzahl der Wurzel-Anweisungsdatei ist an der ERZEUGTEN Datei gemessen, nicht
an der Quelle.** Die Quelle ist 11.924 Zeichen lang; die Platzhalter werden beim Erzeugen
aufgelöst, und die Länge ändert sich dabei. *Das ist derselbe Fall, den `0.88.0` schon
einmal bezahlt hat, als eine Zahl aus einem Längenunterschied hochgerechnet statt gelesen
wurde.*

---

## 3. Zwei Aufzählungen, die ihre eigene Zahl widerlegen

**Die Bauform ist beide Male dieselbe:** Eine Zahl steht vor einer Aufzählung, die
Aufzählung ändert sich, die Zahl bleibt.

| Satz | Aufzählung daneben | Seit |
|---|---|---|
| *„Ein Client Pack enthält vier Dateien"* | `manifest.json`, `CLIENT_PACK.md`, README der Laufzeitschicht – **drei** | D-36, Release `0.26.0`; die vierte war die README der Regelablage |
| *„Allgemeingültige Regeln in zehn Modulen: FW-CORE-00 …, 01 …, … 10 …"* | elf Module in derselben Zeile | seit der Erstfassung |

🔴 **„vier Dateien" stand an vier Fundstellen** – in Kapitel 7a.4, zweimal in Kapitel 15
(Baum und Fließtext) und im Inventar 31.1. *Wer eine Zahl an vier Stellen führt, hat vier
Gelegenheiten, sie stehen zu lassen.*

---

## 4. Der Baum, der einen Client zeigte und drei überholte Stände führte

Kapitel 15.2 heißt *„Repository-Struktur"*. Gezeigt wurde die Struktur eines einzigen
Client Packs – und in ihr:

| Was der Baum führte | gemessen an einer frischen Installation | überholt seit |
|---|---|---|
| eine eigene Hook-Datei | **wird für kein Pack erzeugt** | D-32, Release `0.25.0`/`0.26.0` |
| eine README in der Regelablage | **nicht vorhanden** | D-36, Release `0.26.0` |
| `.koolie/core/` und `.koolie/project-overlay/` als zwei Wurzeleinträge | **Geschwister unter `.koolie/`** | Release `0.88.0` |
| `skills/ # fw-*, prj-*` | zusätzlich `role-*` und `tech-*` | seit dem zweiten Role Pack |

**Gemessen:**

```text
devin-desktop: 78 Dateien   claude-code: 78 Dateien
<RUNTIME_DIR>/: README.md, agents/, <PERMISSIONS_FILE>, MCP-Vorlage, rules/, skills/
rules/: 00-framework-core.md, 10-privacy-security.md, 15-development-rules.md,
        20-project-overlay.md, 21-overlay-TEMPLATE.md.template, 40-tech-TEMPLATE.md.template
```

🟢 **Der Baum steht jetzt in Platzhaltern** (D-310) und gilt damit für beide Packs; Anhang
31.2 löst jeden auf. Derselbe Baum in der Wurzel-README ebenso.
⚠️ **Preis, ein echter:** Er liest sich abstrakter. *Dafür behauptet er nicht mehr für jede
Installation, was für eine galt.*

---

## 5. Die befristete Ausnahme, die für ihren halben Gegenstand nie ablaufen konnte

Der Releaseplan sagte: *„Hier fällt die einzige befristete Ausnahme von Prüfung 48. Wer
`AP11` fährt, streicht die Ausnahme … und räumt die dann gemeldeten Fundstellen mit auf."*

**Gemessen, indem die Ausnahme probeweise entfernt und der Validator gefahren wurde:**

| Träger | Fundstellen | Gattung |
|---|---|---|
| `31-anhaenge.md` | 24 | Quellenliste **je Client Pack**, Verifikationsbedarf **eines** Packs |
| `32-abschluss.md` | 3 | Chronik; Aussagen des Auftrags **über** die Produktnennung |
| `15-referenzstruktur.md` | 3 | Baum und Fließtext |
| `05-glossar.md` | 3 | Produkteinträge |
| `00-kopf.md`, `04-geltungsbereich.md`, `29-grenzen.md` | je 1 | Produktstand, Zeitdokument |
| **Summe** | **36** | |

🔴 **27 der 36 liegen in zwei Trägern, und für die konnte die Frist nie ablaufen.** Eine
Liste, die **je Client Pack** geführt wird, muß den Client nennen – das ist dieselbe
Gattung, die `NEUTRAL_ABBILDUNG` seit `0.57.1` **dauerhaft** ausnimmt (`clients/`,
`RUNTIME_GLOSSARY.md`, `PLACEHOLDER_REGISTRY.md`).

🔴 **Und es stand längst entschieden.** `CR-2026-025` E3, 2026-09-10:

> *„Die acht Pfadnennungen in `build/doc/` mitlösen? **Nein**, ausgewiesen. Die Anhänge
> beschreiben teils Prüfpunkte gegen die Dokumentation eines konkreten Clients."*

**Die Frist stand zwanzig Releases lang über einer Entscheidung, die sie aufhob.**

🟢 **Auflösung (D-311):** Die Frist fällt, eine **Dauerausnahme über drei benannte Träger**
tritt an ihre Stelle – `29-grenzen.md` (Zeitdokument), `31-anhaenge.md` (Abbildung je
Pack), `32-abschluss.md` (Chronik). Die übrigen **neun** Fundstellen sind aufgelöst; **31**
der 34 Kapitelquellen sind damit werkzeugneutral.

**Gegengeprüft:**

| Lauf | Ergebnis |
|---|---|
| Validator mit der alten Frist entfernt, vor der Arbeit | 36 Fehler |
| Validator mit `NEUTRAL_DOKUMENT`, nach der Arbeit | 🟢 0 Fehler |

⚠️ **Prüfung 63 teilte sich die Menge und hat den Wechsel mitgemacht.** Sie nimmt
Aufzeichnungen von der Nummernverweisprüfung aus und nannte dafür `NEUTRAL_CHRONIK +
NEUTRAL_FRIST`. Mit dem neuen Zuschnitt prüft sie die Nummernverweise der **31** Kapitelquellen
außerhalb der Dauerausnahme **mit** – und läuft dort ohne Befund durch.

---

## 6. Fünf Querverweise auf die Anhänge zeigten auf den falschen Abschnitt

| Träger | stand | richtig | Gegenstand |
|---|---|---|---|
| `00-kopf.md` | Anhang 31.3 | **31.4** | Quellen der Produktdokumentation |
| `00-kopf.md` | Anhang 31.2 | **31.3** | Platzhalterregister |
| `05-glossar.md` | Anhang 31.2 | **31.3** | Platzhalterregister |
| `08-trennung.md` | Anhang 31.2 | **31.3** | Platzhalter-Schnittstellen |
| `29-grenzen.md` | Anhang 31.3 | **31.4** | Quellen der Produktdokumentation |
| `32-abschluss.md` | Anhang 31.4 | **31.5** | konsolidierte Punkte V2–V10 |

🔴 **Nichts hat es gemeldet.** Prüfung 12 liest Pfad-Token in **Backticks** und keine
Abschnittsnummern in Prosa; Prüfung 63 löst Nummernverweise auf, hatte `build/` aber über
dieselbe Frist ausgenommen. *Zwei Prüfungen, und die Lücke lag genau zwischen ihnen.*

⚠️ **Die Ursache ist mechanisch:** `31.3 Platzhalterregister` ist nachträglich eingefügt
worden und hat alles darunter um eine Nummer verschoben. Die Verweise sind nicht
mitgewandert.

---

## 7. Ein Kodierungsrest, dreiundvierzig Releases alt

`29-grenzen.md`, seit dem Release, das dieses Dokument erzeugt hat (`0.9.0`, 2026-09-10):

> *„Regeln in der Wurzel-Anweisungsdatei und der Regelablage `` wirken über das
> Befolgungsverhalten des Modells …"*

**Leere Backticks.** Gemessen mit `git log -S`: die Zeile ist seit `0.9.0` unverändert.
⚠️ **Sie steht in `29.1`, dem ausdrücklichen Zeitdokument** – und ist trotzdem berichtigt
worden: *Ein Defekt der Wiedergabe ist keine historische Aussage.* Der Fließtext des
Abschnitts bleibt im Übrigen unberührt (D-273).

---

## 8. Drei Nachbarfunde, gemeldet **und behoben**

Sie liegen sämtlich in Trägern, die das Hauptdokument **einbettet** – sie wären Teil der
Lieferung geworden.

### 🔴 Der Träger, der sich selbst widerspricht: `docs/RUNTIME_GLOSSARY.md`

| Stelle | Aussage |
|---|---|
| Tabelle, Zeile „Hook-Konfiguration" | *„in der Berechtigungsdatei"* – bei **beiden** Packs (D-32) |
| Absatz acht Zeilen darunter | *„Die Hook-Konfiguration ist bei `devin-desktop` eine eigene Datei"* |

**Der Absatz, der die Tabelle erklärt, widersprach ihr** – seit `0.26.0`. Das Beispiel
steht jetzt auf der **MCP-Konfiguration**, wo der Unterschied zwischen den Packs wirklich
liegt (in der Laufzeitschicht gegen daneben im Wurzelverzeichnis).

### 🔴 Zwei Träger desselben Hauses, zwei Zahlen: `clients/README.md`

| Angabe | README | Pack selbst |
|---|---|---|
| Status `claude-code` | `entwurf` | **`pilot`** |
| gemessene Matrixzeilen | vier (S3, S4, A1, Reichweite von H2) | **sechs** (dazu B6 und, zur Hälfte, B2) |

*Dieselbe Bauform, die `0.88.1` schon einmal bezahlt hat* (die Übersicht sagte „genau
eine", das Pack „5 der 36").

### 🔴 Die Zusage über die eigene Pflege: `docs/ROADMAP.md`

Die Überschrift **„Stand nach Release 0.56.0 (2026-09-18)"** steht unmittelbar über dem
Satz *„Wird mit jedem Release fortgeschrieben."* Gemessen mit
`git log -S "Stand nach Release 0.56.0"`: gesetzt mit `0.56.0`, seither unverändert –
**zweiunddreißig Releases**. Und `29-grenzen.md` schickt seine Leser genau dorthin, um den
aktuellen Stand zu erfahren.

---

## 9. `K-103` geschlossen – und die eigenen Zahlen des Punktes sind gefallen

| Befund von `K-103` | Auflösung |
|---|---|
| *„Status: alle Module `entwurf` (Validierung in Roadmap-AP2)"* | 🟢 berichtigt: *„kein Modulträger auf `entwurf` – 77 von 77 stehen auf `pilot`"* |
| viermal ein Client genannt, dreimal als Handelnder | 🟢 die drei Akteursnennungen heißen **„der KI-Client"**; die vierte – der Kommentar im Baum – ist mit dem Baum auf Platzhalter umgestellt |

🔴 **Nachgezählt, nicht übernommen:** `K-103` nannte *„80 Träger mit Statuszeile, 73 auf
`pilot`"*. Gemessen über den Zählbereich von Kriterium 3 – jede `.md` unter `<CORE_DIR>/`
außer `build/`, `CHANGELOG.md`, `change-requests/` und `protocols/`, erste Statuszeile in
den ersten 60 Zeilen:

| Wert | gemessen |
|---|---|
| Träger mit Steckbriefzeile | **81** |
| davon `pilot` | **77** (76 schlicht, einer mit Verlaufszusatz) |
| davon Ausfüllschlitz einer Vorlage | **4** |
| davon `entwurf` | **0** |

➡️ *Eine Zahl, die einen Befund begründet, gehört an demselben Gegenstand nachgezählt wie
der Befund.* Die `77` stimmt mit der Standzeile der Roadmap überein, die `80` und die `73`
mit nichts.

🆕 **`K-104` tritt an die Stelle der Frage, die `K-103` offen läßt.** `0.88.1` hat eine
Prüfung auf den Inhalt der Wurzel-README abgelehnt, weil sie *„im Framework grün und in
jeder Installation rot"* wäre. **Derselbe Einwand ist bei Prüfung 75 acht Stunden später
mechanisch gelöst worden:** Sie unterscheidet am Vorhandensein von `UEBERGABE.md`, ob sie
im Framework-Repositorium oder in einer Installation läuft (`_p75_verfolgt`,
`eigenes_repo`). Ob dieser Weg für einen kleinen, mechanischen Gegenstand trägt, ist
`K-104`.

---

## 10. Prüfung 77 – und warum ein Prüfkandidat, der zwei Dutzend Releases wartet, eine Entscheidung ist

Der Prüfkandidat *„Ein Zähler für den Abstand des Hauptdokuments"* steht seit `0.53.0` in
Abschnitt 3 der Übergabe, unter *„bewusst **nicht** der nächste Schritt (bewegen keine
Zahl)"*. **In derselben Zeit ist der Abstand auf zweiundvierzig Releases gewachsen.**
➡️ *Ein Kandidat, den man zwei Dutzend Releases nicht anfaßt, ist keine Vertagung, sondern
eine Entscheidung ohne Aufzeichnung.*

**Zwei Gegenstände, und der zweite trägt den ersten:**

| # | Gegenstand | Warum |
|---|---|---|
| 1 | Der Anker: die Zeile `\| Dokumentversion \| X.Y.Z (entspricht Framework-Release X.Y.Z) \|` ist da | Fehlt sie, bestünde die Prüfung **leise** – genau der Zustand, in dem das Dokument zurückgefallen ist (D-23) |
| 2 | Beide Werte der Zeile sind gleich **und** gleich `VERSION` | Eine Zeile, die zwei Stände nennt, läßt offen, welcher gemeint ist; der Vergleich mit `VERSION` wäre sonst erfüllbar, indem **einer** der beiden paßt |

**Gemessen (Teillauf `--nur 77a,77b,77c`):**

| Einheit | Gegenstand | Ergebnis |
|---|---|---|
| Sonde `77a` | Dokumentversion auf `0.9.0` zurückgesetzt | 🟢 gemeldet |
| Sonde `77b` | dieselbe Zeile nennt `0.89.0` und `0.88.1` | 🟢 gemeldet |
| Sonde `77c` | die Versionszeile heißt `\| Fassung \|` | 🟢 verlorener Anker gemeldet |
| Gegenprobe `77a` | der ausgelieferte Bestand | 🟢 läuft durch |

⚠️ **Nicht gegen das Erzeugnis geprüft, sondern gegen die Quelle.**
`build/out/hauptdokument.md` steht in der `.gitignore` und ist in einer frischen
Auscheckung gar nicht da – eine Prüfung dagegen wäre im Framework grün und **in jeder
Installation rot**. Das ist der Konstruktionsfehler, den Prüfung 75 mit `0.88.0` zweimal
bezahlt hat.

⚠️ **Preis, benannt und nicht klein:** Jedes Release faßt diese Zeile an – derselbe Preis,
den Prüfung 67 für die Übergabe verlangt, und dort trägt er seit elf Releases.
⚠️ **Grenze, ebenso benannt:** Sie mißt die **Version**, nicht den **Inhalt**. Wer die
Zeile mitzieht, ohne die Zahlen nachzusehen, läuft durch.

---

## 11. Sieben Anträge mit offenem Abschnitt 6 – der Plan nannte zwei

| Antrag | Entscheidung steht in | Umgesetzt mit |
|---|---|---|
| `CR-2026-020` | D-28 (2026-09-10) | `0.18.0` bis `0.23.0` |
| `CR-2026-021` | D-29 (2026-09-10) | `0.19.0` |
| `CR-2026-023` | D-30 (2026-09-10) | `0.21.0` |
| `CR-2026-025` | `CHANGELOG.md` zu `0.23.0` | `0.23.0` |
| `CR-2026-026` | D-31 (2026-09-11) | `0.24.0` |
| `CR-2026-029` | D-32 (2026-09-11) | `0.25.0` |
| `CR-2026-030` | D-33 (2026-09-11) | `0.25.0` |

🟢 **Nachgetragen, nicht neu entschieden.** Jeder Block trägt darunter einen Satz, der sagt,
daß er ein Nachtrag ist, woher er stammt und wann er geschrieben wurde. *Ein nachgetragener
Abschnitt sieht aus wie ein zeitgleich geschriebener; der Satz darunter ist die einzige
Trennlinie.*

⚠️ **Eine weitere Unterzählung fiel dabei:** `CR-2026-020` legt in Abschnitt 4 **fünf**
Fragen vor; sein Abschnitt 6 sagte *„E1, E2 und E3 einzeln entscheiden"*.

---

## 12. Was **nicht** gefahren wurde, mit gemessenem Grund

| Posten | Warum nicht |
|---|---|
| **Word-Fassung** (`build-docx.py`) | 🔴 `pandoc` und das Mermaid-Kommandozeilenwerkzeug sind auf diesem Arbeitsplatz nicht installiert – `which pandoc` und `which mmdc` am 2026-09-22, beide ohne Treffer. *Eine Word-Fassung, die niemand erzeugt hat, ist kein Lieferbestandteil, sondern eine Zusage.* 🟢 Der Weg dorthin ist mit diesem Release überhaupt erst frei |
| **Gegenzeichnung der Protokolle** | 🔴 Eine Gegenzeichnung ist die Handlung einer **zweiten Rolle**. Ein Werkzeug, das `<TBD: Rolle>` durch einen Rollennamen ersetzt, **fälscht sie**. Keine Abwägung, eine Abgrenzung |
| **`K-100`** (27 Klärungspunkte in der falschen Tabelle) | Eine Verschiebung von 27 Tabellenzeilen; berührt den Gegenstand dieses Postens nicht |

**Die Zahl der offenen Gegenzeichnungen ist trotzdem nachgezählt**, weil der Plan sie nennt.
Zählregel: *ein Abschnitt mit `Gegenzeichnung` in der Überschrift, und der trägt keinen
`<TBD>` mehr.*

| Menge | gegengezeichnet | offener Abschnitt | ohne Abschnitt |
|---|---|---|---|
| alle 122 Protokolle | 13 | 45 | 64 |
| die 10 FW-Testprotokolle | 3 | 2 | 5 |

🔴 **Der Plan nannte *„zwölf offene und fünf fehlende"*.** *„Fünf ganz ohne"* trifft für die
FW-Testprotokolle; *„zwölf mit offenem Abschnitt"* trifft **keine** der beiden
Abgrenzungen.
⚠️ **Die Zahl hängt an der Zählregel, und deshalb steht sie hier mit ihr** – eine erste
Zählung über *„das Wort `Gegenzeichnung` kommt vor"* ergab 59 und 52.

---

## 13. Der Durchgang vor dem Commit – zum vierunddreißigsten Mal in Folge

| Zahl | zuerst genannt | nachgezählt |
|---|---|---|
| Kapitelquellen | „33 Träger" (Übergabe und Inventar) | 🔴 **34** – `07a-abbildungsschicht.md` fällt aus der Nummernfolge |
| Träger auf `pilot` | „80 Träger, 73 auf `pilot`" (`K-103`) | 🔴 **81, 77 und vier Ausfüllschlitze** |
| Anträge mit offenem Abschnitt 6 | „`CR-2026-029` und `-030`" (Releaseplan) | 🔴 **sieben** |
| offene Gegenzeichnungen | „zwölf offene und fünf fehlende" (Releaseplan) | 🔴 **13 / 45 / 64** über alle, **3 / 2 / 5** über die FW-Protokolle – *„zwölf"* trifft keine Abgrenzung |
| Zeichen der Wurzel-Anweisungsdatei | „rund 8.700" (Dokument) | 🔴 **11.887**, an der **erzeugten** Datei; die Quelle ist 11.924 |
| Fundstellen ohne die Frist | – | 🟢 **36**, davon 27 in zwei Trägern – gemessen, indem die Ausnahme probeweise entfernt wurde |
| Prüfungen | – | 🟢 **77** – Register, Sondenmenge und Testkatalog rechnen es aus (Prüfung 40) |
| Einheiten des Sondenlaufs | – | 🟢 **428** (255 + 150 + 23); die Selbstprobe `B1` meldet **311** – ihr Zählbereich sind die Einheiten **mit** Beschreibungssatz |
| geänderte Kapitelquellen | „32 der 34" | 🔴 **15** – die übrigen 19 tragen ihren Inhalt über Einbettungen. *Die 32 war die Verwechslung mit den Trägern außerhalb der Dauerausnahme – und auch die sind **31***, nicht 32 |
| Zeilen des zeilengleichen Vergleichs | „460" | 🔴 **458** – die 460 stammte aus dem Lauf **mit** zwei Abweichungen |

> 🔴 **Zwei der acht Zeilen sind eigene Zahlen dieses Hauses und in diesem Durchgang
> gefallen** – die „33 Kapitelquellen" der Übergabe und die „80 / 73" von `K-103`. *Eine
> Zahl, die man nicht an ihrem Gegenstand nachgesehen hat, ist geraten*, und beide standen
> schon in mehr als einem Träger.

---

## 14. Abnahme

| Schritt | Ergebnis |
|---|---|
| `assemble.py` (`devin-desktop`) | 🟢 **gebaut** – 1.928.254 Zeichen, 12.840 Zeilen |
| `assemble.py --client claude-code` | 🟢 **gebaut** – 1.931.925 Zeichen, 12.758 Zeilen |
| `validate-framework.py --root .` | 🟢 **0 Fehler, 0 Warnungen** |
| `probe-pruefungen.py .` **ohne** `PYTHONIOENCODING` | 🟢 **Exit 0, alle Sonden und Gegenproben bestanden** – **428 Einheiten** (255 Sonden, 150 Gegenproben, 23 Selbstproben), 3.870,3 s Rechenzeit in **488,9 s** Wanduhr auf 8 Bahnen (Faktor 7,9) |
| `probe-pruefungen.py .` **mit** `PYTHONIOENCODING=utf-8` | 🟢 **Exit 0, alle Sonden und Gegenproben bestanden** – dieselben 428 Einheiten, 3.900,1 s in **492,6 s** Wanduhr |
| Zeilengleicher Vergleich nach D-49 | 🟢 **0 Unterschiede in 458 Zeilen** oberhalb der Trennlinie. Die Auswertung darunter trägt Namen und Laufzeiten und ist nicht Teil des Vergleichs (D-94) |
| Zählung der Einheiten | 🔴 **Nachgezählt, nicht übernommen:** 255 + 150 + 23 = **428** – `0.88.1` meldete 424, und die vier neuen sind die Sonden `77a` bis `77c` samt Gegenprobe. ⚠️ **Nicht zu verwechseln mit der Selbstprobe `B1`**, die *„alle 311 Einheiten tragen einen Beschreibungssatz"* meldet: ihr Zählbereich sind die Einheiten **mit** Beschreibungssatz |

🔴 **Der Bau gehört ab jetzt in den Abnahmelauf, und zwar für beide Packs.** Er hat zwei
Releases lang nicht stattgefunden, ohne daß es auffiel – *eine Prüfung bekommt er nicht
(`E2`), also ist die Anweisung alles, was ihn trägt.*

**Sechs Läufe, drei Bäume – und der dritte ist der Abnahmelauf.**

| Durchgang | Baum | Ergebnis |
|---|---|---|
| 1 | vor der Berichtigung zweier Sondenanker | 🔴 **2 Abweichungen** – `31e` und Gegenprobe `31` suchten wörtlich `\| entwurf \| 22 von 31 \|` in `clients/README.md`, und dieser Statuswert ist in diesem Release auf `pilot` berichtigt worden. **460 Zeilen** |
| 2 | nach der Berichtigung | 🟢 Exit 0 in beiden Umgebungen, **458 Zeilen, 0 Unterschiede** |
| 3 | nach dem Eintrag dieses Abschnitts | 🟢 Exit 0 in beiden Umgebungen, **458 Zeilen, 0 Unterschiede** |
| 4 | nach der Berichtigung der Zahl *„32 der 34"* | 🟢 **Abnahmelauf** – Exit 0 in beiden Umgebungen, **458 Zeilen, 0 Unterschiede**, 428 Einheiten, und **zeilengleich zum dritten Durchgang** |

🟢 **Der vierte Durchgang belegt, was er belegen soll:** Die Berichtigungen zwischen
Durchgang 3 und 4 waren Prosa in Trägern, auf die keine Sonde zugreift – und die Ausgabe
ist **Zeile für Zeile dieselbe**. *Das ist der Nachweis und nicht die Annahme.*

🔴 **Die erste Zeilenzahl war meine eigene und ist im Durchgang vor dem Commit gefallen.**
Die **460** stammte aus dem Lauf **mit** den zwei Abweichungen – zwei Meldezeilen mehr.
➡️ *Auch die Zahl eines Laufs gilt für den Lauf, für den sie erhoben wurde.*

🔴 **Und die zwei Abweichungen sind selbst ein Befund:** Zwei Sonden hielten den
**Statuswert** eines Client Packs als wörtlichen Suchtext, obwohl ihr Gegenstand die
**Zahl** daneben ist. Eine Berichtigung an einer Stelle, die die Prüfung gar nicht misst,
hat sie brechen lassen – *und genau dafür sagt der Sondenapparat „Praeparation gebrochen"
statt „bestanden".*

⚠️ **Die Laufzeiten der Abnahmezeilen sind nach dem Lauf eingetragen.** Sie stehen im
Sondenlauf **unterhalb der Trennlinie** und sind nach D-94 nicht Teil des zeilengleichen
Vergleichs – sonst änderte der Eintrag der Laufzeit die Endfassung, die er misst. *Ein
Sondenlauf mißt den Baum, in dem er startet* (die Lehre von `0.86.0`).
