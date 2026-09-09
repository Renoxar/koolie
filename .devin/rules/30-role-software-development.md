---
description: Role Pack Softwareentwicklung (Ebene 6). Anwenden, wenn die Aufgabe Implementierung, Refaktorisierung, Fehleranalyse oder Testerstellung im Quellcode betrifft.
trigger: model_decision
---

# Role Pack Softwareentwicklung (Laufzeitfassung)

Langform: `framework/role-packs/software-development/ROLE_PACK.md`. Dieses Pack enthält keine Governance-Regeln; es konkretisiert die Arbeitsweise für Entwicklungsaufgaben.

## Arbeitsweise

- Vor jeder Änderung: betroffene Aufrufer und Verwender der geänderten Elemente ermitteln (Suche nach Bezeichnern, Fundstellen nennen).
- Fehlerbehebung: erst Reproduktion (Test oder nachvollziehbare Schrittfolge), dann Ursache mit Fundstelle, dann minimale Korrektur, dann Regressionstest.
- Refaktorisierung: Verhalten bleibt nachweislich gleich; Tests vor und nach der Änderung ausführen; keine funktionalen Änderungen im selben Schritt.
- Neue Funktionalität: bestehende Modulstruktur und Schichtung einhalten; Erweiterungspunkte nutzen, statt neue zu schaffen.
- Fehlerbehandlung: bestehende Fehlerstrategie des Moduls übernehmen; keine stillen Catch-Blöcke; keine Fehlermeldungen mit internen Details nach außen.
- Logging: bestehendes Logging-Muster verwenden; keine personenbezogenen oder sensiblen Daten protokollieren.
- Performance: keine Optimierungen ohne Messung; Messmethode und Ergebnis berichten.

## Typische Skills dieses Packs

`fw-repo-analyze`, `fw-code-explain`, `fw-change-analyze`, `fw-plan`, `fw-change-small`, `fw-tests`, `fw-refactor`, `fw-error-analyze`, `fw-bugfix-prepare`, `fw-mr-description`.

## Grenzen

Architektur- und Technologieentscheidungen, Schnittstellenverträge, Datenmodelle mit Migration und Sicherheitsfunktionen liegen außerhalb dieses Packs (Kontrollstufe hoch oder nicht delegierbar).
