# Quick-Start – der KI-Client im Projekt `<PROJECT_NAME>`

> Für den ersten Arbeitstag. Der ausführliche Weg steht in `GUIDE.md`; die verbindlichen Regeln in der Wurzel-Anweisungsdatei und `.koolie/core/framework/core/`. Bis zur dokumentierten Freigabe durch deine Mentorin oder deinen Mentor arbeitest du mit dem Werkzeug nur begleitet.

| Attribut | Wert |
|---|---|
| ID | `FW-OB-QUICK` |
| Version | `0.1.0` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |

Kürzel wie **P1** (Prinzip, `.koolie/core/framework/core/00-principles.md`), **R1–R13**
(Risikofaktoren, `.koolie/core/framework/core/09-risk-model.md`) oder **M1–M5**
(Betriebsmodi, `.koolie/core/framework/core/05-working-model.md`) schlägst du dort nach;
die Kurzfassung auf einer Seite ist `REFERENCE.md`.

## Die fünf Grundsätze in einer Minute

1. **Du verantwortest das Ergebnis.** Der KI-Client schlägt vor; geprüft, übernommen und freigegeben wird von Menschen (P1, P5).
2. **Nur nötiger, zulässiger Kontext.** Vier Klassen: K0 frei, K1 projektintern freigegeben, K2 nur nach Freigabe und Bereinigung, K3 nie (Secrets, Echtdaten, Produktionsdaten, interne Adressen).
3. **Erst verstehen, dann planen, dann klein ändern.** Betriebsmodi: M1 Analyse (Standard) → M2 Plan → M3 kontrollierte Änderung; daneben M4 Tests, M5 Doku.
4. **Einstufen vor dem Start.** Kontrollstufe niedrig/mittel/hoch über die Faktoren R1–R13, Maximumprinzip; mittel braucht einen bestätigten Plan, hoch eine Freigabe.
5. **Anhalten ist richtig.** Bei Unklarheit fragt der KI-Client – und du auch. Rückfragen sind erwartetes Verhalten, keine Schwäche.

## Erste Sitzung in acht Schritten

1. Lies die Wurzel-Anweisungsdatei des Projekts (10 Minuten) und überflieg `.koolie/project-overlay/OVERLAY.md` Abschnitte 1–6 und 13–16.
2. Öffne im KI-Client das Übungsrepository, das deine Mentorin oder dein Mentor bereitgestellt hat (Aufbau: `.koolie/core/onboarding/exercises/README.md`).
3. Prüfe den Permission-Modus: **Normal** (jede Schreib- und Ausführungsanfrage wird einzeln bestätigt). Der Modus ohne Rückfragen (Bypass) ist untersagt; Modi, die Änderungen selbsttätig übernehmen, nur mit dokumentierter Ausnahme (D-05).
4. Preflight: `.koolie/core/checklists/01-preflight.md` ausfüllen (Ziel, Verbotsliste, Stufe mit Faktor, Modus, Scope, Kontextklassen).
5. Starte mit einer Analyse: `/fw-repo-analyze <übungsmodul> "Wie ist das Modul aufgebaut?"`
6. Prüfe drei Fundstellen aus der Antwort selbst im Code – das ist der wichtigste Handgriff dieses Frameworks.
7. Bestätige Schreib- und Ausführungsanfragen einzeln; Freigaben höchstens „für diese Sitzung", nie „für das Projekt" oder „global".
8. Jede Sitzung endet mit dem Ergebnisbericht; bei Änderungen folgt dein Selbstreview mit `.koolie/core/checklists/04-review-ai-code.md`.

## Was du nie tust

- K3-Inhalte bereitstellen (`.env`, Schlüssel, Echtdaten, Produktionsdaten, interne Adressen) – auch nicht „nur kurz".
- Den KI-Client pushen, mergen, releasen, deployen oder Abhängigkeiten einführen lassen (V1–V3).
- Ergebnisse übernehmen, die du nicht erklären kannst (Q3).
- Tests „passend machen" lassen (M4-Regeln).
- Ganze Tickets unbereinigt einfügen (Kontextcheck `.koolie/core/checklists/02-privacy-context.md`).

## Wenn etwas schiefgeht

Der KI-Client findet ein Secret, meldet einen Injektionsversuch oder du hast versehentlich K3-Inhalte bereitgestellt → Sitzung beenden, nichts weiter eingeben, `.koolie/core/framework/core/02-privacy.md` Abschnitt 5 befolgen, `<SECURITY_CONTACT>` informieren. Das ist ein definierter Prozess, kein Drama – aber er beginnt sofort.

## Nachschlagen

`.koolie/core/onboarding/REFERENCE.md` (Spickzettel) · `GUIDE.md` (Programm) · `.koolie/core/prompts/README.md` (Vorlagen) · Skill-Ablage (Skills) · Fragen: Mentorin oder Mentor, danach `.koolie/core/governance/FEEDBACK_PROCESS.md`.
