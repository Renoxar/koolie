# Änderungsantrag `CR-2026-116`

| Feld | Inhalt |
|---|---|
| Titel | Der Meßtag von Bündel 5 – das Testblatt des Role Packs `requirements-engineering` |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-22 |
| Betroffene Artefakte | `tests/erhebungen/umgebungen-bauen-b5.py`, `baeume-b5.py`, `prompts-schreiben-b5.py`, `reihe-b5.py`, `stand-b5.py`, `zustand-b5.py`, `trust-b5.py`, `auswerten-b5.py`, `dossier-b5.py` (alle neu), `tests/erhebungen/k-bauen-b3.py` (Nachträge Bündel 5), `tests/erhebungen/README.md`, `framework/role-packs/requirements-engineering/skills/role-re-ticket/TESTS.md` (fünfzehn Ergebniszellen), `governance/DECISION_LOG.md`, `tests/protocols/2026-09-22-messtag-buendel-5.md` (neu), `docs/ROADMAP.md`, `CHANGELOG.md`, `VERSION`, `UEBERGABE.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind der Meßapparat und fünfzehn Ergebniszellen des Testkatalogs |
| Art | **Messung mit Kontingent** – gerechnet rund 30 Läufe und 30 bis 37 USD |
| Dringlichkeit | **Regulär**; der Wiederaufnahmepunkt von `0.82.0` nennt ihn als nächsten Posten |

## 1. Anlass

`CR-2026-114` hat die Vorbedingungen von Bündel 5 gemessen, `CR-2026-115` hat es
hergerichtet. **Alle fünfzehn Zellen von `RE-001` sind fahrbar:** Der Meßbaum trägt den
Skill, seine Rollenregel und den Korbeintrag (D-237, D-238), der Kontrollzuschnitt
`ohnepack` ist entschieden (D-242), `UEB-30` und `UEB-31` sind gebaut (D-245, D-246).

**Was fehlt, ist der Apparat.** `baeume-b4.py` und `umgebungen-bauen-b4.py` tragen die
**Mechanik** – Packaktivierung, `ohnepack`, abgeleitete Skillmenge, abgeleiteter Wächter,
alles mit `0.82.0` gemessen. Ihre **Zuordnung**, ihre Pflicht- und Verbotsliste der
Präparationen und ihr Zielpfad `C:\lw-b4` gehören Bündel 4.

> *Die Mechanik ist geerbt und gemessen. Der Zuschnitt ist es nicht – und ein Verzeichnis
> ist kein Zuschnitt, es ist der Zuschnitt von gestern (D-230).*

## 2. Der Gegenstand: fünfzehn Zellen, ein Skill außerhalb des Kerns

`RE-001-P01` bis `P05` und `N01` bis `N10`, Prüfmethode `sitzung`, Blatt
`framework/role-packs/requirements-engineering/skills/role-re-ticket/TESTS.md`.
**Keine einzige ist je abgenommen worden**, und `K-84` hat hier deshalb keinen Biß.

Es ist das **größte Einzelblatt** des Katalogs und das **einzige außerhalb des Kerns**.
Kriterium 2 geht bei vollständiger Abnahme von **19 auf 4**.

## 3. Vorlage zur Entscheidung

### E1 – Welcher Kontrollzuschnitt je Zelle? (die teuerste Frage dieses Antrags)

`K-87` hat `ohnepack` als Zuschnitt **hergestellt**; er beantwortet aber nicht, für
**welche** Zelle er der richtige ist. Ein Kontrollauf fragt nach der **Zurechnung**
(D-115, D-175, D-236): Ist das beobachtete Verhalten dem Gegenstand zuzuschreiben, dem
die Zelle es zuschreibt? Daraus folgt die Trennlinie:

- Steht die geprüfte Schranke **allein im Pack**, ist `ohnepack` der Zuschnitt: Er
  entfernt sie vollständig.
- Steht sie **auch in der Kernregelschicht**, läßt `ohnepack` sie stehen. Der
  Kontrollauf wäre dann **per Konstruktion** unauffällig – *die Null durch Konstruktion*
  (0.59.1) am Kontrollzuschnitt. Dann gehört die **bedeutungsgeschnittene** Klasse
  hierher, die die Schranke in **allen** Schichten entfernt (D-205) – auch in der
  `SKILL.md` und der Rollenregel, denn `k-bauen-b3.py` führt `.claude/skills` und
  `leitwerk-core/framework` in seinen `BEREICHE`n.

**Gemessen, nicht geschätzt** (Fundstellen im Kern gegen Fundstellen im Pack, über
`framework/core`, `framework/skills`, `checklists/`, `decision-trees/`, `templates/`):

| Gegenstand der Zelle | Kern | Pack `re` | Urteil |
|---|---|---|---|
| EARS, `shall` (`P01`) | **0** | 82 | packeigen |
| *„Der Ist-Zustand ist keine Anforderung"* (`P02`) | **0** | 5 Träger | packeigen |
| *„Randbedingung (belegt)"* (`P03`) | **0** | 6 Träger | packeigen |
| Umfangstreue der Überarbeitung (`P05`) | **0** | 6 | packeigen |
| Priorität, Aufwand, Story Points (`N02`) | **0** | 4 | packeigen |
| unbestimmte Wörter (`N06`) | **0** | 9 | packeigen |
| Abnahmekriterien (`N07`) | **0** | 29 | packeigen |
| Widerspruch zur belegten Randbedingung (`N08`) | 1 (fremdes Testblatt) | 2 | packeigen |
| **Prompt Injection, `S6` (`N10`)** | **120** in 45 Trägern | 6 | **beide Schichten** |
| **Datenschutz, `K3` (`N05`)** | **366** in 60 Trägern | 12 | **beide Schichten** |
| **Fernwirkung, `V11`, `M1` (`N03`)** | **203** in 45 Trägern | 31 | **beide Schichten** |
| **No Assumption, Rückfrage, `P3` (`N01`, `N09`)** | **329** in 45 Trägern | 41 | **beide Schichten** |
| **`V3`, Architekturentscheidung (`N04`)** | **21 Träger** | 12 | **beide Schichten** |

➡️ **Aufgelöst:** `ohnepack` für neun Zellen, `inj` für `N10`, `k3` für `N05`, `fern`
für `N03`, `n03` für `N01` und `N09`, **`sc1` für `N04`**.

⚠️ **Die Abweichung ist benannt:** Der Wiederaufnahmepunkt von `0.82.0` nennt vier
bedeutungsgeschnittene Klassen (`inj`, `k3`, `fern`, `n03`). Gemessen sind es **fünf**:
`V3` steht in **21 Trägern des Kerns**, und keine der vier Klassen schneidet ihn –
`fern` führt `Delegationsverbot\w*`, nicht `\bV3\b`. Mit `ohnepack` bliebe für `N04`
genau die geprüfte Schranke stehen.

⚠️ **Preis von `sc1`, benannt:** Die Klasse schneidet über `V3` hinaus die Scope-Treue
und die Nur-Lese-Pfade, die `RE-001-N04` nicht meint. Ein breiterer Zuschnitt schwächt
die Aussage des Kontrollaufs, macht sie aber nicht falsch – die Alternative wäre eine
neue Klasse mit eigenem Stammuster, und die hat vor einem Meßtag niemand gemessen.

### E2 – Braucht Bündel 5 Übungs-Branches und `node_modules`?

`historie-bauen-b4.py` existiert, weil **zwölf der neunzehn Zellen von Bündel 4** ihren
Skill mit `<DEFAULT_BRANCH>` aufrufen und einen Diff verlangen (D-206). **Keine der
fünfzehn Zellen von `RE-001` nennt einen Branch, einen Diff oder einen Testbefehl:**
`role-re-ticket` ist **M1, rein lesend**, sein Prüfmittel ist `validate-output.py`.

➡️ **Aufgelöst:** **keine** Übungs-Branches, **kein** `node_modules`. Jeder Baum bekommt
die **minimale Historie** (`git init`, ein Commit, synthetischer Autor), die
`baeume-b4.py` für die sechs Zellen von `fw-docs-update` schon führt – damit `git status`
im Baum leer ist und kein Lauf einen Fund zeigt, den keine Zelle meint.

⚠️ **Preis, benannt:** Ohne die Verzeichnisverbindung ist `npm test` im Meßbaum nicht
fahrbar. Das ist folgenlos, weil **keine Zelle dieses Blattes einen Testbefehl nennt**;
der Gewinn ist, daß die Löschfalle von `0.74.1` (ein rekursives Löschen, das der
Verbindung folgt) in dieser Erhebung gar nicht erst entstehen kann.

### E3 – Bleibt `Edit(**)` im Rückfragekorb?

`umgebungen-bauen-b4.py` nimmt `Edit(**)` **aus** dem `ask`-Korb und gibt
`Edit(frontend/src/**)` und `Edit(docs/**)` frei – weil `fw-docs-update` **schreibt** und
sechs Zellen sonst den Korb statt den Skill messen (D-178).

`role-re-ticket` trägt `deny` auf `edit` und `exec`, und **`RE-001-N03` mißt genau das**:
daß der Lauf nichts einträgt. Ein freigegebener Schreibkorb nähme dieser Zelle ihren
Gegenstand nicht, aber er wäre eine Abweichung ohne Anlaß.

➡️ **Aufgelöst:** Der Korb bleibt **unverändert**, wie `install.py` ihn erzeugt und
`cc-overlay-fuellen.py` ihn füllt. Kein Schreibkorb, keine Befehlsschlitze.
**Die Abweichungsliste dieses Bündels ist leer** – und das ist der erste Meßaufbau seit
Bündel 2, für den das gilt.

### E4 – Wo werden `UEB-30` und `UEB-31` gesetzt?

Beide sind **je Meßbaum** herzustellen (`TESTS.md`, `CR-2026-115`). `UEB-30` nimmt die
Wertzelle von `<ISSUE_TRACKER>` auf *nicht festgelegt* zurück – und **`RE-001-P04`
verlangt denselben Platzhalter mit Wert** (D-240: zwei Zellen, ein Platzhalter,
entgegengesetztes Vorzeichen).

➡️ **Aufgelöst:** `UEB-30` nur in `re001n09` und `kre001n09`, `UEB-31` nur in `re001n10`
und `kre001n10`, jeweils **vor** `git init` und dem ersten Commit – eine Präparation, die
danach käme, stünde in `git status`. Ein **Verbotswächter** im Basisbaum prüft, daß
keine von beiden dort liegt; ohne ihn trügen sie **alle dreißig** Bäume, und `RE-001-P04`
wäre in keinem einzigen fahrbar.

### E5 – Wie lauten die Prompts von `P04` und `N09`?

Beide Zellen rufen den Skill **ohne Formatangabe** auf und unterscheiden sich allein im
Zustand von `<ISSUE_TRACKER>`.

➡️ **Aufgelöst:** Beide bekommen **denselben Prompt, wörtlich**. Verschieden ist der
**Baum**, nicht die Eingabe – dieselbe Trennlinie, die Haupt- und Kontrollprompt schon
trägt. *Wer den Prompt ändert, mißt den Prompt.*

## 4. Umsetzung

1. **`umgebungen-bauen-b5.py`** – Basisbaum `C:\lw-b5\basis`: archivieren, Vorbedingungen
   prüfen, Packwechsel, `install.py`, Overlay füllen, **Pack aktivieren** (abgeleitet aus
   dem Zuschnitt), Wächter über Skills und Korbeinträge, Verbotswächter, **Prüfmittel
   einmal im Meßbaum fahren** (Lehre aus `0.68.0`).
2. **`baeume-b5.py`** – `ZUORDNUNG` je Zelle nach E1, sechs Klassenbasen, minimale
   Historie je Baum, Präparationen nach E4.
3. **`prompts-schreiben-b5.py`** – fünfzehn Prompts, Haupt- und Kontrollprompt wörtlich
   gleich, Verrat-Wächter (kein Prompt nennt eine Kennung oder einen Erwartungswert).
4. **`k-bauen-b3.py`** – die Nachträge, die der Stammwächter an den Packträgern meldet.
5. **`reihe-b5.py`, `stand-b5.py`, `zustand-b5.py`, `trust-b5.py`** – aus den
   `-b4`-Fassungen, geändert ausschließlich `C:\lw-b4` → `C:\lw-b5`.
6. **`auswerten-b5.py`** – Paare, **Berührungsmarken je Zelle gegen den Baum ihrer Zelle
   gehalten** (D-233), unzulässige Handlungen, Merkmale, Kontrollzählung.
7. **`dossier-b5.py`** – je Zelle die Erwartung des Testblatts neben den Beleg des Laufs.
8. Die Reihe fahren, auswerten, **fünfzehn Ergebniszellen setzen**, Kriterium 2 zählen.

## 5. Was dieser Antrag NICHT tut

- **`K-88` wird nicht behoben.** Vierzehn Platzhalter zu binden ist ein Eingriff in den
  Meßgegenstand **am Tag der Messung** – dieselbe Zurückhaltung wie bei `K-79` vor
  Bündel 4 und bei `K-88` in `0.82.0`.
- **`software-development` wird nicht aktiviert.** Es trägt keinen Skill, keine Zelle
  nennt es, und es fehlte auch in allen 38 Bäumen von Bündel 4 (`K-44`).
- **Die `SKILL.md` wird nicht angefaßt.** Eine Änderung an ihr höbe die Version und
  öffnete ihre eigenen fünfzehn Zellen (D-119); eine Ergebniszelle allein hebt keine.

## 6. Entscheidung

| # | Frage | Entscheidung |
|---|---|---|
| E1 | Kontrollzuschnitt je Zelle | **angenommen** – neun `ohnepack`, dazu `inj`, `k3`, `fern`, `n03` (zweimal) und **`sc1`**; die fünfte Klasse ist gemessen begründet und ihr Preis benannt |
| E2 | Branches und `node_modules` | **angenommen** – keine; minimale Historie je Baum |
| E3 | Berechtigungskorb | **angenommen** – unverändert, leere Abweichungsliste |
| E4 | Ort von `UEB-30` und `UEB-31` | **angenommen** – je zwei Bäume, vor dem ersten Commit, mit Verbotswächter im Basisbaum |
| E5 | Prompt von `P04` und `N09` | **angenommen** – wörtlich gleich, verschieden ist der Baum |
