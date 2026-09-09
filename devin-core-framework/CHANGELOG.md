# Änderungsverzeichnis (Framework)

Format: Semantic Versioning; je Release Änderungen, Migrationshinweise für Overlays und bekannte Einschränkungen. Prozess: `devin-core-framework/governance/RELEASE_PROCESS.md`.

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
