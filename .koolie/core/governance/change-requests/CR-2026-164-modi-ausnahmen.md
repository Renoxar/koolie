# Änderungsantrag `CR-2026-164`

| Feld | Inhalt |
|---|---|
| Titel | Die Modusbindung und die registrierte Ausnahme – und der Upload, an dem das Leseverbot vorbeiging |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-30 |
| Betroffene Artefakte | `framework/runtime/root-instruction.md`, `framework/runtime/rules/00-framework-core.md`, `framework/runtime/rules/10-privacy-security.md`, `framework/core/05-working-model.md`, `governance/PRIORITY_HIERARCHY.md`, `mandat.py`, `wirksamkeit.py`, `tests/scripts/hook-check-secrets.py`, `tests/scripts/pruefungen/` (Prüfungen 99, 109, 110), `tests/scripts/validate-framework.py`, `tests/scripts/probe-pruefungen.py`, `tests/scripts/sonden/teil14_modi_ausnahmen_skills.py` (neu), `clients/claude-code/CLIENT_PACK.md`, `clients/devin-desktop/CLIENT_PACK.md`, `clients/kiro/CLIENT_PACK.md`, `templates/project-overlay/OVERLAY.md`, `framework/role-packs/README.md`, `framework/skills/fw-refactor/TESTS.md` (Stand), Hauptdokument (Kap. 29); `governance/DECISION_LOG.md`, `docs/ROADMAP.md`, `tests/TEST_CATALOG.md`, `CHANGELOG.md`, `VERSION` |
| Ebene laut Entscheidungsbaum 6 | Framework Core (Laufzeitschicht, Schutz-Hook, Validator, Client Packs) |
| Art | Erweiterung ohne Overlay-Bruch; PATCH-Release mit Kontingent, das die Laufzeitschicht berührt |
| Dringlichkeit | geplant (D-485) |
| Status | 🟢 **entschieden am 2026-09-30** (E1 bis E7) |

---

## 1. Anlass

Aus dem Schnitt der Schutzschicht (D-485) trägt `1.20.2` die Modi, die Ausnahmen und die eingebauten Skills: die Modusgrenzen außer M6 (`K-179`), der Schutz ohne Hook bei `kiro` (`K-181`), die registrierte Ausnahme in der Laufzeitschicht (`K-54`), der eingebaute Skill `upload-secrets` (`K-94`), die aktivierten Packs gegen den Bestand (`K-44`) und die Werkzeugfelder der Skills (`K-93`). Das Tor ist das Zeichenbudget des Piloten (`K-185`): Das Release berührt als erstes der Reihe die Laufzeitschicht.

## 2. Vorprüfung

Vorgelegt am 2026-09-30 mit Schätzung: 6 Läufe `claude-code`, rund 3 USD, Deckel 14 Läufe und 8 USD, dazu 2 Läufe `kiro` und 2 Läufe `devin-desktop` als Probelauf, ein bis zwei Sitzungen. Die Vorlage liegt außerhalb des Repositoriums. Der Owner folgt den Empfehlungen. Vor der Vorlage erhoben, ohne Modell:

- Der Pilot stand bei 39.998 von 40.000 Zeichen, seine `CLAUDE.md` genau auf 12.000 – jedes Zeichen des Halbsatzes zu `K-54` hätte Budget und Dateischwelle gerissen.
- `devin skills show upload-secrets` (3000.11.3): Der Skill ruft `devin.exe cloud drs secret-create --from-dotenv .env`; die CLI liest die Werte selbst. Ein Leseverbot der Berechtigungsschicht trifft diesen Weg nicht, und mit `--from-env` und einem Variablennamen steht kein Pfad im Befehl.
- Die Kernquelle führt `ask write **`; bei `kiro` wird eine Rückfrage ohne Rückfragekanal zur Abweisung (`QK-1`).

## 3. Vorlage zur Entscheidung

