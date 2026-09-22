# Änderungsantrag `CR-2026-026`

| Feld | Inhalt |
|---|---|
| Titel | Der Schutz-Hook läuft fail-closed, wo das Eingabeschema belegt ist |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-11 |
| Betroffene Artefakte | `framework/runtime/hooks.json`, `clientmap.py`, `clients/claude-code/manifest.json`, `clients/devin-desktop/manifest.json`, `tests/scripts/hook-check-secrets.py`, `tests/scripts/validate-framework.py` (Prüfung 17 neu), beide `CLIENT_PACK.md` |
| Ebene laut Entscheidungsbaum 6 | Schutzmechanismus, Abbildung und Prüfung; keine Regeländerung |
| Art | Härtung; Einlösung eines seit 0.1.0 ausgewiesenen Vorbehalts |
| Dringlichkeit | regulär – die Lücke besteht nur bei einer Eingabe, die der Hook nicht lesen kann |

## 1. Anlass und Problem

Der Schutz-Hook lässt eine Werkzeugeingabe, die er nicht als JSON lesen kann, durch und meldet
sie nur auf stderr. Der Kopfkommentar von `hook-check-secrets.py` nannte dafür seit 0.1.0 einen
Grund und eine Bedingung:

> Nicht parsebare Eingabe -> standardmäßig Exit-Code 0 mit Warnung auf stderr (fail-open),
> weil das Eingabeschema noch nicht in einer Zielinstallation validiert wurde. […] Nach
> erfolgreicher Validierung im Arbeitspaket „Validierung der Clientfunktionalitäten" SOLL
> fail-closed zum Standard gemacht werden (Secure by Default).

**Die Bedingung ist für einen der beiden Clients erfüllt.** `claude-code` ist mit 0.14.0 bis
0.19.0 gegen eine reale Installation gefahren worden: Das Blockierverhalten ist über den
Exit-Code dokumentiert, H2 ist seit `CR-2026-021` in einer Sitzung beobachtet, und WN-5 belegt
die Lesesperre in einer Umgebung ohne Regeltexte. Für `devin-desktop` ist sie es nicht – V3
führt Eingabeschema und Blockierverhalten weiterhin als unbestätigt, AP2 für dieses Pack steht
aus.

**Ein gemeinsamer Standard wäre in beide Richtungen falsch.** Fail-open für beide verschenkt
eine Sperre, die bei einem Client belegt ist. Fail-closed für beide behauptet eine Sperre, die
beim anderen nicht geprüft ist – und blockierte dort, wenn das Schema abweicht, jeden
Werkzeugaufruf. Der Vorbehalt ist deshalb nicht aufzuheben, sondern **dorthin zu verlagern, wo
er hingehört: in das Pack, dessen Client er beschreibt.**

### Warum der Schalter nicht in die Umgebung gehört

Der Mechanismus für fail-closed existierte bereits: die Umgebungsvariable
`FW_HOOK_FAIL_CLOSED=1`. `clients/claude-code/CLIENT_PACK.md` empfahl bis 0.23.0 ausdrücklich,
sie nach Bestätigung über `env` in der erzeugten Konfiguration zu setzen.

Dieser Weg hängt die Sperre an eine **zweite Clientzusage**: dass der Client den Inhalt von `env`
an den Hook-Prozess weiterreicht. Diese Zusage ist für **kein** Pack belegt. Sie wäre auch nicht
vom Validator prüfbar – er sieht nicht, was der Client an einen Kindprozess weitergibt.

Eine Sperre, die auf einer unbelegten Clientzusage steht, ist genau die Lage, aus der
`AP2-CC-13` kam: Der Hook-Aufruf setzte acht Releases lang voraus, dass `python3` einen
Interpreter startet. Geprüft worden war die Anwesenheit der Konfiguration, nie ihre Wirkung.

## 2. Vorgeschlagene Änderung

**Der Schalter steht im Aufrufkommando.** Das Argument ist Teil der Hook-Konfiguration, die der
Client ohnehin ausführt. Läuft der Hook – was Prüfung 15 an seiner Wirkung belegt –, dann kommt
das Argument an. Es braucht keine weitere Zusage.

**Zwei Felder, zwei Zuständigkeiten:**

| Feld | Ort | Sagt aus | Wer weiß es |
|---|---|---|---|
| `enforcing` | `framework/runtime/hooks.json` | Dieser Hook setzt eine Sperre durch, statt nur zu melden | der Kern – es ist eine Eigenschaft des Hooks |
| `hook_fail_closed` | `clients/<pack>/manifest.json` | Das Eingabeschema **dieses** Clients ist gegen eine Installation bestätigt | das Pack – es ist eine Eigenschaft des Clients |

Trifft beides zu, hängt `clientmap.py` dem Kommando `--fail-closed` an. Das Ergebnis:

```text
claude-code    PreToolUse    … hook-check-secrets.py" --fail-closed
claude-code    SessionStart  … hook-overlay-status.py"
devin-desktop  PreToolUse    … hook-check-secrets.py"
```

Der Statusmelder trägt es nicht – er setzt nichts durch. Das steuert `enforcing`, nicht eine
Liste von Skriptnamen im Abbildungscode.

**Prüfung 17 prüft die Wirkung auf zwei Ebenen.** Beide sind nötig:

