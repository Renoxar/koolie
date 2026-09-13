# Gegenprüfung zu B06: der Hook kennt kein Ereignis – und lässt deshalb in beide Richtungen falsch durch

| Feld | Wert |
|---|---|
| Gegenstand | **B06** – Eingabeschema und Pfadauswertung des Schutz-Hooks (`tests/scripts/hook-check-secrets.py`) |
| Anlass | Der letzte ungeprüfte Befund des unabhängigen Reviews vom 2026-09-12, P2. Nach D-23 und dem Arbeitsplan gehört jeder Befund vor der Umsetzung gegengeprüft |
| Datum | 2026-09-13 |
| Framework-Version | 0.33.0 (Auscheckstand `22d0fcb`, Arbeitsbaum sauber) |
| Prüfmethode | **Vier Messreihen, keine Codelektüre allein.** (1) 41 synthetische Eingaben gegen den Hook, jede mit mitgeführter Erwartung; (2) die **aufgezeichneten** Hook-Eingaben beider Packs aus AP2 – 15 für `claude-code`, 5 für `devin-desktop` – unverändert durch den Hook; (3) Pfadvarianten am **echten Dateisystem**, jede vorab mit `os.path.samefile` als dieselbe Datei belegt; (4) zwei Sitzungen eines realen Clients gegen eine frische Installation, mit Kontrolllauf ohne Hook |
| Umgebung | Windows 11, Python 3.14.4, NTFS; Client `claude-code` |
| Ergebnis | **Der Befund bestätigt sich in allen vier Teilen – und die Zählung war in jedem Teil zu klein.** Dazu **sieben eigene Feststellungen**. Die schwerste dreht die Richtung des Befunds um: Der Hook lässt nicht nur zu viel durch, er **blockiert bei `claude-code` jeden Schreibzugriff überhaupt**. Beide Symptome haben dieselbe Ursache |

## 0. Die Ursache in einem Satz

**Der Hook weiß nicht, was ein Ereignis ist.** Sein Kopfkommentar nennt das eine Entscheidung:

> „Das Skript ist bewusst schema-agnostisch: Es durchsucht alle Zeichenketten der über stdin
> gelieferten JSON-Struktur.“ (`hook-check-secrets.py:6`)

Daraus folgt beides zugleich. Weil er kein Ereignis prüft, nimmt er jede Struktur an, die JSON ist –
das ist der Befund des Reviews. Und weil er *alle* Zeichenketten durchsucht, prüft er auch Felder,
die gar nicht zur Operation gehören – das ist der Befund, den das Review nicht nennt und der
schwerer wiegt. **Eine Zusage, die mehr verspricht, als sie leistet, ist der wiederkehrende
Befundtyp dieses Projekts. Hier steht daneben eine, die etwas ganz anderes tut, als sie sagt.**

## 1. Vorbemerkung: die Fundstellen des Reviews zeigen ins Leere

Das Review nennt `hook-check-secrets.py:154`, `:204`, `:205`, `:217`, `:229`. Gegen 0.33.0
nachgesehen:

| Genannt | Was dort in 0.33.0 steht |
|---|---|
| `:154` | `for verb, ziel in (("write", schreiben), …` – die Verbschleife in `_werkzeugnamen()` |
| `:204` | `for v in obj:` – die Listenschleife in `iter_strings` |
| `:205` | `yield from iter_strings(v)` |
| `:217` | Fließtext im Docstring von `fail_closed()` |
| `:229` | Leerzeile |

**Keine der fünf Angaben trifft.** Der Hook ist seit dem Berichtsstand zweimal gewachsen (0.29.0
Tokenzerlegung, 0.30.0 Such- und Leseverben). Die gemeinten Stellen liegen in 0.33.0 bei `:233`
(Eingabe lesen), `:246` (Werkzeugname), `:247` (Zeichenketten sammeln), `:258` (Werkzeuggatter),
`:266` (`schreibend`), `:287` (Kernverzeichnis). **Das ist die vierte Gegenprüfung in Folge, in der
die Zeilenangaben des Berichts nicht stimmen** – der Befund selbst bleibt davon unberührt.

