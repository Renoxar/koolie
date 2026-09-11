# Änderungsantrag `CR-2026-034`

| Feld | Inhalt |
|---|---|
| Titel | Was ein Nachweis aus dem nicht-interaktiven Betrieb belegt – und was nicht |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-11 |
| Betroffene Artefakte | `tests/TEST_CATALOG.md` (Abschnitt 1, Verfahren), `clients/devin-desktop/CLIENT_PACK.md` (Abschnitt 5), `governance/DECISION_LOG.md` (Fortschreibung D-23) |
| Ebene laut Entscheidungsbaum 6 | Kern – Testverfahren; Client Pack nur nachrichtlich |
| Art | Behebung von `AP2-DD-13` (Schwere: niedrig) und `AP2-DD-14` gemeinsam |
| Dringlichkeit | regulär |

## 1. Anlass und Problem

Zwei Befunde der AP2-Sitzung betreffen nicht das Framework, sondern die **Bedingungen, unter
denen seine Nachweise entstehen**:

| Befund | Beobachtung |
|---|---|
| `AP2-DD-13` | Ein Shell-Befehl im Standardmodus verlangt eine Bestätigung. Nicht-interaktiv kann sie nicht gestellt werden; der Lauf endet **ohne jede Ausgabe mit Exit 0** |
| `AP2-DD-14` | `Error: Refusing to run in an untrusted workspace`. Erst `--respect-workspace-trust false` oder eine interaktive Bestätigung lassen den Lauf überhaupt zu |

Beide führen zur selben Falle: **Ein Lauf, der gar nicht stattgefunden hat, sieht aus wie ein Lauf
mit leerem Ergebnis.** Beim ersten stimmt sogar der Exit-Code.

### Warum das die Beweisführung dieses Protokolls trifft

Der schwerste Befund des Protokolls – `AP2-DD-10`, die nie gelesene Hook-Datei – beruht auf einer
**Abwesenheitsmessung**: null Hook-Aufrufe in vier Konfigurationen. Das ist genau die Form von
Beleg, die ein stiller Abbruch erzeugen kann, ohne dass es auffällt.

Der Befund hält trotzdem – aber nicht wegen der Messung, sondern wegen der Gegenprobe: **G-2 hat
denselben Fall interaktiv in der Agent-Sidebar wiederholt**, mit einem echten `exec`-Aufruf, der
sichtbar lief und trotzdem keine Aufzeichnung erzeugte. Dazu kommt der Positivbeleg aus derselben
Messreihe: Dieselben Hooks in der Berechtigungsdatei lösten **sofort** aus.

**Der stärkste Befund des Protokolls hing damit an einer Gegenprobe, nicht am Messwert.** Dass es
gut ausging, ist kein Verfahren.

### Was das Verfahren heute sagt

`TEST_CATALOG.md` Abschnitt 1 regelt Prüfmethoden, Voraussetzungen (PyYAML), Ergebnisstatus und
die Angaben dynamischer Tests. D-23 verlangt für **Prüfungen** einen Wirksamkeitsnachweis: eine
Sonde mit bekanntem Defekt, die gemeldet wird.

Für **Sitzungsnachweise** gibt es die Entsprechung nicht. Ein ausbleibendes Ereignis zählt als
Beleg, ohne dass belegt sein müsste, dass überhaupt gemessen wurde. Das ist dieselbe Lücke, die
D-23 für Prüfungen geschlossen hat – eine Ebene höher.

## 2. Vorgeschlagene Änderung

1. **Neue Nummer 7 in `TEST_CATALOG.md` Abschnitt 1 (normativ)**, Formulierungsvorschlag:

   > **Nachweise aus dem nicht-interaktiven Betrieb.** Ein Nachweis, der aus dem **Ausbleiben**
   > einer Wirkung besteht, ist nur gültig, wenn der Lauf selbst belegt ist – durch eine Ausgabe,
   > eine Aufzeichnung oder einen zweiten, positiv wirkenden Vorgang im selben Lauf. **Ein
   > Exit-Code allein genügt nicht**; ein nicht-interaktiver Lauf kann bei nötiger Rückfrage ohne
   > Ausgabe mit Erfolgscode enden. Ein Lauf unter aufgehobenen Schutzvorkehrungen des Clients
   > (abgeschaltete Vertrauensprüfung, Modus ohne Rückfragen) belegt **nicht** den Normalbetrieb;
   > das Protokoll weist die Bedingung aus und benennt, was dadurch offen bleibt.

2. **D-23 wird fortgeschrieben**, nicht ersetzt: Der Wirksamkeitsnachweis gilt für Prüfungen;
   für Sitzungsnachweise gilt Nummer 7 des Testkatalogs. Beide sagen dasselbe – **ein Nachweis
   zählt, wenn belegt ist, dass gemessen wurde.**

