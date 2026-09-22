# Wirkungsnachweise zu Release 0.30.0

| Feld | Wert |
|---|---|
| Gegenstand | Die Umsetzungen zu `CR-2026-047` (D-47), `CR-2026-048` (D-48) und `CR-2026-049` (D-49) |
| Datum | 2026-09-12 |
| Framework-Version | 0.30.0 (gegen 0.29.0 = `92545fc`) |
| Prüfmethode | `python leitwerk-core/tests/scripts/probe-pruefungen.py <root>` gegen **beide** Stände, dazu vier Hook-Läufe je Stand |
| Umgebung | Windows 11, Python 3.14.4 |
| Ergebnis | **55 Sonden und Gegenproben bestehen gegen 0.30.0 in beiden Kodierungsumgebungen.** Die vier neuen Sonden fallen gegen 0.29.0 |

## 1. Was hier nachgewiesen wird – und was nicht

D-23 verlangt für eine neue Prüfung den Nachweis, dass sie eine bewusst gesetzte Sonde meldet.
Zwei der drei Umsetzungen dieses Release sind **Textkorrekturen** und stellen keine Prüfung auf;
für sie gibt es bewusst keine Sonde. Eine Prüfung, die eine berichtigte Formulierung bewacht,
wäre eine Prüfung auf Wortlaut – sie meldete jede Umformulierung und nichts sonst.

Nachgewiesen wird deshalb, was Verhalten hat:

| Gegenstand | Art | Nachweis |
|---|---|---|
| Suchwerkzeuge erreichen den Schutz-Hook (`CR-2026-047` E3) | Verhalten | zwei Sonden, zwei Gegenproben |
| Prüfung 26 – erklärte Werkzeugabwesenheit (`CR-2026-047` E3) | neue Prüfung | zwei Sonden, eine Gegenprobe |
| Kodierungsfestigkeit des Sondenlaufs (`CR-2026-049`) | Eigenschaft des Werkzeugs | derselbe Lauf in zwei Umgebungen |
| Reichweite je Zugriffskanal in den Matrizen (`CR-2026-047`) | Text | Protokoll vom selben Tag, keine Sonde |
| Umsetzungszeilen der fünf Betriebsmodi (`CR-2026-048`) | Text | dito |

## 2. Die vier neuen Sonden gegen beide Stände

Gefahren gegen einen frischen Auscheckstand von `92545fc` mit nachinstallierter Laufzeitschicht
(`install.py --client devin-desktop --root <stand>`; ohne sie meldet der Validator die
Pflichtpfade und der Lauf bricht vorher ab).

| Sonde | Gegenstand | 0.29.0 | 0.30.0 |
|---|---|---|---|
| 26 | Erklärte Abwesenheit **ohne Begründung** wird gemeldet | **FEHL** | OK |
| 26 | Erklärte Abwesenheit **im Widerspruch zu `permission_tools`** wird gemeldet | **FEHL** | OK |
| B04 | Suchwerkzeug auf einen Secret-Pfad wird blockiert | **FEHL** | OK |
| B04 | Suchmuster auf Schlüsseldateien wird blockiert | **FEHL** | OK |

**Vier von vier fallen gegen den Vorstand.** Das ist der Nachweis nach D-23: Die Prüfungen
existieren nicht nur, sie melden.

## 3. Die Gegenproben – und was sie gegen 0.29.0 wert sind

| Gegenprobe | Gegenstand | 0.29.0 | 0.30.0 |
|---|---|---|---|
| 26 | Die ausgelieferte Abwesenheitserklärung bleibt unbeanstandet | OK | OK |
| B04 | Suche in einem gewöhnlichen Pfad bleibt möglich | OK | OK |
| B04 | Suche im Kernverzeichnis bleibt möglich – lesen darf der Agent ihn | OK | OK |

