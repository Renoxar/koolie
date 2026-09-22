# Änderungsantrag `CR-2026-012`

| Feld | Inhalt |
|---|---|
| Titel | Schreibschutz auf das gesamte Kernverzeichnis statt nur auf `framework/**` |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | `framework/runtime/permissions.json`; `tests/scripts/hook-check-secrets.py`; `framework/core/03-security.md`; `clients/devin-desktop/CLIENT_PACK.md`, `clients/claude-code/CLIENT_PACK.md`, `clients/_template/CLIENT_PACK.md`; `tests/TEST_CATALOG.md`; `build/doc/08-trennung.md` |
| Ebene laut Entscheidungsbaum 6 | Core (Kernregelmenge, Ebene 3) |
| Art | Verschärfung |
| Dringlichkeit | regulär (Review-Zyklus) |

## 1. Anlass und Problem

Befund aus `CR-2026-008`, dort ausdrücklich für einen eigenen Antrag zurückgestellt: Das
Schreibverbot der Kernregelmenge lautete `<CORE_DIR>/framework/**`. Es schützte damit die
Regeltexte – und ließ ungeschützt, was unmittelbar daneben liegt:

| Datei | Rolle |
|---|---|
| `install.py` | legt die Laufzeitschicht an und aktualisiert sie |
| `clientmap.py` | bildet die Kernregelmenge auf den Client ab und erzwingt die drei Zusicherungen aus D-18 |
| `tests/scripts/validate-framework.py` | gleicht die installierte Berechtigungsdatei gegen die Kernquelle ab |
| `tests/scripts/hook-check-secrets.py` | blockiert Secrets und geschützte Pfade vor der Werkzeugausführung |
| `tests/scripts/hook-overlay-status.py` | meldet den Overlay-Status beim Sitzungsstart |

Das ist die unangenehme Form einer Lücke: Ungeschützt war nicht irgendein Randbereich,
sondern **genau die fünf Skripte, die die Schutzzusagen durchsetzen**. Wer `clientmap.py`
ändern kann, ändert die Kernregeln jeder künftigen Installation; wer
`validate-framework.py` ändern kann, schaltet die Prüfung ab, die das bemerken würde. Die
Lücke war älter als `CR-2026-008` – dieser Antrag hatte sie nur sichtbar gemacht, weil er
`clientmap.py` hinzufügte.

Der Hook trug dieselbe Enge in zweiter Fassung: Seine Musterliste schützte
`framework/core/`, also noch weniger als die Berechtigungsdatei.

## 2. Vorgeschlagene Änderung

**Die Kernregel lautet `<CORE_DIR>/**` statt `<CORE_DIR>/framework/**`.** Eine Regel wird
durch eine breitere ersetzt, keine kommt hinzu: Die Zahl der Kernregeln bleibt bei 13
(`devin-desktop`) beziehungsweise 17 (`claude-code`, dort trägt jeder Schreibschutz zwei
Regeln).

**Kein Ausnahmemuster für einzelne Unterverzeichnisse.** Das ist keine Härte um der Härte
willen, sondern Mechanik: In der Berechtigungsdatei gewinnt `deny` immer, und keine der
beiden abgebildeten Clientformen kennt ein Ausnahmemuster innerhalb eines Verbots. „Der
Kern bis auf ein Verzeichnis" ist schlicht nicht ausdrückbar – ausdrückbar ist nur ein
engeres Verbot, und genau das war der Zustand, der die Skripte ungeschützt ließ.

Die Frage stellt sich für zwei Verzeichnisse, die wie Arbeitsbereiche aussehen:
`tests/protocols/` und `governance/change-requests/`. Beide sind Framework-Gut und werden
über ein Release ausgetauscht. Ein aufnehmendes Projekt legt seine Testergebnisse nach
`CL-10` ohnehin als Anlage der Overlay-Aktivierung ab, nicht im Kern. Wo ein Projekt
dennoch im Kernverzeichnis schreiben müsste, ist entweder der Ablageort falsch gewählt
oder es liegt ein Fall für den Ausnahmeprozess vor – beides bessere Antworten als eine
Lücke in der Regel.

