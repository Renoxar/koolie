# Framework Core 02 – Kontext- und Datenschutzmodell

| Attribut | Wert |
|---|---|
| Modul-ID | FW-CORE-02 |
| Ebene | 1 – Framework Core |
| Verbindlichkeit | normativ (Abschnitte 1–6), Erläuterung (Abschnitt 7) |
| Owner | `<FRAMEWORK_OWNER>` in Abstimmung mit `<DATA_PROTECTION_CONTACT>` |
| Version | 0.1.6 |
| Status | `pilot` |

## 1. Ausgangslage (normativ)

1. Jeder Inhalt, der dem KI-Client als Kontext bereitgestellt wird (geöffnete Dateien, per Erwähnung eingebundene Dateien, Suchergebnisse, Befehlsausgaben, eingefügter Text, Inhalte aus MCP-Werkzeugen, Inhalte in Spaces), verlässt den Arbeitsplatz und wird über die Infrastruktur des Anbieters und dessen Modellanbieter verarbeitet (Annahme A-04; Anbieterdokumentation: Opt-out aus Modelltraining auf kostenpflichtigen Plänen, danach Zero Data Retention bei den Modellanbietern; Enterprise-Kunden: kein Training ohne schriftliche Zustimmung `[DOK]`).
2. Die konkreten vertraglichen und technischen Bedingungen (Auftragsverarbeitung, Verarbeitungsorte, Aufbewahrung, Training-Opt-out, Zero Data Retention, Codebasis-Indexierung) sind organisationsspezifisch und MÜSSEN vor der Einführung geprüft und im Overlay referenziert werden: `<TBD: Ergebnis der Datenschutz- und Vertragsprüfung>`. Art und Ort der Codebasis-Indexierung: `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>`.
3. Bis zum Vorliegen dieser Prüfung gilt die restriktivste Auslegung: Nur Kontextklasse K0 und K1 (Abschnitt 2) dürfen bereitgestellt werden, und nur, wenn die Organisation die Nutzung des Werkzeugs grundsätzlich freigegeben hat.

## 2. Kontextklassen (normativ)

| Klasse | Bezeichnung | Definition | Bereitstellung an den KI-Client |
|---|---|---|---|
| **K0** | Frei | Öffentliche oder framework-eigene Inhalte ohne Projektbezug (Framework-Dateien, öffentliche Dokumentation, Open-Source-Code mit bekannter Lizenz) | zulässig |
| **K1** | Projektintern, freigegeben | Inhalte des Projekt-Repositorys und Dokumente, die im Overlay-Manifest ausdrücklich für den KI-Kontext freigegeben sind und keine K2/K3-Bestandteile enthalten | zulässig, aufgabenbezogen (Least Context) |
| **K2** | Eingeschränkt | Inhalte mit erhöhtem Schutzbedarf, die nur nach dokumentierter Einzel- oder Kategoriefreigabe und gegebenenfalls in abstrahierter oder anonymisierter Form bereitgestellt werden dürfen (zum Beispiel Architekturdokumente mit Infrastrukturdetails, Tickets mit fachlichen Fallbeschreibungen, Testdaten, Logauszüge, Schnittstellenverträge externer Partner) | nur nach Freigabe gemäß Abschnitt 4 und nach Bereinigung |
| **K3** | Ausgeschlossen | Inhalte, die niemals bereitgestellt werden dürfen | nicht zulässig |

### 2.1 Immer K3 (normativ)

Die folgenden Kategorien sind **unbedingt** ausgeschlossen. Eine Freigabe nach Abschnitt 2.2 oder Abschnitt 4 gilt ausschließlich für Inhalte **außerhalb** dieser Kategorien; keine tiefere Ebene, kein Overlay und kein Ausnahmeprozess kann sie freigeben (`leitwerk-core/governance/PRIORITY_HIERARCHY.md`, Regel 2.4). Lässt sich der ausgeschlossene Bestandteil vollständig entfernen oder ersetzen, wird die **bereinigte Ableitung als eigener Inhalt neu eingestuft** (Entscheidungsbaum `leitwerk-core/decision-trees/01-context-allowed.md`, Schritt 1); das Ursprungsdokument bleibt ausgeschlossen (D-52).

