# Änderungsantrag `CR-2026-072`

| Feld | Inhalt |
|---|---|
| Titel | Das Lebenszyklusmodell wird zum ersten Mal angewendet – dreizehn Skills auf `pilot`, vier Formularfelder aus der Zählung, und die Vorbedingung hielt in zwei von drei Punkten nicht |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-15 |
| Betroffene Artefakte | `framework/skills/*/SKILL.md` (zwölf), `framework/role-packs/requirements-engineering/skills/role-re-ticket/SKILL.md`, `clients/_template/CLIENT_PACK.md`, `framework/role-packs/_template/ROLE_PACK.md`, `framework/tech-packs/_template/TECH_PACK.md`, `templates/SKILL_TEMPLATE.md`, `framework/core/01-governance.md`, `framework/core/08-skill-conventions.md`, `governance/DECISION_LOG.md` (D-102 bis D-104, K-36, K-37), `docs/ROADMAP.md` (Standzeile, Kriterientabelle, AP3, P3-Posten, Abschnitt „Geplant: Projekt-Overlays"), `CHANGELOG.md`, `tests/protocols/2026-09-15-gegenpruefung-modulstatus.md`, `tests/protocols/2026-09-15-wirkungsnachweise-0.50.0.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind das Lebenszyklusmodell des Frameworks und der Status seiner eigenen Module |
| Art | Änderung (Statuswechsel), Ergänzung (Übergangsbedingungen für Nicht-Skill-Träger) |
| Dringlichkeit | **Regulär.** Kein Sicherheitsbezug. Der Gegenstand ist die zweite Aktivität von Arbeitspaket `AP3` (P1) und Kriterium 3 von D-11 |

## 1. Anlass

**Beauftragt, nicht gefunden** – wie bei `CR-2026-071`, und mit derselben Quelle: Prüfung 46
zählt seit 0.48.0 die vier maschinell zählbaren Kriterien von D-11 bei jedem Lauf.
Kriterium 4 ist mit 0.49.0 auf null gegangen. **Kriterium 3 ist danach der nächste Posten:
69 Statusträger, keiner über `entwurf`.**

Der Aufgabe war eine **Vorbedingung** vorangestellt, und sie war nicht klein:

> Das Lebenszyklusmodell (`framework/core/08-skill-conventions.md` Abschnitt 7) definiert
> die Übergangsbedingungen **nur für Skills**. 57 der 69 Träger sind keine Skills. Für sie
> gibt es keine niedergeschriebene Bedingung, um `entwurf` zu verlassen. Das gehört
> entschieden, bevor ein Status gehoben wird. Und: Für die zwölf Skills verlangt das Modell
> „Testfälle bestanden" – die stehen alle auf `offen`, also sind Kriterium 2 und 3 dort
> gekoppelt.

**Die Gegenprüfung hat zuerst diese Bedingung geprüft, nicht die Aufgabe** – die Lehre von
0.49.0, eine Woche alt, auf den nächsten Vorgang angewendet. Ergebnis: **Von drei
Behauptungen halten zwei nicht.**

Vollständig mit Fundstellen und unveränderter Messausgabe in
`tests/protocols/2026-09-15-gegenpruefung-modulstatus.md`. Kurzfassung:

| Behauptung | Urteil | Beleg |
|---|---|---|
| „57 der 69 Träger sind keine Skills" | **falsch: 52** | 13 Skills (nicht 12 – der dreizehnte liegt in einem Role Pack), 4 Vorlagen, 52 übrige. `CR-2026-071` hat dieselbe Zahl einen Antrag vorher richtig genannt: „**13 von 13** Skills tragen genau die vier Dateien" |
| „Das Modell verlangt für die Skills bestandene Testfälle, also sind Kriterium 2 und 3 gekoppelt" | **falsch** | Die Spalte *Voraussetzung für Übergang* sagt bei `pilot` „Testfälle **vorhanden**, Validierung bestanden, Review durch Modul-Owner". „Bestanden" steht in der Zeile **`aktiv`**. Gelesen worden ist die falsche Zeile |
| „Für die Nicht-Skills fehlt jede niedergeschriebene Bedingung" | **richtig** | `01-governance.md` Abschnitt 3 Punkt 4 nennt den Lebenszyklus ausdrücklich nur für Skills; 52 Träger führen trotzdem eine Statuszelle |

> **Zum zweiten Mal in zwei Releases war nicht die Aufgabe das Hindernis, sondern ihre
> Bedingung.** Bei `CR-2026-071` war sie falsch **gewählt** und hielt zweiunddreißig
> Releases; hier ist sie falsch **gelesen** und hätte Kriterium 3 an den größten Posten des
> Vorhabens gekettet. **Eine Bedingung, die niemand nachzählt, ist eine Zusage mit
> umgekehrtem Vorzeichen.**

## 2. Der Befund, der nicht gesucht war: vier Träger sind gar keine Module

Vier der 69 sind **Vorlagen**, und bei allen vier ist die Kennungszelle ein Platzhalter
(`CP-<CLIENT_PACK_CODE>`, `RP-<ROLE_PACK_CODE>`, `TP-<TECH_PACK_CODE>`,
`<FW-SK-NNN / …>`). Ihr Steckbrief beschreibt nicht sie selbst, sondern **die Kopie, die
aus ihnen entsteht** – jede Vorlage sagt das in ihrem Ausfüllhinweis.

**Der Statuswert `entwurf` ist dort kein Platzhalter und geht deshalb unverändert in jede
Kopie über.** Heute ist das das richtige Verhalten: Ein neues Pack beginnt im Entwurf.
Daraus folgt aber, dass diese vier Zeilen sich **nie ändern dürfen** – und damit:

> **Kriterium 3 ist in der heutigen Zählung unerreichbar.**

**Das ist genau der Defekt, zu dessen Beseitigung D-11 entstanden ist.** Seine Begründung
über den Vorgänger D-09: *„machte das Release-Gate FW-CL-11 dadurch **unerreichbar**; die
neuen Kriterien sind **prüfbar** und liegen im Einflussbereich des Framework Owners."* Der
Fall ist derselbe, zwei Größenordnungen kleiner – und deshalb seit der Erstfassung
unbemerkt.

## 3. Der zweite Befund: beide naheliegenden mechanischen Bedingungen taugen nicht

Wenn 52 Träger eine Bedingung brauchen, ist die erste Frage, ob sie ein Skript prüfen kann.
Zwei Kandidaten liegen auf der Hand, beide sind versucht, **beide fallen durch**:

| Kandidat | Warum er durchfällt |
|---|---|
| „keine offenen `<TBD:>`-Schlitze" (29 Träger betroffen) | `<TBD:` trägt drei Bedeutungen: **Anweisungstext** eines Skills („nicht belegbare Felder als `<TBD: …>`"), **Ausfüllschlitz** einer Vorlage, und **echte Lücke** – die aber der aufnehmenden Organisation gehört (`checklists/09-onboarding.md`: `<TBD: Referenz auf Unterweisung>`), und die nimmt D-11 ausdrücklich aus. **29 gesperrt, keiner zu Recht** |
| „kein offener `VERIFY`-Marker" (9 Träger betroffen) | **Vier von neun benennen den Marker, statt ihn zu tragen** – `checklists/11-framework-release.md`, `clients/README.md`, `governance/RELEASE_PROCESS.md`, `docs/ROADMAP.md`. Es hätte ausgerechnet die **Release-Checkliste** und den **Release-Prozess** gesperrt. Das ist die Lehre E3 von `CR-2026-070` – Kriterium 1 zählt die Register- und Glossarzeilen des Markers mit – eine Ebene tiefer |

