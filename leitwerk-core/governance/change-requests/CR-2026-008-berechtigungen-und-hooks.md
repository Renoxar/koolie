# Änderungsantrag `CR-2026-008`

| Feld | Inhalt |
|---|---|
| Titel | Berechtigungsdatei und Hook-Konfiguration: eine Kernquelle, Semantikabbildung je Client Pack |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | neu: `leitwerk-core/clientmap.py`, `framework/runtime/permissions.json`, `framework/runtime/hooks.json`; entfallen: `clients/devin-desktop/root-template/.devin/config.json`, `clients/devin-desktop/root-template/.devin/hooks.v1.json`, `clients/claude-code/root-template/.claude/settings.json`; geändert: `install.py`, `tests/scripts/validate-framework.py`, `clients/*/manifest.json`, `clients/*/CLIENT_PACK.md`, `clients/_template/CLIENT_PACK.md`, `clients/README.md`, `docs/PLACEHOLDER_REGISTRY.md` |
| Ebene laut Entscheidungsbaum 6 | Core (Struktur) |
| Art | Änderung |
| Dringlichkeit | regulär (Review-Zyklus) |

## 1. Anlass und Problem

`CR-2026-007` hat die letzte Doppelpflege im Kern beseitigt – mit zwei ausdrücklich vertagten Ausnahmen: der Berechtigungsdatei und der Hook-Konfiguration. Sie blieben zurück, weil ihre Abbildung auf einen Client keine Formfrage ist.

Alle bisher zusammengeführten Artefakte unterscheiden sich zwischen zwei Client Packs nur in der **Form**: ein Frontmatter-Feld heißt anders, eine Werkzeugliste ist kommagetrennt statt eingerückt. Der Rumpf ist identisch, die Transformation verlustfrei und offensichtlich.

Bei Berechtigungen und Hooks unterscheiden sich die **Werkzeuge selbst**:

| Unterschied | `devin-desktop` | `claude-code` |
|---|---|---|
| Schreibwerkzeug | eines (`Write`) | zwei getrennte (`Edit`, `Write`) |
| Befehlsverbote | wörtlich (`Exec(git reset --hard)`) | präfixbasiert (`Bash(git reset:*)`) |
| Netzzugriff | ein Werkzeug mit Muster (`Fetch(*)`) | zwei Werkzeuge ohne Muster (`WebFetch`, `WebSearch`) |
| Suchwerkzeug | kein eigenes | `Grep`, `Glob` |
| Name im Projektverzeichnis | ohne Wurzelangabe (`.env`) | mit Wurzelangabe (`./.env`) |
| Hook-Ablage | eigene Datei | in der Berechtigungsdatei |

Genau daran hängen die Kernzusagen **B1 bis B6**. Doppelte Pflege ist hier deshalb nicht nur unbequem, sondern gefährlich: Eine Regel, die beim Nachziehen in das zweite Pack vergessen wird, ist eine stille Lücke in einer Schutzzusage – und die Fähigkeitsmatrix behauptet weiterhin `[TECHNISCH]`.

## 2. Vorgeschlagene Änderung

**Die Regelmenge liegt einmal im Kern.** `framework/runtime/permissions.json` beschreibt sie werkzeugneutral: Ein Werkzeugverb (`read`, `search`, `write`, `exec`, `fetch`, `mcp`), dazu ein Pfadmuster oder ein Befehl. `framework/runtime/hooks.json` beschreibt die Hooks entsprechend: auf welche Werkzeugklassen ein Hook anspricht und welches Skript er ruft. Beide Dateien werden nicht installiert, sondern übersetzt.

**Die Abbildung steht im Manifest des Client Packs.** Sechs neue Felder für Berechtigungen (`permission_tools`, `permission_tools_bare`, `permission_path_prefix`, `permission_exec_match`, `permission_exec_suffix`, `permissions_extra`), zwei für Hooks (`hook_tools`, `hook_project_dir_var`), dazu `permissions_note` für die Abweichung, die im erzeugten Kommentar stehen soll. Ob ein Client eine eigene Hook-Datei kennt, wird **nicht** eigens angegeben, sondern daran erkannt, dass `<HOOKS_FILE>` und `<PERMISSIONS_FILE>` auf denselben Pfad zeigen – zwei Angaben über dieselbe Tatsache wären eine Fehlerquelle.

