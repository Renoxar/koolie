# Änderungsantrag `CR-2026-027`

| Feld | Inhalt |
|---|---|
| Titel | R4 stuft ein Zeichenlimit als technisch durchgesetzt ein, das für diesen Client nicht dokumentiert ist |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-11 |
| Betroffene Artefakte | `clients/devin-desktop/CLIENT_PACK.md` (Zeile R4), `build/doc/31-anhaenge.md` (V1, QD-7), ggf. `docs/ROADMAP.md` |
| Ebene laut Entscheidungsbaum 6 | Client Pack – Belegstatus einer Zusage; keine Regeländerung |
| Art | Behebung von `AP2-DD-02` (Schwere: mittel) |
| Dringlichkeit | regulär – die Einstufung behauptet eine Schranke, sie schafft keine |

## 1. Anlass und Problem

Die Fähigkeitsmatrix des Packs `devin-desktop` führt:

```text
| R4 | Bekanntes Zeichenlimit | 12.000 je Workspace-Regel, 6.000 global | [TECHNISCH]
     | [DOK] für Cascade; für Devin Local <VERIFY AGAINST CURRENT DEVIN DOCUMENTATION> (K-19) |
```

**Die Belegspalte sagt, was fehlt – die Einstufungsspalte sagt es nicht.** `[TECHNISCH]`
bedeutet nach der Legende des Packs, dass der Client die Zusage durchsetzt. Belegt ist
die Zahl aber nur für **Cascade**, das seit dem Rebrand vom 02.06.2026 von Devin Local
abgelöst wird (QD-1).

**Der Abgleich vom 11.09.2026 gegen Devin Desktop 3.9.19** (`cli/extensibility/rules`)
ergibt: Die aktuelle Regeldokumentation nennt **keinerlei Zeichen- oder Größengrenze**
für Regeldateien – weder für `AGENTS.md` noch für `.devin/rules/*.md` noch für globale
Regeln.

Damit steht die Zeile auf einer Quelle zu einem Vorgängerprodukt, während die Einstufung
eine Durchsetzung im aktuellen behauptet.

### Warum das mehr ist als eine Formalie

Die Zahl ist nicht folgenlos. Sie steht im Größenbudget der Wurzel-Anweisungsdatei, in
`.devin/rules/README.md` und in den Grenzen des Validators. **Ein Projekt, das seine
Regeltexte an 12.000 Zeichen ausrichtet, richtet sich an einer Grenze aus, die für
seinen Client nicht dokumentiert ist** – und hält womöglich eine ein, die es nicht gibt,
oder überschreitet eine, die anders liegt.

Der Befundtyp ist derselbe wie bei `AP2-CC-13` und `FW-KO-01`: **Geprüft war die
Herkunft der Angabe, nie ihre Geltung.** Bei `AP2-CC-13` war der Interpretername
vorhanden und startete kein Python; hier ist die Quelle vorhanden und gilt für ein
anderes Produkt.

## 2. Vorgeschlagene Änderung

**Einstufung auf `[TEXTUELL]`.** Die Zeile beschreibt dann, was sie ist: eine
Budgetannahme des Frameworks, für die beim aktuellen Client keine Herstellerzusage
vorliegt.

**V1 auflösen statt offen tragen.** Der Verifikationsbedarf V1 lautet „Zeichenlimits für
Regeldateien unter Devin Local (dokumentiert bislang für Cascade-Regeln: 6.000/12.000)".
Er ist mit dieser Recherche **beantwortet** – die Antwort lautet „nicht dokumentiert".

Ein Prüfpunkt, dessen Recherche ergeben hat, dass es nichts zu belegen gibt, bleibt
nicht offen; er wird mit dem Ergebnis geschlossen. Sonst wird er beim nächsten Durchgang
erneut recherchiert, und niemand weiß, dass die Antwort schon vorliegt. Dieselbe
Überlegung wie beim Abwesenheitsbeleg X2 bei `claude-code`: **Dass etwas nicht
dokumentiert ist, ist ein Ergebnis, kein fehlendes Ergebnis.**

**Die Zahlen bleiben stehen, als das, was sie sind.** Das Framework braucht ein Budget –
ohne Obergrenze wächst die always-on-Summe unbemerkt (V10). Der Vorschlag ist nicht, die
Zahl zu streichen, sondern sie als **eigene Vorgabe** zu führen statt als
Produkteigenschaft.

## 3. Was dieser Antrag nicht ändert

- **Das Budget selbst.** 12.000/6.000 bleiben als Framework-Vorgabe in Kraft, und der
  Validator prüft weiter dagegen. Eine selbstgesetzte Grenze ist eine Grenze.
- **K-19.** Die Klärungsfrage bleibt bestehen; beantwortet ist nur, dass der Hersteller
  sie derzeit nicht beantwortet.
- **Andere Packs.** Bei `claude-code` sind die dokumentierten Grenzen andere (4 MiB je
  Anweisungsdatei, Empfehlung 200 Zeilen) und mit QC-1 belegt.

## 4. Grenze der Zusage

**Eine nicht dokumentierte Grenze ist keine nicht existierende Grenze.** Möglich bleibt,
dass Devin Local intern kürzt oder verwirft, ohne es zu dokumentieren. Genau deshalb
lautet der Vorschlag `[TEXTUELL]` und nicht „Zeile streichen": Das Framework hält sein
Budget ein, verlässt sich aber nicht darauf, dass der Client es durchsetzt.

Ob eine überlange Regeldatei in der Praxis noch vollständig geladen wird, ließe sich
beobachten – das wäre ein eigener Sitzungsnachweis und ist **nicht** Gegenstand dieses
Antrags.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Einstufung `[TECHNISCH]` oder `[TEXTUELL]`? | **`[TEXTUELL]`.** Für diesen Client liegt keine Herstellerzusage vor | Das Pack weist eine technische Zusage weniger aus – ehrlicher, aber die Matrix wird schwächer |
| E2 | V1 schließen oder offen lassen? | **Schließen, mit dem Ergebnis „nicht dokumentiert"** samt Datum und Clientversion | Wird die Grenze später doch dokumentiert, ist V1 erneut zu öffnen |
| E3 | Die Zahlen 12.000/6.000 behalten? | **Ja, als Vorgabe des Frameworks.** Ohne Obergrenze wächst die always-on-Summe unbemerkt | Eine selbstgesetzte Zahl ohne äußere Begründung – sie ist als solche zu kennzeichnen |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** |
| Datum | 2026-09-11 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | E1 bis E3 wie vorgelegt: Einstufung R4 auf `[TEXTUELL]`; V1 wird mit dem Ergebnis „nicht dokumentiert“ samt Datum und Clientversion geschlossen; die Zahlen 12.000/6.000 bleiben als **ausgewiesene Vorgabe des Frameworks** erhalten. Ziel-Release 0.26.0 |
| Umsetzung | **mit Release 0.26.0** – Einzelheiten und Nachweise in `leitwerk-core/CHANGELOG.md` |
