# Änderungsantrag `CR-2026-156`

| Feld | Inhalt |
|---|---|
| Titel | Das Mandat und die Reibung des ersten Projekteinsatzes – der Hook, der den Inhalt las, und die Entscheidung, die man abschreiben musste |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-27 |
| Betroffene Artefakte | `tests/scripts/hook-check-secrets.py`, `hook-overlay-status.py`, `overlay_status.py`, `validate-framework.py` (Prüfungen 98 bis 100), `probe-pruefungen.py`; `mandat.py` (neu); `install.py`; `framework/runtime/permissions.json`, `root-instruction.md`, `rules/00-framework-core.md`; `framework/core/02`, `03`, `05`, `06`, `09`; Skills `fw-plan`, `fw-change-analyze`, `fw-bugfix-prepare`, `fw-overlay-pflege` (neu); `templates/project-overlay/` (Abschnitte 6, 13, 13.1, 15, 20; ADR-Ablage); `governance/CHANGE_REQUEST_TEMPLATE.md`; Entscheidungsbaum 3, Checklisten 01 und 09, Onboarding, Kapitel 01, 05, 09, 20 des Hauptdokuments; Register, Roadmap, CHANGELOG, `VERSION`, Bestandsliste |
| Ebene laut Entscheidungsbaum 6 | Core (Regeln, Hook, Berechtigungsquelle), Skills, Overlay-Vorlage |
| Art | **Änderung.** MINOR-Release mit Kontingent; **Migrationshinweis für die Berechtigungsdatei** (D-448, D-453) |
| Dringlichkeit | regulär – Auftrag des Owners nach dem ersten Projekteinsatz |
| Status | 🟢 **entschieden am 2026-09-27** (E1 bis E11) |

---

## 1. Anlass

Der Owner hat `1.16.0` in einem Projekt mit `devin-desktop` eingesetzt (Overlay `0.1.1`). Vier Punkte, gleich mit dem
nächsten MINOR: (1) die Befunde der Sitzung A1 bis A7 und B (nachfolgend); (2) Änderungsanträge und Architektur im
Repositorium kollidieren bei mehreren Arbeitsplätzen – führend soll ein Ticketsystem oder eine Doku-Plattform über MCP
sein, das Repositorium nur Rückfall; (3) und (4) mehr Arbeit mit der Dokumentation als mit der Änderung: Besprochene
Änderungen an Overlay und Architektur ließen sich nur als Vorlage liefern und von Hand in gesperrte Dateien kopieren.
*„Wir dürfen die agilen Leitprinzipien neben der Governance nicht vergessen.“* Nachgereicht: Jede Sperre soll sofort
sagen, was zu tun ist; der Skill für die Einrichtung wird auch beim Framework-Update gebraucht; Ticketsystem und
Doku-Plattform sollen bei der Planung einbezogen werden.

## 2. Die Befunde des Einsatzes, gegengeprüft (D-23)

| # | Befund | Gegenprüfung | Behandlung |
|---|---|---|---|
| A1 | Neun von dreizehn Skills für den Client nicht aufrufbar, während Abschnitt 17 ihm den Aufruf aufträgt | Bestätigt – und schärfer: `fw-plan`, `fw-change-analyze`, `fw-bugfix-prepare` sperren `edit` und `exec`, dürften nach `08-skill-conventions.md` also `model` tragen | E7 |
| A2 | Der Hook sperrt einen Antrag unter `docs/`, weil sein Inhalt geschützte Pfade nennt | Bestätigt: Schreibwerkzeuge wurden mit allen Zeichenketten der Eingabe gemessen | E5 |
| A3 | Overlay-Version ersetzt statt geändert; die Statusmeldung sagt „aktiv“ | Bestätigt als Lücke: Der SessionStart-Hook las nur den Status; die Werte stehen in vier Trägern | E8 |
| A4 | Der Validator ist dem Client nicht freigegeben | Bestätigt | E9 |
| A5 | Kein Ort für Pläne und Freigaben | Bestätigt (`<TBD>` in `fw-plan`, Overlay ohne Ablage) | E10 |
| A6 | Zirkel Kontrollstufe/Plan | Bestätigt; aufgelöst über den Aufruf von `fw-change-analyze` durch den Client | E7 |
| A7 | Die Modusgrenzen gelten nur normativ | Seit `CR-2026-048` dokumentiert | `K-179` |
| B | Der Bericht in jedem Turn begräbt die Auskunft | Bestätigt | E10 |

## 3. Die Messung

Mit Client Pack `claude-code` (Claude Code 2.1.283, Opus 5.5) im Übungsrepositorium, Messstand `6c229a7`, Bäume unter
`C:\lw-1170`; Einzelheiten, Belege und Kosten im Protokoll
`.koolie/core/tests/protocols/2026-09-27-mandat-und-reibung.md`. Ein Befund fiel **in** der Messung: Der Hook sperrte
die Auskunft `mandat.py status`, weil der Client neben dem Befehl eine Beschreibung schickt – berichtigt vor der Reihe
(Prüfung 99, Sonde `99d`).

