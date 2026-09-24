# Änderungsantrag `CR-2026-135`

| Feld | Inhalt |
|---|---|
| Titel | Die Auskunft, die unter Windows nur Verzeichnisse sah – und drei Prüfungen, denen ein Umlaut den Pfad nahm |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-24 |
| Betroffene Artefakte | `install.py` (`ignorierte_kerndateien()`); `tests/scripts/validate-framework.py` (`_verfolgte_dateien()`, `_p75_verfolgt()`, neu `_git_pfade()`); `tests/scripts/probe-pruefungen.py` (Bündel `sonden_ignorierte_kerndateien` **neu**: Sonde `D349`, Gegenproben `D349a`/`D349b`; **Sonde 81e** neu); `governance/DECISION_LOG.md` (**D-352**, **K-120**, **K-121**); `governance/ADOPTION_REGISTRY.md`; `build/assemble.py` (Direktive `{{LOKALE-ERGAENZUNG}}`, Erzeugnisse des vorigen Baus werden entfernt); `build/doc/16-agentenanweisung.md`; `clients/openai-codex/manifest.json` (Notiz: Prüfung 88 statt 86); `build/doc/00-kopf.md`, `26-qs-test.md`; `VERSION`, `CHANGELOG.md`, `docs/ROADMAP.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Installationswerkzeug und Prüfapparat |
| Art | **Korrektur.** Patch-Release nach `RELEASE_PROCESS.md` Abschnitt 1: kein Overlay-Feld berührt, keine neue Regel, **keine neue Prüfung** – vier neue Sondeneinheiten, davon drei an einer Auskunft, die bis dahin keine hatte |
| Dringlichkeit | Regulär; gefunden beim Heben auf `1.4.1` |
| Status | 🟢 **entschieden am 2026-09-24** (E1 bis E4), umgesetzt mit `1.4.2` |

---

## 1. Anlaß

Beim Heben der beiden übernehmenden Projekte auf `1.4.1` gab die Auskunft aus D-349 im
Pilotprojekt Pfade der Form `".koolie/core/build/doc/03-ziele-nichtziele.md/r"` aus –
mit Anführungszeichen und einem `/r` am Ende. Der Befund ist in `1.4.1` benannt und
**nicht** behoben worden.

## 2. Die Gegenprüfung

### 2.1 Der Befund selbst – gemessen, nicht erschlossen

`ignorierte_kerndateien()` übergab die Pfade mit `text=True` an
`git check-ignore --stdin`. Unter Windows schreibt Python dabei `\r\n`; git bekommt jeden
Pfad mit angehängtem `\r`, vergleicht ihn **so** gegen die Muster und gibt ihn gequotet
zurück (`"…md\r"`); `replace("\\", "/")` macht aus dem Escape das `/r`.

**Wegwerf-Repositorium, drei Dateien unter `.koolie/core/`, `.gitignore` mit `*.md`:**

| Messung | Ergebnis |
|---|---|
| `git check-ignore` direkt | **2** ignorierte Dateien |
| `ignorierte_kerndateien()` aus `1.4.1` | 🔴 **0** |
| dieselbe, dazu eine dritte `.md`-Datei mit U-Umlaut im Namen | 🔴 **1 von 3, verfälscht** – der letzte Pfad der Eingabe, dem kein Zeilenende folgt; `text=True` schrieb ihn in `cp1252`, und zurück kam `".koolie/core/docs//334bersicht.md"` |

➡️ Ein Verzeichnismuster (`build/`) trifft trotzdem, weil es am Elternverzeichnis greift –
**das war der Anlaßfall von `K-117`, und deshalb fiel es niemandem auf.** Ein Dateimuster
trifft nie. 🔴 **Die Auskunft hatte keine Sonde**: Sie ist keine Prüfung, und die
Sondenpflicht aus D-23 hat sie deshalb nicht erreicht.

### 2.2 🔴 Die zweite Stelle in derselben Richtung

Gesucht nach der Lehre aus `0.57.0` (*zwei Stellen, die einander decken*): Wo liest der
Kern sonst eine Pfadliste von git als Text? **Zwei Hilfsfunktionen des Validators**,
`_verfolgte_dateien()` (Prüfungen 45 und 78) und `_p75_verfolgt()` (Prüfungen 75 und 81),
lesen `git ls-files` zeilenweise. Ohne `-z` quotet git jeden Pfad mit Nicht-ASCII-Zeichen
(`core.quotePath`, Vorgabe an): aus einem U-Umlaut wird `"docs/\303\234bersicht.md"`.

| Prüfung | Was sie mit dem gequoteten Pfad tat |
|---|---|
| 81 | fand unter dem Namen keine Datei – `if not os.path.isfile(pfad): continue`, **leise** |
| 75 | sah die Endung `.md"` statt `.md` und übersprang die Datei als Nicht-Text, **leise** |
| 78 | zählte die Datei, aber **nicht als Markdown** |
| 45 | unberührt – sie sucht `__pycache__` im Pfad, und das Quoting läßt ihn stehen |

