# Protokoll: `K-77` – die Zurechenbarkeit über drei Bündel, und der Wächter, der mit dem Schnittmuster prüft

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-19 |
| Release | `0.75.0` |
| Änderungsantrag | `CR-2026-102` |
| Art | Auswertung vorhandener Meßbelege und ein Werkzeugnachweis – **keine Sitzung, kein Kontingent, kein Modelllauf** |
| Gegenstand | `K-77`: Wie schneidet man einen Kontrolllauf für eine Zelle, deren geprüfte Schranke im Skill steht? |
| Quellen | `2026-09-19-testblaetter-buendel-1.md`, `-buendel-2.md`, `-buendel-3.md`; `devpacks/leitwerk-erhebungen-2026-09-19-b3/skripte/k-bauen-b3.py`, `k77-waechter-nachweis.py` |
| Ergebnis | 🔴 **Die Prämisse von D-203 hält nicht.** Über 47 Zellen sind **27** zurechenbar, **15 davon über Regelschicht-Zuschnitte** – mehr als über `ohneskill` (12). 🔴 **Und der Grund ist gefunden: Der Wächter des Zuschnitts prüft mit dem Schnittmuster.** Gemessen über acht Klassen: **vier lassen den Gegenstand stehen, vier nicht – und nur unter den vier vollständigen ist eine Zelle zurechenbar** (D-205) |

---

## 1. Warum dieser Durchgang gefahren wurde

`K-77` fragt, wie ein Kontrolllauf für eine Zelle zu schneiden ist, deren geprüfte
Schranke in der `SKILL.md` steht. Die Frage stammt aus D-203, und D-203 stützt sich auf
**eine** Messung – Bündel 3 – und auf **einen Satz über Bündel 2**:

> *„Das ist kein Zufall dieses Bündels: In Bündel 2 war jede Zelle mit `ohneskill`
> zurechenbar und keine mit einem Regelschicht-Zuschnitt scharf."*

🔴 **Vor der Entscheidung ist dieser Satz gegen die Ergebnistabelle von Bündel 2 gehalten
worden. Er hält nicht.** Derselbe Griff wie bei D-170 und D-197: **Wer einen vertagten
Punkt entscheidet, liest zuerst dessen eigenen Beleg nach.**

## 2. Die Auszählung über drei Bündel

**Gezählt wurde aus den Ergebnistabellen der drei Meßprotokolle**, nicht aus ihren
Zusammenfassungen – die Zusammenfassung von Bündel 3 war am Vortag bereits als falsch
nachgewiesen worden (`CR-2026-101`).

| Bündel | Skills | Zellen | 🟢 zurechenbar | davon `ohneskill` | davon **Regelschicht** | 🔴 halb | 🔴 nicht |
|---|---|---|---|---|---|---|---|
| **1** (`0.68.0`) | `fw-repo-analyze`, `fw-code-explain`, `fw-change-analyze` | 11 | **6** | 4 | **2** | 2 | 3 |
| **2** (`0.71.0`) | `fw-plan`, `fw-error-analyze`, `fw-bugfix-prepare` | 18 | **17** | 5 | **12** | 1 | 0 |
| **3** (`0.74.0`) | `fw-change-small`, `fw-refactor`, `fw-tests` | 18 | **4** | 3 | **1** | 2 | 12 |
| **Summe** | | **47** | **27** | **12** | **15** | 5 | 15 |

