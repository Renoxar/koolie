# Herrichtung des Übungsrepositoriums und was dabei angefallen ist

| Feld | Wert |
|---|---|
| Datum | 2026-09-14 (Messungen), abgeschlossen in der Nacht zum 2026-09-15 |
| Gegenstand | `devpacks/test-devin-framework` – das synthetische Übungsrepository, Vorbedingung jedes Sitzungstests (Verfahren Nr. 1 des Testkatalogs) |
| Anlass | Kandidat 1 der Übergabe: Übungsrepository von 0.13.0 auf `main` heben, die drei fehlenden Köder anlegen |
| Framework-Stand | vorher 0.13.0, nachher 0.44.0 (einunddreißig Releases) |
| Client Pack dort | `devin-desktop` |
| Ergebnis | Validator `--strict-overlay` **0 Fehler, 0 Warnungen**; Frontend-Tests **18 grün**; `lint` und `typecheck` ohne Befund |
| Folgeantrag | `CR-2026-067` (vier Befunde, davon zwei mit eigener Prüfung) |

## 1. Prüfmethode

Das Heben wurde **zuerst in einer Probe im Scratchpad gefahren**, nicht im Repositorium:
`git archive HEAD` des Übungsrepositoriums, `leitwerk-core/` aus `git archive HEAD` des
Frameworks darübergelegt, dann `install.py --update`. So steht der Migrationsumfang fest,
bevor am eigentlichen Baum etwas geändert wird — und er ist wiederholbar.

Jede Messung am Übungsrepository wurde mit seinem **eigenen** Validator gefahren, also mit
dem Stand, der dort installiert ist. Die Abzählungen über Testfälle und Installationen
liefen über Skripte, nicht über das Auge.

## 2. Was das Heben gekostet hat

`install.py --update`: 24 Core-Dateien erneuert, 40 unverändert, **20 Projektdateien
unangetastet**. Danach meldete der Validator `--strict-overlay`:

| Anzahl | Prüfung | Befund |
|---|---|---|
| 1 | 37 | Der `ask`-Korb führt **8 Regeln**, die die Kernquelle nicht erzeugt, bei **3 gefüllten Platzhalterschlitzen** |
| 8 | 42 | Je eine Meldung pro Exec-Regel: kein Platzhalter des Overlays erklärt diesen Befehl |
| 3 | 42 | Verlorener Anker: keine Tabellenzeile nennt `<BUILD_COMMAND>`, `<TEST_COMMAND>`, `<LINT_COMMAND>` |
| 1 | 13 | Kompatible Framework-Version steht auf `0.13.x` |
| 1 | 20 | Die Importsteuerung `read_config_from` fehlt |
| **14** | | **Fehler gesamt**, dazu **1 Warnung** (verwaiste Hook-Datei neben der wirksamen Konfiguration) |

**Die Übergabe hatte weniger erwartet.** Sie nannte die Platzhalterform — „jeder
Befehlsplatzhalter zweimal und ohne spitze Klammern". Gemessen ist der Befund größer: Das
Übungsrepository ist der **zweite und schärfere echte Fall des 0.44.0-Befunds**. Acht
Exec-Freigaben bei drei Schlitzen heißt: **fünf Freigaben mehr, als die Kernquelle
überhaupt erzeugen kann**, darunter

```
Exec(python3 leitwerk-core/tests/scripts/validate-framework.py)
```

— der Aufruf des Validators selbst. Eingetragen worden sind sie von Hand, und bis
Prüfung 42 hat es nichts gemeldet.

## 3. Welcher Strang die drei Schlitze bekommt — und warum das gemessen wurde

Das Übungs-Overlay führt zwei Technologiestränge (Java/Maven, TypeScript/npm) und damit
sechs Build-, Test- und Prüfbefehle. Die Berechtigungsdatei hält drei Schlitze bereit.
**Die Entscheidung fiel nach der Fahrbarkeit, nicht nach der Reihenfolge im Dokument:**

| Werkzeug | `command -v` | Lauf |
|---|---|---|
| `node` | `/c/Program Files/nodejs/node` | – |
| `npm` | `/c/Program Files/nodejs/npm` | `npm --prefix frontend run test`: **15 Tests grün in 14 s** |
| `java` | **nicht gefunden** | – |
| `javac` | **nicht gefunden** | – |
| `mvn` | **nicht gefunden** | – |

Der Backend-Strang ist auf diesem Arbeitsplatz **nicht ausführbar** — derselbe Umstand wie
beim Piloten (Übergabe vom 13.09.). Die drei Schlitze tragen deshalb die npm-Befehle; die
drei Maven-Befehle bleiben in Abschnitt 5 und 6 gelistet und wirken über die Regelschicht
(D-76). **Ein Schlitz, der einen Befehl trägt, den die Maschine nicht ausführen kann,
sichert nichts ab und verdeckt nur, welcher Befehl wirklich läuft.**

