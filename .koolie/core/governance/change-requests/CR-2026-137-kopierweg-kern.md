# Änderungsantrag `CR-2026-137`

| Feld | Inhalt |
|---|---|
| Titel | Der Kopierweg des Kerns – und das Archiv, aus dem er als sicher galt |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-24 |
| Betroffene Artefakte | `README.md` (Wurzel, Warnsatz am Kopierbefehl); `docs/ADOPTION_GUIDE.md` `0.4.6` (Warnsatz in Abschnitt 2 Schritt 2, Abschnitt 3 Schritt 2, Abschnitt 4); `.koolie/QUELLREPOSITORIUM.md` (Absatz *„Sie wandert nicht in ein Projekt“*); `install.py` (neu `traegt_quellrepo_kennzeichen()` und die Auskunft am Ende des Laufs); `tests/scripts/probe-pruefungen.py` (Bündel `sonden_kennzeichen_im_projekt` **neu**: Sonde `D354`, Gegenprobe `D354a`); `governance/DECISION_LOG.md` (**D-354**); `governance/ADOPTION_REGISTRY.md`; `build/doc/00-kopf.md`, `26-qs-test.md`; `VERSION`, `CHANGELOG.md`, `docs/ROADMAP.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Übernahmeanleitung und Installationswerkzeug |
| Art | **Korrektur.** Patch-Release nach `RELEASE_PROCESS.md` Abschnitt 1: kein Overlay-Feld berührt, keine neue Regel, **keine neue Prüfung** – eine Auskunft (Bauform von D-349) mit zwei Sondeneinheiten |
| Dringlichkeit | Regulär; zwei Fragen des Owners vom 2026-09-24 zu `.koolie/QUELLREPOSITORIUM.md` |
| Status | 🟢 **entschieden am 2026-09-24** (E1 bis E3), umgesetzt mit `1.4.4` |

---

## 1. Anlaß

Der Owner hat am 2026-09-24 zwei Fragen zum Kennzeichen des Quellrepositoriums gestellt
(D-351):

- **(a)** Braucht die Übernahmeanleitung einen Warnsatz, daß nur `.koolie/core/` und nie
  ganz `.koolie/` kopiert wird?
- **(b)** Soll `install.py` melden, wenn es im Ziel `.koolie/QUELLREPOSITORIUM.md` findet?

Beide Anleitungen nennen seit `1.4.1` den richtigen Befehl (`cp -r .koolie/core
<projekt>/.koolie/`). Ob ein Leser, der das Verzeichnis `.koolie/` vor sich sieht, es
**ganz** kopiert, sagt keine von beiden.

## 2. Die Gegenprüfung

### 2.1 🔴 Die Annahme der Vorbereitung war falsch: Auch das Release-Archiv trägt das Kennzeichen

Die Vorbereitung ging davon aus, eine Kopie von ganz `.koolie/` sei nur aus dem
**Arbeitsbaum** gefährlich – dort liegt neben dem Kern das eigene, nicht versionierte
Overlay des Frameworks (`.koolie/project-overlay/`, `.gitignore` Zeile 36) –, aus dem
Release-Archiv dagegen harmlos. **Gemessen:**

| Quelle | `.koolie/QUELLREPOSITORIUM.md` | `.koolie/project-overlay/` |
|---|---|---|
| Release-Archiv `koolie-1.4.3.tar.gz` | 🔴 **enthalten** – die Datei ist versioniert, `git archive` nimmt sie mit | nicht enthalten |
| Arbeitsbaum des Frameworks | enthalten | 🔴 **enthalten**, 18 Dateien |

➡️ **Keine der beiden Quellen ist für eine Kopie von ganz `.koolie/` sicher.** Die
Anleitung, die nur aus einer Quelle harmlos wäre, gibt es nicht – beide sind eine Falle.

### 2.2 Was das Kennzeichen in einem Projekt bewirkt

Wegwerf-Installation: leeres Repositorium, Kern aus dem Arbeitsbaum über `git ls-files`
(der Weg aus `RELEASE_PROCESS.md` 4.1 Schritt 2), `install.py --client claude-code`,
committet, `__pycache__/` ignoriert. Validator ohne `--strict-overlay`:

| Lauf | Ergebnis | Was meldet |
|---|---|---|
| A – ohne Kennzeichen | **0 Fehler, 0 Warnungen** | – |
| B – Kennzeichen kopiert, nicht verfolgt | 🔴 **1 Fehler** | Prüfung 79: `LICENSE: fehlt` in der Projektwurzel |
| C – Kennzeichen committet | 🔴 **80 Fehler** | Prüfung 79 wie in B, dazu Prüfung 81 an **79** Projektträgern (Zeilenenden gegen die Mehrheit aller versionierten Träger) |

🔴 **Keine der Meldungen nennt die Ursache.** Wer `LICENSE: fehlt` liest, legt eine
Lizenz in die Projektwurzel – und hat danach ein Projekt, das dauerhaft als
Framework-Repositorium geprüft wird. Die Prüfungen 75 und 78 melden in dieser
Installation nichts, laufen aber ebenfalls im falschen Zweig.

`install.py` meldet heute **nichts**: Die Datei kommt in keiner Zeile des Werkzeugs vor.

### 2.3 🔴 Was die Kopie aus dem Arbeitsbaum beim Heben bewirkt

Dieselbe Installation, in `OVERLAY.md` eine Projektmarke angehängt und committet; dann
`cp -r <framework>/.koolie .` und `install.py --update`:

| Messung | Ergebnis |
|---|---|
| Projektmarke in `OVERLAY.md` | 🔴 **weg** – `OVERLAY.md` und `overlay-manifest.yaml` sind die des Frameworks |
| `install.py --update` | Exit 0; das Overlay steht in der Liste *„Projektdateien unberührt gelassen“* |
| Kennzeichen | liegt unverfolgt im Projekt |

➡️ ***Ein Werkzeug, das einen Pfad nie schreibt, kann nicht melden, was ein anderer
Schritt dort geschrieben hat.*** Die Aussage *„`install.py` überschreibt
`.koolie/project-overlay/` nie“* im Übernahmeleitfaden (Abschnitt 4) ist wahr – und
genau deshalb beruhigt sie an der falschen Stelle: Überschrieben hat der Kopierbefehl
davor. Das ist die *Zusage, die mehr verspricht als ihr Mechanismus hält*, an einem
Satz, der für sich richtig ist.

### 2.4 Warum ein Abbruch nicht baubar ist

Das Framework-Repositorium erzeugt seine eigenen Wurzeldateien mit `install.py`
(`.gitignore`: *„Im Framework-Repository sind die Wurzelbestandteile Erzeugnisse“*) und
trägt das Kennzeichen. Gesucht nach einem Merkmal, das beide Fälle trennt:

| Merkmal | trennt? |
|---|---|
| Kennzeichen vorhanden | nein – beide |
| git verfolgt das Kennzeichen | 🔴 **nein** – ein Projekt, das die Kopie committet hat, sieht genauso aus; und gerade dort meldet Prüfung 81 am meisten |
| Lage von `install.py` | nein – in beiden `<root>/.koolie/core/install.py` |

---

## 3. Vorlage zur Entscheidung

| # | Frage | Wege und ihre Preise |
|---|---|---|
| **E1** | **Warnsatz an den Kopierbefehlen?** | **Ja, an allen drei Stellen des Übernahmeleitfadens und in der Wurzel-README:** Neuaufnahme (Abschnitt 2 Schritt 2), Aktualisierung (Abschnitt 3 Schritt 2 – dort steht kein Befehl, aber *„ersetzen“*), mehrere Repositories (Abschnitt 4, dort mit der Einschränkung des Satzes über `install.py`). Der Satz nennt **beide** Quellen und **beide** Folgen. Dazu der Absatz *„Sie wandert nicht in ein Projekt“* im Kennzeichen selbst. ⚠️ **Preis:** Ein Warnsatz erreicht nur, wer liest – deshalb E2 |
| **E2** | **Auskunft oder Abbruch in `install.py`?** | **Auskunft** (Bauform von D-349): am Ende jedes Laufs mit Erstinstallation oder `--update`, solange das Kennzeichen im Ziel liegt; Exit-Code unverändert. Der Text nennt **beide** Fälle – Projekt (Datei entfernen, Overlay prüfen, weil eine Kopie aus dem Arbeitsbaum es ersetzt hat) und Framework-Repositorium (nichts zu tun). **Verworfen: Abbruch** – er träfe das Framework-Repositorium selbst, und kein Merkmal trennt die Fälle (2.4). **Verworfen: Auskunft nur bei unverfolgtem Kennzeichen** – sie schwiege in dem Projekt, das die Kopie schon committet hat. **Verworfen: das Kennzeichen per `export-ignore` aus dem Archiv nehmen** – es änderte den Archivinhalt gegen `git ls-tree` der Marke und hülfe beim Arbeitsbaum nicht. ⚠️ **Preis:** Im Framework-Repositorium steht die Auskunft bei jedem Lauf; ihr Text sagt, daß dort nichts zu tun ist |
| **E3** | **Wirkungsnachweis** | **Bündel `sonden_kennzeichen_im_projekt`** an einer echten Installation: Sonde `D354` (Kennzeichen liegt → Hinweis, Exit 0, **und Prüfung 79 verlangt die Lizenz**) und Gegenprobe `D354a` (ohne Kennzeichen → kein Hinweis, keine Lizenzmeldung). 🔴 **Die Sonde hält zwei Stellen gegeneinander:** `install.py` und der Validator führen den Pfad des Kennzeichens je für sich; wandert eine der beiden Konstanten, fällt sie. **Gegen den Vorstand fällt `D354`** |

**Nicht vorgelegt, benannt:** Die Meldungen der Prüfungen 79 und 81 nennen die Ursache
weiterhin nicht. Sie könnten es – ein Zusatz *„geprüft als Quellrepositorium“* –, aber
das ist ein Eingriff in vier Prüfungen für einen Fall, den jetzt zwei Stellen vorher
abfangen. Ein bereits überschriebenes Overlay erkennt **keine** Stelle; dafür gibt es
die Versionierung des Projekts.

**Verworfen im Gespräch (Vorschlag des Owners, begründet abgelehnt):** das Kennzeichen
in die Wurzel neben `README.md` legen, damit man ganz `.koolie/` kopieren kann. Es löst
das Overlay-Problem nicht, und der Gewinn wäre eine Zeile – `mkdir -p` steht in beiden
Anleitungen schon.

> **Empfehlung der Vorbereitung:** E1 bis E3 wie vorgelegt. Keine neue Prüfung – die
> Auskunft bleibt eine Auskunft (D-349), und der Validator behält seinen Gegenstand.

---

## 4. Umsetzung

1. `README.md` und `docs/ADOPTION_GUIDE.md` (`0.4.5` → `0.4.6`): Warnsatz an den drei
   Stellen; Abschnitt 4 schränkt den Satz über `install.py` ein.
2. `.koolie/QUELLREPOSITORIUM.md`: Wer ganz `.koolie/` kopiert, nimmt es mit – auch aus
   dem Archiv.
3. `install.py`: Konstante `QUELLREPO_KENNZEICHEN`, Funktion
   `traegt_quellrepo_kennzeichen()`, Auskunft hinter der aus D-349.
4. `probe-pruefungen.py`: Bündel `sonden_kennzeichen_im_projekt` hinter dem Bündel zu
   D-349.
5. `DECISION_LOG.md`: **D-354**.
6. `VERSION` `1.4.4`, Changelog, Roadmap, Dokumentkopf, Kapitel 26; beide übernehmenden
   Projekte auf `1.4.4` gehoben und dort committet; Hauptdokument und Word-Fassung für
   alle drei Packs gebaut.

## 5. Abnahme

Steht im Protokoll `tests/protocols/2026-09-24-kopierweg-kern.md`.

## 6. Entscheidung

**E1 bis E3 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-24; der Owner hat
vorab erklärt, den Empfehlungen der Vorbereitung zu folgen). Decision Record **D-354**.
Alle vier zählbaren Kriterien von D-11 bleiben **0**; kein Overlay-Feld berührt.
