# Änderungsantrag `CR-2026-041`

| Feld | Inhalt |
|---|---|
| Titel | S5 ist bei `claude-code` `[NICHT ABBILDBAR]` – und die Folge, die `clients/README.md` daran knüpft, ist nicht gemeint |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-12 |
| Betroffene Artefakte | `clients/README.md` (Abschnitt 4, verbindliche Folgen), `clients/claude-code/CLIENT_PACK.md` (S5), `clients/devin-desktop/CLIENT_PACK.md` (S5), `clients/_template/CLIENT_PACK.md`, `governance/DECISION_LOG.md` |
| Ebene laut Entscheidungsbaum 6 | Kern – Bedeutung und Rechtsfolge einer Einstufungsklasse; betrifft **beide** Client Packs |
| Art | Befund aus der Erhebung vom 2026-09-12 (S5); Präzisierung der Folgen von `[NICHT ABBILDBAR]` |
| Dringlichkeit | regulär – aber vor dem nächsten Onboarding zu entscheiden, weil die Folge eine Inbetriebnahme blockiert |

## 1. Anlass und Problem

Die Erhebung vom 2026-09-12 hat S5 für `claude-code` beantwortet
(`tests/protocols/2026-09-12-erhebungen-K28-S5-B9-bypass.md`, Abschnitt 2.2). Das Ergebnis ist
zweigeteilt:

- **Gut:** Fremde Skill-Ablagen führt dieser Client nicht mit. Vier Sonden in vier fremden
  Ablagen blieben ungeführt, die fünfte in der eigenen Ablage wurde geführt.
- **Nicht gut:** Die Zusage der Zeile selbst – *vollständig aufzählbar, samt Herkunft und
  Aufrufbarkeit* – ist nicht eingelöst. Es gibt **kein Aufzählungskommando**: `claude --help`
  kennt keinen Unterbefehl für Skills, `claude doctor` nennt keine Skill-Pfade, und die Sitzung
  erhält Skills als Name und Kurzbeschreibung ohne Pfad. Sie antwortete auf die Frage nach der
  Herkunft wörtlich „Herkunft unbekannt — für alle 84".

Die Zeile trägt deshalb seit dieser Messung `[NICHT ABBILDBAR]`. Das ist die zutreffende
Einstufung: *„Der Client bietet keinen Mechanismus."*

### Die Folge, die daran hängt

`clients/README.md` Abschnitt 4 knüpft daran eine verbindliche Folge:

> Ein Client Pack, das eine **Kernzusage** auf `[NICHT ABBILDBAR]` setzt, DARF nicht ohne Freigabe
> durch `<SECURITY_CONTACT>` in Betrieb genommen werden.

**Der Begriff „Kernzusage" ist nirgends definiert.** Die Spaltenüberschrift der Matrix heißt
„Zusage des Frameworks"; der B-Block führt eine eigene Spalte „Kern" mit `ja`/`–`; der erste
Aufzählungspunkt desselben Abschnitts spricht enger von „einer Kernzusage **aus
`_core_rules_integrity`**". Ob S5 darunter fällt, lässt sich dem Text nicht entnehmen.

Das ist keine Spitzfindigkeit, sondern entscheidet zwei Dinge auf einmal:

1. Ob das Pack `claude-code` ab sofort eine Freigabe von `<SECURITY_CONTACT>` braucht.
2. Ob D-27 noch gilt. Die Roadmap führt als Ergebnis: *„keine Einstufung des Packs steht mehr auf
   `[NICHT ABBILDBAR]`."* Seit dieser Messung steht wieder eine dort.

### Warum die Sperrklausel hier vermutlich nicht gemeint war

Sie steht zwischen zwei Sätzen, die beide von **Sicherheitszusagen** handeln – der erste nennt
`_core_rules_integrity` ausdrücklich, der dritte verlangt für `[TECHNISCH]` einen Beleg gegen eine
reale Installation. S5 ist keine Sicherheitszusage, sondern eine **Transparenzzusage**: Sie sagt
nicht zu, dass etwas verhindert wird, sondern dass man nachsehen kann. Ihr Ausfall ist ernst –
aber er sperrt keine Schranke auf.

