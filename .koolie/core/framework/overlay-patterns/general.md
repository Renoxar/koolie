# Overlay-Muster „General Development“

| Attribut | Wert |
|---|---|
| ID | `FW-OVL-GENERAL` |
| Name | `general` |
| Version | `0.2.2` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Gewählt über | `python .koolie/core/install.py --overlay general` – **nur bei der Erstinstallation** |
| Wirkung | füllt drei Pfadplatzhalter einmal in Overlay, Laufzeitfassung und Berechtigungsdatei; legt sechs Musterdokumente allgemeiner Praktiken an und registriert sie im Manifest |
| Nachweis | Sonden `M355` bis `M355e` und `M359` bis `M359c` in `.koolie/core/tests/scripts/probe-pruefungen.py` |

## Zweck

Ohne Muster beginnt ein Projekt mit einem leeren Overlay: Jeder Platzhalter ist ein Schlitz,
und solange er offen ist, sperrt die Berechtigungsdatei an seiner Stelle nichts. Dieses Muster
füllt die Schlitze, deren Wert sich ohne Kenntnis des Projekts sicher angeben lässt – und nur
diese.

Außerdem liefert es Dokumente mit allgemein anerkannten Praktiken der Softwareentwicklung, die
auf jedes Projekt passen (Abschnitt *„Die Dokumente“*).

## Der Grundsatz: Das Muster sperrt, es gibt nichts frei

Der Kern darf keine Projektwerte enthalten (Entscheidungsbaum 6, Prüfungen 6 und 14). Deshalb
**verschärft jeder Wert dieses Musters**: Er steht ausschließlich in einem `deny`-Eintrag. Passt
ein Wert nicht, sperrt er eine Datei, die es im Projekt nicht gibt, und kostet nichts.

Nicht gefüllt wird alles, was etwas freigibt oder das Projekt beschreibt: `<ALLOWED_PATHS>`,
`<TEST_PATHS>`, `<DOC_PATHS>`, `<READ_ONLY_PATHS>`, die drei Befehlsschlitze, Rollen, Status,
Freigaben und die Ergebnisse der Datenschutz- und Vertragsprüfung. `install.py` nimmt aus dieser
Datei nur die drei Platzhalter der Tabelle unten an und bricht bei jedem anderen ab.

## Die Werte

Gelesen wird diese Tabelle – über die Platzhalterzelle, nicht über eine Spaltennummer.
Jeder Wert steht in einer eigenen Codespanne.

| Platzhalter | Werte | Warum ohne Kenntnis des Projekts sicher |
|---|---|---|
| `<CI_CONFIG_PATHS>` | `.github/workflows/**`, `.gitlab-ci.yml`, `.gitea/workflows/**`, `Jenkinsfile`, `azure-pipelines.yml`, `bitbucket-pipelines.yml`, `.circleci/**` | Die üblichen Ablagen der verbreiteten CI-Werkzeugklassen. Gesperrt wird nur das Schreiben; eine Merge-Request-Vorlage neben `.github/workflows/` bleibt lesbar |
| `<QUALITY_GATE_CONFIG_PATHS>` | `.editorconfig`, `.eslintrc*`, `eslint.config.*`, `.prettierrc*`, `.stylelintrc*`, `sonar-project.properties`, `codecov.yml`, `.codecov.yml`, `.coveragerc`, `.pylintrc`, `.flake8`, `ruff.toml`, `.golangci.yml`, `checkstyle.xml` | Eigenständige Konfigurationsdateien von Linter, Formatierer, Analyse und Abdeckung – Schwellenwerte ändert der KI-Client nie (`OVERLAY.md` Abschnitt 7). Nicht enthalten sind Sammeldateien wie `pyproject.toml` oder `package.json`, die auch Abhängigkeiten tragen; sie zu sperren, wäre eine Aussage über das Projekt |
| `<EXCLUDED_PATHS>` | `**/*.tfstate`, `**/*.tfstate.*`, `**/*.dump` | Zustandsdateien einer Infrastrukturbeschreibung tragen Zugangsdaten im Klartext, Datenbankabzüge echte Daten (K3). Nicht enthalten sind `deploy/**`, `infra/**` oder `config/prod/**` aus dem Beispiel der Vorlage: Sie setzen ein Verzeichnislayout voraus, und eine Lesesperre auf ein Arbeitsverzeichnis wäre ein Hindernis, keine Verschärfung |

