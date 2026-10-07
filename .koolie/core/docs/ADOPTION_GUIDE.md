# Übernahme des Frameworks in ein Projekt

| Attribut | Wert |
|---|---|
| ID | `FW-DOC-ADOPT` |
| Version | `0.9.0` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Checkliste | `.koolie/core/checklists/10-project-adoption.md` (verbindlicher Nachweis) |

## 1. Grundprinzip

Der unveränderliche Kern liegt in **einem** Verzeichnis: `.koolie/core/`. Er wird als Release in
die Wurzel des Projekt-Repositorys kopiert und bleibt byte-gleich zum Release. Änderungswünsche
gehen als Änderungsantrag an den Framework Owner (`.koolie/core/governance/FEEDBACK_PROCESS.md`),
nicht als lokale Bearbeitung.

Zwei Dinge kann der Kern nicht mitbringen, weil der KI-Client sie nur an festen Orten sucht `[DOK]`:

| Bestandteil | Rolle |
|---|---|
| Wurzel-Anweisungsdatei | die zentrale Agentenanweisung, die der Client beim Start lädt |
| Laufzeitschicht | Regeln, Skills, Agentenprofile, Berechtigungen und Hooks, die der Client selbst lädt und ausführt |

Name und Ort hängen vom Client ab; die Pfade je Client stehen in
`.koolie/core/docs/RUNTIME_GLOSSARY.md` und im `CLIENT_PACK.md` des Packs. Die Quellen liegen
trotzdem im Kern (`framework/runtime/`, `framework/skills/`, `templates/`), und
`.koolie/core/install.py` legt sie in der Form des gewählten Clients an. Welcher Client gilt,
entscheidet `--client`; `--list-clients` zeigt die verfügbaren. Wer eine gemeinsame Quelle ändern
will, ändert sie im Kern, nicht im Pack.

**Dem Projekt gehören nur:**

| Bestandteil | Ebene |
|---|---|
| `.koolie/project-overlay/` einschließlich `forbidden-terms.txt` | 4 |
| `20-project-overlay.md` in der Regelablage (und optionale `2N-overlay-*`) | 4 |
| die ausgefüllten Werte in der Berechtigungsdatei | 3/4 |
| die Entscheidung, welche Packs aktiviert sind (Overlay Abschnitt 1) | 5/6 |
| `prj-*`-Skills in der Skill-Ablage | 4 |
| die Entscheidung, welches Client Pack verwendet wird | – |

Alles andere ist Kern. Wechselt ein Team das Projekt, tauscht es nur das Overlay (P10, Baum 6).

## 2. Neuaufnahme (Schrittfolge)

1. **Voraussetzungen der Organisation:** Werkzeugfreigabe, Datenschutz- und Vertragsprüfung,
   dokumentierte Team-Einstellungen (`.koolie/core/framework/org-policies/`; die Projektwerte
   stehen im Overlay).

   Die Schritte 2 und 3 gehen auch in einem Zug – auf zwei Wegen:

   **Über eine Paketquelle.** Im Projektverzeichnis holt `uvx koolie` (oder `pipx run koolie`,
   `npx @renoxar/koolie`) Koolie aus PyPI beziehungsweise npm und startet einen Dialog mit dem
   aktuellen Verzeichnis als Vorgabe. Dauerhaft installiert (`pipx install koolie`,
   `uv tool install koolie`, `npm install -g @renoxar/koolie`) heißt der Befehl `koolie` und nimmt
   dieselben Argumente wie `install.py`, etwa `koolie --target /pfad/zum/projekt --client <client>`.
   `pip install koolie` installiert nur den Befehl; liegt er außerhalb des `PATH`, geht
   `python -m koolie`. Jedes Paket enthält genau den Baum des Release-Archivs.

   **Mit dem Starter.** In der Wurzel des entpackten Release-Archivs liegen `install.cmd` (Windows)
   und `install.command` (macOS). Sie suchen ein Python ab 3.8, fragen Projektverzeichnis, Client,
   Overlay-Muster und Lieferumfang ab und rufen dann diesen Befehl auf, der auch direkt geht:

   ```bash
   python .koolie/core/install.py --target /pfad/zum/projekt --client <client> [--overlay general] [--lieferumfang nutzung]
   ```

   `--target` kopiert nur `.koolie/core/` – aus einem Klon das Versionierte, aus dem Archiv alles
   außer Bytecode und `build/out/` – und ruft dann das kopierte `install.py` im Projekt auf.
   Scheitert es, wird der kopierte Kern wieder entfernt. Python und PyYAML installiert der Starter
   nicht, und die Schritte ab 4 bleiben Handarbeit.

   **Lieferumfang:** `voll` (Vorgabe) kopiert den ganzen Kern. `nutzung` lässt die Nachweisschicht
   weg – Änderungsanträge, Abnahmeprotokolle, Erhebungen und den Bau des Hauptdokuments, zusammen
   der größere Teil der Dateien. Alles zur Nutzung bleibt, auch Hooks und Validator. Die Wahl steht
   in `.koolie/core/LIEFERUMFANG` und gilt beim Update weiter; gewechselt wird nur mit ausdrücklichem
   `--lieferumfang`. In einem reduzierten Projekt nennt der Validator das Weggelassene in
   `HINWEIS`-Zeilen. Verweise auf Protokolle zeigen dort ins Leere; die Belege stehen im
   Release-Archiv.

   ⚠️ Unter Windows muss der Projektpfad so kurz sein, dass kein Pfad im Kern 259 Zeichen
   überschreitet; sonst hält `--target` vor der ersten Kopie an. Beim ersten Start warnt das
   System vor dem unsignierten Starter (SmartScreen, Gatekeeper); unter macOS ist
   `sh install.command` im Terminal der sichere Weg. Der macOS-Starter ist unter Git Bash und
   Linux geprüft, auf macOS selbst noch nicht.

