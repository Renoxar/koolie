# Änderungsantrag `CR-2026-165`

| Feld | Inhalt |
|---|---|
| Titel | Das Banner des Installationsdialogs – und der Name, der an einer Stelle bleibt |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-30 |
| Betroffene Artefakte | `banner.py` (neu), `install_dialog.py`, `LICENSE-HINWEIS.md`, `tests/scripts/pruefungen/bestand.py` (URL-Allowlist von Prüfung 6), `tests/scripts/sonden/teil15_banner_und_nachlauf.py` (neu), `tests/scripts/probe-pruefungen.py` |
| Ebene laut Entscheidungsbaum 6 | Framework Core (Werkzeug der Installation) |
| Art | Erweiterung ohne Overlay-Bruch; Teil des PATCH-Release `1.20.3`, ohne Kontingent |
| Dringlichkeit | Antrag des Owners vom 2026-09-30, umzusetzen mit `1.20.3` |
| Status | 🟢 **entschieden am 2026-09-30** (E1 bis E8) |

---

## 1. Anlass

Der Owner hat am 2026-09-30 einen Entwurf „Installer-Banner“ vorgelegt (Entwurf `CR-001`, Anhang dieses Antrags): Der interaktive Installationsdialog soll beim Start ein Terminal-Banner ausgeben – ein Koolie im Profil, der über der linken oberen Ecke einer Box steht und ihren oberen Rahmen unterbricht, dazu Wortmarke, Version, zwei Textzeilen und eine Fußzeile mit Copyright, Lizenz und Repository. Das Banner ist Darstellung; es darf den Dialog weder verzögern noch abbrechen. Die Vorschau des Entwurfs (`koolie_banner_final_preview.png`) liegt außerhalb des Repositoriums; maßgeblich ist die Textreferenz in Anhang 5.1.

## 2. Vorprüfung

Vor der Vorlage erhoben, ohne Modell:

- **Die Versionsquelle ist `VERSION` im Kern.** Koolie ist kein Python-Paket; `importlib.metadata` und `pyproject.toml` aus dem Entwurf (I-1, O-1) gibt es nicht. Der Dialog liest die Version bereits über `install.kern_version()`.
- **Der Lizenzhinweis nannte nur „Version 3“.** Ohne den Zusatz „oder jede spätere Version“ gilt faktisch `GPL-3.0-only`; eine SPDX-Kennung stand in keinem Träger (O-3).
- **Die Repository-URL stand in keinem Träger.** Prüfung 6 hätte sie als URL außerhalb der Allowlist gewarnt.
- **Der Name in der Fußzeile wäre die zweite Stelle im Kern, die eine Person nennt.** Nach D-323 ist `LICENSE-HINWEIS.md` die einzige.
- **`install_dialog.py` gibt bewusst nur ASCII aus** (die Codepage einer Konsole, die ein Doppelklick öffnet). Es wertet keine Argumente aus, die Starter reichen keine durch, und `--quiet` gibt es nicht (F-4).
- **Python schreibt ab 3.6 in eine Windows-Konsole über die Unicode-Schnittstelle.** Eine Prüfung auf Codepage 65001 (T-5) hielte eine deutsche Konsole (850) immer bei der Textvariante, obwohl die Zeichen ankommen.
- **Die Sonden `T362g` und `T362h` fahren den Dialog über eine Pipe** – die Frage O-2 trifft den Prüfapparat unmittelbar.

## 3. Vorlage zur Entscheidung

| # | Frage | Entscheidung | Preis |
|---|---|---|---|
| E1 | Welche Lizenzfassung (O-3)? | `GPL-3.0-only` als SPDX-Kennung im Lizenzhinweis; das Banner zeigt die Kurzform `GPL-3.0` und liest sie aus dieser Zeile (D-507) | Eine spätere GPL-Fassung gilt nur nach neuer Entscheidung des Rechteinhabers |
| E2 | Wie kommt der Name ins Banner? | Zur Laufzeit aus der Copyright-Zeile von `LICENSE-HINWEIS.md`; in diesem Antrag und im Prüfapparat steht `<FRAMEWORK_OWNER>` (D-507) | Fehlt die Zeile, entfällt der Name im Banner |
| E3 | Welche Repository-URL? | `https://github.com/Renoxar/koolie`, eng gefasst in der URL-Allowlist von Prüfung 6 (D-507) | Die Allowlist nennt erstmals ein Repositorium statt einer Domain |
| E4 | Eigenes Modul oder im Dialog (O-5)? | Eigenes Modul `banner.py` neben dem Dialog; der Dialog ruft es in einer Hülle, die jede Ausnahme schluckt (D-506) | Eine Kerndatei mehr in jeder Installation, auch im Lieferumfang `nutzung` |
| E5 | Versionsquelle (O-1)? | `VERSION` (D-506) | – |
| E6 | Ausgabe ohne Terminal (O-2)? | Textvariante ohne Farbe – Pipe und Protokoll tragen Name und Version (D-506) | Vier Zeilen mehr in jeder mitgeschnittenen Installation |
| E7 | Schalter (O-6, F-4)? | `--no-banner` und `KOOLIE_NO_BANNER=1`; `--quiet` entfällt, weil es ihn nicht gibt. Die Starter reichen keine Argumente durch – für sie ist die Variable der Weg (D-506) | – |
| E8 | Windows und Hyperlink (T-5, T-6, O-4)? | Die Codepage wird nicht geprüft, entscheidend ist die Kodierung, die Python meldet; die Terminalsteuerung wird eingeschaltet, sonst Textvariante; die alte Konsole (ohne `WT_SESSION` und `TERM_PROGRAM`) bekommt die Vollvariante erst ab 81 Spalten; Windows Terminal gilt als Truecolor; kein OSC-8-Hyperlink (D-506) | Ob die alte Konsole alle Zeichen darstellt, ist nicht gemessen – das bleibt der Sichtprüfung des Owners |

