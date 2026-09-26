# Änderungsantrag `CR-2026-152`

| Feld | Inhalt |
|---|---|
| Titel | Die Testblätter nach dem Modellwechsel – und die Überschriften, die auch als Bezeichnung umgeschrieben werden |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-26 |
| Betroffene Artefakte | `.koolie/core/framework/skills/fw-change-small/**`, `fw-refactor/**` (Anweisungen, Beispiele, Änderungsverläufe, Testblätter); `fw-plan/TESTS.md`, `fw-code-explain/TESTS.md` (Zellen); `.koolie/core/framework/core/05-working-model.md`; `.koolie/core/framework/core/08-skill-conventions.md`; `.koolie/core/framework/runtime/rules/00-framework-core.md`; `.koolie/core/onboarding/exercises/README.md` (`UEB-32`); `.koolie/core/tests/erhebungen/messbaum-schnitt.py` (neu), `k-bauen-b3.py`; `.koolie/core/tests/scripts/validate-framework.py`, `probe-pruefungen.py`; `.koolie/core/docs/ROADMAP.md`; `.koolie/core/build/doc/00-kopf.md`, `26-qs-test.md`, `29-grenzen.md`; Register, CHANGELOG, `VERSION`, Bestandsliste |
| Ebene laut Entscheidungsbaum 6 | Skills (Anweisung), Core-Modul und Laufzeitregel (Klarstellung), Prüf- und Messapparat |
| Art | **Änderung.** PATCH-Release nach D-424 – geänderte Anweisungen in zwei Skills, **ohne Overlay-Bruch** |
| Dringlichkeit | regulär – eingeplant mit D-424 |
| Status | 🟢 **entschieden am 2026-09-26** (E1 bis E10) |

---

## 1. Anlass

D-424 und `K-167`: Nach `1.14.0` trugen sechs Zellen mit Opus 5.5 nicht, keine wegen einer Änderung an ihrem
Skill. Dazu drei Befunde am Messapparat – der Kontrollzuschnitt `ohneskill` war durchlässig, Aufzeichnungen im
Messbaum verrieten Präparationen, und der Validator brach in der cp1252-Umgebung an einer eigenen Meldung ab
(`K-168`).

## 2. Die Vorprüfung

Ohne Kontingent: D-423 lässt „ein anderes Wort“ ausdrücklich als Befund stehen; beide Skills verboten jeden
Befehl außer Test und Lint, während der `allow`-Korb lesende Git-Befehle erlaubt; `fw-refactor` lehnt ab Stufe
mittel ohne Plan ab, und `SK-007-P01` erwartete mittel **und** Umsetzung; zwei Übungsaufgaben von `fw-plan`
trugen ihre Stufe nicht. Die Aufzeichnungen im Messbaum waren mehr als gezählt: das ganze Köderregister im
Onboarding und jedes Testblatt. Die Einzelheiten stehen im Protokoll
(`tests/protocols/2026-09-26-testblaetter-modellwechsel.md` Abschnitt 2).

## 3. Die Messung

51 Sitzungsläufe mit dem Client Pack `claude-code` 2.1.283 (Opus 5.5), 32,27 USD, einer davon verworfen.
**17 von 18 Zellen tragen.** Die Überschriften wurden auch als reine Bezeichnung umgeschrieben; nach der Formregel
D-432 standen sie in allen Nachmessungen wörtlich. 🔴 `SK-005-P01` bleibt offen: Der Commit-Vorschlag trägt die
Attributionszeile des Clients (`K-171`).

## 4. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | Umgeschriebene Pflichtüberschriften | 🟢 **Überschriften nur als Bezeichnung**, Bauform D-194 (D-426) | Beide Blätter offen, 14 Zellen |
| **E2** | Lesende Git-Befehle in M3 | 🟢 **Zulässig**, in Modul 05, Kurzfassung und beiden Skills (D-427) | Die Befehlsgrenze ist weiter |
| **E3** | Nicht gemeldete Injektion (`SK-005-N04`) | 🟢 **Pflichtabschnitt „Gemeldete Befunde“**, Meldung auch ohne Befolgen (D-428) | Ein Pflichtabschnitt mehr; `fw-change-small` `0.2.0` |
| **E4** | Die Zellen von `fw-plan` | 🟢 **Aufgaben und Aufrufe gepflegt**, Folgeturn für Abschnitt 10 (D-429) | – |
| **E5** | Einstufung ohne R3 (`SK-007-P01`) | 🟢 **Präparation `UEB-32`** (bestätigter Plan), Stufe im Aufruf (D-429) | Die Einstufung prüft keine Zelle mehr |
| **E6** | Der Validator unter cp1252 | 🟢 **Escape-Folge statt Abbruch**, Sonde 82d (D-430) | – |
| **E7** | `ohneskill` | 🟢 **Auch die Kernfassung**, Stammsatz-Wächter (D-425) | – |
| **E8** | Aufzeichnungen im Messbaum | 🟢 **Aufzeichnungsschnitt mit Wächter**, Transkript-Durchsicht, `SK-002-N02` nachgemessen (D-425) | Ein Messbaum ist kein vollständiges Abbild mehr |
| **E9** | Die letzte offene Zelle | 🟢 **`1.14.2` direkt danach** (D-431) | Kriterium 2 bleibt ein Release auf 1 |
| **E10** | Überschriften, die trotz E1 umgeschrieben werden | 🟢 **Formregel in Kurzfassung und Konvention, nicht im Skill** (D-432) | In zehn Skills nicht gemessen |

## 5. Umsetzung

1. `fw-change-small` `0.2.0` und `fw-refactor` `0.1.5`: Ausgabeformat, Befehlsgrenze, Abschnitt 7; Beispiele und Änderungsverläufe (*Anweisung berührt*).
2. `05-working-model.md` Abschnitt 2 und `00-framework-core.md` (lesende Git-Befehle, Formregel); `08-skill-conventions.md` Abschnitt 6 (Formregel).
3. `UEB-32` registriert; Quelle im Übungsrepositorium.
4. `messbaum-schnitt.py` neu (`aufzeichnungen`, `ohneskill`); `k-bauen-b3.py` schneidet in den Prompts.
5. Validator: `stdout`/`stderr` mit `backslashreplace`; Sonde 82d.
6. Nachlauf der 18 Zellen und des Kontrolllaufs `ksk004p01`; Zellen eingetragen.
7. Register, Roadmap, Hauptdokument, CHANGELOG, `VERSION`, Bestandsliste; Hebung beider Projekte und Bau der Erzeugnisse.

## 6. Entscheidung

🟢 **Angenommen am 2026-09-26.** E1 bis E8 wie vorgelegt (*„Passt und los“*); E9 und E10 sind während der Messung
nach den vorgelegten Empfehlungen entschieden – E10 innerhalb der geschätzten Kosten, E9 nach dem Vorbild von D-424.

| # | Entscheidung | Decision Record |
|---|---|---|
| E7, E8 | Messbaum-Schnitte | D-425 |
| E1 | Überschriften als Bezeichnung | D-426 |
| E2 | Lesende Git-Befehle | D-427 |
| E3 | Gemeldete Befunde | D-428 |
| E4, E5 | Zellpflege, `UEB-32` | D-429 |
| E6 | Berichtsweg des Validators | D-430 |
| E9 | Ergebnis und `1.14.2` | D-431 |
| E10 | Formregel | D-432 |
