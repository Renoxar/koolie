# Änderungsantrag `CR-2026-029`

| Feld | Inhalt |
|---|---|
| Titel | Die Hook-Konfiguration des Packs `devin-desktop` liegt in einer Datei, die der Client nicht liest |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-11 |
| Betroffene Artefakte | `clients/devin-desktop/manifest.json`, `clients/devin-desktop/CLIENT_PACK.md` (H1–H3), `clientmap.py`, `install.py`, `tests/scripts/validate-framework.py` (Prüfung 15 und 17), `docs/PLACEHOLDER_REGISTRY.md` |
| Ebene laut Entscheidungsbaum 6 | Client Pack und Abbildung; Schutzmechanismus |
| Art | Behebung von `AP2-DD-10` (Schwere: **hoch**) |
| Dringlichkeit | **erhöht** – drei Zusagen der Fähigkeitsmatrix sind wirkungslos |

## 1. Anlass und Problem

Das Pack legt die Hook-Konfiguration nach `.devin/hooks.v1.json`. Aus dieser Datei führt
Devin **keinen Hook aus**. Gemessen mit einem Aufzeichnungs-Hook, der jede Eingabe
wegschreibt und nie blockiert (Devin CLI 3000.10.21):

| Konfiguration | Hook-Aufrufe |
|---|---|
| `.devin/hooks.v1.json`, Kommando mit `$DEVIN_PROJECT_DIR` | **0** |
| `.devin/hooks.v1.json`, Kommando mit absolutem Pfad | **0** |
| `.devin/hooks.v1.json`, Matcher leer – trifft jedes Werkzeug | **0** |
| dieselben Hooks in `.devin/config.json` unter `"hooks"` | **sofort ausgelöst** |

Der Unterschied ist allein der **Ort**. Kommando, Matcher, Schema und Interpreter sind in
allen vier Zeilen identisch.

**Damit sind H1, H2 und H3 wirkungslos:** keine Prüfung vor der Werkzeugausführung, keine
Blockierung, keine Overlay-Statusmeldung beim Sitzungsstart. Die Matrix führt H1 und H3 als
`[TECHNISCH]` mit Beleg `[DOK]`.

### Warum das keine falsche Dokumentation ist

Die Hook-Dokumentation nennt `.devin/hooks.v1.json` ausdrücklich als Projektort – neben
`.devin/config.json`, `.devin/config.local.json` und weiteren. Die Angabe des Packs folgt
also der Dokumentation. **Belegt war die Dokumentation, nicht das Verhalten** – derselbe
Befundtyp wie `AP2-CC-13` und `FW-KO-01`, und genau der, gegen den D-23 gerichtet ist.

Ob der Ort im **Desktop** gelesen wird, ist offen; die Messung stammt aus der CLI. Das ist
eine der drei Gegenproben des AP2-Protokolls. Für die Entscheidung ist das nachrangig: Ein
Ort, der bei einem der beiden Frontends nicht trägt, ist als Ablage ungeeignet.

### Warum die Prüfungen es nicht fanden

Prüfung 15 (Interpreter) und Prüfung 17 (fail-closed) lesen die Hook-Kommandos **aus der
erzeugten Konfiguration** und rufen sie selbst auf. Sie belegen damit, dass das Kommando
funktioniert – nicht, dass der Client die Datei je liest. Die Kette hat ein Glied mehr, als
die Prüfungen sehen: Manifest → Abbildung → Datei → **Client liest sie** → Aufruf.

Dieses Glied lässt sich nur mit einer laufenden Sitzung prüfen. Genau das ist AP2.

## 2. Vorgeschlagene Änderung

**Die Hooks des Packs `devin-desktop` wandern in `.devin/config.json` unter den Schlüssel
`"hooks"`** – den Ort, an dem sie nachweislich ausgeführt werden. Der Mechanismus dafür
existiert bereits: Für `claude-code` bettet `render_permissions()` die Hooks in die
Berechtigungsdatei ein, weil dieser Client keine eigene Hook-Datei kennt
(`hooks_in_permissions()`). Bei `devin-desktop` ist die Lage nach dieser Messung dieselbe –
die Abbildung muss das nur sagen.

