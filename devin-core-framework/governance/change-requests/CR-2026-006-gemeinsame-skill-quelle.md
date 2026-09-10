# Änderungsantrag `CR-2026-006`

| Feld | Inhalt |
|---|---|
| Titel | Gemeinsame Skill-Quelle mit Rendering je Client Pack |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | neu: `devin-core-framework/framework/skills/`; entfernt: `clients/*/root-template/**/skills/`; geändert: `install.py`, `tests/scripts/validate-framework.py`, `clients/*/manifest.json`, `docs/PLACEHOLDER_REGISTRY.md` |
| Ebene laut Entscheidungsbaum 6 | Core (Struktur) |
| Art | Änderung |
| Dringlichkeit | regulär (Review-Zyklus) |

## 1. Anlass und Problem

Mit dem zweiten Client Pack lagen die zwölf `fw-*`-Skills doppelt im Kern – einmal je Pack, 48 Dateien jeweils. `CR-2026-004` hat das als bekannte Einschränkung festgehalten, `CR-2026-005` die Datengrundlage geliefert:

| Größe | Wert |
|---|---|
| Zeilen gesamt | 3.003 |
| Abweichende Zeilen | 215 (7,2 %) |
| davon Frontmatter | 147 |
| davon Pfadnennungen im Rumpf | 68 |

**92,8 Prozent identisch.** Ein neuer Skill hätte zweimal geschrieben, jede Korrektur zweimal nachgezogen werden müssen – mit der üblichen Folge, dass die Fassungen auseinanderlaufen, ohne dass es jemand bemerkt.

Der Ort war zudem falsch gewählt: **Ein Skill ist Framework-Inhalt – Ebene 7 der Prioritätshierarchie.** Nur seine Frontmatter-*Form* ist clientspezifisch. Dass die Skills im Client Pack lagen, war ein Erbe daraus, dass `root-template/` ursprünglich alles enthielt.

## 2. Vorgeschlagene Änderung

**Die Skills liegen einmal** unter `devin-core-framework/framework/skills/` (48 Dateien) und werden bei der Installation in die Form des gewählten Clients gebracht.

**Quellformat ist die reichere Listenform** (`allowed-tools` als Liste, dazu `permissions` und `triggers`). Sie trägt mehr Information als die kommagetrennte Form und lässt sich verlustfrei in diese überführen – umgekehrt nicht.

**Zwei Transformationen beim Rendern:**

1. **Frontmatter** nach `skill_frontmatter` im Manifest: `tools_format` (`list` oder `csv`), `tool_names` (Werkzeugabbildung, etwa `edit` → `Edit, Write`), `drop_fields` (Felder, die dieser Client nicht kennt – K-18).
2. **Laufzeit-Platzhalter** nach `runtime_placeholders` im Manifest. Neun neue registrierte Platzhalter (`<RUNTIME_DIR>`, `<ROOT_INSTRUCTION_FILE>`, `<PERMISSIONS_FILE>`, `<SKILLS_DIR>`, `<RULES_DIR>`, `<AGENTS_DIR>`, `<HOOKS_FILE>`, `<MCP_FILE>`, `<ROOT_INSTRUCTION_LOCAL>`) ersetzen die 17 Pfadnennungen in den Skill-Rümpfen.

Sie unterscheiden sich von allen bisherigen Platzhaltern: **Nicht der Mensch füllt sie, sondern `install.py`.** Das ist die gerenderte Entsprechung zu den Begriffen aus D-15 – Fließtext nennt den Begriff, ein Quelltext, der gerendert wird, den Platzhalter.

**Der Validator prüft beide Enden:** die Quelle unter `framework/skills/` streng nach Skill-Standard, und die installierte Laufzeitschicht darauf, dass kein Laufzeit-Platzhalter unaufgelöst geblieben ist. Letzteres deckt ein Client Pack auf, dessen Manifest einen Platzhalter nicht belegt.

## 3. Prüffragen (durch Owner auszufüllen)

