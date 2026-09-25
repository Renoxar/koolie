# Overlay-Muster „General Development“

| Attribut | Wert |
|---|---|
| Name | `general` |
| Version | `0.2.0` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Gewählt über | `python .koolie/core/install.py --overlay general` – **nur bei der Erstinstallation** (D-126) |
| Wirkung | füllt drei Pfadplatzhalter einmal in Overlay, Laufzeitfassung und Berechtigungsdatei (D-355); legt sechs Musterdokumente allgemeiner Praktiken an und registriert sie im Manifest (D-359, D-360) |
| Nachweis | Sonden `M355` bis `M355e` und `M359` bis `M359c` in `.koolie/core/tests/scripts/probe-pruefungen.py` |

## Zweck

Ein Projekt, das das Framework übernimmt, beginnt ohne diesen Parameter mit einem
**leeren** Overlay: Jeder Platzhalter ist ein Schlitz, und bis ein Mensch ihn füllt,
sperrt die Berechtigungsdatei an seiner Stelle nichts. Dieses Muster füllt die Schlitze,
deren Wert sich **ohne Kenntnis des Projekts** sicher angeben läßt – und nur diese.

Seit Version `0.2.0` liefert es außerdem **Dokumente**: allgemein anerkannte Praktiken
der Softwareentwicklung für die Bereiche des Overlays, die auf **jedes** Projekt passen
(Abschnitt *„Die Dokumente“*). Sie sind ein zweiter Gegenstand mit eigener Grenze.

## Der Grundsatz: Das Muster sperrt, es gibt nichts frei

🔴 **Ein mitgeliefertes Muster schlägt Projektwerte vor, und der Kern darf keine
enthalten** (Entscheidungsbaum 6, Prüfungen 6 und 14). Die Grenze ist deshalb keine
Auswahl nach Geschmack, sondern eine Richtung: **Jeder Wert dieses Musters verschärft.**
Er steht ausschließlich in einem `deny`-Eintrag; ein Wert, der auf ein Projekt nicht
paßt, sperrt eine Datei, die es dort nicht gibt, und kostet nichts.

➡️ **Nicht gefüllt wird deshalb alles, was etwas FREIGIBT oder das Projekt BESCHREIBT:**
`<ALLOWED_PATHS>`, `<TEST_PATHS>`, `<DOC_PATHS>`, `<READ_ONLY_PATHS>`, die drei
Befehlsschlitze, Rollen, Status, Freigaben und die Ergebnisse der Datenschutz- und
Vertragsprüfung. `install.py` nimmt aus dieser Datei **nur** die drei Platzhalter der
Tabelle unten an und bricht ab, wenn sie einen anderen führt – die Grenze steht im
Werkzeug, nicht nur in diesem Satz.

## Die Werte

Gelesen wird diese Tabelle – über die Platzhalterzelle, nicht über eine Spaltennummer.
Jeder Wert steht in einer eigenen Codespanne.

| Platzhalter | Werte | Warum ohne Kenntnis des Projekts sicher |
|---|---|---|
| `<CI_CONFIG_PATHS>` | `.github/workflows/**`, `.gitlab-ci.yml`, `.gitea/workflows/**`, `Jenkinsfile`, `azure-pipelines.yml`, `bitbucket-pipelines.yml`, `.circleci/**` | Die üblichen Ablagen der verbreiteten CI-Werkzeugklassen. Gesperrt wird nur das **Schreiben**; eine Merge-Request-Vorlage neben `.github/workflows/` bleibt lesbar (D-161) |
| `<QUALITY_GATE_CONFIG_PATHS>` | `.editorconfig`, `.eslintrc*`, `eslint.config.*`, `.prettierrc*`, `.stylelintrc*`, `sonar-project.properties`, `codecov.yml`, `.codecov.yml`, `.coveragerc`, `.pylintrc`, `.flake8`, `ruff.toml`, `.golangci.yml`, `checkstyle.xml` | Eigenständige Konfigurationsdateien von Linter, Formatierer, Analyse und Abdeckung – Schwellenwerte ändert der KI-Client nie (`OVERLAY.md` Abschnitt 7). ⚠️ **Bewußt nicht:** Sammeldateien wie `pyproject.toml` oder `package.json`, die neben der Prüfkonfiguration auch Abhängigkeiten tragen – sie zu sperren, wäre eine Aussage über das Projekt |
| `<EXCLUDED_PATHS>` | `**/*.tfstate`, `**/*.tfstate.*`, `**/*.dump` | Zustandsdateien einer Infrastrukturbeschreibung tragen Zugangsdaten im Klartext, Datenbankabzüge echte Daten (K3). ⚠️ **Bewußt nicht:** `deploy/**`, `infra/**` oder `config/prod/**` aus dem Beispiel der Vorlage – sie setzen ein Verzeichnislayout voraus, und eine Lesesperre auf ein Verzeichnis, in dem das Projekt arbeitet, ist keine Verschärfung, sondern ein Hindernis |

