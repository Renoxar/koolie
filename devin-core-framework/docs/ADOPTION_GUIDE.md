# Übernahme des Frameworks in ein Projekt

| Attribut | Wert |
|---|---|
| ID | `FW-DOC-ADOPT` |
| Version | `0.4.0` |
| Status | `entwurf` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Checkliste | `devin-core-framework/checklists/10-project-adoption.md` (verbindlicher Nachweis) |

## 1. Grundprinzip

Der gesamte unveränderliche Kern liegt in **einem** Verzeichnis: `devin-core-framework/`. Es
wird als Release in das Wurzelverzeichnis des Projekt-Repositorys kopiert und bleibt
byte-gleich zum Release. Änderungswünsche laufen als Änderungsantrag an den Framework Owner
(`devin-core-framework/governance/FEEDBACK_PROCESS.md`), nicht als lokale Bearbeitung.

Zwei Ladeorte lassen sich nicht mitbündeln, weil sie Werkzeugkonvention sind und nicht
konfigurierbar `[DOK]`:

| Bestandteil | Rolle |
|---|---|
| Wurzel-Anweisungsdatei | Zentrale Agentenanweisung, wird vom Client automatisch geladen |
| Laufzeitschicht | Regelablage, Skill-Ablage, Agentenprofile, Berechtigungsdatei, Hook-Konfiguration |

Die tatsächlichen Pfade unterscheiden sich je Client; sie stehen in
`devin-core-framework/docs/RUNTIME_GLOSSARY.md` und im `CLIENT_PACK.md` des gewählten Packs.

Deshalb bringt der Kern diese Bestandteile im `root-template/` des jeweiligen Client Packs
mit (`devin-core-framework/clients/<client>/root-template/`) und
`devin-core-framework/install.py` legt sie an ihrem Platz an. Welcher Client gilt, entscheidet
`--client`; `--list-clients` zeigt die verfügbaren.

**Projektspezifisch sind ausschließlich:**

| Bestandteil | Ebene |
|---|---|
| `project-overlay/` einschließlich `forbidden-terms.txt` | 4 |
| `20-project-overlay.md` in der Regelablage (plus optionale `2N-overlay-*`) | 4 |
| die ausgefüllten Werte in der Berechtigungsdatei | 3/4 |
| die **Entscheidung**, welche Packs aktiviert sind (Overlay Abschnitt 1) | 5/6 |
| `prj-*`-Skills in der Skill-Ablage | 4 |
| die **Entscheidung**, welches Client Pack verwendet wird | – |

Alles andere ist Core. Ein Projektwechsel tauscht nur die Overlay-Bestandteile; der Core
bleibt unberührt (P10, Baum 6).

## 2. Neuaufnahme (Schrittfolge)

1. **Voraussetzungen der Organisation:** Werkzeugfreigabe, Datenschutz- und Vertragsprüfung,
   dokumentierte Team-Einstellungen (`devin-core-framework/framework/org-policies/`;
   Klärungspunkte K-05/K-06).

2. **Kern kopieren:** Das Verzeichnis `devin-core-framework/` in das Wurzelverzeichnis des
   Projekt-Repositorys kopieren. Bei Monorepos in das Wurzelverzeichnis des Workspace, den
   Devin öffnet (A-01).

   ```bash
   cp -r devin-core-framework/ /pfad/zum/projekt/
   ```

3. **Wurzelbestandteile anlegen:**

   ```bash
   cd /pfad/zum/projekt
   python devin-core-framework/install.py --list-clients
   python devin-core-framework/install.py --client <client>
   ```

   Das Skript legt die Wurzel-Anweisungsdatei, ihre `.example`-Vorlage für nutzerlokale
   Ergänzungen, die Laufzeitschicht und – sofern noch nicht vorhanden – `project-overlay/`
   an. Bestehende Projektdateien werden nie überschrieben.

   **Vor der Wahl des Client Packs** die Fähigkeitsmatrix des Kandidaten lesen
   (`devin-core-framework/clients/<client>/CLIENT_PACK.md`): Sie weist aus, welche Zusagen
   des Frameworks dieser Client technisch erzwingt und welche nur als Anweisung im Kontext
   stehen.

   Übernimm die `.gitignore` des Framework-Repositorys **nicht** unverändert: Dort sind
   die Wurzel-Anweisungsdatei, die Laufzeitschicht und `project-overlay/` ausgeschlossen,
   weil sie im Framework-Repository Erzeugnisse sind. Im Projekt gehören sie in die
   Versionierung.

4. **Overlay ausfüllen:** `project-overlay/OVERLAY.md` vollständig; Laufzeitfassung
   `20-project-overlay.md` in der Regelablage synchron halten; Werte in der
   Berechtigungsdatei eintragen, ohne die Kernregeln im Block `_core_rules_integrity` zu entfernen; Manifest und
   Dokumente einpflegen.

