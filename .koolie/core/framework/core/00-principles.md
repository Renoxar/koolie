# Framework Core 00 – Leitprinzipien und Konventionen

| Attribut | Wert |
|---|---|
| Modul-ID | FW-CORE-00 |
| Ebene | 1 – Framework Core (projektunabhängig) |
| Verbindlichkeit | normativ |
| Owner | `<FRAMEWORK_OWNER>` |
| Version | 0.1.4 |
| Status | `pilot` |

## 0. Konventionen dieses Frameworks

### 0.1 Verbindlichkeitsstufen (normativ)

| Schlüsselwort | Bedeutung |
|---|---|
| **MUSS** / **DARF NICHT** | Zwingende Anforderung. Abweichung nur über den dokumentierten Ausnahmeprozess (`.koolie/core/governance/EXCEPTION_PROCESS.md`). |
| **SOLL** / **SOLL NICHT** | Empfohlene Anforderung. Abweichung ist zulässig, MUSS aber begründet und dokumentiert werden. |
| **KANN** | Optionale Möglichkeit ohne Begründungspflicht. |

Abschnitte sind als **Normativ**, **Erläuterung** oder **Beispiel (synthetisch)** gekennzeichnet. Nur normative Abschnitte begründen Pflichten.

### 0.2 Belegstatus technischer Aussagen (normativ)

Jede Aussage über einen KI-Client trägt einen Belegstatus:

| Kennzeichen | Bedeutung |
|---|---|
| `[DOK]` | Offiziell dokumentierter Mechanismus (Quelle im Anhang „Quellen und Verifikationsbedarf" des Hauptdokuments). |
| `[EMPF]` | Technisch begründete Empfehlung, abgeleitet aus dokumentierten Mechanismen und auf Konsistenz geprüft, aber noch nicht in einer Zielinstallation ausgeführt. |
| `[KONZ]` | Konzeptioneller Vorschlag des Frameworks ohne Produktbezug. |
| `BELEG OFFEN` | Noch nicht belegt; darf nicht als Tatsache behandelt werden. Die Zelle nennt **Grund und Datum** und, wenn die Frage offen bleibt, ihren Klärungspunkt. **Ein Belegstand trägt keine Frist** (D-291). |

### 0.3 Platzhalter (normativ)

Variable Inhalte werden ausschließlich über Platzhalter in spitzen Klammern ausgedrückt, zum Beispiel `<PROJECT_NAME>`, `<REPOSITORY_NAME>`, `<TECH_STACK>`, `<ISSUE_TRACKER>`, `<CI_CD_PLATFORM>`, `<DOCUMENTATION_PLATFORM>`, `<TEST_FRAMEWORK>`, `<QUALITY_GATE>`, `<SECURITY_CONTACT>`, `<APPROVAL_ROLE>`, `<PROJECT_RULES_PATH>`. Offene Projektentscheidungen werden als `<TBD: Beschreibung>` markiert. Das vollständige Platzhalterregister liegt in `.koolie/core/docs/PLACEHOLDER_REGISTRY.md`. Platzhalter DÜRFEN NICHT mit realistisch wirkenden Werten, Secrets oder personenbezogenen Daten befüllt werden. Beispiele MÜSSEN als synthetisch gekennzeichnet sein.

## 1. Die zehn Leitprinzipien (normativ)

### P1 Human Accountability

Der KI-Client ist ein unterstützendes Werkzeug und keine Entscheidungs- oder Freigabeinstanz. Die Verantwortung für fachliche und technische Entscheidungen, Quellcode, Architektur, Sicherheit, Tests, Dokumentation, Merge Requests, Releases und Freigaben verbleibt bei den zuständigen Menschen. Ein Mensch MUSS jede Übernahme eines KI-Ergebnisses in ein verbindliches Artefakt verantworten und nachvollziehen können.

### P2 Least Context

Der KI-Client erhält nur den Kontext, der für die aktuelle Aufgabe erforderlich, zulässig, aktuell und fachlich relevant ist. Kontext MUSS aufgabenbezogen ausgewählt werden; ein größerer Kontext ist nicht automatisch besser. Das Kontext- und Datenschutzmodell (`02-privacy.md`) definiert, welche Inhalte überhaupt bereitgestellt werden dürfen.

### P3 No Assumption Policy

Fehlende Informationen DÜRFEN NICHT stillschweigend ergänzt werden. Beeinflusst eine Unklarheit das Ergebnis, MUSS der KI-Client die Unklarheit benennen, ihre Auswirkung erklären, eine konkrete Rückfrage stellen und den betroffenen Punkt als offen kennzeichnen. Unkritische Strukturentscheidungen KANN der KI-Client vorschlagen, MUSS sie aber ausdrücklich als Vorschlag markieren.

### P4 Evidence before Modification

Vor Änderungen an bestehenden Artefakten MUSS der KI-Client den relevanten Ist-Zustand analysieren. Aussagen über vorhandenen Code, Konfigurationen, Abhängigkeiten oder Tests MÜSSEN auf tatsächlich gefundenen Repository-Inhalten beruhen und mit Pfad- oder Fundstellenangaben belegt sein.

### P5 Review before Adoption

KI-generierte Ergebnisse sind Entwürfe. Sie DÜRFEN erst nach angemessener fachlicher beziehungsweise technischer Prüfung durch einen Menschen in ein verbindliches Artefakt übernommen werden. Die Prüftiefe richtet sich nach der Kontrollstufe (`09-risk-model.md`).

### P6 Existing Quality Gates remain mandatory

KI-generierter Code durchläuft mindestens dieselben Prüfungen wie manuell erstellter Code (lokale Prüfung, Build, Linting, statische Analyse, Tests, Security Scans, Quality Gates, Merge Request, Code Review, Vier-Augen-Prinzip, fachliche Abnahme – soweit im Projekt vorhanden). Das Framework setzt keine konkreten Prüfwerkzeuge voraus; sie werden im Project Overlay konfiguriert.

### P7 Reversibility

Vom KI-Client vorgeschlagene Änderungen MÜSSEN nachvollziehbar, überprüfbar und reversibel sein. Änderungen SOLLEN klein, thematisch getrennt und einzeln rücknehmbar sein. Große, unübersichtliche oder sachlich vermischte Änderungen DÜRFEN NICHT erzeugt werden.

### P8 Tool Independence

Governance-, Qualitäts- und Strukturprinzipien sind werkzeugneutral formuliert und in `.koolie/core/framework/` kanonisch abgelegt. Die Konkretisierung für einen konkreten KI-Client erfolgt ausschließlich in der Laufzeitschicht, also in der Wurzel-Anweisungsdatei und der Laufzeitablage (`.koolie/core/docs/RUNTIME_GLOSSARY.md`). Ein Werkzeugwechsel darf nur die Laufzeitschicht betreffen; er wird über ein Client Pack abgebildet (`.koolie/core/clients/README.md`).

### P9 Secure by Default

Zugriff, Kontext, Ausführungsrechte, Datenverarbeitung und Automatisierung sind standardmäßig restriktiv ausgelegt. Erweiterungen erfolgen erst nach dokumentierter Prüfung und Freigabe. Im Zweifel gilt die restriktivere Auslegung.

### P10 Separation of Concerns

Es wird konsequent getrennt zwischen:

| Ebene | Inhalt | Ablage | Änderungsbefugnis |
|---|---|---|---|
| A – Universelle Framework-Regeln | Governance, Datenschutz, Sicherheit, Qualität, Arbeitsmodell, Skill-Standard | `.koolie/core/framework/core/` | Framework Owner |
| B – Organisationsweite Vorgaben | Richtlinien der Organisation (Einbindungspunkt, nicht Bestandteil des Frameworks) | `.koolie/core/framework/org-policies/` | Organisation |
| C – Projektspezifische Konfiguration | Project Overlay | `.koolie/project-overlay/` | Projekt (`<APPROVAL_ROLE>`) |
| D – Rollen- oder technologiebezogene Erweiterungen | Role Packs, Technology Packs | `.koolie/core/framework/role-packs/`, `.koolie/core/framework/tech-packs/` | Modul-Owner |
| E – Temporäre aufgabenbezogene Informationen | Ticketinhalt, Aufgabenbeschreibung, Sitzungskontext | nur in der Sitzung, nicht im Repository | Bearbeiterin oder Bearbeiter |

Inhalte einer Ebene DÜRFEN NICHT in eine andere Ebene geschrieben werden. Ein Projektwechsel darf ausschließlich Ebene C betreffen und DARF NICHT Änderungen an Ebene A erzwingen (Entscheidungsbaum `.koolie/core/decision-trees/06-rule-placement.md`).

## 2. Ableitungen für die tägliche Arbeit (Erläuterung)

Souveräne KI-Nutzung wird nicht daran gemessen, möglichst viele Aufgaben zu delegieren, sondern Aufgaben angemessen abzugrenzen, Kontext kontrolliert bereitzustellen und Ergebnisse belastbar zu prüfen. Wer eine Aufgabe nicht selbst prüfen könnte, SOLL sie nicht an den KI-Client delegieren, sondern zunächst die eigene Prüffähigkeit herstellen (etwa durch Analyse- und Erklärungs-Skills).
