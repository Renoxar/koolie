# Laufzeitschicht `.codex/` – was hier liegt und wem es gehört

Diese Ablage ist die **Laufzeitform** des Frameworks für den Client `openai-codex`. Die kanonische, werkzeugneutrale Langform steht in `.koolie/core/framework/`; was hier liegt, ist daraus erzeugt (D-02). **Inhaltliche Änderungen gehören in den Kern und laufen als Änderungsantrag** (`.koolie/core/governance/CHANGE_REQUEST_TEMPLATE.md`).

## Was hier liegt

| Pfad | Inhalt | Wem es gehört |
|---|---|---|
| `../AGENTS.md` | Wurzel-Anweisung (Ebene 1). **Sie nennt die Regeldateien unten** – dieser Client lädt sie nicht von sich aus | Framework |
| `rules/00-*.md`, `rules/10-*.md`, `rules/15-*.md` | Regeltexte des Frameworks (Ebene 3) | Framework |
| `rules/20-project-overlay.md` | Laufzeitfassung des Project Overlays (Ebene 4) | Projekt |
| `rules/40-tech-*.md`, `rules/30-*.md` | Technology und Role Packs (Ebenen 5 und 6) | Projekt |
| `rules/koolie.rules` | **Befehlsregeln** – die Befehlsseite der Berechtigungsschicht | Framework |
| `config.toml` | **Rechteprofil** – die Pfadseite der Berechtigungsschicht, dazu die Projektwerte | Projekt (aus dem Kern erzeugt) |
| `hooks.json` | Schutz-Hook und Statusmeldung | Framework |
| `skills/fw-*/` | Skills des Frameworks | Framework |
| `agents/` | Agentenprofile | Framework |

## Drei Dinge, die bei diesem Client anders sind

**1. Die Regeldateien wirken über ihre Nennung, nicht über einen Ladetrigger.** Dieser Client lädt von sich aus **nur** `AGENTS.md`. Eine Regeldatei in diesem Verzeichnis wirkt, weil die Wurzel-Anweisung sie nennt und zu lesen aufgibt – nicht, weil die Engine sie einspeist. *Was eine Nennung bewirkt, hängt am Modell.*

**2. Ohne Vertrauenseintrag trägt diese Ablage nichts.** `config.toml`, `hooks.json` und `rules/*.rules` laden erst, wenn das Projekt in der **Benutzerkonfiguration des Clients** als vertraut eingetragen ist; der Schutz-Hook braucht darüber hinaus sein **eigenes** Vertrauen. Beides liegt außerhalb dieses Repositoriums und ist je Arbeitsplatz zu setzen. **Jede Hebung des Frameworks ändert den Hook – und damit sein Vertrauen.**

**3. Eine Datei namens `AGENTS.override.md` würde die Wurzel-Anweisung vollständig ersetzen.** Nicht ergänzen: ersetzen. Das Framework legt sie nicht an und liefert auch keine Vorlage dafür; `validate-framework.py` meldet sie, wenn sie da ist.

## Was hier **nicht** liegt

Keine Geheimnisse, keine Zugangsdaten, keine Kunden- oder Personennamen. Die Regeln dazu stehen in `rules/10-privacy-security.md`; der Validator prüft es, und der Schutz-Hook blockiert eine Werkzeugeingabe, die ein Muster dieser Kategorien trägt.

## Prüfen

```text
python .koolie/core/tests/scripts/validate-framework.py --strict-overlay
```
