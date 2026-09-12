# Testprotokoll – Wirkungsnachweis der Aktivierungsprüfung und der Clientwahl (Release 0.28.0)

| Feld | Inhalt |
|---|---|
| Test-ID | `FW-KO-01` und `FW-RE-02` (Basis), Teilnachweis für die mit 0.28.0 geänderte Aktivierungsprüfung und die Clientwahl der Installation |
| Framework-Version | 0.28.0 |
| Datum | 2026-09-12 |
| Prüfmethode | skript |
| Prüfgegenstand | **je Sonde eine frische Installation je Client Pack**, nicht eine Kopie des Repositoriums |
| Werkzeug | `leitwerk-core/tests/scripts/probe-pruefungen.py` |
| Umgebung | Windows 11, Python 3.14.4, PyYAML 6.0.3 |
| Ergebnis | **alle Sonden gemeldet, keine Gegenprobe beanstandet; gegen die Vorfassung 0.27.0 fallen acht** |

## 1. Warum diese Nachweise anders gebaut sind

Alle bisherigen Sonden arbeiten auf einer Kopie des Repositoriums. **Für diese beiden Befunde
reicht das nicht.** Die Aktivierungsprüfung liest die Laufzeitschicht eines *Projekts*, und die
Clientwahl entscheidet sich an dem, was in einem Projektverzeichnis liegt. Eine Sonde, die nur im
Repositorium läuft, kann beide Befunde nicht finden – **das ist der Grund, warum sie so lange
unbemerkt blieben.**

Der Sondenblock legt deshalb je Fall eine vollständige Installation an, eine pro Pack.

**Und darin liegt der eigentliche Kern von B02.** Der Befund war nicht, dass eine Prüfung falsch
prüft, sondern dass sie **einen Client gar nicht sieht**. Das fällt nur auf, wenn derselbe Fall in
*jeder* Installation läuft. Genau das verlangt das Abnahmekriterium des Reviews, und genau das ist
jetzt gebaut.

## 2. Ausgeführte Befehle und Ergebnis

```text
python leitwerk-core/tests/scripts/validate-framework.py
→ Ergebnis: 0 Fehler, 0 Warnungen

python leitwerk-core/tests/scripts/probe-pruefungen.py .
→ alle Sonden und Gegenproben bestanden   (Exit 0)
```

## 3. Der Befund vor der Korrektur, gemessen

Zwei frische Installationen, je eine pro Pack, darin **derselbe** Defekt. Gemessen ist die Änderung
der Fehlerzahl, nicht ihr absoluter Wert – ein frisches Overlay trägt ohnehin offene Werte. Der
`devin-desktop`-Lauf ist die Positivkontrolle.

| Defekt | `claude-code` | `devin-desktop` |
|---|---|---|
| Platzhalter in der Berechtigungsdatei (nach Bereinigung gesetzt) | 7 → 7 → 7, **±0** | 10 → 9 → 10, **reagiert** |
| Overlay-Status auf `aktivierung-ausstehend` | **±0** | **−1 Fehler** |

Die zweite Zeile ist kein Messfehler, sondern ein **eigener Befund**: Der Status wurde als Präfix
geprüft, und `aktivierung-ausstehend` beginnt mit `aktiv`. Ein Wert, der wörtlich sagt, dass die
Aktivierung aussteht, ließ den Fehler **verschwinden**, der vorher stand.

**Nach der Korrektur verhalten sich beide Packs identisch:** 10 → 9 → 10.

Für B10 genügte ein Lauf: Eine frische `claude-code`-Installation, darauf der in
`ADOPTION_GUIDE.md` wörtlich dokumentierte Aufruf `install.py --update` ohne `--client`.

```text
vorher:   Client:  devin-desktop
          Zusammenfassung: 60 angelegt, 0 aktualisiert, 0 unveraendert
          Laufzeitschichten: ['.claude'] → ['.claude', '.devin']

nachher:  Client:  claude-code
          Zusammenfassung: 0 angelegt, 0 aktualisiert, 58 unveraendert
          Laufzeitschichten: ['.claude'] → ['.claude']
```

**Sechzig Dateien – und dabei „0 aktualisiert".** Die Installation, die aktualisiert werden sollte,
blieb unberührt. Der Aufruf tat nicht zu viel, er tat das Falsche.