**Die Gegenprobe fällt allerdings unangenehm aus.** Gerade weil ein Skill Verfahren in die Sitzung
bringt, die niemand im Projekt gelesen hat (`AP2-DD-16`, K-24), ist Aufzählbarkeit das einzige
Mittel, das überhaupt bemerkt. Wer die Sperrklausel hier abräumt, sollte den Verlust ersetzen und
nicht bloß abbuchen – siehe E3.

## 2. Vorgeschlagene Änderung

1. **`clients/README.md` Abschnitt 4 definiert „Kernzusage".** Formulierungsvorschlag:

   > **Kernzusage** im Sinne dieses Abschnitts ist jede Zeile des B-Blocks mit `Kern = ja` sowie
   > jede Regel aus `_core_rules_integrity` der Berechtigungsdatei. Zusagen der übrigen Blöcke
   > sind Fähigkeitszusagen: Ihr Ausfall wird im Pack begründet und im Overlay des aufnehmenden
   > Projekts als bekannte Einschränkung geführt, sperrt die Inbetriebnahme aber nicht.

2. **S5 wird im Pack als das ausgewiesen, was fehlt** – nicht nur als Klasse. Die Zeile trägt
   bereits den Messbefund; ergänzt wird der Hinweis auf den Ersatz nach E3.

3. **Ersatz durch das Framework statt durch den Client (E3).** Die Installation kennt jeden Skill,
   den sie schreibt, und der Validator liest die Ablage ohnehin. Vorgeschlagen wird ein
   Aufzählungsschalter des Frameworks – `install.py --list-skills` –, der je Skill Name, Pfad,
   Herkunft (Kern, Overlay, Projekt) und Aufrufbarkeit (`disable-model-invocation`) ausgibt.
   **Das ersetzt nicht, was der Client verschweigt** – Skills aus Ablagen außerhalb des
   Repositoriums sieht auch das Framework nicht –, aber es macht den Teil aufzählbar, für den das
   Framework einstehen kann.

4. **Die Zeile S5 des Packs `devin-desktop` wird nachgezogen.** Dort steht `[TEXTUELL]` mit dem
   Vorbehalt aus ERH-03 (die Pfadauskunft nennt die größte Ablage nicht). ERH-17 setzt daneben
   einen zweiten Befund: Der Block `<available_skills>` **nennt** je Skill den vollen Quellpfad –
   die Auskunft existiert, nur nicht in dem Kommando, das sie verspricht. Beides gehört in die
   Zeile.

5. **D-27 und die Roadmap** werden fortgeschrieben: Der Satz „keine Einstufung steht mehr auf
   `[NICHT ABBILDBAR]`" beschreibt einen Stand, der seit dem 2026-09-12 nicht mehr gilt.

## 3. Was dieser Antrag nicht ändert

- **Die Einstufung selbst.** `[NICHT ABBILDBAR]` ist gemessen und steht nicht zur Disposition.
  Zur Entscheidung steht allein, welche Folge das Regelwerk daran knüpft.
- **Die Definition der drei Klassen.** Abschnitt 4 behält seine Tabelle unverändert.
- **S4.** Die Zusage über benutzergetriggerte Skills ist am selben Tag an ihrer Wirkung belegt
  worden (ERH-13) und wird hier nicht berührt.

## 4. Prüffragen

- [x] Richtige Ebene: Kern – die Klausel steht in `clients/README.md` und gilt für jedes Pack.
- [x] Verschärfungsprinzip: Die vorgeschlagene Definition **lockert** eine Klausel. Sie ist
      deshalb ausdrücklich als Ermessensfrage vorgelegt (E1) und nicht als Redaktion.
