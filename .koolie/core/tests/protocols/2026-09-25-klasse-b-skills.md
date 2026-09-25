# Protokoll: Die Durchsicht der Klasse B, dritter Bereich – und die Anweisung, die stehen bleibt

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-25 |
| Release | `1.9.3` |
| Änderungsantrag | `CR-2026-145` |
| Art | Durchsicht der Skills, der Vorlagen und der Vorlage des Client Packs nach `docs/DOCUMENTATION_STANDARD.md` – **keine Sitzung mit einem Client, kein Kontingent** |
| Gegenstand | 13 `SKILL.md`, `templates/` (Vorlagen, Overlay-Vorlage, Regelvorlagen), `clients/_template/CLIENT_PACK.md`; gelesen, nicht geändert: `TESTS.md`, `EXAMPLES.md`, `CHANGELOG.md` der Skills (Klasse C) |
| Ergebnis | 🟢 **Entschieden, `D-393` und `D-394`.** Keine Anweisung eines Skills geändert, alle 87 Ergebniszellen bleiben abgenommen; zwei Skills in ihrer Erläuterung berichtigt, vier Vorlagen und die Pack-Vorlage überarbeitet; die Befunde als `K-148` bis `K-151`, die Stützung von D-303 als `K-146`, Kiro als `K-147` |

---

## 1. Was gefragt war

Wiederaufnahmepunkt von `1.9.2`, Punkt 2: die Durchsicht der Klasse B, dritter Bereich
(D-380), und vorher die Klärung, wie eine Änderung an einer `SKILL.md` mit Version,
Änderungsverlauf und dem erneuten Auslösen der Testfälle umgeht (D-303). Fragen (a) bis (j)
vorgelegt am 2026-09-25 und angenommen. Während des Baus fragte der Owner, ob sich das
Framework mit Kiro einsetzen lässt; beantwortet aus der Produktdokumentation und als `K-147`
angelegt. `CR-2026-145` E1 bis E10.

## 2. Messungen vor und nach dem Bau

Je eine Testinstallation je Pack aus `v1.9.2` und aus dem neuen Baum
(`install.py --client <pack> --root <leer>`), Zeichen, nicht Bytes.

| Installierter Skill | `claude-code` | `devin-desktop` | `openai-codex` |
|---|---|---|---|
| `fw-docs-update/SKILL.md` vorher → nachher | 17.735 → 17.668 | 17.738 → 17.671 | 17.738 → 17.671 |
| `fw-tests/SKILL.md` vorher → nachher | 14.869 → 14.867 | 14.992 → 14.990 | 14.991 → 14.989 |

**Sonst ist die installierte Laufzeitschicht aller drei Packs unverändert** – Wurzel-Anweisung,
Regeln, Berechtigungen, Hooks und die übrigen elf Skills byte-gleich; die Summe des stets
Geladenen (D-387) ändert sich nicht. Neu erzeugt wird außerdem die Overlay-Vorlage, die nur
bei einer Erstinstallation in ein Projekt kommt.

## 3. Die Durchsicht

Fünf parallele Durchgänge nach einem gemeinsamen schriftlichen Auftrag (Kriterien der Klasse
B; in einer `SKILL.md` nur Schreibung, Verweise auf dieselbe Sache, Erläuterung und Form;
Frontmatter unverändert; keine `SKILL.md` länger; Sondenanker vor jeder Änderung gegen
`probe-pruefungen.py` gehalten; Änderungen nur mit dem Edit-Werkzeug; Validator nach jeder
Datei). Die Diffs hat der Koordinator gelesen.

| Durchgang | Geändert | Art |
|---|---|---|
| `fw-bugfix-prepare`, `fw-change-analyze`, `fw-change-small` | – | – |
| `fw-code-explain`, `fw-docs-update`, `fw-error-analyze` | `fw-docs-update` Abschnitt 4 (17.912 → 17.845 Zeichen in der Quelle) | *Erläuterung*: Herleitung (*„Der bisherige Verweis … ist widerlegt“*) durch die geltende Aussage ersetzt, `PreToolUse` durch den Kernbegriff *Schutz-Hook*; Messung, Protokollverweis und D-48 bleiben |
| `fw-mr-description`, `fw-plan`, `fw-refactor` | – | – |
| `fw-repo-analyze`, `fw-review-support`, `fw-tests`, `role-re-ticket` | `fw-tests` Abschnitt 4 (15.155 → 15.153) | *Erläuterung*, sachlich berichtigt: Sie sagte, ein Hook mit Pfadprüfung sichere die Testpfade technisch ab; der mitgelieferte Schutz-Hook (`framework/runtime/hooks.json`) prüft keine Testpfade |
| Vorlagen, Pack-Vorlage | `SKILL_TEMPLATE.md` (7.633 → 8.041), `CLIENT_PACK.md` (12.463 → 12.548), `OVERLAY.md` (23.846 → 23.379), `overlay-manifest.yaml`, 13 `.gitkeep.md` | *Berichtigung gegen Modul*: `SKILL_TEMPLATE.md` an `08-skill-conventions.md` Abschnitte 2, 3 und 5 (Quelle und installierte Fassung, D-388; `model`/`subagent`/`agent` nur mit Begründung; Beispiele synthetisch). `CLIENT_PACK.md`: `root-template/` trägt nur die README der Laufzeitschicht (`clients/README.md` Abschnitt 5, D-20); Zeile A1 nennt die Kernquelle des Reviewprofils. *Herleitung → Verweis*: `CLIENT_PACK.md` (Vorbemerkung B-Block), `OVERLAY.md` Abschnitte 4, 6 und 21. *Schreibung*: Umlaute in `overlay-manifest.yaml` und den `.gitkeep.md` |

