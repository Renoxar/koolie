# Decision Log und Klärungstabelle (Phase 1)

> **Zweck:** Dieses Verzeichnis dokumentiert alle Entscheidungen, Annahmen und offenen Punkte der Framework-Erstellung. Es wird mit jedem Framework-Release fortgeschrieben.
> **Legende Status:** `geklärt` (durch Auftraggeber entschieden), `entschieden (Vorschlag)` (durch Framework-Erstellung als Strukturentscheidung vorgeschlagen, durch Framework Owner zu bestätigen), `offen` (projekt- oder organisationsspezifische Entscheidung erforderlich), `verify` (gegen aktuelle Devin-Dokumentation zu prüfen).

## 1. Klärungstabelle der Auftrags- und Informationsprüfung

| ID | Fragestellung oder Unklarheit | Relevanz | Auswirkung auf das Ergebnis | Benötigte Entscheidung | Status |
|---|---|---|---|---|---|
| K-01 | Lieferformat des Ergebnisses | hoch | Bestimmt Struktur und Redundanz zwischen Dokument und Repository | Auftraggeber | geklärt: Hauptdokument (Markdown) + Referenz-Repository (ZIP) + Word-Export |
| K-02 | Zugrunde zu legender Produktstand von Devin Desktop | hoch | Bestimmt Pfade, Mechanismen und Verifikationsbedarf der Referenzimplementierung | Auftraggeber | geklärt: aktueller Stand nach Rebrand (Devin Local, `.devin/`-Verzeichnisse); Legacy `.windsurf/` nur als Kompatibilitätshinweis |
| K-03 | Vollständigkeit des Arbeitsauftrags (erste Datei endete mitten im Satz) | hoch | Fehlende Format-, Selbstprüfungs- und Overlay-Anforderungen | Auftraggeber | geklärt: vollständige Fassung nachgeliefert und eingearbeitet |
| K-04 | Nutzungsart im Zielprojekt: nur Devin Desktop lokal oder zusätzlich Devin Cloud / CLI | hoch | Sicherheitsmodell, Betriebsmodi, Berechtigungsvorlagen | Projektleitung mit Informationssicherheit | offen: Framework behandelt Desktop als Kern; Cloud-Sessions und CLI als optionale, standardmäßig deaktivierte Erweiterung (`<TBD: Freigabe Cloud/CLI-Nutzung>`) |
| K-05 | Lizenz- und Planstufe (Teams / Enterprise) | mittel | Verfügbarkeit organisationsweiter Kontrollen (Berechtigungen, Sandbox-Erzwingung, MCP-Allowlists, Training-Opt-out durch Admin) | Organisation / Einkauf | offen: `<TBD: Planstufe und verfügbare Admin-Kontrollen>` |
| K-06 | Vertragliche Datenschutzbasis mit dem Anbieter (Auftragsverarbeitung, Training-Opt-out, Zero Data Retention, Verarbeitungsorte) | hoch | Zulässige Kontextklassen, Freigabe des Werkzeugs überhaupt | Datenschutz und Informationssicherheit der Organisation | offen: `<TBD: Ergebnis der Datenschutz- und Vertragsprüfung>`; Framework definiert Mindestanforderungen |
| K-07 | Existenz einer organisationsweiten KI-Richtlinie | mittel | Inhalt der Ebene B (organisationsweite Vorgaben) | Organisation | offen: Ebene B als Einbindungspunkt vorgesehen (`framework/org-policies/`) |
| K-08 | Zwei abweichende Fassungen der Prioritätshierarchie im Auftrag (7-stufig mit kombinierten Rollen-/Technologiepaketen vs. 8-stufig mit Technology Packs vor Role Packs) | hoch | Konfliktauflösung zwischen Regelebenen | Framework Owner | entschieden (Vorschlag): 8-stufige Fassung übernommen, ergänzt um das Verschärfungsprinzip; Begründung in `governance/PRIORITY_HIERARCHY.md` |
| K-09 | Zielgruppe der Erstfassung | mittel | Umfang der Role Packs | – | geklärt durch Auftrag: Softwareentwicklung zuerst, weitere Rollen strukturell vorbereitet |
| K-10 | Anbindung externer Systeme über MCP (Issue Tracker, Wiki, CI) im Zielprojekt | mittel | Kontextquellen, Berechtigungsvorlage | Projektleitung mit Informationssicherheit | offen: MCP standardmäßig nicht konfiguriert; Freigabe je Server über Overlay (`<TBD: freigegebene MCP-Server>`) |
| K-11 | Betriebssystem der Entwicklerarbeitsplätze | mittel | Verfügbarkeit der OS-Sandbox (laut Dokumentation nicht unter Windows) | Projekt / IT | offen: `<TBD: Betriebssystem und Sandbox-Verfügbarkeit>` |
| K-12 | Speicherort der Skills: `.devin/skills/` oder `.agents/skills/` | mittel | Auffindbarkeit der Skills durch Devin Local | Framework Owner | entschieden (Vorschlag): `.devin/skills/` als Primärpfad (in Desktop-FAQ und CLI-Dokumentation belegt); `.agents/skills/` als dokumentierte Alternative, Discovery durch Devin Local zu verifizieren |
| K-13 | Ablage und Verteilung des Frameworks | mittel | Versionierung, Übertragbarkeit | Framework Owner | entschieden (Vorschlag): eigenes Framework-Repository mit Release-Archiven; Integration in das Wurzelverzeichnis des Projekt-Repositorys; Overlay projektseitig |
| K-14 | Zyklus der Aktualitätsprüfung gegenüber Devin-Produktänderungen | niedrig | Governance-Parameter | Framework Owner | offen: `<TBD: Prüfzyklus>`; Verfahren im Framework definiert |
| K-15 | Zielwerte für Metriken | mittel | Pilotbewertung | Projekt | offen by design: Zielwerte werden ausdrücklich nicht vorgegeben |
| K-16 | Pilotzeitraum | niedrig | Pilotkonzept | Projekt | offen: Parameter `<PILOT_DURATION>` |
| K-17 | Sprache der Agentenanweisungen und Skills | mittel | Verständlichkeit für das Team, Modellverhalten | Framework Owner | entschieden (Vorschlag): Deutsch für Anweisungen und Dokumentation, englische Bezeichner für Dateien, Skill-Namen und IDs |
| K-18 | Zusätzliche Metadatenfelder im SKILL.md-Frontmatter | niedrig | Toleranz unbekannter Frontmatter-Schlüssel nicht dokumentiert | Framework Owner | entschieden (Vorschlag): Frontmatter nur mit dokumentierten Feldern; Framework-Metadaten als Tabelle im Dateikörper; `verify` |
| K-19 | Zeichenlimits für Regeldateien unter Devin Local | mittel | Aufteilung der Regeln auf Dateien | – | verify: für Cascade-Regeln sind 12.000 Zeichen je Workspace-Regel und 6.000 Zeichen für globale Regeln dokumentiert; Gültigkeit für Devin Local nicht belegt; Framework hält die Grenzen konservativ ein |
| K-20 | Art und Ort der Codebasis-Indexierung durch Devin Desktop | mittel | Datenschutzmodell (Verlassen von Code an Anbieterinfrastruktur) | Datenschutz mit Anbieterdokumentation | verify: `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` |

