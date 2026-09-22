# Wirkungsnachweise 0.45.0 – Prüfungen 43 und 44

| Feld | Wert |
|---|---|
| Datum | 2026-09-15 |
| Gegenstand | Prüfung 43 (Hook-Block der Berechtigungsdatei, D-92) und Prüfung 44 (Register der Übungspräparationen, D-93) |
| Antrag | `CR-2026-067` |
| Grundlage | D-23: Eine Prüfung gilt erst als vorhanden, wenn sie eine bewusst gesetzte Sonde meldet |
| Ergebnis | **144 Sonden, 57 Gegenproben, 7 Selbstproben – alle bestanden, in beiden Kodierungsumgebungen zeilengleich** (Exit 0). Validator gegen `main`: 0 Fehler, 0 Warnungen |

## 1. Der Sondenlauf

Abnahmeform seit D-49: zwei Läufe, einmal ohne und einmal mit `PYTHONIOENCODING=utf-8`.

| Umgebung | Sonden | Gegenproben | Selbstproben | Exit |
|---|---|---|---|---|
| ohne `PYTHONIOENCODING` | 144 | 57 | 7 | 0 |
| mit `PYTHONIOENCODING=utf-8` | 144 | 57 | 7 | 0 |

Beide Ausgaben sind **zeilengleich** (`diff` über alle Meldezeilen: kein Unterschied). Vor
diesem Release waren es 135 Sonden und 53 Gegenproben; die Zunahme ist genau die neue:
**neun Sonden und vier Gegenproben.**

| Kennung | Was sie herstellt | Erwartete Meldung |
|---|---|---|
| Sonde 43a (je Pack) | `hooks`-Block aus der Berechtigungsdatei entfernt | „trägt keinen 'hooks'-Block" |
| Sonde 43b (je Pack) | derselbe Zustand **plus** verwaiste Hook-Datei daneben | dieselbe Meldung **und** der Dateiname darin |
| Sonde 43c (je Pack) | Block vorhanden, `PreToolUse` leer | „ohne ein einziges PreToolUse-Kommando" |
| Gegenprobe 43a (je Pack) | Auslieferungszustand | **keine** der beiden Meldungen |
| Sonde 44a | eine Vorbedingung nennt `UEB-99`, das Register führt es nicht | „das Register in …" |
| Sonde 44b | das Register führt `UEB-98`, kein Testfall nennt es | „die kein Testfall nennt" |
| Sonde 44c | die Registerüberschrift ist umbenannt | „führt kein Register mehr" |
| Gegenprobe 44a | Auslieferungszustand | keine Meldung der Prüfung 44 |
| Gegenprobe 44b | eine **achte** Präparation, registriert **und** von einem Testfall gebraucht | keine Meldung der Prüfung 44 |

**Gegenprobe 44b ist die wichtigere Hälfte.** Eine Prüfung, die jede neue Kennung meldet,
bestünde jede Sonde. Sie belegt, dass der **zulässige** Weg – eine Präparation ergänzen und
sie registrieren – nicht teurer ist als der unzulässige.

## 2. Was der erste Lauf gefunden hat, und es war die Sonde

Der erste Durchgang meldete **zwei Abweichungen, in beiden Umgebungen dieselben** – beide
in den neuen Sonden, keine in den Prüfungen:

| Abweichung | Ursache | Behebung |
|---|---|---|
| Sonde 43b fiel bei `claude-code` | Die Sonde legte eine Datei `hooks.json` an. Die kennt der Validator nicht: `VERWAISTE_HOOK_DATEIEN` führt **genau einen** Namen, `hooks.v1.json`, und den für beide Packs. **Geraten statt nachgesehen** | Beide Packs nutzen denselben Namen; die Herkunft steht als Kommentar an der Stelle |
| Gegenprobe 44a brach mit `TypeError` ab | Der generischen `gegenprobe()` wurde ein Tupel übergeben; sie nimmt genau einen Suchtext | Statt drei Meldungen aufzuzählen, sucht die Gegenprobe jetzt `"(D-93)"` – der Decision Record steht in **jeder** Meldung der Prüfung 44 und fängt damit auch künftige |

**Die zweite Behebung ist besser als der erste Entwurf**, und zwar aus einem Grund, der
über diesen Fall hinausgeht: Eine Gegenprobe, die eine Liste bekannter Meldungen
ausschließt, übersieht jede Meldung, die später dazukommt. Ein gemeinsamer Anker im Text
jeder Meldung schließt sie alle ein.

**Ein Nebenbefund, der nicht zu diesem Release gehört:** Prüfung 18 sucht bei **beiden**
Packs nach `hooks.v1.json` – einem Namen aus der `devin-desktop`-Welt. Ob `claude-code` je
eine eigene Hook-Datei angelegt hat und wie sie dort hieße, ist nicht erhoben. Die Prüfung
ist damit für dieses Pack möglicherweise wirkungslos, ohne dass es auffällt. Als Kandidat
geführt, nicht hier behoben.

