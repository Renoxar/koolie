# Wirkungsnachweise 0.47.0 – Prüfung 45 und der erste Fall des Aufräumers

| Feld | Wert |
|---|---|
| Datum | 2026-09-15 |
| Gegenstand | Prüfung 45 (Bytecode des Kerns, D-97) und die Behebung am Aufräumer aus 0.46.0 |
| Antrag | `CR-2026-069` |
| Grundlage | D-23: Eine Prüfung gilt erst als vorhanden, wenn sie eine bewusst gesetzte Sonde meldet. Dazu der Gegenbeweis gegen den Vorstand |
| Ergebnis | **148 Sonden, 59 Gegenproben, 11 Selbstproben – alle bestanden, in beiden Kodierungsumgebungen zeilengleich** (Exit 0). Validator: 0 Fehler, 0 Warnungen. **Gegenbeweis gegen 0.46.0: vier Fundstellen, und beide Gegenproben bestehen dort** |

## 1. Der Befund, abgezählt

| Projekt | Framework-Stand | Versionierte `.pyc` unter `leitwerk-core/` | `.gitignore` deckt `__pycache__` |
|---|---|---|---|
| `devpacks/otp-generator` (Pilot) | 0.41.0 | **6** | nein |
| `devpacks/test-devin-framework` (Übungsrepo) | 0.45.0 | **2** | nein |
| `devpacks/leitwerk` (Framework selbst) | 0.46.0 | 0 | **ja** |

**Zwei von zwei Projekten.** Der Weg zum Befund steht in
`2026-09-15-migrationslauf-pilot-0.46.0.md`, Abschnitt 5.

## 2. Der Sondenlauf

Abnahmeform seit D-49: zwei Läufe, einmal ohne und einmal mit `PYTHONIOENCODING=utf-8`.
Seit 0.46.0 zusätzlich der Vergleich zwischen seriellem und nebenläufigem Lauf.

| Lauf | Zeilen | Sonden | Gegenproben | Selbstproben | Exit | Wanduhr |
|---|---|---|---|---|---|---|
| `--bahnen 8`, ohne `PYTHONIOENCODING` | 235 | 148 | 59 | 11 | 0 | **118,2 s** |
| `--bahnen 8`, mit `PYTHONIOENCODING=utf-8` | 235 | 148 | 59 | 11 | 0 | **120,6 s** |
| `--bahnen 1`, ohne `PYTHONIOENCODING` | 235 | 148 | 59 | 11 | 0 | **911,0 s** |

**Beide Ausgaben sind zeilengleich** – `diff` über die 235 Ergebniszeilen oberhalb der Trennlinie: kein Unterschied. Und der serielle Lauf ist **zeilengleich zum nebenläufigen** – die Zusage von 0.46.0 trägt auch die neuen Einheiten, einschließlich derer, die sich ein Repositorium anlegen.

Vor diesem Release waren es 144 Sonden, 57 Gegenproben und 10 Selbstproben; die Zunahme
ist genau die neue: **vier Sonden, zwei Gegenproben, eine Selbstprobe.**

| Kennung | Was sie herstellt | Erwartete Meldung |
|---|---|---|
| Sonde 45a | Die Deckungszeile fällt aus der `.gitignore` | „deckt den Bytecode des Kerns nicht ab" |
| Sonde 45b | Die `.gitignore` fehlt ganz | „.gitignore: nicht vorhanden" (**Warnung**, kein Fehler) |
| Sonde 45c | Ein echtes Repositorium, eine `.pyc` unter `leitwerk-core/` verfolgt – **bei vorhandener Regel** | „sind versioniert", und der Pfad der Datei steht darin |
| Sonde 45d | Dieselbe Installation **ohne** `git init` | „ist nicht gelaufen" |
| Gegenprobe 45a | `*.pyc` statt `__pycache__/` – andere Schreibweise, gleiche Wirkung | **keine** Meldung der Prüfung 45 |
| Gegenprobe 45b | Ein Repositorium ohne verfolgten Bytecode | weder „sind versioniert" **noch** „ist nicht gelaufen" |
| Selbstprobe A3 | Ein Arbeitsverzeichnis mit einer schreibgeschützten Datei | **keine** Zeile – der Aufräumer räumt weg und schweigt |

