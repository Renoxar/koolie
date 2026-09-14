# Gegenprüfung: „Skills werden nicht bevorzugt" – die Erkennung war nie das Problem

| Feld | Wert |
|---|---|
| Gegenstand | Externer Bericht `skill-priority-improvement.md` vom 2026-09-14 (Devin Desktop am Piloten `otp-generator`): Die Agenten folgten der Skill-Bevorzugung des Frameworks nicht |
| Verfahren | D-23: Vor der Umsetzung gehört jeder Befund gegengeprüft |
| Datum | 2026-09-14 |
| Framework-Version | 0.40.0 (`00b534b`) |
| Methode | Textanalyse der fünf Träger im Repositorium; elf Messungen an einer vollständigen Installation (`2026-09-14-erhebung-skillaufruf.md`) |
| Ergebnis | **Bestätigt, mit umgekehrter Ursache und einem zweiten Befund, den der Bericht nicht nennt** |

## 0. Der Zusammenhang in einem Satz

Der Bericht sagt, der Agent *erkenne* den passenden Skill nicht und rufe ihn deshalb nicht
auf. Gemessen ist beides: Er erkennt ihn in der Hälfte der Läufe **nicht** – und wo er ihn
erkennt und aufruft, **weist die Berechtigungsdatei des Frameworks den Aufruf ab**. Der Bericht
sieht den ersten Fall und hält ihn für den einzigen.

## 1. Was der Bericht behauptet und was davon trägt

