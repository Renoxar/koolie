# Project Overlay – `<PROJECT_NAME>` (`<PROJECT_CODE>`)

<!-- AUSFÜLLHINWEISE (vor Aktivierung entfernen oder belassen – sie sind für Devin unschädlich):
     - Diese Datei ist die einzige Stelle für projektspezifische Vorgaben (Ebene 4). Der Framework Core
       wird nicht verändert. Ein Projektwechsel tauscht ausschließlich das Verzeichnis project-overlay/
       und die Laufzeitfassung <RULES_DIR>/20-project-overlay.md aus.
     - Jedes Feld enthält einen Platzhalter <...> oder einen Ausfüllhinweis. Offene Entscheidungen bleiben
       als <TBD: ...> stehen. Solange ein für Devin sicherheitsrelevantes Feld (Abschnitte 4, 5, 6, 13, 14, 15)
       offen ist, bleibt der Overlay-Status "inaktiv".
     - Keine Secrets, keine Personen, keine internen Adressen, keine nicht öffentlichen Fachinformationen.
       Rollen statt Personen. Beispiele sind als synthetisch zu kennzeichnen.
     - Das Overlay darf Framework-Regeln konkretisieren oder verschärfen, nie lockern
       (leitwerk-core/governance/PRIORITY_HIERARCHY.md).
     - Nach jeder Änderung: python3 leitwerk-core/tests/scripts/validate-framework.py ausführen und die Laufzeitfassung
       <RULES_DIR>/20-project-overlay.md synchron halten. -->

## 1. Projektsteckbrief

| Feld | Wert | Ausfüllhinweis |
|---|---|---|
| Projektname | `<PROJECT_NAME>` | neutraler Arbeitsname, kein Kunden- oder Behördenname |
| Projektkürzel | `<PROJECT_CODE>` | für Ticket-Referenzen und Skill-Präfixe |
| Overlay-Status | `<TBD: aktiv / inaktiv>` | `aktiv` erst nach Abschluss der Checkliste `leitwerk-core/checklists/10-project-adoption.md` |
| Overlay-Version | `<TBD: 0.1.0>` | Semantic Versioning, unabhängig von der Framework-Version |
| Kompatible Framework-Version | `<TBD: z. B. 0.1.x>` | aus `leitwerk-core/VERSION` des Frameworks |
| Overlay Owner (Rolle) | `<APPROVAL_ROLE>` | Rolle, keine Person |
| Fachlicher Kontext (abstrakt) | `<TBD: ein Satz ohne vertrauliche Details, z. B. „Fachanwendung zur Verwaltung von Anträgen">` | keine Fachinformationen mit Schutzbedarf |
| Teamgröße / Rollen im Team | `<TBD: Anzahl und generische Rollen>` | Entwickler, Reviewer, PO, RE, Tester, QA, Architekt, DevOps, Projektleitung |
| Freigabe der Devin-Nutzung durch Organisation | `<TBD: Referenz auf Freigabedokument oder „ausstehend">` | Voraussetzung für Status aktiv |
| Ergebnis Datenschutz- und Vertragsprüfung | `<TBD: Referenz oder „ausstehend">` | siehe `leitwerk-core/framework/core/02-privacy.md` Abschnitt 1 |
| Planstufe / verfügbare Admin-Kontrollen | `<TBD: Teams / Enterprise; erzwungene Einstellungen>` | Klärungspunkt K-05 |
| Nutzungsumfang | `<TBD: nur Devin Desktop lokal / zusätzlich Cloud-Sessions / CLI>` | Klärungspunkt K-04; Standard: nur Desktop lokal |
| Betriebssysteme der Arbeitsplätze | `<TBD>` | relevant für Sandbox-Verfügbarkeit (K-11) |

## 2. Technische Architektur (für Devin relevante Kurzfassung)

