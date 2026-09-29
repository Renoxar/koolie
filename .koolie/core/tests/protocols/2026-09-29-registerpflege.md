# Protokoll: Die Durchsicht der Klärungspunkte zu `1.18.1`

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-29 |
| Release | `1.18.1` (`CR-2026-158`, D-465 bis D-468) |
| Gegenstand | Alle 98 Klärungspunkte, deren Statuszelle mit „offen“ begann, dazu die Lage aller 184 Registerzeilen und die Zeile B4 der fünf Client Packs |
| Verfahren | Durchsicht am Repositorium in vier Teilen, je Punkt ein Vorschlag mit Fundstelle; Schließungen in Stichproben nachgeprüft; B4 an einer Installation jedes Packs nachgezählt |
| Kosten | ohne Kontingent – kein Sitzungslauf am Client |

## 1. Anlass

Der Owner hat am 2026-09-29 die Paketquellen zurückgestellt und nach anderen wichtigen Punkten gefragt. Das Register
nannte 98 offene Klärungspunkte – zu viele, um zu erkennen, was drängt. Die Frage war deshalb zuerst, ob die Zahl
stimmt.

## 2. Ergebnis

| Status nach der Durchsicht | Anzahl | Punkte |
|---|---|---|
| `geklärt` | 22 | mit Fundstelle: `K-10`, `K-29`, `K-33`, `K-42`, `K-45`, `K-57`, `K-59`, `K-62`, `K-82`, `K-97`, `K-111`; mit diesem Release: `K-100`; nach Entscheidung des Owners: `K-14`, `K-37`, `K-39`, `K-71`, `K-105`, `K-114`, `K-121`, `K-122`, `K-159`, `K-180` |
| `zusammengelegt mit …` | 5 | `K-43` mit `K-185`, `K-46` mit `K-56`, `K-34` mit `K-94`, `K-64` mit `K-63`, `K-112` mit `K-113` |
| `an das Projekt übergeben` | 7 | `K-04` bis `K-07`, `K-11`, `K-15`, `K-16` |
| `benannte Grenze` | 7 | `K-41`, `K-63`, `K-65`, `K-68`, `K-109`, `K-110`, `K-113` |
| `eingeplant (…)` | 36 | zehn für `1.19.0` Messapparat, achtzehn für `1.20.0` Schutzschicht, zwei für das Brainstorming, fünf beim Owner, `K-70` für `1.18.2` |
| `offen` | 21 | durchgesehen, ohne Anlass; darunter `K-155` (Paketquellen, zurückgestellt) |
| **zusammen** | **98** | |

26 der Punkte brauchten nur eine Entscheidung des Owners; sie folgen der Empfehlung der Durchsicht.

**Abweichung von der Durchsicht:** Sie schlug vor, `K-79` mit `K-69` zusammenzulegen. `K-69` ist mit `1.5.0`
beantwortet (Prüfung 89); `K-79` bleibt deshalb als eigener Punkt offen. Neu angelegt ist `K-187`.

Die übrigen 86 Registerzeilen – geklärt, verify, offen by design – tragen ihren Wert unverändert; 66 von ihnen
begannen mit einem Wort außerhalb der Legende („beantwortet mit“, „erledigt“, „entschieden (Vorschlag)“) und tragen
jetzt einen Wert der Legende vor dem unveränderten Text (D-465).

## 3. Befunde über das Register hinaus

1. 🔴 **`K-70` ist am Piloten bestätigt.** Die Berechtigungsdatei (`otp-generator`, Stand `6155af4`) sperrt Befehle
   nur als `Bash(…)` – `Bash(git push:*)`, `Bash(docker push:*)` –, der Matcher des Schutz-Hooks lautet
   `Read|Grep|Glob|Bash|Edit|Write|NotebookEdit`. `claude-code` bietet unter Windows ein eigenes Werkzeug
   `PowerShell` an. Gemessen ist nur die Konfiguration, nicht ein Lauf → `1.18.2` (D-467).
2. **`K-85` ist schärfer als geführt.** Der Pilot trägt alle 157 Protokolle versioniert im Kern, darunter die zehn
   mit Kontonamen. Die Prämisse der Zeile – kein Projekt bekommt sie – trifft beim vollen Lieferumfang nicht zu.
3. **Die Zeile B4 von vier Packs beschrieb eine Sperre, die es nicht mehr gibt.** Alle fünf Packs am 2026-09-29 in
   ein leeres Verzeichnis installiert (`install.py --target`): Keine Berechtigungsdatei führt
   `.koolie/project-overlay`, wie D-448 es seit `1.17.0` will. `cursor`, `devin-desktop`, `openai-codex` und `kiro`
   nannten sie in B4 weiter; bei `devin-desktop` zusätzlich am Baum der Stichprobe zu `1.18.0` bestätigt (D-468).
4. **`K-100` war viermal so groß wie registriert:** 114 Klärungspunkte standen in der Entscheidungstabelle, nicht
   27, und eine Leerzeile nach `K-32` teilte die Klärungstabelle.
5. **Zwei Ziele waren überholt:** `K-174` nannte `1.18.0`, `K-155` nannte `1.17.0`; die Roadmap führte noch
   `1.19.0` Paketquellen und `1.20.0` Messapparat.

## 4. Die Stichprobe des Owners zu `1.18.0` unter `devin-desktop`

Ausgewertet aus der Sitzungsdatenbank des Clients (`sessions.db`, Tabelle `tool_call_state`, Sitzung im Baum der
Stichprobe, Modus `bypass`): `git status` und `find …` wurden mit *„Permission denied for this tool.“* abgewiesen;
ein späteres `ls` lief. Die Berechtigungsdatei führt `Exec(git status)` in `allow`. Der aktive Skill
`fw-change-analyze` führt `allowed-tools: read, grep, glob` und `permissions.deny: edit, exec` – die Sperre des
Skills, die D-287 für `edit` gemessen hatte, wirkt auch für `exec` (`K-187`). Das Lesen der git-ignorierten
`.devin/mcp_config.local.json` verweigerte der Client mit eigener Meldung.

## 5. Stichproben der Schließungen

| Punkt | Nachgeprüft an |
|---|---|
| `K-33` | D-89: „`K-33` ist geschlossen, `K-34` offen“ |
| `K-97` | D-304: „`K-97` ist geschlossen“ |
| `K-62` | CHANGELOG `[0.85.0]`: „`K-62` geschlossen“ |
| `K-82` | CHANGELOG `[0.80.0]`: „`K-82` erledigt … Kriterium 2: 32 → 19“ |
| `K-111` | `RELEASE_PROCESS.md` 4.1 Schritt 4: die Freigabezeile in der Marke |
| `K-29` | `CR-2026-041` E1 angenommen, D-41 |
| `K-42`, `K-45`, `K-59` | D-162, D-128 und D-129, D-253 |

## 6. Der Abnahmelauf

