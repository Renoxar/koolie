# Änderungsantrag `CR-2026-050`

| Feld | Inhalt |
|---|---|
| Titel | `allowed-tools` ist keine Werkzeugbeschränkung – und das Feld, das eine war, fiel beim Rendern weg |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-12 |
| Betroffene Artefakte | `clients/claude-code/CLIENT_PACK.md` (S3) und `manifest.json` (`skill_permissions_ersatz`), `clients/devin-desktop/CLIENT_PACK.md` (S3), `install.py` (`render_skill_frontmatter`, neue Prüfhilfe), `tests/scripts/validate-framework.py` (Prüfung 26a → 27), `tests/scripts/probe-pruefungen.py`, `framework/core/05-working-model.md` (M1, M4, M5), `clients/README.md` |
| Ebene laut Entscheidungsbaum 6 | Client Pack und Abbildung; der normative Kern wird nur nachgezogen |
| Art | Befund **B01** des unabhängigen Reviews vom 2026-09-12, P1; **gegengeprüft und gemessen** |
| Dringlichkeit | **mit Paket 3** – B01 war der einzige gemessene Befund des Pakets, der noch offen stand |

## 1. Anlass und Problem

Die Zeile **S3** beider Packs sagt eine „Werkzeugbeschränkung je Skill" zu, bei `claude-code`
eingestuft `[TECHNISCH]` mit Beleg `[DOK]`. **Beides ist widerlegt.**

### Gemessen, nicht nur gelesen

`tests/protocols/2026-09-12-B01-allowed-tools.md`: Ein Skill mit
`allowed-tools: Read, Grep, Glob` **konnte schreiben**. `allowed-tools` ist eine
**Vorabfreigabe** für den aufrufenden Turn, keine abschließende Werkzeugliste. Der
Dokumentationsbeleg `[DOK]` trug damit eine Aussage, die die Dokumentation so nicht macht.

### Das Feld, das die Beschränkung wirklich trug, fiel beim Rendern weg

Zwölf Quellskills tragen `permissions: {deny: [edit, exec]}` – darunter jeder Analyseskill, auf
den sich der Betriebsmodus M1 beruft. Das Manifest von `claude-code` führt `permissions` unter
`skill_frontmatter.drop_fields`; die installierte Fassung trägt nichts davon.

**Das ist nicht „still" im Wortsinn – und gerade das macht es interessant.** Das Verwerfen steht
im Manifest, für sich genommen korrekt: Der Client kennt das Feld für Skills nicht, und K-18
verlangt ein Frontmatter nur mit dokumentierten Feldern. Was fehlte, ist die **Folge**: dass
damit eine Zusage verschwindet und nirgends steht, was an ihre Stelle tritt.

**Genau dieses Muster hatte das Projekt schon einmal.** `triggers` verfiel auf dieselbe Weise,
bis `AP2-CC-01` es fand – und bekam daraufhin eine Abbildung (`model_invocation_field`).
`permissions` bekam keine. Zwei Felder, dasselbe Verfahren, ein Unterschied, den niemand
entschieden hat.

### Gegenprobe beim anderen Pack

Bei `devin-desktop` **überleben** beide Felder das Rendern (`drop_fields` ist dort leer,
Listenform). Das ist am Rendern nachgeprüft. **Ob der Client sie auswertet, ist es nicht** – die
Zeile trägt seit jeher einen VERIFY-Marker und war trotzdem `[TECHNISCH]` eingestuft.

## 2. Vorgeschlagene Änderung

1. **S3 bei `claude-code` auf `[NICHT ABBILDBAR]`**, mit benanntem Ersatz nach Prüfung 25: die
   **globale** Berechtigungsschicht samt Schutz-Hook. Sie wirkt unabhängig vom Skill und hielt
   am 2026-09-12 auch im untersagten Betriebsmodus – ist aber **weniger** als eine Beschränkung
   je Skill, und das gehört in dieselbe Zeile.
2. **S3 bei `devin-desktop` von `[TECHNISCH]` auf `[TEXTUELL]`.** Das Durchreichen der Felder ist
   belegt, ihre Wirkung nicht. Eine Erhebung an einer Installation steht aus.
3. **Ein zusagentragendes Frontmatter-Feld darf nicht ersatzlos entfallen.** `install.py` bricht
   ab, wenn ein Pack `permissions` oder `triggers` verwirft, ohne den Ersatz zu benennen –
   `skill_permissions_ersatz` beziehungsweise `model_invocation_field`.
4. **Prüfung 27** findet denselben Fehler **ohne** Installation, im Repositorium, wo ein neues
   Pack entsteht.
5. **Die Umsetzungszeilen von M1, M4 und M5** nennen künftig den Ersatz statt nur den Ausfall.
6. `clients/README.md` Schritt 6 nennt die neuen Manifestfelder.

## 3. Was dieser Antrag nicht ändert

- **Er beschafft keine Werkzeugbeschränkung je Skill.** Die Herstellerdokumentation nennt
  `disallowed-tools` als gesonderten Mechanismus – **nicht erhoben**, und deshalb hier nicht
  zugesagt. Er trägt einen VERIFY-Marker.
- **Er ändert die zwölf Quellskills nicht.** Das Feld `permissions` bleibt in der Quelle: Beim
  zweiten Pack erreicht es die Installation, und es ist die richtige Stelle, sobald ein Client
  es auswertet.
