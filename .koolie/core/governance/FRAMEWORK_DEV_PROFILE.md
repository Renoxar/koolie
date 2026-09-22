# Entwicklungsprofil des Quellrepositoriums

| Attribut | Wert |
|---|---|
| ID | `FW-GOV-DEV` |
| Version | `0.1.2` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Gilt für | das Quellrepositorium dieses Frameworks – **nicht** für ein Projekt, das ein Release anwendet |
| Entstehung | Befund **B07** des unabhängigen Reviews vom 2026-09-12 (`CR-2026-053`, D-56) |

## 1. Zwei Einsatzkontexte (normativ)

Das Framework wird in zwei verschiedenen Lagen benutzt, und die Regeln der Laufzeitschicht sind
für die erste geschrieben:

| Kontext | Gegenstand der Arbeit | Overlay | Wer setzt die Grenze durch |
|---|---|---|---|
| **Anwendung** | Der Code eines Projekts. Das Framework ist unveränderliches Release | ausgefüllt, Status `aktiv` | Berechtigungsdatei, Schutz-Hook und Regelschicht |
| **Entwicklung** | Das Framework selbst. Es gibt kein Projekt, dessen Code bearbeitet würde | bleibt Vorlage, Status offen | der Änderungsprozess dieses Verzeichnisses |

Bis 0.31.0 war nur der erste Kontext beschrieben. Der zweite entstand dadurch nicht weniger oft –
**jede Sitzung an diesem Framework stand in ihm** –, sondern nur ungeregelt: Die Overlay-Vorlage
bleibt hier absichtlich Vorlage, die Regeln setzen freigegebene Pfade voraus, und die
Analyseskills ließen ein inaktives Overlay nur in Übungsrepositorys zu. Der Einstieg in einen
frischen Auscheckstand verlangte damit Rechte, die niemand erteilt hatte.

## 2. Geltungsbereich (normativ)

1. Dieses Profil gilt in einem Repositorium, das **die Quelle dieses Frameworks ist**: Es führt
   `.koolie/core/VERSION`, `.koolie/core/governance/` und `.koolie/core/framework/core/` unter
   Versionskontrolle, und die Laufzeitschicht ist dort laut `.gitignore` ein **Erzeugnis**.
2. Die Geltung folgt **nicht** aus einem Verzeichnisnamen und **nicht** aus einer Behauptung des
   KI-Clients. Sie folgt aus dem Inhalt des Repositoriums, und sie erteilt **keine technische
   Berechtigung** (Abschnitt 5).
3. **`install.py` schreibt dieses Profil in kein Zielprojekt.** Es liegt unter `governance/`,
   nicht unter `templates/` und nicht unter `framework/runtime/`; `seed_paths` beider Client
   Packs ist leer. 🔴 **Im Zielprojekt liegt es trotzdem, und das ist gemessen** (2026-09-22,
   D-253): `docs/ADOPTION_GUIDE.md` Schritt 2 kopiert `.koolie/core/` als Ganzes, und beide
   übernehmenden Projekte führen es. Bis `0.83.0` stand hier *„wird in kein Zielprojekt
   installiert"* – **der Satz beschrieb das Werkzeug und nicht das Ergebnis.** Er erteilt dort
   keine Geltung: Die folgt nach Abschnitt 2.1 aus dem **Inhalt** des Repositoriums und nicht
   aus der Anwesenheit dieser Datei.

## 3. Lesen (normativ)

1. Der Inhalt dieses Repositoriums ist **K0** nach `.koolie/core/framework/core/02-privacy.md`
   Abschnitt 2: framework-eigene Inhalte ohne Projektbezug. Er ist damit ohne Overlay und ohne
   Einzelfreigabe lesbar.
2. Das gilt ausdrücklich für die Anweisungsquellen selbst – Wurzel-Anweisungsdatei, Regelablage,
   Kernregeltexte, Overlay-Vorlage, Client Packs. **Ihr Schreibschutz ist kein Leseverbot**
   (D-55); beide technischen Schichten machen diese Unterscheidung seit D-30.
3. Die Analyseskills sind hier zulässig, obwohl kein Overlay aktiv ist. Ihre Vorbedingung nennt
   diesen Fall seit 0.32.0 neben dem Übungsrepositorium.
