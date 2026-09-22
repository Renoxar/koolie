# Änderungsantrag `CR-2026-069`

| Feld | Inhalt |
|---|---|
| Titel | Beide Projekte versionieren den Bytecode des Kerns – der Übernahmeleitfaden nennt nur die Zeilen, die man weglassen soll |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-15 |
| Betroffene Artefakte | `docs/ADOPTION_GUIDE.md` (Abschnitt 2), `tests/scripts/validate-framework.py` (Prüfung 45 neu, Register), `tests/scripts/probe-pruefungen.py` (vier Sonden, zwei Gegenproben, `aufraeumen()`, Selbstprobe `A3`), `tests/TEST_CATALOG.md` (`FW-KO-01`), `governance/DECISION_LOG.md`, `docs/ROADMAP.md`, `CHANGELOG.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Übernahmeleitfaden und Prüfapparat sind Framework-Gut |
| Art | Änderung |
| Dringlichkeit | **Regulär.** Der Schaden ist Hygiene, nicht Sicherheit – aber er trifft **zwei von zwei** Projekten, und das macht ihn zu einer Eigenschaft des Leitfadens, nicht der Projekte |

## 1. Anlass

**Gefunden beim Heben des Piloten** (Kandidat 4 der Übergabe, 0.41.0 → 0.46.0), nicht
gesucht. Beim Ersetzen von `leitwerk-core/` standen zwei `.pyc`-Dateien als „modified" im
Arbeitsbaum – versionierter Bytecode eines Werkzeugs, das bei jedem Lauf neuen erzeugt.

### Abgezählt am 2026-09-15

| Projekt | Framework-Stand | Versionierte Bytecode-Dateien unter `leitwerk-core/` | `.gitignore` deckt `__pycache__` |
|---|---|---|---|
| `devpacks/otp-generator` (Pilot) | 0.41.0 | **6** | nein |
| `devpacks/test-devin-framework` (Übungsrepo) | 0.45.0 | **2** | nein |
| `devpacks/leitwerk` (Framework selbst) | 0.46.0 | 0 | **ja** |

**Zwei von zwei.** Das Framework-Repositorium selbst hat die Zeile seit jeher – und genau
deshalb ist der Fehler dort nie aufgefallen.

### Warum das kein Versehen der Projekte ist

`docs/ADOPTION_GUIDE.md` Abschnitt 2 sagte zur `.gitignore` genau einen Satz: *„Übernimm
die `.gitignore` des Framework-Repositorys **nicht** unverändert"* – und nennt dann die
vier Zeilen, die ein Projekt **weglassen** muss. Welche Zeile es **braucht**, stand
nirgends.

> **Das ist die Bauform des Befunds von 0.45.0, ein zweites Mal:** *Eine Anweisung, die
> die halbe Migration beschreibt, ist gefährlicher als keine.* Wer dem Leitfaden wörtlich
> folgt, schreibt eine eigene `.gitignore` – und hat danach keine Zeile gegen den
> Bytecode, weil ihm niemand gesagt hat, dass er eine braucht.

### Was der Schaden ist, und was er nicht ist

**Kein Sicherheitsproblem.** Bytecode des Frameworks enthält keine Projektgeheimnisse.
Der Schaden ist:

- **Dauerrauschen im Arbeitsbaum.** Zwei der sechs Dateien standen beim Auschecken des
  Piloten als geändert da, ohne dass jemand etwas getan hätte.
- **Ein Erzeugnis, das seine Quelle überlebt.** Nach dem Heben des Piloten zeigte `git
  status` vier `.pyc` als **gelöscht** – sie gehörten zu einem Kern, den es nicht mehr
  gibt, und wären als Löschung committet worden.
- **Ein falscher Eindruck von Vollständigkeit.** Wer `leitwerk-core/` ersetzt, ersetzt
  nicht den Bytecode; die Versionierung führt dann beides nebeneinander.

## 2. Vorgeschlagene Änderung

1. **Der Leitfaden nennt die Zeile.** Abschnitt 2 bekommt den Gegensatz zu den vier
   Weglass-Zeilen: `__pycache__/` gehört hinein, mit Begründung und mit dem Weg für
   bereits versionierte Dateien (`git rm -r --cached`).
2. **Prüfung 45** mit **zwei Gegenständen**: die Regel in der `.gitignore` und der
   Bestand über `git ls-files`.
3. **Vier Sonden und zwei Gegenproben** nach D-23.
4. **`aufraeumen()` löst den Schreibschutz** – siehe Abschnitt 3, das ist beim Bauen
   angefallen.

## 3. Was beim Bauen angefallen ist – der Aufräumer aus 0.46.0 hatte seinen ersten Fall

Die Sonde zu Gegenstand 2 legt ein echtes Repositorium an (`git init`). **Git schreibt
seine Objektdateien schreibgeschützt.** Der Aufräumer von 0.46.0 versuchte dreimal über
anderthalb Sekunden zu löschen und meldete dreimal dasselbe:

```
AUFRAEUMER -    FEHL  sonden_bytecode: C:\…\lw-inst-p8auo49r bleibt liegen
        [WinError 5] Zugriff verweigert: …\.git\objects\03\7c6087d4df…
        3 Versuche ueber 1,5 s, danach aufgegeben.
