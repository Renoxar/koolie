# Änderungsantrag `CR-2026-052`

| Feld | Inhalt |
|---|---|
| Titel | Drei normative Regeln widersprechen sich – K3-Einstufung, Sicherheitskonfiguration, Parallelität |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-13 |
| Betroffene Artefakte | `framework/core/02-privacy.md`, `framework/core/09-risk-model.md`, `framework/core/05-working-model.md`, `framework/runtime/root-instruction.md`, `governance/PRIORITY_HIERARCHY.md`, `framework/org-policies/MAPPING_CLASSIFICATION.md`, `tests/EDGE_CASES.md` (neu), `tests/scripts/validate-framework.py` (Prüfungen 29, 30), `tests/scripts/probe-pruefungen.py` |
| Ebene laut Entscheidungsbaum 6 | **Core und Governance** – es sind Datenschutz-, Sicherheits- und Risikoregeln der Ebene 3 |
| Art | Befund **B09** des unabhängigen Reviews vom 2026-09-12, P2; **gegengeprüft, im Text bestätigt und in einem Punkt verschärft** |
| Dringlichkeit | **Paket 4** – das Review entscheidet diese Konflikte ausdrücklich nicht; ohne Entscheidung des `<FRAMEWORK_OWNER>` ist nichts umsetzbar |

## 1. Anlass und Problem

Drei Regelbereiche geben auf dieselbe Frage verschiedene Antworten. **Alle drei sind
gegengeprüft**, jede Fundstelle im Text nachgelesen
(`tests/protocols/2026-09-13-B07-B09-gegenpruefung.md`).

### 1.1 K3 – drei Texte, drei Antworten

| Stelle | Aussage |
|---|---|
| `framework/runtime/root-instruction.md:84` | „Immer K3: … interne Adressen und Umgebungskennungen“ – **ohne Bedingung** |
| `framework/core/02-privacy.md:33` | dieselbe Kategorie, **„sofern nicht im Overlay ausdrücklich als K1 eingestuft“** |
| `framework/core/02-privacy.md:42` | das Overlay darf lockern, wenn die Datenschutz- und Vertragsprüfung es erlaubt |
| `governance/PRIORITY_HIERARCHY.md:31` | „Delegationsverbote und K3 sind ebenenfest“ – **von keiner tieferen Ebene aufhebbar** |

**Die Zeilennummern des Reviews stimmen für die Wurzel-Anweisungsdatei nicht** (dort steht 83
statt 84 und 90 statt 91). Inhaltlich ist der Befund vollständig bestätigt.

**Die Gegenprüfung hat zwei eigene Feststellungen ergeben, die das Bild verschieben:**

1. **Es ist keine Pattsituation, sondern eine Minderheitsmeinung.** Acht weitere Stellen führen
   dieselbe Liste **ohne Bedingung**: die Laufzeitregel `framework/runtime/rules/10-privacy-security.md`,
   Entscheidungsbaum `decision-trees/01-context-allowed.md`, die Checkliste
   `checklists/02-privacy-context.md`, `onboarding/REFERENCE.md`, `onboarding/QUICKSTART.md`,
   `onboarding/KNOWLEDGE_CHECK.md` sowie `prompts/01-understand-codebase.md` und `prompts/10-documentation.md`. Die Bedingung steht an
   **einer** Stelle – und diese eine Stelle ist die kanonische Langform.
2. **Die Kurzform ist zwei Kategorien zu kurz.** Abschnitt 2.1 führt acht Kategorien; die
   Wurzel-Anweisungsdatei nannte sechs. Es fehlten **Sicherheitskonfigurationen mit
   Schutzwirkung** und **Inhalte anderer Projekte oder Mandanten** – und die Kurzform ist die
   Fassung, die in jede Sitzung lädt. Die Laufzeitregel `10-*` und die Checkliste führen alle
   acht; der Ausreißer ist die Kurzform. **Das hat das Review nicht gefunden.**

