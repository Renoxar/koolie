# Änderungsantrag `CR-2026-128`

| Feld | Inhalt |
|---|---|
| Titel | Der Freigabelauf `1.0.0` – und das erste Glied der Nachweiskette, das nie existiert hat |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-23 |
| Betroffene Artefakte | `.gitattributes` (neu); `.koolie/core/tests/scripts/validate-framework.py` (**Prüfung 81** neu, **Prüfung 78** erweitert); `.koolie/core/tests/scripts/probe-pruefungen.py`; `.koolie/core/governance/RELEASE_PROCESS.md`; `.koolie/core/governance/ADOPTION_REGISTRY.md` (neu); `.koolie/core/LICENSE-HINWEIS.md`; `.koolie/core/governance/DECISION_LOG.md`; `.koolie/core/docs/ROADMAP.md`; `.koolie/core/build/doc/00-kopf.md`, `26-qs-test.md`; `.koolie/core/VERSION`; `.koolie/core/CHANGELOG.md`; `UEBERGABE.md` |
| Ebene laut Entscheidungsbaum 6 | Governance und Prüfapparat |
| Art | Freigabelauf `AP12` mit vierzehn Befunden – elf aus dem Vorbedingungsdurchgang, drei aus der Umsetzung |
| Dringlichkeit | **Vorbedingung für `1.0.0`** |
| Status | 🟢 **entschieden am 2026-09-23** (E1 bis E10), umgesetzt mit `1.0.0` |

---

## 1. Anlass

`AP11` ist mit `0.91.0` abgeschlossen. Der Posten ist der **Freigabelauf nach
`checklists/11-framework-release.md`**. Die Vorbereitung dafür liegt seit `0.90.0` vor
(`tests/protocols/2026-09-23-freigabelauf-1.0.0-vorbereitung.md`) und nennt drei Punkte,
die einen Menschen brauchen.

**Der Vorbedingungsdurchgang hat elf Befunde geliefert, und der erste widerlegt den
Prüfkandidaten, mit dem die Übergabe in diese Sitzung geht. Ein zwölfter ist bei der
Umsetzung gefallen, zwei weitere beim Heben der übernehmenden Projekte.** Das ist der achtzehnte
Durchgang in Folge, bei dem die Vorbedingungen der billigste Befund waren.

---

## 2. Die vierzehn Befunde, gemessen

### B1 🔴 Die Zeilenendeform ist am falschen Gegenstand gemessen – und der Kandidat ist `K-81`

Die Übergabe zu `0.91.0` führt als neuen Prüfkandidaten:

> *„KEIN VERSIONIERTER TEXTTRÄGER TRÄGT REINE LF-ZEILENENDEN. Der Bestand ist CRLF."*

**Gemessen am 2026-09-23 über alle 517 verfolgten Einträge:**

| Gegenstand | reines CRLF | reines LF | gemischt |
|---|---|---|---|
| **Arbeitsbaum** (was der Editor sieht) | **515** | 0 | 0 |
| **Blob** (was git speichert – das Versionierte) | 0 | **515** | 0 |

➡️ ***Versioniert ist der Blob, nicht der Arbeitsbaum.*** Die Aussage ist an dem einen
Gegenstand richtig und am anderen in ihr Gegenteil verkehrt. Die Ursache ist
`core.autocrlf=true` – und die steht in der **System**-Konfiguration dieses Arbeitsplatzes
(`C:/Program Files/Git/etc/gitconfig`), **nicht im Repositorium**.

🔴 **Und das ist kein neuer Kandidat: Es ist `K-81`, offen seit `0.78.2`** – *„Welche
Zeilenende-Form gilt im Repositorium, und wer setzt sie durch? `core.autocrlf` ist eine
Einstellung des Arbeitsplatzes, nicht des Repositoriums."* Der Klärungspunkt beschreibt den
Befund wörtlich, ist **dreizehn Releases alt** und trägt seine eigene Sperre: *„nicht vor
dem Meßtag von Bündel 4, weil `git archive` die Meßbäume baut."*

