# Testprotokoll FW-VN-01 (Wiederholungslauf) – Versionskette vollständig

| Feld | Inhalt |
|---|---|
| Test-ID | `FW-VN-01` |
| Framework-Version | 0.13.0 (`CR-2026-015`) |
| Datum | 2026-09-10 |
| Prüfmethode | review |
| Vorlauf | `2026-09-10-FW-VN-01.md` – neun Befunde, Ergebnisstatus `fehlgeschlagen` |
| Anlass | Wiederholung nach Behebung der Befunde V1 bis V9 |
| Referenzinstallation | Übungsrepository auf Stand 0.12.0 (`a4ff67d`), Kopie mit dem Validator aus 0.13.0 |
| Voraussetzung | PyYAML 6.0.3 installiert; der Validator meldet keine Einschränkungswarnung |

> Zur Dateibenennung: Die Regel des Ablageverzeichnisses (`JJJJ-MM-TT-<Test-ID>.md`) sieht
> keinen zweiten Lauf am selben Tag vor. Der Wiederholungslauf trägt deshalb den Zusatz
> `-wiederholung`; der Vorlauf bleibt unverändert stehen.

## Prüfgegenstand nach der Behebung

| Glied | Zustand vor 0.13.0 | Zustand jetzt |
|---|---|---|
| Framework-Version | kein Befund | unverändert kein Befund; `VERSION` 0.13.0, oberster Änderungsverzeichnisabschnitt `[0.13.0]`, `CR-2026-015` und D-25 vorhanden |
| Overlay-Version | drei Ablageorte, kein Abgleich (V1, V2) | Prüfung 13 vergleicht Steckbrief, Manifest und Laufzeitfassung miteinander und die Steckbriefangabe gegen `VERSION` |
| Skill-Versionen | 13 Skills seit 0.1.0 unverändert auf `0.1.0` (V3, V4); keine Formatprüfung (V6) | 13 Skills auf `0.1.1` mit Eintrag je Änderungsverlauf; Prüfung auf `MAJOR.MINOR.PATCH` und auf einen passenden Änderungsverlaufseintrag |
| Berechtigungsstand | kein Befund | unverändert |
| KI-Nutzungsvermerk | Vorlage anders benannt als das Kettenglied (V7), Client in einer Kernvorlage (V8), Kurzform ohne Versionsanker (V9) | 39 Nennungen in 29 Dateien umbenannt (Kern: 39 → 0); Überschrift und Ausfüllhinweis clientneutral; Kurzform nennt Framework- und Overlay-Version |
| Register | kein Befund im Prüfumfang | unverändert |

Zusätzlich außerhalb der Kette, aus derselben Ursache: 10 Checklisten und 13 Prompts auf
`0.1.1`, `11-framework-release.md` auf `0.2.0`; die Release-Checkliste verlangt die
Versionspflege künftig auch für Checklisten und Prompts.

`RELEASE_PROCESS.md` Abschnitt 1.2 nennt die kompatible Framework-Version jetzt nur noch für
Overlay und Client Pack – die beiden Artefakte, die vom Kern abweichen können (Entscheidung
E1). Die Zusage ist damit für alle genannten Klassen erfüllt statt für eine von fünf.

## Wirksamkeitsnachweis (D-23)

Dieselben fünf Sonden wie im Vorlauf, dieselbe Kopie der Referenzinstallation, jetzt mit dem
Validator aus 0.13.0. Ausgangs- und Schlusslauf `--strict-overlay`: 0 Fehler, 0 Warnungen.

| Sonde | Eingebrachter Defekt | Vorlauf | Jetzt |
|---|---|---|---|
| S1 | Steckbrief „Kompatible Framework-Version" `0.12.x` → `0.4.x` | unbemerkt | **gemeldet:** „Kompatible Framework-Version '0.4.x' passt nicht zu leitwerk-core/VERSION (0.12.0). Erwartet '0.12.x' oder '0.12.0' – nach einer Aktualisierung ist der Steckbrief nachzuziehen" |
| S2 | `overlay_version` im Manifest `0.12.0` → `0.9.0` | unbemerkt | **gemeldet:** „Overlay-Version widersprüchlich angegeben (OVERLAY.md: 0.12.0; 20-project-overlay.md: 0.12.0; overlay-manifest.yaml: 0.9.0)" |
| S3 | Laufzeitfassung `Overlay-Version` `0.12.0` → `0.3.0` | unbemerkt | **gemeldet:** dieselbe Meldung mit dem abweichenden Wert an der Laufzeitfassung |
| S4 | Skill-Version `0.1.0` → `0.9.9`, Änderungsverlauf bleibt `0.1.0` | unbemerkt | **gemeldet:** „Version 0.9.9 hat keinen Eintrag in CHANGELOG.md (08-skill-conventions.md Abschnitt 7)" |
| S5 | Skill-Version → `banane` | unbemerkt | **gemeldet:** „Version 'banane' ist kein Semantic Versioning (MAJOR.MINOR.PATCH)" |

