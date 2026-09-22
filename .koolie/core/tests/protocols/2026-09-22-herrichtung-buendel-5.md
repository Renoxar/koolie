# Protokoll: Die Herrichtung von Bündel 5

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-21/22 (eine Sitzung ueber den Tageswechsel; die Messungen tragen den Tag, an dem sie gefahren wurden) |
| Gegenstand | Die fünf Stücke der Herrichtung von Bündel 5 (`role-re-ticket`, 15 Zellen) – **vor** dem ersten bezahlten Lauf |
| Antrag | `CR-2026-115` |
| Kontingent | **keines** – kein Lauf am Client |
| Belege | Diese Herrichtung erzeugt keine Laufbelege. Gemessen wurde an einem Meßbaum unter `C:\lw-b5`, der genau wie die 38 Bäume von Bündel 4 gebaut ist: `git archive` des Übungsrepositoriums, Packwechsel auf `claude-code`, `install.py`, `cc-overlay-fuellen.py` – und seit diesem Release die **Aktivierung des Packs**. Er ist aus den hier genannten Befehlen in vier Minuten neu baubar |

> 🟢 **`K-87` ist entschieden, und die Messung hat die Frage kleiner gemacht:** Der
> dritte Zuschnitt entfällt samt seinen fünfzehn Läufen. 🔴 **Vier weitere Befunde sind
> beim Bauen angefallen, und zwei davon standen dem Meßtag im Weg** – eine Prüfung, die
> verbietet, was eine andere verlangt, und eine Anleitung, die *„kopieren"* sagt, wo
> abgebildet werden muß. **Dreiundzwanzigster Durchgang in Folge, bei dem der billigste
> Befund vor dem ersten Lauf fällt.**

## 1. Die Lage vor der Herrichtung

| Prüfung | Ergebnis |
|---|---|
| `git status` im Framework | sauber, `main` = `0.81.0` |
| `validate-framework.py` | **0 Fehler, 0 Warnungen** |
| Übungsrepositorium | Framework **0.79.2**, Arbeitskopie sauber, `--strict-overlay` **0 Fehler, 0 Warnungen** |
| offene Meßbäume | keine |

## 2. `K-87`: die Frage gegen die Träger gehalten (D-242)

**Der Antrag hatte drei Zuschnitte und fünfzehn weitere Läufe veranschlagt.** Gegen die
Träger gehalten ist die vermutete Teilung nicht herstellbar:

| Gegenstand einer Zelle | `SKILL.md` | `30-role-requirements-engineering.md` | `ROLE_PACK.md` |
|---|---|---|---|
| EARS, alle fünf Muster als Tabelle | ✔ | ✔ | ✔ Abschnitt 6 |
| Anforderung / Befund / Randbedingung | ✔ | ✔ | ✔ Abschnitt 2 |
| M1-Grenzen, V3, V11 | ✔ | ✔ | ✔ Abschnitt 1 |
| Rückfrage bei unbekanntem `<ISSUE_TRACKER>` | ✔ | ✔ | ✔ Abschnitt 5 |
| Datenschutz des Packs | ✔ | ✔ | ✔ Abschnitt 8 |
| **Ausgabegerüst** | ✔ Abschnitt 5 | – | – |

➡️ **`ohnepack`:** Der Zuschnitt entfernt, was die Aktivierung installiert, und läßt die
Kernregelschicht stehen. **Kein zusätzlicher Lauf.**

**Wirkungsnachweis am Baum von Bündel 5:**

| Schritt | Skills in `.claude/skills/` | `Skill()`-Einträge | Rollenregel | `SKILL.md` im Baum |
|---|---|---|---|---|
| nach `install.py` und Füllschritt | 12 | 12 | – | 13 |
| nach der Aktivierung | **13** | **13** | ✔ | 14 |
| nach `ohnepack` | **0** | 12 | – | **0** |

Der Zuschnitt meldet dabei: **3 Träger entfernt** (Laufzeitfassung, Skillablage,
kanonisches Packverzeichnis), **1 Korbeintrag gestrichen**, **3 Ablagen geleert**.
`CLAUDE.md`, `.claude/rules/00-framework-core.md` und `10-privacy-security.md` stehen.

