# Änderungsantrag `CR-2026-132`

| Feld | Inhalt |
|---|---|
| Titel | Die Erhebung zu `openai-codex` – der Client, dessen Wurzelanweisung eine Datei daneben ersetzt |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-23 |
| Betroffene Artefakte | `.koolie/core/tests/scripts/validate-framework.py` (**Prüfung 85**); `.koolie/core/tests/scripts/probe-pruefungen.py`; `.koolie/core/docs/ROADMAP.md`; `.koolie/core/governance/RELEASE_PROCESS.md` (Abschnitt 4.1 Schritt 2); `.koolie/core/checklists/11-framework-release.md`; `.koolie/core/governance/DECISION_LOG.md` (**D-341** bis **D-345**, `K-115`, `K-116`); `.koolie/core/tests/TEST_CATALOG.md`; `.koolie/core/VERSION`; `.koolie/core/CHANGELOG.md`; `.koolie/core/governance/ADOPTION_REGISTRY.md`; `UEBERGABE.md` |
| Ebene laut Entscheidungsbaum 6 | Governance |
| Art | **Änderung.** MINOR-Release nach `RELEASE_PROCESS.md` Abschnitt 1 – eine neue Prüfung ist eine neue Regel, und Abschnitt 4.1 bekommt einen Handgriff |
| Dringlichkeit | regulär – **die Erhebung ist Vorbedingung des Packbaus**, und drei ihrer Befunde ändern dessen Bauform |
| Status | 🟢 **entschieden am 2026-09-23** (E1 bis E5) |

---

## 1. Anlass

**Der Vorbedingungsdurchgang vor dem Posten `openai-codex`** – zum **einundzwanzigsten**
Mal in Folge der billigste Befund eines Releases. Und danach die **Erhebung** selbst:
die Schritte 2, 6 und 7 aus `clients/README.md` Abschnitt 5, die drei Erhebungen sind
und vor dem ersten geschriebenen Trägerbyte stehen.

🔴 **Sie hat den Posten umgeworfen.** Drei der zehn Befunde ändern die **Bauform** des
Packs, nicht seinen Inhalt – und ein Pack, das vor dieser Entscheidung gebaut wird, wird
zweimal gebaut.

🟢 **Und sie hat ihn zugleich billiger gemacht:** `codex debug prompt-input` rendert
genau das, was das Modell zu sehen bekommt, **ohne eine Sitzung zu eröffnen**. Die
gesamte Erhebung dieses Releases – zehn Messungen, sechs davon mit Gegenprobe – hat
**null Kontingent** gekostet.

## 2. Der Vorbedingungsdurchgang

