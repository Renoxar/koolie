# Wirkungsnachweise zu Release 0.34.0

| Feld | Wert |
|---|---|
| Gegenstand | Die Umsetzung zu `CR-2026-056` (D-61, D-62, D-63, Befund **B06**) – Eingabeschema, Prüfmaterial und Pfadidentität des Schutz-Hooks |
| Datum | 2026-09-13 |
| Framework-Version | 0.34.0 (gegen 0.33.0 = `22d0fcb`) |
| Prüfmethode | `probe-pruefungen.py` in **beiden** Kodierungsumgebungen; dazu der Validatorlauf des neuen Prüfsatzes gegen den unveränderten Vorstand, zweimal – einmal wie ausgeliefert und einmal mit neutralisiertem Ankertest |
| Umgebung | Windows 11, Python 3.14.4, NTFS |
| Ergebnis | **104 Sonden und Gegenproben bestehen gegen 0.34.0 in beiden Umgebungen** (71 Sonden, 33 Gegenproben). Validator: 0 Fehler, 0 Warnungen. Gegen den Vorstand meldet Prüfung 32 **zuerst ihren eigenen Anker**; erst mit neutralisiertem Ankertest misst sie durch und nennt **17 Fundstellen** |

## 1. Was hier nachgewiesen wird

| Gegenstand | Art | Nachweis |
|---|---|---|
| Ereignisschema mit `unprüfbar` als drittem Ausgang (D-61) | neuer Mechanismus | Sonde 32b; in Prüfung 32 zehn Eingabeformen |
| Prüfung der Operation statt des Umschlags (D-62) | **Verhaltensänderung** | Sonde 32c; in Prüfung 32 der Vergleich „mit und ohne Umschlag" je Pack |
| Unbekannte Operation wird streng gemessen (`CR-2026-056` E2) | geänderter Rückfall | Sonde 32d |
| Pfadidentität über den aufgelösten Pfad (D-63) | neuer Mechanismus | Sonde 32a; in Prüfung 32 vier Pfadvarianten je Pack |
| Schreibungsunempfindlichkeit aller Pfadmuster (D-63) | geänderte Muster | Sonde 32e |
| `hook_path_fields` aus den Manifesten (E6) | neues Manifestfeld | Gegenprobe 32 |
| Prüfung 32 selbst | neue Prüfung | Sonde 32f (verlorener Anker) |
| Berichtigung von Abschnitt 5 beider Packs (E9) | Textkorrektur | **keine Sonde** – siehe Abschnitt 5 |
| Zeile H4 und die nachgezogenen Summen | Matrixzeile | über Prüfung 31 mitgeprüft |

**Sechs Sonden für sechs Mechanismen, und keine über den naheliegenden Fall.** Bei
`LEITWERK-CORE/VERSION` decken die Auflösung und `re.I` einander gegenseitig zu: Fällt einer von
beiden aus, bestünde die Prüfung trotzdem. 32a und 32e treffen deshalb je einen Fall, den nur
**ein** Mechanismus fängt – ein relativer Pfad, der den Kern gar nicht nennt, und eine
Secret-Datei, die es nicht gibt und die `realpath` darum nicht kanonisieren kann.

## 2. Die Sonden

| Sonde | Präparation | Erwartete Meldung |
|---|---|---|
| 32a | Die Pfadauflösung liefert nichts – die Muster sehen nur den Rohtext | „ohne es zu nennen" |
| 32b | Eine leere Eingabe gilt wieder als harmloses Ereignis – der Stand bis 0.33.0 | „ist kein Werkzeugereignis" |
| 32c | Der Umschlag wandert zurück ins Prüfmaterial – der Stand bis 0.33.0 | „je nachdem ob der Umschlag" |
| 32d | Eine unbekannte Operation gilt wieder als lesend statt als die strengste | „unbekanntes Werkzeug in das Kernverzeichnis" |
| 32e | Das Secret-Muster für `.env` wird wieder schreibungssensitiv | „wenn die Datei nicht existiert" |
| 32f | Der Suchtext, über den Prüfung 32 ihren Gegenstand findet, geht verloren | „'def ereignis_lesen(' fehlt" |

