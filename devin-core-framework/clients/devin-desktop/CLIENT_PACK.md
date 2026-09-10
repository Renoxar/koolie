# Client Pack `devin-desktop`

| Attribut | Wert |
|---|---|
| Modul-ID | `CP-DD` |
| Ebene | keine – Abbildungsschicht |
| Version | 0.2.0 |
| Status | entwurf |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Client | Devin Desktop (Devin Local) |
| Geprüfte Clientversion | `<TBD: verbindliche Zielversion; Roadmap AP2>` |
| Datum der Prüfung | `<TBD: steht aus>` |

> **Keine Einstufung dieses Packs ist gegen eine reale Installation belegt.** Die Spalte „Einstufung" nennt die **vorgesehene** Durchsetzungstiefe, die Spalte „Beleg" ihren Nachweisstand: `[DOK]` = in der Herstellerdokumentation beschrieben, `[EMPF]` = Empfehlung des Frameworks, VERIFY-Marker = gegen die aktuelle Dokumentation beziehungsweise eine Installation zu prüfen. Solange die Zielversion nicht festgelegt und geprüft ist (Roadmap AP2), gilt das Pack als **unbelegt**.

## 1. Pfadabbildung

| Rolle des Artefakts | Pfad bei diesem Client | Belegstatus |
|---|---|---|
| Wurzel-Anweisungsdatei | `AGENTS.md` | `[DOK]` |
| Regeldateien | `.devin/rules/*.md` mit `trigger`-Frontmatter | `[DOK]` |
| Skills | `.devin/skills/<name>/SKILL.md` | `[DOK]`; Alternativpfad `.agents/skills/` unbestätigt (K-12) |
| Subagentenprofile | `.devin/agents/<name>.md` | `[DOK]` |
| Berechtigungskonfiguration | `.devin/config.json` (erzeugt aus `framework/runtime/permissions.json`) | `[DOK]` Mechanismus; Schemadetails `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` |
| Hook-Konfiguration | `.devin/hooks.v1.json` (eigene Datei; erzeugt aus `framework/runtime/hooks.json`) | `[DOK]` Mechanismus; Eingabeschema `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` |
| MCP-Konfiguration | `.devin/mcp_config.json` (Vorlage: `.devin/mcp_config.json.example`) | Dateiname `[DOK]`; Struktur `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` |
| Projektverzeichnis-Variable in Hooks | `DEVIN_PROJECT_DIR` | `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` |
| Nutzerlokale Überschreibung | `AGENTS.local.md`, `.devin/config.local.json`, `*.local.md` neben Regeln | `[DOK]` |

Legacy: `.windsurf/` wird nicht gepflegt; `.devin/` hat Vorrang `[DOK]`.

## 1a. Semantikabbildung der Berechtigungen und Hooks

Die Regelmenge liegt werkzeugneutral im Kern (`devin-core-framework/framework/runtime/permissions.json`, `hooks.json`) und wird bei der Installation in die Werkzeuge dieses Clients übersetzt (D-18). Was dabei abgebildet wird, steht maschinenlesbar im `manifest.json`; diese Tabelle ist die menschenlesbare Fassung.

| Neutrales Werkzeugverb | Werkzeug bei diesem Client | Anmerkung |
|---|---|---|
| `read` | `Read(muster)` | |
| `search` | – | kein eigenes Suchwerkzeug; die `allow`-Regel entfällt und fällt damit auf den strengeren Standard zurück |
| `write` | `Write(muster)` | ein Werkzeug für Ändern und Anlegen |
| `exec` | `Exec(befehl)` | wörtliche Form; die Präfixform der Quelle wird nicht gebraucht |
| `fetch` | `Fetch(muster)` | |
| `mcp` | `mcp__*` | ohne Muster |

| Weitere Eigenschaft | Wert |
|---|---|
| Name ohne Verzeichnisanteil | ohne Wurzelangabe (`.env`) |
| Hook-Werkzeugnamen | `exec`, `edit`, `write` |
| Projektverzeichnis im Hook-Befehl | `$DEVIN_PROJECT_DIR` |

Die Abbildung ist kein freies Feld: Eine `deny`- oder `ask`-Regel, für die dieser Client kein Werkzeug kennt, lässt die Installation scheitern. Nur bei `allow` darf eine Regel entfallen – dort ist das Weglassen eine Verschärfung.

## 2. Fähigkeitsmatrix

