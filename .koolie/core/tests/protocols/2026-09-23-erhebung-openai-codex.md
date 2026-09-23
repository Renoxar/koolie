# Protokoll: Die Erhebung zu `openai-codex` – der Client, dessen Wurzelanweisung eine Datei daneben ersetzt

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-23 |
| Release | **`1.3.0`** |
| Änderungsantrag | `CR-2026-132` |
| Art | **Arbeitsprotokoll.** Gegenstand sind die Erhebung zum Client Pack `openai-codex` (Schritte 2, 6 und 7 aus `clients/README.md` Abschnitt 5), der Vorbedingungsdurchgang davor und eine neue Prüfung |
| Prüfmittel | `codex debug prompt-input` und `codex doctor` gegen ein **eigenes `CODEX_HOME` im Ablagebereich**; dazu das Konfigurationsschema aus dem Binär, der Validator und der volle Sondenlauf in beiden Kodierungsumgebungen |
| Geprüfte Clientversion | **`0.156.1`** – **vor** dem Erheben festgeschrieben (D-117, D-202) |
| Ergebnis | 🟢 **Zehn Befunde, sechs davon mit Gegenprobe, null Kontingent.** 🔴 **Drei ändern die Bauform des Packs, und deshalb rückt sein Bau auf `1.4.0`** |

> 🔴 **Dies ist kein Abnahmeprotokoll des Testkatalogs** und trägt deshalb keinen
> Abschnitt *Gegenzeichnung* (D-319, Zuschnitt von Prüfung 80). Es berichtet eine
> Messung und trägt seinen Beleg in sich.

---

## 1. Der Anlaß

Der Wiederaufnahmepunkt zu `1.2.0` nennt als nächsten Posten das **Client Pack
`openai-codex`** – die neun Schritte aus `clients/README.md` Abschnitt 5. **Drei dieser
neun Schritte sind Erhebungen**, und sie stehen vor dem ersten geschriebenen
Trägerbyte: die Pfadabbildung (Schritt 2), die Semantikabbildung (Schritt 6) und die
Auskunft über Quellen außerhalb des Projekts (Schritt 7).

Vor dem ersten Handgriff stand der Vorbedingungsdurchgang – zum **einundzwanzigsten**
Mal in Folge.

## 2. Der Vorbedingungsdurchgang

| # | Befund | gemessen an |
|---|---|---|
| **V1** | 🟢 Die Tabelle *Nächste freie Kennungen* stimmt – **zum zweiten Mal in Folge** | 340 `D`-Registerzeilen bis `D-340`, 112 `K`-Zeilen bis `K-114`, `CR-2026-131` vergeben, `G-20`, `UEB-31`; alle fünf Gattungen nachgezählt |
| **V2** | 🟢 Das Codex-Konto ist `plus` | `id_token`, Feld `chatgpt_plan_type` |
| **V3** | 🟢 Die geprüfte Clientversion ist **vor** dem Erheben festgeschrieben: `0.156.1` | `codex --version`; `codex doctor` meldet *latest version status: current version is not older* |
| **V4** | 🟢 **Die Word-Fassung steht auf `v1.2.0`** – Schritt 3 von Abschnitt 4.1 hat bei `1.2.0` gehalten. 🔴 **Der erste Anlauf dieses Durchgangs hat das Gegenteil gemeldet, und das war ein Meßfehler** | `build/out/` führt `Koolie_v1.2.0_claude-code.docx` und `Koolie_v1.2.0_devin-desktop.docx`; Abschnitt 6 |
| **V5** | 🟢 Bestandsliste in allen drei Trägern byte-gleich auf `1.2.0`; **beide** Projekte tragen die Hebung als Commit | `cmp` über drei Kopien, `git log` in beiden Projekten (`4f09d0a`, `49dc116`) |
| **V6** | 🟢 **Die Nennungen von `1.2.0` sind vollständig, und zwar in ZWEI beschreibenden Trägern** | `D-335` bis `D-340` je Träger gezählt: `CHANGELOG.md` sechs, `CR-2026-131` sechs, ROADMAP als Spanne, Protokoll zwei. **`K-112` hat seinen ersten Fall nicht gebracht** |
| **V7** | ⚠️ Die Benutzerkonfiguration des Clients führt weiter einen Vertrauenseintrag auf den **alten** Projektnamen – **und einen auf das Benutzerprofil selbst** | gelesen; der zweite schließt jeden Pfad darunter ein und macht die projektgenauen Einträge gegenstandslos |
| **V8** | 🔴 **Drei `Geplant`-Abschnitte in `docs/ROADMAP.md` nennen ein Ziel-Release, das die Gegenwart überholt hat** | gezählt; Abschnitt 5 |
| **V9** | 🟢 Validator `0 Fehler, 0 Warnungen` über **84** Prüfungen; Arbeitsbaum sauber, kein offener Antrag, kein Restbranch | `validate-framework.py`, `git` |

