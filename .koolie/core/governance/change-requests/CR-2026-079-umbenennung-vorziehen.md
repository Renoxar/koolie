# Änderungsantrag `CR-2026-079`

| Feld | Inhalt |
|---|---|
| Titel | Die Umbenennung wird vorgezogen – und die Vorlage von `CR-2026-078` E4 stellte eine Ja/Nein-Frage, wo eine Positionsfrage stand |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-18 |
| Betroffene Artefakte | `docs/ROADMAP.md` (Releaseplan, drei Abschnitte „Geplant", Warnung, Abschnitt zu 0.56.0), `governance/DECISION_LOG.md` (D-127 neu; D-124, D-125, D-126 mit Nachtrag; `K-51` neu), `VERSION`, `CHANGELOG.md`, `tests/protocols/2026-09-18-wirkungsnachweise-0.56.2.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind der Zeitpunkt der Umbenennung und die Abnahmeauflage für Sondenläufe |
| Art | Änderung (Ziel-Release der Umbenennung und der beiden Folgereleases), Klärungspunkt (`K-51`) |
| Dringlichkeit | **Regulär.** Kein anweisender Träger wird geändert; der Gegenstand ist die Reihenfolge der eigenen Arbeit |

## 1. Anlass

Zwei Hinweise des `<FRAMEWORK_OWNER>` nach `0.56.1`:

1. *„Lass uns das als letzten Schritt vor der 1.0.0 einplanen."* – zum Zeitpunkt der
   Umbenennung.
2. *„Führst du gerade alle Tests des Leitwerks durch, bloß weil wir diesen kleinen
   Nachtrag aufgenommen haben? … können wir uns zukünftig bei solchen Änderungen die Tests
   sparen?"* – zur Abnahmeauflage aus D-49.

**Der erste Hinweis deckt einen Fehler in der Vorlage auf, der zweite wird gemessen
beantwortet.**

## 2. Erster Befund: Die Vorlage stellte eine Ja/Nein-Frage, wo eine Positionsfrage stand

`CR-2026-078` E4 lautete *„Wird die Umbenennung vor 1.0.0 vorgezogen?"* und stellte zwei
Antworten gegenüber:

| Stelle | Preis, wie er in E4 stand |
|---|---|
| **vor 1.0.0** | *„Ein Umbenennungslauf über jeden Pfad ist genau die Art Arbeit, die dabei nichts misst und alles anfasst"* – er berührte jede offene Messung |
| **nach 1.0.0** | brechende Änderung, Major-Release, Migration; mit `0.56.1` zusätzlich eine Bedingung, die keine Prüfung hält |

> 🔴 **Beide Antworten waren schlechter als eine dritte, die in keiner Fassung des Antrags
> stand.** „Vor 1.0.0" und „nach 1.0.0" wurden behandelt, **als wären es zwei Punkte – es
> ist ein Intervall.** Die tragfähige Stelle liegt darin: **nach der letzten Messung, vor
> `AP11`, vor der Freigabe.**

**Das ist der wiederkehrende Befundtyp in einer Bauform, die dieses Repositorium bisher
nicht geführt hat:** nicht eine Zusage, die mehr verspricht als sie leistet, sondern **eine
Vorlage, deren Antwortmenge kleiner war als der Gegenstand.** Verwandt mit der Lehre
*„Die Aufgabenbeschreibung war zehnmal in Folge zu klein"*, und hier trifft sie die
Entscheidungsvorlage selbst.

### 2.1 Was an der dritten Stelle wegfällt

| Preis aus 0.56.0 / 0.56.1 | Bei `~0.68.0` |
|---|---|
| brechende Änderung, Major-Release `2.0.0` | **entfällt** – vor 1.0.0 gibt es keine Stabilitätszusage |
| Migration für übernehmende Projekte | **entfällt als Pflicht** – es sind zwei, beide im eigenen Haus, und sie werden ohnehin je Release gehoben |
| kosmetisch: 1.0.0 trägt einen Namen, der wechselt | **entfällt** – die erste freigegebene Fassung heißt **`Koolie 1.0.0`** |
| Bedingung „vor der ersten Übernahme nach `AP13`" (0.56.1) | **entfällt ersatzlos** – `AP13` hängt an `AP12` und beginnt konstruktionsbedingt erst nach 1.0.0 |
| Gegeneinwand: *„nichts misst und alles anfasst"* | **verliert seinen Gegenstand** – an dieser Stelle ist nichts mehr zu messen, Kriterium 1 und 2 stehen auf null. **Der Einwand war gegen „vor die Zahl" gerichtet und trifft „nach der Zahl" nicht** |

### 2.2 Und eine Stelle bleibt, die mechanisch bestimmt ist: **vor `AP11`**

`AP11` setzt das Hauptdokument gegen den dann geltenden Stand und **baut die
Word-Fassung**. Läge die Umbenennung danach, trügen beide den alten Namen und müssten
zweimal gebaut werden. **Das ist dieselbe Begründung, mit der D-124 die Umbenennung vor
`openai-codex` und das Overlay gesetzt hat** – ein Träger mit Pfaden wird nicht zweimal
umbenannt.

> Das Hauptdokument ist ohnehin über vierzig Releases zurück. Es zweimal nachzuziehen wäre
> die teuerste vermeidbare Doppelarbeit im ganzen Plan.

## 3. Zweiter Befund: Braucht ein reines Prosarelease den Sondenlauf? – gemessen

**Die Frage ist berechtigt und die Antwort lautet für `0.56.1`: ja, und er war nicht
leer.**

`probe-pruefungen.py` führt Pfadliterale auf **genau die zwei Dateien**, die `0.56.1`
geändert hat:

| Zeile | Datei | Anker |
|---|---|---|
| 671, 3424 | `docs/ROADMAP.md` | Standzeile von Prüfung 46; B03 |
| 1996, 3520, 3542 | `governance/DECISION_LOG.md` | `\| D-40 \|`, `\| D-10 \|` |

**Diese Anker tragen Präparationswächter, die abbrechen, wenn der Suchtext nicht genau
einmal steht.** Ein sorgloser Prosaeingriff dort **lässt den Validator grün und den
Sondenlauf fallen** – das ist die Bauform *„die Sonde auf den verlorenen Anker"*.

**Wo sich wirklich sparen ließe, ist ausrechenbar:** Vier Gattungen kommen in den
Pfadliteralen des Sondenskripts **nicht** vor – `CHANGELOG.md`, `VERSION`,
`governance/change-requests/**`, `tests/protocols/**`. Ein Release, dessen Diff nur daraus
besteht, bräuchte den Lauf nicht.

> **Ausgezählt über alle Release-Commits: 1 von 57** (`0.53.1`). Alle übrigen haben
> `ROADMAP.md` oder `DECISION_LOG.md` angefasst.

## 4. Vorgeschlagene Änderung

1. **Die Umbenennung wandert von `2.0.0` auf `~0.68.0`** – nach der letzten Messung, **vor
   `AP11`**, vor der Freigabe. `AP11` wird `~0.69.0`.
2. **`openai-codex` wird `1.1.0`, das Projekt-Overlay `1.2.0`.** Die Reihenfolge der drei
   Änderungen aus D-124 bleibt unverändert; nur die Linie 1.0.0 verschiebt sich.
3. **D-127** neu; D-124, D-125 und D-126 tragen den Nachtrag in ihrer Statuszelle.
4. **`K-51`** neu – die Sondenlauf-Auflage, angelegt und **nicht** entschieden.
5. Roadmap, `VERSION` auf `0.56.2`, Änderungsverzeichnis, Protokoll.

**Kein anweisender Träger wird geändert, keine Prüfung, keine Sonde.**

## 5. Vorlage zur Entscheidung

### E1 – Wird die Umbenennung vorgezogen?

**Auflösung: ja, auf `~0.68.0` – den letzten inhaltlichen Schritt vor 1.0.0.**

Abschnitt 2 und die Tabelle in 2.1: **alle vier benannten Preise fallen weg, und der
Gegeneinwand verliert seinen Gegenstand.** Es gibt an dieser Stelle keinen Posten auf der
Gegenseite, der noch trüge.

**Preis, benannt, und er ist neu:** Die Umbenennung liegt im **Freigabefenster** –
zwischen der letzten Messung und dem Gate. Wer dort einen Pfad übersieht, tut es
unmittelbar vor der Freigabe. **Das Gegengewicht ist, dass ihr zwei vollständige Durchgänge
folgen:** `AP11` und der Freigabelauf nach `checklists/11-framework-release.md`. **Das ist
mehr Nachkontrolle, als die Umbenennung an jeder anderen Stelle des Plans bekäme.**

**Verworfen:** *Bei `2.0.0` bleiben* – dieselbe Arbeit kostet dann ein Major-Release, eine
Migrationspflicht und eine Bedingung, die keine Prüfung hält. *Vor die Messungen ziehen* –
dort trifft der ursprüngliche Gegeneinwand zu: 105 Ergebniszellen und 23 Marker sind offen,
und jede Fundstelle in einem Testblatt wäre berührt.

### E2 – Vor oder nach `AP11`?

**Auflösung: vor `AP11`.** Begründung in 2.2 – `AP11` erzeugt Hauptdokument und
Word-Fassung; danach müssten beide zweimal gebaut werden.

**Preis, benannt:** `AP11` ist damit der **letzte** Vorgang vor der Freigabe und trägt die
Nachkontrolle der Umbenennung mit. Das ist eine Zusatzlast für ein Paket, das ohnehin die
größte Aufräumarbeit des Plans enthält.

**Verworfen:** *Nach `AP11`* – dann trägt das gerade erst nachgezogene Hauptdokument den
alten Namen, und die Word-Fassung ist zweimal zu bauen. *Umbenennung und `AP11` in einem
Release* – ein Vorgang, der Pfade umschreibt, und einer, der Inhalte gegen den Stand setzt,
gehören getrennt; sonst ist im Diff nicht mehr zu erkennen, was Umbenennung war und was
Inhalt.

### E3 – Was wird aus `2.0.0` und der Bedingung aus `0.56.1`?

**Auflösung: beides entfällt.** Es gibt kein `2.0.0`; `openai-codex` wird `1.1.0`, das
Overlay `1.2.0`. Die Bedingung *„`2.0.0` MUSS vor der ersten Übernahme nach `AP13`
liegen"* entfällt **ersatzlos**, weil `AP13` an `AP12` hängt und die Umbenennung jetzt
davor liegt.

**Preis, benannt:** Der Nachtrag von `0.56.1` ist damit **nach einem halben Tag überholt**.
Er bleibt wörtlich stehen und trägt den Verweis – dieselbe Entscheidung wie dort selbst.
**Drei Fassungen desselben Zeitpunkts in drei Releases sind kein schöner Verlauf, aber ein
ehrlicher**, und jede Fassung trägt ihre Begründung.

**Verworfen:** *Die alten Fassungen löschen und nur die letzte stehen lassen.* Dann steht
in der Chronik eine Festlegung, die nie so entstanden ist – und die Lehre aus 2 wäre
nirgends aufgeschrieben.

### E4 – Wird die Sondenlauf-Auflage aus D-49 gelockert?

**Auflösung: nein – `K-51`, angelegt und nicht entschieden.**

Abschnitt 3 misst den Gegenstand: Für `0.56.1` war der Lauf **nicht leer**, weil das
Sondenskript in genau die beiden geänderten Dateien hineinpatcht. Und die saubere Ausnahme
wäre **ausrechenbar, nicht gepflegt**: ein Skript zieht die Pfadmenge aus
`probe-pruefungen.py` und hält sie gegen `git diff --name-only`, **fail-closed** bei jedem
Pfad, den es nicht auflösen kann.

**Preis, benannt, und er trägt die Vertagung:** Diese Form braucht nach D-23 selbst
Skript, **Sonde und Gegenprobe** – ein eigenes Release – um bei einer gemessenen
Trefferquote von **1 zu 57** rund fünf Minuten Wanduhr **ohne Kontingent** zu sparen. Der
Lauf kostet keine Modellzeit und läuft im Hintergrund.

**Verworfen:** *Eine Ausnahme nach Ermessen* („kleine Änderung, Lauf entfällt"). **Das ist
genau die Bauform, die dieses Repositorium sonst als Befund führt** – eine Grenze, die
niemand nachrechnet. Und sie träfe zuerst die Releases, die wie harmlose Prosa aussehen
und an einem Präparationswächter hängen. *Nur einen Lauf statt zwei* – D-49 verlangt beide
Kodierungsumgebungen, weil die Konsolenkodierung schon einmal eine Null erzeugt hat, die
wie ein Messwert aussah; die Auflage hat einen Anlass.

## 6. Prüffragen

- [x] **Richtige Ebene?** — Ja. Reihenfolge der Framework-Arbeit und eine Abnahmeauflage.
- [x] **Verschärfungsprinzip eingehalten?** — Ja. **`K-51` wäre eine Lockerung und wird
  ausdrücklich nicht entschieden**; die Auflage aus D-49 gilt unverändert weiter.
- [x] **Widerspruchsfreiheit geprüft?** — Gelesen: `docs/ROADMAP.md` (Releaseplan, `AP11`,
  `AP12`, `AP13`, drei Abschnitte „Geplant", Abschnitt zu 0.56.0), `CR-2026-078` E2 bis E4
  samt Nachtrag, D-49, D-23, D-124 bis D-126, `K-50`,
  `checklists/11-framework-release.md`. **Ein Widerspruch gefunden und aufgelöst:** Die
  Zeile `2.0.0` und der Abschnitt „Geplant: Die Umbenennung" trugen den alten Zeitpunkt;
  beide sind nachgezogen, die historischen Abschnitte tragen Verweise statt neuer Texte.
- [x] **Laufzeitfassungen betroffen?** — **Nein.** Angefasst sind `docs/`, `governance/`,
  `VERSION`, `CHANGELOG.md`.
- [x] **Belegstatus korrekt?** — Die Zahlen in Abschnitt 3 sind ausgezählt: fünf
  Fundstellen im Sondenskript mit Zeilennummern, 1 von 57 Release-Commits.
- [x] **Test- und Validierungsbedarf?** — Keine neue Prüfung, keine neue Sonde. Validator
  0/0; Sondenlauf in beiden Kodierungsumgebungen – **und diesmal aus einem benannten Grund
  und nicht nur aus Auflage**, weil `ROADMAP.md` und `DECISION_LOG.md` erneut angefasst
  sind.
- [x] **Auswirkungen auf Overlays?** — Keine heute. **`K-50` wird wichtiger:** Beide
  übernehmenden Projekte sind zwischen `~0.68.0` und 1.0.0 zu heben und umzubenennen.
- [x] **Zahlen nachgezählt?** — Ja. `1 von 57` ist über alle Release-Commits ausgezählt,
  nicht geschätzt; die fünf Fundstellen im Sondenskript stehen mit Zeilennummer.
- [x] **Dokumentation:** CHANGELOG, Decision Log, Roadmap, Protokoll.

## 7. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** (E1 bis E4) |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Die dritte Stelle ist beiden vorgelegten überlegen, und zwar ohne Gegenposten: Alle vier benannten Preise fallen weg, und der eigene Gegeneinwand verliert seinen Gegenstand. Die Lage vor `AP11` ist mechanisch bestimmt. Die Sondenlauf-Auflage bleibt, weil die Messung zeigt, dass sie greift |
| Ziel-Release | **0.56.2** |
| Decision-Log-Eintrag | **D-127**; D-124, D-125 und D-126 mit Nachtrag; **`K-51`** neu |

## 8. Umsetzung

- [x] `docs/ROADMAP.md`: Releaseplan – Umbenennung `~0.68.0`, `AP11` `~0.69.0`,
      `openai-codex` `1.1.0`, Overlay `1.2.0`; Warnung zum Preis ersetzt; drei Abschnitte
      „Geplant" mit neuen Ziel-Releases; **der Abschnitt zu 0.56.0 behält seinen Wortlaut
      und trägt zwei Verweise**
- [x] `governance/DECISION_LOG.md`: D-127 neu; D-124, D-125, D-126 mit Nachtrag; `K-51` neu
- [x] `VERSION` auf `0.56.2`; CHANGELOG-Eintrag
- [x] Validator ohne Fehler; Sondenlauf in beiden Kodierungsumgebungen
- [x] **Dokumentation:** `tests/protocols/2026-09-18-wirkungsnachweise-0.56.2.md`
- [ ] **Zur Entscheidung offen:** `K-50` (Migrationspfad der Umbenennung), `K-51`
      (Sondenlauf-Auflage)

## 9. Abnahme

- `validate-framework.py --root .`: 0 Fehler, 0 Warnungen
- `probe-pruefungen.py .` in beiden Kodierungsumgebungen: 254 Ergebniszeilen bestanden
- Kriterium 2 unverändert **105**, Kriterium 1 unverändert **23** – ein Plan ist keine
  Abnahme
- Protokoll: `tests/protocols/2026-09-18-wirkungsnachweise-0.56.2.md`
