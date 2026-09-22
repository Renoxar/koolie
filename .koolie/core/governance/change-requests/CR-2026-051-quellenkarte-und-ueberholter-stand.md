# Änderungsantrag `CR-2026-051`

| Feld | Inhalt |
|---|---|
| Titel | Die Quellenkarte führt an einen leeren Ordner, und das Hauptdokument beschreibt einen Stand von vor zwanzig Releases |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-12 |
| Betroffene Artefakte | `README.md` (Verzeichnisbaum, Abschnitt „Arbeiten an diesem Repository", Update-Tabelle), `docs/ADOPTION_GUIDE.md`, `clients/README.md` (Schritte 4 und 6), `build/doc/29-grenzen.md` |
| Ebene laut Entscheidungsbaum 6 | Kern – Dokumentation |
| Art | Befund **B12** des unabhängigen Reviews vom 2026-09-12, P3; **gegengeprüft** |
| Dringlichkeit | mit Paket 3 – der Befund kostet jeden neuen Mitwirkenden Zeit und ist billig zu beheben |

## 1. Anlass und Problem

Drei Aussagen beschreiben einen überholten Stand. **Alle drei sind nachgeprüft:**

### Die Quellenkarte führt an einen Ordner mit einer README darin

`README.md` nennt das `root-template/` des Client Packs als „Quelle der Wahrheit" für Änderungen
am Kern; `docs/ADOPTION_GUIDE.md` sagt, der Kern bringe die Bestandteile dort mit.

**Nachgezählt:** `git ls-files` findet unter `clients/*/root-template/` **genau zwei Dateien** –
je eine README der Laufzeitschicht. `seed_paths` ist in **beiden** Manifesten leer. Die
gemeinsamen Quellen liegen seit `CR-2026-010` unter `framework/runtime/`, `framework/skills/`
und `templates/`.

**Ein neuer Mitwirkender, der der README folgt, öffnet ein leeres Verzeichnis** und sucht dann
selbst. Das Abnahmekriterium des Reviews ist genau dieser Fall.

### Die Update-Tabelle verspricht eine Aktualisierung, die nicht stattfindet

`README.md` führt die Hook-Konfiguration unter „wird bei `--update` überschrieben".

**Nachgeprüft:** Bei **beiden** Packs zeigt `<HOOKS_FILE>` auf dieselbe Datei wie
`<PERMISSIONS_FILE>`, und diese steht unter `shared_seed` – sie wird **nur bei der
Erstinstallation** angelegt und bleibt danach unberührt. Das ist eine bewusste
Eigentumsentscheidung und richtig; die Tabelle sagt trotzdem das Gegenteil.

**Der Fall ist nicht theoretisch:** Release 0.30.0 hat die Suchwerkzeuge in die
Hook-Konfiguration aufgenommen. Ein Projekt, das der Tabelle glaubt, hält sie nach `--update`
für aktuell – und der Suchkanal bleibt unbewacht.

### Kapitel 29 beschreibt den Stand der Erstfassung als gegenwärtig

`build/doc/29-grenzen.md` sagt weiterhin, **kein** Mechanismus sei je in einer Zielinstallation
ausgeführt worden, der Schutz-Hook laufe **fail-open** und alle dynamischen Tests stünden auf
`offen`.

Der Abschnitt ist mit „Grenzen dieser Erstfassung" überschrieben – und wird unverändert in das
**aktuelle** Hauptdokument eingebettet. Wer das Dokument liest, liest es als Gegenwart.
Tatsächlich ist AP2 für beide Packs gefahren, und beide Manifeste führen
`hook_fail_closed: true` seit 0.24.0.

## 2. Vorgeschlagene Änderung

1. **Eine Tabelle „Wo eine Änderung hingehört"** in der `README.md` – je Artefaktart die Quelle.
   Das `root-template/` wird als das beschrieben, was es ist: die README der Laufzeitschicht.
2. **Die Update-Tabelle nennt die Hook-Konfiguration beim Projekt**, mit einem ausdrücklichen
   Hinweis, dass eine Hook-Änderung eines Releases **von Hand nachzutragen** ist – und dass der
   `CHANGELOG.md`-Eintrag solche Fälle unter „Migrationshinweise" führt.
3. **`ADOPTION_GUIDE.md` und `clients/README.md`** nennen dieselbe Quellenkarte; Schritt 4 der
   Pack-Erstellung sagt, dass das `root-template/` nur die README enthält.
4. **Kapitel 29 bekommt einen datierten Vorspann**, der es als Zeitdokument kennzeichnet und die
   drei überholten Aussagen ausdrücklich benennt, mit Verweis auf die aktuelle Quelle. Der
   Bestandstext bleibt unverändert – er ist die Erstfassung und soll es bleiben.

## 3. Was dieser Antrag nicht ändert

- **Er schafft `root-template/` nicht ab.** Die README dort ist Teil der Laufzeitschicht, die
  ein Projekt bekommt; und `install.py` erkennt ein Pack an diesem Verzeichnis.
- **Er ändert das Updateverhalten nicht.** Dass die Berechtigungsdatei dem Projekt gehört, ist
  richtig und bleibt. Berichtigt wird die Beschreibung, nicht das Verhalten.
- **Er schreibt Kapitel 29 nicht um.** Ein Zeitdokument, das man nachträglich glättet, ist keines
  mehr.
- **Er baut keine gemeinsame Statusquelle.** Das Review schlägt vor, veränderliche Statusangaben
  aus einer versionsgebundenen Quelle einzubetten. Das ist richtig und ein eigener Gegenstand –
  siehe E3.

## 4. Prüffragen

- [x] Richtige Ebene: Kern – Dokumentation.
- [x] Verschärfungsprinzip: keine Regel berührt.
- [x] Widerspruchsfreiheit: D-16, D-17, D-20 (`CR-2026-010`, die Saat kommt aus dem Kern), D-31
      (`hook_fail_closed`) gelesen; die Korrekturen ziehen nach, was dort entschieden ist.
- [x] Laufzeitfassungen: nicht betroffen.
- [x] Belegstatus: **nachgeprüft** – `git ls-files` für das `root-template/`, beide Manifeste für
      `<HOOKS_FILE>` und `shared_seed`, beide für `hook_fail_closed`.
- [x] Test- und Validierungsbedarf: **keiner.** Reine Textkorrektur; sie stellt keine Prüfung
      auf. Eine Prüfung auf Wortlaut wäre eine, die jede Umformulierung meldet.
- [x] Overlays: nicht betroffen.
- [ ] Dokumentation: CHANGELOG, Roadmap.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Quellenkarte als Tabelle oder als Fließtext? | **Als Tabelle.** Die Frage lautet „wo ändere ich X" und hat je X genau eine Antwort. Fließtext hat den Befund gerade erst erzeugt | Die `README.md` wird länger. Sie ist der Einstieg, und der Einstieg darf länger sein als der Rest |
| E2 | Kapitel 29 berichtigen oder kennzeichnen? | **Kennzeichnen, datiert, mit Nennung der überholten Aussagen.** Der Text ist die Erstfassung; ihn stillschweigend nachzuziehen nähme dem Dokument seine Zeitaussage – und niemand sähe, wie weit das Projekt gekommen ist | Ein Vorspann, den man lesen muss, bevor man den Abschnitt liest. Wer nur den Abschnitt liest, liest weiterhin Überholtes |
| E3 | Veränderliche Statusangaben aus einer gemeinsamen Quelle einbetten? | **Nein, nicht in diesem Antrag.** Das Review schlägt es vor und es ist richtig – aber es ist ein Bauvorhaben am Dokumentenbau, kein Redaktionsschritt. Ein Antrag, der einen Befund behebt und dabei ein Werkzeug erfindet, wird nicht fertig (dieselbe Begründung wie `CR-2026-044` E4) | Beim nächsten Release veraltet die nächste Statusangabe. Der Vorspann aus E2 nennt deshalb die **Quelle** des aktuellen Stands, statt ihn zu wiederholen |
| E4 | Den Migrationsfall „Hooks von Hand nachtragen" nur beschreiben oder prüfen? | **Nur beschreiben.** Eine Prüfung müsste die installierte Hook-Konfiguration mit der Kernquelle vergleichen – das ist der offene Gegenstand aus `CR-2026-044` E4 (Abgleich Quelle/Laufzeitfassung) und gehört dorthin | Ein Projekt, das den `CHANGELOG.md` nicht liest, merkt den Rückstand nicht. **Der Pilot ist der erste Fall** und steht auf 0.29.0 |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle vier Fragen wie vorgelegt.** E1 Quellenkarte als Tabelle; E2 Kapitel 29 wird datiert gekennzeichnet, nicht umgeschrieben; E3 die gemeinsame Statusquelle bleibt einem eigenen Gegenstand; E4 der Migrationsfall wird beschrieben, nicht geprüft |
| Datum | 2026-09-12 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | **Der Hinweis zur Hook-Konfiguration muss den konkreten Fall nennen, nicht nur die Regel.** 0.30.0 hat die Suchwerkzeuge aufgenommen; ein Projekt, das nur `--update` fährt, hat sie nicht. **Der Pilot ist der erste Betroffene** und steht auf 0.29.0. **Offen bleibt E3** – veränderliche Statusangaben stehen weiterhin an mehreren Stellen; und **E4** hängt am Abgleich zwischen Quell-Overlay und Laufzeitfassung (`CR-2026-044` E4), der seit 0.28.0 offen ist |
| Umsetzung | umgesetzt mit `0.31.0` |
