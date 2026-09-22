# Protokoll: Die Markerform selbst – Kriterium 1 von 18 auf 0

| Feld | Wert |
|---|---|
| Gegenstand | Die registrierte Markerform `<VERIFY AGAINST CURRENT … DOCUMENTATION>` in beiden Schreibweisen – und was Prüfung 46 danach zählt |
| Antrag | `CR-2026-121` |
| Datum | 2026-09-22 |
| Framework-Version | 0.86.1 (Befunde) / 0.87.0 (Behebung) |
| Art | **ohne Kontingent** – kein Lauf an einem Client, keine Modellzeit |
| Ergebnisstatus | **bestanden.** 18 gezählte Fundstellen auf 0, dazu 6 in versionierten Trägern außerhalb des Zählbereichs; sieben Decision Records, ein neuer Klärungspunkt |

> 🔴 **Zwölfter Durchgang in Folge, bei dem der billigste Befund vor dem ersten Handgriff
> fällt.** Fünf Befunde, keiner hat etwas gekostet, **zwei hätten den Schritt still
> falsch gemacht.**

## 1. Die Lage vor dem Durchgang

Kriterium 1 von D-11 stand auf **18**, verteilt auf **14 Dateien**. `CR-2026-070` E3 hat
entschieden, daß auch die nur **nennende** Fundstelle zählt – Registerzeile, Glossarzeile,
Arbeitsanweisung –, und den Grund mitgeliefert: `docs/PLACEHOLDER_REGISTRY.md` schrieb
beiden Formen in der Spalte „Ersetzung/Frist" ausdrücklich **„vor Version 1.0.0"** vor.
*Ein Platzhalter, dessen letzte Aussage verifiziert ist, gehört aus dem Register.*

**Die Vorbedingung dafür war mit `0.86.0` eingetreten:** `AP2` ist zu Ende gefahren, vier
von fünf Markern des Packs `devin-desktop` sind gefallen, `X2` ist als dauerhaft nicht
beobachtbar festgestellt (`K-20`).

## 2. Der Vorbedingungsdurchgang – fünf Befunde

### 2.1 V1: Der Zählbereich war kleiner als die Wirkungsfläche (D-295)

Prüfung 46 zählt unter `<CORE_DIR>/` ohne `build/`, `CHANGELOG.md`,
`governance/change-requests/` und `tests/protocols/`. **Gezählt am Bestand, nicht an der
Regel:**

| Menge | Fundstellen | von Prüfung 46 gezählt |
|---|---|---|
| `<CORE_DIR>/` ohne die vier Gattungen | **18** in 14 Dateien | ja |
| `README.md` (Wurzel) | **1** | nein – außerhalb `<CORE_DIR>/` |
| `build/doc/` (5 Quellen des Hauptdokuments) | **5** | nein – `build/` ist ausgenommen |
| Chronik (`CHANGELOG.md` 4, `change-requests/` 9, `protocols/` 2) | **15** | nein – Gattungsausnahme E2 |
| `.devin/` (Laufzeitschicht) | **4** | nein – **in `.gitignore`**, Erzeugnis |
| `build/out/hauptdokument.md` | **32** | nein – **in `.gitignore`**, Erzeugnis |

🔴 **Wer nur die gezählten achtzehn entfernt, läßt die Form in der Wurzel-README und im
Glossar des Hauptdokuments stehen – und der Zähler meldet trotzdem null.**
🟢 **Entlastet sind die beiden Erzeugnisablagen:** `.devin/` folgt aus `install.py`,
`build/out/` aus dem nächsten Bau; **beide sind nicht versioniert.**

➡️ **Entschieden (D-295):** Der Zählbereich bleibt, die Abschaffung greift für jeden
**versionierten** Träger. Daß die sechs daneben weg sind, sagt keine Prüfung, sondern
dieser Wirkungsnachweis – und das ist `K-98`.

