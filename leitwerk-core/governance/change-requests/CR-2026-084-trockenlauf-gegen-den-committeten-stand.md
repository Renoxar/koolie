# Änderungsantrag `CR-2026-084`

| Feld | Inhalt |
|---|---|
| Titel | Der Trockenlauf hat den committeten Stand gemessen – und die Null war eine Tautologie |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-18 |
| Betroffene Artefakte | `tests/protocols/2026-09-18-wirkungsnachweise-0.59.0.md` (Nachtrag), `CHANGELOG.md` (Migrationshinweis von 0.59.0 berichtigt, Eintrag 0.59.1), `docs/ROADMAP.md` (eine Zeile im Abschnitt zu 0.59.0), `governance/DECISION_LOG.md` (`K-56`), `VERSION` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand ist eine berichtigte Messaussage |
| Art | Berichtigung einer gemessenen Zahl, neuer Klärungspunkt |
| Dringlichkeit | **Regulär.** Kein Sicherheitsvorfall. **Aber ohne Aufschub**, weil die falsche Zahl in einem gemergten Release steht |

## 1. Anlass

Der Migrationshinweis von `0.59.0` sagt: *„Keiner. … `install.py --update` schreibt nichts
außerhalb von `leitwerk-core/` – gemessen am Übungsrepositorium."*

**Der Satz ist falsch, und die Messung dahinter war keine.**

Der Trockenlauf baute seinen Prüfling so:

```
git archive HEAD leitwerk-core | tar -x -C /c/lw-mig/ueb
python /c/lw-mig/ueb/leitwerk-core/install.py --update --dry-run --root /c/lw-mig/ueb
```

🔴 **`git archive HEAD` nimmt den committeten Stand.** Zum Zeitpunkt des Laufs war
`0.59.0` noch nicht committet – der Prüfling trug also `0.58.0`, und die Kopie des
Übungsrepositoriums ebenfalls. **Gemessen wurde 0.58.0 gegen 0.58.0.**

> 🔴 **Eine Null, die durch Konstruktion entsteht, ist keine Messung, sondern eine
> Tautologie.** Sie sieht genauso aus wie eine gemessene Null – und dieses Projekt hat
> genau dafür eine Regel: *Ein Lauf, der eine Null meldet, ist erst ein Messwert, wenn
> eine Ergebniszeile daneben steht.* Hier stand eine, und sie war aus demselben Fehler.

> ⚠️ **Derselbe Fehler war in derselben Sitzung schon einmal aufgetreten.** Beim Aufbau
> der Messumgebung für den Sitzungstest baute `umgebungen-bauen.py` die Bäume ebenfalls
> aus `git archive HEAD` – und maß deshalb Framework `0.57.1` statt `0.58.0`. Das ist
> aufgefallen, weil ein Lauf die Version in seinem Ergebnisbericht **nannte**; zwei Läufe
> wurden verworfen und neu gefahren.
>
> **Beim zweiten Mal hat der Fehler eine Zahl in ein gemergtes Release getragen**, weil
> dort nichts sie nannte.

## 2. Die Messung, richtig gefahren

Gegen den gemergten Stand (`cdcc4fa`):

| Projekt | Stand vorher | `--update --dry-run` | welche Dateien |
|---|---|---|---|
| Übungsrepositorium | 0.58.0 | 0 angelegt, **1 aktualisiert** | `.devin/skills/fw-tests/TESTS.md` |
| Pilot `otp-generator` | 0.54.1 | 0 angelegt, **5 aktualisiert** | die vier Plan-Skill-Dateien aus 0.57.1 **plus** `.claude/skills/fw-tests/TESTS.md` |

## 3. Und die eine Datei ist ein Befund für sich (`K-56`)

Es ist das **Testblatt**, in das `0.59.0` zwei Ergebniszellen eingetragen hat.

> 🔴 **Eine Ergebniszelle eines dezentralen Testblatts wandert bei jedem Update in die
> Laufzeitschicht jedes übernehmenden Projekts.**
>
> Das steht quer zu **zwei** Entscheidungen dieses Projekts:
>
> - **D-119** sagt, das Eintragen eines Ergebnisstatus sei *keine Änderung des Trägers im
>   Sinne der Versionspflicht* – „eine Ergebniszelle ist eine Aufzeichnung, keine
>   Anweisung". **`install.py` liefert sie trotzdem aus.**
> - **D-141** hat in demselben Release die Trennlinie *Regelquelle gegen Aufzeichnung*
>   gezogen – für den Kontrollzuschnitt. **Ein Testblatt fällt nach dieser Linie auf die
>   Seite der Aufzeichnung und wird auf der Seite der Regelquelle ausgeliefert.**
>
> **Betroffen sind 87 Zellen in dreizehn Blättern, und die Releases `0.61.0` bis
> `~0.65.0` füllen sie.** Jede einzelne erzeugt danach eine Datei im Migrationshinweis
> jedes übernehmenden Projekts.

