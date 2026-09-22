# Änderungsantrag `CR-2026-119`

| Feld | Inhalt |
|---|---|
| Titel | Die Umbenennung auf `Koolie` – vorgezogen vor den Rest von `AP2` |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-22 |
| Betroffene Artefakte | **der gesamte Bestand** – `leitwerk-core/` wird `koolie-core/`, `<CORE_DIR>` ändert seinen Wert, das Repositorium seinen Namen; dazu beide übernehmenden Projekte (`devpacks/otp-generator`, `devpacks/test-devin-framework`) |
| Ebene laut Entscheidungsbaum 6 | **Core**, mit Wirkung auf jede Installation |
| Art | **Umbenennungslauf ohne Kontingent** – kein Lauf an einem Client, keine Modellzeit |
| Dringlichkeit | 🔴 **Terminiert.** Die Vorführung ist am 2026-09-24; die Umbenennung soll am 2026-09-22 laufen, damit der 23.09. als Puffer für Nachzieharbeiten bleibt |
| **Status** | 🔴 **ENTSCHIEDEN am 2026-09-22** (D-269 bis D-275). **`E1` ist abgelehnt:** Die Umbenennung wird **nicht** vorgezogen, D-127 bleibt unverändert in Kraft. **`E2` bis `E9` sind angenommen**, `E4` und `E5` in einer vom Vorschlag abweichenden Fassung (`.koolie/core/` statt Vertagung und `koolie-core/`). 🟢 **Es ist kein Pfad angefaßt worden** – der Lauf selbst steht als Posten `~0.88.0` im Releaseplan, hinter dem Rest von `AP2` |

## 1. Anlass

Der Name steht seit D-125 fest, der Zeitpunkt seit D-127: **nach der letzten Messung,
vor `AP11`**. Der Framework Owner will die Umbenennung **vorziehen** – vor den Rest von
`AP2` –, damit sie einen Tag vor der Vorführung liegt und ein Puffertag bleibt.

**Das ist eine Abweichung von D-127 und wird als solche vorgelegt, nicht stillschweigend
umgesetzt.**

## 2. Trägt die Begründung von D-127 noch? – gezählt, nicht geschätzt

D-127 hat die Möglichkeit *„die Umbenennung vor die Messungen ziehen"* **ausdrücklich
erwogen und verworfen**, mit dieser Begründung:

> *„dann faßt sie jeden Pfad an, während **105 Ergebniszellen und 23 Marker** offen sind
> – der ursprüngliche Gegeneinwand, und dort trifft er zu"*

| Größe | Stand zu D-127 (`0.56.2`) | Stand heute (`0.85.0`) |
|---|---|---|
| offene Ergebniszellen (Kriterium 2) | **105** | **0** |
| offene `VERIFY`-Marker (Kriterium 1) | **23** | **22** |
| ausstehende **Meßsitzungen** | fünf Bündel + Nachläufe | **eine** (Rest von `AP2`) |

🔴 **Die tragende Hälfte der Begründung ist entfallen, die andere nicht.** Kriterium 2
steht auf null; die verbleibende Messung betrifft **eine** Fähigkeitsmatrix statt fünf
Bündel. **Aber sie steht aus**, und der Satz von D-127 *„An dieser Stelle ist nichts mehr zu
messen"* trifft damit heute nicht zu.

➡️ **Die Frage ist deshalb nicht „darf man", sondern „was kostet es".** Der Preis steht
in `E1`.

## 3. Der Umfang – gemessen am 2026-09-22

### 3.1 Im Repositorium

> **Alle Zahlen dieses Abschnitts sind gegen den Stand `0.85.0` gezaehlt** – also
> **vor** diesem Antrag. *Ein Antrag, der seinen eigenen Gegenstand vergroessert,
> waehrend er ihn misst, nennt den Stand, gegen den er gemessen hat.*

| Größe | Zahl |
|---|---|
| verfolgte Dateien gesamt | **494** |
| davon unter `leitwerk-core/` | **490** – sie wandern mit **einem** `git mv` |
| außerhalb | **4** (`README.md`, `UEBERGABE.md`, `.gitignore`, `UEBERGABE.local.md.example`) |
| textliche Fundstellen `leitwerk-core` | **1.976** in 326 Dateien |
| dazu `Leitwerk` / `leitwerk` / `LEITWERK` | 27 / 98 / 7 |
| Träger mit `<CORE_DIR>` | **43** |

