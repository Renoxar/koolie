# Änderungsantrag `CR-2026-033`

| Feld | Inhalt |
|---|---|
| Titel | Im untersagten Modus ist die erste Linie aus – die Matrix stuft B2 bis B8 unbedingt als `[TECHNISCH]` ein |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-11 |
| Betroffene Artefakte | `clients/README.md` (Abschnitt 4, Definition `[TECHNISCH]`), beide `CLIENT_PACK.md` (B-Block), `clients/_template/CLIENT_PACK.md`, `framework/core/03-security.md` (T7) |
| Ebene laut Entscheidungsbaum 6 | Kern – Bedeutung einer Einstufungsklasse; betrifft **beide** Client Packs |
| Art | Behebung von `AP2-DD-12` (Schwere: mittel); Präzisierung der Klasse `[TECHNISCH]` |
| Dringlichkeit | regulär |

## 1. Anlass und Problem

In der AP2-Sitzung las der Agent `.env` mit dem Lesewerkzeug, **obwohl die Berechtigungsdatei
eine Verweigerungsregel für Secret-Pfade führt**. Der Lauf stand im Modus `Bypass`. Die
Team-Dokumentation des Clients sagt, dass allein Regeln der Organisationsebene „cannot be
overridden" – projektweite offenbar schon.

### Was die Matrix zusagt

`clients/README.md` Abschnitt 4 definiert die Klasse:

> `[TECHNISCH]` – Der Client erzwingt die Zusage. **Ein Verstoß ist nicht möglich, unabhängig vom
> Modellverhalten.**

Beide Packs führen B2 bis B8 in dieser Klasse. Der Satz ist **wörtlich nicht widerlegt**: Der
Zugriff geschah nicht am Modell vorbei, sondern weil die Engine in diesem Modus nicht prüft. Aber
er sagt das, was ein Leser mitnimmt, nicht: **`[TECHNISCH]` beschreibt die Unabhängigkeit vom
Modellverhalten, nicht die Unabhängigkeit vom Betriebsmodus.** Die Bedingung steht in keiner
Zeile, in keiner Vorbemerkung und in keinem der beiden Packs.

Damit steht in der Matrix eine Zusage, die in einem bestimmten Betriebszustand nicht gilt – und
der Betriebszustand ist genau der, den D-05 untersagt und den `M2` bei diesem Pack **nicht
technisch sperren kann**.

### Der Befund belegt D-05 und K-05 empirisch

Bis zu dieser Sitzung war „der Modus ohne Rückfragen ist untersagt" eine Anordnung mit
plausibler Begründung. Jetzt ist es eine Messung: **Ohne Admin-Kontrollen gibt es gegen ihn keine
technische Schranke, und mit ihm fällt die gesamte erste Linie.** K-05 ist damit nicht mehr nur
eine Beschaffungsfrage, sondern die Bedingung, unter der sechs Kernzusagen technisch gelten.

Den richtigen Hebel benennt `CR-2026-028` bereits: Nicht der Modus wird gesperrt, seine Wirkung
wird durch Berechtigungen der Organisationsebene begrenzt. Dieser Antrag zieht die Folge für die
**Einstufung** nach; die beiden überschneiden sich nicht.

### Die zweite Linie hat gehalten – und das ist der eigentliche Beleg

Im selben Modus **blockierte der Schutz-Hook `cat .env`** (Zusage H2, Abschnitt 3 des Protokolls).
Erste und zweite Linie fallen also nicht gemeinsam, sondern unter verschiedenen Bedingungen:

| Linie | fällt aus, wenn | hielt in der Sitzung |
|---|---|---|
| Berechtigungsregeln | der Betriebsmodus die Prüfung abschaltet | nein |
| Schutz-Hook | die Hook-Konfiguration nicht gelesen wird (`AP2-DD-10`) oder das Werkzeugverb fehlt (`AP2-DD-11`) | ja, für `exec` |

**Das ist die empirische Rechtfertigung des Hooks überhaupt** – und der Grund, warum
`CR-2026-030` die Lücke beim Leseverb schließen musste: Ohne sie blieb im Bypass-Modus **keine**
Linie stehen, und genau dieser Fall ist beobachtet worden.

## 2. Vorgeschlagene Änderung

1. **Vorbemerkung im B-Block jeder Fähigkeitsmatrix**, Formulierungsvorschlag:

   > `[TECHNISCH]` heißt in diesem Block: Die Engine setzt die Regel durch, **solange der
   > Betriebsmodus die Berechtigungsprüfung nicht abschaltet.** Im Modus ohne Rückfragen, den
   > D-05 untersagt, ist diese Linie aus; dann trägt allein der Schutz-Hook. Beobachtet am
   > 2026-09-11 (`devin-desktop`, Modus `Bypass`): Eine `deny`-Regel auf einen Secret-Pfad griff
   > nicht, der Schutz-Hook griff.

2. **Die Definition in `clients/README.md` Abschnitt 4 wird präzisiert:** „…unabhängig vom
   Modellverhalten. Die Abhängigkeit vom Betriebsmodus weist der B-Block des jeweiligen Packs
   aus."

