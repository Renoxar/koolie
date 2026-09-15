# Änderungsantrag `CR-2026-074`

| Feld | Inhalt |
|---|---|
| Titel | Die restlichen einundvierzig Nicht-Skill-Träger sind abgenommen – bis auf einen, der sich selbst sperrt |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-15 |
| Betroffene Artefakte | `prompts/01-understand-codebase.md` bis `prompts/12-developer-training.md`, `prompts/README.md` (Abschnitt 7), `decision-trees/01-context-allowed.md` bis `06-rule-placement.md`, `governance/EXCEPTION_PROCESS.md`, `FEEDBACK_PROCESS.md`, `FRAMEWORK_DEV_PROFILE.md`, `INCIDENT_HANDLING.md`, `PRIORITY_HIERARCHY.md`, `RACI.md`, `RELEASE_PROCESS.md`, `docs/ADOPTION_GUIDE.md`, `docs/ROADMAP.md` (Statuszelle, Standzeile, Kriterientabelle, AP3, P3-Posten, Abschnitte zu 0.52.0), `docs/RUNTIME_GLOSSARY.md`, `tests/EDGE_CASES.md`, `tests/TEST_CATALOG.md`, `onboarding/COMPLETION_CRITERIA.md`, `GUIDE.md`, `KNOWLEDGE_CHECK.md`, `MENTOR_CHECKLIST.md`, `pilot/METRICS.md`, `pilot/PILOT_CONCEPT.md`, `clients/README.md`, `clients/claude-code/CLIENT_PACK.md`, `framework/role-packs/requirements-engineering/ROLE_PACK.md`, `framework/role-packs/software-development/ROLE_PACK.md`, `governance/DECISION_LOG.md` (D-109 bis D-111, K-39), `VERSION`, `CHANGELOG.md`, `tests/protocols/2026-09-15-gegenpruefung-restliche-nicht-skill-traeger.md`, `tests/protocols/2026-09-15-wirkungsnachweise-0.52.0.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand ist der Lebenszyklusstatus der Module des Frameworks selbst |
| Art | Änderung (Statuswechsel), Klarstellung (drei Auslegungen von Punkt 3 (d) und (a)) |
| Dringlichkeit | **Regulär.** Kein Sicherheitsbezug. Der Gegenstand ist Kriterium 3 von D-11 |

## 1. Anlass

Die Übergabe nennt als Kandidat 1 *„die restlichen 41 Nicht-Skill-Träger heben"* und
vermerkt dazu etwas, das es seit 0.48.0 nicht gab:

> ✅ **Kandidat 1 verlangt diesmal KEINE Vorentscheidung.** `K-36` ist geklärt, die
> Bedingung steht, das Vokabular ist durchgesetzt, und die Bündelform ist an zwei
> Gattungen erprobt. **Das ist die erste Kandidatenzeile seit 0.48.0 ohne vorangestelltes
> Hindernis** – und genau deshalb ist zu erwarten, dass das Hindernis woanders liegt.

**Es liegt woanders, und zwar im Gegenstand.** Vierzig der einundvierzig Träger erfüllen
die Übergangsbedingung. **Der einundvierzigste erfüllt sie nicht und sagt das selbst** –
in dem Absatz unter seinem Steckbrief, unverändert seit acht Releases.

## 2. Der Befund: (d) kennt zwei Fälle, der Bestand hat drei

`01-governance.md` Abschnitt 5 Punkt 3, Zeile `entwurf → pilot`, Bedingung (d):

> Ein offener Ausfüllwert (`<TBD…>`) sperrt den Übergang **nicht**, wenn er einen Wert der
> aufnehmenden Organisation bezeichnet; er sperrt ihn, wenn er eine Aussage des Frameworks
> offenlässt.

Die Unterscheidung ist richtig und trägt. **Sie benennt aber nur zwei der drei Bauformen,
in denen die Marke im Bestand vorkommt.** Die dritte ist die **Nennung**: eine Stelle, die
die Marke zitiert oder einen offenen Punkt benennt, ohne selbst einen Wert offenzulassen.

**Das ist nicht neu, sondern eine Ebene höher dieselbe Feststellung wie D-102:** Dort war
der Befund, dass `<TBD:` drei Bedeutungen trägt und deshalb als **maschinelle** Bedingung
untauglich ist. Für die Abnahme je Träger folgt daraus nicht, dass die Marke unbrauchbar
ist, sondern dass ihre Bedeutung **gelesen** und nicht gezählt wird.

**Gemessen über die einundvierzig Träger:** 35 Fundstellen in 13 Dateien. Davon sperren
**zwei** – beide im selben Träger.

## 3. Der gesperrte Träger, und der Unterschied zu seinem Schwesterpack

`clients/devin-desktop/CLIENT_PACK.md`, Steckbriefzeilen 11 und 12:

```
| Geprüfte Clientversion | <TBD: verbindliche Zielversion; Roadmap AP2> |
| Datum der Prüfung | <TBD: steht aus> |
```

Und zwei Zeilen darunter, seit 0.44.0 unverändert:

> Solange die Zielversion nicht festgelegt und geprüft ist (Roadmap AP2), gilt das Pack als
> **unbelegt**.

**Beide Schlitze bezeichnen keinen Wert der aufnehmenden Organisation**, sondern eine
ausstehende Festlegung des Framework Owners aus `AP2`. (d) greift; der Träger bleibt auf
`entwurf`.

`clients/claude-code/CLIENT_PACK.md` trägt **denselben Satz** über den Belegstand und ist
trotzdem abnehmbar: Seine beiden Steckbriefzellen tragen echte Werte (`2.1.267`,
`2026-09-10`) und verweisen auf ein Protokoll. **Die Trennlinie ist der Schlitz, nicht der
Satz** – für den Belegstand ist der Modulstatus nicht zuständig, das sagt Punkt 4 desselben
Abschnitts wörtlich.

## 4. Der dritte Befund: dieselbe Zeichenfolge, zwei Bedeutungen, zwei Träger

`docs/ROADMAP.md` führt in der Zeile *Offene Entscheidungen* von `AP2`:

```
| Offene Entscheidungen | <TBD: verbindliche Zielversion von Devin Desktop> |
```

**Das ist derselbe offene Punkt, der das Client Pack sperrt** – und hier sperrt er nichts.
In einer Spalte namens *Offene Entscheidungen* ist die Marke die **Nennung** eines offenen
Punktes; ein Dokument, dessen Zweck es ist, offene Punkte zu führen, ist vollständig, wenn
es sie führt. Im Client Pack fehlt dagegen der Wert einer Aussage über ein Produkt.

**Wer nur die Marke zählt, nimmt beide Träger ab oder sperrt beide – und liegt in genau
einem der beiden Fälle falsch.**

## 5. Der vierte Befund: ein Register mit offenen Ergebnissen

`tests/TEST_CATALOG.md` führt **31 Ergebniszellen auf `offen`**. Ist es damit im Sinne von
(a) *inhaltlich unvollständig*?

**Nein.** Sein Gegenstand sind die Testfälle – Kennung, Aufgabe, Vorbedingung, Erwartung,
Gegenerwartung, Prüfmittel –, und die sind ausgefüllt. Die Ergebnisse sind Kriterium 2 von
D-11.

**Die andere Antwort kettete Kriterium 3 an Kriterium 2, und zwar zum dritten Mal in drei
Releases:** D-103 hat die Kettung für die dreizehn Skills gelöst, D-107 für die zwölf
Prompt-Vorlagen. **Dieselbe Bewegung, drei Ablagen** – sie entsteht nicht aus
Nachlässigkeit, sondern weil ein unerfülltes Vorzeichen wie Sorgfalt aussieht (Lehre von
0.49.0).

## 6. Vorgeschlagene Änderung

1. **Vierzig Träger von `entwurf` auf `pilot`**, in neun Bündeln nach Gattung, mit einem
   Protokollabschnitt je Bündel, der jeden Träger namentlich nennt und (a) bis (d) je
   Träger festhält (Punkt 3 (e)).
2. **`clients/devin-desktop/CLIENT_PACK.md` bleibt auf `entwurf`**, mit benannter
   Begründung im selben Protokoll.
3. **Drei Auslegungen als Decision Records festhalten**, damit der nächste Vorgang sie
   nicht neu entscheiden muss.
4. **`prompts/README.md` Abschnitt 7 nachziehen** – der Satz „Alle zwölf Vorlagen liegen im
   Status `entwurf`" wird mit diesem Release falsch.
5. **Standzeile und Roadmap nachziehen** (Prüfung 46 erzwingt es).
6. **Kein Statuswechsel erhöht eine Version** (D-106).

## 7. Vorlage zur Entscheidung

### E1 – Wie wird abgenommen: einzeln, gebündelt oder pauschal?

**Auflösung: neun Bündel nach Gattung, je ein Protokollabschnitt, jeder Träger namentlich.**

Punkt 3 (e) verlangt ein Protokoll, *„das den Träger namentlich nennt und (a) bis (d) je
Träger festhält"*. Eine Bündelung ist zulässig, eine Pauschalierung nicht: Wer bündelt,
muss trotzdem je Träger schreiben.

**Preis, benannt:** Das ist die Arbeit dieses Vorgangs und nicht maschinell. Ein Bündel,
das nur gezählt wird, verletzt die Bedingung.

**Verworfen:** *Ein Abschnitt je Träger* (41 Abschnitte, die neunmal dieselbe
Gattungsaussage wiederholen – die Gattung trägt, was allen gemeinsam ist).

### E2 – Ist `clients/devin-desktop/CLIENT_PACK.md` abnehmbar?

**Auflösung: nein.** Beide Schlitze seines Steckbriefs bezeichnen eine ausstehende
Festlegung des Framework Owners, nicht einen Wert der aufnehmenden Organisation. (d)
greift.

**Preis, benannt:** **Kriterium 3 endet bei 1 statt bei 0.** Der Träger geht über `AP2` –
Zielversion festlegen, Pack gegen sie prüfen, beide Zellen füllen –, nicht über ein Review.

**Verworfen:** *Die beiden Schlitze als Organisationswerte lesen* (die Zielversion eines
Client Packs legt der Framework Owner fest; `AP2` führt sie als eigenes Arbeitspaket).
*Die Schlitze entfernen und die Zellen leeren* – das senkte die Zahl, ohne dass etwas
geprüft worden wäre, und ist die Bewegung, die `CR-2026-070` E6 verworfen hat.

### E3 – Und `clients/claude-code/CLIENT_PACK.md`, das denselben Satz über den Belegstand trägt?

**Auflösung: abnehmbar.** Beide Steckbriefzellen tragen echte Werte. **Die Trennlinie ist
der Ausfüllschlitz, nicht der Satz über den Belegstand** – `01-governance.md` Abschnitt 5
Punkt 4 sagt ausdrücklich, ein Statuswert sei keine Aussage über beobachtetes Verhalten.

**Preis, benannt:** Zwei Träger derselben Gattung mit demselben Satz gehen verschieden aus.
Wer die Begründung nicht liest, hält das für eine Ungleichbehandlung; sie steht deshalb in
Abschnitt 3.2 des Protokolls und hier.

**Verworfen:** *Beide sperren* (hieße, den Modulstatus für den Belegstand haften zu lassen,
den Punkt 4 ausdrücklich von ihm trennt – und alle drei Client-Pack-Dokumente blieben
liegen). *Beide abnehmen* (der Schlitz ist genau der Fall, für den (d) geschrieben wurde).

### E4 – Sperrt ein `<TBD…>` in einer Zelle der Spalte *Offene Entscheidungen*?

**Auflösung: nein.** Es ist die Nennung eines offenen Punktes, nicht der fehlende Wert
einer Aussage. `docs/ROADMAP.md` ist abnehmbar.

**Preis, benannt:** **Die Trennung ist nicht maschinell.** Sie steht je Träger im
Protokoll, mit Zeilennummer, und sie ist dieselbe Trennung, die D-102 für die Zählregel
schon getroffen hat.

**Verworfen:** *Die Spalte umbenennen oder die Marke dort ersetzen* (der Gegenstand wäre
derselbe, nur unauffindbar – die Roadmap führte ihre offenen Punkte in einer Schreibweise,
die keine Suche kennt).

### E5 – Ist `tests/TEST_CATALOG.md` mit 31 offenen Ergebniszellen inhaltlich vollständig?

**Auflösung: ja.** Der Gegenstand des Katalogs sind die Testfälle, nicht ihre Ergebnisse;
die Ergebnisse sind Kriterium 2. Dasselbe gilt für `tests/EDGE_CASES.md`.

**Preis, benannt:** Ein Register auf `pilot`, dessen Ergebnisse offen sind, sieht
fortgeschrittener aus, als der Testbestand ist. **Dagegen steht Punkt 4 desselben
Abschnitts** – ein Träger auf `pilot` ist strukturell abgenommen, nicht erprobt – und der
Umstand, dass die Gegenrichtung Kriterium 3 zum dritten Mal an Kriterium 2 kettete.

**Verworfen:** *Beide Register bis zum ersten Sitzungstest liegen lassen* (genau die
Kettung, die D-103 und D-107 je einmal gelöst haben).

### E6 – Was geschieht mit dem Statuszusatz des Referenzpacks?

**Auflösung:** `entwurf (Referenzpack der Erstfassung)` wird zu `pilot (Referenzpack der
Erstfassung)`. Der Zusatz beschreibt die Rolle des Packs, nicht seinen Status.

**Preis:** keiner. Prüfung 46 und Prüfung 47 vergleichen das **erste Wort** des Werts –
gebaut genau für diesen Träger (E6 von `CR-2026-070`).

### E7 – Wird in diesem Release eine Prüfung gebaut?

**Auflösung: nein.** Die Anweisung des Menschen vom 2026-09-15 gilt: keine neue Prüfung,
solange eine Zahl zu senken ist. Dieses Release senkt Kriterium 3 von 41 auf 1.

**Und es gäbe auch nichts zu bauen:** Die Unterscheidung zwischen Schlitz und Nennung ist
nach D-102 ausdrücklich **nicht** maschinell; eine Prüfung darauf wäre eine Prüfung, die
mehr verspricht, als sie leistet – der wiederkehrende Befundtyp dieses Projekts.
**Prüfung 46 fängt jede Bewegung der Zahl ohnehin, in beide Richtungen.**

### E8 – Wird `docs/ROADMAP.md` aus dem Zählbereich genommen?

**Auflösung: nein, und die Frage bleibt offen** (`K-39`). Sie wird in jedem Release
fortgeschrieben, ihre Steckbriefversion steht seit `0.2.0` unverändert, und `CHANGELOG.md`
– der Träger mit derselben Eigenschaft – ist vom Zählbereich ausgenommen. **Der Vorgang hat
sich ausdrücklich nicht auf diesem Weg entlastet:** Einen Träger aus dem Zählbereich zu
nehmen, um eine Zahl zu senken, ist die Bewegung, die `CR-2026-070` E6 verworfen hat.

**Preis, benannt:** Die Roadmap führt weiter eine Version, die niemand pflegt, und einen
Status, der wenig über sie aussagt. Das ist der Gegenstand von `K-39`.

## 8. Prüffragen

- [x] **Richtige Ebene nach Entscheidungsbaum 6?** — Ja. Gegenstand ist der Status der
  Module des Frameworks selbst; das ist Core.
- [x] **Verschärfungsprinzip eingehalten?** — Ja. Kein Statuswechsel lockert eine
  Verhaltensregel; die drei Auslegungen halten (d) und (a) unverändert und schreiben nur
  fest, wie sie gelesen werden. Keine Berührung von V1–V12 oder K3.
- [x] **Widerspruchsfreiheit geprüft?** — Gelesen: `01-governance.md` Abschnitt 5,
  `08-skill-conventions.md` Abschnitt 7, `checklists/11-framework-release.md`,
  `governance/RELEASE_PROCESS.md`, `prompts/README.md`, `docs/ROADMAP.md` (Standzeile,
  AP2, AP3, P3), D-11, D-102 bis D-108. **Ein Widerspruch gefunden und behoben:**
  `prompts/README.md` Abschnitt 7 behauptete nach dem Wechsel, alle zwölf Vorlagen stünden
  auf `entwurf`.
- [x] **Laufzeitfassungen betroffen?** — Nein. Weder die Wurzel-Anweisungsdatei noch die
  Regelablage noch die Berechtigungsdatei führen einen Modulstatus. `install.py --update`
  fasst in diesem Release keine Datei außerhalb von `leitwerk-core/` an.
- [x] **Belegstatus korrekt?** — Keine produktbezogene Aussage ist berührt. **Im
  Gegenteil:** Der einzige Träger, dessen Belegstatus offen ist, ist deshalb **nicht**
  abgenommen.
- [x] **Test- und Validierungsbedarf?** — Keine neue Prüfung (E7). Validatorlauf 0/0;
  Sondenlauf unverändert in beiden Kodierungsumgebungen, weil weder Prüfungen noch Sonden
  geändert sind.
- [x] **Auswirkungen auf Overlays?** — Keine. Der Modulstatus ist eine Angabe des Kerns;
  übernehmende Projekte lesen ihn, setzen ihn nicht.
- [x] **Zahlen nachgezählt?** — Ja, und **fünf eigene waren falsch** (35 statt 31
  Fundstellen, 13 statt 18 Dateien, fünf statt sechs Verfahrensschritte, sieben statt fünf
  Verfahrensregeln, „elf der dreizehn" bei einer Aufzählung von sieben). Gefunden im
  Durchgang vor dem Commit.
- [x] **Dokumentation:** CHANGELOG, Decision Log (D-109 bis D-111, `K-39` neu), Roadmap,
  zwei Protokolle.

## 9. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** (E1 bis E8) |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Die Bedingung stand, das Vokabular war durchgesetzt, die Bündelform erprobt – und das Hindernis lag im Gegenstand statt in der Bedingung. Vierzig Träger sind je einzeln gegen (a) bis (d) geprüft und abgenommen; der eine, der die Bedingung nicht erfüllt, bleibt stehen und seine Begründung steht namentlich. **Kriterium 3: 41 → 1** |
| Ziel-Release | **0.52.0** |
| Decision-Log-Eintrag | **D-109** (Schlitz, Organisationswert und Nennung – die drei Bauformen von (d)), **D-110** (`devin-desktop` bleibt auf `entwurf`; `claude-code` nicht), **D-111** (ein Register ist vollständig, wenn es seinen Gegenstand führt); **`K-39`** neu |

## 10. Umsetzung

- [x] Vierzig Statuszellen von `entwurf` auf `pilot`; der Zusatz des Referenzpacks bleibt
- [x] `clients/devin-desktop/CLIENT_PACK.md` unverändert auf `entwurf`, mit Wächter im
      Patchskript
- [x] Keine Version erhöht, kein Eintrag im Änderungsverlauf eines Trägers (D-106)
- [x] `prompts/README.md` Abschnitt 7 nachgezogen
- [x] Standzeile, Kriterientabelle, AP3 und P3-Posten der Roadmap nachgezogen; Abschnitte
      „Was 0.52.0 gebracht hat" und „Was 0.52.0 offen lässt" ergänzt
- [x] `VERSION` auf 0.52.0; CHANGELOG-Eintrag
- [x] Decision Log: D-109 bis D-111, `K-39`
- [x] Validator ohne Fehler; Sondenlauf in beiden Kodierungsumgebungen
- [x] **Dokumentation:** zwei Protokolle
- [ ] **Zur Entscheidung offen, mit einem späteren Vorgang:** `K-37` (Versionszelle der
      Vorlagen), `K-38` (Einordnung einer gestiegenen Zahl durch Prüfung 46), `K-39`
      (Modulträgerschaft der Roadmap)
