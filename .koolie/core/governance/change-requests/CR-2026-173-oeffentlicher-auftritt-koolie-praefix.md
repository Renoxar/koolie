# Änderungsantrag `CR-2026-173`

| Feld | Inhalt |
|---|---|
| Titel | Sauberer öffentlicher Auftritt und das Skill-Präfix `koolie-` |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-10-02 |
| Betroffene Artefakte | alle mitgelieferten Skills (`framework/skills/`, `framework/role-packs/requirements-engineering/skills/`), `framework/runtime/agents/`, `framework/runtime/permissions.json`, `framework/core/08-skill-conventions.md`, die Manifeste der Client Packs, `install.py`, `koexistenz.py`, Prüfungen 5, 49, 111, Sondenteil 19; Produktdokumentation; `docs/DOCUMENTATION_STANDARD.md` |
| Ebene laut Entscheidungsbaum 6 | Framework Core (Skills, Werkzeuge, Validator, Dokumentation) und alle Client Packs |
| Art | MAJOR-Release: Die Befehlsnamen der Skills ändern sich |
| Dringlichkeit | geplant (Owner 2026-10-02: *„Ja, wie empfohlen“*) |
| Status | 🟢 **umgesetzt** – Release `2.0.0` |

---

## 1. Anlass

Eine Rückmeldung zum öffentlichen Repositorium am 2026-10-02: Verweise auf `CR-`, `D-` und `K-` sowie Entscheidungsbegründungen gehören nicht in die Produktdokumentation; die Texte wirken generiert, schwer verständlich und aufgebläht. Das Skill-Präfix `fw-` passt nicht mehr zum Namen Koolie, und `role-re-ticket` weicht davon noch einmal ab.

## 2. Vorprüfung

- 576 Markdown-Dateien, davon 374 Nachweisschicht und 202 Produktdokumentation (223.700 Wörter, 2.783 Kennungen).
- `fw-<skill>` rund 4.300-mal in 327 Dateien; Präfixlogik in `install.py` (über `core_skill_prefix`), `koexistenz.py`, `pruefungen/bestand.py`, `pruefungen/testkatalog.py`, `pruefungen/overlay.py` und den Sondenteilen 4 und 16.
- Ein aktivierter Pack-Skill gilt `install.py` als aktiviert, solange sein Ordner in der Skill-Ablage liegt – ohne Migration fiele `koolie-ticket` beim Heben still aus der Aktivierung.
- Außerhalb der Nachweisschicht: 1.074 Nennungen in 148 Dateien.

## 3. Vorlage zur Entscheidung

| # | Frage | Entscheidung |
|---|---|---|
| F1 | Was wird bereinigt? | Nur die Produktdokumentation; die Nachweisschicht (Decision Log, `CHANGELOG`, Änderungsanträge, Protokolle, Ergebnisspalten der Testblätter, Erhebungen) bleibt, die Git-Historie ebenso |
| F2 | Umfang | Kennungen und Begründungsprosa aus allen Produktdateien; stilistisch neu nur die rund 15 meistgelesenen; der Rest und `build/doc/` in Folge-Releases |
| F3 | Skills und Laufzeitregeln | Anweisungstexte bleiben unverändert (D-303); nur Kennungen und Begründungen in den Erläuterungen fallen weg |
| F4 | Präfix | `koolie-` |
| F5 | Geltung | Alle mitgelieferten Skills, auch aus Packs (`role-re-ticket` → `koolie-ticket`); eindeutig über alle Packs; projekteigene bleiben `prj-`. Auf Rückfrage am 2026-10-02 auch das Agentenprofil (`koolie-reviewer`) |
| F6 | Migration | `install.py --update` benennt selbst um, mit Meldung |
| F7 | Version | `2.0.0` |
| F8 | Schreibregeln | Im Dokumentationsstandard und im Entwicklungsprofil; neue Prüfung 113 meldet Kennungen außerhalb der Nachweisschicht |
| F9 | Messung | Namensanpassung, keine Zelle öffnet sich; drei Stichprobenläufe `claude-code`, Deckel 5 Läufe / 4 USD |
| F10 | Ideen des Owners | Drei Posten ohne Ziel-Release in der Roadmap, je mit eigener Kennung |

## 4. Umsetzung

