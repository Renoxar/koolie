# Wirkungsnachweise Release 0.37.0 – die drei Lücken aus 0.36.0

| Feld | Wert |
|---|---|
| Gegenstand | `CR-2026-059`, D-72 und D-73: Widerspruch zwischen Profil und Skill, Hintergrund-Unteragent, zweite Ebene – und die Zusage, dass ein Agentenprofil kein Startwerkzeug bekommt (Prüfung 35) |
| Datum | 2026-09-13 |
| Vorstand | `570f316` (0.36.0) |
| Grundlage der Zusagen | `tests/protocols/2026-09-13-erhebung-unteragent-tiefe.md`, sieben Läufe, Clientversion 2.1.270 |
| Ergebnis | **Validator 0 Fehler, 0 Warnungen. 123 Sonden und Gegenproben bestanden** (87 Sonden, 36 Gegenproben) – **in beiden Kodierungsumgebungen**. Gegen den Vorstand fällt **eine** Fundstelle, und sie kommt **nicht** aus Prüfung 35 |

## 1. Was neu geprüft wird

| Prüfung | Gegenstand | Sonden | Gegenprobe |
|---|---|---|---|
| **35 (neu)** | Kein Agentenprofil bekommt ein Startwerkzeug – weder über `agent_frontmatter.tool_names` noch direkt im Frontmatter (D-73) | 35a, 35b, 35c | die unveränderte Ablage bleibt unbeanstandet |
| **30 (Datenstand)** | D-72 braucht einen deckenden Grenzfall | G-19 | – |

## 2. Der Gegenbeweis gegen den Vorstand – und wo er schweigt

Der Vorstand wurde frisch ausgecheckt (`git archive 570f316`), **mit seinem eigenen
`install.py`** installiert, und bekam erst danach den neuen Validator. Sein eigener Validator
meldet 0 Fehler; der neue meldet **eine** Fundstelle:

| Prüfung | Fundstelle | Was sie sagt |
|---|---|---|
| 30 | `tests/EDGE_CASES.md` | keine Grenzfallzeile verweist auf D-72 |

**Das ist der ganze Gegenbeweis, und das ist keine Nachlässigkeit, sondern die Sache selbst.**

### Prüfung 35 findet gegen den Vorstand nichts – vorhergesagt, und so gewollt

`CR-2026-059` E1 hat es vor dem Bauen so aufgeschrieben: **Die Prüfung fängt heute nichts.**
`agent_frontmatter.tool_names` kennt gar kein Startwerkzeug, also kann keine erzeugte
`tools`-Liste eines enthalten. Sie ist eine **Verankerung**, keine Behebung – dieselbe Bauart
wie der fünfte Gegenstand der Prüfung 32 mit 0.36.0.

> **Was sie wert ist, hängt allein an ihren Sonden.** Ein Gegenbeweis gegen den Vorstand kann
> sie nicht erbringen: Dort gibt es den Fall nicht. **Sonde 35a stellt ihn her** – sie lehrt die
> Abbildung ein Startwerkzeug, also genau den Handgriff, der die Zusage aus D-73 lautlos fallen
> ließe. **Sonde 35b geht an der Abbildung vorbei** und schreibt es direkt ins Profil.
> **Sonde 35c** nimmt die Ablage weg und belegt, dass die Prüfung ihr Fehlen selbst meldet,
> statt leise zu bestehen.

**Wer die Zahl „eine Fundstelle" liest, muss beides wissen:** Sie ist richtig, und sie sagt über
Prüfung 35 nichts aus. Die Aussage über Prüfung 35 steht in den drei Sonden.

## 3. Was beim Bauen aufgefallen ist

### Ein Textanker, der auf den falschen Block gezeigt hätte

Die erste Fassung von Sonde 35a präparierte das Manifest über einen Textanker
(`"exec": [ "Bash" ]`). **Dieses Muster kommt zweimal vor** – `skill_frontmatter.tool_names`
und `agent_frontmatter.tool_names` sind zeichengleich –, und der erste Treffer ist der falsche:
Prüfung 35 liest nur den zweiten.

