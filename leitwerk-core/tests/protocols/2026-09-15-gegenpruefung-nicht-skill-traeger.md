# Gegenprüfung: `K-36`, die zwölf Träger ohne Statuszeile und die Abnahme des ersten Nicht-Skill-Bündels

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-15 |
| Framework-Version | `0.50.0` (Stand `main`, Commit `0f3ed1f`); umgesetzt mit `0.51.0` |
| Gegenstand | Kriterium 3 von D-11 – *„alle Modulstatus oberhalb `entwurf`"*. Gezählt von Prüfung 46 zu Beginn: **52** |
| Anlass | Kandidat 1 der Übergabe, mit der ausdrücklichen Auflage, **zuerst `K-36` zu entscheiden**: Tragen die elf Module unter `framework/core/` eine Statuszeile? |
| Antrag | `CR-2026-073`, D-105 bis D-108, K-36, K-38 |
| Prüfmethode | Abzählen am Bestand mit der Leseregel der Prüfung 46 (`_d11_zaehlen`, Kriterium 3) und mit einer zweiten, unabhängigen Erkennungsregel für den Steckbrief; je Träger die vier Bedingungen (a) bis (d) aus `framework/core/01-governance.md` Abschnitt 5 Punkt 3 gegen den vorliegenden Stand gehalten, Fundstelle je offene Marke |
| Ausgeführte Befehle | Vier Messskripte über `leitwerk-core/` (Ausgaben in Abschnitt 2 und 3 unverändert); `python leitwerk-core/tests/scripts/validate-framework.py --root .` |
| Ergebnis | **`K-36` ist mit ja zu beantworten, und der Gegenstand ist zwölf statt elf.** Die Antwort steht im Gründungstext von D-11. Die Definition des Modulträgers war selbstbezüglich und ist der eigentliche Befund. **23 Träger sind abgenommen**; zwei Nebenbefunde sind angefallen, einer davon eine zweite, strengere Übergangsbedingung, die seit der Erstfassung in `prompts/README.md` steht |

## 1. Warum diese Gegenprüfung mit der Bedingung beginnt

Das ist der dritte Vorgang in Folge, dem eine Bedingung vorangestellt ist, und der dritte,
bei dem die Bedingung nicht hält, wie sie dasteht:

| Release | Die Bedingung | Der Fehler |
|---|---|---|
| 0.49.0 | drei Einwände aus `CR-2026-019` | falsch **gewählt** – hielt zweiunddreißig Releases |
| 0.50.0 | „erst die Vorentscheidung, die Skills sind an Kriterium 2 gekettet" | falsch **gelesen** – „bestanden" steht in der Zeile `aktiv` |
| **0.51.0** | „`K-36`: die **elf** Module unter `framework/core/`" | **richtig gestellt, falsch gezählt** – es sind zwölf |

**Die Frage von `K-36` ist diesmal die richtige.** Was daneben lag, ist ihr Gegenstand.

## 2. Die Messung: wie viele Träger führen keine Statuszeile?

Gemessen mit zwei Skripten, die dieselbe Frage auf zwei Wegen stellen. Das erste sucht
die Steckbriefzeile mit der Leseregel der Prüfung 46 (erste sechzig Zeilen); das zweite
erkennt den **Steckbrief selbst** – die erste Tabelle des Dokuments, vor der ersten
Überschrift der Ebene 2, mit der Kopfzeile `\| Attribut \| Wert \|`.

```
Kerndateien (.md) im Zaehlbereich: 167
  MIT Statuszeile ................ 69
  Steckbrief OHNE Statuszeile .... 12
  ganz OHNE Steckbrief ........... 86
```

**Die zwölf:**

| # | Träger | Steckbrief führt |
|---|---|---|
| 1–11 | `framework/core/00-principles.md` bis `framework/core/10-error-escalation.md` | Modul-ID, Ebene, Verbindlichkeit, Owner, Version |
| 12 | `prompts/README.md` | Ebene, Verbindlichkeit, Owner, Version, Grundlage |

