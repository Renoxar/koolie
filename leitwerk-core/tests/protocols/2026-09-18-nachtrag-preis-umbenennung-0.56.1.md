# Nachtrag 0.56.1: Der Preis der Umbenennung war überzeichnet

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-18 |
| Framework-Version | `0.56.1` (Vorstand `0.56.0`, Commit `9628e13`) |
| Antrag | `CR-2026-078` (Nachtrag zu E4); D-125 ergänzt |
| Gegenstand | Die Preisangabe zur Festlegung „Umbenennung nach 1.0.0" behauptet mehr, als der Bestand hergibt – **und benennt die Widerlegung im eigenen Absatz.** Die Auflösung von E4 bleibt unverändert; sie trägt ab jetzt auf einem anderen Grund, und **eine echte Bedingung kommt hinzu** |
| Prüfmethode | Gegenprüfung nach D-23 am Bestand: Arbeitspakete der Roadmap, Standzeile, Übernahmeliste. Validatorlauf gegen den fertigen Baum; Sondenlauf in beiden Kodierungsumgebungen (Lauf A 139,2 s, Lauf B 140,6 s, je 254 Ergebniszeilen bestanden) |
| Ergebnis | **Der Preis ist berichtigt, die Entscheidung bestätigt, und eine Bedingung ist gefunden, die vorher niemand gesehen hat.** Validator 0 Fehler, 0 Warnungen |

---

## 1. Der Befund

`CR-2026-078` E4 schreibt:

> *„**Der Preis dieser Festlegung ist hoch und wird hier benannt, nicht verschwiegen:**
> Eine Umbenennung nach 1.0.0 ist nach SemVer eine **brechende Änderung** und erzwingt ein
> Major-Release samt Migration für **jedes** übernehmende Projekt. Vor 1.0.0 wäre sie
> billiger: **Es gibt genau zwei übernehmende Projekte, beide im eigenen Haus**, und keine
> Zusage über Stabilität ist gegeben."*

> 🔴 **Die Warnung und ihre Widerlegung stehen in demselben Absatz, zwei Sätze
> auseinander.** *„Migration für jedes übernehmende Projekt"* klingt nach vielen; der
> nächste Satz sagt, es sind **zwei**, beide im eigenen Haus. **Das ist der wiederkehrende
> Befundtyp dieses Projekts – eine Aussage, deren Widerlegung im eigenen Dokument steht –,
> diesmal in einem Absatz über die eigene Planung.**

**Gefunden hat ihn nicht eine Prüfung und nicht der Schreibende, sondern ein Einwand des
`<FRAMEWORK_OWNER>`:** *Es gibt noch keinen produktiven Einsatz, damit sehe ich es
unkritisch.*

---

## 2. Die Gegenprüfung nach D-23 – und sie fällt größer aus als der Einwand

**Nicht die Auskunft übernommen, sondern am Bestand nachgesehen:**

| # | Behauptung | Fundstelle | Ergebnis |
|---|---|---|---|
| 1 | Es gibt Übernahmen außerhalb des Hauses | `docs/ROADMAP.md`, `AP13 – Übernahme in weitere Projekte`: *Abhängigkeiten: **AP12***; *Eingaben: **Release 1.0.0*** | **nein – und konstruktionsbedingt.** `AP13` kann erst nach 1.0.0 beginnen |
| 2 | Der Pilot ist im Realbetrieb | `docs/ROADMAP.md`, `AP9 – Pilot`: *Realbetrieb in der Pilotgruppe*; offene Entscheidungen `<PILOT_DURATION>`, `<TBD: Zielwerte>` | **nein** – nicht gefahren, kein produktiver Einsatz |
| 3 | Die Übernahme hat Organisationsbezug | Standzeile der Roadmap, Kriterium 5 von D-11 | *„erfüllt … **organisatorisch bleibt es offen, weil es keinen Organisationsbezug hat**"* |