🔴 **Keine Prüfung erreichte V7 oder V8.** 🔴 **Und V4 war ein Meßfehler des Durchgangs selbst – Abschnitt 6.**

## 3. Das Meßmittel – und warum es nichts kostet

`codex debug prompt-input` gibt die Entwickler- und Nutzernachrichten als JSON aus, die
der Client der nächsten Anfrage voranstellt – **ohne eine Anfrage zu stellen.** Damit
ist ablesbar, was das Modell zu Beginn einer Sitzung sieht: die Wurzel-Anweisung, die
Skillmenge samt Herkunftstabelle, die Umgebungsangaben und das wirksame Rechteprofil.

**Das ist bei diesem Client die Entsprechung der Mitschrift**, mit der `0.86.0` das Pack
`devin-desktop` gemessen hat – **und es ist billiger:** die Mitschrift entsteht aus einem
Lauf, dieser Ausdruck aus keinem.

🔴 **An einer Stelle ist es auch schärfer.** Die Verdrängung der Wurzel-Anweisung (E1)
ist an einer **Abwesenheit** im Prompt erkennbar. Ein Lauf hätte sie nur gezeigt, wenn
das Modell zufällig auf die fehlende Regel gestoßen wäre. ➡️ ***Ein Vorhandensein belegt
sich selbst, ein Fehlen nicht*** – hier läßt sich das Fehlen zum ersten Mal direkt
ablesen.

### 3.1 Die Isolation, und warum sie hier Bedingung war

**Die Hälfte der Befunde hängt an Einträgen in der Benutzerkonfiguration des
Arbeitsplatzes.** Sie dort zu setzen hieße, den Arbeitsplatz zu verändern, um ihn zu
messen. Alle Messungen dieses Abschnitts laufen deshalb gegen ein **eigenes
`CODEX_HOME`** im Ablagebereich, das nur die Anmeldedaten und die jeweils gemessene
Einstellung trägt. **Die Konfiguration des Arbeitsplatzes ist nicht angefaßt worden** –
und damit ist auch nichts über sie gemessen worden.

## 4. Die zehn Befunde

### 4.1 `E1` – eine Datei neben der Wurzel-Anweisung verdrängt sie vollständig

Ein Projekt mit einer Wurzel-Anweisung und einer gleichnamigen Overlaydatei daneben
(`AGENTS.override.md`). Gemessen wurde die **Anwesenheit einer Sondenmarke** im Prompt:

| Lauf | Wurzel-Anweisung im Prompt | Overlaydatei im Prompt |
|---|---|---|
| **Sonde:** beide Dateien vorhanden | 🔴 **nein** | ja |
| **Gegenprobe:** nur die Wurzel-Anweisung | 🟢 **ja** | – |

➡️ ***Eine Wurzel-Anweisung, die eine ungeprüfte Datei im selben Verzeichnis ersetzen
kann, ist keine Ebene 1 – sie ist ein Standard.***

🔴 **Die Folge für `R1` ist nicht redaktionell.** Die Prioritätshierarchie stellt die
Wurzel-Anweisung auf Ebene 1; hier genügt eine Datei im Arbeitsbaum, um sie
**vollständig** zu ersetzen, und nichts meldet es. Ein aufnehmendes Projekt, das die
Overlaydatei in seine `.gitignore` schreibt – der naheliegende Ort für eine persönliche
Fassung –, hätte damit eine unversionierte Ebene 1 je Arbeitsplatz.

### 4.2 `E2` und `E3` – das Vertrauensmodell über der gesamten projektlokalen Schicht