O-7 (Höhe unter 25 Zeilen) gilt wie vorgeschlagen: keine Prüfung. N-4 (Tests mit `pytest` in einer CI) setzt dieses Repositorium mit seinem eigenen Prüfapparat um: Die Sonden `T506a` bis `T506k` laufen in jedem Sondenlauf.

## 4. Umsetzung

1. **`banner.py`:** Hund und Zonenkarte als zwei gleich große Raster, die Box mit berechnetem Abstand, Farbe in Läufen je Zone mit Rückstellung am Zeilenende; Auswahl nach Abschnitt 6 des Entwurfs mit den Abweichungen aus E8; Vorschau mit `python .koolie/core/banner.py --variante voll --farbe true`.
2. **`install_dialog.py`:** das Banner vor der ersten Zeile, `--no-banner`, Hülle um Import und Aufruf.
3. **`LICENSE-HINWEIS.md`:** die SPDX-Kennung (Version `0.2.2`).
4. **Prüfung 6:** die URL in der Allowlist.
5. **Sonden:** Bündel `sonden_installer_banner` in Teil 15 – Voll-, Kompakt- und Textvariante zeichengenau gegen Anhang 5.1, 5.4 und 5.5, die Zonenkarte gegen 5.2, Auswahl und Farbstufe, `NO_COLOR` ohne Steuerzeichen, der Dialog über eine Pipe und mit beiden Schaltern, ASCII ohne Ausnahme, ein defektes Asset und ein nicht ladbares Modul ohne Abbruch, Fußzeile und Version aus ihren Quellen.

## 5. Entscheidung

🟢 **Angenommen am 2026-09-30.** Die Fragen nach Lizenzfassung, Name und URL hat der Owner beantwortet; den übrigen Empfehlungen folgt er.

| # | Entscheidung | Decision Record |
|---|---|---|
| E1–E3 | Lizenzkennung, Name, URL | D-507 |
| E4–E8 | Modul, Quellen, Auswahl und Schalter | D-506 |

## 6. Messung und Belege

Kein Sitzungslauf. Die Referenzen in Anhang 5.1, 5.2 und 5.4 sind aus `banner.py` erzeugt, nachdem die Ausgabe gegen den Entwurf des Owners zeichengleich gehalten worden war (mit seinem Namen, 25 und 13 Zeilen, dazu die Zonenkarte); danach ist nur der Name durch `<FRAMEWORK_OWNER>` ersetzt. Der Entwurf selbst liegt außerhalb des Repositoriums. Protokoll `tests/protocols/2026-09-30-nachlauf-banner.md`.

---

## Anhang: Der Entwurf des Owners

Wortlaut des Entwurfs `CR-001` vom 2026-09-30. Die Überschriften sind um eine Ebene tiefer gesetzt, der Name des Antragstellers ist durch `<FRAMEWORK_OWNER>` ersetzt (D-323), und die Referenzblöcke 5.1, 5.2, 5.4 und 5.5 tragen den Platzhalter in derselben Breite, in der ihn das Banner setzen würde. Die sechs Darstellungsanforderungen des Entwurfs (dort Buchstabe D mit Nummer) heißen hier `DS-1` bis `DS-6`, weil `D-<Zahl>` in diesem Repositorium einen Decision Record bezeichnet; der Platzhalter der Hyperlink-Sequenz in Anhang B ist kleingeschrieben. Wo der Entwurf von der Umsetzung abweicht, gilt Abschnitt 3.

### CR-001 · Installer-Banner „Koolie"