## 3. Gegenbeweis gegen den Vorstand

### Prüfung 43 – an einem echten Projekt, nicht an einer Konstruktion

Zuschnitt: der **alte Stand des Übungsrepositoriums** (`a2dab6b`, Framework 0.13.0, via
`git archive`), sein `leitwerk-core/` durch das aus 0.45.0 ersetzt, **kein** `--update` –
damit die Projektdateien den Auslieferungszustand behalten.

```
FEHLER  .devin/config.json: trägt keinen 'hooks'-Block. […] Daneben liegt
        .devin/hooks.v1.json: Dort steht eine Regelmenge, die aussieht, als gälte sie —
        der Client liest diese Datei nicht (D-32). […] (D-92)
```

**Die Prüfung findet den Befund, der sie ausgelöst hat**, und ihre Meldung nennt beide
Hälften der Migration. Die Fehlerzahl ist dabei nachgezählt und nicht nur vorhanden:

| Fehler | Herkunft |
|---|---|
| 14 | dieselben, die der 0.44.0-Validator meldete (8× Prüfung 42 unerklärt, 3× verlorener Anker, 1× Prüfung 37, 1× Steckbriefversion, 1× Importsteuerung) |
| **+1** | **Prüfung 43** – der Gegenstand dieses Nachweises |
| +1 | `AGENTS.md:3` – eine Prüfung, die zwischen 0.13.0 und heute dazugekommen ist. **Gehört zum Zuschnitt, nicht zum Befund:** Ohne `--update` ist die Wurzel-Anweisungsdatei noch die von 0.13.0 |
| **16** | **gemessen** |

### Prüfung 44 – der Gegenbeweis ist konstruktionsbedingt stumm, und das gehört gesagt

Zuschnitt: der Vorstand `22b8949` (0.44.0) via `git archive`, geprüft mit dem Validator aus
0.45.0 über `--root`.

```
FEHLER  leitwerk-core/onboarding/exercises/README.md: führt kein Register mehr
        (gesucht: '### Register der Präparationen'). […] (D-93)
```

**Das ist ein Treffer, aber nicht der Gegenstand.** Die Prüfung meldet dort den verlorenen
Anker, weil das Register mit **diesem** Release entsteht; über Präparationen sagt der
Vorstand nichts, weil er keine kennt. Der Wirkungsnachweis für Prüfung 44 ruht deshalb
allein auf ihren drei Sonden und zwei Gegenproben – **nicht** auf einem Fund im Vorstand.
Das ist dieselbe Lage wie am 2026-09-13 bei Prüfung 33 und sie wird hier genauso
ausgewiesen, statt eine Zahl zu nennen, die mehr verspricht.

Die 46 Fehler, die derselbe Lauf insgesamt meldet, sind **kein Messwert über den Vorstand**:
Ein neuer Validator gegen einen alten Baum fällt in die Ankertests der Prüfungen, deren
Gegenstand dort noch fehlt. Das ist bekannt (Protokoll zu 0.33.0) und hier nur erwähnt,
damit die Zahl niemanden in die Irre führt.

## 4. Wo die Prüfungen im eigenen Repositorium stehen

| Prüfung | Läuft im Repo-Lauf? | Findet sie dort etwas? |
|---|---|---|
| 43 | **ja** – die lokale Testinstallation ist `devin-desktop` und führt ihre Hooks in der Berechtigungsdatei | **nein**, sie trägt ihren Block. Das ist der erwartete Zustand und kein Beleg für Wirkung |
| 44 | **ja** – beide Register liegen im Repositorium | **nein**, sieben registrierte und sieben gebrauchte Kennungen decken sich |

**Prüfung 43 entgeht damit nicht dem Befund B02** (eine Prüfung, die im eigenen
Repositorium gar nicht ausgeführt wird): Sie läuft. Sie meldet nur nichts, weil hier nichts
zu melden ist.

## 5. Was dieser Nachweis nicht leistet

- **Er belegt, dass die Prüfungen wirken, nicht dass ihre Gegenstände richtig sind.** Ob der
  Hook-Block, den eine Installation trägt, den richtigen Hook aufruft, prüfen 15, 16 und 17
  – nicht 43.
- **Prüfung 44 gleicht zwei Register ab, nicht ein Register gegen die Wirklichkeit.** Ob
  `UEB-02` im Übungsrepository wirklich unter dem genannten Pfad liegt, sieht kein Validator
  dieses Repositoriums.
- **Kein Lauf gegen einen Client.** Dass ein wiederhergestellter Hook in einer Sitzung
  tatsächlich auslöst, ist hier nicht gemessen – nur, dass die Konfiguration dasteht.
