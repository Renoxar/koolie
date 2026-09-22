# Gegenprüfung zu B07 und B09: die Widersprüche, die nur ein Mensch entscheiden kann

| Feld | Wert |
|---|---|
| Gegenstand | **B09** – drei Regelkonflikte: K3-Einstufung, Sicherheitskonfiguration, Parallelität. **B07** – Lese- und Schreibsperre in der Overlay-Vorlage und der fehlende Weg in das eigene Repositorium |
| Anlass | Die Befunde **B07** und **B09** des unabhängigen Reviews vom 2026-09-12, beide P2 und beide ungeprüft. Nach D-23 und dem Arbeitsplan gehört jeder Befund vor der Umsetzung gegengeprüft, auch ein Befund von außen |
| Datum | 2026-09-13 |
| Framework-Version | 0.31.0 (Auscheckstand `97052c1`, Arbeitsbaum sauber) |
| Prüfmethode | **Dokumenten- und Codeprüfung.** Jede der elf Fundstellen des Reviews einzeln nachgelesen; dazu die beiden technischen Schichten – `framework/runtime/permissions.json` und `tests/scripts/hook-check-secrets.py` – auf die behauptete Vermischung geprüft, und die K3-Kategorien über alle Fassungen gezählt |
| Umgebung | Windows 11, Python 3.14.4 |
| Ergebnis | **Beide Befunde bestätigen sich inhaltlich vollständig.** Dazu **fünf eigene Feststellungen** (Abschnitte 1.1 bis 2.2), von denen zwei den Befund verschärfen, ein **Nebenbefund** zum Kernverzeichnis und eine **Berichtigung**: Drei der vier Zeilenangaben zur Wurzel-Anweisungsdatei stimmen nicht |

> **Was diese Gegenprüfung nicht ist.** Sie misst nichts. B07 und B09 sind
> Dokumentenwidersprüche; es gibt keinen Mechanismus, der sie zeigen könnte. Geprüft ist
> deshalb der Text – und dort, wo der Bericht eine Vermischung der Schutzziele behauptet,
> zusätzlich der Code, der sie angeblich trägt. **Genau dort liegt der Zugewinn:** Der Code
> trennt korrekt, und das macht den Befund schlimmer, nicht kleiner.

## 1. B09 – die drei Konflikte, Fundstelle für Fundstelle

### 1.1 K3: bestätigt, mit zwei eigenen Feststellungen

| Behauptung des Reviews | Nachgelesen | Ergebnis |
|---|---|---|
| Die Wurzel-Anweisung erklärt interne Adressen ausnahmslos zu K3 (`:83`) | `framework/runtime/root-instruction.md:84` | **bestätigt**, Zeile 84 statt 83 |
| Die Langform erlaubt eine K1-Einstufung im Overlay (`02-privacy.md:33`) | `framework/core/02-privacy.md:33`: „…, sofern nicht im Overlay ausdrücklich als K1 eingestuft“ | **bestätigt**, Zeile trifft |
| Die Langform nennt eine allgemeine Lockerungsmöglichkeit (`:42`) | `framework/core/02-privacy.md:42`, Einstufungsregel 4 | **bestätigt**, Zeile trifft |
| Die Hierarchie erklärt K3 für nicht aufhebbar (`PRIORITY_HIERARCHY.md:31`) | Regel 2.4: „Delegationsverbote und K3 sind ebenenfest“ | **bestätigt**, Zeile trifft |

**Eigene Feststellung 1 – es ist keine Pattsituation, sondern eine Minderheitsmeinung.**
Ausgezählt über das ganze Repositorium: **acht weitere Stellen** führen dieselbe Kategorie
**ohne** jede Bedingung.

| Nr. | Stelle | Art |
|---|---|---|
| 1 | `framework/runtime/rules/10-privacy-security.md:17` | Laufzeitregel, immer geladen |
| 2 | `decision-trees/01-context-allowed.md:14` | Entscheidungsbaum, normativ |
| 3 | `checklists/02-privacy-context.md:23` | Checkliste, MUSS-Punkt |
| 4 | `onboarding/REFERENCE.md:12` | Spickzettel |
| 5 | `onboarding/QUICKSTART.md:26` | Einstieg |
| 6 | `onboarding/KNOWLEDGE_CHECK.md:36` | Wissensprüfung |
| 7 | `prompts/01-understand-codebase.md:27` | Promptvorlage |
| 8 | `prompts/10-documentation.md:27` | Promptvorlage |

