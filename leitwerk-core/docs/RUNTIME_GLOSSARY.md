# Begriffe der Laufzeitschicht

| Attribut | Wert |
|---|---|
| ID | `FW-DOC-GLOSSARY` |
| Version | `0.2.0` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |

## Zweck

Der Kern des Frameworks ist werkzeugneutral (D-02). Er darf deshalb **keine Pfade nennen, die nur bei einem einzigen KI-Client existieren** – sonst ist er nicht neutral, sondern nur so formuliert, als wäre er es.

Diese Datei legt die Begriffe fest, mit denen der Kern die Bestandteile der Laufzeitschicht bezeichnet, und bildet sie auf die tatsächlichen Pfade je Client Pack ab. Sie ist damit das Gegenstück zum Platzhalterregister: Dort stehen projektspezifische Werte, hier clientspezifische Pfade.

## Regel

- Im **Kern** (`leitwerk-core/framework/`, `governance/`, `checklists/`, `prompts/`, `decision-trees/`, `onboarding/`, `docs/`, `templates/`, `examples/`, `tests/`) wird ausschließlich der **Begriff** verwendet.
- In einem **Client Pack** (`leitwerk-core/clients/<client>/`) wird der **Pfad** verwendet – dort ist er richtig und notwendig.
- In **historischen Dokumenten** bleiben genannte Pfade unverändert. Sie beschreiben einen vergangenen Zustand; ihn nachträglich zu glätten, würde die Nachvollziehbarkeit zerstören.

### Die vier Ausnahmen, vollständig (D-128)

Die Regel gilt für jeden Träger des Kerns. Ausgenommen ist genau, was hier steht – eine Ausnahme, die nur im Quelltext einer Prüfung stünde, wäre keine Regel, sondern eine Voreinstellung.

| Gattung | Träger | Warum |
|---|---|---|
| **Chronik** | `CHANGELOG.md`, `governance/change-requests/`, `governance/DECISION_LOG.md`, `tests/protocols/`, **`docs/ROADMAP.md`** | Sie berichten einen vergangenen Stand. Die Roadmap gehört dazu, weil sie die Erhebungsergebnisse je Arbeitspaket und die Befundberichte je Release führt |
| **Werkzeuge** | alle `.py` des Kerns | Ein Skript, das eine Installation herstellt oder prüft, **muss** Pfade nennen. `install.py` und `clientmap.py` lösen sie aus den Manifesten auf, die Prüfskripte stellen Installationen her |
| **Abbildungstabellen** | diese Datei, `docs/PLACEHOLDER_REGISTRY.md`, `clients/` | Sie müssen beide Namen nennen; dort ist der Pfad der Inhalt |
| **Mit Frist: `build/`** | die Quellen des Hauptdokuments | Das Hauptdokument ist über vierzig Releases zurück und wird mit `AP11` (~0.69.0) neu gesetzt. **Die Ausnahme fällt mit diesem Schritt**; sie steht dort in der Roadmap |

**Eine Spalte statt einer Datei.** In `tests/TEST_CATALOG.md` ist die **letzte** Zelle einer Tabellenzeile der Ergebnisstatus. Ein Pfad dort nennt, was ein Lauf gelesen hat, und gehört zum gemessenen Client Pack (D-117) – er ist Beleg, nicht Anweisung. Die übrigen Spalten derselben Zeile stehen unter der Regel: Die Eingabezelle „Passe AGENTS.md an" war bis 0.56.2 eine davon. Denselben Zuschnitt – die letzte Zelle – benutzt Prüfung 46 für den Ergebnisstatus.

### Was die Regel durchsetzt

**Prüfung 48** hält jeden anweisenden Kernträger gegen die Laufzeitpfade **aller** Client Packs; die Marken stammen aus den `runtime_placeholders` der Manifeste, nicht aus einer gepflegten Liste. Ein neues Client Pack bringt seine Pfade damit selbst mit.

> 🔴 **Von 0.31.0 bis 0.56.2 galt diese Regel und wurde von nichts durchgesetzt.** Siebzehn Fundstellen in vierzehn anweisenden Trägern nannten den Pfad genau eines Packs – darunter sechs Prompt-Vorlagen und mit Abschnitt 2 von `framework/core/08-skill-conventions.md` ein **normatives** Kernmodul, dessen Prosa zwei Zeilen tiefer richtig „die Skill-Ablage der Laufzeitschicht" sagte. **Prüfung 12 konnte sie nicht finden:** Sie liest nur Token in Backticks (zehn der siebzehn standen ohne), sie meldet nur Pfade, **die es nicht gibt** (im Framework-Repositorium ist genau ein Pack installiert, dessen Laufzeitschicht existiert und damit unsichtbar ist), und ihre eigene Wurzelliste war clientgebunden (`CR-2026-080`).

