# Gegenprüfung: die Abnahme der restlichen einundvierzig Nicht-Skill-Träger

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-15 |
| Framework-Version | `0.51.0` (Stand `main`, Commit `b2a75af`); umgesetzt mit `0.52.0` |
| Gegenstand | Kriterium 3 von D-11 – *„alle Modulstatus oberhalb `entwurf`"*. Gezählt von Prüfung 46 zu Beginn: **41** |
| Anlass | Kandidat 1 der Übergabe. **Erstmals seit 0.48.0 ohne vorangestellte Vorentscheidung:** `K-36` ist mit 0.51.0 geklärt, die Übergangsbedingung steht seit 0.50.0 in `framework/core/01-governance.md` Abschnitt 5, das Statusvokabular hält seit 0.51.0 Prüfung 47, und die Bündelform ist an zwei Gattungen erprobt |
| Antrag | `CR-2026-074`, D-109 bis D-111, `K-39` neu |
| Prüfmethode | Je Träger die vier Bedingungen (a) bis (d) aus `framework/core/01-governance.md` Abschnitt 5 Punkt 3, Zeile `entwurf → pilot`, gegen den vorliegenden Stand gehalten; Fundstelle je offener Marke, mit Zeilennummer erhoben. Die Träger sind nach Gattung gebündelt; **jeder ist namentlich genannt**, wie (e) es verlangt |
| Ausgeführte Befehle | Zwei Messskripte über `leitwerk-core/` (Auszählung nach der Leseregel der Prüfung 46; Erhebung der Marken je Träger mit Zeilennummer); `python leitwerk-core/tests/scripts/validate-framework.py --root .` |
| Ergebnis | **Vierzig der einundvierzig Träger sind abgenommen; Kriterium 3 fällt von 41 auf 1.** Der eine, der nicht abgenommen ist, sperrt sich selbst: `clients/devin-desktop/CLIENT_PACK.md`. Drei Ermessensfragen sind dabei angefallen und in D-109 bis D-111 aufgelöst; ein Klärungspunkt bleibt offen (`K-39`) |

## 1. Warum dieser Vorgang ohne Vorentscheidung beginnt – und was daraus folgt

Die drei Vorgänger trugen je eine vorangestellte Bedingung, und alle drei hielten nicht,
wie sie dastanden:

| Release | Die Bedingung | Der Fehler |
|---|---|---|
| 0.49.0 | drei Einwände aus `CR-2026-019` | falsch **gewählt** – hielt zweiunddreißig Releases |
| 0.50.0 | „die Skills sind an Kriterium 2 gekettet" | falsch **gelesen** – „bestanden" steht in der Zeile `aktiv` |
| 0.51.0 | „`K-36`: die **elf** Module unter `framework/core/`" | richtig gestellt, **falsch gezählt** – es sind zwölf |

**Diesmal steht keine Bedingung davor.** Die Übergabe hat das ausdrücklich vermerkt und
denselben Satz hinterhergeschickt: *„genau deshalb ist zu erwarten, dass das Hindernis
woanders liegt."*

**Es liegt im Gegenstand.** Einer der einundvierzig Träger besteht die Bedingung nicht –
und er sagt das selbst, in dem Absatz unter seinem Steckbrief, seit acht Releases
unverändert (Abschnitt 3.1).

## 2. Der Gegenstand: die einundvierzig, nach Gattung

Gezählt mit der Leseregel der Prüfung 46 (`_d11_zaehlen`, Kriterium 3: erste Steckbriefzeile
`| Status | … |` im Kopf einer `.md` des Zählbereichs, verglichen am **ersten Wort** des
Werts).

| # | Gattung | Anzahl | Abnahme |
|---|---|---|---|
| 1 | Prompt-Vorlagen (`prompts/01…12`) | 12 | **alle** |
| 2 | Entscheidungsbäume (`decision-trees/01…06`) | 6 | **alle** |
| 3 | Governance-Dokumente | 7 | **alle** |
| 4 | `docs/` | 3 | **alle** |
| 5 | `tests/`-Register | 2 | **alle** |
| 6 | Onboarding-Dokumente | 4 | **alle** |
| 7 | Pilot-Dokumente | 2 | **alle** |
| 8 | Client-Pack-Dokumente | 3 | **zwei von drei** |
| 9 | Role-Pack-Dokumente | 2 | **alle** |
| | **Summe** | **41** | **40** |