### 2.1 Der zwölfte war nicht gesucht

`K-36` nennt elf, weil die Erhebung von 0.50.0 nur `framework/core/` abgesucht hat.
`prompts/README.md` führt **denselben Steckbrief** und ist ein normatives Dokument: Seine
Steckbriefzeile sagt *„normativ (Abschnitte 2, 3, 5, 6, 7)"*, und Abschnitt 2 trägt vier
nummerierte Regeln, von denen zwei ein MUSS enthalten.

**Damit war die eigene Zahl erneut zu klein** – der häufigste Einzelbefund dieses
Repositoriums. Die Regel gilt auch für einen Klärungspunkt.

### 2.2 Und eine Regel, die zu breit gewesen wäre

Die erste Fassung der Erkennungsregel suchte die Kopfzeile `\| Attribut \| Wert \|` in
den ersten sechzig Zeilen. Sie meldete **dreizehn** Träger ohne Statuszeile – der
dreizehnte war `templates/PLAN_TEMPLATE.md`.

**Das ist ein Fehltreffer, und ein lehrreicher.** Dort steht die Tabelle nicht im
Steckbrief, sondern im **Körper** der Vorlage, hinter einer Überschrift der Ebene 2:

```
## Änderungsplan: <Kurztitel> (<Ticket-Referenz oder Platzhalter>)

| Attribut | Wert |
|---|---|
| Erstellt mit | `fw-plan` v<Version> |
| Bestätigungsstatus | entwurf / bestätigt durch <Rolle> am <Datum> / abgelehnt |
```

Es ist das Formular für den Plan, der aus der Vorlage entsteht – und die Datei führt zu
Recht keinen Modulstatus. **Die Erkennungsregel ist deshalb an der Stellung festgemacht,
nicht an der Zeichenfolge.** Gegen den Bestand gemessen erkennt sie 81 Steckbriefe (69
mit und 12 ohne Statuszeile) und keinen Fehltreffer.

## 3. `K-36`: Die Antwort steht im Gründungstext von D-11

Der Klärungspunkt nennt beide Antworten vertretbar. **Sie sind es nicht.**

`CR-2026-001` ist der Antrag, der D-09 durch D-11 ersetzt hat. Er formuliert Kriterium 3
wörtlich:

> 3. Alle **Core-Module**, Skills und Packs haben einen Status oberhalb von `entwurf`.

