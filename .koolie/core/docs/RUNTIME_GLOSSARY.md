# Begriffe der Laufzeitschicht

| Attribut | Wert |
|---|---|
| ID | `FW-DOC-GLOSSARY` |
| Version | `0.4.1` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |

## Zweck

Der Kern des Frameworks ist werkzeugneutral (D-02). Er darf deshalb **keine Pfade nennen, die nur bei einem einzigen KI-Client existieren** – sonst ist er nicht neutral, sondern nur so formuliert, als wäre er es.

Diese Datei legt die Begriffe fest, mit denen der Kern die Bestandteile der Laufzeitschicht bezeichnet, und bildet sie auf die tatsächlichen Pfade je Client Pack ab. Sie ist damit das Gegenstück zum Platzhalterregister: Dort stehen projektspezifische Werte, hier clientspezifische Pfade.

## Regel

- Im **Kern** (`.koolie/core/framework/`, `governance/`, `checklists/`, `prompts/`, `decision-trees/`, `onboarding/`, `docs/`, `templates/`, `examples/`, `tests/`) wird ausschließlich der **Begriff** verwendet.
- In einem **Client Pack** (`.koolie/core/clients/<client>/`) wird der **Pfad** verwendet – dort ist er richtig und notwendig.
- In **historischen Dokumenten** bleiben genannte Pfade unverändert. Sie beschreiben einen vergangenen Zustand; ihn nachträglich zu glätten, würde die Nachvollziehbarkeit zerstören.

### Die vier Ausnahmen, vollständig (D-128)

Die Regel gilt für jeden Träger des Kerns. Ausgenommen ist genau, was hier steht – eine Ausnahme, die nur im Quelltext einer Prüfung stünde, wäre keine Regel, sondern eine Voreinstellung.

| Gattung | Träger | Warum |
|---|---|---|
| **Chronik** | `CHANGELOG.md`, `governance/change-requests/`, `governance/DECISION_LOG.md`, `tests/protocols/`, **`docs/ROADMAP.md`** | Sie berichten einen vergangenen Stand. Die Roadmap gehört dazu, weil sie die Erhebungsergebnisse je Arbeitspaket und die Befundberichte je Release führt |
| **Werkzeuge** | alle `.py` des Kerns | Ein Skript, das eine Installation herstellt oder prüft, **muss** Pfade nennen. `install.py` und `clientmap.py` lösen sie aus den Manifesten auf, die Prüfskripte stellen Installationen her |
| **Abbildungstabellen** | diese Datei, `docs/PLACEHOLDER_REGISTRY.md`, `clients/` | Sie müssen beide Namen nennen; dort ist der Pfad der Inhalt |
| **Anhänge und Chronik des Hauptdokuments** | `build/doc/29-grenzen.md`, `build/doc/31-anhaenge.md`, `build/doc/32-abschluss.md` | Die übrigen Kapitelquellen unter `build/doc/` stehen unter der Regel (D-311). Diese drei Träger haben einen dauerhaften Grund: `29-grenzen.md` ist ein ausdrückliches Zeitdokument des Stands vom 2026-09-01, `31-anhaenge.md` führt die Quellenliste **je Client Pack** und den Verifikationsbedarf **eines** Packs – dieselbe Gattung wie die Abbildungstabellen –, und `32-abschluss.md` trägt die Releasechronik samt den Aussagen des Auftrags **über** die Produktnennung selbst |

**Eine Spalte statt einer Datei.** In `tests/TEST_CATALOG.md` ist die **letzte** Zelle einer Tabellenzeile der Ergebnisstatus. Ein Pfad dort nennt, was ein Lauf gelesen hat, und gehört zum gemessenen Client Pack (D-117) – er ist Beleg, nicht Anweisung. Die übrigen Spalten derselben Zeile stehen unter der Regel. Denselben Zuschnitt – die letzte Zelle – benutzt Prüfung 46 für den Ergebnisstatus.

### Was die Regel durchsetzt

**Prüfung 48** hält jeden anweisenden Kernträger gegen die Laufzeitpfade **aller** Client Packs; die Marken stammen aus den `runtime_placeholders` der Manifeste, nicht aus einer gepflegten Liste. Ein neues Client Pack bringt seine Pfade damit selbst mit (D-128, `CR-2026-080`).

**Prüfung 14** setzt dieselbe Regel für den **Namen** durch: Im Kern steht kein Clientname – weder als Handelnder noch als Produkt, und kein Platzhalter trägt ihn (D-28, **D-129**). Beide Prüfungen teilen sich **eine** Ausnahmemenge.

