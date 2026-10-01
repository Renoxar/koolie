# Änderungsantrag `CR-2026-172`

| Feld | Inhalt |
|---|---|
| Titel | Ein neuer Auftritt, npm unter dem Scope und die Suche nach dem Ältesten – und der Name, den npm für `cookie` hielt |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-10-01 |
| Betroffene Artefakte | `README.md`, `README.en.md`, `CONTRIBUTING.md` (neu), `QUICKSTART.md`, `QUICKSTART.en.md`, `docs/ADOPTION_GUIDE.md` (Abschnitte 2 und 9), `paketquellen/bauen.py`, `paketquellen/README.md`, `governance/RELEASE_PROCESS.md`, `framework/skills/fw-change-analyze`, `fw-plan`, `fw-bugfix-prepare` (SKILL, CHANGELOG, TESTS), `clients/claude-code/CLIENT_PACK.md` (Zeile B2), `tests/scripts/pruefungen/bestand.py` (Allowlist), `tests/scripts/sonden/teil17_paketquellen.py`, `tests/scripts/validate-framework.py`, `docs/ROADMAP.md` |
| Ebene laut Entscheidungsbaum 6 | Framework Core (Skills, Werkzeuge, Validator, Release-Prozess), Client Pack `claude-code` und Einstieg des Repositoriums |
| Art | MINOR-Release: Anweisungsänderung in drei Skills mit Nachlauf, neuer Auftritt, npm-Name |
| Dringlichkeit | geplant (Owner 2026-10-01: *„mach 1.25.0“*) |
| Status | 🟢 **entschieden am 2026-10-01** (E1 bis E6) |

---

## 1. Anlass

Drei Dinge kamen am 2026-10-01 zusammen: npm wies das Paket `koolie` beim ersten Hochladen ab (*„too similar to existing package cookie“*); eine Rückmeldung aus dem Umfeld des Owners nannte die README *viel zu lang und zu detailliert* – ein Leser, der über das Repositorium stolpert, wird nicht abgeholt; und die Roadmap führte `K-207` (die Suchgrenze schneidet die ältesten Treffer ab) und `K-208` (ein lesender Befehl ohne Korb lief ohne Rückfrage).

## 2. Vorprüfung

- **README:** 444 Zeilen, 4.315 Wörter, 19 Abschnitte, 16 Verweise auf `CR-`, `D-` oder `K-`. Die Installationsbefehle standen zugleich im Übernahmeleitfaden.
- **npm:** Ein Paket mit Scope ist ohne `publishConfig.access: public` privat; der Befehl bleibt über `bin` `koolie`.
- **`K-207`:** Die Anweisung steht wortgleich in drei Skills; nach D-303 öffnet ihre Änderung alle Zellen der drei Testblätter – 27 Zellen statt der zuerst geschätzten zehn. Der Owner wählte die volle Lösung mit Deckel 35 Läufe und 22 USD.

## 3. Vorlage zur Entscheidung

| # | Frage | Entscheidung | Preis |
|---|---|---|---|
| E1 | Name auf npm | `@renoxar/koolie`, öffentlich; der Befehl bleibt `koolie` (D-535) | Zwei Paketnamen |
| E2 | Auftritt | README als Startseite, Maintainer-Inhalte in `CONTRIBUTING.md`, Befehle im Übernahmeleitfaden; deutsch und englisch gleich gekürzt; keine Kennungen auf der Startseite (D-538) | Belege eine Ebene tiefer |
| E3 | `K-207` | Zweite Suche mit den ältesten zuerst, in allen drei Skills, mit vollem Nachlauf (D-536) | Eine Suche mehr; rund 30 Sitzungsläufe |
| E4 | `K-208` | Trennlauf mit und ohne `deny`-Eintrag (D-537) | – |
| E5 | Badges | ja, die Allowlist nimmt Paketseiten und Badges eng gefasst auf (D-535) | – |
| E6 | Veröffentlichung | PyPI mit der Signatur (D-530); vor dem ersten Hochladen auf npm unter dem neuen Namen eine Rückfrage beim Owner | – |

## 4. Umsetzung

1. README und `README.en.md` neu, `CONTRIBUTING.md` neu, Übernahmeleitfaden Abschnitt 2 (Paketquelle) und 9 (Befehle), Quickstart-Verweise.
2. `bauen.py`: `NPM_NAME`, `publishConfig`; Nachprüfung meldet einen anderen Namen oder fehlenden öffentlichen Zugang; Sonde `112j`.
3. Die Suchanweisung in den drei Skills, Versionen 0.1.7, 0.1.9, 0.1.9; Nachlauf aller Zellen.
4. Zeile B2 der Fähigkeitsmatrix `claude-code` (0.26.4).

## 5. Entscheidung

🟢 **Angenommen am 2026-10-01.**

| # | Entscheidung | Decision Record |
|---|---|---|
| E1, E5 | npm unter dem Scope, Badges | D-535 |
| E3 | Die zweite Suche | D-536 |
| E4 | Der lesende Befehl ohne Korb | D-537 |
| E2 | Der Auftritt | D-538 |
| E6 | Veröffentlichung | D-530 (unverändert) |

## 6. Messung und Belege

Protokoll `tests/protocols/2026-10-01-auftritt-und-suche.md`. Erhebungsablage `leitwerk-erhebungen-2026-10-01-1250` außerhalb des Repositoriums.
