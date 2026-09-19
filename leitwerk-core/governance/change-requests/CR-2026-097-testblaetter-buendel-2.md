# Änderungsantrag `CR-2026-097`

| Feld | Inhalt |
|---|---|
| Titel | Testblätter, Bündel 2 – die Überschrift, die eine Anweisung ist, und die Kennung, die keine Sitzung lädt |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-19 |
| Betroffene Artefakte | `framework/skills/fw-plan/{SKILL.md,EXAMPLES.md,CHANGELOG.md,TESTS.md}`, `framework/skills/fw-error-analyze/TESTS.md`, `framework/skills/fw-bugfix-prepare/{SKILL.md,CHANGELOG.md,TESTS.md}`, `clients/claude-code/CLIENT_PACK.md` (Zeile `S3`), `governance/DECISION_LOG.md` (**D-194** bis **D-196**, `K-74` neu, `K-73` beantwortet), `docs/ROADMAP.md` (Standzeile, Posten `0.71.0`), `tests/protocols/2026-09-19-testblaetter-buendel-2.md` (neu), `CHANGELOG.md`, `VERSION`; **außerhalb des Repositoriums:** das Übungsrepositorium (auf 0.70.0 gehoben), Belege unter `devpacks/leitwerk-erhebungen-2026-09-19-b2/` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind zwei Skills, eine Zeile der Fähigkeitsmatrix und achtzehn Ergebniszellen |
| Art | Messung nach Testkatalog, Befunde an Skills und Fähigkeitsmatrix |
| Dringlichkeit | **Regulär.** Der Posten stand im Releaseplan; die Vorbedingungen sind mit `0.70.0` hergerichtet |

## 1. Anlass

Der Releaseplan sah für dieses Release den **zweiten Bündellauf** vor (D-180): `fw-plan`
(`SK-004`), `fw-error-analyze` (`SK-008`) und `fw-bugfix-prepare` (`SK-009`),
**achtzehn Ergebniszellen**, Kriterium 2 von 74 auf 56. Die Vorbedingungen sind mit
`0.70.0` durchgegangen und hergerichtet worden (`CR-2026-096`, `UEB-17`, D-192, D-193).

Gefahren wurden **43 Läufe** unter `C:\lw-b2` in **vierzehn** Bäumen.

## 2. Der Meßaufbau – und eine Vorbedingung, die keine Routine war

| Schritt | Was er herstellt |
|---|---|
| **Das Übungsrepositorium auf Framework `0.70.0` heben** | 🔴 **Bei diesem Bündel keine Routine, sondern Vorbedingung** – siehe unten |
| `git archive HEAD` des Übungsrepositoriums | der **committete** Stand; für den Prüfling richtig |
| Packwechsel auf `claude-code` | `.devin/` und `AGENTS.md` weichen, dann `install.py --client claude-code` |
| `cc-overlay-fuellen.py` | der Füllschritt (0.65.0): sonst steht `Read(<EXCLUDED_PATHS>)` wörtlich im `deny`-Korb |
| Schreibkorb geöffnet | `Edit(**)` aus `ask`, `Edit(frontend/src/**)` in `allow` – ausgewiesene Abweichung (D-140) |
| Wächter **auf die Vorbedingungen** | Framework-Version, die Überschriften `### 3.3` bis `### 3.5`, `UEB-17` **ohne** Testdatei, `UEB-14`, `api-contracts/openapi.yaml`, `V1__init.sql`, die vier Rollenwerte |

🔴 **Das Heben war die Vorbedingung, nicht die Pflege.** `0.70.0` hat `02-privacy.md`
seine Unterabschnitte gegeben (D-193), und **drei der achtzehn Zellen erwarten eine
Bereinigung *nach Abschnitt 3.3***. Ein Meßbaum aus dem ungehobenen Stand hätte gegen
genau den Mangel gemessen, den das Vorrelease behoben hat. Dazu stellt `0.67.0` das
Prüfmittelwort der Testblätter von `manuell` auf `sitzung` – der ungehobene Baum trug
noch `manuell`.
➡️ **Wer einen Meßbaum aus einem übernehmenden Projekt baut, prüft zuerst, auf welchem
Releasestand dessen Kern steht** – und ob eines der Releases dazwischen den **Gegenstand
der Messung** angefaßt hat. Bündel 1 durfte die Frage verneinen (D-186, Protokoll
0.68.0 Abschnitt 1); Bündel 2 nicht.

🟢 **Und die Lehre aus D-186 hat sich getragen:** Das zweite Prüfmittel
`validate-output.py` ist **vor** dem ersten Lauf einmal im Meßbaum gefahren worden – für
alle drei Skills mit Gegenstand. Es ist seit 0.68.0 nicht mehr clientgebunden.

## 3. Befund 1: die Pflichtüberschrift, die eine Anweisung ist (D-194)

**Neun von neun** planerzeugenden Läufen verfehlen dieselbe Pflichtüberschrift:

```
### Plan (Struktur exakt nach leitwerk-core/templates/PLAN_TEMPLATE.md)
```

