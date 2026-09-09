# Änderungsverzeichnis (Framework)

Format: Semantic Versioning; je Release Änderungen, Migrationshinweise für Overlays und bekannte Einschränkungen. Prozess: `devin-core-framework/governance/RELEASE_PROCESS.md`.

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
