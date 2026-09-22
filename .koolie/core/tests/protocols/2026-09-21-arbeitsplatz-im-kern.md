# Protokoll: Der Arbeitsplatz im Kern – und ein Werkzeug, das auf ein Datum wartete

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-21 |
| Gegenstand | Die Werkzeuge des Meßapparats, gefunden beim Bau der Dossiers des Nachlaufs |
| Antrag | `CR-2026-112` |
| Kontingent | **keines** – kein Lauf am Client |
| Belege | Dieser Durchgang erzeugt keine Laufbelege. Die Dossiers liegen in `devpacks/leitwerk-erhebungen-2026-09-20-b4n/belege/dossier/` |

> 🔴 **Zwei Befunde, beide beim Bau der Dossiers, beide vor der Auswertung der
> Zellen.** Der eine hat den Lauf angehalten; der andere wäre ohne ihn nicht gesehen
> worden.

## 1. Die Lage vor dem Durchgang

| Prüfung | Ergebnis |
|---|---|
| `git status` | sauber, `main` = `origin/main` auf `e732ddf` (`0.79.3`) |
| `validate-framework.py` | **0 Fehler, 0 Warnungen** |
| Nachlauf | **28 von 28 Läufen gültig**, Zustandsaufnahme *nachher* genommen |
| `auswerten-b4.py` | gefahren, 30 Läufe, Kontrollzählung **0 Treffer** |

## 2. Der Abbruch, der beides sichtbar gemacht hat

```
> python leitwerk-core\tests\erhebungen\dossier-b4.py
ABBRUCH: …\belege\auswertung-2026-09-20.log fehlt - erst auswerten-b4.py
```

**Die Auswertung war gefahren** – nur eben am 21. Der Dateiname stand als Zeichenkette
im Quelltext. Und in derselben Datei, zwei Zeilen darüber:

```python
KERN = os.path.join(r"C:\Users\<konto>\Documents\devpacks\leitwerk", "leitwerk-core")
```

## 3. Befund 1: Neun Werkzeuge nennen einen Arbeitsplatz (D-231)

**Gemessen über den ganzen Kern, vor dem Eingriff:**

| | Träger |
|---|---|
| **Werkzeuge** mit einem Benutzerprofilpfad samt Kontonamen | **8** (dazu ein Kommentar in `auswerten-b4.py`) |
| **Aufzeichnungen** mit demselben Namen | **10** – acht Protokolle, zwei Änderungsanträge |
| **Summe** | **18** |

Acht Werkzeuge zeigten auf `…\devpacks\test-devin-framework` (das
Übungsrepositorium), zwei auf das Repositorium selbst.

Solange der Apparat **neben** dem Repositorium lag, stand das in einer unversionierten
Ablage. **Mit D-222 ist er hineingewandert und hat die Pfade mitgebracht** – in
dasselbe Repositorium, für das `0.78.1` eigens `UEBERGABE.local.md` eingeführt hat,
weil eine Übergabe mit Servername und Konto den Validator mit drei Fehlern und drei
Warnungen beantwortet.

> *Wer einen Apparat umzieht, zieht seine Arbeitsplatzpfade mit um – und veröffentlicht
> sie, ohne es zu entscheiden.*

### 🔴 Keine der siebzig Prüfungen sah es

Prüfung 6 kennt Secret-Muster, E-Mail-Adressen, IP-Adressen, interne Hostnamen und URLs
außerhalb der Allowlist. **Ein Pfad in ein Benutzerprofil ist nichts davon – und trägt
trotzdem den Namen eines Menschen.**

**Abhilfe:** Der Pfad des Übungsrepositoriums wird **gesagt**
(`LW_UEBUNG`, `ablage.uebungsrepositorium()`, dieselbe Form wie `LW_ERHEBUNG` nach
D-224), der Pfad des Repositoriums **abgeleitet** (`ablage.WURZEL`). **Prüfung 71**
meldet jeden absoluten Pfad in ein Benutzerprofil, dessen Kontosegment kein Platzhalter
ist und dessen Zeile keine Begründung trägt – dieselbe Bauform wie das Feld
`_uebererfasst` von Prüfung 68.