> **Die Sonde hätte präpariert, der Baum hätte sich geändert, und die Prüfung hätte trotzdem
> nichts gemeldet** – ein stiller Fehlschlag mitten in einer Sonde, die einen stillen Fehlschlag
> verhindern soll. Aufgefallen ist es beim Nachzählen der Treffer, nicht beim Lauf. Sie
> präpariert seither über das geparste JSON, und der Grund steht in ihrem Docstring.

### Die Gegenprobe 30 ist zum vierten Mal an der Grenzfallanzahl gebrochen

`18 → 19` musste zu `19 → 20` werden. **Das ist die vierte Änderung in Folge, die dieselbe
Stelle trifft** – mit 0.36.0 war es dieselbe Zeile, und dort kam die Kennungskollision dazu.
Die Frage, ob eine Gegenprobe ihre Summen **ableiten** soll, ist damit zum vierten Mal
aufgetreten und **weiterhin nicht entschieden**; sie gehört in einen eigenen Antrag.

### Zwei Patchskripte sind an Escapes gescheitert, eines mit Folgen

Beim Einfügen von Prüfung 35 hat ein mehrzeiliges Literal mit `\r\n` den Weg durch die Shell
nicht überlebt; die geschriebene Datei parste nicht mehr. **Der Rückweg war
`git checkout` auf die eine Datei** – deshalb ist es folgenlos geblieben. Seither werden solche
Blöcke als Zeilenliste geführt und die Escapes aus `chr(92)` zusammengesetzt, und beide
Patchskripte prüfen ihr Ergebnis mit `ast.parse()`, **bevor** sie schreiben.

## 4. Sondenlauf

**87 Sonden, 36 Gegenproben, alle bestanden – in beiden Kodierungsumgebungen** (mit und ohne
`PYTHONIOENCODING=utf-8`, Abnahmeauflage seit D-49). Neu sind **drei Sonden** (35a bis 35c) und
**eine Gegenprobe** (35).

| Sonde | Präparation | Was ohne sie durchginge |
|---|---|---|
| **35a** | `agent_frontmatter.tool_names` lernt ein Startwerkzeug | der Handgriff, der die Zusage aus D-73 **lautlos** fallen ließe |
| **35b** | das Profil `fw-reviewer` nennt ein Startwerkzeug selbst | derselbe Schaden an der Abbildung vorbei |
| **35c** | die Agentenablage des Kerns fehlt | die Prüfung bestünde leise – sie meldet das Fehlen jetzt selbst |

**Die Gegenprobe ist die wichtigere Hälfte:** Die unveränderte Ablage bleibt unbeanstandet.
Ohne sie stünde nur fest, dass die Prüfung irgendetwas meldet.

## 5. Was dieses Release nicht belegt

- **Drei Ebenen und tiefer.** Gemessen sind zwei; „mindestens zwei" ist wörtlich gemeint.
- **Der umgekehrte Widerspruch** – Profil sperrt über `disallowedTools`, Skill erlaubt. Nach
  dem Ergebnis von D-72 vorhersagbar, **aber eine Vorhersage ist keine Messung.**
- **Ob ein blockierender Hook auch auf der zweiten Ebene stoppt.** Für die erste Ebene ist es
  gemessen (D-69); der Rekorder sieht die Aufrufe der zweiten, ein entscheidender Hook ist dort
  nicht gefahren.
- **Prüfung 35 fängt heute nichts**, und der Gegenbeweis gegen den Vorstand kann das nicht
  ändern. Siehe Abschnitt 2.
- **Prüfung 35 prüft die Deklaration, nicht die Wirkung.** Dass ein genanntes Werkzeug beim
  Client wirklich startet, belegt allein eine Erhebung.
- **`devin-desktop` ist unerhoben**, und sein Manifest führt kein `agent_start_tools` – Prüfung
  35 überspringt es deshalb, und Prüfung 34 entscheidet, ob das zulässig ist.
- **Der Wortlaut des Clients ist zitiert, nicht gemessen.** „for this session" ist seine
  Aussage; gemessen ist der Turn (D-64).

## 6. Gegenzeichnung

| Rolle | Name/Kennung | Datum | Ergebnis bestätigt |
|---|---|---|---|
| `<FRAMEWORK_OWNER>` | `<TBD>` | `<TBD>` | `<TBD>` |
