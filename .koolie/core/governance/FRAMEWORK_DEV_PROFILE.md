# Entwicklungsprofil des Quellrepositoriums

| Attribut | Wert |
|---|---|
| ID | `FW-GOV-DEV` |
| Version | `0.1.5` |
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

Dieses Profil regelt den zweiten Kontext (D-56), weil **jede Sitzung an diesem Framework in ihm
steht**: Die Overlay-Vorlage bleibt hier absichtlich Vorlage, während die Regeln der
Laufzeitschicht freigegebene Pfade voraussetzen.

## 2. Geltungsbereich (normativ)

1. Dieses Profil gilt in einem Repositorium, das **die Quelle dieses Frameworks ist**: Es führt
   `.koolie/core/VERSION`, `.koolie/core/governance/` und `.koolie/core/framework/core/` unter
   Versionskontrolle, und die Laufzeitschicht ist dort laut `.gitignore` ein **Erzeugnis**.
2. Die Geltung folgt **nicht** aus einem Verzeichnisnamen und **nicht** aus einer Behauptung des
   KI-Clients. Sie folgt aus dem Inhalt des Repositoriums, und sie erteilt **keine technische
   Berechtigung** (Abschnitt 5).
3. **`install.py` schreibt dieses Profil in kein Zielprojekt.** Es liegt unter `governance/`,
   nicht unter `templates/` und nicht unter `framework/runtime/`; `seed_paths` jedes Client
   Packs ist leer. **Im Zielprojekt liegt es trotzdem** (gemessen am 2026-09-22, D-253): Die
   Installation kopiert `.koolie/core/` samt `governance/` in jedem Lieferumfang
   (`docs/ADOPTION_GUIDE.md` Abschnitt 2, D-354, D-367). Es erteilt dort keine Geltung: Die folgt nach Abschnitt 2.1 aus dem **Inhalt** des
   Repositoriums und nicht aus der Anwesenheit dieser Datei.

## 3. Lesen (normativ)

1. Der Inhalt dieses Repositoriums ist **K0** nach `.koolie/core/framework/core/02-privacy.md`
   Abschnitt 2: framework-eigene Inhalte ohne Projektbezug. Er ist damit ohne Overlay und ohne
   Einzelfreigabe lesbar.
2. Das gilt ausdrücklich für die Anweisungsquellen selbst – Wurzel-Anweisungsdatei, Regelablage,
   Kernregeltexte, Overlay-Vorlage, Client Packs. **Ihr Schreibschutz ist kein Leseverbot**
   (D-55); beide technischen Schichten machen diese Unterscheidung (D-30).
3. Die Analyseskills sind hier zulässig, obwohl kein Overlay aktiv ist. Ihre Vorbedingung nennt
   diesen Fall neben dem Übungsrepositorium (D-56).
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
   Repositoriums; eine Analyse oder ein Review legt ihr Ergebnis dort ab. **Das ist die
   schreibende Hälfte des zweiten Einsatzkontextes** – M5 nach `framework/core/05-working-model.md`;
   die drei anweisenden Fassungen der Laufzeitschicht verweisen für **beide** Hälften hierher
   (D-253, Grenzfall G-11).
7. **Übergabe** fortschreiben – `UEBERGABE.md` in der Wurzel, **lokal und nicht versioniert** (D-350). Sie steht in der `.gitignore` wie ihre Beilage `UEBERGABE.local.md`, und keine Prüfung erreicht sie. ⚠️ **Das ist ihr Preis:** Stand und Zahlen der Übergabe hält niemand gegen `<CORE_DIR>/VERSION` – sie gehört deshalb an den Schluss eines Releases, wenn alle Zahlen feststehen, und wer sie liest, zählt nach, statt ihr zu glauben. **Sie darf eine Nummer des Merge Requests nennen**, weil sie keinem Release-Commit mehr angehört (D-350).
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
  führt für `exec` ausschließlich Befehlsverbote und keine einzige Pfadregel. **Gemessen** ist
  das nur für `claude-code` (`tests/protocols/2026-09-12-B04-B05-gegenpruefung.md`, Läufe B04-1
  bis B04-3, Framework 0.29.0); für die übrigen Packs ist es **nicht gemessen**. Ausgewiesen ist
  es in den Fähigkeitsmatrizen der Packs bei B4, B5 und B8 je Zugriffskanal (D-47). **Der
  Kanal steht offen:** Was eine Änderung über ihn aufhält, ist der Prozess aus Abschnitt 4 und
  die menschliche Freigabe – nicht der Hook.
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

Der Kontext wird **benannt**, die Lesefreigabe folgt aus der Kontextklasse statt aus einer
Ausnahme, und die Schranke bleibt der Prozess (D-56). Das ist weniger, als eine technische
Durchsetzung wäre.

- **Verworfen:** das Quellrepositorium technisch auszunehmen – ein abschwächender Schalter an
  einem Schutzmechanismus wäre in jeder Installation ausgeliefert (D-56).
- **Verworfen:** die Entwicklung ganz außerhalb des eigenen Regelwerks zu führen – das gäbe den
  Nutzen der Selbstanwendung auf, die jeden Befund zuerst am eigenen Repositorium zeigt (D-56).
