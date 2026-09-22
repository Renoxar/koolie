# Änderungsantrag `CR-2026-102`

| Feld | Inhalt |
|---|---|
| Titel | `K-77` entschieden – der Zuschnitt folgt der Schranke, und der Wächter prüfte mit dem Schnittmuster |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-19 |
| Betroffene Artefakte | `governance/DECISION_LOG.md` (**D-205** neu, `K-77` erledigt, Belegzellen von D-203 und `K-77` berichtigt), `tests/TEST_CATALOG.md` (Punkt 4: die Zurechenbarkeitsangabe), `framework/skills/{fw-change-small,fw-refactor,fw-tests}/TESTS.md` (zwölf Ergebniszellen, **kein Versionsheben** – D-119), `tests/protocols/2026-09-19-k77-zurechenbarkeit.md` (neu), `docs/ROADMAP.md`, `CHANGELOG.md`, `VERSION`; **außerhalb des Repositoriums:** `devpacks/leitwerk-erhebungen-2026-09-19-b3/skripte/k-bauen-b3.py` (Stammwächter) und `k77-waechter-nachweis.py` (neu) |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand ist die Aussagekraft des Testkatalogs |
| Art | Entscheidung eines Klärungspunkts, **keine Messung, kein Kontingent, kein Modelllauf** |
| Dringlichkeit | **Regulär, mit einer Frist:** vor Bündel 4 (D-204, Posten `~0.75.0`) |

## 1. Anlass

`K-77` fragt seit `0.74.0`, wie ein Kontrolllauf für eine Zelle zu schneiden ist, deren
geprüfte Schranke in der `SKILL.md` steht. Der Punkt stellt zwei Wege zur Wahl:

1. ein Zuschnitt an der `SKILL.md` selbst, mit Wächter auf die Restfundstellen;
2. die ausdrückliche Feststellung, daß bei Skillzellen **keine** Zurechenbarkeit erhoben
   wird – spart je Zelle einen Lauf, **kostet D-175 seinen Gegenstand für die dreizehn
   Blätter**.

🔴 **Vor der Entscheidung ist der Beleg des Punktes nachgelesen worden – und er hält
nicht.** Das ist derselbe Griff wie bei D-170 und D-197.

## 2. Die Prämisse von D-203 hält nicht

D-203 stützt sich auf **eine** Messung (Bündel 3) und auf einen Satz über Bündel 2:
*„In Bündel 2 war jede Zelle mit `ohneskill` zurechenbar und keine mit einem
Regelschicht-Zuschnitt scharf."*

**Ausgezählt aus den Ergebnistabellen der drei Meßprotokolle** (Protokoll Abschnitt 2):

| Bündel | Zellen | 🟢 zurechenbar | davon `ohneskill` | davon **Regelschicht** |
|---|---|---|---|---|
| 1 | 11 | 6 | 4 | 2 |
| 2 | 18 | **17** | 5 | **12** |
| 3 | 18 | 4 | 3 | 1 |
| **Summe** | **47** | **27** | **12** | **15** |

🔴 **15 der 27 zurechenbaren Zellen sind über einen Regelschicht-Zuschnitt zurechenbar** –
mehr als über `ohneskill`. **Und `SK-004-N01` (Bündel 2, Zuschnitt `kn03`) ist
ausdrücklich *scharf*.** Beide Hälften des Satzes sind an einer einzelnen Zeile desselben
Protokolls widerlegt.

## 3. Der eigentliche Befund: der Wächter prüft mit dem Schnittmuster

`k-bauen-b3.py` schneidet nach den `ZEILE`-Mustern einer Klasse und prüft danach mit ihren
`MARKEN`. 🔴 **Die `MARKEN` sind in allen acht geprüften Klassen eine Teilmenge der
`ZEILE`-Muster.** Der Wächter sucht weniger, als der Schnitt entfernt – *die Null durch
Konstruktion* (0.59.1) am Wächter des Zuschnitts.

**Gemessen über acht Klassen** (Protokoll Abschnitt 4): Vier Zuschnitte lassen den
Gegenstand stehen (`sc1` 23, `plan` 17, `test` 15, `befund` 14 Zeilen), vier nicht (`k3`,
`inj`, `testnachweis`, `abw` – je **null**).

🟢 **Und damit fällt die Bilanz von Bündel 3 an der richtigen Linie auseinander:**

| Zuschnitt | Zellen | zurechenbar |
|---|---|---|
| **vollständig** (`k3`, `inj`, `testnachweis`, `abw`) | 5 | **1** (scharf) + 1 halb |
| **unvollständig** (`sc1`, `plan`, `test`, `befund`) | 9 | **0** |
| `ohneskill` | 3 | **3** |
| ⚠️ ungeprüft (`injk3`, kein Stammmuster) | 1 | 0 (1 halb) |
| **Summe** | **18** | **4** |

**Die einzige Regelschicht-Klasse, die getrennt hat, ist auch die einzige mit null
Restfundstellen.** ➡️ **Nicht *Regelschicht gegen Skill* ist die Trennlinie, sondern die
REICHWEITE des Zuschnitts.**

🔴 **Und die Schwäche war benannt:** Der Kopfkommentar desselben Skripts sagt seit der
Erhebung `s4`, ein grüner Wächter belege **nicht**, daß die Schranke weg sei. **Drei
Bündelprotokolle führen ihn trotzdem als Beleg.** Die Grenze war aufgeschrieben, und
niemand hat sie gegen ihre Verwendung gehalten.

