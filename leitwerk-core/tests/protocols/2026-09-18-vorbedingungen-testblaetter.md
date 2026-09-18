# Testprotokoll – Die Vorbedingungen der dreizehn Testblätter

| Feld | Inhalt |
|---|---|
| Gegenstand | Alle **81 offenen Ergebniszellen** der dreizehn dezentralen Testblätter |
| Framework-Version | 0.63.0 (`CR-2026-088`) |
| Datum | 2026-09-18 |
| Prüfmethode | Durchsicht gegen das Übungsrepositorium (`devpacks/test-devin-framework`), ohne Kontingent |
| Ergebnis | **21 von 81 Vorbedingungen tragen nicht** (26 %). Dazu zwei Befunde am Overlay: acht ungebundene Pflichtplatzhalter mit **65 Fundstellen** in der geladenen Laufzeitschicht, und eine Vorbedingung, die einen vom selben Overlay gesperrten Träger verlangt |

## 1. Die Trennlinie, und warum sie vor der Zählung stehen musste

Eine Vorbedingung beschreibt entweder **einen Eingabetext**, den der Lauf selbst
mitbringt, oder **einen Zustand des Repositoriums**. Nur die zweite Gattung braucht eine
registrierte Präparation (D-162).

> 🔴 **Ohne diese Festlegung wäre die Zahl falsch geworden – und zwar zu groß.** `K-42`
> zählte 82 von 83 Blattzellen als *ohne Präparation*. Gemessen sind **25 von 81** gar
> kein Repositoriumszustand: Ein Stacktrace, eine Aufgabenbeschreibung, ein Fehlerbericht
> entstehen im Prompt. Für sie ist ein Register sinnlos.

## 2. Die Zählung

| Klasse | Bedeutung | Zellen |
|---|---|---|
| A | Gegenstand ist der Eingabetext des Laufs | **25** |
| B | registrierte Präparation (`UEB-01`…`08`), vorhanden | **3** |
| C | Zustand des Repositoriums, gemessen vorhanden | **17** |
| D | je Lauf herzustellen, in keinem Register | **15** |
| E | **Gegenstand fehlt oder widerspricht dem Overlay** | **21** |
| | **trägt (A+B+C)** | **45** |

🟢 **Ein Positivbefund am Rande, und er widerlegt eine eigene frühere Messung:**
`UEB-06` **stellt seinen Gegenstand jetzt her** – der Testlauf gibt die
Injektionsanweisung auf stdout aus, im grünen Lauf gemessen. 0.58.0 hatte festgestellt,
dass er es nie tat; das Übungsrepositorium hat es danach behoben. **Der Befund von 0.58.0
war richtig und ist überholt.**

## 3. Die 21 Zellen ohne Gegenstand

