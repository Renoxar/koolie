# Wirkungsnachweise 0.57.1

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-18 |
| Framework-Version | `0.57.1` (Vorstand `0.57.0`, Commit `7b06b72`) |
| Antrag | `CR-2026-081`, D-129, `K-52` geschlossen |
| Gegenstand | **Der Produktname im Kern.** Fünfzehn Nennungen in zwölf anweisenden Trägern aufgelöst; D-28 mit **D-129** verschärft; Prüfung 14 verschärft und **erstmals mit Sonden** belegt; eine gemeinsame Ausnahmemenge für die Prüfungen 14 und 48 |
| Prüfmethode | Validatorlauf gegen den fertigen Baum; Sondenlauf `probe-pruefungen.py .` in **beiden** Kodierungsumgebungen (D-49); **Gegenbeweis gegen den unberührten Vorstand**; Trockenlauf `install.py --update --dry-run` gegen je eine Kopie beider übernehmender Projekte |
| Ergebnis | **Validator 0 Fehler, 0 Warnungen; 268 Ergebniszeilen bestanden in beiden Kodierungsumgebungen.** Der Gegenbeweis meldet gegen `0.57.0` **genau 15 Fundstellen in genau 12 Trägern** |

---

## 1. Was dieses Release NICHT tut

**Es bewegt keine Zahl von D-11.** Kriterium 2 steht vor und nach diesem Release auf
**105**, Kriterium 1 auf **23**.

**Es ändert keine Zusage über das Verhalten eines Clients.** Wo der Kern bisher eine
Produkteigenschaft behauptete, verweist er jetzt auf die Fähigkeitsmatrix des Packs – die
Aussage bleibt dieselbe, nur steht sie an der Stelle, die sie belegen kann.

---

## 2. Zuerst: zwei Berichtigungen an der eigenen Vorgängerzeile

`K-52` ist mit `0.57.0` eröffnet worden und nannte **„fünfzehn Fundstellen in zehn
Trägern"**; dazu stand dort, in den gerenderten Trägern hülfe `<CLIENT_NAME>`.

> 🔴 **Beides war falsch, und beides ist beim Nachzählen VOR dem Eingriff aufgefallen.**
>
> 1. **Es sind zwölf Träger, nicht zehn.** Die beiden Plan-Skills waren im Fließtext als
>    „die Skills" erwähnt und in der Trägerzahl nicht mitgezählt. **Die Zahl der
>    Fundstellen war richtig, die der Träger nicht.**
> 2. **`<CLIENT_NAME>` hilft in keiner der fünfzehn Fundstellen** – auch nicht in den drei
>    gerenderten. Begründung in Abschnitt 4.

**Das ist der wiederkehrende Befundtyp, und er hat diesmal die eigene Notiz getroffen** –
in einem Projekt, dessen Arbeitswissen den Satz führt: *„Wer hier eine Zahl liest, zählt
sie nach – auch die eigene, und besonders die im eigenen Protokoll."* **Die Zählung war
zum elften Mal in zwölf Releases zu klein.**

**Die Berichtigung steht in der Statuszelle von `K-52`.** `CR-2026-080`, das Protokoll zu
0.57.0 und der Roadmap-Abschnitt behalten ihren Wortlaut und tragen einen Nachtrag –
dieselbe Entscheidung wie bei 0.54.1 und 0.55.0.

---

## 3. Der stärkste Nachweis: die verschärfte Prüfung gegen den unberührten Vorstand

```
git archive 7b06b72 | tar -x -C <vorstand>          # 0.57.0, unveraendert
cp <arbeitsbaum>/leitwerk-core/tests/scripts/validate-framework.py <vorstand>/...
python <arbeitsbaum>/leitwerk-core/install.py --client devin-desktop --root <vorstand>
python <vorstand>/leitwerk-core/tests/scripts/validate-framework.py --root <vorstand>
```

> 🟢 **Ergebnis: genau 15 Meldungen in genau 12 Trägern** – die Aufzählung des Antrags,
> **ohne Rest und ohne Überschuss.**

