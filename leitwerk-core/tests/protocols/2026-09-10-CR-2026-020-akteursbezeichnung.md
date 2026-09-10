# Wirksamkeitsnachweis `CR-2026-020` – Prüfung 14 (Akteursbezeichnung)

| Feld | Inhalt |
|---|---|
| Gegenstand | Prüfung 14 des Validators: Kein Client wird im Kern als Akteur benannt (D-02, D-28) |
| Prüfmethode | Sonde je Prüfung mit Gegenproben (D-23) |
| Datum | 2026-09-10 |
| Framework-Version | 0.18.0 |
| Ausgangslauf | 0 Fehler, 0 Warnungen |
| Ausführende Rolle | Ersteller (KI-gestützt, Sitzung) |

## Anlass

D-23 verlangt für einen bestandenen Testfall neben dem grünen Lauf einen Wirksamkeitsnachweis.
Prüfung 14 ist mit `CR-2026-020` neu; ohne Nachweis wäre nicht belegt, dass sie etwas findet.

**Das war hier nicht theoretisch.** Im ersten Einbau fehlten die Wortgrenzen im Suchmuster – ein
Steuerzeichen war an ihre Stelle getreten. Die Prüfung meldete **null Treffer bei 27
vorhandenen** und lief grün. Aufgefallen ist es allein dadurch, dass das erwartete Ergebnis
vorher feststand und mit dem tatsächlichen verglichen wurde. Derselbe Befundtyp wie `FW-KO-01`
(eine grüne Prüfung, die sechs von 22 Defekten durchließ) und `AP2-CC-09` (eine vorgeschriebene
Prüfung, die nie gelaufen war).

## Sonden – müssen gemeldet werden

Jede Sonde wurde einzeln in eine unveränderte Datei eingebracht und danach zurückgenommen.

| Sonde | Eingebrachter Defekt | Datei | Ergebnis |
|---|---|---|---|
| S1 | `Devin prüft den Ist-Zustand vor jeder Änderung.` | `framework/core/00-principles.md` | **gemeldet:** „'Devin' benennt einen Client als Akteur; der Kern ist werkzeugneutral (D-02)" |
| S2 | `Die Aufgabe wird an Claude delegiert.` | `framework/core/00-principles.md` | **gemeldet** – der zweite Clientname wird gleichrangig erfasst, ohne dass er in der Prüfung steht |
| S3 | `- [ ] Devin hat den Scope bestätigt.` | `checklists/01-preflight.md` | **gemeldet** – auch außerhalb von `framework/core/` |

S2 belegt die tragende Eigenschaft: Die Namen stammen aus den **Pack-Kennungen**
(`clients/*/manifest.json`), nicht aus einer Liste im Prüfskript. Ein künftiges Client Pack
wird ohne Änderung an der Prüfung erfasst.

## Grenzproben – dürfen nicht gemeldet werden

| Probe | Eingebrachter Text | Datei | Ergebnis |
|---|---|---|---|
| G1 | `Getestet gegen Devin Desktop 3.8.20.` | `framework/core/00-principles.md` | still – Produktname mit Zusatz |
| G2 | `Die Devin-Desktop-Installation ist Voraussetzung.` | `framework/core/00-principles.md` | still – Produktname auch mit Bindestrich |
| G3 | `Devin wurde als Akteur entfernt.` | `CHANGELOG.md` | still – historisches Dokument |
| G4 | `Devin lädt AGENTS.md beim Sitzungsstart.` | `clients/devin-desktop/CLIENT_PACK.md` | still – im Client Pack ist der Name richtig |

G2 war beim ersten Entwurf ein **Fehlalarm**: Das Muster schloss nur `Devin Desktop` mit
Leerzeichen aus und meldete `Devin-Desktop-Version` in `tests/TEST_CATALOG.md`. Die erlaubten
Vollformen werden seitdem ebenfalls aus der Pack-Kennung abgeleitet (`devin-desktop` →
`Devin Desktop`, `Devin-Desktop`), statt sie im Skript zu pflegen.

