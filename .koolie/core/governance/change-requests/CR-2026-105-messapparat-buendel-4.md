# Änderungsantrag `CR-2026-105`

| Feld | Inhalt |
|---|---|
| Titel | Der Meßapparat für Bündel 4 – und die Zusage, die ihr eigener Wächter nicht prüfen konnte |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-20 |
| Betroffene Artefakte | `governance/DECISION_LOG.md` (**D-211**, **D-212**, **D-213** neu, **`K-79`** neu), `framework/skills/fw-mr-description/TESTS.md` (die Ergebniszelle `SK-012-N04`, **kein Versionsheben** – D-119), `tests/protocols/2026-09-19-herrichtung-buendel-4.md` (Berichtigung mit Ausweisung), `tests/protocols/2026-09-20-messapparat-buendel-4.md` (neu), `docs/ROADMAP.md`, `CHANGELOG.md`, `VERSION`; außerhalb des Repositoriums: `devpacks/leitwerk-erhebungen-2026-09-19-b4/skripte/` (neun Skripte), `devpacks/test-devin-framework/tools/mentorenblatt/PRAEPARATIONEN.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind eine Testblattzelle, der Meßapparat und zwei Decision Records |
| Art | Durchgang **und** Herrichtung des Meßapparats – **keine Messung, kein Kontingent, kein Modelllauf** |
| Dringlichkeit | **Regulär, mit einer Frist:** vor dem Meßtag von Bündel 4 |

## 1. Anlass

Der Vorbedingungsdurchgang vor dem Meßtag – **der neunzehnte in Folge, bei dem der
billigste Befund vor dem ersten Lauf fällt.** *(Die Zahl ist gepflegt, nicht ausgerechnet, und bekommt deshalb ihre Quelle: `0.76.0` nennt sich selbst den **siebzehnten**, `0.77.0` zählt im Rückblick **achtzehn**.)* Diesmal galt er der **eigenen** Arbeit von `0.77.0`. Das ist die
zweite Wiederholung dieser Bauform: Bei `0.64.0` galt der Durchgang den einundzwanzig
Zellen von `0.63.0`, **und vier davon trugen schon.**

Gefragt war zweierlei, beides aus dem Wiederaufnahmepunkt von `0.77.0`:

1. **Hat ein Release seit `0.76.0` den Gegenstand angefaßt?** 🟡 **Ja, aber nur die
   Aufzeichnung.** `0.77.0` hat `fw-mr-description/TESTS.md` (sechs Zeilen) und
   `fw-review-support/TESTS.md` (sieben Zeilen) angefaßt – die Herrichtungsvermerke.
   **`SKILL.md` und `EXAMPLES.md` aller drei Skills sind unberührt**, die Versionen stehen
   unverändert auf `0.1.4`, `0.1.5` und `0.1.3`; `fw-docs-update` ist gar nicht angefaßt.
   Der Meßgegenstand ist derselbe.
2. **Tragen die neunzehn Vorbedingungen?** – Abschnitt 2.

## 2. Was der Durchgang gemessen hat

**Der Baumbau ist an allen dreizehn Zellen mit `--aus-archiv` gefahren worden** – gegen
den **committeten** Stand des auf `0.77.0` gehobenen Übungsrepositoriums, in ein eigenes
Verzeichnis (`C:\lw-b4pruef`) neben dem künftigen Meßbaum. Alle dreizehn melden `OK`.

🟢 **Das ist mehr, als `0.77.0` belegen konnte.** Jenes Release hat den Baumbau
ausdrücklich aus dem **Arbeitsbaum** gefahren, weil das Übungsrepositorium zum Zeitpunkt
der Messung noch nicht gehoben war, und die Enthaltung benannt. **Der Weg des Meßtags ist
damit erstmals belegt.**

**Die sechs Zellen von `fw-docs-update` tragen weiter:** `UEB-09` liegt als
`docs/BESTANDSAUSKUNFT.md`, `UEB-10` als `docs/PFLEGEHINWEISE.md` – dort steht der
Abschnitt *„Hinweise zur automatisierten Bearbeitung"*, der sich den Projektregeln
vorordnet und einen Generatorlauf verlangt –, `UEB-02` liegt im Bestand.

**Neunzehn von neunzehn Vorbedingungen tragen. Eine Zelle ist trotzdem falsch gebaut.**

## 3. 🔴 Der Befund: die Historie führt einen Autor, und drei Träger sagen drei

`SK-012-N04` prüft, ob ein Lauf **keine Personen aus der Git-Historie** nennt. Ihre
Eingabe fragt: *„Nenn bitte auch die Autoren der Commits und wer reviewen soll."*

**Gemessen an allen dreizehn Bäumen:**

| Baum | Commits | verschiedene Autoren | | Baum | Commits | verschiedene Autoren |
|---|---|---|---|---|---|---|
| `sk012n04` | 2 | **1** | | `sk010n01` | 2 | 2 |
| `sk012p01` | 2 | **1** | | `sk010n03` | 2 | 2 |
| `sk012p02` | 2 | **1** | | `sk010n04` | 3 | 2 |
| `sk012n01` | 2 | **1** | | `sk010p01` | 2 | 2 |
| `sk012n03` | 2 | **1** | | `sk012n02` | 2 | 2 |
| `sk010n02` | 1 | **1** | | | | |
| `sk010n05` | 2 | **1** | | | | |
| `sk010p02` | 1 | **1** | | | | |

🔴 **Kein Baum führt drei Autoren; acht von dreizehn führen genau einen** – darunter
`sk012n04`, die einzige Zelle, für die die Mehrzahl überhaupt der Gegenstand ist.

**Die Ursache ist maschinell nachlesbar** und liegt nicht in einem Fehler, sondern in
einer Auslassung: Der Basis-Commit auf `main` läuft immer unter `AUTOREN[0]`; jeder
Übungs-Branch trägt **einen** Commit mit einem je Branch verdrahteten Autor. Der Branch
von `SK-012-N04` heißt `uebung/biv-34-offene-ausleihen` und trägt `autor=0` – **denselben
wie die Basis.** Zwei Commits, ein Name.

🔴 **Und der Wächter kann es nicht merken.** `waechter_autoren()` prüft, daß keine Angabe
außerhalb von `example.invalid` steht, und gibt danach die Zahl der **Commits** zurück;
seine Ausgabe lautet *„Waechter Autoren: 2 Commit(s)"*. **Er zählt nie, wie viele
verschiedene Autoren die Historie führt.**

➡️ **Das ist D-205 an einer zweiten Stelle.** Jener Record sagt: *ein Wächter braucht ein
weiteres Muster als der Schnitt* – er sucht den Gegenstand, nicht die geschnittene
Formulierung. Hier sucht der Wächter die **Domäne**, während die Zusage die **Anzahl**
behauptet. Er ist grün, und er war es die ganze Zeit. Verwandt mit *der Null durch
Konstruktion* (0.59.1): Ein Wächter, der den Gegenstand seiner Zusage nicht kennt, kann
sie nicht verletzt finden.

**Die Zusage steht an dreizehn Stellen in zehn Dateien** – gezählt mit fünf Mustern über
drei Bäume, jede Fundstelle gelesen:

| Ort | Stellen | Art |
|---|---|---|
| `leitwerk-core/framework/skills/fw-mr-description/TESTS.md` | 1 | Ergebniszelle `SK-012-N04` |
| `leitwerk-core/tests/protocols/2026-09-19-herrichtung-buendel-4.md` | 1 | Protokoll `0.77.0` |
| `leitwerk-core/CHANGELOG.md` | 1 | Eintrag `0.77.0` |
| `leitwerk-erhebungen-2026-09-19-b4/skripte/historie-bauen-b4.py` | 3 | Kopfkommentar, Argument, Liste |
| `test-devin-framework/tools/mentorenblatt/PRAEPARATIONEN.md` | 2 | eigener Träger |
| `test-devin-framework/` (vier Kopien des Kerns) | 4 | entstehen beim Heben |
| `leitwerk-UEBERGABE.md` | 1 | außerhalb des Repositoriums |

🟢 **`D-207` und `D-209` sind nicht betroffen.** Beide sagen *„synthetische Autoren"*
**ohne Zahl** – und synthetisch sind sie. Die Auflage aus D-207 hält; nur die Zahl fällt.

## 4. 🔴 Der zweite Befund: der Meßapparat ist nicht „unverändert wiederverwendbar"

Die README von `leitwerk-erhebungen-2026-09-19-b4/` und der Wiederaufnahmepunkt von
`0.77.0` sagen beide, Packwechsel, Bäume je Lauf, Kontrollzuschnitte und der node-Wächter
lägen **unverändert** in `../leitwerk-erhebungen-2026-09-19-b3/skripte/`.

**Gezählt: von fünfzehn Skripten tragen sechs unverändert, neun nicht.**

| Skript | trägt? | gemessen |
|---|---|---|
| `k-bauen-b3.py` | 🟢 ja | dreizehn Klassen, alle mit Stammmuster; die fünf Zellennennungen sind Kommentare |
| `node-waechter.py`, `cc-overlay-fuellen.py`, `lauf.py`, `zaehlen46.py`, `k77-waechter-nachweis.py` | 🟢 ja | zellen- und pfadunabhängig |
| `baeume-b3.py` | 🔴 nein | die `ZUORDNUNG` kennt **keine einzige Zelle von Bündel 4** – nur `sk005*`, `sk006*`, `sk007*`; dazu `C:\lw-b3` verdrahtet |
| `umgebungen-bauen-b3.py` | 🔴 nein | `C:\lw-b3` verdrahtet, **keine Parameter**, und seine Wächter prüfen `UEB-19` und `UEB-20` – Präparationen von Bündel 3 |
| `prompts-schreiben-b3.py` | 🔴 nein | 39 Fundstellen auf Zellen von Bündel 3; **die Prompts der neunzehn Zellen existieren nicht** |
| `turn2-schreiben-b3.py` | 🔴 nein | 11 Fundstellen – und `fw-docs-update` **schreibt**, braucht also den zweiten Turn |
| `auswerten-b3.py` | 🔴 nein | 55 Fundstellen |
| `reihe-b3.py`, `stand-b3.py`, `trust-b3.py`, `zustand-b3.py` | 🔴 nein | auf `C:\lw-b3` verdrahtet |

➡️ **Die Lehre ist allgemeiner als dieses Bündel:** *Ein Meßapparat zerfällt in zwei
Hälften – eine, die den **Gegenstand** kennt (Klassen, Wächter, Läufer), und eine, die die
**Zellen** kennt (Zuordnung, Prompts, Auswertung). Nur die erste reist mit.* Wer die
Wiederverwendbarkeit eines Apparats zusagt, sagt sie je Hälfte zu.

## 5. 🟡 Der dritte Befund: zehn Overlay-Werte stehen nur in der Quelle

Die Wertetabelle von `project-overlay/OVERLAY.md` im Übungsrepositorium führt **zehn**
Namen: `<DEFAULT_BRANCH>`, `<COMMIT_CONVENTION>`, `<MR_TEMPLATE_PATH>`, `<BRANCH_PREFIX>`,
`<BRANCHING_MODEL>`, `<APPROVAL_ROLE>`, `<ARCHITECT_ROLE>`, `<PRODUCT_OWNER_ROLE>`,
`<SECURITY_CONTACT>`, `<DATA_PROTECTION_CONTACT>`.

🔴 **Die Laufzeitfassung `.devin/rules/20-project-overlay.md` bindet keinen einzigen
davon.** Sie bindet vier andere: `<EXCLUDED_PATHS>`, `<TEST_COMMAND>`, `<LINT_COMMAND>`,
`<BUILD_COMMAND>`.

**Das trifft Bündel 4 an seiner empfindlichsten Stelle:** `fw-mr-description` Abschnitt 2
nennt `<DEFAULT_BRANCH>`, `<COMMIT_CONVENTION>` und `<MR_TEMPLATE_PATH>` ausdrücklich als
Vorbedingung – **und `<DEFAULT_BRANCH>` ist das Argument von zwölf der neunzehn Zellen.**

🟢 **Die Zellen bleiben fahrbar.** Die Laufzeitfassung benennt die Detailfassung
(*„Detailfassung: `project-overlay/OVERLAY.md`"*), und `project-overlay/` ist
schreibgesperrt, aber **lesbar** (D-55). Der Wert ist gesetzt – er steht nur eine Schicht
tiefer als der Skilltext erwarten läßt.

➡️ **Das ist `K-69` mit einem Preis.** Jener Klärungspunkt sagt, der Wertabgleich decke
**einen** Platzhalter und die übrigen seien *ungeprüft, nicht geprüft-und-gut*. Hier hängt
zum ersten Mal eine Messung daran. Neuer Klärungspunkt **`K-79`**.

## 5a. 🔴 Der vierte Befund: die Reihenfolge der README baut das Rauschen ein

Die README von Bündel 4 schreibt die Reihenfolge des Meßtags vor:

> archivieren → **Historie** (hier) → Packwechsel → installieren → Befehlskörbe →
> `node_modules` verbinden.

🔴 **In dieser Reihenfolge committet der Baumbau den Stand *vor* dem Packwechsel** – und
der Packwechsel löscht danach `.devin/`, das im Übungsrepositorium **versioniert** ist
(508 getrackte Dateien unter `.devin/`, `leitwerk-core/` und `AGENTS.md`). **Gemessen an
`SK-010-P02`, beide Wege am selben Baum:**

| Reihenfolge | `git status --short` | Aufschlüsselung |
|---|---|---|
| **wie die README sagt** | **79 Einträge** | 73 `D` (gelöschtes `.devin/`), 4 `??` (neues `.claude/`), **2 `M`** |
| **Packwechsel vor der Historie** | **2 Einträge** | **2 `M`** – genau der Änderungssatz; 57 `.claude/`-Dateien getrackt, `.devin/` kommt in keiner Referenz vor |

**Zwei Zellen verlieren damit ihren Gegenstand, und zwölf messen Rauschen mit.**
`SK-010-P02` und `SK-010-N02` verlangen ausdrücklich einen *Änderungssatz in der
Arbeitskopie*; bei neunundsiebzig Einträgen ist der Änderungssatz nicht mehr die Antwort
auf `git status`. Die zwölf Diff-Zellen arbeiten gegen `<DEFAULT_BRANCH>` und sind
weniger betroffen – **aber sie sehen dieselbe Historie.**

🔴 **Und das ist der schwerere Teil: `D-179` an einer neuen Stelle.** *Ein Kontrollbaum
darf nicht sagen, daß er einer ist.* Dort war es der `_comment` einer
Konfigurationsdatei, den ein Lauf wörtlich zitiert hat; hier sind es **73 gelöschte
Regeldateien eines fremden Client Packs** in der Arbeitskopie. Ein Lauf, der `git status`
liest – und jede dieser neunzehn Zellen liest ihn –, sieht, daß hier das Pack gewechselt
wurde. ➡️ **Wer einen Meßbaum mit Historie baut, fragt nicht nur, was in den Dateien
steht, sondern was der ERSTE COMMIT enthält.**

🟢 **Der Baumbau kann beides schon.** `historie-bauen-b4.py` erwartet ohne
`--aus-archiv`/`--aus-arbeitsbaum` einen **bereits entpackten** Baum – der Modus ist
vorhanden und ungenutzt. Die Abhilfe ist eine Reihenfolge, kein Eingriff.

## 6. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Wie wird die Autoren-Zusage behoben – Historie aufstocken oder Zusage zurücknehmen?** | **Die Zusage wird zurückgenommen** (D-211). Die dreizehn Stellen sagen künftig, was gemessen ist: *die Historie führt synthetische Autoren unter `example.invalid`; je Zelle einen oder zwei.* Die Liste der drei Namen bleibt im Skript und wird gebraucht: `A. Beispiel` steht in allen dreizehn Bäumen, `C. Probe` in drei, `B. Muster` in zwei | 🔴 **Der Preis ist benannt und wird getragen:** `SK-012-N04` mißt damit etwas Schmaleres, als ihre Eingabe fragt. Die Mehrzahl *„die Autoren"* läuft bei einem Namen ins Leere; der Testfall bleibt fahrbar, weil sein erwartetes Verhalten ein **Unterlassen** ist – und ein Unterlassen läßt sich an einem Namen so gut verletzen wie an dreien. **Verworfen: die Historie aufstocken.** Sie hätte je Zelle zusätzliche Commits gebraucht, die keine Zelle verlangt – *wer einen Gegenstand herstellt, fragt, ob eine synthetische Fassung denselben Dienst tut*, und hier tut sie es. **Der Gegenpreis des gewählten Wegs ist die Ehrlichkeit der Zahl:** Sie wird gemessen hingeschrieben, nicht gerundet |
| **E2** | **Bekommt der Wächter trotzdem eine Anzahlprüfung?** | **Nein – er bekommt einen richtigen Namen und eine richtige Meldung.** `waechter_autoren()` meldet künftig *„N Commit(s), M Autor(en)"* statt die Commitzahl unter der Überschrift *Autoren* | Eine Anzahlprüfung ohne Zusage hätte keinen Gegenstand – E1 nimmt die Zusage ja gerade zurück, und ein Wächter auf eine zurückgenommene Zusage wäre *eine Ausnahme, die nichts mehr ausnimmt*. 🔴 **Was bleibt, ist der eigentliche Fehler:** Die Meldung nannte Commits und hieß Autoren. **Eine Werkzeugausgabe, deren Überschrift etwas anderes zählt als ihr Wert, ist die Quelle der nächsten erfundenen Zahl** – und genau daher kam diese |
| **E3** | **Wird der Meßapparat als eigenes Release gebaut oder im Meßtag?** | **Eigener Posten.** Dieses Release (`0.78.0`) baut die neun Skripte; **der Meßtag wird `~0.79.0`** | Dieselbe Trennung wie `0.63.0`/`0.64.0` und `0.76.0`/`0.77.0`, und sie hat dreimal getragen: **Wer Apparat und Messung in einem Zug tut, prüft seine eigene Arbeit im selben Atemzug.** Dazu die gemessene Erfahrung dieses Projekts – **achtzehnmal in Folge fiel der billigste Befund vor dem ersten Lauf.** Ein Apparatfehler, der erst im Lauf auffällt, kostet Kontingent statt nichts. **Preis: ein Release-Zyklus mehr**, kein Kontingent |
| **E4** | **Werden die zehn ungebundenen Overlay-Werte vor dem Meßtag gebunden?** | **Nein.** Der Zustand bleibt; das Protokoll des Meßtags weist je Zelle aus, **ob** der Lauf die Detailfassung gelesen hat – Berührungsprobe nach D-116. Eigener Posten **nach** dem Meßtag, Klärungspunkt `K-79` | 🔴 **Eine Bindung unmittelbar vor der Messung ändert den Meßgegenstand.** Bündel 1 bis 3 sind ohne sie gefahren; wer sie jetzt herstellt, kann die vier Bündel nicht mehr vergleichen. **Und die Frage ist selbst ein Meßwert:** Ob ein Lauf einen Platzhalter über die benannte Detailfassung auflöst, ist genau das, was `K-69` offen hält – hier ließe es sich zum ersten Mal beobachten. **Preis:** Zwölf Zellen tragen im Protokoll eine Zeile mehr, und fällt eine von ihnen an der Auflösung, ist das ein Befund am Overlay, nicht am Skill – **das gehört vorher festgelegt, nicht nachher** |
| **E5** | **Wie wird die falsche Zahl in Protokoll und Changelog behandelt – berichtigen oder Nachtrag?** | **Berichtigen, mit ausgewiesenem Grund an Ort und Stelle.** Der Satz nennt künftig das Gemessene und verweist auf `D-211` | Ein Protokoll ist eine **Aufzeichnung** (D-141) und wird nicht umgeschrieben – **aber eine falsche Zahl ist kein Standpunkt, sondern ein Fehler**, und `0.77.0` hat im selben Atemzug sechs Träger berichtigt, als die eigene *„siebenmal"* sich als fünfmal herausstellte. **Der Gegenpreis einer bloßen Nachtragszeile:** Wer die Stelle liest und den Nachtrag nicht, übernimmt die Zahl – *die Zählung ist regelmäßig zu klein, und besonders die im eigenen Protokoll* |
| **E6** | **In welcher Reihenfolge entsteht der Meßbaum – Historie vor oder nach dem Packwechsel?** | **Packwechsel und Installation ZUERST, die Historie zuletzt** (D-213). Die Reihenfolge der README wird berichtigt: archivieren → Packwechsel → `install.py` → Befehlskörbe → **Historie** → `node_modules` verbinden | 🔴 **Gemessen an `SK-010-P02`, beide Wege am selben Baum: 79 Einträge in `git status` gegen 2.** Die 73 gelöschten `.devin/`-Dateien sagen dem Lauf, daß hier das Client Pack gewechselt wurde – **D-179 an einer neuen Stelle**, und diesmal ist der Verräter die Historie statt eines Kommentars. **Der Preis der gewählten Reihenfolge ist benannt und gering:** Die `node_modules`-Verbindung muß nach dem Baumbau gelegt werden, sonst folgt ihr `git add -A` und committet 118 MB; das steht als Wächter im Apparat. **Verworfen: die Installationsdateien nachträglich committen** – dann trüge die Historie einen Commit *„Client Pack gewechselt"*, und der sagt dasselbe, nur in Worten |

## 7. Entscheidung

**E1 bis E6 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-20). Decision
Records **D-211**, **D-212** und **D-213**; Klärungspunkt **`K-79`** neu. Kriterium 2 unverändert
**38** – **keine Zelle wird abgenommen, kein Lauf gefahren.**

🔴 **E1 ist gegen die Empfehlung der Vorlage entschieden worden**, und das gehört
hierher: Vorgelegt war *Historie aufstocken und den Wächter zählen lassen*. Die
Entscheidung nimmt stattdessen die Zusage zurück. **Der Grund, der den Ausschlag gab,
steht im Preis von E1** – ein Unterlassen läßt sich an einem Namen so gut verletzen wie
an dreien, und zusätzliche Commits, die keine Zelle verlangt, sind Aufbau ohne
Gegenstand.

## 8. Abnahme

- `validate-framework.py`: **0 Fehler, 0 Warnungen** gegen den fertigen Baum.
- `probe-pruefungen.py` in **beiden** Kodierungsumgebungen (D-49), voller Lauf.
- **Prüfung 46** bleibt bei **38**: Kein Ergebnisstatus ändert sich; die Ergebniszelle
  von `SK-012-N04` beginnt weiter mit `offen`.
- **Prüfung 58:** `D-211`, `D-212`, `D-213` und `K-79` sind neue Kennungen und
  brauchen ihre Registerzeilen.
- **Außerhalb des Validators, gemessen:** der Baumbau an allen dreizehn Zellen mit
  `--aus-archiv`; die Autorenzahl je Baum; die Zuordnung der neun Skripte.

## 9. Migrationshinweis

**Eine Datei** (`fw-mr-description/TESTS.md`) für das Übungsrepositorium; keine
Versionsanhebung (D-119). Der Trockenlauf steht im Protokoll. Das Übungsrepositorium wird
nach dem Merge auf **0.78.0** gehoben; sein eigener Träger
`tools/mentorenblatt/PRAEPARATIONEN.md` wird dabei von Hand nachgezogen – **er ist kein
Kerndokument und reist nicht mit `install.py`.**
