# Änderungsantrag `CR-2026-053`

| Feld | Inhalt |
|---|---|
| Titel | Der Schreibschutz der Regelquellen war als Leseverbot ausgeschrieben – und der Einstieg in das eigene Repositorium war nirgends geregelt |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-13 |
| Betroffene Artefakte | `templates/project-overlay/OVERLAY.md` (Abschnitt 4), `framework/runtime/rules/20-project-overlay.md`, `framework/runtime/root-instruction.md` (Abschnitte 3 und 6), fünf Skills (`fw-repo-analyze`, `fw-code-explain`, `fw-change-analyze`, `fw-error-analyze`, `fw-review-support`), `governance/FRAMEWORK_DEV_PROFILE.md` (neu), `README.md`, `tests/scripts/validate-framework.py` (Prüfung 28), `tests/scripts/probe-pruefungen.py`, `tests/EDGE_CASES.md` |
| Ebene laut Entscheidungsbaum 6 | **Core und Governance**; die Overlay-Vorlage ist Kern-Artefakt, das ausgefüllte Overlay bleibt Ebene 4 |
| Art | Befund **B07** des unabhängigen Reviews vom 2026-09-12, P2; **gegengeprüft, bestätigt und erheblich verschärft** |
| Dringlichkeit | **Paket 4**, gemeinsam mit `CR-2026-052`; B07 hing an der K3-Entscheidung |

## 1. Anlass und Problem

### 1.1 Der Befund ist schlimmer als beschrieben

Das Review nennt es eine Vermischung von Integritäts- und Vertraulichkeitsschutz: Die
Overlay-Vorlage führt unter „weder lesen noch ändern“ auch Regelablage, Wurzel-Anweisungsdatei,
Overlay und Framework auf – die der Agent laden **soll**.

**Die Gegenprüfung zeigt eine Wirkungskette, die der Bericht nicht nennt.** Beide technischen
Schichten trennen die beiden Schutzziele längst korrekt:

| Schicht | Vertraulichkeit | Integrität |
|---|---|---|
| `framework/runtime/permissions.json` | `read deny <EXCLUDED_PATHS>` und die Secret-Muster | `write deny <ROOT_INSTRUCTION_FILE>`, `<RUNTIME_DIR>/**`, `<CORE_DIR>/**`, `project-overlay/**` – bei `read allow **` |
| `tests/scripts/hook-check-secrets.py` | `SECRET_PATH_PATTERNS`: lesend **und** schreibend blockiert | `STRUKTURPFAD`-Liste: nur schreibend; `PROTECTED_WRITE_PATH_PATTERNS` für das Kernverzeichnis |

Die Trennung ist seit D-30 gebaut und im Skript kommentiert. Falsch ist allein der **Text** – und
zwar an einer Stelle, die in die Technik zurückwirkt: `<EXCLUDED_PATHS>` ist der Platzhalter, der
in die **`read`-Verweigerung** eingesetzt wird. Ein Projekt, das die Vorlage wörtlich ausfüllt,
erzeugt damit eine **Lesesperre auf seine eigenen Regeldateien** – auf genau die Anweisungen, die
der KI-Client befolgen soll. Das ist kein Dokumentenwiderspruch mehr, sondern ein Fehler, der die
erzeugte Berechtigungsdatei erreicht.

**Fundstellen, gegengeprüft:** `templates/project-overlay/OVERLAY.md:71` und
`framework/runtime/rules/20-project-overlay.md:23`. Die Wurzel-Anweisungsdatei macht es in
Abschnitt 3 (Lesen) und Abschnitt 6 (Ändern) **richtig** – sie bekommt die Lesesperre nur
zugeliefert. Der Befund sitzt also nicht dort, wo das Review ihn vermutet; die Zeilenangaben
`:37` und `:60` treffen einmal (37) und einmal nicht (die Verbotsliste steht auf 57).

**Nebenbefund, eigene Feststellung:** `<CORE_DIR>/**` steht in der Berechtigungsdatei als
`write`-Verweigerung, **aber nicht** in der Verbotsliste der Wurzel-Anweisungsdatei. Der
Mechanismus schützt mehr, als der Text sagt – der wiederkehrende Befundtyp dieses Projekts mit
umgekehrtem Vorzeichen. Ein Agent bekäme eine Blockierung, die ihm niemand angekündigt hat.

