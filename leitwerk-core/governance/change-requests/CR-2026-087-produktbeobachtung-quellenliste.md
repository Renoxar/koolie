# Änderungsantrag `CR-2026-087`

| Feld | Inhalt |
|---|---|
| Titel | Die Quellenliste gegen die Wirklichkeit – `FW-AK-01` gefahren, dreizehn Befunde, und zwei Anweisungsquellen, von denen nur eine abschaltbar ist |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-18 |
| Betroffene Artefakte | `clients/claude-code/CLIENT_PACK.md` (Steckbrief, `R5`, `S4`, `S5`, `X1`, `X2`, Abschnitt 8a, Änderungsverlauf), `clients/claude-code/manifest.json` (`settings_extra`), `clients/devin-desktop/CLIENT_PACK.md` (Steckbrief, Pfadabbildung, `R1`, `R4`, `M2`, `X1`, `X2`, Änderungsverlauf), `clients/devin-desktop/manifest.json` (`settings_extra` leer, deklariert), `clientmap.py` (Abbildung der obersten Ebene), `build/doc/31-anhaenge.md` (31.4, 31.4.1 bis 31.4.3, `QC-6`), `tests/TEST_CATALOG.md` (`FW-AK-01`, Sondenmenge), `tests/scripts/validate-framework.py` (**Prüfung 54**, Kopfkommentar), `tests/scripts/probe-pruefungen.py` (vier Sonden, drei Gegenproben), `governance/DECISION_LOG.md` (D-154 bis D-159, `K-62` bis `K-65`), `docs/ROADMAP.md` (Releaseplan, Standzeile), `tests/protocols/2026-09-18-FW-AK-01.md`, `CHANGELOG.md`, `VERSION` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind zwei Client Packs, die Abbildungsschicht, der Testkatalog und der Prüfapparat |
| Art | Produktbeobachtung (`FW-AK-01`), Befundbehebung, eine neue Prüfung, ein aufgelöster VERIFY-Marker |
| Dringlichkeit | **Regulär, mit einem Vorbehalt.** Kein Sicherheitsvorfall im eigenen Bestand – aber zwei Befunde betreffen **Anweisungs- und Skillquellen außerhalb des Repositoriums, die standardmäßig eingeschaltet sind**, und einer betrifft eine Zusage, die in der verbindlichen Zielspanne eines Packs nachweislich nicht galt (CVE-2026-81376) |

## 1. Anlass

**`FW-AK-01` ist gefahren, zum ersten Mal vollständig, und er hat kein Kontingent
gekostet.** Die Zelle stand seit 0.16.0 halb geführt: Teil `claude-code` mit
Recherchestand 10.09.2026 gegen 2.1.267, Teil `devin-desktop` **gar nicht** – dort war
seit dem 02.09.2026 kein Changelog gesichtet.

**Der Anlass, sie jetzt zu fahren, ist dieselbe Lehre, die 0.61.0 an `FW-KO-05` gezogen
hat:** Sie trägt Prüfmittel **`review`**, nicht `sitzung`. *`sitzung` heißt teuer, `review`
heißt jetzt.* Der Releaseplan führte beide Zellen im Bündel des fünften Sitzungstests und
wies seit 0.61.0 darauf hin, dass sie kein Kontingent brauchen.

> 🟢 **Zwei `review`-Zellen in zwei Releases, zusammen siebzehn Befunde, zusammen kein
> Kontingent.** Wer ein Testbündel plant, trennt zuerst nach Prüfmittel.

**Der Umfang:** 22 Quellen (17 `QD`, 5 `QC`) und beide Produkt-Changelogs –
`devin-desktop` von 3.8.20 bis **3.10.31**, `claude-code` von 2.1.268 bis **2.1.275**.
**Zwölf Quellen tragen ihren zugeschriebenen Beleg unverändert, zehn nicht.** Daraus
**dreizehn Befunde**; das Protokoll führt sie als `B1` bis `B13`
(`tests/protocols/2026-09-18-FW-AK-01.md`).

