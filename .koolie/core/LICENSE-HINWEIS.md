# Lizenzhinweis

| Attribut | Wert |
|---|---|
| ID | `FW-GOV-LIC` |
| Version | `0.2.1` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Gilt für | den gesamten Inhalt dieses Frameworks – Kern, Client Packs, Regeltexte, Werkzeuge, Vorlagen und Dokumentation |
| Entstehung | `CR-2026-126`, **D-316** bis **D-317** (2026-09-23); Rechteinhaber benannt mit `CR-2026-128`, **D-323** |

## 1. Lizenz (normativ)

**Dieses Framework steht unter der GNU General Public License, Version 3** (`LICENSE`,
wörtlicher Text der Free Software Foundation). Es ist damit **freie Software im Sinne der
Open-Source-Definition** – jede und jeder darf es nutzen, untersuchen, ändern und
weitergeben.

Copyright © 2026 René Hildebrand

> 🔴 **Diese eine Zeile nennt eine Person, und sie ist die einzige im ganzen Kern, die
> das tut** (D-323, `CR-2026-128` E7). Überall sonst gilt die Projektneutralität: Rollen
> statt Personen, Platzhalter statt Namen. **Hier gilt sie nicht, und der Grund ist
> keine Ausnahme vom Prinzip, sondern seine Grenze.** Die Neutralitätsregel hält
> **fremde** Personen aus generischen Bestandteilen – Kunden, Behörden, Kolleginnen und
> Kollegen. Der **Urheber des Werks** ist keine fremde Person: Ohne ihn hat die Lizenz
> keinen Zusagenden, die Zusatzerlaubnis aus Abschnitt 2 niemanden, der sie erteilt, und
> §7 GPL-3.0 keine Rechtsgrundlage.
>
> ⚠️ **Der Preis ist benannt:** Der Name wandert mit jeder Kopie des Kerns in jedes
> übernehmende Projekt. ⚠️ **Und der Widerspruch, der ihn nötig machte, ist gemessen:**
> Die Historie dieses Repositoriums führt denselben Namen in **122 Commits** und die
> Adresse in allen **261** – *er stand dort, wo er niemandem nützt, und fehlte dort, wo
> er rechtlich wirkt* (D-324).

> Dieses Programm ist freie Software: Sie können es unter den Bedingungen der GNU General
> Public License, Version 3, weitergeben und/oder verändern. Es wird **ohne jede
> Gewährleistung** bereitgestellt, sogar ohne die implizite Gewährleistung der
> Marktgängigkeit oder der Eignung für einen bestimmten Zweck. Einzelheiten stehen in der
> GNU General Public License.

**Die Lizenzdatei liegt an zwei Stellen und trägt an beiden denselben Inhalt:** in der
Wurzel des Repositoriums (`LICENSE`, dort finden sie die Hostingdienste) und im Kern
(`<CORE_DIR>/LICENSE`, dort **wandert sie mit** – ein übernehmendes Projekt kopiert den Kern
als Ganzes, und ein Werk ohne seine Lizenz weiterzugeben ist nach §4 GPL-3.0 unzulässig).
🔴 **Prüfung 79 hält beide Dateien gegeneinander** – *zwei Stellen mit demselben Inhalt
laufen auseinander, wenn niemand nachzählt; das ist in diesem Repositorium der häufigste
Befundtyp.*

## 2. Zusätzliche Erlaubnis nach §7 GPL-3.0 (normativ)

> **Dateien, die aus den mitgelieferten Vorlagen dieses Frameworks entstehen, und jede
> Ausgabe seiner Werkzeuge unterliegen nicht dieser Lizenz.** Das Urheberrecht daran liegt
> bei dem Projekt, das sie erzeugt hat; es darf sie unter beliebigen Bedingungen
> weitergeben oder für sich behalten.

**Gemeint sind ausdrücklich:** das ausgefüllte Project Overlay
(`.koolie/project-overlay/OVERLAY.md`), aus `*.template` erzeugte Regel- und
Technology-Pack-Dateien, die von `install.py` erzeugte Laufzeitschicht, Ergebnisberichte,
Protokolle und jede sonstige Ausgabe eines Werkzeugs dieses Frameworks.

🔴 **Warum diese Erlaubnis dasteht, und sie ist kein Schmuck.** Ohne sie wäre ein
ausgefülltes Overlay formal eine *geänderte Fassung* eines GPL-Werks – ein Ergebnis, das
niemand beabsichtigt und das eine Rechtsabteilung zu Recht aufhält. ➡️ *Dieses Framework
benennt Preise, statt sie zu verschweigen; eine Lizenzkante gehört genauso benannt wie eine
Prüfungsgrenze.*

## 3. Was die Lizenz für ein übernehmendes Projekt bedeutet (Erläuterung)

**Die GPL bindet die Weitergabe, nicht die Nutzung.** Solange ein Projekt dieses Framework
nur benutzt, entsteht keine einzige Pflicht.

| Lage | Folge |
|---|---|
| Der Kern wird in ein Projekt kopiert und dort benutzt – auch in einem Unternehmen, auch für ein kommerzielles Produkt | **keine Pflicht.** Es wird nichts weitergegeben |
| Mit dem Framework wird ein Produkt entwickelt und verkauft | **keine Pflicht.** Das Produkt ist keine Ableitung: Es enthält keine Zeile dieses Frameworks, und die Ausgabe eines Werkzeugs ist keine Ableitung des Werkzeugs (Abschnitt 2) |
| Das Projektrepositorium wird veröffentlicht, mit `<CORE_DIR>/` darin | `<CORE_DIR>/` steht unter GPL-3.0 – **es steht ohnehin schon so da.** Der eigene Code daneben bleibt frei: §5 GPL-3.0 nennt das ein *aggregate*, und ein gemeinsames Repositorium ist genau das |
| Code dieses Frameworks wird **in** ein Produkt hineinkopiert | Dieser Teil wird GPL-3.0. **Das ist gewollt** und der einzige Fall, in dem die Lizenz greift |
| Das Framework selbst wird weitergegeben, entgeltlich oder unentgeltlich | Es muss unter GPL-3.0 weitergegeben werden, mit Quelltext. **Ein Umbenennen-und-proprietär-Verkaufen ist damit ausgeschlossen** – das war der tragende Grund der Lizenzwahl (D-316) |

## 4. Die verworfenen Alternativen (Erläuterung)

Beides ist in `CR-2026-126` Abschnitt 4 einzeln vorgelegt und in D-316 entschieden:

- **Apache-2.0** – verworfen: Sie erlaubt ausdrücklich, das Werk umzubenennen, zu schließen
  und zu verkaufen. Ihr einziger Riegel ist §6, und der schützt den **Namen**, nicht die
  Sache.
- **BUSL-1.1** – verworfen: Sie trifft die Absicht wörtlich, ist aber **kein
  OSI-Open-Source**. Der Zweck dieses Frameworks ist die Übernahme in Unternehmen, und eine
  Lizenz, die eine Rechtsabteilung als proprietär einstuft, kostet genau dort.

⚠️ **Der Preis der gewählten Lizenz ist benannt:** Manche Organisationen führen pauschale
GPL-Verbote. Abschnitt 3 und die Zusatzerlaubnis aus Abschnitt 2 sind die Antwort darauf –
sie machen nachlesbar, dass für einen Anwender dieses Frameworks **keine** Pflicht entsteht.
