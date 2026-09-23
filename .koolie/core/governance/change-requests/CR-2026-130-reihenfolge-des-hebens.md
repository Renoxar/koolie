# Änderungsantrag `CR-2026-130`

| Feld | Inhalt |
|---|---|
| Titel | Die Reihenfolge des Hebens – ein Prüfpunkt, den sein eigenes Verfahren hinter seinen Zeitpunkt legt |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-23 |
| Betroffene Artefakte | `.koolie/core/governance/RELEASE_PROCESS.md` (Abschnitt 4.1); `.koolie/core/checklists/11-framework-release.md` (Prüfpunkt 20); `.koolie/core/governance/ADOPTION_REGISTRY.md`; `.koolie/core/tests/scripts/validate-framework.py` (**Prüfung 82**); `.koolie/core/tests/scripts/probe-pruefungen.py`; `.koolie/core/governance/DECISION_LOG.md` (**D-329** bis **D-332**, `K-110`); `.koolie/core/VERSION`; `.koolie/core/CHANGELOG.md`; `.koolie/core/docs/ROADMAP.md`; `.koolie/core/build/doc/00-kopf.md`, `26-qs-test.md`; `UEBERGABE.md` |
| Ebene laut Entscheidungsbaum 6 | Governance |
| Art | **Änderung.** MINOR-Release nach `RELEASE_PROCESS.md` Abschnitt 1 – Prüfung 82 ist eine neue Regel, keine Formulierung |
| Dringlichkeit | regulär – der Schuldposten ist aus `1.0.1` übernommen und steht seit zwei Releases |
| Status | 🟢 **entschieden am 2026-09-23** (E1 bis E5) |

---

## 1. Anlass

**Die Bestandsliste der übernehmenden Projekte war in zwei aufeinanderfolgenden Releases
falsch, und beide Male aus demselben Grund.**

`1.0.0` hat sie angelegt (D-322), und ihr erster Eintrag war zugleich ihr erster Befund:
Beide übernehmenden Projekte standen **drei Releases** hinter `main`, während Kriterium 5
von D-11 als erfüllt geführt wurde. `1.0.1` hat es wiederholt – die Liste stand einen
halben Tag auf `1.0.0`, während die Projekte `1.0.1` trugen.

Die Übergabe zu `1.0.1` hat die Ursache richtig benannt:

> *„Sie wurden NACH dem Merge gehoben statt davor, und damit war `FW-CL-11` Prüfpunkt 20
> zum Merge-Zeitpunkt nicht erfüllt."*

**Und sie hat die Frage ausdrücklich offen gelassen:** *„Zu prüfen: Gehört das Heben vor
den Release-Commit, und muß Abschnitt 4.1 die Reihenfolge nennen?"*

## 2. Der gemessene Bestand – der Befund ist größer als der Schuldposten

Prüfpunkt 20 von `FW-CL-11` lautet:

> *„**MUSS** Release-Archiv erzeugt und abgelegt; übernehmende Projekte informiert
> (Migrationshinweise, betroffene Overlay-Felder)."*

**Das ist EIN Haken über ZWEI Gegenständen** – und ihre frühesten möglichen Zeitpunkte
liegen auf **entgegengesetzten Seiten** des Release-Commits:

| Hälfte von Prüfpunkt 20 | frühestens möglich | warum |
|---|---|---|
| *„Release-Archiv erzeugt und abgelegt"* | **nach** dem Commit | Abschnitt 4.1 Schritt 2 baut das Archiv **aus der Marke**, und Schritt 1 setzt die Marke **auf** den Release-Commit |
| *„übernehmende Projekte informiert"* | **vor** dem Commit | `install.py --update` läuft gegen den Arbeitsbaum, und der trägt die neue `VERSION` bereits |

➡️ ***Ein Prüfpunkt, dessen eigenes Verfahren seine Erfüllung hinter den Zeitpunkt legt,
an dem er abgehakt wird, ist nicht unerfüllt – er ist falsch geschnitten.***

