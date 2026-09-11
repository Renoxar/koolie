# `.claude/` – Laufzeitschicht für Claude Code

Dieses Verzeichnis enthält alles, was Claude Code aus dem Repository liest. Es ist die einzige clientspezifische Schicht des Frameworks (Tool Independence). Alle Inhalte sind Konkretisierungen der werkzeugneutralen Regeln in `leitwerk-core/framework/`.

Die Durchsetzungstiefe – welche Zusage dieser Client technisch erzwingt und welche nur als Anweisung im Kontext steht – ist in der Fähigkeitsmatrix des Client Packs ausgewiesen: `leitwerk-core/clients/claude-code/CLIENT_PACK.md`.

| Datei / Verzeichnis | Zweck | Belegstatus |
|---|---|---|
| `rules/*.md` | Regeltexte (Core, Overlay, Packs); werden vom Client selbst geladen – ohne `paths`-Feld unbedingt, mit `paths`-Feld bei passenden Dateien | [DOK] (AP2, Clientversion 2.1.267) |
| `skills/<name>/SKILL.md` | Skills, Aufruf über den Namen mit vorangestelltem Schrägstrich; Frontmatter `name`, `description`, `argument-hint`, `allowed-tools` | `[DOK]` |
| `agents/<name>.md` | Subagentenprofile (hier: nur lesender Reviewer); Frontmatter `name`, `description`, `tools` (ergänzend `disallowedTools`) | [DOK] (AP2, Clientversion 2.1.267) |
| `settings.json` | Berechtigungen `deny` / `ask` / `allow` **und** Hooks (projektweit, versioniert). Erzeugt aus `leitwerk-core/framework/runtime/permissions.json` und `hooks.json`; hier trägt das Projekt nur die Platzhalterwerte ein | `[DOK]` Mechanismus; Regelmenge `[EMPF]`; Mustersemantik [DOK] (AP2, Clientversion 2.1.267) – gitignore-Syntax; **Pfadregeln wertet dieser Client nur für `Read` und `Edit` aus** |
| `settings.local.json` (nicht versioniert) | persönliche Überschreibungen; im Framework nur zum Verschärfen zulässig | `[DOK]` |

Im Wurzelverzeichnis liegen außerdem `CLAUDE.md` (Wurzel-Anweisung) und `.mcp.json.example` (Vorlage für MCP-Server; Standard: keine). Die Wurzel-Anweisung bindet die Regeltexte **nicht** ein; sie liegen in `rules/` und werden von dort geladen.

## Zwei Unterschiede zur Fassung anderer Client Packs

Die **Regeltexte sind inhaltlich identisch**. Abweichend ist nur, wie ihre Ladebedingung notiert wird.

1. **Eine Bedingung statt dreier Ladetrigger.** Die Kernquelle kennt `always_on`, `model_decision` und `glob`; dieser Client kennt für Regeldateien nur die Bindung an Dateimuster (`paths`). `always_on` und `model_decision` werden deshalb beide auf unbedingtes Laden abgebildet, `glob` auf `paths`. Für `model_decision` ist das eine Verschärfung, keine Lockerung – es kostet Kontext (rund 25.000 Zeichen einschließlich `CLAUDE.md`), senkt aber kein Schutzniveau. Einzelheiten: Abschnitt „Regelablage" weiter unten.

2. **Hooks stehen in `settings.json`**, nicht in einer eigenen Datei.

Bis Framework-Release 0.14.0 stand hier ein dritter Unterschied – „Schreibschutz braucht zwei Regeln je Pfad". Er galt nie: Dieser Client wertet Pfadregeln ausschließlich für `Read` und `Edit` aus (AP2-CC-02, D-26).

## Technology Packs

Ein Technology Pack (Ebene 5) lädt über ein Dateimuster – etwa nur bei Java-Dateien. Dieser Client bildet das nativ ab: Die Laufzeitfassung des Packs liegt als `rules/40-tech-<name>.md` mit `paths:` und den Dateimustern der Technologie. Sie lädt, sobald der Client eine passende Datei liest.

Zu beachten: Die Regel steht damit nicht schon zu Beginn der Aufgabe im Kontext, sondern erst nach der ersten Berührung einer passenden Datei. Ein Pack, dessen Regeln vorher gelten müssen, bleibt unbedingt geladen. Details: Abschnitt „Regelablage" weiter unten und `CLIENT_PACK.md` Abschnitt 5.

## Berechtigungsmodi und Framework-Vorgabe

| Modus | Verhalten | Framework-Vorgabe |
|---|---|---|
| `default` | Lesen automatisch; Schreiben und Befehle fragen | **Standard** für alle Kontrollstufen |
| `acceptEdits` | Dateiänderungen automatisch; Befehle fragen | nur Kontrollstufe niedrig, nur mit Overlay-Freigabe |
| `plan` | nur Analyse und Planung, keine Änderungen | zulässig; entspricht M1/M2 |
| `bypassPermissions` | alles automatisch | **untersagt** (D-05) |

## Regelablage (`rules/`)

