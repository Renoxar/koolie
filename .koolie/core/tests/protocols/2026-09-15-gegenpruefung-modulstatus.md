# Gegenprüfung: die 69 Statusträger des Kerns und die Vorbedingung, ohne die nichts gehen sollte

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-15 |
| Framework-Version | `0.49.0` (Stand `main`, Commit `73d7fbd`); umgesetzt mit `0.50.0` |
| Gegenstand | Kriterium 3 von D-11 – *„alle Modulstatus oberhalb `entwurf`"*. Gezählt von Prüfung 46: **69**, und keiner steht darüber |
| Anlass | Arbeitspaket `AP3` der Roadmap (P1), zweite Aktivität: *„Status je Modul von `entwurf` auf `pilot`"*. Kandidat 1 der Übergabe – mit der ausdrücklichen Auflage, **zuerst eine Vorentscheidung zu klären** |
| Antrag | `CR-2026-072`, D-102 bis D-104, K-36, K-37 |
| Prüfmethode | Abzählen am Bestand mit der Zählregel der Prüfung 46 selbst (`_d11_zaehlen`, Kriterium 3), getrennt nach Gattung; je Träger die Bedingungen des Lebenszyklusmodells (`framework/core/08-skill-conventions.md` Abschnitt 7) gegen den vorliegenden Stand gehalten; die beiden naheliegenden **mechanischen** Bedingungen versuchsweise angewendet und an ihren Fehltreffern gemessen |
| Ausgeführte Befehle | Ein Messskript über `leitwerk-core/` (Ausgabe in Abschnitt 2 unverändert); `python leitwerk-core/tests/scripts/validate-framework.py --root .` |
| Ergebnis | **Die Vorentscheidung war für 13 der 69 Träger keine Vorbedingung.** Das Lebenszyklusmodell verlangt für `pilot` „Testfälle **vorhanden**" – „bestanden" erst für `aktiv`. Die angenommene Kopplung an Kriterium 2 besteht für den ersten Übergang **nicht**. Für die 52 Nicht-Skill-Träger besteht sie, und dort fehlt jede Übergangsbedingung. **Vier weitere Träger sind gar keine Module:** ihr Statuswert ist ein Formularfeld, das in jede Kopie übergeht – mit ihnen ist Kriterium 3 **nie** auf null zu bringen |

## 1. Warum diese Gegenprüfung die Vorbedingung prüft und nicht den Befund

D-23 verlangt die Gegenprüfung vor der Umsetzung. Der Gegenstand hier ist kein Befund,
sondern eine **Aufgabe mit vorangestellter Bedingung**. Die Übergabe formuliert sie so:

> ⚠️ **Zuerst eine Frage klären, die beim Zählen aufgefallen ist:** Das Lebenszyklusmodell
> definiert die Übergangsbedingungen **nur für Skills**. 57 der 69 Träger sind keine
> Skills. **Für sie gibt es keine niedergeschriebene Bedingung, um `entwurf` zu
> verlassen.** Das gehört entschieden, bevor ein Status gehoben wird. **Und:** Für die
> zwölf Skills verlangt das Modell „Testfälle bestanden" – die stehen alle auf `offen`,
> also sind Kriterium 2 und 3 dort **gekoppelt**.

**Das ist die Form, die dieses Repositorium mit 0.49.0 gelernt hat zu misstrauen.** Dort
hielt eine Bedingung einen Vorgang zweiunddreißig Releases lang auf, und alle drei
Einwände, aus denen sie bestand, zielten an ihrem Gegenstand vorbei. Die Lehre steht als
Satz im Protokoll:

> **Eine zu schwache Zusage lässt durch und fällt irgendwann auf. Eine zu starke Bedingung
> hält auf – und fällt nie auf, weil ein unerfülltes Vorzeichen wie Sorgfalt aussieht.**

Die erste Frage dieser Gegenprüfung ist deshalb nicht „wie lautet die Bedingung für die
Nicht-Skills?", sondern: **Stimmt die Bedingung, die hier vorangestellt wird?** Sie
enthält drei Behauptungen, und zwei davon sind falsch.

## 2. Die Messung am Bestand (unveränderte Ausgabe)

Zählregel und Sichtfeld sind die der Prüfung 46: jede Zeile `| Status | … |` in den ersten
sechzig Zeilen einer `.md` unter `leitwerk-core/`, ohne `build/`, `CHANGELOG.md`,
`governance/change-requests/` und `tests/protocols/`, verglichen am **ersten Wort** des
Werts.