**Gegenprobe 32:** Ein **zusätzliches** Pfadfeld in beiden Manifesten bleibt unbeanstandet. Sie ist
hier die wichtigere Hälfte: `hook_path_fields` ist über alle Packs vereinigt, und ein zusätzlich
erkanntes Feld ist eine Verschärfung (D-28). Ohne diese Gegenprobe stünde nur fest, dass Prüfung 32
etwas meldet – und eine Prüfung, die jede Manifestergänzung beanstandet, wäre eine Bremse statt
einer Schranke.

32f ist die **Sonde auf den verlorenen Anker**, dieselbe Bauform wie 28c, 29c und 31c. Sie wiegt in
diesem Release schwerer als sonst, denn im Gegenbeweis ist genau dieser Fall eingetreten – siehe
Abschnitt 3.

## 3. Der Gegenbeweis gegen den Vorstand

Vorgehen wie bei 0.32.0 und 0.33.0: `git archive 22d0fcb` in ein leeres Verzeichnis, dort mit
**dem eigenen** `install.py` des Vorstands installiert (nach `--dry-run`), dann nur
`validate-framework.py` aus 0.34.0 hineinkopiert.

### 3.1 Wie ausgeliefert – drei Fehler, und Prüfung 32 misst ihre Sache gar nicht

```
FEHLER  …/tests/EDGE_CASES.md: Keine Grenzfallzeile verweist auf D-61
FEHLER  …/tests/EDGE_CASES.md: Keine Grenzfallzeile verweist auf D-63
FEHLER  …/tests/scripts/hook-check-secrets.py: 'def ereignis_lesen(' fehlt. Pruefung 32
        misst Eingabeschema und Pfadidentitaet des Hooks; ohne diese Stufen prueft sie
        einen Aufbau, den es nicht mehr gibt, und bestuende leise (D-23, CR-2026-056)
Ergebnis: 3 Fehler, 1 Warnungen
```

Die ersten beiden stammen von **Prüfung 30** und gehören dazu: Die Grenzfalltabelle des Vorstands
kennt D-61 und D-63 nicht, weil es die Entscheidungen dort nicht gibt. Dasselbe hat 0.33.0 mit D-59
gezeigt.

Die dritte ist **Prüfung 32, die sich selbst anhält.** Der Hook des Vorstands kennt die drei Stufen
nicht; die Prüfung stellt das fest und **bricht ab, statt leise zu bestehen**. Das ist die Wirkung,
für die die Ankersonde gebaut ist, und sie tritt beim ersten Anwendungsfall ein. Es ist aber
**keine Messung der zwölf Fälle** – und dieser Unterschied ist der Grund für den zweiten Lauf.

### 3.2 Mit neutralisiertem Ankertest – siebzehn Fundstellen

Nur für die Messung, und nur in der Kopie im Arbeitsverzeichnis, wurde der Ankerblock entfernt.
Dann misst Prüfung 32 durch:

| Gruppe | Anzahl | Was |
|---|---|---|
| Eingabeformen | **10** | leer, nur Weißraum, `[]`, `null`, `"x"`, `42`, ohne `tool_name`, leerer `tool_name`, ohne `tool_input`, `tool_input` als Zeichenkette – sämtlich mit **Exit 0** trotz `--fail-closed` |
| `claude-code` | **4** | der Umschlag entscheidet mit (Exit 0 ohne, **Exit 2 mit**); unbekanntes Werkzeug schreibt in den Kern; Secret-Pfad in abweichender Schreibweise; ein Nachbarverzeichnis wird blockiert |
| `devin-desktop` | **3** | unbekanntes Werkzeug schreibt in den Kern; `LEITWERK-CORE/VERSION` wird anders entschieden als die Standardschreibweise; Secret-Pfad in abweichender Schreibweise |

