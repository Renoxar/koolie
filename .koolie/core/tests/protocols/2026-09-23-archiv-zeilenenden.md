# Protokoll: Die Zeilenenden des Release-Archivs – gemessen an der ersten Lieferung

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-23 |
| Release | **`1.0.1`** |
| Änderungsantrag | `CR-2026-129` |
| Art | **Meßprotokoll.** Der Gegenstand ist ein Erzeugnis außerhalb des Repositoriums |
| Prüfmittel | `review` – drei Läufe von `git archive` gegen dieselbe Marke, Auszählung im Erzeugnis |
| Ergebnis | 🔴 **Die Zusage aus Abschnitt 4.1 ist widerlegt.** `git archive` schreibt im **Arbeitsbaum**-Format aus; die Lieferung hängt am erzeugenden Rechner |

> 🔴 **Dies ist kein Abnahmeprotokoll des Testkatalogs** und trägt deshalb keinen
> Abschnitt *Gegenzeichnung* (D-319, Zuschnitt von Prüfung 80). Es berichtet eine
> Messung und trägt seinen Beleg in sich.

---

## 1. Der Anlaß

`1.0.0` hat mit **D-321** das Release-Archiv eingeführt – den MUSS-Prüfpunkt, den
`FW-CL-11` seit jeher verlangt und den **106 Release-Commits** lang niemand erfüllt hat.
Im selben Release schrieb Abschnitt 4.1:

> ⚠️ *„Die Zeilenenden des Archivs stehen seit D-320 fest. `git archive` folgt der
> `.gitattributes`; ohne sie hinge der Inhalt der Lieferung an der Konfiguration des
> Rechners, der sie erzeugt hat."*

**Das erste Archiv, das nach dieser Regel erzeugt wurde, hat sie widerlegt** – rund
dreißig Minuten nach ihrer Aufnahme.

## 2. Das Verfahren

Dreimal derselbe Befehl gegen dieselbe Marke `v1.0.0`, nur die Einstellung des
erzeugenden Rechners verstellt. Gezählt wurde **im Erzeugnis**, nicht an der Meldung:

```
git -c core.autocrlf=<wert> archive --format=tar -o <ziel> v1.0.0
```

## 3. Die Messung

| `core.autocrlf` beim Erzeugen | CRLF | LF | Blob unverändert? |
|---|---|---|---|
| `true` (dieser Arbeitsplatz) | **520** | 0 | ✅ LF |
| `false` | **520** | 0 | ✅ LF |
| `input` | 0 | **520** | ✅ LF |

🔴 **Der Blob liegt in allen drei Fällen auf LF.** Die `.gitattributes` wirkt – nur nicht
dort, wo die Zusage sie behauptet.

➡️ ***`git archive` wendet dieselbe Umwandlung an wie ein `git checkout`.*** Es schreibt
die Dateien im **Arbeitsbaum**-Format aus, und das bestimmen `core.eol` (Vorgabe
`native`, auf Windows CRLF) und `core.autocrlf`.

## 4. Was daraus folgt

| Gegenstand | Folge |
|---|---|
| **Die Lieferung** | Zwei Arbeitsplätze erzeugen aus **derselben signierten Marke** zwei Archive mit **zwei Prüfsummen**. Eine Prüfsumme, die ihren Erzeuger nicht mitnennt, belegt nichts |
| **Die Nachweiskette** | Abschnitt 8 beginnt mit *„Framework-Version (`VERSION`, Release-Archiv)"*. Ein Glied, das je nach Rechner anders aussieht, trägt sie nur halb |
| **Die Reichweite von D-320** | Gemessen war der **Blob**. Daß damit auch das **Archiv** feststehe, war eine **Folgerung** – und sie stand eine Regel lang unbelegt da |

➡️ ***Eine Entscheidung gilt so weit wie ihr gemessener Gegenstand und nicht so weit wie
die Folgerung aus ihr.***

## 5. 🔴 Wie der Befund gefunden wurde – und wie nicht

**`git archive` meldete Exit 0 und schrieb eine Datei von 2,67 MB.** Kein Werkzeug hat
etwas beanstandet; der Validator kennt den Gegenstand nicht, und es gibt keine Prüfung
dafür.

**Gefunden hat ihn das Auszählen im Erzeugnis** – dieselbe Regel, die `0.90.0` am
Word-Bau gelernt hat, als der Bau *„geschrieben"* meldete und **null von acht**
Diagrammen eingebettet hatte.

➡️ ***Ein Erzeugnis mit Exit 0 ist kein Beleg.*** Das Nachzählen steht seit `1.0.1` als
**Schritt 3** im Verfahren.

## 6. Die Abhilfe und ihre Grenze

🟢 **Die Form steht jetzt im Befehl**, nicht in der `.gitattributes`:

```
git -c core.eol=lf -c core.autocrlf=input archive \
  --format=tar.gz --prefix=koolie-<Version>/ -o <Ziel> v<Version>
```

⚠️ **Verworfen: `eol=lf` in der `.gitattributes`.** Sie zwänge auch den **Arbeitsbaum**
auf LF – abgelehnt mit `CR-2026-128` E1 und dort begründet. *Eine Regel für die Lieferung
gehört an die Lieferung, nicht an das Repositorium.*

🔴 **Verworfen: eine Prüfung – und die Begründung ist gemessen.** Der Gegenstand liegt
**außerhalb** des Repositoriums. Eine Prüfung dagegen wäre im Framework grün und in jeder
Installation ohne Archiv rot – der Konstruktionsfehler aus D-299, den dieses Projekt
zuletzt bei Prüfung 78 und 79 bezahlt hat (D-326).

⚠️ **Was bleibt, ist ein Verfahrensschritt, und der ist schwächer als eine Prüfung.**
Er hängt an der Sorgfalt dessen, der das Release fährt. **Das steht hier, statt daß es
verschwiegen wird** – nach D-23 gilt eine Zusage ohne Mechanismus als nicht vorhanden,
und dieser Satz sagt, welche Art von Zusage hier getroffen wurde.

## 7. Das Archiv zu `1.0.0`

🟢 **Nach dem berichtigten Verfahren neu erzeugt und im Erzeugnis nachgezählt:**

| Gegenstand | Wert |
|---|---|
| Dateien | **521**, davon **515** im Kern |
| Zeilenenden | **520 LF**, 0 CRLF, 0 gemischt, 1 binär |
| Lizenz in der Wurzel | ✅ |
| Lizenz im Kern | ✅ – sie muß nach §4 GPL-3.0 mitwandern (D-317) |
| Erzeugnisse aus `build/out/` | **nicht enthalten** (`.gitignore`, und das ist richtig) |
| Ablage | außerhalb des Repositoriums, mit Prüfsumme |
