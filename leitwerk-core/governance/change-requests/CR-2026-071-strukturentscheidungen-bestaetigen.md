# Änderungsantrag `CR-2026-071`

| Feld | Inhalt |
|---|---|
| Titel | Die neun Strukturentscheidungen sind bestätigt – und die drei Einwände, die sie zweiunddreißig Releases lang aufgehalten haben, zielten an der Entscheidung vorbei |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-15 |
| Betroffene Artefakte | `governance/DECISION_LOG.md` (D-01 bis D-08, D-10, K-08, Legende, D-100, D-101), `docs/ROADMAP.md` (Standzeile, Kriterientabelle, Abschnitt „Strukturentscheidungen bestätigen", AP3), `tests/scripts/probe-pruefungen.py` (Sonde 46f), `CHANGELOG.md`, `tests/protocols/2026-09-15-gegenpruefung-strukturentscheidungen.md`, `tests/protocols/2026-09-15-wirkungsnachweise-0.49.0.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind die Strukturentscheidungen des Frameworks selbst |
| Art | Änderung (Statuswechsel), Fortschreibung |
| Dringlichkeit | **Regulär.** Kein Sicherheitsbezug. Der Gegenstand ist Arbeitspaket `AP3` der Roadmap mit Priorität P1 und Kriterium 4 von D-11 |

## 1. Anlass

**Beauftragt, nicht gefunden.** Das ist der erste Unterschied zu den fünf Releases davor:
Dieser Antrag geht nicht auf einen Befund zurück, sondern auf eine Anweisung. Sie folgt
aus der Messung, die `CR-2026-070` beigebracht hat.

Prüfung 46 zählt seit 0.48.0 die vier maschinell zählbaren Kriterien von D-11 bei jedem
Lauf. Ihre erste Anwendung war eine rückwirkende Messung über dreiundzwanzig
Releasestände, und ihr Ergebnis ist die Begründung dieses Antrags:

| Release | K1 | K2 | K3 | K4 | Summe |
|---|---|---|---|---|---|
| 0.26.0 | 30 | 117 | 67 | 9 | **223** |
| 0.33.0 | 31 | 118 | 69 | 9 | **227** |
| 0.35.0 … 0.48.0 | 29 | 118 | 69 | 9 | **225** |

**Kriterium 4 steht seit 0.26.0 auf neun. Es stand auch davor auf neun.** Die neun
Records tragen ihr Datum vom **2026-09-01**, dem Tag der Erstfassung 0.1.0 – seither sind
**neunundvierzig Releases** vergangen, und keiner hat einen davon gehoben.

**Der Vorgang war vorbereitet.** `CR-2026-019` hat am 2026-09-10 die Vorbedingung
geschaffen: Acht der zehn Records beschrieben einen Stand, den es nicht mehr gab; alle
acht sind fortgeschrieben worden. Derselbe Antrag hat die Entscheidung selbst
ausdrücklich **nicht** getroffen, sondern je Record vorgelegt (Abschnitt 4) – und
festgehalten, dass sieben ohne erkennbaren Einwand dastehen und drei mit einem benannten.

**Diese Vorlage ist seit zweiunddreißig Releases unbeantwortet.** Sie steht bis heute als
offener Haken in Abschnitt 7 von `CR-2026-019`:

> - [ ] **Zur Entscheidung offen:** der Statuswechsel je Record (Abschnitt 4). Drei
>   tragen einen benannten Einwand: D-05 (AP2-CC-12 offen), D-07 (K-20 bei
>   `devin-desktop` unbelegt), D-10 (K-04 offen)

**Der eigentliche Befund dieses Antrags steht in Abschnitt 3, und er war nicht gesucht:**
Alle drei Einwände zielen an der Entscheidung vorbei, gegen die sie vorgebracht sind.
Zwei von ihnen knüpfen die Bestätigung an Bedingungen, die **D-11 selbst ausdrücklich
ausnimmt**. Der dritte verwechselt eine Regel mit ihrer Durchsetzungstiefe bei einem
Client – der Unterscheidung, für die es **D-12** gibt.

> **Es ist nicht so, dass niemand entschieden hätte. Es ist so, dass die Bedingung falsch
> gewählt war – und eine falsch gewählte Bedingung wartet für immer.**

## 2. Die Gegenprüfung: neun Records, je Record ein Urteil

Nach D-23 gehört jeder Befund gegengeprüft, bevor er umgesetzt wird. Hier ist der
Gegenstand kein Befund, sondern eine Bestätigung – die Gegenprüfung fragt deshalb nicht
„stimmt der Befund?", sondern: **Trägt die Begründung von 2026-09-01 heute noch, und
womit ist das belegt?**

Vollständig mit Fundstellen und Messungen in
`tests/protocols/2026-09-15-gegenpruefung-strukturentscheidungen.md`. Kurzfassung:

| ID | Gegenstand | Begründung von 2026-09-01 | Trägt sie heute? | Beleg – gemessen, nicht gelesen |
|---|---|---|---|---|
| **D-01** | Ebenenmodell | „Vorgabe des Auftrags; Ebenen B und E sind für Separation of Concerns erforderlich" | **Ja** | `governance/PRIORITY_HIERARCHY.md` führt acht Stufen; Ebene B ist Stufe 2 und hat unter `framework/org-policies/` einen Einbindungspunkt mit zwei Dateien, Ebene E ist Stufe 8. Die Alternative „drei Ebenen ohne Packs" ist durch **zwei** Role Packs praktisch widerlegt. **Ehrlich dazu:** Von den beiden Packebenen ist eine besetzt; ein Technology Pack liegt bisher nur als Vorlage vor – das ist eine Aktivität von `AP4` und keine Frage an das Ebenenmodell |
| **D-02** | Lang- und Laufzeitform | „Tool Independence und Least Context" | **Ja, und stärker als damals** | D-12 bis D-14 haben die Naht benannt und maschinenlesbar gemacht: Beide Client Packs führen ein `manifest.json`, aus dem `install.py` und der Validator die Pfade lesen. 2026-09-01 war das eine Absicht, heute ist es eine Datei |
| **D-03** | Vier-Dateien-Struktur je Skill | „Trennung normativ/erläuternd; Least Context" | **Ja** | **13 von 13** Skills tragen genau `SKILL.md`, `EXAMPLES.md`, `TESTS.md`, `CHANGELOG.md` – abgezählt, nicht behauptet. Least Context ist seit dem 2026-09-12 gemessen (`ERH-13`) und am 2026-09-14 ein zweites Mal: Von zwölf Framework-Skills erscheinen **drei** in der Skill-Auflistung einer echten Sitzung, die übrigen neun hält `disable-model-invocation` aus dem Kontext (Zusage S4) |
| **D-04** | Berechtigungsdatei, restriktiver Standard | „Secure by Default" | **Ja, und seit D-18 geprüft statt zugesagt** | `framework/runtime/permissions.json` führt **53** `deny`-, **5** `ask`- und **19** `allow`-Regeln; die Kernzusagen werden als `_core_rules_integrity.deny_must_contain` aus derselben Quelle erzeugt (`clientmap.py`) und vom Validator gegen sie gehalten |
| **D-05** | Berechtigungsmodi | „Human Accountability, Review before Adoption" | **Ja** – Einwand siehe Abschnitt 3.1 | Das Verbot steht in beiden Client Packs; bei `claude-code` zusätzlich technisch sperrbar (AP2-CC-05). Das Framework liefert **genau ein** Agentenprofil aus (`framework/runtime/agents/fw-reviewer.md`), und es setzt das Feld nicht, um das der Einwand geht |
| **D-06** | Prioritätshierarchie, Verschärfungsprinzip | „Auflösung des Zielkonflikts Core über Overlay gegen Overlay definiert die Projektwerte" | **Ja** | Das Verschärfungsprinzip ist Regel 2.1 von `PRIORITY_HIERARCHY.md` und seit D-18 an der tragenden Stelle eine **geprüfte Eigenschaft**: Die Semantikabbildung lässt die Installation scheitern, wenn eine `deny`- oder `ask`-Regel kein Zielwerkzeug hat, und untersagt bei `allow` jede Verbreiterung |
| **D-07** | Kontextklassen K0 bis K3 | „Operationalisierbarkeit statt abstrakter Regeln" | **Ja** – Einwand siehe Abschnitt 3.2 | Die vier Klassen stehen in `framework/core/02-privacy.md` Abschnitt 2, vollständig auch in der Laufzeitschicht (D-24). Die Alternative „Freitextregeln" hätte weder die Auffangkategorie in 2.1 noch die Vorrangregel in 2.2 tragen können |
| **D-08** | Metadaten im Dateikörper | „Toleranz unbekannter Frontmatter-Schlüssel nicht belegt" | **Die Entscheidung ja – die Begründung nicht mehr** | Siehe Abschnitt 2.1. Die Form ist durchgehend angewendet: die Steckbriefzeile `\| Status \| … \|` steht in **69** Kerndateien, und Prüfung 46 zählt sie |
| **D-10** | Erweiterungsmodule, standardmäßig deaktiviert | „K-04 offen; Secure by Default" | **Ja** – Einwand siehe Abschnitt 3.3 | Seit 0.5.0 kein Vorsatz mehr, sondern erzeugt: `framework/runtime/` liefert **nur** `mcp-config.example.json`, keine wirksame Konfiguration, und `permissions.json` stellt **alle** MCP-Werkzeuge in `ask` (`{"tool": "mcp", "pattern": "*"}`) |

### 2.1 D-08 ist der einzige Sonderfall – und er ist kein Hindernis

**Bei acht von neun trägt die Begründung von 2026-09-01 unverändert. Bei D-08 trägt sie
nicht mehr, und die Entscheidung steht trotzdem** – auf einem anderen Grund.

Die Begründung war eine **Vorsichtsannahme**: Weil die Toleranz unbekannter
Frontmatter-Schlüssel unbelegt war, sollten Framework-Metadaten nicht ins Frontmatter.
Für `claude-code` ist die Lage seither geklärt (K-18): Die Herstellerdokumentation zählt
die Felder je Artefaktart abschließend auf, und die Abbildung erzeugt seit D-26 und D-27
**nur** dokumentierte Felder. Ein Metadatenfeld im Frontmatter wäre dort heute kein
Risiko mehr, sondern ein **undokumentiertes Feld** – Ballast ohne Durchsetzung. Für
`devin-desktop` ist die Frage unverändert unbelegt; dort trägt die alte Begründung weiter.

**Dieselbe Entscheidung, zwei Gründe, je Client ein anderer.** Das ist genau die Lage,
für die es die Fähigkeitsmatrix gibt, und es ist kein Einwand gegen die Bestätigung. Der
Statustext hält beides fest, damit niemand die Begründung von 2026-09-01 für die heutige
hält.

> **Eine Bestätigung ist keine Behauptung, dass sich nichts geändert hat.** Sie ist die
> Feststellung, dass die Entscheidung heute trägt – und wo sie es aus einem anderen Grund
> tut, gehört der andere Grund hingeschrieben.

## 3. Die drei Einwände aus `CR-2026-019` – und was sie wirklich treffen

### 3.1 D-05 / `AP2-CC-12`: ein Einwand gegen die Durchsetzungstiefe, nicht gegen die Regel

**Der Einwand, wörtlich:** Ob die Sperre gegen den Modus ohne Rückfragen auch für das Feld
`permissionMode` eines Subagentenprofils gilt, ist nicht dokumentiert.

**Gemessen: die Frage ist unverändert offen.** Die Erhebung vom 2026-09-13 über
Unteragenten führt sie ausdrücklich unter „Was diese Erhebung nicht belegt": „`permissionMode`
im Profil (`AP2-CC-12`, offene Teilfrage zu M2). **Unberührt.**"

**Und sie ist trotzdem kein Einwand gegen D-05.** D-05 entscheidet, dass der Modus ohne
Rückfragen **untersagt** ist. `AP2-CC-12` fragt, ob ein bestimmter Client dieses Verbot auf
einem bestimmten Weg zusätzlich **technisch** erzwingen kann. Das sind zwei verschiedene
Dinge, und dass sie zwei sind, ist keine Auslegung, sondern **D-12**: Jede technische
Zusage wird je Client als `[TECHNISCH]`, `[TEXTUELL]` oder `[NICHT ABBILDBAR]`
eingestuft, weil eine Regel auch dort gilt, wo die Engine sie nicht erzwingt.

> **Wer eine Regel erst bestätigt, wenn jeder Client sie technisch erzwingt, hat D-12
> abgeschafft** – und mit ihr die halbe Begründung des Frameworks.

**Dazu ein Messwert, der die Reichweite des Einwands bemisst:** Das Framework liefert
**genau ein** Agentenprofil aus, und es setzt das Feld `permissionMode` **nicht**. Die
offene Frage hat in den ausgelieferten Artefakten keinen Träger. Sie bleibt offen, sie
bleibt eine Verifikationsschuld der Fähigkeitsmatrix – **und sie steht in Kriterium 1 von
D-11, nicht in Kriterium 4.**

### 3.2 D-07 / `K-20`: das Modell beantwortet den Einwand in seinem eigenen Abschnitt 1.3

**Der Einwand, wörtlich:** K-20 – Art und Ort der Codebasis-Indexierung – ist bei
`devin-desktop` unbelegt; das Datenschutzmodell setzt eine Aussage darüber voraus.

**Der zweite Halbsatz ist falsch, und der Gegenbeweis steht im Modell selbst.**
`framework/core/02-privacy.md` regelt den Fall der fehlenden Aussage ausdrücklich:

> Abschnitt 1.3: *Bis zum Vorliegen dieser Prüfung gilt die restriktivste Auslegung: Nur
> Kontextklasse K0 und K1 dürfen bereitgestellt werden …*
>
> Abschnitt 2.2 Regel 3: *Fehlt eine Einstufung, gilt K3.*

**Das Modell setzt die Aussage nicht voraus – es enthält die Regel für ihr Fehlen.** Ein
Modell, das seinen eigenen unbeantworteten Eingabewert auffängt, wird durch dessen
Unbeantwortetheit nicht geschwächt; es wird durch sie **vorgeführt**. Dass K-20 offen ist,
ist ein Argument **für** D-07 und gegen die Alternative „Freitextregeln", die für diesen
Fall gar keine Antwort gehabt hätte.

**Dazu die Zuständigkeit:** Abschnitt 1.2 desselben Moduls erklärt die vertraglichen und
technischen Bedingungen – Verarbeitungsorte, Aufbewahrung, Codebasis-Indexierung –
ausdrücklich für **organisationsspezifisch** und verlangt sie vor der Einführung geprüft
und im Overlay referenziert. **Das ist Aufgabe der aufnehmenden Organisation, und D-11
nimmt genau das aus.** Der offene Rest von K-20 ist ein VERIFY-Marker – **Kriterium 1**,
nicht Kriterium 4. Ihn zur Bedingung von Kriterium 4 zu machen, koppelt zwei Kriterien,
die D-11 getrennt aufzählt.

### 3.3 D-10 / `K-04`: die Zusage hat ein Gegenüber, und es ist ein Mechanismus

**Der Einwand, wörtlich:** K-04 – Nutzungsumfang Cloud/CLI – ist offen und liegt außerhalb
des Frameworks. Solange die Organisation ihn nicht festgelegt hat, ist „vorgesehen,
standardmäßig deaktiviert" eine Zusage ohne Gegenüber.

**Zwei Gründe, und der zweite ist der stärkere.**

**Erstens die Zuständigkeit.** K-04 nennt als entscheidende Rolle „Projektleitung mit
Informationssicherheit" und trägt den Platzhalter `<TBD: Freigabe Cloud/CLI-Nutzung>`. Das
ist eine **organisatorische Freigabe**. D-11 sagt dazu einen Satz, und er ist eindeutig:
*Pilot, Onboarding und organisatorische Freigabe sind **nicht** Vorbedingung, sondern
Aufgabe der aufnehmenden Organisation.* Ein Einwand, der genau das zur Vorbedingung macht,
steht gegen die Entscheidung, deren Kriterium er bedienen will.

**Zweitens der Mechanismus.** „Eine Zusage ohne Gegenüber" trifft seit 0.5.0 nicht mehr zu,
und das ist nachzählbar: `framework/runtime/` liefert **keine** wirksame MCP-Konfiguration
aus, sondern nur `mcp-config.example.json`; `permissions.json` stellt **alle**
MCP-Werkzeuge in `ask`. Die Deaktivierung ist erzeugt, nicht versprochen. **D-10 ist
gerade die Entscheidung, die das Framework sicher hält, solange K-04 offen ist** – sie
braucht K-04 nicht beantwortet, sie ist die Antwort auf seine Offenheit.

### 3.4 Was die drei gemeinsam haben

| Einwand | Wogegen er sich richtet | Wozu er gehört |
|---|---|---|
| `AP2-CC-12` (D-05) | die Durchsetzungstiefe **eines** Clients | Fähigkeitsmatrix (D-12), Kriterium 1 von D-11 |
| `K-20` (D-07) | eine **Eingabe** des Modells, deren Fehlen das Modell selbst regelt | organisatorische Prüfung, Kriterium 1 von D-11 |
| `K-04` (D-10) | eine **organisatorische Freigabe** | aufnehmende Organisation – von D-11 ausdrücklich ausgenommen |

**Keiner der drei richtet sich gegen die Entscheidung, gegen die er vorgebracht ist.**
Alle drei sind gute Fragen, keine davon ist beantwortet, und keine davon gehört zu
Kriterium 4.

> **Der wiederkehrende Befundtyp dieses Repositoriums, eine Ebene höher:** Sonst ist es
> *eine Zusage, die mehr verspricht, als sie leistet*. Hier ist es **eine Bedingung, die
> mehr verlangt, als ihr Kriterium fordert** – und das hält genauso zuverlässig auf, wie
> eine zu schwache Zusage durchlässt. Zweiunddreißig Releases lang, mit einem grünen
> Validator bei jedem einzelnen.

## 4. Nebenbefunde

### 4.1 Die Legende erklärt vier Statuswerte, die Tabelle führt sieben

**Beim Nachzählen der Statuszelle, also beim Vorbereiten eben dieses Antrags, angefallen.**
Die Legende in Zeile 4 von `DECISION_LOG.md` nennt `geklärt`, `entschieden (Vorschlag)`,
`offen` und `verify`. Abgezählt über beide Tabellen:

| Statuswert | Vorkommen | In der Legende? |
|---|---|---|
| `entschieden (CR-2026-NNN)` | **89** Decision Records | **nein** |
| `ersetzt durch D-11` | 1 (D-09) | **nein** |
| `offen by design` | 1 (K-16) | **nein** |
| `geklärt durch Auftrag` | 1 (K-09) | **nein** |
| `entschieden (Vorschlag)` | 9 Records, 5 Klärungspunkte | ja |
| `geklärt`, `offen`, `verify` | übrige | ja |

**Der meistverwendete Statuswert des Dokuments steht nicht in seiner Legende** – seit
D-11 und neunundachtzig Records. Das ist der Befundtyp dieses
Repositoriums in seiner Grundform: ein Verzeichnis, das seinen eigenen Bestand nicht
vollständig nennt.

**Berichtigt, nicht geprüft.** Eine Prüfung, die das Vokabular der Statuszellen gegen die
Legende hält, ist baubar und wäre die richtige Abhilfe. Sie ist hier **bewusst nicht
gebaut**: Der `<FRAMEWORK_OWNER>` hat für dieses Release angeordnet, keine neue Prüfung zu
bauen, bevor sich eine der vier D-11-Zahlen bewegt hat. **Sie bewegt sich mit diesem
Release** – die Prüfung ist damit ab dem nächsten zulässig und steht als Kandidat. Siehe
E5.

### 4.2 `K-08` ist die offene Entscheidung von `AP3` und trägt denselben Statuswert

`AP3` führt in seinem Feld „Offene Entscheidungen" genau einen Eintrag: *Bestätigung der
8-stufigen Hierarchie (K-08)*. K-08 steht auf `entschieden (Vorschlag)` und sagt in der
Sache dasselbe wie D-01 und D-06.

**D-01 und D-06 zu bestätigen und K-08 stehen zu lassen, hieße denselben Sachverhalt in
zwei Zuständen zu führen** – das zweite Register neben dem ersten, und dieses Repositorium
hat diesen Befundtyp in seinem eigenen Bestand siebenmal gefunden. K-08 geht mit.

**Die vier übrigen Klärungspunkte auf `entschieden (Vorschlag)` gehen nicht mit.** Sie
tragen offene Teilfragen und keinen Decision Record: K-12 (Skill-Ablage – die Discovery
ist unverifiziert, die Sache ist durch D-15 und D-16 ohnehin in eine Pfadabbildung je Pack
überführt), K-13 (Ablage und Verteilung), K-17 (Sprache) und K-18 (Frontmatter-Felder –
für einen Client geklärt, für den anderen `verify`). Siehe E4.

### 4.3 Nachtrag zum Protokoll von `CR-2026-070`

Das Protokoll `2026-09-15-gegenpruefung-d11-zaehlregeln.md` formuliert die Zeile zum
seriellen Abnahmelauf **vorsichtiger, als die Messung es verlangt**: Es sagt, der Vergleich
sei an einem Zwischenstand gemessen, weil der serielle Lauf gegen den endgültigen Wortlaut
bei Protokollabschluss noch nicht zurück war. **Er ist es inzwischen, und er ist grün** –
Exit 0, 250 Ergebniszeilen, sortiert deckungsgleich mit dem nebenläufigen Lauf, 977 s auf
einer Bahn gegen 128 s auf acht. Das ist kein Fehler im Protokoll (es behauptet weniger,
als wahr ist) und kein eigenes Release wert; es ist hier nachgetragen, wie die Übergabe es
vorgesehen hat.

## 5. Vorgeschlagene Änderung

1. **Die neun Records D-01 bis D-08 und D-10 wechseln den Status** auf
   `entschieden (CR-2026-071)`. Der Wortlaut von 2026-09-01 und die Fortschreibung aus
   `CR-2026-019` bleiben unverändert stehen (die Regel aus `CR-2026-019`: ein Decision Log
   ist ein Verlaufsdokument). Angehängt wird je Record ein Satz, der die Bestätigung datiert
   und den Beleg nennt, auf dem sie steht.
2. **`K-08` wird mitbestätigt** – die offene Entscheidung von `AP3`, in der Sache D-01 und
   D-06.
3. **Die Legende führt die Statuswerte, die die Tabellen wirklich verwenden** (Nebenbefund
   4.1).
4. **Zwei neue Decision Records:** D-100 (die Bestätigung und ihr Maßstab), D-101 (das
   Statusvokabular des Decision Logs).
5. **Die Standzeile in `docs/ROADMAP.md`** wird nachgezogen: Kriterium 4 von **9 auf 0**.
   Das ist der Vorgang, für den Prüfung 46 gebaut ist – **ohne ihn wäre der Lauf rot**.
6. **Sonde 46f wird umgebaut.** Sie hob bisher D-10 aus `entschieden (Vorschlag)` und
   belegte damit die Richtung „Fortschritt nicht nachgezogen". Nach diesem Release hat die
   Hebung keinen Gegenstand mehr – die Sonde **stellt ihren Defekt jetzt her statt ihn zu
   entfernen** und deckt die Richtung, die bisher **keine** Sonde deckte: den **Rückfall**.
7. **Die Roadmap** zieht Kriterientabelle, den Abschnitt „Strukturentscheidungen
   bestätigen" und das Feld „Offene Entscheidungen" von `AP3` nach.

## 6. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | **Welcher Statuswert?** „Bestätigen" ist der Vorgang; welcher Zustand steht danach da? | **`entschieden (CR-2026-071)`** – derselbe Wert, den die übrigen **89** Records tragen. Der Vorgang steht in der Antragsnummer und im angehängten Satz, nicht in einem eigenen Wort | **Der Unterschied zwischen „vorgeschlagen und bestätigt" und „von Anfang an entschieden" ist danach nur noch im Text der Zelle zu lesen, nicht mehr am Statuswort.** Das ist hinnehmbar, weil die Zelle ihn ausdrücklich nennt und das Datum 2026-09-01 stehen bleibt. Verworfen: **ein eigener Wert `bestätigt`** – ein zweites Vokabular für denselben Zustand, und Prüfung 46 müsste es mitlernen; genau der Befundtyp, den dieses Repositorium siebenmal gefunden hat |
| **E2** | **Alle neun in einem Antrag – oder je Record ein eigener?** | **Alle neun in einem.** Sie teilen den Anlass (`AP3`), das Datum, die Vorlage aus `CR-2026-019` und den Maßstab | Preis: Wer später nachliest, warum **ein** Record bestätigt wurde, liest einen Antrag über neun. **Aufgefangen durch die Zeile je Record in Abschnitt 2** – und neun Anträge über denselben Vorgang wären neun Kopien derselben Begründung. Verworfen: **nur die sieben ohne Einwand bestätigen** – das hätte die drei Einwände ein zweites Mal ungeprüft stehen gelassen, und ihre Prüfung ist der Ertrag dieses Antrags |
| **E3** | **Was geschieht mit den drei Einwänden – aufgelöst oder übergangen?** | **Aufgelöst, einzeln, mit Beleg** (Abschnitt 3). Die drei **Fragen** bleiben offen und behalten ihren Ort: `AP2-CC-12` in der Fähigkeitsmatrix, K-20 und K-04 in der Klärungstabelle | **Es bleibt drei offene Fragen zu einem bestätigten Bestand.** Das ist die Lage und nicht ihre Verschleierung: Keine der drei ist eine Frage nach Kriterium 4. Verworfen: **die Bestätigung bis zu ihrer Beantwortung zurückstellen** – das ist genau das, was zweiunddreißig Releases lang geschehen ist, und zwei der drei liegen ausdrücklich außerhalb des Einflussbereichs des `<FRAMEWORK_OWNER>`, den D-11 zum Maßstab macht |
| **E4** | **Gehen die fünf Klärungspunkte auf `entschieden (Vorschlag)` mit?** | **Nur `K-08`.** Es ist die namentlich genannte offene Entscheidung von `AP3` und sagt in der Sache dasselbe wie D-01 und D-06 | **Vier Klärungspunkte behalten einen Statuswert, den kein Decision Record mehr trägt.** Das ist gewollt: Ein Klärungspunkt ist eine **Frage**, ein Decision Record eine **Festlegung**, und bei allen vieren ist ein Teil der Frage unbeantwortet (K-12 Discovery unverifiziert, K-18 bei einem Client `verify`). Prüfung 46 zählt sie nicht – das ist seit `CR-2026-070` entschieden und hier nicht neu aufzumachen. Verworfen: **alle fünf mitnehmen** – das hätte vier offene Fragen für entschieden erklärt, um eine Zahl zu senken, die sie gar nicht zählt |
| **E5** | **Bekommt das Statusvokabular eine Prüfung?** Die Legende nannte vier von sieben Werten | **Nein, nicht in diesem Release.** Die Legende wird berichtigt; die Prüfung steht als Kandidat für das nächste | **Eine Zusage ohne Mechanismus, und der Antrag sagt es selbst.** Der Grund ist eine ausdrückliche Anweisung des `<FRAMEWORK_OWNER>` vom 2026-09-15: keine neue Prüfung, bevor sich eine der vier D-11-Zahlen bewegt hat. **Mit diesem Release bewegt sie sich** – die Sperre fällt danach, und der Kandidat steht in der Roadmap. Verworfen: **die Prüfung gleich mitbauen** – dann wäre dieses Release wieder zur Hälfte Arbeit am Prüfapparat, und genau das war der Anlass der Anweisung |
| **E6** | **Was wird aus Sonde 46f?** Sie hebt D-10 aus `entschieden (Vorschlag)`; nach diesem Release gibt es dort nichts mehr zu heben | **Umbauen: Sie setzt einen bestätigten Record auf `entschieden (Vorschlag)` zurück** und belegt damit den **Rückfall** – die Richtung, die bisher keine Sonde deckte, weil Kriterium 4 nie null war | **Die Richtung „Fortschritt nicht nachgezogen" verliert bei Kriterium 4 ihre Sonde.** Sie bleibt gedeckt: Sonde 46a stellt eine Zahl der Standzeile zu hoch und erzeugt genau diese Meldung. Verworfen: **die Sonde auf ein anderes Kriterium umhängen** – dann prüfte sie nicht mehr den Gegenstand, an dem der Rückfall wirklich eintreten kann; **die Sonde entfernen** – eine Prüfung ohne Sonde gilt nach D-23 als nicht vorhanden, und Prüfung 46 hat vier Gegenstände |
| **E7** | **Muss die Standzeile in demselben Release nachgezogen werden?** | **Ja, im selben Patch.** Ohne sie ist der Lauf rot | **Keiner – das ist der Preis, den `CR-2026-070` E1 ausdrücklich gewollt hat.** Dies ist der erste Fall, in dem der Mechanismus greift, und er greift bei einem Fortschritt. **Gemessen zwischen zwei Patches:** Nach dem Statuswechsel im Decision Log und **vor** dem Nachziehen der Standzeile meldete der Lauf gegen den Arbeitsbaum genau **einen** Fehler, und zwar über einen **Fortschritt** – `Kriterium 4 … ist gezählt 0, die Standzeile nennt 9`. Ohne diese Bauform stünde dort heute noch neun |

## 7. Prüffragen (durch Owner auszufüllen)

- [x] Richtige Ebene nach Entscheidungsbaum 6? — Ja. Gegenstand sind die Strukturentscheidungen des Kerns; geändert werden ein Governance-Dokument, die Roadmap und eine Sonde. Keine Regel wird eingeführt oder gelockert.
- [x] Verschärfungsprinzip eingehalten? — Nicht berührt. Keine Regel ändert ihren Inhalt; neun Festlegungen wechseln ihren Status.
- [x] Widerspruchsfreiheit geprüft? — Gegenstand von Abschnitt 2 und 3. Gelesen: `PRIORITY_HIERARCHY.md`, `framework/core/02-privacy.md`, `framework/core/08-skill-conventions.md`, beide `CLIENT_PACK.md`, `framework/runtime/permissions.json`, `clientmap.py`, `CR-2026-018`, `CR-2026-019`, `CR-2026-070`, `tests/protocols/2026-09-13-erhebung-unteragent.md`.
- [x] Laufzeitfassungen betroffen? — Nein. Weder Wurzel-Anweisungsdatei noch Regelablage noch Berechtigungsdatei ändern sich; `install.py --check` bleibt unberührt.
- [x] Belegstatus korrekt? — Jede Zeile von Abschnitt 2 nennt eine gemessene Fundstelle. Die drei offenen Fragen sind als **offen** geführt und nicht als beantwortet ausgegeben.
- [x] Test- und Validierungsbedarf? — Keine neue Prüfung (E5). **Eine bestehende Sonde bricht und wird umgebaut** (E6); der Gegenbeweis dazu steht im Wirkungsnachweis. Validator und Sondenlauf in beiden Kodierungsumgebungen.
- [x] Auswirkungen auf Overlays und laufende Onboardings? — Keine. Der Kern bleibt byte-gleich bis auf Governance- und Dokumenttexte; Prüfung 46 läuft in jeder Installation mit derselben Standzeile.
- [x] Dokumentation? — CHANGELOG, Decision Log (D-100, D-101), Roadmap (Standzeile, Kriterientabelle, `AP3`), Protokolle.

## 8. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen.** E1 bis E7 wie vorgelegt am 2026-09-15 durch den Framework Owner entschieden |
| Datum | 2026-09-15 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Die Vorlage aus `CR-2026-019` liegt seit zweiunddreißig Releases unbeantwortet vor. Ihre Gegenprüfung zeigt: Bei acht von neun Records trägt die Begründung von 2026-09-01 unverändert, bei D-08 trägt die Entscheidung auf einem anderen Grund – und die drei benannten Einwände richten sich sämtlich gegen etwas anderes als die Entscheidung, gegen die sie vorgebracht sind. Zwei von ihnen machen zur Bedingung, was D-11 ausdrücklich ausnimmt. **Eine falsch gewählte Bedingung wartet für immer**; sie wird hier nicht erfüllt, sondern richtiggestellt |
| Decision-Log-Eintrag | **D-100** (die neun sind bestätigt; Maßstab ist die tragende Begründung, nicht die unveränderte), **D-101** (das Statusvokabular des Decision Logs steht vollständig in seiner Legende) |
| Auflagen | **Der Gegenbeweis gehört dazu:** Die umgebaute Sonde 46f MUSS gegen 0.48.0 fallen und gegen `main` bestehen. **Dazu ist zu messen, was die alte Fassung auf dem neuen Stand anrichten würde** – und das Ergebnis gehört ins Protokoll, auch wenn es unbequemer ist als erwartet: Sie meldet **nicht** `[Praeparation gebrochen]`, sondern ihr Suchtext trifft weiterhin – im Verlaufszusatz der Zelle, also an einer Stelle, die Prüfung 46 gar nicht liest. Der Baumvergleich meldet dann kein `[nichts praepariert]`, und der Fehlschlag sähe aus wie ein Befund an der Prüfung, wo einer an der Sonde vorliegt. **Das ist der schlechteste der drei möglichen Zustände, und er ist der Grund, warum die neue Fassung den ANFANG der Statuszelle trifft statt eine Zeichenkette irgendwo in ihr.** **Dazu die Gegenprüfung selbst:** Jeder der neun Records ist mit seiner Begründung, seinem Beleg und seinem Urteil im Protokoll auszuweisen; eine Bestätigung ohne die neun Nachweise wäre genau die Bauform, die dieses Repositorium beanstandet |
| Ziel-Release | `0.49.0` |
| Umsetzung | umgesetzt mit `0.49.0` |

## 9. Umsetzung (nach Annahme)

- [x] D-01 bis D-08 und D-10 auf `entschieden (CR-2026-071)`; Wortlaut, Begründung und Datum von 2026-09-01 sowie die Fortschreibung aus `CR-2026-019` unverändert stehen gelassen
- [x] Je Record ein angehängter Satz mit Datum und Beleg der Bestätigung
- [x] `K-08` mitbestätigt (E4)
- [x] Legende um `entschieden (CR-…)`, `ersetzt durch …`, `offen by design` und `geklärt durch Auftrag` ergänzt (D-101)
- [x] D-100 und D-101 eingetragen
- [x] Standzeile in `docs/ROADMAP.md`: Kriterium 4 von 9 auf **0** (E7)
- [x] Sonde 46f umgebaut (E6), Gegenbeweis gegen 0.48.0 im Wirkungsnachweis
- [x] Roadmap: Kriterientabelle, Abschnitt „Strukturentscheidungen bestätigen", `AP3` nachgezogen
- [x] Validator 0 Fehler, 0 Warnungen; Sondenlauf in beiden Kodierungsumgebungen über 251 Zeilen zeilengleich, Exit 0 (154 Sonden, 62 Gegenproben, 12 Selbstproben – unverändert gegenüber 0.48.0)
- [x] Gegenbeweis gegen 0.48.0: **genau eine Abweichung**, und es ist Sonde 46f mit `[Praeparation gebrochen]`
- [x] Die zweite Richtung der Auflage gemessen – die alte Fassung hätte **danebengetroffen statt gebrochen**; der Antragstext ist gegen die Messung berichtigt worden, nicht umgekehrt
- [x] Wirkungsnachweis: `tests/protocols/2026-09-15-wirkungsnachweise-0.49.0.md`
- [ ] **Folgearbeit:** Die Prüfung auf das Statusvokabular des Decision Logs (E5, Nebenbefund 4.1) – ab dem nächsten Release zulässig, weil sich mit diesem eine der vier D-11-Zahlen bewegt hat
- [ ] **Folgearbeit:** Die vier Klärungspunkte K-12, K-13, K-17 und K-18 (E4) – je ein eigener Vorgang, weil bei allen vieren ein Teil der Frage unbeantwortet ist