| Feld | Wert | Ausfüllhinweis |
|---|---|---|
| Architekturstil | `<TBD: z. B. modularer Monolith, Services, Schichtenarchitektur>` | ein Begriff, keine Systemnamen |
| Hauptkomponenten (logisch) | `<TBD: Liste logischer Komponenten mit Verzeichnis>` | keine Hostnamen, keine Umgebungen |
| Schichtung und erlaubte Abhängigkeitsrichtungen | `<TBD: z. B. UI → Anwendung → Domäne → Infrastruktur>` | Devin prüft Vorschläge dagegen |
| Kritische Komponenten (Änderung mindestens Stufe hoch) | `<TBD: Liste>` | Authentifizierung, Autorisierung, Zahlungs-/Fachkern, Schnittstellen zu Externen, Datenmigrationen |
| Externe Schnittstellen (abstrakt) | `<TBD: Typ und Richtung, z. B. „REST-Schnittstelle zu externem Fachverfahren (ausgehend)">` | keine Partnernamen, keine Adressen |
| Architekturvorgaben (Dokument) | `<TBD: Pfad im Overlay-Dokumentenverzeichnis, Kontextklasse>` | siehe Abschnitt 19 |
| Architekturentscheidungen (ADR-Ablage) | `<TBD: Pfad oder „nicht vorhanden">` | Devin liest ADRs nur lesend |

## 3. Repository-Struktur

```text
<REPOSITORY_NAME>/
├── <ROOT_INSTRUCTION_FILE>                      # Framework (nicht ändern)
├── <RUNTIME_DIR>/                        # Framework-Laufzeitschicht + Overlay-Laufzeitfassung
├── leitwerk-core/framework/                     # Framework Core, Packs (nicht ändern)
├── project-overlay/               # dieses Overlay
├── <TBD: src/>                    # Produktivcode – Beschreibung: <TBD>
├── <TBD: test/>                   # Tests – Beschreibung: <TBD>
├── <TBD: docs/>                   # Dokumentation – Beschreibung: <TBD>
├── <TBD: weitere Verzeichnisse>   # Beschreibung: <TBD>
└── <TBD: deploy/ infra/ config/>  # ausgeschlossen (siehe Abschnitt 4)
```

Ausfüllhinweis: Nur Verzeichnisse auf der obersten und gegebenenfalls zweiten Ebene beschreiben. Devin erschließt Details selbst (Skill `fw-repo-analyze`). Mehrere Repositories: je Repository ein Overlay oder ein Abschnitt je Repository mit eigenen Pfadlisten.

## 4. Erlaubte und ausgeschlossene Verzeichnisse

| Kategorie | Platzhalter | Wert | Ausfüllhinweis |
|---|---|---|---|
| Erlaubte Pfade (Lesen und Ändern in M3) | `<ALLOWED_PATHS>` | `<TBD: z. B. src/**, test/**, docs/**>` | Glob-Muster; alles Übrige ist nicht erlaubt |
| Testpfade (Ändern in M4) | `<TEST_PATHS>` | `<TBD>` | Teilmenge der erlaubten Pfade |
| Dokumentationspfade (Ändern in M5) | `<DOC_PATHS>` | `<TBD>` | Teilmenge der erlaubten Pfade |
| Ausgeschlossene Pfade (weder lesen noch ändern) | `<EXCLUDED_PATHS>` | `<TBD: z. B. deploy/**, infra/**, config/prod/**, **/fixtures/real/**>` | zusätzlich zu den festen Framework-Ausschlüssen (Secrets, `<RUNTIME_DIR>/`, `<ROOT_INSTRUCTION_FILE>`, `project-overlay/`, `leitwerk-core/framework/`) |
| Nur-Lese-Pfade (Lesen erlaubt, Ändern nie) | `<READ_ONLY_PATHS>` | `<TBD: z. B. api-contracts/**, db/migrations/**>` | Schnittstellenverträge, Migrationen, generierter Code |
| CI/CD-Konfiguration | `<CI_CONFIG_PATHS>` | `<TBD: z. B. .gitlab-ci.yml, .github/workflows/**, Jenkinsfile>` | wird in `<PERMISSIONS_FILE>` als `Write`-deny eingetragen |
| Quality-Gate-Konfiguration | `<QUALITY_GATE_CONFIG_PATHS>` | `<TBD: z. B. Linter-, Coverage-, Analyse-Konfigurationsdateien>` | `Write`-deny |

Diese Werte werden in `<PERMISSIONS_FILE>` und in `<RULES_DIR>/20-project-overlay.md` übernommen. Bei Widerspruch gilt die restriktivere Angabe.

## 5. Build-Befehle

