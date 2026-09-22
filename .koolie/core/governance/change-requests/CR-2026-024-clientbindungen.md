# Änderungsantrag `CR-2026-024`

| Feld | Inhalt |
|---|---|
| Titel | Die letzten Client-Bindungen des Kerns – und die Prüfung, die sie nicht sehen konnte |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | 14 Kerndateien, ein Dateiname, `tests/scripts/validate-framework.py` (Prüfung 14 erweitert) |
| Ebene laut Entscheidungsbaum 6 | Kerndokumentation und Prüfung; keine Regeländerung |
| Art | Abarbeitung der mit `CR-2026-020` ausgewiesenen Restpunkte |
| Dringlichkeit | regulär |

## 1. Anlass und Problem

`CR-2026-020` hat 248 Akteursnennungen aus dem Kern gelöst und mit Prüfung 14 durchgesetzt. Drei
Punkte blieben ausdrücklich ausgewiesen und offen:

- der Dateiname `decision-trees/02-may-devin-do-task.md`,
- der Marker `VERIFY AGAINST CURRENT <name> DOCUMENTATION` „an fünf Kernstellen",
- die clientspezifischen Inhalte der Zeile „Umsetzung beim KI-Client" in `05-working-model.md`.

**Die Zählung war wieder zu niedrig.** Statt fünf Markerstellen waren es **acht** in
Markdown-Dateien und **zwei weitere in den Kernskripten** – letztere hatte die manuelle Zählung
übersehen, weil sie nur `*.md` durchsucht hatte. Gefunden hat sie erst die neue Prüfung.

Das ist derselbe Vorgang wie bei `CR-2026-020` selbst, wo die Roadmap 76 Nennungen führte und es
248 waren. **Eine von Hand erhobene Zahl über den eigenen Zustand ist im Mittel zu klein** – und
zwar systematisch, weil man dort zählt, wo man den Fehler vermutet.

### Warum Prüfung 14 den Marker nicht fand

Sie sucht den **kapitalisierten** Clientnamen (`Devin`, `Claude`). Ein Platzhalter schreibt ihn
**groß**: `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>`. Die Großform pauschal zu verbieten wäre
falsch gewesen – `CLAUDE.md` ist ein Dateiname, `DEVIN_PROJECT_DIR` eine Umgebungsvariable des
Clients, und beide stehen zu Recht in Abbildungstabellen und im Client Pack.

Die präzise Regel lautet deshalb: **Ein Platzhalter, der einen Clientnamen trägt, gehört nicht in
den Kern.** Er bindet ihn genauso an ein Produkt wie eine Akteursnennung.

## 2. Vorgeschlagene Änderung

- **Der Entscheidungsbaum heißt `02-may-ai-do-task.md`.** Fünf Verweise nachgezogen; historische
  Dokumente behalten den alten Namen, weil sie einen vergangenen Zustand beschreiben.
- **Zehn Markerstellen tragen die neutrale Form** `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>`,
  die `docs/PLACEHOLDER_REGISTRY.md` bereits führte. Im Client Pack `devin-desktop` bleibt die
  clientgebundene Form – dort ist sie richtig.
- **Das Register sagt jetzt, welche Form wohin gehört:** die clientgebundene als Altform „nur in
  einem Client Pack zulässig", die neutrale als „die im Kern zu verwendende Form".
- **Prüfung 14 erfasst zusätzlich Platzhalter mit Clientnamen.** Getrennt wird an Leerzeichen
  **und Unterstrichen** – sonst entginge ihr ein Platzhalter, der den Namen als Namensteil führt.
  Das Register ist ausgenommen: Es nennt Platzhalter, es verwendet sie nicht.
- **Neun Artefakte sind um eine PATCH-Stelle gehoben**, zwei Skills mit Eintrag im eigenen
  Änderungsverlauf – konsequent zu E3 aus `CR-2026-020`.

## 3. Was dieser Antrag nicht ändert

- **Keine Regel, keine Zusage.** Der Marker bedeutet unverändert „noch zu verifizieren".
- **Die dritte Restpunkt-Position bleibt offen.** Die Zeile „Umsetzung beim KI-Client" in
  `05-working-model.md` nennt weiterhin `~/.devin/plans/` und `subagent_explore`. Das ist keine
  Bezeichnungsfrage: Der Kern beschreibt dort, **was ein bestimmter Client kann** – das gehört in
  dessen Fähigkeitsmatrix und ist ein eigener Vorgang mit eigenem Umfang.

## 4. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Dateiname umbenennen? | **Ja**, zu `02-may-ai-do-task.md` – die Nachbardateien sind ebenfalls englisch benannt (`01-context-allowed`, `03-analyze-or-modify`) | Fünf Verweise; historische Dokumente nennen weiter den alten Namen, was beim Nachlesen einen Schritt kostet |
| E2 | Großform des Clientnamens pauschal verbieten? | **Nein** – `CLAUDE.md` ist ein Dateiname, `DEVIN_PROJECT_DIR` eine Umgebungsvariable. Nur **Platzhalter** werden erfasst | Eine Client-Bindung außerhalb eines Platzhalters und außerhalb der kapitalisierten Form bleibt unerkannt |
| E3 | Die Altform des Markers aus dem Register entfernen? | **Nein**, sie bleibt – mit dem Vermerk, dass sie nur im Client Pack zulässig ist. Das Register dokumentiert, was es gibt | Ein Leser könnte die Altform für gleichwertig halten; der Vermerk muss das tragen |

## 5. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | `<TBD: angenommen / abgelehnt / mit Auflagen>` |
| Datum | `<TBD>` |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | `<TBD: E1, E2 und E3 einzeln entscheiden>` |
