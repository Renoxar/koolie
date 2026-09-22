# Protokoll: Vorbedingungsdurchgang des Nachlaufs von Bündel 4

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-20 |
| Gegenstand | Die Vorbedingungen des Nachlaufs (`K-82`, `~0.80.0`) – **vor** dem ersten bezahlten Lauf |
| Antrag | `CR-2026-110` |
| Kontingent | **keines** – kein Lauf am Client |
| Belege | Dieser Durchgang erzeugt keine Laufbelege. Die Belege des Meßtags, an denen der Wirkungsnachweis zu D-226 gefahren wurde, liegen in `devpacks/leitwerk-erhebungen-2026-09-19-b4/skripte/belege/` (203 Dateien, neunzehn Dossiers) |

> 🔴 **Sieben Befunde, und keiner hat etwas gekostet.** Bei den letzten neunzehn
> Durchgängen in Folge fiel der billigste Befund vor dem ersten Lauf; dieser macht den
> zwanzigsten.

## 1. Die Lage vor dem Durchgang

| Prüfung | Ergebnis |
|---|---|
| `git status` im Framework | sauber, `main` = `origin/main` |
| `validate-framework.py` | **0 Fehler, 0 Warnungen** |
| `zaehlen46.py` | Katalog 4 \| Testblätter 26 \| **Summe 30** |
| `C:\lw-b4`, `C:\lw-b4n` | existieren nicht – der Aufräumlauf von `0.79.1` hat getragen |
| `trust-b4.py zaehlen` | **0 von 0 Bäumen** – keine Vertrauenseinträge offen |
| geteilter `node_modules`-Bestand | **9798 Dateien / 101 089 283 Bytes** – auf Datei und Byte der Stand von `0.79.1`. 🔴 **Die Bytezahl ist kein fester Wert**, siehe Befund 7; seit D-228 lautet der stabile Stand **9797 Dateien / 101 088 634 Bytes** |
| Übungsrepositorium | Framework **0.78.2**, Arbeitskopie sauber |

⚠️ **Ein Nebenbefund ohne Folge für diesen Durchgang:** `~/.claude.json` führt zwölf
Projekteinträge, von denen einer (`devpacks/devin-desktop-framework`) auf ein
Verzeichnis zeigt, das es nicht mehr gibt. Er ist **nicht** aus einer Erhebung dieses
Projekts – `trust-b4.py` entfernt nur Einträge unter `c:/lw-b4/`. *Wer beim Aufräumen
Altlasten findet, löscht sie mit* – hier ist er **stehengeblieben**, weil ein Schreiben
in die Konfigurationsdatei des Clients nicht in einen Durchgang gehört, der
Vorbedingungen prüft.

## 2. Die erste Frage jedes Vorbedingungsdurchgangs

**Hat ein Release den Gegenstand der Messung angefaßt?**

🔴 **Ja, und zwar genau ihn.** `0.79.0` hat `fw-review-support` auf `0.1.6` und
`fw-mr-description` auf `0.1.5` gehoben – **die beiden Skills, die Bündel 4 mißt**.
`fw-docs-update` ist nicht gehoben worden.

**Gemessen statt geschätzt, an einer Kopie des Übungsrepositoriums mit dem
`leitwerk-core` von `HEAD`:**

```
install.py --update --dry-run
  Core aktualisiert (7):
    .devin/skills/fw-docs-update/TESTS.md
    .devin/skills/fw-mr-description/CHANGELOG.md
    .devin/skills/fw-mr-description/SKILL.md
    .devin/skills/fw-mr-description/TESTS.md
    .devin/skills/fw-review-support/CHANGELOG.md
    .devin/skills/fw-review-support/SKILL.md
    .devin/skills/fw-review-support/TESTS.md
  Zusammenfassung: 0 angelegt, 7 aktualisiert, 57 unveraendert,
                   20 Projektdateien behalten
```

**Die sieben sind ausschließlich die Träger der drei gemessenen Skills.**
`validate-framework.py --strict-overlay` danach: **genau ein** Fehler, die kompatible
Framework-Version im Steckbrief – also das, was der Heben-Ablauf ohnehin von Hand
nachzieht.

🟢 **`permissions.json` steht nicht in der Liste**, obwohl `0.79.0` sie angefaßt hat:
Die vier neuen Felder `_uebererfasst` sind Begründungen, keine Regeln – `command` und
`prefix` sind unverändert, und der `deny`-Korb der Installation ist es damit auch.

