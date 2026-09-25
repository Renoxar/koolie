# Änderungsantrag `CR-2026-145`

| Feld | Inhalt |
|---|---|
| Titel | Die Durchsicht der Klasse B, dritter Bereich – und die Anweisung, die stehen bleibt |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-25 |
| Betroffene Artefakte | Durchsicht: die 13 `SKILL.md` (zwei geändert: `fw-docs-update`, `fw-tests`), `templates/` (`SKILL_TEMPLATE.md`, `project-overlay/OVERLAY.md`, `overlay-manifest.yaml`, die 13 `documents/*/.gitkeep.md`), `clients/_template/CLIENT_PACK.md`; Änderungsverlauf der beiden Skills; Register: Decision Log, Roadmap, Bestandsliste, Kopf des Hauptdokuments, `VERSION`, Changelog |
| Ebene laut Entscheidungsbaum 6 | **Core** – Regeldokumente und Vorlagen |
| Art | **PATCH** nach `RELEASE_PROCESS.md` Abschnitt 1: Formulierungen, Erläuterungen und Berichtigungen gegen das maßgebliche Core-Modul, keine Anweisung eines Skills geändert, keine neue Prüfungsnummer, kein Overlay muss sich anpassen |
| Dringlichkeit | Posten `1.9.3` nach D-380 |
| Status | 🟢 **entschieden am 2026-09-25** (E1 bis E10), umgesetzt mit `1.9.3` |

---

## 1. Anlass

D-380 plant die inhaltliche Durchsicht der Klasse B in drei Bereichen; der dritte sind
`framework/skills/`, die Skills der Role Packs, `templates/` und `clients/_template/`. Die
Roadmap verlangte vorher zu klären, wie eine Änderung an einer `SKILL.md` mit Version,
Änderungsverlauf des Skills und dem erneuten Auslösen der Testfälle umgeht (D-303).

## 2. Der Vorbedingungsdurchgang

Gemessen am 2026-09-25 am Stand `v1.9.2`.

| Messung | Ergebnis |
|---|---|
| Bereich | 13 `SKILL.md` (rund 215 KB), die Vorlagen unter `templates/` (rund 47 KB), `clients/_template/CLIENT_PACK.md` (12,6 KB) |
| Klasse der Skill-Register | `TESTS.md`, `EXAMPLES.md` und `CHANGELOG.md` der Skills sind **Klasse C** (`docs/DOCUMENTATION_STANDARD.md`, `dokumentklasse()` des Validators) – nicht Gegenstand der Durchsicht |
| Ergebniszellen | **87, alle abgenommen** (72 in den zwölf `fw-`-Skills, 15 in `role-re-ticket`); Kriterium 2 von D-11 zählt jede `TESTS.md` des Kerns |
| Herleitung in den Skills | null bis ein D-Verweis je Skill; `(Erläuterung)` in fünf Skills je einmal – der Rest ist Anweisung. `CLIENT_PACK.md`: 13 D- und 4 CR-Verweise |
| Sondenanker im Bereich | `fw-plan/SKILL.md`, `fw-code-explain/SKILL.md`, `OVERLAY.md`, `overlay-manifest.yaml`, `documents/README.md`, `SKILL_TEMPLATE.md`, `PLAN_TEMPLATE.md`, `CLIENT_PACK.md` |

## 3. Vorlage zur Entscheidung

Vorgelegt am 2026-09-25 als Fragen (a) bis (j), angenommen mit *„Ja, das passt. Du kannst
loslegen“*. Während des Baus fragte der Owner, ob sich das Framework mit Kiro einsetzen lässt,
und beauftragte die Aufnahme als Client Pack (*„Ja, bitte nimm Kiro mit in die Roadmap als
neues Client-Pack. Ich weiß allerdings noch nicht, für welches Release“*).

| # | Frage | Entscheidung und Preis |
|---|---|---|
| **E1** | **Umfang** (a) | Klasse B nach dem Validator: die `SKILL.md`, alles unter `templates/`, `CLIENT_PACK.md`; die Register der Skills werden nur gegen ihren Skill gelesen (D-393) |
| **E2** | **Grenze in einer `SKILL.md`** (b) | Nur Schreibung, Namen und Verweise auf dieselbe Sache, Erläuterung, Form; was eine Anweisung ändern würde, wird ein Klärungspunkt – keine Zelle öffnet sich, Kriterium 2 bleibt 0 (D-393 (a)) |
| **E3** | **Verweis innerhalb einer Anweisung** (c) | Gilt als Namensanpassung, wenn das Ziel dieselbe Sache ist; jeder Fall einzeln im Protokoll (D-393 (a)). Es gab keinen |
| **E4** | **Version und Änderungsverlauf** (d) | PATCH je geändertem Skill, der Verlauf nennt die Art der Änderung und *„Keine Anweisung berührt“* (D-393 (c)) |
| **E5** | **Länge** (e) | Keine `SKILL.md` wird länger, das Frontmatter und `description` bleiben unverändert (D-393 (b)) |
| **E6** | **Erläuterungen** (f) | Werden nicht nach `EXAMPLES.md` verschoben (D-393 (b)) |
| **E7** | **`SKILL_TEMPLATE.md` und `CLIENT_PACK.md`** (g), (h) | Vorlage an `08-skill-conventions.md` angeglichen; Herleitung in der Pack-Vorlage auf die Regel mit Verweis gekürzt, jede entfallene Kennung steht in einem anderen Träger (D-393 (d)) |
| **E8** | **Versionsart** (i) | PATCH `1.9.3` (D-393 (e)) |
| **E9** | **D-303 maschinell stützen** (j) | Nicht in `1.9.3`; als `K-146` für `1.11.0` (D-394) |
| **E10** | **Kiro** (Zwischenfrage) | Als `K-147` angelegt, ohne Ziel-Release; die Befunde als `K-148` bis `K-151` eingeplant (D-394) |

> **Empfehlung der Vorbereitung:** E1 bis E9 wie vorgelegt.

---

## 4. Umsetzung

1. Durchsicht nach dem Auftrag `durchsicht-auftrag-193.md` (Ablagebereich der Sitzung) in fünf
   parallelen Durchgängen: drei Gruppen zu je drei Skills, eine zu vier Skills (mit
   `role-re-ticket`), eine über die Vorlagen und die Pack-Vorlage. Änderungen nur mit dem
   Edit-Werkzeug; die Diffs vom Koordinator gelesen.
2. `fw-docs-update` `0.1.5` und `fw-tests` `0.1.4` – je eine Erläuterung in Abschnitt 4.
3. `SKILL_TEMPLATE.md` `0.1.4`, `CLIENT_PACK.md` (Vorlage) `0.3.1`; `OVERLAY.md`,
   `overlay-manifest.yaml` und die `.gitkeep.md` der Dokumentablage ohne Steckbrief.
4. Die Befunde als `K-148` bis `K-151`, die Frage (j) als `K-146`, Kiro als `K-147` (D-394).
5. Roadmap `0.3.3` (Planabschnitt `1.10.0`, Kiro vorgemerkt), Decision Log, Bestandsliste,
   Kopf des Hauptdokuments, `VERSION`, Changelog.
6. Beide Projekte mit `--target --update` heben.

## 5. Abnahme

Steht im Protokoll `tests/protocols/2026-09-25-klasse-b-skills.md`.

## 6. Entscheidung

**E1 bis E10 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-25; (a) bis (j) vor dem
Bau vorgelegt und angenommen). Decision Records **D-393** und **D-394**. Alle vier zählbaren
Kriterien von D-11 bleiben **0**.
