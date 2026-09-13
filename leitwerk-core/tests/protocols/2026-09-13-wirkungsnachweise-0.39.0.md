# Wirkungsnachweise Release 0.39.0 – die Berechtigungsdatei wird nachgezählt

| Feld | Wert |
|---|---|
| Gegenstand | `CR-2026-061`, D-76 und D-77: Prüfung 37 für die drei Körbe der Berechtigungsdatei, der Präfixteil für gefüllte Befehlsschlitze, und drei Texte, die mehr versprachen als der Mechanismus hält |
| Datum | 2026-09-13 |
| Vorstand | `07c8183` (0.38.0) |
| Grundlage der Zusagen | `tests/protocols/2026-09-13-gegenpruefung-berechtigungsdatei.md`, zwölf Messungen an einer frischen `claude-code`-Installation |
| Ergebnis | **Validator 0 Fehler, 0 Warnungen. 143 Sonden, Gegenproben und Selbstproben bestanden** (97 Sonden, 39 Gegenproben, 7 Selbstproben) – **in beiden Kodierungsumgebungen**, null Fehlschläge, Exit 0 |

## 1. Was neu geprüft wird

| Prüfung | Gegenstand | Sonden | Gegenproben |
|---|---|---|---|
| **37 (neu)** | Die drei Körbe der installierten Berechtigungsdatei gegen die aus der Kernquelle erzeugte Regelmenge: Fehlen ist immer ein Fehler, Überzähliges nur in `ask` und `allow` (D-77) | 37a bis 37e, 37g | 37a (Auslieferungszustand), 37b (gefüllte Schlitze) |
| **37 (Präfixteil)** | Ein gefüllter Befehlsschlitz trägt das Präfixzeichen des Clients nicht – die Abbildung hängt es bewusst nicht an | 37f | mitgeprüft über die Gegenprobe 37b |

**Die zweite Gegenprobe ist die wichtigere Hälfte.** Die erste belegt nur, dass der
Auslieferungszustand mit offenen Platzhaltern durchläuft; das ist der leichtere Fall, weil ein
offener Schlitz wörtlich in der erzeugten Menge steht. **Die zweite fährt drei ordentlich
gefüllte Schlitze** – `Bash(mvn -B clean package)`, `Bash(mvn -B test)`, `Bash(mvn -B verify)` –
und belegt, dass die Prüfung den Normalfall eines aktiven Projekts nicht beanstandet. **Ohne sie
stünde nur fest, dass sie irgendetwas meldet, und eine Prüfung, die jede gefüllte Datei
beanstandet, bestünde jede Sonde.**

## 2. Der Gegenbeweis – er ist eine Konstruktion, und das stand vorher im Antrag

**Prüfung 37 findet gegen 0.38.0 nichts**, und der Grund ist nicht, dass dort nichts wäre: Die
erzeugte Datei passt per Konstruktion zu der Regelmenge, aus der sie erzeugt wurde. **Ein
Gegenbeweis durch Auschecken eines alten Standes ist hier sinnlos** – er misst die Konstruktion
und nicht den Befund. Das steht so in `CR-2026-061` Abschnitt 4, vor dem Bauen.

**Der Gegenstand der Prüfung ist, was ein Projekt nach der Installation mit der Datei macht.**
Der Gegenbeweis läuft deshalb über dieselben zehn Eingriffe, mit denen die Gegenprüfung die Lücke
gemessen hat – einmal mit dem Validator des Vorstands, einmal mit dem neuen, an derselben
frischen `claude-code`-Installation:

| Nr. | Eingriff in `.claude/settings.json` | 0.38.0 | 0.39.0 |
|---|---|---|---|
| M1 | `ask` um `Bash(docker run --rm --network none:*)` ergänzt | 0 Fehler | **1** |
| M2 | `allow` um `Bash(docker run:*)` ergänzt | 0 Fehler | **1** |
| M3 | `Bash(curl:*)` aus `deny` gelöscht | 0 Fehler | **1** |
| M4 | alle 41 Nicht-Kernregeln aus `deny` gelöscht | 0 Fehler | **37** |
| M5 | `Bash(kubectl:*)` → `Bash(kubectl delete:*)` verengt | 0 Fehler | **1** |
| M6 | `Bash(<TEST_COMMAND>)` → `Bash(mvn -B test:*)` | 0 Fehler | **1** |
| M7 | Platzhalter gar nicht gefüllt (Auslieferungszustand) | 0 Fehler | **0** |
| M8 | `ask`-Korb geleert | 0 Fehler | **2** |
| M9 | *Gegenprobe:* Kernregel `Bash(sudo:*)` gelöscht | 1 Fehler | **2** |
| M10 | *Gegenprobe:* Kernregel in `allow` | 2 Fehler | **3** |

**M4 meldet 37 und nicht 41, und die Differenz ist kein Ausfall:** Vier der 41 gelöschten Regeln
sind Platzhalterschlitze (`Read(<EXCLUDED_PATHS>)`, `Edit(<CI_CONFIG_PATHS>)`,
`Edit(<QUALITY_GATE_CONFIG_PATHS>)`, `Edit(<EXCLUDED_PATHS>)`). Ein Schlitz, den ein Projekt
nicht braucht und streicht, ist eine Verschärfung – die Prüfung fordert ihn nicht ein.