Die Meldung zu S2 und S3 nennt **alle drei** Werte mit Fundstelle, nicht nur den abweichenden.
Das ist Absicht: Welcher der drei der richtige ist, entscheidet das Projekt, nicht die Prüfung.

Die drei Gegenproben des Vorlaufs wurden wiederholt und weiterhin jede gemeldet:
Metadatenzeile `Version` entfernt, Kopfschlüssel `overlay_version` entfernt, Overlay-Status auf
`inaktiv`. Keine der neuen Prüfungen hat eine bestehende verdrängt.

## Weitere Läufe

| Prüfung | Ergebnis |
|---|---|
| `validate-framework.py` gegen das Framework-Repository | 0 Fehler, 0 Warnungen |
| `validate-framework.py --strict-overlay` gegen die Referenzinstallation | 0 Fehler, 0 Warnungen |
| `FW-KO-04` (Querverweise, Prüfung 12) | 0 Fehler – die Umbenennung in 29 Dateien hat keinen Verweis gebrochen |
| `install.py --check` | „Core ist auf dem Stand des Releases" (60 Dateien unverändert) nach `--update` der Laufzeitschicht |
| Hauptdokument | baut für beide Client Packs: `devin-desktop` 9.309 Zeilen, `claude-code` 9.203 Zeilen |

## Bewertung

Alle neun Befunde sind behoben, und die fünf Sonden, die im Vorlauf unbemerkt blieben, werden
gemeldet. Die Kette hält damit nicht mehr nur durch Sorgfalt: Vier ihrer Angaben kann der
Validator gegeneinander prüfen, und die fünfte – der Nutzungsvermerk – nennt bei jeder
Kontrollstufe eine Version, die sich bewegt.

**Ergebnisstatus: weiterhin `fehlgeschlagen`, bis die Gegenzeichnung vorliegt.**

Die Prüfmethode `review` verlangt ein Dokumentenreview durch eine **zweite Rolle**. Die beiden
Auflösungen mit Ermessensspielraum sind entschieden – E1: Abschnitt 1.2 wird eingeschränkt;
E2: die Skill-Versionen werden angehoben –, die Abnahme des Reviews selbst steht aus. Eine
Selbstbestätigung der erstellenden Rolle ist kein Review; der Status wechselt nicht dadurch,
dass der Lauf grün ist.

## Bekannte Grenzen

- Die Versionsanhebung löst nach `08-skill-conventions.md` Abschnitt 7 die erneute Ausführung
  der Testfälle in `TESTS.md` je Skill aus. Sie sind sämtlich `sitzung` und hängen an AP2, also
  heute nicht ausführbar. Diese Pflicht bleibt offen und ist in der Roadmap vermerkt – sie war
  der ausdrücklich vorgelegte Preis der Entscheidung E2.
- Prüfung 13 vergleicht Versionsangaben miteinander. Ob eine Version **inhaltlich** die
  richtige ist – ob also eine Änderung MINOR statt PATCH verdient hätte –, prüft sie nicht und
  kann sie nicht; das bleibt Sache des Release-Reviews.
- Geprüft wurde weiterhin die Kette im Framework und in der Referenzinstallation, nicht an
  realen Merge Requests.

## Gegenzeichnung

Rollen statt Personen (`framework/runtime/rules/20-project-overlay.md`).

| Rolle | Datum | Ergebnis |
|---|---|---|
| Ersteller des Reviews (KI-gestützt, Sitzung) | 2026-09-10 | neun Befunde behoben; fünf Sonden gemeldet; Ergebnisstatus bleibt `fehlgeschlagen` bis zur Gegenzeichnung |
| Zweite Rolle: `<FRAMEWORK_OWNER>` | `<TBD: Datum>` | E1 entschieden: Abschnitt 1.2 auf Overlay und Client Pack einschränken. E2 entschieden: Skill-Versionen anheben. `<TBD: Review abgenommen / Einwände>` |
