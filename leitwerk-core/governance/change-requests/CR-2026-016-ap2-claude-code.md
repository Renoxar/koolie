# Änderungsantrag `CR-2026-016`

| Feld | Inhalt |
|---|---|
| Titel | Drei Befunde aus AP2: Eine Kernzusage verfiel beim Rendern, 18 Regeln waren wirkungslos, und die vorgeschriebene Prüfung war nie gelaufen |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | `clients/claude-code/manifest.json`; `install.py`; `tests/scripts/validate-framework.py`; `clients/claude-code/CLIENT_PACK.md`; `tests/protocols/2026-09-10-AP2-claude-code.md` |
| Ebene laut Entscheidungsbaum 6 | Abbildungsschicht (Client Pack) und Prüfwerkzeug |
| Art | Fehlerbehebung, sicherheitsrelevant |
| Dringlichkeit | regulär – kein Projekt setzt das Pack produktiv ein |

## 1. Anlass und Problem

`AP2` für das Client Pack `claude-code` ergab acht Befunde
(`tests/protocols/2026-09-10-AP2-claude-code.md`). Zwei davon sind schwer, ein dritter kam bei
der Behebung dazu. Alle drei haben dieselbe Ursache: **Das Pack ist nie gegen eine reale
Installation gefahren worden**, obwohl der Client die ganze Zeit erreichbar war.

**AP2-CC-01 – die Zusage S4 verfiel beim Rendern.** Die Skill-Quellen tragen `triggers: [user]`;
der Validator erzwingt das für jeden schreibenden Skill. Die Semantikabbildung verwarf das Feld
(`skill_frontmatter.drop_fields`), weil der Client es nicht kennt – **ersatzlos**. In der
installierten Fassung stand nichts mehr davon, und das Modell konnte `fw-change-small`, einen
Skill mit `Edit`, `Write` und `Bash`, selbst wählen.

Das Feld existiert beim Client: `disable-model-invocation: true`. Die Fähigkeitsmatrix führte S4
als `[NICHT ABBILDBAR]` mit genau der Frage, ob es so ein Feld gibt.

**AP2-CC-02 – 18 Regeln ohne Wirkung.** Der Client wertet Pfadregeln nur für `Read` und `Edit`
aus; eine Pfadregel für `Write`, `NotebookEdit`, `Glob` oder `MultiEdit` wird angenommen, nie
konsultiert und beim Sitzungsstart als Warnung gemeldet. Die Abbildung erzeugte je Pfad
zusätzlich eine `Write(...)`-Regel und begründete das als Verschärfung: „Ändern und Anlegen sind
getrennte Werkzeuge." Für Pfadregeln trifft das nicht zu.

In einer frischen Installation waren das 15 `Write(...)` in `deny`, eine in `ask` und ein
`Glob(**)` in `allow` – dazu ein `Grep(**)`, das nach derselben Regel nicht ausgewertet wird.
**Vier** der wirkungslosen Regeln standen in `_core_rules_integrity.deny_must_contain`: Der
Validator erzwang die Anwesenheit von Regeln, die der Client ignoriert.

**AP2-CC-03 (neu, bei der Behebung gefunden) – die vorgeschriebene Prüfung ist nie gelaufen.**
`CLIENT_PACK.md` Abschnitt 7 nennt zwei Befehle: `install.py --client claude-code`, dann
`validate-framework.py`. Führt man sie nacheinander aus, meldet der Validator **zwölf Fehler**
„triggers fehlt" – er verlangt das Feld unbedingt, während die Abbildung es für diesen Client
verwirft. Die beiden Befehle widersprachen einander seit 0.5.0.

Dieselbe Prüfung hatte einen zweiten Defekt: `allowed-tools` steht in der installierten Fassung
als **kommagetrennte Zeichenkette**, nicht als Liste. Die Prüfung `any(t in ("edit","exec",
"write") for t in tools)` lief damit über die *Zeichen* der Zeichenkette und meldete jeden
installierten Skill als nicht schreibend. Auch ohne AP2-CC-01 hätte der Validator die Verletzung
von S4 nicht sehen können.

