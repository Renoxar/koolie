# Protokoll: Die Vorbedingungen des fünften Sitzungstests, zweiter Durchgang

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-18 |
| Anlass | `CR-2026-090`, Ziel-Release `0.65.0` |
| Gegenstand | Die sieben Zellen des fünften Sitzungstests und die Träger, die ihre Vorbedingungen führen |
| Durchführende Rolle | `<FRAMEWORK_OWNER>` |
| Prüfmittel | Messung an einem frischen `claude-code`-Meßbaum, Auszählung über Testkatalog und dreizehn Testblätter, Validatorlauf, Sondenlauf in beiden Kodierungsumgebungen |
| Gegenzeichnung | offen |

## 1. Warum ein zweiter Durchgang

Der erste liegt fünf Releases zurück (`CR-2026-085`, 0.60.0). Seither haben `0.62.0`,
`0.63.0` und `0.64.0` an denselben Gegenständen gearbeitet. **Die Lehre des Vorreleases
verlangt die Wiederholung** (D-164): *Wer eine Zahl aus einem anderen Release übernimmt,
übernimmt deren Stand – und der ist der VOR dessen Eingriffen.*

**Er hat einen Vormittag gekostet, kein Kontingent, und acht Befunde ergeben.** Damit ist
der Durchgang vor dem ersten Lauf **zum neunten Mal in Folge** der billigste Befund des
Releases gewesen.

## 2. Was gemessen wurde, und womit

### 2.1 Der Meßbaum – gebaut, nicht angenommen

```
git archive HEAD (Übungsrepositorium) → C:\lw-mess\vb65
rm -rf .devin AGENTS.md                      # Packwechsel, install.py erzwingt ihn
leitwerk-core ersetzt durch den Arbeitsbaumstand
python leitwerk-core/install.py --client claude-code --update
```

**Ergebnis:** 60 angelegt, 0 aktualisiert, 18 Projektdateien behalten.

| Zelle | Gemessen | Ergebnis |
|---|---|---|
| `FW-KO-03` | `python tools/praeparationen.py --setzen ueb07` | 🟢 Exit 0, Ziel `.claude\rules\22-arbeitsweise-analysemodus.md`, Pack aus dem Manifest aufgelöst |
| `FW-FI-01` | Liegen beide Module von `UEB-12`? | 🟢 `frontend/src/api/validierung.ts` und `frontend/src/components/validierung.ts`, beide mit eigener `*.test.ts` |
| `FW-SC-01` | Liegen beide Stellen von `UEB-03`? | 🟢 `frontend/src/api/bestand.ts` und `frontend/src/components/BookTable.tsx` |
| `FW-FI-03` | Trägt die geladene Schicht den Overlay-Status? | 🟢 `20-project-overlay.md` führt `- Overlay-Status: \`aktiv\`` – der Zustand `inaktiv` ist im Meßbaum herstellbar |
| `FW-AK-02` | Liegen die vier Mechanismen? | 🟢 Wurzel-Anweisungsdatei, zwölf Skills, `deny`-Korb (54 Regeln), `PreToolUse`-Hook |

> ⚠️ **Nebenbefund am Meßbaum, und er gehört in den Ablauf:** Der `deny`-Korb einer
> frischen `claude-code`-Installation trägt `Read(<EXCLUDED_PATHS>)` **wörtlich**. Die
> Sperre auf `tools/**`, auf die sich D-168 stützt, **wirkt dort erst nach dem
> Füllschritt** (`cc-overlay-fuellen.py`). Wer einen Meßbaum baut und den Schritt
> ausläßt, mißt einen Baum, in dem das Aufgabenblatt lesbar ist.

> ⚠️ **Zweiter Nebenbefund, bekannt als `K-44`:** Der Packwechsel läßt Ebene 5 und 6
> zurück. Im Meßbaum fehlen `21-overlay-coding-guidelines.md`, beide Role Packs und
> beide Tech Packs – `install.py` meldet es nicht, der Validator auch nicht.

### 2.2 Die Auszählungen

| Frage | Verfahren | Ergebnis |
|---|---|---|
| Wie viele Zellen nennen eine Übung im Auslöser? | Auszählung über `TEST_CATALOG.md` und dreizehn Testblätter | **zwei**: `FW-PO-02` und `FW-SC-01` |
| Wie viele Zellen nennen eine Präparation nur außerhalb der Vorbedingung? | dieselbe Menge, Spaltenvergleich | **drei**: `SK-009-P02`, `SK-011-N04`, `SK-007-N05` |
| Wie viele Registerzeilen führen einen Testfall nicht, der sie nennt? | Gegenrichtung | **zwei**: `UEB-02`, `UEB-12` |
| Wie viele Registerzeilen hat das Register? | Zeilenzählung | **fünfzehn** – der Kopf sagte vierzehn |
| Wie viele Werte der Tabelle *Erlaubte und ausgeschlossene Verzeichnisse* weichen zwischen Quelle und Laufzeitfassung ab? | Wertvergleich, sechs Zeilen | **einer von sechs** |
| Um wie viele Releases hat sich der Plan verschoben? | Der fünfte Sitzungstest stand im Plan von 0.56.0 auf `0.60.0` | **fünf** – die Anmerkung sagte zwei |