### 2.2 V2: Der Belegstand des Packs `devin-desktop` war seit `0.86.0` falsch (D-297)

Er sagte *„**5 der 36 Zeilen** tragen einen offenen VERIFY-Marker – **X2** unmittelbar,
B4, B5, B6 und B8 über den Verweis „wie B3""* – **und im selben Absatz**, daß `B3` mit
`0.86.0` aufgelöst ist. *Ein Verweisbeleg erbt den Beleg seines Ziels* (D-266); ist das
Ziel aufgelöst, ist der Verweis es auch.

| Träger | sagte | richtig |
|---|---|---|
| `clients/devin-desktop/CLIENT_PACK.md` | 5 von 36 | **1 von 36** |
| `clients/README.md` (Übersicht) | „genau eine" | **1 von 36** |

⚠️ **Zwei Träger desselben Hauses, zwei Zahlen – und keine Prüfung rechnet sie nach.**
Das Pack sagt es über sich selbst: *„Die vier über den Verweis mitgezählten sind eine
Ermessensgrenze und werden von keiner Prüfung nachgerechnet."*

### 2.3 V3: Der Belegstand des Packs `claude-code` war seit `0.62.0` falsch (D-297)

Er sagte *„**Eine** Zeile trägt einen VERIFY-Marker – R5"*. **Der Änderungsverlauf
desselben Packs** sagt hundertfünfzig Zeilen weiter unten, der Marker auf `R5` sei mit
Pack-Version `0.21.0` aufgelöst (D-158, 2026-09-18), **und keine Fundstelle des Packs trug
die Form.** *Die Zusage, deren Widerlegung im eigenen Dokument steht.*

🔴 **Zwei weitere Zahlen desselben Absatzes waren überholt:** *„bei `devin-desktop`: 9 von
36"* (richtig: 1) und *„keine einzige Einstufung ist gegen eine Installation oder gegen
die Herstellerdokumentation geprüft"* – seit `0.53.0` falsch, seit `0.86.0` grob falsch.
**Drei Zahlen über denselben Gegenstand, drei Stände.**

### 2.4 V4: Der Vorbehalt von Prüfung 34 hätte seinen Gegenstand verloren (D-296)

`check_agent_startwerkzeug` läßt eine Zeile `A1` auf `[TECHNISCH]` durchgehen, **solange
sie `<VERIFY` trägt**. Seit `0.86.0` trägt keine Zeile `A1` die Form mehr, und die
zugehörige Sonde hat ihren Präparationsort bereits gewechselt. Mit der Abschaffung wäre
die Bedingung **dauerhaft wahr** – *eine Ausnahme, die nichts mehr ausnimmt* (0.57.1).

➡️ **Der Vorbehalt steht seither auf `BELEG OFFEN`.** ⚠️ **Er hat heute keinen Fall im
Bestand:** Beide Packs führen `agent_start_tools` gefüllt, der Zweig wird nicht erreicht.
Er ist Vorsorge, und Sonde `34e` präpariert sie.

### 2.5 V5: Die Lebenszyklusregel nennt den Marker, ohne ihn zu schreiben

`framework/core/01-governance.md` Abschnitt 5, Übergang `entwurf → pilot`, Bedingung (c):
*„Offene `VERIFY`-Marker des Trägers sind benannt."* **Schreibweise mit Bindestrich –
Kriterium 1 zählt sie nicht, ein Sweep nach der Form findet sie nicht.** Dasselbe gilt für
Punkt 7 desselben Abschnitts, der D-114 wörtlich wiederholt.

➡️ *Die Aufzählung unter der entfernten Überschrift* (0.58.0), diesmal **vor** dem Schnitt
gefunden. **Der Wächter dieses Schnitts braucht ein zweites Muster** (0.75.0, D-205):
Gesucht wurde jede Nennung des Wortes `VERIFY` in **jedem versionierten Träger außerhalb
der Chronik**, nicht nur die Form. Er hat **25 Stellen in neun Trägern** gefunden, die
der Formsweep nicht gefunden hätte:

| Art | Stellen | Träger |
|---|---|---|
| **normative Regeln** | **2** | `framework/core/01-governance.md` Abschnitt 5.3 (c) – Übergangsbedingung `entwurf → pilot` – und Abschnitt 5.7, der D-114 wörtlich wiederholt |
| **Belegstände, Vorbemerkungen, Übersicht** | **8** | `clients/devin-desktop/CLIENT_PACK.md` (4), `clients/claude-code/CLIENT_PACK.md` (3), `clients/README.md` (1) |
| **Arbeitsanweisungen und Prüflisten** | **7** | `clients/README.md` Abschnitt 5 Schritt 3, `governance/CHANGE_REQUEST_TEMPLATE.md`, `tests/TEST_CATALOG.md` (Erwartungswert `FW-AK-01`), `build/doc/32-abschluss.md` (4) |
| **im Prüfapparat** | **8** | `validate-framework.py` (Registereinträge 34 und 46, drei Kopfkommentare, **die Prüfbedingung selbst**), `probe-pruefungen.py` (1) |

> 🔴 **Die Zahl stand bis zum Durchgang vor dem Commit auf „vier", und sie war an den
> ZEILEN dieser Tabelle abgelesen, nicht am Bestand** – die vierte Zeile führte fünf
> Träger auf einmal. *Dieselbe Bauform wie „eine mit `head` abgeschnittene Ausgabe trägt
> keine Zahl" (0.77.0), hier an einer Erläuterungstabelle statt an einer
> Werkzeugausgabe.* **Nachgezählt ist an den gefahrenen Ersetzungen.**

