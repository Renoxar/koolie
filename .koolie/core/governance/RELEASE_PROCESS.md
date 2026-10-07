# Betriebsmodell: Review-Zyklus, Versionierung, Release und Produktbeobachtung

| Attribut | Wert |
|---|---|
| ID | `FW-GOV-REL` |
| Version | `0.5.2` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |

## 1. Versionierung (normativ)

1. Das Framework folgt Semantic Versioning (`.koolie/core/VERSION`, `.koolie/core/CHANGELOG.md`): **MAJOR** bei Struktur- oder Hierarchieänderungen, die Overlays anpassen müssen; **MINOR** bei neuen Modulen, Skills oder Regeln ohne Overlay-Bruch; **PATCH** bei Korrekturen und Formulierungen.
2. Skills, Packs, Checklisten, Prompts und Overlays tragen eigene Versionen (Metadatentabellen). Jede Änderung an einem dieser Artefakte erhöht dessen Version im selben Release; die Release-Checkliste (`.koolie/core/checklists/11-framework-release.md`) fordert das je Artefaktklasse ein. Ein reiner Statuswechsel zählt nicht als Änderung (`.koolie/core/framework/core/01-governance.md` Abschnitt 5 Punkt 5).

   Eine kompatible Framework-Version nennen nur die Artefakte, die vom Kern abweichen können:

   | Artefakt | Steckbriefzeile | Warum |
   |---|---|---|
   | Overlay | „Kompatible Framework-Version" | gehört dem Projekt und kann einem älteren Stand folgen |
   | Client Pack | „Geprüfte Clientversion" | bildet einen fremden Client ab und ist gegen eine Version belegt |

   Skills, Checklisten und Prompts werden byte-gleich ausgeliefert; ihre kompatible Framework-Version ist der Inhalt von `.koolie/core/VERSION` daneben. Ein eigenes Feld je Datei müsste bei jedem Release in Dutzenden Dateien nachgezogen werden.
3. Jede Auslieferung erfolgt als Release-Archiv mit Stand aus dem Framework-Repository; Projekte übernehmen nur Releases, keine Zwischenstände.

## 2. Review-Zyklus (normativ)

1. Das Framework wird **quartalsweise** überprüft; die Produktbeobachtung (Abschnitt 6) zusätzlich vor jedem Release, das die Zielspanne eines Client Packs berührt. Inhalte: offene Änderungsanträge, Feedback- und Lessons-Learned-Einträge, Vorfallauswertung, Metrik-Signale aus Piloten, Ergebnis der Produktbeobachtung.
2. Zwischen den Terminen sind Hotfix-Releases zulässig für: Sicherheits- oder Datenschutzlücken im Framework, gebrochene Mechanismen des KI-Clients, fehlerhafte Skills mit Schadenspotenzial.

## 3. Änderungsanträge (normativ)

1. Jede Änderung an Core, Packs, Skills, Checklisten, Prompts, Bäumen oder Templates beginnt als Änderungsantrag (`CHANGE_REQUEST_TEMPLATE.md`) an den zuständigen Owner (RACI).
2. Der Owner prüft: Zuordnung nach Entscheidungsbaum 6, Verschärfungsprinzip, Auswirkungen auf Laufzeitfassungen, Test- und Dokumentationsbedarf.
3. Angenommene Anträge werden umgesetzt, validiert (`.koolie/core/tests/scripts/validate-framework.py`), im Testkatalog abgedeckt und im Decision Log sowie `.koolie/core/CHANGELOG.md` dokumentiert.

## 4. Release-Prozess (normativ)

1. Release-Vorbereitung nach `.koolie/core/checklists/11-framework-release.md` (Konsistenz, Projektneutralität, Produktstand, Testkatalog).
2. Freigabe durch den Framework Owner; Archiv erzeugen; Version und Changelog veröffentlichen.
3. Kommunikation an alle übernehmenden Projekte mit Migrationshinweisen (betroffene Overlay-Felder, neue Pflichtprüfungen, deprecatete Skills).
4. Projekte übernehmen Releases über `.koolie/core/docs/ADOPTION_GUIDE.md` Abschnitt „Aktualisierung"; der Framework Owner führt die Bestandsliste der Projekte mit eingesetzter Version in `.koolie/core/governance/ADOPTION_REGISTRY.md` (Auditierbarkeit).

### 4.1 Das Release-Archiv (normativ)