Dieselbe Projektkonfiguration, zweimal gemessen, mit zwei Benutzerverzeichnissen:

| Lauf | Vertrauenseintrag | Modell | Rückfragepolitik | Dateisystem-Sandkasten |
|---|---|---|---|---|
| **A** | 🟢 vorhanden | **aus dem Projekt** | **`Never`** | **ohne Schranken** |
| **B** (Gegenprobe) | 🔴 fehlt | Benutzerstandard | `OnRequest` | eingeschränkt |

🔴 **Zwei Befunde in einer Messung.**

**(E2)** Ohne Vertrauenseintrag lädt die projektlokale Schicht **gar nicht** – und zwar
nicht nur die Konfiguration, sondern nach der Meldung des Clients *„project-local config,
hooks, and exec policies"* zusammen. ➡️ *Ein versionierter Träger, der nicht lädt, trägt
nichts.* **`B1` ist damit bedingt:** Die Berechtigungen liegen versioniert im
Repositorium **und** ihre Wirksamkeit hängt an einem Eintrag außerhalb.

**(E3)** Mit Vertrauenseintrag **lockert** die projektlokale Schicht den Benutzerstandard:
Rückfragen aus, Sandkasten offen. **Das ist das Spiegelbild von `B9`** – dort lautet die
Zusage *„eine nutzerlokale Konfiguration kann nur verschärfen"*; hier verschärft nicht
die nutzerlokale, sondern **lockert die projektlokale**.

⚠️ **Und der Vertrauenseintrag wird üblicherweise einmal und beiläufig erteilt.** Der
Vorbedingungsdurchgang hat auf diesem Arbeitsplatz einen Eintrag auf das
**Benutzerprofil** gefunden (V7), der jeden Pfad darunter einschließt.

### 4.3 `E4` und `E5` – die Pfadrechteschicht kennt keine Muster, und hier gar nichts

Die Rechteprofile des Clients binden Pfade an eine Zugriffsart. **Ein Musterausdruck als
Schlüssel wird abgewiesen:** verlangt sind absolute Pfade, `~/`-Pfade oder Sonderziele
(Projektwurzel, Arbeitsbereich, Temporärverzeichnis).

🔴 **Die Kernzusage `B3` verlangt genau Muster** – `.env`, `*.pem`, `*.key`,
`secrets/**`. Sie ist in dieser Form **nicht abbildbar**.

🔴 **Und auf diesem Arbeitsplatz gar nicht.** Ein Profil mit einer `deny`-Leseregel
führt zur Abweisung *„windows unelevated restricted-token sandbox cannot enforce
deny-read restrictions directly; refusing to run unsandboxed"*. 🟢 **Das Verhalten ist
fail-closed und damit richtig** – der Client läuft lieber nicht, als ungeschützt zu
laufen. ⚠️ **Für das Pack heißt es trotzdem:** `B3` steht in diesem Betriebsmodus auf
`[NICHT ABBILDBAR]`, und die Vorbemerkung des B-Blocks zur Betriebsmodus-Abhängigkeit
(D-35) bekommt einen zweiten Fall – diesmal einen, der nicht vom **Modus**, sondern vom
**Betriebssystem und der Rechtestufe** abhängt.

**`B3` ist eine Kernzusage.** Damit greift `clients/README.md` Abschnitt 4: Begründung
im Pack, dokumentierte Ausnahme im Overlay des aufnehmenden Projekts, und **keine
Inbetriebnahme ohne Freigabe durch `<SECURITY_CONTACT>`.**

### 4.4 `E6` – Hooks tragen ein Vertrauensmodell über einen Hash

Das Konfigurationsschema führt je Hook einen **vertrauten Hash**; die Befehlszeile kennt
einen Schalter, der das Vertrauen übergeht und sich selbst als gefährlich bezeichnet.

➡️ **Die Entsprechung zu D-281 und zu `AP2-CC-13`:** *Ein Schutz-Hook, der nicht läuft,
blockiert nichts.* 🔴 **Und die Bindung an den Hash hat eine Folge, die D-281 nicht
hat:** **Jede Hebung des Frameworks ändert den Hook und damit den Hash.** Ein Projekt,
das nach `install.py --update` nicht erneut vertraut, läuft ab dann **ohne** Schutz-Hook
– und der Validator sieht es nicht, weil die Datei ja da ist.

