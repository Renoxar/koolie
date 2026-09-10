# Änderungsverzeichnis (Framework)

Format: Semantic Versioning; je Release Änderungen, Migrationshinweise für Overlays und bekannte Einschränkungen. Prozess: `leitwerk-core/governance/RELEASE_PROCESS.md`.

## [0.8.0] – 2026-09-10

### Geändert
- **Die letzte Restduplikation zwischen den Client Packs ist zusammengeführt (`CR-2026-010`, Decision Record D-20).** Overlay-Laufzeitregel, nutzerlokale Ergänzungsvorlage und MCP-Vorlage liegen jetzt einmal unter `framework/runtime/`. **Ein Client Pack besteht aus vier Dateien statt sieben:** `CLIENT_PACK.md`, `manifest.json` und zwei Laufzeit-READMEs.

  Gemessen wurde vor der Zusammenführung – nach Normalisierung der Client- und Pfadnamen:

  | Dateipaar | Zeilen | abweichend | Ergebnis |
  |---|---|---|---|
  | `20-project-overlay.md` | 119 | 11 | zusammengeführt |
  | `*.local.md.example` | 38 | 8 | zusammengeführt |
  | MCP-Vorlage | 8 | 2 | zusammengeführt |
  | Laufzeit-`README.md` | 86 | 64 | **bleibt je Pack** |

  Entscheidend war nicht der Prozentsatz, sondern was in den abweichenden Zeilen stand: **ausschließlich Werte, für die bereits ein Laufzeit-Platzhalter registriert ist** (`<RUNTIME_DIR>`, `<ROOT_INSTRUCTION_FILE>`, `<ROOT_INSTRUCTION_LOCAL>`, `<MCP_FILE>`). Es war keine neue Abbildung zu erfinden, sondern nur eine vorhandene anzuwenden – kein neuer Mechanismus, kein neues Manifestfeld.

  Die letzte Zeile der Tabelle ist die Gegenprobe: Die beiden Laufzeit-READMEs beschreiben tatsächlich verschiedene Mechanismen und bleiben getrennt. Eine gemeinsame Fassung wäre für beide Clients ungenau.

- **`seed_paths` ist in beiden Manifesten leer.** Die gesamte Saat eines Projekts – Overlay, Overlay-Laufzeitregel, Berechtigungsdatei – kommt jetzt aus dem Kern. `root-template/` enthält nur noch Core-Dateien.

- **Zwei Ungenauigkeiten in der MCP-Vorlage korrigiert.** „laut Devin-Dokumentation" wurde zu „laut Dokumentation dieses Clients", und der Marker `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` zu seiner clientneutralen Form. In der Fassung des Packs `claude-code` standen beide bislang falsch – ein Rest aus der Konvertierung, der dort nie zutraf.

### Behoben
- **`render_rule` beschrieb das Ladeverhalten invertiert.** Eine Regel mit `trigger: always_on` erhielt den Satz „Wird über den Import in der Wurzel-Anweisungsdatei geladen." – *ohne* das Wort „immer" –, während eine Regel mit `model_decision` ihn *mit* erhielt. Genau umgekehrt wäre richtig gewesen: `always_on` lädt ausnahmslos, und für die andere ist die Einbindung eine Verschärfung, die eigens benannt wird.

  Ohne Wirkung auf das Verhalten, aber irreführend – der erzeugte Kommentar behauptete den schwächeren Ladezustand für die Regel, die tatsächlich immer lädt. Beide Fälle sagen jetzt „immer geladen"; nur die Verschärfungsnotiz unterscheidet sie. Gefunden beim Zusammenführen der Overlay-Regel, weil deren handgeschriebene Fassung im Pack `claude-code` die richtige Formulierung trug.

### Nachweise
- **Zeichenweiser Vergleich gegen 0.7.0:** Fünf der sechs erzeugten Dateien sind identisch. Die sechste – die Overlay-Regel des Packs `claude-code` – weicht in drei Zeilen ihres erzeugten Kommentars ab und liest sich dadurch wie ihre drei Nachbarregeln.
- Erstinstallation beider Packs: 80 beziehungsweise 79 Dateien wie zuvor; `--check` gegen beide fehlerfrei; `FW-KO-04` und der Validator gegen beide Installationen und die Wurzelinstallation: 0 Fehler.

### Migrationshinweise für Overlays
Keine Handarbeit nötig. Die beiden Vorlagen sind Core und werden von `python leitwerk-core/install.py --update` erneuert; die Overlay-Laufzeitregel ist Saat und wird nie überschrieben – ein bestehendes Projekt behält seine ausgefüllte Fassung unverändert.

### Bekannte Einschränkungen
- `root-template/` enthält je Pack nur noch zwei READMEs, und `seed_paths` ist überall leer. Beides bleibt im Manifest, weil ein künftiges Client Pack wieder eigene Wurzelartefakte mitbringen kann.
- Die Einstufungen der Fähigkeitsmatrix bleiben unbelegt (Roadmap AP2).

## [0.7.0] – 2026-09-10

> **Brechende Änderung.** Das Kernverzeichnis heißt jetzt `leitwerk-core/`. Ein bestehendes Projekt muss migrieren – der Weg steht unten und ist durchgespielt.

### Geändert
- **Das Framework heißt Leitwerk (`CR-2026-009`, Decision Record D-19).** Das Kernverzeichnis `devin-core-framework/` heißt `leitwerk-core/`, Repository und Projektverzeichnis `leitwerk`, der Eigenname in Prosa und Erzeugnissen „Leitwerk". 994 Pfadnennungen und 6 Namensnennungen in 182 Dateien.

  Seit 0.5.0 ist der Kern inhaltlich werkzeugneutral – er bezeichnet die Laufzeitschicht mit Begriffen statt mit Pfaden, und die Bindung an einen Client leistet ein Client Pack. Der Name war dieser Entwicklung nicht gefolgt. Wer `claude-code` installierte, las durchgehend einen Pfad mit dem Produktnamen eines Werkzeugs, das bei ihm nicht im Einsatz ist – dieselbe Beobachtung, die schon `CR-2026-005` ausgelöst hatte.

  Das Bild trifft zudem die Selbstbeschreibung: Ein Leitwerk fliegt das Flugzeug nicht, es hält es stabil und auf Kurs. Das Framework schreibt nicht vor, wie Software entsteht, sondern hält den Prozess in einer Spur, die prüfbar, nachvollziehbar und übertragbar bleibt.

- **Unverändert und ausdrücklich nicht betroffen:** das Client Pack `devin-desktop` (59 Nennungen), die Laufzeitschicht `.devin/` (250 Nennungen) und alle Produktnennungen „Devin Desktop", „Devin Local", „Devin Cloud" dort, wo tatsächlich der Client gemeint ist. Sie benennen einen realen Client korrekt.

- **`README.md` und Titelblatt des Hauptdokuments** auf den neuen Namen und die Mehrclient-Sicht gebracht. Das Titelblatt weist jetzt ausdrücklich aus, dass der Fließtext der Kapitel 1 bis 32 weiterhin auf 0.1.0 steht und aus der Sicht eines einzelnen Clients geschrieben ist – maßgeblich ist bis zu dessen Überarbeitung das Repository.

- **`governance/RELEASE_PROCESS.md` Punkt 1** um eine Klarstellung ergänzt: Solange die Hauptversion 0 ist, erscheint eine brechende Änderung als MINOR mit Migrationsabschnitt. Der Grund ist nicht formal, sondern inhaltlich – `1.0.0` ist durch D-11 an fünf prüfbare Kriterien gebunden; eine Hauptversion für eine Verzeichnisumbenennung zu verbrauchen, würde diese Kriterien behaupten und das Release-Gate `FW-CL-11` entwerten.

