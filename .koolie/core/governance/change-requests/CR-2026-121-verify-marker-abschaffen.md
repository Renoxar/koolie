# Änderungsantrag `CR-2026-121`

| Feld | Inhalt |
|---|---|
| Titel | Die Markerform selbst – Kriterium 1 von 18 auf 0, und was der Zähler danach zählt |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-22 |
| Betroffene Artefakte | `framework/core/00-principles.md` (Belegstatustabelle), `framework/core/01-governance.md` (Lebenszyklus, Bedingung c), `framework/core/02-privacy.md` (zwei Fundstellen), `framework/skills/fw-mr-description/SKILL.md`, `framework/skills/fw-review-support/SKILL.md` (zwei Fundstellen), `templates/SKILL_TEMPLATE.md`, `clientmap.py`, `tests/scripts/hook-overlay-status.py`, `clients/README.md` (Abschnitte 4 und 5), `clients/devin-desktop/CLIENT_PACK.md` (Vorbemerkung, Zeile `X2`, Belegstand), `clients/claude-code/CLIENT_PACK.md` (Vorbemerkung, Belegstand), `docs/PLACEHOLDER_REGISTRY.md` (zwei Registerzeilen), `docs/ROADMAP.md` (Standzeile, Zählregel, Releaseplan, `AP2`, `AP11`), `governance/DECISION_LOG.md` (`K-20`, `A-05`, **D-291** bis **D-297**), `governance/RELEASE_PROCESS.md`, `governance/CHANGE_REQUEST_TEMPLATE.md`, `checklists/11-framework-release.md`, `tests/TEST_CATALOG.md`, `tests/scripts/validate-framework.py` (Prüfungen 34 und 46, Register), `tests/scripts/probe-pruefungen.py` (Kopfkommentare), `build/doc/00-kopf.md`, `build/doc/05-glossar.md`, `build/doc/15-referenzstruktur.md`, `build/doc/31-anhaenge.md`, `build/doc/32-abschluss.md`, `README.md`, `tests/protocols/2026-09-22-verify-marker-abschaffen.md` (neu), `CHANGELOG.md`, `VERSION`, `UEBERGABE.md`. **Gehoben:** sieben Modulträger und beide Client Packs (E9) |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand ist eine registrierte Platzhalterform, die Belegstatuskonvention des Frameworks und eine Zählregel von D-11 |
| Art | **Durchsicht und Herrichtung ohne Kontingent** – kein Lauf an einem Client, keine Modellzeit |
| Dringlichkeit | **Regulär**; der Wiederaufnahmepunkt von `0.86.0` nennt ihn als letzten Posten von Kriterium 1 |

## 1. Anlass

**Kriterium 1 von D-11 steht auf 18, und es kann ohne diesen Schritt nicht auf null
gehen.** `CR-2026-070` E3 hat ausdrücklich entschieden, daß auch die Fundstelle zählt,
die den Marker nur **nennt** – Registerzeile, Glossarzeile, Arbeitsanweisung –, und hat
den Grund gleich mitgeliefert: `docs/PLACEHOLDER_REGISTRY.md` schreibt beiden
Markerformen in der Spalte „Ersetzung/Frist" ausdrücklich **„vor Version 1.0.0"** vor.
*Ein Platzhalter, dessen letzte Aussage verifiziert ist, gehört aus dem Register; sonst
führt das Repositorium einen Platzhalter ohne Gegenstand.*

**Die Vorbedingung dafür ist mit `0.86.0` eingetreten.** `AP2` ist zu Ende gefahren:
`S3`, `B3`, `B10` und `A1` sind an einer Installation gemessen (D-277 bis D-287), `X2`
ist als **dauerhaft** nicht beobachtbar festgestellt (`K-20`). Von den achtzehn
Fundstellen trägt damit **genau eine** noch eine wirklich offene Frage – und ihre Frist
„vor Version 1.0.0" war von Anfang an falsch, weil die Frage keine Frist einhalten kann.