```

**Der Aufräumer hatte recht und war trotzdem nutzlos.** Er meldete einen Zustand, den er
selbst hätte auflösen können: *Warten hilft gegen eine gehaltene Datei und gar nichts
gegen eine schreibgeschützte.* Die Roadmap führte das als offenen Punkt („unerhoben, ob
drei Versuche für den echten Fall reichen") – **der Fall ist da, und die Antwort ist
nein.**

Jeder Versuch ab dem zweiten nimmt jetzt zuerst den Schreibschutz weg. **Die Selbstprobe
`A3` misst es**, denn eine Behebung ohne Sonde ist nach D-23 keine.

## 4. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | **Prüft 45 die Regel, den Bestand, oder beides?** | **Beides.** Gegenstand 1 vergleicht die `.gitignore` gegen eine Liste wirksamer Schreibweisen; Gegenstand 2 zählt über `git ls-files`, was unter `<CORE_DIR>/` verfolgt ist | **Die Regel allein wäre die halbe Migration ein zweites Mal:** Git liest die `.gitignore` für bereits verfolgte Dateien **nicht**. Wer die Zeile nachträgt und `git rm --cached` vergisst, bekäme einen grünen Lauf und hätte die sechs Dateien weiter im Repositorium. Der Bestand allein wiederum sagt nicht, wie man die Wiederholung verhindert. Preis von „beides": eine bedingte Prüfhälfte, und ihre Sonde braucht ein echtes Repositorium – `kopie()` lässt `.git` weg, das geht nur im Bündel |
| **E2** | **Was tut Gegenstand 2, wo git fehlt?** | **Er sagt als Warnung, dass er nicht gelaufen ist.** Dieselbe Bauform, die dieses Skript für das fehlende PyYAML schon hat | **Jede Sonde dieses Skripts erzeugt die Warnung** – sie läuft auf einer Kopie ohne `.git`. Das ist gewollt und harmlos (Gegenproben verlangen 0 **Fehler**, nicht 0 Warnungen), aber die Ausgabe wird um eine Zeile länger. Verworfen: schweigen – eine Prüfhälfte, die stumm ausfällt, ist der Befundtyp selbst |
| **E3** | **Was gilt bei fehlender `.gitignore`?** | **Warnung.** Ob ein Projekt überhaupt versioniert, kann kein Validator wissen | **Wer die Datei löscht, macht Gegenstand 1 zur Warnung statt zum Fehler.** Gegenstand 2 fängt den echten Fall trotzdem, sobald git da ist. Verworfen: Fehler (ein Projekt ohne Versionierung bekäme einen Fehler, den es nicht abstellen kann) und Schweigen (der verlorene Anker, den 28, 29, 31 und 40 ausdrücklich selbst melden) |
| **E4** | **Welche Schreibweisen gelten als Deckung?** | **Eine kleine ausdrückliche Liste:** `__pycache__/`, `__pycache__`, `**/__pycache__/`, `*.pyc`, `**/*.pyc` | **Was die Liste nicht kennt, meldet sie** – ein Projekt mit einer exotischen, aber wirksamen Schreibweise bekommt einen falschen Fehler. Die Gegenprobe belegt, dass `*.pyc` allein durchläuft. Verworfen: nur `__pycache__/` (dann wäre ein richtiges Projekt rot – der Fehler, den Prüfung 37 einmal gemacht hat) und `git check-ignore` (dann bräuchte **auch** Gegenstand 1 git, und man könnte ihn gleich weglassen) |
| **E5** | **Schreibt `install.py --update` die Zeile selbst?** | **Nein.** Der Leitfaden nennt sie, die Prüfung verlangt sie, das Projekt trägt sie ein | **Bequem wäre es.** Aber die `.gitignore` ist eine Projektdatei, und das Framework hat dort noch nie hineingeschrieben – D-46 ist gerade darum gebaut. Die Zusage „Projektdateien bleiben unberührt" trüge ab dann eine Ausnahme, und das Werkzeug müsste den Aufbau einer fremden Datei kennen |
| **E6** | **Wie wird der Schreibschutz behandelt?** | **Jeder Versuch ab dem zweiten löst ihn im ganzen Baum**, leise, danach der nächste Löschversuch. Ohne `onerror`/`onexc` von `shutil.rmtree` | Die beiden Namen haben sich zwischen den Python-Fassungen abgelöst; **ein Nachweiswerkzeug, das an der Fassung seines Interpreters hängt, ist genau das, was D-49 abgeschafft hat.** Preis: ein zusätzlicher Baumdurchlauf je Fehlversuch – er fällt nur an, wenn ohnehin etwas klemmt |

## 5. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen.** E1 bis E4 wie vorgelegt am 2026-09-15 durch den Framework Owner entschieden; E5 ebenfalls; **E6 ist beim Bauen angefallen** und folgt aus D-23 – eine Behebung ohne Sonde ist keine |
| Datum | 2026-09-15 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Eintrag | D-97 (der Bytecode des Kerns gehört nicht in die Versionierung, und die Prüfung fragt nach Regel **und** Bestand) |
| Auflagen | **Der Gegenbeweis gehört dazu und ist eigen:** Die vier Sonden MÜSSEN gegen 0.46.0 fallen, **und die beiden Gegenproben MÜSSEN dort bestehen** – ein zulässiger Zustand läuft auch ohne die neue Prüfung durch. Dazu die Abzählung an beiden Projekten, nicht nur am Piloten |
| Ziel-Release | `0.47.0` |
| Umsetzung | umgesetzt mit `0.47.0` |
