# Wirkungsnachweise 0.55.0

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-18 |
| Framework-Version | `0.55.0` (Vorstand `0.54.1`, Commit `c8c8ab4`) |
| Antrag | `CR-2026-077`, D-120 bis D-123, `K-47` bis `K-49` neu |
| Gegenstand | **Ein Regressionsnachweis, kein Wirkungsnachweis einer neuen Prüfung.** Dieses Release baut und ändert **keine** Prüfung (E4 des Antrags); es ändert zwei Verfahren des Testkatalogs, einen Belegstatus im Kern, eine Einstufungszeile eines ausgelieferten Client Packs und füllt sechs Ergebniszellen |
| Prüfmethode | Validatorlauf gegen den fertigen Baum; Sondenlauf `probe-pruefungen.py .` in **beiden** Kodierungsumgebungen (D-49); Gegenbeweis für Prüfung 46 am gemischten Stand; Trockenlauf `install.py --update --dry-run` gegen je eine Kopie beider übernehmender Projekte |
| Ergebnis | **Validator 0 Fehler, 0 Warnungen; 254 Ergebniszeilen bestanden in beiden Kodierungsumgebungen** – zeilengleich mit 0.54.1. Prüfung 46 hat zum achten Mal gegriffen |

---

## 1. Was dieses Release NICHT tut, und warum das hier steht

**Es baut keine Sonde und ändert keine Prüfung.** Die Sondenmenge bleibt bei 254
Ergebniszeilen (159 Sonden, 65 Gegenproben, 12 Selbstproben, 18 Bündelkopfzeilen), die
Spanne, die Prüfung 40 nachrechnet, bleibt unverändert, und das Register im Kopfkommentar
des Validators endet weiterhin bei Prüfung 47.

**Das ist eine Entscheidung mit benanntem Preis** (E4): Drei gemessene Befunde bleiben
ungeprüft – `K-47`, `K-48` und `K-49`. Der schwerste ist `K-47`: Ein Projekt, das seinen
`allow`-Korb auf `Bash(git:*)` verbreitert, verliert den Schutz auf Fernwirkung, **ohne
dass eine Meldung erscheint**.

> **Der Grund für die Vertagung ist derselbe wie bei 0.54.0, und er ist diesmal genauer
> zu benennen:** Eine Prüfung für `K-47` müsste **Befehlsäquivalenz** erkennen – dass
> `git -C <pfad> push` dasselbe tut wie `git push` –, und das ist keine
> Zeichenkettenaussage. Eine Prüfung für `K-48` müsste erkennen, was in Prosa ein Verweis
> ist. **Beide wären Prüfung 29 in einem neuen Gegenstand, mit deren seit dem 2026-09-13
> bekannter Grenze.**

---

## 2. Der Wächter hat gegriffen – zum achten Mal

Nach dem Füllen der sechs Ergebniszellen und **vor** dem Nachziehen der Standzeile:

```
FEHLER   leitwerk-core/docs/ROADMAP.md: Kriterium 2 von D-11 (Testkatalog und dezentrale
         Testblätter ohne `offen`) ist gezählt **105**, die Standzeile nennt 111 – der
         Fortschritt ist nicht nachgezogen.
```

**Achte Gelegenheit, achter Treffer, kein Rückfall darunter.** Es ist die zweite, die
Kriterium 2 betrifft, und die zweite in Folge.

> Der Zähler sagt nicht, ob jemand eine Zahl senkt – **er sagt, ob die geschriebene Zahl
> stimmt.** Ohne diese Bauform stünde in der Roadmap heute `111`.

---

## 3. Die Läufe

### 3.1 Validator