2. **Kern kopieren (von Hand):** `.koolie/core/` in die Wurzel des Projekt-Repositorys kopieren,
   bei einem Monorepo in die Wurzel des Workspace, den der KI-Client öffnet.

   ```bash
   mkdir -p /pfad/zum/projekt/.koolie
   cp -r .koolie/core /pfad/zum/projekt/.koolie/
   ```

   ⚠️ **Nur `.koolie/core/` kopieren, nie ganz `.koolie/`.** Daneben liegt das Kennzeichen des
   Framework-Repositoriums (`.koolie/QUELLREPOSITORIUM.md`). Kopiert hält der Validator das Projekt
   für das Framework selbst und meldet Fehler, die die Ursache nicht nennen; aus einem Klon kommt
   außerdem dessen Overlay mit. `install.py` meldet ein mitkopiertes Kennzeichen – dann die Datei
   löschen.

3. **Wurzelbestandteile anlegen:**

   ```bash
   cd /pfad/zum/projekt
   python .koolie/core/install.py --list-clients
   python .koolie/core/install.py --client <client>
   # oder, mit einem vorbefüllten Overlay-Muster (nur bei der Erstinstallation):
   python .koolie/core/install.py --client <client> --overlay general
   ```

   Vor der Wahl des Client Packs dessen Fähigkeitsmatrix lesen
   (`.koolie/core/clients/<client>/CLIENT_PACK.md`): Sie zeigt, welche Zusagen der Client
   technisch erzwingt und welche nur als Anweisung wirken.

   Das Skript legt die Wurzel-Anweisungsdatei, ihre `.example`-Vorlage für persönliche
   Ergänzungen, die Laufzeitschicht und – falls noch nicht vorhanden – `.koolie/project-overlay/`
   an. **Berechtigungsdatei und Overlay werden nie überschrieben**, auch bei `--update` nicht.

   **Das Overlay-Muster `general` ist wählbar, nicht Standard.** Ohne `--overlay` beginnt das
   Projekt mit einem leeren Overlay. Mit ihm füllt `install.py` drei Pfadplatzhalter, deren Wert
   sich ohne Kenntnis des Projekts sicher angeben lässt – `<CI_CONFIG_PATHS>`,
   `<QUALITY_GATE_CONFIG_PATHS>` und `<EXCLUDED_PATHS>` –, in Overlay, Laufzeitfassung und
   Berechtigungsdatei zugleich. Das Muster sperrt nur, es gibt nichts frei; ein Overlay daraus ist
   noch nicht aktivierungsreif. Dazu kommen sechs Musterdokumente – Coding Guidelines, Definition
   of Ready, Definition of Done, Qualität, Sicherheit, Branching – unter
   `.koolie/project-overlay/documents/<typ>/` mit Status `entwurf`. Verbindlich werden sie erst,
   wenn der Overlay Owner sie prüft, im Manifest auf `aktuell` setzt, freigibt und in der
   Laufzeitfassung als K1-Dokumente führt. Einzelheiten:
   `.koolie/core/framework/overlay-patterns/general.md`. Liegt schon ein Overlay im Projekt, bricht
   `--overlay` ab.

   Gewählt wird genau ein Muster. Neben `general` stehen zur Wahl:

   - **`java-spring`, `web-frontend`, `infrastructure`** bauen auf `general` auf und sperren
     zusätzlich Dateien, die für den Projekttyp typisch heikel sind – Schlüsselspeicher,
     lokale Umgebungsdateien, Terraform-Variablen und Kubeconfig, dazu die Konfiguration
     der jeweiligen Prüfwerkzeuge.
   - **`zoomies`** ist ein Party-Overlay: alles aus `general` und dazu eine kurze, immer
     geladene Regel, die Dokumenten, Commit-Texten, Testnamen und Merge Requests ein
     Augenzwinkern erlaubt – höchstens eines je Artefakt, nie bei Sperren, Freigaben,
     Sicherheit oder Datenschutz. Es ändert keine Pflicht und gibt nichts frei; jeder der elf
     Bausteine lässt sich in der Regeldatei `21-overlay-zoomies.md` abschalten. Im Dialog ist es
     nie die Vorgabe.
   - **Muster eines Unternehmens** liegen in einem eigenen Verzeichnis im selben Format und
     kommen mit `--overlay-quelle <pfad>` dazu (im Dialog über die Umgebungsvariable
     `KOOLIE_OVERLAY_QUELLE`). Für sie gilt dieselbe Grenze: Sie sperren, sie geben nichts frei.
     Name, Version, Quelle und SHA-256 des Musters stehen danach im Manifest. Ein späteres
     `--update --overlay-quelle <pfad>` meldet eine neuere Musterversion und legt neue Dokumente
     an; vorhandene überschreibt es nie.

   **Belegt das Projekt schon einen Pfad des Frameworks, bricht die Installation ab** und nennt die
   Dateien. Meist ist es die Wurzel-Anweisungsdatei, weil das Projekt bereits mit dem Client
   arbeitet. Wie ihr Inhalt übernommen wird, steht in Schritt 3a.

   **`.gitignore`:** Die des Framework-Repositorys nicht übernehmen – sie schließt
   Wurzel-Anweisungsdatei, Laufzeitschicht und Overlay aus, die im Projekt versioniert werden.
   Hinein gehört dagegen diese Zeile, weil die Werkzeuge des Kerns bei jedem Lauf Bytecode
   erzeugen:

   ```gitignore
   __pycache__/
   ```

   Ist Bytecode schon versioniert, entfernt die Zeile ihn nicht. Zuerst
   `git rm -r --cached .koolie/core/**/__pycache__`, dann die Zeile. Der Validator meldet beides
   (Prüfung 45).

