# Änderungsantrag `CR-2026-004`

| Feld | Inhalt |
|---|---|
| Titel | Zweites Client Pack `claude-code`; Manifeste; clientneutraler Validator |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | neu: `devin-core-framework/clients/claude-code/`, `devin-core-framework/clients/*/manifest.json`; geändert: `devin-core-framework/install.py`, `devin-core-framework/tests/scripts/validate-framework.py`, `devin-core-framework/tests/scripts/hook-check-secrets.py`, `devin-core-framework/clients/README.md`, `devin-core-framework/OWNERS.md` |
| Ebene laut Entscheidungsbaum 6 | Core (Struktur) |
| Art | neu |
| Dringlichkeit | regulär (Review-Zyklus) |

## 1. Anlass und Problem

`CR-2026-002` und `CR-2026-003` haben die Client Packs eingeführt und installierbar gemacht – aber mit genau einem Pack. Ob die Abstraktion trägt oder nur eine Umbenennung war, konnte damit niemand feststellen. Ein zweites Pack ist der einzige belastbare Nachweis.

`claude-code` eignet sich als Gegenprobe besonders, weil der Client in einem zentralen Punkt anders gebaut ist: Er kennt **keine Regeldateien mit Ladetriggern**. Damit prüft das Pack nicht nur die Pfadabbildung, sondern die Annahme, dass die Framework-Regeln überhaupt von diesem Mechanismus lösbar sind.

## 2. Vorgeschlagene Änderung

1. **Client Pack `claude-code`** mit `CLIENT_PACK.md`, `manifest.json` und vollständigem `root-template/` (79 Dateien).

2. **Manifeste für beide Packs.** `install.py` hatte `CORE_PATHS`, `SEED_PATHS` und die Projektpfad-Hinweise fest verdrahtet – auf `.devin/`. Diese Listen stehen jetzt je Pack in `manifest.json`. Ohne Manifest gilt ein Pack als nicht installierbar.

3. **Clientneutraler Validator.** `check_required`, `check_config`, `check_rules` und `skill_dirs` liefen fest gegen `.devin/`. Sie ermitteln die Laufzeitschicht jetzt über `detect_client()` aus dem Manifest des Packs, dessen `runtime_dir` im Zielverzeichnis liegt. Sind mehrere Laufzeitschichten vorhanden, ist das ein Fehler – ein Projekt nutzt genau ein Pack.

4. **`check_rules` unterscheidet zwei Bauarten.** Mit Ladetriggern wird das Frontmatter geprüft. Ohne Ladetrigger wird geprüft, dass jede Kernregel in der Wurzel-Anweisung **eingebunden** ist – dort ist eine nicht eingebundene Regeldatei stillschweigend wirkungslos, ein Fehlerfall, den es bei Clients mit Ladetriggern nicht gibt. Zusätzlich wird der ständig geladene Kontext gemessen und ab 40.000 Zeichen gewarnt.

5. **Der Schutz-Hook wurde clientneutral.** `hook-check-secrets.py` schützte `AGENTS.md` und `.devin/`; es schützt jetzt beide Namensformen. Das Skript war ohnehin schema-agnostisch und funktioniert damit bei beiden Clients unverändert.

6. **Der Querverweis-Check unterscheidet drei Fälle** (siehe Abschnitt 2a).

### 2a. Der wichtigste Befund: 63 Client-Bindungen im „werkzeugneutralen" Kern

Der Validator gegen die erste `claude-code`-Installation meldete **104 Fehler**. Keiner davon war ein Programmfehler. Die Ursache: D-02 nennt `devin-core-framework/framework/` „kanonisch und werkzeugneutral" – tatsächlich nennt der Kern an vielen Stellen `AGENTS.md` und `.devin/`, also die Laufzeitpfade genau eines Clients.

Nach Abzug der berechtigten Fälle bleiben **63 echte Client-Bindungen**, verteilt über `framework/core/`, `governance/`, `docs/`, `checklists/`, `onboarding/`, `prompts/` und `tests/`. Häufigste Nennungen: `AGENTS.md` (37), `.devin/config.json` (17), `.devin/` (16).

Der Querverweis-Check unterscheidet deshalb jetzt:

| Fall | Behandlung |
|---|---|
| Pfad existiert nicht und gehört zu keinem Client Pack | **Fehler** – tote Referenz |
| Pfad gehört zur Laufzeitschicht eines nicht installierten Client Packs | **Warnung** mit Anzahl und Fundstellen – Client-Bindung im Kern |
| Datei liegt im `root-template/` eines Packs, Pfad dort auflösbar | kein Befund – das Pack beschreibt seine eigene Laufzeitschicht |
| Datei ist eine `CLIENT_PACK.md` oder liegt unter `clients/_template/` | kein Befund – sie beschreibt fremde Pfade |

