# AP2: die Zielversion von Devin Desktop, und sechs Marker, deren Beleg im Haus lag

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-16 |
| Framework-Version | `0.52.0` (Stand `main`, Commit `dabbbf7`); umgesetzt mit `0.53.0` |
| Gegenstand | `AP2` für das Client Pack `devin-desktop`: die verbindliche Zielversion festlegen, das Pack gegen sie erheben, die beiden Steckbriefzellen füllen. Mittelbar Kriterium 1 und Kriterium 3 von D-11 – gezählt von Prüfung 46 zu Beginn: **29** und **1** |
| Anlass | Kandidat 1 der Übergabe, und der einzige Träger, der nach 0.52.0 noch auf `entwurf` steht. Er sperrt sich über zwei Ausfüllschlitze seines Steckbriefs, nicht über seine acht Marker (D-110) |
| Antrag | `CR-2026-075`, D-112 bis D-114, `K-40` und `K-41` neu |
| Prüfmethode | Erhebung an der **installierten** Fassung des Clients auf diesem Arbeitsplatz, nicht an seiner Dokumentation. Je Marker: Gegenstand benennen, messen, Ergebnis gegen den Marker halten. Für die Träger die fünf Bedingungen (a) bis (e) aus `framework/core/01-governance.md` Abschnitt 5 Punkt 3, Zeile `entwurf → pilot` |
| Ausgeführte Befehle | siehe Abschnitt 3 – acht Läufe, sämtlich **ohne Sitzungskontingent** |
| Ergebnis | **Die Zielversion ist als Spanne festgelegt (D-112, D-113), sechs Markerfundstellen sind aufgelöst, und `clients/devin-desktop/CLIENT_PACK.md` ist abgenommen.** Kriterium 1 fällt von **29 auf 23**, Kriterium 3 von **1 auf 0**. Vier Nebenbefunde sind angefallen, zwei davon in Klärungspunkte überführt |

## 1. Die Vorentscheidung – und sie ist gegen den Vorschlag ausgefallen

Die Übergabe hat diesem Vorgang eine Bedingung vorangestellt und sie ausdrücklich dem
Menschen zugeschrieben: **welche Devin-Desktop-Version ist die verbindliche Zielversion?**
Vorgelegt wurden drei Auflösungen. Empfohlen war die **Punktversion** – die installierte
Fassung, gegen die schon zweimal gemessen worden ist. Entschieden wurde die **Spanne**.

**Die Entscheidung hat sich binnen eines Befehls als die richtige erwiesen**, und der Beleg
steht in Abschnitt 6: Das Schwesterpack `claude-code` nennt als geprüfte Clientversion
`2.1.267`; installiert ist auf demselben Arbeitsplatz **`2.1.273`**. Sechs Patchstände
Abstand, entstanden ohne Zutun; die Zelle steht seit 0.13.0 unverändert, über vierzig
Releases. **Eine Punktversion veraltet
zwischen zwei Releases des Frameworks, weil der Client sich selbst aktualisiert und das
Framework seinen Takt nicht setzt.**

> **Die Lehre, und sie ist der Grund für D-113:** Eine Angabe, die das Framework nicht
> taktet, gehört nicht als Punktwert in einen Steckbrief. Sie gehört als **Spanne** hinein,
> mit dem gemessenen Punktwert daneben – die Spanne sagt, wofür das Pack gilt, der
> Punktwert sagt, woran gemessen wurde. **Beides in eine Zelle zu schreiben, heißt eine der
> beiden Aussagen zu verlieren**, und verloren gegangen ist bisher die erste.

**Der Preis der Spanne ist benannt und er ist nicht bezahlt** (Abschnitt 8): Eine Spanne ist
eine Behauptung über Versionen, die nie gemessen wurden, und **keine Prüfung rechnet nach,
ob der gemessene Punktwert in ihr liegt.** Das ist `K-40`.

## 2. Der Gegenstand: zwei Schlitze und zehn Marker

`clients/devin-desktop/CLIENT_PACK.md` steht nach 0.52.0 als einziger Modulträger auf
`entwurf`. Abschnitt 11 des Abnahmeprotokolls vom 2026-09-15 hat den Gegenstand je
Fundstelle erhoben; diese Erhebung hat ihn nachgezählt und **eine Fundstelle mehr gefunden
als die Übergabe nannte.**

