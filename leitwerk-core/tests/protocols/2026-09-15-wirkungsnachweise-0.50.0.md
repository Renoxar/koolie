# Wirkungsnachweise 0.50.0 – der Mechanismus und der Wächter haben beide gegriffen

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-15 |
| Framework-Version | `0.49.0` → **`0.50.0`** |
| Gegenstand | `CR-2026-072` – dreizehn Skills auf `pilot`, vier Vorlagen ohne Statuswert, Übergangsbedingungen für Nicht-Skill-Träger (D-102 bis D-104) |
| Gegenprüfung | `tests/protocols/2026-09-15-gegenpruefung-modulstatus.md` |
| Prüfmethode | Zwischen den Patches gemessen: erst der Statuswechsel, dann die Standzeile – so ist sichtbar, ob Prüfung 46 den nicht nachgezogenen Fortschritt meldet. Dazu vollständige Abnahme nach D-49 (Validator; Sondenlauf in beiden Kodierungsumgebungen, nebenläufig und seriell) |
| Ergebnis | **Zwei Wächter haben gegriffen, und einer davon gegen diesen Antrag selbst.** Prüfung 46 meldete den nicht nachgezogenen Fortschritt mit genau einem Fehler; der Kennungswächter `frei()` meldete, dass `K-36` – die in diesem Release **wirklich** vergebene Kennung – als synthetische Kennung einer Gegenprobe belegt war |

## 1. Prüfung 46 hat zum zweiten Mal gegriffen, und wieder bei einem Fortschritt

Gemessen wurde **zwischen** zwei Patches: Nach dem Statuswechsel der dreizehn Skills und der
Umstellung der vier Vorlagen, aber **vor** dem Nachziehen der Standzeile in
`docs/ROADMAP.md`. Der Validatorlauf meldete genau einen Fehler, unverändert
wiedergegeben:

```text
FEHLER   leitwerk-core/docs/ROADMAP.md: Kriterium 3 von D-11 (Modulstatus über `entwurf`)
ist gezählt **52**, die Standzeile nennt 69 – der Fortschritt ist nicht nachgezogen. Der
1.0.0-Stand gehört ausgerechnet und nicht gepflegt; am 2026-09-15 lagen alle vier Zahlen
daneben, ohne dass eine je falsch geschrieben worden wäre (CR-2026-070, D-98)

Ergebnis: 1 Fehler, 0 Warnungen
```

**Ohne diese Bauform stünde in der Roadmap heute noch 69.** Das ist der Preis, den
`CR-2026-070` E1 ausdrücklich gewollt hat – die Abweichung gilt **in beide Richtungen** –,
und er ist bei der zweiten Gelegenheit, die es je gab, ein zweites Mal fällig geworden. Bei
0.49.0 war es Kriterium 4, hier Kriterium 3.

Der Stand der Statuswerte nach dem Patch, mit der Zählregel der Prüfung 46 selbst
ausgezählt (unveränderte Ausgabe):

```text
Traeger mit Statuszeile: 69
   51  entwurf
   13  pilot
    3  <TBD: Status; ein neues Pack beginnt auf entwurf>
    1  entwurf (Referenzpack der Erstfassung)
    1  <TBD: Status; ein neuer Skill beginnt auf entwurf>

Nach Gattung:
  Skill         13
  Vorlage        4
  Nicht-Skill   52
```

**Die 52, die Prüfung 46 danach zählt, sind genau die 52 Nicht-Skill-Träger** – der eine mit
dem Zusatz `entwurf (Referenzpack der Erstfassung)` ist dabei, weil der Vergleich am ersten
Wort läuft (E6 von `CR-2026-070`).

## 2. Der Kennungswächter hat gegen diesen Antrag selbst gegriffen

**Der erste Sondenlauf dieses Releases war rot, und der Befund lag nicht im Repositorium,
sondern in diesem Antrag.** Unverändert wiedergegeben:

```text
GEGENPROBE 46b  FEHL  Ein Klaerungspunkt mit demselben Statuswort bleibt ungezaehlt - die
                      alte Regel zaehlte fuenf davon mit  [Praeparation gebrochen]
        DECISION_LOG.md: Die synthetische Kennung 'K-36' ist dort bereits vergeben. Eine
        Gegenprobe, die eine echte Kennung doppelt, misst nicht mehr ihren Fall - eine neue
        synthetische Kennung waehlen

Ergebnis: 1 Abweichung(en)
```

**Die Gegenprobe 46b legt einen synthetischen Klärungspunkt an**, um zu belegen, dass
Prüfung 46 ihn *nicht* als Decision Record zählt. Ihre synthetische Kennung war `K-36` –
und `K-36` ist mit diesem Release **wirklich vergeben** (Statuszeile der elf Kernmodule).