Gezählt sind nur Stellen, die die K3-**Kategorien aufzählen**. Nicht gezählt sind Verbote und Bereinigungspflichten, die dieselben Angaben nennen, ohne eine Klasse zu bestimmen – `framework/runtime/rules/15-development-rules.md:31`, `prompts/05-test-generation.md:89`, die Ausfüllhinweise der Vorlagen und die Prüflisten dreier Skills. Sie gehören nicht dazu, weil sie keine Einstufung aussprechen. **Eine Zahl steht hier absichtlich nicht:** Wo die Grenze zwischen einer Aufzählung und einem Verbot liegt, ist eine Ermessensfrage – eine gezählte Zahl wäre dann eine Genauigkeit, die es nicht gibt.

Die Bedingung steht an **einer** Stelle – und diese eine ist die kanonische Langform. Der
Entscheidungsbaum beschreibt sogar bereits den Weg, der nach der Entscheidung offen bleibt: „Lässt
sich der K3-Anteil vollständig entfernen oder ersetzen, wird die bereinigte Fassung neu
eingestuft.“

**Eigene Feststellung 2 – die Kurzform ist zwei Kategorien zu kurz.** Abschnitt 2.1 führt
**acht** Kategorien. Die Wurzel-Anweisungsdatei nannte **sechs**:

| Nr. | Kategorie aus Abschnitt 2.1 | in der Kurzform |
|---|---|---|
| 1 | Secrets, Zugangsdaten, Schlüssel, Zertifikate, Keystores | ja |
| 2 | personenbezogene Echtdaten | ja |
| 3 | Produktionsdaten | ja |
| 4 | nicht freigegebene Kunden-, Behörden-, Vertragsdokumente | ja |
| 5 | **Sicherheitskonfigurationen mit Schutzwirkung** | **nein** |
| 6 | interne Adressen, Hostnamen, Netzpläne, Kennungen | ja |
| 7 | als vertraulich oder höher eingestufte Inhalte | ja |
| 8 | **Inhalte aus anderen Projekten oder Mandanten** | **nein** |

Die Laufzeitregel `10-*` und die Checkliste führen alle acht. **Der Ausreißer ist die Fassung, die
in jede Sitzung lädt** – dieselbe Lehre wie bei `CR-2026-048`: Wer beim Gegenprüfen merkt, dass
eine Fassung die richtige Form hat, zieht auf sie nach. Hier ist es umgekehrt zu der Vermutung des
Berichts: Die Kurzform ist nicht der strengere, sondern der lückenhafte Text.

**Ein zusätzlicher Träger, den das Review nicht nennt:**
`framework/org-policies/MAPPING_CLASSIFICATION.md:12` bot für die Organisationsstufe „vertraulich“
eine Lockerung auf K2 an. Diese Stufe ist Kategorie 7 – die Zeile widersprach derselben Regel.

### 1.2 Sicherheitskonfiguration: bestätigt, aber nur teilweise ein Widerspruch

| Behauptung | Nachgelesen | Ergebnis |
|---|---|---|
| Die Wurzel-Anweisung lässt Umsetzung nach Sicherheitsfreigabe zu (`:90`) | `framework/runtime/root-instruction.md:91` | **bestätigt**, Zeile 91 statt 90 |
| V6 nennt Änderungen an Sicherheitskonfigurationen nicht delegierbar (`09-risk-model.md:64`) | V6, zulässige Unterstützung „Analyse und Planvorschlag“ | **bestätigt**, Zeile trifft |

**Eigene Feststellung 3 – das Framework will die eine Hälfte ausdrücklich.** Dieselbe Datei
enthält die Kontrollstufentabelle, und sie sieht für Stufe hoch vor: „Controlled Modification nur
nach dokumentierter Freigabe durch `<APPROVAL_ROLE>` und mit begleitender Person (Pairing)“. **R3**
stuft „Kryptografie, Sitzungsverwaltung, Berechtigungsprüfung, Security-Konfiguration“ als hoch
ein, **R10** jede Änderung an Authentifizierung oder Autorisierung. Ein Risikomodell, das einen
Gegenstand einstuft und die Umsetzungsbedingungen dafür nennt, verbietet sie nicht.

Der Widerspruch ist also nicht „Freigabe gegen Verbot“, sondern **zwei Sätze über zwei
verschiedene Gegenstände, von denen keiner sagt, welcher gemeint ist**: V6 nennt neben
Sicherheitskonfigurationen auch Produktionssysteme, Infrastruktur und Berechtigungen – das ist der
Betrieb. Die Wurzel-Anweisung nennt Authentifizierung, Autorisierung, Kryptografie und
Sitzungsverwaltung – das ist Anwendungslogik. Nur das vierte Glied, „Sicherheitskonfiguration“,
steht in beiden Listen.

### 1.3 Parallelität: bestätigt und verschärft – die Regel war nicht erfüllbar