Der erste Sondenlauf (beide Kodierungen, je 378 Einheiten) schlug an einer Stelle fehl, in beiden gleich: Gegenprobe 46b setzt eine Registerzeile mit der synthetischen Kennung `K-99` und dem Wert eines Decision Records, um zu zeigen, dass Prüfung 46 Klärungspunkte nicht mitzählt – und die neue Prüfung 102 meldete genau diesen Wert. Die Sonde ist ein Sondenfall, kein Registerfall: Prüfung 102 nimmt die belegten synthetischen Kennungen jetzt aus, wie Prüfung 50 es tut.

## 7. Die Vorschläge der Durchsicht je Punkt

Die folgenden Tabellen sind die Vorschläge der Durchsicht, wie sie vorgelegt wurden; übernommen ist, was Abschnitt 2
nennt. Die Statuszelle jedes Punkts trägt die Entscheidung mit ihrer Fundstelle.

### Teil 1

| K | Kurzgegenstand (≤12 Wörter) | Vorschlag | Beleg / Begründung (≤40 Wörter) | Priorität alt→neu |
|---|---|---|---|---|
| K-04 | Nutzungsumfang: nur lokal oder zusätzlich Cloud/CLI | OWNER-ENTSCHEIDUNG (Gruppe „Eingangsbedingungen“) | Rahmenseite beantwortet durch D-386 (DECISION_LOG.md:493, Ausschluss nur ohne beobachtende Person); Rest ist ein Projektwert im Overlay-Feld `templates/project-overlay/OVERLAY.md:37`. Frage: Status auf „an Projekt übergeben“ setzen? Empfehlung: ja. Wortlaut „Devin Cloud/CLI“ ist veraltet | hoch→niedrig |
| K-05 | Planstufe und Admin-Kontrollen der Organisation | OWNER-ENTSCHEIDUNG (Gruppe) | Projektwert, Feld `OVERLAY.md:36`, Checkliste `checklists/10-project-adoption.md:24`. Das Framework kann ihn nicht beantworten; `devin-desktop` CLIENT_PACK:138/142/143 verweist für „nicht beobachtet“ darauf. Empfehlung: an Projekt übergeben | mittel→niedrig |
| K-06 | Datenschutz- und Vertragsbasis mit dem Anbieter | OWNER-ENTSCHEIDUNG (Gruppe) | Als MUSS-Punkt der Übernahme verankert (`checklists/10-project-adoption.md:23`, restriktivste Auslegung ohne Ergebnis). Empfehlung: Status „an Projekt übergeben, Mindestanforderungen im Framework“ | hoch→mittel |
| K-07 | Organisationsweite KI-Richtlinie vorhanden? | OWNER-ENTSCHEIDUNG (Gruppe) | Einbindungspunkt existiert (`framework/org-policies/README.md`). Registerzeile nennt noch den alten Pfad `leitwerk-core/…`. Empfehlung: an Projekt übergeben, Pfad berichtigen | mittel→niedrig |
| K-10 | MCP-Anbindung externer Systeme im Zielprojekt | SCHLIESSEN | Mechanismus seit 1.18.0 vorhanden: Freigabe je Server mit Zweck und Werkzeugen (D-455, D-459; `OVERLAY.md:182` und Abschnitt 13.2); K-178 steht auf „beantwortet mit 1.18.0“. Welcher Server freigegeben ist, ist ein Overlay-Wert | mittel→– |
| K-11 | Betriebssystem der Arbeitsplätze / Sandbox-Verfügbarkeit | OWNER-ENTSCHEIDUNG (Gruppe) | Projektwert im Feld `OVERLAY.md:38`; die Folgen für die Packs sind entschieden (D-05 zu `Autonomous`, `openai-codex` CLIENT_PACK:108). Wortlaut nennt nur Devin. Empfehlung: an Projekt übergeben | mittel→niedrig |
| K-14 | Zyklus der Aktualitätsprüfung gegenüber Produktänderungen | OWNER-ENTSCHEIDUNG | `governance/RELEASE_PROCESS.md:22` führt weiter `<TBD: Prüfzyklus, Vorschlag quartalsweise>`. Frage: Welcher Zyklus gilt? Empfehlung: quartalsweise plus vor jedem Release, das eine Zielspanne berührt; bei fünf Packs dringlicher. Wortlaut „Devin“ veraltet | niedrig→mittel |
| K-15 | Zielwerte für Metriken | OWNER-ENTSCHEIDUNG (Gruppe) | Der Status sagt „offen by design“: Zielwerte gibt das Framework bewusst nicht vor. Frage: Als „geklärt (by design)“ schließen? Empfehlung: ja; die Werte setzt der Pilot (`build/doc/32-abschluss.md:62`) | mittel→– |
| K-16 | Pilotzeitraum | OWNER-ENTSCHEIDUNG (Gruppe) | Längst ein Projektparameter: `docs/PLACEHOLDER_REGISTRY.md:73` (`<PILOT_DURATION>`, „vor Pilotstart“), Checkliste 10:56. Empfehlung: als „in Platzhalter überführt“ schließen | niedrig→– |
| K-29 | Sperrt der Ausfall von S5 als Kernzusage die Inbetriebnahme? | SCHLIESSEN | CR-2026-041 ist angenommen (E1: sperrt nicht). D-41 (DECISION_LOG.md:130) definiert die Kernzusage, `clients/README.md:60` ebenso, und Prüfung 25 setzt das durch. Der Registerstatus „vorgelegt“ ist veraltet | hoch→– |
| K-30 | Mehrere Client Packs in einem Repositorium | BEHALTEN | Weiterhin durch D-45 ausgeschlossen; kein späterer Beschluss. Mit fünf Packs realistischer, aber ohne Anlass. Laut Register „nicht vor Abschluss des Piloten“ | offen→niedrig |
| K-31 | Aufnahme eines Projekts mit fremdem Agenten-Framework | EINPLANEN C | Ungelöst, auch in `docs/ADOPTION_GUIDE.md:199` so benannt. Die Koexistenz mit anderen Agenten-Frameworks (z. B. solchen, die CLAUDE.md-Abschnitte erzeugen) ist eine Frage des Marktvergleichs | hoch (bedingt)→hoch (bedingt) |
| K-32 | Entwicklungsweg, falls der Shell-Schreibweg geschlossen wird | BEHALTEN, an B gekoppelt | Der Auslöser ist nicht eingetreten: `hook-check-secrets.py:170-177` sagt „Kanal steht offen“. D-447 (Mandat: befristet, nur durch den Menschen, sichtbar) liefert die Bauform der Antwort. Kommt in B eine Pfadprüfung für die Shell, wird K-32 dort fällig | hoch (bedingt)→unverändert |
| K-33 | Ist der Skillaufruf bei devin-desktop ein Werkzeugaufruf? | SCHLIESSEN | D-89 (DECISION_LOG.md:178): „K-33 ist geschlossen, K-34 offen“. Ebenso `clients/devin-desktop/manifest.json:125`, CLIENT_PACK.md:242 und CR-2026-065 E4. Die Registerzeile wurde nie umgestellt | mittel→– |
| K-35 | Inhalt der Pfadschlitze gegen das Overlay prüfen | EINPLANEN B (Restumfang) | `<EXCLUDED_PATHS>` ist durch Prüfung 59(c) abgedeckt (D-171, Lese- und Schreibsperre je Glob), `<READ_ONLY_PATHS>` durch Prüfung 89 (D-357). Offen sind nur `<CI_CONFIG_PATHS>` und `<QUALITY_GATE_CONFIG_PATHS>`. Die Prüfung ist billig und hat dieselbe Bauform wie 89 | mittel→mittel |
| K-37 | Versionszelle der Vorlagen: eigener Wert oder Schlitz? | OWNER-ENTSCHEIDUNG | Weiter offen. Die Vorlagen werden faktisch gepflegt (SKILL_TEMPLATE `0.1.5`, `clients/_template` `0.3.3`). Frage: Ist die Version Eigentum der Vorlage? Empfehlung: ja, dazu ein Ausfüllhinweis „neues Modul beginnt bei 0.1.0“ analog zur Statuszelle | mittel→niedrig |
| K-38 | Meldung von Prüfung 46: zurückgefallen oder vollständiger? | EINPLANEN A | Der Meldetext ist unverändert (`validate-framework.py:6182`). Fall ein zweites Mal aufgetreten (Protokoll 2026-09-18 0.59.0:63). Er gehört zur Wartbarkeit der Prüfwerkzeuge | niedrig→niedrig |
| K-39 | Ist docs/ROADMAP.md ein Modulträger? | OWNER-ENTSCHEIDUNG | Eine der drei Beobachtungen ist überholt: Die Steckbriefversion wird inzwischen gepflegt (`0.4.10` statt `0.2.0`). D-128 führt die Roadmap als Chronik-Ausnahme von Prüfung 48. Frage: Modulträger bleiben? Empfehlung: ja, schließen | niedrig–mittel→– |
| K-40 | Geprüfte Clientversion innerhalb der Zielspanne nachrechnen | EINPLANEN A | Es gibt keine Prüfung. Der Grund der Vertagung („keine neue Prüfung, solange eine Zahl zu senken ist“) ist entfallen, weil die Kriterien 2–4 auf 0 stehen. Ein Präfixvergleich ist billig; die Grenze ist benannt (D-Zeile 247, CR-2026-087) | mittel→mittel |
| K-41 | Ort und Durchsetzung der [TECHNISCH]-Norm | OWNER-ENTSCHEIDUNG | Die Norm hat inzwischen einen Ort: `clients/README.md:69` („MUSS gegen eine reale Installation belegt sein“) und `01-governance.md:58` Nr. 7. Offen ist nur die Durchsetzung. Frage: „Satz ohne Prüfung“ als Bauform annehmen (wie D-120, D-121)? Empfehlung: ja, schließen | mittel→niedrig |
| K-42 | Testblätter an das Präparationsregister anschließen | SCHLIESSEN | D-162 zieht die Trennlinie (nur Repositoriumszustände brauchen `UEB`). K-66 ist mit 0.64.0 erledigt (UEB-09ff.). Nachgezählt: 12 von 13 Blättern nennen `UEB-` (vorher 1), und Kriterium 2 steht auf 0 | mittel→– |
| K-43 | Zählt die Overlay-Zeichengrenze den Client-Kopf mit? | ZUSAMMENLEGEN mit K-185 | D-387: Die 6.000er-Grenze ist nur noch eine Warnung, verbindlich ist die Summe von 40.000, die den Kopf ohnehin enthält. Der Rest ist eine Budgetfrage wie K-185 (B) | niedrig→niedrig |
| K-44 | Prüfung der im Overlay behaupteten aktiven Packs | EINPLANEN B | Weiter ungeprüft. Prüfung 72 (D-238) hält nur Skills gegen die Berechtigungen. `install.py:180ff.` leitet die Aktivierung aus dem Ziel ab, nicht aus dem Overlay. Der Vertagungsgrund „nur Prosa“ ist teils entfallen: `OVERLAY.md:131` hat jetzt ein Feld für Tech Packs. Mehrfach gemessen (Bündel 4/5) | hoch→hoch |
| K-45 | Prüfung 14: Produktbedingung, Warnung Kern/Projekt, historische Dokumente | SCHLIESSEN | Alle drei Teile sind erledigt: D-129 (kein Clientname im Kern, auch nicht mit Zusatz) und D-128 (Prüfung 48 nur über anweisende Kernträger, Chronik ausgenommen, Warnung aus Prüfung 12 entfernt, `validate-framework.py:2094-2098`) | mittel→– |
| K-46 | Gehört TESTS.md in die Laufzeitschicht des Projekts? | ZUSAMMENLEGEN mit K-56 | Gleicher Gegenstand wie K-56 („Testblatt als Regelquelle ausgeliefert“). `install.py:701-723` kopiert weiter das ganze Skillverzeichnis. Zusammen in A einplanen (Testblätter, Messapparat) | mittel→mittel |

