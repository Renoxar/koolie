# Wirkungsnachweise 0.57.0

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-18 |
| Framework-Version | `0.57.0` (Vorstand `0.56.2`, Commit `e9f4367`) |
| Antrag | `CR-2026-080`, D-128, `K-52` neu |
| Gegenstand | **Die Clientbindung des werkzeugneutralen Kerns.** Siebzehn Fundstellen in vierzehn anweisenden Trägern aufgelöst; **Prüfung 48** neu, die die Neutralitätsregel durchsetzt; `OPTIONAL_RUNTIME_RE` entfernt |
| Prüfmethode | Validatorlauf gegen den fertigen Baum; Sondenlauf `probe-pruefungen.py .` in **beiden** Kodierungsumgebungen (D-49); **Gegenbeweis gegen den unberührten Vorstand**; drei Zuschnitte zur entfernten Ausnahme; Trockenlauf `install.py --update --dry-run` gegen je eine Kopie beider übernehmender Projekte |
| Ergebnis | **Validator 0 Fehler, 0 Warnungen; 261 Ergebniszeilen bestanden in beiden Kodierungsumgebungen.** Der Gegenbeweis meldet gegen `0.56.2` **genau 17 Fundstellen in genau 14 Trägern** |

---

## 1. Was dieses Release NICHT tut

**Es bewegt keine Zahl von D-11.** Kriterium 2 steht vor und nach diesem Release auf
**105**, Kriterium 1 auf **23**. Prüfung 46 meldet nichts, und das ist hier das erwartete
Ergebnis.

**Es ändert keine Zusage über das Verhalten eines Clients.** Geändert sind die Worte, mit
denen der Kern die Laufzeitschicht bezeichnet – nicht, was sie tut.

---

## 2. Der stärkste Nachweis: der neue Validator gegen den unberührten Vorstand

Dasselbe Release entfernt die siebzehn Fundstellen **und** baut die Prüfung, die sie finden
soll. Ein Lauf gegen den fertigen Baum meldet deshalb null – und belegt nichts über die
Wirkung. **Der Gegenbeweis braucht den unberührten Vorstand.**

```
git archive e9f4367 | tar -x -C <vorstand>          # 0.56.2, unveraendert
cp <arbeitsbaum>/leitwerk-core/tests/scripts/validate-framework.py <vorstand>/...
python <arbeitsbaum>/leitwerk-core/install.py --client devin-desktop --root <vorstand>
python <vorstand>/leitwerk-core/tests/scripts/validate-framework.py --root <vorstand>
```

> 🟢 **Ergebnis: genau 17 Meldungen in genau 14 Trägern** – die Aufzählung des Antrags,
> **ohne Rest und ohne Überschuss.**

| Träger | Meldungen | Marke |
|---|---|---|
| `prompts/01`, `02`, `03`, `05`, `06`, `07` | je 1 | Skill-Ablage |
| `framework/role-packs/README.md` | 2 | Regelablage, Skill-Ablage |
| `framework/tech-packs/_template/TECH_PACK.md` | 2 | Regelablage |
| `tests/TEST_CATALOG.md` | 2 | Wurzel-Anweisungsdatei (Zeilen 112 und 136) |
| `framework/core/08-skill-conventions.md` | 1 | Skill-Ablage |
| `framework/role-packs/_template/ROLE_PACK.md` | 1 | Regelablage |
| `governance/CHANGE_REQUEST_TEMPLATE.md` | 1 | Berechtigungsdatei |
| `decision-trees/03-analyze-or-modify.md` | 1 | Wurzel-Anweisungsdatei |
| `tests/EDGE_CASES.md` | 1 | Wurzel-Anweisungsdatei |

**Das belegt drei Dinge auf einmal:** dass die Prüfung ihren Gegenstand trifft, dass die
Aufzählung des Antrags vollständig war – und dass sie **nicht zu groß** war, denn die
Ausnahmemenge hält: `tests/scripts/` (44 Treffer einer Vorabzählung), `docs/ROADMAP.md`
(10) und die neun Ergebnisstatus-Zellen des Testkatalogs bleiben unbeanstandet.