**(b) gilt für alle gemeinsam:** Der Validatorlauf gegen den fertigen Baum steht auf
0 Fehler, 0 Warnungen.

## 3. Die drei Ermessensfragen, die die Abnahme aufgeworfen hat

Punkt 3 (d) der Übergangsbedingung lautet:

> Ein offener Ausfüllwert (`<TBD…>`) sperrt den Übergang **nicht**, wenn er einen Wert der
> aufnehmenden Organisation bezeichnet; er sperrt ihn, wenn er eine Aussage des Frameworks
> offenlässt.

Die Bedingung ist richtig gestellt. **Sie kennt aber nur zwei Fälle, und im Bestand gibt es
drei.** Der dritte ist die **Nennung**: eine Stelle, die die Marke `<TBD…>` zitiert oder
einen offenen Punkt benennt, statt selbst einen Wert offenzulassen. D-102 hat genau das
schon einmal festgestellt – *„`<TBD:` trägt drei Bedeutungen"* – und daraus geschlossen,
dass die Marke als **maschinelle** Bedingung untauglich ist. Für die Abnahme je Träger gilt
dasselbe eine Ebene höher: **Die Trennung ist zu treffen, nicht zu zählen.**

### 3.1 `clients/devin-desktop/CLIENT_PACK.md` sperrt sich selbst

Sein Steckbrief (Z11 und Z12):

```
| Geprüfte Clientversion | <TBD: verbindliche Zielversion; Roadmap AP2> |
| Datum der Prüfung | <TBD: steht aus> |
```

Und der Absatz unmittelbar darunter (Z14):

> **Keine Einstufung dieses Packs ist gegen eine reale Installation belegt.** […] Solange
> die Zielversion nicht festgelegt und geprüft ist (Roadmap AP2), gilt das Pack als
> **unbelegt**.

**Beide Schlitze bezeichnen keinen Wert der aufnehmenden Organisation.** Sie bezeichnen
eine Festlegung des Framework Owners, die `AP2` als Arbeitspaket führt und die aussteht.
Das ist der zweite Fall von (d), und er **sperrt** – der Träger bleibt auf `entwurf`
(D-110).

> ⚠️ **Der Träger ist nicht durch eine Suche aufgefallen.** Eine Auszählung der Marke
> `<TBD…>` über die einundvierzig Träger meldet **fünfunddreißig** Fundstellen in **dreizehn**
> Dateien; dreiunddreißig davon sind Werte der Organisation oder Nennungen. **Aufgefallen
> ist er, weil er zur Abnahme anstand und gelesen wurde.** Zum zweiten Mal in Folge: Wer
> einen Gegenstand anfasst, findet die Aussage daneben, die niemand nachgezählt hat.

### 3.2 Und `clients/claude-code/CLIENT_PACK.md`, das denselben Satz trägt?

Sein Steckbrief trägt in beiden Zellen **echte Werte**:

```
| Geprüfte Clientversion | 2.1.267 (AP2-Dokumentenabgleich, tests/protocols/2026-09-10-AP2-claude-code.md). …
| Datum der Prüfung | 2026-09-10 – Dokumentenabgleich und Prüfung der erzeugten Artefakte; …
```

Der Absatz darunter sagt denselben Satz wie beim Schwesterpack – *„Solange die Zielversion
nicht festgelegt und geprüft ist, gilt das Pack als **unbelegt**"* –, und dieser Träger ist
trotzdem abgenommen. **Die Trennlinie ist der Schlitz, nicht der Satz über den Belegstand**
(D-109):

- Ein **Schlitz** im Steckbrief ist eine Aussage des Frameworks, die offensteht. (d) greift.
- Ein **Satz über den Belegstand** sagt, was gemessen ist und was nicht. Dafür ist der
  Status nicht zuständig: `01-governance.md` Abschnitt 5 Punkt 4 sagt wörtlich, ein
  Statuswert sei **keine** Aussage über das Verhalten eines KI-Clients, und ein Träger auf
  `pilot` sei *strukturell abgenommen, nicht erprobt*.