| Behauptung | Gegenprüfung |
|---|---|
| „**Keine automatische Skill-Erkennung:** Die Agent-Logik prüft nicht aktiv, ob ein Skill für die aktuelle Aufgabe verfügbar ist" | **Zur Hälfte widerlegt.** In zwei von vier Läufen rief die Sitzung den passenden Skill auf, ohne dass die Aufgabe ihn nannte (A1, A3). In den beiden anderen benannte sie ihn im Bericht und hielt den Aufruf für entbehrlich (A2) oder erwähnte ihn gar nicht (A4) |
| „**Fehlende Validierung:** Es gibt keinen Mechanismus, der die Einhaltung der Skill-Bevorzugung überprüft" | **Bestätigt** – und der Grund ist ein anderer als vermutet: Der Ergebnisbericht fragt nach „Verwendete Skills", nie danach, ob der Aufruf gelungen ist. Ein abgewiesener Aufruf erscheint dort als Verwendung (Lauf A3) |
| „Es gibt **keinen Preflight-Check-Punkt**, der die Skill-Verwendung vor Aufgabenausführung verlangt" | **Falsch.** `checklists/01-preflight.md:39` trägt ihn – als **SOLL** und adressiert an „Bearbeiterin oder Bearbeiter", nicht an den Agenten |
| Zitat der Systemanweisung des Clients (*„invoke it immediately"*) als Framework-Regel | **Kategorienfehler.** Nach Abschnitt 2 der Wurzel-Anweisungsdatei hat eine Ablage außerhalb des Repositoriums **keine Ebene dieser Hierarchie**. Sie darf einschränken, nie erweitern – und sie begründet keine Framework-Pflicht |
| Empfehlung **Option 1**: „Bei Übereinstimmung Skills automatisch aufrufen", „Agent-Logik anpassen" | **Außerhalb der Reichweite.** Leitwerk ändert keine Agentenlogik; es liefert Regeltexte, Skills, eine Berechtigungsdatei und einen Hook. Ein Antrag, der die Agentenlogik ändern will, ist in diesem Projekt kein Antrag, sondern eine Anforderung an den Hersteller |
| Erfolgskriterium „Skills werden in ≥ 95 % der Fälle automatisch verwendet" | **Nicht messbar mit den Mitteln dieses Projekts** – und eine Zahl, deren Grenze Ermessen ist, ist nach der eigenen Lehre keine Zahl. Was sich messen lässt, ist der **Mechanismus**, nicht die Quote |

**Was am Bericht richtig ist und nicht verworfen gehört:** Das beobachtete Verhalten ist real,
es reproduziert sich, und es reproduziert sich **besonders bei der Aufgabenform, die der
Bericht beschreibt** – die Planungsaufgabe zog in keinem Lauf einen Skill. Seine
Lösungsvorschläge 2 und 3 zielen in die richtige Richtung. Nur seine Ursachenanalyse trägt
nicht, und sein empfohlener Vorschlag ist der einzige der drei, der sich nicht bauen lässt.

## 2. Befund 1: Die Skillwahl steht an fünf Stellen und erreicht den Agenten nirgends verbindlich

| Träger | Wortlaut | Verbindlichkeit | Adressat |
|---|---|---|---|
| `framework/core/06-prompting-rules.md:34` | „**Skills bevorzugen.** Liegt für eine Aufgabe ein Skill vor, **wird er verwendet**" | normativ | Das Modul regelt den **Aufbau einer Aufgabenanweisung** – also den Menschen. Das Passiv lässt offen, wer handelt |
| `checklists/01-preflight.md:39` | „Passender Skill gewählt (`/fw-…`)" | **SOLL** | „Bearbeiterin oder Bearbeiter", „vor dem ersten Prompt" |
| `framework/core/05-working-model.md` Abschnitt 1 | Skill in der Spalte **Referenz**, bei sechs der vierzehn Schritte | – | Die Spalte ist keine Pflichtspalte; verbindlich ist „Mindestinhalt" |
| `framework/runtime/root-instruction.md` Abschnitt 17 | „Nutze für **Standardaufgaben** die Skills unter `<SKILLS_DIR>/`" | **ohne Marke** | Agent – letzter von 17 Abschnitten |
| `framework/runtime/rules/00-framework-core.md` (always-on) | nennt Skills **nur** in der Aufzählung des Ergebnisberichts | – | Agent – die **Wahl** kommt dort nicht vor |

**Drei Beobachtungen, jede für sich tragend:**

1. **Die stärkste Formulierung steht im Modul für den Menschen.** Regel 7 ist normativ und
   eindeutig – und sie steht in `06-prompting-rules.md`, dessen Abschnitt 1 mit „Jede Anweisung
   an den KI-Client" beginnt. Wer sie als Agentenpflicht zitiert, zitiert eine Regel über das
   Schreiben von Prompts.
2. **Die einzige agentenseitige Stelle trägt keine Verbindlichkeitsmarke.** Die
   Wurzel-Anweisungsdatei führt **null** Vorkommen von MUSS, SOLL oder KANN – das ist ihre
   Bauform und kein Fehler. Abschnitt 17 hat deshalb kein Mittel, sich von einer Empfehlung zu
   unterscheiden, und nutzt keines.
3. **Der Auslöser ist undefiniert.** Das Wort „Standardaufgaben" kommt im ganzen Kern kein
   zweites Mal vor. Es gibt keine Liste, keinen Verweis und keinen Schritt, an dem die Prüfung
   fällig wäre.

**Die always-on-Schicht ist der Träger, der fehlt.** Der Entlastungslauf G1 belegt, dass sie
die Sitzung ohne Werkzeugaufruf erreicht. Sie führt die vierzehn Schritte, den Satz „Schritte
werden nicht übersprungen" und die Pflicht zum Ergebnisbericht – und zur Skillwahl schweigt
sie.

## 3. Befund 2: Der Bericht sieht die Mechanik nicht, und sie ist der schwerere Teil

Der zweite Befund steht nicht im Bericht und ist gemessen
(`2026-09-14-erhebung-skillaufruf.md`, Abschnitte 3 bis 5):

- Der Skillaufruf ist bei `claude-code` ein **eigener Werkzeugaufruf** mit dem Namen `Skill`.
- Die ausgelieferte Berechtigungsdatei kennt ihn in **keinem** Korb und lässt ihn auf die
  Rückfrage fallen; im rückfragefreien Betrieb ist das eine Abweisung.
- Die Ursache liegt eine Ebene tiefer: Das Werkzeugvokabular der Kernquelle führt sechs Verben
  und **keines für den Skillaufruf**. Eine Freigabe war in dieser Datei nie ausdrückbar.
- Der Rückfall – `SKILL.md` als Datei lesen und den Ablauf von Hand nacharbeiten – ist **von
  einem gelungenen Lauf nicht zu unterscheiden** und **verliert die Werkzeugbeschränkung des
  Skills** (Zusage S3). In Lauf A3 nachweisbar: ein `Bash`-Aufruf, den der Skill sperrt.

**Das Projekt wusste es und hat es nie aufgeschrieben.** Drei Protokolle halten fest, dass ein
Lauf verworfen wurde, weil „der `Skill`-Aufruf scheiterte"
(`2026-09-12-B01-allowed-tools.md:120`, `2026-09-13-erhebung-disallowed-tools.md`, Läufe A und
G; `CR-2026-057`:76). Aus dem dreimaligen Eigenverschulden ist nie ein Befund über die
ausgelieferte Datei geworden. **Das ist der wiederkehrende Befundtyp dieses Projekts, an einer
neuen Stelle:** eine Aufforderung (Abschnitt 17), die mehr verspricht, als die Datei daneben
zulässt.

## 4. Befund 3 – nicht gesucht: Zeile S2 nennt keine einzige Grenze

Die Fähigkeitsmatrix des Packs `claude-code` führt in Zeile **S2** „Gezielter Aufruf – Aufruf
über den Skill-Namen mit vorangestelltem Schrägstrich", Einstufung `[TECHNISCH]`, Beleg `[DOK]`
– und nennt weder die Rückfragepflicht noch die Argumentform noch den stummen Rückfall.

**Zum Vergleich:** Die Nachbarzeile S3 trägt seit 0.35.0 **drei** benannte Grenzen. S2 ist
seit dem ersten Release unverändert und hat nie eine getragen. Die Zusage ist nicht falsch –
der Aufruf **funktioniert** – aber sie ist unvollständig, und die Unvollständigkeit ist genau
die, die den Bericht ausgelöst hat.

## 5. Befund 4 – die Entlastung: Der Pilot ist wieder installiert

Die Übergabe vom 13.09. hält fest, die Leitwerk-Installation in `devpacks/otp-generator` sei
entfernt worden; **Kandidat 1** war, sie neu aufzusetzen oder den Piloten aufzugeben.
Vorgefunden am 2026-09-14: `.claude/` vollständig (Regeln, Skills, Agentenprofil,
Berechtigungsdatei), `project-overlay/` vollständig samt `CR-OTP-G-001` und den
Overlay-Dokumenten, `leitwerk-core/` vollständig, Framework-Version dort **0.37.0**.

**Der Kandidat hat sich erledigt, ohne dass dieser Antrag ihn behandelt.** Was bleibt, ist der
Versionsabstand: Der Pilot steht drei Releases hinter `main`.

## 6. Was diese Gegenprüfung nicht leistet

- **Sie prüft den Bericht, nicht seinen Anlass.** Die Sitzung, die ihn ausgelöst hat, ist nicht
  nachvollzogen; ihre Mitschrift liegt nicht vor. Was nachvollzogen ist, ist das beschriebene
  **Verhalten** an einem anderen Client.
- **Sie misst nicht, ob der verschärfte Text hilft.** Vier Läufe je Bedingung sind keine
  Stichprobe für eine Verhaltensaussage. Was gemessen ist, ist der Mechanismus.
- **Sie sagt nichts über `devin-desktop`** – den Client, an dem der Bericht entstanden ist. Ob
  der Skillaufruf dort rückfragepflichtig ist, bleibt unerhoben und wird als unerhoben
  deklariert.

## 7. Gegenzeichnung

| Feld | Inhalt |
|---|---|
| Durchführung | KI-Client unter Aufsicht, Sitzung vom 2026-09-14 |
| Gegengezeichnet durch | `<APPROVAL_ROLE>` |
| Datum | `<TBD: Datum der Gegenzeichnung>` |
| Anmerkungen | `<TBD: Anmerkungen der gegenzeichnenden Rolle>` |
