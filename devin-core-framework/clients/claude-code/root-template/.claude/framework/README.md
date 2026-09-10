# `.claude/framework/` – Regeltexte für Claude Code

Dieses Verzeichnis enthält die Laufzeitfassung der Framework-Regeln für das Client Pack `claude-code`. Die kanonische, werkzeugneutrale Langform liegt in `devin-core-framework/framework/`. Bei Widersprüchen gilt die Langform; die Laufzeitfassung wird dann korrigiert.

**Die Regeltexte sind inhaltlich identisch zu denen anderer Client Packs.** Abweichend ist ausschließlich der Lademechanismus.

## Mechanismus (Belegstatus)

| Aussage | Status |
|---|---|
| `CLAUDE.md` im Wurzelverzeichnis wird zu Beginn jeder Sitzung geladen | `[DOK]` |
| `CLAUDE.md` kann weitere Dateien über `@pfad/zur/datei` einbinden; der Inhalt wird mitgeladen | `[DOK]` |
| Eine `CLAUDE.md` in einem Unterverzeichnis wird beim Zugriff auf dieses Verzeichnis geladen | `[DOK]` |
| Dateien in diesem Verzeichnis werden **nicht** von sich aus geladen – nur über einen Import | `[KONZ]` Framework-Konvention |
| Es gibt keine Ladetrigger und keine Bindung von Regeln an Dateimuster | `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>` |
| Zeichenlimit für die Wurzel-Anweisung und ihre Importe | kein Limit dokumentiert; `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>` |

## Nummernschema und Ebenenzuordnung (Framework-Konvention `[KONZ]`)

Das Schema ist über alle Client Packs gleich, damit eine Regel beim Wechsel des Clients wiedererkennbar bleibt.

| Präfix | Ebene der Prioritätshierarchie | Ladeweg bei diesem Client | Pflege |
|---|---|---|---|
| `00-` | 3 Framework Core | Import in `CLAUDE.md` | Framework Owner |
| `10-` | 3 Framework Core (Datenschutz/Sicherheit) | Import in `CLAUDE.md` | Framework Owner |
| `15-` | 3 Framework Core (Entwicklungsregeln) | Import in `CLAUDE.md` | Framework Owner |
| `20-` | 4 Project Overlay | Import in `CLAUDE.md` | Projekt (Overlay Owner) |
| `30-` | 6 Role Packs | Import in `CLAUDE.md` | Modul-Owner |
| `40-` | 5 Technology Packs | verschachtelte `CLAUDE.md` oder Import – siehe `../README.md` | Modul-Owner |

Die Nummern bilden die Ladereihenfolge im Dateisystem ab, nicht die Priorität. Die Priorität regelt `CLAUDE.md` Abschnitt 2 beziehungsweise `devin-core-framework/governance/PRIORITY_HIERARCHY.md`.

## Was das Fehlen der Ladetrigger bedeutet

Bei Clients mit Ladetriggern laden `10-` und `15-` nur, wenn die Aufgabe sie berührt. Hier sind sie **immer** geladen.

- **Für die Regelwirkung:** eine Verschärfung. Mehr Regeln sind aktiv, nicht weniger.
- **Für den Kontext:** rund 22.000 Zeichen sind ständig belegt (`CLAUDE.md` und die vier importierten Regeltexte zusammen). Das Prinzip Least Context wird damit schwächer eingehalten als bei einem Client mit Ladetriggern. Least Context ist ein Prinzip zur Ergebnisqualität, keine Sicherheitszusage – die Abweichung ist deshalb vertretbar und in `CLIENT_PACK.md` Zeile R2 ausgewiesen.

Wächst der ständige Kontext durch aktivierte Packs deutlich, ist zu prüfen, ob ein Pack besser über eine verschachtelte `CLAUDE.md` gebunden wird.

## Regeln für dieses Verzeichnis

- Änderungen an `00-`, `10-`, `15-` nur über einen Framework-Änderungsantrag; `20-` über den Overlay-Prozess des Projekts; `30-`, `40-` über den jeweiligen Modul-Owner.
- Eine hier abgelegte Datei wirkt erst, wenn sie in `CLAUDE.md` importiert oder in einer verschachtelten `CLAUDE.md` eingebunden ist. Eine Datei ohne Einbindung ist wirkungslos – anders als bei Clients mit Ladetriggern, wo das Frontmatter allein genügt.
- Dateien mit Endung `.template` sind Vorlagen und werden nicht eingebunden.
