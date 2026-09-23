# Protokoll: Die Gegenzeichnung – eine Rollenfrage, kein Arbeitsposten

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-23 |
| Release | `0.91.0` |
| Änderungsantrag | `CR-2026-127` (E1 bis E5 entschieden) |
| Art | Governance-Entscheidung, eine neue Prüfung, sieben Gegenzeichnungen – **keine Sitzung, kein Kontingent, kein Modelllauf** |
| Gegenstand | Der letzte offene Posten von `AP11`: die Gegenzeichnung der Protokolle |
| Ergebnis | 🟢 **`AP11` ist abgeschlossen.** **D-319**, **Prüfung 80**, `K-107` neu. 🔴 **Der eigene Vorschlag zu E3 ist im Durchgang gefallen** |

---

## 1. Der Befund, der den Posten getragen hat, war schon gebucht – und unvollständig

`0.89.0` hat die Gegenzeichnung nicht gefahren und den Grund als **Abgrenzung**
aufgeschrieben:

> *„Eine Gegenzeichnung ist die Handlung einer **zweiten Rolle**. Ein Werkzeug, das
> `<TBD: Rolle>` durch einen Rollennamen ersetzt, **fälscht sie**."*

**Das trägt.** Was dort fehlte, ist die Folge: **An diesem Framework arbeitet eine
Person.** Es gibt keine zweite Rolle, und damit war die Pflicht in ihrer damaligen Form
**nicht erfüllbar** – nicht aus Nachlässigkeit, sondern konstruktiv.

➡️ ***Eine Pflicht, die niemand erfüllen kann, ist ein Befund über ihre Formulierung.***
🔴 **Das ist die Bauform *die Regel mit leerer Schnittmenge*** (D-189, `K-72`) – bisher
an einer Testzelle gemessen, hier **an einer Governance-Regel**.

## 2. Der Zuschnitt ist gemessen, nicht gewählt

**Nicht jedes Protokoll ist eine Abnahme.** Von 125 sind die meisten Arbeits- und
Meßprotokolle, die ihren Beleg in sich tragen. Eine Gegenzeichnung sagt etwas anderes:
*Eine zweite Person hat geprüft und steht dafür ein.*

| Menge | Zählregel A (nur Überschrift) | Zählregel B (auch Tabellenzeile) |
|---|---|---|
| **Gesamtbestand** | 13 / 45 / 64 von **122** (Stand `0.89.0`) | 17 / 47 / 61 von **125** (Stand `0.91.0`) |
| **die zehn Abnahmeprotokolle** | **3 / 2 / 5** | **3 / 2 / 5** |

➡️ ***Ein Gegenstand, der unter zwei Zählregeln derselbe ist, ist der richtige
Gegenstand.*** Der Gesamtbestand ist es nicht: Er gibt zwei Zahlen, und keine davon ist
nachprüfbar falsch.

## 3. 🔴 Der eigene Vorschlag zu E3 ist im Durchgang gefallen

`CR-2026-127` E3 schlug vor, die offenen `<TBD>` **zu entfernen**, wo der Abschnitt nach
der Abgrenzung entfällt. **Beim Hinsehen kippt das.**

| Befund | Folge |
|---|---|
| Es sind **45** Träger, nicht wenige | ein Sweep, keine Handreichung |
| Sie stehen in **drei verschiedenen Tabellenformen** | eine einzelne Metadatenzeile, ein Abschnitt mit voll-`<TBD>`-Zeile, ein Abschnitt mit `<TBD: Rolle>`/`<TBD: Datum>` |
| Protokolle sind **Chronik** (D-273) | *„die Chronik beschreibt einen vergangenen Zustand und wandert nicht mit"* |

🔴 **Und das `<TBD>` ist dort inhaltlich richtig:** Es hält fest, daß zu jenem Zeitpunkt
eine Gegenzeichnung **vorgesehen und nicht erfolgt** war. ➡️ *Wer eine Aufzeichnung
nachträglich glattzieht, verliert genau die Angabe, die sie trägt.*