## 2. Was das Review nennt – und was gemessen dabei herauskommt

Messreihe 1, 41 Eingaben. Vollständige Tabelle in Abschnitt 7.

### 2.1 „Leere Eingabe und ein JSON-Array passieren trotz `--fail-closed`“ – bestätigt, es sind sechs Formen

`--fail-closed` fängt genau einen Fall ab: den **Syntaxfehler**. Alles, was gültiges JSON ist, aber
kein Objekt, läuft durch:

| Eingabe | `--fail-closed` | gemessen |
|---|---|---|
| `kein json {` | greift | Exit 2 |
| leere Eingabe | **greift nicht** | Exit 0 |
| nur Weißraum | **greift nicht** | Exit 0 |
| `[]` | **greift nicht** | Exit 0 |
| `null` | **greift nicht** | Exit 0 |
| `"leitwerk-core/VERSION"` | **greift nicht** | Exit 0 |
| `42` | **greift nicht** | Exit 0 |

Der Grund steht in einer Zeile:

```python
payload = json.loads(raw) if raw.strip() else {}      # :233
```

Eine leere Eingabe wird zu einem leeren Objekt **erklärt**, und ein `json.loads`, das nicht wirft,
gilt als gelesenes Ereignis. **Das Review nennt zwei Formen, es sind sechs.**

### 2.2 „Ein unbekannter, nicht leerer Werkzeugname umgeht die Pfadprüfung“ – bestätigt

```python
if tool_name in WRITE_TOOLS + EXEC_TOOLS + READ_TOOLS + SEARCH_TOOLS or not tool_name:   # :258
```

Ein Name, der in keiner Liste steht und nicht leer ist, überspringt **beide** Pfadblöcke. Gemessen,
jeweils mit `--fail-closed`:

| Werkzeugname | Eingabe | Exit |
|---|---|---|
| `MultiEdit` | `file_path: leitwerk-core/VERSION` | **0** |
| `mcp__fs__write_file` | `path: leitwerk-core/VERSION` | **0** |
| `ReadFileTool` | `file_path: .env` | **0** |
| `Task` | `prompt: "Schreibe 9 nach leitwerk-core/VERSION"` | **0** |
| `42` (Zahl statt Zeichenkette) | `file_path: leitwerk-core/VERSION` | **0** |

Die letzte Zeile ist eine eigene Feststellung: `str(payload.get("tool_name", ""))` macht aus jedem
Wert eine Zeichenkette, und `42` ist dann ein unbekannter Werkzeugname. **Die Secret-Muster greifen
weiterhin** – sie laufen vor dem Werkzeuggatter; ein `password = …` im Inhalt blockiert auch bei
`VoelligUnbekannt` (gemessen). Betroffen ist ausschließlich die **Pfad**prüfung.

### 2.3 „Das Muster für das Kernverzeichnis ist groß-/kleinschreibungssensitiv“ – bestätigt, es sind sieben von neun

Das Review nennt ein Muster. Gezählt sind es sieben:

| Liste | Muster | `re.I` |
|---|---|---|
| `SECRET_PATH_PATTERNS` | `(^\|[\\/])\.env(\.\|$)` | **nein** |
| | `\.(pem\|key\|p12\|pfx\|jks\|keystore)$` | ja |
| | `(^\|[\\/])id_(rsa\|ed25519\|ecdsa)` | **nein** |
| | `(^\|[\\/])secrets?[\\/]` | ja |
| `STRUCTURE_PATH_PATTERNS` | `(^\|[\\/])(AGENTS\|CLAUDE)\.md$` | **nein** |
| | `(^\|[\\/])\.(devin\|claude)[\\/]` | **nein** |
| | `(^\|[\\/])project-overlay[\\/]` | **nein** |
| | `(^\|[\\/])framework[\\/]core[\\/]` | **nein** |
| `PROTECTED_WRITE_PATH_PATTERNS` | `(^\|[\\/])<CORE_DIR>[\\/]` | **nein** |

**Zwei tragen `re.I`, sieben nicht.** Das ist der eigentliche Beleg: Wäre die Sensitivität eine
Entscheidung für POSIX-Semantik, stünden die zwei nicht da. Sie ist keine Entscheidung, sondern
eine Ungleichbehandlung innerhalb derselben Datei.