**M7 bleibt bei null, und das ist die eigentliche Zusage der Tabelle.** Der Auslieferungszustand
muss durchlaufen; gefangen wird er dort, wo er hingehört:

```text
--strict-overlay      → FEHLER  .claude/settings.json: enthält noch Platzhalter (strict-overlay)
--check-overlay-ready → FEHLER  .claude/settings.json: enthält noch Platzhalter (check-overlay-ready)
```

**Prüfung 37 läuft bei beiden Packs – und das ist geprüft, nicht angenommen.** B02 war nicht,
dass eine Prüfung falsch prüft, sondern dass sie einen Client gar nicht sieht. Belegt an der
Testinstallation des Repositoriums (`devin-desktop`): Eine Zeile `Exec(docker run)` im `ask`-Korb
von `.devin/config.json` fiel sofort, der Eingriff wurde zurückgenommen, der Lauf steht wieder
auf 0/0.

## 3. Der Gegenbeweis am Piloten ist nicht fahrbar – und das ist ein eigener Befund

Der Antrag sah vor, den konstruierten Gegenbeweis an einer Datei zu ergänzen, die niemand für
diesen Zweck gebaut hat: der des Piloten. Er trug nach der Übergabe zwei stille Abweichungen,
darunter `Bash(mvn -B test:*)`.

**Diese Datei gibt es nicht mehr.** Vorgefunden am 2026-09-13 in `devpacks/otp-generator`:

| Erwartet laut Übergabe | Vorgefunden |
|---|---|
| `.claude/` mit `settings.json`, Framework 0.37.0 | `.claude/` enthält **nur** `settings.local.json` mit einer einzigen `allow`-Zeile |
| `project-overlay/` untracked vorhanden | **nicht vorhanden** |
| `leitwerk-core/` vollständig | nur `leitwerk-core/build/` |
| Branch `chore/leitwerk-pilot`, **nichts committet** | Branch trägt einen Commit (`45373e9`, Klassendokumentation) |

**Die Leitwerk-Installation des Piloten ist also entfernt worden**, und die Arbeit dort läuft
ohne sie weiter. Das ist keine Feststellung über das Framework und keine über den Piloten – es
ist die Feststellung, dass **der einzige verfügbare unkonstruierte Beleg für Prüfung 37 fehlt.**
Der Gegenbeweis dieses Releases bleibt damit eine Konstruktion, und die Tabelle in Abschnitt 2
ist alles, was er hergibt.

> **Der Befund des Piloten bleibt trotzdem gültig.** Dass `Bash(mvn -B test:*)` dort stand, ist
> in der Übergabe festgehalten und war der Anlass für den Präfixteil. Was fehlt, ist nicht der
> Befund, sondern die Möglichkeit, ihn heute noch einmal zu messen. **Ein Vorhandensein belegt
> sich selbst, ein Fehlen nicht** – und hier fehlt der Gegenstand, nicht der Nachweis.

## 4. Was beim Bauen aufgefallen ist

### 4.1 Die erste Fassung des Präfixteils meldete etwas anderes, als der Fall hergab

Beim ersten Lauf der Messreihe meldete die neue Prüfung bei M1, M2 und M10 **zwei** Fehler statt
einem: zum Überschuss kam die Meldung, die Abbildung hänge das Präfixzeichen „an einen gefüllten
Projektplatzhalter bewusst nicht an". **Keiner der drei Fälle war ein gefüllter Schlitz** –
`Bash(docker run:*)` und `Bash(sudo:*)` sind hinzugefügte Freigaben, und über deren Herkunft sagte
die Meldung etwas Falsches.

**Das ist der Befundtyp dieses Projekts, neu erzeugt** – eine Meldung, die mehr behauptet, als ihr
Gegenstand hergibt. Der Präfixteil läuft seither nur, wenn der Überschuss die Zahl der offenen
Schlitze **nicht** übersteigt; dann und nur dann ist entschieden, dass die Zeile ein gefüllter
Schlitz ist. Gefunden hat es die Messreihe selbst, nicht eine Prüfung.

### 4.2 Der Präparationswächter aus 0.38.0 passt nicht auf eine JSON-Datei

Die Sonden zu 37 verändern eine JSON-Datei, nicht einen Fließtext. `ersetzt()` taugt dort nicht,
und ein Textvergleich vorher/nachher als Ersatz taugt ebenso wenig: `json.dumps` normalisiert die
Datei ohnehin, der Wächter meldete also immer „verändert" und wäre wertlos. **Der Wächter sitzt
deshalb in den Eingriffen selbst** – `_37_weg` verlangt, dass die Regel dasteht, `_37_dazu`, dass
sie es nicht tut, `_37_statt` beides. Dieselbe Zusage wie D-74, an einem anderen Gegenstand.