## 2. B1: Eine Skillquelle des Kontos, standardmäßig an – und die Abhilfe ist in genau der ausgelieferten Datei unwirksam

`QC-3` sagt seit Clientversion 2.1.275 wörtlich **„This is enabled by default."** Der
Client lädt die im Konto eingeschalteten Skills nach `~/.claude/skills/synced/` und
gleicht sie **während** der Sitzung etwa alle zehn Minuten ab.

**Der Befund ist nicht die Quelle, sondern die Stelle, an der sie abzuschalten wäre.**
`QC-5` führt eine Tabelle der Vorrangausnahmen; für `syncClaudeAiSkills` steht dort, der
Wert `false` werde aus verwalteten Einstellungen, aus `--settings`, aus der Benutzerdatei
und aus der unversionierten Projektdatei geehrt – **„a `false` in `.claude/settings.json`
is ignored"**.

🔴 **`.claude/settings.json` ist der `permissions_file` dieses Packs.** Von den vier
Ebenen, aus denen der Schalter wirkt, ist keine eine, in die das Framework versioniert
schreiben kann.

➡️ 🆕 **Neue Bauform für den Befundkatalog: die Abhilfe, die in genau der ausgelieferten
Datei unwirksam ist.** Sie ist die schärfere Verwandte der *Zusage, die mehr verspricht als
ihr Mechanismus hält*: Der Mechanismus existiert, ist dokumentiert und eine Zeile lang –
und die Ebene, auf der das Framework arbeitet, ist die einzige ausgenommene. **Wer eine
Abhilfe findet, prüft, aus welcher Ebene sie wirkt, bevor er sie einplant.**

Ohne `QC-5` hätte das Framework den Schlüssel ausgeliefert, **der Validator hätte ihn
bestätigt**, und er hätte nichts getan.

## 3. B2: Eine zweite Anweisungsquelle, die der Client sich selbst schreibt – und diese ist lieferbar

`QC-1` führt unter *Auto memory* einen Mechanismus, den die Fassung von 2.1.267 nicht
hatte: Der Client schreibt sich selbst Notizen unter
`~/.claude/projects/<projekt>/memory/` und lädt den Index `MEMORY.md` mit den ersten 200
Zeilen beziehungsweise 25 KB **in jede Sitzung**. Wörtlich: **„Auto memory is on by
default."**

**Damit stünde in jeder Sitzung ein Anweisungstext, den die Prioritätshierarchie nicht
kennt, der Validator nicht sieht und kein Review erreicht** – weder versioniert noch
gegengezeichnet. Für genau diesen Gegenstand gibt es die Ebenen 1 bis 6.

🟢 **`autoMemoryEnabled` steht in keiner Vorrangausnahme**, gilt also nach gewöhnlichem
Vorrang, und die Quelle nennt die Projektdatei ausdrücklich als Ort. **Das Framework
liefert den Schlüssel aus** – als Standard, nicht als Schranke: `.claude/settings.local.json`
hat höheren Vorrang, ein Projekt kann die Quelle zurückholen und weist die Abweichung aus.

> 🔴 **Der Vergleich B1 gegen B2 ist der Ertrag dieses Durchgangs.** Zwei Quellen außerhalb
> des Repositoriums, beide standardmäßig an, beide mit einem dokumentierten
> Ein-Zeilen-Schalter – **die eine ist lieferbar, die andere nicht, und der Unterschied
> steht in einer Tabelle, die man gelesen haben muss.**

**Und die Abhilfe brauchte einen Mechanismus, den es nicht gab:** `permissions_extra`
landet **innerhalb** von `permissions`; `autoMemoryEnabled` gehört auf die **oberste**
Ebene. Dafür ist `settings_extra` neu (Abschnitt 5).

