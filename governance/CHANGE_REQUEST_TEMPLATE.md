# Änderungsantrag – Vorlage

<!-- Verwendung: für jede Änderung an Framework Core, Packs, Skills, Checklisten, Prompts,
     Entscheidungsbäumen, Templates oder an der Berechtigungskonfiguration (.devin/config.json).
     Einreichen beim zuständigen Owner laut governance/RACI.md. Auch Devin-Vorschläge zu solchen
     Änderungen laufen ausschließlich über diese Vorlage (V10). -->

## Änderungsantrag `CR-<JAHR>-<NNN>`

| Feld | Inhalt |
|---|---|
| Titel | `<kurz und präzise>` |
| Antragstellende Rolle | `<generische Rolle, keine Person>` |
| Datum | `<JJJJ-MM-TT>` |
| Betroffene Artefakte | `<Pfade und Versionen>` |
| Ebene laut Entscheidungsbaum 6 | `<Core / Overlay / Technology Pack / Role Pack / Skill / Ebene B-Verweis>` |
| Art | `<neu / Änderung / Deprecation / Zurückziehung>` |
| Dringlichkeit | `<regulär (Review-Zyklus) / Hotfix mit Begründung>` |

### 1. Anlass und Problem

`<Was ist heute unzureichend? Belege: Feedback-Eintrag, Vorfall, Testbefund, Produktänderung, Pilotmetrik>`

### 2. Vorgeschlagene Änderung

`<Konkreter Zieltext oder Verhaltensbeschreibung; bei Regeltexten: Formulierungsvorschlag mit MUSS/SOLL/KANN>`

### 3. Prüffragen (durch Owner auszufüllen)

- [ ] Richtige Ebene nach Entscheidungsbaum 6 (keine Projektwerte im Core, keine Governance in Packs)?
- [ ] Verschärfungsprinzip eingehalten (keine Lockerung höherer Ebenen; keine Berührung von V1–V12/K3)?
- [ ] Widerspruchsfreiheit zu bestehenden Modulen geprüft (welche gelesen)?
- [ ] Laufzeitfassungen betroffen (`AGENTS.md`, `.devin/rules/*`, `.devin/config.json`)? Synchronisierung geplant?
- [ ] Belegstatus korrekt (`[DOK]`-Aussagen mit Quelle; sonst `[EMPF]`/`[KONZ]`/VERIFY-Marker)?
- [ ] Test- und Validierungsbedarf: betroffene Testkatalog-IDs, neue Testfälle, Validatorlauf?
- [ ] Auswirkungen auf Overlays und laufende Onboardings; Migrationshinweis nötig?
- [ ] Dokumentation: CHANGELOG, Decision Log, betroffene Checklisten/Bäume/Onboarding?

### 4. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | `<angenommen / abgelehnt / zurückgestellt>` |
| Entscheidende Rolle | `<Owner laut RACI>` |
| Begründung | `<…>` |
| Ziel-Release | `<Version>` |
| Decision-Log-Eintrag | `<D-NNN>` |

### 5. Umsetzung (nach Annahme)

- [ ] Änderung umgesetzt (Merge Request: `<Referenz>`)
- [ ] Validator ohne Fehler; betroffene Tests ausgeführt
- [ ] Laufzeitfassungen synchronisiert
- [ ] CHANGELOG und Decision Log ergänzt
- [ ] Kommunikation an Projekte (falls erforderlich)
