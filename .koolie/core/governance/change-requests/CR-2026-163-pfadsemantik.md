# Änderungsantrag `CR-2026-163`

| Feld | Inhalt |
|---|---|
| Titel | Die zweite Lesart von `/c/…` und die Schreibweise der Muster – und der Kurzname, der am Kernschutz vorbeischrieb |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-30 |
| Betroffene Artefakte | `tests/scripts/hook-check-secrets.py`, `tests/scripts/pruefungen/` (Prüfungen 32, 89, 108), `tests/scripts/validate-framework.py`, `tests/scripts/probe-pruefungen.py`, `tests/scripts/sonden/teil13_pfad_und_mustersemantik.py` (neu), `clients/claude-code/CLIENT_PACK.md`, `clients/devin-desktop/CLIENT_PACK.md`, `clients/openai-codex/CLIENT_PACK.md`, `templates/project-overlay/OVERLAY.md`, Hauptdokument (Kap. 29); `governance/DECISION_LOG.md`, `docs/ROADMAP.md`, `tests/TEST_CATALOG.md`, `CHANGELOG.md`, `VERSION` |
| Ebene laut Entscheidungsbaum 6 | Framework Core (Schutz-Hook, Validator, Client Packs) |
| Art | Berichtigung und Erweiterung ohne Overlay-Bruch; PATCH-Release mit Kontingent |
| Dringlichkeit | geplant (D-485) |
| Status | 🟢 **entschieden am 2026-09-30** (E1 bis E8) |

---

## 1. Anlass

Aus dem Schnitt der Schutzschicht (D-485) trägt `1.20.1` die Pfad- und Mustersemantik: zwei Schichten mit zwei Mustersemantiken (`K-92`), die POSIX-Schreibweise unter MSYS (`K-96`), der Inhalt der Pfadschlitze (`K-35`), `allow`-Muster, die ein `deny`-Präfix umschließen (`K-47`), projektrelative `deny`-Globs bei `openai-codex` (`K-160`), Befehlsregeln über Ablagen hinweg (`K-119`) und der an die Shell-Pfadprüfung gekoppelte `K-32`.

## 2. Vorprüfung

Vorgelegt am 2026-09-30 mit Schätzung: rund 5 Läufe, rund 1 USD, Deckel 12 Läufe und 6 USD, ein bis zwei Sitzungen. Die Vorlage liegt außerhalb des Repositoriums. Der Owner folgt den Empfehlungen. Vor der Vorlage gemessen, synthetisch und ohne Modell: Ein Schreibwerkzeug auf `/c/<projekt>/KOOLIE~1/core/VERSION` ging am Schutz-Hook mit Exit 0 durch, dieselbe Angabe in Windows-Form oder relativ sperrte. Beim Bau kam ein zweiter Weg ohne Kurznamen dazu: `/c/<projekt>/.koolie/./core/VERSION`.

## 3. Vorlage zur Entscheidung

| # | Frage | Entscheidung | Preis |
|---|---|---|---|
| E1 | Wohin gehört die MSYS-Schreibweise (`K-96`)? | An die Auflösung im Hook: `/<laufwerk>/…` wird unter Windows in beiden Lesarten aufgelöst, `X:\…` und `C:\<laufwerk>\…`; die strengere gewinnt (D-491) | `/cygdrive/` und `/mnt/` bleiben ungemessen und bei einer Lesart |
| E2 | Welche Mustersemantik gilt (`K-92`)? | Die des Hooks: Pfadidentität, ohne Rücksicht auf Groß- und Kleinschreibung. Die Berechtigungsschicht gehört dem Client; ihre Grenze wird benannt, nicht angeglichen (D-492) | Eine Zusage, die nur die Regel trägt, gilt nur in der Schreibweise des Musters |
| E3 | Inhalt der Pfadschlitze (`K-35`) | „Deckungsgleich“ heißt: Jeder Glob von `<CI_CONFIG_PATHS>` und `<QUALITY_GATE_CONFIG_PATHS>` hat seine eigene Schreibsperre; Prüfung 89 (c) aufgeweitet, keine neue Nummer (D-493) | Nur die Richtung Quelle → Korb, nur unter `--strict-overlay` |
| E4 | `allow` umschließt `deny` (`K-47`) | Prüfung 108 als Warnung: allow-Befehl als echtes Wortpräfix eines deny-Befehls, in der Kernquelle und im installierten JSON-Korb (D-494) | Die Schreibweise, nicht die Befehlsäquivalenz |
| E5 | Projektrelative `deny`-Globs bei `openai-codex` (`K-160`) | Gemessen ohne Modell: Der Glob wird mit 0.157.1 angenommen, das `deny`-Leserecht verlangt weiter den erhöhten Sandkasten; `B3` bleibt `[NICHT ABBILDBAR]` (D-495) | – |
| E6 | Befehlsregeln über Ablagen hinweg (`K-119`) | Gemessen: Die strengste Entscheidung gewinnt, in beiden Richtungen; `B6` braucht keine Bedingung (D-496) | – |
| E7 | Kernänderung über die Shell (`K-32`) | Nicht in `1.20.1`: keine Tokensperre für Strukturpfade in der Shell; eingeplant für `1.21.0` Einsatzarchitektur (D-497) | Der Shell-Kanal in den Kern bleibt offen, wie seit D-30 |
| E8 | Der macOS-Starter | Vom Owner am 2026-09-30 auf macOS abgenommen; die Köderläufe für `cursor` (`K-176`) bleiben beim Owner (D-498) | – |

## 4. Umsetzung

1. **Schutz-Hook:** `lesarten()` neben `aufloesen()`; das Material der Pfadprüfung und die Deckung eines Mandats nehmen alle Lesarten.
2. **Prüfungen:** 32 mit dem Fall c) (POSIX-Schreibweise der Projektwurzel mit Punktsegment, nur unter Windows); 89 (c) für die CI- und Quality-Gate-Pfade; 108 neu. Sonden `32`, `108`, `108a` bis `108c`, `89e`, `89f` in Teil 13.
3. **Packs:** `claude-code` Zeilen B3 und H4 (0.26.1), `devin-desktop` Zeilen B3 und H4 (0.14.7), `openai-codex` Zeilen B3 und B6 (0.1.9).
4. Overlay-Vorlage (Satz zu Prüfung 89), Hauptdokument Kap. 29 (die Grenze der Berechtigungsschicht), Register, Roadmap, Testkatalog, CHANGELOG, `VERSION`.

## 5. Entscheidung

🟢 **Angenommen am 2026-09-30.**

| # | Entscheidung | Decision Record |
|---|---|---|
| E1 | Zwei Lesarten von `/c/…` | D-491 |
| E2 | Die Semantik des Hooks gilt | D-492 |
| E3 | CI- und Quality-Gate-Pfade in Prüfung 89 | D-493 |
| E4 | Prüfung 108 | D-494 |
| E5 | `deny`-Globs bei `openai-codex` | D-495 |
| E6 | Befehlsregeln über Ablagen hinweg | D-496 |
| E7 | `K-32` zu `1.21.0` | D-497 |
| E8 | Der macOS-Starter | D-498 |

## 6. Messung und Belege

Protokoll `tests/protocols/2026-09-30-pfadsemantik.md`. 3 Sitzungsläufe mit `claude-code` (0,11 USD nach Listenpreis), 2 Läufe mit `openai-codex` im Abonnement; dazu Messungen ohne Modell (Hook synthetisch, `codex sandbox`, `codex execpolicy check`). Erhebungsablage `leitwerk-erhebungen-2026-09-30-1201` außerhalb des Repositoriums.