**Die Unterscheidung ist auch sachlich und nicht nur formal:** `claude-code` ist gegen eine
benannte Clientversion abgeglichen und das Protokoll dazu liegt vor; `devin-desktop` ist
gegen **keine** Version abgeglichen. Der Unterschied steht in den Zellen, weil er besteht.

### 3.3 Dieselbe Marke in zwei Trägern – und zweimal etwas anderes

`docs/ROADMAP.md` führt in `AP2` die Zeile:

```
| Offene Entscheidungen | <TBD: verbindliche Zielversion von Devin Desktop> |
```

**Das ist derselbe offene Punkt, der das Client Pack sperrt** – und in der Roadmap sperrt
er nichts. Die Zelle steht in einer Spalte namens *Offene Entscheidungen*: Sie ist die
**Nennung** eines offenen Punktes, und ein Dokument, dessen Zweck es ist, offene Punkte zu
führen, ist vollständig, **wenn** es sie führt. Im Client Pack dagegen fehlt der Wert einer
Aussage über ein Produkt.

| | `docs/ROADMAP.md`, AP2 | `clients/devin-desktop/CLIENT_PACK.md`, Steckbrief |
|---|---|---|
| Zeichenfolge | `<TBD: verbindliche Zielversion …>` | `<TBD: verbindliche Zielversion …>` |
| Spalte | *Offene Entscheidungen* | *Geprüfte Clientversion* |
| Bedeutung | „hier ist etwas offen" | „hier fehlt ein Wert" |
| (d) | greift nicht | **greift** |

**Sieben der dreizehn `<TBD…>`-Fundstellen der Roadmap sind von dieser Art** (Z2057, Z2073,
Z2101, Z2129, Z2143, Z2171, Z2227 in den Zeilen *Offene Entscheidungen* der Arbeitspakete);
die übrigen sechs sind Zitate der Marke im Fließtext (Z201, Z494, Z528, Z1599, Z1786,
Z1921). **Keine davon ist ein unausgefüllter Wert einer Aussage der Roadmap.**

### 3.4 Sperrt ein Register mit offenen Ergebnissen sich selbst?

`tests/TEST_CATALOG.md` führt **31 Ergebniszellen auf `offen`** – das ist der größte Teil
von Kriterium 2 von D-11. Die Frage bei (a) lautet: Ist ein Testkatalog *inhaltlich
vollständig*, dessen Ergebnisse offen sind?

**Ja** (D-111). Der Gegenstand des Katalogs sind die Testfälle: Kennung, Aufgabe,
Vorbedingung, Erwartung, Gegenerwartung, Prüfmittel. Alle sind ausgefüllt. **Die Ergebnisse
sind nicht sein Inhalt, sondern sein Gegenstand der Messung** – und sie sind Kriterium 2.

**Eine andere Antwort kettete Kriterium 3 an Kriterium 2, und zwar zum dritten Mal:**

| Release | Wo die Kettung stand | Wer sie gelöst hat |
|---|---|---|
| 0.50.0 | „Testfälle bestanden" in der falschen Zeile gelesen, dreizehn Skills | D-103 |
| 0.51.0 | eigene Bedingung in `prompts/README.md` Abschnitt 7, zwölf Vorlagen | D-107 |
| **0.52.0** | „ein Katalog mit offenen Ergebnissen ist unvollständig", zwei Register | **D-111** |

Dieselbe Bewegung, drei Releases, drei Ablagen. **Sie entsteht nicht aus Nachlässigkeit,
sondern weil sie wie Sorgfalt aussieht** – die Lehre von 0.49.0, zum dritten Mal
bestätigt.

`tests/EDGE_CASES.md` steht aus demselben Grund: Es führt zwanzig Grenzfälle mit Regel,
Auflösung und Fundstelle; ein einundzwanzigster ist kein offener Punkt, sondern ein noch
nicht eingetretener Fall.

## 4. Bündel 1 – die zwölf Prompt-Vorlagen

