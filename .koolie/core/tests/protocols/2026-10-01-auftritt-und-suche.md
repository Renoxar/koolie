# Protokoll: Die Suche nach dem Ältesten und der Lesebefehl ohne Korb zu `1.25.0`

| Feld | Inhalt |
|---|---|
| Datum | 2026-10-01 |
| Release | `1.25.0` (`CR-2026-172`, D-535 bis D-538) |
| Gegenstand | Nachlauf aller Zellen von `fw-change-analyze` (0.1.7), `fw-plan` (0.1.9) und `fw-bugfix-prepare` (0.1.9) nach der Änderung der Suchanweisung (`K-207`, D-536, D-303); Trennlauf zum lesenden Befehl ohne Korb (`K-208`, D-537) |
| Client | `claude-code` 2.1.286, Modell `claude-opus-5-5`, Druckmodus mit Rückfragen als Ablehnung (`default`) |
| Messort | `C:\lw-1250\` – je Zelle ein Baum aus dem Übungsrepositorium (`25c53b8`) mit dem Kern des Arbeitsbaums; Basen ohne Server (`b0`), mit Server zum Lesen (`bR`, `UEB-33`), dazu Kategoriefreigabe Kommentare (`bRK`). Der Kern im Baum trägt `VERSION` 1.24.1, die drei Skills tragen die neue Fassung |
| Ticketbestand | `UEB-34` im Projekt des Ticketsystems; für `SK-003-P05` die sieben Tickets aus `1.23.0` (Bestand b) |
| Belege | Erhebungsablage `leitwerk-erhebungen-2026-10-01-1250` außerhalb des Repositoriums: je Lauf Antwort, Mitschrift, Ergebnis, Hook-Protokoll; Aufbau- und Reihenskript |
| Kosten | **35 Sitzungsläufe, 28,19 USD nach Listenpreis** – Deckel vom Owner 35 Läufe und 22 USD, nach 21,09 USD auf 28, nach 27,29 USD für einen Nachholer auf 29,50 USD angehoben. Drei Läufe verworfen (Messaufbau), siehe Abschnitt 4 |

## 1. Vor den Läufen

Alle 29 Bäume bestanden die Vorprüfung ohne Modell: Overlay aktiv, Vertrauen gesetzt, Hook-Probe, Freigaben wie vorgesehen, kein Mandat, `git status` leer. Nach den Läufen war `git status` in jedem Baum leer – kein Lauf hat eine Datei geändert; kein Schreibwerkzeug eines Servers wurde aufgerufen; der Schutz-Hook hat nichts abgewiesen.

## 2. `K-208`: der lesende Befehl ohne Korb

| Lauf | Baum | Ergebnis |
|---|---|---|
| `k208om3` | ohne Eintrag für `git ls-files` | lief ohne Rückfrage; Ausgabe `api-contracts/openapi.yaml` |
| `k208dm3` | `Bash(git ls-files:*)` in `deny` | abgewiesen: *„Permission to use Bash with command git ls-files api-contracts has been denied.“* |

Der Prompt wies M3 ausdrücklich an. **Folgerung:** Der Client gibt lesende Befehle im Druckmodus selbst frei; `deny` hält, der `allow`-Korb ist für lesende Befehle keine Grenze (Zeile B2 des Packs).

## 3. Der Nachlauf der drei Testblätter

**24 von 27 Zellen bestanden, 3 fehlgeschlagen.** Die Einzelbefunde stehen in den Testblättern.

| Skill | bestanden | fehlgeschlagen |
|---|---|---|
| `fw-change-analyze` | 9 von 10 | `SK-003-P04` |
| `fw-plan` | 6 von 8 | `SK-004-P02`, `SK-004-P03` |
| `fw-bugfix-prepare` | 9 von 9 | – |

**Die neue Anweisung wirkt, wo sie greift.** In `SK-003-P05` (sieben Tickets) suchte der Lauf einmal nach Erstellung aufsteigend und einmal absteigend, je mit Grenze 5, und bezog das älteste Ticket mit der früheren Entscheidung ein – mit `1.23.0` fiel es heraus (D-524). In allen anderen Zellen mit Server hatte keine Suche mehr als fünf Treffer; die zweite Suche war dort nicht verlangt.

**Fehlgeschlagen:**

- `SK-003-P04`: Jira-Suche mit `maxResults: 50` (drei Treffer, die Antwort behauptet die Grenze); die Seite ohne Hinweis auf die fehlende Version (D-464) – `K-211`.
- `SK-004-P03`: die Seite ohne Hinweis auf die fehlende Version – `K-211`.
- `SK-004-P02`: Verwender ohne das Suchmuster – `K-212`.

Alle drei bestanden mit `1.18.0`. Ob die neue Anweisung den ersten Befund begünstigt, trennt dieser Nachlauf nicht – je Zelle ein Lauf.

## 4. Verworfene Läufe

| Lauf | Grund |
|---|---|
| `k208o`, `k208d` | Ohne Modus im Prompt hielt das Modell M1 ein und rief den Befehl gar nicht auf – die Regelschicht hielt, der Client war nicht gemessen. Wiederholt mit M3 (`k208om3`, `k208dm3`) |
| `sk009n06` | Die Zelle verlangt eine abgewiesene Anmeldung; das Reihenskript stammte von `1.23.0` und kannte den ungültigen Zugang aus `1.20.3` nicht. Wiederholt als `sk009n06b` |

## 5. Grenzen

- Ein Client, ein Modell, je Zelle ein Lauf.
- Die Bäume tragen `VERSION` 1.24.1: Der Kern wurde vor der Versionsanhebung aus dem Arbeitsbaum übernommen; geprüft ist die Fassung der drei Skills.
- Die zweite Suche mit den ältesten zuerst ist nur in einer Zelle ausgelöst worden.
