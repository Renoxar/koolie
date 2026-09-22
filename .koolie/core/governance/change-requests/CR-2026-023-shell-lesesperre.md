# Änderungsantrag `CR-2026-023`

| Feld | Inhalt |
|---|---|
| Titel | Für Shell-Befehle bestand keine Lesesperre – die Abbildung erreichte den Matcher, nicht die Prüfung |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | `tests/scripts/hook-check-secrets.py`, `tests/scripts/validate-framework.py` (Prüfung 16 neu) |
| Ebene laut Entscheidungsbaum 6 | Schutzmechanismus und Prüfung; keine Regeländerung |
| Art | Behebung von `AP2-CC-16` (neu, Schwere hoch) und `AP2-CC-15` |
| Dringlichkeit | erhöht – betrifft die Vertraulichkeit von Secrets |

## 1. Anlass und Problem

`AP2-CC-15` hielt fest: Die Lesesperre gilt für `Read`, nicht für Shell-Lesebefehle; die
`deny`-Liste führt 21 Bash-Regeln und keine fürs Lesen. Aufgefangen würde das vom Schutz-Hook.
Bei der Prüfung, ob der Hook das leistet, kam ein schwererer Befund zutage.

### AP2-CC-16 – Die Abbildung erreichte den Matcher, nicht die Prüfung

Das Manifest jedes Client Packs bildet die Verben der Kernquelle auf die Werkzeugnamen seines
Clients ab:

```json
"hook_tools": {"exec": ["Bash"], "write": ["Edit", "Write", "NotebookEdit"]}
```

Diese Abbildung erzeugt den **Matcher** der Hook-Konfiguration – `"matcher":
"Bash|Edit|Write|NotebookEdit"`. Der Hook wird also aufgerufen. Aber er verglich intern gegen
die **generischen** Verbnamen:

```python
WRITE_TOOLS = ("edit", "write", "notebookedit")
if tool_name in WRITE_TOOLS + ("exec",):
```

Der Client schickt `Bash`. Das Ergebnis, direkt nachgestellt:

| Eingabe | Ergebnis |
|---|---|
| `{"tool_name": "Bash", "command": "cat .env"}` | **nicht blockiert**, Exit 0 |
| `{"tool_name": "Write", "file_path": ".env"}` | blockiert, Exit 2 |

**Der Verlust war clientspezifisch.** Bei `devin-desktop` heißt das Verb `exec`, dort griff die
Prüfung. Bei `claude-code` nicht – seit acht Releases. Genau die Lage, gegen die D-26 gerichtet
ist: eine Semantikabbildung, die eine Zusage verliert. Neu ist die Ebene: **Abgebildet wurde die
erzeugte Konfiguration, nicht das Skript, das die Zusage durchsetzt.**

### AP2-CC-15 – Die Pfadmuster treffen einen Pfad im Befehl nicht

Selbst mit richtigem Werkzeugnamen hätte die Prüfung `cat .env` nicht getroffen. Die Muster
verlangen vor dem Pfad einen Zeilenanfang oder ein Trennzeichen:

| Zeichenkette | Treffer |
|---|---|
| `.env`, `./.env`, `cat /pfad/.env` | ja |
| `cat .env`, `grep X .env` | **nein** |

**Beide Ursachen zusammen heißen: Für Shell-Befehle bestand keine Lesesperre.**

## 2. Vorgeschlagene Änderung

**Die Werkzeugnamen kommen aus den Manifesten.** Der Hook liest `hook_tools` aus **allen**
Client Packs – er liegt einmal im Kern und wird von allen geteilt; ein zusätzlich erkannter Name
ist eine Verschärfung. Dasselbe Prinzip, mit dem Prüfung 14 seit D-28 die Clientnamen aus den
Pack-Kennungen liest, statt sie zu pflegen. Fehlt jedes Manifest, gilt die bisherige Basisliste:
Ein Hook, der wegen einer fehlenden Datei gar nichts mehr blockiert, wäre die schlechtere Lage.

