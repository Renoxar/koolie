# Protokoll: Die Chronik, die ihr eigenes Release nicht zu Ende zählt

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-23 |
| Release | **`1.2.0`** |
| Änderungsantrag | `CR-2026-131` |
| Art | **Arbeitsprotokoll.** Gegenstand sind die Chronik des Repositoriums, die Packmenge des Prüfapparats und zwei neue Prüfungen |
| Prüfmittel | `review` – Auszählung im Bestand; dazu ein **gemessener Eingriff** am Prüfapparat (Probemanifest), der Validator und der volle Sondenlauf in beiden Kodierungsumgebungen |
| Ergebnis | 🟢 **Zwei Befunde, beide aus dem Vorbedingungsdurchgang, beide mit einer Prüfung beantwortet.** 🔴 **Und eine Lehre aus `0.86.0` ist zugeschnappt, die wörtlich in der Übergabe stand** |

> 🔴 **Dies ist kein Abnahmeprotokoll des Testkatalogs** und trägt deshalb keinen
> Abschnitt *Gegenzeichnung* (D-319, Zuschnitt von Prüfung 80). Es berichtet eine
> Messung und trägt seinen Beleg in sich.

---

## 1. Der Anlaß

Der Wiederaufnahmepunkt zu `1.1.0` nennt als nächsten Posten das **Client Pack
`openai-codex`**. Vor dem ersten Handgriff stand der Vorbedingungsdurchgang – zum
**zwanzigsten** Mal in Folge, und zum zwanzigsten Mal war er der billigste Befund.

Elf Punkte gemessen: **fünf grün, drei rot, drei mit Vermerk.** Die drei roten hängen an
zwei Gegenständen, und **beide liegen vor dem eigentlichen Posten.**

## 2. Der Vorbedingungsdurchgang

| # | Befund | gemessen an |
|---|---|---|
| **V1** | 🟢 Die Tabelle *Nächste freie Kennungen* stimmt – **zum ersten Mal seit vier Releases** | `CR-2026-131`, `D-335`, `K-112`, `G-21`, `UEB-32` über alle fünf Gattungen nachgezählt; sie stand in `1.1.0`, `1.0.0` und `0.80.0` falsch |
| **V2** | 🟢 Das angemeldete Codex-Konto ist `plus` – die Berichtigung aus `1.1.0` hält | `id_token` des Kontos, Feld `chatgpt_plan_type` |
| **V3** | 🔴 **Die Release-Spanne von `1.1.0` endete bei `D-332`, vergeben sind `D-329` bis `D-334`** | Register lückenlos, 334 Zeilen; Abschnitt 3 |
| **V4** | 🔴 **Kein beschreibender Träger nennt alle sechs Entscheidungen** | vier Träger, vier Mengen; Abschnitt 3.2 |
| **V5** | 🔴 **`_template` steht in der Packmenge des Prüfapparats** | mit Probemanifest gemessen; Abschnitt 4 |
| **V6** | ⚠️ Codex unverändert `0.155.1`, verfügbar `0.156.1`. **Folgenlos für dieses Release** – der Meßtag ist auf `1.3.0` gerückt, und die geprüfte Clientversion wird nach D-117 und D-202 **vor** dem Erheben festgeschrieben | `codex doctor` |
| **V7** | ⚠️ `~/.codex/config.toml` führt weiter einen Vertrauenseintrag auf den **alten** Projektnamen und keinen auf den neuen. Rest der Umbenennung, **außerhalb des Repositoriums** | gelesen |
| **V8** | ⚠️ **`1.0.1` stand in `docs/ROADMAP.md` vor `1.0.0`** – die Tabelle ist über 133 Zeilen monoton aufsteigend und war an genau dieser einen Stelle nicht | gezählt |
| **V9** | 🟢 Die Bestandsliste steht in **allen drei** Trägern byte-gleich auf `1.1.0` – Prüfung 82 ist überall grün | Framework und beide übernehmenden Projekte |
| **V10** | 🟢 Die Word-Fassung steht auf `v1.1.0`; D-332 hält | `build/out/` |
| **V11** | 🟢 Standüberschrift und der Vermerk *„dieses Release"* stehen je **einmal** | gezählt |

