# Gegenprüfung: die Berechtigungsdatei nach der Installation – eine Erweiterung, die es nicht gibt, und ein Korb, den niemand nachzählt

| Feld | Wert |
|---|---|
| Gegenstand | Zwei Framework-Lücken, die der Pilot sichtbar gemacht hat: (1) **Ein Overlay kann keinen zusätzlichen Befehl freigeben** – die Regelmenge hat für Befehle genau drei Platzhalter, `clientmap.py` kennt keine Erweiterungsquelle, und der Kommentarkopf der erzeugten Datei sagt trotzdem „Ebene 3 + Overlay-Erweiterungen"; (2) **der `ask`-Korb wird von nichts geprüft** – eine von Hand ergänzte Zeile wird weder überschrieben noch gemeldet |
| Anlass | Beide stehen als Kandidat 1 und 2 in der Übergabe und sind der dritte Ablehnungsgrund von `CR-OTP-G-001` („Es gibt keine geprüfte Änderungsschicht für diese Datei"). Nach D-23 gehört ein Befund vor der Umsetzung gegengeprüft, auch wenn er aus dem eigenen Haus stammt |
| Datum | 2026-09-13 |
| Framework-Version | 0.38.0 (Auscheckstand `07c8183`, Arbeitsbaum sauber, Validator 0/0) |
| Prüfmethode | **Zwölf Messungen an einer frischen Installation, keine Codelektüre allein.** Eine Testinstallation `claude-code` in einem leeren Verzeichnis; je Messung ein Eingriff in `.claude/settings.json`, danach der ausgelieferte Validator, danach Rücknahme des Eingriffs und Abgleich mit dem Ausgangstext. Zwei der zwölf sind **Gegenproben** – Eingriffe, die der Validator fangen *muss*; ohne sie wäre „0 Fehler" kein Messwert, sondern womöglich ein nicht gestarteter Lauf |
| Umgebung | Windows 11, Python 3.14.4, NTFS; Testinstallation im Scratchpad, `leitwerk-core` hineinkopiert (sonst zeigen die Hook-Kommandos ins Leere) |
| Ergebnis | **Beide Befunde bestätigen sich, und beide sind erheblich größer als die Übergabe sagt.** Nicht nur der `ask`-Korb ist ungeprüft, sondern **41 der 54 deny-Regeln** ebenso. Und die Erweiterungslücke ist nicht nur ein falscher Kommentarkopf: **Die Vorlage des Overlays fordert in ihrer eigenen Tabelle vier Befehlszeilen an, die den Weg in die Datei nicht haben – unter einer Spaltenüberschrift, die ihn behauptet** |

## 0. Der Zusammenhang in einem Satz

**Die Berechtigungsdatei wird einmal erzeugt und danach von niemandem mehr gelesen – außer an
dreizehn Zeilen.** Alles andere an ihr ist ab dem Augenblick der Installation ungeprüfter
Projektbesitz: ergänzbar, kürzbar, verengbar, ohne dass irgendein Lauf davon Notiz nimmt. Der
Kommentarkopf der Datei nennt sie „Ebene 3 + Overlay-Erweiterungen"; **es gibt weder die
Erweiterung noch die Prüfung.**

## 1. Der Aufbau der Messung

Eine frische Installation, damit die Messung nicht an der lokalen Testinstallation des
Repositoriums hängt:

```
python leitwerk-core/install.py --client claude-code --root <leeres Verzeichnis>
cp -r leitwerk-core <root>/leitwerk-core
printf '# Testprojekt\n' > <root>/README.md      # README.md ist Pflichtpfad
```

**Ausgangslage: 0 Fehler, 1 Warnung.** Die Warnung sind die bekannten zehn `.devin/`-Pfadangaben
aus `docs/ROADMAP.md` und `build/doc/` – derselbe Posten, den der Pilot seit seinem ersten Lauf
meldet. Sie ist für diese Messung ohne Belang und bleibt in jeder Zeile unten gleich.

Die erzeugte Datei trägt:

| Korb | Regeln | davon mit Projektplatzhalter |
|---|---|---|
| `deny` | 54 | 4 (`Read(<EXCLUDED_PATHS>)`, `Edit(<CI_CONFIG_PATHS>)`, `Edit(<QUALITY_GATE_CONFIG_PATHS>)`, `Edit(<EXCLUDED_PATHS>)`) |
| `ask` | 5 | 3 (`Bash(<BUILD_COMMAND>)`, `Bash(<TEST_COMMAND>)`, `Bash(<LINT_COMMAND>)`) |
| `allow` | 6 | 0 |
| `_core_rules_integrity.deny_must_contain` | **13** | 0 |

**Dreizehn von fünfundsechzig.** Das ist der Anteil, den der Validator kennt.

## 2. Befund 1: Der `ask`-Korb wird von nichts geprüft – und der `deny`-Korb auch nicht

### 2.1 Was behauptet wird

Aus der Übergabe, Kandidat 2: *„Eine von Hand ergänzte `ask`-Zeile wird weder überschrieben
(`--update` fasst die Datei nicht an) noch gemeldet (der Validator prüft nur
`deny_must_contain`, also nur was fehlt)."*

### 2.2 Was gemessen dabei herauskommt

Jede Zeile: Eingriff in `.claude/settings.json`, Validator, Rücknahme.

| Nr. | Eingriff | Validator | Meldung zur Datei |
|---|---|---|---|
| **M1** | `ask` um `Bash(docker run --rm --network none:*)` ergänzt – die Zeile, die `CR-OTP-G-001` wollte | 0 Fehler | keine |
| **M2** | `allow` um `Bash(docker run:*)` ergänzt | 0 Fehler | keine |
| **M3** | eine **Nicht**-Kernregel aus `deny` gelöscht (`Bash(curl:*)`) | 0 Fehler | keine |
| **M4** | **alle 41** Nicht-Kernregeln aus `deny` gelöscht | 0 Fehler | keine |
| **M5** | eine Nicht-Kernregel **verengt**: `Bash(kubectl:*)` → `Bash(kubectl delete:*)` | 0 Fehler | keine |
| **M6** | Platzhalter mit Präfixzeichen gefüllt: `Bash(<TEST_COMMAND>)` → `Bash(mvn -B test:*)` | 0 Fehler | keine |
| **M7** | Platzhalter gar nicht gefüllt (Auslieferungszustand) | 0 Fehler | keine |
| **M8** | `ask`-Korb geleert – `Edit(**)` und `mcp__*` verschwinden mit | 0 Fehler | keine |
| **M9** | *Gegenprobe:* Kernregel `Bash(sudo:*)` aus `deny` gelöscht | **1 Fehler** | `Kernregel fehlt in deny: Bash(sudo:*)` |
| **M10** | *Gegenprobe:* Kernregel `Bash(sudo:*)` in `allow` gesetzt | **2 Fehler** | `Kernverbot steht in allow` · `unzulässige allow-Regel` |

**M9 und M10 sind der Grund, warum die acht Nullen darüber Messwerte sind.** Ein Validator, der
gar nicht startet, meldet auch null – das war am 13.09. schon einmal ein Absturz statt eines
Ergebnisses. Hier greift er, sobald sein Gegenstand betroffen ist.

**M7 ist kein Befund.** Der Auslieferungszustand mit offenen Platzhaltern soll im Normallauf
durchgehen; gefangen wird er dort, wo er gefangen gehört:

```
--strict-overlay      → FEHLER  .claude/settings.json: enthält noch Platzhalter (strict-overlay)
--check-overlay-ready → FEHLER  .claude/settings.json: enthält noch Platzhalter (check-overlay-ready)
```

Das ist richtig so und bleibt unberührt.

### 2.3 Die Übergabe hat zu klein gezählt

Kandidat 2 nennt den `ask`-Korb. **Gemessen ist es der ganze Rest der Datei:**

- **M4 ist die schwerste Zeile der Tabelle.** Ein Projekt kann `curl`, `wget`, `ssh`, `scp`,
  `kubectl`, `helm`, `terraform`, `npm publish`, `docker push`, `git rebase`, `git tag`,
  `git clean`, `git remote`, `chmod`, sämtliche Lockfile-Sperren und zehn der fünfzehn
  Secret-Lesesperren streichen – und der Lauf bleibt grün. Übrig bleiben die dreizehn
  Kernregeln. **Das ist keine Lücke im `ask`-Korb, das ist eine Lücke in der Datei.**
- **M5 ist die stillste.** Eine verengte Regel *sieht aus* wie eine Regel. `Bash(kubectl delete:*)`
  steht im `deny`-Korb, sperrt aber `kubectl apply` nicht mehr. Wer die Datei liest, zählt eine
  Sperre und hat keine.
- **M6 ist der Fall des Piloten.** `clientmap._befehl` hängt bei einem offenen Projektplatzhalter
  **ausdrücklich kein** Präfixzeichen an, mit Begründung im Code: *„Der Overlay Owner trägt den
  vollständigen Befehl ein; ein angehängtes Präfixzeichen würde ihn verfälschen."* Am Piloten
  steht `Bash(mvn -B test:*)`. **Das Zeichen, das die Abbildung bewusst weglässt, hat jemand von
  Hand nachgetragen** – und damit aus der Freigabe eines Befehls die Freigabe einer Befehlsfamilie
  gemacht.

### 2.4 `install.py` greift es auch nicht auf

Gemessen an derselben Installation mit **drei** gleichzeitigen Eingriffen (M1 + M2 + M3):

| Lauf | Exit | Datei danach | Ausgabe zur Datei |
|---|---|---|---|
| `install.py --check` | 0 | unberührt | **nennt sie gar nicht** – `Unveraendert: 58 \| Projektdateien vorhanden: 20` |
| `install.py --update` | 0 | unberührt | `Hinweis: .claude/settings.json wurde nicht angefasst, weil sie Projektwerte enthaelt.` |

Die Datei steht in `shared_seed`, nicht in `shared_core` – sie wird bei der Erstinstallation
angelegt und danach nie wieder geschrieben. **Das ist richtig** (sie trägt Projektwerte), und es
ist zugleich der Grund, warum die Prüfung nicht aus dem Abgleich kommen kann, den `--check` für
die Kerndateien leistet. `--check` sagt über diese Datei nichts, nicht einmal ihren Namen.

## 3. Befund 2: Es gibt keine Overlay-Erweiterung – und drei Texte sagen etwas anderes

### 3.1 Was behauptet wird

Aus der Übergabe, Kandidat 1: *„Die Regelmenge hat für Befehle genau drei Platzhalter, alle drei
belegt; `clientmap.py` kennt keine Erweiterungsquelle. Und der Kommentarkopf der erzeugten Datei
sagt trotzdem ‚Ebene 3 + Overlay-Erweiterungen'."*

### 3.2 Bestätigt, im Code

`render_permissions` baut die Körbe so:

```python
rechte.update(man.get("permissions_extra", {}))
for korb in ("deny", "ask", "allow"):
    rechte[korb] = _korb_rendern(quelle, man, korb)
```

`permissions_extra` ist eine **Manifest**-Angabe, also Ebene 3, und wird von der Schleife
darunter für die drei Körbe ohnehin wieder überschrieben; bei `claude-code` trägt es
`{"defaultMode": "default"}`. **Eine Quelle des Projekts liest diese Funktion nicht** – kein
Pfad unterhalb von `project-overlay/`, kein Feld, keine Datei. Die einzige Stelle, an der ein
Projekt in diese Datei hineinkommt, ist der Platzhalter, und davon gibt es für Befehle drei.

### 3.3 Die drei Texte, die mehr sagen

**T1 – `clientmap.py` Zeile 182, der Kommentarkopf jeder erzeugten Datei:**

> „Berechtigungsvorlage des Frameworks (**Ebene 3 + Overlay-Erweiterungen**), erzeugt für das
> Client Pack …"

Die Wendung „Overlay-Erweiterung" hat im Repositorium eine feste Bedeutung, und es ist nicht
diese: Sie bezeichnet die projekteigenen **Regeldateien** `2N-*`
(`CHANGELOG.md` Zeile 1447, `FW-KO-02`-Protokoll, `build/doc/15-referenzstruktur.md`). Hier
meint sie die gefüllten Platzhalter. **Derselbe Begriff, zwei Gegenstände, und der falsche steht
in jeder erzeugten Datei jedes Projekts.**

**T2 – `templates/project-overlay/OVERLAY.md` Abschnitt 6.** Die Tabelle hat sechs Zeilen und
eine Spalte mit der Überschrift **„Freigabestufe in `<PERMISSIONS_FILE>`"**:

| Zeile | Platzhalter | Spalte „Freigabestufe in `<PERMISSIONS_FILE>`" | Erreicht die Datei? |
|---|---|---|---|
| Alle Unit-Tests | `<TEST_COMMAND>` | ask (KANN … auf allow) | ja |
| Einzelner Test / Testklasse | – | ask | **nein** |
| Integrations-/Komponententests | – | ask | **nein** |
| Linting / Formatprüfung | `<LINT_COMMAND>` | ask | ja |
| Statische Codeanalyse (lokal) | – | ask | **nein** |
| Weitere freigegebene Befehle | – | ask | **nein** |

**Vier von sechs Zeilen der Tabelle fordern einen Eintrag an, für den es keinen Weg gibt** – und
die Spaltenüberschrift nennt die Datei beim Namen. Ein Overlay Owner, der diese Tabelle
gewissenhaft ausfüllt, hat danach vier Befehle, die er für freigegeben hält, und eine
Berechtigungsdatei, die drei kennt.

**T3 – `framework/core/03-security.md` Zeile 52, Abschnitt 4 „Berechtigungspolitik (normativ)":**

> | Freigegebene Projektbefehle | `Exec(<TEST_COMMAND>)`, `Exec(<BUILD_COMMAND>)`,
> `Exec(<LINT_COMMAND>)` | ask (**KANN im Overlay für Stufe niedrig auf allow gesetzt werden**) |

**Drei Zeilen unter derselben Tabelle steht der Satz, der das aufhebt:**

> „Änderungen an der Regelmenge erfolgen ausschließlich über Änderungsantrag (V10)."

Das ist die Bauform, die dieses Projekt schon zweimal gefunden hat – **die Zusage, deren
Widerlegung im eigenen Dokument steht.** Bei B11 war es „Ausnahmen je Domain" und fünf Zeilen
darunter „`deny` gewinnt immer"; das wurde mit 0.32.0 berichtigt. **Die Zeile darüber blieb
stehen** und macht dieselbe Aussage über dieselbe Datei.

### 3.4 Ein Entlastungsbefund: die MCP-Zeile ist *nicht* derselbe Fehler

Dieselbe Tabelle in `03-security.md` trägt eine Zeile, die nach der Bauform von T3 aussieht:

> | MCP-Werkzeuge | `mcp__*` | ask; **Freigaben je Server im Overlay** |

**Sie ist in Ordnung, und das gehört gesagt, weil die Ähnlichkeit trügt.** Die Freigabe je
Server läuft nicht über die Berechtigungsdatei, sondern über `<MCP_FILE>`; `OVERLAY.md` Zeile 173
sagt es ausdrücklich: *„Eintrag in `<MCP_FILE>` erst nach Freigabe; **Standard ask**"*. Die
Berechtigungsstufe bleibt `ask`, das Overlay entscheidet nur, welche Server es überhaupt gibt.
**Zwei getrennte Mechanismen, beide vorhanden, beide stimmig beschrieben.** Wer T3 behebt, darf
diese Zeile nicht mitnehmen.

### 3.5 Und ein Befund, der keiner ist: der Regelweg trägt bereits

`framework/core/05-working-model.md` Abschnitt 3.2 Nummer 1 und
`framework/runtime/root-instruction.md` Abschnitt 7:

> „Führe nur Befehle aus, die im Overlay freigegeben sind (`<BUILD_COMMAND>`, `<TEST_COMMAND>`,
> `<LINT_COMMAND>`, **weitere gemäß Overlay Abschnitt 6**)."

**Diese beiden Sätze sind richtig.** Sie sind eine **Anweisung** an den KI-Client, kein Versprechen
über eine Datei – genau wie die M3-Regel zu Hintergrund-Subagenten, die normativ gilt und
technisch nicht abbildbar ist (D-66). Der Kanal für „weitere freigegebene Befehle" **existiert
also**; er ist die Regelschicht, nicht die Berechtigungsdatei.

**Das entscheidet die Frage von Kandidat 1 praktisch mit.** Es geht nicht darum, ob ein Projekt
einen vierten Befehl freigeben kann – das kann es, über Abschnitt 6 und die Regelschicht. Es
geht darum, dass **drei Texte behaupten, dieser Befehl stehe danach in der Berechtigungsdatei.**

## 4. Warum eine `ask`-Zeile eine Ausweitung ist, auch wenn sie mechanisch nichts tut

Gegen die Behandlung einer ergänzten `ask`-Zeile als Ausweitung lässt sich einwenden: `ask` heißt
Rückfrage, und ein nicht gelisteter Befehl führt beim ausgelieferten `defaultMode` ebenfalls zu
einer Rückfrage. Mechanisch ändere die Zeile also nichts.

**Der Einwand trägt nicht, und zwar unabhängig davon, ob er stimmt.** Was die Zeile ändert, ist
nicht der Mechanismus, sondern die **Erklärung**: Nach `05-working-model.md` Abschnitt 3.2
führt der KI-Client *nur* Befehle aus, die im Overlay als freigegeben gelistet sind. Eine Zeile
im `ask`-Korb erklärt einen Befehl für freigegeben. **Das ist die Ausweitung, und sie wirkt auf
der Ebene, auf der dieses Framework arbeitet.** `CR-OTP-G-001` wurde genau daran abgelehnt: nicht
weil `docker run` ohne Rückfrage liefe, sondern weil die Zeile ihn für freigegeben erklärt hätte.

Diese Gegenprüfung misst deshalb **keine** Clientwirkung des `ask`-Korbs und stützt sich auf
keine. Sie misst, was der Validator sieht.

## 5. Was diese Gegenprüfung nicht leistet

- **Sie misst nur das Pack `claude-code`.** Bei `devin-desktop` ist die Abbildung anders
  (`permission_exec_match` literal statt prefix); die Befunde M1 bis M8 hängen am Validator und
  nicht an der Abbildung, aber gemessen ist es dort nicht.
- **Sie misst keine Clientwirkung.** Ob eine ergänzte `allow`-Zeile am Client tatsächlich
  durchlässt, ist nicht gemessen – siehe Abschnitt 4, warum es für den Befund nicht nötig ist.
  Wer die Wirkung behaupten will, braucht eine Sitzung.
- **Sie sagt nichts über den Piloten selbst.** Dass dort `Bash(mvn -B test:*)` und ein belegter
  `<LINT_COMMAND>` stehen, obwohl das Overlay „Lint: nicht vorhanden" sagt, steht in der Übergabe
  und ist hier nicht nachgemessen worden; die Datei des Piloten ist untracked und gehört dem
  Piloten.
- **Sie beantwortet die Ermessensfrage nicht.** Ob es eine ausgewiesene Overlay-Erweiterung
  *geben soll*, ist keine Messung. Die Messung sagt nur, dass es sie nicht gibt und dass drei
  Texte das Gegenteil behaupten.

## 6. Gegenzeichnung

| Rolle | Name/Kennung | Datum | Ergebnis bestätigt |
|---|---|---|---|
| `<FRAMEWORK_OWNER>` | `<TBD>` | `<TBD>` | `<TBD>` |
