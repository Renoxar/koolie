# Wirksamkeitsnachweis `CR-2026-024` – Platzhalter mit Clientnamen

| Feld | Inhalt |
|---|---|
| Gegenstand | Erweiterung von Prüfung 14: Kein Platzhalter des Kerns trägt einen Clientnamen |
| Prüfmethode | Sonde je Prüfung mit Grenzproben (D-23) |
| Datum | 2026-09-10 |
| Framework-Version | 0.22.0 |
| Ausgangslauf | 0 Fehler, 0 Warnungen |
| Ausführende Rolle | Ersteller (KI-gestützt, Sitzung) |

## Ausgangslage

`CR-2026-020` wies drei Restpunkte aus, darunter den Marker
`VERIFY AGAINST CURRENT <name> DOCUMENTATION` „an fünf Kernstellen". Prüfung 14 fand ihn nicht:
Sie sucht den **kapitalisierten** Clientnamen, ein Platzhalter schreibt ihn **groß**.

## Sonden – müssen gemeldet werden

Angehängt an `framework/core/00-principles.md`, danach zurückgenommen.

| Sonde | Eingebrachter Platzhalter | Ergebnis |
|---|---|---|
| S1 | `VERIFY AGAINST CURRENT DEVIN DOCUMENTATION` (in spitzen Klammern) – Name als eigenes Wort | **gemeldet** |
| S2 | `DEVIN_PROJECT_DIR` (in spitzen Klammern) – Name als Namensteil mit Unterstrich | **gemeldet** |
| S3 | `CLAUDE_SETTINGS_PATH` (in spitzen Klammern) – der zweite Clientname | **gemeldet** |

**S2 war zunächst still.** Die erste Fassung trennte den Platzhalternamen nur an Leerzeichen,
sodass `DEVIN_PROJECT_DIR` ein einziges Token blieb und der Vergleich ins Leere lief. Getrennt
wird seitdem an Leerzeichen **und** Unterstrichen. Ohne diese Sonde wäre die Prüfung mit einer
Lücke ausgeliefert worden, die genau die Hälfte der Fälle betrifft.

**S3 belegt** wie schon bei der Akteursprüfung: Die Namen stammen aus den Pack-Kennungen, nicht
aus einer Liste im Skript. Ein künftiges Client Pack wird ohne Änderung erfasst.

## Grenzproben – dürfen nicht gemeldet werden

| Probe | Eingebrachter Text | Ort | Ergebnis |
|---|---|---|---|
| G1 | `VERIFY AGAINST CURRENT CLIENT DOCUMENTATION` (in spitzen Klammern) | Kernmodul | still |
| G2 | `RUNTIME_DIR`, `CLIENT_NAME` (in spitzen Klammern) | Kernmodul | still |
| G3 | `HOOKS_FILE`, `PERMISSIONS_FILE` (in spitzen Klammern) | Kernmodul | still |
| G4 | `DEVIN_PROJECT_DIR` (in spitzen Klammern) | **Client Pack** | still |
| G5 | `DEVIN_PROJECT_DIR` (in spitzen Klammern) | **Platzhalterregister** | still |

G4 und G5 ziehen die beiden Linien, auf die es ankommt: Im Client Pack ist der Name richtig, und
das Register **nennt** Platzhalter, es verwendet sie nicht.

## Was die Prüfung gefunden hat, das die Zählung nicht sah

`CR-2026-020` führte „fünf Kernstellen". Tatsächlich:

| Ort | Stellen |
|---|---|
| Markdown-Dateien des Kerns | **8** |
| `tests/scripts/hook-overlay-status.py` | 1 |
| `tests/scripts/hook-check-secrets.py` | 1 |

Die beiden Skriptstellen hatte die manuelle Zählung übersehen, weil sie nur `*.md` durchsucht
hatte. **Dasselbe Muster wie bei `CR-2026-020` selbst**, wo die Roadmap 76 Nennungen führte und
es 248 waren: Eine von Hand erhobene Zahl über den eigenen Zustand fällt zu klein aus, weil man
dort zählt, wo man den Fehler vermutet.

## Die Prüfung erwischt ihren eigenen Erklärtext

Dreimal in dieser Sitzung meldete eine neu gebaute Prüfung den Text, der sie **beschreibt** –
den erläuternden Absatz in der Roadmap, den Docstring der Prüffunktion, den Kommentar über der
Trennregel. Jedes Mal war die Meldung **richtig**: Wer einen Namen im Kern verbietet, verbietet
ihn auch in der eigenen Begründung.

Das ist kein Fehlalarm, sondern die Probe aufs Exempel. Die Texte sind so umformuliert, dass sie
die Regel beschreiben, ohne sie zu verletzen.

## Regressionsproben

| Probe | Erwartung | Ergebnis |
|---|---|---|
| R1 | Prüfung 14 meldet weiterhin eine Akteursnennung im Kern | gemeldet |
| R2 | Prüfung 16 meldet weiterhin einen nicht erkannten Werkzeugnamen | gemeldet |
| R3 | Ausgangslauf 0 Fehler | 0 Fehler, 0 Warnungen |

## Was dieser Nachweis nicht belegt

- **Nur Platzhalter werden erfasst.** Eine Client-Bindung außerhalb spitzer Klammern und außerhalb
  der kapitalisierten Form – etwa ein Produktname mitten in einem Codebeispiel – bleibt
  unerkannt. Das ist die bewusste Grenze aus E2: `CLAUDE.md` ist ein Dateiname, kein Akteur.
- **Der dritte Restpunkt aus `CR-2026-020` bleibt offen.** Die Zeile „Umsetzung beim KI-Client"
  in `05-working-model.md` nennt weiterhin clientspezifische Mechanismen. Das ist keine
  Bezeichnungsfrage und braucht einen eigenen Vorgang.

## Gegenzeichnung (Prüfmethode `review`)

| Rolle | Datum | Ergebnis |
|---|---|---|
| Ersteller des Reviews (KI-gestützt, Sitzung) | 2026-09-10 | Dateiname umbenannt, zehn Markerstellen gelöst, Prüfung 14 erweitert; drei Sonden gemeldet, fünf Grenzproben still, drei Regressionsproben; eine Lücke der ersten Fassung durch Sonde S2 gefunden |
| Zweite Rolle: `<FRAMEWORK_OWNER>` | `<TBD: Datum>` | `<TBD: Abnahme; E1, E2 und E3 einzeln entscheiden>` |

Solange die zweite Zeile offen ist, ist dieser Nachweis **vorgelegt, nicht abgezeichnet**.