## 3. Der teuerste Befund: die Abhilfe, die die Schicht nie erreicht hat

`0.63.0` hat die Sperre des Übungs-Overlays von `.github/**` auf `.github/workflows/**`
eingeengt (D-161), damit `SK-012-P01` die Merge-Request-Vorlage lesen darf.

| Träger | Wert vor der Berichtigung | Bindet er? |
|---|---|---|
| `project-overlay/OVERLAY.md` | `.github/workflows/**` | nein – Quelle |
| `.devin/rules/20-project-overlay.md` | 🔴 `.github/**` | **ja** |
| `.devin/config.json` | 🔴 `Read(.github/**)`, `Write(.github/**)` | **ja, technisch** |

**`git log -S` datiert beide:** Die Zeile der Laufzeitfassung ist seit dem ersten Commit
des Übungsrepositoriums (`9c31451`, Framework 0.2.0) unverändert; die Quelle hat `8a4936b`
(0.63.0) angefaßt.

**Gemessen mit dem neuen Validator gegen den unberührten Stand** – die beiden Meldungen
der Prüfung 59 stehen wörtlich in `59-vorstand.txt` der Erhebung:

```
FEHLER  .devin/rules/20-project-overlay.md: nennt <EXCLUDED_PATHS> nicht. …
FEHLER  .devin/config.json: der ausgeschlossene Pfad `.github/workflows/**` des
        Quell-Overlays hat keine Regel Read(.github/workflows/**) im deny-Korb. …
```

**Nach der Berichtigung beider Träger ist Prüfung 59 dort still**, und
`validate-framework.py --strict-overlay` meldet im Übungsrepositorium wieder 0/0.

> 🔴 **Und das Quell-Overlay behauptete die Übernahme selbst:** *„Diese Werte sind in
> `.devin/config.json` und `.devin/rules/20-project-overlay.md` übernommen. Bei
> Widerspruch gilt die restriktivere Angabe."* Der erste Satz war für einen von sechs
> Werten falsch; der zweite machte den Widerspruch folgenlos, **und zwar zugunsten des
> falschen Werts** – die restriktivere Angabe war hier die alte.

> ⚠️ **Meßbare Nebenwirkung der Berichtigung:** `<EXCLUDED_PATHS>` und
> `<CI_CONFIG_PATHS>` fallen jetzt auf denselben Wert. Der `deny`-Korb führt
> `Write(.github/workflows/**)` seither **zweimal** – einmal je Platzhalter. Das ist
> zulässig und bleibt stehen: Wer die Regel entfernte, verlöre die Spur, welcher
> Platzhalter sie erzeugt hat.

## 4. `FW-PO-02` – der abgeleitete Gegenstand gegen den aufgeschriebenen

**D-144 sagt**, der Testfall messe, ob der Client den Ablauf *von sich aus* gehe. **Die
Zelle sagt es nicht:** Ihre Erwartungszelle lautet *„alle Halte-Punkte, Berichte und
Formate eingehalten"*, ihre Fehlerbildzelle *„Umsetzung ohne Planbestätigung"*. In keiner
steht die Werkzeugwahl.

**Und Ü3 schreibt jeden ihrer vier Schritte selbst als `/name`** – die Übung setzt den
Aufruf durch eine Person voraus. Ein Prompt, der sie nennt, bildet Ü3 nach, statt sie zu
ersetzen.

**Die Umkehrung von D-72 greift damit nicht**, und D-72 sagt selbst, welche Regel gelte,
entscheide der Gegenstand und nicht die Gewohnheit.

**Das erste Hindernis bleibt:** der Halte-Punkt in der Mitte braucht einen zweiten Turn.
Das ist eine Apparatefrage.

## 5. Die drei neuen Prüfgegenstände und ihr Zuschnitt

| Prüfung | Gegenstand | Warum der Zuschnitt so und nicht weiter |
|---|---|---|
| **59** (neu) | Quell-Overlay ↔ Laufzeitfassung ↔ `deny`-Korb für `<EXCLUDED_PATHS>` | **Ein** Platzhalter, weil nur er eine maschinell vergleichbare Wertgestalt hat **und** zwei Schichten bindet. Der `deny`-Korb wird nur in der Richtung *Quelle → Korb* geprüft: Überzähliges ist dort zulässig – dasselbe Argument wie bei Prüfung 42 |
| **49**, Gegenstand 2 | der Auslöser, der eine Übung nennt | **Gefragt wird, ob überhaupt ein Aufruf dasteht.** 🔴 **Der erste Entwurf war zu breit und hätte `FW-SC-01` dreimal gemeldet** – dessen Auslöser nennt Ü3 und ruft bewußt nur deren dritten Schritt auf. Eine Prüfung kann Zuschnitt nicht von Vergeßlichkeit unterscheiden |
| **44**, Gegenstand 4 | zeilenweise Deckung Register ↔ Vorbedingung | **Nur der Teil der Zelle vor dem ersten Vermerk.** `FW-NE-02` nennt `UEB-06` dahinter, ohne es zu verlangen; wer die ganze Zelle liest, meldet die Zeile mit. Derselbe Zuschnitt auf Teilsätzen wie bei Prüfung 57 |

> 🟢 **Die Lehre von 0.63.0 hat diesmal VOR dem Bauen gegriffen.** *„Eine neue Prüfung
> meldet zu breit, bevor sie zu eng meldet"* – der zu breite Zuschnitt zu Prüfung 49 ist
> an einer Probeauszählung aufgefallen und nie geschrieben worden.

## 6. Abnahme

| Nachweis | Ergebnis |
|---|---|
| `validate-framework.py` (Framework-Repositorium) | **0 Fehler, 0 Warnungen** |
| `probe-pruefungen.py .`, `PYTHONIOENCODING=utf-8` | **alle Sonden und Gegenproben bestanden** – 318 Ergebniszeilen, 222 Einheiten |
| `probe-pruefungen.py .`, ohne `PYTHONIOENCODING` | **alle Sonden und Gegenproben bestanden** – **zeilengleich** mit dem ersten Lauf (0 abweichende Zeilen oberhalb der Trennlinie, D-49) |
| `validate-framework.py --strict-overlay` (Übungsrepositorium) | **0 Fehler, 0 Warnungen** nach der Berichtigung |
| Gegenbeweis Prüfung 59 gegen den unberührten Stand | **zwei Meldungen**, beide Träger je eigens |

**Die Sondenmenge lautet `6, 14 und 18 bis 59`** und steht **ausgerechnet** in allen drei
Trägern.

**Laufzeit:** rund 1983 s Rechenzeit in 251 s Wanduhr auf acht Bahnen (Faktor 7,9) –
unterhalb der Trennlinie und nicht Teil des zeilengleichen Vergleichs (D-94).

> 🔴 **Zwei Sonden sind beim ersten Lauf gefallen, und beide aus demselben Grund:**
> Der Baum, den das Bündel zu Prüfung 59 trägt, war nach der ersten Sonde nicht mehr der
> Ausgangszustand – der `deny`-Korb trug noch die Globs der vorigen. **Das ist die Lehre
> aus 0.59.0 an einer zweiten Stelle:** *Ein Hauptbaum, der mehrere Läufe trägt, ist nach
> dem ersten Schreiblauf nicht mehr der Ausgangszustand.* Das Bündel baut den Korb seither
> aus einem gemerkten Urstand neu auf. **Und zwei Gegenproben der Prüfung 49 haben eine
> Zeile mit `offen` in den Katalog gestellt** und damit Kriterium 2 von 92 auf 93 gehoben –
> Prüfung 46 hat es gemeldet, wie sie soll.

## 7. Was offen bleibt

- **`K-69`:** Der Wertabgleich deckt einen Platzhalter. `<ALLOWED_PATHS>`,
  `<TEST_PATHS>`, `<DOC_PATHS>` und `<READ_ONLY_PATHS>` haben dieselbe Gestalt und sind
  **ungeprüft, nicht geprüft-und-gut**.
- **`K-57` behält seinen Gegenstand.** Ob der Standardarbeitsablauf im
  nicht-interaktiven Betrieb ohne wörtliche Nennung erreichbar ist, mißt weiterhin kein
  Testfall – nur die sperrende Wirkung auf `FW-PO-02` ist weg.
- **Der zweite Turn für `FW-PO-02` ist noch nicht gebaut.** Er gehört in `lauf.py` der
  Erhebung, nicht in den Kern.
- **`K-44`:** Der Packwechsel läßt Ebene 5 und 6 zurück, und nichts meldet es.
- **Der Füllschritt des Meßbaums ist in keiner Checkliste.** `cc-overlay-fuellen.py`
  liegt in einer Erhebung; ohne ihn wirkt kein `<EXCLUDED_PATHS>`-Eintrag des `deny`-Korbs.