- **`.gitignore`:** veralteten Verweis auf ein `root-template/` im Wurzelverzeichnis korrigiert – das liegt seit 0.5.0 je Client Pack.

### Nachweise
- **`FW-KO-04` gegen beide Installationen: 0 Fehler.** Die Querverweisprüfung war für genau diesen Fall gebaut; ihre Umbenennungssimulation in 0.5.0 hatte 685 Fehler gemeldet und damit belegt, dass sie eine solche Änderung vollständig erfasst. Eine Suche nach den drei alten Namensformen im Repository ist leer.
- Erstinstallation beider Packs: 80 beziehungsweise 79 Dateien wie zuvor; `--check` fehlerfrei; die Dateiliste der Wurzelinstallation wurde gegen eine Referenzinstallation abgeglichen und ist deckungsgleich.
- **`<CORE_DIR>` hat sich bewährt.** Die erzeugten Berechtigungs- und Hookdateien tragen den neuen Kernpfad, ohne dass ein Manifest angefasst wurde: `Write(leitwerk-core/framework/**)` in den Kernregeln beider Packs, `$DEVIN_PROJECT_DIR/leitwerk-core/…` im Hook-Befehl. Der Platzhalter war in 0.6.0 genau dafür eingeführt worden.
- Dokumentbau intakt: alle 91 Einbettungspfade auflösbar, 8.559 Zeilen erzeugt.
- Der längste relative Pfad sinkt von 110 auf 103 Zeichen; unter `MAX_PATH` bleiben damit rund 156 statt 149 Zeichen für den Projektpfad.

### Migrationshinweise für bestehende Projekte

Durchgespielt an einem Projekt auf Stand 0.6.0 mit eigenen Werten in der Berechtigungsdatei.

1. **Verzeichnis umbenennen:** `devin-core-framework/` → `leitwerk-core/`. Unter Windows kann ein geöffneter Editor das Verzeichnis sperren; dann die Inhalte verschieben statt das Verzeichnis umzubenennen.
2. **Core aktualisieren:** `python leitwerk-core/install.py --update`.
3. **Validator laufen lassen:** `python leitwerk-core/tests/scripts/validate-framework.py`. Er meldet an dieser Stelle **genau zwei Fehler** und benennt die betroffene Kernregel – die Berechtigungsdatei gehört dem Projekt und wird von `--update` nicht angefasst, trägt also noch den alten Pfad.
4. **Alten Pfad in der Berechtigungsdatei ersetzen** (fünf Nennungen: in `deny`, in `_core_rules_integrity` und im erzeugten Kommentar), ebenso in Overlay-Dokumenten, die ihn nennen.
5. **Erneut validieren:** 0 Fehler. Die Projektwerte bleiben dabei unverändert erhalten.

Dass Schritt 3 den Fehler überhaupt meldet, ist Verdienst der Kernquellenprüfung aus 0.6.0 – vor diesem Release wäre der veraltete Pfad in der Berechtigungsdatei unbemerkt geblieben.

### Außerhalb des Repositorys
Git-Repository umbenennen, Remote-URL der Arbeitskopien nachziehen (`git remote set-url origin …`), lokales Projektverzeichnis umbenennen. Diese drei Schritte kann kein Skript des Frameworks übernehmen.

### Bekannte Einschränkungen
- Der Fließtext des Hauptdokuments (`build/doc/`, Kapitel 1 bis 32) steht weiterhin auf 0.1.0 und ist aus der Sicht eines einzelnen KI-Clients geschrieben. Client Packs, Abbildungsschicht und Fähigkeitsmatrix sind dort nicht eingearbeitet. Das Titelblatt weist diesen Stand aus, statt ihn zu verdecken.
- Die Einstufungen der Fähigkeitsmatrix bleiben unbelegt (Roadmap AP2).

## [0.6.0] – 2026-09-10

### Geändert
- **Berechtigungen und Hooks liegen einmal im Kern (`CR-2026-008`, Decision Record D-18).** Die Regelmenge steht werkzeugneutral in `leitwerk-core/framework/runtime/permissions.json` und `hooks.json`; die drei Vorlagendateien in den Client Packs (`.devin/config.json`, `.devin/hooks.v1.json`, `.claude/settings.json`) entfallen. Ein Client Pack enthält jetzt fünf Dateien.

  Das war die letzte Doppelpflege im Kern – und die einzige, bei der sie sicherheitsrelevant war. `CR-2026-007` hatte sie ausdrücklich vertagt: Anders als bei Regeltexten, Skills und Overlay ist die Abbildung hier keine Formfrage. Die Werkzeuge selbst unterscheiden sich – ein Client trennt Ändern und Anlegen in `Edit` und `Write`, ein anderer nicht; Befehlsverbote greifen hier wörtlich (`Exec(git reset --hard)`) und dort präfixbasiert (`Bash(git reset:*)`); Netzzugriff ist einmal ein Werkzeug mit Muster und einmal zwei ohne. An genau diesen Regeln hängen die Kernzusagen **B1 bis B6**: Eine beim Nachziehen in das zweite Pack vergessene Regel wäre eine stille Lücke gewesen, während die Fähigkeitsmatrix weiterhin `[TECHNISCH]` behauptet.

- **`_core_rules_integrity.deny_must_contain` wird erzeugt, nicht gepflegt.** Die Kernzusagen sind in der Quelle mit `"core": true` gekennzeichnet; die Liste je Client entsteht daraus (13 Regeln bei `devin-desktop`, 17 bei `claude-code` – dort trägt jeder Schreibschutz zwei Regeln).

### Hinzugefügt
- **`leitwerk-core/clientmap.py` – die Semantikabbildung.** Von `install.py` zum Erzeugen und von `validate-framework.py` zum Prüfen genutzt. Das Modul **erzwingt** drei Eigenschaften, statt sie zuzusagen:

  | Zusicherung | Bei Verletzung |
  |---|---|
  | Keine `deny`- oder `ask`-Regel ohne Zielwerkzeug beim Client | Installation bricht ab; Weglassen wäre eine Lockerung. Bei `allow` ist Weglassen zulässig – es fällt auf den strengeren Standard zurück |
  | Die Präfixform eines Befehlsverbots muss ein Präfix seiner wörtlichen Form sein | Installation bricht ab. Damit ist die Präfixform nachweislich mindestens so breit – die Abweichung ist belegbar eine Verschärfung |
  | Bei `allow` müssen wörtliche und Präfixform übereinstimmen | Installation bricht ab; dort wäre jede Verbreiterung eine Lockerung |

- **Der Validator prüft die Kernregeln gegen die Kernquelle.** Bisher genügte es, eine Kernregel in `deny` **und** in `_core_rules_integrity` zu streichen: Die Datei blieb in sich stimmig, der Verlust unbemerkt. Weil die Berechtigungsdatei Saat ist und `install.py --check` sie nie anfasst, war das die letzte Lücke in der Kette. Fehlt `clientmap.py`, wird gewarnt statt abgebrochen; die bisherigen Prüfungen greifen weiter.

- **Neun Abbildungsfelder je Manifest:** `permission_tools`, `permission_tools_bare`, `permission_path_prefix`, `permission_exec_match`, `permission_exec_suffix`, `permissions_extra`, `permissions_note`, `hook_tools`, `hook_project_dir_var`. Ob ein Client eine eigene Hook-Datei kennt, wird **nicht** eigens angegeben, sondern daran erkannt, dass `<HOOKS_FILE>` und `<PERMISSIONS_FILE>` auf denselben Pfad zeigen – zwei Angaben über dieselbe Tatsache wären eine Fehlerquelle.