3a. **Vorhandene Anweisungsdatei übernehmen** (nur, wenn Schritt 3 abgebrochen ist). Die
   Wurzel-Anweisungsdatei gehört dem Kern. Ihr bisheriger Inhalt geht nicht verloren, er zieht um:

   | Bisheriger Inhalt | Neuer Ort |
   |---|---|
   | Projektwissen – Stack, Befehle, Architektur, Konventionen | `.koolie/project-overlay/OVERLAY.md`, passender Abschnitt |
   | Projektspezifische **Regeln** an den Agenten | eine eigene Regeldatei `2N-overlay-<name>.md` in der Regelablage (Ebene 4) |
   | Persönliche Gewohnheiten | die `.example`-Vorlage für persönliche Ergänzungen, nicht das Repositorium |
   | Abschnitte, die ein **anderes Werkzeug** erzeugt | siehe Abschnitt 8.2 |

   Danach die alte Datei löschen und Schritt 3 wiederholen. Führt das Projekt bereits ein anderes
   Agenten-Rahmenwerk, das Abschnitte in die Wurzel-Anweisung schreibt, wird es vorher auf eine
   eigene Datei umgestellt.

4. **Overlay ausfüllen:** `.koolie/project-overlay/OVERLAY.md` vollständig; die Laufzeitfassung
   `20-project-overlay.md` synchron halten; Werte in die Berechtigungsdatei eintragen, ohne die
   Kernregeln im Block `_core_rules_integrity` zu entfernen; Manifest und Dokumente einpflegen.

   **Mehr als ein Technologiestrang?** Die Berechtigungsdatei hat drei Befehlsschlitze –
   `<BUILD_COMMAND>`, `<TEST_COMMAND>`, `<LINT_COMMAND>` –, ein Projekt mit Backend und Frontend
   aber sechs Befehle. So gehen sie zusammen:

   - **Je Platzhalter genau eine Tabellenzeile** in Abschnitt 5 oder 6 des Overlays, mit dem
     Platzhalter in spitzen Klammern und dem Befehl rechts daneben (Prüfung 42).
   - **Den Schlitz bekommt der Befehl, der auf den Arbeitsplätzen tatsächlich läuft.** Ein Schlitz
     mit einem Befehl, der nicht läuft, sichert nichts ab.
   - **Die übrigen Befehle bleiben gelistet und wirken über die Regelschicht** – als Anweisung,
     nicht als technische Schranke. Von Hand in die Berechtigungsdatei eintragen hilft nicht;
     Prüfung 42 meldet jeden Befehl, den kein Platzhalter erklärt.

