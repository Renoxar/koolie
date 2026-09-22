# Änderungsantrag `CR-2026-095`

| Feld | Inhalt |
|---|---|
| Titel | Der Prüfapparat bekommt einen Filter – die Schleife wird kürzer, der Nachweis nicht |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-19 |
| Betroffene Artefakte | `tests/scripts/probe-pruefungen.py` (Schalter `--nur` und `--liste`, Auswahl, Teillaufbanner, Selbstprobe `F1`/`F2`), `governance/DECISION_LOG.md` (D-191), `docs/ROADMAP.md` (Posten 0.69.0), `tests/protocols/2026-09-19-pruefapparat-filter.md` (neu), `CHANGELOG.md`, `VERSION` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand ist der Prüfapparat |
| Art | Werkzeug, Arbeitsablauf |
| Dringlichkeit | **Regulär, aber vor Bündel 2.** Der Meßtag von 0.68.0 hat den Anlaß geliefert, und die vier folgenden Bündel bezahlen ihn sonst viermal |

## 1. Anlaß

**Gemessen am 2026-09-19:** `probe-pruefungen.py` fährt **238 Einheiten**, rund **2300 s
Rechenzeit** und **290 s Wanduhr** – und das **zweimal je Release** (D-49). Jede Einheit
legt eine eigene Kopie des Repositoriums an und fährt den **ganzen** Validator, um
**eine** Meldung zu sehen.

🔴 **Der Schaden ist nicht die Rechenzeit, sondern die Gewohnheit:** Ein Werkzeug, das vor
jedem Zwischenschritt fünf Minuten kostet, wird seltener gefahren, als es soll. **Der
Nachweis nach D-23 ist nicht wertvoll, weil er existiert, sondern weil er gefahren wird.**

## 2. Was eingebaut ist

| Schalter | Was er tut |
|---|---|
| `--nur 44,62` | fährt die Einheiten, deren Kennung mit einer der Marken **beginnt** |
| `--liste` | zeigt alle Einheiten mit Art, Kennung und Satz |

**Eine Marke ohne Treffer ist ein Abbruch**, kein leerer Lauf – sonst meldete ein
Tippfehler *„alle bestanden"*.

🔴 **Der Teillauf sagt dreimal, daß er keiner ist:** im Kopf (Banner), in der
Ergebniszeile (*„TEILLAUF, 5 von 238"*) und im Abschlußsatz. **Die Bauform, gegen die das
steht, ist bekannt:** *die Null durch Konstruktion* (0.59.1) – grün, weil nichts gefahren
wurde.

## 3. Gemessen

| Lauf | Einheiten | Wanduhr |
|---|---|---|
| voll | 238 | **rund 290 s** |
| `--nur 62,selbstprobe_filter` | 5 | **8,0 s** |

## 4. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Filter oder Abschalten?** | **Filter** (D-191); der volle Lauf bleibt die Abnahme | Ein Schalter mehr und die Gefahr der Verwechslung – dagegen stehen drei Hinweise im Lauf. **Verworfen: Prüfungen abschalten** – eine abgeschaltete Prüfung fällt erst auf, wenn sie gebraucht wird (Prüfung 49 und 60 liefen fünfzehn Monate ohne Gegenstand) |
| **E2** | **Auch die Kopie je Bahn und `--nur-pruefung` im Validator?** | **Vertagt** | Beide senken den **vollen** Lauf, und der läuft zweimal je Release – nicht zwanzigmal am Tag. **Der Filter trifft den Engpaß, den der Meßtag gezeigt hat** |
| **E3** | **Braucht der Filter selbst einen Nachweis?** | **Ja, eine Selbstprobe** (`F1`, `F2`) auf gebauten Kennungen | Zwei Einheiten mehr im Lauf. **Ein Filter ohne Nachweis wählt irgendwann das Falsche, und der Lauf meldet es als bestanden** |

## 5. Entscheidung

**E1 bis E3 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-19). Decision Record
**D-191**.

## 6. Abnahme

- `validate-framework.py`: **0 Fehler, 0 Warnungen**.
- `probe-pruefungen.py` **voll** in beiden Kodierungsumgebungen (D-49) – der Filter darf
  den vollen Lauf nicht verändern, und das ist der eigentliche Nachweis.
- **Selbstprobe `F1`/`F2`** auf sechs gebauten Kennungen: Auswahl am Anfang der Kennung,
  ohne Rücksicht auf Großschreibung, `6` trifft auch `62a`.