Dass AP2-CC-01 acht Releases unbemerkt blieb, erklärt sich damit vollständig: Die Prüfung, die
es hätte finden müssen, war gegen diese Installation nie gelaufen – und hätte es auch nicht
gefunden.

## 2. Vorgeschlagene Änderung

**`triggers` bekommt eine Abbildung statt ersatzlos zu entfallen.** Das Manifest nennt ein
`model_invocation_field`; nennt die Quelle `triggers` ohne `model`, setzt die Installation dieses
Feld auf `true`. Die Aussage der Quelle bleibt damit erhalten, in der Form des Zielclients. Für
`devin-desktop` ändert sich nichts: Dort steht `triggers` im Frontmatter und wird nicht verworfen.

Verworfen wurde, `triggers` einfach stehen zu lassen: K-18 verlangt, dass das Frontmatter nur
dokumentierte Felder trägt, und ein unbekanntes Feld ist keine Durchsetzung, sondern Ballast.
Ebenfalls verworfen: die Zusage S4 für diesen Client als „nicht abbildbar" hinzunehmen und beim
`ask`-Ersatz zu belassen – der Client kann es, und eine Zusage aufzugeben, die der Zielclient
erfüllt, wäre die schlechteste aller Auflösungen.

**Pfadregeln nur für Werkzeuge, die der Client dafür auswertet.** `permission_tools.write` bildet
auf `Edit` ab, `search` auf nichts – `Read(**)` deckt den Lesezugriff ab. Die Berechtigungsdatei
schrumpft von 83 auf 65 Regeln, `_core_rules_integrity.deny_must_contain` von 17 auf 13.

Verworfen wurde, die `Write(...)`-Regeln als Vorsorge für eine künftige Clientänderung zu
behalten: Sie erzeugen heute Startwarnungen, die echte Warnungen übertönen, und täuschen einen
Schutz vor, den sie nicht leisten. Ändert der Client sein Verhalten, ändert sich das Pack – dafür
gibt es die Fähigkeitsmatrix und die Testfallklasse AK. Eine wirkungslose Regel vorzuhalten ist
das Gegenteil einer ausgewiesenen Durchsetzungstiefe (D-12).

**Der Validator prüft künftig beides.** Drei Änderungen:

1. Ein Ablageort, der `triggers` abgebildet trägt, wird nicht mehr auf das Feld selbst geprüft,
   sondern auf das abgebildete: Ein schreibender Skill **muss** die Sperre tragen.
2. `allowed-tools` wird in beiden Formen gelesen – Liste und kommagetrennte Zeichenkette –, und
   die Werkzeugnamen des Clients werden über `tool_names` auf die Verben zurückgeführt.
3. Neue Prüfung: Jede Pfadregel der Berechtigungsdatei muss ein Werkzeug nennen, für das der
   Client Pfadregeln auswertet (`permission_path_tools` im Manifest). Ohne diese Angabe
   unterbleibt die Prüfung – für `devin-desktop` ist sie unbelegt und wird deshalb nicht
   behauptet.

## 3. Prüffragen (durch Owner auszufüllen)