**Das ist die zweite Kollision dieser Art in diesem Projekt und die erste, die gemeldet
wurde statt zu täuschen.** Am 2026-09-13 trug die Gegenprobe 30 als synthetische Kennung
ausgerechnet `G-18` – dieselbe, die 0.36.0 wirklich vergab; die Falle stand damals in der
Übergabe benannt und schnappte trotzdem zu. Genau daraufhin ist `frei()` entstanden
(`CR-2026-060` E3), mit dem Satz: *„eine benannte Falle, in die man zweimal tritt, gehört in
den Code."*

**Was ohne den Wächter passiert wäre**, und es ist der schlechtere von zwei Zuständen:

| Ohne `frei()` | Was der Lauf gezeigt hätte |
|---|---|
| Die Gegenprobe legt `K-36` **ein zweites Mal** an | Das Decision Log trägt zwei Zeilen `\| K-36 \|` |
| Prüfung 46 zählt Klärungspunkte nicht | Die Gegenprobe wäre **grün** geblieben |
| Gemessen worden wäre | **nichts** – der Fall „ein Klärungspunkt mit demselben Statuswort" wäre hergestellt worden, aber nicht unterscheidbar von dem echten daneben |

> **Eine Gegenprobe, die eine echte Kennung doppelt, besteht – und belegt nichts.** Sie ist
> die stille Verwandte der Sonde, die danebentrifft (0.49.0, Sonde 46f): Dort verändert eine
> Sonde etwas, ohne ihren Gegenstand zu treffen; hier stellt eine Gegenprobe einen Zustand
> her, der schon da ist.

**Behoben:** Die Gegenprobe trägt jetzt `K-99`, als benannte Konstante `P46_KLAERUNG` und mit
dem Grund im Kommentar. Die 99 folgt der Konvention von `G-99` und `UEB-99` – hoch genug,
dass keine echte Vergabe sie erreicht.

## 3. Die Abnahmeläufe

| Lauf | Umgebung | Ergebnis |
|---|---|---|
| Validator gegen den Arbeitsbaum, **vor** dem Nachziehen der Standzeile | – | **1 Fehler**, und es ist der erwartete (Abschnitt 1) |
| Validator gegen den Arbeitsbaum, nach dem Nachziehen | – | **0 Fehler, 0 Warnungen** |
| Sondenlauf 1 (nebenläufig, 8 Bahnen) | ohne `PYTHONIOENCODING` | **1 Abweichung** – die Kollision aus Abschnitt 2 |
| Sondenlauf 2 (nebenläufig, 8 Bahnen) | ohne `PYTHONIOENCODING` | **alle Sonden und Gegenproben bestanden** |
| Sondenlauf 3 (nebenläufig, 8 Bahnen) | `PYTHONIOENCODING=utf-8` | **alle bestanden**, über 251 Zeilen **zeilengleich** mit Lauf 2 |
| Sondenlauf 4 (**seriell**, `--bahnen 1`) | ohne `PYTHONIOENCODING` | **alle bestanden**, über 251 Zeilen **zeilengleich** mit Lauf 2. 868,8 s Wanduhr gegen 135,2 s auf acht Bahnen |
| Sondenlauf 5 (nebenläufig, 8 Bahnen) | gegen den **fertigen** Baum, also einschließlich dieses Protokolls | **alle bestanden**, über 251 Zeilen **zeilengleich** mit Lauf 2 |
| `install.py --root . --update` | lokale Testinstallation (`devin-desktop`) | 0 angelegt, **12 aktualisiert**, 46 unverändert, 20 Projektdateien behalten |

**228 Ergebniszeilen bestanden** – 154 Sonden, 62 Gegenproben, 12 Selbstproben, dazu 18
Bündelkopfzeilen, zusammen die 246 Zeilen der Abnahme nach D-49. Die Laufzeiten stehen
unterhalb der Trennlinie und sind nach D-94 nicht Teil des zeilengleichen Vergleichs.

**Warum es einen fünften Lauf gibt.** Die Läufe 2 bis 4 sind gegen den Baum **ohne** dieses
Protokoll gefahren – so verlangt es die Reihenfolge, weil das Protokoll die Läufe
beschreibt. `probe-pruefungen.py` kopiert aber **das ganze Verzeichnis** je Sonde: Eine Datei,
die den Validator stört, lässt **alle Gegenproben** scheitern, während die Sonden grün
bleiben. Lauf 5 schließt genau diese Lücke und ist zeilengleich mit Lauf 2 – **die neue Datei
verändert keinen einzigen Messwert.**