🟢 **Die Sperre ist entfallen.** Die Meßtage von Bündel 4 und 5 sind gefahren (`0.80.0`,
`0.83.0`, `0.84.0`), `AP2` ist zu Ende (`0.86.0`). Und `git archive` ist ab diesem Release
nicht mehr das Werkzeug der Meßbäume, sondern **das Werkzeug der Lieferung** (B2) – aus
einem Grund, vertagt zu bleiben, ist ein Grund geworden, jetzt entschieden zu werden.

### B2 🔴 Null Tags – das erste Glied der Nachweiskette hat nie existiert

`FW-CL-11` verlangt als **MUSS** bei **jedem** Release: *„Release-Archiv erzeugt und
abgelegt."* `RELEASE_PROCESS.md` Abschnitt 1 Punkt 3: *„Jede Auslieferung erfolgt als
Release-Archiv mit Stand aus dem Framework-Repository; Projekte übernehmen nur Releases,
keine Zwischenstände."* Abschnitt 8 beginnt die Nachweiskette mit *„Framework-Version
(`VERSION`, Release-Archiv)"*.

**Gemessen:** `git tag` liefert **null**, lokal und auf dem Server. **In 106
Release-Commits ist kein Archiv erzeugt worden.**

➡️ *Eine Nachweiskette, deren erstes Glied fehlt, ist eine Aufzählung.* Und `K-107` fragt
nach einem **signierten** Tag – es gibt keinen unsignierten, gegen den die Frage stünde.

### B3 🔴 Die Bestandsliste gibt es nicht

`RELEASE_PROCESS.md` Abschnitt 4 Punkt 4: *„der Framework Owner führt eine Bestandsliste
der Projekte mit eingesetzter Version (Auditierbarkeit)."* `AP12` führt *„Bestandsliste
initialisieren"* als Aktivität. **Gemessen: kein Träger dieses Namens im Bestand.**

### B4 ⚠️ Der Prüfpunkt Aktualitätsprüfung hat einen Beleg, den die Vorbereitung nicht gesucht hat

Die Vorbereitung stellt den Prüfpunkt auf 🔴 *„Braucht einen Menschen"*. **Gemessen:
`FW-AK-01` ist am 2026-09-18 vollständig gefahren** – 22 Quellen (17 `QD`, 5 `QC`),
**beide** Produkt-Changelogs (`devin-desktop` bis 3.10.31, `claude-code` bis 2.1.275),
dreizehn Befunde, sämtlich als `CR-2026-087` erfaßt.

➡️ *Ein Prüfpunkt, dessen Beleg fünf Tage alt im eigenen Protokollordner liegt, ist nicht
ungedeckt – er ist ungesucht.* Was bleibt, ist die **Frist**, und die gehört benannt.

### B5 ⚠️ Die Checkliste hat 24 Prüfpunkte, nicht 22

Die Vorbereitung nennt *„Version `0.2.3`, 22 Prüfpunkte"* und **listet 23**. Die Übergabe
übernimmt die 22. **Gemessen an `checklists/11-framework-release.md` (Version `0.3.0`):
24 – 22 MUSS und 2 SOLL.** Mit Prüfung 80 ist einer hinzugekommen; die Differenz davor war
schon da.

### B6 🔴 Der Klarname steht in 122 Merge-Commits des Servers – und die Adresse unter beiden Namen

`K-107` (b): *„Die Historie führt den Klarnamen des Owners und seine Adresse in 109
Releases rückwirkend."* **Gemessen über alle 261 Commits:**

| Gegenstand | Zahl |
|---|---|
| Release-Commits | **106**, nicht 109 |
| Commits mit Klarnamen | **122** – und **alle 122 sind Merge-Commits**, die der Gitea-Server erzeugt |
| Commits unter dem Pseudonym | **139** – **kein einziger Merge**, alle lokal gesetzt |
| Fundstellen des Klarnamens im **Dateibestand** | **null** |
| Commits mit der Adresse | **261** – unter **beiden** Namen |

