# Änderungsverzeichnis (Framework)

Format: Semantic Versioning; je Release Änderungen, Migrationshinweise für Overlays und bekannte Einschränkungen. Prozess: `devin-core-framework/governance/RELEASE_PROCESS.md`.

## [0.5.0] – 2026-09-10

### Geändert
- **Definition des Release 1.0.0 (`CR-2026-001`, Decision Record D-11, ersetzt D-09).** 1.0.0 bezeichnet künftig den Stand „technisch validiert und übertragbar" mit fünf prüfbaren Kriterien: kein unbearbeiteter VERIFY-Marker, Testkatalog vollständig protokolliert (kein Testfall `offen`), alle Modulstatus oberhalb `entwurf`, kein Decision Record im Status `entschieden (Vorschlag)`, Übernahme in ein zweites Projekt nachgewiesen.

  Pilot (AP9), Onboarding (AP8) und organisatorische Freigabe (AP10) sind **keine** Vorbedingung mehr für 1.0.0. Sie setzen eine aufnehmende Organisation mit besetzten Rollen voraus und sind damit projektseitige Arbeitspakete; in der Roadmap hängen sie jetzt an AP13 (Übernahme). AP11 folgt direkt auf AP7.

  Hintergrund: Die bisherige Definition machte das Release-Gate `FW-CL-11` strukturell unerreichbar, solange keine Organisation benannt ist – obwohl die verbleibenden Lücken ausschließlich Nachweise betreffen. Ein Release 1.0.0 erklärt ausdrücklich nicht, dass das Framework im Realbetrieb erprobt wurde.

- `devin-core-framework/checklists/11-framework-release.md`: vier Prüfpunkte mit der Kennzeichnung **(ab 1.0.0, D-11)** ergänzt.
- `devin-core-framework/docs/ROADMAP.md`: Abhängigkeitsgraph und Arbeitspakete AP8–AP13 neu zugeordnet; AP8–AP10 auf P3 und als projektseitig gekennzeichnet.
- Neue Ablage für Änderungsanträge: `devin-core-framework/governance/change-requests/`.

### Hinzugefügt
- **Querverweisprüfung im Validator (`FW-KO-04`).** `validate-framework.py` prüft als zwölfte Prüfung, dass Markdown-Links und in Backticks genannte Framework-Pfade auf existierende Dateien oder Verzeichnisse zeigen. Der Testkatalog führte diese Prüfung bislang als `skript (validate-framework.py-Erweiterung <TBD>)` mit Ergebnisstatus `offen`; sie ist jetzt umgesetzt und bestanden.

  Nicht als Fehler gewertet werden – jeweils im Skript begründet – Laufzeitfassungen aktivierter Packs (`.devin/rules/2N-`, `30-`, `40-`, `.devin/skills/role-`, `tech-`, `prj-`), nutzerlokale Dateien mit Namensbestandteil `.local.`, Pfade mit vorhandener `.example`- oder `.template`-Fassung sowie Globs, Platzhalter und Befehlszeilen.

  Wirksamkeit belegt: Sondendatei mit zwei defekten Verweisen und vier Nicht-Pfad-Angaben → genau 2 Fehler, keine Fehlmeldung. Umbenennungssimulation `devin-core-framework/` → `agent-core-framework/` → 685 gemeldete Fehler. Damit ist die für 0.5.0 vorgesehene Umbenennung abgesichert.

- **Ablage für Testprotokolle: `devin-core-framework/tests/protocols/`.** Löst `<TBD: Ablage der Testprotokolle>` aus dem Testkatalog. Namensschema `JJJJ-MM-TT-<Test-ID>.md` beziehungsweise `JJJJ-MM-TT-release-<Version>.md`; ein Ergebnisstatus außer `offen` MUSS auf ein Protokoll verweisen. Erster Eintrag: `2026-09-10-FW-KO-04.md`.