#### Auffälligkeiten

Mindestens vier Punkte stehen im Register auf „offen“, obwohl sie belegt entschieden sind: K-33 (D-89 schließt ihn wörtlich), K-29 (D-41), K-45 (D-128/D-129) und K-42 (D-162 plus K-66). Die Statusspalte wird bei Beschlüssen offenbar nicht nachgeführt, und `check_klaerungsregister` sieht das nicht. Die Gruppe K-04 bis K-07, K-11, K-15 und K-16 sind organisatorische Eingangsbedingungen aus der Devin-Erstfassung. Sie sind längst als Overlay-Felder, Checklistenpunkte oder Platzhalter abgebildet, tragen aber noch Devin-Wortlaut und den alten Pfad `leitwerk-core/`. Eine einzige Owner-Entscheidung („an das Projekt übergeben“) würde sieben Punkte bereinigen. Mehrere Vertagungen (K-40, K-35, K-38, K-44) beriefen sich auf die Anweisung „keine neue Prüfung, solange eine Zahl zu senken ist“. Da die Kriterien 2–4 auf 0 stehen, trägt dieser Grund nicht mehr. Dubletten über meine Teilmenge hinaus: K-46 und K-56 haben denselben Gegenstand, K-43 hängt an K-185. CR-2026-071:205 nennt K-16 als „offen by design“, das Register führt aber K-15 so (Zuordnungsfehler in CR oder Register). Außerdem führt K-100 (27 Klärungspunkte in der falschen Tabelle) seit 0.88.0 weiter „offen“.

### Teil 2

