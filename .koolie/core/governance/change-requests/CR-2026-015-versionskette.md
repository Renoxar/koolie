# Änderungsantrag `CR-2026-015`

| Feld | Inhalt |
|---|---|
| Titel | Neun Lücken der Versionskette, gefunden beim Ausführen von `FW-VN-01` |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | `governance/RELEASE_PROCESS.md`; `checklists/11-framework-release.md` und die übrigen zehn Checklisten; `prompts/*` (13 Dateien); `templates/MR_AI_DISCLOSURE.md`; alle 13 Skills (`SKILL.md`, `CHANGELOG.md`, `EXAMPLES.md`); `tests/scripts/validate-framework.py`; `examples/example-mr-description.md`, `example-ergebnisbericht.md`; 30 Kerndateien mit der Bezeichnung des Nutzungsvermerks; `tests/TEST_CATALOG.md`; neu: `tests/protocols/2026-09-10-FW-VN-01.md` und `-wiederholung.md` |
| Ebene laut Entscheidungsbaum 6 | Core (Governance-Regeltext, Ebene 3) und Prüfwerkzeug |
| Art | Fehlerbehebung, Verschärfung und eine Regeleinschränkung |
| Dringlichkeit | regulär (Review-Zyklus) |

## 1. Anlass und Problem

`FW-VN-01` prüft die Nachweiskette aus `RELEASE_PROCESS.md` Abschnitt 8: Framework-Version →
Overlay-Version → Skill-Versionen → Berechtigungsstand → KI-Nutzungsvermerk im Merge Request →
Vorfall- und Ausnahmeregister. Der Testfall ist der zweite Review-Testfall des Katalogs
überhaupt. Ergebnis: **`fehlgeschlagen`, neun Befunde in drei der sechs Glieder.**

**Die Kette ist nirgends gebrochen.** In der Referenzinstallation stimmt jede Angabe mit jeder
anderen überein. Sie hält aber ausschließlich durch Sorgfalt – und an einer Stelle hat die
Sorgfalt über zwölf Releases nachgelassen, ohne dass es jemand bemerkt hat.

**Der tragende Befund: Eine Versionsangabe, die sich nie ändert, unterscheidet keine zwei
Zeitpunkte.** Alle 13 Skills stehen unverändert auf `0.1.0`, obwohl alle 13 `SKILL.md`
geändert wurden – 126 Zeilen in den Releases 0.5.0 und 0.7.0. Kein Skill-Änderungsverlauf hat
dafür einen Eintrag bekommen. Das ist kein Ermessen: `08-skill-conventions.md` Abschnitt 7
stuft solche Änderungen als PATCH ein, und die Release-Checkliste verlangt die Pflege je
geändertem Skill als **MUSS**. Dieselbe Lücke, ohne jede Pflicht dahinter, tragen elf
Checklisten und dreizehn Prompts.

**Wirksam wird das im Nutzungsvermerk.** Die Kurzform für Kontrollstufe niedrig – den Regelfall
– nannte weder Framework- noch Overlay-Version; ihre einzige Versionsangabe waren die Skills.
Das synthetische Beispiel des Frameworks zeigte es unfreiwillig:

    - Verwendete Skills: fw-change-analyze v0.1.0, fw-change-small v0.1.0

Beide Werte waren für jedes Release von 0.1.0 bis 0.12.0 identisch. Bei Kontrollstufe niedrig
enthielt ein Merge Request damit keine einzige Versionsangabe, die sich je geändert hat – die
Kette war dort formal vollständig und inhaltlich leer.

**Der Validator prüft, ob Versionsfelder da sind, nie ob sie stimmen.** Fünf Sonden mit
bekanntem Defekt blieben sämtlich unbemerkt: Steckbriefangabe gegen `VERSION`, Manifestwert
gegen Steckbrief, Laufzeitfassung gegen Steckbrief, Skill-Version gegen den eigenen
Änderungsverlauf, und `banane` als Versionswert. Drei Gegenproben wurden jede gemeldet. Das ist
exakt die Blindstellenform, die D-23 an vier anderen Prüfungen gefunden hat, hier auf das
Merkmal angewandt, um das es in diesem Testfall geht.

**Die Overlay-Version steht an drei Stellen** – Steckbrief, Manifest, Laufzeitfassung – und
keine wurde gegen eine andere geprüft. Für den Overlay-*Status* hat D-23 genau diese Lücke
geschlossen; für die Version blieb sie offen.

**Das Kettenglied heißt anders als sein Artefakt.** Abschnitt 8 nennt den
„**KI**-Nutzungsvermerk"; die Vorlage, auf die überall verwiesen wird, hieß
„**Devin**-Nutzungsvermerk". Im Kern standen 39 Nennungen der alten Form in 29 Dateien. Das ist
die unerledigte Hälfte von Befund B1 aus `FW-KO-02` – dort wurde nur die Laufzeitschicht
umgestellt – und `CR-2026-005` hatte dieselbe Umbenennung bereits für 0.5.0 als Nebeneffekt
verzeichnet. Zweimal angekündigt, zweimal nicht zu Ende geführt.

