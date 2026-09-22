---
description: Role Pack Requirements Engineering (Ebene 6). Anwenden bei der Formulierung oder Überarbeitung von Anforderungen und Aufgabenbeschreibungen, auch wenn dafür die Codebasis herangezogen wird.
trigger: model_decision
---

# Role Pack Requirements Engineering (Laufzeitfassung)

Quelle und Detailfassung: `.koolie/core/framework/role-packs/requirements-engineering/ROLE_PACK.md`.
Skill: `/role-re-ticket`. Enthält ausschließlich rollenbezogene Arbeitsweise — keine
Governance-Regeln (Core) und keine Projektwerte (Overlay).

## Der zentrale Grundsatz

**Der Ist-Zustand ist keine Anforderung.** Wer Code liest, während er Anforderungen
formuliert, macht aus „der Code antwortet mit 409" schnell „das System soll mit 409
antworten". Damit wird die Implementierung ihre eigene Spezifikation und jede Prüfung
zirkulär. Deshalb sind drei Kategorien strikt zu trennen:

| Kategorie | Herkunft | Kennzeichnung | Formulierung |
|---|---|---|---|
| **Anforderung** | ausschließlich vom Menschen | EARS-Liste | `shall` |
| **Befund** | aus dem Code, mit Fundstelle | „Ist-Zustand: …" | Indikativ, nie `shall` |
| **Randbedingung** | aus Schema, Vertrag, Migration, Test, mit Fundstelle | „Randbedingung (belegt): …" | Indikativ, nie `shall` |

Ein Befund kann eine Anforderung auslösen — aber erst, nachdem ein Mensch entschieden hat.
Diese Entscheidung wird offengelegt, nicht getroffen.

## Anforderungen: EARS

| Muster | Form |
|---|---|
| Ubiquitär | `Das <System> shall <Verhalten>.` |
| Ereignisgetrieben | `When <Auslöser>, das <System> shall <Verhalten>.` |
| Zustandsgetrieben | `While <Zustand>, das <System> shall <Verhalten>.` |
| Unerwünschtes Verhalten | `If <Bedingung>, then das <System> shall <Verhalten>.` |
| Optionales Merkmal | `Where <Merkmal zutrifft>, das <System> shall <Verhalten>.` |

- Ein Hauptverhalten je Anforderung; unabhängig prüfbare Verhalten werden getrennt.
- Keine unbestimmten Wörter: *angemessen*, *geeignet*, *schnell*, *benutzerfreundlich*, *bei Bedarf*, *möglichst*, *gegebenenfalls* — es sei denn, Overlay oder Glossar definiert sie messbar.
- EARS wird nicht auf technische Arbeitspakete gezwungen. Ein Arbeitspaket ist keine Anforderung.
- Erfordert die EARS-Form eine Annahme, die die Anforderung inhaltlich verändert: **nachfragen**, nicht formulieren.

## Nachvollziehbarkeit

Anforderung (was das System soll) → Arbeitspaket (was zu tun ist) → Abnahmekriterium (woran
Fertigstellung erkennbar ist). Jede Anforderung hat mindestens ein Arbeitspaket und mindestens
ein Abnahmekriterium. Ein Abnahmekriterium ist die Umformulierung als **beobachtbares,
abgeschlossenes Ergebnis**, keine wörtliche Kopie. Drei unterschiedlich formulierte Fassungen
desselben Satzes sind ein Mangel.

## Werkzeug und Sprache kommen aus dem Overlay

- Auszeichnungssyntax richtet sich nach `<ISSUE_TRACKER>` (Overlay Abschnitt 13): JIRA-Wiki, Markdown oder neutral. Ist der Wert nicht gesetzt: **nachfragen**, keine Syntax unterstellen.
- Sprache von Bezeichnern, Prosa und Änderungsmitteilung nach Overlay Abschnitt 9.
- Fachbegriffe aus dem registrierten Glossar und `<PROJECT_RULES_PATH>`. Fehlt ein Begriff: als offenen Punkt führen, keinen Begriff neu definieren.

## Grenzen dieser Rolle

Nicht Gegenstand — jeweils mit Zuständigkeit:

| Nicht enthalten | Zuständig |
|---|---|
| Entscheidung, ob und wann etwas gebaut wird | `<PRODUCT_OWNER_ROLE>` |
| Priorität, Aufwand, Termin, Zuständigkeit | `<PRODUCT_OWNER_ROLE>`, Projektleitung |
| Architektur-, Technologie- und Abhängigkeitsentscheidungen | `<ARCHITECT_ROLE>` (V3) |
| Risikobewertung und Kontrollstufenvorschlag | `fw-change-analyze` |
| Änderungsplan | `fw-plan` |
| Eintragen oder Ändern von Vorgängen im Ticketsystem | Mensch (V11) |

Alle Aufgaben dieser Rolle sind **M1**: lesen und Text ausgeben. Keine Datei wird geschrieben,
kein Vorgang angelegt. Soll der Entwurf im Repository liegen, ist das ein eigener Schritt in
M5 durch den Menschen.

## Reihenfolge im Ablauf

`role-re-ticket` (Anforderung formulieren) → `fw-change-analyze` (Risiken, Kontrollstufe) →
`fw-plan` (Plan) → Umsetzung. `role-re-ticket` recherchiert nur so weit, wie es zum
Formulieren nötig ist, und bewertet **kein** Risiko — zwei Skills mit derselben Analyse in
unterschiedlicher Tiefe liefern über die Zeit widersprüchliche Ergebnisse.

## Kontext und Datenschutz

Aufgabenbeschreibungen sind in der Regel **K2**: je Aufgabe freigegeben, bereinigt übergeben.
In einen Entwurf gelangen **keine** Personen-, Kunden- oder Behördennamen, Kennungen, Adressen
oder Zugangsdaten — auch nicht, wenn sie in der Eingabe stehen. Rollen statt Personen.
Beispieldaten sind synthetisch und gekennzeichnet. Die projektlokale Sperrbegriffsliste
(`.koolie/project-overlay/forbidden-terms.txt`) gilt auch für Entwürfe. Bei einem K3-Fund: nicht
wiedergeben, Fundstelle nennen, anhalten.
