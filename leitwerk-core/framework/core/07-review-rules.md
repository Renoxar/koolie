# Framework Core 07 – Review-Regeln für KI-unterstützte Änderungen

| Attribut | Wert |
|---|---|
| Modul-ID | FW-CORE-07 |
| Ebene | 1 – Framework Core |
| Verbindlichkeit | normativ (Abschnitte 1–4), Erläuterung (Abschnitt 5) |
| Owner | `<FRAMEWORK_OWNER>` |
| Version | 0.1.0 |

## 1. Grundsätze (normativ)

1. Ein Review prüft das Ergebnis, nicht die Entstehung: Für den Reviewer gelten dieselben Maßstäbe wie bei manuell erstelltem Code, ergänzt um die Prüfpunkte aus Abschnitt 2.
2. Die Bearbeiterin oder der Bearbeiter ist die erste Reviewerin beziehungsweise der erste Reviewer (Selbstreview anhand `leitwerk-core/checklists/04-review-ai-code.md`) und DARF NICHT die einzige Prüfinstanz sein (Vier-Augen-Prinzip, sofern im Projekt vorgesehen; ab Kontrollstufe mittel verpflichtend).
3. Devin KANN das Review unterstützen (Skill `fw-review-support`), aber ein Devin-Befund ersetzt keine menschliche Prüfung und eine Devin-„Freigabe" existiert nicht (V1).
4. Reviewerinnen und Reviewer erhalten den KI-Nutzungsvermerk (Kontrollstufe, Modus, Skills, Kontext) vor Beginn des Reviews.

## 2. Zusätzliche Prüfpunkte für KI-generierte Änderungen (normativ)

| Nr. | Prüfpunkt | Typische Auffälligkeit |
|---|---|---|
| RV1 | Scope-Treue: Wurden nur die freigegebenen Dateien und Bereiche geändert? | „Beiläufige" Umformatierungen, geänderte Nachbarmethoden |
| RV2 | Fundstellen-Treue: Stimmen die im Bericht genannten Fundstellen mit dem Code überein? | Erfundene Aufrufer, nicht existierende Konfigurationsschlüssel |
| RV3 | Verhaltensäquivalenz bei Refaktorisierungen: Ist das fachliche Verhalten nachweislich unverändert? | Geänderte Randbedingungen (`<`, `<=`), veränderte Fehlerbehandlung |
| RV4 | Testaussagekraft: Prüfen die Tests Verhalten oder zementieren sie die Implementierung? | Tests, die nur Mocks verifizieren; entfernte Assertions |
| RV5 | API-Existenz: Existieren verwendete Methoden, Klassen, Bibliotheksfunktionen in der eingesetzten Version? | Halluzinierte Methoden, veraltete Signaturen |
| RV6 | Abhängigkeiten: Wurden Abhängigkeiten, Versionen, Lockfiles oder Paketquellen verändert? | Neue Bibliothek „für eine Zeile" |
| RV7 | Sicherheit: Eingabevalidierung, Autorisierungsprüfung, Logging sensibler Daten, Kryptografie, Fehlermeldungen mit Interna | Fehlende Prüfung im neuen Code-Pfad |
| RV8 | Datenschutz: Neue Verarbeitung, Speicherung oder Ausgabe personenbezogener Daten? | Debug-Logging von Anfrageinhalten |
| RV9 | Konfiguration und Quality Gates: Unverändert? | Angepasste Linter-Schwellen, ignorierte Tests |
| RV10 | Verständlichkeit: Kann die Bearbeiterin oder der Bearbeiter jede Zeile erklären? | Übernommene Muster ohne Begründung |
| RV11 | Dokumentation: Sind Dokumentation, Kommentare und Commit-Nachricht konsistent mit der Änderung? | Kommentare aus einem anderen Kontext |
| RV12 | Offene Punkte: Sind Annahmen und Rückfragen aus dem Ergebnisbericht adressiert? | Als „TODO" verbliebene Annahmen |

## 3. Review-Tiefe nach Kontrollstufe (normativ)

| Stufe | Mindesttiefe |
|---|---|
| niedrig | Vollständiges Lesen des Diffs; RV1, RV2, RV5, RV9, RV10 |
| mittel | Alle Prüfpunkte RV1–RV12; Abgleich mit bestätigtem Plan; Ausführung der Tests durch die Reviewerin oder den Reviewer |
| hoch | Wie mittel; zusätzlich Architektur- und Security-Review durch die im Overlay benannten Rollen; Sitzungsprotokoll wird geprüft |

## 4. Umgang mit Befunden (normativ)

1. Befunde werden wie bei jedem Review im Merge Request dokumentiert.
2. Systematische Befunde (dieselbe Auffälligkeit in mehreren Devin-Änderungen) werden als Feedback an den Framework Owner gemeldet (`leitwerk-core/governance/FEEDBACK_PROCESS.md`), da sie auf eine Regel- oder Skill-Lücke hindeuten.
3. Sicherheitsrelevante Befunde folgen dem Prozess der Organisation und werden zusätzlich in `leitwerk-core/governance/INCIDENT_HANDLING.md` erfasst, wenn sie auf ein Framework-Versagen zurückgehen.

## 5. Erläuterung

Reviews von KI-Änderungen scheitern selten an Sorgfalt und häufig an Ermüdung: Der Code sieht sauber aus, die Beschreibung ist ausführlich, die Tests sind grün. Die Prüfpunkte RV2 (Fundstellen), RV4 (Testaussagekraft) und RV5 (API-Existenz) adressieren genau die Fehlerklassen, die ein routiniertes Review sonst übersieht.
