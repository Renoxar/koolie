# Änderungsantrag `CR-2026-103`

| Feld | Inhalt |
|---|---|
| Titel | Die Vorbedingungen von Bündel 4 – der Meßbaum hat keine Historie |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-19 |
| Betroffene Artefakte | `governance/DECISION_LOG.md` (**D-206**, **D-207** neu, `K-78` neu), `framework/skills/{fw-mr-description,fw-review-support}/TESTS.md` (dreizehn Vorbedingungszellen, **kein Versionsheben** – D-119), `tests/protocols/2026-09-19-vorbedingungen-buendel-4.md` (neu), `docs/ROADMAP.md` (neuer Posten `~0.77.0`, Bündel 4 auf `~0.78.0`), `CHANGELOG.md`, `VERSION` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind Testblattzellen und der Meßaufbau |
| Art | Durchgang vor dem Meßtag, **keine Messung, kein Kontingent** |
| Dringlichkeit | **Regulär, mit einer Frist:** vor Bündel 4 |

## 1. Anlass

Der Wiederaufnahmepunkt von `0.74.0` verlangt vor Bündel 4 zwei Dinge: den
Vorbedingungsdurchgang – *„sechzehnmal in Folge der billigste Befund"* – und die Frage, ob
ein Release seit `0.73.0` den Gegenstand der Messung angefaßt hat.

🟢 **Die zweite Frage ist beantwortet: nein.** `git log 0373f1f..HEAD` über die drei
Skillverzeichnisse ist leer; die Skillversionen stehen unverändert.

🔴 **Die erste hat dreizehn von neunzehn Zellen getroffen** – und der teuerste Befund liegt
am **Meßapparat**.

## 2. Der Befund: ein Meßbaum aus `git archive` hat keine Historie

**Zwölf der neunzehn Zellen** rufen ihren Skill mit `<DEFAULT_BRANCH>` auf und verlangen
einen Diff gegen einen Branch. `umgebungen-bauen-b3.py` baut den Meßbaum mit
`git archive HEAD | tar -x` – **kein `.git`, kein Branch, kein Diff.**

**Für Bündel 1 bis 3 war das richtig** (D-141); für Bündel 4 ist die Historie der
Gegenstand. 🟢 **Die Vorlage liegt vor:** `k3-bauen.py` legt seit dem 17.09. ein echtes
Git-Repositorium an.

**Dazu drei weitere Befundgruppen** (Protokoll Abschnitte 4 bis 6):

- **Präparationen in der Historie** – zwei Commit-Betreffs mit Anweisung, dazu
  Autorenangaben. **Neue Gattung:** Alle zwanzig registrierten Präparationen sind
  Dateizustände mit einem Pfad.
- 🔴 **Echte Personendaten im Meßaufbau:** 33 Commits eines Autors mit echtem Namen und
  echter E-Mail – in einem Baum, dessen Zelle prüft, ob der Lauf Personen verschweigt.
- **Artefakte eines Laufs** (Ergebnisberichte, Plan, Bericht mit falscher Fundstelle) –
  **sechste und siebte Wiederholung** der Bauform aus D-192. Und `UEB-18` trägt nicht: Er
  ist der Plan **ohne** die zweite Datei, gebaut für den Abweichungsfall.

## 3. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Bekommt der Meßbaum von Bündel 4 ein echtes Git-Repositorium?** | **Ja** (D-206) – `git init`, `main`, zwei Übungs-Branches, präparierte Commits; `k3-bauen.py` ist die Vorlage | Der Baumbau wird teurer und bekommt einen eigenen Wächter. **Der Gegenpreis ist zwölf unfahrbare Zellen.** ⚠️ **Und der Baum trägt damit eine Aufzeichnung, die D-141 sonst heraushält** – die Grenze gilt für **Regeltexte**, nicht für den Gegenstand der Messung |
| **E2** | **Werden Historienzustände als Präparation registriert?** | **Ja** (D-207) – mit der Commitkennung statt eines Pfades | Das Register bekommt eine zweite Gattung und eine Spalte, die nicht jede Zeile füllt. **Der Gegenpreis:** Ein Zustand, den niemand registriert, ist beim nächsten Baumbau verschwunden – und Prüfung 44 könnte ihn nie zählen |
| **E3** | **Bekommt die Historie synthetische Autoren?** | **Ja** | Der Baumbau schreibt `GIT_AUTHOR_NAME`/`GIT_AUTHOR_EMAIL` um. 🔴 **Der Gegenpreis ist ein Meßaufbau, der echte Personendaten ausliefert, um deren Verschweigen zu prüfen** – dieselbe Bauform wie D-179 |
| **E4** | **Wird in diesem Release hergerichtet?** | **Nein – der Durchgang wird festgehalten, die Herrichtung ist ein eigener Posten** | Ein Release mehr. **Präzedenz und Grund:** `0.63.0` (Durchgang) und `0.64.0` (Herrichtung) waren getrennt, und die Herrichtung hat damals **vier** Zellen gefunden, die schon trugen – wer beides in einem Zug tut, prüft seine eigene Arbeit im selben Atemzug |
| **E5** | **Wie entstehen die Ergebnisberichte?** | **`K-78`** – nicht hier entschieden | Ein Klärungspunkt mehr. **Der Grund ist die Falle von `UEB-07`:** Ein synthetischer Bericht muß den Fall herstellen, **ohne die Antwort mitzuliefern**, und bei `SK-010-P02` muß er sogar eine **falsche** Fundstelle tragen, die der Lauf finden soll. Das ist Ermessen und gehört in den Antrag, der die Arbeit auslöst |
| **E6** | **Werden die dreizehn Zellen vermerkt?** | **Ja, in ihrer Vorbedingungszelle** | Dreizehn Zellen in zwei `TESTS.md`, **kein Versionsheben** (D-119). **Der Gegenpreis wäre eine Zelle, die `offen` sagt und damit behauptet, fahrbar zu sein** (`K-66`, D-162) |

## 4. Entscheidung

**E1 bis E6 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-19). Decision Records
**D-206** und **D-207**; **`K-78`** neu. Kriterium 2 unverändert **38**.

## 5. Abnahme

- `validate-framework.py`: **0 Fehler, 0 Warnungen** gegen den fertigen Baum.
- `probe-pruefungen.py` in **beiden** Kodierungsumgebungen (D-49), voller Lauf.
- **Prüfung 58:** `D-206`, `D-207` und `K-78` sind neue Kennungen und brauchen ihre
  Registerzeilen.
- **Prüfung 44** bleibt grün: Die Vermerke nennen keine Präparationskennung, die es nicht
  gibt; `UEB-14`, `UEB-09`, `UEB-10` und `UEB-02` bleiben unverändert genannt.
- **Prüfung 46** bleibt bei **38**: Kein Ergebnisstatus ändert sich.

## 6. Migrationshinweis

**Zwei Dateien** (`fw-mr-description/TESTS.md`, `fw-review-support/TESTS.md`) für das
Übungsrepositorium; **der Pilot bekäme 38** (er steht auf `0.54.1`). Keine
Versionsanhebung (D-119).