## Wie die Werte in das Projekt kommen

`install.py --overlay general` schreibt bei der Erstinstallation **drei** Träger aus dieser
Tabelle, und zwar genau einmal (D-353, D-355):

| Träger | Was gefüllt wird |
|---|---|
| `.koolie/project-overlay/OVERLAY.md` | die Spalte **Wert** der drei Zeilen in Abschnitt 4; ein Eintrag im Änderungsverlauf nennt Muster und Version |
| `<RULES_DIR>/20-project-overlay.md` | der Wert hinter `<EXCLUDED_PATHS>` – die beiden anderen Platzhalter führt die Laufzeitfassung nicht |
| `<PERMISSIONS_FILE>` | jeder `deny`-Eintrag der Kernquelle, der einen der drei Platzhalter trägt, wird zu einem Eintrag je Wert – **dieselben Schlitze, keiner mehr** |

⚠️ **Abgrenzung zu D-76.** Gelesen wird ein Träger des Kerns, nicht des Projekts, und
zugesagt ist der **Anfangszustand**, kein Kanal. Danach gehören alle drei Dateien dem
Projekt wie ohne Muster; `install.py --update` liest dieses Muster nie wieder. Ein
Projekt, das einen Wert später ändert, zieht ihn wie jeden anderen Wert von Hand nach –
**und Prüfung 59 findet die Abweichung für `<EXCLUDED_PATHS>`.**

⚠️ **Bei einem Client Pack, dessen Berechtigungsschicht keine Musterform kennt**
(`openai-codex`, B3 und B5 `[NICHT ABBILDBAR]`), kommt nur ein Teil an – gemessen an
einer Wegwerf-Installation: Ein Teilbaum (`.github/workflows/**`) und ein einzelner
Dateiname (`Jenkinsfile`) werden zu einem Pfad mit Zugriffsart `read`, ein Namensmuster
mit `*` (`**/*.tfstate`, `.eslintrc*`) erreicht die Datei nicht. Das Muster ändert daran
nichts, und das Pack sagt es in Abschnitt 5 selbst.

## Die Dokumente

🔴 **Die Regel „sperrt, gibt nichts frei“ gilt für Schlitzwerte, und Dokumente sind ein
zweiter Gegenstand mit eigener Grenze** (D-359). Ein Dokument gibt nichts frei, aber es
**beschreibt** – und darf deshalb nur beschreiben, was für jedes Projekt gilt:

- **nur allgemein anerkannte, werkzeug- und sprachneutrale Praktiken;**
- **keine Schwellenwerte** (Abdeckung, Methodenlänge, Anzahl Reviewer), **keine
  Werkzeugnamen**, **keine Vorgaben, die Vorgehensmodell, Teamgröße oder Plattform
  voraussetzen;**
- **keine Wiederholung des Kerns.** Was der Kern für KI-unterstützte Arbeit schon regelt
  – `04-quality.md` Abschnitte 2 und 3, `07-review-rules.md`, die Checklisten 03, 05, 06,
  07 und 08 –, wird verwiesen, nicht abgeschrieben. Jedes Dokument sagt in einem Abschnitt
  *„Verhältnis zum Framework“*, wo die Grenze liegt; bei Widerspruch gilt der Kern.

➡️ **Was davon nicht überall paßt, kommt nicht hinein** – auch nicht als Beispiel. Die
Stelle für Projektfestlegungen ist der Abschnitt *„Projektspezifische Ergänzungen“* am
Ende jedes Dokuments und die zugehörige Zeile in `OVERLAY.md`.

Diese Tabelle beschreibt die Ablage unter `overlay-patterns/general/documents/<typ>/`;
`install.py` hält ihre erste Spalte gegen die Verzeichnisse und bricht ab, wenn beide
auseinanderlaufen.