- **Client Packs als Abbildungsschicht (`CR-2026-002`, Decision Record D-12).** Neu unter `devin-core-framework/clients/`: `README.md`, die Vorlage `_template/CLIENT_PACK.md` und das erste Pack `devin-desktop/CLIENT_PACK.md`.

  Kern der Vorlage ist die **Fähigkeitsmatrix**: 26 technische Zusagen des Frameworks in sieben Gruppen (Regelladung, Skills, Berechtigungen, Hooks, Agentenprofile, Modi, externe Anbindung), jede eingestuft als `[TECHNISCH]` (die Engine erzwingt sie), `[TEXTUELL]` (nur Anweisung im Kontext) oder `[NICHT ABBILDBAR]`. Sechs davon sind Kernzusagen und entsprechen `_core_rules_integrity` in der Berechtigungsdatei; weicht eine ab, ist sie einzeln zu begründen, im Overlay als Ausnahme zu führen und durch `<SECURITY_CONTACT>` freizugeben.

  Ein Client Pack ist **keine Regelebene**. Es führt keine Verhaltensregel ein und lockert keine; die achtstufige Prioritätshierarchie (D-06) bleibt unberührt. Bei Widerspruch zur werkzeugneutralen Langform gilt die Langform.

  Befund aus dem ersten ausgefüllten Pack: 21 der 26 Zusagen sind als `[TECHNISCH]` vorgesehen, alle sechs Kernzusagen darunter – aber **13 der 26 Zeilen tragen einen VERIFY-Marker und keine einzige Einstufung ist gegen eine Installation geprüft**. Besonders: Der Schutz-Hook läuft fail-open, die Zusage „Prüfung kann blockieren" ist damit derzeit `[TEXTUELL]`.

- Neue Platzhalter: `<CLIENT_PACK_NAME>`, `<CLIENT_PACK_CODE>` sowie der clientneutrale Marker `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>`, der die devin-spezifische Form ab 0.5.0 ersetzt.

- **Wurzelartefakte je Client Pack; `install.py --client` (`CR-2026-003`, Decision Record D-13).** `devin-core-framework/root-template/` liegt jetzt unter `devin-core-framework/clients/devin-desktop/root-template/`. Ein Client Pack besteht damit aus `CLIENT_PACK.md` (was der Client durchsetzt) und `root-template/` (was installiert wird).

  `install.py` kennt `--client` (Standard `devin-desktop`) und `--list-clients`; die Vorlage wird aus dem gewählten Pack abgeleitet statt aus einer Konstanten. Ein unbekannter Client bricht mit Exit-Code 1 ab und nennt die verfügbaren Packs.

  Die Schicht selbst wanderte von `framework/client-packs/` nach `clients/` – aus zwei Gründen. Inhaltlich: Unter `framework/` liegen die Regelebenen, und D-12 hält fest, dass ein Client Pack keine ist. Technisch: Die erste Testinstallation brach unter Windows an `MAX_PATH` ab, weil der längste relative Pfad von 89 auf 126 Zeichen wuchs; unter `clients/` sind es 111.

  **Für aufnehmende Projekte ändert sich nichts.** `install.py` ohne Schalter verhält sich unverändert; die installierten Artefakte sind byteweise dieselben. Betroffen ist nur, wer den Kern selbst bearbeitet: Core-Änderungen gehören jetzt nach `devin-core-framework/clients/<client>/root-template/`.

- **Zweites Client Pack: `claude-code` (`CR-2026-004`, Decision Record D-14).** Vollständiges `root-template/` mit 79 Dateien – eine weniger als `devin-desktop`, weil die Hooks dort in einer eigenen Datei stehen und hier in der Berechtigungsdatei aufgehen.

  **Die Abstraktion trägt.** Alle sechs Kernzusagen sind auch bei diesem Client technisch abgebildet (20 von 26 Zusagen `[TECHNISCH]`, gegenüber 21 bei `devin-desktop`). Die vier nicht abbildbaren Zusagen betreffen ausschließlich Least Context und Ergonomie, keine Schutzzusage: Der Client kennt keine Regeldateien mit Ladetriggern. Die Regeltexte sind inhaltlich identisch und werden über Importe in der Wurzel-Anweisung stets geladen – eine Verschärfung, die rund 22.000 Zeichen ständigen Kontext kostet.

- **Manifeste je Client Pack.** `install.py` hatte die Core- und Saatpfade fest auf `.devin/` verdrahtet; sie stehen jetzt in `clients/<name>/manifest.json`. Ein Pack ohne Manifest gilt als nicht installierbar.

