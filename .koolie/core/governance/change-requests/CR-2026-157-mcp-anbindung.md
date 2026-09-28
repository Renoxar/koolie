# Änderungsantrag `CR-2026-157`

| Feld | Inhalt |
|---|---|
| Titel | Das Ticketsystem und die Doku-Plattform über MCP – die Rückfrage, die die Freigabe schlug, und das Token ohne Bereiche |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-28 |
| Betroffene Artefakte | `framework/core/02-privacy.md` (3.8); `framework/runtime/rules/10-privacy-security.md`, `20-project-overlay.md`; Skills `fw-change-analyze`, `fw-plan`, `fw-bugfix-prepare` (SKILL, TESTS, CHANGELOG); `templates/project-overlay/OVERLAY.md` (13, 13.1, 13.2 neu); `tests/scripts/validate-framework.py` (Prüfung 101, Prüfung 13 mit Mandat), `probe-pruefungen.py`; `clients/claude-code/manifest.json`, `CLIENT_PACK.md`; `tests/TEST_CATALOG.md` (Klasse EX); `onboarding/exercises/README.md` (`UEB-33`, `UEB-34`); Register, Roadmap, CHANGELOG, `VERSION`, Bestandsliste, Hauptdokument |
| Ebene laut Entscheidungsbaum 6 | Core (Datenschutzregel, Prüfapparat), Skills, Overlay-Vorlage, Client Pack |
| Art | **Änderung.** MINOR-Release mit Kontingent; **Migrationshinweis für die Berechtigungsdatei**, sobald ein Projekt einen MCP-Server zum Lesen freigibt (D-459) |
| Dringlichkeit | regulär – geplant mit D-445 |
| Status | 🟢 **entschieden am 2026-09-28** (E1 bis E16) |

---

## 1. Anlass

Auftrag und Idee des Owners vom 2026-09-27 (`K-178`): Änderungsanträge und Architektur kollidieren im Repositorium,
sobald mehrere Arbeitsplätze arbeiten; führend soll ein Ticketsystem oder eine Doku-Plattform über MCP sein. Und die
Planung soll bestehende Anforderungen und frühere Entscheidungen aus diesen Systemen neben der Codebasis einbeziehen.
`1.17.0` hat die Felder angelegt (Overlay 13.1, Zweck je Server, Kategoriefreigabe für Kommentarverläufe); dieses
Release bindet an und misst.

## 2. Vorprüfung

Am 2026-09-28 gegen ein Atlassian-Cloud-Konto des Owners (Jira und Confluence, Free) und den offiziellen
Remote-MCP-Server des Herstellers, ohne Kontingent bis auf zwei Läufe (0,28 USD):

| # | Frage | Ergebnis |
|---|---|---|
| V1 | Erreicht die REST-Schnittstelle Projekt und Bereich? | ja |
| V2 | Welche Werkzeuge zeigt der Server? | Mit einem Token **ohne Bereiche** vier bis sechs Graph-Werkzeuge und keines für Jira oder Confluence (Gateway: `401 scope does not match`); mit Bereichen 46, jedes mit `readOnlyHint`. Ein Aufruf ohne eigene Kennung des Aufrufers wird abgewiesen (Cloudflare 1010) |
| V4 | Lädt `claude-code` den Server im Druckmodus, und greifen die Regeln je Werkzeug? | Ja: `.mcp.json` mit Kopfzeile aus `${VARIABLE}`; `allow` auf das Lesewerkzeug lässt es durch, `ask` auf das Schreibwerkzeug weist es ab |
| V5 | Und mit der pauschalen Rückfrage `mcp__*`, wie sie die Kernquelle erzeugt? | 🔴 **Auch das einzeln freigegebene Lesewerkzeug wird abgewiesen** – die Rückfrage schlägt die Freigabe |
| – | Erreicht ein MCP-Aufruf den Schutz-Hook? | 🔴 **Nein** – kein Pack führt MCP in seinem Hook-Matcher (`K-184`) |

## 3. Die Messung

Mit Client Pack `claude-code` (Claude Code 2.1.283, Opus 5.5) im Übungsrepositorium, Messstände `c437e15` und `4268827`, Bäume `C:\lw-1180` und `C:\lw-1180b`; Stichprobe `cursor` (cursor-agent 2026.09.26, Free) in `C:\lw-1180c`. 36 Sitzungsläufe, 26,96 USD nach Listenpreis, keiner verworfen. **Alle 29 Zellen tragen** – zwei nach einem Folgeturn, zwei nach der Angleichung an D-464, `FW-EX-03` erst nach einem Befund (D-458). Einzelheiten im Protokoll `.koolie/core/tests/protocols/2026-09-28-mcp-anbindung.md`.

## 4. Vorlage zur Entscheidung

Vorgelegt am 2026-09-28 mit Empfehlung und Schätzung (45 bis 55 Läufe `claude-code`, 28 bis 40 USD); der Owner hat alle
Empfehlungen angenommen – *„Ja, so machen wir das“*. Zwei Punkte haben sich beim Bau an einem Messbefund verschoben und
sind unten so benannt.

