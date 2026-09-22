# Wirkungsnachweise 0.56.0

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-18 |
| Framework-Version | `0.56.0` (Vorstand `0.55.0`, Commit `57eadcb`) |
| Antrag | `CR-2026-078`, D-124 bis D-126, `K-50` neu |
| Gegenstand | **Ein Planungsrelease.** Es ändert **keinen anweisenden Träger, keine Prüfung und keine Sonde** – es legt fest, was wann gebaut wird, wie das Projekt künftig heißt und wie der Installationsparameter für ein mitgeliefertes Overlay lautet |
| Prüfmethode | Validatorlauf gegen den fertigen Baum; Sondenlauf `probe-pruefungen.py .` in **beiden** Kodierungsumgebungen (D-49); Trockenlauf `install.py --update --dry-run` gegen je eine Kopie beider übernehmender Projekte |
| Ergebnis | **Validator 0 Fehler, 0 Warnungen; 254 Ergebniszeilen bestanden in beiden Kodierungsumgebungen** – zeilengleich mit 0.55.0. **Prüfung 14 hat gegriffen** (Abschnitt 2) |

---

## 1. Was dieses Release NICHT tut

**Es bewegt keine Zahl von D-11.** Kriterium 2 steht vor und nach diesem Release auf
**105**, Kriterium 1 auf **23**. Prüfung 46 meldet nichts, und das ist hier das erwartete
Ergebnis: Ein Plan ist keine Abnahme.

**Es ändert keine Regel und keine Zusage.** Angefasst sind `docs/ROADMAP.md`,
`governance/DECISION_LOG.md`, `VERSION` und `CHANGELOG.md`. Kein Kernmodul, kein Client
Pack, kein Skill, kein Testblatt.

> **Warum ein Plan trotzdem ein Release ist:** Eine Festlegung, wann etwas gebaut wird,
> verschiebt alles Übrige nach hinten – und die Umbenennung ist die weitreichendste
> Einzelentscheidung seit der Wahl des ersten Client Packs. **Eine solche Entscheidung
> gehört in einen Antrag mit Vorlage und Preis, nicht in einen Nebensatz** (Abschnitt 4
> des Entwicklungsprofils).

---

## 2. Prüfung 14 hat gegriffen, und sie hatte recht

Der erste Entwurf des Releaseplans trug in der Spalte *Sitzungskontingent* den Eintrag
`ja (Devin)` – ein Produktname für den Client, dessen Pack die vier offenen Marker trägt.

```
FEHLER   leitwerk-core/docs/ROADMAP.md:98: 'Devin' benennt einen Client als Akteur;
         der Kern ist werkzeugneutral (D-02). Gemeint ist der Begriff 'der KI-Client';
         muss der Text den Produktnamen tragen, steht dort <CLIENT_NAME>
```

**Berichtigt auf `ja (Pack `devin-desktop`)`.** Der Packname ist zulässig – er benennt
einen Bestandteil des Frameworks und keinen Handelnden.

> ➡️ **Das ist die dritte Gattung von Fund in diesem Release-Zyklus, und die billigste:**
> Der Fehler entstand beim Schreiben eines Planungsdokuments, also weit weg von jedem
> Regeltext, und wurde vom ersten Validatorlauf gemeldet. **Prüfung 14 läuft über den
> ganzen Baum, nicht nur über die Regelmodule** – genau die Eigenschaft, die `K-45`
> zugleich als Nachteil führt, weil die Meldung dort einem Projekt sagt, es habe eine
> Regel des Kerns verletzt.

---

## 3. Die Läufe

### 3.1 Validator

| Lauf | Zuschnitt | Ergebnis |
|---|---|---|
| V1 | `--root .` gegen den Baum mit Plan und Decision Records | **1 Fehler** – Prüfung 14, siehe Abschnitt 2 |
| V2 | `--root .` nach der Berichtigung | **0 Fehler, 0 Warnungen** |
| V3 | `--root .` gegen den **fertigen** Baum, Antrag, Änderungsverzeichnis und dieses Protokoll eingeschlossen | **0 Fehler, 0 Warnungen** |

### 3.2 Sondenlauf

| Lauf | Kodierungsumgebung | Ergebniszeilen | Wanduhr |
|---|---|---|---|
| A | ohne `PYTHONIOENCODING` | **254, alle bestanden** | 137,3 s |
| B | mit `PYTHONIOENCODING=utf-8`, gegen die **Endfassung** | **254, alle bestanden** | 141,2 s |

**Zwei Läufe statt vier, und das ist begründet:** Dieses Release fasst keine Datei an, die
eine Prüfung liest – kein Kernmodul, kein Pack, kein Testblatt, kein Skript. Der
Sondenlauf ist hier reine Regression. **Die Abnahmeauflage aus D-49 bleibt eingehalten:**
beide Kodierungsumgebungen, und der zweite Lauf geht gegen die Endfassung.

---

## 4. Der Migrationshinweis ist gemessen, nicht abgeleitet

| Projekt | Client Pack | angelegt | aktualisiert | unverändert | Projektdateien behalten |
|---|---|---|---|---|---|
| Pilot (`otp-generator`) | `claude-code` | 0 | **0** | 58 | 20 |
| Übungsrepositorium (`test-devin-framework`) | `devin-desktop` | 0 | **0** | 64 | 20 |