**Gattungsmerkmal:** acht Pflichtabschnitte (1. Zweck, 2. Einzusetzender Kontext,
3. Nicht einzusetzender Kontext, 4. Eingabeparameter, 5. Prompt-Vorlage, 6. Erwartetes
Ergebnis, 7. Prüfschritte, 8. Typische Fehlanwendungen). **Alle zwölf führen alle acht.**

**Mit D-107 ist für sie allein die Bedingung geklärt worden, nicht die Abnahme** – sie
steht hier nach.

| Träger | (a) vollständig | (c) offene `VERIFY`-Marker | (d) offene `<TBD…>` |
|---|---|---|---|
| `prompts/01-understand-codebase.md` | ja – acht Abschnitte, Vorlage mit Rückfrage- und Scoperegel | keiner | **eine Nennung:** Z53 weist den Client an, Unklares als `<TBD: …>` zu kennzeichnen |
| `prompts/02-impact-analysis.md` | ja – acht Abschnitte, drei Eingabeparameter mit Kontextklasse | keiner | **eine Nennung** (Z51) und **einer, unkritisch:** Z94 `<TBD: Ablageort für Ergebnisberichte>` – Overlay-Wert |
| `prompts/03-implementation-planning.md` | ja – acht Abschnitte, Optionsbewertung und Planformat | keiner | **eine Nennung** (Z52) und **zwei, unkritisch:** Z91 und Z101 `<TBD: Ablage von Plänen im Projekt>` – Overlay-Wert |
| `prompts/04-code-generation.md` | ja – acht Abschnitte, Vorlage mit Scope- und Testauflagen | keiner | keiner |
| `prompts/05-test-generation.md` | ja – acht Abschnitte, Fallabdeckung und Gegenerwartung | keiner | **eine Nennung:** Z51 |
| `prompts/06-refactoring.md` | ja – acht Abschnitte, Verhaltensgleichheit als Auflage | keiner | keiner |
| `prompts/07-debugging.md` | ja – acht Abschnitte, bereinigter Fehlerbericht als Pflichtparameter | keiner | keiner |
| `prompts/08-security-review.md` | ja – acht Abschnitte, Befundklassen und Meldeweg | keiner | keiner |
| `prompts/09-performance-analysis.md` | ja – acht Abschnitte, Messvorgabe vor Bewertung | keiner | keiner |
| `prompts/10-documentation.md` | ja – acht Abschnitte, Quellenbindung der Aussagen | keiner | keiner |
| `prompts/11-merge-request-review.md` | ja – acht Abschnitte, RV1–RV12 abgebildet | keiner | keiner |
| `prompts/12-developer-training.md` | ja – acht Abschnitte, Lernziel und Übungsform | keiner | keiner |

**(e) ist mit diesem Abschnitt erfüllt.** Alle zwölf gehen auf `pilot`.

## 5. Bündel 2 – die sechs Entscheidungsbäume

**Gattungsmerkmal:** drei Abschnitte – *Textbeschreibung (normativ)*, *Diagramm*
(Mermaid), *Hinweise* –, dazu im Steckbrief die Zeilen *Anwendung* und *Quelle*, die den
Baum an ein Kernmodul binden. **Alle sechs führen alle drei und beide Steckbriefzeilen.**

| Träger | (a) vollständig | (c) offene `VERIFY`-Marker | (d) offene `<TBD…>` |
|---|---|---|---|
| `decision-trees/01-context-allowed.md` | ja – sechs nummerierte Regeln, Diagramm mit allen Ausgängen, Quelle `02-privacy.md` | keiner | keiner |
| `decision-trees/02-may-ai-do-task.md` | ja – Regelfolge, Diagramm, Hinweise; Quelle `09-risk-model.md` und `01-governance.md` | keiner | keiner |
| `decision-trees/03-analyze-or-modify.md` | ja – Regelfolge, Diagramm, Hinweise; Quelle `05-working-model.md` und `09-risk-model.md` | keiner | keiner |
| `decision-trees/04-required-review.md` | ja – Regelfolge, Diagramm, Hinweise; Quelle `07-review-rules.md` | keiner | keiner |
| `decision-trees/05-stop-or-escalate.md` | ja – Regelfolge, Diagramm, Hinweise; Quelle `10-error-escalation.md` | keiner | keiner |
| `decision-trees/06-rule-placement.md` | ja – Regelfolge, Diagramm, Hinweise; die Ebenenzuordnung, auf die jeder Änderungsantrag verweist | keiner | keiner |

