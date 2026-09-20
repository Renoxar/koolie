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
| `dossier-b4.py` | legt je Zelle die **Erwartung** des Testblatts neben den **Beleg** des Laufs |
| `zustand-b4.py`, `node-waechter.py` | Zustandsaufnahme vor und nach der Reihe; Gegenzählung des geteilten Bestands |
| `umgebungen-bauen-b4.py`, `trust-b4.py` | Umgebungen und Vertrauenseinträge |
| `baeume_loeschen.py` | löst **jede Verzeichnisverbindung einzeln**, dann `shutil.rmtree` mit `onexc`-Haken |
| `zaehlen46.py` | zählt Kriterium 2 mit der Regel von Prüfung 46 |
| `ablage.py` | sagt allen anderen, **wo** Belege, Prompts und Zustandsaufnahmen liegen – und **welche Kernversion** das Übungsrepositorium tragen muß |

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

## Vor jedem Meßtag

- **Das Prüfmittel einmal im Meßbaum laufen lassen** – nicht danach (0.68.0).
- **Den Apparat als Ganzes einmal fahren.** Beim ersten vollständigen Aufbau von
  Bündel 4 brach er an **sechs** Stellen, und alle sechs kosteten nichts.
- **Nicht unterhalb des Arbeitsbereichs messen** – dort liegt eine sachfremde
  Anweisungsdatei, und der Client lädt sie aus jedem übergeordneten Verzeichnis. Die
  Kontrollzählung über alle Mitschriften muß **null** ergeben.