| Was die Läufe statt dessen schreiben | Anzahl |
|---|---|
| `### Plan (Struktur nach …)` – **genau ein Wort weggelassen** | 5 |
| die Überschrift ganz weggelassen, direkt `## Änderungsplan: …` | 2 |
| umformuliert (`### 5. Schritte der Umsetzung (Option A, klein und einzeln prüfbar)`) | 2 |

`validate-output.py` vergleicht Abschnittsnamen als **Teilzeichenfolge in beide
Richtungen** – die Prüfung ist also schon bewußt nachsichtig. **Ein Wort in der Mitte
überbrückt sie trotzdem nicht.**

🔴 **Die Richtung entscheidet der Vergleich, nicht der Ärger** (D-193): Eine Überschrift
ist eine **Bezeichnung**; `Struktur exakt nach <Vorlage>` ist eine **Anweisung**. Das
Ziel ist der Ausreißer, nicht die neun Läufe. Die Anweisung geht nicht verloren – sie
steht in beiden Skills unverändert in `description`, im Zweck und in Arbeitsschritt 10,
und geprüft wird sie weiter über die **zehn Abschnitte der Vorlage**, die einzeln in
derselben Pflichtliste stehen und von allen neun Läufen geliefert wurden.

🟢 **Die Abhilfe ist nachgemessen, nicht behauptet.** Die beiden Zellen, deren zweites
Prüfmittel den Befund gemeldet hat (`SK-004-P01`, `SK-009-P01`), sind gegen den
**berichtigten** Stand neu gefahren (Baum `b2n`). Die alten Antworten gegen das neue
Format zu halten wäre *der Befund, der an der eigenen Abhilfe altert* (D-164).

🔴 **Und die Bauform ist breiter als die eine Zeile:** **46 der 131**
Pflichtüberschriften aller zwölf Skills tragen einen Klammerzusatz. Die meisten sind
Etiketten, die ein Lauf mitkopiert (`Reproduktionshypothese (nicht ausgeführt)` – von
beiden `fw-error-analyze`-Läufen wörtlich geliefert); die, die eine **Vorschrift**
enthalten, werden umformuliert. Das ist `K-74`, und es gehört **vor Bündel 3**
entschieden: `fw-change-small` und `fw-refactor` tragen dieselbe Bauform.

## 4. Befund 2: die Sperre weist ab, sie entfernt nicht (D-195) – und der Zuschnitt, der nichts trennt

`K-73` verlangte *„eine eigene kleine Reihe … in drei Zuschnitten (Frontmatter mit und
ohne Sperre, Korb mit und ohne Freigabe)"*. Sie ist gefahren – **und sie hat die
Schichtfrage nicht entschieden.**

**Alle Bäume tragen dieselbe Berechtigungsdatei; `ls` steht in keinem ihrer Körbe.**

| Zuschnitt | Frontmatter | `Bash` im Korb | Ergebnis für ein schlichtes `ls` |
|---|---|---|---|
| `b2`, `ksc1` | aktiv (Skill über Schrägstrich) | nicht freigegeben | 🔴 **abgewiesen** – *„Permission to use Bash has been denied"* |
| `kohneskill` | **kein Skill** | nicht freigegeben | 🟢 **ausgeführt** |
| `kwerkzeugfrei` | Schlüssel entfernt | nicht freigegeben | **kein Aufruf abgesetzt** |
| `kbash` / `kbashfrei` | mit / ohne | **freigegeben** | 🔴 **kein Aufruf abgesetzt – das Paar trennt nichts** |

🔴 **Das Modell hat den Aufruf abgesetzt** – das Werkzeug war also **im Vorrat**. Die
Zeile `S3` sagt seit 0.35.0, die Sperre **entferne das Werkzeug aus dem Vorrat**;
gemessen ist eine **Abweisung**. **An der Wirkung ändert das nichts, an der Beschreibung
alles:** Wer der alten Formulierung glaubt, hält einen abgewiesenen Aufruf für einen
Widerspruch – und genau deshalb stand `K-73` zwei Releases offen.

🔴 **Das eigens gebaute Paar hat nichts beigetragen, und das gehört hierhin:**
`k73bash` und `k73bashfrei` haben mit **demselben Prompt**, der in `b2` spontan zwei
Aufrufe erzeugt hatte, **gar keinen Bash-Aufruf abgesetzt** – zum zweiten Mal nach
`ksk002n02b` in Bündel 1. Die Schichtfrage ist damit **wahrscheinlich, nicht isoliert**;
`K-73` wird deshalb **nicht geschlossen**, sondern beantwortet, soweit er sich
beantworten ließ (dieselbe Zurückhaltung wie bei `K-71`).
➡️ **Ein Zuschnitt, der auf einen SPONTANEN Aufruf wartet, ist kein Zuschnitt.**

⚠️ **Die Abweisung trägt kein `toolDenialKind`.** Sie steht in `permission_denials` des
Ergebnis-JSON und im Text des Werkzeugergebnisses. Wer nur die Mitschrift nach
`toolDenialKind` durchsucht, zählt **null**.

## 5. Befund 3: die Kennung, die keine Sitzung lädt (D-196)

Drei Zellenarten verlangen eine **Kennung**, und keine davon steht in der Schicht, die
jede Sitzung lädt.