**Drei Wege sind denkbar, und keiner ist offensichtlich richtig:**

| Weg | Preis |
|---|---|
| Das Blatt beim Ausliefern um die Ergebnisspalte kürzen | `install.py` verändert dann einen Träger beim Kopieren – eine Fähigkeit, die es heute nicht hat und die schwer zu prüfen ist |
| Das Blatt gar nicht ausliefern | Dem übernehmenden Projekt fehlen die Testfälle seiner Skills – und `FW-RE-01` verlangt sie |
| So lassen und die Folge benennen | Der heutige Zustand, nur mit der Benennung. **Jeder Sitzungstest der nächsten fünf Releases erzeugt dann einen Migrationseintrag** |

**Die Entscheidung gehört nicht in dieses Nachtragsrelease.** Sie ist `K-56`.

## 4. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | **Wird die falsche Zahl im Protokoll gelöscht oder bleibt sie stehen?** | **Sie bleibt stehen und trägt einen Nachtrag.** Dieselbe Entscheidung wie bei 0.54.1 und 0.58.0: *Ein Protokoll, das seine eigene Fehleinordnung löscht, verliert den Lernwert* | **Das Protokoll widerspricht sich in zwei Zeilen** – sichtbar, und genau das ist der Zweck |
| **E2** | **Eigenes Release oder Nachtrag im nächsten?** | **Eigenes Release `0.59.1`.** Der Migrationshinweis von `0.59.0` ist bereits ausgeliefert; ein Projekt, das ihn liest, hebt nicht und wundert sich über eine geänderte Datei | **Ein Release, das keine Zahl von D-11 bewegt** – das vierte dieser Art (0.53.1, 0.56.1, 0.56.2, 0.57.1) |
| **E3** | **Wird `K-56` jetzt entschieden?** | **Nein.** Alle drei Wege haben einen Preis, und der teuerste Weg wäre, ihn heute zu wählen, um das Nachtragsrelease größer aussehen zu lassen | **Ein offener Punkt mehr**, und er wird mit jedem Sitzungstest der nächsten fünf Releases teurer |
| **E4** | **Bekommt der Fehler eine Auflage?** | **Ja, und sie ist eine Zeile:** *Ein Trockenlauf gegen `git archive HEAD` misst den committeten Stand – wer den Arbeitsbaum messen will, kopiert ihn* (`git archive` ist für den **Vergleichsstand** richtig, nicht für den Prüfling) | **Keine Prüfung setzt das durch.** Es ist eine Regel für den Menschen, wie die Berührungsprobe |

## 5. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle vier Fragen wie vorgelegt.** E1 die falsche Zahl bleibt stehen und trägt den Nachtrag; E2 eigenes Release `0.59.1`; E3 `K-56` bleibt offen; E4 die Auflage steht im Protokoll und in der Übergabe |
| Datum | 2026-09-18 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | keine. **Das ist Absicht:** Die Berichtigung einer Messaussage ist keine Entscheidung, und die Auflage aus E4 ist eine Arbeitsregel ohne Ermessensfrage. Neu ist allein `K-56` |
| Auflagen | **Ein Trockenlauf, der den Arbeitsbaum messen soll, nimmt den Arbeitsbaum** – `git archive HEAD` liefert den committeten Stand und ist damit für den **Vergleichsstand** richtig und für den **Prüfling** falsch. **Und eine Null aus einem Trockenlauf gehört gegen die Erwartung gehalten:** Ein Release, das einen ausgelieferten Träger anfasst, kann keine Null haben |
| Ziel-Release | `0.59.1` |
| Umsetzung | umgesetzt mit `0.59.1` |

## 6. Abnahme

| Lauf | Ergebnis |
|---|---|
| `validate-framework.py` | **0 Fehler, 0 Warnungen** |
| `probe-pruefungen.py .` **mit** `PYTHONIOENCODING=utf-8` | **alle Sonden und Gegenproben bestanden** (200,9 s) |
| `probe-pruefungen.py .` **ohne** `PYTHONIOENCODING` | **alle Sonden und Gegenproben bestanden** (170,1 s) |
| Pruefung 46, Kriterium 2 | **93** – unveraendert, dieses Release bewegt keine Zahl von D-11 |

**Der Sondenlauf war nicht optional:** Dieses Release fasst `docs/ROADMAP.md` und
`governance/DECISION_LOG.md` an, und beide tragen Pfadliterale des Sondenskripts mit
Praeparationswaechter (`K-51`). **Ein sorgloser Prosaeingriff dort laesst den Validator
gruen und den Sondenlauf fallen.**