🔴 **Die Checkliste wird VOR dem Release durchgegangen.** Ihre eigene Kopfzeile sagt es:
*„Wann: vor jedem Framework-Release (auch Patch-Releases)."* Die erste Hälfte von
Prüfpunkt 20 konnte zu diesem Zeitpunkt **noch nie** erfüllt sein – auch nicht in `1.0.0`,
dem Release, das das Archivverfahren eingeführt hat.

## 3. Das Heben ist ein Prüfmittel, nicht eine Fortschreibung

**Die Empirie der beiden Releases zeigt in eine Richtung, und sie zeigt mehr als die
Reihenfolge.**

| Release | wann gehoben | was dabei herauskam |
|---|---|---|
| `1.0.0` | **vor** dem Abschluß | 🔴 **B13 und B14** – Prüfung 78 und 79 aus `0.90.0` waren in **jeder** Installation rot. **Gefunden hat sie kein Validatorlauf, sondern das Heben** |
| `1.0.1` | **nach** dem Merge | 🔴 Die Bestandsliste stand einen halben Tag falsch |

➡️ ***Das Heben ist nicht die Fortschreibung einer Liste, es ist ein Lauf gegen eine
fremde Installation*** – und D-326 sagt es bereits, nur an der Prüfung und nicht am
Release:

> *„Jede neue Prüfung läuft einmal gegen ein übernehmendes Projekt, bevor sie als fertig
> gilt – `--strict-overlay` ist billiger als der nächste Meßtag."*

🔴 **Genau diese Lehre stand in der Übergabe und nicht im Ablauf, und ihre Halbwertszeit
war ein Release** (D-326). Dasselbe würde einem Satz in Abschnitt 4.1 widerfahren, der
ohne Prüfung dasteht.

## 4. Und die Liste war an ZWEI Stellen falsch, nicht an einer

🔴 **Gemessen am 2026-09-23, im Vorbedingungsdurchgang dieses Releases, vor dem ersten
Handgriff:**

| Ort | `VERSION` | Spalte `Framework-Version` der Bestandsliste |
|---|---|---|
| Framework-Repositorium | `1.0.1` | `1.0.1` ✅ – mit `1.0.1` nachgezogen |
| `devpacks/test-devin-framework` | `1.0.1` | 🔴 **`1.0.0`** |
| `devpacks/otp-generator` | `1.0.1` | 🔴 **`1.0.0`** |

**`1.0.1` hat die Liste an einer Stelle berichtigt und sie an zwei ausgeliefert.** Die
Berichtigung fiel **nach** dem Heben, und damit erreichte sie die Kopien nicht mehr.

➡️ ***Wer eine Liste nach dem Heben fortschreibt, schreibt sie an einer Stelle fort und
liefert sie an zwei.***

🟢 **Das ist zugleich der gemessene Beleg dafür, daß ein Verfahrensschritt allein hier
nicht getragen hätte** – er stünde im Framework und wäre in beiden Installationen
unbelegt.

---

## 5. Vorlage zur Entscheidung

### E1 – Gehört das Heben der übernehmenden Projekte vor den Release-Commit?

| | |
|---|---|
| **Auflösung** | 🟢 **Ja.** Abschnitt 4.1 bekommt das Heben als **Schritt 1**, ausdrücklich vor dem Freigabe-Commit; die bisherigen Schritte rücken nach |
| **Preis, benannt** | ⚠️ Wer vor dem Commit hebt, hebt aus einem **unveröffentlichten** Stand. Ändert sich der Baum danach noch – und in `1.0.0` hat er sich **genau deswegen** geändert –, muß **erneut** gehoben werden. ➡️ ***Heben und Commit gehören als Paar***, wie Commit und Marke (D-321, Falle 4 aus `1.0.0`) |
| **Verworfen** | **Nach dem Merge heben** – der Stand von heute. Zweimal in zwei Releases gemessen, zweimal mit derselben Folge |
| **Verworfen** | **Die Liste ohne Versionsangabe führen.** Dann veraltet sie nicht – und beantwortet die Frage nicht mehr, für die sie angelegt wurde (D-322) |

### E2 – Wird Prüfpunkt 20 geteilt?