- **Laufzeit-Platzhalter `<CORE_DIR>`.** Der Name des Kernverzeichnisses steht in den Schreibverboten und im Hook-Befehl. Er ist keine Eigenschaft eines Clients, sondern dieser Installation, und wird deshalb von `install.py` und dem Validator aus dem tatsächlichen Verzeichnisnamen gesetzt; ein Client Pack darf ihn nicht belegen. Die in der Roadmap vorgesehene Umbenennung des Kernverzeichnisses berührt damit kein Pack.

- **Abschnitt 1a „Semantikabbildung" in beiden Client Packs und der Vorlage.** Die menschenlesbare Fassung der Abbildungsfelder, Werkzeugverb für Werkzeugverb.

### Nachweise
- **Byteweiser Vergleich gegen 0.5.0:** Jede erzeugte Berechtigungsregel und beide `_core_rules_integrity`-Blöcke sind identisch; die Hook-Datei von `devin-desktop` vollständig. Zwei gewollte Abweichungen ohne Wirkung auf das Schutzniveau: der erzeugte `_comment` (er nennt jetzt die Kernquelle) und die Reihenfolge im Hook-Matcher von `claude-code` (`Bash|Edit|Write|NotebookEdit` statt `Edit|Write|Bash|NotebookEdit` – dieselbe Menge, eine Alternation ist ungeordnet).
- Erstinstallation beider Packs in ein leeres Verzeichnis: 80 beziehungsweise 79 Dateien wie zuvor; `--check` gegen beide fehlerfrei; Validator gegen beide Installationen und die Wurzelinstallation dieses Repositorys: 0 Fehler.
- **Negativtests:** Kernregel aus *beiden* Listen einer installierten Datei entfernt → gemeldet (vor dieser Änderung unbemerkt). Abbildung ohne Schreibwerkzeug, `prefix` ohne Präfixeigenschaft, `allow`-Regel mit verkürzter Präfixform, Hook-Werkzeugklasse ohne Werkzeug → Installation bricht jeweils mit benannter Ursache ab.

### Migrationshinweise für Overlays
- Für ein bestehendes Projekt ändert sich nichts. Die Berechtigungsdatei ist Saat und wird von `--update` nie überschrieben; die eingetragenen Projektwerte bleiben.
- `install.py --update` bringt bei `devin-desktop` die Hook-Datei auf den Kernstand (unverändert gegenüber 0.5.0). Bei `claude-code` liegen die Hooks in der Berechtigungsdatei und damit in der Saat – eine spätere Änderung an den Hooks des Kerns erreicht ein bestehendes Projekt dieses Packs **nicht** von selbst und ist beim Release-Wechsel von Hand nachzuziehen.
- Prüfung nach dem Wechsel wie bisher: `python leitwerk-core/tests/scripts/validate-framework.py --strict-overlay`.

### Bekannte Einschränkungen
- Die Schreibverbote schützen `<CORE_DIR>/framework/**`, nicht das gesamte Kernverzeichnis. `install.py`, `validate-framework.py`, die beiden Hook-Skripte und nun auch `clientmap.py` sind damit nicht schreibgeschützt – gerade die Skripte, die die Schutzzusagen durchsetzen. Der Befund ist älter als diese Änderung; die naheliegende Verschärfung auf `<CORE_DIR>/**` ändert die Kernregelmenge und braucht deshalb einen eigenen Änderungsantrag.
- Die Einstufungen der Fähigkeitsmatrix bleiben unbelegt (Roadmap AP2). Diese Änderung stellt sicher, dass beide Packs dieselbe Regelmenge tragen – nicht, dass ein Client sie durchsetzt.

## [0.5.0] – 2026-09-10

### Geändert
- **Definition des Release 1.0.0 (`CR-2026-001`, Decision Record D-11, ersetzt D-09).** 1.0.0 bezeichnet künftig den Stand „technisch validiert und übertragbar" mit fünf prüfbaren Kriterien: kein unbearbeiteter VERIFY-Marker, Testkatalog vollständig protokolliert (kein Testfall `offen`), alle Modulstatus oberhalb `entwurf`, kein Decision Record im Status `entschieden (Vorschlag)`, Übernahme in ein zweites Projekt nachgewiesen.

  Pilot (AP9), Onboarding (AP8) und organisatorische Freigabe (AP10) sind **keine** Vorbedingung mehr für 1.0.0. Sie setzen eine aufnehmende Organisation mit besetzten Rollen voraus und sind damit projektseitige Arbeitspakete; in der Roadmap hängen sie jetzt an AP13 (Übernahme). AP11 folgt direkt auf AP7.

  Hintergrund: Die bisherige Definition machte das Release-Gate `FW-CL-11` strukturell unerreichbar, solange keine Organisation benannt ist – obwohl die verbleibenden Lücken ausschließlich Nachweise betreffen. Ein Release 1.0.0 erklärt ausdrücklich nicht, dass das Framework im Realbetrieb erprobt wurde.

- `leitwerk-core/checklists/11-framework-release.md`: vier Prüfpunkte mit der Kennzeichnung **(ab 1.0.0, D-11)** ergänzt.
- `leitwerk-core/docs/ROADMAP.md`: Abhängigkeitsgraph und Arbeitspakete AP8–AP13 neu zugeordnet; AP8–AP10 auf P3 und als projektseitig gekennzeichnet.
- Neue Ablage für Änderungsanträge: `leitwerk-core/governance/change-requests/`.

### Hinzugefügt
- **Querverweisprüfung im Validator (`FW-KO-04`).** `validate-framework.py` prüft als zwölfte Prüfung, dass Markdown-Links und in Backticks genannte Framework-Pfade auf existierende Dateien oder Verzeichnisse zeigen. Der Testkatalog führte diese Prüfung bislang als `skript (validate-framework.py-Erweiterung <TBD>)` mit Ergebnisstatus `offen`; sie ist jetzt umgesetzt und bestanden.

  Nicht als Fehler gewertet werden – jeweils im Skript begründet – Laufzeitfassungen aktivierter Packs (`.devin/rules/2N-`, `30-`, `40-`, `.devin/skills/role-`, `tech-`, `prj-`), nutzerlokale Dateien mit Namensbestandteil `.local.`, Pfade mit vorhandener `.example`- oder `.template`-Fassung sowie Globs, Platzhalter und Befehlszeilen.

  Wirksamkeit belegt: Sondendatei mit zwei defekten Verweisen und vier Nicht-Pfad-Angaben → genau 2 Fehler, keine Fehlmeldung. Umbenennungssimulation `leitwerk-core/` → `agent-core-framework/` → 685 gemeldete Fehler. Damit ist die für 0.5.0 vorgesehene Umbenennung abgesichert.

- **Ablage für Testprotokolle: `leitwerk-core/tests/protocols/`.** Löst `<TBD: Ablage der Testprotokolle>` aus dem Testkatalog. Namensschema `JJJJ-MM-TT-<Test-ID>.md` beziehungsweise `JJJJ-MM-TT-release-<Version>.md`; ein Ergebnisstatus außer `offen` MUSS auf ein Protokoll verweisen. Erster Eintrag: `2026-09-10-FW-KO-04.md`.

