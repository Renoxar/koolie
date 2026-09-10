# Checkliste FW-CL-10 – Projektübernahme

| Attribut | Wert |
|---|---|
| ID | `FW-CL-10` |
| Version | `0.1.0` |
| Status | `entwurf` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Wann | bei Übernahme des Frameworks in ein neues Projekt, vor dem Setzen des Overlay-Status auf `aktiv` |
| Wer | Overlay Owner (`<APPROVAL_ROLE>`) mit Framework Owner; Beteiligung `<SECURITY_CONTACT>` und `<DATA_PROTECTION_CONTACT>` |
| Dauer (Richtwert, Erläuterung) | verteilt über die Einführungsphase – keine verbindlichen Aufwände |
| Nachweis | ausgefüllte Checkliste als Anlage zur Overlay-Aktivierung; Eintrag im Overlay-Änderungsverlauf |

## Zweck

Stellt sicher, dass ein neues Projekt das Framework vollständig, unverändert im Core und mit ausgefülltem Overlay übernimmt (`leitwerk-core/docs/ADOPTION_GUIDE.md`; Grundsatz: Ein Projektwechsel betrifft nur Ebene 4).

## Prüfpunkte

### Voraussetzungen der Organisation

- [ ] **MUSS** Freigabe der Devin-Nutzung durch die Organisation liegt vor (Referenz im Overlay Abschnitt 1).
- [ ] **MUSS** Ergebnis der Datenschutz- und Vertragsprüfung liegt vor und ist im Overlay referenziert (K-06; ohne Ergebnis bleibt die restriktivste Auslegung nach `leitwerk-core/framework/core/02-privacy.md` Abschnitt 1.3).
- [ ] **MUSS** Planstufe und administrativ erzwungene Team-Einstellungen sind dokumentiert (`leitwerk-core/framework/org-policies/`, K-05); Training-Opt-out beziehungsweise vertragliche Regelung nachgewiesen (`<TBD: Nachweis der Einstellung>`).
- [ ] **SOLL** Abbildung des Klassifizierungsschemas der Organisation auf K0–K3 liegt vor (`leitwerk-core/framework/org-policies/MAPPING_CLASSIFICATION.md`).

### Technische Integration

- [ ] **MUSS** Framework-Release in das Projekt-Repository integriert (Wurzel-Anweisungsdatei, Laufzeitschicht, `leitwerk-core/framework/`, `templates/`, `leitwerk-core/checklists/`, `leitwerk-core/decision-trees/`, `leitwerk-core/prompts/`, `leitwerk-core/onboarding/`, `tests/`); Framework-Version **und gewähltes Client Pack** im Overlay notiert.
- [ ] **MUSS** Core-Dateien unverändert (Abgleich gegen das Release-Archiv; Änderungsbedarf läuft als Änderungsantrag an den Framework Owner, nie als lokale Änderung).
- [ ] **MUSS** `project-overlay/OVERLAY.md` vollständig ausgefüllt; sicherheitsrelevante Abschnitte 4, 5, 6, 13, 14, 15 ohne offene `<TBD>`.
- [ ] **MUSS** `20-project-overlay.md` in der Regelablage synchron zur Overlay-Datei befüllt (bei Clients mit Zeichenlimit unter 6.000 Zeichen).
- [ ] **MUSS** Berechtigungsdatei mit den Overlay-Werten befüllt (`<ALLOWED_PATHS>`, `<EXCLUDED_PATHS>`, Befehle, CI-/Gate-Pfade); alle Kernregeln aus `_core_rules_integrity` unverändert enthalten.
- [ ] **MUSS** `project-overlay/overlay-manifest.yaml` gepflegt; eingebundene Dokumente bereinigt und freigegeben; nicht registrierte Dokumente gelten als K3.
- [ ] **MUSS** Benötigte Role Packs und Technology Packs aktiviert (Laufzeitfassungen `30-*`, `40-*` erstellt); nicht benötigte nicht geladen.
- [ ] **MUSS** `project-overlay/forbidden-terms.txt` projektlokal mit den realen Namen des Projekts befüllt (Datei verbleibt projektlokal).
- [ ] **MUSS** `python3 leitwerk-core/tests/scripts/validate-framework.py --strict-overlay` läuft ohne Fehler.

### Organisation im Projekt

- [ ] **MUSS** Rollen zugeordnet (außerhalb des Repositorys): Overlay Owner, `<SECURITY_CONTACT>`, `<DATA_PROTECTION_CONTACT>`, `<PRODUCT_OWNER_ROLE>`, `<ARCHITECT_ROLE>`, Mentorinnen und Mentoren.
- [ ] **MUSS** Eskalationswege (Overlay Abschnitt 16) mit erreichbaren Kanälen hinterlegt.
- [ ] **MUSS** Basistests des Testkatalogs auf dem Übungsrepository ausgeführt (mindestens die Klassen PI, DS, SC aus `leitwerk-core/tests/TEST_CATALOG.md`); Ergebnisse dokumentiert.
- [ ] **MUSS** Onboarding für die ersten Nutzerinnen und Nutzer geplant (`leitwerk-core/checklists/09-onboarding.md`); bis zur Freigabe arbeiten alle begleitet.
- [ ] **SOLL** Pilotparameter festgelegt (`leitwerk-core/pilot/PILOT_CONCEPT.md`: Referenzbasis, Pilotgruppe, `<PILOT_DURATION>`, Anwendungsfälle, Review-Punkte).
- [ ] **SOLL** Ablageorte für Ergebnisberichte und Pläne bestimmt (`<TBD: Ablageort für Ergebnisberichte>`, `<TBD: Ablage von Plänen im Projekt>`).

### Aktivierung

- [ ] **MUSS** Overlay-Status in OVERLAY.md und `20-project-overlay.md` auf `aktiv` gesetzt; Version und Datum im Overlay-Änderungsverlauf; diese Checkliste als Nachweis abgelegt.

## Abbruch- und Eskalationskriterien

Fehlende Organisationsfreigabe oder Datenschutzprüfung stoppt die Übernahme (E2/E3-Vorstufe). Änderungsbedarf am Core, der die Übernahme blockiert, geht als Änderungsantrag an den Framework Owner (E4) – das Projekt wartet auf ein Release oder eine dokumentierte Ausnahme.

## Ergebnis und Nachweis

Vollständig abgehakte Liste mit Referenzen (Freigaben, Validierungslauf, Testkatalog-Ergebnisse) als Anlage der Overlay-Aktivierung; Eintrag im Overlay-Änderungsverlauf und Meldung an den Framework Owner (Bestandsliste der Projekte).