### R – Regelladung

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| R1 | Wurzel-Anweisungsdatei wird ungefragt geladen | `AGENTS.md` wird als always-on-Regel in die Regel-Engine eingespeist | `[TECHNISCH]` | `[DOK]` |
| R2 | Regeldateien mit Ladebedingungen | Frontmatter `trigger`: `always_on`, `model_decision`, `manual`, `agent` | `[TECHNISCH]` | `[DOK]` |
| R3 | Regeln an Dateimuster bindbar | Frontmatter `trigger: glob` mit `globs` – Grundlage der Technology Packs | `[TECHNISCH]` | `[DOK]` |
| R4 | Bekanntes Zeichenlimit | 12.000 je Workspace-Regel, 6.000 global | `[TECHNISCH]` | `[DOK]` für Cascade; für Devin Local `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` (K-19) |

### S – Skills

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| S1 | Versionierte Skills im Repository | `.devin/skills/<name>/SKILL.md` mit Frontmatter | `[TECHNISCH]` | `[DOK]` |
| S2 | Gezielter Aufruf | Aufruf über den Skill-Namen mit vorangestelltem Schrägstrich | `[TECHNISCH]` | `[DOK]` |
| S3 | Werkzeugbeschränkung je Skill | Frontmatter `allowed-tools`, `permissions` | `[TECHNISCH]` | Wirkung additiver Skill-Permissions `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` |
| S4 | Schreibende Skills nur benutzergetriggert | Frontmatter `triggers` – Framework-Konvention, statisch geprüft durch `devin-core-framework/tests/scripts/validate-framework.py` | `[TEXTUELL]` | `[EMPF]`; die Laufzeitwirkung ist Modellverhalten |

### B – Berechtigungen

| ID | Zusage des Frameworks | Kern | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|---|
| B1 | Berechtigungen versioniert im Repository | ja | `.devin/config.json` | `[TECHNISCH]` | `[DOK]` |
| B2 | Verweigern vor Rückfragen vor Erlauben | ja | Zusammenführung über Ebenen | `[TECHNISCH]` | `[DOK]` |
| B3 | Secret-Dateien per Pfadmuster lesegeschützt | ja | Verweigerungsregeln auf `.env`, `**/*.pem`, `**/secrets/**` und weitere | `[TECHNISCH]` | Mechanismus `[DOK]`; Muster-Semantik `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` |
| B4 | Framework- und Overlay-Artefakte schreibgeschützt | ja | Verweigerungsregeln auf `AGENTS.md`, `.devin/`, `project-overlay/` | `[TECHNISCH]` | wie B3 |
| B5 | CI-, Quality-Gate- und Lockdateien schreibgeschützt | ja | Verweigerungsregeln auf Lockdateien und die Overlay-Platzhalterpfade | `[TECHNISCH]` | wie B3 |
| B6 | Befehle per Muster verweigerbar | ja | Verweigerungsregeln auf Push-, Merge-, Lösch- und Rechteausweitungsbefehle | `[TECHNISCH]` | wie B3 |
| B7 | Schreiboperationen fragen zurück | – | Rückfrageregel auf alle Schreiboperationen | `[TECHNISCH]` | `[DOK]` |
| B8 | Netzwerkzugriff standardmäßig unterbunden | – | Verweigerungsregeln auf Abruf- und Download-Werkzeuge | `[TECHNISCH]` | wie B3 |
| B9 | Nutzerlokale Konfiguration kann nur verschärfen | – | `.devin/config.local.json` – **Framework-Regel, keine Produkteigenschaft** | `[TEXTUELL]` | `[EMPF]`; ob der Client eine Lockerung technisch verhindert: `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` |

### H – Hooks

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| H1 | Prüfung vor Werkzeugausführung | `PreToolUse` mit Matcher auf schreibende und ausführende Werkzeuge | `[TECHNISCH]` | `[DOK]` Mechanismus |
| H2 | Prüfung kann **blockieren** | `hook-check-secrets.py` läuft derzeit fail-open; blockierend erst mit gesetzter Umgebungsvariable `FW_HOOK_FAIL_CLOSED` | `[TEXTUELL]` | Eingabeschema und Blockierverhalten `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` (V3) |
| H3 | Statusmeldung beim Sitzungsstart | `SessionStart` mit `hook-overlay-status.py` | `[TECHNISCH]` | `[DOK]` Mechanismus |

### A – Agentenprofile

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| A1 | Rein lesendes Reviewprofil | `.devin/agents/fw-reviewer.md` | `[TECHNISCH]` | `[DOK]`; Profilwirkung `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` |