🔴 **Keine Prüfung erreichte V3, V4, V5 oder V8.**

## 3. Der erste Befund: die Chronik zählt ihr eigenes Release nicht zu Ende

`docs/ROADMAP.md` führt je Release die **Spanne** seiner Entscheidungen. Über vierzehn
Releases mit dieser Schreibweise ist sie lückenlos – und genau die letzte war um **zwei**
zu niedrig.

| Release | Spanne laut ROADMAP | vergeben laut Register |
|---|---|---|
| `0.90.0` | `D-313` bis `D-318` | sechs ✅ |
| `1.0.0` | `D-320` bis `D-327` | acht ✅ |
| `1.0.1` | `D-328` | eine ✅ |
| **`1.1.0`** | 🔴 **`D-329` bis `D-332`** | 🔴 **`D-329` bis `D-334`** |

**Die Ursache ist gemessen und steht im eigenen Release.** `D-333` und `D-334` sind
*beim Umsetzen* gefallen – die Übergabe zu `1.1.0` sagt es wörtlich –, `K-111` sogar
erst beim Setzen der Marke. Die ROADMAP-Zeile war zu diesem Zeitpunkt längst geschrieben.

➡️ ***Eine Zahl, die vor ihrem Gegenstand geschrieben wird, ist zum Zeitpunkt ihrer
Niederschrift richtig und danach nicht mehr.*** Das ist die Bauform von Prüfung 40 –
hier **innerhalb eines einzigen Releases** statt über zweiundvierzig.

### 3.2 Der schwerere Teil

Vier Träger beschreiben `1.1.0`. Gemessen über die wörtlichen Nennungen:

| Träger | genannt | fehlt |
|---|---|---|
| `docs/ROADMAP.md` | 4 (als Spanne) | `D-333`, `D-334` |
| `CHANGELOG.md` | 5 | 🔴 **`D-333`** |
| `CR-2026-130` | 4 | `D-331`, `D-333` |
| Protokoll | 4 | `D-329`, `D-332` |
| 🟢 **Marke `v1.1.0`** | 🟢 **alle sechs** | – |

🔴 **`D-333` steht in keinem der vier.** Es steht im Register, im Protokoll und in den
**beiden normativen Trägern, die es geändert hat** – also dort, wo es **wirkt**, und
nirgends dort, wo das Release **erklärt** wird. Und es ist die Entscheidung, die den
**schwersten** Befund von `1.1.0` behoben hat.

➡️ ***Der einzige Träger, der die Menge vollständig nennt, ist der, den keine Prüfung
erreichen kann*** – der Markentext liegt im Tag-Objekt, nicht im Arbeitsbaum (`K-113`).
**Das ist `K-111` an einem zweiten Gegenstand:** dort die Freigabe, hier die
Entscheidungsmenge.

### 3.3 Warum Prüfung 58 es nicht fängt

Prüfung 58 (D-169) hält die Vollständigkeit des Registers: *jede genannte Kennung steht
im Register.* Der Befund hier ist die **Gegenrichtung**.
➡️ ***Prüfung 58 fängt die verwaiste Nennung, nicht die verwaiste Kennung.***

## 4. Der zweite Befund: die Vorlage in der Packmenge – ein gemessener Eingriff

`_client_packs()` nimmt jedes Verzeichnis unter `clients/` auf, das eine
`CLIENT_PACK.md` trägt. **`_template` erfüllt das.** Der Docstring hielt die Annahme
fest, die die Funktion trug: *„`_template` ohne Manifest"*.

**Der Eingriff, gefahren am 2026-09-23 und wieder zurückgenommen:** ein Probemanifest in
`clients/_template/` – eine Kopie des Manifests von `claude-code`, also eines, das einen
**fremden** Client beschreibt.

| Messung | vorher | mit Probemanifest |
|---|---|---|
| `_client_packs()` | `_template`, `claude-code`, `devin-desktop` | unverändert **drei** |
| davon **mit Manifest** | zwei | 🔴 **drei** |
| `_p65_packkennungen()` | 🔴 **führt `_template` bereits** | unverändert |
| Validator | 0 Fehler, 0 Warnungen | 🔴 **0 Fehler, 0 Warnungen** |