## 4. Der Lauf, der den Nachweis trägt

Derselbe Sondenblock gegen die Vorfassung 0.27.0 – eine Kopie des Arbeitsbaums, in der allein
`validate-framework.py` und `install.py` auf den Stand `HEAD` zurückgesetzt sind:

| Sonde | gegen 0.27.0 | gegen 0.28.0 |
|---|---|---|
| Status `aktivierung-ausstehend` wird gemeldet (`claude-code`) | **fällt** | besteht |
| Status `aktivierung-ausstehend` wird gemeldet (`devin-desktop`) | **fällt** | besteht |
| Platzhalter in der Berechtigungsdatei (`claude-code`) | **fällt** | besteht |
| Platzhalter in der Berechtigungsdatei (`devin-desktop`) | besteht | besteht |
| Fehlender sicherheitsrelevanter Abschnitt (`claude-code`) | **fällt** | besteht |
| Fehlender sicherheitsrelevanter Abschnitt (`devin-desktop`) | **fällt** | besteht |
| Aktualisierung ohne `--client` trifft das Pack (`claude-code`) | **fällt** | besteht |
| Aktualisierung ohne `--client` trifft das Pack (`devin-desktop`) | besteht | besteht |
| Widersprechendes `--client` bricht ab (beide Richtungen) | **fällt, zweimal** | besteht |
| Gegenproben zum Status `aktiv` und zur bereinigten Berechtigungsdatei | bestehen | bestehen |

**Acht Abweichungen gegen 0.27.0, keine gegen 0.28.0.** Die zwei Sonden, die auch alt bestehen,
sind genau die beiden Fälle, die die alte Fassung zufällig traf: die Berechtigungsdatei des einen
Packs, das sie fest verdrahtet las – und die Aktualisierung desselben Packs, das ihr Vorgabewert
war. **Das ist kein Mangel der Sonden, sondern die Form des Befunds.**

## 5. Ein Befund über die Gegenproben

Beim ersten Lauf fielen die beiden Platzhalter-Sonden in **beiden** Packs, obwohl die Korrektur
saß. Ursache: Der Unterprozess schrieb seine Ausgabe in der Konsolenkodierung des Systems; der
Diagnosetext enthält einen Umlaut und kam verändert zurück. Der gesuchte Text traf nie.

**Die zugehörige Gegenprobe hat das klaglos bestanden** – sie prüft auf *nicht enthalten*, und ein
Text, der nie auftreten kann, ist immer nicht enthalten. Eine Gegenprobe, die nichts mehr prüft und
es nicht zeigt.

Bemerkt hat es nur ihr Sondenpaar: Sonde und Gegenprobe suchen denselben Text, und die Sonde fiel.
**Die Paarung ist hier die Absicherung**, nicht die einzelne Prüfung. Der Unterprozess läuft
seither ausdrücklich mit UTF-8.

## 6. Grenzen dieses Nachweises

- **Geprüft ist die Aktivierungs*reife*, nicht die Aktivierung.** Dass ein Overlay `aktiv` sagt,
  heißt nicht, dass der Client seine Regeln lädt.
- **Der Abgleich zwischen Quell-Overlay und Laufzeitfassung fehlt weiterhin** (E4 von
  `CR-2026-044`). Die Laufzeitfassung kann von der Quelle abweichen, ohne dass es jemand merkt. Ein
  eigener Gegenstand, ausdrücklich offen – nicht erledigt.
- **Die Erkennung des installierten Packs ist an zwei Packs gemessen.** Ein drittes Pack bringt
  eine dritte Laufzeitschicht; die Sonden sind darauf vorbereitet, gemessen ist es nicht.
- **Bestehende Doppelinstallationen werden nicht aufgeräumt.** Wer bereits zwei Laufzeitschichten
  hat, bekommt einen Abbruch mit Hinweis, keine Hilfe beim Entfernen.

## 7. Bewertung

**Bestanden.** Dieselben Fälle laufen für beide Packs und melden in beiden dasselbe – das war das
Abnahmekriterium. Die Aktualisierung trifft das installierte Pack, und ein widersprechender Aufruf
bricht ab, statt eine zweite Laufzeitschicht anzulegen.

| Feld | Inhalt |
|---|---|
| Gegenzeichnung | `<TBD>` |
