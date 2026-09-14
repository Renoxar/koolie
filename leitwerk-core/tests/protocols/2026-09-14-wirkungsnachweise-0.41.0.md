# Wirkungsnachweise Release 0.41.0 – der Skillaufruf ist ein Werkzeugaufruf

| Feld | Wert |
|---|---|
| Gegenstand | `CR-2026-063`, D-81 bis D-84: das Verb `skill` im Berechtigungsvokabular, zwölf wörtliche Freigaben, die Skillwahl an vier Trägern, der abgewiesene Aufruf als eigener Berichtsfall, Prüfung 39 – und Zeile S2 des Packs, die seit dem ersten Release keine Grenze nannte |
| Datum | 2026-09-14 |
| Vorstand | `00b534b` (0.40.0) |
| Grundlage der Zusagen | `tests/protocols/2026-09-14-gegenpruefung-skillwahl.md` und `-erhebung-skillaufruf.md`, elf Läufe mit vier Kontroll- und Entlastungsläufen |
| Ergebnis | **Validator 0 Fehler, 0 Warnungen. 162 Sonden, Gegenproben und Selbstproben bestanden** (112 Sonden, 43 Gegenproben, 7 Selbstproben) – **in beiden Kodierungsumgebungen, zeilengleich**, null Fehlschläge, Exit 0 |

## 1. Was neu geprüft wird

| Prüfung | Gegenstand | Sonden | Gegenproben |
|---|---|---|---|
| **39, Gegenstand 1** | Der verlorene Anker: ohne Skillverzeichnis und ohne eine einzige `skill`-Regel meldet die Prüfung ihr eigenes Fehlen | 39d | – |
| **39, Gegenstand 2** | Die Deckung in **beide** Richtungen: jeder ausgelieferte Skill hat genau eine Freigabe, jede Freigabe einen Skill (D-81) | 39a, 39b, 39f | 39a |
| **39, Gegenstand 3** | Kein Musterzeichen in einer Skill-Regel – es gäbe lautlos nichts frei (D-82) | 39c | **39b** |
| **39, Gegenstand 4** | Die Skillwahl an allen vier Regelträgern (D-84) | 39e | – |

**Die zweite Gegenprobe ist die wichtigere Hälfte.** Sie fügt eine **Pfadregel** mit
Muster hinzu (`search` auf `src/**`) – eine Regel, die ein Muster tragen **muss**. Eine
Musterprüfung ohne die Unterscheidung zwischen Namens- und Pfadargument hätte den
richtigen Text beanstandet; das ist derselbe Fall wie bei Prüfung 36, wo eine naive
Zählung zwei korrekt maskierte Striche gemeldet hätte.

**Sonde 39f ist die einzige, die einen künftigen Fall misst statt eines vergangenen.**
Sie legt einen dreizehnten Skill an, ohne die Freigabe nachzutragen. Das ist der Preis von
E3 – die Regeln stehen in der Datei, statt aus dem Verzeichnis erzeugt zu werden –, und
diese Sonde ist der Grund, warum der Preis vertretbar ist.

## 2. Der Wirkungsnachweis am Client

Auflage aus `CR-2026-063` Abschnitt 6. Eine **frische, vollständige Installation** aus dem
Arbeitsbaum, dieselbe Aufgabe wie Lauf A1, **Berechtigungsdatei unverändert** – kein
`settings.local.json`, kein Bypass, kein Eingriff nach der Installation.

| Feld | Vorstand 0.40.0 (Läufe A1, A3) | Arbeitsbaum 0.41.0 (Lauf W1) |
|---|---|---|
| `allow`-Regeln der erzeugten Datei | 6 | **18, davon 12 für den Skillaufruf** |
| Aufgerufener Skill | `fw-code-explain` | `fw-code-explain` |
| Ergebnis des Aufrufs | **abgewiesen** (`toolDenialKind: user-rejected`) | **läuft durch** |
| `permission_denials` | führt `Skill` | **leer** |
| `SKILL.md` ersatzweise gelesen | ja | **nein** |
| Stellung im Ablauf | dritter Werkzeugaufruf, nach zwei Suchen | **erster Werkzeugaufruf** |

**Das ist der Nachweis, auf den es ankommt:** derselbe Aufbau, dieselbe Aufgabe, ein
Unterschied – die zwölf Zeilen. Der Lauf liegt in
`devpacks/leitwerk-erhebungen-2026-09-14/laeufe/W1.json`.