| K | Kurzgegenstand (≤12 Wörter) | Vorschlag | Beleg / Begründung (≤40 Wörter) | Priorität alt→neu |
|---|---|---|---|---|
| K-47 | `allow`-Korb verbreitert, `deny`-Präfix erfasst `git -C … push` nicht | EINPLANEN B | Unverändert offen (TEST_CATALOG.md:128, claude-code CLIENT_PACK.md:119). Die billige Zwischenstufe (allow umschließt deny-Präfix) ist eine Schutzschichtprüfung. Auslöser derzeit nicht erfüllt: otp-generator gibt nur fünf lesende `git`-Präfixe frei. | hoch (bedingt) → mittel |
| K-48 | Verweis innerhalb eines Trägers (Zeilenkennung) wird nicht geprüft | BEHALTEN | Keine spätere Prüfung/D-Zeile dazu; letzte Nennung CR-2026-081:111. Prosaerkennung, dieselbe Grenze wie Prüfung 29; kein aktueller Anlass. | mittel → niedrig |
| K-49 | Befehle mit Arbeitsbaum-Wirkung weder in `deny` noch `allow` | BEHALTEN | Nie ausgezählt (Protokoll 2026-09-17 Abschn. 8/416). Fällt faktisch auf Abweisung/Rückfrage; die Aufzählung ist unbegrenzt – der Punkt trägt selbst den Grund der Vertagung. | mittel → niedrig |
| K-51 | Sondenlauf-Auflage D-49 an Gegenstand statt Release binden | EINPLANEN A | Nirgends entschieden (CR-2026-079:159, CHANGELOG:7439). Die „saubere Form“ (Pfadmenge aus probe-pruefungen.py gegen `git diff`) ist genau Messapparat-/Modularisierungsarbeit von K-174. | niedrig → niedrig |
| K-54 | Laufzeitschicht verbietet Lockerung unbedingt, kennt registrierte Ausnahmen nicht | EINPLANEN B | `framework/runtime/root-instruction.md:17` weiterhin „nie lockern“ ohne Vorbehalt; nur noch als Bauform-Zitat genannt (D-330-Zeile DL:440). Änderung trifft die Wurzeldatei → zusammen mit K-185-Budget in B, nicht einzeln. | mittel → hoch |
| K-34 | Ist Skillaufruf bei `devin-desktop` per Berechtigungsdatei sperrbar? | ZUSAMMENLEGEN mit K-94 | Weiter offen (devin CLIENT_PACK.md:93, manifest.json:125, `permission_tools.skill: []`). K-94 (Builtin `upload-secrets`) hängt genau daran, ob eine wirksame Skill-Sperre existiert; eine Erhebung beantwortet beide → B. | mittel → hoch |
| K-57 | Neun von zwölf `fw-*`-Skills für das Modell gesperrt | SCHLIESSEN | D-451 (DL:558, CR-2026-156 E7): lesende Skills `fw-plan`, `fw-change-analyze`, `fw-bugfix-prepare` bekommen `model`, schreibende bleiben `user` („Verworfen: allen Skills model“), Prüfung 100. Nachgezählt: heute 6 von 13 mit `model`. | hoch → – |
| K-58 | Abschnitt 17 hält nicht gegen Werkzeugmeldung stand | BEHALTEN | Abschnitt 17 mit D-451 neu gefasst („abgewiesen … ist ein Ergebnis, kein Hindernis: Bitte um den Aufruf“). Gemessen ist diese Form gegen eine Abweisungsmeldung nicht (Protokoll 2026-09-27 ohne solche Zelle). Schließbar nach einer Zelle. | mittel → niedrig |
| K-56 | Testblatt `TESTS.md` wird als Regelquelle ausgeliefert | EINPLANEN A | `install.py:701ff` liefert weiterhin jede Datei des Skillordners aus; CHANGELOG:4403 benennt die Folge wiederholt. Wohin Ergebniszellen gehören, entscheidet der Messapparat (A) – dort Owner-Wahl zwischen den drei Wegen. | mittel → mittel |
| K-59 | Zweiter Einsatzkontext fehlt in drei anweisenden Fassungen | SCHLIESSEN | D-253 (DL:360, CR-2026-117): Verweis statt Ausnahme, `FW-KO-05` abgenommen; TEST_CATALOG.md:70 „B4 (G-11) mit diesem Release“. Die Registerzeile selbst sagt „🟢 Entschieden mit 0.84.0“ und steht trotzdem auf „offen“. | mittel → – |
| K-60 | Stuft ein Client die Grenzfälle tatsächlich so ein? | BEHALTEN | Kein Testfall seither (EDGE_CASES.md:61, validate-framework.py:3810 verweisen nur). Eigene Zelle erhöhte Kriterium 2 (steht auf 0); Mehrwert gegenüber Einzelfällen ungeklärt. | mittel → niedrig |
| K-61 | Ein `bestanden` eines Konsistenztests altert unbemerkt | EINPLANEN A | Kein Mechanismus gebaut; nur Einzelnachprüfungen (TEST_CATALOG.md:70, :152 „altert ab dem Abnahmetag“; Protokoll 2026-09-22-quellenzuordnung:229). Weg 3 (Zelle nennt Stand, Checkliste hält dagegen) ist deterministische Vorprüfung im Sinne K-174. | mittel → mittel |
| K-62 | 29 von 43 `[DOK]`-Zeilen ohne Quellenangabe | SCHLIESSEN | D-263 bis D-268, Prüfungen 73/74 (0.85.0); CHANGELOG.md:3464 „`K-62` geschlossen“; CR-2026-118:8; ROADMAP.md:87 „erledigt“. Rest `M3` ist an `FW-AK-01` übergeben. | hoch → – |
| K-63 | Kontoskillquelle `claude-code` nicht aus versionierter Datei abschaltbar | OWNER-ENTSCHEIDUNG | Weg (3) seit 0.62.0 umgesetzt (claude-code CLIENT_PACK.md:153), (1)/(2) nie entschieden. Frage: Ist das Benennen die endgültige Antwort? Empfehlung: ja, Wege 1 und 2 verwerfen, als „dauerhaft benannt“ schließen (wie K-20). | hoch → mittel |
| K-64 | Organisationsseitige Skillquelle `devin-desktop` („Indexed repos“) ohne Schalter | ZUSAMMENLEGEN mit K-63 | Register nennt es selbst „das Gegenstück zu K-63“; einzige Abhilfe ist Benennen, erfolgt in devin CLIENT_PACK.md:149 (X1, zweite Grenze) und :150 (X2, K-20). Mit K-63 gemeinsam entscheiden. | mittel → mittel |
| K-65 | ACP-Schalter entfallen – Freigabezeile des Overlays ohne technische Seite | OWNER-ENTSCHEIDUNG | devin CLIENT_PACK.md:149 führt die Zeile bereits als „organisatorische Auflage“ ohne technische Seite. Frage: Genügt das, oder je Pack eine Zeile „Schranke/Auflage“? Empfehlung: genügt – schließen; die allgemeine Frage in K-184/B mitnehmen. | mittel → niedrig |
| K-67 | Overlay-Vorlage kennt drei Bindungsformen, keine verbindliche | BEHALTEN | D-353 (CR-2026-136 E4): bewusst keine Voraussetzung von 1.5.0, MAJOR-Kandidat ohne Ziel-Release (DL:460, :477). Echter offener Gegenstand, kein Anlass vor einem MAJOR. | mittel → niedrig |
| K-68 | Backend-Strang des Übungsrepositoriums nirgends übersetzbar | OWNER-ENTSCHEIDUNG | Unverändert: `java`/`mvn` auf diesem Arbeitsplatz weiterhin nicht vorhanden (geprüft). Frage: Werkzeugkette aufsetzen oder Grenze dauerhaft benannt? Empfehlung: dauerhaft benennen (wie K-20), solange keine Zelle einen Backend-Lauf verlangt. | mittel → niedrig |
| K-70 | Zweites Ausführungswerkzeug (`PowerShell`) an Berechtigung und Hook vorbei | EINPLANEN B | Offen: `clients/claude-code/manifest.json` `hook_tools.exec = ['Bash']`, `permission_tools.exec = ['Bash']`, „PowerShell“ in keinem Pack-Träger. Gleiche Bauform wie K-184 (Werkzeug am Matcher vorbei) → dieselbe gemessene Schutzschicht-Arbeit. | hoch → hoch |
| K-71 | Einmalige, nicht reproduzierte Abweichung bei Gegenprobe 44a | OWNER-ENTSCHEIDUNG | Messung erbracht, vier Läufe grün (CHANGELOG:5990); in keinem Protokoll nach 2026-09-19 erneut gemeldet. Frage: als „unerklärt, nicht reproduziert“ schließen? Empfehlung: ja, mit Vermerk; bei Wiederauftreten neuer Punkt. | mittel → niedrig |
| K-76 | Wiederherstellungsschritt `fw-refactor` Schritt 5 nicht messbar | OWNER-ENTSCHEIDUNG | Weiter „Rücknahme unbelegt“ (Protokoll 2026-09-26-skill-anweisungen:72). Frage: Falle-Präparation, `review`-Zelle oder allgemeine Regel? Empfehlung: (2) `review`-Zelle und Schritt als `[DOK]` ausweisen; eine Falle misst die Präparation. | mittel → mittel |
| K-79 | Zehn Overlay-Werte in keiner bindenden Laufzeitschicht | ZUSAMMENLEGEN mit K-69 | Nachgezählt: `test-devin-framework/.devin/rules/20-project-overlay.md` bindet 0 der 10 (Stand a7815dd, 2026-09-28); Vorlage bindet 8. CR-2026-117:238 und DL:364 führen K-79/K-69 nur noch gemeinsam („Zähler, keine Antwort“). | hoch (Messtag B4, abgelaufen) → mittel |
| K-82 | Zwölf ungemessene Zellen Bündel 4 brauchen Nachlauf | SCHLIESSEN | Nachlauf mit 0.80.0 gefahren: CHANGELOG.md:4005 „`K-82` erledigt … Kriterium 2: 32 → 19“; ROADMAP.md:81/82 „ERLEDIGT“; CR-2026-113:92. Register steht trotzdem auf „offen (CR-2026-108 E1)“. | hoch → – |
| K-85 | Zehn Aufzeichnungen tragen den Kontonamen einer natürlichen Person | OWNER-ENTSCHEIDUNG | Nachgezählt: weiter 10 Dateien, keine neue seit 2026-09-19. **Prämisse falsch:** `otp-generator/.koolie/core/tests/protocols` (VERSION 1.18.0, versioniert) enthält dieselben 10 – ausgeliefert. Frage: Aufzeichnungen beim Heben ausnehmen oder Bestand pseudonymisieren? Empfehlung: ausnehmen. | mittel → hoch |
| K-86 | Drei `ohneskill`-Kontrollläufe ohne Zurechnung | EINPLANEN A | Unverändert offen (DL:340/342, CR-2026-113:87); Kosten gerechnet ~3 USD. Idealer erster Nachlauf für den Messapparat (Cache, kleineres Modell, deterministische Vorprüfung). | mittel → niedrig |