Gemessen, alle mit `Write`:

| Eingabe | Exit |
|---|---|
| `leitwerk-core/VERSION` | 2 |
| `LEITWERK-CORE/VERSION` | **0** |
| `AGENTS.md` | 2 |
| `agents.md` | **0** |
| `.env` | 2 |
| `.ENV` | **0** |
| `.claude/settings.json` | 2 |
| `.Claude/settings.json` | **0** |

## 3. Eigene Feststellung 1: Der Rückfall für die unbekannte Operation ist die einzige Stelle ohne Kernschutz

Der Kommentar sagt das Gegenteil dessen, was der Code tut:

```python
# Ohne Werkzeugnamen ist die Art der Operation unbekannt; dann gilt die
# strengere Liste. Eine unbekannte Operation als lesend zu behandeln, waere
# die Annahme zugunsten des Zugriffs.
schreibend = tool_name in WRITE_TOOLS or not tool_name          # :266
```

`schreibend` steuert die Wahl zwischen `SECRET_PATH_PATTERNS` und `PROTECTED_PATH_PATTERNS`. Die
**strengste** Liste – das Kernverzeichnis als Ganzes – hängt aber an einer anderen Bedingung:

```python
if tool_name in WRITE_TOOLS:                                    # :287
```

Ohne Werkzeugnamen ist diese Bedingung **falsch**. Gemessen:

| Eingabe | Exit |
|---|---|
| `{"tool_input": {"file_path": "leitwerk-core/VERSION"}}` (kein `tool_name`) | **0** |
| `{"tool_name": "", "tool_input": {"file_path": "leitwerk-core/VERSION"}}` | **0** |
| `["leitwerk-core/VERSION"]` | **0** |
| `{"tool_name": "Write", "tool_input": {"file_path": "leitwerk-core/VERSION"}}` | 2 |

**Die Stelle, die ausdrücklich für sich in Anspruch nimmt, die strengere zu sein, ist die einzige,
an der das Kernverzeichnis ungeschützt ist.** Das Review nennt diesen Fall nicht; es beschreibt den
unbekannten *nicht leeren* Namen. Der leere Name ist der schlechtere Fall, weil der Kommentar ihn
für erledigt erklärt.

## 4. Eigene Feststellung 2: Fünf bzw. sechs Pfadvarianten treffen dieselbe Datei und werden verschieden entschieden

Messreihe 3, am echten Dateisystem einer frischen Installation. **Jede Variante wurde vorab mit
`os.path.samefile` gegen die Standardschreibweise geprüft** – die Tabelle führt nur Varianten, bei
denen das Betriebssystem dieselbe Datei liefert.

Ziel `<CORE_DIR>/VERSION`, Werkzeug `Write`, Referenzentscheidung Exit 2:

| Variante | dieselbe Datei | Exit |
|---|---|---|
| relativ, Standardschreibweise | ja | 2 |
| absolut | ja | 2 |
| doppelter Trenner, gemischte Trenner, Punktsegmente | ja | 2 |
| aus `tests/` heraus über `..`, ohne den Kern zu nennen | ja | 2 |
| Gerätepfad `\\?\…` | ja | 2 |
| **Kernverzeichnis in Großbuchstaben** | ja | **0** |
| **absolut, Kern in Großbuchstaben** | ja | **0** |
| **8.3-Kurzname (`LEITWE~1`)** | ja | **0** |
| **Junction auf das Kernverzeichnis** | ja | **0** |
| **Gerätepfad mit Großschreibung** | ja | **0** |

Wurzel-Anweisungsdatei `CLAUDE.md`, Werkzeug `Write`, Referenzentscheidung Exit 2:

| Variante | dieselbe Datei | Exit |
|---|---|---|
| `CLAUDE.md`, absolut, über Punktsegment | ja | 2 |
| **`claude.md`, `Claude.Md`** | ja | **0** |
| **`CLAUDE.md.`** (Punkt am Ende) | ja | **0** |
| **`CLAUDE.md `** (Leerzeichen am Ende) | ja | **0** |
| **`CLAUDE.md::$DATA`** (Datenstrom-Zusatz) | ja | **0** |