### M – Modi und Sitzungsfreigaben

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| M1 | Standardmodus fragt bei Schreiben und Befehlen zurück | Modus `Normal` | `[TECHNISCH]` | `[DOK]` |
| M2 | Modus ohne Rückfragen ausschließbar | `Bypass` ist per D-05 untersagt; eine technische Sperre setzt Admin-Kontrollen der Planstufe voraus (K-05 offen) | `[TEXTUELL]` | `[EMPF]`; Verfügbarkeit der Sperre `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` |
| M3 | Freigabe auf die Sitzung begrenzbar | Sitzungsfreigaben „einmalig" und „für die Sitzung" | `[TECHNISCH]` | `[DOK]` |

### X – Externe Anbindung

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| X1 | Keine externe Anbindung ohne Einzelfreigabe | Keine MCP-Konfiguration ausgeliefert, nur die `.example`-Vorlage; Rückfrageregel auf alle MCP-Werkzeuge | `[TECHNISCH]` | `[DOK]` |
| X2 | Art und Ort der Codebasis-Indexierung bekannt | Kein Mechanismus zur Steuerung bekannt | `[NICHT ABBILDBAR]` | `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` (K-20) |

## 3. Zusammenfassung der Durchsetzungstiefe

| Klasse | Anzahl | davon Kernzusagen |
|---|---|---|
| `[TECHNISCH]` | 21 von 26 | 6 von 6 |
| `[TEXTUELL]` | 4 von 26 | 0 |
| `[NICHT ABBILDBAR]` | 1 von 26 | 0 |

**Belegstand:** 13 der 26 Zeilen tragen einen VERIFY-Marker. Keine Einstufung ist gegen eine Installation geprüft.

## 4. Kernzusagen ohne technische Durchsetzung

Alle sechs Kernzusagen (B1 bis B6) sind als `[TECHNISCH]` vorgesehen. Ein Eintrag in dieser Tabelle ist damit **derzeit nicht erforderlich** – unter dem Vorbehalt, dass die Prüfung nach Roadmap AP2 die Einstufung bestätigt.

Ergibt die Prüfung, dass eine der sechs Zusagen nicht technisch durchgesetzt wird, ist sie hier einzutragen und nach der Regel in `devin-core-framework/clients/README.md` Abschnitt 4 durch `<SECURITY_CONTACT>` freizugeben.

## 5. Bekannte Abweichungen im Verhalten

- **Der Schutz-Hook blockiert nicht.** `hook-check-secrets.py` läuft bis zum Abschluss von AP2 fail-open: Bei einem Fehler im Hook läuft die Werkzeugausführung weiter. Die Umstellung auf fail-closed setzt die Klärung des Eingabeschemas voraus. Bis dahin ist H2 eine Absichtserklärung, keine Schranke – die technische Durchsetzung von B3 ruht damit allein auf den Verweigerungsregeln der Berechtigungsdatei.
- **Zwei Skill-Ablagen dokumentiert.** `.devin/skills/` ist Primärpfad, `.agents/skills/` dokumentierte Alternative; welche der Client tatsächlich findet, ist unbestätigt (K-12).
- **Keine Workflows, keine Memories.** Beides wird vom Client nicht unterstützt `[DOK]`; Skills und versionierte Regeln übernehmen diese Funktion. Für ein Client Pack mit Memory-Mechanismus wäre zu klären, wie das Framework verhindert, dass Wissen an den versionierten Regeln vorbei entsteht.
- **Sandbox nicht auf allen Betriebssystemen.** Laut Dokumentation unter Windows nicht verfügbar (K-11); der Modus `Autonomous` ist damit dort nicht absicherbar.

## 6. Installation und Prüfung

```text
python devin-core-framework/install.py --client devin-desktop
python devin-core-framework/tests/scripts/validate-framework.py
```

Bis `install.py` den Schalter `--client` kennt, ist `devin-desktop` der eingebaute Standard und der Aufruf erfolgt ohne Schalter.

## 7. Änderungsverlauf

| Version | Datum | Änderung | Autor (Rolle) |
|---|---|---|---|
| 0.1.0 | 2026-09-10 | angelegt aus dem Ist-Zustand der Laufzeitschicht (`CR-2026-002`) | `<FRAMEWORK_OWNER>` |
| 0.2.0 | 2026-09-10 | Berechtigungen und Hooks aus dem Pack in den Kern; Semantikabbildung ergänzt (`CR-2026-008`) | `<FRAMEWORK_OWNER>` |
