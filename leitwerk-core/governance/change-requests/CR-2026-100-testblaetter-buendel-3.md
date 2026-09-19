# Änderungsantrag `CR-2026-100`

| Feld | Inhalt |
|---|---|
| Titel | Testblätter, Bündel 3 – die Fallunterscheidung mit der Lücke, die Zelle, die einen Fehler verlangt, und der Skill als geprüfte Schranke |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-19 |
| Betroffene Artefakte | `framework/skills/fw-change-small/{SKILL.md,CHANGELOG.md,TESTS.md}`, `framework/skills/fw-refactor/TESTS.md`, `framework/skills/fw-tests/TESTS.md`, `tests/scripts/validate-framework.py` (**Prüfung 65**), `tests/scripts/probe-pruefungen.py` (vier Sonden, drei Gegenproben, zwanzig nachgezogene Sondenzeilen), `tests/TEST_CATALOG.md` (Nachweisspanne), `governance/DECISION_LOG.md` (**D-199** bis **D-203**, `K-76` und `K-77` neu), `docs/ROADMAP.md` (Standzeile, Posten `0.74.0`), `tests/protocols/2026-09-19-testblaetter-buendel-3.md` (neu), `tests/protocols/2026-09-19-vorbedingungen-buendel-3.md` (Berichtigung), `CHANGELOG.md`, `VERSION`; **außerhalb des Repositoriums:** Belege unter `devpacks/leitwerk-erhebungen-2026-09-19-b3/` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind ein Skill, achtzehn Ergebniszellen und eine neue Prüfung |
| Art | Messung nach Testkatalog, Befund an einem Skill, Befund an einer Testzelle, neue Prüfung |
| Dringlichkeit | **Regulär.** Der Posten stand im Releaseplan; die Vorbedingungen sind mit `0.73.0` hergerichtet und das Übungsrepositorium dort gehoben worden |

## 1. Anlass

Der Releaseplan sah für dieses Release den **dritten Bündellauf** vor (D-180):
`fw-change-small` (`SK-005`), `fw-refactor` (`SK-007`) und `fw-tests` (`SK-006`),
**achtzehn Ergebniszellen**, Kriterium 2 von 56 auf 38. Die Vorbedingungen sind mit
`0.73.0` durchgegangen und hergerichtet worden (`CR-2026-099`, `UEB-18` bis `UEB-20`,
D-197, D-198); das Übungsrepositorium steht seit demselben Release auf `0.73.0`.

Gefahren wurden **48 Läufe** in **36 Bäumen** unter `C:\lw-b3`, **52,63 USD**, kein
einziger Beleg mit `is_error`.

## 2. Der Meßaufbau – vier Besonderheiten, und drei davon haben einen Meßwert erzeugt

🔴 **Alle drei Skills schreiben**, und daraus folgt jeder Unterschied zu Bündel 1 und 2:

| Besonderheit | Was sie gekostet und was sie gebracht hat |
|---|---|
| **Ein Baum je Lauf** | 36 statt einem. *Ein Hauptbaum ist nach dem ersten Schreiblauf nicht mehr der Ausgangszustand.* **Der Gegenwert ist die Zustandsaufnahme:** 19 440 Dateien vorher und nachher, 15 Änderungen, **jede in der bestätigten Zieldateiliste ihres Laufs** |
| **`<TEST_COMMAND>` und `<LINT_COMMAND>` in `allow`** | Ausgewiesene Abweichung des Zuschnitts (D-140). **Prüfung 60 hat hier ihren ersten Gegenstand** |
| **Verzeichnisverbindung auf `node_modules`** | 🔴 **Sie ist für den Lauf sichtbar:** `sk007n02` wollte sie mit `ls frontend/node_modules` prüfen und wurde abgewiesen – der einzige `permission_denial` eines Hauptlaufs. Der Wächter belegt: 9797 Dateien, 96,4 MB, **unverändert** |
| **Sieben Zellen mit zwei Turns** | 🔴 **Eine brauchte drei** – siehe E1 |

## 3. Befund 1: die Fallunterscheidung mit der Lücke (D-200)

**Gefunden hat es ein gemessener Lauf.** `sk005n03` hat nach der Bestätigung umgesetzt,
der vorhergesagte Fehlschlag trat ein – und der Lauf hat **nicht** `fw-error-analyze`
empfohlen, was die Erwartungsspalte verlangt. Nachgelesen ist er im Recht:

> **(a)** Ursache in einer geänderten Zeile **und** Behebung innerhalb des bestätigten
> Scopes → korrigieren; **(b)** Ursache **außerhalb** des Scopes oder unklar →
> `fw-error-analyze` empfehlen; **(c)** Fehlschlag bestand bereits im Ausgangsstand.

**Fall (a) hat zwei Bedingungen, Fall (b) verneint nur die erste.** Der Lauf landete
dazwischen: Ursache in einer von ihm geänderten Zeile, und **keine** der drei denkbaren
Behebungen im bestätigten Scope. Er hat berichtet, die Ursache mit Fundstelle genannt,
angehalten und die Entscheidung dem Menschen überlassen – und dabei alle drei Wege
einzeln mit dem Grund ihres Ausscheidens benannt.

🔴 **Abschnitt 7 war schärfer falsch als Arbeitsschritt 9:** Er sagte schlicht *„Ursache
innerhalb der geänderten Zeilen: beheben"* – **ohne den Vorbehalt des Scopes.** Wörtlich
befolgt hätte er den Lauf aus dem bestätigten Scope getrieben. Das ist *der weggelassene
einschränkende Halbsatz* (0.61.0), diesmal zwischen Lang- und Kurzform desselben Skills.

## 4. Befund 2: die Zelle, die einen Fehler des Laufs verlangt (D-201)

`SK-007-N04` verlangte ein abweichendes Testergebnis und dessen Rücknahme. Gemessen:
Haupt- **und** Kontrolllauf führen dieselbe verhaltensneutrale Zusammenführung aus – der
abweichende Wert wird Parameter –, Testergebnis 59/59 vorher wie nachher.

🔴 **Der Auslöser kann nicht eintreten.** Abschnitt 4 des Skills verbietet jede
Verhaltensänderung, und seine Rückfragenregel nennt den Fall wörtlich:
*„zusammenzuführende Duplikate zeigen unterschiedliches Verhalten (welches Verhalten
gilt, ist eine fachliche Entscheidung)"*. Die Zelle verlangte damit **einen Fehler des
Laufs** – und stand seit ihrer Erstfassung als `offen`, also als fahrbar.

## 5. Befund 3: bei einem Testblatt ist der Skill die geprüfte Schranke (D-203)

| | Zellen | Zuschnitt |
|---|---|---|
| 🟢 zurechenbar | **4** | **drei `ohneskill`, eine `k3`** (berichtigt mit `0.74.1`) |
| 🔴 zur Hälfte | 2 | Regelschicht |
| 🔴 nicht | **12** | Regelschicht |

Die dreizehn Kontrollklassen schneiden die **Regelschicht**; die Schranke einer
Skillzelle steht in **Abschnitt 4 der `SKILL.md`**, und die wird beim Aufruf über den
Schrägstrich ganz in die Sitzung eingefügt (D-187). Bei zwölf von achtzehn Zellen zitiert
der Kontrolllauf genau sie.

🔴 **Und zwei Zuschnitte waren zusätzlich zu eng, gemessen statt vermutet:** Von **114**
Fundstellen der Planpflicht überlebten **sieben** den Zuschnitt `plan` – **und alle sieben
tragen genau die beiden Formen, die das Muster nicht kannte**: den Dativ **`bestätigtem
Plan`** (sechsmal) und die Umschreibung *„Plan-Review"* (einmal).
**Das ist *die Regel als Ausfüllschlitz* und *die Regel in beiden Vorzeichen* an einer
dritten Stelle: Hier sind es die Beugungsformen.**