## Wie die Werte in das Projekt kommen

`install.py --overlay general` schreibt bei der Erstinstallation drei Träger aus dieser
Tabelle, und zwar genau einmal:

| Träger | Was gefüllt wird |
|---|---|
| `.koolie/project-overlay/OVERLAY.md` | die Spalte **Wert** der drei Zeilen in Abschnitt 4; ein Eintrag im Änderungsverlauf nennt Muster und Version |
| `<RULES_DIR>/20-project-overlay.md` | der Wert hinter `<EXCLUDED_PATHS>` – die beiden anderen Platzhalter führt die Laufzeitfassung nicht |
| `<PERMISSIONS_FILE>` | jeder `deny`-Eintrag der Kernquelle, der einen der drei Platzhalter trägt, wird zu einem Eintrag je Wert – dieselben Schlitze, keiner mehr |

Das Muster liefert nur den Anfangszustand. Danach gehören alle drei Dateien dem Projekt;
`install.py --update` liest das Muster nie wieder. Wer einen Wert später ändert, zieht ihn in
allen Trägern von Hand nach; Prüfung 59 meldet eine Abweichung bei `<EXCLUDED_PATHS>`.

Bei `openai-codex` (B3 und B5 `[NICHT ABBILDBAR]`) kennt die Berechtigungsschicht keine
Musterform, und nur ein Teil kommt an: Ein Teilbaum (`.github/workflows/**`) und ein einzelner
Dateiname (`Jenkinsfile`) werden zu einem Pfad mit Zugriffsart `read`, ein Namensmuster mit `*`
(`**/*.tfstate`, `.eslintrc*`) erreicht die Datei nicht. Das Pack nennt diese Grenze in
Abschnitt 5.

## Die Dokumente

Ein Dokument gibt nichts frei, aber es beschreibt. Deshalb darf es nur beschreiben, was für
jedes Projekt gilt:

- nur allgemein anerkannte, werkzeug- und sprachneutrale Praktiken;
- keine Schwellenwerte (Abdeckung, Methodenlänge, Anzahl Reviewer), keine Werkzeugnamen, keine
  Vorgaben, die Vorgehensmodell, Teamgröße oder Plattform voraussetzen;
- keine Wiederholung des Kerns. Was der Kern für KI-unterstützte Arbeit regelt –
  `04-quality.md` Abschnitte 2 und 3, `07-review-rules.md`, die Checklisten 03, 05, 06, 07 und
  08 –, wird verwiesen. Jedes Dokument sagt im Abschnitt *„Verhältnis zum Framework“*, wo die
  Grenze liegt; bei Widerspruch gilt der Kern.

Was nicht überall passt, kommt nicht hinein, auch nicht als Beispiel. Projektfestlegungen
gehören in den Abschnitt *„Projektspezifische Ergänzungen“* am Ende jedes Dokuments und in die
zugehörige Zeile in `OVERLAY.md`.

Diese Tabelle beschreibt die Ablage unter `overlay-patterns/general/documents/<typ>/`;
`install.py` hält ihre erste Spalte gegen die Verzeichnisse und bricht ab, wenn beide
auseinanderlaufen.