- **Client Packs als Abbildungsschicht (`CR-2026-002`, Decision Record D-12).** Neu unter `leitwerk-core/clients/`: `README.md`, die Vorlage `_template/CLIENT_PACK.md` und das erste Pack `devin-desktop/CLIENT_PACK.md`.

  Kern der Vorlage ist die **Fähigkeitsmatrix**: 26 technische Zusagen des Frameworks in sieben Gruppen (Regelladung, Skills, Berechtigungen, Hooks, Agentenprofile, Modi, externe Anbindung), jede eingestuft als `[TECHNISCH]` (die Engine erzwingt sie), `[TEXTUELL]` (nur Anweisung im Kontext) oder `[NICHT ABBILDBAR]`. Sechs davon sind Kernzusagen und entsprechen `_core_rules_integrity` in der Berechtigungsdatei; weicht eine ab, ist sie einzeln zu begründen, im Overlay als Ausnahme zu führen und durch `<SECURITY_CONTACT>` freizugeben.

  Ein Client Pack ist **keine Regelebene**. Es führt keine Verhaltensregel ein und lockert keine; die achtstufige Prioritätshierarchie (D-06) bleibt unberührt. Bei Widerspruch zur werkzeugneutralen Langform gilt die Langform.

  Befund aus dem ersten ausgefüllten Pack: 21 der 26 Zusagen sind als `[TECHNISCH]` vorgesehen, alle sechs Kernzusagen darunter – aber **13 der 26 Zeilen tragen einen VERIFY-Marker und keine einzige Einstufung ist gegen eine Installation geprüft**. Besonders: Der Schutz-Hook läuft fail-open, die Zusage „Prüfung kann blockieren" ist damit derzeit `[TEXTUELL]`.

- Neue Platzhalter: `<CLIENT_PACK_NAME>`, `<CLIENT_PACK_CODE>` sowie der clientneutrale Marker `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>`, der die devin-spezifische Form ab 0.5.0 ersetzt.

- **Wurzelartefakte je Client Pack; `install.py --client` (`CR-2026-003`, Decision Record D-13).** `leitwerk-core/root-template/` liegt jetzt unter `leitwerk-core/clients/devin-desktop/root-template/`. Ein Client Pack besteht damit aus `CLIENT_PACK.md` (was der Client durchsetzt) und `root-template/` (was installiert wird).

  `install.py` kennt `--client` (Standard `devin-desktop`) und `--list-clients`; die Vorlage wird aus dem gewählten Pack abgeleitet statt aus einer Konstanten. Ein unbekannter Client bricht mit Exit-Code 1 ab und nennt die verfügbaren Packs.

  Die Schicht selbst wanderte von `framework/client-packs/` nach `clients/` – aus zwei Gründen. Inhaltlich: Unter `framework/` liegen die Regelebenen, und D-12 hält fest, dass ein Client Pack keine ist. Technisch: Die erste Testinstallation brach unter Windows an `MAX_PATH` ab, weil der längste relative Pfad von 89 auf 126 Zeichen wuchs; unter `clients/` sind es 111.

  **Für aufnehmende Projekte ändert sich nichts.** `install.py` ohne Schalter verhält sich unverändert; die installierten Artefakte sind byteweise dieselben. Betroffen ist nur, wer den Kern selbst bearbeitet: Core-Änderungen gehören jetzt nach `leitwerk-core/clients/<client>/root-template/`.

- **Zweites Client Pack: `claude-code` (`CR-2026-004`, Decision Record D-14).** Vollständiges `root-template/` mit 79 Dateien – eine weniger als `devin-desktop`, weil die Hooks dort in einer eigenen Datei stehen und hier in der Berechtigungsdatei aufgehen.

  **Die Abstraktion trägt.** Alle sechs Kernzusagen sind auch bei diesem Client technisch abgebildet (20 von 26 Zusagen `[TECHNISCH]`, gegenüber 21 bei `devin-desktop`). Die vier nicht abbildbaren Zusagen betreffen ausschließlich Least Context und Ergonomie, keine Schutzzusage: Der Client kennt keine Regeldateien mit Ladetriggern. Die Regeltexte sind inhaltlich identisch und werden über Importe in der Wurzel-Anweisung stets geladen – eine Verschärfung, die rund 22.000 Zeichen ständigen Kontext kostet.

- **Manifeste je Client Pack.** `install.py` hatte die Core- und Saatpfade fest auf `.devin/` verdrahtet; sie stehen jetzt in `clients/<name>/manifest.json`. Ein Pack ohne Manifest gilt als nicht installierbar.

- **Der Validator ist clientneutral.** `check_required`, `check_config`, `check_rules` und `skill_dirs` liefen fest gegen `.devin/`; sie ermitteln die Laufzeitschicht jetzt über `detect_client()`. Mehrere gleichzeitig vorhandene Laufzeitschichten sind ein Fehler. `check_rules` unterscheidet zwei Bauarten: mit Ladetriggern wird das Frontmatter geprüft, ohne Ladetrigger, dass jede Kernregel in der Wurzel-Anweisung **eingebunden** ist – dort ist eine nicht eingebundene Regeldatei stillschweigend wirkungslos.

- **`hook-check-secrets.py` schützt beide Namensformen** der Wurzel-Anweisung und der Laufzeitschicht. Das Skript war schema-agnostisch und läuft bei beiden Clients unverändert.

- **Der Kern ist neutralisiert (`CR-2026-005`, Decision Record D-15).** Er bezeichnet die Bestandteile der Laufzeitschicht jetzt mit Begriffen statt mit Pfaden: Wurzel-Anweisungsdatei, Laufzeitschicht, Berechtigungsdatei, Regelablage, Skill-Ablage, Agentenprofile, Hook-Konfiguration, MCP-Konfiguration, nutzerlokale Überschreibung.

  Neu: `leitwerk-core/docs/RUNTIME_GLOSSARY.md` bildet jeden Begriff auf die Pfade je Client Pack ab – das Gegenstück zum Platzhalterregister. Die Regel: im Kern der Begriff, im Client Pack der Pfad, in historischen Dokumenten bleibt beides unverändert.

  **61 von 63 Stellen ersetzt**, gemessen nach jedem Durchgang: 63 → 57 → 33 → 23 → 8 → 2. Die zwei verbliebenen stehen in Roadmap-AP2, das bewusst die Mechanismen *eines* Clients validiert; dort steht jetzt der Hinweis, dass es je Client Pack zu wiederholen ist.

  Mitgenommen: Wo die Prosa eine Eigenschaft beschreibt und keinen Beleg, ist auch der Produktname gewichen – „Devin passt Tests an" wurde zu „Das Werkzeug passt Tests an", „Devin-Nutzungsvermerk" zu „KI-Nutzungsvermerk".

  Decision Record D-02 wurde **nicht** umgeschrieben – ein Decision Record beschreibt eine Entscheidung zu ihrem Zeitpunkt. Er trägt einen Fortschreibungsvermerk auf D-12 bis D-14.

  **Keine Regel wurde inhaltlich geändert.** Nachgewiesen durch byteweise unveränderte Installationen: weiterhin 80 Dateien (`devin-desktop`) und 79 (`claude-code`), `--check` fehlerfrei.

- **Die Skills haben eine gemeinsame Quelle (`CR-2026-006`, Decision Record D-16).** Sie liegen jetzt einmal unter `leitwerk-core/framework/skills/` und werden bei der Installation in die Form des gewählten Clients gebracht. Ein neuer Skill wird einmal geschrieben und gilt für alle Client Packs.

  Zwei Transformationen, beide aus dem Manifest gesteuert: Das **Frontmatter** wird nach `skill_frontmatter` umgeformt (Listenform oder kommagetrennt, Werkzeugabbildung, Wegfall unbekannter Felder), die **Laufzeit-Platzhalter** werden nach `runtime_placeholders` aufgelöst.

  Neun neue registrierte Platzhalter (`<RUNTIME_DIR>`, `<ROOT_INSTRUCTION_FILE>`, `<ROOT_INSTRUCTION_LOCAL>`, `<PERMISSIONS_FILE>`, `<SKILLS_DIR>`, `<RULES_DIR>`, `<AGENTS_DIR>`, `<HOOKS_FILE>`, `<MCP_FILE>`) ersetzen die 17 Pfadnennungen in den Skill-Rümpfen. Sie unterscheiden sich von allen bisherigen: **Nicht der Mensch füllt sie, sondern `install.py`.** Sie sind die gerenderte Entsprechung zu den Begriffen aus D-15.

  Der Validator prüft beide Enden – die Quelle streng nach Skill-Standard, die installierte Laufzeitschicht darauf, dass kein Platzhalter unaufgelöst blieb.

  **Wirkung:** Die Client Packs schrumpfen von 80 auf 32 beziehungsweise von 79 auf 31 Dateien. 48 Dateien liegen einmal statt zweimal. Der Installationsumfang bleibt unverändert bei 80 und 79 Dateien.