> **Die beiden B04-Gegenproben bestehen gegen 0.29.0 aus dem falschen Grund.** Dort erreichte
> *keine* Suche den Hook, also passierte auch die erlaubte – die Gegenprobe prüfte nichts und
> zeigte es nicht. Erst gegen 0.30.0, wo der Kanal bewacht ist, sagt sie etwas: **dass die
> Bewachung nicht alles blockiert.** Genau dafür ist sie da, und ein Hook, der jede Suche
> blockiert, bestünde beide Sonden und machte das Suchwerkzeug unbenutzbar.
>
> Das ist dieselbe Bauart, die am 2026-09-12 schon zweimal aufgefallen ist (`CR-2026-042`,
> `CR-2026-049`): **Eine Gegenprobe ist nur so viel wert wie die Sonde daneben.**

## 4. Die Kodierungsfestigkeit – der Lauf in beiden Umgebungen

Die Abnahmeauflage aus D-49: Der Sondenlauf muss unabhängig davon bestehen, ob die aufrufende
Umgebung `PYTHONIOENCODING` setzt.

| Stand | ohne `PYTHONIOENCODING` | mit `PYTHONIOENCODING=utf-8` |
|---|---|---|
| 0.29.0 | alle bestanden | **1 Abweichung** (Sonde 19, `auÃŸerhalb` statt `außerhalb`) |
| 0.30.0 | **alle 55 bestanden** | **alle 55 bestanden** |

Die rote Zelle war genau die Konfiguration, die das Arbeitswissen dieses Projekts für
Unterprozesse empfiehlt. Seit 0.30.0 läuft jeder Unterprozessaufruf des Skripts über
`unterprozess()`, die Umgebung **und** Dekodierung festlegt; `subprocess.run` steht nur noch
dort.

## 5. Der Suchkanal am Hook – vier Läufe je Stand

Synthetische Werkzeugeingaben gegen `hook-check-secrets.py --fail-closed` des jeweiligen Standes.
Keine echten Geheimnisse, kein Dateisystemzugriff.

| Eingabe | 0.29.0 | 0.30.0 | gewollt |
|---|---|---|---|
| `Grep` auf `sonde/.env` | Exit 0 | **Exit 2** | blockiert |
| `Glob` auf `**/*.pem` | Exit 0 | **Exit 2** | blockiert |
| `Grep` auf `src/` | Exit 0 | Exit 0 | passiert |
| `Grep` auf `<kern>/framework/core/` | Exit 0 | Exit 0 | passiert – den Kern zu lesen ist erlaubt |

Die letzte Zeile ist die wichtigere Hälfte: Der Kern ist **schreib**geschützt, nicht
lesegeschützt. Eine Sperre, die auch das Lesen träfe, bräche den Betrieb des Frameworks – der
Validator, `install.py --check` und jedes `git diff` nennen Kernpfade.

## 6. Was dieses Release nicht nachweist

- **Keine vollständige Clientsitzung.** Gemessen ist der Hook. Dass der Client die Suche
  tatsächlich an ihn übergibt, folgt aus der Hook-Konfiguration, die die Abbildung erzeugt
  (Matcher `Read|Grep|Glob|Bash|Edit|Write|NotebookEdit`) – **belegt ist die Erzeugung, nicht
  das Auslösen.** Das bleibt offen und gehört in den nächsten AP2-Lauf.
- **Für Shell und Unterprozess ist nichts durchgesetzt worden.** Dieses Release berichtigt
  dort nur die Aussage. Die technische Durchsetzung braucht eine Isolationsschicht des
  Betriebssystems und ist unerhoben (`CR-2026-047` E5).
- **Die Modusgrenze von M4/M5 ist weiterhin nicht technisch durchgesetzt** und sagt das jetzt.
- **Prüfung 26 belegt nicht, dass ein Client ein Werkzeug wirklich nicht hat.** Sie belegt, dass
  die beiden Felder, die es behaupten, einander nicht widersprechen und dass jemand den Satz
  dazu verantwortet. Die Grenze steht im Kopfkommentar der Prüfung.

## 7. Gegenzeichnung

| Rolle | Datum | Ergebnis |
|---|---|---|
| Ersteller des Nachweises (KI-gestützt, Sitzung) | 2026-09-12 | 55 von 55 bestanden gegen 0.30.0 in beiden Umgebungen; vier neue Sonden fallen gegen 0.29.0 |
| `<FRAMEWORK_OWNER>` | `<TBD>` | `<TBD>` |