Damit ist die Neutralisierung des Kerns keine Schätzung mehr, sondern eine messbare Restgröße. Sie ist **nicht** Bestandteil dieses Antrags.

## 3. Prüffragen (durch Owner auszufüllen)

- [x] Richtige Ebene nach Entscheidungsbaum 6? — Ja, Struktur des Kerns.
- [x] Verschärfungsprinzip eingehalten? — Ja. Die Regeltexte sind inhaltlich identisch übernommen. Drei Abweichungen des neuen Packs sind sämtlich Verschärfungen: Regeln ohne Ladetrigger sind immer statt bedingt geladen; Befehlsverbote wirken präfixbasiert und damit breiter; der Schutz-Hook deckt jetzt beide Namensformen ab.
- [x] Widerspruchsfreiheit geprüft? — `clients/README.md` Abschnitt 2 (keine Regelebene) gilt unverändert. Die Fähigkeitsmatrix des neuen Packs weist vier Zusagen als `[NICHT ABBILDBAR]` aus; alle vier betreffen Least Context und Ergonomie, keine Schutzzusage.
- [x] Laufzeitfassungen betroffen? — Für `devin-desktop` nicht: `install.py --check` unverändert, Erstinstallation weiterhin 80 Dateien.
- [x] Belegstatus korrekt? — 9 der 26 Matrixzeilen tragen einen VERIFY-Marker. Das Pack weist sich im Kopf als unbelegt aus. Eine Beobachtung während der Erstellung (Abschnitt 6 des Packs) ist ausdrücklich als solche gekennzeichnet und ersetzt AP2 nicht.
- [x] Test- und Validierungsbedarf? — Siehe Abschnitt 5. Offen: ein Testfall, der die Vollständigkeit einer Fähigkeitsmatrix prüft.
- [x] Auswirkungen auf Overlays und laufende Onboardings? — Für bestehende Projekte keine. Das Übungsrepository wurde mit dem neuen Kern gegengeprüft (simulierte Übernahme): fehlerfrei, aktivierte Packs weiterhin erkannt.
- [x] Dokumentation? — `clients/README.md` (Pack-Liste mit Durchsetzungstiefe, Manifest-Pflicht, Erstellungsschritte), `OWNERS.md`, CHANGELOG, Decision Log.

## 4. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | angenommen |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Das zweite Pack belegt, dass die Abstraktion trägt: Alle sechs Kernzusagen sind auch bei einem Client mit grundlegend anderem Regelmechanismus technisch abgebildet. Zugleich hat der Versuch zwei Schwächen aufgedeckt, die ohne ihn unentdeckt geblieben wären – die harte Verdrahtung in `install.py` und im Validator sowie die 63 Client-Bindungen im angeblich werkzeugneutralen Kern. Beide sind jetzt behoben beziehungsweise messbar. |
| Ziel-Release | 0.5.0 |
| Decision-Log-Eintrag | D-14 |

## 5. Umsetzung (nach Annahme)

- [x] Client Pack `claude-code`: `CLIENT_PACK.md`, `manifest.json`, `root-template/` (79 Dateien)
- [x] Manifeste für beide Packs; `install.py` liest sie statt fester Listen
- [x] Validator clientneutral: `detect_client`, `check_required`, `check_config`, `check_rules`, `skill_dirs`
- [x] `hook-check-secrets.py` clientneutral; Selbsttest: beide Namensformen blockieren (Exit 2), Quellcodepfad nicht (Exit 0)
- [x] Erstinstallation `--client claude-code` in leeres Verzeichnis: 79 Dateien (eine weniger als `devin-desktop`, weil Hooks in der Berechtigungsdatei aufgehen); `--check` dagegen fehlerfrei
- [x] Validator gegen beide Installationen: je 0 Fehler
- [x] Regression `devin-desktop`: Erstinstallation weiterhin 80 Dateien, `--check` fehlerfrei
- [x] Übungsrepository mit Kern 0.5.0 gegengeprüft: 0 Fehler, aktivierte Packs erkannt
- [x] CHANGELOG und Decision Log ergänzt
- [ ] Folgearbeit: Neutralisierung der 63 Client-Bindungen im Kern; gemeinsame Skill-Quelle statt Duplikat je Pack; Testfall für die Vollständigkeit einer Fähigkeitsmatrix