### 4.5 `E7` bis `E10` – die übrigen vier

| # | Befund | Beleg |
|---|---|---|
| **E7** | Das Benutzerverzeichnis des Clients führt eine **eigene Anweisungsdatei**, die in jede Sitzung lädt | Sonde im isolierten `CODEX_HOME`, im Prompt wiedergefunden |
| **E8** | Skills laden projektlokal aus **zwei** Ablagen; eine dritte, naheliegende an der Projektwurzel **nicht**. Die Menge ist **mit Herkunft vollständig aufzählbar** | drei Sonden an drei Orten, eine davon negativ; der Prompt führt eine Tabelle der Skillwurzeln |
| **E9** | **Regeldateien mit Ladebedingungen gibt es nicht.** Der Geltungsbereich einer Anweisungsdatei ist ihr Verzeichnisbaum; eine Datei im Unterverzeichnis steht **nicht** vorab im Kontext | Sonde im Unterverzeichnis, im Prompt **nicht** wiedergefunden |
| **E10** | Ein projektlokal **nicht unterstützter** Schlüssel wird in einer Startmeldung **benannt** | gemessen mit einem solchen Schlüssel; die Meldung nennt ihn wörtlich |

🟢 **`E8` und `E10` sind gute Nachrichten für das Pack:** `S5` ist gemessen erfüllt, und
ein falsch abgebildeter Konfigurationsschlüssel fällt nicht lautlos aus.
⚠️ **`E9` nicht:** `R2` und `R3` haben eine andere Gestalt, und die Abbildung der
Ladetrigger (`rule_triggers`) braucht eine eigene Auflösung – ein Ladetrigger ohne
Eintrag läßt die Installation scheitern (D-26, D-27).

## 5. Der Befund am eigenen Plan

`docs/ROADMAP.md` führte drei Abschnitte der Form
`### Geplant: <Posten> – Ziel-Release <Version>`:

| Abschnitt | Zielangabe | Wirklichkeit |
|---|---|---|
| Die Umbenennung auf `Koolie` | `~0.68.0` | 🔴 erledigt mit `0.88.0` – **fünfzehn Releases** unter der Überschrift *„Geplant"* |
| Client Pack `openai-codex` | `1.1.0` | 🔴 die **Releasetabelle derselben Datei** führte ihn auf `1.3.0` |
| Projekt-Overlays als Installationsparameter | `1.2.0` | 🔴 `1.2.0` ausgeliefert, Posten nicht gefahren |

➡️ ***Eine Zielangabe ist eine Zahl, die vor ihrem Gegenstand geschrieben wird*** – die
Bauform von Prüfung 83, hier an der **Planseite** derselben Datei statt an der
Chronikseite.

🔴 **Die Ursache ist gemessen:** Beide Verschiebungen des Packpostens sind je einzeln
ausgewiesen worden (D-127 auf `1.1.0`, D-339 auf `1.3.0`), und **keine hat die
Überschrift angefaßt** – die Releasetabelle galt als der eine Ort. ➡️ *Wer eine Zahl an
zwei Stellen führt, pflegt eine.*

### 5.1 Prüfung 85 – vier Einheiten

| Einheit | Gegenstand | Ergebnis |
|---|---|---|
| **Gegenprobe 85a** | die berichtigte ROADMAP läuft durch, und die Prüfung ist dabei nachweislich gelaufen | 🟢 |
| **Gegenprobe 85b** | 🔴 **die, die man weglassen würde:** eine Zielangabe in der **Zukunft** muß durchlaufen | 🟢 |
| **Sonde 85a** | eine Zielangabe, die `VERSION` erreicht hat, wird gemeldet | 🟢 |
| **Sonde 85b** | eine Planüberschrift **ohne** Zielangabe wird gemeldet | 🟢 |

🔴 **Warum Sonde 85b sein muß:** Ohne sie wäre das Streichen der Zahl der billigste Weg,
diese Prüfung loszuwerden – und D-124 hat die Frage schon beantwortet: *ein Posten ohne
Zahl bleibt in diesem Projekt erfahrungsgemäß lange liegen.*

