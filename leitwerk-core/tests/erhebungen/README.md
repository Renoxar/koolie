# Meßapparat der Erhebungen

Die Skripte, mit denen die **Sitzungstests** dieses Projekts gefahren und ausgewertet
werden. Sie laufen ausschließlich im **Quellrepositorium** und werden von `install.py`
in kein Projekt geschrieben – wie `tests/scripts/probe-pruefungen.py` auch.

> 🔴 **Warum sie hier liegen und nicht daneben** (D-222). Am Morgen des Meßtags von
> Bündel 4 lagen **zehn der elf Erhebungsablagen im Papierkorb**, und der Apparat
> hängt an fünf Skripten aus einer davon. *Ein Meßapparat, der ein Nachbarverzeichnis
> braucht, ist so haltbar wie dieses Verzeichnis.*

## Was hier liegt und was nicht

| | |
|---|---|
| **Hier:** die Skripte | Baumbau, Zuschnitte, Lauf, Auswertung, Dossiers, Aufräumen |
| **Nicht hier:** die Belege | Antworten, Ergebnis-JSON, stdout und Sitzungsmitschriften je Lauf, dazu die **Prompts** und die **Zustandsaufnahmen**. Sie sind **Aufzeichnung**, nicht Anweisung (dieselbe Trennlinie wie D-141), und liegen neben dem Repositorium. **Jedes Protokoll nennt den Ablageort seiner Belege** |

## 🔴 Zwei Pfade werden gesagt – `LW_ERHEBUNG` und `LW_UEBUNG`

**Vor jedem Lauf zu setzen:**

```
set LW_ERHEBUNG=C:\...\devpacks\leitwerk-erhebungen-<datum>-<buendel>   # SYNTHETISCH
set LW_UEBUNG=C:\...\devpacks\<uebungsrepositorium>                     # SYNTHETISCH
```

🔴 **`LW_UEBUNG` gibt es seit `0.79.4` und aus demselben Grund wie `LW_ERHEBUNG`**
(**D-231**): **Neun Werkzeuge dieses Apparats trugen einen Arbeitsplatzpfad im
Quelltext – mit dem Kontonamen einer natürlichen Person.** Solange sie neben dem
Repositorium lagen, stand das in einer unversionierten Ablage; **mit D-222 sind sie
hineingewandert und haben die Pfade mitgebracht.** **Prüfung 71** meldet seither jeden
absoluten Pfad in ein Benutzerprofil, dessen Kontosegment kein Platzhalter ist und
dessen Zeile keine Begründung trägt.

> *Wer einen Apparat umzieht, zieht seine Arbeitsplatzpfade mit um – und veröffentlicht
> sie, ohne es zu entscheiden.*

⚠️ **Ausgenommen sind Aufzeichnungen** (`tests/protocols/`,
`governance/change-requests/`): Sie halten fest, **wo** gemessen wurde, und ein
Protokoll, das man umschreibt, ist keines mehr (D-141). Zehn von ihnen tragen den
Kontonamen weiter – das ist **`K-85`** und nicht entschieden.

## 🔴 Die Ablage wird gesagt, nicht abgeleitet – `LW_ERHEBUNG`

**Vor jedem Lauf zu setzen**, sonst bricht jedes Skript ab, das eine
Belegablage braucht:

```
set LW_ERHEBUNG=C:\...\devpacks\leitwerk-erhebungen-<datum>-<buendel>
```

Darunter entstehen `belege/`, `prompts/` und die vier Zustandsaufnahmen.

🔴 **Warum es diese Angabe gibt** (Vorbedingungsdurchgang des Nachlaufs,
2026-09-20). Bis zum Meßtag lag der Apparat **neben** dem Repositorium, und
fünf Skripte legten ihre Belege schlicht neben sich ab –
`os.path.dirname(os.path.abspath(__file__))`. Das war richtig, solange sie
daneben lagen. **Mit dem Umzug nach D-222 zeigt derselbe Ausdruck hinein**, und
`lauf.py` legt das Verzeichnis selbst an: Der Nachlauf hätte 44 Belegdateien
samt Sitzungsmitschriften mit Werkzeugeingaben versioniert – genau das, was
D-222 verworfen hat.

> *Wer einen Apparat umzieht, zieht seine relativen Pfade mit um – oder er
> verschiebt ihr Ziel, ohne es zu merken.*

