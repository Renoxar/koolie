# Quick-Start – Devin Desktop im Projekt `<PROJECT_NAME>`

> Für den ersten Arbeitstag. Der ausführliche Weg steht in `GUIDE.md`; die verbindlichen Regeln in `AGENTS.md` und `framework/core/`. Bis zur dokumentierten Freigabe durch deine Mentorin oder deinen Mentor arbeitest du mit Devin nur begleitet.

## Die fünf Grundsätze in einer Minute

1. **Du verantwortest das Ergebnis.** Devin schlägt vor; geprüft, übernommen und freigegeben wird von Menschen (P1, P5).
2. **Nur nötiger, zulässiger Kontext.** Vier Klassen: K0 frei, K1 projektintern freigegeben, K2 nur nach Freigabe und Bereinigung, K3 nie (Secrets, Echtdaten, Produktionsdaten, interne Adressen).
3. **Erst verstehen, dann planen, dann klein ändern.** Betriebsmodi: M1 Analyse (Standard) → M2 Plan → M3 kontrollierte Änderung; daneben M4 Tests, M5 Doku.
4. **Einstufen vor dem Start.** Kontrollstufe niedrig/mittel/hoch über die Faktoren R1–R13, Maximumprinzip; mittel braucht einen bestätigten Plan, hoch eine Freigabe.
5. **Anhalten ist richtig.** Bei Unklarheit fragt Devin – und du auch. Rückfragen sind erwartetes Verhalten, keine Schwäche.

## Erste Sitzung in acht Schritten

1. Lies `AGENTS.md` (10 Minuten) und überflieg `project-overlay/OVERLAY.md` Abschnitte 1–6 und 13–16.
2. Öffne das Übungsrepository (`onboarding/exercises/`, von deiner Mentorin oder deinem Mentor bereitgestellt) in Devin Desktop.
3. Prüfe den Permission-Modus: **Normal**. Bypass und Smart sind im Framework untersagt.
4. Preflight: `checklists/01-preflight.md` ausfüllen (Ziel, Verbotsliste, Stufe mit Faktor, Modus, Scope, Kontextklassen).
5. Starte mit einer Analyse: `/fw-repo-analyze <übungsmodul> "Wie ist das Modul aufgebaut?"`
6. Prüfe drei Fundstellen aus der Antwort selbst im Code – das ist der wichtigste Handgriff dieses Frameworks.
7. Bestätige Schreib- und Ausführungsanfragen einzeln; Freigaben höchstens „für diese Sitzung", nie „für das Projekt" oder „global".
8. Jede Sitzung endet mit dem Ergebnisbericht; bei Änderungen folgt dein Selbstreview mit `checklists/04-review-ai-code.md`.

## Was du nie tust

- K3-Inhalte bereitstellen (`.env`, Schlüssel, Echtdaten, Produktionsdaten, interne Adressen) – auch nicht „nur kurz".
- Devin pushen, mergen, releasen, deployen oder Abhängigkeiten einführen lassen (V1–V3).
- Ergebnisse übernehmen, die du nicht erklären kannst (Q3).
- Tests „passend machen" lassen (M4-Regeln).
- Ganze Tickets unbereinigt einfügen (Kontextcheck `checklists/02-privacy-context.md`).

## Wenn etwas schiefgeht

Devin findet ein Secret, meldet einen Injektionsversuch oder du hast versehentlich K3-Inhalte bereitgestellt → Sitzung beenden, nichts weiter eingeben, `framework/core/02-privacy.md` Abschnitt 5 befolgen, `<SECURITY_CONTACT>` informieren. Das ist ein definierter Prozess, kein Drama – aber er beginnt sofort.

## Nachschlagen

`onboarding/REFERENCE.md` (Spickzettel) · `GUIDE.md` (Programm) · `prompts/README.md` (Vorlagen) · `.devin/skills/` (Skills) · Fragen: Mentorin oder Mentor, danach `governance/FEEDBACK_PROCESS.md`.