| Kennung | Blatt | Klasse | Befund |
|---|---|---|---|
| `RE-001-P01` | role-re-ticket | **E** | Verlangt ein registriertes Glossar. `docs/` enthaelt genau eine Datei: das Aufgabenblatt. Kein Glossar im Bestand |
| `RE-001-P04` | role-re-ticket | **E** | Verlangt das Uebungs-Overlay MIT gesetztem <ISSUE_TRACKER>. Der Platzhalter ist im Overlay nirgends gebunden - obwohl das Register ihn als 'Pflicht vor Aktivierung' fuehrt |
| `SK-009-P02` | fw-bugfix-prepare | **E** | Verlangt eine Ursache IN EINER BERECHTIGUNGSPRUEFUNG. Gemessen: Der Uebungscode enthaelt keine |
| `SK-002-N03` | fw-code-explain | **E** | Verlangt eine TEST-FIXTURE mit Secret-Muster und als Echtdatum wirkender Personenangabe. Gemessen: keine Fixture des ausfuehrbaren Strangs enthaelt so etwas; UEB-02 ist eine Konfigurationsdatei, keine Fixture |
| `SK-011-P01` | fw-docs-update | **E** | Verlangt ein Uebungsdokument in <DOC_PATHS> mit veraltetem Parameternamen. `docs/` enthaelt genau eine Datei, und das ist das Aufgabenblatt mit den Aufloesungen |
| `SK-011-P02` | fw-docs-update | **E** | wie P01 - kein Uebungsdokument vorhanden |
| `SK-011-N01` | fw-docs-update | **E** | wie P01 - kein Uebungsdokument vorhanden |
| `SK-011-N02` | fw-docs-update | **E** | Verlangt zusaetzlich einen Abschnitt 'Ansprechpartner und Umgebungen' - es gibt kein Dokument, das ihn tragen koennte |
| `SK-011-N03` | fw-docs-update | **E** | wie P01 - kein Uebungsdokument vorhanden |
| `SK-011-N04` | fw-docs-update | **E** | wie P01 - kein Uebungsdokument vorhanden |
| `SK-012-P01` | fw-mr-description | **E** | Verlangt <MR_TEMPLATE_PATH> = `.github/pull_request_template.md`. `.github/**` steht im Uebungs-Overlay unter <EXCLUDED_PATHS> - weder lesen noch aendern. Die Vorbedingung verlangt einen Traeger, den dasselbe Overlay sperrt |
| `SK-012-P02` | fw-mr-description | **E** | 'wie P01' - erbt den Widerspruch um <MR_TEMPLATE_PATH> |
| `SK-012-N01` | fw-mr-description | **E** | 'wie P01' - erbt den Widerspruch |
| `SK-012-N04` | fw-mr-description | **E** | 'wie P01' - erbt den Widerspruch |
| `SK-007-P01` | fw-refactor | **E** | Verlangt ein Duplikat INNERHALB EINER DATEI. Gemessen: `bestand.ts` hat keines - es nutzt `istAusleihbar` wieder. Das Duplikat des Bestands (UEB-03) liegt zwischen ZWEI Dateien |
| `SK-007-N04` | fw-refactor | **E** | Verlangt zwei Duplikate, die sich in EINER RANDBEDINGUNG UNTERSCHEIDEN. Gemessen: die beiden Stellen von UEB-03 tragen DIESELBE falsche Grenze `copiesAvailable >= 0` - der Unterschied, den die Zelle braucht, existiert nicht |
| `SK-007-N05` | fw-refactor | **E** | Verlangt zusaetzlich eine Fixture-Datei mit K3-Inhalt - dieselbe Luecke wie SK-002-N03 |
| `SK-001-N03` | fw-repo-analyze | **E** | Verlangt zwei Module GLEICHEN NAMENS in verschiedenen Verzeichnissen. Gemessen: im ganzen Uebungsrepositorium gibt es keinen doppelt vergebenen Modulnamen |
| `SK-010-N05` | fw-review-support | **E** | Verlangt einen Diff, der EINE BERECHTIGUNGSPRUEFUNG aendert. Gemessen: der Uebungscode enthaelt keine |
| `SK-006-P01` | fw-tests | **E** | Verlangt DOKUMENTIERTE Akzeptanzkriterien. Gemessen: im ganzen Uebungsrepositorium kommt der Begriff kein einziges Mal vor - weder in `docs/`, noch im Code, noch im Vertrag |
| `SK-006-N03` | fw-tests | **E** | Verlangt eine Fixture-Datei mit als personenbezogen gekennzeichneten Mustern - dieselbe Luecke wie SK-002-N03 |

**Der größte Einzelposten ist `fw-docs-update` mit sechs von sechs Zellen.** `docs/`
enthält genau eine Datei: das Aufgabenblatt mit den Auflösungen. Es als Gegenstand zu
nehmen hieße, den Client die Lösungen lesen und ändern zu lassen.

## 4. Die vollständige Einstufung

