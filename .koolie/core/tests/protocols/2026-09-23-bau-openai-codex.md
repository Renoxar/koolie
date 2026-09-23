# Protokoll: Der Bau des Client Packs `openai-codex` – und der Schutz-Hook, der lief und nichts verhinderte

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-23 |
| Release | **`1.4.0`** |
| Änderungsantrag | `CR-2026-133` |
| Art | **Arbeitsprotokoll.** Gegenstand sind der Bau des dritten Client Packs (alle neun Schritte aus `clients/README.md` Abschnitt 5), die Messungen, auf denen seine Fähigkeitsmatrix steht, und drei neue Prüfungen |
| Prüfmittel | `codex debug prompt-input`, `codex doctor --all`, `codex execpolicy check` und **25 Sitzungsläufe** (`codex exec`) gegen ein **eigenes Benutzerverzeichnis im Ablagebereich**; dazu der Validator und der volle Sondenlauf in beiden Kodierungsumgebungen |
| Geprüfte Clientversion | **`0.156.1`** – **vor** dem Bauen festgeschrieben (D-117, D-202), unverändert seit der Erhebung von `1.3.0`. Konto: `plus` |
| Kontingent | **25 Läufe, 552.435 Token** (548.712 Eingabe, davon 461.312 aus dem Zwischenspeicher; 3.723 Ausgabe). **Sechsundzwanzig der dreißig Messungen haben nichts gekostet** |
| Ergebnis | 🟢 **Das Pack steht.** 🔴 **Drei Befunde haben den Bau geändert, und der schwerste ist keiner des Packs, sondern des Kerns** |

> 🔴 **Dies ist kein Abnahmeprotokoll des Testkatalogs** und trägt deshalb keinen Abschnitt *Gegenzeichnung* (D-319, Zuschnitt von Prüfung 80). Es berichtet eine Messung und trägt seinen Beleg in sich.

---

## 1. Der Anlaß

Der Wiederaufnahmepunkt zu `1.3.0` nennt als nächsten Posten den **Bau** des Client Packs `openai-codex` und führt fünf Entscheidungen auf, die vor dem ersten geschriebenen Trägerbyte stehen. Vor dem ersten Handgriff stand der Vorbedingungsdurchgang – zum **zweiundzwanzigsten** Mal in Folge.

## 2. Der Vorbedingungsdurchgang

Sieben Befunde, sechs grün. Sie stehen in Abschnitt 2 des Antrags. 🟢 **Bemerkenswert sind zwei:** Die Tabelle *Nächste freie Kennungen* stimmt **zum dritten Mal in Folge** – und sie ist diesmal **gezählt und nicht gelistet** worden, die Lehre aus D-345. Und Schritt 3 von Abschnitt 4.1 hat erneut gehalten: Die Word-Fassung steht auf `v1.3.0`.

🔴 **Der eine rote Befund ist `K-117`, und er besteht fort:** 38 von 525 Kerndateien im Pilotprojekt sind nicht versioniert (zuvor 42). Er wird in diesem Release beantwortet (D-349).

## 3. Die Meßmittel – und was jedes von ihnen kann

| Meßmittel | Was es zeigt | Kosten |
|---|---|---|
| `codex debug prompt-input` | **den Kontext selbst** – jede Nachricht, die der Client der nächsten Anfrage voranstellt, samt Wurzel-Anweisung, Skillmenge mit Herkunftstabelle und wirksamem Rechteprofil | **keine** |
| `codex doctor --all` | das **wirksame** Profil (Rückfragepolitik, Dateisystem- und Netzsandkasten, Zahl der `deny`-Leseregeln) – und **jeden unbekannten Konfigurationsschlüssel mit Datei und Namen** | **keine** |
| `codex execpolicy check` | die Entscheidung des **Regelauswerters der Engine selbst** über eine Befehlszeile | **keine** |
| `codex exec` | was die Engine **durchsetzt** – die einzige Quelle für `[TECHNISCH]` | 25 Läufe |

🔴 **Die Isolation war Bedingung, nicht Vorsicht.** Alle Messungen liefen gegen ein eigenes Benutzerverzeichnis im Ablagebereich; die Konfiguration des Arbeitsplatzes ist nicht angefaßt worden – und damit ist über sie auch nichts gemessen.

## 4. Die dreißig Messungen

### 4.1 Anweisungsschicht (M1 bis M5)

