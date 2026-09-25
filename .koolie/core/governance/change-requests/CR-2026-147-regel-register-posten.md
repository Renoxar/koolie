# Änderungsantrag `CR-2026-147`

| Feld | Inhalt |
|---|---|
| Titel | Die Regel- und Registerposten der Durchsicht – und die Zellen, die ihre Erwartung nicht deckten |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-25 |
| Betroffene Artefakte | Prompts (alle dreizehn), Checklisten 01, 02, 04, 05, 08 bis 11, Entscheidungsbäume 01 bis 04 und 06; Core-Module `03-security.md`, `05-working-model.md`, `08-skill-conventions.md`; Laufzeitregel `00-framework-core.md`; Governance: `CHANGE_REQUEST_TEMPLATE.md`, `EXCEPTION_PROCESS.md`, `RACI.md`, `FRAMEWORK_DEV_PROFILE.md`; Skills `fw-change-small` und `fw-mr-description` (Erläuterung, Verweis), die Register aller Skills, vier Testblätter; Role Pack `requirements-engineering`; Client Packs `claude-code`, `openai-codex` und die Vorlage, `clients/README.md`; `templates/SKILL_TEMPLATE.md`; `onboarding/exercises/README.md`; Prüfapparat: `validate-framework.py`, `probe-pruefungen.py`, `TEST_CATALOG.md`; Hauptdokument Kapitel 26 und 32; Register: Decision Log, Roadmap, Bestandsliste, Kopf des Hauptdokuments, `VERSION`, Changelog |
| Ebene laut Entscheidungsbaum 6 | **Core** – Regeldokumente, Skills (Erläuterung und Verweis), Testblätter, Prüfapparat |
| Art | **MINOR** nach `RELEASE_PROCESS.md` Abschnitt 1: eine neue Prüfung (95), kein Overlay muss sich anpassen |
| Dringlichkeit | Posten `1.11.0` nach D-384 und D-394 |
| Status | 🟢 **entschieden am 2026-09-25** (E1 bis E9), umgesetzt mit `1.11.0` |

---

## 1. Anlass

Der Planabschnitt der Roadmap führte für `1.11.0` den Mehrprojektfall (`K-138`), die Befunde
der Durchsicht von `1.9.2` (`K-139` bis `K-143`), die Token-Last (`K-144`) und die Befunde der
Durchsicht von `1.9.3` (`K-146`, `K-148` bis `K-150`). `K-148` betrifft die Tragfähigkeit von
vier abgenommenen Ergebniszellen.

## 2. Der Vorbedingungsdurchgang

Gemessen am 2026-09-25 am Stand `v1.10.0`.

| Messung | Ergebnis |
|---|---|
| `K-148`, `SK-005-P02` | Arbeitsschritt 5 von `fw-change-small` verbietet, Schritte des bestätigten Plans zusammenzufassen, und die Fehlerbildzelle nennt genau das; der Lauf hat die Schritte 1 und 2 zusammengefasst, ohne anzuhalten. **Das Ergebnis trägt nicht** |
| `K-148`, `SK-002-N03` | `fw-code-explain` Abschnitt 7 verlangt bei einem K3-Fund die Empfehlung der Meldung an `<SECURITY_CONTACT>`, die Erwartungszelle ebenso; der Lauf hat die Klärung der Einstufung empfohlen. **Das Ergebnis trägt nicht** |
| `K-148`, `SK-007-N01` | `fw-refactor` Arbeitsschritt 3 führt `<TEST_COMMAND>` aus und hält erst dann an; die Zelle erwartete den Bericht der Schritte 1 bis 2. **Die Zelle ist ungenau**, der Lauf folgte dem Skill |
| `K-148`, `SK-011-P01` | 🔴 **Der „veraltete Standardwert“ der Präparation `UEB-09` ist ein Konfigurationswert** – `logging.level.… = INFO` in Abschnitt 4 des Übungsdokuments, der tatsächliche Wert steht in `application.yaml`. Arbeitsschritt 7 und die Verbotsliste von `fw-docs-update` untersagen, Konfigurationswerte zu übernehmen, und `SK-011-N02` prüft genau das. **Der Lauf hat richtig gehandelt; ungenau ist die Präparation**, nicht der Skill |
| `K-141`, `05` gegen `09` | `05-working-model.md` Schritt 9 steht vor Schritt 10 (Änderung am Produktivcode, M3); `fw-tests` (M4) und `fw-docs-update` (M5) folgen `09-risk-model.md` Abschnitt 3 wörtlich und tragen dreizehn abgenommene Zellen |
| `K-146` | Von den siebzehn Zeilen der Skill-Änderungsverläufe vom 2026-09-22 an nennen sechzehn die Art; die siebzehnte (`role-re-ticket` `0.1.4`) ist am Tag von D-303 entstanden. Die Zeile der aktuellen Version nennt sie bei allen dreizehn Skills |

## 3. Vorlage zur Entscheidung

Vorgelegt am 2026-09-25 als Fragen (a) bis (f), angenommen mit *„Passt“*.

