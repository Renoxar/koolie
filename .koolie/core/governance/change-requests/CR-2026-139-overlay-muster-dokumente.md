# Änderungsantrag `CR-2026-139`

| Feld | Inhalt |
|---|---|
| Titel | Best Practices im Overlay-Muster „General“ – und das Register, das auf nichts zeigen durfte |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-25 |
| Betroffene Artefakte | `framework/overlay-patterns/general.md` (`0.2.0`); `framework/overlay-patterns/general/documents/` (sechs Dokumente, neu); `install.py` (Dokumente, Manifest, Abbruchfälle); `tests/scripts/validate-framework.py` (Prüfung 8); `tests/scripts/probe-pruefungen.py` (Sonden `8a`, `8b`, `M359` bis `M359c`); `tests/TEST_CATALOG.md`; `docs/ADOPTION_GUIDE.md`, `README.md`; `docs/ROADMAP.md`; `governance/DECISION_LOG.md` (**D-359** bis **D-361**); `governance/ADOPTION_REGISTRY.md`; `build/doc/00-kopf.md`, `26-qs-test.md`; `VERSION`, `CHANGELOG.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Auslieferbestand, Installationswerkzeug, Prüfapparat |
| Art | **MINOR** nach `RELEASE_PROCESS.md` Abschnitt 1: neuer Auslieferbestand und erweiterte Prüfung; kein bestehendes Overlay-Feld geändert |
| Dringlichkeit | Auftrag des Owners vom 2026-09-25, **vor** dem Installer |
| Status | 🟢 **entschieden am 2026-09-25** (E1 bis E10), umgesetzt mit `1.6.0` |

---

## 1. Anlaß

Der `<FRAMEWORK_OWNER>` hat am 2026-09-25 beauftragt, daß das Muster `general`
**allgemeingültige Best Practices der Softwareentwicklung** für die Bereiche des Overlays
mitliefert – Coding Guidelines, Definition of Ready, Definition of Done und so weiter –,
**nur, was auf jedes Softwareprojekt paßt**. `1.5.0` hat das nicht getan: Das Muster füllt
drei sperrende Pfadplatzhalter und sonst nichts (D-355).

## 2. Die Gegenprüfung

### 2.1 Was der Kern schon regelt

Der Kern führt für KI-unterstützte Arbeit bereits eine normative Definition of Done
(`04-quality.md` Abschnitt 3), Anforderungen an Änderungen (Q1 bis Q8), Review-Prüfpunkte
(`07-review-rules.md`, RV1 bis RV12) und die Checklisten 03 (vor der Änderung), 05 (Tests),
06 (Sicherheit), 07 (neue Abhängigkeiten) und 08 (Merge Request). **Ein Musterdokument,
das davon etwas wiederholt, wäre ein zweites Register.**

🔴 **Ein Widerspruch, gefunden bevor geschrieben wurde:** Die *Pfadfinderregel* in ihrer
üblichen Form – *„Code sauberer hinterlassen, als man ihn vorfand“* – widerspricht **Q1**
(ein Ziel je Änderung) und **RV1** (Scope-Treue). Sie gehört zu den verbreitetsten Clean-
Code-Regeln und paßt trotzdem nicht in dieses Framework, jedenfalls nicht ungekürzt.

### 2.2 Was die Dokumentablage der Vorlage anbietet

`templates/project-overlay/documents/` führt dreizehn Typen; das Manifest kennt dieselben
und `other`. Sieben davon beschreiben das Projekt (`architecture`, `roadmap`, `deployment`,
`roles`, `glossary`) oder werden vom Kern getragen (`ai-governance`, `ai-process-model`).
**Sechs bleiben, die ein allgemeines Dokument tragen können.**

### 2.3 🔴 Prüfung 8 prüft nicht, ob ein registriertes Dokument existiert

`check_manifest` prüft Kopfschlüssel, Pflichtfelder und Aufzählungswerte – **nicht, ob
unter `path` etwas liegt**. Ein Manifest, dessen Einträge auf nichts zeigen, besteht.
Gezählt am 2026-09-25: Beide übernehmenden Projekte führen nur existierende Pfade (Pilot
14, Übungsrepositorium 7 Einträge). **Prüfung 8 hatte keine einzige Sonde.**

### 2.4 Der Status eines Dokuments und Kriterium 3

Ein Steckbrief mit Status `entwurf` in einem Kernträger hebt Kriterium 3 von D-11
(Prüfung 46, 47). Die Dokumente tragen deshalb **keinen** Steckbrief; der Status
`entwurf` steht im **Manifest des Projekts**, wo er den Lebenszyklus des Projektdokuments
beschreibt. Modulträger bleibt das Muster.

## 3. Vorlage zur Entscheidung

| # | Frage | Wege und ihre Preise |
|---|---|---|
| **E1** | **Ort** | **Registrierte Dokumente unter `documents/<typ>/`**, im Muster mitgeliefert, im Manifest eingetragen. **Verworfen:** Text in `OVERLAY.md` Abschnitt 9 bis 12 – bei jedem Projekt mit eigenen Dokumenten ein zweites Register |
| **E2** | **Grenze zum Kern** | **Nur ergänzen und verweisen, nichts wiederholen** (2.1); jedes Dokument sagt in einem eigenen Abschnitt, wo die Grenze liegt; bei Widerspruch gilt der Kern. Die Pfadfinderregel nur eingeschränkt |
| **E3** | **Inhaltliche Grenze** | **Nur allgemein anerkannte, werkzeug- und sprachneutrale Praktiken**; keine Schwellenwerte, keine Werkzeugnamen, keine Vorgaben, die Vorgehensmodell, Teamgröße oder Plattform voraussetzen. D-355 wird fortgeschrieben, nicht aufgehoben. ⚠️ **Preis:** Keine Maschine prüft, ob ein Satz auf jedes Projekt paßt |
| **E4** | **Status** | Kontextklasse K1, im Manifest `entwurf`, **Vorschlagsvermerk im Kopf jedes Dokuments**; kein eigener Steckbrief (2.4). Das Overlay bleibt nicht aktivierungsreif |
| **E5** | **Laden** | **`on-demand`**; die K1-Liste der Laufzeitfassung bleibt offen. ⚠️ **Preis:** Bis der Overlay Owner freigibt, wirken die Dokumente nicht auf den Client. **Verworfen:** `summary`/`rule` – sofort wirksam mit ungeprüftem Inhalt, dazu weitere Träger je Pack |
| **E6** | **Beispiele der Manifestvorlage** | **Ersetzen**, nicht ergänzen – drei Einträge mit Ausfüllschlitz neben sechs echten wären ein Register mit Einträgen, die auf nichts zeigen |
| **E7** | **Auswahl der Typen** | **Sechs:** `coding-guidelines`, `definition-of-ready`, `definition-of-done`, `quality`, `security`, `branching-strategy` (2.2) |
| **E8** | **Weitere Platzhalter, Bestandsprojekte** | **Keine weiteren Platzhalter** (`<PROJECT_RULES_PATH>`, DoR/DoD-Pfade bleiben offen). **Kein Modus für Bestandsprojekte** (D-126); der Leitfaden beschreibt die Übernahme von Hand |
| **E9** | **Release** | **MINOR `1.6.0`**, ohne Kontingent; der Installer rückt auf **`1.7.0`** – er bietet `--overlay` an und soll das vollständige Muster ausliefern. ⚠️ **Preis:** die dritte Verschiebung des Installers (D-339, D-341) |
| **E10** | **Prüfbarkeit** (im Zuge der Vorbereitung gefunden, 2.3) | **Sonden `M359` bis `M359c`** an echten Erstinstallationen, und **Prüfung 8 prüft die Existenz von `path` und – bei `load: rule` – `rule_file`**, außer der Pfad trägt einen Ausfüllschlitz. **Verworfen:** eine eigene Prüfung für die Musterablage – `install.py` hält Ablage und Beschreibung ohnehin gegeneinander und bricht ab |

> **Empfehlung der Vorbereitung:** E1 bis E10 wie vorgelegt.

---

## 4. Umsetzung

1. Sechs Dokumente unter `framework/overlay-patterns/general/documents/<typ>/muster-general.md`.
2. `general.md` auf `0.2.0`: Abschnitt *„Die Dokumente“* mit Grenze, Tabelle der Typen und
   dem, was bewußt fehlt.
3. `install.py`: `muster_dokumente()`, `muster_manifest()`, Schreiben der Dokumente bei der
   Erstinstallation, Vermerk im Änderungsverlauf, Hinweis am Ende des Laufs, Abbruch bei
   vorhandenen Dokumenten.
4. Validator: Prüfung 8 um die Existenz erweitert; Sondenmenge um Prüfung 8.
5. Sonden `8a`, `8b`, Gegenprobe `8a`; im Bündel `sonden_overlay_muster` die Sonden `M359`
   bis `M359b` und die Gegenprobe `M359c`.
6. Leitfaden (Abschnitt 2 und 3), README, Roadmap, Decision Log, Bestandsliste, Katalog,
   Kopf, Kapitel 26, `VERSION`, Changelog.
7. Beide Projekte heben; das Muster erreicht sie nicht.

## 5. Abnahme

Steht im Protokoll `tests/protocols/2026-09-25-overlay-muster-dokumente.md`.

## 6. Entscheidung

**E1 bis E10 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-25; E1 bis E9 vor dem
Bau vorgelegt und mit *„Machen wir es“* angenommen. Von E10 war die Sonde vorgelegt und der
Befund an Prüfung 8 benannt; die Erweiterung der Prüfung selbst ist im Bau entschieden worden –
der Owner hat vorab erklärt, den Empfehlungen der Vorbereitung zu folgen).
Decision Records **D-359** bis **D-361**. Alle vier zählbaren Kriterien von D-11 bleiben
**0**.