> **Eine Marke, die in einem Bestand sowohl benutzt als auch benannt wird, taugt nicht als
> Bedingung.** Beide Kandidaten scheitern nicht an ihrer Strenge, sondern daran, dass sie
> eine Zeichenkette zählen, wo ein Urteil gefragt ist.

## 4. Vorgeschlagene Änderung

1. **Die dreizehn Skills gehen auf `pilot`** – die Bedingungen des geltenden Modells sind
   erfüllt und je Skill an sechs Gegenständen abgenommen (Protokoll Abschnitt 5).
2. **Die Statuszelle der vier Vorlagen wird ein Ausfüllschlitz**, und der Ausfüllhinweis
   nennt den Wert, mit dem eine Kopie beginnt.
3. **`framework/core/01-governance.md` erhält einen normativen Abschnitt mit den
   Übergangsbedingungen für Nicht-Skill-Träger**; Punkt 4 der Änderungsgrundsätze wird von
   „Skills" auf „jeder Modulträger" erweitert und verweist auf ihn.
4. **`framework/core/08-skill-conventions.md` Abschnitt 7 erhält einen Verweis** auf den
   allgemeinen Teil; die Tabelle dort bleibt die Schärfung für Skills.
5. **Die Standzeile in `docs/ROADMAP.md` wird nachgezogen: Kriterium 3 = 52.**
6. **Kein Nicht-Skill-Träger wird in diesem Release gehoben** – die Bedingung entsteht hier,
   die Abnahme je Träger ist der nächste Vorgang.