⚠️ **Preis, benannt:** Aktiviert wird, was die Messung braucht. Das Overlay des
Übungsrepositoriums führt daneben `software-development` als aktiv; es trägt keinen
Skill, keine Zelle nennt es, und es fehlte auch in allen 38 Bäumen von Bündel 4
(`K-44`). Der Baum trägt es deshalb nicht.

## 3. Befund: Prüfung 37 verbietet, was Prüfung 72 verlangt (D-243)

**Gemessen am fertig aktivierten Baum:**

```
FEHLER  .claude/settings.json: der allow-Korb führt 1 Regel(n), die die Kernquelle
        nicht erzeugt, bei 0 gefüllten Platzhalterschlitz(en): Skill(role-re-ticket).
```

| Prüfung | Aussage zum selben Eintrag |
|---|---|
| **72** (neu mit `0.81.0`, D-238) | er **muß** dastehen – sonst fällt der Aufruf in die Abweisung |
| **37** (seit `0.38.0`, D-77) | er ist eine **Ausweitung** – die Kernquelle erzeugt ihn nicht |

🔴 **`0.81.0` konnte es nicht sehen:** Dort wurde *vor* dem dritten Teil gemessen – 13
Skills gegen 12 Einträge, Validator 0 Fehler. **Die Meldung entsteht erst durch die
Abhilfe.** Damit war D-238 in keinem übernehmenden Projekt umsetzbar, ohne den eigenen
Validator rot zu färben.

**Abhilfe:** Prüfung 37 leitet die zulässigen Skillfreigaben aus der **Skillablage** ab
(`skillfreigaben()`). **Belegt durch ein Paar:**

| Einheit | Fall | Erwartung | Ergebnis |
|---|---|---|---|
| Gegenprobe 37c | Skill in der Ablage **und** im Korb | keine Meldung | **OK** |
| Sonde 37h | `Skill(role-gibt-es-nicht)`, kein Skill in der Ablage | Ausweitung wird gemeldet | **OK** |

> *Wer eine Prüfung baut, die etwas VERLANGT, fragt, ob eine andere desselben
> Repositoriums es VERBIETET.*

## 4. Befund: „kopieren" ist für `claude-code` falsch (D-244)

| Weg | Validator an `.claude/rules/30-role-requirements-engineering.md` |
|---|---|
| `cp`, wie `framework/role-packs/README.md` es vorschrieb | **2 Fehler** – `description` und `trigger` sind Felder, die dieser Client für Regeldateien nicht auswertet (`K-18`) |
| über `render_rule()` des Frameworks | **0** – Kommentarblock, Ladeverhalten ausgewiesen |

Der gerenderte Kopf weist die Verschärfung aus: *„Dieser Client kennt für Regeldateien
nur die Bedingung über Dateimuster; gegenüber `model_decision` ist unbedingtes Laden
eine Verschärfung, keine Lockerung."*

🔴 **Der erste Versuch war eine Zusage ohne Wirkung.** `render_rule()` steigt aus, wenn
der Text nicht mit dem Zeilenvorschub nach den drei Strichen beginnt; die Quelle ist
CRLF, und mit erhaltenen Zeilenenden gelesen kam sie **unverändert** zurück. Der Baum
sah danach aus wie vorher, und der Aufruf stand im Quelltext.

➡️ Der Apparat legt die Quelle flach **und prüft danach, ob die Abbildung gegriffen
hat** – ein Vorhandensein belegt sich selbst, eine Wirkung nicht.

## 5. `UEB-30`: der Wert stand in drei Trägern (D-245)

| Träger | vorher | jetzt |
|---|---|---|
| `project-overlay/OVERLAY.md` Abschnitt 13 | `ISSUE_TRACKER` in Prosa, **ohne** spitze Klammern | eigene Wertzeile, gebunden, Wert `GitHub Issues` |
| `.devin/rules/20-project-overlay.md` | *„Ausgabeformat: Markdown (Ticketsystem des Projekts: GitHub Issues)"* | Bindung ohne Wert, Verweis auf Abschnitt 13 |
| `README.md` des Übungsrepositoriums | *„in diesem Projekt sind es GitHub Issues, also Markdown"* | Verweis auf Abschnitt 13 |

