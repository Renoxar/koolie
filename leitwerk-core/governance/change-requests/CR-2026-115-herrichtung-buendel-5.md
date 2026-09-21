# Änderungsantrag `CR-2026-115`

| Feld | Inhalt |
|---|---|
| Titel | Die Herrichtung von Bündel 5 – `K-87` wurde kleiner, und zwei Prüfungen desselben Repositoriums standen gegeneinander |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-22 |
| Betroffene Artefakte | `tests/erhebungen/packaktivierung.py` (neu), `tests/erhebungen/ablage.py` (`blaetter()`, `skillmenge()`, `zellkennung()`), `tests/erhebungen/baeume-b4.py` (Zuschnitt `ohnepack`, `--zellen`), `tests/erhebungen/umgebungen-bauen-b4.py` (abgeleiteter Wächter, Packaktivierung), `tests/scripts/validate-framework.py` (**Prüfung 37**), `tests/scripts/probe-pruefungen.py` (Sonde 37h, Gegenprobe 37c), `framework/role-packs/README.md`, `framework/role-packs/requirements-engineering/ROLE_PACK.md` (0.1.1 → 0.1.2), `framework/role-packs/requirements-engineering/skills/role-re-ticket/TESTS.md` (vier Vorbedingungen), `onboarding/exercises/README.md` (`UEB-30`, `UEB-31`), `governance/DECISION_LOG.md` (**D-242** bis **D-246** neu, **`K-88`** neu, `K-87` geschlossen), `tests/protocols/2026-09-22-herrichtung-buendel-5.md` (neu), `docs/ROADMAP.md`, `CHANGELOG.md`, `VERSION`, `UEBERGABE.md`; **außerhalb des Repositoriums** das Übungsrepositorium (Overlay, Laufzeitfassung, `README.md`, `tools/praeparationen.py`, `tools/praeparationen/ueb31-fernleihe.ts`, Mentorenblatt) |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind der Meßapparat, der Prüfapparat und die Vorbedingungen eines Testblatts |
| Art | Herrichtung vor einem bezahlten Meßtag – **kein Kontingent, kein Lauf am Client** |
| Dringlichkeit | **Regulär**, unmittelbar vor Bündel 5 |

## 1. Anlass

`CR-2026-114` hat den Vorbedingungsdurchgang von Bündel 5 gefahren und fünf Befunde
aufgenommen. Vier davon sind Aufträge an diese Herrichtung, der fünfte ist `K-87` –
ausdrücklich **nicht** entschieden, weil die Antwort den Meßaufbau festlegt und Läufe
kostet. Der Wiederaufnahmepunkt nennt fünf Stücke:

1. `K-87` entscheiden,
2. der Baumbau aktiviert das Pack (D-237) und leitet seine Skillmenge aus dem Zuschnitt ab,
3. `UEB-30` bauen (D-240),
4. `UEB-31` bauen (D-241),
5. das Übungsrepositorium heben und die Vorbedingung von `RE-001-P05` präzisieren (D-241).

**Alle fünf sind erledigt. Dabei sind vier weitere Befunde angefallen, und zwei von
ihnen hätten den Meßtag gekostet.**

### 🟢 Befund 1: `K-87` ist kleiner geworden, als der Antrag angenommen hat (D-242)

`CR-2026-114` hat die Frage als Abwägung zwischen *„nur den Skill schneiden"* und
*„Skill und Rollenregel schneiden"* gestellt und für die Trennung **drei Zuschnitte und
fünfzehn weitere Läufe** veranschlagt – D-122 an einer neuen Stelle.

**Gegen die Träger gehalten ist die vermutete Teilung gar nicht herstellbar.** Die
Laufzeitfassung `30-role-requirements-engineering.md` trägt