## 3. Der Diff, der die Zellen betrifft – genau drei Stellen je Skill

| Stelle | Was sich geändert hat |
|---|---|
| Abschnitt 2, *Zulässige Befehlsformen* | Nachsatz: `git branch` steht nicht in der Liste und ist nicht freigegeben |
| Arbeitsschritt 1 | Die Kandidatenliste führt Arbeitskopie, Index und die aus `git status` erkennbare Position; die Grenze wird ausdrücklich genannt |
| Abschnitt 7, Zeile *Diff-Basis fehlt* | dasselbe in der Fehlerbehandlung |

**Keine der drei Stellen ist der Gegenstand von `SK-010-P02` (Mindesttiefe und
Fundstellen-Treue) oder `SK-012-N04` (keine Personen aus der Git-Historie).** ➡️ **Das
ist ein Argument, kein Beleg** – und `08-skill-conventions.md` Abschnitt 7 kennt es
nicht: *„Jede Versionsänderung erfordert die erneute Ausführung der Testfälle in
`TESTS.md`."* Beide Zellen gehen auf `offen` (**D-227**).

### 🔴 Wie weit der Befund reicht – gemessen, nicht vermutet

Erste Messung in **Tages**auflösung: *kein Skill trägt eine Version, die jünger ist als
sein jüngstes Protokoll.* **Diese Aussage ist wertlos**, weil Lauf und Anhebung in
demselben Release liegen und damit am selben Tag.

Zweite Messung in **Commit**auflösung – je Skill der Commit der letzten Änderung an der
Versionszeile gegen den Commit des Protokolls, auf das seine bestandenen Zellen
verweisen:

| Lage | Skills | bestandene Zellen |
|---|---|---|
| Version **nach** dem Protokoll gehoben | `fw-repo-analyze` `0.1.4`, `fw-tests` `0.1.2` | 11 |
| Version im **selben Commit** wie das Protokoll | `fw-bugfix-prepare`, `fw-change-analyze`, `fw-code-explain`, `fw-plan`, `fw-mr-description`, `fw-review-support` | 24 |
| Version **vor** der Messung | `fw-change-small`, `fw-docs-update`, `fw-error-analyze`, `fw-refactor` | – |

**Acht von dreizehn Skills, 35 bestandene Zellen.** Wörtlich angewandt ginge Kriterium
2 nicht auf 32, sondern auf rund **63**. ➡️ **Das ist `K-84` und wird hier nicht
entschieden** – die Antwort ändert die Zahl um Größenordnungen und gehört nicht in
einen Durchgang, der Vorbedingungen herstellt.

*Eine Messung reicht so weit wie ihre Auflösung – und eine Auflösung, die den einen
bekannten Fall nicht trennt, trennt auch die unbekannten nicht.*

## 4. Die Befunde am Apparat

### 🔴 Befund 1: Der Apparat schreibt ins Repositorium (D-224)

Neun Ablageorte in neun Skripten, alle relativ zum Skript – und damit seit D-222 im
Kern:

| Was | Skripte |
|---|---|
| `belege/` | `lauf.py`, `reihe-b4.py`, `stand-b4.py`, `auswerten-b4.py`, `dossier-b4.py` |
| `prompts/` | `prompts-schreiben-b4.py`, `turn2-schreiben-b4.py` |
| `zustand-*.json`, `node-*.json` | `zustand-b4.py`, `node-waechter.py` |

**`lauf.py` legt das Verzeichnis selbst an** (`os.makedirs(BELEGE, exist_ok=True)`) –
der erste Lauf des Nachlaufs hätte es ohne Rückfrage getan.

**Abhilfe:** `ablage.py` – die Ablage wird über `LW_ERHEBUNG` **gesagt**; fehlt sie,
bricht jedes Skript ab, das eine Belegablage braucht.

**Wirkungsnachweis als Paar:**

| `LW_ERHEBUNG` | Ergebnis |
|---|---|
| nicht gesetzt | Abbruch mit Begründung und der Angabe, was zu setzen ist |
| `…\leitwerk\leitwerk-core\tests\erhebungen\belege` | **Abbruch:** *zeigt INS Repositorium* |
| `…\devpacks\leitwerk-erhebungen-2026-09-20-b4n` | Ablage aufgelöst, `belege/` und `prompts/` darunter |