| Lauf | Zuschnitt | Ergebnis |
|---|---|---|
| V1 | `--root .` nach dem Füllen der Zellen, **vor** der Standzeile | **1 Fehler** – Prüfung 46, siehe Abschnitt 2 |
| V2 | `--root .` nach dem Nachziehen von Standzeile und Kriterientabelle | **0 Fehler, 0 Warnungen** |
| V3 | `--root .` gegen den Baum mit Änderungsverzeichnis und Antrag | **0 Fehler, 0 Warnungen** |
| V4 | `--root .` gegen den **fertigen** Baum, dieses Protokoll eingeschlossen | **0 Fehler, 0 Warnungen** |

### 3.2 Sondenlauf

| Lauf | Kodierungsumgebung | Ergebniszeilen | Wanduhr |
|---|---|---|---|
| A | ohne `PYTHONIOENCODING` | **254, alle bestanden** | 143,3 s |
| B | mit `PYTHONIOENCODING=utf-8` | **254, alle bestanden** | 134,6 s |
| C | ohne `PYTHONIOENCODING`, gegen die **Endfassung** | **254, alle bestanden** | 134,7 s |
| D | mit `PYTHONIOENCODING=utf-8`, gegen die **Endfassung** | **254, alle bestanden** | 136,8 s |

**Vier Läufe, vier Mal 254 Ergebniszeilen, kein Fehlschlag – zeilengleich untereinander
und zeilengleich mit 0.54.1.** Beide Kodierungsumgebungen sind abgedeckt (D-49), und die
Läufe C und D laufen gegen den Baum **einschließlich** dieses Protokolls: `probe-pruefungen.py`
kopiert je Sonde das ganze Verzeichnis, und eine Datei, die den Validator stört, lässt
**alle Gegenproben** scheitern, während die Sonden grün bleiben.

**Die Laufzeiten stehen unterhalb der Trennlinie und sind nicht Teil des zeilengleichen
Vergleichs** (D-94) – ihr Eintrag ändert nichts, was eine Prüfung liest.

---

## 4. Gegenbeweis gegen den Vorstand

Ein Gegenbeweis im üblichen Sinn – *„die neue Prüfung fällt gegen den Vorstand"* – ist
hier nicht führbar, **weil keine neue Prüfung existiert.** Was stattdessen belegbar ist
und belegt wurde:

| Gegenstand | Vorstand `0.54.1` | Stand `0.55.0` |
|---|---|---|
| Prüfung 46, Kriterium 2 | gezählt 111, Standzeile 111 → grün | gezählt 105, Standzeile 105 → grün |
| dieselbe Prüfung gegen den **gemischten** Stand | – | **rot** (Abschnitt 2) |

**Der gemischte Stand ist der Gegenbeweis.** Er ist nicht konstruiert worden, sondern
zwangsläufig entstanden: Zwischen dem Füllen der Zellen und dem Nachziehen der Standzeile
liegt genau der Zustand, den Prüfung 46 fangen soll – und sie hat ihn gefangen.

---

## 5. Der Gegenbeweis, den dieses Release wirklich braucht: der Träger gegen den Befund

**Das Messprotokoll hat einen Befund eingeordnet, und die Einordnung hat gegen den Träger
nicht gehalten.** Das ist die Gegenprüfung nach D-23, und sie ist hier der eigentliche
Wirkungsnachweis.

| Schritt | Behauptung | Prüfung | Ergebnis |
|---|---|---|---|
| 1 | Der Vorbehalt zu B6 *„nennt die Breite und verschweigt die Schmalheit"* | Vollständiges Lesen der Zelle in `clients/claude-code/CLIENT_PACK.md` Abschnitt 4 | **widerlegt** – die Zelle endet mit *„Ihre Grenze nennt B6: eine andere Schreibweise desselben Befehls, etwa `git -C . push`"* |
| 2 | Der Satz ist neu oder jüngeren Datums | `git log -S "Ihre Grenze nennt B6" -- <datei>` | **Commit `91d967d`, 2026-09-10, Release 0.15.0** |
| 3 | „seit jeher" / „seit vielen Releases" | `git log --oneline --grep='^Release ' 91d967d..main \| wc -l` | **42** – ausgerechnet, nicht geschätzt |
| 4 | Der Verweis löst sein Versprechen ein | Lesen von Zeile B6 der Fähigkeitsmatrix | **nein** – dort stand ausschließlich *„Wirkt breiter als eine Verweigerung des vollständigen Befehls"* |