```text
Traeger mit Statuszeile: 69
   68  entwurf
    1  entwurf (Referenzpack der Erstfassung)

Nach Gattung:
  Skill         13
  Vorlage        4
  Nicht-Skill   52

Die dreizehn Skills:
  role-re-ticket           RP-RE-SK-001 v0.1.2 M1  Dateien 4/4  P5 N10  offene Zellen 15  Marker 0
  fw-bugfix-prepare        FW-SK-009    v0.1.1 M2  Dateien 4/4  P2 N4  offene Zellen  6  Marker 0
  fw-change-analyze        FW-SK-003    v0.1.2 M1  Dateien 4/4  P2 N3  offene Zellen  5  Marker 0
  fw-change-small          FW-SK-005    v0.1.1 M3  Dateien 4/4  P2 N5  offene Zellen  7  Marker 0
  fw-code-explain          FW-SK-002    v0.1.3 M1  Dateien 4/4  P2 N3  offene Zellen  5  Marker 0
  fw-docs-update           FW-SK-011    v0.1.2 M5  Dateien 4/4  P2 N4  offene Zellen  6  Marker 0
  fw-error-analyze         FW-SK-008    v0.1.3 M1  Dateien 4/4  P2 N4  offene Zellen  6  Marker 0
  fw-mr-description        FW-SK-012    v0.1.3 M5  Dateien 4/4  P2 N4  offene Zellen  6  Marker 1
  fw-plan                  FW-SK-004    v0.1.1 M2  Dateien 4/4  P2 N4  offene Zellen  6  Marker 0
  fw-refactor              FW-SK-007    v0.1.1 M3  Dateien 4/4  P2 N5  offene Zellen  7  Marker 0
  fw-repo-analyze          FW-SK-001    v0.1.3 M1  Dateien 4/4  P2 N3  offene Zellen  5  Marker 0
  fw-review-support        FW-SK-010    v0.1.4 M1  Dateien 4/4  P2 N5  offene Zellen  7  Marker 2
  fw-tests                 FW-SK-006    v0.1.1 M4  Dateien 4/4  P2 N4  offene Zellen  6  Marker 0

Die vier Vorlagen:
  clients/_template/CLIENT_PACK.md
      Status 'entwurf'  Version '0.2.0'  Ausfuellschlitze <TBD: 20
      Kennungszelle: CP-<CLIENT_PACK_CODE>
  framework/role-packs/_template/ROLE_PACK.md
      Status 'entwurf'  Version '0.1.1'  Ausfuellschlitze <TBD: 5
      Kennungszelle: RP-<ROLE_PACK_CODE>
  framework/tech-packs/_template/TECH_PACK.md
      Status 'entwurf'  Version '0.1.0'  Ausfuellschlitze <TBD: 7
      Kennungszelle: TP-<TECH_PACK_CODE>
  templates/SKILL_TEMPLATE.md
      Status 'entwurf'  Version '0.1.2'  Ausfuellschlitze <TBD: 1
      Kennungszelle: <FW-SK-NNN / PRJ-SK-NNN / RP-<PACK>-SK-NNN / TP-<PACK>-SK-NNN>

Markerfundstellen der Traeger, nach Rolle:
  NENNUNG  checklists/11-framework-release.md:40
  NENNUNG  clients/README.md:67
  offen    clients/claude-code/CLIENT_PACK.md:89
  offen    clients/devin-desktop/CLIENT_PACK.md:24
  offen    clients/devin-desktop/CLIENT_PACK.md:26
  offen    clients/devin-desktop/CLIENT_PACK.md:27
  offen    clients/devin-desktop/CLIENT_PACK.md:82
  offen    clients/devin-desktop/CLIENT_PACK.md:94
  offen    clients/devin-desktop/CLIENT_PACK.md:101
  offen    clients/devin-desktop/CLIENT_PACK.md:116
  offen    clients/devin-desktop/CLIENT_PACK.md:136
  NENNUNG  docs/ROADMAP.md:1878
  offen    framework/skills/fw-mr-description/SKILL.md:78
  offen    framework/skills/fw-review-support/SKILL.md:77
  offen    framework/skills/fw-review-support/SKILL.md:91
  NENNUNG  governance/RELEASE_PROCESS.md:46
  offen    templates/SKILL_TEMPLATE.md:26

Kernmodule ohne Statuszeile:
  framework/core/00-principles.md           Statuszeile: NEIN  Verbindlichkeit: normativ
  framework/core/01-governance.md           Statuszeile: NEIN  Verbindlichkeit: normativ
  framework/core/02-privacy.md              Statuszeile: NEIN  Verbindlichkeit: normativ (Abschnitte 1–6), Erläuterung (Abschnitt 7)
  framework/core/03-security.md             Statuszeile: NEIN  Verbindlichkeit: normativ (Abschnitte 1–6), Erläuterung (Abschnitt 7)
  framework/core/04-quality.md              Statuszeile: NEIN  Verbindlichkeit: normativ (Abschnitte 1–4), Erläuterung (Abschnitt 5)
  framework/core/05-working-model.md        Statuszeile: NEIN  Verbindlichkeit: normativ (Abschnitte 1–3), Erläuterung (Abschnitt 4)
  framework/core/06-prompting-rules.md      Statuszeile: NEIN  Verbindlichkeit: normativ (Abschnitte 1–3), Erläuterung (Abschnitt 4)
  framework/core/07-review-rules.md         Statuszeile: NEIN  Verbindlichkeit: normativ (Abschnitte 1–4), Erläuterung (Abschnitt 5)
  framework/core/08-skill-conventions.md    Statuszeile: NEIN  Verbindlichkeit: normativ (Abschnitte 1–7), Erläuterung (Abschnitt 8)
  framework/core/09-risk-model.md           Statuszeile: NEIN  Verbindlichkeit: normativ (Abschnitte 1–4), Erläuterung (Abschnitt 5)
  framework/core/10-error-escalation.md     Statuszeile: NEIN  Verbindlichkeit: normativ (Abschnitte 1–4), Erläuterung (Abschnitt 5)
```

