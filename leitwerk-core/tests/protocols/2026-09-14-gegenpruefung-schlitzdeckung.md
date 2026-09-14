# Gegenprüfung: Drei offene Schlitze decken drei Befehlsfreigaben – und drei Texte sagen das Gegenteil

| Feld | Wert |
|---|---|
| Gegenstand | Kandidat 2 der Übergabe: der Abgleich zwischen Overlaytext und Berechtigungsdatei. Prüfung 37 zählt die Platzhalterschlitze des `ask`-Korbes, vergleicht aber ihren **Inhalt** mit nichts. Am Piloten steht `Bash(mvn -B -q compile)` im `ask`-Korb, während Abschnitt 6 des Overlays `<LINT_COMMAND>` als „nicht vorhanden" erklärt |
| Anlass | Kandidat 2 war der einzige Kandidat der Übergabe mit einer gemessenen Fundstelle statt einer Vermutung. Nach D-23 gehört er vor der Umsetzung gegengeprüft |
| Datum | 2026-09-14 |
| Framework-Version | 0.43.0 (Auscheckstand `c0f15a9`, Arbeitsbaum sauber, Validator 0/0) |
| Prüfmethode | **Zwölf Messläufe an zwei Packs**, davon **vier Kontrollläufe** (M5, M6, M7, M11) und **zwei Entlastungsläufe** (M2, M12), dazu **vier Abzählungen** (A1 bis A4) ohne Lauf. Gemessen wird an einer **Arbeitskopie** des Piloten und an einer **frischen Installation**; der Pilot selbst bleibt unberührt |
| Umgebung | Windows 11, Python 3.14.4. Arbeitskopie des Piloten im Scratchpad (ohne `.git` und `target/`), einmal mit dem ausgelieferten Kern des Piloten (0.41.0) und einmal mit dem Kern von `main` (0.43.0). Frische `devin-desktop`-Installation aus `install.py` |
| Ergebnis | **Der Befund bestätigt sich, und er liegt woanders, als die Übergabe ihn vermutet hat.** Die Lücke in Prüfung 37 ist **erklärt** – `CR-2026-061` Abschnitt 4 nimmt genau diesen Fall ausdrücklich aus. Der Befund ist, dass **drei ausgelieferte Texte aus demselben Patch das Gegenteil versprechen, ohne Einschränkung** – und einer von ihnen steht in **jeder** erzeugten Berechtigungsdatei |

## 0. Der Befund in einem Satz

**Drei offene Platzhalterschlitze decken drei beliebige Befehlsfreigaben, und die Enthaltung
darüber steht im Änderungsantrag, während drei ausgelieferte Texte sie uneingeschränkt
bestreiten.**

## 1. Was gemessen wurde

| Nr. | Messung | Ort |
|---|---|---|
| M1 | Was meldet Prüfung 37 am Piloten, unverändert? | Arbeitskopie, `claude-code` |
| M2 | **Entlastung:** Läuft Prüfung 37 dort überhaupt und sieht sie den `ask`-Korb? | dort, `Edit(**)` entfernt |
| M3 | Ein gefüllter Schlitz trägt einen **anderen** Befehl als das Overlay erklärt | `mvn -B test` → `mvn -B verify` |
| M4 | Ein Schlitz, den das Overlay als „nicht vorhanden" erklärt, trägt einen Befehl **mit Fernwirkung** | `mvn -B -q compile` → `mvn -B deploy` |
| M5 | **Kontrolle:** eine **vierte** zusätzliche Regel | dort |
| M6 | **Kontrolle der Arithmetik:** ein Schlitz weniger gefüllt | dort |
| M7 | **Kontrolle:** der alte Befund von 0.39.0 – Präfixzeichen von Hand nachgetragen | `mvn -B test:*` |
| M8 | Präfixzeichen **und** vierter Eintrag zugleich | dort |
| M9 | Frische `devin-desktop`-Installation, unverändert | Scratchpad |
| M10 | Drei Befehlsfreigaben eingetragen, während das Overlay dreimal `<TBD>` erklärt | dort |
| M11 | **Kontrolle:** eine vierte Freigabe | dort |
| M12 | **Entlastung:** Sieht Prüfung 37 den `ask`-Korb **dieses** Packs? | dort, `Write(**)` entfernt |
| A1 | Wie viele Projektschlitze hat die Kernquelle, in welchem Korb, für welches Verb? | `framework/runtime/permissions.json` |
| A2 | Wie viele Träger führen dieselben drei Werte je Installation? | Pilot |
| A3 | Steht die Zuordnung Platzhalter → Wert in den Overlays maschinenlesbar? | vier Overlays |
| A4 | Was führt der Pilot im `ask`-Korb an Befehlsregeln? | Pilot |