#### Auffälligkeiten

Drei Punkte (K-59, K-62, K-82) sind nachweislich erledigt und stehen im Statusfeld weiterhin auf „offen“ – bei K-59 und K-62 sogar mit „🟢 Entschieden/Erledigt“ im selben Feld; der Status wird offenbar nicht mitgeführt, sobald der Text einen Nachtrag bekommt. K-57 ist durch D-451 beantwortet, ohne dass D-451 die Kennung nennt (D-451 zitiert „neun von dreizehn“ als Befund des Projekteinsatzes) – eine Dublette über Kennung und Befund hinweg, die kein grep auf „K-57“ findet. K-85 ist schärfer als geführt: Die Annahme „Quellrepositorium, das kein Projekt ausgeliefert bekommt“ stimmt nicht; `otp-generator` trägt die zehn Aufzeichnungen mit Kontonamen versioniert im Kern. K-71 bis K-98 stehen weiterhin in der Entscheidungstabelle (Abschnitt 2, K-100 unverändert offen), davon betroffen sind sechs Punkte dieser Teilmenge. Zur Klasse „Werkzeug am Hook-Matcher vorbei“ gehören K-70, K-184 und mittelbar K-34/K-94; sie sollten in B als ein Gegenstand gemessen werden – die triagierende Claude-Code-Sitzung selbst bietet unter Windows ein `PowerShell`-Werkzeug an (Beobachtung, keine Messung unter Framework-Einstellungen).

### Teil 3

