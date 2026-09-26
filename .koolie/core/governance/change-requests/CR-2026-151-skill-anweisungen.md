# Änderungsantrag `CR-2026-151`

| Feld | Inhalt |
|---|---|
| Titel | Die Anweisungen der Skills gegen ihre Module – und das Modell, das die Überschriften umschreibt |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-26 |
| Betroffene Artefakte | `.koolie/core/framework/skills/fw-change-small/**`, `fw-refactor/**`, `fw-plan/**`, `fw-code-explain/**` (Anweisungen, Änderungsverläufe, Testblätter); `.koolie/core/framework/core/02-privacy.md`; `.koolie/core/framework/core/08-skill-conventions.md`; `.koolie/core/prompts/02-impact-analysis.md` bis `05-test-generation.md`; `.koolie/core/docs/PLACEHOLDER_REGISTRY.md`; `.koolie/core/docs/RUNTIME_GLOSSARY.md`; `.koolie/core/tests/scripts/validate-framework.py` (Prüfung 20); `.koolie/core/tests/scripts/validate-output.py`; `.koolie/core/tests/scripts/probe-pruefungen.py`; `.koolie/core/tests/erhebungen/k-bauen-b3.py` (Klasse `bew`); `.koolie/core/docs/ROADMAP.md`; `.koolie/core/build/doc/00-kopf.md`, `01-executive-summary.md`, `26-qs-test.md`, `29-grenzen.md`; Register, CHANGELOG, `VERSION`, Bestandsliste |
| Ebene laut Entscheidungsbaum 6 | Skills (Anweisung), Core-Modul (Klarstellung), Prüfapparat |
| Art | **Änderung.** MINOR-Release nach `RELEASE_PROCESS.md` Abschnitt 1 – geänderte Anweisungen in vier Skills, **ohne Overlay-Bruch** |
| Dringlichkeit | regulär – eingeplant mit D-406 |
| Status | 🟢 **entschieden am 2026-09-26** (E1 bis E9) |

---

## 1. Anlass

`K-153`: fünf Anweisungen in Skills weichen von ihrem Core-Modul oder ihrer Zelle ab, und `1.11.0` durfte
sie nicht ändern, weil jede Änderung ein Testblatt öffnet (D-303). Die fünfte hält Kriterium 2 von D-11 seit
`1.11.0` auf 1: `SK-002-N03` hält an einer gekennzeichneten, ungeöffneten K3-Fixture nicht an.

## 2. Die Vorprüfung

Die Vorprüfung vor der Vorlage hat den Umfang zweimal verschoben: „K2 (bereinigt)“ steht nicht nur in
`fw-error-analyze`, sondern in **sechs** Skills und vier Prompts – und die Klassendefinition K2 schließt die
Freigabe schon ein. Der K3-Auslöser steht in **elf** von zwölf Skills. Die übrigen Befunde des
Vorbedingungsdurchgangs stehen im Protokoll (`tests/protocols/2026-09-26-skill-anweisungen.md` Abschnitt 2).

## 3. Die Messung

57 Sitzungsläufe mit `claude-code` 2.1.283 (Opus 5.5), 32,32 USD. **`SK-002-N03` trägt** – der Lauf hält an
und empfiehlt die Meldung; der Kontrolllauf ohne die Datenschutzregeln tut beides nicht. 🔴 **Sechs andere
Zellen tragen nicht**, keine wegen einer Änderung dieses Releases; die Einzelheiten stehen im Protokoll,
Abschnitte 3 und 4.

## 4. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | `fw-change-small`: Kontakt bei R4? | 🟢 **R3 und R10 `<SECURITY_CONTACT>`, R4 `<DATA_PROTECTION_CONTACT>`** wie `09-risk-model.md` (D-419) | – |
| **E2** | `fw-refactor`: Plan **oder** Freigabe bei Stufe hoch? | 🟢 **Plan und Freigabe**, kumulativ (D-419) | Keine Zelle fährt Stufe hoch |
| **E3** | K2 ohne Freigabe? | 🟢 **Keine Skilländerung;** Klarstellung im Modul, Konvention und Prompts (D-420) | Die Tabelle eines Skills sagt die Freigabe nicht selbst |
| **E4** | `fw-plan`: die feste Planablage? | 🟢 **Nach Zeile M4 der Fähigkeitsmatrix**; M4 bleibt für zwei Packs `BELEG OFFEN` (D-419) | Keine Zelle prüft die Ablage |
| **E5** | Die fehlende Spalte für `kiro` (gefunden bei E4) | 🟢 **Nachgetragen; Prüfung 20 verlangt je Pack eine Spalte** (D-421) | – |
| **E6** | Der K3-Auslöser: wie weit präzisieren? | 🟢 **Auch eine als K3 erkannte oder gekennzeichnete, ungeöffnete Datei; in den vier ohnehin geöffneten Skills** (D-419), die übrigen sieben als `K-165` | Auch ein Positivfall hält an (`SK-004-P02`) |
| **E7** | Der Plan nach dem Auftrag des Owners | 🟢 **`1.15.0` Verständlichkeit (eingegrenzt), `1.16.0` Cursor, `1.17.0` Paketquellen;** der Rest des Auftrags als `K-166` (D-422) | Paketquellen kommen später |
| **E8** | Pflichtüberschriften, die der Lauf umschreibt | 🟢 **Das Prüfmittel vergleicht zusätzlich die Bezeichnung** (D-423, Antwort des Owners) | Es verzeiht, was D-194 als Befund führte |
| **E9** | Sechs offene Zellen | 🟢 **`1.14.1` direkt danach** (D-424, Antwort des Owners) | Kriterium 2 von 1 auf 6 |

## 5. Umsetzung

1. Vier Skills: `fw-change-small` `0.1.7`, `fw-refactor` `0.1.4`, `fw-plan` `0.1.6`, `fw-code-explain` `0.1.6` – Anweisungen und Änderungsverläufe (*Anweisung berührt*).
2. `02-privacy.md` Abschnitt 4, `08-skill-conventions.md` Zeile 9, Prompts `02` bis `05` (K2; Planablage in `03`).
3. Platzhalterregister und Laufzeitglossar: Spalte `kiro`; Prüfung 20 mit Sonde und Gegenprobe.
4. `validate-output.py`: Vergleich an der Bezeichnung, Selbstprobe A8 bis A11.
5. `k-bauen-b3.py`: Klasse `bew` mit Stammmuster.
6. Nachlauf der 25 Zellen; Zellen eingetragen, Erwartung von `SK-005-N03` angeglichen.
7. Register, Roadmap (Kette von Kriterium 2 einschließlich des fehlenden Glieds von `1.11.0`), Hauptdokument, CHANGELOG, `VERSION`, Bestandsliste; Hebung beider Projekte und Bau der Erzeugnisse.

## 6. Entscheidung

🟢 **Angenommen am 2026-09-26.** E1 bis E7 wie vorgelegt (*„Passt.“*, mit der Eingrenzung von `1.15.0` durch den Owner); E8 und E9 hat der Owner während der Auswertung entschieden.

| # | Entscheidung | Decision Record |
|---|---|---|
| E1, E2, E4, E6 | Anweisungen angeglichen, K3-Auslöser, Nachlauf | D-419 |
| E3 | K2 heißt bereinigt und freigegeben | D-420 |
| E5 | Prüfung 20 je Pack | D-421 |
| E7 | Releaseplan | D-422 |
| E8 | Bezeichnung statt Wortlaut | D-423 |
| E9 | `1.14.1` | D-424 |
