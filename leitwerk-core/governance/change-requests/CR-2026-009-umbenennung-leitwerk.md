# Änderungsantrag `CR-2026-009`

| Feld | Inhalt |
|---|---|
| Titel | Das Framework heißt Leitwerk; das Kernverzeichnis heißt `leitwerk-core/` |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | Verzeichnis `devin-core-framework/` → `leitwerk-core/`; 182 Dateien mit Pfad- oder Namensnennungen; `README.md`, `build/doc/00-kopf.md`, `build/build-docx.py`, `install.py`, `.gitignore`, `governance/RELEASE_PROCESS.md` |
| Ebene laut Entscheidungsbaum 6 | Core (Struktur) |
| Art | Änderung |
| Dringlichkeit | regulär (Review-Zyklus); vor 1.0.0 durchzuführen |

## 1. Anlass und Problem

Seit `CR-2026-005` ist der Kern inhaltlich werkzeugneutral: Er bezeichnet die Bestandteile der Laufzeitschicht mit Begriffen statt mit Pfaden, und die Abbildung auf einen konkreten Client leistet ein Client Pack. Seit `CR-2026-008` gilt das auch für die Berechtigungs- und Hook-Regeln.

Der **Name** ist dieser Entwicklung nicht gefolgt. Er trug den Produktnamen eines einzelnen Clients an drei Stellen:

| Stelle | Bisher | Vorkommen |
|---|---|---|
| Kernverzeichnis | `devin-core-framework/` | 994 |
| Repository und Projektverzeichnis | `devin-desktop-framework` | – |
| Eigenname in Prosa und Erzeugnissen | „Devin Desktop Framework" | 6 |

Das ist mehr als eine Schönheitsfrage. Ein Projekt, das `claude-code` installiert, liest durchgehend einen Pfad, der den Namen eines Werkzeugs nennt, das dort nicht im Einsatz ist – und dieselbe Beobachtung hatte bereits `CR-2026-005` ausgelöst. Die Roadmap führte die Umbenennung deshalb seit 0.5.0 als P3.

## 2. Vorgeschlagene Änderung

**Der Name ist `Leitwerk`.** Ein Leitwerk fliegt das Flugzeug nicht – es hält es stabil und auf Kurs. Das trifft die Selbstbeschreibung des Frameworks genauer als ein Regelbegriff: Es schreibt nicht vor, wie Software entsteht, sondern hält den Prozess in einer Spur, die prüfbar, nachvollziehbar und übertragbar bleibt. Der Name ist zudem herstellerneutral, kurz und im Repository eindeutig.

| Ebene | Neu |
|---|---|
| Kernverzeichnis | `leitwerk-core/` |
| Repository und Projektverzeichnis | `leitwerk` |
| Eigenname | Leitwerk |
| Titel des Hauptdokuments | „Leitwerk – Framework für den professionellen Einsatz von KI-Codierassistenten in Softwareentwicklungsteams" |

**Nicht betroffen** und ausdrücklich unverändert: das Client Pack `devin-desktop` (59 Nennungen), die Laufzeitschicht `.devin/` (250 Nennungen) und alle Produktnennungen „Devin Desktop", „Devin Local", „Devin Cloud" dort, wo tatsächlich der Client gemeint ist. Sie benennen einen realen Client korrekt.

**Ein Nebeneffekt, der zur Sache gehört:** Der längste relative Pfad sinkt von 110 auf 103 Zeichen. Unter `MAX_PATH` (260) bleiben damit rund 156 statt 149 Zeichen für den Projektpfad – die Einschränkung, die `CR-2026-003` bei einer Testinstallation unter Windows zum Scheitern gebracht hatte.

**Klarstellung im Release-Prozess.** Die Umbenennung ist eine brechende Änderung; `RELEASE_PROCESS.md` Punkt 1 verlangt dafür ein MAJOR-Release. Das ist hier nicht möglich, ohne Schaden anzurichten: `1.0.0` ist durch D-11 an fünf prüfbare Kriterien gebunden, von denen keines erfüllt ist. Eine Hauptversion für eine Verzeichnisumbenennung zu verbrauchen, würde diese Kriterien behaupten und das Release-Gate `FW-CL-11` entwerten. Semantic Versioning stellt `0.y.z` ausdrücklich für die Entwicklungsphase frei; der Punkt wird entsprechend ergänzt, damit die Regel nicht künftig erneut kollidiert. Ziel-Release ist **0.7.0** mit Migrationsabschnitt.

## 3. Prüffragen (durch Owner auszufüllen)

