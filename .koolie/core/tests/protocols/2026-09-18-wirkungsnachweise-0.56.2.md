# Wirkungsnachweise 0.56.2

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-18 |
| Framework-Version | `0.56.2` (Vorstand `0.56.1`, Commit `067da4c`) |
| Antrag | `CR-2026-079`, D-127 neu; D-124, D-125, D-126 mit Nachtrag; `K-51` neu |
| Gegenstand | Die Umbenennung wandert von `2.0.0` auf `~0.68.0` – **vor 1.0.0 und vor `AP11`**. Dazu die gemessene Antwort auf die Frage, ob ein reines Prosarelease den Sondenlauf braucht |
| Prüfmethode | Auszählung am Sondenskript und über alle Release-Commits; Validatorlauf; Sondenlauf in beiden Kodierungsumgebungen (D-49) |
| Ergebnis | **Validator 0 Fehler, 0 Warnungen; 254 Ergebniszeilen bestanden in beiden Kodierungsumgebungen.** Keine Zahl von D-11 bewegt sich |

---

## 1. Der Befund an der eigenen Vorlage

`CR-2026-078` E4 fragte *„Wird die Umbenennung vor 1.0.0 vorgezogen?"* und bot zwei
Antworten an. **Beide waren schlechter als eine dritte, die in keiner Fassung des Antrags
stand.**

> 🔴 **„Vor 1.0.0" und „nach 1.0.0" wurden behandelt, als wären es zwei Punkte – es ist ein
> Intervall.** Die tragfähige Stelle liegt darin: **nach der letzten Messung, vor `AP11`,
> vor der Freigabe.**

**Das ist eine Bauform, die dieses Repositorium bisher nicht geführt hat.** Der
wiederkehrende Befundtyp lautet sonst *„eine Zusage, die mehr verspricht, als sie leistet"*.
Hier ist es **eine Vorlage, deren Antwortmenge kleiner war als ihr Gegenstand** – verwandt
mit *„Die Aufgabenbeschreibung war zehnmal in Folge zu klein"*, aber eine Ebene höher: Sie
trifft nicht die Beschreibung der Arbeit, sondern **die Entscheidungsvorlage**.

**Gefunden hat ihn wieder nicht eine Prüfung, sondern ein Einwand des
`<FRAMEWORK_OWNER>`** – zum zweiten Mal in Folge nach `0.56.1`.

### 1.1 Was an der dritten Stelle wegfällt – gegengeprüft, nicht behauptet

| Preis aus 0.56.0 / 0.56.1 | Prüfung | Ergebnis |
|---|---|---|
| brechende Änderung, Major `2.0.0` | SemVer vor 1.0.0 | **entfällt** – keine Stabilitätszusage vor 1.0.0 |
| Migrationspflicht | Zahl der übernehmenden Projekte | **entfällt als Pflicht** – zwei, beide im eigenen Haus, je Release ohnehin gehoben |
| kosmetisch: 1.0.0 trägt einen wechselnden Namen | Reihenfolge | **entfällt** – die erste freigegebene Fassung heißt `Koolie 1.0.0` |
| Bedingung „vor der ersten Übernahme nach `AP13`" | `AP13`: *Abhängigkeiten: AP12* | **entfällt ersatzlos** – `AP13` beginnt erst nach 1.0.0 |
| Gegeneinwand *„nichts misst und alles anfasst"* | Stand von Kriterium 1 und 2 an dieser Stelle | **verliert seinen Gegenstand** – beide stehen dann auf null |

> ➡️ **Die letzte Zeile ist die wichtigste, und sie ist eine Selbstkorrektur:** Der
> Gegeneinwand war gegen *„vor die Zahl"* gerichtet. **Er trifft *„nach der Zahl"* nicht**
> – und E4 hat ihn trotzdem gegen beide Stellen in Anschlag gebracht, weil es die zweite
> gar nicht unterschied.

### 1.2 Die eine Stelle, die mechanisch bestimmt ist: vor `AP11`

`AP11` setzt das Hauptdokument gegen den dann geltenden Stand und **baut die
Word-Fassung**. Läge die Umbenennung danach, trügen beide den alten Namen und müssten
zweimal gebaut werden. **Dieselbe Begründung, mit der D-124 die Umbenennung vor
`openai-codex` und das Overlay gesetzt hat** – ein Träger mit Pfaden wird nicht zweimal
umbenannt.

---

## 2. Die gemessene Antwort auf die Frage nach dem Sondenlauf

**Frage:** Braucht ein reines Prosarelease wie `0.56.1` den Sondenlauf?
**Antwort: ja, und er war nicht leer.**

| Zeile in `probe-pruefungen.py` | Datei | Anker |
|---|---|---|
| 671 | `leitwerk-core/docs/ROADMAP.md` | `B03_ZIEL` |
| 3424 | `leitwerk-core/docs/ROADMAP.md` | `P46_ROADMAP` – die Standzeile von Prüfung 46 |
| 1996 | `leitwerk-core/governance/DECISION_LOG.md` | `DECISION_LOG_36`, Anker `\| D-40 \|` |
| 3520, 3542 | `leitwerk-core/governance/DECISION_LOG.md` | Anker `\| D-10 \|` samt Statuszelle |

**Diese Anker tragen Präparationswächter**, die abbrechen, wenn der Suchtext nicht **genau
einmal** steht.

