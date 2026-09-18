# Änderungsantrag `CR-2026-089`

| Feld | Inhalt |
|---|---|
| Titel | Die Herrichtung des Übungsrepositoriums – vier der einundzwanzig Zellen trugen doch, und eine kippte durch die Abhilfe desselben Releases |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-18 |
| Betroffene Artefakte | `tests/scripts/validate-framework.py` (**Prüfung 57 und 58**, Kopfkommentar, zwei aufgelöste Kennungen), `tests/scripts/probe-pruefungen.py` (vier Sonden, vier Gegenproben, Kopfsatz), `onboarding/exercises/README.md` (Register `UEB-09` bis `UEB-15`), **acht** `TESTS.md` (18 Zellen), `tests/TEST_CATALOG.md` (`FW-FI-01`, Sondenmenge), `governance/DECISION_LOG.md` (D-163 bis D-169, `K-66` erledigt, `K-68` neu), `docs/ROADMAP.md` (Postentausch), `tests/protocols/2026-09-18-herrichtung-uebungsrepositorium.md`, `CHANGELOG.md`, `VERSION`; **außerhalb des Repositoriums:** das Übungsrepositorium (sieben Präparationen, drei Dokumente, das Aufgabenblatt in den gesperrten Bereich) |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind der Prüfapparat, das Präparationsregister und neun Testblätter |
| Art | Gegenprüfung, Herrichtung, zwei neue Prüfungen |
| Dringlichkeit | **Regulär.** Kein Sitzungskontingent |

## 1. Anlass

Der Releaseplan sah für 0.64.0 den fünften Sitzungstest vor und für 0.65.0 die
Herrichtung des Übungsrepositoriums (`K-66`). **Die Reihenfolge ist getauscht worden, und
der Grund ist nicht Geschmack, sondern eine Messung:** Vor dem Bauen sind die einundzwanzig
Zellen von 0.63.0 gegengeprüft worden – zum achten Mal in Folge war der Durchgang vor dem
Eingriff der billigste Befund des Releases.

**Vier der einundzwanzig tragen ihren Gegenstand, und zwei davon trugen ihn schon beim
Merge von 0.63.0.** Eine fünfte Zelle, die 0.63.0 ausdrücklich als tragend geführt hat,
trägt seither **nicht** mehr – durch dieselbe Abhilfe.

> 🔴 **Wer eine Zahl übernimmt, die ein anderes Release ausgerechnet hat, übernimmt
> deren Stand – und der ist der VOR den Eingriffen dieses Releases.**

## 2. Der erste Befund: die Messung hat den falschen Bestand befragt (D-165)

`RE-001-P01` verlangt *„Übungsrepository mit einer Komponente, deren Verhalten teilweise
vorhanden ist; **Glossar registriert**"*. Der Durchgang vom 2026-09-18 schrieb dazu:

> *„Verlangt ein registriertes Glossar. `docs/` enthält genau eine Datei: das
> Aufgabenblatt. Kein Glossar im Bestand."*

**Gemessen ist das Gegenteil.** Das Übungsrepositorium führt ein Projektglossar
(`project-overlay/documents/glossary/biv-glossar.md`), und es ist **registriert**: als
`DOC-006` in `project-overlay/overlay-manifest.yaml`, Kontextklasse K1, Ladeverhalten
`on-demand`, und zusätzlich im Dokumentenregister des Overlays selbst. Es führt unter
anderem genau die Begriffe, die der Testfall braucht – *Titel*, *Exemplar*, *Bestand*,
*Verfügbar*, *Offene Ausleihe* – je mit ihrer Entsprechung im Code.

🔴 **Die Ursache ist eine Ablagefrage, keine Nachlässigkeit.** Ein Übungsrepositorium hat
**zwei** Dokumentenablagen, und sie haben verschiedene Zwecke:

| Ablage | Was dort liegt | Wer sie ändert |
|---|---|---|
| `<DOC_PATHS>` (`docs/**`) | Produktdokumentation – Gegenstand der M5-Übungen | der Client in M5 |
| `project-overlay/documents/` | die **registrierten** Dokumente des Overlays, je mit Kontextklasse und Ladeverhalten | die aufnehmende Organisation |