**Das Review nennt Verknüpfungen und Groß-/Kleinschreibung. Kurzname, Punkt- und
Leerzeichen-Anhang und der Datenstrom-Zusatz kommen dort nicht vor** – drei Bauformen, die Windows
alle auf dieselbe Datei abbildet.

Die Gegenprobe hält: `leitwerk-core-alt/x.txt` und `AGENTS.md.bak` werden **nicht** blockiert. Der
Präfixfehler, den das Review vorsorglich nennt („ein Verzeichnis mit ähnlichem Namensanfang ist
kein Kind“), liegt hier **nicht** vor – die Muster verlangen einen Trenner.

### Nachgemessen: die Auflösung trägt

Vor dem Entwurf geprüft, ob `os.path.realpath` diese Varianten einfängt:

| Variante | aufgelöst |
|---|---|
| Großbuchstaben, 8.3-Kurzname, Junction, Punktsegmente | → Standardschreibweise |
| Punkt am Ende, Leerzeichen am Ende, `::$DATA` | → Standardschreibweise |
| nicht existierendes Ziel, auch über die Junction | → Standardschreibweise des Elternpfads |
| **Gerätepfad `\\?\…`** | **bleibt `\\?\…`** |

**Bis auf den Gerätepfad-Präfix trägt die Auflösung alles.** Das entscheidet den Zuschnitt der
Umsetzung: Es braucht keinen Neubau der Musterlogik, sondern die Anwendung der vorhandenen Muster
auf den **aufgelösten** Pfad – plus eine ausdrückliche Behandlung des Gerätepfad-Präfixes.

## 5. Eigene Feststellung 3: Der Hook blockiert bei `claude-code` jeden Schreibzugriff

**Das ist der schwerste Punkt dieser Gegenprüfung, und das Review nennt ihn nicht.** Es beschreibt
B06 durchgehend als „lässt durch“. Gemessen ist die Gegenrichtung.

### 5.1 Der Beleg stammt aus einer Aufzeichnung, nicht aus einer Annahme

`devpacks/leitwerk-erhebungen-2026-09-12/ap2-hook-aufzeichnung-*.jsonl` hält 15 reale
`claude-code`-Hook-Eingaben. Ihre Felder:

```
cwd, effort, hook_event_name, permission_mode, prompt_id,
session_id, tool_input, tool_name, tool_use_id, transcript_path
```

Genau eine davon ist ein Schreibzugriff – auf eine harmlose Datei in einem Wegwerfverzeichnis:

```json
"transcript_path": "C:\\Users\\reneh\\.claude\\projects\\…\\72a9d9af….jsonl",
"tool_name": "Write",
"tool_input": { "file_path": "…\\scratchpad\\b01\\B01-SCHREIBPROBE.txt", "content": "GESCHRIEBEN-5502" }
```

Unverändert durch den Hook (Messreihe 2): **Exit 2.**