| Typ | Was das Dokument enthält | Was bewußt fehlt |
|---|---|---|
| `coding-guidelines` | Lesbarkeit, eine Verantwortung je Einheit, KISS/DRY/YAGNI, Fehlerbehandlung, Kommentare zum Warum, kleine Schritte | Benennungsschema, Formatierer, Längengrenzen; die Pfadfinderregel über den Scope hinaus (widerspräche Q1 und RV1) |
| `definition-of-ready` | Zweck, prüfbare Akzeptanzkriterien, Abgrenzung, Größe, Abhängigkeiten, offene Fragen, nicht-funktionale Anforderungen | Schätzgrößen, Vorgehensmodell; die KI-Zusatzkriterien aus `OVERLAY.md` Abschnitt 11 |
| `definition-of-done` | Akzeptanzkriterien belegt, getestet, Prüfungen grün, begutachtet, Dokumentation, integriert, offene Punkte sichtbar | Abdeckungsgrenzen, Freigabestufen; die KI-DoD aus `04-quality.md` Abschnitt 3 |
| `quality` | Tests als Teil der Änderung, Fehler zuerst per Test, instabile Tests sind Fehler, Review-Grundsätze, Prüfungen nicht umgehen | Testwerkzeuge, Testpyramide in Zahlen, Anzahl Reviewer; die Prüfpunkte aus Checkliste 05 und `07-review-rules.md` |
| `security` | Sicherheit als Anforderung, minimale Rechte, gestaffelte Abwehr, sicher scheitern, sichere Voreinstellungen, Geheimnisse, Pflege der Abhängigkeiten | Verfahren, Bibliotheken, Schutzkonfiguration (K3); die Prüfpunkte aus Checkliste 06 und 07 |
| `branching-strategy` | Standard-Branch baubar, kurzlebige Branches, Integration über Merge Request, schlüssige Commits, gemeinsame Historie nicht umschreiben | ein Branching-Modell, Namensschema, Commit-Konvention (`OVERLAY.md` Abschnitt 10) |

**Nicht mitgeliefert** werden `architecture`, `roadmap`, `deployment`, `roles` und
`glossary` – sie beschreiben das Projekt – sowie `ai-governance` und `ai-process-model`,
die der Kern selbst trägt.

### Wie die Dokumente in das Projekt kommen

`install.py --overlay general` schreibt sie bei der Erstinstallation nach
`.koolie/project-overlay/documents/<typ>/muster-general.md` und **ersetzt** die drei
Beispieleinträge der Manifestvorlage durch einen Eintrag je Dokument (D-360):

| Feld | Wert | Warum |
|---|---|---|
| `context_class` | `K1` | allgemeines Wissen ohne Projektbezug |
| `status` | `entwurf` | ein Vorschlag, den niemand geprüft hat |
| `load` | `on-demand` | kein weiterer Träger je Client Pack; `summary` und `rule` wählt der Overlay Owner |
| `approved_by`, `approved_on` | Ausfüllschlitze | die Freigabe erteilt ein Mensch |

🔴 **Die Dokumente wirken erst, wenn der Overlay Owner sie freigibt.** Die Liste der
freigegebenen K1-Dokumente in der Laufzeitfassung bleibt ein Ausfüllschlitz, und einen
offenen Wert behandelt der KI-Client als nicht freigegeben. ⚠️ **Preis, benannt:** Bis
dahin haben sie keine Wirkung auf den Client – sie sind ein Anfang für Menschen. Das ist
die Richtung von D-355 an einem Gegenstand, der beschreibt statt sperrt: Ein ungeprüfter
Text wird nicht verbindlich, nur weil er mitgeliefert wurde.

⚠️ **Kein weiterer Platzhalter wird gefüllt**, auch nicht `<PROJECT_RULES_PATH>` oder die
Pfade der projektweiten DoR und DoD in `OVERLAY.md` Abschnitt 11 und 12 – sie zu setzen,
hieße, die Dokumente für das Projekt zu erklären. **Bestandsprojekte** erreicht das Muster
nicht (D-126); sie übernehmen einzelne Dokumente von Hand
(`.koolie/core/docs/ADOPTION_GUIDE.md` Abschnitt 3).

## Die Grenze zur Aktivierungsreife

🔴 **Ein Overlay aus diesem Muster ist nicht aktivierungsreif, und das ist gewollt**
(D-57). Es läßt die Pflichtwerte der Abschnitte 1, 5, 6, 13, 14 und 15 offen; ein Overlay,
das die Prüfung `--check-overlay-ready` von selbst bestünde, wäre ein aktivierungsreifer
Zustand, den niemand geprüft hat. **Die Sonde `M355b` hält fest, daß eine frische
Installation mit diesem Muster die Prüfung nicht besteht.**

## Änderungsverlauf

| Version | Datum | Änderung |
|---|---|---|
| `0.2.0` | 2026-09-25 | Sechs Musterdokumente allgemeiner Praktiken, im Manifest als `entwurf` registriert; Framework-Release `1.6.0` (`CR-2026-139`, D-359, D-360) |
| `0.1.0` | 2026-09-25 | Erstfassung mit Framework-Release `1.5.0` (`CR-2026-138`, D-355) |