## 2. Die zwölf Läufe

**Pack `claude-code`, Arbeitskopie des Piloten.** Die Spalte „37 meldet" zählt die Meldungen
der Prüfung 37, nicht das Gesamtergebnis; das Gesamtergebnis steht daneben, damit eine Null
ein Messwert ist und kein Absturz (die Lehre vom 14.09.).

| Lauf | Eingriff | 37 meldet | Gesamt (0.41.0) | Gesamt (0.43.0) | Urteil |
|---|---|---|---|---|---|
| **M1** | keiner – der Pilot wie vorgefunden | **0** | 1 Fehler | 2 Fehler | **Der Befund steht und wird nicht gemeldet** |
| **M2** | `Edit(**)` aus `ask` entfernt | **1** (fehlend) | 2 | 3 | Entlastung: die Prüfung läuft hier und liest diesen Korb |
| **M3** | `Bash(mvn -B test)` → `Bash(mvn -B verify)` | **0** | 1 | 2 | Ein Schlitz mit fremdem Inhalt läuft durch |
| **M4** | `Bash(mvn -B -q compile)` → `Bash(mvn -B deploy)` | **0** | 1 | 2 | **Ein Befehl mit Fernwirkung läuft durch** |
| **M5** | zusätzlich `Bash(mvn -B deploy)` (vierter Eintrag) | **1** (Überschuss) | 2 | 3 | Kontrolle: die Deckung endet bei drei |
| **M6** | ein Schlitz weniger gefüllt | **0** | 1 | 2 | Kontrolle: weniger Überschuss meldet erst recht nichts |
| **M7** | `Bash(mvn -B test:*)` | **1** (Präfix) | 2 | 3 | Kontrolle: der Befund von 0.39.0 wird weiter gefangen |
| **M8** | Präfixzeichen **und** vierter Eintrag | **1** (Überschuss) | 2 | 3 | Der Präfixteil **schweigt**, sobald der Überschuss die Deckung übersteigt – bewusst so gebaut, aber nennenswert |

**Die beiden Kernstände melden zeilengleich.** Was der Pilot mit seinem ausgelieferten
Validator (0.41.0) nicht sieht, sieht der Validator von `main` (0.43.0) auch nicht. Die
zusätzliche Grundmeldung von 0.43.0 ist die Versionsangabe des Overlays und gehört nicht
zur Sache.

**Pack `devin-desktop`, frische Installation** – wörtliche Befehlssperre statt Präfixform,
`Exec` statt `Bash`. Die Frage nach B02: Läuft die Arithmetik auch hier?

| Lauf | Eingriff | 37 meldet | Gesamt | Urteil |
|---|---|---|---|---|
| **M9** | keiner – alle drei Schlitze offen | **0** | 2 Fehler | Ausgangslage |
| **M10** | drei Befehle eingetragen: `mvn -B clean package`, `mvn -B test`, **`mvn -B deploy`** | **0** | 2 | **Das Overlay erklärt dreimal `<TBD>` – und drei Freigaben laufen durch** |
| **M11** | eine vierte: `Exec(mvn release:perform)` | **1** (Überschuss) | 3 | Kontrolle: die Deckung endet auch hier bei drei |
| **M12** | `Write(**)` aus `ask` entfernt | **1** (fehlend) | 3 | Entlastung: die Prüfung läuft auch bei diesem Pack |