## Regressionsproben – keine bestehende Prüfung verdrängt

| Probe | Erwartung | Ergebnis |
|---|---|---|
| R1 | Prüfung 13 meldet ein Versionsfeld, das kein `MAJOR.MINOR.PATCH` ist | **still** – siehe Befund unten |
| R2 | Prüfung 5 meldet einen Skill ohne `triggers` | **gemeldet:** „triggers fehlt" |

### Befund aus R1 – Prüfung 13 prüft die Versionsfelder der Kernartefakte nicht

`| Version | \`0.1\` |` und `| Version | \`abc\` |` in `checklists/01-preflight.md` laufen beide
mit 0 Fehlern durch. Der Kopfkommentar des Validators sagt zu Prüfung 13 zu: „Versionsfelder in
der Form `MAJOR.MINOR.PATCH`". Tatsächlich deckt sie drei Dinge ab – die Overlay-Version an
ihren drei Ablageorten, `<CORE_DIR>/VERSION` und die Steckbriefangabe zur kompatiblen
Framework-Version. Die Versionsfelder der rund sechzig Kernartefakte prüft sie nicht.

**Schwere: mittel.** Derselbe Befundtyp wie `FW-KO-01`: eine Prüfung, die mehr zusagt, als sie
leistet. Sie ist mit diesem Release **ausgewiesen, nicht geschlossen** – eine eigene Prüfung
braucht einen eigenen Wirksamkeitsnachweis und gehört nicht in ein Release, das die
Akteursbezeichnung löst.

Bemerkenswert am Zeitpunkt: Der Befund fiel an, während 62 Versionsfelder von Hand um eine
PATCH-Stelle gehoben wurden – ohne dass irgendetwas geprüft hätte, ob das Ergebnis gültig ist.

## Was dieser Nachweis nicht belegt

- **Dass der Kern vollständig neutral ist.** Belegt ist, dass Prüfung 14 eine Akteursnennung
  findet und einen Produktnamen durchlässt. Ob jede der 248 ersetzten Stellen sprachlich richtig
  aufgelöst ist, ist eine Frage des Lesens, nicht der Prüfung; sie ist Gegenstand der
  Gegenzeichnung.
- **Dass sich das Verhalten einer Sitzung nicht ändert.** Die Laufzeitschicht ist seit 0.12.0
  frei von der Akteursbezeichnung; die Langform wird nicht in eine Sitzung geladen. Ein Beleg
  aus einer laufenden Sitzung liegt nicht vor und ist für diese Änderung auch nicht vorgesehen.
- **Pfadnennungen.** `~/.devin/plans/` und die clientspezifischen Inhalte der Zeile „Umsetzung
  beim KI-Client" in `05-working-model.md` sind Sache von Prüfung 12 und bleiben offen.

## Gegenzeichnung (Prüfmethode `review`)

Rollen statt Personen (`framework/runtime/rules/20-project-overlay.md`). D-23 verlangt für die
Prüfmethode `review` eine **zweite Rolle**; ein grüner Lauf und ein Wirksamkeitsnachweis
ersetzen sie nicht. Die fünf Auflösungen mit Ermessensspielraum liegen in `CR-2026-020`
Abschnitt 4 einzeln vor; E1 und E2 sind bereits entschieden.

| Rolle | Datum | Ergebnis |
|---|---|---|
| Ersteller des Reviews (KI-gestützt, Sitzung) | 2026-09-10 | 248 Akteursnennungen in 78 Dateien gelöst; Prüfung 14 eingeführt; drei Sonden gemeldet, vier Grenzproben still; zwei Nebenbefunde aufgenommen |
| Zweite Rolle: `<FRAMEWORK_OWNER>` | `<TBD: Datum>` | `<TBD: Abnahme; E3, E4 und E5 einzeln entscheiden>` |

Solange die zweite Zeile offen ist, ist dieser Nachweis **vorgelegt, nicht abgezeichnet**.
