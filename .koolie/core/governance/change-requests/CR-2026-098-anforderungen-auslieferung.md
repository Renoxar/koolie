# Änderungsantrag `CR-2026-098`

| Feld | Inhalt |
|---|---|
| Titel | Zwei Anforderungen an die Auslieferung – die Installationsbibliothek und das frameworkeigene Unterverzeichnis |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-19 |
| Betroffene Artefakte | `docs/ROADMAP.md` (neuer Posten `1.3.0`, Posten der Umbenennung erweitert), `governance/DECISION_LOG.md` (`K-50` erweitert, `K-75` neu), `CHANGELOG.md`, `VERSION` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand ist der Releaseplan |
| Art | Planänderung, keine Messung, kein Kontingent |
| Dringlichkeit | **Regulär, mit einer Frist:** Anforderung 2 gehört in die Umbenennung (`~0.68.0`) und wird danach teurer, nicht billiger |

## 1. Anlass

Der Mensch hat am 2026-09-19 zwei Anforderungen an die **Auslieferung** gestellt. Beide
betreffen nicht, was das Framework sagt, sondern **wie es in ein Zielprojekt kommt** –
und dafür gab es bisher genau einen Weg: das Repositorium kopieren und von dort
installieren.

## 2. Anforderung 1 – die Installationsbibliothek (neuer Posten `1.3.0`)

**Wortlaut sinngemäß:** Ein Zielprojekt soll das Framework nicht mehr nur als Kopie des
ganzen Repositoriums bekommen – mit Tests, Änderungsanträgen und Protokollen – und von
dort aus installieren. Der Weg soll **bleiben**; daneben soll es eine
**Installationsbibliothek** geben: Der Mensch nennt Projektpfad, Client und Overlay, und
der Installer legt an beziehungsweise hebt. Zusätzlich soll der **Lieferumfang wählbar**
sein: alles, oder nur das zur Nutzung Nötige.

**Warum das ein eigener Posten ist:** Drei Dinge des heutigen Aufbaus hängen daran, und
alle drei sind belegt, nicht vermutet.

| # | Was daran hängt | Beleg |
|---|---|---|
| 1 | **Der Kern liegt im Zielprojekt und wird von dort ausgeführt.** Die Hook-Kommandos der erzeugten Berechtigungsdatei zeigen auf `leitwerk-core/…` im Zielprojekt | Abschnitt 6 der Übergabe: ohne `cp -r leitwerk-core <root>/` zeigen sie ins Leere |
| 2 | **Das Heben ersetzt das Verzeichnis, nicht einzelne Dateien** (`rm -rf` + `git archive` + `--update`) | der Zehn-Minuten-Ablauf |
| 3 | **Mehrere Prüfungen laufen gegen den Kern im Zielprojekt** (45, 59) und `--strict-overlay` ist die Abnahme jeder Übernahme | `CR-2026-090`, D-171 |

**Wo der Posten hingehört: nach `1.2.0`.** Er ändert den **Übernahmeweg**, und der muß
gegen den dann geltenden Bestand gebaut werden – also nach der Umbenennung, nach `AP11`,
nach `1.0.0` und nach den beiden Erweiterungen, die **neue Träger mit Pfaden** anlegen
(Client Pack `openai-codex` in `1.1.0`, Overlay-Muster in `1.2.0`). Ein Mindestpaket, das
davor geschnitten wird, schneidet an einem Bestand, den es danach nicht mehr gibt.

## 3. Anforderung 2 – das frameworkeigene Unterverzeichnis (zur Umbenennung)

**Wortlaut sinngemäß:** `koolie-core/` und `project-overlay/` sollen im Zielprojekt nicht
im Wurzelverzeichnis liegen, sondern in einem frameworkspezifischen Unterverzeichnis,
vorgeschlagen `.koolie/`.

**Einzuordnen bei `~0.68.0`, nicht als eigener Posten.** D-127 verschiebt ohnehin
`leitwerk-core/` nach `koolie-core/` und ändert den Wert von `<CORE_DIR>`. Beides zweimal
zu tun hieße, jede Fundstelle zweimal anzufassen und jedes übernehmende Projekt zweimal
zu heben.

🔴 **Und es beantwortet `K-50` faktisch mit ja:** Ein Umzug ist kein Update. `install.py
--update` schreibt an den alten Ort; ohne einen Migrationspfad bleibt in jedem
übernehmenden Projekt der alte Baum stehen.

## 4. `K-75` – die offenen Entscheidungen

