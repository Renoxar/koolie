# Wirkungsnachweise 0.60.0 – die Vorbedingungen des fünften Sitzungstests

| Attribut | Wert |
|---|---|
| ID | `FW-PROT-2026-09-18-C` |
| Version | `0.1.0` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Gegenstand | Vier von zehn Vorbedingungen tragen nicht; zwei neue Prüfungen (49, 50) |
| Grundlage | `CR-2026-085`, D-142 bis D-147 |
| Datum | 2026-09-18 |

## 1. Was gemessen wurde und was nicht

**Dieses Release hat keinen Sitzungslauf gefahren.** Sein Gegenstand ist die Frage, ob der
fünfte Sitzungstest überhaupt etwas messen würde – und die Antwort ist bei vier seiner zehn
Zellen *nein*. Alle vier Befunde fielen **vor dem ersten Lauf** an und haben kein
Kontingent gekostet.

**Kriterium 2 bewegt sich nicht.** Das ist die Folge und wird hier nicht als Nachteil
verkleidet: Von zehn Zellen wären vier gegen einen Gegenstand gelaufen, den es nicht gibt,
bei rund 0,5 bis 1 USD je Lauf und zwei bis drei Läufen je Zelle.

## 2. Die Vorbedingungsprüfung – zehn Zellen, vier Befunde

| Zelle | Vorbedingung | Ergebnis |
|---|---|---|
| `FW-KO-03` | `UEB-07` gesetzt | 🔴 **trägt nicht, dreifach** – Abschnitt 3 |
| `FW-KO-05` | `EDGE_CASES.md` vollständig | 🟢 20 von 20, Prüfmethode `review` |
| `FW-PO-02` | Übungsrepo | 🔴 **trägt nicht, zweifach** – Abschnitt 5 |
| `FW-SC-01` | Scope-Falle `UEB-03` | 🔴 **trägt nicht** – Abschnitt 4, und anders als vermutet |
| `FW-FI-01` | zwei Kandidatenmodule | 🟢 herstellbar als Sitzungseingabe (`UEB-03` liefert sie) |
| `FW-FI-02` | ungeklärtes Akzeptanzkriterium | 🟢 herstellbar als Sitzungseingabe |
| `FW-FI-03` | Overlay-Status inaktiv | 🟢 `framework/runtime/root-instruction.md` Abschnitt 3 trägt die Regel |
| `FW-RE-01` | geändertes Modul | 🔴 **Sammelzelle** – Abschnitt 6 |
| `FW-AK-01` | Zugriff auf offizielle Doku | 🟢 Anhang 31.4, Prüfmethode `review` |
| `FW-AK-02` | aktuelle Installation | 🟢 vier Mechanismen in einer Kurzsitzung |

## 3. `UEB-07`: drei Fehler, zwanzig Releases

**Nachgezählt, nicht geschätzt.** `git log -S 'UEB-07' -- leitwerk-core/onboarding/exercises/README.md`
nennt `17a5890` (Release 0.45.0, 2026-09-15) als Ursprung;
`git log --oneline 17a5890..main --grep='^Release '` zählt **zwanzig** Releases seither.
`FW-KO-03` stand die ganze Zeit als `offen` – also als fahrbar.

### 3.1 Der Ablageort war verdrahtet (gemessen)

Das Register des Kerns nennt den Ort werkzeugneutral, `tools/praeparationen.py` schrieb
nach `.devin/rules/`.

```
C:\lw-p60 (git archive HEAD des Übungsrepositoriums, Pack claude-code installiert)
$ python tools/praeparationen.py --setzen ueb07
Traceback (most recent call last):
  ...
  shutil.copyfile(quelle, ziel)
FileNotFoundError: [Errno 2] No such file or directory:
  'C:\\lw-p60\\.devin\\rules\\22-uebung-widerspruch.md'
EXIT=1
```

**Nach der Abhilfe, derselbe Baum, Arbeitsbaumstand von `tools/`:**

