# Wirkungsnachweise Release 0.36.0 – der Unteragent ist erhoben

| Feld | Wert |
|---|---|
| Gegenstand | `CR-2026-058`, D-67 bis D-71: die Reichweite der Werkzeugsperre in den Unteragenten (S3), der Messbeleg für das Profilfeld (A1), die Reichweite des Schutz-Hooks (H2), die Deklaration des Startwerkzeugs (Prüfung 34), der dritte Umschlag in Prüfung 32 und die nachgerechnete Übersicht (Prüfung 31) |
| Datum | 2026-09-13 |
| Vorstand | `961ea6c` (0.35.0) |
| Grundlage der Zusagen | `tests/protocols/2026-09-13-erhebung-unteragent.md`, zwölf Läufe, Clientversion 2.1.270 |
| Ergebnis | **Validator 0 Fehler, 0 Warnungen. `**119 Sonden und Gegenproben bestanden** (84 Sonden, 35 Gegenproben)` – in beiden Kodierungsumgebungen.** Gegen den Vorstand fallen **fünf** Fundstellen |

## 1. Was neu geprüft wird

| Prüfung | Gegenstand | Sonden | Gegenprobe |
|---|---|---|---|
| **34 (neu)** | `agent_start_tools` ist genannt oder seine Abwesenheit erklärt (D-70) | 34a bis 34e | die unveränderten Packs bleiben unbeanstandet – eines nennt, eines erklärt mit offenem Vorbehalt |
| **32 (erweitert)** | fünfter Gegenstand: der Unteragenten-Umschlag ändert die Entscheidung nicht (D-62, `CR-2026-058` E3) | 32g | unverändert |
| **31 (erweitert)** | die `[TECHNISCH]`-Zahl in `clients/README.md` wird aus der Matrix nachgerechnet (D-71) | 31e, 31f | angepasst: sie zieht jetzt **beide** Stellen nach |
| **30 (Datenstand)** | D-67 braucht einen deckenden Grenzfall | G-18 | – |

## 2. Der Gegenbeweis gegen den Vorstand

Der Vorstand wurde frisch ausgecheckt (`git archive 961ea6c`), **mit seinem eigenen
`install.py`** installiert, und erst danach bekam er den neuen Validator. Der Kontrolllauf mit
seinem eigenen Validator meldet **0 Fehler**; mit dem neuen sind es **fünf**:

| Prüfung | Fundstelle | Was sie sagt |
|---|---|---|
| 34 | `clients/claude-code/manifest.json` | Feld `agent_start_tools` fehlt |
| 34 | `clients/devin-desktop/manifest.json` | dasselbe |
| 31 | `clients/README.md`, `claude-code` | „25 von 29" – gezählt 22 von 31 |
| 31 | `clients/README.md`, `devin-desktop` | „24 von 34" – gezählt 20 von 36 |
| 30 | `tests/EDGE_CASES.md` | keine Grenzfallzeile verweist auf D-67 |

**Die beiden Fundstellen der Prüfung 31 sind der Befund dieses Releases**, nicht bloß ein
Anker: Es sind die zwei Zahlen aus Befund 6, und sie standen dort seit zwei beziehungsweise
drei Releases falsch.

### Wo der Gegenbeweis konstruktionsbedingt stumm ist – und warum das richtig so ist

**Der fünfte Gegenstand der Prüfung 32 findet gegen den Vorstand nichts, und das ist kein
Mangel.** Der Schutz-Hook ist mit diesem Release **unverändert**: Er prüft seit 0.34.0
ausschließlich `tool_input` (D-62), und deshalb ändert ein zusätzliches Umschlagfeld seine
Entscheidung schon heute nicht. Die Erweiterung ist eine **Verankerung**, keine Behebung.

Belegen lässt sie sich deshalb nur an einem gebauten Rückfall, und genau das tut Sonde **32g**:
Sie nimmt Aufrufe aus einem Unteragenten von der Prüfung aus – die naheliegende Regression,
„das ist doch schon oben geprüft". **Keine der übrigen sechs Sonden zu 32 sieht das**, weil die
Ausnahme ohne `agent_type` im Umschlag gar nicht greift.

> Das ist die Bauform, die dieses Projekt am 13.09. schon einmal benannt hat: Ein Gegenbeweis
> gegen den Vorstand kann stumm sein, wenn die neue Prüfung eine Struktur misst, die es dort
> nicht gibt. **Wer die Zahl ins Protokoll schreibt, muss beides nennen** – hier: fünf
> Fundstellen, davon **null** aus dem fünften Gegenstand der Prüfung 32.

## 3. Was die Sonden gefangen haben, bevor es ins Release kam

**Die Zellenprüfung des Decision Logs hat beim ersten Lauf sofort gegriffen.** D-69 zitiert den
Matcher `Edit|Write|NotebookEdit`; die beiden Striche hätten die Zeile auf **acht** Zellen
zerrissen. Das Patchskript brach ab, ohne zu schreiben. **Genau dieser Fehler ist mit 0.34.0
viermal entstanden und mit 0.35.0 von Hand berichtigt worden** – gezählt hat ihn bis heute
nichts, und der Prüfvorschlag aus jenem Protokoll ist damit ein zweites Mal bestätigt.

**Prüfung 34 hat ihre eigene Regel korrigiert.** Beim ersten Lauf meldete sie `devin-desktop`
als Fehler: Zeile A1 steht dort auf `[TECHNISCH]`, das Startwerkzeug ist aber nur erklärt. Das
Pack ist an dieser Stelle jedoch **ehrlich** – seine Präambel sagt ausdrücklich, die Spalte
nenne die **vorgesehene** Durchsetzungstiefe, und die Zeile trägt einen offenen VERIFY-Marker
auf genau die Profilwirkung.