**Zur Messung selbst, weil sie die Falle dieses Repositoriums zweimal ausgelöst hat.** Der
erste Lauf meldete bei den Vorlagen „Kennungszelle: -" und bei den Kernmodulen
„Verbindlichkeit: -" – beides ist vorhanden. Ursache: Das Repositorium ist CRLF, und ein
auf `$` verankerter Ausdruck trifft dann nie, weil vor dem `\n` ein `\r` steht.
**Aufgefallen ist es nur, weil ein Strich nicht zur Erwartung passte** – wieder derselbe
billige Prüfstein, den dieses Projekt inzwischen kennt. Das Skript legt seither in `read()` auf LF flach.

## 3. Befund 1 – es sind dreizehn Skills, nicht zwölf; und 52 Nicht-Skills, nicht 57

| Behauptung der Vorbedingung | Gemessen |
|---|---|
| „57 der 69 Träger sind keine Skills" | **52.** Dazu vier Vorlagen (Abschnitt 6) und **13** Skills |
| „Für die zwölf Skills …" | **dreizehn.** Zwölf Framework-Skills unter `framework/skills/` und **einer** in einem Role Pack: `framework/role-packs/requirements-engineering/skills/role-re-ticket/SKILL.md` |

**Das ist genau die Abweichung, die Prüfung 46 bei Kriterium 2 schon berichtigt hat.** Dort
war „je Skill" als zwölf Testblätter gelesen worden, und das dreizehnte – das des
Role-Pack-Skills mit fünfzehn offenen Zellen – fehlte. **Die Vorbedingung zu Kriterium 3
hat denselben Fehler in derselben Woche wiederholt**, an derselben Datei, in derselben
Richtung.

Das Repositorium selbst zählt an anderer Stelle richtig: `CR-2026-071` belegt D-03 mit
„**13 von 13** Skills tragen genau die vier Dateien". **Die richtige Zahl stand also
bereits geschrieben, einen Antrag vorher.**

> **Wer hier eine Zahl liest, zählt sie besser nach – auch die eigene, und besonders die in
> der eigenen Übergabe.** Erneut, und diesmal gegen einen Wert, der aus derselben Woche
> stammt.

## 4. Befund 2 – die angenommene Kopplung besteht für den ersten Übergang nicht

Der Wortlaut des Lebenszyklusmodells (`framework/core/08-skill-conventions.md`
Abschnitt 7), Spalte *Voraussetzung für Übergang*:

| Status | Voraussetzung laut Modell |
|---|---|
| `entwurf` | – |
| **`pilot`** | **Testfälle vorhanden**, Validierung bestanden, Review durch Modul-Owner |
| `aktiv` | Pilotfeedback ausgewertet, **Positiv- und Negativtests bestanden**, Freigabe Framework Owner |

**„Bestanden" steht in der Zeile `aktiv`, nicht in der Zeile `pilot`.** Für den ersten
Übergang verlangt das Modell, dass Testfälle **existieren** – nicht, dass sie bestanden
sind. Die Vorbedingung hat die Zeile `aktiv` gelesen und den Übergang `entwurf → pilot`
damit begründet.

**Die Folge ist nicht klein.** Nach der Vorbedingung hätte Kriterium 3 auf keinem der 13
Skills bewegt werden können, solange Kriterium 2 offen ist – und Kriterium 2 ist der
größte Posten des ganzen Vorhabens (118 Zellen, mehrere Sitzungen, Modellkontingent). Nach
dem Wortlaut des Modells ist der Übergang **heute** möglich, ohne einen einzigen
Sitzungstest.

> **Zum zweiten Mal in zwei Releases war nicht die Aufgabe das Hindernis, sondern ihre
> Bedingung.** Bei `CR-2026-071` war die Bedingung falsch **gewählt**; hier ist sie falsch
> **gelesen**. Der Schaden ist derselbe: Ein Vorgang, der möglich war, sah unmöglich aus.

**Und die Kopplung, die tatsächlich besteht, ist die umgekehrte.** Für den Übergang nach
`aktiv` verlangt das Modell bestandene Tests. Kriterium 3 kann also für die Skills bis
`pilot` gehen, ohne Kriterium 2 zu berühren – **und nicht weiter**. Das ist kein Hindernis
dieses Vorgangs, sondern die Grenze des nächsten.

## 5. Die Abnahme der dreizehn Skills durch den Modul-Owner

Die dritte Voraussetzung für `pilot` ist ein **Review durch den Modul-Owner**. Owner ist
bei allen dreizehn `<FRAMEWORK_OWNER>` – bei zwölf wörtlich, bei `fw-repo-analyze` mit dem
Zusatz „(bis zur Benennung eines Modul-Owners)" (Steckbriefzeile *Owner (Rolle)*). Was
dieses Review ist und was es nicht ist, gehört benannt – sonst ist ein gehobener Status
eine Behauptung.

