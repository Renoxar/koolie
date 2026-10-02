# Entwicklungsprofil des Quellrepositoriums

| Attribut | Wert |
|---|---|
| ID | `FW-GOV-DEV` |
| Version | `0.2.0` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Gilt für | das Quellrepositorium dieses Frameworks – **nicht** für ein Projekt, das ein Release anwendet |

## 1. Zwei Einsatzkontexte (normativ)

Das Framework wird in zwei Lagen benutzt; die Regeln der Laufzeitschicht sind für die erste
geschrieben:

| Kontext | Gegenstand der Arbeit | Overlay | Wer setzt die Grenze durch |
|---|---|---|---|
| **Anwendung** | Der Code eines Projekts. Das Framework ist unveränderliches Release | ausgefüllt, Status `aktiv` | Berechtigungsdatei, Schutz-Hook und Regelschicht |
| **Entwicklung** | Das Framework selbst. Es gibt kein Projekt, dessen Code bearbeitet würde | bleibt Vorlage, Status offen | der Änderungsprozess dieses Verzeichnisses |

Dieses Profil regelt den zweiten Kontext. Jede Sitzung an diesem Framework steht in ihm: Die
Overlay-Vorlage bleibt hier Vorlage, während die Regeln der Laufzeitschicht freigegebene Pfade
voraussetzen.

## 2. Geltungsbereich (normativ)

1. Dieses Profil gilt in einem Repositorium, das **die Quelle dieses Frameworks ist**: Es führt
   `.koolie/core/VERSION`, `.koolie/core/governance/` und `.koolie/core/framework/core/` unter
   Versionskontrolle, und die Laufzeitschicht ist dort laut `.gitignore` ein Erzeugnis.
2. Die Geltung folgt aus dem Inhalt des Repositoriums – nicht aus einem Verzeichnisnamen und nicht
   aus einer Behauptung des KI-Clients. Sie erteilt **keine technische Berechtigung**
   (Abschnitt 5).
3. `install.py` schreibt dieses Profil in kein Zielprojekt: Es liegt unter `governance/`, nicht
   unter `templates/` oder `framework/runtime/`, und `seed_paths` jedes Client Packs ist leer. Als
   Teil von `.koolie/core/` liegt es trotzdem in jedem installierten Projekt
   (`docs/ADOPTION_GUIDE.md` Abschnitt 2). Dort gilt es nicht, weil die Geltung nach Punkt 1 aus
   dem Inhalt des Repositoriums folgt.

## 3. Lesen (normativ)

1. Der Inhalt dieses Repositoriums ist **K0** nach `.koolie/core/framework/core/02-privacy.md`
   Abschnitt 2: framework-eigene Inhalte ohne Projektbezug. Er ist ohne Overlay und ohne
   Einzelfreigabe lesbar.
2. Das gilt auch für die Anweisungsquellen selbst – Wurzel-Anweisungsdatei, Regelablage,
   Kernregeltexte, Overlay-Vorlage, Client Packs. Ihr Schreibschutz ist kein Leseverbot; beide
   technischen Schichten unterscheiden das.
3. Die Analyseskills sind hier zulässig, obwohl kein Overlay aktiv ist. Ihre Vorbedingung nennt
   diesen Fall neben dem Übungsrepositorium.
4. **Ausgenommen bleibt, was auch hier K3 ist:** Secret-Dateien, Schlüsselmaterial und alles
   Übrige aus Abschnitt 2.1 des Datenschutzmodells. Eine Datei wird nicht dadurch lesbar, dass sie
   neben einer Regeldatei liegt.

## 4. Ändern (normativ)

Die Reihenfolge ist der Änderungsprozess des Frameworks, kein Betriebsmodus:

1. **Befund** mit Fundstelle (`pfad/datei:zeile`). Ein Befund von außen, auch aus einem Review,
   wird zuerst gegengeprüft.
2. **Änderungsantrag** unter `governance/change-requests/` nach
   `governance/CHANGE_REQUEST_TEMPLATE.md`, mit dem Abschnitt „Vorlage zur Entscheidung“: jede
   Ermessensfrage einzeln, mit Auflösung und Preis.
3. **Entscheidung** durch `<FRAMEWORK_OWNER>` in Abschnitt 6 des Antrags; tragende Entscheidungen
   zusätzlich als Decision Record in `governance/DECISION_LOG.md`, mit Begründung und verworfenen
   Alternativen.
