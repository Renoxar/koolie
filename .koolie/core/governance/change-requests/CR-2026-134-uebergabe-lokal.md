# Änderungsantrag `CR-2026-134`

| Feld | Inhalt |
|---|---|
| Titel | Die Übergabe wird ein lokales Arbeitsdokument – und vier Prüfungen verlieren den Anker, an dem sie das Quellrepositorium erkannten |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-24 |
| Betroffene Artefakte | `.gitignore`; `UEBERGABE.md` und `UEBERGABE.local.md.example` (aus dem Versionierten genommen); `.koolie/QUELLREPOSITORIUM.md` (**neu**); `tests/scripts/validate-framework.py` (Prüfung 67 entfällt, 78 verliert einen Gegenstand, 75/78/79/81 am Kennzeichen); `tests/scripts/probe-pruefungen.py` (67a–d, 78d/78e entfallen; **81d** und **Gegenprobe 81b** neu; 82b umgestellt); `tests/TEST_CATALOG.md`; `governance/DECISION_LOG.md` (**D-350**, **D-351**; D-214 und D-216 aufgehoben); `governance/FRAMEWORK_DEV_PROFILE.md` (Schritt 7, `0.1.3`); `governance/RELEASE_PROCESS.md` (Abschnitt 4.1, `0.3.1`); `governance/ADOPTION_REGISTRY.md` (`0.2.1`); `docs/ADOPTION_GUIDE.md` (`0.4.5`); `README.md`; `build/doc/00-kopf.md`, `26-qs-test.md`; `VERSION`, `CHANGELOG.md`, `docs/ROADMAP.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Prüfapparat und Änderungsprozess des Quellrepositoriums; dazu eine Korrektur an zwei Übernahmetexten |
| Art | **Korrektur.** Patch-Release nach `RELEASE_PROCESS.md` Abschnitt 1: kein Overlay-Feld berührt, keine neue Regel, **keine neue Prüfung** – zwei neue Sondeneinheiten an einer bestehenden |
| Dringlichkeit | Regulär; Anlaß ist eine Entscheidung des Owners, nicht ein Vorfall |
| Status | 🟢 **entschieden am 2026-09-24** (E1 bis E4), umgesetzt mit `1.4.1` |

---

## 1. Anlaß

**Der Framework Owner hat am 2026-09-24 entschieden, daß die Übergabe nicht mehr
eingecheckt wird** – sie und ihre Vorlage sollen nur noch lokal vorliegen. Die Begründung
ist inhaltlich: Die Übergabe ist Arbeitswissen eines Arbeitsplatzes, **kein Bestandteil
des Frameworks.** Dass Prüfungen an ihr hingen, stand in keinem Träger, den man vor dieser
Frage liest.

Dazu kommt ein Auftrag, der mit derselben Sitzung kam: **Die Wurzel-README an den Stand
von `1.4.0` angleichen.**

## 2. Die Gegenprüfung – was am Austragen hängt

**Gemessen, bevor eine Zeile geändert wurde** (`grep` über Validator und Sondenapparat):

| Stelle | Wie sie die Übergabe nutzt | Folge des bloßen Austragens |
|---|---|---|
| **Prüfung 67** | prüft Titelzeile, Lagezeilen und Antragsnummern der Übergabe | ihr Gegenstand fehlt in jeder frischen Auscheckung |
| **Prüfung 78**, Gegenstand 4 | hält die Abnahmezeile der Übergabe gegen das Register | ebenso |
| **Prüfung 78**, Enthaltung | enthält sich ganz, wenn die Übergabe fehlt | im Klon: enthält sich **leise** |
| **Prüfung 79** | prüft die Wurzel-Lizenz nur, wenn die Übergabe da ist | im Klon: prüft **leise** nur die Kernfassung |
| 🔴 **Prüfung 75** | zählt alle verfolgten Träger, wenn die Übergabe **verfolgt** ist, sonst nur das Ausgelieferte | **sofort**, auch hier: prüft **leise** nur noch das Ausgelieferte |
| 🔴 **Prüfung 81** | ebenso | ebenso |

🔴 **Die letzten beiden Zeilen sind der Befund.** Die Prüfungen 75 und 81 lesen
`git ls-files`. Nach dem Austragen hätten sie das Quellrepositorium **auf dem
Arbeitsplatz, der die Datei noch führt**, für ein übernehmendes Projekt gehalten. Keine
Meldung, keine Warnung: Der Validator wäre grün gelaufen und hätte weniger geprüft.
➡️ ***Ein Anker, der nur an einem Arbeitsplatz liegt, ist keiner.***

**Gegenbeweis, gemessen:** Eine Kopie des Bestands mit ausgetragener Übergabe (lokal
vorhanden), `README.md` auf LF gestellt. **Der Validator aus `1.4.0` meldet sie nicht (0
Treffer), der neue meldet sie (1 Treffer).**

### 2.1 Der zweite Auftrag: drei Aussagen der Wurzel-README, die `1.4.0` überholt hat

| Stelle | Aussage | Stand |
|---|---|---|
| Einleitung | *„derzeit `devin-desktop` und `claude-code`"* | 🔴 drei Packs seit `1.4.0` |
| Hinweis unter dem Baum | *„Eine eigene Hook-Datei gibt es nicht. Bei beiden ausgelieferten Packs …"* | 🔴 `openai-codex` liest Hooks **nur** aus `.codex/hooks.json` |
| `install.py`-Tabelle und Hinweis | Hook-Konfiguration gehört dem Projekt und wird von `--update` nicht erneuert | 🔴 bei `openai-codex` gehört die Hook-Datei zum **Kern** und wird erneuert – mit Folge für das Hook-Vertrauen |
| Absatz zu `root-template/` | *„`seed_paths` ist in beiden Manifesten leer"* | ⚠️ in allen **drei** |

🔴 **Und ein Nachbarfund, der schwerer wiegt als alle vier:** Der Kopierbefehl in der
README und zweimal im Übernahmeleitfaden lautete `cp -r .koolie/core/ /pfad/zum/projekt/`.
Mit dem Schrägstrich am Quellpfad legt `cp` den **Inhalt** ab: Der Kern landet unter
`<projekt>/core`, nicht unter `<projekt>/.koolie/core`, und `install.py` findet sich
danach nicht dort, wo die nächste Zeile es aufruft. **Der erste Befehl der Anleitung
funktionierte nicht.** Gefunden beim Lesen, nicht durch eine Prüfung.

⚠️ **Zweiter Nachbarfund:** Der Kopf des Hauptdokuments (`build/doc/00-kopf.md`) sagte
*„Ausgeliefert werden zwei: `devin-desktop` und `claude-code`."* Prüfung 77 hält dort die
**Version**, nicht den Inhalt – die Grenze, die sie selbst benennt.

⚠️ **Dritter Nachbarfund:** `governance/ADOPTION_REGISTRY.md` führte die
**Overlay-Versionen** `0.3.3` und `1.1.0`; die Projekte tragen seit `1.3.0` `0.3.5` und
`1.3.0`. Prüfung 82 hält nur die Spalte `Framework-Version` – *eine Spalte, die niemand
zählt, ist eine, die niemand veralten sieht.*

---

## 3. Vorlage zur Entscheidung

| # | Frage | Wege und ihre Preise |
|---|---|---|
| **E1** | **Wird die Übergabe aus dem Versionierten genommen?** | **Ja, samt Vorlage `UEBERGABE.local.md.example`**, per `git rm --cached`; beide stehen in der `.gitignore`. Beilage und Übergabe bleiben **getrennte** Dateien. ⚠️ **Preis:** Ein zweiter Arbeitsplatz bekommt die Übergabe nicht mehr über `git clone` – genau der Anlaß von D-214. Die Git-Historie trägt die Fassungen bis `1.4.0` |
| **E2** | **Was wird aus den Prüfungen 67 und 78 (zweiter Gegenstand)?** | **Ersatzlos streichen** (Entscheidung des Owners). Die Nummer 67 bleibt im Register als *entfallen*, weil Prüfung 40 ein lückenloses Register verlangt und eine neu vergebene Nummer jeden alten Verweis falsch machte. **Verworfen: lokal weiterlaufen lassen** – eine Prüfung, deren Gegenstand eine frische Auscheckung nicht führt, läuft nur an einem Arbeitsplatz. ⚠️ **Preis:** Stand und Zahlen der Übergabe prüft niemand mehr |
| **E3** | **Woran erkennt der Validator künftig das Quellrepositorium?** | **An einer eigenen, versionierten Datei neben dem Kern: `.koolie/QUELLREPOSITORIUM.md`.** Das Heben kopiert nur `.koolie/core/`, `install.py` legt sie nicht an. **Verworfen:** am lokalen Vorhandensein der Übergabe (im Klon prüfte der Validator leise weniger); unter `.koolie/core/` (wanderte in jedes Projekt); eine vorhandene Wurzeldatei wie `README.md` (ein Projekt führt sie auch). **Wirkungsnachweis:** Sonde 81d und Gegenprobe 81b, dazu 82b auf das Kennzeichen umgestellt |
| **E4** | **Die README-Befunde und die Nachbarfunde** | **Berichtigen, alle.** Kein Befund ändert eine Zusage des Frameworks – sie ändern Beschreibungen, die hinter dem Bestand zurückblieben, und einen Befehl, der nicht lief. **Keine neue Prüfung:** Eine Prüfung auf die Aussagen der README ist `K-104`, und dessen Frage bleibt, wo sie steht |

> **Empfehlung der Vorbereitung:** E1 bis E4 wie vorgelegt. Die Entscheidungen E1 bis E3
> hat der Owner am 2026-09-24 im Gespräch getroffen, bevor dieser Antrag geschrieben
> wurde; der Antrag hält sie mit ihren Preisen fest.

---

## 4. Umsetzung

1. `git rm --cached UEBERGABE.md UEBERGABE.local.md.example`; beide in die `.gitignore`.
2. `.koolie/QUELLREPOSITORIUM.md` angelegt; im Validator `QUELLREPO_KENNZEICHEN` und
   `ist_quellrepositorium()`, gelesen von 75 und 81 (versionierter Bestand) sowie 78 und
   79 (Arbeitsbaum).
3. Prüfung 67 und Gegenstand 4 von Prüfung 78 entfernt; Registereintrag 67 als
   *entfallen*; im Sondenapparat 67a–67d, Gegenproben 67a/67b sowie 78d/78e entfernt,
   81d und Gegenprobe 81b neu, 82b auf das Kennzeichen umgestellt. Die Sondenmenge an
   drei Stellen: *„6, 14, 18 bis 66 und 68 bis 88"*.
4. Entwicklungsprofil Schritt 7 und `RELEASE_PROCESS.md` Abschnitt 4.1 auf die lokale
   Übergabe umgeschrieben.
5. README, Übernahmeleitfaden (zwei Kopierbefehle), Dokumentkopf und Bestandsliste
   berichtigt.
6. `VERSION` `1.4.1`, Changelog, Roadmap; beide übernehmenden Projekte auf `1.4.1`
   gehoben – **zugleich der für `1.4.0` verschobene Schritt 2.**

## 5. Abnahme

Steht im Protokoll `tests/protocols/2026-09-24-uebergabe-lokal.md`.

## 6. Entscheidung

**E1 bis E4 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-24). Decision
Records **D-350** und **D-351**; D-214 und D-216 sind aufgehoben. Alle vier zählbaren
Kriterien von D-11 bleiben **0**; kein Overlay-Feld berührt.
