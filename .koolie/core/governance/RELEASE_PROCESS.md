# Betriebsmodell: Review-Zyklus, Versionierung, Release und Produktbeobachtung

| Attribut | Wert |
|---|---|
| ID | `FW-GOV-REL` |
| Version | `0.3.5` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |

## 1. Versionierung (normativ)

1. Das Framework folgt Semantic Versioning (`.koolie/core/VERSION`, `.koolie/core/CHANGELOG.md`): **MAJOR** bei Struktur- oder Hierarchieänderungen, die Overlays anpassen müssen; **MINOR** bei neuen Modulen, Skills oder Regeln ohne Overlay-Bruch; **PATCH** bei Korrekturen und Formulierungen.

   **Solange die Hauptversion 0 ist, gilt die MAJOR-Regel nicht:** Eine brechende Änderung erscheint dort als MINOR mit einem Migrationsabschnitt im Änderungsverzeichnis, weil `1.0.0` durch D-11 an fünf prüfbare Kriterien gebunden ist und eine vorzeitige Hauptversion das Release-Gate `FW-CL-11` entwerten würde. Ab `1.0.0` gilt die Regel oben unverändert.
2. Skills, Packs, Checklisten, Prompts und Overlays tragen eigene Versionen (Metadatentabellen). Jede Änderung an einem dieser Artefakte erhöht dessen Version im selben Release; die Release-Checkliste fordert das je Artefaktklasse ein. **Ein reiner Statuswechsel zählt dabei nicht als Änderung** (`.koolie/core/framework/core/01-governance.md` Abschnitt 5 Punkt 5, D-106) (`.koolie/core/checklists/11-framework-release.md`).

   **Eine kompatible Framework-Version nennen nur die Artefakte, die vom Kern abweichen können:** das Overlay (Steckbriefzeile „Kompatible Framework-Version") und das Client Pack (Zeile „Geprüfte Clientversion" für den Client, gegen den es belegt ist). Beide gehören nicht zum Kern – ein Overlay gehört dem Projekt, ein Pack bildet einen fremden Client ab, und beide können einem älteren Stand folgen. Skills, Checklisten und Prompts werden byte-gleich im Release ausgeliefert; ihre kompatible Framework-Version ist der Inhalt von `.koolie/core/VERSION` im selben Verzeichnis. Ein eigenes Feld je Datei wäre ein Wert, der bei jedem Release in Dutzenden Dateien nachzuziehen wäre und veraltet, ohne dass es auffällt (D-25).
3. Jede Auslieferung erfolgt als Release-Archiv mit Stand aus dem Framework-Repository; Projekte übernehmen nur Releases, keine Zwischenstände.

## 2. Review-Zyklus (normativ)

1. Regelmäßiger Review-Termin des Frameworks: `<TBD: Prüfzyklus, Vorschlag quartalsweise>` – Inhalte: offene Änderungsanträge, Feedback- und Lessons-Learned-Einträge, Vorfallauswertung, Metrik-Signale aus Piloten, Ergebnis der Produktbeobachtung.
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

### 4.1 Das Release-Archiv (normativ, seit `1.0.0` – D-321)

**Ein Release ist ab `1.0.0` erst dann eines, wenn es einen benannten Stand hat:** eine
annotierte, signierte Marke und ein daraus erzeugtes Archiv (Punkt 2), weil Abschnitt 8
die Nachweiskette mit dem Archiv beginnt.

**Die Reihenfolge ist normativ, und die Trennlinie ist der Freigabe-Commit** (D-330).
Die Schritte 1 bis 3 stehen **davor**, die Schritte 4 bis 7 **danach** – weil das Archiv
aus der **Marke** entsteht und die Marke auf dem Release-Commit sitzt.

