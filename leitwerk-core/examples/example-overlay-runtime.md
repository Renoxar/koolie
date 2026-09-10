# Beispiel (synthetisch): ausgefüllte Overlay-Laufzeitfassung

> Synthetisches Beispiel für `20-project-overlay.md` in der Regelablage. Projekt, Pfade und Befehle sind erfunden („Bestellverwaltung", Kürzel `BSV`); sie bezeichnen kein reales Vorhaben. Frontmatter wie im Original (`trigger: always_on`).

```markdown
# Project Overlay – Laufzeitfassung für Bestellverwaltung (BSV)

## Status
- Overlay-Status: `aktiv`
- Overlay-Version: `0.1.0` · Framework-Version: siehe `leitwerk-core/VERSION`
- Overlay Owner (Rolle): Technische Projektleitung

## Arbeitsbereich
- Erlaubte Pfade: `src/**`, `test/**`, `docs/**`
- Ausgeschlossene Pfade: `deploy/**`, `config/env/**` – zusätzlich immer: Secret-Dateien, Laufzeitschicht, Wurzel-Anweisungsdatei, `project-overlay/`
- Testpfade: `test/**` · Dokumentationspfade: `docs/**`
- Als kritisch eingestufte Komponenten (mindestens Stufe hoch): `src/auth/**`, `src/export/**`

## Freigegebene Befehle
- Build: `build-tool compile` · Test: `build-tool test` · Lint: `build-tool lint`
- Weitere freigegebene Befehle: keine
- Alle anderen Befehle sind nicht freigegeben.

## Technik und Konventionen
- Technologie-Stack: Sprache X 21, Framework Y 3, Build-Tool Z · Testframework: Testframework T 5
- Coding Conventions: `project-overlay/documents/coding-guidelines/bsv-guidelines.md`
- Commit-Konvention: Typ + BSV-Ticketnummer + Kurzbeschreibung · Branching: Feature-Branches auf `main`
- Definition of Ready / Done: `project-overlay/documents/definition-of-ready/dor.md`, `.../definition-of-done/dod.md`

## Freigegebene Kontextquellen (Overlay-Manifest)
- K1: `bsv-guidelines.md`, `dor.md`, `dod.md`, `architektur-kurzfassung.md`
- K2 (nur nach Freigabe in der Aufgabe): `architektur-vollfassung.md`
- Freigegebene MCP-Server: keine
- Freigegebene externe Domains: keine

## Rollen und Eskalation (Rollen, keine Personen)
- Freigabe Stufe hoch: Technische Projektleitung · Sicherheit: Security-Rolle des Projekts · Datenschutz: Datenschutzkoordination
- Fachliche Klärung: Product Owner · Architektur: Softwarearchitektur

## Projektspezifische Verschärfungen
- Keine Änderungen an Datenbankmigrationen (`src/db/migrations/**`) durch den KI-Client – auch nicht auf Stufe hoch.

## Aktive projektspezifische Skills
- keine (Stand 0.1.0)
```

**Woran man ein gutes Overlay erkennt:** keine offenen `<TBD>` in den sicherheitsrelevanten Abschnitten, Rollen statt Personen, keine Hostnamen oder Adressen, Verschärfungen statt Lockerungen und eine kurze, immer ladbare Form (unter 6.000 Zeichen).
