# Begriffe der Laufzeitschicht

| Attribut | Wert |
|---|---|
| ID | `FW-DOC-GLOSSARY` |
| Version | `0.5.0` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |

## Zweck

Der Kern des Frameworks ist werkzeugneutral. Er nennt deshalb keine Pfade, die nur bei einem einzigen KI-Client existieren.

Diese Datei legt die Begriffe fest, mit denen der Kern die Bestandteile der Laufzeitschicht bezeichnet, und bildet sie auf die Pfade je Client Pack ab. Das Platzhalterregister ist das Gegenstück: Dort stehen projektspezifische Werte, hier clientspezifische Pfade.

## Regel

- Im Kern (`.koolie/core/framework/`, `governance/`, `checklists/`, `prompts/`, `decision-trees/`, `onboarding/`, `docs/`, `templates/`, `examples/`, `tests/`) steht ausschließlich der **Begriff**.
- In einem Client Pack (`.koolie/core/clients/<client>/`) steht der **Pfad**.
- In historischen Dokumenten bleiben genannte Pfade unverändert; sie beschreiben einen vergangenen Zustand.

### Die vier Ausnahmen, vollständig

Die Regel gilt für jeden Träger des Kerns. Ausgenommen ist genau, was hier steht.

| Gattung | Träger | Warum |
|---|---|---|
| **Chronik** | `CHANGELOG.md`, `governance/change-requests/`, `governance/DECISION_LOG.md`, `tests/protocols/`, `docs/ROADMAP.md` | Sie berichten einen vergangenen Stand. Die Roadmap gehört dazu, weil sie die Erhebungsergebnisse je Arbeitspaket und die Befundberichte je Release führt |
| **Werkzeuge** | alle `.py` des Kerns | Ein Skript, das eine Installation herstellt oder prüft, muss Pfade nennen. `install.py` und `clientmap.py` lösen sie aus den Manifesten auf, die Prüfskripte stellen Installationen her |
| **Abbildungstabellen** | diese Datei, `docs/PLACEHOLDER_REGISTRY.md`, `clients/` | Sie müssen beide Namen nennen; dort ist der Pfad der Inhalt |
| **Anhänge und Chronik des Hauptdokuments** | `build/doc/29-grenzen.md`, `build/doc/31-anhaenge.md`, `build/doc/32-abschluss.md` | Die übrigen Kapitelquellen unter `build/doc/` stehen unter der Regel. Diese drei Träger haben einen dauerhaften Grund: `29-grenzen.md` ist ein ausdrückliches Zeitdokument des Stands vom 2026-09-01, `31-anhaenge.md` führt die Quellenliste je Client Pack und den Verifikationsbedarf eines Packs – dieselbe Gattung wie die Abbildungstabellen –, und `32-abschluss.md` trägt die Releasechronik samt den Aussagen des Auftrags über die Produktnennung selbst |

**Eine Spalte statt einer Datei.** In `tests/TEST_CATALOG.md` ist die letzte Zelle einer Tabellenzeile der Ergebnisstatus. Ein Pfad dort nennt, was ein Lauf gelesen hat, und ist Beleg, nicht Anweisung. Die übrigen Spalten derselben Zeile stehen unter der Regel. Prüfung 46 liest den Ergebnisstatus aus derselben Zelle.

### Was die Regel durchsetzt

Prüfung 48 hält jeden anweisenden Kernträger gegen die Laufzeitpfade aller Client Packs. Die Marken stammen aus den `runtime_placeholders` der Manifeste; ein neues Client Pack bringt seine Pfade damit selbst mit.

Prüfung 14 setzt dieselbe Regel für den **Namen** durch: Im Kern steht kein Clientname, weder als Handelnder noch als Produkt, und kein Platzhalter trägt ihn. Beide Prüfungen teilen sich eine Ausnahmemenge.

## Der Name: nennen oder zuschreiben

Für Namen gilt dieselbe Regel wie für Pfade, mit einer Trennlinie:

| Fall | Was der Text tut | Was dort steht |
|---|---|---|
| **Nennen** | Der Text trägt den Namen und sagt nichts über das Produkt | `<CLIENT_NAME>`; er löst sich nur in einer gerenderten Quelle auf. Einziger Fall im Bestand: der Titel von `framework/runtime/root-instruction.md` |
| **Zuschreiben** | Der Text sagt etwas über das Produkt – eine Fähigkeit, eine Voreinstellung, einen Geltungsbereich, eine Voraussetzung | Das gehört in das Client Pack; der Kern verweist auf dessen Fähigkeitsmatrix (`.koolie/core/clients/README.md` Abschnitt 4) |