| Schritt | Was | Wer | Lage |
|---|---|---|---|
| 1 | **Bestandsliste fortschreiben:** `.koolie/core/governance/ADOPTION_REGISTRY.md` nennt je Projekt den Stand, auf den es gehoben wurde. **Prüfung 82 hält die Spalte gegen `VERSION`** | Werkzeug oder Mensch | **vor** dem Commit |
| 2 | **Übernehmende Projekte heben**, und zwar aus dem **Arbeitsbaum**, beschränkt auf das Verfolgte (D-333): `rm -rf .koolie/core`, dann `(cd <framework> && git ls-files -z .koolie/core \| tar --null -T - -cf -) \| tar -xf - -C .`; danach `install.py --update` – alle drei Handgriffe in einem: `python <framework>/.koolie/core/install.py --target <projekt> --update` (D-362; aus dem Klon nur Verfolgtes, aus dem Arbeitsbaum) –, den Overlay-Wert in **drei** Trägern nachziehen, `validate-framework.py --strict-overlay` dort fahren **und im übernehmenden Projekt committen** (D-343). **Ausnahmslos, auch bei einem Patch-Release ohne berührtes Artefakt** | Werkzeug oder Mensch | **vor** dem Commit, **nach dem letzten Eingriff in den Kern** |
| 3 | **Erzeugnisse der Lieferung bauen:** Hauptdokument (`build/assemble.py`) und Word-Fassung (`build/build-docx.py`) **je Client Pack**, und im Erzeugnis nachzählen | Werkzeug oder Mensch | **vor** dem Commit |
| 4 | **Annotierte, signierte Marke** auf dem Release-Commit: `v` und der Inhalt von `VERSION`. Die Nachricht nennt Release, Antrag, die Entscheidungen **und die Freigabezeile** – *„Freigegeben durch den Framework Owner am `<JJJJ-MM-TT>`"* (D-334, `K-111`). Damit trägt die Marke die Unterschrift, und deshalb setzt sie der Mensch | **der Framework Owner, nicht ein Werkzeug** | **nach** dem Commit |
| 5 | **Archiv** aus der Marke, mit **ausdrücklicher** Zeilenendeform **und ausdrücklichem Dateimodus**: `git -c core.eol=lf -c core.autocrlf=input -c tar.umask=022 archive --format=tar.gz --prefix=koolie-<Version>/ -o <Ziel> v<Version>` – ohne `tar.umask=022` trägt git jede Datei mit `0664` und `install.command` mit `0775` (gemessen an `v1.7.0`, D-369) | Werkzeug oder Mensch | **nach** dem Commit |
| 6 | **Im Erzeugnis nachzählen**, nicht der Meldung glauben: Dateizahl, Zeilenendeform, Lizenz in Wurzel **und** Kern, keine Erzeugnisse aus `build/out/`, **Modus der Tar-Einträge** – `install.command` `0755`, jede übrige Datei `0644` | Werkzeug oder Mensch | **nach** dem Commit |
| 7 | **Ablage außerhalb des Repositoriums**, zusammen mit der Prüfsumme des Archivs; Mitteilung an die übernehmenden Projekte nach Punkt 3 | Werkzeug oder Mensch | **nach** dem Commit |

**Das Heben gehört vor den Commit** (D-330), weil es ein Lauf gegen eine fremde
Installation ist und nicht die Fortschreibung einer Tabelle: Es findet, was kein
Validatorlauf findet, und hinter dem Merge läge dieser Prüfschritt hinter der Freigabe, die
er absichern soll. ⚠️ **Preis, benannt:** Wer vor dem Commit hebt, hebt aus einem
unveröffentlichten Stand; ändert sich der Baum danach noch, muss erneut gehoben werden –
Heben und Commit gehören als Paar, wie Commit und Marke.

**Die Bestandsliste wird an zwei Stellen geführt:** im Framework und in jeder
ausgelieferten Kopie. Deshalb nennt Schritt 1 den Zielstand, **bevor** Schritt 2 hebt –
sonst kopiert das Heben den alten Stand in die Projekte (D-331).

