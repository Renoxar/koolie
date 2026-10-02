# Entscheidungsbaum 3 – Muss der KI-Client nur analysieren oder darf der KI-Client ändern?

| Attribut | Wert |
|---|---|
| ID | `FW-DT-03` |
| Version | `0.1.4` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Anwendung | im Preflight nach Baum 2; wählt den Betriebsmodus M1–M6 |
| Quelle | `.koolie/core/framework/core/05-working-model.md`, `.koolie/core/framework/core/09-risk-model.md` |

## Textbeschreibung (normativ)

1. **Nur Verstehen oder Befund?** Soll ausschließlich verstanden, erklärt, geprüft oder bewertet werden (kein Artefakt im Repository ändert sich)? → **M1 Read-only Analysis** (Skills `koolie-repo-analyze`, `koolie-code-explain`, `koolie-change-analyze`, `koolie-error-analyze`, `koolie-review-support`).
2. **Plan gesucht?** Soll ein Vorgehen oder Änderungsplan entstehen, aber noch nichts umgesetzt werden? → **M2 Guided Planning** (`koolie-plan`, `koolie-bugfix-prepare`). M2 ist Pflichtstation vor M3 ab Kontrollstufe mittel; M4 und M5 folgen `09-risk-model.md` Abschnitt 3.
3. **Nur Tests?** Sollen ausschließlich Tests erstellt, erweitert oder ausgeführt werden (`<TEST_PATHS>`)? → **M4 Test and Validation** (`koolie-tests`). Stellt sich heraus, dass Produktivcode geändert werden müsste, wird angehalten und über M2/M3 neu entschieden.
4. **Nur Dokumentation?** Sollen ausschließlich Dokumente in `<DOC_PATHS>` entstehen oder aktualisiert werden? → **M5 Documentation Support** (`koolie-docs-update`, `koolie-mr-description`).
5. **Eine Entscheidung des Menschen in Overlay oder Projektdokumentation eintragen?** Hat der Mensch über Architektur, Overlay-Werte oder Projektdokumente entschieden und soll der KI-Client sie eintragen? → **M6 Mandated Maintenance** (`koolie-overlay-pflege`) – nur mit Mandat (`python .koolie/core/mandat.py erteilen …`, der Mensch im eigenen Terminal). Ohne Mandat: Blockade-Hinweis. Ist noch nicht entschieden → M1/M2.
6. **Produktivcode ändern?** → **M3 Controlled Modification** (`koolie-change-small`, `koolie-refactor`) – nur wenn die Stufenvoraussetzungen erfüllt sind: niedrig mit klar abgegrenzter Aufgabe; mittel mit bestätigtem Plan; hoch mit dokumentierter Freigabe und Begleitung. Sind sie nicht erfüllt → zurück zu M1/M2.
7. **Gemischte Aufgaben** werden zerlegt: erst M1/M2, dann je ein Modus je Sitzung (Q1, P7). Ein Moduswechsel innerhalb einer Sitzung erfordert eine ausdrückliche Anweisung und wird im Ergebnisbericht vermerkt.
8. **Ohne Angabe gilt M1** (Wurzel-Anweisungsdatei, Abschnitt 17).

## Diagramm

```mermaid
flowchart TD
    A["Aufgabe ist delegierbar<br/>(Ergebnis aus Baum 2)"] --> B{"Nur verstehen, erklären,<br/>prüfen oder bewerten?"}
    B -- "ja" --> M1["M1 Read-only Analysis<br/>koolie-repo-analyze, koolie-code-explain,<br/>koolie-change-analyze, koolie-error-analyze,<br/>koolie-review-support"]
    B -- "nein" --> C{"Soll zunächst nur ein<br/>Plan entstehen?"}
    C -- "ja" --> M2["M2 Guided Planning<br/>koolie-plan, koolie-bugfix-prepare<br/>Pflicht vor M3 ab Stufe mittel"]
    C -- "nein" --> D{"Was wird geändert?"}
    D -- "nur Tests in TEST_PATHS" --> M4["M4 Test and Validation<br/>koolie-tests"]
    D -- "nur Doku in DOC_PATHS" --> M5["M5 Documentation Support<br/>koolie-docs-update, koolie-mr-description"]
    D -- "Entscheidung ins Overlay eintragen" --> M6{"Mandat des Menschen<br/>vorhanden?"}
    M6 -- "ja" --> M6J["M6 Mandated Maintenance<br/>koolie-overlay-pflege"]
    M6 -- "nein" --> BH["Blockade-Hinweis:<br/>mandat.py erteilen"]
    D -- "Produktivcode" --> E{"Stufenvoraussetzungen erfüllt?<br/>niedrig: klar abgegrenzt<br/>mittel: bestätigter Plan<br/>hoch: Freigabe + Begleitung"}
    E -- "nein" --> Z["Zurück zu M1/M2"]
    Z --> M1
    Z --> M2
    E -- "ja" --> M3["M3 Controlled Modification<br/>koolie-change-small, koolie-refactor"]
    M4 --> F{"Produktivcode-Änderung<br/>nötig?"}
    F -- "ja" --> HALT["Anhalten:<br/>neu entscheiden über M2/M3"]
    F -- "nein" --> OK["Fortfahren"]
```

## Hinweise

- M2 schreibt nur die Plan-Datei außerhalb des Quellcodes; M4 und M5 schreiben nur in ihren Pfaden – alles Weitere ist ein Modusbruch und wird gemeldet (S4).
- Wer unsicher ist, beginnt mit M1: Eine Analyse zu viel kostet Minuten, eine Änderung zu früh kostet ein Review.
