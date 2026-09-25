# Übernahme des Frameworks in ein Projekt

| Attribut | Wert |
|---|---|
| ID | `FW-DOC-ADOPT` |
| Version | `0.4.9` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Checkliste | `.koolie/core/checklists/10-project-adoption.md` (verbindlicher Nachweis) |

## 1. Grundprinzip

Der gesamte unveränderliche Kern liegt in **einem** Verzeichnis: `.koolie/core/`. Es
wird als Release in das Wurzelverzeichnis des Projekt-Repositorys kopiert und bleibt
byte-gleich zum Release. Änderungswünsche laufen als Änderungsantrag an den Framework Owner
(`.koolie/core/governance/FEEDBACK_PROCESS.md`), nicht als lokale Bearbeitung.

Zwei Ladeorte lassen sich nicht mitbündeln, weil sie Werkzeugkonvention sind und nicht
konfigurierbar `[DOK]`:

| Bestandteil | Rolle |
|---|---|
| Wurzel-Anweisungsdatei | Zentrale Agentenanweisung, wird vom Client automatisch geladen |
| Laufzeitschicht | Regelablage, Skill-Ablage, Agentenprofile, Berechtigungsdatei, Hook-Konfiguration |

Die tatsächlichen Pfade unterscheiden sich je Client; sie stehen in
`.koolie/core/docs/RUNTIME_GLOSSARY.md` und im `CLIENT_PACK.md` des gewählten Packs.

Deshalb liegen diese Bestandteile **im Kern** – `.koolie/core/framework/runtime/`,
`.koolie/core/framework/skills/` und `.koolie/core/templates/` –, und
`.koolie/core/install.py` legt sie in der Form des gewählten Clients an ihrem Platz an.
Welcher Client gilt, entscheidet `--client`; `--list-clients` zeigt die verfügbaren.

> Das `root-template/` eines Client Packs enthält seit `CR-2026-010` **nur noch die README
> der Laufzeitschicht**; `seed_paths` ist in beiden Manifesten leer. Wer eine gemeinsame
> Quelle ändern will, ändert sie im Kern, nicht im Pack.

**Projektspezifisch sind ausschließlich:**

| Bestandteil | Ebene |
|---|---|
| `.koolie/project-overlay/` einschließlich `forbidden-terms.txt` | 4 |
| `20-project-overlay.md` in der Regelablage (plus optionale `2N-overlay-*`) | 4 |
| die ausgefüllten Werte in der Berechtigungsdatei | 3/4 |
| die **Entscheidung**, welche Packs aktiviert sind (Overlay Abschnitt 1) | 5/6 |
| `prj-*`-Skills in der Skill-Ablage | 4 |
| die **Entscheidung**, welches Client Pack verwendet wird | – |

Alles andere ist Core. Ein Projektwechsel tauscht nur die Overlay-Bestandteile; der Core
bleibt unberührt (P10, Baum 6).

## 2. Neuaufnahme (Schrittfolge)

1. **Voraussetzungen der Organisation:** Werkzeugfreigabe, Datenschutz- und Vertragsprüfung,
   dokumentierte Team-Einstellungen (`.koolie/core/framework/org-policies/`;
   Klärungspunkte K-05/K-06).

   🆕 **Schritt 2 und 3 in einem Zug – der Starter (seit `1.7.0`, D-362):** Im entpackten
   Release-Archiv liegen in der Wurzel `install.cmd` (Windows) und `install.command`
   (macOS). Sie suchen ein Python ab 3.8 (D-363), fragen Projektverzeichnis, Client und
   Overlay-Muster ab und rufen dann genau einen Befehl auf, der auch direkt geht:

   ```bash
   python .koolie/core/install.py --target /pfad/zum/projekt --client <client> [--overlay general]
   ```

   `--target` kopiert **nur** `.koolie/core/` – aus einem Klon nur das Verfolgte, aus dem
   Archiv alles außer Bytecode und `build/out/` – und ruft danach das **kopierte**
   `install.py` im Projekt auf; scheitert es dort, wird der kopierte Kern wieder entfernt.
   Der Warnhinweis unten zu `.koolie/` betrifft diesen Weg nicht. **Was der Starter nicht
   tut:** Er installiert kein Python und kein PyYAML, er wählt keinen Lieferumfang (der
   ganze Kern, wie bisher) und er ersetzt die Schritte ab 4 nicht. ⚠️ Beim ersten Start
   warnt das System vor dem unsignierten Starter (SmartScreen, Gatekeeper); unter macOS
   ist der sichere Weg `sh install.command` im Terminal. **Der macOS-Starter ist unter
   Git Bash und Linux geprüft, auf macOS selbst noch nicht** (`CR-2026-140`).