| Feld | Inhalt |
|---|---|
| Status | Entwurf – zur Freigabe |
| Datum | 30.09.2026 |
| Antragsteller | <FRAMEWORK_OWNER> |
| Komponente | Koolie – interaktiver Konsolen-Installer |
| Art der Änderung | Feature (Ausgabe/Darstellung); keine Änderung an der Installationslogik |
| Referenz | Designentwurf „Konzept 4 – Hybrid", Vorschau `koolie_banner_final_preview.png` |
| Umsetzungsentscheidung offen | Auslagerung in eigenes Python-Modul vs. Inline im Installer (siehe Abschnitt 9) |

---

#### 1 Zusammenfassung

Der interaktive Installer von Koolie soll beim Start ein Terminal-Banner ausgeben, das als visuelles Markenzeichen des Frameworks dient: ein stilisierter Koolie (Hütehund, Profil), der über der linken oberen Ecke einer Terminal-Box steht und den oberen Rahmen unterbricht. Die Box enthält die Wortmarke `KOOLIE`, die Versionsnummer, eine Catch-Line, eine sachliche Unterzeile sowie eine Fußzeile mit Copyright, Lizenz und Repository-URL.

Das Banner ist rein informativ und dekorativ. Es darf den Installer weder verzögern noch zum Abbruch bringen und muss in jeder Terminalumgebung eine saubere Ausgabe liefern – notfalls als reine Textvariante.

#### 2 Motivation

- Wiedererkennung: Der Installer ist der erste Kontaktpunkt mit Koolie. Ein eigenständiges Banner unterscheidet das Tool von generischen Installer-Skripten.
- Metapher im Bild: Der Hund steht *auf* der Linie – Kopf außerhalb der Box, Brust innerhalb, der Rahmen läuft hinter ihm durch. Das ist die Kernaussage des Frameworks (offenes Gelände mit verstandener Grenze, kein Käfig, keine Leine) ohne erklärenden Text.
- Pflichtangaben an prominenter Stelle: Version, Lizenz (GPL-3.0), Copyright und Repository-Link sind beim Start sichtbar.

#### 3 Scope

**Im Scope**
- Ausgabe des Banners beim Start des interaktiven Installers (einmalig, vor der ersten Nutzerinteraktion).
- Vier Ausgabevarianten in Abhängigkeit von Terminalbreite, Encoding und Farbunterstützung (Abschnitt 6).
- Dynamische Einbindung der Versionsnummer.
- Abschaltbarkeit (Flag/Umgebungsvariable).

**Nicht im Scope**
- Änderungen an Ablauf, Prompts oder Logik des Installers.
- Banner an anderen Stellen (z. B. `koolie --version`, README) – kann später denselben Asset-Code nutzen, ist aber nicht Teil dieses CR.
- Animationen, Farbverläufe, Themes für helle Terminalhintergründe.
- Neue Pflichtabhängigkeiten (siehe N-1).

#### 4 Anforderungen

##### 4.1 Funktional

| ID | Anforderung |
|---|---|
| F-1 | Das Banner wird beim Start des interaktiven Installers genau einmal ausgegeben, bevor die erste Eingabeaufforderung erscheint. |
| F-2 | Inhalte der Vollvariante: Koolie-Grafik, Wortmarke `KOOLIE`, Version, Catch-Line, Unterzeile, Fußzeile (Copyright, Lizenz, Repository-URL). |
| F-3 | Die Version wird zur Laufzeit aus einer einzigen Quelle gelesen (Single Source of Truth, siehe I-1) und nicht im Banner hart codiert. |
| F-4 | Das Banner lässt sich unterdrücken über ein CLI-Flag (Vorschlag: `--no-banner`) und eine Umgebungsvariable (Vorschlag: `KOOLIE_NO_BANNER=1`). Ein vorhandenes `--quiet`/`-q` unterdrückt es ebenfalls. |
| F-5 | Die Banner-Ausgabe darf den Installer nie abbrechen. Jede Ausnahme beim Rendern oder Schreiben wird abgefangen; Fallback ist die Textvariante, im Zweifel gar keine Ausgabe. |
| F-6 | Nach dem Banner folgt genau eine Leerzeile, davor keine. Das Banner wird linksbündig ohne Einrückung ausgegeben. |

##### 4.2 Darstellung