| # | Befund | gemessen an |
|---|---|---|
| **V1** | 🟢 Die Tabelle *Nächste freie Kennungen* stimmt – **zum zweiten Mal in Folge** | `CR-2026-132`, `D-341`, `K-115`, `G-21`, `UEB-32` über alle fünf Gattungen nachgezählt: 340 `D`-Zeilen bis `D-340`, 112 `K`-Zeilen bis `K-114` |
| **V2** | 🟢 Das Codex-Konto ist `plus` – die Berichtigung aus `1.1.0` hält | `id_token`, Feld `chatgpt_plan_type` |
| **V3** | 🟢 **Die geprüfte Clientversion ist VOR dem Erheben festgeschrieben: `0.156.1`** (D-117, D-202). Der Owner hat während der Sitzung von `1.2.0` von `0.155.1` gehoben | `codex --version`, `codex doctor` |
| **V4** | 🔴 **Die Word-Fassung steht auf `v1.1.0`, `VERSION` auf `1.2.0`** – Schritt 3 von Abschnitt 4.1 ist bei `1.2.0` **nicht ausgeführt** worden. **Dritter Preis von `K-110` in vier Releases** | `build/out/` führt `Koolie_v1.1.0_*.docx` und keine Fassung `v1.2.0` |
| **V5** | 🟢 Die Bestandsliste steht in **allen drei** Trägern byte-gleich auf `1.2.0`, und **beide** übernehmenden Projekte tragen die Hebung als Commit | `cmp` über drei Kopien; `git log` in beiden Projekten |
| **V6** | 🟢 **Die Nennungen von `1.2.0` sind vollständig – und zwar in ZWEI beschreibenden Trägern**, `CHANGELOG.md` und dem Antrag. `K-112` hat seinen ersten Fall **nicht** gebracht | `D-335` bis `D-340` je Träger gezählt |
| **V7** | ⚠️ `~/.codex/config.toml` führt weiter einen Vertrauenseintrag auf den **alten** Projektnamen – **und einen auf das Benutzerprofil selbst**, der jeden Pfad darunter einschließt. Rest der Umbenennung, und ein Befund dazu | gelesen |
| **V8** | 🔴 **Drei `Geplant`-Abschnitte in `docs/ROADMAP.md` nennen ein Ziel-Release, das die Gegenwart überholt hat** – `~0.68.0` (erledigt mit `0.88.0`), `1.1.0` (steht in der Releasetabelle derselben Datei auf `1.3.0`) und `1.2.0` (ausgeliefert, Posten nicht gefahren) | gezählt; Abschnitt 4 |
| **V9** | 🟢 Validator `0 Fehler, 0 Warnungen` über **84** Prüfungen; Arbeitsbaum sauber, kein offener Antrag, kein Restbranch | `validate-framework.py`, `git` |

🔴 **Keine Prüfung erreichte V7 oder V8.** 🔴 **Und V4 war ein Meßfehler des Durchgangs selbst** – siehe Abschnitt 5.

## 3. Die Erhebung – zehn Messungen am Prompt-Eingang

**Das Meßmittel ist neu und kostet nichts.** `codex debug prompt-input` gibt die
Entwickler- und Nutzernachrichten aus, die der Client der nächsten Anfrage voranstellt –
ohne eine Anfrage zu stellen. Das ist bei diesem Client die Entsprechung der Mitschrift,
mit der `0.86.0` das Pack `devin-desktop` gemessen hat, **und sie ist billiger:** die
Mitschrift entsteht aus einem Lauf, dieser Ausdruck aus keinem.

🔴 **Für die Isolation trägt ein eigenes `CODEX_HOME` im Ablagebereich.** Keine Messung
dieses Abschnitts hat die Konfiguration des Arbeitsplatzes angefaßt – die
Vertrauenseinträge, an denen die Hälfte der Befunde hängt, sind in einem zweiten,
wegwerfbaren Benutzerverzeichnis gesetzt und wieder gefallen.

