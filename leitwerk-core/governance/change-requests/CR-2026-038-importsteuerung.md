# Änderungsantrag `CR-2026-038`

| Feld | Inhalt |
|---|---|
| Titel | Die Quellen außerhalb des Projekts lassen sich abschalten – aus der Auskunft nach D-34 kann eine Schranke werden |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-11 |
| Betroffene Artefakte | beide `manifest.json` (neue Abbildung), `clientmap.py`, beide `CLIENT_PACK.md` (Zeile R5 und neuer Abschnitt), `governance/PRIORITY_HIERARCHY.md` (Regel 2.6, nachrichtlich), `governance/DECISION_LOG.md` (Fortschreibung D-34), `tests/scripts/validate-framework.py` (mögliche Prüfung 22) |
| Ebene laut Entscheidungsbaum 6 | Kern – Semantikabbildung und Abbildungsschicht; betrifft **beide** Client Packs |
| Art | Fortschreibung von D-34 nach der Erhebung K-21/K-23 (`tests/protocols/2026-09-11-erhebungen-K21-K26.md`) |
| Dringlichkeit | regulär; der Beschluss zu `CR-2026-031` ist noch nicht umgesetzt, beide Änderungen fallen in dieselbe Umsetzung |

## 1. Anlass und Problem

D-34 ist am 2026-09-11 unter einer ausdrücklich benannten Annahme entschieden worden: Eine Quelle
außerhalb des Projekts sei **auszuweisen, nicht zu unterbinden**. K-21 stand offen, und der
Antrag sagte dazu: „Eine Auskunft ist keine Schranke."

**Die Erhebung desselben Tages hat K-21 beantwortet – mit Ja, für beide Packs.**

### Was gemessen wurde

| Pack | Mechanismus | Messung |
|---|---|---|
| `devin-desktop` | `read_config_from` in **`.devin/config.json`**, also in der Berechtigungsdatei, die das Framework ohnehin erzeugt | Mit `windsurf: false` verschwindet der Inhalt der fremden Regel aus dem Kontext; ohne die Einstellung steht er darin. Mit `claude: false` sinkt die Skill-Zahl von 69 auf 2 – die 67 fremden Skills sind weg |
| `claude-code` | `claudeMdExcludes` in den Projekteinstellungen | Ohne die Einstellung lädt die `CLAUDE.md` eines Elternverzeichnisses mit; mit ihr bleibt allein die des Projekts |

Beides ist **projektseitig** wirksam, versionierbar und steht damit in Artefakten, die das
Framework schon heute schreibt.

### Der zweite Anlass: Es sind nicht nur Anweisungen

Die Erhebung hat außerhalb des Projekts auch **Konfiguration** gefunden (ERH-07):
`~/.claude/settings.json` führt sechs `allow`-Regeln **und** Hooks für `SessionStart`,
`PreToolUse` und `PostToolUse`; eine nutzerlokale Einstellungsdatei liegt zusätzlich im
Elternverzeichnis des Projekts.

**D-34 spricht von „Regeltexten, Skills oder Profilen".** Berechtigungen und Hooks außerhalb des
Projekts fallen nicht darunter – obwohl gerade sie die Linien betreffen, auf denen die
Kernzusagen B1 bis B6 stehen.

### Der dritte Anlass: Die Aufzählung zeigt mehr, als lädt

Zeile R5 aus `CR-2026-031` sagt zu: „Die geladenen Regelquellen sind vollständig aufzählbar."
Gemessen ist das Gegenteil einer Lücke – ein Überschuss: Mit abgeschaltetem Import führt
`devin rules list` die fremde Regel **weiter auf**, obwohl ihr Inhalt nicht mehr im Kontext steht
(ERH-02). Dazu nennt `devin skills paths` die Ablage nicht, aus der 67 von 81 Skills stammen
(ERH-03).

**Die Aufzählung ist eine Auskunft des Clients über sich selbst, kein Abbild des Kontexts.**

## 2. Vorgeschlagene Änderung

1. **Der Kern trifft die Aussage werkzeugneutral:** Das Framework importiert **keine** Regel- und
   Skillquellen fremder Werkzeugformate. Die eigene Wurzel-Anweisungsdatei ist davon
   ausgenommen – sie ist bei `devin-desktop` genau eines dieser Formate.