**Zusammen 17**, dazu die beiden aus Prüfung 30 – der Lauf meldet 19 Fehler.

**Die vierte Zeile bei `claude-code` ist der P1-Befund selbst, von der Prüfung ausgesprochen:** Das
Nachbarverzeichnis `leitwerk-core-notizen/x.txt` ist harmlos und wird trotzdem blockiert – nicht
wegen seines Namens, sondern weil im Umschlag dieses Clients `transcript_path` steht. Beim Pack
`devin-desktop` fehlt diese Zeile, und das ist kein Verdienst des Hooks: Dessen Schema führt
schlicht kein `transcript_path`.

**Ebenso aussagekräftig ist, was der Vorstand *nicht* meldet.** Der Fall „relativer Pfad aus dem
Kern heraus" (`../VERSION` mit `cwd` im Kernverzeichnis) besteht dort – weil `cwd` damals
Prüfmaterial war und deshalb aus dem falschen Grund blockierte. Genau diesen Grund stellt D-62 ab,
und seither trägt den Fall allein die Auflösung. **Eine Sonde, die nur „blockiert ja/nein" fragt,
hätte hier keinen Unterschied gesehen.**

### 3.3 Die Zahl war behauptet, nicht gezählt

Der Entwurf von CHANGELOG und Roadmap nannte **„15 Fundstellen gegen 0.33.0"**. Nachgemessen sind
es 17, und der Weg dorthin ist ein anderer als der Text nahelegte: Wie ausgeliefert meldet der
Validator **drei** Fehler, weil die Ankersonde vorher greift. Beide Stellen sind berichtigt.

**Das ist der wiederkehrende Fall dieses Projekts, hier in eigener Sache:** 76 statt 248, fünf statt
zehn, sechs statt zwölf, 25 statt 20 – und jetzt 15 statt 17, in einem Text, der die Lehre daraus
selbst aufschreibt. **Wer hier eine Zahl liest, zählt sie nach, auch die eigene.**

## 4. Vier bestehende Sonden haben die eigene Umsetzung gefangen

Der erste Sondenlauf dieses Releases fiel mit **vier Abweichungen**, in beiden Kodierungsumgebungen
gleich. Keine betraf Prüfung 32; alle vier betrafen **Sonden zu 30 und 31, die an Zahlen verankert
sind, die dieses Release geändert hat**:

| Abweichung | Ursache |
|---|---|
| Sonde 31a `[nichts präpariert]` | suchte `\| \`[TECHNISCH]\` \| 20 von 30 \|`; die Matrix trägt seit H4 `21 von 31` |
| Sonde 31b `[nichts präpariert]` | dasselbe für die Gesamtzahl |
| Gegenprobe 31 fiel | zog die Summen auf 21/31 nach – gezählt sind seit H4 22/32 |
| Gegenprobe 30 fiel | suchte `\| Anzahl der Grenzfälle \| 13 \|`; es sind seit G-14/G-15 **15**. Dazu kollidierte ihre synthetische Kennung `G-14` mit dem **echten** neuen G-14 |

Zwei davon meldeten sich als `[nichts präpariert]` – die Sonde stellt selbst fest, dass ihr
Suchtext nicht mehr greift, und sagt es, statt die Prüfung zu messen. Die anderen beiden
präparierten halb und fielen an der Zahl. **Berichtigt sind die Suchtexte, nicht die Prüfungen**;
die synthetische Kennung heißt jetzt `G-16`.

**Zwei Beobachtungen, und die zweite ist ein offener Punkt:**

- Der Fall ist der erwartete Nutzen dieser Sondenbauart, nicht ihr Versagen: Die Meldung
  `[nichts präpariert]` existiert genau dafür, und ohne sie hätten die Sonden 31a und 31b nach
  diesem Release **grün und wirkungslos** dagestanden – der stillste aller Fehlschläge.
