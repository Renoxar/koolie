# Änderungsantrag `CR-2026-043`

| Feld | Inhalt |
|---|---|
| Titel | Der Inhaltsvalidator gibt gefundene sensible Werte im Klartext aus |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-12 |
| Betroffene Artefakte | `tests/scripts/validate-framework.py` (Prüfung 6 und der Mermaid-Fehlerpfad), `tests/scripts/hook-check-secrets.py` (Meldung ungültiger Zusatzmuster), `tests/scripts/probe-pruefungen.py` (neue Sonden), `tests/TEST_CATALOG.md` (`FW-KO-01`) |
| Ebene laut Entscheidungsbaum 6 | Kern – Prüfwerkzeug |
| Art | Befund **B03** des unabhängigen Reviews vom 2026-09-12, P1; im Code gegengeprüft nach D-23 |
| Dringlichkeit | **vorrangig** – der Schaden entsteht bei jedem Lauf, nicht erst bei einer Änderung |

## 1. Anlass und Problem

Prüfung 6 des Validators sucht in allen Textdateien nach Secret-Mustern, E-Mail-Adressen,
IP-Adressen, internen Hostnamen, URLs außerhalb der Allowlist und projektspezifischen
Sperrbegriffen. Fünf dieser sechs Diagnosen nannten den **gefundenen Wert im Klartext**:

| Diagnose | Bisherige Ausgabe |
|---|---|
| E-Mail-Adresse | Pfad, dann „E-Mail-Adresse gefunden" **und der Wert in Klammern** |
| IP-Adresse | Pfad, dann „IP-Adresse gefunden" **und der Wert in Klammern** |
| interner Hostname | Pfad, dann „interner Hostname gefunden" **und der Wert in Klammern** |
| URL | Pfad, dann „URL außerhalb der Allowlist:" **und die vollständige URL samt Parametern** |
| Sperrbegriff | Pfad, dann „gesperrter Begriff" **und der Begriff in Anführungszeichen** |
| Secret-Muster | Pfad, dann „Secret-Muster" und die **Kategorie** – **macht es bereits richtig** |

**Damit trägt ein Schutzlauf genau die Angaben weiter, die er finden soll** – in ein Terminal, ein
Protokoll, eine Agentensitzung. Die Ausgabe des Validators ist kein geschlossener Raum: Sie steht
in Sitzungsmitschriften, in Prüfprotokollen unter `tests/protocols/` und im Kontext jedes Modells,
das den Lauf auslöst.

### Es ist die eigene Regel, die hier gebrochen wird

Der Befund ist kein Verstoß gegen eine fremde Anforderung. Er verstößt gegen **zwei eigene
normative Festlegungen**, die dieses Framework jeder Sitzung auferlegt:

- `framework/runtime/root-instruction.md`, Abschnitt 11: „Findest du vermutete Secrets oder
  personenbezogene Echtdaten: gib sie nicht aus, wiederhole sie nicht, **nenne nur die
  Fundstelle** und halte an."
- `tests/TEST_CATALOG.md`, `FW-DS-01`: Erwartet ist „nur Fundstelle; Inhalt nirgends
  wiedergegeben"; als unzulässiges Verhalten ist ausdrücklich **„Zitat, Weiterverarbeitung"**
  benannt.

Das Prüfwerkzeug hat getan, was es der Sitzung verbietet. **`FW-DS-01` prüft die Sitzung, nicht
das Werkzeug** – und sein Ergebnisstatus steht bis heute auf `offen`. Geprüft wurde also weder
das eine noch das andere.

### Am schärfsten beim Sperrbegriff

`project-overlay/forbidden-terms.txt` enthält reale Projekt-, Kunden- und Behördennamen. Prüfung 6
nimmt diese Datei deshalb **ausdrücklich von der eigenen Inhaltsprüfung aus** – und schrieb den
gefundenen Namen anschließend in die Fehlermeldung. Die eine Zeichenkette, die in keiner Ausgabe
des Frameworks stehen darf, stand dort durch die Prüfung, die sie verhindern soll.

### Der Befund hat sich selbst vorgeführt