3. **`framework/core/03-security.md`, T7 („Übermäßige Berechtigungen"):** Die Gegenmaßnahme nennt
   bisher D-05 und Regel 3.1 – beides organisatorisch. Ergänzt wird, was **technisch** trägt,
   wenn T7 eintritt: der Schutz-Hook, seit 0.25.0 auch für lesende Werkzeuge (D-33). Ohne diesen
   Satz nennt der Kern für seine dritte Bedrohung keine technische Gegenmaßnahme, obwohl es eine
   gibt.

4. **Keine neue Prüfung.** Ein Validator sieht den Betriebsmodus einer künftigen Sitzung nicht.
   Prüfbar wäre allein die Anwesenheit der Vorbemerkung – eine Prüfung, die belegt, dass ein Satz
   dasteht. Das ist zu wenig für eine eigene Nummer und wird hier ausdrücklich nicht beantragt
   (siehe E4).

## 3. Was dieser Antrag nicht ändert

- **Die Einstufungen selbst.** B2 bis B8 bleiben `[TECHNISCH]`. In den Modi, die das Framework
  erlaubt, setzt die Engine durch – daran ändert der Befund nichts.
- **D-05.** Die Anordnung gilt unverändert; sie ist durch den Befund gestützt, nicht berührt.
- **M2 und den Mechanismus der Modus-Sperre.** Das ist Gegenstand von `CR-2026-028`.
- **Die Regelmenge.** `permissions.json`, die Secret-Pfade und die Abbildung bleiben unverändert.

## 4. Grenze der Zusage

**Der Hook ist die zweite Linie, nicht die erste – und nur dort, wo er läuft.** Bei
`devin-desktop` tut er das seit 0.25.0; H3 ist weiterhin unbeobachtet, H1 und H2 sind beobachtet.
Fällt die Hook-Konfiguration aus, steht im Bypass-Modus nichts mehr.

**Nicht erhoben ist, ob im Bypass-Modus auch die `ask`-Regeln entfallen.** Nach der
Modusbeschreibung („All tool calls are auto-approved without prompting") ist es zu erwarten,
gemessen ist es nicht.

**Für `claude-code` ist der Fall unerhoben.** Dort ist der Modus technisch sperrbar
(`permissions.disableBypassPermissionsMode`, AP2-CC-05) und in verwalteten Einstellungen
unüberschreibbar – die Lage ist also nicht dieselbe, aber sie ist auch nicht gemessen.

**Ein Nachweis aus einem untersagten Modus belegt keinen erlaubten Betrieb.** Abschnitt 4 des
Protokolls sagt das bereits; dieser Antrag stützt sich ausdrücklich auf einen Lauf, der so nicht
stattfinden dürfte – als Testnachweis zulässig, als Betriebszustand nicht.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Einstufung ändern oder Bedingung ausweisen? | **Ausweisen.** `[TECHNISCH]` ist richtig für den erlaubten Betrieb; eine Herabstufung würde eine Durchsetzung verschweigen, die es gibt | Wer nur die Spalte liest, liest weiterhin „erzwungen". Die Bedingung steht über der Tabelle, nicht in der Zeile |
| E2 | Eigene Matrixspalte „gilt im Modus"? | **Nein.** Sie beträfe acht Zeilen in jedem Pack und trüge in sieben davon denselben Wert | Die Information ist Fließtext und damit leichter zu überlesen als eine Spalte |
| E3 | Definition in `clients/README.md` schärfen? | **Ja.** Sie ist die Stelle, an der die Klasse definiert wird | Alle bestehenden Matrizen erben die Präzisierung, ohne dass jemand sie einzeln geprüft hat: Die Aussage wird richtig, der Belegstand ändert sich nicht |
| E4 | Prüfung aufnehmen? | **Nein**, mit Begründung im Antrag | Die Vorbemerkung kann bei einem neuen Pack fehlen, und nichts meldet es. `clients/README.md` Abschnitt 5 nennt sie als Pflicht – das ist eine Anweisung, keine Prüfung |
| E5 | Den Fall für `claude-code` erheben? | **Ja, als Folgearbeit in AP2** – ein Lauf im Bypass-Modus gegen die isolierte Umgebung, wie WN-5 ihn geführt hat | Ein weiterer Nachweis in einem untersagten Modus. Zulässig nur als Test, und im Protokoll als solcher auszuweisen |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** |
| Datum | 2026-09-11 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | E1 bis E5 wie vorgelegt: Die Einstufungen bleiben `[TECHNISCH]`, die Bedingung kommt als **Vorbemerkung** in den B-Block; keine eigene Matrixspalte; die Klassendefinition in `clients/README.md` wird präzisiert; T7 nennt künftig die technische Gegenmaßnahme; keine neue Prüfung; der Bypass-Lauf für `claude-code` wird als Folgearbeit in AP2 geführt und im Protokoll als Testnachweis ausgewiesen. Ziel-Release 0.26.0 |