**Eine Präparation, die nur den ersten zurücknimmt, nimmt nichts zurück.**

**Die Form des zurückgenommenen Werts, gemessen:**

| Wert der Zelle | `--strict-overlay` im Übungsrepositorium |
|---|---|
| `<TBD: Ticketsystem des Projekts>` | **1 Fehler** – Abschnitt 13 ist ein sicherheitsrelevanter Abschnitt |
| `nicht festgelegt` | **0** |

➡️ **`nicht festgelegt`.** Die **Bindung** bleibt in beiden Fällen; verloren geht der
**Wert**. Mit dem Schlitz wäre `RE-001-N09` nur in einem Baum fahrbar, den das eigene
Repositorium beanstandet – der Widerspruch, gegen den Prüfung 57 gebaut ist, eine
Prüfung weiter.

**Wirkungsnachweis der Präparation:** Prüfsumme von `OVERLAY.md` vor dem Setzen und nach
dem Entfernen identisch (`01614f1f…`); Validator in **beiden** Zuständen 0 Fehler.

## 6. `UEB-31`: der erste Fachbegriff hätte eine abgenommene Zelle entwertet (D-246)

| Begriff | Fundstellen im Übungsrepositorium | Urteil |
|---|---|---|
| *Vormerkung* | 0 im Code – **aber** der abgenommene Beleg von `SK-009-N02` stützt sich wörtlich auf dieses Fehlen. **Gezählt über 14 Blätter: genau eine abgenommene Zelle tut das** | **fällt aus** |
| *Fernleihe* | **0** über Quellcode, Verträge, Migrationen, Dokumentation | gewählt |

Das ist D-137 eine Ebene weiter außen: Dort verdrängt eine Präparation den Gegenstand
einer anderen Präparation, bei `K-72` den einer Zelle – hier den **Beleg einer bereits
abgenommenen Zelle**.

🔴 **Und der Verrat-Wächter hätte die Quelle durchgelassen.** Sein Muster führte die
Kennungsfamilie `SK-` mit drei Ziffern wörtlich; Bündel 5 heißt `RE-001-*`. Er
beschreibt die Familie jetzt als Form.

## 7. `K-88`: Prüfung 55b prüft eine Teilzeichenkette – gezählt

| Messung am Übungs-Overlay | Zahl |
|---|---|
| Pflichtplatzhalter im Register | 29 |
| davon von der Laufzeitschicht genannt | 26 |
| **von Prüfung 55b heute gemeldet** | **0** |
| gemeldet, wenn sie spitze Klammern verlangte | **14** |
| gemeldet, wenn zusätzlich der Änderungsverlauf des Overlays nicht zählte | **15** |

🔴 **`<ISSUE_TRACKER>` stand mit spitzen Klammern ausschließlich im Eintrag `0.63.0` des
Änderungsverlaufs** – in dem Satz, der meldet, acht Pflichtplatzhalter seien *„jetzt
GEBUNDEN statt ersetzt"*.

⚠️ **Hier nicht behoben.** Vierzehn Platzhalter zu binden ist ein Eingriff in den
Meßgegenstand, wenige Tage vor dem Meßtag – dieselbe Zurückhaltung wie bei `K-79` vor
Bündel 4. **Und es ist nicht nur Text:** Die Laufzeitfassung steht mit 5.963 Zeichen
dicht an ihrer SOLL-Grenze von 6.000; **eine einzige weitere Bindung hat sie in diesem
Release bereits darüber gehoben** (6.099) und mußte an anderer Stelle wieder eingespart
werden.

## 8. Der Stand der fünfzehn Zellen nach der Herrichtung

| | Zellen |
|---|---|
| **tragen** | `P01`, `P02`, `P03`, `N01`–`N08` – **elf**, unverändert |
| **jetzt vollständig** | `P04` (echte Wertzeile), `P05` (Vorbedingung präzisiert), `N09` (`UEB-30`), `N10` (`UEB-31`) |
| **fahrbar** | **alle fünfzehn** – der Meßbaum trägt den Skill, die Rollenregel und den Korbeintrag |