**Ein eigenes Modul `clientmap.py`**, weil die Abbildung von zwei Werkzeugen gebraucht wird: `install.py` erzeugt damit die Dateien, `validate-framework.py` prüft damit die installierte Datei gegen die Kernquelle.

**Drei Zusicherungen werden erzwungen, nicht behauptet.** Das Verschärfungsprinzip ist bei einer Semantikabbildung keine Frage der Sorgfalt mehr, sondern eine Eigenschaft, die das Werkzeug prüfen kann:

| Zusicherung | Wirkung bei Verletzung |
|---|---|
| Eine `deny`- oder `ask`-Regel, für die ein Client kein Werkzeug kennt, ist ein Fehler | Installation bricht ab. Stillschweigendes Weglassen wäre eine Lockerung. Bei `allow` ist Weglassen zulässig – es fällt auf den strengeren Standard zurück |
| Die Präfixform eines Befehlsverbots muss ein Präfix seiner wörtlichen Form sein | Installation bricht ab. Die Zusicherung macht die Präfixform nachweislich mindestens so breit – die Abweichung ist damit belegbar eine Verschärfung |
| Bei `allow` müssen wörtliche und Präfixform übereinstimmen | Installation bricht ab. Dort wäre jede Verbreiterung eine Lockerung |

**Der Validator prüft die Kernregeln erstmals gegen die Kernquelle**, nicht nur gegen die Datei selbst. Bisher genügte es, eine Kernregel in `deny` **und** in `_core_rules_integrity.deny_must_contain` zu streichen: Die Datei blieb in sich stimmig, der Verlust unbemerkt. Weil die Berechtigungsdatei Saat ist und `install.py --check` sie deshalb nie anfasst, war das die einzige verbleibende Lücke in der Kette.

**Ein neuer Platzhalter `<CORE_DIR>`.** Der Name des Kernverzeichnisses steht in den Schreibverboten und im Hook-Befehl. Er ist keine Eigenschaft eines Clients, sondern dieser Installation, und wird deshalb von `install.py` und dem Validator aus dem tatsächlichen Verzeichnisnamen gesetzt – nicht im Manifest belegt. Damit berührt die in der Roadmap vorgesehene Umbenennung des Kernverzeichnisses (P3) kein Client Pack.

## 3. Prüffragen (durch Owner auszufüllen)

- [x] Richtige Ebene nach Entscheidungsbaum 6? — Ja. Die Regelmenge ist Ebene 3 (Framework Core); die Abbildung auf Werkzeugnamen ist die Abbildungsschicht aus D-12 und führt keine Regel ein.
- [x] Verschärfungsprinzip eingehalten? — Ja, und **nachgewiesen statt behauptet**: Alle drei erzeugten Dateien sind gegen den Stand 0.5.0 verglichen. Jede einzelne Berechtigungsregel und beide `_core_rules_integrity`-Blöcke sind byteweise identisch (13 Kernregeln bei `devin-desktop`, 17 bei `claude-code`). Zwei gewollte Abweichungen, beide ohne Wirkung auf das Schutzniveau: der erzeugte `_comment` (siehe Abschnitt 5) und die Reihenfolge im Hook-Matcher von `claude-code` (`Bash|Edit|Write|NotebookEdit` statt `Edit|Write|Bash|NotebookEdit`) – dieselbe Menge, eine Alternation ist ungeordnet.
- [x] Widerspruchsfreiheit geprüft? — Gelesen: `clients/README.md` Abschnitt 4 (Fähigkeitsmatrix, Kernzusagen), `PRIORITY_HIERARCHY.md`, D-04 (Berechtigungen versioniert mit restriktivem Standard), beide `CLIENT_PACK.md`. D-04 bleibt unberührt: Die Berechtigungen sind weiterhin versioniert und weiterhin Eigentum des Projekts, sobald sie angelegt sind.
- [x] Laufzeitfassungen betroffen? — Nur ihr Ursprung. Installationsumfang unverändert: 80 Dateien bei `devin-desktop`, 79 bei `claude-code`. Ein Client Pack enthält jetzt fünf Dateien statt sieben beziehungsweise sechs.
- [x] Belegstatus korrekt? — Unverändert. Keine Einstufung der Fähigkeitsmatrix wird durch diese Änderung belegt; die VERIFY-Marker bleiben stehen (Roadmap AP2).
- [x] Test- und Validierungsbedarf? — Siehe Abschnitt 5.
- [x] Auswirkungen auf Overlays und laufende Onboardings? — Für ein bestehendes Projekt keine. Die Berechtigungsdatei ist Saat und wird nie überschrieben; die dort eingetragenen Projektwerte bleiben. Neu ist allein, dass der Validator die Kernregeln zusätzlich gegen die Kernquelle prüft – ein Projekt, das keine Kernregel entfernt hat, merkt davon nichts.
- [x] Dokumentation? — Platzhalterregister (`<CORE_DIR>`), beide `CLIENT_PACK.md`, `clients/_template/CLIENT_PACK.md`, `clients/README.md`, die beiden Laufzeit-READMEs, CHANGELOG, Decision Log.

