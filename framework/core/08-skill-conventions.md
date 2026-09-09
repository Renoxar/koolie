# Framework Core 08 – Skill-Standard

| Attribut | Wert |
|---|---|
| Modul-ID | FW-CORE-08 |
| Ebene | 1 – Framework Core |
| Verbindlichkeit | normativ (Abschnitte 1–7), Erläuterung (Abschnitt 8) |
| Owner | `<FRAMEWORK_OWNER>` |
| Version | 0.1.0 |

## 1. Begriff (normativ)

Ein **Skill** ist eine versionierte, testbare, wiederverwendbare Arbeitsanweisung für Devin, die eine abgegrenzte Aufgabe nach einem festen Verfahren mit festem Ausgabeformat bearbeitet. Skills sind die bevorzugte Form, wiederkehrende Aufgaben zu standardisieren. Ein Skill entscheidet nichts, was ein Mensch entscheiden muss (Delegationsverbotsliste).

## 2. Ablage und Dateien (normativ)

```text
.devin/skills/<skill-name>/
├── SKILL.md        # normativ: Frontmatter + Metadaten + Anweisung (wird vom Agenten geladen)
├── EXAMPLES.md     # erläuternd: Positiv- und Negativbeispiele (synthetisch gekennzeichnet)
├── TESTS.md        # Testfälle für den Testkatalog (mindestens ein Positiv- und ein Negativtest)
└── CHANGELOG.md    # Änderungsverlauf des Skills
```

- Ablageort `.devin/skills/<skill-name>/SKILL.md` `[DOK]` (Devin-Desktop-FAQ und CLI-Dokumentation). Alternativer, in der Produktdokumentation als empfohlen genannter Pfad `.agents/skills/` – Discovery durch Devin Local `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>`.
- Der Verzeichnisname ist der Aufrufname (`/skill-name`) `[DOK]`.
- Framework-Skills tragen das Präfix `fw-`, projektspezifische Skills `prj-`, Role-Pack-Skills `role-<pack>-`, Technology-Pack-Skills `tech-<pack>-`.
- Skill-Namen bestehen aus Kleinbuchstaben, Ziffern und Bindestrichen.

## 3. Frontmatter (normativ)

Das Frontmatter enthält ausschließlich in der Devin-Dokumentation belegte Felder `[DOK]`:

| Feld | Pflicht | Regel |
|---|---|---|
| `name` | MUSS | identisch mit dem Verzeichnisnamen |
| `description` | MUSS | ein Satz: Was der Skill tut und wann er verwendet wird; keine Projektbezüge |
| `argument-hint` | SOLL | erwartete Argumente, zum Beispiel `[pfad-oder-ticket]` |
| `allowed-tools` | MUSS | minimal notwendige Werkzeuge (`read`, `grep`, `glob`, `edit`, `exec`, MCP-Muster); lesende Skills ohne `edit` und `exec` |
| `permissions` | SOLL | zusätzliche `deny`/`ask`/`allow`-Regeln des Skills; additiv zur Sitzung `[DOK]` |
| `triggers` | MUSS | `["user"]` für alle Skills, die Dateien ändern oder Befehle ausführen; `["user", "model"]` nur für rein lesende Skills |
| `model`, `subagent`, `agent` | KANN | nur mit dokumentierter Begründung im Metadatenblock |

Framework-Metadaten (ID, Version, Status, Owner) stehen nicht im Frontmatter, sondern im Metadatenblock des Dateikörpers (D-08).

## 4. Pflichtinhalte je Skill (normativ)