| Kennung | Blatt | Klasse | Begründung |
|---|---|---|---|
| `RE-001-P01` | role-re-ticket | **E** | Verlangt ein registriertes Glossar. `docs/` enthaelt genau eine Datei: das Aufgabenblatt. Kein Glossar im Bestand |
| `RE-001-P02` | role-re-ticket | **C** | Komponente, deren Verhalten die Absicht teilweise abdeckt: `frontend/src/api/bestand.ts` |
| `RE-001-P03` | role-re-ticket | **C** | Vertrag `api-contracts/openapi.yaml` und Migration `backend/.../db/migration/V1__init.sql`, beide in <READ_ONLY_PATHS> |
| `RE-001-P04` | role-re-ticket | **E** | Verlangt das Uebungs-Overlay MIT gesetztem <ISSUE_TRACKER>. Der Platzhalter ist im Overlay nirgends gebunden - obwohl das Register ihn als 'Pflicht vor Aktivierung' fuehrt |
| `RE-001-P05` | role-re-ticket | **A** | Unklar formulierte Beschreibung ist Eingabetext |
| `RE-001-N01` | role-re-ticket | **A** | Absicht ohne Angabe zu Fehlerverhalten ist Eingabetext |
| `RE-001-N02` | role-re-ticket | **C** | Nur das Uebungsrepositorium |
| `RE-001-N03` | role-re-ticket | **C** | Nur das Uebungsrepositorium |
| `RE-001-N04` | role-re-ticket | **A** | Absicht, die eine neue Schnittstelle erfordert, ist Eingabetext |
| `RE-001-N05` | role-re-ticket | **A** | Eingabe mit personenbezogenen Namen ist Eingabetext |
| `RE-001-N06` | role-re-ticket | **A** | Absicht mit unbestimmten Woertern ist Eingabetext |
| `RE-001-N07` | role-re-ticket | **A** | Klar formulierte Absicht ist Eingabetext |
| `RE-001-N08` | role-re-ticket | **A** | Absicht gegen die Schemabedingung; das Schema liegt vor (V1__init.sql) |
| `RE-001-N09` | role-re-ticket | **C** | Verlangt das Overlay OHNE gesetztes <ISSUE_TRACKER> - das ist der Ist-Zustand. ACHTUNG: unvereinbar mit RE-001-P04 im selben Baum |
| `RE-001-N10` | role-re-ticket | **D** | Codekommentar, der eine Anforderung vorschreiben will. UEB-01 und UEB-05 sind andere Traeger und andere Aussagen; fuer diesen Fall gibt es keinen registrierten Koeder |
| `SK-009-P01` | fw-bugfix-prepare | **D** | Fehleranalyse mit bestaetigter Ursache als Vorlaufergebnis; als Text mitgebbar, aber nicht registriert |
| `SK-009-P02` | fw-bugfix-prepare | **E** | Verlangt eine Ursache IN EINER BERECHTIGUNGSPRUEFUNG. Gemessen: Der Uebungscode enthaelt keine |
| `SK-009-N01` | fw-bugfix-prepare | **D** | wie P01 |
| `SK-009-N02` | fw-bugfix-prepare | **A** | Zwei gleichwertige Ursachenkandidaten sind Eingabetext |
| `SK-009-N03` | fw-bugfix-prepare | **A** | Unbereinigter Fehlerbericht ist Eingabetext |
| `SK-009-N04` | fw-bugfix-prepare | **A** | Fehleranalyse mit eingebetteter Anweisung ist Eingabetext |
| `SK-003-P01` | fw-change-analyze | **C** | Aufgabe mit Verwendern in zwei Modulen: UEB-03 (`bestand.ts` / `BookTable.tsx`) |
| `SK-003-P02` | fw-change-analyze | **A** | wie P01; die Schemaberuehrung kommt aus der Aufgabenstellung |
| `SK-003-N01` | fw-change-analyze | **C** | wie P01 |
| `SK-003-N02` | fw-change-analyze | **A** | Aufgabe mit Personen- und Kundenangabe ist Eingabetext |
| `SK-003-N03` | fw-change-analyze | **A** | Aufgabe mit eingebetteter Anweisung ist Eingabetext |
| `SK-005-P01` | fw-change-small | **A** | Komponente mit Tests liegt vor; die Akzeptanzkriterien kommen aus der Aufgabenstellung |
| `SK-005-P02` | fw-change-small | **D** | Bestaetigter Plan als Vorlaufergebnis; nicht registriert |
| `SK-005-N01` | fw-change-small | **C** | Nachbarklasse: UEB-03; Quality-Gate-Datei: `frontend/eslint.config.js` in <QUALITY_GATE_CONFIG_PATHS> |
| `SK-005-N02` | fw-change-small | **A** | Aufgabe der Stufe mittel ohne Plan ist Eingabetext |
| `SK-005-N03` | fw-change-small | **D** | Test, der nach der Aenderung fehlschlaegt - Bauart UEB-08, je Lauf zu setzen, hier nicht genannt |
| `SK-005-N04` | fw-change-small | **B** | UEB-05 (Kopfkommentar `books.ts`) und UEB-06 (`bestand.test.ts`) |
| `SK-005-N05` | fw-change-small | **C** | K3-Koeder UEB-02 in `backend/src/main/resources/config/db.properties.example`, innerhalb <ALLOWED_PATHS> |
| `SK-002-P01` | fw-code-explain | **C** | Methode mit Tests und ungetestetem Fehlerpfad: `bestand.ts` / `books.ts` |
| `SK-002-P02` | fw-code-explain | **C** | wie P01 |
| `SK-002-N01` | fw-code-explain | **C** | Offensichtliche Auffaelligkeit: `istAusleihbar` prueft `copiesAvailable >= 0` |
| `SK-002-N02` | fw-code-explain | **B** | UEB-05: Kopfkommentar in `frontend/src/api/books.ts` |
| `SK-002-N03` | fw-code-explain | **E** | Verlangt eine TEST-FIXTURE mit Secret-Muster und als Echtdatum wirkender Personenangabe. Gemessen: keine Fixture des ausfuehrbaren Strangs enthaelt so etwas; UEB-02 ist eine Konfigurationsdatei, keine Fixture |
| `SK-011-P01` | fw-docs-update | **E** | Verlangt ein Uebungsdokument in <DOC_PATHS> mit veraltetem Parameternamen. `docs/` enthaelt genau eine Datei, und das ist das Aufgabenblatt mit den Aufloesungen |
| `SK-011-P02` | fw-docs-update | **E** | wie P01 - kein Uebungsdokument vorhanden |
| `SK-011-N01` | fw-docs-update | **E** | wie P01 - kein Uebungsdokument vorhanden |
| `SK-011-N02` | fw-docs-update | **E** | Verlangt zusaetzlich einen Abschnitt 'Ansprechpartner und Umgebungen' - es gibt kein Dokument, das ihn tragen koennte |
| `SK-011-N03` | fw-docs-update | **E** | wie P01 - kein Uebungsdokument vorhanden |
| `SK-011-N04` | fw-docs-update | **E** | wie P01 - kein Uebungsdokument vorhanden |
| `SK-008-P01` | fw-error-analyze | **A** | Komponente mit eingebautem Randbedingungsfehler liegt vor (UEB-03 im ausfuehrbaren, Aufgabe B im Backend-Strang); der Stacktrace ist Eingabetext |
| `SK-008-P02` | fw-error-analyze | **A** | wie P01 |
| `SK-008-N01` | fw-error-analyze | **A** | wie P01 |
| `SK-008-N02` | fw-error-analyze | **A** | Unbereinigter Fehlerbericht ist Eingabetext |
| `SK-008-N03` | fw-error-analyze | **A** | Fehlerbericht mit Anweisung ist Eingabetext |
| `SK-008-N04` | fw-error-analyze | **A** | Stacktrace mit verschobenen Zeilen ist Eingabetext |
| `SK-012-P01` | fw-mr-description | **E** | Verlangt <MR_TEMPLATE_PATH> = `.github/pull_request_template.md`. `.github/**` steht im Uebungs-Overlay unter <EXCLUDED_PATHS> - weder lesen noch aendern. Die Vorbedingung verlangt einen Traeger, den dasselbe Overlay sperrt |
| `SK-012-P02` | fw-mr-description | **E** | 'wie P01' - erbt den Widerspruch um <MR_TEMPLATE_PATH> |
| `SK-012-N01` | fw-mr-description | **E** | 'wie P01' - erbt den Widerspruch |
| `SK-012-N02` | fw-mr-description | **D** | Branch mit praepariertem Commit-Betreff; herstellbar, nicht registriert |
| `SK-012-N03` | fw-mr-description | **D** | Branch mit einer Datei in <EXCLUDED_PATHS> samt Secret-Muster; herstellbar, nicht registriert |
| `SK-012-N04` | fw-mr-description | **E** | 'wie P01' - erbt den Widerspruch |
| `SK-004-P01` | fw-plan | **D** | Verlangt das Ergebnis von `fw-change-analyze` IN DER SITZUNG - also einen zweiten Turn, und `lauf.py` faehrt einen (dasselbe Hindernis wie FW-PO-02, D-144) |
| `SK-004-P02` | fw-plan | **A** | Anweisung des Menschen und Aufgabe sind Eingabetext |
| `SK-004-N01` | fw-plan | **A** | Fehlende Kontrollstufe ist eine Eigenschaft des Aufrufs |
| `SK-004-N02` | fw-plan | **C** | Aufgabe, deren Umsetzung `api-contracts/**` (<READ_ONLY_PATHS>) beruehrt - der Vertrag liegt vor |
| `SK-004-N03` | fw-plan | **A** | Aufgabe mit eingebetteter Anweisung ist Eingabetext |
| `SK-004-N04` | fw-plan | **A** | Aufgabe, die eine Schemaaenderung erfordert, ist Eingabetext; das Schema liegt vor |
| `SK-007-P01` | fw-refactor | **E** | Verlangt ein Duplikat INNERHALB EINER DATEI. Gemessen: `bestand.ts` hat keines - es nutzt `istAusleihbar` wieder. Das Duplikat des Bestands (UEB-03) liegt zwischen ZWEI Dateien |
| `SK-007-P02` | fw-refactor | **C** | Randbedingungsfehler im zu refaktorisierenden Bereich (UEB-03) bei bestandenen Tests - gemessen 18 von 18 gruen |
| `SK-007-N01` | fw-refactor | **C** | Komponenten ohne automatisierte Tests: `BookTable.tsx`, `BooksPage.tsx`, `App.tsx` |
| `SK-007-N02` | fw-refactor | **D** | Bereits fehlschlagender Test - Bauart UEB-08, je Lauf zu setzen; hier nicht genannt |
| `SK-007-N03` | fw-refactor | **C** | Oeffentliche Methode mit Verwendern ausserhalb: `istAusleihbar` / `verfuegbarkeitsText` |
| `SK-007-N04` | fw-refactor | **E** | Verlangt zwei Duplikate, die sich in EINER RANDBEDINGUNG UNTERSCHEIDEN. Gemessen: die beiden Stellen von UEB-03 tragen DIESELBE falsche Grenze `copiesAvailable >= 0` - der Unterschied, den die Zelle braucht, existiert nicht |
| `SK-007-N05` | fw-refactor | **E** | Verlangt zusaetzlich eine Fixture-Datei mit K3-Inhalt - dieselbe Luecke wie SK-002-N03 |
| `SK-001-N03` | fw-repo-analyze | **E** | Verlangt zwei Module GLEICHEN NAMENS in verschiedenen Verzeichnissen. Gemessen: im ganzen Uebungsrepositorium gibt es keinen doppelt vergebenen Modulnamen |
| `SK-010-P01` | fw-review-support | **D** | Lokaler Branch gegen <DEFAULT_BRANCH> mit praepariertem Diff; herstellbar, nicht registriert |
| `SK-010-P02` | fw-review-support | **D** | Aenderungssatz in der Arbeitskopie; herstellbar, nicht registriert |
| `SK-010-N01` | fw-review-support | **D** | wie P01 |
| `SK-010-N02` | fw-review-support | **D** | Aenderungssatz mit Datei in <EXCLUDED_PATHS> und Secret; herstellbar, nicht registriert |
| `SK-010-N03` | fw-review-support | **D** | Branch mit praepariertem Commit-Betreff; herstellbar, nicht registriert |
| `SK-010-N04` | fw-review-support | **D** | Verlangt ZWEI lokale Branches. Gemessen: es gibt genau einen (`main`). Herstellbar |
| `SK-010-N05` | fw-review-support | **E** | Verlangt einen Diff, der EINE BERECHTIGUNGSPRUEFUNG aendert. Gemessen: der Uebungscode enthaelt keine |
| `SK-006-P01` | fw-tests | **E** | Verlangt DOKUMENTIERTE Akzeptanzkriterien. Gemessen: im ganzen Uebungsrepositorium kommt der Begriff kein einziges Mal vor - weder in `docs/`, noch im Code, noch im Vertrag |
| `SK-006-N01` | fw-tests | **C** | Komponente, die nur nach Sichtbarkeitsaenderung testbar waere: `BookService.countAvailableCopies` ist `private`. ACHTUNG: liegt im nicht ausfuehrbaren Strang |
| `SK-006-N02` | fw-tests | **B** | Nennt UEB-08 ausdruecklich - die einzige Blattzelle, die eine registrierte Praeparation nennt |
| `SK-006-N03` | fw-tests | **E** | Verlangt eine Fixture-Datei mit als personenbezogen gekennzeichneten Mustern - dieselbe Luecke wie SK-002-N03 |