⚠️ **Die Zahlen von Bündel 1 tragen ein Ermessen und sind deshalb aufgezählt:** Jenes
Protokoll führt die Zurechenbarkeit im Fließtext seiner Kontrollspalte statt in einer
eigenen Spalte. Zurechenbar sind `SK-001-N03` (`kn03`, Regelschicht), `SK-002-P01`,
`SK-002-P02`, `SK-003-P01`, `SK-003-P02` (je *„ohne Skill"*) und `SK-003-N02`
(*„ohne die Datenschutzregeln"*, Regelschicht); halb `SK-002-N02` und `SK-002-N03`.
**Bündel 2 und 3 führen die Spalte und sind ausgezählt, nicht ausgelegt.**

🔴 **Das Ergebnis steht gegen D-203 in beiden Hälften:**

- **15 der 27 zurechenbaren Zellen sind über einen Regelschicht-Zuschnitt zurechenbar** –
  mehr als über `ohneskill` (12).
- **Und einer davon ist ausdrücklich *scharf*:** `SK-004-N01` in Bündel 2, Zuschnitt
  `kn03` – *„der Kontrolllauf legt die Stufe selbst fest und schreibt den vollen Plan"*.
  Der Satz, in Bündel 2 sei *„keine mit einem Regelschicht-Zuschnitt scharf"* gewesen, ist
  damit an einer einzelnen Zeile desselben Protokolls widerlegt.

## 3. Was Bündel 3 von Bündel 2 unterscheidet – nicht die Schicht

**Nicht die Schicht, in der die Schranke steht.** Sonst hätte Bündel 2 dasselbe Ergebnis
liefern müssen: Auch dort wird die `SKILL.md` beim Aufruf über den Schrägstrich ganz in
die Sitzung eingefügt (D-187), auch dort steht in Abschnitt 4 jedes Skills eine Grenze.

**Sondern die Reichweite der Zuschnitte.** Bündel 3 hat die acht Klassen von Bündel 2 um
**fünf neue** ergänzt (`plan`, `test`, `befund`, `testnachweis`, `abw`), und die Bilanz
trennt sich an dieser Linie:

| Klassen | Zellen in Bündel 3 | zurechenbar | halb |
|---|---|---|---|
| die **acht alten** (`n03`, `sc1`, `inj`, `injk3`, `k3`, `halt`, `konf`, `risiko`) | 6 | 1 | 1 |
| die **fünf neuen** (`plan`, `test`, `befund`, `testnachweis`, `abw`) | 9 | **0** | 1 |
| `ohneskill` | 3 | **3** | 0 |

**Die acht alten Klassen schneiden Gegenstände, die das Regelwerk unabhängig vom Skill
trägt** – Datenschutz, Injektion, Scope, Risiko, Halt, Konfiguration, Rückfragepflicht.
**Die fünf neuen schneiden Gegenstände, die zugleich Arbeitsschritte der Skills sind:**
Planpflicht, Testnachweis, Befundmeldung, Abweichungsmeldung. Sie stehen in **beiden**
Schichten – und der Zuschnitt hat nur die eine erwischt.

🟢 **Die Gegenprobe steht daneben:** Der Zuschnitt `k3` **hat** getrennt, und zwar scharf –
`ksk005n05` schreibt den personenbezogen strukturierten Datensatz, den der Hauptlauf
verweigert. Seine Marken treffen **zehn Zeilen in
`framework/skills/fw-change-small/SKILL.md`**, darunter die Ausschlußzeile in Abschnitt 4
und die Rückfragenregel.

➡️ **Nicht *Regelschicht gegen Skill* ist die Trennlinie, sondern die REICHWEITE des
Zuschnitts.**

## 4. 🔴 Der Befund: der Wächter prüft mit dem Schnittmuster

`k-bauen-b3.py` schneidet nach den `ZEILE`-Mustern einer Klasse und prüft danach mit ihren
`MARKEN`. 🔴 **Die `MARKEN` sind je Klasse eine Teilmenge der `ZEILE`-Muster** – in allen
acht geprüften Klassen, ohne Ausnahme. Der Wächter sucht also **weniger**, als der Schnitt
entfernt, und kann per Konstruktion nichts finden, was das Schnittmuster nicht kannte.
**Das ist *die Null durch Konstruktion* (0.59.1), angewandt auf den Wächter des
Zuschnitts.**

**Gemessen am 2026-09-19 gegen `devpacks/test-devin-framework`** (172 Träger der
Bereichsliste). **A** = das Schnittmuster trifft, **B** = der heutige Wächter trifft,
**C \ A** = was der Schnitt **stehen läßt** und der Wächter **nicht meldet**:

| Klasse | A | B | C \ A | Zuschnitt |
|---|---|---|---|---|
| `sc1` | 258 | 224 | **23** | 🔴 unvollständig |
| `plan` | 211 | 131 | **17** | 🔴 unvollständig |
| `test` | 187 | 100 | **15** | 🔴 unvollständig |
| `befund` | 86 | 74 | **14** | 🔴 unvollständig |
| `k3` | 528 | 337 | **0** | 🟢 vollständig |
| `inj` | 100 | 95 | **0** | 🟢 vollständig |
| `testnachweis` | 103 | 81 | **0** | 🟢 vollständig |
| `abw` | 247 | 97 | **0** | 🟢 vollständig |

🔴 **Und jetzt fällt die Bilanz von Bündel 3 an der richtigen Linie auseinander:**

| Zuschnitt | Zellen | zurechenbar | halb | nicht |
|---|---|---|---|---|
| **vollständig** (`k3`, `inj`, `testnachweis`, `abw`) | 5 | **1** (scharf) | 1 | 3 |
| **unvollständig** (`sc1`, `plan`, `test`, `befund`) | 9 | **0** | 0 | 9 |
| `ohneskill` | 3 | **3** | 0 | 0 |
| ⚠️ **ungeprüft** (`injk3`, kein Stammmuster) | 1 | 0 | 1 | 0 |
| **Summe** | **18** | **4** | **2** | **12** |

⚠️ **Die Summenzeile steht hier, weil der Durchgang vor dem Commit sie gebraucht hat:**
Die Tabelle deckte im ersten Entwurf **17 der 18 Zellen** – `SK-007-N05` mit dem
Kombinationszuschnitt `injk3` fiel heraus, weil für ihn kein Stammmuster vorliegt.
**Neunzehnter Fall in Folge**, und diesmal an der eigenen Bilanz.

🟢 **Die einzige Regelschicht-Klasse, die getrennt hat, ist auch die einzige mit null
Restfundstellen.** Von neun Zellen mit unvollständigem Zuschnitt ist keine einzige
zurechenbar – und das ist kein Befund über das Framework, sondern über den Meßaufbau.

⚠️ **Die 17 Restfundstellen von `plan` sind einzeln gelesen worden, und keine ist eine
Fehlmeldung:** dreizehnmal der Dativ `bestätigtem Plan`, einmal *„Plan-Review"*, dreimal
`dokumentierten Freigabe`. **Vier stehen in einer `SKILL.md`** (`fw-change-small`,
`fw-refactor` dreimal) – also genau in der Schicht, um die `K-77` streitet –, **und eine
in einem Flußdiagramm-Knoten** (`decision-trees/02-may-ai-do-task.md`), die Bauform von
0.66.0.

⚠️ **Gemessen wurde am heutigen Stand des Übungsrepositoriums, nicht in den Meßbäumen von
Bündel 3** – die sind gelöscht (`CR-2026-101`). **Für `plan` deckt sich der Befund
unabhängig:** Das Meßprotokoll nennt sieben Überlebende, aus den Kontrollläufen erfahren.
**Und die Unvollständigkeit ist ohnehin eine Eigenschaft des MUSTERS, nicht des Baums:**
Ein Muster, das den Dativ nicht kennt, kennt ihn in jedem Baum nicht.

🔴 **Die Schwäche war benannt und ist trotzdem als Beleg verwendet worden.** Der
Kopfkommentar desselben Skripts sagt seit der Erhebung `s4`:

> *„Ein grüner Wächter belegt NICHT, daß die Schranke weg ist: Die Zeilen, die einen
> Begriff AUSMACHEN, überleben eine Suche nach der Zeile, die ihn NENNT."*

**Der Satz steht dort, seit es das Skript gibt. Die Protokolle von drei Bündeln führen den
grünen Wächter trotzdem als Beleg des Zuschnitts.** Das ist die schärfere Verwandte der
*Zusage, die mehr verspricht als ihr Mechanismus hält*: Hier ist die Grenze
**aufgeschrieben**, und niemand hat sie gegen ihre Verwendung gehalten.

## 5. Warum Weg (2) verworfen ist

Weg (2) – die Zurechenbarkeit bei Skillzellen ausdrücklich **nicht** zu erheben – spart je
Zelle einen Lauf, bei Bündel 4 also rund **21 USD** (19 × 1,10 USD, `CR-2026-101`).

🔴 **Er ist durch den eigenen Bestand widerlegt, und zwar mit 27 zu 0:** Hätte er seit
Bündel 1 gegolten, wäre **keine** der 27 zurechenbaren Zellen erhoben worden – darunter
die siebzehn von Bündel 2 und die schärfste Trennung von Bündel 3. **Eine Ersparnis, die
den Gegenstand mit wegwirft, ist keine Ersparnis.**

**Und die Ersparnis ist kleiner, als sie aussieht:** Der Kontrolllauf ist nicht der teure
Teil eines Meßtags. 48 Läufe kosteten 52,63 USD; der Aufbau kostete zwei Tage.

## 6. Die Entscheidung (D-205) und ihr Wirkungsnachweis am Werkzeug

**Der Zuschnitt folgt der Schranke, nicht der Schicht.** Drei Sätze für jeden künftigen
Meßaufbau:

1. **Ein Zuschnitt erfaßt seine Schranke in allen Schichten** – Quelle, Laufzeitfassung,
   Hook (D-176) **und `SKILL.md`** – **und in allen Formen**: Beugungsformen (D-203),
   Vorzeichen (0.66.0), Ausfüllschlitze (0.61.0), Diagrammknoten.
2. **Der Wächter benutzt ein anderes, weiteres Muster als der Schnitt.** Er sucht den
   **Gegenstand**, nicht die geschnittene Formulierung. Ein Wächter, der enger ist als der
   Schnitt, bestätigt den Schnitt und nicht die Abwesenheit der Schranke.
3. **Meldet er Restfundstellen, ist der Zuschnitt unfertig.** Läßt sich der Rest nicht
   entfernen, trägt die Zelle **`Zurechenbarkeit nicht erhoben` mit Grund – nicht
   `nicht zurechenbar`**. Ein *nicht zurechenbar* behauptet, das Framework wirke nicht;
   *nicht erhoben* sagt, daß der Aufbau es nicht trennen konnte.

🟢 **Umgesetzt in `k-bauen-b3.py`** (außerhalb des Repositoriums):

- Ein **Stammwächter** prüft nach dem Marken-Wächter mit den Stammmustern der Klasse; er
  bricht ab und **löscht den Baum**, wie der erste.
- Für eine Klasse **ohne** Stammmuster bricht das Skript **vor** dem Kopieren ab. Wer
  trotzdem bauen will, setzt `--ohne-stammwaechter` – dann ist es eine **ausgewiesene
  Abweichung des Zuschnitts und gehört ins Protokoll**, wie die `ask`/`allow`-Abweichung
  von Prüfung 60.
- **Der Nachweis ist ein Paar am selben Baum:** Zuschnitt `plan` gegen
  `devpacks/test-devin-framework` – **Wächter 1 (Marken) meldet keine Restfundstelle,
  Wächter 2 (Stamm) meldet 17 und bricht ab.** Derselbe Zuschnitt, derselbe Baum, zwei
  Ergebnisse.
- ⚠️ **Der erste Entwurf des Stammmusters für `plan` meldete 307 Zeilen** – ein bloßes
  `Freigabe\w*` traf jede *„Freigabeinstanz"*. Eingeengt auf den Gegenstand und **jede
  Meldung gelesen**; die Lehre von 0.63.0 hat beim ersten Lauf zugeschlagen.
- **Stammmuster liegen jetzt für acht der dreizehn Klassen vor.** Die übrigen fünf
  (`n03`, `injk3`, `halt`, `konf`, `risiko`) brechen ab, bis eines formuliert ist.

### Die zwölf Zellen von Bündel 3, die `nicht zurechenbar` trugen

**Neun gehen auf `Zurechenbarkeit nicht erhoben`** – ihr Zuschnitt ist nachweislich
unvollständig: `SK-005-N01`, `SK-005-N02`, `SK-005-N03` (`fw-change-small`),
`SK-007-N02`, `SK-007-N03`, `SK-007-N04`, `SK-007-P02` (`fw-refactor`), `SK-006-N01`,
`SK-006-N02` (`fw-tests`).

🟢 **Drei bleiben `nicht zurechenbar` – und sind es jetzt zum ersten Mal belegt:**
`SK-005-N04` (`inj`), `SK-007-N01` (`testnachweis`), `SK-006-N03` (`k3`). Bei ihnen meldet
der Stammwächter **null** Restfundstellen; das erwartete Verhalten tritt dort wirklich
auch ohne die Regel ein. **Das ist D-175 in seiner belegten Form** – und es sind die
ersten drei Zellen des Projekts, bei denen das nicht nur behauptet ist.

🔴 **Der Ergebnisstatus bleibt unberührt.** Alle achtzehn Zellen sind `bestanden`; D-115
sagt seit jeher, daß die Zurechenbarkeit nicht der Ergebnisstatus ist. **Kriterium 2
bewegt sich nicht.**

## 7. Was offen bleibt

- ⚠️ **Fünf Klassen ohne Stammmuster** (`n03`, `injk3`, `halt`, `konf`, `risiko`) – der
  erste Handgriff beim Aufbau von Bündel 4, das ohnehin eigene Klassen braucht.
- ⚠️ **Die neun Zellen mit unvollständigem Zuschnitt werden nicht neu gefahren.** Neun
  Läufe (rund 10 USD) bewegen keine Zahl von D-11. **Wer sie fährt, fährt sie mit
  Bündel 4 zusammen**, wo der Aufbau ohnehin steht.
- ⚠️ **`K-76`** ist unberührt: Der Rücknahmeschritt von `fw-refactor` bleibt unbelegt.
- ⚠️ **Das Vokabular der Zurechenbarkeitsangabe wird von keiner Prüfung durchgesetzt.**
  **Ausgezählt über alle Testblätter: acht verschiedene Formeln in 42 Zellen** – von
  `Zurechenbar` (17) über `Nur zur Hälfte zurechenbar` (4) und `Zurechenbar, und zwar
  genau zur Hälfte` (1) bis zu einer, die gar keine Formel ist, sondern ein Satzteil
  (*„Die Einstufung ist zurechenbar, die Verweigerung nicht"*). **Erwogen und nicht
  gebaut** (`CR-2026-102` E4); derselbe Prüfkandidat wie beim Statusvokabular des
  Decision Logs (D-101).
- ⚠️ **Eine Prüfung, die eine Aussage über ein Bündel gegen die Ergebnistabelle seines
  Protokolls hält, ist erwogen und nicht gebaut.** Der Befund ist innerhalb von zwei Tagen
  zweimal aufgetreten; beim dritten Mal wird er Prüfgegenstand.