### 3.2 🟢 Die Chronik und der Pfadprüfer vertragen sich – das war die erste Frage

D-125 sagt: *„Die Chronik wird nicht umgeschrieben"* – Protokolle, Änderungsanträge und
das Änderungsverzeichnis beschreiben einen vergangenen Zustand. **Damit stünde in ihnen
nach der Umbenennung ein Pfad, den es nicht mehr gibt** – und Prüfung 12 (`FW-KO-04`)
meldet tote Pfadangaben.

**Gemessen:**

| Prüfweg | Fundstellen in der Chronik | Folge |
|---|---|---|
| **Markdown-Links** (`[x](…)`) – **überall** geprüft, ohne Ausnahme | 🟢 **null** | keine Kollision |
| **Backtick-Pfade** – Ausnahmemenge `LINK_EXCEPTIONS` | **319** in 107 Dateien | 🟢 **ausgenommen** (`tests/protocols/`, `governance/change-requests/`, `CHANGELOG.md`, `DECISION_LOG.md`) |
| Backtick-Pfade in **lebenden** Trägern | **925** in 128 Dateien | **müssen wandern** |

> 🟢 **D-125 und Prüfung 12 stehen nicht gegeneinander.** Das Projekt nennt
> Framework-Pfade in Backticks und nicht als Markdown-Link – und genau die Backticks
> sind in der Chronik ausgenommen. **Die Arbeitsfläche des Textlaufs ist damit 925
> Fundstellen in 128 Dateien, nicht 1.976 in 326.**

### 3.3 🔴 Der Name steht auch im Werkzeug – und dort ist er Gegenstand von Sonden

| Werkzeug | Nennungen |
|---|---|
| `tests/scripts/probe-pruefungen.py` | **170** |
| `tests/scripts/validate-framework.py` | **54** |
| `install.py` | 15 |
| `tests/erhebungen/*.py` (16 Werkzeuge) | 59 |
| übrige (`clientmap.py`, `build/`, Hooks, `validate-output.py`) | 6 |
| **Summe über alle `.py` des Bestands** | **304** |

🔴 **Die 170 Nennungen in `probe-pruefungen.py` sind überwiegend Suchtexte von
Präparationen.** Eine Sonde, deren Suchtext nicht mehr trifft, **verliert ihren
Gegenstand** – und nach D-23 gilt die Prüfung dann als nicht vorhanden. *Der
Präparationswächter meldet es (`Praeparationsfehler`), aber erst im Lauf.*

➡️ **Der Sondenlauf in beiden Kodierungsumgebungen ist bei dieser Umbenennung kein
Formalakt, sondern der eigentliche Nachweis.**

### 3.4 🟢 Die übernehmenden Projekte – drei Schichten, und nur eine braucht Arbeit

| Schicht | `otp-generator` | `test-devin-framework` | wer sie umsetzt |
|---|---|---|---|
| **1** – `leitwerk-core/` im Zielprojekt | 1.357 | 1.848 | 🟢 **das Heben** (`rm -rf` + `git archive`) |
| **2** – Laufzeitschicht (`.claude/`, `.devin/`, Wurzeldatei) | 220 | 336 | 🟢 **`install.py --update`** – sie wird aus dem Kern **erzeugt** |
| **3** – **Projekteigenes** (Saat, Overlay, `tools/`, `README`) | **45** in **11 Dateien** | **88** in **16 Dateien** | 🔴 **niemand – das ist `K-50`** |

**Schicht 3 im einzelnen:**

| `otp-generator` | `test-devin-framework` |
|---|---|
| `project-overlay/OVERLAY.md` (21) | `project-overlay/OVERLAY.md` (50) |
| `project-overlay/change-requests/CR-OTP-G-001-…` (9) | `README.md` (8) |
| `…/branching-strategy/MR_TEMPLATE.md` (3) | `.github/pull_request_template.md` (4) |
| `README.md` (2), `overlay-manifest.yaml` (2) | `…/tech-packs/java-spring/TECH_PACK.md` (4) |
| `BRANCHING_STRATEGY.md` (2), `DEFINITION_OF_DONE.md` (2) | `…/definition-of-done/biv-dod.md` (3), `tools/praeparationen.py` (3) |
| `forbidden-terms.txt`, `documents/README.md`, `AI_GOVERNANCE.md`, `EXCEPTIONS.md` (je 1) | `tools/mentorenblatt/*` (je 3), `react-typescript/TECH_PACK.md` (2), `biv-deployment-hinweis.md` (2), fünf weitere (je 1) |

