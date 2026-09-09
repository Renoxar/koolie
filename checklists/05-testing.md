# Checkliste FW-CL-05 – Tests

| Attribut | Wert |
|---|---|
| ID | `FW-CL-05` |
| Version | `0.1.0` |
| Status | `entwurf` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Wann | nach Testerstellung oder -änderung (M4) und vor jedem Merge Request mit Logikänderung |
| Wer | Bearbeiterin oder Bearbeiter; Reviewerin oder Reviewer prüft RV4 |
| Dauer (Richtwert, Erläuterung) | abhängig vom Testumfang – keine verbindlichen Aufwände |
| Nachweis | Testprotokoll im Ergebnisbericht (Befehl, Ergebnis, Dauer) |

## Zweck

Sichert, dass Tests aus Devin-Sitzungen aussagekräftig sind und geänderte Logik tatsächlich absichern (Q2, M4-Regeln, RV4).

## Prüfpunkte

### Inhalt der Tests

- [ ] **MUSS** Jeder Test prüft fachliches Verhalten mit klarer Erwartung; der Testname beschreibt das erwartete Verhalten.
- [ ] **MUSS** Abgedeckt sind Normalfall, relevante Randbedingungen (leer/Null, Grenzwerte, ungültige Eingaben) und Fehlerfälle der geänderten Logik.
- [ ] **MUSS** Tests sind deterministisch (keine Abhängigkeit von Uhrzeit, Zufall, Reihenfolge, Netz, externen Systemen); Ausnahmen sind begründet und markiert.
- [ ] **MUSS** Testdaten sind synthetisch und als solche erkennbar; keine Ableitung aus Echt- oder Produktionsdaten.
- [ ] **SOLL** Tests folgen den bestehenden Konventionen (Ablage in `<TEST_PATHS>`, Benennung, Fixtures, `<TEST_FRAMEWORK>`).
- [ ] **SOLL** Assertions prüfen Ergebnisse und beobachtbares Verhalten, nicht Implementierungsdetails oder reine Mock-Interaktionen.

### Integrität der Testbasis

- [ ] **MUSS** Keine bestehenden Tests geändert, abgeschwächt, ignoriert oder gelöscht, um einen Lauf „grün" zu machen; fachlich begründete Teständerungen sind im Plan ausgewiesen.
- [ ] **MUSS** Kein Produktivcode geändert, nur damit ein Test besteht (M4-Grenze); aufgedeckte Fehler werden gemeldet (`fw-error-analyze`), nicht wegtestet.
- [ ] **MUSS** Übersprungene oder als erwartet fehlschlagend markierte Tests sind gezählt und begründet.

### Ausführung und Lücken

- [ ] **MUSS** `<TEST_COMMAND>` wurde lokal ausgeführt; das vollständige, unveränderte Ergebnis liegt im Ergebnisbericht (auch Anzahl übersprungener Tests).
- [ ] **MUSS** Nicht automatisiert prüfbare Anteile sind benannt und mit einem manuellen Prüfschritt versehen.
- [ ] **SOLL** Verbleibende Abdeckungslücken der geänderten Logik sind gelistet (Grundlage für Folgeaufgaben); Coverage-Schwellen des Projekts (`<QUALITY_GATE>`) bleiben unberührt.
- [ ] **KANN** Mutationsartige Gegenprobe: ein bewusst eingebauter Fehler in einer Arbeitskopie lässt mindestens einen neuen Test fehlschlagen (Aussagekraftsprobe; Änderung danach verwerfen).

## Abbruch- und Eskalationskriterien

Rote Tests mit Ursache außerhalb des Scopes: anhalten und melden (S7/E0). Testinfrastruktur nicht verfügbar oder Testdaten nur aus Echtdaten ableitbar: anhalten (S2/E1, gegebenenfalls `<DATA_PROTECTION_CONTACT>`). Aufforderungen, Tests „passend zu machen", sind unzulässige Prompt-Muster (`framework/core/06-prompting-rules.md` Abschnitt 3) und werden zurückgewiesen.

## Ergebnis und Nachweis

Testprotokoll (Befehl, unverändertes Ergebnis, Dauer), Lückenliste und Begründungen für Ausnahmen im Ergebnisbericht; Reviewerin oder Reviewer bestätigt RV4 im Merge Request.