Ein zusätzlicher Träger kam dazu: `framework/org-policies/MAPPING_CLASSIFICATION.md:12` bot für
die Organisationsstufe „vertraulich“ eine Lockerung auf K2 an. Diese Stufe ist Kategorie 7 aus
Abschnitt 2.1 – die Lockerungszusage widersprach damit derselben Regel.

### 1.2 Sicherheitskonfiguration – Freigabe gegen Delegationsverbot

`framework/runtime/root-instruction.md:91` lässt die Umsetzung nach dokumentierter Freigabe zu.
**V6** (`framework/core/09-risk-model.md:64`) nennt „Änderungen an Produktionssystemen,
Infrastruktur, Berechtigungen, Sicherheitskonfigurationen“ **nicht delegierbar** und lässt nur
Analyse und Planvorschlag zu. Nach `governance/PRIORITY_HIERARCHY.md` Regel 2.4 ist die V-Liste
ebenenfest – die Wurzel-Anweisungsdatei kann sie nicht lockern.

**Eigene Feststellung:** Der Widerspruch ist nicht vollständig, sondern **teilweise**. Die
Kontrollstufentabelle desselben Moduls sieht Controlled Modification bei Kontrollstufe hoch
ausdrücklich vor – „nur nach dokumentierter Freigabe durch `<APPROVAL_ROLE>` und mit begleitender
Person“ –, und R3 und R10 stufen genau solche Änderungen dorthin ein. Das Framework **will** also,
dass Authentifizierungslogik im Code bearbeitbar ist. Was V6 meint, ist der Betrieb. Die beiden
Sätze reden über zwei verschiedene Gegenstände, und keiner sagt das.

### 1.3 Parallelität – die Schnittmenge ist leer

**R12** (`framework/core/09-risk-model.md:38`) stuft „Hintergrund-Subagenten, Parallelsitzungen
oder erweiterte Permission-Modi“ als **hoch** ein. Das Arbeitsmodell
(`framework/core/05-working-model.md:119`) erlaubt Parallelsitzungen „nur für voneinander
unabhängige Aufgaben der Kontrollstufe **niedrig**“.

**Eigene Feststellung, und sie ist die schärfste des Antrags:** Das ist nicht bloß uneinheitlich,
sondern **zirkulär**. Die Kontrollstufe ist der höchste Treffer über alle dreizehn Faktoren
(Abschnitt 5 desselben Moduls). Wer parallel arbeitet, trifft R12 hoch – die Aufgabe ist damit
Kontrollstufe hoch und kann nie „niedrig“ sein. **Die Regel des Arbeitsmodells war nie
erfüllbar.** Derselbe Befundtyp wie B08, wo die Aktivierung eine Prüfung verlangt, die bereits
Aktivität voraussetzt.

Der Vorschlag des Reviews – Parallelität nur im für Kontrollstufe hoch zulässigen Modus – löst den
Widerspruch **nicht**, weil er R12 unangetastet lässt: Schon ein rein lesender Subagent machte
damit jede Analyse zu einer Aufgabe der Kontrollstufe hoch, mit Architektur- und Security-Review
und vollständigem Sitzungsprotokoll. Das widerspricht Abschnitt 3.1 desselben Arbeitsmodells, der
ein rein lesendes Agentenprofil für M1 ausdrücklich erlaubt.

## 2. Vorgeschlagene Änderung

1. **Die acht Kategorien aus Abschnitt 2.1 sind unbedingt.** Die Bedingung an der sechsten
   Kategorie entfällt; Abschnitt 2.2 Regel 4 hält fest, dass keine Kategorie aus 2.1 auf irgendeinem
   Weg gelockert werden kann – nicht durch das Overlay, nicht durch die Datenschutz- und
   Vertragsprüfung, nicht durch den Ausnahmeprozess. Änderbar bleibt die Liste über den
   Änderungsprozess des Frameworks, also auf ihrer eigenen Ebene.
