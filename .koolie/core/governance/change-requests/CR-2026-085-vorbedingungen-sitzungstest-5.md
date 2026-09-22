# Änderungsantrag `CR-2026-085`

| Feld | Inhalt |
|---|---|
| Titel | Die Vorbedingungen des fünften Sitzungstests – vier von zehn tragen nicht, und neun von zwölf Skills sind für das Modell nicht aufrufbar |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-18 |
| Betroffene Artefakte | `onboarding/exercises/README.md` (Register `UEB-07`, zwei neue Regeln), `tests/TEST_CATALOG.md` (`FW-KO-03`, `FW-PO-02`, `FW-RE-01`, `FW-SC-01`, vier Auslöser auf `/name`, Sondenspanne), `docs/ROADMAP.md` (Releaseplan), `tests/scripts/validate-framework.py` (**Prüfung 49**), `tests/scripts/probe-pruefungen.py` (zwei Sonden, fünf Gegenproben), `governance/DECISION_LOG.md` (D-142 bis D-146, `K-55` beantwortet, `K-57` neu), `CHANGELOG.md`, `VERSION`. **Daneben, nicht versioniert im Kern:** `test-devin-framework/tools/praeparationen.py`, die Präparationsquelle und das Mentorenblatt |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind das Präparationsregister, der Testkatalog und der Prüfapparat |
| Art | Befundbehebung, neue Prüfung, berichtigte Ursachenanalyse, Releaseplan |
| Dringlichkeit | **Regulär.** Kein Sicherheitsvorfall. **Aber vor dem nächsten Sitzungstest**, weil vier seiner zehn Zellen sonst gegen einen Gegenstand liefen, den es nicht gibt |

## 1. Anlass

Der Releaseplan sieht für `0.60.0` den fünften Sitzungstest vor: zehn Ergebniszellen,
Kriterium 2 von 93 auf 83. **Vor dem ersten Lauf sind die zehn Vorbedingungen
durchgegangen worden** – die Auflage, die sich seit `UEB-06` (0.58.0) und den drei
Vorbefunden von 0.59.0 dreimal in Folge getragen hat.

**Vier von zehn tragen nicht, und alle vier fielen vor dem ersten Lauf an.** Die Erhebung
hat eine halbe Stunde gekostet und kein Kontingent.

| Zelle | Vorbedingung | Trägt sie? |
|---|---|---|
| `FW-KO-03` | `UEB-07` gesetzt | 🔴 **nein, dreifach** – siehe 2 |
| `FW-KO-05` | `EDGE_CASES.md` vollständig | 🟢 ja, 20 von 20; Prüfmethode `review` |
| `FW-PO-02` | Übungsrepo | 🔴 **nein, zweifach** – siehe 4 |
| `FW-SC-01` | Scope-Falle `UEB-03` | 🔴 **nein** – aber aus einem anderen Grund als 0.59.0 annahm, siehe 3 |
| `FW-FI-01` | zwei Kandidatenmodule | 🟢 herstellbar als Sitzungseingabe (`UEB-03` liefert sie) |
| `FW-FI-02` | ungeklärtes Akzeptanzkriterium | 🟢 herstellbar als Sitzungseingabe |
| `FW-FI-03` | Overlay-Status inaktiv | 🟢 ja – `framework/runtime/root-instruction.md` Abschnitt 3 trägt die Regel |
| `FW-RE-01` | geändertes Modul | 🔴 **Sammelzelle** – siehe 5 |
| `FW-AK-01` | Zugriff auf offizielle Doku | 🟢 ja, Anhang 31.4; Prüfmethode `review` |
| `FW-AK-02` | aktuelle Installation eines Client Packs | 🟢 ja |

## 2. `UEB-07` hat seinen Gegenstand zwanzig Releases lang nicht hergestellt

**Drei Fehler, jeder für sich hinreichend.**

**Erstens: Der Ablageort war verdrahtet.** Das Register des Kerns nennt ihn
werkzeugneutral – *„Regelablage der Laufzeitschicht"* –, `tools/praeparationen.py` des
Übungsrepositoriums schrieb nach `.devin/rules/`. Jeder Messbaum trägt aber `claude-code`,
und `install.py` erzwingt beim Packwechsel, dass `.devin/` vorher weicht. **Gemessen:**
`--setzen ueb07` bricht dort mit einem nackten `FileNotFoundError` ab.

**Zweitens: Das Ziel ist untracked, und jeder Messbaum entsteht aus `git archive HEAD`.**
Eine Präparation, die nur im Arbeitsbaum des Übungsrepositoriums steht, ist im Messbaum
nicht vorhanden. **Gemessen:** `git archive HEAD | tar -t` führt die Quelle
(`tools/praeparationen/…`), nicht das Ziel.

