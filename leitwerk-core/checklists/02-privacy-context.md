# Checkliste FW-CL-02 – Datenschutz- und Kontextcheck

| Attribut | Wert |
|---|---|
| ID | `FW-CL-02` |
| Version | `0.1.3` |
| Status | `entwurf` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` in Abstimmung mit `<DATA_PROTECTION_CONTACT>` |
| Wann | im Preflight-Check und erneut vor jeder zusätzlichen Kontextbereitstellung in der Sitzung |
| Wer | Bearbeiterin oder Bearbeiter; bei K2-Freigaben `<APPROVAL_ROLE>` beziehungsweise `<DATA_PROTECTION_CONTACT>` |
| Dauer (Richtwert, Erläuterung) | wenige Minuten je Quelle – keine verbindlichen Aufwände |
| Nachweis | Kontextliste mit Klassen im Ergebnisbericht; K2-Freigaben mit Rolle und Datum |

## Zweck

Verhindert, dass unzulässige Inhalte (K3) oder nicht freigegebene Inhalte (K2) an den KI-Client gelangen (`leitwerk-core/framework/core/02-privacy.md`, `leitwerk-core/decision-trees/01-context-allowed.md`).

## Prüfpunkte

### Je Kontextquelle

- [ ] **MUSS** Kontextklasse bestimmt (K0/K1/K2/K3); ohne Einstufung gilt K3 und die Quelle wird nicht verwendet.
- [ ] **MUSS** K3-Kategorien geprüft: Secrets und Schlüsselmaterial; personenbezogene Echtdaten; Produktionsdaten; nicht freigegebene Kunden- oder Behördendokumente; Sicherheitskonfigurationen; interne Adressen, Hostnamen, Mandanten- und Umgebungskennungen; Inhalte anderer Projekte; als vertraulich eingestufte Inhalte.
- [ ] **MUSS** Mischinhalte tragen die höchste enthaltene Klasse, bis die höher eingestuften Bestandteile entfernt sind.
- [ ] **MUSS** Aufgabenbezug vorhanden: Die Quelle ist für genau diese Aufgabe erforderlich (Least Context, keine Pauschalfreigaben ganzer Ablagen).
- [ ] **SOLL** Aktualität geprüft; als `veraltet` markierte Dokumente werden nicht verwendet.

### K2-Inhalte (nur mit Freigabe)

- [ ] **MUSS** Freigabe vorhanden: Kategoriefreigabe im Overlay-Manifest oder Einzelfreigabe durch `<APPROVAL_ROLE>` (bei Personenbezug zusätzlich `<DATA_PROTECTION_CONTACT>`), mit Datum dokumentiert.
- [ ] **MUSS** Bereinigung durchgeführt: Personen → Rollen; Organisationen, Adressen, Kennungen → Platzhalter; Fallbeschreibungen abstrahiert.
- [ ] **MUSS** Tickets: nur Titel, technische Beschreibung, Akzeptanzkriterien; keine Kommentarverläufe, Anhänge, Screenshots, Kundenkommunikation.
- [ ] **MUSS** Logs und Stacktraces: personenbezogene Daten, Secrets, Hostnamen und Kennungen entfernt.
- [ ] **MUSS** Die bereinigte Fassung wird nicht in das Repository übernommen (Ebene E).

### Testdaten, Werkzeuge, geteilter Kontext

- [ ] **MUSS** Testdaten sind synthetisch und als solche erkennbar; keine Ableitung aus Echt- oder Produktionsdaten.
- [ ] **MUSS** Keine Websuche und kein Abruf externer Seiten. Eine Freigabe je Domain
      gibt es nicht (D-59); benötigte externe Quellen werden lokal bereitgestellt.
- [ ] **MUSS** MCP-Werkzeuge nur, wenn der Server im Overlay (Abschnitt 13) freigegeben ist; MCP-Bestätigungen bleiben auf `ask`.
- [ ] **MUSS** Geteilter Kontext (Spaces, parallele Sitzungen) enthält nur Inhalte, die für alle beteiligten Aufgaben freigegeben sind.
- [ ] **SOLL** Nutzerlokale Überschreibungen erweitern keine Kontextfreigaben.

## Abbruch- und Eskalationskriterien

Sind K3-Inhalte bereits an den KI-Client gelangt: sofort nach `leitwerk-core/framework/core/02-privacy.md` Abschnitt 5 verfahren (Sitzung beenden, Secrets rotieren lassen, Meldung an `<SECURITY_CONTACT>` und bei Personenbezug `<DATA_PROTECTION_CONTACT>`, Erfassung nach `leitwerk-core/governance/INCIDENT_HANDLING.md`) – Eskalationsstufe E3 (`leitwerk-core/framework/core/10-error-escalation.md`). Fehlende K2-Freigabe: Quelle nicht verwenden, gegebenenfalls Freigabe anfordern (E1).

## Ergebnis und Nachweis

Liste der verwendeten Quellen mit Klasse und – bei K2 – Freigabe (Rolle, Datum, Bereinigung) im Ergebnisbericht; Reviewer prüfen die Liste stichprobenartig (RV-Stichprobe nach `leitwerk-core/framework/core/02-privacy.md` Abschnitt 4 Schritt 5).
