# Änderungsantrag `CR-2026-143`

| Feld | Inhalt |
|---|---|
| Titel | Die Durchsicht der Klasse B, erster Bereich – und die Grenze ohne Sonde |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-25 |
| Betroffene Artefakte | die elf Module unter `framework/core/` (Durchsicht; zehn geändert); die Laufzeitschicht unter `framework/runtime/` und `framework/role-packs/*/runtime/` (Durchsicht; `agents/fw-reviewer.md` geändert); Modusbegriffe in `onboarding/GUIDE.md`, `onboarding/MENTOR_CHECKLIST.md`, `onboarding/QUICKSTART.md`, `onboarding/REFERENCE.md`, `checklists/01-preflight.md`, `governance/EXCEPTION_PROCESS.md`, `governance/PRIORITY_HIERARCHY.md`, `pilot/PILOT_CONCEPT.md`, `prompts/README.md`, `framework/skills/fw-change-small/SKILL.md`; `.gitignore` und `README.md` der Wurzel; `tests/scripts/validate-framework.py` (Prüfung 45, Gegenstand 3); `tests/scripts/probe-pruefungen.py` (Sonde 45e, Gegenprobe 45c, Bündel `sonden_zeichengrenze`); `tests/TEST_CATALOG.md`; `governance/DECISION_LOG.md` (**D-381** bis **D-384**, `K-130` bis `K-137`); `governance/ADOPTION_REGISTRY.md`; `docs/ROADMAP.md`; `build/doc/00-kopf.md`; `VERSION`, `CHANGELOG.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Regeldokumente, Prüfapparat |
| Art | **PATCH** nach `RELEASE_PROCESS.md` Abschnitt 1: Formulierungen und Berichtigungen, kein Regelinhalt geändert, keine neue Prüfungsnummer, kein Overlay-Feld |
| Dringlichkeit | Posten `1.9.1` nach D-380 |
| Status | 🟢 **entschieden am 2026-09-25** (E1 bis E8), umgesetzt mit `1.9.1` |

---

## 1. Anlass

D-380 hat die inhaltliche Durchsicht der Klasse B (Regeldokumente) je Bereich als `1.9.1`
ff. eingeplant; der erste Bereich sind die Core-Module und die Laufzeitschicht. Der
Planabschnitt der Roadmap verlangte, zwei Fragen **vor** der Durchsicht zu klären: wie eine
Änderung an der Laufzeitschicht die Projekte erreicht, und wie sie die Zeichengrenze der
Regeldateien (Prüfung 4) einhält. Dazu kamen die Klärungspunkte `K-123` bis `K-129` aus der
Durchsicht von `1.9.0`.

## 2. Der Vorbedingungsdurchgang

Gemessen am 2026-09-25 am Stand `v1.9.0`, mit je einer Testinstallation je Pack.

| Messung | Ergebnis |
|---|---|
| Bereich | 11 Core-Module (104 KB), `root-instruction.md`, vier Laufzeitregeln, `fw-reviewer`, zwei Regeln der Role Packs |
| Wurzel-Anweisung installiert | `claude-code` **11.894**, `devin-desktop` **11.887** von 12.000 Zeichen (Fehlergrenze der Prüfung 4); `openai-codex` 12.516 – dort gilt die Grenze nicht, weil die Regeln über die Wurzel-Anweisung eingebunden werden; die Summe des stets Geladenen liegt bei rund 30.300 von 40.000 (Warnung) |
| Sonden der Zeichengrenze | **keine** – die Grenze war seit der Erstfassung ungeprüft durch den Sondenapparat |
| Herkunft der Grenze | Dokumentation des Vorgängerprodukts von `devin-desktop` (QD-7); seit `CR-2026-027` E3 eine **Vorgabe des Frameworks**, keine Produkteigenschaft |
| Modusnamen (`K-126`) | `Normal`/`Bypass` in `03-security.md` (drei Stellen), `05-working-model.md`, `09-risk-model.md`, im Onboarding (fünf Stellen) und in sechs weiteren Regel- und Einstiegsdokumenten |
| `.gitignore` (`K-124`) | schließt nur die Erzeugnisse von `devin-desktop` aus; die Wurzelerzeugnisse der drei Packs lassen sich aus `shared_core` und `shared_seed` der Manifeste ableiten |

## 3. Vorlage zur Entscheidung

Vorgelegt am 2026-09-25 als Fragen (a) bis (i), angenommen mit *„Bei dem Rest bin ich schon
mal einverstanden“*; zu (c) die Rückfrage nach Herkunft und Anhebung der Grenze, beantwortet
und angenommen mit *„Perfekt, so machen wir das“*.

| # | Frage | Entscheidung und Preis |
|---|---|---|
| **E1** | **Wie erreicht eine Änderung die Projekte?** (a) | Über Schritt 2 des Release-Prozesses (`install.py --target <projekt> --update`); der Änderungsverlauf nennt, dass sie erst danach wirkt (D-381 (a)) |
| **E2** | **Darf die Durchsicht Regelinhalt ändern?** (b) | Nein. Ein Widerspruch zwischen zwei Regeln wird ein Klärungspunkt; das Release bleibt PATCH (D-381 (b)) |
| **E3** | **Zeichengrenze** (c) | Keine Laufzeitdatei wird länger; Längen je Pack vorher und nachher im Protokoll; die Grenze bekommt Sonden (D-381 (c)) |
| **E4** | **Anheben der Grenze?** (Rückfrage zu (c)) | Nicht in `1.9.1`: Die Grenze ist eine Vorgabe des Frameworks (`CR-2026-027` E3), ihr Zweck ist die Summe des stets Geladenen. Als `K-130` für `1.9.2` eingeplant, mit der Empfehlung, die Summe verbindlich und die Grenze je Datei zur Warnung zu machen (D-381, D-384) |
| **E5** | **`K-126`** (e) | Sachbegriffe im Kern und im Onboarding, dazu in den übrigen Regel- und Einstiegsdokumenten; Register bleiben (D-382) |
| **E6** | **`K-124`** (f) | Einträge aller drei Packs; Prüfung 45 leitet sie aus den Manifesten ab (Gegenstand 3, keine neue Nummer) (D-383) |
| **E7** | **`K-128`** (g) | In `1.9.2` (Governance) – D-10 präzisieren (D-384) |
| **E8** | **`K-123`, `K-125`, `K-127`, `K-129`** (h) | Ein eigenes MINOR-Release nach `1.9.3` (D-384) |
| – | **Vorgehen** (d), (i) | Core-Modul maßgeblich, Laufzeitfassung auf Widerspruch geprüft (D-381 (d)); fünf parallele Durchsichten nach einem schriftlichen Auftrag, Register in einem Schritt |

> **Empfehlung der Vorbereitung:** E1 bis E8 wie vorgelegt.

---

## 4. Umsetzung

1. Durchsicht nach dem Auftrag `durchsicht-auftrag-191.md` (Ablagebereich der Sitzung) in
   fünf parallelen Durchgängen: 00/01/04/06/07, 02/03, 05/10, 08/09 und die Laufzeitschicht.
   Geschichte durch Verweis ersetzt (D-376), Hervorhebungen reduziert, einzelne Aussagen
   sachlich berichtigt (Protokoll, Abschnitt 2). `10-error-escalation.md` und acht der neun
   Laufzeitdateien blieben unverändert.
2. `K-126`: Sachbegriffe an allen Fundstellen außerhalb der Register (D-382).
3. `K-124`: `.gitignore` um `/CLAUDE.md`, `/CLAUDE.local.md.example`, `/.mcp.json.example`,
   `/.claude/`, `/.codex/` und `CLAUDE.local.md`; Kommentar und Wurzel-README zählen die
   Zeilen nicht mehr; Prüfung 45 Gegenstand 3, Sonde 45e, Gegenprobe 45c (D-383).
4. Zeichengrenze: Bündel `sonden_zeichengrenze` – Sonde 4a an einer Installation von
   `claude-code`, Gegenproben 4a bis 4c je Pack (D-381 (c)). Die Sondenmenge lautet damit
   *„4, 6, 8, 14, 18 bis 66 und 68 bis 94“* an allen drei Stellen, die Prüfung 40 vergleicht.
5. Sieben Befunde der Durchsicht als `K-131` bis `K-137`; `K-130` für das Zeichenbudget.
6. Versionen aller geänderten Dokumente mit Steckbrief um PATCH angehoben; Änderungsverlauf
   von `fw-change-small` (`0.1.5`, keine Anweisung berührt, D-303).
7. Roadmap, Decision Log, Testkatalog, Bestandsliste, Kopf des Hauptdokuments, `VERSION`,
   Changelog.
8. Beide Projekte mit `--target --update` heben.

## 5. Abnahme

Steht im Protokoll `tests/protocols/2026-09-25-klasse-b-core-laufzeit.md`.

## 6. Entscheidung

**E1 bis E8 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-25; (a) bis (i) vor
dem Bau vorgelegt und angenommen, die Rückfrage zu (c) beantwortet). Decision Records
**D-381** bis **D-384**. Alle vier zählbaren Kriterien von D-11 bleiben **0**.