- **Die Sonden zu 31 pflegen dieselben Zahlen von Hand, die Prüfung 31 gerade deshalb ausrechnet**
  (D-60). Jede künftige Matrixzeile bricht sie erneut. Ob die Gegenprobe ihre Summen aus der
  Tabelle ableiten sollte – und ob sie dann noch beweist, was sie beweisen soll, oder nur die
  Rechenweise der Prüfung verdoppelt –, ist eine **Ermessensfrage und kein Messwert**. Sie gehört
  in einen Änderungsantrag und ist in diesem Release **nicht** entschieden.

## 5. Was dieses Release nicht nachweist

- **Die Berichtigung von Abschnitt 5 beider Packs hat keine Sonde**, bewusst: Es ist eine
  Textkorrektur an drei Aussagen, und eine Prüfung, die eine Formulierung bewacht, meldet jede
  Umformulierung und sonst nichts. Belegt ist der Widerspruch – Zeile H2 derselben Dokumente und
  der Manifestwert `hook_fail_closed: true` sagen seit 0.25.0 das Gegenteil.
- **Prüfung 32 misst am Hook, nicht am Client.** Die Messung am Client steht in der Gegenprüfung
  (`2026-09-13-B06-gegenpruefung.md`, Abschnitt 5.3), nicht im Validator. **Eine Messung am Hook
  ist keine Messung am Client** – das ist die Lehre, an der dieser Befund neun Releases lang
  vorbeikam.
- **Kein Lauf gegen einen Client mit 0.34.0.** Dass der Schreibzugriff bei `claude-code` *nach* der
  Berichtigung durchläuft, ist am Hook gemessen und im Validator geprüft, **nicht in einer
  Clientsitzung**. Der Kontrolllauf der Gegenprüfung belegt die Sperre, nicht ihre Aufhebung.
- **Symbolische Verknüpfungen unter Linux und macOS sind nicht gemessen.** Junctions unter NTFS
  sind es. Die Auflösung sollte dort gleich wirken – Erwartung, nicht Messung.
- **Die Zeitlücke ist benannt, nicht geschlossen** (E7). Ein Hook prüft vor dem Zugriff; eine
  zwischenzeitlich umgebogene Verknüpfung kann er nicht ausschließen. Zeile H4 und
  `framework/core/03-security.md` Abschnitt 4 sagen es.
- **Der Shell-Schreibweg bleibt offen** (D-30, D-47), und damit bleibt **K-32 offen**.
- **Die Lockerung aus E3 ist nachgerechnet** (Auflage des Antrags): Neu blockieren die zehn
  Eingabeformen, das unbekannte Werkzeug im Kern und die Pfadvarianten; neu durchläuft
  ausschließlich der Fall, in dem ein Pfad **außerhalb** von `tool_input` steht. In beiden
  aufgezeichneten Schemata trägt der Umschlag keine Operationsdaten – Sitzungs- und
  Ablaufkennungen, `cwd` und `transcript_path`. **Für ein künftiges Schema ist das eine offene
  Flanke**, und E1 ist die Kompensation: Was die Form nicht einhält, gilt als unprüfbar.

## 6. Der Lauf in beiden Kodierungsumgebungen

| Umgebung | Sonden und Gegenproben | Ergebnis |
|---|---|---|
| ohne `PYTHONIOENCODING` | 104 | alle bestanden |
| mit `PYTHONIOENCODING=utf-8` | 104 | alle bestanden |

104 = 97 aus 0.33.0 plus **6 Sonden und 1 Gegenprobe**. Ausgezählt aus dem Lauf: **71 Sonden, 33
Gegenproben** – 65 + 6 und 32 + 1. Der Validator meldet in beiden Umgebungen 0 Fehler und 0
Warnungen.

Der **erste** Lauf dieses Releases meldete in beiden Umgebungen 4 Abweichungen (Abschnitt 4); der
hier ausgewiesene ist der Lauf nach deren Berichtigung.

## 7. Gegenzeichnung

| Rolle | Name/Kennung | Datum | Ergebnis bestätigt |
|---|---|---|---|
| `<FRAMEWORK_OWNER>` | `<TBD>` | `<TBD>` | `<TBD>` |