## 2. Entscheidungen (Decision Records)

| ID | Entscheidung | Begründung | Alternativen | Status | Datum |
|---|---|---|---|---|---|
| D-01 | Vier Ebenen plus zwei Querschnittsebenen: Framework Core, Role Packs, Technology Packs, Project Overlay; ergänzt um Ebene B (organisationsweite Vorgaben) als Einbindungspunkt und Ebene E (aufgabenbezogene Informationen) als flüchtige Ebene | Vorgabe des Auftrags; Ebenen B und E sind für Separation of Concerns erforderlich | Drei Ebenen ohne Packs | entschieden (Vorschlag) | 2026-09-01 |
| D-02 | Regeln werden in zwei Formen gepflegt: kanonische Langform in `framework/` (tool-neutral) und kompakte Laufzeitform in `AGENTS.md` und `.devin/rules/` (Devin-spezifisch) | Tool Independence und Least Context; die Laufzeitform verweist auf die Langform | Nur Laufzeitform | entschieden (Vorschlag) | 2026-09-01 |
| D-03 | Skills liegen unter `.devin/skills/<skill-name>/` mit `SKILL.md` (normativ), `EXAMPLES.md` (erläuternd), `TESTS.md` (Testfälle) und `CHANGELOG.md` | Trennung normativ/erläuternd; Least Context (Beispiele werden nicht bei jedem Aufruf geladen) | Alles in SKILL.md | entschieden (Vorschlag) | 2026-09-01 |
| D-04 | Berechtigungen werden versioniert in `.devin/config.json` mit restriktivem Standard ausgeliefert (`deny` für Secrets und ausgeschlossene Pfade, `ask` für Schreib- und Ausführungsoperationen, `allow` nur für Leseoperationen im Arbeitsbereich) | Secure by Default | Berechtigungen nur lokal je Entwickler | entschieden (Vorschlag) | 2026-09-01 |
| D-05 | Der Permission-Modus `Bypass` ist im Framework untersagt; `Smart` und `Accept Edits` sind nur über dokumentierte Ausnahme für Kontrollstufe niedrig zulässig; Standard ist `Normal` | Human Accountability, Review before Adoption | Modusfreigabe je Entwickler | entschieden (Vorschlag) | 2026-09-01 |
| D-06 | Prioritätshierarchie 8-stufig mit Verschärfungsprinzip (niedrigere Ebenen dürfen höhere nur konkretisieren oder verschärfen, nie lockern) | Auflösung des Zielkonflikts zwischen „Core über Overlay" und „Overlay definiert projektspezifische Parameter" | Overlay über Core | entschieden (Vorschlag) | 2026-09-01 |
| D-07 | Kontextklassen K0 bis K3 als operatives Datenschutzmodell | Operationalisierbarkeit statt abstrakter Regeln | Freitextregeln | entschieden (Vorschlag) | 2026-09-01 |
| D-08 | Framework-Metadaten (ID, Version, Status, Owner) als Tabelle im Dateikörper, nicht im Frontmatter | Toleranz unbekannter Frontmatter-Schlüssel nicht belegt | Eigene Sidecar-Datei | entschieden (Vorschlag) | 2026-09-01 |
| D-09 | Versionierung nach Semantic Versioning; Erstfassung 0.1.0; Version 1.0.0 erst nach Pilotauswertung | Nachvollziehbarkeit, Roadmap | Datumsversionen | entschieden (Vorschlag) | 2026-09-01 |
| D-10 | Devin Cloud, Devin CLI und ACP-Fremdagenten sind im Framework als Erweiterungsmodule vorgesehen, standardmäßig deaktiviert | K-04 offen; Secure by Default | Cloud-Nutzung im Kern | entschieden (Vorschlag) | 2026-09-01 |