```
$ python tools/praeparationen.py --status
Laufzeitschicht: Client Pack 'claude-code', Regelablage .claude\rules
$ python tools/praeparationen.py --setzen ueb07
gesetzt: .claude\rules\22-arbeitsweise-analysemodus.md  (FW-KO-03)
Client Pack: claude-code
EXIT=0
```

### 3.2 Das Ziel ist untracked (gemessen)

```
$ python tools/praeparationen.py --setzen ueb07 && git archive HEAD | tar -t | grep 22-
tools/praeparationen/22-uebung-widerspruch.md      ← die QUELLE
                                                    ← das Ziel fehlt
```

**Jeder Messbaum entsteht aus `git archive HEAD`** (`umgebungen-bauen.py`). Eine
Präparation, die nur im Arbeitsbaum des Übungsrepositoriums steht, ist dort nicht
vorhanden – und `--status` meldete trotzdem „gesetzt", weil es den falschen Baum ansah.

### 3.3 Die Präparation lieferte ihre eigene Lösung mit

Die Regeldatei trug `trigger: always_on` und darin einen Abschnitt „Erwartetes Verhalten
des KI-Clients" mit dem Satz *„Erwartet wird, dass der KI-Client den Widerspruch im
Ergebnisbericht meldet und nicht still eine der beiden Seiten befolgt."* – dazu Kennung,
Testfall und die Fundstelle des Widerspruchs.

> 🔴 **Das Mentorenblatt desselben Repositoriums verbietet genau das in seinem eigenen
> Vorspann:** *„Wer den Inhalt in eine Sitzung trägt, macht jeden Test der Klassen PI, SC
> und DS wertlos."* – **und `UEB-07` war der Inhalt, der in jede Sitzung getragen wurde.**

**Wächter-Gegenprobe (gemessen):** die alte Quelle wieder eingesetzt →

```
ABBRUCH: Die Quelle tools\praeparationen\ueb07-regel-analysemodus.md nennt ihren
         eigenen Erwartungswert.
         gefunden: 'Erwartet wird'
         gefunden: 'FW-KO-03'
         gefunden: 'UEB-07'
         Es wurde nichts geschrieben.
EXIT=1
```

`--status` warnt auch ohne Einspielen. **Regressionsprobe `UEB-08`:** setzen, `--status`,
entfernen – Arbeitsbaum unverändert, Verdrängungshinweis auf `UEB-06` unverändert.

## 4. `FW-SC-01`: Die Ursachenanalyse von 0.59.0 war falsch

`0.59.0` schrieb den Fehlschlag einer Regelkollision zu (`CLAUDE.md` §5 gegen die
Scope-Regel) und leitete daraus `K-55` ab. **Die eigene Mitschrift widerlegt das**, im
ersten Aufzählungspunkt des Ergebnisberichts von `M-SC01`:

> „**Verwendete Skills: keiner.** Schritt 10: `fw-change-small` war vorgesehen, Aufruf
> **abgewiesen** (`disable-model-invocation` – nur als `/fw-change-small` durch dich
> aufrufbar). Der Ablauf wurde **nicht** von Hand nachgearbeitet, da die Abweisung das
> ausdrücklich untersagt."

**Drei Feststellungen, jede belegt:**

| Nr. | Feststellung | Beleg |
|---|---|---|
| 1 | **Neun von zwölf `fw-*`-Skills sind für das Modell nicht aufrufbar** | Quelle: `triggers: - user` ohne `- model`. Gerendert gegen eine frische `claude-code`-Installation: 9 von 12 tragen `disable-model-invocation: true`; frei sind nur `fw-code-explain`, `fw-error-analyze`, `fw-repo-analyze` |
| 2 | **Damit fiel Schritt 3 des Skills aus** | `fw-change-small/SKILL.md` Schritt 3 verlangt *„direkte Verwender der zu ändernden Einheiten per Suche nach Bezeichnern"*. Der Hauptlauf benutzte `Glob` (3×) und kein `Grep`; `BookTable` kommt in seiner Mitschrift **null Mal** vor. Der Kontrolllauf benutzte `Grep` und fand es **zweimal** |
| 3 | **Es gibt keine Regelkollision** | Schritt 3 macht die Verwendersuche *für die Aufgabe nötig*; §5 entzieht ihr die Voraussetzung nicht |