2. **Die Kurzform führt alle acht Kategorien** und nennt die bereinigte Ableitung als den Weg, der
   offen bleibt. Die Abbildung des Organisationsschemas verliert ihre Lockerungszusage.
   `governance/PRIORITY_HIERARCHY.md` bekommt die Fundstellen beider ebenenfester Listen und
   Befund 7 in der Widerspruchsprüfung.
3. **V6 erfasst den Betrieb, nicht die Anwendungslogik.** Ein normativer Abgrenzungsabschnitt hinter
   der V-Liste sagt, was auf welche Seite gehört, und nennt das Kriterium: Wirkt die Änderung über
   Build, Review und Quality Gates des Projekts, oder ist die geänderte Datei selbst die
   Berechtigung eines laufenden Systems? **Sicherheitskonfiguration als Code gehört zum Betrieb** –
   Infrastrukturbeschreibungen, Richtlinien- und Berechtigungsdateien, die Berechtigungsdatei
   dieses Frameworks. Die Wurzel-Anweisungsdatei trägt beide Sätze.
4. **R12 unterscheidet nach Schreibziel und Aufsicht, nicht nach der Zahl der Sitzungen:** rein
   lesende Parallelarbeit unter Aufsicht niedrig, schreibende auf disjunkten Zielen mittel,
   gemeinsame Schreibziele hoch. Erweiterte Permission-Modi bleiben hoch. Das Arbeitsmodell nennt
   statt einer Kontrollstufe die **Voraussetzungen** und verweist für die Einstufung auf R12.
5. **Zwölf Grenzfälle** in `tests/EDGE_CASES.md`, je mit Entscheidung, Betriebsmodus,
   Kontrollstufe, Rollen und Fundstelle – das Abnahmekriterium des Reviews, prüfbar gemacht.
6. **Prüfung 29** vergleicht die K3-Liste in fünf Fassungen und weist eine Bedingung zurück.
   **Prüfung 30** prüft die Grenzfalltabelle auf Vollständigkeit.

## 3. Was dieser Antrag nicht ändert

- **Er ändert das Schutzmodell nicht.** Die Kategorien bleiben, wie sie sind; entfernt wird eine
  Ausnahme, nicht eine Kategorie. Die Alternative – technische Metadaten aus der absoluten Liste
  ausgliedern – hätte das Modell geändert und eine Entscheidung des
  `<DATA_PROTECTION_CONTACT>` gebraucht.
- **Er erlaubt keine neue Umsetzung.** Die Abgrenzung zu V6 beschreibt, was nach der bestehenden
  Kontrollstufentabelle ohnehin gilt. Was heute nicht delegierbar ist, bleibt es.
- **Er belegt keine technische Durchsetzung.** Ob ein Client eine Einstufung erzwingt, steht in
  seiner Fähigkeitsmatrix. Die Grenzfälle nennen Einstufungen, keine Mechanismen.
- **Er prüft nicht, ob ein KI-Client die Grenzfälle richtig einstuft.** Das ist eine Sitzung, kein
  Skript – `FW-KO-05` im Testkatalog.

## 4. Prüffragen

- [x] Richtige Ebene: Core (Ebene 3) und Governance. Datenschutz- und Sicherheitsregeln stehen dort
      und nur dort (P10).
- [x] Verschärfungsprinzip: **verschärft dreifach.** Eine Ausnahme entfällt, zwei fehlende
      Kategorien kommen in die Kurzform, die Sicherheitsgrenze wird für den Betrieb absolut. Die
      R12-Neufassung ist **keine Lockerung**, sondern die Auflösung einer leeren Schnittmenge: Was
      vorher galt, war nicht erfüllbar. Erweiterte Permission-Modi bleiben hoch.
- [x] Widerspruchsfreiheit: gelesen wurden `governance/PRIORITY_HIERARCHY.md` (Regeln 2.1, 2.4),
      `framework/core/02-privacy.md`, `framework/core/09-risk-model.md` (R3, R10, R12, V4, V6, V10,
      Kontrollstufen), `framework/core/05-working-model.md` (3.1), `decision-trees/01-context-allowed.md`,
      `decision-trees/06-rule-placement.md`, `checklists/02-privacy-context.md`, D-23, D-35, D-47.
