# Nachtrag 0.54.1: Der Migrationshinweis von 0.54.0 war falsch

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-17 |
| Framework-Version | `0.54.0` (Commit `63c3205`); berichtigt mit `0.54.1` |
| Gegenstand | Der Migrationshinweis von 0.54.0: *„Keiner. Dieses Release ändert keine Datei der Laufzeitschicht und keinen Träger, der in ein Projekt installiert wird."* |
| Anlass | **Das Heben der beiden Projekte, unmittelbar nach dem Merge.** Der Hinweis ist nicht widerlegt worden, weil jemand ihn geprüft hätte, sondern weil der nächste Arbeitsschritt ihn ausgeführt hat |
| Antrag | `CR-2026-076` (Nachtrag); `K-45` erweitert, `K-46` neu |
| Prüfmethode | `install.py --update` in **beiden** übernehmenden Projekten, je gefolgt von `git status` und `git diff --numstat` über alles außerhalb von `leitwerk-core/` |
| Ergebnis | **Der Hinweis ist falsch.** 0.54.0 ändert **je Projekt genau eine** Datei der Laufzeitschicht |
| Abnahme | Validator **0 Fehler, 0 Warnungen**. **Sechs Sondenläufe, je 254 Ergebniszeilen, alle bestanden, beide Kodierungsumgebungen (D-49)** – siehe Abschnitt 6 |

---

## 1. Die Messung

| Projekt | Client Pack | Dateien außerhalb `leitwerk-core/` | `git diff --numstat` |
|---|---|---|---|
| `test-devin-framework` | `devin-desktop` | **1** – `.devin/skills/fw-repo-analyze/TESTS.md` | `4  4` |
| `otp-generator` | `claude-code` | **1** – `.claude/skills/fw-repo-analyze/TESTS.md` | `4  4` |

Die vier geänderten Zeilen sind **genau die vier Ergebniszellen**, die 0.54.0 von `offen`
auf `bestanden` gesetzt hat.

## 2. Warum der Hinweis falsch war

`install.py` kopiert je Skill das **ganze Verzeichnis** in die Laufzeitschicht – und ein
Skillverzeichnis enthält neben `SKILL.md` auch `EXAMPLES.md`, `CHANGELOG.md` **und
`TESTS.md`**. Der Hinweis wurde geschrieben in der Annahme, ein Testblatt sei eine Datei
des Prüfapparats. **Es ist auch eine Datei des Skills.**

> **Der wiederkehrende Befundtyp, diesmal an einer Aussage über das eigene Erzeugnis.** Der
> Satz „keine Datei der Laufzeitschicht" ist keine Nachlässigkeit, sondern eine **ungeprüfte
> Ableitung**: Das Release fasst den Testkatalog und ein Testblatt an, beides liegt unter
> `tests/` beziehungsweise unter `framework/skills/…/`, und keines davon sieht nach
> Laufzeitschicht aus. **Die Ableitung war plausibel und falsch, und ein einziger
> `install.py --update` widerlegt sie.**

**Die Lehre ist nicht neu, sie hat nur einen neuen Gegenstand.** Am 2026-09-16 hat dieses
Projekt gelernt, dass eine Null aus einem `grep` kein Beleg für Abwesenheit ist – gefangen
hat es damals eine frische Installation, die für etwas anderes gefahren wurde. **Hier ist es
dasselbe:** Gefangen hat es das Heben der Projekte, das ohnehin anstand.

➡️ **Wer einen Migrationshinweis schreibt, führt vorher ein `install.py --update` gegen ein
übernehmendes Projekt aus.** Der Hinweis ist eine Aussage über ein Erzeugnis; Aussagen über
Erzeugnisse werden am Erzeugnis geprüft, nicht am Quelltext.

## 3. Was daraus folgt, und was nicht

**Kein Anlass zur Sorge für die Projekte.** Berührt ist eine Aufzeichnung über Testergebnisse
des Frameworks – keine Regeldatei, kein Hook, keine Berechtigung, keine Anweisung. Beide
Validatorläufe tragen dieselben Zahlen wie vorher (`0/0` beim Übungsrepositorium,
`1 Fehler / 3 Warnungen` beim Piloten). **Der Fehler und zwei der drei Warnungen sind
eigener Projektinhalt; die dritte hat ihren Inhalt geändert, und zwar durch Dokumente
des Frameworks** – siehe Abschnitt 4. *Der erste Entwurf dieses Absatzes schrieb
„sämtlich eigener Projektinhalt" und widersprach damit dem eigenen Abschnitt 4; der
Durchgang vor dem Commit hat es gefangen.*

**Aber eine offene Frage bleibt** (`K-46`): Ein Projekt sieht jetzt in seiner Laufzeitschicht
die Testergebnisse des Frameworks, und zwar **ohne dass eine Version sich ändert** – D-119
sagt ausdrücklich, dass das Füllen einer Ergebniszelle keine Versionsänderung ist. **Wer den
Diff seiner Laufzeitschicht liest, findet eine Änderung ohne Version dahinter.** D-119 bleibt
für seinen Gegenstand richtig; die Frage ist, ob ein Testblatt überhaupt in die
Laufzeitschicht gehört.

## 4. Ein zweiter Befund aus demselben Handgriff