> **Die Einstufung allein sagt nicht, ob eine Zusage schon gilt – das sagt der Marker.** Die
> Prüfung verlangt die Nennung seither nur bei A1 **ohne** offenen Vorbehalt. Sonde 34e belegt
> die verschärfte Hälfte: Wird der Marker entfernt, fällt das Pack.

**Und die Gegenprobe zu Prüfung 31 ist an der Erweiterung gefallen**, wie vorgesehen: Sie zog
bis dahin nur die Summe im Pack nach. Seit die Übersicht mitgerechnet wird, muss sie beide
Stellen nachziehen – ohne diese Anpassung hätte sie gemeldet, was sie beweisen soll.

## 4. Sondenlauf

**84 Sonden, 35 Gegenproben, alle bestanden – in beiden Kodierungsumgebungen** (mit und
ohne `PYTHONIOENCODING=utf-8`, Abnahmeauflage seit D-49). Neu sind **acht Sonden** (31e, 31f,
32g, 34a bis 34e) und **eine Gegenprobe** (34); die Gegenprobe zu 31 ist angepasst.

### Der erste Lauf fiel – und zwar genau dort, wo die Übergabe es vorhergesagt hatte

**Die Gegenprobe 30 brach an der neuen Grenzfallzeile, in beiden Umgebungen.** Sie verankert
die Anzahl aus dem Steckbrief **wörtlich** (`17 → 18`), und mit G-18 stimmte das nicht mehr.
Dazu kam die zweite Falle im selben Handgriff: **Ihre synthetische Kennung war `G-18`** – genau
die, die dieses Release wirklich vergibt.

> **Beide Fallen stehen in der Übergabe benannt, und beide sind trotzdem zugeschnappt.** „Eine
> neue Matrixzeile oder ein neuer Grenzfall bricht bestehende Sonden" – zum **dritten Mal in
> Folge**. Und: „Eine synthetische Kennung der Gegenprobe kann mit einer echten neuen
> kollidieren" – hier zum ersten Mal wirklich geschehen.

Berichtigt: Die Kennung ist jetzt `G-99` und kollidiert mit keinem echten Fall. **Die Anzahl
bleibt wörtlich verankert** – ob eine Gegenprobe ihre Summen ableiten soll, ist eine
Ermessensfrage, sie steht seit 0.34.0 offen und ist **hier nicht entschieden worden**. Eine
abgeleitete Summe verdoppelt womöglich nur die Rechenweise der Prüfung, statt sie zu belegen.
Der Grund für die Zurückhaltung ist derselbe wie damals: Das gehört in einen eigenen Antrag,
nicht in einen Nebensatz beim Aufräumen.

### Was die neuen Sonden belegen

| Sonde | Präparation | Was ohne sie durchginge |
|---|---|---|
| **31e** | die überholte Zahl `25 von 29` in der Übersicht wiederherstellen | genau der Stand, der bis 0.35.0 dort stand |
| **31f** | die Zeile eines Packs aus der Übersicht entfernen | ein Pack ohne Eintrag – die Prüfung bestünde sonst leise |
| **32g** | Aufrufe aus einem Unteragenten von der Hookprüfung ausnehmen | **keine der übrigen sechs Sonden zu 32 sieht das**: Ohne `agent_type` im Umschlag greift die Ausnahme gar nicht |
| **34a** | `agent_start_tools` entfernen | ein Kanal ohne Deklaration – der Stand bis 0.35.0 |
| **34b** | leere Liste ohne erklärte Abwesenheit | „unerhoben" und „abwesend" wären nicht mehr zu unterscheiden |
| **34c** | erklärte Abwesenheit ohne Begründung | eine Behauptung statt einer Erklärung |
| **34d** | genannt **und** für abwesend erklärt | zwei Aussagen, eine davon falsch |
| **34e** | den VERIFY-Vorbehalt aus Zeile A1 entfernen | eine Zusage ohne Vorbehalt, deren Werkzeug das Pack nicht nennen kann |

**Die Gegenprobe zu 34 ist die wichtigere Hälfte:** Die unveränderten Packs bleiben
unbeanstandet – eines **nennt** (`claude-code`), eines **erklärt mit offenem Vorbehalt**
(`devin-desktop`). Ohne sie stünde nur fest, dass die Prüfung irgendetwas meldet.

## 5. Was dieses Release nicht belegt

- **Kein Lauf mit dem Schutz-Hook des Frameworks in einer vollständigen Installation.**
  Gemessen ist ein synthetischer Sperr-Hook in der Form, die `clientmap.py` erzeugt.
- **Hintergrund-Unteragenten und zwei Ebenen tief** sind nicht gemessen.
- **Das Zusammenspiel von Profilfeld und Skill-Sperre** ist nicht gemessen: beide einzeln ja,
  welche Liste bei Widerspruch gewinnt, ist offen.
- **`devin-desktop` ist unerhoben.** Die leere Liste sagt das jetzt ausdrücklich – sie ist eine
  Aussage über den Belegstand, nicht über den Client.
- **Prüfung 34 prüft die Deklaration, nicht ihre Richtigkeit.** Ob der genannte Name beim
  Client wirklich sperrt, belegt allein eine Erhebung.
- **Die VERIFY-Zahlen werden weiterhin von nichts nachgerechnet.** Sie sind von Hand berichtigt
  und in der Übersicht gestrichen; ihre Grenze ist zur Hälfte Ermessen (D-71).

## 6. Gegenzeichnung

| Rolle | Name/Kennung | Datum | Ergebnis bestätigt |
|---|---|---|---|
| `<FRAMEWORK_OWNER>` | `<TBD>` | `<TBD>` | `<TBD>` |