## Der Name: nennen oder zuschreiben

Für Namen gilt dieselbe Regel wie für Pfade, und sie hat eine Trennlinie, die man kennen muss:

| Fall | Was der Text tut | Was dort steht |
|---|---|---|
| **Nennen** | Der Text trägt den Namen und sagt **nichts** über das Produkt | `<CLIENT_NAME>` – und der löst sich **nur in einer gerenderten Quelle** auf. Einziger angewandter Fall im ganzen Bestand: der Titel von `framework/runtime/root-instruction.md` |
| **Zuschreiben** | Der Text sagt etwas **über** das Produkt – eine Fähigkeit, eine Voreinstellung, einen Geltungsbereich, eine Voraussetzung | Das gehört in das **Client Pack**; der Kern verweist auf dessen **Fähigkeitsmatrix** (`.koolie/core/clients/README.md` Abschnitt 4) |

> ⚠️ **Der Verweis geht auf die Matrix, nicht auf eine Zeile darin.** Die Fähigkeitsmatrizen führen je Pack verschiedene Zeilen – `devin-desktop` etwa hat `M1` bis `M7`, `claude-code` nur `M1` bis `M3`. Eine Zeilenkennung in einem Kerntext wäre dieselbe Client-Bindung eine Ebene tiefer, und keine Prüfung meldet sie: Prüfung 31 rechnet die Summen *innerhalb* eines Packs nach und verlangt nirgends, dass zwei Packs dieselben Zeilen führen.

**Der ausgeschriebene Name kann beides sein, nennen oder zuschreiben, und kein Skript kann es unterscheiden.** Deshalb ist er im Kern gar nicht zulässig, auch nicht mit Zusatz: *Eine Marke mit zwei Bedeutungen taugt weder als Bedingung noch als Entlastung* (D-129, `CR-2026-081`).

## Begriffe und ihre Entsprechungen

| Begriff im Kern | Was es ist | `devin-desktop` | `claude-code` | `openai-codex` |
|---|---|---|---|---|
| **Wurzel-Anweisungsdatei** | Die Datei im Wurzelverzeichnis, die der Client zu Beginn jeder Sitzung lädt | `AGENTS.md` | `CLAUDE.md` | `AGENTS.md` |
| **Laufzeitschicht** | Das Verzeichnis mit allem, was der Client aus dem Repository liest | `.devin/` | `.claude/` | `.codex/` |
| **Berechtigungsdatei** | Versionierte Konfiguration der Rechte (verweigern / rückfragen / erlauben) | `.devin/config.json` | `.claude/settings.json` | `.codex/config.toml` (Pfadseite), dazu die Befehlsregeldatei `.codex/rules/koolie.rules` (D-346) |
| **Regelablage** | Verzeichnis der Regeltexte (Core-Kurzfassungen, Overlay, Packs) | `.devin/rules/` | `.claude/rules/` | `.codex/rules/` |
| **Skill-Ablage** | Verzeichnis der Skills, je Skill ein Unterverzeichnis mit `SKILL.md` | `.devin/skills/` | `.claude/skills/` | `.codex/skills/` |
| **Agentenprofile** | Verzeichnis der Subagentenprofile | `.devin/agents/` | `.claude/agents/` | `.codex/agents/` |
| **Hook-Konfiguration** | Ort der Lebenszyklus-Hooks | in der Berechtigungsdatei (`.devin/config.json`, D-32) | in der Berechtigungsdatei (`.claude/settings.json`) | eigene Datei `.codex/hooks.json` |
| **MCP-Konfiguration** | Ort der Anbindung externer Systeme | `.devin/mcp_config.json` | `.mcp.json` | in der Berechtigungsdatei (`.codex/config.toml`, Tabelle `mcp_servers`) |
| **Nutzerlokale Überschreibung** | Nicht versionierte, persönliche Ergänzung; im Framework nur zum Verschärfen zulässig | `AGENTS.local.md`, `.devin/config.local.json` | `CLAUDE.local.md`, `.claude/settings.local.json` | `AGENTS.override.md` – ⚠️ **verdrängt** die Wurzel-Anweisung, statt sie zu ergänzen; das Pack liefert dafür keine Vorlage, und Prüfung 88 meldet die Datei, wenn sie im Projekt liegt (`CLIENT_PACK.md` Abschnitt 1) |

