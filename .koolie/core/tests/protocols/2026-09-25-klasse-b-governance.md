# Protokoll: Die Durchsicht der Klasse B, zweiter Bereich – und das Budget statt der Grenze

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-25 |
| Release | `1.9.2` |
| Änderungsantrag | `CR-2026-144` |
| Art | Durchsicht der Regeldokumente (Governance, Checklisten, Entscheidungsbäume, Prompts) nach `docs/DOCUMENTATION_STANDARD.md`, sieben Klärungspunkte entschieden, Prüfung 4 auf ein Budget umgestellt – **keine Sitzung mit einem Client, kein Kontingent** |
| Gegenstand | 42 Dokumente der Klasse B; die Core-Module `05`, `08`, `09`, `10`; die Laufzeitregel `10-privacy-security.md`; D-10 und die Kapitel 3, 4, 29, 32 des Hauptdokuments; Prüfung 4 und ihre Sonden |
| Ergebnis | 🟢 **Entschieden, `D-385` bis `D-392`.** Kein Regelinhalt durch die Durchsicht geändert; 17 Dokumente überarbeitet, 25 unverändert; `K-128` und `K-130` bis `K-135` beantwortet; die Befunde als `K-139` bis `K-143`, der Mehrprojektfall als `K-138`, die Token-Last als `K-144`, der Aufruf von `--mermaid` als `K-145`; die Summe des stets Geladenen ist verbindlich |

---

## 1. Was gefragt war

Wiederaufnahmepunkt von `1.9.1`, Punkt 2: die Durchsicht der Klasse B, zweiter Bereich
(D-380), dazu `K-128` und `K-130` (D-384) und die Entscheidungen zu `K-131` bis `K-135`.
Fragen (a) bis (m) vorgelegt am 2026-09-25 und angenommen. Während des Baus fragte der
Owner, wie das Framework mit mehreren Projekten unter einem Verzeichnis umgeht; beantwortet
aus dem Protokoll vom 2026-09-12 und als `K-138` angelegt; danach, ob das Framework
wesentlich mehr Tokens verbraucht – als `K-144` angelegt, mit der Vorgabe, nur ohne Lockerung
zu sparen. `CR-2026-144` E1 bis E15.

## 2. Messungen vor und nach dem Bau

Je eine Testinstallation je Pack (`install.py --client <pack> --root <leer>`), Zeichen, nicht
Bytes. *Stets geladen* heißt: Wurzel-Anweisung plus die Regeln ohne Ladebedingung
(`claude-code`), mit `always_on` (`devin-desktop`) oder in der Wurzel-Anweisung genannt
(`openai-codex`).

| Träger | `claude-code` | `devin-desktop` | `openai-codex` |
|---|---|---|---|
| Wurzel-Anweisung | 11.894 | 11.887 | 12.516 |
| `10-privacy-security.md` vorher → nachher | 5.168 → 5.162 | 4.801 → 4.795 | 5.160 → 5.154 |
| stets geladen vorher → nachher | 29.773 → 29.767 | 20.349 → 20.349 (bisher nicht gezählt) | 30.274 → 30.268 |

Übernehmende Projekte vor dem Bau: Pilot 38.986 (sechs Regeln ohne Ladebedingung,
Wurzel-Anweisung 11.894), Übungsrepositorium 22.835 (`20-project-overlay.md` 6.095 –
Warnung, unverändert). **Kein Projekt überschreitet das Budget.**

## 3. Die Durchsicht

Sechs parallele Durchgänge nach einem gemeinsamen schriftlichen Auftrag (Kriterien der Klasse
B; harte Grenzen: kein Regelinhalt, kein Prüfpunkt gestrichen, keine Nummer, kein Anker,
Änderungen nur mit dem Edit-Werkzeug; Validator nach jeder Datei). Die Diffs hat der
Koordinator gelesen; jede gestrichene Kennung steht im Decision Log.