### 2.1 Die beiden Gegenproben sind hier die schärferen

**Gegenprobe 45a** misst die Breite: Ein Projekt, das `*.pyc` schreibt, ist **richtig**.
Eine Prüfung, die nur `__pycache__/` gelten ließe, meldete den richtigen Text – und das
ist genau der Fehler, den Prüfung 37 einmal gemacht hat.

**Gegenprobe 45b** misst zwei Dinge auf einmal, und das zweite ist das wichtigere: Sie
verlangt, dass „sind versioniert" **fehlt** – und dass „ist nicht gelaufen" **ebenfalls
fehlt**. Ohne die zweite Bedingung bestünde sie auch dann, wenn git gar nicht da wäre;
sie bewiese dann nichts über Gegenstand 2, sondern nur, dass er schwieg. **Eine
Gegenprobe, die eine abgeschaltete Prüfung nicht von einer schweigenden unterscheidet,
misst ihren Fall nicht mehr.**

### 2.2 Warum die Sonden zu Gegenstand 2 im Bündel stehen

`kopie()` lässt `.git` bewusst weg – eine Kopie des Repositoriums ist keins. Gegenstand 2
ist deshalb auf einer Kopie **nicht herstellbar**; seine Sonden legen sich ihr
Repositorium selbst an (`installation()`, dann `git init`). Das ist dieselbe Begründung,
aus der die Sonden zu den Prüfungen 33, 37, 42 und 43 im Bündel stehen: Der Gegenstand
ist eine installierte Lage, nicht ein Text.

**Sonde 45d steht vor dem `git init`** – und zwar bewusst: Genau dieser Zustand, ein Baum
ohne `.git`, ist der Normalfall **jeder anderen Sonde dieses Skripts**. Sie belegt damit
zugleich, dass die Warnung, die alle übrigen Sondenläufe jetzt tragen, die richtige ist.

## 3. Der Gegenbeweis gegen den Vorstand

Gemessen mit dem **neuen** Sondenskript gegen einen **vollständigen** Arbeitsbaum auf
0.46.0 – Validator, Sondenskript und Testkatalog dort auf dem Stand von `main`, alles
übrige identisch:

| Einheit | Gegen 0.46.0 | Erwartet |
|---|---|---|
| Sonde 45a | **FEHL** | fällt |
| Sonde 45b | **FEHL** | fällt |
| Sonde 45c | **FEHL** | fällt |
| Sonde 45d | **FEHL** | fällt |
| Gegenprobe 45a | OK | **besteht** |
| Gegenprobe 45b | OK | **besteht** |

**Vier Fundstellen, und die beiden Gegenproben bestehen.** Das ist die richtige Form und
nicht nur die erfreuliche: Eine Gegenprobe stellt einen **zulässigen** Zustand her, und
ein zulässiger Zustand läuft auch dort durch, wo es die neue Prüfung noch gar nicht gibt.
Fiele sie gegen den Vorstand, prüfte sie etwas anderes als ihren Fall.

> **Ein Zwischenfall, der hier hingehört:** Der erste Versuch des Gegenbeweises lief gegen
> einen frischen `git worktree` auf `main` – und **alle** Einheiten fielen, auch die
> Gegenproben. Der Grund ist nicht das Release: Das Framework-Repositorium versioniert
> seine Wurzelerzeugnisse bewusst **nicht** (sie entstehen aus `install.py`), und ein
> frischer Worktree hat sie deshalb nicht. Sein eigener Validatorlauf meldete **46 Fehler**.
> **Ein Vorstand ohne Wurzelerzeugnisse ist kein Vorstand**, und eine Gegenprobe, die
> „0 Fehler" verlangt, fällt dort aus einem Grund, der mit ihrem Gegenstand nichts zu tun
> hat. Der Vorstand ist deshalb ein vollständiger Arbeitsbaum mit drei zurückgesetzten
> Dateien – und der meldet 0 Fehler, 0 Warnungen.