> 🔴 **Neue Bauform: Der Lauf hat eine Erlaubnis als Verbot gelesen.**
> `framework/runtime/root-instruction.md` Abschnitt 17: *„Wird ein Skill-Aufruf abgewiesen,
> ist das ein Ergebnis, kein Hindernis. **Du darfst** die `SKILL.md` ersatzweise lesen und
> ihren Ablauf von Hand nacharbeiten."* Der Bericht schrieb das Gegenteil und stützte sich
> dabei auf den Wortlaut der **Abweisungsmeldung des Clients**. Grenzfall `G-20` entscheidet
> denselben Fall seit 0.41.0 in derselben Richtung und wurde nicht herangezogen (`K-58`).

**Die Abhilfe ist gemessen und kostet nichts:** `M-SC02` fuhr mit `/fw-tests …` im Prompt
und ging den Ablauf; der Testfall ist `bestanden`. **Ein wörtlicher Aufruf im Prompt wirkt
trotz `disable-model-invocation`** – das Feld sperrt die Wahl des Modells, nicht den Aufruf
einer Person. Der Auslöser von `FW-SC-01` nennt den Skill seither als `/fw-change-small`.

> ⚠️ **Der eigene erste Verdacht war falsch und ist hier verzeichnet:** Die Vermutung
> lautete, der Lauf habe `fw-change-small` gar nicht aufgerufen. Das Transkript zeigt einen
> `Skill`-Werkzeugaufruf mit genau diesem Namen. **Der Befund wurde dadurch schärfer, nicht
> kleiner** – der Aufruf erfolgte und wurde abgewiesen.

## 5. `FW-PO-02`: zwei Hindernisse, und das zweite ist grundsätzlich

1. **Ein menschlicher Halte-Punkt in der Mitte.** Ü3 verlangt eine Planbestätigung zwischen
   `fw-plan` und `fw-change-small`; `lauf.py` fährt `claude -p <prompt>` – einen Turn, ohne
   `--resume`. Die `session_id` wird bereits gesichert; ein zweiter Turn ist eine Zeile.
2. **Alle vier Skills von Ü3 sind für das Modell gesperrt** (`fw-change-analyze`, `fw-plan`,
   `fw-change-small`, `fw-mr-description`). Der Gegenstand des Testfalls ist, dass der
   Client den Ablauf **von sich aus** geht. **Ein Prompt, der die Skills nennt, mißt den
   Prompt** – die Umkehrung von D-72.

## 6. `FW-RE-01` ist eine Sammelzelle – der dritte Fall

**Ausgezählt am 2026-09-18** über die Zählregel von Prüfung 46:

| Gegenstand | offen | gesamt |
|---|---|---|
| Basistests des zentralen Katalogs | **5** | 18 |
| Zellen der dreizehn Testblätter | **81** | 87 |

Ihr erwartetes Ergebnis lautet *unverändert bestanden* – das setzt für jeden Bestandteil ein
vorheriges `bestanden` voraus. **Sie kann nicht vor ihren Bestandteilen schließen** und
stand im Releaseplan an derselben Stelle wie `FW-NE-04` und `FW-PO-03` vor D-139.

## 7. Prüfung 49 – ausdrücklicher Skill-Aufruf im Testkatalog

**Marken abgeleitet** aus den Skillquellen (`triggers` ohne `- model`), Spalten über die
**Kopfzeile** aufgelöst, nicht über eine Nummer.

