# Änderungsantrag `CR-2026-106`

| Feld | Inhalt |
|---|---|
| Titel | Die Übergabe wird eingecheckt – und das Framework hält seine eigene Datenschutzregel zum ersten Mal an sich selbst ein |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-20 |
| Betroffene Artefakte | `UEBERGABE.md` (**neu**, Wurzel), `UEBERGABE.local.md.example` (**neu**), `.gitignore`, `tests/scripts/validate-framework.py` (Lesebereich, **D-215**), `tests/scripts/probe-pruefungen.py` (Sonde und Gegenprobe **6i**), `governance/DECISION_LOG.md` (**D-214**, **D-215** neu), `CHANGELOG.md`, `VERSION` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand ist ein Wurzeldokument des Repositoriums |
| Art | Strukturänderung, **kein Kontingent, kein Modelllauf, keine Messung** |
| Dringlichkeit | Regulär, ohne Frist |

## 1. Anlass

**Die Übergabe lag außerhalb des Repositoriums** (`devpacks/leitwerk-UEBERGABE.md`) und
war bewußt nicht versioniert. Zwei Nachteile, beide praktisch:

1. **Von einem anderen Arbeitsplatz aus gibt es keine Übergabe.** Wer das Repositorium
   klont, bekommt den Kern, den Testkatalog und das Decision Log – aber nicht das
   Arbeitswissen, das für die Weiterarbeit nötig ist.
2. **Alte Stände müssen von Hand gesichert werden.** Beim Einchecken übernimmt die
   Git-Historie das.

## 2. 🔴 Was die Prüfung ergeben hat – und warum die Datei so nicht einscheckbar war

**Gemessen, nicht angenommen:** Eine Probekopie in der Wurzel, dann der Validator.

| | Fundstelle | Befund |
|---|---|---|
| zweimal | die Adresse des Git-Servers | 🔴 `FW-CONTENT-IP` |
| `UEBERGABE.md:1257` | eine URL, die das Token vor dem Hostnamen traegt | 🔴 **`FW-CONTENT-SECRET`: Verbindungszeichenfolge mit Anmeldedaten** |
| dreimal | `claude.ai`, Gitea-URL | 🟡 `FW-CONTENT-URL` außerhalb der Allowlist |

**Ergebnis: 3 Fehler, 3 Warnungen.** Dazu, ohne Validatorbefund, **vier Fundstellen des
Benutzernamens** in Arbeitsplatzpfaden – ein Personenbezug.

🔴 **Der Befund hinter dem Befund:** Das Framework verlangt von **jedem** Overlay
*„Keine Secrets, keine Personen, keine internen Adressen. Rollen statt Personen"*
(`overlay-manifest.yaml`, Kopf) und setzt es mit vier Prüfungen durch. **Seine eigene
Übergabe hielt die Regel nicht ein** – sie konnte es nicht, weil sie nie geprüft wurde.
*Eine Regel, die für den eigenen Bestand nicht gilt, ist eine Zusage an andere.*

🔴 **Und die eigene Vorabmessung war zu klein.** Sie suchte nach Zugangsdaten in der
Form `token=…` und meldete **null**; der Validator fand die **URL-Form**
eine URL, die das Token vor dem Hostnamen traegt. ➡️ **Wer prüft, ob ein Text ein Secret trägt, nimmt die
Prüfung, die es später meldet – nicht eine eigene.** Dieselbe Bauform wie *die Sonde,
die einen Dateinamen rät* (Abschnitt 6), an einem Mustersatz.