| # | Befund | Beleg |
|---|---|---|
| **E1** | 🔴 **`AGENTS.override.md` verdrängt `AGENTS.md` VOLLSTÄNDIG.** Liegt die Datei im Projekt, steht die Wurzel-Anweisung des Frameworks in **keiner** Nachricht der Sitzung | Sonde und **Gegenprobe**: mit Overlaydatei trägt der Prompt `SONDE-OVERRIDE` und nicht `SONDE-AGENTS-ROOT`; ohne sie genau umgekehrt |
| **E2** | 🔴 **Die gesamte projektlokale Schicht lädt nur bei eingetragenem Vertrauen.** `.codex/config.toml`, Hooks und Exec-Policies bleiben ohne einen `trust_level`-Eintrag in der **Benutzer**konfiguration wirkungslos | A/B mit zwei Benutzerverzeichnissen, identisches Projekt: mit Eintrag greift das Projektmodell, ohne Eintrag der Benutzerstandard |
| **E3** | 🔴 **Und sie kann LOCKERN.** `approval_policy = "never"` und `sandbox_mode = "danger-full-access"` im Projekt schlagen den Benutzerstandard – gemessen: `approval policy Never`, `filesystem sandbox unrestricted` | derselbe A/B-Lauf, `codex doctor` |
| **E4** | 🔴 **Die Pfadrechteschicht kennt KEINE Muster.** Die Schlüssel sind Pfade und müssen absolut sein, mit `~/` beginnen oder ein Sonderziel sein (Projektwurzel, Arbeitsbereich, Temporärverzeichnis) | Abweisung: *filesystem path … must be absolute, use `~/…`, or start with `:`* |
| **E5** | 🔴 **Auf diesem Arbeitsplatz kann der Sandkasten `deny`-Leserechte GAR NICHT durchsetzen – und der Client läuft dann nicht** | Abweisung: *windows unelevated restricted-token sandbox cannot enforce deny-read restrictions directly; refusing to run unsandboxed* |
| **E6** | 🔴 **Hooks tragen ein Vertrauensmodell über einen HASH**, und es gibt einen Schalter, der es übergeht (`--dangerously-bypass-hook-trust`) | Konfigurationsschema aus dem Binär; Befehlszeilenhilfe |
| **E7** | ⚠️ **Das Benutzerverzeichnis des Clients führt eine eigene `AGENTS.md`** – eine Anweisungsquelle außerhalb des Projekts, die in jede Sitzung lädt | Sonde `SONDE-GLOBAL-AGENTS-MD` im Prompt |
| **E8** | 🟢 **Skills laden projektlokal aus zwei Ablagen** (`.codex/skills/` und `.agents/skills/`); eine dritte, naheliegende (`skills/` an der Projektwurzel) **nicht**. Die Menge ist **mit Herkunft vollständig aufzählbar** – der Prompt führt eine Tabelle der Skillwurzeln | drei Sonden an drei Orten, eine davon negativ |
| **E9** | ⚠️ **Regeldateien mit Ladebedingungen gibt es nicht.** Der Client kennt eine Anweisungsdatei je Verzeichnisbaum; eine Datei im Unterverzeichnis steht **nicht** vorab im Kontext | Sonde `SONDE-NESTED-AGENTS` fehlt im Prompt |
| **E10** | 🟢 **Ein projektlokal nicht unterstützter Schlüssel wird BENANNT**, nicht verschwiegen | Startmeldung: *Ignored unsupported project-local config keys … : notify* |

### 3.1 Was daraus für die Fähigkeitsmatrix folgt

| Zeile | Lage nach der Erhebung |
|---|---|
| **R1** (Wurzel-Anweisung wird ungefragt geladen) | 🔴 **Bedingt.** Eine Datei daneben hebt sie auf (E1). ➡️ *Eine Wurzel-Anweisung, die eine ungeprüfte Datei im selben Verzeichnis ersetzen kann, ist keine Ebene 1 – sie ist ein Standard.* |
| **B1** (Berechtigungen liegen versioniert im Repositorium) | 🔴 **Bedingt.** Die Datei liegt versioniert im Projekt und **lädt nur, wenn der Arbeitsplatz das Projekt vertraut** (E2) |
| **B3** (Lesezugriff auf Secret-Dateien per **Pfadmuster** verweigerbar) | 🔴 **In seiner Musterform nicht abbildbar** (E4) – und auf diesem Betriebssystem im gegebenen Sandkastenmodus **gar nicht** (E5). **B3 ist eine Kernzusage**, damit greift `clients/README.md` Abschnitt 4: Begründung im Pack, Ausnahme im Overlay, Freigabe durch `<SECURITY_CONTACT>` |
| **B9** (nutzerlokale Konfiguration kann nur verschärfen) | 🔴 **Spiegelbild gemessen:** Hier lockert die **projektlokale** Konfiguration den **Benutzer**standard (E3) |
| **H1/H2** (Prüfung vor dem Werkzeugaufruf, blockierend) | ⚠️ **Vorhanden und bedingt.** Der Mechanismus blockiert, **aber ein nicht vertrauter Hook läuft nicht** (E6) – und jede Hebung des Frameworks ändert den Hash. *Ein Schutz-Hook, der nicht läuft, blockiert nichts* (AP2-CC-13) |
| **R2/R3** (Ladebedingungen, Bindung an Dateimuster) | ⚠️ **Andere Gestalt** (E9): Geltungsbereich ist der Verzeichnisbaum, nicht ein Muster |
| **S5** (Skills vollständig aufzählbar samt Herkunft) | 🟢 **Gemessen erfüllt** (E8) |