| | |
|---|---|
| **Auflösung** | 🟢 **Ja, in zwei Prüfpunkte.** Einer vor dem Commit (*Projekte gehoben, Bestandsliste fortgeschrieben*), einer danach (*Archiv erzeugt, nachgezählt und abgelegt*) |
| **Preis, benannt** | ⚠️ Ein Haken mehr in einer Checkliste, die bereits 24 führt |
| **Verworfen** | **Den Haken lassen und die Reihenfolge nur in 4.1 nennen.** Dann bleibt ein Prüfpunkt, der zum Zeitpunkt des Abhakens nicht erfüllbar ist – und das ist die Bauform *die Regel mit leerer Schnittmenge* (D-189, `K-72`), hier an einem Prüfpunkt |

### E3 – Bekommt die Reihenfolge eine Prüfung, oder bleibt sie ein Verfahrensschritt?

| | |
|---|---|
| **Auflösung** | 🟢 **Prüfung 82.** Jede Zeile der Bestandsliste nennt in der Spalte `Framework-Version` den Inhalt von `.koolie/core/VERSION`; Abweichung ist ein **Fehler** |
| **D-299-Probe** | 🟢 **Geführt und bestanden.** In einem übernehmenden Projekt sind Liste und `VERSION` **byte-gleich aus demselben Release** ausgeliefert und tragen deshalb denselben Wert – auch dann, wenn das Projekt mehrere Releases zurückliegt. Die Prüfung ist dort grün, **und sie braucht dafür keine Ausnahme** |
| **Grenze, benannt** | 🔴 **Sie mißt die Behauptung, nicht die Tatsache.** Wer die Zeile ändert, ohne zu heben, kommt durch. Dieselbe Bauform wie Prüfung 77, die die **Version** des Hauptdokuments mißt und nicht seinen **Inhalt** (D-312) |
| **Preis, benannt** | ⚠️ **Jedes Release faßt diese Tabelle an** – derselbe Preis wie bei Prüfung 67 und 77 |
| **Verworfen** | **Die Liste gegen die Projekte halten.** Sie liegen außerhalb des Repositoriums; eine Prüfung, die sie sucht, wäre auf jedem anderen Arbeitsplatz rot (D-299) |
| **Verworfen** | **Nur ein Verfahrensschritt.** D-326 hat gemessen, was eine Lehre ohne Prüfung wert ist: ein Release |

### E4 – Gilt das Heben auch bei einem Release, das kein ausgeliefertes Artefakt berührt?

| | |
|---|---|
| **Auflösung** | 🟢 **Ja, ausnahmslos** |
| **Begründung** | Eine Ausnahme *„nur wenn ein ausgeliefertes Artefakt berührt ist"* verlangt eine **Einstufung**, und keine Prüfung kann sie nachrechnen. 🔴 **`1.0.1` wäre genau der Fall gewesen, in dem sie falsch entschieden hätte:** Es galt als Patch-Release *„ohne neue Prüfung"* – und es änderte `RELEASE_PROCESS.md`, einen Träger, der ausgeliefert **und** in das Hauptdokument eingebettet ist |
| **Preis, benannt** | ⚠️ `install.py --update` je Projekt bei jedem Release, auch bei reiner Prosa. Gemessen ist das ein Zehn-Minuten-Vorgang je Projekt |
| **Verworfen** | **Eine Ausnahme für reine Chronikreleases.** Sie wäre billig und ungeprüft – die Bauform *die Ausnahme mit leerem Geltungsbereich* (0.57.1) mit umgekehrtem Vorzeichen |

### E5 – Was wird aus der Word-Fassung, die auf `v1.0.0` stehengeblieben ist?