🟢 **Auflösung:** Die Abgrenzung steht **einmal** an den drei Stellen, an denen sie gilt –
`checklists/11-framework-release.md`, `tests/protocols/README.md`, `governance/RACI.md` –
und **nicht fünfundvierzigmal in den Aufzeichnungen.**

## 4. 🆕 Die Frage, die erst beim Vorbereiten entstand: Was **ist** die Unterschrift?

Sie stand in keinem Abschnitt des Antrags und ist die wichtigste: **Wenn ein Werkzeug die
Zeile schreibt – was macht sie dann zu einer Unterschrift?**

🔴 **Eine Fehleinschätzung war dabei zu berichtigen.** Die Vorbereitung hatte zunächst
gesagt, ein Werkzeug *könne* den Commit nicht setzen. **Es kann.** Git ist auf diesem
Arbeitsplatz mit der Identität des Owners konfiguriert, und alle Commits der beiden
vorangegangenen Releases sind so entstanden. **Genau deshalb darf es den Commit für die
Gegenzeichnung nicht setzen** – die Fälschung wanderte sonst nur aus der Markdown-Zeile in
die Commit-Metadaten.

🟢 **Die Auflösung (D-319, E5):**

| Träger | Aussage |
|---|---|
| die **Zeile** im Protokoll | **WAS** gegengezeichnet wurde: Rolle, Datum, Umfang |
| der **Commit** | **WER** – die Identität des Owners, gesetzt von ihm |

➡️ *Damit wird die Fälschung **unmöglich** statt nur verboten.* Ein Werkzeug kann den Text
hinlegen; den Akt kann es nicht vollziehen.

⚠️ **Preis, benannt und gemessen:** Die Commits dieses Repositoriums sind **nicht
signiert** (`%G?` liefert `N` für jeden). Die Unterschrift ist damit so stark wie der
Schreibzugriff. `K-107` führt die Frage auf ein signiertes Tag für `1.0.0` weiter.

## 5. Was gezeichnet wurde

| Protokoll | vorher | jetzt |
|---|---|---|
| `2026-09-18-FW-AK-01.md` | `<TBD: Rolle>` / `<TBD: Datum>` | gezeichnet |
| `2026-09-18-FW-KO-05.md` | drei `<TBD>` in einer Zeile | gezeichnet |
| `2026-09-10-FW-DS-03.md` | **kein Abschnitt** | Abschnitt angelegt, gezeichnet |
| `2026-09-10-FW-KO-01.md` | **kein Abschnitt** | Abschnitt angelegt, gezeichnet |
| `2026-09-10-FW-KO-04.md` | **kein Abschnitt** | Abschnitt angelegt, gezeichnet |
| `2026-09-10-FW-RE-02.md` | **kein Abschnitt** | Abschnitt angelegt, gezeichnet |
| `2026-09-10-FW-ZA-05.md` | **kein Abschnitt** | Abschnitt angelegt, gezeichnet |

**Die drei übrigen** – `FW-KO-02`, `FW-VN-01` und dessen Wiederholung – trugen ihre
Gegenzeichnung schon und sind **unberührt**.

⚠️ **Der Umfang steht so da, wie der Owner ihn genannt hat:** *„Protokoll vollständig
gelesen"*. **Keine Silbe mehr.** Eine Vorbereitung, die dem Gegenzeichner Prüfungen
zuschreibt, die er nicht genannt hat, ist dieselbe Fälschung mit besseren Manieren.

## 6. Prüfung 80 – und sie war beim ersten Lauf rot über genau die sieben

**Fünf Einheiten, und die letzte trägt die Entscheidung:**

| Einheit | Gegenstand | Ergebnis |
|---|---|---|
| Sonde `80a` | einem Abnahmeprotokoll fehlt der Abschnitt | 🟢 mit Dateinamen gemeldet |
| Sonde `80b` | ein offenes `<TBD>` im Abschnitt | 🟢 gemeldet |
| Sonde `80c` | kein Träger paßt mehr auf das Namensmuster | 🟢 verlorener Anker gemeldet |
| Gegenprobe `80a` | ausgelieferter Bestand | 🟢 läuft durch |
| Gegenprobe `80b` | ein offenes `<TBD>` in einem **Arbeitsprotokoll** | 🟢 **bleibt unbeanstandet** |

