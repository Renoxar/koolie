# Betriebsmodell: Review-Zyklus, Versionierung, Release und Produktbeobachtung

| Attribut | Wert |
|---|---|
| ID | `FW-GOV-REL` |
| Version | `0.2.0` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |

## 1. Versionierung (normativ)

1. Das Framework folgt Semantic Versioning (`.koolie/core/VERSION`, `.koolie/core/CHANGELOG.md`): **MAJOR** bei Struktur- oder Hierarchieänderungen, die Overlays anpassen müssen; **MINOR** bei neuen Modulen, Skills oder Regeln ohne Overlay-Bruch; **PATCH** bei Korrekturen und Formulierungen.

   **Solange die Hauptversion 0 ist, gilt die MAJOR-Regel nicht.** Semantic Versioning stellt `0.y.z` ausdrücklich für die Entwicklungsphase frei; eine brechende Änderung erscheint dort als MINOR mit einem Migrationsabschnitt im Änderungsverzeichnis. Der Grund ist hier nicht formal, sondern inhaltlich: `1.0.0` ist durch D-11 an fünf prüfbare Kriterien gebunden. Eine Hauptversion für eine strukturelle Änderung zu verbrauchen, würde diese fünf Kriterien behaupten, ohne sie zu erfüllen – das Release-Gate `FW-CL-11` wäre entwertet. Ab `1.0.0` gilt die Regel oben unverändert.
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

**Ein Release ist ab `1.0.0` erst dann eines, wenn es einen benannten Stand hat.** Punkt 2
verlangt das Archiv seit der Erstfassung, und Abschnitt 8 beginnt die Nachweiskette mit
ihm; bis `0.91.0` ist in **106 Release-Commits keines erzeugt worden**, und das
Repositorium führte **null** Marken. *Eine Nachweiskette, deren erstes Glied fehlt, ist
eine Aufzählung.*

| Schritt | Was | Wer |
|---|---|---|
| 1 | **Annotierte, signierte Marke** auf dem Release-Commit: `v` und der Inhalt von `VERSION`, die Nachricht nennt Release, Antrag und die Entscheidungen | 🔴 **der Framework Owner, nicht ein Werkzeug** |
| 2 | **Archiv** aus der Marke: `git archive --format=tar.gz --prefix=koolie-<Version>/ -o <Ziel> v<Version>` | Werkzeug oder Mensch |
| 3 | **Ablage außerhalb des Repositoriums**, zusammen mit der Prüfsumme des Archivs | Werkzeug oder Mensch |
| 4 | Eintrag in `.koolie/core/governance/ADOPTION_REGISTRY.md` und Mitteilung an die übernehmenden Projekte nach Punkt 3 | Framework Owner |

🔴 **Die Signatur braucht eine Prüfvorrichtung, sonst belegt sie die halbe Aussage**
(D-327). Ohne hinterlegten Unterzeichner meldet `git tag -v` **keine** Bestätigung –
gemessen unmittelbar nach der ersten Marke dieses Repositoriums. Einmal je Arbeitsplatz:

```
git config --local gpg.ssh.allowedSignersFile ".git/allowed_signers"
printf '%s %s\n' "<Adresse des Taggers>" "$(cat ~/.ssh/id_ed25519.pub)" \
  > .git/allowed_signers
```

⚠️ **Die Datei liegt unter `.git/` und wird nicht versioniert** – sie bindet eine Adresse
an einen Schlüssel, und eine Adresse im Kern meldet Prüfung 6 zu Recht. ➡️ *Eine
Signatur ohne hinterlegten Unterzeichner belegt, daß jemand mit diesem Schlüssel
unterschrieben hat – nicht, wem der Schlüssel gehört.*

🔴 **Schritt 1 ist nicht delegierbar, und die Begründung ist D-319.** Die Marke sagt
**wer** freigegeben hat. Ein Werkzeug kann sie technisch setzen und mit einem vorhandenen
Schlüssel sogar signieren – **und genau deshalb darf es nicht.** Dieselbe Trennung gilt für
den Freigabe-Commit.

⚠️ **Die Zeilenenden des Archivs stehen seit D-320 fest.** `git archive` folgt der
`.gitattributes`; ohne sie hinge der Inhalt der Lieferung an der Konfiguration des
Rechners, der sie erzeugt hat.

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