- **Der Validator ist clientneutral.** `check_required`, `check_config`, `check_rules` und `skill_dirs` liefen fest gegen `.devin/`; sie ermitteln die Laufzeitschicht jetzt über `detect_client()`. Mehrere gleichzeitig vorhandene Laufzeitschichten sind ein Fehler. `check_rules` unterscheidet zwei Bauarten: mit Ladetriggern wird das Frontmatter geprüft, ohne Ladetrigger, dass jede Kernregel in der Wurzel-Anweisung **eingebunden** ist – dort ist eine nicht eingebundene Regeldatei stillschweigend wirkungslos.

- **`hook-check-secrets.py` schützt beide Namensformen** der Wurzel-Anweisung und der Laufzeitschicht. Das Skript war schema-agnostisch und läuft bei beiden Clients unverändert.

- **Der Kern ist neutralisiert (`CR-2026-005`, Decision Record D-15).** Er bezeichnet die Bestandteile der Laufzeitschicht jetzt mit Begriffen statt mit Pfaden: Wurzel-Anweisungsdatei, Laufzeitschicht, Berechtigungsdatei, Regelablage, Skill-Ablage, Agentenprofile, Hook-Konfiguration, MCP-Konfiguration, nutzerlokale Überschreibung.

  Neu: `devin-core-framework/docs/RUNTIME_GLOSSARY.md` bildet jeden Begriff auf die Pfade je Client Pack ab – das Gegenstück zum Platzhalterregister. Die Regel: im Kern der Begriff, im Client Pack der Pfad, in historischen Dokumenten bleibt beides unverändert.

  **61 von 63 Stellen ersetzt**, gemessen nach jedem Durchgang: 63 → 57 → 33 → 23 → 8 → 2. Die zwei verbliebenen stehen in Roadmap-AP2, das bewusst die Mechanismen *eines* Clients validiert; dort steht jetzt der Hinweis, dass es je Client Pack zu wiederholen ist.

  Mitgenommen: Wo die Prosa eine Eigenschaft beschreibt und keinen Beleg, ist auch der Produktname gewichen – „Devin passt Tests an" wurde zu „Das Werkzeug passt Tests an", „Devin-Nutzungsvermerk" zu „KI-Nutzungsvermerk".

  Decision Record D-02 wurde **nicht** umgeschrieben – ein Decision Record beschreibt eine Entscheidung zu ihrem Zeitpunkt. Er trägt einen Fortschreibungsvermerk auf D-12 bis D-14.

  **Keine Regel wurde inhaltlich geändert.** Nachgewiesen durch byteweise unveränderte Installationen: weiterhin 80 Dateien (`devin-desktop`) und 79 (`claude-code`), `--check` fehlerfrei.

- **Die Skills haben eine gemeinsame Quelle (`CR-2026-006`, Decision Record D-16).** Sie liegen jetzt einmal unter `devin-core-framework/framework/skills/` und werden bei der Installation in die Form des gewählten Clients gebracht. Ein neuer Skill wird einmal geschrieben und gilt für alle Client Packs.

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
- **Der Kern liegt jetzt in einem einzigen Verzeichnis:** `devin-core-framework/`. Dorthin verschoben wurden `framework/`, `templates/`, `prompts/`, `checklists/`, `decision-trees/`, `onboarding/`, `examples/`, `governance/`, `pilot/`, `docs/`, `tests/`, `build/` sowie `VERSION`, `CHANGELOG.md` und `OWNERS.md`. Die Übernahme in ein Projekt ist damit das Kopieren eines Ordners statt der Einzelübernahme von sechzehn Wurzeleinträgen.
- Im Wurzelverzeichnis verbleiben nur die Bestandteile, deren Ladeort Werkzeugkonvention ist und nicht konfigurierbar `[DOK]`: `AGENTS.md` und `.devin/`. Dazu `project-overlay/` als austauschbare Projektkonfiguration und die Repository-Einstiegsdateien `README.md` und `.gitignore`.
- Alle 803 Pfadverweise in Dokumenten, Regeln, Skills und Skripten wurden nachgezogen. Projektpfad-Beispiele in der Overlay-Vorlage (`src/**`, `test/**`, `docs/**`) blieben unverändert, weil sie Projektpfade bezeichnen und nicht Framework-Verzeichnisse.
- Die projektlokale Sperrbegriffsliste liegt nun unter `project-overlay/forbidden-terms.txt` statt unter `tests/`. Sie ist Projektbestand, nicht Kern; der bisherige Ort widersprach dieser Zuordnung. `validate-framework.py` liest sie am neuen Ort.
- `.devin/hooks.v1.json` ruft die Hook-Skripte unter `devin-core-framework/tests/scripts/` auf.
- `build/assemble.py` unterscheidet jetzt zwei Wurzeln: `CORE` für die Kapitelquellen, `REPO` für die `{{EMBED}}`-Ziele (`AGENTS.md`, `.devin/`, `project-overlay/` liegen im Wurzelverzeichnis). `build-docx.py` liest den Dateinamen des Ausgabedokuments aus `VERSION` statt ihn fest zu verdrahten.