**M10 ist der schärfste Lauf des Protokolls.** Nicht ein *falsch* gefüllter Schlitz läuft
durch, sondern ein Overlay, das **überhaupt nichts erklärt**, deckt drei Befehlsfreigaben –
darunter eine mit Fernwirkung, die `framework/core/05-working-model.md` Abschnitt 3.2 Nummer 2
**in jedem Modus** verbietet.

## 3. Die vier Abzählungen

### A1 – Die Deckung ist genau drei

| Korb | Verb | Schlitze |
|---|---|---|
| `ask` | `exec` | **3** – `<BUILD_COMMAND>`, `<TEST_COMMAND>`, `<LINT_COMMAND>` |
| `deny` | `read` | 1 – `<EXCLUDED_PATHS>` |
| `deny` | `write` | 3 – `<CI_CONFIG_PATHS>`, `<QUALITY_GATE_CONFIG_PATHS>`, `<EXCLUDED_PATHS>` |

**Deckung entsteht nur in `ask` und `allow`**, denn nur dort ist Überzähliges ein Fehler. Im
`deny`-Korb ist eine zusätzliche Regel eine Verschärfung und ohnehin zulässig – die vier
Pfadschlitze decken also nichts. **Die Zahl, die den Befund trägt, ist drei.**

### A2 – Drei Träger führen dieselben drei Werte

| Träger | Am Piloten |
|---|---|
| Quell-Overlay, Abschnitt 5 und 6 | `mvn -B clean package` · `mvn -B test` · **nicht vorhanden** |
| Laufzeitfassung `.claude/rules/20-project-overlay.md` | `mvn -B clean package` · `mvn -B test` · **nicht vorhanden** |
| Berechtigungsdatei `.claude/settings.json` | `mvn -B clean package` · `mvn -B test` · **`mvn -B -q compile`** |

**Zwei von drei Trägern sagen dasselbe, der dritte gewährt etwas anderes** – und der dritte
ist der einzige, der durchsetzt. Der Abgleich zwischen Quell-Overlay und Laufzeitfassung ist
seit `CR-2026-044` E4 offen; **das ist seine erste gemessene Fundstelle**, und sie fällt
zugunsten der beiden Textträger aus.

### A3 – Die Zuordnung steht maschinenlesbar da, in allen vier geprüften Overlays

| Overlay | `<BUILD_COMMAND>` | `<TEST_COMMAND>` | `<LINT_COMMAND>` |
|---|---|---|---|
| Vorlage `templates/project-overlay/OVERLAY.md` | 1 Zeile → `<TBD>` | 1 Zeile → `<TBD>` | 1 Zeile → `<TBD>` |
| Pilot | 1 Zeile → `mvn -B clean package` | 1 Zeile → `mvn -B test` | 1 Zeile → `nicht vorhanden` |
| frische `devin-desktop`-Installation | 1 Zeile → `<TBD>` | 1 Zeile → `<TBD>` | 1 Zeile → `<TBD>` |
| Testinstallation im Repositorium | 1 Zeile → `<TBD>` | 1 Zeile → `<TBD>` | 1 Zeile → `<TBD>` |

**Jeder Platzhalter steht in genau einer Tabellenzeile, und der Wert steht in der Zelle
rechts daneben.** Das gilt für die Vorlage von 0.43.0 ebenso wie für den Piloten, dessen
Abschnitt 6 aus einer älteren Vorlage stammt und eine andere Spaltenüberschrift führt. **Die
Zuordnung wird nicht aus Fließtext geraten, sie steht in einer Schlüsselspalte** – und
`docs/PLACEHOLDER_REGISTRY.md` weist sie längst aus („Overlay 5" beziehungsweise „Overlay 6").

### A4 – Der Pilot füllt alle drei Schlitze, obwohl er nur zwei Befehle erklärt

