# Koolie

**Governance für KI-Coding-Assistenten – eine Regelquelle für jeden Client, technisch durchgesetzt, wo der Client es kann.**

[![PyPI](https://img.shields.io/pypi/v/koolie)](https://pypi.org/project/koolie/)
[![npm](https://img.shields.io/npm/v/@renoxar/koolie)](https://www.npmjs.com/package/@renoxar/koolie)
[![Lizenz: GPL-3.0](https://img.shields.io/badge/Lizenz-GPL--3.0-blue)](LICENSE)

*English: [README.en.md](README.en.md)*

Wer mit KI-Coding-Assistenten im Team arbeitet, braucht mehr als eine Anweisungsdatei: gemeinsame Regeln für
jeden Assistenten, technische Sperren dort, wo eine Regel nicht verletzt werden darf, und klare Stellen, an
denen ein Mensch entscheidet. Koolie bringt genau das in ein bestehendes Git-Repository – und sagt für jeden
Client offen, welche Regel er wirklich erzwingt und welche nur als Anweisung wirkt.

## Schnellstart

Im Verzeichnis des Projekts:

```bash
uvx koolie                  # oder: pipx run koolie · npx @renoxar/koolie
```

Der Befehl holt Koolie, zeigt das aktuelle Verzeichnis als Projekt an und fragt nach dem KI-Client. Danach
liegen im Projekt die Anweisungsdatei, die Berechtigungen und ein Schutz-Hook für diesen Client. Ohne
Paketquelle geht es mit dem Release-Archiv und den Startern `install.cmd` / `install.command`.

**Erst ausprobieren?** Der [Quickstart](QUICKSTART.md) installiert Koolie in ein leeres Übungs-Repository – in
zehn Minuten, ohne einen KI-Client zu starten.

## So funktioniert es

```text
  Kern  .koolie/core/            Project Overlay  .koolie/project-overlay/
  Regeln, Skills, Checklisten,   Pfade, Freigabewege, Projektdokumente
  Schutz-Hook, Validator         – gehört dem Projekt
            │                               │
            └───────────────┬───────────────┘
                            ▼
                  Client Pack je KI-Client
       Anweisungsdatei · Berechtigungen · Hooks · Skills
       (z. B. CLAUDE.md und .claude/ für Claude Code)
```

- **Ein Kern für alle Clients.** Regeln und Skills stehen einmal, werkzeugneutral; ein Team mit gemischten
  Werkzeugen teilt dieselben Regeln.
- **Das Projekt bleibt bei sich.** Projektwerte leben im Overlay. Ein neues Release übernimmt ein Projekt mit
  demselben Befehl: Er erkennt den vorhandenen Kern und bietet das Update an, das Overlay bleibt unberührt.
- **Kontrollstufen statt Vertrauen.** Kleine Aufgaben erledigt der Assistent selbst, ab „mittel“ braucht er
  einen bestätigten Plan, bei „hoch“ eine ausdrückliche Freigabe.

## Was durchgesetzt wird – und was nicht

| Art der Regel | Was das heißt | Beispiel |
|---|---|---|
| **Technisch** | Der Client erzwingt sie, egal was das Modell tut | `git push` ist gesperrt; Secret-Dateien sind lesegeschützt |
| **Als Anweisung** | Die Regel steht im Kontext des Modells; es kann ihr folgen | „Ändere keine Dateien außerhalb des freigegebenen Scopes“ |
| **Beim Menschen** | Freigaben, Reviews, Entscheidungen | Ein Release gibt ein Mensch frei |

Jedes Client Pack führt eine **Fähigkeitsmatrix**, die jede Zusage einer dieser Arten zuordnet – mit Beleg aus
einer Messung am Client. Koolie ergänzt eine gute Standardkonfiguration (Branch-Schutz, CI, verwaltete
Einstellungen); es ersetzt sie nicht.

## Unterstützte Clients

| Client | Pack | Stand |
|---|---|---|
| Claude Code | [`claude-code`](.koolie/core/clients/claude-code/CLIENT_PACK.md) | Pilot |
| Cursor | [`cursor`](.koolie/core/clients/cursor/CLIENT_PACK.md) | Pilot |
| Devin Desktop | [`devin-desktop`](.koolie/core/clients/devin-desktop/CLIENT_PACK.md) | Pilot |
| Kiro | [`kiro`](.koolie/core/clients/kiro/CLIENT_PACK.md) | Pilot |
| OpenAI Codex CLI | [`openai-codex`](.koolie/core/clients/openai-codex/CLIENT_PACK.md) | Pilot, Inbetriebnahme nur mit Freigabe der Sicherheitsverantwortlichen |

*Pilot* heißt: vollständig gebaut, an realen Installationen gemessen, für den begleiteten Einsatz gedacht. Die
Grenzen jedes Clients stehen in seinem Pack.

## Für wen?

- **Entwicklungsteams**, die KI-Assistenten im Alltag nutzen und gemeinsame, prüfbare Regeln wollen.
- **Technische Verantwortliche** – Teamleitung, Architektur, Sicherheit, Datenschutz –, die belegen müssen,
  was ein Werkzeug technisch einhält.

Nicht gedacht ist Koolie für den vollständig autonomen Betrieb eines Agenten ohne menschliche Freigaben.

## Dokumentation

| Thema | Wo |
|---|---|
| Ausprobieren in zehn Minuten | [`QUICKSTART.md`](QUICKSTART.md) |
| In ein Projekt übernehmen, aktualisieren, Kosten | [Übernahmeleitfaden](.koolie/core/docs/ADOPTION_GUIDE.md) |
| Erster Arbeitstag in einem Projekt mit Koolie | [Onboarding](.koolie/core/onboarding/QUICKSTART.md) |
| Client Packs und Fähigkeitsmatrizen | [`clients/README.md`](.koolie/core/clients/README.md) |
| Die Regeln selbst | [`framework/core/`](.koolie/core/framework/core/) |
| Änderungen und Planung | [`CHANGELOG.md`](.koolie/core/CHANGELOG.md) · [`ROADMAP.md`](.koolie/core/docs/ROADMAP.md) |
| Am Framework mitarbeiten | [`CONTRIBUTING.md`](CONTRIBUTING.md) |

## Warum „Koolie“?

Ein Koolie ist ein australischer Hütehund. Er treibt die Herde nicht und ersetzt den Schäfer nicht – er hält
sie beisammen, in Richtung und an den Grenzen. Genau das soll dieses Framework mit einem KI-Assistenten tun.

## Lizenz

[GPL-3.0](LICENSE) mit einer Zusatzerlaubnis: Dateien, die aus den Vorlagen entstehen, und jede Ausgabe der
Werkzeuge gehören dem Projekt, das sie erzeugt. Wer Koolie nur benutzt – auch kommerziell –, hat daraus keine
Pflichten; die Einzelheiten stehen in [`LICENSE-HINWEIS.md`](.koolie/core/LICENSE-HINWEIS.md).
Copyright © 2026 `<FRAMEWORK_OWNER>`.