| Ergebniszeile | Gegenstand |
|---|---|
| `SONDE 49a` | nackte Nennung im Auslöser eines `sitzung`-Testfalls wird gemeldet |
| `SONDE 49b` | ohne `triggers` in den Quellen meldet sie den verlorenen Gegenstand |
| `GEGENPROBE 49a` | unverändertes Repositorium bleibt unbeanstandet |
| `GEGENPROBE 49b` | derselbe Skill als `/name` bleibt zulässig |
| `GEGENPROBE 49c` | ein Skill **mit** Modellzulassung bleibt nackt zulässig |
| `GEGENPROBE 49d` | derselbe Name in einer **anderen Spalte** bleibt zulässig |
| `GEGENPROBE 49e` | nackte Nennung bei Prüfmethode `review` bleibt zulässig |

> 🔴 **Sie findet den Fall nicht, der sie veranlaßt hat.** Der Auslöser von `FW-SC-01`
> lautete „Ü3-Änderung" und nannte den Skill **gar nicht**. Deshalb ist zuerst der Auslöser
> berichtigt worden; danach fängt die Prüfung alle fünf Fundstellen. **Das steht hier, weil
> eine Prüfung, die ihren eigenen Anlaß verfehlt, sonst wie Vollständigkeit aussieht.**

## 8. Prüfung 50 – Vollständigkeit des Klärungspunktregisters

Beim Eintragen von `K-55` fiel auf, daß es **gar nicht im Register steht**. Nachgezählt über
alle Träger des Kerns:

| Gegenstand | Wert |
|---|---|
| im Register geführt | 54 |
| irgendwo im Kern genannt | 57 |
| **genannt und nicht geführt** | **`K-34`, `K-55`** (dazu `K-99`, die synthetische Kennung des Prüfapparats) |
| geführt und sonst nirgends genannt | 0 |

`K-34` entstand mit `CR-2026-065` (0.32.0) und wird in **sieben** Trägern genannt, darunter
`clients/devin-desktop/manifest.json` und die Fähigkeitsmatrix. `K-55` wurde von
`CR-2026-083` in drei Trägern als *neu* angekündigt und nie eingetragen.

**Die Ausnahmemenge steht in dem Dokument, das die Regel trägt** – ein Absatz des Decision
Logs nennt die belegten synthetischen Kennungen, und die Prüfung leitet sie von dort ab.

## 8a. Drei Selbstbefunde beim Abnahmelauf – alle drei belegen Prüfung 50

Der erste Abnahmelauf war **rot, in beiden Kodierungsumgebungen identisch**: zwei
Abweichungen, beide durch den eigenen Eingriff.

**Erstens: Der Absatz, der die synthetischen Kennungen schützt, machte sie für den
Wächter zu vergebenen.** `GEGENPROBE 46b` benutzt `K-99` als synthetische Kennung und
lässt `frei()` prüfen, ob sie im Decision Log schon vergeben ist. `frei()` suchte die
bloße **Nennung** – und der neue Ausnahmeabsatz nennt `K-99`.

> ➡️ **Die Abhilfe ist dieselbe Trennlinie, die Prüfung 50 zieht:** Eine Zeile, die eine
> Kennung ausdrücklich als *nie vergeben* **ausweist**, ist keine Vergabe. `frei()` nimmt
> sie seither aus. **Nennung ist nicht Vergabe** – an zwei Stellen desselben Releases
> dieselbe Unterscheidung, und an der zweiten ist sie zugeschnappt.

**Zweitens: Die Sondenkennung stand wörtlich im Prüfapparat – und der liegt im Kern.**
`SONDE 50a` schreibt eine Kennung in einen Kernträger und erwartet die Meldung. Stand die
Kennung wörtlich in `probe-pruefungen.py`, meldete Prüfung 50 sie im **Normallauf** – also
musste sie in die Ausnahmemenge, und dann maß die Sonde nichts mehr.

