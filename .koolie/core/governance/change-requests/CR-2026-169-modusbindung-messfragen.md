# Änderungsantrag `CR-2026-169`

| Feld | Inhalt |
|---|---|
| Titel | Modusbindung M3 bis M5 und die offenen Messfragen – und der Befehl im Folgeturn, den es nicht gab |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-10-01 |
| Betroffene Artefakte | `mandat.py`, `tests/scripts/hook-check-secrets.py`, `tests/scripts/pruefungen/berechtigungen.py` (Prüfung 99), `tests/scripts/sonden/teil18_modusbindung_m3_m5.py` (neu), `tests/scripts/probe-pruefungen.py`, `framework/runtime/rules/00-framework-core.md`, `framework/core/05-working-model.md`, `build/doc/29-grenzen.md`, `clients/claude-code/CLIENT_PACK.md`, Testblätter `fw-change-analyze`, `fw-plan`, `fw-bugfix-prepare`, `fw-refactor` (Stand bestätigt), `onboarding/exercises/README.md`, `docs/ROADMAP.md` |
| Ebene laut Entscheidungsbaum 6 | Framework Core (Schutzschicht, Arbeitsmodell, Testblätter) |
| Art | Erweiterte technische Durchsetzung und Messung; MINOR-Release mit Kontingent; die Laufzeitschicht ändert einen Satz ohne neue Zeile |
| Dringlichkeit | geplant (`K-201`, `K-186`, `K-202`, `K-203`; Roadmap-Zeile `1.23.0`, D-518) |
| Status | 🟢 **entschieden am 2026-10-01** (E1 bis E8) |

---

## 1. Anlass

Nach `1.22.0` stehen in einem Release zusammen: die Bindung der Modi M3 bis M5 an den Schutz-Hook (`K-201`), die drei offenen Messfragen aus `1.18.0` (`K-186` (1), (4), (5)), der Auftrag gegen die Regel ohne technische Schicht (`K-202`) und, bei Bedarf, die Erweiterung der Vergleichsmessung (`K-203`).

## 2. Vorprüfung

Vorgelegt am 2026-10-01 mit Schätzung (rund 24 Läufe `claude-code`, rund 11 USD, Deckel 30 Läufe und 20 USD); die Vorlage liegt außerhalb des Repositoriums. Der Owner folgt den Empfehlungen. Vor der Vorlage gelesen: Der Leseweg für die Pfadlisten besteht schon (`mandat.py abgleichen`, D-452); die Werte der drei gemessenen Overlays haben drei Gestalten, darunter einen Glob mitten im Pfad – ein Präfixvergleich wie bei M2 trägt sie nicht; Regel 00 nennt die Bindung in einem Satz, der sich ohne neue Zeile umformulieren lässt.

## 3. Vorlage zur Entscheidung

| # | Frage | Entscheidung | Preis |
|---|---|---|---|
| E1 | Wie kommt der Hook an die Pfadliste? | `mandat.py modus` kopiert sie beim Binden in die Bindung, dazu `<READ_ONLY_PATHS>`; der Hook liest das Overlay nicht (D-523) | Momentaufnahme bis zum nächsten Binden |
| E2 | Wie wird ein Glob ausgewertet? | `**`, `*`, `?`, ohne Joker genau die Datei, ohne Groß- und Kleinschreibung; jede Lesart muss im Projekt liegen; Nur-Lese-Pfade bleiben gesperrt (D-523) | Klammern und Mengen gelten wörtlich |
| E3 | M3 mit engerem Scope? | `--umfang`, ausgewertet als Schnittmenge mit `<ALLOWED_PATHS>`; leere oder offene Liste bindet nicht (D-523) | – |
| E4 | Prüfung? | Keine neue Nummer: Prüfung 99 vergleicht den Rumpf von `glob_muster` in Hook und `mandat.py`; Sondenteil 18 (D-523) | Abweichung von der Vorlage, die Prüfung 113 vorsah |
| E5 | `K-186` (1) und (4) | Neue Zelle `SK-003-P05`, Nachstellung von `SK-009-P01`; keine Anweisungsänderung; die Kappung nach Aktualität wird `K-207` (D-524) | – |
| E6 | `K-186` (5) | Der Beleg war eine Fehllesung; die Sperre eines Skills gilt nur in seinem Turn – benannte Grenze in S3 (D-525) | – |
| E7 | `K-202` | Auf `cursor` und `openai-codex` ausgedehnt; nicht reproduziert, geklärt (D-526) | Zwei Läufe `cursor` unerhoben |
| E8 | `K-203` | Nicht in diesem Release, ohne Ziel – kein Bedarf aus einem Projekt | – |

## 4. Umsetzung

1. **Bindung:** `mandat.py modus M3|M4|M5` mit `--umfang`; Hook `glob_muster` und `modus_erlaubt`; `MODUS_GEBUNDEN` in beiden Dateien auf M1 bis M5.
2. **Prüfung 99** vergleicht den Rumpf von `glob_muster`; Sondenteil 18 (`K201a` bis `K201n`).
3. **Texte:** Regel 00 Zeile 31 (ein Zeichen kürzer), `05-working-model.md` M3 bis M5, Hauptdokument Kapitel 29, Fähigkeitsmatrix `claude-code` (Zeilen M4 und S3).
4. **Testblätter:** `SK-003-P05` neu, `SK-004-N04` berichtigt, `SK-009-P01` nachgestellt, Stand von `SK-007-N06` bestätigt; Übungsregister `UEB-33`, `UEB-34`.

## 5. Entscheidung

🟢 **Angenommen am 2026-10-01.**

| # | Entscheidung | Decision Record |
|---|---|---|
| E1 bis E4 | Die Modusbindung M3 bis M5 | D-523 |
| E5 | Suche und Beifund gemessen | D-524 |
| E6 | Die Sperre eines Skills im Folgeturn | D-525 |
| E7 | Auftrag gegen die Regel | D-526 |
| E8 | Vergleichsmessung | – (`K-203` bleibt offen) |

## 6. Messung und Belege

Protokoll `tests/protocols/2026-10-01-modusbindung-messfragen.md`. 21 Sitzungsläufe `claude-code`, 11,08 USD (5 verworfen, Messaufbau); `cursor` 1 Lauf, `openai-codex` 3 Läufe. Erhebungsablage `leitwerk-erhebungen-2026-10-01-1230` außerhalb des Repositoriums.