| Was | Wo | Anzahl |
|---|---|---|
| Ausfüllschlitze, die den Übergang sperren | `CLIENT_PACK.md` Z11, Z12 | **2** |
| `VERIFY`-Marker im Pack | `CLIENT_PACK.md` Z24, Z26, Z27, Z82, Z94, Z101, Z116, Z136 | **8** |
| `VERIFY`-Marker im `root-template/` des Packs | `root-template/.devin/README.md` Z10, Z12 | **2** |
| `VERIFY`-Marker in der **Quelle** der MCP-Vorlage | `framework/runtime/mcp-config.example.json` | **1** |

**Die elfte Fundstelle ist die interessante.** Die Übergabe nannte „die acht Marker des
Packs plus die zwei in dessen `root-template/`" – zehn. Die Vorlage
`.devin/mcp_config.json.example`, die das Pack in Z26 nennt, liegt aber **nicht** im
`root-template/`: Sie wird von `install.py` aus `framework/runtime/mcp-config.example.json`
erzeugt, und **diese Quelle trägt denselben Marker ein drittes Mal.**

> ⚠️ **Und hier ist mir die Lehre von 0.51.0 ein zweites Mal passiert, im selben Vorgang.**
> Ein `grep -n "mcp" leitwerk-core/install.py` meldete **null Treffer**, und daraus wurde
> geschlossen, die Datei werde gar nicht ausgeliefert – ein Befund „das Pack nennt eine
> Vorlage, die es nicht gibt". **Er war falsch.** Die frische Installation in Abschnitt 3
> legte sie an. `install.py` kopiert das Verzeichnis `framework/runtime/` als Ganzes und
> nennt die Datei deshalb nirgends beim Namen. **Eine Null ist erst ein Messwert, wenn eine
> Ergebniszeile daneben steht** – zum vierten Mal in diesem Repositorium, und diesmal hat
> der Kontrolllauf sie gefangen, nicht das Auge.

## 3. Die Erhebung – acht Läufe, kein Kontingent

Alle Läufe auf dem Arbeitsplatz, auf dem das Framework entwickelt wird. **Keiner startet
eine Sitzung**, also fällt kein Devin-Kontingent an. Die Ausgaben sind unverändert
wiedergegeben.

| Lauf | Befehl | Ergebnis |
|---|---|---|
| **E1** | `devin.exe --version` | `devin 3000.10.21 (611c1cba)` |
| **E2** | `(Get-Item …\Programs\Devin\Devin.exe).VersionInfo` | `FileVersion 3.9.19`, `ProductVersion 3.9.19` |
| **E3** | `claude --version` | `2.1.273 (Claude Code)` – für Abschnitt 6 |
| **E4** | `devin.exe doctor` | `1 check(s): 1 passed, 0 warning(s), 0 failure(s)` – **und das ist der Messwert, nicht die Bestätigung:** Der Selbsttest des Clients prüft genau einen Gegenstand (`custom subagent profiles`). Er taugt **nicht** als Schemaprüfung für `config.json` |
| **E5** | `devin.exe mcp add --help` | Drei Ablageorte, ausdrücklich benannt: `local` → `.devin/mcp_config.local.json` (**Standard**), `project` → `.devin/mcp_config.json`, `user` → `~/.config/devin/mcp_config.json` |
| **E6** | `devin.exe mcp add probe-stdio --scope project -- python -m http.server` in einem leeren Verzeichnis | `✓ Added MCP server 'probe-stdio' to project config`; angelegt wurde `.devin/mcp_config.json` mit dem Inhalt unten |
| **E7** | `install.py --client devin-desktop --root <leeres Verzeichnis>` | 78 Dateien außerhalb von `leitwerk-core/`; darunter `.devin/mcp_config.json.example` – **der Kontrolllauf, der den Fehlschluss aus Abschnitt 2 aufgehoben hat** |
| **E8** | Auswertung von `devpacks/lw-tech/ap2-hook-aufzeichnung.jsonl` (5 Sätze, 2026-09-11) | je Satz `"umgebung": {"DEVIN_PROJECT_DIR": "gesetzt: zeigt auf dieses Projekt", …}` |

**Der Messwert aus E6, unverändert:**

```json
{
  "mcpServers": {
    "probe-stdio": {
      "command": "python",
      "args": ["-m", "http.server"],
      "transport": "stdio"
    }
  }
}
```

**Die Enthaltung zu E6.** Derselbe Lauf sollte zusätzlich einen `http`-Server anlegen
(`--transport http https://example.invalid/mcp`). Er ist nach zwei Minuten **ohne Ausgabe
abgebrochen** worden – der Befehl versucht offenbar, den Server zu erreichen. **Der
`http`-Fall ist deshalb nicht gemessen**, und die Auflösung von Z26 sagt das. Ein Ergebnis,
das nicht vorliegt, wird hier nicht aus dem `--help`-Text abgeleitet.