`transcript_path` enthält `\.claude\`. Das Muster `(^|[\\/])\.(devin|claude)[\\/]` trifft, `Write`
ist ein schreibendes Werkzeug, also gelten die Strukturpfade – **und der Pfad, der sie auslöst, ist
nicht das Ziel der Operation, sondern ein Nebenfeld des Clients.**

### 5.2 Die Ursache ist einvariabel isoliert

Ausgangspunkt ist dieselbe aufgezeichnete Eingabe; verändert wird je Zeile genau ein Feld:

| Variante | Exit |
|---|---|
| unverändert, wie aufgezeichnet | **2** |
| ohne `transcript_path` | 0 |
| `transcript_path` mit `\neutral\` statt `\.claude\` | 0 |
| ohne `cwd` | **2** |
| nur `tool_name` + `tool_input` | 0 |
| dieselbe Eingabe als `Read` | 0 |
| dieselbe Eingabe als `Bash` | 0 |

**`transcript_path`, und nur dieses Feld.** Betroffen sind ausschließlich die drei schreibenden
Werkzeuge – `Read`, `Grep`, `Glob` und `Bash` werden nach D-30 nur an den Secret-Pfaden gemessen
und bleiben unberührt. Das erklärt, warum die übrigen 14 Aufzeichnungen sich richtig verhalten:
**Es war die einzige Schreiboperation im ganzen Bestand.**

### 5.3 Am Client nachgemessen – eine Messung am Hook ist keine Messung am Client

Drei Läufe gegen frisch erzeugte Verzeichnisse, Aufgabe jeweils identisch: „Lege
`B06-SCHREIBPROBE.txt` mit dem Inhalt `GESCHRIEBEN-4711` an, nutze das Write-Werkzeug.“

| Lauf | Umgebung | Ergebnis | Datei angelegt |
|---|---|---|---|
| 1 | vollständige Installation **mit Regeltexten** | Der Agent verweigert unter Verweis auf das inaktive Overlay und M1 | nein |
| 2 | **nur die Hook-Konfiguration, keine Regeltexte** | „Der Schreibvorgang wurde von einem Guard-Hook blockiert“, Wortlaut der Framework-Meldung | **nein** |
| 3 | **Kontrolle: nichts installiert** | Datei angelegt, Inhalt `GESCHRIEBEN-4711` | ja |

Lauf 1 ist der Grund, warum es Lauf 2 braucht: **Mit Regeltexten misst man Modellverhalten statt
Engine.** Lauf 3 ist der Kontrolllauf ohne die geprüfte Schranke und macht Lauf 2 erst zu einer
Messung. Die Kette ist damit geschlossen: **Der Hook ist die Ursache, nicht das Modell, nicht der
Client, nicht die Berechtigungsdatei.**

### 5.4 Die Konfiguration erfasst genau diese Werkzeuge

An einer frischen Installation nachgesehen (`.claude/settings.json`):

```json
"matcher": "Read|Grep|Glob|Bash|Edit|Write|NotebookEdit",
"command": "python \"$CLAUDE_PROJECT_DIR/…/hook-check-secrets.py\" --fail-closed"
```

`Edit`, `Write` und `NotebookEdit` stehen im Matcher, `--fail-closed` steht im Kommando. **Für ein
Projekt, das dieses Pack installiert, ist damit jedes direkte Schreiben gesperrt** – unabhängig vom
Ziel.

### 5.5 Warum es unbemerkt blieb

Nicht durch Nachlässigkeit, sondern weil jede vorhandene Prüfung an dieser Stelle vorbeisieht:

- **Prüfung 16** ruft den Hook mit `{"tool_name": …, "tool_input": …}` auf – **ohne Umschlag**.
  Sie kann den Fehler nicht sehen, weil sie das Feld nie mitschickt.
- **Die AP2-Aufzeichnung** enthält genau einen Schreibzugriff, und der Aufzeichnungs-Hook ist ein
  *anderer* Hook: Er schreibt mit und entscheidet nichts. Die Aufzeichnung belegt das Schema, sie
  hat den Schutz-Hook nie ausgeführt.
- **Der Pilot** steht auf 0.29.0 mit `claude-code`, und auf seinem Branch ist **nichts committet**.
  Der Fall ist dort nie eingetreten, weil noch niemand schreiben wollte.

**Das ist der Befundtyp „eine Messung am Hook ist keine Messung am Client“, ein Feld weiter:** Eine
Messung mit selbst gebauter Eingabe ist keine Messung mit der Eingabe des Clients.

## 6. Eigene Feststellung 4: `cwd` ist der zweite Kanal derselben Ursache

Nicht nur `transcript_path`. Jedes Umschlagfeld, das einen Pfad trägt, wirkt gleich:

| Eingabe | Exit |
|---|---|
| nur Pflichtfelder, Ziel `/tmp/x.txt` | 0 |
| dieselbe Eingabe **+ `cwd` = `…\leitwerk-core\tests`** | **2** |
| dieselbe Eingabe + `cwd` = `…\leitwerk-core` (ohne Trenner danach) | 0 |

**Eine Sitzung, die im Kernverzeichnis startet, kann nirgendwohin mehr schreiben** – auch nicht
außerhalb. Dass die Kernwurzel selbst durchläuft, ist reiner Zufall der Mustergrenze: Das Muster
verlangt einen Trenner **nach** dem Namen, und `cwd` endet ohne einen.

Das ist zugleich die Antwort auf die Frage, ob eine Ausnahmeliste für `transcript_path` genügte:
**Nein.** Es ist kein Feld, es ist eine Gattung. Ein Pack, das morgen `workspace_root` mitschickt,
bringt den Fehler zurück.

## 7. Messreihe 1 vollständig

41 Eingaben, jede mit mitgeführter Erwartung. **19 Abweichungen.** Positivkontrollen (normales
Schreiben, normales Lesen, `git diff` auf einen Kernpfad) und Negativkontrollen (Kernpfad
schreiben, `.env` lesen, `AGENTS.md` schreiben) verhalten sich sämtlich richtig – der Hook wirkt,
und die Abweichungen sind Abweichungen, kein toter Hook.

| Gruppe | Fälle | Abweichungen |
|---|---|---|
| Positiv- und Negativkontrollen | 6 | 0 |
| Eingabeschema (Abschnitt 2.1, 3) | 12 | **11** |
| Unbekannte Werkzeugnamen (Abschnitt 2.2) | 5 | **5** |
| Groß-/Kleinschreibung (Abschnitt 2.3) | 4 | **4** |
| Pfadformen, die richtig entschieden werden | 8 | 0 |
| Umschlagfelder (Abschnitt 5, 6) | 6 | **1** |

Die Skripte der vier Messreihen liegen **nicht** im Repositorium – sie sind Wegwerfwerkzeug und
jederzeit aus diesem Protokoll neu baubar. Was bleibt, sind die Sonden in
`tests/scripts/probe-pruefungen.py` und die Prüfung, die sie belegen.

## 8. Was diese Gegenprüfung nicht belegt

- **Sie belegt nichts für `devin-desktop` in der Gegenrichtung.** Dessen aufgezeichnete Eingaben
  führen `hook_event_name`, `prompt_id`, `session_id`, `tool_input`, `tool_name`, `tool_use_id` –
  **kein `transcript_path`, kein `cwd`**. Die fünf Aufzeichnungen laufen sämtlich richtig durch.
  Dass dieses Pack den Fehler nicht zeigt, ist eine Eigenschaft seines Schemas, **keine
  Eigenschaft des Hooks**; sendet es morgen ein Pfadfeld im Umschlag, trifft ihn dasselbe.
- **Sie belegt keinen Schreibversuch über die Shell.** Der Kernschutz für `exec` besteht
  unverändert nicht (B04, D-47); daran ändert diese Prüfung nichts und der kommende Umbau ebenso
  wenig. **K-32 bleibt damit offen** – der Selbstanwendungsweg über die Shell wird hier nicht
  geschlossen.
- **Sie belegt die Wirkung der Junction nur unter NTFS.** Symbolische Verknüpfungen unter Linux und
  macOS sind **nicht** gemessen; die Auflösung sollte dort gleich wirken, das ist Erwartung, nicht
  Messung.
- **Sie belegt keine Zeitlücke.** Dass zwischen Prüfung und Zugriff eine Verknüpfung umgebogen
  werden kann, ist Mechanik und wird benannt, nicht gemessen. Ein Hook kann das nicht ausschließen;
  dafür braucht es die Isolationsschicht des Betriebssystems (Paket 6, `CR-2026-047` E5).
- **Sie belegt nicht, dass ein Client den Matcher einhält.** Dass ein unbekannter Werkzeugname den
  Hook überhaupt erreicht, ist bei `claude-code` unwahrscheinlich, weil der Matcher aus
  `hook_tools` erzeugt wird. Das ist aber eine **Clientzusage** – genau die Art unbelegter Annahme,
  an der AP2-CC-13 acht Releases lang hing (D-31). Der Hook darf sich nicht darauf stützen.

## 9. Gegenzeichnung

| Rolle | Name/Kennung | Datum | Ergebnis bestätigt |
|---|---|---|---|
| `<FRAMEWORK_OWNER>` | `<TBD>` | `<TBD>` | `<TBD>` |