**Prüfgegenstände je Skill, alle am Bestand geprüft:**

1. **Die vier Dateien** nach D-03 – `SKILL.md`, `EXAMPLES.md`, `TESTS.md`, `CHANGELOG.md`.
2. **Die sieben Pflichtabschnitte** und die sieben Metadatenzeilen nach
   `08-skill-conventions.md` Abschnitte 2 und 4 – durchgesetzt vom Validator
   (`SKILL_SECTIONS`, `SKILL_META_KEYS`), Lauf grün.
3. **Frontmatter** nach D-08 und D-26: nur belegte Felder, `triggers: [user]` bei jedem
   schreibenden oder ausführenden Skill – durchgesetzt vom Validator.
4. **Testfälle vorhanden**, mit der Mindestzahl aus dem Skill-Standard: **jeder** der
   dreizehn trägt mindestens zwei Positiv- und drei Negativtests (gemessen: 29 Positiv- und
   58 Negativfälle, zusammen 87 – dieselben 87 Zellen, die Kriterium 2 als offen zählt).
5. **Versionsstand und Änderungsverlauf** stimmig – durchgesetzt vom Validator
   (Version nach SemVer, Eintrag in der `CHANGELOG.md` des Skills).
6. **Offene Verifikationsbedarfe benannt**, nicht beseitigt: zwei der dreizehn tragen einen
   `VERIFY`-Marker (`fw-mr-description`, `fw-review-support`).

| Skill | ID | Version | Modus | 4 Dateien | P/N | Marker | Urteil |
|---|---|---|---|---|---|---|---|
| `fw-repo-analyze` | `FW-SK-001` | 0.1.3 | M1 | ja | 2/3 | – | **pilotreif** |
| `fw-code-explain` | `FW-SK-002` | 0.1.3 | M1 | ja | 2/3 | – | **pilotreif** |
| `fw-change-analyze` | `FW-SK-003` | 0.1.2 | M1 | ja | 2/3 | – | **pilotreif** |
| `fw-plan` | `FW-SK-004` | 0.1.1 | M2 | ja | 2/4 | – | **pilotreif** |
| `fw-change-small` | `FW-SK-005` | 0.1.1 | M3 | ja | 2/5 | – | **pilotreif** |
| `fw-tests` | `FW-SK-006` | 0.1.1 | M4 | ja | 2/4 | – | **pilotreif** |
| `fw-refactor` | `FW-SK-007` | 0.1.1 | M3 | ja | 2/5 | – | **pilotreif** |
| `fw-error-analyze` | `FW-SK-008` | 0.1.3 | M1 | ja | 2/4 | – | **pilotreif** |
| `fw-bugfix-prepare` | `FW-SK-009` | 0.1.1 | M2 | ja | 2/4 | – | **pilotreif** |
| `fw-review-support` | `FW-SK-010` | 0.1.4 | M1 | ja | 2/5 | **2** | **pilotreif**, siehe unten |
| `fw-docs-update` | `FW-SK-011` | 0.1.2 | M5 | ja | 2/4 | – | **pilotreif** |
| `fw-mr-description` | `FW-SK-012` | 0.1.3 | M5 | ja | 2/4 | **1** | **pilotreif**, siehe unten |
| `role-re-ticket` | `RP-RE-SK-001` | 0.1.2 | M1 | ja | 5/10 | – | **pilotreif** |

### 5.1 Warum ein offener Marker den Übergang nach `pilot` nicht sperrt

Die drei offenen Marker der beiden Skills betreffen **nicht das Verhalten des Skills**,
sondern die Syntax beziehungsweise den Aufrufweg eines Clientmechanismus:

| Fundstelle | Gegenstand |
|---|---|
| `fw-mr-description/SKILL.md:78` | die Muster-Syntax der `permissions`-Regeln **im Skill-Frontmatter** |
| `fw-review-support/SKILL.md:77` | dieselbe Aussage, wörtlich gleich |
| `fw-review-support/SKILL.md:91` | der Aufrufweg des lesenden Subagentenprofils `fw-reviewer` **aus einem Skill heraus** |

Beide Stellen tragen den Zusatz „(Erläuterung)" beziehungsweise stehen in einem
Arbeitsschritt mit „KANN". **`pilot` heißt nach dem Modell „Nutzung in Pilotgruppe"** – ein
benannter, sichtbarer Verifikationsbedarf ist genau das, wofür eine Pilotnutzung da ist.
Ein Marker sperrt den Übergang nach `aktiv`, weil dort das Wort „Freigabe" steht; für
`pilot` verlangt das Modell ihn nicht, und ihn hier zu verlangen wäre dieselbe zu starke
Bedingung ein zweites Mal.

**Die drei Marker bleiben stehen und bleiben in Kriterium 1 gezählt.** Dieser Vorgang senkt
Kriterium 1 um nichts.

### 5.2 Was diese Abnahme nicht leistet, und es ist der wichtigere Satz

**Sie sagt nichts über das Verhalten.** Geprüft sind Struktur, Vollständigkeit,
Versionsstand und das Vorhandensein von Testfällen – alles Eigenschaften, die ein Skript
sehen kann, und alle vom Validator bei jedem Lauf gehalten. **Ob ein KI-Client nach diesen
dreizehn Anweisungen tatsächlich tut, was dort steht, ist unerhoben** – das sind die 87
offenen Ergebniszellen, und sie sind Kriterium 2.

