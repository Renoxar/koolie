# KI-Nutzungsvermerk für Merge Requests – Vorlage

<!-- Verwendung: Abschnitt in jeder Merge-Request-Beschreibung, an der ein KI-Werkzeug beteiligt war
     (Framework Core 04, Q5; 09-risk-model Dokumentationsumfang). Kurzform für Stufe niedrig,
     Langform ab Stufe mittel. Der Vermerk enthält keine Personen, keine Prompts mit K2/K3-Inhalten,
     keine internen Adressen. Er dient der Nachvollziehbarkeit und der Pilotauswertung.
     Beide Fassungen nennen die Framework- und die Overlay-Version: Sie sind die ersten beiden
     Glieder der Nachweiskette (RELEASE_PROCESS 8). Ohne sie trägt der Merge Request bei
     Kontrollstufe niedrig keine Versionsangabe, die sich je ändert (FW-VN-01). -->

## Kurzform (Kontrollstufe niedrig)

```markdown
### KI-Unterstützung
- Kontrollstufe: niedrig (Faktor <R#>) · Betriebsmodus: <M#>
- Framework-Version: <Inhalt der Datei leitwerk-core/VERSION> · Overlay-Version: <Version>
- Verwendete Skills: <fw-... vVersion, ...>
- Verwendeter Kontext: <Pfade / Dokumente, nur K0/K1>
- Selbstreview nach leitwerk-core/checklists/04-review-ai-code.md: durchgeführt
- Verworfene Vorschläge: <keine / Anzahl mit Stichwort>
```

## Langform (Kontrollstufe mittel und hoch)

```markdown
### KI-Unterstützung
- Kontrollstufe: <mittel / hoch> (Faktor <R#>) · Betriebsmodus: <M#>
- Framework-Version: <Inhalt der Datei leitwerk-core/VERSION> · Overlay-Version: <Version>
- Verwendete Skills: <fw-... vVersion, ...>
- Verwendeter Kontext: <Pfade / Dokumente mit Kontextklasse; K2-Freigabe: <Rolle, Datum>>
- Bestätigter Plan: <Referenz / Anhang> · Abweichungen vom Plan: <keine / Liste>
- Ausgeführte Befehle: <Liste mit Ergebnis>
- Ergebnisbericht: <Referenz / Anhang>
- Freigabe Stufe hoch: <Rolle, Datum, Referenz> (nur Stufe hoch)
- Restrisiken und empfohlene Prüfungen: <Liste>
- Verworfene Vorschläge: <Anzahl mit Stichwort>
```