- [x] Richtige Ebene nach Entscheidungsbaum 6? — Ja. Die Abbildungsschicht ist keine Regelebene; sie führt keine Regel ein und lockert keine. Geändert werden das Manifest eines Packs und die beiden Skripte, die es auswerten.
- [x] Verschärfungsprinzip eingehalten? — Ja, in beide Richtungen. S4 gilt nach der Änderung technisch statt gar nicht. Die entfernten Regeln waren wirkungslos: Der Schutz von B4 und B5 trug schon vorher allein die `Edit(...)`-Hälfte, es entfällt keine wirksame Verweigerung.
- [x] Widerspruchsfreiheit geprüft? — Der Widerspruch zwischen `install.py` und `validate-framework.py` (AP2-CC-03) ist der Anlass und mit Punkt 1 und 2 behoben. Beide Befehle laufen jetzt nacheinander fehlerfrei.
- [x] Laufzeitfassungen betroffen? — Ja, bei `claude-code`: alle Skills und die Berechtigungsdatei werden neu erzeugt. Die Berechtigungsdatei ist **Saat** und wird von `--update` nicht angefasst; Migrationshinweis im CHANGELOG.
- [x] Belegstatus korrekt? — Das ist der Kern dieses Antrags. Jede Aussage stützt sich auf die Herstellerdokumentation der Clientversion 2.1.267, im Protokoll mit Zitat.
- [x] Test- und Validierungsbedarf? — Vier Sonden nach D-23, alle gemeldet (siehe Abschnitt 5). `FW-KO-01` bleibt davon unberührt; die Skill-Testfälle je `TESTS.md` sind ohnehin offen (AP2).
- [x] Auswirkungen auf Overlays und laufende Onboardings? — Kein Projekt setzt `claude-code` produktiv ein; das Übungsrepository nutzt `devin-desktop` und ist nicht betroffen. Ein künftiges Projekt mit diesem Pack bekommt eine kleinere Berechtigungsdatei und Skills mit einem zusätzlichen Frontmatter-Feld.
- [x] Dokumentation? — CHANGELOG, Decision Log, Roadmap, Client Pack, AP2-Protokoll.

## 4. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | angenommen |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Eine Abbildungsschicht, die eine Zusage beim Rendern verliert, ist schlimmer als keine: Sie erzeugt genau das falsche Vertrauen, gegen das D-12 sie eingeführt hat. Dass der Zielclient ein Feld dafür hat und das Pack es nicht kannte, macht den Befund nicht kleiner, sondern peinlicher. Und dass die vorgeschriebene Prüfung acht Releases lang nie gelaufen ist, erklärt beides. |
| Ziel-Release | 0.14.0 |
| Decision-Log-Eintrag | D-26 |

## 5. Umsetzung (nach Annahme)

- [x] AP2-CC-01: `model_invocation_field` im Manifest; `install.py` übersetzt `triggers` ohne `model` in `disable-model-invocation: true`. **9 von 12 Skills** tragen die Sperre; die drei ohne sind die rein lesenden mit `model`-Trigger
- [x] AP2-CC-02: `permission_tools.write` → `["Edit"]`, `search` → `[]`; `permission_path_tools` im Manifest. Berechtigungsdatei 83 → 65 Regeln, `deny_must_contain` 17 → 13
- [x] AP2-CC-03: Validator liest `allowed-tools` in beiden Formen, führt Werkzeugnamen über `tool_names` zurück und prüft bei abgebildetem `triggers` das Zielfeld statt des Quellfelds
- [x] Neue Prüfung: Pfadregel für ein Werkzeug ohne Pfadauswertung ist ein Fehler
- [x] **Wirksamkeitsnachweis (D-23), vier Sonden, alle gemeldet:** Sperre entfernt → Fehler; Sperre auf `false` → Fehler; `Write(leitwerk-core/**)` von Hand eingefügt → Fehler; `NotebookEdit(project-overlay/**)` → Fehler. Ausgangs- und Schlusslauf je 0 Fehler
- [x] `install.py --client claude-code` gefolgt von `validate-framework.py`: **0 Fehler** – erstmals seit 0.5.0
- [x] Framework-Repository (`devin-desktop`): 0 Fehler, 0 Warnungen; `install.py --check` unverändert
- [ ] **Folgearbeit:** Die Wirkungsnachweise aus einer Sitzung *in* der Installation stehen weiter aus (AP2-Protokoll, Abschnitt „Offen"). Sie sind der Beleg dafür, dass die Sperre auch greift – dieses Release belegt, dass sie gesetzt wird
- [ ] **Folgearbeit:** R2 und R3 stehen weiter auf `[NICHT ABBILDBAR]`, obwohl `.claude/rules/` mit `paths:`-Frontmatter sie abbildet (AP2-CC-03 des Protokolls). Eigener Antrag, weil er die Technology Packs betrifft
