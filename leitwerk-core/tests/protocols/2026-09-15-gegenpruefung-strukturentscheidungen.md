# Gegenprüfung: die neun Strukturentscheidungen D-01 bis D-08 und D-10

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-15 |
| Framework-Version | `0.48.0` (Stand `main`, Commit `4f5dc93`); umgesetzt mit `0.49.0` |
| Gegenstand | Die neun Decision Records D-01 bis D-08 und D-10, sämtlich seit dem 2026-09-01 auf `entschieden (Vorschlag)` |
| Anlass | Arbeitspaket `AP3` der Roadmap (P1), Aktivität *„Beschluss offener Strukturentscheidungen (D-01…D-10 bestätigen)"*; Kriterium 4 von D-11 |
| Antrag | `CR-2026-071`, D-100, D-101 |
| Prüfmethode | Dokumentenanalyse mit **Messung am Bestand**: Je Record wird die Begründung von 2026-09-01 gegen den heutigen Bestand gehalten, und der Beleg ist ein abgezählter oder aus der Datei gelesener Wert, keine Lektüre. Dazu die Auflösung der drei Einwände aus `CR-2026-019` gegen ihren jeweiligen Gegenstand |
| Ausgeführte Befehle | Ein Messskript über `framework/`, `clients/`, `governance/` (Ausgabe in Abschnitt 3 unverändert); `_d11_zaehlen()` aus `tests/scripts/validate-framework.py` direkt aufgerufen; die Zellenzerlegung des Validators über beide Tabellen des Decision Logs |
| Ergebnis | **Alle neun bestätigungsreif.** Bei acht trägt die Begründung von 2026-09-01 unverändert, bei D-08 trägt die Entscheidung auf einem anderen Grund. **Die drei Einwände aus `CR-2026-019` richten sich sämtlich gegen etwas anderes als die Entscheidung, gegen die sie vorgebracht sind** – zwei gegen Bedingungen, die D-11 ausdrücklich ausnimmt |

## 1. Warum diese Gegenprüfung anders fragt als die übrigen

D-23 verlangt die Gegenprüfung **vor** der Umsetzung eines Befundes. Hier ist der
Gegenstand kein Befund, sondern eine **Bestätigung**. Die Frage lautet deshalb nicht
„stimmt der Befund?", sondern:

> **Trägt die Begründung von 2026-09-01 heute noch – und woran ist das gemessen?**

Das ist eine schärfere Frage als „hat jemand widersprochen?". Eine Entscheidung, die
niemand angefochten hat, kann trotzdem auf einer Begründung stehen, die ihren Gegenstand
verloren hat. **Bei einem der neun ist genau das eingetreten** (D-08, Abschnitt 4).

**Was diese Gegenprüfung ausdrücklich nicht behauptet:** dass sich nichts geändert hätte.
Acht der neun sind mit `CR-2026-019` fortgeschrieben worden, weil sie einen Stand
beschrieben, den es nicht mehr gab. Bestätigt wird die **Entscheidung**, nicht der
Wortlaut von damals.

## 2. Der Vorlauf: eine Vorlage, zweiunddreißig Releases unbeantwortet

| Datum | Release | Vorgang |
|---|---|---|
| 2026-09-01 | 0.1.0 | D-01 bis D-10 niedergeschrieben, sämtlich `entschieden (Vorschlag)` |
| 2026-09-10 | 0.16.0 | D-11 setzt Kriterium 4: kein Record mehr auf `entschieden (Vorschlag)` |
| 2026-09-10 | 0.17.0 | `CR-2026-019` schreibt acht der zehn fort und **legt den Statuswechsel je Record vor**. Sieben ohne Einwand, drei mit einem benannten. Die Entscheidung selbst fällt ausdrücklich nicht |
| 2026-09-15 | 0.48.0 | Prüfung 46 zählt Kriterium 4 zum ersten Mal richtig: **9**, nicht 16 |
| 2026-09-15 | 0.49.0 | **dieser Vorgang** |