- [x] Richtige Ebene nach Entscheidungsbaum 6? — Ja, und die Änderung korrigiert eine falsche Zuordnung: Ein Skill ist Ebene 7 (Framework), kein Bestandteil der Client-Abbildung.
- [x] Verschärfungsprinzip eingehalten? — Ja. Kein Skill-Inhalt wurde geändert. Nachgewiesen durch unveränderte Installationsumfänge und einen Vergleich der gerenderten Fassungen mit den bisherigen.
- [x] Widerspruchsfreiheit geprüft? — `framework/core/08-skill-conventions.md` nennt seit `CR-2026-005` die Skill-Ablage als Begriff; die Quelle liegt nun folgerichtig im werkzeugneutralen Kern. Das Nummern- und Präfixschema (`fw-`, `role-`, `tech-`, `prj-`) bleibt unverändert.
- [x] Laufzeitfassungen betroffen? — Nur ihr Ursprung. Installationsumfang unverändert: 80 Dateien (`devin-desktop`), 79 (`claude-code`).
- [x] Belegstatus korrekt? — Unverändert.
- [x] Test- und Validierungsbedarf? — Siehe Abschnitt 5. Neu: Prüfung auf unaufgelöste Laufzeit-Platzhalter, mit Wirksamkeitsnachweis.
- [x] Auswirkungen auf Overlays und laufende Onboardings? — Keine. Projektspezifische `prj-*`-Skills bleiben unberührt; sie liegen weiterhin allein in der Laufzeitschicht des Projekts und werden von `install.py` nie angefasst.
- [x] Dokumentation? — Platzhalterregister (neuer Abschnitt für Laufzeit-Platzhalter), CHANGELOG, Decision Log.

## 4. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | angenommen |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Die doppelte Pflege war die einzige Stelle, an der ein weiteres Client Pack echten Zusatzaufwand erzeugt hätte. Sie ist beseitigt, ohne dass ein Skill-Inhalt sich ändert. Die dafür gebaute Infrastruktur – Renderer und Laufzeit-Platzhalter – trägt auch die übrigen Artefakte, deren Inhalt Framework und deren Form Client ist. |
| Ziel-Release | 0.5.0 |
| Decision-Log-Eintrag | D-16 |

## 5. Umsetzung (nach Annahme)

- [x] 48 Dateien nach `framework/skills/` verschoben; 17 Pfadnennungen durch Laufzeit-Platzhalter ersetzt (Restprüfung: 0 verbliebene Client-Pfade)
- [x] Manifeste um `runtime_placeholders` und `skill_frontmatter` erweitert
- [x] `install.py`: `resolve_placeholders`, `render_skill_frontmatter`, `framework_skill_files`, `write_rendered`, `rendered_matches`
- [x] Skill-Verzeichnisse aus beiden `root-template/` entfernt
- [x] Validator: Quelle als Skill-Ablage geprüft; neue Prüfung `check_runtime_placeholders`
- [x] Platzhalterregister um den Abschnitt „Laufzeit-Platzhalter" erweitert
- [x] Erstinstallation unverändert: 80 / 79 Dateien; `--check` gegen beide fehlerfrei
- [x] Drift-Erkennung an einem gerenderten Skill: Exit 1 mit Nennung der gemeinsamen Quelle; `--update` stellt her
- [x] Wirksamkeitsnachweis: `<HOOKS_FILE>` testweise aus einem Manifest entfernt → drei gemeldete Fehler wegen unaufgelöster Platzhalter; Manifest wiederhergestellt
- [x] Validator gegen beide Installationen und gegen das Übungsrepository mit neuem Kern: je 0 Fehler
- [x] CHANGELOG und Decision Log ergänzt
- [ ] Folgearbeit: `project-overlay/` und die beiden Pack-Vorlagen aus den Client Packs herauslösen (18 byteweise identische Dateien); Regeltexte, Wurzel-Anweisung, Agentenprofil und Berechtigungsdatei über denselben Renderer führen