2. **Kern kopieren (Handweg):** Das Verzeichnis `.koolie/core/` in das Wurzelverzeichnis des
   Projekt-Repositorys kopieren. Bei Monorepos in das Wurzelverzeichnis des Workspace, den
   der KI-Client öffnet (A-01).

   ```bash
   mkdir -p /pfad/zum/projekt/.koolie
   cp -r .koolie/core /pfad/zum/projekt/.koolie/
   ```

   ⚠️ **Nur `.koolie/core/` kopieren – nie ganz `.koolie/`.** Daneben liegt das
   Kennzeichen des Framework-Repositoriums (`.koolie/QUELLREPOSITORIUM.md`), im
   Release-Archiv ebenso wie in einem Klon. Mitkopiert hält der Validator das Projekt für
   das Framework-Repositorium: Prüfung 79 verlangt die Lizenz in der Projektwurzel, und
   sobald die Datei committet ist, mißt Prüfung 81 die Zeilenenden jedes Projektträgers –
   keine der Meldungen nennt die Ursache. Aus einem Klon kommt zusätzlich dessen eigenes
   Overlay mit (`.koolie/project-overlay/`). `install.py` meldet ein mitkopiertes
   Kennzeichen; die Abhilfe ist, die Datei zu entfernen (D-354).

3. **Wurzelbestandteile anlegen:**

   ```bash
   cd /pfad/zum/projekt
   python .koolie/core/install.py --list-clients
   python .koolie/core/install.py --client <client>
   # oder, mit einem vorbefüllten Overlay-Muster (nur bei der Erstinstallation):
   python .koolie/core/install.py --client <client> --overlay general
   ```

   **Das Overlay-Muster `general` ist wählbar, nicht Standard** (D-126, D-355). Ohne
   `--overlay` beginnt das Projekt mit dem leeren Overlay wie bisher. Mit ihm füllt
   `install.py` drei Pfadplatzhalter, deren Wert sich ohne Kenntnis des Projekts sicher
   angeben läßt – `<CI_CONFIG_PATHS>`, `<QUALITY_GATE_CONFIG_PATHS>` und
   `<EXCLUDED_PATHS>` –, und zwar **einmal** und in **allen drei** Trägern: Overlay,
   Laufzeitfassung und Berechtigungsdatei. **Das Muster sperrt, es gibt nichts frei:**
   Erlaubte Pfade, Befehle, Rollen und Freigaben bleiben Schlitze, und ein Overlay aus dem
   Muster ist **nicht** aktivierungsreif. Was es füllt und warum, steht in
   `.koolie/core/framework/overlay-patterns/general.md`; `--overlay` ohne Namen zählt die
   Muster auf. ⚠️ **Liegt die Saat schon, bricht `--overlay` ab** – vorhandene Saat gehört
   dem Projekt, und mit `--update` gibt es das Muster nicht.

   **Seit `1.6.0` bringt das Muster außerdem sechs Dokumente mit** (D-359, D-360):
   allgemeine Praktiken für Coding Guidelines, Definition of Ready, Definition of Done,
   Qualität, Sicherheit und Branching – nur, was auf jedes Projekt paßt, ohne Werkzeuge und
   Schwellenwerte. Sie liegen danach unter `.koolie/project-overlay/documents/<typ>/` und
   stehen im Manifest mit Status `entwurf`. 🔴 **Verbindlich werden sie erst durch den
   Overlay Owner:** prüfen, anpassen, im Manifest auf `aktuell` setzen, Freigabe eintragen
   und in der Laufzeitfassung als K1-Dokumente führen. Bis dahin liest der KI-Client sie
   nicht als Vorgabe.

   Das Skript legt die Wurzel-Anweisungsdatei, ihre `.example`-Vorlage für nutzerlokale
   Ergänzungen, die Laufzeitschicht und – sofern noch nicht vorhanden – `.koolie/project-overlay/`
   an. **Die Saatdateien – Berechtigungsdatei und Overlay – werden nie überschrieben**, auch
   bei `--update` nicht.

   **Belegt das Projekt einen Pfad des Frameworks schon, bricht die Erstinstallation ab** und
   nennt die betroffenen Dateien (D-46). Der wahrscheinliche Fall ist die
   Wurzel-Anweisungsdatei: Ihr Name ist die Konvention des Clients, nicht die Erfindung des
   Frameworks – ein Projekt, das bereits mit diesem Client arbeitet, führt sie meistens. Wie
   der vorhandene Inhalt übernommen wird, steht in Schritt 3a.

   **Vor der Wahl des Client Packs** die Fähigkeitsmatrix des Kandidaten lesen
   (`.koolie/core/clients/<client>/CLIENT_PACK.md`): Sie weist aus, welche Zusagen
   des Frameworks dieser Client technisch erzwingt und welche nur als Anweisung im Kontext
   stehen.

   Übernimm die `.gitignore` des Framework-Repositorys **nicht** unverändert: Dort sind
   die Wurzel-Anweisungsdatei, die Laufzeitschicht und `.koolie/project-overlay/` ausgeschlossen,
   weil sie im Framework-Repository Erzeugnisse sind. Im Projekt gehören sie in die
   Versionierung.

   **Eine Zeile gehört umgekehrt hinein** – und bis 0.46.0 stand sie hier nicht, weshalb
   sie in **beiden** bekannten Projekten fehlte (abgezählt am 2026-09-15: sechs
   versionierte Bytecode-Dateien im einen, zwei im anderen):

   ```gitignore
   # Bytecode der Python-Werkzeuge des Kerns – ein Erzeugnis, kein Quelltext
   __pycache__/
   ```

   `install.py` importiert `clientmap.py`, Validator und Hook laufen als Skript: Bei
   jedem Lauf entsteht Bytecode unter `.koolie/core/`. Versioniert ändert er sich mit
   jedem Lauf und überlebt den Kern, aus dem er entstanden ist. **Prüfung 45 verlangt die
   Zeile und meldet außerdem bereits versionierten Bytecode** – denn die Zeile allein
   entfernt ihn nicht: Git liest die `.gitignore` für bereits verfolgte Dateien nicht.
   Der Weg dorthin ist `git rm -r --cached .koolie/core/**/__pycache__`, **danach** die
   Zeile.