- [x] Richtige Ebene nach Entscheidungsbaum 6? — Ja, Core (Struktur). Keine Regel ändert sich inhaltlich.
- [x] Verschärfungsprinzip eingehalten? — Nicht berührt. Die Regelmenge ist identisch; **nachgewiesen**: Die aus dem Kern erzeugten Kernregeln unterscheiden sich ausschließlich in dem einen Pfadbestandteil, der umbenannt wurde (`Write(leitwerk-core/framework/**)` statt `Write(devin-core-framework/framework/**)`), und dieser Wert stammt aus dem Platzhalter `<CORE_DIR>`, nicht aus einer bearbeiteten Zeile.
- [x] Widerspruchsfreiheit geprüft? — `FW-KO-04` ist die dafür gebaute Prüfung und meldet gegen beide Installationen **0 Fehler**. Genau diese Absicherung war der Grund, die Umbenennung nicht vor 0.5.0 zu versuchen.
- [x] Laufzeitfassungen betroffen? — Nur über den Pfad. Installationsumfang unverändert: 80 / 79 Dateien. Die erzeugten Berechtigungs- und Hookdateien tragen den neuen Kernpfad, **ohne dass ein Manifest angefasst wurde** – `<CORE_DIR>` aus `CR-2026-008` hat sich hier zum ersten Mal bewährt.
- [x] Belegstatus korrekt? — Unverändert. Kein VERIFY-Marker wird berührt.
- [x] Test- und Validierungsbedarf? — Siehe Abschnitt 5.
- [x] Auswirkungen auf Overlays und laufende Onboardings? — **Ja, hier liegt der Aufwand.** Ein bestehendes Projekt muss das Verzeichnis umbenennen und die Nennungen in seiner Berechtigungsdatei und seinen Overlay-Dokumenten nachziehen. Der Weg ist durchgespielt und im Änderungsverzeichnis als Migrationsabschnitt dokumentiert.
- [x] Dokumentation? — CHANGELOG, Decision Log, `README.md`, Titelblatt des Hauptdokuments, `RELEASE_PROCESS.md`.

## 4. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | angenommen |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Der Kern ist seit 0.5.0 werkzeugneutral, sein Name war es nicht. Die Umbenennung ist ein Breaking Change und gehört deshalb vor 1.0.0 – abgesichert durch `FW-KO-04`, das eine solche Änderung nachweislich vollständig erfasst. |
| Ziel-Release | 0.7.0 |
| Decision-Log-Eintrag | D-19 |

## 5. Umsetzung (nach Annahme)

- [x] Verzeichnis umbenannt; 994 Pfadnennungen und 6 Namensnennungen in 182 Dateien ersetzt
- [x] `README.md` und Titelblatt des Hauptdokuments auf den neuen Namen und die Mehrclient-Sicht gebracht
- [x] `.gitignore`: veralteten Verweis auf `root-template/` im Wurzelverzeichnis korrigiert (liegt seit 0.5.0 je Client Pack)
- [x] `RELEASE_PROCESS.md` Punkt 1 um die `0.y.z`-Klarstellung ergänzt
- [x] **`FW-KO-04` gegen beide Installationen: 0 Fehler.** Kein toter Verweis, keine übersehene Nennung; `git grep` nach den drei alten Namensformen ist leer
- [x] Erstinstallation beider Packs: 80 / 79 Dateien wie zuvor; `--check` fehlerfrei; Dateiliste gegen eine Referenzinstallation abgeglichen und deckungsgleich
- [x] Erzeugte Artefakte tragen den neuen Kernpfad automatisch: `Write(leitwerk-core/framework/**)` in den Kernregeln beider Packs, `$DEVIN_PROJECT_DIR/leitwerk-core/...` im Hook-Befehl
- [x] Dokumentbau intakt: alle Einbettungspfade auflösbar, 8.559 Zeilen erzeugt
- [x] **Migration durchgespielt** an einem Projekt auf Stand 0.6.0 mit eigenen Werten in der Berechtigungsdatei: Nach Umbenennung und `--update` meldet der Validator genau zwei Fehler und benennt die betroffene Kernregel; nach dem Ersetzen der fünf Nennungen 0 Fehler, die Projektwerte unverändert erhalten
- [ ] **Außerhalb des Repositorys, durch den Owner:** Git-Repository umbenennen, Remote-URL der Arbeitskopien nachziehen, lokales Projektverzeichnis umbenennen
- [ ] **Folgearbeit:** Der Fließtext des Hauptdokuments (`build/doc/`, Kapitel 1 bis 32) steht weiterhin auf 0.1.0 und ist aus der Sicht eines einzelnen Clients geschrieben. Das Titelblatt weist diesen Stand jetzt ausdrücklich aus; die Einarbeitung ist eigene Arbeit
