# Prompt-Bibliothek

| Attribut | Wert |
|---|---|
| Ebene | 1 – Framework Core (projektunabhängig) |
| Verbindlichkeit | normativ (Abschnitte 2, 3, 5, 6, 7), Erläuterung (Abschnitte 1, 4) |
| Owner | `<FRAMEWORK_OWNER>` |
| Version | 0.1.3 |
| Status | `pilot` |
| Grundlage | `.koolie/core/framework/core/06-prompting-rules.md`, `.koolie/core/framework/core/05-working-model.md`, `.koolie/core/framework/core/09-risk-model.md`, `.koolie/core/framework/core/02-privacy.md` |

## 1. Zweck (Erläuterung)

Die Prompt-Bibliothek enthält zwölf geprüfte Vorlagen für wiederkehrende Aufgaben mit dem KI-Client. Jede Vorlage setzt die Pflichtelemente einer Aufgabenanweisung aus `.koolie/core/framework/core/06-prompting-rules.md` Abschnitt 1 um (Ziel, Betriebsmodus, Kontrollstufe mit Faktor, Scope, Kontext mit Klasse, Akzeptanzkriterien, Ausgabeformat, Rückfrageregel) und verankert die Regeln des Frameworks im Wortlaut der Anweisung: Fundstellen statt Behauptungen, gekennzeichnete Annahmen, keine Scope-Erweiterung, Rückfragen statt Annahmen, Ergebnisbericht am Ende, menschliche Prüfung vor jeder Übernahme. Die Vorlagen sind für zwei Situationen gedacht: für Aufgaben ohne passenden Skill sowie als strukturierte Anweisung rund um den Aufruf eines Skills (zum Beispiel mit Fragenkatalog, ausformulierten fachlichen Erwartungen oder zusätzlichen Vorgaben).

## 2. Verhältnis Prompt und Skill

1. Liegt für eine Aufgabe ein Skill vor, MUSS er bevorzugt verwendet werden (`.koolie/core/framework/core/06-prompting-rules.md`, Regel 7; Aufruf `/skill-name` `[DOK]`). Skills sind versioniert, getestet und über `allowed-tools` und `permissions` technisch abgesichert; eine Prompt-Vorlage ist es nicht.
2. Eine Prompt-Vorlage mit verwandtem Skill KANN als strukturierte Anweisung um den Skill herum verwendet werden oder den Skill ersetzen, wenn dieser in der Laufzeitschicht nicht verfügbar ist. In beiden Fällen gelten die Grenzen des Skills (Betriebsmodus, Kontrollstufen, Delegationsverbote) unverändert.
3. Prompt-Vorlagen ohne verwandten Skill (FW-PR-008, FW-PR-009) liefern ausschließlich Befunde und Hypothesen mit Fundstellen; die Bewertung erfolgt durch die benannte Rolle (zum Beispiel `<SECURITY_CONTACT>`) beziehungsweise durch Messung. Sie sind auf den Modus M1 beschränkt und ersetzen weder Security Scans noch Penetrationstests noch Messungen.
4. Eine Prompt-Vorlage erweitert den Handlungsspielraum des Werkzeugs nie über die Wurzel-Anweisungsdatei, die Regeln der Regelablage und das Project Overlay hinaus; sie kann ihn nur einschränken.

## 3. Aufbau einer Prompt-Vorlage

Jede Datei `.koolie/core/prompts/NN-<name>.md` folgt derselben Struktur: Metadatenblock (ID `FW-PR-0NN`, Version, Status, Owner, Betriebsmodus, typische Kontrollstufe, verwandter Skill) und acht Abschnitte:

| Abschnitt | Inhalt |
|---|---|
| 1. Zweck | Aufgabe, Ergebnisart, Abgrenzung zu Skills und anderen Vorlagen |
| 2. Einzusetzender Kontext | Positivliste der Kontextquellen mit Kontextklasse (K0–K2) |
| 3. Nicht einzusetzender Kontext | Negativliste, mindestens K3 und `<EXCLUDED_PATHS>` |
| 4. Eingabeparameter | Tabelle: Parameter, Pflicht, Kontextklasse, Beschreibung |
| 5. Prompt-Vorlage | Genau ein Codeblock mit der wörtlichen Anweisung; Parameter in geschweiften Klammern `{parameter}`, Framework-Platzhalter in spitzen Klammern (`<TEST_COMMAND>`) |
| 6. Erwartetes Ergebnis | Gerüst des Ergebnisses; verweist auf das Ausgabeformat des verwandten Skills und den Ergebnisbericht |
| 7. Prüfschritte | Checkbox-Liste für den Menschen mit Verweis auf die passende Checkliste |
| 8. Typische Fehlanwendungen | Tabelle: Fehlanwendung, Folge, Stattdessen |