### 1.2 Der Einstieg in das eigene Repositorium war nirgends geregelt

Im Quellrepositorium bleibt das Overlay absichtlich Vorlage. Der Overlay-Status steht auf
`<TBD: aktiv | inaktiv>`, und die Wurzel-Anweisungsdatei sagt für diesen Fall: „arbeitest du nur
lesend“. Die fünf Analyseskills verlangten `<ALLOWED_PATHS>` oder erlaubten ohne Overlay
ausdrücklich nur Übungsrepositorys. Für die Entwicklung und Prüfung von Leitwerk **selbst** gab es
keinen benannten Weg – auch nicht für das Ablegen eines Ergebnisdokuments.

**Das ist nicht theoretisch, sondern die Arbeitsbedingung jeder Sitzung dieses Projekts** – die
dieser hier eingeschlossen. Das externe Review musste dafür den Auftrag als Berechtigung behandeln
und hat es ausgewiesen.

## 2. Vorgeschlagene Änderung

1. **`<EXCLUDED_PATHS>` wird zur reinen Vertraulichkeitskategorie.** In der Overlay-Vorlage und in
   der Laufzeitregel stehen dort nur noch die Secret-Dateien; die Strukturpfade des Frameworks
   wandern in `<READ_ONLY_PATHS>` – die Kategorie „Lesen erlaubt, Ändern nie“, die es bereits gibt
   und die die Skills als Lesebereich schon anerkennen. **Keine neue Kategorie, keine neue
   Semantik:** Damit sagt der Text dasselbe wie beide Mechanismen.
2. **Die Overlay-Vorlage erklärt den Unterschied an der Stelle, an der er gebraucht wird** – mit
   dem Satz, dass `<EXCLUDED_PATHS>` zu einer `read`- **und** `write`-Verweigerung wird und wer die
   Strukturpfade dort einträgt, den Lesezugriff auf die eigenen Regeln sperrt.
3. **Die Wurzel-Anweisungsdatei sagt beides ausdrücklich:** in Abschnitt 3, dass der Schreibschutz
   kein Leseverbot ist und die Regelquellen gelesen werden sollen; in Abschnitt 6 tritt
   `<CORE_DIR>/` in die Verbotsliste ein – der Text zieht dem Mechanismus nach.
4. **Ein Entwicklungsprofil für das Quellrepositorium** (`governance/FRAMEWORK_DEV_PROFILE.md`):
   zwei Einsatzkontexte, Geltungsbereich aus dem Inhalt des Repositoriums statt aus einem
   Verzeichnisnamen, Inhalt ist K0 und damit lesbar, Berichtspfad `tests/protocols/`, Änderungen
   nur über den Änderungsprozess (V10 bleibt), freigegebene Prüfkommandos – und ein Abschnitt
   „Was dieses Profil nicht leistet“.
5. **Die fünf Analyseskills** nennen neben dem Übungsrepositorium das Quellrepositorium des
   Frameworks. Fünf, nicht einer: Dieselbe Vorbedingung stand in allen fünf, und eine Ausnahme in
   einem Skill wäre die nächste Inkonsistenz.
6. **Prüfung 28** findet einen Strukturpfad in der Deklaration von `<EXCLUDED_PATHS>` – in der
   Vorlage, in der Laufzeitregel, im ausgefüllten Overlay und in der installierten Regelablage.
   Sie meldet zusätzlich, wenn die **Beschriftung** der Deklaration verloren geht, weil sie sonst
   leise bestünde.

## 3. Was dieser Antrag nicht ändert

- **Er hebt keinen Schreibschutz auf.** `<CORE_DIR>/**`, `<RUNTIME_DIR>/**`,
  `<ROOT_INSTRUCTION_FILE>` und `project-overlay/**` bleiben schreibgesperrt – auch im
  Quellrepositorium. Das Entwicklungsprofil ist ein Dokument, kein Schalter.
