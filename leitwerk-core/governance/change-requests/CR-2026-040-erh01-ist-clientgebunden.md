# Änderungsantrag `CR-2026-040`

| Feld | Inhalt |
|---|---|
| Titel | Der Kern schreibt einen Befund über **einen** Client als Aussage über **alle** – K-28 widerlegt ihn für das zweite Pack |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-12 |
| Betroffene Artefakte | `framework/runtime/root-instruction.md` (Kopfkommentar), `tests/scripts/validate-framework.py` (Kopfkommentar und Meldungstext der Prüfung 23), `clients/devin-desktop/CLIENT_PACK.md` (Regelladung), `governance/DECISION_LOG.md` (K-28, D-38) |
| Ebene laut Entscheidungsbaum 6 | Kern – Laufzeitfassung der Wurzel-Anweisung und Validator |
| Art | Befund aus der Erhebung vom 2026-09-12 (K-28); **keine AP2-Kennung** |
| Dringlichkeit | regulär – die Maßnahme aus `CR-2026-039` bleibt in der Sache richtig; falsch ist ihre **Begründung** |

## 1. Anlass und Problem

`CR-2026-039` hat einen normativen Satz aus dem Kopfkommentar der Wurzel-Anweisungsdatei in den
Fließtext gehoben, weil der Kommentar die Sitzung nicht erreicht (ERH-01). An seiner Stelle steht
seither im Kommentar derselben Datei der Satz:

```text
Ein Kommentar erreicht die Sitzung nicht (ERH-01) - was gilt, steht im Fließtext, Abschnitt 2.
```

Dieselbe Aussage trägt der Validator an drei Stellen – im Kopfkommentar, in der Beschreibung der
Prüfung 23 und in ihrem Meldungstext.

**Der Satz ist für das zweite Pack falsch.** Am 2026-09-12 ist K-28 erhoben worden
(`tests/protocols/2026-09-12-erhebungen-K28-S5-B9-bypass.md`, Abschnitt 2.1): Bei
`devin-desktop` steht der Kommentar **wörtlich** im Regelblock, den der Client selbst bildet – die
Mitschrift führt ihn samt Kommentarklammern, und die Sitzung gab die Marke aus dem Kommentar
zurück, ohne eine Datei zu lesen (`"tool_calls": []`).

### Warum das nicht bloß eine Ungenauigkeit ist

`framework/runtime/root-instruction.md` und der Validator sind **Kernartefakte**. Sie sind
werkzeugneutral – das ist der Sinn von D-15 und D-28. Ein Satz, der das Verhalten **eines**
Clients zur allgemeinen Eigenschaft erklärt, ist dort dieselbe Konstruktion, die dieses Projekt
seit Releases in Client Packs aufspürt: eine Aussage, die mehr behauptet, als gemessen ist. Dass
sie diesmal in einem Kommentar steht, den bei `claude-code` niemand liest, macht es nicht besser –
bei `devin-desktop` steht sie in jeder Sitzung im Kontext, und dort ist sie unzutreffend.

### Was dadurch **nicht** falsch wird

Die Maßnahme selbst trägt weiter, und zwar mit einer besseren Begründung als bisher:

> Ein Kommentar in einem Kernartefakt erreicht die Sitzung **bei dem einen Client, beim anderen
> nicht.** Genau deshalb ist er als Ablageort für einen normativen Satz untauglich: Was gilt,
> darf nicht davon abhängen, mit welchem Werkzeug gearbeitet wird.

Das ist stärker als die alte Begründung. Die alte sagte „erreicht die Sitzung nicht" und wäre mit
einem Client, der Kommentare durchreicht, hinfällig. Die neue sagt „erreicht sie uneinheitlich"
und wird durch genau diese Messung **bestätigt**.

## 2. Vorgeschlagene Änderung

1. **Kopfkommentar der Wurzel-Anweisungsdatei.** Statt einer Behauptung über Clients ein Satz
   über den Kern:

   > `Was gilt, steht im Fließtext, Abschnitt 2 - ein Kommentar erreicht nicht jede Sitzung`
   > `(ERH-01, K-28).`

2. **Prüfung 23 im Validator.** Kopfkommentar und Meldungstext werden entsprechend gefasst: Die
   Prüfung besteht, weil das Ladeverhalten von HTML-Kommentaren **clientabhängig** ist, nicht weil
   Kommentare grundsätzlich verloren gingen. Die Prüfung selbst, ihre Wortliste und ihre Sonde
   bleiben unverändert – es ändert sich kein Prüfergebnis.

3. **`clients/devin-desktop/CLIENT_PACK.md`.** Der Abschnitt zur Regelladung erhält den gemessenen
   Satz: Bei diesem Client geht der HTML-Kommentar einer Regeldatei **in den Kontext ein**.
   Damit steht in beiden Packs, was für den jeweiligen Client gilt – das ist der Ort dafür, nicht
   der Kern.

