# Wirkungsnachweise Release 0.44.0 – Prüfung 42 und die drei berichtigten Zusagen

| Feld | Wert |
|---|---|
| Gegenstand | `CR-2026-066`, D-90 und D-91: Prüfung 42 (ein gefüllter Befehlsschlitz trägt, was das Overlay erklärt), die Korbzerlegung an **einer** Stelle, und die drei uneingeschränkten Zusagen aus 0.39.0 |
| Datum | 2026-09-14 |
| Vorstand | `c0f15a9` (0.43.0) |
| Umgebung | Windows 11, Python 3.14.4 |
| Abnahmeform | Validator 0/0, Sondenlauf in **beiden** Kodierungsumgebungen (D-49), Gegenbeweis gegen den Vorstand |
| Ergebnis | **Bestanden.** Validator 0 Fehler, 0 Warnungen; **195 Sonden, Gegenproben und Selbstproben in beiden Umgebungen, zeilengleich**; Gegenbeweis als **Abzählen an einem echten Projekt** |

## 1. Der Gegenbeweis – ein Abzählen an einem echten Projekt

**Die Belegform dieses Releases ist ein Abzählen, keine Konstruktion.** Der Befund stand am
Piloten, bevor die Prüfung gebaut wurde; die Prüfung findet ihn. Das ist die Lage von 0.42.0
und der Unterschied zu 0.39.0, 0.40.0 und 0.41.0, deren Gegenbeweise Konstruktionen waren.

**Der Zuschnitt hat zwei Hälften, und beide gehören genannt:**

| Zuschnitt | Fundstellen |
|---|---|
| Neuer Validator gegen eine **frische Installation des Vorstands** (`c0f15a9`, Pack `devin-desktop`, installiert mit dem `install.py` des Vorstands) | **0** – und das ist kein Versehen: Die Schlitze stehen dort wörtlich offen, und das Overlay sagt dreimal `<TBD>`. **Es gibt dort nichts zu finden** |
| Neuer Validator gegen den **Piloten**, wie er steht (`devpacks/otp-generator`, Arbeitskopie, Pack `claude-code`) | **1** – `Bash(mvn -B -q compile)` im `ask`-Korb, während Abschnitt 6 `<LINT_COMMAND>` als „nicht vorhanden" erklärt |

**Die eine Fundstelle ist die richtige, und nur sie.** `Bash(mvn -B clean package)` und
`Bash(mvn -B test)` laufen durch, weil Abschnitt 5 und 6 sie für ihre Platzhalter erklären.
Eine Prüfung, die jede gefüllte Datei beanstandete, bestünde jede Sonde.

### Dieselben Läufe, Vorstand gegen diesen Stand

Die Läufe der Gegenprüfung an der Arbeitskopie des Piloten, ein zweites Mal gefahren –
einmal mit dem Kern des Vorstands, einmal mit diesem. **Die Gesamtzahl steht daneben, damit
eine Null ein Messwert ist und kein Absturz.**

| Lauf | Eingriff | 0.43.0 | 0.44.0 | Was Prüfung 42 neu sagt |
|---|---|---|---|---|
| **M1** | keiner – der Pilot wie vorgefunden | 0 (2 Fehler) | **1** (3 Fehler) | `Bash(mvn -B -q compile)` füllt keinen erklärten Schlitz |
| **M2** | `Edit(**)` aus `ask` entfernt | 1 (37) | 2 (37 **und** 42) | 42 meldet daneben weiter den Ist-Befund |
| **M3** | `Bash(mvn -B test)` → `Bash(mvn -B verify)` | 0 | **3** | zwei unerklärte Regeln **und** der erklärte Testbefehl fehlt |
| **M4** | dritter Schlitz trägt `mvn -B deploy` | 0 | **1** | der Befehl mit Fernwirkung wird benannt |
| **M5** | eine **vierte** Zeile im `ask`-Korb | 1 (37) | 3 (37 und 42) | beide Prüfungen, jede mit ihrem eigenen Satz |
| **M6** | `Bash(mvn -B -q compile)` **entfernt** | 0 | **0** | **Der zulässige Weg bleibt still** |
| **M7** | `Bash(mvn -B test:*)` | 1 (37) | 4 (37 und 42) | Präfixzeichen **und** abweichender Wert |

**M6 ist die wichtigste Zeile der Tabelle.** Sie zeigt, dass der Weg, auf dem ein Projekt den
Befund behebt – die Zeile streichen –, keinen Fehler erzeugt. **Eine Prüfung, die den
zulässigen Weg teurer macht als den unzulässigen, wäre ihre eigene Umgehung wert.**

**M3 und M7 melden mehr als eine Fundstelle, und das ist richtig:** Ein Schlitz mit fremdem
Inhalt ist zwei Aussagen zugleich – der erklärte Befehl steht nicht da, und ein nicht
erklärter steht da. Die beiden Meldungen sagen verschiedene wahre Dinge.

## 2. Sondenlauf

`python leitwerk-core/tests/scripts/probe-pruefungen.py .`, in beiden Kodierungsumgebungen –
mit und ohne `PYTHONIOENCODING=utf-8` (Abnahmeauflage seit D-49).

