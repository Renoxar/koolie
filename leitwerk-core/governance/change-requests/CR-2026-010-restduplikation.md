# Änderungsantrag `CR-2026-010`

| Feld | Inhalt |
|---|---|
| Titel | Restduplikation: Overlay-Laufzeitregel, nutzerlokale Ergänzung und MCP-Vorlage in den Kern |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | neu: `framework/runtime/rules/20-project-overlay.md`, `framework/runtime/root-instruction-local.example.md`, `framework/runtime/mcp-config.example.json`; entfallen: die sechs entsprechenden Dateien in den beiden Client Packs; geändert: `clients/*/manifest.json`, `install.py`, `clients/README.md`, beide `CLIENT_PACK.md` |
| Ebene laut Entscheidungsbaum 6 | Core (Struktur) |
| Art | Änderung |
| Dringlichkeit | regulär (Review-Zyklus) |

## 1. Anlass und Problem

Nach `CR-2026-008` bestand ein Client Pack aus sieben Dateien. Eine Messung der verbliebenen Ähnlichkeit – nach Normalisierung der Client- und Pfadnamen – ergab:

| Dateipaar | Zeilen | abweichend | Befund |
|---|---|---|---|
| `20-project-overlay.md` | 119 | 11 | 91 Prozent identisch |
| `*.local.md.example` | 38 | 8 | 79 Prozent identisch |
| MCP-Vorlage | 8 | 2 | bis auf zwei Zeilen identisch |
| Laufzeit-`README.md` | 86 | 64 | **zu Recht getrennt** |

Die ersten drei sind derselbe Fall wie in `CR-2026-007`: Der Inhalt gehört dem Framework, nur Pfad- und Namensnennungen hängen vom Client ab. Die vierte Zeile ist die Gegenprobe – die beiden Laufzeit-READMEs beschreiben tatsächlich verschiedene Mechanismen und bleiben, wo sie sind.

Bemerkenswert an der Untersuchung: **Jede der elf abweichenden Zeilen der Overlay-Regel und jede der acht der nutzerlokalen Ergänzung enthielt ausschließlich Werte, für die bereits ein Laufzeit-Platzhalter registriert ist** (`<RUNTIME_DIR>`, `<ROOT_INSTRUCTION_FILE>`, `<ROOT_INSTRUCTION_LOCAL>`, `<MCP_FILE>`). Es war also keine Abbildung zu erfinden, sondern nur eine bereits vorhandene anzuwenden.

## 2. Vorgeschlagene Änderung

**Drei Quellen im Kern**, alle über die vorhandenen Mechanismen aus `CR-2026-007` installiert:

| Quelle | Ziel | Art | Transformation |
|---|---|---|---|
| `framework/runtime/rules/20-project-overlay.md` | `<RULES_DIR>/20-project-overlay.md` | Saat | `render_rule` + Platzhalter |
| `framework/runtime/root-instruction-local.example.md` | `<ROOT_INSTRUCTION_LOCAL>.example` | Core | nur Platzhalter |
| `framework/runtime/mcp-config.example.json` | `<MCP_FILE>.example` | Core | nur Platzhalter |

Kein neuer Mechanismus, kein neues Manifestfeld. Die Overlay-Regel liegt unter `framework/runtime/rules/` und wird dadurch von der Regeltransformation aus `CR-2026-007` erfasst, ohne dass `install.py` eine weitere Fallunterscheidung braucht. Dass sie – anders als ihre drei Nachbarn dort – **Saat** und nicht Core ist, entscheidet allein der Eintrag im Manifest (`shared_seed` statt `shared_core`); die Ablage trifft darüber keine Aussage.

**Ergebnis:** Ein Client Pack besteht aus vier Dateien: `CLIENT_PACK.md`, `manifest.json` und zwei Laufzeit-READMEs. `seed_paths` ist in beiden Manifesten leer – die gesamte Saat kommt jetzt aus dem Kern.

**Zwei Korrekturen an der MCP-Vorlage**, die durch die Zusammenführung nötig wurden und beide eine Ungenauigkeit beseitigen: „laut Devin-Dokumentation" wird zu „laut Dokumentation dieses Clients", und der Marker `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` zu seiner clientneutralen Form. In der Fassung des Packs `claude-code` standen beide bislang falsch – ein Rest aus der Konvertierung, der dort nie zutraf.

## 3. Prüffragen (durch Owner auszufüllen)

