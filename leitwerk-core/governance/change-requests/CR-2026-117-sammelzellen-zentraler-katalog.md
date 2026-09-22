# Änderungsantrag `CR-2026-117`

| Feld | Inhalt |
|---|---|
| Titel | Die vier Sammelzellen des zentralen Katalogs – und der Nachlauf von `RE-001-P05` |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-22 |
| Betroffene Artefakte | `tests/TEST_CATALOG.md` (vier Ergebniszellen, zwei Vorbedingungen), `framework/runtime/root-instruction.md`, `framework/runtime/rules/20-project-overlay.md`, `checklists/01-preflight.md`, `governance/FRAMEWORK_DEV_PROFILE.md`, `framework/role-packs/requirements-engineering/skills/role-re-ticket/SKILL.md` und `TESTS.md`, `tests/scripts/validate-framework.py` (Prüfung 55b), `tests/scripts/validate-output.py`, `tests/scripts/probe-pruefungen.py`, `tests/erhebungen/*-b5.py` (Nachlauf und MCP-Wächter), `tests/erhebungen/README.md`, `governance/DECISION_LOG.md`, `tests/protocols/2026-09-22-sammelzellen-zentraler-katalog.md` (neu), `docs/ROADMAP.md`, `CHANGELOG.md`, `VERSION`, `UEBERGABE.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind vier Ergebniszellen des Testkatalogs, drei anweisende Laufzeitfassungen und zwei Prüfmittel |
| Art | **Abnahme ohne Kontingent, mit einem Nachlauf** – zwei bezahlte Läufe, rund 2,70 USD |
| Dringlichkeit | **Regulär**; der Wiederaufnahmepunkt von `0.83.0` nennt ihn als nächsten Posten |

## 1. Anlass

Der Meßtag von Bündel 5 (`CR-2026-116`) hat Kriterium 2 von 19 auf **5** gebracht. Offen
sind die **vier Sammelzellen des zentralen Katalogs** und **`RE-001-P05`**.

Die Sammelzellen können nicht vor ihren Bestandteilen schließen (D-139, D-143). **Ob sie
es jetzt können, ist eine Zählung und kein Lauf** – und die Zählung ist der erste Posten
dieses Antrags. Sie hat vier Befunde ergeben, **alle vor dem ersten bezahlten Lauf**.

> *Fünfundzwanzigster Durchgang in Folge, bei dem der billigste Befund vor dem Lauf fällt.*

## 2. Der Gegenstand: vier Sammelzellen – gezählt, nicht geschätzt

| Sammelzelle | Bestandteile laut Vorbedingung | gezählt | davon offen | schließbar |
|---|---|---|---|---|
| `FW-NE-04` | „alle 58 Zellen `SK-…-N0n` der dreizehn Testblätter" | **58** | **0** | 🟢 **sofort** |
| `FW-PO-03` | „alle 29 Zellen `SK-…-P0n` der dreizehn Testblätter" | **29** | **1** (`RE-001-P05`) | nach dem Nachlauf |
| `FW-RE-01` | „alle 18 Basistests und die Skill-Tests der betroffenen Skills" | **18 + 87** | **1** (dieselbe) | nach dem Nachlauf |
| `FW-KO-05` | 20 Grenzfälle, `EDGE_CASES.md` vollständig | 18 prüfbar | G-11 | nach `K-59` |

**Alle 18 Basistests des Katalogs tragen `bestanden`.** Von den 87 Blattzellen der
dreizehn Testblätter ist **eine** offen, und sie ist dieselbe in beiden Sammelzellen.

> ➡️ **Der Nachlauf von `RE-001-P05` ist der Schlüssel zu zwei der vier Sammelzellen**,
> `K-59` der zu einer dritten. Die vierte steht schon offen.

## 3. Vorlage zur Entscheidung

### E1 – Die Vorbedingung nennt ein Kennungsmuster und meint eine Gattung

🔴 **Gemessen.** `FW-PO-03` verlangt *„alle **29** Zellen `SK-…-P0n`"*. Zellen mit dem
Präfix `SK-` gibt es **24** – zwei je `fw-*`-Skill, zwölf Skills. Die 29 stimmen erst,
wenn die fünf `RE-001-P0n` des Role Packs mitzählen; bei `FW-NE-04` ebenso: 48 `SK-`,
zehn `RE-001-N0n`, zusammen **58**.

**Beide Zahlen sind richtig, beide Muster sind falsch.** Sie stammen aus `CR-2026-083`
(2026-09-18), als `role-re-ticket` das dreizehnte Testblatt schon trug.

| Auflösung | Preis |
|---|---|
| **a) Das Muster auf die Gattung stellen** – *„alle 29 Positivzellen (`…-P0n`) der dreizehn Testblätter"* | Die Vorbedingung nennt keine Kennungsfamilie mehr; wer ein vierzehntes Blatt anlegt, ändert die Zahl und nicht das Muster |
| b) Das Muster stehen lassen und die Zahl auf 24 bzw. 48 senken | **Die fünfzehn Zellen des Role Packs fielen aus beiden Sammelzellen heraus** – genau der Fehler, den die Zählregel von Kriterium 2 ausdrücklich benennt (*„wer das übersieht, zählt 103 statt 118"*) |
| c) Beides stehen lassen | Eine Vorbedingung, deren Muster ihre eigene Zahl nicht trifft, ist bei jeder Wiederholung neu auszulegen |

➡️ **Vorschlag: a.** Die Gattung ist der Gegenstand, die Kennungsfamilie war nur ihre
Schreibweise – dieselbe Lehre wie D-246 am Verrat-Wächter und D-237 am Skillwächter:
**Marken und Namenslisten gehören abgeleitet, nicht aufgeschrieben.**

### E2 – `K-59`: Wie kommt der zweite Einsatzkontext in die drei Fassungen?

**Die Lage war anders beschrieben, als sie ist.** Drei Messungen:

🔴 **Der Preis, der die Vertagung trägt, ist seit `0.32.0` bezahlt.** `K-59` steht auf
*„den Text nachziehen hieße, eine Ausnahme in **jede Installation** auszuliefern"*.
Gemessen an einer frischen Installation (`install.py --client claude-code --root <leer>`):
Der Halbsatz *„und im Quellrepositorium des Frameworks selbst"* steht dort **in zehn
Dateien** – fünf `SKILL.md` und fünf Skill-`CHANGELOG.md`.

🔴 **Und das Profil, das die Ausnahme trägt und begrenzt, liegt in beiden übernehmenden
Projekten.** Sein Abschnitt 2.3 sagt *„Dieses Profil wird in **kein Zielprojekt**
installiert"* und begründet es mit `install.py`. Der Satz beschreibt das **Werkzeug**,
nicht das **Ergebnis**: `docs/ADOPTION_GUIDE.md` Schritt 2 sagt `cp -r leitwerk-core/
/pfad/zum/projekt/`, und `test-devin-framework` wie `otp-generator` führen
`leitwerk-core/governance/FRAMEWORK_DEV_PROFILE.md`.

🔴 **Die Abweichung ist größer als beschrieben, nicht kleiner.** G-11 erlaubt **zwei**
Handlungen: die Analyse (**M1**) und das Ablegen des Protokolls (**M5**, schreibend). Die
**Leseseite** kennen fünf der sechs Fassungen. Die **Schreibseite kennt keine einzige** –
auch nicht die fünf Analyseskills, die alle M1 führen; und `fw-docs-update`, der einzige
M5-Skill mit dieser Vorbedingung, sagt ausdrücklich *„Ohne aktives Overlay arbeitet der
Skill nur lesend (Abgleich ohne Änderung)"* und nennt das Quellrepositorium nicht.

> *Ein Befund aus einer Messung gehört gegen den Träger gehalten, bevor er eingeordnet
> wird (0.55.0) – hier wird er dadurch schärfer.*

🟢 **Die Bedingung aus Abschnitt 2.1 ist trennscharf, und das ist gemessen.** Sie fragt,
ob die Laufzeitschicht laut `.gitignore` ein **Erzeugnis** ist. Im Quellrepositorium
stehen `/AGENTS.md`, `/.devin/` und `/project-overlay/` in der `.gitignore`; das
Übungsrepositorium schließt sie ausdrücklich **nicht** aus und sagt im Kommentar warum;
der Pilot führt sie ebenfalls versioniert. **Drei Repositorien, drei Male richtig.**
Damit fällt auch der zweite Einwand: Abschnitt 2.2 verbietet die **Behauptung** des
Clients, nicht die **Beobachtung** eines Inhalts, der nach Abschnitt 3.1 K0 ist.

| Auflösung | Preis |
|---|---|
| **a) Verweis statt Ausnahme** – die drei Fassungen nennen das Entwicklungsprofil als die Fassung, die diesen Fall führt, **ohne** eine Erlaubnis auszusprechen; der Satz *„nur lesend"* bleibt wörtlich stehen | Der Verweis wird in jede Installation ausgeliefert – was die fünf Analyseskills seit vierunddreißig Releases ohnehin tun. **Er lockert nichts:** Das Profil erteilt nach seinem Abschnitt 5 keine technische Berechtigung, und die Schranke bleibt der Prozeß |
| b) Die Grenzfallzeile G-11 auf die Leseseite einschränken | `FW-KO-05` mißt für die Schreibseite nichts mehr – und die Schreibseite ist genau das, was **jede** Sitzung an diesem Framework tut, auch die, die dieses Protokoll ablegt. Die Lage bliebe ungeregelt, nur unsichtbar |
| c) `K-59` weiter offen lassen | `FW-KO-05` bleibt offen; Kriterium 2 geht auf **1** statt auf **0**, und der Klärungspunkt blockiert den letzten Schritt vor der Umbenennung |

➡️ **Vorschlag: a**, mit drei Nachträgen: Abschnitt 2.3 des Profils wird auf das
berichtigt, was gemessen ist; die Schreibseite (M5, Berichtspfad) wird in Abschnitt 4.6
ausdrücklich als das benannt, was der Verweis trägt; `EDGE_CASES.md` G-11 nennt das
Profil als Quelle beider Hälften.

### E3 – Die Reihenfolge: zwei Posten greifen in den Meßgegenstand ein

🔴 **Gemessen.** `K-88` bindet vierzehn Pflichtplatzhalter im **Übungs-Overlay** – dem
Meßgegenstand von `RE-001-P04` und `N09`. `K-90` ändert die **`SKILL.md`** von
`role-re-ticket` – dem Meßgegenstand aller fünfzehn Zellen. **Der Nachlauf von
`RE-001-P05` steht noch aus.**

| Auflösung | Preis |
|---|---|
| **a) Nachlauf zuerst, dann `K-88` und `K-90`** | Das Release hat eine Binnenreihenfolge, die eingehalten werden muß, und die Abnahme läuft zweimal |
| b) `K-88` und `K-90` nur entscheiden, nicht umsetzen | Zwei Klärungspunkte bleiben formal offen, der Vorbedingungsdurchgang ist zweimal zu machen |
| c) Alles vor dem Nachlauf | **Der Nachlauf mäße gegen ein anderes Overlay und eine andere `SKILL.md` als die vierzehn abgenommenen Zellen** – zwei Meßpunkte mit drei Unterschieden, und `K-84` selbst erzeugt |

➡️ **Vorschlag: a.** *Wer den Meßgegenstand anfaßt, während eine Zelle auf ihm noch
offen ist, mißt den Eingriff.*

### E4 – `K-91`: Wie sieht der Prompt des Nachlaufs aus – und soll die Zelle ihn verlangen?

`RE-001-P05` verlangt *„Bestehende Beschreibung überarbeiten, Umfang erhalten"*. Der
Prompt des Meßtags lautete `ueberarbeite:` und drei vage Sätze; der Lauf hat gemeldet,
daß keine Beschreibung übergeben wurde, und den Umfang **nicht** erweitert. **Sein
Verhalten war einwandfrei, und die Zelle blieb offen** (D-116): *„Umfang unverändert"*
hat ohne bestätigten Umfang keinen Bezugspunkt.

**Der Nachlauf braucht eine Beschreibung, die zugleich unklar und im Umfang erkennbar
ist.** Die Erwartungsspalte nennt vier Gegenstände: Klarheit, Struktur, Prüfbarkeit
verbessert – **Umfang unverändert** – Lücken als offene Fragen mit Adressat – keine neuen
Anforderungen. Die dritte und vierte brauchen unpräzise Abnahmekriterien, die zweite
braucht einen abgrenzbaren Umfang.

| Auflösung | Preis |
|---|---|
| **a) Strukturierte Beschreibung im Prompt: Titel, Umfang in drei Punkten, zwei unpräzise Abnahmekriterien** – und die Vorbedingung der Zelle verlangt es ausdrücklich | Der Prompt wird länger und die Vorbedingung nennt einen Eingabebestandteil. **Genau das ist der Punkt:** Eine Vorbedingung, die den Gegenstand der Eingabe nicht nennt, läßt ihn beim nächsten Mal wieder fehlen |
| b) Nur den Prompt ändern, Vorbedingung lassen | Der nächste Durchgang schreibt den Prompt wieder frei und fällt in dieselbe Lücke – `K-91` wäre behoben und sein Mechanismus nicht |
| c) Die Erwartungsspalte entschärfen (*„Umfang unverändert"* streichen) | Die Zelle verlöre ihren Gegenstand; der Skill hat die Umfangstreue als ausdrückliche Rollengrenze |

➡️ **Vorschlag: a.** Die Vorbedingung bekommt den Satz, daß die zu überarbeitende
Beschreibung **mit erkennbarem Umfang** im Prompt übergeben wird, und der Verrat-Wächter
von `prompts-schreiben-b5.py` bleibt unberührt: Die Beschreibung nennt weder Kennung noch
Erwartungswert noch den Gegenstand der Recherche.

> *Beim Schreiben eines Prompts gegen jede Erwartungsspalte seiner Zelle lesen – nicht
> nur gegen die Eingabespalte (D-255).*

### E5 – `K-89`: Ein Wächter für die MCP-Ausstattung des Meßbaums

Gemessen am Meßtag: **19 von 30 Läufen** melden den Widerspruch, **null** rufen ein
MCP-Werkzeug auf. Das Übungs-Overlay führt *„Freigegebene MCP-Server: keine"*; die
Sitzungen bekamen zwei gestellt, weil sie in der **Benutzerkonfiguration** stehen.

| Auflösung | Preis |
|---|---|
| **a) Wächter im Baumbau, der die Ausstattung gegen das Overlay hält und den Befund NENNT** | Er kann sie nicht abschalten – die Quelle liegt außerhalb jedes Baums. Er macht die Abweichung zu einer **ausgewiesenen** statt zu einer entdeckten |
| b) Zusätzlich abschalten (`--strict-mcp-config` oder eine leere Projektkonfiguration) | Ein Meßaufbau, der die Umgebung des Arbeitsplatzes verändert, mißt eine Umgebung, die es sonst nicht gibt – und die Meldepflicht des Frameworks wäre nicht mehr meßbar |
| c) Nichts tun | Der nächste Meßtag findet denselben Widerspruch, und niemand weiß, ob er derselbe ist |

➡️ **Vorschlag: a.** *Vor jedem Meßtag den Werkzeugbestand des Baums gegen sein Overlay
halten* – und das Ergebnis in die Zustandsaufnahme schreiben, nicht in eine Erinnerung.
🟢 **Daß die Läufe es von sich aus gemeldet haben, ist ein Meßwert und bleibt einer.**

### E6 – `K-88`: Prüft 55b eine Bindung oder eine Teilzeichenkette?

🔴 **Nachgemessen am 2026-09-22.** Die Prüfung fragt `if name in text` und meldet **0**.
Mit dem Namen **in spitzen Klammern** meldet sie **14 von 26** – und dieselben 14 auch ohne den
Änderungsverlauf des Overlays. *(Der Decision Log nennt dort 15; `<ISSUE_TRACKER>` ist mit
`0.82.0` gebunden worden, D-245.)*

**Die schärfste Stelle ist der Meldungstext der Prüfung selbst:** Er sagt *„ist im Overlay
aber **nirgends gebunden**"* – und prüft eine Nennung. **Der wiederkehrende Befundtyp,
in der Prüfung, die ihn finden soll.**

| Auflösung | Preis |
|---|---|
| **a) 55b verlangt den Namen in spitzen Klammern; die vierzehn Platzhalter werden gebunden** | Die Laufzeitfassung des Übungs-Overlays hat **37 Zeichen** Luft bis zur SOLL-Grenze von 6.000 – die Bindungen gehören in die **Detailfassung**, und die Grenze ist nachzumessen. **Nur nach dem Nachlauf** (E3) |
| b) 55b verlangt die spitzen Klammern und meldet als **Warnung** | Der Validator bliebe fehlerfrei und trüge vierzehn Zeilen neben jedem Lauf. Eine Warnung, die bei jedem Lauf steht, wird gelesen und nicht bearbeitet |
| c) Teilzeichenkette belassen, `K-88` mit Begründung schließen | Meldungstext und Mechanismus stehen weiter gegeneinander |

➡️ **Vorschlag: a**, mit Sonde und Gegenprobe nach D-23 und einem Nachtrag an `K-69` und
`K-79`: Sie bekommen mit dieser Prüfung ihren Zähler.

### E7 – `K-90`: `validate-output.py` gegen einen Abschnitt, der zu Recht fehlt

🔴 **Am Beleg nachgesehen, und die Lage ist genauer als beschrieben.** `RE-001-P02` hat
nicht *weggelassen*, sondern **fünf Abschnitte zu einer Überschrift zusammengezogen** –
*„### Titel, Beschreibung, Anforderungen, Arbeitspakete, Abnahmekriterien"* – und den
Inhalt als `` `<TBD: ausgesetzt, bis F1 beantwortet ist>` `` ausgewiesen, mit Begründung.
Das Prüfmittel meldet die drei, deren Name es in der zusammengezogenen Überschrift nicht
wiederfindet.

**`SKILL.md` Abschnitt 5 sagt *„Abschnitte ohne Inhalt werden weggelassen"* und nennt
keine Form für das Aussetzen.** Der Lauf hat eine erfunden, und sie ist gut – aber sie ist
nicht vereinbart, und deshalb kann kein Prüfmittel sie kennen.

| Auflösung | Preis |
|---|---|
| **a) Die Schreibweise festlegen und das Prüfmittel sie kennen lassen:** Die Überschrift bleibt stehen, der Inhalt ist `<TBD: ausgesetzt, weil …>` | Eingriff in die `SKILL.md`, also in den Meßgegenstand – **nur nach dem Nachlauf** (E3). Die Version des Skills steigt, und nach D-119 wäre das ein Fall für `K-84`; er ist im Antrag benannt |
| b) Nur `validate-output.py` ändern: fehlende Abschnitte werden verziehen, sobald die Ausgabe irgendwo `<TBD: ausgesetzt` trägt | Kein Eingriff in den Meßgegenstand – aber ein Lauf, der einen Abschnitt **vergißt** und anderswo ein Aussetzen ausweist, kommt durch. Die Zuordnung Abschnitt ↔ Aussetzen wird nicht geprüft |
| c) `K-90` offen lassen | Das zweite Prüfmittel von drei Zellen meldet bei richtigem Verhalten rot, und die Auflösung steht nur in Prosa |

➡️ **Vorschlag: a.** Die Trennlinie ist **ausgewiesenes Aussetzen ja, stilles Weglassen
nein** – und sie hängt an einer Schreibweise, die dann vereinbart ist.

## 4. Umsetzung

**Die Reihenfolge ist Gegenstand von E3 und wird eingehalten.**

1. **Vorbedingungen (E1):** Die beiden Sammelzellen bekommen die Gattung statt des
   Kennungsmusters. Die Zählung selbst kommt ins Protokoll.
2. **`K-59` (E2):** Verweis in `root-instruction.md` §3, in die Statuszeile von
   `rules/20-project-overlay.md` und in `checklists/01-preflight.md`; Berichtigung von
   `FRAMEWORK_DEV_PROFILE.md` 2.3 und Nachtrag in 4.6; `EDGE_CASES.md` G-11 nennt das
   Profil für **beide** Hälften. Decision Record.
3. **`FW-KO-05`, `FW-NE-04`** abnehmen. Kriterium 2: **5 → 3**.
4. **`K-89` (E5):** Wächter über die Werkzeugausstattung des Meßbaums, in die
   Zustandsaufnahme und in die Vorbedingungsliste von `tests/erhebungen/README.md`.
5. **Rücksprache mit `<FRAMEWORK_OWNER>` vor dem bezahlten Lauf.**
6. **Der Nachlauf (E4):** Basis und zwei Bäume neu bauen (`re001p05`, `kre001p05`), Prompt
   schreiben, zwei Läufe, auswerten, Dossier. `RE-001-P05`, `FW-PO-03` und `FW-RE-01`
   setzen. Kriterium 2: **3 → 0**.
7. **`K-88` (E6)** und **`K-90` (E7)** umsetzen, je mit Sonde und Gegenprobe.
8. Validator, Sondenlauf in beiden Kodierungsumgebungen, Protokoll, Übergabe.
9. **Aufräumen** – und hier fiel der neunte Befund: `baeume_loeschen.py` führte den
   Zielpfad von Bündel 4 im Quelltext (D-262).

## 5. Was dieser Antrag NICHT tut

- **`K-84` wird nicht entschieden.** Er wird durch E7 **größer**: Eine Änderung an der
  `SKILL.md` von `role-re-ticket` hebt deren Version, und vierzehn frisch abgenommene
  Zellen stehen auf der Fassung davor. Der Antrag benennt es und entscheidet es nicht.
- **Die Umbenennung auf `Koolie` wird nicht vorgezogen** (D-125, D-127).
- **Kriterium 1 wird nicht angefaßt** – das ist der Posten nach diesem.
- **`K-79` und `K-69` werden nicht geschlossen.** E6 gibt ihnen einen Zähler, keine
  Antwort: Zehn Werte des Quell-Overlays stehen weiter in keiner bindenden Schicht.

## 6. Entscheidung

| # | Frage | Entscheidung |
|---|---|---|
| E1 | Kennungsmuster oder Gattung | **angenommen (a)** – die Gattung; die Zahlen 29 und 58 bleiben und stimmen (D-252) |
| E2 | `K-59` | **angenommen (a)** – Verweis statt Ausnahme, mit drei Nachträgen; der Preis der Vertagung ist seit `0.32.0` bezahlt (D-253) |
| E3 | Reihenfolge | **angenommen (a)** – Nachlauf vor `K-88` und `K-90` (D-254) |
| E4 | Prompt und Vorbedingung von `RE-001-P05` | **angenommen (a)** – strukturierte Beschreibung, und die Vorbedingung verlangt sie (D-255) |
| E5 | `K-89` | **angenommen (a)** – Wächter, der nennt; nicht abschalten (D-256) |
| E6 | `K-88` | **angenommen (a)** – 55b verlangt die Bindung, vierzehn Platzhalter werden gebunden (D-257) |
| E7 | `K-90` | **angenommen (a)** – Schreibweise des Aussetzens vereinbart, Prüfmittel kennt sie (D-258) |