- **Er macht keine Projektdatei lesbar, die es nicht war.** Ausgeschlossen bleibt, was Abschnitt 2.1
  des Datenschutzmodells ausschließt. Eine Datei wird nicht dadurch lesbar, dass sie neben einer
  Regeldatei liegt.
- **Er löst B08 nicht.** Die Zirkularität der Aktivierung – `--strict-overlay` verlangt, was es
  herstellen soll – ist Paket 5 und bleibt offen.
- **Er beseitigt die Lücke im Shell-Kanal nicht.** Sie ist gemessen (B04), sie ist der Weg, über
  den Änderungen an diesem Framework heute entstehen, und sie steht als solche im Profil.

## 4. Prüffragen

- [x] Richtige Ebene: Kern-Artefakte und Governance. Das ausgefüllte Overlay bleibt Ebene 4; die
      Vorlage gehört dem Kern.
- [x] Verschärfungsprinzip: **verschärft zweimal, lockert einmal – und die Lockerung ist die
      Berichtigung einer falschen Zusage.** Verschärft: `<CORE_DIR>/` in der Verbotsliste, Prüfung
      28. Gelockert: Die Regelquellen sind lesbar – sie waren es technisch immer, nur der Text
      behauptete etwas anderes. **Eine Lesesperre, die kein Mechanismus erhebt und die ihren
      eigenen Regelträger sperrt, ist keine Schutzwirkung, die man verteidigt.**
- [x] Widerspruchsfreiheit: gelesen wurden D-22 (das gesamte Kernverzeichnis ist geschützt), D-30
      (zwei Schutzziele, zwei Listen), D-47 (Zusagen je Zugriffskanal), V10, `framework/core/02-privacy.md`
      Abschnitt 2 (K0-Definition), `framework/runtime/permissions.json`,
      `tests/scripts/hook-check-secrets.py`, die fünf Skill-Vorbedingungen.
- [x] Laufzeitfassungen: Wurzel-Anweisungsdatei und Regelablage `20-*` betroffen, beide erzeugt aus
      dem Kern. **Migrationshinweis nötig:** Ein bestehendes Projekt muss seine
      `<EXCLUDED_PATHS>`-Liste durchsehen – `--update` erneuert die Berechtigungsdatei nicht.
- [x] Belegstatus: **im Code und im Text gegengeprüft.** Die Trennung beider Mechanismen ist an
      `permissions.json` und am Hook-Skript nachgelesen, nicht abgeleitet.
- [x] Test- und Validierungsbedarf: **drei Sonden und eine Gegenprobe** für Prüfung 28. Die
      Gegenprobe ist die wichtigere: Beide Träger erklären im Fließtext, dass die Strukturpfade
      gerade **nicht** hierher gehören, und nennen dabei beides in einer Zeile.
- [x] Overlays: Jedes bestehende Overlay, das der Vorlage gefolgt ist, trägt den Fehler. Prüfung 28
      findet ihn beim nächsten Lauf.
- [ ] Dokumentation: `CHANGELOG.md` mit Migrationshinweis, Decision Log (D-55, D-56), Roadmap,
      `README.md`, Grenzfälle G-10 bis G-12.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Wohin gehören die Strukturpfade des Frameworks? | **In `<READ_ONLY_PATHS>`.** Die Kategorie existiert, heißt „Lesen erlaubt, Ändern nie“ und wird von den Skills bereits als zulässiger Lesebereich geführt. Beide Mechanismen machen genau diese Unterscheidung. Es gibt hier keine Ermessensfrage – nur einen Text, der seiner Technik nachzieht | `<READ_ONLY_PATHS>` trug bisher nur Projektwerte (Schnittstellenverträge, Migrationen) und bekommt feste Framework-Einträge. Und: Die Kategorie wird **nicht** in die Berechtigungsdatei abgebildet – der Schreibschutz dieser Pfade kommt weiterhin aus den festen `write`-deny-Regeln, nicht aus dem Overlay. Das ist ausgewiesen |