➡️ ***Das Pseudonym anonymisiert nicht.*** Es trägt dieselbe Adresse, und die Adresse ist
die Verbindung. 🔴 **Und die Quelle des Klarnamens ist das Gitea-Profil, nicht
`git config`** – wer ihn aus künftigen Merges halten will, greift dort zu und nicht am
Arbeitsplatz.

### B7 ⚠️ Beide übernehmenden Projekte stehen drei Releases zurück

**Gemessen:** `devpacks/otp-generator` und `devpacks/test-devin-framework` führen beide
`0.88.0`. Kriterium 5 von D-11 gilt als erfüllt – **sein Nachweis ist drei Releases alt.**
⚠️ Die Vorbedingungsliste der Übergabe nennt für das Übungsrepositorium `0.82.0`; auch das
ist überholt.

### B8 🔴 Der Copyright-Vermerk nennt einen Platzhalter

`LICENSE-HINWEIS.md`: *„Copyright © 2026 `<FRAMEWORK_OWNER>`"*. Mit der Entscheidung für
GPL-3.0 (D-316) träte ein Werk **ohne benannten Rechteinhaber** an die Öffentlichkeit –
während die Historie den Namen in 122 Commits trägt.

➡️ *Der Name steht dort, wo er niemandem nützt, und fehlt dort, wo er rechtlich wirkt.*

### B9 🔴 Zwei Zählungen desselben Gegenstands, beide im Prüfapparat

Der Kopfkommentar von `probe-pruefungen.py` definiert: *„Die kleinste Einheit ist die
Sonde, die Gegenprobe oder – wo mehrere Fälle aufeinander aufbauen – das **Bündel**, nie
einer seiner Teile."*

| Zählung | Zahl | Wer sie führt |
|---|---|---|
| angemeldete **Einheiten** (ein Bündel zählt einmal) | **321** | Selbstprobe `B1` |
| **Ergebniszeilen** (264 Sonden + 154 Gegenproben + 23 Selbstproben) | **441** | die Abnahmezeile der Übergabe |

**Beide stehen im selben Lauf, keine ist falsch** – und der Apparat reserviert das Wort
*Einheit* für die eine, während die Übergabe es für die andere benutzt. 🔴 **Das ist
`K-100` an einem zweiten Gegenstand:** zwei Zählformen, kein Vokabular.

### B10 ⚠️ `1.0.0` ändert das Versionierungsregime, und niemand hat es ausgewiesen

`RELEASE_PROCESS.md` Abschnitt 1 Punkt 1: *„Solange die Hauptversion 0 ist, gilt die
MAJOR-Regel nicht … **Ab `1.0.0` gilt die Regel oben unverändert.**"*

**Ab diesem Release ist jede Struktur- oder Hierarchieänderung, die Overlays anpassen muß,
ein MAJOR-Release.** Das ist eine Folge des Releases selbst, sie steht in keinem Plan, und
sie trifft als erstes die Posten, die nach `1.0.0` anstehen.

### B11 🔴 Die Abnahmezeile der Übergabe steht zum VIERTEN Mal auf einem überholten Stand

`UEBERGABE.md` nennt *„Der Prüfapparat steht bei **76** … **424 Einheiten**"*. **Gemessen:
80 Prüfungen, 441 Ergebniszeilen.** Die Zeile trägt daneben die Lehre aus ihrem dritten
Vorkommen: *„Eine Zahl, die gepflegt werden muß, wird nicht gepflegt – zum dritten Mal an
derselben Zeile."*

🔴 **Und die Prüfung dafür existiert: Prüfung 78 hält genau diese Zahlen gegen den
Bestand – an einer von zwei Stellen.** Sie mißt `build/doc/26-qs-test.md`; dieselben Zahlen
in der Übergabe erreicht sie nicht. ➡️ *Das ist D-295 an einem zweiten Gegenstand: Der
Zählbereich war kleiner als die Wirkungsfläche.*

### B12 🔴 Keine Prüfung setzt die Regel „Rollen statt Personen" durch

**Bei der Umsetzung von E7 gefallen, und deshalb steht er hier hinter den anderen.** Der
Klarname des Owners ist in einen Kernträger geschrieben worden – **und alle 81 Prüfungen
liefen grün.**