| ID | Anforderung |
|---|---|
| DS-1 | Die Vollvariante entspricht zeichengenau der Referenzgrafik in 5.1 (25 Zeilen × 80 Spalten). |
| DS-2 | Die Farbgebung folgt der Zonenkarte 5.2 und der Farbspezifikation 5.3. Es werden keine weiteren Farben verwendet. |
| DS-3 | Die Monochromvariante ist formgleich mit der Farbvariante; es entfallen ausschließlich die Escape-Sequenzen. |
| DS-4 | Keine Animation, kein Blinken, keine Hintergrundfarben. Der Hintergrund bleibt der Terminalhintergrund. |
| DS-5 | Die Hundegrafik ist ein statisches Asset. Die Textzeilen der Box (Version, Catch-Line, Unterzeile, Fußzeile) werden aus Konstanten generiert; das Padding wird berechnet, damit Änderungen am Text die Ausrichtung nicht zerstören. |
| DS-6 | Zeichenvorrat ausschließlich: Block Elements (U+2580–U+259F), Box Drawing (U+2500–U+257F), ASCII sowie `©` (U+00A9), `·` (U+00B7) und `é` in der Fußzeile. Keine Braille-, Emoji- oder Ambiguous-Width-Zeichen darüber hinaus (Anhang A). |

##### 4.3 Terminal-Erkennung und Fallbacks

| ID | Anforderung |
|---|---|
| T-1 | **Encoding:** Nur wenn `sys.stdout.encoding` UTF-8 ist (case-insensitiv, `utf-8`/`utf8`), werden Block- und Box-Zeichen ausgegeben. Sonst Textvariante (ASCII, Abschnitt 5.5). |
| T-2 | **Breite:** Ermittlung über `shutil.get_terminal_size(fallback=(80, 24))`. Schwellen: ≥ 80 Spalten → Vollvariante, 66–79 → Kompaktvariante, < 66 → Textvariante. Die Höhe wird nicht geprüft. |
| T-3 | **Farbe:** Farbausgabe nur wenn (a) `stdout` ein TTY ist, (b) `NO_COLOR` nicht gesetzt ist, (c) `TERM` nicht `dumb` ist. Stufen: `COLORTERM` ∈ {`truecolor`, `24bit`} → Truecolor; sonst `TERM` enthält `256color` → 256-Farben-Palette; sonst monochrom. Auf 16-Farben-Terminals wird bewusst monochrom ausgegeben (keine Näherung). |
| T-4 | **Nicht-TTY** (Pipe, Redirect, CI-Log): keine Escape-Sequenzen. Ob dann die Textvariante oder gar nichts ausgegeben wird, ist Entscheidung O-2. |
| T-5 | **Windows:** Auf Windows 10 (ab Build 10586) und Windows Terminal wird die VT-Verarbeitung aktiviert (`ENABLE_VIRTUAL_TERMINAL_PROCESSING` über `SetConsoleMode` oder den dokumentierten `os.system("")`-Aufruf). Ist VT nicht aktivierbar oder die Codepage nicht 65001 → Textvariante. |
| T-6 | **Auto-Wrap:** Ältere Windows-Konsolen brechen bei exakt 80 Zeichen sofort um und erzeugen Leerzeilen. Dort ist für die Vollvariante eine Breite ≥ 81 zu fordern (nur Windows-Legacy-Konsole, sonst ≥ 80). |

##### 4.4 Inhalte und Datenquellen

| ID | Anforderung |
|---|---|
| I-1 | **Version:** Format `v<version>`, rechtsbündig unter der rechten Kante der Wortmarke (Spalte 70 innerhalb der Box). Quelle ist die Paketversion (`importlib.metadata.version("koolie")` bzw. `koolie.__version__`). **Achtung:** Läuft der Installer, bevor das Paket installiert ist (Bootstrap-Skript), ist diese Quelle nicht verfügbar; dann muss die Version aus dem Installer selbst bzw. einer `VERSION`-Datei kommen (Entscheidung O-1). Zeichenketten bis 42 Zeichen wachsen nach links; längere werden abgeschnitten. |
| I-2 | **Copyright/Lizenz:** Text `© 2026 <FRAMEWORK_OWNER> · GPL-3.0`. Das Jahr ist eine Konstante und wird bei Bedarf zu einem Zeitraum erweitert (`2026–2027`), nicht automatisch aus der Systemzeit erzeugt. Die Lizenzangabe muss mit `LICENSE` und `pyproject.toml` übereinstimmen (Entscheidung O-3 zur SPDX-Kennung). |
| I-3 | **Repository:** Vollvariante `https://github.com/Renoxar/koolie`, Kompaktvariante `github.com/Renoxar/koolie`. Optional als OSC-8-Hyperlink (Entscheidung O-4). |
| I-4 | **Catch-Line:** `The field is open. The edge is not.` – max. 47 Zeichen in der Vollvariante (Box-Innenbreite 78 abzüglich 29 Einzug und 2 Rand). |
| I-5 | **Unterzeile:** `Governance for AI coding assistants` – gleiche Längengrenze wie I-4. |
| I-6 | Alle Texte sind Konstanten an einer Stelle; sie werden nicht in die Grafik „eingebrannt". |