🔴 **Gegenprobe `80b` ist die, die man weglassen würde, und sie trägt den ganzen
Zuschnitt.** Ohne sie wäre D-319 eine Behauptung im Kopfkommentar statt eine gemessene
Eigenschaft – und die Prüfung verlangte still die Gegenzeichnung von 125 Protokollen
statt von zehn.

🔴 **Jede Sonde prüft ihre eigene Fundstelle.** Der Bestand trägt sieben frisch
gezeichnete Protokolle; eine Sonde, die nur auf den Meldungstext prüft, bestünde **auch
ohne Präparation**. Der Erwartungstext nennt deshalb den **Dateinamen** des Opfers –
dieselbe Bauform wie Sonde `75a`.

## 7. Der Durchgang vor dem Commit – zum sechsunddreißigsten Mal in Folge

| Zahl oder Aussage | zuerst genannt | nachgezählt |
|---|---|---|
| E3: die offenen `<TBD>` | „entfernen" (eigener Vorschlag) | 🔴 **stehenlassen** – 45 Träger, drei Tabellenformen, Chronik (D-273) |
| *„ein Werkzeug kann den Commit nicht setzen"* | in der Vorbereitung behauptet | 🔴 **falsch** – es kann, und genau deshalb darf es nicht |
| Protokolle gesamt | „122" (Stand `0.89.0`) | ⚠️ **125**, und die Zahl hängt an der Zählregel |
| offene Gegenzeichnungen gesamt | 13 / 45 / 64 | ⚠️ **17 / 47 / 61** unter der zweiten Regel – *zwei Regeln, zwei Zahlen* |
| die zehn Abnahmeprotokolle | 3 / 2 / 5 | 🟢 **3 / 2 / 5** unter **beiden** Regeln |
| Prüfungen | – | 🟢 **80** |

> 🔴 **Zwei der sechs Zeilen sind eigene Aussagen dieser Vorbereitung**, und beide sind
> gefallen: der Vorschlag zu E3 und der Satz über den Commit. *Auch eine Aussage, die man
> eine Stunde vorher selbst geschrieben hat, gehört an ihrem Gegenstand nachgesehen.*

## 8. Abnahme

| Schritt | Ergebnis |
|---|---|
| `assemble.py` (`devin-desktop`) | 🟢 1.975.665 Zeichen, 12.902 Zeilen |
| `build-docx.py` (`devin-desktop`) | 🟢 `Koolie_v0.91.0_devin-desktop.docx`, 1.979.134 Bytes, **8 Diagramme** |
| `assemble.py --client claude-code` | 🟢 1.979.336 Zeichen, 12.820 Zeilen |
| `build-docx.py` (`claude-code`) | 🟢 `Koolie_v0.91.0_claude-code.docx`, 1.980.448 Bytes, **8 Diagramme** |
| `validate-framework.py --root .` | 🟢 **0 Fehler, 0 Warnungen** |
| `probe-pruefungen.py .` **ohne** `PYTHONIOENCODING` | 🟢 **Exit 0** – **441 Einheiten** (264 Sonden, 154 Gegenproben, 23 Selbstproben), 3.856,4 s in **486,3 s** Wanduhr |
| `probe-pruefungen.py .` **mit** `PYTHONIOENCODING=utf-8` | 🟢 **Exit 0**, dieselben 441 Einheiten, 3.686,9 s in **461,0 s** Wanduhr |
| Zeilengleicher Vergleich nach D-49 | 🟢 **0 Unterschiede in 473 Zeilen** oberhalb der Trennlinie |
| Zählung der Einheiten | 🔴 **Nachgezählt:** 264 + 154 + 23 = **441**. `0.90.0` meldete 436; die fünf neuen sind die Sonden `80a` bis `80c` und die Gegenproben `80a` und `80b` |

