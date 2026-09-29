# Änderungsantrag `CR-2026-162`

| Feld | Inhalt |
|---|---|
| Titel | Die Wirksamkeitsprobe und der MCP-Aufruf am Schutz-Hook – und die Vorprüfung, die den Hook nie startete |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-29 |
| Betroffene Artefakte | `wirksamkeit.py` (neu), `install.py`, `clientmap.py`, `framework/runtime/hooks.json`, `tests/scripts/hook-check-secrets.py`, die Manifeste aller fünf Packs, `clients/claude-code/CLIENT_PACK.md`, `clients/cursor/CLIENT_PACK.md`, `tests/erhebungen/apparat/clients.py`, `tests/scripts/pruefungen/` (Prüfungen 16, 26, 106, 107), `tests/scripts/sonden/teil12_pruefungen_106_und_107.py` (neu), `templates/project-overlay/overlay-manifest.yaml`, `checklists/10-project-adoption.md`, `governance/RELEASE_PROCESS.md`; `governance/DECISION_LOG.md`, `docs/ROADMAP.md`, `tests/TEST_CATALOG.md`, `CHANGELOG.md`, `VERSION`, Hauptdokument |
| Ebene laut Entscheidungsbaum 6 | Framework Core (Schutz-Hook, Installer, Client Packs) |
| Art | Erweiterung ohne Overlay-Bruch; MINOR-Release mit Kontingent |
| Dringlichkeit | geplant (`K-195`, D-478; Triage D-466) |
| Status | 🟢 **entschieden am 2026-09-29** (E1 bis E6) |

---

## 1. Anlass

Der Roadmap-Posten `1.20.0` trug 21 Klärungspunkte mit dem Status „eingeplant (1.20.0 Schutzschicht)“. Seit D-478 ist sein Kern die Wirksamkeitsprobe (`K-195`): Validator, `install.py --check` und Prüfung 96 prüfen Dateien – ob der Schutz-Hook im Projekt läuft und sperrt, ob die Konfiguration lädt und ob der Client dem Projekt vertraut, prüfte niemand. Dazu die Lücke, die `1.18.0` gefunden hat: MCP-Aufrufe liefen an den Hook-Matchern aller fünf Packs vorbei (`K-184`); die Connectoren des claude.ai-Kontos, die `1.19.0` in jeder Sitzung gezählt hat (`K-191`); und ein Hook, der keine Entscheidung festhält (`K-192`).

## 2. Vorprüfung

Vorgelegt am 2026-09-29 mit Schätzung: rund 16 Läufe, rund 6 USD, Deckel 30 Läufe und 20 USD, zwei bis drei Sitzungen. Die Vorlage liegt außerhalb des Repositoriums. Der Owner folgt den Empfehlungen. Gegen den Stand gehalten vor dem Bau – vier Präzisierungen, alle eingearbeitet:

1. `tests/erhebungen/` gehört zur Nachweisschicht und fehlt im Lieferumfang `nutzung` (`clientmap.NACHWEIS_ABLAGEN`); die Probe kann dort nicht liegen.
2. Ein MCP-Werkzeug ist für den Hook `unbekannt` und würde nach der strengsten Lesart geprüft; ein bloßer Inhaltsabgleich ließe einen Dateisystem-Server `.env` lesen.
3. `hook_tools_absent` sagt „gibt es nicht“; ein neues Pflichtverb bräche die drei ungemessenen Packs – es braucht einen Zustand „unerhoben“.
4. `K-32` hängt an einer Pfadprüfung für die Shell und gehört zu `1.20.1`.

## 3. Vorlage zur Entscheidung

