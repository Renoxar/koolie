# Protokoll: Die Wiederaufnahme des Nachlaufs von Bündel 4 – zwei tote Befehle auf dem Weg

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-21 |
| Gegenstand | Der Weg der Wiederaufnahme selbst (`WIEDERAUFNAHME.md`, vier Befehle) – **vor** dem ersten bezahlten Kontrollauf |
| Antrag | `CR-2026-111` |
| Kontingent | **keines für die Befunde** – sie fielen alle vor dem ersten Lauf |
| Belege | Dieser Durchgang erzeugt keine Laufbelege. Die Belege des Nachlaufs liegen in `devpacks/leitwerk-erhebungen-2026-09-20-b4n/belege/` |

> 🔴 **Zwei Befunde, und beide liegen auf dem Weg, den die Wiederaufnahme vorschreibt.**
> Von den **vier** Befehlen des Wiederaufnahmepunkts startete der erste nicht, und der
> vierte hätte in seiner argumentlosen Form **keinen einzigen Lauf** gefahren. Bei den
> letzten zwanzig Durchgängen in Folge fiel der billigste Befund vor dem ersten Lauf;
> dieser macht den einundzwanzigsten.

## 1. Die Lage vor dem Durchgang

| Prüfung | Ergebnis |
|---|---|
| `git status` im Framework | sauber, `main` = `origin/main`, `HEAD` auf `f3fe603` |
| `validate-framework.py` | **0 Fehler, 0 Warnungen** |
| `C:\lw-b4` | **35 Verzeichnisse** – 27 Meßbäume und acht Kontrollbasen, wie der Wiederaufnahmepunkt sie beschreibt |
| Vertrauenseinträge unter `c:/lw-b4/` | **35** – vollständig |
| Zustandsaufnahmen *vorher* | `zustand-vorher.json` und `node-vorher.json` liegen vor |
| Belege des ersten Teils | **15 Belegsätze, `is_error` bei keinem**, zusammen 15,86 USD |

🟢 **Die fünfzehn Belegsätze sind nicht fünfzehn bezahlte Läufe.** Zwei davon –
`sk011n04` und `sk011n04t1` – sind **übernommen**: Sie tragen den Zeitstempel *vor* dem
Beginn der Reihe (18:41 gegen 18:43), haben in dieser Erhebung **keinen Meßbaum**, und
die README nennt den Hauptlauf von `SK-011-N04` ausdrücklich unter *„was nicht noch
einmal bezahlt wird"*. **15,86 USD − 1,90 − 1,42 = 12,53 USD** – Cent für Cent die
Zahl, die der Wiederaufnahmepunkt nennt. **13 von 28 gefahren.**

⚠️ **Vierzehn Zellen oder dreizehn – beides stimmt, und der Unterschied ist benannt.** Der Releaseplan führt **dreizehn** Zellen; das sind die, die mit Haupt- **und** Kontrollauf fahren. `SK-011-N04` ist die vierzehnte: Von ihr fährt **nur** der Kontrollauf (`konf` statt `risiko`, D-221), ihr Hauptlauf vom Meßtag bleibt gültig. `stand-b4.py` zählt Bäume und kennt diesen Unterschied nicht – es meldet deshalb **14 Zellen / 28 Läufe**, und die Zahl der **Läufe** ist in beiden Lesarten dieselbe.

## 2. Befund 1: Befehl 1 von 4 startete seit `0.79.0` nicht

```
> python leitwerk-core\tests\erhebungen\stand-b4.py
Traceback (most recent call last):
  File "...\stand-b4.py", line 28, in <module>
    PROMPTS = os.path.join(os.path.dirname(S), "prompts")
                                           ^
NameError: name 'S' is not defined
```

**`S` trug bis D-222 den Ablageort neben dem Skript.** Der Umzug in den Kern hat den
Namen entfernt und **zwei** Lesestellen stehen lassen. Die zweite fiel erst nach der
Berichtigung der ersten:

```
  File "...\stand-b4.py", line 123, in main
    da = os.path.isfile(os.path.join(S, pflicht))
```

Seit `0.79.0` war das Werkzeug tot – **elf Tage und drei Releases lang**, und der Tag
seiner Wiederaufnahme war der Tag, an dem es auffiel.

> *Ein Werkzeug, das niemand fährt, verfällt lautlos – und der Tag, an dem es gebraucht
> wird, ist der Tag, an dem es fehlt.*

### 🔴 Der eigentliche Befund: keine der 69 Prüfungen konnte es sehen

