# Änderungsantrag `CR-2026-014`

| Feld | Inhalt |
|---|---|
| Titel | Sieben Abweichungen zwischen Kurz- und Langform, gefunden beim Ausführen von `FW-KO-02` |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | `framework/runtime/root-instruction.md`; `framework/runtime/rules/00-framework-core.md`, `10-privacy-security.md`, `15-development-rules.md`, `20-project-overlay.md`; `framework/core/05-working-model.md`, `10-error-escalation.md`; `tests/TEST_CATALOG.md`; neu: `tests/protocols/2026-09-10-FW-KO-02.md` |
| Ebene laut Entscheidungsbaum 6 | Core (Regeltexte, Ebene 3) |
| Art | Fehlerbehebung und Verschärfung |
| Dringlichkeit | regulär (Review-Zyklus) |

## 1. Anlass und Problem

Das Framework führt seine Regeln in zwei Fassungen (D-02): der kanonischen Langform unter
`framework/core/` und der kompakten Laufzeitfassung, die in jeder Sitzung geladen wird. Die
Kurzfassungen tragen den Satz „Diese Fassung ist normativ; bei Abweichungen gilt die
Langform." `FW-KO-02` prüft, ob dieser Satz trägt.

Er trug nicht durchgehend. Der Abgleich ergab **sieben Befunde** – drei Widersprüche, vier
Lücken – dazu zwei begriffliche Abweichungen.

**Der wichtigste Befund ist eine Lücke, kein Widerspruch.** Die Delegationsverbotsliste ist
die schärfste Regel des Frameworks: Sie gilt unabhängig von der Kontrollstufe, und das
Overlay darf sie erweitern, aber nicht verkürzen. **Vier ihrer zwölf Einträge kamen in
keiner geladenen Datei vor** – V6 (Produktionssysteme, Infrastruktur, Berechtigungen,
Sicherheitskonfigurationen), V9 (Entscheidung über die Fortsetzung bei einem
Sicherheitsvorfall), V11 (Kommunikation nach außen) und V12 (Löschen von Branches, Historie,
Daten außerhalb des Arbeitsbereichs). Die Langform steht nicht im Kontext einer Sitzung; was
dort steht und in der Kurzform fehlt, erreicht das Werkzeug nicht.

**Zwei Widersprüche betreffen Rechte und Einstufungen:**

Die Kurzform verbot in M1 jede Befehlsausführung, die Langform erlaubt lesende
Analysebefehle – und die ausgelieferte Berechtigungsdatei stellt `git status`, `diff`, `log`,
`show` und `blame` in jedem Modus auf `allow`. Die Kurzform behauptete also ein Verbot, das
an keiner Stelle durchgesetzt wird. Der Testfall nennt Modusrechte ausdrücklich als
Beispiel für unzulässiges Verhalten.

Die Kurzform stufte jede Berührung personenbezogener Datenverarbeitung als mindestens
Kontrollstufe hoch ein. Die Langform unterscheidet: ein Code-Pfad, der personenbezogene
Daten verarbeitet, ohne dass sich die Verarbeitungslogik ändert, ist **mittel** – das
Rechenbeispiel in `09-risk-model.md` Abschnitt 5 stuft genau so ein. Zwei gegensätzliche
Aussagen über dieselbe Kontrollstufe.

**Ein Widerspruch liegt innerhalb der Langform selbst:** `10-error-escalation.md` lässt in
S10 „mehr als zwei Versuche" zu, verlangt in Abschnitt 3.1 desselben Moduls aber den Abbruch
„nach zwei fehlgeschlagenen Korrekturschleifen". Die Wurzel-Anweisung folgt der strengeren
Lesart.

