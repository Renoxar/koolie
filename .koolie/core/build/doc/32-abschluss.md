# Abschluss der Ausarbeitung

## Stand dieser Dokumentfassung

Die Erstfassung 0.1.0 beschrieb ein Framework für genau einen KI-Client. Seither ist der Kern in mehreren Schritten von dieser Bindung gelöst worden; die folgenden Abschnitte sind entsprechend fortgeschrieben.

| Release | Was sich geändert hat |
|---|---|
| 0.2.0 | Der Kern liegt in einem einzigen Verzeichnis; `install.py` trennt Core von Projektbestand |
| 0.5.0 | **Client Packs** als Abbildungsschicht mit Fähigkeitsmatrix (Kap. 7a); 61 von 63 Client-Bindungen im Kern durch Begriffe ersetzt; Querverweisprüfung `FW-KO-04` |
| 0.6.0 | Berechtigungen und Hooks als **Semantikabbildung** aus einer Kernquelle; drei Zusicherungen werden erzwungen statt zugesagt |
| 0.7.0 | Das Framework heißt **Leitwerk**; der Name folgt dem Inhalt (mit `0.88.0` umbenannt in **Koolie**) |
| 0.8.0 | Ein Client Pack besteht aus vier Dateien; die gesamte Saat kommt aus dem Kern |
| 0.9.0 | Dieses Dokument baut aus einem frischen Auscheckstand und weist bei jeder Laufzeitdatei aus, aus welchem Client Pack sie stammt |
| 0.26.0 | Der Schutz-Hook läuft **fail-closed**, und die Hook-Konfiguration steht dort, wo der Client sie nachweislich liest – nicht dort, wo seine Dokumentation sie nennt (D-31, D-32). Ein Client Pack umfasst seither drei Dateien (D-36) |
| 0.49.0 | **Kriterium 4 der 1.0.0-Definition erfüllt:** kein Decision Record mehr im Status `entschieden (Vorschlag)` |
| 0.53.0 | **Kriterium 3 erfüllt:** kein Modulträger mehr im Status `entwurf` |
| 0.57.0 | Der Validator setzt die **Werkzeugneutralität des Kerns selbst** durch (Prüfung 14 und 48). Bis dahin galt sie als Regel und wurde von nichts gemessen – siebzehn Fundstellen in vierzehn Trägern fielen im ersten Lauf |
| 0.84.0 | **Kriterium 2 erfüllt:** keine Ergebniszelle mehr auf `offen`. 111 Zellen über sechs Messtage, ein Schritt aufwärts darunter, und er war Absicht |
| 0.85.0 | Jede mit `[DOK]` belegte Zeile einer Fähigkeitsmatrix nennt die **Quellenkennung** ihrer Belegliste; Prüfung 73 setzt es durch. Eine Zeile bleibt ausdrücklich ohne Zuordnung – *geraten wird nicht* |
| 0.86.0 | **Roadmap-AP2 ist zu Ende gefahren:** 70 Sitzungsläufe an einer Installation, vier Zusagen gemessen – zwei zum Besseren, zwei zum Schlechteren |
| 0.87.0 | **Kriterium 1 erfüllt**, indem die Markerform selbst abgeschafft wurde: *Ein Belegstand sagt, was heute belegt ist, nicht, bis wann es belegt sein muss* (D-291). Die Zahl bleibt als Rückfallsperre stehen |
| 0.88.0 | **Das Framework heißt Koolie.** Der Kern liegt unter `.koolie/core/`, das Project Overlay unter `.koolie/project-overlay/`; 498 Dateien mit einem `git mv`, 1.645 Ersetzungen in 197 Trägern |
| 0.89.0 | Dieses Dokument ist gegen den geltenden Stand gesetzt. 🔴 **Es war seit 0.88.0 nicht baubar** – das Assemblierungsskript zählte den Weg zur Projektwurzel im Quelltext, und der Kern liegt seit der Umbenennung eine Ebene tiefer |