Der Kopfkommentar der Prüfung 46 sagt es für genau diesen Fall voraus:

> Ein Modulstatus, der von `entwurf` auf `pilot` gehoben wird, ohne dass jemand das Modul
> angesehen hat, senkt Kriterium 3 um eins. Die fachliche Abnahme ist nicht maschinell.

**Angesehen ist jeder der dreizehn – an sechs benannten Gegenständen, nicht an einem
Gefühl.** Was die Prüfung nicht leisten kann, leistet diese Abnahme auch nicht: Sie ersetzt
keinen Sitzungstest. **Das ist der Unterschied zwischen `pilot` und `aktiv`, und deshalb
gibt es beide.**

## 6. Befund 3 – vier Träger sind keine Module, sondern Formulare

| Vorlage | Kennungszelle | Statuszelle | Ausfüllschlitze |
|---|---|---|---|
| `clients/_template/CLIENT_PACK.md` | `CP-<CLIENT_PACK_CODE>` | `entwurf` | 20 |
| `framework/role-packs/_template/ROLE_PACK.md` | `RP-<ROLE_PACK_CODE>` | `entwurf` | 5 |
| `framework/tech-packs/_template/TECH_PACK.md` | `TP-<TECH_PACK_CODE>` | `entwurf` | 7 |
| `templates/SKILL_TEMPLATE.md` | `<FW-SK-NNN / PRJ-SK-NNN / …>` | `entwurf` | 1 |

**Bei allen vier ist die Kennungszelle ein Platzhalter.** Der Steckbrief dieser Dateien
beschreibt nicht sie selbst, sondern **die Kopie, die aus ihnen entsteht**. Jede Vorlage
sagt das in ihrem Ausfüllhinweis ausdrücklich: *„Kopiere dieses Verzeichnis nach …,
ersetze alle Platzhalter"* beziehungsweise *„Dieser Kommentarblock und alle
`<…>`-Platzhalter werden beim Ausfüllen ersetzt oder entfernt."*

**Der Statuswert `entwurf` ist dort kein Platzhalter – und deshalb geht er unverändert in
jede Kopie über.** Das ist heute sogar das richtige Verhalten: Ein neues Pack beginnt im
Entwurf. Genau daraus folgt aber:

> **Die vier Vorlagen können ihren Entwurfsstatus nie verlassen.** Stünde dort `pilot`,
> wäre die erste Fassung jedes neuen Packs mit dem Anspruch ausgeliefert, eine
> Pilotgruppe könne damit arbeiten – eine Zusage, die das Formular über eine Datei macht,
> die es noch nicht gibt.

**Damit ist Kriterium 3 in der heutigen Zählung unerreichbar.** Und das ist nicht irgendein
Mangel: **D-11 ist genau deshalb entstanden.** Seine Begründung sagt über den Vorgänger
D-09:

> D-09 koppelte die Aussagefähigkeit des Frameworks an Rollen und einen Realbetrieb
> außerhalb seines Verantwortungsbereichs und machte das Release-Gate FW-CL-11 dadurch
> **unerreichbar**; die neuen Kriterien sind **prüfbar** und liegen im Einflussbereich des
> Framework Owners.

**Ein Kriterium, dessen Gegenstand vier Zeilen enthält, die sich nie ändern dürfen, ist
derselbe Defekt, den D-11 beseitigt hat** – nur zwei Größenordnungen kleiner und deshalb
seit der Erstfassung unbemerkt.

### 6.1 Die Auflösung liegt am Gegenstand, nicht an der Zählregel

Zwei Wege wären möglich, und nur einer ist ehrlich:

| Weg | Wirkung | Bewertung |
|---|---|---|
| Die Zählregel nimmt Vorlagen aus | Kriterium 3 sinkt um 4, im Bestand ändert sich nichts | **Verworfen.** `CR-2026-070` E6 hat die Zählung ausdrücklich auf den **ganzen** Bestand gestellt, weil ein Kriterium nicht klein werden soll, indem es einen Teil seines Gegenstands nicht ansieht. Eine Ausnahme dafür wäre dieselbe Bewegung mit umgekehrtem Vorzeichen |
| Die Statuszelle der Vorlage wird ein Ausfüllschlitz | Kriterium 3 sinkt um 4, **weil vier falsche Treffer entfallen**; die Vorlage verlangt die Entscheidung künftig ausdrücklich | **Gewählt.** Es ist keine Ausnahme von der Regel, sondern die Beseitigung eines Gegenstands, der nie einer war – und die Zelle kommt in die Form, in der jede andere Zelle desselben Steckbriefs schon steht |

**Der Preis des gewählten Wegs, benannt:** Wer eine Vorlage kopiert und den Schlitz nicht
füllt, hat ein Pack ohne Statuswert. Bei einem Skill fängt das der Validator
(`SKILL_STATUS`, unbekannter Wert ist ein Fehler); **bei Client-, Role- und Technology-Pack
fängt es heute nichts** – siehe Abschnitt 9.