➡️ ***Eine Vorlage, die nur deshalb keine Prüfung auslöst, weil ihr ein Bestandteil
fehlt, ist nicht ausgenommen – sie ist unvollständig.*** Und der Tag, an dem jemand sie
nach der eigenen Anleitung vervollständigt – `clients/README.md` Schritt 5 verlangt genau
dieses Manifest –, ist der Tag, an dem sie geprüft wird, ohne daß es jemand entschieden
hat.

🔴 **Die Bauform *„zwei Stellen, die einander decken"*** (`0.57.0`): Die unvollständige
Vorlage verhindert, daß die fehlende Ausnahme je auffällt.

⚠️ **Und die Ausnahme existierte bereits an zwei anderen Stellen** – Prüfung 73 und die
Pfadausnahmen – und nicht dort, wo die Packmenge **entsteht**.
➡️ *Wer eine Ausnahme an zwei Stellen führt und an der dritten vergißt, hat sie nicht
vergessen – er hat keine Stelle, an der sie steht.*

## 5. Die beiden neuen Prüfungen

| Prüfung | Gegenstand | Einheiten | D-299-Probe |
|---|---|---|---|
| **83** | die höchste Release-Spanne gegen die höchste vergebene Kennung | 3 Sonden, 2 Gegenproben | 🟢 **bestanden** – beide Träger liegen im Kern und werden byte-gleich ausgeliefert |
| **84** | die Vorlage trägt keine Packbestandteile | 3 Sonden, 2 Gegenproben | 🟢 **bestanden** – der Gegenstand liegt im Kern |

🟢 **Prüfung 83 hat bei ihrem ersten Lauf ihren eigenen Anlaß gemeldet** – wie Prüfung 81
in `1.0.0`.

🔴 **Die zweite Gegenprobe von Prüfung 83 ist die, die man weglassen würde, und sie
trägt den Zuschnitt.** Die Releasetabelle ist **nicht sortiert** – V8 hat es gemessen.
Deshalb nimmt die Prüfung die **höchste** Obergrenze und nicht die zuletzt geschriebene;
die Gegenprobe stellt eine niedrigere Spanne **hinter** die höchste und verlangt Grün.
Ohne sie wäre die Reihenfolgefestigkeit eine Behauptung im Kopfkommentar statt eine
gemessene Eigenschaft (D-299, D-326).

🔴 **Die erste Gegenprobe von Prüfung 84 mißt die Ausnahme selbst, nicht die Meldung.**
Sie legt das Probemanifest an und verlangt, daß **keine andere** Prüfung anspringt –
damit ist der Eingriff aus Abschnitt 4 eine **dauerhafte Einheit** und nicht eine
einmalige Messung.

⚠️ **Beide Prüfungen sind gegen beide übernehmenden Projekte gelaufen, bevor sie als
fertig galten** (D-326, D-299) – die Lehre, die `0.90.0` notiert und nicht angewandt hat.

## 5.1 Der Befund, den der Abnahmelauf gebracht hat – und zwei gefallene Auflösungen

🔴 **Prüfung 83 hat beim ersten Abnahmelauf einen Befund gemeldet, den keine der 82
bisherigen Prüfungen sehen konnte** (D-340). Die Gegenprobe 58b legt eine Registerzeile
mit ihrer Sondenkennung an; Prüfung 83 las sie als höchste vergebene Entscheidung und
meldete **654 fehlende Entscheidungen**.

**Die Auflösung ist zweimal gefallen, und beide Male im vollen Sondenlauf:**

