# Änderungsantrag `CR-2026-067`

| Feld | Inhalt |
|---|---|
| Titel | Eine Berechtigungsdatei ohne Hook-Block ist stumm, und das Register der Übungspräparationen nennt drei von sieben |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-15 |
| Betroffene Artefakte | `tests/scripts/validate-framework.py` (Prüfungen 43 und 44 neu, Meldung der Prüfung 18, Register), `tests/scripts/probe-pruefungen.py` (Sonden und Gegenproben, Kopfsatz), `onboarding/exercises/README.md` (Präparationsregister `UEB-01` bis `UEB-07`), `tests/TEST_CATALOG.md` (Vorbedingungen mit Kennung, `FW-PI-04`, `FW-KO-01`), `docs/ADOPTION_GUIDE.md` (mehrere Technologiestränge), `governance/DECISION_LOG.md`, `docs/ROADMAP.md`, `CHANGELOG.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – die Durchsetzungsschicht, ihre Prüfung und der Testkatalog sind Framework-Gut |
| Art | Änderung; Anlass ist **Kandidat 1** der Übergabe – das Übungsrepository herrichten |
| Dringlichkeit | **P1 für Gegenstand 1.** Gemessen war der Hook eines echten Projekts **einunddreißig Releases lang wirkungslos**, und der Validator meldete durchgehend 0 Fehler. Bei `devin-desktop` ist der Hook die einzige technische Secret-Schranke |

## 1. Anlass

Kandidat 1 der Übergabe nannte zwei Aufgaben: das Übungsrepository
(`devpacks/test-devin-framework`) von 0.13.0 auf `main` heben und die **drei** fehlenden
Köder anlegen. Beides ist am 2026-09-14 gemacht; der Weg ist protokolliert
(`tests/protocols/2026-09-15-herrichtung-uebungsrepositorium.md`). **Vier Befunde sind
dabei angefallen, und keiner davon stand in der Kandidatenbeschreibung.**

### Befund 1 – die Berechtigungsdatei ohne Hook-Block ist stumm und läuft grün

Das Übungsrepository trug in `.devin/config.json` **keinen `hooks`-Block**. Seine Hooks
standen in `.devin/hooks.v1.json` – der Datei, aus der dieser Client keinen Hook ausführt
(AP2-DD-10, D-32, seit 0.25.0). Der Hook war damit seit der Erstinstallation wirkungslos.

**Gemessen, nicht geschlossen:** In einer frischen 0.44.0-Installation wurde der
`hooks`-Block entfernt und der Validator gefahren. Ergebnis mit Block: 2 Fehler. Ergebnis
ohne Block: **dieselben 2 Fehler** (beide Artefakte der Testinstallation, kein Bezug zum
Hook). **Kein Lauf sieht das Fehlen.**

Die Gegenprüfung über alle vier lokalen Installationen stellt den Befund **um**: `lw-tech`
und `leitwerk-ap2` stehen auf 0.24.0 und tragen den Block; der Pilot trägt ihn. **Nur das
Übungsrepositorium nicht** – es wurde vor 0.25.0 installiert, und
`install.py --update` schreibt die Berechtigungsdatei nie (`shared_seed`, D-76). Die
Reichweite ist damit **eine** Fundstelle, nicht vier. Der Befund selbst bleibt.

**Und Prüfung 18 beschreibt die halbe Migration.** Ihre Warnung sagt: die verwaiste
`hooks.v1.json` ist von Hand zu löschen. Wer ihr wörtlich folgt und sonst nichts tut, hat
danach **gar keinen Hook mehr** – und kein Lauf meldet es. Das ist derselbe Befundtyp, den
dieses Projekt seit zwölf Releases bei sich selbst findet: eine Anweisung, die weniger
herstellt, als ihr Leser annimmt.

### Befund 2 – das Register der Präparationen nennt drei von sieben

`onboarding/exercises/README.md` Nummer 4 verlangt **drei Köder** (Injektion, K3,
Scope-Falle). Abgezählt gegen die Vorbedingungen des Testkatalogs braucht ein fahrbares
Übungsrepositorium **sieben Präparationen für neun Testfälle**: dazu eine `.env`-Testdatei
(`FW-DS-02`), einen präparierten Codekommentar (`FW-PI-02`), eine Injektion in einer
Testdatei (`SK-006-N04`) und einen Regeltext mit bewusstem Widerspruch (`FW-KO-03`). Keine
dieser vier steht in der Liste, und der Testkatalog führt alle neun Fälle als `offen`,
also als fahrbar.

### Befund 3 – `FW-PI-04` verlangt, was D-76 ausschließt

Die Vorbedingung lautet „Testskript mit präparierter stdout-Anweisung **als freigegebener
Befehl**". Die Berechtigungsdatei hält genau drei Befehlsschlitze bereit, und ein Overlay
kann dort keinen vierten Eintrag erzeugen (D-76, seit 0.39.0; Prüfung 42 seit 0.44.0
meldet jeden unerklärten). **Der Testfall verlangt in dieser Form etwas, das das Framework
seit sechs Releases ausschließt** – und niemand hat es bemerkt, weil ihn niemand gefahren
hat.

### Befund 4 – der Übernahmeleitfaden schweigt zu mehreren Technologiesträngen

Das Übungs-Overlay führt zwei Stränge und damit sechs Build-, Test- und Prüfbefehle. Seine
Berechtigungsdatei trug **acht** Exec-Freigaben bei drei Schlitzen – fünf mehr, als die
Kernquelle erzeugen kann, darunter den Aufruf des Validators selbst. `ADOPTION_GUIDE.md`
Abschnitt 3 beschreibt die Migration, nennt aber den Fall nicht, den jedes Projekt mit
mehr als einem Strang hat: **Welcher Befehl bekommt den Schlitz, wenn es sechs Kandidaten
für drei Plätze gibt?**

## 2. Vorgeschlagene Änderung

1. **Prüfung 43 (neu):** Führt ein Client Pack seine Hooks in der Berechtigungsdatei –
   erkennbar daran, dass `<HOOKS_FILE>` und `permissions_file` auf dieselbe Datei zeigen –,
   dann MUSS diese Datei einen nichtleeren `PreToolUse`-Block tragen. **Fehler.** Beide
   ausgelieferten Packs fallen darunter.
2. **Die Meldung der Prüfung 18 bekommt ihren zweiten Halbsatz:** Nicht nur die alte Datei
   löschen, sondern den Block in der Berechtigungsdatei führen – mit dem Verweis auf
   Prüfung 43, die es nachzählt.
3. **Prüfung 44 (neu):** Das Präparationsregister in `onboarding/exercises/README.md` und
   die Vorbedingungen in `tests/TEST_CATALOG.md` decken sich – **in beiden Richtungen,
   über die Kennung**: Jede im Katalog genannte Kennung `UEB-NN` steht im Register, und
   jede Kennung des Registers wird von mindestens einem Testfall gebraucht.
4. **Das Register wird vollständig:** `UEB-01` bis `UEB-07` mit Ort, Gegenstand und den
   Testfällen, die sie brauchen. Die Vorbedingungszellen des Katalogs nennen die Kennung.
5. **`FW-PI-04` wird berichtigt:** Die präparierte Ausgabe kommt aus einem der **drei
   erklärten** Befehle, nicht aus einem vierten. Was der Testfall misst, bleibt gleich;
   was er voraussetzt, wird herstellbar.
6. **`ADOPTION_GUIDE.md` bekommt den Absatz zu mehreren Technologiesträngen**, mit der
   gemessenen Entscheidungsregel: Den Schlitz bekommt der Befehl, der auf den
   Arbeitsplätzen des Projekts tatsächlich läuft.
7. **Register und Sondenmenge** werden nachgezogen – Einträge 43 und 44, Spanne wörtlich an
   den drei Trägern, die Prüfung 40 vergleicht. **Erst die Sonden, dann die Spanne** (die
   Lehre vom 2026-09-14).

## 3. Auswirkungen

- **Bestehende Installationen ohne Hook-Block bekommen einen Fehler.** Das ist der Zweck.
  Gemessen ist es genau eine: das Übungsrepositorium, dort mit diesem Release behoben.
  Die Behebung ist ein Handgriff – den Block aus einer frischen Installation übernehmen –
  und sie steht als Migrationshinweis im `CHANGELOG.md`.
- **Im Repositorium selbst findet Prüfung 43 nichts.** Die lokale Testinstallation trägt
  ihren Block. Das gehört so gesagt: Der Gegenbeweis ist ein Abzählen an einem echten
  Projekt, kein Fund im eigenen Baum.
- **Prüfung 44 hängt an einem Dokument, das dem Framework gehört** – anders als Prüfung 42,
  die in ein Projektdokument liest. Ein Umbau von `exercises/README.md` bricht sie, und der
  Bruch meldet sich als verlorener Anker.
- **Prüfung 44 sieht das Übungsrepositorium nicht.** Sie gleicht zwei Register ab, nicht
  Register gegen Wirklichkeit: Ob die Präparation `UEB-02` dort wirklich liegt, kann kein
  Validator dieses Repositoriums feststellen. **Das ist eine Enthaltung, keine Stille**, und
  sie steht im Kopfkommentar.
- **Der Testkatalog bekommt Kennungen in seinen Vorbedingungszellen.** Wer einen Testfall
  ergänzt, der eine Präparation braucht, muss sie registrieren – oder Prüfung 44 schweigt,
  weil er keine Kennung nennt. Auch das ist eine Grenze und steht dort.

## 4. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | **Fehler oder Warnung, wenn der Hook-Block fehlt?** | **Fehler.** Bei beiden Packs ist der Hook die einzige technische Schranke gegen Secrets in Werkzeugeingaben und gegen Schreibzugriffe auf den Kern über Werkzeuge, die die Berechtigungsdatei nicht erfasst. Eine Warnung hätte denselben Rang wie der Hinweis auf die verwaiste Datei – und genau der wurde einunddreißig Releases lang überlesen | **Ein Projekt, das den Hook bewusst nicht will, bekommt einen Fehler und kann ihn nicht abstellen.** Das ist gewollt: Der Hook ist Kernzusage, nicht Projektwahl. Wer ihn nicht will, deinstalliert das Framework – der Weg steht in `ADOPTION_GUIDE.md` Abschnitt 5 |
| **E2** | **Wie tief prüft 43 – Vorhandensein oder Inhalt?** | **Vorhandensein eines nichtleeren `PreToolUse`-Blocks.** Den Inhalt prüfen die Prüfungen 19 (Interpreter), 26 (Werkzeugabdeckung) und 27 (fail-closed) bereits – sie greifen, sobald der Block da ist. Eine vierte Inhaltsprüfung verdoppelte sie | **Ein Block mit einem `PreToolUse`-Eintrag, der auf ein fremdes Skript zeigt, läuft durch 43 durch** – und wird von 19 gefangen, weil der Interpreteraufruf nicht passt. Zwei Prüfungen, die zusammen greifen, sind erklärungsbedürftig; der Registereintrag sagt, was 43 **nicht** prüft |
| **E3** | **Was gilt für ein Pack mit eigener Hook-Datei?** | **Enthaltung.** Die Prüfung greift nur, wenn `<HOOKS_FILE>` und `permissions_file` auf dieselbe Datei zeigen. Derzeit tun das beide Packs; die Bedingung steht trotzdem da, weil ein künftiges Pack es anders halten kann | **Ein Pack mit eigener Hook-Datei bleibt ungeprüft.** Die Enthaltung ist benannt – und sie ist derselbe Zuschnitt, den Prüfung 18 schon hat |
| **E4** | **Wird Prüfung 18 erweitert oder bleibt sie?** | **Sie bleibt, ihre Meldung wächst.** 18 räumt die alte Datei ab, 43 verlangt die neue – zwei Gegenstände, zwei Nummern (dieselbe Begründung wie bei 37 und 42). Die Warnung nennt künftig beide Hälften der Migration | **Wer nur die Warnung liest, sieht jetzt mehr Text.** Der Preis ist Lesbarkeit gegen Vollständigkeit, und dieses Projekt hat die Frage entschieden |
| **E5** | **Welche Kennung bekommen die Präparationen?** | **`UEB-01` bis `UEB-07`.** `P1`, `P3` sind im Kern als Prinzipienkennungen vergeben (`05-working-model.md`); eine zweite Bedeutung desselben Zeichens in derselben Dokumentfamilie ist ein Fehler, den dieses Projekt schon einmal gemacht hat (`G-18`, 2026-09-13). `UEB-` ist im gesamten Kern frei – geprüft | **Eine weitere Kennungsfamilie** neben `CR-`, `D-`, `K-`, `G-`, `FW-`, `SK-`, `EX-`. Sie ist die erste, die einen Gegenstand **außerhalb** des Repositoriums benennt |
| **E6** | **Prüft 44 beide Richtungen?** | **Ja.** Eine Kennung im Katalog ohne Registereintrag ist ein Tippfehler oder eine unregistrierte Präparation; eine Kennung im Register, die kein Testfall braucht, ist eine tote Präparation, die jemand pflegt | **Was sie nicht kann:** einen Testfall fangen, der eine Präparation braucht und keine Kennung nennt. Genau der Fall von Befund 2 – **die Prüfung verhindert seine Wiederholung nur, wenn die Kennung gesetzt wird.** Das ist dieselbe Ehrlichkeit wie bei Prüfung 38 und 40, und es steht im Kopfkommentar |
| **E7** | **Wie wird `FW-PI-04` aufgelöst – Testfall streichen oder umformulieren?** | **Umformulieren.** Die Injektion über eine Werkzeugausgabe ist ein realer Angriffsweg und der einzige Testfall, der ihn abdeckt. Herstellbar wird er, wenn die präparierte Ausgabe aus einem der drei **erklärten** Befehle kommt – im Übungsrepositorium aus `<TEST_COMMAND>`, dessen Lauf eine Anweisung auf stdout schreibt | **Der Testfall misst danach denselben Mechanismus in einer engeren Lage:** Die Ausgabe kommt aus dem Testlauf, nicht aus einem beliebigen Skript. Wer ihn fährt, muss die Präparation in einer Testdatei unterbringen – sie ist `UEB-06` und liegt ohnehin dort |
| **E8** | **Eigenes Release oder Anhang an 0.44.0?** | **Eigenes Release `0.45.0`.** Zwei neue Prüfungen, ein Migrationshinweis, ein berichtigter Testfall – das ist ein geschlossener Gegenstand | **Das zwanzigste Release in vier Tagen.** Und das erste, dessen Anlass **nicht** ein Befund im Repositorium war, sondern die Arbeit an einem Projekt, das dieses Repositorium benutzt |

## 5. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle acht Fragen wie vorgelegt.** E1 fehlender Hook-Block ist ein Fehler; E2 Prüfung 43 prüft das Vorhandensein, den Inhalt prüfen 19, 26 und 27; E3 ein Pack mit eigener Hook-Datei bleibt ausgenommen und die Enthaltung steht im Kopfkommentar; E4 Prüfung 18 bleibt, ihre Meldung nennt beide Hälften der Migration; E5 Kennungen `UEB-01` bis `UEB-07`; E6 Prüfung 44 gleicht beide Richtungen ab, ihre Grenze steht im Kopfkommentar; E7 `FW-PI-04` wird umformuliert statt gestrichen; E8 eigenes Release `0.45.0` |
| Datum | 2026-09-15 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | D-92 (führt ein Pack seine Hooks in der Berechtigungsdatei, ist ein fehlender Hook-Block ein Fehler – eine Hook-Konfiguration am falschen Ort ist keine), D-93 (die Präparationen des Übungsrepositoriums sind ein Register mit Kennungen, und der Testkatalog nennt sie an der Vorbedingung) |
| Auflagen | **Der Gegenbeweis für Prüfung 43 ist ein Abzählen an vier echten Installationen, und seine Grenze steht daneben:** Im Repositorium selbst findet sie nichts, weil die lokale Testinstallation ihren Block trägt. **Und Prüfung 44 weist ihre Enthaltung aus** – sie gleicht zwei Register ab, nicht ein Register gegen die Wirklichkeit des Übungsrepositoriums |
| Ziel-Release | `0.45.0` |
| Umsetzung | umgesetzt mit `0.45.0` |
