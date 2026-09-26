---
description: Vorgaben des Frameworks für die Spezifikationen, die der Client selbst als Planartefakt anlegt (Anforderungen, Entwurf, Aufgaben). Immer aktiv bei Clients mit eigenem Spezifikationsablauf.
trigger: always_on
---

# Planartefakt: die Spezifikationen des Clients (Laufzeitfassung)

Langform: `<CORE_DIR>/framework/core/05-working-model.md` (Abschnitt 1 und Modus M2 – Planbestätigung), `<CORE_DIR>/templates/PLAN_TEMPLATE.md`, `<CORE_DIR>/framework/role-packs/requirements-engineering/skills/role-re-ticket/SKILL.md`. Entscheidung: D-415.

Dein Client legt Spezifikationen unter `<RUNTIME_DIR>/specs/<name>/` an: `requirements.md` (bei einem Fehler `bugfix.md`), `design.md` und `tasks.md`. **Sie sind in diesem Projekt der Träger des Änderungsplans.** Einen zweiten Plan nach `PLAN_TEMPLATE.md` legst du daneben nicht an. Die folgenden Vorgaben gelten für jede Spezifikation, auch im schnellen Ablauf ohne Zwischenfreigaben.

## 1. `requirements.md`

- **Jede Anforderung nennt ihre Quelle:** die Aufgabenstellung, ein Dokument aus dem Overlay-Manifest oder eine Fundstelle im Code (Pfad und Zeile). Eine Anforderung ohne Quelle wird nicht geschrieben.
- **Nichts erfinden.** Was die Quelle nicht hergibt, steht unter **Offene Fragen**, mit der Rolle, die entscheiden muss – nicht als Anforderung und nicht als Annahme ohne Kennzeichnung.
- Anforderung, Befund und Randbedingung bleiben getrennt. Keine Personen, keine Kunden- oder Behördennamen, keine Echtdaten (`<RULES_DIR>/10-privacy-security.md`).

## 2. `design.md`

Führt zusätzlich zum Entwurf die Pflichtfelder der Planvorlage:

- **Zieldateiliste:** jede Datei, die die Umsetzung anlegt, ändert oder löscht. Eine Datei, die nicht in der Liste steht, wird nicht angefasst.
- **Kontrollstufe** (niedrig, mittel, hoch) mit dem auslösenden Risikofaktor.
- **Teststrategie, Risiken, Rollback und Abbruchkriterien** – in der Tiefe, die die Kontrollstufe verlangt.

## 3. `tasks.md` – erst nach Bestätigung

- Die Aufgabenliste trägt oben den **Bestätigungsstatus**: `entwurf` oder `bestätigt durch <Rolle> am <Datum>`.
- **Du führst keine Aufgabe aus, solange der Status `entwurf` lautet.** Die Bestätigung erteilt ein Mensch ausdrücklich in der Sitzung; bei Kontrollstufe hoch ist es die Freigabe durch `<APPROVAL_ROLE>`. Eine Bestätigung des Entwurfs gilt nicht für die Aufgaben.
- Ändert sich der Plan nach der Bestätigung – eine weitere Datei, ein anderer Schritt –, fällt der Status auf `entwurf` zurück.

⚠️ **Grenze, benannt:** Diese Datei ist eine Anweisung. Ob der Client den Spezifikationsablauf an ihr ausrichtet, ist eine Frage des Modellverhaltens (`[TEXTUELL]`); die Fähigkeitsmatrix des Client Packs sagt, was davon gemessen ist.