Dieselbe Formulierung steht seither im Prüfpunkt von `FW-CL-11` – der Checkliste, die
1.0.0 freigibt. **Die Kurzfassung im Decision Log** („alle Modulstatus oberhalb
`entwurf`") **hat die Aufzählung verloren, und die Zählregel hat die Kurzfassung
gelesen.**

Das ist derselbe Befundtyp wie bei allen vier Zählregeln von 0.48.0: nicht falsch
geschrieben, sondern das richtige Ergebnis einer Regel, die weniger kann als ihr
Kriterium verlangt.

### 3.1 Der eigentliche Befund ist die Definition

`01-governance.md` Abschnitt 5 Punkt 1 sagte bis 0.50.0:

> **Modulträger** ist jede versionierte Datei des Frameworks, die in ihrem Steckbrief eine
> Zeile `\| Status \| … \|` führt

**Modulträger ist, wer die Statuszeile führt** – also entkommt dem Lebenszyklus, wer sie
weglässt. Eine Definition, die ihren Gegenstand über das Merkmal bestimmt, das er tragen
soll, sieht vollständig aus, solange niemand zählt, wer nicht dazugehört.

**Zwölf Dateien taten genau das, darunter die elf normativsten Dokumente des
Frameworks.** Ohne eine Prüfung wäre die nächste genauso entkommen; deshalb gehört zu
D-105 Gegenstand 2 der Prüfung 47 und nicht nur eine berichtigte Zeile.

## 4. Die Abnahme, Bündel 1: die elf Checklisten

Geprüft je Träger gegen `01-governance.md` Abschnitt 5 Punkt 3, Zeile `entwurf → pilot`.
**(b) gilt für alle gemeinsam:** Der Validatorlauf steht auf 0 Fehler, 0 Warnungen.

| Träger | (a) vollständig | (c) offene `VERIFY`-Marker | (d) offene `<TBD…>` |
|---|---|---|---|
| `checklists/01-preflight.md` | ja – Zweck, vier Prüfblöcke, Abbruch- und Eskalationskriterien, Ergebnis und Nachweis | keiner | keiner |
| `checklists/02-privacy-context.md` | ja – drei Prüfblöcke je Kontextquelle, K2 und Testdaten | keiner | keiner |
| `checklists/03-before-code-change.md` | ja – vier Prüfblöcke von Freigaben bis Grenzen der Änderung | keiner | keiner |
| `checklists/04-review-ai-code.md` | ja – fünf Prüfblöcke, RV1 bis RV12 vollständig abgebildet | keiner | keiner |
| `checklists/05-testing.md` | ja – Inhalt, Integrität der Testbasis, Ausführung und Lücken | keiner | keiner |
| `checklists/06-security.md` | ja – Einstufung, Code-Prüfpunkte, KI-spezifische Prüfpunkte | keiner | keiner |
| `checklists/07-new-dependency.md` | ja – Bedarf, Herkunft, Zustand, Lizenz, Einführung | keiner | keiner |
| `checklists/08-merge-request.md` | ja – vor dem Erstellen und vor dem Mergen getrennt | keiner | keiner |
| `checklists/09-onboarding.md` | ja – Voraussetzungen, acht Module, Abschluss | keiner | **einer, unkritisch:** Z23 `<TBD: Referenz auf Unterweisung>` – die Datenschutzunterweisung **der Organisation**; D-11 nimmt organisatorische Vorgaben ausdrücklich aus |
| `checklists/10-project-adoption.md` | ja – Voraussetzungen, technische Integration, Organisation, Aktivierung | keiner | **vier, alle unkritisch:** Z24 `<TBD: Nachweis der Einstellung>`, Z59 `<TBD: Ablageort für Ergebnisberichte>` und `<TBD: Ablage von Plänen im Projekt>` – Overlay-Werte; Z35 `<TBD>` ist eine **Nennung**, kein Schlitz (der Prüfpunkt verlangt, dass das Overlay keine offenen `<TBD>` trägt) |
| `checklists/11-framework-release.md` | ja – Inhalt, Projektneutralität, Produktstand, Tests, Abschluss | **einer, und er ist eine Nennung:** Z40 nennt den Marker als Gegenstand des Prüfpunkts, trägt ihn nicht. Das ist einer der vier Träger aus dem Befund von 0.50.0 | keiner |

**(e) ist mit diesem Abschnitt erfüllt:** Jeder der elf ist namentlich genannt, und (a)
bis (d) stehen je Träger.

## 5. Die Abnahme, Bündel 2: die zwölf Träger mit dem Kernmodul-Steckbrief

| Träger | (a) vollständig | (c) offene `VERIFY`-Marker | (d) offene `<TBD…>` |
|---|---|---|---|
| `framework/core/00-principles.md` | ja – Konventionen (Verbindlichkeit, Belegstatus, Platzhalter), zehn Leitprinzipien, Ableitungen | **eine Nennung:** Z32 erklärt den Marker in der Belegstatustabelle | **eine Nennung:** Z36 erklärt die Platzhalterkonvention |
| `framework/core/01-governance.md` | ja – Geltung, Rollen, Änderungsgrundsätze, Auditierbarkeit, Lebenszyklus | keiner | **eine Nennung:** Z51 zitiert die Marke in der Übergangsbedingung |
| `framework/core/02-privacy.md` | ja – Ausgangslage, vier Kontextklassen mit K3-Liste, Bereitstellung, K2-Freigabe, Vorfall, technische Absicherung | **zwei echte:** Z14 (Art und Ort der Codebasis-Indexierung) und Z56 (Spaces und geteilter Kontext). **Benannt, sperren nicht** – gezählt in Kriterium 1 | **vier, alle unkritisch:** Z14, Z78, Z87, Z89 – Ergebnis der Datenschutz- und Vertragsprüfung, Löschverfahren, Nachweis der Einstellung, Betriebssystem. Sämtlich Werte der aufnehmenden Organisation, und Abschnitt 1.3 regelt ihr Fehlen selbst |
| `framework/core/03-security.md` | ja – Schutzziele, zehn Bedrohungen, vier Kontrollschichten, Berechtigungspolitik, Prompt Injection, Supply Chain | keiner | **einer, unkritisch:** Z28 `<TBD: Erweiterungsrichtlinie>` – Vorgabe der Organisation |
| `framework/core/04-quality.md` | ja – Gleichbehandlung, Q1 bis Q8, Definition of Done, Metriken | keiner | keiner |
| `framework/core/05-working-model.md` | ja – vierzehn Schritte, fünf Betriebsmodi mit Einzelbeschreibung, sechs Querschnittsregeln, Standardformat | keiner | **zwei, unkritisch:** Z74 und Z140 – Ablageorte, die das Overlay festlegt |
| `framework/core/06-prompting-rules.md` | ja – Aufbau einer Anweisung, acht Regeln, sechs unzulässige Muster | keiner | **einer, unkritisch:** Z33 `<TBD: Arbeitssprache>` – Overlay-Wert |
| `framework/core/07-review-rules.md` | ja – Grundsätze, RV1 bis RV12, Review-Tiefe je Stufe, Umgang mit Befunden | keiner | keiner |
| `framework/core/08-skill-conventions.md` | ja – Begriff, Ablage, Frontmatter, Pflichtinhalte, Trennung, Verhalten, Lebenszyklus | keiner | keiner |
| `framework/core/09-risk-model.md` | ja – Grundregeln, R1 bis R13, drei Kontrollstufen, V1 bis V12 | keiner | **einer, unkritisch:** Z41 `<TBD: Schwellenwert für Änderungsumfang>` – Overlay-Wert |
| `framework/core/10-error-escalation.md` | ja – S1 bis S10, E0 bis E4, Umgang mit Fehlern, Wiederanlauf | keiner | keiner |
| `prompts/README.md` | ja – Zweck, Verhältnis Prompt/Skill, Aufbau, Übersicht der zwölf, Regeln, Verwendung, Versionierung | keiner | **drei:** Z37 ist eine **Nennung** der Platzhalterkonvention; Z70 und Z79 sind Overlay-Werte (Arbeitssprache, Ablageort) |

**(e) ist mit diesem Abschnitt erfüllt.**

### 5.1 Was die Abnahme ausdrücklich nicht behauptet

`01-governance.md` Abschnitt 5 Punkt 4 sagt es, und es gilt hier wörtlich: **Ein Träger
auf `pilot` ist strukturell abgenommen, nicht erprobt.** Kein Sitzungstest ist gefahren;
ob ein KI-Client diesen 23 Trägern folgt, sagt allein Kriterium 2, und das steht
unverändert auf 118.

## 6. Nebenbefund – `prompts/README.md` trägt eine zweite, strengere Übergangsbedingung

Abschnitt 7 des Trägers, der in Bündel 2 zur Abnahme stand, sagt seit der Erstfassung:

> Alle Vorlagen liegen im Status `entwurf`. Der Übergang nach `pilot` setzt voraus:
> Validierung bestanden, **mindestens eine dokumentierte Testsitzung je Vorlage auf dem
> Übungsrepository**, Review durch `<FRAMEWORK_OWNER>`.

**Das ist eine eigene Übergangsbedingung für zwölf Modulträger, und sie steht in keinem
Register.** Ein `grep` über den Bestand findet genau diese eine Stelle; das Modell in
`01-governance.md` Abschnitt 5 und `08-skill-conventions.md` Abschnitt 7 kennt sie nicht.

**Es ist derselbe Fehler, den D-103 sieben Tage zuvor berichtigt hat.** Dort stand
„Testfälle bestanden" in der Spalte einer Tabelle und wurde in der falschen Zeile
gelesen; hier steht er ausgeschrieben in einer anderen Ablage und wurde nie gelesen.
**Beide Male kettet er Kriterium 3 an Kriterium 2** – den Posten, der Modellzeit und ein
Devin-Kontingent kostet.

**Gefunden hat ihn keine Suche**, sondern der Umstand, dass der Träger selbst zur Abnahme
anstand. Wer einen Gegenstand anfasst, findet die Regel daneben, die niemand kennt.

**Aufgelöst mit D-107.** Die Testsitzung bleibt Voraussetzung für `aktiv`. **Die zwölf
Prompt-Vorlagen werden mit diesem Release nicht gehoben** – entschieden ist allein,
welche Bedingung für sie gilt.

## 7. Nebenbefund – Versionsregel gegen Statuswechsel

D-103 hat die dreizehn Skills ohne Versionswechsel gehoben. Die Begründung ist allgemein,
der Vermerk steht aber nur in einem Record über Skills. Dagegen stehen zwei Sätze:

| Träger | Wortlaut |
|---|---|
| `RELEASE_PROCESS.md` Abschnitt 1 Punkt 2 | *„Jede Änderung an einem dieser Artefakte erhöht dessen Version im selben Release"* |
| `checklists/11-framework-release.md` | *„**MUSS** Version je geänderter Checkliste und je geändertem Prompt gepflegt"* |

**Beim ersten gehobenen Nicht-Skill-Träger stehen sie gegeneinander.** Mit D-106 gilt: Ein
reiner Statuswechsel ist keine Änderung im Sinne dieser Sätze. **Preis, benannt:** Der
Änderungsverlauf des einzelnen Trägers verzeichnet ihn nicht.

## 8. Was diese Gegenprüfung nicht leistet

- **Sie hebt 41 Träger nicht.** Zwölf Prompt-Vorlagen, sechs Entscheidungsbäume, sieben
  Governance-Dokumente, drei `docs/`, zwei `tests/`-Register, vier Onboarding-, zwei
  Pilot-, drei Client-Pack- und zwei Role-Pack-Dokumente stehen weiter auf `entwurf`.
- **Sie sagt nichts über das Verhalten eines KI-Clients** gegenüber den 23 abgenommenen
  Trägern (Abschnitt 5.1).
- **Sie senkt Kriterium 1 und 2 um nichts.** 29 und 118 stehen unverändert.
- **Sie beantwortet `K-37` nicht** – die Versionszelle der vier Vorlagen hat dieselbe
  Bauform wie ihre Statuszelle, und Prüfung 47 sichert nur die Statuszelle ab.
- **Sie berichtigt das Hauptdokument nicht.** Sein Satz „Alle Module im Status `entwurf`"
  ist mit 0.51.0 für 36 Träger falsch statt für dreizehn; der Grund, ihn nicht
  nachzuziehen, ist unverändert der von 0.50.0.

## 9. Bewertung

**`K-36` ist mit ja zu beantworten, und die Antwort war nicht zu finden, sondern zu
lesen.** Sie steht seit dem 2026-09-10 im Gründungstext von D-11 und seither wörtlich im
Prüfpunkt von `FW-CL-11`.

**Der Ertrag liegt daneben:** Die Definition des Modulträgers ließ ihren Gegenstand
entkommen, und eine zweite Übergangsbedingung stand seit der Erstfassung in einer Ablage,
die niemand als Regelquelle liest. **Beide sind nur aufgefallen, weil ein Träger zur
Abnahme anstand** – zum siebten Mal in Folge war die Aufgabenbeschreibung kleiner als die
Aufgabe.