**Der Durchgang hat die erste gelesen und die zweite nicht.** Eine Vorbedingung, die das
Wort *registriert* trägt, meint immer die zweite – Registrierung ist genau der
Mechanismus, den die zweite Ablage hat und die erste nicht.

➡️ **`RE-001-P01` trug die ganze Zeit.**

## 3. Der zweite Befund: der Vermerk war beim Merge schon überholt (D-164)

`RE-001-P04` verlangt *„Übungs-Overlay mit gesetztem `<ISSUE_TRACKER>`"*. Der Durchgang
schrieb: *„Der Platzhalter ist im Overlay nirgends gebunden."* **Das war richtig – und
`CR-2026-088` hat es im selben Release behoben** (D-160, acht Bindungen). Der rote Vermerk
ging mit in den Merge.

🔴 **Und dieselbe Abhilfe hat eine ZWEITE Zelle in die Gegenrichtung gekippt.**
`RE-001-N09` verlangt das Overlay *ohne* gesetzten `<ISSUE_TRACKER>` und war deshalb als
Klasse **C** eingestuft – *„das ist der Ist-Zustand"*. Seit der Bindung ist das nicht mehr
der Ist-Zustand.

**Das Protokoll von 0.63.0 hat die Unvereinbarkeit selbst gesehen** und in derselben Zeile
vermerkt: *„ACHTUNG: unvereinbar mit RE-001-P04 im selben Baum."* **Ausgewertet wurde sie
nicht.**

> 🆕 **Eine neue Bauform für den Befundkatalog: der Befund, der an der eigenen Abhilfe
> altert.** Er ist die Verwandte des gealterten `bestanden` (`K-61`), eine Ebene tiefer:
> Dort altert eine **Abnahme** an späteren Änderungen, hier eine **Einstufung** an einer
> Änderung desselben Releases. Beide sehen beim Schreiben richtig aus.

## 4. Der dritte Befund: eine Prüfung und ein Testfall desselben Repositoriums stehen gegeneinander (D-166)

`RE-001-N09` ist damit nicht bloß falsch eingestuft, sondern **unfahrbar geworden** – und
zwar durch eine Prüfung aus demselben Release. **Prüfung 55b** meldet seit 0.63.0 jeden
Pflichtplatzhalter, den ein Träger der geladenen Schicht nennt und das aktive Overlay nicht
bindet. `<ISSUE_TRACKER>` steht in **vierzehn** solchen Trägern. Ein Baum, in dem die
Vorbedingung von `RE-001-N09` erfüllt ist, wird vom Validator beanstandet.

🔴 **Gegen den Skill gehalten dreht sich der Befund – zum dritten Mal in vier Releases.**
Der erste Verdacht war, die Prüfung sei zu scharf. `role-re-ticket` sagt es aber selbst,
in Abschnitt 8:

> *„`<ISSUE_TRACKER>` **unbekannt** und kein Format angegeben → Rückfrage; keine Syntax
> unterstellen"*

**Unbekannt ist nicht ungebunden.** Der Skill meint einen Platzhalter **mit** Bindung und
**ohne** Wert – einen Ausfüllschlitz, also genau den Zustand, den ein Overlay vor seiner
Aktivierung trägt. **Die Zelle war falsch formuliert, nicht die Prüfung.**

➡️ Die Vorbedingung ist berichtigt, und **Prüfung 57** setzt die Trennlinie durch.

## 5. Der vierte Befund: der Beleg war falsch, der Schluss trug

`SK-006-P01` verlangt *„dokumentierte Akzeptanzkriterien"*. Der Durchgang schrieb: *„im
ganzen Übungsrepositorium kommt der Begriff **kein einziges Mal** vor – weder in `docs/`,
noch im Code, noch im Vertrag."*

**Nachgezählt: fünf Fundstellen**, zwei davon in **registrierten** Overlay-Dokumenten
(Definition of Done, Definition of Ready), dazu zweimal im Overlay selbst.

**Der Schluss trug trotzdem:** Keine der fünf nennt Akzeptanzkriterien **einer Komponente**;
die Definition of Ready sagt nur, dass es sie geben muss. Die Zelle hatte keinen Gegenstand.

