---
description: Allgemeine Entwicklungsregeln für KI-unterstützte Änderungen (Qualität, Tests, Commits, Dokumentation). Anwenden bei jeder Aufgabe in den Modi M3, M4 oder M5.
trigger: model_decision
---

# Allgemeine Entwicklungsregeln (Laufzeitfassung)

Langform: `.koolie/core/framework/core/04-quality.md`, `.koolie/core/framework/core/07-review-rules.md`. Projektspezifische Conventions stehen im Overlay und haben bei Konkretisierungen Vorrang vor allgemeinen Mustern.

## Änderungen

- Ein Ziel je Änderung; keine Vermischung von Fehlerbehebung, Refaktorisierung und Feature.
- Berührt eine Änderung mehr als `<CHANGE_SIZE_THRESHOLD>` Dateien, wird sie aufgeteilt oder als Kontrollstufe hoch behandelt; bei fehlendem Wert im Overlay ist der Umfang zu melden.
- Bestehende Muster des betroffenen Moduls übernehmen, sofern sie nicht den Overlay-Conventions widersprechen. Keine neuen Muster, Frameworks oder Abstraktionen ohne Auftrag.
- Keine beiläufigen Umformatierungen, Umbenennungen, Import-Umsortierungen oder Kommentarkorrekturen außerhalb der geänderten Zeilen.
- Generierte Reste entfernen: ungenutzte Importe, tote Pfade, auskommentierter Code, generische Platzhalterkommentare.
- Öffentliche Schnittstellen (Signaturen, Schemata, Endpunkte, Konfigurationsschlüssel) nur ändern, wenn der bestätigte Plan es vorsieht; jede Änderung als Schnittstellenänderung kennzeichnen.
- Behauptete Eigenschaften (thread-safe, abwärtskompatibel, performanter) nur mit Beleg (Test, Messung, Fundstelle) angeben.

## Tests

- Geänderte Logik wird von Tests begleitet, die das fachliche Verhalten prüfen; Testnamen beschreiben das erwartete Verhalten.
- Bestehende Tests nicht anpassen, um neue Implementierungen zu bestätigen, außer der bestätigte Plan ändert das fachliche Verhalten ausdrücklich; dann Änderung begründen.
- Testbefehle nur aus dem Overlay (`<TEST_COMMAND>`); Ergebnisse unverändert berichten, einschließlich Anzahl übersprungener Tests.
- Nicht testbare Änderungen als solche benennen und einen manuellen Prüfschritt vorschlagen.

## Commits und Merge Requests (Vorschläge, Ausführung durch den Menschen)

- Commit-Nachricht nach `<COMMIT_CONVENTION>`: Was und warum, Bezug zum Ticket (`<ISSUE_TRACKER>`-Kennung als Platzhalter, wenn nicht bekannt).
- Merge-Request-Beschreibung nach Skill `fw-mr-description`, einschließlich KI-Nutzungsvermerk (`.koolie/core/templates/MR_AI_DISCLOSURE.md`).
- Keine Nennung von Personen, Kunden, Behörden oder internen Adressen in Commits, Kommentaren oder Beschreibungen.

## Dokumentation

- Dokumentation nur in den Dokumentationspfaden des Overlays ändern und nur für Verhalten, das im Code belegt ist.
- Kommentare erklären das Warum; keine Kommentare über die Tatsache der KI-Erzeugung im Code.
- Abweichungen zwischen Code und bestehender Dokumentation melden, nicht stillschweigend „korrigieren", wenn unklar ist, welche Seite richtig ist.

## Selbstprüfung vor der Übergabe

Vor dem Ergebnisbericht prüfen: Scope eingehalten · Fundstellen korrekt · verwendete Methoden, Klassen und Bibliotheksfunktionen existieren in der eingesetzten Version (Fundstelle) · keine neuen Abhängigkeiten · keine geänderten Konfigurationen oder Quality Gates · Tests vorhanden und ausgeführt · keine K3-Inhalte im Ergebnis · offene Punkte und Annahmen gelistet.
