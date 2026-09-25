# 3 Ziele und Nicht-Ziele

## 3.1 Ziele

| Nr. | Ziel | Umgesetzt durch |
|---|---|---|
| Z1 | Sicherer, kontrollierter, effizienter Assistenz-Einsatz mit klaren Grenzen | Kontrollschichten (Kap. 12), Betriebsmodi (Kap. 9), Risikoklassifizierung (Kap. 13), Delegationsverbote |
| Z2 | Konsistentes, schnelles Onboarding neuer Entwicklerinnen und Entwickler | Onboarding-Paket (Kap. 24), lesende Skills, Erklärvorlagen |
| Z3 | Kontrollierte, aufgabenbezogene Kontextbereitstellung | Kontextklassen K0–K3, Overlay-Manifest, technische Sperren (Kap. 11) |
| Z4 | Wiederverwendbarkeit über Projekte mit minimalem Anpassungsaufwand | Ebenenarchitektur, austauschbares Overlay, Adoption Guide (Kap. 7, 8, 28) |
| Z5 | Unveränderte Geltung bestehender Qualitäts- und Freigabeprozesse | P6, Review-Regeln, MR-Vermerk (Kap. 10, 14, 22) |
| Z6 | Nachvollziehbarkeit und Auditierbarkeit jedes KI-Einsatzes | Ergebnisberichte, Nutzungsvermerke, Versionsketten (Kap. 25) |
| Z7 | Pflegbarkeit und Prüfbarkeit des Frameworks selbst | Governance, Testkatalog, Validierungsskripte (Kap. 25, 26) |
| Z8 | Messbarkeit von Nutzen, Qualität, Risiken und Akzeptanz | Pilotkonzept und Metriken (Kap. 27) |
| Z9 | Übertragbarkeit der Prinzipien auf andere KI-Werkzeuge | Tool Independence: kanonische Ebene getrennt von der Laufzeitschicht (Kap. 8, 15) |

## 3.2 Nicht-Ziele

| Nr. | Nicht-Ziel | Begründung und Abgrenzung |
|---|---|---|
| N1 | Maximierung des Automatisierungsgrads oder „autonome" Entwicklung | Human Accountability ist Grundprinzip; Autonomie-Modi sind untersagt beziehungsweise ausnahmepflichtig |
| N2 | Ersatz bestehender Prozesse, Reviews, Gates oder Rollen | Das Framework ergänzt; es ersetzt nichts (P6) |
| N3 | Rechtliche Bewertung oder Compliance-Freigabe (Datenschutzrecht, Lizenzrecht, KI-Regulierung) | Liegt bei den zuständigen Rollen der Organisation; das Framework liefert operative Anschlusspunkte und benennt Prüfbedarfe (K-06) |
| N4 | Bewertung oder Überwachung von Personen anhand von Nutzungs- oder Pilotdaten | Ausdrücklich ausgeschlossen (V7, Metrik-Grundsätze) |
| N5 | Produktdokumentation oder Schulung für einen KI-Client als Produkt | Das Framework referenziert die offizielle Dokumentation; es dupliziert sie nicht |
| N6 | Vollständige technologie- oder branchenspezifische Regelwerke in der Erstfassung | Technology Packs entstehen projektbezogen; die Struktur dafür ist Teil des Frameworks |
| N7 | Abdeckung anderer Einsatzformen (Cloud-Sitzungen, Kommandozeilenbetrieb, Fremdagenten) im Kern der Erstfassung | Als Erweiterung vorgesehen, standardmäßig deaktiviert (D-10, K-04) |
| N8 | Garantie fehlerfreier KI-Ergebnisse | Unerreichbar; das Framework macht Fehler früh sichtbar und begrenzt ihre Wirkung |