## 4. Vorlage zur Entscheidung

Vorgelegt am 2026-09-27 mit Empfehlung; der Owner hat Punkt (d) und (f) ergänzt, eine Idee nachgereicht und mit *„go“*
alle Empfehlungen angenommen, einschließlich der Teilfrage (n) zu den Kommentarverläufen.

| # | Frage | Entscheidung | Preis |
|---|---|---|---|
| E1 | Schnitt | `1.17.0` Reibung und Mandat, `1.18.0` MCP, `1.19.0` Paketquellen, dann Marktvergleich, `1.20.0` Messapparat | Paketquellen zwei Releases später |
| E2 | Modus | M6 Mandated Maintenance; Entscheidung beim Menschen, Eintragung delegierbar | Grenze *entschieden/vorgeschlagen* nur normativ |
| E3 | Durchsetzung | Mandatsdatei im Git-Verzeichnis, nur vom Menschen per `mandat.py`, befristet, Umfang | Verschleierter Befehlsname entgeht dem Muster (wie `K-32`) |
| E4 | Statische Sperre | Overlay nicht mehr im `deny`-Korb, allein der Hook | Ohne laufenden Hook nur normativ (`K-181`) |
| E5 | A2 | Schreibwerkzeuge am Ziel messen | – |
| E6 | Sperren | Blockade-Hinweis in vier Zeilen, auch in den Meldungen des Hooks | längere Meldungen |
| E7 | A1, A6 | Trigger `model` für die drei rein lesenden Skills; Bitte um den Aufruf statt Nacharbeit | 18 Zellen offen, nachgemessen |
| E8 | Skill und A3 | `fw-overlay-pflege`; Abgleich der Laufzeitfassung in `mandat.py`; SessionStart meldet Versionswiderspruch | ein Befehl des Menschen nach M6 |
| E9 | A4 | Prüfbefehle im `allow`-Korb der Kernquelle | drei Regeln von Hand beim Heben |
| E10 | Ablage, A5, B | Führendes System, Rückfall mit Datum und Kurzname, ADR je Datei; Kurzstatus zwischen Turns | Anbindung erst `1.18.0` |
| E11 | Kommentare, MCP-Zweck | Kategoriefreigabe für Kommentarverläufe; Zweck je MCP-Server | Einbindung in die Skills erst `1.18.0` |

## 5. Umsetzung

1. Schutz-Hook: Ziele statt Inhalt (`ziele_der_schreiboperation`, Patch-Köpfe), Mandat (`mandat_lesen`, `mandat_deckt`,
   `OVERLAY_MUSTER`), Mandatsschutz (`MANDATS_MUSTER`, Auskunft `status`), Blockade-Hinweis (`hinweis`).
2. `mandat.py`: `erteilen`, `status`, `beenden` (mit Abgleich), `abgleichen`.
3. `permissions.json`: Overlay aus `deny`; `allow` für Validator, `install.py --check`, `mandat.py status`, Skill
   `fw-overlay-pflege`. `install.py --update` nennt eine verbliebene statische Overlay-Sperre.
4. Regeln: M6 in `05` (Tabelle, Modusbeschreibung, 3.5 Kurzstatus, 3.7 Blockade-Hinweis), V3/V10 und die Stellung von
   M6 in `09`, Kommentarverläufe und MCP-Zweck in `02`, Overlay-Zeile in `03`, M1–M6 in `06`; Laufzeitschicht und
   Wurzelanweisung knapp (Budget 12.000 Zeichen).
5. Skills: drei mit `model` (K3-Auslöser für zwei nach `K-165`), `fw-overlay-pflege` (FW-SK-013) mit sechs Zellen,
   neue Zelle `SK-003-P03`.
6. Overlay-Vorlage: Prüfbefehle (6), MCP-Zweck und Kommentarverläufe (13), Ablage und führendes System (13.1), Mandat
   (15), Ausfüllhinweis zum Verlauf (20), `documents/architecture/decisions/`; Antragsvorlage mit Rückfallkennung.
7. Prüfungen 98 bis 100 mit Sonden; Bündel `sonden_mandat`.
8. Register, Roadmap, CHANGELOG, `VERSION`, Bestandsliste, Hauptdokument; Hebung beider Projekte; Bau.

## 6. Entscheidung

🟢 **Angenommen am 2026-09-27, E1 bis E11 wie vorgelegt** – *„go“*.

| # | Entscheidung | Decision Record |
|---|---|---|
| E1 | Releaseplan | D-445 |
| E2 | Modus M6 | D-446 |
| E3 | Mandat | D-447 |
| E4 | Overlay nicht mehr statisch gesperrt | D-448 |
| E5 | Ziel statt Inhalt | D-449 |
| E6 | Blockade-Hinweis | D-450 |
| E7 | Trigger `model` | D-451 |
| E8 | `fw-overlay-pflege` und Abgleich | D-452 |
| E9 | Prüfbefehle | D-453 |
| E10 | Ablage und führendes System | D-454 |
| E11 | Kommentarverläufe und MCP-Zweck | D-455 |