| Typ | Was das Dokument enthält | Was bewusst fehlt |
|---|---|---|
| `coding-guidelines` | Lesbarkeit, eine Verantwortung je Einheit, KISS/DRY/YAGNI, Fehlerbehandlung, Kommentare zum Warum, kleine Schritte | Benennungsschema, Formatierer, Längengrenzen; die Pfadfinderregel über den Scope hinaus (widerspräche Q1 und RV1) |
| `definition-of-ready` | Zweck, prüfbare Akzeptanzkriterien, Abgrenzung, Größe, Abhängigkeiten, offene Fragen, nicht-funktionale Anforderungen | Schätzgrößen, Vorgehensmodell; die KI-Zusatzkriterien aus `OVERLAY.md` Abschnitt 11 |
| `definition-of-done` | Akzeptanzkriterien belegt, getestet, Prüfungen grün, begutachtet, Dokumentation, integriert, offene Punkte sichtbar | Abdeckungsgrenzen, Freigabestufen; die KI-DoD aus `04-quality.md` Abschnitt 3 |
| `quality` | Tests als Teil der Änderung, Fehler zuerst per Test, instabile Tests sind Fehler, Review-Grundsätze, Prüfungen nicht umgehen | Testwerkzeuge, Testpyramide in Zahlen, Anzahl Reviewer; die Prüfpunkte aus Checkliste 05 und `07-review-rules.md` |
| `security` | Sicherheit als Anforderung, minimale Rechte, gestaffelte Abwehr, sicher scheitern, sichere Voreinstellungen, Geheimnisse, Pflege der Abhängigkeiten | Verfahren, Bibliotheken, Schutzkonfiguration (K3); die Prüfpunkte aus Checkliste 06 und 07 |
| `branching-strategy` | Standard-Branch baubar, kurzlebige Branches, Integration über Merge Request, schlüssige Commits, gemeinsame Historie nicht umschreiben | ein Branching-Modell, Namensschema, Commit-Konvention (`OVERLAY.md` Abschnitt 10) |

Nicht mitgeliefert werden `architecture`, `roadmap`, `deployment`, `roles` und `glossary` – sie
beschreiben das Projekt – sowie `ai-governance` und `ai-process-model`, die der Kern selbst
trägt.

### Wie die Dokumente in das Projekt kommen

`install.py --overlay general` schreibt sie bei der Erstinstallation nach
`.koolie/project-overlay/documents/<typ>/muster-general.md` und ersetzt die drei
Beispieleinträge der Manifestvorlage durch einen Eintrag je Dokument:

| Feld | Wert | Warum |
|---|---|---|
| `context_class` | `K1` | allgemeines Wissen ohne Projektbezug |
| `status` | `entwurf` | ein Vorschlag, den niemand geprüft hat |
| `load` | `on-demand` | kein weiterer Träger je Client Pack; `summary` und `rule` wählt der Overlay Owner |
| `approved_by`, `approved_on` | Ausfüllschlitze | die Freigabe erteilt ein Mensch |

**Die Dokumente wirken erst, wenn der Overlay Owner sie freigibt.** Die Liste der freigegebenen
K1-Dokumente in der Laufzeitfassung bleibt ein Ausfüllschlitz, und einen offenen Wert behandelt
der KI-Client als nicht freigegeben. Bis dahin sind die Dokumente ein Anfang für Menschen; ein
ungeprüfter Text wird nicht verbindlich, nur weil er mitgeliefert wurde.

Kein weiterer Platzhalter wird gefüllt, auch nicht `<PROJECT_RULES_PATH>` oder die Pfade der
projektweiten DoR und DoD in `OVERLAY.md` Abschnitt 11 und 12 – das hieße, die Dokumente für
das Projekt zu erklären. Bestandsprojekte erreicht das Muster nicht; sie übernehmen einzelne
Dokumente von Hand (`.koolie/core/docs/ADOPTION_GUIDE.md` Abschnitt 3).

## Die Grenze zur Aktivierungsreife

Ein Overlay aus diesem Muster ist nicht aktivierungsreif, und das ist gewollt. Es lässt die
Pflichtwerte der Abschnitte 1, 5, 6, 13, 14 und 15 offen; ein Overlay, das
`--check-overlay-ready` von selbst bestünde, wäre aktivierungsreif, ohne dass jemand es geprüft
hat. Die Sonde `M355b` hält fest, dass eine frische Installation mit diesem Muster die Prüfung
nicht besteht.

## Änderungsverlauf

| Version | Datum | Änderung |
|---|---|---|
| `0.2.2` | 2026-10-02 | Sprachlich überarbeitet; Werte und Dokumente unverändert |
| `0.2.0` | 2026-09-25 | Sechs Musterdokumente allgemeiner Praktiken, im Manifest als `entwurf` registriert; Framework-Release `1.6.0` |
| `0.1.0` | 2026-09-25 | Erstfassung mit Framework-Release `1.5.0` |