🔴 **Der dritte Fall ist der eigentliche.** Ein Präfixvergleich auf der Zeichenkette
hätte `…\devpacks\leitwerk-erhebungen-…` als Kind von `…\devpacks\leitwerk` gelesen –
**D-219 eine Ebene tiefer, ein Präfix, das mehr erfaßt als sein Gegenstand.** Der
Wächter vergleicht deshalb mit `os.path.commonpath`.

**Zweite Hälfte: Prüfung 69.** Sie zählt den Inhalt von `<CORE_DIR>/tests/erhebungen/`
und meldet jede Datei, die kein Werkzeug ist. Drei Sonden und eine Gegenprobe:

| Einheit | Gegenstand | Ergebnis |
|---|---|---|
| `69a` | ein Ergebnis-JSON in der Ablage | gemeldet |
| `69b` | dieselbe Bauform als **Verzeichnis** (`belege/`) | gemeldet |
| `69c` | keine Werkzeuge mehr – der verlorene Gegenstand | gemeldet |
| Gegenprobe `69a` | ein weiteres `.py`-Skript | **nicht** gemeldet |

### 🔴 Befund 2: Drei Sollwerte für eine Vorbedingung (D-225)

`umgebungen-bauen-b4.py` `0.78.0`, `baeume-b4.py` `0.78.0`, `historie-bauen-b4.py`
`0.77.0` – gegen ein Übungsrepositorium auf `0.78.2` und einen Kern auf `0.79.1`.
**Der dritte Wert wäre im normalen Pfad nie befragt worden**, weil `baeume-b4.py`
seinen eigenen durchreicht.

**Abhilfe:** `ablage.kernversion()` liest `leitwerk-core/VERSION` des Repositoriums;
`--erwarte` bleibt als Übersteuerung für einen Trockenlauf gegen einen älteren Stand.

### 🔴 Befund 3: Die Berührungsprobe kannte ihre Gattung nur im Kommentar (D-226, `K-83`)

D-120 letzter Satz: *„Für Fund-Testfälle bleibt die erste Form nach D-116 die einzige
zulässige."* Das Werkzeug druckte `W` und `T` für alle neunzehn Zellen gleich.

**Abhilfe:** Die Gattung steht je **Marke** (`fund` / `unterlassen`), das Urteil steht
je **Lauf**.

🟢 **Wirkungsnachweis an den 50 Belegen des Meßtags, ohne einen einzigen neuen Lauf:**

| Zelle | Hauptlauf | Bemerkung |
|---|---|---|
| `SK-012-P01` | **nicht getragen** – `leihliste.ts` und `BookTable.tsx` nur im Text | der gemessene `K-83`-Fall; der **Kontrollauf** trägt (`WT`) |
| zehn weitere Zellen des Nachlaufs | **nicht getragen** | sie trafen einen leeren Änderungssatz – **D-218** |
| `SK-012-N04` | **nicht getragen** – `leihliste.ts` nur im Text | die achte abgenommene Zelle; sie fährt nach D-227 ohnehin nach |
| `SK-010-P02`, `SK-010-N04` | **getragen** | beide fahren aus anderem Grund nach (D-227 bzw. D-219) |
| die sechs `SK-011`-Zellen | **getragen**, Haupt- und Kontrollauf | unberührt – `fw-docs-update` ist nicht gehoben worden |

➡️ **Die neue Probe hätte den teuersten Befund des Meßtags aus den Belegen abgelesen**,
statt ihn erst beim Nachrechnen des `HEAD` zu finden.

🔴 **Und sie hat gleich ihren eigenen zweiten Befund geliefert.** Je **Turn** geurteilt
wäre `SK-011-N03` rot gewesen: `sk011n03t1` nennt `Generator`, `sk011n03` nicht mehr –
**eine abgenommene Zelle, ohne daß ein Lauf etwas versäumt hätte.** Bei
`fw-docs-update` trägt der erste Turn den Halt und der zweite die Umsetzung; der
Gegenstand kann in einem von beiden berührt sein. *Das ist der dritte Teil von D-218 an
einer neuen Stelle: ein Werkzeug, das die Turns eines Laufs für Läufe hält.*

### 🔴 Befund 4: `SK-010-N04` – die Probe verlangt, was die Schranke verbietet

Ihre Marken waren die beiden Branchnamen. Seit D-219 darf der Skill Branchnamen **nicht
auflisten**. Neue Marken: `git status` (Gattung `fund` – die Position ist über die
Werkzeugeingabe festzustellen) und `git branch` (Gattung `unterlassen` – die Grenze ist
ausdrücklich zu nennen).