| K | Kurzgegenstand (≤12 Wörter) | Vorschlag | Beleg / Begründung (≤40 Wörter) | Priorität alt→neu |
|---|---|---|---|---|
| K-92 | Hook ohne, Berechtigungsschicht mit Groß-/Kleinschreibung – welche gilt? | EINPLANEN B | Bereits als B-Punkt vorgesehen. Keine spätere D-Zeile entscheidet die Richtung (letzte Nennung D-277/D-306). `hook-check-secrets.py:715 aufloesen()` löst per `realpath` auf, die Berechtigungsschicht bleibt ungemessen beim Schwesterpack. | hoch→hoch |
| K-93 | Skill-Frontmatter wirkt nur mit `allowed-tools` UND `permissions` zusammen | EINPLANEN B | Alle 13 Skills führen weiterhin beide Felder (nachgezählt). Validator verlangt nur `allowed-tools` (`validate-framework.py:1793`), `permissions` nicht. Der Grund für die Zurückstellung („keine neue Prüfung, solange eine Zahl zu senken ist“) ist entfallen. Die Prüfung ist billig. | mittel→mittel |
| K-94 | Eingebauter Skill `upload-secrets` vs. Zusage `B3` ungemessen | EINPLANEN B | Keine Messung nach D-288 gefunden. `devin-desktop/CLIENT_PACK.md:29` sagt weiterhin „ungemessen“. Gehört zur Schutzschicht und braucht die eigene Freigabe nach D-34 vor dem Lauf. | hoch→hoch |
| K-96 | POSIX-Pfad `/c/…` unter MSYS verlässt das Projekt unbemerkt | EINPLANEN B | Keine spätere Entscheidung. `aufloesen()` (`hook-check-secrets.py:715–745`) behandelt die MSYS-Form nicht eigens. Selber Ort wie K-92 (Pfadidentität an der Auflösung, D-63): gemeinsam messen. | mittel→mittel |
| K-97 | Auf welchem Konto und Modell wird künftig gemessen? | SCHLIESSEN | D-304 (DECISION_LOG:411): „`K-97` ist geschlossen: … bleiben auf `SWE-1.6 Slow` eingefroren“. Auch CR-2026-122:12 und CHANGELOG:2760. Nur die Statusspalte beginnt noch mit „offen“. | hoch→– |
| K-98 | Markerform außerhalb des Zählbereichs von Prüfung 46 durchsetzen? | EINPLANEN A | Laut eigener Zeile ist der Punkt entscheidbar, sobald keine Zahl mehr offen ist. Das trifft seit 1.0.0 zu. README und `build/doc` sind heute frei von der Markerform (grep). Es geht um einen Zählbereich: passt zur Validator-Neuordnung in A. | niedrig→niedrig |
| K-100 | Klärungspunkte stehen in der Entscheidungstabelle statt in Abschnitt 1 | EINPLANEN A | Nachgezählt: nicht 27, sondern **114** K-Zeilen stehen in Abschnitt 2 (DECISION_LOG:265–654). Abschnitt 1 endet bei K-70 (Zeile 80). Zusätzlich fehlt ein Statusvokabular (CR-2026-125:188). Diese Triage zeigt die Folgen. | mittel→hoch |
| K-101 | Namensableitung in mehreren Trägern ohne bindenden Mechanismus | BEHALTEN | Die Trägermenge ist veraltet: `UEBERGABE.md` ist lokal (D-350), die ROADMAP enthält die Ableitung nicht mehr. Heute steht sie in `README.md:159`, `build/doc/00-kopf.md:16` und D-125. Zu binden wären höchstens README und `00-kopf`. | niedrig–mittel→niedrig |
| K-102 | Zurechenbarkeit nur über Bündel 1–3 ausgezählt | BEHALTEN | Keine spätere Auszählung in `tests/protocols` gefunden. Das Ergebnis wäre eine Auswertung vorhandener Protokolle ohne Kontingent. Derzeit hängt kein Anlass daran (Vortrag). | mittel→niedrig |
| K-104 | Prüfung auf Aussagen der Wurzel-README doch baubar? | BEHALTEN | Keine README-Prüfung gebaut. Der Validator (`:9430`) nennt „den Rest von K-104“ ausdrücklich. Die README ist seit 1.15.0 neu geschrieben, die Statuszeile (`README.md:13`, „Pilot“) wäre der mechanische Gegenstand. | mittel→niedrig |
| K-105 | Foliensatz außerhalb des Repos mit ungeprüften Zahlen | OWNER-ENTSCHEIDUNG | Frage: Zahlen durch einen Standverweis ersetzen, oder den Abgleich als Posten in die Release-Checkliste aufnehmen? Seit D-332 keine Entscheidung, kein Posten in `checklists/11-*`. Empfehlung: Verweis statt Zahlen (1), sonst Checklistenposten (3). | mittel→mittel (vor Termin) |
| K-106 | Aufzählung synthetischer Kennungen entgeht Prüfung 50 | BEHALTEN | Keine Prüfung gebaut, keine D-Zeile gefunden. Die Selbstbezüglichkeit (die Prüfung würde zur Fundstelle) bleibt ungelöst. Kein Anlass. | niedrig→niedrig |
| K-109 | Keine Prüfung setzt „Rollen statt Personen“ durch | OWNER-ENTSCHEIDUNG | Frage: Wird die Regel als reine Anweisung ausgewiesen, statt behauptet zu werden? Der Validator kennt nur die projektlokale `forbidden-terms.txt` (`:1889`). Empfehlung: Option (3) ausweisen, dazu die Ausnahme D-323 in README:393 benennen. | mittel→mittel |
| K-110 | Erreicht eine Prüfung Lieferungserzeugnisse (build/out, Archiv)? | OWNER-ENTSCHEIDUNG | Frage (1) ist nach dem Zeilentext mit nein beantwortet. Der Verfahrensschritt steht in `checklists/11-framework-release.md:58` (D-332). Frage: Als benannte Grenze schließen? Empfehlung: ja, Option (3). | mittel→niedrig |
| K-111 | Soll RELEASE_PROCESS die Freigabezeile in der Marke vorschreiben? | SCHLIESSEN | Umgesetzt: `RELEASE_PROCESS.md:53` Schritt 4 „… **und die Freigabezeile** … (D-334, `K-111`)“ und `checklists/11-framework-release.md:59`. CHANGELOG:1922 „nennen die Freigabezeile seit diesem Release“. Frage (1) ist damit bejaht, (2) gegenstandslos. | mittel→– |
| K-112 | Prüfung auf vollständige Nennungen eines Releases, nicht nur Spanne | ZUSAMMENLEGEN mit K-113 | Selber Gegenstand (vollständige Entscheidungsmenge je Release). Die eigene Frage (2) führt ausdrücklich zu K-113. D-335/D-338 nennen beide gemeinsam. | mittel→niedrig |
| K-113 | Markentext in den Arbeitsbaum spiegeln? | OWNER-ENTSCHEIDUNG | Die Vorbedingung „K-111 zuerst“ ist erfüllt (s. o.). Frage: Markentext spiegeln, oder die Grenze dauerhaft ausweisen? Empfehlung: ausweisen (2). Validator:610 und :9891 benennen die Grenze bereits. Mit K-112 schließen. | mittel→niedrig |
| K-114 | Reservierter Sondenbereich D ≥ 900 ohne Durchsetzung | OWNER-ENTSCHEIDUNG | Heute höchste Vergabe D-464 (Abstand 436, nicht 560). Frage: Genügt der Abstand mit Wiedervorlage? Empfehlung: ja, Option (1), Wiedervorlage bei der Nummer 713 (zwei Drittel des Abstands ab D-340). | niedrig→niedrig |
| K-116 | Prüfung 85 sieht Zielangabe, nicht Stand eines Planpostens | BEHALTEN | Keine Erweiterung gebaut. Die ROADMAP führt nur zwei `Geplant`-Abschnitte (Zeilen 271 und 279), beide mit künftigem Ziel. Geringes Risiko. | niedrig→niedrig |
| K-118 | Vertrauenseintrag bei `openai-codex` außerhalb jeder Prüfung | EINPLANEN B | Frage (3) ist teilweise durch D-395 beantwortet: `install.py` nennt den Vertrauensschritt, auch das erneute Vertrauen nach einer Hebung. Offen bleibt laut D-395 („prüft nicht, ob sie getan sind (`K-118` bleibt offen)“) Frage (2): Konfiguration lesen und melden. Das gehört zur Schutzschicht. | hoch→mittel |
| K-119 | Arbeitsplatz- vs. Projektbefehlsregel bei `openai-codex` – wer gewinnt? | EINPLANEN B | Keine Erhebung gefunden. Der Pack erhebt nur „innerhalb einer Menge“ (`CLIENT_PACK.md:119`). Eine kleine Messung (zwei Regeldateien, `execpolicy check` und ein Lauf) entscheidet über die Bedingung an `B6`. Passt in das gemessene Schutzschicht-Release. | mittel→mittel |
| K-121 | Schreibrückfrage bei `devin-desktop` für Professionals abschaltbar? | OWNER-ENTSCHEIDUNG | Frage (3) ist beantwortet (D-353), (1) und (2) sind offen. Spätere D-Zeilen (D-382, D-459) regeln nur MCP und Begriffe. Frage: Wird die Schreibrückfrage ein Overlay-Wert? Empfehlung: nein, solange K-120 ohne Prüfung ist. Bis dahin gilt die Sitzungsfreigabe (M3). | mittel→mittel |
| K-122 | Große Entwicklungsträger (CHANGELOG, DECISION_LOG u. a.) in Nachweisschicht? | OWNER-ENTSCHEIDUNG | Keine spätere Entscheidung nach D-367. Frage: Lohnt eine zweite Gattung für rund 26 % der Bytes? Empfehlung: nein und schließen, weil die Regeln auf D-Kennungen verweisen (die Zeile begründet das selbst). | niedrig→niedrig |
| K-152 | Übungs- und Messrepositorium trennen | BEHALTEN | Der Auslöser ist definiert: „sobald ein zweites Projekt ein Übungsrepositorium aufbaut“ (D-400, DECISION_LOG:507). Kein solcher Fall ist belegt. | niedrig→niedrig |
| K-155 | Installation über öffentliche Paketquellen (PyPI, winget …) | BEHALTEN | Der Status ist falsch geführt: Die Registerzeile sagt „eingeplant für `1.17.0`“, D-445 verschob auf 1.19.0, `ROADMAP.md:271` führt „Ziel-Release 1.19.0“. Laut Owner ohne Ziel zurückgestellt. Register und ROADMAP-Abschnitt nachziehen. | niedrig→niedrig |