- [x] Widerspruchsfreiheit: D-27, `CR-2026-017`, `CR-2026-032`, D-34 gelesen.
- [ ] Laufzeitfassungen betroffen: nur bei Annahme von E3 (`install.py`).
- [x] Belegstatus: gemessen, ein Lauf mit Positivkontrolle und vier Negativsonden.
- [ ] Test- und Validierungsbedarf: bei Annahme von E3 eine Prüfung samt Sonde nach D-23.
- [x] Overlays: Bei Annahme von E1 führt das aufnehmende Projekt S5 als bekannte Einschränkung.
- [ ] Dokumentation: CHANGELOG, Decision Log, ROADMAP (Stand zu D-27).

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Sperrt `[NICHT ABBILDBAR]` bei S5 die Inbetriebnahme? | **Nein – und der Begriff „Kernzusage" wird definiert, statt im Einzelfall ausgelegt zu werden.** Eine Transparenzzusage ist keine Schranke; die Klausel war für Sicherheitszusagen gedacht | Eine Klausel wird gelockert, und zwar in dem Augenblick, in dem sie das erste Mal greifen würde. Das ist der unangenehmste denkbare Zeitpunkt für eine Lockerung – und genau deshalb gehört die Frage vorgelegt und nicht redaktionell entschieden |
| E2 | Die Definition im Kern oder je Pack? | **Im Kern** (`clients/README.md`). Eine Rechtsfolge, die für jedes Pack gilt, darf nicht je Pack ausgelegt werden | Der Kern wächst um eine Definition. Wer ein neues Pack schreibt, muss sie kennen |
| E3 | Den Ausfall durch das Framework ersetzen? | **Ja, `install.py --list-skills`.** Aufzählbarkeit ist das einzige Mittel, das einen unbemerkten Skill überhaupt bemerkt; sie ganz aufzugeben, wäre die schlechtere Lage | Ein neuer Schalter, eine neue Prüfung, eine neue Sonde. Und eine Teilauskunft, die mehr verspricht, als sie leistet, wenn niemand dazusagt, dass fremde Ablagen darin fehlen – genau der Befundtyp dieses Projekts. Der Satz muss in die Ausgabe, nicht nur in die Dokumentation |
| E4 | S5 bei `devin-desktop` nachziehen? | **Ja.** ERH-17 ist dort ein eigener Befund: Die Herkunft steht im Sitzungskontext, das Kommando gibt sie nicht. Das gehört neben ERH-03 in dieselbe Zeile | Die Zeile wird lang. Sie trägt dann drei Belege für dieselbe Zusage, zwei davon einschränkend |
| E5 | D-27 als überholt kennzeichnen? | **Fortschreiben, nicht aufheben.** Der Satz war zum Zeitpunkt der Entscheidung richtig; er beschreibt einen Stand, keinen Beschluss | Die Roadmap-Tabelle trägt eine Einschränkung in einer Zeile, die bisher als Erfolg gelesen wurde |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle fünf Fragen wie vorgelegt.** E1 `[NICHT ABBILDBAR]` bei S5 sperrt die Inbetriebnahme **nicht**; der Begriff „Kernzusage" wird definiert statt im Einzelfall ausgelegt. E2 die Definition steht im Kern. E3 der Ausfall wird ersetzt: `install.py --list-skills`. E4 S5 bei `devin-desktop` wird um ERH-17 nachgezogen. E5 D-27 wird fortgeschrieben, nicht aufgehoben |
| Datum | 2026-09-12 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | **Die Lockerung gilt nur zusammen mit dem Ersatz.** Eine Fähigkeitszusage auf `[NICHT ABBILDBAR]` MUSS den Ersatz benennen oder festhalten, dass es keinen gibt; **Prüfung 25** setzt das durch und ist nach D-23 mit Sonde und Gegenprobe belegt. Beim ersten Lauf meldete sie **zwei** Zeilen ohne benannten Ersatz (S5 und X2) – die Lücke, gegen die sie gebaut ist, war bereits da. Die Ausgabe von `--list-skills` MUSS ihre eigene Grenze nennen; auch das ist als Sonde belegt |
| Umsetzung | umgesetzt mit `0.27.0` |