- Secrets, Zugangsdaten, Tokens, private Schlüssel, Zertifikate mit privatem Schlüssel, Verbindungszeichenfolgen mit Anmeldedaten, `.env`-Dateien mit Werten, Keystores
- personenbezogene Echtdaten (Namen, Kontaktdaten, Kennnummern, Gesundheits-, Finanz- oder sonstige Daten realer Personen), auch in Testdaten, Fixtures, Datenbank-Dumps, Logs oder Screenshots
- Produktionsdaten und Produktionsdatenbankauszüge
- nicht freigegebene Kunden-, Behörden- oder Vertragsdokumente
- Sicherheitskonfigurationen mit Schutzwirkung (Firewall-Regeln, Berechtigungsmatrizen realer Systeme, Schwachstellenberichte)
- interne Adressen, Hostnamen, Netzpläne, Mandanten- und Umgebungskennungen
- Inhalte, die durch Vertraulichkeitsvereinbarungen oder Einstufung der Organisation als vertraulich oder höher gekennzeichnet sind
- Inhalte aus anderen Projekten oder Mandanten

### 2.2 Einstufungsregeln (normativ)

1. Die Einstufung erfolgt durch den Menschen vor der Bereitstellung (Entscheidungsbaum `leitwerk-core/decision-trees/01-context-allowed.md`).
2. Enthält ein Inhalt Bestandteile unterschiedlicher Klassen, gilt die höchste Klasse für den gesamten Inhalt, bis die höher eingestuften Bestandteile entfernt oder ersetzt sind.
3. Das Project Overlay legt im Manifest (`project-overlay/overlay-manifest.yaml`) für jeden eingebundenen Dokumenttyp die Klasse fest. Fehlt eine Einstufung, gilt K3.
4. Das Overlay DARF eine Klasse verschärfen (K1 → K2), aber NICHT lockern, es sei denn, die Datenschutz- und Vertragsprüfung (Abschnitt 1.2) erlaubt dies ausdrücklich und die Lockerung ist im Decision Log dokumentiert. **Eine Kategorie aus Abschnitt 2.1 DARF auf keinem Weg gelockert werden** – nicht durch das Overlay, nicht durch die Datenschutz- und Vertragsprüfung, nicht durch einen Eintrag im Decision Log und nicht durch den Ausnahmeprozess. Änderbar ist die Liste allein über den Änderungsprozess des Frameworks, also auf ihrer eigenen Ebene (D-52).

## 3. Bereitstellungsregeln (normativ)