> 🔴 **UND DER TROCKENLAUF HAT DIE REICHWEITE DIESER ABHILFE EINGESCHRÄNKT – ZUM DRITTEN
> MAL IN VIER RELEASES WIRFT ER EINEN MIGRATIONSHINWEIS UM.** `install.py --update`
> führt `.claude/settings.json` unter *Projektdateien unberührt gelassen* – die Datei
> trägt Projektwerte und wird von einem Update **nie** überschrieben. **Der Schlüssel
> erreicht damit jede Erstinstallation und kein bestehendes Projekt.** Gemessen am
> 2026-09-18 gegen eine Kopie beider übernehmender Projekte, mit dem `leitwerk-core` des
> Arbeitsbaums: `otp-generator` **6 Dateien aktualisiert, `settings.json` nicht darunter**;
> `test-devin-framework` 1 Datei, und dieses Pack führt `settings_extra` ohnehin leer.
> ➡️ **Das ist dieselbe Bauform wie B1, eine Ebene tiefer:** Die Abhilfe ist lieferbar –
> aber nur an einen Empfänger, den es bei einem bestehenden Projekt nicht mehr gibt.
> **Wer ein Projekt hebt, trägt die Zeile von Hand nach**; der Migrationshinweis sagt es,
> wie 0.33.0 es für die Domainzeile gesagt hat.

## 4. B7 und B9: Zwei Befunde am Pack `devin-desktop`, die ohne den Changelog nicht entstanden wären

**B7 – drei von siebzehn Quellen belegen einen entfernten Agenten.** Changelog zu 3.9.19
(08.09.2026): *„Cascade has been removed. Devin Local is now the only agent available in
Devin Desktop."* `QD-5`, `QD-7` und `QD-8` liegen unter `desktop/cascade/` und sprechen
weiter im Präsens von ihm. **Die Seiten sind erreichbar und inhaltlich unverändert** –
veraltet ist nicht ihr Text, sondern wofür sie taugen.

🔴 **Die schärfste Stelle ist `QD-5`, weil Zeile `R1` daran hängt** – die tragendste
Regelladungszusage dieses Packs. 🟢 **Und hier wurde der Befund beim Messen kleiner und
schärfer:** Der tragfähige Beleg stand daneben und war nicht genannt – `QD-6` führt
`AGENTS.md` als Regeldatei **ohne Bindung an einen Agenten**. Die Abhilfe ist deshalb
nicht, eine Zusage aufzugeben, sondern einen vorhandenen Beleg dorthin zu stellen, wo die
Einstufung steht. Dieselbe Bewegung wie bei 0.55.0.

**B9 – eine Aussage der Liste ist in der Zielspanne des Packs widerlegt.** Changelog zu
3.10.31 (16.09.2026): *„Restricted Mode blocks restricted workspace settings written in
nested object form, **not just the dotted form** (CVE-2026-81376)."* `QD-12` sagt
unverändert *„Organization-level (enterprise) settings can **never** be overridden"*, nennt
den Restricted Mode mit keinem Wort und verwendet in seinen Beispielen die verschachtelte
Form. **Zeile `M2` stützt sich genau darauf, und die Zielspanne `3.9.x` liegt vollständig
vor der Behebung.**

➡️ **Es ist dieselbe Regel in zwei Ausdrucksformen, durchgesetzt nur in einer** – die
Bauform von D-150, hier im Produkt statt im eigenen Bestand.

> 🔴 **Beide Befunde wären bei einem Abgleich Seite gegen Seite herausgefallen.** `QD-5`,
> `QD-7`, `QD-8` und `QD-12` sind Wort für Wort unverändert. **Deshalb musste vor dem
> Abgleich festgelegt werden, wann eine Quelle als abweichend zählt** – siehe E1.

## 5. B13: Der Befund, der die Liste selbst trifft

Anhang 31.4 sagte über sich selbst: *„Dort nennt die Belegspalte **je Zeile** die Seite,
auf die sie sich stützt."*

| Pack | Matrixzeilen | davon `[DOK]` | davon mit genannter Quelle |
|---|---|---|---|
| `devin-desktop` | 36 | **20** | **4** |
| `claude-code` | 32 | **23** | **10** |
| **zusammen** | **68** | **43** | **14** |

**Die Zusage trifft für 14 von 43 Zeilen zu** – der wiederkehrende Befundtyp in seiner
Grundform.