##### 4.5 Nicht-funktional

| ID | Anforderung |
|---|---|
| N-1 | Keine neue Pflichtabhängigkeit. Farbausgabe mit nativen ANSI-Sequenzen ist ausreichend. Ob `rich` oder `colorama` optional genutzt werden, entscheidet die Umsetzung; das Banner muss auch ohne funktionieren. |
| N-2 | Renderzeit vernachlässigbar (< 50 ms), keine Netzwerkzugriffe, keine Dateizugriffe außer ggf. Lesen der Versionsquelle. |
| N-3 | Grafik und Zonenkarte liegen als eine Datei bzw. ein Modul vor, damit spätere Designänderungen an genau einer Stelle erfolgen. |
| N-4 | Testbarkeit: Snapshot-Test der Monochromausgabe (zeichengenau), Tests der Auswahllogik (Breite, Encoding, TTY, `NO_COLOR`), Test, dass mit `NO_COLOR=1` kein `\x1b` im Output vorkommt. |

#### 5 Referenz-Design

##### 5.1 Vollvariante (≥ 80 Spalten, UTF-8) – Monochrom-Referenz

25 Zeilen × 80 Spalten. Zeilen 1–12 sind der Hund oberhalb der Box, Zeile 13 ist der obere Rahmen, den der Hund unterbricht, Zeilen 13–21 enthalten Hund und Box gemeinsam.

```text
                 ▄
           ▄    ▄█▄
          ▄█▄  ▄█▒█▄
         ▄████▄██▒██▄
        ▄████████████▄
        ██████████████▄
        ███████████░███
        ███████████████▄▄▄▄▄▄▄▄▄
        █████████████████████████▓▓
         ████████████████████████▓▓▓▓
         ████████████████████████▓▓▓
          ████████████▒▒▒▒▒▒▒▒▒▒▀
╭─────────██████████▒▒▒▒▒▒▒▒▀▀─────────────────────────────────────────────────╮
│         ████████▒▒▒▒▒▀▀                                                      │
│        ████████▒▒▒░         ██  ▄█  ▄████▄  ▄████▄  ██      ██  ██████       │
│       ████████▒▒▒░░░        ██ ▄█▀  ██  ██  ██  ██  ██      ██  ██           │
│      ▄███████▒▒▒▒░░░░▄      ████▀   ██  ██  ██  ██  ██      ██  █████        │
│     ▄███████▒▒▒▒░░░░░▄      ██ ▀█▄  ██  ██  ██  ██  ██      ██  ██           │
│    ▄███████▒▒▒▒▒░░░░░░▄     ██  ▀█  ▀████▀  ▀████▀  ██████  ██  ██████       │
│   ▄████████▒▒▒▒░░░░░░░░                                         v0.1.0       │
│  ▄████████▒▒▒▒▒░░░░░░░▀     The field is open. The edge is not.              │
│                             Governance for AI coding assistants              │
├──────────────────────────────────────────────────────────────────────────────┤
│  © 2026 <FRAMEWORK_OWNER> · GPL-3.0       https://github.com/Renoxar/koolie  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

Die Versionsnummer `v0.1.0` ist ein Platzhalter (I-1). Das Hunde-Asset allein (21 Zeilen, wird transparent über die Box gelegt, Leerzeichen sind durchsichtig):

```text
                 ▄
           ▄    ▄█▄
          ▄█▄  ▄█▒█▄
         ▄████▄██▒██▄
        ▄████████████▄
        ██████████████▄
        ███████████░███
        ███████████████▄▄▄▄▄▄▄▄▄
        █████████████████████████▓▓
         ████████████████████████▓▓▓▓
         ████████████████████████▓▓▓
          ████████████▒▒▒▒▒▒▒▒▒▒▀
          ██████████▒▒▒▒▒▒▒▒▀▀
          ████████▒▒▒▒▒▀▀
         ████████▒▒▒░
        ████████▒▒▒░░░
       ▄███████▒▒▒▒░░░░▄
      ▄███████▒▒▒▒░░░░░▄
     ▄███████▒▒▒▒▒░░░░░░▄
    ▄████████▒▒▒▒░░░░░░░░
   ▄████████▒▒▒▒▒░░░░░░░▀
