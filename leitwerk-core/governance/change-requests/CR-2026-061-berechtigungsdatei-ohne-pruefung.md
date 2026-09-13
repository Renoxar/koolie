# Änderungsantrag `CR-2026-061`

| Feld | Inhalt |
|---|---|
| Titel | Die Berechtigungsdatei nach der Installation – eine Erweiterung, die es nicht gibt, und fünfzig Regeln, die niemand nachzählt |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-13 |
| Betroffene Artefakte | `tests/scripts/validate-framework.py` (Prüfung 37 neu), `clientmap.py` (neue öffentliche Funktion `basket_rules`, berichtigter Kommentarkopf), `tests/scripts/probe-pruefungen.py` (Sonden und Gegenprobe zu 37), `framework/core/03-security.md` (Abschnitt 4), `templates/project-overlay/OVERLAY.md` (Abschnitt 6), `governance/DECISION_LOG.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – die Berechtigungspolitik ist normativ (`03-security.md` Abschnitt 4), die Prüfung ist Framework-Gut |
| Art | Änderung; erledigt die beiden Framework-Lücken, die der Pilot sichtbar gemacht hat, und den dritten Ablehnungsgrund von `CR-OTP-G-001` |
| Dringlichkeit | **P1.** Anders als die letzten vier Releases betrifft dieser Antrag eine Zusage **gegenüber einem Projekt**: Die Berechtigungsdatei ist der Träger der Kernzusagen B1 bis B6, und außerhalb ihrer dreizehn Kernregeln prüft sie nichts |

## 1. Anlass

Zwei Punkte stehen als **Kandidat 1 und 2** in der Übergabe. Sie sind beide am Piloten
aufgefallen, und sie sind zusammen der **dritte Ablehnungsgrund** von `CR-OTP-G-001`
(„Es gibt keine geprüfte Änderungsschicht für diese Datei").

**Beide sind gegengeprüft** (`tests/protocols/2026-09-13-gegenpruefung-berechtigungsdatei.md`,
zwölf Messungen an einer frischen `claude-code`-Installation, davon zwei Gegenproben).
**Beide bestätigen sich, und beide sind erheblich größer als die Übergabe sagt.**

### 1.1 Befund 1: Geprüft werden dreizehn von fünfundsechzig Regeln

Die erzeugte Datei trägt 54 `deny`-, 5 `ask`- und 6 `allow`-Regeln. Der Validator kennt davon
die **dreizehn** Kernregeln aus `_core_rules_integrity.deny_must_contain`. Gemessen:

| Eingriff | Validator |
|---|---|
| `ask` um `Bash(docker run --rm --network none:*)` ergänzt | **0 Fehler** |
| `allow` um `Bash(docker run:*)` ergänzt | **0 Fehler** |
| `Bash(curl:*)` aus `deny` gelöscht | **0 Fehler** |
| **alle 41** Nicht-Kernregeln aus `deny` gelöscht | **0 Fehler** |
| `Bash(kubectl:*)` → `Bash(kubectl delete:*)` verengt | **0 Fehler** |
| `Bash(<TEST_COMMAND>)` → `Bash(mvn -B test:*)` (der Fall des Piloten) | **0 Fehler** |
| `ask`-Korb geleert, `Edit(**)` und `mcp__*` verschwinden mit | **0 Fehler** |
| *Gegenprobe:* Kernregel gelöscht | **1 Fehler** |
| *Gegenprobe:* Kernregel in `allow` | **2 Fehler** |

**Die Übergabe nennt den `ask`-Korb. Gemessen ist es der ganze Rest der Datei.** Ein Projekt
kann `curl`, `wget`, `ssh`, `scp`, `kubectl`, `helm`, `terraform`, `npm publish`, `docker push`,
`git rebase`, `git tag`, `git clean`, `git remote`, `chmod`, sämtliche Lockfile-Sperren und zehn
der fünfzehn Secret-Lesesperren streichen, und der Lauf bleibt grün.

**`install.py` greift es ebenfalls nicht auf:** `--update` rührt die Datei nicht an (sie steht in
`shared_seed`, mit Hinweis in der Ausgabe), und `--check` **nennt sie nicht einmal**.

### 1.2 Befund 2: Es gibt keine Overlay-Erweiterung – und drei Texte sagen etwas anderes

`render_permissions` überschreibt die drei Körbe vollständig aus der Kernquelle;
`permissions_extra` ist eine **Manifest**-Angabe, also Ebene 3. **Eine Quelle des Projekts liest
diese Funktion nicht.** Der einzige Weg eines Projekts in die Datei ist der Platzhalter, und für
Befehle gibt es drei.

Drei Texte behaupten mehr:

| | Stelle | Wortlaut |
|---|---|---|
| **T1** | `clientmap.py` Zeile 182, Kommentarkopf **jeder** erzeugten Datei | „Berechtigungsvorlage des Frameworks (**Ebene 3 + Overlay-Erweiterungen**)" – die Wendung bezeichnet im Repositorium sonst die Regeldateien `2N-*`, nicht gefüllte Platzhalter |
| **T2** | `templates/project-overlay/OVERLAY.md` Abschnitt 6 | Eine Tabelle mit **sechs** Zeilen unter der Spaltenüberschrift „Freigabestufe in `<PERMISSIONS_FILE>`". **Zwei** Zeilen tragen einen Platzhalter, **vier** nicht – und für die vier gibt es keinen Weg in die Datei |
| **T3** | `framework/core/03-security.md` Zeile 52, Abschnitt 4 (**normativ**) | „ask (**KANN im Overlay für Stufe niedrig auf allow gesetzt werden**)" – **drei Zeilen unter derselben Tabelle** steht: „Änderungen an der Regelmenge erfolgen ausschließlich über Änderungsantrag (V10)" |

**T3 ist die Bauform, die dieses Projekt zum dritten Mal findet:** *die Zusage, deren Widerlegung
im eigenen Dokument steht.* Bei B11 war es „Ausnahmen je Domain" und fünf Zeilen darunter „`deny`
gewinnt immer"; das wurde mit 0.32.0 berichtigt. **Die Zeile darüber blieb stehen** und macht
dieselbe Aussage über dieselbe Datei.

### 1.3 Zwei Entlastungen – sie gehören dazu, weil die Ähnlichkeit trügt

**Die MCP-Zeile ist *nicht* derselbe Fehler.** `03-security.md` führt „`mcp__*` | ask; Freigaben
je Server im Overlay". Das sieht aus wie T3 und ist in Ordnung: Die Freigabe läuft über
`<MCP_FILE>`, nicht über die Berechtigungsdatei, und `OVERLAY.md` Zeile 173 sagt es ausdrücklich
(„Eintrag in `<MCP_FILE>` erst nach Freigabe; **Standard ask**"). **Wer T3 behebt, darf diese
Zeile nicht mitnehmen.**

**Der Regelweg für weitere Befehle trägt bereits.** `05-working-model.md` Abschnitt 3.2 und
`root-instruction.md` Abschnitt 7 sagen: „Führe nur Befehle aus, die im Overlay freigegeben sind
(… **weitere gemäß Overlay Abschnitt 6**)." **Diese beiden Sätze sind richtig** – sie sind eine
Anweisung an den KI-Client, kein Versprechen über eine Datei, genau wie die M3-Regel zu
Hintergrund-Subagenten (D-66). **Der Kanal existiert also; er ist die Regelschicht.** Falsch ist
allein die Behauptung, der Befehl stehe danach in der Berechtigungsdatei.

## 2. Warum eine `ask`-Zeile eine Ausweitung ist

Gegen die Behandlung einer ergänzten `ask`-Zeile als Ausweitung lässt sich einwenden: `ask` heißt
Rückfrage, und ein nicht gelisteter Befehl führt beim ausgelieferten `defaultMode` ebenfalls zu
einer Rückfrage; mechanisch ändere die Zeile also nichts.

**Der Einwand trägt nicht, und zwar unabhängig davon, ob er stimmt.** Was die Zeile ändert, ist
nicht der Mechanismus, sondern die **Erklärung**: Nach `05-working-model.md` Abschnitt 3.2 führt
der KI-Client *nur* Befehle aus, die im Overlay als freigegeben gelistet sind. Eine Zeile im
`ask`-Korb erklärt einen Befehl für freigegeben. **Genau daran ist `CR-OTP-G-001` gescheitert** –
nicht daran, dass `docker run` ohne Rückfrage liefe.

Dieser Antrag stützt sich deshalb auf **keine** gemessene Clientwirkung des `ask`-Korbs und
behauptet keine.

## 3. Vorgeschlagene Änderung

1. **Prüfung 37 (neu)** in `check_config`: Die drei Körbe der installierten Datei werden gegen
   die aus `framework/runtime/permissions.json` und dem Manifest **erzeugte** Regelmenge gehalten.
   Zwei Sätze, keine Ausnahmen:
   - **Fehlt eine erzeugte Regel, ist es ein Fehler** – in jedem Korb.
   - **Steht eine Regel zu viel, entscheidet der Korb:** in `deny` zulässig (Verschärfung), in
     `ask` und `allow` ein Fehler (Ausweitung) – **abzüglich der Platzhalterschlitze**, die das
     Projekt gefüllt hat.
2. **Der gefüllte Befehlsschlitz darf das Präfixzeichen des Clients nicht tragen.**
   `clientmap._befehl` hängt es bei einem offenen Projektplatzhalter ausdrücklich **nicht** an,
   mit Begründung im Code. Wer es von Hand nachträgt, macht aus der Freigabe eines Befehls die
   Freigabe einer Befehlsfamilie. Gilt nur bei `permission_exec_match: prefix`.
3. **`clientmap.basket_rules(quelle, man, korb)`** wird öffentlich – dieselbe Bauart wie
   `core_rules`, damit die Prüfung nicht auf eine private Funktion greift.
4. **T1 berichtigt:** Der Kommentarkopf sagt „Ebene 3"; was dem Projekt gehört, steht zwei Sätze
   weiter unten ohnehin schon („Platzhalter in spitzen Klammern trägt der Overlay Owner hier
   ein – das ist der einzige Teil dieser Datei, der dem Projekt gehört").
5. **T2 berichtigt:** Die Spalte in `OVERLAY.md` Abschnitt 6 sagt je Zeile die Wahrheit – die
   vier Zeilen ohne Platzhalter tragen „nur Regelschicht (Abschnitt 6), kein Eintrag in
   `<PERMISSIONS_FILE>`". Ein Satz unter der Tabelle erklärt den Unterschied.
6. **T3 berichtigt:** Der Zusatz „KANN im Overlay für Stufe niedrig auf allow gesetzt werden"
   entfällt in `03-security.md` **und** in `OVERLAY.md` Abschnitt 6 Zeile 1.
7. **Sonden und Gegenprobe** zu Prüfung 37 gegen eine **frische Installation** – die Bauart von
   Prüfung 33, aus demselben Grund: Die Prüfung hängt an einer installierten Datei, nicht an
   einem Repositoriumstext.

## 4. Auswirkungen

- **Der Pilot bekommt einen Fehler.** `Bash(mvn -B test:*)` steht dort seit dem Heben auf 0.37.0.
  **Das ist der Zweck der Prüfung** und kein Nebenschaden: Die Zeile ist genau die stille
  Ausweitung, die Kandidat 2 beschreibt. Der zweite dort benannte Posten – ein belegter
  `<LINT_COMMAND>`, obwohl das Overlay „Lint: nicht vorhanden" sagt – bleibt **unbeanstandet**;
  ein gefüllter Schlitz ist ein gefüllter Schlitz, und den Abgleich mit dem Overlaytext leistet
  diese Prüfung nicht.
- **Ein Projekt, das eine `allow`-Regel absichtlich streicht, bekommt jetzt einen Fehler.** Das
  Streichen ist eine Verschärfung und damit sachlich zulässig – aber `03-security.md` Abschnitt 4
  sagt normativ zu, dass die Regel dasteht. Der Weg dahin ist der Ausnahmeprozess, nicht die
  stille Kürzung.
- **Bei `devin-desktop` wirkt Punkt 2 nicht** (`permission_exec_match: literal`). Die Prüfung
  läuft dort, der Präfixteil greift nicht – und das ist keine Lücke, sondern die Abwesenheit
  ihres Gegenstands.
- **Prüfung 37 fängt gegen den unmittelbaren Vorstand nichts**, weil die erzeugte Datei per
  Konstruktion zu sich selbst passt. **Ihr Gegenbeweis ist deshalb eine Konstruktion und kein
  Abzählen** – die neun Eingriffe aus 1.1, gegen 0.38.0 sämtlich stumm. Das gehört so in den
  Wirkungsnachweis, mit derselben Ehrlichkeit wie bei Prüfung 35 und 36.
- **`CR-OTP-G-001` bleibt abgelehnt.** Dieser Antrag beseitigt seinen dritten Ablehnungsgrund
  nicht, sondern **bestätigt ihn**: Es gibt keine Änderungsschicht, und es soll keine geben. Die
  Ersatzwege (A) und (B) seines Abschnitts 6.3 bleiben die einzigen.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | Bekommt ein Overlay eine ausgewiesene Erweiterungsschicht für die Berechtigungsdatei – oder wird die Grenze bestätigt? | **Grenze bestätigen.** Drei Gründe, jeder für sich tragend: (1) **Der Kanal existiert bereits** – „weitere gemäß Overlay Abschnitt 6" ist eine Anweisung an den Client, und sie ist richtig formuliert (1.3). (2) **Eine Erweiterung wäre nicht haltbar:** Die Datei steht in `shared_seed`, `--update` fasst sie nie an; eine nur bei der Installation gelesene Erweiterungsquelle wäre eine Zusage, die beim ersten Releasewechsel bricht. (3) **Das Verschärfungsprinzip verbietet sie:** Jede zusätzliche `ask`-Zeile für einen Befehl ist eine Ausweitung der Erklärung (Abschnitt 2) | **Ein Projekt mit mehr als drei Befehlen behält sie nur in der Regelschicht.** Wer die Berechtigungsdatei liest, sieht sie dort nicht – und das ist eine Unvollständigkeit, die man aushalten muss. **Die Gegenposition ist ernst zu nehmen:** Eine geprüfte Erweiterung, die *ausschließlich* `ask` befüllen und `deny` nie anfassen dürfte, wäre mechanisch möglich. Sie scheitert an (2), nicht an (3) – und an (2) scheitert sie vollständig |
| **E2** | Entsteht Prüfung 37, und wie scharf? | **Ja, in zwei Sätzen: Fehlen ist immer ein Fehler; Überzähliges ist in `deny` zulässig und in `ask`/`allow` ein Fehler.** Das ist das Verschärfungsprinzip, mechanisch angewandt – nicht eine dritte Regel neben ihm. **Die Alternative, `deny_must_contain` einfach auf alle 54 Regeln zu erweitern, wäre zu wenig:** Sie fängt M3 bis M5, aber weder die ergänzte `allow`-Zeile noch den geleerten `ask`-Korb | **Ein Projekt, das eine `allow`-Regel streicht, bekommt einen Fehler für eine Verschärfung.** Das ist gewollt (Abschnitt 4), aber es ist ein Preis: Die Prüfung ist an dieser Stelle strenger als das Prinzip, auf das sie sich beruft. **Und sie prüft die Form, nicht den Sinn** – ein Schlitz, der mit einem unsinnigen Befehl gefüllt ist, besteht sie |
| **E3** | Wird ein gefüllter Befehlsschlitz auf das Präfixzeichen geprüft? | **Ja.** Die Abbildung lässt es bewusst weg und schreibt den Grund daneben; ein von Hand nachgetragenes `:*` hebelt genau diese Entscheidung aus. **Am Piloten steht es bereits** – das ist kein hypothetischer Fall | **Ein Projekt, das wirklich eine Befehlsfamilie freigeben will, kann es nicht mehr still tun** und braucht einen Änderungsantrag. Das ist der Zweck. **Bei `devin-desktop` greift der Teil nicht**, weil der Client Befehle wörtlich sperrt – die Prüfung ist dort um diesen Gegenstand ärmer, und das gehört gesagt statt verschwiegen |
| **E4** | Was geschieht mit T1, T2 und T3? | **Alle drei berichtigen, T3 durch Streichung.** Die Freigabestufe je Kontrollstufe im Overlay zu verankern, wäre die Alternative – sie scheitert daran, dass die Fußnote derselben Tabelle sie bereits verbietet (V10). **Eine Zusage, die im eigenen Dokument widerlegt wird, wird nicht durch Mechanik gerettet, sondern gestrichen** – so ist B11 entschieden worden | **Eine dokumentierte Freiheit entfällt.** Wer sie gebraucht hat, merkt es erst jetzt – aber sie war nie ausführbar: Eine so gesetzte `allow`-Zeile wäre nach E2 ab sofort ein Fehler. **Der Preis ist also nicht der Verlust, sondern das Eingeständnis**, dass sie zwölf Releases lang unausführbar dastand |
| **E5** | Läuft Prüfung 37 im Normallauf oder nur unter `--strict-overlay`? | **Im Normallauf.** Sie trägt die Kernzusagen B1 bis B6, wie `deny_must_contain` daneben. Der Auslieferungszustand mit offenen Platzhaltern besteht sie – ein noch nicht gefüllter Schlitz ist ein Schlitz | **Jeder Lauf jedes Projekts fährt sie mit.** Kostet Laufzeit (einmal rendern) und macht den Normallauf strenger, ohne dass jemand es bestellt hat. **Das ist bei einer Kernzusage die richtige Seite des Irrtums** |
| **E6** | Ein eigenes Release oder Anhang an das nächste? | **Ein eigenes Release, `0.39.0`.** Der Gegenstand ist geschlossen, er ist P1, und er ist der erste seit vier Releases, der eine Zusage gegenüber einem **Projekt** betrifft statt eines Prüfwerkzeugs | **Das vierzehnte Release in zwei Tagen.** Und wieder ist kein Ergebnis eine Messung am Client – gemessen ist der Validator, nicht die Wirkung der Datei |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle sechs Fragen wie vorgelegt.** E1 die Grenze wird bestätigt, es entsteht keine Erweiterungsschicht; E2 Prüfung 37 in zwei Sätzen; E3 der Präfixteil, mit benannter Lücke bei `devin-desktop`; E4 T1 bis T3 berichtigt, T3 durch Streichung, die MCP-Zeile ausdrücklich nicht; E5 Normallauf; E6 eigenes Release `0.39.0` |
| Datum | 2026-09-13 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | D-76 (ein Overlay erweitert die Berechtigungsdatei nicht – der Kanal für weitere Befehle ist die Regelschicht), D-77 (die Körbe werden gegen die Kernquelle geprüft: Fehlen ist immer ein Fehler, Überzähliges nur in `ask` und `allow`) |
| Auflagen | **Der Gegenbeweis wird als Konstruktion ausgewiesen, nicht als Abzählen** – Prüfung 37 findet gegen 0.38.0 nichts, weil die erzeugte Datei zu sich selbst passt; ihr Wert hängt allein an den Sonden. **Der Befund am Piloten wird gemeldet, nicht behoben** – die Datei dort ist untracked und gehört dem Piloten. **Und die MCP-Zeile bleibt unberührt**; sie ist der Entlastungsbefund dieser Gegenprüfung, und wer sie mitstreicht, zerstört einen stimmigen Mechanismus |
| Ziel-Release | `0.39.0` |
| Umsetzung | umgesetzt mit `0.39.0` |
