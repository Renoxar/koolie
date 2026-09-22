# 4 Geltungsbereich

## 4.1 Sachlich

Das Framework gilt für den Einsatz eines **KI-Codierassistenten** in Softwareentwicklungsprojekten mit Git-basiertem Entwicklungsprozess und den im verfügbaren Kontext genannten generischen Werkzeugklassen (Issue Tracking wie `<ISSUE_TRACKER>`, Git-Repository, Merge beziehungsweise Pull Requests, `<CI_CD_PLATFORM>`, statische Codeanalyse, automatisierte Tests, technische Dokumentation, Teamkommunikation und Wissensmanagement). Es umfasst Governance, Datenschutz- und Sicherheitsmodell, Arbeitsmodell, Skills, Prompts, Checklisten, Entscheidungsbäume, Onboarding, Framework-Qualitätssicherung, Pilotierung und Übernahme.

Vorausgesetzt ist die **lokale, beobachtete** Nutzung: Der Assistent läuft in der Entwicklungsumgebung, eine Person verfolgt die Sitzung. Nicht Teil des Kerngeltungsbereichs – strukturell vorbereitet und standardmäßig deaktiviert (D-10, `<TBD: Freigabe Cloud/CLI-Nutzung>`): Cloud-Sitzungen, Kommandozeilenbetrieb, automatisierte Reviews, Fremdagenten über offene Agentenprotokolle sowie Hintergrundläufe ohne beobachtende Person. Eine Freigabe dieser Formen erfordert eine Erweiterung des Sicherheitsmodells über den Änderungsprozess.

**Welcher** Assistent zum Einsatz kommt, legt das gewählte Client Pack fest (Kap. 7a). Der Geltungsbereich ist davon unabhängig; die Durchsetzungstiefe der Zusagen ist es nicht – sie steht in der Fähigkeitsmatrix des Packs und ist vor Inbetriebnahme zu bewerten.

## 4.2 Persönlich

Es gilt für alle Personen, die im Geltungsbereich eines aktiven Project Overlays mit dem Assistenten arbeiten oder dessen Ergebnisse prüfen und freigeben – zunächst für die Rolle Softwareentwicklung; weitere Rollen (Softwarearchitektur, Requirements Engineering, Testing und QA, DevOps, Dokumentation, Code Review) sind über Role Packs strukturell vorgesehen (Ebene 6). Ohne dokumentierte Onboarding-Freigabe ist nur begleitetes Arbeiten zulässig.

## 4.3 Organisatorisch und zeitlich

Je Projekt wird der Geltungsbereich durch das Project Overlay konkretisiert (Repositorys, Pfade, Rollen, Freigaben); ohne aktives Overlay ist produktiver Einsatz unzulässig (nur Onboarding-Übungen auf dem synthetischen Übungsrepository). Voraussetzungen auf Organisationsebene – Werkzeugfreigabe, Datenschutz- und Vertragsprüfung, administrativ gesetzte Team-Einstellungen – sind Eingangsbedingungen (Klärungspunkte K-04 bis K-06) und werden über die Ebene der Organisationsvorgaben eingebunden. Das Framework gilt ab Übernahme (Adoption) in der jeweils referenzierten Release-Version bis zur Deaktivierung des Overlays.

## 4.4 Produktstand und Grenzen der Aussagen

Das Framework legt keinen Produktstand fest – ein Client Pack tut es. Jedes Pack nennt in seinem Kopf die **geprüfte Clientversion** und das Datum der Prüfung; ohne diese Angabe ist keine Einstufung `[TECHNISCH]` zulässig (Kap. 7a).

Für das in diesem Dokument durchgehend verwendete Pack `devin-desktop` ist der referenzierte Produktstand Devin Desktop nach dem Rebranding vom 02.06.2026 (recherchierte Version 3.8.20 vom 21.08.2026) mit dem Agenten Devin Local. Cascade-spezifische Mechanismen (Workflows, Memories) werden nicht verwendet, da laut Dokumentation nicht unterstützt `[DOK]`.

Alle produktbezogenen Aussagen tragen Belegstatus. **Keine Einstufung eines Client Packs ist bislang gegen eine reale Installation belegt**; die verbindliche Zielversion und die Bestätigung der Mechanismen sind Gegenstand von AP2 (`<TBD: verbindliche Zielversion>`).