## 4. Der Befund am eigenen Plan (V8)

`docs/ROADMAP.md` führt drei Abschnitte der Form
`### Geplant: <Posten> – Ziel-Release <Version>`. **Alle drei nennen eine Version, die
`VERSION` erreicht oder überschritten hat:**

| Abschnitt | Ziel-Release laut Überschrift | Wirklichkeit |
|---|---|---|
| Die Umbenennung auf `Koolie` | `~0.68.0` | 🔴 **erledigt mit `0.88.0`** – der Abschnitt heißt seit **fünfzehn** Releases *„Geplant"* |
| Client Pack `openai-codex` | `1.1.0` | 🔴 **Die Releasetabelle derselben Datei führt ihn auf `1.3.0`** – zwei Stellen, rund 1.280 Zeilen auseinander, mit verschiedenen Zahlen |
| Projekt-Overlays als Installationsparameter | `1.2.0` | 🔴 **`1.2.0` ist ausgeliefert, der Posten nicht gefahren** |

➡️ ***Eine Zielangabe ist eine Zahl, die vor ihrem Gegenstand geschrieben wird*** – die
Bauform von Prüfung 83, hier an der **Planseite** derselben Datei statt an der
Chronikseite. 🔴 **Und die Verschiebungen sind je einzeln ausgewiesen worden** (D-127,
D-339); **keine von ihnen hat die Überschrift angefaßt**, weil die Releasetabelle als
der eine Ort galt. *Wer eine Zahl an zwei Stellen führt, pflegt eine.*

## 5. Der Befund, den es nicht gab – und warum er trotzdem hier steht (V4)

🔴 **Der erste Anlauf dieses Durchgangs hat gemeldet, die Word-Fassung stehe auf
`v1.1.0`, während `VERSION` auf `1.2.0` stand.** Daraus wurde ein dritter Preis für
`K-110` abgeleitet, und daraus ein Decision Record.

🟢 **Es war falsch.** `build/out/` führt `Koolie_v1.2.0_claude-code.docx` und
`Koolie_v1.2.0_devin-desktop.docx`; Schritt 3 von Abschnitt 4.1 ist bei `1.2.0`
**ausgeführt worden**.

🔴 **Die Ursache ist gemessen: Die Verzeichnisliste war auf zehn Zeilen beschnitten**,
und die beiden Träger standen auf Zeile elf und zwölf. Die Liste war nicht falsch – sie
war **kürzer als ihr Gegenstand**, und die Abwesenheit einer Zeile wurde als Abwesenheit
einer Datei gelesen.

➡️ ***Eine Messung, die ihre Ausgabe beschneidet, mißt die Beschneidung.***
➡️ ***Ein Vorhandensein belegt sich selbst, ein Fehlen nicht*** – derselbe Satz, den
dieser Antrag in Abschnitt 3 als **Stärke** des neuen Meßmittels führt, hat hier gegen
die eigene Messung gearbeitet.

🟢 **Gefunden hat es der Bau selbst.** Erst als Schritt 3 dieses Releases die
Erzeugnisse schrieb, stand die vollständige Liste da. ➡️ ***Der Vorgang findet, was
seine Beschreibung übersieht.***

🔴 **Der Befund bleibt gebucht, statt gestrichen zu werden.** D-305 hat denselben Fall
schon einmal aufgenommen – dort hatte D-301 *„einen Verlust gebucht, den es nicht
gab"* –, und genau diese Buchungen sind der Grund, warum dieses Repositorium seine
Fehlerarten kennt. 🟢 **Was sachlich bleibt:** `K-110` ist **nicht** ein drittes Mal
angefallen; der Verfahrensschritt aus D-332 hat mit `1.2.0` gehalten.