2. **Jedes Pack bildet die Aussage ab**, wie es Berechtigungen und Hooks abbildet (D-18):
   - `devin-desktop`: `read_config_from` mit `agents_standard: true` und `cursor`, `windsurf`,
     `claude` auf `false`, erzeugt von `clientmap.py` in die Berechtigungsdatei.
   - `claude-code`: `claudeMdExcludes` – **nicht** als Vorgabe der Installation, siehe E2.
   Ein Pack, dessen Client keinen solchen Mechanismus kennt, trägt die Aussage als
   `[NICHT ABBILDBAR]` und bleibt bei der Auskunft.

3. **Der Auskunftsabschnitt aus `CR-2026-031` heißt „Anweisungs- und Konfigurationsquellen
   außerhalb des Projekts"** und führt auch Berechtigungs-, Hook- und
   Einstellungsdateien außerhalb des Repositoriums.

4. **Zeile R5 trägt den Vorbehalt aus ERH-02**: Die Aufzählung des Clients ist nicht
   deckungsgleich mit dem, was lädt – sie kann zu viel zeigen und, wie ERH-03 belegt, auch zu
   wenig.

5. **D-34 wird fortgeschrieben**, nicht ersetzt: Der Rang bleibt, wie er ist; ergänzt wird, dass
   eine Quelle, für die der Client eine Importsteuerung kennt, **abgeschaltet statt nur
   ausgewiesen** wird.

6. **Prüfung 22 (siehe E4):** Die installierte Berechtigungsdatei führt die Importsteuerung so,
   wie das Manifest sie abbildet. Sonde nach D-23: Ein Wert wird in einer Kopie verfälscht – die
   Prüfung meldet ihn.

## 3. Was dieser Antrag nicht ändert

- **Den Rang aus D-34.** Eine Quelle außerhalb des Projekts bleibt ebenenlos. Wer sie abschaltet,
  ändert nicht ihren Rang, sondern ihre Anwesenheit.
- **Die Auskunftspflicht.** Sie gilt weiter, und gerade dann: Was abgeschaltet ist, muss benannt
  sein, sonst sucht jemand den Fehler an der falschen Stelle.
- **`agents_standard`.** Dieser Schalter bleibt `true`. Er steuert bei `devin-desktop` das Format
  der **eigenen** Wurzel-Anweisungsdatei; ihn abzuschalten hieße, das Framework abzuschalten.
- **Die Prioritätshierarchie.** Regel 2.6 bleibt unverändert.

## 4. Grenze der Zusage

**Gemessen wurde mit drei abgeschalteten Formaten zugleich.** `windsurf: false` allein ist nicht
geprüft; ebenso wenig, welches der drei `claudeMdExcludes`-Muster greift.

**Die Importsteuerung räumt das Register nicht.** `devin rules list` führt die Quelle weiter auf
(ERH-02). Wer die Wirkung prüfen will, muss den Kontext messen, nicht das Register lesen – genau
die Unterscheidung, an der `AP2-DD-10` hing.

**Der Vorrang gegenüber der nutzerglobalen Konfiguration ist unbekannt.** Die Dokumentation nennt
dieselben Schlüssel für `%APPDATA%\devin\config.json`. Ob eine nutzerglobale Einstellung die
projektseitige aufhebt, ist **nicht gemessen** – neu als **K-27**. Fiele die Antwort ungünstig
aus, wäre die Schranke wieder eine Auskunft.

**Ein Mensch kann sie zurücknehmen.** Die Einstellung steht in der Berechtigungsdatei; der
KI-Client darf sie nicht schreiben, eine Person schon. Das ist dieselbe Grenze wie bei B9.

