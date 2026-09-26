# Quickstart – Koolie in zehn Minuten ausprobieren

*English version: [QUICKSTART.en.md](QUICKSTART.en.md). Die deutsche Fassung ist maßgeblich.*

Dieser Quickstart installiert Koolie in ein **leeres Übungs-Repository** und zeigt, was dabei entsteht. Er
startet keinen KI-Client und verändert kein bestehendes Projekt. Als Beispiel dient das Client Pack
`claude-code`; jedes andere Pack funktioniert genauso (Schritt 3).

Wer Koolie in ein **bestehendes** Projekt übernehmen will, liest danach den
[Übernahmeleitfaden](.koolie/core/docs/ADOPTION_GUIDE.md). Wer in einem Projekt, das Koolie schon nutzt, den
ersten Arbeitstag hat, beginnt mit dem [Quick-Start des Onboardings](.koolie/core/onboarding/QUICKSTART.md).

## Voraussetzungen

- **Git** und **Python ab 3.8** (ohne Zusatzpakete). Heißt der Aufruf auf dem System `python3`, gilt er in allen
  Befehlen unten statt `python`.
- Eine Kommandozeile mit POSIX-Shell – unter Windows zum Beispiel Git Bash. Schritt 2 lässt sich auch mit den
  Startern `install.cmd` (Windows) oder `install.command` (macOS) in der Wurzel des Release-Archivs erledigen;
  sie fragen dieselben Angaben ab. Die übrigen Schritte brauchen die Kommandozeile.
- Koolie selbst: das **entpackte Release-Archiv** oder ein **Klon** dieses Repositorys. Die Schritte 1 bis 4
  laufen aus dessen Wurzelverzeichnis, ab Schritt 5 im Übungs-Repository.

## Schritt 1: Ein Übungs-Repository anlegen

```bash
mkdir ../koolie-uebung
git -C ../koolie-uebung init
echo "# Übungsprojekt" > ../koolie-uebung/README.md
git -C ../koolie-uebung add README.md
git -C ../koolie-uebung commit -m "Start"
```

## Schritt 2: Koolie installieren

```bash
python .koolie/core/install.py --target ../koolie-uebung --client claude-code
```

`--target` kopiert nur den Kern (`.koolie/core/`) in das Übungs-Repository und legt dort die Dateien an, die
der Client braucht. Am Ende nennt der Installer die nächsten Schritte für ein echtes Projekt.

⚠️ Unter Windows darf kein kopierter Pfad länger als 259 Zeichen werden. Liegt das Übungs-Repository zu tief,
hält der Installer vor der ersten Kopie an und nennt, wie viele Zeichen zu viel sind – dann einen kürzeren Ort
wählen und `../koolie-uebung` in allen Befehlen durch ihn ersetzen, in Git Bash zum Beispiel `/c/koolie-uebung`.

## Schritt 3: Einen anderen Client wählen (optional)

```bash
python .koolie/core/install.py --list-clients
```

zeigt die verfügbaren Client Packs. Welcher Client was technisch durchsetzt, steht in der
[Übersicht der Client Packs](.koolie/core/clients/README.md), Abschnitt 6. Die Dateinamen in Schritt 4 gelten
für `claude-code`; welche Dateien ein anderes Pack anlegt, nennt das
[Laufzeitglossar](.koolie/core/docs/RUNTIME_GLOSSARY.md). Für diesen Quickstart genügt `claude-code`.

## Schritt 4: Ansehen, was entstanden ist