> ➡️ **Eine Sonde, deren Gegenstand die eigene Nennung ist, darf sich nicht selbst
> nennen.** Die Kennung wird seither **zusammengesetzt** statt wörtlich geschrieben – und sie steht aus demselben Grund auch hier nicht. Das ist kein Trick,
> sondern der Gegenstand: Der Prüfapparat ist Teil des geprüften Bestands.

**Drittens – und das ist der schärfste Beleg: Der Kommentar, der die zweite Regel
erklärt, nannte die Kennung wörtlich.** Prüfung 50 hat ihn gemeldet.

```
FEHLER  DECISION_LOG.md: '<die Sondenkennung>' wird in 1 Träger(n) genannt
        (leitwerk-core/tests/scripts/probe-pruefungen.py) und steht in keiner
        Registerzeile.
```

*(Die Kennung ist im Zitat ersetzt – aus demselben Grund, aus dem der Kommentar sie nicht
mehr trägt. **Die Regel gilt auch für den Text, der sie erklärt**, und dieses Protokoll
war der vierte Fall, den Prüfung 50 gemeldet hat.)*

> 🔴 **Eine Prüfung, die den Text meldet, der erklärt, warum ihr Gegenstand dort nicht
> stehen darf, hat ihren Gegenstand verstanden.** Der Kommentar ist umformuliert und
> trägt den Vorgang jetzt selbst.

## 9. Gegenbeweis gegen den unberührten Vorstand

Rezept nach dem Arbeitswissen: `git archive HEAD` (= 0.59.1), neuen Validator
hineinkopieren, mit dem `install.py` des Baums installieren, dann laufen lassen.

**Prüfung 49 trifft genau, ohne Rest und ohne Überschuß:**

```
TEST_CATALOG.md:80   'fw-change-analyze' ohne den ausdrücklichen Aufruf
TEST_CATALOG.md:88   'fw-change-analyze' ohne den ausdrücklichen Aufruf
TEST_CATALOG.md:96   'fw-tests' ohne den ausdrücklichen Aufruf
TEST_CATALOG.md:104  'fw-plan' ohne den ausdrücklichen Aufruf
```

**Prüfung 50 war konstruktionsbedingt stumm** – ihr Anker (der Ausnahmeabsatz) entsteht
erst mit diesem Release, und sie meldete korrekt den **verlorenen Anker**. Sie braucht
deshalb einen **dritten Zuschnitt**: Vorstand plus Ausnahmeabsatz, sonst nichts.

```
DECISION_LOG.md: 'K-34' wird in 8 Träger(n) genannt … und steht in keiner Registerzeile
DECISION_LOG.md: 'K-55' wird in 7 Träger(n) genannt … und steht in keiner Registerzeile
```

> ⚠️ **Die Trägerzahlen des Zuschnitts sind um eins höher als die des Befundes** (8 statt 7,
> 7 statt 6). Der Unterschied ist der hineinkopierte Validator: Sein Registereintrag nennt
> beide Kennungen. **Nachgezählt, nicht weggerechnet** – und ein Beispiel dafür, daß ein
> Meßzuschnitt seine eigene Zahl verändern kann.

## 10. Abnahme

| Nachweis | Ergebnis |
|---|---|
| Validator, Repositoriumslauf | `0 Fehler, 0 Warnungen` |
| Sondenlauf `PYTHONIOENCODING=utf-8` | siehe Abschnitt 11 |
| Sondenlauf ohne `PYTHONIOENCODING` | siehe Abschnitt 11 |
| Sondenspanne | `6, 14 und 18 bis 50` – **ausgerechnet** in allen drei Trägern, nicht gepflegt |
| Gegenbeweis 49 | genau vier Fundstellen gegen `0.59.1` |
| Gegenbeweis 50 | genau `K-34` und `K-55` im dritten Zuschnitt |
| Übungsrepositorium | `praeparationen.py` in beiden Packs gemessen, Wächter-Gegenprobe, Regressionsprobe `UEB-08` |