**(e) ist mit diesem Abschnitt erfüllt.** Alle sechs gehen auf `pilot`.

## 6. Bündel 3 – die sieben Governance-Dokumente

| Träger | (a) vollständig | (c) offene `VERIFY`-Marker | (d) offene `<TBD…>` |
|---|---|---|---|
| `governance/EXCEPTION_PROCESS.md` | ja – Geltung, Verfahren in fünf Schritten (Antrag, Prüfung, Genehmigung, Registrierung, Überprüfung), Grundsätze; alle drei Abschnitte normativ | keiner | keiner |
| `governance/FEEDBACK_PROCESS.md` | ja – Zweck, Kanäle und Erfassung, Auswertung, Erläuterung | keiner | **einer, unkritisch:** Z18 `<TBD: Feedbackkanal, z. B. Ticket-Typ im <ISSUE_TRACKER>>` – der Kanal **der Organisation**; der Prozess selbst ist beschrieben |
| `governance/FRAMEWORK_DEV_PROFILE.md` | ja – zwei Einsatzkontexte, Geltungsbereich, Lesen, Ändern, Grenzen, freigegebene Prüfkommandos, Erläuterung. **Der Träger, der den Arbeitsweg dieses Vorgangs selbst beschreibt** | keiner | keiner |
| `governance/INCIDENT_HANDLING.md` | ja – Geltung und Vorrang, Sofortmaßnahmen je Vorfallart, Erfassung, Rückfluss, Erläuterung | keiner | **zwei, beide unkritisch:** Z19 `<TBD: Löschverfahren laut Vertrag>` – der Vertrag der Organisation; Z26 `<TBD: Ablageort des Registers, außerhalb des Frameworks-Repositorys möglich>` – die Ablage der Organisation, und der Träger sagt das selbst |
| `governance/PRIORITY_HIERARCHY.md` | ja – die acht Stufen, die ergänzenden Regeln, die Widerspruchsprüfung mit Begründung, die Anwendung | keiner | keiner |
| `governance/RACI.md` | ja – Ausfüllhinweis, Matrix mit 21 Aktivitäten über elf Rollenspalten, Konsistenzregeln. **Keine Überschriften der Ebene 2; die Gattung ist eine Matrix und der Zweck verlangt keine** | keiner | keiner |
| `governance/RELEASE_PROCESS.md` | ja – acht Abschnitte von der Versionierung bis zur Auditierbarkeit; Abschnitt 1 trägt seit 0.51.0 die Regel aus D-106 | **einer, und er ist eine Nennung:** Z46 weist an, die Marker zu aktualisieren, trägt selbst keinen Verifikationsbedarf. **Einer der vier nennenden Träger aus dem Befund von 0.50.0** | **einer, unkritisch:** Z22 `<TBD: Prüfzyklus, Vorschlag quartalsweise>` – die Taktung **der Organisation**; der Vorschlag steht daneben |

**(e) ist mit diesem Abschnitt erfüllt.** Alle sieben gehen auf `pilot`.

## 7. Bündel 4 – die drei `docs/`

| Träger | (a) vollständig | (c) offene `VERIFY`-Marker | (d) offene `<TBD…>` |
|---|---|---|---|
| `docs/ADOPTION_GUIDE.md` | ja – Grundprinzip, Neuaufnahme als Schrittfolge, Aktualisierung auf ein neues Release, mehrere Repositories, Deinstallation, Begründung der Bündelung. **Mit 0.47.0 um die `.gitignore`-Zeile ergänzt, die zwei von zwei Projekten gefehlt hat** | keiner | keiner |
| `docs/ROADMAP.md` | ja – Stand, Arbeitspakete AP1–AP13, Abhängigkeitsübersicht, bewusst offen Gelassenes. **Ihr Zweck ist es, offene Punkte zu führen; sie führt sie** (Abschnitt 3.3) | **einer, und er ist eine Nennung:** Z2065 nennt in der Zielzeile von `AP2` den Marker als Gegenstand des Arbeitspakets. Einer der vier nennenden Träger | **dreizehn, keiner sperrend:** sieben in Zellen der Spalte *Offene Entscheidungen* (Z2057, Z2073, Z2101, Z2129, Z2143, Z2171, Z2227), sechs als Zitat der Marke im Fließtext (Z201, Z494, Z528, Z1599, Z1786, Z1921). **Begründung je Art in Abschnitt 3.3** |
| `docs/RUNTIME_GLOSSARY.md` | ja – Zweck, Regel, Begriffstabelle mit den Entsprechungen beider Packs, Abgrenzung, Nummernschema | keiner | keiner |

