# Änderungsantrag `CR-2026-018`

| Feld | Inhalt |
|---|---|
| Titel | Die Quellenliste belegte die `[DOK]`-Aussagen nur eines Clients |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | `build/doc/31-anhaenge.md`; `clients/claude-code/CLIENT_PACK.md`; `clients/README.md`; `tests/protocols/2026-09-10-AP2-claude-code.md` |
| Ebene laut Entscheidungsbaum 6 | Dokumentation und Abbildungsschicht; keine Regelebene |
| Art | Fehlerbehebung (Belegkette), Vorarbeit zu `FW-AK-01` |
| Dringlichkeit | regulär |

## 1. Anlass und Problem

Anhang 31.4 des Hauptdokuments sagt über sich selbst: „Die Quellen belegen die als `[DOK]`
gekennzeichneten Aussagen; der Framework Owner hält diese Liste im Rahmen der Produktbeobachtung
aktuell (`FW-AK-01`)." Die Liste führte **17 Quellen, sämtlich von `docs.devin.ai`.**

Seit Release 0.14.0 trägt das Client Pack `claude-code` ein Dutzend `[DOK]`-Aussagen, die gegen
`code.claude.com/docs/en/*` erhoben wurden. **Keine dieser Quellen stand in der Liste.** Für
einen der beiden Clients löste der Anhang seine eigene Zusage nicht ein – und `FW-AK-01`, dessen
Prüfgegenstand genau diese Liste ist, hätte den fehlenden Teil nicht prüfen können, weil er nicht
da war.

Zwei kleinere Befunde kamen beim Abgleich dazu:

**Die Belegspalte der Fähigkeitsmatrix nannte keine Fundstelle.** Zwölf Zeilen trugen `[DOK]
(AP2, Clientversion 2.1.267, tests/protocols/…)`. Das nennt den **Vorgang**, nicht die **Quelle**.
Wer eine einzelne Einstufung nachprüfen wollte, musste erst das Protokoll lesen, um zu erfahren,
auf welcher der fünf Seiten die Aussage steht. D-25 hatte für Versionsangaben denselben
Unterschied herausgearbeitet: Eine Angabe, die man nicht gegen etwas halten kann, ist keine.

**Die Kennungen `Q1` bis `Q17` waren doppelt belegt.** Dieselben Kürzel bezeichnen im Framework
an rund zwanzig Stellen – in Checklisten, Entscheidungsbäumen und im Änderungsverzeichnis – die
**Qualitätsregeln**: `Q8` ist dort die Größenschwelle einer Änderung, im Anhang dagegen
`docs.devin.ai/desktop/cascade/workflows`.

## 2. Vorgeschlagene Änderung

**Anhang 31.4 wird je Client Pack geführt.** Das ist keine Gliederungsfrage: Eine Aussage über
einen Client hängt an dessen Dokumentation und an keiner anderen, und die beiden Listen haben
verschiedene Recherchestände – `devin-desktop` 01.–02.09.2026 gegen Produktversion 3.8.20,
`claude-code` 10.09.2026 gegen Clientversion 2.1.267.

**Fünf Quellen kommen dazu** (`QC-1` bis `QC-5`): `docs/en/memory`, `permissions`, `skills`,
`sub-agents` und `settings`. Je Quelle steht, was sie belegt.

**Die Kennungen tragen das Präfix des Packs** – `QD-` und `QC-`. Zwei Bedeutungen desselben
Kürzels in einem Dokument sind eine Verwechslung ohne Nutzen. Die Quellenkennungen werden
außerhalb des Anhangs nirgends referenziert; die Umbenennung bricht keinen Verweis.

**Die Belegspalte der Fähigkeitsmatrix nennt die Seite**, etwa ``[DOK] `docs/en/memory` (AP2,
Clientversion 2.1.267, …)``. Damit ist jede Zeile einzeln nachprüfbar, ohne den Umweg über das
Protokoll. Die Seitennamen stehen im Pack, die vollständige Belegzuordnung im Anhang – das Pack
bleibt für sich lesbar, ohne die Zuordnungstabelle zu verdoppeln.

**Ein neuer Abschnitt 31.4.3 sagt, was die Liste über sich selbst weiß:** dass die beiden
Recherchestände neun Tage auseinanderliegen, dass nur der jüngere gegen eine benannte
Clientversion erhoben ist, und dass `FW-AK-01` deshalb `offen` bleibt.

**Was verworfen wurde:**

