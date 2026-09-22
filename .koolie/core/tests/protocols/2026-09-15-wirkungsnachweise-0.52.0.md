# Wirkungsnachweise Release 0.52.0

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-15 |
| Framework-Version | `0.51.0` → `0.52.0` |
| Gegenstand | `CR-2026-074` – vierzig Statuswechsel von `entwurf` auf `pilot`, drei Auslegungen als Decision Records (D-109 bis D-111), ein neuer Klärungspunkt (`K-39`) |
| Prüfmethode | Abnahme nach D-49: Sondenlauf **in beiden Kodierungsumgebungen** und zeilengleich zwischen seriellem und nebenläufigem Lauf; dazu eine gezielte Gegenprobe gegen Prüfung 46 auf einer Kopie des fertigen Baums mit der Standzeile des Vorstands |
| Ausgeführte Befehle | `python leitwerk-core/tests/scripts/validate-framework.py --root .` (nach jedem Patch); `python -u leitwerk-core/tests/scripts/probe-pruefungen.py .` (ohne und mit `PYTHONIOENCODING=utf-8`, dazu `--bahnen 1`) |
| Ergebnis | **Alle 254 Ergebniszeilen bestanden – in beiden Kodierungsumgebungen, seriell wie nebenläufig und gegen den fertigen Baum, durchgehend zeilengleich über 259 Zeilen.** Prüfung 46 hat genau einmal gemeldet, gegen diesen Vorgang selbst. **Prüfung 47 hat geschwiegen** – das Vokabular hielt bei allen vierzig Wechseln |

## 1. Warum dieses Release keine neue Prüfung baut

Die Anweisung des Menschen vom 2026-09-15 gilt unverändert: **keine neue Prüfung, solange
eine Zahl zu senken ist.** Dieses Release senkt Kriterium 3 von 41 auf 1.

**Und es gäbe auch nichts zu bauen.** Der Gegenstand dieses Vorgangs ist die Unterscheidung
zwischen einem Ausfüllschlitz und einer Nennung derselben Marke – und die ist nach D-102
ausdrücklich **nicht** maschinell. Eine Prüfung darauf wäre eine Prüfung, die mehr
verspricht, als sie leistet: der wiederkehrende Befundtyp dieses Projekts.

**Der Wächter für diesen Vorgang ist gebaut und steht seit 0.48.0:** Prüfung 46 rechnet
Kriterium 3 bei jedem Lauf aus und hält es gegen die Standzeile, **in beide Richtungen**.
Sie hat gegriffen (Abschnitt 2).

## 2. Prüfung 46 hat gegriffen – zum fünften Mal, und zum fünften Mal bei einem Fortschritt

Gefahren als **gezielte Gegenprobe** auf einer vollständigen Kopie des fertigen Baums, in
der allein die Standzeile auf den Vorstand `41` zurückgesetzt ist. Der Lauf ist damit
derselbe wie der Zwischenstand, den ein Vorgang ohne nachgezogene Standzeile hinterließe:

```
FEHLER   leitwerk-core/docs/ROADMAP.md: Kriterium 3 von D-11 (Modulstatus über `entwurf`)
ist gezählt **1**, die Standzeile nennt 41 – der Fortschritt ist nicht nachgezogen. Der
1.0.0-Stand gehört ausgerechnet und nicht gepflegt; am 2026-09-15 lagen alle vier Zahlen
daneben, ohne dass eine je falsch geschrieben worden wäre (CR-2026-070, D-98)

Ergebnis: 1 Fehler, 1 Warnungen
```

**Genau ein Fehler**, und er benennt diesen Vorgang. Die Warnung ist ein Artefakt der
Kopie: Gegenstand 2 der Prüfung 45 braucht ein Git-Repositorium, und die Kopie ist keines.

| Release | Meldung | Anlass |
|---|---|---|
| 0.49.0 | `Kriterium 4 … gezählt 0, die Standzeile nennt 9` | Fortschritt |
| 0.50.0 | `Kriterium 3 … gezählt 52, die Standzeile nennt 69` | Fortschritt |
| 0.51.0 | `gezählt 64, die Standzeile nennt 52` | **Gegenstand vollständiger** (`K-38`) |
| 0.51.0 | `gezählt 41, die Standzeile nennt 52` | Fortschritt |
| **0.52.0** | `gezählt 1, die Standzeile nennt 41` | Fortschritt |