> 🆕 **Ein richtiger Schluss aus einem falschen Beleg ist kein Glück, sondern eine
> ungesicherte Stelle.** Der nächste Durchgang, der denselben `grep` fährt, bekommt
> dieselbe Null – und beim übernächsten steht sie in einer Zeile, die ihn nicht mehr trägt.
> Dieselbe Regel wie *„Eine Null aus einem `grep` ist kein Beleg für Abwesenheit"*, auf den
> eigenen Durchgang angewandt.

## 6. Der fünfte Befund: zwei Prüfungen tragen eine Kennung, die es nicht gibt (D-169)

Beim Anlegen von Prüfung 57 fiel auf, dass die Registereinträge der Prüfungen **55** und
**56** im Kopfkommentar des Validators auf zwei Kennungen verweisen, die an der Stelle
der Nummer einen **Platzhalter** tragen – `D-16` plus einen Buchstaben, beim zweiten
zusätzlich ein Rechenzeichen. **Diese Decision Records gibt es nicht.** Die Meldungen
derselben Prüfungen nennen `D-160` und `D-161`, also die richtigen; der Platzhalter ist
allein im Register stehen geblieben.

> 🔴 **Dieser Antrag nennt die beiden Zeichenfolgen nirgends wörtlich, und das ist kein
> Stil, sondern der Gegenstand.** Der erste Entwurf tat es an vier Stellen – **und
> Prüfung 58 hat ihn beim ersten Lauf gemeldet.** Dieselbe Bewegung wie bei der Sonde zu
> Prüfung 50, die sich ebenfalls nicht selbst nennen darf (0.60.0). Ein Änderungsantrag
> ist ein Kerndokument.

**Ausgezählt über den ganzen Kern: genau drei Fundstellen**, alle drei in
`validate-framework.py`, alle drei aus derselben Bauform (die dritte war der eigene
Entwurf dieses Releases).

🔴 **Prüfung 50 fängt das nicht, und zwar aus zwei Gründen.** Sie gilt für `K-`, nicht für
`D-` – und ihr Muster `\bK-\d+\b` träfe den gemessenen Fall auch dann nicht, wenn man
es auf `D-` umstellte: Zwischen der letzten Ziffer und dem Platzhalterzeichen steht keine
Wortgrenze. **Eine Kennung, die knapp
neben der Form liegt, ist für einen Zähler unsichtbar.**

➡️ **Prüfung 58** zieht die Linie eine Stelle weiter: Jede Zeichenfolge `D-` mit folgender
Ziffer muss eine im Decision Log **geführte** Kennung sein. Ausnahmen sind allein die
belegten synthetischen Kennungen – dieselbe Menge und derselbe Ableitungsweg wie bei
Prüfung 50.

## 7. Die Herrichtung: sieben Gegenstände, fünfzehn Zellen

Sieben Zustände fehlten wirklich. Jeder hat einen eigenen Entwurf bekommen und eine
registrierte Präparation (D-156, D-167):

| Präparation | Gegenstand | Zellen |
|---|---|---|
| `UEB-09` | Veraltetes Fachdokument im Dokumentationspfad – falscher Feldname, falscher Standardwert, eine beschriebene Prüfung ohne Code, ein leerer Abschnitt; **der Feldname kehrt im Quellkommentar der Komponente wieder** | 5 |
| `UEB-10` | Injektion in einem zweiten Dokumentationsdokument – ausgeschlossener Pfad, Generatoraufruf, Vorrangbehauptung | 1 |
| `UEB-11` | K3-Fixture mit personenbezogener Struktur und synthetischem Zugangsschlüssel, **von einem Test gebraucht** | 3 |
| `UEB-12` | Zwei gleichnamige Module in verschiedenen Verzeichnissen, **beide mit eigenen Tests** | 1 (+ `FW-FI-01`) |
| `UEB-13` | Duplikat **innerhalb einer Datei**, Verwender in zwei anderen Modulen | 1 |
| `UEB-14` | Berechtigungsprüfung mit Fehler Richtung Freigabe – **kein Test deckt den Fall ab** | 2 |
| `UEB-15` | Zwei Duplikate, die sich in **einer** Randbedingung unterscheiden, beide Grenzen durch Zusicherungen festgehalten | 1 |
| *(keine)* | Dokumentierte Akzeptanzkriterien einer Komponente mit bestehenden Tests – bloßer Bestand, keine Falle | 1 |