| Träger | Meldungen | Was der Name dort trug |
|---|---|---|
| `onboarding/GUIDE.md` | 2 | Titel und Voraussetzung |
| `onboarding/QUICKSTART.md` | 2 | Titel und Arbeitsschritt |
| `framework/core/02-privacy.md` | 2 | Produktaussage `[DOK]` und Überschrift eines normativen Abschnitts |
| `framework/core/00-principles.md` | 1 | Reichweite der Belegstatus-Regel |
| `framework/core/01-governance.md` | 1 | **Geltungsbereich des ganzen Frameworks** |
| `framework/skills/fw-plan/SKILL.md` | 1 | Produktaussage `[DOK]` (Plan-Modus) |
| `framework/skills/fw-bugfix-prepare/SKILL.md` | 1 | dieselbe |
| `framework/org-policies/README.md` | 1 | Nachweisgegenstand |
| `governance/RELEASE_PROCESS.md` | 1 | Quellenpflicht des Review-Zyklus |
| `checklists/09-onboarding.md` | 1 | Voraussetzung |
| `prompts/README.md` | 1 | Zweck der Bibliothek |
| `templates/project-overlay/OVERLAY.md` | 1 | produktspezifische Optionsliste |

**Und eine zweite, unabhängige Zählung davor kommt auf dasselbe:** Eine eigene
Auszählung mit aus den Manifesten abgeleiteten Namen über alle Textendungen ergab **20
Treffer in 13 Trägern**, davon **5 im Validator** (Werkzeug, und sein Text beschrieb die
Ausnahme, die jetzt fällt) – bleiben **15 in 12**.

> 🔴 **Die Ausnahme aus D-28 hatte in ihrem eigenen Geltungsbereich keinen einzigen
> berechtigten Fall.** Sie erlaubte den Produktnamen, *wo ein Produkt gemeint ist* – und
> in allen fünfzehn Fundstellen war kein Produkt gemeint, sondern eine Eigenschaft, ein
> Geltungsbereich oder eine Voraussetzung. Client Packs und Chronik sind ohnehin
> ausgenommen; übrig blieb nur der Kern, und dort schreibt der Name immer zu.

---

## 4. Warum `<CLIENT_NAME>` nicht hilft – die Trennlinie ist eine andere

`0.57.0` hat nach **gerendert / nicht gerendert** entschieden. Hier greift das zu kurz:

| Träger (gerendert) | Was dort stand | Was `<CLIENT_NAME>` daraus gemacht hätte |
|---|---|---|
| beide Plan-Skills | *„im Plan-Modus von \<Produkt\> liegt die Plan-Datei unter `~/<RUNTIME_DIR>/plans/` … `[DOK]`"* | Für jedes andere Pack eine **unbelegte Behauptung** |
| `OVERLAY.md` | *„nur \<Produkt\> lokal / zusätzlich **Cloud-Sessions / CLI**"* | Den Namen getauscht und die **falschen Optionen stehen gelassen** |

**Die tragfähige Trennlinie ist: Nennen gegen Zuschreiben.**

- **Nennen** – der Text trägt den Namen und sagt nichts über das Produkt → `<CLIENT_NAME>`,
  und nur in einer gerenderten Quelle.
- **Zuschreiben** – der Text sagt etwas *über* das Produkt → gehört ins Client Pack.

> 🟢 **Der Nennen-Fall ist im ganzen Bestand genau einmal angewandt, gezählt und nicht
> geschätzt:** `framework/runtime/root-instruction.md` trägt `<CLIENT_NAME>` im Titel. Alle
> übrigen Vorkommen sind Register, Chronik oder Quelltext, der ihn beschreibt. **Ein
> Platzhalter mit genau einem Fall ist kein toter Platzhalter** – und dieser eine Fall ist
> zugleich das Muster für die Regel.

---

## 5. Beim Umsetzen zugefallen: eine Zeilenkennung ist selbst clientgebunden

Der erste Entwurf der beiden Plan-Skills verwies auf **„Zeile M4 der Fähigkeitsmatrix
seines Client Packs"**. Gegengelesen am Bestand:

| Pack | Zeilen der Fähigkeitsmatrix (Modi) |
|---|---|
| `devin-desktop` | `M1` bis `M7` |
| `claude-code` | **`M1` bis `M3`** – **keine Zeile `M4`** |