**Was an der Ehrlichkeitsgrenze geblieben ist, und was nicht.** Der Satz „kein Mechanismus wurde in einer Zielinstallation ausgeführt" gilt **nicht mehr**: Für das Client Pack `devin-desktop` ist AP2 gefahren und mit Release 0.86.0 abgeschlossen, neun Matrixzeilen sind an einer laufenden Installation beobachtet. **Geblieben ist die Grenze in ihrer genaueren Form:** Ein Beleg gilt je Zeile, je Client und je Produktstand – nicht als Gesamturteil über eine Matrix. Für `claude-code` sind die Wirkungsnachweise überwiegend offen; ein Dokumentenabgleich belegt `[DOK]`, nicht `[TECHNISCH]` im Sinne einer beobachteten Wirkung. 🔴 **Und zwei der gemessenen Zusagen sind zum Schlechteren ausgegangen** – die Messung hat widerlegt, was das Pack vorgesehen hatte. Das steht in den betreffenden Zeilen und ist nicht eingeebnet worden; *eine Matrix, in der jede Messung die Erwartung bestätigt, misst nicht.*

## Kritische Selbstprüfung

Die Selbstprüfung bezieht sich auf die Erstfassung 0.1.0 und wurde für diese Dokumentfassung auf den Stand 0.89.0 fortgeschrieben. Sie wurde automatisiert durchgeführt (Strukturvalidator über das gesamte Repository: 0 Fehler, 0 Warnungen; zusätzlich Querverweisprüfung `FW-KO-04`; Inhaltsprüfungen auf Secret-Muster, E-Mail-Adressen, IP-Adressen, interne Hostnamen, nicht gelistete URLs; Mermaid-Syntaxprüfung aller Diagramme: valide) und im Durchsichtsverfahren. Ergebnis je Prüffrage:

| Nr. | Prüffrage | Ergebnis |
|---|---|---|
| 1 | Identifizierende Projektinformationen enthalten? | Nein. Variable Inhalte ausschließlich als registrierte Platzhalter; automatische und manuelle Prüfung ohne Befund. |
| 2 | Reale Organisationen, Personen, Kunden, Behörden, Infrastrukturen genannt? | Nein – mit zwei bewussten, zulässigen Ausnahmen laut Auftrag: generische Werkzeugklassen (Jira, Git, GitLab, GitHub, CI/CD, IDE, Wiki) und der Hersteller-/Produktbezug zu Devin Desktop (ehemals Windsurf) samt offizieller Dokumentation, der für Phase 3 erforderlich ist. Rollen statt Personen durchgängig. |
| 3 | Unbelegte Client-Funktionen als Tatsache behauptet? | Nein. Jede Produktaussage trägt `[DOK]` mit Quellenzuordnung (Anhang 31.4), `[EMPF]` oder `[KONZ]`; Offenes trägt den Belegstand `BELEG OFFEN` und ist in Anhang 31.5 konsolidiert. Einschränkung transparent: `[DOK]` heißt dokumentationsbelegt, nicht installationsgeprüft (AP2). |
| 4 | Framework Core und Project Overlay sauber getrennt? | Ja. Platzhalter-Schnittstellen, getrennte Ownership, technische Schreibsperren, Integritätsblock in der Berechtigungsdatei (seit 0.6.0 erzeugt und gegen die Kernquelle geprüft), Integritätsblock in `config.json`, strikte Overlay-Validierung; Grenzfälle über Entscheidungsbaum 6 (Kap. 8). |
| 5 | Referenzartefakte tatsächlich wiederverwendbar? | Ja. Alle Artefakte sind projektneutral, versioniert, mit Owner-Feld und Ausfüllhinweisen; Skills/Prompts/Checklisten arbeiten ausschließlich mit Overlay-Platzhaltern; Übernahmeweg inklusive Aktualisierung ist definiert (Kap. 28). |
| 6 | Widersprüchliche Anweisungen? | Keine bekannten. Prioritätshierarchie mit Widerspruchsprüfung und Zusatzregeln (Kap. 25.1); die zwei im Auftrag angelegten Spannungen (zwei Hierarchiefassungen; M5 ohne Befehle vs. lesende Git-Befehle für MR-Texte) wurden erkannt, entschieden und dokumentiert (K-08; FW-CORE-05). Restsicherung über Konsistenztests KO und Review-Zyklus. |
| 7 | Annahmen als Annahmen gekennzeichnet? | Ja. A-01 bis A-05 im Decision Log und im Abschlussabschnitt; in Artefakten sind Vermutungen und Vorschläge als solche markiert (P3-Konvention durchgängig). |
| 8 | Rückfragen bei relevanten Unklarheiten verlangt? | Ja. No Assumption Policy in der Wurzel-Anweisungsdatei, jedem Skill (Rückfragenregeln, [RÜCKFRAGE]-Punkte), jeder Prompt-Vorlage und im Arbeitsablauf Schritt 4; Testklasse FI prüft es. |
| 9 | Datenschutz und Informationssicherheit operativ umsetzbar? | Ja. Vier Kontextklassen mit Entscheidungsbaum und Checkliste, Freigabeverfahren, Vorfallablauf, technische Sperren (deny-Regeln, Hook), Team-Einstellungs-Anschlüsse; offene organisationsspezifische Voraussetzungen sind als K-05/K-06 ausgewiesen statt wegdefiniert. |
| 10 | Menschliche Prüfung an allen relevanten Stellen verankert? | Ja. P1/P5, Delegationsverbote V1/V2, Freigabepunkt Schritt 9, Review-Regeln mit Stufen-Tiefe, MR-Checkliste, „keine Stufe ersetzt menschliche Prüfung" (FW-CORE-09), der Assistent erklärt nie etwas für freigegeben. |
| 11 | Übernahme ohne Core-Änderung möglich? | Ja. Adoption Guide + CL-10; Projektwechsel = Overlay-Tausch; byte-gleiche Core-Übernahme aus Releases; nachgewiesen durch Trennmechanik (Kap. 8). |
| 12 | Skills versionierbar, testbar, wartbar? | Ja. Semantic Versioning je Skill, Lebenszyklus mit Kriterien, Pflicht-Testfälle (2 Positiv/3 Negativ je Skill), CHANGELOG je Skill, Strukturvalidierung und Ausgabeprüfung per Skript, Owner-Feld. |
| 13 | Beispiele ausschließlich synthetisch und gekennzeichnet? | Ja. Kennzeichnungspflicht ist Konvention und Validator-Prüfung („synthetisch" in jeder EXAMPLES.md); Beispiele nutzen offensichtlich fiktive Bezeichner und Beispiel-Domänen. |
| 14 | Offene Entscheidungen im Decision Log? | Ja, und das Register ist seither erheblich gewachsen: **312 Decision Records von D-01 bis D-312, lückenlos; 102 Klärungspunkte von K-01 bis K-104 – zwei Nummern fehlen: `K-99`, eine belegte synthetische Kennung des Prüfapparats, und die zusammengesetzte Kennung der Sonde zu Prüfung 50 – die gerade **nicht** belegt ist und im Kern nicht ausgeschrieben stehen darf, weil sie gemeldet werden soll; dazu fünf Annahmen A-01 bis A-05** – zentral geführt (Kap. 29.2), **gezählt am 2026-09-22 und als datierte Angabe stehengeblieben** (D-318). Die Vollständigkeit beider Register setzen Prüfung 50 und 58 durch: Jede im Kern genannte Kennung steht als Zeile im Log. Entscheidungsreife Kurzliste unten. |
| 15 | Technische Empfehlungen nach Verbindlichkeit und Belegstatus gekennzeichnet? | Ja. MUSS/SOLL/KANN/DARF NICHT plus `[DOK]`/`[EMPF]`/`[KONZ]`/`BELEG OFFEN` durchgängig; Legende in Kap. 6 (FW-CORE-00). |

Im Zuge der Selbstprüfung behobene Mängel (Auszug): Vereinheitlichung der M5-Befehlsregel (lesende Git-Befehle) über Modul, Laufzeitregel und Skills; Registrierung nachträglich aufgefallener Schema-Platzhalter; Entfernung eines Kodierungsartefakts; Korrektur eines Abschnittsverweises in der MCP-Vorlage; Ergänzung fehlender Kernregeln-Prüfungen im Validator während der Erstellung.

## Offene Entscheidungen

Punkte, die tatsächlich eine projektspezifische oder organisatorische Entscheidung erfordern (Details und Wege im Decision Log):

1. **Organisationsfreigabe und Vertragslage (K-05, K-06):** Planstufe/Admin-Kontrollen erheben; Datenschutz- und Vertragsprüfung (Auftragsverarbeitung, Training-Opt-out, Zero Data Retention, Verarbeitungsorte, Löschverfahren) durchführen und im Overlay referenzieren. Vorher keine Aktivierung.
2. **Nutzungsumfang (K-04):** Nur lokale, beobachtete Nutzung (Framework-Standard) oder Freigabe von Cloud-Sitzungen und Läufen ohne beobachtende Person mit erweitertem Sicherheitsmodell.
3. **Rollenbesetzung:** `<FRAMEWORK_OWNER>`, Overlay Owner, `<SECURITY_CONTACT>`, `<DATA_PROTECTION_CONTACT>`, Mentorinnen/Mentoren, Modul-Owner (Zuordnung außerhalb des Repositorys).
4. **Bestätigung der Strukturentscheidungen D-01 bis D-10** durch den künftigen Framework Owner – insbesondere D-05 (Modus ohne Rückfragen untersagt), D-06/K-08 (8-stufige Hierarchie mit Verschärfungsprinzip), D-10 (Cloud-Sitzungen und Läufe ohne beobachtende Person deaktiviert, D-386). Die übrigen 302 der am 2026-09-22 gezählten 312 Records sind Framework-Entscheidungen und betreffen ein aufnehmendes Projekt nur über ihre Wirkung.
5. **Erstprojekt-Parameter:** Overlay-Werte (Pfade, Befehle, kritische Komponenten, `<CHANGE_SIZE_THRESHOLD>`), Ablageorte für Ergebnisberichte/Pläne/Testprotokolle, Feedbackkanal, Review-Zyklus-Frequenz.
6. **Wahl des Client Packs und dessen verbindliche Zielversion** für AP2 und den Pilot. Ohne geprüfte Zielversion ist in der Fähigkeitsmatrix keine Einstufung `[TECHNISCH]` zulässig.
7. **Pilotparameter:** Pilotgruppe, `<PILOT_DURATION>`, Fallliste, Zielwerte der Metriken (erst nach Referenzbasis).

## Annahmen

Unvermeidbare Annahmen dieser Erstfassung – alle gekennzeichnet, keine stillschweigenden (vollständig mit Auswirkungsanalyse im Decision Log):

1. **A-01:** Das Projekt-Repository kann im Wurzelverzeichnis um die Wurzel-Anweisungsdatei und die Laufzeitschicht des gewählten Client Packs ergänzt werden (sonst eigener Workspace-Zuschnitt nötig).
2. **A-02:** Entwickler arbeiten auf Feature-Branches ohne Direktschreibrechte auf geschützte Branches.
3. **A-03:** Ein dokumentierter Review-/Freigabeprozess (Merge Request, CI) existiert und bleibt bestehen.
4. **A-04:** Verarbeitung der Anfragen erfolgt über Anbieter-/Modellanbieter-Infrastruktur (kein lokales Modell) – Grundlage der restriktiven Kontextklassen.
5. **A-05 (gilt für das Client Pack `devin-desktop`):** Die in der CLI-Dokumentation beschriebenen Mechanismen gelten für Devin Local in Devin Desktop (die Desktop-Dokumentation verweist auf geteilte Modi/Mechanismen); Absicherung über die Belegspalte der Fähigkeitsmatrix und AP2.

## Verifikationsbedarf

Gegen die Dokumentation des gewählten Clients beziehungsweise in einer Zielinstallation zu prüfen: die Fähigkeitsmatrix des Client Packs (**1 von 36 Zeilen bei `devin-desktop` sagt `BELEG OFFEN` – dauerhaft –, bei `claude-code` keine von 31; dort stehen dafür die Wirkungsnachweise überwiegend aus**) sowie die konsolidierten Punkte V2–V10 aus Anhang 31.5 – V1 ist mit 0.26.0 geschlossen, Ergebnis „nicht dokumentiert"; exakte `config.json`-Schemadetails; Hook-Eingabeschema (danach fail-closed als Standard); Skill-Discovery `.agents/skills/` und `@skills:`-Verhalten; Frontmatter-Toleranz; MCP-Dateistruktur; Codebasis-Indexierung; Spaces-Kontextreichweite; Wirkung additiver Skill-Permissions; reales Ladeverhalten der always-on-Summe. Prüfweg: Roadmap-AP2 mit Protokollpflicht; laufend: Testklasse AK im Release-Zyklus.

## Datenschutzprüfung

Das Ergebnis ist nach automatisierter Prüfung (Sperrbegriffe, E-Mail-/IP-/Hostnamen-/URL-Muster, Secret-Muster über alle Dateien) und manueller Durchsicht **frei von identifizierenden Projekt-, Personen-, Kunden-, Behörden- und Infrastrukturinformationen**: keine realen oder plausibel wirkenden Namen, Organisationseinheiten, Standorte, internen URLs, Repository-, Server-, Mandanten- oder Umgebungsbezeichnungen; keine Geheimnisse oder personenbezogenen Daten; Platzhalter sind nicht mit realistisch wirkenden Werten befüllt; alle Beispiele sind synthetisch und als solche gekennzeichnet. Genannt werden ausschließlich – auftragsgemäß zulässig – generische Werkzeugklassen sowie Hersteller, Produkt und offizielle Dokumentations-Fundstellen von Devin Desktop (ehemals Windsurf). Die Eingaben des Auftrags enthielten keine schutzbedürftigen Informationen, die zu übernehmen oder zu abstrahieren gewesen wären.

## Empfohlene nächste Schritte

Priorisiert und unmittelbar umsetzbar auf dem Weg zur ersten produktiven Framework-Version:

1. **Rollen besetzen und Prüfungen beauftragen (AP1):** Framework Owner und Projektrollen benennen; Datenschutz-/Vertragsprüfung (K-06) und Erhebung der Planstufe/Admin-Kontrollen (K-05) starten – der kritische Pfad.
2. **Mechanismen validieren (AP2):** Testinstallation mit fixierter Zielversion; die offenen Belege der Fähigkeitsmatrix und die konsolidierten Prüfpunkte protokolliert abarbeiten; Hook auf fail-closed stellen; Belegstatus-Tabellen aktualisieren.
3. **Core-Review durchführen (AP3):** FW-CORE-Module und Prioritätshierarchie durch die benannten Rollen abnehmen; D-01…D-10 bestätigen; Organisations-Mapping (Klassifizierung → K0–K3) füllen.
4. **Erstprojekt konfigurieren (AP4):** Client Pack wählen, Overlay vollständig ausfüllen, die Platzhalter der Berechtigungsdatei befüllen, erstes Technology Pack für `<TECH_STACK>` erstellen, Übungsrepository erzeugen; strikte Validierung.
5. **Sicherheits-/Datenschutzfreigabe einholen (AP6)** und **Basistests des Testkatalogs ausführen (AP7-Teilmenge)** – erst danach Overlay aktivieren (CL-10).
6. **Erste Nutzergruppe onboarden (AP8):** Mentoren briefen, Köder scharf schalten, Freigaben dokumentieren.
7. **Pilot starten (AP9):** Referenzbasis erheben, Etikettierung einrichten, Review-Punkte terminieren – und die Auswertung (AP10) als echte Entscheidung über Fortführung, Anpassung oder Beendigung behandeln.