🔴 **Prüfung 80 war vor der Gegenzeichnung rot – über genau die sieben Protokolle.** Der
grüne Lauf hier ist deshalb kein Formalismus: *Die Abnahme konnte erst gelingen, nachdem
ein Mensch gezeichnet hat.*

**Drei Durchgänge.**

| Durchgang | Baum | Ergebnis |
|---|---|---|
| 1 | Teillauf `--nur 80`, vor dem vollen Apparat | 🟢 alle fünf Einheiten bestanden |
| 2 | voller Lauf, beide Umgebungen | 🟢 **473 Zeilen, 0 Unterschiede**, 441 Einheiten |
| 3 | **Abnahmelauf**, nach dem Eintrag dieses Abschnitts | 🟢 Exit 0 in beiden Umgebungen, **473 Zeilen, 0 Unterschiede**, 441 Einheiten – und **zeilengleich zum zweiten Durchgang**. 🟢 *Das belegt, was es belegen soll:* Der Eintrag dieses Abschnitts ist Prosa in einem Träger, auf den keine Sonde zugreift – und die Ausgabe ist Zeile für Zeile dieselbe |
| 4 | **Bestätigungslauf**, nach der Berichtigung der Zeilenenden | 🟢 Exit 0 in beiden Umgebungen, **473 Zeilen, 0 Unterschiede**, 441 Einheiten – und **zeilengleich zum dritten Durchgang**. 🔴 **Anlaß:** Der Eintrag der Abnahme hat **28 reine LF-Zeilenenden** in einen CRLF-Bestand geschleppt. **Keine Prüfung erfaßt das** – gefunden hat es der nächste Suchtext, der deshalb nicht mehr traf. *Ein Sondenlauf mißt den Baum, in dem er startet*, also wurde er neu gefahren |
⚠️ **Nach der Zeile über Durchgang 4 ist nicht erneut gefahren worden.** Belegt ist die Zeilengleichheit durch die Durchgänge 2 → 3 und 3 → 4, zwischen denen ebenfalls nur Prosa in genau diesem Träger stand – auf den keine Sonde zugreift. *Eine Abnahmetabelle, die einen Lauf behauptet, den es nicht gab, ist derselbe Befundtyp wie die Zusage über einen Vorgang, den niemand ausgeführt hat* (D-309).


⚠️ **Die Laufzeiten sind nach dem Lauf eingetragen** und stehen unterhalb der Trennlinie –
nach D-94 nicht Teil des zeilengleichen Vergleichs.

---

## 9. Was **nicht** gefahren wurde, mit gemessenem Grund

| Posten | Warum nicht |
|---|---|
| **Signatur der Commits** | `K-107`. Sie ist kein Posten dieses Releases, sondern eine Entscheidung über das Verfahren – und sie berührt die Veröffentlichung (Klarnamen in 109 Releases Historie) |
| **`K-100`** | unverändert offen und teurer als gebucht: Ohne Statusvokabular bleibt die Zahl der offenen Klärungspunkte auch nach der Verschiebung unzählbar |
| **Die drei übrigen menschlichen Prüfpunkte von `FW-CL-11`** | manuelle Stichprobe, Aktualitätsprüfung gegen die Clientdokumentation, dokumentierte Freigabe. Sie gehören in den Freigabelauf `AP12` und stehen im Vorbereitungsprotokoll vom selben Tag |

## 10. Gegenzeichnung

Rollen statt Personen (`framework/runtime/rules/20-project-overlay.md`).

| Rolle | Datum | Umfang |
|---|---|---|
| Durchführung (KI-gestützt, Sitzung) | 2026-09-23 | Vorbereitung, Prüfung 80, sieben Abschnitte |
| Gegenzeichnung: `<FRAMEWORK_OWNER>` | 2026-09-23 | Protokoll vollständig gelesen |

🔴 **Selbstgegenzeichnung: keine zweite Rolle vorhanden** (D-319). *Die Zeile sagt, WAS
gegengezeichnet wurde; der Commit sagt, WER.*
