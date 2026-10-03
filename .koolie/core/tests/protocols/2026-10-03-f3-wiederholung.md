# Protokoll: Die drei offenen Zellen der externen Suche, je zweimal wiederholt (F3 zu `2.1.0`)

| Feld | Inhalt |
|---|---|
| Datum | 2026-10-03 |
| Release | `2.1.0` in Arbeit (`CR-2026-174` E3, Stufe 1) |
| Gegenstand | Wiederholung der Zellen `SK-003-P04`, `SK-004-P03` und `SK-004-P02`, die im Nachlauf zu `1.25.0` nicht hielten (`K-211`, `K-212`), ohne Anweisungsänderung: Streuung oder Regel? |
| Skills | `koolie-change-analyze` 0.1.8, `koolie-plan` 0.1.10. Seit der Messung zu `1.25.0` nur umbenannt (D-539) und um zwei Klammerverweise `(K-182)` gekürzt (D-540); `PLAN_TEMPLATE.md` ebenso nur im Namen. Keine Zelle öffnet sich dadurch (D-303), die Wiederholung misst dieselbe Anweisung |
| Client | `claude-code` 2.1.288, Modell `claude-opus-5-5`, Druckmodus mit Rückfragen als Ablehnung (`default`) |
| Messort | Ubuntu-Ausweichrechner, `/var/tmp/koolie-mess/lw-2100/` – je Lauf ein Baum aus dem Übungsrepositorium (`7673539`) mit dem Kern des Arbeitsbaums (Branch `feature/lehren-und-nachlauf-2.1.0`); Basen ohne Server (`b0`) und mit Server zum Lesen (`bR`, `UEB-33`) |
| Ticketbestand | `UEB-34` im Projekt des Ticketsystems, unverändert seit `1.25.0` |
| Belege | Erhebungsablage `leitwerk-erhebungen-2026-10-03-2100` außerhalb des Repositoriums: je Lauf Antwort, Mitschrift, Ergebnis, Hook-Protokoll; Aufbau- und Reihenskript, `mcp-aufrufe.py` (Werkzeugaufrufe mit Parametern aus der Mitschrift) |
| Kosten | **8 Sitzungsläufe, 8,25 USD nach Listenpreis** (Deckel für `2.1.0`: anfangs 55 Läufe / 50 USD, nach diesem Befund vom Owner auf 80 Läufe / 75 USD angehoben) |

## 1. Vor und nach den Läufen

Alle sechs Bäume bestanden die Vorprüfung ohne Modell: Overlay aktiv, Vertrauen gesetzt, Hook-Probe, Freigaben wie vorgesehen (16 Lesewerkzeuge in `bR`), kein Mandat, `git status` leer. Nach den Läufen war `git status` in jedem Baum leer; kein Schreibwerkzeug eines Servers wurde aufgerufen. Eine Abweisung (`sk004p02w2`): eine lesende Befehlskette `git ls-files … | head` – kein Kriterium berührt.

## 2. Ergebnis je Kriterium

| Zelle | Kriterium | Lauf 1 | Lauf 2 |
|---|---|---|---|
| `SK-003-P04` | höchstens fünf Treffer je Suche | ✅ `maxResults: 5`, `limit: 5` | ✅ `maxResults: 5`, `limit: 5` |
| `SK-003-P04` | Seite mit Version – liefert das Werkzeug keine, mit dem Hinweis darauf | ❌ „Stand 28.09.2026“ ohne Hinweis | ❌ ebenso |
| `SK-004-P03` | dasselbe für die Architekturentscheidung im Plan | ✅ „keine Versionsnummer geliefert“ | ❌ „Stand 28.09.2026“ ohne Hinweis |
| `SK-004-P02` | Verwender per Suche mit Suchmuster und Fundstellen | ✅ „(Suchmuster `BookTable`)“ | ❌ nur Fundstellen |

Alle übrigen Kriterien der drei Zellen hielten in allen Läufen: Ticket und Seite über Lesewerkzeuge gelesen, Widerspruch zum Backend benannt, Plan nach Vorlage, die empfohlene Option folgt der Architekturentscheidung; in `SK-004-P02` Verkürzung als Annahme, offene Frage mit Entscheidung und Rolle, abhängige Schritte „blockiert bis F1“ mit `<TBD: …>`.

**Die Vorläufe von `SK-004-P03` sind Läufe derselben Analyse** (`/koolie-change-analyze KOOL-2`, wie `SK-003-P04`). Von diesen vier Analyseläufen forderte **einer** (`sk004p03t1w2`) wieder `maxResults: 50` an und schrieb in der Antwort trotzdem „jeweils höchstens 5“ – dasselbe Muster wie `sk003p04` am 2026-10-01. Den Versionshinweis trug von den vier Analyseläufen einer (`sk004p03t1w1`).

## 3. Folgerung

Keines der drei Kriterien hält verlässlich; das ist bei zwei Wiederholungen keine Streuung, die man stehen lassen kann:

- **`K-211` (1)**, die Grenze: hielt in den beiden Zellenläufen, fiel in einem von vier gleichen Analyseläufen – mit falscher Behauptung in der Antwort.
- **`K-211` (2)**, der Versionshinweis: fehlte in vier von sechs Läufen mit einer Seite.
- **`K-212`**, das Suchmuster: einmal ja, einmal nein.

Stufe 2 nach `CR-2026-174` E3: die Abhilfen aus `K-211` und `K-212` als Anweisungsänderung mit Nachlauf aller Zellen der betroffenen Skills (D-303). Der Owner hat sie am 2026-10-03 noch für `2.1.0` entschieden und den Deckel dafür angehoben.

## 4. Grenzen

- Zwei Wiederholungen je Zelle trennen „hält meistens“ nicht von „hält zur Hälfte“; die Folgerung stützt sich darauf, dass jedes der drei Kriterien mindestens einmal fiel.
- Erster Messtag auf dem Ubuntu-Ausweichrechner; die Läufe zu `1.25.0` liefen unter Windows mit `claude-code` 2.1.286. Ein Unterschied durch Betriebssystem oder Clientversion ist nicht getrennt; die Befunde gleichen denen vom 2026-10-01.
