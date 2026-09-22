# Änderungsantrag `CR-2026-019`

| Feld | Inhalt |
|---|---|
| Titel | Acht der zehn Strukturentscheidungen beschrieben einen Stand, den es nicht mehr gibt |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | `governance/DECISION_LOG.md` (Abschnitt 2, D-01 bis D-10) |
| Ebene laut Entscheidungsbaum 6 | Governance-Dokumentation; keine Regelebene |
| Art | Fortschreibung; Vorbedingung für Kriterium 4 aus D-11 |
| Dringlichkeit | regulär |

## 1. Anlass und Problem

Kriterium 4 aus D-11 verlangt für Release 1.0.0, dass **kein** Decision Record mehr den Status
`entschieden (Vorschlag)` trägt. Zehn tun es: D-01 bis D-10, sämtlich datiert auf den
**2026-09-01**, den Tag der Erstfassung.

Sie zu bestätigen setzt voraus, dass sie beschreiben, was gilt. Das taten sie nicht. Zwischen
ihrer Niederschrift und heute liegen sechzehn Releases und die Decision Records D-11 bis D-27 –
und die haben acht der zehn an mindestens einer Stelle überholt, ohne dass es jemand vermerkt
hätte. Fortgeschrieben war genau **einer** (D-02, durch `CR-2026-002`); ein weiterer ist ersetzt
(D-09 durch D-11).

Das ist derselbe Befundtyp wie `FW-VN-01` und `CR-2026-018`, eine Ebene höher: **Eine Angabe, die
sich nie bewegt, während sich ihr Gegenstand bewegt, sagt irgendwann nichts mehr.** Bei `FW-VN-01`
waren es Versionsfelder, bei `CR-2026-018` die Quellenliste, hier die Grundentscheidungen selbst.

Die acht Befunde fallen in zwei Gruppen.

**Vier waren überholt – sie nannten Pfade und Produktnamen eines einzelnen Clients:**

| ID | Was dort stand | Seit wann überholt |
|---|---|---|
| D-03 | „Skills liegen unter `.devin/skills/<skill-name>/`" | D-15 (Begriffe statt Pfade), D-16 (eine Quelle, je Client gerendert), D-26 (`triggers` wird abgebildet statt verworfen) |
| D-04 | „Berechtigungen werden versioniert in `.devin/config.json`" | D-15, D-18 (Semantikabbildung, Kernregelintegrität), D-22 (Schreibverbot auf das gesamte Kernverzeichnis), D-26 (Pfadregeln nur für pfadauswertende Werkzeuge) |
| D-05 | „Der Permission-Modus `Bypass` … `Smart` und `Accept Edits` … Standard ist `Normal`" | D-15; zusätzlich seit AP2 technisch sperrbar (AP2-CC-05), mit einer offenen Teilfrage (AP2-CC-12) |
| D-10 | „Devin Cloud, Devin CLI und ACP-Fremdagenten" | D-15, D-19 (der Kern nennt keinen Produktnamen, wo er die Sache meint) |

Das ist bemerkenswert, weil D-15 und D-19 genau das behoben haben – im **Kern**. 61 von 63
Client-Bindungen wurden ersetzt, der Name des Frameworks wurde geändert, 994 Pfadnennungen
angefasst. Das Decision Log lag außerhalb dieses Umfangs, und niemandem fiel auf, dass die
Entscheidungen, die den werkzeugneutralen Kern begründen, selbst client-gebunden formuliert
waren.

**Vier waren richtig, aber unvollständig:**