**Eine Kernvorlage nannte einen Client.** Beide Textblöcke der Vermerkvorlage trugen die
Überschrift `### KI-Unterstützung (Devin Desktop)`. Die Vorlage wird in **jedes** Client Pack
installiert; ein Projekt mit dem Pack `claude-code` hätte den Produktnamen eines Werkzeugs in
seinen Merge Request geschrieben, das bei ihm nicht im Einsatz ist. Derselbe Befundtyp wie B2
aus `FW-KO-02`.

**Die Zusage aus Abschnitt 1.2 stand seit 0.1.0 unerfüllt im Regeltext.** Sie verlangt von fünf
Artefaktklassen eine Referenz auf die kompatible Framework-Version. Erfüllt hat sie genau eine:
das Overlay – ausgerechnet die Klasse, die nicht im Kern liegt.

## 2. Vorgeschlagene Änderung

Sieben der neun Befunde lassen nur eine Auflösungsrichtung zu. Zwei ändern eine Regel und nicht
nur ihre Durchsetzung; sie wurden der zweiten Rolle einzeln vorgelegt (Protokoll, E1 und E2).

**Der Validator bekommt Prüfung 13 (Versionskette).** Sie vergleicht die drei Ablageorte der
Overlay-Version miteinander, die Steckbriefangabe zur kompatiblen Framework-Version gegen
`leitwerk-core/VERSION` und jedes Versionsfeld gegen die Form `MAJOR.MINOR.PATCH`; zusätzlich
muss eine Skill-Version einen Eintrag im eigenen Änderungsverlauf haben. Damit hält die Kette
durch einen Mechanismus statt durch Disziplin – die Konsequenz aus D-23.

**Die Skill-Versionen werden auf `0.1.1` angehoben**, mit einem Eintrag je Änderungsverlauf
(E2, bestätigt). Verworfen wurde eine Ausnahmeregel für reine Pfad- und Namensanpassungen: Die
Grenze wäre nicht prüfbar, weil `CR-2026-009` 994 Pfadnennungen geändert hat, darunter Verweise
auf Vorlagen und Checklisten, die ein Skill anwendet – „nur ein Pfad" ist eine Aussage über die
Absicht, nicht über die Datei. Ebenfalls verworfen wurde das Streichen der Skill-Version: Sie
löst zwei Befunde auf einmal, nimmt dem Nutzungsvermerk aber die Angabe, welcher Skill in
welchem Stand gelaufen ist – und die wertet `pilot/METRICS.md` je Vermerk aus.

Der Preis ist benannt: `08-skill-conventions.md` Abschnitt 7 verlangt bei jeder Versionsänderung
die erneute Ausführung der Testfälle in `TESTS.md`. Diese sind sämtlich `sitzung` und hängen an
AP2, bleiben also bis dahin offen. Eine offene Testpflicht ist ehrlicher als eine
Versionsangabe, die nichts aussagt: Die erste ist in AP2 sichtbar, die zweite nicht.

**Checklisten und Prompts werden gleich behandelt** und bekommen erstmals eine Pflicht: Die
Release-Checkliste fordert die Versionspflege künftig auch für sie. Ohne diesen Punkt hätte das
Release eine Regel ausgeliefert, die im selben Stand schon verletzt ist.

**Abschnitt 1.2 wird eingeschränkt statt eingelöst** (E1, bestätigt). Eine kompatible
Framework-Version nennen nur die Artefakte, die vom Kern **abweichen können**: das Overlay
(gehört dem Projekt) und das Client Pack (bildet einen fremden Client ab). Skills, Checklisten
und Prompts werden byte-gleich im Release ausgeliefert; ihre kompatible Framework-Version ist
`leitwerk-core/VERSION` im selben Verzeichnis. Verworfen wurde das Einlösen der Zusage: Es
entstünde in 35 Dateien ein Wert, der bei jedem Release nachzuziehen wäre – genau die
Doppelpflege, die D-16, D-17 und D-20 beseitigt haben – und der veraltet, ohne dass es auffällt.

**Die Umbenennung des Nutzungsvermerks wird zu Ende geführt**, im Kern und nicht nur in der
Laufzeitschicht: 39 Nennungen in 29 Dateien. Die Überschrift der Vorlage wird clientneutral,
und ihr Ausfüllhinweis spricht nicht mehr von einem einzelnen Produkt.

**Die Kurzform des Vermerks nennt Framework- und Overlay-Version.** Zwei Zeilen. Ohne sie hat
die Kette bei Kontrollstufe niedrig keinen Anker.

Änderungsverzeichnis, Änderungsanträge und Testprotokolle bleiben unangetastet – sie sind
historische Belege und dürfen nicht rückwirkend geglättet werden.

## 3. Prüffragen (durch Owner auszufüllen)