`overlay-manifest.yaml` Zeile 3 verlangt *„Keine Secrets, keine Personen, keine internen
Adressen. Rollen statt Personen."*, `AGENTS.md` Abschnitt 11 dasselbe. **Gemessen kennt
die Inhaltsprüfung:** Secret-Muster, E-Mail-Adressen, IP-Adressen, interne Hostnamen, URLs
außerhalb der Allowlist und die projektlokale Sperrliste – **keinen Personennamen.**

➡️ *Eine Regel, die in zwei normativen Trägern steht und von keiner Prüfung erreicht wird,
ist der wiederkehrende Befundtyp dieses Projekts in seiner reinsten Form.* Ein Name, der
aus einem Kundenprojekt einsickert, käme genauso durch wie dieser. Neu: **`K-109`**.

### B13 und B14 🔴 Zwei Prüfungen aus `0.90.0` sind in jeder Installation rot

**Gefunden beim Heben der übernehmenden Projekte (E9) – also von einem Posten, der ohne
diesen Antrag gar nicht in diesem Release gelegen hätte.** Es war der **erste Lauf beider
Prüfungen gegen ein übernehmendes Projekt.**

| # | Prüfung | Was sie dort meldet | Warum sie unrecht hat |
|---|---|---|---|
| **B13** | **78** (die Zahlen des Hauptdokuments) | *„515 versionierte Dateien"* gegen **500** gezählte | Der Träger wird **byte-gleich ausgeliefert** (D-25) und beschreibt den Bestand des **Framework**-Repositoriums. Ein übernehmendes Projekt pflegt ihn nicht und soll es nicht |
| **B14** | **79** (die Lizenz an zwei Stellen) | *„LICENSE: fehlt"* | 🔴 **Sie verlangt von jedem übernehmenden Projekt eine GPL-3.0 in SEINER Wurzel** – und das ist das **Gegenteil** dessen, was dieselbe Entscheidung wollte: Die Zusatzerlaubnis nach §7 (D-317) nimmt Ausgaben und ausgefüllte Vorlagen ausdrücklich **aus** der GPL heraus, damit ein Projekt nicht zur Offenlegung gezwungen wird |

🔴 **Das ist D-299 an zwei weiteren Stellen – und die Lehre stand im SELBEN Release, das
beide Prüfungen gebaut hat:**

> *„Jede neue Prüfung läuft einmal gegen ein übernehmendes Projekt, bevor sie als fertig
> gilt – `--strict-overlay` ist billiger als der nächste Meßtag."*

➡️ ***Sie ist notiert und nicht angewandt worden.*** Eine Lehre, die in der Übergabe steht
und nicht im Ablauf, ist eine Lehre mit Halbwertszeit von einem Release.

🟢 **Beide Auflösungen nutzen dieselbe Unterscheidung wie Prüfung 75 und 81:** Das
Framework-Repositorium führt `UEBERGABE.md`, ein übernehmendes Projekt nicht. Prüfung 78
hält dort Enthaltung; Prüfung 79 verlangt dort allein die **Kernfassung** – die ist die,
die nach §4 GPL-3.0 mitwandern muß. **Die Wurzel gehört dem Projekt.** (**D-326**)

---

## 3. Vorlage zur Entscheidung