| Prüfung | Gegenstand | Sieht sie es? |
|---|---|---|
| **45** | unter `leitwerk-core/` ist kein Bytecode versioniert | nein – sie prüft die **Abwesenheit** einer Datei |
| **69** | in der Erhebungsablage liegen nur `.py` und `.md` | nein – sie prüft die **Art** der Dateien |
| *keine* | ob eines dieser `.py` **startet** | – |

Der Apparat hatte zwei Wächter über seinen **Ablageort** und keinen einzigen darüber,
ob seine Werkzeuge **laufen**.

**Abhilfe: Prüfung 70** (D-229). Zu jeder `.py` unter `<CORE_DIR>/` wird die
**Symboltabelle** gebaut, die der Interpreter selbst anlegt, und jeder global gelesene
Name gemeldet, den weder der Modulrumpf noch die eingebauten Namen binden – dazu jede
Quelle, die er nicht übersetzt.

**Warum nicht importieren:** Das führt den Modulrumpf aus. `ablage.py` bricht ohne
`LW_ERHEBUNG` mit Absicht ab, und `lauf.py` legt sein Belegverzeichnis an – **genau
das, was D-222 verworfen hat.** *Eine Prüfung, die ihren Gegenstand verändert, mißt ihn
nicht.*

**Gemessen gegen den gesamten Kern, vor der Berichtigung:** ein Befund
(`stand-b4.py`, zwei Fundstellen) aus zwanzig `.py`-Dateien. Zwölf davon nennen
Modulglobale wie `__file__`; sie laufen, und die Prüfung schweigt über sie. *Ein
Wächter, der bei jedem Lauf meldet, wird abgeschaltet.*

## 3. Befund 2: Der nächste Befehl hätte keinen einzigen Lauf gefahren

`stand-b4.py` schließt mit `NAECHSTER BEFEHL: python reihe-b4.py`. Genau dieser Aufruf
**ohne Argumente** bricht ab:

```
ABBRUCH: der Baum C:\lw-b4\sk011n01 fehlt - erst baeume-b4.py
```

Beide Skripte leiteten ihre Sollmenge aus dem **Promptverzeichnis** ab. Der Nachlauf
mißt vierzehn Zellen; sein Promptverzeichnis trägt die **fünfzig** Prompts des
Meßtags, weil `prompts-schreiben-b4.py` alle schreibt und keine Zelle kennt.

| | vorher gemeldet | fällig | nachher gemeldet |
|---|---|---|---|
| Sollmenge | **50 Läufe / 19 Zellen** | 28 / 14 | **28 Läufe / 14 Zellen, 1 mit zweitem Turn** |
| gültig | 15 | 15 | **15** |
| Fehlbestand | **35** | 15 | **13** *(zwei Kontrolläufe waren bereits gefahren)* |
| Restkosten | **rund 37 USD** | rund 18 USD | **rund 13 USD** |
| `reihe-b4.py` ohne Argumente | **Abbruch, 0 Läufe** | 15 Läufe | fährt den Zuschnitt |

🔴 **Gerettet hat den Nachlauf allein die Kennungsliste im Wiederaufnahmepunkt – und
sie weist sich selbst als *„Vorsicht, keine Pflicht"* aus.** Wer dem Apparat gefolgt
wäre statt der Liste, hätte einen Abbruch bekommen; wer seiner Zahl gefolgt wäre, hätte
das Doppelte veranschlagt und das Kontingent danach bemessen.

> *Ein Verzeichnis ist kein Zuschnitt. Es ist der Zuschnitt von gestern.*

**Abhilfe: `ablage.sollmenge()`** (D-230). Die Sollmenge kommt aus den **Meßbäumen** –
`baeume-b4.py` legt genau die an, die der Zuschnitt nennt –, sie steht **einmal** im
Apparat, und beide Skripte benutzen dieselbe. Die elf Prompts ohne Meßbaum werden
**namentlich** genannt:

```
Nicht im Zuschnitt dieser Erhebung (Prompt vorhanden, kein Messbaum): 11
  ksk011n01 ksk011n02 ksk011n03 ksk011p01 ksk011p02 sk011n01
  sk011n02 sk011n03 sk011n04 sk011p01 sk011p02
```

Das ist dieselbe Bauform wie D-224 (`LW_ERHEBUNG`) und D-218 (`--ziel`), eine Ebene
weiter: **Ein Ort, der aus der Umgebung erschlossen wird, gehört dem, der ihn zuletzt
gefüllt hat.**

## 4. Warum der Nachlauf vor der Abhilfe angefahren wurde

Die fünfzehn Kontrolläufe hängen an 27 Meßbäumen, 35 Vertrauenseinträgen und einer
Zustandsaufnahme *vorher*, die seit dem 2026-09-20 stehen. **Jede Stunde Verzug ist
eine Stunde, in der etwas davon verlorengehen kann** – und die Abhilfe berührt
`reihe-b4.py` selbst, dessen laufender Prozeß sein Modul bereits geladen hat.

