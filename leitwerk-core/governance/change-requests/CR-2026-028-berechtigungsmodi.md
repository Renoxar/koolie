# Änderungsantrag `CR-2026-028`

| Feld | Inhalt |
|---|---|
| Titel | D-05 verweist für die Modus-Zuordnung auf Matrixzeilen, die zwei der geregelten Modi nicht führen |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-11 |
| Betroffene Artefakte | `clients/devin-desktop/CLIENT_PACK.md` (Zeilen M1–M5), `governance/DECISION_LOG.md` (D-05) |
| Ebene laut Entscheidungsbaum 6 | Client Pack – Vollständigkeit der Abbildung; Fortschreibung eines Decision Records |
| Art | Behebung von `AP2-DD-03` (Schwere: niedrig bis mittel) |
| Dringlichkeit | regulär – die Regel gilt, nur ihre Zuordnung fehlt |

## 1. Anlass und Problem

D-05 regelt **vier** Berechtigungsmodi und sagt, wo ihre clientseitige Entsprechung
steht:

> Der Permission-Modus `Bypass` ist im Framework untersagt; `Smart` und `Accept Edits`
> sind nur über dokumentierte Ausnahme für Kontrollstufe niedrig zulässig; Standard ist
> `Normal`. […] **Die Zuordnung je Client steht in der Fähigkeitsmatrix (Zeilen M1 bis
> M3).**

Die Fähigkeitsmatrix des Packs `devin-desktop` führt in M1 bis M3:

| Zeile | Gegenstand |
|---|---|
| M1 | Standardmodus fragt zurück → Modus `Normal` |
| M2 | Modus ohne Rückfragen ausschließbar → Modus `Bypass` |
| M3 | Freigabe auf die Sitzung begrenzbar → Sitzungsfreigaben – **kein Modus** |

**`Smart` und `Accept Edits` haben keine Zeile.** Der Verweis in D-05 geht damit ins
Leere: Er nennt eine Zuordnung, die es für zwei der vier geregelten Modi nicht gibt.

Der Abgleich vom 11.09.2026 gegen Devin Desktop 3.9.19 (`cli/reference/permissions`)
bestätigt alle vier als existierende Modi und nennt einen **fünften**:

| Modus | Dokumentierte Wirkung | In D-05 | In der Matrix |
|---|---|---|---|
| `Normal` | fragt bei Schreiben und Shell-Befehlen zurück | Standard | M1 |
| `Accept Edits` | genehmigt Dateiänderungen im Workspace automatisch | nur über Ausnahme | **fehlt** |
| `Smart` | genehmigt Workspace-Änderungen automatisch, beurteilt übrige Aktionen nach Sicherheit | nur über Ausnahme | **fehlt** |
| `Bypass` | „All tool calls are auto-approved without prompting" | untersagt | M2 |
| `Autonomous` | mit `--sandbox`; genehmigt Shell-Befehle innerhalb der Sandbox | **fehlt** | nur in Abschnitt 5 erwähnt |

### Warum das zählt

Ein Modus, der **selbst beurteilt**, was sicher ist, ist für ein Framework einschlägig,
dessen tragendes Prinzip lautet, dass der Mensch prüft und freigibt. D-05 hat ihn
deshalb zu Recht geregelt. Was fehlt, ist die Brücke zur Installation: **Ohne Matrixzeile
sagt das Pack nicht, wie der Modus beim Client heißt, wie er eingestellt wird und ob die
Ausnahme überhaupt technisch begrenzbar ist.** Eine Regel ohne Zuordnung ist eine Regel,
die man nicht anwenden kann, ohne sie selbst zu übersetzen – genau die Lage, die die
Abbildungsschicht beseitigen soll (D-12).