| # | Frage | Wege und ihre Preise |
|---|---|---|
| **E1** | **`K-81`: Bekommt das Repositorium eine `.gitattributes`, und mit welchem Wert?** | **Weg A – `* text=auto`.** 🟢 **Der Preis ist gemessen und null:** In einem Klon dieses Repositoriums ändert sie **keinen einzigen Blob** – alle 515 liegen bereits auf LF. Wirkung: Die Form im Repositorium hängt nicht mehr an der Konfiguration des jeweiligen Arbeitsplatzes, und `git archive` erzeugt ab jetzt reproduzierbar dieselbe Lieferung. ⚠️ **Grenze:** Sie setzt den **Blob**, nicht den Arbeitsbaum.<br><br>**Weg B – zusätzlich `eol=crlf`.** Zwingt auch den Arbeitsbaum. ⚠️ **Preis:** Sie bindet jeden künftigen Arbeitsplatz an eine Form, die nur dieser hier braucht, und `0.78.2` hat gemessen, daß eine Zeilenendevorschrift bei genau den Trägern nicht greift, um die es dort ging.<br><br>**Weg C – keine.** ⚠️ **Preis:** `K-81` bleibt offen, und die Lieferung von `1.0.0` entsteht aus einer Einstellung außerhalb des Repositoriums |
| **E2** | **Braucht `K-81` neben der Datei auch eine Prüfung?** | **Vorschlag: ja – Prüfung 81, und sie mißt den Arbeitsbaum.** Die `.gitattributes` setzt den Blob; was sie **nicht** sieht, ist der Fall, der diese Sitzung ausgelöst hat: **28 eingeschleppte LF-Zeilen im Arbeitsbaum**, gefunden von einem Suchtext, der nicht mehr traf, und von keiner der 80 Prüfungen. 🔴 **Prüfung 66 prüft die Gegenrichtung** (CR ohne LF) und greift hier nicht.<br><br>**Zuschnitt:** Sie schreibt **keine Form vor** – sie verlangt, daß es **eine** ist, über alle versionierten Textträger. ➡️ *Einheitlichkeit ist in jeder Installation richtig; eine bestimmte Form ist es nur an einem Arbeitsplatz.* Damit ist der Konstruktionsfehler ausgeschlossen, den D-299 benannt hat: im Framework grün, in jeder Installation rot |
| **E3** | **Wird Prüfung 78 auf die Abnahmezeile der Übergabe erweitert (B11)?** | **Vorschlag: ja.** Die Prüfung existiert, ihr Gegenstand steht an zwei Stellen, und sie erreicht eine. ⚠️ **Preis, benannt:** Jedes Release faßt diese Zeile dann an – derselbe Preis wie bei Prüfung 67 und 77, und er ist bei einer Zahl, die viermal veraltet ist, gerechtfertigt.<br><br>**Verworfen: die Zahlen aus der Übergabe streichen.** Sie ist der Ort, an dem der nächste Mensch nachsieht; eine Abnahmezeile ohne Zahlen verlagert das Problem, statt es zu lösen |
| **E4** | **Welche Form bekommt das Release-Archiv (B2)?** | **Vorschlag: annotiertes, signiertes Tag – `v` und der Inhalt von `VERSION` – plus `git archive`.** Das Tag ist der benannte Stand, das Archiv sein Abzug. **Ablage außerhalb des Repositoriums** – ein Erzeugnis gehört nicht in seine eigene Quelle (dieselbe Begründung wie bei `build/out/`). 🔴 **Das Verfahren gehört in `RELEASE_PROCESS.md`, nicht in eine Sitzung** – sonst ist es beim nächsten Release wieder keines |
| **E5** | **Wer setzt das Tag für `1.0.0`?** | 🔴 **Der Mensch, und die Begründung ist D-319.** Die Zeile sagt, **was** freigegeben wurde; der Commit – und ab jetzt das Tag – sagt **wer**. Ein Werkzeug kann beides setzen, es kann mit dem vorhandenen Schlüssel sogar signieren, **und genau deshalb darf es nicht.**<br><br>🟢 **Was `K-107` (a) dabei als Hindernis nannte, ist keines:** *„Das Einrichten eines Signierschlüssels ist eine Änderung am Arbeitsplatz."* **Gemessen: es ist kein Einrichten nötig.** `~/.ssh/id_ed25519` liegt seit Monaten am Platz, git ist `2.53` und signiert seit `2.34` mit SSH-Schlüsseln. Was bleibt, ist eine **repository-lokale** `git config` – kein Eingriff in den Arbeitsplatz |
| **E6** | **`K-107` (b): Wird die Historie angefaßt?** | **Vorschlag: nein, und der Befund tritt an die Stelle der Vermutung.** Der Name steht in **122 Merge-Commits des Servers**, in **keiner Datei**, und die **Adresse steht ohnehin unter beiden Namen in allen 261 Commits** – ein Umschreiben, das nur den Namen nimmt, ändert an der Zuordenbarkeit nichts. ⚠️ **Preis eines Umschreibens, benannt:** jeder Hash ändert sich, jede Commit-Verweisung in Protokollen und Anträgen bricht, und ein Tag danach zertifizierte eine andere Historie als die, die 106 Releases dokumentiert haben.<br><br>**Was stattdessen gilt:** Der Befund wird als Entscheidung festgehalten, die Wahl des Profilnamens für **künftige** Merges bleibt beim Owner, und sie wirkt nicht rückwirkend |
| **E7** | **`B8`: Was steht im Copyright-Vermerk?** | **Entschieden: der Klarname.** Ein GPL-Werk braucht einen benannten Rechteinhaber; ein Platzhalter benennt niemanden, und die Zusatzerlaubnis nach §7 (D-317) hängt an derselben Person. ⚠️ **Preis, benannt:** Der Name wandert in **jede Kopie des Kerns**, und die Neutralitätsprüfung braucht dafür eine ausdrückliche Ausnahme.<br><br>🟢 **Die Begründung ist eng:** Die Neutralitätsregel hält **fremde** Personen aus generischen Bestandteilen. **Der Urheber des Werks ist keine fremde Person** – ohne ihn ist die Lizenz nicht wirksam.<br><br>🔴 **Bei der Umsetzung gemessen, und es ist der schwerere Befund (B12):** Die angekündigte Ausnahme ist **unnötig – weil es keine Prüfung gibt, von der sie ausnähme.** Der Klarname ist in einen Kernträger geschrieben worden, und alle 81 Prüfungen liefen grün. Die Inhaltsprüfung kennt Secret-Muster, E-Mail-Adressen, IP-Adressen, Hostnamen, URLs und die projektlokale Sperrliste – **keinen Personennamen.** ➡️ *Eine Ausnahme für eine Prüfung, die es nicht gibt, ist die Bauform „Ausnahme mit leerem Geltungsbereich“ (0.57.1) – hier vor ihrer Entstehung gefangen.* Neu: `K-109` |
| **E8** | **`B4`: Deckt `FW-AK-01` vom 2026-09-18 den Prüfpunkt Aktualität?** | **Vorschlag: ja, mit ausdrücklich genannter Frist.** Der Prüfpunkt verlangt *„durchgeführt"*, nicht *„am Tag der Freigabe durchgeführt"*. Das Freigabeprotokoll nennt den gemessenen Produktstand und die Frist von fünf Tagen; was danach kam, ist Produktbeobachtung nach `RELEASE_PROCESS` Abschnitt 6 und nicht Gegenstand der Freigabe. ⚠️ **Preis:** Ein Produkt kann sich in fünf Tagen bewegt haben, und das Release sagt darüber nichts |
| **E9** | **`B7`: Werden die übernehmenden Projekte vor der Freigabe gehoben?** | **Vorschlag: ja, beide auf `1.0.0`.** Kriterium 5 ist die einzige Feststellung unter den fünf, die Prüfung 46 **nicht** nachrechnet – ein Nachweis, der drei Releases alt ist, ist genau deshalb einer, den niemand meldet. ⚠️ **Preis:** zwei Hebevorgänge, je rund zehn Minuten, und der Pilot trägt einen bekannten Projektbefund, der dabei nicht verschwindet |
| **E10** | **Ein Release oder zwei – Vorbedingungen in `0.92.0`, Freigabe in `1.0.0`?** | **Vorschlag: eines.** Neun der elf Befunde sind **Prüfpunkte von `FW-CL-11` selbst** (Archiv, Bestandsliste, Aktualität, Übernahme) – sie in ein eigenes Release zu ziehen hieße, dieselbe Checkliste zweimal abzuarbeiten, einmal ohne Freigabe. ⚠️ **Preis, und er ist real:** `1.0.0` trägt damit zwei neue Prüfungen, und der Abnahmelauf mißt einen Baum, der sich in derselben Sitzung stark bewegt hat. **Die Gegenmaßnahme ist die vorhandene:** Der Abnahmelauf gegen den fertigen Baum ist ein eigener Lauf, in **beiden** Kodierungsumgebungen, mit zeilengleichem Vergleich |

