# Protokoll: Die Code- und Pack-Posten der Durchsicht – und der Hook, dem nach jeder Hebung neu vertraut werden muss

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-25 |
| Release | `1.10.0` |
| Änderungsantrag | `CR-2026-146` |
| Art | Werkzeuge, Client Packs und Hauptdokument nach den Befunden der Durchsicht der Klasse B – **drei kurze Sitzungsläufe mit Claude Code für `K-129` (1), sonst keine Sitzung, kein Kontingent** |
| Gegenstand | `install.py`, `validate-framework.py --mermaid`, `build/assemble.py`, `build/build-docx.py`, die drei Client Packs und ihre Vorlage, `02-privacy.md`, `03-security.md`, `onboarding/exercises/README.md` |
| Ergebnis | 🟢 **Entschieden, `D-395` bis `D-401`.** Acht Klärungspunkte beantwortet, `K-152` neu; zwei neue Sondenbündel, beide fallen gegen den Vorstand |

---

## 1. Was gefragt war

Wiederaufnahmepunkt von `1.9.3`, Punkt 2: die Code- und Pack-Posten der Durchsicht (D-384),
`K-125` entscheiden oder vertagen. Fragen (a) bis (j) vorgelegt am 2026-09-25 und angenommen.
`CR-2026-146` E1 bis E10; E11 ist die Einplanung von Kiro, beauftragt während des Baus (D-401).

## 2. Messungen

**Gegenbeweis gegen den Vorstand.** Ein Baum aus `v1.9.3` (`git archive`) mit dem neuen
Sondenskript:

| Einheit | `v1.9.3` | `1.10.0` |
|---|---|---|
| `D395` (`openai-codex`: Vertrauensschritte nach Installation und Hebung) | FEHL – keiner der drei Sätze, dafür der Integritätsblock | OK |
| `D395a` (`claude-code`: Integritätsblock, kein Vertrauensschritt) | OK | OK |
| `D398`, `D398a` (Unterscheidung des Renderers) | FEHL – das Modul gibt es nicht | OK |

**`K-145`, am Renderer gemessen** (`mmdc` mit Edge über die Konfiguration des Baus):

| Fall | Exit | Umgebungsfehler erkannt |
|---|---|---|
| gültiger Block, mit Konfiguration | 0 | – |
| ungültiger Block, mit Konfiguration (*„Parse error on line 2“*) | 1 | nein – bleibt ein Fehler |
| gültiger Block, **ohne** Konfiguration (*„Could not find chrome-headless-shell“*) | 1 | ja |

`validate-framework.py --mermaid` am Stand `v1.9.3`: **8 Fehler**, einer je Mermaid-Block; neu:
**0**.

**`K-127`, am Bau gemessen:** `assemble.py --client openai-codex` – `v1.9.3` bettet
`.codex/config.toml` mit der Sprachangabe `json` ein, 1.949.844 Zeichen, die Kopfzeile des Packs
sechsmal; neu mit `toml`, 1.994.810 Zeichen, siebenmal (die Matrix in Kapitel 7a).

**`K-129` (1), gemessen mit Claude Code `2.1.282`** in einem Messbaum außerhalb des
Benutzerprofils: ein Elternverzeichnis mit einer `CLAUDE.md` (Kontrollmarke E), darunter ein
Projekt mit eigener `CLAUDE.md` (Marke P). Frage an die Sitzung: welche Marken in den
mitgegebenen Anweisungen stehen, ohne Werkzeug; je Lauf eine Runde, keine Abweisung.

| Lauf | Eintrag `claudeMdExcludes: ["**/cme/CLAUDE.md"]` | Antwort |
|---|---|---|
| A (Gegenlauf) | keiner | E, P |
| B | `.claude/settings.json` | P |
| C | `.claude/settings.local.json` | P |

**Installierte Laufzeitschicht.** Frischinstallationen aus `v1.9.3` und `1.10.0` je Pack
verglichen: Unterschiede nur in der Regelvorlage `21-overlay-TEMPLATE.md.template` (alle drei
Packs) und im Kommentar der erzeugten Berechtigungsdatei (`claude-code`, `devin-desktop`).
Wurzel-Anweisung, Regeln, Skills, Hooks, Agentenprofile byte-gleich.

## 3. Befund beim Bau

- **Die Empfehlung zu (g) stand gegen D-39.** Die Fehlerausgabe des Renderers zitiert den
  Diagrammtext; der Validator gibt sie deshalb bewusst nicht wieder. Umgesetzt ist die
  Unterscheidung nach Umgebungs- und Diagrammfehler ohne Wiedergabe (D-398).
- **Derselbe falsche Satz an zweiter Stelle.** *„mit keinem Overlaytext verglichen“* stand
  nicht nur im Kommentar von `clientmap.py` (`K-151` (5)), sondern auch in `03-security.md`;
  beide berichtigt (D-399).
- **`K-137` war zum Teil überholt:** Die vermisste Matrixzeile X2 steht in allen drei Packs.

## 4. Abnahme

| Lauf | Ergebnis |
|---|---|
| Validator | 0 Fehler, 0 Warnungen, beide Kodierungsumgebungen; mit `--mermaid` ebenfalls 0 Fehler, 0 Warnungen |
| Sondenlauf | **346** Einheiten (344 und die zwei neuen Bündel), alle bestanden, beide Kodierungsumgebungen zeilengleich (608 Zeilen), rund 670 s Wanduhr; Abnahmelauf gegen den fertigen Baum zeilengleich |
| Pilot / Übungsrepositorium | 1 Fehler, 2 Warnungen / 0 Fehler, 1 Warnung – unverändert gegen den Stand vor dem Heben; mit `install.py --target <projekt> --update` gehoben, 564 Kerndateien, dort committet. Beim Heben meldet `install.py` je Projekt eine aktualisierte Laufzeitdatei, die Regelvorlage 21 |
| Bau | `v1.10.0` 1.996.452 / 1.997.621 / 1.991.356 Bytes (`devin-desktop` / `claude-code` / `openai-codex`); Kapitel 31 nennt 564 versionierte Dateien, 8 Diagramme je Fassung; im Bau für `openai-codex` die Berechtigungsdatei als `toml`, die Matrix des Packs in Kapitel 7a |

## 5. Was offen bleibt

- `install.py` nennt die Vertrauensschritte, es prüft sie nicht (`K-118`).
- `K-138` bis `K-144`, `K-146`, `K-148` bis `K-150` für `1.11.0`; `K-147` für `1.12.0` (D-401), `K-152`
  ohne Ziel-Release.
- Die Abnahme des macOS-Starters auf macOS steht weiter aus.