> 🟢 **Das ist der Befund, der `K-50` entscheidbar macht.** Der Klärungspunkt fragt seit
> dem 18.09., ob die Umbenennung einen **maschinellen** Migrationspfad braucht. **Die
> Fläche ist 27 Dateien über beide Projekte** – und `K-50` selbst nennt den Preis der
> Gegenseite: *„Ein maschineller Pfad ist Code, der genau einmal läuft und danach ewig
> gepflegt oder zurückgebaut werden will."*

## 4. Vorlage zur Entscheidung

> 🔴 **Jede Frage einzeln, mit Auflösung und Preis. Vor der Beantwortung wird kein Pfad
> angefaßt.**

| Nr. | Frage | Vorschlag und **Preis** |
|---|---|---|
| **E1** | **Wird die Umbenennung vor den Rest von `AP2` gezogen – abweichend von D-127?** | **Vorschlag: ja.** Die tragende Hälfte der Begründung von D-127 ist entfallen (105 → 0 Ergebniszellen). 🔴 **Preis, und er ist der einzige echte:** Der Vorbedingungsdurchgang der `AP2`-Sitzung muß **auf dem umbenannten Baum wiederholt** werden – Meßbaum, Apparat, Übungsrepositorium und Prompts tragen dann den neuen Namen. **Eine Sitzung, kein Kontingent.** **Preis des Gegenwegs:** `AP2` zuerst kostet **Modellzeit und mindestens eine Sitzung**, und die Umbenennung fiele hinter den Vorführungstermin |
| **E2** | **`K-50`: maschineller Migrationspfad oder Migrationshinweis?** | **Vorschlag: Migrationshinweis mit benannter Dateiliste.** Die Fläche ist **27 Dateien** (Schicht 3), und beide Projekte werden in derselben Sitzung von Hand gehoben. **Preis:** Ein drittes übernehmendes Projekt müßte die Liste selbst anwenden. **Preis des Gegenwegs (`K-50` nennt ihn selbst):** Code, der genau einmal läuft und danach gepflegt werden will |
| **E3** | **Soll der Validator einen Restbestand des alten Namens MELDEN?** | **Vorschlag: ja, als eigene Prüfung 75** – über den ganzen Kern, mit der Chronik als **deklarierter** Ausnahmemenge (dieselbe Bauform wie `P73_OFFEN`). 🔴 **Ohne sie ist „der Name ist weg" eine Behauptung ohne Prüfung** – und genau das ist der wiederkehrende Befundtyp dieses Projekts. **Preis:** eine Prüfung mehr, mit Sonden |
| **E4** | **`K-75` (1): `.koolie/` mit Punkt oder ohne?** | **Vorschlag: vertagen, und zwar ausdrücklich.** `K-75` ordnet die Frage dem Umzug in ein Unterverzeichnis zu (`1.3.0`), **nicht der Umbenennung**. 🔴 **Die Frist in `K-75` gilt der Entscheidung, nicht dem Umzug** – sie ist mit *„wir benennen um, ohne zu verschieben"* beantwortbar. **Preis:** `koolie-core/` liegt weiter in der Projektwurzel; der Umzug nach `.koolie/` bleibt ein eigener Vorgang |
| **E5** | **`K-75` (2): `core/` oder `koolie-core/` unter dem künftigen Unterverzeichnis?** | **Vorschlag: `koolie-core/`,** und damit hängt `E4` nicht mehr daran. Der Name sagt aus dem Zusammenhang gerissen, wem der Pfad gehört (Prüfung 48). **Preis:** Der Name doppelt sich, sobald `.koolie/koolie-core/` daraus wird – das ist der Einwand von `K-75`, und er ist mit `E4` vertagt |
| **E6** | **Wandert die Chronik mit?** | **Vorschlag: nein** (D-125, unverändert). Protokolle, Änderungsanträge, `CHANGELOG.md` und `DECISION_LOG.md` behalten `leitwerk-core/`. 🟢 **Gemessen verträglich** (Abschnitt 3.2). **Preis:** Wer eine alte Fundstelle nachschlägt, findet einen Pfad, den es nicht mehr gibt – *und das ist richtig so, er hat damals existiert* |
| **E7** | **Wandert `UEBERGABE.md` mit?** | **Vorschlag: ja.** Sie ist **kein** Chronikträger, sondern das Arbeitsdokument der laufenden Arbeit, und sie liegt seit `0.78.1` im Repositorium (D-216). **Preis:** Ihre Release-Abschnitte beschreiben vergangene Stände unter neuem Namen – zulässig, weil sie **fortgeschrieben** und nicht abgelegt wird |
| **E8** | **Wird das Repositorium bei Gitea umbenannt, und wann?** | **Vorschlag: nach dem Merge**, in derselben Sitzung. **Preis:** Die Remote-URL ändert sich; die lokale Beilage `UEBERGABE.local.md` und die Push-Befehlszeile sind nachzuziehen. 🔴 **Vorher zu klären:** ob Gitea eine Weiterleitung vom alten Namen anlegt |
| **E9** | **Was geschieht mit dem Foliensatz und den vier Vorführstationen?** | **Vorschlag: Folien nachziehen, Rückfall-Belege NICHT.** Die aufgezeichneten Belege von Bündel 3 sind Chronik (`E6`). 🔴 **Preis, und er trifft den Termin:** Die Live-Vorführung läuft auf dem umbenannten Baum, die Rückfall-Belege zeigen den alten Namen – **das gehört im Vortrag gesagt**, sonst sieht es aus wie ein Fehler |