Ein Release hat einen benannten Stand: eine annotierte, signierte Marke und ein daraus erzeugtes
Archiv. Mit dem Archiv beginnt die Nachweiskette aus Abschnitt 8.

Die Reihenfolge ist normativ. Die Trennlinie ist der Release-Commit: Die Schritte 1 bis 3 stehen
davor, die Schritte 4 bis 7 danach, weil das Archiv aus der Marke entsteht und die Marke auf dem
Release-Commit sitzt.

| Schritt | Was | Wer | Lage |
|---|---|---|---|
| 1 | **Bestandsliste fortschreiben:** `.koolie/core/governance/ADOPTION_REGISTRY.md` nennt je Projekt den Zielstand. Prüfung 82 hält die Spalte gegen `VERSION` | Werkzeug oder Mensch | vor dem Commit |
| 2 | **Übernehmende Projekte aktualisieren:** `python <framework>/.koolie/core/install.py --target <projekt> --update` (kopiert aus dem Arbeitsbaum nur Verfolgtes und ruft dann `install.py --update` im Projekt auf); den Overlay-Wert in den drei Trägern nachziehen; dort `validate-framework.py --strict-overlay` und `install.py --probe` fahren; das Update **im übernehmenden Projekt committen**. Ausnahmslos, auch bei einem Patch-Release ohne berührtes Artefakt | Werkzeug oder Mensch | vor dem Commit, nach dem letzten Eingriff in den Kern |
| 3 | **Erzeugnisse der Lieferung bauen:** Hauptdokument (`build/assemble.py`) und Word-Fassung (`build/build-docx.py`) je Client Pack, und im Erzeugnis nachzählen | Werkzeug oder Mensch | vor dem Commit |
| 4 | **Annotierte, signierte Marke** auf dem Release-Commit: `v` und der Inhalt von `VERSION`. Die Nachricht nennt Release, Antrag, Entscheidungen und die Freigabezeile *„Freigegeben durch den Framework Owner am `<JJJJ-MM-TT>`"* | **der Framework Owner, nicht ein Werkzeug** | nach dem Commit |
| 5 | **Archiv** aus der Marke: `git -c core.eol=lf -c core.autocrlf=input -c tar.umask=022 archive --format=tar.gz --prefix=koolie-<Version>/ -o <Ziel> v<Version>` | Werkzeug oder Mensch | nach dem Commit |
| 6 | **Im Erzeugnis nachzählen**, nicht der Meldung glauben: Dateizahl, Zeilenenden (LF), Lizenz in Wurzel und Kern, nichts aus `build/out/`, Modus der Tar-Einträge (`install.command` `0755`, jede übrige Datei `0644`) | Werkzeug oder Mensch | nach dem Commit |
| 7 | **Ablage außerhalb des Repositoriums** mit Prüfsumme des Archivs; Mitteilung an die übernehmenden Projekte nach Punkt 3 | Werkzeug oder Mensch | nach dem Commit |

**Zu Schritt 1 und 2.** Die Bestandsliste liegt im Framework und in jeder ausgelieferten Kopie.
Deshalb nennt Schritt 1 den Zielstand, bevor Schritt 2 aktualisiert – sonst kopiert das Update den alten
Stand in die Projekte. Prüfung 82 prüft nur die Zeile, nicht den Stand des Projekts; den Git-Stand
eines fremden Repositoriums erreicht keine Prüfung.

**Zu Schritt 2.** Das Update ist ein Lauf gegen eine fremde Installation und findet, was kein
Validatorlauf im Framework findet; deshalb steht es vor dem Commit und nicht hinter der Freigabe.

- Es ist der letzte Eingriff in den Kern. Jede Änderung an `.koolie/core/**` danach macht die
  Kopien falsch und verlangt ein erneutes Update. Die lokale Übergabe darf danach noch geschrieben
  werden; sie wird nicht versioniert und nicht installiert.
- Quelle ist der Arbeitsbaum, nicht `HEAD`: Vor dem Commit fehlen in `HEAD` der Änderungsantrag
  und das Protokoll des Releases. Die Beschränkung auf verfolgte Dateien hält Bytecode und
  `build/out/` draußen.
- `--update` schreibt Berechtigungs- und Hook-Datei nie. Erst `install.py --probe` meldet, wenn
  eine neue Werkzeugklasse im Matcher des Projekts fehlt (Kontrolle H2).
- Der Schritt endet mit dem Commit im übernehmenden Projekt, damit das Update dauerhaft ist.