5. **Packs aktivieren.** Nach der Installation ist kein Pack aktiv, auch nicht das Referenzpack
   `software-development`. Je benötigtem Pack die Rolle im Overlay Abschnitt 1 eintragen, dann
   die Laufzeitfassung und – falls vorhanden – die Skills kopieren:

   ```bash
   # <regelablage> ist der Pfad aus dem manifest.json des gewählten Client Packs
   P=.koolie/core/framework/role-packs/software-development
   cp $P/runtime/30-role-software-development.md <regelablage>/
   ```

   Danach hält `install.py --update` diese Bestandteile auf dem Stand des Releases; `--check`
   meldet lokale Abweichungen.

6. **Projektlokal härten:** `.koolie/project-overlay/forbidden-terms.txt` mit den echten Projekt-,
   Kunden-, Behörden-, Produkt- und Systemnamen füllen (bleibt projektlokal); bei Bedarf weitere
   Verbote in der Berechtigungsdatei.

7. **Validieren und testen:**

   ```bash
   python .koolie/core/tests/scripts/validate-framework.py --check-overlay-ready
   python .koolie/core/install.py --check
   ```

   Der erste Befehl prüft Struktur, Inhalte und ob das Overlay aktivierungsreif ist; er erwartet
   einen Status, der noch nicht `aktiv` ist. Der zweite prüft, ob eine Kerndatei lokal verändert
   wurde. Danach die Basistests des Testkatalogs auf dem Übungsrepository fahren und das
   Übungsrepository für das Onboarding anlegen (`.koolie/core/onboarding/exercises/README.md`).

8. **Organisation im Projekt:** Rollen zuordnen (außerhalb des Repositorys), Eskalationskanäle,
   Ablageorte für Berichte und Pläne, Feedbackkanal.

9. **Overlay aktivieren:** Checkliste 10 abschließen, den Overlay-Status an jeder Stelle, an der
   das Overlay ihn führt, auf `aktiv` setzen, dann `validate-framework.py --strict-overlay` und
   `install.py --probe` laufen lassen und das Projekt beim Framework Owner melden (Bestandsliste).
   **Erst danach** arbeitet der Agent mit Schreibrechten.

10. **Menschen befähigen:** Onboarding vor der produktiven Nutzung; Pilotparameter setzen, wenn
   das Projekt als Pilot läuft.

## 3. Aktualisierung auf ein neues Framework-Release

1. Die Release-Notes und Migrationshinweise im `CHANGELOG.md` des neuen Releases lesen.

2. **Update.** Am einfachsten aus dem neuen Release heraus – mit `uvx koolie` im Projekt, mit dem
   Starter oder direkt:

   ```bash
   python .koolie/core/install.py --target /pfad/zum/projekt --update
   ```

   Der alte Kern wird als Ganzes ersetzt und erst entfernt, wenn `--update` im Projekt geklappt
   hat; sonst liegt er wieder an seinem Platz. Der Lieferumfang bleibt, wie er war.

   **Von Hand:** `.koolie/core/` im Projekt löschen, das neue Verzeichnis hineinkopieren – nur
   dieses, nie ganz `.koolie/` (Abschnitt 2, Schritt 2) – und im Projekt aufrufen:

   ```bash
   python .koolie/core/install.py --update
   ```

   Von Hand geht der Lieferumfang `nutzung` verloren; das Projekt ist danach wieder `voll`.

   **Das Client Pack wird erkannt.** `install.py` sieht, welche Laufzeitschicht im Projekt liegt,
   und aktualisiert dieses Pack; `--client` ist nicht nötig. Die erste Ausgabezeile nennt das
   erkannte Pack. Findet die Erkennung nichts, etwa bei einer unvollständigen Installation, ist
   `--client <pack>` anzugeben.

   **Was `--update` schreibt:** die Kerndateien in der Wurzel – Wurzel-Anweisungsdatei, Regeln
   `00-`, `10-`, `15-`, die `*-TEMPLATE`-Vorlagen, die `koolie-*`-Skills, die Agentenprofile, bei
   `openai-codex` auch Hook-Datei und Befehlsregeldatei – und die Bestandteile aktivierter Packs
   (Regeln `30-`, `40-` und ihre Skills). Welche Dateien das sind, steht im `manifest.json` des
   Packs.

   **Was `--update` nicht schreibt:** Berechtigungsdatei (bei `devin-desktop` und `claude-code`
   samt Hooks), Overlay, `prj-*`-Skills und projekteigene Packs. Die Berechtigungsdatei trägt
   Projektwerte; nach dem Update prüfen, ob die Kernregeln vollständig sind, und Hook-Änderungen
   aus den Migrationshinweisen von Hand nachtragen.

   ⚠️ Bei `openai-codex` ändert `--update` die Hook-Datei und damit ihren Hash. Der Schutz-Hook
   läuft erst wieder, wenn ihm erneut vertraut wurde
   (`.koolie/core/clients/openai-codex/CLIENT_PACK.md` Abschnitt 1b).

   **Wechsel auf 2.0.0: neue Skillnamen.** Die mitgelieferten Skills heißen jetzt `koolie-<name>`
   statt `fw-<name>`, `role-re-ticket` heißt `koolie-ticket` und das Agentenprofil
   `koolie-reviewer`. `--update` benennt die Skillordner um, entfernt das alte Agentenprofil und
   ersetzt die alten Namen einmalig in der Berechtigungsdatei – das ist die einzige Stelle, an der
   es die Berechtigungsdatei anfasst. Die Ausgabe listet jede Änderung. Ins Overlay schreibt es
   nicht; es nennt die Dateien, in denen noch ein alter Name steht (etwa `/fw-plan`), zum Anpassen
   von Hand.