⚠️ **Grenze, benannt, und sie zeigt sich am ersten Fall:** Den erledigten Abschnitt hat
die Prüfung **aus dem falschen Grund** gefangen – weil seine Zahl zufällig auch veraltet
war. Eine Zielangabe `2.0.0` hätte dieselbe Überschrift durchgelassen. ➡️ *Eine Prüfung,
die den richtigen Fall aus dem falschen Grund fängt, ist beim nächsten Fall blind*
(`K-116`).

## 6. Der Befund, den es nicht gab – und der Meßfehler dahinter

🔴 **`V4` lautete im ersten Anlauf: die Word-Fassung steht auf `v1.1.0`, `VERSION` auf
`1.2.0` – Schritt 3 von Abschnitt 4.1 ist bei `1.2.0` nicht ausgeführt worden.** Daraus
wurde ein dritter Preis für `K-110` abgeleitet, und daraus ein Decision Record.

🟢 **Es war falsch.** `build/out/` führt zwölf Träger, darunter
`Koolie_v1.2.0_claude-code.docx` und `Koolie_v1.2.0_devin-desktop.docx`.

🔴 **Die Ursache, gemessen:** Die Verzeichnisliste war auf **zehn Zeilen** beschnitten.
Sieben Erzeugnisse, zwei Verzeichniseinträge und die Summenzeile füllten sie; die beiden
Träger von `1.2.0` standen auf Zeile **elf** und **zwölf**.

| | |
|---|---|
| Was die Liste sagte | sieben Erzeugnisse, das jüngste `v1.1.0` |
| Was im Verzeichnis lag | **elf** Erzeugnisse, das jüngste `v1.2.0` |
| Was gelesen wurde | eine fehlende **Zeile** als fehlende **Datei** |

➡️ ***Eine Messung, die ihre Ausgabe beschneidet, mißt die Beschneidung.***

🔴 **Und der Satz, der es hätte verhindern müssen, steht in diesem Protokoll zwei
Abschnitte weiter oben.** Abschnitt 3 führt ihn als **Stärke** des neuen Meßmittels:
*Ein Vorhandensein belegt sich selbst, ein Fehlen nicht.* Ein Fehlen zu belegen verlangt
eine Messung, die **den ganzen Gegenstand sieht** – und genau das tat diese nicht.

🟢 **Gefunden hat es der Bau selbst.** Erst als Schritt 3 dieses Releases die
Erzeugnisse schrieb, stand die vollständige Liste da. ➡️ ***Der Vorgang findet, was
seine Beschreibung übersieht.***

### 6.1 Warum der Befund gebucht bleibt

🔴 **Weil dieses Repositorium seine Fehlerarten kennt, indem es sie aufschreibt.** D-305
hat denselben Fall schon einmal aufgenommen – dort hatte D-301 *„einen Verlust gebucht,
den es nicht gab"*. **D-345 hält ihn fest**, und der Zuschnitt ist diesmal enger als der
Einzelfall: **Der Prüfapparat schneidet an vielen Stellen Ausgaben ab.** *Eine Zählung
gehört gezählt, nicht gelistet.*

🟢 **Was sachlich bleibt:** `K-110` ist **nicht** ein drittes Mal angefallen. Der
Verfahrensschritt aus D-332 hat mit `1.2.0` gehalten – und die Erzeugnisse dieses
Releases sind gebaut und im Erzeugnis nachgezählt (Abschnitt 9).

## 7. Was für `1.4.0` entschieden werden muß, bevor ein Träger entsteht

| # | Frage | Woran sie hängt |
|---|---|---|
| **1** | Bekommt `clientmap.py` eine **zweite Ausgabeform**? Die heutige rendert Körbe aus `Werkzeug(Muster)`-Regeln; dieser Client bindet **Pfade an Zugriffsarten** und Befehle an eigene Regeldateien | `E4`. Betrifft `B2` bis `B6`, also **vier Kernzusagen** |
| **2** | Wie wird das **Vertrauensmodell** im B-Block ausgewiesen? Es steht über der ganzen projektlokalen Schicht, nicht nur über den Hooks | `E2`, `E6`. Betrifft `B1`, `H1`, `H2` – und die Vorbemerkung zur Betriebsmodus-Abhängigkeit (D-35) |
| **3** | Wie steht die **verdrängbare Wurzel-Anweisung** in `R1`? Als `[TEXTUELL]` mit Begründung, oder als `[TECHNISCH]` mit benannter Bedingung? | `E1`. **Keine der beiden vorhandenen Packzeilen hat diese Gestalt** |
| **4** | Wie werden die **Ladetrigger** abgebildet, wenn es keine gibt? `rule_triggers` läßt einen Trigger ohne Eintrag die Installation abbrechen (D-26, D-27) | `E9` |
| **5** | Trägt das Pack **beide** Skillablagen oder eine? | `E8` |

