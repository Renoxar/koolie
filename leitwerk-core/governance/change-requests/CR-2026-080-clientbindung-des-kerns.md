# Änderungsantrag `CR-2026-080`

| Feld | Inhalt |
|---|---|
| Titel | Die Clientbindung des werkzeugneutralen Kerns – siebzehn Fundstellen, und die Prüfung, die sie melden sollte, trug sie selbst |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-18 |
| Betroffene Artefakte | vierzehn anweisende Träger (Aufzählung in Abschnitt 2), `docs/RUNTIME_GLOSSARY.md`, `tests/scripts/validate-framework.py` (Prüfung 48 neu, `LINK_ROOTS` abgeleitet, `OPTIONAL_RUNTIME_RE` entfernt), `tests/scripts/probe-pruefungen.py` (vier Sonden, drei Gegenproben), `tests/TEST_CATALOG.md`, `governance/DECISION_LOG.md` (D-128 neu, `K-52` neu), `docs/ROADMAP.md`, `VERSION`, `CHANGELOG.md`, `tests/protocols/2026-09-18-wirkungsnachweise-0.57.0.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand ist die Werkzeugneutralität des Kerns (D-02) und ihre Durchsetzung |
| Art | Änderung (vierzehn Träger), Neubau (Prüfung 48), Rückbau (`OPTIONAL_RUNTIME_RE`), Klärungspunkt (`K-52`) |
| Dringlichkeit | **Regulär.** Der Befund ist seit 0.31.0 wirksam und hat keinem Projekt geschadet; er macht den Kern nur unwahr über sich selbst |

## 1. Anlass

Der Releaseplan (`CR-2026-078`, D-124) führt `0.57.0` als *„Die Clientbindung des
werkzeugneutralen Kerns – 17 Fundstellen in 14 anweisenden Trägern … Dazu die Prüflücke
benennen, die es nie gemeldet hat"*. Die Aufzählung lag aus der Erhebung vom 17.09. fertig
vor.

**Sie ist vor der Umsetzung unabhängig nachgezählt worden** – die Aufzählung stammte aus
einem Skript außerhalb des Repositoriums, mit einer von Hand gepflegten Markenliste und nur
über `.md`-Dateien. Die Nachzählung hat andere Marken benutzt (abgeleitet aus den
Manifesten), alle Textendungen gelesen und Mehrfachtreffer auf derselben Stelle
ausgeschlossen.

> 🟢 **Die Zahl hält: siebzehn Fundstellen in vierzehn anweisenden Trägern.** Das ist in
> diesem Projekt die Ausnahme – die Aufgabenbeschreibung war zehnmal in Folge zu klein.
> **Der Gegenstand ist trotzdem größer geworden, nur an anderer Stelle:** nicht bei den
> Fundstellen, sondern bei der Prüflücke (Abschnitt 3).

## 2. Erster Befund: siebzehn Fundstellen in vierzehn anweisenden Trägern

`docs/RUNTIME_GLOSSARY.md` sagt seit 0.31.0: *„Im Kern wird ausschließlich der Begriff
verwendet."* Vierzehn Träger taten es nicht.

| Träger | Fundstellen | Was dort stand |
|---|---|---|
| `prompts/01`, `02`, `03`, `05`, `06`, `07` | 6 | Die Ausgabeformatzeile der **Prompt-Vorlage selbst** – der Text, den ein Mensch in seinen Client kopiert – nannte den Skillpfad eines Packs |
| `framework/core/08-skill-conventions.md` | 1 | Abschnitt 2, **normativ**: der Ablagebaum im Codeblock |
| `framework/role-packs/README.md` | 2 | die beiden Aktivierungsbefehle im `bash`-Block |
| `framework/tech-packs/_template/TECH_PACK.md` | 2 | der Ausfüllhinweis |
| `framework/role-packs/_template/ROLE_PACK.md` | 1 | der Ausfüllhinweis |
| `tests/TEST_CATALOG.md` | 2 | die **Eingabezellen** von `FW-ZA-02` und `FW-AK-02` |
| `decision-trees/03-analyze-or-modify.md` | 1 | Punkt 7 der normativen Textbeschreibung |
| `governance/CHANGE_REQUEST_TEMPLATE.md` | 1 | der Verwendungshinweis |
| `tests/EDGE_CASES.md` | 1 | Grenzfall `G-14` |

> 🔴 **Der schärfste Einzelbefund steht in einem normativen Kernmodul und widerlegt sich
> zwei Zeilen tiefer selbst.** `08-skill-conventions.md` Abschnitt 2 zeigte den Ablagebaum
> unter dem Verzeichnisnamen eines Packs – und der Absatz direkt darunter sagt seit jeher
> richtig: *„Ablageort: die Skill-Ablage der Laufzeitschicht … Der konkrete Pfad … steht im
> Client Pack."* **Die Zusage und ihre Widerlegung standen in demselben Abschnitt**, und
> die falsche von beiden war die normative Form.

**Ein zweiter Befund ist beim Lesen zugefallen und wird mitbehoben:** Die beiden
Pack-Vorlagen wiesen an, die Laufzeitfassung **in der Regelablage** anzulegen. Sie gehört
in die Quellablage des Packs (`<pack>/runtime/`), wie `role-packs/README.md` selbst sagt
und wie beide bestehenden Packs es halten. Wer der Vorlage wörtlich folgte, legte die Datei
an einer Stelle an, die `install.py --update` nie anfasst. **Die Fundstelle war
clientgebunden *und* falsch; der Client war das Auffälligere von beidem.**

## 3. Zweiter Befund: Warum keine der 47 Prüfungen es gemeldet hat

Prüfung 12 trug bis 0.56.2 am Ende von `check_links` eine Warnung mit genau diesem Wortlaut:
*„… nennen die Laufzeitschicht des Client Packs … Im werkzeugneutralen Kern ist das eine
Client-Bindung (D-02)."* Sie hat in siebenundfünfzig Releases keine der siebzehn Stellen
gemeldet. **Drei Gründe, und der dritte stand in keiner Fassung des Befunds:**

1. **Sie liest nur Token in Backticks.** Zehn der siebzehn standen ohne – im Codeblock, in
   Prosa oder im HTML-Kommentar.
2. **Sie meldet nur Pfade, die es NICHT GIBT.** Im Framework-Repositorium ist genau ein
   Pack installiert; dessen Laufzeitschicht existiert und ist damit unsichtbar. Gemeldet
   wurde nur der jeweils *andere* Client. **Das ist `B02` eine Ebene höher.**
3. 🔴 **Ihre eigene Wurzelliste war clientgebunden.** `LINK_ROOTS` führte wörtlich
   `.devin/`, `AGENTS.md` und `AGENTS.local.md`. Die Pfade des anderen Packs waren damit
   **gar kein Kandidat** der Heuristik. **Die Prüfung, die die Client-Bindung melden
   sollte, trug sie selbst.**

### 3.1 Und der dritte Grund ist beim Messen kleiner geworden, nicht größer

Der Verdacht war, die enge Wurzelliste erzeuge in einer Installation des anderen Packs eine
**Falschmeldung**: Ein Verweis auf die Laufzeitfassung eines aktivierten Role Packs
(`…/rules/30-role-…`) sei dort als toter Pfad gemeldet worden, weil die Ausnahme
`OPTIONAL_RUNTIME_RE` nur `.devin/` kannte.

**Gemessen in drei Zuschnitten – der Verdacht trifft nicht zu** (Protokoll Abschnitt 3):

| Zuschnitt | Ergebnis |
|---|---|
| `claude-code`-Installation, Kerntext mit `.claude/rules/30-role-…`, **alter** Validator | **nichts gemeldet** – der Pfad war kein Kandidat der Wurzelliste |
| dieselbe Lage, **neuer** Validator | **nichts gemeldet** – der Pfad ist Kandidat und wird von der Fremdpfaderkennung gedeckt |
| dritter Zuschnitt: Ausnahme ausgeschaltet, Fremdpfaderkennung aktiv | **nichts gemeldet** – die Ausnahme ist unerreichbar |

> 🔴 **Zwei Fehler in derselben Richtung haben einander gedeckt.** `LINK_ROOTS` war zu eng,
> und `OPTIONAL_RUNTIME_RE` war auf dieselbe Weise zu eng. Die erste Enge verhinderte, dass
> die zweite je auffiel. **Das ist eine Bauform, die dieses Repositorium noch nicht geführt
> hat** – neben *„die Zusage, die mehr verspricht als sie leistet"* steht jetzt *„zwei
> Stellen, die einander decken"*. Einzeln wäre jede aufgefallen; zusammen sahen sie aus wie
> ein Lauf ohne Befund.

> 🟢 **Daraus folgt ein Rückbau, kein Umbau:** Sobald die Client-Bindungs-Warnung nach
> Prüfung 48 wandert, ist `OPTIONAL_RUNTIME_RE` **unerreichbar** – die Fremdpfaderkennung
> deckt denselben Fall vollständig ab. **Eine Ausnahme, die nichts mehr ausnimmt, ist
> schlimmer als keine: Sie sieht wie Sorgfalt aus.**

## 4. Dritter Befund: Die Ausnahmen standen außerhalb des Repositoriums

Die Erhebung vom 17.09. hat `docs/ROADMAP.md`, `tests/scripts/` und die
Ergebnisstatus-Zellen des Testkatalogs **bewusst nicht gezählt** – der Grund stand im
Kopfkommentar eines Skripts in `devpacks/leitwerk-erhebungen-2026-09-17-schranken/`. Das
Glossar nennt als historische Dokumente nur vier Träger und die Roadmap nicht.

**Eine Ausnahme, die nur im Quelltext einer Prüfung oder in einem Erhebungsskript steht, ist
keine Regel, sondern eine Voreinstellung.** Sie gehört in das Dokument, das die Regel trägt.

## 5. Vorgeschlagene Änderung

1. Die siebzehn Fundstellen durch den **Begriff** ersetzen (E1), den Nebenbefund zu den
   Pack-Vorlagen mitbeheben.
2. Die vier Ausnahmegattungen in `docs/RUNTIME_GLOSSARY.md` aufnehmen, vollständig und mit
   Begründung je Gattung – `build/` **mit Frist**.
3. **Prüfung 48** bauen, Marken aus den Manifesten abgeleitet; vier Sonden, drei
   Gegenproben.
4. `LINK_ROOTS` aus den Manifesten ableiten, `OPTIONAL_RUNTIME_RE` entfernen, die
   Client-Bindungs-Warnung aus Prüfung 12 nach Prüfung 48 überführen.
5. `K-52` für die Produktnamen anlegen.

## 6. Vorlage zur Entscheidung

### E1 – Platzhalter oder Begriff?

**Auflösung: Begriff.**

**Keiner der vierzehn Träger wird gerendert.** `install.py` löst Laufzeit-Platzhalter nur in
`framework/runtime/`, `framework/skills/`, `templates/rules/`, `templates/project-overlay/`
und den `runtime/`-Ablagen der Packs auf – nachgelesen in `render_for_client` und den
`shared_core`/`shared_seed`-Einträgen beider Manifeste. Ein `<SKILLS_DIR>` in
`leitwerk-core/prompts/` bliebe **für immer stehen**. Schlimmer: `prompts/README.md`
Abschnitt 3 erklärt spitze Klammern als *Overlay-Werte, die ein Mensch ersetzt* – ein
Laufzeit-Platzhalter dort wäre **eine Marke mit zwei Bedeutungen**, und genau daran ist
0.52.0 schon einmal hängengeblieben.

**Preis, benannt:** Der Text wird länger und verliert die Kopierbarkeit. *„Ausgabeformat:
Repository-Analyse nach Abschnitt 5 der `SKILL.md` des Skills `fw-repo-analyze`"* ist
sperriger als der Pfad und **kann nicht mehr blind eingefügt werden**. Das trifft
ausgerechnet die sechs Prompt-Vorlagen, deren Zweck das Kopieren ist.

**Verworfen:** *Laufzeit-Platzhalter überall* – er löst sich in keinem der vierzehn Träger
auf. *Beides, je nach Träger* – eine Marke, die in einem Bestand mal aufgelöst und mal
wörtlich gemeint ist, taugt weder als Bedingung noch als Entlastung (die Lehre aus 0.50.0
und 0.52.0).

**Eine Ausnahme mit Begründung:** Im `bash`-Codeblock von `framework/role-packs/README.md`
steht kein Begriff, sondern ein **Ausfüllschlitz** `<Regelablage>` / `<Skill-Ablage>` – die
Zeile ist ein Befehl und braucht eine Stelle zum Einsetzen. Sie steht in demselben Block wie
`<pack>`, folgt also einer Form, die dort schon galt, und eine Kommentarzeile darüber nennt
das Glossar als Quelle. **Prüfung 12 verwirft spitze Klammern über `NOT_A_PATH`** – der
Schlitz erzeugt also keinen toten Verweis.

### E2 – Nur benennen, oder die Prüflücke schließen?

**Auflösung: schließen. Prüfung 48.**

Der Plan sagt *„die Prüflücke benennen"*. Das genügt nicht: **Die siebzehn Fundstellen sind
entstanden, weil nichts sie maß.** Wer sie entfernt und die Lücke offen lässt, stellt genau
den Zustand wieder her, der sie erzeugt hat – und der nächste Träger kommt ohne Meldung.
D-23 sagt es für Prüfungen; hier gilt es für die Regel: **Eine Norm ohne Durchsetzung ist
der wiederkehrende Befundtyp dieses Projekts** (vgl. `K-41` für die `[TECHNISCH]`-Norm).

**Preis, benannt, und er ist zweiteilig:**

1. **Sie prüft die Schreibweise, nicht die Sache** – derselbe Gegenpreis wie bei `K-40`.
   Ein Kerntext, der „lege die Datei im Verzeichnis `.devin` ab" mit einem Leerzeichen statt
   eines Schrägstrichs schreibt, läuft durch. **Gegengewicht:** Die Marken sind abgeleitet,
   nicht geraten, und der Gegenbeweis in Abschnitt 8 zeigt, dass sie den ganzen Bestand
   treffen.
2. **Die Ausnahmemenge ist der eigentliche Inhalt** – und eine Ausnahme, die falsch
   geschnitten ist, entfernt den Gegenstand mit. Deshalb steht sie im Glossar, nicht im
   Quelltext, und deshalb belegt Sonde `48c`, dass der Zuschnitt beim Testkatalog **nicht**
   zu breit ist.

**Verworfen:** *Prüfung 12 erweitern* – sie prüft tote Verweise; ihre drei Grenzen
(Backticks, Existenz, Wurzelliste) sind für diesen Zweck richtig und für jenen falsch. Zwei
Gegenstände in einer Prüfung hätten beide verwässert.

### E3 – Bleibt die Client-Bindungs-Warnung in Prüfung 12?

**Auflösung: nein, sie wandert vollständig nach Prüfung 48 – und wird dort ein Fehler.**

Zwei Prüfungen, die denselben Gegenstand melden, sind eine Verdopplung; welche von beiden
gilt, entscheidet dann der Zufall des Aufrufpfads. Die Erkennung selbst **bleibt** in
Prüfung 12 – sie verhindert weiterhin, dass ein Packpfad als toter Verweis gemeldet wird.

**Warnung → Fehler, weil D-02 normativ ist** und der Bestand jetzt sauber ist: Eine Warnung
hätte niemanden aufgehalten, und die siebzehn Stellen belegen das für siebenundfünfzig
Releases.

**Preis, benannt:** Ab sofort blockiert ein clientgebundener Pfad in einem Kernträger den
Validatorlauf. Wer einen Befund **beschreiben** will, muss ihn in die Chronik schreiben –
oder die Ausnahmemenge ändern und begründen. Das ist gewollt und macht das Schreiben eines
Kerntextes unbequemer.

### E4 – Wird `LINK_ROOTS` abgeleitet, obwohl die Messung keine Wirkung zeigt?

**Auflösung: ja, und die fehlende Wirkung gehört hingeschrieben.**

Abschnitt 3.1: Die Ableitung behebt **keine gemessene Falschmeldung**. Sie schafft eine von
Hand gepflegte Clientliste ab, die ein drittes Client Pack (`openai-codex`, Release `1.1.0`)
nachtragen müsste und die **niemand nachzählt** – dieselbe Bauform, an der Prüfung 40
gebaut wurde.

**Preis, benannt:** Eine Änderung am Prüfapparat ohne gemessene Wirkung ist eine Änderung
auf Vorrat. Sie kostet einen Funktionsaufruf je Lauf und die Pflicht, sie ehrlich zu
beschreiben; **die Versuchung, ihr nachträglich eine Wirkung anzudichten, ist der eigentliche
Preis.**

**Verworfen:** *`LINK_ROOTS` wörtlich lassen* – dann steht neben einer abgeleiteten
Markenliste (Prüfung 48) eine gepflegte für denselben Gegenstand.

### E5 – Wo steht die Ausnahmemenge, und gehört `docs/ROADMAP.md` hinein?

**Auflösung: im Glossar, und ja.**

Zehn Fundstellen liegen in der Roadmap; **neun davon in Rückblicks- und Befundabschnitten**
(„Was 0.55.0 offen lässt", „Unabhängiges Review vom 2026-09-12", die Erhebungstabellen).
Die zehnte steht in der Aktivitätenzeile von `AP2` – einem Arbeitspaket, das **im Absatz
unter seinem Steckbrief selbst sagt**: *„Dieses Arbeitspaket ist bewusst clientspezifisch."*

**Preis, benannt:** Die Roadmap ist **kein reines Chronikdokument** – sie trägt den
Releaseplan, also Text, der anweist. Eine Datei-Ausnahme nimmt beides heraus. **Die
Alternative wäre schlechter:** ein Zuschnitt nach Abschnitten, der an jeder neuen
Überschrift bricht.

**`tests/scripts/` und `build/`:** Werkzeuge müssen Pfade nennen – `install.py` und
`clientmap.py` lösen sie auf, die Prüfskripte stellen Installationen her. Prüfung 12 nimmt
`tests/scripts/` aus demselben Grund schon aus. **`build/` bekommt als einzige Ausnahme
eine Frist:** Es hält die Quellen des Hauptdokuments, das über vierzig Releases zurück ist;
die Ausnahme fällt mit `AP11` (~0.69.0) und steht dort in der Roadmap. **Eine Ausnahme ohne
Frist an einem Träger, der ohnehin neu gesetzt wird, wäre eine stille.**

### E6 – Gehören die Produktnamen in dieses Release?

**Auflösung: nein. `K-52`, mit vollständiger Aufzählung.**

Die Nachzählung hat **fünfzehn Nennungen des Produktnamens in zehn Trägern** gefunden –
`onboarding/GUIDE.md` (im **Titel**), `onboarding/QUICKSTART.md` (im Titel),
`prompts/README.md` (*„zwölf geprüfte Vorlagen für wiederkehrende Aufgaben mit …"*),
`checklists/09-onboarding.md`, `framework/org-policies/README.md`,
`framework/core/00-principles.md`, `-01-governance.md`, `-02-privacy.md`,
`governance/RELEASE_PROCESS.md`, `templates/project-overlay/OVERLAY.md`.

**Das ist keine Lücke, sondern eine entschiedene Position:** D-28 lässt den Produktnamen
ausdrücklich zu, *„wo ein Produkt gemeint ist"*, und Prüfung 14 setzt genau diese Grenze
durch. Sie umzuwerfen braucht eine eigene Vorlage mit eigenem Preis.

**Der Zweifel, den `K-52` festhält, ist eng und benennbar:** D-28 erlaubt den Namen, wo ein
**Produkt** gemeint ist – nicht, wo der Kern ein bestimmtes Werkzeug **voraussetzt**. Ein
Onboarding-Leitfaden, der ein Produkt im Titel trägt, und eine Prompt-Bibliothek, die sich
als *„Vorlagen für Aufgaben mit einem Produkt"* einführt, sind Kandidaten für die zweite
Lesart. **Zwei Träger sind gerendert** (`templates/project-overlay/OVERLAY.md` und die
Skills) – dort hülfe `<CLIENT_NAME>` wirklich; in den übrigen acht nicht.

**Preis der Vertagung, benannt:** Der Kern bleibt an ein Produkt gebunden, und zwar an der
sichtbarsten Stelle, die er hat – dem Titel des Dokuments, das neue Entwicklerinnen und
Entwickler zuerst lesen. **Ein Klärungspunkt ohne Ziel-Release bleibt in diesem Projekt
erfahrungsgemäß lange liegen** (D-124); deshalb trägt `K-52` einen Kandidaten: `0.57.1`
oder das Release, das `AP11` vorbereitet.

## 7. Prüffragen

| Frage | Antwort |
|---|---|
| Stimmt die Zahl siebzehn? | **Ja, und sie ist doppelt belegt.** Unabhängige Nachzählung vor dem Eingriff: 80 Treffer in 18 Trägern, davon 44 in `tests/scripts/`, 10 in der Roadmap, 9 in Ergebnisstatus-Zellen – bleiben **17 in 14**. Und der Gegenbeweis in Abschnitt 8: Prüfung 48 gegen den unberührten Vorstand meldet **genau 17**, in genau diesen 14 Trägern |
| Wird ein bestehender Verweis dadurch ungenau? | **Ja, an einer Stelle bewusst.** `G-14` beschrieb einen Grenzfall über zwei konkrete Dateinamen, die sich nur in der Schreibung unterscheiden. Der Begriff kann das nicht abbilden; die Zelle nennt jetzt „eine zweite Datei, deren Name sich nur in der Groß-/Kleinschreibung unterscheidet". **Der Grenzfall bleibt derselbe, sein Beispiel ist weg** |
| Bricht Prüfung 48 einen bestehenden Träger? | **Nein.** Validatorlauf gegen den fertigen Baum: 0 Fehler, 0 Warnungen |
| Kann Prüfung 48 leise bestehen? | **Nein, und das ist belegt.** Sonde `48d`: Ohne `runtime_placeholders` in den Manifesten meldet sie den verlorenen Gegenstand selbst (D-23) |
| Schneidet die Testkatalog-Ausnahme zu breit? | **Nein, und das ist belegt.** Sonde `48c` setzt denselben Pfad in eine **anweisende** Spalte derselben Tabelle – er wird gemeldet. Gegenprobe `48b` setzt ihn in die **letzte** Zelle – er wird nicht gemeldet |
| Werden die Versionszellen der beiden Pack-Vorlagen gehoben? | **Nein, bewusst.** `K-37` ist offen: Die Versionszelle einer Vorlage hat dieselbe Bauform wie ihre Statuszelle, die 0.53.0 zum Ausfüllschlitz gemacht hat. Sie hier zu heben, hieße `K-37` nebenbei zu entscheiden |
| Ist der Nebenbefund zu den Pack-Vorlagen gemessen? | **Er ist am Bestand gegengeprüft:** Beide vorhandenen Packs legen ihre Laufzeitfassung unter `<pack>/runtime/` ab, und `role-packs/README.md` schreibt es so. Ein Lauf, der der alten Vorlage folgt, ist **nicht** gefahren – der Befund ist ein Textbefund mit zweiter Quelle im Bestand |

## 8. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** (E1 bis E6) |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Die Regel galt seit 0.31.0 und wurde von nichts durchgesetzt; siebzehn Fundstellen sind die Folge, nicht der Zufall. Der Begriff ist die einzige Ersetzung, die in nicht gerenderten Trägern trägt. Die Prüflücke zu benennen, ohne sie zu schließen, stellt den Zustand wieder her, der sie erzeugt hat. Die Produktnamen sind eine entschiedene Position und brauchen eine eigene Vorlage |
| Ziel-Release | **0.57.0** |
| Decision-Log-Eintrag | **D-128**; **`K-52`** neu |

## 9. Umsetzung

- [x] Siebzehn Fundstellen in vierzehn Trägern auf den Begriff umgestellt; Nebenbefund zu
      den beiden Pack-Vorlagen mitbehoben
- [x] `docs/RUNTIME_GLOSSARY.md`: vier Ausnahmegattungen, die Spaltenregel für den
      Testkatalog, was die Regel durchsetzt; Version `0.1.1` → `0.2.0`
- [x] `tests/scripts/validate-framework.py`: **Prüfung 48** neu mit Registereintrag;
      `LINK_ROOTS` abgeleitet; `OPTIONAL_RUNTIME_RE` entfernt; Client-Bindungs-Warnung aus
      Prüfung 12 entfernt
- [x] `tests/scripts/probe-pruefungen.py`: vier Sonden (`48a` bis `48d`), drei Gegenproben
      (`48a` bis `48c`); Sondenmenge auf `6 und 18 bis 48` an allen drei Stellen
- [x] `governance/DECISION_LOG.md`: **D-128** neu, **`K-52`** neu
- [x] `docs/ROADMAP.md`: Releaseplanzeile `0.57.0` als erledigt, Frist der `build/`-Ausnahme
      an `AP11` vermerkt, Abschnitt zu 0.57.0
- [x] `VERSION` auf `0.57.0`; CHANGELOG-Eintrag
- [x] Validator ohne Fehler; Sondenlauf in beiden Kodierungsumgebungen
- [x] **Dokumentation:** `tests/protocols/2026-09-18-wirkungsnachweise-0.57.0.md`
- [ ] **Zur Entscheidung offen:** `K-52` (Produktnamen im Kern), `K-37` (Versionszelle der
      Vorlagen)

## 10. Abnahme

- `validate-framework.py --root .`: 0 Fehler, 0 Warnungen
- `probe-pruefungen.py .` in beiden Kodierungsumgebungen: alle Ergebniszeilen bestanden
- **Gegenbeweis gegen den unberührten Vorstand:** der neue Validator gegen `0.56.2`
  (`git archive e9f4367`, Installation mit dem `install.py` des Vorstands) meldet **genau
  17 Fundstellen in genau 14 Trägern** – die Aufzählung dieses Antrags, ohne Rest und ohne
  Überschuss
- Kriterium 2 unverändert **105**, Kriterium 1 unverändert **23** – dieses Release bewegt
  keine Zahl von D-11 und sagt es
- Protokoll: `tests/protocols/2026-09-18-wirkungsnachweise-0.57.0.md`
