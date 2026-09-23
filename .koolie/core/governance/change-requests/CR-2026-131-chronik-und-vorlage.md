# Änderungsantrag `CR-2026-131`

| Feld | Inhalt |
|---|---|
| Titel | Die Chronik, die ihr eigenes Release nicht zu Ende zählt – und eine Vorlage, die nur durch ihre Unvollständigkeit ungeprüft bleibt |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-23 |
| Betroffene Artefakte | `.koolie/core/tests/scripts/validate-framework.py` (**Prüfung 83**, **Prüfung 84**); `.koolie/core/tests/scripts/probe-pruefungen.py`; `.koolie/core/docs/ROADMAP.md`; `.koolie/core/clients/README.md` (Abschnitt 5); `.koolie/core/clients/_template/`; `.koolie/core/governance/DECISION_LOG.md` (**D-335** bis **D-340**, `K-112`, `K-113`); `.koolie/core/tests/TEST_CATALOG.md`; `.koolie/core/VERSION`; `.koolie/core/CHANGELOG.md`; `UEBERGABE.md` |
| Ebene laut Entscheidungsbaum 6 | Governance |
| Art | **Änderung.** MINOR-Release nach `RELEASE_PROCESS.md` Abschnitt 1 – zwei neue Prüfungen sind zwei neue Regeln, keine Formulierung |
| Dringlichkeit | regulär – **E2 ist Vorbedingung des nächsten Postens** und schnappt sonst mitten im Lauf zu |
| Status | 🟢 **entschieden am 2026-09-23** (E1 bis E5) |

---

## 1. Anlass

**Der Vorbedingungsdurchgang vor dem Posten `openai-codex`** – zum zwanzigsten Mal in
Folge der billigste Befund eines Releases. Elf Punkte gemessen, fünf grün, drei rot, drei
mit Vermerk. Die drei roten hängen an zwei Gegenständen, und beide liegen **vor** dem
eigentlichen Posten:

1. Die Chronik des Repositoriums zählt das eigene Release nicht zu Ende.
2. Die Vorlage, aus der das nächste Client Pack entstehen soll, ist vor dem Prüfapparat
   allein durch ihre Unvollständigkeit geschützt.

🟢 **Ein Befund ist dabei ausgeblieben, und das ist berichtenswert:** Die Tabelle
*Nächste freie Kennungen* stimmt – zum ersten Mal seit vier Releases, nachgezählt über
alle fünf Gattungen. Sie stand in `1.1.0`, `1.0.0` und `0.80.0` falsch.

## 2. Der erste Befund – gemessen, nicht gelesen

`docs/ROADMAP.md` führt je Release eine Zeile mit der **Spanne** der Entscheidungen, die
es vergeben hat. Über vierzehn Releases mit Spannenschreibweise ist sie lückenlos:

| Release | Spanne laut ROADMAP | vergeben laut Register |
|---|---|---|
| `0.90.0` | `D-313` bis `D-318` | sechs ✅ |
| `1.0.0` | `D-320` bis `D-327` | acht ✅ |
| `1.0.1` | `D-328` | eine ✅ |
| **`1.1.0`** | 🔴 **`D-329` bis `D-332`** | 🔴 **`D-329` bis `D-334` – sechs** |

**Das Register ist lückenlos:** 334 Zeilen bis `D-334`, keine Lücke. Die
Obergrenze der letzten Spanne ist um **zwei** zu niedrig.

### 2.1 Die Ursache ist gemessen und steht im eigenen Release

`D-333` und `D-334` sind **beim Umsetzen** gefallen – die Übergabe zu `1.1.0` sagt es
wörtlich: *„Zwei Befunde fielen erst beim Umsetzen, und der erste ist der schwerste des
Releases."* `K-111` fiel noch später, **beim Setzen der Marke**. Die ROADMAP-Zeile war zu
diesem Zeitpunkt längst geschrieben.