| # | Frage | Entscheidung | Preis |
|---|---|---|---|
| E1 | Zielsystem | Atlassian Cloud (Jira, Confluence) mit dem offiziellen Remote-MCP-Server | Messung an einem Konto |
| E2 | Anmeldung | Interaktiv je Arbeitsplatz; für kopflose Läufe ein Token mit Bereichen, Kopfzeile aus einer Umgebungsvariablen; nie ein Zugang in einer versionierten Datei | Ein Token läuft ab |
| E3 | Umfang | Lesen für Planung und Schreiben für Ablage | – |
| E4 | Ort der Anweisung | In den drei Skills, dazu die Kernregel `02-privacy.md` 3.8 und ihre Kurzfassung | 18 Zellen offen, nachgemessen |
| E5 | Schreiben | Lesende Skills schreiben nie; Ablage nur auf Anweisung, ein Plan erst nach Bestätigung | – |
| E6 | Rechte | Lesewerkzeuge einzeln in `allow`, Schreibwerkzeuge einzeln in `ask`; **beim Bau verschoben:** Die Berechtigungsdatei erzeugt kein Werkzeug (V6, D-452) – Prüfung 101 und `mandat.py abgleichen` nennen die Regeln, der Mensch trägt sie ein; die Pauschale weicht bei einer Freigabe zum Lesen (V5) | Handarbeit bei der Freigabe |
| E7 | Schutz-Hook für MCP | **Beim Bau zurückgestellt:** Der Hook sieht MCP-Aufrufe heute gar nicht; ein neuer Kanal in fünf Packs ist ein eigener Posten (`K-184`) | Bis dahin allein die Rückfrage je Schreibaufruf |
| E8 | Trefferzahl und Fundstelle | höchstens fünf je Suche; Ticketschlüssel mit Stand, Seite mit Version | – |
| E9 | Testdaten | per Skript über REST, synthetisch | – |
| E10 | Clients | `claude-code` vollständig, `cursor` und `devin-desktop` als Stichprobe, `openai-codex` und `kiro` aus der Dokumentation | `[DOK]` für zwei Packs |
| E11 | Rückfall | Server nicht erreichbar → sagen, im Repositorium weiter, nichts erfinden | – |
| E12 | `K-182` (1), (2) | im selben Zug an den Skills | Beifund hält nicht mehr an |
| E13 | `K-182` (3) | Validator erkennt ein gültiges Mandat | – |
| E14 | `fw-overlay-pflege`, Messapparat | nicht geändert (`K-183`); Apparat weiter kopiert bis `1.20.0` | – |
| E15 | Schutz-Hook, zwei BOM | **Beim Messen gefunden:** Die Eingabe von `cursor` kam mit zwei BOM; der Hook entfernt jetzt jedes | – |
| E16 | Version einer Seite | **Beim Messen gefunden:** Im Client liefert das Seitenwerkzeug keine Versionsnummer → Stand und Hinweis; Personenangaben aus Werkzeugantworten nicht wiedergeben | eine Aussage trägt dann einen Stand statt einer Version |

## 5. Umsetzung

1. `02-privacy.md` 3.8: Werkzeuge je Server, Lesen für Planung, Schreiben für Ablage; Kurzfassung in der Laufzeitschicht.
2. Drei Skills: externe Quellen im ersten Arbeitsschritt, Ausgabeabschnitt „Externe Quellen“, kein Schreiben nach
   außen, Rückfallzeile, Injektion auch aus Ticket und Seite; `K-182` (1) und (2).
3. Overlay-Vorlage Abschnitt 13.2 (Tabelle der Server mit Zweck und Werkzeugen, Trefferzahl, Anmeldung).
4. Prüfung 101 mit Sonde, Gegenprobe und Bündel `sonden_mcp`; Prüfung 13 schwächt die Versionsmeldung während eines
   Mandats zur Warnung ab (D-461).
5. `claude-code`: `mcp_permission_rule` im Manifest, Pack-Dokument mit den Messwerten.
6. Testblätter: 18 Zellen offen, acht neue; Katalogklasse EX mit drei Zellen; Präparationen `UEB-33`, `UEB-34`.
7. Register, Roadmap, CHANGELOG, `VERSION`, Bestandsliste, Hauptdokument; Hebung beider Projekte; Bau.

## 6. Entscheidung

🟢 **Angenommen am 2026-09-28, E1 bis E14**; E15 und E16 folgen Messbefunden und sind Berichtigungen ohne Ermessen – *„Ja, so machen wir das“*.

| # | Entscheidung | Decision Record |
|---|---|---|
| E1, E2 | Zielsystem und Anmeldung | D-456 |
| E3, E4, E8, E11 | Lesen für Planung in drei Skills | D-457 |
| E5 | Schreiben für Ablage | D-458 |
| E6 | Rechte je Werkzeug, Prüfung 101 | D-459 |
| E12 | Anhaltezeilen nach `K-182` | D-460 |
| E13 | Versionsabgleich im Mandat | D-461 |
| E9, E10, E14 | Messung | D-462 |
| E15 | Schutz-Hook, zwei BOM | D-463 |
| E16 | Version und Personenangaben | D-464 |
| E7 | Schutz-Hook für MCP | `K-184` |