## 6. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | Wird das Pack in diesem Release gebaut – oder erst die Erhebung gebucht? | 🔴 **Erst die Erhebung.** `1.3.0` ist der **Erhebungsdurchgang**, der Bau rückt auf `1.4.0`. **Drei der zehn Befunde ändern die Bauform des Packs** – die musterlose Pfadrechteschicht (E4), das Vertrauensmodell über der ganzen projektlokalen Schicht (E2/E6) und die verdrängbare Wurzel-Anweisung (E1). Ein Pack, das davor entsteht, entsteht zweimal | ⚠️ **Der Releaseplan rückt zum ZWEITEN Mal in Folge um eins** – Overlay auf `1.5.0`, Installationsbibliothek auf `1.6.0`. **Ausgewiesen statt stillschweigend**, wie D-339. 🟢 **Das Muster ist erprobt:** `0.81.0` Vorbedingungen → `0.82.0` Herrichtung → `0.83.0` Meßtag – drei Nummern für einen Posten |
| **E2** | Bekommt der Befund am eigenen Plan (V8) eine Prüfung? | **Prüfung 85:** Jede Überschrift eines `Geplant`-Abschnitts in `docs/ROADMAP.md`, die ein Ziel-Release nennt, wird gegen `VERSION` gehalten. Nennt sie eine Version, die erreicht oder überschritten ist, ist das ein **Fehler**. Und die drei vorgefundenen Abschnitte werden berichtigt | ⚠️ **Grenze, benannt: sie mißt die ZIELANGABE, nicht den Stand des Postens.** Ein Abschnitt, dessen Ziel in der Zukunft liegt, kann längst erledigt sein und kommt durch – dieselbe Bauform wie Prüfung 77 (*Version, nicht Inhalt*) und 82 (*Behauptung, nicht Tatsache*); `K-116` führt die Frage weiter. ⚠️ **Preis:** Wer einen Posten verschiebt, faßt die Überschrift an – und genau das ist der Zweck |
| **E3** | `K-115` ins Register – und die Antwort auf seine drei Fragen? | **Ja, und Abschnitt 4.1 Schritt 2 bekommt den fünften Handgriff: im übernehmenden Projekt committen.** Frage (1) *ja*; Frage (2) *nein* – der Git-Stand eines Projekts außerhalb des Repositoriums ist für keine Prüfung erreichbar (dieselbe Grenze wie D-331 und D-299); Frage (3) *nein*, die Bestandsliste führt weiter die Version und nicht den Commit: ein Commit-Verweis in einem Träger, den beide Projekte als Kopie tragen, wäre in jeder Kopie ein anderer | ⚠️ **Wieder ein Verfahrensschritt statt einer Prüfung** – und V4 desselben Durchgangs mißt gerade, was das wert ist. 🟢 **Der Unterschied zu V4: dieser Schritt hat seinen Gegenstand IM Repositorium des übernehmenden Projekts und ist dort sichtbar**, während ein nicht gebautes Erzeugnis nirgends fehlt |
| **E4** | Was folgt aus V4, nachdem er sich als Meßfehler erwiesen hat – streichen oder buchen? | 🔴 **Buchen.** D-345 hält fest, daß die Meldung aus einer **beschnittenen Verzeichnisliste** kam: *Eine Messung, die ihre Ausgabe beschneidet, mißt die Beschneidung.* D-305 hat denselben Fall schon einmal aufgenommen – dort hatte D-301 *„einen Verlust gebucht, den es nicht gab"*. 🟢 **Sachlich bleibt:** `K-110` ist **nicht** ein drittes Mal angefallen, und die Erzeugnisse dieses Releases werden gebaut und im Erzeugnis nachgezählt | ⚠️ **Keine neue Prüfung, und die erste Frage von `K-110` ist trotzdem beantwortet – mit nein:** Eine Prüfung gegen ein Erzeugnis unter `build/out/` wäre im Framework nach dem Bau grün und in jeder Installation rot (D-299). ⚠️ **Die Lehre hat Reichweite über diesen Fall hinaus:** Der Prüfapparat schneidet an vielen Stellen Ausgaben ab – **eine Zählung gehört gezählt, nicht gelistet** |
| **E5** | Einstufung | **MINOR.** Eine neue Prüfung ist eine neue Regel, und Abschnitt 4.1 bekommt einen Handgriff. **Kein Overlay-Bruch** – kein Träger des Overlays ändert seine Gestalt | – |