**Bestand danach: null Werkzeuge, zehn Aufzeichnungen.**

### ⚠️ Die Grenze steht hier, und sie ist gesagt

`tests/protocols/` und `governance/change-requests/` sind **ausgenommen**. Sie halten
fest, **wo** gemessen wurde – meist in der Form *„außerhalb von `C:\Users\…`"* –, und
ein Protokoll, das man umschreibt, ist keines mehr (D-141). **Was daraus folgt, ist
`K-85` und hier nicht entschieden.** Die Prüfung schweigt darüber, statt es durch ihren
Zuschnitt stillschweigend zu entscheiden.

## 4. 🟢 Prüfung 70 hat ihren ersten echten Fang gemacht – am Eingriff selbst

Die Umstellung ließ in **drei** Werkzeugen den Aufruf `ablage.…` stehen, **ohne den
Import**:

```
FEHLER  leitwerk-core/tests/erhebungen/baeume_loeschen.py:   der Name `ablage` … nirgends gebunden
FEHLER  leitwerk-core/tests/erhebungen/cc-overlay-fuellen.py: der Name `ablage` … nirgends gebunden
FEHLER  leitwerk-core/tests/erhebungen/zaehlen46.py:          der Name `ablage` … nirgends gebunden
```

**Der Validator meldete drei `NameError`, bevor ein Lauf sie fand** – genau der Fall,
für den Prüfung 70 einen Tag zuvor entstanden ist, und genau die Bauform, an der
`stand-b4.py` elf Tage lang tot war. *Ein Wächter, der am Tag nach seinem Bau den
ersten echten Fall meldet, hat seinen Anlaß nicht erfunden.*

## 5. Befund 2: Ein Werkzeug wartete auf ein Datum (D-232)

Der Dateiname `auswertung-2026-09-20.log` stand im Quelltext. Das ist die Bauform von
D-225 (drei `--erwarte`-Sollwerte, keiner stimmte) und D-153 (*eine Zahl, die gepflegt
werden muß, wird nicht gepflegt*), diesmal als **Datum**.

> *Ein Werkzeug, das die Ausgabe eines anderen beim Namen nennt, wartet auf den Tag, an
> dem jemand diesen Namen anders wählt.*

**Abhilfe:** `dossier-b4.py` fährt `auswerten-b4.py` **selbst** und legt dessen
Protokoll mit dem Datum **dieses** Laufes neben die Belege. 🟢 **Nebenwirkung,
gewollt:** Ein Dossier kann nicht mehr aus einer veralteten Auswertung entstehen.

## 6. Die berichtigten Werkzeuge sind gefahren

| Werkzeug | Ergebnis |
|---|---|
| `zaehlen46.py` | Katalog 4 \| Testblätter 28 \| **Summe 32** – unverändert |
| `node-waechter.py zaehlen` | **9797 Dateien, 96,4 MB** (dazu 1 Zwischenstandsdatei) – der stabile Stand nach D-228 |
| `dossier-b4.py` | **19 Dossiers**, *„Jede Zelle hat eine Blattzeile UND einen Auswertungsblock"* |

## 7. Abnahme dieses Durchgangs

- `validate-framework.py --root .`: **0 Fehler, 0 Warnungen**.
- `probe-pruefungen.py --nur 71`: **sechs von sechs Einheiten bestanden** – Sonden `71a`
  bis `71c`, Gegenproben `71a` bis `71c`. Gegenprobe `71c` belegt die angesagte Grenze:
  Eine Aufzeichnung bleibt unbeanstandet.
- `probe-pruefungen.py`: **voller Lauf in beiden Kodierungsumgebungen, 289 Einheiten, 416 Meldezeilen, keine ohne `OK`** – oberhalb der Trennlinie **zeilengleich** (345,0 s und 337,2 s), darunter die sechs neuen Einheiten zu Prüfung 71.
- **Kein Lauf am Client, kein Kontingent verbraucht.**