**Zwei Hälften eines Gegenstands:** `ablage.py` weist einen Pfad **im**
Repositorium ab (vorher), **Prüfung 69** meldet jede Datei, die dort trotzdem
liegt (nachher). Ein Sollwert im Quelltext wäre eine gepflegte Zahl gewesen –
dieselbe Lehre wie `--ziel` beim Baumbau (D-218).

## Die Werkzeuge

| Skript | Was es tut |
|---|---|
| `lauf.py` | fährt **einen** Lauf und sichert alle drei Belegquellen sofort weg |
| `reihe-b4.py` | fährt die Reihe und **nur, was fehlt** |
| `stand-b4.py` | sagt den Stand der Reihe in einem Befehl |
| `historie-bauen-b4.py` | baut einen Meßbaum mit **echter Historie**, synthetischen Autoren und Übungs-Branches |
| `baeume-b4.py` | legt Haupt- und Kontrollbäume an (`--ziel` sagt, wohin) |
| `k-bauen-b3.py` | baut den Kontrollzuschnitt **ohne die geprüfte Schranke**, mit Stammwächter |
| `cc-overlay-fuellen.py` | füllt eine frische Installation aus dem versionierten Projektbestand |
| `prompts-schreiben-b4.py`, `turn2-schreiben-b4.py` | schreiben die Prompts; Haupt- und Kontrollprompt sind **wörtlich gleich** |
| `auswerten-b4.py` | Kennzahlen, Berührungsprobe, Merkmale, Kontrollzählung |
| `dossier-b4.py` | legt je Zelle die **Erwartung** des Testblatts neben den **Beleg** des Laufs – und **fährt die Auswertung dafür selbst** (D-232) |
| `zustand-b4.py`, `node-waechter.py` | Zustandsaufnahme vor und nach der Reihe; Gegenzählung des geteilten Bestands |
| `umgebungen-bauen-b4.py`, `trust-b4.py` | Umgebungen und Vertrauenseinträge |
| `baeume_loeschen.py` | löst **jede Verzeichnisverbindung einzeln**, dann `shutil.rmtree` mit `onexc`-Haken |
| `zaehlen46.py` | zählt Kriterium 2 mit der Regel von Prüfung 46 |
| `ablage.py` | sagt allen anderen, **wo** Belege, Prompts und Zustandsaufnahmen liegen, **welche Kernversion** das Übungsrepositorium tragen muß – und **welche Zellen eine Erhebung schuldet** (`sollmenge()`, D-230) |
| `packaktivierung.py` | aktiviert ein Role oder Tech Pack im Meßbaum (drei Teile, drei Wächter), nimmt es für `ohnepack` wieder heraus und trägt den Skillschnitt (D-237, D-238, D-242, D-244) |

## 🟢 Der Apparat von Bündel 5 – dieselbe Mechanik, ein eigener Zuschnitt

**Zu Bündel 5 (`RE-001`, `role-re-ticket`) gehören eigene Werkzeuge**, und der
Grund steht in D-230: *Ein Verzeichnis ist kein Zuschnitt. Es ist der Zuschnitt
von gestern.* Geerbt und mit `0.82.0` gemessen ist die **Mechanik**;
Zuordnung, Pflichtliste und Zielpfad (`C:\lw-b5`) gehören diesem Bündel.

| Skript | Was es anders macht als seine `-b4`-Fassung |
|---|---|
| `umgebungen-bauen-b5.py` | **aktiviert das Role Pack** (bei Bündel 4 ist der Block leer, weil alle drei Skills im Kern liegen); prüft Vertrag, Schema, Glossar und die **Wertzeile** von `<ISSUE_TRACKER>`; **leere Abweichungsliste** – kein Schreibkorb, keine Befehlsschlitze; fährt `validate-output.py` statt `npm test` |
| `baeume-b5.py` | **sechs** Kontrollklassen statt acht, **keine** Übungs-Branches, **kein** `node_modules`; setzt `UEB-30` und `UEB-31` in je **zwei** Bäume **vor** dem ersten Commit |
| `prompts-schreiben-b5.py` | fünfzehn Prompts; `RE-001-P04` und `RE-001-N09` tragen **denselben** Prompt – verschieden ist der Baum (D-240) |
| `auswerten-b5.py` | Marken sind **Muster**, keine Teilzeichenketten; dritte Gattung `nennung`; `--marken` hält jede `fund`-Marke **gegen den Baum ihrer Zelle** (D-233) |
| `dossier-b5.py` | findet das Testblatt über `ablage.blaetter()` – `role-re-ticket` liegt **nicht** unter `framework/skills/` |
| `reihe-b5.py`, `stand-b5.py`, `zustand-b5.py`, `trust-b5.py` | aus den `-b4`-Fassungen; geändert wurde ausschließlich der Basispfad und die Nennung der Nachbarwerkzeuge |