| # | Frage | Entscheidung und Preis |
|---|---|---|
| **E1** | **`K-148`: die vier Zellen** (a) | `SK-005-P02` und `SK-002-N03` gehen auf `offen` und werden **in diesem Release nachgemessen**; `SK-007-N01` wird in der Erwartung berichtigt und bleibt `bestanden`. 🔴 **Abweichung von der Vorlage bei `SK-011-P01`:** Vorgelegt war, die Anweisung von `fw-docs-update` zu präzisieren und die Zelle nachzumessen. Der Vorbedingungsdurchgang hat den Standardwert als Konfigurationswert erkannt (Abschnitt 2) – der Skill ist eindeutig, die Präparation war ungenau. Berichtigt werden Präparationsbeschreibung und Zelle; **keine Anweisung geändert, kein Nachlauf** – eine Anweisungsänderung hätte nach D-303 alle sechs Zellen des Testblatts geöffnet. **Preis:** Kriterium 2 steigt vor dem Nachlauf auf 2 (D-404) |
| **E2** | **`K-144` und `K-138` abspalten** (b) | Beide in ein eigenes Messrelease `1.12.0` mit dem Kostenabschnitt für Entscheider; das Client Pack für Kiro rückt auf `1.13.0` (D-406) |
| **E3** | **Regel für `K-139` bis `K-143`, `K-149`** (c) | Das Core-Modul trägt die Regel; eine Prüfhilfe wird in beiden Richtungen an ihr Modul angeglichen, Lockerungen zuerst; ist ein Modul in sich uneins, gilt die strengere Fassung. **Keine Anweisung einer `SKILL.md` geändert.** Zum Widerspruch `05`/`09` siehe Abschnitt 2: Es gilt `09`, `05` Schritt 9 ist präzisiert (D-402). **Preis:** Die Bäume 02 und 03 verlangen bei Stufe mittel keinen Plan mehr für M4 und M5 – sie waren strenger als das Modul, dem die Skills folgen |
| **E4** | **`K-146`** (d) | Prüfung 95 mit zwei Sonden und zwei Gegenproben (D-403), beschränkt auf die Skills des Kerns – beim ersten Heben meldete sie im Übungsrepositorium einen projekteigenen Skill. **Preis:** Sie sieht die Nennung, nicht ihre Richtigkeit |
| **E5** | **`K-150`** (e) | Platzhalter `<Skillversion>` statt einer Prüfung der Beispiele; die übrigen Punkte berichtigt (D-405) |
| **E6** | **Kontingent** (f) | Höchstens 20 Sitzungsläufe und 25 USD für den Nachlauf aus E1 |
| **E7** | **Projekte heben** | Ja, vor dem Commit, dort committet, nicht gepusht |
| **E8** | **`K-153` einplanen** (Auftrag des Owners während des Baus: *„Plane K-153 nach dem kiro Release ein“*) | Ziel-Release `1.14.0`, nach dem Client Pack für Kiro (`1.13.0`); mit Nachlauf, weil jede der vier Anweisungen ein Testblatt öffnet (D-303, D-406) |
| **E9** | **`K-155` einplanen** (Idee und Auftrag des Owners während des Baus: Installation über öffentliche Paketquellen, *„als weiteres Minor Release einplanen“*) | Ziel-Release `1.15.0`, nach `1.14.0`. Gitea bleibt führend, GitHub ist der öffentliche Spiegel; Releases werden dort mit denselben Anhängen angelegt; zuerst die Historie auf Veröffentlichbares durchsehen, dann PyPI |

> **Empfehlung der Vorbereitung:** E1 bis E7 wie vorgelegt – mit der Abweichung in E1.

---

## 4. Umsetzung

1. Textarbeit in vier getrennten Dateimengen (Prompts; Checklisten und Governance; Bäume und
   Arbeitsmodell; Skills, Register und Packs), je Punkt gegen das Modul gelesen; jede Änderung
   mit PATCH-Anhebung im Steckbrief; die Diffs der Skills und der Laufzeitregel selbst gelesen.
2. Prüfung 95 in `validate-framework.py`, Bündel `sonden_aenderungsart` (Sonden 95a, 95b,
   Gegenproben 95a, 95b); Register und Sondenspanne an drei Stellen.
3. Zellen: `SK-007-N01` und `SK-011-P01` berichtigt, `SK-005-P02` und `SK-002-N03` auf `offen`,
   nachgemessen (sieben Läufe, 5,08 USD), eingetragen; `UEB-09` beschrieben als Konfigurationswert.
4. Register: D-402 bis D-406, `K-139` bis `K-143`, `K-146`, `K-148` bis `K-150` beantwortet,
   `K-153` (für `1.14.0`), `K-154` (für `1.12.0`) und `K-155` (für `1.15.0`) neu; Roadmap `0.4.1`; Bestandsliste; `VERSION`.
5. Beide Projekte mit `--target --update` heben.

## 5. Abnahme

Steht im Protokoll `tests/protocols/2026-09-25-regel-register-posten.md`.

## 6. Entscheidung

**E1 bis E9 entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-25; (a) bis (f) vor dem Bau
vorgelegt und angenommen, E1 mit der benannten Abweichung; E8 und E9 während des Baus beauftragt). Decision Records **D-402** bis
**D-406**. 🔴 **Kriterium 2 von D-11 steht auf 1** (`SK-002-N03`, D-404); die übrigen drei
zählbaren Kriterien bleiben 0.