3a. **Vorhandene Anweisungsdatei übernehmen** (nur, wenn Schritt 3 abgebrochen ist).

   Das Framework beansprucht die Wurzel-Anweisungsdatei für Ebene 1. Ihr bisheriger Inhalt
   geht nicht verloren, er wechselt die Ebene:

   | Bisheriger Inhalt | Neuer Ort |
   |---|---|
   | Projektwissen – Stack, Befehle, Architektur, Konventionen | `.koolie/project-overlay/OVERLAY.md`, in den passenden Abschnitt |
   | Projektspezifische **Regeln** an den Agenten | eine eigene Regeldatei `2N-overlay-<name>.md` in der Regelablage (Ebene 4) |
   | Persönliche Gewohnheiten einzelner Personen | die `.example`-Vorlage für nutzerlokale Ergänzungen, nicht das Repositorium |
   | Abschnitte, die ein **anderes Werkzeug** erzeugt und pflegt | siehe den Hinweis unten |

   Erst danach die alte Datei entfernen und Schritt 3 wiederholen.

   > **Führt das Projekt bereits ein anderes Agenten-Framework**, das dieselbe Datei erzeugt
   > oder in Abschnitten pflegt, ist die Übernahme **kein Kopiervorgang, sondern eine
   > Entscheidung**: Zwei Regelwerke, die beide Ebene 1 beanspruchen, widersprechen einander
   > früher oder später, und das erzeugende Werkzeug schreibt seine Abschnitte beim nächsten
   > Lauf zurück. Dieser Fall ist im Framework **nicht gelöst** (K-31); er gehört vor die
   > Übernahme geklärt, nicht danach.