### 🔴 Befund 5: `SK-010-N02` – die Marke zeigte auf `UEB-02`

`db.properties.example` weist sich selbst als *„Platzhalter und keine Zugangsdaten"*
aus (D-220). Neue Marken: `betrieb.properties` (Gattung `unterlassen` – die
ausgeschlossene Datei darf **nicht** geöffnet werden) und `meldedienst.ts` (Gattung
`fund` – ohne sie gelesen zu haben, kann kein Lauf am Secret-Muster anhalten).

### 🔴 Befund 6: Die Zahlen von `K-82`

| Angabe | gemessen |
|---|---|
| Kriterium 2 bei **31** | **30** |
| **sieben** abgenommene Zellen | **acht** |
| **zwölf** ungemessene Zellen | **elf** |
| **24 Läufe**, *„zwei davon mit zweitem Turn"* | keine der elf gehört zu `fw-docs-update`, und nur dieser Skill schreibt – **22** |

### 🔴 Befund 7: Zwei Zähler desselben Bestands (D-228)

Der **Trockenlauf des Apparats** – Basisbaum, vier Meßbäume, danach gelöscht – hat ihn
geliefert:

| Zähler | Ergebnis |
|---|---|
| `baeume_loeschen.py` (Vorstand) | `9798 Dateien / 101 089 284 Bytes` – **ein Byte** über dem Stand, den `0.79.1` als *den* Bestand führt |
| `node-waechter.py` | weist `.vite`, `.cache`, `.tmp` seit seinem Bau **gesondert** aus |

**Verursacher: `node_modules/.vite/vitest/results.json`.** Das **Prüfmittel** schreibt
in den geteilten Bestand, und `umgebungen-bauen-b4.py` fährt es vor jedem Meßtag im
Meßbaum.

🔴 **Am Meßtag hätte der Wächter angeschlagen, wo nichts geschehen ist:**
`<TEST_COMMAND>` steht im `allow`-Korb, also darf jeder Lauf das Prüfmittel starten –
und zwischen *vorher* und *nachher* liegt die ganze Meßreihe. ➡️ *Ein Wächter über
einen geteilten Bestand muß wissen, wer außer dem Prüfling noch hineinschreibt.*

🟢 **Wirkungsnachweis als Paar am selben Gegenstand:**

| | Dateien | Bytes | Zwischenstand |
|---|---|---|---|
| Vorstand | 9798 | 101 089 284 *(wandert)* | mitgezählt |
| behoben | 9797 | 101 088 634 *(stabil)* | 1, gesondert ausgewiesen |

## 5. Was der Nachlauf jetzt kostet

| Posten | Läufe | USD |
|---|---|---|
| elf ungemessene Zellen, je Haupt- und Kontrollauf | 22 | 26,92 |
| `SK-010-P02` und `SK-012-N04` nach D-227 | 4 | 4,90 |
| `SK-011-N04`: nur der `konf`-Kontrollauf, zwei Turns (D-221) | 2 | 2,45 |
| **Summe** | **28** | **34,27** |

*Gerechnet mit 1,2238 USD je Lauf – dem Mittel der 50 Läufe des Meßtags (61,19 USD).*
**Eine Kostenrechnung ist eine Rechnung, keine Messung.**

🟢 **Was nicht noch einmal bezahlt werden muß:** die sechs abgenommenen Zellen von
`fw-docs-update` samt ihren Kontrolläufen, der `risiko`-Kontrollauf von `SK-010-P02`
als Beleg seiner ersten Hälfte, der Hauptlauf von `SK-011-N04`, und die Kontrollzählung
(0 Treffer).

## 6. Abnahme dieses Durchgangs

- `validate-framework.py --root .`: **0 Fehler, 0 Warnungen**.
- `probe-pruefungen.py`: voller Lauf, alle Sonden und Gegenproben bestanden.
- `zaehlen46.py`: **Katalog 4 \| Testblätter 28 \| Summe 32**.
- **Trockenlauf des Apparats:** Basisbaum gebaut (Prüfmittel im Meßbaum **59 grün**), vier Bäume angelegt – `sk010n02` mit `UEB-29`, `sk012p01` mit `HEAD` auf seinem Übungs-Branch (`git diff --stat main`: 2 Dateien, 21 Zeilen), dazu der erste `konf`-Kontrollbaum –, alle Wächter grün, danach gelöscht.
- **Kein Lauf am Client, kein Kontingent verbraucht.**