**Verweisberichtigungen innerhalb einer Anweisung (D-393 (a)): keine.** Geprüft und stimmig:
die Abschnittsverweise auf die Core-Module, die Kennungen R, V, Q, RV und T, die Zeilen S2, S3
und A1 der Fähigkeitsmatrix, die Pfade der Checklisten und Vorlagen, die Platzhalter; die als
wörtlich ausgewiesenen Zitate aus `09-risk-model.md` Abschnitt 3 stimmen Wort für Wort.

**Entfallene Kennungen** – jede steht weiter in anderen Trägern: `CR-2026-066` und `B08` (aus
`OVERLAY.md`; Decision Log, Changelog, Checkliste 10), `AP2-DD-12` (aus `CLIENT_PACK.md`; D-35,
Pack `devin-desktop`, `CR-2026-030`).

**Befunde, die eine Entscheidung brauchen** – als Klärungspunkte angelegt, nicht behoben
(D-393 (a), D-394):

| Kennung | Gegenstand |
|---|---|
| `K-148` | Vier abgenommene Zellen, deren Ergebnis ihre Erwartung nicht deckt: `SK-005-P02`, `SK-002-N03`, `SK-007-N01`, `SK-011-P01` |
| `K-149` | Skills gegen Modul, Fähigkeitsmatrix und Role Pack: Planablage und Zeile M4, Aufrufform bei `openai-codex`, sitzungsweite Freigaben in `fw-change-small`, V7 in `fw-mr-description`, Randbedingung aus Tests in `role-re-ticket` |
| `K-150` | Register der Skills: Version `v0.1.1` in allen Beispielen, fünf Beispiele sachlich schief, Verlaufszeilen außer der Reihe, Modusname im Testblatt von `fw-change-small` |
| `K-151` | Pack-Vorlage ohne B10, H4, A2; R1 nennt `AGENTS.md` (Anker der Gegenprobe 73c); *automatischer* statt *selbsttätiger* Übernahme; Regelvorlage 21 gegen `openai-codex`; Kommentar in `clientmap.py` |

Nicht als Klärungspunkt geführt: Die Anführungszeichen schließen im Kern überwiegend mit dem
geraden Zeichen („…"), rund 1.389 gegen 374 Stellen. Prüfung 92 verlangt das typografische nicht;
eine Angleichung wäre ein eigener Durchgang über den ganzen Bestand.

## 4. Abnahme

| Lauf | Ergebnis |
|---|---|
| Validator | 0 Fehler, 0 Warnungen, beide Kodierungsumgebungen |
| Sondenlauf | **344** Einheiten, alle bestanden, beide Kodierungsumgebungen zeilengleich (602 Zeilen), rund 690 s Wanduhr; Abnahmelauf gegen den fertigen Baum zeilengleich |
| Pilot / Übungsrepositorium | 1 Fehler, 2 Warnungen / 0 Fehler, 1 Warnung – unverändert gegen den Stand vor dem Heben; mit `install.py --target <projekt> --update` gehoben, 561 Kerndateien, dort committet |
| Bau | `v1.9.3` 1.963.850 / 1.965.055 / 1.959.685 Bytes (`devin-desktop` / `claude-code` / `openai-codex`); Kapitel 31 nennt 561 versionierte Dateien, 8 Diagramme je Fassung |

## 5. Was offen bleibt

- `K-146` bis `K-150` für `1.11.0`, `K-151` für `1.10.0`; `K-147` ohne Ziel-Release (D-394).
- Die Grenze zwischen Anweisung und Erläuterung hat der Koordinator gezogen, keine Prüfung
  (D-303); die beiden geänderten Absätze tragen den Vermerk *(Erläuterung)*.
- Die Abnahme des macOS-Starters auf macOS steht weiter aus.