### Geprüft (gemeinsame Skill-Quelle)
- Erstinstallation unverändert: 80 Dateien (`devin-desktop`), 79 (`claude-code`); `--check` gegen beide fehlerfrei.
- Gerendertes Frontmatter stichprobenartig geprüft: `fw-tests` erhält bei `devin-desktop` die Listenform mit `permissions` und `triggers`, bei `claude-code` `allowed-tools: Read, Grep, Glob, Edit, Write, Bash`.
- Platzhalterauflösung: 0 unaufgelöste Laufzeit-Platzhalter in beiden Installationen. Bei `claude-code` laufen `<PERMISSIONS_FILE>` und `<HOOKS_FILE>` erwartungsgemäß auf dieselbe Datei zusammen.
- Drift an einem gerenderten Skill: Exit 1 mit Nennung der gemeinsamen Quelle; `--update` stellt her.
- Wirksamkeitsnachweis der neuen Prüfung: `<HOOKS_FILE>` testweise aus einem Manifest entfernt → drei gemeldete Fehler; Manifest wiederhergestellt.
- Übungsrepository mit neuem Kern: 0 Fehler, `--check` fehlerfrei.

- **Ein Client Pack enthält nur noch Clientspezifisches (`CR-2026-007`, Decision Record D-17).** Von 80 Dateien sind sieben geblieben (`devin-desktop`) beziehungsweise sechs (`claude-code`): die Übersicht der Laufzeitschicht, die Berechtigungsdatei, die Hook-Konfiguration, die MCP-Vorlage, die Vorlage für nutzerlokale Ergänzungen und die Overlay-Saat.

  Alles andere liegt einmal im Kern und wird über `shared_core` / `shared_seed` des Manifests installiert:

  | Neue Ablage | Inhalt |
  |---|---|
  | `templates/project-overlay/` | Saat für Ebene 4 – hatte im Client Pack nie etwas zu suchen |
  | `templates/rules/` | die beiden Regelvorlagen |
  | `framework/runtime/` | Wurzel-Anweisung, Core-Regeltexte `00-`, `10-`, `15-`, Agentenprofil |

  `framework/runtime/` ist die werkzeugneutrale Laufzeitfassung – genau das, was D-02 seit jeher meint, aber bisher nirgends lag.

  **Drei neue Formtransformationen**, aus dem Manifest gesteuert: Regeltexte erhalten bei einem Client ohne Ladetrigger statt des YAML-Frontmatters einen Kommentar mit Zweck und Ladeverhalten; die Wurzel-Anweisung bekommt an der Marke `<!-- RUNTIME_IMPORTS -->` die Einbindungen dieses Clients; das Agentenprofil wird auf Feldname und Werkzeugformat des Clients gebracht. Neu ist der Laufzeit-Platzhalter `<CLIENT_NAME>` – der Titel der Wurzel-Anweisung nannte bisher fest einen Produktnamen und war damit in der anderen Installation schlicht falsch.

### Geprüft (geteilte Kernbestandteile)
- **Byteweiser Vergleich gegen 0.4.0**: Wurzel-Anweisung, die drei Core-Regeltexte und das Agentenprofil sind nach dem Rendern identisch mit dem bisherigen Stand. Einzige gewollte Abweichung ist der Titel, der jetzt den Namen des verwendeten Clients trägt.
- Erstinstallation unverändert: 80 Dateien (`devin-desktop`), 79 (`claude-code`); `--check` gegen beide fehlerfrei.
- Gerendertes Overlay: `devin-desktop` erhält `.devin/config.json` und `.devin/mcp_config.json`, `claude-code` erhält `.claude/settings.json` und `.mcp.json`; 0 unaufgelöste Platzhalter.
- Drift an einer gerenderten Regel: Exit 1 mit Nennung der gemeinsamen Quelle; `--update` stellt her.
- Validator gegen beide Installationen und das Übungsrepository: je 0 Fehler.

### Zwischenbefund während der Umsetzung
Beim Entfernen der Import-Marke blieb eine Leerzeile stehen. Die Wurzel-Anweisung war damit gegenüber 0.4.0 um genau ein Zeichen verschieden – genug, damit `install.py --check` in **jedem** bestehenden Projekt eine Abweichung gemeldet hätte, die keine ist. Aufgefallen ist es nur durch den byteweisen Vergleich gegen den Vorstand; die Prüfungen selbst waren grün.

### Verbliebene Duplikate zwischen den Client Packs
Von den 32 Dateien des Packs `devin-desktop` sind **18 byteweise identisch** mit ihrer Entsprechung im Pack `claude-code`:

| Bestandteil | Dateien | Warum es dort nicht hingehört |
|---|---|---|
| `project-overlay/` | 16 | Ebene 4 (Projekt) – hat mit dem Client nichts zu tun |
| `21-overlay-TEMPLATE.md.template`, `40-tech-TEMPLATE.md.template` | 2 | Framework-Vorlagen |

Die übrigen 12 zerfallen in zwei Klassen: **Inhalt Framework, Form Client** (Wurzel-Anweisung, die drei Core-Regeltexte, Agentenprofil, Berechtigungsdatei, Hook-Konfiguration) – für sie trägt der mit diesem Release gebaute Renderer – und **echt clientspezifisch** (die beiden Übersichten der Laufzeitschicht, die MCP-Vorlage, die Vorlage für nutzerlokale Ergänzungen, die Overlay-Saat).

### Messung: Wie viel Skill-Inhalt ist wirklich clientspezifisch?
Grundlage für die noch offene Zusammenführung der Skills. Verglichen wurden die 48 Dateien je Client Pack (12 Skills mal `SKILL.md`, `EXAMPLES.md`, `TESTS.md`, `CHANGELOG.md`):

| Größe | Wert |
|---|---|
| Zeilen gesamt | 3.003 |
| Abweichende Zeilen | 215 (7,2 %) |
| davon Frontmatter | 147 |
| davon Pfadnennungen im Rumpf | 68 |

**92,8 Prozent sind identisch.** Beide Abweichungsklassen sind auflösbar: Das Frontmatter ist mechanisch abbildbar (die Abbildung wurde beim Anlegen des zweiten Packs bereits einmal von Hand ausgeführt), die Pfadnennungen im Rumpf verschwinden durch dieselbe Neutralisierung, die dieser Eintrag für den Kern beschreibt.

### Befund: 63 Client-Bindungen im werkzeugneutralen Kern
Der Validator gegen die erste `claude-code`-Installation meldete 104 Fehler – keiner davon ein Programmfehler. D-02 bezeichnet `framework/` als werkzeugneutral; tatsächlich nennt der Kern an 63 Stellen die Laufzeitpfade genau eines Clients (`AGENTS.md` 37-mal, `.devin/config.json` 17-mal, `.devin/` 16-mal), verteilt über `framework/core/`, `governance/`, `docs/`, `checklists/`, `onboarding/`, `prompts/` und `tests/`.

Der Querverweis-Check unterscheidet solche Nennungen jetzt von toten Referenzen und meldet sie gesammelt als Warnung. Die Neutralisierung des Kerns ist damit eine messbare Restgröße statt einer Schätzung; sie steht noch aus.