> ⚠️ **`docs/ROADMAP.md` ist abgenommen und trägt zugleich `K-39`.** Die Frage, **ob** sie
> ein Modulträger sein soll, ist eine andere als die, ob sie die Bedingung erfüllt. Sie
> erfüllt sie. Ob ein Dokument, das in jedem Release fortgeschrieben wird, überhaupt einen
> Modulstatus führen sollte – so wie `CHANGELOG.md`, das vom Zählbereich ausgenommen ist –,
> ist mit diesem Release **nicht** entschieden. **Der Vorgang hat sich ausdrücklich nicht
> auf diesem Weg entlastet:** Einen Träger aus dem Zählbereich zu nehmen, um eine Zahl zu
> senken, ist die Bewegung, die `CR-2026-070` E6 verworfen hat.

**(e) ist mit diesem Abschnitt erfüllt.** Alle drei gehen auf `pilot`.

## 8. Bündel 5 – die zwei `tests/`-Register

| Träger | (a) vollständig | (c) offene `VERIFY`-Marker | (d) offene `<TBD…>` |
|---|---|---|---|
| `tests/EDGE_CASES.md` | ja – Zweck, zwanzig Grenzfälle mit Regel, Auflösung und Fundstelle, Abgrenzung | keiner | keiner |
| `tests/TEST_CATALOG.md` | ja – sieben Verfahrensregeln, elf Testklassen mit allen Testfällen, Pflegeregel. **31 Ergebniszellen stehen auf `offen`; das ist Kriterium 2, nicht die Unvollständigkeit des Trägers** (D-111, Abschnitt 3.4) | keiner | **eine Nennung:** Z90 beschreibt in `FW-FI-02` das erwartete Ergebnis „Rest `<TBD>`/blockiert" |

**(e) ist mit diesem Abschnitt erfüllt.** Beide gehen auf `pilot`.

## 9. Bündel 6 – die vier Onboarding-Dokumente

| Träger | (a) vollständig | (c) offene `VERIFY`-Marker | (d) offene `<TBD…>` |
|---|---|---|---|
| `onboarding/COMPLETION_CRITERIA.md` | ja – Pflichtkriterien, ergänzende Kriterien, Freigabe | keiner | keiner |
| `onboarding/GUIDE.md` | ja – Lernziele, Voraussetzungen, Programmüberblick, neun Module, Abschlusscheck, Nachschlagewerk | keiner | **einer, unkritisch:** Z27 `<TBD: Referenz>` – die Datenschutzunterweisung **der Organisation**. **Dieselbe Marke steht in `checklists/09-onboarding.md`** und ist dort mit 0.51.0 aus demselben Grund als unkritisch abgenommen worden |
| `onboarding/KNOWLEDGE_CHECK.md` | ja – Fragen und Lösungsteil, mit der ausdrücklichen Zusicherung, dass es keine Personalbeurteilung ist | keiner | keiner |
| `onboarding/MENTOR_CHECKLIST.md` | ja – vor dem Start, während der Module, rote Flaggen, Freigabe | keiner | keiner |

**(e) ist mit diesem Abschnitt erfüllt.** Alle vier gehen auf `pilot`.

## 10. Bündel 7 – die zwei Pilot-Dokumente