```

Kompositionsregel: Box-Zeilen zuerst schreiben, Hund-Zeilen darüber legen; nur Nicht-Leerzeichen des Hundes überschreiben Box-Zeichen. Offset des Box-Assets: Zeile 13, Spalte 1 (0-basiert: Zeile 12, Spalte 0).

##### 5.2 Farbzonen-Karte

Zellgenau parallel zu 5.1. Jeder Buchstabe steht für eine Farbrolle aus 5.3; Leerzeichen bleiben ungefärbt. Diese Karte ist die Implementierungsgrundlage: Grafik-Layer und Zonen-Layer sind zwei gleich große Zeichen-Raster, der Renderer färbt zeilenweise zusammenhängende gleiche Zonen mit je einer Escape-Sequenz.

```text
                 F
           F    FFF
          FFF  FFLFF
         FMFFFFFFLFFF
        FFFFMMFFFFFFFF
        FFFFMFFFFFFFFFF
        FFFFFFFFFFFEFFF
        FFMMFFFFFFFFFFFFFFFFFFFF
        FFFFFFFFFMMFFFFFFFFFFFFFFNN
         FFFFFFFFMFFFFFFFFFFFFFFFNNNN
         FFFFMFFFFFFFFFFFFFFFFFFFNNN
          FFFFMFFFFFFFLLLLLLLLLLL
BBBBBBBBBBFFFFFFFFFFLLLLLLLLLFBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
B         FFFFFFFFLLLLLLF                                                      B
B        FFFFFFFFLLLL         KK  KK  KKKKKK  KKKKKK  KK      KK  KKKKKK       B
B       FFFFFFFFLLLLLL        KK KKK  KK  KK  KK  KK  KK      KK  KK           B
B      FFFFFFFFLLLLLLLLL      KKKKK   KK  KK  KK  KK  KK      KK  KKKKK        B
B     FFFFFFFFLLLLLLLLLL      KK KKK  KK  KK  KK  KK  KK      KK  KK           B
B    FFFFFFFFLLLLLLLLLLLL     KK  KK  KKKKKK  KKKKKK  KKKKKK  KK  KKKKKK       B
B   FFFFFFFFFLLLLLLLLLLLL                                         VVVVVV       B
B  FFFFFFFFFLLLLLLLLLLLLL     CCC CCCCC CC CCCCC CCC CCCC CC CCCC              B
B                             SSSSSSSSSS SSS SS SSSSSS SSSSSSSSSS              B
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
B  T TTTT TTTTTTTTTTTTTTTTT T TTTTTTT       TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT  B
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
```

##### 5.3 Farbspezifikation

| Zone | Bereich | Zeichen | Truecolor | 256-Farben | Attribut |
|---|---|---|---|---|---|
| F | Fell Grundton (Schädel, Ohren, Fang, Nacken, Kanten) | `█ ▄ ▀` | `#B8BEC7` | 250 | – |
| M | Merle-Akzent (11 einzelne Zellen, feste Positionen laut Karte) | `█` | `#5E7F99` | 67 | – |
| N | Nase | `▓` | `#3A4657` | 239 | – |
| E | Auge (eine Zelle) | `░` | `#4FB3C8` | 74 | nicht bold |
| L | helles Fell (Ohrinnenseite, Unterkiefer, Kehle, Brust, zugehörige Kanten) | `▒ ░ ▄ ▀` | `#E6E9EC` | 254 | – |
| B | Rahmen und Trennlinie | Box Drawing | `#3B8C8C` | 66 | – |
| K | Wortmarke `KOOLIE` | `█ ▄ ▀` | `#5CD6E0` | 80 | bold |
| V | Version | Text | `#3B8C8C` | 66 | – |
| C | Catch-Line | Text | `#E0B36A` | 179 | – |
| S | Unterzeile | Text | `#8A9199` | 245 | dim |
| T | Fußzeile (Copyright, Lizenz, URL) | Text | `#8A9199` | 245 | dim |

Hinweise:
- `▓ ▒ ░` lassen Terminalhintergrund durchscheinen; die Palette ist für dunkle Hintergründe abgestimmt. Auf hellem Hintergrund bleibt die Form lesbar, die Tonstufen kehren sich aber um. Ein helles Theme ist nicht Teil dieses CR.
- Das Auge bleibt bewusst `░` in gedämpftem Cyan, kein Vollblock: sonst wirkt es wie ein Comic-Punkt.
- Merle-Zellen sind reine Umfärbung; monochrom sind sie unsichtbar.
- Die Escape-Sequenzen stehen in Anhang B.

##### 5.4 Kompaktvariante (66–79 Spalten)

Box ohne Hund, 13 Zeilen × 66 Spalten, gleiche Inhalte, URL ohne Schema. Farbzonen wie oben (B, K, V, C, S, T).

```text
╭────────────────────────────────────────────────────────────────╮
│                                                                │
│   ██  ▄█  ▄████▄  ▄████▄  ██      ██  ██████                   │
│   ██ ▄█▀  ██  ██  ██  ██  ██      ██  ██                       │
│   ████▀   ██  ██  ██  ██  ██      ██  █████                    │
│   ██ ▀█▄  ██  ██  ██  ██  ██      ██  ██                       │
│   ██  ▀█  ▀████▀  ▀████▀  ██████  ██  ██████                   │
│                                       v0.1.0                   │
│   The field is open. The edge is not.                          │
│   Governance for AI coding assistants                          │
├────────────────────────────────────────────────────────────────┤
│  © 2026 <FRAMEWORK_OWNER> · GPL-3.0 github.com/Renoxar/koolie  │
╰────────────────────────────────────────────────────────────────╯
```