## 3. Annahmen

Unvermeidbare Annahmen der Erstfassung. Jede Annahme ist als solche gekennzeichnet und im Hauptdokument (Kapitel 29) gespiegelt.

| ID | Annahme | Warum unvermeidbar | Auswirkung, falls falsch |
|---|---|---|---|
| A-01 | Das Projekt-Repository kann im Wurzelverzeichnis um `AGENTS.md`, `.devin/` und die Framework-Verzeichnisse ergänzt werden | Devin Local lädt Root-Regeln nur aus dem geöffneten Workspace | Framework muss in einem separaten Workspace-Ordner betrieben werden; Root-Regeln entfallen |
| A-02 | Entwicklerinnen und Entwickler haben Schreibrechte auf lokale Feature-Branches, aber keine direkten Schreibrechte auf geschützte Branches | Üblicher Git-basierter Prozess laut verfügbarem Kontext | Zusätzliche Branch-Schutzregeln erforderlich |
| A-03 | Der bestehende Review- und Freigabeprozess (Merge Request, Review, CI) ist dokumentiert und wird unverändert beibehalten | Vorgabe des verfügbaren Kontexts | Framework-Freigabeschritte müssen an den tatsächlichen Prozess angepasst werden |
| A-04 | Die Verarbeitung von Anfragen erfolgt über die Infrastruktur des Anbieters und dessen Modellanbieter (kein lokales Modell) | Anbieterdokumentation beschreibt Cloud-Verarbeitung; lokale Modelle sind nicht dokumentiert | Kontextklassen könnten gelockert werden |
| A-05 | Die dokumentierten Mechanismen der Devin-CLI-Dokumentation (Berechtigungen, Skills, Hooks, Subagenten) gelten für Devin Local in Devin Desktop | Die Desktop-Dokumentation verweist ausdrücklich auf geteilte Modi und Mechanismen | Betroffene Bestandteile sind mit `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` markiert und im Arbeitspaket „Validierung" zu prüfen |
