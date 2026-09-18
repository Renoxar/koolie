# Änderungsantrag `CR-2026-081`

| Feld | Inhalt |
|---|---|
| Titel | Der Produktname im Kern – die Ausnahme aus D-28 hatte in ihrem eigenen Geltungsbereich keinen einzigen Fall |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-18 |
| Betroffene Artefakte | zwölf anweisende Träger (Aufzählung in Abschnitt 2), `docs/RUNTIME_GLOSSARY.md`, `docs/PLACEHOLDER_REGISTRY.md`, `tests/scripts/validate-framework.py` (Prüfung 14 verschärft, gemeinsame Ausnahmemenge), `tests/scripts/probe-pruefungen.py` (vier Sonden, drei Gegenproben), `tests/TEST_CATALOG.md`, `governance/DECISION_LOG.md` (D-129 neu, `K-52` geschlossen), `docs/ROADMAP.md`, `VERSION`, `CHANGELOG.md`, `tests/protocols/2026-09-18-wirkungsnachweise-0.57.1.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand ist die Werkzeugneutralität des Kerns (D-02) und die Reichweite von D-28 |
| Art | Änderung (zwölf Träger), Verschärfung (D-28 → D-129), Nachbau (Sonden für Prüfung 14), Erledigung (`K-52`) |
| Dringlichkeit | **Regulär.** Der Befund schadet keinem Projekt; er macht den Kern unwahr über sich selbst – und an der sichtbarsten Stelle, die er hat |

## 1. Anlass – und zuerst zwei Berichtigungen an der eigenen Vorgängerzeile

`K-52` ist mit `0.57.0` eröffnet worden: *Reicht die Erlaubnis aus D-28, den Produktnamen
eines Clients im Kern zu nennen, zu weit?* Der Eintrag nannte **„fünfzehn Fundstellen in
zehn Trägern"** und schrieb: *„Zwei Träger sind gerendert … dort hülfe `<CLIENT_NAME>`
wirklich."*

**Vor dem Eingriff ist unabhängig nachgezählt worden. Beides war falsch.**

> 🔴 **Erstens: es sind ZWÖLF Träger, nicht zehn.** Die beiden Plan-Skills
> (`framework/skills/fw-plan/SKILL.md`, `…/fw-bugfix-prepare/SKILL.md`) fehlten in der
> Aufzählung – sie waren im Fließtext als „die Skills" erwähnt und in der Trägerzahl nicht
> mitgezählt. **Die Zahl der Fundstellen war richtig, die der Träger nicht.**
>
> 🔴 **Zweitens: `<CLIENT_NAME>` hilft in KEINER der fünfzehn Fundstellen** – auch nicht in
> den drei gerenderten. Der Grund steht in Abschnitt 3 und ist der eigentliche Befund
> dieses Antrags.

**Das ist derselbe Befundtyp, den dieses Repositorium seit zehn Releases führt, und er hat
diesmal die eigene Notiz getroffen** – in einem Dokument, dessen Arbeitswissen den Satz
*„Wer hier eine Zahl liest, zählt sie nach – auch die eigene, und besonders die im eigenen
Protokoll"* enthält. **Die Berichtigung steht in der Statuszelle von `K-52`; `CR-2026-080`
und das Protokoll zu 0.57.0 behalten ihren Wortlaut und tragen einen Nachtrag** – dieselbe
Entscheidung wie bei 0.54.1: *Ein Protokoll, das seine eigene Fehleinordnung löscht,
verliert den Lernwert.*

## 2. Der Befund: fünfzehn Fundstellen in zwölf anweisenden Trägern

| Träger | Fundstellen | Was der Name dort trägt |
|---|---|---|
| `framework/core/01-governance.md` | 1 | **Den Geltungsbereich des ganzen Frameworks:** *„Das Framework regelt den Einsatz von \<Produkt\> (und strukturell weiterer KI-gestützter Entwicklungswerkzeuge)"* |
| `framework/core/00-principles.md` | 1 | **Die Reichweite der Belegstatus-Regel:** *„Jede Aussage über \<Produkt\> trägt einen Belegstatus"* – sie gilt für jedes Pack |
| `framework/core/02-privacy.md` | 2 | Eine **Produktaussage** mit `[DOK]` (MCP-Bestätigung) und die Überschrift eines **normativen** Abschnitts |
| `framework/skills/fw-plan/SKILL.md`, `…/fw-bugfix-prepare/SKILL.md` | 2 | Eine **Produktaussage** mit `[DOK]`: Plan-Modus mit Ablage außerhalb des Repositoriums |
| `onboarding/GUIDE.md`, `onboarding/QUICKSTART.md` | 4 | Je der **Titel** und eine Voraussetzung beziehungsweise ein Arbeitsschritt |
| `checklists/09-onboarding.md` | 1 | Eine **Voraussetzung**: *„Zugang zu \<Produkt\> vorhanden"* |
| `framework/org-policies/README.md` | 1 | Ein **Nachweisgegenstand**: *„Freigabe von \<Produkt\> mit Auflagen"* |
| `governance/RELEASE_PROCESS.md` | 1 | Die **Quellenpflicht** des Review-Zyklus – in einem Abschnitt, der „Produktänderungen vom **KI-Client**" heißt |
| `prompts/README.md` | 1 | Den **Zweck der Bibliothek**: *„Vorlagen für wiederkehrende Aufgaben mit \<Produkt\>"* |
| `templates/project-overlay/OVERLAY.md` | 1 | Eine **Optionsliste** im Ausfüllschlitz: *„nur \<Produkt\> lokal / zusätzlich Cloud-Sessions / CLI"* |

> 🔴 **In KEINER der fünfzehn Fundstellen wird der Name bloß genannt.** Jede trägt einen
> Geltungsbereich, eine Produktaussage oder eine Voraussetzung. **Das ist die Antwort auf
> `K-52`, und sie ist schärfer als die Frage:** D-28 erlaubt den Produktnamen, *wo ein
> Produkt gemeint ist* – **diese Erlaubnis hatte in ihrem eigenen Geltungsbereich keinen
> einzigen berechtigten Fall.** Client Packs und Chronik sind ohnehin ausgenommen; übrig
> bleibt nur der Kern, und dort schreibt der Name immer zu.

**Zwei Träger widerlegen sich im selben Abschnitt selbst** – dieselbe Bauform wie bei
`08-skill-conventions.md` in 0.57.0:

- `01-governance.md` Satz 1 nennt ein Produkt, Satz 2 desselben Absatzes sagt richtig
  *„… die mit dem KI-Client arbeiten"*.
- `RELEASE_PROCESS.md` Abschnitt 6 heißt *„Umgang mit Produktänderungen vom KI-Client"*,
  und Punkt 1 nennt ein Produkt; Punkt 4 desselben Abschnitts sagt richtig, ein
  Werkzeugwechsel beschränke sich auf ein neues Client Pack.

## 3. Warum `<CLIENT_NAME>` nicht hilft – auch nicht dort, wo gerendert wird

`0.57.0` E1 hat die Ersetzung nach **gerendert / nicht gerendert** entschieden: Wo
`install.py` auflöst, hilft ein Platzhalter; sonst nicht. **Diese Regel greift hier zu
kurz, und die Messung zeigt warum.**

Drei der zwölf Träger werden gerendert – die beiden Plan-Skills und die Overlay-Vorlage.
**In allen dreien trägt der Name eine Aussage, die nur für ein Pack gilt:**

| Träger | Was dort steht | Was `<CLIENT_NAME>` daraus machen würde |
|---|---|---|
| beide Plan-Skills | *„im Plan-Modus von \<Produkt\> liegt die Plan-Datei unter `~/<RUNTIME_DIR>/plans/` … `[DOK]`"* | Für jedes andere Pack eine **unbelegte Behauptung**. Der Plan-Modus ist Zeile **M4** der Fähigkeitsmatrix von `devin-desktop` – und sie ist dort `[DOK]` **für dieses eine Pack** |
| `OVERLAY.md` | *„nur \<Produkt\> lokal / zusätzlich **Cloud-Sessions / CLI**"* | Die Optionsliste selbst ist produktspezifisch. `<CLIENT_NAME>` hätte den Namen getauscht und die **falschen Optionen stehen lassen** |

> 🟢 **Daraus wird eine Trennlinie, die schärfer ist als „gerendert oder nicht":**
>
> - **Nennen** – der Text trägt den Namen und sagt **nichts** über das Produkt. Dafür ist
>   `<CLIENT_NAME>` gebaut, und er löst sich nur in einer gerenderten Quelle auf.
> - **Zuschreiben** – der Text sagt etwas **über** das Produkt. Das gehört in dessen Client
>   Pack; der Kern verweist auf die **Fähigkeitsmatrix**.

**Und der Nennen-Fall ist im ganzen Bestand genau einmal angewandt – gezählt, nicht
geschätzt:** `framework/runtime/root-instruction.md` trägt `<CLIENT_NAME>` im Titel
(*„Agentenanweisung – Framework für den Einsatz von …"*). Das ist die einzige produktive
Verwendung; alle anderen Fundstellen von `<CLIENT_NAME>` sind Register, Chronik oder
Quelltext, der ihn beschreibt.

## 3a. Beim Umsetzen zugefallen: eine Zeilenkennung ist selbst clientgebunden

Der erste Entwurf der beiden Plan-Skills verwies auf **„Zeile M4 der Fähigkeitsmatrix
seines Client Packs"**. Beim Gegenlesen am Bestand:

| Pack | Zeilen der Fähigkeitsmatrix (Modi) |
|---|---|
| `devin-desktop` | `M1` bis `M7` |
| `claude-code` | **`M1` bis `M3`** – **es gibt dort keine Zeile `M4`** |

> 🔴 **Der Verweis wäre für eines der beiden Packs ins Leere gegangen – dieselbe
> Client-Bindung eine Ebene tiefer, und in einem Satz, der sie gerade beheben sollte.**
> **Keine Prüfung hätte es gemeldet:** Prüfung 31 rechnet die Summen *innerhalb* eines
> Packs nach und verlangt nirgends, dass zwei Packs dieselben Zeilen führen; Prüfung 12
> prüft Pfade, keine dokumentinternen Verweise (`K-48`).

**Abhilfe, und sie steht als Regel im Glossar:** Ein Kerntext verweist auf die
**Fähigkeitsmatrix**, nie auf eine **Zeile** darin.

**Das ist der zweite Fall in zwei Releases, in dem die erste Fassung der Abhilfe den
Befund wiederholt hat** – bei 0.57.0 war es der Verdacht auf eine Falschmeldung, der sich
beim dritten Zuschnitt auflöste. **Die Lehre ist dieselbe: Den eigenen Lösungsvorschlag
gegenprüfen, nicht nur den Befund.**

## 4. Der zweite Befund: Prüfung 14 hatte seit 0.20.0 keine Sonde

Der Nachweissatz lautete *„für die Prüfungen 6 und 18 bis 48"*. **Prüfung 14 lag
außerhalb.** Nach D-23 gilt eine Prüfung ohne Sonde als **nicht vorhanden** – und diese
hier wird mit diesem Release geändert.

**Beim Nachbauen ist ein dritter Befund aufgefallen:** `check_actor_naming` stieg bei
fehlenden Manifesten mit `if not namen: return` **still** aus. Eine Prüfung, die ihren
Gegenstand verliert und nichts sagt, besteht leise – genau die Bauform, gegen die die
Prüfungen 28, 29, 31, 40, 46 und 48 je eine eigene Ankermeldung tragen.

## 5. Der dritte Befund: zwei Ausnahmelisten für denselben Gegenstand

Prüfung 14 las `ACTOR_HISTORY`, Prüfung 48 las `ACTOR_HISTORY + (docs/ROADMAP.md,)`.
**Die beiden Listen waren nach einem einzigen Release schon auseinandergelaufen** – die
Roadmap stand nur in einer von beiden, obwohl sie für beide Chronik ist.

**Ein dritter Nutzer derselben Liste meinte etwas ganz anderes:** Prüfung 13 fragt, welches
Dokument eine **eigene Artefaktversion** trägt. Wer `ACTOR_HISTORY` für die Neutralität
erweitert hätte, hätte Prüfung 13 stillschweigend mit erweitert – `docs/ROADMAP.md` trägt
eine Version und gehört geprüft. **Die Liste sah aus wie ein Begriff und war eine
Zufallsschnittmenge.**

## 6. Vorgeschlagene Änderung

1. Die fünfzehn Fundstellen neutralisieren; wo eine Produktaussage gemeint ist, auf die
   Fähigkeitsmatrix des Packs verweisen (E1).
2. **D-28 verschärfen (D-129):** Im Kern steht kein Clientname – auch nicht mit Zusatz
   (E2).
3. Prüfung 14 entsprechend verschärfen, ihr eine Ankermeldung geben und ihr **erstmals
   Sonden** bauen (E3).
4. Eine **gemeinsame** Ausnahmemenge für Prüfung 14 und 48; Prüfung 13 bekommt eine eigene
   mit eigenem Namen (E4).
5. Die Trennlinie *Nennen / Zuschreiben* in `docs/RUNTIME_GLOSSARY.md` und
   `docs/PLACEHOLDER_REGISTRY.md` aufnehmen.

## 7. Vorlage zur Entscheidung

### E1 – Womit werden die fünfzehn Fundstellen ersetzt?

**Auflösung: mit dem Begriff – und wo eine Produktaussage gemeint ist, mit einem Verweis
auf die Fähigkeitsmatrix des Packs.**

Abschnitt 3: `<CLIENT_NAME>` hilft in keiner einzigen, auch nicht in den drei gerenderten
Trägern. Ein Platzhalter hätte dort die **Aussage** an jedes Pack weitergegeben.

**Preis, benannt, und er ist an zwei Stellen spürbar:**

1. **Die beiden Plan-Skills verlieren eine konkrete Angabe.** Statt *„die Plan-Datei liegt
   unter `~/…/plans/`"* steht dort jetzt *„kennt der Client einen Plan-Modus mit eigener
   Ablage außerhalb des Repositoriums, gilt sie ebenso"*. **Wer den Skill mit
   `devin-desktop` fährt, muss den Pfad jetzt im Pack nachschlagen.** Das ist der Preis
   dafür, dass derselbe Satz mit jedem anderen Pack nicht mehr falsch ist.
2. **`OVERLAY.md` verliert die Beispieloptionen.** *„Cloud-Sessions / CLI"* waren eine
   Ausfüllhilfe; jetzt steht dort *„weitere Betriebsarten"* mit Verweis auf das Pack.
   **`K-04` bleibt davon unberührt** – der Klärungspunkt ist Chronik und behält seinen
   Wortlaut.

**Verworfen:** *`<CLIENT_NAME>` in den drei gerenderten Trägern* – gemessen falsch, siehe
Abschnitt 3. *Die Produktaussagen in die Client Packs kopieren* – sie stehen dort bereits
(Zeile M4 der Fähigkeitsmatrix); eine zweite Fassung wäre eine zweite Quelle.

### E2 – Wird D-28 verschärft, oder werden nur die schärfsten Fälle behoben?

**Auflösung: verschärft. D-129.**

Die Grenze *„wo ein Produkt gemeint ist"* ist **nicht prüfbar** – ein Skript kann Nennen
und Zuschreiben am ausgeschriebenen Namen nicht unterscheiden. Sie hat fünfzehn
Fundstellen durchgelassen, darunter den Geltungsbereich des Frameworks und zwei Titel.
**Eine Marke mit zwei Bedeutungen taugt weder als Bedingung noch als Entlastung** – die
Lehre aus 0.50.0 und 0.52.0, hier auf einen Namen statt auf `<TBD…>` angewandt.

**Preis, benannt:** Der Kern kann ein Produkt nicht mehr beim Namen nennen, auch wo es
handlicher wäre. Wer künftig in einem Kerntext ein Produkt meint, muss entscheiden, ob er
es **nennt** (dann `<CLIENT_NAME>`, und nur in einer gerenderten Quelle) oder ihm etwas
**zuschreibt** (dann gehört es ins Pack). **Das ist mehr Nachdenken je Satz, und es ist der
Zweck der Regel.**

**Verworfen:** *Nur die Titel und `01-governance.md` beheben* – dann bliebe die Grenze
unprüfbar, und der nächste Satz käme ohne Meldung. *D-28 um eine Aufzählung erlaubter
Stellen ergänzen* – eine gepflegte Liste für einen Gegenstand, der sich mit jedem Träger
ändert.

### E3 – Bekommt Prüfung 14 Sonden?

**Auflösung: ja, vier Sonden und drei Gegenproben.**

D-23 ist unbedingt formuliert, und sie wird hier **geändert**. Die Nachweisspanne lautet
jetzt *„6, 14 und 18 bis 48"*; Prüfung 40 rechnet sie aus und hält sie an drei Stellen
wörtlich nach.

**Der Gegenstand ist größer als die Verschärfung:** Sonde `14b` belegt, dass die
**bisherige** Aussage – der bloße Name als Handelnder – weiterhin gemeldet wird. *Eine neue
Prüfung darf den Fall ihrer Vorgängerin nicht mitnehmen.* Sonde `14c` belegt den zweiten
Teil (ein Platzhalter mit Clientnamen), `14d` die neue Ankermeldung.

**Preis, benannt:** Vier Einheiten mehr je Sondenlauf. Gemessen sind das rund vier Sekunden
Rechenzeit auf acht Bahnen – der Lauf ist nebenläufig und wächst an der Wanduhr kaum.

### E4 – Eine Ausnahmemenge für beide Prüfungen, oder zwei?

**Auflösung: eine – und Prüfung 13 bekommt eine eigene mit eigenem Namen.**

Abschnitt 5. Zwei Listen für denselben Gegenstand driften, und sie hatten es nach einem
Release schon getan. **Umgekehrt gilt genauso:** Prüfung 13 stellt eine andere Frage und
darf nicht an derselben Liste hängen, nur weil deren Inhalt zufällig passte.

**Preis, benannt:** `OHNE_ARTEFAKTVERSION` und `NEUTRAL_CHRONIK` haben heute fast denselben
Inhalt und werden getrennt gepflegt. **Wer eine Chronikdatei ergänzt, muss entscheiden, ob
sie eine Artefaktversion trägt** – und wenn er es übersieht, meldet Prüfung 13 es, nicht
die Neutralitätsprüfung. Das ist die richtige Richtung für einen Irrtum.

### E5 – `0.57.1` oder `0.58.0`?

**Auflösung: `0.57.1`.**

`RELEASE_PROCESS.md` Abschnitt 1: **MINOR** bei neuen Modulen, Skills oder Regeln ohne
Overlay-Bruch; **PATCH** bei Korrekturen und Formulierungen. Dieses Release bringt **kein
neues Modul, keinen neuen Skill und keine neue Regel** – es nimmt einer bestehenden Regel
ihre Ausnahme und ändert Formulierungen in zwölf Trägern.

**Preis, benannt:** Eine verschärfte Regel als PATCH auszuliefern, **unterzeichnet sie** –
wer nur die Versionsnummer liest, hält 0.57.1 für eine Korrektur. **Gegengewicht:** Der
Releaseplan hat `0.58.0` für Sitzungstest 3 vergeben; ein MINOR hier verschöbe jede
folgende Nummer, und die Nummern des Plans sind eine Reihenfolge. Der Migrationsabschnitt
im Änderungsverzeichnis trägt die Verschärfung sichtbar.

## 8. Prüffragen

| Frage | Antwort |
|---|---|
| Stimmt die Zahl fünfzehn? | **Ja, und sie ist doppelt belegt.** Eigene Zählung mit abgeleiteten Namen über alle Textendungen: 20 Treffer in 13 Trägern, davon 5 im Validator (Werkzeug) – bleiben **15 in 12**. Und der Gegenbeweis: die verschärfte Prüfung 14 gegen den unberührten Vorstand `0.57.0` meldet **genau 15 in genau 12** |
| Gibt es weitere Hersteller- oder Produktnamen im Kern? | **Nein.** Gesucht wurde zusätzlich nach `Windsurf`, `Codeium`, `Cascade`, `Anthropic`, `OpenAI`, `Codex`, `Copilot`, `Cursor`, `Gemini`, `GPT` – **kein Treffer** außerhalb von Chronik, Client Packs und Abbildungstabellen |
| Bleibt `<CLIENT_NAME>` übrig, wenn er nirgends mehr gebraucht wird? | **Er wird gebraucht – genau einmal.** `framework/runtime/root-instruction.md` trägt ihn im Titel, und das ist der Nennen-Fall. Ein Platzhalter mit genau einem Fall ist kein toter Platzhalter |
| Verliert Prüfung 14 ihren alten Gegenstand? | **Nein, und das ist belegt.** Sonde `14b` setzt den bloßen Namen als Handelnden – er wird weiterhin gemeldet |
| Bricht die gemeinsame Ausnahmemenge Prüfung 13? | **Nein.** Sie bekommt eine eigene Konstante mit dem alten Inhalt; `docs/ROADMAP.md` bleibt dort **in** der Prüfung, weil sie eine Artefaktversion trägt |
| Ist die Produktaussage zum Plan-Modus im Pack wirklich vorhanden? | **Ja, nachgelesen:** `clients/devin-desktop/CLIENT_PACK.md` Zeile **M4** – „Plan-Modus mit persistenter Plan-Datei … außerhalb des Repositorys", `[DOK]`. Der Kern verweist jetzt auf die **Matrix**, nicht auf die Zeile – siehe Abschnitt 3a |
| Erreicht die Änderung ein übernehmendes Projekt? | **Drei Träger werden gerendert** – die beiden Plan-Skills und die Overlay-Vorlage. Die Skills gehen mit `install.py --update` mit; die Overlay-Vorlage ist `shared_seed` und wird **nur bei der Erstinstallation** geschrieben. Gemessen in Abschnitt 10 |

## 9. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** (E1 bis E5) |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Die Ausnahme aus D-28 hatte in ihrem eigenen Geltungsbereich keinen einzigen berechtigten Fall; eine Grenze, die ein Skript nicht ziehen kann, ist keine. `<CLIENT_NAME>` hilft in keiner der fünfzehn Fundstellen, weil alle fünfzehn zuschreiben statt zu nennen. Eine Prüfung, die geändert wird und keine Sonde hat, gilt nach D-23 als nicht vorhanden |
| Ziel-Release | **0.57.1** |
| Decision-Log-Eintrag | **D-129**; **`K-52`** geschlossen und in der Trägerzahl berichtigt |

## 10. Umsetzung

- [x] Fünfzehn Fundstellen in zwölf Trägern auf den Begriff umgestellt; die drei
      Produktaussagen verweisen auf die Fähigkeitsmatrix des Packs
- [x] `tests/scripts/validate-framework.py`: Prüfung 14 verschärft, Ankermeldung statt
      stillem Ausstieg, Registereintrag neu; **gemeinsame Ausnahmemenge** `NEUTRAL_*` für
      Prüfung 14 und 48; `OHNE_ARTEFAKTVERSION` für Prüfung 13
- [x] `tests/scripts/probe-pruefungen.py`: vier Sonden (`14a` bis `14d`), drei Gegenproben
      (`14a` bis `14c`); Sondenmenge auf `6, 14 und 18 bis 48` an allen drei Stellen
- [x] `docs/RUNTIME_GLOSSARY.md`: die Trennlinie *Nennen / Zuschreiben*;
      `docs/PLACEHOLDER_REGISTRY.md`: `<CLIENT_NAME>` geschärft
- [x] `governance/DECISION_LOG.md`: **D-129** neu, **`K-52`** geschlossen und berichtigt
- [x] `docs/ROADMAP.md`: Abschnitt zu 0.57.1, **Nachtrag** an den Abschnitt zu 0.57.0
- [x] Versionen der berührten Träger gehoben; die beiden Skill-`CHANGELOG.md` ergänzt
- [x] `VERSION` auf `0.57.1`; CHANGELOG-Eintrag
- [x] Validator ohne Fehler; Sondenlauf in beiden Kodierungsumgebungen
- [x] **Dokumentation:** `tests/protocols/2026-09-18-wirkungsnachweise-0.57.1.md`
- [ ] **Zur Entscheidung offen:** `K-37` (Versionszelle der Vorlagen)

## 11. Abnahme

- `validate-framework.py --root .`: 0 Fehler, 0 Warnungen
- `probe-pruefungen.py .` in beiden Kodierungsumgebungen: alle Ergebniszeilen bestanden
- **Gegenbeweis gegen den unberührten Vorstand `0.57.0`** (`git archive 7b06b72`,
  Installation mit dem `install.py` des Arbeitsbaums): **genau 15 Fundstellen in genau 12
  Trägern** – die Aufzählung dieses Antrags, ohne Rest und ohne Überschuss
- Kriterium 2 unverändert **105**, Kriterium 1 unverändert **23**
- Protokoll: `tests/protocols/2026-09-18-wirkungsnachweise-0.57.1.md`