| Anlauf | Auflösung | Was sie widerlegt hat |
|---|---|---|
| **1** | Die Kennung in die Menge der **belegten synthetischen Kennungen** stellen | 🔴 **Sonde 58a verlor ihren Gegenstand.** Prüfung 58 nimmt genau jene Menge vom **Melden** aus – und die Sonde prüft, daß gemeldet wird. Das Decision Log sagt denselben Satz über die Sondenkennung von Prüfung 50: *„sie soll ja gemeldet werden"* |
| **2** | Ein **eigener Absatz**, der die Kennung wörtlich nennt | 🔴 **Prüfung 58 meldete die Nennung**, weil die Kennung in keiner Registerzeile steht |
| **3** | 🟢 **Ein reservierter BEREICH** – `D`-Kennungen ab 900 | trägt. Er nennt keine Kennung, und er trägt die nächste Sondenkennung ohne Nachtrag |

➡️ ***Zwei Prüfungen, die dieselbe Kennung ansehen, stellen nicht dieselbe Frage.***
Prüfung 50 und 58 fragen nach **Zugehörigkeit**, Prüfung 83 nach einer **Grenze**. Eine
Liste beantwortet beide mit demselben Eintrag – und hebt dabei die eine Antwort auf.

➡️ ***Eine Ausnahme, die ihren Gegenstand nennen muß, um zu wirken, erzeugt den Befund,
den sie verhindern soll.*** Das ist der Grund, weshalb es ein Bereich geworden ist und
keine Liste.

🔴 **Das ist D-243 – *zwei Regeln, die einander die Voraussetzung entziehen* – an einem
Paar von SONDEN statt an einem Paar von Regeltexten, und zweimal hintereinander
zugeschnappt.** ⚠️ **Und es ist der Beleg dafür, daß der Abnahmelauf gegen den fertigen
Baum kein Formalakt ist:** Beide Auflösungen sahen am Validator grün aus. **Gefunden hat
sie allein der volle Sondenlauf.**

⚠️ **Grenze, benannt:** Der Bereich ist eine Behauptung über künftige Vergaben. Wird je
eine echte Entscheidung oberhalb der Grenze vergeben, ist die Regel verletzt, und **keine
Prüfung meldet das** (`K-114`). Heute beträgt der Abstand 560 Kennungen.


## 6. Die Fallen, die zugeschnappt sind

| # | Falle | Wo sie zuschnappte |
|---|---|---|
| 1 | 🔴 **DIE TEUERSTE, UND SIE STAND WÖRTLICH IN DER ÜBERGABE.** *„Ein Sondenlauf mißt den Baum, in dem er startet; wer ihn nebenher fahren läßt, mißt den Baum von vorhin"* – der Fall aus `0.86.0`. **Der volle Lauf wurde gefahren, als `VERSION` schon auf `1.2.0` stand und die Übergabe noch auf `1.1.0`.** 112 von 325 Einheiten meldeten **dieselben zwei Fehler**, die nichts mit ihrem Gegenstand zu tun haben. **509 Sekunden verloren.** ➡️ *Die Lehre stand da, war gelesen, und ist trotzdem zugeschnappt* – **D-326 an einem dritten Gegenstand.** 🔴 **Keine Prüfung erreicht die Reihenfolge**, und das ist der eigentliche Befund |
| 2 | 🔴 **Ein neu angelegter Träger trägt LF, der Kern trägt CRLF.** Der Änderungsantrag dieses Releases. **Prüfung 81 fängt es – aber erst im Sondenlauf**, weil sie den **Git-Bestand** mißt und ein nicht committeter Träger nicht darin steht. ➡️ *Eine Prüfung, die den Bestand mißt, erreicht eine Datei erst, wenn sie darin ist* – **der Validatorlauf davor war grün** |
| 3 | ⚠️ **Die Zahl in `26-qs-test.md` bewegt sich mit jedem angelegten Träger.** Antrag und Protokoll heben sie um zwei. Sie gehört gesetzt, **nachdem** alle Träger stehen, und nicht davor |
| 4 | ⚠️ **Die Heredoc-Form bricht an einem Anführungszeichen im Text.** Die Patchblöcke dieses Releases laufen deshalb über Dateien im Ablagebereich, nicht über die Eingabezeile – die Verschärfung von Falle 1 aus `1.1.0` |
| 6 | 🔴 **Eine Ausnahme kann den Gegenstand einer FREMDEN Sonde aufheben.** Der erste Anlauf zu D-340 stellte eine Sondenkennung in die Ausnahmemenge von Prüfung 58 – und **Sonde 58a hatte danach nichts mehr zu messen.** ➡️ *Wer eine Ausnahme setzt, zählt zuerst, wer den Gegenstand noch braucht.* 🔴 **Der zweite Anlauf nannte die Kennung wörtlich, und Prüfung 58 meldete die Nennung** – *eine Ausnahme, die ihren Gegenstand nennen muß, um zu wirken, erzeugt den Befund, den sie verhindern soll.* 🟢 Beide gefunden **nur** vom vollen Sondenlauf; der Validator war beide Male grün |
| 5 | 🟢 **Gefangen, bevor sie zuschnappte:** `printf` schreibt LF, und `VERSION` ist ein versionierter Träger. **Prüfung 81 hat es beim nächsten Lauf gemeldet** – derselbe Gegenstand wie Falle 2, zwei Stunden früher |