### Geprüft
- Erstinstallation `--client claude-code`: 79 Dateien; `--check` dagegen fehlerfrei. Validator gegen beide Installationen: je 0 Fehler.
- Regression `devin-desktop`: Erstinstallation weiterhin 80 Dateien, `--check` fehlerfrei.
- Übungsrepository mit dem Kern dieses Standes gegengeprüft (simulierte Übernahme): 0 Fehler, aktivierte Packs weiterhin erkannt.
- `hook-check-secrets.py`: beide Namensformen blockieren mit Exit-Code 2, ein Quellcodepfad nicht.

### Geprüft (0.5.0, Client Packs)
- Erstinstallation in leerem Verzeichnis: 80 Dateien, kein Pack aktiv, `.devin/skills/` nur `fw-*` – identisch zum Stand vor der Verschiebung.
- `--check` gegen die frische Installation: keine Abweichung. Manipulierte Core-Datei: Exit 1 mit Nennung des Client-Pack-Pfades; `--update` stellt her.
- Unbekannter Client: Exit 1, verfügbare Packs genannt.
- `FW-KO-04` meldete unmittelbar nach der Verschiebung genau die zwei gebrochenen Querverweise in `README.md` und `ADOPTION_GUIDE.md` – ohne die historischen Nennungen in `CHANGELOG.md` fälschlich mitzumelden.

### Bekannte Einschränkungen
- Die Querverweisprüfung prüft die Existenz von Dateien und Verzeichnissen, nicht die Gültigkeit von Anker-Fragmenten (`datei.md#abschnitt`).
- Backtick-Pfade werden nur unter den Framework-Wurzeln geprüft; Pfade in den Projektbereichen eines aufnehmenden Repositorys bleiben ungeprüft.
- Das Übungsrepository (Testprojekt) trägt weiterhin die Kernkopie aus 0.4.0 und erhält die neue Prüfung erst mit der Übernahme des Release 0.5.0.
- Berechtigungsdatei und Hook-Konfiguration liegen weiterhin je Client Pack. Sie sind mehr als eine Formfrage: Eine gemeinsame Quelle erfordert die Semantikabbildung der Regeln (Werkzeugnamen, Präfixmuster, getrennte Werkzeuge für Ändern und Anlegen) und ist einem eigenen Änderungsantrag vorbehalten.
- Zwei Pfadnennungen verbleiben in Roadmap-AP2; sie sind dort begründet und mit einem Hinweis auf die Wiederholung je Client Pack versehen.
- Ohne installiertes `PyYAML` prüft der Validator das Frontmatter von Regeln und Skills nur eingeschränkt.
- Ein Client Pack fügt eine Verschachtelungsebene hinzu: Der längste relative Pfad wächst von 89 auf 111 Zeichen. Unter Windows mit `MAX_PATH` von 260 Zeichen bleiben damit rund 149 Zeichen für den Projektpfad. Bei sehr langen Basispfaden ist entweder die erweiterte Pfadunterstützung des Betriebssystems zu aktivieren oder ein kürzerer Ablageort zu wählen.

### Migrationshinweise
Keine. Kein Overlay-Feld, kein Laufzeitartefakt (`AGENTS.md`, `.devin/`) und kein Onboarding-Schritt referenziert die Release-Definition.

## [0.4.0] – 2026-09-09

### Geändert
- **Kein Pack ist nach einer Erstinstallation mehr aktiv — auch nicht das Referenzpack `software-development`.** Dessen Laufzeitfassung lag bisher als Saatdatei in `root-template/.devin/rules/30-role-software-development.md` und kam damit bei jeder Installation mit. Das widersprach der eigenen Regel in `framework/role-packs/README.md` Punkt 4, wonach ein Pack im Overlay aktiviert wird. Die Datei liegt jetzt in der Pack-Quellablage unter `framework/role-packs/software-development/runtime/`, wie beim Pack `requirements-engineering`.

  Damit ist der Mechanismus für alle Packs einheitlich:

  | Schritt | Wer |
  |---|---|
  | Pack liegt im Kern (`<pack>/runtime/`, `<pack>/skills/`) | Framework |
  | Rolle im Overlay Abschnitt 1 aufführen, Bestandteile nach `.devin/` kopieren | Projekt |
  | Kopierte Bestandteile auf dem Stand des Releases halten | `install.py --update` |

  `install.py` legt kein Pack mehr an: Eine Erstinstallation umfasst jetzt 80 statt 81 Dateien.

- `framework/role-packs/README.md`: Aktivierung mit Befehlsbeispiel beschrieben; der Sonderweg des Referenzpacks entfällt.
- `framework/role-packs/software-development/ROLE_PACK.md`: neuer Abschnitt 5b „Aktivierung im Projekt".
- `docs/ADOPTION_GUIDE.md` (jetzt 0.4.0): „Packs aktivieren" ist ein eigener Schritt 5 der Neuaufnahme; Abschnitt 3 nennt die Pack-Bestandteile ausdrücklich im Aktualisierungsumfang. Bei den projektspezifischen Bestandteilen steht nun die **Entscheidung**, welche Packs aktiv sind — nicht mehr die kopierten Dateien selbst, denn deren Inhalt ist Framework-Gut.

### Migrationshinweise
Ein Projekt, das das Referenzpack bereits nutzt, ist **nicht betroffen**: Die vorhandene `.devin/rules/30-role-software-development.md` wird ab 0.3.1 als Bestandteil eines aktivierten Packs erkannt und von `install.py --update` auf dem Stand gehalten. Zwei Dinge sind nachzuziehen:

1. Falls die Rolle Softwareentwicklung im Overlay Abschnitt 1 nicht ausdrücklich aufgeführt ist, dort ergänzen — die Aktivierung war bisher implizit.
2. Bei einer **Neuinstallation** in einem weiteren Repository muss das Pack künftig ausdrücklich aktiviert werden; sonst fehlt `30-role-software-development.md`. Der Validator verlangt die Datei nicht, das Pack wäre also stillschweigend inaktiv.

### Geprüft
- Frische Installation in einem leeren Verzeichnis: 80 Dateien angelegt, `.devin/rules/` enthält nur die Core-Regeln und die beiden `*-TEMPLATE`-Vorlagen, `.devin/skills/` nur die zwölf `fw-*`-Skills — kein `role-*`- oder `tech-*`-Skill, keine Pack-Laufzeitfassung.
- `validate-framework.py`: 0 Fehler, 0 Warnungen.

## [0.3.1] – 2026-09-09

### Behoben
- **`install.py` aktualisiert jetzt auch aktivierte Pack-Bestandteile.** Bisher blieben ein nach `.devin/skills/` kopierter Pack-Skill und eine nach `.devin/rules/` kopierte Pack-Laufzeitfassung bei einem Release-Wechsel unberührt: `--update` fasste sie nicht an und `--check` meldete „Core ist auf dem Stand des Releases", obwohl die Kopie abwich. Ein Projekt behielt damit stillschweigend die Fassung aus dem Release, in dem es das Pack aktiviert hatte — eine Verbesserung am Pack-Skill hätte es nie erreicht.

  Die zugrunde liegende Unterscheidung ist jetzt sauber gezogen: **Ob** ein Pack aktiv ist, entscheidet das Projekt (Overlay Abschnitt 1) — `install.py` aktiviert nach wie vor nichts von selbst. **Was** in einem aktivierten Pack-Skill steht, ist Framework-Inhalt und gehört damit zum Aktualisierungsumfang.

  Erfasst wird nur, was in einer Pack-Quellablage dieses Kerns eine Entsprechung hat. Projekteigene Packs — etwa unter `project-overlay/tech-packs/` — bleiben unberührt; das ergibt sich automatisch aus dem Abgleich gegen die Quellablage und braucht keine Sonderregel.

  Gefunden durch die Frage, warum die `fw-*`-Skills in der Laufzeitschicht liegen und ein Pack-Skill in der Pack-Quellablage. Wirksamkeit nachgewiesen: manipulierte Kopie → `--check` Exit 1 mit Nennung der Pack-Quelle → `--update` stellt her → Exit 0. Der Überwachungsumfang im Erprobungsprojekt wuchs dadurch von 60 auf 65 Dateien.