**Die Maßnahme nimmt etwas weg.** Wer 67 Skills eines anderen Werkzeugs gewohnt ist, verliert sie
in Projekten mit dieser Installation. Das ist die Absicht – aber es ist eine Absicht, die jemand
erklären muss.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Fremdformate bei `devin-desktop` abschalten? | **Ja.** Die Quelle lädt sonst unbedingt und ebenenlos in jedes Projekt; die Steuerung liegt in einer Datei, die das Framework ohnehin schreibt | Skills und Regeln anderer Werkzeuge stehen in einem Projekt mit dieser Installation nicht mehr zur Verfügung. Wer sie braucht, braucht eine Ausnahme |
| E2 | `claudeMdExcludes` als Vorgabe der Installation bei `claude-code`? | **Nein.** Eine `CLAUDE.md` im Elternverzeichnis ist im Mehrprojekt-Verzeichnis oft **gewollt**; ein pauschaler Ausschluss bräche legitime Anordnungen | Bei diesem Pack bleibt es bei Auskunft und Empfehlung – die Lage ist damit zwischen den Packs verschieden, und die Matrix muss das zeigen |
| E3 | Auskunft auf Konfigurationsquellen erweitern? | **Ja.** Berechtigungen und Hooks außerhalb des Projekts betreffen genau die Linien, auf denen B1 bis B6 stehen | Der Abschnitt wird länger und verlangt bei jeder Erhebung mehr Arbeit |
| E4 | Prüfung 22 aufnehmen? | **Ja.** Ohne sie ist die Importsteuerung eine Zeile, die eine Installation still verlieren kann – der Befundtyp dieses Projekts | Eine Prüfung mehr, gebunden an ein clientspezifisches Feld; ein Pack ohne den Mechanismus muss ausdrücklich ausgenommen sein |
| E5 | K-27 (Vorrang nutzerglobal gegen projektseitig) vor der Umsetzung erheben? | **Erledigt am 2026-09-11.** Ergebnis im Nachtrag unten: Die Benutzerkonfiguration hat Vorrang | Die Antwort ist ungünstig – sie kostet die Einstufung, nicht die Maßnahme |

> **Vor der Entscheidung Abschnitt 7 lesen.** K-27 ist nach dem Verfassen dieses Antrags erhoben worden; das Ergebnis ändert die Einstufung der Maßnahme und bringt eine sechste Frage mit.

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** |
| Datum | 2026-09-11 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | E1 bis E6 wie vorgelegt, mit der Änderung aus dem Nachtrag: Die Importsteuerung wird gesetzt (`agents_standard` bleibt **true** – das ist die eigene Wurzel-Anweisungsdatei), ihre Einstufung ist jedoch **`[TEXTUELL]`**, weil die Benutzerkonfiguration Vorrang hat (K-27); bei `claude-code` **keine** Vorgabe von `claudeMdExcludes`; die Auskunft umfasst auch **Konfigurationsquellen**; Zeile R5 trägt den Vorbehalt aus ERH-02; Prüfung 22 kommt hinzu; **E6: Zeile B9 im Pack `devin-desktop` wird auf den gemessenen Stand gebracht** (ERH-11 widerlegt die Zusage für diesen Client). Ziel-Release 0.26.0 |

## 7. Nachtrag 2026-09-11 – K-27 ist erhoben, und die Antwort ist ungünstig

`tests/protocols/2026-09-11-erhebungen-K21-K26.md`, Abschnitt 7.

**Die nutzerglobale Einstellung hat Vorrang vor der projektseitigen** – gemessen in beiden
Richtungen. Was Abschnitt 4 als Risiko benannt hat, ist eingetreten: „Fiele die Antwort ungünstig
aus, wäre die Schranke wieder eine Auskunft."

**Was das für diesen Antrag ändert – und was nicht:**

- **Die Maßnahme bleibt richtig.** Ein Standard, der ohne Zutun gilt, ist besser als keiner. Wo
  die Benutzerkonfiguration schweigt – der Normalfall – wirkt die projektseitige Einstellung;
  das ist gemessen.
- **Die Einstufung ändert sich.** Die Zeile ist `[TEXTUELL]`, nicht `[TECHNISCH]`: Das Framework
  setzt einen Standard, den es nicht durchsetzt. Alles andere wäre die Art Zusage, gegen die
  dieses Projekt seine Sonden gebaut hat.
- **B9 ist bei diesem Pack widerlegt, nicht nur unbelegt** (ERH-11). Der VERIFY-Marker der Zeile
  („ob der Client eine Lockerung technisch verhindert") ist aufgelöst: Er verhindert sie nicht.
  Das gehört in dieselbe Umsetzung – als Korrektur der Zeile B9 und als bekannte Abweichung in
  Abschnitt 5 des Packs.

**Neue Frage zur Entscheidung:**

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E6 | B9 im Pack `devin-desktop` auf den gemessenen Stand bringen? | **Ja.** Die Zeile trägt heute einen offenen Marker, wo eine Messung vorliegt – und die Messung widerlegt die Zusage für diesen Client | Das Pack weist eine Zusage weniger aus. Dafür steht in der Matrix, was gilt, statt einer Frage, die beantwortet ist |
