# Änderungsantrag `CR-2026-036`

| Feld | Inhalt |
|---|---|
| Titel | Drei Dokumentstellen nennen weiter den Ort der Hook-Konfiguration, den D-32 abgelöst hat – und nichts vergleicht sie mit dem Manifest |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-11 |
| Betroffene Artefakte | `clients/devin-desktop/root-template/.devin/README.md` (Zeile 12), `docs/PLACEHOLDER_REGISTRY.md` (Zeile 38), `docs/RUNTIME_GLOSSARY.md` (Zeile 34), `tests/scripts/validate-framework.py` (neue Prüfung 20) |
| Ebene laut Entscheidungsbaum 6 | Kern – Dokumentation der Abbildung und Validator |
| Art | Behebung eines Befundes aus der Antragsarbeit zu `AP2-DD-15`/`-16` (Sitzung 2026-09-11); **keine AP2-Kennung** |
| Dringlichkeit | regulär; die erste Stelle wird jedoch in jede Installation ausgeliefert |

## 1. Anlass und Problem

D-32 hat mit 0.25.0 entschieden: Die Hook-Konfiguration des Packs `devin-desktop` steht in der
Berechtigungsdatei unter `hooks`; **eine eigene Hook-Datei wird nicht mehr erzeugt.** Prüfung 18
meldet eine zurückgebliebene `hooks.v1.json` aus einer früheren Installation als Warnung.

Drei Stellen im Kern sagen weiterhin das Gegenteil:

| Stelle | Aussage |
|---|---|
| `clients/devin-desktop/root-template/.devin/README.md:12` | listet `hooks.v1.json` unter den ausgelieferten Dateien: „Lebenszyklus-Hooks … Erzeugt aus `leitwerk-core/framework/runtime/hooks.json`" |
| `docs/PLACEHOLDER_REGISTRY.md:38` | `<HOOKS_FILE>` = `.devin/hooks.v1.json` |
| `docs/RUNTIME_GLOSSARY.md:34` | Hook-Konfiguration = `.devin/hooks.v1.json` |

**Das Manifest ist richtig:** `runtime_placeholders["<HOOKS_FILE>"]` steht auf `.devin/config.json`,
und `clientmap.py` wie `validate-framework.py` lesen es von dort. Die Abweichung liegt also
nicht zwischen Dokument und Wirklichkeit, sondern **zwischen der maschinenlesbaren Quelle und
ihrer menschenlesbaren Fassung** – und nichts vergleicht die beiden.

### Die erste Stelle wird ausgeliefert

`.devin/README.md` steht in `core_paths` des Manifests. Sie landet bei jeder Installation im
Projekt und wird von `install.py --update` erneuert. Dort beschreibt sie seit 0.25.0 eine Datei,
die die Installation **nicht anlegt** – und deren Vorhandensein Prüfung 18 als Rest einer
früheren Installation meldet.

**Ein ausgeliefertes Dokument beschreibt damit genau den Zustand, den eine Prüfung desselben
Releases als Altlast anzeigt.**

### Der Befundtyp ist bekannt

Eine Aussage, die ihren Gegenstand überlebt hat. Dasselbe Muster wie in 0.23.0, als der
Steuerungsabschnitt der Roadmap zwei Releases lang einen Befund als offen führte, den das
Protokoll als behoben auswies. Gefunden hat es beide Male das Lesen, nicht eine Prüfung – hier
beim Zusammentragen der Belegstellen für `CR-2026-031`.

## 2. Vorgeschlagene Änderung

1. **Die drei Stellen nachziehen.** In der Laufzeit-README tritt an die Stelle der Zeile zu
   `hooks.v1.json` ein Zusatz in der Zeile zu `config.json`: Die Datei trägt Berechtigungen
   **und** Hooks; der Ort folgt D-32. Registrierungstabelle und Glossar nennen
   `.devin/config.json`.