Parameter in geschweiften Klammern werden vor dem Einsatz vollständig ersetzt; unbefüllte Parameter DÜRFEN NICHT an den KI-Client gesendet werden (Entfernen oder „nicht angegeben" eintragen). Platzhalter in spitzen Klammern bezeichnen Werte des Project Overlays (`.koolie/core/docs/PLACEHOLDER_REGISTRY.md`) und werden durch die im Overlay festgelegten Werte ersetzt; offene Overlay-Entscheidungen (`<TBD: …>`) blockieren den Einsatz der betroffenen Vorlage.

## 4. Übersicht der Prompt-Vorlagen (Erläuterung)

| ID | Datei | Titel | Modus | Verwandter Skill |
|---|---|---|---|---|
| `FW-PR-001` | `01-understand-codebase.md` | Codebasis verstehen | M1 | `fw-repo-analyze` |
| `FW-PR-002` | `02-impact-analysis.md` | Impact-Analyse | M1 | `fw-change-analyze` |
| `FW-PR-003` | `03-implementation-planning.md` | Implementierungsplanung | M2 | `fw-plan` |
| `FW-PR-004` | `04-code-generation.md` | Codegenerierung | M3 | `fw-change-small` |
| `FW-PR-005` | `05-test-generation.md` | Testgenerierung | M4 | `fw-tests` |
| `FW-PR-006` | `06-refactoring.md` | Refactoring | M3 | `fw-refactor` |
| `FW-PR-007` | `07-debugging.md` | Debugging | M1 | `fw-error-analyze` |
| `FW-PR-008` | `08-security-review.md` | Security Review | M1 | keiner (Ansatz von `fw-review-support`) |
| `FW-PR-009` | `09-performance-analysis.md` | Performance-Analyse | M1 | keiner |
| `FW-PR-010` | `10-documentation.md` | Dokumentation | M5 | `fw-docs-update` |
| `FW-PR-011` | `11-merge-request-review.md` | Review eines Merge Requests | M1 | `fw-review-support` |
| `FW-PR-012` | `12-developer-training.md` | Technische Schulung eines neuen Entwicklers | M1 | `fw-code-explain` |

Typische Abfolge einer Änderung: FW-PR-001 (Verstehen) → FW-PR-002 (Impact-Analyse, Vorschlag der Kontrollstufe) → Preflight durch den Menschen → FW-PR-003 (Plan, Bestätigung) → FW-PR-004, FW-PR-005 oder FW-PR-006 (Umsetzung in neuer Sitzung) → FW-PR-011 (Review-Unterstützung) → Merge Request mit KI-Nutzungsvermerk (`.koolie/core/templates/MR_AI_DISCLOSURE.md`).

## 5. Prompting-Regeln in Kurzform

Vollständig in `.koolie/core/framework/core/06-prompting-rules.md`; die Kurzform ersetzt das Dokument nicht.

1. **Ein Ziel je Anweisung.** Mehrere Ziele werden in mehrere Sitzungen zerlegt; eine Vorlage je Sitzung.
2. **Pflichtelemente vollständig.** Ziel, Betriebsmodus, Kontrollstufe mit Faktor, Scope (erlaubt und ausgeschlossen) sowie Kontext mit Klasse MÜSSEN, Akzeptanzkriterien und Ausgabeformat SOLLEN enthalten sein; die Rückfrageregel KANN wiederholt werden (Standard über die Wurzel-Anweisungsdatei). Die Vorlagen enthalten alle acht Elemente.
3. **Referenzen statt Kopien.** Dateien per Pfad referenzieren; eingefügter Text MUSS vorher auf seine Kontextklasse geprüft sein (`.koolie/core/decision-trees/01-context-allowed.md`, `.koolie/core/checklists/02-privacy-context.md`).
4. **Keine impliziten Berechtigungen.** Formulierungen wie „mach einfach", „räum auf" oder „alles, was nötig ist" DÜRFEN NICHT verwendet werden.
5. **Keine Rollenspiele mit Regelwirkung.** Aufforderungen, Regeln zu ignorieren oder Prüfungen zu überspringen, sind unzulässig – auch zu Testzwecken außerhalb des Testkatalogs.
6. **Ergebnis vor Stil.** Belegte Ergebnisse (Fundstellen, unveränderte Testausgaben) statt Selbstbewertungen.
7. **Skills bevorzugen.** Freie Prompts nur für Aufgaben ohne passenden Skill (Abschnitt 2).
8. **Iterationen kennzeichnen.** Folgeanweisungen benennen, was sich gegenüber dem vorherigen Schritt ändert.
9. **Sprache.** Anweisungen in der Arbeitssprache des Overlays (`<TBD: Arbeitssprache>`); Bezeichner, Befehle und Pfade unverändert.
10. **Unzulässige Muster** (Auszug aus Abschnitt 3 des Kerndokuments): „Behebe alle Fehler im Projekt", „Hier ist der Ticket-Export, mach das", „Schreib die Tests so, dass sie durchlaufen", „Push das und erstell den MR", „Welche Bibliothek wäre gut? Bau sie ein."

## 6. Verwendung

1. Preflight durchführen (`.koolie/core/checklists/01-preflight.md`): Delegierbarkeit (V1–V12), Kontrollstufe mit Faktor nach dem Maximumprinzip, Betriebsmodus, Scope.
2. Passende Vorlage wählen (Abschnitt 4); prüfen, ob stattdessen der Skill direkt aufzurufen ist (Abschnitt 2).
3. Parameter befüllen; jeden Wert auf Kontextklasse prüfen; K2-Inhalte nur nach dokumentierter Freigabe und Bereinigung, K3 nie.
4. Codeblock aus Abschnitt 5 in eine neue KI-Sitzung einfügen (eine Aufgabe, eine Sitzung); Schreib- und Ausführungsanfragen einzeln bestätigen (Permission-Modus Normal `[DOK]`).
5. Ergebnis anhand Abschnitt 7 der Vorlage und der genannten Checklisten prüfen; Ergebnisbericht ablegen (ab Stufe mittel: `<TBD: Ablageort für Ergebnisberichte>`).
6. Übernahme ausschließlich über den bestehenden Review- und Freigabeprozess; im KI-Nutzungsvermerk KANN die verwendete Prompt-ID neben den Skills genannt werden.

## 7. Versionierung und Pflege

- Jede Vorlage trägt Version (`MAJOR.MINOR.PATCH`) und Status (`entwurf`, `pilot`, `aktiv`, `veraltet`, `zurückgezogen`) analog zum Skill-Standard (`.koolie/core/framework/core/08-skill-conventions.md`, Abschnitt 7). MAJOR: Änderung der Struktur, des Ausgabeformats oder des Scopes; MINOR: neue Schritte, Parameter oder Prüfungen ohne Formatbruch; PATCH: Korrekturen und Formulierungen.
- Änderungen an Vorlagen erfolgen über den Änderungsprozess des Frameworks (`.koolie/core/framework/core/01-governance.md`); Projekte DÜRFEN Vorlagen in `.koolie/core/prompts/` NICHT anpassen. Projektspezifische Ergänzungen gehören in das Project Overlay, nicht in dieses Verzeichnis (`.koolie/core/decision-trees/06-rule-placement.md`).
- Die strukturelle Konformität (Platzhalter, verbotene Muster, Codeblöcke) prüft `.koolie/core/tests/scripts/validate-framework.py`; die Wirksamkeit einer Vorlage wird wie bei Skills über Testsitzungen auf dem Übungsrepository bewertet. Systematische Befunde aus Reviews (dieselbe Auffälligkeit bei mehreren Einsätzen) werden als Feedback an `<FRAMEWORK_OWNER>` gemeldet.
- Alle zwölf Vorlagen stehen seit 0.52.0 auf `pilot`; ihre Abnahme steht namentlich in `.koolie/core/tests/protocols/2026-09-15-gegenpruefung-restliche-nicht-skill-traeger.md` (`CR-2026-074`, D-109). **Ihre Übergangsbedingungen stehen in `.koolie/core/framework/core/01-governance.md` Abschnitt 5 und nicht hier** (D-102). Bis 0.50.0 stand an dieser Stelle eine eigene, strengere Bedingung: „mindestens eine dokumentierte Testsitzung je Vorlage auf dem Übungsrepository". **Das ist derselbe Fehler, den D-103 für die Skills berichtigt hat** – ein bestandener Sitzungstest ist Voraussetzung für `aktiv`, nicht für `pilot`. Die strengere Fassung kettete Kriterium 3 von D-11 an Kriterium 2, seinen größten Posten, ohne dass ein Decision Record das je entschieden hätte; sie stand in einem Modulträger und in keinem Register (D-107). Für `aktiv` gilt die Testsitzung unverändert, dazu die Voraussetzungen des Skill-Standards (Pilotfeedback ausgewertet, Freigabe durch den Framework Owner).