| Zweck | Platzhalter | Befehl | Laufzeit / Hinweise |
|---|---|---|---|
| Vollständiger Build | `<BUILD_COMMAND>` | `<TBD>` | `<TBD: erwartete Dauer, benötigte lokale Voraussetzungen>` |
| Schneller Kompilier-/Syntaxcheck | – | `<TBD oder „nicht vorhanden">` | KANN für M3 freigegeben werden |
| Build-Voraussetzungen (lokal) | – | `<TBD: Werkzeuge und Versionen ohne interne Registry-Adressen>` | Registry-Adressen gehören nicht in das Overlay |

## 6. Test-, Prüf- und weitere freigegebene Befehle

| Zweck | Platzhalter | Befehl | Freigegeben für Modus | Freigabestufe in `<PERMISSIONS_FILE>` |
|---|---|---|---|---|
| Alle Unit-Tests | `<TEST_COMMAND>` | `<TBD>` | M3, M4 | ask (KANN für Stufe niedrig auf allow gesetzt werden – Entscheidung: `<TBD>`) |
| Einzelner Test / Testklasse | – | `<TBD: Befehlsmuster mit Platzhalter für Testname>` | M3, M4 | ask |
| Integrations-/Komponententests | – | `<TBD oder „nur in CI">` | `<TBD>` | ask |
| Linting / Formatprüfung | `<LINT_COMMAND>` | `<TBD>` | M3, M4, M5 | ask |
| Statische Codeanalyse (lokal) | – | `<TBD oder „nur in CI">` | M3 | ask |
| Weitere freigegebene Befehle | – | `<TBD: Liste oder „keine">` | `<TBD>` | ask |

Alle nicht gelisteten Befehle sind nicht freigegeben. Befehle mit Fernwirkung (Push, Merge, Deployment, Veröffentlichung) werden hier nie gelistet.

## 7. Qualitätsprüfungen (Quality Gates)

| Prüfung | Werkzeugklasse | Wo | Verbindlich für Devin-Änderungen | Ausfüllhinweis |
|---|---|---|---|---|
| Build | `<CI_CD_PLATFORM>` | lokal + CI | MUSS | – |
| Linting / Formatierung | `<TBD>` | lokal + CI | MUSS | Konfigurationspfad in Abschnitt 4 |
| Statische Codeanalyse | `<TBD>` | CI | MUSS, falls vorhanden | – |
| Unit Tests | `<TEST_FRAMEWORK>` | lokal + CI | MUSS | Mindestabdeckung: `<TBD oder „nicht definiert">` |
| Integrations-/Komponententests | `<TBD>` | CI | `<TBD>` | – |
| Security Scan (Abhängigkeiten, Code) | `<TBD>` | CI | MUSS, falls vorhanden | – |
| Quality Gate | `<QUALITY_GATE>` | CI | MUSS | Schwellenwerte werden von Devin nie geändert |
| Merge Request + Code Review | `<TBD: Plattform>` | Prozess | MUSS | Anzahl Reviewer: `<TBD>` |
| Vier-Augen-Prinzip | Prozess | Prozess | MUSS ab Kontrollstufe mittel | projektspezifisch: `<TBD>` |
| Fachliche Abnahme | Prozess | Prozess | `<TBD>` | – |

## 8. Programmiersprachen und Frameworks

| Element | Wert | Ausfüllhinweis |
|---|---|---|
| Technologie-Stack | `<TECH_STACK>` | Sprache(n) und Versionen, Hauptframeworks, Build-System |
| Testframework | `<TEST_FRAMEWORK>` | inklusive Mocking-/Assertion-Bibliotheken |
| Aktivierte Technology Packs | `<TBD: Liste, z. B. tech-<name> Version>` | jeweils Laufzeitfassung `<RULES_DIR>/40-tech-<name>.md` |
| Erlaubte Paketquellen | `<TBD: „nur Artefakt-Repository der Organisation" – ohne Adresse>` | Adresse gehört nicht in das Overlay |
| Abhängigkeitsverwaltung | `<TBD: Manifest- und Lockdatei>` | Änderungen nur durch den Menschen |

## 9. Coding Conventions