🟢 **Was NICHT angefaßt wurde, und das ist die Trennlinie:** Fundstellen, die eine
**Messung von damals berichten** – `claude-code` Zeile `R5` (*„Der VERIFY-Marker ist damit
aufgelöst"*), der Notiztext im Manifest von `devin-desktop`, die Ergebniszelle von
`FW-AK-01`, die Änderungsverläufe beider Packs, `build/doc/31-anhaenge.md`. *Ein Bericht
von gestern ist nicht bearbeitbar* – dieselbe Regel, die Gegenprobe `46c` für die
Protokolle durchsetzt.

## 3. Der Eingriff – achtzehn Fundstellen, je mit ihrer Auflösung

**Sechzehn sind sachlich aufgelöst, zwei sind umgewidmet – und die beiden sind dieselbe
Frage.** Das ist die Bedingung, unter der D-294 trägt: *Kriterium 1 wäre sonst durch
bloßes Umetikettieren erfüllbar.*

| Auflösung | Zahl | Fundstellen |
|---|---|---|
| **durch eine Messung von `0.86.0`** | **5** | `clientmap.py` (`B3`/D-277), `fw-mr-description`, `fw-review-support` (`S3`/D-287), `fw-review-support` (`A1`/D-284), `SKILL_TEMPLATE` (`S3`) |
| **durch einen Verweis auf die Fähigkeitsmatrix** | **3** | `02-privacy.md` (2×), `hook-overlay-status.py` |
| **reine Nennung, umformuliert** | **5** | `checklists/11`, `clients/README`, `RELEASE_PROCESS`, `ROADMAP` (`AP2`), `DECISION_LOG` (`A-05`) |
| **Register und Glossar, entfallen** | **3** | `PLACEHOLDER_REGISTRY` (2×), `00-principles.md` |
| **umgewidmet, dauerhaft offen** | **2** | Zeile `X2` des Packs `devin-desktop` **und** die Nachweiszelle von `K-20` – zwei Fundstellen, **eine Frage** (D-292) |
| **Summe** | **18** | dazu `.devin/config.json`, nicht versioniert |

> 🔴 **DIESE TABELLE IST DER BEFUND DES DURCHGANGS VOR DEM COMMIT, UND ZWAR DER
> EINUNDDREISSIGSTE IN FOLGE.** Sie stand zuerst auf **7 / 3 / 5 / 3 / 1** und summierte
> sich auf **19** – bei achtzehn gezählten Fundstellen. Zwei Fehler auf einmal: `.devin/
> config.json` war unter den gezählten mitgeführt, **obwohl es in `.gitignore` steht**,
> und die Zeile `X2` und die Nachweiszelle von `K-20` waren als **eine** Fundstelle
> geführt, weil sie **eine** Frage sind. *Wer nach der Art der Auflösung gruppiert,
> zählt Fragen; der Zähler zählt Fundstellen.* **Gezählt sind 18; behandelt sind 18 + 6 +
> 4 = 28.**

### 3.1 Die eine Zeile, die offen bleibt

Zeile `X2` des Packs `devin-desktop` sagt seither:

```
`BELEG OFFEN (dauerhaft)` – von außen nicht zu beobachten, Stand 2026-09-22 (`K-20`, D-292).
```

🔴 **Der Unterschied zum Marker ist keine Schreibweise, sondern die Frist.** Das Register
schrieb der Markerform *„vor Version 1.0.0"* vor; `BELEG OFFEN` trägt keine. *Eine Frage,
die dauerhaft nicht beobachtbar ist, kann keine Frist einhalten* – und der Marker hat sie
achtundneunzig Releases lang als Rückstand geführt – die Zeile `X2` steht unverändert seit `0.7.0` (`git log -S`), und zwischen `0.7.0` und `0.87.0` liegen 98 Einträge im Changelog. ⚠️ **Geschätzt stand hier „achtzig“; der Durchgang vor dem Commit hat auch diese Zahl kassiert.**

## 4. Was Prüfung 46 danach zählt (D-293)

**Der Zähler bleibt, unverändert, und wird zur Rückfallsperre umgewidmet.** Muster und
Zählbereich sind wörtlich dieselben; was sich ändert, ist die Lesart: **Die Zahl war ein
Arbeitsvorrat und ist jetzt ein Pegel gegen die Wiedereinführung.**

🟢 **Die Null ist gemessen und nicht konstruiert, und das ist der Prüfstein dieses
Releases.** *Die Null durch Konstruktion* (0.59.1) und *der Wächter, der mit dem
Schnittmuster prüft* (0.75.0, D-205) sind genau die Bauformen, in die dieser Schritt sonst
fiele. Zwei Dinge halten ihn davon ab:

1. **Die Sonden bringen ihren Gegenstand selbst mit.** Sonde `46c` schreibt einen Marker
   nach `framework/core/03-security.md` und verlangt die Meldung; Gegenprobe `46c`
   schreibt einen in ein datiertes Protokoll und verlangt ihr **Ausbleiben**. Keine von
   beiden setzt einen Marker im Bestand voraus – die Abhilfe aus dem Wirkungsnachweis
   `0.86.0` Abschnitt 2a, hier zum ersten Mal an einem Schnitt bewährt, der ihren
   Gegenstand vollständig entfernt.
2. **Die Vollständigkeit des Schnitts wird NICHT am Zähler abgelesen**, sondern am zweiten
   Muster aus 2.5. *Ein Wächter braucht ein weiteres Muster als der Schnitt.*

⚠️ **Verworfen: der Ausbau.** D-11 verlöre seinen einzigen maschinellen Zähler für
Kriterium 1, die Standzeile fiele von vier Zahlen auf drei, und eine Wiedereinführung der
Form fiele niemandem auf. ⚠️ **Preis des gewählten Wegs, benannt:** Eine Zahl, die dauerhaft
auf null steht, wird nicht mehr gelesen; sie trägt nur, solange ihre Sonde läuft.

## 5. Nebenbefund: der vierte Träger, schon wieder

`clientmap.py` erzeugt den `_comment` der Berechtigungsdatei, und darin stand die
Markerform. **`install.py --update` faßt die Berechtigungsdatei nicht an**, weil sie
Projektwerte enthält – die Änderung an der Quelle erreicht eine **bereits installierte**
Datei also nicht. Die Laufzeitschicht dieses Repositoriums ist von Hand nachgezogen worden.

➡️ *Derselbe vierte Träger wie 2026-09-18 bei `<EXCLUDED_PATHS>`* – dort hat es zwei
Releases gedauert, bis es auffiel. **Hier ist es beim Trockenlauf aufgefallen**, weil
`install.py --dry-run` die Datei ausdrücklich unter „Projektdateien unberührt gelassen"
ausweist.

## 5a. Welche Träger gehoben werden – und die zwei, die es nicht werden

**Gehoben sind die Träger, deren normativer Text sich geändert hat:** `00-principles.md`
(0.1.4), `01-governance.md` (0.3.2), `02-privacy.md` (0.1.8), `clients/README.md` (0.6.0),
`SKILL_TEMPLATE.md` (0.1.3), `checklists/11` (0.2.3), `RELEASE_PROCESS.md` (0.1.4) sowie
beide Client Packs (`devin-desktop` 0.14.0, `claude-code` 0.24.0).

🔴 **Die beiden Skills `fw-mr-description` und `fw-review-support` werden NICHT gehoben,
und das ist eine Entscheidung mit Preis.** *Eine angehobene Skillversion setzt die
abgenommenen Zellen seines Testblatts auf die Fassung davor* (D-119). **`0.79.0` hat genau
das getan** – beide Skills in demselben Commit gehoben, der zwei ihrer Zellen abgenommen
hat –, und Kriterium 2 ist daraufhin **aufwärts** gegangen (D-227). Wörtlich angewandt
ginge es hier **von null wieder aufwärts, in demselben Release, das Kriterium 1 auf null
bringt.**

⚠️ **Der Eingriff an beiden Skills betrifft eine `(Erläuterung)`** – kein Arbeitsschritt,
kein Frontmatterfeld, keine Zusage. **Entschieden wird hier nichts:** Die Frage, wann eine
Skillversion steigen muß und was das die abgenommenen Zellen kostet, ist `K-84`, und `K-84`
ist offen. **Preis, benannt:** Zwei Skills tragen eine unveränderte Version bei geändertem
Text.

🟢 **Die Client Packs sind der Gegenfall, und er ist nachgezählt:** **Keine** Zelle eines
Testblatts und keine Zelle des zentralen Katalogs nennt eine **Packversion** – sie nennen
den **Produktstand** des Clients (D-117, D-202), etwa `2.1.274` oder `3.10.31`. Eine Hebung
des Packs altert deshalb keine Zelle. *Die Asymmetrie hat einen gemessenen Grund und ist
keine Ungleichbehandlung.*

## 6. Abnahme

| Gegenstand | Ergebnis |
|---|---|
| Kriterium 1 vorher / nachher | **18 → 0** |
| Kriterium 2, 3, 4 | **0 / 0 / 0**, unberührt |
| Literale Fundstellen, versioniert, außerhalb der Chronik | **0** (vorher 24) |
| Literale Fundstellen, Chronik | **15**, unberührt (Gattungsausnahme E2) |
| Literale Fundstellen, nicht versioniert | `.devin/` **0** (vorher 4), `build/out/hauptdokument.md` **32** – beide in `.gitignore`, letzteres bis zum nächsten Bau |
| Zweites Muster: Nennungen des Wortes außerhalb der Chronik | **4 konstituierende umformuliert**, berichtende stehen gelassen |
| Validator | *siehe unterhalb der Trennlinie* |
| Sondenlauf, beide Kodierungsumgebungen | *siehe unterhalb der Trennlinie* |

## 7. Was offen bleibt, und es ist benannt

- **`K-98` (neu):** Soll eine Prüfung die Abwesenheit der Form auch außerhalb des
  Zählbereichs durchsetzen – `README.md` und die fünf Quellen unter `build/doc/`? **Hier
  nicht entschieden**, weil die Anweisung vom 15.09. gilt: *keine neue Prüfung, solange
  eine Zahl zu senken ist*, und Kriterium 1 war genau diese Zahl. ⚠️ **Nach diesem Release
  greift sie nicht mehr** – keine der vier Zahlen steht mehr offen.
- **`K-20` bleibt offen, und dauerhaft** (D-292). Die Frage bleibt, die Marke nicht.
- **Daß eine unbelegte Aussage überhaupt gekennzeichnet wird, setzt keine Prüfung durch** –
  dieselbe Bauform wie `K-41`. Durchgesetzt bleiben Prüfung 73 (Quellenkennung je
  `[DOK]`-Zeile) und Prüfung 74 (die Zeile steht in ihrer Tabelle).
- **`build/out/hauptdokument.md` führt die Form noch 32mal.** Es ist nicht versioniert,
  über vierzig Releases zurück und gehört zu `AP11`; die Quellen darunter sind gepflegt,
  und der nächste Bau löst es auf.

---

*Laufzeiten und Abnahmeläufe (D-94, unterhalb der Trennlinie – sie sind nicht Teil des
zeilengleichen Vergleichs):*

| Lauf | Kodierungsumgebung | Einheiten | Ausgang | Wanduhr |
|---|---|---|---|---|
| Validator | ohne und mit `PYTHONIOENCODING=utf-8` | – | **0 Fehler, 0 Warnungen** | < 10 s |
| Sondenlauf A | **ohne** `PYTHONIOENCODING` | **415 von 415** | **alle bestanden**, Exit 0 | 440,5 s (3489,5 s Rechenzeit, 8 Bahnen, Faktor 7,9) |
| Sondenlauf B | **mit** `PYTHONIOENCODING=utf-8` | **415 von 415** | **alle bestanden**, Exit 0 | 450,8 s (3570,6 s Rechenzeit, 8 Bahnen, Faktor 7,9) |

🟢 **Der zeilengleiche Vergleich nach D-49 ist gefahren:** Die Ausgaben beider Läufe
oberhalb der Trennlinie sind **Zeile für Zeile identisch** (`diff` → null Unterschiede).

🟢 **Und der Punkt, auf den es bei diesem Release ankam: KEINE SONDE HAT IHREN
GEGENSTAND VERLOREN.** `0.86.0` hat sieben gefällt, weil ein Eingriff den Gegenstand
entfernte, den sie im Bestand voraussetzten – **und der Validator war bei allen sieben
grün.** Dieses Release entfernt den Gegenstand einer Zählung **vollständig**, und die
beiden Sonden dazu laufen durch, weil sie ihn seither selbst mitbringen.

⚠️ **Der Abnahmelauf war ein eigener Lauf – und er ist ZWEIMAL gefahren worden, mit Absicht.**
Der erste Durchgang (446,9 s / 438,6 s, ebenfalls 415 von 415 und zeilengleich) lief gegen
einen Baum, dem danach noch etwas zugewachsen ist: die Hebung von sieben Modulträgern und
beiden Client Packs, die Entscheidung E9 und zwei berichtigte Zahlen. **Ein Sondenlauf mißt
den Baum, in dem er startet** – also ist er neu gefahren worden, statt behauptet zu werden.
*`0.86.0` hat dieselbe Regel gebrochen und 418 Sekunden zweimal bezahlt; hier sind es 891
Sekunden, und sie sind eingeplant gewesen.* 🟢 **Die Tabelle oben nennt den ZWEITEN
Durchgang** – den gegen den ausgelieferten Baum.