**Zu Schritt 3.** Hauptdokument und Word-Fassung liegen unter `build/out/`, stehen in der
`.gitignore` und gehören nicht ins Archiv. Keine Prüfung erreicht sie. Wer sie mitliefert, legt sie
neben das Archiv.

**Zu Schritt 4.** Die Marke sagt, wer freigegeben hat; deshalb setzt sie der Mensch. Ein Werkzeug
könnte sie mit einem vorhandenen Schlüssel signieren und darf es gerade deshalb nicht. Für Commits
gilt: Ein Commit ist nur dann nicht delegierbar, wenn er eine Unterschrift trägt – eine
Gegenzeichnung oder eine Freigabezeile nach `FW-CL-11`. Ein Release-Commit ohne solchen Inhalt darf
ein Werkzeug setzen.

Damit `git tag -v` den Unterzeichner bestätigt, braucht jeder Arbeitsplatz einmal eine
Prüfvorrichtung:

```
git config --local gpg.ssh.allowedSignersFile ".git/allowed_signers"
printf '%s %s\n' "<Adresse des Taggers>" "$(cat ~/.ssh/id_ed25519.pub)" \
  > .git/allowed_signers
```

Die Datei liegt unter `.git/` und wird nicht versioniert: Sie bindet eine Adresse an einen
Schlüssel, und eine Adresse im Kern meldet Prüfung 6.

**Zu Schritt 5 und 6.** Zeilenenden und Dateimodus setzt der Befehl, nicht die `.gitattributes`.
`git archive` schreibt im Arbeitsbaum-Format: Mit `core.autocrlf` `true` oder `false` entsteht CRLF,
mit `input` LF. Ohne `tar.umask=022` trägt jede Datei `0664` und `install.command` `0775`
(gemessen an `v1.7.0`). Mit beiden Schaltern ist das Archiv bytegleich wiederholbar.

Die Schritte 1 bis 7 sind Verfahrensschritte, keine Prüfungen: Ihr Gegenstand liegt außerhalb des
Repositoriums, und eine Prüfung dagegen wäre in jeder Installation ohne Archiv rot.

### 4.2 Die Pakete der Paketquellen (normativ)

Die Pakete entstehen aus dem Archiv aus Schritt 5, nicht aus dem Arbeitsbaum. Wheel (PyPI),
npm-Paket, Scoop-Manifest und Homebrew-Formel tragen oder laden genau den Baum der Marke. Der Befehl
`koolie` in jedem Paket gibt vor `install.py` das Banner aus (Prüfung 112).

| Schritt | Was | Wer | Lage |
|---|---|---|---|
| 8 | **Pakete bauen und nachprüfen:** `python paketquellen/bauen.py --archiv <Archiv aus Schritt 5> --aus <Ablage>`. Das Skript prüft selbst nach – Dateimenge gleich dem Archiv, Version aus `VERSION`, `RECORD` des Wheels, Ziele der Befehle, kein Installationsskript im npm-Paket, Prüfsumme des Archivs in beiden Manifesten – und baut zweimal bytegleich; Exit 0 heißt ohne Befund. Die Erzeugnisse und `SHA256SUMS` liegen neben dem Archiv | Werkzeug oder Mensch | nach Schritt 7, jedes Release |
| 9 | **Veröffentlichen auf PyPI und npm** über den Workflow `.github/workflows/publish.yml` (Trusted Publishing, ohne Token). Er startet, sobald die Marke auf dem GitHub-Spiegel ankommt, und prüft zuerst Signatur und `VERSION` der Marke. Dann baut er die Pakete wie Schritt 8, lädt das Wheel auf TestPyPI und installiert es in ein Wegwerfprojekt. Erst nach der Freigabe des Framework Owners in der GitHub-Umgebung `release` gehen dieselben Bytes auf PyPI (mit Attestierung) und `@renoxar/koolie` auf npm (mit Provenienz); zum Schluss wartet er, bis beide Quellen die Pakete ausliefern, und vergleicht sie mit den Bytes, die er selbst hochgeladen hat. Scheitert ein Schritt, läuft keiner danach. Eine Version lässt sich nicht zurücknehmen und nicht neu vergeben – ein Befund nach dem Hochladen wird ein PATCH-Release. Scoop und Homebrew ruhen | Workflow; **der Framework Owner signiert die Marke und gibt die Umgebung `release` frei** | nach Schritt 8 |

Ob eine Paketquelle dem Befehl ein Terminal gibt, prüft keine Prüfung; es ist gemessen (Protokoll
`2026-09-30-paketquellen`). Die Homebrew-Formel ist gebaut, nicht gemessen.

