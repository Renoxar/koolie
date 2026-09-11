# Änderungsantrag `CR-2026-037`

| Feld | Inhalt |
|---|---|
| Titel | Das meldende Hook-Skript des Kerns nennt die Laufzeitschicht eines Clients – die Semantikabbildung erreicht nur den durchsetzenden Hook |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-11 |
| Betroffene Artefakte | `tests/scripts/hook-overlay-status.py` (Zeilen 8, 19, 21), `clientmap.py` (Hook-Kommando), `tests/scripts/validate-framework.py` (neue Prüfung 21), `governance/DECISION_LOG.md` (Fortschreibung D-30) |
| Ebene laut Entscheidungsbaum 6 | Kern – Laufzeitskript und Semantikabbildung; betrifft **beide** Client Packs |
| Art | Behebung eines Befundes aus der Antragsarbeit zu `AP2-DD-15`/`-16` (Sitzung 2026-09-11); **keine AP2-Kennung** |
| Dringlichkeit | regulär – H3 ist ohnehin unbeobachtet (siehe Abschnitt 4) |

## 1. Anlass und Problem

`hook-overlay-status.py` meldet beim Sitzungsstart den Overlay-Status (Zusage **H3**). Das Skript
liegt im Kern, der seit D-15 werkzeugneutral ist. Es nennt an drei Stellen einen Client:

```python
# Zeile 8 (Docstring): Liest project-overlay/OVERLAY.md und .devin/rules/20-project-overlay.md
root = os.environ.get("DEVIN_PROJECT_DIR", os.getcwd())          # Zeile 19
candidates = [os.path.join(root, ".devin", "rules", "20-project-overlay.md"), …]   # Zeile 21
```

Das Manifest von `claude-code` führt für dieselbe Rolle `CLAUDE_PROJECT_DIR`
(`hook_project_dir_var`). Das Kommando wird korrekt gerendert – der Pfad zum Skript steht in der
Variablen dieses Clients –, **aber im Skript ist sie unbekannt**. Dort greift der Rückfall auf
`os.getcwd()`, und der erste Kandidat (`.devin/rules/…`) kann bei diesem Client nie zutreffen.

**Folge bei `claude-code`:** Der Status wird allein aus `project-overlay/OVERLAY.md` hergeleitet,
und das nur, wenn das Arbeitsverzeichnis beim Sitzungsstart das Projektverzeichnis ist – **für
keinen der beiden Clients belegt**. Trifft es nicht zu, meldet das Skript `unbekannt`; nach
Abschnitt 3 der Wurzel-Anweisungsdatei soll der KI-Client dann nur lesend arbeiten. Die Meldung
wäre also nicht bloß ungenau, sie hätte eine Wirkung.

### Warum das den Kern betrifft

D-30 hat entschieden:

> Eine Semantikabbildung gilt **auch für die Skripte, die die Zusage durchsetzen** – nicht nur
> für die erzeugte Konfiguration.

`hook-check-secrets.py` löst das ein: Es liest die Werkzeugnamen aus `hook_tools` **aller** Packs.
Das zweite Hook-Skript ist bei dieser Entscheidung nie betrachtet worden – **weil es nichts
durchsetzt, sondern meldet.** Die Begründung von D-30 trägt aber genauso weit: Ein Skript, das in
einer Sitzung läuft, darf die Laufzeitschicht nicht raten.

### Warum keine Prüfung es sieht

| Prüfung | Warum sie schweigt |
|---|---|
| 14 (kein Client als Akteur) | Ihr Muster ist `\bDevin\b`, **zeichengetreu**. `DEVIN_PROJECT_DIR` trifft es nicht |
| 12 (Nennung einer nicht installierten Laufzeitschicht) | Sie warnt nur, wenn die Laufzeitschicht **fehlt**. In diesem Repositorium liegt eine `devin-desktop`-Testinstallation – der Pfad existiert |

Beide Blindstellen sind strukturell, nicht zufällig: Die eine unterscheidet Produktname von
Akteursnennung und muss dafür Groß- und Kleinschreibung ernst nehmen; die andere prüft
Verweisziele, nicht Neutralität. Eine Ausweitung von Prüfung 14 auf Kleinschreibung wäre teuer
und falsch – `.devin/` steht in Glossar, Registrierungstabelle und der Rückfallabbildung des
Validators an Stellen, an denen es **hingehört**.

## 2. Vorgeschlagene Änderung

1. **Projektverzeichnis und Regelablage kommen als Argumente**, nicht aus der Umgebung. Die
   Abbildung setzt sie aus `hook_project_dir_var` und `runtime_placeholders["<RULES_DIR>"]`:

   ```text
   python "$PROJEKTVERZEICHNIS/<CORE_DIR>/tests/scripts/hook-overlay-status.py" "$PROJEKTVERZEICHNIS" "<RULES_DIR>"
   ```

   `PROJEKTVERZEICHNIS` steht dabei für die Variable, die das Manifest des Packs unter
   `hook_project_dir_var` führt – der Kern nennt sie nicht.

   Das ist die Begründung aus **D-31**, angewandt auf einen zweiten Fall: Der Wert steht im
   Kommando, das der Client ohnehin ausführt, statt in einer Umgebung, von der für kein Pack
   belegt ist, dass sie den Hook-Prozess erreicht.

