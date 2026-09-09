# Devin-Nutzungsvermerk für Merge Requests – Vorlage

<!-- Verwendung: Abschnitt in jeder Merge-Request-Beschreibung, bei der Devin beteiligt war
     (Framework Core 04, Q5; 09-risk-model Dokumentationsumfang). Kurzform für Stufe niedrig,
     Langform ab Stufe mittel. Der Vermerk enthält keine Personen, keine Prompts mit K2/K3-Inhalten,
     keine internen Adressen. Er dient der Nachvollziehbarkeit und der Pilotauswertung. -->

## Kurzform (Kontrollstufe niedrig)

```markdown
### KI-Unterstützung (Devin Desktop)
- Kontrollstufe: niedrig (Faktor <R#>) · Betriebsmodus: <M#>
- Verwendete Skills: <fw-... vVersion, ...>
- Verwendeter Kontext: <Pfade / Dokumente, nur K0/K1>
- Selbstreview nach devin-core-framework/checklists/04-review-ai-code.md: durchgeführt
- Verworfene Vorschläge: <keine / Anzahl mit Stichwort>
```

## Langform (Kontrollstufe mittel und hoch)

```markdown
### KI-Unterstützung (Devin Desktop)
- Kontrollstufe: <mittel / hoch> (Faktor <R#>) · Betriebsmodus: <M#>
- Framework-Version: <Inhalt der Datei devin-core-framework/VERSION> · Overlay-Version: <Version>
- Verwendete Skills: <fw-... vVersion, ...>
- Verwendeter Kontext: <Pfade / Dokumente mit Kontextklasse; K2-Freigabe: <Rolle, Datum>>
- Bestätigter Plan: <Referenz / Anhang> · Abweichungen vom Plan: <keine / Liste>
- Ausgeführte Befehle: <Liste mit Ergebnis>
- Ergebnisbericht: <Referenz / Anhang>
- Freigabe Stufe hoch: <Rolle, Datum, Referenz> (nur Stufe hoch)
- Restrisiken und empfohlene Prüfungen: <Liste>
- Verworfene Vorschläge: <Anzahl mit Stichwort>
```
