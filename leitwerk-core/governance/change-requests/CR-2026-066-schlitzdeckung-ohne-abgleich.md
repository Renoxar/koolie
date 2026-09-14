# Änderungsantrag `CR-2026-066`

| Feld | Inhalt |
|---|---|
| Titel | Drei offene Platzhalterschlitze decken drei beliebige Befehlsfreigaben – und drei ausgelieferte Texte bestreiten das ohne Einschränkung |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-14 |
| Betroffene Artefakte | `tests/scripts/validate-framework.py` (Prüfung 42 neu, Korbzerlegung an **eine** Stelle, Register), `tests/scripts/probe-pruefungen.py` (Sonden und Gegenproben, Kopfsatz), `clientmap.py` (Kommentarkopf jeder erzeugten Berechtigungsdatei), `framework/core/03-security.md`, `templates/project-overlay/OVERLAY.md` Abschnitt 6, `tests/TEST_CATALOG.md` (`FW-KO-01`), `governance/DECISION_LOG.md`, `docs/ROADMAP.md`, `CHANGELOG.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – die Durchsetzungsschicht und ihre Prüfung sind Framework-Gut |
| Art | Änderung; Anlass ist **Kandidat 2** der Übergabe, der einzige mit einer gemessenen Fundstelle |
| Dringlichkeit | **P1.** Gemessen läuft eine Freigabe für einen Befehl **mit Fernwirkung** in beiden Packs lautlos durch, und der Text, der das bestreitet, steht im Kopf genau der Datei, in der jemand die Zeile einträgt |

## 1. Anlass

Kandidat 2 der Übergabe beschrieb den Befund als Formfrage: Am Piloten trug die
Berechtigungsdatei `Bash(mvn -B test:*)`, während Abschnitt 6 des Overlays `mvn -B test`
erklärt – gefangen hat es Prüfung 37, weil die Abweichung **zufällig auch formal auffällig**
war. Die Gegenprüfung liegt vor:
`tests/protocols/2026-09-14-gegenpruefung-schlitzdeckung.md`, **zwölf Läufe an zwei Packs**
(vier Kontroll-, zwei Entlastungsläufe) und **vier Abzählungen**.

**Der Befund bestätigt sich und er liegt woanders.**

### 1.1 Befund 1: Die Deckung ist drei, und sie ist beliebig füllbar

Die Kernquelle hält im `ask`-Korb genau **drei** Befehlsschlitze (`<BUILD_COMMAND>`,
`<TEST_COMMAND>`, `<LINT_COMMAND>`); die vier Pfadschlitze stehen im `deny`-Korb und decken
nichts, weil Überzähliges dort ohnehin zulässig ist. Prüfung 37 vergleicht **Mengen**: Sie
zählt den Überschuss gegen die Zahl der offenen Schlitze. **Welcher Eintrag welcher Schlitz
ist, steht dort nicht – und kann dort nicht stehen.**

Gemessen (M10, frische `devin-desktop`-Installation): Das Overlay erklärt dreimal `<TBD>` –
also **gar nichts** –, und drei eingetragene Befehlsfreigaben laufen durch, darunter
`mvn -B deploy`. Derselbe Befund am Piloten mit `claude-code` (M4). **Die vierte Zeile fällt**
(M5, M11) – D-76 hat das richtig vorhergesagt.

### 1.2 Befund 2: Die Lücke ist erklärt – aber nur an einer Stelle

`CR-2026-061` Abschnitt 4 nennt genau diesen Fall und nimmt ihn ausdrücklich aus:

> „Der zweite dort benannte Posten – ein belegter `<LINT_COMMAND>`, obwohl das Overlay
> ‚Lint: nicht vorhanden' sagt – bleibt **unbeanstandet**; ein gefüllter Schlitz ist ein
> gefüllter Schlitz, und den Abgleich mit dem Overlaytext leistet diese Prüfung nicht."

Auch D-76 und D-77 bleiben genau. **Drei ausgelieferte Texte aus demselben Commit
(`34d850e`, Release 0.39.0) tun es nicht:**

| # | Träger | Wortlaut (verkürzt) |
|---|---|---|
| **Z1** | `templates/project-overlay/OVERLAY.md` Abschnitt 6 | „Ein Eintrag von Hand in `<PERMISSIONS_FILE>` ist **kein** Ersatz: Prüfung 37 des Validators meldet ihn als Ausweitung" |
| **Z2** | `clientmap.py`, Kommentarkopf **jeder erzeugten Berechtigungsdatei** | „… unter ‚ask' und ‚allow' wäre sie eine Ausweitung **und ist ein Fehler**. Ein zusätzlicher freigegebener Befehl gehört deshalb nicht hierher" |
| **Z3** | `framework/core/03-security.md` | „**Prüfung 37 hält die installierte Datei gegen die Kernquelle:** Was dort erzeugt wird, muss hier stehen; eine zusätzliche Regel ist nur unter `deny` zulässig" |

**Z2 ist die teuerste.** Sie steht nicht in einem Dokument, das man zum Nachschlagen
aufschlägt, sondern im Kopf der Datei, in der jemand die Zeile einträgt, über die sie eine
Aussage macht. Wer dort „ist ein Fehler" liest, die Zeile trotzdem einträgt und einen grünen
Lauf bekommt, liest den grünen Lauf als Bestätigung.

**Die Lehre ist die von 0.42.0, eine Ebene tiefer:** *Eine Enthaltung, die nur in einem Antrag
steht, hält nicht einmal bis zum Ende desselben Patches.*

### 1.3 Befund 3 – nicht gesucht: Zwei von drei Trägern sagen längst das Richtige

Je Installation führen **drei** Träger dieselben drei Werte: das Quell-Overlay, die
Laufzeitfassung `20-project-overlay.md` und die Berechtigungsdatei. Am Piloten sagen
Quell-Overlay **und** Laufzeitfassung „Lint/Statische Analyse: nicht vorhanden"; allein die
Berechtigungsdatei gewährt einen dritten Befehl. **Das ist die erste gemessene Fundstelle für
`CR-2026-044` E4** (Abgleich Quell-Overlay gegen Laufzeitfassung, seit 0.33.0 offen), und sie
fällt zugunsten der beiden Textträger aus.

### 1.4 Befund 4 – nicht gesucht: Die Zuordnung steht maschinenlesbar da

In **allen vier** geprüften Overlays – Vorlage, Pilot, frische Installation,
Testinstallation im Repositorium – steht jeder der drei Platzhalter in **genau einer**
Tabellenzeile, und der Wert steht in der Zelle **rechts daneben**. Das gilt auch für den
Piloten, dessen Abschnitt 6 aus einer älteren Vorlage stammt und eine andere
Spaltenüberschrift führt. Und `docs/PLACEHOLDER_REGISTRY.md` weist die Herkunft für alle drei
längst aus: „Overlay 5" beziehungsweise „Overlay 6".

**Das Register behauptet die Zuordnung seit jeher. Durchgesetzt hat sie niemand.**

## 2. Vorgeschlagene Änderung

1. **Prüfung 42 (neu)** – *Ein gefüllter Schlitz trägt, was das Overlay erklärt.* Je
   Befehlsplatzhalter der Kernquelle wird der Wert aus `project-overlay/OVERLAY.md` gelesen
   (über die **Platzhalterzelle**, nicht über die Spaltenposition) und gegen die installierte
   Berechtigungsdatei gehalten:
   - Das Overlay erklärt einen Befehl → die Datei **muss** die Schlitzregel mit genau diesem
     Wert tragen.
   - Das Overlay erklärt keinen (`<TBD>`, „nicht vorhanden", „–", leer) → der Schlitz ist
     **nicht gefüllt** und deckt **keinen** Überschuss.
   - Eine Befehlsregel im Schlitzkorb, die keinen erklärten Wert trägt und die die Kernquelle
     nicht erzeugt, ist ein Fehler.
2. **Die Korbzerlegung liegt künftig an einer Stelle.** `_korb_zerlegung()` liefert Pflicht,
   Schlitze, offene Schlitze und Überschuss; Prüfung 37 und 42 lesen daraus. **Zwei
   Gelegenheiten für denselben Fehler sind eine** – dieselbe Begründung wie bei
   `tabellenzellen()` mit 0.37.0.
3. **Prüfung 37 bleibt unverändert.** Sie hängt allein an der Kernquelle und läuft ohne
   Overlay; 42 entzieht ihr keine Deckung, sondern prüft die Zuordnung getrennt. Sonst hinge
   das Ergebnis von 37 an der Anwesenheit eines Nachbardokuments.
4. **Z1, Z2 und Z3 bekommen ihre Bedingung** – Z2 zuerst, weil sie in jeder erzeugten Datei
   steht. Der Satz nennt künftig beides: den Schlitz, der dem Projekt gehört, und die
   Grenze, die auch nach Prüfung 42 bleibt.
5. **Register und Sondenmenge** werden nachgezogen: Registereintrag 42, Spanne „6 und 18 bis
   42" wörtlich an den drei Trägern, die Prüfung 40 vergleicht.
6. **Sonden und Gegenproben** zu Prüfung 42 gegen eine **frische Installation** mit
   gefülltem Overlay – die Bauart von Prüfung 37 und 33, aus demselben Grund: Die Prüfung
   hängt an installierten Dateien, nicht an einem Repositoriumstext.

## 3. Auswirkungen

- **Der Pilot bekommt einen Fehler.** `Bash(mvn -B -q compile)` steht dort, während Abschnitt 6
  `<LINT_COMMAND>` als „nicht vorhanden" erklärt. **Das ist der Zweck der Prüfung** und kein
  Nebenschaden. Die Behebung ist eine Entscheidung des Overlay Owners und keine des Frameworks:
  entweder die Zeile fällt, oder Abschnitt 6 erklärt den Befehl als `<LINT_COMMAND>`.
- **Der Gegenbeweis gegen den Vorstand ist ein Abzählen an einem echten Projekt**, nicht eine
  Konstruktion: Der Befund stand am Piloten, bevor die Prüfung gebaut wurde, und sie findet
  ihn. **Im Repositorium selbst findet sie nichts** – die Testinstallation hat drei offene
  Schlitze und ein Overlay, das dreimal `<TBD>` sagt. Das gehört so gesagt.
- **Ein Projekt, das seine Schlitze sauber füllt, merkt nichts.** Die Deckung entsteht genau
  dort, wo ein Projekt einen Befehl **nicht** hat und die freigewordene Zeile anderweitig
  benutzt.
- **Die Prüfung hängt an einer Tabellenform, die dem Projekt gehört.** Wer Abschnitt 5 oder 6
  so umbaut, dass ein Platzhalter in keiner Tabellenzeile mehr steht, bekommt die Meldung über
  den verlorenen Anker – nicht über seine Berechtigungsdatei.
- **Bestehende Installationen ändern sich nicht von selbst.** Die Berechtigungsdatei steht in
  `shared_seed` und wird nach der Erstinstallation nie wieder geschrieben (D-76); die Prüfung
  meldet, sie behebt nicht.

## 4. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | **Darf eine Prüfung einen Wert aus dem Overlaytext auswerten?** Bisher liest der Validator dort nur Zustände – Status, offene `<TBD>`, Versionsangabe | **Ja, über die Platzhalterzelle der Tabellen in Abschnitt 5 und 6.** Die Zuordnung gibt es genau einmal, und `docs/PLACEHOLDER_REGISTRY.md` weist sie für alle drei Platzhalter längst aus. Sie dort zu lesen ist keine neue Freiheit, sondern die Durchsetzung einer Behauptung, die das Register seit jeher macht. Gemessen steht jeder Platzhalter in allen vier geprüften Overlays in **genau einer** Tabellenzeile | **Die Prüfung hängt an einem Dokument, das dem Projekt gehört.** Ein Umbau von Abschnitt 5 oder 6 bricht sie – deshalb wird die Zeile über die **Platzhalterzelle** gefunden und der Wert rechts daneben gelesen, nie über eine Spaltennummer. Und der Bruch meldet sich als **verlorener Anker**, nicht als Befund über die Berechtigungsdatei |
| **E2** | Wird stattdessen die **Laufzeitfassung** `20-project-overlay.md` gelesen? Sie ist Framework-Gut und führt dieselben drei Werte | **Nein.** Sie führt sie in einer Fließzeile ohne Schlüsselspalte – und der Pilot hat sie bereits umgebaut (zwei Zeilen statt einer, ein zusätzliches Feld „Schnellprüfung"). Eine Prüfung darüber fiele beim ersten echten Projekt **an der Form, nicht an der Sache** | **Der Abgleich zwischen Quell-Overlay und Laufzeitfassung bleibt offen** (`CR-2026-044` E4, seit 0.33.0). Er hat jetzt seine erste gemessene Fundstelle und bekommt sie als Kandidaten – **das ist eine Enthaltung, und sie wird als solche geführt** |
| **E3** | Was gilt, wenn der Overlaywert **kein Befehl** ist (`<TBD>`, „nicht vorhanden", „–")? | **Der Schlitz gilt als nicht gefüllt und deckt keinen Überschuss.** Das ist der Satz, der den Befund am Piloten fängt: Wo ein Projekt keinen Befehl hat, darf die freigewordene Zeile nicht anderweitig benutzt werden | **Das ist eine Verschärfung gegenüber 0.43.0.** Ein Projekt, das den Befehl in der Datei führt und im Overlay `<TBD>` stehen lässt, bekommt jetzt einen Fehler – auch wenn der Befehl harmlos ist. Der dokumentierte Weg ist, Abschnitt 6 auszufüllen |
| **E4** | Was gilt, wenn das Overlay einen Befehl erklärt, die Datei ihn aber **nicht** trägt? | **Fehler**, mit einer Meldung, die beide Auflösungen nennt. Nach D-77 („Fehlen ist immer ein Fehler, gleich in welchem Korb") ist das die konsequente Fortsetzung; die beiden Träger müssen übereinstimmen | **Eine frische Installation vor dem Ausfüllen bleibt still**, weil dort `<TBD>` steht – der Fehler trifft nur ein Overlay, das bereits etwas erklärt. **Das ist gewollt, aber es heißt auch: Der halb ausgefüllte Zustand wird erst dann laut, wenn er halb ist** |
| **E5** | **Nur die drei Befehlsschlitze – oder auch die vier Pfadschlitze?** | **Nur die drei Befehlsschlitze.** Die Pfadschlitze stehen sämtlich im `deny`-Korb, wo Überzähliges ohnehin zulässig ist; dort gibt es keine Deckung zu entziehen. Und sie sind **n:1** – eine Liste im Overlay, eine Regel in der Datei | **Ein zu eng gefüllter `<EXCLUDED_PATHS>`-Schlitz bleibt eine stille Lockerung.** Das ist eine andere Prüfung mit einer eigenen Ermessensfrage, und sie wird **nicht** in einem Nebensatz erledigt. Sie wird als Kandidat geführt – die Lehre von 0.43.0: eine Enthaltung erklärt sich oder sie ist eine Behauptung |
| **E6** | Eigene Nummer oder Erweiterung von Prüfung 37? | **Eigene Nummer, Prüfung 42.** Prüfung 37 hängt allein an der Kernquelle und läuft ohne Overlay; 42 enthält sich ohne Overlay. Zwei Gegenstände, zwei Nummern – und 37 behält ihre Arithmetik, damit ihr Ergebnis nicht von der Anwesenheit eines Nachbardokuments abhängt | **Am Piloten meldet 37 weiterhin nichts**, während 42 meldet. Zwei Prüfungen über dieselbe Datei, die verschieden ausgehen, sind erklärungsbedürftig – der Registereintrag sagt deshalb, was jede von beiden **nicht** prüft |
| **E7** | Werden Z1 bis Z3 berichtigt, obwohl Prüfung 42 sie einholt? | **Ja, alle drei.** Sie sagen auch nach 42 mehr, als die Mechanik hält: Die Pfadschlitze bleiben ungeprüft, und ein vom Overlay erklärter Befehl ist zulässig. **Z2 zuerst** – sie ist die einzige der drei, die den Leser an der Stelle erreicht, an der er eingreift | **Drei Sätze werden länger**, und zwei davon stehen in Texten, die ohnehin dicht sind. Der Preis ist Lesbarkeit gegen Wahrheit – und dieses Projekt hat die Frage schon entschieden |
| **E8** | Eigenes Release oder Anhang? | **Ein eigenes Release, `0.44.0`.** Der Gegenstand ist geschlossen, und er trägt einen Migrationshinweis für jede Installation mit gefülltem Overlay | **Das neunzehnte Release in drei Tagen** – und das erste seit 0.42.0, dessen Gegenbeweis ein **Abzählen an einem echten Projekt** ist statt einer Konstruktion |

## 5. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle acht Fragen wie vorgelegt.** E1 der Wert wird über die Platzhalterzelle gelesen; E2 die Laufzeitfassung bleibt außen vor und `CR-2026-044` E4 wird als Kandidat geführt; E3 ein Schlitz ohne Befehl deckt nichts; E4 ein erklärter Befehl muss dastehen; E5 nur die drei Befehlsschlitze, die Pfadschlitze werden als Enthaltung geführt; E6 eigene Nummer 42, Prüfung 37 unverändert; E7 alle drei Texte bekommen ihre Bedingung; E8 eigenes Release `0.44.0` |
| Datum | 2026-09-14 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | D-90 (ein Platzhalterschlitz trägt den Wert, den das Overlay für ihn erklärt – ein Schlitz ohne erklärten Befehl deckt keinen Überschuss), D-91 (der Validator darf **Werte** aus `OVERLAY.md` auswerten, wenn sie in einer Schlüsselspalte stehen – nicht aus Fließtext) |
| Auflagen | **Der Gegenbeweis wird als Abzählen an einem echten Projekt ausgewiesen und im selben Atemzug seine Grenze:** Im Repositorium selbst findet Prüfung 42 nichts, weil die Testinstallation drei offene Schlitze und ein leeres Overlay hat. **Und die Enthaltung zu den Pfadschlitzen steht im Registereintrag, nicht nur im Antrag** – genau der Fehler, den dieser Antrag behebt, darf ihn nicht selbst wiederholen |
| Ziel-Release | `0.44.0` |
| Umsetzung | umgesetzt mit `0.44.0` |
