# 9 Betriebsmodi

Jede Devin-Aufgabe läuft in genau einem von fünf Betriebsmodi; der Modus wird im Preflight festgelegt (Entscheidungsbaum 3) und begrenzt Schreibrechte, Befehlsausführung und erwartete Ausgabe. Ohne ausdrückliche Angabe gilt der nur lesende Modus M1; ein Moduswechsel innerhalb einer Sitzung erfordert eine ausdrückliche menschliche Anweisung und wird im Ergebnisbericht vermerkt.

| Modus | Zweck in einem Satz | Schreiben | Befehle | Typische Skills |
|---|---|---|---|---|
| **M1 Read-only Analysis** | Verstehen, prüfen, erklären – Befunde nur mit Fundstellen | nein | keine (bei Review-Unterstützung: nur lesende Git-Befehle) | `fw-repo-analyze`, `fw-code-explain`, `fw-change-analyze`, `fw-error-analyze`, `fw-review-support` |
| **M2 Guided Planning** | prüfbaren Änderungsplan erarbeiten – mit Halte-Punkt vor jeder Umsetzung | nur Plan-Datei außerhalb des Quellcodes | nein | `fw-plan`, `fw-bugfix-prepare` |
| **M3 Controlled Modification** | freigegebene Änderung in kleinen, berichteten Schritten umsetzen | nur im freigegebenen Scope | nur freigegebene Build-/Test-/Lint-Befehle | `fw-change-small`, `fw-refactor` |
| **M4 Test and Validation** | Tests erstellen und ausführen, Aussagekraft bewerten | nur `<TEST_PATHS>` | nur freigegebene Testbefehle | `fw-tests` |
| **M5 Documentation Support** | Dokumentation aus dem belegten Code-Stand pflegen | nur `<DOC_PATHS>` | nur lesende Git-Befehle | `fw-docs-update`, `fw-mr-description` |

Jeder Modus ist im Modul FW-CORE-05 (vollständig in Kapitel 10 wiedergegeben) mit denselben sieben Merkmalen normiert: Zweck, zulässige Aktionen, verbotene Aktionen, benötigter Kontext, Prüfpflichten, Abbruchkriterien, erwartete Ausgabe – ergänzt um die konkrete Devin-Umsetzung mit Belegstatus (Plan-Modus `[DOK]`, Skill-`allowed-tools` und -`permissions` `[DOK]`, Permission-Modus Normal `[DOK]`, Hook-Absicherung `[EMPF]`). Die Zulässigkeit je Kontrollstufe regelt Kapitel 13: Ab Stufe mittel setzt M3 einen bestätigten Plan voraus, ab Stufe hoch eine dokumentierte Freigabe mit begleitender Person; M4 bleibt auf Stufe hoch auf testseitige Artefakte beschränkt.

Bewusste Festlegungen dieser Erstfassung: Der Devin-Permission-Modus **Normal** ist Standard für alle Modi; **Bypass** ist untersagt und **Smart**/**Accept Edits** sind nur über dokumentierte Ausnahme für Stufe niedrig zulässig (D-05). Hintergrund-Subagenten sind für M3 untersagt; für M1 ist das nur lesende Profil zulässig. Parallele Agentensitzungen (Agent Command Center `[DOK]`) sind auf unabhängige Aufgaben der Stufe niedrig begrenzt.