## 5. Der Ablauf, wenn E1 bis E9 beantwortet sind

1. **Beide übernehmenden Projekte sichern** (Kopie neben dem Baum) – *vor dem ersten
   `git mv`, nicht danach.*
2. `git mv leitwerk-core koolie-core` – **490 Dateien in einem Schritt.**
3. **Textlauf über die lebenden Träger** (925 Fundstellen, 128 Dateien), **Chronik
   ausgenommen** nach `E6`. Zeilenendungserhaltend (`devpacks/leitwerk-ed.py`), CRLF
   zurückschreiben.
4. **Werkzeuge zuletzt** (`E3`): `validate-framework.py`, `probe-pruefungen.py`,
   `install.py`, `clientmap.py`, `tests/erhebungen/*.py`.
   🔴 **Die Lehre von `0.84.0` gilt hier doppelt:** *„Kern erst nach dem letzten Träger
   kopieren"* – und ein Werkzeug, das leise nichts tut, sieht aus wie ein Erfolg (D-262).
5. `<CORE_DIR>` in **43** Trägern, Platzhalterregister, `LINK_ROOTS_FEST`.
6. **Prüfung 75** bauen (`E3`), mit Sonde und Gegenprobe.
7. Validator, **dann** Sondenlauf in **beiden** Kodierungsumgebungen.
   🔴 **Hier fällt es auf, wenn ein Suchtext einer Präparation nicht mehr trifft.**
8. **Beide übernehmenden Projekte heben und migrieren** (`E2`), je mit
   `validate-framework.py --strict-overlay`.
9. Übergabe, CHANGELOG, `VERSION`, Protokoll – **dann** Branch, Commit, PR, Merge.
10. Repositorium bei Gitea umbenennen (`E8`), lokale Beilage nachziehen.

## 6. Entscheidung

🔴 **Am 2026-09-22 beantwortet, mit `0.85.2` aufgezeichnet: `E1` abgelehnt, `E2` bis `E9`
angenommen.** Die Vorlage ist am selben Tag mit `0.85.1` vorgelegt worden; **es ist auch
in dieser Sitzung kein Pfad angefaßt worden.**

