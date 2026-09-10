# Änderungsantrag `CR-2026-005`

| Feld | Inhalt |
|---|---|
| Titel | Neutralisierung des Kerns: Begriffe statt clientspezifischer Pfade |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | neu: `leitwerk-core/docs/RUNTIME_GLOSSARY.md`; geändert: `framework/core/*`, `framework/role-packs/`, `framework/tech-packs/`, `governance/`, `checklists/`, `onboarding/`, `prompts/`, `examples/`, `decision-trees/`, `docs/`, `tests/TEST_CATALOG.md`, `OWNERS.md`, `README.md`, `tests/scripts/validate-framework.py` |
| Ebene laut Entscheidungsbaum 6 | Core (Redaktion) |
| Art | Änderung |
| Dringlichkeit | regulär (Review-Zyklus) |

## 1. Anlass und Problem

`CR-2026-004` hat gemessen, was D-02 bislang nur behauptete: Der als „kanonisch und werkzeugneutral" bezeichnete Kern nannte an **63 Stellen** die Laufzeitpfade genau eines KI-Clients – `AGENTS.md` (37-mal), `.devin/config.json` (17-mal), `.devin/` (16-mal) und weitere.

Die Folge war nicht theoretisch. Wer das Framework mit einem anderen Client Pack installierte, las in den Core-Modulen, Checklisten und Onboarding-Texten durchgehend Pfade, die in seiner Installation nicht existieren. Ein Kern, der so formuliert ist, ist nicht neutral – er ist nur so benannt.

## 2. Vorgeschlagene Änderung

**Ein Glossar legt die Begriffe fest** (`leitwerk-core/docs/RUNTIME_GLOSSARY.md`) und bildet sie auf die Pfade je Client Pack ab. Es ist das Gegenstück zum Platzhalterregister: dort projektspezifische Werte, hier clientspezifische Pfade.

| Begriff im Kern | `devin-desktop` | `claude-code` |
|---|---|---|
| Wurzel-Anweisungsdatei | `AGENTS.md` | `CLAUDE.md` |
| Laufzeitschicht | `.devin/` | `.claude/` |
| Berechtigungsdatei | `.devin/config.json` | `.claude/settings.json` |
| Regelablage | `.devin/rules/` | `.claude/framework/` |
| Skill-Ablage | `.devin/skills/` | `.claude/skills/` |
| Agentenprofile | `.devin/agents/` | `.claude/agents/` |
| Hook-Konfiguration | `.devin/hooks.v1.json` | in der Berechtigungsdatei |
| MCP-Konfiguration | `.devin/mcp_config.json` | `.mcp.json` |
| Nutzerlokale Überschreibung | `AGENTS.local.md`, `.devin/config.local.json` | `CLAUDE.local.md`, `.claude/settings.local.json` |

**Die Regel:** Im Kern steht der Begriff, im Client Pack der Pfad, in historischen Dokumenten bleibt beides unverändert.

**Umsetzung:** 61 der 63 Stellen redaktionell ersetzt, in sieben Durchgängen, jeweils mit anschließender Messung. Nicht ersetzt wurden zwei Stellen in Roadmap-AP2 – das Arbeitspaket validiert bewusst die Mechanismen *eines* Clients; dort steht jetzt ein Hinweis, dass es je Client Pack zu wiederholen ist.

**Nebeneffekt:** Auch die Prosa wurde vom Produktnamen gelöst, wo sie eine Eigenschaft beschreibt und keinen Beleg – „Devin passt Tests an" wurde zu „Das Werkzeug passt Tests an", „Devin-Nutzungsvermerk" zu „KI-Nutzungsvermerk".

**Decision Record D-02** wurde nicht umgeschrieben – Decision Records beschreiben eine Entscheidung zu ihrem Zeitpunkt. Er trägt jetzt einen Fortschreibungsvermerk auf D-12 bis D-14.

**Validator:** Vier Dateiklassen sind von der Fremdpfad-Warnung ausgenommen, jede mit Begründung im Code: das Glossar (dort sind die Pfade der Inhalt), Dateien im `root-template/` eines Packs (sie beschreiben ihre eigene Laufzeitschicht), `CLIENT_PACK.md` (beschreibt fremde Pfade) und historische Dokumente.

## 3. Prüffragen (durch Owner auszufüllen)

- [x] Richtige Ebene nach Entscheidungsbaum 6? — Ja, Redaktion des Kerns.
- [x] Verschärfungsprinzip eingehalten? — Ja. **Keine Regel wurde inhaltlich geändert**, nur ihre Bezugnahme auf Artefakte. Jede Ersetzung war ein Eins-zu-eins-Austausch von Pfad gegen Begriff.
- [x] Widerspruchsfreiheit geprüft? — Das Glossar ist die einzige Stelle, an der Begriff und Pfad zusammenstehen; alle anderen Kerntexte verweisen darauf. Die Begriffe waren bereits in den Client Packs eingeführt und sind damit nicht neu erfunden.
- [x] Laufzeitfassungen betroffen? — Nein. Die installierten Artefakte sind byteweise unverändert: Erstinstallation weiterhin 80 Dateien (`devin-desktop`) beziehungsweise 79 (`claude-code`), `--check` fehlerfrei.
- [x] Belegstatus korrekt? — Unverändert. Wo ein `[DOK]` an einem Pfad hing, hängt es jetzt am Begriff; die Belegkette läuft über das Client Pack.
- [x] Test- und Validierungsbedarf? — `FW-KO-04` hat den Fortschritt in jedem Durchgang gemessen (63 → 57 → 33 → 23 → 8 → 2).
- [x] Auswirkungen auf Overlays und laufende Onboardings? — Keine funktionale. Redaktionell: Onboarding-Texte nennen jetzt Begriffe; die Zuordnung zum eigenen Client steht im Glossar. Das Übungsrepository wurde mit dem neuen Kern gegengeprüft: 0 Fehler.
- [x] Dokumentation? — Glossar neu, CHANGELOG, Decision Log.

## 4. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | angenommen |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Ohne diesen Schritt wäre die Clientneutralität eine Behauptung geblieben, die jeder Leser eines Core-Moduls widerlegt hätte. Die Änderung ist rein redaktionell und lässt jede Regel inhaltlich unberührt – nachgewiesen durch byteweise identische Installationen. |
| Ziel-Release | 0.5.0 |
| Decision-Log-Eintrag | D-15 |

## 5. Umsetzung (nach Annahme)

- [x] `RUNTIME_GLOSSARY.md` mit Begriffen, Abbildungstabelle und Geltungsregel
- [x] 61 von 63 Stellen neutralisiert; die zwei verbleibenden in AP2 begründet
- [x] D-02 mit Fortschreibungsvermerk versehen, Eintrag selbst unverändert
- [x] Validator: vier begründete Ausnahmeklassen
- [x] Messung nach jedem Durchgang: 63 → 57 → 33 → 23 → 8 → 2
- [x] Regression: beide Erstinstallationen unverändert (80 / 79 Dateien), `--check` fehlerfrei, Validator gegen beide Installationen 0 Fehler, Übungsrepository mit neuem Kern 0 Fehler
- [x] CHANGELOG und Decision Log ergänzt
- [ ] Folgearbeit: gemeinsame Skill-Quelle (siehe Messung im CHANGELOG)