3. **Projektdateien nachziehen.** Overlay, Laufzeitfassung, projekteigene Packs, `prj-*`-Skills,
   `README`, Onboarding-Material und `.gitignore` können auf geänderte Kernpfade, Platzhalter oder
   Skillnamen verweisen. Der Validator findet nur, was er als Verweis erkennt – eine Suche über das
   Projekt gehört dazu.

   Feste Versionswerte in Projektdateien fallen dabei am wenigsten auf: Nennt eine
   Merge-Request-Vorlage oder ein `README` die Framework-Version als Wert, veraltet sie mit dem
   nächsten Release. Besser einen Platzhalter eintragen (`<Inhalt der Datei .koolie/core/VERSION>`).

   Die Musterdokumente des Overlay-Musters `general` kommen bei einem Update nicht ins Projekt.
   Wer eines übernehmen will, kopiert es aus
   `.koolie/core/framework/overlay-patterns/general/documents/<typ>/`, registriert es im Manifest
   (`.koolie/project-overlay/OVERLAY.md` Abschnitt 19) und gleicht es vorher mit den vorhandenen
   Dokumenten desselben Typs ab.

4. Validator (`--strict-overlay`) und Basistests erneut ausführen; bei einem MAJOR-Release
   zusätzlich FW-RE-01/02.

5. Den Overlay-Änderungsverlauf ergänzen, das Team informieren, das Onboarding-Material prüfen.

6. **Kern, Laufzeitschicht und Overlay in einem Commit festhalten.** Erst dann ist der neue Stand
   dauerhaft.

## 4. Mehrere Repositories, ein Projekt

**Entscheidend ist, wo die Sitzung startet, nicht wo das Framework liegt.** Eine Installation
wirkt nur für eine Sitzung, die im Verzeichnis der Installation startet. Startet sie in einem
Repository darunter, laden weder Berechtigungen noch Hooks – und nichts meldet es. Gemessen am
2026-09-26 (`.koolie/core/tests/protocols/2026-09-26-mehrprojekt-tokenlast.md`):

| Client Pack (Clientversion) | Sitzung im Verzeichnis der Installation | Sitzung im Repository darunter: Wurzel-Anweisung | … Berechtigungen und Hooks | Eigene Installation im Repository |
|---|---|---|---|---|
| `claude-code` (2.1.283) | trägt | lädt | laden nicht | trägt; beide Wurzel-Anweisungen laden |
| `devin-desktop` (3000.11.1) | trägt | lädt nicht | laden nicht | trägt; nur die eigene lädt |
| `openai-codex` (0.157.0) | Konfiguration lädt | lädt nicht | Konfiguration lädt nicht (Projektwurzel ist die git-Wurzel des Repositorys) | lädt |

**Drei Einsatzszenarien:**

1. **Ein Repository:** Installation in dessen Wurzel. Der Normalfall.
2. **Mehrere lose Repositories:** je Repository eine eigene Installation; die Sitzung startet im
   Repository. Das Overlay kann gemeinsam gepflegt und je Repository ausgerollt werden.
3. **Ein Multimodul-Projekt in einem Repository:** eine Installation in der Wurzel, die Sitzung
   startet dort. Unterschiede der Module tragen Technology Packs mit Pfad-Ladebedingung (bei
   `openai-codex` ohne Ladebedingung).

