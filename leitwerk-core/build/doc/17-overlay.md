# 17 Projekt-Overlay

Das Project Overlay ist die einzige Stelle, an der ein Projekt das Framework konfiguriert. Die Vorlage enthält alle geforderten Abschnitte – Projektsteckbrief, technische Architektur, Repository-Struktur, erlaubte und ausgeschlossene Verzeichnisse, Build- und Testbefehle, Qualitätsprüfungen, Sprachen und Frameworks, Coding Conventions, Branching- und Merge-Modell, Definition of Ready und Done, zulässige Kontexte, ausgeschlossene Daten, Rollen und Freigaben, Eskalationsweg, projektspezifische Skills, dokumentierte Ausnahmen – durchgängig mit Platzhaltern und Ausfüllhinweisen, dazu den Aktivierungsmechanismus (Status `aktiv` erst nach Projektübernahme-Checkliste und strikter Validierung) und den Änderungsverlauf.

Kernstück der geforderten Overlay-Erweiterung ist der **Manifest-Mechanismus** (Abschnitt 19 der Vorlage): Künftige projektspezifische Dokumente – KI-Governance-Rahmenwerk, KI-Vorgehensmodell, Projektroadmap, Architekturvorgaben, Coding Guidelines, Definition of Ready, Definition of Done, Branching-Strategie, Deployment-Vorgaben, Security-Vorgaben, Qualitätsrichtlinien, Rollenbeschreibungen, Projektglossar – werden unter `project-overlay/documents/<typ>/` abgelegt (oder als Verweisblatt geführt), im Manifest mit Kontextklasse, Status, Freigabe und Ladeverhalten registriert und je nach Ladeverhalten als Kurzfassung (`summary`), bei Bedarf (`on-demand`), als eigene Overlay-Regeldatei (`rule`, der Regelablage `2N-*`) oder gar nicht (`never`) für den Assistenten wirksam. Nicht registrierte Dokumente gelten als K3. Der Framework Core bleibt dabei in jedem Fall unverändert.

## 17.1 Overlay-Vorlage

{{EMBED:leitwerk-core/templates/project-overlay/OVERLAY.md}}
## 17.2 Manifest-Vorlage

{{EMBED:leitwerk-core/templates/project-overlay/overlay-manifest.yaml:yaml}}
## 17.3 Laufzeitfassung (always-on-Regel)

Die kompakte, immer geladene Laufzeitfassung des Overlays – vom Projekt synchron zur Vorlage gepflegt, unter 6.000 Zeichen:

{{EMBED:<RULES_DIR>/20-project-overlay.md}}
## 17.4 Vorlage für Overlay-Regelerweiterungen

Für Dokumente mit Ladeverhalten `rule`:

{{EMBED:leitwerk-core/templates/rules/21-overlay-TEMPLATE.md.template}}
## 17.5 Begleitdateien

Regeln des Dokumentenverzeichnisses und Ausnahmeregister:

{{EMBED-RAW:leitwerk-core/templates/project-overlay/documents/README.md:1}}
{{EMBED-RAW:leitwerk-core/templates/project-overlay/exceptions/EXCEPTIONS.md:1}}
Ein vollständig ausgefülltes Beispiel (synthetisch) der Laufzeitfassung zeigt `leitwerk-core/examples/example-overlay-runtime.md` (im Repository enthalten).