- **Er entscheidet nicht, ob M1 anders gebaut werden muss.** M1 stützt sich jetzt sichtbar auf
  die globale Schicht; ob das genügt, ist eine Frage an das Arbeitsmodell, nicht an dieses Pack.

## 4. Prüffragen

- [x] Richtige Ebene: Client Pack und gemeinsame Abbildung.
- [x] Verschärfungsprinzip: **verschärft dreifach** – der Abbruch, die Prüfung und die
      berichtigten Einstufungen. Gelockert wird nichts; eine Einstufung auf den gemessenen
      Stand zu senken, ist keine Lockerung des Schutzes, sondern das Ende einer Behauptung.
- [x] Widerspruchsfreiheit: D-18 (keine stille Lockerung in der Abbildung), D-26 (`AP2-CC-01`),
      D-41 (Kernzusage – S3 ist keine), D-47 (deklarierte Abwesenheit) gelesen. **Die Bauform
      ist dieselbe wie bei `hook_tools_absent`.**
- [x] Laufzeitfassungen: Die installierten Skills ändern sich nicht – das Feld entfiel vorher
      und entfällt weiterhin. Neu ist nur, dass der Ersatz benannt sein muss.
- [x] Belegstatus: **gemessen** (Protokoll vom 2026-09-12), dazu das Rendern beider Packs
      nachgeprüft.
- [x] Test- und Validierungsbedarf: **drei Sonden und zwei Gegenproben** – zwei für Prüfung 27,
      eine für den Installationsabbruch, je eine Gegenprobe dazu.
- [x] Overlays: nicht betroffen.
- [ ] Dokumentation: CHANGELOG, Decision Log, Roadmap, `clients/README.md`.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Welche Einstufung trägt S3 bei `claude-code`? | **`[NICHT ABBILDBAR]` mit benanntem Ersatz.** `[TEXTUELL]` wäre falsch: Es gibt keinen Regeltext, der eine Werkzeugbeschränkung je Skill aussprechen würde – es gibt sie schlicht nicht. Nach D-41 ist S3 eine **Fähigkeitszusage**; der Ausfall sperrt die Inbetriebnahme nicht | Die zweite Zeile auf `[NICHT ABBILDBAR]` in diesem Pack, nach S5. Das ist unangenehm zu lesen und zutreffend |
| E2 | Wie verhindert man den nächsten Fall? | **Absenz deklarieren, nicht erraten** – wie bei `hook_tools_absent` (D-47). Ein zusagentragendes Feld in `drop_fields` verlangt den benannten Ersatz, sonst bricht die Installation ab | Ein neues Manifestfeld und eine neue Prüfung. **Die Alternative wäre, `permissions` einfach nicht mehr zu verwerfen** – das erzeugte ein Frontmatter mit einem Feld, das der Client nicht kennt, gegen K-18, und änderte an der Wirkung nichts |
| E3 | Welche Felder gelten als zusagentragend? | **`permissions` und `triggers`** – die beiden, die im Frontmatter eine Schutzaussage machen. Die Liste steht an einer Stelle im Code und ist erweiterbar | Eine Liste, die jemand pflegen muss. Ohne sie müsste **jedes** verworfene Feld erklärt werden, auch `argument-hint` – das wäre Bürokratie ohne Schutzgewinn |
| E4 | S3 bei `devin-desktop` mit anfassen, obwohl der Befund den anderen Client nennt? | **Ja, auf `[TEXTUELL]`.** Dort ist gemessen, dass die Felder durchgereicht werden – nicht, dass sie wirken. Eine Zeile mit VERIFY-Marker auf `[TECHNISCH]` zu belassen, nachdem dieselbe Frage beim Nachbarpack die Zusage widerlegt hat, wäre genau die Zählung, die dieses Projekt sich abgewöhnt | Die Erhebung an einer Installation bleibt offen und ist in der Zeile ausgewiesen |
| E5 | Wie wird die Wirkung nachgewiesen? | **Zwei Schichten, zwei Sonden:** Prüfung 27 im Repositorium, der Abbruch bei der Installation. Dazu eine Gegenprobe je Schicht | Die Installationssonde braucht eine vollständige Kopie des Repositoriums und macht den Lauf länger. Sie ist die wichtigere – sie steht zwischen dem Befund und einer ausgelieferten Installation |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle fünf Fragen wie vorgelegt.** E1 S3 bei `claude-code` auf `[NICHT ABBILDBAR]` mit benanntem Ersatz; E2 die Absenz wird deklariert, sonst bricht die Installation ab; E3 zusagentragend sind `permissions` und `triggers`; E4 S3 bei `devin-desktop` auf `[TEXTUELL]`; E5 Nachweis auf beiden Schichten |
| Datum | 2026-09-12 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | **Der Ersatzsatz muss sagen, dass der Ersatz schwächer ist.** Die globale Berechtigungsschicht ist keine Beschränkung je Skill – ein Analyseskill kann schreiben, soweit die globalen Regeln es zulassen. Ein Ersatzsatz, der das verschweigt, wäre derselbe Befundtyp eine Ebene höher. **Nachgewiesen:** drei Sonden, zwei Gegenproben; die Installationssonde belegt den Abbruch, ihre Gegenprobe belegt, dass eine Installation mit benanntem Ersatz weiterhin durchläuft. **Offen bleibt:** `disallowed-tools` ist nicht erhoben und trägt einen VERIFY-Marker; die Wirkung der Skill-`permissions` bei `devin-desktop` ebenfalls |
| Umsetzung | umgesetzt mit `0.31.0` |