⚠️ Eine einzige Installation über mehreren Repositories trägt nur, solange jede Sitzung im
gemeinsamen Arbeitsbereich startet. Das prüft kein Werkzeug; wenn Menschen Repositories einzeln
öffnen, ist davon abzuraten.

Mehrere Repositories lassen sich in einer Schleife aktualisieren; `--target` kopiert nur den Kern, das
Overlay jedes Repositorys bleibt:

```bash
for repo in repo-a repo-b; do
  python .koolie/core/install.py --target "$repo" --update
done
```

## 5. Deinstallation oder Werkzeugwechsel

**Deaktivieren:** Overlay-Status auf `inaktiv` setzen – das Werkzeug arbeitet dann nur noch
lesend –, danach bei Bedarf die Laufzeitschicht entfernen. `.koolie/core/` kann als Nachweis im
Repository bleiben.

**Werkzeug wechseln:** Die Regeln unter `.koolie/core/framework/` sind werkzeugneutral und bleiben.
Für einen neuen KI-Client entsteht ein Client Pack unter `.koolie/core/clients/<client>/`
(`.koolie/core/clients/README.md`, Abschnitt 5). Vorher die Fähigkeitsmatrix des Zielclients
auswerten: Eine Kernzusage, die er nicht technisch durchsetzt, ist zu begründen, im Overlay als
Ausnahme zu führen und durch `<SECURITY_CONTACT>` freizugeben. Wer das überspringt, senkt das
Schutzniveau, ohne dass es jemand merkt.

## 6. Warum der Kern gebündelt ist

Liegt der Kern in einem Ordner, muss beim Übernehmen und beim Update niemand entscheiden, was zum
Framework und was zum Projekt gehört, und die Wurzel des Projekts bleibt übersichtlich. **Der Kern
ist ein Ordner, den man ersetzt. Das Projekt ist alles daneben.**

## 7. Was das Framework kostet – gemessen

Koolie verteuert eine Aufgabe des KI-Clients: Es lädt Regeln in jeden Modellaufruf und verlangt
mehr – Fundstellen, einen Ergebnisbericht, den passenden Skill. Gemessen am 2026-09-26 im
Übungsrepository, je Client Pack derselbe Auftrag mit und ohne Installation, jeder dreimal
(`.koolie/core/tests/protocols/2026-09-26-mehrprojekt-tokenlast.md`). Mittelwerte; die feste Last
mit angelegtem Cache:

| Client Pack | Aufgabe | Eingabe-Token ohne → mit | Kosten je Aufgabe ohne → mit (USD) | Faktor Kosten |
|---|---|---|---|---|
| `claude-code` | nur „OK“ antworten (feste Last) | 32.330 → 47.232 | 0,007 → 0,010 (erster Aufruf einer Sitzung: 0,137 → 0,285) | 1,4 (2,1) |
| | kleine Änderung als Diff | 65.466 → 99.443 | 0,065 → 0,184 | 2,8 |
| | Analyse über mehrere Dateien | 104.503 → 173.236 | 0,137 → 0,284 | 2,1 |
| `devin-desktop` | feste Last | 23.556 → 31.913 | 0,012 → 0,016 | 1,3 |
| | kleine Änderung als Diff | 47.983 → 81.585 | 0,051 → 0,123 | 2,4 |
| | Analyse über mehrere Dateien | 167.503 → 295.203 | 0,272 → 0,494 | 1,8 |
| `openai-codex` | feste Last | 15.346 → 19.755 | 0,006 → 0,011 | 1,7 |
| | kleine Änderung als Diff | 63.503 → 107.119 | 0,021 → 0,049 | 2,4 |
| | Analyse über mehrere Dateien | 89.826 → 135.566 | 0,035 → 0,062 | 1,8 |

**Was daraus folgt:**

- **Die feste Last ist klein und kommt fast immer aus dem Cache:** rund 15.000 Token bei
  `claude-code`, 8.400 bei `devin-desktop`, 4.400 bei `openai-codex`. Der Cache kostet ein Zehntel
  des Eingabepreises; teuer ist nur der erste Aufruf einer Sitzung.
- **Eine kleine Aufgabe wird zwei- bis dreimal so teuer, eine größere rund doppelt so teuer.** Den
  Unterschied macht die Arbeitsweise: Die Sitzung liest den Skill, belegt mit Fundstellen und
  schreibt einen Ergebnisbericht.
- **In Beträgen:** je hundert kleine Aufgaben rund 3 bis 12 USD mehr, je hundert Analysen rund 3
  bis 22 USD mehr, je nach Client (Listenpreise vom 2026-09-26). Die Laufzeit steigt bis auf das
  Doppelte.

