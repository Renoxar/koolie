# Overlay-Muster „Infrastruktur als Code“

| Attribut | Wert |
|---|---|
| ID | `FW-OVL-INFRASTRUCTURE` |
| Name | `infrastructure` |
| Version | `0.1.0` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Baut auf | `general` |
| Im Dialog | für Terraform, Kubernetes und Betriebskonfiguration, baut auf general auf |
| Gewählt über | `python .koolie/core/install.py --overlay infrastructure` – **nur bei der Erstinstallation** |
| Wirkung | alles aus `general`, dazu weitere Sperrwerte für diesen Projekttyp |

## Zweck

Für Repositorien mit Infrastruktur als Code: Terraform oder OpenTofu, Kubernetes-Manifeste, Helm, Ansible.

Gewählt wird genau ein Muster. Dieses Muster baut auf `general` auf: Es übernimmt dessen Werte
und Dokumente und ergänzt Werte, die für diesen Projekttyp ohne weitere Kenntnis des Projekts
sicher sind. Es gilt derselbe Grundsatz wie dort: **Das Muster sperrt, es gibt nichts frei.**
Jeder Wert steht ausschließlich in einem `deny`-Eintrag; passt einer nicht, sperrt er eine
Datei, die es im Projekt nicht gibt.

## Die Werte

Zusätzlich zu den Werten von `general`. Gelesen wird die Tabelle wie bei `general`.

| Platzhalter | Werte | Warum ohne Kenntnis des Projekts sicher |
|---|---|---|
| `<CI_CONFIG_PATHS>` | `atlantis.yaml` | Die Planungs- und Anwendungsläufe von Terraform sind Teil der Auslieferung |
| `<QUALITY_GATE_CONFIG_PATHS>` | `.tflint.hcl`, `.checkov.yml`, `.checkov.yaml`, `.trivyignore` | Regeln und Ausnahmen der Prüfwerkzeuge für Infrastrukturcode; eine Ausnahme abzuschalten, ist eine Freigabe |
| `<EXCLUDED_PATHS>` | `**/*.tfvars`, `**/*.tfvars.json`, `**/.terraform/**`, `**/kubeconfig*`, `**/*.kubeconfig`, `**/*.pem`, `**/*.key`, `**/*.pfx` | Variablendateien tragen oft Zugangsdaten, `.terraform/` Zustand und Anbieterdaten, Kubeconfig und Schlüsseldateien Zugänge (K3). Eine Variablendatei ohne Geheimnisse gibt das Projekt in `OVERLAY.md` Abschnitt 4 wieder frei |

Wie die Werte in Overlay, Laufzeitfassung und Berechtigungsdatei kommen und was danach dem
Projekt gehört, steht in `general.md`. Eigene Dokumente bringt dieses Muster nicht mit.

## Änderungsverlauf

| Version | Datum | Änderung |
|---|---|---|
| `0.1.0` | 2026-10-06 | Erstfassung |
