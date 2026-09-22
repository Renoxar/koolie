# Änderungsantrag `CR-2026-046`

| Feld | Inhalt |
|---|---|
| Titel | Die Erstinstallation überschreibt eine gleichnamige Datei des Projekts – ohne Warnung |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-12 |
| Betroffene Artefakte | `install.py` (`run`), `docs/ADOPTION_GUIDE.md` (Abschnitte 1 und 2), `tests/scripts/probe-pruefungen.py` (neue Sonde) |
| Ebene laut Entscheidungsbaum 6 | Kern – Installationswerkzeug |
| Art | Befund aus der Vorbereitung der ersten Inbetriebnahme (2026-09-12); **gemessen** |
| Dringlichkeit | **blockierend** – er trifft den allerersten Befehl, den ein aufnehmendes Projekt ausführt |

## 1. Anlass und Problem

`install.py` kopiert die Core-Bestandteile des gewählten Client Packs in das Projekt. Für jeden
Core-Pfad gilt: Existiert die Datei nicht, wird sie angelegt. Existiert sie und ist byte-gleich,
bleibt sie. **Existiert sie und weicht ab, wird sie überschrieben** – in `install` ebenso wie in
`update`. Ob die vorhandene Datei jemals vom Framework stammt, prüft niemand.

Für die Laufzeitschicht ist das richtig: `.claude/rules/00-framework-core.md` gehört dem Kern.
**Für die Wurzel-Anweisungsdatei ist es falsch**, denn ihr Name ist keine Erfindung des
Frameworks, sondern die Konvention des Clients – und deshalb belegt ein Projekt ihn oft schon.

### Gemessen

Trockenlauf gegen ein reales Projekt, das seit Monaten mit `claude-code` arbeitet und eine eigene
Anweisungsdatei von rund 34 Kilobyte führt, versioniert:

```text
Framework 0.28.0
Client:  claude-code
Modus:   install  (dry-run, es wird nichts geschrieben)

Angelegt (77): …
Core aktualisiert (1):
  CLAUDE.md

Zusammenfassung: 77 angelegt, 1 aktualisiert, 0 unveraendert, 0 Projektdateien behalten.
```

**Der erste Befehl des Übernahmeleitfadens hätte die Projektdatei ersetzt.** Ohne Rückfrage, ohne
Sicherung, und in der Zusammenfassung als „1 aktualisiert" ausgewiesen – ein Wort, das nach Pflege
klingt und hier Verlust bedeutet.

### Der Leitfaden sagt das Gegenteil

`docs/ADOPTION_GUIDE.md` Abschnitt 2, Schritt 3, wörtlich:

> Bestehende Projektdateien werden nie überschrieben.

Der Satz ist für die Saatdateien richtig – Berechtigungsdatei, Overlay – und für die
Wurzel-Anweisungsdatei falsch. **Das ist der wiederkehrende Befundtyp dieses Projekts**, diesmal
an der empfindlichsten Stelle: in dem Satz, auf den sich verlässt, wer das Framework zum ersten Mal
anfasst.

### Der zweite, größere Teil des Befunds

Selbst mit einem Abbruch bleibt die Frage offen, **was mit dem Inhalt geschieht**. Ein Projekt, das
bereits eine Anweisungsdatei führt, hat dort Projektwissen stehen – Architektur, Befehle,
Konventionen. Das Framework beansprucht dieselbe Datei für Ebene 1. Wohin der vorhandene Inhalt
gehört, steht **nirgends**: Weder Leitfaden noch Checkliste kennen den Fall.

Nach der Ebenenlehre gehört er in das Overlay (Ebene 4) und, soweit er Regeln enthält, in eine
`2N-overlay-*`-Regeldatei. Das ist ableitbar – aber ableiten muss es heute jeder selbst, im
ungünstigsten Moment.

## 2. Vorgeschlagene Änderung

1. **Die Erstinstallation überschreibt keine vorhandene Core-Datei.** Weicht eine vorhandene Datei
   ab, bricht `install` ab, nennt sie und den Weg. Für `--update` bleibt es beim Überschreiben –
   das ist sein Zweck, und das Pack ist dort bereits installiert.

2. **Der Abbruchtext nennt die Entscheidung, nicht nur den Fehler:** welche Datei betroffen ist,
   dass das Framework diesen Pfad beansprucht, dass der vorhandene Inhalt ins Overlay gehört, und
   dass `--update` der Weg ist, wenn die Datei aus einer früheren Installation stammt.

3. **Der Leitfaden bekommt den Fall.** Abschnitt 1 stellt richtig, für welche Dateien die Zusage
   gilt. Abschnitt 2 erhält einen Schritt „Vorhandene Anweisungsdatei übernehmen": Inhalt sichten,
   Projektwissen ins Overlay, Regeln in eine `2N-overlay-*`-Datei, danach installieren.

4. **Wirkungsnachweis nach D-23:** Eine Sonde legt eine fremde Datei unter dem Namen der
   Wurzel-Anweisungsdatei an und belegt, dass die Erstinstallation abbricht **und die Datei
   unverändert lässt**. Gegenprobe: Dieselbe Installation in ein leeres Verzeichnis läuft durch.