## 3. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Wird die Übergabe eingecheckt?** | **Ja**, bereinigt, als `UEBERGABE.md` in der Wurzel | 🔴 **Der Preis ist die Bereinigung**, und sie ist kein Formfehler: Servername, Konto und Arbeitsplatzpfade **müssen** heraus, sonst scheitert der Validator und mit ihm jede Abnahme. **Der Gegenwert:** Das Arbeitswissen ist von jedem Arbeitsplatz lesbar, die Historie ersetzt die Handsicherungen – und die Datenschutzregel des Frameworks gilt zum ersten Mal auch für das Framework |
| **E2** | **Wohin mit den konkreten Werten?** | **In `UEBERGABE.local.md`**, nicht versioniert, mit einer eingecheckten Vorlage `UEBERGABE.local.md.example` | 🟢 **Die Konvention gibt es schon:** `.gitignore` führt `AGENTS.local.md` und `.devin/config.local.json` als *„Persönliche, nicht zu teilende Konfiguration (Framework-Konvention)"*. Der Eintrag reiht sich ein, statt eine zweite Konvention aufzumachen. **Verworfen: die Werte ersatzlos streichen** – *wie komme ich an das Gitea* ist das erste, was ein fremder Arbeitsplatz braucht |
| **E3** | **Wohin im Repositorium?** | **Repo-Wurzel**, neben `README.md` und `AGENTS.md` | 🔴 **Nicht unter `leitwerk-core/`**, und der Grund ist mechanisch: Das Heben eines Projekts ersetzt **das ganze Verzeichnis** (`rm -rf leitwerk-core` + `git archive HEAD leitwerk-core`). Eine Übergabe dort läge danach im Piloten und im Übungsrepositorium, wo sie nichts zu suchen hat. **Verworfen: ein neues `docs/` in der Wurzel** – ein Verzeichnis für eine Datei ist Aufbau ohne Gegenstand |
| **E4** | **Welcher Name?** | **`UEBERGABE.md`**, groß geschrieben | Alle Wurzeldokumente des Repositoriums sind groß: `README.md`, `AGENTS.md`, `CHANGELOG.md`, `VERSION`, `OWNERS.md`. **Ein kleingeschriebenes `uebergabe.md` wäre der einzige Ausreißer** – und die Beilage heißt dann folgerichtig `UEBERGABE.local.md`, wie `AGENTS.local.md` |
| **E5** | **Werden neue Platzhalter fuer Servername und Arbeitsbereich eingeführt?** | **Nein.** Prosa mit Verweis auf die Beilage | 🔴 **Gemessen:** Der Validator meldet jeden Platzhalter, der nicht in `docs/PLACEHOLDER_REGISTRY.md` steht – **je eine Warnung**, und die Abnahme verlangt null. Ein Platzhalter für eine Angabe, die es nur auf einem Arbeitsplatz gibt, gehört nicht ins Register des Frameworks. **Preis: der Text nennt den Wert nicht, sondern seinen Ort** |
| **E6** | **Was wird aus `devpacks/leitwerk-UEBERGABE.md`?** | **Sie entfällt**; das Archiv bleibt daneben liegen | Zwei Fassungen derselben Datei driften – *zwei Listen für denselben Gegenstand driften, und zwar schnell* (Abschnitt 6). **Das Archiv bleibt außerhalb**, weil es 3378 Zeilen Chronik trägt, die niemand im Repositorium braucht und die dieselbe Bereinigung erfordern würden |

## 4. Entscheidung

**E1 bis E6 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-20). Decision
Records **D-214** und **D-215**. Kriterium 2 unverändert **38** – keine Zelle berührt, kein Lauf
gefahren.

## 5. Abnahme

- `validate-framework.py --root .`: **0 Fehler, 0 Warnungen** – gemessen **nach** der
  Bereinigung, gegen die Datei an ihrem endgültigen Ort.
- `probe-pruefungen.py` in **beiden** Kodierungsumgebungen (D-49): **342 Einheiten,
  keine ohne `OK`** (340 bisherige plus Sonde und Gegenprobe **6i**).
- **Sonde 6i und Gegenprobe 6i** belegen den Zuschnitt als **Paar** (D-23): Die Sonde
  zeigt, dass eine **nicht** gefuehrte Datei mit derselben IP-Adresse weiter gemeldet
  wird; die Gegenprobe, dass die gefuehrte uebersprungen wird. Ohne die erste belegte
  die zweite nur, dass der Validator schweigt.

🔴 **Der erste Abnahmelauf ist gefallen, und der Grund gehoert ins Protokoll:**
Fuenf Einheiten meldeten `[Praeparation gebrochen]` - **das `Edit`-Werkzeug hatte
`validate-framework.py` von CRLF auf LF umgestellt**, alle 7240 Zeilen, und die
Praeparation von Pruefung 40 splittet nach `
`. Das Arbeitswissen fuehrt die Regel
fuer das `Write`-Werkzeug (*Dateien aus dem `Write`-Werkzeug sind LF und muessen nach
dem Anlegen umgestellt werden*); **sie gilt fuer `Edit` genauso, und das stand dort
nicht.** 🟢 **Die Sonden haben es laut gemeldet, nicht leise bestanden.**
- **Der Gegenbeweis, der zählt:** Vor der Bereinigung meldete derselbe Validator gegen
  dieselbe Datei **3 Fehler und 3 Warnungen**. Das belegt, daß die Prüfung ihren
  Gegenstand trifft – und nicht bloß schweigt.

## 6. Migrationshinweis

**Keiner.** Die neuen Dateien liegen in der Wurzel; `install.py` schreibt dort nichts
und kopiert von dort nichts. Übernehmende Projekte sind nicht betroffen.