| Gegenstand | `SKILL.md` | Laufzeitfassung | `ROLE_PACK.md` |
|---|---|---|---|
| EARS-Muster, vollständige Tabelle | ✔ (Abschnitt 3, Schritt 5) | ✔ | ✔ (Abschnitt 6) |
| Anforderung / Befund / Randbedingung | ✔ | ✔ | ✔ (Abschnitt 2) |
| M1-Grenzen, Zuständigkeiten (V3, V11) | ✔ | ✔ | ✔ (Abschnitt 1) |
| Rückfrage bei unbekanntem `<ISSUE_TRACKER>` | ✔ | ✔ | ✔ (Abschnitt 5) |
| Datenschutzregel des Packs | ✔ | ✔ | ✔ (Abschnitt 8) |
| **Ausgabegerüst (Abschnitt 5)** | ✔ | – | – |

Wer nur `ROLE_PACK.md` schneidet, läßt EARS in der Rollenregel stehen; wer nur den Skill
schneidet, ebenso. **Die Wahl ist binär.** Damit entfällt der dritte Zuschnitt samt
seinen fünfzehn Läufen, und die Entscheidung kostet nichts.

### 🔴 Befund 2: Prüfung 37 verbietet genau den Eintrag, den Prüfung 72 verlangt (D-243)

**Gemessen am 2026-09-21 am Meßbaum von Bündel 5, nach der vollständigen Aktivierung:**

```
FEHLER  .claude/settings.json: der allow-Korb führt 1 Regel(n), die die Kernquelle
        nicht erzeugt, bei 0 gefüllten Platzhalterschlitz(en): Skill(role-re-ticket).
```

**Prüfung 72 ist erst mit `0.81.0` entstanden und verlangt diesen Eintrag** – er ist der
dritte Teil der Aktivierung (D-238). **Prüfung 37 hält ihn für eine Ausweitung.** Damit
war die Abhilfe von D-238 in keinem übernehmenden Projekt umsetzbar, ohne den eigenen
Validator rot zu färben.

🔴 **Warum `0.81.0` es nicht sehen konnte:** Dort wurde *vor* dem dritten Teil gemessen –
der Baum trug 13 Skills und 12 Korbeinträge, und der Validator meldete 0 Fehler. **Die
Meldung entsteht erst durch die Abhilfe.**

> *Wer eine Prüfung baut, die etwas VERLANGT, fragt, ob eine andere desselben
> Repositoriums es VERBIETET.*

### 🔴 Befund 3: Die Aktivierungsanleitung sagt „kopieren", und für `claude-code` ist Kopieren falsch (D-244)

`framework/role-packs/README.md` schreibt zur Aktivierung ein `cp` der Laufzeitfassung
vor. **Gemessen am selben Baum:**

| Weg | Validator an `30-role-requirements-engineering.md` |
|---|---|
| `cp` – die Quellform, wie die README sie vorschreibt | **2 Fehler** (`description`, `trigger`) |
| über `render_rule()` des Frameworks | **0** |

`claude-code` wertet für Regeldateien nur `paths` aus (`K-18`); das Quellfrontmatter
trägt `description` und `trigger: model_decision`. **Für `devin-desktop` ist Quellform
gleich Zielform** – dort war der fehlende Schritt folgenlos, und deshalb ist er acht
Releases lang niemandem aufgefallen. `install.py` kann die Abbildung seit `0.14.0`;
`ist_regelquelle()` führt die Laufzeitfassungen aktivierter Packs ausdrücklich auf.

> *Ein Werkzeug, das eine Abbildung kann, und eine Anleitung, die „kopieren" sagt: Die
> Anleitung gewinnt, weil sie gelesen wird.*

🔴 **Und der erste Versuch tat nichts, lautlos.** `render_rule()` steigt aus, wenn der
Text nicht mit dem Zeilenvorschub nach den drei Strichen beginnt. Die Quelle im
Repositorium ist CRLF; ohne Flachlegen war der Aufruf eine **Zusage ohne Wirkung**, und
der Baum sah aus wie vorher. `install.py` selbst liest im Universal-Newline-Modus und
merkt davon nichts. Der Meßapparat legt seither flach **und prüft danach, ob die
Abbildung überhaupt gegriffen hat.**