| # | Frage | Entscheidung | Preis |
|---|---|---|---|
| E1 | Woher kommt der Platz für `K-54` (Tor `K-185`)? | Aus dem Kern: Wurzel-Anweisung, Regel 00 und Regel 10 werden ohne Regeländerung gestrafft, zusammen −748 Zeichen (D-499) | Zwei Aussagen stehen nur noch als Verweis auf ihren zweiten Ort |
| E2 | Wie lernt die Laufzeitschicht die registrierte Ausnahme (`K-54`)? | Ein Halbsatz in Abschnitt 2 der Wurzel-Anweisung und in Regel 2.1 der Prioritätshierarchie (D-500) | Die Gegenprobe trennt nicht: alt wie neu urteilten richtig |
| E3 | Trägt das Muster des Mandats die übrigen Modi (`K-179`)? | Für M1 und M2: `mandat.py modus`, der Hook sperrt Schreibwerkzeuge außerhalb der Plan-Ablage; keine neue Zeile in der Laufzeitschicht (D-501) | Shell-Befehle entgehen der Bindung; M3 bis M5 bleiben normativ (`K-201`) |
| E4 | Wie wird `kiro` ohne Hook geschützt (`K-181`)? | Keine statische Sperre im Profil; gemessen trägt die Rückfrage, `--trust-all-tools` öffnet das Overlay (D-502) | Im untersagten Modus ist das Overlay bei `kiro` ungeschützt |
| E5 | Was geschieht mit `upload-secrets` (`K-94`)? | Der Hook sperrt `cloud drs secret-create` für jedes ausführende Werkzeug; die Wirksamkeitsprobe prüft es (D-503) | Das Muster kennt nur diesen Befehl |
| E6 | Aktivierte Packs gegen den Bestand (`K-44`) | Prüfung 110 unter `--strict-overlay`; die Vorlage führt die Zeile für Role Packs (D-504) | Nennung und Laufzeitfassung, nicht Skills und Version |
| E7 | Werkzeugfelder der Skills (`K-93`) | Prüfung 109: beide oder keines (D-505) | Die Anwesenheit, nicht die Wirkung |

## 4. Umsetzung

1. **Laufzeitschicht:** Wurzel-Anweisung (Herkunftskommentar gekürzt, zwei Doppelungen entfernt, Halbsatz zur Ausnahme), Regel 00 (Absatz zur Modusgrenze mit der Bindung, kürzer), Regel 10 (V6 als Verweis).
2. **Schutz-Hook:** `MODUS_DATEI`, `modus_lesen()`, die Sperre der Bindung nach allen übrigen Sperren; `koolie-modus` in den Mandatsmustern; `UEBERTRAGUNGS_MUSTER` für `cloud drs secret-create`.
3. **Werkzeuge:** `mandat.py modus M1|M2|aus` und die Anzeige in `status`; die Wirksamkeitsprobe sperrt in H3 zusätzlich den Secret-Upload.
4. **Prüfungen:** 99 hält Datei und Befehl der Bindung, 109 und 110 neu. Sonden `99e`, `107d`, `109`, Bündel `110a` bis `110d` und `sonden_modusbindung` (`D501` bis `D501j`, `D503`) in Teil 14.
5. **Packs:** `claude-code` Zeile M4 (0.26.2), `devin-desktop` Zeile zu den Skills, die das Modell erreicht (0.14.8), `kiro` Zeile B4 (0.1.2).
6. Langform M1 und M2, Overlay-Vorlage (Zeile „Aktivierte Role Packs“), Role-Pack-Anleitung, Hauptdokument Kap. 29, Register, Roadmap, Testkatalog, CHANGELOG, `VERSION`. Der Stand der Zelle `SK-007-N06` ist bestätigt: Die Änderung an `05-working-model.md` betrifft M1 und M2, nicht den Arbeitsschritt 5 von `fw-refactor`.

## 5. Entscheidung

🟢 **Angenommen am 2026-09-30.**

| # | Entscheidung | Decision Record |
|---|---|---|
| E1 | Das Tor im Kern öffnen | D-499 |
| E2 | Die registrierte Ausnahme in der Laufzeitschicht | D-500 |
| E3 | Die Modusbindung für M1 und M2 | D-501 |
| E4 | `kiro` ohne Hook | D-502 |
| E5 | `upload-secrets` und der Upload über die CLI | D-503 |
| E6 | Prüfung 110 | D-504 |
| E7 | Prüfung 109 | D-505 |

## 6. Messung und Belege

Protokoll `tests/protocols/2026-09-30-modi-ausnahmen.md`. 7 Sitzungsläufe mit `claude-code` (0,83 USD nach Listenpreis), 2 Läufe mit `kiro` (0,31 Credits), 2 Läufe mit `devin-desktop`; dazu Messungen ohne Modell (Hook synthetisch, Wirksamkeitsprobe, Zeichenbudget). Erhebungsablage `leitwerk-erhebungen-2026-09-30-1202` außerhalb des Repositoriums.
