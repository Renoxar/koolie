# Framework Core 09 – Risikoklassifizierung und Kontrollstufen

| Attribut | Wert |
|---|---|
| Modul-ID | FW-CORE-09 |
| Ebene | 1 – Framework Core |
| Verbindlichkeit | normativ (Abschnitte 1–4), Erläuterung (Abschnitt 5) |
| Owner | `<FRAMEWORK_OWNER>` |
| Version | 0.1.4 |
| Status | `pilot` |

> **Abgrenzung:** Diese Klassifizierung dient der operativen Steuerung des KI-Einsatzes. Sie ist keine rechtliche Klassifizierung und ersetzt keine Bewertung nach Datenschutz-, IT-Sicherheits- oder KI-regulatorischen Vorgaben der Organisation.

## 1. Grundregeln (normativ)

1. Jede Aufgabe, die an den KI-Client gegeben wird, MUSS vor Beginn einer Kontrollstufe zugeordnet werden (Preflight-Check, `.koolie/core/checklists/01-preflight.md`).
2. Es gilt das **Maximumprinzip**: Die Kontrollstufe einer Aufgabe ist die höchste Stufe, die einer der Risikofaktoren aus Abschnitt 2 auslöst. Es wird nicht gemittelt.
3. Erfüllt eine Aufgabe ein Kriterium der **Delegationsverbotsliste** (Abschnitt 4), DARF sie NICHT an den KI-Client delegiert werden – unabhängig von der Kontrollstufe.
4. Keine Kontrollstufe ersetzt die menschliche Prüfung vollständig. Auch auf Stufe niedrig MUSS ein Mensch das Ergebnis vor Übernahme prüfen.
5. Steigt das Risiko während der Bearbeitung (zum Beispiel weil sich herausstellt, dass Authentifizierungscode betroffen ist), MUSS der KI-Client die Bearbeitung anhalten, die neue Einstufung melden und auf eine menschliche Entscheidung warten.
6. Im Zweifel zwischen zwei Stufen MUSS die höhere gewählt werden.
7. Das Project Overlay KANN Kriterien verschärfen und projektspezifische Komponenten einer Stufe fest zuordnen (zum Beispiel „alle Änderungen im Modul `<CRITICAL_MODULE>` sind mindestens Stufe hoch"). Es DARF Kriterien NICHT lockern.

## 2. Risikofaktoren und Einstufungskriterien (normativ)

| Nr. | Risikofaktor | niedrig | mittel | hoch |
|---|---|---|---|---|
| R1 | Umfang der Änderung | wenige Zeilen in einer Datei, eine Verantwortlichkeit | mehrere Dateien eines Moduls | modulübergreifend oder mehr als `<CHANGE_SIZE_THRESHOLD>` geänderte Dateien |
| R2 | Kritikalität betroffener Komponenten | Hilfs-, Test- oder Dokumentationscode | fachliche Standardkomponente | im Overlay als kritisch markierte Komponente |
| R3 | Sicherheitsrelevanz | keine sicherheitsrelevante Funktion berührt | indirekte Berührung (zum Beispiel Eingabevalidierung, Logging) | Kryptografie, Sitzungsverwaltung, Berechtigungsprüfung, Security-Konfiguration |
| R4 | Datenschutzbezug | keine personenbezogenen Daten im Code-Pfad | Code-Pfad verarbeitet personenbezogene Daten ohne Änderung der Verarbeitungslogik | Änderung an Erhebung, Speicherung, Weitergabe oder Löschung personenbezogener Daten |
| R5 | Produktionsnähe | nur lokale Entwicklung oder Testumgebung betroffen | Änderung geht mit dem regulären Release in Produktion | Konfiguration oder Skripte mit unmittelbarer Produktionswirkung (Deployment, Migration, Infrastruktur) |
| R6 | Reversibilität | vollständig per Revert rücknehmbar | Revert mit Folgeaufwand (zum Beispiel Datenbereinigung) | nicht oder nur schwer rücknehmbar (Datenmigration, externe Effekte) |
| R7 | Testbarkeit | vollständig durch bestehende automatisierte Tests abgedeckt | teilweise abgedeckt, manuelle Prüfung möglich | nicht automatisiert testbar oder Tests fehlen |
| R8 | Reichweite über Komponenten | eine Komponente | mehrere Komponenten eines Systems | systemübergreifend oder externe Konsumenten betroffen |
| R9 | Einführung externer Abhängigkeiten | keine | Aktualisierung einer bestehenden Abhängigkeit (Patch/Minor) | neue Abhängigkeit oder Major-Update (Checkliste `.koolie/core/checklists/07-new-dependency.md`) |
| R10 | Änderung von Authentifizierung oder Autorisierung | keine | keine (jede Berührung ist mindestens hoch) | jede Änderung |
| R11 | Änderung von Datenmodellen oder Schnittstellen | keine | interne, abwärtskompatible Erweiterung | Schema-Änderung, Vertragsbruch einer Schnittstelle, Migration |
| R12 | Automatisierungsgrad der KI-Nutzung | einzelne, überwachte Sitzung im rückfragenden Standardmodus (D-05; wie der Modus im Client heißt, nennt die Fähigkeitsmatrix des Client Packs); oder mehrere rein lesende Sitzungen beziehungsweise Subagenten (M1, M2) unter einer aufsichtführenden Person | mehrere Schritte in einer Sitzung mit sitzungsweiten Freigaben; oder parallele schreibende Sitzungen auf disjunkten Schreibzielen | Modus mit selbsttätiger Übernahme, soweit ihn eine dokumentierte Ausnahme zulässt (D-05); parallele Sitzungen auf gemeinsamen Schreibzielen; Hintergrund-Subagenten in M3 |
| R13 | Mögliche Fehlerfolgen | lokal begrenzt, sofort erkennbar | Funktionsstörung in Test oder Produktion, erkennbar durch Monitoring | Datenverlust, Sicherheitsvorfall, Verstoß gegen rechtliche Vorgaben, Reputationsschaden |

`<CHANGE_SIZE_THRESHOLD>` und die Liste kritischer Komponenten werden im Project Overlay festgelegt (`<TBD: Schwellenwert für Änderungsumfang>`).

**Zu R12 (normativ).** Die Spalten unterscheiden nach **Schreibziel und Aufsicht**, nicht nach der Zahl der Sitzungen: rein lesende Parallelarbeit unter Aufsicht niedrig, schreibende Parallelarbeit auf getrennten Zielen mittel, gemeinsame Schreibziele hoch (D-54; die Voraussetzungen für Parallelarbeit nennt `.koolie/core/framework/core/05-working-model.md`, Abschnitt 3.1). Ein Modus mit selbsttätiger Übernahme bleibt **hoch**: Dass die erste Schutzlinie in einem erweiterten Modus ausfällt, ist gemessen (D-35), und diese Einstufung wird nicht gelockert. Der Modus ohne Rückfragen ist **keine Stufe von R12**, sondern untersagt (D-05, D-389).

## 3. Kontrollstufen (normativ)

| Aspekt | Stufe **niedrig** | Stufe **mittel** | Stufe **hoch** |
|---|---|---|---|
| Zulässige Betriebsmodi | alle fünf Modi (`05-working-model.md`) | Read-only Analysis, Guided Planning, Test and Validation, Documentation Support uneingeschränkt; Controlled Modification nur auf Basis eines von einem Menschen bestätigten Plans | Read-only Analysis und Guided Planning; Controlled Modification nur nach dokumentierter Freigabe durch `<APPROVAL_ROLE>` und mit begleitender Person (Pairing); Test and Validation nur ohne Änderung an Produktivcode; Documentation Support zulässig |
| Erforderliche Prüfungen | Selbstprüfung der Bearbeiterin oder des Bearbeiters anhand `.koolie/core/checklists/04-review-ai-code.md`; alle bestehenden Quality Gates | zusätzlich: Plan-Review vor Umsetzung; vollständiger Diff-Review durch unabhängige Reviewerin oder Reviewer; Tests für geänderte Logik verpflichtend | zusätzlich: Architektur- und Security-Review; Nachweis der Testabdeckung; bei R3/R4/R10: Einbindung `<SECURITY_CONTACT>` beziehungsweise Datenschutzkontakt |
| Notwendige Freigaben | reguläres Review gemäß Projektprozess | Review plus Bestätigung durch Modul-Owner oder `<APPROVAL_ROLE>` | schriftliche Freigabe `<APPROVAL_ROLE>`; bei Sicherheitsrelevanz zusätzlich `<SECURITY_CONTACT>` |
| Dokumentationsumfang | KI-Nutzungsvermerk im Merge Request (Kurzform, `.koolie/core/templates/MR_AI_DISCLOSURE.md`) | zusätzlich: Plan, Fundstellenliste, Ergebnisbericht mit Abweichungen und Restrisiken | zusätzlich: vollständiges Sitzungsprotokoll (Prompts, Freigaben, ausgeführte Befehle), Entscheidungsvermerk der Freigabe |
| Eskalationskriterien | Scope-Überschreitung, unerwartete Berührung anderer Komponenten, fehlgeschlagene Quality Gates ohne klare Ursache | zusätzlich: Abweichung vom bestätigten Plan, neue Abhängigkeit, Testlücke | jede Unklarheit führt zum Stopp; Fortsetzung nur nach erneuter Freigabe |

## 4. Delegationsverbotsliste (normativ)

Folgende Aufgaben und Entscheidungen DÜRFEN NICHT an den KI-Client delegiert werden. Der KI-Client KANN – soweit im Overlay nicht ausgeschlossen – vorbereitende Analysen liefern, trifft aber keine der Entscheidungen und führt keine der Handlungen aus:

| Nr. | Nicht delegierbar | Zulässige Unterstützung durch den KI-Client |
|---|---|---|
| V1 | Freigabe, Genehmigung oder Abnahme von Änderungen, Merge Requests, Releases | Review-Unterstützung mit Befunden (Skill `fw-review-support`) |
| V2 | Merge in geschützte Branches, Tagging von Releases, Deployment in Produktion | Erstellung von Merge-Request-Beschreibungen |
| V3 | Architekturentscheidungen, Technologieauswahl, Einführung neuer Abhängigkeiten | Optionsanalyse mit Vor- und Nachteilen, Vorschlag mit Kennzeichnung |
| V4 | Umgang mit Secrets, Zugangsdaten, Zertifikaten, Schlüsselmaterial (Erzeugen, Rotieren, Eintragen, Lesen) | keine; Fundstellen vermuteter Secrets sind zu melden, nicht auszugeben |
| V5 | Verarbeitung personenbezogener Echtdaten oder Produktionsdaten | Arbeit mit synthetischen oder anonymisierten Testdaten |
| V6 | Änderungen an Produktionssystemen, Infrastruktur, Berechtigungen, Sicherheitskonfigurationen | Analyse und Planvorschlag |
| V7 | Bewertung von Personen, Leistungsbeurteilungen, arbeitsrechtliche oder disziplinarische Fragen | keine |
| V8 | Rechtliche Bewertungen (Lizenzkonformität, Datenschutzrechtliche Zulässigkeit, Vertragsauslegung) | Sammlung von Fakten (zum Beispiel Lizenzangaben aus Manifestdateien) mit Fundstellen |
| V9 | Entscheidung über Fortsetzung bei Sicherheitsvorfall oder Verdacht auf Datenabfluss | keine; sofortiger Stopp und Eskalation |
| V10 | Änderung der Framework-Regeln, des Project Overlays oder der Berechtigungsdatei | Vorschläge als Änderungsantrag (`.koolie/core/governance/CHANGE_REQUEST_TEMPLATE.md`) |
| V11 | Kommunikation nach außen (Kunden, Behörden, Öffentlichkeit) im Namen des Projekts | Entwürfe für interne Verwendung |
| V12 | Löschen von Branches, Historie, Daten oder Artefakten außerhalb des Arbeitsbereichs | keine |

**Abgrenzung zu V6 (normativ).** V6 erfasst den **Betrieb**: tatsächliche Berechtigungen sowie Betriebs-, Infrastruktur- und Sicherheitskonfigurationen – auch dann, wenn sie als Code im Repositorium liegen (Infrastrukturbeschreibungen, Berechtigungs- und Richtliniendateien, die Berechtigungsdatei dieses Frameworks), denn ihr Inhalt **ist** die Berechtigung. V6 erfasst **nicht** die lokale Anwendungslogik mit Sicherheitsbezug: Authentifizierungs- und Autorisierungsprüfungen im Quellcode, Verwendung kryptografischer Bibliotheken, Sitzungsverwaltung. Diese ist über R3 und R10 Kontrollstufe **hoch** und nach deren Freigaben umsetzbar – dokumentierte Freigabe durch `<APPROVAL_ROLE>` und `<SECURITY_CONTACT>`, Umsetzung mit begleitender Person. **Die Frage im Zweifel:** Wirkt die Änderung über Build, Review und Quality Gates des Projekts, oder ist die geänderte Datei selbst die Berechtigung eines laufenden Systems? Im zweiten Fall gilt V6. Greift daneben ein anderes Delegationsverbot – V4 für Schlüsselmaterial, V10 für die Framework-Regeln und die Berechtigungsdatei –, bleibt es unberührt (D-53).

Das Project Overlay KANN die Liste erweitern (`.koolie/project-overlay/OVERLAY.md`, Abschnitt „Ausgeschlossene Aufgaben"). Es DARF sie NICHT verkürzen.

## 5. Anwendungshinweise (Erläuterung)

Die Einstufung dauert in der Praxis unter einer Minute, wenn sie in den Preflight-Check integriert ist: Bearbeiterin oder Bearbeiter geht die Risikofaktoren aus Abschnitt 2 durch, notiert den höchsten Treffer und trägt Stufe und auslösenden Faktor in die Aufgabenbeschreibung ein (zum Beispiel „Stufe mittel wegen R8"). Diese Angabe wandert in den KI-Nutzungsvermerk des Merge Requests und ermöglicht später die Auswertung im Pilot (`.koolie/core/pilot/METRICS.md`).

**Beispiel (synthetisch):** Eine Aufgabe „Fehlermeldung im Formular `<FORM_NAME>` korrigieren" berührt eine Datei (R1 niedrig), eine Standardkomponente (R2 niedrig), keine Sicherheitsfunktion (R3 niedrig), zeigt aber Daten eines Nutzers an (R4 mittel, da der Pfad personenbezogene Daten verarbeitet, die Logik aber unverändert bleibt). Ergebnis: Stufe mittel wegen R4 – Umsetzung nur nach bestätigtem Plan.