🔴 **Zwei Befunde am Kontrollzuschnitt fielen vor dem ersten bezahlten Lauf**
(D-247, D-248) – beide an der Klasse `fern`, und beide hätten einen Kontrollauf
unbrauchbar gemacht, ohne daß ein Wächter es gemeldet hätte.

## Die drei Wächter, die es seit 0.79.0 gibt

Jeder von ihnen hat einen gemessenen Anlaß, und alle drei stehen in **D-218**:

1. **`HEAD` nach dem Baumbau.** Der Wächter davor verglich die *Menge der
   Branchnamen* – an allen 38 Bäumen des Meßtags richtig, während `HEAD` auf allen 38
   auf `main` stand. *Ein Vorhandensein belegt sich selbst, ein Zustand nicht.*
2. **Die Zeilenenden der Arbeitskopie.** `ersetze()` legte sie als LF zurück, während
   der Baum CRLF führt – 165 Zeilen Rauschen in einem Änderungssatz von sechs.
3. **Der Baumname in der Zustandsaufnahme.** Ein zweiter Turn heißt `sk011p01t1`, sein
   Baum aber `sk011p01`; der Präfixvergleich traf nie, und jeder erste Turn meldete
   *„nichts geändert"*, ohne daß es gemessen war.

## Die drei Befunde des Vorbedingungsdurchgangs (2026-09-20)

Sie kosteten nichts, weil sie vor dem ersten bezahlten Lauf kamen:

1. **Der Apparat schrieb ins Repositorium** – siehe oben, `LW_ERHEBUNG` und
   Prüfung 69.
2. **Drei Wächter derselben Vorbedingung, drei Sollwerte, keiner stimmte.**
   `umgebungen-bauen-b4.py` und `baeume-b4.py` führten `--erwarte 0.78.0`,
   `historie-bauen-b4.py` führte `0.77.0` – das Übungsrepositorium stand auf
   `0.78.2`, der Kern auf `0.79.1`. Der Sollwert wird seither **abgeleitet**
   (`ablage.kernversion()`); `--erwarte` bleibt als Übersteuerung.
3. **Die Berührungsprobe kannte ihre Gattung nur im Kommentar.** D-120
   schließt mit *„Für Fund-Testfälle bleibt die erste Form nach D-116 die
   einzige zulässige“* – `auswerten-b4.py` druckte `W` und `T` für alle
   neunzehn Zellen gleich. Die Gattung steht jetzt **je Marke im Code**, und
   das Urteil steht **je Lauf**, nicht je Turn: Bei `fw-docs-update` trägt der
   erste Turn den Halt und der zweite die Umsetzung (dieselbe Bauform wie der
   dritte Teil von D-218).

## Die zwei Befunde der Wiederaufnahme (2026-09-21)

Sie kosteten nichts, weil sie vor dem ersten bezahlten Kontrollauf kamen – und sie
lagen beide **auf dem Weg**, den der Wiederaufnahmepunkt vorschreibt:

1. 🔴 **`stand-b4.py` startete seit `0.79.0` nicht** (**D-229**). Zwei Lesestellen
   eines Namens, den der Umzug nach D-222 entfernt hat – `NameError` beim Import, und
   das Skript stand als **Befehl 1 von 4** im Wiederaufnahmepunkt. **Keine der 69
   Prüfungen konnte es sehen:** Prüfung 45 prüft die *Abwesenheit* von Bytecode,
   Prüfung 69 die *Art* der Dateien hier – daß eine davon **läuft**, prüfte keine.
   **Prüfung 70** baut seither zu jeder `.py` des Kerns die Symboltabelle.

   > *Ein Werkzeug, das niemand fährt, verfällt lautlos – und der Tag, an dem es
   > gebraucht wird, ist der Tag, an dem es fehlt.*

2. 🔴 **Die Sollmenge kam aus dem Promptverzeichnis** (**D-230**). Der Nachlauf mißt
   vierzehn Zellen, sein Promptverzeichnis trägt die fünfzig Prompts des Meßtags.
   `stand-b4.py` meldete **35 Fehlbestände und rund 37 USD**, fällig waren fünfzehn
   und rund achtzehn – und `reihe-b4.py` **ohne Argumente**, der Befehl, den
   `stand-b4.py` selbst als nächsten nennt, brach am ersten Baum ab, den es in dieser
   Erhebung nie gab. Die Sollmenge kommt seither aus den **Meßbäumen**
   (`ablage.sollmenge()`), und ein Prompt ohne Baum wird **genannt**.

   > *Ein Verzeichnis ist kein Zuschnitt. Es ist der Zuschnitt von gestern.*