- **Die Quellenliste ganz in die Client Packs verlegen.** Naheliegend nach dem Muster von 31.5
  („der maßgebliche Verifikationsbedarf steht in der Fähigkeitsmatrix"), aber die Liste ist mehr
  als eine Zuordnung: Sie trägt Abrufdatum und Produktstand und ist damit das Artefakt, gegen das
  `FW-AK-01` prüft. Ein Testfall braucht **einen** Prüfgegenstand, nicht je Pack einen.
- **Die Seitennamen nur im Anhang führen und im Pack bei „AP2" belassen.** Ein Pack wird in ein
  Projekt installiert, das Hauptdokument nicht. Eine Belegangabe, die erst in einem anderen
  Dokument auflösbar ist, hilft dort niemandem.
- **Die Quellenkennungen `QC-1` bis `QC-5` auch im Pack verwenden.** Dann müsste die Zuordnung
  Kennung → Seite in beiden Dokumenten stehen – genau die Doppelpflege, die D-16, D-17 und D-20
  beseitigt haben. Der Seitenname ist ohne Nachschlagen lesbar und dafür die bessere Angabe.

## 3. Nebenbefunde aus dem Abgleich

Der Abgleich hat drei Einstufungen genauer belegt und eine offene Frage aufgeworfen. Alle vier
sind Nachträge zu bestehenden Zeilen, keine neuen Zusagen.

| Zeile | Was dazukommt | Quelle |
|---|---|---|
| H2 | Ein mit Exit-Code 2 blockierender Hook greift **bevor** die Berechtigungsregeln ausgewertet werden – er geht damit auch einer `allow`-Regel vor. Umgekehrt hebt eine Hook-Entscheidung keine `deny`- oder `ask`-Regel auf | `QC-2` |
| A1 | `disallowedTools` wird **zuerst** angewandt, dann `tools` gegen den Rest aufgelöst. Ein Profil, dessen `tools`-Liste sich zu keinem Werkzeug auflöst, wird gar nicht erst gestartet – ein Tippfehler führt zum Abbruch, nicht zu einem Subagenten ohne Beschränkung | `QC-4` |
| S4 | `disable-model-invocation: true` hält zusätzlich die Beschreibung des Skills aus dem Kontext – ein Gewinn für Least Context, nicht nur für die Zusage | `QC-3` |
| M2 | **AP2-CC-12 (offen):** Ein Subagentenprofil kennt ein eigenes Feld `permissionMode`, das den Wert `bypassPermissions` annimmt. Ob `disableBypassPermissionsMode` auch dort greift, sagt keine der fünf Seiten. M2 gilt damit für die Hauptsitzung als belegt und für den Weg über ein Subagentenprofil als ungeklärt | keine – Belegfrage |

Die Einstufung von M2 bleibt `[TECHNISCH]`: Die Sperre ist dokumentiert und wirkt aus jeder
Einstellungsebene. Offen ist eine **Teilfrage**, und sie steht als solche in der Zeile. Das
Framework liefert genau ein Subagentenprofil aus (`fw-reviewer`), und es setzt das Feld nicht.

## 4. Prüffragen (durch Owner auszufüllen)

- [x] Richtige Ebene nach Entscheidungsbaum 6? — Ja. Geändert werden ein Kapitel des Hauptdokuments und die Belegspalte eines Client Packs. Keine Regel wird eingeführt, keine gelockert; keine Einstufung ändert sich.
- [x] Verschärfungsprinzip eingehalten? — Nicht berührt. Die Änderung fügt Belege hinzu und nimmt keinen weg.
- [x] Widerspruchsfreiheit geprüft? — Der Widerspruch war der Anlass: Der Anhang behauptete, die `[DOK]`-Aussagen zu belegen, und tat es für einen Client nicht. Zusätzlich beseitigt: die Doppelbelegung der Kennungen `Q1` bis `Q17`.
- [x] Laufzeitfassungen betroffen? — Nein. Weder Installation noch Validator ändern sich; `install.py --check` und der Validator laufen unverändert.
- [x] Belegstatus korrekt? — Das ist der Gegenstand. Jede neue Zeile nennt Seite und Abrufdatum; die Nebenbefunde sind mit der Seite belegt, aus der sie stammen. AP2-CC-12 ist ausdrücklich als **ungeklärt** geführt und nicht als Befund.
- [x] Test- und Validierungsbedarf? — Keine Sonde: Die Änderung fügt keine Prüfung hinzu und ändert keine. `FW-AK-01` bleibt `offen`; für `claude-code` ist der Abgleich mit diesem Release geführt, für `devin-desktop` steht er aus.
- [x] Auswirkungen auf Overlays und laufende Onboardings? — Keine.
- [x] Dokumentation? — CHANGELOG, Roadmap, Client Pack, AP2-Protokoll, `clients/README.md`.

## 5. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | angenommen |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Die Belegkette ist der Kern dessen, was das Framework über sich behauptet: `[DOK]` heißt „in der Herstellerdokumentation beschrieben", und wenn nicht auffindbar ist, **wo**, ist das eine Behauptung mit Fußnote. Dass die Liste über zwei Releases hinweg nur einen der beiden Clients kannte, ist derselbe Befundtyp wie `AP2-CC-09`: eine Zusage, die niemand gegen ihren eigenen Gegenstand gehalten hat. |
| Ziel-Release | 0.16.0 |
| Decision-Log-Eintrag | keiner – die Änderung führt keine neue Festlegung ein, sondern löst eine bestehende ein (D-12, D-14, D-25) |

## 6. Umsetzung (nach Annahme)

- [x] Anhang 31.4 je Client Pack gegliedert; `QC-1` bis `QC-5` aufgenommen; Kennungen auf `QD-`/`QC-` umgestellt
- [x] Abschnitt 31.4.3: was die Liste über ihre eigenen Recherchestände weiß
- [x] Belegstand in 31.5 nachgezogen (die Angabe „9 von 26 bei `claude-code`" war seit AP2 überholt)
- [x] Belegspalte der Fähigkeitsmatrix nennt je Zeile die Seite; Hinweis dazu am Kopf von Abschnitt 2
- [x] Nebenbefunde zu H2, A1 und S4 in die Matrix übernommen; AP2-CC-12 in Pack und Protokoll aufgenommen
- [x] Quellenzeile des AP2-Protokolls berichtigt: die Seite heißt `sub-agents`, nicht `subagents`
- [x] Validator 0 Fehler, 0 Warnungen; `install.py --check` unverändert; Hauptdokument baut für beide Packs
- [ ] **Folgearbeit:** `FW-AK-01` bleibt `offen`. Die Hälfte `devin-desktop` verlangt einen Abgleich der Quellen `QD-1` bis `QD-17` und des Produkt-Changelogs; der Recherchestand ist der 02.09.2026
- [ ] **Folgearbeit:** AP2-CC-12 klären. Ohne Sitzung nur über die Dokumentation zu Subagenten und verwalteten Einstellungen zu beantworten
