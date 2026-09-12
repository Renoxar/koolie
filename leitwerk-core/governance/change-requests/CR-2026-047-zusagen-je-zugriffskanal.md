# Änderungsantrag `CR-2026-047`

| Feld | Inhalt |
|---|---|
| Titel | Datei-, Such- und Netzsperren werden weiter zugesagt, als sie reichen – die Zusagen gehören nach Zugriffskanal aufgeteilt |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-12 |
| Betroffene Artefakte | `clients/claude-code/CLIENT_PACK.md` (B3, B4, B5, B8, `permissions_note` im Manifest), `clients/devin-desktop/CLIENT_PACK.md` (B3, B4, B5, B8), `clients/*/manifest.json` (`hook_tools`, `permission_tools`), `tests/scripts/hook-check-secrets.py` (Kommentar vor `PROTECTED_WRITE_PATH_PATTERNS`; bei Annahme von E3 auch die Prüflogik), `tests/scripts/probe-pruefungen.py` (bei Annahme von E3) |
| Ebene laut Entscheidungsbaum 6 | Client Pack – Fähigkeitsmatrix und Abbildung; der Kern bleibt unberührt |
| Art | Befund **B04** des unabhängigen Reviews vom 2026-09-12, P1; **gegengeprüft und gemessen** |
| Dringlichkeit | **vor der weiteren Nutzung im Pilotprojekt** – dort laufen echte Daten, und B3 bis B5 sind Kernzusagen nach D-41 |

## 1. Anlass und Problem

Vier Zeilen der Fähigkeitsmatrizen sagen einen Schutz pauschal und `[TECHNISCH]` zu:

- **B3** Secret-Dateien per Pfadmuster lesegeschützt (Kernzusage)
- **B4** Framework- und Overlay-Artefakte schreibgeschützt (Kernzusage)
- **B5** CI-, Quality-Gate- und Lockdateien schreibgeschützt (Kernzusage)
- **B8** Netzwerkzugriff standardmäßig unterbunden

**Keine dieser Zusagen gilt für alle Zugriffskanäle.** Sie gelten für die Kanäle, an denen sie
entstanden sind – direktes Lesen und direktes Schreiben –, und dort sind sie mehrfach gemessen.
Für Shell, Unterprozess und Suche gelten sie nicht.

### Gemessen, nicht nur gelesen

`tests/protocols/2026-09-12-B04-B05-gegenpruefung.md`: vierzehn synthetische Werkzeugeingaben
gegen den ausgelieferten Schutz-Hook, davon drei Positivkontrollen, dazu vier Abbildungsläufe
gegen `clientmap.py` für beide Packs. **Keine Abweichung vom Bericht des Reviews.**

| Kanal | B3 Lesesperre | B4/B5 Schreibsperre | B8 Netzsperre |
|---|---|---|---|
| direktes Lesen | **wirkt** | – | – |
| direktes Schreiben | – | **wirkt** | – |
| Shell | **wirkt** (Tokenisierung) | **fällt aus** | **teilweise** – vier Programme gesperrt |
| Unterprozess | nicht geprüft | **fällt aus** – der Befehlstext nennt den Pfad nicht | **fällt aus** |
| Suche | **fällt aus** | nicht anwendbar | – |
| Abrufwerkzeuge | – | – | **wirkt** |

### Die Kette reißt zwischen zwei Schichten, die aufeinander zeigen

Der Schutz-Hook prüft das Schreibverbot auf das Kernverzeichnis nur für schreibende Werkzeuge.
Der Kommentar darüber begründet das ausdrücklich: „bei exec trägt die deny-Regel der
Berechtigungsdatei". **Die Berechtigungsdatei enthält für `exec` keine einzige Pfadregel** – 21
Verweigerungen, sämtlich Befehlsverbote (`git push`, `rm -rf`, `sudo`, `curl`, `wget`, …).
Umgekehrt verlässt sich die Berechtigungsdatei für Shell-Schreibwege auf den Hook. Was den
Shell-Schreibweg in den Kern tatsächlich aufhält, ist die Regelschicht – also Modellverhalten,
und damit `[TEXTUELL]`.

Das ist der wiederkehrende Befundtyp dieses Projekts, diesmal als **Verweis zwischen zwei
Schichten, die beide auf die andere zeigen**.

### Der Suchkanal ist nicht bloß unbewacht, er ist derzeit nicht bewachbar

`permission_tools.search` ist bei **beiden** Packs die leere Liste, und `hook_tools` kennt kein
Suchverb. Eine synthetische Regel `{"tool": "search", "pattern": "**/.env"}` bricht deshalb in
`clientmap._regel_rendern()` bei beiden Packs mit `AbbildungsFehler` ab – „das wäre eine
Lockerung".

**Das Verhalten der Abbildung ist richtig** und genau das, was D-18 verlangt. Die Folge ist
trotzdem hart: Solange kein Suchwerkzeug im Manifest steht, kann niemand eine Suchsperre
aussprechen. **Das berührt D-30 unmittelbar** – dort ist entschieden, dass Secret-Pfade auch
gegen lesende Werkzeuge durchgesetzt werden. Für das Suchwerkzeug ist das nicht eingelöst;
dieselbe Lücke wie `AP2-DD-11`, ein Werkzeug weiter.

