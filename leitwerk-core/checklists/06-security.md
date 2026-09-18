# Checkliste FW-CL-06 – Security

| Attribut | Wert |
|---|---|
| ID | `FW-CL-06` |
| Version | `0.1.2` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` in Abstimmung mit `<SECURITY_CONTACT>` |
| Wann | bei jeder Änderung mit R3-, R10- oder R11-Bezug; ergänzend zum Review bei Stufe hoch; stichprobenartig bei Stufe mittel |
| Wer | Bearbeiterin oder Bearbeiter; bei Stufe hoch zusätzlich `<SECURITY_CONTACT>` |
| Dauer (Richtwert, Erläuterung) | abhängig vom Umfang – keine verbindlichen Aufwände |
| Nachweis | Security-Abschnitt im Ergebnisbericht und im KI-Nutzungsvermerk (Langform) |

## Zweck

Operationalisiert das Sicherheitsmodell (`leitwerk-core/framework/core/03-security.md`) für Änderungen mit Sicherheitsbezug und für die Prüfung KI-typischer Schwächen (T2, T4, T5, T6).

## Prüfpunkte

### Einstufung und Prozess

- [ ] **MUSS** Berührung von Authentifizierung, Autorisierung, Sitzungsverwaltung oder Kryptografie **in der Anwendungslogik** erkannt → Kontrollstufe hoch, Umsetzung nur mit Freigabe `<APPROVAL_ROLE>` und `<SECURITY_CONTACT>` (R3/R10).
- [ ] **MUSS** Berührung tatsächlicher Berechtigungen oder einer Betriebs-, Infrastruktur- oder Sicherheitskonfiguration erkannt → **V6, nicht delegierbar, auch nicht nach Freigabe**; zulässig sind Analyse und Planvorschlag. Das gilt auch für Sicherheitskonfiguration als Code im Repositorium – ihr Inhalt **ist** die Berechtigung (D-53, Grenzfälle G-05 und G-06).
- [ ] **MUSS** Security Scans und statische Analyse der CI sind für den Änderungssatz erfolgreich (P6); Schwellenwerte unverändert (T6).

### Code-Prüfpunkte (soweit für die Änderung relevant)

- [ ] **MUSS** Eingaben an Systemgrenzen werden validiert (Länge, Typ, Wertebereich, Kodierung); Validierung liegt auf der Serverseite beziehungsweise der vertrauenswürdigen Seite.
- [ ] **MUSS** Autorisierung wird in jedem neuen oder geänderten Pfad geprüft (nicht nur in der Oberfläche); keine unbeabsichtigte Rechteausweitung.
- [ ] **MUSS** Keine Injection-Vektoren: parametrisierte Abfragen, kein String-Zusammenbau für Interpreter (SQL, Shell, Pfade, Ausdrücke), sichere Deserialisierung, kein ungeprüftes Laden von Ressourcen über Nutzereingaben.
- [ ] **MUSS** Keine hartcodierten Geheimnisse, Schlüssel oder Zugangsdaten; Konfiguration über die vorgesehenen Mechanismen des Projekts.
- [ ] **MUSS** Logging ohne personenbezogene Daten, Geheimnisse oder Sitzungsartefakte; Fehlermeldungen nach außen ohne Stacktraces, Pfade oder Versionsinterna.
- [ ] **MUSS** Kryptografie nur über die im Projekt freigegebenen Bibliotheken und Verfahren; keine Eigenbauten, keine veralteten Algorithmen; Zufall aus kryptografisch geeigneten Quellen.
- [ ] **SOLL** Ressourcen- und Fehlerpfade geschlossen (Timeouts, Freigabe von Handles, kein „fail open" bei Sicherheitsprüfungen).
- [ ] **SOLL** Sichere Standardwerte: neue Konfigurationsschalter sind restriktiv voreingestellt (P9).

### KI-spezifische Prüfpunkte

- [ ] **MUSS** Ergebnisbericht auf gemeldete Injektionsversuche geprüft (T2); Meldungen sind an `<SECURITY_CONTACT>` weitergegeben.
- [ ] **MUSS** Abhängigkeiten unverändert; vorgeschlagene neue Abhängigkeiten laufen über `leitwerk-core/checklists/07-new-dependency.md` (T4); Paketnamen exakt gegen die Quelle geprüft (halluzinierte Namen, Typosquatting).
- [ ] **MUSS** Sicherheitsrelevante Aussagen des Vorschlags („validiert", „escaped", „konstant-zeitlich") sind belegt (Fundstelle, Test) und nicht nur behauptet (Q7).
- [ ] **SOLL** Diff auf entfernte oder umgangene bestehende Sicherheitsprüfungen durchgesehen (auch „vereinfachte" Varianten).

## Abbruch- und Eskalationskriterien

Fund von Secrets oder personenbezogenen Echtdaten: S3/E3 (`leitwerk-core/framework/core/10-error-escalation.md`, `leitwerk-core/framework/core/02-privacy.md` Abschnitt 5). Verdacht auf ausgenutzte Schwachstelle oder Datenabfluss: V9 – keine eigenständige Weiterarbeit, Meldeweg der Organisation. Unaufgelöste MUSS-Punkte blockieren den Merge.

## Ergebnis und Nachweis

Beantwortete Prüfpunkte mit Fundstellen im Security-Abschnitt des Ergebnisberichts; bei Stufe hoch Gegenzeichnung durch `<SECURITY_CONTACT>` im Merge Request.
