# `.claude/rules/` – Regeltexte für Claude Code

Dieses Verzeichnis enthält die Laufzeitfassung der Framework-Regeln für das Client Pack `claude-code`. Die kanonische, werkzeugneutrale Langform liegt in `leitwerk-core/framework/`. Bei Widersprüchen gilt die Langform; die Laufzeitfassung wird dann korrigiert.

**Die Regeltexte sind inhaltlich identisch zu denen anderer Client Packs.** Abweichend ist ausschließlich, wie die Ladebedingung notiert wird.

## Mechanismus (Belegstatus)

| Aussage | Status |
|---|---|
| `CLAUDE.md` im Wurzelverzeichnis wird zu Beginn jeder Sitzung geladen | `[DOK]` |
| Jede `.md`-Datei in diesem Verzeichnis wird gefunden, auch in Unterverzeichnissen | [DOK] (AP2, Clientversion 2.1.267) |
| Eine Regeldatei **ohne** `paths`-Feld wird beim Sitzungsstart unbedingt geladen – ohne Import | [DOK] (AP2, Clientversion 2.1.267) |
| Eine Regeldatei **mit** `paths`-Feld lädt, sobald der Client eine Datei liest, die auf eines der Glob-Muster passt | [DOK] (AP2, Clientversion 2.1.267) |
| `paths` nimmt mehrere Muster; Klammer-Expansion (`{ts,tsx}`) ist zulässig | [DOK] (AP2, Clientversion 2.1.267) |
| `description` ist für Regeldateien **nicht** dokumentiert und steht deshalb nicht im Frontmatter (K-18) | [DOK] (AP2, Clientversion 2.1.267) |
| Zeichenlimit der Wurzel-Anweisung: 4 MiB je Datei; darüber wird sie übersprungen. Empfehlung: unter 200 Zeilen | [DOK] (AP2, Clientversion 2.1.267) |

Bis Framework-Release 0.14.0 lag diese Ablage unter `.claude/framework/` und wurde über `@pfad`-Importe in `CLAUDE.md` geladen. Der Grund dafür – „dieser Client kennt keine Ladebedingungen" – war falsch (AP2-CC-03).

## Frontmatter

```markdown
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
---
```

Nur das Feld `paths` ist zulässig, und nur bei Regeln, die an Dateimuster gebunden sind. Eine Regel ohne Frontmatter lädt unbedingt. Der Validator meldet jedes andere Feld – insbesondere ein aus der Kernquelle stehen gebliebenes `trigger:` oder `globs:`, das dieser Client nicht auswertet.

Der erzeugte HTML-Kommentar oberhalb des Regeltextes nennt Zweck, Ladeverhalten und den Ladetrigger der Kernquelle. Für `CLAUDE.md`-Dateien ist dokumentiert, dass Block-Kommentare vor dem Einspeisen entfernt werden; für Regeldateien ist das **nicht** dokumentiert. Der Kommentar ist deshalb knapp gehalten und zählt hier vorsorglich zum ständigen Kontext.

## Abbildung der Ladetrigger

Die Kernquelle kennt drei Ladetrigger, dieser Client eine Bedingung. Was womit abgebildet wird, steht maschinenlesbar in `leitwerk-core/clients/claude-code/manifest.json` unter `rule_triggers`:

| Ladetrigger der Kernquelle | Fassung hier | Ladeverhalten |
|---|---|---|
| `always_on` | kein `paths`-Feld | bei jedem Sitzungsstart |
| `model_decision` | kein `paths`-Feld | bei jedem Sitzungsstart – **Verschärfung**, siehe unten |
| `glob` mit `globs: "<Muster>"` | `paths:` mit denselben Mustern | sobald der Client eine passende Datei liest |

Ein Ladetrigger ohne Eintrag in dieser Abbildung lässt die Installation scheitern; er wird nicht stillschweigend verworfen (D-26, D-27).

## Nummernschema und Ebenenzuordnung (Framework-Konvention `[KONZ]`)

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

## Was die Abbildung von `model_decision` bedeutet

Bei Clients mit einer modellentschiedenen Ladebedingung laden `10-` und `15-` nur, wenn die Aufgabe sie berührt. Hier sind sie **immer** geladen, weil dieser Client für Regeldateien nur die Bedingung über Dateimuster kennt.

- **Für die Regelwirkung:** eine Verschärfung. Mehr Regeln sind aktiv, nicht weniger.
- **Für den Kontext:** rund 25.000 Zeichen sind ständig belegt (`CLAUDE.md` und die vier unbedingten Regeltexte einer frischen Installation zusammen). Das Prinzip Least Context wird damit schwächer eingehalten als bei einem Client mit modellentschiedener Bedingung. Least Context ist ein Prinzip zur Ergebnisqualität, keine Sicherheitszusage – die Abweichung ist deshalb vertretbar und in `CLIENT_PACK.md` Zeile R2 ausgewiesen.

Wächst der ständige Kontext durch aktivierte Packs deutlich, ist zu prüfen, ob ein Pack an Dateimuster gebunden werden kann. Der Validator warnt, sobald die unbedingt geladenen Texte zusammen 40.000 Zeichen überschreiten.

## Grenzen dieser Ablage

- **Eine pfadgebundene Regel lädt beim Lesen einer passenden Datei, nicht bei jedem Werkzeugaufruf.** Sie steht also nicht schon zu Beginn der Aufgabe im Kontext. Für Regeln, die vor der ersten Dateiberührung gelten müssen, ist `paths` deshalb ungeeignet – sie bleiben unbedingt.
- **Eine Kernregel darf nicht an Dateimuster gebunden werden.** `00-`, `10-`, `15-` und `20-` gelten für jede Aufgabe; ein `paths`-Feld dort wäre eine Lockerung. Der Validator meldet es als Fehler.
- **Ein ungültiges Muster trifft nichts.** Glob liest `[` als Beginn eines Klammerausdrucks; `photos [2024/**` ist ungültig und trifft keine Datei, während die übrigen Muster derselben Regel weiter wirken. Ein literales `[` wird als `\[` geschrieben.
- **Klammer-Expansion hat ein Budget.** Die `paths`-Liste einer Regel teilt sich 1.000 expandierte Muster und 4 MiB; ein Muster darüber wird unexpandiert verwendet und trifft dann nichts.
- **Nutzerlokal ausschließbar.** `claudeMdExcludes` in `.claude/settings.local.json` kann Regeldateien über ein Glob-Muster vom Laden ausnehmen. Das ist eine **Lockerung** und damit im Framework unzulässig (B9); technisch verhindert wird sie nicht. Der KI-Client selbst kann die Datei nicht schreiben – `Edit(.claude/**)` steht in `deny` –, ein Mensch schon.

## Regeln für dieses Verzeichnis

- Änderungen an `00-`, `10-`, `15-` nur über einen Framework-Änderungsantrag; `20-` und `2N-` über den Overlay-Prozess des Projekts; `30-`, `40-` über den jeweiligen Modul-Owner.
- Eine hier abgelegte Datei wirkt ohne weiteres Zutun. Eine Regel, die nicht wirken soll, gehört nicht in dieses Verzeichnis.
- Dateien mit Endung `.template` sind Vorlagen; sie enden nicht auf `.md` und werden deshalb nicht geladen.