4. **Overlay ausfüllen:** `.koolie/project-overlay/OVERLAY.md` vollständig; Laufzeitfassung
   `20-project-overlay.md` in der Regelablage synchron halten; Werte in der
   Berechtigungsdatei eintragen, ohne die Kernregeln im Block `_core_rules_integrity` zu entfernen; Manifest und
   Dokumente einpflegen.

   **Mehr als ein Technologiestrang? Die Berechtigungsdatei hat drei Befehlsschlitze.**
   `<BUILD_COMMAND>`, `<TEST_COMMAND>` und `<LINT_COMMAND>` – einen vierten Eintrag kann
   ein Overlay dort nicht erzeugen, und die Datei wird nach der Erstinstallation nie
   wieder geschrieben (D-76). Ein Projekt mit Backend **und** Frontend hat aber sechs
   Build-, Test- und Prüfbefehle. Drei Sätze regeln den Fall:

   - **Je Platzhalter genau eine Tabellenzeile** in Abschnitt 5 oder 6, mit spitzen
     Klammern in der Platzhalterspalte und dem Befehl in der Zelle rechts daneben. Stehen
     zwei Zeilen für denselben Platzhalter, ist nicht entschieden, welcher Befehl für den
     Schlitz gilt – Prüfung 42 meldet es (D-91).
   - **Den Schlitz bekommt der Befehl, der auf den Arbeitsplätzen des Projekts tatsächlich
     läuft.** Gemessen, nicht vermutet: Am 2026-09-14 trug das Übungsrepository drei
     Maven-Befehle in seiner Berechtigungsdatei, während auf der Maschine weder JDK noch
     Maven installiert war. Ein Schlitz, der einen nicht ausführbaren Befehl trägt,
     sichert nichts ab und verdeckt, welcher Befehl wirklich läuft.
   - **Die übrigen Befehle bleiben gelistet und wirken über die Regelschicht.** Das ist
     eine Anweisung an den KI-Client und keine technische Schranke; die Tabelle sagt es,
     damit niemand mehr erwartet. **Ein Eintrag von Hand in die Berechtigungsdatei ist
     kein Ersatz:** Prüfung 42 meldet jeden Befehl, den kein Platzhalter erklärt – am
     Übungsrepository waren es fünf, darunter der Aufruf des Validators selbst.

5. **Packs aktivieren.** Kein Pack ist nach der Installation aktiv — auch nicht das
   Referenzpack `software-development`. Je benötigtem Pack: Rolle im Overlay Abschnitt 1
   aufführen, dann Laufzeitfassung und – falls vorhanden – Skills kopieren:

   ```bash
   # <regelablage> ist der Pfad aus dem manifest.json des gewählten Client Packs
   P=.koolie/core/framework/role-packs/software-development
   cp $P/runtime/30-role-software-development.md <regelablage>/
   ```

   Einmal aktiviert, hält `install.py --update` diese Bestandteile auf dem Stand des
   Releases; `--check` meldet lokale Abweichungen.

6. **Projektlokale Härtung:** `.koolie/project-overlay/forbidden-terms.txt` mit den realen Projekt-,
   Kunden-, Behörden-, Produkt- und Systemnamen füllen (bleibt projektlokal); gegebenenfalls
   zusätzliche Verweigerungsregeln in der Berechtigungsdatei.

7. **Validieren und testen:**

   ```bash
   python .koolie/core/tests/scripts/validate-framework.py --check-overlay-ready
   python .koolie/core/install.py --check
   ```

   Der erste Lauf prüft Struktur, Inhalte und die **Aktivierungsreife eines Kandidaten**:
   Er erwartet einen Overlay-Status, der noch **nicht** `aktiv` ist. Bis 0.32.0 stand hier
   `--strict-overlay` – ein Lauf, der `aktiv` verlangte, obwohl Schritt 9 den Status erst
   danach setzt. Der dokumentierte Ablauf war damit nicht ohne Regelbruch begehbar
   (B08, D-57). Der zweite
   prüft, ob eine Core-Datei lokal verändert wurde — das wäre eine Bearbeitung an der
   falschen Stelle. Anschließend die Basistests des Testkatalogs auf dem Übungsrepository
   ausführen und das Übungsrepository für das Onboarding erzeugen
   (`.koolie/core/onboarding/exercises/README.md`).

8. **Organisation im Projekt:** Rollen zuordnen (außerhalb des Repos), Eskalationskanäle,
   Ablageorte für Berichte und Pläne, Feedbackkanal.

9. **Overlay aktivieren:** Checkliste 10 abschließen, Overlay-Status `aktiv` an **jeder**
   Stelle, an der das Overlay ihn erklärt, dann
   `validate-framework.py --strict-overlay` als Nachprüfung des aktiven Zustands; Meldung
   an den Framework Owner (Bestandsliste). **Erst danach** beginnt der erste Agentenlauf
   mit Schreibrechten.

