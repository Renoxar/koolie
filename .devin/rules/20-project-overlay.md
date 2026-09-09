---
description: Projektspezifische Laufzeitfassung des Project Overlays (Ebene 4). Immer aktiv. Wird vom Projekt aus project-overlay/OVERLAY.md gepflegt; darf keine Framework-Regeln lockern.
trigger: always_on
---

# Project Overlay – Laufzeitfassung für `<PROJECT_NAME>`

<!-- AUSFÜLLHINWEIS: Diese Datei ist die kompakte, immer geladene Fassung des Overlays.
     Quelle und Detailfassung: project-overlay/OVERLAY.md. Beide Dateien werden gemeinsam
     versioniert. Halte diese Datei unter 6.000 Zeichen. Trage nur Werte ein, die durch den
     Overlay Owner freigegeben sind. Offene Werte bleiben als <TBD: …> stehen; Devin behandelt
     offene Werte als nicht freigegeben. Keine Secrets, keine Personen, keine internen Adressen. -->

## Status

- Overlay-Status: `<TBD: aktiv | inaktiv>` (bei `inaktiv` oder fehlendem Eintrag arbeitet Devin nur lesend)
- Overlay-Version: `<TBD: Version>` · Framework-Version: siehe `VERSION`
- Overlay Owner (Rolle): `<APPROVAL_ROLE>`

## Arbeitsbereich

- Erlaubte Pfade (`<ALLOWED_PATHS>`): `<TBD: Liste, zum Beispiel src/**, test/**, docs/**>`
- Ausgeschlossene Pfade (`<EXCLUDED_PATHS>`): `<TBD: Liste, zum Beispiel deploy/**, infra/**, config/prod/**>` – zusätzlich immer: Secret-Dateien, `.devin/`, `AGENTS.md`, `project-overlay/`
- Testpfade (`<TEST_PATHS>`): `<TBD>` · Dokumentationspfade (`<DOC_PATHS>`): `<TBD>`
- Als kritisch eingestufte Komponenten (Änderungen mindestens Kontrollstufe hoch): `<TBD: Liste>`

## Freigegebene Befehle

- Build: `<BUILD_COMMAND>` · Test: `<TEST_COMMAND>` · Lint/Statische Analyse: `<LINT_COMMAND>`
- Weitere freigegebene Befehle: `<TBD: Liste oder „keine">`
- Alle anderen Befehle sind nicht freigegeben.

## Technik und Konventionen

- Technologie-Stack: `<TECH_STACK>` · Testframework: `<TEST_FRAMEWORK>`
- Coding Conventions: `<PROJECT_RULES_PATH>` (nur die dort referenzierten Dokumente sind verbindlich)
- Commit-Konvention: `<COMMIT_CONVENTION>` · Branching: `<BRANCHING_MODEL>` · Standard-Branch: `<DEFAULT_BRANCH>`
- Definition of Ready / Definition of Done: `<TBD: Pfad im Overlay-Dokumentenverzeichnis>`

## Freigegebene Kontextquellen (Overlay-Manifest)

- Dokumente der Klasse K1 (frei nutzbar): `<TBD: Liste aus project-overlay/overlay-manifest.yaml>`
- Dokumente der Klasse K2 (nur nach Freigabe in der Aufgabe): `<TBD: Liste>`
- Freigegebene MCP-Server: `<TBD: Liste oder „keine">`
- Freigegebene externe Domains: `<TBD: Liste oder „keine">`

## Rollen und Eskalation (Rollen, keine Personen)

- Freigabe Kontrollstufe hoch: `<APPROVAL_ROLE>` · Sicherheit: `<SECURITY_CONTACT>` · Datenschutz: `<DATA_PROTECTION_CONTACT>`
- Fachliche Klärung: `<PRODUCT_OWNER_ROLE>` · Architektur: `<ARCHITECT_ROLE>`
- Devin nennt bei Eskalation immer die Rolle, nie eine Person.

## Projektspezifische Verschärfungen

`<TBD: zusätzliche Verbote oder Verschärfungen, zum Beispiel „keine Änderungen an Datenbankmigrationen durch Devin">`

## Aktive projektspezifische Skills

`<TBD: Liste der prj-*-Skills mit Status>`