Am 2026-09-12 lag das externe Review als unversioniertes Verzeichnis im Arbeitsbaum. Sein
Prüfprotokoll enthält den synthetischen Kontakt, mit dem das Review B03 nachgewiesen hat. Der
Validator meldete ihn – **und gab ihn dabei im Klartext aus**, also genau das, was B03 beanstandet.
Das Verzeichnis ist inzwischen ausgelagert; der Vorgang bleibt der stärkste Beleg des Antrags.

## 2. Vorgeschlagene Änderung

1. **Eine gemeinsame Fundstellenfunktion.** Sie liefert Pfad, Zeile und Spalte – **ohne den
   Treffer selbst**. Alle Diagnosen der Prüfung 6 laufen über sie.

2. **Neutrale Regel-IDs statt sprechender Werte.** Je Kategorie eine feste Kennung, die den Befund
   benennt, ohne ihn wiederzugeben: `FW-CONTENT-EMAIL`, `FW-CONTENT-IP`, `FW-CONTENT-HOST`,
   `FW-CONTENT-URL`, `FW-CONTENT-TERM`.

3. **Die Secret-Diagnose bekommt die Position**, die ihr fehlt. Sie nennt bereits nur die
   Kategorie – aber nur den Pfad, nicht die Stelle. Das Abnahmekriterium des Reviews verlangt,
   dass der Befund „über Pfad und Position auffindbar" bleibt.

4. **Fehlerpfade mit fremdem Inhalt schließen.** Zwei Stellen tragen Daten weiter, die niemand
   dorthin gelegt hat:
   - `validate-framework.py`: Der Mermaid-Fehlerpfad gibt 300 Zeichen der Fehlerausgabe des
     externen Renderers aus. Darin steht in aller Regel der **Quelltext des Diagrammblocks**.
   - `hook-check-secrets.py`: Ein ungültiges Zusatzmuster aus der Umgebungsvariablen für
     projektspezifische Pfadmuster wird mitsamt seinem Wert ausgegeben. Solche Muster tragen
     Projekt-, Kunden- und Hostnamen – dieselbe Datenart wie die Sperrbegriffe.

5. **Wirkungsnachweis nach D-23.** `probe-pruefungen.py` erhält je Kategorie eine Sonde mit einem
   **eindeutig synthetischen Marker**. Sie prüft beides: Der Befund **wird gemeldet**, und der
   Markerwert steht **weder in der Standardausgabe noch in der Fehlerausgabe**. Dazu die
   Gegenprobe: Der erlaubte Fall derselben Kategorie – eine Adresse aus dem
   Dokumentationsbereich – wird nicht gemeldet.

## 3. Was dieser Antrag nicht ändert

- **Keine Prüfung wird enger oder weiter.** Es ändert sich, was die Diagnose **sagt**, nicht,
  was sie **findet**. Kein Prüfergebnis kippt; die Zahl der Fehler und Warnungen bleibt gleich.
- **Die Altprotokolle werden nicht umgeschrieben.** `tests/protocols/2026-09-10-FW-KO-01.md`
  zitiert zweimal den alten Wortlaut. Ein Protokoll ist die Aufzeichnung eines Laufs, keine
  Beschreibung des Soll-Zustands – es hält fest, was damals ausgegeben wurde, und bleibt
  unverändert.
- **`FW-DS-01` bleibt offen.** Der Sitzungstest wird von diesem Antrag nicht eingelöst; er prüft
  das Verhalten des Modells, nicht das des Werkzeugs.
- **Die Sperrbegriffsliste bleibt, wo sie ist.** Dass eine Datei mit realen Namen im Arbeitsbaum
  liegt, ist eine eigene Frage und wird hier nicht berührt.

## 4. Prüffragen

- [x] Richtige Ebene: Kern – ein Prüfwerkzeug des Frameworks.
- [x] Verschärfungsprinzip: Der Antrag verschärft die Ausgabedisziplin; er lockert nichts.
- [x] Widerspruchsfreiheit: `root-instruction.md` Abschnitt 11, `02-privacy.md` Abschnitt 5 und
      `FW-DS-01` gelesen – der Antrag stellt die Übereinstimmung mit ihnen **her**.
- [x] Laufzeitfassungen: `hook-check-secrets.py` wird ausgeliefert und ist betroffen.
- [x] Belegstatus: **im Code bestätigt und unbeabsichtigt vorgeführt.**
- [ ] Test- und Validierungsbedarf: **neue Sonden nach D-23** – ohne sie gilt die Änderung als
      nicht vorhanden.
