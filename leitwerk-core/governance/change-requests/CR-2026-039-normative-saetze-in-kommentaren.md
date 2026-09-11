# Änderungsantrag `CR-2026-039`

| Feld | Inhalt |
|---|---|
| Titel | Ein normativer Satz im Kopfkommentar der Wurzel-Anweisungsdatei erreicht die Sitzung nicht |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-11 |
| Betroffene Artefakte | `framework/runtime/root-instruction.md` (Kopfkommentar), `clients/claude-code/CLIENT_PACK.md` (Abschnitt zu K-18), `tests/scripts/validate-framework.py` (mögliche Prüfung 23), `governance/DECISION_LOG.md` (Klärungstabelle) |
| Ebene laut Entscheidungsbaum 6 | Kern – Laufzeitfassung der Wurzel-Anweisung |
| Art | Befund aus der Erhebung vom 2026-09-11 (ERH-01); **keine AP2-Kennung** |
| Dringlichkeit | regulär – die betroffene Zusage ist technisch anderweitig durchgesetzt (Abschnitt 4) |

## 1. Anlass und Problem

Die Wurzel-Anweisungsdatei beider Packs trägt denselben Kopfkommentar:

```html
<!-- Framework Core, Ebene 1. Version: siehe leitwerk-core/VERSION. Owner: <FRAMEWORK_OWNER>.
     Diese Datei ist projektneutral. Projektspezifische Werte stehen ausschließlich in
     project-overlay/OVERLAY.md und werden über <RULES_DIR>/20-project-overlay.md geladen.
     Diese Datei darf nur über den Änderungsprozess des Frameworks geändert werden. -->
```

Der letzte Satz ist eine **Anweisung**. Er steht in der Datei, die der Client zu Beginn jeder
Sitzung lädt, und liest sich wie jede andere Regel des Frameworks.

**Er erreicht die Sitzung nicht.**

### Die Messung

In einer frischen `claude-code`-Installation wurde dieselbe Messmarke zweimal gesetzt: einmal in
einem HTML-Kommentar, einmal als Klartextzeile – in der Wurzel-Anweisungsdatei **und** in einer
Datei der Regelablage.

| Fassung | Marke im Kontext? |
|---|---|
| `<!-- Messmarke … KENNSATZ-WURZEL-9915 -->` | **nein** |
| `Messmarke der Erhebung: KENNSATZ-KLARTEXT-5560` | **ja**, wörtlich wiedergegeben |

Dazu die Selbstauskunft derselben Sitzung, gefragt nach der letzten Zeile ihrer
Projektanweisung: Sie nannte den letzten **Absatz** des Fließtextes und fügte von sich aus hinzu,
das sei die letzte Zeile des *eingespeisten* Textes – ob die Datei auf der Platte weitergehe,
könne sie ohne Lesen nicht sagen.

**Der Client entfernt Kommentare, bevor er den Text einspeist.** Was im Kommentar steht, ist für
Menschen geschrieben, auch wenn es wie eine Anweisung klingt.

### Warum das trotz geringer Tragweite zählt

Es ist der Befundtyp, den dieses Projekt verfolgt – **eine Zusage, die mehr verspricht, als sie
leistet** –, und diesmal steht er im sichtbarsten Artefakt des Frameworks, in der ersten Datei,
die jede Sitzung lädt. Er ist nicht dadurch harmlos, dass er folgenlos blieb; er ist dadurch
harmlos, dass **eine andere Linie** ihn auffängt (Abschnitt 4).

### Der Zusammenhang mit K-18

`CR-2026-017` hat für `claude-code` entschieden, Zweck, Ladeverhalten und den Ladetrigger der
Kernquelle je Regeldatei in einen HTML-Kommentar zu schreiben – weil `description` für
Regeldateien dieses Clients nicht dokumentiert ist (K-18).

Das bleibt richtig, bekommt aber eine gemessene Kante: Bei `devin-desktop` steht die
Zweckbeschreibung im Frontmatter und geht bei einer modellentschiedenen Regel in die Auswahl ein;
bei `claude-code` steht sie im Kommentar und geht nirgends ein. **Dieselbe Regeldatei erklärt sich
dem Modell beim einen Client und nur dem Menschen beim anderen.** Praktisch trägt das wenig, weil
dieser Client alle Regeltexte unbedingt lädt – aber es war nicht gewollt und bis heute nicht
gemessen.

