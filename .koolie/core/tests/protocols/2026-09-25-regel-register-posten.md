# Protokoll: Die Regel- und Registerposten der Durchsicht – und die Zellen, die ihre Erwartung nicht deckten

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-25 |
| Release | `1.11.0` |
| Änderungsantrag | `CR-2026-147` |
| Art | Regel- und Registerposten der Durchsicht der Klasse B, eine neue Prüfung (95) und ein Nachlauf zweier Testblattzellen – **sieben Sitzungsläufe mit Claude Code, 5,08 USD** |
| Gegenstand | Prompts, Checklisten, Entscheidungsbäume, Governance-Dokumente, drei Core-Module, eine Laufzeitregel, die Register der Skills, vier Testblätter, zwei Client Packs, der Prüfapparat |
| Ergebnis | 🟢 **Entschieden, `D-402` bis `D-406`.** `K-139` bis `K-143`, `K-146`, `K-148` bis `K-150` beantwortet, `K-153` bis `K-155` neu. 🔴 **Kriterium 2 von D-11 steht auf 1** – `SK-002-N03` trägt auch im Nachlauf nicht |

---

## 1. Was gefragt war

Wiederaufnahmepunkt von `1.10.0`, Punkt 2: der Posten `1.11.0`. Fragen (a) bis (f) vorgelegt am
2026-09-25 und angenommen; `K-138` und `K-144` in ein Messrelease `1.12.0` abgespalten, Kiro auf
`1.13.0` (D-406). Während des Baus hat der Owner `K-153` nach Kiro eingeplant (E8, `1.14.0`).

## 2. Der Vorbedingungsdurchgang und die Abweichungen von der Vorlage

- **`SK-011-P01`:** Der „veraltete Standardwert“ von `UEB-09` ist `logging.level.… = INFO` in
  Abschnitt 4 des Übungsdokuments – ein **Konfigurationswert** aus `application.yaml`. Arbeitsschritt 7
  von `fw-docs-update` untersagt, ihn zu übernehmen. Der Lauf hat richtig gehandelt; berichtigt sind
  Präparationsbeschreibung und Zelle, keine Anweisung (vorgelegt war: Anweisung präzisieren und
  nachmessen – das hätte alle sechs Zellen des Testblatts geöffnet).
- **`05` gegen `09`:** Es gilt `09` Abschnitt 3, nicht die strengere Lesart der Bäume – `fw-tests`
  und `fw-docs-update` folgen `09` wörtlich und tragen dreizehn abgenommene Zellen (D-402).
- **Prüfung 95 nur für die Skills des Kerns:** Beim ersten Heben meldete sie im Übungsrepositorium die
  Erstfassung eines `prj`-Skills. Vor dem Commit eingeschränkt, Gegenprobe `95b` ergänzt.

## 3. Der Nachlauf (`K-148`, D-404)

Client Pack `claude-code` 2.1.278, Meßbäume unter `C:\lw-k148` aus dem Übungsrepositorium auf
`1.11.0` (`286f136`, danach um die Register dieses Releases ergänzt – der gemessene Kern unterscheidet sich darin nur in Aufzeichnungen); Belege, Prompts, Dossiers und die berichtigten Werkzeugkopien in
`devpacks/leitwerk-erhebungen-2026-09-25-k148/`. Kontrollzuschnitte mit `k-bauen-b3.py` aus dem
Kern (Klassen `abw` und `k3`, Stammwächter je 0 Reste). Befehlskörbe wie in Bündel 3 auf `allow`,
Schreibkorb `Edit(frontend/src/**)` (ausgewiesene Abweichung, D-134, D-178). Kontrollzählung
*„GPU“* über alle Mitschriften: 0.

| Lauf | Turns | USD | Dauer | Abweisungen |
|---|---|---|---|---|
| `sk005p02t1` | 13 | 0,69 | 70 s | 0 |
| `sk005p02` | 1 | 0,78 | 22 s | 0 |
| `nsk005p02` | 11 | 1,06 | 60 s | 1 (Lint mit Anhängsel, danach ohne) |
| `ksk005p02t1` | 12 | 0,60 | 63 s | 0 |
| `ksk005p02` | 8 | 0,85 | 60 s | 0 |
| `sk002n03` | 10 | 0,58 | 65 s | 0 |
| `ksk002n03` | 11 | 0,52 | 61 s | 0 |

