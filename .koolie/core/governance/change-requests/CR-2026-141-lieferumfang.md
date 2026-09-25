# Änderungsantrag `CR-2026-141`

| Feld | Inhalt |
|---|---|
| Titel | Der wählbare Lieferumfang – und die Liste, die sich nicht ableiten ließ |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-25 |
| Betroffene Artefakte | `clientmap.py` (`NACHWEIS_ABLAGEN`, `lieferumfang()`); `install.py` (`--lieferumfang`, `LIEFERUMFANG`, Pfadgrenze); `install_dialog.py`; `tests/scripts/validate-framework.py` (**Prüfung 90**, `HINWEIS`, Prüfungen 12, 76, 77, 80); `tests/scripts/probe-pruefungen.py` (Bündel `sonden_lieferumfang`, Sonden `90`, `90a`, `T362`); `tests/TEST_CATALOG.md`; `docs/ADOPTION_GUIDE.md`, `README.md`; `governance/RELEASE_PROCESS.md` (Schritte 5 und 6); `docs/ROADMAP.md`; `governance/DECISION_LOG.md` (**D-367** bis **D-370**, `K-75`, `K-122`); `governance/ADOPTION_REGISTRY.md`; `build/doc/00-kopf.md`, `15-referenzstruktur.md`, `26-qs-test.md`, `31-anhaenge.md`; `VERSION`, `CHANGELOG.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Installationswerkzeug, Auslieferbestand, Prüfapparat |
| Art | **MINOR** nach `RELEASE_PROCESS.md` Abschnitt 1: neue Wahl beim Übernehmen, neue Prüfung, neue Ausgabeform; der Standard bleibt der bisherige Umfang, kein Overlay-Feld geändert |
| Dringlichkeit | Posten `1.8.0` nach D-366 |
| Status | 🟢 **entschieden am 2026-09-25** (E1 bis E10), umgesetzt mit `1.8.0` |

---

## 1. Anlaß

`K-75` fragt seit `0.72.0`, was ins **Mindestpaket** gehört und womit ein Projekt mit
reduziertem Umfang seine Übernahme prüft. `1.7.0` hat den Lieferumfang aus dem Posten des
Installers gelöst (D-366): Hooks und Validator liegen unter `tests/scripts/`, der Schnitt
*„ohne `tests/`“* bräche jede Installation, und **die Liste gehört abgeleitet, nicht
aufgezählt** – sonst fehlt nach dem ersten neuen Träger einer.

## 2. Die Gegenprüfung

Gemessen am 2026-09-25 an sechs frischen Installationen (drei Packs, je ohne und mit
Muster `general`), außerhalb des Repositoriums.

### 2.1 🔴 Die Lesespur taugt nicht

Jede Datei, die Installer und Validator im Projekt öffnen, protokolliert über einen
Audit-Hook: **549 von 549** Kerndateien. Der Validator prüft Inhalte über den ganzen Baum.
*Was gelesen wird, ist nicht, was nötig ist.*

### 2.2 🔴 Die Verweishülle taugt nicht

Transitiv über die Verweisauswertung von Prüfung 12 (Markdown-Links und Framework-Pfade in
Backticks), ausgehend von den installierten Trägern: mit Verzeichnisverweisen **548 von
548**. Ohne Verzeichnisverweise bleiben **39 Protokolle, 5 Anträge und 6 Träger aus
`build/`** in der Hülle – und es fallen **die Skillquellen, die Laufzeitschicht und
`templates/project-overlay/`** heraus, ohne die `install.py --update` nicht läuft. Zu groß
und zu klein zugleich.

### 2.3 🟢 Der Validator ist das Orakel

Aus einer Kopie der Installation die vier Ablagen der Nachweisschicht entfernt –
`governance/change-requests`, `tests/protocols`, `tests/erhebungen`, `build`, zusammen
**350 von 550 Dateien, rund 47 % der Bytes** – und die Validatorausgabe gegen die volle
Installation gehalten. **In allen drei Packs gleich:**

| Neu gegenüber voll | Anzahl | Woher |
|---|---|---|
| *„Pfadangabe existiert nicht“*, Ziel `tests/protocols/` | **70** (33 verschiedene Ziele) | `TEST_CATALOG` 22, Skillquellen 17, installierte Skills 14, `framework/core` 5, `EDGE_CASES` 4, übrige 8 |
| Prüfung ohne Gegenstand | **3** | 76 (`tests/erhebungen/ablage.py`), 77 (`build/doc/00-kopf.md`), 80 (`tests/protocols/`) |
| sonst | **0** | – |

Die 70 Verweise sind **Herkunftsangaben**: Die Aussage des verweisenden Trägers steht ohne
die Datei. Sonst hängt kein Werkzeug an der Nachweisschicht.

### 2.4 Nebenbefund: die Windows-Pfadgrenze

Die erste Messung legte die Projekte im Ablagebereich der Sitzung an. `--target` brach beim
Kopieren ab: `…\core.koolie-neu\framework\role-packs\requirements-engineering\runtime\30-role-requirements-engineering.md`
riß die Grenze von 259 Zeichen. Der Rückbau hielt, **die Meldung fragte, ob eine Datei
geöffnet sei.** Längster Kernpfad 102 Zeichen; ab 146 Zeichen Projektpfad scheitert es.

### 2.5 Nebenbefund: der Dateimodus des Archivs

Beim Nachzählen von `koolie-1.7.0.tar.gz`: `install.command` mit `0775`, jede Datei `0664` –
gits Voreinstellung `tar.umask=0002`. Mit `-c tar.umask=022`: `0755` und `0644`, zweimal
bytegleich. Das Archiv ist vor der Veröffentlichung so neu erzeugt worden.

## 3. Vorlage zur Entscheidung

Vorgelegt am 2026-09-25 als Fragen (a) bis (j), angenommen mit *„Passt“*.

| # | Frage | Wege und ihre Preise |
|---|---|---|
| **E1** | **Wie wird die Liste abgeleitet?** (a) | **Umgekehrt: aufgezählt ist die Nachweisschicht, geschlossen nach Ablageort, an einer Stelle** (`clientmap.NACHWEIS_ABLAGEN`); `nutzung` ist der Kern ohne sie. Ob die Nutzung auskommt, entscheidet der Validator (2.3), gehalten von einer Sonde. **Verworfen:** Lesespur (2.1), Verweishülle (2.2), Kennzeichnung je Datei – dieselbe Aufzählung, verteilt über 550 Träger |
| **E2** | **Die 70 Verweise** (b) | **Herkunftsangaben:** In einer reduzierten Installation meldet Prüfung 12 sie nicht, sondern zählt sie in einer `HINWEIS`-Zeile; im Quellrepositorium bleibt sie streng. **Verworfen:** auf Kennungen umschreiben – 70 Eingriffe in Belege; zitierte Protokolle mitliefern – wieder eine Liste |
| **E3** | **Die Prüfungen 76, 77 und 80** (c) | **Prüfen nur das Gelieferte, mit je einer `HINWEIS`-Zeile.** Still übersprungen wäre die Bauform, die `1.4.0` abgestellt hat (D-346). Dazu die **Ausgabeform `HINWEIS`**, die weder Fehler noch Warnung ist; eine volle Installation trägt keine |
| **E4** | **Wo steht die Wahl?** (d) | **`.koolie/core/LIEFERUMFANG`** neben `VERSION`, geschrieben bei jedem `--target`; ohne Datei gilt `voll`. Das Heben übernimmt sie, gewechselt wird nur ausdrücklich; eine reduzierte Quelle liefert keinen vollen Kern. **Prüfung 90** hält die Angabe gegen den Bestand. **Verworfen:** die Wahl am Zustand erkennen – täuschbar |
| **E5** | **Standard und Bedienung** (e), (f) | **`voll` bleibt Standard**; `--lieferumfang voll` oder `nutzung`, **nur mit `--target`**; der Dialog fragt bei der Erstinstallation, beim Heben nennt er den bisherigen Umfang |
| **E6** | **Große Einzelträger** (g) | **Nicht in `1.8.0`** – `CHANGELOG.md`, `DECISION_LOG.md`, `ROADMAP.md`, Sondenskript, zusammen rund 26 % der Bytes, wären eine Aufzählung einzelner Dateien. Offen als **`K-122`** |
| **E7** | **Archive** (h) | **Eines, voll.** Reduziert wird beim Installieren |
| **E8** | **Pfadgrenze** (i) | **Vorprüfung in `install.py`** gegen das längere Zwischenverzeichnis, mit Pfad, Länge und Überschuß; Sonde `T368` |
| **E9** | **Dateimodus des Archivs** (j) | **`-c tar.umask=022` in Schritt 5**, der Modus als Gegenstand von Schritt 6 |
| **E10** | **Qualitätssicherungsrelease** (Frage des Owners während des Baus) | **`1.9.0`, direkt nach `1.8.0`:** Nach `1.8.0` ist kein grundsätzlicher Posten geplant; `K-67` hat kein Ziel-Release. Beginnt mit einem Vorbedingungsdurchgang, der Dokumentliste und Kriterien festlegt |

> **Empfehlung der Vorbereitung:** E1 bis E10 wie vorgelegt.

---

## 4. Umsetzung

1. `clientmap.py`: `LIEFERUMFANG_DATEI`, `LIEFERUMFAENGE`, `NACHWEIS_ABLAGEN`,
   `ist_nachweis()`, `lieferumfang()`.
2. `install.py`: `--lieferumfang` (nur mit `--target`), Umfang aus Angabe, bisheriger Datei
   oder `voll`; Filter der Nachweisschicht; `LIEFERUMFANG` ins Zwischenverzeichnis;
   Verweigerung bei reduzierter Quelle; Zeile *„Umfang:“* samt Wechsel; Vorprüfung der
   Pfadgrenze (`PFAD_GRENZE_DATEI`, `PFAD_GRENZE_VERZEICHNIS`).
3. `install_dialog.py`: Frage nach dem Umfang bei der Erstinstallation.
4. Validator: `HINWEISE`/`hinweis()`, `reduziert()`, `nicht_geliefert()`; Prüfung 12
   (Herkunftsangaben), 76, 77, 80 (nur Geliefertes); **Prüfung 90**; `LIEFERUMFANG` als
   Verweisziel im Quellrepositorium; Register und Sondenmenge bis 90.
5. Sonden: Bündel `sonden_lieferumfang` (`L367` bis `L367e`, `90b`, `90c`, `T368`), Sonden
   `90`, `90a`; `T362` erwartet `LIEFERUMFANG`, `T362g` die neue Frage.
6. Leitfaden, README, Release-Prozess (Schritte 5 und 6, dazu die Schrittnummern einer
   Begründung berichtigt), Roadmap (Standüberschrift, `1.8.0`, Planabschnitt `1.9.0`),
   Decision Log, Bestandsliste, Kapitel 00, 15, 26, 31, `VERSION`, Changelog.
7. Beide Projekte heben – mit `--target --update`, **voll** wie bisher.

## 5. Abnahme

Steht im Protokoll `tests/protocols/2026-09-25-lieferumfang.md`.

## 6. Entscheidung

**E1 bis E10 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-25; (a) bis (j) vor
dem Bau vorgelegt und angenommen, E10 als Frage des Owners während des Baus – der Owner
hat vorab erklärt, den Empfehlungen der Vorbereitung zu folgen). Decision Records
**D-367** bis **D-370**; `K-75` beantwortet, `K-122` neu. Alle vier zählbaren Kriterien
von D-11 bleiben **0**.