**Gegenbeweis, gemessen:** Arbeitsbaumkopie, `git init`, ein Träger
`Übersicht-probe.md` mit einer eingeschleppten LF-Zeile. **Validator aus `1.4.1`: 0
Treffer auf `mischt CRLF- und LF-Zeilen`; neuer Validator: 1.**

Heute trägt keiner der drei gezählten Bestände einen solchen Pfad (Quellrepositorium 535
verfolgte Dateien, Pilot 622, Übungsrepositorium 719 – je **0** mit Nicht-ASCII-Zeichen).
⚠️ **Das ist kein Entlastungsgrund:** Ein übernehmendes Projekt in deutscher Sprache legt
den ersten solchen Namen an, ohne daß es jemand merkt – und genau dann schweigt die
Prüfung.

### 2.3 🔴 Ein Befund des Verfahrens: Das Hauptdokument war für `openai-codex` nicht baubar

Gefunden beim Schritt 3 aus `RELEASE_PROCESS.md` Abschnitt 4.1 (Hauptdokument und
Word-Fassung **je Client Pack**), der in `1.4.1` ausgelassen war – **und für das mit
`1.4.0` gekommene dritte Pack nie gelaufen ist:**

```
FEHLER: eingebettete Datei fehlt (Referenzinstallation openai-codex): AGENTS.override.md.example
```

Kapitel 16 bettet `<ROOT_INSTRUCTION_LOCAL>.example` für jedes Pack ein. `openai-codex`
liefert die Vorlage **bewusst nicht** aus: Die Datei an dieser Stelle verdrängt die
Wurzel-Anweisung (D-341). Die Entscheidung stand im Pack – das Kapitel kannte sie nicht.

🔴 **Und der abgebrochene Bau hat ein falsches Erzeugnis hinterlassen.** `assemble.py`
brach ab, ohne `hauptdokument.md` und `referenzclient.txt` des vorigen Laufs zu entfernen;
`build-docx.py` setzte daraus die Word-Fassung **des vorigen Packs** ein zweites Mal
zusammen und meldete Erfolg. ➡️ *Ein Werkzeug, das nach einem Abbruch das Erzeugnis von
vorhin stehen läßt, liefert eine Erfolgsmeldung für den falschen Gegenstand.*

⚠️ **Nachbarfund:** Die Notiz zu den Laufzeit-Platzhaltern im Manifest von `openai-codex`
nannte **Prüfung 86** als die, die `AGENTS.override.md` im Projekt meldet. Es ist
**Prüfung 88**; 86 prüft die Sperrform des Hooks.

---

## 3. Vorlage zur Entscheidung

