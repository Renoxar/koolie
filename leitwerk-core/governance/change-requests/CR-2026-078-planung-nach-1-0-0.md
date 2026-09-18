# Änderungsantrag `CR-2026-078`

| Feld | Inhalt |
|---|---|
| Titel | Der Weg bis 1.0.0 bekommt einen Releaseplan – und die drei Änderungen danach ein Ziel-Release, einen Parameternamen und einen neuen Projektnamen |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-18 |
| Betroffene Artefakte | `docs/ROADMAP.md` (Releaseplan, drei Abschnitte „Geplant", Abschnitt zu 0.56.0), `governance/DECISION_LOG.md` (D-124 bis D-126, `K-50`), `VERSION`, `CHANGELOG.md`, `tests/protocols/2026-09-18-wirkungsnachweise-0.56.0.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind die Reihenfolge der Arbeit, der Name des Auslieferbestands und ein Parameter von `install.py` |
| Art | Festlegung (Ziel-Releases, Reihenfolge, Projektname, Parametername) |
| Dringlichkeit | **Regulär.** Kein Sicherheitsbezug, keine Verhaltensregel berührt. **Dieses Release ändert keinen anweisenden Träger** – es legt fest, was wann gebaut wird |

## 1. Anlass

Die Roadmap führt seit mehreren Releases zwei Abschnitte, die mit demselben Satz enden:

> *„Ein Ziel-Release ist nicht festgelegt."*

Betroffen sind das **Client Pack `openai-codex`** (Projektentscheidung vom 2026-09-12) und
die **Projekt-Overlays als Installationsparameter** (Anregung vom 2026-09-15,
`CR-2026-072` E8). Beide sind sachlich durchdacht – die Voraussetzungen stehen je
Abschnitt –, und beide liegen seit Wochen ohne Platz in einer Reihenfolge.

**Dazu kommt eine dritte, neue Änderung:** Der Name `leitwerk` soll durch einen
griffigeren ersetzt werden. Und mit 0.55.0 ist ein vierter Posten entstanden, der
ebenfalls kein Ziel-Release hat: die **Clientbindung des werkzeugneutralen Kerns**.

> **Warum das ein eigener Vorgang ist und kein Nebensatz in einem anderen:** Eine
> Festlegung, wann etwas gebaut wird, ist eine Entscheidung mit Preis – sie verschiebt
> alles Übrige nach hinten. Und die Umbenennung ist die weitreichendste Einzelentscheidung
> seit der Wahl des ersten Client Packs: Sie trifft jeden Pfad, jedes übernehmende Projekt
> und den Namen des Repositoriums.

## 2. Der Stand, von dem aus geplant wird

Nach 0.55.0 (Prüfung 46, gerechnet beim Validatorlauf):

| Kriterium (D-11) | Stand | Was übrig ist |
|---|---|---|
| 1 – kein unbearbeiteter `VERIFY`-Marker | **23** | Vier sitzungsgebundene Marker von `devin-desktop` (S3, B3, B10, A1), `X2` dauerhaft unbeobachtbar (`K-20`), dazu die Fundstellen der übrigen Träger |
| 2 – Testkatalog ohne `offen` | **105** (22 + 83) | **Der Posten mit Abstand.** 22 Zellen im zentralen Katalog, 83 in dreizehn Testblättern |
| 3 – Modulstatus über `entwurf` | **0 ✅** | erfüllt seit 0.53.0 |
| 4 – keine Records `entschieden (Vorschlag)` | **0 ✅** | erfüllt seit 0.49.0 |
| 5 – Übernahme in ein zweites Projekt | **erfüllt** | zählt Prüfung 46 nicht (ausdrückliche Enthaltung) |

**Die 22 offenen Katalogzellen nach Klasse**, ausgezählt und nicht geschätzt:
`NE` 4, `PI` 3, `SC` 3, `FI` 3, `KO` 2, `PO` 2, `DS` 2, `AK` 2, `RE` 1 – Summe **22**.
Die Klasse `ZA` ist mit 0.55.0 vollständig abgenommen.

> ⚠️ **Kriterium 1 hat einen Bodensatz, und er ist kein Versehen.** `CR-2026-070` E3 hat
> entschieden, dass auch die Fundstelle zählt, die den Marker nur **nennt** – Registerzeile,
> Glossarzeile, Arbeitsanweisung. *„Kriterium 1 kann damit nicht auf null gehen, solange der
> Marker sein eigenes Register und seine Glossarzeile hat – und das ist richtig so."*
> **Der letzte Schritt vor 1.0.0 ist deshalb nicht „den letzten Marker auflösen", sondern
> „den Marker samt Register und Glossarzeile abschaffen".** `PLACEHOLDER_REGISTRY.md`
> schreibt beiden Formen in der Spalte *Ersetzung/Frist* ausdrücklich **„vor Version 1.0.0"**
> vor; der Zähler verlangt am Ende genau das. **Das gehört in den Plan, sonst läuft das
> letzte Release in eine Zahl, die sich nicht mehr senken lässt.**

## 3. Vorgeschlagene Änderung

1. `docs/ROADMAP.md` bekommt einen **Releaseplan bis 1.0.0 und darüber hinaus** – als
   Reihenfolge, ausdrücklich ohne Termine und ohne Aufwände (Vorbemerkung der Roadmap).
2. Die drei Abschnitte „Geplant" bekommen ihr Ziel-Release; ein vierter kommt hinzu
   (Umbenennung).
3. **D-124 bis D-126** und **`K-50`** im Decision Log.
4. `VERSION` auf `0.56.0`, Änderungsverzeichnis, Wirkungsnachweis-Protokoll.

**Dieser Vorgang ändert keinen anweisenden Träger, keine Prüfung und keine Sonde.**

## 4. Vorlage zur Entscheidung

### E1 – Bekommen die noch nicht eingeplanten Änderungen ein Ziel-Release?

**Auflösung: ja, alle vier.** Die Clientbindung des Kerns rückt vor 1.0.0, die drei
übrigen unmittelbar danach.

Die beiden alten Posten liegen seit dem 2026-09-12 beziehungsweise 2026-09-15 ohne Platz.
**Ein Posten ohne Zahl bleibt in diesem Projekt erfahrungsgemäß lange liegen** – D-117 hat
denselben Preis schon einmal benannt, und Paket 6 steht seit neunzehn Releases ohne
Fortschritt.

**Preis, benannt:** Eine Reihenfolge ist eine Zusage, und dieses Projekt kennt den
Befundtyp *„eine Zusage, die mehr verspricht, als sie leistet"* besser als jeden anderen.
**Die Gegenmaßnahme steht im Plan selbst:** Die Nummern sind eine **Reihenfolge**, keine
Termine, und der Plan sagt ausdrücklich, dass Folge-Releases aus Testfunden dazwischen
fallen. **Erfahrungswert dieses Projekts: sie fallen dazwischen** – die
Aufgabenbeschreibung war zehnmal in Folge zu klein, und 0.54.1 ist ein Nachtrag zu einem
Release, das fertig aussah.

### E2 – In welcher Reihenfolge stehen die drei Änderungen nach 1.0.0?

**Auflösung: Umbenennung zuerst, dann `openai-codex`, dann das Overlay.**

**Nicht in der Reihenfolge, in der sie aufgeschrieben wurden** – und der Grund ist
mechanisch: Ein neues Client Pack und ein neues Overlay-Muster sind **neue Träger mit
Pfaden**. Wer sie vor der Umbenennung baut, baut sie unter einem Namen, der zwei Releases
später wechselt, und benennt sie zweimal um.

**Preis, benannt:** Die beiden inhaltlichen Erweiterungen warten auf einen Vorgang, der
sachlich nichts beiträgt. **Das Gegengewicht ist der doppelte Umbau**, den die andere
Reihenfolge erzwingt.

**Verworfen:** *Die Reihenfolge der Nennung übernehmen* (`openai-codex`, Overlay,
Umbenennung). Sie kostet zwei zusätzliche Umbenennungsläufe über neue Träger.

### E3 – Wie heißt das Projekt künftig?

**Auflösung: `Koolie`.** Der australische Hütehund, der auf Deutsch **German Coolie**
heißt, weil deutsche Auswanderer ihn mitbrachten.

**Die Metapher trägt den Gegenstand:** Ein Hütehund hält die Herde in den Grenzen, **ohne
ihr zu schaden**, und arbeitet auf Zuruf. Genau das tut dieses Framework – es macht den
KI-Client nicht besser, es hält ihn im Gatter und zwingt ihn zum Anhalten. Sechs Zeichen,
in deutscher und englischer Prosa sprechbar, keine bekannte Softwarekollision.

**Preis, benannt:** Jeder Pfad des Auslieferbestands ändert sich (`leitwerk-core/` →
`koolie-core/`), ebenso der Platzhalter `<CORE_DIR>`, der Name des Repositoriums und
die Verzeichnisse beider übernehmender Projekte. **Und der Bestand an Chronik bleibt beim
alten Namen** – Protokolle, Änderungsanträge und das Änderungsverzeichnis beschreiben
einen vergangenen Zustand und werden nach D-02 nicht umgeschrieben. Das Repositorium führt
danach dauerhaft zwei Namen: einen für die Sache und einen für ihre Geschichte.

**Verworfen, je mit Grund:**

- **`Kelpie`** – klanglich der beste Kandidat und dieselbe Hütehund-Metapher, **aber
  doppeldeutig, und die zweite Lesart ist das Gegenteil der Zusage:** Der Kelpie der
  schottischen Sage ist ein Wassergeist in Pferdegestalt, der vertrauenswürdig aussieht,
  zum Aufsitzen einlädt und den Reiter ertränkt. **Das ist die Archetypfigur des
  trügerischen Versprechens** – und der wiederkehrende Befundtyp dieses Projekts heißt
  wörtlich *„eine Zusage, die mehr verspricht, als sie leistet"*. Im Alltag folgenlos; in
  genau dem Gespräch mit `<SECURITY_CONTACT>` und Datenschutz, für das dieses Framework
  gebaut ist, eine offene Flanke.
- **`Ibex`** – vier Zeichen, trittsicher im Steilhang, keine Kollision. Verworfen wegen
  der Endung: `-ex` liest sich als Konsummarke.
- **`Meerkat`**, **`Hornbill`**, **`Markhor`** – je eine tragende Metapher (Schildwache,
  vermauerte Höhle mit einem Durchlass, sicherer Schritt), aber länger und teils
  vorbelegt.

### E4 – Wird die Umbenennung vor 1.0.0 vorgezogen?

**Auflösung: nein. Sie steht als `2.0.0` unmittelbar nach 1.0.0 – so festgelegt.**

**Der Preis dieser Festlegung ist hoch und wird hier benannt, nicht verschwiegen:** Eine
Umbenennung nach 1.0.0 ist nach SemVer eine **brechende Änderung** und erzwingt ein
Major-Release samt Migration für **jedes** übernehmende Projekt. Vor 1.0.0 wäre sie
billiger: Es gibt genau zwei übernehmende Projekte, beide im eigenen Haus, und keine
Zusage über Stabilität ist gegeben. **Wer das Gegenteil entscheiden will, entscheidet es
mit diesem Absatz.**

**Die Gegenseite, und sie trägt die Festlegung:** 1.0.0 ist in diesem Projekt kein
Formalakt, sondern die Bedingung aus D-11 – fünf Kriterien, von denen zwei erfüllt sind
und einer 105 Einzelnachweise verlangt. **Ein Umbenennungslauf über jeden Pfad des
Bestands ist genau die Art Arbeit, die dabei nichts misst und alles anfasst**, und er
würde jede offene Messung, jede Fundstelle in einem Testblatt und jeden laufenden Zweig
berühren. Er gehört hinter die Zahl, nicht vor sie.

#### Nachtrag vom 2026-09-18 (`0.56.1`): Der Preis oben ist überzeichnet, und die Widerlegung steht zwei Sätze daneben

> 🔴 **Der Absatz „Der Preis dieser Festlegung ist hoch" sagt *„Migration für **jedes**
> übernehmende Projekt"* – und benennt im nächsten Satz selbst, dass es **zwei** sind,
> beide im eigenen Haus. **Das ist der wiederkehrende Befundtyp dieses Projekts, diesmal in
> einem Absatz über die eigene Planung:** eine Aussage, deren Widerlegung im eigenen
> Dokument steht.

**Aufgefallen ist es nicht beim Schreiben, sondern beim Einwand des `<FRAMEWORK_OWNER>`:**
*Es gibt noch keinen produktiven Einsatz.* **Gegengeprüft am Bestand, und der Befund ist
größer als der Einwand:**

| Beleg | Fundstelle | Was er sagt |
|---|---|---|
| **`AP13 – Übernahme in weitere Projekte` hängt von `AP12` ab** | `docs/ROADMAP.md`, Arbeitspakete: *Abhängigkeiten: AP12*; *Eingaben: Release 1.0.0* | **Die ersten Übernahmen außerhalb des Hauses kommen konstruktionsbedingt erst NACH 1.0.0** |
| `AP9 – Pilot` ist nicht gefahren | dieselbe Ablage, *Realbetrieb in der Pilotgruppe*; offene Entscheidungen `<PILOT_DURATION>`, `<TBD: Zielwerte>` | Kein Realbetrieb, also kein produktiver Einsatz |
| Kriterium 5 von D-11 | Standzeile der Roadmap | *„erfüllt … organisatorisch bleibt es offen, weil es keinen Organisationsbezug hat"* |

> ➡️ **Damit trägt die Festlegung auf einem anderen Grund, und der Grund gehört
> hingeschrieben** (*„Eine Bestätigung ist nicht die Behauptung, dass sich nichts geändert
> hat"*): Eine Umbenennung als `2.0.0`, unmittelbar nach 1.0.0 und **vor** dem Beginn von
> `AP13`, trifft **genau dieselben zwei Projekte** wie eine Umbenennung davor. **Der
> Unterschied ist die Versionsnummer, nicht die Arbeit.**

**Was als Preis übrig bleibt, vollständig:**

1. **Kosmetisch:** `1.0.0` trägt einen Namen, der ein Release später wechselt.
2. **Und eine echte Bedingung, die vorher niemand gesehen hat:** **`2.0.0` MUSS vor der
   ersten Übernahme nach `AP13` liegen.** Läuft `AP13` zuerst an, kehrt der ursprüngliche
   Preis zurück – dann ist *„Migration für jedes übernehmende Projekt"* keine Übertreibung
   mehr, sondern zutreffend. **Diese Bedingung steht ab 0.56.1 in der Zeile `2.0.0` des
   Releaseplans.**

**Die Auflösung von E4 bleibt unverändert** – sie ist jetzt besser begründet als durch
ihre eigene Vorlage. **Der falsche Absatz bleibt stehen**; ein Antrag, der seine
Fehleinschätzung löscht, verliert den Lernwert (dieselbe Entscheidung wie bei 0.54.1 und
bei 0.55.0).

### E5 – Wie heißt der Installationsparameter für das mitgelieferte Overlay?

**Auflösung: `--overlay <name>`, erster und vorerst einziger Wert `general`.**

```
python koolie-core/install.py --client claude-code --overlay general
```

**Eine Achse mit Werteliste statt eines Schalters je Overlay.** Ein zweites Muster
(`--overlay java-service`) kommt später ohne Änderung an der Befehlszeile hinzu, und
`--overlay` ohne Wert kann aufzählen, was es gibt. **Ohne den Parameter bleibt es beim
leeren Overlay wie bisher** (`CR-2026-072` E8).

**Preis, benannt:** Ein Wort mehr als ein bloßer Schalter.

**Verworfen:** *`--general`* – jedes weitere Overlay bräuchte ein eigenes Flag, und ein
„was gibt es"-Kommando ist damit nicht ausdrückbar. *`--preset general`* – sachlich
gleichwertig, führt aber einen zweiten Begriff neben „Overlay" ins Vokabular ein, der
gepflegt werden müsste. *`--profile general`* – **kollidiert** mit dem Entwicklungsprofil
(`FRAMEWORK_DEV_PROFILE.md`) und den Agentenprofilen; eine Doppelbelegung desselben Wortes
ist in diesem Repositorium bereits zweimal als Befund aufgetreten.

### E6 – Bekommt der Weg bis 1.0.0 einen Releaseplan in der Roadmap?

**Auflösung: ja – als Reihenfolge, ausdrücklich ohne Termine und ohne Aufwände.**

Die Vorbemerkung der Roadmap sagt seit der Erstfassung: *„Es werden keine Termine oder
Aufwände vorgegeben."* Der Plan hält sich daran – er nummeriert, er datiert nicht.

**Preis, benannt:** Ein geschriebener Plan veraltet, und dieses Repositorium hat mehrfach
gemessen, dass eine gepflegte Zahl falsch wird. **Die Gegenmaßnahme ist, dass der Plan
keine Zahl führt, die eine Prüfung nachrechnen könnte** – die vier Zahlen von D-11 stehen
weiterhin ausschließlich in der Standzeile, die Prüfung 46 hält.

### E7 – Bekommt die Clientbindung des Kerns ihr Ziel-Release?

**Auflösung: ja, `0.57.0` – das nächste Sachrelease.**

Der Befund ist gemessen, die Aufzählung liegt fertig vor (17 Fundstellen in 14 anweisenden
Trägern), und er kostet **kein Sitzungskontingent**. Er gehört vor die nächste Messreihe,
weil die Eingabe von `FW-ZA-02` selbst betroffen ist.

**Preis, benannt:** Ein Release ohne Bewegung an einer Zahl von D-11.

## 5. Prüffragen

- [x] **Richtige Ebene?** — Ja. Gegenstand sind die Reihenfolge der Framework-Arbeit, der
  Name des Auslieferbestands und ein Parameter von `install.py`. Kein Projektwert.
- [x] **Verschärfungsprinzip eingehalten?** — Ja, trivial: keine Verhaltensregel wird
  berührt, V1–V12 und K3 bleiben unverändert.
- [x] **Widerspruchsfreiheit geprüft?** — Gelesen: `docs/ROADMAP.md` (Vorbemerkung, „Der
  Weg nach 1.0.0", beide Abschnitte „Geplant", `AP11`, `AP12`), `CR-2026-070` E3,
  `CR-2026-072` E8, D-02, D-11, D-57, D-76, `clients/README.md` Abschnitt 5,
  `docs/PLACEHOLDER_REGISTRY.md`. **Ein Widerspruch gefunden und in Abschnitt 2 benannt:**
  Kriterium 1 kann nicht auf null gehen, solange der Marker sein eigenes Register hat –
  das ist Absicht und verlangt einen letzten Schritt, den der Plan jetzt führt.
- [x] **Laufzeitfassungen betroffen?** — **Nein.** Angefasst werden `docs/`, `governance/`,
  `VERSION` und `CHANGELOG.md`. Gemessen mit `install.py --update --dry-run`.
- [x] **Belegstatus korrekt?** — Keine neue Aussage über einen Client. Die Zahlen des
  Abschnitts 2 stammen aus Prüfung 46 und einer unabhängigen Auszählung.
- [x] **Test- und Validierungsbedarf?** — Keine neue Prüfung, keine neue Sonde.
- [x] **Auswirkungen auf Overlays?** — Keine heute. **Für `2.0.0` erheblich** – das ist
  `K-50`.
- [x] **Zahlen nachgezählt?** — Ja. Die 22 offenen Katalogzellen sind nach Klasse
  ausgezählt (`NE` 4, `PI` 3, `SC` 3, `FI` 3, `KO` 2, `PO` 2, `DS` 2, `AK` 2, `RE` 1 = 22)
  und gegen die Gesamtzahl von Prüfung 46 gehalten.
- [x] **Dokumentation:** CHANGELOG, Decision Log, Roadmap, Protokoll.

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** (E1 bis E7) |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Vier Posten ohne Ziel-Release sind vier Posten, die liegen bleiben. Der Plan ordnet sie, ohne Termine zu behaupten, und benennt den Schritt, den Kriterium 1 zum Schluss braucht. Der neue Projektname ist entschieden, die verworfenen Kandidaten sind mit Grund festgehalten |
| Ziel-Release | **0.56.0** |
| Decision-Log-Eintrag | **D-124** (Ziel-Releases und Reihenfolge), **D-125** (der Projektname `Koolie`), **D-126** (`--overlay <name>`); **`K-50`** neu |

## 7. Umsetzung

- [x] `docs/ROADMAP.md`: Abschnitt **„Der Releaseplan bis 1.0.0 und darüber hinaus"** neu;
      die Abschnitte „Geplant: Projekt-Overlays als Installationsparameter" und „Geplant:
      Client Pack `openai-codex`" bekommen ihr Ziel-Release; **„Geplant: Die Umbenennung
      auf `Koolie`"** neu; Abschnitte zu 0.56.0
- [x] `governance/DECISION_LOG.md`: D-124 bis D-126, `K-50`
- [x] `VERSION` auf `0.56.0`; CHANGELOG-Eintrag mit Migrationshinweis
- [x] Validator ohne Fehler; Sondenlauf in beiden Kodierungsumgebungen
- [x] **Dokumentation:** `tests/protocols/2026-09-18-wirkungsnachweise-0.56.0.md`
- [ ] **Zur Entscheidung offen, mit einem späteren Vorgang:** `K-50` (Migrationspfad der
      Umbenennung)

## 8. Abnahme

- `validate-framework.py --root .`: 0 Fehler, 0 Warnungen
- `probe-pruefungen.py .` in beiden Kodierungsumgebungen: 254 Ergebniszeilen bestanden,
  unverändert gegenüber 0.55.0
- Prüfung 46 rechnet Kriterium 2 = 105 – **unverändert, und das ist hier das erwartete
  Ergebnis**
- Protokoll: `tests/protocols/2026-09-18-wirkungsnachweise-0.56.0.md`