4. **K-28 schließt** (`governance/DECISION_LOG.md`): beantwortet mit „nein", Beleg das Protokoll
   vom 2026-09-12.

## 3. Was dieser Antrag nicht ändert

- **Prüfung 23 bleibt, wie sie ist.** Weder Wortliste noch Sonde noch Gegenprobe werden berührt;
  kein Prüfergebnis ändert sich. Geändert wird ausschließlich die Begründung im Text.
- **D-38 bleibt gültig.** Normative Aussagen gehören in den Fließtext. Die Entscheidung wird
  bestätigt, nicht aufgehoben – nur ihre Begründung wird die belastbarere.
- **Der Kommentar von `CR-2026-039` wird nicht zurückgenommen.** Der normative Satz bleibt im
  Fließtext.

## 4. Prüffragen

- [x] Richtige Ebene: Kern, weil die falsche Aussage in einem Kernartefakt steht; die
      clientgebundene Aussage wandert ins Pack.
- [x] Verschärfungsprinzip: unberührt, es ändert sich keine Regel.
- [x] Widerspruchsfreiheit: D-38, `CR-2026-039`, Prüfung 23, beide Packs gelesen.
- [x] Laufzeitfassungen betroffen: ja, `framework/runtime/root-instruction.md`; beide Packs
      erzeugen daraus, die Änderung erreicht beide über `install.py`.
- [x] Belegstatus: gemessen, ein Lauf mit Positivkontrolle und Mitschrift.
- [ ] Test- und Validierungsbedarf: Validatorlauf; **keine** neue Prüfung, **keine** neue Sonde –
      Prüfung 23 bleibt unverändert.
- [x] Overlays: nicht betroffen.
- [ ] Dokumentation: CHANGELOG, Decision Log (K-28, D-38 fortgeschrieben).

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Den Satz im Kern korrigieren oder streichen? | **Korrigieren.** Ein Hinweis, warum der Fließtext der Ort ist, gehört an die Stelle, an der jemand den Kommentar erweitern will. Gestrichen wäre die Falle wieder unmarkiert | Der Kommentar der Wurzel-Anweisungsdatei bleibt eine Zeile lang – in der Datei, für die das Framework Least Context fordert |
| E2 | Prüfung 23 im Zuschnitt ändern? | **Nein.** Sie trifft weiterhin genau den Fehler, und ihre Berechtigung wird durch K-28 eher größer: Was bei einem Client verschwindet und beim anderen mitläuft, ist als Ablageort erst recht untauglich | Die Prüfung bleibt eine Wortlistenprüfung mit den bekannten Fehlalarmen (`CR-2026-039` E3) |
| E3 | Den gemessenen Satz ins Pack `devin-desktop` aufnehmen? | **Ja.** Er ist für die Regelladung dieses Clients erheblich und steht sonst nirgends: Wer dort einen Kommentar schreibt, schreibt in den Sitzungskontext | Eine weitere Zeile im Pack; die Asymmetrie zwischen den Packs wird sichtbar statt stillschweigend |
| E4 | Die strengere Lesart für `devin-desktop` beibehalten? | **Ja, aber neu begründet.** Nicht mehr „vorsorglich, weil unerhoben", sondern „weil das Verhalten clientabhängig ist". Aus einer Annahme wird ein Grund | Keiner in der Sache. Der Preis ist redaktionell: Zwei Stellen tragen künftig unterschiedliche Begründungen für dieselbe Regel |
| E5 | Auch den `claude-code`-Abschnitt zu K-18 anfassen? | **Nein.** Er beschreibt korrekt das Verhalten **seines** Clients und ist durch ERH-01 gedeckt | Die Formulierung „zählt hier vorsorglich zum ständigen Kontext" bleibt stehen, obwohl ERH-01 sie erübrigt – ein eigener, kleinerer Befund für eine spätere Durchsicht |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle fünf Fragen wie vorgelegt.** E1 korrigieren statt streichen; E2 Prüfung 23 im Zuschnitt unverändert; E3 der gemessene Satz kommt in das Pack `devin-desktop`; E4 die strengere Lesart bleibt, neu begründet; E5 der `claude-code`-Abschnitt zu K-18 bleibt unberührt |
| Datum | 2026-09-12 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | **Kein Prüfergebnis darf sich ändern.** Nachgewiesen: Validator vor und nach der Änderung 0 Fehler, 0 Warnungen; Sonde und Gegenprobe zu Prüfung 23 unverändert bestanden. Die Sonde zu Prüfung 23 hat dabei ihren Suchtext verloren und musste nachgezogen werden – der Vorfall steht in D-43 |
| Umsetzung | umgesetzt mit `0.27.0` |