| Träger | (a) vollständig | (c) offene `VERIFY`-Marker | (d) offene `<TBD…>` |
|---|---|---|---|
| `pilot/METRICS.md` | ja – Erhebungsgrundsätze, vier Metrikgruppen, Auswertung | keiner | **einer, unkritisch:** Z10 `<TBD: Zielwerte je Metrik>`. **Der Träger sagt in derselben Zeile, dass das Absicht ist:** *„Zielwerte werden ausdrücklich **nicht** durch das Framework vorgegeben; sie sind projektspezifisch festzulegen"* |
| `pilot/PILOT_CONCEPT.md` | ja – Ziel und Grundsätze, Aufbau, Abbruchkriterien, Entscheidung am Pilotende | keiner | **sechs, alle unkritisch:** Z21 Referenzzeitraum, Z22 Anzahl der Pilotgruppe, Z27 Takt der Review-Punkte, dazu drei bloße `<TBD>` in der Spalte *Projektwert* (Z22, Z27, Z28). **Die Abschnittsüberschrift benennt es selbst:** *„2. Aufbau (normativ, Parameter projektspezifisch)"* – normativ ist der Aufbau, die Parameter gehören dem Projekt |

**(e) ist mit diesem Abschnitt erfüllt.** Beide gehen auf `pilot`.

## 11. Bündel 8 – die drei Client-Pack-Dokumente, und einer bleibt

**Diese Gattung trägt zusammen zehn Markerfundstellen (8 + 1 + 1)** – der größte Posten von
Kriterium 1 außerhalb des `root-template/`. **Marker sperren den Übergang nicht** (Punkt 3
(c)), sind aber je Träger zu benennen.

| Träger | (a) vollständig | (c) offene `VERIFY`-Marker | (d) offene `<TBD…>` | Abnahme |
|---|---|---|---|---|
| `clients/README.md` | ja – Zweck, Abgrenzung zur Regelebene, Bestandteile, Fähigkeitsmatrix, Erstellung eines Packs, verfügbare Packs, Änderungsverlauf | **einer, und er ist eine Nennung:** Z67 erklärt, dass eine `[TECHNISCH]`-Zeile bis zum Beleg den Marker trägt. Einer der vier nennenden Träger | keiner | **ja** |
| `clients/claude-code/CLIENT_PACK.md` | ja – Pfad- und Semantikabbildung, Fähigkeitsmatrix über sieben Klassen, Durchsetzungstiefe, Kernzusagen ohne Durchsetzung, bekannte Abweichungen, Installation, Anweisungsquellen außerhalb des Projekts, Änderungsverlauf | **einer, echt:** Z89 (R5) – ein **technischer** Aufzählungsweg der geladenen Regelquellen ist nicht belegt; die Selbstauskunft der Sitzung ist Modellverhalten, kein Mechanismus. **Benannt, sperrt nicht** | keiner – beide Steckbriefzellen tragen echte Werte (`2.1.267`, `2026-09-10`) | **ja** (Abschnitt 3.2) |
| `clients/devin-desktop/CLIENT_PACK.md` | ja – derselbe Aufbau | **acht, alle echt:** Z24 (Schemadetails der Berechtigungskonfiguration), Z26 (Struktur der MCP-Konfiguration), Z27 (`DEVIN_PROJECT_DIR`), Z82 (S3), Z94 (B3), Z101 (B10), Z116 (A1), Z138 (X2, `K-20`). **Benannt, sperren nicht** | **zwei, und beide sperren:** Z11 `<TBD: verbindliche Zielversion; Roadmap AP2>`, Z12 `<TBD: steht aus>`. Keiner bezeichnet einen Wert der aufnehmenden Organisation | **nein** – bleibt auf `entwurf` (D-110, Abschnitt 3.1) |

**(e) ist mit diesem Abschnitt erfüllt** – auch für den Träger, der nicht abgenommen ist:
Die Begründung steht namentlich.

## 12. Bündel 9 – die zwei Role-Pack-Dokumente

| Träger | (a) vollständig | (c) offene `VERIFY`-Marker | (d) offene `<TBD…>` |
|---|---|---|---|
| `framework/role-packs/requirements-engineering/ROLE_PACK.md` | ja – zehn Abschnitte von Zweck und Abgrenzung über EARS-Syntax und Nachvollziehbarkeit bis Aktivierung und Änderungsverlauf | keiner | keiner |
| `framework/role-packs/software-development/ROLE_PACK.md` | ja – acht nummerierte Abschnitte in neun Überschriften (5b *Aktivierung im Projekt* ist eingeschoben), Referenzpack der Erstfassung | keiner | keiner |