**Zwei begriffliche Befunde:** Der Nutzungsvermerk im Merge Request hieß an drei Stellen
verschieden, eine Bezeichnung davon an einen Client gebunden. Und `20-project-overlay.md` –
eine Kernvorlage, die in **jedes** Client Pack installiert wird – nannte an vier Stellen
„Devin" als Akteur; ein Projekt mit dem Pack `claude-code` liest dort den Produktnamen eines
Werkzeugs, das bei ihm nicht im Einsatz ist.

## 2. Vorgeschlagene Änderung

Die Richtung der Auflösung ist bei jedem Widerspruch begründungspflichtig, weil beide
Fassungen normativ sind.

**M1-Befehlsrecht: Die Kurzform folgt der Langform.** Lesende Analysebefehle bleiben
zulässig; sie sind in der Berechtigungsdatei ohnehin erlaubt, und ein Verbot, das nirgends
greift, erzeugt nur ein falsches Bild der Durchsetzungstiefe. Im selben Zug wird die
Langform mit sich selbst in Einklang gebracht: M2 führte „Alles aus M1" und
„Befehlsausführung: nein" nebeneinander.

**Kontrollstufe bei personenbezogenen Daten: Die Kurzform folgt der Langform.** Die
Gegenrichtung – jede Berührung auf hoch – hätte die Abstufung in R4 und ihr Rechenbeispiel
entwertet und die Stufe hoch inflationär gemacht. Die Kurzform übernimmt die Unterscheidung
im Wortlaut.

**Abbruchschwelle: Die Langform folgt der Kurzform.** S10 wird auf „zwei erfolglose
Versuche" gesetzt – die strengere Lesart, die zugleich mit Abschnitt 3.1 desselben Moduls
und mit der Wurzel-Anweisung übereinstimmt.