## 7. Befund 4 – für die 52 Nicht-Skill-Träger fehlt jede Übergangsbedingung

Dieser Teil der Vorbedingung stimmt, und er ist nach Abzug der Vorlagen kleiner als
behauptet: **52 Träger, nicht 57.**

Was sie sind: elf Checklisten, zwölf Prompts, sechs Entscheidungsbäume, sieben
Governance-Dokumente, drei `docs/`-Dokumente, zwei `tests/`-Register, vier
Onboarding-Dokumente, zwei `pilot/`-Dokumente, drei Client-Pack-Dokumente und zwei
Role-Pack-Steckbriefe. **Für keinen von ihnen nennt das Framework eine Bedingung, um
`entwurf` zu verlassen.**

`framework/core/01-governance.md` Abschnitt 3 Punkt 4 sagt heute:

> Skills durchlaufen den Lebenszyklus `entwurf → pilot → aktiv → veraltet → zurückgezogen`
> (`08-skill-conventions.md`).

**Der Satz ist richtig und vollständig – und genau das ist der Befund.** Das Framework
kennt einen Lebenszyklus für Skills und vergibt Statuswerte an 52 weitere Träger, für die
er nicht gilt. Die Statuszelle dieser 52 ist damit **eine Angabe ohne Regel**: Sie sagt
etwas aus, aber es gibt keinen Satz, gegen den man prüfen könnte, ob sie stimmt.

> **Der wiederkehrende Befundtyp dieses Repositoriums ist eine Zusage ohne Mechanismus.
> Hier ist es ein Feld ohne Vokabular** – die Statuszelle behauptet einen Lebenszyklus, den
> das Modul nicht hat.

## 8. Befund 5 – beide naheliegenden mechanischen Bedingungen taugen nicht

Wenn 52 Träger eine Bedingung brauchen, ist die erste Frage, ob sie maschinell prüfbar
sein kann. Zwei Kandidaten liegen auf der Hand. **Beide sind versucht und beide fallen
durch, aus demselben Grund.**

### 8.1 „Keine offenen `<TBD:>`-Schlitze"

29 der 69 Träger enthalten mindestens einen. Gelesen zeigt sich: **`<TBD:` trägt in diesem
Bestand drei verschiedene Bedeutungen.**

| Rolle | Beispiel | Ist es eine Lücke des Framework Owners? |
|---|---|---|
| **Anweisungstext eines Skills** | `fw-mr-description/SKILL.md`: „nicht belegbare Felder als `<TBD: …>`" – elf Fundstellen, alle normativer Inhalt | **nein**, das ist der Inhalt der Regel |
| **Ausfüllschlitz einer Vorlage** | `clients/_template/CLIENT_PACK.md`, 20 Fundstellen | **nein**, das ist der Zweck der Datei |
| **Echte Lücke** | `checklists/09-onboarding.md`: `<TBD: Referenz auf Unterweisung>` | **nein – es ist eine Lücke der aufnehmenden Organisation**, und D-11 nimmt die ausdrücklich aus |

**Keine der drei Rollen taugt als Sperre**, und die dritte ist die interessanteste: Sie ist
eine echte offene Stelle, aber sie liegt außerhalb des Einflussbereichs, den D-11 zum
Maßstab macht. Eine Bedingung „keine `<TBD:>`" hätte 29 Träger gesperrt, davon keinen
zu Recht.

### 8.2 „Kein offener `VERIFY`-Marker"

Neun der 69 Träger enthalten einen. Gelesen zeigt sich: **vier von ihnen benennen den
Marker, statt ihn zu tragen.**

| Fundstelle | Was dort steht |
|---|---|
| `checklists/11-framework-release.md:40` | der Prüfpunkt, der die Marker beim Release aktualisiert |
| `clients/README.md:67` | die Regel, dass eine unbelegte `[TECHNISCH]`-Zeile den Marker trägt |
| `governance/RELEASE_PROCESS.md:46` | der Schritt der Produktbeobachtung |
| `docs/ROADMAP.md:1878` | das Ziel von AP2 |

**Das ist die Lehre E3 von `CR-2026-070` eine Ebene tiefer.** Dort war bemerkt worden, dass
Kriterium 1 die Register- und Glossarzeilen des Markers mitzählt und deshalb ein **Pegel**
ist, kein Arbeitsvorrat. Hier hätte dieselbe Eigenschaft vier Träger gesperrt, die nichts
zu verifizieren haben – darunter ausgerechnet die **Release-Checkliste** und den
**Release-Prozess**.

### 8.3 Was daraus folgt

> **Eine Marke, die in einem Bestand sowohl benutzt als auch benannt wird, taugt nicht als
> Bedingung.** Beide Kandidaten scheitern nicht an ihrer Strenge, sondern daran, dass sie
> eine Zeichenkette zählen, wo ein Urteil gefragt ist.

Die Übergangsbedingung für die 52 Nicht-Skill-Träger muss deshalb **ein Review durch den
Modul-Owner** enthalten, so wie das Skill-Modell es auch tut. Was daneben maschinell prüfbar
bleibt, ist nur: **dass der Statuswert aus dem Vokabular stammt** und **dass die Zahl in
der Standzeile stimmt** – das Zweite leistet Prüfung 46 schon, das Erste heute nur für
Skills.