Die maßgebliche Fassung je Client steht in `manifest.json` (maschinenlesbar) und `CLIENT_PACK.md` Abschnitt 1 (mit Belegstatus) des jeweiligen Packs.

Der Begriff bezeichnet dabei nur den **Ort**. Berechtigungsdatei und Hook-Konfiguration haben zusätzlich einen **Inhalt**, der je Client anders geschrieben wird – andere Werkzeugnamen, getrennte Werkzeuge für Ändern und Anlegen, wörtliche gegen präfixbasierte Befehlsverbote. Diese zweite Abbildung steht in `CLIENT_PACK.md` Abschnitt 1a und wird von `.koolie/core/clientmap.py` ausgeführt (D-18).

## Was der Begriff nicht sagt

Ein Begriff benennt die **Rolle** eines Artefakts, nicht seine Eigenschaften. Ob ein Client eine Zusage des Frameworks technisch erzwingt oder nur als Anweisung führt, steht in der **Fähigkeitsmatrix** seines Client Packs (`.koolie/core/clients/README.md` Abschnitt 4).

Zwei Beispiele, in denen der Begriff gleich und die Wirkung verschieden ist:

- Die **Regelablage** enthält bei allen Packs dieselben Regeltexte. Verschieden ist, **wie sie geladen werden**: `devin-desktop` kennt die Ladetrigger der Kernquelle, `claude-code` kennt nur die Bindung an Dateimuster (`paths`) und lädt alles Übrige unbedingt, und `openai-codex` lädt von sich aus keine Regeldatei – dort nennt die Wurzel-Anweisung die Dateien, die zu Beginn der Sitzung zu lesen sind (D-348). Der Kern beschreibt deshalb, *was* eine Regel bewirkt, nicht *wann* sie geladen wird; die Abbildung der Ladetrigger steht im Manifest des Packs unter `rule_triggers`.
- Die **MCP-Konfiguration** liegt bei `devin-desktop` innerhalb der Laufzeitschicht, bei `claude-code` daneben im Wurzelverzeichnis und bei `openai-codex` in der Berechtigungsdatei. Ein Kerntext, der „die Datei in der Laufzeitschicht“ nennt, wäre schon wieder clientgebunden.

## Ausgabemarken: `[HALT]` und `[RÜCKFRAGE]`

Die Skills des Kerns und ihre Testfälle verwenden zwei Marken. Was sie bedeuten und wo sie
Abnahmekriterium sind, steht hier (`K-74`, D-197).

| Marke | Was sie bedeutet | Wo sie gilt |
|---|---|---|
| `[HALT]` | Der Skill **unterbricht** und legt vor, was er vorhat oder gefunden hat; er fährt erst nach ausdrücklicher Bestätigung fort. Was zu bestätigen ist und durch wen, sagt die Kontrollstufe | In `fw-plan`, `fw-bugfix-prepare` und `fw-change-small` **auch als Ausgabemarke** – dort steht sie im Ausgabeformat (Abschnitt 5) und in den Qualitätskriterien (Abschnitt 6). In den übrigen neun Skills nur als **Handlungsmarke** in Arbeitsschritten und Fehlerbildern |
| `[RÜCKFRAGE]` | Der Skill **fragt zurück**, in der Form aus Abschnitt 4 seiner `SKILL.md`: Unklarheit benennen → Auswirkung erklären → konkrete Frage stellen → betroffenen Punkt als offen kennzeichnen | **Ausschließlich als Handlungsmarke.** Sie steht in keinem Abschnitt 5 und in keinem Abschnitt 6 der zwölf Skills |

### Handlungsmarke und Ausgabemarke (D-197)

Eine **Handlungsmarke** sagt, *was zu tun ist*: `| Kontrollstufe nicht angegeben \| [RÜCKFRAGE] |`
heißt *frage zurück*, nicht *schreibe die Zeichenfolge*. Eine **Ausgabemarke** sagt, *was in
der Antwort stehen muss* – und nur dort, wo Abschnitt 5 oder 6 sie führt, ist sie das.

**Auch wo die Marke Abnahmekriterium ist, verlangt sie kein Zeichen.** Abschnitt 6 von
`fw-change-small` sagt *„der [HALT] vor dem ersten Schreibzugriff ist **erkennbar**“* – nicht
*„wörtlich geschrieben“*. **Prüfung 64** setzt durch, dass eine Ergebniszelle die
Marke nur dort verlangt, wo ihr Skill sie führt; sonst verlangt sie die **Sache**.

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