2. **Prüfung 20 vergleicht Tabelle und Manifest.** Die Client-Spalten von
   `PLACEHOLDER_REGISTRY.md` und `RUNTIME_GLOSSARY.md` werden je Pack gegen dessen
   `manifest.json` geprüft – Wert für Wert, für jeden Begriff mit Manifestentsprechung
   (Laufzeitschicht, Berechtigungsdatei, Regelablage, Skill-Ablage, Agentenprofile,
   Wurzel-Anweisungsdatei, Hook-Konfiguration, MCP-Konfiguration).

   Sonde nach D-23: Ein Wert wird in einer Kopie verfälscht – die Prüfung meldet ihn.
   Gegenprobe: Ein Begriff **ohne** Manifestfeld („Nutzerlokale Überschreibung") bleibt
   unbeanstandet, und ein Pack ohne eigene Hook-Datei (`<HOOKS_FILE>` gleich
   `<PERMISSIONS_FILE>`) gilt als übereinstimmend, nicht als Fehler.

3. **Migrationshinweis.** Eine bestehende Installation behält ihre `hooks.v1.json`, bis jemand
   sie löscht. Prüfung 18 meldet sie; der Hinweis nennt den Handgriff ausdrücklich.

## 3. Was dieser Antrag nicht ändert

- **D-32 und die Abbildung.** Beide sind richtig und bleiben unverändert; korrigiert wird, was
  über sie geschrieben steht.
- **Die Manifeste.** Sie führen den richtigen Wert. Dieser Antrag macht die Dokumentation an sie
  anschlussfähig, nicht umgekehrt.
- **Prüfung 18.** Sie bleibt, wie sie ist – zur möglichen Erweiterung siehe E3.

## 4. Grenze der Zusage

**Prüfung 20 prüft Übereinstimmung, nicht Richtigkeit.** Steht im Manifest ein falscher Pfad,
sind Tabelle und Manifest danach einig – und beide falsch. Was den Manifestwert prüft, ist die
Installation selbst und der Nachweis an ihr (D-23, AP2).

**Sie deckt nur Zeilen mit Manifestentsprechung ab.** Begriffe ohne Feld – nutzerlokale
Überschreibung, künftige Ergänzungen – bleiben ungeprüft und altern weiter still.

**Sie hätte diesen Befund gefunden, nicht aber die README.** Die Laufzeit-README nennt Dateinamen
in Fließtext, kein Platzhalterfeld; dafür braucht es E3 oder weiterhin das Lesen.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Die drei Stellen nachziehen? | **Ja**, ohne Vorbehalt. Eine davon wird ausgeliefert | Keiner, außer der Migration einer zurückgebliebenen Datei |
| E2 | Prüfung 20 aufnehmen? | **Ja.** Sie schließt die Naht zwischen Manifest und Dokumenttabellen – die Naht, an der dieser Befund entstanden ist | Sie bindet zwei Dokumenttabellen an das Manifestformat: Ändert sich das Format, ist die Prüfung mitzuändern |
| E3 | Prüfung 18 um die Vorlagen erweitern (kein verwaister Hook-Dateiname in einem `root-template`)? | **Ja.** Die Liste der verwaisten Dateinamen steht bereits im Validator; sie auch gegen die ausgelieferten READMEs zu halten, kostet wenige Zeilen | Eine Prüfung auf Dateinamen im Fließtext meldet auch eine Nennung, die den Ort erklärt statt ihn zu behaupten. Ein Fehlalarm ist möglich |
| E4 | Eigener Antrag oder Nachtrag zu `CR-2026-029`? | **Eigener Antrag.** `CR-2026-029` ist entschieden und umgesetzt; ein umgesetzter Antrag wird nicht nachträglich erweitert | Die Ursache steht in einem Antrag, ihre Folgen in einem zweiten. Der Verweis muss die Verbindung tragen |
| E5 | Den Befund als AP2-Befund führen? | **Nein.** Er stammt nicht aus einem AP2-Lauf, sondern aus der Antragsarbeit dieser Sitzung. Der Antrag selbst ist der Nachweis | Die Befundzählung des AP2-Protokolls bleibt bei 17 und erfasst damit nicht alles, was in seinem Umfeld gefunden wurde |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** |
| Datum | 2026-09-11 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | E1 bis E5 wie vorgelegt: Die drei Stellen werden nachgezogen; Prüfung 20 hält die Client-Spalten von `PLACEHOLDER_REGISTRY.md` und `RUNTIME_GLOSSARY.md` je Pack gegen das Manifest; Prüfung 18 wird auf die `root-template`-Vorlagen ausgedehnt; eigener Antrag statt Nachtrag zu `CR-2026-029`; **keine** AP2-Kennung. Ziel-Release 0.26.0 |
| Umsetzung | **mit Release 0.26.0** – Einzelheiten und Nachweise in `leitwerk-core/CHANGELOG.md` |