##### 5.5 Textvariante (< 66 Spalten, kein UTF-8 oder VT nicht verfügbar)

Reines ASCII, keine Escape-Sequenzen, keine Box:

```text
KOOLIE v0.1.0
The field is open. The edge is not.
Governance for AI coding assistants
(c) 2026 <FRAMEWORK_OWNER> - GPL-3.0 - https://github.com/Renoxar/koolie
```

Das `é` wird in dieser Variante nur dann transliteriert, wenn das Ausgabe-Encoding es nicht darstellen kann (`str.encode(enc, errors="strict")` prüfen); bei Latin-1-Terminals bleibt `René` erhalten.

#### 6 Entscheidungslogik

Reihenfolge der Prüfung, erste zutreffende Regel gewinnt:

| # | Bedingung | Ausgabe |
|---|---|---|
| 1 | `--no-banner`, `--quiet` oder `KOOLIE_NO_BANNER=1` | nichts |
| 2 | `stdout` kein TTY | Textvariante ohne Farbe *oder* nichts (O-2) |
| 3 | Encoding nicht UTF-8 oder (Windows) VT nicht aktivierbar / Codepage ≠ 65001 | Textvariante |
| 4 | Breite < 66 | Textvariante |
| 5 | Breite 66–79 | Kompaktvariante |
| 6 | Breite ≥ 80 (Windows-Legacy-Konsole: ≥ 81) | Vollvariante |

Farbstufe unabhängig davon nach T-3: Truecolor → 256 → monochrom; `NO_COLOR` erzwingt monochrom, `TERM=dumb` ebenfalls.

#### 7 Akzeptanzkriterien

- [ ] In einem 80×30-Terminal mit UTF-8 und `COLORTERM=truecolor` entspricht die Ausgabe zeichengenau der Referenz 5.1 (Diff nach Entfernen der Escape-Sequenzen ist leer) und die Farben den Zonen 5.2/5.3.
- [ ] Mit `NO_COLOR=1` ist die Ausgabe formgleich und enthält kein `\x1b`.
- [ ] `TERM=xterm-256color` ohne `COLORTERM` verwendet die 256-Farben-Indizes aus 5.3.
- [ ] `COLUMNS=70` liefert die Kompaktvariante 5.4, `COLUMNS=60` die Textvariante 5.5.
- [ ] `PYTHONIOENCODING=ascii` bzw. `LANG=C` erzeugt keinen `UnicodeEncodeError`, sondern die Textvariante.
- [ ] `installer | cat` erzeugt keine Escape-Sequenzen (und das in O-2 festgelegte Verhalten).
- [ ] `--no-banner` und `KOOLIE_NO_BANNER=1` unterdrücken jede Ausgabe.
- [ ] Die angezeigte Version stimmt mit der Paketversion bzw. der festgelegten Versionsquelle überein.
- [ ] Copyright, Lizenzkennung und URL stimmen mit `LICENSE`, `pyproject.toml` und dem Repository überein.
- [ ] Windows Terminal und PowerShell 7 zeigen die Vollvariante; die Legacy-Konsole (`cmd.exe` ohne VT) zeigt mindestens die Textvariante ohne Artefakte.
- [ ] Ein provozierter Fehler im Renderer (z. B. defektes Asset) bricht den Installer nicht ab.
- [ ] Ein Snapshot-Test für die Monochromausgabe existiert und läuft in der CI.

#### 8 Umsetzungshinweise (unverbindlich)

- **Datenhaltung:** Grafik-Layer (5.1 ohne Box-Textzeilen) und Zonen-Layer (5.2) als zwei Tupel von Strings gleicher Länge. Der Renderer läuft pro Zeile über die Zellen, fasst Läufe gleicher Zone zusammen und gibt pro Lauf eine Farbsequenz und am Zeilenende `ESC[0m` aus. Kein Markup-Parser nötig.
- **Box-Zeilen generieren:** Version, Catch-Line, Unterzeile und Fußzeile werden mit berechnetem Padding in die Box-Zeilen eingesetzt (Innenbreite 78, Einzug 29, Fußzeile Rand 2 links/rechts). Der Hund wird danach transparent darübergelegt.
- **Modulschnitt (Option A):** `koolie/installer/banner.py` mit einer Funktion `print_banner(stream=None, *, force_variant=None, force_color=None)`. Die `force_*`-Parameter dienen Tests und einem späteren `--banner-preview`.
- **Inline (Option B):** Bei einem Single-File-Installer dieselben Datenstrukturen direkt im Skript; dann Snapshot-Test gegen eine Referenzdatei im Repository.
- **Tests:** `pytest` mit `capsys` und `monkeypatch` für `COLUMNS`, `NO_COLOR`, `COLORTERM`, `TERM`, `sys.stdout.isatty`, `sys.stdout.encoding`.
- **Windows:** VT aktivieren, bevor die erste Escape-Sequenz geschrieben wird; Fehler beim Aktivieren still in Monochrom/Text degradieren.