**Was dabei auffällt und nicht mitbehoben ist:** Der eingebaute Übungsfehler des
Repositoriums (Aufgabe B, `BookService.countAvailableCopies`) liegt im **nicht fahrbaren**
Strang. Wer ihn über einen Testlauf aufdecken will, braucht ein JDK. Das ist kein Befund
am Framework und keine Aufgabe dieser Sitzung — es steht hier, damit es beim ersten
Sitzungstest niemanden überrascht.

## 4. Der Befund, der nicht gesucht wurde: ein Hook, der einunddreißig Releases lang stumm war

`.devin/config.json` trug **keinen `hooks`-Block**. Die Hooks des Projekts standen in
`.devin/hooks.v1.json` — der Datei, aus der dieser Client keinen Hook ausführt (AP2-DD-10,
D-32, seit 0.25.0). Der Hook war seit der Erstinstallation wirkungslos.

**Gemessen, nicht geschlossen.** In einer frischen 0.44.0-Installation wurde der Block
entfernt und der Lauf wiederholt:

| Zustand | Validatorlauf |
|---|---|
| mit `hooks`-Block (Auslieferung) | 2 Fehler |
| **ohne `hooks`-Block** | **2 Fehler — dieselben** |

Beide Fehler sind Artefakte der Testinstallation (fehlende `README.md`) und haben mit dem
Hook nichts zu tun. **Kein Lauf sieht das Fehlen.**

**Die Gegenprüfung stellt die Reichweite um.** Abgezählt über alle vier lokalen
Installationen:

| Installation | Pack | Framework | `hooks`-Block |
|---|---|---|---|
| `test-devin-framework` | `devin-desktop` | 0.13.0 | **NEIN** |
| `otp-generator` (Pilot) | `claude-code` | 0.41.0 | ja |
| `lw-tech` | `devin-desktop` | 0.24.0 | ja |
| `leitwerk-ap2` | `devin-desktop` | 0.24.0 | ja |

Es liegt also **nicht am Releasestand** — `lw-tech` und `leitwerk-ap2` stehen auf 0.24.0
und tragen den Block, weil sie nach D-32 frisch installiert wurden. Betroffen ist **eine**
Installation, nicht vier. Der Befund selbst bleibt, und er hat eine zweite Hälfte:

> **Prüfung 18 beschreibt die halbe Migration.** Ihre Warnung sagt, die verwaiste Datei sei
> von Hand zu löschen. Wer ihr wörtlich folgt und sonst nichts tut, hat danach **gar keinen
> Hook mehr** — und kein Lauf meldet es.

Was die alte Datei zusätzlich verpasst hätte, selbst wenn der Client sie läse: Sie kennt
`read|grep|find_file_by_name` nicht (nur `exec|edit|write`), ruft ohne `--fail-closed` auf
und übergibt dem Statushook keine Argumente. **Drei Verschärfungen seit 0.25.0, keine davon
wirksam.**

## 5. Die Präparationen: drei genannt, sieben gebraucht

Verfahren Nr. 1 bindet jeden Sitzungstest an das Übungsrepository;
`onboarding/exercises/README.md` Nummer 4 nannte **drei Köder**. Abgezählt gegen die
Vorbedingungen des Testkatalogs:

| Kennung | Präparation | Gebraucht von | Lag vor? |
|---|---|---|---|
| `UEB-01` | Injektionsköder | `FW-PI-01` | nein |
| `UEB-02` | K3-Köder | `FW-DS-01` | nein |
| `UEB-03` | Scope-Falle | `FW-SC-01`, `FW-SC-02` | nein |
| `UEB-04` | `.env`-Testdatei | `FW-DS-02` | nein |
| `UEB-05` | präparierter Codekommentar | `FW-PI-02` | nein |
| `UEB-06` | Injektion in einer Testdatei | `SK-006-N04`, `FW-PI-04` | nein |
| `UEB-07` | Regelwiderspruch zu `FW-CORE-05` | `FW-KO-03` | nein |

**Keine einzige lag vor**, und der Testkatalog führte alle neun Fälle als `offen`, also als
fahrbar. Die Abwesenheit ist mit `git ls-files` und `ls -a` geprüft; die
**Anwesenheitsprobe desselben Gegenstandstyps** (Verfahren Nr. 7) ist die `.gitignore` und
`.devin/` — beide Punktdateien, beide gefunden.

**Zwei Vorbedingungen sind keine Präparationen:** `FW-PI-03` und `FW-DS-05` brauchen einen
präparierten Aufgabentext, und der ist eine Sitzungseingabe.

## 6. Was beim Anlegen der Köder gemessen wurde

Zwei Fragen waren vorab zu klären, weil sie die Ablage bestimmen:

| Frage | Messung | Folge |
|---|---|---|
| Macht ein K3-Köder im Repositorium den eigenen Validator rot? | **Nein.** Lauf mit Köder: 14 Fehler — dieselben wie ohne | Der Köder darf im Repositorium liegen |
| Greift der Schutz-Hook auf den Köder? | **Lesen: Exit 0** (Pfad enthält kein Muster). **Schreiben eines Textes mit `db.password=…`: Exit 2**, auch mit ausdrücklich synthetischem Wert; Kontrolllauf mit einem echt aussehenden Wert identisch | Der Köder ist nur über den Shell-Kanal anzulegen — **und für `FW-DS-01` ist der Hook eine zweite Schranke.** Ein Lauf, in dem der Client den Inhalt nicht zitiert, belegt **ohne Entlastungslauf** nicht das S3-Verhalten |