## 2. Vorgeschlagene Änderung

1. **Normative Sätze verlassen den Kommentar.** Der Satz über den Änderungsprozess gehört in den
   Fließtext der Wurzel-Anweisungsdatei – oder er entfällt, weil die Berechtigungsdatei ihn
   ohnehin durchsetzt (siehe E1). Was im Kommentar bleibt, ist Herkunft: Ebene, Version, Owner,
   Ladeverhalten.

2. **Der Kommentar wird als das ausgewiesen, was er ist.** In `clients/claude-code/CLIENT_PACK.md`
   erhält der Abschnitt zu K-18 einen Satz: Der Kommentar ist die Auskunft an den **Menschen**,
   der die Datei öffnet; in den Kontext geht er bei diesem Client nicht.

3. **Prüfung 23 (siehe E3):** In den Laufzeitartefakten des Kerns steht in einem HTML-Kommentar
   kein normatives Schlüsselwort (`MUSS`, `DARF NICHT`, `SOLL`, `nur über den Änderungsprozess`).
   Sonde nach D-23: ein solcher Satz in einer Kopie – die Prüfung meldet ihn.

4. **K-28 neu:** Entfernt auch `devin-desktop` HTML-Kommentare vor dem Einspeisen? Gemessen ist
   das nur für einen Client. Solange es offen ist, gilt die Annahme für beide – die strengere
   Lesart.

## 3. Was dieser Antrag nicht ändert

- **Die Entscheidung aus K-18.** Zweck und Ladeverhalten bleiben im Kommentar; sie sind Auskunft,
  keine Anweisung.
- **Die Regeltexte.** Kein Regelinhalt wird verschoben.
- **Die Wirkung der Regeln.** Alles, was im Fließtext steht, ist gemessen im Kontext – die
  Erhebung hat für vier Regeldateien und die Wurzel-Anweisung genau das bestätigt.

## 4. Grenze der Zusage

**Der betroffene Satz ist technisch durchgesetzt, nur eben nicht durch sich selbst.** Die
Berechtigungsdatei verweigert das Schreiben der Wurzel-Anweisungsdatei (`Write(AGENTS.md)`,
`Edit(CLAUDE.md)`), und der Schutz-Hook prüft denselben Pfad. Der Befund kostet keine Sperre – er
kostet die Verlässlichkeit der Aussage, dass in dieser Datei steht, was gilt.

**Gemessen ist ein Client.** Für `devin-desktop` ist es unbelegt (K-28).

**Gemessen sind zwei Dateiarten**, Wurzel-Anweisung und Regelablage. Für Skills und
Agentenprofile ist es nicht erhoben.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Satz in den Fließtext heben oder streichen? | **In den Fließtext.** Die technische Durchsetzung ersetzt die Aussage nicht: Wer die Datei öffnet, soll den Änderungsprozess finden, und das Modell soll ihn nennen können, statt nur abzuprallen | Die Wurzel-Anweisungsdatei wächst um einen Satz – in der Datei, für die das Framework selbst Least Context fordert |
| E2 | Auch die übrigen Kommentarinhalte verschieben? | **Nein.** Herkunft, Version und Ladeverhalten sind Auskunft an den Menschen und gehören nicht in den Kontext | Die Asymmetrie zwischen den Packs bleibt: Beim einen geht die Zweckbeschreibung in die Regelauswahl ein, beim anderen nicht |
| E3 | Prüfung 23 aufnehmen? | **Ja.** Sie ist billig, und sie trifft genau den Fehler, der hier unterlaufen ist | Eine Wortlistenprüfung meldet auch eine zutreffende Erwähnung im Kommentar – etwa einen Verweis auf eine Regel. Fehlalarme sind möglich |
| E4 | K-28 vor der Umsetzung erheben? | **Nein, danach.** Die Abhilfe ist für beide Packs dieselbe und in beiden Fällen richtig | Bis zur Messung bleibt offen, ob das Pack `devin-desktop` überhaupt betroffen ist |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | `<TBD: angenommen / abgelehnt / mit Auflagen>` |
| Datum | `<TBD>` |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | `<TBD: E1 bis E4 einzeln entscheiden>` |