## 9. Was dieses Release gebaut hat

| Artefakt | Gegenstand |
|---|---|
| `tests/erhebungen/packaktivierung.py` | Aktivierung (drei Teile, drei Wächter), Umkehrung, Skillschnitt an **einer** Stelle |
| `tests/erhebungen/ablage.py` | `blaetter()`, `skillmenge()`, `zellkennung()` – die Zuordnung Zelle → Skill wird abgeleitet |
| `tests/erhebungen/baeume-b4.py` | Klasse `ohnepack`, `--zellen` |
| `tests/erhebungen/umgebungen-bauen-b4.py` | abgeleiteter Wächter, Aktivierung, Korbprüfung |
| Prüfung 37 | Skillfreigaben aus der Ablage abgeleitet; Sonde 37h, Gegenprobe 37c |
| `role-packs/README.md`, `ROLE_PACK.md` 0.1.2 | die Aktivierung hat vier Schritte |
| Übungsrepositorium | `<ISSUE_TRACKER>` gebunden, `UEB-30` und `UEB-31`, Verrat-Wächter, Mentorenblatt |
| `role-re-ticket/TESTS.md` | vier Vorbedingungen |

## 10. Der Durchgang vor dem Commit

🔴 **Zwei Zahlen waren in diesem Durchgang falsch, bevor sie geschrieben wurden.**

1. **Der erste Trockenlauf des Hebens lief gegen `HEAD` statt gegen den Arbeitsbaum** und
   sagte **zwei** Dateien außerhalb von `leitwerk-core/` voraus. Gegen den Arbeitsbaum
   gefahren sind es **drei** – die dritte ist `.devin/skills/role-re-ticket/TESTS.md`
   *(aus dem Pack aktualisiert)*, also genau die Zusage, die `CR-2026-114` Abschnitt 2
   gemessen hat. *Ein Trockenlauf gegen den committeten Stand mißt den Vorstand gegen
   sich selbst.*
2. **Das Hilfsskript für die Textersetzungen schrieb zwei von drei Ersetzungen
   weg.** Es las je Auftrag frisch von der Platte und schrieb am Ende jede Fassung
   einzeln – die letzte gewann. Der Lauf meldete dreimal *„geschrieben"*. **Gefunden,
   weil die eingefügte Funktion danach nicht existierte**, nicht weil das Werkzeug es
   gesagt hätte.

⚠️ **Und zweimal ist eine Escape-Ebene verlorengegangen**, beide Male in einem
Bash-Heredoc mit deutscher Prosa: einmal wurde aus der Zeichenfolge für einen
Zeilenvorschub ein echter Zeilenumbruch mitten im Quelltext, einmal beendete ein gerades
Anführungszeichen den Python-String. **Beides steht seit `0.77.0` im Arbeitswissen, und
beides ist wieder passiert.** ➡️ Für jeden Text mit Escapes oder deutscher Prosa: das
`Write`-Werkzeug und eine Datei, nie ein Heredoc.

## 11. Abnahme

| Prüfung | Ergebnis |
|---|---|
| `validate-framework.py` im Framework | **0 Fehler, 0 Warnungen** |
| `validate-framework.py --strict-overlay` im Übungsrepositorium | **0 Fehler, 0 Warnungen**; Suite **59 grün**, `tsc --noEmit` sauber |
| `probe-pruefungen.py` in beiden Kodierungsumgebungen | **alle 290 Einheiten bestanden** – je 395 Ergebniszeilen mit `OK` und 23 Bündelköpfe, keine Zeile ohne `OK`, Rückgabewert 0; **360,8 s** und **359,8 s** Wanduhr auf acht Bahnen |
| Kriterium 2 | `zaehlen46.py`: Katalog 4 \| Testblätter 15 \| **Summe 19** – gedeckt mit der Standzeile der Roadmap |
| Heben des Übungsrepositoriums | **drei** Dateien außerhalb von `leitwerk-core/`, vorhergesagt und getroffen: die Testblätter von `role-re-ticket`, `fw-mr-description` und `fw-review-support` |
| Meßbaum `C:\lw-b5` | nach der Abnahme entfernt |