- [x] Laufzeitfassungen: Wurzel-Anweisungsdatei und Regelablage `10-*` betroffen; beide entstehen
      aus dem Kern und werden mit der Installation erneuert. Kein Pack-Eingriff nötig.
- [x] Belegstatus: Textbefund, **im Text gegengeprüft** – jede Fundstelle nachgelesen, die
      Zeilennummern des Reviews berichtigt. Keine Messung nötig und keine behauptet.
- [x] Test- und Validierungsbedarf: **sechs Sonden und zwei Gegenproben** (Prüfungen 29 und 30), je
      mit einer Sonde auf den verlorenen Anker. Gegenbeweis gegen 0.31.0.
- [x] Overlays: betroffen ist ein Overlay, das interne Kennungen als K1 führt – es wird damit
      ungültig. Migrationshinweis im `CHANGELOG.md`.
- [ ] Dokumentation: `CHANGELOG.md`, Decision Log (D-52 bis D-54), Roadmap, Testkatalog.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Welche K3-Kategorien sind unbedingt, welche einstufbar? | **Alle acht aus Abschnitt 2.1 sind unbedingt**, die Overlay-Ausnahme entfällt. Praktikabel bleibt die Lage über die bereinigte Ableitung: Platzhalter statt Hostname, das Original bleibt ausgeschlossen – das verlangt die Wurzel-Anweisungsdatei ohnehin. Sieben von acht Texten standen bereits so | Eine Konfigurationsdatei mit internen Hostnamen darf nicht unbereinigt bereitgestellt werden, und die Organisationsstufe „vertraulich“ verliert den K2-Pfad. Gewinn: **Die Kurzform, die tatsächlich in jede Sitzung lädt, ist erstmals wahr** |
| E2 | Bleibt die Möglichkeit, interne Adressen einzustufen, auf Ebene 1–3 erhalten? | **Nein.** Sie wäre der kleinere Eingriff, aber die Kurzform müsste den Vorbehalt mittragen – ein Bedingungssatz in genau dem Text, der ohne Nachlesen gelten soll. Dieses Projekt kennt den Befundtyp: eine Zusage, die mehr verspricht, als sie leistet. Eine unbedingte Regel, die stimmt, ist mehr wert als eine bedingte, die niemand nachliest | Weniger fachlicher Spielraum. Wer ihn braucht, ändert die Liste über den Änderungsprozess – sichtbar und mit Begründung, statt still im Overlay |
| E3 | Welche sicherheitsrelevanten Codeänderungen sind mit Freigabe bearbeitbar? | **Lokale Anwendungslogik** – Authentifizierungs- und Autorisierungsprüfungen im Quellcode, Kryptonutzung, Sitzungsverwaltung – bei Kontrollstufe hoch, mit Freigabe von `<APPROVAL_ROLE>` **und** `<SECURITY_CONTACT>` und mit begleitender Person. **Betrieb, Infrastruktur und tatsächliche Berechtigungen bleiben V6**, absolut | Die Grenze braucht ein entscheidbares Kriterium. Es lautet: Wirkt die Änderung über Build, Review und Quality Gates, oder **ist** die Datei die Berechtigung? Die Alternative – jede sicherheitsrelevante Umsetzung auszuschließen – wäre einfacher und widerspräche R3, R10 und der Kontrollstufentabelle |
| E4 | Auf welche Seite gehört Sicherheitskonfiguration als Code? | **Zum Betrieb, also V6** – trotz Ablage im Repositorium und trotz Review-Weg. Der Inhalt der Datei **ist** die Berechtigung; ein Fehler wirkt beim nächsten Deployment, nicht erst nach einer menschlichen Konfiguration. Das ist der Grenzfall, an dem die Regel entschieden wird, und er steht in der Tabelle (G-06) | Infrastrukturbeschreibungen sind damit nicht bearbeitbar, auch nicht mit Freigabe. Das trifft Projekte, die alles als Code führen – und ist der Preis dafür, dass die Grenze überhaupt eine ist |
| E5 | Wird das Aufgabenrisiko vom Koordinationsrisiko getrennt? | **Nein – R12 wird neu geschnitten**, nach Schreibziel und Aufsicht statt nach der Zahl der Sitzungen. Ein Faktor, drei neue Spalten, kein neuer Risikofaktor. Das löst die leere Schnittmenge auf und erhält die Einstufung, die gemessen ist: erweiterte Permission-Modi bleiben hoch (D-35) | Ein Faktor trägt weiterhin zwei Gedanken. Die Alternative – ein vierzehnter Faktor für das Koordinationsrisiko – wäre saubere Dimensionentrennung, verlangte aber eine zweidimensionale Einstufung und eine neue Regel für den „höchsten Treffer“. Für einen Widerspruch, der sich mit drei Spalten auflösen lässt, ist das zu viel Modell |
| E6 | Wie wird die Wirkung nachgewiesen, wo es nichts zu messen gibt? | **Zwei maschinelle Prüfungen und eine Grenzfalltabelle.** Prüfung 29 vergleicht die K3-Liste über fünf Fassungen und weist Bedingungen zurück – sie hätte beide Befunde dieses Antrags gefunden. Prüfung 30 hält die Grenzfalltabelle vollständig. Je Prüfung eine Sonde auf den **verlorenen Anker**: Eine Konsistenzprüfung, die ihren Suchtext verliert, besteht leise | Für die Abgrenzung zu V6 und für R12 gibt es keine maschinelle Prüfung – ein Skript kann eine Einstufung nicht beurteilen. Dort trägt die Grenzfalltabelle, geprüft in einer Sitzung (`FW-KO-05`). Das ist ausgewiesen, nicht überspielt |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle sechs Fragen wie vorgelegt.** E1 alle acht Kategorien unbedingt, Overlay-Ausnahme entfällt; E2 keine Einstufungsmöglichkeit auf Ebene 1–3; E3 Trennung nach Wirkungsweg, Anwendungslogik bei Kontrollstufe hoch bearbeitbar; E4 Sicherheitskonfiguration als Code gehört zu V6; E5 R12 wird neu geschnitten, kein neuer Risikofaktor; E6 Nachweis über Prüfungen 29 und 30 plus Grenzfalltabelle |
| Datum | 2026-09-13 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | D-52 (K3 unbedingt), D-53 (Betrieb gegen Anwendungslogik), D-54 (R12 nach Schreibziel und Aufsicht) |
| Auflagen | **Der Preis gehört in den Migrationshinweis, nicht nur in diesen Antrag.** Ein Overlay, das interne Kennungen als K1 führt, wird mit 0.32.0 ungültig, und die Organisationsstufe „vertraulich“ verliert ihren K2-Pfad – beides betrifft ein übernehmendes Projekt unmittelbar und steht im `CHANGELOG.md`. **Die zwei fehlenden Kategorien der Kurzform sind mitzuberichtigen**, obwohl der Befund sie nicht nennt: Eine Fassung, die sechs von acht führt, ist der eigentliche Schaden der Inkonsistenz. **Nachgewiesen:** sechs Sonden, zwei Gegenproben, Gegenbeweis gegen 0.31.0 – dort melden die neuen Prüfungen die drei Befunde dieses Antrags von selbst. **Offen bleibt:** Für die V6-Abgrenzung und für R12 gibt es keine maschinelle Prüfung; sie tragen über die Grenzfalltabelle und `FW-KO-05`, und dieser Test ist eine Sitzung und steht auf `offen` |
| Ziel-Release | `0.32.0` |
| Umsetzung | umgesetzt mit `0.32.0` |
