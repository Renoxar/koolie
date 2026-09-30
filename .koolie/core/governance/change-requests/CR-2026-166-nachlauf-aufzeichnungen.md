# Änderungsantrag `CR-2026-166`

| Feld | Inhalt |
|---|---|
| Titel | Anweisungen mit Nachlauf und die Aufzeichnungen – und der Schnitt, der die Pakete nicht kannte |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-30 |
| Betroffene Artefakte | `framework/skills/fw-overlay-pflege/` (SKILL, TESTS, CHANGELOG), `framework/skills/fw-bugfix-prepare/` (SKILL, TESTS, CHANGELOG), `tests/scripts/pruefungen/werkzeuge.py` (Prüfung 71), `tests/scripts/sonden/teil08_pruefungen_66_bis_80.py`, `tests/erhebungen/messbaum-schnitt.py`, `onboarding/exercises/README.md` |
| Ebene laut Entscheidungsbaum 6 | Framework Core (Skills, Validator, Messapparat) |
| Art | Anweisungsänderung mit Nachlauf; PATCH-Release mit Kontingent, ohne Änderung der Laufzeitschicht |
| Dringlichkeit | geplant (D-485) |
| Status | 🟢 **entschieden am 2026-09-30** (E1 bis E4) |

---

## 1. Anlass

Aus dem Schnitt der Schutzschicht (D-485) trägt `1.20.3` die Anweisungen mit Nachlauf und die Aufzeichnungen mit Kontonamen: die MCP-Abfrage in `fw-overlay-pflege` (`K-183`), die Befunde der Messung zu `1.18.0` (`K-186`) und die zehn Aufzeichnungen mit dem Kontonamen einer Person (`K-85`). `K-202` aus `1.20.2` gehört dazu: Ob die Regelschicht einen ausdrücklichen Auftrag gegen die Regel aufhält, ist mit den Anweisungsänderungen zu prüfen. Mit demselben Release setzt `CR-2026-165` den Antrag des Owners zum Banner des Installationsdialogs um.

## 2. Vorprüfung

Vorgelegt am 2026-09-30 mit Schätzung: rund 21 Läufe `claude-code`, rund 16 USD, Deckel 30 Läufe und 25 USD, dazu 2 Läufe `kiro`. Die Vorlage liegt außerhalb des Repositoriums. Der Owner folgt den Empfehlungen und hat die Frage zu `K-85` selbst beantwortet. Vor der Vorlage erhoben, ohne Modell:

- Nach `08-skill-conventions.md` Abschnitt 7 verlangt jede Änderung einer Anweisung das ganze Testblatt neu: `SK-013` hat sechs Zellen, `SK-009` neun, drei davon mit Zugriff auf das angebundene System.
- Die Merkmalszeile aus `K-186` (2) in allen drei lesenden Skills hätte zusätzlich `SK-003` und `SK-004` geöffnet – 17 Zellen, rund 13 USD.
- Die Testdaten `UEB-34` stehen unverändert im System (vier Tickets, die Seite in Version 2).
- Die zehn Aufzeichnungen mit Kontonamen tragen den Namen des Owners; außer ihnen trifft Prüfung 71 keine Aufzeichnung.

## 3. Vorlage zur Entscheidung

| # | Frage | Entscheidung | Preis |
|---|---|---|---|
| E1 | Wie lernt `fw-overlay-pflege` den MCP-Server (`K-183`)? | Schritt 3 fragt alle Angaben aus Overlay 13.2 ab, ohne Zweck oder Werkzeugliste kein Eintrag, Schritt 7 nennt die Einzelregeln; Zugangsdaten ausgeschlossen; neue Zelle `SK-013-P03` (D-509) | Sieben Zellen nachgemessen |
| E2 | Welche Befunde aus `K-186` werden Anweisung? | (3) und (2) in `fw-bugfix-prepare`, (6) in der Präparation `UEB-33`; (1), (4) und (5) bleiben offen (D-510) | `fw-plan` und `fw-change-analyze` kennen das Merkmal der abgewiesenen Anmeldung nicht |
| E3 | Was geschieht mit den zehn Aufzeichnungen (`K-85`)? | Der Bestand bleibt; Prüfung 71 nimmt nur noch die zehn Dateien aus, nicht mehr die Ordner (D-508) | Eine gepflegte Liste, die nur schrumpfen darf |
| E4 | Was folgt aus `K-202`? | Gemessen ohne technische Schicht: 0 von 5 Läufen haben geschrieben (`claude-code` 2, `kiro` 3); der Regeltext bleibt, `K-202` bleibt offen (D-512) | Ein seltener Ausreißer ist nicht ausgeschlossen; der Schutz des Overlays bleibt die technische Schicht |

## 4. Umsetzung

1. **Skills:** `fw-overlay-pflege` 0.2.0 (Schritte 3 und 7, ausgeschlossene Informationen), `fw-bugfix-prepare` 0.1.8 (Abschnitt 7, zwei Zeilen); Erwartung von `SK-009-P02` nach D-510 ergänzt.
2. **Prüfung 71:** geschlossene Liste `P71_BESTAND`; Sonde `71d` neu, Gegenprobe `71c` auf eine Aufzeichnung des Bestands.
3. **Messapparat:** `messbaum-schnitt.py` schneidet die Pakete `tests/scripts/sonden/` und `tests/scripts/pruefungen/` (D-511); `UEB-33` im Übungs-README beschrieben wie gebaut.
4. **Messung:** Testblätter `SK-009` und `SK-013` nachgemessen, `K-202` an `claude-code` und `kiro`.

## 5. Entscheidung

🟢 **Angenommen am 2026-09-30.**

| # | Entscheidung | Decision Record |
|---|---|---|
| E1 | MCP-Abfrage in `fw-overlay-pflege` | D-509 |
| E2 | `fw-bugfix-prepare` und `UEB-33` | D-510 |
| E3 | Die Aufzeichnungen mit Kontonamen | D-508 |
| E4 | `K-202` | D-512 |
| – | Befund beim Baumbau: der Schnitt und die Pakete | D-511 |

## 6. Messung und Belege

Protokoll `tests/protocols/2026-09-30-nachlauf-banner.md`. 23 Sitzungsläufe mit `claude-code` (15,41 USD nach Listenpreis), davon 21 für die 16 Zellen und 2 für `K-202`; 3 Läufe mit `kiro` (`--trust-all-tools`). Erhebungsablage `leitwerk-erhebungen-2026-09-30-1203` außerhalb des Repositoriums.