| Nr. | Entscheidung | Abweichung vom Vorschlag | Record |
|---|---|---|---|
| **E1** | 🔴 **Abgelehnt.** Die Umbenennung wird **nicht** vor den Rest von `AP2` gezogen. **D-127 bleibt unverändert in Kraft** – nach der letzten Messung, vor `AP11` | **ja**, der Vorschlag lautete *vorziehen* | **D-269** |
| **E2** | **Migrationshinweis mit benannter Dateiliste** (`K-50` geschlossen) | nein | **D-270** |
| **E3** | **Prüfung 75 wird gebaut** – **im Umbenennungsrelease, nicht vorher** | nein (Zeitpunkt benannt) | **D-271** |
| **E4** + **E5** | 🔴 **`.koolie/core/`** – mit Punkt, und unter dem Unterverzeichnis heißt der Kern **`core/`**. `K-75` (1) und (2) sind damit **entschieden statt vertagt** | **ja**, der Vorschlag lautete *vertagen* und `koolie-core/` | **D-272** |
| **E6** | **Die Chronik wandert nicht mit** (D-125 bestätigt) | nein | **D-273** |
| **E7** | **`UEBERGABE.md` wandert mit** | nein | **D-273** |
| **E8** | **Gitea nach dem Merge** des Umbenennungsreleases. 🟢 **Der Vorbehalt ist gemessen, nicht angenommen** (Gitea 1.27.3, Testrepositorium): Gitea **legt** eine Weiterleitung an – **301**, `git ls-remote` läuft durch. 🔴 **Sie endet lautlos, sobald der alte Name neu belegt wird**, deshalb bleibt er unbelegt und die Remote-URL wird sofort nachgezogen | nein (Vorbehalt geklärt, **und die Annahme der Vorlage war falsch**) | **D-274** |
| **E9** | **Foliensatz und Vorführstationen bleiben unverändert** – die Vorführung am 24.09. läuft auf `leitwerk-core/`, und die bevorstehende Umbenennung wird im Vortrag **gesagt** | 🔴 **ja, weil `E1` sie gegenstandslos gemacht hat** – der Vorschlag setzte den umbenannten Baum voraus | **D-275** |

🔴 **Was die Ablehnung von `E1` kostet und was sie erspart.** Erspart wird der Preis, den
`E1` nennt: Der Vorbedingungsdurchgang der `AP2`-Sitzung bleibt auf dem Baum gültig, auf
dem er gefahren wird. **Bezahlt wird mit dem Termin:** Die Vorführung am 2026-09-24 läuft
unter dem alten Namen, und der Puffertag des 23.09. wird nicht gebraucht. *Der Satz von
D-127 „an dieser Stelle ist nichts mehr zu messen" trifft erst zu, wenn `AP2` zu Ende
ist – und genau darauf wartet der Lauf jetzt.*

🟢 **Die Messungen dieses Antrags bleiben gültig und sind der Vorrat des Umbenennungsreleases:**
490 von 494 Dateien wandern mit einem `git mv`, die Arbeitsfläche des Textlaufs ist **925
Fundstellen in 128 Dateien**, 43 Träger führen `<CORE_DIR>`, die Werkzeuge nennen den Namen
**304**mal.
⚠️ **Sie sind gegen `0.85.0` gezählt und altern mit jedem Release** – wer den Lauf fährt,
zählt sie nach, und der Ablauf in Abschnitt 5 gilt unverändert.

🔴 **Zwei Zahlen dieses Antrags sind bei der Entscheidung nachgezählt worden, und eine hat
nicht gehalten.**

| Zahl | im Antrag | nachgezählt am 2026-09-22 |
|---|---|---|
| Nennungen in den Werkzeugen | **304** | 🟢 **304** – mit dem Muster `leitwerk`; **311** über alle Schreibweisen, **295** allein für den Pfad `leitwerk-core`. *Ein Textlauf allein auf den Pfad ließe 16 Nennungen des bloßen Namens stehen.* |
| Migrationsfläche (Schicht 3) | **27 Dateien**, 133 Nennungen | 🔴 **30 Dateien, 141 Nennungen** – Pilot **50 in 13**, Übungsrepositorium **91 in 17**. **Es fehlten die `.gitignore` beider Projekte und ein Glossareintrag** – und `leitwerk-core/build/out/` im Übungsrepositorium ist ein **wirksames** Ausschlußmuster, das nach dem Umzug stumm aufhört zu greifen (D-97, Prüfung 45) |

➡️ **Der Migrationshinweis aus `E2` wird deshalb gegen den Bestand erzeugt und nicht aus
dieser Liste abgeschrieben.**