| Behauptung | Nachgelesen | Ergebnis |
|---|---|---|
| R12 stuft Parallelsitzungen als hoch ein (`09-risk-model.md:38`) | R12, Spalte „hoch“: „Hintergrund-Subagenten, Parallelsitzungen oder erweiterte Permission-Modi“ | **bestätigt**, Zeile trifft |
| Das Arbeitsmodell empfiehlt sie für Aufgaben niedriger Kontrollstufe (`05-working-model.md:119`) | Abschnitt 3.1, Punkt 3: „SOLLEN nur für voneinander unabhängige Aufgaben der Kontrollstufe niedrig“ | **bestätigt**, Zeile trifft |

**Das ist mehr als eine Uneinheitlichkeit.** `framework/core/09-risk-model.md` Abschnitt 5 legt
fest, wie die Kontrollstufe bestimmt wird: „geht die dreizehn Faktoren durch, notiert den
**höchsten Treffer**“. Wer parallel arbeitet, trifft R12 hoch. Die Aufgabe ist damit Kontrollstufe
hoch – und kann die Voraussetzung des Arbeitsmodells, Stufe niedrig, **nie** erfüllen.

**Die Schnittmenge ist leer. Die Regel war seit ihrer Erstfassung nicht anwendbar** – dieselbe
Bauform wie B08, wo die Aktivierung eine Prüfung verlangt, die bereits Aktivität voraussetzt.

**Und der Lösungsvorschlag des Reviews löst es nicht.** Er lautet, Parallelität nur im für Stufe
hoch zulässigen Modus zu erlauben und die Beschränkung auf niedrige Aufgaben zu entfernen. R12
bleibt dabei unangetastet – also macht auch danach ein rein lesender Subagent jede Analyse zu einer
Aufgabe der Kontrollstufe hoch, mit Architektur- und Security-Review, Nachweis der Testabdeckung
und vollständigem Sitzungsprotokoll. Das widerspricht Abschnitt 3.1 Punkt 4 desselben
Arbeitsmodells, der für M1 ausdrücklich „ein rein lesendes Agentenprofil“ erlaubt.

## 2. B07 – bestätigt, und der Befund sitzt an einer anderen Stelle als vermutet

### 2.1 Die Vermischung ist real – aber nur im Text

Das Review nennt es eine Vermischung von Integritäts- und Vertraulichkeitsschutz „obwohl der Hook
sie bereits unterscheidet“. **Nachgeprüft an beiden Schichten – beide unterscheiden korrekt:**

`framework/runtime/permissions.json`, die werkzeugneutrale Regelmenge:

| Verb | Regel | Schutzziel |
|---|---|---|
| `read` | `deny` auf `.env*`, Schlüsseldateien, Keystores, `**/secrets/**`, `<EXCLUDED_PATHS>` | Vertraulichkeit |
| `read` | `allow **` | alles Übrige ist lesbar |
| `write` | `deny` auf `<ROOT_INSTRUCTION_FILE>`, `<RUNTIME_DIR>/**`, `<CORE_DIR>/**`, `project-overlay/**` | Integrität, **nur schreibend** |

`tests/scripts/hook-check-secrets.py` führt zwei Musterlisten und kommentiert den Unterschied
ausdrücklich: „Ein Secret-Pfad ist vertraulich – er darf auch nicht GELESEN werden. Ein
Strukturpfad ist integritaetsgeschuetzt – er darf nicht GESCHRIEBEN werden, gelesen aber sehr
wohl.“ Die Trennung besteht seit D-30.

**Eigene Feststellung 4 – der Textfehler wirkt in die Technik zurück.** `<EXCLUDED_PATHS>` ist
nicht irgendeine Liste: Er ist **der Platzhalter, der in die `read`-Verweigerung eingesetzt wird**.
Die Vorlage (`templates/project-overlay/OVERLAY.md:71`) und die Laufzeitregel
(`framework/runtime/rules/20-project-overlay.md:23`) tragen ihm die Strukturpfade zu. Ein Projekt,
das die Vorlage wörtlich ausfüllt, erzeugt damit eine **Lesesperre auf seine eigenen
Regeldateien** – auf genau die Anweisungen, die der KI-Client befolgen soll.

Damit ist B07 kein reiner Dokumentenwiderspruch mehr. Er erreicht die erzeugte
Berechtigungsdatei.

**Wo der Befund nicht sitzt:** Die Wurzel-Anweisungsdatei macht es richtig. Abschnitt 3 verbietet
das Lesen von `<EXCLUDED_PATHS>`, Abschnitt 6 verbietet das Ändern der Strukturpfade – zwei
getrennte Aussagen. Sie bekommt die Lesesperre nur zugeliefert. Die Zeilenangabe `:37` des Reviews
trifft; `:60` trifft nicht, die Verbotsliste steht auf Zeile 57.