| Nr. | Element | Ablage | Inhalt |
|---|---|---|---|
| 1 | Eindeutige ID | SKILL.md Metadaten | Schema `FW-SK-NNN` (Framework), `PRJ-SK-NNN` (Projekt), `RP-<PACK>-SK-NNN`, `TP-<PACK>-SK-NNN` |
| 2 | Name | Frontmatter `name` | Verzeichnisname |
| 3 | Version | SKILL.md Metadaten | Semantic Versioning `MAJOR.MINOR.PATCH` |
| 4 | Status | SKILL.md Metadaten | `entwurf`, `pilot`, `aktiv`, `veraltet`, `zurückgezogen` |
| 5 | Zweck | SKILL.md Abschnitt 1 | ein Absatz |
| 6 | Zielgruppe | SKILL.md Abschnitt 1 | Rollen |
| 7 | Trigger | SKILL.md Abschnitt 1 | Situationen, in denen der Skill verwendet wird; Aufrufform |
| 8 | Vorbedingungen | SKILL.md Abschnitt 2 | Was vor dem Aufruf erfüllt sein muss (Preflight, Kontrollstufe, Modus) |
| 9 | Benötigte Eingaben | SKILL.md Abschnitt 2 | Argumente und Kontext mit Kontextklasse |
| 10 | Zulässige Kontextquellen | SKILL.md Abschnitt 2 | Positivliste |
| 11 | Ausgeschlossene Informationen | SKILL.md Abschnitt 2 | Negativliste, mindestens K3 |
| 12 | Arbeitsschritte | SKILL.md Abschnitt 3 | nummeriert, mit Halte- und Rückfragepunkten |
| 13 | Grenzen | SKILL.md Abschnitt 4 | Was der Skill nicht tut |
| 14 | Rückfragenregeln | SKILL.md Abschnitt 4 | Wann und wie gefragt wird |
| 15 | Erwartetes Ausgabeformat | SKILL.md Abschnitt 5 | festes Markdown-Gerüst |
| 16 | Qualitätskriterien | SKILL.md Abschnitt 6 | prüfbare Kriterien |
| 17 | Prüf- und Freigabeschritt | SKILL.md Abschnitt 6 | Was der Mensch danach tut |
| 18 | Fehlerbehandlung | SKILL.md Abschnitt 7 | Verhalten bei Fehlschlag, Abbruchbedingungen |
| 19 | Beispiele | EXAMPLES.md | mindestens ein Positivbeispiel, synthetisch gekennzeichnet |
| 20 | Negativbeispiele | EXAMPLES.md | mindestens ein Negativbeispiel mit Erklärung |
| 21 | Testfälle | TESTS.md | mindestens ein Positiv- und ein Negativtest nach Testkatalogschema |
| 22 | Owner | SKILL.md Metadaten | generische Rolle |
| 23 | Änderungsverlauf | CHANGELOG.md | Version, Datum, Änderung, Autor-Rolle |

## 5. Trennung normativ / erläuternd (normativ)

- `SKILL.md` enthält nur normative Anweisungen und den Metadatenblock. Erläuterungen werden auf `EXAMPLES.md` verwiesen, nicht eingebettet (Least Context).
- Innerhalb von `SKILL.md` sind Abschnitte, die nur der Orientierung dienen, mit „(Erläuterung)" gekennzeichnet; alles andere ist normativ.
- Beispiele sind mit „**Beispiel (synthetisch)**" gekennzeichnet und enthalten ausschließlich Platzhalter oder offensichtlich fiktive Bezeichner.

## 6. Anforderungen an das Verhalten jedes Skills (normativ)

1. Projektneutral: keine Projekt-, Kunden-, Personen- oder Infrastrukturbezüge; projektspezifische Werte werden aus dem Overlay gelesen oder als Platzhalter geführt.
2. Rückfragen bei Unklarheiten verlangen (P3) und Annahmen sichtbar machen.
3. Scope ausdrücklich begrenzen (Pfade, Modus, Kontrollstufe) und Überschreitungen melden.
4. Relevante Prüfungen definieren (welche Tests, welche Checkliste).
5. Festes Ausgabeformat verwenden.
6. Delegationsverbotsliste beachten.
7. Bei Kontrollstufe hoch ohne dokumentierte Freigabe die Bearbeitung ablehnen.

## 7. Lebenszyklus, Versionierung und Test (normativ)

| Status | Bedeutung | Voraussetzung für Übergang |
|---|---|---|
| `entwurf` | in Erstellung, nicht für produktive Nutzung | – |
| `pilot` | Nutzung in Pilotgruppe | Testfälle vorhanden, Validierung bestanden, Review durch Modul-Owner |
| `aktiv` | freigegeben | Pilotfeedback ausgewertet, Positiv- und Negativtests bestanden, Freigabe Framework Owner |
| `veraltet` | ersetzt oder nicht mehr empfohlen; Nutzung mit Hinweis | Nachfolger benannt oder Begründung dokumentiert |
| `zurückgezogen` | entfernt; Verzeichnis bleibt bis zum nächsten Major-Release mit Hinweisdatei | Deprecation-Frist abgelaufen |

- MAJOR: Änderung des Ausgabeformats oder des Scopes; MINOR: neue Schritte oder Prüfungen ohne Formatbruch; PATCH: Korrekturen und Formulierungen.
- Jede Versionsänderung erfordert die erneute Ausführung der Testfälle in `TESTS.md`; Ergebnisse werden im Testkatalog vermerkt.
- Die strukturelle Konformität prüft `tests/scripts/validate-framework.py` (Pflichtabschnitte, Frontmatter, Platzhalter, verbotene Muster).

## 8. Erläuterung

Ein Skill ist weniger ein „Prompt" als eine Arbeitsanweisung, wie sie auch für Menschen geschrieben würde: Zweck, Voraussetzungen, Schritte, Ergebnis, Prüfung. Der Aufwand für Testfälle und Beispiele zahlt sich aus, sobald der zweite Skill auf dem ersten aufbaut oder ein Produkt-Update das Verhalten verändert – dann zeigt ein fehlgeschlagener Negativtest das Problem, bevor es im Projekt auffällt.