### 🔴 Befund 4: Der Wert von `<ISSUE_TRACKER>` stand in drei Trägern (D-245)

D-240 hat gemessen, daß er im Quell-Overlay **einmal** steht, in Prosa und ohne spitze
Klammern. **Er steht aber noch zweimal, und beide Male ist es eine Ersetzung statt einer
Bindung:**

| Träger | Wortlaut |
|---|---|
| `.devin/rules/20-project-overlay.md` | *„Ausgabeformat: Markdown (Ticketsystem des Projekts: GitHub Issues)"* |
| `README.md` des Übungsrepositoriums | *„in diesem Projekt sind es GitHub Issues, also Markdown"* |

**Eine Präparation, die nur die Overlay-Zeile zurücknimmt, nimmt nichts zurück:** Ein
Lauf von `RE-001-N09` hätte das Format weiter aus der immer geladenen Laufzeitfassung
abgelesen. Beide Träger verweisen jetzt auf die Bindungszeile, statt den Wert zu
wiederholen – das ist D-160 an zwei neuen Stellen.

🔴 **Und `UEB-30` bekommt keinen `<TBD:>`-Schlitz, obwohl D-240 einen vorgezeichnet
hat.** Abschnitt 13 ist für den Validator ein **sicherheitsrelevanter** Abschnitt:

| Wert der Zelle | `validate-framework.py --strict-overlay` |
|---|---|
| `<TBD: Ticketsystem des Projekts>` | **1 Fehler** – offene `<TBD>`-Werte, sicherheitsrelevant |
| `nicht festgelegt` | **0** |

Mit dem Schlitz wäre `RE-001-N09` nur in einem Baum fahrbar, den das eigene
Repositorium beanstandet – **genau der Widerspruch, gegen den Prüfung 57 gebaut ist,
eine Prüfung weiter.** Die **Bindung** bleibt in beiden Fällen bestehen; verloren geht
allein der **Wert**, und genau diesen Zustand nennt der Skill *„`<ISSUE_TRACKER>`
unbekannt"*.

### 🔴 Befund 5: Der erste Fachbegriff für `UEB-31` hätte eine abgenommene Zelle entwertet (D-246)

Der naheliegende Gegenstand für einen Kopfkommentar mit Produktverhalten war eine
*Vormerkung*. **Er fällt aus, und der Grund steht in einer geschlossenen Zelle:** Der
abgenommene Beleg von `SK-009-N02` stützt sich wörtlich darauf, daß der Lauf den zweiten
Ursachenkandidaten *„mit Suchmuster widerlegt"* hat – *„kein Vormerkungsbegriff im
Code"*. **Eine neue Präparation hätte einer bereits abgenommenen Zelle den Boden
entzogen.** Das ist D-137 eine Ebene weiter außen. Gewählt ist *Fernleihe*: **0
Fundstellen** über Quellcode, Verträge, Migrationen und Dokumentation.

🔴 **Und der Verrat-Wächter des Übungsrepositoriums hätte eine Quelle durchgelassen, die
ihren eigenen Testfall beim Namen nennt.** Sein Muster führte die Kennungsfamilie `SK-`
mit drei Ziffern wörtlich; die fünfzehn Zellen von Bündel 5 heißen `RE-001-*`. **Zu eng
genau bei dem Bündel, für das er gebraucht wird.** Er beschreibt die Familie jetzt als
Form.

### ⚠️ Nebenbefund: `K-88` – Prüfung 55b prüft eine Teilzeichenkette, und es sind 15 von 26

D-240 hat die Bauform benannt. **Gezählt ist sie jetzt:** Von 26 Pflichtplatzhaltern,
die die Laufzeitschicht nennt, sind im aktiven Übungs-Overlay **14 nirgends** mit
spitzen Klammern gebunden; rechnet man den **Änderungsverlauf des Overlays** heraus,
sind es **15**. **Prüfung 55b meldet null.**