Konkret entfällt die Zuordnung `<HOOKS_FILE>` → `.devin/hooks.v1.json` aus der
Platzhalterabbildung, womit `hooks_in_permissions()` für dieses Pack wahr wird.

**Der Validator prüft künftig das fehlende Glied.** Eine Prüfung kann nicht feststellen, ob
ein Client eine Datei liest – das kann nur eine Sitzung. Sie kann aber feststellen, **ob die
Hook-Konfiguration an einem Ort steht, der für dieses Pack als wirksam belegt ist**. Der
Beleg gehört ins Manifest, mit Fundstelle auf das Protokoll, und die Prüfung hält die
Konfiguration dagegen.

Das ist bewusst schwächer als eine Wirkungsprüfung, und der Antrag sagt das: Es ist eine
Konsistenzprüfung gegen einen Beleg, kein Nachweis. Ein Nachweis bleibt der Sitzungstest.

## 3. Was dieser Antrag nicht ändert

- **`claude-code`.** Dort liegen die Hooks bereits in der Berechtigungsdatei und laufen
  nachweislich (`AP2-CC-13`, Prüfung 15).
- **Den Hook selbst.** `hook-check-secrets.py` und `hook-overlay-status.py` bleiben
  unverändert. Sie waren nie das Problem – sie wurden nur nie aufgerufen.
- **Die Kernquelle.** `framework/runtime/hooks.json` bleibt, wie sie ist; sie beschreibt,
  *was* konfiguriert wird, nicht *wohin*.

## 4. Grenze der Zusage

**Gemessen wurde die CLI, nicht der Desktop.** Sollte der Desktop `hooks.v1.json` lesen, wäre
die Verlagerung trotzdem richtig – ein Ort, der für beide trägt, ist einem vorzuziehen, der
nur für eines trägt. Ergibt die Gegenprobe, dass auch `config.json` im Desktop nicht gelesen
wird, ist H1 bis H3 dort als `[NICHT ABBILDBAR]` zu führen; dieser Antrag deckt diesen Fall
**nicht** ab.

**Eine Folge ist auszuweisen:** Liegen die Hooks in `config.json`, teilen sie deren Schicksal
als Saat – `install.py --update` fasst sie dann nicht mehr an, wie schon bei `claude-code`.
Eine Änderung an den Hooks des Kerns erreicht ein bestehendes Projekt nicht mehr von selbst.
Das ist der Preis und gehört in die Migrationshinweise.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Ort wechseln oder auf Herstellerkorrektur warten? | **Wechseln.** Drei Zusagen sind wirkungslos; ein Schutzmechanismus, der nicht läuft, ist schlimmer als ein fehlender (D-29) | Die Hooks werden Teil der Saat und sind beim Release-Wechsel von Hand nachzuziehen |
| E2 | Vor der Gegenprobe im Desktop entscheiden? | **Ja.** Der belegte Ort trägt in beiden Fällen; der unbelegte in mindestens einem nicht | Sollte der Desktop abweichen, ist erneut zu messen |
| E3 | Prüfung auf Ort oder auf Wirkung? | **Auf den Ort, gegen einen im Manifest hinterlegten Beleg.** Ob ein Client eine Datei liest, kann kein Validator feststellen | Eine Konsistenzprüfung, die als solche zu kennzeichnen ist – sie belegt nichts, sie hält einen Beleg fest |
| E4 | H1/H3 bis zur Gegenprobe herabstufen? | **Ja, auf `[TEXTUELL]`** mit Verweis auf dieses Protokoll | Das Pack weist zwei technische Zusagen weniger aus |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | `<TBD: angenommen / abgelehnt / mit Auflagen>` |
| Datum | `<TBD>` |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | `<TBD: E1 bis E4 einzeln entscheiden>` |
