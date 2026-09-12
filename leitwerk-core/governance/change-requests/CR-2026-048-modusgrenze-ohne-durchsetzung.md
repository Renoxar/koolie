# Änderungsantrag `CR-2026-048`

| Feld | Inhalt |
|---|---|
| Titel | Die Betriebsmodi nennen eine technische Durchsetzung, die es nicht gibt – drei von fünf Modi |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-12 |
| Betroffene Artefakte | `framework/core/05-working-model.md` (Zeile „Durchsetzung" in M1, M2, M4, M5; M3 hat keine), `framework/skills/fw-docs-update/SKILL.md` (Erläuterung zur Pfadprüfung), gegebenenfalls die übrigen Skills mit `permissions`-Frontmatter |
| Ebene laut Entscheidungsbaum 6 | Kern – Arbeitsmodell; die Mechanismusnennung gehört ohnehin nicht dorthin |
| Art | Befund **B05** des unabhängigen Reviews vom 2026-09-12, P1; **gegengeprüft und gemessen** |
| Dringlichkeit | **vor der weiteren Nutzung im Pilotprojekt** – M5 ist der Modus, in dem dort gearbeitet wird |

## 1. Anlass und Problem

Das Arbeitsmodell führt je Betriebsmodus eine Zeile **Durchsetzung**. Sie beantwortet die Frage,
was einen Modus von einer Absichtserklärung unterscheidet. Bei M4 und M5 lautet sie:

| Modus | Zeile „Durchsetzung" heute |
|---|---|
| M4 Test and Validation | Skill-`permissions` mit `Write(<TEST_PATHS>/**)` und `Exec(<TEST_COMMAND>)`; Hook `PreToolUse` zur Blockierung von Schreibzugriffen außerhalb der Testpfade |
| M5 Documentation Support | Skill-`permissions` mit `Write(<DOC_PATHS>/**)`, `deny: exec` |

**Beide genannten Mechanismen tragen nicht.**

### Der Hook kennt die Grenze nicht – gemessen

`tests/protocols/2026-09-12-B04-B05-gegenpruefung.md`, vier Läufe mit drei Positivkontrollen im
selben Lauf:

| Lauf | Eingabe | Ergebnis |
|---|---|---|
| B05-1 | `Write` auf einen Quellcodepfad – **außerhalb** des M5-Scopes | **passiert** |
| B05-2 | `Write` auf einen Dokumentationspfad – **innerhalb** des M5-Scopes | **passiert** |
| B05-3 | `Edit` auf Produktivcode – **außerhalb** des M4-Scopes | **passiert** |
| B05-4 | derselbe Zugriff mit `"mode": "M5"` in der Eingabe | **passiert** |

**Auf B05-1 und B05-2 kommt es an.** Sie unterscheiden sich genau im zugesagten Merkmal, und der
Hook entscheidet gleich. Der Befund ist nicht, dass er zu wenig blockiert – er ist, dass er die
zugesagte Grenze **nicht kennt**: Weder ein Betriebsmodus noch eine Liste erlaubter Schreibpfade
erreicht ihn. B05-4 schließt die naheliegende Ausrede aus; ein mitgeführter Modus ändert nichts,
das Feld wird nicht gelesen. Die drei Positivkontrollen desselben Laufs blockieren
erwartungsgemäß – der Hook läuft, er kennt diese Grenze nur nicht.

### Die Skill-`permissions` tragen sie doppelt nicht

Erstens sagt der Skill `fw-docs-update` es selbst: Eine Beschränkung auf `<DOC_PATHS>` unter
Ausschluss aller übrigen Pfade sei über Skill-`permissions` **nicht ausdrückbar**, weil
`<DOC_PATHS>` eine Teilmenge von `<ALLOWED_PATHS>` ist und `deny` gegen `allow` gewinnt. Der
Skill verweist deshalb auf den Hook – und dort endet der Verweis, siehe oben.

Zweitens verwirft `install.py` beim Rendern des Frontmatters jedes Feld, das das Manifest nicht
kennt, und `permissions` ist eines davon (**B01**, gemessen am 2026-09-12). Zwölf Quellskills
tragen das Feld; keine installierte Fassung trägt es.

### Derselbe Satz steht bei M1 und M2

| Modus | Zeile „Durchsetzung" heute | Lage |
|---|---|---|
| M1 Read-only Analysis | Werkzeugbeschränkung des Skills auf lesende Verben und `deny: edit, exec` über dessen `permissions` | **trägt nicht** – dasselbe verworfene Feld (B01) |
| M2 Guided Planning | Schreibrecht allein auf die Plan-Datei | **kein benannter Mechanismus**, nur eine Wirkung |
| M3 Controlled Modification | keine Zeile `Durchsetzung`, wohl aber `Umsetzung im Werkzeug` – mit Belegklasse je Mechanismus | **trägt, und zwar als einziger richtig.** Bei der Umsetzung hat sich gezeigt: Das ist die Form, die die anderen vier haben sollten |

Drei von fünf Modi nennen einen Mechanismus, und alle drei nennen einen, der nicht trägt. **Zwei
Zeilen zu berichtigen und zwei stehen zu lassen wäre genau der Fehler, den dieses Projekt
wiederholt bei sich selbst gefunden hat** (76 statt 248, fünf statt zehn, sechs statt zwölf).

> **Berichtigt bei der Umsetzung:** Der Antrag führte M3 zunächst als Ausreißer, weil ihm die
> Zeile `Durchsetzung` fehlt. Er hat stattdessen `Umsetzung im Werkzeug` – und nennt dort je
> Mechanismus eine Belegklasse (`[DOK]`, `[KONZ]`, `[EMPF]`). Das ist die ehrlichere Form.
> **Die vier übrigen Modi sind deshalb auf M3 nachgezogen worden, nicht umgekehrt.**

## 2. Vorgeschlagene Änderung

1. **Die Zeile „Durchsetzung" nennt künftig die Klasse, nicht einen Mechanismus.** Für M1, M4 und
   M5 lautet sie: die Scope-Grenze gilt **normativ** (`[TEXTUELL]`), getragen von der Regelschicht
   und der menschlichen Prüfpflicht des Modus; eine technische Durchsetzung besteht **nicht**.
   Die zusätzlich wirkenden technischen Sperren (Secret-Pfade, Kernverzeichnis beim direkten
   Schreibwerkzeug) bleiben genannt – sie wirken, sie sind nur nicht die Modusgrenze.
2. **M2 und M3 bekommen dieselbe Zeile**, damit jeder Modus dieselbe Frage beantwortet. Bei M3
   ist die Antwort ausdrücklich zu geben, nicht wegzulassen.
3. **Der Verweis in `fw-docs-update/SKILL.md` wird berichtigt.** Der Satz „die technische
   Absicherung erfolgt über den `PreToolUse`-Hook mit Pfadprüfung" entfällt; an seine Stelle
   tritt der gemessene Stand samt Protokollverweis.
4. **Der Mechanismus, wo er genannt bleibt, gehört in die Packs**, nicht in den Kern. Der Kern
   ist werkzeugneutral (D-15, D-28); `Write(...)`, `Exec(...)` und `PreToolUse` sind Namen aus
   der Welt eines Clients.

## 3. Was dieser Antrag nicht ändert

- **Er baut kein Sitzungsobjekt.** Das Review schlägt eines vor (`mode`, `writable_roots`,
  `allowed_commands`, gebunden an eine bestätigte Konfigurationsversion). Es ist der richtige
  Weg und braucht zwei Voraussetzungen, die beide fehlen: die Pfadauswertung aus **B06** und
  eine Quelle, die der Agent nicht selbst schreiben kann. Siehe E1.
- **Er ändert an den Modi selbst nichts** – nicht an den zulässigen Aktionen, nicht an den
  Verbotslisten, nicht an den Prüfpflichten. Nur die Aussage darüber, was sie erzwingt.
- **Er behebt B01 nicht.** Dass `install.py` das Feld `permissions` still verwirft, ist ein
  eigener Befund mit eigenem Antrag; er ist hier nur die halbe Begründung.
- **Er berührt B3/B4/B5/B8 der Packs nicht** – das ist `CR-2026-047`.

## 4. Prüffragen

- [x] Richtige Ebene: Kern. Die Modusdefinition ist Kern; die **Mechanismusnennung** darin war
      schon vorher eine Client-Bindung im werkzeugneutralen Kern (D-15, D-28) und fällt damit.
- [x] Verschärfungsprinzip: Keine Lockerung. Die Regel bleibt wortgleich verbindlich; allein die
      Behauptung über ihre Erzwingung entfällt. **K3 nicht berührt.**
- [x] Widerspruchsfreiheit: D-15, D-28 (werkzeugneutraler Kern), D-23 (Wirkungsnachweis), D-41
      (Kernzusage – M4/M5 sind keine), B01-Protokoll gelesen.
- [x] Laufzeitfassungen: Das Arbeitsmodell ist Kernquelle; die Kurzform in der Regelablage ist
      auf denselben Stand zu bringen (D-24 – geladene Kurzform und kanonische Langform dürfen
      nicht auseinanderlaufen). **Zu prüfen, bevor der Antrag umgesetzt wird.**
- [x] Belegstatus: **gemessen**, vier Läufe mit drei Positivkontrollen.
- [ ] Test- und Validierungsbedarf: Textkorrektur ohne neue Prüfung. **Aber:** Prüfung 25
      verlangt bei `[NICHT ABBILDBAR]` den benannten Ersatz – bei E2 zu beachten.
- [x] Overlays: nicht betroffen; kein Projekt fällt durch diese Änderung durch. Der **Pilot**
      arbeitet in M5 und ist über den geänderten Stand zu informieren.
- [ ] Dokumentation: CHANGELOG, Decision Log, `docs/ROADMAP.md` (Paket 3).

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Jetzt ausweisen – oder gleich das Sitzungsobjekt bauen? | **Jetzt ausweisen.** Das Sitzungsobjekt setzt B06 voraus (Pfadidentität und Eingabeschema) und eine Quelle außerhalb der Reichweite des Agenten. Beides fehlt. Ein zweiter Mechanismus auf unbelegter Grundlage ist genau die Konstruktion, die `AP2-DD-10` acht Releases lang trug | **Die Modusgrenze bleibt Modellverhalten.** Wer M5 einsetzt, verlässt sich auf Regeltext und menschliche Prüfung – das ist ab dann wenigstens zutreffend beschrieben, aber es ist weniger, als heute dasteht |
| E2 | Welche Klasse trägt die Modusgrenze künftig? | **`[TEXTUELL]`.** Die Regel existiert, ist verbindlich formuliert und wirkt über die Regelschicht. `[NICHT ABBILDBAR]` wäre falsch und würde nach Prüfung 25 einen Ersatz verlangen, den die Regelschicht gerade darstellt | Ein Leser, der `[TEXTUELL]` überliest, hält die Lage für unverändert. Deshalb gehört die Änderung in den CHANGELOG und an den Piloten kommuniziert, nicht nur in die Tabelle |
| E3 | **Nur M4/M5 berichtigen – oder alle fünf Modi?** | **Alle fünf.** M1 trägt denselben verworfenen Mechanismus, M2 nennt eine Wirkung statt eines Mechanismus, und M3 – der Modus, der Produktivcode ändert – nennt gar nichts. Zwei von fünf zu berichtigen hieße, den Befund zu kennen und liegen zu lassen | Der Antrag wird größer als der Befund des Reviews. **Die Gegenposition ist vertretbar:** B05 nennt M4 und M5; wer den Befundumfang strikt hält, behandelt M1 im Antrag zu B01 und M2/M3 gesondert. Dann sind es drei Anträge statt einem, und die Tabelle bleibt bis dahin uneinheitlich |
| E4 | Bleibt der Mechanismus überhaupt irgendwo genannt? | **Ja – im Client Pack, nicht im Kern.** Was ein Client erzwingen kann, steht in seiner Fähigkeitsmatrix; dort steht es bereits (B-Block). Der Kern verweist darauf, statt Werkzeugnamen zu führen | Wer die Modusdefinition liest, muss für den Mechanismus eine zweite Datei aufschlagen. Das ist der Preis der Werkzeugneutralität und in diesem Projekt bereits 61-mal bezahlt (D-15) |
| E5 | Muss die Kurzform in der Regelablage mitgezogen werden? | **Ja, im selben Antrag.** D-24 ist genau deshalb entstanden: Sieben Abweichungen zwischen geladener Kurzform und kanonischer Langform. Eine Korrektur, die nur die Langform erreicht, stellt den Zustand wieder her, den D-24 beendet hat | Zwei Dateien statt einer, und die Kurzform ist die, die tatsächlich in jede Sitzung lädt. Der Abgleich ist vor der Umsetzung zu prüfen – er ist im Antrag als offene Prüffrage markiert |
| E6 | Wie wird die Wirkung nachgewiesen? | **Gar nicht durch eine neue Prüfung** – der Antrag entfernt eine unzutreffende Behauptung, er stellt keine auf. Der Beleg ist das Protokoll vom 2026-09-12. **Wohl aber eine Validatorprüfung:** Die Zeile „Durchsetzung" darf künftig keinen Client-Werkzeugnamen mehr enthalten; Prüfung 14 erfasst Clientnamen, nicht Werkzeugnamen | Eine solche Prüfung ist neu und braucht nach D-23 Sonde und Gegenprobe. **Sie ist optional** – ohne sie wandert derselbe Satz beim nächsten Mal wieder in den Kern, und gefunden hat ihn diesmal ein externes Review |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle sechs Fragen wie vorgelegt.** E1 jetzt ausweisen statt das Sitzungsobjekt bauen; E2 die Modusgrenze trägt `[TEXTUELL]`; E3 **alle fünf Modi**, nicht nur M4 und M5; E4 der Mechanismus bleibt im Client Pack genannt, nicht im Kern; E5 die Kurzform der Regelablage wird mitgezogen; E6 kein neuer Sondenblock, aber der Beleg im Protokoll |
| Datum | 2026-09-12 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | **E3 hat den Befund bei der Umsetzung berichtigt, und zwar zugunsten des Bestands:** M3 nennt seine Durchsetzung nicht gar nicht, sondern unter der Überschrift `Umsetzung im Werkzeug` – mit Belegklassen je Mechanismus. **Das ist die richtige Form, und die vier übrigen Modi sind darauf nachgezogen worden**, statt M3 auf die schlechtere zu bringen. Der Antragstext hatte M3 als Ausreißer geführt; das ist im Protokoll und in der Roadmap berichtigt. **E5 ist eingelöst:** `framework/runtime/rules/00-framework-core.md` trägt den Satz, dass die Schreibrechte der Modustabelle normativ gelten – das ist die Fassung, die in jede Sitzung lädt (D-24). **Offen bleibt E1:** Das Sitzungsobjekt mit `mode` und `writable_roots` setzt B06 voraus und bleibt Paket 6 |
| Umsetzung | umgesetzt mit `0.30.0` |