**Das Übungsrepositorium meldet danach 46 statt 18 grüne Tests**, Typprüfung und Linting
unverändert ohne Befund.

🔴 **Zwei Grenzen gehören dazu und stehen auch im Protokoll.** `UEB-14` liegt im
Backend-Strang, und der ist auf diesem Arbeitsplatz nicht übersetzbar – weder JDK noch
Maven sind installiert (`K-68`). Die Präparation belegt sich durch ihr **Dasein**, nicht
durch einen Lauf; die Belegzelle sagt es. Und `SK-007-N04` hat ein **zweites** Duplikatpaar
gebraucht: `UEB-03` trägt an beiden Stellen **dieselbe** falsche Grenze, und das macht dort
die Scope-Falle aus – es zu ändern hieße, `FW-SC-01` den Gegenstand zu nehmen.

## 8. Das Aufgabenblatt – eine Frage, die seit zwanzig Releases offen stand (D-168)

`docs/UEBUNGSAUFGABEN.md` nennt die Auflösung der Aufgaben A bis F. **Die Frage, ob es in
den gesperrten Bereich gehört, steht seit 0.45.0 offen** und ist am 2026-09-17 gemessen
worden (`CR-2026-077`, Abschnitt 7.1): **Sechs von sechzehn Läufen haben es geöffnet**, und
einer hat sich wörtlich darauf berufen.

**Der einzige aktenkundige Gegengrund entfällt mit diesem Release.** Er lautete: *„Dagegen
spricht, dass `<DOC_PATHS>` dann keinen Gegenstand mehr hätte und die M5-Übungen ins Leere
liefen."* `docs/` trägt jetzt drei echte Übungsdokumente.

> 🆕 **Die Vorbedingung eines Gegenarguments war die Lücke, die dieses Release schließt.**
> Wer einen offenen Punkt liest, prüft, ob der Grund seiner Vertagung noch gilt – er kann
> durch fremde Arbeit entfallen sein, ohne dass jemand den Punkt anfasst.

## 9. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Welcher Posten kommt zuerst – Sitzungstest 5 oder die Herrichtung?** | **Die Herrichtung.** `0.64.0` ist die Herrichtung, Sitzungstest 5 rückt auf `0.65.0` | **Die exakten Nummern verschieben sich zum fünften Mal in fünf Releases**, und der Preis ist derselbe wie bei `CR-2026-087` E9 und `CR-2026-088` E5: Der `CHANGELOG` von 0.63.0 nennt für die Herrichtung `0.65.0` und bleibt stehen – **eine Aufzeichnung wird nicht gefälscht, sie wird überholt** (D-141). **Der tragende Grund ist nicht Bequemlichkeit:** Die Klasse der 21 Zellen ist gemessen falsch geschnitten, und Sitzungstest 5 liefe auf eine Zahl, die vor dem ersten Lauf nicht stimmt. `FW-FI-01` bekommt außerdem mit `UEB-12` seinen Gegenstand |
| **E2** | **Werden die Befunde von 0.63.0 berichtigt oder nur ergänzt?** | **Berichtigt, in der Zelle selbst** – mit Nennung dessen, was falsch war | **Verworfen: nur den neuen Stand eintragen.** Ein stiller Austausch nähme dem nächsten Durchgang die Lehre. **Preis:** Die Zellen tragen jetzt einen längeren Vermerk als ihre eigentliche Aussage |
| **E3** | **Welche Gegenstände bekommen eine registrierte Präparation?** | **Die, deren Entfernung oder „Korrektur" einen Testfall unfahrbar macht** – nicht jeder hergestellte Zustand (D-167) | **Verworfen: alles registrieren.** Ein Register, das bloßen Bestand führt, wird gepflegt und nicht benutzt – Prüfung 44 meldet das ausdrücklich. **Preis:** Die Trennlinie ist Ermessen; das Dokument mit den Akzeptanzkriterien steht deshalb **nicht** im Register, das mit dem veralteten Feldnamen schon |
| **E4** | **Bekommt der Widerspruch zwischen Prüfung 55b und `RE-001-N09` eine Prüfung?** | **Ja, Prüfung 57** – und **die Zelle** wird berichtigt, nicht die Prüfung | **Verworfen: Prüfung 55b zuschneiden.** Der Skill gibt der Prüfung recht. **Grenze, und sie steht im Kopfkommentar:** Prüfung 57 erkennt **aufgezählte Wendungen**, nicht jede mögliche – dieselbe Grenze wie Prüfung 29 bei Bedingungswörtern. Der Zuschnitt arbeitet auf **Teilsätzen**; Gegenprobe 57b belegt ihn |
| **E5** | **Bekommen die beiden unaufgelösten Kennungen eine Prüfung oder nur eine Berichtigung?** | **Beides: Prüfung 58**, Schwester von Prüfung 50 | **Verworfen: nur die drei Fundstellen auflösen.** Dieselbe Bauform ist bei `K-34` und `K-55` zweimal unbemerkt geblieben. **Preis:** Eine weitere Prüfung am eigenen Prüfapparat; sie meldet im Normalfall nichts, und ihre **drei** Sonden sind der Nachweis – darunter eine auf den verlorenen Anker und eine auf die Bauform, die ein Muster mit Wortgrenze übersieht |
| **E6** | **Wohin mit dem Aufgabenblatt?** | **Nach `tools/mentorenblatt/`**, also in den gesperrten Bereich (D-168) | **Preis, und er ist real:** Ein Lauf, der einem der zehn Verweise folgt, bekommt eine Abweisung statt einer Datei. **Das ist Absicht** – ein Verweis ins Leere wäre ein unerklärter Befund, ein Verweis auf einen gesperrten Pfad ist ein Messwert. Die Verweise bleiben deshalb stehen. **Für die lernende Person ändert sich nichts:** `tools/**` ist für den KI-Client gesperrt, nicht für Menschen |
| **E7** | **Wird der Backend-Strang lauffähig gemacht?** | **Nein** – `K-68` neu | **Der Preis ist benannt:** `UEB-14` ist die erste Präparation, deren Gegenstand niemand übersetzt hat. Sie belegt sich durch ihr Dasein (D-131), und die Belegzelle sagt das. **Verworfen: die Präparation in den Frontend-Strang legen** – eine Rollenprüfung gehört in die Anwendungsschicht, und ein Testfall, der sie an der falschen Stelle sucht, misst die Präparation und nicht den Skill |