🔴 **Die schärfste Fundstelle ist die Zeile, die die Bindung verkündet:**
`<ISSUE_TRACKER>` stand vor dieser Herrichtung mit spitzen Klammern **ausschließlich**
im Eintrag `0.63.0` des Änderungsverlaufs – in dem Satz *„Acht Pflichtplatzhalter sind
jetzt GEBUNDEN statt ersetzt"*.

**Hier nicht behoben**, und der Grund ist derselbe wie bei `K-79` vor Bündel 4: Vierzehn
Platzhalter zu binden ist ein Eingriff in den **Meßgegenstand**, wenige Tage vor dem
Meßtag. `K-88`, **nach** Bündel 5.

## 2. Gegenprüfung (D-23)

| Befund | Gegenprüfung | Ergebnis |
|---|---|---|
| 1 | Trägt die Rollenregel EARS wirklich vollständig, oder nur eine Kurzfassung? | **Vollständig, alle fünf Muster als Tabelle**, dazu die vier Regeln des Packs. Die Kurzfassung hat den Vorbehalt der Langform **nicht** verloren |
| 2 | Meldet Prüfung 37 auch, wenn der Skill fehlt? | **Ja** – Sonde 37h: `Skill(role-gibt-es-nicht)` bleibt eine Ausweitung. Der Zuschnitt hängt an der Ablage, nicht am Wort |
| 2 | Wäre der Befund am Meßtag aufgefallen? | **Nein.** Der Baumbau ruft den Validator nicht; die Meldung träfe erst das nächste übernehmende Projekt |
| 3 | Liegt es an `render_rule()` oder an der Anleitung? | **An der Anleitung.** `render_rule()` bildet korrekt ab, sobald es aufgerufen wird; `ist_regelquelle()` führt Packlaufzeitfassungen seit `0.14.0` |
| 4 | Ist der Wert vielleicht noch an einer vierten Stelle? | **Nein, gemessen:** `GitHub Issues` kam außerhalb von `leitwerk-core/` in genau drei Trägern vor, alle drei sind angefaßt. **Danach nachgezählt:** eine Fundstelle außerhalb von `tools/**` – die Bindungszeile selbst |
| 5 | Stützt sich noch eine andere abgenommene Zelle auf ein Fehlen im Code? | **Nein, gezählt:** über **14 Blätter** (dreizehn Testblätter und den zentralen Katalog) trägt **genau eine** abgenommene Zelle einen Fehlensbeleg in ihrem Ergebnisstatus – `SK-009-N02` |

## 3. Vorlage zur Entscheidung

**E1 – Was schneidet der Kontrollzuschnitt bei einem Role Pack? (`K-87`)**

| Auflösung | Preis |
|---|---|
| **(a) `ohnepack`: die Aktivierung rückwärts** – Laufzeitfassung, Skillablage, Korbeintrag, dazu das kanonische Packverzeichnis; die Kernregelschicht bleibt | Trennt Skill und Rollenregel **nicht**. Kein zusätzlicher Lauf |
| (b) `ohneskill` unverändert | Rund zehn der fünfzehn Kontrolläufe behalten ihren Gegenstand in der Rollenregel; die Zurechnung lautet durchweg *„nicht dem Skill zurechenbar"*, ohne Grund |
| (c) Drei Zuschnitte | +15 Läufe, +15 bis 18 USD für eine Trennung, die **keine** der fünfzehn Zellen verlangt |

➡️ **Empfehlung und Entscheidung: (a).** Alle fünfzehn Zellen nennen Abschnitte der
`SKILL.md` als ihren Gegenstand, keine die Rollenregel.

**E2 – Wie werden Prüfung 37 und Prüfung 72 miteinander verträglich?**