**Die Vorlage von `CR-2026-019` steht bis heute als offener Haken in dessen Abschnitt 7.**
Zwischen 0.17.0 und 0.48.0 liegen **zweiunddreißig Releases**. In keinem davon ist über
sie entschieden worden – und in jedem einzelnen war der Validator grün.

**Das ist der Befundtyp dieses Repositoriums an einer neuen Stelle.** Sonst ist es *eine
Zusage, die mehr verspricht, als sie leistet*. Hier ist es **eine Bedingung, die mehr
verlangt, als ihr Kriterium fordert** – siehe Abschnitt 5. Eine solche Bedingung hält
genauso zuverlässig auf, wie eine zu schwache Zusage durchlässt, und sie fällt keiner
Prüfung auf, weil ein unbeantworteter Haken in einem abgeschlossenen Antrag kein
Prüfgegenstand ist.

## 3. Die Messung am Bestand (unveränderte Ausgabe)

```
=== D-01: Stufen der Prioritaetshierarchie ===
Stufen: ['1', '2', '3', '4', '5', '6', '7', '8']
org-policies: ['MAPPING_CLASSIFICATION.md', 'README.md']

=== D-02: Client Packs mit manifest.json ===
  _template manifest.json: False
  claude-code manifest.json: True
  devin-desktop manifest.json: True

=== D-03: Skills und ihre Dateien ===
  Skills gesamt: 13, davon genau die vier Dateien: 13

=== D-04: permissions.json ===
  deny: 53
  ask: 5
  allow: 19
  _core_rules_integrity erzeugt in clientmap.py: True
  deny_must_contain im Validator: 3

=== D-05: Agentenprofile ===
  fw-reviewer.md: permissionMode gesetzt: False

=== D-06: Verschaerfungsprinzip ===
  Regel 2.1 vorhanden: True
  Regeln in Abschnitt 2: 6

=== D-07: Kontextklassen ===
  Klassen: ['K0', 'K1', 'K2', 'K3']
  Abschnitt 1.3 restriktivste Auslegung: True
  Regel 2.2.3 'Fehlt eine Einstufung, gilt K3': True
  Abschnitt 1.2 organisationsspezifisch: True

=== D-08: Steckbriefzeilen im Kern ===
  Prüfung 46 zaehlt jetzt: [29, 118, 69, 9]

=== D-10: MCP ===
  Dateien in framework/runtime: ['agents', 'hooks.json', 'mcp-config.example.json',
  'permissions.json', 'root-instruction-local.example.md', 'root-instruction.md', 'rules']
  MCP-Regeln: [('ask', {'tool': 'mcp', 'pattern': '*'})]
```

**Zum letzten Block, weil er der wichtigste ist:** `framework/runtime/` liefert genau
**eine** MCP-Datei aus, und sie heißt `.example.json`. Es gibt keine wirksame
MCP-Konfiguration im Kern, und die einzige MCP-Regel der Berechtigungsdatei steht in
`ask`. Das ist der Mechanismus hinter D-10 – siehe Abschnitt 5.3.

## 4. Urteil je Record

### D-01 – Ebenenmodell

**Begründung 2026-09-01:** *Vorgabe des Auftrags; Ebenen B und E sind für Separation of
Concerns erforderlich.*

**Trägt.** Die Prioritätshierarchie führt genau acht Stufen (gemessen, Abschnitt 3); Ebene
B steht dort als Stufe 2 und hat unter `framework/org-policies/` einen Einbindungspunkt
mit zwei Dateien, Ebene E als Stufe 8. Die Fortschreibung aus `CR-2026-019` – die Zählung
„vier plus zwei" meint die **Regelebenen**, die Hierarchie zählt acht Stufen, weil die
Skills als Ebene 7 dazwischenstehen – beschreibt den Bestand richtig.