## 9. Nebenbefund – das Statusvokabular ist für 13 von 69 Trägern durchgesetzt

`tests/scripts/validate-framework.py` führt `SKILL_STATUS = {"entwurf", "pilot", "aktiv",
"veraltet", "zurückgezogen"}` und meldet jeden anderen Wert als Fehler – **aber nur in
einer `SKILL.md`**. Für die übrigen 56 Träger ist jede Zeichenfolge zulässig; `| Status |
banane |` bliebe unbemerkt. Genau dieser Fall ist für Skills bis 0.12.0 offen gestanden und
mit `FW-VN-01` geschlossen worden – **für die anderen Ablagen nie.**

**Solange kein Nicht-Skill gehoben ist, hat das keinen Gegenstand.** Mit dem ersten
gehobenen Nicht-Skill hat es einen, und dann ist die Prüfung fällig. Sie gehört in dieses
Release **nicht**: Es hebt ausschließlich Skills, und für die ist das Vokabular
durchgesetzt.

## 10. Nebenbefund – die elf Kernmodule tragen keine Statuszeile, und die Release-Checkliste verlangt eine

`framework/core/` enthält elf normative Module. **Keines trägt eine Statuszeile**; sie
führen stattdessen die Zeile *Verbindlichkeit*. Prüfung 46 zählt sie deshalb nicht – das
ist seit 0.48.0 bekannt und stand dort als „`framework/core/` war genannt und trägt gar
keine Statuszeile".

**Neu ist, was daneben liegt.** `checklists/11-framework-release.md` führt unter *Abschluss*
den Prüfpunkt:

> - [ ] **MUSS** (ab 1.0.0, D-11) Alle **Core-Module**, Skills und Packs tragen einen
>   Status oberhalb von `entwurf`.

**Das Release-Gate verlangt für die elf Kernmodule einen Statuswert, den es dort nicht
gibt.** Ein Prüfpunkt ohne Gegenstand – und zwar in der Checkliste, die das 1.0.0-Release
freigibt.

**Die Frage ist nicht nebenbei zu beantworten**, und dieses Release beantwortet sie
ausdrücklich nicht:

- Tragen die elf Kernmodule künftig eine Statuszeile, **wächst Kriterium 3 von 52 auf 63** –
  in einem Vorgang, dessen Auftrag es ist, die Zahl zu senken. Das wäre richtig und sähe
  falsch aus.
- Tragen sie keine, **muss der Prüfpunkt der Release-Checkliste umformuliert werden**, und
  „alle Modulstatus" in D-11 bedeutet dann ausdrücklich: alle, die einen führen.
- **Beides ist vertretbar, keines von beiden steht heute da.** Als `K-36` aufgenommen.

### 10.1 Und der Auftrag selbst meint etwas anderes als der Zähler

`AP3` nennt als Ziel *„Core-Module fachlich abgenommen (Status je Modul von `entwurf` auf
`pilot`)"* und als Aktivität *„Review aller `leitwerk-core/framework/core/`-Module"*.

**Der Gegenstand dieser Aktivität sind also genau die elf Module, die keine Statuszeile
führen** – und **keiner** der 69 Träger, die Prüfung 46 zählt, liegt unter
`framework/core/`. Die beiden Mengen sind **disjunkt**.

| Gegenstand | Menge | Statuszeile |
|---|---|---|
| `AP3`, Aktivität „Status je Modul" | die **elf** Module unter `framework/core/` | **keine** |
| D-11, Kriterium 3 (Prüfung 46) | **69** Träger in zehn anderen Ablagen | ja |

**Was daraus folgt, und es ist eine Einschränkung dieses Releases:** Was hier gehoben wird,
senkt **Kriterium 3 von D-11**. **`AP3` ist damit nicht weiter** – seine Aktivität hat einen
Gegenstand, der bis zur Entscheidung über `K-36` gar keinen Statuswert kennt. Die Roadmap
sagt das ab diesem Release ausdrücklich, statt einen Fortschritt zu suggerieren.

## 11. Nebenbefund – das Hauptdokument nennt für alle zwölf Skills die Version 0.1.0

`build/doc/20-referenz-skills.md` sagt:

> Alle Skills liegen im Status `entwurf` (Version 0.1.0, Owner `<FRAMEWORK_OWNER>`) und
> durchlaufen den Lebenszyklus aus Kapitel 18.

**Die Versionsangabe ist für alle zwölf falsch** – gemessen stehen sie auf 0.1.1 bis 0.1.4.
Die Statusangabe wird mit diesem Release falsch. Dazu `build/doc/00-kopf.md`: *„Alle Module
im Status `entwurf`"*.

**Berichtigt wird hier keiner der Sätze, und der Grund ist eine Zahl:** Derselbe Steckbrief
nennt *Dokumentversion 0.9.0, Stand 2026-09-10*. Das Hauptdokument ist **zweiundvierzig
Releases** hinter dem Kern. Zwei Sätze darin nachzuziehen würde einen aktuellen Stand
behaupten, den das Dokument nicht hat – **und das ist der Befundtyp dieses Repositoriums in
Reinform.** Die Lehre von 0.45.0 gilt hier wörtlich: *„Eine Anweisung, die die halbe
Migration beschreibt, ist gefährlicher als keine."*

