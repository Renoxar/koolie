# Änderungsverzeichnis (Framework)

Format: Semantic Versioning; je Release Änderungen, Migrationshinweise für Overlays und bekannte Einschränkungen. Prozess: `governance/RELEASE_PROCESS.md`.

## [0.1.0] – 2026-09-01

### Hinzugefügt
- Erstfassung des gesamten Frameworks (Status aller Module: `entwurf`): Framework Core (FW-CORE-00…10), zentrale Agentenanweisung `AGENTS.md`, Devin-Laufzeitschicht `.devin/` (Regeln, Berechtigungen, Hooks, Subagent-Profil, MCP-Vorlage), Project-Overlay-Vorlage mit Manifest und Dokumentenmechanismus, Role-Pack-Struktur mit Referenzpack Softwareentwicklung, Technology-Pack-Struktur mit Vorlagen, Skill-Standard und Skill-Template, zwölf Referenz-Skills (FW-SK-001…012), Prompt-Bibliothek (FW-PR-001…012), elf Checklisten (FW-CL-01…11), sechs Entscheidungsbäume (FW-DT-01…06, Mermaid validiert), Onboarding-Paket (Quick-Start, Leitfaden, Mentor-Checkliste, Übungen, Wissenstest, Kriterien, Nachschlagewerk), Governance (RACI, Prioritätshierarchie, Release-, Änderungs-, Ausnahme-, Feedback-, Vorfallprozess, Decision Log), Testkatalog mit Validierungsskripten, Pilotkonzept mit Metriken, Adoption Guide, Roadmap (AP1–AP13), Beispiele (synthetisch), Platzhalterregister.

### Migrationshinweise
- Keine (Erstfassung). Projekte übernehmen über `docs/ADOPTION_GUIDE.md` und `checklists/10-project-adoption.md`.

### Bekannte Einschränkungen
- Kein Mechanismus wurde bislang in einer Zielinstallation von Devin Desktop ausgeführt; alle produktbezogenen Aussagen tragen Belegstatus (`[DOK]`/`[EMPF]`/`[KONZ]`) und offene Punkte den Marker `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>`. Validierung erfolgt in Roadmap-AP2.
- Zeichenlimits für Regeldateien unter Devin Local, exakte `config.json`-Schemadetails, Hook-Eingabeschema, Skill-Discovery über `.agents/skills/` und Codebasis-Indexierung sind zu verifizieren (Klärungspunkte K-18…K-20, Verifikationsliste im Hauptdokument).
- `tests/scripts/hook-check-secrets.py` läuft bis zur Validierung in AP2 standardmäßig fail-open (Umgebungsvariable `FW_HOOK_FAIL_CLOSED=1` aktiviert fail-closed).
- Technology Packs enthalten noch kein konkretes Pack (bewusst; entsteht projektbezogen in AP4).