| Element | Wert | Ausfüllhinweis |
|---|---|---|
| Verbindliches Convention-Dokument | `<PROJECT_RULES_PATH>` | im Overlay-Dokumentenverzeichnis, Kontextklasse K1 |
| Formatter / Linter als Quelle der Wahrheit | `<TBD>` | Devin folgt der Konfiguration, nicht Erinnerungen |
| Benennungskonventionen (Kurzfassung) | `<TBD>` | maximal zehn Zeilen; Rest im Dokument |
| Verbotene Muster | `<TBD>` | z. B. bestimmte Bibliotheken, Reflection, statische Zustände |
| Sprache von Bezeichnern, Kommentaren, Commits | `<TBD>` | – |

## 10. Branching- und Merge-Modell

| Element | Platzhalter | Wert |
|---|---|---|
| Branching-Modell | `<BRANCHING_MODEL>` | `<TBD: z. B. Feature-Branches auf Standard-Branch, Release-Branches>` |
| Standard-Branch | `<DEFAULT_BRANCH>` | `<TBD>` |
| Branch-Namensschema | `<BRANCH_PREFIX>` | `<TBD: z. B. feature/<PROJECT_CODE>-<ticket>-kurzbeschreibung>` |
| Commit-Konvention | `<COMMIT_CONVENTION>` | `<TBD: z. B. Conventional Commits mit Ticket-Referenz>` |
| Merge-Strategie | – | `<TBD: Squash / Merge-Commit / Rebase – durch Menschen>` |
| Merge-Request-Vorlage | `<MR_TEMPLATE_PATH>` | `<TBD>`; enthält den KI-Nutzungsvermerk (`leitwerk-core/templates/MR_AI_DISCLOSURE.md`) |
| Geschützte Branches | – | `<TBD>`; Devin arbeitet nie direkt darauf |

## 11. Definition of Ready (für Devin-Aufgaben)

Eine Aufgabe ist bereit für die Bearbeitung mit Devin, wenn zusätzlich zur projektweiten Definition of Ready (`<TBD: Pfad>`):

1. Ziel und Akzeptanzkriterien schriftlich vorliegen (bereinigt, ohne K2/K3-Inhalte),
2. Kontrollstufe und Betriebsmodus festgelegt sind,
3. der Scope (Pfade) benannt ist,
4. die benötigten Kontextquellen eingestuft und – bei K2 – freigegeben sind,
5. `<TBD: projektspezifische Zusatzkriterien>`.

## 12. Definition of Done (für Devin-Aufgaben)

Zusätzlich zur projektweiten Definition of Done (`<TBD: Pfad>`) gilt `leitwerk-core/framework/core/04-quality.md` Abschnitt 3 (Ergebnisbericht, lokale Prüfungen, Selbstreview, Nutzungsvermerk, offene Punkte sichtbar). Projektspezifische Ergänzungen: `<TBD>`.

## 13. Zulässige Kontexte und Werkzeuge

| Kontextquelle | Kontextklasse | Freigabe | Bedingungen |
|---|---|---|---|
| Quellcode in `<ALLOWED_PATHS>` | K1 | pauschal | Least Context |
| Quellcode in `<READ_ONLY_PATHS>` | K1 | pauschal (lesend) | – |
| Overlay-Dokumente laut Manifest (Abschnitt 19) | K1 / K2 je Dokument | laut Manifest | K2 nur mit Freigabe in der Aufgabe |
| Tickets aus `<ISSUE_TRACKER>` | K2 | je Aufgabe durch Bearbeiterin oder Bearbeiter | nur Titel, technische Beschreibung, Akzeptanzkriterien; bereinigt |
| Inhalte aus `<DOCUMENTATION_PLATFORM>` | `<TBD: K1 nach Freigabe je Seite / K2>` | `<TBD>` | – |
| Logauszüge, Stacktraces | K2 | je Aufgabe | bereinigt (keine personenbezogenen Daten, Hostnamen, Kennungen) |
| Testdaten | K1 nur synthetisch | pauschal für synthetische Daten | Echtdaten nie |
| Freigegebene MCP-Server | – | `<TBD: Liste mit Zweck und Berechtigungsumfang oder „keine">` | Eintrag in `<MCP_FILE>` erst nach Freigabe; Standard ask |
| Freigegebene externe Domains (Fetch) | K0 | `<TBD: Liste oder „keine">` | `Fetch(domain:...)`-Regeln in `<PERMISSIONS_FILE>` |
| Cloud-Sessions / CLI / ACP-Fremdagenten | – | `<TBD: nicht freigegeben / freigegeben mit Auflagen>` | Standard: nicht freigegeben (D-10) |