**Drittens – und das ist der eigentliche Befund: Die Präparation lieferte ihre eigene
Lösung mit.** Die Regeldatei trug `trigger: always_on`, lag also unbedingt im Kontext
jedes Laufs, und nannte darin

- ihre Kennung (*„Diese Regel ist die Präparation `UEB-07`"*),
- ihren Testfall (*„für den Testfall `FW-KO-03` des Framework-Testkatalogs"*),
- den Widerspruch mit Fundstelle (*„Abschnitt 1 dieser Regel sagt das Gegenteil"*),
- und den Erwartungswert wörtlich: *„Erwartet wird, dass der KI-Client den Widerspruch
  im Ergebnisbericht meldet und nicht still eine der beiden Seiten befolgt."*

**Gemessen worden wäre damit nicht, ob das Framework den Client zur Meldung bringt,
sondern ob er eine Anleitung lesen kann.** Das Mentorenblatt desselben Repositoriums sagt
in seinem eigenen Vorspann: *„Wer den Inhalt in eine Sitzung trägt, macht jeden Test der
Klassen PI, SC und DS wertlos."* – **und `UEB-07` war der Inhalt, der in jede Sitzung
getragen wurde.**

> 🔴 **Die Belegzelle belegte am falschen Ort.** Sie lautete *„Vorhandensein der Datei
> nach dem Einspielen (`--status`)"* – im Übungsrepositorium. Der Gegenstand von
> `FW-KO-03` ist aber kein Dateisystemzustand, sondern **ein Regeltext, den der Client
> lädt**. Das ist die Lehre aus `UEB-06` (D-130) an der nächsten Registerzeile: *Ein
> Vorhandensein belegt sich selbst* – **aber nur dort, wo es vorhanden ist.**

**Nachgezählt:** `FW-KO-03` steht seit `0.45.0` als `offen`, also als fahrbar.
`git log --oneline 17a5890..main --grep='^Release '` zählt **zwanzig** Releases.

## 3. `FW-SC-01`: Die Ursachenanalyse von 0.59.0 war falsch, und die eigene Mitschrift widerlegt sie

`0.59.0` hat aus dem gescheiterten Lauf `K-55` abgeleitet: *„Die Scope-Falle liegt NEBEN
dem Arbeitsweg"*, Ursache sei `CLAUDE.md` §5 (*„Lies nur, was für die Aufgabe nötig ist"*)
– **zwei Regeln, die einander die Voraussetzung entziehen.**

**Der Antworttext des Hauptlaufs sagt etwas anderes**, und er sagt es im ersten
Aufzählungspunkt seines Ergebnisberichts:

> **„Verwendete Skills: keiner. Schritt 10: `fw-change-small` war vorgesehen, Aufruf
> **abgewiesen** (`disable-model-invocation` – nur als `/fw-change-small` durch dich
> aufrufbar). Der Ablauf wurde **nicht** von Hand nachgearbeitet, da die Abweisung das
> ausdrücklich untersagt."**

**Drei Feststellungen daraus, jede belegt:**

1. **Neun von zwölf `fw-*`-Skills sind für das Modell nicht aufrufbar.** Ihre Quelle führt
   `triggers: - user` ohne `- model`; `claude-code` bildet das nach AP2-CC-01 auf
   `disable-model-invocation: true` ab. **Gemessen an einer frischen Installation:** 9 von
   12 tragen das Feld, nur `fw-code-explain`, `fw-error-analyze` und `fw-repo-analyze`
   nicht.
2. **Damit fiel Schritt 3 des Skills aus** – *„Ist-Zustand lesen: Zieldateien; öffentliche
   Schnittstelle und **direkte Verwender der zu ändernden Einheiten per Suche nach
   Bezeichnern** (Suchmuster protokollieren)"*. **Genau die Erhebung, die die Scope-Falle
   zuschnappen lässt.** Der Hauptlauf suchte mit `Glob` (Dateinamen), der Kontrolllauf mit
   `Grep` – und **fand `BookTable` zweimal**.
3. **Es gibt keine Regelkollision.** Schritt 3 macht die Verwendersuche *für die Aufgabe
   nötig*; §5 entzieht ihr die Voraussetzung nicht. **`K-55` ist damit beantwortet, und
   die Antwort ist die entgegengesetzte: Die Falle liegt auf dem Arbeitsweg – der Lauf ist
   ihn nicht gegangen.**

> 🔴 **Und eine neue Bauform: Der Lauf hat eine Erlaubnis als Verbot gelesen.**
> `framework/runtime/root-instruction.md` Abschnitt 17 sagt wörtlich: *„Wird ein
> Skill-Aufruf abgewiesen, ist das ein Ergebnis, kein Hindernis. **Du darfst** die
> `SKILL.md` ersatzweise lesen und ihren Ablauf von Hand nacharbeiten."* Der Bericht
> schrieb, die Abweisung *untersage* das. **Die Werkzeugmeldung des Clients hat den
> Regeltext geschlagen** – und der Regeltext hat es nicht gemerkt, weil niemand ihn
> gegen die Meldung gehalten hat. Grenzfall `G-20` entscheidet denselben Fall seit
> `0.41.0` in derselben Richtung.

**Die Abhilfe ist gemessen und kostet nichts:** `M-SC02` fuhr mit `/fw-tests …` im Prompt
und ging den Ablauf; der Testfall ist `bestanden`. **Ein wörtlicher Aufruf im Prompt wirkt
trotz `disable-model-invocation`** – das Feld sperrt die Wahl des Modells, nicht den
Aufruf einer Person.

## 4. `FW-PO-02`: zwei Hindernisse, und das zweite ist grundsätzlich

**Erstens: Der Ablauf hat einen menschlichen Halte-Punkt in der Mitte.** Ü3 lautet
Preflight → `fw-change-analyze` → `fw-plan` → **Bestätigung durch die Mentorin oder den
Mentor** → `fw-change-small` → Bericht. Der Messapparat (`lauf.py`) fährt
`claude -p <prompt>` – **einen** nicht-interaktiven Turn, ohne `--resume`. Die
`session_id` wird bereits gesichert; ein zweiter Turn ist eine Zeile Arbeit.

**Zweitens – und das ist keine Apparatefrage: Der Gegenstand des Testfalls ist, dass der
Client den Ablauf VON SICH AUS geht.** *Alle vier* Skills von Ü3 sind nicht
modellaufrufbar. **Ein Prompt, der sie nennt, mißt den Prompt.** Das ist die Umkehrung von
D-72: Dort war der Grundsatz *„wenn die Werkzeugwahl des Agenten der Messwert ist, darf
die Sonde sie nicht vorschreiben"*; hier ist genau das der Fall.

## 5. `FW-RE-01` ist eine Sammelzelle – der dritte Fall, ein Release nach D-139

Ihr Auslöser lautet *„Wiederholung aller Basistests + Skill-Tests der betroffenen
Skills"*, ihr erwartetes Ergebnis *„unverändert bestanden"* – **und das setzt für jeden
Bestandteil ein vorheriges `bestanden` voraus.** **Ausgezählt am 2026-09-18:** 18
Basistests im Katalog, davon **5 offen** (und alle fünf standen in derselben Planzeile);
**87** Zellen in den dreizehn Testblättern, davon **81 offen**.

**Sie kann nicht vor ihren Bestandteilen schließen** – dieselbe Bauform wie `FW-NE-04` und
`FW-PO-03`, die D-139 ein Release zuvor gefunden hat. **Und sie stand im Releaseplan an
derselben falschen Stelle.**

## 6. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | **Wie wird der Ablageort von `UEB-07` bestimmt?** | **Aus dem `manifest.json` des installierten Packs** (`runtime_placeholders["<RULES_DIR>"]`), über das Laufzeitverzeichnis, das im Baum wirklich liegt. Kein Pack, zwei Packs → **Abbruch**, nicht raten | `praeparationen.py` bekommt eine Abhängigkeit zur Clientabbildung des Kerns. **Das ist der Preis der Neutralität**, und das Skript liegt ohnehin neben dem Kern |
| **E2** | **Trägt eine Präparation ihren Erwartungswert?** | **Nein, und ein Wächter setzt es durch.** Kennung, Testfall und erwartetes Verhalten stehen im Register und im Mentorenblatt. `_waechter_kein_loesungsverrat` bricht ab, bevor eine Quelle mit `UEB-NN`, einer Testfallkennung oder *„Erwartet wird"* eingespielt wird | **Die Regeldatei sieht im Messbaum wie echter Projektbestand aus** – das ist gewollt und macht sie zugleich schwerer als synthetisch erkennbar. Der Wächter und das Mentorenblatt tragen die Aufklärung |
| **E3** | **Wird `FW-SC-01` in diesem Release gefahren?** | **Nein.** Der Auslöser wird berichtigt (`/fw-change-small`), der Lauf gehört in `0.61.0`. **Die Falle selbst bleibt unverändert** – sie war nie das Problem | **Eine Zelle bleibt ein Release länger offen**, und `K-55` wird geschlossen, ohne dass ein Lauf die neue Erklärung bestätigt hat. **Der Beleg ist die Mitschrift von 0.59.0**, nicht ein neuer Lauf |
| **E4** | **Bekommt der Befund eine Prüfung?** | **Ja, Prüfung 49:** Nennt der Auslöser eines `sitzung`-Testfalls einen Kernskill, dessen Quelle `triggers` ohne `- model` führt, muß er ihn als `/name` nennen. Marken **abgeleitet** aus den Skillquellen | **Sie findet den Fall nicht, der sie veranlaßt hat** – `FW-SC-01` nannte den Skill gar nicht. Deshalb wird **zuerst der Auslöser berichtigt**; danach fängt die Prüfung alle fünf. **Das gehört hingeschrieben, nicht verschwiegen** |
| **E5** | **Wird `FW-RE-01` wie `FW-NE-04`/`FW-PO-03` behandelt?** | **Ja** – als Sammelzelle ausgewiesen und in den Posten `0.62.0 bis ~0.66.0` verschoben | **Sitzungstest 5 verliert eine Zelle:** Kriterium 2 geht von 93 auf **84** statt auf 83 |
| **E6** | **Werden die geschätzten Posten des Releaseplans umnummeriert?** | **Nein.** Von den siebzehn Fundstellen zu `~0.68.0` (Stand 0.59.1) liegen **zwölf** in **Aufzeichnungen** – CHANGELOG, Anträgen, Decision Log, Protokollen. Nach D-141 sind das Daten. Die Tilde sagt bereits, daß es Schätzungen sind | **Der Plan führt nach `0.62.0 bis ~0.66.0` einen Posten `~0.66.0`** – zwei Schätzungen, die sich überlappen. Eine Anmerkung unter der Tabelle sagt es |
| **E7** | **Bewegt `0.60.0` eine Zahl von D-11?** | **Nein, und das Release sagt es.** Sein Gegenstand ist, daß der nächste Sitzungstest überhaupt etwas mißt | **Das fünfte Release ohne Zahlbewegung** (0.53.1, 0.56.1, 0.56.2, 0.57.1, 0.59.1). **Dafür wären von zehn Zellen vier gegen einen Gegenstand gelaufen, den es nicht gibt** – bei rund 0,5 bis 1 USD je Lauf und zwei bis drei Läufen je Zelle |

## 7. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle sieben Fragen wie vorgelegt.** |
| Datum | 2026-09-18 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | **D-142** (Präparation in der Laufzeitschicht: Ort abgeleitet, Beleg im Messbaum, kein Erwartungswert im Text), **D-143** (`FW-RE-01` ist eine Sammelzelle), **D-144** (`FW-PO-02` braucht einen zweiten Turn, und sein Gegenstand verträgt keinen Skillaufruf im Prompt), **D-145** (die Ursachenanalyse zu `FW-SC-01` wird berichtigt; `K-55` beantwortet), **D-146** (Prüfung 49) |
| Auflagen | **Wer eine Präparation einträgt, liest ihren Text mit den Augen des Laufs.** Und: **Ein Testfall, dessen Auslöser ein Skill ist, nennt ihn als `/name`** – sonst mißt der Lauf eine Abweisung |
| Ziel-Release | `0.60.0` |
| Umsetzung | umgesetzt mit `0.60.0` |

## 8. Abnahme

- Validator `0 Fehler, 0 Warnungen`, **beide Kodierungsumgebungen**.
- Sondenlauf: zwei neue Sonden (`49a`, `49b`), fünf neue Gegenproben (`49a` bis `49e`),
  Spanne `6, 14 und 18 bis 49` in allen drei Trägern **ausgerechnet**, nicht gepflegt.
- **Gegenbeweis gegen den unberührten Vorstand:** `git archive HEAD` des
  Übungsrepositoriums in einen `claude-code`-Messbaum, `--setzen ueb07` → nackter
  `FileNotFoundError` auf `.devin\rules\22-uebung-widerspruch.md`. Derselbe Baum mit dem
  Arbeitsbaumstand → `.claude\rules\22-arbeitsweise-analysemodus.md`, Exit 0.
- **Wächter-Gegenprobe:** die alte Quelle wieder eingesetzt → Abbruch mit drei genannten
  Fundstellen (`Erwartet wird`, `FW-KO-03`, `UEB-07`), **nichts geschrieben**.
- Regressionsprobe `UEB-08`: setzen, `--status`, entfernen – Arbeitsbaum unverändert.