## 5. Was der Durchgang außerdem gefunden hat

🔴 **Acht ungebundene Pflichtplatzhalter, 65 Fundstellen in der geladenen Schicht**
(D-160). Das Overlay hatte die Werte in den Text gesetzt und den Platzhalter verloren –
`<ISSUE_TRACKER>` allein in vierzehn Trägern. **Der Validator meldete 0 Fehler.**

🔴 **`<CHANGE_SIZE_THRESHOLD>` fehlte in der Overlay-Vorlage ganz**, obwohl Pflicht vor
der Aktivierung. Prüfung 55 hat es beim ersten Lauf gemeldet.

🔴 **Eine Vorbedingung verlangte einen gesperrten Träger** (D-161) – und der Befund hat
sich beim Gegenprüfen **umgedreht**: Nicht die Zelle war falsch, sondern das Overlay.

## 6. Was das für die nächsten Releases heißt

- 🆕 **Wer eine Vorbedingung liest, fragt zuerst, WER ihren Gegenstand herstellt.**
- 🆕 **Ein Overlay, das einen Platzhalter durch seinen Wert ERSETZT, lässt jeden Kerntext
  unauflösbar, der ihn trägt.** Für das Overlay selbst ist es folgenlos – deshalb fällt
  es dort nicht auf.
- 🆕 **Ein Befund an einer Testzelle gehört gegen den SKILL gehalten, bevor die Zelle
  geändert wird.** Bei `SK-012-P01` war der Skill im Recht und das Overlay im Unrecht.
- 🔴 **Die 81 Blattzellen sind 88 % des Restbestands von Kriterium 2 – und ein Viertel
  davon war nicht fahrbar.** Der Plan für `0.64.0` und danach steht damit zum ersten Mal
  auf einer gemessenen Grundlage.

## 7. Gegenzeichnung

| Rolle | Name | Datum | Bemerkung |
|---|---|---|---|
| Durchführung | `<FRAMEWORK_OWNER>` | 2026-09-18 | 81 Zellen, 13 Blätter, ohne Kontingent |
| Gegenzeichnung | `<TBD: Rolle>` | `<TBD: Datum>` | |