### Die zwei Befunde beim Bau der Dossiers (2026-09-21)

1. 🔴 **Neun Werkzeuge nannten einen Arbeitsplatz** (**D-231**, **Prüfung 71**) – siehe
   oben. **Achtzehn Träger** trugen den Kontonamen vor dem Eingriff, **acht Werkzeuge**
   und **zehn Aufzeichnungen**; danach **null Werkzeuge**.
   🟢 **Und Prüfung 70 hat dabei ihren ersten echten Fang gemacht:** Die Umstellung
   ließ in drei Werkzeugen den Aufruf `ablage.…` ohne den Import stehen – **drei
   `NameError`, gemeldet vom Validator, bevor ein Lauf sie fand.**

2. 🔴 **`dossier-b4.py` wartete auf ein Datum** (**D-232**). Es nannte
   `auswertung-2026-09-20.log` im Quelltext und brach am 21. ab – *obwohl die
   Auswertung gefahren war*. Es fährt sie seither selbst.

   > *Ein Werkzeug, das die Ausgabe eines anderen beim Namen nennt, wartet auf den
   > Tag, an dem jemand diesen Namen anders wählt.*

### Die drei Befunde der Auswertung (2026-09-21)

Sie liegen alle am **Apparat**, nicht an den Skills – und sie sind erst aufgefallen,
als 28 bezahlte Läufe gegen sie gehalten wurden:

1. 🔴 **Der Kontrollzuschnitt `ohneskill` schnitt das Kommando, nicht den Skill**
   (**D-234**). Er leerte allein die Skillablage der Laufzeitschicht – **der Meßbaum
   trägt aber das Framework, und dort steht der Skill.** Drei Kontrollläufe derselben
   Klasse, drei Ausgänge: einer las die kanonische `SKILL.md` und arbeitete sie **von
   Hand nach**, einer das Subagentenprofil, einer sah nur in der Skillablage. Der
   Zuschnitt entfernt seither **jeden** Träger, und ein **Stammwächter** sucht über den
   ganzen Baum nach `SKILL.md`.

   > *Ein Zuschnitt, der davon abhängt, wohin der Lauf schaut, ist keiner.*

2. 🔴 **Zwei Berührungsmarken konnten nicht treffen** (**D-233**): `TBD` als Gattung
   `fund` – eine `fund`-Marke verlangt die **Werkzeugeingabe**, und `<TBD>` ist etwas,
   das der Lauf **schreibt** – und die Dateien einer **anderen** Zelle. Berichtigt und
   **aus den vorhandenen Belegen** neu ausgewertet: kein neuer Lauf, 15,85 USD gespart.

3. 🔴 **Das Werkzeug sagte für einen ausgefallenen Kontrollauf mehr, als aus ihm folgt**
   (**D-236**). Der Hauptlauf trägt das **Urteil** (D-116), der Kontrollauf die
   **Zurechnung** (D-115, D-175). `auswerten-b4.py` sagt es seither je Lauf getrennt.

## Vor jedem Meßtag

- **Das Prüfmittel einmal im Meßbaum laufen lassen** – nicht danach (0.68.0).
- **Jede Berührungsmarke gegen den Baum ihrer Zelle halten** – eine `fund`-Marke muß ein Gegenstand sein, den ein Werkzeug öffnen kann, und sie muß im Änderungssatz **dieser** Zelle liegen (D-233).
- **Den Kontrollzuschnitt gegen seinen Gegenstand halten, nicht gegen seinen Namen** – `ohneskill` hat drei Meßtage lang nur das Kommando geschnitten (D-234).
- **Jedes Werkzeug einmal aufrufen, das der Ablauf nennt** – `stand-b4.py` stand
  elf Tage lang im Ablauf und startete nicht (D-229). Prüfung 70 nimmt das ab,
  aber nur für die Namen, nicht für die Werte.
- **Den Apparat als Ganzes einmal fahren.** Beim ersten vollständigen Aufbau von
  Bündel 4 brach er an **sechs** Stellen, und alle sechs kosteten nichts.
- **Nicht unterhalb des Arbeitsbereichs messen** – dort liegt eine sachfremde
  Anweisungsdatei, und der Client lädt sie aus jedem übergeordneten Verzeichnis. Die
  Kontrollzählung über alle Mitschriften muß **null** ergeben.