#### 9 Offene Punkte / Entscheidungen

| ID | Frage | Vorschlag |
|---|---|---|
| O-1 | Versionsquelle, wenn der Installer vor der Paketinstallation läuft | Konstante/`VERSION`-Datei im Installer, gepflegt über den Release-Prozess; Paketmetadaten nur als Fallback |
| O-2 | Verhalten bei Nicht-TTY (Pipe/CI-Log) | Textvariante ohne Farbe, damit Logs Name und Version enthalten |
| O-3 | SPDX-Kennung: `GPL-3.0-only` oder `GPL-3.0-or-later` | Muss mit `LICENSE` übereinstimmen; im Banner bleibt die Kurzform `GPL-3.0` |
| O-4 | Repository-URL als OSC-8-Hyperlink | Ja, wenn Truecolor-Stufe aktiv ist; sonst Klartext |
| O-5 | Eigenes Modul vs. Inline | Wird bei der Umsetzung entschieden (Vorgabe des Antragstellers) |
| O-6 | Flag-Namen (`--no-banner`, `KOOLIE_NO_BANNER`) | Wie vorgeschlagen, sofern kein Konflikt mit bestehenden Optionen |
| O-7 | Verhalten bei Terminalhöhe < 25 Zeilen | Keine Prüfung; erste Zeile (Ohrspitze) scrollt weg, akzeptiert |

#### 10 Risiken

| Risiko | Auswirkung | Maßnahme |
|---|---|---|
| Font stellt `▓ ▒ ░` nicht unterscheidbar dar | Kehle/Nase wirken flach | Form trägt über Kontur; Farbvariante bleibt eindeutig; kein Handlungsbedarf |
| Terminal behandelt Ambiguous-Width-Zeichen (`©`, `·`, Box Drawing) als 2 Spalten (CJK-Locale) | Zeilen verschoben | Akzeptiertes Restrisiko; optional `wcwidth`-Prüfung mit Fallback auf Textvariante |
| Windows-Legacy-Konsole | Auto-Wrap bei 80 Spalten, fehlende Glyphen | T-5/T-6; Textvariante |
| Lange Versionsstrings (`v0.1.0.dev3+g1a2b3c`) | Wachsen nach links unter die Wortmarke | Erlaubt bis 42 Zeichen, sonst kürzen |
| Heller Terminalhintergrund | Tonstufen invertiert | Form bleibt lesbar; helles Theme außerhalb des Scope |

#### Anhang A – Zeicheninventar

| Zeichen | Codepoint | Verwendung |
|---|---|---|
| `█` | U+2588 | Fell, Wortmarke |
| `▓` | U+2593 | Nase |
| `▒` | U+2592 | helles Fell (Ohrinnenseite, Unterkiefer, Kehle) |
| `░` | U+2591 | Auge, Brust |
| `▀` `▄` | U+2580, U+2584 | Kanten, Wortmarke |
| `─` `│` | U+2500, U+2502 | Rahmen |
| `╭` `╮` `╰` `╯` | U+256D, U+256E, U+2570, U+256F | Rahmenecken |
| `├` `┤` | U+251C, U+2524 | Trennlinie Fußzeile |
| `©` `·` `é` | U+00A9, U+00B7, U+00E9 | Fußzeile |

#### Anhang B – ANSI-Sequenzen

`ESC` = `\x1b`.

| Zweck | Sequenz |
|---|---|
| Vordergrund Truecolor | `ESC[38;2;<R>;<G>;<B>m` |
| Vordergrund 256-Farben | `ESC[38;5;<N>m` |
| Bold | `ESC[1m` |
| Dim | `ESC[2m` |
| Reset | `ESC[0m` |
| OSC-8-Hyperlink (optional) | `ESC]8;;<url>ESC\<Text>ESC]8;;ESC\` |

Beispiel Wortmarke (Truecolor): `ESC[1mESC[38;2;92;214;224m` … `ESC[0m`. Reset am Ende jeder Zeile, nicht erst am Ende des Banners, damit ein Abbruch mittendrin keinen gefärbten Prompt hinterlässt.