➡️ ***Eine Zahl, die vor ihrem Gegenstand geschrieben wird, ist zum Zeitpunkt ihrer
Niederschrift richtig und danach nicht mehr.*** Das ist die Bauform von Prüfung 40 – hier
**innerhalb eines einzigen Releases** statt über zweiundvierzig.

### 2.2 Der schwerere Teil: kein beschreibender Träger nennt alle sechs

Vier Träger beschreiben `1.1.0`. Gemessen über die wörtlichen Nennungen:

| Träger | genannte Entscheidungen | fehlt |
|---|---|---|
| `docs/ROADMAP.md` | 4 (als Spanne `D-329`–`D-332`) | `D-333`, `D-334` |
| `CHANGELOG.md` | 5 | 🔴 **`D-333`** |
| `CR-2026-130` | 4 | `D-331`, `D-333` |
| Protokoll | 4 | `D-329`, `D-332` |
| 🟢 **Marke `v1.1.0`** | 🟢 **alle sechs** (*„D-329 bis D-334"*) | – |

🔴 **`D-333` steht in keinem der vier.** Es steht im Register, im Protokoll und in den
**beiden normativen Trägern, die es geändert hat** (`RELEASE_PROCESS.md`,
`checklists/11-framework-release.md`) – also dort, wo es **wirkt**, und nirgends dort, wo
das Release **erklärt** wird. Wer die Chronik liest, findet die Regel nicht, die sein
eigenes Release eingeführt hat. Und `D-333` ist die Entscheidung, die den **schwersten**
Befund von `1.1.0` behoben hat.

➡️ ***Der einzige Träger, der die Menge vollständig nennt, ist der, den keine Prüfung
erreichen kann.*** Der Markentext liegt im Tag-Objekt, nicht im Arbeitsbaum, und in einer
Installation gibt es ihn nicht – das ist genau die Grenze, die `K-111` benennt.

### 2.3 Warum Prüfung 58 es nicht fängt

Prüfung 58 (D-169) hält die Vollständigkeit des Registers: **jede genannte Kennung steht
im Register.** Der Befund hier ist die **Gegenrichtung**: eine vergebene Kennung wird
nirgends genannt.

➡️ ***Prüfung 58 fängt die verwaiste Nennung, nicht die verwaiste Kennung.*** Die
Richtung ist einseitig, und die fehlende Richtung ist die, die die Chronik unvollständig
läßt. Das ist keine Lücke in Prüfung 58 – sie hat einen anderen Gegenstand –, sondern
eine Prüfung, die es nicht gibt.

## 3. Der zweite Befund – teurer, und er lag auf dem Weg des nächsten Postens

`clients/README.md` Abschnitt 5 beschreibt in neun Schritten, wie ein Client Pack
entsteht. **Schritt 1:** *„`_template/` nach `<client-name>/` kopieren und alle
Platzhalter ersetzen."* **Schritt 5:** *„`manifest.json` anlegen"* – und Abschnitt 3
sagt: *„Ohne Manifest ist ein Pack nicht installierbar."*

### 3.1 Die Vorlage trägt ein Drittel

| Bestandteil laut Abschnitt 3 | `_template/` | `claude-code/` | `devin-desktop/` |
|---|---|---|---|
| `CLIENT_PACK.md` | 🟢 ja (31 Matrixzeilen) | 🟢 ja | 🟢 ja |
| `manifest.json` | 🔴 **fehlt** | 🟢 ja | 🟢 ja |
| `root-template/` | 🔴 **fehlt** | 🟢 ja | 🟢 ja |

Schritt 1 sagt *„kopieren"* und liefert **eines von drei** Bestandteilen. Das allein wäre
ein Mangel der Anleitung. Der Befund ist der nächste Schritt.

### 3.2 Die Vorlage steht in der Packmenge des Prüfapparats – gemessen

`_client_packs()` in `validate-framework.py` nimmt jedes Verzeichnis unter `clients/` auf,
das eine `CLIENT_PACK.md` trägt. **`_template` erfüllt das.** Der Docstring der Funktion
hält die Annahme fest, die sie trägt:

> *„(Kennung, Verzeichnis, Manifest) je Client Pack; **`_template` ohne Manifest**."*

**Gemessen am 2026-09-23** – ein Probemanifest angelegt (eine Kopie des Manifests von
`claude-code`, also ein Manifest, das einen **fremden** Client beschreibt), Validator
gefahren, Probemanifest wieder entfernt:

| Messung | vorher | mit Probemanifest |
|---|---|---|
| `_client_packs()` | `_template`, `claude-code`, `devin-desktop` | unverändert **drei** |
| davon **mit Manifest** | `claude-code`, `devin-desktop` | 🔴 **`_template`, `claude-code`, `devin-desktop`** |
| `_p65_packkennungen()` | 🔴 **führt `_template` bereits heute** | unverändert |
| Validator | 0 Fehler, 0 Warnungen | 🔴 **0 Fehler, 0 Warnungen** |

🔴 **Der Validator meldet null.** Ein Verzeichnis namens `_template` mit einem Manifest,
das `claude-code` beschreibt, läuft als drittes Client Pack durch alle 82 Prüfungen.

### 3.3 Was der Befund wirklich ist

➡️ ***Eine Vorlage, die nur deshalb keine Prüfung auslöst, weil ihr ein Bestandteil
fehlt, ist nicht ausgenommen – sie ist unvollständig.*** Und der Tag, an dem jemand sie
nach der eigenen Anleitung vervollständigt, ist der Tag, an dem sie geprüft wird, ohne
daß es jemand entschieden hat.

🔴 **Das ist die Bauform *„Zwei Stellen, die einander decken"*** (`0.57.0`): Die
unvollständige Vorlage verhindert, daß die fehlende Ausnahme je auffällt. **Einzeln wäre
jede aufgefallen; zusammen sehen sie aus wie ein Lauf ohne Befund** – und genau so hat
der Validator 82 Prüfungen lang ausgesehen.

⚠️ **Und die Ausnahme existiert bereits – an zwei anderen Stellen.** Prüfung 73 schließt
`_template` ausdrücklich aus (`if n != "_template"`), und die Pfadausnahmen führen
`.koolie/core/clients/_template/` mit Begründung. **Der zentrale Iterator tut es nicht.**
➡️ *Wer eine Ausnahme an zwei Stellen führt und an der dritten vergißt, hat sie nicht
vergessen – er hat keine Stelle, an der sie steht.*

## 4. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | Bekommt die Chronik eine Prüfung – und welche Form? | **Prüfung 83:** Die Obergrenze der letzten Release-Spanne in `docs/ROADMAP.md` ist die höchste vergebene `D`-Kennung des Registers. Abweichung ist ein **Fehler** | ⚠️ **Jedes Release faßt diese Zeile an** – derselbe Preis wie bei Prüfung 67, 77 und 82. ⚠️ **Grenze, benannt: sie mißt die OBERGRENZE, nicht die Vollständigkeit der Nennungen.** Ein Träger, der die Spanne richtig führt und `D-333` im Fließtext nicht nennt, kommt durch |
| **E2** | Wird die Vorlage vervollständigt oder ausgenommen? | **Ausgenommen, und zwar dort, wo die Packmenge entsteht.** `_client_packs()` nimmt `_template` nicht mehr auf; **Prüfung 84** hält die Ausnahme fest und meldet, wenn die Vorlage Bestandteile eines vollständigen Packs trägt | ⚠️ Die Vorlage bleibt bei einem Bestandteil – **Schritt 1 der Anleitung wird deshalb umformuliert**, statt ein Drittel als Ganzes auszugeben. 🔴 **Der Gegenvorschlag (vervollständigen) ist abgelehnt:** Eine vollständige Vorlage wäre ein Pack ohne Client, und jede Prüfung müßte sie einzeln ausnehmen – die Ausnahme wanderte von einer Stelle auf achtzig |
| **E3** | Werden die beiden Chronikbefunde berichtigt? | **Ja.** ROADMAP-Zeile `1.1.0` auf `D-329` bis **`D-334`**, `K-110` **und** `K-111`; `1.0.1` und `1.0.0` in die richtige Reihenfolge | 🟢 **Kein Verstoß gegen D-273:** Berichtigt wird eine **Zahl**, die ihren Gegenstand falsch benennt, nicht ein Stand, der historisch gilt |
| **E4** | Wird `D-333` in einem beschreibenden Träger nachgetragen? | **Ja, im `CHANGELOG.md` von `1.1.0`.** Nachgetragen wird, was Register und Protokoll bereits festhalten; der Eintrag sagt in einem eigenen Satz, daß er ein Nachtrag ist | ⚠️ **Prüfung 83 erreicht es nicht** (siehe E1). Der Nachtrag ist eine Handlung, keine Regel – `K-112` führt die Frage weiter |
| **E5** | Einstufung und Lage im Releaseplan | **MINOR.** Zwei neue Prüfungen sind zwei neue Regeln. 🔴 **Der Releaseplan rückt um eins:** `openai-codex` von `1.2.0` auf `1.3.0`, Overlay *„General Development"* auf `1.4.0`, Installationsbibliothek auf `1.5.0` | ⚠️ **Eine Planzahl wird verschoben, und das wird ausgewiesen statt stillschweigend getan.** 🟢 Das Muster ist erprobt: `0.81.0` Vorbedingungen → `0.82.0` Herrichtung → `0.83.0` Meßtag – drei Nummern für einen Posten |

## 5. Umsetzung

1. **Prüfung 83** in `validate-framework.py`, mit drei Sonden und **zwei** Gegenproben in
   `probe-pruefungen.py`. Die zweite Gegenprobe: ein Release **ohne** Spannenschreibweise
   (ein einzelner Decision Record, wie `1.0.1`) muß **grün** sein.
2. **Prüfung 84** ebenso. `_client_packs()` schließt `_template` aus; die Ausnahme steht
   **an einer Stelle** und trägt ihre Begründung im Quelltext.
3. `docs/ROADMAP.md`: Zeile `1.1.0` berichtigt, `1.0.0`/`1.0.1` in Reihenfolge, Planzeilen
   gerückt, Standüberschrift auf `1.2.0`.
4. `clients/README.md` Abschnitt 5 Schritt 1 umformuliert; Abschnitt 3 nennt den Umfang
   der Vorlage ausdrücklich.
5. `CHANGELOG.md`: Nachtrag `D-333` bei `1.1.0`, neuer Abschnitt `1.2.0`.
6. `DECISION_LOG.md`: **D-335** bis **D-340**, `K-112` und `K-113`.
7. `TEST_CATALOG.md`: Prüfung 83 und 84 eingetragen.
8. 🔴 **Beide neuen Prüfungen laufen gegen BEIDE übernehmenden Projekte, bevor sie als
   fertig gelten** (D-326, D-299) – die Lehre, die `0.90.0` notiert und nicht angewandt
   hat.
9. Validator und Sondenlauf in **beiden** Kodierungsumgebungen (D-49).
10. Heben der übernehmenden Projekte **vor** dem Release-Commit (D-330), als **letzter**
    Eingriff in den Kern (D-333).

## 6. Entscheidung

🟢 **Angenommen am 2026-09-23, E1 bis E5 wie vorgelegt.**

| # | Entscheidung | Decision Record |
|---|---|---|
| E1 | Prüfung 83 – die Spanne der Chronik gegen das Register | **D-335** |
| E2 | Die Vorlage wird ausgenommen, nicht vervollständigt – Prüfung 84 | **D-336** |
| E3 | Die beiden Chronikbefunde werden berichtigt | **D-337** |
| E4 | `D-333` wird im `CHANGELOG.md` nachgetragen | **D-338** |
| E5 | MINOR; der Releaseplan rückt um eins | **D-339** |

Neue Klärungspunkte: `K-112` (erreicht eine Prüfung die **Nennungen**, nicht nur die
Spanne?), `K-113` (die Marke ist der vollständigste Träger und der einzige ungeprüfte –
gehört ihr Text in den Arbeitsbaum?).
