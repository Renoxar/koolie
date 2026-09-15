# Checkliste für Mentorinnen, Mentoren und Reviewer im Onboarding

| Attribut | Wert |
|---|---|
| ID | `FW-OB-MENTOR` |
| Version | `0.1.1` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Verhältnis zu FW-CL-09 | `leitwerk-core/checklists/09-onboarding.md` führt durch das Programm; diese Liste ergänzt die Mentorenperspektive je Modul |

## Vor dem Start

- [ ] **MUSS** Übungsrepository nach `exercises/README.md` eingerichtet (inklusive der drei Köder für Ü6); Overlay-Übungsfassung aktiv.
- [ ] **MUSS** Zugänge geprüft; Permission-Modus Normal beim Mentee eingestellt; keine globalen Freigaben aus früheren Installationen (`~/.config/devin/config.json` des Mentee frei von projektfremden Allow-Regeln – gemeinsam sichten).
- [ ] **SOLL** Drei bereinigte Beispielaufgaben aus dem Projektalltag für Modul 1 vorbereitet (delegierbar niedrig, delegierbar hoch, nicht delegierbar).

## Während der Module

- [ ] **MUSS** Modul 1: Verbotsliste nicht abfragen, sondern anwenden lassen (Mentee ordnet die Beispiele ein und begründet).
- [ ] **MUSS** Modul 2: Einstufungsübung Ü5 beobachten; typischen Fehler ansprechen (Mischinhalte nicht auf die höchste Klasse gehoben).
- [ ] **MUSS** Modul 3: Beide Preflights gegenzeichnen; auf vollständige Stufenbegründung (Faktor!) bestehen.
- [ ] **MUSS** Modul 7: Planbestätigung ausdrücklich als eigenen Schritt zelebrieren (nicht „passt schon") – das prägt das spätere Verhalten bei Stufe mittel.
- [ ] **MUSS** Modul 8: Beim Gegenreview drei bewusste Fragen stellen: Woher weißt du, dass diese API existiert? Was prüft dieser Test wirklich? Welche Fundstelle hast du selbst geöffnet?
- [ ] **MUSS** Modul 9/Ü6: Reaktion auf die Köder bewerten – erkannt und gemeldet (bestanden) oder befolgt/ignoriert (Modul wiederholen).
- [ ] **SOLL** Nach jedem Modul kurzes Feedbackgespräch; Beobachtungen sachbezogen notieren (Sachstände, keine Personenbewertungen – V7; das Protokoll dokumentiert Modulabschlüsse, nicht „Leistung").

## Rote Flaggen (Freigabe zurückstellen)

- Übernahme von Ergebnissen ohne geöffnete Fundstelle, auch nach Ansprache.
- Umgehungsversuche: Bypass/Smart aktivieren, globale Freigaben erteilen, Köder-Anweisungen befolgen.
- Einstufungsfehler bei K3-Kategorien in Ü5 oder Ü6.
- „Der KI-Client hat gesagt"-Argumentationen in fachlichen Fragen.

Zurückstellen heißt: betroffene Module wiederholen, weiter begleitet arbeiten, neuer Termin – ohne Vorwurf, das Framework ist neu für alle.

## Freigabe

- [ ] **MUSS** Alle Kriterien aus `COMPLETION_CRITERIA.md` gemeinsam durchgegangen; offene Punkte mit Folgeplan notiert.
- [ ] **MUSS** Freigabe mit Datum und Rolle im Onboarding-Protokoll dokumentiert; Projekt informiert.
- [ ] **SOLL** Follow-up-Termin nach den ersten selbstständigen Wochen vereinbart (Erfahrungen, Feedback an `leitwerk-core/governance/FEEDBACK_PROCESS.md`).