1. **Aufgabenbezug:** Es wird nur der Kontext bereitgestellt, der für die konkrete Aufgabe erforderlich ist. Ganze Verzeichnisbäume, vollständige Ticketsysteme oder ganze Wikis DÜRFEN NICHT pauschal eingebunden werden.
2. **Aktualität:** Veraltete Dokumente SOLLEN nicht bereitgestellt werden; ist ein Dokument im Manifest als veraltet markiert, DARF es NICHT verwendet werden.
3. **Bereinigung vor Bereitstellung:** K2-Inhalte werden vor der Bereitstellung bereinigt: Personen durch Rollen, Organisationen durch Platzhalter, Adressen und Kennungen durch `<PLACEHOLDER>`, Fallbeschreibungen durch abstrahierte Sachverhalte ersetzt. Die bereinigte Fassung wird nicht in das Repository übernommen (Ebene E).
4. **Tickets:** Aus `<ISSUE_TRACKER>` werden nur Titel, technische Beschreibung und Akzeptanzkriterien übernommen – nach Prüfung auf personenbezogene Daten und vertrauliche Inhalte. Kommentarverläufe, Anhänge, Screenshots und Kundenkommunikation SOLLEN nicht übernommen werden.
5. **Befehlsausgaben und Logs:** Vor der Weitergabe an den KI-Client werden Befehlsausgaben und Logauszüge auf personenbezogene Daten, Secrets und Hostnamen geprüft. Das Werkzeug selbst wird angewiesen, vermutete Secrets oder personenbezogene Daten in Ausgaben nicht zu wiederholen (Wurzel-Anweisungsdatei).
6. **Testdaten:** der KI-Client arbeitet ausschließlich mit synthetischen oder nachweislich anonymisierten Testdaten. Synthetische Daten werden als solche gekennzeichnet (zum Beispiel Namen wie `Testperson-01`).
7. **Externe Quellen:** Websuche und Abruf externer Seiten sind standardmäßig deaktiviert (Enterprise-Standard laut Anbieterdokumentation `[DOK]`; Framework-Standard für alle Pläne `[KONZ]`). **Eine Freigabe je Domain ist nicht vorgesehen** und war es nie: In der Berechtigungskonfiguration gewinnt `deny`, eine zusätzliche `allow`-Regel hebt das generelle Verbot nicht auf, und bei einem Client ohne Musterunterstützung für die Abrufwerkzeuge ist sie nicht einmal ausdrückbar. Wer externen Abruf braucht, ersetzt die Verbotsregel über einen Änderungsantrag (`leitwerk-core/framework/core/03-security.md` Abschnitt 4, D-59); bis dahin wird freigegebene Dokumentation lokal bereitgestellt.
8. **MCP-Werkzeuge:** Anbindungen an `<ISSUE_TRACKER>`, `<DOCUMENTATION_PLATFORM>` oder andere Systeme über MCP DÜRFEN NUR nach Freigabe je Server im Overlay konfiguriert werden. Die Bestätigungspflicht vor einem MCP-Aufruf DARF NICHT auf `allow` gesetzt werden, solange der Server nicht im Overlay als freigegeben dokumentiert ist; **ob der Client sie von sich aus stellt, führt sein Client Pack in der Fähigkeitsmatrix** (`[DOK]` bei `devin-desktop`).
9. **Spaces und geteilter Kontext:** Werden Kontexte zwischen Agenten geteilt (Spaces `[DOK]`, Details `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>`), gelten für den geteilten Kontext dieselben Klassen; ein Space DARF NICHT K2-Inhalte enthalten, die nicht für alle beteiligten Aufgaben freigegeben sind.
10. **Persönliche Regeln:** Persönliche Ergänzungen (nutzerlokale Überschreibungen, globale Regeln) DÜRFEN NICHT Kontext einbinden, der über die Freigaben des Overlays hinausgeht. Dies ist eine Regel **an den Menschen**, keine Rangaussage: Welchen Rang eine Anweisungsquelle außerhalb des Repositoriums hat – nämlich keinen –, regelt Regel 2.6 der Prioritätshierarchie (D-34). Welche Quellen ein Client kennt und was davon abgeschaltet ist, führt sein Client Pack im Abschnitt „Anweisungs- und Konfigurationsquellen außerhalb des Projekts".

## 4. Freigabeverfahren für K2-Inhalte (normativ)

