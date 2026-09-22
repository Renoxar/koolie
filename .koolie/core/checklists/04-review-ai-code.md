# Checkliste FW-CL-04 – Review KI-generierten Codes

| Attribut | Wert |
|---|---|
| ID | `FW-CL-04` |
| Version | `0.1.2` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Wann | Selbstreview vor jedem Commit mit KI-Beteiligung; unabhängiges Review im Merge Request |
| Wer | Bearbeiterin oder Bearbeiter (Selbstreview); unabhängige Reviewerin oder Reviewer (ab Stufe mittel verpflichtend) |
| Dauer (Richtwert, Erläuterung) | abhängig vom Diff – keine verbindlichen Aufwände |
| Nachweis | Selbstreview im KI-Nutzungsvermerk; Review-Befunde im Merge Request |

## Zweck

Operationalisiert die Prüfpunkte RV1–RV12 aus `.koolie/core/framework/core/07-review-rules.md` für die tägliche Anwendung. Ein KI-Befund (`fw-review-support`) ersetzt keine dieser Prüfungen.

## Prüfpunkte

### Scope und Belege

- [ ] **MUSS** (RV1) Nur freigegebene Dateien und Bereiche geändert; keine beiläufigen Umformatierungen, Umbenennungen oder Import-Umsortierungen.
- [ ] **MUSS** (RV2) Stichprobe der Fundstellen aus dem Ergebnisbericht geprüft (mindestens drei); Aussagen decken sich mit dem Code.
- [ ] **MUSS** (RV12) Annahmen und offene Fragen aus dem Ergebnisbericht sind adressiert oder im Merge Request sichtbar.

### Fachlichkeit und Korrektheit

- [ ] **MUSS** (RV10) Jede geänderte Zeile ist der Bearbeiterin oder dem Bearbeiter erklärbar (Q3); Unerklärliches wird nicht übernommen.
- [ ] **MUSS** (RV5) Verwendete Methoden, Klassen und Bibliotheksfunktionen existieren in der eingesetzten Version (Import- oder Manifest-Fundstelle; bei Zweifel Suche im Repository beziehungsweise in der lokalen Abhängigkeit).
- [ ] **MUSS** (RV3) Bei Refaktorisierungen: fachliches Verhalten nachweislich unverändert (Vorher/Nachher-Testlauf, unveränderte Randbedingungen `<`/`<=`, Fehlerbehandlung, Rundung, Reihenfolge).
- [ ] **MUSS** Randbedingungen geprüft: Null/leer, Grenzwerte, Zeitzonen/Locale, Nebenläufigkeit, Ressourcenfreigabe – soweit für die Änderung relevant.

### Tests und Quality Gates

- [ ] **MUSS** (RV4) Tests prüfen fachliches Verhalten, nicht die Implementierung; keine entfernten oder abgeschwächten Assertions; keine Tests, die nur Mocks verifizieren.
- [ ] **MUSS** (RV9) Keine Änderungen an Linter-, Coverage-, Pipeline- oder Quality-Gate-Konfiguration; keine ignorierten oder übersprungenen Tests ohne dokumentierte Begründung.
- [ ] **MUSS** Lokale Prüfungen ausgeführt (`<LINT_COMMAND>`, `<TEST_COMMAND>`); Ergebnisse liegen unverändert vor.

### Sicherheit, Datenschutz, Abhängigkeiten

- [ ] **MUSS** (RV7) Eingabevalidierung und Autorisierungsprüfung in neuen Pfaden; Fehlermeldungen ohne Interna; kein Logging sensibler Daten; keine hartcodierten Geheimnisse; bei Treffern `.koolie/core/checklists/06-security.md` anwenden.
- [ ] **MUSS** (RV8) Keine neue oder erweiterte Verarbeitung personenbezogener Daten; sonst Stufe hoch und `<DATA_PROTECTION_CONTACT>`.
- [ ] **MUSS** (RV6) Abhängigkeiten, Versionen, Lockfiles, Paketquellen unverändert; sonst `.koolie/core/checklists/07-new-dependency.md` und regulärer Prozess.
- [ ] **MUSS** Keine K3-Inhalte im Diff, in Kommentaren, Testdaten oder Commit-Nachrichten.

### Konsistenz

- [ ] **MUSS** (RV11) Dokumentation, Kommentare und Commit-Nachricht sind konsistent mit der Änderung; Konventionen (`<PROJECT_RULES_PATH>`, `<COMMIT_CONVENTION>`) eingehalten.
- [ ] **SOLL** Generierte Reste entfernt (ungenutzte Importe, tote Pfade, auskommentierter Code, Platzhalterkommentare) (Q6).
- [ ] **SOLL** Review-Tiefe entspricht der Kontrollstufe (`.koolie/core/framework/core/07-review-rules.md` Abschnitt 3); bei Stufe mittel führt die Reviewerin oder der Reviewer die Tests selbst aus.

## Abbruch- und Eskalationskriterien

Befunde, die auf Scope-Verlassen, erfundene Fundstellen oder umgangene Quality Gates hindeuten, stoppen die Übernahme (E0/E1). Systematische Befunde über mehrere der KI-Client-Änderungen werden an den Framework Owner gemeldet (`.koolie/core/governance/FEEDBACK_PROCESS.md`, E4). Sicherheits- oder Datenschutzbefunde: Prozess der Organisation, Erfassung nach `.koolie/core/governance/INCIDENT_HANDLING.md` (E3).

## Ergebnis und Nachweis

Selbstreview wird im KI-Nutzungsvermerk bestätigt; unabhängige Review-Befunde und ihre Auflösung stehen im Merge Request. Verworfene Vorschläge werden mit Grund gezählt (Pilotmetrik).
