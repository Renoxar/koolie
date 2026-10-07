# Overlay-Muster „Java und Spring“

| Attribut | Wert |
|---|---|
| ID | `FW-OVL-JAVA-SPRING` |
| Name | `java-spring` |
| Version | `0.1.0` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Baut auf | `general` |
| Im Dialog | für Java-Projekte mit Maven oder Gradle, baut auf general auf |
| Gewählt über | `python .koolie/core/install.py --overlay java-spring` – **nur bei der Erstinstallation** |
| Wirkung | alles aus `general`, dazu weitere Sperrwerte für diesen Projekttyp |

## Zweck

Für Backend-Projekte in Java, typischerweise mit Spring, Maven oder Gradle.

Gewählt wird genau ein Muster. Dieses Muster baut auf `general` auf: Es übernimmt dessen Werte
und Dokumente und ergänzt Werte, die für diesen Projekttyp ohne weitere Kenntnis des Projekts
sicher sind. Es gilt derselbe Grundsatz wie dort: **Das Muster sperrt, es gibt nichts frei.**
Jeder Wert steht ausschließlich in einem `deny`-Eintrag; passt einer nicht, sperrt er eine
Datei, die es im Projekt nicht gibt.

## Die Werte

Zusätzlich zu den Werten von `general`. Gelesen wird die Tabelle wie bei `general`.

| Platzhalter | Werte | Warum ohne Kenntnis des Projekts sicher |
|---|---|---|
| `<QUALITY_GATE_CONFIG_PATHS>` | `checkstyle-suppressions.xml`, `spotbugs-exclude.xml`, `spotbugs-include.xml`, `pmd-ruleset.xml`, `config/checkstyle/**`, `config/pmd/**`, `config/spotbugs/**` | Regeln und Ausnahmen der verbreiteten Analysewerkzeuge für Java. Wer sie ändert, ändert die Schwelle; das bleibt Menschen vorbehalten |
| `<EXCLUDED_PATHS>` | `**/*.jks`, `**/*.p12`, `**/*.keystore`, `**/*.truststore` | Schlüssel- und Zertifikatsspeicher tragen private Schlüssel (K3). `application-*.yml` bleibt lesbar: Eine Lesesperre auf die Konfiguration wäre ein Hindernis, keine Verschärfung |

Wie die Werte in Overlay, Laufzeitfassung und Berechtigungsdatei kommen und was danach dem
Projekt gehört, steht in `general.md`. Eigene Dokumente bringt dieses Muster nicht mit.

## Änderungsverlauf

| Version | Datum | Änderung |
|---|---|---|
| `0.1.0` | 2026-10-06 | Erstfassung |