- [x] Overlays: nicht betroffen.
- [ ] Dokumentation: CHANGELOG; `FW-KO-01` erhält den Hinweis auf den neuen Sondenblock.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Welches Schema tragen die neutralen Regel-IDs? | **Sprechende Kennungen mit dem Präfix `FW-CONTENT-` und der Kategorie im Namen.** Die Ausgabe muss ohne Nachschlagewerk lesbar sein: Wer `FW-CONTENT-TERM` liest, weiß, was gefunden wurde, ohne die Datei zu öffnen | Ein **zweites** Kennungsschema neben dem Testkatalog, der `FW-XX-NN` verwendet. Zwei Schemata mit demselben Präfix sind eine Quelle von Verwechslungen – die Alternative `FW-IN-01` bis `-05` wäre einheitlich, aber in der Ausgabe stumm |
| E2 | Zeile allein oder Zeile **und Spalte**? | **Beides.** Zwei Treffer derselben Zeile bleiben sonst ununterscheidbar, und der zweite fällt als scheinbares Duplikat nicht auf | Die Fundstellenangabe wird länger und weicht vom Format ab, das die übrigen Prüfungen verwenden – dort steht Pfad und Zeile |
| E3 | Auch die Secret-Diagnose anfassen, obwohl sie den Wert nie ausgab? | **Ja – die Position ergänzen.** Sie ist die einzige Diagnose der Prüfung 6, die eine Datei nennt, aber nicht die Stelle. Das Abnahmekriterium verlangt Auffindbarkeit | Eine Änderung an der einen Stelle, die den Befund **nicht** hatte. Wer den Diff liest, muss den Grund kennen |
| E4 | Die beiden Fehlerpfade mitnehmen oder eigener Antrag? | **Mitnehmen.** Das Review verlangt ausdrücklich, „unbeabsichtigte Daten in Fehlerpfaden" zu berücksichtigen; ein eigener Antrag für zwei Zeilen ist Verwaltung ohne Ertrag | Beim Mermaid-Pfad geht **Diagnosekomfort** verloren: Die Fehlermeldung des Renderers sagt heute, *warum* ein Block ungültig ist. Künftig stehen dort Datei und Blocknummer, den Rest muss man von Hand reproduzieren |
| E5 | Wie wird die Wirkung nachgewiesen? | **Sonde je Kategorie mit doppelter Bedingung:** Befund gemeldet **und** Marker nicht in der Ausgabe. Die zweite Bedingung ist die eigentliche – die erste hätte die alte Fassung auch bestanden | Der Sondenblock wächst um sechs Fälle; `probe-pruefungen.py` führt je Fall einen vollständigen Validatorlauf auf einer Kopie aus und wird spürbar langsamer |
| E6 | Release als `0.26.1` (Patch)? | **Ja.** Kein Verhalten einer Prüfung ändert sich, nur ihr Wortlaut – das ist kein Minor | Die Fundstellenformate künftiger Protokolle weichen von denen der `0.26.0`-Protokolle ab, ohne dass die Versionsnummer eine Änderung erwarten lässt |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle sechs Ermessensfragen wie vorgelegt.** E1 sprechende Kennungen mit dem Präfix `FW-CONTENT-`; E2 Pfad, Zeile und Spalte; E3 die Secret-Diagnose bekommt die Position – und dabei dieselbe Kennungsform wie die übrigen Kategorien (`FW-CONTENT-SECRET`), damit die Ausgabe der Prüfung einheitlich bleibt; E4 die beiden Fehlerpfade werden mitgenommen; E5 Sonde je Kategorie mit doppelter Bedingung; E6 Release `0.26.1` |
| Datum | 2026-09-12 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | Der Sondenblock muss gegen die Fassung 0.26.0 **fehlschlagen** – eine Sonde, die gegen beide Fassungen besteht, misst nicht die Änderung, sondern nur sich selbst. **Nachgewiesen:** sieben Abweichungen gegen 0.26.0, keine gegen 0.26.1. Der Mermaid-Fehlerpfad bleibt **unbelegt**, solange der externe Renderer in der Umgebung fehlt; er ist als offener Nachweis auszuweisen, nicht als erledigter |
| Umsetzung | umgesetzt mit `0.26.1` |
