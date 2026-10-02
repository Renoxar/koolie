# Role Pack Softwareentwicklung

| Attribut | Wert |
|---|---|
| Modul-ID | RP-DEV |
| Ebene | 6 – Role Pack |
| Version | 0.1.2 |
| Status | pilot (Referenzpack der Erstfassung) |
| Owner | `<FRAMEWORK_OWNER>` (bis zur Benennung eines Modul-Owners) |
| Zielrolle | Softwareentwicklerinnen und Softwareentwickler |
| Laufzeitfassung | `runtime/30-role-software-development.md`, zur Aktivierung in die Regelablage |

## 1. Zweck und Abgrenzung

Dieses Pack konkretisiert das Arbeitsmodell für Implementierungsaufgaben: Verstehen von Code, Analyse von Änderungen, Planung, Umsetzung kleiner Änderungen, Tests, Refaktorisierung, Fehleranalyse, Vorbereitung von Bugfixes und Merge Requests. Es enthält keine Governance-Regeln (Core) und keine Projektwerte (Overlay).

Nicht Gegenstand dieses Packs: Architektur- und Technologieentscheidungen, Schnittstellenverträge, Datenmodelle mit Migration, Sicherheitsfunktionen, Deployment (jeweils Kontrollstufe hoch, andere Packs oder nicht delegierbar).

## 2. Typische Aufgaben mit Betriebsmodus und Kontrollstufe

| Aufgabe | Modus | Typische Kontrollstufe (Maximumprinzip beachten) | Skill |
|---|---|---|---|
| Repository oder Modul kennenlernen | M1 | niedrig | `koolie-repo-analyze` |
| Bestehende Funktion erklären lassen | M1 | niedrig | `koolie-code-explain` |
| Auswirkungen einer geplanten Änderung analysieren | M1 | niedrig–mittel | `koolie-change-analyze` |
| Implementierungsplan erstellen | M2 | mittel | `koolie-plan` |
| Kleine, klar abgegrenzte Änderung umsetzen | M3 | niedrig–mittel | `koolie-change-small` |
| Unit Tests erstellen oder erweitern | M4 | niedrig | `koolie-tests` |
| Refaktorisierung ohne Verhaltensänderung | M3 | mittel | `koolie-refactor` |
| Fehler analysieren | M1 | niedrig–mittel | `koolie-error-analyze` |
| Bugfix vorbereiten | M2 | mittel | `koolie-bugfix-prepare` |
| Merge-Request-Beschreibung erstellen | M5 | niedrig | `koolie-mr-description` |

## 3. Arbeitsweise (normativ)

1. Vor jeder Änderung MUSS die Menge der Verwender geänderter Elemente ermittelt werden (Suche nach Bezeichnern, Aufrufhierarchie, Konfigurationsreferenzen); Fundstellen werden gelistet.
2. Fehlerbehebung folgt der Reihenfolge Reproduktion → Ursache mit Fundstelle → minimale Korrektur → Regressionstest. Eine Korrektur ohne verstandene Ursache DARF NICHT übernommen werden.
3. Refaktorisierungen MÜSSEN verhaltensneutral sein; Tests werden vor und nach der Änderung ausgeführt; funktionale Änderungen erfolgen in getrennten Schritten und Commits.
4. Neue Funktionalität SOLL bestehende Erweiterungspunkte, Schichtung und Muster des Moduls nutzen; neue Abstraktionen erfordern eine Begründung im Plan.
5. Fehlerbehandlung und Logging folgen den bestehenden Mustern des Moduls; stille Catch-Blöcke, Fehlermeldungen mit Interna und Logging sensibler Daten sind unzulässig.
6. Performance-Änderungen erfordern eine Messung vorher/nachher; Methode und Ergebnis werden berichtet.
7. Generierter Code wird vor Übernahme vollständig gelesen; die Bearbeiterin oder der Bearbeiter MUSS jede Zeile erklären können (Q3).
8. Bei Unsicherheit über fachliche Anforderungen wird `<PRODUCT_OWNER_ROLE>` gefragt, nicht der KI-Client.

## 4. Rollenspezifische Kontextquellen

| Quelle | Typische Kontextklasse | Hinweis |
|---|---|---|
| Quellcode des betroffenen Moduls und seiner Verwender | K1 | Least Context: nur betroffene Pakete |
| Bestehende Tests des Moduls | K1 | Teststil übernehmen |
| Coding Conventions (`<PROJECT_RULES_PATH>`) | K1 | verbindlich |
| Ticket (bereinigt) | K2 | Titel, Beschreibung, Akzeptanzkriterien |
| Stacktraces und Logauszüge | K2 | bereinigt |
| Architekturvorgaben | K1/K2 laut Manifest | bei Änderungen an Modulgrenzen |

## 5. Rollenspezifische Prüfpunkte (Ergänzung zur Review-Checkliste)

- Wurden alle Verwender geänderter Signaturen angepasst (Fundstellen)?
- Sind Randbedingungen (Null, leer, Grenzwerte, Nebenläufigkeit) explizit behandelt und getestet?
- Ist die Fehlerbehandlung konsistent mit dem Modul?
- Wurde die Reihenfolge Reproduktion → Ursache → Korrektur eingehalten (bei Bugfixes)?
- Sind Refaktorisierung und Funktionsänderung getrennt?

## 5b. Aktivierung im Projekt

Dieses Pack ist nach einer Erstinstallation **nicht** aktiv. Es wird wie jedes Pack im Projekt aktiviert (`.koolie/core/framework/role-packs/README.md` Punkt 4):

1. Rolle im Overlay Abschnitt 1 („Rollen im Team") aufführen.
2. Laufzeitfassung kopieren:
   `runtime/30-role-software-development.md` → `30-role-software-development.md` in der Regelablage
3. `python .koolie/core/install.py --update` ausführen; er bringt die Laufzeitfassung in die Form des installierten Client Packs.
4. Validieren: `python .koolie/core/tests/scripts/validate-framework.py --strict-overlay`

Eigene Skills sind nicht mitzukopieren – das Pack nutzt die Framework-Skills, die ohnehin in der Laufzeitschicht liegen (Abschnitt 6).

## 6. Rollenspezifische Skills

Das Pack nutzt die Framework-Skills `FW-SK-001` bis `FW-SK-013` und bringt keine eigenen mit.

## 7. Typische Fehlanwendungen in dieser Rolle

| Fehlanwendung | Folge | Gegenmaßnahme |
|---|---|---|
| Ganze Feature-Tickets „an den KI-Client geben" | Scope-Verlust, unprüfbare Änderungssätze | Zerlegung in Analyse, Plan, kleine Änderungen |
| Vorschläge übernehmen, ohne sie zu verstehen | Fehler in Randbedingungen bleiben unentdeckt | Q3, Skill `koolie-code-explain` auf den eigenen Diff anwenden |
| Tests vom KI-Client „passend machen" lassen | Fehlverhalten wird zementiert | M4-Regeln, Review-Punkt RV4 |
| Stacktrace unbereinigt einfügen | K2/K3-Abfluss | Checkliste `02-privacy-context.md` |
| Refaktorisierung und Fix in einem Schritt | Nicht reversibel, schwer zu reviewen | P7, getrennte Schritte |

## 8. Änderungsverlauf

| Version | Datum | Änderung | Autor (Rolle) |
|---|---|---|---|
| 0.1.0 | 2026-09-01 | Referenzpack angelegt | Framework-Erstellung |
| 0.1.2 | 2026-10-02 | Sprachlich überarbeitet; Abschnitt 5b nennt `install.py --update` wie `role-packs/README.md` | `<FRAMEWORK_OWNER>` |