Nebenbefund: Der `permissions_note` des Packs `claude-code` sagt weiterhin, `search` bilde „auf
Grep" ab. Das beschreibt einen Stand, den das Manifest seit `CR-2026-016` nicht mehr trägt.

## 2. Vorgeschlagene Änderung

1. **Die Zeilen B3, B4, B5 und B8 beider Packs werden nach Zugriffskanal aufgeteilt.** Je Kanal
   steht eine der drei Angaben: **wirkt** (mit Beleg), **nicht nachgewiesen**, **nicht
   verfügbar**. Die Einstufung `[TECHNISCH]` gilt nur noch für die Kanäle, für die sie gemessen
   ist; die übrigen tragen `[TEXTUELL]` mit Nennung der tragenden Regelstelle.
2. **Die bereits gemessenen Sperren werden ausdrücklich anerkannt**, nicht nur die Lücken
   benannt. B3 gegen das Lesewerkzeug und gegen den Shell-Befehl hält auch im untersagten
   Betriebsmodus – das ist am 2026-09-12 in drei Läufen mit Kontrolllauf belegt.
3. **Der Kommentar im Schutz-Hook wird berichtigt.** Er darf keine Sperre als Träger benennen,
   die die Berechtigungsdatei nicht enthält.
4. **Der `permissions_note` des Packs `claude-code` wird berichtigt** – `search` bildet auf
   nichts ab, und der Grund dafür (`AP2-CC-02`) gehört in denselben Satz.
5. **Keine Ausweitung der Befehlsverbote.** Das Review warnt ausdrücklich davor, die Sperre auf
   immer mehr Shell-Schreibweisen auszudehnen und daraus Vollständigkeit abzuleiten. Der Antrag
   folgt dem.

## 3. Was dieser Antrag nicht ändert

- **Er baut keine technische Durchsetzung für Shell und Unterprozess.** Dafür braucht es eine
  Isolationsschicht des Betriebssystems; ihre Verfügbarkeit unter Windows ist unerhoben (das
  Review nennt macOS, Linux und WSL2). Das ist Paket 6 und braucht eine eigene Erhebung.
- **Er ändert nichts an den Regeltexten.** Die Regelschicht wirkt; sie wirkt nur `[TEXTUELL]`.
- **Er entscheidet B06 nicht mit** (Eingabeschema und Pfadidentität des Hooks). B06 härtet den
  Hook; dieser Antrag korrigiert, was über ihn behauptet wird.
- **Er berührt M4/M5 nicht** – das ist `CR-2026-048`.

## 4. Prüffragen

- [x] Richtige Ebene: Client Pack. Die Zusage ist werkzeugneutral, ihre Reichweite ist es nicht.
- [x] Verschärfungsprinzip: Der Antrag lockert keine Regel. Er senkt eine **Einstufung** auf den
      gemessenen Stand – das ist keine Lockerung des Schutzes, sondern das Ende einer
      unzutreffenden Behauptung über ihn.
- [x] Widerspruchsfreiheit: D-18 (keine stille Lockerung in der Abbildung), D-30 (Secret-Pfade
      auch gegen lesende Werkzeuge), D-35 (`[TECHNISCH]` ist betriebsmodusabhängig), D-41
      (Kernzusage) gelesen. **D-30 ist für den Suchkanal nicht eingelöst** – siehe E3.
- [x] Laufzeitfassungen: bei E3 „nur Ausweis" nicht betroffen; bei E3 „Hook-Eintrag" ist die
      Hook-Konfiguration beider Packs betroffen und in beiden zu synchronisieren.
- [x] Belegstatus: **gemessen**, vierzehn Läufe mit drei Positivkontrollen.
- [ ] Test- und Validierungsbedarf: bei E3 „Hook-Eintrag" **neue Sonde und Gegenprobe nach
      D-23**, je Pack. Der reine Ausweis ist eine Textkorrektur ohne neue Prüfung.