**Das Heben ist der letzte Eingriff in den Kern** (D-333): Jede Änderung an
`.koolie/core/**` danach macht die Kopien wieder falsch. Die Übergabe darf danach noch
geschrieben werden – sie ist ein lokales Arbeitsdokument, wird nicht versioniert und in
kein Projekt installiert (D-350).

**Schritt 2 endet mit dem Commit im übernehmenden Projekt** (D-343), weil ein
Verfahrensschritt, der endet, bevor sein Ergebnis dauerhaft ist, einen Zustand liefert und
keinen Stand. ⚠️ **Grenze, benannt:** Prüfung 82 misst nur die Behauptung der
Bestandsliste, nicht den Stand des Projekts (D-331), und der Git-Stand eines Projekts
außerhalb dieses Repositoriums ist für keine Prüfung erreichbar (D-299). Es bleibt ein
Verfahrensschritt, dessen Gegenstand im übernehmenden Repositorium jederzeit sichtbar ist.

**Die Quelle des Hebens ist der Arbeitsbaum, nicht `HEAD`** (D-333): Vor dem Commit
fehlen `git archive HEAD` der Änderungsantrag und das Protokoll des Releases. ⚠️ **Die
Beschränkung auf das Verfolgte ist nicht verzichtbar:** Sie hält Bytecode und `build/out/`
draußen.

⚠️ **Grenze zu Schritt 3, benannt:** Hauptdokument und Word-Fassung liegen unter
`build/out/` und stehen in der `.gitignore`; keine Prüfung erreicht sie (D-332, `K-110`).
Deshalb ist ihr Bau ein benannter Schritt.

**Die Signatur braucht eine Prüfvorrichtung, sonst belegt sie die halbe Aussage**
(D-327): Ohne hinterlegten Unterzeichner meldet `git tag -v` keine Bestätigung. Einmal je
Arbeitsplatz:

```
git config --local gpg.ssh.allowedSignersFile ".git/allowed_signers"
printf '%s %s\n' "<Adresse des Taggers>" "$(cat ~/.ssh/id_ed25519.pub)" \
  > .git/allowed_signers
```

⚠️ **Die Datei liegt unter `.git/` und wird nicht versioniert** – sie bindet eine Adresse
an einen Schlüssel, und eine Adresse im Kern meldet Prüfung 6 zu Recht. Ohne sie belegt
die Signatur nur, dass jemand mit diesem Schlüssel unterschrieben hat – nicht, wem der
Schlüssel gehört.

**Die Marke ist nicht delegierbar** (D-319, D-321): Sie sagt, **wer** freigegeben hat. Ein
Werkzeug kann sie technisch setzen und mit einem vorhandenen Schlüssel sogar signieren –
und genau deshalb darf es nicht.

**Für den Commit gilt eine engere, prüfbare Regel** (D-334): Ein Commit ist genau dann
nicht delegierbar, wenn er eine **Unterschrift trägt** – eine Gegenzeichnung nach D-319
oder eine Freigabezeile nach `FW-CL-11`. Ein Release-Commit ohne solchen Inhalt trägt
keine, und ein Werkzeug, das ihn setzt, fälscht nichts.

**Die Zeilenenden des Archivs setzt der Befehl, nicht die `.gitattributes`** (D-328):
`git archive` schreibt im Arbeitsbaum-Format aus, nicht im Blob-Format – mit
`core.autocrlf` `true` oder `false` entsteht CRLF, mit `input` LF. Deshalb stehen die
Schalter in Schritt 5, und deshalb wird in Schritt 6 nachgezählt. ⚠️ **Verworfen:**
`eol=lf` in der `.gitattributes` – sie zwänge auch den Arbeitsbaum auf LF (D-328,
`CR-2026-128` E1).

**Den Dateimodus setzt ebenfalls der Befehl** (D-369): Mit gits Voreinstellung
`tar.umask=0002` trägt das Archiv jede Datei mit `0664` und `install.command` mit `0775`,
gruppenschreibbar; mit `-c tar.umask=022` sind es `0644` und `0755`, bytegleich
wiederholbar. Der Modus ist deshalb ein Gegenstand von Schritt 6, nicht nur die
Zeilenendeform.