> 🔴 **Und das ist der eigentliche Befund dieses Antrags.** Die Markerform verbindet zwei
> Dinge, die nicht zusammengehören: **den Belegstand einer Aussage** und **eine Frist, bis
> wann er hergestellt sein muß**. Für sechzehn Fundstellen war die Frist richtig und ist
> eingelöst. Für `X2` war sie nie einlösbar, und der Marker hat das achtundneunzig Releases (seit `0.7.0`, nachgezählt am Changelog) lang
> als Arbeitsvorrat ausgewiesen. *Eine Marke, die einen dauerhaften Zustand als Rückstand
> führt, macht aus einer ehrlichen Auskunft eine offene Schuld.*

## 2. Der Vorbedingungsdurchgang – fünf Befunde vor dem ersten Handgriff

**Zum zwölften Mal in Folge trägt er sich.** Keiner der fünf Befunde hat etwas gekostet,
und zwei von ihnen hätten den Schritt still falsch gemacht.

### V1 – Der Zählbereich ist kleiner als die Wirkungsfläche

Prüfung 46 zählt unter `<CORE_DIR>/` **ohne** `build/`, `CHANGELOG.md`,
`governance/change-requests/` und `tests/protocols/`. Die Markerform steht darüber hinaus
in **sechs weiteren versionierten Trägern**, die der Zähler nie gesehen hat:

| Träger | Fundstellen | gezählt |
|---|---|---|
| `README.md` (Wurzel) | 1 | **nein** – liegt außerhalb `<CORE_DIR>/` |
| `build/doc/00-kopf.md`, `05-glossar.md`, `15-referenzstruktur.md`, `31-anhaenge.md`, `32-abschluss.md` | je 1 | **nein** – `build/` ist ausgenommen |

🔴 **Wer nur die gezählten achtzehn entfernt, läßt die Form in der Wurzel-README und im
Glossar des Hauptdokuments stehen – und der Zähler meldet trotzdem null.** *Das ist die
Null durch Konstruktion (0.59.1) in ihrer teuersten Gestalt: nicht die Prüfung lügt,
sondern ihr Zuschnitt.*

🟢 **Gegenprobe, und sie entlastet zwei Ablagen:** `.devin/` (vier Fundstellen) und
`build/out/hauptdokument.md` (32) stehen in `.gitignore` – sie sind **Erzeugnisse**,
nicht Bestand. Die vier unter `.devin/` entstehen aus `clientmap.py` und den beiden
Skills und folgen aus `install.py --update`; die 32 im Hauptdokument entstehen beim
nächsten Bau aus `build/doc/`.

### V2 – Der Belegstand des Packs `devin-desktop` ist seit `0.86.0` falsch

Er sagt: *„**5 der 36 Zeilen** tragen einen offenen VERIFY-Marker – **X2** unmittelbar,
B4, B5, B6 und B8 über den Verweis „wie B3""* – und **im selben Absatz**, daß `B3` mit
`0.86.0` aufgelöst ist. **Ein Verweisbeleg erbt den Beleg seines Ziels** (D-266); ist das
Ziel aufgelöst, ist der Verweis es auch. Richtig ist **1 von 36**.

