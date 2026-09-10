# Framework Core 04 – Qualitätsgrundsätze

| Attribut | Wert |
|---|---|
| Modul-ID | FW-CORE-04 |
| Ebene | 1 – Framework Core |
| Verbindlichkeit | normativ (Abschnitte 1–4), Erläuterung (Abschnitt 5) |
| Owner | `<FRAMEWORK_OWNER>` |
| Version | 0.1.0 |

## 1. Gleichbehandlung (normativ)

1. KI-generierter oder KI-unterstützter Code MUSS mindestens dieselben Prüfungen durchlaufen wie manuell erstellter Code. Das Framework fügt Prüfungen hinzu, es entfernt keine.
2. Welche Prüfungen es gibt (Build, Linting, statische Analyse, Unit-, Integrations-, Komponententests, Security Scans, `<QUALITY_GATE>`, Merge Request, Code Review, Vier-Augen-Prinzip, fachliche Abnahme), legt ausschließlich das Project Overlay fest (Abschnitt 7 des Overlays). Das Framework setzt kein bestimmtes Werkzeug voraus.
3. Die Herkunft einer Änderung (mit oder ohne Devin) ändert nichts an der Verantwortung: Wer den Commit erstellt, verantwortet ihn.

## 2. Anforderungen an KI-unterstützte Änderungen (normativ)

| Nr. | Anforderung | Verbindlichkeit |
|---|---|---|
| Q1 | Eine Änderung verfolgt genau ein Ziel (ein Ticket, ein Fehler, eine Refaktorisierung). Vermischte Änderungen werden aufgeteilt. | MUSS |
| Q2 | Jede Änderung an Logik wird von Tests begleitet, die das fachliche Verhalten prüfen; reine Umformatierungen sind davon ausgenommen. | MUSS |
| Q3 | Devin-Vorschläge werden vor Übernahme vollständig gelesen und verstanden. Code, den die Bearbeiterin oder der Bearbeiter nicht erklären kann, wird nicht übernommen. | MUSS |
| Q4 | Generierter Code folgt den Coding Conventions des Overlays; bei Widerspruch zwischen Devin-Vorschlag und Convention gilt die Convention. | MUSS |
| Q5 | Kommentare und Commit-Nachrichten beschreiben das Warum, nicht die Tatsache der KI-Nutzung; die KI-Nutzung wird im Merge Request vermerkt (`leitwerk-core/templates/MR_AI_DISCLOSURE.md`). | SOLL |
| Q6 | Tote Pfade, ungenutzte Importe, auskommentierter Code und generische Platzhalterkommentare aus der Generierung werden vor Übernahme entfernt. | MUSS |
| Q7 | Behauptete Eigenschaften („thread-safe", „abwärtskompatibel", „performanter") werden nur übernommen, wenn sie belegt sind (Test, Messung, Fundstelle). | MUSS |
| Q8 | Änderungen, die mehr als `<CHANGE_SIZE_THRESHOLD>` Dateien berühren, werden in mehrere Merge Requests aufgeteilt oder als Kontrollstufe hoch behandelt. | SOLL |

## 3. Definition of Done für Devin-Aufgaben (normativ)

Eine Devin-Aufgabe ist abgeschlossen, wenn:

1. der Ergebnisbericht (`05-working-model.md`, Abschnitt 3.6) vorliegt,
2. alle im Overlay definierten lokalen Prüfungen erfolgreich sind,
3. die Review-Checkliste für KI-generierten Code (`leitwerk-core/checklists/04-review-ai-code.md`) durch die Bearbeiterin oder den Bearbeiter abgearbeitet ist,
4. der Merge Request den Devin-Nutzungsvermerk enthält,
5. offene Punkte und Annahmen im Merge Request sichtbar sind,
6. die projektspezifische Definition of Done (Overlay, Abschnitt 12) erfüllt ist.

## 4. Metriken der Ergebnisqualität (normativ für die Erfassung, Zielwerte offen)

Für den Pilot werden je Devin-unterstütztem Merge Request erfasst: Kontrollstufe, Betriebsmodus, Anzahl Review-Iterationen, Anzahl fehlgeschlagener Pipeline-Läufe, Anteil verworfener Devin-Vorschläge (Selbsteinschätzung), Nachbearbeitungsaufwand (Selbsteinschätzung in Kategorien). Zielwerte werden nicht durch das Framework vorgegeben (`leitwerk-core/pilot/METRICS.md`).

## 5. Erläuterung

Die häufigste Qualitätsfalle ist nicht offensichtlich falscher Code, sondern plausibler Code, der ein Nachbarproblem löst: eine ähnliche Methode ändert, eine Randbedingung anders interpretiert oder ein Muster aus einem anderen Modul kopiert, das hier nicht gilt. Q3 („nur übernehmen, was man erklären kann") und P4 („Fundstellen statt Behauptungen") sind die wirksamsten Gegenmittel.