> **Empfehlung der Vorbereitung:** E1 Weg A, E2 bis E4 wie vorgeschlagen, E5 durch den
> Menschen, E6 nein, E7 Klarname, E8 ja, E9 ja, E10 ein Release.

---

## 4. Was dieser Antrag ausdrücklich **nicht** entscheidet

- **Die Veröffentlichung.** `1.0.0` ist ein Release im vorhandenen Repositorium. Ob und wo
  das Framework öffentlich erscheint, ist eine eigene Entscheidung – und sie ist nach B6
  **nicht mehr durch ein Umschreiben der Historie vorbereitbar**, sondern nur durch die
  Kenntnis dessen, was die Historie trägt.
- **`K-100`.** Die Zahl der offenen Klärungspunkte bleibt unermittelbar; B9 zeigt dieselbe
  Bauform an einem zweiten Gegenstand. Das ist ein Befund, kein Posten dieses Releases –
  **offene Klärungspunkte sind kein Prüfpunkt von `FW-CL-11` und kein Kriterium von D-11.**
- **`K-105`.** Der Foliensatz liegt außerhalb des Repositoriums und steht auf `0.90.0`.
  Keine Prüfung erreicht ihn; dieses Release ändert daran nichts.
- **Der `SOLL`-Prüfpunkt `M1→M2→M3→M4`.** Er braucht ein Sitzungskontingent. Er wird
  **ausgewiesen, nicht weggelassen** – ein nicht gefahrenes `SOLL` ist ein Messwert, ein
  verschwiegenes ist ein Befund.