**Prüfung 14** setzt die zweite Hälfte durch: Kein Client wird im Kern als **Handelnder** benannt (D-28). Der **Produktname** bleibt dort ausdrücklich zulässig, wo ein Produkt gemeint ist. Ob diese Erlaubnis zu weit reicht, ist **`K-52`** und nicht entschieden – Prüfung 48 findet Pfade, keine Produktnamen.

## Begriffe und ihre Entsprechungen

| Begriff im Kern | Was es ist | `devin-desktop` | `claude-code` |
|---|---|---|---|
| **Wurzel-Anweisungsdatei** | Die Datei im Wurzelverzeichnis, die der Client zu Beginn jeder Sitzung lädt | `AGENTS.md` | `CLAUDE.md` |
| **Laufzeitschicht** | Das Verzeichnis mit allem, was der Client aus dem Repository liest | `.devin/` | `.claude/` |
| **Berechtigungsdatei** | Versionierte Konfiguration der Rechte (verweigern / rückfragen / erlauben) | `.devin/config.json` | `.claude/settings.json` |
| **Regelablage** | Verzeichnis der Regeltexte (Core-Kurzfassungen, Overlay, Packs) | `.devin/rules/` | `.claude/rules/` |
| **Skill-Ablage** | Verzeichnis der Skills, je Skill ein Unterverzeichnis mit `SKILL.md` | `.devin/skills/` | `.claude/skills/` |
| **Agentenprofile** | Verzeichnis der Subagentenprofile | `.devin/agents/` | `.claude/agents/` |
| **Hook-Konfiguration** | Ort der Lebenszyklus-Hooks | in der Berechtigungsdatei (`.devin/config.json`, D-32) | in der Berechtigungsdatei (`.claude/settings.json`) |
| **MCP-Konfiguration** | Ort der Anbindung externer Systeme | `.devin/mcp_config.json` | `.mcp.json` |
| **Nutzerlokale Überschreibung** | Nicht versionierte, persönliche Ergänzung; im Framework nur zum Verschärfen zulässig | `AGENTS.local.md`, `.devin/config.local.json` | `CLAUDE.local.md`, `.claude/settings.local.json` |

Die maßgebliche Fassung je Client steht in `manifest.json` (maschinenlesbar) und `CLIENT_PACK.md` Abschnitt 1 (mit Belegstatus) des jeweiligen Packs.

Der Begriff bezeichnet dabei nur den **Ort**. Berechtigungsdatei und Hook-Konfiguration haben zusätzlich einen **Inhalt**, der je Client anders geschrieben wird – andere Werkzeugnamen, getrennte Werkzeuge für Ändern und Anlegen, wörtliche gegen präfixbasierte Befehlsverbote. Diese zweite Abbildung steht in `CLIENT_PACK.md` Abschnitt 1a und wird von `leitwerk-core/clientmap.py` ausgeführt (D-18).

## Was der Begriff nicht sagt

Ein Begriff benennt die **Rolle** eines Artefakts, nicht seine Eigenschaften. Ob ein Client eine Zusage des Frameworks technisch erzwingt oder nur als Anweisung führt, steht in der **Fähigkeitsmatrix** seines Client Packs (`leitwerk-core/clients/README.md` Abschnitt 4).

Zwei Beispiele, in denen der Begriff gleich und die Wirkung verschieden ist:

- Die **Regelablage** enthält bei beiden Packs dieselben Regeltexte, und beide Clients laden sie von sich aus. Verschieden ist die **Bedingungssprache**: `devin-desktop` kennt die Ladetrigger der Kernquelle, `claude-code` kennt nur die Bindung an Dateimuster (`paths`) und lädt alles Übrige unbedingt. Der Kern beschreibt deshalb, *was* eine Regel bewirkt, nicht *wann* sie geladen wird; die Abbildung der Ladetrigger steht im Manifest des Packs unter `rule_triggers`.
- Die **Hook-Konfiguration** ist bei `devin-desktop` eine eigene Datei, bei `claude-code` ein Abschnitt der Berechtigungsdatei. Ein Kerntext, der „die Hook-Datei" nennt, wäre schon wieder clientgebunden.

## Nummernschema der Regelablage

Das Schema gilt über alle Client Packs, damit eine Regel beim Clientwechsel wiedererkennbar bleibt. Es ist eine Framework-Konvention (`[KONZ]`), keine Produkteigenschaft.

| Präfix | Ebene der Prioritätshierarchie |
|---|---|
| `00-` | 3 Framework Core (Arbeitsmodell) |
| `10-` | 3 Framework Core (Datenschutz und Sicherheit) |
| `15-` | 3 Framework Core (Entwicklungsregeln) |
| `20-` | 4 Project Overlay |
| `30-` | 6 Role Packs |
| `40-` | 5 Technology Packs |