| Umgebung | Sonden | Gegenproben | Selbstproben | Ergebnis |
|---|---|---|---|---|
| ohne `PYTHONIOENCODING` | 135 | 53 | 7 | **alle bestanden** (Exit 0) |
| `PYTHONIOENCODING=utf-8` | 135 | 53 | 7 | **alle bestanden** (Exit 0) |

**Zeilengleich in beiden Umgebungen.** Der Vorstand trug 123 Sonden und 47 Gegenproben;
dieses Release fügt **zwölf Sonden und sechs Gegenproben** hinzu – je sechs und drei pro
Pack, denn Prüfung 42 hängt an einer Installation und wird deshalb je Pack gefahren (B02).

**Die achtzehn neuen im Einzelnen, je Pack identisch:**

| Kennung | Art | Fall |
|---|---|---|
| 42a | Gegenprobe | Auslieferungszustand: Overlay dreimal `<TBD>`, drei offene Schlitze |
| 42b | Gegenprobe | Drei erklärte Befehle, drei passende Regeln – der Normalfall |
| 42c | Gegenprobe | **Kein Lintbefehl, Schlitz gestrichen – der zulässige Weg** |
| 42a | Sonde | Der Fall des Piloten: Overlay sagt „nicht vorhanden", die Datei gewährt einen dritten Befehl |
| 42b | Sonde | Overlay erklärt dreimal `<TBD>`, die Datei gewährt drei Befehle – einer mit Fernwirkung |
| 42c | Sonde | Gefüllter Schlitz mit fremdem Befehl – der Fall, den Kandidat 2 beschrieb |
| 42d | Sonde | Das Overlay erklärt einen Befehl, die Datei trägt noch den offenen Schlitz |
| 42e | Sonde | Verlorener Anker – keine Tabellenzeile nennt den Platzhalter mehr |
| 42f | Sonde | Zwei Tabellenzeilen nennen denselben Platzhalter – welcher Befehl gilt? |

**Die drei Gegenproben sind die wichtigere Hälfte**, und 42c ist die entscheidende: Ein
Projekt ohne Formatprüfung, das seinen Schlitz streicht, läuft durch. Ohne diese Gegenprobe
stünde nur fest, dass die Prüfung irgendetwas meldet.

**Prüfung 40 hat während der Umsetzung zweimal gegriffen** – und beide Male zu Recht:

1. Die Spanne der Sondenmenge wurde auf „6 und 18 bis 42" gesetzt, **bevor** die erste Sonde
   zu Prüfung 42 existierte. Drei Meldungen, eine je Träger. **Die Prüfung hat einen
   vorgezogenen Registereintrag gefangen** – genau ihr Zweck.
2. Ein erster Entwurf fasste die Validatorläufe der Sonden in eine Hilfsfunktion, die
   `melde()` verdeckte. Prüfung 40 rechnet die Sondenmenge aus dem **wörtlichen** Muster
   `melde("SONDE", "…"` aus; die Sonden wären dort unsichtbar geblieben und die Spanne bei
   41 stehen geblieben. **Gefangen vor dem ersten Lauf, beim Lesen der Prüfung 40.**

## 3. Validator

`python leitwerk-core/tests/scripts/validate-framework.py --root .` gegen das Repositorium:
**0 Fehler, 0 Warnungen** – nach jedem der acht Patchschritte einzeln geprüft.

Die lokale Testinstallation (`.devin/`, `project-overlay/`) ist nach den Kernänderungen mit
`install.py --update` nachgezogen worden: 0 angelegt, 0 aktualisiert, 58 unverändert,
20 Projektdateien behalten.

**Prüfung 42 meldet im Repositorium nichts**, und das steht so im Kopfkommentar: Die
Testinstallation hat drei offene Schlitze und ein Overlay, das dreimal `<TBD>` sagt.

## 4. Was dieses Release nicht belegt

- **Die vier Pfadschlitze sind ungeprüft** (**K-35**). Kein Lauf dieses Protokolls sagt
  etwas über `<EXCLUDED_PATHS>` und die beiden Konfigurationslisten. Ein zu **eng**
  gefüllter Pfadschlitz bleibt eine stille Lockerung.
- **Prüfung 42 vergleicht Zeichenketten.** Dass `mvn -B test` in Abschnitt 6 und
  `Bash(mvn -B test)` in der Datei denselben Befehl meinen, ist eine Textgleichheit und
  keine Aussage über den Befehl.
- **Keine Sitzung ist gemessen.** Dass ein KI-Client eine unerklärte Zeile als Freigabe
  benutzt, ist **nicht beobachtet** – belegt ist, dass sie dasteht und bis 0.43.0
  unbeanstandet blieb.
- **Die drei berichtigten Zusagen sind nicht geprüft, sondern geschrieben.** Kein
  Mechanismus hält sie künftig gegen das, was der Validator leistet; sie bleiben Text.
  **Das ist genau die Bauform, die dieses Release behandelt** – hier nicht abgeschafft,
  sondern an drei Stellen berichtigt.
- **Der Pilot ist unberührt geblieben.** Alle Läufe liefen an Kopien; die Ausgangszustände
  sind nach jedem Lauf zurückgeschrieben und geprüft worden.

## 5. Gegenzeichnung

| Feld | Wert |
|---|---|
| Durchgeführt von | KI-Client (Claude Code) in der Sitzung vom 2026-09-14 |
| Gegengezeichnet | offen – `<FRAMEWORK_OWNER>` |