| # | Frage | Wege und ihre Preise |
|---|---|---|
| **E1** | **Wie wird die Auskunft berichtigt?** | **`git check-ignore -z --stdin`, Eingabe als UTF-8-Bytes, NUL-getrennt; die Ausgabe ebenso gelesen.** Hebt das `\r` **und** das Quoting auf. **Verworfen:** nur das `\r` abschneiden – das Quoting bliebe, und es trifft jeden Arbeitsplatz. **Verworfen:** `core.quotePath=false` für den Aufruf – Pfade mit Zeilenumbruch oder Anführungszeichen blieben mehrdeutig. ⚠️ **Preis:** keiner, den ein Projekt merkt; die Auskunft meldet nur mehr, wo sie bisher zu wenig meldete |
| **E2** | **Werden die Prüfungen 45, 75, 78 und 81 im selben Release berichtigt?** | **Ja** – dieselbe Ursache, dieselbe Abhilfe (`git ls-files -z`), eine gemeinsame Hilfsfunktion `_git_pfade()`. **Verworfen: ein eigener Posten.** Ein bekannter leiser Fehler in einer Prüfung wiegt schwerer als eine Sondeneinheit mehr. ⚠️ **Preis:** Eine Prüfung kann nach dem Heben in einem Projekt **neu melden** – dann, wenn dort ein Träger mit Nicht-ASCII-Namen schon abweicht. Das ist der Befund, nicht der Preis |
| **E3** | **Wirkungsnachweis** | **Bündel `sonden_ignorierte_kerndateien`** an einer echten Installation mit `git init`, drei Einheiten, **jede gegen einen `os.walk` über den Kern gezählt, nicht gegen eine gepflegte Zahl:** Sonde `D349` (`*.md`), Gegenprobe `D349a` (`build/`, der Anlaßfall), Gegenprobe `D349b` (ein Muster, das nichts trifft: kein Hinweis). Dazu **Sonde 81e** im Bündel zu Prüfung 81. **Gegen den Vorstand fallen `D349` und `81e`** |
| **E4** | **Wie wird Kapitel 16 für ein Pack ohne Ergänzungsdatei gebaut?** | **Eine Direktive `{{LOKALE-ERGAENZUNG}}`, deren Weiche das Manifestfeld `root_instruction_override` ist:** ohne das Feld der bisherige Satz samt Einbettung – und eine fehlende Datei bricht den Bau **weiter** ab –, mit dem Feld eine Erklärung, weshalb es die Datei nicht gibt. Dazu entfernt `assemble.py` vor dem Bau die Erzeugnisse des vorigen Laufs. **Verworfen:** eine Einbettung, die bei jedem Fehlen still eine Erklärung einsetzt – die Ausnahme, die alles ausnimmt. **Wirkungsnachweis:** Alle drei Fassungen gebaut; `claude-code` und `devin-desktop` **zeichengleich** zum Bau vor dem Eingriff (2.085.504 und 2.081.833 Zeichen), `openai-codex` 2.073.255 Zeichen mit der Erklärung genau einmal. ⚠️ **Keine Sonde:** Der Bau braucht `pandoc` und `mmdc`, und keine Prüfung fährt ihn – die Grenze, die Schritt 3 von Hand schließt |

> **Empfehlung der Vorbereitung:** E1 bis E4 wie vorgelegt. Keine neue Prüfung – die
> Auskunft bleibt eine Auskunft (D-349), die Prüfungen behalten ihren Gegenstand.

**Mit aufgenommen, ohne Änderung am Bestand:** Zwei Fragen des Owners vom 2026-09-24
stehen seither als Klärungspunkte im Decision Log – **`K-120`** (Overlay-Werte an einem
Ort, `--update` rendert Laufzeitfassung und Berechtigungsdatei; vor `1.5.0` einzuordnen)
und **`K-121`** (die Schreibrückfrage bei `devin-desktop` als Overlay-Wert).

---

## 4. Umsetzung

1. `install.py`: `ignorierte_kerndateien()` mit `-z`, Ein- und Ausgabe als Bytes.
2. `validate-framework.py`: `_verfolgte_dateien()` und `_p75_verfolgt()` rufen
   `git ls-files -z`; beide geben ihre Ausgabe an die neue `_git_pfade()`.
3. `probe-pruefungen.py`: Bündel `sonden_ignorierte_kerndateien` hinter dem Bündel zu
   D-46; Sonde 81e zwischen 81b und 81d; die Einheitenzahl im Kopf des Bündels zu
   Prüfung 81 berichtigt (*„VIER"* – es waren seit `1.4.1` sechs, jetzt sieben).
4. `DECISION_LOG.md`: **D-352**, **K-120**, **K-121**.
5. `build/assemble.py`: Direktive `{{LOKALE-ERGAENZUNG}}` und das Entfernen der
   Erzeugnisse des vorigen Baus; Kapitel 16 auf die Direktive umgestellt; die Notiz im
   Manifest von `openai-codex` nennt Prüfung 88. Hauptdokument und Word-Fassung für alle
   **drei** Packs gebaut.
6. `VERSION` `1.4.2`, Changelog, Roadmap, Dokumentkopf; beide übernehmenden Projekte auf
   `1.4.2` gehoben und dort committet.

## 5. Abnahme

Steht im Protokoll `tests/protocols/2026-09-24-pfadlisten-nul-getrennt.md`.

## 6. Entscheidung

**E1 bis E4 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-24; der Owner hat
vorab erklärt, den Empfehlungen der Vorbereitung zu folgen). Decision Record **D-352**.
Alle vier zählbaren Kriterien von D-11 bleiben **0**; kein Overlay-Feld berührt.