Beim Piloten (`claude-code`) meldet der Validator seit jeher eine Warnung über Pfadangaben,
die ein dort nicht installiertes Client Pack nennen. **Ihre Zahl steigt mit 0.54.0 von 9 auf
12** – nicht durch das Projekt, sondern weil die beiden neuen Dokumente des Frameworks
(Antrag und Messprotokoll) den Pfad des anderen Packs nennen. Sie tun das zu Recht: Die
Messung ist in einer Installation jenes Packs gefahren worden.

**Prüfung 14 nimmt historische Dokumente ausdrücklich aus** – `tests/protocols/` und
`governance/change-requests/` stehen in ihrer Ausnahmeliste, weil sie einen vergangenen
Zustand beschreiben. **Die Pfadprüfung tut das nicht.** Jedes Protokoll, das einen Lauf gegen
ein anderes Client Pack beschreibt, erhöht damit dauerhaft eine Warnung in jeder Installation
des jeweils anderen Packs. Aufgenommen in `K-45`.

---

## 6. Die Sondenläufe

**Sechs Läufe, drei Paare, jedes Paar in beiden Kodierungsumgebungen (D-49).** Zwischen den
Paaren liegt je eine Berichtigung, die dieses Protokoll selbst benennt:

| Paar | Zuschnitt | Ergebniszeilen | Wanduhr |
|---|---|---|---|
| E / F | vor der Berichtigung in Abschnitt 3 | **254 / 254**, alle bestanden | 167,1 s / 167,8 s |
| G / H | nach Abschnitt 3, vor der Berichtigung des Migrationshinweises | **254 / 254**, alle bestanden | 244,3 s / 244,0 s |
| **I / J** | **gegen die Endfassung** | **254 / 254**, alle bestanden** | 172,2 s / 172,1 s |

> **Warum sechs und nicht zwei.** Zweimal hat der Durchgang vor dem Commit eine Aussage
> dieses Protokolls berichtigt – einen Widerspruch zum eigenen Abschnitt 4 und einen Beleg,
> den es noch nicht gab. **Jede Berichtigung macht den vorangegangenen Abnahmelauf zu einem
> Lauf gegen einen anderen Baum**, und dieses Release handelt von genau diesem Fehlertyp:
> einer Aussage, die ihrer Messung vorausläuft. Die Läufe zu wiederholen war billiger als
> die Aussage zu verteidigen.

> **Der Rückschritt ohne Ende ist nach D-94 aufgelöst.** Ein Lauf gegen die Endfassung
> ändert die Endfassung, sobald man sein Ergebnis einträgt. Die Zahlen dieser Tabelle sind
> eine **Laufaufzeichnung** und nicht Teil des zeilengleichen Vergleichs; ihr Eintrag ändert
> nichts, was eine Prüfung liest. **Ohne diesen Satz sähe der Eintrag aus wie eine
> nachträgliche Korrektur am Messergebnis.**

> ⚠️ **Zur Wanduhr:** Die Paare sind nebenläufig gefahren, zwei Läufe zugleich auf acht
> Bahnen – deshalb liegen sie über den 135 s eines Einzellaufs. **Die Zahlen sind kein
> Vergleichsmaßstab für künftige Läufe**, und die Übergabe sagt seit 0.53.1, dass man die
> Wanduhr mitmisst statt sie zu übernehmen.

## 7. Gegenzeichnung

| Frage | Antwort |
|---|---|
| Ist der Befund gemessen oder abgeleitet? | **Gemessen**, in zwei Projekten unabhängig voneinander, mit `git diff --numstat` als zweiter Quelle neben `git status` |
| Wurde der falsche Hinweis entfernt oder berichtigt? | **Berichtigt und stehen gelassen.** Der Eintrag zu 0.54.0 im Änderungsverzeichnis behält seinen Wortlaut und trägt den Verweis auf diesen Nachtrag – ein Änderungsverzeichnis, das seine eigenen Fehler löscht, ist keines |
| Ist ein Release für eine Zeile gerechtfertigt? | **Ja.** Der Migrationshinweis ist die Zeile, die ein übernehmendes Projekt liest, bevor es aktualisiert. Ein falscher Hinweis dort kostet Vertrauen in jeden richtigen |
| Ändert dieser Nachtrag eine Zahl von D-11? | **Nein.** Kriterium 1 bleibt 23, Kriterium 2 bleibt 111, Kriterium 3 und 4 bleiben 0 |
| Ist der Migrationshinweis dieses Releases selbst gemessen? | **Ja, und zwar vor dem Merge.** Je ein `install.py --update --dry-run` gegen eine Kopie beider Projekte mit dem `leitwerk-core` dieses Arbeitsbaums: `claude-code` 0 angelegt / **0 aktualisiert** / 58 unveraendert, `devin-desktop` 0 / **0** / 64. **Der erste Entwurf behauptete einen Beleg „nach dem Merge" – also einen, den es nicht gab.** Derselbe Fehler wie der, den dieses Release behebt, eine Ebene weiter |
| Wurde eine Aussage dieses Protokolls im Durchgang vor dem Commit berichtigt? | **Ja, zwei.** Abschnitt 3 behauptete, die drei Warnungen beim Piloten seien sämtlich eigener Projektinhalt – Abschnitt 4 desselben Protokolls belegt das Gegenteil für eine davon. **Die Bauform ist bekannt: eine Zusammenfassung, die ihre eigene Tabelle überzeichnet** |