**Vor einer ersten Veröffentlichung** – einer neuen Paketquelle oder eines geänderten Pakets – baut
`bauen.py --vorab N` aus dem Arbeitsbaum eine Vorabversion `<V>.devN` für TestPyPI, vor der
Signatur. Das Archiv dafür entsteht mit
`git -c core.eol=lf -c core.autocrlf=input archive --prefix=koolie-<V>/ $(git stash create)`; ohne
die beiden Schalter trägt es unter Windows CRLF. Die Probe macht der Owner im eigenen
Projektverzeichnis mit: Sie prüft, was ein Nutzer erlebt, nicht nur, ob der Befehl startet.

**Abgleich mit Schritt 8.** Der Workflow baut auf einer anderen Maschine. Wheel und npm-Paket
weichen deshalb in den Bytes von Schritt 8 ab (andere zlib-Kompression), im Inhalt nicht. Nach dem
Hochladen werden beide Pakete von PyPI und npm geladen und Datei für Datei gegen Schritt 8
verglichen: Dateimenge, Inhalt, Rechte und Zeitstempel. Die Anhänge des Gitea-Release sind die
veröffentlichten Bytes mit einer eigenen `SHA256SUMS`.

**Workflow-Datei und Marke nicht im selben Push.** Ändert ein Release `publish.yml`, zuerst `main`
spiegeln lassen, dann die Marke pushen – kommen beide im selben Spiegel-Push an, startet GitHub keinen
Lauf. Ist es passiert: die Marke auf GitHub löschen und den Spiegel in Gitea neu synchronisieren
(Repository → Einstellungen → Spiegel, oder `POST /api/v1/repos/<owner>/<repo>/push_mirrors-sync`).

**npm braucht nach dem Hochladen einige Minuten.** Die Version erscheint zuerst in den Metadaten
(`npm view`), die Paketdatei erst danach; der Workflow wartet auf die Datei.

**Ein gestörter Lauf wird wiederholt, die Marke bleibt.** Findet ein Job keinen Runner (*„job was
not acquired by Runner“*) oder antwortet TestPyPI mit einem Serverfehler, im Lauf „Re-run failed
jobs“ wählen, sobald die Störung vorbei ist – bestandene Jobs laufen nicht noch einmal, die Freigabe
der Umgebung `release` wird neu verlangt. Das geht auch über mehrere Versuche. Die Marke wird dafür
nie gelöscht oder neu gesetzt: Sie ist signiert, und ein neuer Push startet einen zweiten Lauf.
Der Workflow läuft auf einem festen Runner-Image (`ubuntu-24.04`), damit ein Wechsel des Images eine
Änderung an `publish.yml` ist und nicht still zwischen zwei Releases geschieht.

#### Einrichtung für Schritt 9 (einmalig, durch den Framework Owner)

| Wo | Was |
|---|---|
| Gitea, Repository → Einstellungen | **Actions abschalten.** Gitea liest ohne eigenes `.gitea/workflows/` auch `.github/workflows/` und startete den Workflow ein zweites Mal |
| Gitea, Repository → Einstellungen → Spiegel | Das GitHub-Token des Push-Spiegels braucht den Scope `workflow` (fein granuliert: „Workflows: Read and write“). Ohne ihn lehnt GitHub jeden Push ab, der `.github/workflows/` enthält – auch `main` und die Marke; die Ursache steht nur im `last_error` des Spiegels |
| GitHub `Renoxar/koolie` → Settings → Environments | Umgebung `testpypi` ohne Freigabe; Umgebung `release` mit dem Owner als *Required reviewer*. Bei beiden *Deployment branches and tags* auf das Muster `v*` für Tags beschränken |
| GitHub → Settings → Secrets and variables → Actions → *Variables* | Variable `KOOLIE_ALLOWED_SIGNERS` mit dem Inhalt der lokalen Datei `.git/allowed_signers` (eine Zeile: Adresse, Schlüsseltyp, öffentlicher Schlüssel). Eine Variable, kein Secret: Der Schlüssel ist öffentlich |
| pypi.org → Projekt `koolie` → Manage → Publishing | *Add a new publisher* → GitHub: Owner `Renoxar`, Repository `koolie`, Workflow `publish.yml`, Environment `release` |
| test.pypi.org → Projekt `koolie` → Manage → Publishing | dasselbe mit Environment `testpypi` |
| npmjs.com → Paket `@renoxar/koolie` → Settings → Trusted Publisher | GitHub Actions: Organization or user `Renoxar`, Repository `koolie`, Workflow filename `publish.yml`, Environment name `release`. Den Haken **„Allow npm publish“** setzen – ohne ihn erlaubt der Publisher nur `npm stage publish`, und `npm publish` scheitert mit `OIDC permission denied for this action` |

