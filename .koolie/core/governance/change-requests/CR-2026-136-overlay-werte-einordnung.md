# Änderungsantrag `CR-2026-136`

| Feld | Inhalt |
|---|---|
| Titel | Die Frage nach dem einen Ort der Overlay-Werte – und der Träger, den sie dafür vorschlug, trägt sie nicht |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-24 |
| Betroffene Artefakte | `governance/DECISION_LOG.md` (**D-353**; `K-120` beantwortet; Vermerke an `K-67`, `K-69`, `K-121`); `docs/ROADMAP.md` (Posten `1.5.0`: Füllschritt bei der Erstinstallation, `K-69` und die Abbildung von `<READ_ONLY_PATHS>` in den Umfang genommen); `governance/ADOPTION_REGISTRY.md`; `build/doc/00-kopf.md`, `26-qs-test.md`; `VERSION`, `CHANGELOG.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Eigentumsgrenze zwischen Kern und Projekt, Releaseplan |
| Art | **Einordnung.** Patch-Release nach `RELEASE_PROCESS.md` Abschnitt 1: kein Overlay-Feld berührt, keine Regel, **keine Prüfung, kein Werkzeug geändert** – entschieden wird, **was `1.5.0` baut und was nicht** |
| Dringlichkeit | Vor `1.5.0` (Frage (2) von `K-120`) |
| Status | 🟢 **entschieden am 2026-09-24** (E1 bis E4), umgesetzt mit `1.4.3` |

---

## 1. Anlaß

`K-120` fragt, ob die Projektwerte eines Overlays an **einem** Ort stehen sollen und
`install.py --update` Laufzeitfassung und Berechtigungsdatei daraus **erzeugt**. Der Punkt
ist *vor `1.5.0` einzuordnen*, weil das Overlay *General Development* (D-126) weitere Werte
mitbringt. `K-121` hängt mit seiner Frage (3) daran.

## 2. Die Gegenprüfung

### 2.1 🔴 Der vorgeschlagene Träger trägt die Werte nicht

`K-120` Frage (1) schlägt `overlay-manifest.yaml` als einzige Quelle vor. **Gelesen in der
Vorlage und in beiden übernehmenden Projekten:** Die Datei ist das **Register der
Projektdokumente** (Ebene 4, `OVERLAY.md` Abschnitt 19). Von den Projektwerten führt sie
genau einen, die Overlay-Version (`overlay_version`), dazu `project_code`. **Die Pfad- und
Befehlswerte stehen in keinem der drei Bestände darin.** Ihre Quelle ist die
**Bindungstabelle in `OVERLAY.md`** (Abschnitte 4 bis 6), und das sagt die Vorlage selbst:
*„Diese Werte MÜSSEN in `<PERMISSIONS_FILE>` und in `<RULES_DIR>/20-project-overlay.md`
übernommen werden.“*

🔴 **Und die „bis zu vier Träger“ sind zwei verschiedene Dreiergruppen.** Die Zahl stammt
aus der Auflage von `CR-2026-090` (*„Quelle, Manifest, Laufzeitfassung,
Berechtigungsdatei“*) und vereinigt zwei Gegenstände:

| Wert | Träger | Zahl |
|---|---|---|
| Overlay-Version | `OVERLAY.md`, `overlay-manifest.yaml`, Laufzeitfassung | 3 |
| ein Pfad- oder Befehlswert | `OVERLAY.md`, Laufzeitfassung, Berechtigungsdatei | 3 |

➡️ **Kein Wert steht in vier Trägern.** Der Befund von `K-120` trägt trotzdem – drei Stellen
Handpflege sind zwei zu viel –, aber **die Abhilfe, die er vorschlug, hätte am falschen Ort
angesetzt:** Wer das Dokumentenregister zur Wertquelle macht, verschiebt jeden Pfadwert in
eine **vierte** Datei.

### 2.2 Was ein Erzeugen aus der Quelle überschreiben würde – gemessen an beiden Projekten

Die Kernquelle `framework/runtime/permissions.json` mit `install.py` für das jeweilige Pack
gerendert und gegen die Berechtigungsdatei des Projekts gehalten (Stand `1.4.2`):

| | Pilot (`claude-code`) | Übungsrepositorium (`devin-desktop`) |
|---|---|---|
| Einträge nur im Projekt | **12** (2 `ask`, 10 `deny`) | **25** (3 `ask`, 22 `deny`) |
| davon aus einem Platzhalter der Kernquelle ableitbar | 10 | 20 |
| davon Umsetzung von `<READ_ONLY_PATHS>` – **ein Platzhalter, den die Kernquelle nicht abbildet** | 2 (`pom.xml`, `start.ps1`) | 2 (`api-contracts/**`, Migrationen) |
| davon **echte Projektzusätze ohne jeden Platzhalter** | **0** | **3** (`Exec(mvn deploy)`, `Exec(npm install)`, `Exec(npm uninstall)`) |
| Einträge der Kernquelle, die das Projekt **entfernt** hat, weil sein Wert „nicht vorhanden“ ist | 2 (`<QUALITY_GATE_CONFIG_PATHS>`, `<LINT_COMMAND>`) | 0 |

Alle Zusätze sind **Verschärfungen** (`deny`) oder gefüllte Befehlsschlitze – D-76 verbietet
dem Overlay **Freigaben** über die drei Schlitze hinaus, keine Sperren.

**Die Laufzeitfassung ist überwiegend Projektprosa.** Ohne den Inhalt der Codespannen
gezählt, weichen im Pilot **59 von 91** Zeilen von der Vorlage ab, im Übungsrepositorium
**48 von 78**; einen gebundenen Platzhalter tragen 8 beziehungsweise 5 Zeilen.

➡️ **Ein Erzeugen bei `--update` bräuchte also drei Dinge, die es heute nicht gibt:** eine
zweite Quelle für die Projektzusätze – **ein zweites Register**, genau der Befundtyp, den
die Roadmap für `1.5.0` ausdrücklich vermeiden will –, ein Vokabular für *„nicht
vorhanden“*, und eine Abgrenzung der Laufzeitfassung zwischen erzeugtem und geschriebenem
Text.

### 2.3 🔴 Was ein vorbefülltes Overlay heute nach der Erstinstallation hinterläßt – gemessen

Wegwerf-Installation aus dem Arbeitsbaum (`claude-code`), danach `<EXCLUDED_PATHS>` in
`OVERLAY.md` und Laufzeitfassung auf `deploy/**` gesetzt – so, wie ein Muster mit
vorgeschlagenen Werten es ausliefern würde:

| Zustand | `--strict-overlay` |
|---|---|
| Berechtigungsdatei wie installiert | `.claude/settings.json: enthält noch Platzhalter` – `Read(<EXCLUDED_PATHS>)` steht **wörtlich** im `deny`-Korb. **Prüfung 59 enthält sich** (Code: *„Schlitz noch ungefüllt“*) |
| Gegenprobe: `deny` auf `deploy/**` gefüllt | Meldung zu `EXCLUDED_PATHS` fällt weg; übrig bleiben die übrigen Schlitze |

➡️ **Ein Muster, das Werte vorschlägt, erreicht die Schicht nicht, die sie durchsetzt.**
Die Berechtigungsdatei entsteht aus der Kernquelle, nicht aus dem Overlay – und bis ein
Mensch sie füllt, **sperrt der vorgeschlagene Wert nichts**, während `OVERLAY.md` ihn schon
nennt. Das ist die Lage, die der Sitzungsaufbau des Übungsrepositoriums seit `0.65.0` mit
einem eigenen Füllskript überbrückt (*„der Füllschritt gehört zum Aufbau“*).

### 2.4 Die Grenze zu D-76

D-76 hat 2026-09-13 eine Erweiterungsschicht verworfen, weil *„eine nur beim Installieren
gelesene Quelle eine Zusage wäre, die beim ersten Releasewechsel bricht“*. **Ein
Füllschritt bei der Erstinstallation ist dieselbe Lesestelle** – der Unterschied muß
deshalb in der Zusage und in der Quelle liegen, nicht im Mechanismus: D-76 verwarf einen
**fortlaufenden** Kanal für zusätzliche Freigaben aus dem **Projekt**; ein Füllschritt
verspricht nur den **Anfangszustand**, füllt ausschließlich die Schlitze, die die
Kernquelle ohnehin hat, und liest dafür **das mitgelieferte Muster – einen Träger des
Kerns, nicht des Projekts.** Der Befund von D-76, *„`render_permissions` liest keine Quelle
des Projekts“*, bleibt damit wahr. Danach gehört die Datei dem Projekt wie heute.

### 2.5 🔴 Was eine verbindliche Bindungsform kosten würde

`K-67` fragt, ob die Overlay-Vorlage **eine** Form verlangen soll, einen Platzhalter zu
binden. Sein eigener Statusvermerk nennt den Preis: *„verlangte einen Umbau **jeder**
bestehenden Overlay-Datei“*. **Nach `RELEASE_PROCESS.md` Abschnitt 1 ist das MAJOR** –
eine Änderung, die Overlays anpassen müssen. ➡️ **Eine Voraussetzung, die ein
MAJOR-Release verlangt, kann nicht Voraussetzung eines MINOR-Postens sein.** Sie ist es
auch nicht: Der Füllschritt liest das Muster, dessen Form das Framework selbst festlegt
(2.4), und Prüfung 59 liest `<EXCLUDED_PATHS>` schon heute aus der dreispaltigen Zeile von
Abschnitt 4 – in **beiden** Projekten stehen alle fünf Pfadplatzhalter in genau dieser Form.

---

## 3. Vorlage zur Entscheidung

| # | Frage | Wege und ihre Preise |
|---|---|---|
| **E1** | **Wird `overlay-manifest.yaml` die Quelle der Projektwerte?** (`K-120` (1)) | **Nein.** Quelle ist und bleibt die Bindungstabelle in `OVERLAY.md` (2.1). `K-120` wird in diesem Punkt **berichtigt**, nicht beantwortet: Das Register trägt einen einzigen Wert, und die „vier Träger“ sind zwei Dreiergruppen. **Verworfen:** das Register zur Wertquelle ausbauen – jeder Pfadwert bekäme eine vierte Ablage. ⚠️ **Preis:** keiner; die Auflage aus `CR-2026-090` bleibt richtig, sie zählt nur zusammen, was zwei Gegenstände sind |
| **E2** | **Erzeugt `--update` Laufzeitfassung und Berechtigungsdatei aus der Quelle?** (`K-120` (1) und (3)) | **Nein, nicht in `1.x`.** Beide Dateien bleiben Saat (D-76). Gemessen (2.2): **3 von 37** Projekteinträgen sind aus keinem Platzhalter ableitbar, **4** setzen einen Platzhalter um, den die Kernquelle gar nicht abbildet, **2** Kerneinträge hat ein Projekt bewußt entfernt, und die Laufzeitfassung ist zu gut der Hälfte Projektprosa. Ein Erzeugen verschöbe die Eigentumsgrenze und zwänge jedes Overlay zur Anpassung – nach `RELEASE_PROCESS.md` Abschnitt 1 **MAJOR**. **Antwort auf Frage (3):** Die Projektzusätze bleiben, wo sie sind, weil nichts sie überschreibt. **Verworfen:** Erzeugen mit einer zweiten Quelle für Zusätze (ein zweites Register); Erzeugen mit Markerblöcken (JSON trägt keine Kommentare, zwei der drei Berechtigungsdateien sind JSON). ⚠️ **Preis, benannt: Die Handpflege an drei Stellen bleibt.** Gemildert wird sie durch E4 – geprüft statt erzeugt. **Ein Erzeugen bleibt ein möglicher MAJOR-Posten**, wenn die erweiterte Prüfung (E4) im Betrieb Abweichungen findet, die sie nur melden und nicht verhindern kann |
| **E3** | **Was braucht `1.5.0` dann?** (`K-120` (2)) | **Einen Füllschritt bei der Erstinstallation:** Wer `--overlay general` wählt, bekommt Laufzeitfassung und Berechtigungsdatei **einmal** aus der Bindungstabelle des gewählten Musters gefüllt – dieselben Schlitze, die die Kernquelle hat, keiner mehr. Saat bleibt Saat, das Eigentum ändert sich nicht, **MINOR** wie geplant. Ohne ihn liefert das Muster einen Wert, der nichts sperrt (2.3). **Abgrenzung zu D-76 (2.4):** Die Zusage ist der Anfangszustand, kein Kanal, und die Quelle ist das Muster im Kern, nicht das Projekt. **Ohne `--overlay` bleibt alles wie heute** – das leere Overlay hat keine Werte, die zu füllen wären. **Verworfen:** den Füllschritt auch aus einem **projekteigenen** `OVERLAY.md` speisen – das wäre der Kanal, den D-76 verworfen hat, und bräuchte `K-67`. ⚠️ **Preis:** Ein Projekt, das nach der Installation einen vorgeschlagenen Wert ändert, zieht ihn wie heute von Hand nach – der Füllschritt wirkt genau einmal |
| **E4** | **Wie werden `K-67` und `K-69` eingeordnet?** | **`K-69` wird Voraussetzung von `1.5.0`, `K-67` nicht.** `K-69` (der Wertabgleich für `<ALLOWED_PATHS>`, `<TEST_PATHS>`, `<DOC_PATHS>`, `<READ_ONLY_PATHS>`), weil E2 die Handpflege bestehen läßt und nur eine Prüfung sie auffängt – gelesen wird wie bei Prüfung 59 die dreispaltige Zeile von Abschnitt 4. **Dazu in den Umfang:** die Frage, ob die Kernquelle `<READ_ONLY_PATHS>` als Schreibsperre abbildet – **beide Projekte tun es von Hand, auf dieselbe Weise** (2.2). **`K-67` bleibt offen und bekommt seinen Preis dazugeschrieben:** Eine verbindliche Bindungsform ist MAJOR (2.5). **Verworfen:** `K-69` als eigenes Release vor `1.5.0` – der Releaseplan rückte zum **dritten** Mal um eins (nach D-339 und D-341), für eine Prüfung, deren erster neuer Gegenstand erst mit dem Muster entsteht. **Verworfen:** `K-67` in `1.5.0` – ein MAJOR-Eingriff als Voraussetzung eines MINOR-Postens. ⚠️ **Preis:** `1.5.0` wird größer; und die erweiterte Prüfung sieht wie Prüfung 59 nur die tabellarische Bindung – ein Overlay, das anders bindet, **entgeht ihr, und das muß die Prüfung dann melden, nicht verschweigen** |

**Zu `K-121` Frage (3)** – *hängt die Schreibrückfrage an `K-120`?* – **ja, und E2 sagt
wie:** Ein Overlay-Wert, der die Schreibrückfrage steuert, stünde als Hand-Eintrag in der
Berechtigungsdatei, an einer der drei Stellen ohne Erzeugung. **Er ist erst dann ein
tragbarer Ort für eine Sicherheitseinstellung, wenn eine Prüfung ihn gegen die Quelle hält**
– also frühestens mit E4. `K-121` bleibt in (1) und (2) offen.

> **Empfehlung der Vorbereitung:** E1 bis E4 wie vorgelegt. Keine neue Prüfung, kein
> Werkzeug geändert – dieses Release ordnet ein, `1.5.0` baut.

---

## 4. Umsetzung

1. `DECISION_LOG.md`: **D-353**; `K-120` auf *beantwortet*; Vermerke an `K-69`
   (Voraussetzung von `1.5.0`), an `K-67` (keine Voraussetzung, Preis MAJOR) und an
   `K-121` (Frage (3) beantwortet).
2. `docs/ROADMAP.md`: im Abschnitt zum Posten `1.5.0` die entschiedenen Voraussetzungen
   und der erweiterte Umfang; Zeile `1.5.0` der Releasetabelle; Zeile `1.4.3`.
3. `VERSION` `1.4.3`, Changelog, Dokumentkopf, Bestandsliste; beide übernehmenden Projekte
   auf `1.4.3` gehoben und dort committet; Hauptdokument und Word-Fassung je Pack.

## 5. Abnahme

Steht im Protokoll `tests/protocols/2026-09-24-overlay-werte-einordnung.md`.

## 6. Entscheidung

**E1 bis E4 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-24; der Owner hat
vorab erklärt, den Empfehlungen der Vorbereitung zu folgen). Decision Record **D-353**.
Alle vier zählbaren Kriterien von D-11 bleiben **0**; kein Overlay-Feld berührt.
