# Änderungsantrag `CR-2026-144`

| Feld | Inhalt |
|---|---|
| Titel | Die Durchsicht der Klasse B, zweiter Bereich – und das Budget statt der Grenze |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-25 |
| Betroffene Artefakte | Durchsicht: `governance/` ohne die Register (vier Dokumente geändert), `checklists/` (sechs), `decision-trees/` (eines), `prompts/` (sechs); Klärungspunkte: `framework/core/05-working-model.md`, `08-skill-conventions.md`, `09-risk-model.md`, `10-error-escalation.md`, `framework/runtime/rules/10-privacy-security.md`, `decision-trees/05-stop-or-escalate.md`; Zeichenbudget: `tests/scripts/validate-framework.py` (Prüfung 4), `tests/scripts/probe-pruefungen.py` (Bündel `sonden_zeichengrenze`), `clients/devin-desktop/CLIENT_PACK.md`, `clients/openai-codex/CLIENT_PACK.md`, die Laufzeit-README von `claude-code` und `devin-desktop`; Geltungsbereich: `build/doc/03`, `04`, `16`, `29`, `32`; `governance/DECISION_LOG.md` (**D-385** bis **D-392**, D-10 präzisiert, `K-138` bis `K-145`); `governance/ADOPTION_REGISTRY.md`; `docs/ROADMAP.md`; `build/doc/00-kopf.md`; `VERSION`, `CHANGELOG.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Regeldokumente, Prüfapparat |
| Art | **PATCH** nach `RELEASE_PROCESS.md` Abschnitt 1: Formulierungen und Berichtigungen gegen das maßgebliche Core-Modul, keine neue Prüfungsnummer, kein Overlay-Feld, kein Overlay muss sich anpassen (gemessen) |
| Dringlichkeit | Posten `1.9.2` nach D-380 und D-384 |
| Status | 🟢 **entschieden am 2026-09-25** (E1 bis E15), umgesetzt mit `1.9.2` |

---

## 1. Anlass

D-380 plant die inhaltliche Durchsicht der Klasse B in drei Bereichen; der zweite sind
`governance/` ohne die Register, `checklists/`, `decision-trees/` und `prompts/`. D-384 hat
diesem Release dazu `K-128` (Kommandozeilenbetrieb, D-10) und `K-130` (Zeichenbudget)
zugewiesen und die Befunde `K-131` bis `K-135` aus `1.9.1` zur Entscheidung gestellt.

## 2. Der Vorbedingungsdurchgang

Gemessen am 2026-09-25 am Stand `v1.9.1`, mit je einer Testinstallation je Pack.

| Messung | Ergebnis |
|---|---|
| Bereich | 42 Dokumente der Klasse B, rund 260 KB (Governance 8, Checklisten 12, Entscheidungsbäume 7, Prompts 13) – 2,5-mal der erste Bereich; alle sechs Bäume tragen ein Mermaid-Diagramm |
| Stets geladen, installiert | `claude-code` 29.773, `openai-codex` 30.274 (Wurzel-Anweisung 12.516, dort ohne Grenze je Datei), `devin-desktop` 20.349 – **bei diesem Pack zählte Prüfung 4 die Summe nicht** |
| Übernehmende Projekte | Pilot (`claude-code`, sechs Regeln ohne Ladebedingung) **38.986** von 40.000; Übungsrepositorium (`devin-desktop`) 22.835 |
| `K-128` | *„Kommandozeilenbetrieb“* als ausgeschlossen in Kapitel 3 (N7), 4, 29 und 32 des Hauptdokuments; D-10 sagt seit `CR-2026-019` *„ohne menschliche Sitzung“* |
| `K-134` | *„Onboarding und Skills vermitteln dies“* – belegt nur `onboarding/QUICKSTART.md`, in keinem `SKILL.md` gefunden |
| `K-135` | `SK-007-P01` ist gegen Stufe **mittel** für Eingabevalidierung gemessen (R3) |

## 3. Vorlage zur Entscheidung

Vorgelegt am 2026-09-25 als Fragen (a) bis (m), angenommen mit *„Ja, das passt. Leg los“*;
`K-138` auf die Zwischenfrage des Owners zum Mehrprojektfall angelegt (*„Ja, lege den
Klärungspunkt K-138 an“*), `K-144` auf seine Frage nach der Token-Last (*„Ja nimm es mit auf“*).

| # | Frage | Entscheidung und Preis |
|---|---|---|
| **E1** | **Regeln der Durchsicht** (a) | D-381 unverändert: kein Regelinhalt, ein Widerspruch wird ein Klärungspunkt (D-385 (a)) |
| **E2** | **Arbeitsweise** (b) | Sechs parallele Durchsichten nach schriftlichem Auftrag, Änderungen nur mit dem Edit-Werkzeug, keine Packnamen als Handelnde; Register, Sonden und Versionen in einem Schritt, die Diffs vom Koordinator gelesen |
| **E3** | **Herleitungen in `RELEASE_PROCESS.md` und `FRAMEWORK_DEV_PROFILE.md`** (c) | Auf die Regel mit D-Verweis gekürzt; jede entfallene Kennung steht in einem anderen Träger (D-385 (b)). Preis: die Erzählung trägt das Decision Log |
| **E4** | **Entscheidungsbäume** (d) | Diagramm und Text gemeinsam gelesen, Abweichungen gemeldet, nicht angeglichen (D-385 (c)) |
| **E5** | **Versionen** (e) | Jedes geänderte Dokument mit Steckbrief um PATCH gehoben (D-385 (d)) |
| **E6** | **`K-128`** (f) | D-10 schließt den Betrieb ohne beobachtende Person aus, nicht eine Oberfläche; Messläufe des Frameworks fallen nicht darunter (D-386) |
| **E7** | **`K-130`** (g) | Summe verbindlich (40.000, Fehler, jedes Pack), Grenze je Datei Warnung (D-387). Preis: 1.014 Zeichen Reserve im Pilot; ob `devin-desktop` lange Regeln kürzt, ist nicht erhoben |
| **E8** | **`K-131`** (h) | Quelle und installierte Fassung in der Regel unterschieden (D-388) |
| **E9** | **`K-132`** (i) | R12 hoch nur für den per Ausnahme zulässigen Modus; der Modus ohne Rückfragen ist keine Stufe (D-389) |
| **E10** | **`K-133`** (j) | *„Ohne Angabe gilt M1“* im Core-Modul (D-390) |
| **E11** | **`K-134`** (k) | Kennungen bleiben, Matrixzeilen heißen *Zeile*; S2 ohne Bereitstellung → E0; Satz über das Anhalten auf das Belegte begrenzt (D-391) |
| **E12** | **`K-135`** (l) | Laufzeitregel an R3/R4 angeglichen, nicht länger (D-392). Preis: in jeder Sitzung lockerer für die indirekte Berührung |
| **E13** | **Versionsart** (m) | PATCH `1.9.2` (D-385 (e)) |
| **E14** | **Mehrprojektfall** (Zwischenfrage) | Als `K-138` angelegt, eingeplant nach `1.10.0` |
| **E15** | **Token-Last** (Zwischenfrage) | Als `K-144` angelegt, eingeplant für `1.11.0`; Vorgabe des Owners: nur sparen, wo keine Schranke nachgibt, Prompt-Caching vorausgesetzt |

> **Empfehlung der Vorbereitung:** E1 bis E13 wie vorgelegt.

---

## 4. Umsetzung

1. Durchsicht nach dem Auftrag `durchsicht-auftrag-192.md` (Ablagebereich der Sitzung) in
   sechs parallelen Durchgängen: `RELEASE_PROCESS`/`FRAMEWORK_DEV_PROFILE`; übrige Governance
   und Entscheidungsbäume; Checklisten; Prompts `README`–`03`, `04`–`07`, `08`–`12`.
2. `K-128`: D-10 präzisiert, Kapitel 3, 4, 29 und 32 des Hauptdokuments (D-386).
3. `K-130`: Prüfung 4 zählt das stets Geladene jedes Packs (bei `devin-desktop` die Regeln mit
   `always_on`) und meldet über 40.000 einen Fehler; die Grenze je Datei ist eine Warnung.
   Bündel `sonden_zeichengrenze` um Sonde 4b und Gegenprobe 4d erweitert, Sonde 4a erwartet
   die Warnung; Zeile R4 der Packs und die Laufzeit-README nachgezogen (D-387).
4. `K-131` bis `K-135` in den Core-Modulen `05`, `08`, `09`, `10`, der Laufzeitregel
   `10-privacy-security.md` und Baum 05 (D-388 bis D-392).
5. Befunde der Durchsicht als `K-139` bis `K-143`, der Mehrprojektfall als `K-138`, die
   Token-Last als `K-144`, der Aufruf von `--mermaid` als `K-145` (Codeposten, `1.10.0`).
6. Versionen, Roadmap (`0.3.2`, Posten `1.11.0`), Decision Log, Bestandsliste, Kopf des
   Hauptdokuments, `VERSION`, Changelog.
7. Beide Projekte mit `--target --update` heben.

## 5. Abnahme

Steht im Protokoll `tests/protocols/2026-09-25-klasse-b-governance.md`.

## 6. Entscheidung

**E1 bis E15 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-25; (a) bis (m) vor
dem Bau vorgelegt und angenommen). Decision Records **D-385** bis **D-392**. Alle vier
zählbaren Kriterien von D-11 bleiben **0**.
