# Protokoll: Die Übergabe wird ein lokales Arbeitsdokument – und vier Prüfungen verlieren ihren Anker

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-24 |
| Release | `1.4.1` |
| Änderungsantrag | `CR-2026-134` |
| Art | Korrektur am Prüfapparat und an zwei Übernahmetexten – **keine Sitzung, kein Kontingent, kein Modelllauf** |
| Gegenstand | Die Übergabe aus dem Versionierten nehmen, ohne daß der Validator dabei leise weniger prüft; die Wurzel-README an `1.4.0` angleichen |
| Ergebnis | 🟢 **Entschieden und umgesetzt, `D-350` und `D-351`.** 🔴 **Vier Prüfungen hingen an der Übergabe, zwei davon hätten ihr Austragen nicht bemerkt** – gemessen mit Gegenbeweis. 🔴 **Und der erste Befehl der Übernahmeanleitung lief nicht** |

---

## 1. Was gefragt war

Der Framework Owner will die Übergabe und ihre Vorlage nicht mehr eingecheckt haben; beide
sollen nur lokal vorliegen. Die Prüfungen 67 und 78 (soweit sie die Übergabe betreffen)
sollen ersatzlos entfallen, das Kennzeichen des Quellrepositoriums eine eigene Datei
werden, Übergabe und Beilage getrennt bleiben. Dazu: die Wurzel-README auf den Stand von
`1.4.0` bringen.

## 2. Gegenprüfung

### 2.1 Was an der Übergabe hing

Gezählt mit `grep` über `validate-framework.py` und `probe-pruefungen.py`, **bevor** etwas
geändert wurde: Die Übergabe ist Gegenstand der Prüfungen **67** und **78** (vierter
Abschnitt) und **Anker** der Prüfungen **75, 78, 79 und 81** – an ihr unterschieden sie
Quellrepositorium und übernehmendes Projekt. 75 und 81 lesen dafür den **versionierten**
Bestand (`git ls-files`), 78 und 79 den Arbeitsbaum. Im Sondenapparat hingen die Einheiten
67a–d, die Gegenproben 67a/67b, 78d/78e und die Gegenprobe 82b an ihr.

### 2.2 🔴 Der Gegenbeweis: Das Austragen allein hätte niemand bemerkt

Eine Kopie des versionierten Bestands, die Übergabe **lokal vorhanden, aber nicht
verfolgt**, `README.md` durchgehend auf LF gestellt, `git init` und `git add -A`:

| Validator | Treffer auf `README.md: trägt …` |
|---|---|
| aus `1.4.0` (Anker: `UEBERGABE.md` im versionierten Bestand) | 🔴 **0** |
| aus `1.4.1` (Anker: `.koolie/QUELLREPOSITORIUM.md`) | 🟢 **1** |

➡️ ***Ein Anker, der nur an einem Arbeitsplatz liegt, ist keiner.*** Der alte Validator
lief in diesem Baum ohne Befund durch und prüfte dabei nur noch das Ausgelieferte.

### 2.3 Die README und ihre Nachbarn

| # | Fundstelle | Befund |
|---|---|---|
| R1 | `README.md`, Einleitung | zwei Client Packs genannt, drei ausgeliefert |
| R2 | `README.md`, Hinweis unter dem Baum | *„Eine eigene Hook-Datei gibt es nicht"* – bei `openai-codex` gibt es nur sie (`.codex/hooks.json`) |
| R3 | `README.md`, `install.py`-Tabelle und Hinweis | die Hook-Konfiguration als Projekteigentum für alle Packs; bei `openai-codex` gehört die Hook-Datei zum Kern (`shared_core`) und wird bei `--update` erneuert, womit sich ihr Hash und damit das Hook-Vertrauen ändert |
| R4 | `README.md`, Absatz zu `root-template/` | *„in beiden Manifesten"* – `seed_paths` ist in allen drei leer (gezählt) |
| 🔴 R5 | `README.md` und zweimal `docs/ADOPTION_GUIDE.md` | `cp -r .koolie/core/ /pfad/zum/projekt/` legt mit dem Schrägstrich am Quellpfad den Kern unter `<projekt>/core` ab – **der erste Befehl der Anleitung lief nicht** |
| N1 | `build/doc/00-kopf.md` | *„Ausgeliefert werden zwei"* – Prüfung 77 hält dort die Version, nicht den Inhalt |
| N2 | `governance/ADOPTION_REGISTRY.md` | Spalte `Overlay-Version` auf `0.3.3` und `1.1.0`, die Projekte trugen `0.3.5` und `1.3.0` – Prüfung 82 hält nur die Framework-Version |

## 3. Umsetzung

Wie in `CR-2026-134` Abschnitt 4. Die Nummer 67 bleibt im Register als *entfallen*;
Prüfung 40 verlangt ein lückenloses Register. Die Sondenmenge steht an allen drei Stellen
als *„6, 14, 18 bis 66 und 68 bis 88"*.

**Neu im Sondenapparat, beide im Bündel zu Prüfung 81:**

| Einheit | Was sie mißt |
|---|---|
| **Sonde 81d** | `README.md` – eine Datei der Wurzel, außerhalb des Kerns – auf der anderen Zeilenendeform wird im Quellrepositorium gemeldet. **Gegen den Vorstand fällt sie** (Abschnitt 2.2) |
| **Gegenprobe 81b** | dieselbe Datei ohne Kennzeichen, also in einem übernehmenden Projekt: nicht gemeldet |

## 4. Abnahme

| Lauf | Ergebnis |
|---|---|
| `validate-framework.py --root .` | **0 Fehler, 0 Warnungen** |
| `probe-pruefungen.py .` mit `PYTHONIOENCODING=utf-8` | 🟢 **alle Sonden und Gegenproben bestanden**, 323 Einheiten, Exit 0 |
| `probe-pruefungen.py .` ohne | 🟢 **alle Sonden und Gegenproben bestanden**, 323 Einheiten, Exit 0 |
| Ergebniszeilen oberhalb der Trennlinie, beide Läufe | 🟢 **zeilengleich** (511 Zeilen bis zur Trennlinie; darunter nur Laufzeiten, D-94) |

## 5. Was offen bleibt

- ⚠️ **Stand und Zahlen der Übergabe prüft niemand mehr** – der benannte Preis von D-350.
- ⚠️ **`K-104`** (eine Prüfung auf die Aussagen der Wurzel-README) bleibt, wo er steht.
  R1 bis R5 sind von Hand gefunden, und der schwerste davon – ein Befehl, der nicht lief –
  ist die Art Befund, die eine Textprüfung nicht sieht.