## 7. Umsetzung

1. **Prüfung 85** in `validate-framework.py`, mit zwei Sonden und **zwei** Gegenproben in
   `probe-pruefungen.py`. Die zweite Gegenprobe ist die, die man weglassen würde: eine
   Zielangabe **in der Zukunft** muß durchlaufen – sonst mißt die Prüfung die
   Schreibweise und nicht die Sache.
2. `docs/ROADMAP.md`: die drei `Geplant`-Abschnitte berichtigt, Releasetabelle um `1.3.0`
   ergänzt und `1.4.0` bis `1.6.0` gerückt, Standüberschrift auf `1.3.0`.
3. `RELEASE_PROCESS.md` Abschnitt 4.1 Schritt 2: fünfter Handgriff; `checklists/11`
   ebenso.
4. `DECISION_LOG.md`: **D-341** bis **D-345**, `K-115` und `K-116`; `K-110` im Zuschnitt
   verengt.
5. `TEST_CATALOG.md`: Prüfung 85 eingetragen.
6. `CHANGELOG.md`, `VERSION`, `ADOPTION_REGISTRY.md`.
7. Protokoll mit allen zehn Messungen und ihren Gegenproben.
8. 🔴 **Die Erhebung faßt die Konfiguration des Arbeitsplatzes nicht an** – alle Messungen
   laufen gegen ein eigenes `CODEX_HOME` im Ablagebereich, und der Ablagebereich wird
   danach geräumt.
9. 🔴 **Die Übergabe wird VOR dem Abnahmelauf gehoben** (Falle 1 aus `1.2.0`); nur die
   Laufzeiten stehen unterhalb der Trennlinie (D-94).
10. Validator und Sondenlauf in **beiden** Kodierungsumgebungen (D-49); Heben der
    übernehmenden Projekte **vor** dem Release-Commit (D-330) und als **letzter** Eingriff
    in den Kern (D-333), **mit Commit dort** (E3).

## 8. Entscheidung

🟢 **Angenommen am 2026-09-23, E1 bis E5 wie vorgelegt.**

| # | Entscheidung | Decision Record |
|---|---|---|
| E1 | `1.3.0` ist der Erhebungsdurchgang; der Packbau rückt auf `1.4.0` | **D-341** |
| E2 | Prüfung 85 – die Zielangabe eines Planabschnitts gegen `VERSION` | **D-342** |
| E3 | `K-115` beantwortet; Abschnitt 4.1 Schritt 2 bekommt den fünften Handgriff | **D-343** |
| E4 | Die Erhebung eines Client Packs ist kontingentfrei, solange sie am Prompt-Eingang mißt | **D-344** |
| E5 | V4 war ein Meßfehler des Durchgangs selbst und wird als solcher gebucht | **D-345** |

Neue Klärungspunkte: `K-115` (im Register, mit Antwort), `K-116` (erreicht eine Prüfung
den **Stand** eines Planpostens, nicht nur seine Zielangabe?)
🔴 **Und ein dritter, gefallen beim Heben selbst:** `K-117` – das `.gitignore` von
`devpacks/otp-generator` verschluckt **42** der 525 ausgelieferten Kerndateien,
darunter die gesamte Quelle des Hauptdokuments. Gemessen in Schritt 2 dieses
Releases, drei Fragen vorgelegt, hier nicht entschieden.
