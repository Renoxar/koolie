# Checkliste FW-CL-07 – Neue Abhängigkeiten

| Attribut | Wert |
|---|---|
| ID | `FW-CL-07` |
| Version | `0.1.2` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` in Abstimmung mit `<SECURITY_CONTACT>` |
| Wann | bevor eine neue Abhängigkeit oder ein Major-Update eingeführt wird (auch nach einem KI-Vorschlag) |
| Wer | Bearbeiterin oder Bearbeiter; Freigabe `<APPROVAL_ROLE>`, bei Sicherheitsrelevanz `<SECURITY_CONTACT>` |
| Dauer (Richtwert, Erläuterung) | abhängig von der Bibliothek – keine verbindlichen Aufwände |
| Nachweis | ausgefüllte Prüfpunkte im Ticket oder Merge Request; Eintrag der Freigabe |

## Zweck

Abhängigkeiten sind Kontrollstufe hoch (R9) und ihre Einführung ist nicht delegierbar (V3). Diese Liste strukturiert die menschliche Entscheidung nach einem KI-Vorschlag (T4: halluzinierte Pakete, Typosquatting, Lizenzrisiken).

## Prüfpunkte

### Bedarf

- [ ] **MUSS** Der Bedarf ist fachlich begründet; eine Umsetzung mit Bordmitteln des Projekts oder vorhandenen Abhängigkeiten wurde geprüft und verworfen (Begründung dokumentiert).
- [ ] **MUSS** Der KI-Vorschlag enthält Name, Quelle, Version, Lizenzangabe aus der Manifestdatei, Begründung und Alternativen – und wurde nicht ungeprüft übernommen.
- [ ] **SOLL** Der Funktionsumfang passt zum Bedarf (keine große Bibliothek für eine Kleinigkeit).

### Identität und Herkunft

- [ ] **MUSS** Das Paket existiert unter exakt diesem Namen im Artefakt-Repository der Organisation; Schreibweise Zeichen für Zeichen geprüft (Typosquatting, halluzinierte Namen).
- [ ] **MUSS** Bezugsquelle ist ausschließlich das Artefakt-Repository der Organisation; keine zusätzlichen Registries, keine direkten Downloads.
- [ ] **MUSS** Herausgeber beziehungsweise Projekt sind identifizierbar; das Paket ist keine kürzlich umbenannte oder übernommene Hülle.

### Zustand und Sicherheit

- [ ] **MUSS** Bekannte Schwachstellen der Zielversion geprüft (Werkzeugklasse Dependency-/Security-Scan); keine offenen kritischen Findings ohne dokumentierte Bewertung.
- [ ] **MUSS** Pflegezustand bewertet: letzte Releases, offene sicherheitsrelevante Issues, Aktivität der Betreuung.
- [ ] **MUSS** Transitive Abhängigkeiten gesichtet; keine unerwarteten zusätzlichen Quellen oder auffällig große Bäume ohne Bewertung.
- [ ] **SOLL** Verhalten zur Laufzeit betrachtet: keine ungeklärten Netzwerkzugriffe, Telemetrie oder Codenachladung.

### Lizenz und Recht

- [ ] **MUSS** Lizenzangabe aus der Manifest- oder Lizenzdatei erhoben (Faktensammlung); die rechtliche Bewertung der Lizenzkompatibilität trifft die zuständige Rolle der Organisation (V8), nicht der KI-Client und nicht diese Checkliste.
- [ ] **MUSS** Lizenz- oder Herkunftsauffälligkeiten (fehlende Lizenz, Copyleft-Fragen, unklare Urheberschaft) sind an die zuständige Rolle gemeldet.

### Einführung

- [ ] **MUSS** Version exakt fixiert; Lockfile wird durch den Menschen mit dem vorgesehenen Werkzeug aktualisiert (nie manuell editiert, nie durch den KI-Client).
- [ ] **MUSS** Freigabe durch `<APPROVAL_ROLE>` (bei Sicherheitsrelevanz zusätzlich `<SECURITY_CONTACT>`) liegt dokumentiert vor.
- [ ] **MUSS** Die Einführung ist ein eigener, klar benannter Commit oder Merge Request (Reversibilität, P7).
- [ ] **SOLL** Das Technology Pack der betroffenen Technologie wird um Hinweise zur neuen Abhängigkeit ergänzt, wenn sie projektprägend ist.

## Abbruch- und Eskalationskriterien

Paket nicht im Artefakt-Repository, Identität unklar, offene kritische Schwachstellen oder Lizenzfragen ungeklärt → keine Einführung; Klärung über E1/E2, bei Sicherheitsverdacht E3 (`leitwerk-core/framework/core/10-error-escalation.md`).

## Ergebnis und Nachweis

Ausgefüllte Prüfpunkte, Bewertungsergebnisse und Freigabe (Rolle, Datum) im Ticket oder Merge Request; der KI-Ursprungsvorschlag bleibt als Anlage nachvollziehbar.
