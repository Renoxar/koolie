# Framework für den professionellen Einsatz von Devin Desktop

Projektneutrales, wiederverwendbares Framework für den sicheren, kontrollierten und effizienten Einsatz von **Devin Desktop (ehemals Windsurf)** in Softwareentwicklungsteams – mit methodischem Vorgehensmodell und sofort nutzbarer technischer Referenzimplementierung. Erste Anwendung: strukturierte Einführung und Onboarding neuer Entwicklerinnen und Entwickler in einem bestehenden Projekt; Übertragung auf weitere Projekte über ein austauschbares Project Overlay.

**Version:** siehe `VERSION` · **Änderungen:** `CHANGELOG.md` · **Status:** Erstfassung, alle Module `entwurf` (Validierung in Roadmap-AP2) · **Owner:** `<FRAMEWORK_OWNER>` (`OWNERS.md`)

## Leitidee in drei Sätzen

Devin ist ein unterstützendes Werkzeug – Verantwortung, Prüfung und Freigabe bleiben bei Menschen. Kontext wird bewusst und minimal bereitgestellt (Klassen K0–K3), Aufgaben werden eingestuft (Kontrollstufen niedrig/mittel/hoch) und in definierten Betriebsmodi (M1–M5) bearbeitet. Alles Projektspezifische lebt im austauschbaren Overlay; der Kern bleibt bei Projektwechseln unverändert.

## Schnellzugriff nach Rolle

| Ich bin … | Startpunkt |
|---|---|
| neu im Team | `onboarding/QUICKSTART.md`, dann `onboarding/GUIDE.md` |
| Entwicklerin oder Entwickler im Alltag | `onboarding/REFERENCE.md` (Spickzettel), `checklists/01-preflight.md`, Skills unter `.devin/skills/` |
| Reviewerin oder Reviewer | `checklists/04-review-ai-code.md`, `framework/core/07-review-rules.md` |
| Overlay Owner / Projektleitung | `docs/ADOPTION_GUIDE.md`, `project-overlay/OVERLAY.md`, `checklists/10-project-adoption.md`, `pilot/` |
| Framework Owner | `governance/`, `tests/TEST_CATALOG.md`, `checklists/11-framework-release.md`, `docs/ROADMAP.md` |
| Sicherheit / Datenschutz | `framework/core/02-privacy.md`, `03-security.md`, `.devin/config.json`, `governance/INCIDENT_HANDLING.md` |

## Aufbau des Repositorys

```text
.
├── AGENTS.md                  # zentrale Agentenanweisung (always-on) – Kern der Laufzeitschicht
├── .devin/                    # Devin-Laufzeitschicht: rules/, skills/ (12 Referenz-Skills),
│                              # agents/, config.json (Berechtigungen), hooks.v1.json, README
├── framework/                 # kanonischer, werkzeugneutraler Kern
│   ├── core/                  # FW-CORE-00…10: Prinzipien, Governance, Datenschutz, Sicherheit,
│   │                          # Qualität, Arbeitsmodell, Prompting, Review, Skill-Standard,
│   │                          # Risikomodell, Fehler/Eskalation
│   ├── role-packs/            # Ebene 6 (Referenzpack Softwareentwicklung + Vorlage)
│   ├── tech-packs/            # Ebene 5 (Vorlagen; konkrete Packs entstehen je Projekt)
│   └── org-policies/          # Ebene 2: Einbindungspunkt für Organisationsvorgaben
├── project-overlay/           # Ebene 4: austauschbare Projektkonfiguration (Vorlage + Manifest)
├── templates/                 # Skill-, Plan-, MR-Vermerk-Vorlagen
├── prompts/                   # Prompt-Bibliothek FW-PR-001…012
├── checklists/                # FW-CL-01…11
├── decision-trees/            # FW-DT-01…06 (Text + validiertes Mermaid)
├── onboarding/                # Quick-Start, Leitfaden, Mentor-Checkliste, Übungen, Test, Kriterien
├── examples/                  # ausschließlich synthetische Beispiele
├── tests/                     # Testkatalog + Validierungs- und Hook-Skripte
├── governance/                # RACI, Hierarchie, Prozesse, Decision Log, Vorlagen
├── pilot/                     # Pilotkonzept und Metriken
├── docs/                      # Adoption Guide, Roadmap, Platzhalterregister
├── OWNERS.md · VERSION · CHANGELOG.md · AGENTS.local.md.example · .gitignore
```

## Erste Schritte

- **Als Projekt übernehmen:** `docs/ADOPTION_GUIDE.md` → Overlay ausfüllen → `python3 tests/scripts/validate-framework.py --strict-overlay` → `checklists/10-project-adoption.md` → Status `aktiv`.
- **Als Person starten:** Onboarding durchlaufen; ohne dokumentierte Freigabe nur begleitet arbeiten.
- **Framework prüfen:** `python3 tests/scripts/validate-framework.py` (Struktur), `--mermaid` (Diagramme), `tests/TEST_CATALOG.md` (Verhalten).

## Wichtige Konventionen

Verbindlichkeit über **MUSS/SOLL/KANN/DARF NICHT**; produktbezogene Aussagen tragen Belegstatus `[DOK]`/`[EMPF]`/`[KONZ]` oder den Marker `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>`; variable Inhalte ausschließlich als registrierte Platzhalter (`docs/PLACEHOLDER_REGISTRY.md`); Beispiele sind stets als synthetisch gekennzeichnet; Personen werden nirgends genannt – nur Rollen.