4. **Ausgenommen bleibt, was auch hier K3 ist:** Secret-Dateien, Schlüsselmaterial und alles
   Übrige aus Abschnitt 2.1 des Datenschutzmodells. Eine Datei wird nicht dadurch lesbar, dass sie
   neben einer Regeldatei liegt.

## 4. Ändern (normativ)

Die Reihenfolge ist der Änderungsprozess des Frameworks, nicht ein Betriebsmodus:

1. **Befund** mit Fundstelle (`pfad/datei:zeile`). Ein Befund von außen wird zuerst gegengeprüft
   (D-23) – auch ein Review-Befund.
2. **Änderungsantrag** unter `governance/change-requests/` nach
   `governance/CHANGE_REQUEST_TEMPLATE.md`, mit dem Abschnitt „Vorlage zur Entscheidung“: jede
   Ermessensfrage einzeln, mit Auflösung **und Preis**.
3. **Entscheidung** durch `<FRAMEWORK_OWNER>` in Abschnitt 6 des Antrags; die tragenden
   Entscheidungen zusätzlich als Decision Record in `governance/DECISION_LOG.md`, mit Begründung
   und verworfenen Alternativen.
4. **Umsetzung** mit Wirkungsnachweis nach D-23: je neue Prüfung eine Sonde und eine Gegenprobe in
   `tests/scripts/probe-pruefungen.py`, dazu der Gegenbeweis gegen den Vorstand – die neuen Sonden
   MÜSSEN gegen die Vorversion **fallen**.
5. **Abnahme:** `python .koolie/core/tests/scripts/validate-framework.py --root .` ohne Fehler und
   der Sondenlauf in **beiden** Kodierungsumgebungen, mit und ohne `PYTHONIOENCODING=utf-8` (D-49).
   Verglichen werden die **Ergebniszeilen oberhalb der Trennlinie**; der Auswertungsblock darunter
   trägt Namen und Laufzeiten und ist ausdrücklich **nicht** Teil des Vergleichs (D-94). Ein
   gescheiterter Aufräumer ist eine Abweichung wie jede andere (D-96).
6. **Bericht** als Protokoll unter `tests/protocols/`. Das ist der Berichtspfad dieses
   Repositoriums; eine Analyse oder ein Review legt ihr Ergebnis dort ab. 🔴 **Das ist die
   SCHREIBENDE Hälfte des zweiten Einsatzkontextes** – M5 nach `framework/core/05-working-model.md`
   –, und bis `0.83.0` stand sie in **keiner** Fassung der Laufzeitschicht: Die fünf Analyseskills
   nennen das Quellrepositorium seit `0.32.0`, führen aber alle M1, und `fw-docs-update` (M5) sagt
   für ein inaktives Overlay ausdrücklich *„arbeitet der Skill nur lesend"*. Seit `0.84.0`
   verweisen die drei anweisenden Fassungen für **beide** Hälften hierher (D-253, Grenzfall G-11).
7. **Übergabe** fortschreiben – im Quellrepositorium `UEBERGABE.md` in der Wurzel (D-214). Sie gehört in den **Release-Commit**, nicht in einen Nachtrag danach: Alles, was sie braucht, liegt nach Schritt 5 und 6 vor. **Eine Nummer des Merge Requests steht nicht darin** – sie ist der einzige Wert, den man vor dem Anlegen des Antrags nicht kennt, und damit der einzige Grund, überhaupt nach dem Merge zu schreiben; *alles gemergt, kein offener Antrag* ist die Aussage, auf die es ankommt, und `git` beantwortet sie. Prüfung 67 hält die Titelzeile gegen `<CORE_DIR>/VERSION` (D-216).
8. **Freigabe und Merge führt der Mensch aus** (V1, V2). Der KI-Client schlägt Commit-Nachricht und
   Merge-Request-Beschreibung vor.

V10 bleibt unberührt: Eine Änderung an Framework-Regeln, Overlay oder Berechtigungsdatei ist
nicht delegierbar. **Was dieses Profil regelt, ist nicht, dass der KI-Client entscheidet, sondern
wie er vorbereitet** – und dass er dabei nicht gegen eine Regel läuft, die für den anderen
Einsatzkontext geschrieben ist.

## 5. Was dieses Profil nicht leistet