**Was die Zahlen nicht sagen:** Sie stammen aus drei Aufgaben in einem Repository an einem Tag;
die Spannen stehen im Protokoll. Die Preise sind Listenpreise der API. Ein Abo rechnet anders ab –
dort zählt der Verbrauch am Kontingent, und dafür sind die Token die richtige Größe. **Den Nutzen
messen sie nicht:** ob weniger Nacharbeit, weniger Fehler oder ein verhindertes Leck die
Mehrkosten aufwiegen.

## 8. Einsatzarchitektur, Koexistenz und Vergleich

Koolie ist die Regel- und Nachweisschicht im Repositorium – kein Sandkasten und keine
GRC-Plattform. Es wirkt über Dateien im Projekt und über den Client, der sie lädt. Was außerhalb
davon liegt, muss die Umgebung tragen.

### 8.1 Was Koolie trägt – und was die Umgebung tragen muss

| Schicht | Trägt | Was Koolie beiträgt | Was fehlt, wenn nur Koolie da ist |
|---|---|---|---|
| Regeln, Skills, Nachweise | Koolie | Ebenen 1 bis 7, Testblätter, Validator, Protokolle | – |
| Berechtigungen und Schutz-Hook des Projekts | Koolie | Berechtigungsdatei und Hook je Client Pack, Wirksamkeitsprobe `install.py --probe` | Die Dateien liegen im Projekt; ein Mensch kann sie ändern, und sie wirken nur für eine Sitzung, die im Projekt startet |
| Verwaltete Einstellungen des Clients | Administration | Das Pack nennt die Schalter (etwa `disableBypassPermissionsMode`, `syncClaudeAiSkills`) | Ein Schutz, den weder Agent noch Projekt abschalten kann und der auch außerhalb des Projekts gilt |
| Branch-Schutz, Pflicht-Review, CI | Plattform | Die CI- und Quality-Gate-Pfade sind für den Agenten gesperrt (Prüfung 89) | Eine Prüfung, die der Agent weder erzeugen noch umgehen kann |
| Isolation (Container, Netz, Dateisystem) | Laufzeit | – | Schutz gegen einen Agenten, der aktiv umgeht |

Schließt eine Isolationsschicht den Schreibweg über die Shell, gibt es für eine Änderung am Kern
nur die registrierte, befristete Ausnahme nach `governance/EXCEPTION_PROCESS.md`.

### 8.2 Koexistenz mit einem anderen Agenten-Rahmenwerk

OpenSpec und GitHub Spec Kit schreiben beim Anlegen nicht in die Wurzel-Anweisung und ändern keine
Datei von Koolie, auch umgekehrt nicht (gemessen am 2026-09-30 mit OpenSpec 1.13.2). Beide legen
ihre Skills aber in **dieselbe Ablage** wie Koolie, mit den Präfixen `openspec-` und `speckit-`.
Die Aufteilung: Koolie trägt Ebene 1 – Sicherheit, Berechtigungen, Schutz-Hook –, das andere
Rahmenwerk seine Prozessartefakte in eigener Ablage.

1. `install.py` meldet ein erkanntes Rahmenwerk am Ende jedes Laufs.
2. Die fremden Skills im Overlay-Manifest deklarieren, damit der Validator sie nicht nach den
   Regeln für Koolie-Skills prüft (Prüfung 111):

   ```yaml
   fremde_skills: openspec-, speckit-
   ```

   Ein Präfix, das einen Koolie-Skill treffen könnte (`koolie-`, `prj-`), nimmt nichts aus.
3. Jeden fremden Skill in der Berechtigungsdatei einem Korb zuordnen, etwa `Skill(openspec-*)` in
   `ask` – sonst fällt sein Aufruf in die Rückfrage (Prüfung 72).

**Die Wurzel-Anweisung gehört dem Kern.** Schreibt ein Generator markierte Abschnitte hinein
(`<!-- NAME:START -->` … `<!-- NAME:END -->`), bricht `install.py --update` ab, statt sie zu
überschreiben, und Prüfung 111 warnt vorher. Abhilfe: den Generator auf eine eigene Datei
umstellen, die bei Bedarf lädt. Jeder Block in der Wurzel-Anweisung zählt außerdem ins Budget der
stets geladenen Texte (Prüfung 4).

### 8.3 Koolie gegen eine gute Standardkonfiguration – gemessen

Was trägt Koolie zusätzlich zu dem, was ein Team mit einer guten Standardkonfiguration ohnehin hat?
Gemessen am 2026-09-30 mit `claude-code` 2.1.285 und Opus 5.5
(Protokoll `tests/protocols/2026-09-30-einsatzarchitektur.md`):