| Durchgang | Geändert | Sachlich berichtigt |
|---|---|---|
| `RELEASE_PROCESS`, `FRAMEWORK_DEV_PROFILE` | beide; neun Herleitungsabsätze in `RELEASE_PROCESS` auf die Regel mit D-Verweis gekürzt (18.507 → 14.322 Bytes), `FRAMEWORK_DEV_PROFILE` 10.503 → 9.181 Bytes; die Schritte von 4.1, die Befehlszeilen und die benannten Grenzen unverändert | Profil: *„beider“* Packs bei drei Packs; die Installation kopiert `governance/` in jedem Lieferumfang, nicht *„als Ganzes“* (D-367) |
| übrige Governance, Entscheidungsbäume | `PRIORITY_HIERARCHY` (Auftragsgeschichte zu D-06, D-34, D-52 ersetzt), `INCIDENT_HANDLING` (Schreibfehler); die Bäume unverändert | – |
| Checklisten | `README`, `01`, `03`, `05`, `10`, `11`; in `11` fünf Herleitungen gestrichen | `README`: auch KANN; `10`: Integrationspunkt nach D-354; `11`: Verweis auf `RELEASE_PROCESS.md` Abschnitt 6, Versions- und Aktualitätstests, `--target` (D-362) |
| Prompts `README`–`03` | `README`, `03` | `README`: der Aufrufweg eines Skills steht in Zeile S2 der Fähigkeitsmatrix; `03`: Planablage als `<RUNTIME_DIR>` statt eines Clientpfads |
| Prompts `04`–`07` | `07` (eine Begründung, ein Grammatikfehler) | – |
| Prompts `08`–`12` | `10`, `11`, `12` (Schreib- und Grammatikfehler) | – |

**Befunde, die eine Entscheidung brauchen** – als Klärungspunkte angelegt, nicht behoben
(D-385 (a)):

| Kennung | Gegenstand |
|---|---|
| `K-139` | Prompts gegen Module und Skills – darunter Injektionsverdacht ohne Anhalten (S6) in acht Vorlagen, K2-Eingaben ohne Freigabe, Git-Befehle ohne Overlay-Bedingung |
| `K-140` | Checklisten mit anderer Pflichtstufe als ihr Modul, strenger und lockerer |
| `K-141` | Entscheidungsbäume: Diagramm, Text und Modul weichen ab; `05` Schritt 9 gegen `09` |
| `K-142` | Einzelbefunde in `governance/` |
| `K-143` | `03-security.md` T5 *„hoch für R3/R10“* gegen die Einstufung in `09` |

**Mermaid:** `validate-framework.py --mermaid` meldet in dieser Umgebung jeden Mermaid-Block
als ungültig, auch unveränderte (Roadmap, Kapitel 7). Der Bau rendert dieselben Diagramme: Er
übergibt `mmdc` eine Puppeteer-Konfiguration, der Validator nicht (`K-145`).

## 4. Die Klärungspunkte

| Kennung | Umsetzung |
|---|---|
| `K-128` (D-386) | D-10 präzisiert; Kapitel 3 (N7), 4, 29, 32 nennen *„Läufe ohne beobachtende Person“* statt *„Kommandozeilenbetrieb“* |
| `K-130` (D-387) | Prüfung 4: Summe über 40.000 **Fehler** für jedes Pack, bei `devin-desktop` die Regeln mit `always_on` neu gezählt; 12.000 je Datei **Warnung**; R4 beider Packs mit eigener Zeile, Laufzeit-README von `claude-code` und `devin-desktop`, Kapitel 16 |
| `K-131` (D-388) | `08-skill-conventions.md` Abschnitt 3: Quelle und installierte Fassung |
| `K-132` (D-389) | `09-risk-model.md` R12 und die Erläuterung darunter |
| `K-133` (D-390) | `05-working-model.md` Abschnitt 2 |
| `K-134` (D-391) | `10-error-escalation.md` Abschnitte 1 und 2; `05-working-model.md` an drei Stellen *Zeile S3*; Baum 05 in Text und Diagramm |
| `K-135` (D-392) | `rules/10-privacy-security.md`, sechs Zeichen kürzer |

## 5. Wirkungsnachweis – Sonden und Gegenproben, mit Gegenbeweis