**Preis, benannt:** Die fünfzehn Kontrolläufe sind mit der **alten** Fassung gefahren.
An dem, was sie messen, ändert das nichts – die Kennungen standen im Aufruf –, aber der
Wirkungsnachweis zu D-230 steht am **Stand**, nicht an der Reihe.

## 5. Vorbedingungen der fünfzehn Kontrolläufe

Geprüft **vor** dem Anfahren, an allen vierzehn Zielbäumen:

| Prüfung | Ergebnis |
|---|---|
| `HEAD` je Baum auf dem Branch seiner Zelle (D-218) | **14 von 14** – elf auf einem `uebung/*`-Branch, drei auf `main` |
| Die drei auf `main` | `ksk010p02` und `ksk010n02` mit je zwei geänderten Dateien in der Arbeitskopie (der Änderungssatz ihrer Zelle), `ksk010n04` sauber (Grenze statt Branchliste, D-219); `ksk011n04` nennt seine Datei im Prompt und führt nur `main` |
| Arbeitskopie sonst | sauber |
| Vertrauenseinträge | **35** |

## 6. Der Wirkungsnachweis zu D-230 – nach dem Nachlauf, ohne einen Lauf

Als alle 28 Belege vorlagen, ist `reihe-b4.py` **ohne Argumente** gefahren – genau der Aufruf, der vor der Abhilfe abbrach:

```
nicht im Zuschnitt dieser Erhebung (Prompt vorhanden, kein Messbaum):
  ksk011n01 ksk011n02 ksk011n03 ksk011p01 ksk011p02 sk011n01
  sk011n02 sk011n03 sk011n04 sk011p01 sk011p02
uebersprungen (gueltiger Beleg liegt vor): sk010n01
… 27 Kennungen …
gefahren: 0 | Kosten dieser Reihe: 0.00 USD
```

**Er geht den ganzen Zuschnitt durch, nennt die elf Prompts ohne Baum und fährt nichts.** Vorher brach er beim ersten dieser elf ab – `sk011n01` – und kam nie bis zu einem Kontrollauf. **Der Nachweis kostet nichts, weil alles belegt ist.**

## 7. Das Ergebnis des Nachlaufs

| | |
|---|---|
| Gefahren | **28 von 28**, `is_error` bei keinem |
| Kosten insgesamt | **28,38 USD** (Mittel 1,01 USD, 139 s je Lauf) |
| Davon dieser Tag | **15,85 USD** für die fünfzehn Kontrolläufe |
| Gerechnet war | rund 18,40 USD – **2,55 USD unter der Schätzung** |
| Abweisungen | drei Läufe mit `permission_denials` > 0 (`ksk012n03`: 1, `ksk010p01`: 2) – **Gegenstand der Auswertung**, nicht dieses Protokolls |

🔴 **Der Meßtag ist nicht aufgeräumt** – 27 Bäume, acht Kontrollbasen und 35 Vertrauenseinträge stehen, weil die Auswertung sie braucht. **Aufgeräumt wird vor der Übergabe von `~0.80.0`** (D-223).

⚠️ **Ein Nebenbefund beim Fortschreiben, ohne eigenen Decision Record:** Der Posten `0b` der Plantabelle in `UEBERGABE.md` trug **sechs Zellen in einer vierspaltigen Tabelle**. Der Nachtrag vom 2026-09-20 hatte *Aufwand* und *Wirkung* neu angehängt, ohne die alten zu entfernen – dieselbe Bauform wie D-216, eine Zeile tiefer. Beim Fortschreiben dieses Releases ist die Zeile auf vier Zellen zurückgeführt worden. **Keine Prüfung sieht das**: Prüfung 67 vergleicht die Titelzeile und die Lagezeile der Übergabe gegen `VERSION`, nicht ihre Tabellen.

## 8. Abnahme dieses Durchgangs

- `validate-framework.py --root .`: **0 Fehler, 0 Warnungen**.
- `probe-pruefungen.py --nur 70`: **fünf von fünf Einheiten bestanden** – Sonden `70a`
  bis `70c`, Gegenproben `70a` und `70b`. Sonde `70a` setzt den Defekt **wörtlich** so,
  wie er gefunden wurde.
- `probe-pruefungen.py`: **voller Lauf in beiden Kodierungsumgebungen, 283 Einheiten, 410 Meldezeilen, keine ohne `OK`** – oberhalb der Trennlinie **zeilengleich** (324,6 s und 324,4 s), darunter die fünf neuen Einheiten zu Prüfung 70.
- **Kein Lauf am Client für die Befunde selbst, kein Kontingent verbraucht.**