### Offener Punkt (mit 0.4.0 erledigt)
- Das Referenzpack `software-development` brachte seine Laufzeitfassung als Saatdatei in `root-template/.devin/rules/30-role-software-development.md` mit und wird damit bei jeder Erstinstallation aktiv. Das widerspricht `framework/role-packs/README.md` Punkt 4, wonach ein Pack im Overlay aktiviert werden muss. `requirements-engineering` folgt dem dokumentierten Weg über `<pack>/runtime/`. Die Vereinheitlichung würde bestehende Projekte betreffen, die das Pack ohne ausdrückliche Aktivierung nutzen, und ist deshalb einem eigenen Release vorbehalten.

## [0.3.0] – 2026-09-09

### Hinzugefügt
- **Role Pack `requirements-engineering` (RP-RE)** – Ebene 6, Status `entwurf`. Konkretisiert das Arbeitsmodell für die Formulierung von Anforderungen und schließt damit das erste der sechs bislang nur vorgesehenen Packs.
  - `ROLE_PACK.md` mit Abgrenzung, EARS-Syntax, Nachvollziehbarkeit, Werkzeug- und Sprachneutralität sowie Aktivierungsanleitung.
  - **Skill `role-re-ticket` (`RP-RE-SK-001`)** – M1, rein lesend (`deny` auf `edit` und `exec`). Erzeugt aus einer Absicht eine umsetzungsreife Aufgabenbeschreibung: Beschreibung, EARS-Anforderungen, Arbeitspakete, Abnahmekriterien, Änderungsmitteilung. Recherchiert dafür die Codebasis anhand von vier festgelegten Fragen, jede Antwort mit Fundstelle.
  - Laufzeitfassung `runtime/30-role-requirements-engineering.md` (`trigger: model_decision`), zur Aktivierung nach `.devin/rules/` zu kopieren.
  - Vollständiger Satz nach Skill-Standard: `SKILL.md`, `EXAMPLES.md` (ein Positiv- und sieben Negativbeispiele), `TESTS.md` (5 Positiv-, 10 Negativtests), `CHANGELOG.md`.

### Zentrale Regel des neuen Packs
- **Der Ist-Zustand ist keine Anforderung.** Sobald bei der Anforderungsformulierung Code mitgelesen wird, entsteht die Gefahr, dass aus einem Befund („der Code antwortet mit 409") eine Anforderung wird („das System soll mit 409 antworten"). Damit wäre die Implementierung ihre eigene Spezifikation und jede Prüfung zirkulär. Das Pack trennt deshalb verbindlich drei Kategorien: **Anforderung** (nur vom Menschen, `shall`), **Befund** (aus dem Code, mit Fundstelle, nie `shall`) und **Randbedingung** (aus Schema, Vertrag, Migration oder Test, mit Fundstelle, nie `shall`). Ein Befund kann eine Anforderung auslösen — aber erst, nachdem ein Mensch entschieden hat; der Skill legt diese Entscheidung offen, statt sie zu treffen.

### Geändert
- `framework/role-packs/README.md`: `requirements-engineering` von „vorgesehen" auf „entwurf"; neuer Abschnitt zur Quellablage der Laufzeitfassung (`<pack>/runtime/`) mit der Klarstellung, dass `install.py` die Aktivierung eines Packs bewusst nicht vorwegnimmt — sie ist eine Projektentscheidung nach Overlay Abschnitt 1.
- `OWNERS.md`: Pack und Skill eingetragen.

### Abgrenzung zu bestehenden Skills
- `role-re-ticket` bewertet **kein** Risiko und schlägt **keine** Kontrollstufe vor. Das leistet `fw-change-analyze` mit der ausgearbeiteten Faktorenliste R1–R13. Der neue Skill recherchiert nur so weit, wie es zum Formulieren nötig ist, und empfiehlt `fw-change-analyze` als Folgeschritt. Zwei Skills mit derselben Codeanalyse in unterschiedlicher Tiefe liefern über die Zeit widersprüchliche Ergebnisse.
- Der Skill schreibt nichts in ein Ticketsystem; die Übertragung des Entwurfs bleibt beim Menschen (V11). Damit ist kein MCP-Server mit Schreibrechten auf ein Ticketsystem erforderlich.

### Behoben
- **`validate-framework.py` prüft jetzt auch die Skill-Quellablagen der Packs** (`framework/role-packs/<pack>/skills/` und `framework/tech-packs/<pack>/skills/`). Bisher wurde ausschließlich `.devin/skills/` geprüft — ein Pack-Skill fiel damit erst auf, nachdem ein Projekt ihn aktiviert hatte, also nach der Auslieferung. Ein Release konnte einen Skill enthalten, der den Skill-Standard verletzt. Gleiche Skillnamen in Quellablage und aktivierter Schicht werden als Kopie erkannt und nicht als ID-Konflikt gemeldet. Gefunden beim Anlegen des Packs `requirements-engineering`.

### Migrationshinweise
- Keine. Das Pack ist optional und wird erst durch Aktivierung im Overlay wirksam (Abschnitt 1 sowie Kopieren von Laufzeitfassung und Skill). Bestehende Overlays sind nicht betroffen.
- Projekte, die das Pack aktivieren, setzen `<ISSUE_TRACKER>` in Overlay Abschnitt 13 und prüfen die Sprachregeln in Abschnitt 9. Ein Glossar als Manifest-Typ `glossary` verbessert die Begriffstreue erheblich.

### Bekannte Einschränkungen
- Die 15 Testfälle des Skills haben durchgehend den Ergebnisstatus `offen`: Sie sind für eine Testsitzung auf dem Übungsrepository spezifiziert, aber noch nicht ausgeführt.
- Die Ableitung der Auszeichnungssyntax aus `<ISSUE_TRACKER>` deckt JIRA-Wiki, Markdown und eine neutrale Form ab. Andere Werkzeuge erfordern eine ausdrückliche Formatangabe beim Aufruf.

## [0.2.0] – 2026-09-09

### Geändert (strukturell, ohne inhaltliche Regeländerung)
- **Der Kern liegt jetzt in einem einzigen Verzeichnis:** `leitwerk-core/`. Dorthin verschoben wurden `framework/`, `templates/`, `prompts/`, `checklists/`, `decision-trees/`, `onboarding/`, `examples/`, `governance/`, `pilot/`, `docs/`, `tests/`, `build/` sowie `VERSION`, `CHANGELOG.md` und `OWNERS.md`. Die Übernahme in ein Projekt ist damit das Kopieren eines Ordners statt der Einzelübernahme von sechzehn Wurzeleinträgen.
- Im Wurzelverzeichnis verbleiben nur die Bestandteile, deren Ladeort Werkzeugkonvention ist und nicht konfigurierbar `[DOK]`: `AGENTS.md` und `.devin/`. Dazu `project-overlay/` als austauschbare Projektkonfiguration und die Repository-Einstiegsdateien `README.md` und `.gitignore`.
- Alle 803 Pfadverweise in Dokumenten, Regeln, Skills und Skripten wurden nachgezogen. Projektpfad-Beispiele in der Overlay-Vorlage (`src/**`, `test/**`, `docs/**`) blieben unverändert, weil sie Projektpfade bezeichnen und nicht Framework-Verzeichnisse.
- Die projektlokale Sperrbegriffsliste liegt nun unter `project-overlay/forbidden-terms.txt` statt unter `tests/`. Sie ist Projektbestand, nicht Kern; der bisherige Ort widersprach dieser Zuordnung. `validate-framework.py` liest sie am neuen Ort.
- `.devin/hooks.v1.json` ruft die Hook-Skripte unter `leitwerk-core/tests/scripts/` auf.
- `build/assemble.py` unterscheidet jetzt zwei Wurzeln: `CORE` für die Kapitelquellen, `REPO` für die `{{EMBED}}`-Ziele (`AGENTS.md`, `.devin/`, `project-overlay/` liegen im Wurzelverzeichnis). `build-docx.py` liest den Dateinamen des Ausgabedokuments aus `VERSION` statt ihn fest zu verdrahten.