> 🔴 **Und das ist in diesem Projekt der seltenere Ausgang.** Die Aufgabenbeschreibung war
> zehnmal in Folge zu klein. Hier hält sie – **weil sie vor dem Eingriff unabhängig
> nachgezählt worden ist**, mit abgeleiteten statt gepflegten Marken, über alle
> Textendungen und ohne Doppelzählung derselben Stelle. Die Vorabzählung ergab 80 Treffer
> in 18 Trägern; nach Abzug der drei Ausnahmegattungen blieben 17 in 14.

---

## 3. Der dritte Grund für die Prüflücke – und wie er beim Messen kleiner wurde

Der Befund nannte zwei Gründe, aus denen Prüfung 12 die siebzehn Stellen nie gemeldet hat:
nur Token in Backticks, nur Pfade, die es nicht gibt. **Beim Nachlesen kam ein dritter
dazu:** `LINK_ROOTS` führte wörtlich `.devin/`, `AGENTS.md` und `AGENTS.local.md` – die
Pfade des anderen Packs waren gar kein Kandidat der Heuristik.

**Daraus wurde eine Hypothese mit Mechanismus, also eine widerlegbare:** In einer
Installation des Packs `claude-code` müsste ein Kerntext, der auf die Laufzeitfassung eines
aktivierten Role Packs verweist (`…/rules/30-role-…`), als **toter Pfad** gemeldet werden –
denn die zuständige Ausnahme `OPTIONAL_RUNTIME_RE` kannte ebenfalls nur `.devin/`.

**Drei Zuschnitte, je eine frische Installation aus dem Vorstand:**

| # | Zuschnitt | Ergebnis |
|---|---|---|
| 1 | `claude-code` installiert, Kerntext mit `` `.claude/rules/30-role-software-development.md` ``, **alter** Validator | **nichts gemeldet** – der Pfad ist kein Kandidat der Wurzelliste |
| 2 | dieselbe Lage, **neuer** Validator | **nichts gemeldet** – der Pfad ist jetzt Kandidat und wird von der Fremdpfaderkennung gedeckt |
| 3 | neuer Validator, Ausnahme ausgeschaltet (`re.compile(r"(?!)")`), Verweis in der Chronik | **nichts gemeldet** – die Ausnahme ist unerreichbar |

> 🔴 **Die Hypothese ist widerlegt, und die Widerlegung ist der eigentliche Befund.**
> `LINK_ROOTS` und `OPTIONAL_RUNTIME_RE` waren in **derselben Richtung** zu eng und haben
> einander gedeckt: Die erste Enge verhinderte, dass die zweite je auffiel. **Einzeln wäre
> jede aufgefallen; zusammen sahen sie aus wie ein Lauf ohne Befund.**

**Zuschnitt 3 ist der, den die Übergabe verlangt** – *„Bei einem Laufzeitbefund gehören alle
Zuschnitte gemessen, bevor man ihn einordnet: Zwei Messpunkte verführen zu einer Aussage,
die der dritte umwirft."* Hier hat der dritte sie umgeworfen.

**Zwei Folgen:**

1. **`OPTIONAL_RUNTIME_RE` ist entfernt**, nicht abgeleitet. Sobald die
   Client-Bindungs-Warnung nach Prüfung 48 wandert, deckt die Fremdpfaderkennung denselben
   Fall vollständig ab. *Eine Ausnahme, die nichts mehr ausnimmt, ist schlimmer als keine:
   Sie sieht wie Sorgfalt aus.*
2. 🟢 **Die Ableitung von `LINK_ROOTS` bleibt – ohne gemessene Wirkung, und das steht so im
   Quelltext.** Sie schafft eine von Hand gepflegte Clientliste ab, die ein drittes Client
   Pack (`openai-codex`, `1.1.0`) nachtragen müsste und die niemand nachzählt. **Die
   Versuchung, ihr nachträglich eine Wirkung anzudichten, ist der eigentliche Preis dieser
   Änderung.**