Die Regelablage enthält die Laufzeitfassung der Framework-Regeln. Die kanonische, werkzeugneutrale Langform liegt in `leitwerk-core/framework/`. Bei Widersprüchen gilt die Langform; die Laufzeitfassung wird dann korrigiert. **Die Regeltexte sind inhaltlich identisch zu denen anderer Client Packs.** Abweichend ist ausschließlich, wie die Ladebedingung notiert wird.

> **Warum dieser Abschnitt hier steht und nicht in `rules/`.** Bis 0.25.0 lag dort eine eigene README. Dieser Client lädt **jede** `.md`-Datei der Regelablage unbedingt – gemessen am 2026-09-11: Die Sitzung führte die Datei samt Inhaltsangabe in ihrem geladenen Bestand auf (K-26). Ein erklärender Text mit Belegvorbehalten hatte damit einen dauerhaften Platz im Kontext. Seit 0.26.0 gilt: **Die Regelablage enthält ausschließlich Regeln** (D-36).

### Mechanismus (Belegstatus)

| Aussage | Status |
|---|---|
| `CLAUDE.md` im Wurzelverzeichnis wird zu Beginn jeder Sitzung geladen | `[DOK]` |
| Jede `.md`-Datei in diesem Verzeichnis wird gefunden, auch in Unterverzeichnissen | [DOK] (AP2, Clientversion 2.1.267) |
| Eine Regeldatei **ohne** `paths`-Feld wird beim Sitzungsstart unbedingt geladen – ohne Import | [DOK] (AP2, Clientversion 2.1.267) |
| Eine Regeldatei **mit** `paths`-Feld lädt, sobald der Client eine Datei liest, die auf eines der Glob-Muster passt | [DOK] (AP2, Clientversion 2.1.267) |
| `paths` nimmt mehrere Muster; Klammer-Expansion (`{ts,tsx}`) ist zulässig | [DOK] (AP2, Clientversion 2.1.267) |
| `description` ist für Regeldateien **nicht** dokumentiert und steht deshalb nicht im Frontmatter (K-18) | [DOK] (AP2, Clientversion 2.1.267) |
| Zeichenlimit der Wurzel-Anweisung: 4 MiB je Datei; darüber wird sie übersprungen. Empfehlung: unter 200 Zeilen | [DOK] (AP2, Clientversion 2.1.267) |
| **Ein HTML-Kommentar erreicht die Sitzung nicht.** Dieselbe Messmarke blieb unsichtbar, solange sie in Kommentarklammern stand, und war im Klartext sofort da – in der Wurzel-Anweisungsdatei **und** in der Regelablage | in einer Sitzung erhoben (2026-09-11, ERH-01) |

Bis Framework-Release 0.14.0 lag diese Ablage unter `.claude/framework/` und wurde über `@pfad`-Importe in `CLAUDE.md` geladen. Der Grund dafür – „dieser Client kennt keine Ladebedingungen" – war falsch (AP2-CC-03).

### Frontmatter

Nur das Feld `paths` ist zulässig, und nur bei Regeln, die an Dateimuster gebunden sind; es nimmt eine Liste von Glob-Mustern. Eine Regel ohne Frontmatter lädt unbedingt. Der Validator meldet jedes andere Feld – insbesondere ein aus der Kernquelle stehen gebliebenes `trigger:` oder `globs:`, das dieser Client nicht auswertet.

Der erzeugte HTML-Kommentar oberhalb des Regeltextes nennt Zweck, Ladeverhalten und den Ladetrigger der Kernquelle. **Er ist die Auskunft an den Menschen, der die Datei öffnet; in den Kontext geht er bei diesem Client nicht** – gemessen am 2026-09-11 (ERH-01). Deshalb steht dort Herkunft und keine Anweisung: Ein normativer Satz im Kommentar wäre eine Regel, die niemanden erreicht (D-38). Prüfung 23 meldet normative Schlüsselwörter in solchen Kommentaren.

### Abbildung der Ladetrigger

Die Kernquelle kennt drei Ladetrigger, dieser Client eine Bedingung. Was womit abgebildet wird, steht maschinenlesbar in `leitwerk-core/clients/claude-code/manifest.json` unter `rule_triggers`:

| Ladetrigger der Kernquelle | Fassung hier | Ladeverhalten |
|---|---|---|
| `always_on` | kein `paths`-Feld | bei jedem Sitzungsstart |
| `model_decision` | kein `paths`-Feld | bei jedem Sitzungsstart – **Verschärfung**, siehe unten |
| `glob` mit Mustern | `paths:` mit denselben Mustern | sobald der Client eine passende Datei liest |

Ein Ladetrigger ohne Eintrag in dieser Abbildung lässt die Installation scheitern; er wird nicht stillschweigend verworfen (D-26, D-27).

### Nummernschema und Ebenenzuordnung (Framework-Konvention `[KONZ]`)

Das Schema ist über alle Client Packs gleich, damit eine Regel beim Wechsel des Clients wiedererkennbar bleibt.