| ID | Was fehlte |
|---|---|
| D-01 | Die Zählung „vier Ebenen plus zwei Querschnittsebenen" meint die Regelebenen; die Prioritätshierarchie führt acht Stufen, weil zwischen den Packs und der Nutzeranweisung noch die **Skills** stehen |
| D-06 | Das Verschärfungsprinzip ist seit D-18 an der Stelle, an der die Kernzusagen hängen, eine **geprüfte Eigenschaft** und keine Zusage mehr; D-27 zieht das für die Ladebedingung nach und zieht ihre Grenze |
| D-07 | D-24 hat die K3-Definition um die **Auffangkategorie** nachgeschärft und festgelegt, dass eine normative Liste vollständig in der Laufzeitschicht stehen muss |
| D-08 | Die Begründung war eine **Vorsichtsannahme** („Toleranz unbekannter Frontmatter-Schlüssel nicht belegt"). Für `claude-code` ist die Lage inzwischen geklärt und stützt die Entscheidung; für `devin-desktop` bleibt sie unbelegt |

## 2. Vorgeschlagene Änderung

**Jeder der acht Records bekommt eine Fortschreibung im Statusfeld**, nach dem Muster, das D-02
seit `CR-2026-002` verwendet: Der ursprüngliche Wortlaut bleibt unverändert stehen, die
Fortschreibung nennt, was seither gilt und durch welchen Record.

Der ursprüngliche Wortlaut bleibt aus zwei Gründen stehen. Erstens ist ein Decision Log ein
Verlaufsdokument: Wer wissen will, warum eine Entscheidung so getroffen wurde, braucht die
Begründung von damals und nicht die von heute. Zweitens ist der Unterschied selbst die Aussage –
dass D-04 am 2026-09-01 einen Client-Pfad nannte, erklärt, warum es D-15 gebraucht hat.

**Die Statusänderung selbst ist nicht Gegenstand dieses Antrags.** Ob ein Record von
`entschieden (Vorschlag)` auf `entschieden` geht, ist eine Entscheidung des
`<FRAMEWORK_OWNER>` und nicht die Folge einer Textpflege. Abschnitt 4 legt sie je Record vor.

**Was verworfen wurde:**

- **Den Wortlaut korrigieren statt fortzuschreiben.** Dann stünde im Decision Log, D-04 habe am
  2026-09-01 die Semantikabbildung aus D-18 vorgesehen. Das wäre falsch und würde die
  Nachvollziehbarkeit zerstören, für die es das Dokument gibt.
- **Die Records ersetzen, wie D-09 durch D-11 ersetzt wurde.** Angemessen, wenn eine Entscheidung
  *anders* ausfällt – D-09 hatte 1.0.0 an eine Pilotauswertung gebunden, D-11 tut das
  ausdrücklich nicht. Hier fällt keine Entscheidung anders aus; nur ihre Beschreibung ist
  veraltet.
- **Gleich auf `entschieden` setzen.** Die Fortschreibung ist die Vorbedingung, nicht die
  Entscheidung. Ein Record, dessen Status ein Skript ändert, ist kein Governance-Artefakt mehr.
- **Nur D-04 fortschreiben, wie in der Roadmap vorgesehen.** Er war der auffälligste, aber nicht
  der einzige. Sieben weitere in demselben Zustand stehen zu lassen, hieße den Befund zu kennen
  und nur seinen sichtbarsten Teil zu beheben.

## 3. Was dieser Antrag nicht ändert

Keine Entscheidung fällt anders aus. Kein Mechanismus, keine Regel, keine Einstufung ändert sich.
Weder Installation noch Validator noch Laufzeitschicht sind betroffen; es gibt keine Sonde nach
D-23, weil keine Prüfung hinzukommt oder sich ändert.

Zwei Records bleiben unverändert: **D-02** ist seit `CR-2026-002` fortgeschrieben, **D-09** ist
durch D-11 ersetzt und trägt deshalb keinen Vorschlagsstatus mehr.

## 4. Vorlage zur Entscheidung: Statuswechsel je Record

`<FRAMEWORK_OWNER>` entscheidet je Zeile. Die Spalte „Einwand" nennt, was einer Bestätigung
heute entgegenstehen könnte – sie ist der eigentliche Gegenstand der Vorlage.

| ID | Gegenstand | Einwand gegen eine Bestätigung |
|---|---|---|
| D-01 | Ebenenmodell | keiner erkennbar; die Ebenen tragen seit 0.1.0 unverändert |
| D-02 | Lang- und Laufzeitform | keiner erkennbar; fortgeschrieben durch D-12 bis D-14 |
| D-03 | Skill-Struktur | keiner erkennbar; die Vier-Dateien-Struktur ist über zwölf Skills und sechzehn Releases getragen |
| D-04 | Berechtigungsdatei | keiner erkennbar; die Kernzusagen B1 bis B6 hängen daran und sind seit D-18 geprüft statt zugesagt |
| D-05 | Berechtigungsmodi | **Ja:** Die Ausnahmeregel für den Modus mit automatischer Übernahme ist nie in einem realen Projekt angewandt worden, und AP2-CC-12 ist offen. Eine Bestätigung wäre vertretbar, eine Zurückstellung bis AP2 ebenfalls |
| D-06 | Prioritätshierarchie | keiner erkennbar; seit D-18 und D-27 in ihrem tragenden Teil geprüft |
| D-07 | Kontextklassen | **Ja, geringfügig:** K-20 (Codebasis-Indexierung) ist bei `devin-desktop` unbelegt; das Datenschutzmodell setzt eine Aussage darüber voraus. Bei `claude-code` ist die Abwesenheit belegt (X2) |
| D-08 | Metadaten im Dateikörper | keiner erkennbar; für einen Client belegt, für den anderen weiterhin die sichere Annahme |
| D-09 | Versionierung | entfällt – ersetzt durch D-11 |
| D-10 | Erweiterungsmodule | **Ja:** K-04 (Nutzungsumfang Cloud/CLI) ist offen und liegt außerhalb des Frameworks. Solange die Organisation ihn nicht festgelegt hat, ist „vorgesehen, standardmäßig deaktiviert" eine Zusage ohne Gegenüber |

Drei Records tragen damit einen benannten Einwand (D-05, D-07, D-10), sieben keinen. Kriterium 4
aus D-11 ist erreichbar, sobald über diese drei entschieden ist – durch Bestätigung oder durch
eine ausdrückliche Zurückstellung mit Bedingung.

## 5. Prüffragen (durch Owner auszufüllen)

- [x] Richtige Ebene nach Entscheidungsbaum 6? — Ja. Geändert wird ein Governance-Dokument. Keine Regel wird eingeführt, keine gelockert.
- [x] Verschärfungsprinzip eingehalten? — Nicht berührt; keine Regel ändert sich.
- [x] Widerspruchsfreiheit geprüft? — Der Widerspruch war der Anlass: Acht Records beschrieben einen Stand, den spätere Records ersetzt hatten. Nach der Fortschreibung nennt jeder Record den späteren, der ihn überholt.
- [x] Laufzeitfassungen betroffen? — Nein.
- [x] Belegstatus korrekt? — Jede Fortschreibung nennt den Record, aus dem sie folgt. Die einzige Aussage über einen Client stützt sich auf AP2 (D-05, D-08).
- [x] Test- und Validierungsbedarf? — Keine Sonde; die Änderung fügt keine Prüfung hinzu und ändert keine. Validator und `install.py --check` laufen unverändert.
- [x] Auswirkungen auf Overlays und laufende Onboardings? — Keine.
- [x] Dokumentation? — CHANGELOG, Roadmap, Decision Log.

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | angenommen |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Ein Decision Log, dessen älteste Einträge einen Stand von vor sechzehn Releases beschreiben, ist keine Entscheidungsgrundlage, sondern ein Archiv, das sich für eine hält. Dass ausgerechnet die vier Records, die den werkzeugneutralen Kern begründen, selbst client-gebunden formuliert waren, ist der Befund – D-15 und D-19 haben den Kern von seinen Client-Bindungen befreit und das Dokument übersehen, das sie angeordnet hat. |
| Ziel-Release | 0.17.0 |
| Decision-Log-Eintrag | keiner – der Antrag schreibt bestehende Records fort und führt keine neue Festlegung ein |

## 7. Umsetzung (nach Annahme)

- [x] D-01, D-03 bis D-08 und D-10 fortgeschrieben; Wortlaut und Begründung von 2026-09-01 unverändert stehen gelassen
- [x] Je Fortschreibung ist der spätere Record genannt, aus dem sie folgt
- [x] Validator 0 Fehler, 0 Warnungen; `install.py --check` unverändert; Hauptdokument baut für beide Packs
- [ ] **Zur Entscheidung offen:** der Statuswechsel je Record (Abschnitt 4). Drei tragen einen benannten Einwand: D-05 (AP2-CC-12 offen), D-07 (K-20 bei `devin-desktop` unbelegt), D-10 (K-04 offen)
- [ ] **Folgearbeit:** Die Klärungspunkte K-04 und K-20 liegen außerhalb des Frameworks beziehungsweise an AP2. Solange sie offen sind, ist ein Statuswechsel bei D-07 und D-10 eine bewusste Entscheidung unter Unsicherheit, keine Formalie