Sie gehören in den Antrag, der die Arbeit auslöst, nicht in den Plan:

| # | Frage |
|---|---|
| 1 | **Punkt oder kein Punkt?** Die Anforderung nennt beides. Ein Punkt-Verzeichnis ist voreingestellt unsichtbar – für eine **Regelablage, die ein Mensch lesen soll**, ist das eine Entscheidung, keine Schreibweise. Der Bestand kennt beides: `.claude/`, `.devin/` mit Punkt, `project-overlay/` ohne |
| 2 | **`core/` oder `koolie-core/` darunter?** `.koolie/koolie-core/` doppelt den Namen; `.koolie/core/` ist kürzer, aber ein herausgelöster Pfad `core/…` sagt nicht mehr, wem er gehört – und genau das war der Gegenstand der Clientneutralität (Prüfung 48) |
| 3 | **Was ist das Mindestpaket?** Eine Datei, die ein Skill **mit Pfad** zitiert, kann nicht weggelassen werden, ohne den Verweis ins Leere zeigen zu lassen – **D-193 an einer neuen Stelle** |
| 4 | **Womit prüft ein Projekt mit reduziertem Umfang seine Übernahme?** `validate-framework.py` liegt unter `tests/`, und `tests/` wäre das erste, was ein Mindestpaket wegläßt |
| 5 | **Woher weiß der Installer beim Heben, welche Dateien dem Projekt gehören**, wenn die Quelle nicht mehr im Zielprojekt liegt? |
| 6 | **Wo steht dann die Herkunftsangabe?** Heute in `leitwerk-core/VERSION` im Ziel; ohne sie kann weder Validator noch Mensch sagen, welcher Stand installiert ist |
| 7 | **Vertriebsweg:** Python-Paket, Git-Bezug oder Archiv? Eine Annahme über die vorhandene Werkzeugkette wäre eine Annahme (P3) |

## 5. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Ersetzt die Installationsbibliothek den heutigen Weg?** | **Nein – sie tritt daneben** | Zwei Wege sind zu pflegen und zu prüfen. **Der Gegenpreis wäre größer:** Der heutige Weg ist der einzige, der heute belegt funktioniert, und beide übernehmenden Projekte stehen auf ihm |
| **E2** | **Eigener Posten oder Teil von `1.2.0`?** | **Eigener Posten `1.3.0`, nach `1.2.0`** | Eine Nummer mehr. **Begründet, nicht bequem:** Der Posten ändert den Übernahmeweg, und `1.1.0` und `1.2.0` legen **neue Träger mit Pfaden** an – ein Mindestpaket, das davor geschnitten wird, schneidet an einem Bestand, den es danach nicht mehr gibt |
| **E3** | **Wird das Unterverzeichnis ein eigener Posten oder Teil der Umbenennung?** | **Teil der Umbenennung (`~0.68.0`)** | Der Umbenennungsposten wird größer. **Der Gegenpreis ist die doppelte Arbeit:** D-127 verschiebt das Kernverzeichnis ohnehin und ändert `<CORE_DIR>`; wer beides trennt, faßt jede Fundstelle zweimal an und hebt jedes übernehmende Projekt zweimal |
| **E4** | **Werden die sieben offenen Fragen hier entschieden?** | **Nein – `K-75`** | Ein Klärungspunkt mehr. **Der Grund ist die Trennlinie dieses Projekts:** Der Plan sagt, **was** und **wann**; die Ermessensfragen gehören einzeln vorgelegt, mit Auflösung **und Preis**, in den Antrag, der die Arbeit auslöst |
| **E5** | **Wird in diesem Release etwas gebaut?** | **Nein – Planänderung ohne Kontingent** | Ein Einschub mehr. **Kriterium 2 bewegt sich nicht**, und das ist richtig so: Eine Anforderung aufzuschreiben ist keine Messung |

## 6. Entscheidung

**E1 bis E5 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-19). Kein neuer
Decision Record – der Plan trägt die Festlegung, `K-75` die offenen Fragen.

## 7. Abnahme

- `validate-framework.py`: **0 Fehler, 0 Warnungen** gegen den fertigen Baum.
- `probe-pruefungen.py` in **beiden** Kodierungsumgebungen (D-49), voller Lauf.
- 🔴 **Prüfung 53 ist der Wirkungsnachweis dieses Antrags:** Sie rechnet die Kette der
  Releaseplan-Posten nach, und dieser Antrag fügt eine Nummer hinzu.