| Präfix | Ebene der Prioritätshierarchie | Ladebedingung hier | Pflege |
|---|---|---|---|
| `00-` | 3 Framework Core | unbedingt | Framework Owner |
| `10-` | 3 Framework Core (Datenschutz/Sicherheit) | unbedingt | Framework Owner |
| `15-` | 3 Framework Core (Entwicklungsregeln) | unbedingt | Framework Owner |
| `20-` | 4 Project Overlay | unbedingt | Projekt (Overlay Owner) |
| `2N-` | 4 Overlay-Regelerweiterungen | je Vorlage; `paths` zulässig | Projekt (Overlay Owner) |
| `30-` | 6 Role Packs | unbedingt | Modul-Owner |
| `40-` | 5 Technology Packs | `paths` mit den Dateimustern der Technologie | Modul-Owner |

Die Nummern bilden die Ladereihenfolge im Dateisystem ab, nicht die Priorität. Die Priorität regelt `CLAUDE.md` Abschnitt 2 beziehungsweise `leitwerk-core/governance/PRIORITY_HIERARCHY.md`.

### Was die Abbildung von `model_decision` bedeutet

Bei Clients mit einer modellentschiedenen Ladebedingung laden `10-` und `15-` nur, wenn die Aufgabe sie berührt. Hier sind sie **immer** geladen, weil dieser Client für Regeldateien nur die Bedingung über Dateimuster kennt.

- **Für die Regelwirkung:** eine Verschärfung. Mehr Regeln sind aktiv, nicht weniger.
- **Für den Kontext:** rund 25.000 Zeichen sind ständig belegt (`CLAUDE.md` und die vier unbedingten Regeltexte einer frischen Installation zusammen). Das Prinzip Least Context wird damit schwächer eingehalten als bei einem Client mit modellentschiedener Bedingung. Least Context ist ein Prinzip zur Ergebnisqualität, keine Sicherheitszusage – die Abweichung ist deshalb vertretbar und in `CLIENT_PACK.md` Zeile R2 ausgewiesen.

Wächst der ständige Kontext durch aktivierte Packs deutlich, ist zu prüfen, ob ein Pack an Dateimuster gebunden werden kann. Der Validator warnt, sobald die unbedingt geladenen Texte zusammen 40.000 Zeichen überschreiten.

### Grenzen dieser Ablage

- **Eine pfadgebundene Regel lädt beim Lesen einer passenden Datei, nicht bei jedem Werkzeugaufruf.** Sie steht also nicht schon zu Beginn der Aufgabe im Kontext. Für Regeln, die vor der ersten Dateiberührung gelten müssen, ist `paths` deshalb ungeeignet – sie bleiben unbedingt.
- **Eine Kernregel darf nicht an Dateimuster gebunden werden.** `00-`, `10-`, `15-` und `20-` gelten für jede Aufgabe; ein `paths`-Feld dort wäre eine Lockerung. Der Validator meldet es als Fehler.
- **Ein ungültiges Muster trifft nichts.** Glob liest eine öffnende eckige Klammer als Beginn eines Klammerausdrucks; ein unausgeglichenes Muster trifft keine Datei, während die übrigen Muster derselben Regel weiter wirken. Eine literale Klammer wird mit vorangestelltem Rückstrich geschrieben.
- **Klammer-Expansion hat ein Budget.** Die `paths`-Liste einer Regel teilt sich 1.000 expandierte Muster und 4 MiB; ein Muster darüber wird unexpandiert verwendet und trifft dann nichts.
- **Nutzerlokal ausschließbar.** `claudeMdExcludes` in `.claude/settings.local.json` kann Regeldateien über ein Glob-Muster vom Laden ausnehmen. Das ist eine **Lockerung** und damit im Framework unzulässig (B9); technisch verhindert wird sie nicht. Der KI-Client selbst kann die Datei nicht schreiben – eine Verweigerungsregel auf die Laufzeitschicht steht in `deny` –, ein Mensch schon. Dasselbe Feld ist zugleich der Weg, eine Anweisungsdatei **außerhalb** des Projekts auszuschließen; das Framework liefert dafür keine Vorgabe aus (Zeile R6, D-37).

### Regeln für die Regelablage

- **Dort liegt nur, was Regel ist.** Ein erklärender Text gehört hierher, nicht dorthin (D-36). Der Validator meldet eine Datei in der Vorlage der Regelablage, die dem Nummernschema nicht folgt.
- Änderungen an `00-`, `10-`, `15-` nur über einen Framework-Änderungsantrag; `20-` und `2N-` über den Overlay-Prozess des Projekts; `30-`, `40-` über den jeweiligen Modul-Owner.
- Eine dort abgelegte Datei wirkt ohne weiteres Zutun. Eine Regel, die nicht wirken soll, gehört nicht in dieses Verzeichnis.
- Dateien mit Endung `.template` sind Vorlagen; sie enden nicht auf `.md` und werden deshalb nicht geladen.

**Migration aus einer Installation vor 0.26.0:** `install.py --update` legt diese Fassung an, **löscht die alte README der Regelablage aber nicht.** Sie ist von Hand zu entfernen; solange sie liegt, lädt sie unbedingt mit.

## Validierung

```text
python leitwerk-core/tests/scripts/validate-framework.py
```