### Hinzugefügt
- **`devin-core-framework/install.py`** – legt die Wurzelbestandteile aus `devin-core-framework/root-template/` an und trennt dabei Core von Projekt:
  - Core (wird bei `--update` überschrieben): `AGENTS.md`, `AGENTS.local.md.example`, `.devin/rules/00-`, `10-`, `15-`, die `21-`/`40-TEMPLATE`-Vorlagen, `.devin/rules/README.md`, `.devin/skills/fw-*`, `.devin/agents/`, `hooks.v1.json`, `mcp_config.json.example`, `.devin/README.md`.
  - Projekt (wird nie überschrieben): `.devin/config.json`, `.devin/rules/20-project-overlay.md`, `30-*`, `40-<name>`, `2N-overlay-*`, `.devin/skills/prj-*`, `project-overlay/**`.
  - `--check` meldet fehlende und lokal veränderte Core-Dateien (Exit-Code 1) und deckt damit Bearbeitung an der falschen Stelle auf. `--dry-run` zeigt den Ablauf ohne Schreibvorgang.
  - Die `fw-*`-Skills werden zur Laufzeit ermittelt; neue Skills eines Releases kommen ohne Anpassung des Skripts mit.
- **`devin-core-framework/root-template/`** – einzige Quelle der Wurzelbestandteile.

### Migrationshinweise für bestehende Overlays
Die Ebenenhierarchie, alle Regeln, Kontextklassen, Kontrollstufen, Betriebsmodi, Skills und Prüfschritte sind **inhaltlich unverändert**. Ein bestehendes Projekt migriert so:

1. Die zwölf Core-Verzeichnisse und `VERSION`, `CHANGELOG.md`, `OWNERS.md` aus dem Wurzelverzeichnis entfernen und das neue `devin-core-framework/` hineinkopieren.
2. `python devin-core-framework/install.py --update` ausführen. `AGENTS.md` und die Core-Regeln werden aktualisiert; das Overlay und `config.json` bleiben unberührt.
3. `tests/forbidden-terms.txt` nach `project-overlay/forbidden-terms.txt` verschieben, falls das Projekt eine gefüllte Liste hatte.
4. Eigene Verweise auf Framework-Pfade im Overlay und in `prj-*`-Skills um das Präfix `devin-core-framework/` ergänzen. Betroffen sind Verweise auf `framework/`, `checklists/`, `decision-trees/`, `prompts/`, `templates/`, `onboarding/`, `governance/`, `pilot/`, `examples/`, `docs/ADOPTION_GUIDE.md`, `docs/PLACEHOLDER_REGISTRY.md`, `docs/ROADMAP.md`, `tests/TEST_CATALOG.md` und `tests/scripts/`. Verweise auf eigene Projektpfade bleiben unverändert.
5. `.gitignore`: Die vier Zeilen `/AGENTS.md`, `/AGENTS.local.md.example`, `/.devin/` und `/project-overlay/` gelten nur im Framework-Repository und dürfen im Projekt **nicht** übernommen werden.
6. Overlay-Version erhöhen, kompatible Framework-Version auf `0.2.x` setzen, `validate-framework.py --strict-overlay` und `install.py --check` ausführen.