- [x] Richtige Ebene nach Entscheidungsbaum 6? — Ja. `RELEASE_PROCESS.md` ist Governance-Regeltext der Ebene 3; die Prüfung im Validator ist Werkzeug, kein Regeltext.
- [x] Verschärfungsprinzip eingehalten? — Acht der neun Befunde werden durch Verschärfung oder Klarstellung aufgelöst. Eine Auflösung schränkt eine Regel **ein** (E1) und ist deshalb einzeln begründet und vorgelegt worden: Die Zusage aus Abschnitt 1.2 war für drei der fünf Klassen nie erfüllbar, ohne eine Doppelpflege zu erzeugen, die drei Decision Records zuvor beseitigt haben. Der Nachweis wird dadurch nicht schwächer – der Wert steht im selben Verzeichnis.
- [x] Widerspruchsfreiheit geprüft? — `FW-KO-04` und der Validator melden 0 Fehler. Die Umbenennung des Nutzungsvermerks beseitigt eine Abweichung zwischen Abschnitt 8 und dem Artefakt, auf das er zeigt.
- [x] Laufzeitfassungen betroffen? — Nein. Die vier Regeltexte der Laufzeitschicht sagten seit 0.12.0 bereits „KI-Nutzungsvermerk". Betroffen ist die **Saat**: `templates/MR_AI_DISCLOSURE.md` behält in einem bestehenden Projekt seine Fassung. Migrationshinweis im CHANGELOG.
- [x] Belegstatus korrekt? — Unverändert. Dieser Antrag berührt keine Aussage über Produktfunktionen eines Clients.
- [x] Test- und Validierungsbedarf? — `FW-VN-01` ist durchgeführt, die Befunde sind behoben, der Wiederholungslauf meldet alle fünf Sonden. Die Gegenzeichnung durch eine zweite Rolle steht aus, siehe Abschnitt 5.
- [x] Auswirkungen auf Overlays und laufende Onboardings? — Prüfung 13 kann in einem bestehenden Projekt Fehler melden, deren Ursache älter ist als dieses Release: eine nicht nachgezogene Steckbriefangabe oder auseinandergelaufene Overlay-Versionen. Das ist der Zweck der Prüfung; die Behebung sind zwei Zeilen und steht im CHANGELOG.
- [x] Dokumentation? — CHANGELOG, Decision Log, Roadmap, Testkatalog, zwei Testprotokolle.

## 4. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | angenommen |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Eine Nachweiskette ist kein Formular. Sie taugt genau so weit, wie ihre Glieder zwei Zeitpunkte unterscheiden können – und eine Versionsangabe, die sich über zwölf Releases nicht bewegt, kann das nicht. Dass niemand es bemerkt hat, ist der eigentliche Befund: Der Validator prüfte die Anwesenheit der Felder und niemals ihren Inhalt. Mit Prüfung 13 hält die Kette durch einen Mechanismus; mit den angehobenen Versionen sagt sie wieder etwas aus. |
| Ziel-Release | 0.13.0 |
| Decision-Log-Eintrag | D-25 |

## 5. Umsetzung (nach Annahme)

- [x] V1: Prüfung 13 vergleicht Steckbrief, Manifest und Laufzeitfassung; abweichende Overlay-Versionen sind ein Fehler
- [x] V2: Prüfung 13 vergleicht die Steckbriefangabe zur kompatiblen Framework-Version gegen `leitwerk-core/VERSION` (`0.N.x` oder exakt)
- [x] V6: Versionsfelder werden gegen `MAJOR.MINOR.PATCH` geprüft; eine Skill-Version ohne Eintrag im eigenen Änderungsverlauf ist ein Fehler
- [x] V3/V4 (E2): 13 Skills auf `0.1.1` mit Eintrag je Änderungsverlauf; 10 Checklisten und 13 Prompts auf `0.1.1`; `11-framework-release.md` auf `0.2.0` wegen der neuen Pflicht
- [x] V5 (E1): `RELEASE_PROCESS.md` Abschnitt 1.2 auf Overlays und Client Packs eingeschränkt, mit Begründung im Regeltext
- [x] V7: „Devin-Nutzungsvermerk" → „KI-Nutzungsvermerk" in 29 Kerndateien (39 Nennungen). **Nennungen im Kern: 39 → 0**
- [x] V8: Überschrift und Ausfüllhinweis der Vermerkvorlage clientneutral; dieselbe Überschrift in drei weiteren Dateien nachgezogen
- [x] V9: Kurzform des Vermerks nennt Framework- und Overlay-Version; beide Beispiele nachgezogen
- [x] Wiederholungslauf `FW-VN-01`: alle fünf Sonden gemeldet, Ausgangs- und Schlusslauf 0 Fehler
- [x] Validator, `FW-KO-04` und `install.py --check`: 0 Fehler, 0 Warnungen
- [x] **Gegenzeichnung** durch `<FRAMEWORK_OWNER>` am 2026-09-10 erfolgt; die beiden Auflösungen mit Ermessensspielraum wurden einzeln vorgelegt und entschieden (E1: Abschnitt 1.2 einschränken statt einlösen; E2: Skill-Versionen anheben). `FW-VN-01` steht damit auf `bestanden`. Nachgetragen nach dem Merge des Releases
- [ ] **Folgearbeit:** Die Testfälle in `TESTS.md` je Skill sind wegen der Versionsanhebung erneut auszuführen (`08-skill-conventions.md` Abschnitt 7). Sie sind sämtlich `sitzung` und hängen an AP2; in der Roadmap vermerkt