**Ein Shell-Befehl wird tokenisiert.** Für ausführende Werkzeuge wird die Eingabe an
Shell-Trennzeichen zerlegt und jedes Token wie eine Pfadangabe geprüft. Keine neuen Muster – nur
eine andere Zerlegung.

**Die Pfadlisten werden nach Schutzziel getrennt.** Sie standen in einer, und das verwischte den
Unterschied:

| Liste | Schutzziel | Gilt für |
|---|---|---|
| `SECRET_PATH_PATTERNS` | **Vertraulichkeit** – darf auch nicht *gelesen* werden | alle Werkzeuge, auch ausführende |
| `STRUCTURE_PATH_PATTERNS` | **Integrität** – darf nicht *geschrieben* werden | nur schreibende Werkzeuge |

Ohne die Trennung hätte die Erweiterung ein `git diff leitwerk-core/framework/core/…` blockiert –
eine Operation, die das Framework mit P4 („Befunde mit Fundstellen") ausdrücklich voraussetzt.

**Prüfung 16 setzt es durch, und zwar an der Wirkung.** Der Validator ruft den Hook je
abgebildetem Werkzeugnamen mit einer Sonde auf, die er blockieren muss. Ein Listenvergleich hätte
genügt, um die beiden Listen gleichzuhalten – aber genau eine solche Prüfung ist an diesem Befund
vorbeigekommen.

## 3. Was dieser Antrag nicht ändert

- **Keine Regel und keine Zusage.** Der Hook tut, was die Fähigkeitsmatrix seit jeher ausweist.
- **Kein neues Muster.** Die Secret- und Strukturpfade sind unverändert; sie sind aufgeteilt,
  nicht erweitert.
- **Das fail-open-Verhalten bleibt.** Die Umstellung auf fail-closed ist weiterhin ein eigener
  Punkt der Roadmap.
- **Die `deny`-Liste bleibt unverändert.** Sie führt weiterhin keine Regel für Lesebefehle; der
  Schutz kommt jetzt vom Hook, wo er hingehört.

## 4. Grenze der Zusage

**Die Sperre schützt gegen Versehen, nicht gegen Absicht.** Geprüft wird die Zeichenkette des
Befehls. Wer den Pfad verschleiert – `cat .e''nv`, eine Variable, ein base64-Umweg, ein Skript,
das die Datei öffnet – wird nicht erfasst. Das ist keine Lücke dieser Änderung, sondern die
Grenze jeder textuellen Prüfung; sie ist hier ausgewiesen, damit die Fähigkeitsmatrix nicht mehr
verspricht, als sie hält.

Der Fall, gegen den die Sperre wirkt, ist der häufige: ein beiläufiges `cat .env`, ein
`grep -r API .` über ein Verzeichnis mit Secret-Dateien.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Werkzeugnamen aus den Manifesten oder feste Liste? | **Aus den Manifesten**, aus allen Packs – wie D-28 es für die Clientnamen tut | Der Hook liest beim Start bis zu zwei kleine Dateien |
| E2 | Schutzziele trennen? | **Ja.** Ohne die Trennung blockiert die Erweiterung lesende Kernzugriffe | Eine Lockerung gegenüber dem bisherigen `exec`-Verhalten bei `devin-desktop`, wo ein `git diff` auf `framework/core/` blockiert war. Begründet: Lesen war dort nie das Schutzziel |
| E3 | Prüfung 16 durch Aufruf oder Listenvergleich? | **Durch Aufruf.** Ein Listenvergleich belegt Übereinstimmung, nicht Wirkung | Zwei bis acht Prozessstarts je Validatorlauf |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | `<TBD: angenommen / abgelehnt / mit Auflagen>` |
| Datum | `<TBD>` |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | `<TBD: E1, E2 und E3 einzeln entscheiden>` |