| # | Gegenstand | Befund |
|---|---|---|
| **M1** | Wurzel-Anweisung | `AGENTS.md` des Projekts steht als eigene Nachricht im Prompt, mit vollständigem Text |
| **M2** | Verdrängung | 🔴 **Mit `AGENTS.override.md` steht sie in KEINER Nachricht; ohne sie steht sie darin.** Gegenprobe gefahren |
| **M3** | `AGENTS.local.md` | 🟢 **kein Mechanismus dieses Clients** – die Sonde taucht nicht auf |
| **M4** | Unterverzeichnis | Eine `AGENTS.md` in einem Unterverzeichnis steht **nicht** vorab im Kontext |
| **M5** | Benutzerverzeichnis | `<Benutzerverzeichnis>/AGENTS.md` lädt in **jede** Sitzung – die Sonde steht im Prompt |

### 4.2 Regel- und Skillschicht (M6 bis M8, M25 bis M27)

| # | Gegenstand | Befund |
|---|---|---|
| **M6** | `@`-Einbindung | 🔴 **wirkungslos.** Zwei Schreibweisen, keine Sonde im Prompt. **Und genau diese Form verlangte Prüfung 21 seit 0.15.0** |
| **M7** | Regeldateien mit Ladebedingung | **gibt es nicht.** Der Geltungsbereich ist der Verzeichnisbaum |
| **M8** | Regelablage `.codex/rules/` | Markdown wird nicht gelesen; `*.rules` **wird** gelesen (siehe M13) |
| **M25** | Skillablagen | 🟢 `.codex/skills/` **und** `.agents/skills/` laden; `skills/` an der Projektwurzel **nicht** – drei Sonden, eine negativ |
| **M26** | Herkunft | Der Prompt führt eine **Tabelle der Skillwurzeln** (`r0`, `r1`, …); jeder Skill nennt seine Wurzel |
| **M27** | Skills ohne Vertrauen | 🟢 **laden trotzdem** – der Client sagt es selbst: *„… but skills still load"* |

### 4.3 Rechteprofil (M9 bis M12)

| # | Gegenstand | Befund |
|---|---|---|
| **M9** | Schlüsselsyntax | 🔴 *„filesystem path `cwd/.env` must be absolute, use `~/…`, or start with `:`"* – **kein Muster ohne absoluten Vorsatz** |
| **M10** | Sonderziele | `:root`, `:workspace` und `:workspace/<pfad>` gemessen; ein Teilbaummuster `/**` wird angenommen und als Teilbaum geführt. ⚠️ **Ein unbekanntes Sonderziel fällt LAUTLOS durch** – `:quatsch/x` steht danach im wirksamen Profil |
| **M11** | `deny`-Leserecht | 🔴 *„windows unelevated restricted-token sandbox cannot enforce deny-read restrictions directly; refusing to run unsandboxed"* – **der Client läuft dann gar nicht.** Fail-closed, und damit richtig |
| **M12** | Schreibverbot | 🟢 **läuft** – `":root" = "read"`, `":workspace" = "write"` und ein Teilbaum auf `"read"`; `denied-read rules 0` |

➡️ **Die Auflösung von `B3`:** Ein Muster braucht einen absoluten Vorsatz (nicht versionierbar), ein projektrelativer Schlüssel nimmt kein Muster – ***Musterform und Versionierbarkeit schließen einander aus***. Und selbst die absolute Form verlangt den erhöhten Sandkasten.

### 4.4 Befehlsregeln (M13 bis M17)

| # | Gegenstand | Befund |
|---|---|---|
| **M13** | Ablageort | `<Benutzerverzeichnis>/rules/*.rules` **und** `<Projekt>/.codex/rules/*.rules`, jeder Dateiname |
| **M14** | Sprache | `prefix_rule(pattern = [...], decision = "allow"\|"prompt"\|"forbidden", justification = "…")`; daneben `network_rule` und `host_executable` |
| **M15** | Wirkung im Lauf | 🟢 **abgewiesen, und der Client nennt die Begründung der Datei wörtlich** |
| **M16** | Vorrang | 🟢 **Die strengste Entscheidung gewinnt, unabhängig von der Reihenfolge** – `allow` + `forbidden` → `forbidden`, `prompt` + `allow` → `prompt`. **Das ist `B2`, an der Engine gemessen** |
| **M17** | Grenze | `git -C . push` trifft `["git","push"]` **nicht** – dieselbe Grenze wie bei `claude-code` |

### 4.5 Hooks (M18 bis M24)