| Pfad im Übungs-Repository | Was es ist |
|---|---|
| `CLAUDE.md` | die **Anweisungsdatei**, die der Client beim Start lädt – mit den Regeln des Frameworks, zum Beispiel *„Nie: `git push` …“* |
| `.claude/settings.json` | die **Berechtigungsdatei**: Was der Client technisch verweigert (`deny`), erfragt (`ask`) oder ohne Rückfrage darf (`allow`), dazu die Hooks |
| `.claude/rules/`, `.claude/skills/`, `.claude/agents/` | Kurzfassungen der Regeln, die Skills des Frameworks und ein nur lesendes Review-Profil |
| `.koolie/core/` | der **Kern** – in jedem Projekt gleich, nie von Hand ändern |
| `.koolie/project-overlay/` | das **Project Overlay** – die Projektkonfiguration, die das Team ausfüllt |

Die Sperre aus dem Beispiel der [README](README.md#wie-sieht-ein-konkreter-einsatz-aus) steht in
`.claude/settings.json`:

```bash
grep -n "git push" ../koolie-uebung/.claude/settings.json
```

Die Ausgabe nennt `Bash(git push:*)` zweimal: in `permissions.deny`, wo der Client die Sperre liest, und in
`_core_rules_integrity.deny_must_contain`, der Liste der Kernregeln, gegen die der Validator die Datei prüft.

## Schritt 5: Den Stand festhalten und prüfen

```bash
echo "__pycache__/" > ../koolie-uebung/.gitignore
git -C ../koolie-uebung add -A
git -C ../koolie-uebung commit -m "Koolie installiert"
cd ../koolie-uebung
python .koolie/core/tests/scripts/validate-framework.py
```

**Erwartet:** `Ergebnis: 0 Fehler, 0 Warnungen`. Der Validator prüft unter anderem, dass die Kernregeln der
Berechtigungsdatei vollständig sind. Die `.gitignore` gehört dazu, weil die Werkzeuge des Kerns bei jedem Lauf
Python-Bytecode erzeugen; ohne sie meldet der Validator eine Warnung.

## Schritt 6: Sehen, was für den echten Einsatz fehlt

```bash
python .koolie/core/tests/scripts/validate-framework.py --check-overlay-ready
```

**Erwartet:** mehrere Zeilen mit `FEHLER` und `enthält offene <TBD>-Werte` zu Dateien unter
`.koolie/project-overlay/` und zur Overlay-Regel in `.claude/rules/`. Das ist richtig so: Das Overlay ist noch
nicht ausgefüllt. Solange es nicht ausgefüllt, geprüft und auf aktiv gesetzt ist, arbeitet der Agent im
Projekt nur lesend. Welche Werte
ein Projekt eintragen muss und wer sie freigibt, beschreibt der
[Übernahmeleitfaden](.koolie/core/docs/ADOPTION_GUIDE.md).

## Schritt 7: Den Client dagegen laufen lassen (optional)

Wer Claude Code installiert hat, kann im Übungs-Repository eine Sitzung starten und den Assistenten bitten,
einen Commit zu pushen. **Erwartet**, weil so gemessen: Der Assistent lehnt ab; versucht er es trotzdem,
weist der Client den Aufruf zurück. Für diesen Quickstart ist das **nicht erneut geprüft** worden – gemessen
wurde es am 2026-09-17 mit Claude Code 2.1.274
([Protokoll](.koolie/core/tests/protocols/2026-09-17-sitzungstest-schranken.md)). Ein Modell kann sich
anders verhalten – deshalb gibt es die technische Sperre, und deshalb nennt die Fähigkeitsmatrix ihre Grenze.

## Aufräumen

Das Übungs-Repository kann danach gelöscht werden – aus dem Verzeichnis, in dem Schritt 1 lief, ist es
`../koolie-uebung`.

## Wie es weitergeht

- [README](README.md): was Koolie ist, für wen es gedacht ist, welche Clients in welchem Stand unterstützt werden.
- [Übernahmeleitfaden](.koolie/core/docs/ADOPTION_GUIDE.md): Aufnahme in ein bestehendes Projekt, Aktualisierung, Kosten.
- [Übersicht der Client Packs](.koolie/core/clients/README.md): Fähigkeitsmatrizen und ihre Belege.