**Ohne diese Bauform stünde in der Roadmap heute noch 41.** Fünf Gelegenheiten, fünf
Treffer, und keine einzige davon ein Rückfall – der Preis, den `CR-2026-070` E1
ausdrücklich gewollt hat, ist ausschließlich bei Fortschritten fällig geworden.

## 3. Prüfung 47 hat geschwiegen – und das ist hier der Messwert

Prüfung 47 ist mit 0.51.0 gebaut worden und hält vier Gegenstände: den verlorenen Anker,
die Vollständigkeit der Statuszeile, das **Vokabular** und den Ausfüllschlitz, der einer
Vorlage gehört – in beide Richtungen.

**Dieses Release hat vierzig Statuswerte angefasst.** Wäre auch nur einer außerhalb des
Vokabulars gelandet – ein Tippfehler, ein `Pilot` statt `pilot`, ein verlorener Zusatz –,
hätte sie es gemeldet. Sie hat nichts gemeldet.

**Der Zusatz des Referenzpacks ist der interessante Fall:**
`framework/role-packs/software-development/ROLE_PACK.md` trägt
`pilot (Referenzpack der Erstfassung)`. **Gegenprobe 47b belegt genau das** – *„Ein
Verlaufszusatz in Klammern bleibt zulässig – verglichen wird das erste Wort des Werts"* –
und sie ist in allen Läufen dieses Releases grün. Dieselbe Leseregel benutzt Prüfung 46 für
ihre Zählung (E6 von `CR-2026-070`).

## 4. Der Sondenlauf – Abnahme nach D-49

D-49 verlangt den Lauf in **beiden** Kodierungsumgebungen und zeilengleich. Gefahren sind
vier Läufe:

| Lauf | Umgebung | Bahnen | Baum | Ergebnis |
|---|---|---|---|---|
| A | ohne `PYTHONIOENCODING` | 8 | ohne dieses Protokoll | alle Sonden und Gegenproben bestanden |
| B | `PYTHONIOENCODING=utf-8` | 8 | ohne dieses Protokoll | alle Sonden und Gegenproben bestanden |
| C | ohne `PYTHONIOENCODING` | **1** (seriell) | ohne dieses Protokoll | alle Sonden und Gegenproben bestanden |
| D | ohne `PYTHONIOENCODING` | 8 | **fertig, mit diesem Protokoll** | alle Sonden und Gegenproben bestanden |

**Zeilengleich verglichen sind A gegen B** (beide Kodierungsumgebungen), **A gegen C**
(nebenläufig gegen seriell) und **A gegen D** (gegen den fertigen Baum): in allen drei Vergleichen **kein Unterschied**. Der Lauf ist damit unabhängig von der Konsolenkodierung, von der Bahnenzahl und davon, ob die Protokolle dieses Releases im Baum liegen

**Die 254 Ergebniszeilen der Abnahme** setzen sich zusammen aus **159 Sonden**,
**65 Gegenproben**, **12 Selbstproben** und **18 Bündelkopfzeilen**; mit der
Zusammenfassungszeile und den Trennzeilen sind es 259 verglichene Zeilen. **Gegenüber
0.51.0 ist keine Zahl verändert** – dieses Release baut keine Prüfung und keine Sonde.

### Laufzeiten (unterhalb der Trennlinie, nicht Teil des zeilengleichen Vergleichs, D-94)

| Lauf | Wanduhr | Rechenzeit | Faktor |
|---|---|---|---|
| A | 147,8 s | 1165,9 s | 7,9 |
| B | 138,9 s | 1096,2 s | 7,9 |
| C | 1004,9 s | 1004,8 s | – |
| D | 140,3 s | 1105,2 s | 7,9 |

> ⚠️ **Die drei Werte des Laufs D sind nach dem Lauf eingetragen worden** – sie stehen
> erst danach fest. **Das ist zulässig, weil die Laufzeiten unterhalb der Trennlinie
> stehen und nach D-94 ausdrücklich nicht Teil des zeilengleichen Vergleichs sind:** Der
> Eintrag ändert nichts, was eine Prüfung liest. Ohne diese Abgrenzung entstünde ein
> Rückschritt ohne Ende – **jeder Lauf gegen die Endfassung ändert die Endfassung.**

## 5. Der Aufräumer

Der Aufräumer aus 0.46.0 hat in **allen** Läufen dieser Sitzung geschwiegen: Kein
verwaistes Arbeitsverzeichnis ist gemeldet worden.