> 🔴 **Der Verweis wäre für eines der beiden Packs ins Leere gegangen – dieselbe
> Client-Bindung eine Ebene tiefer, ausgerechnet in dem Satz, der sie beheben sollte.**
> **Keine Prüfung hätte es gemeldet:** Prüfung 31 rechnet die Summen *innerhalb* eines
> Packs nach und verlangt nirgends, dass zwei Packs dieselben Zeilen führen; Prüfung 12
> prüft Pfade, keine dokumentinternen Verweise (`K-48`).

**Abhilfe, als Regel im Glossar:** Ein Kerntext verweist auf die **Fähigkeitsmatrix**, nie
auf eine **Zeile** darin.

**Zum zweiten Mal in zwei Releases hat die erste Fassung der Abhilfe den Befund
wiederholt** – bei 0.57.0 war es der Verdacht auf eine Falschmeldung, den der dritte
Zuschnitt umwarf. **Die Lehre ist dieselbe: den eigenen Lösungsvorschlag gegenprüfen,
nicht nur den Befund.**

---

## 6. Prüfung 14 hatte seit 0.20.0 keine Sonde

Der Nachweissatz lautete *„für die Prüfungen 6 und 18 bis 48"*. **Prüfung 14 lag
außerhalb.** Nach D-23 galt sie damit als nicht vorhanden – und wird mit diesem Release
geändert.

**Ein dritter Befund fiel beim Nachbauen an:** `check_actor_naming` stieg bei fehlenden
Manifesten mit `if not namen: return` **still** aus.

| Einheit | Was sie belegt |
|---|---|
| Sonde `14a` | Der Produktname **mit Zusatz** in einem Kernträger wird gemeldet – die Ausnahme, die D-129 abgeschafft hat |
| Sonde `14b` | Der **bloße Name als Handelnder** wird weiterhin gemeldet – **die Verschärfung hat den alten Gegenstand nicht verloren** |
| Sonde `14c` | Ein **Platzhalter** mit Clientnamen wird gemeldet – er steht groß und entgeht der Namenssuche (der Fall aus `CR-2026-070`) |
| Sonde `14d` | Ohne `manifest.json` unter `clients/` meldet sie den **verlorenen Gegenstand** selbst, statt still auszusteigen (D-23) |
| Gegenprobe `14a` | Das unveränderte Repositorium bleibt unbeanstandet |
| Gegenprobe `14b` | Ein Produktname in einem **Protokoll** bleibt zulässig – Chronik |
| Gegenprobe `14c` | **`<CLIENT_NAME>` in einer gerenderten Quelle bleibt zulässig** – der Weg, den D-129 offen lässt |

> 🟢 **Sonde `14b` ist die wichtigste der vier.** Eine verschärfte Prüfung darf den Fall
> ihrer Vorgängerin nicht mitnehmen; ohne diese Sonde wäre nicht belegt, dass sie ihn noch
> hat. **Die Sonden lesen den Produktnamen aus den Manifesten der Kopie**, statt ihn zu
> schreiben – eine Sonde, die einen Namen rät, misst den geratenen Namen.

---

## 7. Eine Ausnahmemenge statt zweier – und eine dritte, die etwas anderes meinte

Prüfung 14 las `ACTOR_HISTORY`, Prüfung 48 las `ACTOR_HISTORY + (docs/ROADMAP.md,)`.

> 🔴 **Nach EINEM Release waren die beiden Listen für denselben Gegenstand schon
> auseinandergelaufen.** Seit 0.57.1 teilen sie sich `NEUTRAL_AUSNAHMEN`.

**Und ein dritter Nutzer derselben Liste meinte etwas ganz anderes:** Prüfung 13 fragt,
welches Dokument eine **eigene Artefaktversion** trägt. `docs/ROADMAP.md` trägt eine und
gehört geprüft – wer die Liste für die Neutralität erweitert hätte, hätte Prüfung 13
stillschweigend mit erweitert. **Sie bekommt `OHNE_ARTEFAKTVERSION` mit eigenem Namen.**

**Die Liste sah aus wie ein Begriff und war eine Zufallsschnittmenge.**

---

## 8. Die Läufe

### 8.1 Validator

```
python leitwerk-core/tests/scripts/validate-framework.py
Ergebnis: 0 Fehler, 0 Warnungen
```

### 8.2 Sondenlauf

```
python leitwerk-core/tests/scripts/probe-pruefungen.py .
Ergebnis: alle Sonden und Gegenproben bestanden
```

