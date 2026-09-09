# Übernahme des Frameworks in ein Projekt

| Attribut | Wert |
|---|---|
| ID | `FW-DOC-ADOPT` |
| Version | `0.2.0` |
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

| Pfad | Rolle |
|---|---|
| `AGENTS.md` | Zentrale Agentenanweisung, wird von Devin automatisch geladen |
| `.devin/` | Laufzeitschicht: `rules/`, `skills/`, `agents/`, `config.json`, `hooks.v1.json` |

Deshalb bringt der Kern diese Bestandteile in `devin-core-framework/root-template/` mit und
`devin-core-framework/install.py` legt sie an ihrem Platz an.

**Projektspezifisch sind ausschließlich:**

| Bestandteil | Ebene |
|---|---|
| `project-overlay/` einschließlich `forbidden-terms.txt` | 4 |
| `.devin/rules/20-project-overlay.md` (plus optionale `2N-overlay-*`) | 4 |
| die ausgefüllten Werte in `.devin/config.json` | 3/4 |
| aktivierte Pack-Laufzeitfassungen (`.devin/rules/30-*`, `40-*`) | 5/6 |
| `prj-*`-Skills unter `.devin/skills/` | 4 |

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
   python devin-core-framework/install.py
   ```

   Das Skript legt `AGENTS.md`, `AGENTS.local.md.example`, `.devin/` und – sofern noch nicht
   vorhanden – `project-overlay/` an. Bestehende Projektdateien werden nie überschrieben.

   Übernimm die `.gitignore` des Framework-Repositorys **nicht** unverändert: Dort sind
   `AGENTS.md`, `.devin/` und `project-overlay/` ausgeschlossen, weil sie im
   Framework-Repository Erzeugnisse sind. Im Projekt gehören sie in die Versionierung.

4. **Overlay ausfüllen:** `project-overlay/OVERLAY.md` vollständig; Laufzeitfassung
   `.devin/rules/20-project-overlay.md` synchron halten; Werte in `.devin/config.json`
   eintragen, ohne die Kernregeln im Block `_core_rules_integrity` zu entfernen; Manifest und
   Dokumente einpflegen; Packs aktivieren.

5. **Projektlokale Härtung:** `project-overlay/forbidden-terms.txt` mit den realen Projekt-,
   Kunden-, Behörden-, Produkt- und Systemnamen füllen (bleibt projektlokal); gegebenenfalls
   zusätzliche `deny`-Pfade in `.devin/config.json`.

6. **Validieren und testen:**

   ```bash
   python devin-core-framework/tests/scripts/validate-framework.py --strict-overlay
   python devin-core-framework/install.py --check
   ```

   Der erste Lauf prüft Struktur, Inhalte und Aktivierungsreife des Overlays. Der zweite
   prüft, ob eine Core-Datei lokal verändert wurde — das wäre eine Bearbeitung an der
   falschen Stelle. Anschließend die Basistests des Testkatalogs auf dem Übungsrepository
   ausführen und das Übungsrepository für das Onboarding erzeugen
   (`devin-core-framework/onboarding/exercises/README.md`).

7. **Organisation im Projekt:** Rollen zuordnen (außerhalb des Repos), Eskalationskanäle,
   Ablageorte für Berichte und Pläne, Feedbackkanal.

8. **Aktivieren:** Checkliste 10 abschließen, Overlay-Status `aktiv`, Meldung an den Framework
   Owner (Bestandsliste).

9. **Menschen befähigen:** Onboarding vor produktiver Nutzung; Pilotparameter setzen, wenn das
   Projekt als Pilot läuft.

## 3. Aktualisierung auf ein neues Framework-Release

1. Release-Notes und Migrationshinweise lesen
   (`devin-core-framework/CHANGELOG.md` des neuen Releases).

2. Das Verzeichnis `devin-core-framework/` durch das neue ersetzen, dann die
   Wurzelbestandteile nachziehen:

   ```bash
   python devin-core-framework/install.py --update
   ```

   `--update` überschreibt die Core-Dateien im Wurzelverzeichnis (`AGENTS.md`,
   `.devin/rules/00-`, `10-`, `15-`, die `*-TEMPLATE`-Vorlagen, `.devin/skills/fw-*`,
   `.devin/agents/`, `hooks.v1.json`) und lässt die Projektbestandteile unberührt.
   `.devin/config.json` wird bewusst nicht angefasst, weil sie Projektwerte enthält — prüfe
   nach dem Wechsel, ob die Kernregeln noch vollständig sind.

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

**Deaktivierung:** Overlay-Status `inaktiv` (Devin arbeitet nur noch lesend), danach
Entfernen der `.devin/`-Laufzeitschicht, wenn gewünscht. Das Verzeichnis
`devin-core-framework/` kann als Nachweis im Repository bleiben.

**Werkzeugwechsel:** Die kanonische Ebene `devin-core-framework/framework/` bleibt; eine neue
Laufzeitschicht wird analog zu `.devin/` aufgebaut und als zweite Vorlage unter
`devin-core-framework/root-template/` geführt (P8; MAJOR-Release,
`devin-core-framework/governance/RELEASE_PROCESS.md` Abschnitt 6.4).

## 6. Warum der Kern gebündelt ist

Bis Release 0.1.0 lagen zwölf Core-Verzeichnisse und vier Core-Dateien direkt im
Wurzelverzeichnis — unmittelbar neben dem Produktivcode des Projekts. Das hatte zwei
praktische Folgen: Die Übernahme war fehleranfällig, weil bei jedem Schritt zu entscheiden
war, welches Verzeichnis zum Framework und welches zum Projekt gehört; und das
Wurzelverzeichnis eines Projekts wurde unübersichtlich.

Die Bündelung ändert nichts an der Ebenenhierarchie und an keiner inhaltlichen Regel. Sie
trennt physisch, was ohnehin logisch getrennt war: **Der Kern ist ein Ordner, den man
ersetzt. Das Projekt ist alles daneben.**