## 14. Ausgeschlossene Daten (projektspezifische Ergänzung zu K3)

Zusätzlich zu den festen K3-Kategorien (`leitwerk-core/framework/core/02-privacy.md` Abschnitt 2.1):

| Ausgeschlossen | Wo typischerweise anzutreffen | Technische Sperre |
|---|---|---|
| `<TBD: z. B. Fachdaten realer Vorgänge>` | `<TBD: Verzeichnisse>` | `Read`-deny in `<PERMISSIONS_FILE>` |
| `<TBD: z. B. Umgebungskonfigurationen>` | `<TBD>` | `<EXCLUDED_PATHS>` |
| `<TBD: z. B. Schnittstellenverträge externer Partner mit Vertraulichkeitsvermerk>` | `<TBD>` | Overlay-Manifest: nicht gelistet = K3 |

## 15. Rollen und Freigaben

| Rolle (generisch) | Platzhalter | Zuständigkeit im Devin-Kontext |
|---|---|---|
| Freigabe Kontrollstufe hoch, Overlay Owner | `<APPROVAL_ROLE>` | schriftliche Freigaben, Overlay-Pflege, Ausnahmen |
| Sicherheitskontakt | `<SECURITY_CONTACT>` | Sicherheitsfreigaben, Vorfälle, Abhängigkeiten |
| Datenschutzkontakt | `<DATA_PROTECTION_CONTACT>` | Kontextfreigaben K2 mit Personenbezug, Vorfälle |
| Product Owner | `<PRODUCT_OWNER_ROLE>` | fachliche Klärungen, Akzeptanzkriterien |
| Softwarearchitektur | `<ARCHITECT_ROLE>` | Architekturentscheidungen, Review Stufe hoch |
| Reviewerinnen und Reviewer | – | Review nach `leitwerk-core/framework/core/07-review-rules.md` |
| Mentorinnen und Mentoren | – | Onboarding, Freigabe zur selbstständigen Nutzung |
| Modul-Owner projektspezifischer Skills | – | Pflege der `prj-*`-Skills |

Ausfüllhinweis: Rollen bleiben generisch. Die Zuordnung zu Personen erfolgt außerhalb des Repositorys (zum Beispiel im Teamverzeichnis der Organisation).

## 16. Eskalationsweg

| Stufe (aus `leitwerk-core/framework/core/10-error-escalation.md`) | Erreichbar über | Reaktionszeit (projektspezifisch) |
|---|---|---|
| E1 fachlich/technisch | `<PRODUCT_OWNER_ROLE>` / `<ARCHITECT_ROLE>` über `<TBD: Kanal, z. B. Ticket-Kommentar, Team-Chat>` | `<TBD>` |
| E2 Freigabe Stufe hoch | `<APPROVAL_ROLE>` über `<TBD>` | `<TBD>` |
| E3 Sicherheits-/Datenschutzvorfall | `<SECURITY_CONTACT>`, `<DATA_PROTECTION_CONTACT>` über den Meldeweg der Organisation `<TBD: Referenz>` | gemäß Organisation |
| E4 Framework-Mangel | `<FRAMEWORK_OWNER>` über `leitwerk-core/governance/FEEDBACK_PROCESS.md` | `<TBD>` |

## 17. Projektspezifische Skills

| Skill | ID | Status | Owner (Rolle) | Zweck | Ersetzt/ergänzt Framework-Skill |
|---|---|---|---|---|---|
| `prj-<TBD>` | `PRJ-SK-001` | entwurf | `<TBD>` | `<TBD>` | `<TBD: keiner / fw-...>` |

Regeln: Projekt-Skills folgen dem Skill-Standard (`leitwerk-core/framework/core/08-skill-conventions.md`), tragen das Präfix `prj-`, liegen unter `<SKILLS_DIR>/prj-<name>/` und DÜRFEN Framework-Skills ergänzen, aber deren Prüfschritte nicht entfernen.

## 18. Dokumentierte Ausnahmen

| ID | Ausnahme von Regel | Begründung | Kompensierende Maßnahme | Freigegeben durch (Rolle) | Gültig bis | Status |
|---|---|---|---|---|---|---|
| `EX-<PROJECT_CODE>-001` | `<TBD>` | `<TBD>` | `<TBD>` | `<APPROVAL_ROLE>` | `<TBD: Datum oder Ereignis>` | `<TBD>` |