2. **Rückfall ohne Argumente:** Arbeitsverzeichnis und ausschließlich `project-overlay/OVERLAY.md`
   – werkzeugneutral, mit Kommentar, dass dies der Notweg ist und nicht der vorgesehene Pfad.

3. **Prüfung 21:** Ein Hook-Skript des Frameworks nennt **keine** clientgebundene
   Umgebungsvariable und keinen Laufzeitpfad eines Packs. Geltungsbereich ausdrücklich die
   Hook-Skripte – nicht der Validator, der eine dokumentierte Rückfallabbildung führt
   (`validate-framework.py`, Kommentar bei Zeile 235).

   Sonde nach D-23: In einer Kopie wird eine solche Variable eingesetzt – die Prüfung meldet sie.
   Gegenprobe: `hook-check-secrets.py`, das seine Namen aus den Manifesten liest, bleibt
   unbeanstandet.

4. **D-30 wird fortgeschrieben:** Die Semantikabbildung gilt für **jedes** Skript, das in einer
   Sitzung läuft – auch für das meldende. Ein neuer Record ist nicht nötig; die Entscheidung ist
   dieselbe, nur ihr Geltungsbereich war zu eng beschrieben.

## 3. Was dieser Antrag nicht ändert

- **Was gemeldet wird.** Der Overlay-Status und seine drei Werte (`aktiv`, `inaktiv`,
  `unbekannt`) bleiben unverändert; nur die Herkunft der Pfade ändert sich.
- **Der durchsetzende Hook.** `hook-check-secrets.py` ist seit D-30 in Ordnung und wird nicht
  angefasst.
- **Die Rückfallabbildung des Validators.** Sie bleibt zulässig und ausdrücklich außerhalb von
  Prüfung 21 (siehe E3).

## 4. Grenze der Zusage

**Die Änderung macht die Meldung richtig, nicht beobachtet.** H3 ist bei `devin-desktop`
unbeobachtet – das Protokoll führt die Zeile so, und der Hook lief bis 0.24.0 ohnehin nicht.
**Dieser Befund hat sich im Betrieb nie gezeigt, weil die Zusage, an der er hängt, selbst nie
gezeigt wurde.** Er ist durch Lesen gefunden, nicht durch Messen.

**Ob `os.getcwd()` beim Sitzungsstart das Projektverzeichnis ist, bleibt unbelegt.** Nach dieser
Änderung nur noch als Notweg – vorher war es der Normalfall für eines von zwei Packs.

**Prüfung 21 prüft Skripte, nicht Wirkung.** Ein Hook-Skript, das seine Pfade sauber übergeben
bekommt und trotzdem den falschen Status meldet, fällt ihr nicht auf. Dafür braucht es einen
Nachweis an einer Installation – denselben, der für H3 aussteht.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Argumente oder Umgebungsvariable? | **Argumente**, mit der Begründung aus D-31 | Das Hook-Kommando wird länger und trägt zwei Werte mehr, die bei jeder Abbildungsänderung mitzupflegen sind |
| E2 | Regelablage als zweites Argument oder Kandidat streichen? | **Als Argument.** Streichen würde ändern, *was* gemessen wird: Die gerenderte Regeldatei trägt den Status ebenso wie das Overlay | Ein Argument mehr. Wer die Regelablage umbenennt, muss an die Abbildung denken – der Validator meldet es nicht |
| E3 | Geltungsbereich von Prüfung 21: Hook-Skripte oder alle Skripte des Kerns? | **Hook-Skripte.** Der Validator führt eine dokumentierte Rückfallabbildung auf `.devin/`, die er braucht, wenn kein Pack gefunden wird | Die Rückfallabbildung bleibt ungeprüft. Sie ist begründet, aber sie ist auch eine Client-Bindung im Kern |
| E4 | D-30 fortschreiben oder neuer Decision Record? | **Fortschreiben**, mit Datum und Verweis auf diesen Antrag | Ein Record, der zwei Sachverhalte trägt; die Historie steht im Änderungsverlauf, nicht in zwei Records |
| E5 | H3 im selben Zug nachweisen? | **Nein, getrennt.** Der Nachweis gehört zu AP2 und braucht eine Sitzung mit Aufzeichnung, nicht diesen Antrag | Die Zusage bleibt bis dahin unbeobachtet – jetzt mit richtigen Pfaden, aber weiterhin ohne Beleg |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | `<TBD: angenommen / abgelehnt / mit Auflagen>` |
| Datum | `<TBD>` |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | `<TBD: E1 bis E5 einzeln entscheiden>` |
