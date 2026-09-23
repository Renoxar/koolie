# Änderungsantrag `CR-2026-129`

| Feld | Inhalt |
|---|---|
| Titel | Die Zeilenenden des Archivs – eine Zusage, die ihr eigenes Werkzeug nicht hält |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-23 |
| Betroffene Artefakte | `.koolie/core/governance/RELEASE_PROCESS.md` (Abschnitt 4.1); `.koolie/core/governance/DECISION_LOG.md` (**D-328**, D-320 berichtigt); `.koolie/core/VERSION`; `.koolie/core/CHANGELOG.md`; `.koolie/core/docs/ROADMAP.md`; `.koolie/core/build/doc/00-kopf.md`, `26-qs-test.md`; `UEBERGABE.md` |
| Ebene laut Entscheidungsbaum 6 | Governance |
| Art | **Korrektur.** Patch-Release nach `RELEASE_PROCESS.md` Abschnitt 1 |
| Dringlichkeit | hoch – die falsche Zusage steht im ausgelieferten `1.0.0` **und in dessen Archiv** |
| Status | 🟢 **entschieden am 2026-09-23** (E1 bis E3), umgesetzt mit `1.0.1` |

---

## 1. Anlass

**Das erste Release-Archiv, das dieses Projekt je erzeugt hat, hat die Regel widerlegt,
die es erzeugen ließ.** Keine drei Stunden nach ihrer Aufnahme.

`RELEASE_PROCESS.md` Abschnitt 4.1 sagt seit `1.0.0`:

> ⚠️ *„Die Zeilenenden des Archivs stehen seit D-320 fest. `git archive` folgt der
> `.gitattributes`; ohne sie hinge der Inhalt der Lieferung an der Konfiguration des
> Rechners, der sie erzeugt hat."*

**Der zweite Halbsatz ist richtig. Der erste ist es nicht** – und der erste ist die
Zusage.

## 2. Der gemessene Bestand

Dreimal dieselbe Marke `v1.0.0`, dreimal `git archive`, nur die Einstellung des
erzeugenden Rechners verstellt:

| `core.autocrlf` beim Erzeugen | Inhalt des Archivs |
|---|---|
| `true` (dieser Arbeitsplatz) | **520 CRLF**, 0 LF |
| `false` | **520 CRLF**, 0 LF |
| `input` | 0 CRLF, **520 LF** |

🔴 **Der Blob liegt in allen drei Fällen unverändert auf LF.** Die `.gitattributes`
wirkt – nur nicht dort, wo die Zusage sie behauptet.

➡️ ***`git archive` schreibt die Dateien im ARBEITSBAUM-Format aus, nicht im
Blob-Format.*** Es wendet dieselbe Umwandlung an wie ein `git checkout`, und die hängt an
`core.eol` und `core.autocrlf` des Rechners. **Die Abhängigkeit, die D-320 für das
Repositorium beseitigt hat, besteht für die Lieferung unverändert fort.**

## 3. Warum das mehr ist als ein Satz

| Gegenstand | Folge |
|---|---|
| **Die Lieferung** | Zwei Arbeitsplätze erzeugen aus **derselben signierten Marke** zwei verschiedene Archive – mit verschiedenen Prüfsummen. Eine Prüfsumme, die den Erzeuger nicht mitnennt, belegt nichts |
| **Die Nachweiskette** | `RELEASE_PROCESS.md` Abschnitt 8 beginnt mit *„Framework-Version (`VERSION`, Release-Archiv)"*. Ein Glied, das je nach Rechner anders aussieht, trägt die Kette nur halb |
| **Die Bauform** | *Eine Zusage, die mehr verspricht, als sie leistet* – der wiederkehrende Befundtyp dieses Projekts, diesmal an einer Regel, die **im selben Release** geschrieben wurde, das sie widerlegt hat |

⚠️ **Und der Befund hat sich nicht von selbst gezeigt.** `git archive` meldete Exit 0 und
schrieb eine Datei. **Gefunden hat es das Nachzählen im Erzeugnis** – dieselbe Regel, die
`0.90.0` am Word-Bau gelernt hat: *Ein Erzeugnis mit Exit 0 ist kein Beleg.*

---

## 4. Vorlage zur Entscheidung

| # | Frage | Wege und ihre Preise |
|---|---|---|
| **E1** | **Welche Zeilenendeform trägt die Lieferung?** | **Weg A – LF, die Form des Blobs.** Sie ist plattformneutral, entspricht dem, was git speichert, und ist die Konvention für Quelltextarchive. 🟢 **Gemessen: das Archiv zu `1.0.0` ist so erzeugt und enthält 520 LF, 0 CRLF, 0 gemischt.**<br><br>**Weg B – CRLF, die Form des Arbeitsbaums dieses Projekts.** ⚠️ **Preis:** Sie bindet die Lieferung an die Plattform ihres Ursprungs; ein übernehmendes Projekt unter Linux bekäme eine Form, die sein eigener Arbeitsbaum nie trägt.<br><br>**Weg C – keine Festlegung.** ⚠️ **Preis:** genau der gemessene Zustand – zwei Prüfsummen für dieselbe Marke |
| **E2** | **Wie wird die Form durchgesetzt?** | **Vorschlag: über die Schalter des Befehls, nicht über die `.gitattributes`.** `git -c core.eol=lf -c core.autocrlf=input archive …` legt die Form **im Befehl** fest und läßt den Arbeitsbaum unberührt. 🔴 **Verworfen: `eol=lf` in der `.gitattributes`** – das zwänge auch den Arbeitsbaum auf LF, und genau das hat `CR-2026-128` E1 mit Begründung abgelehnt. ➡️ *Eine Regel für die Lieferung gehört an die Lieferung, nicht an das Repositorium* |
| **E3** | **Braucht das eine Prüfung?** | **Vorschlag: nein, und der Grund ist gemessen.** Der Gegenstand ist ein **Erzeugnis außerhalb des Repositoriums** – eine Prüfung dagegen wäre im Framework grün und in jeder Installation ohne Archiv rot (D-299). 🟢 **Was trägt, ist das Nachzählen im Erzeugnis**, und das steht ab jetzt als Schritt im Verfahren. ⚠️ **Die Grenze ist benannt:** Ein Verfahrensschritt ist schwächer als eine Prüfung, und dieser Antrag sagt das, statt es zu verschweigen |

> **Empfehlung der Vorbereitung:** E1 Weg A, E2 wie vorgeschlagen, E3 nein – mit dem
> Nachzählen als benanntem Schritt und der benannten Grenze.

---

## 5. Umsetzung

1. `RELEASE_PROCESS.md` Abschnitt 4.1: der Befehl mit den Schaltern, der falsche Satz
   durch den gemessenen ersetzt, das Nachzählen als **Schritt 3**.
2. Decision Log: **D-328**; D-320 bekommt einen Nachtrag, der seine Reichweite auf den
   Blob begrenzt.
3. `VERSION` auf `1.0.1`, Changelog, Roadmap, Dokumentkopf und die Zahlen des
   Prüfapparats.
4. Das Archiv zu `1.0.1` nach dem berichtigten Verfahren, mit Nachzählen im Erzeugnis.

## 6. Entscheidung

**E1 bis E3 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-23). Decision
Record **D-328**, D-320 im Nachtrag begrenzt. Alle vier zählbaren Kriterien von D-11
bleiben **0**; kein Overlay-Feld berührt.
