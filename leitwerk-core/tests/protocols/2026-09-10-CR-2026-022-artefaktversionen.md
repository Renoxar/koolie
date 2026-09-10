# Wirksamkeitsnachweis `CR-2026-022` – Prüfung 13, Artefaktversionen

| Feld | Inhalt |
|---|---|
| Gegenstand | Erweiterung von Prüfung 13: Das Versionsfeld jedes Kernartefakts hat die Form `MAJOR.MINOR.PATCH` |
| Prüfmethode | Sonde je Prüfung mit Grenzproben (D-23) |
| Datum | 2026-09-10 |
| Framework-Version | 0.20.0 |
| Ausgangslauf | 0 Fehler, 0 Warnungen |
| Ausführende Rolle | Ersteller (KI-gestützt, Sitzung) |

## Ausgangslage

Die Blindstelle war mit `CR-2026-020` ausgewiesen und durch dessen Regressionsprobe R1 belegt:
`| Version | 0.1 |` und `| Version | abc |` in `checklists/01-preflight.md` liefen beide mit
0 Fehlern durch, obwohl der Kopfkommentar des Validators „Versionsfelder in der Form
`MAJOR.MINOR.PATCH`" zusagte.

## Sonden – müssen gemeldet werden

Jede Sonde wurde einzeln eingebracht, ihr Ankommen in der Datei verifiziert und danach
zurückgenommen.

| Sonde | Eingebrachter Defekt | Datei | Ergebnis |
|---|---|---|---|
| S1 | Versionswert `0.1` – zwei Stellen statt drei | `checklists/01-preflight.md` | **gemeldet** |
| S2 | Versionswert `abc` – gar keine Zahl | `checklists/01-preflight.md` | **gemeldet** |
| S3 | Versionswert `1.0`, Steckbriefzeile ohne Backticks | `framework/core/00-principles.md` | **gemeldet** |

S3 belegt, dass beide im Kern vorkommenden Schreibweisen erfasst werden: mit Backticks
(Checklisten, Skills) und ohne (Kernmodule).

Die Meldung im Wortlaut:

```
leitwerk-core/checklists/01-preflight.md: Versionsfeld '0.1' ist kein Semantic
Versioning (MAJOR.MINOR.PATCH). Eine Angabe, die keiner Form folgt, laesst sich nicht
vergleichen - und eine Version, die sich nicht vergleichen laesst, unterscheidet keine
zwei Zeitpunkte (D-25, FW-VN-01)
```

## Grenzproben – dürfen nicht gemeldet werden

| Probe | Eingebrachter Wert | Ergebnis |
|---|---|---|
| G1 | `2.10.33` – mehrstellige Stellen | **still** |
| G2 | `<TBD: 0.1.0>` – nicht ausgefüllte Vorlage | **still** |

## Fehlalarm der ersten Fassung

Die erste Fassung des Musters war zu breit und meldete
`templates/project-overlay/OVERLAY.md: Versionsfeld 'Datum' ist kein Semantic Versioning`.
Getroffen war die **Kopfzeile des Overlay-Änderungsverlaufs**:

```
| Version | Datum | Änderung | Autor (Rolle) | Validierung bestanden |
```

Eine Steckbriefzeile hat genau zwei Spalten. Das Muster ist seitdem auf das Zeilenende
verankert. Derselbe Fehlertyp wie bei Prüfung 14 in `CR-2026-020`, wo `Devin-Desktop` zunächst
als Akteursnennung gemeldet wurde: **Ein Muster, das die richtige Sache findet, findet zunächst
auch die falschen.** Die Grenzproben sind dafür da, nicht die Sonden.

## Regressionsproben

| Probe | Erwartung | Ergebnis |
|---|---|---|
| R1 | Der bestehende Teil von Prüfung 13 meldet weiterhin | **gemeldet:** „Kompatible Framework-Version '0.1.0' passt nicht zu `leitwerk-core/VERSION`" nach Verfälschung der Steckbriefangabe |
| R2 | Prüfung 15 (`CR-2026-021`) meldet weiterhin einen nicht lauffähigen Hook-Interpreter | **gemeldet** nach Zurückdrehen des Hook-Aufrufs auf `python3` |

## Was dieser Nachweis nicht belegt

- **Nicht, dass eine Version sich bewegt, wenn sich das Artefakt ändert.** Das war der tragende
  Befund von `FW-VN-01`: Alle 13 Skills standen unverändert auf `0.1.0`, obwohl alle 13 geändert
  worden waren. Diese Frage braucht die Versionsgeschichte, nicht die Datei; sie bleibt beim
  Release-Prozess und außerhalb der Reichweite des Validators.
- **Nicht, dass die Versionen inhaltlich richtig sind.** Geprüft wird die Form, nicht die
  Angemessenheit einer MAJOR-, MINOR- oder PATCH-Anhebung.

## Gegenzeichnung (Prüfmethode `review`)

| Rolle | Datum | Ergebnis |
|---|---|---|
| Ersteller des Reviews (KI-gestützt, Sitzung) | 2026-09-10 | Prüfung 13 erweitert; drei Sonden gemeldet, zwei Grenzproben still; ein Fehlalarm der ersten Fassung behoben |
| Zweite Rolle: `<FRAMEWORK_OWNER>` | `<TBD: Datum>` | `<TBD: Abnahme; E1 und E2 einzeln entscheiden>` |

Solange die zweite Zeile offen ist, ist dieser Nachweis **vorgelegt, nicht abgezeichnet**.