| Schritt | Inhalt | Verantwortung |
|---|---|---|
| 1 | Bedarf begründen: Welche Aufgabe erfordert welchen Inhalt, warum reicht K1 nicht | Bearbeiterin oder Bearbeiter |
| 2 | Bereinigungsplan: Welche Bestandteile werden wie ersetzt | Bearbeiterin oder Bearbeiter |
| 3 | Freigabe: Einzelfreigabe durch `<APPROVAL_ROLE>` oder Kategoriefreigabe im Overlay-Manifest (zum Beispiel „Architekturdokumente nach Entfernung des Kapitels Infrastruktur") | `<APPROVAL_ROLE>`, bei personenbezogenen Daten zusätzlich `<DATA_PROTECTION_CONTACT>` |
| 4 | Dokumentation: Freigabe mit Datum, Umfang und Bereinigung im Ergebnisbericht und – bei Kategoriefreigaben – im Manifest | Bearbeiterin oder Bearbeiter |
| 5 | Nachprüfung: Stichprobe im Review, ob nur freigegebener Kontext verwendet wurde | Reviewerin oder Reviewer |

## 5. Verhalten bei unbeabsichtigter Bereitstellung (normativ)

Wird festgestellt, dass K3-Inhalte an den KI-Client gelangt sind (zum Beispiel eine Datei mit Zugangsdaten wurde eingebunden):

1. Sitzung sofort beenden; keine weiteren Eingaben.
2. Betroffene Secrets als kompromittiert behandeln und über den Prozess der Organisation rotieren lassen (`<SECURITY_CONTACT>`).
3. Vorfall an `<SECURITY_CONTACT>` und – bei personenbezogenen Daten – an `<DATA_PROTECTION_CONTACT>` melden; die Meldefristen der Organisation gelten.
4. Vorfall im Framework-Betrieb erfassen (`leitwerk-core/governance/INCIDENT_HANDLING.md`) und Ursache im nächsten Review-Zyklus adressieren (zum Beispiel fehlende `deny`-Regel).

Eine Löschung beim Anbieter ist über den vertraglich vereinbarten Weg zu beantragen (`<TBD: Löschverfahren laut Vertrag>`).

## 6. Technische Absicherung in der Laufzeitschicht (normativ, soweit `[DOK]`)

| Maßnahme | Umsetzung | Belegstatus |
|---|---|---|
| Lesezugriff auf Secret-Pfade verhindern | Verweigerungsregeln für Lesezugriffe in der Berechtigungsdatei auf `.env*`, Schlüsseldateien, Keystores, `<EXCLUDED_PATHS>`; im Sandbox-Modus werden `Read`-Deny-Pfade für Befehle unsichtbar | `[DOK]` |
| Websuche deaktivieren | Team-Einstellung (Enterprise) beziehungsweise keine `Fetch`-Allow-Regeln | `[DOK]` (Enterprise), `[EMPF]` (andere Pläne) |
| MCP nur nach Freigabe | keine Einträge in der MCP-Konfiguration, bis Freigabe vorliegt; Rückfrage als Standard belassen | `[DOK]` |
| Training-Opt-out und Zero Data Retention | Data-Controls-Einstellung durch Administrator (Teams) beziehungsweise vertragliche Regelung (Enterprise) | `[DOK]`, Umsetzung `<TBD: Nachweis der Einstellung>` |
| Prüfung von Werkzeugaufrufen auf Secrets | Hook `PreToolUse` mit Skript, das Schreib- und Ausführungsanfragen auf Secret-Muster prüft und blockiert (`leitwerk-core/tests/scripts/hook-check-secrets.py`) | `[DOK]` (Hook-Mechanismus), `[EMPF]` (Skript) |
| Sandbox für Befehlsausführung | Sandbox-Modus mit Domain-Allowlist; unter Windows laut Dokumentation nicht verfügbar; Netzwerkfilterung laut Dokumentation instabil | `[DOK]`, Einsatz `<TBD: Betriebssystem und Sandbox-Verfügbarkeit>` |

## 7. Erläuterung

Das Modell ist bewusst einfach gehalten: Vier Klassen, eine Einstufung durch den Menschen, eine Bereinigungspflicht für K2 und ein absolutes Verbot für K3. Die häufigsten Fehler in der Praxis sind nicht bösartig, sondern beiläufig: das Einfügen eines Logauszugs mit einer E-Mail-Adresse, das Einbinden eines Ticket-Kommentars mit einem Kundennamen, das Öffnen einer `.env`-Datei „nur zum Nachsehen". Deshalb kombiniert das Framework die Verhaltensregel (Checkliste, Onboarding) mit der technischen Sperre (`deny`-Regeln, Hook), sodass ein einzelner Fehler nicht ausreicht, um K3-Inhalte weiterzugeben.
