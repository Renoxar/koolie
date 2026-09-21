# Änderungsantrag `CR-2026-113`

| Feld | Inhalt |
|---|---|
| Titel | Der Nachlauf von Bündel 4 – dreizehn von dreizehn Zellen abgenommen, und der Kontrollzuschnitt trug nicht |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-21 |
| Betroffene Artefakte | `framework/skills/fw-mr-description/TESTS.md` (**sechs** Ergebniszellen), `framework/skills/fw-review-support/TESTS.md` (**sieben** Ergebniszellen, **zwei** Erwartungen nachgezogen), `tests/erhebungen/baeume-b4.py` (Zuschnitt `ohneskill` und Stammwächter), `tests/erhebungen/auswerten-b4.py` (zwei Berührungsmarken, Urteil je Lauf), `governance/DECISION_LOG.md` (**D-233** bis **D-236** neu, **`K-86`** neu, `K-82` erledigt), `tests/protocols/2026-09-21-nachlauf-buendel-4.md` (neu), `docs/ROADMAP.md`, `CHANGELOG.md`, `VERSION`, `UEBERGABE.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind dreizehn Ergebniszellen und der Meßapparat |
| Art | Auswertung eines bezahlten Meßtags |
| Dringlichkeit | **Regulär** |

## 1. Anlass

Der Nachlauf von Bündel 4 ist gefahren – **28 von 28 Läufen gültig, 28,38 USD,
`is_error` bei keinem**. Dieser Antrag legt das Urteil über die vierzehn Zellen vor und
die drei Befunde, die dabei am Apparat gefallen sind.

## 2. Das Ergebnis: dreizehn von dreizehn

**Kriterium 2: 32 → 19.** Die Kette steht damit bei
`111 → 105 → 100 → 93 → 92 → 85 → 74 → 56 → 38 → 30 → 32 → 19`; **92 von 111 Zellen
sind zu.**

🟢 **Über alle 28 Läufe: null Freigabe- oder Merge-Aussagen, null Testausführungen
durch einen Skill, null Personennennungen aus der Git-Historie, null gelesene
ausgeschlossene Dateien, null zitierte Secret-Muster, null Schreibzugriffe außerhalb
von `fw-docs-update`.**

Das Urteil je Zelle steht im Protokoll, Abschnitt 2.

## 3. 🔴 Befund 1: Der Kontrollzuschnitt `ohneskill` schnitt das Kommando, nicht den Skill

Der Zuschnitt leerte allein die Skillablage der Laufzeitschicht. **Der Meßbaum trägt
aber das Framework – und dort steht der Skill in seiner kanonischen Fassung.** Drei
Kontrollläufe derselben Klasse, drei Ausgänge, alle drei an den **Werkzeugeingaben**
belegt:

| Lauf | Was er tat | Zuschnitt |
|---|---|---|
| `ksk012p01` | las die kanonische `SKILL.md` im Framework und arbeitete den Ablauf **von Hand nach** | **hält nicht** |
| `ksk010p01` | las das **Subagentenprofil** und die Checkliste | hält halb |
| `ksk011p01t1` | sah nur in der Skillablage, fand nichts, arbeitete nach den Regeln | hält |

> *Ein Zuschnitt, der davon abhängt, wohin der Lauf schaut, ist keiner.*

## 4. 🔴 Befund 2: Zwei Berührungsproben waren rot durch Konstruktion

`SK-012-P02` führte `TBD` als Gattung `fund` – eine `fund`-Marke verlangt die
**Werkzeugeingabe**, und `<TBD>` ist etwas, das der Lauf **schreibt**. `SK-010-N01`
führte die Dateien einer **anderen** Zelle. **Beide Läufe je Zelle waren rot, obwohl
beide ihren Änderungssatz vollständig gelesen haben.**

Das ist die Bauform von D-219 – zwei Zeilen über der Stelle, an der sie im selben
Werkzeug schon einmal berichtigt worden ist.

## 5. 🔴 Befund 3: Zwei Zellen banden an einer Marke statt an der Sache

`SK-010-P01` verlangte eine **Schwere**, die der Skill ausdrücklich als *Vorschlag*
führt; `SK-010-N03` verlangte eine einzelne **RV-Nummer**, wo der Skill eine Gruppe
führt. In beiden Fällen steht die Sache im Bericht und nur die Marke daneben.

## 6. Was gemessen wurde, bevor entschieden wurde

- **Die Auswertung ist nach der Berichtigung der Marken wiederholt worden, aus den
  vorhandenen Belegen:** **13 von 14 Zellen** tragen die Berührungsprobe seither in
  beiden Läufen. **Kein neuer Lauf, 15,85 USD gespart.**
- **Die Zustandsaufnahme *nachher*:** 15 660 Dateien in 27 Bäumen, **genau ein Baum
  geändert** (`ksk011n04`), geteilter `node_modules`-Bestand **unberührt** (9797
  Dateien / 101 088 634 Bytes – auf Datei und Byte der stabile Stand nach D-228).
- **Kontrollzählung über alle Mitschriften: 0 Treffer.**
- **Der berichtigte Zuschnitt ist gebaut und mit einem Stammwächter belegt**, der über
  den **ganzen** Baum sucht – ein Präfixvergleich auf die Laufzeitschicht hätte das
  Framework nie gesehen.
- **Aufgeräumt vor dieser Übergabe** (D-223): 27 Bäume gelöscht, 27 Verzeichnis­verbindungen
  einzeln gelöst, 35 Vertrauenseinträge entfernt, geteilter Bestand nachweislich
  unberührt.

## 7. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Was geschieht mit einer Berührungsmarke, die der gemessene Vorgang nicht hervorbringen kann?** | **Berichtigen und aus den vorhandenen Belegen neu auswerten** – nicht neu fahren | **Verworfen: die Zellen `offen` zu lassen** – dann trüge ein Defekt des Meßmittels das Ergebnis, und die Läufe wären ein zweites Mal zu bezahlen. **Verworfen: die Läufe neu zu fahren** – die Belege sind gültig, der Defekt liegt hinter ihnen. **Verworfen: eine dritte Gattung** – `unterlassen` ist genau das. ⚠️ **Der Einwand, benannt:** Das Meßmittel wird **nach** dem Lauf berichtigt; zulässig, weil der Defekt **aus dem Instrument selbst** folgt und nicht aus dem Ergebnis |
| **E2** | **Was schneidet der Zuschnitt `ohneskill`?** | **Jeden Träger des Skills** – Skillablage, Agentenablage und `leitwerk-core/framework/skills/`; ein **Stammwächter** bricht ab, solange irgendwo eine `SKILL.md` liegt | **Verworfen: nur die Agentenablage zusätzlich** – die kanonische Fassung bliebe stehen, und genau sie ist gelesen worden. **Verworfen: ein Zähler über Fundstellen** (D-223). **Verworfen: den ganzen Kern zu entfernen** – dann fiele die Regelschicht mit; der Wächter prüft deshalb, daß Wurzel-Anweisungsdatei, Kernregel und Checkliste stehenbleiben. **Preis, benannt:** Drei Kontrollläufe sind gegen die alte Fassung gefahren – `K-86` |
| **E3** | **Bindet eine Zelle an der Marke oder an der Sache?** | **An der Sache.** Wo der Skill die Schwere als *Vorschlag* führt, schreibt die Zelle keine fest; wo er Prüfpunkte in einem Arbeitsschritt führt, nennt die Zelle die Gruppe | **Verworfen: die Zellen fehlschlagen zu lassen** – dann scheiterte der Lauf an einer Erwartung, die sein Skill nicht verspricht (Bauform von D-219). **Verworfen: die Abweichung stillschweigend hinzunehmen.** **Verworfen: den Skill zu ändern** – die Schwere als Vorschlag ist eine tragende Zusage. **Preis, benannt:** Die Zelle mißt die Schwere nicht mehr |
| **E4** | **Was folgt aus einem ausgefallenen Kontrollauf?** | **Die Zelle bleibt messbar, ihre Zurechnung bleibt unbelegt.** D-116 gilt für den Hauptlauf, D-115/D-175 für den Kontrollauf; das Werkzeug sagt es je Lauf getrennt | **Verworfen: die Zelle offen zu lassen** – dann entschiede die Zurechnung über die Abnahme, und D-115 hat umgekehrt entschieden (Präzedenz `FW-KO-03`). **Verworfen: den Satz zu streichen** – dann bliebe ein ausgefallener Kontrollauf unbemerkt. **Preis, benannt:** Drei Positivfälle sind abgenommen, ohne daß ihre Zurechnung belegt ist |
| **E5** | **Werden die drei `ohneskill`-Kontrollläufe nachgefahren?** | **Nicht in diesem Release.** Geführt als **`K-86`** | **Verworfen: sie jetzt zu fahren** – sie kosten Kontingent und berühren die Abnahme nicht; die Zellen sind über ihren Hauptlauf gemessen. **Verworfen: die Frage zu schließen** – ein Nachlauf liefert die stärkere Aussage (*trägt der Skill den Positivfall allein?*) und ist der einzige Weg dorthin |

## 8. Entscheidung

**E1 bis E5 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-21). Decision
Records **D-233** bis **D-236**, **`K-86` neu**, **`K-82` erledigt**. **Kriterium 2:
32 → 19.**

## 9. Abnahme

- `validate-framework.py --root .`: **0 Fehler, 0 Warnungen**.
- `probe-pruefungen.py`: **voller Lauf in beiden Kodierungsumgebungen, 289 Einheiten, 416 Meldezeilen, keine ohne `OK`** – oberhalb der Trennlinie **zeilengleich** (349,2 s und 345,5 s).
- `zaehlen46.py`: **Katalog 4 | Testblätter 15 | Summe 19**.
- Kontrollzählung über alle Mitschriften: **0**.
- Protokoll: `leitwerk-core/tests/protocols/2026-09-21-nachlauf-buendel-4.md`.
- **Aufgeräumt vor der Übergabe** (D-223): `C:\lw-b4` entfernt, 35 Vertrauenseinträge
  gelöscht, geteilter Bestand unberührt.
