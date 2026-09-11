# Änderungsantrag `CR-2026-032`

| Feld | Inhalt |
|---|---|
| Titel | Die Skill-Ablage eines anderen Clients füllt Ebene 7 mit modellaufrufbaren Verfahren |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-11 |
| Betroffene Artefakte | `framework/core/08-skill-conventions.md` (0.1.1), beide `CLIENT_PACK.md` (Zeile S4, neuer Abschnitt), `clients/_template/CLIENT_PACK.md`, `governance/DECISION_LOG.md` (Klärungstabelle) |
| Ebene laut Entscheidungsbaum 6 | Kern – Skill-Konventionen und Abbildungsschicht; betrifft **beide** Client Packs |
| Art | Behebung von `AP2-DD-16` (Schwere: mittel); Ausweisung der Reichweite von S4 |
| Dringlichkeit | regulär |
| Abhängigkeit | Baut auf dem Abschnitt „Anweisungsquellen außerhalb des Projekts" aus `CR-2026-031` auf (siehe E2) |

## 1. Anlass und Problem

`devin skills list` führt in der AP2-Sitzung neben den zwölf `fw-*`-Skills des Frameworks
**Dutzende Skills aus `~\.claude\skills\`** – der nutzerglobalen Skill-Ablage eines anderen
Clients. Sämtlich als `[user,model]`, also **vom Modell selbst aufrufbar**.

Daneben steht in derselben Ausgabe der Beleg, dass die Zusage des Frameworks für seine eigene
Ablage hält: **9 der 12 `fw-*`-Skills sind `[user]`** – exakt die Verteilung der Kernquelle. Ohne
`triggers` wäre der Default `["user","model"]`.

**Beides in einer Liste: eine Zusage, die genau so weit reicht wie die Ablage, die das Framework
schreibt – und daneben eine Ablage, die es nicht schreibt.**

### Was daran den Kern betrifft

1. **Ebene 7 ist von außen befüllt.** Die Prioritätshierarchie führt Skills als Ebene 7. Was dort
   aus dem Benutzerprofil hineinkommt, hat keinen Owner im Sinne der `RACI.md`, keine Version,
   keinen Änderungsverlauf und keine Testfälle – alles Dinge, die
   `08-skill-conventions.md` für einen Framework-Skill normativ verlangt (Pflichtfelder 3, 21,
   23). Die Konventionen gelten für die Ablage des Frameworks; die Hierarchieebene gilt für
   beide.

2. **`[user,model]` heißt: ohne menschlichen Anstoß.** S4 sagt zu, dass schreibende Skills nur
   benutzergetriggert sind. Die Zusage ist **nicht verletzt** – ihr Gegenstand sind die Skills
   des Frameworks, und dort hält sie nachweislich. Aber ihr **Zweck** – dass kein Verfahren ohne
   menschlichen Anstoß anläuft – wird in der Sitzung nicht erreicht, weil neben der geregelten
   Ablage eine ungeregelte liegt.

   **S4 verspricht nicht mehr, als es hält. Es hält weniger, als sein Zweck verlangt.** Das ist
   der wiederkehrende Befundtyp dieses Projekts von der anderen Seite gesehen, und er fällt nur
   auf, wenn man die Reichweite einer Zusage neben ihre Wirkung legt.

3. **Regel 2.3 der Hierarchie beruht auf einer Annahme.** „Packs (5, 6) und Skills (7) enthalten
   keine Governance-, Datenschutz- oder Sicherheitsregeln; damit sind Konflikte strukturell
   ausgeschlossen." Strukturell ausgeschlossen sind sie, solange das Framework die Artefakte
   dieser Ebenen schreibt. Für eine fremde Ablage gilt die Annahme nicht – dort kann stehen, was
   will.

### Woher die fremde Ablage kommt

Nicht aus einer Installation dieses Frameworks. `install.py` schreibt Skills ausschließlich in
die **projektbezogene** Ablage des gewählten Packs (`skills_dir` im Manifest, ein relativer
Pfad). Die Dutzende Skills im Benutzerprofil gehören dem **Arbeitsplatz**, nicht einem Projekt.

Bemerkenswert ist die Richtung: Das Framework führt zwei Packs für zwei Clients, und auf einer
Arbeitsstation, auf der beide Clients installiert sind, **liest der eine die nutzerglobale Ablage
des anderen mit**. Der Befund ist damit keine Eigenschaft des Repositoriums, sondern eine der
Arbeitsstation – und das ist genau der Grund, warum ihn kein Validatorlauf erreicht.

## 2. Vorgeschlagene Änderung

1. **Der Abschnitt aus `CR-2026-031` umfasst auch Skills.** „Anweisungsquellen außerhalb des
   Projekts" listet nicht nur Regeltexte, sondern jede Ablage, aus der der Client Anweisungen
   lädt: Regeln, **Skills**, Agentenprofile. Für `devin-desktop` ist der erste Eintrag damit
   belegt: `~\.claude\skills\`, Aufrufbarkeit `[user,model]`, erhoben mit
   `devin skills list --json` am 2026-09-11.

2. **Eine Matrixzeile für die Aufzählbarkeit.** Neue Zeile **S5**: „Die geladenen Skills sind
   vollständig aufzählbar, samt Herkunft und Aufrufbarkeit." Für `devin-desktop`
   **beobachtet** (`devin skills list --json` führt Herkunftspfad und `[user,model]`), für
   `claude-code` bis zur Erhebung mit VERIFY-Marker.

3. **Die Reichweite von S4 wird ausgewiesen, nicht erweitert.** Zusatz in der Belegspalte beider
   Packs und in `08-skill-conventions.md` Abschnitt 7, Formulierungsvorschlag:

   > Die Zusage gilt für die **Skill-Ablage, die das Framework schreibt**. Skills aus Ablagen
   > außerhalb des Repositoriums unterliegen diesen Konventionen nicht; sie sind nach Regel 2.6
   > der Prioritätshierarchie ebenenlos und dürfen den Handlungsspielraum nur einschränken.

4. **Zwei offene Punkte kommen in die Klärungstabelle.**
   - **K-23:** Lässt sich die Mitnutzung einer fremden Skill-Ablage projektseitig abschalten?
     Offen je Pack, VERIFY-Marker. Die Frage ist billig zu beantworten – `devin skills list --json` und
     `devin doctor` sind Diagnosekommandos ohne Agentenlauf.
   - **K-24:** Erzeugt der Aufruf eines Skills Werkzeugaufrufe, die Berechtigungsregeln und
     Schutz-Hook sehen? In AP2 kam kein Skill-Aufruf vor; erhoben sind nur `exec` und `read`.
     **An dieser Frage hängt die Schwere des Befundes.**

5. **Keine eigene Prüfung.** Prüfung 19 aus `CR-2026-031` deckt die Auskunftspflicht mit ab,
   sobald ihre Abschnittsdefinition Skills einschließt. Eine zweite Prüfung würde dieselbe
   Anwesenheit ein zweites Mal belegen und keine Wirkung mehr.

## 3. Was dieser Antrag nicht ändert

- **S4 selbst.** Die Zusage bleibt wörtlich, wie sie ist – sie wird nicht erweitert, sondern in
  ihrer Reichweite beschrieben. Eine Erweiterung wäre eine Zusage über fremde Verzeichnisse, die
  das Framework nicht schreibt und nicht prüfen kann.
- **Die zwölf `fw-*`-Skills**, die `triggers`-Abbildung und die statische Prüfung darauf. Der
  belegte Teil bleibt unberührt.
- **Die Prioritätshierarchie.** Regel 2.6 aus `CR-2026-031` deckt Skills bereits ab; hier kommt
  keine weitere Regel hinzu.
- **Den Arbeitsplatz.** Das Framework stellt keine Anforderung an nutzerglobale Verzeichnisse
  (siehe E4).

## 4. Grenze der Zusage

**Aufzählbarkeit ist keine Kontrolle.** Die Liste zeigt, was lädt. Sie verhindert nichts, und sie
entsteht nur, wenn ein Mensch das Kommando ausführt – im Repositorium beobachtet sie niemand.
Zwischen zwei AP2-Läufen erscheint ein neuer Skill im Benutzerprofil unbemerkt.

**Die zweite Linie steht vermutlich – belegt ist sie nicht.** Was ein fremder Skill tut, muss
durch die Werkzeuge des Clients, und die sind von den Berechtigungsregeln und – seit 0.25.0 auch
für das Leseverb – vom Schutz-Hook abgedeckt. **Ob ein Skill-Aufruf tatsächlich als
Werkzeugaufruf erscheint, ist nicht erhoben** (K-24). Solange das offen ist, ist die Einstufung
„mittel" eine Annahme, keine Messung.

**Nicht erhoben ist auch, ob ein fremder Skill je aufgerufen wurde.** Die Ausgabe zeigt
Verfügbarkeit, nicht Gebrauch.

**Für `claude-code` gilt die Frage spiegelbildlich und ist unbeantwortet.** Ob dieser Client
seinerseits fremde Skill-Ablagen mitliest, hat AP2 am 2026-09-10 nicht erhoben.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | S4 erweitern oder seine Reichweite ausweisen? | **Ausweisen.** Eine Zusage über Verzeichnisse, die das Framework weder schreibt noch prüft, wäre nicht einlösbar | Die Zusage bleibt kleiner, als ihr Zweck verlangt – künftig sichtbar, statt stillschweigend vorausgesetzt |
| E2 | Eigener Abschnitt oder Mitnutzung aus `CR-2026-031`? | **Mitnutzung.** Eine Quelle, eine Auskunftspflicht, eine Prüfung | Abhängigkeit: Wird `CR-2026-031` abgelehnt, trägt dieser Antrag den Abschnitt selbst – dann ohne Prüfung 19 und damit ohne jede Durchsetzung |
| E3 | Neue Matrixzeile S5 oder nur Fließtext in Abschnitt 5? | **Zeile.** Was keine Zeile hat, hat keine Einstufung und keinen Belegstatus | Die Matrix wächst mit R5 aus `CR-2026-031` von 26 auf 28 Zeilen; drei Packs, die Zusammenfassung der Durchsetzungstiefe und das Hauptdokument sind nachzuziehen, und beide Zeilen tragen bei `claude-code` zunächst einen VERIFY-Marker |
| E4 | Darf das Overlay eine leere fremde Skill-Ablage fordern? | **Nein.** Das Framework regelt das Repositorium, nicht die Arbeitsstation. Eine Forderung, die niemand prüfen kann, ist eine Zusage ohne Deckung | Der Weg, die Lücke wirklich zu schließen, bleibt außerhalb des Frameworks – eine Vorgabe auf Ebene 2 (Organisation) oder eine Clienteinstellung, falls K-23 eine hergibt |
| E5 | K-24 (Werkzeugweg eines Skill-Aufrufs) jetzt erheben? | **Ja, als Folgearbeit in AP2** – nicht als Teil dieses Antrags. Eine Sitzung mit Aufzeichnungs-Hook in der Umgebung ohne Regeltexte beantwortet sie | Bis dahin bleibt unbelegt, ob Berechtigungsschranke und Schutz-Hook einen fremden Skill überhaupt sehen. Die Schwere des Befundes steht damit unter Vorbehalt |

**Zu E5 im Klartext:** Fällt die Erhebung so aus, dass ein Skill-Aufruf **keine** Werkzeugaufrufe
im Sinne des Hooks erzeugt, ist dies kein Befund der Schwere mittel mehr, sondern einer, der den
Kern betrifft – dann führt Ebene 7 Verfahren, die an beiden Linien vorbeilaufen. Diese Möglichkeit
ist der Grund, den Punkt zu erheben und nicht zu schätzen.

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** (2026-09-11, nach Erfüllung der Auflage) |
| Datum | 2026-09-11 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | E1 bis E5 wie vorgelegt: Die Reichweite von S4 wird **ausgewiesen, nicht erweitert**; der Auskunftsabschnitt aus `CR-2026-031` wird mitgenutzt; Zeile **S5** kommt in die Matrix; das Overlay fordert **keine** leere Fremdablage – die technische Maßnahme liegt in `CR-2026-038` (nicht importieren statt Ablage leer fordern); E5 ist mit der Erhebung erledigt. Ziel-Release 0.26.0 |
| Umsetzung | **mit Release 0.26.0** – Einzelheiten und Nachweise in `leitwerk-core/CHANGELOG.md` |


**Nachtrag 2026-09-11 – K-24 ist erhoben** (`tests/protocols/2026-09-11-erhebungen-K21-K26.md`): Eine Sonde in der fremden Skill-Ablage erzeugte zwei `read`-Werkzeugaufrufe; beide erreichten den Schutz-Hook, der Zugriff auf die Secret-Datei wurde blockiert – auch im Modus ohne Rückfragen und mit Positivkontrolle im selben Lauf. Der Skill-Aufruf selbst erzeugt **keinen** eigenen Werkzeugaufruf. **Die Schwere bleibt mittel, der vorgelegte Zuschnitt trägt.** Dazu ist K-23 beantwortet: Die fremde Ablage lässt sich projektseitig abschalten (`read_config_from.claude: false`, gemessen 69 → 2 Skills) – E4 ist damit neu zu bewerten, und `CR-2026-038` legt den Mechanismus vor