> ➡️ **Der Befund ist dadurch kleiner und schärfer geworden.** Kleiner: Der Träger hat die
> Grenze nicht verschwiegen. Schärfer: **Er hat sie an einer Stelle gesagt, die für sie
> auf eine andere Stelle verweist, an der sie fehlt** – zweiundvierzig Releases lang, bei
> durchgehend grünem Lauf. Prüfung 12 prüft **Pfade**; ein Verweis auf eine Zeilenkennung
> im selben Dokument ist kein Pfad (`K-48`).
>
> **Die Lehre, und sie ist neu:** *Ein Befund aus einer Messung gehört gegen den Träger
> gehalten, bevor er als „der Träger verschweigt es" eingeordnet wird.* Die Abhilfe ist
> dann eine andere: nicht einen fehlenden Satz ergänzen, sondern einen vorhandenen dorthin
> stellen, wo die Einstufung steht.

**Was daraus im Träger geworden ist** (D-123): Zeile B6 trägt die Grenze, ihren Beleg
(`PX1`, `PX2`, Wirkung am Remote nachgeprüft) und den Hinweis, dass die ausgelieferte
Fassung über den `allow`-Korb hält. Der Vorbehalt führt beide Richtungen. Die Einleitung
des Abschnitts sagt nicht mehr, die Abweichung sei eine Verschärfung. **Die Einstufung
`[TECHNISCH]` bleibt** – der Mechanismus setzt durch, was er trifft.

---

## 6. Der Migrationshinweis ist gemessen, nicht abgeleitet

**Die Lehre von 0.54.1 ist eingehalten.** Vor dem Schreiben des Hinweises:

1. Je eine Kopie beider übernehmender Projekte aus `git archive HEAD`.
2. `leitwerk-core/` darin durch den **Arbeitsbaum dieses Release-Kandidaten** ersetzt.
3. `python leitwerk-core/install.py --update --dry-run --root <kopie>`.

| Projekt | Client Pack | angelegt | aktualisiert | unverändert | Projektdateien behalten |
|---|---|---|---|---|---|
| Pilot (`otp-generator`) | `claude-code` | 0 | **0** | 58 | 20 |
| Übungsrepositorium (`test-devin-framework`) | `devin-desktop` | 0 | **0** | 64 | 20 |

**Der Hinweis lautet damit „keiner", und er ist belegt.** Anders als bei 0.54.0 ist
diesmal auch kein Testblatt eines Skills berührt (`K-46`): Gefüllt wurden ausschließlich
Zellen des **zentralen** Katalogs, und `tests/TEST_CATALOG.md` liegt nicht in der
Laufzeitschicht.

> **Warum der Trockenlauf trotzdem gefahren wurde, obwohl die Ableitung diesmal
> offensichtlich schien:** Genau so klang sie bei 0.54.0 auch. Er kostet eine Minute.

---

## 7. Zahlen dieses Releases, nachgezählt

| Zahl | Behauptet | Nachgezählt | Quelle |
|---|---|---|---|
| offene Ergebniszellen vorher | 111 | **111** | Prüfung 46 gegen den Vorstand |
| davon im Katalog | 28 | **28** | unabhängige Auszählung mit der Regel von Prüfung 46 |
| davon in den Testblättern | 83 | **83** | dieselbe |
| gefüllte Zellen | 6 | **6** | `git diff` über `tests/TEST_CATALOG.md` |
| offene Ergebniszellen nachher | 105 | **105** | Prüfung 46 **und** die unabhängige Auszählung: `Katalog: 22 \| Testblaetter: 83 \| SUMME: 105` |
| offene Zellen mit `UEB-`Kennung | 6 von 105 | **6** | im Katalog 5 von 22, in den Testblättern 1 von 83 – zwei getrennte Auszählungen |
| Läufe der Erhebung | 23 | **23** | Belegdateien, vier je Lauf |
| Releases seit dem Satz über die Grenze von B6 | 42 | **42** | `git log --grep='^Release ' 91d967d..main` |
| Ergebniszeilen des Sondenlaufs | 254 | **254** | vier Läufe, je einzeln gezählt |

