# Änderungsantrag `CR-2026-001`

| Feld | Inhalt |
|---|---|
| Titel | Definition des Release 1.0.0: technische Validierung statt Pilotauswertung |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | `devin-core-framework/governance/DECISION_LOG.md` (D-09), `devin-core-framework/docs/ROADMAP.md` (AP8–AP13), `devin-core-framework/checklists/11-framework-release.md`, `devin-core-framework/CHANGELOG.md` |
| Ebene laut Entscheidungsbaum 6 | Core (Governance) |
| Art | Änderung |
| Dringlichkeit | regulär (Review-Zyklus) |

## 1. Anlass und Problem

D-09 legt fest: „Version 1.0.0 erst nach Pilotauswertung". Die Roadmap setzt das um, indem AP12 (Release 1.0) von AP11 → AP10 → AP9 (Pilot) → AP8 (Onboarding) abhängt. Der Pilot nach `devin-core-framework/pilot/PILOT_CONCEPT.md` setzt eine Pilotgruppe, eine Mentorenrolle, einen `<ISSUE_TRACKER>` mit Etikettierung sowie die Rollen `<SECURITY_CONTACT>`, `<DATA_PROTECTION_CONTACT>` und `<APPROVAL_ROLE>` voraus.

Diese Voraussetzungen sind Eigenschaften einer **aufnehmenden Organisation**, nicht des Frameworks. Solange keine solche Organisation benannt ist, ist AP12 strukturell nicht erreichbar: Die Release-Checkliste `FW-CL-11` enthält MUSS-Punkte, die ohne diese Rollen nicht abhakbar sind. Das Framework kann damit dauerhaft keinen verbindlichen Stand erklären — obwohl seine inhaltliche Substanz vollständig ist und die verbleibenden Lücken ausschließlich Nachweise betreffen (52 offene VERIFY-Marker, 35 Testfälle mit Ergebnisstatus `offen`, Modulstatus durchweg `entwurf`).

Zweitens vermischt D-09 zwei verschiedene Aussagen: „das Framework ist als Artefakt belastbar" und „das Framework hat sich im Realbetrieb einer Organisation bewährt". Die zweite Aussage kann ein Framework über sich selbst nicht treffen; sie entsteht projektseitig. Die Kopplung macht die erste Aussage unerreichbar, ohne die zweite belastbarer zu machen.

## 2. Vorgeschlagene Änderung

**D-09 wird durch D-11 ersetzt.** Neue Definition:

> Version 1.0.0 bezeichnet den Stand, in dem das Framework **technisch validiert und übertragbar** ist. Kriterien:
>
> 1. Alle produktbezogenen Aussagen sind gegen eine reale Installation des jeweiligen KI-Clients belegt; kein VERIFY-Marker ist unbearbeitet (jeder ist bestätigt, korrigiert oder in einen Änderungsantrag überführt).
> 2. Der Testkatalog `devin-core-framework/tests/TEST_CATALOG.md` ist vollständig ausgeführt und protokolliert; kein Testfall steht auf `offen`.
> 3. Alle Core-Module, Skills und Packs haben einen Status oberhalb von `entwurf`.
> 4. Die Strukturentscheidungen D-01…D-10 sind bestätigt oder ersetzt; kein Decision Record trägt mehr den Status `entschieden (Vorschlag)`.
> 5. Die Übernahme in mindestens ein zweites Projekt ist nach `devin-core-framework/checklists/10-project-adoption.md` nachgewiesen.
>
> **Pilot, Onboarding und organisatorische Freigabe (AP8, AP9, AP10) sind nicht Vorbedingung für 1.0.0.** Sie sind Aufgaben der aufnehmenden Organisation und in `devin-core-framework/docs/ADOPTION_GUIDE.md` sowie `devin-core-framework/checklists/10-project-adoption.md` geregelt. Ein Release 1.0.0 erklärt ausdrücklich **nicht**, dass das Framework in einem Realbetrieb erprobt wurde.

**Roadmap:** AP12 hängt künftig an AP11, AP11 an AP7. AP8, AP9, AP10 werden als projektseitige Arbeitspakete gekennzeichnet und der Übernahme (AP13) zugeordnet. Die Priorität von AP8–AP10 sinkt auf P3.

**Release-Checkliste FW-CL-11:** Der Abschnitt „Tests" wird um den MUSS-Punkt „kein Testfall mit Ergebnisstatus `offen`" ergänzt; der Abschnitt „Abschluss" um „Modulstatus oberhalb `entwurf`" und „keine Decision Records im Status `entschieden (Vorschlag)`". Die bestehenden MUSS-Punkte, die eine Pilotgruppe voraussetzen, entfallen für 1.0.0.

## 3. Prüffragen (durch Owner auszufüllen)

- [x] Richtige Ebene nach Entscheidungsbaum 6? — Ja, Governance ist Core.
- [x] Verschärfungsprinzip eingehalten? — Ja. Die Änderung berührt keine der Ebenen V1–V12 und keine Kontextklasse; sie lockert keine Verhaltensregel, sondern definiert ein Release-Kriterium neu. Die Kriterien 1–5 sind gegenüber D-09 in der Sache **strenger** formuliert (D-09 nannte keine prüfbaren Schwellen).
- [x] Widerspruchsfreiheit geprüft? — Gelesen: `PILOT_CONCEPT.md`, `RELEASE_PROCESS.md`, `ADOPTION_GUIDE.md`, `10-project-adoption.md`, `11-framework-release.md`, `ROADMAP.md`. Widerspruch bestand nur zwischen D-09 und der Erreichbarkeit von FW-CL-11; er wird durch diesen Antrag aufgelöst.
- [x] Laufzeitfassungen betroffen? — Nein. `AGENTS.md`, `.devin/rules/*` und `.devin/config.json` enthalten keine Release-Definition.
- [x] Belegstatus korrekt? — Keine produktbezogene Aussage betroffen.
- [x] Test- und Validierungsbedarf? — Keine neue Testkatalog-ID. Kriterium 2 macht den bestehenden Katalog zum Release-Gate.
- [x] Auswirkungen auf Overlays und laufende Onboardings? — Keine. Kein Overlay-Feld und kein Onboarding-Schritt referenziert D-09.
- [x] Dokumentation? — CHANGELOG, Decision Log (D-09 ersetzt, D-11 neu), ROADMAP, FW-CL-11.

## 4. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | angenommen |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Die bisherige Definition koppelt die Aussagefähigkeit des Frameworks an Voraussetzungen, die außerhalb seines Verantwortungsbereichs liegen, und macht das Release-Gate dadurch unerreichbar. Die neue Definition ist prüfbar, liegt vollständig im Einflussbereich des Framework Owners und trennt die Aussage „belastbares Artefakt" sauber von der Aussage „im Realbetrieb erprobt". |
| Ziel-Release | 0.5.0 |
| Decision-Log-Eintrag | D-11 |

## 5. Umsetzung (nach Annahme)

- [x] Decision Log: D-09 als ersetzt gekennzeichnet, D-11 ergänzt
- [x] ROADMAP: AP8–AP13 neu zugeordnet, Abhängigkeitsgraph angepasst
- [x] FW-CL-11: Prüfpunkte angepasst
- [x] CHANGELOG: Abschnitt „Unveröffentlicht" ergänzt
- [ ] Validator ohne Fehler; betroffene Tests ausgeführt
- [ ] Kommunikation an Projekte — entfällt, da bislang nur das Übungsrepository aufgenommen hat