3. **Zwei Zeilen in Abschnitt 5 des Packs `devin-desktop`** („Bekannte Abweichungen im
   Verhalten"): der stille Abbruch bei nötiger Rückfrage und die Vertrauensschranke im
   nicht-interaktiven Betrieb, jeweils mit der Folge für die in Abschnitt 6 vorgeschriebene
   Prüfung.

4. **Keine Änderung an Skripten.** Der Befund liegt im Verfahren, nicht im Code.

## 3. Was dieser Antrag nicht ändert

- **Die Vertrauensschranke.** Sie ist eine **Verschärfung** des Clients und willkommen. Das
  Framework verlangt nicht, sie im Normalbetrieb abzuschalten; es regelt nur, was ein Nachweis
  wert ist, der sie abgeschaltet hat.
- **Die bestehenden Protokolle.** Sie bleiben, wie sie sind. Abschnitt 4 des AP2-Protokolls weist
  die Bedingungen bereits aus – dieser Antrag macht daraus eine Pflicht statt einer guten
  Gewohnheit (zur Nachschau siehe E4).
- **`AP2-DD-10` und `AP2-DD-11`.** Beide sind behoben und in 0.25.0 positiv nachgewiesen; an
  ihrer Geltung ändert sich nichts.

## 4. Grenze der Zusage

**Die Regel verhindert keinen stillen Abbruch.** Sie entwertet nur den Schluss, den man daraus
zöge. Der Abbruch bleibt eine Eigenschaft des Clients.

**Sie ist `review`-prüfbar, nicht skriptprüfbar.** Wer ein Protokoll schreibt, muss sie anwenden;
kein Werkzeug erzwingt sie. Ein Validator kann nicht sehen, ob eine Zeile „0 Aufrufe" aus einer
Messung oder aus einem Abbruch stammt.

**Der Positivbeleg im selben Lauf ist nicht immer herstellbar.** Ein Lauf, der vor dem ersten
Werkzeugaufruf abbricht, erzeugt gar nichts – dann bleibt nur die Wiederholung in einer
interaktiven Sitzung, so wie G-2 sie geführt hat. Die Regel macht diesen Mehraufwand
verbindlich; billiger wird die Beweisführung dadurch nicht.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Zwei Anträge oder einer für `AP2-DD-13` und `AP2-DD-14`? | **Einer.** Beide Befunde beantworten dieselbe Frage – unter welchen Bedingungen ein Nachweis entstanden ist –, und die Abhilfe ist in beiden Fällen derselbe Absatz | `AP2-DD-14` hat damit keinen eigenen Antrag. Wer die Vertrauensschranke sucht, findet sie unter einem Titel über Nachweise |
| E2 | Regel in den Testkatalog oder in D-23? | **Testkatalog**, D-23 nur fortschreiben | Die Forderung steht an zwei Stellen und muss bei Änderungen an beiden gepflegt werden |
| E3 | Nachweise mit abgeschalteter Vertrauensprüfung weiterhin zulassen? | **Ja**, mit Ausweis im Protokoll. Ohne sie wäre für dieses Pack **kein** technischer Nachweis zu führen gewesen | Die Nachweise gelten dann für eine Umgebung, die vom Normalbetrieb abweicht – und der Normalbetrieb bleibt unbelegt, bis ihn jemand interaktiv prüft |
| E4 | Bestehende Protokolle einmalig auf Abwesenheitsnachweise durchsehen? | **Ja**, einmalig und als Review, nicht als Testfall | Ein Reviewgang durch die bisherigen Protokolle. Findet er einen ungedeckten Abwesenheitsnachweis, wird daraus ein eigener Befund |
| E5 | Den stillen Abbruch dem Hersteller melden? | **Zurückgestellt.** Das Framework führt keinen Herstellerkanal; `FEEDBACK_PROCESS.md` regelt den Weg nach innen | Ein Verhalten, das jede Automatisierung trifft, bleibt unadressiert – es steht in einem Protokoll, das der Hersteller nicht liest |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** |
| Datum | 2026-09-11 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | E1 bis E5 wie vorgelegt: **ein** Antrag für beide Befunde; die Regel steht als Nummer 7 im Testkatalog, D-23 wird nur fortgeschrieben; Nachweise mit abgeschalteter Vertrauensprüfung bleiben zulässig, mit Ausweis im Protokoll; die **einmalige Durchsicht** der bestehenden Protokolle auf ungedeckte Abwesenheitsnachweise wird als Review durchgeführt; die Meldung an den Hersteller bleibt zurückgestellt. Ziel-Release 0.26.0 |