10. **Menschen befähigen:** Onboarding vor produktiver Nutzung; Pilotparameter setzen, wenn das
   Projekt als Pilot läuft.

## 3. Aktualisierung auf ein neues Framework-Release

1. Release-Notes und Migrationshinweise lesen
   (`.koolie/core/CHANGELOG.md` des neuen Releases).

2. Das Verzeichnis `.koolie/core/` durch das neue ersetzen – **nur dieses Verzeichnis**:
   Eine Kopie von ganz `.koolie/` aus einem Klon des Frameworks ersetzt das Overlay des
   Projekts durch das des Frameworks, und zwar **ohne Meldung** (Abschnitt 2, Schritt 2;
   D-354). Dann die Wurzelbestandteile nachziehen:

   ```bash
   python .koolie/core/install.py --update
   ```

   🆕 **Oder beides in einem Befehl aus dem neuen Release heraus** (seit `1.7.0`, D-362):
   `python .koolie/core/install.py --target /pfad/zum/projekt --update` – oder der
   Starter, der ein vorhandenes Projekt erkennt und das Heben anbietet. Das Verzeichnis
   wird als Ganzes ersetzt, nicht Datei für Datei, und erst nach erfolgreichem
   `--update` im Projekt ist der alte Kern weg; scheitert es, liegt er wieder an seinem
   Platz.

   **Das Client Pack wird erkannt, nicht vermutet.** `install.py` liest, welche Laufzeitschicht im Wurzelverzeichnis liegt, und aktualisiert dieses Pack – `--client` ist dafür nicht nötig und sollte weggelassen werden. Die erste Ausgabezeile nennt das erkannte Pack; stimmt es nicht, bricht der Lauf ab, statt eine zweite Laufzeitschicht anzulegen (D-45). Findet die Erkennung nichts – etwa bei einer unvollständigen Installation –, ist `--client <pack>` anzugeben.

   `--update` überschreibt die Core-Dateien im Wurzelverzeichnis (Wurzel-Anweisungsdatei,
   Regelablage `00-`, `10-`, `15-`, die `*-TEMPLATE`-Vorlagen, Skill-Ablage `fw-*`,
   Agentenprofile, Hook-Konfiguration) **und die Bestandteile aktivierter Packs**, deren
   Quelle im Kern liegt (Regelablage `30-`, `40-` sowie Skill-Ablage `role-*`, `tech-*`).
   Welche Datei dazuzählt, steht im `manifest.json` des Client Packs. Unberührt bleiben die
   Projektbestandteile: Berechtigungsdatei, Overlay, `prj-*`-Skills und projekteigene
   Packs. Die Berechtigungsdatei wird bewusst nicht angefasst, weil sie Projektwerte enthält — prüfe nach dem Wechsel, ob die Kernregeln
   noch vollständig sind.

3. Overlay-Bestandteile gegen die Migrationshinweise prüfen (neue Pflichtfelder, geänderte
   Platzhalter, deprecatete Skills). Nennt ein Release einen geänderten Kernpfad, betrifft
   das nicht nur die Berechtigungsdatei: Das Overlay, seine Laufzeitfassung, projekteigene
   Packs, `prj-*`-Skills, `README`, Onboarding-Material und die `.gitignore` verweisen
   ebenfalls darauf. Beim Wechsel von 0.4.0 auf 0.10.0 waren es 74 Nennungen in 19
   Projektdateien (`.koolie/core/tests/protocols/2026-09-10-FW-RE-02.md`). Der Validator
   meldet davon nur, was er als Verweis erkennt – die Suche über das Projekt gehört dazu.

   **Feste Versionswerte in Projektdateien sind dabei die unauffälligste Stelle.** Eine
   Merge-Request-Vorlage, ein `README` oder ein Onboarding-Dokument, das die Framework- oder
   Overlay-Version als **Wert** statt als Platzhalter nennt, veraltet mit dem nächsten Release,
   ohne dass eine Prüfung anschlägt – der Validator kennt die Projektvorlage nicht. Im
   Übungsrepository trug die Merge-Request-Vorlage über elf Releases hinweg
   `Framework-Version: 0.2.0`, also genau in der Datei, aus der die Nachweiskette in jeden
   Merge Request übernommen wird. Empfehlung: An dieser Stelle Platzhalter eintragen
   (`<Inhalt der Datei .koolie/core/VERSION>`), keine Werte.

   **Die Musterdokumente des Overlay-Musters `general` erreichen ein bestehendes Projekt
   nicht** – das Muster wirkt nur bei der Erstinstallation (D-126, D-359). Wer eines davon
   übernehmen will, kopiert es aus
   `.koolie/core/framework/overlay-patterns/general/documents/<typ>/` in die
   Dokumentablage des Overlays, registriert es im Manifest wie jedes andere Dokument
   (`.koolie/project-overlay/OVERLAY.md` Abschnitt 19) und prüft es vorher gegen die
   vorhandenen Dokumente desselben Typs: Zwei Coding Guidelines nebeneinander sind zwei
   Register.