## 7. Die Abnahme

*(Die Zahlen unterhalb dieser Linie sind Laufzeiten und nicht Teil des zeilengleichen
Vergleichs nach D-94.)*

---

| Lauf | Ergebnis |
|---|---|
| Validator, Framework | 🟢 **0 Fehler, 0 Warnungen** über **84 Prüfungen** |
| Validator, `devpacks/otp-generator` `--strict-overlay` | 🟢 **1 Fehler, 2 Warnungen** – **identisch mit dem Stand vor dem Heben**; der Fehler ist Projektarbeit (gesperrter Begriff im Projekt-`CHANGELOG.md`) |
| Validator, `devpacks/test-devin-framework` `--strict-overlay` | 🟢 **0 Fehler, 1 Warnung** (`K-88`, 6.023 von 6.000 Zeichen) |
| Sondenlauf, beide Kodierungsumgebungen (D-49) | 🟢 **325 angemeldete Einheiten, 463 Ergebniszeilen, Exit 0** – *„alle Sonden und Gegenproben bestanden"* in **beiden** Umgebungen |
| Zeilengleicher Vergleich der beiden Läufe (D-49) | 🟢 **0 Unterschiede in 499 Zeilen** |
| Erzeugnisse der Lieferung (Abschnitt 4.1 Schritt 3) | 🟢 **Je Client Pack gebaut und im Erzeugnis nachgezählt:** `Koolie_v1.2.0_claude-code.docx` und `Koolie_v1.2.0_devin-desktop.docx`, je 2,01 MB, **8 von 8 Diagrammen eingebettet** – gezählt an `word/media/` und den Bildverweisen, nicht an der Meldung (D-328) |
| Heben (Abschnitt 4.1 Schritt 2) | 🟢 **521 Träger aus dem Arbeitsbaum**, deckungsgleich mit `git ls-files`, **null Einträge aus `build/out/`**; beide Projekte **vor** dem Release-Commit gehoben (D-330, D-333) |

⚠️ **Laufzeit des Sondenapparats:** 4.136 s Rechenzeit in 525 s Wanduhr (Umgebung 1),
4.213 s in 534 s (Umgebung 2), je acht Bahnen.
🔴 **Dazu kommen DREI verworfene Läufe von zusammen rund 1.590 s** – der verfrühte aus
Falle 1 und die beiden, die die gefallenen Auflösungen von D-340 gemessen haben.
➡️ *Zwei davon waren kein Verlust, sondern der Preis der Messung: Sie haben die beiden
falschen Auflösungen widerlegt, und der Validator war beide Male grün.*

🔴 **Der Overlay-Änderungsverlauf beider übernehmenden Projekte trägt die falsche Spanne
`D-329 bis D-332`** – der Befund aus Abschnitt 3 an einer **vierten** Stelle, in beide
Projekte ausgeliefert. **Er bleibt stehen:** Die Chronik berichtet ihren damaligen Stand
(D-273), und **Prüfung 83 erreicht ein Overlay nicht** – sie mißt `docs/ROADMAP.md`
gegen das Decision Log, und beide sind Kernträger. ➡️ *Eine Prüfung reicht so weit wie
ihr Gegenstand, und die Auslieferung trägt weiter als er.*