🔴 **Zwei der betroffenen Zeilen sind Kernzusagen** (`B3`, `B9`) – nach
`clients/README.md` Abschnitt 4 brauchen sie eine Begründung im Pack, eine dokumentierte
Ausnahme im Overlay und eine Freigabe durch `<SECURITY_CONTACT>`. **Das ist keine
Fußnote, und deshalb rückt der Bau** (D-341).

## 8. Ein Befund beim Heben selbst – `K-117`

Schritt 2 des Verfahrens hat einen eigenen Befund geliefert, und er hat mit `openai-codex`
nichts zu tun.

| Projekt | Kerndateien im Arbeitsbaum | davon versioniert | Differenz |
|---|---|---|---|
| `devpacks/otp-generator` | 525 | 🔴 **483** | 🔴 **42** |
| `devpacks/test-devin-framework` | 525 | 🟢 521 | 4 (Bytecode) |

🔴 **Die Ursache ist eine Zeile im `.gitignore` des Projekts:** `build/` trifft auch
`.koolie/core/build/` – und damit **die gesamte Quelle des Hauptdokuments**, die das
Framework ausliefert.

➡️ ***Ein Kern, der ausgeliefert, aber nicht versioniert wird, ist beim nächsten Klonen
dieses Projekts unvollständig*** – und der Validator sieht es nicht, weil er den
**Arbeitsbaum** mißt. ⚠️ **Prüfung 81 fängt es ebenfalls nicht:** Sie mißt die
Zeilenendeform der **verfolgten** Träger, also gerade derer, die noch da sind.

**Als `K-117` aufgenommen, drei Fragen vorgelegt, in diesem Release nicht entschieden.**

🔴 **Und der Eintrag hat den benannten Preis von D-330 fällig gemacht:** Er ist ein
Kerneingriff **nach** dem Heben, also mußte **erneut gehoben** werden. *Heben und Commit
gehören als Paar* – hier zum zweiten Mal gemessen.

## 9. Abnahme

| Gegenstand | Ergebnis |
|---|---|
| Validator (84 → **85 Prüfungen**) | *(siehe Abnahmezeile der Übergabe)* |
| Sondenlauf, beide Kodierungsumgebungen | *(siehe Abnahmezeile der Übergabe)* |
| Zeilengleicher Vergleich nach D-49 | *(siehe Abnahmezeile der Übergabe)* |
| Erzeugnisse der Lieferung, je Client Pack | 🟢 **gebaut und im Erzeugnis nachgezählt:** `Koolie_v1.3.0_claude-code.docx` und `Koolie_v1.3.0_devin-desktop.docx`, je **8 Diagramme** eingebettet und **36** Fundstellen der Version im Dokumentkörper; das Hauptdokument mit **13.041** Zeilen (`claude-code`) beziehungsweise **13.123** (`devin-desktop`) |
| Übernehmende Projekte | gehoben **und dort committet** (D-343) |

---

## Anhang: Was dieses Protokoll nicht belegt

🔴 **Der Prompt-Eingang zeigt, was das Modell SIEHT, nicht, was die Engine
DURCHSETZT.** Jede Zeile des B-Blocks braucht weiterhin einen Lauf gegen eine reale
Installation; `[TECHNISCH]` bleibt daran gebunden (`clients/README.md` Abschnitt 4,
D-344).

🔴 **Und alle Messungen liefen gegen ein isoliertes Benutzerverzeichnis.** Über die
Konfiguration dieses Arbeitsplatzes ist damit **nichts** gemessen – außer dem, was der
Vorbedingungsdurchgang gelesen hat (V7).