---

## 4. Prüfung 48 – vier Sonden, drei Gegenproben

| Einheit | Was sie belegt |
|---|---|
| Sonde `48a` | Der Pfad des **installierten** Packs in einem Kernträger wird gemeldet – genau der Fall, den Prüfung 12 nie sah (Grund 2) |
| Sonde `48b` | Ein Clientpfad **ohne Backticks** wird gemeldet (Grund 1) |
| Sonde `48c` | Ein Clientpfad in einer **anweisenden** Spalte des Testkatalogs wird gemeldet, obwohl die letzte Zelle ausgenommen ist |
| Sonde `48d` | Ohne `runtime_placeholders` in den Manifesten meldet die Prüfung ihren **verlorenen Gegenstand** selbst, statt leise zu bestehen (D-23) |
| Gegenprobe `48a` | Das unveränderte Repositorium bleibt unbeanstandet |
| Gegenprobe `48b` | Derselbe Pfad in der **Ergebnisstatuszelle** bleibt zulässig – dort ist er Beleg (D-117) |
| Gegenprobe `48c` | Ein Clientpfad in `docs/ROADMAP.md` bleibt zulässig – sie führt die Erhebungen je Arbeitspaket |

> 🟢 **Sonde `48c` und Gegenprobe `48b` sind ein Paar und stehen für sich:** Sie setzen
> denselben Pfad in **dieselbe Tabelle** – einmal in eine anweisende Spalte, einmal in die
> letzte Zelle. Der erste Fall wird gemeldet, der zweite nicht. **Damit ist der Zuschnitt
> belegt und nicht behauptet**; ein Zuschnitt, der die Zeile statt der Spalte genommen
> hätte, hätte genau die Eingabezelle mit herausgenommen, in der bis 0.56.2 *„Passe
> AGENTS.md an"* stand.

**Die Sonden raten ihren Pfad nicht, sie lesen ihn** aus den Manifesten der Kopie – und sie
unterscheiden dabei das **installierte** vom **nicht installierten** Pack, weil genau diese
Unterscheidung der zweite Grund für die Blindheit von Prüfung 12 ist. Findet eine Sonde
weniger als zwei Packs oder keine Laufzeitschicht im Baum, bricht sie als
**Präparationsfehler** ab, statt etwas anderes zu messen.

---

## 5. Die Läufe

### 5.1 Validator

```
python leitwerk-core/tests/scripts/validate-framework.py
Ergebnis: 0 Fehler, 0 Warnungen
```

**Ein Zwischenstand gehört dazu, weil er eine Regel bestätigt hat:** Nach dem Einbau von
Prüfung 48 und vor dem Bau ihrer Sonden meldete **Prüfung 40** einen Fehler – die
Sondenmenge stand noch auf *„6 und 18 bis 47"*. **Das ist die Reihenfolge, die der
Prüfapparat selbst erzwingt:** erst die Sonde, dann die Spanne. Eine Prüfung, deren Nummer
im Register steht, bevor ihre Sonde existiert, fällt – und das ist richtig.

### 5.2 Sondenlauf

```
python leitwerk-core/tests/scripts/probe-pruefungen.py .
Ergebnis: alle Sonden und Gegenproben bestanden
```

**Beide Kodierungsumgebungen, zeilengleich** (Abnahmeauflage aus D-49):

| Lauf | Ergebniszeilen | Abweichungen | Wanduhr |
|---|---|---|---|
| mit `PYTHONIOENCODING=utf-8` | **261** | 0 | 159,4 s auf 8 Bahnen |
| ohne | **261** | 0 | 151,1 s auf 8 Bahnen |

**261 = 163 Sonden, 68 Gegenproben, 12 Selbstproben, 18 Bündelkopfzeilen.** Der Vorstand
stand auf 254 (159/65/12/18); **die Differenz ist genau die dieses Releases** – vier Sonden
und drei Gegenproben zu Prüfung 48, keine weitere.

