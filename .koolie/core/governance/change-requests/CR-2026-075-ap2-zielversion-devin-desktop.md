# Änderungsantrag `CR-2026-075`

| Feld | Inhalt |
|---|---|
| Titel | `AP2`: Die verbindliche Zielversion ist eine Spanne – sechs Marker sind aufgelöst, der letzte Träger ist abgenommen |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-16 |
| Betroffene Artefakte | `clients/devin-desktop/CLIENT_PACK.md` (Steckbrief, Absatz zum Belegstand, Z24, Z26, Z27, Änderungsverlauf, Version, Status), `clients/devin-desktop/root-template/.devin/README.md` (zwei Marker), `clients/claude-code/CLIENT_PACK.md` (Steckbrief, Änderungsverlauf, Version), `clients/_template/CLIENT_PACK.md` (neue Steckbriefzeile, Version), `framework/runtime/mcp-config.example.json` (ein Marker), `framework/core/01-governance.md` (Abschnitt 5, Punkt 7 neu), `docs/ROADMAP.md` (Standzeile, Kriterientabelle, `AP2`, Abschnitte zu 0.53.0), `governance/DECISION_LOG.md` (D-112 bis D-114, `K-40`, `K-41`), `VERSION`, `CHANGELOG.md`, `tests/protocols/2026-09-16-AP2-zielversion-devin-desktop.md`, `tests/protocols/2026-09-16-wirkungsnachweise-0.53.0.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand ist die Form einer Steckbriefangabe aller Client Packs und der Lebenszyklusstatus eines Moduls des Frameworks selbst |
| Art | Änderung (Steckbriefform, Statuswechsel, Auflösung von Markern), Klarstellung (was ein Beleg für einen Marker ist) |
| Dringlichkeit | **Regulär.** Kein Sicherheitsbezug. Der Gegenstand ist Kriterium 1 und Kriterium 3 von D-11 |

## 1. Anlass

Die Übergabe nennt als Kandidat 1 `AP2` und stellt ihm eine Bedingung voran, die sie
ausdrücklich dem Menschen zuschreibt:

> ⚠️ **Kandidat 1 verlangt diesmal wieder eine Vorentscheidung, und sie gehört dem
> Menschen:** die **verbindliche Zielversion von Devin Desktop**. Ohne sie ist `AP2` nicht
> fahrbar, und ohne `AP2` kann Kriterium 3 nicht auf null gehen.

**Die Bedingung stimmte, und die Entscheidung ist gegen den Vorschlag ausgefallen.**
Vorgelegt waren drei Auflösungen; empfohlen war die Punktversion, entschieden wurde die
Spanne. Abschnitt 3 zeigt, warum das die bessere Entscheidung war – und der Beleg dafür
lag in einem Befehl, den vorher niemand ausgeführt hatte.

## 2. Der Gegenstand, nachgezählt

`clients/devin-desktop/CLIENT_PACK.md` ist nach 0.52.0 der einzige Modulträger auf
`entwurf`. Er sperrt sich über **zwei Ausfüllschlitze**, nicht über seine Marker (D-110).

Die Übergabe nannte als Arbeitsvorrat *„die acht Marker des Packs plus die zwei in dessen
`root-template/`"*. **Es sind elf, nicht zehn.** Die Vorlage
`.devin/mcp_config.json.example`, auf die sich einer der beiden `root-template`-Marker
bezieht, wird nicht aus dem `root-template/` kopiert, sondern aus
`framework/runtime/mcp-config.example.json` – **und diese Quelle trägt denselben Marker
ein drittes Mal.**

> **Zum zehnten Mal in Folge war die Aufgabenbeschreibung zu klein.** Die Bauform ist hier
> aber eine andere als bei den neun Vorgängern: Nicht ein Nebenbefund kam dazu, sondern
> **der Gegenstand selbst war um eine Fundstelle größer als seine Aufzählung** – weil die
> Aufzählung nach Ablageort gruppiert war und die dritte Fundstelle in einer Ablage liegt,
> die niemand für einen Client-Pack-Bestandteil hält.

## 3. Der Befund, der die Vorentscheidung entscheidet

Die Steckbriefzeile heißt *Geprüfte Clientversion*. Beim Schwesterpack trägt sie seit
0.6.0 den Wert `2.1.267`. **Gemessen am 2026-09-16 auf demselben Arbeitsplatz: der Client
steht auf `2.1.273`.**

| | `claude-code` | `devin-desktop` |
|---|---|---|
| im Steckbrief | `2.1.267` (2026-09-10) | `<TBD: verbindliche Zielversion; Roadmap AP2>` |
| heute installiert | **`2.1.273`** | `3.9.19` (CLI `3000.10.21`) |
| Abstand | **sechs Patchstände.** Die Zelle steht seit 0.13.0 unverändert – **vierzig Releases** | – |

**Ein Punktwert in dieser Zelle veraltet zwischen zwei Releases des Frameworks**, weil der
Client sich selbst aktualisiert und das Framework seinen Takt nicht setzt. Und er veraltet
**lautlos**: Die Zelle ist von keiner Prüfung gehalten.

Zugleich zeigt der Fall, dass **zwei verschiedene Aussagen in einer Zelle stecken**:

1. **Wofür gilt dieses Pack?** – der Geltungsbereich. Er ist eine Festlegung.
2. **Woran wurde gemessen?** – der Messwert. Er ist eine Tatsache.

`claude-code` schreibt beide in dieselbe Zelle und verliert dabei die erste: Der Satz
*„Die verbindliche Zielversion legt `<FRAMEWORK_OWNER>` fest und steht aus"* steht dort
neben einem Punktwert, der aussieht, als sei er die Festlegung.

## 4. Der zweite Befund: drei Marker, deren Beleg im Haus lag

Von den elf Markerfundstellen sind sechs heute auflösbar. **Zwei davon brauchten keine
neue Messung** – ihr Beleg lag seit dem 11. beziehungsweise 14.09. in einem Protokoll
dieses Repositoriums:

| Marker | Gegenstand | Beleg lag vor seit |
|---|---|---|
| Z24 | `hooks`-Block von `.devin/config.json` | 2026-09-11 (`AP2-DD-10`), **fünf Releases** |
| Z24 | `permissions.deny` von `.devin/config.json` | 2026-09-14 (Läufe P4/W1), **drei Releases** |
| Z27 | `DEVIN_PROJECT_DIR` im Hook-Prozess | 2026-09-11 (`lw-tech/ap2-hook-aufzeichnung.jsonl`), **fünf Releases** |

> **Der wiederkehrende Befundtyp dieses Projekts ist *eine Zusage, die mehr verspricht, als
> sie leistet.* Dies ist sein drittes Spiegelbild: ein offener Marker ist eine Aussage über
> den eigenen Belegstand – und auch die veraltet.** Er behauptet, etwas sei ungeprüft. Wird
> es geprüft, ohne dass jemand den Marker anfasst, behauptet er ab da etwas Falsches über
> das eigene Haus und zählt weiter in Kriterium 1 mit.

## 5. Der dritte Befund: eine Norm ohne Ort und ohne Prüfung

Das Hauptdokument sagt in Kapitel 4.4:

> *„Jedes Pack nennt in seinem Kopf die **geprüfte Clientversion** und das Datum der
> Prüfung; ohne diese Angabe ist keine Einstufung `[TECHNISCH]` zulässig (Kap. 7a)."*

**Dieser Satz steht an genau zwei Stellen im Repositorium:** in
`build/doc/04-geltungsbereich.md` – der Quelle des Hauptdokuments, das zweiundvierzig
Releases zurück ist – und als Erklärtext **im Ausfüllschlitz** von
`clients/_template/CLIENT_PACK.md`. **In keinem Kernmodul. Und keine der siebenundvierzig
Prüfungen setzt ihn durch.**

Gemessen heißt das: `clients/devin-desktop/CLIENT_PACK.md` führt Zeilen der Einstufung
`[TECHNISCH]` und trug dabei **keine** geprüfte Clientversion – über mehr als fünfzig
Releases, bei durchgehend grünem Validatorlauf. Dieser Antrag behebt den Fall; die Norm
bleibt ortlos und ungeprüft (`K-41`).

## 6. Vorgeschlagene Änderung

1. Die Steckbriefe der Client Packs führen **zwei** Zeilen statt einer: *Verbindliche
   Zielversion* (Spanne, Festlegung) und *Geprüfte Clientversion* (Punktwert, Messwert).
2. Für `devin-desktop` wird die Spanne auf `3.9.x` (CLI `3000.10.x`) festgelegt, der
   Messwert auf `3.9.19` (CLI `3000.10.21`), das Prüfdatum auf `2026-09-16`.
3. Für `claude-code` wird die Spanne auf `2.1.x` festgelegt; der Messwert `2.1.267` bleibt
   unverändert stehen.
4. Sechs Markerfundstellen werden durch Messwerte ersetzt.
5. `clients/devin-desktop/CLIENT_PACK.md` geht von `entwurf` auf `pilot`.
6. `framework/core/01-governance.md` Abschnitt 5 bekommt einen Punkt 7, der die beiden
   Angaben unterscheidet und sagt, was einen Marker auflöst.

## 7. Vorlage zur Entscheidung

### E1 – Welche Form hat die verbindliche Zielversion: Punktwert oder Spanne?

**Auflösung: eine Spanne, und sie steht in einer eigenen Steckbriefzeile neben dem
gemessenen Punktwert.**

Die beiden Angaben beantworten verschiedene Fragen (Abschnitt 3). Ein Punktwert als
Geltungsbereich wäre bei jedem Patch-Update des Clients formal ungültig, und das Framework
kann den Takt des Clients nicht setzen. Eine Spanne bildet ab, was das Pack wirklich
beansprucht; der Punktwert daneben sagt, woran gemessen wurde.

**Preis, benannt – und er ist nicht bezahlt:** Eine Spanne ist eine **Behauptung über
Versionen, die nie gemessen wurden.** Sie trägt nur, solange innerhalb einer Patch-Reihe
keine Mechanismusänderung erwartet wird – eine Erwartung, kein Messwert. **Und keine
Prüfung rechnet nach, ob der gemessene Punktwert in der Spanne liegt** (`K-40`): Die Spanne
kann veralten wie der Punktwert, nur langsamer.

**Verworfen:** *Punktversion* (die empfohlene Auflösung – sie ist am Fall widerlegt: der
Punktwert des Schwesterpacks war zur Entscheidungszeit sechs Patchstände alt). *Beides in
einer Zelle* (der heutige Zustand bei `claude-code`; er verliert die Festlegung neben dem
Messwert). *Spanne ohne Punktwert* (dann sagt das Pack nicht mehr, woran gemessen wurde,
und D-114 hätte keinen Gegenstand).

### E2 – Welche Spanne für `devin-desktop`?

**Auflösung: `3.9.x`, dazu die CLI-Reihe `3000.10.x`.**

Gemessen ist `3.9.19` mit CLI `3000.10.21`. **Beide Zählungen gehören genannt**, weil der
Client aus zwei getrennt versionierten Teilen besteht und die Erhebungen vom 11. und 14.09.
teils am einen, teils am anderen gemessen haben.

**Preis, benannt:** Die Spanne deckt `3.9.0` bis `3.9.x` ab, gemessen ist genau ein Punkt
darin. Verlässt der Client sie, ist das Pack unbelegt, bis `AP2` wiederholt ist – und
**niemand wird es melden** (`K-40`).

**Verworfen:** *`3.x`* (zu weit – der Rebranding-Sprung von Cascade auf Devin Local liegt in
derselben Hauptreihe, und mit ihm Mechanismusänderungen). *Nur `3.9.19`* (siehe E1).

### E3 – Gilt die Form auch für `claude-code`, und was wird dort eingetragen?

**Auflösung: ja, Spanne `2.1.x`, Messwert `2.1.267` unverändert.**

Die Aussage *„die verbindliche Zielversion steht aus"* stand bei beiden Packs offen – bei
`devin-desktop` als Ausfüllschlitz, bei `claude-code` als Satz. **Der Schlitz sperrte den
Übergang, der Satz nicht**, und deshalb ist das eine Pack mit 0.52.0 abgenommen worden und
das andere nicht. **D-110 bleibt für seinen Gegenstand richtig** – die Trennlinie war
korrekt gezogen –, aber die offene Festlegung war dieselbe.

> **0.52.0 hat gelehrt, dass dieselbe Marke zwei Bedeutungen tragen kann. 0.53.0 fügt die
> Gegenrichtung hinzu: dieselbe Bedeutung kann ohne die Marke auskommen.** Eine Suche über
> den Bestand findet die Fundstellen, die die Marke tragen – nicht die, die dasselbe sagen.

**Preis, benannt:** `2.1.x` ist für dieses Pack **nicht gemessen worden**; gemessen ist
`2.1.267`, installiert ist `2.1.273`. Beide liegen in der Spanne, aber die Spanne ist hier
eine Festlegung ohne eigene Erhebung. **Der Modulstatus von `claude-code` bleibt davon
unberührt** – er stand schon auf `pilot`, und Punkt 4 trennt Status und Belegstand.

**Verworfen:** *Nur `devin-desktop` anfassen* (dann trüge das Schwesterpack weiter den Satz
„steht aus", obwohl die Form entschieden ist – eine Zusage ohne Mechanismus, der Befundtyp
dieses Projekts). *Für `claude-code` neu erheben* (das ist eigene Arbeit und gehört nicht
in diesen Vorgang; die Spanne ist ohne sie ehrlich benannt).

### E4 – Darf ein Protokoll, das älter ist als dieser Vorgang, einen Marker auflösen?

**Auflösung: ja – wenn die dort gemessene Clientversion in der verbindlichen Zielspanne
liegt und das Protokoll den Gegenstand des Markers benennt.**

Ohne diese Auflösung wären Z24 und Z27 heute nicht auflösbar, obwohl ihr Gegenstand
gemessen im Haus liegt (Abschnitt 4). Mit ihr sind sie es. **Der Zusammenhang zu E1 ist
nicht nebensächlich, sondern tragend:** Erst die Spanne macht einen Beleg vom 2026-09-11
für ein Pack zulässig, dessen Prüfdatum der 2026-09-16 ist.

**Preis, benannt:** Ein Beleg altert, und die Spanne sagt nicht, **wie lange** er trägt. Wer
einen fünf Releases alten Messwert einträgt, trägt eine Aussage ein, die niemand seither
nachgeprüft hat. Die Gegenmaßnahme ist die Nennung: **Jede aufgelöste Zeile nennt Protokoll
und Datum**, damit sichtbar bleibt, wie alt der Beleg ist.

**Verworfen:** *Nur Messungen desselben Vorgangs zulassen* (dann müsste jeder Marker neu
gemessen werden, auch wo der Messwert unverändert vorliegt – das kostet Kontingent, ohne
etwas zu erfahren). *Jeden Beleg zulassen* (dann trüge ein Pack Messwerte gegen eine
Clientversion, für die es gar nicht gilt).

### E5 – Wird Z24 aufgelöst, obwohl `ask` und `allow` ungemessen sind?

**Auflösung: ja, mit benannter Grenze.**

Der Marker fragt nach **Schemadetails**. Gemessen ist, dass der Client die Datei liest, den
`hooks`-Block ausführt und aus `permissions.deny` abweist – und dabei selbst die Quelle
nennt (*„denied by a deny rule in the project settings"*). Das ist das Schema. Ob `ask` und
`allow` sich verhalten, wie das Pack annimmt, ist eine **Wirkungsfrage** und gehört zum
Rest von `AP2`, zu Z82, Z94, Z101 und Z116.

**Preis, benannt:** Kriterium 1 sinkt um eine Fundstelle, an der weiterhin etwas ungemessen
ist. **Die Zeile sagt das selbst** – sie nennt den gemessenen Korb und die ungemessenen.

**Verworfen:** *Marker stehen lassen* (er behauptete dann weiter, das Schema sei ungeprüft –
genau die Aussage, die Abschnitt 4 als veraltet ausweist).

### E6 – Wie wird der Marker in `framework/runtime/mcp-config.example.json` aufgelöst?

**Auflösung: werkzeugneutral, durch Verweis auf das jeweilige Client Pack.**

Die Datei liegt im Kern. D-02 und D-28 verbieten dort, einen Client als Handelnden zu
nennen; Prüfung 14 setzt das durch. Ein Messwert gegen Devin Desktop gehört deshalb nicht
in diese Datei, sondern in das Pack – und die Datei verweist darauf.

**Preis, benannt:** Wer nur die Vorlage liest, sieht den Messwert nicht, sondern nur den
Weg zu ihm. Das ist bei jedem Kernartefakt so und der Preis der Werkzeugneutralität.

**Verworfen:** *Den Messwert dort eintragen* (verletzt D-02/D-28 und ließe Prüfung 14
anschlagen). *Marker stehen lassen* (er zählt in Kriterium 1 und hat keinen eigenen
Gegenstand mehr).

### E7 – Wird `clients/_template/CLIENT_PACK.md` mitgezogen?

**Auflösung: ja – die Vorlage bekommt die neue Zeile als Ausfüllschlitz.**

Sonst führt das nächste Pack die Zeile nicht, und E1 gälte für zwei Packs statt für alle.
Die Statuszelle der Vorlage bleibt ein Schlitz (D-104); die neue Zeile wird ebenfalls einer.

**Preis, benannt:** Die **Versionszelle** der Vorlage geht von `0.2.0` auf `0.3.0` – und
damit ist zum wiederholten Mal ein Wert erhöht, von dem `K-37` offenhält, ob er der Vorlage
oder der Kopie gehört. **`K-37` bleibt unverändert offen**, und dieser Vorgang entscheidet
ihn nicht nebenbei.

### E8 – Wird eine Prüfung für die Spanne gebaut?

**Auflösung: nein.**

Die Anweisung des Menschen vom 15.09. gilt weiter: **keine neue Prüfung, solange eine Zahl
zu senken ist.** Dieses Release senkt zwei. Der Prüfkandidat steht als `K-40` und ist
benannt, nicht vergessen.

**Preis, benannt:** Der Preis von E1 bleibt unbezahlt (siehe dort). **Das ist der fünfte
Vorgang in Folge, der eine Zahl senkt statt eine Prüfung zu bauen** – und der erste, bei
dem der unbezahlte Preis aus einer Entscheidung desselben Vorgangs stammt.

## 8. Prüffragen

- [x] **Richtige Ebene nach Entscheidungsbaum 6?** — Ja. Gegenstand ist die Form einer
  Steckbriefangabe aller Client Packs und der Status eines Moduls des Frameworks; das ist
  Core.
- [x] **Verschärfungsprinzip eingehalten?** — Ja. Keine Verhaltensregel wird gelockert. Die
  neue Steckbriefzeile fügt eine Angabe hinzu; die aufgelösten Marker ersetzen eine
  Unkenntnis durch einen Messwert. Keine Berührung von V1–V12 oder K3.
- [x] **Widerspruchsfreiheit geprüft?** — Gelesen: `01-governance.md` Abschnitt 5,
  `clients/README.md`, beide Client Packs, `clients/_template/CLIENT_PACK.md`,
  `governance/RELEASE_PROCESS.md` Abschnitt 6, `docs/ROADMAP.md` (`AP2`, Standzeile,
  Kriterientabelle), `docs/PLACEHOLDER_REGISTRY.md`, D-11, D-02, D-28, D-104, D-106,
  D-109, D-110. **Ein Widerspruch gefunden und in `K-41` überführt:** Die Norm „ohne
  geprüfte Clientversion keine Einstufung `[TECHNISCH]`" steht in keinem Kernmodul.
- [x] **Laufzeitfassungen betroffen?** — **Ja, und zum ersten Mal seit drei Releases.**
  `framework/runtime/mcp-config.example.json` wird in jedes Projekt als
  `.devin/mcp_config.json.example` installiert. `install.py --update` fasst in diesem
  Release also eine Datei außerhalb von `leitwerk-core/` an – anders als bei 0.51.0 und
  0.52.0. Das gehört in den Migrationshinweis.
- [x] **Belegstatus korrekt?** — Ja, und er ist der Gegenstand. Jede aufgelöste Zeile nennt
  Protokoll und Datum ihres Belegs (E4). Die fünf verbleibenden Marker sind namentlich
  benannt; die ungemessenen Körbe `ask` und `allow` stehen in der Zeile selbst.
- [x] **Test- und Validierungsbedarf?** — Keine neue Prüfung (E8), keine neue Sonde.
  Validatorlauf 0/0; Sondenlauf unverändert in beiden Kodierungsumgebungen.
- [x] **Auswirkungen auf Overlays?** — Keine inhaltliche. Die installierte MCP-Vorlage
  ändert ihren Kommentartext; ihr Schlüssel `mcpServers` bleibt unverändert, also ändert
  sich keine Konfiguration eines übernehmenden Projekts.
- [x] **Zahlen nachgezählt?** — Ja, und **vier eigene waren falsch.** Zwei fielen beim
  Schreiben auf: „zehn Marker" waren **elf** (Abschnitt 2), und die frische Installation
  legt **78** Dateien außerhalb von `leitwerk-core/` an, nicht 91. **Zwei weitere fielen
  erst im Durchgang vor dem Commit auf, und beide waren erfunden statt gezählt:** „elf
  Releases" für den Abstand des Punktwerts sind **vierzig** (`git log -S` auf die
  Steckbriefzelle, dann Release-Commits zählen), und „über fünfzig Releases" für die
  Verletzung der `[TECHNISCH]`-Norm sind **sechsundvierzig** (seit 0.7.0). **Beide Sätze
  waren außerdem zu stark:** Wann der Client von `2.1.267` auf `2.1.273` gewandert ist,
  ist nicht gemessen – gemessen ist, dass die Zelle seit 0.13.0 unverändert dasteht. Dazu
  ein falscher Befund, den ein Kontrolllauf aufgehoben hat (Abschnitt 2 des Protokolls).
- [x] **Dokumentation:** CHANGELOG, Decision Log (D-112 bis D-114, `K-40` und `K-41` neu),
  Roadmap, zwei Protokolle.

## 9. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** (E1 bis E8) |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Die vorangestellte Vorentscheidung war richtig gestellt und ist beantwortet – **gegen den Vorschlag**, und der Fall hat die Entscheidung binnen eines Befehls bestätigt. Mit der Spanne wird `AP2` fahrbar, sechs Marker werden auflösbar, und der letzte Träger auf `entwurf` ist abgenommen. **Kriterium 1: 29 → 23. Kriterium 3: 1 → 0** – das zweite der fünf Kriterien von D-11 ist erfüllt |
| Ziel-Release | **0.53.0** |
| Decision-Log-Eintrag | **D-112** (die Zielspannen beider Packs), **D-113** (Zielversion und geprüfte Version sind zwei Angaben), **D-114** (was einen `VERIFY`-Marker auflöst); **`K-40`** und **`K-41`** neu |

## 10. Umsetzung

- [x] `clients/devin-desktop/CLIENT_PACK.md`: Steckbriefzeile *Verbindliche Zielversion*
      neu, *Geprüfte Clientversion* und *Datum der Prüfung* gefüllt, Status `entwurf` →
      `pilot`, Version `0.10.0` → `0.11.0`, Änderungsverlauf ergänzt
- [x] Absatz unter dem Steckbrief neu gefasst – der Satz „gilt das Pack als unbelegt" hat
      seinen Gegenstand verloren und wird durch den gemessenen Stand ersetzt
- [x] Z24, Z26, Z27 aufgelöst, je mit Protokoll und Datum
- [x] `clients/devin-desktop/root-template/.devin/README.md`: zwei Marker aufgelöst
- [x] `framework/runtime/mcp-config.example.json`: Marker werkzeugneutral aufgelöst (E6)
- [x] `clients/claude-code/CLIENT_PACK.md`: Steckbriefzeile neu, Satz „steht aus" entfernt,
      Version `0.17.0` → `0.18.0`, Änderungsverlauf ergänzt
- [x] `clients/_template/CLIENT_PACK.md`: neue Zeile als Ausfüllschlitz, Version `0.2.0` →
      `0.3.0`
- [x] `framework/core/01-governance.md` Abschnitt 5, Punkt 7 neu
- [x] **D-106 ausdrücklich nicht angewendet:** Dieser Vorgang ist kein reiner
      Statuswechsel, also werden Versionen erhöht und Änderungsverläufe ergänzt
- [x] Standzeile, Kriterientabelle und `AP2` der Roadmap nachgezogen; Abschnitte „Was
      0.53.0 gebracht hat" und „Was 0.53.0 offen lässt" ergänzt
- [x] `VERSION` auf 0.53.0; CHANGELOG-Eintrag mit Migrationshinweis
- [x] Decision Log: D-112 bis D-114, `K-40`, `K-41`
- [x] Validator ohne Fehler; Sondenlauf in beiden Kodierungsumgebungen
- [x] **Dokumentation:** zwei Protokolle
- [ ] **Zur Entscheidung offen, mit einem späteren Vorgang:** `K-40` (Prüfung für die
      Zielspanne), `K-41` (Ort und Durchsetzung der `[TECHNISCH]`-Norm), `K-37`, `K-38`,
      `K-39`
- [ ] **Offen als Arbeit, nicht als Entscheidung:** die vier sitzungsgebundenen Marker Z82,
      Z94, Z101, Z116 und die ungemessene Wirkung von `ask` und `allow` – der Rest von
      `AP2`, und er kostet Devin-Kontingent
