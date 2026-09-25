# Protokoll: Best Practices im Overlay-Muster „General“ – und das Register, das auf nichts zeigen durfte

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-25 |
| Release | `1.6.0` |
| Änderungsantrag | `CR-2026-139` |
| Art | Neuer Auslieferbestand im Overlay-Muster, erweiterte Prüfung – **keine Sitzung, kein Kontingent, kein Modelllauf** |
| Gegenstand | Die sechs Musterdokumente und ihre Registrierung an Erstinstallationen aller drei Packs; Prüfung 8 an beiden übernehmenden Projekten |
| Ergebnis | 🟢 **Entschieden, `D-359` bis `D-361`.** Sechs Dokumente, sechs Manifesteinträge als `entwurf`, keine Freigabe, keine zusätzliche Validatormeldung in keinem Pack. 🔴 **Prüfung 8 prüfte nicht, ob ein registriertes Dokument existiert** – jetzt schon, beide Projekte still |

---

## 1. Was gefragt war

Wiederaufnahmepunkt von `1.5.0`, Punkt 2: Das Muster `general` soll allgemeingültige Best
Practices der Softwareentwicklung für die Bereiche des Overlays mitliefern, **nur was auf
jedes Projekt paßt**. Vor dem Bau vorgelegt und mit *„Machen wir es“* entschieden:
`CR-2026-139` E1 bis E9; E10 aus der Vorbereitung.

## 2. Messungen

Alle Messungen an Wegwerf-Verzeichnissen außerhalb des Repositoriums; der Kern kommt über
`git ls-files -z .koolie/core | tar` aus dem Arbeitsbaum.

### 2.1 Vor dem Bau: was der Kern schon regelt

Gelesen: `04-quality.md` (Q1 bis Q8, Abschnitt 3), `07-review-rules.md` (RV1 bis RV12),
`03-security.md` Abschnitt 6, die Checklisten 03, 05, 06 und 08, `OVERLAY.md` Abschnitt 7
und 9 bis 12, die Manifestvorlage und die Dokumentablage der Vorlage (13 Typen).

| Befund | Folge |
|---|---|
| Die Pfadfinderregel (*„sauberer hinterlassen, als vorgefunden“*) widerspricht Q1 und RV1 | nur eingeschränkt: benennen statt nebenbei beheben |
| Checkliste 06 führt Eingabevalidierung, Autorisierung, Injection, Geheimnisse, Logging, Kryptografie als Prüfpunkte je Änderung | das Sicherheitsdokument führt die **Grundsätze** dahinter und verweist |
| Checkliste 05 führt Aussagekraft, Determinismus, Integrität der Tests für KI-Änderungen | das Qualitätsdokument führt Grundsätze für **jede** Änderung und verweist |
| `check_manifest` (Prüfung 8) prüft Schlüssel und Werte, **nicht die Existenz von `path`**; keine Sonde | E10 |
| Beide Projekte: Pilot 14, Übungsrepositorium 7 Manifesteinträge, alle Pfade und alle drei Regeldateien vorhanden (gezählt) | die Erweiterung bricht keines |

### 2.2 Die Erstinstallation mit Muster – je Pack

`install.py --client <pack> --overlay general` in ein leeres Repositorium, daneben dieselbe
Installation ohne Muster; Validator in beiden, Standardlauf und `--strict-overlay`.

| Pack | Ergebnis |
|---|---|
| `claude-code` | Exit 0; sechs Dokumente unter `.koolie/project-overlay/documents/<typ>/muster-general.md`; Manifest mit genau sechs Einträgen `DOC-001` bis `DOC-006`, je K1, `entwurf`, `on-demand`; K1-Liste der Laufzeitfassung weiter `<TBD: …>`; Änderungsverlauf nennt die Dokumente |
| `devin-desktop` | dito |
| `openai-codex` | dito |

| Validatorlauf | Meldungen nur **mit** Muster, gegenüber derselben Installation ohne |
|---|---|
| Standardlauf, alle drei Packs | **keine** |
| `--strict-overlay`, alle drei Packs | **keine** |

⚠️ **Einzelbeobachtung, nicht reproduziert:** Ein Lauf `--strict-overlay` an der
Installation `openai-codex` **ohne** Muster meldete einmal die Hook-Sonde *„AP2-CC-16“*
(`devin-desktop/manifest.json`, Exit 1 statt 2). In sechs Wiederholungen – drei mit, drei
ohne Muster – trat sie nicht wieder auf. Kein Zusammenhang mit diesem Release erkennbar;
benannt, weil eine Prüfung, die in acht gleichen Läufen einmal anders antwortet, ein
eigener Gegenstand ist.