**Die vier Lücken werden in der Kurzform geschlossen.** Die fehlenden Delegationsverbote,
die K3-Auffangkategorie („alles, was die Organisation als vertraulich oder höher eingestuft
hat" – eine Aufzählung ohne Auffangkategorie lädt zum Umkehrschluss ein), die
Größenschwelle aus Q8 und die Erleichterung bei Kontrollstufe niedrig, die bisher nur in
der Langform stand.

**Die Laufzeitschicht wird client-neutral.** „KI-Nutzungsvermerk" mit Verweis auf die
Vorlage; in `20-project-overlay.md` direkte Anrede statt Produktname. Damit enthalten alle
fünf Dateien der Laufzeitschicht null Client-Bindungen.

Die 74 Nennungen von „Devin" in den elf Langform-Modulen bleiben unangetastet. Sie sind der
Rest der Neutralisierung aus D-15 – dort wurden Pfade ersetzt, nicht die Akteursbezeichnung
– und wirken nicht auf das Verhalten, weil die Langform nicht in die Sitzung geladen wird.
Das ist eine eigene Aufgabe und gehört in die Roadmap, nicht in diesen Antrag.

## 3. Prüffragen (durch Owner auszufüllen)

- [x] Richtige Ebene nach Entscheidungsbaum 6? — Ja. Die Regeltexte der Ebene 3 ändern sich; deshalb ein Änderungsantrag und keine redaktionelle Korrektur.
- [x] Verschärfungsprinzip eingehalten? — Sechs der sieben Befunde werden durch Verschärfung oder Klarstellung aufgelöst. Zwei Auflösungen erweitern den Spielraum und sind deshalb einzeln begründet: das M1-Befehlsrecht (die Kurzform behauptete ein Verbot, das die Berechtigungsdatei nicht kennt) und die Kontrollstufe bei personenbezogenen Daten (die Kurzform übersteuerte eine bewusste Abstufung der Langform). In beiden Fällen galt bereits die Langform – der Spielraum wird nicht erweitert, sondern richtig beschrieben.
- [x] Widerspruchsfreiheit geprüft? — Das ist der Gegenstand dieses Antrags. Nach der Änderung: keine widersprüchlichen Anweisungen; die verbliebenen Abweichungen sind im Protokoll dokumentiert. Validator und `FW-KO-04`: 0 Fehler.
- [x] Laufzeitfassungen betroffen? — Ja, alle fünf. Sie sind **Core** und werden von `install.py --update` überschrieben; einzige Ausnahme ist `20-project-overlay.md`, das als Saat in einem bestehenden Projekt seine ausgefüllte Fassung behält. Migrationshinweis im CHANGELOG.
- [x] Belegstatus korrekt? — Unverändert. Dieser Antrag berührt keine Aussage über Produktfunktionen eines Clients.
- [x] Test- und Validierungsbedarf? — `FW-KO-02` ist durchgeführt; die Gegenzeichnung durch eine zweite Rolle steht aus, siehe Abschnitt 5.
- [x] Auswirkungen auf Overlays und laufende Onboardings? — Die Kurzfassungen werden länger (00: 3.301 → 3.946 Zeichen, weit unter der Grenze von 12.000). Ein Projekt mit ausgefülltem `20-project-overlay.md` zieht die vier neutralisierten Stellen von Hand nach oder belässt sie – sie sind erläuternd, nicht normativ.
- [x] Dokumentation? — CHANGELOG, Decision Log, Roadmap, Testkatalog, Testprotokoll.

## 4. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | angenommen |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Zwei Fassungen derselben Regel sind nur so lange ein Gewinn, wie sie dasselbe sagen. Die Kurzform ist die einzige, die das Werkzeug je zu sehen bekommt – eine Regel, die nur in der Langform steht, ist eine Regel, die nicht wirkt. Dass ein Drittel der Delegationsverbotsliste nirgends geladen wurde, ist der Befund, der diesen Antrag trägt; die drei Widersprüche sind der Anlass, aus dem er gefunden wurde. |
| Ziel-Release | 0.12.0 |
| Decision-Log-Eintrag | D-24 |

## 5. Umsetzung (nach Annahme)

- [x] W1: M1 und M2 in Kurz- und Langform auf „nur lesende Analysebefehle" angeglichen
- [x] W2: Kurzform übernimmt die Abstufung aus R4 (mittel bei unveränderter Verarbeitungslogik, hoch bei Änderung an Erhebung, Speicherung, Weitergabe oder Löschung)
- [x] W3: S10 auf „zwei erfolglose Versuche" gesetzt, im Einklang mit Abschnitt 3.1 und der Wurzel-Anweisung
- [x] L1: Alle zwölf Delegationsverbote stehen in der Kurzform; die Wurzel-Anweisung nennt zusätzlich Sicherheitsvorfall, Außenkommunikation und Löschen außerhalb des Arbeitsbereichs als Haltegründe
- [x] L2: K3-Auffangkategorie, Keystores und Verbindungszeichenfolgen mit Anmeldedaten ergänzt; Hinweis, dass eine K2-Freigabe dokumentiert sein muss
- [x] L3: Größenschwelle aus Q8 in `15-development-rules.md`
- [x] L4: Erleichterung bei Kontrollstufe niedrig in der Kurzform benannt
- [x] B1/B2: „KI-Nutzungsvermerk" mit Verweis auf die Vorlage; `20-project-overlay.md` neutralisiert. **Client-Bindungen in der Laufzeitschicht: 4 → 0**
- [x] Validator, `FW-KO-04` und `install.py --check`: 0 Fehler. Hauptdokument baut für beide Client Packs
- [ ] **Offen, absichtlich:** Die Gegenzeichnung des Reviews durch eine zweite Rolle steht aus. `FW-KO-02` bleibt bis dahin auf `offen` – der Abgleich ist durchgeführt und die Befunde sind behoben, aber eine Selbstbestätigung ist kein Review durch eine zweite Rolle
- [ ] **Folgearbeit:** 74 Nennungen von „Devin" als Akteur in den elf Langform-Modulen. Sie wirken nicht auf das Verhalten, widersprechen aber der Zusage eines werkzeugneutralen Kerns (D-15). Eigene Änderung, in der Roadmap vermerkt