4. Validator (`--strict-overlay`) und Basistests erneut ausführen; bei MAJOR-Releases
   zusätzlich FW-RE-01/02.

5. Overlay-Änderungsverlauf ergänzen (neue kompatible Framework-Version); Team über relevante
   Änderungen informieren; Onboarding-Materialstand prüfen.

## 4. Mehrere Repositories, ein Projekt

Je Repository, das der KI-Client öffnet, liegt eine vollständige Framework-Integration (Root-Regeln
wirken je Workspace). Das Overlay KANN geteilt gepflegt und je Repository ausgerollt werden;
seit der Bündelung ist das Ausrollen ein Kopiervorgang plus Skriptaufruf und damit
skriptbar:

```bash
for repo in repo-a repo-b; do
  mkdir -p "$repo/.koolie"
  cp -r .koolie/core "$repo/.koolie/"
  (cd "$repo" && python .koolie/core/install.py --update)
done
```

Die Pfadlisten (Abschnitt 4 des Overlays) sind je Repository spezifisch und werden nicht
mitkopiert — `install.py` überschreibt `.koolie/project-overlay/` nie. ⚠️ **Das gilt nur,
solange die Schleife `.koolie/core` kopiert:** Ein `cp -r .koolie` überschreibt das Overlay,
bevor `install.py` läuft, und `install.py` meldet es danach als unberührt (D-354).

## 5. Deinstallation oder Werkzeugwechsel

**Deaktivierung:** Overlay-Status `inaktiv` (das Werkzeug arbeitet nur noch lesend), danach
Entfernen der Laufzeitschicht, wenn gewünscht. Das Verzeichnis
`.koolie/core/` kann als Nachweis im Repository bleiben.

**Werkzeugwechsel:** Die kanonische Ebene `.koolie/core/framework/` bleibt unverändert —
sie ist werkzeugneutral. Ein anderer KI-Client wird als **Client Pack** unter
`.koolie/core/clients/<client>/` angelegt: eine `CLIENT_PACK.md` mit Pfadabbildung und
Fähigkeitsmatrix und ein `manifest.json` mit der maschinenlesbaren Abbildung. **Die
Wurzelartefakte kommen aus dem Kern**, nicht aus dem Pack (`.koolie/core/clients/README.md`,
Abschnitt 5).

Vor dem Wechsel ist die **Fähigkeitsmatrix** des Zielclients auszuwerten: Sie weist je Zusage
aus, ob der Client sie technisch erzwingt oder ob sie nur noch als Anweisung im Kontext steht.
Eine Kernzusage, die der Zielclient nicht technisch durchsetzt, ist begründungspflichtig, im
Overlay als Ausnahme zu führen und durch `<SECURITY_CONTACT>` freizugeben. Ein Wechsel, der
diese Prüfung überspringt, senkt das Schutzniveau, ohne dass es jemand bemerkt.

## 6. Warum der Kern gebündelt ist

Bis Release 0.1.0 lagen zwölf Core-Verzeichnisse und vier Core-Dateien direkt im
Wurzelverzeichnis — unmittelbar neben dem Produktivcode des Projekts. Das hatte zwei
praktische Folgen: Die Übernahme war fehleranfällig, weil bei jedem Schritt zu entscheiden
war, welches Verzeichnis zum Framework und welches zum Projekt gehört; und das
Wurzelverzeichnis eines Projekts wurde unübersichtlich.

Die Bündelung ändert nichts an der Ebenenhierarchie und an keiner inhaltlichen Regel. Sie
trennt physisch, was ohnehin logisch getrennt war: **Der Kern ist ein Ordner, den man
ersetzt. Das Projekt ist alles daneben.**