**Ehrlich zur Alternative:** „Drei Ebenen ohne Packs" ist durch **zwei** Role Packs
praktisch widerlegt. Von den beiden Packebenen ist damit **eine besetzt**; ein Technology
Pack liegt bisher nur als Vorlage vor. Das ist eine Aktivität von `AP4` (*„erstes
Technology Pack für `<TECH_STACK>` erstellen"*) und keine Frage an das Ebenenmodell: Eine
Ebene, für die es eine Vorlage, eine Rangposition und eine Zuständigkeitsregel gibt, ist
vorgesehen, auch wenn sie noch leer ist.

### D-02 – Lang- und Laufzeitform

**Begründung 2026-09-01:** *Tool Independence und Least Context; die Laufzeitform verweist
auf die Langform.*

**Trägt, und sie ist heute stärker als damals.** 2026-09-01 war die werkzeugneutrale Naht
eine Absicht; D-12 bis D-14 haben sie benannt und **maschinenlesbar** gemacht. Beide
ausgelieferten Client Packs führen ein `manifest.json` (gemessen), aus dem `install.py`
und der Validator die Pfade lesen, statt sie zu verdrahten. Ein Pack ohne Manifest gilt
als nicht installierbar.

### D-03 – Vier-Dateien-Struktur je Skill

**Begründung 2026-09-01:** *Trennung normativ/erläuternd; Least Context (Beispiele werden
nicht bei jedem Aufruf geladen).*

**Trägt, und beide Hälften sind belegt.** Die Struktur: **13 von 13** Skills tragen genau
`SKILL.md`, `EXAMPLES.md`, `TESTS.md`, `CHANGELOG.md` – abgezählt über den Baum, nicht über
eine Liste. Der Least-Context-Teil ist seit dem 2026-09-12 nicht mehr nur Absicht: Damals
führte eine Sitzung von zwölf `fw-`-Skills genau die **drei ohne** `disable-model-invocation`
(`ERH-13`, `tests/protocols/2026-09-12-erhebungen-K28-S5-B9-bypass.md`). Am 2026-09-14 ein
zweites Mal gemessen: **83** Einträge in der Skill-Auflistung, davon **drei** mit dem Präfix
`fw-` (`tests/protocols/2026-09-14-erhebung-skillaufruf.md`). Zusage S4, zweimal belegt.

> Das ist der einzige der neun, dessen Begründung eine **Wirkungsaussage** enthält – und
> sie ist gemessen. Bei den übrigen acht sind die Begründungen Strukturaussagen, die sich
> am Bestand abzählen lassen.

### D-04 – Berechtigungsdatei, restriktiver Standard

**Begründung 2026-09-01:** *Secure by Default.*

**Trägt, und sie ist seit D-18 geprüft statt zugesagt.** `framework/runtime/permissions.json`
führt **53** `deny`-, **5** `ask`- und **19** `allow`-Regeln – das Verhältnis ist die
Entscheidung. Die Kernzusagen werden als `_core_rules_integrity.deny_must_contain` aus
derselben Quelle erzeugt (`clientmap.py`, gemessen) und vom Validator an drei Stellen
gegen sie gehalten. Eine Installation, in der eine Kernregel fehlt, ist rot.

### D-05 – Berechtigungsmodi

**Begründung 2026-09-01:** *Human Accountability, Review before Adoption.*

**Trägt.** Einwand `AP2-CC-12` – Abschnitt 5.1.

### D-06 – Prioritätshierarchie und Verschärfungsprinzip

**Begründung 2026-09-01:** *Auflösung des Zielkonflikts zwischen „Core über Overlay" und
„Overlay definiert projektspezifische Parameter".*

**Trägt.** Das Verschärfungsprinzip ist Regel 2.1 von `PRIORITY_HIERARCHY.md` (gemessen);
Abschnitt 2 führt inzwischen **sechs** ergänzende Regeln, ohne die die Hierarchie
widersprüchlich wäre – die sechste ist mit D-34 dazugekommen, für eine Quelle, die keine
der acht Ebenen führt. Seit D-18 ist das Prinzip an der Stelle, an der die Kernzusagen
hängen, eine **geprüfte Eigenschaft**: Die Semantikabbildung lässt die Installation
scheitern, wenn eine `deny`- oder `ask`-Regel kein Zielwerkzeug hat, und untersagt bei
`allow` jede Verbreiterung.

**Der Zielkonflikt, den die Begründung nennt, ist als Befund 3 in Abschnitt 3 desselben
Moduls ausbuchstabiert** und dort aufgelöst. Die Begründung verweist damit auf einen Text,
den es gibt – das ist bei einer vierzehn Tage alten Begründung nicht selbstverständlich
und bei acht ihrer Geschwister mit `CR-2026-019` nachzuziehen gewesen.

### D-07 – Kontextklassen K0 bis K3

**Begründung 2026-09-01:** *Operationalisierbarkeit statt abstrakter Regeln.*

**Trägt.** Die vier Klassen stehen in `framework/core/02-privacy.md` Abschnitt 2
(gemessen), seit D-24 vollständig auch in der Laufzeitschicht – eine normative Liste, die
nur in der Langform steht, wirkt nicht. Einwand `K-20` – Abschnitt 5.2.

### D-08 – Framework-Metadaten als Tabelle im Dateikörper

**Begründung 2026-09-01:** *Toleranz unbekannter Frontmatter-Schlüssel nicht belegt.*

**Die Entscheidung trägt. Die Begründung trägt nicht mehr – für einen der beiden Clients.**
Das ist der einzige Sonderfall unter den neun, und er gehört benannt statt geglättet.

| Client | Lage 2026-09-01 | Lage heute |
|---|---|---|
| `claude-code` | Toleranz unbelegt → Vorsichtsannahme | **geklärt** (K-18): Die Herstellerdokumentation zählt die Felder je Artefaktart abschließend auf, und die Abbildung erzeugt seit D-26 und D-27 **nur** dokumentierte Felder. Ein Metadatenfeld im Frontmatter wäre heute kein Risiko, sondern ein **undokumentiertes Feld** – Ballast ohne Durchsetzung |
| `devin-desktop` | Toleranz unbelegt → Vorsichtsannahme | **unverändert unbelegt.** Dort trägt die Begründung von 2026-09-01 weiter |

**Dieselbe Entscheidung, zwei Gründe, je Client ein anderer.** Genau dafür gibt es die
Fähigkeitsmatrix (D-12). Die Form selbst ist durchgehend angewendet: Die Steckbriefzeile
`| Status | … |` steht in **69** Kerndateien – dieselben 69, die Prüfung 46 für Kriterium 3
zählt.

> **Eine Bestätigung ist keine Behauptung, dass sich nichts geändert hat.** Wo die
> Entscheidung heute aus einem anderen Grund trägt, gehört der andere Grund
> hingeschrieben – sonst bestätigt man einen Satz, den niemand mehr glaubt.

### D-10 – Erweiterungsmodule, standardmäßig deaktiviert

**Begründung 2026-09-01:** *K-04 offen; Secure by Default.*

**Trägt.** Einwand `K-04` – Abschnitt 5.3.

## 5. Die drei Einwände aus `CR-2026-019`

`CR-2026-019` hat je Record die Spalte „Einwand gegen eine Bestätigung" geführt und sie als
„den eigentlichen Gegenstand der Vorlage" bezeichnet. Drei Einwände stehen dort. **Alle
drei sind gute Fragen. Keiner von ihnen ist eine Frage nach Kriterium 4.**

### 5.1 `AP2-CC-12` gegen D-05 – Durchsetzungstiefe, nicht Regel

**Der Einwand:** Ob die Sperre gegen den Modus ohne Rückfragen auch für das Feld
`permissionMode` eines Subagentenprofils gilt, ist nicht dokumentiert.

**Zuerst der Stand, und er ist unverändert:** Die Erhebung vom 2026-09-13 über
Unteragenten führt die Frage ausdrücklich unter „Was diese Erhebung nicht belegt" –
*„`permissionMode` im Profil (`AP2-CC-12`, offene Teilfrage zu M2). **Unberührt.**"*
(`tests/protocols/2026-09-13-erhebung-unteragent.md`). Elf Läufe an jenem Tag, und keiner
hat sie berührt. **Sie ist offen und bleibt es.**

**Und sie ist kein Einwand gegen D-05.** D-05 entscheidet, dass der Modus ohne Rückfragen
**untersagt** ist – eine Regel. `AP2-CC-12` fragt, ob ein bestimmter Client dieses Verbot
auf einem bestimmten Weg zusätzlich **technisch** erzwingt. Dass das zwei verschiedene
Dinge sind, ist keine Auslegung, sondern **D-12**: Jede technische Zusage wird je Client
als `[TECHNISCH]`, `[TEXTUELL]` oder `[NICHT ABBILDBAR]` eingestuft, *weil* eine Regel auch
dort gilt, wo die Engine sie nicht erzwingt.

> **Wer eine Regel erst bestätigt, wenn jeder Client sie auf jedem Weg technisch erzwingt,
> hat D-12 abgeschafft** – und mit ihr die Begründung, aus der die Fähigkeitsmatrix
> überhaupt entstanden ist.

**Dazu ein Messwert, der die Reichweite bemisst:** Das Framework liefert **genau ein**
Agentenprofil aus (`framework/runtime/agents/fw-reviewer.md`), und es setzt
`permissionMode` **nicht** (gemessen, Abschnitt 3). Die offene Frage hat in den
ausgelieferten Artefakten keinen Träger.

**Wo sie hingehört:** Die Zeile M2 des Packs `claude-code` führt sie als offene Teilfrage.
Das ist eine Verifikationsschuld – **Kriterium 1 von D-11**, nicht Kriterium 4.

### 5.2 `K-20` gegen D-07 – das Modell regelt das Fehlen selbst

**Der Einwand:** K-20 – Art und Ort der Codebasis-Indexierung – ist bei `devin-desktop`
unbelegt; *das Datenschutzmodell setzt eine Aussage darüber voraus*.

**Der zweite Halbsatz ist falsch, und der Gegenbeweis steht im Modell selbst.**
`framework/core/02-privacy.md` regelt den Fall der fehlenden Aussage ausdrücklich, an zwei
Stellen (beide gemessen, Abschnitt 3):

> **Abschnitt 1.3:** *Bis zum Vorliegen dieser Prüfung gilt die restriktivste Auslegung:
> Nur Kontextklasse K0 und K1 dürfen bereitgestellt werden, und nur, wenn die Organisation
> die Nutzung des Werkzeugs grundsätzlich freigegeben hat.*
>
> **Abschnitt 2.2 Regel 3:** *Fehlt eine Einstufung, gilt K3.*

**Das Modell setzt die Aussage nicht voraus – es enthält die Regel für ihr Fehlen.** Ein
Modell, das seinen eigenen unbeantworteten Eingabewert auffängt, wird durch dessen
Unbeantwortetheit nicht geschwächt; es wird durch sie vorgeführt. Dass K-20 offen ist, ist
ein Argument **für** D-07 und gegen die Alternative „Freitextregeln", die für diesen Fall
gar keine Antwort gehabt hätte.

**Dazu die Zuständigkeit:** Abschnitt 1.2 desselben Moduls erklärt die vertraglichen und
technischen Bedingungen – Auftragsverarbeitung, Verarbeitungsorte, Aufbewahrung,
Training-Opt-out, Zero Data Retention, **Codebasis-Indexierung** – ausdrücklich für
**organisationsspezifisch** und verlangt sie vor der Einführung geprüft und im Overlay
referenziert. **Das ist Aufgabe der aufnehmenden Organisation, und D-11 nimmt genau das
aus.**

**Was von K-20 übrig bleibt, ist ein VERIFY-Marker** in der Zeile X2 des Packs
`devin-desktop` – **Kriterium 1**, nicht Kriterium 4. Ihn zur Bedingung von Kriterium 4 zu
machen, koppelt zwei Kriterien, die D-11 getrennt aufzählt.

### 5.3 `K-04` gegen D-10 – die Zusage hat ein Gegenüber, und es ist ein Mechanismus

**Der Einwand:** K-04 – Nutzungsumfang Cloud/CLI – ist offen und liegt außerhalb des
Frameworks. Solange die Organisation ihn nicht festgelegt hat, ist „vorgesehen,
standardmäßig deaktiviert" *eine Zusage ohne Gegenüber*.

**Erstens die Zuständigkeit.** K-04 nennt als entscheidende Rolle „Projektleitung mit
Informationssicherheit" und trägt den Platzhalter `<TBD: Freigabe Cloud/CLI-Nutzung>`. Das
ist eine **organisatorische Freigabe**, und D-11 sagt dazu einen Satz: *Pilot, Onboarding
und organisatorische Freigabe sind **nicht** Vorbedingung, sondern Aufgabe der
aufnehmenden Organisation.* Ein Einwand, der genau das zur Vorbedingung macht, steht gegen
die Entscheidung, deren Kriterium er bedienen will.

**Zweitens der Mechanismus, und er ist der stärkere Grund.** „Eine Zusage ohne Gegenüber"
trifft seit 0.5.0 nicht mehr zu, und es ist nachzählbar (Abschnitt 3):

- `framework/runtime/` liefert **keine** wirksame MCP-Konfiguration aus, sondern
  ausschließlich `mcp-config.example.json`.
- `permissions.json` stellt **alle** MCP-Werkzeuge in `ask`: `{"tool": "mcp", "pattern": "*"}`.

**Die Deaktivierung ist erzeugt, nicht versprochen.** D-10 ist gerade die Entscheidung,
die das Framework sicher hält, **solange** K-04 offen ist – sie braucht K-04 nicht
beantwortet, sie ist die Antwort auf seine Offenheit. Ein Einwand, der ihre Bestätigung an
K-04 bindet, hat die Richtung der Abhängigkeit umgedreht.

### 5.4 Was die drei gemeinsam haben

| Einwand | Richtet sich gegen | Gehört zu |
|---|---|---|
| `AP2-CC-12` (D-05) | die Durchsetzungstiefe **eines** Clients auf **einem** Weg | Fähigkeitsmatrix (D-12); Kriterium 1 von D-11 |
| `K-20` (D-07) | eine **Eingabe** des Modells, deren Fehlen das Modell selbst regelt | organisatorische Prüfung; Kriterium 1 von D-11 |
| `K-04` (D-10) | eine **organisatorische Freigabe** | aufnehmende Organisation – von D-11 ausdrücklich ausgenommen |

**Alle drei bleiben offen.** Keiner wird durch diese Gegenprüfung beantwortet, und keiner
wird für beantwortet erklärt. Sie behalten ihren Ort und ihre Frist.

## 6. Nebenbefund: die Legende erklärt vier Statuswerte, die Tabellen führen sieben

**Beim Abzählen der Statuszelle angefallen, nicht gesucht.** Die Legende in Zeile 4 von
`DECISION_LOG.md` nennt vier Werte. Abgezählt mit derselben Zellenzerlegung, die der
Validator benutzt (`tabellenzellen()`), über **99** Decision Records und die
Klärungstabelle:

| Statuswert | Vorkommen | In der Legende? |
|---|---|---|
| `entschieden (CR-2026-NNN)` | **89** Decision Records | **nein** |
| `entschieden (Vorschlag)` | 9 Records, 5 Klärungspunkte | ja |
| `ersetzt durch D-11` | 1 (D-09) | **nein** |
| `offen by design` | 1 Klärungspunkt | **nein** |
| `geklärt durch Auftrag` | 1 Klärungspunkt | **nein** |
| `geklärt` / `offen` / `verify` | übrige Klärungspunkte | ja |

**Der meistverwendete Statuswert des Dokuments steht nicht in seiner Legende** – seit D-11
und neunundachtzig Records. Das ist der Befundtyp dieses Repositoriums in seiner
Grundform: ein Verzeichnis, das seinen eigenen Bestand nicht vollständig nennt.

**Berichtigt, nicht geprüft** (`CR-2026-071` E5, D-101). Eine Prüfung, die das Vokabular
der Statuszellen gegen die Legende hält, ist baubar und wäre die richtige Abhilfe; sie ist
hier bewusst nicht gebaut, weil der `<FRAMEWORK_OWNER>` für dieses Release angeordnet hat,
keine neue Prüfung zu bauen, bevor sich eine der vier D-11-Zahlen bewegt. **Sie bewegt
sich mit diesem Release.**

## 7. Was diese Gegenprüfung nicht leistet

- **Sie prüft nicht, ob die Entscheidungen die *besten* wären.** Sie prüft, ob ihre
  Begründung heute trägt. Eine Bestätigung ist keine Neuverhandlung.
- **Sie beantwortet keinen der drei Einwände.** `AP2-CC-12`, `K-20` und `K-04` bleiben
  offen; sie werden nur ihrem richtigen Kriterium zugeordnet.
- **Sie sagt nichts über die vier übrigen Klärungspunkte** auf `entschieden (Vorschlag)`
  (K-12, K-13, K-17, K-18). Bei allen vieren ist ein Teil der Frage unbeantwortet; sie
  gehören in einen eigenen Vorgang (`CR-2026-071` E4).
- **Sie bewegt Kriterium 4 und sonst nichts.** Die Kriterien 1, 2 und 3 bleiben bei 29,
  118 und 69. Eine Zahl von vier ist gefallen; drei stehen.
- **Kriterium 5 bleibt unbeobachtet** – eine Feststellung, keine Zahl, ausdrückliche
  Enthaltung seit `CR-2026-070` E8.

## 8. Nachtrag zum Protokoll von `CR-2026-070`

`2026-09-15-gegenpruefung-d11-zaehlregeln.md` formuliert die Zeile zum seriellen
Abnahmelauf **vorsichtiger, als die Messung es verlangt**: Sie sagt, der Vergleich sei an
einem Zwischenstand gemessen, weil der serielle Lauf gegen den endgültigen Wortlaut bei
Protokollabschluss noch nicht zurück war.

**Er ist inzwischen zurück und grün:** Exit 0, **250 Ergebniszeilen**, sortiert
deckungsgleich mit dem nebenläufigen Lauf; **977 s auf einer Bahn gegen 128 s auf acht**,
Faktor 7,6 – das deckt sich mit den 7,9 aus 0.46.0. Die vierzig Minuten Wanduhr waren
Konkurrenz um die Platte, nicht Rechenzeit.

Das ist **kein Fehler im Protokoll** – es behauptet weniger, als wahr ist – und war kein
eigenes Release wert. Es ist hier nachgetragen, damit die vorsichtige Zeile nicht als
letzter Stand stehen bleibt.

## 9. Bewertung

**Alle neun Records sind bestätigungsreif.** Bei acht trägt die Begründung von 2026-09-01
unverändert; bei D-08 trägt die Entscheidung auf einem anderen Grund, und der Grund ist
benannt. Die drei Einwände aus `CR-2026-019` sind aufgelöst – nicht dadurch, dass ihre
Fragen beantwortet wären, sondern dadurch, dass keiner von ihnen eine Frage nach Kriterium
4 stellt.

> **Die Lehre, die über den Fall hinausgeht:** Dieses Repositorium prüft seit
> dreiundzwanzig Releases, ob seine Zusagen halten. **Es hat nie geprüft, ob seine
> Bedingungen die richtigen sind.** Eine zu schwache Zusage lässt durch und fällt
> irgendwann auf. Eine zu starke Bedingung hält auf – und fällt nie auf, weil ein
> unerfülltes Vorzeichen wie Sorgfalt aussieht.

Umsetzung mit `0.49.0`, Antrag `CR-2026-071`, Decision Records D-100 und D-101.