- [x] Richtige Ebene nach Entscheidungsbaum 6? — Ja. Die Overlay-Laufzeitregel ist die Kurzfassung von Ebene 4 und damit Framework-Gut in der Form, Projekt-Gut im Inhalt – genau deshalb Saat. Die beiden Vorlagen sind Core.
- [x] Verschärfungsprinzip eingehalten? — Ja, und **nachgewiesen**: Fünf der sechs erzeugten Dateien sind gegenüber 0.7.0 zeichengleich. Die sechste – die Overlay-Regel des Packs `claude-code` – unterscheidet sich in drei Zeilen ihres erzeugten Kommentars; siehe Abschnitt 5.
- [x] Widerspruchsfreiheit geprüft? — `FW-KO-04` gegen beide Installationen: 0 Fehler.
- [x] Laufzeitfassungen betroffen? — Nur ihr Ursprung. Installationsumfang unverändert: 80 / 79 Dateien.
- [x] Belegstatus korrekt? — Der Belegstatus der MCP-Vorlage wird von einem client­spezifischen auf den clientneutralen Marker gehoben. Inhaltlich ist das keine Änderung des Nachweisstands, sondern die Korrektur einer falschen Zuordnung im Pack `claude-code`.
- [x] Test- und Validierungsbedarf? — Siehe Abschnitt 5.
- [x] Auswirkungen auf Overlays und laufende Onboardings? — Keine. Die beiden Vorlagen sind Core und werden von `--update` erneuert; die Overlay-Regel ist Saat und wird nie überschrieben. Ein bestehendes Projekt behält seine ausgefüllte Fassung unverändert.
- [x] Dokumentation? — CHANGELOG, Decision Log, `clients/README.md`, beide `CLIENT_PACK.md`.

## 4. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | angenommen |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Die Zusammenführung braucht keinen neuen Mechanismus – die Abbildung lag bereits vollständig als Laufzeit-Platzhalter vor. Ein Client Pack enthält damit ausschließlich, was zwei Clients tatsächlich unterscheidet: die Pfadabbildung, die Semantikabbildung, die Fähigkeitsmatrix und zwei erklärende READMEs. |
| Ziel-Release | 0.8.0 |
| Decision-Log-Eintrag | D-20 |

## 5. Umsetzung (nach Annahme)

- [x] Drei Quellen unter `framework/runtime/` angelegt, Client-Bindungen durch registrierte Platzhalter ersetzt
- [x] Manifeste: Einträge aus `core_paths` und `seed_paths` in `shared_core` beziehungsweise `shared_seed` überführt; `seed_paths` ist jetzt in beiden Packs leer
- [x] Sechs Dateien aus den Client Packs entfernt; ein Pack umfasst noch vier Dateien statt sieben
- [x] **Zeichenweiser Vergleich gegen 0.7.0:** `20-project-overlay.md` (`devin-desktop`), beide `*.local.md.example` und beide MCP-Vorlagen bis auf die zwei gewollten Wortkorrekturen identisch
- [x] Erstinstallation beider Packs: 80 / 79 Dateien wie zuvor; `--check` gegen beide fehlerfrei; Validator gegen beide Installationen und die Wurzelinstallation: 0 Fehler
- [x] **Befund und Korrektur an `render_rule`:** Die Formulierung des Ladeverhaltens war invertiert – ausgerechnet eine Regel mit `trigger: always_on` erhielt den Satz *ohne* das Wort „immer", während eine Regel mit `model_decision` ihn *mit* erhielt. Der Fehler war ohne Wirkung auf das Verhalten, aber irreführend: Er behauptete den schwächeren Ladezustand für die Regel, die tatsächlich ausnahmslos lädt. Beide Fälle sagen jetzt „immer geladen"; nur die Verschärfungsnotiz unterscheidet sie. Dadurch weicht die Overlay-Regel des Packs `claude-code` in drei Kommentarzeilen von ihrer 0.7.0-Fassung ab – sie liest sich jetzt wie ihre drei Nachbarregeln
- [ ] **Beobachtung ohne Handlungsbedarf:** `root-template/` enthält je Pack nur noch zwei READMEs. Die Ablage bleibt, weil ein künftiges Pack wieder eigene Wurzelartefakte mitbringen kann; `seed_paths` bleibt aus demselben Grund im Manifest, obwohl es derzeit überall leer ist