| Einheit | Gegenstand | Ergebnis |
|---|---|---|
| Sonde 4a | Wurzel-Anweisung einer `claude-code`-Installation über 12.000 Zeichen | als **Warnung** gemeldet, nicht als Fehler |
| Sonde 4b | `devin-desktop`: eine Regel mit `always_on` um 30.000 Zeichen verlängert | Budget als **Fehler** gemeldet |
| Gegenprobe 4d | `devin-desktop`: eine Regel mit `model_decision` um 30.000 Zeichen verlängert | kein Budgetbefund |
| Gegenproben 4a, 4b, 4c | frische Installation je Pack | weder Budget noch Grenze |

**Gegenbeweis**, je an einer Installation mit dem Validator aus `v1.9.1` und dem neuen:

| Präparation | `v1.9.1` | neu |
|---|---|---|
| `devin-desktop`, zwei zusätzliche Regeln mit `always_on` (je 10.993 Zeichen, jede unter der Grenze je Datei), stets geladen 42.335 | kein Befund | **Fehler** (Budget) |
| `claude-code`, Wurzel-Anweisung auf 12.003 Zeichen | **Fehler** | Warnung |

Die sieben übrigen Fehler beider Läufe kommen aus der Testinstallation ohne `README.md`.

## 6. Abnahme

| Lauf | Ergebnis |
|---|---|
| Validator | **0 Fehler, 0 Warnungen**, beide Kodierungsumgebungen |
| Sondenlauf | **344 Einheiten, alle bestanden** (das Bündel `sonden_zeichengrenze` trägt jetzt sechs Einheiten statt vier und zählt als eine), beide Kodierungsumgebungen Exit 0 und oberhalb der Trennlinie zeilengleich (602 Zeilen), rund 770 s Wanduhr je Lauf. Der erste volle Lauf hatte Sonde 52a als gebrochen gemeldet (Abschnitt 7) |
| Abnahmelauf gegen den fertigen Baum | steht in der Nachricht des Release-Commits – der Lauf misst dieses Protokoll mit |
| Pilot / Übungsrepo `--strict-overlay` nach der Hebung | beide mit `--target --update`; Ergebnis im Änderungsverlauf des jeweiligen Overlays |

## 7. Befunde während des Baus

- **Die neuen Sonden verlangten zuerst „0 Fehler“** – eine Testinstallation ohne `README.md`
  meldet aber sieben fremde Fehler. Gefunden beim Gegenbeweis, vor dem ersten Lauf; die
  Sonden prüfen jetzt nur die Zeilen der Prüfung 4.
- **Die angeglichene Laufzeitregel war im ersten Entwurf 34 Zeichen länger** – gegen die
  Zusage (l). Umformuliert, bis sie kürzer war.
- **Der erste volle Sondenlauf meldete Sonde 52a als gebrochen:** Ihr Suchtext war der
  Zeilenanfang der Laufzeitregel `10-privacy-security.md`, den `K-135` umgestellt hat. Prüfung 52
  selbst trug (Gegenprobe 52a bestand); der Suchtext ist nachgezogen. *Wer eine Laufzeitregel
  umformuliert, sucht ihre Sonden mit.*
- **Der Befund am Renderer war falsch zugeordnet.** Die Durchsicht und der erste Entwurf dieses
  Protokolls schrieben das Scheitern von `--mermaid` dem Renderer zu; der Bau hat im selben
  Arbeitsgang alle acht Diagramme gerendert. Gemessen: Ohne die Puppeteer-Konfiguration des Baus
  findet `mmdc` seinen Browser nicht (`K-145`).
- **Ein Befund der Durchsicht berührt die eigene Entscheidung:** `03-security.md` T5 nennt
  *„hoch für R3/R10“*. D-392 bleibt, weil R3 die Einstufung regelt; die Kurzform ist `K-143`.

## 8. Offen und benannt

- `K-138` (Mehrprojektfall), `K-139` bis `K-143` und `K-144` (Token-Last) für `1.11.0`; `K-123`, `K-125`, `K-127`,
  `K-129`, `K-136`, `K-137` und `K-145` für `1.10.0` (D-384).
- Die Abnahme des macOS-Starters auf macOS (aus `1.7.0`).