#### Auffälligkeiten

1. **Status falsch geführt:** K-97 ist durch D-304 geschlossen, seine Statusspalte beginnt aber mit „offen“. Die Zählung liest den Punkt deshalb als offen. K-111 ist durch `RELEASE_PROCESS.md:53` umgesetzt und trotzdem offen geführt. Der Zählung nach offener Punkte ist nicht zu trauen, solange es kein Statusvokabular gibt (K-100).
2. **K-100 ist weit größer als registriert:** 114 statt 27 K-Zeilen stehen unter den Überschriften der Entscheidungstabelle (DECISION_LOG:265–654). Jeder seit 0.88.0 neu angelegte Klärungspunkt hat den Befund vergrößert.
3. **Veraltete Zielangaben über meine Teilmenge hinaus:** Die Registerzeile von K-174 sagt „eingeplant für `1.18.0` (D-436)“. 1.18.0 ist aber das MCP-Release, und D-445 nennt `1.20.0`. K-155 sagt `1.17.0`. `docs/ROADMAP.md:271/279` führt Paketquellen auf 1.19.0 und Messapparat auf 1.20.0. Beides widerspricht dem aktuellen Plan (Messapparat als Nächstes, Paketquellen ohne Ziel), und Prüfung 85 würde es erst nach Überschreiten melden.
4. **Stehengebliebene Zurückstellungsgründe:** K-93, K-96 und K-98 wurden mit der „Anweisung vom 15.09.“ (keine neue Prüfung, solange eine Zahl zu senken ist) zurückgestellt. Diese Anweisung greift laut K-98 selbst seit 0.87.0/1.0.0 nicht mehr. Die Punkte sind seither ohne Grund liegen geblieben.
5. **Bündel:** K-92 und K-96 (Pfadidentität an der Auflösung, D-63) gehören in dieselbe Messung von B. K-112/K-113/K-111 bilden einen Komplex, der mit K-111 im Kern entschieden ist. K-104 und K-101 hängen beide an der Frage, wie sich die Wurzel-README prüfen lässt (Lehre aus Prüfung 75).

### Teil 4

Stand geprüft am Repositorium 2026-09-29 (nur gelesen).