4. **Umsetzung** mit Wirkungsnachweis: je neue Prüfung eine Sonde und eine Gegenprobe in
   `tests/scripts/probe-pruefungen.py`; die neuen Sonden MÜSSEN gegen die Vorversion **fallen**.
   **Schreiben** nach den Schreibregeln in `docs/DOCUMENTATION_STANDARD.md` Abschnitt 3: In der
   Produktdokumentation steht, was gilt und was zu tun ist – ohne Kennung und ohne
   Entscheidungsgeschichte. Kennung, Begründung und Verworfenes gehören in Änderungsantrag und
   Decision Log; Prüfung 113 meldet eine Kennung am falschen Ort.
5. **Abnahme:** `python .koolie/core/tests/scripts/validate-framework.py --root .` ohne Fehler und
   der Sondenlauf in beiden Kodierungsumgebungen, mit und ohne `PYTHONIOENCODING=utf-8`.
   Verglichen werden die Ergebniszeilen oberhalb der Trennlinie; der Auswertungsblock darunter
   trägt Namen und Laufzeiten und gehört nicht zum Vergleich. Ein gescheiterter Aufräumer ist eine
   Abweichung wie jede andere.
6. **Bericht** als Protokoll unter `tests/protocols/`. Das ist der Berichtspfad dieses
   Repositoriums; auch eine Analyse oder ein Review legt ihr Ergebnis dort ab. Das ist die
   schreibende Hälfte des zweiten Einsatzkontextes – M5 nach `framework/core/05-working-model.md`;
   die drei anweisenden Fassungen der Laufzeitschicht verweisen für beide Hälften hierher
   (Grenzfall G-11).
7. **Übergabe** fortschreiben – `UEBERGABE.md` in der Wurzel, lokal und nicht versioniert. Sie
   steht wie ihre Beilage `UEBERGABE.local.md` in der `.gitignore`, und keine Prüfung erreicht sie.
   Ihre Zahlen hält deshalb niemand gegen `<CORE_DIR>/VERSION`: Sie wird am Schluss eines Releases
   geschrieben, und wer sie liest, zählt nach. Sie darf die Nummer des Merge Requests nennen, weil
   sie keinem Release-Commit angehört.
8. **Freigabe und Merge führt der Mensch aus** (V1, V2). Der KI-Client schlägt Commit-Nachricht und
   Merge-Request-Beschreibung vor.

V10 bleibt unberührt: Eine Änderung an Framework-Regeln, Overlay oder Berechtigungsdatei ist
nicht delegierbar. Dieses Profil regelt nicht, dass der KI-Client entscheidet, sondern wie er
vorbereitet, ohne gegen eine Regel des anderen Einsatzkontextes zu laufen.

## 5. Was dieses Profil nicht leistet

- **Es hebt keinen Schreibschutz auf.** `<CORE_DIR>/**`, `<RUNTIME_DIR>/**`,
  `<ROOT_INSTRUCTION_FILE>` und `.koolie/project-overlay/**` bleiben in der Berechtigungsdatei
  `write`-verweigert, und der Schutz-Hook blockiert dieselben Pfade für schreibende Werkzeuge.
  Ein Schalter, der das abschwächt, wäre in jeder Installation mit ausgeliefert.
- **Die Selbstanwendung ist unvollständig.** Ein Shell-Befehl, der in das Kernverzeichnis
  schreibt, passiert den Hook; die Berechtigungsdatei führt für `exec` nur Befehlsverbote und keine
  Pfadregel. Gemessen ist das für `claude-code`
  (`tests/protocols/2026-09-12-B04-B05-gegenpruefung.md`, Läufe B04-1 bis B04-3, Framework
  0.29.0), für die übrigen Packs nicht. Ausgewiesen ist es in den Fähigkeitsmatrizen der Packs bei
  B4, B5 und B8 je Zugriffskanal. Was eine Änderung über diesen Kanal aufhält, ist der Prozess aus
  Abschnitt 4 und die menschliche Freigabe, nicht der Hook.
- **Offen:** Wird der Shell-Schreibweg geschlossen – über eine Isolationsschicht des
  Betriebssystems oder eine Pfadprüfung im Hook –, braucht die Entwicklung dieses Frameworks einen
  ausdrücklich entschiedenen Weg. Bis dahin beschreibt dieses Profil die Lage.

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

Der Kontext wird benannt, die Lesefreigabe folgt aus der Kontextklasse statt aus einer Ausnahme,
und die Schranke bleibt der Prozess. Das ist weniger als eine technische Durchsetzung, aber ein
abschwächender Schalter am Schutzmechanismus wäre in jeder Installation mit ausgeliefert. Die
Entwicklung bleibt innerhalb des eigenen Regelwerks, damit jeder Befund zuerst am eigenen
Repositorium sichtbar wird.