Ausnahmen folgen `leitwerk-core/governance/EXCEPTION_PROCESS.md`. Ausnahmen von Delegationsverboten (V1–V12) und von der K3-Definition sind nicht zulässig.

## 19. Eingebundene Projektdokumente (Overlay-Erweiterung)

Projektspezifisches Wissen wird ausschließlich über diesen Mechanismus eingebunden; der Framework Core bleibt unverändert.

**Mechanismus (normativ):**

1. Das Dokument (oder ein bereinigter Auszug) wird unter `project-overlay/documents/<dokumenttyp>/` abgelegt oder – falls es außerhalb des Repositorys bleibt – dort mit einem Verweisblatt (`REFERENCE.md`) beschrieben.
2. Das Dokument wird in `project-overlay/overlay-manifest.yaml` registriert: Typ, Pfad, Kontextklasse, Status, Freigabe (Rolle, Datum), Ladeverhalten.
3. Ladeverhalten:
   - `summary`: Kernaussagen (maximal zehn Zeilen) werden in `<RULES_DIR>/20-project-overlay.md` übernommen (immer aktiv, nur K1).
   - `on-demand`: Devin liest das Dokument, wenn die Aufgabe es erfordert; K2-Dokumente nur nach Freigabe in der Aufgabe.
   - `rule`: Das Projekt legt eine zusätzliche Overlay-Regeldatei `<RULES_DIR>/2N-overlay-<name>.md` (N = 1–9) mit `trigger: model_decision` oder `glob` an, die die Kernregeln des Dokuments enthält und auf das Dokument verweist (unter 12.000 Zeichen).
   - `never`: Das Dokument ist registriert, aber nicht für Devin bestimmt (Nachweiszweck).
4. Nicht registrierte Dokumente gelten als K3.
5. Änderungen an Dokumenten erhöhen die Overlay-Version; veraltete Dokumente werden im Manifest als `veraltet` markiert und nicht mehr geladen.

**Vorgesehene Dokumenttypen:**

| Typ (Manifest-Schlüssel) | Dokument | Empfohlenes Ladeverhalten | Typische Kontextklasse |
|---|---|---|---|
| `ai-governance` | KI-Governance-Rahmenwerk der Organisation oder des Projekts | `rule` (Kernregeln) | K1 |
| `ai-process-model` | KI-Vorgehensmodell | `on-demand` | K1 |
| `roadmap` | Projektroadmap | `never` oder `on-demand` (bereinigt) | K2 |
| `architecture` | Architekturvorgaben | `rule` + `on-demand` | K1 nach Entfernung von Infrastrukturdetails, sonst K2 |
| `coding-guidelines` | Coding Guidelines | `rule` (`glob`) | K1 |
| `definition-of-ready` | Definition of Ready | `summary` | K1 |
| `definition-of-done` | Definition of Done | `summary` | K1 |
| `branching-strategy` | Branching-Strategie | `summary` | K1 |
| `deployment` | Deployment-Vorgaben | `never` (Devin deployt nicht) oder `on-demand` (bereinigt) | K2 |
| `security` | Security-Vorgaben | `rule` (nur Entwicklungsregeln) | K1 nach Bereinigung; Schutzkonfigurationen K3 |
| `quality` | Qualitätsrichtlinien | `rule` | K1 |
| `roles` | Rollenbeschreibungen | `summary` (Rollen, keine Personen) | K1 |
| `glossary` | Projektglossar | `on-demand` | K1 nach Prüfung auf vertrauliche Fachbegriffe |

## 20. Änderungsverlauf des Overlays

| Version | Datum | Änderung | Autor (Rolle) | Validierung bestanden |
|---|---|---|---|---|
| `<TBD: 0.1.0>` | `<TBD>` | Overlay angelegt | `<APPROVAL_ROLE>` | `<TBD>` |

## 21. Aktivierung

Der Status wird erst auf `aktiv` gesetzt, wenn `leitwerk-core/checklists/10-project-adoption.md` vollständig abgearbeitet ist und `python3 leitwerk-core/tests/scripts/validate-framework.py --strict-overlay` ohne Befund durchläuft.