## 5. Vorlage zur Entscheidung

Jede Ermessensfrage einzeln, mit Auflösung **und Preis**.

### E1 – Gehen die dreizehn Skills auf `pilot`, obwohl alle 87 Testfälle offen sind?

**Ja.** Das Modell verlangt für `pilot` „Testfälle **vorhanden**"; jeder der dreizehn trägt
mindestens zwei Positiv- und drei Negativtests (gemessen: 29 + 58 = 87). „Bestanden" ist die
Bedingung für `aktiv`, und dort bleibt sie.

**Verworfen:** auf Kriterium 2 warten. Das wäre die falsch gelesene Bedingung aus der
Vorbedingung – sie hätte Kriterium 3 an mehrere Sitzungen und ein Modellkontingent gebunden,
obwohl der Wortlaut des Modells das nicht verlangt.

**Preis, benannt:** `pilot` heißt „Nutzung in Pilotgruppe". Nach diesem Release trägt jeder
Skill des Frameworks diesen Anspruch, **ohne dass ein einziger Sitzungstest gefahren ist**.
Der Anspruch ist durch das Modell gedeckt und durch nichts sonst. Wer ihn für zu stark
hält, muss das **Modell** ändern, nicht diesen Statuswechsel – und das wäre ein eigener
Antrag.

### E2 – Ist der Statuswechsel eine Versionsänderung des Skills?

**Nein.** Weder Version noch `CHANGELOG.md` der dreizehn Skills werden angefasst.

**Begründung:** `08-skill-conventions.md` Abschnitt 7 bindet die Versionsarten an
**Inhalt** (MAJOR: Ausgabeformat oder Scope; MINOR: neue Schritte oder Prüfungen; PATCH:
Korrekturen und Formulierungen) und sagt im nächsten Satz: *„Jede Versionsänderung
erfordert die erneute Ausführung der Testfälle in `TESTS.md`."* Ein Statuswechsel ändert
keine Anweisung – ihn zur Versionsänderung zu erklären würde die erneute Ausführung der
Testfälle auslösen und damit **genau die Kopplung an Kriterium 2 herstellen, die E1 gerade
als nicht bestehend nachgewiesen hat.**

**Verworfen:** PATCH-Anhebung mit Eintrag „Status auf `pilot`". Sie sieht sauber aus und
verlangt nach dem Wortlaut des Modells dreizehn Testreihen, die niemand fahren wird – eine
Zusage ohne Mechanismus, in der Datei, die den Mechanismus beschreibt.

**Preis, benannt:** Der Änderungsverlauf des einzelnen Skills verzeichnet den
Statuswechsel **nicht**. Wer nur `framework/skills/<name>/CHANGELOG.md` liest, sieht ihn
nicht; er steht im Framework-`CHANGELOG.md`, in diesem Antrag und in D-103.

### E3 – Zählregel ändern oder Gegenstand beseitigen (die vier Vorlagen)?

**Gegenstand beseitigen:** Die Statuszelle der vier Vorlagen wird zum Ausfüllschlitz.

**Verworfen:** die Zählregel um eine Ausnahme für Vorlagen erweitern. `CR-2026-070` E6 hat
die Zählung ausdrücklich auf den **ganzen** Bestand gestellt, damit ein Kriterium nicht
klein wird, indem es einen Teil seines Gegenstands nicht ansieht. Eine Ausnahme wäre
dieselbe Bewegung mit umgekehrtem Vorzeichen – und sie hätte die Vorlagen in dem Zustand
gelassen, der den Fehler erzeugt.

**Preis, benannt:** Wer eine Vorlage kopiert und den Schlitz nicht füllt, hat ein Pack ohne
Statuswert. Bei einem Skill fängt das der Validator (`SKILL_STATUS`); **bei Client-, Role-
und Technology-Pack fängt es heute nichts** – siehe E5.