## 3. Der Gegenbeweis gegen den Vorstand – zwei Zuschnitte

Der neue Validator gegen eine vollständige Installation von `00b534b`, installiert mit dem
`install.py` **des Vorstands**:

| Zuschnitt | Fundstellen der Prüfung 39 | Was er misst |
|---|---|---|
| **wie ausgeliefert** | **1** | Der Ankertest greift: keine einzige `skill`-Regel in der Kernquelle. Die drei übrigen Gegenstände kommen **gar nicht zum Zug** |
| **Ankertest neutralisiert** | **16** | Zwölf ausgelieferte Skills ohne Freigabe **und vier Regelträger ohne die Skillwahl** |
| **Kontrollprobe Arbeitsbaum 0.41.0** | **0** | Validator 0 Fehler, 0 Warnungen |

**Wer nur die zweite Zahl nennt, behauptet eine Messung, die der ausgelieferte Lauf nicht
macht** – dieselbe Auflage wie bei Prüfung 38 mit 0.40.0. Der ausgelieferte Lauf meldet
**eine** Fundstelle und hört dort auf; das ist richtig so, weil ein fehlender Anker jede
weitere Aussage wertlos machte.

> **Der erste Versuch von Zuschnitt 2 meldete 0 Fundstellen, und das war ein Absturz.**
> Die neutralisierte Kopie des Validators lag in einem Verzeichnis ohne ihr Nachbarmodul
> `overlay_status` und brach mit `ModuleNotFoundError` ab, bevor eine Prüfung lief.
> **Aufgefallen ist es nur, weil 0 nicht zur Erwartung passte.** Das Skript prüft seither
> auf eine Ergebniszeile und bricht ab, statt eine Null zu berichten – **derselbe Fall wie
> am 2026-09-13 gegen 0.32.0, und er ist ein zweites Mal eingetreten.**

## 4. Was der Sondenlauf gefangen hat

**Die Gegenprobe 30 ist gefallen, und sie hat sich selbst als gebrochen gemeldet:**

```text
GEGENPROBE 30   FEHL  Zusaetzlicher Grenzfall mit mitgezaehlter Anzahl  [Praeparation gebrochen]
        EDGE_CASES.md: Suchtext trifft 0x statt 1x: '| Anzahl der Grenzfälle | 19 |'
```

**Das ist der Fall, den die Übergabe seit vier Releases vorhersagt** – eine neue
Matrixzeile bricht die Sonden, die ihre Zahlen wörtlich verankern. Neu seit 0.38.0 ist,
dass der Bruch **eine Zeile Diagnose** kostet statt einer Fehlersuche: `ersetzt()` nennt
den Suchtext und die Trefferzahl, und die Gegenprobe erscheint nicht als scheinbarer
Befund im Repositorium. **Das ist die Wirkung von D-74, zum zweiten Mal gemessen.**

Nachgezogen sind beide Stellen: die Anzahl (`20 → 21`) und der Einfügeanker
(`| G-19 |` → `| G-20 |`). Die synthetische Kennung `G-99` bleibt frei – der Wächter
`frei()` hat das geprüft, und diesmal kollidiert sie nicht, anders als am 13.09. mit
`G-18`.

## 5. Was beim Bauen sonst aufgefallen ist

### 5.1 Die Argumentform war eine Messung wert, und sie ging anders aus als erwartet

Vor der Erhebung war die Erwartung, ein Präfixmuster `Skill(fw-*)` werde wirken – die
Berechtigungsschicht dieses Clients wertet für Befehle Präfixe aus und für Pfade Globs.
**Gemessen wirkt es nicht.** Hätte dieser Antrag die Erwartung übernommen, stünde jetzt
eine Regel in der ausgelieferten Datei, die richtig aussieht und **lautlos nichts
freigibt** – die Bauform von D-66, mit umgekehrtem Vorzeichen.

**Drei Läufe haben das entschieden**, und der wichtigste war der Kontrolllauf E1: Ohne ihn
wäre offen geblieben, ob das Argument überhaupt verglichen wird.

### 5.2 Der Entlastungslauf musste wiederholt werden

Der erste Kanarienvogel-Lauf griff zu `Grep` und fand die Merkwörter im Dateisystem.
**Damit war nichts belegt** – gemessen wäre das Suchwerkzeug gewesen, nicht der Kontext.
Der gültige Lauf fuhr mit abgeschalteten Werkzeugen; eine Antwort kann dann nur aus dem
geladenen Kontext kommen. **Verwandt mit der D-72-Lehre, aber nicht dieselbe:** Dort
wählte der Gegenstand einen anderen Weg, hier wählte er ein Werkzeug, das die Frage
beantwortete, ohne sie zu messen.