Drei Befehlsregeln im `ask`-Korb bei drei Schlitzen – **genau an der Grenze**, ab der
Prüfung 37 meldet. Eine weitere Zeile, und der Befund wäre 0.39.0 aufgefallen.

## 4. Der eigentliche Befund: eine Enthaltung, die nur im Antrag steht

Die Lücke in Prüfung 37 ist **kein Versehen**. `CR-2026-061` Abschnitt 4 nennt sie beim Namen:

> „Der zweite dort benannte Posten – ein belegter `<LINT_COMMAND>`, obwohl das Overlay
> ‚Lint: nicht vorhanden' sagt – bleibt **unbeanstandet**; ein gefüllter Schlitz ist ein
> gefüllter Schlitz, und den Abgleich mit dem Overlaytext leistet diese Prüfung nicht."

**Das ist eine saubere Enthaltung.** Auch D-76 und D-77 im Decision Log bleiben genau: D-77
sagt „Ein Platzhalterschlitz darf gefüllt sein und zählt dann gegen den Überschuss", und D-76
sagt „einen **vierten** Eintrag kann ein Projekt dort nicht erzeugen" – M5 und M11 belegen,
dass der vierte tatsächlich fällt.

**Derselbe Patch hat drei Texte ausgeliefert, die die Enthaltung nicht kennen.** Alle drei
stammen aus `34d850e` (Release 0.39.0) – demselben Commit wie die Enthaltung:

| # | Träger | Wortlaut | Gemessen |
|---|---|---|---|
| **Z1** | `templates/project-overlay/OVERLAY.md` Abschnitt 6 | „Ein Eintrag von Hand in `<PERMISSIONS_FILE>` ist **kein** Ersatz: Prüfung 37 des Validators meldet ihn als Ausweitung" | **Falsch, solange ein Schlitz offen ist** (M1, M4, M10) |
| **Z2** | `clientmap.py`, Kommentarkopf **jeder erzeugten Berechtigungsdatei** | „Eine zusätzliche Regel ist nur unter ‚deny' zulässig … unter ‚ask' und ‚allow' wäre sie eine Ausweitung **und ist ein Fehler**. Ein zusätzlicher freigegebener Befehl gehört deshalb nicht hierher" | **Falsch, solange ein Schlitz offen ist** |
| **Z3** | `framework/core/03-security.md` | „**Prüfung 37 hält die installierte Datei gegen die Kernquelle:** Was dort erzeugt wird, muss hier stehen; eine zusätzliche Regel ist nur unter `deny` zulässig" | **Falsch, solange ein Schlitz offen ist** |

**Z2 ist die teuerste der drei.** Sie steht nicht in einem Dokument, das man zum Nachschlagen
aufschlägt, sondern im Kopf genau der Datei, in der jemand die Zeile einträgt, über die sie
eine Aussage macht. Wer dort liest „ist ein Fehler" und trotzdem eine Zeile einträgt, bekommt
einen grünen Lauf – und liest das als Bestätigung, dass seine Zeile keine zusätzliche war.

**Die Lehre ist die von 0.42.0, eine Ebene tiefer:** *Eine Entscheidung, die nur in einem
Antrag steht, hält bis zum nächsten Antrag.* Hier hält eine **Enthaltung**, die nur in einem
Antrag steht, nicht einmal bis zum Ende desselben Patches.

## 5. Warum das kein Schönheitsfehler ist

- **Die `ask`-Stufe ist keine Entwarnung.** `CR-2026-061` Abschnitt 2 hat das ausbuchstabiert:
  Eine Zeile im `ask`-Korb erklärt einen Befehl für **freigegeben**, gleich wie der Client sie
  behandelt. „Alle nicht gelisteten Befehle sind nicht freigegeben" steht unter jeder Tabelle
  des Abschnitts 6.