## 4. Auflösung je Marker

Die Auflösung folgt der Regel, die dieses Repositorium seit 0.4.0 anwendet: **Ein Marker
wird durch einen Messwert ersetzt, auch wenn der Messwert die Zusage verschlechtert.**
Sechs der elf Fundstellen sind damit erledigt, fünf bleiben.

| Fundstelle | Gegenstand | Beleg | Auflösung |
|---|---|---|---|
| `CLIENT_PACK.md` Z24 | Schemadetails von `.devin/config.json` | **Beide Hälften in Sitzungen gemessen:** der `hooks`-Block am 2026-09-11 (`2026-09-11-AP2-devin-desktop.md`, `AP2-DD-10`: aus `hooks.v1.json` läuft kein Hook, aus `config.json` sofort), der `permissions`-Korb `deny` am 2026-09-14 (`2026-09-14-erhebung-devin-werkzeuge.md`, Läufe P4 und W1 – der Client weist ab und nennt dabei selbst die Quelle: *„denied by a deny rule in the project settings"*) | **aufgelöst**, mit benannter Grenze: Gemessen ist der Korb `deny`; `ask` und `allow` sind es **nicht**. Das ist keine Schema-, sondern eine Wirkungsfrage und gehört zum Rest von `AP2` – zu Z82, Z94, Z101 und Z116, nicht in einen Klärungspunkt |
| `CLIENT_PACK.md` Z26 | Struktur von `.devin/mcp_config.json` | E5, E6 | **aufgelöst zum Besseren**: Der Container `mcpServers` der ausgelieferten Vorlage ist zeichengleich mit dem, was der Client selbst erzeugt. Zusätzlich erhoben: zwei weitere Ablageorte, und der **Standard ist der unversionierte** |
| `CLIENT_PACK.md` Z27 | `DEVIN_PROJECT_DIR` im Hook | E8 | **aufgelöst**: gesetzt, und zeigt auf das Projektverzeichnis – fünfmal aufgezeichnet |
| `root-template/.devin/README.md` Z10 | Schemadetails von `config.json` | wie Z24 | **aufgelöst**, gleiche Grenze |
| `root-template/.devin/README.md` Z12 | Struktur der MCP-Vorlage | wie Z26 | **aufgelöst** |
| `framework/runtime/mcp-config.example.json` | Struktur der MCP-Vorlage | wie Z26 | **aufgelöst, und zwar werkzeugneutral**: Die Datei liegt im Kern und darf nach D-02/D-28 keinen Client als Handelnden nennen. Sie verweist deshalb auf den Belegstand im jeweiligen Client Pack, statt einen Messwert zu wiederholen |
| `CLIENT_PACK.md` Z82 (S3) | Wirkung additiver Skill-Permissions | – | **bleibt.** Braucht eine Sitzung |
| `CLIENT_PACK.md` Z94 (B3) | Muster-Semantik der Pfadregeln | – | **bleibt.** Braucht eine Sitzung |
| `CLIENT_PACK.md` Z101 (B10) | Auswertung einer Domain-Angabe | – | **bleibt.** Braucht eine Sitzung |
| `CLIENT_PACK.md` Z116 (A1) | Profilwirkung des Reviewprofils | – | **bleibt.** Braucht eine Sitzung |
| `CLIENT_PACK.md` Z136 (X2) | Codebasis-Indexierung | – | **bleibt, und zwar dauerhaft.** Die Zeile sagt selbst, dass der Gegenstand von außen nicht beobachtbar ist (`K-20`) |

**Die Zeile *Belegstand* des Packs (Z150) ist davon nicht berührt.** Sie zählt die neun
Marker der **Fähigkeitsmatrix**; Z24, Z26 und Z27 stehen in der Pfadabbildung, Abschnitt 1.
Nachgezählt: neun vorher, neun nachher.

## 5. Die Abnahme – `clients/devin-desktop/CLIENT_PACK.md`

Geprüft gegen `framework/core/01-governance.md` Abschnitt 5 Punkt 3, Zeile
`entwurf → pilot`. Der Träger ist **namentlich** genannt, wie (e) es verlangt.

| Bedingung | Befund |
|---|---|
| **(a)** inhaltlich vollständig | **ja** – Pfadabbildung, Semantikabbildung, Fähigkeitsmatrix über sieben Klassen, Zusammenfassung der Durchsetzungstiefe, Kernzusagen ohne Durchsetzung, bekannte Abweichungen, Installation, Anweisungsquellen außerhalb des Projekts, Änderungsverlauf |
| **(b)** Validatorlauf ohne Fehler | **ja** – 0 Fehler, 0 Warnungen (Abschnitt 9) |
| **(c)** offene `VERIFY`-Marker benannt | **ja** – fünf, je Zeile benannt in Abschnitt 4. Sie sperren den Übergang nicht |
| **(d)** offene Ausfüllwerte | **keine mehr.** Beide Schlitze, die 0.52.0 als sperrend eingestuft hat (D-110), tragen jetzt Werte: die geprüfte Clientversion `3.9.19 (CLI 3000.10.21)` und das Prüfdatum `2026-09-16`. **Die neue Zeile *Verbindliche Zielversion* trägt ebenfalls einen Wert** und nicht etwa den nächsten Schlitz – das war die Vorentscheidung |
| **(e)** Review mit Fundstelle | **dieses Protokoll** |

> **Abgenommen: `entwurf` → `pilot`.** Damit steht **kein** Modulträger des Frameworks mehr
> auf `entwurf`. **Kriterium 3 von D-11 ist erfüllt** – das zweite der fünf, nach Kriterium 4
> mit 0.49.0.

**D-106 ist eingehalten, wo er gilt, und ausdrücklich nicht, wo er nicht gilt.** Ein reiner
Statuswechsel ist keine Versionsänderung. Dieser Vorgang ist **kein** reiner Statuswechsel:
Er füllt zwei Steckbriefzellen, legt eine dritte an und löst drei Marker auf. Die Version
des Packs geht deshalb von `0.10.0` auf `0.11.0`, und der Änderungsverlauf des Trägers
bekommt einen Eintrag. **Wer hier D-106 anwendete, verschwiege eine Inhaltsänderung.**

## 6. Nebenbefund 1: Das Schwesterpack trägt dieselbe offene Festlegung – als Prosa

`clients/claude-code/CLIENT_PACK.md` Z11 lautet seit 0.6.0:

> `2.1.267 (AP2-Dokumentenabgleich, …). Die **verbindliche Zielversion** legt`
> `<FRAMEWORK_OWNER>` `fest und steht aus`

**Es ist dieselbe ausstehende Festlegung des Framework Owners wie bei `devin-desktop`** –
nur steht sie dort als Ausfüllschlitz und hier als Satz. **Der Schlitz sperrte den
Übergang, der Satz nicht**, und deshalb ist dieses Pack mit 0.52.0 abgenommen worden,
während das andere liegen blieb.

**D-110 war für seinen Gegenstand richtig und ist es geblieben:** Für den *Belegstand* ist
der Modulstatus nicht zuständig, und die Trennlinie war korrekt gezogen. **Der Befund liegt
eine Ebene höher:** Die Entscheidung, die 0.52.0 für `devin-desktop` offenhielt, stand für
`claude-code` genauso offen – und **die Kandidatenzeile der Übergabe nannte nur ein Pack.**

> ⚠️ **Zum zehnten Mal in Folge war die Aufgabenbeschreibung zu klein**, und diesmal ist die
> Bauform benennbar: **Eine Suche nach einer Marke findet die Fundstellen, die die Marke
> tragen – nicht die, die dasselbe sagen.** 0.52.0 hat gelehrt, dass dieselbe Marke zwei
> Bedeutungen tragen kann. 0.53.0 fügt die Gegenrichtung hinzu: **Dieselbe Bedeutung kann
> ohne die Marke auskommen.**

Behoben: Beide Packs führen ab 0.53.0 die Zeile *Verbindliche Zielversion* mit einem Wert.
Für `claude-code` ist das `2.1.x` – **und der gemessene Punktwert `2.1.267` liegt darin,
der installierte `2.1.273` ebenfalls.**

## 7. Nebenbefund 2: Drei Marker, deren Beleg seit fünf Tagen im Haus lag

Z24, Z26 und Z27 sind heute aufgelöst worden. **Zwei davon brauchten keine neue Messung.**

| Marker | Beleg | Lag vor seit |
|---|---|---|
| Z24 (`hooks`) | `2026-09-11-AP2-devin-desktop.md`, `AP2-DD-10` | **2026-09-11**, fünf Releases |
| Z24 (`permissions`) | `2026-09-14-erhebung-devin-werkzeuge.md`, Läufe P4/W1 | **2026-09-14**, drei Releases |
| Z27 (`DEVIN_PROJECT_DIR`) | `devpacks/lw-tech/ap2-hook-aufzeichnung.jsonl` | **2026-09-11**, fünf Releases |

**Der wiederkehrende Befundtyp dieses Projekts ist *eine Zusage, die mehr verspricht, als
sie leistet.* Hier steht sein drittes Spiegelbild:**

> **Ein offener Marker ist eine Aussage über den eigenen Belegstand – und auch die
> veraltet.** Er behauptet, etwas sei ungeprüft. Wird es geprüft, ohne dass jemand den
> Marker anfasst, **behauptet er ab da etwas Falsches über das eigene Haus** und zählt
> weiter in Kriterium 1 mit.

Das erste Spiegelbild war 0.49.0 (*eine Bedingung, die mehr verlangt, als ihr Kriterium
fordert*), das zweite 0.50.0 (*eine Bedingung, die niemand nachzählt, ist eine Zusage mit
umgekehrtem Vorzeichen*). **Alle drei haben dieselbe Ursache:** Das Repositorium prüft, was
es zusagt, und nicht, was es über sich selbst behauptet.

**Daraus folgt D-114**, und die Entscheidung ist nicht selbstverständlich: Ein Protokoll,
das **älter** ist als der Vorgang, der einen Marker auflöst, ist als Beleg zugelassen –
**aber nur, weil die Zielversion jetzt eine Spanne ist und die Messung nachweislich in ihr
liegt.** Ohne D-112/D-113 wäre ein Beleg vom 2026-09-11 gegen `3.9.19` für ein Pack, das
auf einen anderen Punktwert festgelegt wäre, kein Beleg.

## 8. Was offen bleibt

| Kennung | Frage | Warum sie hier steht und nicht gelöst wird |
|---|---|---|
| **`K-40`** | Soll eine Prüfung nachrechnen, dass die geprüfte Clientversion in der verbindlichen Zielspanne liegt? | **Der Preis von D-113, unbezahlt.** Die Spanne ist von keiner Prüfung gehalten; sie kann veralten, ohne dass es auffällt – genau die Eigenschaft, die `2.1.267` sechs Patchstände alt werden ließ. **Nicht gebaut**, weil die Anweisung des Menschen vom 15.09. weiter gilt: keine neue Prüfung, solange eine Zahl zu senken ist. Dieses Release senkt zwei |
| **`K-41`** | Gehört der Satz *„ohne geprüfte Clientversion ist keine Einstufung `[TECHNISCH]` zulässig"* in ein Kernmodul – und wer setzt ihn durch? | **Gefunden beim Lesen, nicht beim Suchen.** Der Satz steht an genau zwei Stellen: in `build/doc/04-geltungsbereich.md` – dem Hauptdokument, das zweiundvierzig Releases zurück ist – und als Erklärtext im Ausfüllschlitz von `clients/_template/CLIENT_PACK.md`. **In keinem Kernmodul, und keine der 47 Prüfungen setzt ihn durch.** Gemessen heißt das: `devin-desktop` trug bis heute `[TECHNISCH]`-Zeilen ohne geprüfte Clientversion – seit 0.7.0, also über **sechsundvierzig Releases**, bei grünem Validatorlauf |
| `K-20` | Codebasis-Indexierung | unverändert offen; Z136 bleibt |
| `K-37`, `K-38`, `K-39` | unverändert | – |

**Nicht offen, sondern Arbeit:** die vier sitzungsgebundenen Marker Z82, Z94, Z101, Z116 –
und die ungemessene Wirkung der Körbe `ask` und `allow` aus Abschnitt 4. Sie sind der Rest
von `AP2` und kosten Devin-Kontingent.

## 9. Kontrollläufe

| Lauf | Ergebnis |
|---|---|
| `validate-framework.py --root .` vor dem Eingriff | 0 Fehler, 0 Warnungen |
| Auszählung Kriterium 1 nach der Leseregel der Prüfung 46, vor dem Eingriff | **29**, verteilt auf 17 Dateien – zeichengleich mit der Standzeile |
| Auszählung Kriterium 1 nach dem Eingriff | **23** |
| Auszählung Kriterium 3 nach dem Eingriff | **0** |

Die Läufe nach dem Eingriff und der vollständige Sondenlauf stehen im Wirkungsnachweis
`2026-09-16-wirkungsnachweise-0.53.0.md`.