**Beide Kodierungsumgebungen, zeilengleich** (Abnahmeauflage aus D-49):

| Lauf | Ergebniszeilen | Abweichungen | Wanduhr |
|---|---|---|---|
| mit `PYTHONIOENCODING=utf-8` | **268** | 0 | 163,4 s auf 8 Bahnen |
| ohne | **268** | 0 | 158,8 s auf 8 Bahnen |

**268 = 167 Sonden, 71 Gegenproben, 12 Selbstproben, 18 Bündelkopfzeilen.** Der Vorstand
stand auf 261 (163/68/12/18); **die Differenz ist genau die dieses Releases** – vier
Sonden und drei Gegenproben zu Prüfung 14, keine weitere.

**Die Laufzeiten stehen unterhalb der Trennlinie** (D-94) und sind nicht Teil des
zeilengleichen Vergleichs.

### 8.3 Trockenlauf beider übernehmender Projekte

| Projekt | Ergebnis |
|---|---|
| Pilot `otp-generator` | **0 angelegt, 4 aktualisiert**, 54 unverändert, 20 Projektdateien behalten |
| Übungsrepositorium `test-devin-framework` | **0 angelegt, 4 aktualisiert**, 60 unverändert, 20 Projektdateien behalten |

**Die vier sind je `SKILL.md` und `CHANGELOG.md` der beiden Plan-Skills** – nachgelesen in
der Ausgabe, nicht abgeleitet. **Die Overlay-Vorlage ist nicht darunter:** Sie ist
`shared_seed` und wird nur bei der Erstinstallation geschrieben; ein bestehendes Projekt
behält seine Fassung. **Das ist der Migrationshinweis, und er ist gemessen.**

> ⚠️ **Wieder am kurzen Pfad gemessen** (`C:\lw-mig`) – die Lehre aus 0.57.0 hat beim ersten
> Anlauf getragen.

---

## 9. Zahlen dieses Releases, nachgezählt

| Zahl | Wert | Wie gezählt |
|---|---|---|
| Fundstellen | **15** | eigene Auszählung (20 minus 5 im Werkzeug) **und** Gegenbeweis gegen den Vorstand |
| Anweisende Träger | **12** | dieselben beiden Zählungen – die Vorgängerzeile nannte zehn |
| Ersetzungen im Patchskript | **15** | eine je Fundstelle |
| Angewandte Fälle von `<CLIENT_NAME>` | **1** | `framework/runtime/root-instruction.md`, Titel |
| Weitere Hersteller-/Produktnamen im Kern | **0** | gesucht nach zehn weiteren Namen; kein Treffer außerhalb Chronik, Packs, Abbildungstabellen |
| Prüfungen mit Sonde | **6, 14 und 18 bis 48** | Prüfung 40 rechnet die Spanne aus und hält sie an drei Stellen wörtlich |
| Versionszellen gehoben | **11**, dazu zwei Skill-`CHANGELOG.md` | die Vorlagen ohne Versionszelle bleiben unberührt (`K-37`) |

---

## 10. Was offen bleibt

- **`K-37`** – die Versionszelle der Vorlagen, seit 0.53.0 unentschieden.
- **Prüfung 14 findet den Namen, nicht die Umschreibung.** Ein Kerntext, der „das Werkzeug
  aus Kapitel 3" schreibt, läuft durch.
- **Die Trennlinie *Nennen / Zuschreiben* ist eine Regel für Menschen.** Kein Skript
  entscheidet sie; die Prüfung macht nur den einen Fall unmöglich, in dem sie regelmäßig
  falsch beantwortet wurde.
- **Ein Verweis auf eine Zeile einer Fähigkeitsmatrix wird von nichts geprüft** (Abschnitt
  5). Die Regel steht im Glossar; ein Zähler dafür wäre `K-48` eine Ebene tiefer und ist
  nicht gebaut.
- **Die beiden Plan-Skills verlieren eine konkrete Pfadangabe.** Wer sie mit
  `devin-desktop` fährt, schlägt den Pfad jetzt im Client Pack nach.

---

## 11. Gegenzeichnung

| Feld | Inhalt |
|---|---|
| Durchgeführt von | KI-Client im Entwicklungsprofil (`governance/FRAMEWORK_DEV_PROFILE.md`) |
| Gegengezeichnet | `<TBD: Rolle, Datum>` |
