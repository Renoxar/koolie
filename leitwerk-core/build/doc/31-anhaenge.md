# 31 Anhänge

## 31.1 Inventar des Referenz-Repositorys

Stand Release 0.9.0, 233 versionierte Dateien im Kern. Die vollständige Struktur mit Erläuterung steht in Kap. 15.2; hier nur die Größenordnung je Bereich.

| Bereich | Dateien | Inhalt |
|---|---|---|
| direkt im Kernverzeichnis | 5 | `install.py`, `clientmap.py`, `VERSION`, `CHANGELOG.md`, `OWNERS.md` |
| `clients/` | 10 | Abbildungsschicht: zwei Client Packs zu je vier Dateien, Regeln der Schicht, Vorlage |
| `framework/` | 83 | Core-Module, Laufzeitfassung, 12 Referenz-Skills, Role- und Tech-Packs, Organisationsvorgaben |
| `templates/` | 23 | Project-Overlay-Saat, Regelvorlagen, Skill-Vorlage |
| `build/` | 37 | 33 Kapitelquellen, Assemblierungs- und DOCX-Skript, Referenzdokument, README |
| `prompts/` · `checklists/` · `decision-trees/` | 32 | 12 Prompt-Vorlagen, 11 Checklisten, 6 Entscheidungsbäume, je README |
| `governance/` | 18 | Decision Log, RACI, Hierarchie, Prozesse, Änderungsanträge |
| `onboarding/` · `examples/` · `pilot/` · `docs/` · `tests/` | 25 | Onboarding-Paket, synthetische Beispiele, Pilotkonzept, Leitfäden, Testkatalog mit Skripten und Protokollen |

**Was daraus in ein Projekt installiert wird:** 80 Dateien beim Client Pack `devin-desktop`, 79 bei `claude-code` – Wurzel-Anweisungsdatei, Laufzeitschicht und Project Overlay. Der Unterschied liegt allein darin, dass ein Client keine eigene Hook-Datei kennt.

Bewusst ohne Dateizahlen je Unterverzeichnis: Diese Tabelle stand bis Release 0.8.0 auf dem Stand von 0.2.0, weil sie beschrieb, was das Dateisystem ohnehin weiß. Verbindlich ist der Baum in Kap. 15.2 und – für den Installationsumfang – die Ausgabe von `install.py`.

## 31.2 Laufzeitglossar

Der Kern nennt die Bestandteile der Laufzeitschicht mit Begriffen, nicht mit Pfaden. Die Abbildung auf die Pfade eines konkreten Client Packs steht hier:

{{EMBED-RAW:leitwerk-core/docs/RUNTIME_GLOSSARY.md:2}}
## 31.3 Platzhalterregister

{{EMBED-RAW:leitwerk-core/docs/PLACEHOLDER_REGISTRY.md:2}}

## 31.4 Quellen der Produktdokumentation und Belegzuordnung

Die Quellen belegen die als `[DOK]` gekennzeichneten Aussagen; der Framework Owner hält diese Liste im Rahmen der Produktbeobachtung aktuell (FW-AK-01).

Sie ist **je Client Pack** geführt. Das ist keine Gliederungsfrage: Eine Aussage über einen Client hängt an dessen Dokumentation und an keiner anderen, und beide Listen haben verschiedene Recherchestände. Bis Release 0.15.0 enthielt dieser Anhang ausschließlich der KI-Client-Quellen – auch dann noch, als das Pack `claude-code` bereits ein Dutzend `[DOK]`-Aussagen gegen `code.claude.com` trug. Die Liste behauptete damit, die `[DOK]`-Aussagen zu belegen, und tat es für einen der beiden Clients nicht.

Die Kennungen tragen seit Release 0.16.0 das Präfix des Client Packs (`QD-` für `devin-desktop`, `QC-` für `claude-code`). Vorher hießen sie `Q1` bis `Q17` – dieselben Kürzel, mit denen das Framework an rund zwanzig Stellen seine **Qualitätsregeln** bezeichnet (`Q8` etwa die Größenschwelle einer Änderung). Zwei Bedeutungen desselben Kürzels in einem Dokument sind eine Verwechslung, die keinen Nutzen hat.