🟢 **Die Gegenprobe steht im eigenen Bestand:** Das Pack `claude-code` sagt dasselbe
**eingeschränkt** (*„Wo eine Zeile mit AP2 belegt ist"*) und ist damit wahr. **Die
unbedingte Fassung stand im Anhang, die bedingte im Pack, und nur eine von beiden traf
zu.** ➡️ **Wer zwei Fassungen derselben Zusage hat, prüft die unbedingte.**

🔴 **Der Preis ist an diesem Durchgang gemessen:** Weil die Zuordnung fehlt, mussten **alle
22 Quellen** abgerufen werden – es war nicht zu sagen, welche Seite welche Zusage trägt.
**Eine Quellenliste ohne Zuordnung je Zeile macht ihre eigene Wiederholungsprüfung so teuer
wie die erste**, und `FW-AK-01` verlangt sie *laufend*.

## 6. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | **Wann zählt eine Quelle als *abweichend*?** | **Wenn sie den ihr zugeschriebenen Beleg nicht mehr unverändert trägt** – gleich ob die Seite sich geändert hat, ihr Gegenstand im Produkt entfallen ist, **oder der Produkt-Changelog ihre Aussage widerlegt** | **Die dritte Alternative ist Ermessen und musste vor dem Abgleich festgelegt werden.** Ohne sie wären B7 und B9 herausgefallen: Alle vier betroffenen Seiten sind Wort für Wort unverändert. **Der Preis der Gegenseite ist höher als der der Regel:** Ein Abgleich Seite gegen Seite hätte zehn Abweichungen als vier gezählt |
| **E2** | **Was tritt an die Stelle der Zusage, die B1 nicht mehr trägt?** | **Die Zusage wird eingeschränkt und der Kanal benannt** – in `X1` als Grenze, in `S4` und `S5` als Reichweitenverlust. `K-63` hält die Frage offen | **Das kostet nichts und schützt nichts, und es ist als einziger Weg wahr.** Die beiden Alternativen beschädigen das Framework an anderer Stelle: die unversionierte Projektdatei mitliefern hieße eine Datei ausliefern, die das Framework nicht versionieren kann; eine Installationswarnung ist die Bauform, die `FRAMEWORK_DEV_PROFILE.md` Abschnitt 5 ablehnt – **und sie erschiene in jeder Installation** |
| **E3** | **Wird die selbstgeschriebene Anweisungsquelle (B2) abgeschaltet?** | **Ja, `autoMemoryEnabled: false` in der erzeugten Einstellungsdatei** (D-154) | **Es ist eine Verschärfung, die in jede Installation geht.** Sie ist aber ein **Standard**, keine Schranke: `.claude/settings.local.json` hat höheren Vorrang. **Der Gegenpreis wäre schwerer** – ein Anweisungstext in jeder Sitzung, den die Prioritätshierarchie nicht kennt und den D-34 nicht auskunftsfähig macht |
| **E4** | **Wie kommt der Schlüssel auf die richtige Ebene?** | **Neues Manifestfeld `settings_extra`** für die oberste Ebene, neben `permissions_extra` für das Objekt `permissions`. **Beide sind Pflicht, notfalls leer** (D-155) | **Ein Feld mehr je Pack.** Die Alternative – `permissions_extra` verallgemeinern – ließe den Schlüsselnamen über die Ebene entscheiden, und ein Tippfehler wäre eine **stille Verlagerung**. **Die Pflicht auch bei leerem Wert** kostet eine Zeile und trennt die ausdrückliche Abwesenheit von der Lücke; ohne sie wäre `devin-desktop` nicht von einem vergessenen Pack zu unterscheiden |
| **E5** | **Bekommt der Befund eine Prüfung?** | **Ja, Prüfung 54:** Jeder deklarierte Zusatzschlüssel steht in der erzeugten Datei auf **seiner** Ebene und mit **seinem** Wert | 🔴 **Der Anlass ist eine fremde Messung, keine eigene** – CVE-2026-81376 beim Schwesterclient. **Was sie nicht leistet:** Sie prüft, ob ein deklarierter Schlüssel ankommt, nicht ob er der richtige ist. Ob `autoMemoryEnabled` der Schlüssel ist, den der Client liest, sagt die Herstellerdokumentation – **dafür gibt es `FW-AK-01`, nicht den Validator** |
| **E6** | **Werden die 29 Zeilen ohne Quellenangabe (B13) in diesem Release nachgetragen?** (nach dem Eingriff **26 von 44** – fünf haben ihre Quelle bekommen, weil der Abgleich sie gelesen hat) | **Nein.** Berichtigt wird die **Aussage** des Anhangs; die Lücke wird als `K-62` geführt und bekommt einen **eigenen Posten** im Releaseplan (`~0.65.0`, D-156) | 🔴 **Eine Zuordnung, die niemand belegt hat, sähe wie ein Beleg aus** – genau der Befundtyp, gegen den die Zeile gebaut ist. **Der Preis der Vertagung ist benannt und wiederkehrend:** Jede Wiederholung von `FW-AK-01` kostet bis dahin denselben vollständigen Durchgang wie dieser |
| **E7** | **Wird die verbindliche Zielspanne von `devin-desktop` auf `3.10.x` gehoben?** | **Nein** (D-157). Die Spanne bleibt `3.9.x`; der **Abstand zum ausgelieferten Produkt** wird im Steckbrief benannt | **Das Pack bleibt sichtbar hinter dem Produkt**, und das ist der Punkt: Die Spanne ist der *geprüfte* Geltungsbereich. Sie zu heben ohne Messung wäre eine Zusage ohne Messung – **und D-113 hat die Spanne gerade deshalb eingeführt**. ⚠️ **`K-40` kann diesen Fall nicht fangen:** Der aktuelle Produktstand steht in keiner Datei dieses Repositoriums |
| **E8** | **Wird `FW-AK-01` abgenommen?** | **Ja, `bestanden`** – Kriterium 2: 93 → 92 | **Der Erwartungswert lautet *„Abweichungen als CR erfasst; VERIFY-Marker gepflegt"*, und beides ist geschehen.** Das unzulässige Ergebnis lautet *„veraltete Aussagen als Tatsache"* – keine steht mehr. 🔴 **Der Preis ist benannt:** Vier Befunde bleiben als Klärungspunkte offen, weil ihr Gegenstand außerhalb der Reichweite des Frameworks liegt. **Ein offener Klärungspunkt ist kein unzulässiges Ergebnis dieser Zelle** – sonst wäre sie nie abnehmbar, solange irgendein Hersteller etwas ändert. **Und das `bestanden` altert ab dem Abnahmetag** (`K-61`-Bauform) |
| **E9** | **Wie trägt der Releaseplan die Verschiebung?** | **Dieses Release wird `0.62.0`, Sitzungstest 5 wandert auf `0.63.0` mit `92 → 85`, die Testblätter auf `0.64.0 bis ~0.68.0` mit `85 → 0`**, dazu der neue Posten `~0.65.0` für `K-62` | **Die exakten Nummern verschieben sich zum dritten Mal in drei Releases.** Dieselbe Entscheidung wie `CR-2026-086` E7 und `CR-2026-085` E6: exakte Nummern wandern, geschätzte nicht. 🟢 **Prüfung 53 rechnet die Kette jetzt nach** – sie ist mit 0.61.0 genau für diesen Vorgang gebaut worden und hat ihn beim ersten Anwendungsfall begleitet |
| **E10** | **Was wird aus dem aufgelösten Marker auf `R5`?** | **Die Zeile geht auf `[DOK]` mit zwei benannten Grenzen** (D-158): Die Nutzlast des Hooks ist nicht dokumentiert, und gemessen ist keiner der beiden Wege | **Sie geht nicht auf `[TECHNISCH]`.** Ein Dokumentenabgleich belegt `[DOK]`, nie eine beobachtete Wirkung (D-12). **Die Gegenseite wäre, den Marker stehen zu lassen, bis der Weg gemessen ist** – dann verlangte er mehr, als sein eigener Wortlaut fordert: die Bauform *„eine Bedingung, die mehr verlangt als ihr Kriterium"* |

## 7. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle zehn Fragen wie vorgelegt.** |
| Datum | 2026-09-18 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | **D-154** (die selbstgeschriebene Anweisungsquelle wird abgeschaltet), **D-155** (`settings_extra`, Prüfung 54), **D-156** (eine Quellenliste sagt, was sie leistet), **D-157** (die Zielspanne wird nicht mitgezogen), **D-158** (der VERIFY-Marker auf `R5` ist aufgelöst), **D-159** (die Quellenliste führt jede benutzte Seite; `QC-6`) |
| Neue Klärungspunkte | `K-62` (29 von 43 `[DOK]`-Zeilen ohne Quellenangabe, nach dem Eingriff 26 von 44), `K-63` (Kontoquelle der Skills, aus der ausgelieferten Datei nicht abschaltbar), `K-64` (organisationsseitige Skillquelle), `K-65` (der Schalter für fremde Agentenprotokolle ist entfallen) |
| Auflagen | **Wer eine Abhilfe findet, prüft, aus welcher Ebene sie wirkt, bevor er sie einplant.** Und: **Wer eine Quelle abgleicht, hält sie gegen den Changelog, nicht nur gegen ihre eigene Vorfassung** – eine unveränderte Seite kann widerlegt sein |
| Ziel-Release | `0.62.0` |
| Umsetzung | umgesetzt mit `0.62.0` |

## 8. Abnahme

- Validator `0 Fehler, 0 Warnungen`, **beide Kodierungsumgebungen**.
- Sondenlauf: **vier neue Sonden** (`54a` auf der Kopie des Repositoriums, `54b` bis `54d`
  an einer `claude-code`-Installation) und **drei neue Gegenproben** (`54a` bis `54c`);
  Spanne `6, 14 und 18 bis 54` in allen drei Trägern **ausgerechnet**, nicht gepflegt.
- 🔴 **Der Zuschnitt musste geteilt werden, und das ist `B02` in klein.** Die
  Testinstallation dieses Repositoriums ist `devin-desktop`, und dieses Pack führt
  `settings_extra` **absichtlich leer**; eine Sonde auf der Kopie belegt deshalb nur die
  Deklarationspflicht. **Wert und Ebene sind nur an einer `claude-code`-Installation zu
  messen.**
- **Die wichtigere Hälfte ist Gegenprobe `54b`:** Ein **leeres** `settings_extra` bleibt
  zulässig. Ohne sie stünde nur fest, dass die Prüfung ein fehlendes Feld meldet – nicht,
  dass sie die ausdrückliche Abwesenheit von der Lücke unterscheidet, und genau das ist
  ihr Zweck.
- **Drei Prüfungen haben gegen diese Änderung gemeldet, bevor sie fertig war:** Prüfung 46
  (`gezählt 22, die Standzeile nennt 23` – **zum neunten Mal und wieder gegen einen
  Fortschritt**), Prüfung 50 (`K-63` und `K-64` standen in den Manifesten, bevor sie im
  Register standen) und Prüfung 40 (die Sondenmenge nannte `18 bis 53`, während Prüfung 54
  bereits lief – *erst die Sonde, dann die Spanne*).
- **Trockenlauf gegen beide übernehmenden Projekte** mit dem `leitwerk-core` des
  **Arbeitsbaums**, nicht aus `git archive HEAD` (D-155 ist eine Änderung an einem
  ausgelieferten Träger – eine Null wäre hier eine Null durch Konstruktion gewesen).
- ⚠️ **Zwei eigene Zahlen sind vor dem Festschreiben berichtigt worden:** die Zahl der
  abweichenden Quellen (neun statt zehn – `QD-12` war herausgefallen, weil die Seite
  unverändert ist, also genau der Fall, für den E1 die Regel aufstellt) und zwei
  Sondenkennungen, die beide `54a` hießen.
