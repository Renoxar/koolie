# 5 Begriffe und Glossar

| Begriff | Bedeutung im Framework |
|---|---|
| KI-Codierassistent | Sammelbegriff für das Werkzeug, das dieses Framework steuert. Welches Produkt konkret, legt das Client Pack fest |
| Client Pack | Abbildungsschicht für genau einen KI-Client: Pfadabbildung, Semantikabbildung und Fähigkeitsmatrix (Kap. 7a). Keine Regelebene |
| Fähigkeitsmatrix | Einstufung jeder technischen Zusage des Frameworks je Client: `[TECHNISCH]` erzwungen · `[TEXTUELL]` nur Anweisung · `[NICHT ABBILDBAR]`. Die Zeilenzahl ist je Pack verschieden – ein Client, der für eine Zusage keinen Mechanismus hat, bekommt dafür auch keine Zeile (Kap. 7a.3) |
| Kernzusage B1–B6 | Die sechs Zusagen, die dem Integritätsblock der Berechtigungsdatei entsprechen; eine Abweichung von `[TECHNISCH]` ist begründungs- und freigabepflichtig |
| `claude-code` · `devin-desktop` · `openai-codex` | Die drei ausgelieferten Client Packs. **Welches Produkt, welcher Agent und welche geprüfte Version dahinterstehen, nennt der Kopf des jeweiligen Packs** (Kap. 7a.3, 15.1) – dieser Kern nennt es nicht, weil er sich sonst mit dem Produkt änderte (D-02, D-129). In diesem Dokument ist `devin-desktop` das durchgehende Beispiel |
| Wurzel-Anweisungsdatei | zentrale Agentenanweisung im Wurzelverzeichnis; wird zu Beginn jeder Sitzung geladen `[DOK]`. Dateiname je Client Pack (Anhang 31.2) |
| Regel (Rule) | Markdown-Datei in der Regelablage mit Ladebedingung. Quellform: Frontmatter `description`, `trigger` (`always_on`, `model_decision`, `glob`, `manual`, `agent`) und bei `glob` zusätzlich `globs`. Die Ladebedingung wird bei der Installation auf die Bedingungssprache des Clients abgebildet (D-27); welche das ist, steht im Client Pack `[DOK]` |
| Skill | versionierte, testbare Arbeitsanweisung in der Skill-Ablage (`<name>/SKILL.md`); Aufruf `/name` `[DOK]`; Standard in Kap. 18 |
| Subagent | eigenständiges Agentenprofil für abgegrenzte Teilaufgaben `[DOK]`; im Framework nur das lesende Profil `fw-reviewer` |
| Hook | konfigurierter Eingriffspunkt im Agenten-Lebenszyklus (Hook-Konfiguration), kann Aktionen blockieren `[DOK]` |
| Permission-Modus | Bestätigungsverhalten des Clients; Framework-Standard ist der Modus, der bei Schreiben und Befehlen rückfragt. Bezeichnungen je Client (bei `devin-desktop`: Normal, Accept Edits, Smart, Bypass, Autonomous `[DOK]`) |
| Berechtigungsregeln | `deny`/`ask`/`allow`-Regeln in der Berechtigungsdatei; `deny` gewinnt immer `[DOK]`. Die Regelmenge liegt werkzeugneutral im Kern, die Werkzeugnamen entstehen aus der Semantikabbildung (Kap. 7a) |
| Sandbox | optionale Isolation der Befehlsausführung mit Pfad- und Domainfilter `[DOK]`; Verfügbarkeit betriebssystemabhängig |
| MCP | Model Context Protocol; Anbindung externer Werkzeuge/Server; im Framework nur nach Overlay-Freigabe, Standard `ask` `[DOK]` |
| Spaces / Agent Command Center | Desktop-Funktionen für geteilten Kontext beziehungsweise parallele Agenten `[DOK]`; im Framework restriktiv geregelt (Kap. 12) |
| Ebenen A–E | Trennungsmodell nach P10: A universelle Framework-Regeln, B Organisationsvorgaben, C Projektkonfiguration, D Rollen-/Technologieerweiterungen, E aufgabenbezogene flüchtige Informationen |
| Framework Core | Ebene 3 der Prioritätshierarchie; projektunabhängige Module FW-CORE-00…10 unter `.koolie/core/framework/core/` |
| Role Pack / Technology Pack | optionale rollen- beziehungsweise technologiebezogene Module (Ebenen 6 und 5) mit Laufzeitfassung `30-*` / `40-*` in der Regelablage |
| Project Overlay | einzige projektspezifische Ebene (4): `.koolie/project-overlay/` plus Laufzeitfassung `20-*` in der Regelablage; austauschbar ohne Core-Änderung |
| Overlay-Manifest | Register der für den Assistenten freigegebenen Projektdokumente (`overlay-manifest.yaml`) mit Klasse, Status, Ladeverhalten |
| Kontextklasse K0–K3 | Zulässigkeitsstufen für Inhalte an den Assistenten: frei / projektintern freigegeben / nur nach Freigabe und Bereinigung / nie (Kap. 11) |
| Kontrollstufe | Risikoklasse einer Aufgabe (niedrig/mittel/hoch) nach Faktoren R1–R13, Maximumprinzip (Kap. 13) |
| Delegationsverbotsliste V1–V12 | Aufgaben und Entscheidungen, die nie an den Assistenten delegiert werden (Kap. 13) |
| Betriebsmodus M1–M5 | Read-only Analysis, Guided Planning, Controlled Modification, Test and Validation, Documentation Support (Kap. 9) |
| Standardarbeitsablauf | die vierzehn Schritte jeder Assistenz-Aufgabe (Kap. 10) |
| Stop-Bedingungen S1–S10 / Eskalationsstufen E0–E4 | definierte Anhalte- und Eskalationspunkte (Kap. 10, 25; Baum 5) |
| Preflight | Pflichtprüfung vor jeder Assistenz-Aufgabe (Checkliste FW-CL-01) |
| Ergebnisbericht | Pflichtabschluss jeder Sitzung nach festem Format (Kap. 10) |
| KI-Nutzungsvermerk | Kennzeichnungsblock in Merge Requests (`.koolie/core/templates/MR_AI_DISCLOSURE.md`) |
| Quality Gate | bestehende Prüfschranke des Projekts (`<QUALITY_GATE>`); gilt für KI-Code unverändert (P6) |
| Merge Request | Änderungsvorschlag mit Review im Git-Prozess (plattformneutral; synonym Pull Request) |
| MUSS / SOLL / KANN / DARF NICHT | Verbindlichkeitsstufen des Frameworks (Kap. 6) |
| Belegstatus `[DOK]` / `[EMPF]` / `[KONZ]` | Kennzeichnung produktbezogener Aussagen: offiziell dokumentiert / begründete, noch nicht installationsgeprüfte Empfehlung / konzeptioneller Vorschlag |
| `BELEG OFFEN` | Belegstand einer Aussage, deren Nachweis noch aussteht; die Zelle nennt Grund und Datum. Trägt keine Frist |
| `<TBD: …>` | offene projekt- oder organisationsspezifische Entscheidung |
| Platzhalter | registrierte variable Bezeichner in spitzen Klammern (Anhang 31.3) |
| RACI | Verantwortungsmodell: Responsible, Accountable, Consulted, Informed (Kap. 25) |
| Decision Log | fortgeschriebenes Entscheidungs- und Klärungsregister (`.koolie/core/governance/DECISION_LOG.md`) |
| Übungsrepository | synthetisches Repository für Onboarding und Tests (Kap. 24, 26) |
| Köder | präparierte Negativübungs-Inhalte (Injektion, Pseudo-Secret, Scope-Falle) im Übungsrepository |
| Referenzbasis | Vor-Einführung-Vergleichswerte der Pilotmetriken (Kap. 27) |
| Synthetisches Beispiel | erfundenes, ausdrücklich gekennzeichnetes Beispiel ohne Bezug zu realen Projekten, Personen oder Systemen |