- **Es hebt keinen Schreibschutz auf.** `<CORE_DIR>/**`, `<RUNTIME_DIR>/**`,
  `<ROOT_INSTRUCTION_FILE>` und `.koolie/project-overlay/**` bleiben in der Berechtigungsdatei
  `write`-verweigert, und der Schutz-Hook blockiert dieselben Pfade für schreibende Werkzeuge.
  Ein Schalter, der das abschwächt, wäre in jeder Installation ausgeliefert – genau die Bauform,
  aus der in diesem Projekt die Befunde entstehen.
- **Die Selbstanwendung ist damit unvollständig, und zwar benennbar unvollständig.** Ein
  Shell-Befehl, der in das Kernverzeichnis schreibt, passiert den Hook; die Berechtigungsdatei
  führt für `exec` ausschließlich Befehlsverbote und keine einzige Pfadregel. Das ist **gemessen**
  (`tests/protocols/2026-09-12-B04-B05-gegenpruefung.md`, Läufe B04-1 bis B04-3) und in den
  Fähigkeitsmatrizen beider Packs bei B4, B5 und B8 je Zugriffskanal ausgewiesen (D-47). **Über
  diesen Kanal entstehen die Änderungen an diesem Framework heute.** Was sie aufhält, ist der
  Prozess aus Abschnitt 4 und die menschliche Freigabe – nicht der Hook.
- **Damit ist eine Frage offen, und sie steht als Klärungspunkt K-32:** Schließt Paket 6 den
  Shell-Schreibweg – über eine Isolationsschicht des Betriebssystems oder eine Pfadprüfung im Hook
  –, dann braucht die Entwicklung dieses Frameworks einen ausdrücklich entschiedenen Weg. Dieses
  Profil beschreibt bis dahin die Lage, es beschönigt sie nicht.

## 6. Freigegebene Prüfkommandos (normativ)

Lesende und prüfende Befehle; keiner verändert das Repositorium:

| Zweck | Befehl |
|---|---|
| Struktur- und Inhaltsprüfung | `python .koolie/core/tests/scripts/validate-framework.py --root .` |
| Aktivierungsreife eines Overlays | `python .koolie/core/tests/scripts/validate-framework.py --root . --strict-overlay` |
| Wirksamkeitsnachweis der Prüfungen | `python .koolie/core/tests/scripts/probe-pruefungen.py .` |
| Derselbe Nachweis, streng seriell | `python .koolie/core/tests/scripts/probe-pruefungen.py . --bahnen 1` |
| Abweichung einer Kern-Datei | `python .koolie/core/install.py --check` |
| Trockenlauf vor einer Installation | `python .koolie/core/install.py --dry-run` |
| Änderungsübersicht | `git status`, `git diff`, `git log`, `git show`, `git blame` |

Befehle mit Fernwirkung – `git push`, `git merge`, Tagging, Veröffentlichung – bleiben in jedem
Kontext ausgeschlossen (V2).

## 7. Erläuterung

Das Review hat diesen Befund nicht theoretisch gefunden, sondern an sich selbst: Es musste den
Auftrag als Berechtigung behandeln, um einen frischen Auscheckstand überhaupt analysieren zu
dürfen, und hat das ausgewiesen. Dieselbe Lage hatte jede Sitzung dieses Projekts vor sich – auch
die, die dieses Dokument geschrieben hat.

Die naheliegende Auflösung wäre gewesen, das Quellrepositorium technisch auszunehmen. Sie ist
verworfen: Ein abschwächender Schalter an einem Schutzmechanismus ist im Bestand dieses Projekts
der häufigste Befundtyp – eine Zusage, die mehr verspricht, als sie leistet, nur mit umgekehrtem
Vorzeichen. Die zweite Alternative, die Entwicklung ganz außerhalb des eigenen Regelwerks zu
führen, hätte den Nutzen der Selbstanwendung aufgegeben; sie hat bisher jeden Befund zuerst am
eigenen Repositorium gezeigt.

Geblieben ist der dritte Weg: Der Kontext wird **benannt**, die Lesefreigabe folgt aus der
Kontextklasse statt aus einer Ausnahme, und die Schranke bleibt der Prozess. Das ist weniger, als
eine technische Durchsetzung wäre, und mehr, als vorher dastand – nämlich nichts.
