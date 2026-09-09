# Übernahme des Frameworks in ein Projekt

| Attribut | Wert |
|---|---|
| ID | `FW-DOC-ADOPT` |
| Version | `0.1.0` |
| Status | `entwurf` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Checkliste | `checklists/10-project-adoption.md` (verbindlicher Nachweis) |

## 1. Grundprinzip

Das Framework wird als **Release-Archiv** in das Wurzelverzeichnis des Projekt-Repositorys integriert. Projektspezifisch sind ausschließlich: `project-overlay/` (Ebene 4), die Overlay-Laufzeitfassung `.devin/rules/20-project-overlay.md` (plus optionale `2N-overlay-*`), die ausgefüllten Werte in `.devin/config.json`, aktivierte Pack-Laufzeitfassungen (`30-*`, `40-*`), `prj-*`-Skills und die projektlokale `tests/forbidden-terms.txt`. Alles andere ist Core und bleibt byte-gleich zum Release – Änderungswünsche laufen als Änderungsantrag an den Framework Owner. Ein Projektwechsel tauscht nur die Overlay-Bestandteile; der Core bleibt unberührt (P10, Baum 6).

## 2. Neuaufnahme (Schrittfolge)

1. **Voraussetzungen der Organisation:** Werkzeugfreigabe, Datenschutz- und Vertragsprüfung, dokumentierte Team-Einstellungen (`framework/org-policies/`; Klärungspunkte K-05/K-06).
2. **Integration:** Release-Archiv in das Repository entpacken (`AGENTS.md`, `.devin/`, `framework/`, `project-overlay/`, `templates/`, `prompts/`, `checklists/`, `decision-trees/`, `onboarding/`, `tests/`, `docs/`, `governance/`, `OWNERS.md`, `VERSION`, `CHANGELOG.md`); bei Monorepos in das Wurzelverzeichnis des Workspace, den Devin öffnet (A-01).
3. **Overlay ausfüllen:** `project-overlay/OVERLAY.md` vollständig; Laufzeitfassung `20-project-overlay.md` synchron; Werte in `.devin/config.json` eintragen (Kernregeln unangetastet); Manifest und Dokumente einpflegen; Packs aktivieren.
4. **Projektlokale Härtung:** `tests/forbidden-terms.txt` mit realen Namen füllen (bleibt projektlokal); gegebenenfalls zusätzliche `deny`-Pfade.
5. **Validieren und testen:** `python3 tests/scripts/validate-framework.py --strict-overlay`; Basistests des Testkatalogs auf dem Übungsrepository; Übungsrepository für das Onboarding erzeugen (`onboarding/exercises/README.md`).
6. **Organisation im Projekt:** Rollen zuordnen (außerhalb des Repos), Eskalationskanäle, Ablageorte für Berichte und Pläne, Feedbackkanal.
7. **Aktivieren:** Checkliste 10 abschließen, Overlay-Status `aktiv`, Meldung an den Framework Owner (Bestandsliste).
8. **Menschen befähigen:** Onboarding vor produktiver Nutzung; Pilotparameter setzen, wenn das Projekt als Pilot läuft.

## 3. Aktualisierung auf ein neues Framework-Release

1. Release-Notes und Migrationshinweise lesen (`CHANGELOG.md` des Releases).
2. Core-Bestandteile durch die neuen ersetzen (byte-gleich); Overlay-Bestandteile bleiben, werden aber gegen die Migrationshinweise geprüft (neue Pflichtfelder, geänderte Platzhalter, deprecatete Skills).
3. Validator (`--strict-overlay`) und Basistests erneut ausführen; bei MAJOR-Releases zusätzlich FW-RE-01/02.
4. Overlay-Änderungsverlauf ergänzen (neue kompatible Framework-Version); Team über relevante Änderungen informieren; Onboarding-Materialstand prüfen.

## 4. Mehrere Repositories, ein Projekt

Je Repository, das Devin öffnet, liegt eine vollständige Framework-Integration (Root-Regeln wirken je Workspace). Das Overlay KANN geteilt gepflegt und je Repository ausgerollt werden (`<TBD: Ausrollmechanismus, z. B. Subtree oder Kopierskript>`); die Pfadlisten (Abschnitt 4 des Overlays) sind je Repository spezifisch.

## 5. Deinstallation oder Werkzeugwechsel

Deaktivierung: Overlay-Status `inaktiv` (Devin arbeitet nur noch lesend), danach Entfernen der `.devin/`-Laufzeitschicht, wenn gewünscht. Werkzeugwechsel: kanonische Ebene `framework/` bleibt; neue Laufzeitschicht analog `.devin/` aufbauen (P8; MAJOR-Release, `governance/RELEASE_PROCESS.md` Abschnitt 6.4).