### E4 – Wohin gehören die Übergangsbedingungen der Nicht-Skill-Träger?

**In `framework/core/01-governance.md`, als neuer Abschnitt 5** („Lebenszyklus der
Modulträger"). Dort steht Punkt 4 der Änderungsgrundsätze, der den Lebenszyklus heute für
Skills nennt; dort liegt auch die Rollentabelle mit dem Modul-Owner, der das Review trägt.

**Verworfen:** die Tabelle in `08-skill-conventions.md` Abschnitt 7 auf alle Träger
erweitern. Das ist der **Skill-Standard**; ein Lebenszyklus für Checklisten und
Governance-Dokumente wäre dort unauffindbar, und ein Verweis von der Governance in den
Skill-Standard hätte die Schichtung verdreht.

**Verworfen:** die fünf Statuswerte und ihre Bedeutung in 01 **wiederholen**. Sie stehen in
`08-skill-conventions.md` Abschnitt 7 und werden von dort verwiesen – „eine Quelle, ein
Vokabular" (0.40.0, D-78 bis D-80). Der neue Abschnitt führt nur, was es dort nicht gibt:
die Bedingungen für die Träger, die keine Skills sind.

**Preis, benannt:** Der neue Abschnitt wird **angehängt** (5), nicht an der thematisch
richtigen Stelle eingefügt (nach 3). Grund: `checklists/08-merge-request.md` verweist auf
„`01-governance.md` Abschnitt 4" (Auditierbarkeit); ein Einschub hätte diesen Verweis still
falsch gemacht. **Die Abschnittsfolge ist damit nicht thematisch** – der Vorteil ist, dass
keine bestehende Fundstelle bricht.

### E5 – Wird in diesem Release eine Prüfung gebaut?

**Nein.**

**Begründung:** Der Mensch hat am 2026-09-15 angeordnet, dass das nächste Release wieder
**eine Zahl senkt** und nicht den Prüfapparat vergrößert. Dieses Release senkt Kriterium 3
von 69 auf 52.

Die Prüfung, die fällig **wird**, ist benannt: **Das Statusvokabular ist heute nur in einer
`SKILL.md` durchgesetzt** (`SKILL_STATUS`); für die übrigen 56 Träger wäre `| Status |
banane |` ein zulässiger Wert. **Solange kein Nicht-Skill gehoben ist, hat diese Prüfung
keinen Gegenstand** – dieses Release hebt ausschließlich Skills, und für die greift die
Durchsetzung. Mit dem **ersten** gehobenen Nicht-Skill ist sie fällig, und dann gehört sie
in dasselbe Release.

**Preis, benannt:** Zwischen diesem Release und dem nächsten steht eine normative Regel im
Kern, deren Vokabular für 56 Träger von nichts geprüft wird. Der Antrag sagt es, statt es
zu verschweigen – wie D-101 es eine Woche vorher getan hat.

### E6 – Bekommen die elf Kernmodule eine Statuszeile?

**Nicht in diesem Release; aufgenommen als `K-36`.**

**Der Befund ist echt:** `framework/core/` enthält elf normative Module, **keines** trägt
eine Statuszeile – und `checklists/11-framework-release.md` verlangt unter *Abschluss*:
*„(ab 1.0.0, D-11) Alle **Core-Module**, Skills und Packs tragen einen Status oberhalb von
`entwurf`."* **Das Release-Gate für 1.0.0 verlangt einen Wert, den es an elf Stellen nicht
gibt.**

**Verworfen:** die elf Zeilen hier nachtragen. Kriterium 3 stiege damit von 52 auf **63** –
in einem Vorgang, dessen Auftrag das Senken ist. Das wäre richtig und sähe falsch aus; und
die elf Module sind die normativsten des Bestands, ihre Abnahme ist kein Nebenprodukt.

**Verworfen:** den Prüfpunkt der Checkliste hier umformulieren. Damit wäre die Frage
beantwortet, ohne sie gestellt zu haben.

**Preis, benannt:** Kriterium 3 ist nach diesem Release **um elf Träger zu klein**, und das
steht so im Protokoll und in `K-36`. Die Zahl 52 ist unter der heutigen Zählregel richtig
und unter der Absicht der Release-Checkliste zu niedrig.

### E7 – Wird das Hauptdokument nachgezogen?

**Nein; die Pflicht wird beim P3-Posten „Word-Fassung erzeugen" vermerkt.**

**Der Befund:** `build/doc/20-referenz-skills.md` sagt *„Alle Skills liegen im Status
`entwurf` (Version 0.1.0 …)"*. **Die Versionsangabe ist für alle zwölf falsch** – sie stehen
auf 0.1.1 bis 0.1.4 –, und die Statusangabe wird mit diesem Release falsch. Dasselbe in
`build/doc/00-kopf.md`: *„Alle Module im Status `entwurf`"*.

**Verworfen:** die beiden Sätze berichtigen. Derselbe Steckbrief nennt *Dokumentversion
0.9.0, Stand 2026-09-10*; das Dokument ist **zweiundvierzig Releases** hinter dem Kern. Zwei
Sätze darin nachzuziehen behauptet einen Stand, den das Dokument nicht hat – und es ist die
Lehre von 0.45.0 wörtlich: *„Eine Anweisung, die die halbe Migration beschreibt, ist
gefährlicher als keine."*

**Preis, benannt:** Zwei falsche Sätze bleiben im Repositorium stehen, einer davon wird es
durch dieses Release. Beide stehen in einem Dokument, dessen eigener Steckbrief seinen
Abstand nennt, und beide sind hier und in der Roadmap benannt. **Dass niemand den Abstand
bemerkt hat, liegt daran, dass ihn nichts nachrechnet** – ein Prüfkandidat, und nach E5
nicht dieses Release.

### E8 – Wird die Idee eines mitgelieferten Projekt-Overlays hier entschieden?

**Nein, nur aufgenommen.** Der `<FRAMEWORK_OWNER>` hat am 2026-09-15 angeregt, bei
`install.py` ein **Projekt-Overlay als Parameter** mitgeben zu können – ein Standard-Overlay
statt des leeren, und später weitere, auf Projekttypen zugeschnittene. Ohne Parameter bleibt
es beim leeren Overlay wie bisher.

**Aufgenommen als Abschnitt „Geplant: Projekt-Overlays als Installationsparameter" in
`docs/ROADMAP.md`**, in der Form, die dort für das geplante Client Pack `openai-codex` schon
steht: die **Voraussetzungen vorab**, kein Ziel-Release. Ein eigener Antrag entsteht, wenn
die Fragen dort beantwortet sind.

**Begründung für die Form:** Ein Overlay trägt Projektwerte, und der Kern darf keine
enthalten (Entscheidungsbaum 6, Prüfung 6 und 14). Ein ausgeliefertes Standard-Overlay ist
damit die erste Datei des Frameworks, die Projektwerte **vorschlägt** – die Abgrenzung
gehört geklärt, bevor jemand sie baut. **Und die Nummer dieses Antrags ist keine
Overlay-Nummer:** Ein Antrag, der ein Projekt-Overlay betrifft, gehört in die Nummernfolge
des Projekts, nicht in die des Frameworks – hier geht es um `install.py` und den
Auslieferbestand, also um den Kern.

**Preis, benannt:** Die Idee liegt damit als Absicht im Repositorium, ohne Mechanismus und
ohne Ziel-Release – genau der Zustand, den dieses Projekt sonst misstrauisch betrachtet. Der
Unterschied zu einer Zusage: Ein Abschnitt „Geplant" behauptet nichts über den heutigen
Stand.

## 6. Prüffragen

- [x] **Richtige Ebene nach Entscheidungsbaum 6?** Ja – Core. Gegenstand sind das
      Lebenszyklusmodell und der Status der Kernmodule. Keine Projektwerte.
- [x] **Verschärfungsprinzip eingehalten?** Ja. Ein Statuswechsel `entwurf → pilot` lockert
      keine Regel; V1–V12 und K3 sind nicht berührt. Der neue Abschnitt 5 von
      `01-governance.md` **fügt** eine Bedingung hinzu, wo heute keine steht.
- [x] **Widerspruchsfreiheit geprüft (welche gelesen):** `framework/core/01-governance.md`,
      `framework/core/08-skill-conventions.md` (Abschnitte 2, 4, 7),
      `governance/RELEASE_PROCESS.md` (Abschnitt 1 und Lebenszyklusverweis),
      `checklists/11-framework-release.md`, `governance/DECISION_LOG.md` (D-03, D-08, D-11,
      D-74, D-98 bis D-101), `docs/ROADMAP.md`, `tests/scripts/validate-framework.py`
      (Prüfung 46 und die Skillprüfungen).
- [x] **Laufzeitfassungen betroffen?** Ja, mittelbar: `install.py` bringt jede `SKILL.md` in
      die Frontmatter-Form des gewählten Clients; die Statuszeile steht im **Dateikörper**
      (D-08) und wird unverändert übernommen. **Keine Änderung an einem Client Pack nötig** –
      beide Packs bilden den Status nicht ab, weil er kein Frontmatter-Feld ist. Die lokale
      Testinstallation ist nach dem Patch neu zu erzeugen.
- [x] **Belegstatus korrekt?** Ja. Die drei offenen `VERIFY`-Marker der beiden Skills bleiben
      stehen; dieses Release senkt Kriterium 1 um nichts. Keine neue `[DOK]`-Aussage.
- [x] **Test- und Validierungsbedarf:** Prüfung 46 schlägt zwischen Patch und Nachziehen der
      Standzeile an (erwartet, siehe Wirkungsnachweis). Keine neue Prüfung, keine neue Sonde
      – der Sondenlauf muss unverändert grün bleiben, **und das ist hier der Messwert**:
      Sonde 46f präpariert einen Statuswert im Decision Log, nicht in einer `SKILL.md`.
- [x] **Auswirkungen auf Overlays und laufende Onboardings; Migrationshinweis nötig?**
      Kein Overlay-Feld betroffen. **Migrationshinweis ja, und er ist kurz:** Wer eine
      Installation aktualisiert, bekommt dreizehn Skills mit Status `pilot`; ein Projekt,
      das eigene `prj-*`-Skills führt, ist nicht betroffen. Wer eine Vorlage kopiert, füllt
      künftig die Statuszelle aus.
- [x] **Dokumentation:** CHANGELOG, Decision Log (D-102 bis D-104, K-36, K-37), Roadmap
      (Standzeile, Kriterientabelle, AP3, P3-Posten, neuer Abschnitt „Geplant"), zwei
      Protokolle.

## 7. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** (E1 bis E8) |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Die Vorbedingung, die den Vorgang aufhalten sollte, hält in zwei von drei Punkten nicht: Der erste Übergang der dreizehn Skills verlangt weder einen bestandenen Test noch eine neue Bedingung, und vier der 69 Träger sind Formulare, mit denen das Kriterium unerreichbar wäre. Was übrig bleibt – die fehlende Bedingung für 52 Nicht-Skill-Träger – wird hier niedergeschrieben und **nicht** angewendet: Die Abnahme je Träger ist nicht maschinell und gehört in den nächsten Vorgang. **Kriterium 3: 69 → 52** |
| Ziel-Release | **0.50.0** |
| Decision-Log-Eintrag | **D-102** (Lebenszyklus für jeden Modulträger), **D-103** (dreizehn Skills auf `pilot`, ohne Versionswechsel), **D-104** (Vorlagen tragen keinen Statuswert); Klärungspunkte **K-36** (Statuszeile der elf Kernmodule), **K-37** (eigene Steckbriefwerte einer Vorlage) |

## 8. Umsetzung

- [x] Änderung umgesetzt (Branch `feature/modulstatus-heben`, PR `#60`)
- [x] Validator ohne Fehler und ohne Warnungen; Sondenlauf in beiden Kodierungsumgebungen
      zeilengleich
- [x] Laufzeitfassungen: keine Änderung nötig; lokale Testinstallation neu erzeugt
- [x] CHANGELOG und Decision Log ergänzt
- [x] Standzeile in `docs/ROADMAP.md` auf Kriterium 3 = 52 nachgezogen
- [x] Kommunikation an Projekte: Migrationshinweis im CHANGELOG; Pilot und
      Übungsrepositorium auf 0.50.0 gehoben
- [ ] **Zur Entscheidung offen, mit dem nächsten Vorgang:** `K-36` (Statuszeile der elf
      Kernmodule – Kriterium 3 ist bis dahin um elf Träger zu klein) und `K-37` (eigene
      Steckbriefwerte einer Vorlage, insbesondere die Versionszelle)
- [ ] **Fällig mit dem ersten gehobenen Nicht-Skill-Träger:** die Prüfung auf das
      Statusvokabular aller Träger (E5). Heute ohne Gegenstand, ab dann nicht mehr