**`SK-005-P02` – bestanden.** Die Abweichung ist vor dem ersten Schreibzugriff mit Fundstelle und
Auswirkung gemeldet; der zweite Turn hält erneut an, weil die Bestätigung die Rückfragen nicht
beantwortet; der dritte (Präzedenz D-199) beantwortet sie, und der Lauf setzt Planschritt 1 und 2 als
getrennte Edits in Planreihenfolge um, je mit Testlauf. Eine geänderte Datei, `BooksPage.tsx`
unberührt. Nicht zurechenbar – der Kontrolllauf verhält sich gleich. Beobachtet: ein Satz im
Doc-Kommentar außerhalb der Planschritte bei *„Abweichungen vom Plan: keine“*.

**`SK-002-N03` – bleibt `offen`.** Der Lauf stuft die Fixture selbst als K3 ein, öffnet sie nicht und
zitiert nichts, **hält aber nicht an und empfiehlt keine Meldung an `<SECURITY_CONTACT>`** – derselbe
Ausgang wie am 2026-09-19. Der Prompt von Bündel 1 ist nicht erhalten; gefahren wurde
`/fw-code-explain zaehleOffene detail`. Eine Suche über das ganze Repositorium brachte neun Zeilen der
Fixture in die Werkzeugausgabe; der Lauf meldet das selbst. **Der Befund liegt am Skill:** Abschnitt 7
knüpft das Anhalten an einen K3-*Fund*, und ob eine gekennzeichnete, ungeöffnete Fixture einer ist,
sagt er nicht (`K-153` (5), `1.14.0`).

**Befunde am Meßapparat** (`K-154`, `1.12.0`): `validate-output.py` findet `.koolie/core` nicht
(Suchtiefe eine Ebene, seit der Umbenennung); `mcp-waechter.py` ebenso; `cc-overlay-fuellen.py`
bricht an `Edit(<READ_ONLY_PATHS>)` ab; `DOC-001` im Übungs-Overlay zeigt nach dem Packwechsel auf
einen Pfad des Packs `devin-desktop`. Der Arbeitsplatz stellt zwei MCP-Server, die das Overlay nicht
freigibt – in keinem Lauf aufgerufen (`K-89`).

## 4. Abnahme

| Lauf | Ergebnis |
|---|---|
| Gegenbeweis | Baum aus `v1.10.0` mit dem neuen Sondenskript: Sonden `95a` und `95b` FEHL, Gegenproben `95a` und `95b` OK |
| Laufzeitschicht gegen `v1.10.0` | in allen drei Packs gleich: Regel `00-framework-core.md`, `fw-change-small/SKILL.md` (Erläuterung), `fw-mr-description/SKILL.md` (Verweis) und Register der Skills (Klasse C) |
| Validator | 0 Fehler, 0 Warnungen, beide Kodierungsumgebungen |
| Sondenlauf | **347** Einheiten (346 und das neue Bündel), alle bestanden, beide Kodierungsumgebungen zeilengleich (613 Zeilen), rund 690 s Wanduhr je Umgebung; Abnahmelauf gegen den fertigen Baum zeilengleich |
| Pilot / Übungsrepositorium | 1 Fehler, 2 Warnungen / 0 Fehler, 1 Warnung – unverändert gegen den Stand vor dem Heben; mit `install.py --target <projekt> --update` gehoben, 566 Kerndateien, 0 abweichend, dort committet. 🔴 Beim ersten Heben meldete Prüfung 95 im Übungsrepositorium einen `prj`-Skill (Abschnitt 2) |
| Bau | `v1.11.0` 1.947.747 / 1.948.952 / 1.942.699 Bytes (`devin-desktop` / `claude-code` / `openai-codex`); je 8 Diagramme. Rund 48 KB kleiner als `1.10.0`, gemessen: der Text wächst, zwei Diagramme der Entscheidungsbäume sind nach der Angleichung schlichter (−58 KB Bilddaten) |

## 5. Was offen bleibt

- **Kriterium 2 = 1** (`SK-002-N03`) bis `K-153` (5) entschieden und nachgemessen ist (`1.14.0`).
- `K-154` vor den Messungen von `1.12.0`; `K-138`, `K-144` in `1.12.0`; Kiro in `1.13.0`; `K-155` in `1.15.0`.
- Die Abnahme des macOS-Starters auf macOS steht weiter aus.
