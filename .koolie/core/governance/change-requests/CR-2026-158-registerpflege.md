# Änderungsantrag `CR-2026-158`

| Feld | Inhalt |
|---|---|
| Titel | Das Register, das seine offenen Punkte nicht zählte – und die Sperre, die nur noch auf dem Papier stand |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-29 |
| Betroffene Artefakte | `governance/DECISION_LOG.md` (Legende, Klärungstabelle, D-465 bis D-468, `K-187`); `tests/scripts/validate-framework.py` (Prüfung 102), `probe-pruefungen.py`; `docs/ROADMAP.md`; `governance/RELEASE_PROCESS.md` (Abschnitt 2); `clients/cursor`, `devin-desktop`, `openai-codex`, `kiro` (`CLIENT_PACK.md`); `tests/TEST_CATALOG.md`, `build/doc/00-kopf.md`, `26-qs-test.md`; `governance/ADOPTION_REGISTRY.md`; `CHANGELOG.md`, `VERSION`; Protokoll `tests/protocols/2026-09-29-registerpflege.md` |
| Ebene laut Entscheidungsbaum 6 | Governance (Register, Releaseplan, Prozess), Prüfapparat, Client Pack (Dokumentation) |
| Art | **Korrektur.** PATCH-Release ohne Kontingent; keine Anweisung eines Skills und keine Laufzeitdatei geändert, kein Migrationshinweis |
| Dringlichkeit | regulär – Auftrag des Owners vom 2026-09-29 |
| Status | 🟢 **entschieden am 2026-09-29** (E1 bis E5) |

---

## 1. Anlass

Der Owner hat am 2026-09-29 die Paketquellen (`K-155`) ohne Ziel-Release zurückgestellt und gefragt, welche anderen
Punkte wichtig wären. Das Register nannte 98 offene Klärungspunkte. Die Durchsicht sollte zuerst klären, ob die Zahl
stimmt – sie stimmte nicht.

## 2. Vorprüfung

Durchsicht aller 98 offen geführten Punkte am Repositorium, je Punkt ein Vorschlag mit Fundstelle, Schließungen in
Stichproben nachgeprüft; dazu alle fünf Packs in ein leeres Verzeichnis installiert und die Stichprobe des Owners zu
`1.18.0` unter `devin-desktop` aus der Sitzungsdatenbank des Clients ausgewertet (Protokoll
`2026-09-29-registerpflege.md`):

| # | Frage | Ergebnis |
|---|---|---|
| V1 | Stehen alle Klärungspunkte in der Klärungstabelle? | 🔴 **Nein – 114 von 184 in der Entscheidungstabelle** (`K-100` nannte 27), und eine Leerzeile teilte die Klärungstabelle nach `K-32` |
| V2 | Sind die offen geführten Punkte offen? | 🔴 **Elf sind belegt erledigt**, zwei davon schließt eine Entscheidung wörtlich (D-89, D-304); zwei Zielangaben waren überholt (`K-174`, `K-155`) |
| V3 | Beginnt jeder Status mit einem Wert der Legende? | 66 nicht („beantwortet mit“, „erledigt“, „entschieden (Vorschlag)“); die Legende kannte keinen Wert für „eingeplant“ |
| V4 | Sperrt die Berechtigungsdatei das Overlay, wie B4 von vier Packs sagt? | 🔴 **Nein, bei keinem Pack** – seit D-448 sperrt es allein der Schutz-Hook |
| V5 | Deckt die Schutzschicht von `claude-code` jedes Befehlswerkzeug? | 🔴 **Nein** – Berechtigungsdatei und Hook-Matcher kennen `Bash`, nicht das PowerShell-Werkzeug unter Windows (`K-70`, am Piloten) |
| V6 | Warum wies `devin-desktop` `git status` ab? | Die Werkzeugsperre des Skills `fw-change-analyze` (`permissions.deny: exec`), nicht die Berechtigungsdatei (`K-187`) |

## 3. Vorlage zur Entscheidung

Vorgelegt am 2026-09-29 mit Empfehlung; der Owner hat die Triage und den Plan angenommen – *„Ja, fang mit 1.18.1 an“*.

| # | Frage | Entscheidung | Preis |
|---|---|---|---|
| E1 | Wo stehen die Klärungspunkte? | Alle in der Klärungstabelle, aufsteigend | 114 Zeilen verschoben; Verweise nennen Kennungen, keine Zeilennummern |
| E2 | Wie wird der Status geführt und gehalten? | Vier Werte mehr in der Legende, jede Statuszelle beginnt mit einem Wert; Prüfung 102 hält Lage, Anfang und Zusammenlegung | Die Prüfung sieht den Anfang, nicht die Richtigkeit |
| E3 | Was wird aus den 98 Punkten? | Die Triage nach den Empfehlungen der Durchsicht, 26 Entscheidungen des Owners eingeschlossen; `K-79` bleibt abweichend offen | Eine Einplanung ist eine Absicht |
| E4 | Releaseplan | `1.18.2` PowerShell-Lücke, Brainstorming, `1.19.0` Messapparat, `1.20.0` Schutzschicht; Paketquellen ohne Ziel | Keine Installation über eine Paketquelle |
| E5 | Pack-Dokumente | B4 von vier Packs nach dem Erzeugnis; `devin-desktop` mit der Stichprobe zu `1.18.0` (MCP, S3) | – |

## 4. Umsetzung

1. Register: Klärungspunkte in eine Tabelle, Legende erweitert, Status je Punkt mit Beleg und dem bisherigen Text als
   Verlauf; D-465 bis D-468; `K-187` neu.
2. Prüfung 102 mit vier Sonden und zwei Gegenproben.
3. Roadmap: Standüberschrift, Releasetabelle, Abschnitte für `1.18.2`, `1.19.0`, `1.20.0`, Paketquellen vorgemerkt.
4. `RELEASE_PROCESS.md` Abschnitt 2: der Prüfzyklus (`K-14`).
5. Pack-Dokumente `cursor` 0.2.1, `devin-desktop` 0.14.6, `openai-codex` 0.1.8, `kiro` 0.1.1.
6. CHANGELOG, `VERSION`, Bestandsliste, Hauptdokument; Hebung beider Projekte; Bau.

## 5. Entscheidung

🟢 **Angenommen am 2026-09-29, E1 bis E5.**

| # | Entscheidung | Decision Record |
|---|---|---|
| E1, E2 | Registerform und Prüfung 102 | D-465 |
| E3 | Triage | D-466 |
| E4 | Releaseplan | D-467 |
| E5 | Pack-Dokumente | D-468 |