## 6. Der Validatorlauf

| Zeitpunkt | Ergebnis |
|---|---|
| nach Patch 1 (vierzig Statuswechsel) und Patch 2 (Standzeile, Roadmap, `prompts/README.md`, `VERSION`) | 1 Fehler – die Pfadangabe auf das noch nicht angelegte Abnahmeprotokoll |
| nach Anlegen des Abnahmeprotokolls | **0 Fehler, 0 Warnungen** |
| nach Patch 4 (Decision Log) | **0 Fehler, 0 Warnungen** |
| nach Patch 5 (Änderungsverzeichnis) | **0 Fehler, 0 Warnungen** |
| gegen den fertigen Baum | **0 Fehler, 0 Warnungen** |

> ⚠️ **Der erste Fehler war ein Wächter und kein Versehen.** `prompts/README.md` verweist
> seit Patch 2 auf das Abnahmeprotokoll; der Validator prüft jede Pfadangabe auf Existenz
> und meldete sie, bevor die Datei geschrieben war. **Eine Zusage auf ein Dokument, das es
> nicht gibt, fällt in diesem Repositorium sofort auf** – das ist Prüfung 3, und sie hat
> hier ihren Zweck erfüllt.

## 7. D-106 ist am Diff belegbar, nicht nur behauptet

**Ein Statuswechsel ist keine Versionsänderung** (D-106, `01-governance.md` Abschnitt 5
Punkt 5). Das ist in diesem Release nicht zugesichert, sondern **nachgezählt**:

```
git diff --numstat -- <die vierzig Träger>
```

meldet für **jeden** der vierzig Träger genau `1  1` – eine geänderte Zeile, und das ist
die Statuszelle. Ein `grep` über denselben Diff nach geänderten Zeilen der Form
`| Version |`, `| Stand |` oder `| Datum |` liefert **null Treffer**.

**Keine Version ist erhöht, kein Änderungsverlauf eines Trägers hat einen Eintrag
bekommen.** Das ist zugleich der Nachweis, dass der Prüfpunkt von `FW-CL-11`
(*„Version je geänderter Checkliste und je geändertem Prompt gepflegt"*) hier nicht greift –
seit 0.51.0 steht die Ausnahme wörtlich in seinem Text.

## 8. Was in diesem Release nicht gemessen ist

- **Kein Sitzungstest.** Die vierzig Träger sind strukturell abgenommen, nicht erprobt
  (`01-governance.md` Abschnitt 5 Punkt 4). **Kriterium 2 steht unverändert auf 118.**
- **Kein `VERIFY`-Marker bearbeitet.** Kriterium 1 steht unverändert auf 29. Die zehn
  Markerfundstellen der Client-Pack-Gattung sind je Träger **benannt**, nicht abgearbeitet –
  Punkt 3 (c) verlangt das Benennen, nicht das Schließen.
- **Der Wirkungsnachweis für die Auslegung selbst ist ein Protokoll, kein Skript.** Ob die
  Trennung zwischen Schlitz und Nennung je Träger richtig getroffen ist, belegt das
  Abnahmeprotokoll mit Fundstelle und Zeilennummer. **Eine Prüfung kann das nicht
  nachrechnen**, und dieses Release behauptet es nicht.

## 9. Bewertung

| Frage | Antwort |
|---|---|
| Sind alle 254 Ergebniszeilen bestanden? | **Ja**, in vier Läufen |
| Zeilengleich in beiden Kodierungsumgebungen? | **Ja**, über 259 Zeilen |
| Zeilengleich seriell gegen nebenläufig? | **Ja**, über 259 Zeilen. Der serielle Lauf braucht 1004,9 s gegen 147,8 s auf acht Bahnen – Faktor 6,8 |
| Hat ein Wächter gegen den Vorgang gegriffen? | **Ja, Prüfung 46** – `gezählt 1, die Standzeile nennt 41`. Fünfte Gelegenheit, fünfter Treffer, fünfter Fortschritt |
| Hat eine Prüfung zu Unrecht geschwiegen? | **Nein, soweit prüfbar.** Prüfung 47 hat vierzig angefasste Statuswerte durchgelassen, und Gegenprobe 47b belegt, dass sie den Zusatz des Referenzpacks zu Recht durchlässt |
| Ist eine neue Prüfung gebaut? | **Nein** – und der Grund steht in Abschnitt 1, nicht nur die Tatsache |