**Der Hook schützt das Kernverzeichnis, aber nur gegen schreibende Werkzeuge.** Die
bestehende Musterliste gilt auch für `exec`. Hätte das Kernmuster dort gestanden, wäre
jeder Befehl blockiert, der einen Kernpfad nennt – der Aufruf des Validators,
`install.py --check`, ein `git diff leitwerk-core/`. Das Framework hätte sich seine eigene
Prüfung verboten. Das Muster steht deshalb in einer zweiten Liste, die nur für `edit`,
`write` und `notebookedit` ausgewertet wird. Die Ergänzung ist rein additiv: Sie
verschärft, ohne eine bisher blockierte Operation freizugeben.

**Den Namen des Kernverzeichnisses leitet der Hook aus seinem eigenen Ort ab**
(`<CORE_DIR>/tests/scripts/`), statt ihn festzuschreiben. Damit erreicht ihn eine
Umbenennung des Kerns von selbst – dieselbe Überlegung, die `<CORE_DIR>` in `CR-2026-008`
eingeführt hatte.

## 3. Prüffragen (durch Owner auszufüllen)

- [x] Richtige Ebene nach Entscheidungsbaum 6? — Ja. Die Kernregelmenge (Ebene 3) ändert sich; deshalb dieser Antrag und nicht ein Nebenbefund in `CR-2026-008`.
- [x] Verschärfungsprinzip eingehalten? — Ja, in beide Richtungen geprüft: `<CORE_DIR>/framework/**` ist eine echte Teilmenge von `<CORE_DIR>/**`, und die zweite Hook-Musterliste ergänzt Blockaden, ohne eine bestehende aufzuheben. Kein Overlay kann die Regel lockern; sie steht als Kernzusage in `_core_rules_integrity`.
- [x] Widerspruchsfreiheit geprüft? — Drei Stellen beschrieben den Schutz enger oder anders, als er nun ist, und wurden nachgezogen: die Berechtigungspolitik in `03-security.md` Abschnitt 4, die Zeile B4 beider Fähigkeitsmatrizen und die Mechaniktabelle in Kapitel 8 des Hauptdokuments. Validator und `FW-KO-04`: 0 Fehler.
- [x] Laufzeitfassungen betroffen? — Ja, die Berechtigungsdatei. Sie ist **Saat** und wird bei `--update` nie überschrieben; bestehende Installationen migrieren von Hand (Abschnitt 5 und Migrationshinweis im CHANGELOG). Der Installationsumfang bleibt unverändert.
- [x] Belegstatus korrekt? — Der Hook-Anteil ist geprüft (`FW-ZA-05`, skript). Dass ein Client die `deny`-Regel durchsetzt, bleibt unbelegt wie alle Einstufungen der Fähigkeitsmatrizen – dafür steht `FW-ZA-06` neu im Katalog (sitzung, Roadmap AP2). Belegstand der Matrizen unverändert: 13 von 26 Zeilen bei `devin-desktop`, 9 von 26 bei `claude-code`.
- [x] Test- und Validierungsbedarf? — Zwei neue Testfälle, siehe Abschnitt 5.
- [x] Auswirkungen auf Overlays und laufende Onboardings? — Ein Overlay ändert sich nicht. Ein Projekt, das die Migration unterlässt, fällt beim nächsten Validatorlauf auf (nachgewiesen, Abschnitt 5).
- [x] Dokumentation? — CHANGELOG, Decision Log, Roadmap, Testkatalog, Testprotokoll.

## 4. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | angenommen |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Ein Schutz, der die Regeltexte umfasst, aber nicht die Skripte, die sie durchsetzen, schützt die Aussage und nicht ihre Grundlage. Die Verschärfung kostet nichts, was das Framework braucht: Der Kern gehört dem Framework Owner und wird ausschließlich über ein Release ausgetauscht – das war seit D-17 die Ablageregel, ohne dass die Berechtigungsdatei sie abbildete. |
| Ziel-Release | 0.10.0 |
| Decision-Log-Eintrag | D-22 |