`install.py --update --dry-run` mit dem `leitwerk-core` dieses Arbeitsbaums gegen je eine
Kopie aus `git archive HEAD`. **Der Hinweis lautet „keiner", und er ist belegt.**

> ⚠️ **Für `2.0.0` gilt das ausdrücklich nicht.** Die Umbenennung auf `Koolie` ist eine
> **brechende** Änderung: Jedes übernehmende Projekt trägt den alten Namen in seiner
> Berechtigungsdatei, im Hook-Kommando, in jeder Regeldatei mit `<CORE_DIR>` und in seinem
> Overlay, und `install.py --update` schreibt das Kernverzeichnis **nicht**. Ihr
> Migrationshinweis ist selbst Gegenstand von `K-50`.

---

## 5. Zahlen dieses Releases, nachgezählt

| Zahl | Behauptet | Nachgezählt | Quelle |
|---|---|---|---|
| offene Ergebniszellen | 105 | **105** | Prüfung 46, unverändert gegenüber 0.55.0 |
| davon im zentralen Katalog | 22 | **22** | unabhängige Auszählung |
| offene Katalogzellen nach Klasse | `NE` 4, `PI` 3, `SC` 3, `FI` 3, `KO` 2, `PO` 2, `DS` 2, `AK` 2, `RE` 1 | **Summe 22** | Auszählung je Klasse, gegen die Gesamtzahl gehalten |
| offene `VERIFY`-Marker | 23 | **23** | Prüfung 46, unverändert |
| Posten ohne Ziel-Release vor diesem Release | 4 | **4** | `openai-codex`, Overlay-Parameter, Clientbindung des Kerns, Umbenennung |
| Ergebniszeilen des Sondenlaufs | 254 | **254** | zwei Läufe, je einzeln gezählt |

> ⚠️ **Die Klassensumme ist der Prüfstein dieses Releases.** Der Releaseplan verteilt die
> 22 Katalogzellen auf drei Sitzungstests; **stimmte die Aufteilung nicht, stünde in der
> Roadmap eine Zahlenfolge, die niemand nachrechnet.** Sie ist je Klasse ausgezählt und
> gegen die Gesamtzahl von Prüfung 46 gehalten: 4+3+3+3+2+2+2+2+1 = **22**.
>
> **Die 83 Zellen der dreizehn Testblätter sind bewusst NICHT je Blatt aufgeteilt.** Wo
> die Grenze eines Bündels Ermessen ist, gehört die Aufzählung ins Protokoll und die Zahl
> nicht – der Plan sagt deshalb „je Bündel von zwei bis drei Skills" und nennt nur den
> einen belegten Ausreißer: 15 Zellen im Blatt des Role Packs `requirements-engineering`.

---

## 6. Gegenzeichnung

| Frage | Antwort |
|---|---|
| Wurde jede Zahl nachgezählt? | **Ja.** Die Klassenaufteilung der 22 Katalogzellen ist einzeln ausgezählt und gegen Prüfung 46 gehalten |
| Behauptet der Plan Termine? | **Nein, und das ist eine Bedingung, keine Vorliebe.** Die Vorbemerkung der Roadmap sagt seit der Erstfassung: *„Es werden keine Termine oder Aufwände vorgegeben."* Der Plan nummeriert, er datiert nicht |
| Führt der Plan eine Zahl, die veralten kann? | **Nein.** Die vier Zahlen von D-11 stehen weiterhin ausschließlich in der Standzeile, die Prüfung 46 hält. Die Zwischenstände im Plan (`105 → 100 → 93 → 83`) sind **Vorhersagen** und als solche gekennzeichnet – sie tragen keinen Anspruch, den eine Prüfung einlösen müsste |
| Ist der Preis jeder Festlegung benannt? | **Ja, und der höchste steht zweimal:** Die Umbenennung nach 1.0.0 erzwingt ein Major-Release samt Migration für jedes übernehmende Projekt; vor 1.0.0 wäre sie billiger. Der Satz steht im Antrag (E4), im Decision Record (D-125) und in der Roadmap |
| Wurde ein Kandidat verworfen, ohne den Grund festzuhalten? | **Nein.** `Kelpie`, `Ibex`, `Meerkat`, `Hornbill` und `Markhor` stehen je mit Grund im Antrag und in der Roadmap – **einschließlich der Feststellung, dass `Kelpie` klanglich der beste war** |
| Wurde ein Befund beim Planen entdeckt? | **Ja, einer, und er trifft das letzte Release vor 1.0.0:** Kriterium 1 kann nicht auf null gehen, solange der `VERIFY`-Marker sein eigenes Register und seine Glossarzeile hat. Das ist Absicht (`CR-2026-070` E3) und verlangt einen Schritt, den bis heute kein Plan führte |

---

*Unterhalb der Trennlinie, nach D-94 nicht Teil des zeilengleichen Vergleichs:*
*Lauf A 137,3 s Wanduhr (1080,3 s Rechenzeit, 8 Bahnen, Faktor 7,9); Lauf B 141,2 s*
*(1113,5 s, Faktor 7,9).*