⚠️ **Die Übersicht in `clients/README.md` sagt seit `0.86.0` genau das** (*„Genau eine
Zeile trägt noch einen offenen VERIFY-Marker, und dauerhaft: `X2`"*). **Zwei Träger
desselben Hauses widersprechen sich, und keine Prüfung rechnet die Zahl nach** – das Pack
sagt es über sich selbst: *„Die vier über den Verweis mitgezählten sind eine
Ermessensgrenze und werden von keiner Prüfung nachgerechnet."*

### V3 – Der Belegstand des Packs `claude-code` ist seit `0.62.0` falsch

Er sagt: *„**Eine** Zeile trägt einen VERIFY-Marker – R5"*. Der **Änderungsverlauf
desselben Packs** sagt hundertfünfzig Zeilen weiter unten, der Marker auf `R5` sei mit
Pack-Version `0.21.0` aufgelöst (D-158, 2026-09-18). **Keine Fundstelle des Packs trägt
die Form.** Richtig ist **null**.

🔴 **Derselbe Absatz nennt zwei weitere Zahlen, und beide sind überholt:** *„bei
`devin-desktop`: 9 von 36"* (richtig: 1) und der Satz darüber, dort sei *„keine einzige
Einstufung gegen eine Installation oder gegen die Herstellerdokumentation geprüft"* –
`AP2` ist seit `0.86.0` zu Ende gefahren. *Drei Zahlen über denselben Gegenstand, drei
Stände.*

### V4 – Der Vorbehalt von Prüfung 34 verliert seinen Gegenstand

`check_agent_startwerkzeug` läßt eine Zeile `A1` auf `[TECHNISCH]` durchgehen, **solange
sie `<VERIFY` trägt** – der Vorbehalt, den die Prüfung bei ihrem ersten Lauf selbst
gelernt hat. **Seit `0.86.0` trägt keine Zeile `A1` eines Packs die Form mehr**, und die
zugehörige Sonde hat ihren Präparationsort bereits gewechselt (sie nimmt jetzt das
Startwerkzeug weg statt den Marker). Mit der Abschaffung wird die Bedingung **dauerhaft
wahr**: *eine Ausnahme, die nichts mehr ausnimmt* (0.57.0) – sie sieht wie Sorgfalt aus
und ist toter Code.

### V5 – Die Lebenszyklusregel nennt den Marker, ohne ihn zu schreiben

`01-governance.md` Abschnitt 5, Punkt 3, Übergang `entwurf → pilot`, Bedingung **(c)**:
*„Offene `VERIFY`-Marker des Trägers sind benannt; sie sperren den Übergang **nicht** –
gezählt werden sie in Kriterium 1 von D-11."* Sie steht in der Schreibweise mit
Bindestrich und **zählt deshalb bei Kriterium 1 nicht mit** – ein Sweep nach der
Markerform findet sie nicht.

➡️ **Das ist *die Aufzählung unter der entfernten Überschrift* (0.58.0), diesmal vor dem
Schnitt gefunden:** Wer die Form entfernt, entfernt die Zeilen, die den Begriff
**schreiben** – die Regel, die ihn **ausmacht**, bleibt stehen und verweist auf einen
Gegenstand, den es nicht mehr gibt. **Der Wächter dieses Schnitts braucht deshalb ein
zweites Muster** (0.75.0, D-205): gesucht wird nicht nur die Form, sondern jede Nennung
des Wortes `VERIFY` in jedem versionierten Träger außerhalb der Chronik.

## 3. Die achtzehn gezählten Fundstellen, je mit ihrer Auflösung

**Sechzehn sind sachlich aufgelöst, zwei werden umgewidmet – und die beiden sind dieselbe
Frage.** Keine wird stillschweigend umetikettiert; das ist die Bedingung, unter der dieser
Schritt kein Taschenspielertrick ist.

> 🔴 **Die Aufschlüsselung stand bis zum Durchgang vor dem Commit auf „siebzehn und eine"
> und summierte sich auf 19.** Nachgezählt je Fundstelle sind es **5 + 3 + 5 + 3 + 2 = 18**:
> Zeile `X2` **und** die Nachweiszelle von `K-20` sind **zwei** gezählte Fundstellen mit
> **einer** Frage, und `.devin/config.json` ist nicht versioniert und zählt nicht mit.
> *Einunddreißigster Durchgang in Folge, der sich trägt.*

| # | Fundstelle | Art | Auflösung |
|---|---|---|---|
| 1 | `checklists/11-framework-release.md:40` | nur nennend | Die Checklistenzeile nennt künftig die **Belegspalte** statt der Markerform |
| 2 | `clientmap.py:328` | tragend | **Gemessen** (`B3`, D-277): Die Zeile verweist auf die Matrixzeile `B3` des jeweiligen Packs, die die Mustersemantik samt Groß-/Kleinschreibungsgrenze trägt |
| 3 | `clients/devin-desktop/CLIENT_PACK.md:144` (`X2`) | tragend | **Dauerhaft offen** (`K-20`): Belegzelle sagt `BELEG OFFEN (dauerhaft)` mit Grund, Datum und Klärungspunkt |
| 4 | `clients/README.md:67` | nur nennend | Die Regel nennt künftig `BELEG OFFEN` statt der Markerform |
| 5 | `docs/PLACEHOLDER_REGISTRY.md:80` (Altform) | Registerzeile | **entfällt** |
| 6 | `docs/PLACEHOLDER_REGISTRY.md:81` (neutrale Form) | Registerzeile | **entfällt** |
| 7 | `docs/ROADMAP.md:2585` (`AP2`, Ziel) | nur nennend | `AP2` ist gefahren; die Zeile nennt das Ergebnis statt der Marke |
| 8 | `framework/core/00-principles.md:33` | Glossarzeile | **entfällt**; die Belegstatustabelle führt `BELEG OFFEN` als vierte Zeile |
| 9 | `framework/core/02-privacy.md:20` | tragend | Verweist auf die Matrixzeile `X2` und `K-20` – die Frage bleibt, die Marke nicht |
| 10 | `framework/core/02-privacy.md:91` | tragend | Verweist auf die Fähigkeitsmatrix des jeweiligen Packs |
| 11 | `framework/skills/fw-mr-description/SKILL.md:78` | tragend | **Gemessen** (`S3`, D-287): Verweist auf die Matrixzeile `S3` |
| 12 | `framework/skills/fw-review-support/SKILL.md:77` | tragend | **Gemessen** (`S3`, D-287): Verweist auf die Matrixzeile `S3` |
| 13 | `framework/skills/fw-review-support/SKILL.md:91` | tragend | **Gemessen** (`A1`, D-284): Verweist auf `agent_start_tools` des Manifests und die Matrixzeile `A1` |
| 14 | `governance/DECISION_LOG.md:29` (`K-20`) | tragend | Die Nachweiszelle nennt den Belegstand statt der Marke |
| 15 | `governance/DECISION_LOG.md:415` (`A-05`) | tragend | `AP2` ist gefahren; die Annahme nennt die Fähigkeitsmatrix als Nachweisort |
| 16 | `governance/RELEASE_PROCESS.md:46` | nur nennend | Nennt die Belegspalte statt der Markerform |
| 17 | `templates/SKILL_TEMPLATE.md:26` | tragend | **Gemessen** (`S3`, D-287): Verweist auf die Matrixzeile `S3` |
| 18 | `tests/scripts/hook-overlay-status.py:6` | tragend | Der Mechanismus ist `[DOK]`; **daß die Nutzlast nicht dokumentiert ist, wird gesagt statt markiert** – dieselbe Form wie die benannte Grenze von `R5` |

Die Aufschlüsselung nach Art der Auflösung steht im Protokoll, Abschnitt 3.

**Dazu sechs Fundstellen außerhalb des Zählbereichs** (V1): `README.md` und die fünf
Quellen des Hauptdokuments unter `build/doc/`.

## 4. Vorlage zur Entscheidung

| # | Frage | Auflösung und Preis |
|---|---|---|
| **E1** | **Was zählt Prüfung 46 bei Kriterium 1, nachdem die Markerform abgeschafft ist – und gehört der Zähler ausgebaut statt stillgelegt (D-23)?** | **Er bleibt, unverändert, und wird zur Rückfallsperre umgewidmet.** Das Muster bleibt wörtlich, der Zählbereich bleibt; was sich ändert, ist die Lesart: Die Zahl ist ab jetzt kein **Arbeitsvorrat**, sondern ein **Pegel gegen die Wiedereinführung**. 🟢 **Die Null ist gemessen und nicht konstruiert, und das ist belegt:** Sonde `46c` legt einen Marker in `03-security.md` und verlangt die Meldung, Gegenprobe `46c` legt einen in ein datiertes Protokoll und verlangt ihr Ausbleiben. **Beide bringen ihren Gegenstand selbst mit** (Wirkungsnachweis `0.86.0` Abschnitt 2a) und sind vom Schnitt nicht betroffen. **Preis des Gegenwegs (Ausbau):** D-11 verlöre seinen einzigen maschinellen Zähler für Kriterium 1, die Standzeile fiele von vier Zahlen auf drei, und eine Wiedereinführung der Form – aus einem Changelogzitat, aus einem neuen Client Pack – fiele niemandem auf. **Preis des gewählten Wegs, und er ist benannt:** Eine Zahl, die dauerhaft auf null steht, wird nicht mehr gelesen; sie trägt nur noch, solange ihre Sonde läuft |
| **E2** | **Tritt eine Ersatzmarke an die Stelle des Markers?** | **Nein – und das ist der Unterschied zu einer Umbenennung.** Der Nachweisstand steht künftig dort, wo er ohnehin hingehört: in der **Belegspalte**. Sie führt `[DOK]`, `[EMPF]`, `[KONZ]` und neu `BELEG OFFEN` – letzteres **mit Grund und Datum**, nach dem Vorbild von `QUELLE NICHT ZUGEORDNET` (D-156, D-263). 🔴 **Der sachliche Unterschied, und er ist der Grund des ganzen Antrags:** Der Marker war ein **Platzhalter mit Frist** („vor Version 1.0.0"), `BELEG OFFEN` ist ein **Belegstand ohne Frist**. Eine Frage, die dauerhaft nicht beobachtbar ist (`X2`/`K-20`), kann keine Frist einhalten; achtundneunzig Releases (seit `0.7.0`, nachgezählt am Changelog) lang stand sie trotzdem als Rückstand. ⚠️ **Preis, und er ist die Bauform von `K-41`:** Daß eine unbelegte Aussage überhaupt gekennzeichnet wird, setzt **keine Prüfung** durch. Was durchgesetzt bleibt, ist die Quellenangabe jeder `[DOK]`-Zeile (Prüfung 73) und die Aufzählbarkeit der Matrixzeilen (Prüfung 74) |
| **E3** | **Wird `BELEG OFFEN` bei Kriterium 1 mitgezählt?** | **Nein.** Kriterium 1 zählt **fristgebundene, unerledigte** Marken; `BELEG OFFEN` trägt keine Frist. **Preis, und er ist die ernsteste Frage dieses Antrags:** Kriterium 1 wäre damit durch bloßes Umetikettieren erfüllbar. 🟢 **Die Gegenprobe ist geführt und steht in Abschnitt 3:** Von achtzehn Fundstellen werden **genau zwei** zu `BELEG OFFEN` – die Zeile `X2` und die Nachweiszelle von `K-20`, also **eine** Frage, die das Projekt seit `0.62.0` als dauerhaft offen führt. **Die übrigen sechzehn sind sachlich aufgelöst, fünf davon durch eine Messung mit Decision Record.** *Wer diesen Schritt wiederholen will, muß die Auflösung je Fundstelle wieder mitliefern* |
| **E4** | **Reicht der Zählbereich von Prüfung 46, oder wird er erweitert?** | **Er bleibt, die Abschaffung greift weiter.** Der Zählbereich von `CR-2026-070` ist begründet und wird nicht angefaßt; die **Abschaffung** dagegen greift für **jeden versionierten Träger** – also auch `README.md` und `build/doc/`. **Preis des Gegenwegs (Erweiterung):** Der Zähler nähme dann `build/` auf, und damit die Quellen eines Dokuments, das über vierzig Releases zurück ist und zu `AP11` gehört – die Zahl stiege aus einem Grund, der nichts mit dem Gegenstand zu tun hat. **Preis des gewählten Wegs:** Daß die sechs Fundstellen außerhalb des Zählbereichs wirklich weg sind, sagt **keine Prüfung**; es sagt der Wirkungsnachweis, mit dem zweiten Muster aus V5 |
| **E5** | **Was geschieht mit dem Vorbehalt von Prüfung 34 (V4)?** | **Er wandert auf die Nachfolgeform.** Statt `<VERIFY` erkennt die Prüfung künftig `BELEG OFFEN` in der Zeile `A1`. **Preis des Gegenwegs (ersatzlos streichen):** Ein Pack, das `A1` ehrlich als **vorgesehene** Tiefe führt und das Startwerkzeug noch nicht erhoben hat, fiele durch – genau der Fall, an dem diese Prüfung bei ihrem ersten Lauf gelernt hat. **Preis des gewählten Wegs:** Der Vorbehalt hat heute **keinen** Fall im Bestand (beide Packs führen `agent_start_tools` gefüllt); er ist eine Vorsorge, und seine Sonde präpariert sie |
| **E6** | **Werden die drei überholten Belegstände (V2, V3) hier berichtigt?** | **Ja.** Sie sind **Buchführung über den Marker** und damit Gegenstand dieses Antrags; sie stehen zu lassen hieße, die Zahl zu senken und die Sätze über sie falsch zu lassen. **Preis:** Der Antrag faßt zwei Client Packs an, die er sonst nicht anfassen müßte. **Preis des Gegenwegs:** Nach dem Schnitt behaupteten zwei Packs einen Marker, den es nicht mehr gibt – *die Zusage, deren Widerlegung im eigenen Dokument steht* |
| **E7** | **Wird das Hauptdokument neu gebaut?** | **Nein**, wie `0.85.0` und `0.62.0`. Gepflegt werden die Quellen unter `build/doc/`; `build/out/hauptdokument.md` steht in `.gitignore`, ist über vierzig Releases zurück und gehört zu `AP11`. 🟢 **Die 32 Fundstellen dort verschwinden beim nächsten Bau von selbst** |
| **E8** | **Wird eine neue Prüfung gebaut, die die Abwesenheit der Form durchsetzt?** | **Nein.** *Keine neue Prüfung, solange eine Zahl zu senken ist* – und Kriterium 1 ist genau diese Zahl. **Der Zähler aus E1 leistet es für den Zählbereich ohnehin;** für die sechs Träger außerhalb wäre eine Prüfung denkbar und ist **ausdrücklich vertagt** (`K-98`) |

| **E9** | **Welche Modulträger werden gehoben?** | **Gehoben werden die Träger, deren NORMATIVER Text sich geändert hat:** `00-principles.md` (0.1.4), `01-governance.md` (0.3.2), `02-privacy.md` (0.1.8), `clients/README.md` (0.6.0), `SKILL_TEMPLATE.md` (0.1.3), `checklists/11` (0.2.3), `RELEASE_PROCESS.md` (0.1.4) sowie beide Client Packs (`devin-desktop` 0.14.0, `claude-code` 0.24.0). 🔴 **NICHT gehoben werden die beiden Skills `fw-mr-description` und `fw-review-support`** – und das ist keine Nachlässigkeit, sondern `K-84`: *Eine angehobene Skillversion setzt die abgenommenen Zellen seines Testblatts auf die Fassung davor* (D-119), und genau das hat `0.79.0` getan – **zwei Zellen gingen zurück auf `offen`, Kriterium 2 stieg** (D-227). **Wörtlich angewandt ginge Kriterium 2 hier von 0 wieder aufwärts, in demselben Release, das Kriterium 1 auf 0 bringt.** ⚠️ **Der Eingriff an beiden Skills betrifft eine `(Erläuterung)`, nicht eine Anweisung** – kein Arbeitsschritt, kein Frontmatterfeld, keine Zusage. **Hier nicht entschieden; die Frage gehört zu `K-84` und ist dort ausdrücklich offen.** **Preis, benannt:** Zwei Skills tragen eine unveränderte Version bei geändertem Text. ⚠️ **Die Client Packs sind der Gegenfall und deshalb gehoben:** Nachgezählt nennt **keine** Zelle eines Testblatts eine Packversion – sie nennen den **Produktstand** (D-117, D-202) |

## 5. Wirkung auf D-11

| Kriterium | vorher | nachher | Grund |
|---|---|---|---|
| 1 – `VERIFY`-Marker | **18** | **0** | Sechzehn Fundstellen sachlich aufgelöst, zwei umgewidmet (dieselbe Frage), beide Registerzeilen entfallen |
| 2 – Testkatalog | 0 | 0 | unberührt |
| 3 – Modulstatus | 0 | 0 | unberührt |
| 4 – Decision Records | 0 | 0 | Die sieben neuen Records werden **bestätigt** eingetragen |

> 🔴 **Damit stehen alle vier zählbaren Kriterien auf null, und Kriterium 5 ist erfüllt.**
> **Das heißt nicht `1.0.0`-reif**, und Prüfung 46 behauptet es auch nicht (E8 von
> `CR-2026-070`): Sie rechnet vier Zahlen aus und hält sie gegen die Standzeile. Was
> zwischen diesem Stand und `1.0.0` liegt, steht im Releaseplan – die Umbenennung
> (`~0.88.0`) und `AP11`.

## 6. Entscheidung

**Angenommen** in der Fassung von Abschnitt 4. Die Umsetzung steht in
`leitwerk-core/tests/protocols/2026-09-22-verify-marker-abschaffen.md`.