> **Der Statuswert des zweiten trägt einen Zusatz:** `entwurf (Referenzpack der
> Erstfassung)` wird zu `pilot (Referenzpack der Erstfassung)`. Der Zusatz beschreibt die
> Rolle des Packs, nicht seinen Status, und bleibt. **Prüfung 46 und Prüfung 47 vergleichen
> das erste Wort des Werts** – genau für diesen Fall (E6 von `CR-2026-070`).

**(e) ist mit diesem Abschnitt erfüllt.** Beide gehen auf `pilot`.

## 13. Was diese Gegenprüfung ausdrücklich nicht behauptet

`01-governance.md` Abschnitt 5 Punkt 4 gilt hier wörtlich: **Ein Träger auf `pilot` ist
strukturell abgenommen, nicht erprobt.** Kein Sitzungstest ist gefahren; ob ein KI-Client
diesen vierzig Trägern folgt, sagt allein Kriterium 2, und das steht unverändert auf 118.

**Und sie behauptet nicht, dass Kriterium 3 damit erledigt ist.** Es steht auf 1, und der
Rest hängt an `AP2` – an einer Messung gegen ein Produkt, nicht an einem Review.

## 14. `K-39` – ist `docs/ROADMAP.md` ein Modulträger?

**Aufgefallen bei der Abnahme, nicht gesucht.** Drei Beobachtungen an demselben Träger:

1. Sie wird **in jedem Release** fortgeschrieben – zuletzt in diesem, durch diesen Vorgang.
2. Ihre Steckbriefversion steht seit `0.2.0` unverändert, während der Inhalt fünfzig
   Releases weitergelaufen ist. **Der Versionsprüfpunkt von `FW-CL-11` hat sie nie
   getroffen**, und niemandem ist es aufgefallen.
3. **`CHANGELOG.md` hat dieselbe Eigenschaft und ist vom Zählbereich der Prüfung 46
   ausdrücklich ausgenommen** – als *„datierte, abgeschlossene Aufzeichnung"*, gemeinsam mit
   `governance/change-requests/` und `tests/protocols/`.

**Beide Antworten haben einen Preis, und keiner ist klein:**

| Antwort | Preis |
|---|---|
| Ja, sie ist ein Modulträger (heutiger Stand) | Ein Dokument, dessen Inhalt sich mit jedem Release ändert, führt eine Version, die niemand pflegt, und einen Status, der nichts über es aussagt |
| Nein, sie gehört wie `CHANGELOG.md` heraus | **Der Zählbereich schrumpft, und eine Zahl sinkt, ohne dass jemand etwas abgenommen hat.** Das ist die Bewegung, die `CR-2026-070` E6 verworfen hat – auch wenn sie hier sachlich begründbar wäre |

**In diesem Release nicht entschieden.** Der Klärungspunkt ist angelegt; die Abnahme steht
unabhängig davon, weil sie die Bedingung erfüllt.

## 15. Bewertung

| Frage | Antwort |
|---|---|
| Sind alle einundvierzig Träger je einzeln geprüft? | **Ja**, namentlich, in neun Bündeln nach Gattung, mit (a) bis (d) je Träger |
| Wie viele sind abgenommen? | **Vierzig.** Kriterium 3: **41 → 1** |
| Warum nicht alle? | `clients/devin-desktop/CLIENT_PACK.md` lässt zwei Aussagen des Frameworks offen und sagt das selbst. Er geht über `AP2`, nicht über eine Abnahme |
| Wie viele Ermessensfragen sind angefallen? | **Drei** – die Trennung von Schlitz und Nennung (D-109), der gesperrte Träger und seine Abgrenzung zum Schwesterpack (D-110), die Vollständigkeit eines Registers mit offenen Ergebnissen (D-111) |
| Und ein Klärungspunkt? | **`K-39`** – ob `docs/ROADMAP.md` überhaupt ein Modulträger ist |
| War die Aufgabenbeschreibung groß genug? | **Zum neunten Mal in Folge nicht.** Sie lautete „die restlichen 41 Träger heben"; angefallen sind ein Träger, der sich selbst sperrt, drei Ermessensfragen und ein Klärungspunkt |