- [x] Overlays: nicht betroffen. Kein Projekt fällt durch diese Änderung durch.
- [ ] Dokumentation: CHANGELOG, Decision Log, `docs/ROADMAP.md` (Paket 3).

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Aufteilung je Kanal **in der Matrixzeile** oder als Vorbemerkung je Block? | **In der Zeile.** Die Vorbemerkung trägt bereits zwei Bedingungen (Betriebsmodus nach D-35, und der Startort steht noch aus). Eine dritte macht sie zur Fußnotensammlung, und wer eine Zeile liest, liest die Vorbemerkung nicht | Die vier Zeilen werden deutlich länger. Die Matrix verliert an Überblick, was sie an Ehrlichkeit gewinnt |
| E2 | Welche Einstufung tragen Shell und Unterprozess bei B4/B5 künftig? | **`[TEXTUELL]`**, nicht `[NICHT ABBILDBAR]`. Eine Regel existiert und wirkt – über das Modellverhalten. `[NICHT ABBILDBAR]` hieße, es gebe nichts, und würde zudem nach Prüfung 25 einen benannten Ersatz verlangen, den es in Gestalt der Regelschicht gerade gibt | **B4 und B5 sind Kernzusagen** (`core: true`). Eine Kernzusage, die für einen Kanal nur noch `[TEXTUELL]` ist, ist eine ernste Aussage über das Framework – und genau deshalb gehört sie vorgelegt und nicht redaktionell entschieden |
| E3 | **Der Suchkanal: nur ausweisen, oder schließen?** | **Vorschlag: Hook-Eintrag ja, Berechtigungsregel nein.** Ein `hook_tools`-Suchverb schließt die Lücke echt – der Hook misst das Suchwerkzeug dann wie ein lesendes an den Secret-Pfaden und löst D-30 ein. Eine Pfadregel in der Berechtigungsdatei brächte bei `claude-code` dagegen nichts: Dieser Client wertet Pfadregeln nur für zwei Werkzeuge aus, alles andere wird angenommen, nie konsultiert und beim Sitzungsstart als Warnung gemeldet (`AP2-CC-02`). Genau solche Regeln hat `CR-2026-016` entfernt | **Das ist Code, nicht Text** – und damit die einzige Stelle, an der dieser Antrag über eine Korrektur hinausgeht. Er braucht eine Sonde und eine Gegenprobe je Pack (D-23) und ist damit spürbar teurer. **Die Gegenposition ist vertretbar:** den Kanal nur ausweisen und das Schließen zu B06 in Paket 6 legen. Dann bleibt eine Kernzusage für einen Kanal offen, der gemessen offen ist |
| E4 | B8: die Befehlsliste um weitere Netzprogramme ergänzen? | **Nein.** Jedes ergänzte Programm suggeriert Vollständigkeit, die es nicht gibt – `python`, `node`, `git`, die Bordmittel der Shell und jedes selbst geschriebene Skript bleiben. Das Review warnt davor ausdrücklich | B8 sinkt für den Shell-Kanal auf `[TEXTUELL]` und bleibt dort, bis eine Isolationsschicht erhoben ist. Wer eine vollständige Netzsperre braucht, betreibt den Agenten ohne automatische Befehlsausführung |
| E5 | Die Betriebssystem-Sandbox jetzt erheben? | **Nein, nicht in diesem Antrag.** Sie ist der einzige Weg zu einer echten Zusage für Shell und Unterprozess, aber ihre Reichweite unter Windows ist unbekannt, und eine ungemessene Sandbox-Empfehlung wäre derselbe Fehler eine Ebene höher | Die technische Durchsetzung bleibt offen und wandert als eigener Gegenstand nach Paket 6. Der Antrag macht die Lage ehrlich, nicht sicher |
| E6 | Wie wird die Wirkung nachgewiesen? | **Der Ausweis ist eine Textkorrektur und braucht keine Sonde** – er behauptet keine Prüfung. **Wird E3 mit „Hook-Eintrag" entschieden, gilt D-23 voll:** eine Sonde je Pack, die ein Suchwerkzeug auf einen Secret-Pfad schickt, plus Gegenprobe | Ohne E3 bleibt dieser Antrag ohne neuen Wirkungsnachweis – ungewohnt für dieses Projekt, aber richtig: Eine Prüfung, die nichts prüft, wäre schlechter als keine |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle sechs Fragen wie vorgelegt.** E1 die Aufteilung steht in der Matrixzeile; E2 Shell und Unterprozess tragen bei B4/B5 `[TEXTUELL]`; E3 **der Suchkanal wird geschlossen – Hook-Eintrag ja, Berechtigungsregel nein**; E4 die Befehlsliste von B8 wird nicht verlängert; E5 die Betriebssystem-Sandbox bleibt einer eigenen Erhebung; E6 der Ausweis braucht keine Sonde, der Hook-Eintrag schon |
| Datum | 2026-09-12 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | **E3 war die einzige Frage, die über eine Textkorrektur hinausgeht, und sie hat eine zweite aufgeworfen:** Ein Pack ohne Suchwerkzeug kann keines abbilden, und eine leere Liste galt bisher als Abbildungsfehler. Die Abwesenheit wird deshalb **deklariert statt erraten** – `hook_tools_absent` im Manifest, mit Begleitsatz. Weil das ein Schlupfloch wäre, wenn jemand dort `write` einträge, prüft **Prüfung 26** beides: dass ein so erklärtes Verb auch in `permission_tools` leer ist und dass der Begleitsatz existiert. **Nachgewiesen:** zwei Sonden und eine Gegenprobe für Prüfung 26, zwei Sonden und zwei Gegenproben für den Suchkanal am Hook. **Die Gegenproben sind hier der wichtigere Teil** – ein Hook, der jede Suche blockiert, bestünde jede Sonde und machte das Suchwerkzeug unbenutzbar. **Offen bleibt E5:** Die technische Durchsetzung für Shell und Unterprozess braucht eine Isolationsschicht des Betriebssystems und ist unerhoben; sie steht als eigener Gegenstand in Paket 6 |
| Umsetzung | umgesetzt mit `0.30.0` |
