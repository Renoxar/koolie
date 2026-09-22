# Änderungsantrag `CR-2026-042`

| Feld | Inhalt |
|---|---|
| Titel | Ein Abwesenheitsnachweis über das Suchwerkzeug ist für Punktdateien keiner |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-12 |
| Betroffene Artefakte | `tests/TEST_CATALOG.md` (Verfahren Nummer 7), `tests/protocols/README.md`, `clients/claude-code/CLIENT_PACK.md` (Werkzeugblock) |
| Ebene laut Entscheidungsbaum 6 | Kern – Nachweisverfahren |
| Art | Befund aus der Erhebung vom 2026-09-12 (ERH-12); **keine AP2-Kennung** |
| Dringlichkeit | regulär – aber vor dem nächsten Abwesenheitsnachweis zu entscheiden |

## 1. Anlass und Problem

Nummer 7 des Testkatalogs verlangt seit `CR-2026-034`, dass ein Nachweis aus dem **Ausbleiben**
einer Wirkung den Lauf selbst belegt – durch Ausgabe, Aufzeichnung oder eine Positivkontrolle im
selben Lauf. Die Regel richtet sich gegen den stillen Abbruch (`AP2-DD-13`, ERH-05): ein Lauf,
der mit Exit 0 endet und nichts getan hat.

**Am 2026-09-12 ist eine zweite Bauart desselben Fehlers aufgetreten, gegen die Nummer 7 nicht
schützt.** Im ersten B9-Lauf berichtete die Sitzung, die Messdatei `.env` existiere nicht, und
belegte das mit zwei Suchläufen:

| Befehl | Ergebnis |
|---|---|
| `Glob .env*` | `No files found` |
| `Glob **/.env*` | `No files found` |

**Die Datei lag im Verzeichnis.** Sie war im selben Lauf über einen anderen Weg lesbar; ihr Inhalt
steht in drei späteren Läufen desselben Protokolls im Ergebnis. Das Suchwerkzeug dieses Clients
führt Punktdateien nicht auf.

### Warum Nummer 7 das nicht abfängt

Der Lauf hatte alles, was Nummer 7 verlangt: eine Ausgabe, eine Positivkontrolle, die gelang, und
ein Werkzeug, das ordnungsgemäß antwortete. Es fehlte keine Wirkung – **das Werkzeug hat
gearbeitet und ein falsches Ergebnis geliefert.** Eine Positivkontrolle an einer anderen Datei
hätte den Fehler nicht gezeigt, denn sie trifft eine Datei ohne führenden Punkt.

Der Lauf wäre als sauberer Abwesenheitsnachweis durchgegangen: „gesucht, zweifach, nichts
gefunden". Er hätte in ein Protokoll gehen und dort die Annahme tragen können, eine geprüfte Datei
sei nicht vorhanden. Gemerkt hat es nur, wer wusste, dass er die Datei selbst angelegt hatte.

## 2. Vorgeschlagene Änderung

1. **Nummer 7 des Testkatalogs erhält einen zweiten Absatz.** Formulierungsvorschlag:

   > **Ein Werkzeugergebnis ist kein Abwesenheitsnachweis.** Wo der Nachweis lautet „die Datei,
   > der Eintrag, die Marke ist nicht da", MUSS die Abwesenheit mit einem Mittel geprüft werden,
   > dessen Trefferbild für den geprüften Gegenstand belegt ist – und die Prüfung MUSS eine
   > **Anwesenheitsprobe desselben Gegenstandstyps** enthalten. Für Punktdateien ist das
   > Suchwerkzeug mindestens eines Clients ungeeignet: Es meldet `No files found` für eine
   > vorhandene Datei (ERH-12).

2. **`tests/protocols/README.md`** nimmt die Bauart in die Zeile zu Nummer 7 auf: Neben dem
   „Beleg des Laufs selbst" steht künftig „und, bei einem Abwesenheitsnachweis über ein
   Suchwerkzeug, eine Anwesenheitsprobe desselben Gegenstandstyps".

3. **`clients/claude-code/CLIENT_PACK.md`** hält den Befund beim Werkzeug fest, wo er hingehört:
   Das Suchwerkzeug dieses Clients führt Punktdateien nicht auf; gemessen mit zwei Mustern gegen
   eine vorhandene Datei.