---

## 5. Umsetzung

1. `.gitattributes` mit `* text=auto` (E1).
2. **Prüfung 81** – einheitliche Zeilenendeform über alle versionierten Textträger (E2),
   mit Sonde, Gegenprobe und Ankerprobe.
3. **Prüfung 78** erweitert auf die Abnahmezeile der Übergabe (E3), mit eigener Sonde.
4. `RELEASE_PROCESS.md`: Archivverfahren und Bestandsliste als normative Schritte (E4).
5. `governance/ADOPTION_REGISTRY.md` angelegt und mit dem gemessenen Stand gefüllt (E5).
6. `LICENSE-HINWEIS.md`: Copyright auf den benannten Rechteinhaber, mit der Begründung
   der Grenze im Träger selbst (E7) – **ohne** Ausnahme im Validator, weil es dort nichts
   auszunehmen gibt (B12).
7. Decision Log: **D-320** bis **D-327**; `K-81` und `K-107` geschlossen, **`K-108`** und
   **`K-109`** neu.
8. Die vier falschen Zahlen berichtigt: 22 → **24** Prüfpunkte, 109 → **106** Releases,
   76/424 → **80/441**, und die LF-Aussage an ihrem Gegenstand.
9. Beide übernehmenden Projekte auf `1.0.0` gehoben (E9).
10. `VERSION`, `CHANGELOG.md`, `ROADMAP.md`, `build/doc/00-kopf.md`, `26-qs-test.md`,
    Hauptdokument und Word-Fassung für **beide** Client Packs.
11. Das Freigabeprotokoll mit **24** Prüfpunkten – **nicht abgehakt**; das Abhaken ist die
    Handlung des Menschen.

---

## 6. Entscheidung

**E1 bis E10 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-23), mit einer
Abweichung: **E7 auf den Klarnamen** statt auf den Platzhalter, wie in der Vorlage als
zweiter Weg beschrieben.

Decision Records **D-320** bis **D-327**. `K-81` **geschlossen** (offen seit `0.78.2`),
`K-107` **geschlossen**, **`K-108`** neu (die Veröffentlichung als eigene Entscheidung)
und **`K-109`** neu (die Regel ohne Prüfung, B12).
Alle vier zählbaren Kriterien von D-11 bleiben **0**.