**Der Vorgang dazu steht in der Roadmap als P3 („Word-Fassung erzeugen") und bekommt mit
diesem Release eine benannte Pflicht:** Beim Bau ist der Steckbrief von `00-kopf.md` und
der Absatz in `20-referenz-skills.md` gegen den dann geltenden Stand zu setzen. Dass
niemand den Abstand bemerkt hat, liegt daran, dass ihn nichts nachrechnet – ein
Prüfkandidat, und er ist es nicht wert, bevor eine der vier Zahlen weiter gefallen ist.

## 12. Nebenbefund – die Versionszelle der Vorlagen hat dieselbe Bauform wie die Statuszelle

Die vier Vorlagen tragen `Version 0.2.0`, `0.1.1`, `0.1.0` und `0.1.2`. Auch dieser Wert
**geht in die Kopie über**, und für ein neues Pack ist er falsch: Es beginnt bei `0.1.0`.
Bei `templates/SKILL_TEMPLATE.md` ist die Folge greifbar – ein daraus erzeugter Skill trägt
`0.1.2` und braucht dafür einen Eintrag in einer `CHANGELOG.md`, die es noch nicht gibt;
der Validator verlangt ihn.

**Anders als bei der Statuszelle ist hier nicht entschieden, wessen Wert das ist:** Die
Versionen 0.1.1 und 0.1.2 sehen gepflegt aus, also führt die Vorlage sie womöglich als
**ihre eigene**. Dann wäre die Zelle doppelt belegt – eigene Angabe und Formularfeld
zugleich.

**Nicht angefasst.** Der Gegenstand dieses Antrags ist der Modulstatus; die Frage, welche
Steckbriefwerte einer Vorlage ihr selbst gehören, ist eine eigene und als `K-37`
aufgenommen. **Sie gehört nicht in einen Nebensatz** – dieselbe Begründung, mit der
`CR-2026-070` die Ableitung der Gegenprobensummen abgelehnt hat.

## 13. Was diese Gegenprüfung nicht leistet

- **Sie beantwortet K-36 und K-37 nicht.** Beide sind benannt, keiner ist entschieden.
- **Sie sagt nichts über das Verhalten der dreizehn Skills.** Siehe Abschnitt 5.2.
- **Sie hebt keinen der 52 Nicht-Skill-Träger.** Sie stellt die Bedingung auf, unter der es
  möglich wird; die Abnahme je Träger ist Arbeit des nächsten Vorgangs, und sie ist nicht
  maschinell.
- **Sie senkt Kriterium 1 und Kriterium 2 um nichts.** Die drei offenen Marker der beiden
  Skills bleiben stehen, die 87 offenen Zellen bleiben offen.
- **Sie hat den Abstand des Hauptdokuments gemessen, nicht verkleinert** (Abschnitt 11).
- **Sie bringt `AP3` nicht weiter.** Dessen Aktivität meint die elf Module unter
  `framework/core/`, und die führen keine Statuszeile (Abschnitt 10.1).

## 14. Bewertung

**Von den drei Behauptungen der Vorbedingung sind zwei falsch und eine richtig.**

| Behauptung | Urteil |
|---|---|
| „57 der 69 Träger sind keine Skills" | **falsch** – 52, dazu vier Vorlagen und 13 Skills |
| „Für die zwölf Skills verlangt das Modell Testfälle bestanden, also sind Kriterium 2 und 3 gekoppelt" | **falsch** – „bestanden" verlangt erst `aktiv`; für `pilot` genügt „vorhanden". Die Kopplung besteht für den ersten Übergang nicht |
| „Für die Nicht-Skills gibt es keine niedergeschriebene Bedingung" | **richtig**, und sie ist der eigentliche Gegenstand der Vorentscheidung |

**Die Wirkung auf Kriterium 3 ist damit heute messbar und nicht klein:** 69 → 52, ohne
einen Sitzungstest, ohne Modellkontingent und ohne eine einzige Zusage, die nicht am
Bestand belegt ist.

| Posten | Träger |
|---|---|
| Stand vor diesem Release | **69** |
| dreizehn Skills auf `pilot` (Abschnitt 5) | **−13** |
| vier Vorlagen: Statuszelle wird Ausfüllschlitz (Abschnitt 6) | **−4** |
| **Stand nach diesem Release** | **52** |

> **Die Lehre, die über diesen Fall hinausgeht.** Mit 0.49.0 hat dieses Repositorium
> gelernt, dass es seine Zusagen prüft und seine Bedingungen nicht. Der Satz ist eine
> Woche alt, und schon der nächste Vorgang bringt den Beweis nach: **Die Bedingung, die
> ihm vorangestellt war, enthielt drei Behauptungen, und zwei hielten nicht.** Beide Male
> war die Aufgabe leichter als ihr Vorzeichen.
>
> **Eine Bedingung, die niemand nachzählt, ist eine Zusage mit umgekehrtem Vorzeichen.**