## 4. Der Aufräumer aus 0.46.0 – sein erster echter Fall

Die Sonde zu Gegenstand 2 legt ein Repositorium an. **Git schreibt seine Objektdateien
schreibgeschützt.** Der Aufräumer versuchte dreimal über anderthalb Sekunden zu löschen
und meldete:

```
AUFRAEUMER -    FEHL  sonden_bytecode: C:\…\lw-inst-p8auo49r bleibt liegen
        [WinError 5] Zugriff verweigert: …\.git\objects\03\7c6087d4df…
        3 Versuche ueber 1,5 s, danach aufgegeben.
```

**Er hatte recht und war trotzdem nutzlos.** Er meldete einen Zustand, den er selbst
hätte auflösen können: *Warten hilft gegen eine gehaltene Datei und gar nichts gegen eine
schreibgeschützte.* Die Roadmap führte genau diese Frage als offenen Punkt von 0.46.0
(„unerhoben, ob drei Versuche über 1,5 s für den echten Fall reichen") – **der Fall ist
da, und die Antwort ist nein.**

Jeder Versuch ab dem zweiten nimmt jetzt zuerst den Schreibschutz im ganzen Baum weg.
**Ohne `onerror`/`onexc` von `shutil.rmtree`:** Die beiden Namen haben sich zwischen den
Python-Fassungen abgelöst, und ein Nachweiswerkzeug, das an der Fassung seines
Interpreters hängt, ist genau das, was D-49 abgeschafft hat.

**Die Selbstprobe `A3` misst es** – eine Behebung ohne Sonde ist nach D-23 keine. Sie
gilt auf beiden Betriebssystemen, aus verschiedenen Gründen: Unter Windows belegt sie den
Mechanismus, unter POSIX, dass er nichts kaputt macht (dort blockiert eine
schreibgeschützte *Datei* das Löschen ohnehin nicht). **Wer den Mechanismus unter Windows
entfernt, macht sie rot.**

> **Das ist der Ertrag von 0.46.0, eingelöst binnen eines Releases:** Bis dahin stand an
> dieser Stelle `ignore_errors=True`. Das Verzeichnis wäre liegen geblieben, der Lauf
> wäre grün gewesen, und niemand hätte je erfahren, dass die Sonde zu Prüfung 45 bei
> jedem Lauf ein Repositorium auf der Platte zurücklässt.

## 5. Was dieses Protokoll nicht belegt

- **Nicht, dass die Deckungsliste vollständig ist.** Fünf Schreibweisen gelten; eine
  wirksame, aber exotische sechste meldet die Prüfung als fehlend. Die Grenze steht im
  Kopfkommentar.
- **Nicht, dass Gegenstand 1 die Wirkung prüft.** Eine Regel, die durch eine spätere
  Ausnahmezeile (`!*.pyc`) wieder aufgehoben wird, fällt ihm nicht auf. Den Fall fängt
  Gegenstand 2 – aber nur, wo git da ist.
- **Nicht, dass drei Versuche jetzt reichen.** Sie reichen gegen den Schreibschutz, weil
  er gelöst wird, und gegen eine kurz gehaltene Datei. Gegen eine dauerhaft geöffnete
  reichen sie nicht – und genau das misst `A2`, indem sie sie herstellt.
- **Nicht, dass das Übungsrepositorium hergerichtet ist.** Es führt weiterhin zwei
  versionierte `.pyc` und steht auf 0.45.0. Das gehört zum nächsten Heben dorthin.