| Kennung | Wo sie steht | Wo sie nicht steht | Gemessen |
|---|---|---|---|
| Risikofaktor `R1`–`R13` | `framework/core/09-risk-model.md` | **alle vier Regeldateien** – sie nennen zusammen **einen** Faktor (`R4`), beiläufig | `sk009p02` hat die Quelle per Grep geöffnet und **alle dreizehn** genannt; `sk004n04` hat sie **nicht** geöffnet und nur `R1` genannt |
| `02-privacy.md` Abschnitt 3.3 | seit D-193 als Überschrift im Kernmodul | **keine der vier Regeldateien trägt nummerierte Abschnitte** | einer von drei Läufen nennt die Nummer, zwei zitieren die geladene Schicht ohne sie |
| Rolle (`<APPROVAL_ROLE>` …) | im Overlay als **Wert**, nicht als Platzhalter (`K-69`) | – | die Läufe nennen *„Technische Projektleitung"*, *„Product Owner"* – wie in 0.21 festgelegt |

🔴 **`sk004n04` hat die Sache richtig gemeldet und die Nummer nicht.** Es zitiert genau
die Zeile der geladenen Kurzfassung, die den Inhalt von `R11` **ohne** die Nummer trägt:
*„Datenmodellen mit Migration … ist mindestens hoch beziehungsweise nicht delegierbar"*.
Das ist der wiederkehrende Befundtyp *„eine Suche nach einer Marke findet nicht, was
dieselbe Bedeutung ohne sie ausdrückt"* – hier auf der Seite des **Laufs**.

➡️ **Festlegung:** Eine Zelle, die eine Kennung verlangt, ist erfüllt, wenn der Lauf die
**Sache** nennt, solange die geladene Schicht die Kennung nicht führt. Die Zurechnung
steht im Protokoll, die Zelle wird nicht geändert.

## 6. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Wird die Pflichtüberschrift berichtigt oder werden die beiden Zellen als `offen` geführt?** | **Berichtigt, und die beiden Zellen werden gegen den berichtigten Stand NEU gefahren** (D-194) | Zwei Skills steigen auf `0.1.4`, drei Träger geändert, **drei zusätzliche Läufe**. **Der Gegenpreis ist größer:** Zwei Zellen blieben an einer Überschrift hängen, die neun von neun Läufen nicht reproduzieren – und Bündel 3 liefe in dieselbe Zeile |
| **E2** | **Wird `K-73` mit diesen Läufen geschlossen?** | **Nein – beantwortet, soweit er sich beantworten ließ** (D-195). `S3` sagt künftig *weist ab* statt *entfernt*; die **Schichtfrage** bleibt offen | Eine Zeile der Fähigkeitsmatrix wird länger, ein Klärungspunkt bleibt stehen. **Der Gegenpreis wäre größer:** Das eigens gebaute Paar hat keinen Aufruf abgesetzt, und aus einem beiläufigen Vergleich eine Isolation zu machen wäre die Null durch Konstruktion (0.59.1). **Die Einstufung `[TECHNISCH]` bleibt** – die Sperre wirkt |
| **E3** | **Wie werden Zellen bewertet, die eine Kennung verlangen, die keine Sitzung lädt?** | **Erfüllt, wenn der Lauf die Sache nennt** (D-196) | Eine Festlegung mehr, die man lesen muß. **Verworfen: die Kennungen in die Kurzfassung übernehmen** – sie ist eine Kurzfassung, und was beim Kürzen passiert, hat 0.61.0 gezeigt |
| **E4** | **Bleibt der Schreibkorb offen, obwohl D-188 ihn für wirkungslos erklärt hat?** | **Ja, unverändert** | Kostet nichts und macht die Abweichung sichtbar. **Bestätigt:** Kein Lauf dieses Bündels hat geschrieben; `zustand-b2.py` belegt es vorher und nachher |
| **E5** | **Werden die Ausgabemarken `[HALT]`/`[RÜCKFRAGE]` in diesem Release geklärt?** | **Nein – `K-74`** | Ein offener Punkt mehr. **Der Grund:** 145 Fundstellen in 54 anweisenden Trägern sind kein Nebenbei, und die Entscheidung gehört vor Bündel 3, nicht in einen Meßtag |

## 7. Entscheidung

**E1 bis E5 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-19). Decision
Records **D-194**, **D-195**, **D-196**; `K-73` beantwortet, soweit er sich beantworten
ließ; `K-74` neu.

## 8. Abnahme

- `validate-framework.py`: **0 Fehler, 0 Warnungen** gegen den fertigen Baum.
- `probe-pruefungen.py` in **beiden** Kodierungsumgebungen (D-49), voller Lauf.
- **Prüfung 46** rechnet Kriterium 2 nach und hält es gegen die Standzeile.
- **Prüfung 62** ist der zweite Wirkungsnachweis: Beide Skills steigen auf `0.1.4`, ihre
  Ausgabevorlage leitet die Version aus dem Steckbrief ab.
- Trockenlauf vor dem Migrationshinweis, mit dem `leitwerk-core` des **Arbeitsbaums**.