## 3. Was dieser Antrag nicht ändert

- **Nummer 7 bleibt in Kraft.** Der Absatz ergänzt sie, er ersetzt nichts. Die Positivkontrolle
  im selben Lauf bleibt Pflicht.
- **Keine Prüfung im Validator.** Der Befund betrifft ein Verfahren für Menschen und Sitzungen,
  nicht ein Artefakt im Repositorium. Eine Prüfung hätte nichts zu lesen.
- **Die bisherigen Protokolle werden nicht neu bewertet.** Ob eines von ihnen einen
  Abwesenheitsnachweis über ein Suchwerkzeug führt, ist offen – die Durchsicht der Altprotokolle
  nach `CR-2026-034` E4 steht ohnehin aus und bekommt mit diesem Antrag ein zweites Kriterium.

## 4. Prüffragen

- [x] Richtige Ebene: Kern – Nummer 7 ist ein Verfahren des Testkatalogs.
- [x] Verschärfungsprinzip: Der Absatz verschärft; er lockert nichts.
- [x] Widerspruchsfreiheit: `CR-2026-034`, Nummer 7, ERH-05 gelesen.
- [x] Laufzeitfassungen: nicht betroffen.
- [x] Belegstatus: gemessen, zwei Muster gegen eine nachweislich vorhandene Datei.
- [x] Test- und Validierungsbedarf: keiner – keine neue Prüfung, keine Sonde.
- [x] Overlays: nicht betroffen.
- [ ] Dokumentation: CHANGELOG, und die Durchsicht nach `CR-2026-034` E4 erhält ein zweites
      Kriterium.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | In den Testkatalog oder nur ins Client Pack? | **In beide, mit verschiedener Reichweite.** Ins Pack der gemessene Werkzeugbefund, in den Katalog die Verfahrensregel: Der Fehler ist nicht an dieses eine Werkzeug gebunden, sondern an die Bauart „Abwesenheit durch Suchen belegen" | Nummer 7 wächst. Sie war ein Absatz und wird zwei – eine Verfahrensvorschrift, die niemand liest, nützt nichts |
| E2 | Anwesenheitsprobe desselben Gegenstandstyps verlangen? | **Ja.** Genau das hätte den Fehler gezeigt: eine zweite Punktdatei, die gefunden werden **muss**. Eine Positivkontrolle an einer gewöhnlichen Datei genügt nicht | Jeder Abwesenheitsnachweis wird um einen Handgriff teurer. Bei einem Verfahren, das ohnehin schon Positivkontrolle und Mitschrift verlangt, ist das spürbar |
| E3 | Eine Prüfung im Validator? | **Nein.** Es gibt nichts zu lesen: Der Befund betrifft, wie gemessen wird, nicht was im Repositorium steht | Die Regel bleibt auf Disziplin angewiesen. Das ist die schwächste Durchsetzungsform, die dieses Projekt kennt – und für ein Verfahren die einzige mögliche |
| E4 | Die Altprotokolle daraufhin durchsehen? | **Ja, im selben Zug wie `CR-2026-034` E4.** Zwei Kriterien in einem Durchgang statt zweier Durchgänge | Die ohnehin ausstehende Durchsicht wird aufwendiger und rückt damit weiter nach hinten |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle vier Fragen wie vorgelegt.** E1 in Testkatalog **und** Client Pack, mit verschiedener Reichweite; E2 die Anwesenheitsprobe desselben Gegenstandstyps wird verlangt; E3 keine Validatorprüfung – es gibt nichts zu lesen; E4 die Altprotokolle werden im selben Zug wie `CR-2026-034` E4 durchgesehen |
| Datum | 2026-09-12 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | Die Durchsicht der Altprotokolle nach `CR-2026-034` E4 führt künftig **zwei** Kriterien und steht weiterhin aus. Im Wirkungsnachweis selbst ist die Regel bereits angewandt: `probe-pruefungen.py` prüft seit 0.27.0 vor jedem Sondenlauf, ob die Sonde den Baum überhaupt verändert hat |
| Umsetzung | umgesetzt mit `0.27.0` |