Nach dem ersten Lauf, der auf allen drei Quellen ankommt, werden die Tokens zurückgezogen: auf
PyPI, TestPyPI und npm löschen, die Benutzervariablen `PYPI_TOKEN`, `TESTPYPI_TOKEN` und
`NPM_TOKEN` entfernen. Bei npm zusätzlich unter *Publishing access* „Require two-factor
authentication and disallow tokens“ wählen.

**Rückfall.** Scheitert der Workflow an der Einrichtung, nicht an den Paketen, geht Schritt 9 von
Hand mit den Erzeugnissen aus Schritt 8: `uv publish` auf TestPyPI, Probe, PyPI; dann
`npm publish <tgz> --access public`. Das braucht die Tokens – sie werden deshalb erst nach dem
ersten erfolgreichen Lauf zurückgezogen.

## 5. Freigabe und Deprecation von Skills (normativ)

Lebenszyklus und Kriterien: `.koolie/core/framework/core/08-skill-conventions.md` Abschnitt 7. Ergänzend: Deprecation wird mindestens ein MINOR-Release vor der Zurückziehung angekündigt; die Hinweisdatei im Skill-Verzeichnis nennt Nachfolger und Migrationsweg; Projekte mit eigenen `prj-*`-Skills prüfen bei jedem Release die Kompatibilität.

## 6. Umgang mit Produktänderungen vom KI-Client (normativ)

1. **Beobachtung:** Der Framework Owner sichtet im Review-Zyklus (und anlassbezogen) die offiziellen Quellen **je installiertem Client Pack**: Produkt-Changelog und Dokumentation des jeweiligen Clients. Quellenliste: Hauptdokument, Anhang „Quellen und Verifikationsbedarf".
2. **Bewertung:** Jede relevante Änderung wird klassifiziert: (a) kosmetisch – keine Aktion; (b) erweiternd – Chance, als Änderungsantrag bewerten; (c) brechend – betroffene `[DOK]`-Aussagen, Pfade, Berechtigungen oder Skills identifizieren.
3. **Reaktion auf brechende Änderungen:** Sofortmaßnahme kommunizieren (zum Beispiel betroffenen Mechanismus nicht nutzen), Änderungsantrag mit Priorität, gegebenenfalls Hotfix-Release; Belegspalte der betroffenen Matrixzeilen aktualisieren; Testkatalog-Klasse AK (Aktualität) erneut ausführen.
4. **Werkzeugwechsel:** Ein Wechsel oder Parallelbetrieb eines anderen KI-Werkzeugs beschränkt sich auf ein neues Client Pack (`.koolie/core/clients/README.md`, Tool Independence P8); die kanonischen Regeln in `.koolie/core/framework/` bleiben unverändert. Vor dem Wechsel ist die Fähigkeitsmatrix des Zielclients auszuwerten. Ein solcher Schritt ist ein MAJOR-Release.

## 7. Behandlung von Sicherheitsvorfällen, Lessons Learned, Feedback, Ausnahmen (Verweise)

- Vorfälle: `INCIDENT_HANDLING.md` (Erfassung, Auswertung, Rückfluss in Regeln).
- Feedback: `FEEDBACK_PROCESS.md` (niederschwellig, ausgewertet im Review-Zyklus).
- Ausnahmen: `EXCEPTION_PROCESS.md` (befristet, kompensiert, registriert).
- Lessons Learned: fester Tagesordnungspunkt des Review-Zyklus; Ergebnisse fließen als Änderungsanträge ein und werden im Decision Log nachgewiesen.

## 8. Auditierbarkeit (normativ)

Nachweiskette je Zeitpunkt: Framework-Version (`.koolie/core/VERSION`, Release-Archiv) → Overlay-Version (Overlay-Steckbrief) → Skill-Versionen (Metadaten) → Berechtigungsstand (Berechtigungsdatei im Repository-Verlauf) → Nutzung je Änderung (KI-Nutzungsvermerk im Merge Request) → Vorfälle und Ausnahmen (Register). Alle Nachweise liegen in versionierten Repositories oder im Merge-Request-System; gesonderte Schattenablagen sind unzulässig.
