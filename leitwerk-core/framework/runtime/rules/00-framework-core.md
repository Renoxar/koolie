---
description: Kurzfassung des Framework-Arbeitsmodells (Standardarbeitsablauf, Betriebsmodi, Kontrollstufen). Immer aktiv.
trigger: always_on
---

# Framework Core – Arbeitsmodell (Kurzfassung)

Langform: `leitwerk-core/framework/core/05-working-model.md`, `leitwerk-core/framework/core/09-risk-model.md`. Diese Kurzfassung ist normativ; bei Abweichungen gilt die Langform.

## Standardarbeitsablauf

1 Aufgabe verstehen → 2 Scope und Grenzen bestimmen → 3 Datenschutz und Kontextfreigabe prüfen → 4 Rückfragen und offene Punkte erfassen → 5 Ist-Zustand analysieren → 6 Befunde mit Fundstellen darstellen → 7 Lösungsoptionen bewerten → 8 Vorgehen oder Änderungsplan vorschlagen → 9 Freigabepunkt vor risikoreichen Änderungen → 10 Änderung in kleinen Schritten umsetzen → 11 Tests und Qualitätsprüfungen ausführen → 12 Ergebnis, Abweichungen, Restrisiken dokumentieren → 13 menschliche Prüfung ermöglichen → 14 Übernahme über den bestehenden Review- und Freigabeprozess.

Schritte werden nicht übersprungen. Ohne bestätigten Plan (Schritt 9) beginnt bei Kontrollstufe mittel und hoch keine Umsetzung.

## Betriebsmodi

| Modus | Schreiben | Befehle | Kernregel |
|---|---|---|---|
| M1 Read-only Analysis (Standard) | nein | nein | Befunde nur mit Fundstellen |
| M2 Guided Planning | nur Plan-Datei | nein | Plan enthält Schritte, Dateien, Tests, Risiken, Rollback, offene Fragen |
| M3 Controlled Modification | im freigegebenen Scope | freigegebene Build-/Test-/Lint-Befehle | ein Schritt je Änderung, Bericht nach jedem Schritt |
| M4 Test and Validation | nur Testpfade | freigegebene Testbefehle | kein Produktivcode, keine abgeschwächten Tests |
| M5 Documentation Support | nur Dokumentationspfade | nur lesende Git-Befehle | nur belegtes Verhalten dokumentieren |

Der Modus wird vom Menschen vorgegeben. Ohne Angabe gilt M1. Ein Moduswechsel erfordert eine ausdrückliche Anweisung und wird im Ergebnisbericht vermerkt.

## Kontrollstufen (Maximumprinzip)

- **niedrig:** alle Modi; Selbstreview und bestehende Quality Gates.
- **mittel:** M3 nur nach bestätigtem Plan; unabhängiger Diff-Review; Tests für geänderte Logik verpflichtend.
- **hoch:** M3 nur nach dokumentierter Freigabe durch `<APPROVAL_ROLE>` mit begleitender Person; Architektur-/Security-Review. Jede Berührung von Authentifizierung, Autorisierung, Kryptografie, personenbezogener Datenverarbeitung, Datenmodellen mit Migration, Produktionskonfiguration oder neuen Abhängigkeiten ist mindestens hoch beziehungsweise nicht delegierbar.
- Steigt die Stufe während der Arbeit: anhalten, melden, auf Entscheidung warten.
- Nicht delegierbar (nur Analyse/Vorbereitung): Freigaben, Merges, Releases, Deployments, Secrets, Produktionsdaten, Architektur- und Technologieentscheidungen, Personenbewertungen, rechtliche Bewertungen, Änderungen an Framework, Overlay und Berechtigungen.

## Ergebnisbericht (Pflicht am Ende jeder Sitzung)

Aufgabe · Modus · Kontrollstufe (auslösender Faktor) · verwendete Skills · verwendeter Kontext mit Klasse · Befunde/Änderungen mit Fundstellen · ausgeführte Befehle mit Ergebnis · Abweichungen vom Plan · gekennzeichnete Annahmen und offene Fragen · Restrisiken und empfohlene Prüfungen.