## 5. Umsetzung (nach Annahme)

- [x] `framework/runtime/permissions.json`: `<CORE_DIR>/framework/**` → `<CORE_DIR>/**`, weiterhin `"core": true`
- [x] Erzeugte Kernregeln geprüft: `Write(leitwerk-core/**)` bei `devin-desktop`, `Edit(leitwerk-core/**)` **und** `Write(leitwerk-core/**)` bei `claude-code`. Anzahl der Kernregeln unverändert (13 / 17)
- [x] `hook-check-secrets.py`: zweite Musterliste für das Kernverzeichnis, nur für schreibende Werkzeuge; Verzeichnisname aus dem eigenen Ort abgeleitet
- [x] **Zweiter Nebenbefund:** `NotebookEdit` stand in keiner der geprüften Werkzeugklassen und lief an der **gesamten** Musterliste vorbei – auch an den Mustern für Secrets-Pfade, Laufzeitschicht und Overlay. Die Werkzeugklassen stehen jetzt einmal in `WRITE_TOOLS` und werden von beiden Listen verwendet
- [x] **Nebenbefund im selben Zug behoben:** Fünf Vorkommen der Zeichenklasse `[\/]` trafen nur den Schrägstrich, nicht den umgekehrten. Die Muster für Wurzel-Anweisungsdatei und Laufzeitschicht griffen unter Windows nicht. Alle fünf lauten jetzt `[\\/]`
- [x] `FW-ZA-05` (skript) **bestanden**: vierzehn synthetische Werkzeugeingaben, vierzehnmal wie erwartet. Protokoll: `leitwerk-core/tests/protocols/2026-09-10-FW-ZA-05.md`. Sieben der acht Blockadefälle liefen vor der Änderung durch – darunter der Schreibzugriff auf das Hook-Skript selbst
- [x] `FW-ZA-06` (sitzung) neu im Katalog, Status `offen`: Ob ein Client die `deny`-Regel durchsetzt, ist Gegenstand von AP2
- [x] **Migration erzwungen, nicht angekündigt:** Gegen eine nicht migrierte Installation meldet der Validator zwei Fehler (`Kernregel fehlt in deny` und `… in _core_rules_integrity.deny_must_contain`). Nachgewiesen durch Rückbau der Referenzinstallation dieses Repositorys und erneuten Lauf
- [x] Frische Installation beider Client Packs in leeren Verzeichnissen: erzeugt die neue Regel; Validator und `install.py --check` ohne Befund aus dieser Änderung
- [x] Referenzinstallation dieses Repositorys migriert; Validator: 0 Fehler, 0 Warnungen
- [x] Dokumentation nachgezogen: `03-security.md` Abschnitt 4 (dort zugleich zwei Client-Bindungen aus dem Kern entfernt, D-15), B4 in beiden Packs und in der Vorlage, Kapitel 8 des Hauptdokuments
- [ ] **Bewusst offen:** Ein Shell-Befehl, der in den Kern schreibt, wird vom Hook nicht erfasst – dort trägt allein die `deny`-Liste der Berechtigungsdatei. Das gilt für jedes Pfadverbot des Frameworks gleichermaßen und ist keine Eigenschaft dieser Änderung
- [ ] **Bewusst offen:** Im Framework-Repository selbst schützt die Regel den Kern auch vor dem KI-Client, der am Framework arbeitet. Das ist beabsichtigt – V10 verlangt für Änderungen an Framework-Regeln ohnehin den Änderungsantrag. Wer den Client dort schreiben lassen will, führt das über den Ausnahmeprozess (`leitwerk-core/governance/EXCEPTION_PROCESS.md`), nicht über eine Lücke in der Regel