> ⚠️ **Eine Zahl dieses Vorgangs war zunächst falsch, und sie stand in der Übergabe.**
> Der Vorbehalt zu B6 wurde als Stelle geführt, die die Grenze **verschweigt**; er nennt
> sie seit 0.15.0. **Gefunden beim Gegenprüfen am Träger, nicht beim Schreiben** – und die
> zweite Zahl daneben („seit jeher") war gar keine, sondern eine Wendung. Ausgerechnet
> sind es **zweiundvierzig Releases**.
>
> **Die Zählregel von Kriterium 2 ist zweimal unabhängig angewandt worden** – von
> Prüfung 46 und von einem Skript, das sie nachbildet. Beide kommen auf 105. Das ist kein
> Zufallstreffer, sondern die Lehre aus 0.54.0: Dort lag die erste eigene Auszählung bei
> 103 statt 118, weil sie eine Kennung in der ersten Spalte verlangte.

---

## 8. Gegenzeichnung

| Frage | Antwort |
|---|---|
| Wurde jede Zahl nachgezählt? | **Ja, und eine war falsch** – siehe Abschnitt 7. Kriterium 2 ist aus zwei unabhängigen Quellen bestätigt |
| Läuft der Sondenlauf in beiden Kodierungsumgebungen? | **Ja, vier Läufe** (D-49), zwei davon gegen die Endfassung. 254 Ergebniszeilen, zeilengleich mit 0.54.1 |
| Ist der Gegenbeweis geführt? | **Ja, zweifach.** Prüfung 46 gegen den gemischten Stand (Abschnitt 4) und der Träger gegen den Befund des Messprotokolls (Abschnitt 5). **Der zweite ist der wichtigere** – er hat eine Einordnung umgeworfen, bevor sie ausgeliefert wurde |
| Ist der Migrationshinweis gemessen? | **Ja, vor dem Schreiben** (Abschnitt 6). Die Lehre von 0.54.1 ist eingehalten |
| Wurde etwas verschwiegen? | **Nein.** Die falsche Einordnung des Messprotokolls bleibt dort stehen und trägt einen Nachtrag (6.1a); die drei ungeprüften Befunde stehen als `K-47` bis `K-49` im Decision Log und im Änderungsverzeichnis |
| Halten die Richtwerte für Sondenläufe? | **Ja, alle vier Läufe zwischen 134,6 und 143,3 s Wanduhr.** Die Warnung der Übergabe gilt weiter: Der Störfall vom 16.09. lag bei 1351,8 s bei identischem Baum. **Ein Richtwert von hier ersetzt das Mitmessen der Wanduhr nicht** |
| Wurde eine Prüfung gebaut? | **Nein, und der Preis ist benannt** (Abschnitt 1). Drei Befunde bleiben ungeprüft und wiederholbar |

---

*Unterhalb der Trennlinie, nach D-94 nicht Teil des zeilengleichen Vergleichs:*
*Lauf A 143,3 s Wanduhr (1123,2 s Rechenzeit, 8 Bahnen, Faktor 7,8); Lauf B 134,6 s*
*(1059,1 s, Faktor 7,9); Lauf C 134,7 s (1056,8 s, Faktor 7,8); Lauf D 136,8 s*
*(1078,1 s, Faktor 7,9). **Vier Läufe zwischen 134,6 und 143,3 s** – die Richtwerte*
*von 0.54.0 halten diesmal, anders als am 16.09. (siehe die Warnung zu den Laufzeiten*
*in der Übergabe).*