| | |
|---|---|
| **Anlaß** | 🔴 Gemessen im Vorbedingungsdurchgang: `build/out/` führt `Koolie_v1.0.0_claude-code.docx` und `Koolie_v1.0.0_devin-desktop.docx` – **keine Fassung `v1.0.1`**. `1.0.1` hat den Dokumentkopf auf `1.0.1` gehoben und `RELEASE_PROCESS.md` geändert, einen Träger, den `25-governance.md` einbettet |
| **Auflösung** | 🟢 Abschnitt 4.1 nennt den **Bau der Erzeugnisse** als eigenen Schritt. Er steht dort bereits als Ablage-Hinweis (*„wer sie mitliefern will, legt sie neben das Archiv"*) – **nicht aber, daß sie gebaut werden** |
| **Grenze, benannt** | ⚠️ **Wieder ein Verfahrensschritt statt einer Prüfung, und damit schwächer.** Die Erzeugnisse liegen unter `build/out/` und stehen in der `.gitignore`; **keine der 82 Prüfungen erreicht sie.** Dieselbe benannte Lage wie beim Archiv (D-328) und beim Foliensatz (`K-105`) |
| **Fortführung** | 🆕 **`K-110`** – ob eine Prüfung die Erzeugnisse der Lieferung überhaupt erreichen kann |
| **Verworfen** | **Die Erzeugnisse versionieren.** Zwei Träger von je 2 MB je Release; die `.gitignore` steht seit `0.97`-Zeiten aus gutem Grund |

### E6 – Welcher Commit ist nicht delegierbar, und woran erkennt man ihn?

| | |
|---|---|
| **Anlaß** | 🔴 **Eine Rückfrage des Owners, und sie hat einen Befund ausgelöst.** Die Übergabe zu `1.0.0` führt *„Nicht delegierbar, ab jetzt bei JEDEM Release: der Freigabe-Commit und die signierte Marke (D-319, D-321)"*, und `RELEASE_PROCESS.md` 4.1 sagt *„Dieselbe Trennung gilt für den Freigabe-Commit"*. **Gemessen an den beiden Entscheidungen, die sie zitieren, geht die Auflage über beide hinaus** |
| **Der Bestand** | **D-319:** *„Die Gegenzeichnungspflicht gilt nur für die **Abnahmeprotokolle des Testkatalogs** … Die Zeile sagt, WAS gegengezeichnet wurde – die Unterschrift ist der Commit."* Gegenstand ist eine **Gegenzeichnung**, kein Release-Commit. **D-321:** *„…und das **Tag** setzt der Mensch."* Der Commit steht dort nicht. ➡️ *Der Satz in 4.1 ist eine Folgerung ohne eigenen gemessenen Gegenstand* |
| **Und er hatte keinen Anwendungsfall** | 🔴 Eine **dokumentierte Freigabe** gibt es in diesem Repositorium **genau einmal** – im Freigabeprotokoll zu `1.0.0`, Abschnitt 7.1. **`1.0.1` hat keine**, und sein Release-Commit ist ein gewöhnlicher. Bis `0.91.0` hat das Werkzeug alle Release-Commits gesetzt, und D-319 hält das selbst fest |
| **Auflösung** | 🟢 **Ein Commit ist genau dann nicht delegierbar, wenn er eine Unterschrift TRÄGT** – eine Gegenzeichnung nach D-319 oder eine Freigabezeile nach `FW-CL-11`. **Ein Release-Commit ohne solchen Inhalt trägt keine**, und ein Werkzeug, das ihn setzt, fälscht nichts. 🔴 **Die signierte Marke bleibt beim Menschen** – D-321 sagt es wörtlich und ohne Folgerung |
| **Warum das die schärfere Regel ist** | ⚠️ Die pauschale Fassung ist **nicht prüfbar**: *„Freigabe-Commit"* hat keinen erkennbaren Gegenstand, und ein Prüfmittel kann nicht nachsehen, wer eine Tastatur bedient hat. **Die neue Fassung hat einen: den INHALT des Commits.** ➡️ *Eine Auflage, deren Gegenstand niemand benennen kann, wird entweder übererfüllt oder vergessen – beides ist hier eingetreten* |
| **Verworfen** | **Die pauschale Fassung beibehalten.** Sie hätte jeden Release-Commit an eine Handlung gebunden, die bei `1.0.1` gemessen niemand für nötig hielt – *eine Regel, die im Bestand keine Spur hinterläßt, ist keine* |
| **Verworfen** | **Die Trennung ganz aufgeben.** D-319 ist gemessen richtig: Ein Werkzeug, das eine Gegenzeichnung setzt, fälscht sie, und die Fälschung wanderte nur aus der Zeile in die Metadaten |

### E7 – Die dokumentierte Freigabe fehlt in `1.0.1` (V13)

| | |
|---|---|
| **Befund** | 🔴 `FW-CL-11` verlangt *„Freigabe des Releases durch den Framework Owner dokumentiert"* als **MUSS bei jedem Release**. Gemessen: Sie existiert **einmal**, für `1.0.0`. **`1.0.1` hat keine** – derselbe Prüfpunkt, den `1.0.0` beim ersten Anlauf leer gelassen hat (`B16`), ein Release später wieder |
| **Auflösung** | ⚠️ **Gemeldet, nicht geheilt** (`FW-SC-01`). Eine Freigabe für ein vergangenes Release nachzutragen wäre genau die Fälschung, gegen die D-319 argumentiert. 🆕 **`K-111`** führt die Frage weiter: Wo steht die Freigabe eines Releases, das kein eigenes Freigabeprotokoll hat – und was trägt sie, wenn sie nicht in einem Protokoll steht? |
| **Warum keine Prüfung** | ⚠️ Der Gegenstand ist eine **Handlung**, kein Träger. Eine Prüfung könnte das Vorhandensein einer Zeile messen, nicht ihre Wahrheit – dieselbe Grenze wie bei Prüfung 80 und bei Prüfung 82 |

---

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** – E1 bis E7 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Der Schuldposten ist zweimal in zwei Releases aufgetreten, und der Vorbedingungsdurchgang hat ihn an einer **dritten** Stelle gemessen: in den ausgelieferten Kopien. Ein Verfahrensschritt allein hat in diesem Projekt gemessen eine Halbwertszeit von einem Release (D-326) |
| Ziel-Release | `1.1.0` |
| Decision-Log-Eintrag | **D-329** bis **D-334**, `K-110` und `K-111` neu |

⚠️ **Zur Einstufung, und sie ist im Durchgang gefallen.** Der Posten wurde als **PATCH**
vorgelegt – *Korrektur am Verfahren*. Gemessen an Abschnitt 1 trägt das nur ohne E3:
**Prüfung 82 ist eine neue Regel**, keine Formulierung, und ein übernehmendes Projekt
bekommt mit ihr eine neue Fehlermöglichkeit im Validator. ➡️ ***Eine Einstufung gilt so
weit wie ihr Gegenstand*** – der Gegenstand der Vorlage war die Checkliste, nicht der
Prüfapparat. **Das ist D-328 an der eigenen Vorlage**, und es ist die erste Anwendung des
Versionierungsregimes, das `1.0.0` wieder in Kraft gesetzt hat.

## 7. Umsetzung

- [x] `RELEASE_PROCESS.md` Abschnitt 4.1: Heben als Schritt 1, Bau der Erzeugnisse als eigener Schritt, Reihenfolge ausdrücklich (Version `0.2.1` → `0.3.0`)
- [x] `checklists/11-framework-release.md`: Prüfpunkt 20 geteilt (Version `0.3.0` → `0.4.0`)
- [x] `governance/ADOPTION_REGISTRY.md`: offene Frage geschlossen, Verfahren benannt (Version `0.1.1` → `0.2.0`)
- [x] **Prüfung 82** im Validator, mit Registereintrag im Kopfkommentar
- [x] **Sonden 82a bis 82c und Gegenprobe 82a** in `probe-pruefungen.py`
- [x] Decision Log: **D-329** bis **D-332**, `K-110`
- [x] **Beide übernehmenden Projekte gehoben – VOR dem Release-Commit**, als erste Anwendung von D-330
- [x] Validator ohne Fehler; Sondenlauf in **beiden** Kodierungsumgebungen
- [x] Hauptdokument und Word-Fassung für **beide** Client Packs gebaut und im Erzeugnis nachgezählt
- [x] `CHANGELOG.md`, `docs/ROADMAP.md`, `build/doc/00-kopf.md`, `UEBERGABE.md`