> ⚠️ **Konkret für `0.56.1`:** Hätte der Nachtrag versehentlich eine zweite Zeile erzeugt,
> die mit `| D-10 |` beginnt, oder die Standzeile berührt, **wäre der Validator grün
> geblieben und der Sondenlauf gefallen.** Das ist die Bauform *„die Sonde auf den
> verlorenen Anker"*, und sie ist der Grund für die Auflage.

### 2.1 Wo sich wirklich sparen ließe – und wie oft das vorkam

**Vier Gattungen kommen in den Pfadliteralen des Sondenskripts nicht vor:**
`CHANGELOG.md`, `VERSION`, `governance/change-requests/**`, `tests/protocols/**`.

**Ausgezählt über alle Release-Commits (`git log --grep='^Release '`, 57 Stück): genau
einer** hat ausschließlich diese vier berührt – `0.53.1`.

| Zahl | Behauptet | Nachgezählt |
|---|---|---|
| Release-Commits im Bestand | 57 | **57** |
| davon ohne Berührung der Sondenmenge | – | **1** (`0.53.1`) |
| Pfadliterale im Sondenskript insgesamt | – | **53** verschiedene |

> ➡️ **Damit ist die Vertagung von `K-51` gerechnet und nicht gefühlt:** Die saubere
> Ausnahme braucht nach D-23 Skript, **Sonde und Gegenprobe** – ein eigenes Release –, um
> bei **1 zu 57** rund fünf Minuten Wanduhr **ohne Kontingent** zu sparen.
>
> **Und eine Ausnahme nach Ermessen wäre schlimmer als keine:** Sie träfe zuerst die
> Releases, die wie harmlose Prosa aussehen **und an einem Präparationswächter hängen** –
> also genau diesen Fall.

---

## 3. Die Läufe

### 3.1 Validator

| Lauf | Zuschnitt | Ergebnis |
|---|---|---|
| V1 | `--root .` nach Releaseplan und Decision Records | **0 Fehler, 0 Warnungen** |
| V2 | `--root .` nach dem Ersetzen der überholten Warnung und der Verweise im Abschnitt zu 0.56.0 | **0 Fehler, 0 Warnungen** |
| V3 | `--root .` gegen den **fertigen** Baum, Antrag und dieses Protokoll eingeschlossen | **0 Fehler, 0 Warnungen** |

### 3.2 Sondenlauf

| Lauf | Kodierungsumgebung | Ergebniszeilen | Wanduhr |
|---|---|---|---|
| A | ohne `PYTHONIOENCODING` | **254, alle bestanden** | 146,4 s |
| B | mit `PYTHONIOENCODING=utf-8`, gegen die **Endfassung** | **254, alle bestanden** | 142,6 s |

**Und diesmal steht der Grund daneben statt nur der Auflage:** `ROADMAP.md` und
`DECISION_LOG.md` sind erneut angefasst – **beide tragen Anker des Sondenskripts**
(Abschnitt 2).

---

## 4. Was nicht geändert wurde

- **Die Wahl des Namens.** `Koolie` steht unverändert (D-125). Geändert ist der Zeitpunkt.
- **Die Reihenfolge der drei Änderungen** aus D-124: Umbenennung, dann `openai-codex`, dann
  das Overlay. **Nur die Linie 1.0.0 verschiebt sich hinter die Umbenennung.**
- **Die Abnahmeauflage aus D-49.** `K-51` ist angelegt und **nicht** entschieden; eine
  Lockerung wäre gegen das Verschärfungsprinzip vorzulegen, nicht nebenbei zu übernehmen.
- **Die überholten Fassungen.** Der Nachtrag von `0.56.1` und der Absatz von `0.56.0`
  bleiben wörtlich stehen und tragen Verweise. **Drei Fassungen desselben Zeitpunkts in
  drei Releases sind kein schöner Verlauf, aber ein ehrlicher** – und jede trägt ihre
  Begründung.

---

## 5. Gegenzeichnung

| Frage | Antwort |
|---|---|
| Wurde der Einwand übernommen oder geprüft? | **Geprüft.** Die Frage nach dem Sondenlauf ist am Sondenskript und über alle 57 Release-Commits ausgezählt worden; die Antwort fällt **gegen** die naheliegende Vermutung aus – der Lauf war nicht leer |
| Wird eine Entscheidung umgestoßen? | **Ja, eine: der Zeitpunkt** (D-125 → D-127). Der Name bleibt, die Reihenfolge bleibt |
| Ist der neue Preis benannt? | **Ja, und er ist neu:** Die Umbenennung liegt im Freigabefenster. Das Gegengewicht sind zwei vollständige Durchgänge danach – `AP11` und der Freigabelauf |
| Ist eine Auflage gelockert worden? | **Nein.** `K-51` ist angelegt und nicht entschieden; D-49 gilt unverändert |
| Wurde ein überholter Text gelöscht? | **Nein, keiner.** Drei Träger führen alte Fassung und Verweis nebeneinander |
| Bewegt sich eine Zahl von D-11? | **Nein.** Kriterium 2 steht auf **105**, Kriterium 1 auf **23** – ein Plan ist keine Abnahme |

---

*Unterhalb der Trennlinie, nach D-94 nicht Teil des zeilengleichen Vergleichs:*
*Lauf A 146,4 s Wanduhr (1152,4 s Rechenzeit, 8 Bahnen, Faktor 7,9); Lauf B 142,6 s*
*(1123,4 s, Faktor 7,9).*