> ➡️ **Damit trägt die Festlegung auf einem anderen Grund als dem, mit dem sie begründet
> wurde – und der Grund gehört hingeschrieben.** Das ist die Regel *„Eine Bestätigung ist
> nicht die Behauptung, dass sich nichts geändert hat"*, angewandt auf die eigene
> Entscheidung von gestern.
>
> **Der bessere Grund, und er steht im eigenen Dokument:** `AP13` hängt an `AP12`. Die
> ersten Übernahmen außerhalb des Hauses kommen erst **nach** 1.0.0. **Eine Umbenennung
> als `2.0.0`, unmittelbar danach und vor dem Beginn von `AP13`, trifft genau dieselben
> zwei Projekte wie eine Umbenennung davor. Der Unterschied ist die Versionsnummer, nicht
> die Arbeit.**

---

## 3. Was als Preis übrig bleibt – vollständig aufgezählt

1. **Kosmetisch:** `1.0.0` trägt einen Namen, der ein Release später wechselt. Kein
   Aufwand, keine Migration, keine Zusage gebrochen.
2. 🔴 **Eine echte Bedingung, die vorher niemand gesehen hat: `2.0.0` MUSS vor der ersten
   Übernahme nach `AP13` liegen.** Läuft `AP13` zuerst an, kehrt der ursprüngliche Preis
   zurück – **und dann ist er zutreffend**, nicht überzeichnet.

> ⚠️ **Die Bedingung ist von keiner Prüfung gehalten, und das ist eine Entscheidung.**
> Eine Prüfung müsste wissen, welche Projekte übernommen haben; **diese Liste führt das
> Framework nicht** – `AP13` nennt sie als *Ergebnis* („gepflegte Bestandsliste"), also als
> etwas, das erst entsteht. Die Bedingung steht deshalb als Satz in der Zeile `2.0.0` des
> Releaseplans und in D-125, und sie ist `review`-prüfbar.

---

## 4. Was geändert wurde – und was ausdrücklich nicht

| Träger | Änderung |
|---|---|
| `governance/change-requests/CR-2026-078-...md` | Nachtrag unter E4. **Der falsche Absatz bleibt wörtlich stehen** |
| `governance/DECISION_LOG.md` | D-125 trägt den Nachtrag in seiner Statuszelle. **Die Auflösung bleibt unverändert** |
| `docs/ROADMAP.md` | Die Warnung zum Preis ist berichtigt; die Zeile `2.0.0` des Releaseplans trägt die neue Bedingung |

> **Warum der falsche Absatz stehen bleibt:** Dieselbe Entscheidung wie bei 0.54.1 (*„Ein
> Änderungsverzeichnis, das seine eigenen Fehler löscht, ist keines"*) und bei 0.55.0
> (Nachtrag 6.1a im Messprotokoll). **Ein Antrag, der seine Fehleinschätzung löscht,
> verliert den Lernwert** – und dieser hier ist lehrreich, weil er zeigt, dass eine
> überzeichnete Warnung genauso ein Befund ist wie eine überzeichnete Zusage.

**Keine Zahl von D-11 bewegt sich.** Kriterium 2 steht vor und nach diesem Nachtrag auf
**105**, Kriterium 1 auf **23**.

---

## 5. Gegenzeichnung

| Frage | Antwort |
|---|---|
| Wurde die Auskunft des `<FRAMEWORK_OWNER>` übernommen oder geprüft? | **Geprüft** (Abschnitt 2), an drei Fundstellen des eigenen Bestands. **Der Befund fiel größer aus als der Einwand:** `AP13` hängt konstruktionsbedingt an `AP12`, das war im Einwand nicht enthalten |
| Wird eine Entscheidung umgestoßen? | **Nein.** E4 bleibt: Umbenennung als `2.0.0` nach 1.0.0. Geändert ist ihre **Begründung**, und sie ist jetzt tragfähiger als die ursprüngliche |
| Ist der Preis jetzt vollständig? | **Ja, und er ist kürzer als vorher:** ein kosmetischer Posten und eine Bedingung. Die Bedingung ist neu und war in keiner Fassung des Antrags enthalten |
| Wird die Bedingung durchgesetzt? | **Nein, und der Grund steht in Abschnitt 3.** Sie ist `review`-prüfbar; die Liste übernommener Projekte führt das Framework nicht |
| Wurde ein falscher Satz gelöscht? | **Nein, keiner.** Drei Träger tragen den Nachtrag neben dem ursprünglichen Wortlaut |