### 4.3 Der Kopfkommentar des Validators endet bei Prüfung 31

Er listet die Prüfungen 1 bis 31; **32 bis 36 stehen nicht darin**, und 37 wäre die sechste Lücke.
Der Kopf ist damit seit fünf Releases unvollständig. **Hier nur benannt, nicht behoben** – eine
Nachtragung von 32 bis 37 in einem Release, das von der Berechtigungsdatei handelt, wäre ein
Nebengleis, und das ist die Bauform, an der dieses Projekt vier Releases verloren hat.

## 5. Sondenlauf

```text
python leitwerk-core/tests/scripts/probe-pruefungen.py .
Ergebnis: alle Sonden und Gegenproben bestanden        (Exit 0)

PYTHONIOENCODING=utf-8 python leitwerk-core/tests/scripts/probe-pruefungen.py .
Ergebnis: alle Sonden und Gegenproben bestanden        (Exit 0)
```

| | Vorstand 0.38.0 | Arbeitsbaum 0.39.0 |
|---|---|---|
| Sonden | 90 | **97** |
| Gegenproben | 37 | **39** |
| Selbstproben | 7 | 7 |
| **Summe** | 134 | **143** |

Die neuen Meldungen im Wortlaut, in beiden Umgebungen gleich:

```text
GEGENPROBE 37a  OK    Auslieferungszustand mit offenen Platzhaltern - ein Schlitz ist ein Schlitz
GEGENPROBE 37b  OK    Drei gefuellte Befehlsschlitze ohne Praefixzeichen - der Normalfall
SONDE      37a  OK    Geloeschte Nicht-Kernregel im deny-Korb - bis 0.38.0 stumm
SONDE      37b  OK    Verengte Nicht-Kernregel - kubectl apply liefe wieder
SONDE      37c  OK    Ergaenzte ask-Zeile - der Antrag CR-OTP-G-001 des Piloten
SONDE      37d  OK    Ergaenzte allow-Zeile - kein Abrufwerkzeug, nicht auf der Verbotsliste
SONDE      37e  OK    Geleerter ask-Korb - Edit(**) und mcp__* verschwinden mit
SONDE      37f  OK    Befehlsschlitz mit Praefixzeichen gefuellt - der Fall des Piloten
SONDE      37g  OK    Verlorener Anker - die Pruefung meldet ihr Fehlen selbst
```

**Keine bestehende Sonde ist verdrängt worden:** 90 + 7 = 97 und 37 + 2 = 39, null Fehlschläge in
293 Meldezeilen.

## 6. Was dieses Release nicht belegt

- **Keine Messung am Client.** Belegt ist, was der Validator sieht. Ob eine ergänzte `allow`-Zeile
  am Client tatsächlich durchlässt, ist nicht gemessen – und der Befund braucht es nicht: Eine
  Zeile im `ask`-Korb **erklärt** einen Befehl für freigegeben (`05-working-model.md`
  Abschnitt 3.2), und das ist die Ausweitung, unabhängig vom Mechanismus.
- **Der Präfixteil ist bei `devin-desktop` nicht gemessen, weil er dort keinen Gegenstand hat.**
  Dieses Pack sperrt Befehle wörtlich (`permission_exec_match: literal`). Prüfung 37 selbst läuft
  dort, belegt in Abschnitt 2.
- **Die Prüfung prüft die Form, nicht den Sinn.** Ein Befehlsschlitz, der mit einem Befehl gefüllt
  ist, den es gar nicht gibt, besteht sie. Der Abgleich zwischen Overlaytext und
  Berechtigungsdatei bleibt offen – am Piloten stand ein belegter `<LINT_COMMAND>`, obwohl das
  Overlay „Lint: nicht vorhanden" sagt, und Prüfung 37 sagt dazu nichts.
- **Kein Lauf gegen ein Projekt mit gefüllten Pfadschlitzen.** `<EXCLUDED_PATHS>`,
  `<CI_CONFIG_PATHS>` und `<QUALITY_GATE_CONFIG_PATHS>` sind in allen Sonden offen; gefüllt sind
  nur die drei Befehlsschlitze. Ein Projekt mit mehreren Ausschlusspfaden sollte durchlaufen, weil
  der `deny`-Korb Überzähliges zulässt – **das ist eine Erwartung, keine Messung.**
- **Die Testinstallation des Repositoriums trägt weiter den alten Kommentarkopf.**
  `install.py --update` fasst `.devin/config.json` nicht an – **genau der Mechanismus, den dieses
  Release beschreibt**, hier am eigenen Baum zu besichtigen. Der Kopf ist nicht normativ und wird
  von keiner Prüfung gelesen.
- **Der Gegenbeweis ist eine Konstruktion**, und der unkonstruierte Beleg ist mit der
  Pilotinstallation verschwunden (Abschnitt 3).

## 7. Gegenzeichnung

| Rolle | Name/Kennung | Datum | Ergebnis bestätigt |
|---|---|---|---|
| `<FRAMEWORK_OWNER>` | `<TBD>` | `<TBD>` | `<TBD>` |
