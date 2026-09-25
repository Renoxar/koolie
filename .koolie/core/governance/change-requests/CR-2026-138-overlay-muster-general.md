# Änderungsantrag `CR-2026-138`

| Feld | Inhalt |
|---|---|
| Titel | Das Overlay-Muster „General Development“ – und die Prüfung, die von fünf Pfadwerten einen sah |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-25 |
| Betroffene Artefakte | `framework/overlay-patterns/general.md` (neu); `install.py` (`--overlay`, Füllschritt); `framework/runtime/permissions.json` (Schlitz `<READ_ONLY_PATHS>`); `tests/scripts/validate-framework.py` (**Prüfung 89**, Prüfung 59 formatgebunden); `tests/scripts/probe-pruefungen.py` (zwei Bündel); `clients/openai-codex/CLIENT_PACK.md` Abschnitt 5; `templates/project-overlay/OVERLAY.md` Abschnitt 4; `docs/ADOPTION_GUIDE.md`, `README.md`; `docs/ROADMAP.md`; `governance/DECISION_LOG.md` (**D-355** bis **D-358**, `K-69`); `governance/ADOPTION_REGISTRY.md`; `tests/TEST_CATALOG.md`; `build/doc/00-kopf.md`, `26-qs-test.md`; `VERSION`, `CHANGELOG.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Auslieferbestand, Installationswerkzeug, Prüfapparat |
| Art | **MINOR** nach `RELEASE_PROCESS.md` Abschnitt 1: neue Funktion (`--overlay`), neue Prüfung, neuer Schlitz der Kernquelle; kein bestehendes Overlay-Feld geändert |
| Dringlichkeit | Posten `1.5.0` des Releaseplans (D-126, D-341, D-353) |
| Status | 🟢 **entschieden am 2026-09-25** (E1 bis E9), umgesetzt mit `1.5.0` |

---

## 1. Anlaß

Der Posten `1.5.0`: das optionale Projekt-Overlay *General Development*, gewählt über
`--overlay general` (D-126), mit dem Umfang aus D-353 – Füllschritt bei der
Erstinstallation, Wertabgleich aus `K-69`, die Frage nach `<READ_ONLY_PATHS>` in der
Kernquelle. **Offen waren seit D-126** vier Voraussetzungen: welche Felder das Muster
füllen darf, wer Owner ist, die Bauform und die Grenze zur Aktivierungsreife (D-57).

## 2. Die Gegenprüfung

### 2.1 Welche Werte ein Muster ohne Kenntnis des Projekts sicher angeben kann

Die Kernquelle der Berechtigungen trägt drei Pfadschlitze, alle im `deny`-Korb:
`<EXCLUDED_PATHS>` (Lesen und Schreiben), `<CI_CONFIG_PATHS>` und
`<QUALITY_GATE_CONFIG_PATHS>` (Schreiben). **Jeder Wert dort verschärft.** Ein Wert, der
auf ein Projekt nicht paßt, sperrt eine Datei, die es dort nicht gibt. Die übrigen
Pfadplatzhalter – `<ALLOWED_PATHS>`, `<TEST_PATHS>`, `<DOC_PATHS>` – **geben frei**, und
die Befehlsschlitze stehen im `ask`-Korb; ein Fehlgriff dort wäre eine Lockerung.
➡️ *Die Grenze ist keine Auswahl nach Geschmack, sondern eine Richtung.*

### 2.2 🔴 Prüfung 59 übersprang ihren dritten Gegenstand bei `openai-codex` still

Gemessen am 2026-09-25 an einer Wegwerf-Installation von `openai-codex`:
`<EXCLUDED_PATHS>` in `OVERLAY.md` und Laufzeitfassung auf `deploy/**` gesetzt, die
Berechtigungsdatei unverändert. `--strict-overlay` meldete **nichts** zu diesem Wert.

| Befund | Beleg |
|---|---|
| `.codex/config.toml` führt keinen Eintrag für `<EXCLUDED_PATHS>` und keinen für `deploy/**` | `grep` auf die Datei |
| Gegenstand (c) von Prüfung 59 ruft `json.loads` auf und kehrt bei `JSONDecodeError` zurück – *„check_config hat das bereits gemeldet“*, was für TOML nicht stimmt | Quelltext |
| Prüfung 59 steht **nicht** in `FORMATGEBUNDENE_PRUEFUNGEN`, und Prüfung 87 hält diese Liste gegen das Pack, **nicht gegen den Code** | Quelltext |

➡️ **Die Bauform *„zwei Stellen, die einander decken“* (0.57.0):** Die Liste war
vollständig in Bezug auf die Prüfungen, die sich auf sie berufen – und genau diese hier
tat es nicht.

### 2.3 Die vier übrigen Pfadplatzhalter in beiden Projekten

| | Pilot (`claude-code`) | Übungsrepositorium (`devin-desktop`) |
|---|---|---|
| Quelle: alle vier in der dreispaltigen Zeile von Abschnitt 4 | ja | ja |
| Laufzeitfassung **nennt** die Platzhalter | **ja, alle vier** | 🔴 **keinen der vier** – nur die Werte (*„Erlaubte Pfade: `backend/src/**`, …“*) |
| Schreibweise für „kein Wert“ | `nicht vorhanden` (Quelle), `keine` (Laufzeitfassung) für `<DOC_PATHS>` | – |
| Schreibsperre der Nur-Lese-Pfade im `deny`-Korb | von Hand, 2 Einträge | von Hand, 2 Einträge |

➡️ **Die Ersetzung statt der Bindung (D-160) stand im Übungsrepositorium an vier Stellen**,
seit dessen Laufzeitfassung besteht. Keine Prüfung konnte sie sehen, weil keine die vier
Platzhalter las.

### 2.4 Der Füllschritt an Wegwerf-Installationen aller drei Packs

| Pack | Berechtigungsdatei | Laufzeitfassung | `OVERLAY.md` |
|---|---|---|---|
| `claude-code` | alle Werte als `Read(…)`/`Edit(…)`; kein Schlitz der drei mehr wörtlich | Wert hinter `(<EXCLUDED_PATHS>)` | drei Wertzeilen, Vermerk im Änderungsverlauf |
| `devin-desktop` | dito mit `Read`/`Write` | dito | dito |
| `openai-codex` | 🔴 **nur ein Teil kommt an:** Teilbäume (`.github/workflows/**` → `":workspace/.github/workflows" = "read"`) und einzelne Dateinamen; Namensmuster mit `*` nicht | dito | dito |

⚠️ **Die erste Fassung der Musterdatei behauptete für `openai-codex`, die Globwerte
erreichten die Datei gar nicht.** Die Messung hat sie berichtigt, bevor sie ausgeliefert
wurde.

## 3. Vorlage zur Entscheidung

| # | Frage | Wege und ihre Preise |
|---|---|---|
| **E1** | **Welche Felder darf das Muster füllen?** | **Nur die drei Pfadplatzhalter im `deny`-Korb** (2.1). Die Grenze steht **im Werkzeug**: `install.py` nimmt keinen anderen Platzhalter an und bricht vor dem ersten Schreibvorgang ab. **Verworfen:** freigebende Pfade, Befehle, Rollen, Status. ⚠️ **Preis:** Das Muster füllt wenig – drei von rund vierzig Platzhaltern |
| **E2** | **Bauform: Varianten oder Kopien?** | **Eine Wertedatei, die nur die Abweichung trägt.** `install.py` schreibt die eine Vorlage und füllt aus derselben Tabelle alle drei Träger. **Verworfen:** *n* vollständige Kopien – ein zweites Register. ⚠️ **Preis:** Der Füllschritt hängt an der Form der Wertzeilen und bricht ab, wenn ein Anker fehlt |
| **E3** | **Wer ist Owner?** | **`<FRAMEWORK_OWNER>`**; das Muster ist ein Modulträger mit Steckbrief, Status `pilot` – `entwurf` höbe Kriterium 3 von D-11 auf 1. Es liegt unter `framework/overlay-patterns/`, **nicht** unter `templates/`, weil Prüfung 47 dort einen Ausfüllschlitz im Status verlangt |
| **E4** | **Grenze zur Aktivierungsreife (D-57)?** | Ein Overlay aus dem Muster **besteht** `--check-overlay-ready` **nicht** – die organisatorischen Pflichtwerte bleiben offen. Eine Sonde hält es fest |
| **E5** | **`<READ_ONLY_PATHS>` in der Kernquelle?** | **Ja, als Schlitz ohne Kernzusage.** Wirkt nur bei neuen Installationen; beide Projekte führen die Sperre schon von Hand (2.3). **Verworfen:** `core: true` – verlangte die Freigabe durch `<SECURITY_CONTACT>` für jedes Pack, das es nicht abbildet |
| **E6** | **Wie wird `K-69` geprüft?** | **Prüfung 89**, dieselben drei Gegenstände wie 59, gleicher Schweregrad; ein Overlay, das anders bindet, bekommt eine eigene Meldung; „kein Wert“ in beiden gemessenen Schreibweisen ist die leere Menge. ⚠️ **Preis:** Das Übungsrepositorium muß beim Heben seine Laufzeitfassung umschreiben (2.3) |
| **E7** | **Füllschritt je Client Pack?** | Laufzeitfassung und `OVERLAY.md` bei allen drei; die Berechtigungsdatei, soweit das Pack den Wert abbildet – bei `openai-codex` mit der benannten Lücke (2.4) |
| **E8** | **Einstufung?** | **MINOR, ohne Kontingent** – gemessen an Wegwerf-Installationen, nicht mit Sitzungsläufen |
| **E9** | **Prüfung 59 (c) formatgebunden** (2.2, im Bau gefunden) | **In `FORMATGEBUNDENE_PRUEFUNGEN` aufnehmen**, wie (c) von Prüfung 89, und in Abschnitt 5 des Packs nennen. **Verworfen:** (c) für TOML nachbauen – die Pfadrechteschicht kennt keine Musterform (D-346). ⚠️ **Preis:** Die Lücke bleibt, sie ist nur erklärt |

> **Empfehlung der Vorbereitung:** E1 bis E9 wie vorgelegt.

---

## 4. Umsetzung

1. `framework/overlay-patterns/general.md` neu; `install.py` mit `--overlay`, Füllschritt,
   Vorlauf und vier Abbruchfällen.
2. `permissions.json`: Schlitz `write <READ_ONLY_PATHS>`.
3. Validator: Prüfung 89, `FORMATGEBUNDENE_PRUEFUNGEN` um 59 und 89; Register im
   Kopfkommentar.
4. Sondenbündel `sonden_overlay_pfadabgleich` und `sonden_overlay_muster`.
5. Overlay-Vorlage Abschnitt 4, Leitfaden, README, Codex-Pack Abschnitt 5, Roadmap (mit
   eigenem Planabschnitt für `1.6.0`), Decision Log, Bestandsliste, Katalog, Kopf,
   Kapitel 26, `VERSION`, Changelog.
6. Beide Projekte heben; im Übungsrepositorium die vier Zeilen der Laufzeitfassung auf
   die Bindung umstellen.

## 5. Abnahme

Steht im Protokoll `tests/protocols/2026-09-25-overlay-muster-general.md`.

## 6. Entscheidung

**E1 bis E9 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-25; E1 bis E8 vor dem
Bau vorgelegt und mit *„wie empfohlen“* beantwortet, E9 im Bau gefunden – der Owner hat
vorab erklärt, den Empfehlungen der Vorbereitung zu folgen). Decision Records **D-355**
bis **D-358**; `K-69` beantwortet. Alle vier zählbaren Kriterien von D-11 bleiben **0**.
