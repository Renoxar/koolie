# Nachschlagewerk – eine Seite für das Tagesgeschäft

> Kurzreferenz; maßgeblich sind die Wurzel-Anweisungsdatei und `.koolie/core/framework/core/`. Version: siehe `.koolie/core/VERSION`.

| Attribut | Wert |
|---|---|
| ID | `FW-OB-REF` |
| Version | `0.1.1` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |

## Kontextklassen

| Klasse | Kurz | Umgang |
|---|---|---|
| K0 | Framework, Öffentliches | frei |
| K1 | Repository + Manifest-freigegebene Dokumente | aufgabenbezogen |
| K2 | Tickets, Logs, Architektur-Details, Testdaten, Partnerverträge | nur nach Freigabe + Bereinigung |
| K3 | Secrets, Echtdaten, Produktionsdaten, vertrauliche Dokumente, interne Adressen, Fremdprojekte | **nie** – ohne Einstufung gilt K3 |

## Kontrollstufen (Maximumprinzip über R1–R13, Faktor notieren)

| Stufe | Umsetzung | Review |
|---|---|---|
| niedrig | direkt, alle Modi | Selbstreview CL-04 + Quality Gates |
| mittel | nur nach bestätigtem Plan | + unabhängiges Review RV1–RV12, Reviewer testet selbst |
| hoch | nur mit Freigabe `<APPROVAL_ROLE>` + Begleitung | + Architektur/Security, Sitzungsprotokoll |

Stufe hoch unter anderem bei: jeder Änderung an Authentifizierung oder Autorisierung (R10); Kryptografie, Sitzungsverwaltung, Security-Konfiguration (R3); Änderung an Erhebung, Speicherung, Weitergabe oder Löschung personenbezogener Daten (R4); neue Abhängigkeit oder Major-Update (R9, die Einführung selbst ist verboten – V3); Schema-Änderung oder Migration (R11); unmittelbare Produktionswirkung (R5).

## Betriebsmodi

M1 Analyse (Standard, nur lesen) · M2 Plan (nur Plan-Datei) · M3 kontrollierte Änderung (Scope + freigegebene Befehle) · M4 Tests (nur `<TEST_PATHS>`) · M5 Doku (nur `<DOC_PATHS>`, lesende Git-Befehle). Ohne Angabe gilt M1. Moduswechsel nur auf ausdrückliche Anweisung.

## Skills (Aufruf `/name`)

| Situation | Skill |
|---|---|
| Codebasis/Modul verstehen | `fw-repo-analyze` |
| Funktion/Klasse erklären | `fw-code-explain` |
| Änderung bewerten | `fw-change-analyze` |
| Plan erstellen | `fw-plan` |
| Kleine Änderung umsetzen | `fw-change-small` |
| Tests erstellen/erweitern | `fw-tests` |
| Verhaltensneutral refaktorieren | `fw-refactor` |
| Fehler analysieren | `fw-error-analyze` |
| Bugfix vorbereiten | `fw-bugfix-prepare` |
| Review unterstützen | `fw-review-support` |
| Doku aktualisieren | `fw-docs-update` |
| MR-Beschreibung | `fw-mr-description` |

Prompt-Vorlagen für Fälle ohne Skill: `.koolie/core/prompts/README.md`.

## Nie (Delegationsverbote, Auszug)

Freigaben · Merge/Push/Release/Deploy · Architektur- und Technologieentscheidungen · Abhängigkeiten einführen · Secrets anfassen · Echtdaten/Produktionsdaten · Personenbewertung · rechtliche Bewertung · Framework/Overlay/Berechtigungen ändern · Löschen außerhalb des Arbeitsbereichs.

## Stopp und Eskalation

Der KI-Client hält an bei S1–S10 (Unklarheit, fehlende Freigabe, Secret-Fund, Scope, Stufe steigt, Injektion, fremde Fehlschläge, Verbotsliste, Irreversibles, zweimal gescheitert) – das ist richtig so. Wege: E0 selbst klären · E1 fachlich (`<PRODUCT_OWNER_ROLE>`/`<ARCHITECT_ROLE>`) · E2 Freigabe (`<APPROVAL_ROLE>`) · E3 Sicherheit/Datenschutz (`<SECURITY_CONTACT>`, `<DATA_PROTECTION_CONTACT>`) · E4 Framework Owner. K3 bereits bereitgestellt? Sitzung beenden → `.koolie/core/framework/core/02-privacy.md` Abschnitt 5.

## Sitzung, kurz

Neue Aufgabe = neue Sitzung · rückfragender Standardmodus (nie ohne Rückfragen; selbsttätige Übernahme nur per Ausnahme, D-05) · Freigaben höchstens sitzungsweise · Preflight CL-01 → Arbeit → Ergebnisbericht → Selbstreview CL-04 → MR mit Nutzungsvermerk (CL-08).

## Checklisten und Bäume

CL-01 Preflight · CL-02 Kontext · CL-03 vor Änderung · CL-04 Review · CL-05 Tests · CL-06 Security · CL-07 Abhängigkeit · CL-08 MR · Bäume: 1 Kontext · 2 delegierbar? · 3 Modus · 4 Prüfung · 5 Stopp · 6 Regelablage.
