# Änderungsantrag `CR-2026-025`

| Feld | Inhalt |
|---|---|
| Titel | Der Kern beschrieb bei den Betriebsmodi, was ein bestimmter Client kann |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | `framework/core/05-working-model.md`, `clients/devin-desktop/CLIENT_PACK.md` |
| Ebene laut Entscheidungsbaum 6 | Framework Core und Abbildungsschicht; keine Regeländerung |
| Art | Dritter und letzter Restpunkt aus `CR-2026-020` |
| Dringlichkeit | regulär |

## 1. Anlass und Problem

`CR-2026-020` hat die Akteursbezeichnung aus dem Kern gelöst und drei Restpunkte ausgewiesen.
Zwei sind mit `CR-2026-024` abgearbeitet. Der dritte ist der schwierigste, weil er **keine
Bezeichnungsfrage** ist.

Vier Betriebsmodi-Tabellen in `05-working-model.md` führten eine Zeile „Umsetzung beim
KI-Client". Ihr Inhalt:

| Modus | Genannt wurde |
|---|---|
| M1 Read-only Analysis | Plan-Modus („read-only research"), Subagent-Profil `subagent_explore` |
| M2 Guided Planning | Plan-Modus mit Plan-Datei unter `~/.devin/plans/plan-<session>.md` |
| M4 Test and Validation | Skill-`permissions`, Hook `PreToolUse` |
| M5 Documentation Support | Skill-`permissions` |

**M4 und M5 waren bereits neutral** – `permissions`, `PreToolUse` und die Schreibweise `Write(…)`
sind Kernbegriffe des Frameworks, keine Produktnamen. **M1 und M2 nicht:** Ein Modusname eines
Produkts, ein Profilname und ein Pfad im Home-Verzeichnis eines Clients.

Der Unterschied zur Akteursbezeichnung: Dort stand ein falscher Name für dieselbe Sache. Hier
sagte der Kern **eine Sache aus, die nur für einen Client gilt** – und die Abbildungsschicht
(D-12) ist genau der Ort, an dem so etwas hingehört.

Dass die Zeile nach `CR-2026-020` „Umsetzung beim KI-Client" hieß, machte es eher schlimmer: Der
Titel behauptete Neutralität, die der Inhalt nicht einlöste.

## 2. Vorgeschlagene Änderung

**Die Zeile heißt „Durchsetzung" und nennt, was durchzusetzen ist:**

- **M1:** Werkzeugbeschränkung des Skills auf lesende Verben und `deny: edit, exec` über dessen
  `permissions`. Kennt der KI-Client einen eigenen Nur-Lese-Modus oder ein rein lesendes
  Agentenprofil, ist dieser Weg vorzuziehen – welcher das ist, steht in der Fähigkeitsmatrix
  seines Client Packs (S3, A1).
- **M2:** Schreibrecht allein auf die Plan-Datei. Kennt der KI-Client einen eigenen
  Planungsmodus, ist dieser vorzuziehen. Liegt die Plan-Datei außerhalb des Repositorys, wird
  sie in das im Overlay festgelegte Ablageformat übernommen.
- **M4 und M5** bleiben inhaltlich unverändert; nur die Zeilenbezeichnung und die
  `[DOK]`-Marken entfallen – ein Belegstatus gehört an eine Produktaussage, nicht an eine
  Framework-Anordnung.

**Die drei clientgebundenen Angaben stehen jetzt im Pack `devin-desktop`:**

| Neu | Zusage | Mechanismus |
|---|---|---|
| A2 | Rein lesendes Analyseprofil für Modus M1 | Subagent-Profil `subagent_explore` |
| M4 | Eigener Planungsmodus für Modus M2 | Plan-Modus mit Plan-Datei unter `~/.devin/plans/…` |
| M5 | Eigener Nur-Lese-Modus für Modus M1 | Plan-Modus („read-only research") |

Die Belegspalte weist aus, dass die Aussagen aus dem Kern übernommen wurden – sie sind nicht neu
erhoben. **AP2 für `devin-desktop` steht weiterhin aus**; die Einstufungen sind damit so belastbar
wie zuvor, nur am richtigen Ort.

## 3. Was dieser Antrag nicht ändert

- **Keine Regel und keine Zusage.** Was ein Modus erlaubt und verbietet, steht unverändert in den
  Zeilen darüber.
- **Keine neue Prüfung.** Prüfung 12 meldet Pfadnennungen der Laufzeitschicht bereits als Warnung;
  `~/.devin/plans/` fiel nicht darunter, weil der Pfad im Home-Verzeichnis liegt und nicht unter
  den geprüften Wurzeln. Eine Erweiterung wäre möglich, ist aber nicht Gegenstand.

## 4. Nebenbefund – wieder eine zu kleine Zählung

Die Roadmap führte unter „Bewusst offen gelassen": „**Zwei** Pfadnennungen in AP2 dieses
Dokuments". Prüfung 12 meldet in einer `claude-code`-Installation **zehn**: zwei in der Roadmap,
acht in den Quellen des Hauptdokuments (`build/doc/15-referenzstruktur.md`,
`build/doc/31-anhaenge.md`).

Die acht sind **nicht geprüft** worden: `assemble.py` löst Laufzeit-Platzhalter je Client auf,
diese Stellen könnten also neutral sein. Ob sie es sein sollen, ist ein eigener Vorgang – die
Anhänge beschreiben teilweise Prüfpunkte gegen die Dokumentation eines konkreten Clients, wo der
Pfad richtig ist.

**Das ist die dritte zu kleine Zählung in Folge:** `CR-2026-020` (76 statt 248), `CR-2026-024`
(fünf statt zehn), hier (zwei statt zehn). Jedes Mal war die Zahl von Hand erhoben, jedes Mal an
der Stelle gezählt, wo man den Fehler vermutete. Die Roadmap-Notiz nennt jetzt die geprüfte Zahl
und ihre Aufschlüsselung.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Die Angaben löschen oder ins Pack übernehmen? | **Übernehmen.** Sie sind belegt und nützlich – nur am falschen Ort | Die Fähigkeitsmatrix wächst um drei Zeilen, die AP2 für `devin-desktop` noch bestätigen muss |
| E2 | Die `[DOK]`-Marken in der Kernzeile behalten? | **Nein.** Ein Belegstatus kennzeichnet eine Produktaussage; was das Framework anordnet, ist keine | Wer die Zeile bisher als Produktaussage gelesen hat, muss umlernen |
| E3 | Die acht Pfadnennungen in `build/doc/` mitlösen? | **Nein**, ausgewiesen. Die Anhänge beschreiben teils Prüfpunkte gegen die Dokumentation eines konkreten Clients | Die Warnung aus Prüfung 12 bleibt bei zehn statt bei zwei |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** |
| Datum | 2026-09-10 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | **E1 bis E3 wie in Abschnitt 5 vorgelegt**: Die drei clientgebundenen Angaben werden in das Pack `devin-desktop` übernommen (A2, M4, M5) statt gelöscht; die `[DOK]`-Marken der Kernzeilen entfallen; die Pfadnennungen in `build/doc/` werden **nicht** mitgelöst, sondern ausgewiesen. 🔴 **E3 ist die Wurzel einer Ausnahme, die danach zwanzig Releases lang als befristet geführt wurde:** Die Begründung – *„die Anhänge beschreiben teils Prüfpunkte gegen die Dokumentation eines konkreten Clients"* – beschreibt einen **dauerhaften** Gegenstand. Mit `AP11` (Release 0.89.0, D-311) ist die Frist gefallen und durch eine Dauerausnahme über drei benannte Träger ersetzt |
| Umsetzung | **mit Release 0.23.0** – Einzelheiten und Nachweise in `.koolie/core/CHANGELOG.md` |

Abschnitt 6 ist am 2026-09-22 mit `CR-2026-124` (`AP11`) **nachgetragen**, nicht neu entschieden: Die Entscheidung selbst steht seit 2026-09-10 in dem `CHANGELOG.md`-Eintrag zu Release 0.23.0, die Umsetzung im `CHANGELOG.md` zu Release 0.23.0. 🔴 **Der Releaseplan nannte für diesen Nachtrag zwei Anträge; gezählt am 2026-09-22 sind es sieben** – `CR-2026-020`, `-021`, `-023`, `-025`, `-026`, `-029` und `-030`.