⚠️ **Grenze, benannt:** Ein Verfahrensschritt ist schwächer als eine Prüfung. Der
Gegenstand liegt **außerhalb** des Repositoriums; eine Prüfung dagegen wäre im Framework
grün und in jeder Installation ohne Archiv rot (D-299).

⚠️ **Das Archiv enthält nur Versioniertes.** Hauptdokument und Word-Fassung sind
Erzeugnisse unter `build/out/` und stehen in der `.gitignore`; wer sie mitliefern will,
legt sie **neben** das Archiv, nicht hinein.

## 5. Freigabe und Deprecation von Skills (normativ)

Lebenszyklus und Kriterien: `.koolie/core/framework/core/08-skill-conventions.md` Abschnitt 7. Ergänzend: Deprecation wird mindestens ein MINOR-Release vor der Zurückziehung angekündigt; die Hinweisdatei im Skill-Verzeichnis nennt Nachfolger und Migrationsweg; Projekte mit eigenen `prj-*`-Skills prüfen bei jedem Release die Kompatibilität.

## 6. Umgang mit Produktänderungen vom KI-Client (normativ)

1. **Beobachtung:** Der Framework Owner sichtet im Review-Zyklus (und anlassbezogen) die offiziellen Quellen **je installiertem Client Pack**: Produkt-Changelog und Dokumentation des jeweiligen Clients. Quellenliste: Hauptdokument, Anhang „Quellen und Verifikationsbedarf".
2. **Bewertung:** Jede relevante Änderung wird klassifiziert: (a) kosmetisch – keine Aktion; (b) erweiternd – Chance, als Änderungsantrag bewerten; (c) brechend – betroffene `[DOK]`-Aussagen, Pfade, Berechtigungen oder Skills identifizieren.
3. **Reaktion auf brechende Änderungen:** Sofortmaßnahme kommunizieren (zum Beispiel betroffenen Mechanismus nicht nutzen), Änderungsantrag mit Priorität, gegebenenfalls Hotfix-Release; Belegspalte der betroffenen Matrixzeilen aktualisieren; Testkatalog-Klasse AK (Aktualität) erneut ausführen.
4. **Werkzeugwechsel:** Dank Tool Independence (P8) beschränkt sich ein Wechsel oder Parallelbetrieb eines anderen KI-Werkzeugs auf ein neues Client Pack (`.koolie/core/clients/README.md`); die kanonischen Regeln in `.koolie/core/framework/` bleiben unverändert. Vor dem Wechsel ist die Fähigkeitsmatrix des Zielclients auszuwerten. Ein solcher Schritt ist ein MAJOR-Release.

## 7. Behandlung von Sicherheitsvorfällen, Lessons Learned, Feedback, Ausnahmen (Verweise)

- Vorfälle: `INCIDENT_HANDLING.md` (Erfassung, Auswertung, Rückfluss in Regeln).
- Feedback: `FEEDBACK_PROCESS.md` (niederschwellig, ausgewertet im Review-Zyklus).
- Ausnahmen: `EXCEPTION_PROCESS.md` (befristet, kompensiert, registriert).
- Lessons Learned: fester Tagesordnungspunkt des Review-Zyklus; Ergebnisse fließen als Änderungsanträge ein und werden im Decision Log nachgewiesen.

## 8. Auditierbarkeit (normativ)

Nachweiskette je Zeitpunkt: Framework-Version (`.koolie/core/VERSION`, Release-Archiv) → Overlay-Version (Overlay-Steckbrief) → Skill-Versionen (Metadaten) → Berechtigungsstand (Berechtigungsdatei im Repository-Verlauf) → Nutzung je Änderung (KI-Nutzungsvermerk im Merge Request) → Vorfälle und Ausnahmen (Register). Alle Nachweise liegen in versionierten Repositories oder im Merge-Request-System; gesonderte Schattenablagen sind unzulässig.