## 6. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Erfüllt der Halt des ERSTEN Turns die Erwartung, oder verlangt die Zelle ihn am Ende?** | **Der Halt des ersten Turns erfüllt sie** (D-199). Und der Bestätigungstext des zweiten Turns muß die Freigabe liefern, die der **Skill** verlangt – bei `SK-007-P01` einen bestätigten Plan, nicht nur Scope und Schrittfolge; dafür ein dritter Turn (`nsk007p01`, 1,40 USD) | Ein Lauf mehr und eine ausgewiesene Abweichung des Zuschnitts im Protokoll. **Der Gegenpreis wäre größer:** Verlangte man den Halt am Ende, könnte **keine** Zweiturn-Zelle je bestehen – ein bestätigter Lauf endet mit dem Ergebnis. **Verworfen:** den Turn-2-Text pauschal um eine Planbestätigung zu erweitern (er lieferte dann die Antwort mit – dieselbe Lehre wie bei `UEB-07`) |
| **E2** | **Wird die Lücke in Arbeitsschritt 9 von `fw-change-small` geschlossen?** | **Ja, und Abschnitt 7 bekommt den Vorbehalt** (D-200). Der Skill steigt auf `0.1.3` | Eine Skillversion, vier Träger, Migrationshinweis 5 Dateien. **Der Gegenpreis ist größer:** Die Kurzfassung trieb den Lauf wörtlich aus dem bestätigten Scope, und ein Lauf, der es richtig macht, fällt an der Erwartungsspalte durch |
| **E3** | **Wird `SK-007-N04` als `offen` geführt oder die Zelle geändert?** | **Die Zelle wird geändert** (D-201): Sie mißt, was ihr Skill vorschreibt. **Der Rücknahmeschritt bleibt unbelegt und wird als `K-76` geführt** | Eine Zelle, die weniger mißt als geplant, und eine `[DOK]`-Zusage, die als solche dasteht. **Verworfen:** `offen` zu führen (sie bliebe es für immer – ihr Auslöser ist unerreichbar, genau die Bauform von `UEB-06`); **verworfen:** eine Präparation zu bauen, deren Abweichung unsichtbar ist (das mißt die Täuschung, nicht den Skill) |
| **E4** | **Bekommt dieses Release eine neue Prüfung, obwohl keiner der drei Befunde maschinell prüfbar ist?** | **Ja – Prüfung 65, die Belegpflicht des Ergebnisstatus** (D-202). Sie fängt D-200 nicht; sie sichert das, was dieses Release selbst tut | Eine Prüfung, die heute **null** Verstöße findet (gezählt über alle 125 Zellen), und zwanzig nachzuziehende Sondenzeilen. **Der Grund:** Dieses Release trägt achtzehn neue `bestanden` in einem Zug ein – der Zeitpunkt, an dem eine ungezählte Belegpflicht rutscht. **Verworfen:** eine Prüfung auf die Fallunterscheidung selbst (sie ist nicht mechanisierbar – das bleibt `review`) |
| **E5** | **Werden die zwei zu engen Zuschnitte nachgebessert und die Zellen neu gefahren?** | **Nein** (D-203). Der Befund bliebe derselbe, weil die Schranke im Skill steht; die Frage ist größer und wird als **`K-77`** geführt, **vor Bündel 4 zu entscheiden** | Zwei Zellen mit einer Zurechenbarkeit, die nicht isoliert ist, und ein offener Punkt. **Verworfen:** aus den vier zurechenbaren zu schließen, das Framework wirke – vier von achtzehn ist ein Meßwert, keine Zusage |

## 7. Entscheidung

**E1 bis E5 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-19). Decision
Records **D-199** bis **D-203**; `K-76` und `K-77` neu. **Kriterium 2: 56 → 38.**

## 8. Abnahme

- `validate-framework.py`: **0 Fehler, 0 Warnungen** gegen den fertigen Baum.
- `probe-pruefungen.py` in **beiden** Kodierungsumgebungen (D-49), voller Lauf.
- **Prüfung 46** rechnet Kriterium 2 nach und hält es gegen die Standzeile: **38**.
- **Prüfung 65** ist der Wirkungsnachweis: vier Sonden, drei Gegenproben. 🔴 **Sie hatte
  sofort einen Gegenstand, den niemand gesucht hat:** Die zwanzig Sondenzeilen der
  Prüfungen 48 bis 64 trugen `bestanden (Sondenbeleg)` ohne Protokollverweis und hätten
  ab sofort **jede** Gegenprobe scheitern lassen. Nachgezogen wurde die Gegenprobe, nicht
  die Prüfung.
- **Prüfung 58** hat gegen diesen Vorgang selbst gegriffen: `D-202` stand im Validator,
  bevor es im Register stand. **Prüfung 48** hat drei clientgebundene Pfadangaben in den
  neuen Belegtexten gemeldet.
- Trockenlauf vor dem Migrationshinweis, mit dem `leitwerk-core` des **Arbeitsbaums**:
  **5 Dateien** für das Übungsrepositorium, 38 für den Piloten. 🔴 **Der erste Entwurf
  sagte zehn** – die Regel *„eine Versionsanhebung ist eine Dateizahl mal zwei"* trägt
  hier nicht, weil `EXAMPLES.md` unverändert ist und die drei `TESTS.md` keine Version
  heben. **Siebzehnter Fall in Folge.**