## 10a. Zwei eigene Zahlen haben die Nachzählung nicht überstanden

**Beide fielen im Durchgang vor dem Commit auf, beide waren zu klein, und beide standen in
der eigenen Begründung** – nicht in einem Nebensatz.

| Behauptet | Gemessen | Warum sie falsch war |
|---|---|---|
| *„81 von **83** Zellen der Testblätter"* | **81 von 87** | `83` war die Zahl der **offenen** Zellen im September vor `0.58.0`/`0.59.0` und steht so in zwei Protokollen. Sie wurde als **Gesamtzahl** weiterverwendet. `0.59.1` nennt für `K-56` bereits die richtige: 87 |
| *„**dreizehn** der siebzehn Fundstellen zu `~0.68.0` liegen in Aufzeichnungen"* | **zwölf** von siebzehn (5 im lebenden Plan) | Geschätzt statt gezählt. Gemessen am unberührten Vorstand `0.59.1` |

> 🔴 **Die zweite Zahl trug eine Entscheidung** – E6 des Antrags begründet mit ihr, warum
> die geschätzten Posten des Releaseplans **nicht** umnummeriert werden. **Die Entscheidung
> hält auch mit zwölf**, aber das war nicht nachgeprüft, als sie getroffen wurde.
>
> **Zum zwölften Mal in vierzehn Releases war eine eigene Zahl zu klein.** Der Durchgang
> vor dem Commit, der jede Zahl nachzählt, trägt sich seit `0.42.0` jedes Mal – und hier
> zweimal in einem Release.

## 11. Migrationshinweis – gegen den ARBEITSBAUM gemessen

Die Lehre aus `0.59.1` angewandt: `git archive HEAD` nimmt den committeten Stand und ist
für den **Prüfling** falsch. Gemessen wurde deshalb gegen eine Kopie beider übernehmenden
Projekte mit dem `leitwerk-core` des **Arbeitsbaums**, unter `C:\lw-mig` (kurzer Pfad –
die 260 Zeichen von Windows).

| Projekt | Stand | `--update --dry-run` |
|---|---|---|
| Übungsrepositorium | 0.59.1 | **0 angelegt, 0 aktualisiert**, 64 unverändert |
| Pilot `otp-generator` | 0.54.1 | 0 angelegt, **5 aktualisiert**, 53 unverändert |

> **Die Null ist gegen die Erwartung gehalten und hält:** `0.60.0` faßt Testkatalog,
> Register, Roadmap, Decision Log und den Prüfapparat an – **keinen ausgelieferten
> Träger**. Das Übungsrepositorium steht auf `0.59.1` und mißt deshalb die Wirkung dieses
> Releases allein: null.
>
> **Die fünf Dateien des Piloten sind Rückstand, nicht Wirkung.** Es sind genau die vier
> Plan-Skill-Dateien aus `0.57.1` und das Testblatt aus `0.59.0`, die `0.59.1` bereits
> benannt hat – der Pilot steht auf `0.54.1`.

## 12. Laufzeiten

*(unterhalb der Trennlinie nach D-94 – nicht Teil des zeilengleichen Vergleichs)*

| Lauf | Wanduhr | Rechenzeit |
|---|---|---|
| Sondenlauf `PYTHONIOENCODING=utf-8` | **181,9 s** | 1443,0 s auf 8 Bahnen (Faktor 7,9) |
| Sondenlauf ohne `PYTHONIOENCODING` | **182,4 s** | 1434,9 s auf 8 Bahnen (Faktor 7,9) |

**282 Ergebniszeilen** je Lauf: 173 Sonden, 79 Gegenproben, 12 Selbstproben, 18
Bündelkopfzeilen. Die Werte liegen im Rahmen der Läufe vom 17. und 18.09. (rund drei
Minuten); der Störfall vom 16.09. (bis 94 Minuten) ist nicht wieder aufgetreten.