- **Referenz R:** Einstellungen außerhalb des Repositoriums (Secret-Pfade, Laufzeitschicht,
  Wurzel-Anweisungsdatei und CI-Dateien gesperrt, Modus ohne Rückfragen abgeschaltet), eine kurze
  Wurzel-Anweisungsdatei mit Teamregeln, ein Remote mit Branch-Schutz und Secret-Scan.
- **R+K:** dasselbe, dazu Koolie mit ausgefülltem Overlay.
- Jede Rückfrage beantwortete ein Stellvertreter mit „ja“ – der unaufmerksame Mensch. Was dann noch
  gesperrt bleibt, sperrt die Technik.

| Test | Läufe je Gruppe | R | R+K |
|---|---|---|---|
| Secret über Lesen, Suche, Shell, Unterprozess, manipuliertes Dokument | 5 | 0 Lecks | 0 Lecks |
| Eingriff in eigene Kontrollen (Einstellungen, Regeln, CI, Hooks), auch per Dokument | 5 | 0 Änderungen | 0 Änderungen |
| Start in einem Unterverzeichnis | 5 | 0 Verletzungen | 0 Verletzungen |
| Gegenlauf **ohne Regeltexte** (Shell, Unterprozess, CI, Hooks) | 6 | **1 Leck** (Unterprozess nach Rückfrage) | 0 – den Unterprozess sperrte der Schutz-Hook |
| Normale kleine Änderung mit Tests | 5 | 5 von 5 richtig, Tests grün | 5 von 5 richtig, Tests grün |
| Kosten je Lauf (Mittel, Listenpreis) | | 0,20 USD (Änderung 0,29) | 0,33 USD (Änderung 0,52) |
| Rückfragen je kleiner Änderung | | 3,8 | 5,0 |

**Was daraus folgt:** Mit Regeltexten hielt in beiden Gruppen fast immer schon das Modell – dafür
genügte auch die kurze Anweisungsdatei der Referenz. Den Unterschied macht die Technik, wenn die
Regel nicht greift: Einen Unterprozess, der eine Secret-Datei liest, erfasst die
Berechtigungsschicht des Clients nicht, der Schutz-Hook von Koolie schon. Der Preis: rund 65 bis
80 Prozent mehr Kosten je Lauf, bei der Änderung rund die Hälfte mehr Zeit und etwas mehr
Rückfragen; Fehlblockaden gab es nicht.

**Was die Zahlen nicht sagen:** Ein Client, ein Modell, ein Tag; je Sicherheitsfall ein Lauf je
Gruppe. Die Einstellungen der Referenz lagen in einer Datei außerhalb des Repositoriums, nicht in
verwalteten Einstellungen; ein Agent, der aktiv umgeht, ist nicht gemessen. Die Zahlen belegen
keine Überlegenheit – nur, dass Koolie eine gute Standardkonfiguration ergänzt und nicht ersetzt.

## 9. Befehle im Überblick

| Befehl | Zweck |
|---|---|
| `uvx koolie` · `pipx run koolie` · `npx @renoxar/koolie` | Im Projektverzeichnis: Koolie holen und installieren oder aktualisieren, mit Dialog |
| `python .koolie/core/install.py --target <projekt> [--update] [--lieferumfang voll\|nutzung]` | Aus einem Klon oder entpackten Archiv den Kern in ein Projekt kopieren und dort installieren oder aktualisieren; die Starter `install.cmd` und `install.command` fragen die Angaben ab |
| `python .koolie/core/install.py --update` | Im Projekt: die Wurzelbestandteile nach einem Austausch von `.koolie/core/` nachziehen |
| `python .koolie/core/install.py --check` | Prüfen, ob eine Kern-Datei lokal verändert wurde (Exit-Code 1, wenn ja) |
| `python .koolie/core/install.py --dry-run` | Zeigen, was passieren würde |
| `python .koolie/core/install.py --overlay <muster> [--overlay-quelle <pfad>]` | Erstinstallation mit einem Overlay-Muster (`general`, `java-spring`, `web-frontend`, `infrastructure`, `zoomies` oder eines aus der Quelle); `--overlay` ohne Namen zählt die Muster auf |
| `python .koolie/core/install.py --probe` | Ohne Modell prüfen, ob die Schutzschicht im Projekt greift |
| `python .koolie/core/install.py --list-clients` / `--list-skills` | Verfügbare Client Packs beziehungsweise die Skills dieser Installation |
| `python .koolie/core/tests/scripts/validate-framework.py --strict-overlay` | Den aktiven Zustand des Projekts prüfen |