**Nebenbefund:** `<CORE_DIR>/**` steht in der Berechtigungsdatei als `write`-Verweigerung mit
`core: true`, **aber nicht** in der Verbotsliste der Wurzel-Anweisungsdatei (Zeile 57 nennt
`<ROOT_INSTRUCTION_FILE>`, `<RUNTIME_DIR>/` und `project-overlay/`). Der Mechanismus schützt mehr,
als der Text ankündigt – der wiederkehrende Befundtyp des Projekts mit umgekehrtem Vorzeichen.

### 2.2 Der fehlende Weg in das eigene Repositorium

| Behauptung | Nachgelesen | Ergebnis |
|---|---|---|
| Der Analyseskill lässt ein inaktives Overlay nur in Übungsrepositorys zu (`fw-repo-analyze/SKILL.md:43`) | Vorbedingung 2: „Ohne Overlay (Status `inaktiv`) ist der Skill nur auf Übungsrepositorys zulässig.“ | **bestätigt**, Zeile trifft |
| Die Regeln setzen freigegebene Pfade voraus (`root-instruction.md:37`) | Abschnitt 3: „nur in den im Overlay als erlaubt gelisteten Pfaden“; bei fehlendem oder inaktivem Overlay „arbeitest du nur lesend“ | **bestätigt** |
| Die README verweist auf `install.py`, ohne den Kontext zu regeln (`README.md:112`, `:144`) | Abschnitt „Arbeiten an diesem Repository“ ordnet die Installation an, sagt aber nichts über die Arbeitsweise | **bestätigt** |

**Eigene Feststellung 5 – derselbe Satz steht in fünf Skills**, nicht in einem:
`fw-repo-analyze`, `fw-code-explain`, `fw-change-analyze`, `fw-error-analyze`,
`fw-review-support`. Eine Berichtigung an einer Stelle hätte die nächste Inkonsistenz erzeugt.

**Der Zustand dieses Repositoriums, geprüft:** Der Overlay-Status steht in der erzeugten
Laufzeitregel auf `<TBD: aktiv | inaktiv>` – also fehlender Eintrag, also „nur lesend“. Die Arbeit
an diesem Framework ist nach seinen eigenen Regeln nicht vorgesehen. **Das ist die
Arbeitsbedingung jeder Sitzung dieses Projekts, auch dieser.** Das externe Review musste den
Auftrag als Berechtigung behandeln und hat es ausgewiesen.

## 3. Berichtigung der Fundstellen

Drei von vier Zeilenangaben des Reviews zu `framework/runtime/root-instruction.md` stimmen nicht:

| Review | tatsächlich | Inhalt |
|---|---|---|
| `:37` | **37** | Ausgeschlossene Pfade werden nicht gelesen (trifft) |
| `:60` | **57** | Verbotsliste der Änderungen |
| `:83` | **84** | „Immer K3: …“ |
| `:90` | **91** | Änderungen an Authentifizierung und Sicherheitskonfiguration |

Die Datei ist seit 0.27.0 unverändert (`5b4f490`); die Abweichung stammt aus dem Prüfstand des
Berichts. **Inhaltlich ändert sie nichts** – jede Aussage ist an der berichtigten Zeile belegt. Sie
steht hier, weil dieses Projekt jede Zahl nachzählt, die es liest.

## 4. Was diese Gegenprüfung nicht belegt

- **Sie belegt nicht, wie ein KI-Client die Grenzfälle einstuft.** Geprüft ist der Text. Ob eine
  Sitzung die entschiedene Einstufung trifft, ist `FW-KO-05` und steht auf `offen`.
- **Sie belegt nicht, dass ein Projekt die fehlerhafte Lesesperre tatsächlich erzeugt.** Belegt ist
  der Weg dorthin: Die Vorlage trägt die Strukturpfade in den Platzhalter, und der Platzhalter
  steht in der `read`-Verweigerung. Ein Lauf gegen eine Installation mit ausgefüllter
  `<EXCLUDED_PATHS>`-Liste ist **nicht** gefahren – kein ausgeliefertes Overlay füllt sie aus,
  weil die Vorlage `<TBD>` liefert.
- **Sie belegt nicht die Wirkung der neuen Prüfungen.** Das leistet der Wirkungsnachweis
  (`2026-09-13-wirkungsnachweise-0.32.0.md`) mit sechs Sonden, zwei Gegenproben und dem Gegenbeweis
  gegen 0.31.0.
- **Zur Zählung:** Sieben zusätzliche K3-Träger und acht Kategorien sind ausgezählt, nicht
  geschätzt. Wer sie nachzählt, sollte auf dieselben Zahlen kommen; wenn nicht, ist dieses
  Protokoll der Befund.

## 5. Gegenzeichnung

| Rolle | Name/Kennung | Datum | Ergebnis bestätigt |
|---|---|---|---|
| `<FRAMEWORK_OWNER>` | `<TBD>` | `<TBD>` | `<TBD>` |