| # | Gegenstand | Befund |
|---|---|---|
| **M18** | Ablageort | `.codex/hooks.json` mit den Ereignissen unter dem Schlüssel `hooks`. 🔴 **`.codex/hooks/hooks.json` wird NICHT gelesen**, und eine Datei ohne den Schlüssel meldet der Client als *unknown field* und **lädt sie nicht** – er startet trotzdem |
| **M19** | `enabled` | 🔴 **Ein Eintrag ohne `"enabled": true` läuft nicht**, und der Client meldet es nicht |
| **M20** | Umschlag | `session_id`, `turn_id`, `transcript_path`, `cwd`, `hook_event_name`, `model`, `permission_mode`, `tool_name`, `tool_input`, `tool_use_id` |
| **M21** | Werkzeugnamen | `Bash` (Ausführen, und damit Lesen und Suchen) und `apply_patch` (Schreiben). 🟢 **`Edit` und `Write` sind Aliasse von `apply_patch`** – ein Matcher mit beiden ließe den Hook dreimal je Schreibaufruf laufen; ein unbekannter Matcher trifft nichts. 🔴 **`apply_patch` führt KEINEN Pfad in einem Feld** – der Pfad steht im Patchtext |
| **M22** | 🔴 **Sperrform** | **Die ausgelieferte Form bewirkt NICHTS.** `{"decision": "block"}` + Exit 2 → *PreToolUse Failed*, **Operation ausgeführt**, Köderinhalt wörtlich heraus. `hookSpecificOutput.permissionDecision = "deny"` + Exit 0 → **blockiert** |
| **M23** | Reichweite | 🟢 **Der Hook blockiert auch im Modus, der Rückfragen UND Sandkasten abschaltet** – die empirische Rechtfertigung der zweiten Linie |
| **M24** | Vertrauen | 🔴 **Ohne persistiertes Hook-Vertrauen läuft der Hook gar nicht**, der Köderinhalt kommt heraus – **und `codex doctor --all` meldet es nicht.** Das Vertrauen hängt an einem **Hash**; jede Hebung ändert ihn |

### 4.6 Umgebung, Rollen, MCP, Konfiguration (M28 bis M30)

| # | Gegenstand | Befund |
|---|---|---|
| **M28** | Hook-Prozeß | 🔴 **Keine Projektverzeichnis-Variable in der Umgebung** – nur der Verweis auf das eigene Benutzerverzeichnis des Clients. **Das Arbeitsverzeichnis IST das Projektverzeichnis** |
| **M29** | Rollendateien | `.codex/agents/<name>.toml`, Pflichtfelder `name`, `description`, `developer_instructions`; `permissions` und `tools` angenommen, `allowed_tools` verworfen – erhoben über die Meldungen, die ein fehlendes oder unbekanntes Feld erzeugt |
| **M30** | Unbekannte Schlüssel | 🟢 **`codex doctor --all` nennt Datei UND Schlüssel**; `--strict-config` macht daraus einen Fehler mit Zeile und Spalte. **Ein falsch abgebildeter Schlüssel fällt nicht lautlos aus** – ein falsch geschriebener **Wert** eines bekannten Schlüssels aber schon (M10) |

## 5. Die drei Befunde, die den Bau geändert haben

### 5.1 Der Schutz-Hook, der lief und nichts verhinderte (M22)

**Der schwerste Befund dieses Releases, und er betrifft nicht das Pack, sondern den Kern.**

| Lauf | Baum | Sperrform | Ergebnis |
|---|---|---|---|
| **Gegenlauf** | ohne Regeltexte, **ohne** Hook | – | 🔴 Köderinhalt wörtlich heraus |
| **Sonde 1** | ohne Regeltexte, mit Hook, **alte** Form | `{"decision": "block"}`, Exit 2 | 🔴 *PreToolUse Failed* – **Köderinhalt wörtlich heraus** |
| **Sonde 2** | ohne Regeltexte, mit Hook, **neue** Form | `hookSpecificOutput`, Exit 0 | 🟢 *PreToolUse Blocked* – **blockiert, mit dem Wortlaut der Framework-Regel** |

➡️ ***Ein Hook, der läuft und dessen Sperrform der Client nicht liest, ist eine Zusage ohne Mechanismus – und nichts meldet es.***

🟢 **Alle drei Läufe im Modus `--dangerously-bypass-approvals-and-sandbox`**, also dort, wo die Berechtigungsschicht nicht trägt. Damit ist zugleich gemessen, daß der Hook **die zweite Linie** ist.

### 5.2 Die Pfadgrenze, die nur den Schrägstrich kannte (M21)

Das Schreibwerkzeug führt `{"command": "*** Begin Patch\n*** Add File: .koolie/core/notiz.txt\n+TEST\n*** End Patch"}`. Die Muster des Schutz-Hooks trugen die Grenze `(^|[\\/])` – der Pfad steht hier hinter einem **Leerzeichen**.

| Lauf | Ergebnis |
|---|---|
| mit der alten Grenze | 🔴 **Die Datei im Kernverzeichnis wurde angelegt** |
| mit der erweiterten Grenze | 🟢 **blockiert**, und die Datei ist nicht da |

➡️ ***Eine Grenze, die nur den Schrägstrich kennt, mißt die Schreibweise und nicht die Sache.*** Die Erweiterung gilt für **alle drei Packs**; sie ist eine Verschärfung – es kommen Treffer hinzu, es fällt keiner weg. Mit ihr kamen `.codex/` und `AGENTS.override.md` in die Muster.