1. Umbenennung: dreizehn Kernskills, `koolie-ticket`, `koolie-reviewer`; Verweise außerhalb der Nachweisschicht; Präfixlogik in Code, Prüfungen und Sonden; Namensregel in `08-skill-conventions.md`; Eindeutigkeit über alle Packs in Prüfung 5.
2. Migration in `install.py --update` (auch `--check` und `--dry-run`), Sondenteil 19 (D539a bis D539h).
3. Skillversionen je um eine Patchstufe angehoben, Verlaufszeile *Namensanpassung*; die Standmarken der Prüfung 103 bestätigt, wo der Gegenstand sich nachweislich nur durch die Ersetzung und die Versionszeile änderte (vier Testblätter).
4. Prüfung 113 (Sondenteil 20) und die Schreibregeln in `docs/DOCUMENTATION_STANDARD.md` Abschnitt 3 und im Entwicklungsprofil. Ausgenommen sind neben der Nachweisschicht die Ergebnis- und Belegspalten der Testblätter und Grenzfälle, die Belegspalte der Fähigkeitsmatrix und Versionsverläufe (Owner 2026-10-02).
5. Kennungen entfernt: 980 in einem mechanischen Durchgang (nur Klammerverweise, kein Satz geändert), 122 von Hand. Das Verbot des Modus ohne Rückfragen stand bisher nur im Decision Log und steht jetzt in `framework/core/03-security.md` Abschnitt 4. In Anweisungstexten fiel nur der Verweis; die Standmarken zweier Testblätter sind mit Nachweis bestätigt.
6. F10: `K-213` bis `K-215` ohne Ziel-Release.
7. Stil: Übernahmeleitfaden, `clients/README.md`, Quickstart (de/en), `CONTRIBUTING.md`, `paketquellen/README.md` und `.koolie/QUELLREPOSITORIUM.md` neu gefasst; README, Onboarding (Quick-Start, Leitfaden, Referenz) und Checklisten (README, 01, 10) durchgesehen und nur punktuell berichtigt. Prüfung 113 erfasst auch `.koolie/` außerhalb des Kerns, ohne das Overlay.
8. Messung (F9): drei Stichprobenläufe `claude-code` 2.1.287 – Slash-Aufruf, modellseitiger Aufruf, gehobenes Projekt –, alle tragen, 0 Abweisungen, 1,49 USD (`tests/protocols/2026-10-02-oeffentlicher-auftritt-2.0.0.md`).
9. Übrige Produktdokumente, Gruppe 1 (Regeln und Prozesse): Release-Prozess, Checkliste 11, Entwicklungsprofil, Bestandsliste, Glossar der Laufzeitbegriffe und Overlay-Muster `general` neu gefasst; Prioritätshierarchie, Kernregeln 01, 03, 05 und 08, Packs, Prompt-Vorlagen (nur Prosa, die Vorlagentexte unverändert), Overlay-Vorlage und Übungsregister punktuell. In `03-security.md` und `05-working-model.md` fielen nur Versionsangaben und Fettdruck; die Standmarke von `koolie-refactor` ist mit Wortdiff bestätigt (Owner 2026-10-02). Zwei sachliche Berichtigungen: Das Pack `software-development` nennt den fehlenden Schritt `install.py --update` und alle dreizehn Kernskills; die Overlay-Vorlage nennt in Abschnitt 6 Prüfung 89 für die Konfigurationslisten.
10. Gruppe 2: Die fünf `CLIENT_PACK.md` sprachlich überarbeitet (`claude-code` 0.27.0, `devin-desktop` 0.15.0, `openai-codex` 0.2.0, `cursor` 0.4.0, `kiro` 0.2.0, je mit Verlaufszeile); Belegspalte der Matrix und bisherige Verlaufszeilen gegen den Vorstand geprüft und wörtlich gleich, die Vorlage unverändert. Eine sachliche Berichtigung: `openai-codex` Abschnitt 7.1 nennt für die Befehlsregeln im Benutzerverzeichnis die strengste Entscheidung, wie die Belegzelle von B6 sie belegt.
11. Gruppe 3: Die Erläuterungen der Skills (`EXAMPLES.md`, Vorspann der Testblätter) waren schon im Stil; geglättet ist nur der Warnsatz „Gesetzt heißt nicht freigegeben“ in drei Testblättern. Die Gegenprobe 31 sucht die Summenzeile der Matrix ohne Fettdruck.
12. Gruppe 4: Prüfung 113 erfasst das Hauptdokument; Nachweis bleiben nur die Kapitel 29 (Grenzen und offene Entscheidungen), 31 (Anhänge) und 32 (Abschluss), der Rest von `build/` ist kein Produkttext (Owner 2026-10-02). Sonde 113d und Gegenprobe 113c; `docs/DOCUMENTATION_STANDARD.md` 0.3.1 nennt die Ausnahme. Die übrigen Kapitel ohne Kennungen und Entscheidungsgeschichte; berichtigt sind veraltete Zählungen und Aussagen (fünf Client Packs, dreizehn Kernskills, Verzeichnisbaum mit `cursor`, `kiro` und vier Kernskripten, Overlay-Sperre durch den Schutz-Hook statt `deny`, Grenzen der Wurzel-Anweisung wie der Validator sie hält, zwölf Testklassen, Installation über Paketquellen).
13. Trusted Publishing (Owner 2026-10-02, D-541, `K-210` geklärt): Workflow `.github/workflows/publish.yml`, Prüfung 112 Gegenstand d mit Sonden 112k bis 112n, Allowlist um die Adressen der Veröffentlichung, `RELEASE_PROCESS.md` 0.5.0 Schritt 9 mit Einrichtung und Rückfall, `paketquellen/README.md`. Lokal gemessen: `actionlint` ohne Befund, Bau und Probe aus dem Wheel, Signaturprüfung an `v1.25.0` mit Gegenprobe.
14. Release `2.0.0`: `VERSION`, `CHANGELOG` mit Migrationshinweis, Roadmap, Bestandsliste.

## 5. Entscheidung

🟢 **Angenommen am 2026-10-02** (alle Empfehlungen).

| # | Entscheidung | Decision Record |
|---|---|---|
| F4 bis F7 | Präfix, Geltung, Migration, Version | D-539 |
| F1 bis F3, F8 | Nachweisschicht, Umfang, Anweisungstexte, Prüfung 113 und Schreibregeln | D-540 |
| F10 | Ideen des Owners | `K-213` bis `K-215` |