**Die zwölf aktualisierten Dateien der Installation sind die zwölf Framework-Skills** – der
dreizehnte (`role-re-ticket`) gehört zu einem Role Pack, das in dieser Testinstallation nicht
aktiviert ist. Nachgesehen: `.devin/skills/fw-plan/SKILL.md` trägt danach
`| Status | \`pilot\` |`.

## 4. Kein Gegenbeweis gegen den Vorstand – und warum das hier richtig ist

Der Gegenbeweis belegt üblicherweise, dass eine **neue Prüfung** gegen den Vorstand
tatsächlich fällt. **Dieses Release baut keine Prüfung** (E5), also hat er keinen
Gegenstand.

Was stattdessen gegen den Vorstand belegt ist, ist die **Zahl**: Prüfung 46 ist mit 0.48.0
entstanden und hat gegen `0.49.0` in jedem Lauf `Kriterium 3 = 69` gerechnet – dieselbe
Prüfung, dieselbe Zählregel, nur ein anderer Bestand. **Der Beleg für die Wirkung ist der
Fehler aus Abschnitt 1**, und er ist an einem Zwischenstand gemessen, nicht an einer
Erwartung.

## 5. Was nicht gemessen ist

- **Ob ein KI-Client den dreizehn Skills folgt.** Das sind die 87 offenen Ergebniszellen von
  Kriterium 2, und sie sind unverändert offen. Ein Träger auf `pilot` ist strukturell
  abgenommen, nicht erprobt – so steht es seit diesem Release in `01-governance.md`
  Abschnitt 5 Punkt 4.
- **Ob ein Client Pack den Statuswert irgendwohin abbildet.** Er steht im Dateikörper
  (D-08), nicht im Frontmatter; keine Abbildung, kein Manifestfeld, also auch kein Beleg
  nötig. Gemessen ist nur, dass die installierte Fassung ihn unverändert trägt.
- **Ob eine aus einer Vorlage erzeugte Kopie den Ausfüllschlitz füllt.** Bei einem Skill
  fängt `SKILL_STATUS` des Validators einen unbekannten Wert; bei Client-, Role- und
  Technology-Pack fängt ihn heute nichts (E5, fällig mit dem ersten gehobenen
  Nicht-Skill-Träger).
- **Die elf Kernmodule.** Sie führen keine Statuszeile; `K-36` ist offen, und Kriterium 3 ist
  bis zu seiner Entscheidung um elf Träger zu klein.

## 6. Eine Zahl im eigenen Text war wieder zu klein

Der letzte Durchgang vor dem Commit – derselbe, der sich seit 0.42.0 jedes Mal trägt – hat
eine eigene Zahl gefunden: Der Abstand des Hauptdokuments stand als **„einundvierzig
Releases"** in vier Trägern (Gegenprüfung, Antrag, Roadmap, Änderungsverzeichnis).
**Abgezählt aus dem Änderungsverzeichnis sind es zweiundvierzig** – 52 Releases insgesamt,
davon 42 nach `0.9.0`. Berichtigt vor dem Commit.

> **Wie schon mehrfach am 13. und 14.09. und einmal in der Gegenprüfung dieses Vorgangs:
> Die eigene Zahl war zu klein.** Sie stand in vier Dateien, bevor sie nachgezählt
> wurde. Der Durchgang lohnt sich, und er gehört vor den teuren Lauf – hier hat er nach ihm
> stattgefunden, weil er eine Zahl in Prosa betrifft und keine, die eine Sonde liest.

## 7. Bewertung

**Beide Wächter dieses Releases haben gegriffen, und beide gegen den, der sie benutzt.**
Prüfung 46 hat den nicht nachgezogenen Fortschritt gemeldet; `frei()` hat eine
Kennungskollision gemeldet, die dieser Antrag selbst erzeugt hat. **Keiner von beiden hat
etwas über das Repositorium gesagt – beide haben etwas über den Vorgang gesagt.**

| Kriterium von D-11 | vor 0.50.0 | nach 0.50.0 |
|---|---|---|
| 1 – `VERIFY`-Marker | 29 | **29** |
| 2 – offene Ergebniszellen | 118 | **118** |
| 3 – Modulstatus auf `entwurf` | 69 | **52** |
| 4 – Records auf `entschieden (Vorschlag)` | 0 | **0** |
| **Summe** | **216** | **199** |

**Zum ersten Mal steht die Summe unter 200**, und es ist das zweite Release in Folge, in dem
sich eine der vier Zahlen bewegt – nach dreiundzwanzig, in denen keine es tat.