## 4. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | angenommen |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Die letzte und heikelste Doppelpflege ist beseitigt, ohne dass eine Regel sich ändert. Wichtiger als die Einsparung: Das Verschärfungsprinzip ist an der Stelle, an der die Kernzusagen B1 bis B6 hängen, jetzt eine geprüfte Eigenschaft und keine Zusage mehr. |
| Ziel-Release | 0.6.0 |
| Decision-Log-Eintrag | D-18 |

## 5. Umsetzung (nach Annahme)

- [x] `framework/runtime/permissions.json` (53 `deny`-, 5 `ask`-, 7 `allow`-Regeln, 13 davon als Kernzusage gekennzeichnet) und `framework/runtime/hooks.json`
- [x] `clientmap.py` mit den drei erzwungenen Zusicherungen; `resolve_placeholders` dorthin verschoben, weil beide Aufrufer sie brauchen
- [x] Manifestfelder in beiden Packs; die drei Vorlagendateien aus den Client Packs entfernt
- [x] `install.py`: Auswahl der Transformation über den Quellpfad, wie bei den übrigen geteilten Bestandteilen; `<CORE_DIR>` aus dem Verzeichnisnamen
- [x] Validator: Abgleich der Kernregeln gegen die Kernquelle; fehlt `clientmap.py`, wird gewarnt statt zu scheitern, und die bisherigen Prüfungen greifen weiter
- [x] **Byteweiser Vergleich gegen 0.5.0**: alle Berechtigungsregeln und beide Kernregellisten identisch; Hook-Datei von `devin-desktop` vollständig identisch
- [x] Erstinstallation beider Packs in ein leeres Verzeichnis: 80 / 79 Dateien wie zuvor; `--check` gegen beide fehlerfrei
- [x] Validator gegen beide Installationen und gegen die Wurzelinstallation dieses Repositorys: 0 Fehler
- [x] **Negativtests der Zusicherungen**: Kernregel aus *beiden* Listen einer installierten Datei entfernt → Validator meldet sie (vor dieser Änderung unbemerkt). Abbildung ohne Schreibwerkzeug, `prefix` ohne Präfixeigenschaft, `allow`-Regel mit verkürzter Präfixform, Hook-Werkzeugklasse ohne Werkzeug → Installation bricht jeweils mit benannter Ursache ab
- [x] Zwischenbefund behoben: Der Validator leitete `<CORE_DIR>` eine Verzeichnisebene zu tief ab und erzeugte dadurch Regeln wie `Write(clients/framework/**)`
- [x] **Befund, eigener Änderungsantrag** – erledigt durch `CR-2026-012` (Release 0.10.0, D-22): Die Schreibverbote schützen `<CORE_DIR>/framework/**`, nicht das gesamte Kernverzeichnis. Damit sind `install.py`, `validate-framework.py`, die beiden Hook-Skripte und nun auch `clientmap.py` nicht schreibgeschützt – gerade die Skripte, die die Schutzzusagen durchsetzen. Der Befund ist älter als diese Änderung; `clientmap.py` tritt einer bestehenden Lücke bei, statt eine neue zu öffnen. Die naheliegende Verschärfung auf `<CORE_DIR>/**` ändert die Kernregelmenge und gehört deshalb nicht in diesen Antrag