Der Aufwand liegt bei Schritt 4 und ist proportional zur Zahl eigener Framework-Verweise; alles Übrige sind zwei Befehle.

### Behoben
- `validate-framework.py` überspringt erzeugte Lockdateien (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Cargo.lock`, `poetry.lock`, `go.sum` und weitere). Sie enthalten naturgemäß fremde E-Mail-Adressen und Registry-Adressen und werden weder vom Framework noch vom Projekt redaktionell gepflegt; die Inhaltsprüfung dagegen erzeugte einen Fehler und mehrere hundert Warnungen, sobald in einem Projekt `npm install` gelaufen war. Gefunden bei der Erprobung am Testprojekt Bibliotheksverwaltung.

### Bekannte Einschränkungen
- Unverändert gegenüber 0.1.0: Kein Mechanismus wurde bislang in einer Zielinstallation von Devin Desktop ausgeführt (Validierung in Roadmap-AP2); die verify-Punkte bleiben offen.
- Im Framework-Repository sind `AGENTS.md`, `.devin/` und `project-overlay/` Erzeugnisse und nicht versioniert. Nach dem Klonen ist `python devin-core-framework/install.py` erforderlich, bevor der Validator läuft. In einem Projekt gilt das nicht — dort sind diese Pfade versionierter Projektbestand.
- `validate-framework.py --strict-overlay` ist im Framework-Repository erwartungsgemäß rot (neun Fehler), weil `project-overlay/` hier die Vorlage mit offenen Platzhaltern ist. Ohne das Flag: 0 Fehler, 0 Warnungen.

## [0.1.0] – 2026-09-01

### Hinzugefügt
- Erstfassung des gesamten Frameworks (Status aller Module: `entwurf`): Framework Core (FW-CORE-00…10), zentrale Agentenanweisung `AGENTS.md`, Devin-Laufzeitschicht `.devin/` (Regeln, Berechtigungen, Hooks, Subagent-Profil, MCP-Vorlage), Project-Overlay-Vorlage mit Manifest und Dokumentenmechanismus, Role-Pack-Struktur mit Referenzpack Softwareentwicklung, Technology-Pack-Struktur mit Vorlagen, Skill-Standard und Skill-Template, zwölf Referenz-Skills (FW-SK-001…012), Prompt-Bibliothek (FW-PR-001…012), elf Checklisten (FW-CL-01…11), sechs Entscheidungsbäume (FW-DT-01…06, Mermaid validiert), Onboarding-Paket (Quick-Start, Leitfaden, Mentor-Checkliste, Übungen, Wissenstest, Kriterien, Nachschlagewerk), Governance (RACI, Prioritätshierarchie, Release-, Änderungs-, Ausnahme-, Feedback-, Vorfallprozess, Decision Log), Testkatalog mit Validierungsskripten, Pilotkonzept mit Metriken, Adoption Guide, Roadmap (AP1–AP13), Beispiele (synthetisch), Platzhalterregister.

### Migrationshinweise
- Keine (Erstfassung). Projekte übernehmen über `devin-core-framework/docs/ADOPTION_GUIDE.md` und `devin-core-framework/checklists/10-project-adoption.md`.

### Bekannte Einschränkungen
- Kein Mechanismus wurde bislang in einer Zielinstallation von Devin Desktop ausgeführt; alle produktbezogenen Aussagen tragen Belegstatus (`[DOK]`/`[EMPF]`/`[KONZ]`) und offene Punkte den Marker `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>`. Validierung erfolgt in Roadmap-AP2.
- Zeichenlimits für Regeldateien unter Devin Local, exakte `config.json`-Schemadetails, Hook-Eingabeschema, Skill-Discovery über `.agents/skills/` und Codebasis-Indexierung sind zu verifizieren (Klärungspunkte K-18…K-20, Verifikationsliste im Hauptdokument).
- `devin-core-framework/tests/scripts/hook-check-secrets.py` läuft bis zur Validierung in AP2 standardmäßig fail-open (Umgebungsvariable `FW_HOOK_FAIL_CLOSED=1` aktiviert fail-closed).
- Technology Packs enthalten noch kein konkretes Pack (bewusst; entsteht projektbezogen in AP4).