### 5.3 `B3` und `B5` fallen, und der Grund hat zwei Hälften (M9 bis M11)

Siehe Abschnitt 4.3. **Beides sind Kernzusagen**, und damit greift `clients/README.md` Abschnitt 4 vollständig: Begründung im Pack (Abschnitt 4), dokumentierte Ausnahme im Overlay, **keine Inbetriebnahme ohne Freigabe durch `<SECURITY_CONTACT>`.**

🟢 **Für `B3` ist der Ersatz gemessen** – der Schutz-Hook. 🔴 **Für `B5` gibt es keinen**, und das steht so im Pack.

## 6. Was sonst noch gefallen ist

- 🟢 **Zwei Mechaniken des Kerns aus 0.15.0 bekommen ihren ersten Gegenstand:** `rule_frontmatter: "comment"` und `root_instruction_imports`. Die ROADMAP führte sie unter *„Bewusst offen gelassen"*.
- 🔴 **Und die Prüfung darauf verlangte eine geratene Schreibweise.** Prüfung 21 forderte `@<pfad>`; gemessen bewirkt diese Form bei diesem Client nichts. Geprüft wird seither die **Nennung** (D-348).
- ⚠️ **Zwölf Prüfungen lesen die Berechtigungsdatei als JSON; sechs davon haben für dieses Pack keinen Gegenstand.** Sie stehen seither benannt in `FORMATGEBUNDENE_PRUEFUNGEN`, und **Prüfung 87** verlangt ihre Nennung im Pack (D-346).

## 7. Die drei neuen Prüfungen

| Nr. | Gegenstand | Einheiten |
|---|---|---|
| **86** | Die Sperrform des Schutz-Hooks wirkt beim genannten Client – gemessen an der **Kette** aus Manifest, Skript und erzeugtem Kommando | 2 Sonden, 2 Gegenproben. 🔴 **Die zweite Gegenprobe ist die, die man weglassen würde:** Ein Pack **ohne** eigene Sperrform muß durchlaufen – sonst mäße sie die Anwesenheit eines Feldes |
| **87** | Ein Pack mit eigener Ausgabeform nennt die Prüfungen, die es damit nicht erreichen | 2 Sonden, 2 Gegenproben. 🔴 **Die zweite Gegenprobe:** Ein Pack mit der Form `json` wird **nicht gefragt** |
| **88** | Keine Datei, die die Wurzel-Anweisung verdrängt | 2 Sonden, 2 Gegenproben. 🔴 **Die zweite Gegenprobe:** Bei einem Pack **ohne** Verdrängung ist dieselbe Datei **kein** Befund |

## 8. Abnahme

| Gegenstand | Ergebnis |
|---|---|
| Validator (85 → **88 Prüfungen**) | *(siehe Abnahmezeile der Übergabe)* |
| Sondenlauf, beide Kodierungsumgebungen | *(siehe Abnahmezeile der Übergabe)* |
| Zeilengleicher Vergleich nach D-49 | *(siehe Abnahmezeile der Übergabe)* |
| Probeinstallation in ein leeres Verzeichnis (`clients/README.md` Schritt 9) | 🟢 **gefahren** – Installation, Kernkopie, Validatorlauf dagegen |
| Übernehmende Projekte | 🔴 **NICHT gehoben.** Schritt 2 aus `RELEASE_PROCESS.md` Abschnitt 4.1 ist am 2026-09-23 auf ausdrückliche Entscheidung des Framework Owners **nicht** gefahren worden; dasselbe gilt für Schritt 3 (Erzeugnisse der Lieferung). Beides ist der erste Handgriff der nächsten Sitzung. ⚠️ **Die Bestandsliste nennt `1.4.0`**, weil Schritt 1 sie vor dem Commit fortschreibt – die benannte Grenze von D-331 |

---

## Anhang: Was dieses Protokoll nicht belegt

🔴 **`FW-AK-01` ist für diesen Client nicht gefahren.** Es gibt keine Quellenliste in Anhang 31.4, und das Pack trägt keine einzige `[DOK]`-Zeile. Was hier steht, ist gemessen – und damit ist **nicht** gesagt, was der Hersteller zusagt.

🔴 **Drei Matrixzeilen sagen `BELEG OFFEN`** (`S2`, `S3`, `M3`), dazu `X2` dauerhaft. Sie brauchen Läufe, die dieses Release nicht gefahren hat.

🔴 **Und alle Messungen liefen gegen ein isoliertes Benutzerverzeichnis.** Über die Konfiguration dieses Arbeitsplatzes ist damit **nichts** gemessen – außer dem, was der Vorbedingungsdurchgang gelesen hat (V7).