Der Verweis geht auf die **Matrix**, nicht auf eine Zeile darin. Die Matrizen führen je Pack verschiedene Zeilen – `devin-desktop` etwa `M1` bis `M7`, `claude-code` nur `M1` bis `M3` –, und eine Zeilenkennung im Kern wäre wieder eine Bindung an einen Client. Keine Prüfung meldet sie.

Der ausgeschriebene Name kann nennen oder zuschreiben, und kein Skript kann das unterscheiden. Deshalb ist er im Kern gar nicht zulässig, auch nicht mit Zusatz.

## Begriffe und ihre Entsprechungen

| Begriff im Kern | Was es ist | `devin-desktop` | `claude-code` | `openai-codex` | `kiro` | `cursor` |
|---|---|---|---|---|---|---|
| **Wurzel-Anweisungsdatei** | Die Datei im Wurzelverzeichnis, die der Client zu Beginn jeder Sitzung lädt | `AGENTS.md` | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` | `AGENTS.md` |
| **Laufzeitschicht** | Das Verzeichnis mit allem, was der Client aus dem Repository liest | `.devin/` | `.claude/` | `.codex/` | `.kiro/` | `.cursor/` |
| **Berechtigungsdatei** | Versionierte Konfiguration der Rechte (verweigern / rückfragen / erlauben) | `.devin/config.json` | `.claude/settings.json` | `.codex/config.toml` (Pfadseite), dazu die Befehlsregeldatei `.codex/rules/koolie.rules` | `.kiro/agents/koolie.json` – das Agentenprofil, gewählt durch `.kiro/settings/cli.json`; fehlt es oder ist es kaputt, fällt der Client still auf seinen eingebauten Agenten zurück | `.cursor/cli.json` – **nur** der Schlüssel `permissions` mit `allow` und `deny`, kein Rückfragekorb; jedes Pfadmuster in zwei Schreibweisen. Dazu `.cursorignore`, die einzige Lesesperre, die das Suchwerkzeug beachtet |
| **Regelablage** | Verzeichnis der Regeltexte (Core-Kurzfassungen, Overlay, Packs) | `.devin/rules/` | `.claude/rules/` | `.codex/rules/` | `.kiro/steering/` | `.cursor/rules/` – nur Dateien mit der Endung `.mdc` laden |
| **Skill-Ablage** | Verzeichnis der Skills, je Skill ein Unterverzeichnis mit `SKILL.md` | `.devin/skills/` | `.claude/skills/` | `.codex/skills/` | `.kiro/skills/` | `.cursor/skills/` |
| **Agentenprofile** | Verzeichnis der Subagentenprofile | `.devin/agents/` | `.claude/agents/` | `.codex/agents/` | `.kiro/agents/` | `.cursor/agents/` |
| **Hook-Konfiguration** | Ort der Lebenszyklus-Hooks | in der Berechtigungsdatei (`.devin/config.json`) | in der Berechtigungsdatei (`.claude/settings.json`) | eigene Datei `.codex/hooks.json` | eigene Datei `.kiro/hooks/koolie.json` | eigene Datei `.cursor/hooks.json` |
| **MCP-Konfiguration** | Ort der Anbindung externer Systeme | `.devin/mcp_config.json` | `.mcp.json` | in der Berechtigungsdatei (`.codex/config.toml`, Tabelle `mcp_servers`) | `.kiro/settings/mcp.json` | `.cursor/mcp.json` |
| **Nutzerlokale Überschreibung** | Nicht versionierte, persönliche Ergänzung; im Framework nur zum Verschärfen zulässig | `AGENTS.local.md`, `.devin/config.local.json` | `CLAUDE.local.md`, `.claude/settings.local.json` | `AGENTS.override.md` – ⚠️ **verdrängt** die Wurzel-Anweisung, statt sie zu ergänzen; das Pack liefert dafür keine Vorlage, und Prüfung 88 meldet die Datei, wenn sie im Projekt liegt (`CLIENT_PACK.md` Abschnitt 1) | keine – der Hersteller dokumentiert keine nutzerlokale Wurzel-Anweisung, und das Pack liefert keine Vorlage | keine – der Hersteller dokumentiert keine nutzerlokale Wurzel-Anweisung, und das Pack liefert keine Vorlage |

Die maßgebliche Fassung je Client steht in `manifest.json` (maschinenlesbar) und `CLIENT_PACK.md` Abschnitt 1 (mit Belegstatus) des jeweiligen Packs.

Der Begriff bezeichnet nur den **Ort**. Berechtigungsdatei und Hook-Konfiguration haben zusätzlich einen Inhalt, der je Client anders geschrieben wird – andere Werkzeugnamen, getrennte Werkzeuge für Ändern und Anlegen, wörtliche gegen präfixbasierte Befehlsverbote. Diese zweite Abbildung steht in `CLIENT_PACK.md` Abschnitt 1a und wird von `.koolie/core/clientmap.py` ausgeführt.

## Was der Begriff nicht sagt

Ein Begriff benennt die **Rolle** eines Artefakts, nicht seine Eigenschaften. Ob ein Client eine Zusage des Frameworks technisch erzwingt oder nur als Anweisung führt, steht in der Fähigkeitsmatrix seines Client Packs (`.koolie/core/clients/README.md` Abschnitt 4).

Zwei Beispiele für gleichen Begriff und verschiedene Wirkung:

- Die **Regelablage** enthält bei allen Packs dieselben Regeltexte. Verschieden ist, wie sie geladen werden: `devin-desktop` kennt die Ladetrigger der Kernquelle, `claude-code` kennt nur die Bindung an Dateimuster (`paths`) und lädt alles Übrige unbedingt, und `openai-codex` lädt von sich aus keine Regeldatei – dort nennt die Wurzel-Anweisung die Dateien, die zu Beginn der Sitzung zu lesen sind. Der Kern beschreibt deshalb, *was* eine Regel bewirkt, nicht *wann* sie geladen wird; die Abbildung der Ladetrigger steht im Manifest des Packs unter `rule_triggers`.
- Die **MCP-Konfiguration** liegt bei `devin-desktop` innerhalb der Laufzeitschicht, bei `claude-code` daneben im Wurzelverzeichnis und bei `openai-codex` in der Berechtigungsdatei. Ein Kerntext, der „die Datei in der Laufzeitschicht“ nennt, wäre clientgebunden.

## Ausgabemarken: `[HALT]` und `[RÜCKFRAGE]`

Die Skills des Kerns und ihre Testfälle verwenden zwei Marken.

| Marke | Was sie bedeutet | Wo sie gilt |
|---|---|---|
| `[HALT]` | Der Skill unterbricht und legt vor, was er vorhat oder gefunden hat; er fährt erst nach ausdrücklicher Bestätigung fort. Was zu bestätigen ist und durch wen, sagt die Kontrollstufe | In `koolie-plan`, `koolie-bugfix-prepare` und `koolie-change-small` auch als Ausgabemarke – dort steht sie im Ausgabeformat (Abschnitt 5) und in den Qualitätskriterien (Abschnitt 6). In den übrigen neun Skills nur als Handlungsmarke in Arbeitsschritten und Fehlerbildern |
| `[RÜCKFRAGE]` | Der Skill fragt zurück, in der Form aus Abschnitt 4 seiner `SKILL.md`: Unklarheit benennen → Auswirkung erklären → konkrete Frage stellen → betroffenen Punkt als offen kennzeichnen | Ausschließlich als Handlungsmarke. Sie steht in keinem Abschnitt 5 und in keinem Abschnitt 6 der zwölf Skills |

### Handlungsmarke und Ausgabemarke

Eine **Handlungsmarke** sagt, *was zu tun ist*: `| Kontrollstufe nicht angegeben \| [RÜCKFRAGE] |`
heißt *frage zurück*, nicht *schreibe die Zeichenfolge*. Eine **Ausgabemarke** sagt, *was in
der Antwort stehen muss* – und nur dort, wo Abschnitt 5 oder 6 sie führt, ist sie das.

Auch wo die Marke Abnahmekriterium ist, verlangt sie kein Zeichen. Abschnitt 6 von
`koolie-change-small` sagt *„der [HALT] vor dem ersten Schreibzugriff ist erkennbar“*, nicht
*„wörtlich geschrieben“*. Prüfung 64 setzt durch, dass eine Ergebniszelle die Marke nur dort
verlangt, wo ihr Skill sie führt; sonst verlangt sie die Sache.

## Nummernschema der Regelablage

Das Schema gilt über alle Client Packs, damit eine Regel beim Clientwechsel wiedererkennbar bleibt. Es ist eine Framework-Konvention (`[KONZ]`), keine Produkteigenschaft.

| Präfix | Ebene der Prioritätshierarchie |
|---|---|
| `00-` | 3 Framework Core (Arbeitsmodell) |
| `10-` | 3 Framework Core (Datenschutz und Sicherheit) |
| `15-` | 3 Framework Core (Entwicklungsregeln) |
| `20-` | 4 Project Overlay |
| `30-` | 6 Role Packs |
| `40-` | 5 Technology Packs |