**Die Laufzeiten stehen unterhalb der Trennlinie** (D-94) und sind nicht Teil des
zeilengleichen Vergleichs.

### 5.3 Trockenlauf beider übernehmender Projekte

| Projekt | Ergebnis |
|---|---|
| Pilot `otp-generator` | **0 angelegt, 0 aktualisiert**, 58 unverändert, 20 Projektdateien behalten |
| Übungsrepositorium `test-devin-framework` | **0 angelegt, 0 aktualisiert**, 64 unverändert, 20 Projektdateien behalten |

**Der Migrationshinweis ist damit gemessen, nicht abgeleitet** – und sein Ergebnis ist
dasselbe Argument wie E1 des Antrags: **Keiner der vierzehn geänderten Träger wird
gerendert.** Genau deshalb hilft dort kein Platzhalter, und genau deshalb erreicht die
Änderung kein übernehmendes Projekt.

> ⚠️ **Ein Umgebungsbefund, keine Framework-Sache, aber er kostet sonst wieder zehn
> Minuten:** Der erste Trockenlauf gegen das Übungsrepositorium brach mit
> `FileNotFoundError` auf eine Datei ab, die es gibt. Ursache ist die **Pfadlänge**: Das
> Scratchpad-Verzeichnis dieser Sitzung plus der Pfad der Role-Pack-Laufzeitfassung
> überschreitet die 260 Zeichen von Windows. **Ein Trockenlauf gehört an einen kurzen
> Pfad** (gemessen unter `C:\lw-mig`).

---

## 6. Zahlen dieses Releases, nachgezählt

| Zahl | Wert | Wie gezählt |
|---|---|---|
| Fundstellen | **17** | Gegenbeweis gegen den Vorstand; vorab unabhängig aus 80 Treffern in 18 Trägern abgeleitet |
| Anweisende Träger | **14** | dieselben beiden Zählungen |
| Ersetzungen im Patchskript | **15** | Zwei Ersetzungen deckten je zwei Fundstellen (`role-packs/README.md`, `TECH_PACK.md`) |
| Prüfungen | **47 → 48** | Register im Kopfkommentar, von Prüfung 40 nachgezählt |
| Marken von Prüfung 48 | **16** | aus den `runtime_placeholders` beider Manifeste abgeleitet, `<CLIENT_NAME>` und `<CORE_DIR>` ausgenommen |
| Produktnamen-Nennungen (`K-52`) | **15 in 10 Trägern** | eigene Zählung; **nicht** Gegenstand dieses Releases |
| Versionszellen gehoben | **11** | die beiden Pack-Vorlagen bewusst **nicht** (`K-37`) |

---

## 7. Was offen bleibt

- **`K-52`** – die Produktnamen. Zwei Träger tragen sie im Titel. D-28 erlaubt den Namen,
  *wo ein Produkt gemeint ist*; ob das auch gilt, wo der Kern ein Werkzeug **voraussetzt**,
  ist nicht entschieden.
- **`K-37`** – die Versionszelle der beiden Pack-Vorlagen, hier bewusst nicht angefasst.
- **Die `build/`-Ausnahme hat eine Frist und keine Prüfung, die sie mahnt.** Sie steht als
  Zeile bei `AP11` in der Roadmap. **Das ist die Bauform, an der dieses Projekt schon
  gescheitert ist** – ein Eintrag ohne Prüfung –, und sie ist hier bewusst gewählt, weil
  eine maschinell bekannte Frist nicht gebaut ist.
- **`G-14` hat sein Beispiel verloren.** Der Grenzfall über zwei Dateinamen, die sich nur in
  der Schreibung unterscheiden, steht jetzt ohne die beiden Namen da. Der Grenzfall ist
  derselbe; seine Anschaulichkeit ist der Preis der Neutralität.

---

## 8. Gegenzeichnung

| Feld | Inhalt |
|---|---|
| Durchgeführt von | KI-Client im Entwicklungsprofil (`governance/FRAMEWORK_DEV_PROFILE.md`) |
| Gegengezeichnet | `<TBD: Rolle, Datum>` |
