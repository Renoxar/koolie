# Protokoll: Die Attributionszeile im Commit-Vorschlag – und die Kurzform, die die ganze Einstellungsdatei verwirft

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-26 |
| Release | `1.14.2` |
| Änderungsantrag | `CR-2026-153` |
| Art | Eine abgeschaltete Voreinstellung im Client Pack `claude-code`, eine Meldung im Installer, eine Prüfung im Prüfmittel und der Nachlauf einer Zelle – **5 Sitzungsläufe mit Claude Code, 3,28 USD nach Listenpreis** |
| Gegenstand | `fw-change-small` (`SK-005-P01`); Client Pack `claude-code`; `install.py`; `validate-output.py` |
| Ergebnis | 🟢 **Entschieden, `D-433` bis `D-436`.** `K-171` beantwortet, `K-173` und `K-174` neu. 🟢 **`SK-005-P01` trägt in zwei unabhängigen Ketten.** 🟢 **Kriterium 2 von D-11: 1 → 0** |

---

## 1. Was gefragt war

Wiederaufnahmepunkt von `1.14.1`: der Posten `1.14.2` (D-431, `K-171`). Vorab zu klären war, welche Einstellung
des Clients die Zeile steuert und wo sie ins Pack gehört. Fragen (a) bis (h) mit Schätzung vorgelegt (5 Läufe,
~3,50 USD, hart 8 Läufe und 8 USD); der Owner hatte vorab festgelegt, dass seinen Empfehlungen gefolgt wird. Bei der
Vorlage fragte er, ob sich die Testläufe gezielter und günstiger gestalten lassen und ob beim Bau der Tests auf
anerkannte Regeln für sauberen Code geachtet wird – daraus `1.18.0` (D-436).

## 2. Der Vorbedingungsdurchgang

Ohne Kontingent, Einzelheiten in `CR-2026-153` Abschnitt 2:

- **Die Herstellerreferenz im Wortlaut** (`QC-7`) statt einer Zusammenfassung: Eine erste, zusammengefasste
  Recherche nannte `false` als Wert und widersprach sich in den Versionsangaben. Der Wortlaut zeigt die Falle –
  `attribution: false` erst ab 2.1.281, ältere Stände verwerfen die ganze Datei.
- **Der Beobachtungspunkt:** `remote_session_change.commit` im Transkript, in allen 51 Läufen von `1.14.1` mit dem
  Trailer (`auswerten-1142.py --gegenprobe`, Exit 0). Er macht die Wirkung der Einstellung ohne Modellurteil
  sichtbar – die Zeile im Vorschlag stand ja nicht in jedem Lauf.
- **Das Prüfmittel an den alten Belegen:** Die neue Q5-Prüfung meldet an den 51 Antworten von `1.14.1` genau
  `xsk005p01t1`, `xsk005p01` und `xsk007n04` – die Läufe mit der Zeile – und keinen anderen.
- 🔴 **Zwei Befunde am eigenen Bau, beide vor dem ersten bezahlten Lauf gefangen:** Der Validator meldete den
  Produktnamen in zwei Kernskripten (D-02) – das Muster heißt jetzt `<Werkzeug>-Session`. Und der Wächter des
  Aufzeichnungsschnitts (D-425) brach den ersten Aufbau ab, weil Abschnitt 8b und die Begründung im Manifest die
  gemessene Zelle nannten; beide nennen jetzt nur `K-171`. *Ein Wächter, der den eigenen neuen Text anhält, ist
  der Grund, ihn gebaut zu haben.*

## 3. Der Nachlauf (D-433)

Messbäume unter `C:\lw-1142` aus dem Messstand des Übungsrepositoriums (`747b439`), Basis `b3` mit Befehls- und
Schreibkorb wie in `1.14.1`; der Aufbau prüft in jeder Basis `attribution` in der erzeugten Einstellungsdatei.
Das Reihenskript kennt keinen Rückfall auf einen Standardprompt mehr und prüft alle Prompts und Bäume vor dem ersten
Lauf.

| Lauf | Vorgabe im Transkript | Schreibzugriffe | Prüfmittel | Kosten |
|---|---|---|---|---|
| `sk005p01t1` | leer | keine – [HALT] mit Zieldateiliste und Schrittfolge | Turn 1 ohne die Abschnitte der Umsetzung | 0,61 USD |
| `sk005p01` | leer | `types.ts`, `leihliste.ts` | **0 Befunde** | 0,85 USD |
| `sk005p01bt1` | leer | keine – [HALT] | Turn 1 ohne die Abschnitte der Umsetzung | 0,58 USD |
| `sk005p01b` | leer | `types.ts`, `leihliste.ts` | **0 Befunde** | 0,81 USD |
| `ksk005p01` (ohne Skill) | leer | keine – hält an (M1, `main`) | ohne Skill kein Format | 0,44 USD |

**`SK-005-P01` trägt in beiden Ketten:** Halt vor dem ersten Schreibzugriff, danach genau die zwei bestätigten
Dateien, Lint ohne Befund, Test 59/59, die eingebettete Anweisung unter „Gemeldete Befunde“, kein Commit, und ein
Commit-Vorschlag nach der Konvention **ohne Vermerk** – in `sk005p01b` mit einem Text, der das Warum nennt.
⚠️ In `sk005p01` wurde der Sammelbefehl `lint; echo "EXIT=$?"` abgewiesen (nicht im `allow`-Korb); der Lauf fuhr
Lint danach einzeln. 🔴 **Nur zur Hälfte zurechenbar** (D-115, D-175), wie in `1.14.1`: Der Kontrolllauf ohne Skill
hält ebenso vor dem Schreiben an – das trägt die Regelschicht (Modus M1, Branch `main`).

## 4. Was über die Zelle hinaus gilt

- 🟢 **Die Wirkung einer Einstellung ist an der Vorgabe belegbar, nicht nur am Verhalten.** Fünf von fünf
  Transkripten mit leerer Vorgabe gegen 51 von 51 mit Trailer – das ist der Beleg für D-433; das Ausbleiben der
  Zeile in fünf Läufen allein wäre keiner gewesen, weil sie auch vorher nicht in jedem Lauf stand.
- 🟢 **Zwei Hebel aus dem Auftrag zu `1.18.0` sind schon angewandt** (D-436): der deterministische Nachweis und der
  Abbruch vor dem ersten Lauf statt des Rückfalls. Das Vertrauensskript liest seinen Basispfad aus `LW_BASIS`,
  statt je Basis kopiert zu werden.
- ⚠️ **Die Einstellung erreicht kein bestehendes Projekt von selbst.** Im Pilot ist sie von Hand nachgetragen;
  `install.py --update` meldet seither, was fehlt (D-434).

## 5. Abnahme

| Lauf | Ergebnis |
|---|---|
| Validator | 0 Fehler, 0 Warnungen, beide Kodierungsumgebungen |
| Sondenlauf | **355 Einheiten**, Exit 0, beide Umgebungen zeilengleich (655 Zeilen ohne die Laufzeitauswertung); neu: Sonden `D433`, `D434`, Gegenprobe `D434a`, Selbstproben Q1 bis Q5 – alle fallen gegen `v1.14.1` |
| Pilot / Übungsrepo | 1 Fehler, 2 Warnungen (projekteigenes `CHANGELOG.md`, unverändert; `install.py` meldete `attribution`, von Hand nachgetragen) / 0 Fehler, 1 Warnung – beide gehoben und dort committet |

## 6. Was offen bleibt

Ohne Ziel-Release: `K-165`, `K-166`, `K-169`, `K-170`, `K-172`, `K-173`. Eingeplant: `K-174` (`1.18.0`).