- **Die gedeckte Menge ist nicht harmlos.** M4 und M10 tragen `mvn -B deploy` ein – einen
  Befehl mit Fernwirkung, den Abschnitt 3.2 des Arbeitsmodells **in jedem Modus** verbietet
  und den Abschnitt 6 des Overlays „nie" listen darf. Kein Lauf meldet etwas.
- **Der Deckel ist die Nachlässigkeit des Projekts, nicht die Strenge der Prüfung.** Ein
  Projekt, das seine drei Schlitze **sauber** füllt, hat keine Deckung mehr. Die Deckung
  entsteht genau dort, wo ein Projekt einen Befehl **nicht** hat – und dann ausgerechnet die
  freigewordene Zeile anderweitig benutzt. **So ist der Pilot entstanden.**
- **Es trifft beide Packs** (M10 gegen M4) und ist unabhängig von der Befehlssperrform.
- **Es steht seit fünf Releases** (0.39.0 bis 0.43.0).

## 6. Was die Behebung sein muss – und was sie nicht sein kann

**Sie kann nicht in der Arithmetik liegen.** Prüfung 37 kennt nur Mengen; welcher Eintrag
welcher Schlitz ist, steht dort nicht und kann dort nicht stehen. Wer die Deckung schlicht
streicht, verbietet dem Projekt das Füllen seiner eigenen Schlitze.

**Die Zuordnung gibt es genau einmal, und zwar im Overlay** (A3). Sie dort zu lesen ist keine
neue Freiheit: `docs/PLACEHOLDER_REGISTRY.md` weist für alle drei Platzhalter die Herkunft
„Overlay 5" beziehungsweise „Overlay 6" aus, und der Validator liest `OVERLAY.md` seit D-44
ohnehin. **Neu ist, dass er einen Wert liest statt eines Zustands** – und das ist die
Ermessensfrage, die vor dem Bauen entschieden gehört.

**Die Laufzeitfassung taugt als Quelle nicht.** `20-project-overlay.md` führt dieselben drei
Werte, aber in einer Fließzeile ohne Schlüsselspalte – und der Pilot hat sie bereits umgebaut
(zwei Zeilen statt einer, ein zusätzliches Feld „Schnellprüfung"). **Eine Prüfung darüber
fiele beim ersten echten Projekt, und zwar an der Form, nicht an der Sache.**

## 7. Was diese Gegenprüfung nicht belegt

- **Sie misst keine Sitzung.** Dass ein KI-Client die Zeile `Bash(mvn -B -q compile)`
  tatsächlich als Freigabe benutzt, ist **nicht beobachtet**. Gemessen ist, dass sie dasteht
  und dass kein Lauf sie beanstandet.
- **Sie sagt nichts über die vier Pfadschlitze.** `<EXCLUDED_PATHS>` und die beiden
  Konfigurationslisten stehen im `deny`-Korb und decken deshalb keinen Überschuss – ob ein zu
  **eng** gefüllter Pfadschlitz eine stille Lockerung ist, ist eine andere Frage und hier
  **nicht** gemessen. Sie ist n:1 (eine Liste im Overlay, eine Regel in der Datei) und braucht
  eine eigene Entscheidung.
- **Sie hat den Überschuss nur in `ask` gemessen.** Im `allow`-Korb gibt es heute keinen
  Befehlsschlitz; ob eine künftige Regelmenge dort einen anlegt, ist offen.
- **Die drei Texte Z1 bis Z3 sind gesucht, nicht abgezählt.** Die Suche lief über
  `leitwerk-core/` ohne `build/out/`, Protokolle und Änderungsanträge und traf drei Stellen;
  ob eine vierte in einer Formulierung steckt, die das Suchmuster nicht trifft, ist offen.
  **Das ist die schwächere Belegform dieses Protokolls**, und sie betrifft genau den Teil, der
  den Befund trägt.
- **Der Pilot ist unberührt geblieben.** Alle zwölf Läufe liefen an Kopien; die
  Ausgangszustände sind nach jedem Lauf zurückgeschrieben und geprüft worden.