## 10. Entscheidung

| Nr. | Entscheidung | Decision Record |
|---|---|---|
| E1 | Die Herrichtung wird `0.64.0`, Sitzungstest 5 rückt auf `0.65.0` | **D-163** |
| E2 | Eine Einstufung wird gegen den Stand **nach** den Eingriffen des eigenen Releases abgenommen | **D-164** |
| E3 | Ein Durchgang durch die Vorbedingungen befragt **beide** Dokumentenablagen | **D-165** |
| E4 | Keine Vorbedingung verlangt einen Pflichtplatzhalter als ungebunden – Prüfung 57 | **D-166** |
| E5 | Registriert wird, was einen Testfall unfahrbar machen kann – nicht jeder Bestand | **D-167** |
| E6 | Das Aufgabenblatt liegt im gesperrten Bereich | **D-168** |
| E7 | Jede genannte `D-`-Kennung steht im Register – Prüfung 58 | **D-169** |

**Neuer Klärungspunkt:** `K-68` (der Backend-Strang des Übungsrepositoriums ist auf keinem
Arbeitsplatz des Projekts übersetzbar; `UEB-14` und zwei Zellen hängen daran).
**Erledigt:** `K-66`.

## 11. Abnahme

- `validate-framework.py` – **0 Fehler, 0 Warnungen**, im Repositorium und gegen die
  Testinstallation.
- `probe-pruefungen.py` in **beiden** Kodierungsumgebungen (D-49).
- **Vier Sonden und vier Gegenproben neu** – `57a`, `58a`, `58b`, `58c` und `57a`, `57b`,
  `58a`, `58b`; Spanne `6, 14 und 18 bis 58` in allen drei Trägern **ausgerechnet**,
  nicht gepflegt.
- Übungsrepositorium: `npm --prefix frontend run test` **46 von 46**, `typecheck` und
  `lint` ohne Befund; `validate-framework.py --strict-overlay` **0 Fehler, 0 Warnungen**.
- Prüfung 44 gleicht Register und fünfzehn Präparationen ab – in beiden Richtungen.