⚠️ **Zwei Befunde am eigenen Bau, beide vor der Auslieferung gefangen:**
(1) Die Musterdatei führt unter *„Die Dokumente“* eine zweite Tabelle (Feld, Wert, Warum),
deren erste Spalte `status` und `load` nennt – der Leser hätte sie als Typen gelesen,
dieselbe Falle wie der Wächter von `1.5.0`. Der Abschnitt endet jetzt an jeder
Überschrift. (2) Die erste Fassung der Sonden zu Prüfung 8 las das Manifest des
Quellrepositoriums – und das steht in der `.gitignore`. Am Gegenbeweis brachen alle drei
mit *FileNotFoundError* ab. Sie schreiben das Manifest jetzt aus der versionierten
Vorlage.

### 2.3 Wirkungsnachweis – Sonden und Gegenproben, mit Gegenbeweis

| Einheit | Stand `1.6.0` | Gegenbeweis |
|---|---|---|
| Sonden `8a`, `8b` | OK | mit dem Validator aus `1.5.0`: **je FEHL** |
| Gegenprobe `8a` | OK | mit dem Validator aus `1.5.0`: FEHL – **nicht an Prüfung 8**, sondern an dessen eigener Sondenmengenzeile, die Prüfung 8 noch nicht nennt (D-86) |
| `M359` bis `M359b`, Gegenprobe `M359c` | OK | mit `install.py` aus `1.5.0`: Bündel bricht ab (`KeyError: 'dokumente'`) |
| `M355` bis `M355e` | unverändert OK | – |

Der Gegenbeweis läuft an einer **vollständigen** Kopie des Arbeitsbaums: An einer
Auscheckung aus `git ls-files` fehlen die ignorierten Wurzeldateien (`AGENTS.md`, das
Overlay des Quellrepositoriums), und **jede** Gegenprobe meldet dort *„Pflichtpfad
fehlt“* – eine Eigenschaft des Apparats, nicht dieses Release.

## 3. Abnahme

| Lauf | Ergebnis |
|---|---|
| Validator | **0 Fehler, 0 Warnungen**, beide Kodierungsumgebungen |
| Sondenlauf | **330 Einheiten, alle bestanden** (vorher 327; neu die Sonden `8a`, `8b`, die Gegenprobe `8a` und im Bündel `sonden_overlay_muster` die Einheiten `M359` bis `M359c`), beide Kodierungsumgebungen Exit 0 und oberhalb der Trennlinie zeilengleich (542 Zeilen), rund 525 s Wanduhr je Lauf; **Abnahmelauf gegen den fertigen Baum zeilengleich** |
| Pilot / Übungsrepo `--strict-overlay` nach der Hebung | Pilot **1 Fehler, 2 Warnungen**, alle im projekteigenen `CHANGELOG.md`, unverändert; Übungsrepo **0 Fehler, 1 Warnung** (Laufzeitfassung 6.095 Zeichen, SOLL-Grenze 6.000, unverändert). **Prüfung 8 in beiden still**; Auskunft über ignorierte Kerndateien im Pilot weiterhin **38** |
| Bau | alle drei Word-Fassungen `v1.6.0` in `build/out/` (2.054.889 / 2.053.579 / 2.049.543 Bytes), im Erzeugnis nachgezählt: Dokumentversion `1.6.0`, *„89 Prüfungen“*, die Musterdokumente je zweimal genannt |

## 4. Nebenhandlungen außerhalb des Kerns

- Signierte Marke `v1.5.0` (vom Owner gesetzt, `Good "git" signature`) **vor** dem
  Gitea-Release gepusht, remote annotiert. Schritte 5 bis 7 aus `RELEASE_PROCESS.md` 4.1:
  `koolie-1.5.0.tar.gz`, **544 Dateien** = `git ls-tree` der Marke, kein CRLF (bytegenau
  gezählt), Lizenz an beiden Stellen gleich, kein `build/out/`; Gitea-Release mit Archiv
  und Prüfsumme, beide Anhänge bytegleich zurückgelesen.

## 5. Offen

- Ob ein Musterdokument auf *jedes* Projekt paßt, prüft keine Maschine (D-359).
- Die Einzelbeobachtung zur Hook-Sonde *„AP2-CC-16“* (2.2).
- `1.7.0`: ob der Installer Python voraussetzen darf (Planabschnitt der Roadmap).
