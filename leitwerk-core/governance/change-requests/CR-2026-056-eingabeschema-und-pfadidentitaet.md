# Änderungsantrag `CR-2026-056`

| Feld | Inhalt |
|---|---|
| Titel | Der Schutz-Hook kennt kein Ereignis – er nimmt jede JSON-Struktur an und prüft Felder, die nicht zur Operation gehören |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-13 |
| Betroffene Artefakte | `tests/scripts/hook-check-secrets.py` (Umbau in drei Stufen), beide `clients/*/manifest.json` (neues Feld `hook_path_fields`), beide `CLIENT_PACK.md` (neue Zeile **H4**, Berichtigung Abschnitt 5, Summen), `tests/scripts/validate-framework.py` (**Prüfung 32**), `tests/scripts/probe-pruefungen.py`, `framework/core/03-security.md`, `tests/EDGE_CASES.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** (durchsetzender Mechanismus) und Client Packs |
| Art | Befund **B06** des unabhängigen Reviews vom 2026-09-12, P2; **gegengeprüft, bestätigt, in jedem Teil größer als berichtet – und um einen Befund der Gegenrichtung erweitert, den der Bericht nicht nennt** |
| Dringlichkeit | **Paket 6**, erster Eintrag. Der Teil aus Abschnitt 1.4 ist **P1**: Er sperrt das Pack `claude-code` für jeden Schreibzugriff und betrifft den laufenden Piloten |

## 1. Anlass und Problem

Die Gegenprüfung liegt vor: `tests/protocols/2026-09-13-B06-gegenpruefung.md`, vier Messreihen –
41 synthetische Eingaben, die 20 **aufgezeichneten** Hook-Eingaben beider Packs, Pfadvarianten am
echten Dateisystem mit `os.path.samefile` als Vorprüfung, und zwei Sitzungen eines realen Clients
mit Kontrolllauf.

### 1.0 Eine Ursache, zwei entgegengesetzte Symptome

Der Kopfkommentar des Hooks nennt sie beim Namen und hält sie für eine Entscheidung:

> „Das Skript ist bewusst schema-agnostisch: Es durchsucht alle Zeichenketten der über stdin
> gelieferten JSON-Struktur.“ (`hook-check-secrets.py:6`)

Weil er kein Ereignis prüft, nimmt er jede Struktur an, die JSON ist – **er lässt zu viel durch**.
Weil er *alle* Zeichenketten durchsucht, prüft er auch Felder, die nicht zur Operation gehören –
**er blockiert zu viel**. Das Review sieht nur die erste Hälfte.

### 1.1 `--fail-closed` fängt genau einen Fall ab: den Syntaxfehler

```python
payload = json.loads(raw) if raw.strip() else {}      # :233
```

Eine leere Eingabe wird zu einem leeren Objekt **erklärt**; ein `json.loads`, das nicht wirft, gilt
als gelesenes Ereignis. Gemessen, alle mit `--fail-closed`: leere Eingabe, nur Weißraum, `[]`,
`null`, eine Zeichenkette und eine Zahl laufen sämtlich mit **Exit 0** durch. **Das Review nennt
zwei Formen, es sind sechs.**

### 1.2 Ein unbekannter Werkzeugname überspringt beide Pfadblöcke

```python
if tool_name in WRITE_TOOLS + EXEC_TOOLS + READ_TOOLS + SEARCH_TOOLS or not tool_name:   # :258
```

Gemessen: `MultiEdit`, `mcp__fs__write_file`, `ReadFileTool`, `Task` und der Wert `42` – jeweils mit
einem Kernpfad oder `.env` in der Eingabe – laufen mit **Exit 0** durch. Die Secret-Muster greifen
weiterhin; betroffen ist die **Pfad**prüfung. Der Wert `42` ist eine eigene Feststellung:
`str(payload.get("tool_name", ""))` macht aus jedem Typ einen Werkzeugnamen.

### 1.3 Eigene Feststellung: Der Rückfall für die unbekannte Operation ist die einzige Stelle ohne Kernschutz

Der Kommentar nimmt für sich in Anspruch, was der Code nicht tut:

```python
# Ohne Werkzeugnamen ist die Art der Operation unbekannt; dann gilt die
# strengere Liste. …
schreibend = tool_name in WRITE_TOOLS or not tool_name          # :266
…
if tool_name in WRITE_TOOLS:                                    # :287  <- das Kernverzeichnis
```

`schreibend` wählt zwischen zwei Listen; die **strengste** – das Kernverzeichnis als Ganzes – hängt
an einer dritten Bedingung, und die ist ohne Werkzeugnamen falsch. Gemessen: Ein Objekt ohne
`tool_name` mit `file_path: leitwerk-core/VERSION` läuft mit **Exit 0** durch, dasselbe mit
`tool_name: "Write"` blockiert. **Die Stelle, die sich ausdrücklich die strengere nennt, ist die
einzige, an der der Kern ungeschützt ist.**

### 1.4 Eigene Feststellung, P1: Der Hook blockiert bei `claude-code` **jeden** Schreibzugriff

Das Review beschreibt B06 durchgehend als „lässt durch“. Gemessen ist die Gegenrichtung.

Die 15 aufgezeichneten `claude-code`-Eingaben führen den Umschlag `cwd`, `effort`,
`hook_event_name`, `permission_mode`, `prompt_id`, `session_id`, `tool_use_id`, **`transcript_path`**.
Der Transkriptpfad liegt immer unter `~\.claude\projects\…` und trifft damit
`(^|[\\/])\.(devin|claude)[\\/]` – ein **Strukturpfad**, und der gilt für schreibende Werkzeuge.

Die einzige Schreiboperation im Bestand – auf eine harmlose Datei in einem Wegwerfverzeichnis –
läuft unverändert durch den Hook mit **Exit 2**. Einvariabel isoliert:

| Variante der aufgezeichneten Eingabe | Exit |
|---|---|
| unverändert | **2** |
| ohne `transcript_path` | 0 |
| `transcript_path` mit `\neutral\` statt `\.claude\` | 0 |
| ohne `cwd` | **2** |
| nur `tool_name` + `tool_input` | 0 |

**Am Client nachgemessen**, drei Läufe, Aufgabe identisch: mit Regeltexten verweigert der Agent aus
den Regeln (Modellverhalten); **ohne Regeltexte, nur mit der Hook-Konfiguration, blockiert der Hook
und die Datei entsteht nicht**; im Kontrolllauf ohne Hook entsteht sie. Der Matcher der erzeugten
`.claude/settings.json` führt `Edit|Write|NotebookEdit`, das Kommando trägt `--fail-closed`.

**Für ein Projekt mit diesem Pack ist damit jedes direkte Schreiben gesperrt, unabhängig vom Ziel.**
Das Muster steht seit 0.7.0. Unbemerkt blieb es, weil Prüfung 16 den Hook **ohne Umschlag** aufruft,
der Aufzeichnungs-Hook ein anderer Hook ist, der nichts entscheidet, und auf dem Branch des Piloten
nichts committet ist.

### 1.5 Eigene Feststellung: `cwd` ist der zweite Kanal derselben Ursache

Nur Pflichtfelder, Ziel `/tmp/x.txt`: Exit 0. Dieselbe Eingabe mit `cwd = …\leitwerk-core\tests`:
**Exit 2**. **Eine Sitzung, die im Kernverzeichnis startet, kann nirgendwohin mehr schreiben.** Es
ist kein Feld, es ist eine Gattung – eine Ausnahmeliste für `transcript_path` würde beim nächsten
Client-Feld wieder brechen.

### 1.6 Sieben von neun Musterfamilien sind schreibungssensitiv – und zwei sind es nicht

Das Review nennt das Kernverzeichnis. Gezählt: `\.env`, `id_(rsa|ed25519|ecdsa)`,
`(AGENTS|CLAUDE)\.md`, `\.(devin|claude)/`, `project-overlay/`, `framework/core/` und
`<CORE_DIR>/` tragen **kein** `re.I`; die Endungsliste und `secrets?/` tragen es. **Das ist der
Beleg, dass es keine Entscheidung für POSIX-Semantik war, sondern eine Ungleichbehandlung
innerhalb derselben Datei.**

### 1.7 Fünf bzw. sechs Pfadvarianten treffen dieselbe Datei und werden verschieden entschieden

Jede Variante vorab mit `os.path.samefile` belegt. Auf `<CORE_DIR>/VERSION` passieren
**Großbuchstaben, der 8.3-Kurzname `LEITWE~1`, eine Junction und ein Gerätepfad mit
Großschreibung**; auf `CLAUDE.md` passieren **Kleinschreibung, ein Punkt am Ende, ein Leerzeichen
am Ende und `::$DATA`**. **Kurzname, Punkt- und Leerzeichen-Anhang und der Datenstrom-Zusatz
kommen im Review nicht vor.**

Die Gegenprobe hält: `leitwerk-core-alt/x.txt` und `AGENTS.md.bak` werden **nicht** blockiert. Der
vom Review vorsorglich genannte Präfixfehler liegt **nicht** vor – die Muster verlangen einen
Trenner.

**Nachgemessen, und es entscheidet den Zuschnitt:** `os.path.realpath` führt Großschreibung,
Kurzname, Junction, Punktsegmente, Punkt- und Leerzeichen-Anhang und `::$DATA` auf die
Standardschreibweise zurück – auch für ein nicht existierendes Ziel über den existierenden
Elternpfad. **Nur der Gerätepfad-Präfix `\\?\` überlebt.** Es braucht also keinen Neubau der
Musterlogik.

### 1.8 Nebenbefund: Abschnitt 5 beider Packs behauptet seit neun Releases fail-open

Beim Einfügen der Matrixzeile aufgefallen:

| Stelle | Wortlaut | Stand |
|---|---|---|
| `devin-desktop/CLIENT_PACK.md` Abschnitt 5 | „**Der Schutz-Hook blockiert nicht.** … läuft bei diesem Pack fail-open … Bis dahin ist H2 eine Absichtserklärung, keine Schranke“ | **falsch seit 0.25.0** |
| ebenda, Folgeabsatz | „Das Manifest führt `hook_fail_closed: false`“ | **falsch** – es führt `true` |
| `claude-code/CLIENT_PACK.md` Abschnitt 5 | „Bei `devin-desktop` ist H2 als `[TEXTUELL]` eingestuft … dort läuft das Hook-Skript weiter fail-open“ | **falsch** – H2 steht dort auf `[TECHNISCH]` |

Zeile H2 desselben Dokuments sagt seit 0.25.0 das Gegenteil: „Seit 0.25.0 **fail-closed**
(`hook_fail_closed: true`)“. **Die Zusammenfassung widerspricht ihrer eigenen Tabelle** – dieselbe
Bauform wie die überzeichneten Summen aus 0.33.0, nur mit umgekehrtem Vorzeichen: Hier
**unter**zeichnet der Fließtext, was der Mechanismus leistet.

## 2. Vorgeschlagene Änderung

Der Hook wird in **drei Stufen** gegliedert, wie das Review es vorschlägt: Ereignis validieren,
Operation samt Pfaden normalisieren, Regeln auswerten. Die Muster bleiben, was sie sind.

1. **Ereignis.** Ein Ereignis ist ein JSON-**Objekt** mit einem nicht leeren `tool_name` vom Typ
   Zeichenkette und einem `tool_input`, das vorhanden und ein Objekt ist. Alles andere gilt als
   **unprüfbar**: mit `--fail-closed` blockiert es, sonst warnt es auf stderr und läuft durch –
   derselbe Weg, den der Syntaxfehler heute nimmt. **Zusätzliche unbekannte Felder bleiben
   zulässig**, damit eine additive Client-Erweiterung nicht zum Ausfall führt.
2. **Operation.** Ein Werkzeugname, der in keiner Verbliste steht, gilt als **unbekannte
   Operation** und wird nach der **strengsten** Liste gemessen – Secret-Pfade, Strukturpfade **und
   das Kernverzeichnis**. Dasselbe gilt für den Fall ohne Werkzeugnamen; damit stimmt der Kommentar
   aus 1.3 zum ersten Mal.
3. **Prüfmaterial.** Geprüft wird **`tool_input`**, nicht der Umschlag. `cwd` wird ausschließlich
   als **Auflösungsbasis** verwendet, nie als Prüfmaterial. Die Tokenzerlegung für ausführende
   Werkzeuge bleibt.
4. **Pfadidentität.** Die als Pfadfelder deklarierten Werte aus `tool_input` werden gegen `cwd`
   (sonst die Projektwurzel) aufgelöst, `\\?\`-Präfixe zuvor entfernt, dann `os.path.realpath`.
   Die vorhandenen Muster laufen zusätzlich über den aufgelösten Pfad – projektrelativ, wenn er
   innerhalb der Projektwurzel liegt, sonst absolut und nur gegen die Secret-Muster. Ein Pfad, der
   sich nicht auflösen lässt, und ein Gerätepfad im `\\.\`-Namensraum gelten als **unprüfbar**.
5. **Groß-/Kleinschreibung.** Alle Pfadmuster laufen mit `re.I`.
6. **Die Pfadfelder kommen aus den Manifesten** – neues Feld `hook_path_fields`, über alle Packs
   vereinigt, über einer Basisliste. Dieselbe Bauart wie `hook_tools` (D-28).
7. **Prüfung 32** misst die Wirkung: Eingabeschema, unbekannter Werkzeugname, Umschlagfeld,
   Pfadidentität – je Pack, mit Gegenproben.
8. **Zeile H4** in beiden Fachmatrizen; Abschnitt 5 beider Packs wird berichtigt; die Summen
   rechnet Prüfung 31 nach.
9. **Die Zeitlücke wird benannt**, im Docstring und in H4: Ein Hook prüft vor dem Zugriff; eine
   zwischenzeitlich umgebogene Verknüpfung kann er nicht ausschließen.

## 3. Was dieser Antrag nicht ändert

- **Er schließt den Shell-Schreibweg nicht.** Ausführende Werkzeuge werden weiterhin nur an den
  Secret-Pfaden gemessen (D-30); das Kernverzeichnis bleibt für `exec` offen (B04, D-47). **K-32
  bleibt damit offen** – der Selbstanwendungsweg über die Shell wird hier nicht zugemacht. Das war
  die Bedingung, unter der K-32 in Paket 6 steht, und sie ist mit diesem Antrag **nicht** erreicht.
- **Er baut keine Isolationsschicht.** Ohne sie bleibt die Zeitlücke bestehen; der Antrag benennt
  sie, er beseitigt sie nicht (`CR-2026-047` E5).
- **Er baut kein Sitzungsobjekt für M4/M5.** Das setzt B06 voraus und **zusätzlich** eine Quelle
  außerhalb der Reichweite des Agenten (`CR-2026-048` E1). Mit diesem Antrag ist die
  Voraussetzung erfüllt, mehr nicht.
- **Er misst keine POSIX-Plattform.** Junctions sind unter NTFS gemessen; symbolische
  Verknüpfungen unter Linux und macOS sind Erwartung, nicht Messung.
- **Er ändert die Musterlisten inhaltlich nicht.** Was geschützt ist, bleibt geschützt; geändert
  wird, **woran** gemessen wird.

## 4. Prüffragen

- [x] Richtige Ebene: durchsetzender Mechanismus im Kern, Deklaration im Pack.
- [x] Verschärfungsprinzip: **verschärft an fünf Stellen, lockert an einer** – und die eine ist
      benannt und kompensiert, siehe E3. Verschärft: sechs Eingabeformen, die durchliefen, blocken;
      unbekannte Werkzeuge und der leere Name bekommen den Kernschutz; sieben Musterfamilien werden
      schreibungsunempfindlich; fünf bzw. sechs Pfadvarianten werden erfasst; nicht auflösbare Pfade
      gelten als unprüfbar. Gelockert: das Prüfmaterial schrumpft vom Umschlag auf `tool_input`.
- [x] Widerspruchsfreiheit: gelesen wurden D-23 (jede Prüfung braucht eine Sonde), D-28
      (Werkzeugnamen aus den Manifesten), D-30 (zwei Schutzziele, zwei Listen), D-31 (der Schalter
      steht im Kommando, nicht in `env`), D-35, D-47 (Zusagen je Zugriffskanal), D-49 (beide
      Kodierungsumgebungen), `governance/PRIORITY_HIERARCHY.md`.
- [x] Laufzeitfassungen: Die erzeugten Regeln und die Hook-Konfiguration ändern sich **nicht**.
      Der Matcher bleibt, das Kommando bleibt. Geändert wird ausschließlich das Skript, das der
      Kern liefert – und das erreicht ein bestehendes Projekt über `install.py --update`.
- [x] Belegstatus: **vier Messreihen, davon zwei mit echten Clientdaten und eine am Client selbst,
      mit Kontrolllauf.** Kein Punkt dieses Antrags steht auf Codelektüre allein.
- [x] Test- und Validierungsbedarf: **Prüfung 32** mit Sonden und Gegenproben je Pack; dazu Sonden
      in `probe-pruefungen.py` für die Prüfung selbst und für ihren Anker.
- [x] Overlays: unberührt. Kein Overlay-Feld ändert sich.
- [ ] Dokumentation: `CHANGELOG.md`, Decision Log (D-61, D-62, D-63), Roadmap, beide Packs,
      `tests/EDGE_CASES.md`, `framework/core/03-security.md`.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Was gilt als Ereignis, und was passiert mit allem anderen? | **Objekt, nicht leerer `tool_name` als Zeichenkette, `tool_input` als vorhandenes Objekt.** Alles andere ist **unprüfbar** und nimmt den Weg des Syntaxfehlers: mit `--fail-closed` blockieren, sonst warnen. Zusätzliche unbekannte Felder bleiben ausdrücklich zulässig | Ein Client, der ein anderes Schema sendet, blockiert bei jedem Werkzeugaufruf statt still durchzulaufen. **Das ist genau, was `--fail-closed` zusagt** – aber es macht aus einem stillen Loch einen sichtbaren Ausfall. Die Meldung muss die Ursache und den Weg nennen: Fundstelle melden, Schema gegen die Clientdokumentation prüfen, Änderungsantrag |
| E2 | Wie wird ein unbekannter Werkzeugname behandelt: blockieren oder streng messen? | **Streng messen, nicht blockieren.** Er gilt als unbekannte Operation und bekommt die strengste Liste, einschließlich Kernverzeichnis. Blockieren würde den Hook darauf stützen, dass der Client den Matcher einhält – eine **Clientzusage**, und genau die Art unbelegter Annahme, an der AP2-CC-13 acht Releases lang hing (D-31) | Ein künftiges lesendes Werkzeug, das nicht im Manifest steht und einen Strukturpfad des Kerns anfasst, wird blockiert. Der Weg zurück ist ein Manifesteintrag, und die Meldung sagt das. **Der Preis ist gewollt:** Ein Werkzeug, das kein Pack kennt, soll auffallen |
| E3 | Wird nur `tool_input` geprüft – und damit die Reichweite **verkleinert**? | **Ja, und das ist die einzige Lockerung dieses Antrags.** Ein Pfad, der außerhalb von `tool_input` steht, wird nicht mehr gesehen. Kompensiert durch E1 und E2: Die Form ist ab jetzt Pflicht, und was nicht passt, wird streng gemessen oder blockiert. Der Umschlag trägt in beiden aufgezeichneten Schemata **keine Operationsdaten** – nur Sitzungs- und Ablaufkennungen | **Sie muss im Wirkungsnachweis nachgerechnet werden, nicht behauptet.** Eine Ausnahmeliste für `transcript_path` wäre die kleinere Änderung gewesen und ist verworfen: Es ist kein Feld, es ist eine Gattung (1.5). Bleibt der Umschlag im Prüfmaterial, kommt der Fehler beim nächsten Clientfeld zurück |
| E4 | Groß-/Kleinschreibung: plattformabhängig oder immer unempfindlich? | **Immer unempfindlich.** Der Hook liegt einmal im Kern und wird von allen Packs auf allen Plattformen geteilt; eine plattformabhängige Entscheidung machte das Ergebnis davon abhängig, wo er läuft, und wäre in einer Umgebung nicht prüfbar. Auf POSIX ist es eine **Verschärfung** – dieselbe Begründung, mit der die Muster schon heute `AGENTS` und `CLAUDE` gemeinsam führen | Ein Projekt auf Linux, das neben `AGENTS.md` eine eigene `agents.md` führt, kann sie nicht mehr schreiben. **Kein Schalter dafür** – ein Schalter wäre ein Hebel, den ein Agent umlegen kann. Der Weg ist der Änderungsantrag, und die Grenze steht in `EDGE_CASES.md` |
| E5 | Pfadidentität: Musterlogik neu bauen oder die Muster auf den aufgelösten Pfad anwenden? | **Auf den aufgelösten Pfad anwenden.** Gemessen (1.7): `realpath` trägt Kurzname, Junction, Punktsegmente, Punkt- und Leerzeichen-Anhang und `::$DATA`, auch für nicht existierende Ziele über den Elternpfad. Ein Neubau mit `commonpath` gegen aufgelöste Wurzeln löste dasselbe Problem mit mehr Code und einer zweiten Wahrheit über das, was geschützt ist | Der Hook fasst jetzt das Dateisystem an. Begrenzt: nur deklarierte Pfadfelder, für `exec` höchstens die Tokens, die wie Pfade aussehen, gedeckelt. **Jeder Fehlschlag ist `unprüfbar`, kein stilles Durchlassen** – sonst wäre die Auflösung eine neue Lücke statt einer Schranke |
| E6 | Woher weiß der Hook, welche Felder Pfade tragen? | **Aus den Manifesten**, neues Feld `hook_path_fields`, über alle Packs vereinigt, über einer Basisliste. Dieselbe Bauart und dieselbe Begründung wie `hook_tools` (D-28): Ein zusätzlich erkanntes Feld ist eine Verschärfung | Jedes künftige Pack braucht den Eintrag. Ein Pack, das ihn weglässt, fällt auf die Basisliste zurück – **die Basisliste muss deshalb gut sein**, und Prüfung 32 misst sie je Pack an einer Sonde, nicht am Vergleich zweier Listen |
| E7 | Wird die Zeitlücke zwischen Prüfung und Zugriff geschlossen? | **Nein, sie wird benannt** – im Docstring und in Zeile H4. Ein Hook kann eine zwischenzeitlich umgebogene Verknüpfung nicht ausschließen; das kann nur die ausführende Dateischicht oder eine Isolation | Eine bewusste, benannte Schuld, verknüpft mit dem Paket-6-Eintrag zur Isolationsschicht (`CR-2026-047` E5). **Eine Zeile, die die Grenze nicht nennt, wäre der Befundtyp dieses Projekts, hier neu erzeugt** |
| E8 | Bekommt die Fähigkeitsmatrix eine eigene Zeile? | **Ja, H4.** Die Lehre aus B11 und aus dem Suchkanal: Eine Zusage ohne Matrixzeile fällt niemandem auf. H4 trägt je Pack, was das Eingabeschema hergibt – bei `claude-code` gegen eine Installation bestätigt, bei `devin-desktop` gegen die Aufzeichnung | Die Summen ändern sich ein Release nach ihrer Berichtigung. Prüfung 31 rechnet sie nach; das ist kein Aufwand, sondern der Zweck der Prüfung |
| E9 | Wird der Nebenbefund aus 1.8 mitberichtigt, obwohl er nicht zu B06 gehört? | **Ja.** Drei Aussagen in zwei Packs behaupten seit **neun Releases** fail-open, während dieselben Dokumente in Zeile H2 fail-closed führen. Sie stehen im selben Abschnitt, den dieser Antrag ohnehin anfasst | Der Antrag wächst um eine Sache, die B06 nicht nennt. **Ihn zu vertagen hieße, eine bekannte Falschaussage stehen zu lassen, während man daneben schreibt** – und die Lehre aus 0.33.0 war genau diese: Was beim Anfassen auffällt, wird mitberichtigt und im Protokoll benannt |
| E10 | Was geschieht mit dem Piloten? | **Er braucht dieses Release, nicht nur `--update` auf 0.33.0.** Er steht auf 0.29.0 mit `claude-code`; das Schreiben ist dort gesperrt, seit die Installation steht. Der Migrationshinweis sagt es ausdrücklich | Die Übergabe an den Nutzer wird länger: `--update` auf 0.34.0, dann die beiden Handgriffe aus 0.30.0/0.32.0. **Dass der Pilot nie geschrieben hat, ist kein Zufall gewesen** – das gehört in den Hinweis, sonst liest es sich wie eine neue Einschränkung |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle zehn Fragen wie vorgelegt.** E1 Ereignisschema mit `unprüfbar` als drittem Ausgang; E2 unbekannter Werkzeugname wird streng gemessen, nicht blockiert; E3 nur `tool_input`, die Lockerung wird nachgerechnet; E4 immer schreibungsunempfindlich, ohne Schalter; E5 Muster auf den aufgelösten Pfad; E6 Pfadfelder aus den Manifesten; E7 Zeitlücke benannt, nicht geschlossen; E8 Zeile H4; E9 der Nebenbefund wird mitberichtigt; E10 der Pilot bekommt einen ausdrücklichen Hinweis |
| Datum | 2026-09-13 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | D-61 (der Hook prüft ein Ereignis, und `unprüfbar` ist ein eigener Ausgang), D-62 (geprüft wird die Operation, nicht der Umschlag), D-63 (Pfadidentität über den aufgelösten Pfad, schreibungsunempfindlich, ohne Schalter) |
| Auflagen | **Die Lockerung aus E3 ist nachzurechnen, nicht zu behaupten:** Der Wirkungsnachweis führt gegen den Vorstand, welche Fälle neu blocken und welcher Fall neu durchläuft. **Prüfung 32 ruft den Hook mit vollständigem Umschlag auf** – Prüfung 16 tut es nicht, und genau daran ist der P1-Befund vorbeigekommen; das ist die eigentliche Lehre und gehört in den Docstring der Prüfung. **Der Migrationshinweis nennt den Piloten.** **Offen bleiben ausdrücklich:** K-32 (der Shell-Weg wird nicht geschlossen), die Isolationsschicht, das Sitzungsobjekt für M4/M5, das Domain-Profil, und die POSIX-Messung der Verknüpfungen |
| Ziel-Release | `0.34.0` |
| Umsetzung | umgesetzt mit `0.34.0` |