5. **Packs aktivieren.** Kein Pack ist nach der Installation aktiv — auch nicht das
   Referenzpack `software-development`. Je benötigtem Pack: Rolle im Overlay Abschnitt 1
   aufführen, dann Laufzeitfassung und – falls vorhanden – Skills kopieren:

   ```bash
   # <regelablage> ist der Pfad aus dem manifest.json des gewählten Client Packs
   P=devin-core-framework/framework/role-packs/software-development
   cp $P/runtime/30-role-software-development.md <regelablage>/
   ```

   Einmal aktiviert, hält `install.py --update` diese Bestandteile auf dem Stand des
   Releases; `--check` meldet lokale Abweichungen.

6. **Projektlokale Härtung:** `project-overlay/forbidden-terms.txt` mit den realen Projekt-,
   Kunden-, Behörden-, Produkt- und Systemnamen füllen (bleibt projektlokal); gegebenenfalls
   zusätzliche Verweigerungsregeln in der Berechtigungsdatei.

7. **Validieren und testen:**

   ```bash
   python devin-core-framework/tests/scripts/validate-framework.py --strict-overlay
   python devin-core-framework/install.py --check
   ```

   Der erste Lauf prüft Struktur, Inhalte und Aktivierungsreife des Overlays. Der zweite
   prüft, ob eine Core-Datei lokal verändert wurde — das wäre eine Bearbeitung an der
   falschen Stelle. Anschließend die Basistests des Testkatalogs auf dem Übungsrepository
   ausführen und das Übungsrepository für das Onboarding erzeugen
   (`devin-core-framework/onboarding/exercises/README.md`).

8. **Organisation im Projekt:** Rollen zuordnen (außerhalb des Repos), Eskalationskanäle,
   Ablageorte für Berichte und Pläne, Feedbackkanal.

9. **Overlay aktivieren:** Checkliste 10 abschließen, Overlay-Status `aktiv`, Meldung an den Framework
   Owner (Bestandsliste).

10. **Menschen befähigen:** Onboarding vor produktiver Nutzung; Pilotparameter setzen, wenn das
   Projekt als Pilot läuft.

## 3. Aktualisierung auf ein neues Framework-Release

1. Release-Notes und Migrationshinweise lesen
   (`devin-core-framework/CHANGELOG.md` des neuen Releases).

2. Das Verzeichnis `devin-core-framework/` durch das neue ersetzen, dann die
   Wurzelbestandteile nachziehen:

   ```bash
   python devin-core-framework/install.py --update
   ```

   `--update` überschreibt die Core-Dateien im Wurzelverzeichnis (Wurzel-Anweisungsdatei,
   Regelablage `00-`, `10-`, `15-`, die `*-TEMPLATE`-Vorlagen, Skill-Ablage `fw-*`,
   Agentenprofile, Hook-Konfiguration) **und die Bestandteile aktivierter Packs**, deren
   Quelle im Kern liegt (Regelablage `30-`, `40-` sowie Skill-Ablage `role-*`, `tech-*`).
   Welche Datei dazuzählt, steht im `manifest.json` des Client Packs. Unberührt bleiben die
   Projektbestandteile: Berechtigungsdatei, Overlay, `prj-*`-Skills und projekteigene
   Packs. Die Berechtigungsdatei wird bewusst nicht angefasst, weil sie Projektwerte enthält — prüfe nach dem Wechsel, ob die Kernregeln
   noch vollständig sind.

3. Overlay-Bestandteile gegen die Migrationshinweise prüfen (neue Pflichtfelder, geänderte
   Platzhalter, deprecatete Skills).

4. Validator (`--strict-overlay`) und Basistests erneut ausführen; bei MAJOR-Releases
   zusätzlich FW-RE-01/02.

5. Overlay-Änderungsverlauf ergänzen (neue kompatible Framework-Version); Team über relevante
   Änderungen informieren; Onboarding-Materialstand prüfen.

## 4. Mehrere Repositories, ein Projekt

Je Repository, das Devin öffnet, liegt eine vollständige Framework-Integration (Root-Regeln
wirken je Workspace). Das Overlay KANN geteilt gepflegt und je Repository ausgerollt werden;
seit der Bündelung ist das Ausrollen ein Kopiervorgang plus Skriptaufruf und damit
skriptbar:

```bash
for repo in repo-a repo-b; do
  cp -r devin-core-framework/ "$repo/"
  (cd "$repo" && python devin-core-framework/install.py --update)
done
```

Die Pfadlisten (Abschnitt 4 des Overlays) sind je Repository spezifisch und werden nicht
mitkopiert — `install.py` überschreibt `project-overlay/` nie.

## 5. Deinstallation oder Werkzeugwechsel

**Deaktivierung:** Overlay-Status `inaktiv` (das Werkzeug arbeitet nur noch lesend), danach
Entfernen der Laufzeitschicht, wenn gewünscht. Das Verzeichnis
`devin-core-framework/` kann als Nachweis im Repository bleiben.

**Werkzeugwechsel:** Die kanonische Ebene `devin-core-framework/framework/` bleibt unverändert —
sie ist werkzeugneutral. Ein anderer KI-Client wird als **Client Pack** unter
`devin-core-framework/clients/<client>/` angelegt: eine `CLIENT_PACK.md` mit Pfadabbildung und
Fähigkeitsmatrix sowie ein `root-template/` mit den Wurzelartefakten in der Form dieses Clients
(`devin-core-framework/clients/README.md`).

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