| E2 | Bekommt das Quellrepositorium eine technische Ausnahme? | **Nein. Ein Dokument, kein Schalter.** Das Profil benennt den Kontext, leitet die Lesefreigabe aus der Kontextklasse K0 ab und lässt die Schranke, wo sie ist: beim Änderungsprozess und bei der menschlichen Freigabe | **Die Selbstanwendung bleibt unvollständig, und zwar über eine gemessene Lücke:** Änderungen an diesem Framework entstehen über den Shell-Kanal, den der Hook nicht erfasst. Das steht im Profil, statt verschwiegen zu werden. Ein abschwächender Schalter wäre in jeder Installation ausgeliefert – genau die Bauform, aus der in diesem Projekt die Befunde entstehen |
| E3 | Was passiert, wenn Paket 6 den Shell-Weg schließt? | **Offen, als Klärungspunkt K-32 aufgenommen.** Dann braucht die Entwicklung dieses Frameworks einen ausdrücklich entschiedenen Weg – und die Entscheidung fällt dort, wo die Durchsetzung gebaut wird, nicht hier | Eine bewusste Schuld. Sie jetzt zu entscheiden hieße, einen Schalter für einen Mechanismus zu bauen, den es noch nicht gibt |
| E4 | Alle fünf Skills anfassen, obwohl der Befund einen nennt? | **Ja.** Dieselbe Vorbedingung steht wörtlich in fünf Skills. Vier davon stehenzulassen wäre dieselbe Inkonsistenz, nur kleiner – und das Abnahmekriterium des Reviews verlangt ausdrücklich, dass Skills dieselbe Einstufung tragen | Fünf Versionsanhebungen und fünf Einträge in den Skill-Änderungsverläufen; der Validator erzwingt beides |
| E5 | Wie verhindert Prüfung 28, dass sie den richtigen Text beanstandet? | **Sie prüft die Deklarationszeile, nicht jede Nennung** – erkannt an der Beschriftung „Ausgeschlossene Pfade“. Beide Träger erklären im Fließtext das Gegenteil und nennen dabei beides in einer Zeile; eine Prüfung, die jede Nennung meldet, wäre unbrauchbar. **Und weil eine verlorene Beschriftung eine Prüfung erzeugt, die leise besteht, ist deren Fehlen selbst ein Fehler** | Wer die Zeile umbenennt und die Beschriftung mit umschreibt, entgeht der Prüfung nicht – aber die Prüfung meldet dann einen fehlenden Anker statt der Sache. Das ist der bessere Fehlerfall: sichtbar statt still |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle fünf Fragen wie vorgelegt.** E1 Strukturpfade nach `<READ_ONLY_PATHS>`; E2 dokumentiertes Entwicklungsprofil ohne technische Ausnahme; E3 die Folgefrage wird als K-32 aufgenommen; E4 alle fünf Skills; E5 Prüfung 28 prüft die Deklaration und meldet den verlorenen Anker |
| Datum | 2026-09-13 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | D-55 (ein Schreibschutz ist kein Leseverbot), D-56 (Entwicklungsprofil des Quellrepositoriums) |
| Auflagen | **Das Profil muss die Lücke benennen, an der es hängt.** Ein Entwicklungsprofil, das die Selbstanwendung behauptet, ohne zu sagen, dass ihr wirksamer Teil auf einem gemessenen Loch im Shell-Kanal beruht, wäre derselbe Befundtyp eine Ebene höher. Der Abschnitt „Was dieses Profil nicht leistet“ ist deshalb Pflichtbestandteil, nicht Beigabe. **Der Migrationshinweis gehört in das `CHANGELOG.md`:** Ein bestehendes Projekt muss seine `<EXCLUDED_PATHS>`-Liste durchsehen, und `--update` erneuert die Berechtigungsdatei nicht. **Nachgewiesen:** drei Sonden, eine Gegenprobe, Gegenbeweis gegen 0.31.0 – dort meldet Prüfung 28 vier Fundstellen, zwei in der Quelle und zwei in der Installation. **Offen bleibt:** K-32, und die Abbildung von `<READ_ONLY_PATHS>` in die Berechtigungsdatei – die Kategorie ist heute rein textuell |
| Ziel-Release | `0.32.0` |
| Umsetzung | umgesetzt mit `0.32.0` |