### Hinzugefügt
- **`leitwerk-core/install.py`** – legt die Wurzelbestandteile aus `leitwerk-core/root-template/` an und trennt dabei Core von Projekt:
  - Core (wird bei `--update` überschrieben): `AGENTS.md`, `AGENTS.local.md.example`, `.devin/rules/00-`, `10-`, `15-`, die `21-`/`40-TEMPLATE`-Vorlagen, `.devin/rules/README.md`, `.devin/skills/fw-*`, `.devin/agents/`, `hooks.v1.json`, `mcp_config.json.example`, `.devin/README.md`.
  - Projekt (wird nie überschrieben): `.devin/config.json`, `.devin/rules/20-project-overlay.md`, `30-*`, `40-<name>`, `2N-overlay-*`, `.devin/skills/prj-*`, `project-overlay/**`.
  - `--check` meldet fehlende und lokal veränderte Core-Dateien (Exit-Code 1) und deckt damit Bearbeitung an der falschen Stelle auf. `--dry-run` zeigt den Ablauf ohne Schreibvorgang.
  - Die `fw-*`-Skills werden zur Laufzeit ermittelt; neue Skills eines Releases kommen ohne Anpassung des Skripts mit.
- **`leitwerk-core/root-template/`** – einzige Quelle der Wurzelbestandteile.

### Migrationshinweise für bestehende Overlays
Die Ebenenhierarchie, alle Regeln, Kontextklassen, Kontrollstufen, Betriebsmodi, Skills und Prüfschritte sind **inhaltlich unverändert**. Ein bestehendes Projekt migriert so:

1. Die zwölf Core-Verzeichnisse und `VERSION`, `CHANGELOG.md`, `OWNERS.md` aus dem Wurzelverzeichnis entfernen und das neue `leitwerk-core/` hineinkopieren.
2. `python leitwerk-core/install.py --update` ausführen. `AGENTS.md` und die Core-Regeln werden aktualisiert; das Overlay und `config.json` bleiben unberührt.
3. `tests/forbidden-terms.txt` nach `project-overlay/forbidden-terms.txt` verschieben, falls das Projekt eine gefüllte Liste hatte.
4. Eigene Verweise auf Framework-Pfade im Overlay und in `prj-*`-Skills um das Präfix `leitwerk-core/` ergänzen. Betroffen sind Verweise auf `framework/`, `checklists/`, `decision-trees/`, `prompts/`, `templates/`, `onboarding/`, `governance/`, `pilot/`, `examples/`, `docs/ADOPTION_GUIDE.md`, `docs/PLACEHOLDER_REGISTRY.md`, `docs/ROADMAP.md`, `tests/TEST_CATALOG.md` und `tests/scripts/`. Verweise auf eigene Projektpfade bleiben unverändert.
5. `.gitignore`: Die vier Zeilen `/AGENTS.md`, `/AGENTS.local.md.example`, `/.devin/` und `/project-overlay/` gelten nur im Framework-Repository und dürfen im Projekt **nicht** übernommen werden.
6. Overlay-Version erhöhen, kompatible Framework-Version auf `0.2.x` setzen, `validate-framework.py --strict-overlay` und `install.py --check` ausführen.

Der Aufwand liegt bei Schritt 4 und ist proportional zur Zahl eigener Framework-Verweise; alles Übrige sind zwei Befehle.

### Behoben
- `validate-framework.py` überspringt erzeugte Lockdateien (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Cargo.lock`, `poetry.lock`, `go.sum` und weitere). Sie enthalten naturgemäß fremde E-Mail-Adressen und Registry-Adressen und werden weder vom Framework noch vom Projekt redaktionell gepflegt; die Inhaltsprüfung dagegen erzeugte einen Fehler und mehrere hundert Warnungen, sobald in einem Projekt `npm install` gelaufen war. Gefunden bei der Erprobung am Testprojekt Bibliotheksverwaltung.

### Bekannte Einschränkungen
- Unverändert gegenüber 0.1.0: Kein Mechanismus wurde bislang in einer Zielinstallation von Devin Desktop ausgeführt (Validierung in Roadmap-AP2); die verify-Punkte bleiben offen.
- Im Framework-Repository sind `AGENTS.md`, `.devin/` und `project-overlay/` Erzeugnisse und nicht versioniert. Nach dem Klonen ist `python leitwerk-core/install.py` erforderlich, bevor der Validator läuft. In einem Projekt gilt das nicht — dort sind diese Pfade versionierter Projektbestand.
- `validate-framework.py --strict-overlay` ist im Framework-Repository erwartungsgemäß rot (neun Fehler), weil `project-overlay/` hier die Vorlage mit offenen Platzhaltern ist. Ohne das Flag: 0 Fehler, 0 Warnungen.

## [0.1.0] – 2026-09-01

### Hinzugefügt
- Erstfassung des gesamten Frameworks (Status aller Module: `entwurf`): Framework Core (FW-CORE-00…10), zentrale Agentenanweisung `AGENTS.md`, Devin-Laufzeitschicht `.devin/` (Regeln, Berechtigungen, Hooks, Subagent-Profil, MCP-Vorlage), Project-Overlay-Vorlage mit Manifest und Dokumentenmechanismus, Role-Pack-Struktur mit Referenzpack Softwareentwicklung, Technology-Pack-Struktur mit Vorlagen, Skill-Standard und Skill-Template, zwölf Referenz-Skills (FW-SK-001…012), Prompt-Bibliothek (FW-PR-001…012), elf Checklisten (FW-CL-01…11), sechs Entscheidungsbäume (FW-DT-01…06, Mermaid validiert), Onboarding-Paket (Quick-Start, Leitfaden, Mentor-Checkliste, Übungen, Wissenstest, Kriterien, Nachschlagewerk), Governance (RACI, Prioritätshierarchie, Release-, Änderungs-, Ausnahme-, Feedback-, Vorfallprozess, Decision Log), Testkatalog mit Validierungsskripten, Pilotkonzept mit Metriken, Adoption Guide, Roadmap (AP1–AP13), Beispiele (synthetisch), Platzhalterregister.

### Migrationshinweise
- Keine (Erstfassung). Projekte übernehmen über `leitwerk-core/docs/ADOPTION_GUIDE.md` und `leitwerk-core/checklists/10-project-adoption.md`.

### Bekannte Einschränkungen
- Kein Mechanismus wurde bislang in einer Zielinstallation von Devin Desktop ausgeführt; alle produktbezogenen Aussagen tragen Belegstatus (`[DOK]`/`[EMPF]`/`[KONZ]`) und offene Punkte den Marker `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>`. Validierung erfolgt in Roadmap-AP2.
- Zeichenlimits für Regeldateien unter Devin Local, exakte `config.json`-Schemadetails, Hook-Eingabeschema, Skill-Discovery über `.agents/skills/` und Codebasis-Indexierung sind zu verifizieren (Klärungspunkte K-18…K-20, Verifikationsliste im Hauptdokument).
- `leitwerk-core/tests/scripts/hook-check-secrets.py` läuft bis zur Validierung in AP2 standardmäßig fail-open (Umgebungsvariable `FW_HOOK_FAIL_CLOSED=1` aktiviert fail-closed).
- Technology Packs enthalten noch kein konkretes Pack (bewusst; entsteht projektbezogen in AP4).