| K | Kurzgegenstand (≤12 Wörter) | Vorschlag | Beleg / Begründung (≤40 Wörter) | Priorität alt→neu |
|---|---|---|---|---|
| K-158 | `render_rule`: kommagetrennte `globs` werden ein einziges `paths`-Muster | BEHALTEN | `install.py:443-449` `_globs_lesen` gibt eine Zeichenkette weiterhin als **ein** Element zurück (keine Kommatrennung). Im Kern führt keine Regel `globs:` (grep `framework`, `templates` leer). Nur projekteigene Regeln betroffen; billiger Fix mit Sonde. | mittel→mittel |
| K-159 | Falscher Startort der Sitzung wird von nichts gemeldet | OWNER-ENTSCHEIDUNG | Frage: Soll die claude-code-Wurzelanweisung einen Satz „Startort melden“ tragen? Empfehlung: nein, solange K-185 (Budget 2 Zeichen) offen ist; Bedingung steht bereits in `ADOPTION_GUIDE.md:373` und CLIENT_PACKs (Z. 110/102/112). | mittel→niedrig |
| K-160 | codex: projektrelative `deny`-Globs unter `:workspace_roots`, unerhöht | EINPLANEN B | Unverändert offen: `openai-codex/CLIENT_PACK.md:120` B3 `[NICHT ABBILDBAR]`, `clientmap.py:674` „nicht nachgemessen“. Gehört thematisch zur Schutzschicht (B3); kleine Messung (`codex sandbox` gegen Köder). | mittel→mittel |
| K-161 | devin: Regel mit `trigger: glob` lädt nicht | BEHALTEN | Weiter Vorbehalt in `devin-desktop/CLIENT_PACK.md:72` (R2). Tech Packs laden über `glob`, und devin war Client des ersten Projekteinsatzes (D-445) – Wirkung größer als eingestuft. | mittel→hoch |
| K-162 | kiro: IDE-Zeilen nicht an einer Sitzung gemessen | EINPLANEN Owner | Vorgabe: Owner übernimmt. Offen laut `kiro/CLIENT_PACK.md:163` und `clients/README.md:96`; kein späterer Messbeleg. | mittel→mittel |
| K-163 | kiro: drei Dokumentationsabweichungen an Hersteller melden | EINPLANEN Owner | Vorgabe: Owner übernimmt. Nur `CHANGELOG.md:368`, `tests/protocols/2026-09-26-bau-kiro.md:74`; keine Meldung belegt. | mittel→mittel |
| K-165 | K3-Auslöser in weiteren Skills präzisieren | BEHALTEN | Nachgezählt: fünf offen (`fw-docs-update:157`, `fw-error-analyze:157`, `fw-mr-description:167`, `fw-review-support:174`, `fw-tests:166` – „anhalten“ an K3-Fund). Zwei nachgezogen (D-451). Titel „sieben“ auf „fünf“ korrigieren. | mittel→mittel |
| K-166 | Rest „Verständlichkeit und Auffindbarkeit“: Website, Artikel, Sichtbarkeit | EINPLANEN C | Register: „Nach `1.15.0` neu bewerten“ – überfällig. Sichtbarkeit/Positionierung ist Stoff des Marktvergleichs; dort neu bewerten. `ROADMAP.md:249` führt es vorgemerkt ohne Ziel. | niedrig→niedrig |
| K-169 | Übungsmethode `auswerten` mehrdeutig (zwei Definitionen) | BEHALTEN | Nur mit nächster Messung an `fw-code-explain` sinnvoll (öffnet `SK-002-N02`). Kein späterer Beleg (nur Aufzählungen in Protokollen). Umbenennung wäre Präparation → optional mit A. | niedrig→niedrig |
| K-170 | Keine Zelle prüft Planablage `fw-plan` und Stufe hoch `fw-refactor` | BEHALTEN | Kein Fundort außer Protokollaufzählungen (`2026-09-26-attributionszeile.md:83`). Planablage wurde mit D-458 (Overlay 13.1) geändert – eine Zelle wäre jetzt dringlicher; Kandidat für B-Messung. | mittel→mittel |
| K-172 | Arbeit auf `main` in Messbäumen uneinheitlich | EINPLANEN A | Reine Präparationsfrage (Arbeitsbranch im Messbaum oder Zellerwartung); passt zum parametrisierten Messapparat. Belege weiter offen: `fw-refactor/TESTS.md:7,12`. | mittel→mittel |
| K-173 | Attributionsvorgabe bei codex, devin, kiro nicht erhoben | BEHALTEN | cursor ist inzwischen erhoben (`cursor/CLIENT_PACK.md:176`), die drei genannten nicht. Reine Doku-Recherche; ließe sich bei C (Herstellerdoku sichten) mitnehmen. | niedrig→niedrig |
| K-174 | Messapparat und Prüfwerkzeuge gezielter, günstiger, wartbar | EINPLANEN A | Statusspalte falsch: „eingeplant für `1.18.0` (D-436)“ – `1.18.0` war MCP (D-445 verschob auf `1.20.0`, `ROADMAP.md:127`). Jetzt nächstes Release A. | mittel→hoch |
| K-175 | cursor: IDE-Zeilen nicht an einer Sitzung gemessen | EINPLANEN Owner | Vorgabe: Owner. Offen laut `cursor/CLIENT_PACK.md:12,72,101,162`. | hoch→hoch |
| K-176 | cursor: Pfadmuster-Schreibweise für macOS/Linux ungemessen | EINPLANEN Owner | Vorgabe: Owner mit macOS-Starter. `cursor/CLIENT_PACK.md:64`, `bau-cursor.md:66` „aus dem Programmcode, nicht gemessen“. | mittel→mittel |
| K-177 | cursor: vier Dokumentationsabweichungen an Hersteller melden | EINPLANEN Owner | Vorgabe: Owner. Keine Meldung belegt (`bau-cursor.md:67`). | niedrig→niedrig |
| K-179 | Modusgrenzen außer M6 nur normativ | EINPLANEN B | Nur `CR-2026-156:37` (A7); keine Folgearbeit. Vorgabe B. Mandatsmuster für M2 wäre eigene Messung. | mittel→mittel |
| K-180 | Abgleich schreibt die Berechtigungsdatei nicht | OWNER-ENTSCHEIDUNG | Frage: Darf `mandat.py abgleichen` fehlende `deny`-Regeln (nur verschärfend) selbst eintragen? D-452 und D-459 (V6) verwerfen das Erzeugen der Rechte; Empfehlung: bei „nein“ schließen mit Verweis D-459 V6, sonst in B. | mittel→niedrig |
| K-181 | Overlay außerhalb Hook-Laufs (kiro nicht interaktiv) nur normativ | EINPLANEN B | Fähigkeitsmatrix nicht nachgezogen: `kiro/CLIENT_PACK.md:111` (B4) nennt weiter `deny fs_write` auf `.koolie/project-overlay/**`, obwohl `framework/runtime/permissions.json` das Overlay seit D-448 nicht mehr führt. Schutzschicht-Doku. | niedrig→mittel |
| K-183 | `fw-overlay-pflege` fragt MCP-Server nicht ab | EINPLANEN B | Vorgabe B; `CR-2026-157:62` (E14) „nicht mit diesem Release“. Kein Nachzug im Skill. | niedrig→niedrig |
| K-184 | MCP-Aufrufe erreichen den Schutz-Hook nicht | EINPLANEN B | Vorgabe B; `CR-2026-157:55` (E7) „beim Bau zurückgestellt“, `CHANGELOG.md:51`. | mittel→hoch |
| K-185 | Pilot zwei Zeichen unter 40.000-Zeichen-Budget | EINPLANEN B | Vorgabe B. Grenze im Validator `validate-framework.py:1712`. Wert 39.998 nicht nachgezählt: nur im Register belegt, Pilotablage liegt nicht im Kern; vor B neu zählen. | mittel→hoch |
| K-186 | Sechs Befunde aus Messung zu `1.18.0` | EINPLANEN B | (3) bestätigt: `fw-bugfix-prepare/SKILL.md:176` hält weiter an, `fw-change-analyze:166` gelockert. (2), (3), (5) → B; (1), (4), (6 `UEB-33`) sind Mess-/Präparationsfragen → A. Aufteilen empfohlen. | mittel→mittel |
| K-187 (neu) | devin: Skillsperre weist `git status`/`find` ab (S3 auf exec) | BEHALTEN (neu anlegen, nicht zusammenlegen) | Kein Duplikat: K-73 fragt claude-code (`disallowed-tools`), K-186 (5) ist das Gegenteil (Sperre greift nicht), K-93 die Feldkombination – hier bestätigt. Sperre ist gewollt (`fw-change-analyze/SKILL.md:12,76`, Prüfung 100, D-451). | –→niedrig |

#### Auffälligkeiten

1. **Falsch geführte Status:** `K-174` steht auf „eingeplant für `1.18.0` (D-436)“, obwohl D-445 ihn auf `1.20.0` verschoben hat und `1.18.0` MCP war; ebenso `K-155` außerhalb dieser Teilmenge („eingeplant für `1.17.0`“, `DECISION_LOG.md:637`), während `ROADMAP.md:126-127` noch `1.19.0` Paketquellen / `1.20.0` Messapparat führt – Register und Roadmap widersprechen dem neuen Plan (A → B → C, Paketquellen zurückgestellt).
2. **K-187 ist inhaltlich ein positiver Beleg**, kein Defekt: Die Sperre von `fw-change-analyze` (`allowed-tools` ohne exec + `permissions.deny: exec`) wirkt bei devin auch für `exec` und erweitert S3 (`devin-desktop/CLIENT_PACK.md:94`, bisher nur `edit` gemessen). Offen ist nur die Reibungsfrage, ob lesende Skills lesende Git-Befehle dürfen – das kollidiert mit Prüfung 100 (D-451) und wäre eine Owner-Entscheidung; `find` ersetzt `glob`. Querverweis auf K-73 und K-186 (5) genügt.
3. **Veraltete B4-Zeilen nach D-448:** Nicht nur kiro – auch `cursor/CLIENT_PACK.md:110`, `devin-desktop/CLIENT_PACK.md:109` und `openai-codex/CLIENT_PACK.md:121` nennen in B4 weiter eine statische Sperre des Overlays, während `framework/runtime/permissions.json` es nicht mehr führt (nicht geprüft, ob `clientmap.py` es je Pack wieder einfügt). Das gehört zu K-181 bzw. B.
4. **K-165** trägt im Titel „sieben“, nachgezählt sind es fünf; **K-159** und **K-185** hängen zusammen (jeder neue Satz in der Wurzelanweisung kostet Budget).
5. **K-161** dürfte wegen des devin-Projekteinsatzes höher wiegen als „mittel“; **K-170** gewinnt durch D-458 (neue Planablage nach Overlay 13.1) an Dringlichkeit.