| # | Frage | Entscheidung | Preis |
|---|---|---|---|
| E1 | Alle 21 Punkte in einem Release? Und das Tor `K-185`? | Drei Releases und ein Posten: `1.20.0` Wirksamkeit und MCP, `1.20.1` Pfad- und Mustersemantik (mit `K-32`), `1.20.2` Modi, Ausnahmen und eingebaute Skills (Tor `K-185`), `1.20.3` Anweisungen mit Nachlauf und Aufzeichnungen. `1.20.0` fügt der Laufzeitschicht keine Zeile hinzu (D-485) | Drei weitere Vorlagen |
| E2 | Form der Wirksamkeitsprobe | `install.py --probe`, Logik in `wirksamkeit.py` im Kern, ohne Modell; Exit 1 bei einer fehlenden Muss-Kontrolle, „unerhoben“, wo nichts erreichbar ist (D-488) | Bei vier Packs bleibt die Konfigurationskontrolle unerhoben (`K-199`) |
| E3 | MCP am Schutz-Hook | Verb `mcp`, erkannt am Präfix; Inhalt gegen die Secret-Muster, Pfadfelder gegen die Secret-Pfade; gemessen an `claude-code` und `cursor`, die übrigen drei `hook_tools_unerhoben` (D-486) | Ein MCP-Server, der selbst lokal schreibt, ist über die Strukturmuster nicht gesperrt |
| E4 | Connectoren des Kontos | Abschnitt 8 des Packs, Abschaltweg erhoben, Warnung der Probe; die Sperre wird nicht ausgeliefert (D-489) | Ein Projekt, das sie nicht will, trägt die Regel selbst ein |
| E5 | Entscheidungsprotokoll des Hooks | JSONL unter dem Git-Verzeichnis, abschaltbar im Overlay-Manifest, nie Inhalt, nie Pfad (D-487) | Nicht manipulationsgeschützt (`K-200`) |
| E6 | Messumfang und Abnahme | `claude-code` vollständig, `cursor` als zweiter Adapter, der Apparat aus `1.19.0`; Abnahme der Probe an intakten und beschädigten Bäumen. Beim Bau gefunden: Die Hook-Vorprüfung des Apparats startete den Hook nie – sie nutzt jetzt die Probe (D-490) | – |

## 4. Umsetzung

1. **Schutz-Hook:** Verb `mcp` aus `hook_mcp_prefixes` aller Manifeste; Material der Pfadprüfung sind bei MCP allein die Pfadfelder, das Mandat wird dort nur an ihnen gemessen. Entscheidungsprotokoll mit Schalter im Overlay-Manifest; eine Zeile nur für ein Ereignis mit `hook_event_name`.
2. **Kernquelle und Abbildung:** `hooks.json` führt `mcp`; `clientmap._hook_matcher` überspringt ein Verb aus `hook_tools_unerhoben`. Manifeste: `claude-code` `mcp__.*`/`mcp__`, `cursor` `MCP:.*`/`MCP:`, die übrigen drei `hook_tools_unerhoben: ["mcp"]` mit Begründung.
3. **Wirksamkeitsprobe:** `wirksamkeit.py` mit den Kontrollen H1 bis H5, K1, V1, V2 und M1; `install.py --probe` und `--ohne-client`; `install.py` nennt die Probe nach Installation und Hebung, die Übernahmecheckliste und `RELEASE_PROCESS.md` Schritt 2 ebenso.
4. **Messapparat:** `hook_probe` von claude-code und cursor ruft die Probe (D-490).
5. **Prüfungen:** 16 sondiert jedes MCP-Präfix (zwei Sperren, eine Gegenprobe); 26 hält `hook_tools_unerhoben` und das Paar aus Matcher und Präfix; 106 das Protokoll; 107 die Gegenfälle der Probe. Sonden `106a` bis `106c`, `107a` bis `107c`, vier zu 26, je eine Gegenprobe.
6. **Packs:** `claude-code` Zeile H1 und Abschnitt 8 (Connectoren, Grenze des Protokolls), `cursor` Zeile H1 und Abschnitt 7.3.
7. Register, Roadmap, Testkatalog, CHANGELOG, `VERSION`, Bestandsliste, Hauptdokument; Hebung beider Projekte mit Probe.

## 5. Entscheidung

🟢 **Angenommen am 2026-09-29.**

| # | Entscheidung | Decision Record |
|---|---|---|
| E1 | Schnitt in drei Releases und einen Posten | D-485 |
| E2 | Die Wirksamkeitsprobe | D-488 |
| E3 | MCP am Schutz-Hook | D-486 |
| E4 | Die Connectoren des Kontos | D-489 |
| E5 | Das Entscheidungsprotokoll | D-487 |
| E6 | Die Hook-Vorprüfung des Apparats | D-490 |

## 6. Messung und Belege

Protokoll `tests/protocols/2026-09-29-schutzschicht.md`. 11 Sitzungsläufe mit `claude-code` (2,01 USD nach Listenpreis), 6 Läufe mit `cursor` im Free-Tarif; dazu kostenfreie Startmeldungen ohne Modellaufruf. Erhebungsablage `leitwerk-erhebungen-2026-09-29-1200` außerhalb des Repositoriums.