## 3. Was dieser Antrag nicht ändert

- **`--update` bleibt, wie es ist.** Wer aktualisiert, will die Core-Dateien auf dem Stand des
  Releases haben; genau dafür ist der Modus da.
- **Die Saatdateien bleiben unberührt.** Berechtigungsdatei und Overlay gehören nach der
  Erstinstallation dem Projekt und werden ohnehin nie überschrieben.
- **Es wird nichts zusammengeführt.** Das Skript sichtet keinen Inhalt und schlägt keine
  Übernahme vor – das ist Arbeit für Menschen, und der Leitfaden sagt künftig, wie sie geht.

## 4. Prüffragen

- [x] Richtige Ebene: Kern – `install.py` und der Übernahmeleitfaden.
- [x] Verschärfungsprinzip: Der Antrag verschärft; ein Lauf, der bisher stillschweigend
      überschrieb, bricht künftig ab.
- [x] Widerspruchsfreiheit: D-45 gelesen – dieselbe Bauart, dieselbe Antwort: abbrechen statt
      stillschweigend das Falsche tun.
- [x] Laufzeitfassungen: nicht betroffen.
- [x] Belegstatus: **gemessen** im Trockenlauf gegen ein reales Projekt.
- [ ] Test- und Validierungsbedarf: **neue Sonde nach D-23** samt Gegenprobe.
- [x] Overlays: nicht betroffen; der Migrationsweg führt Inhalt **in** ein Overlay.
- [ ] Dokumentation: CHANGELOG, `ADOPTION_GUIDE.md`, `10-project-adoption.md`.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Abbrechen oder nur warnen? | **Abbrechen.** Dieselbe Frage wie bei D-45, dieselbe Antwort: Eine Warnung in achtzig Zeilen Ausgabe übersieht man, und der Schaden ist hier nicht rückholbar, wenn die Datei nicht versioniert war | Ein Projekt, das die Installation wiederholt, bekommt einen Abbruch statt eines Durchlaufs. Der Text muss deshalb sagen, dass `--update` der richtige Modus ist |
| E2 | Woran wird „fremd" erkannt – an der Herkunft der Datei oder am Modus? | **Am Modus.** Bei der Erstinstallation ist jede abweichende Core-Datei fremd, denn das Framework hat dort noch nie geschrieben. Eine Herkunftserkennung über den Kopfkommentar wäre feiner – und würde bei `.example`- und JSON-Artefakten versagen, die keinen tragen | Wer nach einer abgebrochenen Erstinstallation erneut `install` ruft, wird abgewiesen, obwohl die Dateien aus dem eigenen Lauf stammen. Der Weg ist `--update`; der Abbruchtext nennt ihn |
| E3 | Gilt der Schutz für alle Core-Pfade oder nur für die Wurzel-Anweisungsdatei? | **Für alle.** Sie ist der wahrscheinliche Kollisionsfall, aber nicht der einzige: Auch die Laufzeit-README oder eine `.example`-Datei kann im Projekt schon existieren | Etwas mehr Reibung bei einer Erstinstallation in ein gewachsenes Projekt. Das ist der Punkt |
| E4 | Den Übernahmeweg für vorhandene Inhalte in den Leitfaden aufnehmen? | **Ja, als eigener Schritt.** Ohne ihn ist der Abbruch eine Sackgasse: Er sagt, was nicht geht, und nicht, was zu tun ist. Projektwissen ins Overlay, Regeln in eine `2N-overlay-*`-Datei | Der Leitfaden wird länger an einer Stelle, die kurz sein sollte. Dafür beantwortet er die erste Frage, die ein reales Projekt stellt |
| E5 | Wie wird die Wirkung nachgewiesen? | **Sonde mit doppelter Bedingung:** Der Lauf bricht ab **und** die fremde Datei ist hinterher unverändert. Die zweite ist die eigentliche – ein Abbruch nach dem Schreiben wäre wertlos | Die Sonde braucht eine Installation, kein Repositorium. Der Aufbau dafür steht seit 0.28.0 |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle fünf Fragen wie vorgelegt.** E1 abbrechen statt warnen; E2 unterschieden wird am Modus, nicht an der Herkunft der Datei; E3 der Schutz gilt für alle Core-Pfade; E4 der Übernahmeweg kommt als Schritt 3a in den Leitfaden; E5 Sonde mit doppelter Bedingung |
| Datum | 2026-09-12 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | **Der Abbruch muss vor dem ersten Schreibvorgang stehen**, nicht während der Schleife – ein Abbruch nach der Hälfte der Dateien wäre schlimmer als keiner. Nachgewiesen über die dritte Bedingung der Sonde: Nach dem Abbruch existiert die Laufzeitschicht **nicht**. **Der Abbruchtext muss den Weg nennen**, sonst ist er eine Sackgasse. **Der ungelöste Fall eines fremden Agenten-Frameworks ist im Leitfaden ausdrücklich als ungelöst auszuweisen** (K-31), nicht zu verschweigen |
| Umsetzung | umgesetzt mit `0.29.0` |
