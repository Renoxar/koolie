# Wirkungsnachweise zu Release 0.31.0

| Feld | Wert |
|---|---|
| Gegenstand | Die Umsetzungen zu `CR-2026-050` (D-50, Befund B01) und `CR-2026-051` (D-51, Befund B12) |
| Datum | 2026-09-12 |
| Framework-Version | 0.31.0 (gegen 0.30.0 = `ca815c2`) |
| Prüfmethode | `probe-pruefungen.py` gegen **beide** Stände und in **beiden** Kodierungsumgebungen; dazu das Rendern des Skill-Frontmatters für beide Packs |
| Umgebung | Windows 11, Python 3.14.4 |
| Ergebnis | **60 Sonden und Gegenproben bestehen gegen 0.31.0 in beiden Umgebungen.** Die drei neuen Sonden fallen gegen 0.30.0 |

## 1. Was hier nachgewiesen wird – und was nicht

`CR-2026-051` (B12) ist **reine Textkorrektur** und stellt keine Prüfung auf. Dafür gibt es
bewusst keine Sonde: Eine Prüfung, die eine Formulierung bewacht, meldet jede Umformulierung
und sonst nichts. Der Beleg dieses Antrags sind die drei Gegenprüfungen aus seinem Abschnitt 1 –
`git ls-files` für das `root-template/`, beide Manifeste für `<HOOKS_FILE>` und `shared_seed`,
beide für `hook_fail_closed`.

Nachgewiesen wird, was Verhalten hat:

| Gegenstand | Art | Nachweis |
|---|---|---|
| Prüfung 27 – verworfenes Zusagenfeld ohne Ersatz | neue Prüfung | zwei Sonden, eine Gegenprobe |
| Installationsabbruch bei fehlendem Ersatz | Verhalten | eine Sonde, eine Gegenprobe |
| S3 in beiden Packs, Modi-Zeilen, Quellenkarte | Text | Protokolle vom selben Tag, keine Sonde |

## 2. Die drei neuen Sonden gegen beide Stände

Gefahren gegen einen frischen Auscheckstand von `ca815c2` mit nachinstallierter Laufzeitschicht.

| Sonde | Gegenstand | 0.30.0 | 0.31.0 |
|---|---|---|---|
| 27 | Verworfenes Zusagenfeld **ohne benannten Ersatz** wird gemeldet | **FEHL** | OK |
| 27 | **Leerer** Ersatzsatz gilt nicht als benannter Ersatz | **FEHL** | OK |
| B01 | **Installation bricht ab**, wenn das Zusagenfeld ersatzlos entfiele | **FEHL** | OK |

**Drei von drei fallen gegen den Vorstand.** Das ist der Nachweis nach D-23.

Die zweite Sonde ist die unscheinbare und die wichtigere: Ein Begleitsatz aus drei Leerzeichen
ist keiner. Dieselbe Strenge trägt Prüfung 26 seit 0.30.0 – ohne sie wäre die Deklaration ein
Feld, das man ausfüllt, indem man die Leertaste drückt.

## 3. Die Gegenproben – und was sie gegen 0.30.0 wert sind

| Gegenprobe | Gegenstand | 0.30.0 | 0.31.0 |
|---|---|---|---|
| 27 | Der ausgelieferte Ersatzsatz bleibt unbeanstandet | OK | OK |
| B01 | Installation mit benanntem Ersatz läuft durch | OK | OK |

> **Beide bestehen gegen 0.30.0 aus dem falschen Grund** – dort gibt es weder die Prüfung noch
> den Abbruch, also kann nichts anschlagen. Erst gegen 0.31.0 sagen sie etwas: **dass die neue
> Strenge den Normalfall nicht bricht.** Ohne sie stünde nur fest, dass irgendetwas abbricht –
> und ein Installer, der immer abbricht, bestünde jede Sonde.
>
> Das ist dieselbe Bauart wie bei den B04-Gegenproben aus 0.30.0. Sie gehört ins Protokoll
> geschrieben, nicht weggelassen.

## 4. Das Rendern beider Packs – der eigentliche Gegenstand von B01

Gemessen am Quelltext von `fw-repo-analyze`, dem Analyseskill, auf den sich M1 beruft.

| Pack | Frontmatter nach dem Rendern | Bewertung |
|---|---|---|
| `claude-code` | `name`, `description`, `argument-hint`, `allowed-tools: Read, Grep, Glob` | **`permissions` fehlt** – das Feld mit `deny: [edit, exec]` erreicht die Installation nicht |
| `devin-desktop` | dieselben Felder **plus `permissions` und `triggers`** unverändert | Die Felder erreichen die Installation; ob der Client sie auswertet, ist unerhoben |

**Das ist der Befund in zwei Zeilen.** Bei `claude-code` fiel die Beschränkung doppelt aus:
`allowed-tools` beschränkt nicht (gemessen am 2026-09-12), und das Feld, das beschränkt hätte,
war weg.

> **Eine Fehlmessung auf dem Weg dorthin, und sie gehört hierher.** Der erste Versuch las die
> Quelldatei mit `newline=""` und damit mit CRLF. `render_skill_frontmatter()` prüft
> `text.startswith("---\n")` und gibt die Eingabe unverändert zurück, wenn das nicht zutrifft –
> die Messung zeigte ein **unverändertes** Frontmatter und sah aus wie ein Beleg dafür, dass
> nichts verworfen wird. **Gemerkt hat es nur, dass beide Packs dasselbe Ergebnis lieferten**,
> obwohl ihre Manifeste sich an genau dieser Stelle unterscheiden. Vierte Bauart des stillen
> Fehlschlags nach ERH-12, ERH-05 und B01 Lauf A: **eine Funktion, die bei unerwarteter Eingabe
> die Eingabe zurückgibt, statt zu melden.**

## 5. Der Lauf in beiden Kodierungsumgebungen

Die Abnahmeauflage aus D-49:

| Stand | ohne `PYTHONIOENCODING` | mit `PYTHONIOENCODING=utf-8` |
|---|---|---|
| 0.31.0 | **alle 60 bestanden** | **alle 60 bestanden** |

## 6. Was dieses Release nicht nachweist

- **`disallowed-tools` ist nicht erhoben.** Die Herstellerdokumentation nennt es als
  gesonderten Mechanismus für eine echte Werkzeugbeschränkung. Es wird deshalb **nicht**
  zugesagt und trägt in S3 einen VERIFY-Marker. Ob damit eine Beschränkung je Skill möglich
  wäre, ist offen – und es wäre der Weg, S3 zurückzugewinnen.
- **Die Wirkung der Skill-`permissions` bei `devin-desktop` ist unerhoben.** Belegt ist allein,
  dass die Felder die installierte Fassung erreichen. Die Zeile steht deshalb auf `[TEXTUELL]`
  und nicht auf `[TECHNISCH]`.
- **Prüfung 27 belegt nicht, dass der genannte Ersatz taugt.** Sie belegt, dass jemand die Frage
  beantwortet hat – dieselbe Grenze wie bei Prüfung 25, und sie steht im Kopfkommentar.
- **Kein Lauf in einer echten Clientsitzung.** Gemessen ist das Rendern und der Installer.

## 7. Gegenzeichnung

| Rolle | Datum | Ergebnis |
|---|---|---|
| Ersteller des Nachweises (KI-gestützt, Sitzung) | 2026-09-12 | 60 von 60 bestanden gegen 0.31.0 in beiden Umgebungen; drei neue Sonden fallen gegen 0.30.0; eine eigene Fehlmessung dokumentiert |
| `<FRAMEWORK_OWNER>` | `<TBD>` | `<TBD>` |