➡️ **Prüfung 37 leitet die Skillfreigaben aus der Skillablage ab.** Verworfen: eine
gepflegte Ausnahmeliste (gepflegte Zahl, D-153) und eine Regel in der Kernquelle
(Vorabfreigabe ohne Gegenstand, D-81).

**E3 – Kopieren oder rendern?**

➡️ **Rendern.** Die Anleitung bekommt `install.py --update` als eigenen Schritt, der
Meßapparat ruft `render_rule()` unmittelbar und prüft danach, ob die Abbildung gegriffen
hat.

**E4 – Welche Form hat der zurückgenommene Wert?**

➡️ **`nicht festgelegt`, kein `<TBD:>`-Schlitz** – gemessen 1 Fehler gegen 0, bei
gleicher Bindung.

**E5 – Welchen Gegenstand bekommt `UEB-31`?**

➡️ **Ein eigenes Modul zur *Fernleihe*.** Verworfen: *Vormerkung* (entwertet den Beleg
von `SK-009-N02`) und `BookForm.tsx` (der letzte unpräparierte Vorrat, `K-72`).

## 4. Entscheidung

| Punkt | Entscheidung | Decision Record |
|---|---|---|
| E1 (`K-87`) | **(a)** – `ohnepack` | **D-242**, `K-87` geschlossen |
| E2 | Prüfung 37 leitet die Skillfreigaben ab | **D-243** |
| E3 | Die Laufzeitfassung wird gerendert | **D-244** |
| E4 | `nicht festgelegt`, der Wert steht an einer Stelle | **D-245** |
| E5 | eigenes Modul, *Fernleihe* | **D-246** |
| – | Prüfung 55b prüft eine Teilzeichenkette, 15 von 26 | **`K-88`**, nach Bündel 5 |

## 5. Umsetzung

1. **`packaktivierung.py`** (neu): `aktivieren()` mit den drei Teilen und je einem
   Wächter, `entfernen()` als Umkehrung, `skillorte()` und `skillschnitt()` – der
   Zuschnitt von D-234/D-239 liegt seither **einmal** und wird von beiden Klassen
   gefahren.
2. **`ablage.py`**: `blaetter()` leitet die Zuordnung Kennungspräfix → Skill aus den
   Testblättern des Frameworks ab, `skillmenge()` gibt zu einer Zellmenge Skills und
   Packs, `zellkennung()` nimmt die zusammengezogene Kennung zurück.
3. **`baeume-b4.py`**: Klasse `ohnepack`, `--zellen`, und die Rückübersetzung der
   Kennung kommt aus `ablage`.
4. **`umgebungen-bauen-b4.py`**: Der Wächter nennt die Skills nicht mehr beim Namen; die
   Packs kommen aus dem Zuschnitt, und der Korbeintrag wird mitgeprüft.
5. **Prüfung 37** in `validate-framework.py`, Sonde 37h und Gegenprobe 37c.
6. **`role-packs/README.md` und `ROLE_PACK.md`** (0.1.1 → 0.1.2): die Aktivierung hat
   vier Schritte.
7. **Übungsrepositorium:** `<ISSUE_TRACKER>` gebunden, `UEB-30` (Art `textersatz`) und
   `UEB-31` gebaut, Verrat-Wächter erweitert, Mentorenblatt und Register nachgezogen,
   auf `0.82.0` gehoben.
8. **Testblatt:** die Vorbedingungen von `RE-001-P04`, `P05`, `N09` und `N10`.
9. Decision Records, Protokoll, ROADMAP, CHANGELOG, VERSION, Übergabe.

## 6. Abnahme

- `validate-framework.py`: **0 Fehler, 0 Warnungen**
- `validate-framework.py --strict-overlay` im Übungsrepositorium: **0 Fehler, 0 Warnungen**
- `probe-pruefungen.py` in **beiden** Kodierungsumgebungen, alle Einheiten `OK`
- Der Durchgang vor dem Commit, der jede Zahl nachzählt
