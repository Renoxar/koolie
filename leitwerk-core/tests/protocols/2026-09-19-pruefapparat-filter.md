# Protokoll: Der Prüfapparat bekommt einen Filter

| Feld | Inhalt |
|---|---|
| Gegenstand | Laufzeit und Gebrauch von `probe-pruefungen.py` |
| Framework-Version | 0.69.0 (`CR-2026-095`, D-191) |
| Datum | 2026-09-19 |
| Prüfmethode | Messung der Wanduhr vor und nach dem Einbau, Selbstprobe auf gebauten Kennungen, voller Abnahmelauf in beiden Kodierungsumgebungen |
| Ergebnis | 🟢 **Derselbe Gegenstand in 8,0 s statt 293 s.** Der volle Lauf ist unverändert grün; ein Teillauf sagt an drei Stellen, daß er keiner ist |

## 1. Die Zahl, die den Anlaß gibt

| Lauf | Einheiten | Rechenzeit | Wanduhr (8 Bahnen) |
|---|---|---|---|
| 0.68.0, `cp1252` | 237 | 2306,3 s | 293,3 s |
| 0.68.0, `utf-8` | 237 | 2219,4 s | 281,8 s |

**Zweimal je Release** (D-49). Jede Einheit kopiert das Repositorium und fährt den ganzen
Validator, um eine Meldung zu sehen.

## 2. Der Einbau

`--nur <Marken>` wählt die Einheiten, deren Kennung mit einer der Marken **beginnt**;
`--liste` zeigt alle. **Eine Marke ohne Treffer bricht ab.**

🔴 **Der Teillauf ist als solcher gekennzeichnet – dreimal.** Die Bauform, gegen die das
steht, hat dieses Projekt schon einmal bezahlt: *Die Null durch Konstruktion* (0.59.1)
sieht genauso aus wie eine gemessene Null.

## 3. Gemessen nach dem Einbau

```
TEILLAUF: 5 von 238 Einheiten (--nur 62,selbstprobe_filter)
Das ist KEIN Abnahmelauf. …
Ergebnis (TEILLAUF, 5 von 238 Einheiten): alle gewaehlten Einheiten bestanden
real    0m7,977s
```

🟢 **Und der erste Teillauf hat sich sofort getragen:** Er meldete zwei Abweichungen, weil
der neue Kopfkommentar `D-191` nannte und der Decision Record noch nicht eingetragen war –
**in acht Sekunden statt in fünf Minuten.**

## 4. Abnahme

| Lauf | Ergebnis |
|---|---|
| `validate-framework.py` | 🟢 **0 Fehler, 0 Warnungen** |
| `probe-pruefungen.py` voll, `cp1252` | 🟢 **alle 238 Einheiten bestanden**, 286,0 s Wanduhr |
| `probe-pruefungen.py` voll, `utf-8` | 🟢 **alle 238 Einheiten bestanden**, 285,3 s Wanduhr |
| Selbstprobe `F1`/`F2` | 🟢 vier Fälle auf sechs gebauten Kennungen |