Die **maßgebliche Zuordnung** steht in der Fähigkeitsmatrix des jeweiligen Packs (Kap. 15.1 beziehungsweise Kap. 7a): Dort nennt der **Belegkopf** jeder mit `[DOK]` belegten Zeile die **Quellenkennung** dieser Liste – und **Prüfung 73 setzt es seit Release 0.85.0 durch**, Verweisbelege (*„wie B3"*) aufgelöst (D-263 bis D-266). Die Kennung ist die verbindliche Form, weil allein sie gegen diese Liste gehalten werden kann; ein Seitenpfad darf danebenstehen. Diese Liste sagt, welche Seite wofür herangezogen wurde und **wann sie abgerufen worden ist** – die Angabe, die eine Wiederholungsprüfung braucht.

🔴 **Bis Release 0.61.0 stand hier, die Belegspalte nenne die Seite *je Zeile*. Das traf für 14 von 43 Zeilen zu.** Ausgezählt am 2026-09-18 im Rahmen von `FW-AK-01`: Das Pack `devin-desktop` führt 20 Zeilen mit `[DOK]`, davon **4** mit genannter Quelle; `claude-code` 23, davon **10**. Die Zusage war damit der wiederkehrende Befundtyp dieses Repositoriums in seiner Grundform – eine Aussage, die mehr verspricht, als sie leistet. **Der Preis ist gemessen, nicht geschätzt:** Die Durchsicht vom 18.09. musste alle 22 Quellen abrufen, weil ohne Zuordnung je Zeile nicht zu sagen ist, welche Seite welche Zusage trägt. Die Lücke war als `K-62` geführt und hat einen eigenen Posten im Releaseplan bekommen; sie ist **nicht** nebenbei geschlossen worden, weil eine geratene Zuordnung wie ein Beleg aussähe (D-156).

🟢 **Geschlossen mit Release 0.85.0** (`CR-2026-118`, D-263 bis D-268). **Der Bestand gab 25 von 26 Zuordnungen her** – diese Liste führt je Quelle, wofür sie herangezogen wurde, und das ist eine Aufzeichnung und keine Schätzung. Die Zuordnung trägt deshalb den Zusatz `(Zuordnung K-62)`: **gewonnen aus dem Bestand am 22.09.2026, nicht aus einem zweiten Abruf.** Der Recherchestand der Seiten bleibt der vom 18.09.2026 – *eine Zuordnung ist keine Aktualitätsaussage.*

🔴 **Eine Zeile ist ausgesprochen offen geblieben, und das ist das Ergebnis und kein Rest:** `M3` des Packs `claude-code` („Freigabe auf die Sitzung begrenzbar") – **keine der sechs Seiten führt die Sitzungs-Grant-Stufen**, während sie beim Schwesterpack in `QD-11` stehen. Die Zeile sagt `QUELLE NICHT ZUGEORDNET`, und Prüfung 73 führt die zugelassenen Lücken als deklarierte Menge. ➡️ **Damit hat der nächste Durchgang von `FW-AK-01` seinen ersten gezielten Auftrag: eine Zeile gegen eine Seite statt 44 gegen 22** – genau die Ersparnis, für die `K-62` aufgemacht worden ist.

🔴 **Und die Zahl 26 von 44 war aus zwei Gründen nicht die richtige.** (1) Vier Belegzellen **nannten** die Marke `[DOK]` nur: zwei erklären sie, zwei nennen sie in der Vergangenheit; ihr heutiger Beleg ist eine Messung (D-265). *Das ist der VERIFY-Marker eine Ebene tiefer – auch dort zählen nur nennende Fundstellen mit.* (2) Die **sieben Verweisbelege** (*„wie B3"*, einer über zwei Glieder) zählten in keiner Richtung mit, obwohl die Zusammenfassung desselben Packs sie beim VERIFY-Marker sehr wohl mitzählt (D-266). **Nach der Kopfregel, die Prüfung 73 durchsetzt, waren es 40 von 46.**

### 31.4.1 Client Pack `devin-desktop`

Recherchestand: 01.–02.09.2026, gegen Devin Desktop 3.8.20 (QD-4). Ergänzt am 11.09.2026 gegen Devin Desktop 3.9.19 / CLI 3000.10.21 (Erhebungen zu K-21 bis K-27). **Vollständig abgeglichen am 18.09.2026 gegen den Produktstand 3.10.31** (`FW-AK-01`, `leitwerk-core/tests/protocols/2026-09-18-FW-AK-01.md`) – der erste vollständige Abgleich dieses Teils. Fünf Zeilen der Fähigkeitsmatrix sind inzwischen in einer Sitzung **beobachtet** (H1, H2, R5, R6, S5); die übrigen Einstufungen sind gegen eine Installation nicht belegt, 8 von 34 Zeilen tragen einen VERIFY-Marker (Roadmap AP2).

🔴 **Drei Quellen belegen einen Agenten, den der Hersteller entfernt hat.** Der Changelog sagt zu 3.9.19 (08.09.2026): *„Cascade has been removed. Devin Local is now the only agent available in Devin Desktop."* QD-5, QD-7 und QD-8 liegen unter `desktop/cascade/` und sprechen weiter im Präsens von diesem Agenten; QD-2 sagt sogar noch, er bleibe *„through July"* verfügbar. **Die Seiten sind erreichbar und inhaltlich unverändert – veraltet ist, wofür sie taugen.** Die Folge steht im Pack: Zeile R1 stützt sich seit 0.12.0 auf QD-6 statt auf QD-5, und die Zeichenzahlen aus QD-7 gelten weiter als **Vorgabe des Frameworks** und nicht als Produkteigenschaft (Zeile R4).

🔴 **Und eine Aussage der Liste ist innerhalb der verbindlichen Zielspanne des Packs widerlegt.** QD-12 sagt *„Organization-level (enterprise) settings can never be overridden by project or user config"*; der Changelog weist zu 3.10.31 (16.09.2026) aus: *„Restricted Mode blocks restricted workspace settings written in nested object form, not just the dotted form (CVE-2026-81376)."* Bis einschließlich 3.10.27 hing die Durchsetzung also an der **Schreibweise**. Die Zielspanne `3.9.x` liegt vollständig davor; Zeile M2 des Packs trägt den Nachtrag.

| Nr. | Quelle | Belegt im Framework insbesondere |
|---|---|---|
| QD-1 | devin.ai/blog/windsurf-is-now-devin-desktop | Rebranding zum 02.06.2026; Devin Local ersetzt Cascade; Übergangsfrist für Cascade; Agent Command Center, Spaces, ACP |
| QD-2 | docs.devin.ai/desktop/devin-desktop-faq | `.devin/` als Primär-, `.windsurf/` als Legacy-Pfad; `.windsurfrules`; Systempfade für organisationsweite Regeln; Legacy-MCP-Pfad; Plankontinuität |
| QD-3 | docs.devin.ai/desktop/devin-local | Modi Normal/Plan/Ask; Berechtigungsmodell deny/ask/allow mit Geltungsbereichen; MCP-Bestätigung als Standard; Subagenten (Preview) und Quick Review; keine Memories/Workflows in Devin Local; Migrationsassistent; Enterprise-Einstellungen (Sandbox-Erzwingung, Domain-Listen); Konfigurationspfade |
| QD-4 | docs.devin.ai/desktop/changelog | Version 3.8.20 vom 21.08.2026; Komposition der Berechtigungsebenen mit deny-Vorrang; `sandbox.excluded`; persistente Plan-Dateien; Subagenten-Dateiformen; Skill-Berechtigungen bei Auto-Genehmigungen |
| QD-5 | docs.devin.ai/desktop/cascade/agents-md | AGENTS.md im Root always-on; Unterverzeichnisse als automatische Glob-Regeln; Einspeisung in die Regel-Engine; Namensvarianten |
| QD-6 | docs.devin.ai/cli/extensibility/rules | Regeldateien und -orte (AGENTS.md, AGENTS.local.md, `.devin/rules/*.md`, global), Frontmatter `description`/`trigger`/`globs` mit Werten, Präzedenzen, Kompatibilitätspfade |
| QD-7 | docs.devin.ai/desktop/cascade/memories | Aktivierungsmodi der Regeln; Zeichenlimits 6.000/12.000 (Cascade-Kontext); Memories nur für Cascade |
| QD-8 | docs.devin.ai/desktop/cascade/workflows | Workflows nur für Cascade; Migration zu Skills; Limits |
| QD-9 | docs.devin.ai/product-guides/skills | SKILL.md-Format; Suchpfade einschließlich `.agents/skills/` (empfohlen) und `.devin/skills/`; `triggers`; `@skills:`-Erwähnung; Argument-Substitution; eine aktive Skill-Grenze |
| QD-10 | docs.devin.ai/cli/extensibility/skills/creating-skills | Projekt- und globale Skill-Pfade; Frontmatter-Felder inkl. `allowed-tools`, `permissions` (additiv), `argument-hint`, `model`, `subagent`, `agent`; Aufruf `/skill-name` |
| QD-11 | docs.devin.ai/cli/reference/permissions | Matcher `Read()`, `Write()`, `Exec()`, `Fetch()`, Tool- und MCP-Matcher; deny > ask > allow; Permission-Modi; Ebenen-Präzedenz; Sitzungs-Grant-Stufen |
| QD-12 | docs.devin.ai/cli/extensibility/configuration | `config.json`-Scopes und -Schlüssel; `mcp_config.json`/`.local`; `read_config_from`; Enterprise unüberschreibbar |
| QD-13 | docs.devin.ai/cli/extensibility/hooks/overview | `hooks.v1.json`; Ereignisse; Blockierung per Exit-Code 2/`decision: block`; `additionalContext`; `DEVIN_PROJECT_DIR` |
| QD-14 | docs.devin.ai/de/cli/subagents | Subagent-Dateiformen und Frontmatter; eingebaute Profile; Vordergrund-/Hintergrundrechte |
| QD-15 | docs.devin.ai/cli/sandbox | Sandbox-Ableitung aus Berechtigungen; Domainfilter und Modi; `sandbox.excluded`; Plattformgrenzen (kein Windows); Instabilität des Netzfilters |
| QD-16 | docs.devin.ai/cli/enterprise/team-settings | Team-Kontrollen: Modell-Allowlist, Websuche standardmäßig aus, MCP-Kontrollen und Registry-Erzwingung, unüberschreibbare Terminal-Permissions, Sandbox-Erzwingung, Attribution-Filter |
| QD-17 | docs.devin.ai/admin/security | Training-Opt-out auf kostenpflichtigen Plänen; Zero Data Retention nach Opt-out; Teams-Opt-out nur durch Admin; Enterprise nur mit schriftlicher Zustimmung; SOC 2 Type II; Verschlüsselung |

### 31.4.2 Client Pack `claude-code`

Recherchestand: 10.09.2026, gegen Clientversion 2.1.267. Erhoben im Rahmen von AP2 (`leitwerk-core/tests/protocols/2026-09-10-AP2-claude-code.md`); die Seitenangaben sind gegenüber dem Protokoll um die genauen Pfade ergänzt. **Abgeglichen am 18.09.2026 gegen 2.1.275**, dazu der Changelog der Stände 2.1.268 bis 2.1.275 (`FW-AK-01`, `leitwerk-core/tests/protocols/2026-09-18-FW-AK-01.md`).

🆕 **QC-6 ist mit diesem Abgleich hinzugekommen, und sein Fehlen ist selbst ein Befund** (D-159): Das Pack trägt drei Hook-Zusagen (H1, H2, H3), und die Liste führte die Hook-Seite nicht – während das Schwesterpack für denselben Gegenstand QD-13 führt. Aufgefallen ist es, weil die Durchsicht selbst auf diese Seite zugreifen musste, um den VERIFY-Marker auf Zeile R5 aufzulösen.

| Nr. | Quelle | Belegt im Framework insbesondere |
|---|---|---|
| QC-1 | code.claude.com/docs/en/memory | Regelablage `.claude/rules/*.md`, rekursiv gefunden; Frontmatter-Feld `paths` mit Glob-Mustern, mehreren Mustern und Klammer-Expansion samt Budget (1.000 expandierte Muster, 4 MiB); eine Regel **ohne** `paths` lädt unbedingt und ohne Import; Ladeordnung und `@pfad`-Importe der Wurzel-Anweisungsdatei; Grenze 4 MiB je Anweisungsdatei und Empfehlung 200 Zeilen; Entfernen von Block-Kommentaren vor dem Einspeisen (für `CLAUDE.md` dokumentiert); `claudeMdExcludes`. **Neu mit dem Abgleich vom 18.09.2026:** die **selbstgeschriebene** Anweisungsquelle des Clients (*„Auto memory is on by default"*) mit Ablage außerhalb des Projekts und Ladung des Index in jede Sitzung – das Framework schaltet sie ab (D-154); `/context` als Auskunft über die tatsächlich geladenen Anweisungsdateien |
| QC-2 | code.claude.com/docs/en/permissions | Pfadregeln werden nur für `Read` und `Edit` ausgewertet, für andere Werkzeuge angenommen, nie konsultiert und beim Sitzungsstart als Warnung gemeldet; `deny` vor `ask` vor `allow` und die Unaufhebbarkeit einer Verweigerung über alle Ebenen; gitignore-Mustersemantik samt Normalisierung auf POSIX-Form unter Windows; Präfixsemantik der Befehlsregeln und ihre Grenze (`git -C . push` trifft nicht); `disableBypassPermissionsMode` und `disableAutoMode`; Vorrang eines mit Exit-Code 2 blockierenden Hooks **vor** den Berechtigungsregeln |
| QC-3 | code.claude.com/docs/en/skills | `SKILL.md`-Frontmatter (`name`, `description`, `allowed-tools`, `disable-model-invocation`, `user-invocable`, `paths`, `model`); Wirkung von `disable-model-invocation: true` – das Modell kann den Skill nicht selbst laden, und seine Beschreibung kommt gar nicht erst in den Kontext; Suchpfade der Skill-Ablage; Aufruf über `/name`. **Neu mit dem Abgleich vom 18.09.2026:** die **Kontoquelle** – der Client lädt die im Konto eingeschalteten Skills nach `~/.claude/skills/synced/`, *„This is enabled by default"*, mit Abgleich etwa alle zehn Minuten **während** der Sitzung; dazu das Vorladen von Skills in ein Unteragentenprofil, das `disable-model-invocation: true` ebenfalls verhindert |
| QC-4 | code.claude.com/docs/en/sub-agents | Subagentenprofile unter `.claude/agents/`; Frontmatter `tools` (Allowlist) und `disallowedTools` (Denylist) mit dokumentierter Verarbeitungsreihenfolge; die Beschränkung wirkt technisch; ein Profil, dessen `tools`-Liste sich zu keinem Werkzeug auflöst, wird gar nicht erst gestartet; weitere Felder, darunter `permissionMode` |
| QC-5 | code.claude.com/docs/en/settings | Ablageorte und Rangfolge der Einstellungsdateien: verwaltet → Kommandozeile → `settings.local.json` → `settings.json` → Nutzer; `permissions`, `hooks`, `env` und `defaultMode` in derselben Datei; verwaltete Einstellungen sind bis auf wenige benannte Ausnahmen unüberschreibbar. **Neu mit dem Abgleich vom 18.09.2026:** die Tabelle der Vorrangausnahmen – für einige Schlüssel gilt der **strengere** Wert aus einer Ebene, die sonst nicht überschreiben dürfte, und für `syncClaudeAiSkills` beziehungsweise `syncClaudeAiPlugins` ausdrücklich *„a `false` in `.claude/settings.json` is ignored"*. Das ist die Datei, die das Client Pack ausliefert (`K-63`) |
| QC-6 | code.claude.com/docs/en/hooks | Ereignisse der Hook-Schicht und ihre Matcher; `InstructionsLoaded` mit dem **Ladegrund** als Matcher (`session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact`) – der dokumentierte technische Aufzählungsweg für Zeile R5 (D-158). Abgerufen am 18.09.2026 |

### 31.4.3 Was die Liste über sich selbst sagt

🟢 **Beide Teile sind am 18.09.2026 gefahren, und damit zum ersten Mal beide gegen eine benannte Produktversion und einen gesichteten Changelog** (`FW-AK-01`, `CR-2026-087`). Bis dahin lagen die Recherchestände neun Tage auseinander, und für `devin-desktop` war seit dem 02.09.2026 kein Changelog gesichtet.

**Was der erste vollständige Durchgang gekostet und ergeben hat:** 22 Quellen abgerufen. **Zwölf tragen ihren zugeschriebenen Beleg unverändert, zehn nicht** – geändert, im Gegenstand entfallen oder vom Produkt-Changelog widerlegt; eine der zwölf führt zusätzlich einen neuen, für das Framework erheblichen Gegenstand. Daraus **dreizehn Befunde**. ⚠️ **Die erste Fassung dieses Absatzes zählte neun statt zehn** und ist vor dem Festschreiben berichtigt worden – zum wiederholten Mal war eine eigene Zahl zu klein. Zwei davon haben eine Zahl von D-11 bewegt (der VERIFY-Marker auf Zeile R5, Kriterium 1: 23 → 22; und die Ergebniszelle selbst, Kriterium 2: 93 → 92), einer hat eine Prüfung erzeugt (54), vier sind als Klärungspunkte offen (`K-62` bis `K-65`).

🔴 **Die teuerste Lehre des Durchgangs betrifft diese Liste selbst und nicht die Quellen.** Weil 29 von 43 `[DOK]`-Zeilen ihre Quelle nicht nannten, war ein *gezielter* Abgleich nicht möglich: Es musste jede Seite gelesen werden, um zu sehen, ob eine Zusage noch trägt. **Eine Quellenliste ohne Zuordnung je Zeile macht ihre eigene Wiederholungsprüfung so teuer wie die erste** – und `FW-AK-01` ist der Testfall, der sie *laufend* verlangt. `K-62` führt die Lücke, D-156 die Entscheidung. **Nach diesem Durchgang sind es 26 von 44** – fünf Zeilen haben ihre Quelle bekommen, weil der Abgleich sie gelesen hat, und eine Einstufung hat sich bewegt. ⚠️ **Nachgerechnet am 22.09.2026 (`CR-2026-118`): Von den fünf genannten Zeilen hatte `X2` ihre Quelle schon vorher** – die Zahlen 29 von 43 und 26 von 44 stimmen, ihre Zerlegung in diesem Satz nicht ganz. *Zum wiederholten Mal war nicht die Zahl falsch, sondern der Satz daneben.* 🟢 **Beides ist mit 0.85.0 erledigt und maschinell gedeckt.**

Eine Quelle ohne Abrufdatum ist kein Beleg, sondern eine Behauptung mit Fußnote: Produktdokumentation ändert sich, und ohne Datum lässt sich nicht sagen, ob eine Aussage noch trägt. Dieselbe Überlegung hatte D-25 für Versionsangaben angestellt. **Der Durchgang vom 18.09. hat die Umkehrung gezeigt:** Ein Abrufdatum nützt nichts, wenn nicht dabeisteht, *welche Zusage* die Seite trägt.


## 31.5 Konsolidierter Verifikationsbedarf

Der **maßgebliche** Verifikationsbedarf steht seit Release 0.5.0 in der Fähigkeitsmatrix des jeweiligen Client Packs: Jede Zeile ohne Beleg sagt dort `BELEG OFFEN` mit Grund und Datum, und die Matrix wird mit dem Pack gepflegt statt in diesem Anhang. Belegstand zum Zeitpunkt dieser Dokumentfassung: 8 von 34 Zeilen bei `devin-desktop` tragen den Marker; bei `claude-code` sind es 2 von 29 – beide mit 0.26.0 neu (R5, S5) und für diesen Client nicht erhoben –, und dort ist weiterhin keine Einstufung als **beobachtete** Durchsetzung belegt – ein Dokumentenabgleich belegt `[DOK]`, nicht `[TECHNISCH]` im Sinne einer beobachteten Wirkung. Die Matrix beider Packs ist in Kap. 15.1 beziehungsweise Kap. 7a eingebettet.

Die folgende Liste ergänzt sie um Punkte, die keiner einzelnen Zusage der Matrix zugeordnet sind, sondern das Zusammenspiel betreffen. Sie gilt für das Client Pack `devin-desktop`; Prüfweg ist Roadmap-AP2, Testklasse AK:

| Nr. | Prüfpunkt | Betroffene Stellen |
|---|---|---|
| ~~V1~~ | **Geschlossen mit 0.26.0, Ergebnis „nicht dokumentiert".** Der Abgleich am 2026-09-11 gegen Devin Desktop 3.9.19 (`cli/extensibility/rules`) nennt für Regeldateien **keine** Zeichen- oder Größengrenze – weder für `AGENTS.md` noch für `.devin/rules/*.md` noch für globale Regeln; zweite unabhängige Bestätigung in derselben Sitzung (ERH-10). Die Zahlen 6.000/12.000 stammen aus der Cascade-Dokumentation (QD-7) und bleiben als **Vorgabe des Frameworks** in Kraft: Zeile R4 führt sie seit 0.26.0 als `[TEXTUELL]` (`CR-2026-027`). Wird die Grenze später doch dokumentiert, ist V1 erneut zu öffnen; K-19 bleibt offen | Laufzeit-README des Packs (Abschnitt „Regelablage"), AGENTS.md-Größenbudget, Validator-Grenzen |
| V2 | Exakte Schemadetails von `.devin/config.json` (Schlüsselstruktur, Glob-/Präfix-Semantik, Wildcard `Fetch(*)`, Kommentarfelder-Toleranz) | `.devin/config.json`, FW-CORE-03 Abschnitt 4 |
| ~~V3~~ | **Erledigt mit 0.25.0.** Das Hook-Eingabeschema ist in einer Sitzung erhoben: `hook_event_name`, `tool_name`, `tool_input`, `session_id`, `prompt_id` und ein in der Dokumentation nicht genanntes `tool_use_id`; Werkzeugnamen `read` und `exec`; Blockieren über Exit 2. Die Umstellung auf fail-closed ist mit `CR-2026-026` je Pack entschieden. **Dabei fiel auf, dass die Hook-Datei des Packs gar nicht gelesen wurde** (`AP2-DD-10`, `CR-2026-029`) | `leitwerk-core/tests/protocols/2026-09-11-AP2-devin-desktop.md` |
| V4 | Skill-Discovery über `.agents/skills/` durch Devin Local; Verhalten der `@skills:`-Erwähnung im Desktop; Grenze „ein Skill aktiv" | FW-CORE-08 Abschnitt 2, K-12 |
| V5 | Toleranz unbekannter Frontmatter-Schlüssel in SKILL.md (D-08 bleibt unabhängig davon bestehen) | Skill-Standard, K-18 |
| V6 | Struktur von `.devin/mcp_config.json` im Desktop und Status des Legacy-Pfads `~/.codeium/mcp_config.json` | `.devin/mcp_config.json.example` |
| V7 | Codebasis-Indexierung: Art, Speicherort, Abschaltbarkeit (Datenschutzmodell Abschnitt 1) | FW-CORE-02, K-20 |
| V8 | Reichweite geteilten Kontexts in Spaces | FW-CORE-02 Abschnitt 3.9 |
| V9 | Wirkung additiver Skill-`permissions` gegenüber Sitzungs- und Projektregeln in Devin Local | Skills mit `permissions`, u. a. `fw-mr-description` |
| V10 | Zeichen-/Größenbudget und Ladeverhalten der always-on-Summe (AGENTS.md + `00-*` + `20-*`) im realen Systemprompt | Laufzeitschicht gesamt |

## 31.6 Beispielartefakte (synthetisch)

Im Repository unter `leitwerk-core/examples/`: ausgefüllte Overlay-Laufzeitfassung, vollständiger Ergebnisbericht und Merge-Request-Beschreibung mit Nutzungsvermerk – alle ausdrücklich synthetisch und mit erfundenen Bezeichnern (siehe `leitwerk-core/examples/README.md`).