`Autonomous` fehlt in D-05 ganz. Das Pack erwähnt ihn in Abschnitt 5 („Sandbox nicht auf
allen Betriebssystemen … der Modus `Autonomous` ist damit dort nicht absicherbar"), also
als Randbemerkung zu einem anderen Thema – nicht als geregelter Modus.

### Der Mechanismus in M2 ist falsch benannt

M2 führt: „`Bypass` ist per D-05 untersagt; eine **technische Sperre** setzt
Admin-Kontrollen der Planstufe voraus (K-05 offen)."

Die Recherche ergibt: **Eine Einstellung, die den Bypass-Modus abschaltet, ist nicht
dokumentiert.** Aufrufbar ist er über `--permission-mode bypass` und
`DEVIN_PERMISSION_MODE=bypass`. Was es gibt, ist etwas anderes und Wirksameres: Die
**Terminal Permissions der Organisationsebene** haben laut Team-Dokumentation „the
highest precedence and cannot be overridden by individual users' local or project
configurations" – sie greifen also **auch dann, wenn der Modus auf Bypass steht**.

Im Ergebnis bleibt die Aussage des Packs richtig (ohne Admin-Kontrollen keine
Durchsetzung), aber sie benennt den falschen Hebel: **Nicht der Modus wird gesperrt,
seine Wirkung wird begrenzt.** Der Unterschied ist praktisch: Wer nach einer
Modus-Sperre sucht, findet keine und schließt daraus, es gebe keine Durchsetzung.

**Anders als bei `claude-code`:** Dort ist die Sperre des Modus selbst dokumentiert
(`permissions.disableBypassPermissionsMode`, AP2-CC-05) und in verwalteten Einstellungen
unüberschreibbar. D-05 führt diesen Beleg bereits. Die beiden Clients unterscheiden sich
an dieser Stelle – und genau das soll eine Fähigkeitsmatrix zeigen.

## 2. Vorgeschlagene Änderung

1. **Zwei Zeilen ergänzen** – für den Modus mit automatischer Übernahme von
   Dateiänderungen und für den selbst beurteilenden Modus –, mit Clientnamen,
   Einstufung und Beleg. Die Zusagenspalte bleibt werkzeugneutral formuliert (D-28).
2. **`Autonomous` in D-05 aufnehmen**, mit Bezug auf die Sandbox-Voraussetzung und den
   Umstand, dass die Sandbox unter Windows nicht verfügbar ist (K-11). Ein Modus, der
   seine Absicherung aus einem Mechanismus bezieht, den es auf der Zielplattform nicht
   gibt, ist dort kein abgesicherter Modus.
3. **M2 im Mechanismus korrigieren:** nicht „technische Sperre des Modus", sondern
   „Begrenzung seiner Wirkung durch unüberschreibbare Berechtigungsregeln der
   Organisationsebene". Der VERIFY-Marker der Zeile wird damit aufgelöst.
4. **Den Verweis in D-05 nachziehen:** nicht „Zeilen M1 bis M3", sondern die Zeilen, die
   die Modi tatsächlich führen.

## 3. Was dieser Antrag nicht ändert

- **Die Regel selbst.** `Bypass` bleibt untersagt, die beiden mittleren Modi bleiben
  ausnahmepflichtig, `Normal` bleibt Standard. Der Antrag ergänzt die Zuordnung, er
  lockert nichts (Verschärfungsprinzip).
- **K-05.** Ob die Planstufe die nötigen Admin-Kontrollen bietet, bleibt offen; belegt
  ist jetzt, welcher Mechanismus zu suchen wäre.
- **`claude-code`.** Dort ist die Lage belegt und unverändert.

## 4. Grenze der Zusage

Die Angaben stammen aus der Herstellerdokumentation, nicht aus einer Installation. Sie
belegen `[DOK]`. **Ob die Organisationsregeln im Bypass-Modus tatsächlich greifen, ist
nicht beobachtet** – und mit einer Einzelplatzinstallation ohne Team-Plan auch nicht
beobachtbar. Die Zeile ist entsprechend als `[TEXTUELL]` zu führen, bis eine Umgebung
mit Admin-Kontrollen zur Verfügung steht.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Zwei Modi als Matrixzeilen aufnehmen? | **Ja.** D-05 regelt sie, und die Matrix ist der Ort der Zuordnung | Die Matrix wächst um zwei Zeilen, die für keine Framework-Zusage stehen, sondern für eine Beschränkung |
| E2 | `Autonomous` in D-05 aufnehmen? | **Ja**, mit Bezug auf K-11 – seine Absicherung fehlt auf der Zielplattform | Eine fünfte Modusregel in einer Entscheidung, die mit vier auskam |
| E3 | M2: Sperre oder Wirkungsbegrenzung? | **Wirkungsbegrenzung.** Eine Modus-Sperre ist bei diesem Client nicht dokumentiert | Die Zusage „ausschließbar" wird schwächer: Der Modus bleibt wählbar, nur folgenlos |
| E4 | Einstufung der neuen und der korrigierten Zeilen? | **`[TEXTUELL]`**, solange keine Umgebung mit Admin-Kontrollen beobachtet wurde | Das Pack weist erneut eine textuelle statt technischer Zusage aus |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** |
| Datum | 2026-09-11 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | E1 bis E4 wie vorgelegt: zwei Matrixzeilen für den Modus mit automatischer Übernahme und den selbst beurteilenden Modus; `Autonomous` wird in D-05 aufgenommen, mit Bezug auf K-11; M2 nennt die **Wirkungsbegrenzung durch Berechtigungsregeln der Organisationsebene** statt einer Modus-Sperre; alle betroffenen Zeilen `[TEXTUELL]`. Ziel-Release 0.26.0 |
| Umsetzung | **mit Release 0.26.0** – Einzelheiten und Nachweise in `leitwerk-core/CHANGELOG.md` |