### 5.3 Die Zählung war wieder zu klein

Der externe Bericht behandelt die Skill-Bevorzugung als **eine** Regel. Es sind **fünf**
Träger – und der schwerste Befund steht an keinem davon, sondern in einer JSON-Datei. Wie
schon vier statt zwei, 25 statt 20, sechs statt zwölf.

### 5.4 Drei Protokolle wussten es und haben es nie gemeldet

`2026-09-12-B01-allowed-tools.md` nennt den Skillaufruf ausdrücklich „als eigenen
Werkzeugaufruf mit dem Namen `Skill` und damit einzeln kontrollierbar"; zwei Läufe des
13.09. sind verworfen worden, weil „der `Skill`-Aufruf scheiterte". **Dreimal
Eigenverschulden, kein einziges Mal ein Befund über die ausgelieferte Datei.** Das gehört
zum Befundtyp dieses Projekts – und es ist der erste Fall, in dem die Information
vollständig vorlag und nur nicht zusammengeführt wurde.

## 6. Sondenlauf

| Umgebung | Sonden | Gegenproben | Selbstproben | Fehlschläge | Exit |
|---|---|---|---|---|---|
| ohne `PYTHONIOENCODING` | 112 | 43 | 7 | **0** | 0 |
| mit `PYTHONIOENCODING=utf-8` | 112 | 43 | 7 | **0** | 0 |

**Zeilengleich.** Die neuen Einträge:

```text
SONDE      39a  OK    Ein ausgelieferter Skill ohne Freigabe - der Zustand vor 0.41.0
SONDE      39b  OK    Eine Freigabe fuer einen Skill, den es nicht gibt
SONDE      39c  OK    Ein Praefixmuster in der Freigabe - es gaebe lautlos nichts frei (D-82)
SONDE      39d  OK    Verlorener Anker - keine einzige skill-Regel mehr
SONDE      39e  OK    Ein Regeltraeger verliert die Skillwahl
SONDE      39f  OK    Ein neuer Skill, dessen Freigabe niemand nachtraegt
GEGENPROBE 39a  OK    Die unveraenderte Datei bleibt unbeanstandet - zwoelf Regeln, zwoelf Skills
GEGENPROBE 39b  OK    Eine PFADregel mit Muster bleibt unbeanstandet - Gegenstand 3 misst nur die skill-Regeln
```

## 7. Was dieses Release nicht belegt

- **Nicht, dass der Agent den Skill wählt.** Der verschärfte Text ist eine Anweisung; ob
  er die Wahl verbessert, ist ein Sitzungstest mit einer Stichprobe, die vier Läufe je
  Bedingung nicht hergeben. **Gemessen ist der Mechanismus, nicht das Verhalten.**
- **Nicht, dass Prüfung 39 heute etwas fängt.** Regeln, Skillmenge und Trägertexte sind
  mit diesem Release entstanden; der Gegenbeweis ist eine **Konstruktion**, kein
  Abzählen – die Lage von Prüfung 37.
- **Nicht, wie sich der Skillaufruf bei `devin-desktop` verhält** (**K-33**). Das Manifest
  deklariert die Enthaltung, statt sie offen zu lassen.
- **Nicht, dass die Regel zum abgewiesenen Aufruf durchgesetzt wird.** Kein Prüfwerkzeug
  liest einen Ergebnisbericht; was sie trägt, ist die Prüfpflicht des Menschen.
- **Nicht, dass ein Skill aus einer fremden Ablage harmlos wäre.** Er bleibt
  rückfragepflichtig – das ist die Absicht, nicht eine Lücke.
- **Nicht, dass die zwölf Freigaben in bestehenden Installationen ankommen.** Die Datei
  wird nach der Erstinstallation nie wieder geschrieben (D-76); dort meldet Prüfung 37
  zwölf fehlende Regeln, bis jemand sie nachträgt.

## 8. Gegenzeichnung

| Feld | Inhalt |
|---|---|
| Durchführung | KI-Client unter Aufsicht, Sitzung vom 2026-09-14 |
| Gegengezeichnet durch | `<APPROVAL_ROLE>` |
| Datum | `<TBD: Datum der Gegenzeichnung>` |
| Anmerkungen | `<TBD: Anmerkungen der gegenzeichnenden Rolle>` |