## 4. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Welcher Weg?** | **Weder (1) noch (2) allein: der Zuschnitt folgt der SCHRANKE, nicht der Schicht** (D-205). Er erfaßt sie in allen Schichten – einschließlich `SKILL.md` – und in allen Formen; der Wächter prüft mit einem **weiteren** Muster als der Schnitt | **Kein Mehrpreis an Läufen** – 19 bleiben 19. Der Preis ist Aufbauzeit: je Klasse ein Stammmuster, und jede seiner Meldungen ist zu lesen. **Weg (1) ist darin enthalten**, weil die `SKILL.md` zu den Schichten gehört – und er ist am 19.09. versehentlich schon gefahren worden (`k3`) |
| **E2** | **Wird Weg (2) verworfen?** | **Ja** | Die Ersparnis von rund 21 USD je Bündel entfällt. 🔴 **Sie ist durch den eigenen Bestand widerlegt, 27 zu 0:** Hätte Weg (2) seit Bündel 1 gegolten, wäre **keine** der 27 zurechenbaren Zellen erhoben worden |
| **E3** | **Was wird aus den zwölf Zellen von Bündel 3, die `nicht zurechenbar` tragen?** | **Neun gehen auf `Zurechenbarkeit nicht erhoben`**, drei bleiben `nicht zurechenbar` – **und sind es zum ersten Mal belegt** | Zwölf Ergebniszellen in drei `TESTS.md`. **Kein Versionsheben** (D-119). **Der Gegenpreis wäre eine Behauptung:** Ein *nicht zurechenbar* sagt, das Framework wirke nicht – bei neun Zellen hat der Aufbau es schlicht nicht trennen können |
| **E4** | **Wird eine Prüfung gebaut?** | **Nein – erwogen und vertagt** | Zwei Prüfkandidaten bleiben offen: das **Vokabular der Zurechenbarkeitsangabe** (dieselbe Gattung wie D-101) und eine Prüfung, die eine **Aussage über ein Bündel gegen die Ergebnistabelle seines Protokolls** hält. 🔴 **Der zweite Befund ist in zwei Tagen zweimal aufgetreten** (`CR-2026-101` und dieser Antrag) – **beim dritten Mal wird er Prüfgegenstand.** Dagegen steht: Beide prüften Prosa, und eine Prüfung, die Prosa liest, arbeitet auf Teilsätzen (0.64.0) |
| **E5** | **Werden die neun Zellen mit unvollständigem Zuschnitt neu gefahren?** | **Nein – mit Bündel 4 zusammen, wenn überhaupt** | Neun Läufe, rund 10 USD, **bewegen keine Zahl von D-11**. Der Aufbau steht bei Bündel 4 ohnehin; ein eigener Meßtag dafür wäre der teuerste Weg zur selben Erkenntnis |
| **E6** | **Wird die falsche Aussage über Bündel 2 berichtigt?** | **Ja, in `K-77` und D-203** | Zwei Belegzellen. **Der Eintrag `0.74.0` im Änderungsverzeichnis bleibt unverändert** – er ist Aufzeichnung (D-141). **Zweiter Fall derselben Gattung in zwei Tagen**, und beide Male war der Zähler richtig und die Zuordnung falsch |

## 5. Entscheidung

**E1 bis E6 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-19). Decision Record
**D-205**; `K-77` ist damit erledigt. **`K-76` bleibt offen.**

## 6. Abnahme

- `validate-framework.py`: **0 Fehler, 0 Warnungen** gegen den fertigen Baum.
- `probe-pruefungen.py` in **beiden** Kodierungsumgebungen (D-49), voller Lauf.
- 🔴 **Der Wirkungsnachweis dieses Antrags liegt außerhalb des Validators**, weil der
  Gegenstand außerhalb liegt: **ein Paar am selben Baum.** Zuschnitt `plan` gegen
  `devpacks/test-devin-framework` – Wächter 1 (Marken) meldet **keine** Restfundstelle,
  Wächter 2 (Stamm) meldet **17** und bricht ab. Dazu die Gegenprobe: vier Klassen mit
  **null** Restfundstellen, darunter die einzige, die je getrennt hat.
- 🔴 **Prüfung 58:** `D-205` ist eine neue Kennung und braucht ihre Registerzeile.
- **Prüfung 65** bleibt grün: Kein Ergebnisstatus ändert sich, jede Zelle behält ihren
  Protokollverweis.

## 7. Migrationshinweis

**Drei Dateien** für das Übungsrepositorium, alle `TESTS.md` (`fw-change-small`,
`fw-refactor`, `fw-tests`); **der Pilot bekäme 38** (er steht auf `0.54.1`).
**Trockengelaufen gegen Kopien beider übernehmender Projekte** unter `C:\lw-mig`, mit dem
`leitwerk-core` des **Arbeitsbaums** – nicht gegen `git archive HEAD`, der den committeten
Stand nähme und 0.74.1 gegen 0.74.1 mäße. **Keine Versionsanhebung**, also auch hier nicht
*„Dateizahl mal zwei"* (D-119, dieselbe Lage wie bei `0.73.0`).

🔴 **Und der Durchgang vor dem Commit hat sich zum NEUNZEHNTEN Mal getragen – an zwei
eigenen Zahlen dieses Antrags:** Die Bilanztabelle deckte **17 der 18** Zellen von
Bündel 3 (`injk3` fiel heraus, weil für ihn kein Stammmuster vorliegt), und die
Vokabularzahlen im ersten Entwurf stammten aus einem groben `grep`. Sauber gezählt sind es
**acht Formeln in 42 Zellen**.