1. **Am Skript:** Mit `--fail-closed` muss eine unlesbare Eingabe Exit 2 liefern, ohne das
   Argument Exit 0. Diese Ebene läuft auch dort, wo es keine Installation gibt. Ohne sie fiele
   ein Schalter, der ins Leere greift, erst in einer Installation auf – die Lage, in der
   `AP2-CC-16` acht Releases lang unbemerkt blieb.
2. **An der erzeugten Konfiguration:** Das Kommando wird so aufgerufen, wie es dort steht, und
   sein Verhalten gegen die Zusage des Packs gehalten. Diese Ebene prüft die ganze Kette –
   Manifest, Abbildung, Konfiguration, Verhalten.

Die Umgebungsvariable wird für den Prüfaufruf aus der Umgebung entfernt. Sonst bestünde der Test
auch dann, wenn das Argument nichts bewirkt.

## 3. Was dieser Antrag nicht ändert

- **Das Kernverhalten des Hooks.** Secret-Muster, geschützte Pfade, die Trennung nach Schutzziel
  aus D-30 und die Tokenisierung von Shell-Befehlen sind unberührt. Fünf Regressionsproben
  belegen es.
- **`devin-desktop`.** Das Pack läuft weiter fail-open – jetzt aber als **ausgewiesene** Angabe
  im Manifest und in der Matrix, statt als Folge einer fehlenden Angabe.
- **Die Umgebungsvariable.** `FW_HOOK_FAIL_CLOSED=1` wirkt weiterhin und bleibt der Weg, in einer
  bestehenden Installation fail-closed zu erproben, ohne neu zu installieren.

## 4. Grenze der Zusage

**Fail-closed betrifft einen einzigen Zweig:** eine Eingabe, die sich nicht als JSON lesen lässt.
Der Hook ist sonst schema-agnostisch – er durchsucht alle Zeichenketten der Struktur und findet
ein Secret auch dann, wenn die Feldnamen anders heißen. Die Änderung härtet also den Fall, in
dem der Hook **gar nichts** sehen kann, nicht den, in dem er etwas übersieht.

**Der Preis ist benannt:** Ändert der Client sein Eingabeformat auf etwas, das kein JSON ist,
blockiert bei `claude-code` jeder erfasste Werkzeugaufruf, bis das Schema nachgezogen ist. Das
ist beabsichtigt – ein Schutz-Hook, der bei unklarer Lage durchwinkt, ist schlimmer als ein
fehlender (D-29). Die Blockierbegründung nennt den Verdacht und den Weg.

**Eine bestehende `claude-code`-Installation erhält das Argument nicht von selbst.** Die Hooks
liegen dort in der Berechtigungsdatei und damit in der Saat; `install.py --update` fasst sie nie
an. Prüfung 17 meldet das als Fehler und nennt den Behebungsweg clientabhängig. Die
Migrationspflicht ist damit sichtbar statt stillschweigend.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Kommandoargument oder Umgebungsvariable? | **Argument.** Es steht in der Konfiguration, die der Client ausführt; `env` hätte die Sperre an eine für kein Pack belegte Clientzusage gehängt | Eine bestehende Installation, deren Hooks in der Saat liegen, zieht das Argument von Hand nach |
| E2 | Für beide Packs oder je Pack? | **Je Pack.** Belegt ist das Schema nur bei `claude-code`; bei `devin-desktop` blockierte fail-closed bei abweichendem Schema jede Sitzung | Die beiden Packs verhalten sich an dieser Stelle unterschiedlich – ausgewiesen in beiden Matrizen |
| E3 | Woran erkennt die Abbildung einen durchsetzenden Hook? | **Am Feld `enforcing` der Kernquelle.** Eine Liste von Skriptnamen im Abbildungscode veraltet beim nächsten Hook | Ein zusätzliches Feld in der neutralen Quelle, das beim Rendern entfernt wird |
| E4 | Prüfung 17 auf einer oder zwei Ebenen? | **Zwei.** Die Ebene am Skript läuft auch ohne Installation; ohne sie fiele ein wirkungsloser Schalter erst dort auf, wo es nichts zu prüfen gibt | Vier zusätzliche Prozessstarts je Validatorlauf |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** |
| Datum | 2026-09-11 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | **E1 bis E4 wie in Abschnitt 5 vorgelegt**: Der Schutzschalter steht im Kommandoargument und nicht in der Umgebung; er wird **je Pack** gesetzt, weil das Eingabeschema nur bei einem belegt war; die Abbildung erkennt einen durchsetzenden Hook am Feld `enforcing` der Kernquelle; Prüfung 17 misst auf **zwei** Ebenen |
| Umsetzung | **mit Release 0.24.0** – Einzelheiten und Nachweise in `.koolie/core/CHANGELOG.md` |

Abschnitt 6 ist am 2026-09-22 mit `CR-2026-124` (`AP11`) **nachgetragen**, nicht neu entschieden: Die Entscheidung selbst steht seit 2026-09-11 in **D-31**, die Umsetzung im `CHANGELOG.md` zu Release 0.24.0. 🔴 **Der Releaseplan nannte für diesen Nachtrag zwei Anträge; gezählt am 2026-09-22 sind es sieben** – `CR-2026-020`, `-021`, `-023`, `-025`, `-026`, `-029` und `-030`.
