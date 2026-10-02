# Quickstart – Koolie in zehn Minuten ausprobieren

*English version: [QUICKSTART.en.md](QUICKSTART.en.md). Die deutsche Fassung ist maßgeblich.*

Dieser Quickstart installiert Koolie in ein **leeres Übungs-Repository** und zeigt, was dabei entsteht. Er
startet keinen KI-Client und verändert kein bestehendes Projekt. Als Beispiel dient das Client Pack
`claude-code`; die anderen Packs funktionieren genauso.

Für ein **bestehendes** Projekt gilt danach der [Übernahmeleitfaden](.koolie/core/docs/ADOPTION_GUIDE.md).
Wer in einem Projekt neu ist, das Koolie schon nutzt, beginnt mit dem
[Quick-Start des Onboardings](.koolie/core/onboarding/QUICKSTART.md).

## Voraussetzungen

- **Git** und **Python ab 3.8**, ohne Zusatzpakete. Heißt der Aufruf auf deinem System `python3`, nimm ihn
  in allen Befehlen statt `python`.
- Eine Kommandozeile mit POSIX-Shell, unter Windows zum Beispiel Git Bash.
- Koolie selbst, auf einem von zwei Wegen:
  - **über eine Paketquelle:** `uvx koolie` (oder `pipx run koolie`, `npx @renoxar/koolie`). Es ersetzt in
    den Schritten 2 und 3 den Aufruf `python .koolie/core/install.py`, und du kannst aus jedem Verzeichnis
    starten. Wer `pip install koolie` nutzt und `koolie` danach nicht findet, ruft `python -m koolie` auf.
  - **aus dem entpackten Release-Archiv oder einem Klon:** Die Schritte 1 bis 4 laufen dann aus dessen
    Wurzelverzeichnis. Statt Schritt 2 gehen auch die Starter `install.cmd` (Windows) und `install.command`
    (macOS); sie fragen dieselben Angaben ab.

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

Über eine Paketquelle: `uvx koolie --target ../koolie-uebung --client claude-code`. Ohne Argumente startet
`uvx koolie` einen Dialog mit dem aktuellen Verzeichnis als Vorgabe.

Der Installer kopiert den Kern (`.koolie/core/`) ins Übungs-Repository, legt die Dateien an, die der Client
braucht, und nennt am Ende die nächsten Schritte für ein echtes Projekt.

⚠️ Unter Windows darf kein Pfad länger als 259 Zeichen werden. Liegt das Übungs-Repository zu tief, hält der
Installer vor der ersten Kopie an. Dann einen kürzeren Ort wählen, in Git Bash etwa `/c/koolie-uebung`, und
ihn in allen Befehlen statt `../koolie-uebung` einsetzen.

## Schritt 3: Einen anderen Client wählen (optional)

```bash
python .koolie/core/install.py --list-clients
```

zeigt die verfügbaren Client Packs. Was jeder Client technisch durchsetzt, steht in der
[Übersicht der Client Packs](.koolie/core/clients/README.md), Abschnitt 6; welche Dateien ein Pack anlegt, im
[Laufzeitglossar](.koolie/core/docs/RUNTIME_GLOSSARY.md). Für diesen Quickstart genügt `claude-code`.

## Schritt 4: Ansehen, was entstanden ist

| Pfad im Übungs-Repository | Was es ist |
|---|---|
| `CLAUDE.md` | die **Anweisungsdatei**, die der Client beim Start lädt – mit den Regeln von Koolie, zum Beispiel *„Nie: `git push` …“* |
| `.claude/settings.json` | die **Berechtigungsdatei**: was der Client verweigert (`deny`), erfragt (`ask`) oder ohne Rückfrage darf (`allow`), dazu die Hooks |
| `.claude/rules/`, `.claude/skills/`, `.claude/agents/` | Kurzfassungen der Regeln, die Skills (`/koolie-plan` und andere) und ein nur lesendes Review-Profil |
| `.koolie/core/` | der **Kern** – in jedem Projekt gleich, nie von Hand ändern |
| `.koolie/project-overlay/` | das **Project Overlay** – die Projektkonfiguration, die das Team ausfüllt |

Die Sperre für `git push` aus der [README](README.md#was-durchgesetzt-wird--und-was-nicht) steht in der
Berechtigungsdatei:

```bash
grep -n "git push" ../koolie-uebung/.claude/settings.json
```

`Bash(git push:*)` erscheint zweimal: in `permissions.deny`, wo der Client die Sperre liest, und in
`_core_rules_integrity.deny_must_contain`, wogegen der Validator die Datei prüft.

## Schritt 5: Den Stand festhalten und prüfen

```bash
echo "__pycache__/" > ../koolie-uebung/.gitignore
git -C ../koolie-uebung add -A
git -C ../koolie-uebung commit -m "Koolie installiert"
cd ../koolie-uebung
python .koolie/core/tests/scripts/validate-framework.py
```

**Erwartet:** `Ergebnis: 0 Fehler, 0 Warnungen`. Der Validator prüft unter anderem, ob die Kernregeln der
Berechtigungsdatei vollständig sind. Die `.gitignore` hält den Python-Bytecode der Werkzeuge aus dem
Repository; ohne sie gibt es eine Warnung.

## Schritt 6: Sehen, was für den echten Einsatz fehlt

```bash
python .koolie/core/tests/scripts/validate-framework.py --check-overlay-ready
```

**Erwartet:** mehrere `FEHLER` mit `enthält offene <TBD>-Werte` zu Dateien unter `.koolie/project-overlay/`
und zur Overlay-Regel in `.claude/rules/`. Das ist richtig so: Das Overlay ist noch leer. Bis es ausgefüllt,
geprüft und aktiv ist, arbeitet der Agent im Projekt nur lesend. Welche Werte ein Projekt einträgt und wer sie
freigibt, beschreibt der [Übernahmeleitfaden](.koolie/core/docs/ADOPTION_GUIDE.md).

## Schritt 7: Den Client dagegen laufen lassen (optional)

Mit installiertem Claude Code kannst du im Übungs-Repository eine Sitzung starten und den Assistenten bitten,
einen Commit zu pushen. **Erwartet:** Er lehnt ab; versucht er es trotzdem, weist der Client den Aufruf
zurück. So wurde es mit Claude Code 2.1.274 gemessen
([Protokoll](.koolie/core/tests/protocols/2026-09-17-sitzungstest-schranken.md)); für diesen Quickstart ist es
nicht erneut geprüft. Ein Modell kann sich anders verhalten – genau dafür gibt es die technische Sperre.

## Aufräumen

Das Übungs-Repository `../koolie-uebung` kann danach gelöscht werden.

## Wie es weitergeht

- [README](README.md): was Koolie ist, für wen es gedacht ist und welche Clients es unterstützt.
- [Übernahmeleitfaden](.koolie/core/docs/ADOPTION_GUIDE.md): Aufnahme in ein bestehendes Projekt, Aktualisierung, Kosten, Einsatzarchitektur und das Nebeneinander mit einem anderen Agenten-Rahmenwerk.
- [Übersicht der Client Packs](.koolie/core/clients/README.md): Fähigkeitsmatrizen und ihre Belege.