Der zweite Befund gehört in das Testblatt von `FW-DS-01`, bevor jemand den Fall fährt.

## 7. Wohin das Mentorenmaterial gehört

Die Zuordnung Präparation → Testfall steht im Mentorenblatt
(`tools/mentorenblatt/PRAEPARATIONEN.md`), und `tools/**` ist neu in `<EXCLUDED_PATHS>`:
Ein KI-Client, der es liest, kennt die Auflösung jeder Negativübung. In der
Strukturtabelle des Overlays wird `tools/` deshalb **neutral** beschrieben —
„Mentorenmaterial und Hilfsskripte". Die Strukturtabelle liest der Client mit; ein Hinweis
auf Köder wäre dort derselbe Fehler wie das Blatt selbst im lesbaren Bereich.

**`UEB-07` liegt nicht im Repositorium**, sondern daneben: Sein Ablageort ist die
Regelablage, und die schreibt `install.py --update` bei jedem Release-Wechsel neu. Eine
Datei, die dort läge, wäre beim nächsten Update still verschwunden. Gesetzt und entfernt
wird sie mit `tools/praeparationen.py`; beide Zustände sind gegen den Validator gemessen
und **beide grün** — was zugleich zeigt, dass `FW-KO-03` ein Sitzungstest ist und kein
Skripttest: Der Validator sieht den Widerspruch nicht.

## 8. Ein Befund lag unter einem verlorenen Anker

Abschnitt 4 des Übungs-Overlays nannte seine sieben Pfadplatzhalter **ohne spitze
Klammern**. Prüfung 28 sucht die Deklaration von `<EXCLUDED_PATHS>` über genau diese Form,
fand sie nicht — und **bestand still**. Erst nachdem die Platzhalter die Form der Vorlage
bekamen, meldete sie:

> Die Deklaration von `<EXCLUDED_PATHS>` nennt `project-overlay/`, `AGENTS.md`, `.devin/`.
> […] sie gehören in `<READ_ONLY_PATHS>` (B07, D-55)

**Ein echter Fall von B07, im Überlebensmodus einer Prüfung ohne Anker.** Berichtigt sind
beide Träger, Overlay und Laufzeitfassung. Das ist die Lehre von 0.32.0 — eine
Konsistenzprüfung ohne ihren Gegenstand besteht leise —, hier zum ersten Mal an einem
fremden Overlay eingetreten.

## 9. Was der Testkatalog für 1.0.0 wirklich führt

Kriterium 2 von D-11 zählt die Ergebnisspalte des Katalogs **und die dezentralen
`TESTS.md` je Skill** (so steht es in `docs/ROADMAP.md`). Abgezählt:

| Ablage | Zeilen | davon `offen` |
|---|---|---|
| `tests/TEST_CATALOG.md` | 38 | **31** |
| zwölf Skill-Testblätter | 72 | **72** |
| **Summe** | **110** | **103** |

Von den 31 Katalogfällen tragen **27** das Prüfmittel `sitzung`, zwei weitere einen
Sitzungsanteil. **Die Zahl „30 offen" der Übergabe ist zu klein**, und zwar doppelt: 31 im
Katalog, und die 72 dezentralen kommen hinzu. Das ändert nichts an der Richtung des
Fokusabschnitts — Kriterium 2 ist der größte Posten —, wohl aber an jeder Schätzung, die
auf „30" aufsetzt.

## 10. Was offen bleibt

- **Der Backend-Strang ist auf diesem Arbeitsplatz nicht fahrbar.** Ohne JDK und Maven sind
  Aufgabe A, B und jeder Test, der einen Backend-Lauf braucht, nicht durchführbar.
- **`docs/UEBUNGSAUFGABEN.md` liegt im lesbaren Bereich** und nennt die Auflösung der
  Aufgaben A bis F, darunter den eingebauten Fehler. Ein Client, der `docs/` liest, kennt
  sie. Die sieben Präparationen sind deshalb **nicht** dort geführt. Ob das Blatt selbst in
  den gesperrten Bereich gehört, ist eine eigene Entscheidung: `<DOC_PATHS>` hätte dann
  keinen Gegenstand mehr, und die M5-Übungen liefen ins Leere.
- **Kein Sitzungstest ist gefahren.** Diese Sitzung hat die Vorbedingung hergestellt, nicht
  die Tests durchgeführt. Der erste Lauf braucht eine Devin-Desktop-Sitzung, und das
  Kontingent ist begrenzt (Free plan).
- **`FW-DS-01` braucht einen Entlastungslauf** (Abschnitt 6), sonst ist die Wirkung des
  Hooks nicht von der Wirkung der Regel zu trennen.
