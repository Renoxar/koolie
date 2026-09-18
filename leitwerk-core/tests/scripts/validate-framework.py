#!/usr/bin/env python3
"""
validate-framework.py – Strukturelle Validierung des Frameworks und eines Project Overlays.

Aufruf (im Wurzelverzeichnis des Repositorys):
    python3 leitwerk-core/tests/scripts/validate-framework.py [--strict-overlay]
        [--check-overlay-ready] [--mermaid] [--root PFAD]

Prüft (statisch, ohne laufenden KI-Client):
  1. Pflichtdateien und -verzeichnisse
  2. Berechtigungsdatei: gültiges JSON, Kernregeln vollständig (Abgleich gegen die
     Kernquelle framework/runtime/permissions.json), keine Kernverbote in allow
  3. weitere JSON-Dateien der Laufzeitschicht (Hooks, mcp-Vorlage): gültiges JSON
  4. .devin/rules/*.md: Frontmatter (description, trigger, globs), Zeichenlimits
  5. Skills (.devin/skills/ und die Quellablagen der Packs): Pflichtdateien, Frontmatter,
     Metadatenblock, Pflichtabschnitte,
     Trigger-Regel (schreibende Skills nur user-getriggert), Beispiele und Testfälle
  6. Verbotene Inhalte (ohne erzeugte Lockdateien): Secret-Muster – dieselben Kategorien,
     die der Schutz-Hook in einer Werkzeugeingabe blockiert –, E-Mail-Adressen, IP-Adressen,
     interne Hostnamen, URLs außerhalb der Quellen-Allowlist, projektspezifische Sperrbegriffe
     (project-overlay/forbidden-terms.txt)
  7. Platzhalter: nur registrierte Platzhalter (leitwerk-core/docs/PLACEHOLDER_REGISTRY.md)
  8. Overlay-Manifest: Kopfschlüssel, Pflichtfelder je Dokumenteintrag, Aufzählungswerte
  9. --strict-overlay: der **aktive** Zustand - keine offenen <TBD> in
     sicherheitsrelevanten Overlay-Feldern; Status aktiv an *jeder* Stelle, an der das
     Overlay ihn erklärt (Steckbrief und Aktivierung)
 9a. --check-overlay-ready: die **Aktivierungsreife eines Kandidaten** - derselbe Inhalt,
     aber der Status ist noch nicht aktiv und an allen Stellen gleich. Ohne diese Pruefung
     verlangte der dokumentierte Ablauf, was er herstellen sollte (B08, D-57)
 10. --mermaid: Syntaxprüfung aller Mermaid-Blöcke mit mmdc (falls installiert)
 11. Codeblöcke mit vier oder mehr Backticks (brechen die Dokumentassemblierung) –
     einschließlich der Quellen unter <CORE_DIR>/build/doc, aus denen sie entsteht
 12. Querverweise (FW-KO-04): Markdown-Links und in Backticks genannte Framework-Pfade
     zeigen auf existierende Dateien oder Verzeichnisse
 13. Versionskette (FW-VN-01): Overlay-Version an allen drei Ablageorten gleich, Steckbrief-
     angabe zur kompatiblen Framework-Version passend zu <CORE_DIR>/VERSION, und das
     Versionsfeld jedes Kernartefakts in der Form MAJOR.MINOR.PATCH
 14. Akteursbezeichnung (D-02, D-28): Der Kern nennt keinen Client als Handelnden. Die
     Namen stammen aus den Pack-Kennungen; der Produktname mit Zusatz bleibt zulaessig,
     historische Dokumente sind ausgenommen
 15. Hook-Interpreter (AP2-CC-13, D-29): Der Interpreter der Hook-Aufrufe startet auf
     dieser Maschine wirklich Python. Geprueft wird die Wirkung, nicht die Anwesenheit
     des Namens - unter Windows ist 'python3' haeufig ein Alias ohne Interpreter
 16. Hook-Abdeckung (AP2-CC-16, D-30): Der Schutz-Hook erkennt jeden Werkzeugnamen,
     den ein Client Pack in hook_tools abbildet. Geprueft durch Aufruf mit einer Sonde,
     die er blockieren muss - ein Listenvergleich belegt Uebereinstimmung, nicht Wirkung
 17. Fail-closed (D-31): Der durchsetzende Hook verhaelt sich so, wie das Pack es zusagt -
     geprueft am Skript und an der erzeugten Konfiguration, nicht am Manifestfeld
 18. Hook-Ablageort (D-32): keine verwaiste Hook-Datei neben der wirksamen, und keine
     root-template-Vorlage, die eine solche Datei als geliefertes Artefakt fuehrt
 19. Quellenauskunft (D-34, D-37): Jedes Client Pack fuehrt den Abschnitt
     "Anweisungs- und Konfigurationsquellen ausserhalb des Projekts", mit mindestens einer
     Quellenzeile oder einem datierten Abwesenheitsbeleg. Belegt Anwesenheit, nicht
     Richtigkeit - siehe Kopfkommentar der Pruefung
 20. Dokumenttabellen (CR-2026-036): Die Client-Spalten von PLACEHOLDER_REGISTRY.md und
     RUNTIME_GLOSSARY.md stimmen je Pack mit dessen manifest.json ueberein. Belegt
     Uebereinstimmung, nicht Richtigkeit
 21. Hook-Skripte (D-30, CR-2026-037): Ein Hook-Skript des Kerns leitet seine Pfade nicht
     aus einer clientgebundenen Umgebungsvariablen oder Laufzeitschicht ab; es bekommt sie
     als Argumente aus der Semantikabbildung
 22. Importsteuerung (D-37): Die installierte Berechtigungsdatei fuehrt sie so, wie das
     Manifest sie abbildet. Belegt Anwesenheit und Uebereinstimmung, nicht Wirkung -
     die Benutzerkonfiguration der Arbeitsstation hat Vorrang (K-27)
 23. Normative Kommentare (D-38): kein normatives Schluesselwort in einem HTML-Kommentar
     der Laufzeitartefakte - ein Kommentar erreicht nicht jede Sitzung (ERH-01, K-28)
 24. Regelablage (D-36): In der Vorlage der Regelablage liegt nur, was dem Nummernschema
     der Regeltexte folgt; erklaerender Text steht in der Laufzeit-README eine Ebene hoeher
 25. Ausfall mit Ersatz (D-41): Eine Matrixzeile eines Client Packs auf [NICHT ABBILDBAR]
     benennt den Ersatz - oder haelt ausdruecklich fest, dass es keinen gibt
 26. Werkzeugabwesenheit (D-47): Eine erklaerte Abwesenheit in hook_tools_absent ist
     belegt und folgerichtig - sie darf keine Werkzeugklasse aus der Durchsetzung nehmen
 27. Zusagenfelder (D-50): Verwirft ein Pack das Skill-Frontmatter-Feld permissions oder
     triggers, benennt es den Ersatz - ein zusagentragendes Feld entfaellt nicht ersatzlos
 28. Lesesperre gegen Schreibsperre (D-55, B07): Die Deklaration von <EXCLUDED_PATHS>
     nennt keinen Strukturpfad des Frameworks. Diese Pfade sind schreibgeschuetzt, nicht
     lesegesperrt - als Ausschluss erzeugen sie eine Lesesperre auf die eigenen Regeln
 29. K3-Kategorien (D-52, B09): Kurzform, Langform, Laufzeitregel, Entscheidungsbaum und
     Checkliste fuehren dieselben acht Kategorien, und keine traegt eine Bedingung
 30. Grenzfaelle (B07, B09): Die Grenzfalltabelle ist vollstaendig, jede Spalte gefuellt,
     jede entschiedene Auslegungsfrage durch mindestens einen Grenzfall gedeckt
 31. Durchsetzungstiefe (D-60): Die Summen der Fachmatrix eines Client Packs sind aus ihr
     ausgerechnet - Zeilenzahl und Anzahl je Einstufung. Eine Zeile zaehlt bei ihrer
     schwaechsten Einstufung; eine Kanalgrenze ist keine technische Durchsetzung (D-47)
 32. Hook-Eingabeschema (D-62, B06): Der Schutz-Hook wird mit dem VOLLSTAENDIGEN
     Umschlag jedes aufgezeichneten Schemas aufgerufen, nicht mit selbst gebauter
     Eingabe - und er darf an einem Feld des Umschlags nicht haengenbleiben
 33. Werkzeugsperre je Skill (D-64 bis D-66): Die erzeugte Fassung bildet
     permissions.deny ab, und kein Eintrag traegt ein Argumentmuster - ein solcher
     wirkt gemessen LAUTLOS gar nicht
 34. Startwerkzeug fuer Unteragenten (D-70): Ein Pack nennt es in agent_start_tools
     oder erklaert seine Abwesenheit ausdruecklich; wer Zeile A1 ohne offenen
     VERIFY-Marker zusagt, muss nennen statt erklaeren
 35. Agentenprofil ohne Startwerkzeug (D-73): Weder agent_frontmatter.tool_names
     bildet eines ab, noch nennt ein ausgeliefertes Profil eines. Eine Verankerung -
     sie faengt heute nichts
 36. Zellen des Decision Logs (D-75): Jede Tabellenzeile fuehrt so viele Zellen wie
     der Kopf ihrer Tabelle; ein maskierter Strich zaehlt als Inhalt
 37. Berechtigungskoerbe (D-77): Die drei Koerbe der installierten Datei werden gegen
     die aus der Kernquelle erzeugte Regelmenge gehalten. Fehlen ist immer ein Fehler,
     Ueberzaehliges nur in ask und allow; ein gefuellter Befehlsschlitz traegt das
     Praefixzeichen des Clients nicht
 38. Werkzeugabbildung des Frontmatters (D-78 bis D-80): Jedes Verb des
     Frontmatter-Vokabulars ist je Pack abgebildet oder ausdruecklich als nicht
     abgebildet erklaert; die Sperrliste hook_tools ist fuer kein Verbpaar enger als
     die Vorabfreigabe tool_names; keine Quelle nennt ein Verb ausserhalb des Vokabulars
 39. Vorabfreigabe des Skillaufrufs (D-81 bis D-84): Jeder ausgelieferte Skill des
     Kerns hat genau eine allow-Regel und jede Regel nennt einen ausgelieferten Skill;
     kein Musterzeichen in einer Skill-Regel - gemessen gaebe es lautlos nichts frei;
     die Skillwahl steht an allen vier Regeltraegern
 40. Register des Pruefapparats (D-85, D-86): Dieses Register ist lueckenlos und endet
     bei der hoechsten Nummer, die die beiden Pruefskripte nennen; die Sondenmenge steht
     im Satz darunter, im Kopfsatz von probe-pruefungen.py und in FW-KO-01 in derselben
     ausgerechneten Schreibweise; die Grenzfallanzahl in FW-KO-05 ist die gezaehlte
 41. Abwesenheitsbeleg (D-88): Eine erklaerte Werkzeugabwesenheit weist sich als
     Enthaltung aus oder belegt sich mit Datum und Fundstelle - eine blosse Behauptung
     nimmt eine Werkzeugklasse aus der Durchsetzung und begruendet es
 42. Schlitzinhalte (D-90, D-91): Ein gefuellter Befehlsschlitz der Berechtigungsdatei
     traegt den Befehl, den Abschnitt 5 oder 6 des Overlays fuer seinen Platzhalter
     erklaert; ein Schlitz ohne erklaerten Befehl deckt keinen Ueberschuss. Geprueft
     werden die drei BEFEHLSSCHLITZE, nicht die vier Pfadschlitze des deny-Korbs - die
     stehen dort, wo Ueberzaehliges ohnehin zulaessig ist, und ihr Vergleich waere n:1.
     Ohne Overlay enthaelt sie sich; fehlt dort ein Platzhalter, meldet sie es
 43. Hook-Block der Berechtigungsdatei (D-92): Fuehrt ein Pack seine Hooks dort - und
     beide ausgelieferten tun das -, traegt die Datei einen nichtleeren
     PreToolUse-Block. Eine Konfiguration in der eigenen Hook-Datei des Packs ist keine,
     weil der Client sie nicht liest; gemessen war der Hook eines Projekts so
     einunddreissig Releases lang stumm, bei 0 Fehlern im Lauf. Geprueft wird das
     VORHANDENSEIN - den Inhalt pruefen 15, 16 und 17
 44. Register der Uebungspraeparationen (D-93): Jede Kennung UEB-NN, die eine
     Vorbedingung des Testkatalogs oder eines dezentralen Testblatts nennt, steht im
     Register in onboarding/exercises/README.md - und jede registrierte Kennung wird von
     mindestens einem Testfall gebraucht. Sie gleicht ZWEI REGISTER ab, nicht ein
     Register gegen das Uebungsrepositorium: Das liegt ausserhalb dieses Repositoriums,
     und ob eine Praeparation dort wirklich liegt, sieht kein Validator
 45. Bytecode des Kerns (D-97): Die .gitignore des Projekts deckt __pycache__ ab,
     und unter <CORE_DIR>/ ist kein Bytecode versioniert. Zwei Gegenstaende, weil
     einer nicht reicht: git liest die .gitignore fuer bereits verfolgte Dateien
     nicht. Gegenstand 2 laeuft nur, wo git erreichbar ist - sonst sagt die
     Pruefung das als Warnung, statt stumm auszufallen
 46. Der 1.0.0-Stand (D-98, D-99): Die vier maschinell zaehlbaren Kriterien
     aus D-11 werden ausgerechnet und gegen die Standzeile in docs/ROADMAP.md
     gehalten - Markerfundstellen, offene Ergebniszellen, Modulstatus auf
     `entwurf`, Decision Records auf `entschieden (Vorschlag)`. Abweichung in
     BEIDE Richtungen ist ein Fehler. Am 2026-09-15 lagen alle vier Zahlen
     daneben, ohne dass eine je falsch geschrieben worden waere: Jede war das
     richtige Ergebnis einer Zaehlregel, die weniger kann als ihr Kriterium
     verlangt. Kriterium 5 zaehlt sie nicht - das ist eine Enthaltung
 47. Statusvokabular jedes Modultraegers (D-105, D-108): Jeder Steckbrief des Kerns
     fuehrt eine Statuszeile, und ihr Wert gehoert zum Vokabular aus
     08-skill-conventions.md Abschnitt 7. Der Ausfuellschlitz einer Vorlage gehoert
     ihr allein - in beide Richtungen. Bis 0.50.0 griff die Vokabularregel nur in
     einer SKILL.md, und der Modultraeger war ueber die Zeile definiert, die er
     tragen soll: Wer sie weglaesst, entkommt dem Lebenszyklus. Zwoelf taten es
 48. Werkzeugneutralitaet des Kerns (D-02, D-128): Kein anweisender Traeger des Kerns
     nennt einen Pfad oder Dateinamen, der genau einem Client Pack gehoert. Die Marken
     stammen aus den runtime_placeholders der Manifeste, nicht aus einer gepflegten
     Liste. Ausgenommen sind Chronik, Werkzeuge und die Abbildungstabellen; die
     Gattungen stehen in docs/RUNTIME_GLOSSARY.md. In tests/TEST_CATALOG.md steht die
     Regel nur vor der letzten Zelle - dort ist ein Pfad der Beleg einer Messung. Die
     Regel galt seit 0.31.0 und wurde von nichts durchgesetzt: Pruefung 12 liest nur
     Token in Backticks, meldet nur Pfade, die es NICHT GIBT, und fuehrte ihre eigenen
     Wurzeln clientgebunden. Siebzehn Fundstellen in vierzehn Traegern

Der Wirksamkeitsnachweis nach D-23 fuer die Pruefungen 6 und 18 bis 48 laeuft als eigenes
Skript: leitwerk-core/tests/scripts/probe-pruefungen.py (je Pruefung eine Sonde und eine
Gegenprobe, auf einer Kopie des Repositoriums).

Ohne PyYAML laufen die Prüfungen 4, 5 und 8 eingeschränkt; das Skript sagt es dann als
Warnung. Für einen Release- oder Übernahmenachweis ist PyYAML erforderlich.

Exit-Code 0 = keine Fehler (Warnungen möglich), 1 = Fehler.
Status des Skripts: entwurf. Es prüft Struktur, nicht Semantik; die semantische Prüfung
(Widerspruchsfreiheit, Verhalten des KI-Clients) erfolgt über leitwerk-core/tests/TEST_CATALOG.md.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

# Die Auswertung des Overlay-Status liegt seit 0.33.0 in einem eigenen Modul, weil der
# Status-Hook sie ebenso braucht und sie dort anders umgesetzt war (B08, D-58). Der Hook
# importiert dieses Modul; er importiert nicht dieses Skript.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from overlay_status import (  # noqa: E402
    AKTIV, INAKTIV, UNBEKANNT, WIDERSPRUECHLICH, auswerten, status_angaben)

# Name des Kernverzeichnisses. Er steht hier einmal statt an drei Stellen im Skript.
KERN = "leitwerk-core"

ERRORS: list[str] = []
WARNINGS: list[str] = []

TEXT_EXT = {".md", ".json", ".yaml", ".yml", ".txt", ".py", ".template", ".example"}
SKIP_DIRS = {".git", "build", "node_modules", "__pycache__", "target", "dist", ".venv"}
# Lockdateien sind erzeugte Abhaengigkeitsmetadaten. Sie enthalten naturgemaess fremde
# E-Mail-Adressen und Registry-Adressen und werden weder vom Framework noch vom Projekt
# redaktionell gepflegt - eine Inhaltspruefung dagegen erzeugt nur Rauschen.
SKIP_FILES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "npm-shrinkwrap.json",
              "composer.lock", "Cargo.lock", "poetry.lock", "go.sum", "Gemfile.lock"}

# Clientneutral: gilt fuer jedes Client Pack. Die clientspezifischen Pflichtpfade
# (Wurzel-Anweisung, Berechtigungsdatei, Skills, Regeltexte) kommen aus dem Manifest.
REQUIRED_PATHS = [
    "README.md", "leitwerk-core/CHANGELOG.md", "leitwerk-core/VERSION", "leitwerk-core/OWNERS.md",
    "leitwerk-core/clients/README.md",
    "leitwerk-core/framework/core/00-principles.md", "leitwerk-core/framework/core/02-privacy.md", "leitwerk-core/framework/core/03-security.md",
    "leitwerk-core/framework/core/05-working-model.md", "leitwerk-core/framework/core/08-skill-conventions.md",
    "leitwerk-core/framework/core/09-risk-model.md", "leitwerk-core/framework/role-packs", "leitwerk-core/framework/tech-packs",
    "project-overlay/OVERLAY.md", "project-overlay/overlay-manifest.yaml",
    "leitwerk-core/templates/SKILL_TEMPLATE.md", "leitwerk-core/prompts",
    "leitwerk-core/checklists", "leitwerk-core/decision-trees",
    "leitwerk-core/onboarding", "leitwerk-core/examples",
    "leitwerk-core/tests/TEST_CATALOG.md", "leitwerk-core/governance/RACI.md", "leitwerk-core/governance/DECISION_LOG.md",
    "leitwerk-core/docs/PLACEHOLDER_REGISTRY.md",
]

RULE_TRIGGERS = {"always_on", "manual", "model_decision", "agent", "glob"}
SKILL_SECTIONS = [
    "## 1. Zweck, Zielgruppe und Trigger",
    "## 2. Vorbedingungen, Eingaben und Kontext",
    "## 3. Arbeitsschritte",
    "## 4. Grenzen und Rückfragenregeln",
    "## 5. Ausgabeformat",
    "## 6. Qualitätskriterien sowie Prüf- und Freigabeschritt",
    "## 7. Fehlerbehandlung und Abbruch",
]
SKILL_META_KEYS = ["ID", "Name", "Version", "Status", "Owner (Rolle)", "Betriebsmodus", "Zulässige Kontrollstufen"]
SKILL_STATUS = {"entwurf", "pilot", "aktiv", "veraltet", "zurückgezogen"}

# Dieselben Kategorien, die der Schutz-Hook in einer Werkzeugeingabe blockiert
# (tests/scripts/hook-check-secrets.py). Ein Muster, das dort blockiert, darf in einer
# versionierten Datei nicht unbemerkt stehen bleiben - sonst waere dieselbe Zusage an
# zwei Stellen unterschiedlich streng.
#
# Ein Wert in spitzen Klammern ist ein Platzhalter und kein Secret; das Framework
# schreibt seine Beispiele durchgehend so. Nur deshalb kommen die Regeln hier ohne
# Ausnahmeliste aus. Bei der Verbindungszeichenfolge zaehlt allein das Kennwort: Ein
# Platzhalter als Benutzername sagt nichts darueber, ob das Kennwort echt ist.
SECRET_PATTERNS = [
    ("privater Schlüssel", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("Cloud-Zugangsschlüssel", re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    ("Bearer-Token", re.compile(r"\bBearer\s+[A-Za-z0-9\-_\.=]{20,}", re.I)),
    ("Zugangsdaten-Zuweisung", re.compile(
        r"(?i)\b(password|passwd|pwd|secret|api[_-]?key|access[_-]?key|token)\b"
        r"\s*[:=]\s*['\"]?(?![<`])[^\s'\"]{8,}")),
    ("Verbindungszeichenfolge mit Anmeldedaten", re.compile(
        r"(?i)\b[a-z][a-z0-9+\-.]*://[^/\s:]+:(?!<)[^@\s]+@")),
]
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
INTERNAL_HOST_RE = re.compile(r"\b[a-z0-9-]+\.(?:internal|intra|corp|lan)\b", re.I)
URL_RE = re.compile(r"https?://[^\s)>\]\"']+")
URL_ALLOWLIST = ("docs.devin.ai", "devin.ai", "cli.devin.ai", "docs.windsurf.com", "windsurf.com",
                 "example.com", "example.org", "example.invalid", "localhost")
PLACEHOLDER_RE = re.compile(r"<([A-Z][A-Z0-9_]{2,})>")
TBD_RE = re.compile(r"<TBD[:>]")
FENCE4_RE = re.compile(r"^`{4,}", re.M)
MERMAID_RE = re.compile(r"```mermaid\n(.*?)```", re.S)

# --- Zellen einer Markdown-Tabellenzeile (CR-2026-060, D-75) --------------------
# GFM trennt Zellen am Strich; ein Strich INNERHALB einer Zelle wird maskiert (\\|)
# und bleibt Inhalt. Eine Zerlegung, die das nicht kennt, beanstandet einen korrekten
# Text - gemessen an Pruefung 30, die eine Grenzfallzeile mit maskiertem Strich als
# neunspaltig meldete, obwohl sie siebenspaltig rendert. D-69 des Decision Logs
# traegt genau diese Schreibweise seit 0.36.0.
#
# Die Zerlegung lag bis 0.37.0 VIERMAL eigenhaendig im Validator. Sie liegt jetzt
# einmal: vier Gelegenheiten fuer denselben Fehler sind eine.
ZELLTRENNER_RE = re.compile(r"(?<!\\)\|")


def tabellenzellen(zeile: str) -> list:
    """Die Zellen einer Tabellenzeile, maskierte Striche als Inhalt.

    Erwartet eine Zeile, die mit '|' beginnt; die aeusseren Striche sind Rahmen und
    zaehlen nicht als Zellen. Fuer eine Zeile ohne Rahmen liefert sie die Felder
    zwischen den Trennern.
    """
    z = zeile.strip()
    teile = ZELLTRENNER_RE.split(z)
    if z.startswith("|"):
        teile = teile[1:]
    if z.endswith("|") and not z.endswith("\\|") and teile:
        teile = teile[:-1]
    return [t.strip() for t in teile]

# --- Querverweisprüfung (FW-KO-04) ---------------------------------------------
# Markdown-Links: [Text](ziel) und [Text](ziel "Titel"); Bildlinks eingeschlossen.
MD_LINK_RE = re.compile(r"""!?\[[^\]]*\]\(\s*<?([^)>\s]+)>?(?:\s+["'][^"']*["'])?\s*\)""")
# Inline-Code: Kandidaten für Pfadnennungen.
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
# Nur Pfade unter diesen Wurzeln werden aus Backticks geprüft. Bewusst eng gehalten:
# Sie benennen Framework-Artefakte und sind damit genau die Verweise, die bei einer
# Umbenennung oder Umstrukturierung stillschweigend brechen.
#
# Die Wurzeln des Frameworks stehen fest, die der Laufzeitschicht kommen aus den
# Manifesten (_link_roots). Bis 0.56.2 standen '.devin/', 'AGENTS.md' und
# 'AGENTS.local.md' hier WOERTLICH - die Pfade des jeweils anderen Packs waren damit
# gar kein Kandidat der Heuristik (CR-2026-080). Die Ableitung hat heute keine
# gemessene Wirkung; sie schafft eine gepflegte Clientliste ab, die ein drittes Client
# Pack von Hand nachtragen muesste und die niemand nachzaehlt.
LINK_ROOTS_FEST = ("leitwerk-core/", "project-overlay/", "README.md")
# Zeichen, die einen Kandidaten als Glob, Platzhalter, Befehl oder Prosa ausweisen.
NOT_A_PATH = set("*<>|?\"' \t()[]{}$!,")
#
# Bis 0.56.2 stand hier zusaetzlich OPTIONAL_RUNTIME_RE: eine Ausnahme fuer die
# Laufzeitpfade, die erst durch eine Projektentscheidung entstehen (30-, 40-, 2N-,
# Pack- und Projektskills). Sie ist mit 0.57.0 weggefallen. In drei Zuschnitten
# gemessen (CR-2026-080): Seit die Client-Bindungs-Warnung nach Pruefung 48 gewandert
# ist, deckt die Fremdpfaderkennung weiter unten denselben Fall VOLLSTAENDIG ab - ein
# Verweis unter der Laufzeitwurzel irgendeines Packs laeuft ohnehin nicht in die
# Totpfadmeldung. Eine Ausnahme, die nichts mehr ausnimmt, ist schlimmer als keine:
# Sie sieht wie Sorgfalt aus. Und sie hat sich mit der engen Wurzelliste gegenseitig
# gedeckt - zwei Fehler in derselben Richtung fallen einzeln nicht auf.
#
# Dateien mit absichtlich nicht existierenden Beispielpfaden (synthetische Beispiele,
# Vorlagen, Migrationshinweise auf frühere Stände). Markdown-Links werden auch dort
# geprüft – nur die Backtick-Heuristik ist ausgesetzt.
LINK_EXCEPTIONS = (
    "leitwerk-core/docs/PLACEHOLDER_REGISTRY.md",
    "leitwerk-core/CHANGELOG.md",
    "leitwerk-core/governance/CHANGE_REQUEST_TEMPLATE.md",
    "leitwerk-core/governance/change-requests/",
    "leitwerk-core/templates/SKILL_TEMPLATE.md",
    "leitwerk-core/examples/",
    # Client Packs beschreiben die Pfade ihres Clients, nicht die der Installation.
    "leitwerk-core/clients/_template/",
    # Das Glossar bildet die Begriffe des Kerns auf die Pfade je Client ab; dort sind
    # clientfremde Pfade der Inhalt, nicht eine Altlast.
    "leitwerk-core/docs/RUNTIME_GLOSSARY.md",
    # Historische Dokumente behalten die Pfade ihres Entstehungsstands.
    "leitwerk-core/tests/protocols/",
    "leitwerk-core/governance/DECISION_LOG.md",
)
# Eine CLIENT_PACK.md nennt naturgemaess Pfade, die nur bei ihrem Client existieren.
LINK_EXCEPTION_BASENAMES = ("CLIENT_PACK.md",)


def fundstelle(rel: str, text: str, pos: int) -> str:
    """Pfad, Zeile und Spalte eines Treffers - **ohne den Treffer selbst**.

    Die Diagnosen der Inhaltspruefung nannten bis 0.26.1 den gefundenen Wert im
    Klartext: die E-Mail-Adresse, die IP, den internen Hostnamen, die vollstaendige
    URL samt Parametern - und den gesperrten Begriff. Damit trug ein Schutzlauf genau
    die Angaben weiter, die er finden soll: in ein Terminal, ein Protokoll, eine
    Agentensitzung.

    Am schaerfsten beim Sperrbegriff. Die Liste in project-overlay/forbidden-terms.txt
    enthaelt reale Projekt-, Kunden- und Behoerdennamen; die Pruefung nimmt diese Datei
    deshalb ausdruecklich von der eigenen Inhaltspruefung aus - und schrieb den Namen
    dann in die Fehlermeldung. Die eine Zeichenkette, die in keiner Ausgabe des
    Frameworks stehen darf, stand dort durch die Pruefung, die sie verhindern soll.

    Die Secret-Diagnose derselben Funktion machte es von Anfang an richtig: Kategorie
    ohne Wert - aber ohne Position. Diese Funktion zieht die uebrigen nach und traegt
    die Fundstelle dort nach, wo sie fehlte (B03, D-39).

    Spalte statt nur Zeile, damit zwei Treffer derselben Zeile unterscheidbar bleiben -
    sonst faellt der zweite als scheinbares Duplikat nicht auf.
    """
    zeile = text.count(chr(10), 0, pos) + 1
    spalte = pos - (text.rfind(chr(10), 0, pos) + 1) + 1
    return f"{rel}:{zeile}:{spalte}"


def err(msg: str) -> None:
    ERRORS.append(msg)


def warn(msg: str) -> None:
    WARNINGS.append(msg)


def read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _walk_text_files(start: str):
    for dirpath, dirnames, filenames in os.walk(start):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            ext = os.path.splitext(fn)[1]
            if ext in TEXT_EXT or fn in ("VERSION", ".gitignore"):
                yield os.path.join(dirpath, fn)


def iter_text_files(root: str):
    yield from _walk_text_files(root)
    # 'build' steht in SKIP_DIRS, weil dort die Erzeugnisse eines Projekts liegen. Die
    # handgeschriebenen Quellen des Hauptdokuments liegen aber darunter und gehoeren
    # geprueft - gerade weil aus ihnen ein Lieferbestandteil entsteht. Vier Backticks
    # brechen genau hier die Assemblierung, und ein Secret erschiene im ausgelieferten
    # Dokument. Das Werkzeug daneben (assemble.py, build/README.md) bleibt aussen vor:
    # Es fuehrt eigene Marker in spitzen Klammern, die keine Framework-Platzhalter sind.
    doc = os.path.join(root, KERN, "build", "doc")
    if os.path.isdir(doc):
        yield from _walk_text_files(doc)


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text
    fm_text, body = parts[1], parts[2]
    if yaml is None:
        return {"_raw": fm_text}, body
    try:
        data = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError as exc:  # type: ignore[attr-defined]
        return {"_error": str(exc)}, body
    return data, body


# --- Clienterkennung (Client Packs) -------------------------------------------
# Der Validator lief frueher fest gegen .devin/. Seit es mehrere Client Packs gibt,
# wird die Laufzeitschicht erkannt: Jedes Pack beschreibt seine Pfade in
# clients/<name>/manifest.json; geprueft wird das Pack, dessen runtime_dir im
# Zielverzeichnis tatsaechlich liegt.
MANIFEST_FALLBACK = {
    "client": "unbekannt", "runtime_dir": ".devin", "root_instruction_file": "AGENTS.md",
    "permissions_file": ".devin/config.json", "skills_dir": ".devin/skills",
    "agents_dir": ".devin/agents", "pack_runtime_dir": ".devin/rules",
    "has_rule_triggers": True,
}


def detect_client(root: str) -> dict:
    """Manifest des installierten Client Packs. Fallback, wenn keines zutrifft."""
    base = os.path.join(root, KERN, "clients")
    treffer = []
    if os.path.isdir(base):
        for name in sorted(os.listdir(base)):
            mp = os.path.join(base, name, "manifest.json")
            if not os.path.exists(mp):
                continue
            try:
                man = json.loads(read(mp))
            except json.JSONDecodeError as exc:
                err(f"clients/{name}/manifest.json ist kein gültiges JSON: {exc}")
                continue
            if os.path.isdir(os.path.join(root, *man.get("runtime_dir", "").split("/"))):
                # mp = <root>/<kern>/clients/<pack>/manifest.json - drei Ebenen hoch
                # liegt das Kernverzeichnis, dessen Name <CORE_DIR> ist.
                man.setdefault("runtime_placeholders", {})["<CORE_DIR>"] = os.path.basename(
                    os.path.dirname(os.path.dirname(os.path.dirname(mp))))
                treffer.append(man)
    if len(treffer) > 1:
        namen = ", ".join(m["client"] for m in treffer)
        err(f"Mehrere Laufzeitschichten gleichzeitig vorhanden ({namen}). "
            f"Ein Projekt nutzt genau ein Client Pack.")
    return treffer[0] if treffer else MANIFEST_FALLBACK


def check_required(root: str, man: dict) -> None:
    pflicht = list(REQUIRED_PATHS)
    pflicht += [man["root_instruction_file"], man["permissions_file"],
                man["skills_dir"], man["agents_dir"]]
    pflicht += [f"{man['pack_runtime_dir']}/{n}.md" for n in
                ("00-framework-core", "10-privacy-security", "15-development-rules",
                 "20-project-overlay")]
    for rel in pflicht:
        if not os.path.exists(os.path.join(root, rel)):
            err(f"Pflichtpfad fehlt: {rel}")


def soll_kernregeln(root: str, man: dict) -> list[str]:
    """Kernzusagen B1 bis B6 in der Schreibweise dieses Clients, aus der Kernquelle.

    Berechtigungen sind Saat: Nach der Erstinstallation gehoert die Datei dem Projekt und
    wird nie ueberschrieben - install.py --check meldet dort also nichts. Diese Pruefung
    ist deshalb die einzige Stelle, an der eine entfernte Kernregel auffaellt. Fehlt das
    Abbildungsmodul (etwa in einer Teilkopie des Kerns), wird nur gewarnt: Die Pruefungen
    gegen die Datei selbst greifen weiterhin.
    """
    kern = os.path.join(root, KERN)
    if not os.path.isdir(kern):
        return []
    if kern not in sys.path:
        sys.path.insert(0, kern)
    try:
        import clientmap
    except ImportError:
        warn("clientmap.py nicht gefunden – Kernregeln werden nur gegen die "
             "Berechtigungsdatei selbst geprüft, nicht gegen die Kernquelle")
        return []
    try:
        quelle = json.loads(clientmap.load_source(kern, "permissions.json"))
        return clientmap.core_rules(quelle, man)
    except (OSError, ValueError) as exc:
        err(f"Kernquelle der Berechtigungen nicht auswertbar: {exc}")
        return []


def check_config(root: str, man: dict) -> None:
    rel = man["permissions_file"]
    path = os.path.join(root, *rel.split("/"))
    if not os.path.exists(path):
        return
    try:
        cfg = json.loads(read(path))
    except json.JSONDecodeError as exc:
        err(f"{rel} ist kein gültiges JSON: {exc}")
        return
    perms = cfg.get("permissions", {})
    deny = set(perms.get("deny", []))
    allow = set(perms.get("allow", []))

    # Eine Pfadregel fuer ein Werkzeug, das der Client dafuer nicht auswertet, wird
    # angenommen und nie konsultiert - sie taeuscht Schutz vor und erzeugt beim
    # Sitzungsstart Laerm. Welche Werkzeuge Pfadregeln kennen, sagt das Manifest; ohne die
    # Angabe unterbleibt die Pruefung, weil sie dann unbelegt waere (AP2-CC-02, D-26).
    pfadwerkzeuge = man.get("permission_path_tools")
    if pfadwerkzeuge:
        befehlswerkzeuge = set(man.get("permission_tools", {}).get("exec", []))
        namenswerkzeuge = set(man.get("permission_name_tools", []))
        for korb in ("deny", "ask", "allow"):
            for regel in perms.get(korb, []):
                if not isinstance(regel, str) or "(" not in regel:
                    continue
                werkzeug = regel.split("(", 1)[0]
                if (werkzeug in befehlswerkzeuge or werkzeug in pfadwerkzeuge
                        or werkzeug in namenswerkzeuge):
                    continue
                err(f"{rel}: {korb}-Regel '{regel}' nennt ein Werkzeug, fuer das dieser "
                    f"Client keine Pfadregeln auswertet. Zulaessig sind "
                    f"{', '.join(sorted(pfadwerkzeuge))}; eine Regel ohne Pfad wirkt "
                    f"weiterhin auf Werkzeugebene")
    must = cfg.get("_core_rules_integrity", {}).get("deny_must_contain", [])
    if not must:
        err(f"{rel}: Block _core_rules_integrity.deny_must_contain fehlt")
    for rule in must:
        if rule not in deny:
            err(f"{rel}: Kernregel fehlt in deny: {rule}")
        if rule in allow:
            err(f"{rel}: Kernverbot steht in allow: {rule}")
    # Die Liste gegen die Kernquelle abgleichen, nicht nur gegen sich selbst. Ohne diesen
    # Schritt genuegte es, eine Kernregel in beiden Listen zu streichen - die Datei bliebe
    # in sich stimmig und der Verlust unbemerkt.
    for rule in soll_kernregeln(root, man):
        if rule in must:
            continue  # von der Schleife darueber bereits geprueft
        err(f"{rel}: Kernregel fehlt in _core_rules_integrity.deny_must_contain "
            f"(laut Kernquelle vorgesehen): {rule}")
        if rule not in deny:
            err(f"{rel}: Kernregel fehlt in deny: {rule}")
    # Nie erlaubt, unabhaengig vom Client: Push, Merge, Rechteausweitung, Loeschen.
    # Die Werkzeugnamen unterscheiden sich je Client, die Absicht nicht.
    verboten = ("Exec(git push", "Exec(sudo", "Exec(rm -rf",
                "Bash(git push", "Bash(git merge", "Bash(sudo", "Bash(rm")
    for rule in allow:
        if rule.startswith(verboten):
            err(f"{rel}: unzulässige allow-Regel: {rule}")
    # Abrufwerkzeuge: aus dem Manifest, nicht aus einer Namensliste. Bis 0.32.0 standen
    # hier "Fetch(*", "WebFetch" und "WebSearch" fest verdrahtet - und das war
    # asymmetrisch: 'Fetch(domain:...)' lief durch, 'WebFetch(domain:...)' fiel, dieselbe
    # Absicht bei zwei Packs verschieden entschieden. Nach D-59 gibt es keine
    # Domain-Ausnahme; damit ist **jede** allow-Regel auf ein Abrufverb unzulaessig, und
    # der dokumentierte Weg ist, das globale Verbot per Aenderungsantrag zu ersetzen
    # (B11, V10).
    abrufwerkzeuge = tuple(man.get("permission_tools", {}).get("fetch", ()))
    for rule in allow:
        if not isinstance(rule, str):
            continue
        name = rule.split("(", 1)[0].strip()
        if abrufwerkzeuge and name in abrufwerkzeuge:
            err(f"{rel}: unzulässige allow-Regel auf ein Abrufwerkzeug: {rule}. Das "
                f"generelle Netzverbot kennt keine Ausnahme je Domain - `deny` gewinnt "
                f"immer, eine zusätzliche allow-Regel hebt es nicht auf. Wer externen "
                f"Abruf braucht, ersetzt die Verbotsregel über einen Änderungsantrag "
                f"(V10) und weist die Ersatzbeschränkung nach (B11, D-59)")
    # Weitere JSON-Dateien der Laufzeitschicht auf Gueltigkeit pruefen.
    rt = man["runtime_dir"]
    for name in os.listdir(os.path.join(root, *rt.split("/"))) if os.path.isdir(os.path.join(root, *rt.split("/"))) else []:
        if not name.endswith((".json", ".json.example")):
            continue
        p = os.path.join(root, *rt.split("/"), name)
        try:
            data = json.loads(read(p))
        except json.JSONDecodeError as exc:
            err(f"{rt}/{name} ist kein gültiges JSON: {exc}")
            continue
        if "mcp" in name and not name.endswith(".example"):
            blob = json.dumps(data).lower()
            if any(k in blob for k in ("password", "token", "secret", "apikey", "api_key")):
                err(f"{rt}/{name} enthält Schlüsselwörter für Zugangsdaten – gehören in eine nicht versionierte Datei oder einen Tresor")


# ---------------------------------------------------------------------------
# 37: Die drei Koerbe der Berechtigungsdatei gegen die Kernquelle
# ---------------------------------------------------------------------------
#
# Anlass ist eine Messung vom 2026-09-13 (CR-2026-061, D-77): Die erzeugte Datei traegt
# 65 Regeln, geprueft waren dreizehn. Ein Projekt konnte 41 deny-Regeln loeschen, den
# ask-Korb leeren und eine allow-Zeile ergaenzen, ohne dass ein Lauf davon Notiz nahm -
# und install.py --update fasst die Datei nie an, --check nennt sie nicht einmal.
#
# Die Pruefung ist das Verschaerfungsprinzip, mechanisch angewandt
# (PRIORITY_HIERARCHY.md Regel 2.1), in zwei Saetzen:
#   Fehlt eine erzeugte Regel, ist es ein Fehler - in jedem Korb.
#   Steht eine Regel zu viel, entscheidet der Korb: in deny zulaessig (Verschaerfung),
#   in ask und allow ein Fehler (Ausweitung) - abzueglich der Platzhalterschlitze.
PROJEKTPLATZHALTER = re.compile(r"<[A-Z][A-Z0-9_]*>")


def korb_zerlegung(ist: list, soll_korb: list) -> tuple:
    """Ein Korb in Pflicht, Schlitze, gefuellte Schlitze und Ueberschuss.

    Die Zerlegung lag bis 0.43.0 in check_berechtigungskoerbe und wurde fuer Pruefung 42
    ein zweites Mal gebraucht. Sie liegt jetzt einmal: zwei Gelegenheiten fuer denselben
    Fehler sind eine - dieselbe Begruendung wie bei tabellenzellen() mit 0.37.0.

    pflicht    Regeln ohne Projektplatzhalter; sie muessen dastehen.
    schlitze   Regeln mit Projektplatzhalter; sie gehoeren dem Projekt.
    ungefuellt Schlitze, die woertlich in der Datei stehen. Sie sind noch offen.
    zusatz     Regeln der Datei, die weder Pflicht noch ein offener Schlitz sind - ein
               gefuellter Schlitz steht hier ebenso wie eine hinzugefuegte Freigabe.
               WELCHE von beiden, sagt diese Funktion nicht und kann es nicht sagen;
               das ist der Gegenstand von Pruefung 42.
    """
    pflicht = [r for r in soll_korb if not PROJEKTPLATZHALTER.search(r)]
    schlitze = [r for r in soll_korb if PROJEKTPLATZHALTER.search(r)]
    ungefuellt = [s for s in schlitze if s in ist]
    zusatz = [r for r in ist if r not in pflicht and r not in schlitze]
    return pflicht, schlitze, ungefuellt, zusatz


def soll_korbregeln(root: str, man: dict) -> dict | None:
    """Die drei Koerbe in der Schreibweise dieses Clients, aus der Kernquelle.

    Dieselbe Quelle wie soll_kernregeln, nur ohne die Einschraenkung auf 'core': true.
    Fehlt das Abbildungsmodul, unterbleibt die Pruefung - check_config hat dafuer bereits
    gewarnt, und eine zweite Warnung ueber dieselbe Tatsache waere Laerm.
    """
    kern = os.path.join(root, KERN)
    if not os.path.isdir(kern):
        return None
    if kern not in sys.path:
        sys.path.insert(0, kern)
    try:
        import clientmap
    except ImportError:
        return None
    # Sonde auf den verlorenen Anker (seit 0.32.0): Diese Pruefung findet ihren
    # Gegenstand ueber einen Funktionsnamen. Geht er bei einem Umbau verloren, bestuende
    # sie leise - deshalb meldet sie sein Fehlen selbst.
    if not hasattr(clientmap, "basket_rules"):
        err(f"{KERN}/clientmap.py: Funktion 'basket_rules(' fehlt – Prüfung 37 hat ihren "
            f"Gegenstand verloren und würde sonst leise bestehen")
        return None
    try:
        quelle = json.loads(clientmap.load_source(kern, "permissions.json"))
        return {korb: clientmap.basket_rules(quelle, man, korb)
                for korb in ("deny", "ask", "allow")}
    except (OSError, ValueError) as exc:
        err(f"Kernquelle der Berechtigungen nicht auswertbar: {exc}")
        return None


def check_berechtigungskoerbe(root: str, man: dict) -> None:
    """Pruefung 37: Was die Kernquelle erzeugt, steht in der installierten Datei.

    Warum nicht einfach _core_rules_integrity auf alle Regeln erweitern: Das faengt die
    geloeschte und die verengte Regel, aber weder die ergaenzte allow-Zeile noch den
    geleerten ask-Korb. Die Liste sagt, was fehlen darf - nicht, was zuviel sein darf.

    Ein Platzhalterschlitz (Bash(<TEST_COMMAND>) und die drei Pfadschlitze) ist der
    einzige Teil dieser Datei, der dem Projekt gehoert. Er darf gefuellt sein, gefuellt
    zaehlt er gegen den Ueberschuss - und er darf das Praefixzeichen des Clients nicht
    tragen: clientmap._befehl haengt es an einen offenen Projektplatzhalter bewusst nicht
    an, weil der Overlay Owner dort den vollstaendigen Befehl eintraegt. Von Hand
    nachgetragen macht es aus der Freigabe eines Befehls die Freigabe einer
    Befehlsfamilie - am Piloten am 2026-09-13 so vorgefunden.
    """
    rel = man["permissions_file"]
    path = os.path.join(root, *rel.split("/"))
    if not os.path.exists(path):
        return
    try:
        cfg = json.loads(read(path))
    except json.JSONDecodeError:
        return  # check_config hat das bereits gemeldet
    soll = soll_korbregeln(root, man)
    if soll is None:
        return
    if not any(soll.values()):
        err(f"{KERN}/framework/runtime/permissions.json: die Abbildung erzeugt für das "
            f"Client Pack {man.get('client', '?')} keine einzige Regel – Prüfung 37 hätte "
            f"nichts zu vergleichen und bestünde leise")
        return

    perms = cfg.get("permissions", {})
    exec_werkzeuge = tuple(man.get("permission_tools", {}).get("exec", ()))
    praefixzeichen = (man.get("permission_exec_suffix", ":*")
                      if man.get("permission_exec_match") == "prefix" else None)

    for korb in ("deny", "ask", "allow"):
        ist = [r for r in perms.get(korb, []) if isinstance(r, str)]
        pflicht, schlitze, ungefuellt, zusatz = korb_zerlegung(ist, soll[korb])
        for regel in pflicht:
            if regel not in ist:
                err(f"{rel}: die Kernquelle erzeugt für den {korb}-Korb die Regel "
                    f"'{regel}'; dort steht sie nicht. Eine fehlende Regel ist eine "
                    f"Lockerung, gleich in welchem Korb – Änderungen an der Regelmenge "
                    f"laufen über einen Änderungsantrag (V10, D-77)")
        if korb == "deny":
            # Eine zusaetzliche deny-Regel ist eine Verschaerfung und deshalb zulaessig.
            continue
        # Gedeckt wird ein Ueberschuss nur von den Schlitzen, die NICHT mehr
        # woertlich dastehen - ein woertlich vorhandener Schlitz ist ungefuellt.
        offen = [s for s in schlitze if s not in ungefuellt]
        if len(zusatz) > len(offen):
            err(f"{rel}: der {korb}-Korb führt {len(zusatz)} Regel(n), die die Kernquelle "
                f"nicht erzeugt, bei {len(offen)} gefüllten Platzhalterschlitz(en): "
                f"{', '.join(zusatz)}. Eine zusätzliche Freigabe ist eine Ausweitung und "
                f"nicht Sache des Overlays; ein weiterer freigegebener Befehl gehört in "
                f"Abschnitt 6 des Overlays und damit in die Regelschicht (D-76)")
        if not praefixzeichen or len(zusatz) > len(offen):
            # Kein Praefixzeichen: Dieser Client sperrt Befehle woertlich.
            # Ueberschuss groesser als die offenen Schlitze: Dann ist nicht entschieden,
            # welche Zeile ein gefuellter Schlitz ist und welche eine hinzugefuegte
            # Freigabe - und eine Meldung, die "gefuellter Platzhalterschlitz" sagt, wo
            # keiner ist, sagt etwas anderes als der Fall hergibt. Die Meldung darueber
            # benennt den Ueberschuss bereits richtig.
            continue
        for regel in zusatz:
            teile = regel.split("(", 1)
            if len(teile) != 2 or teile[0] not in exec_werkzeuge:
                continue
            inhalt = teile[1][:-1] if teile[1].endswith(")") else teile[1]
            if inhalt.endswith(praefixzeichen):
                err(f"{rel}: '{regel}' im {korb}-Korb trägt das Präfixzeichen "
                    f"'{praefixzeichen}'. Die Abbildung hängt es an einen gefüllten "
                    f"Projektplatzhalter bewusst nicht an – von Hand nachgetragen macht "
                    f"es aus der Freigabe eines Befehls die Freigabe einer "
                    f"Befehlsfamilie (D-77)")


KERNREGEL_PRAEFIXE = ("00-", "10-", "15-", "20-")


def _check_rule_client_form(rel: str, fn: str, text: str, spec: dict) -> int:
    """Regeldatei in der Bedingungssprache des Clients. Rueckgabe: Zeichen, die stets laden.

    Geprueft wird die **installierte** Fassung, nicht die Quelle (D-26): Ein stehen
    gebliebenes `trigger:` oder `globs:` bedeutet, dass die Datei nicht durch die Abbildung
    des Client Packs gelaufen ist - der Client wertet diese Felder nicht aus, die
    Ladebedingung waere damit verfallen.
    """
    feld = spec.get("condition_field")
    erlaubt = set(spec.get("allowed_fields", []))
    if not text.startswith("---"):
        return len(text)
    fm, _ = parse_frontmatter(text)
    if not fm or "_error" in fm:
        err(f"{rel}: Frontmatter vorhanden, aber nicht lesbar")
        return 0
    if "_raw" in fm:
        return 0
    for schluessel in sorted(set(fm) - erlaubt):
        err(f"{rel}: Frontmatter-Feld '{schluessel}' – dieser Client wertet für Regeldateien "
            f"nur {sorted(erlaubt)} aus (K-18). Ein stehen gebliebenes 'trigger' oder 'globs' "
            f"heißt: Die Datei ist nicht durch die Abbildung des Client Packs gelaufen, ihre "
            f"Ladebedingung ist verfallen")
    if feld not in fm:
        return len(text)
    werte = fm[feld]
    if spec.get("condition_format", "list") == "list" and (
            not isinstance(werte, list) or not werte
            or not all(isinstance(w, str) and w.strip() for w in werte)):
        err(f"{rel}: '{feld}' muss eine nichtleere Liste von Dateimustern sein")
    if fn.startswith(KERNREGEL_PRAEFIXE):
        err(f"{rel}: Kernregel über '{feld}' an Dateimuster gebunden – sie gilt für jede "
            f"Aufgabe; eine Ladebedingung wäre hier eine Lockerung")
    return 0


def check_rules(root: str, man: dict) -> None:
    """Regeltexte der Laufzeitschicht.

    Drei Bauarten, je nach Client:

    * Der Client kennt die Ladetrigger der Kernquelle (`devin-desktop`): geprueft wird das
      Quellfrontmatter - `description`, `trigger`, bei `glob` zusaetzlich `globs`.
    * Der Client kennt eine **eigene** Bedingungssprache (`rule_triggers` im Manifest, bei
      `claude-code` das Feld `paths`): geprueft wird die installierte Fassung gegen die
      Felder, die er auswertet.
    * Der Client laedt Regeldateien nicht von sich aus: Dort wirkt eine Datei erst, wenn die
      Wurzel-Anweisung sie einbindet - eine nicht eingebundene Datei ist stillschweigend
      wirkungslos, und genau das wird geprueft. Kein ausgeliefertes Pack ist so gebaut.
    """
    rules_rel = man["pack_runtime_dir"]
    rules_dir = os.path.join(root, *rules_rel.split("/"))
    if not os.path.isdir(rules_dir):
        return

    wurzel_rel = man["root_instruction_file"]
    wurzel_pfad = os.path.join(root, *wurzel_rel.split("/"))
    wurzel_text = read(wurzel_pfad) if os.path.exists(wurzel_pfad) else ""
    eigene_bedingung = man.get("rule_triggers")
    mit_triggern = man.get("has_rule_triggers", True)
    ueber_import = not mit_triggern
    stets_geladen = len(wurzel_text)

    for fn in sorted(os.listdir(rules_dir)):
        if not fn.endswith(".md"):
            continue
        text = read(os.path.join(rules_dir, fn))
        rel = f"{rules_rel}/{fn}"

        if not ueber_import:
            if len(text) > 12000:
                err(f"{rel}: {len(text)} Zeichen (> 12.000)")
            if fn == "20-project-overlay.md" and len(text) > 6000:
                warn(f"{rel}: {len(text)} Zeichen (> 6.000, SOLL-Grenze)")
        if fn == "README.md":
            continue

        if eigene_bedingung:
            stets_geladen += _check_rule_client_form(rel, fn, text, eigene_bedingung)
        elif mit_triggern:
            fm, _ = parse_frontmatter(text)
            if not fm or "_error" in fm:
                err(f"{rel}: Frontmatter fehlt oder ungültig")
                continue
            if "_raw" in fm:
                continue
            if "description" not in fm or not str(fm.get("description", "")).strip():
                err(f"{rel}: Frontmatter-Feld description fehlt")
            trig = fm.get("trigger")
            if trig not in RULE_TRIGGERS:
                err(f"{rel}: trigger '{trig}' nicht in {sorted(RULE_TRIGGERS)}")
            if trig == "glob" and not fm.get("globs"):
                err(f"{rel}: trigger glob ohne globs")
        else:
            # Ohne eigene Ladebedingung entscheidet der Import. Eine Kernregel muss
            # eingebunden sein, sonst waere sie wirkungslos.
            eingebunden = f"@{rel}" in wurzel_text
            if fn.startswith(KERNREGEL_PRAEFIXE) and not eingebunden:
                err(f"{rel}: nicht in {wurzel_rel} eingebunden (@{rel}) – die Regel wäre wirkungslos")
            if eingebunden:
                stets_geladen += len(text)
            if text.startswith("---"):
                warn(f"{rel}: YAML-Frontmatter, obwohl dieser Client keine Ladebedingung kennt "
                     f"(Frontmatter nur mit dokumentierten Feldern, K-18)")

    if (eigene_bedingung or ueber_import) and stets_geladen > 40000:
        warn(f"{wurzel_rel} und die unbedingt geladenen Regeltexte ergeben {stets_geladen} "
             f"Zeichen, die in jeder Sitzung geladen werden (Least Context)")

    if os.path.exists(wurzel_pfad) and not ueber_import and len(wurzel_text) > 12000:
        err(f"{wurzel_rel}: {len(wurzel_text)} Zeichen (> 12.000)")


def skill_dirs(root: str, man: dict) -> list[tuple[str, str]]:
    """Alle Skill-Ablagen: die aktivierte Laufzeitschicht und die Quellablagen der Packs.

    Pack-Skills liegen unter framework/{role,tech}-packs/<pack>/skills/ und werden erst zur
    Aktivierung nach .devin/skills/ kopiert. Ohne diese Ablagen wuerde ein fehlerhafter
    Pack-Skill erst im uebernehmenden Projekt auffallen - also nach der Auslieferung.
    """
    out: list[tuple[str, str]] = []
    runtime = os.path.join(root, *man["skills_dir"].split("/"))
    if os.path.isdir(runtime):
        out.append((runtime, man["skills_dir"]))
    # Gemeinsame Quelle der Framework-Skills (seit 0.5.0). Sie wird streng geprueft;
    # die installierte Fassung ist daraus erzeugt.
    quelle = os.path.join(root, "leitwerk-core", "framework", "skills")
    if os.path.isdir(quelle):
        out.append((quelle, "leitwerk-core/framework/skills"))
    for kind in ("role-packs", "tech-packs"):
        base = os.path.join(root, "leitwerk-core", "framework", kind)
        if not os.path.isdir(base):
            continue
        for pack in sorted(os.listdir(base)):
            src = os.path.join(base, pack, "skills")
            if os.path.isdir(src):
                out.append((src, f"leitwerk-core/framework/{kind}/{pack}/skills"))
    return out


def check_skills(root: str, man: dict) -> None:
    ids: dict[str, str] = {}
    runtime = man["skills_dir"]
    for skills_dir, prefix in skill_dirs(root, man):
        # Die Modellwahl-Sperre wird nur in der *installierten* Fassung geprueft: In der
        # Quelle steht die Aussage als `triggers`, erst die Abbildung uebersetzt sie.
        check_skills_in(skills_dir, prefix, ids,
                        man if prefix == runtime else None)


def check_skills_in(skills_dir: str, prefix: str, ids: dict[str, str],
                    man: dict | None = None) -> None:
    for name in sorted(os.listdir(skills_dir)):
        sdir = os.path.join(skills_dir, name)
        if not os.path.isdir(sdir):
            continue
        rel = f"{prefix}/{name}"
        if not re.fullmatch(r"[a-z0-9-]+", name):
            err(f"{rel}: Verzeichnisname muss aus Kleinbuchstaben, Ziffern, Bindestrichen bestehen")
        if not re.match(r"^(fw|prj|role-[a-z0-9]+|tech-[a-z0-9]+)-", name):
            warn(f"{rel}: Präfix entspricht nicht fw-/prj-/role-<pack>-/tech-<pack>-")
        for req in ("SKILL.md", "EXAMPLES.md", "TESTS.md", "CHANGELOG.md"):
            if not os.path.exists(os.path.join(sdir, req)):
                err(f"{rel}: {req} fehlt")
        skill_path = os.path.join(sdir, "SKILL.md")
        if not os.path.exists(skill_path):
            continue
        text = read(skill_path)
        fm, body = parse_frontmatter(text)
        if not fm or "_error" in fm:
            err(f"{rel}/SKILL.md: Frontmatter fehlt oder ungültig")
            continue
        if "_raw" not in fm:
            if fm.get("name") != name:
                err(f"{rel}/SKILL.md: name '{fm.get('name')}' != Verzeichnisname")
            if not str(fm.get("description", "")).strip():
                err(f"{rel}/SKILL.md: description fehlt")
            fmt = (man or {}).get("skill_frontmatter", {})
            # Die Quelle nennt allowed-tools als Liste von Verben, die installierte Fassung
            # je nach Client als Liste oder als kommagetrennte Zeichenkette von Werkzeugnamen.
            # Ohne diese Unterscheidung lief die Pruefung ueber die *Zeichen* der Zeichenkette
            # und meldete jeden installierten Skill als nicht schreibend (AP2-CC-09).
            tools = fm.get("allowed-tools") or []
            if isinstance(tools, str):
                tools = [x for x in re.split(r"[,\s]+", tools) if x]
            if not tools:
                err(f"{rel}/SKILL.md: allowed-tools fehlt (minimale Werkzeugmenge angeben)")
            schreibverben = ("edit", "exec", "write")
            namen = fmt.get("tool_names", {})
            schreibnamen = {n for v in schreibverben for n in namen.get(v, [])}
            writes = any(t in schreibverben or t in schreibnamen for t in tools)

            sperre = fmt.get("model_invocation_field")
            # Traegt dieser Ablageort `triggers` ueberhaupt? Ein Client, der das Feld nicht
            # kennt, bekommt die Aussage abgebildet - dann ist ihr Fehlen kein Fehler,
            # sondern die Abbildung ist zu pruefen (AP2-CC-01 und AP2-CC-09, D-26).
            abgebildet = bool(sperre) and "triggers" in fmt.get("drop_fields", [])
            triggers = fm.get("triggers") or []
            if abgebildet:
                if writes and fm.get(sperre) is not True:
                    err(f"{rel}/SKILL.md: schreibender/ausfuehrender Skill ohne "
                        f"'{sperre}: true' - die Quelle verlangt triggers: [user], die "
                        f"installierte Fassung muss das in der Form dieses Clients tragen")
            else:
                if writes and triggers != ["user"]:
                    err(f"{rel}/SKILL.md: schreibender/ausfuehrender Skill muss "
                        f"triggers: [user] haben")
                if not triggers:
                    err(f"{rel}/SKILL.md: triggers fehlt")

            erlaubt = ("name", "description", "argument-hint", "allowed-tools", "permissions",
                       "triggers", "model", "subagent", "agent")
            # Die beiden abgebildeten Felder heissen je Client anders und stehen deshalb
            # nicht in der Liste, sondern kommen aus dem Manifest: die Modellwahl-Sperre
            # (AP2-CC-01) und seit 0.35.0 die Werkzeugsperre je Skill (D-64).
            deny_feld = fmt.get("skill_deny_field")
            for key in fm:
                if key not in erlaubt and key != sperre and key != deny_feld:
                    warn(f"{rel}/SKILL.md: Frontmatter-Feld '{key}' ist nicht dokumentiert")
        for key in SKILL_META_KEYS:
            if not re.search(rf"^\|\s*{re.escape(key)}\s*\|", body, re.M):
                err(f"{rel}/SKILL.md: Metadatenzeile '{key}' fehlt")
        m = re.search(r"^\|\s*Status\s*\|\s*`?([^`|]+?)`?\s*\|", body, re.M)
        if m and m.group(1).strip() not in SKILL_STATUS:
            err(f"{rel}/SKILL.md: Status '{m.group(1).strip()}' unbekannt")
        # Bis 0.12.0 genuegte irgendein Wert - 'banane' blieb unbemerkt, und die Version
        # konnte dem Aenderungsverlauf widersprechen (FW-VN-01, Sonden S4 und S5).
        m = re.search(r"^\|\s*Version\s*\|\s*`?([^`|]+?)`?\s*\|", body, re.M)
        cl_path = os.path.join(sdir, "CHANGELOG.md")
        if m:
            fassung = m.group(1).strip()
            if not SEMVER_RE.match(fassung):
                err(f"{rel}/SKILL.md: Version '{fassung}' ist kein Semantic Versioning "
                    f"(MAJOR.MINOR.PATCH)")
            elif os.path.exists(cl_path) and not re.search(
                    rf"^\|\s*{re.escape(fassung)}\s*\|", read(cl_path), re.M):
                err(f"{rel}: Version {fassung} hat keinen Eintrag in CHANGELOG.md "
                    f"(08-skill-conventions.md Abschnitt 7)")
        m = re.search(r"^\|\s*ID\s*\|\s*`?([A-Z0-9-]+)`?\s*\|", body, re.M)
        if m:
            vorher = ids.get(m.group(1))
            # Gleicher Skillname in Quellablage und aktivierter Schicht ist eine Kopie,
            # kein Konflikt. Nur unterschiedliche Skills mit gleicher ID sind ein Fehler.
            if vorher is not None and vorher != name:
                err(f"{rel}/SKILL.md: ID {m.group(1)} doppelt (auch in {vorher})")
            ids[m.group(1)] = name
        else:
            err(f"{rel}/SKILL.md: ID nicht lesbar")
        for sec in SKILL_SECTIONS:
            if sec not in body:
                err(f"{rel}/SKILL.md: Pflichtabschnitt fehlt: {sec}")
        for word in ("Rückfrage", "Fundstelle"):
            if word not in body:
                err(f"{rel}/SKILL.md: Begriff '{word}' fehlt (Rückfragen-/Belegpflicht)")
        ex_path = os.path.join(sdir, "EXAMPLES.md")
        if os.path.exists(ex_path):
            ex = read(ex_path)
            if "synthetisch" not in ex:
                err(f"{rel}/EXAMPLES.md: Kennzeichnung 'synthetisch' fehlt")
            if "Positivbeispiel" not in ex or "Negativbeispiel" not in ex:
                err(f"{rel}/EXAMPLES.md: Positiv- und Negativbeispiel erforderlich")
        t_path = os.path.join(sdir, "TESTS.md")
        if os.path.exists(t_path):
            t = read(t_path)
            if not re.search(r"-P0\d", t) or not re.search(r"-N0\d", t):
                err(f"{rel}/TESTS.md: mindestens ein Positivtest (-P0n) und ein Negativtest (-N0n) erforderlich")
            for col in ("Test-ID", "Ziel", "Vorbedingung", "Eingabe", "Erwartetes Verhalten",
                        "Unzulässiges Verhalten", "Prüfmethode", "Ergebnisstatus"):
                if col not in t:
                    err(f"{rel}/TESTS.md: Spalte '{col}' fehlt")


def load_placeholder_registry(root: str) -> set[str]:
    path = os.path.join(root, "leitwerk-core", "docs", "PLACEHOLDER_REGISTRY.md")
    if not os.path.exists(path):
        return set()
    return set(PLACEHOLDER_RE.findall(read(path)))


def check_content(root: str) -> None:
    registry = load_placeholder_registry(root)
    forbidden_terms: list[str] = []
    ft_path = os.path.join(root, "project-overlay", "forbidden-terms.txt")
    if os.path.exists(ft_path):
        forbidden_terms = [l.strip() for l in read(ft_path).splitlines()
                           if l.strip() and not l.startswith("#")]
    unknown_placeholders: dict[str, set[str]] = {}
    for path in iter_text_files(root):
        # os.path.relpath liefert unter Windows Backslashes; ohne diese Normalisierung
        # greift unten kein einziger Pfadvergleich - check_links macht es seit jeher so.
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if rel.startswith(f"{KERN}/tests/scripts/") or rel == "project-overlay/forbidden-terms.txt":
            continue
        if os.path.basename(path) in SKIP_FILES:
            continue
        text = read(path)
        for label, pat in SECRET_PATTERNS:
            m = pat.search(text)
            if m:
                err(f"{fundstelle(rel, text, m.start())}: FW-CONTENT-SECRET: "
                    f"Secret-Muster ({label})")
        for m in EMAIL_RE.finditer(text):
            if not m.group(0).lower().endswith(("example.com", "example.org", "example.invalid")):
                err(f"{fundstelle(rel, text, m.start())}: FW-CONTENT-EMAIL: E-Mail-Adresse")
        for m in IP_RE.finditer(text):
            if not m.group(0).startswith(("0.", "127.", "192.0.2.", "198.51.100.", "203.0.113.")):
                err(f"{fundstelle(rel, text, m.start())}: FW-CONTENT-IP: IP-Adresse")
        for m in INTERNAL_HOST_RE.finditer(text):
            err(f"{fundstelle(rel, text, m.start())}: FW-CONTENT-HOST: interner Hostname")
        for m in URL_RE.finditer(text):
            if not any(host in m.group(0) for host in URL_ALLOWLIST):
                warn(f"{fundstelle(rel, text, m.start())}: FW-CONTENT-URL: URL außerhalb der Allowlist")
        for term in forbidden_terms:
            m = re.search(rf"(?i)\b{re.escape(term)}\b", text)
            if m:
                err(f"{fundstelle(rel, text, m.start())}: FW-CONTENT-TERM: gesperrter Begriff")
        if FENCE4_RE.search(text) and rel.startswith(
                (".devin/", ".claude/", "project-overlay/") +
                tuple(f"{KERN}/{d}/" for d in ("framework", "prompts", "checklists", "decision-trees",
                                               "onboarding", "templates", "governance", "pilot",
                                               "build", "docs", "examples"))):
            err(f"{rel}: Codeblock mit vier oder mehr Backticks (bricht die Dokumentassemblierung)")
        if registry:
            for ph in set(PLACEHOLDER_RE.findall(text)):
                if ph not in registry and ph not in ("TBD",):
                    unknown_placeholders.setdefault(ph, set()).add(rel)
    for ph, files in sorted(unknown_placeholders.items()):
        warn(f"Platzhalter <{ph}> nicht in leitwerk-core/docs/PLACEHOLDER_REGISTRY.md (in {', '.join(sorted(files)[:3])}{'…' if len(files) > 3 else ''})")


def _normalize_target(raw: str):
    """Bereinigt eine Verweisangabe zu einem Pfad oder liefert None, wenn keiner vorliegt."""
    t = raw.strip()
    if not t or t.startswith(("http://", "https://", "mailto:", "#", "//")):
        return None
    t = t.split("#", 1)[0]                    # Anker abtrennen
    t = re.sub(r":\d+(?:-\d+)?$", "", t)      # Fundstellenformat pfad/datei:zeile
    t = t.rstrip(".,;:")                      # Satzzeichen am Satzende
    if not t or t in (".", ".."):
        return None
    if t.endswith("-"):                       # Präfixnennung, z. B. ".devin/rules/00-"
        return None
    if "…" in t or t.endswith("..."):     # Sammelnennung, z. B. "framework/core/…"
        return None
    if any(c in NOT_A_PATH for c in t):
        return None
    return t


def _client_runtime_paths(root: str) -> dict:
    """Laufzeitpfade aller Client Packs: Praefix -> Clientname.

    Damit laesst sich unterscheiden, ob eine nicht aufloesbare Pfadangabe ein echter
    toter Verweis ist oder die Nennung eines Laufzeitpfads, der zu einem anderen
    Client Pack gehoert. Letzteres ist im werkzeugneutralen Kern eine Altlast,
    kein Fehler - aber es gehoert sichtbar gemacht.
    """
    out = {}
    base = os.path.join(root, KERN, "clients")
    if not os.path.isdir(base):
        return out
    for name in sorted(os.listdir(base)):
        mp = os.path.join(base, name, "manifest.json")
        if not os.path.exists(mp):
            continue
        try:
            man = json.loads(read(mp))
        except json.JSONDecodeError:
            continue
        for key in ("runtime_dir", "root_instruction_file"):
            if man.get(key):
                out[man[key]] = man["client"]
    return out


def _link_roots(root: str) -> tuple:
    """Wurzeln der Backtick-Heuristik: die festen des Frameworks und die jedes Packs.

    Die Laufzeitwurzeln stammen aus den Manifesten, damit ein neues Client Pack ohne
    Aenderung an dieser Pruefung erfasst wird - dieselbe Bauform wie
    _client_actor_names in Pruefung 14.
    """
    runtime: set[str] = set()
    base = os.path.join(root, KERN, "clients")
    if os.path.isdir(base):
        for name in sorted(os.listdir(base)):
            if name.startswith("_"):
                continue
            mp = os.path.join(base, name, "manifest.json")
            if not os.path.exists(mp):
                continue
            try:
                man = json.loads(read(mp))
            except json.JSONDecodeError:
                continue
            if man.get("runtime_dir"):
                runtime.add(man["runtime_dir"].rstrip("/") + "/")
            for key in ("root_instruction_file", "root_instruction_local"):
                if man.get(key):
                    runtime.add(man[key])
    return LINK_ROOTS_FEST + tuple(sorted(runtime))


def _target_exists(root: str, src_rel: str, target: str) -> bool:
    """Prüft repo-relativ, relativ zur verweisenden Datei und - für Dateien innerhalb
    eines Client Packs - relativ zu dessen root-template."""
    base = os.path.basename(target)
    # Nutzerlokale Dateien (Namensbestandteil ".local.") sind per .gitignore bewusst
    # nicht versioniert - CLAUDE.local.md, .claude/settings.local.json und Ähnliches.
    # Ein Verweis darauf beschreibt eine Möglichkeit, keine vorhandene Datei.
    if ".local." in base or base.endswith(".local"):
        return True
    # Eine mitgelieferte Vorlage zählt als Nachweis: Dateien wie .mcp.json legt die
    # nutzende Person selbst aus der .example-Fassung an.
    for cand in (target, target + ".example", target + ".template"):
        if os.path.exists(os.path.join(root, cand)):
            return True
    src_dir = os.path.dirname(os.path.join(root, src_rel))
    if os.path.exists(os.path.normpath(os.path.join(src_dir, target))):
        return True
    # Eine Datei im root-template eines Client Packs beschreibt die Laufzeitschicht
    # dieses Packs, nicht die installierte. Ihre Pfade dort aufloesen.
    m = re.match(r"(leitwerk-core/clients/[^/]+/root-template)/", src_rel)
    if m and os.path.exists(os.path.join(root, *m.group(1).split("/"), *target.split("/"))):
        return True
    return False


def check_links(root: str) -> None:  # noqa: C901
    """FW-KO-04: Querverweise zeigen auf existierende Dateien oder Verzeichnisse.

    Zwei Quellen: Markdown-Links (überall geprüft) und in Backticks genannte
    Framework-Pfade (Heuristik, in LINK_EXCEPTIONS ausgesetzt). Globs, Platzhalter
    und Befehlszeilen werden über NOT_A_PATH verworfen statt gemeldet.
    """
    fremdpfade = _client_runtime_paths(root)
    link_roots = _link_roots(root)
    for path in iter_text_files(root):
        if not path.endswith((".md", ".template")):
            continue
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if rel.startswith("leitwerk-core/tests/scripts/"):
            continue
        text = read(path)

        for m in MD_LINK_RE.finditer(text):
            target = _normalize_target(m.group(1))
            if target is not None and not _target_exists(root, rel, target):
                err(f"{rel}: Markdown-Link zeigt ins Leere: {m.group(1)}")

        if rel.startswith(LINK_EXCEPTIONS) or os.path.basename(rel) in LINK_EXCEPTION_BASENAMES:
            continue
        seen = set()
        for m in BACKTICK_RE.finditer(text):
            tok = m.group(1).strip()
            if not tok.startswith(link_roots):
                continue
            target = _normalize_target(tok)
            if target is None or target in seen:
                continue
            seen.add(target)
            if _target_exists(root, rel, target):
                continue
            # Gehoert der Pfad zur Laufzeitschicht eines anderen Client Packs, ist es
            # keine tote Referenz, sondern eine Client-Bindung im Kern (Arbeitsliste
            # fuer die Neutralisierung).
            fremd = next((c for pfx, c in fremdpfade.items()
                          if target == pfx or target.startswith(pfx.rstrip("/") + "/")), None)
            # Eine Datei im root-template eines Packs beschreibt dessen eigene
            # Laufzeitschicht - dort ist der Pfad richtig, nicht eine Altlast.
            if fremd and re.match(r"leitwerk-core/clients/[^/]+/root-template/", rel):
                continue
            # Ein Pfad eines anderen Packs ist kein toter Verweis, sondern eine
            # Client-Bindung. Seit 0.57.0 meldet sie Pruefung 48 - als Fehler, ueber
            # alle Traeger und ohne die drei Grenzen dieser Heuristik (D-128).
            if not fremd:
                err(f"{rel}: Pfadangabe existiert nicht: {tok}")


RUNTIME_PLACEHOLDER_RE = re.compile(
    r"<(RUNTIME_DIR|ROOT_INSTRUCTION_FILE|ROOT_INSTRUCTION_LOCAL|PERMISSIONS_FILE"
    r"|SKILLS_DIR|RULES_DIR|AGENTS_DIR|HOOKS_FILE|MCP_FILE|CLIENT_NAME)>")


def check_runtime_placeholders(root: str, man: dict) -> None:
    """In der installierten Laufzeitschicht darf kein Laufzeit-Platzhalter stehen.

    Sie werden von install.py aus dem Manifest aufgeloest. Bleibt einer stehen, fehlt
    er im Manifest des Client Packs - der Text verweist dann ins Leere.
    """
    rt = os.path.join(root, *man["runtime_dir"].split("/"))
    if not os.path.isdir(rt):
        return
    for dirpath, dirnames, filenames in os.walk(rt):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if os.path.splitext(fn)[1] not in TEXT_EXT:
                continue
            p = os.path.join(dirpath, fn)
            gefunden = {m.group(0) for m in RUNTIME_PLACEHOLDER_RE.finditer(read(p))}
            if gefunden:
                err(f"{os.path.relpath(p, root)}: unaufgelöste Laufzeit-Platzhalter "
                    f"{', '.join(sorted(gefunden))} – fehlen in runtime_placeholders des Client Packs")


def check_manifest(root: str) -> None:
    path = os.path.join(root, "project-overlay", "overlay-manifest.yaml")
    if not os.path.exists(path) or yaml is None:
        return
    try:
        data = yaml.safe_load(read(path)) or {}
    except yaml.YAMLError as exc:  # type: ignore[attr-defined]
        err(f"overlay-manifest.yaml ungültig: {exc}")
        return
    types = {"ai-governance", "ai-process-model", "roadmap", "architecture", "coding-guidelines",
             "definition-of-ready", "definition-of-done", "branching-strategy", "deployment",
             "security", "quality", "roles", "glossary", "other"}
    for key in ("manifest_version", "project_code", "overlay_version"):
        if key not in data:
            err(f"overlay-manifest.yaml: Kopfschlüssel {key} fehlt")
    seen = set()
    for doc in data.get("documents", []) or []:
        did = doc.get("id", "?")
        if did in seen:
            err(f"overlay-manifest.yaml: doppelte id {did}")
        seen.add(did)
        for key in ("id", "type", "title", "path", "context_class", "status", "load", "approved_by"):
            if key not in doc:
                err(f"overlay-manifest.yaml {did}: Feld {key} fehlt")
        if doc.get("type") not in types:
            err(f"overlay-manifest.yaml {did}: type '{doc.get('type')}' unbekannt")
        if doc.get("context_class") not in ("K1", "K2"):
            err(f"overlay-manifest.yaml {did}: context_class muss K1 oder K2 sein (K3 wird nicht registriert)")
        if doc.get("status") not in ("entwurf", "aktuell", "veraltet"):
            err(f"overlay-manifest.yaml {did}: status unbekannt")
        if doc.get("load") not in ("summary", "on-demand", "rule", "never"):
            err(f"overlay-manifest.yaml {did}: load unbekannt")
        if doc.get("load") == "rule" and not doc.get("rule_file"):
            err(f"overlay-manifest.yaml {did}: load rule ohne rule_file")
        if doc.get("load") == "summary" and doc.get("context_class") == "K2":
            err(f"overlay-manifest.yaml {did}: summary-Laden nur für K1 zulässig")


SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


def _overlay_version_angaben(root: str, man: dict) -> list[tuple[str, str]]:
    """Alle Stellen, an denen ein Overlay seine Version *erklaert*, als (Datei, Wert).

    Die Version steht dreimal: im Steckbrief, im Manifest und in der Laufzeitfassung.
    Bis 0.12.0 pruefte der Validator nur, ob der Manifestschluessel vorhanden ist - die
    drei Werte konnten beliebig auseinanderlaufen (FW-VN-01, Sonden S2 und S3). Das ist
    dieselbe Luecke, die D-23 fuer den Overlay-*Status* geschlossen hat.
    """
    angaben: list[tuple[str, str]] = []
    quellen = [
        os.path.join(root, "project-overlay", "OVERLAY.md"),
        os.path.join(root, *man["pack_runtime_dir"].split("/"), "20-project-overlay.md"),
    ]
    for path in quellen:
        if not os.path.exists(path):
            continue
        text = read(path)
        # Schraegstriche wie in den uebrigen Meldungen: Unter Windows liefert relpath
        # Backslashes, und eine gemischte Schreibweise war in D-23 bereits ein echter Fehler.
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        for m in re.finditer(r"^\|\s*Overlay-Version\s*\|\s*`?([^`|]+)", text, re.M):
            angaben.append((rel, m.group(1).strip()))
        for m in re.finditer(r"^-?\s*Overlay-Version:\s*`?([^`\n·]+)", text, re.M):
            angaben.append((rel, m.group(1).strip()))
    mpath = os.path.join(root, "project-overlay", "overlay-manifest.yaml")
    if os.path.exists(mpath) and yaml is not None:
        try:
            data = yaml.safe_load(read(mpath)) or {}
        except yaml.YAMLError:  # type: ignore[attr-defined]
            data = {}
        if "overlay_version" in data:
            angaben.append(("project-overlay/overlay-manifest.yaml",
                            str(data["overlay_version"]).strip()))
    return angaben


def check_versions(root: str, man: dict) -> None:
    """Pruefung 13 - die Nachweiskette aus governance/RELEASE_PROCESS.md Abschnitt 8.

    Geprueft wird nicht, ob Versionsfelder *da* sind - das taten die Pruefungen 5 und 8
    schon -, sondern ob sie *stimmen*. Genau diese Unterscheidung hat FW-VN-01 als Luecke
    ausgewiesen: Eine Versionsangabe, die keiner anderen widersprechen kann, unterscheidet
    keine zwei Zeitpunkte.
    """
    # Overlay-Version: alle Ablageorte muessen denselben Wert nennen. Noch nicht
    # ausgefuellte Vorlagen (<TBD: ...>) bleiben aussen vor - sie erklaeren nichts.
    angaben = [(rel, wert) for rel, wert in _overlay_version_angaben(root, man)
               if not TBD_RE.search(wert)]
    werte = {wert for _, wert in angaben}
    if len(werte) > 1:
        stellen = "; ".join(f"{rel}: {wert}" for rel, wert in angaben)
        err(f"Overlay-Version widersprüchlich angegeben ({stellen}). Steckbrief, Manifest "
            f"und Laufzeitfassung müssen denselben Wert nennen (RELEASE_PROCESS 8)")
    for rel, wert in angaben:
        if not SEMVER_RE.match(wert):
            err(f"{rel}: Overlay-Version '{wert}' ist kein Semantic Versioning "
                f"(MAJOR.MINOR.PATCH)")

    # Kompatible Framework-Version des Steckbriefs gegen die ausgelieferte Version.
    vpath = os.path.join(root, KERN, "VERSION")
    opath = os.path.join(root, "project-overlay", "OVERLAY.md")
    if not (os.path.exists(vpath) and os.path.exists(opath)):
        return
    version = read(vpath).strip()
    if not SEMVER_RE.match(version):
        err(f"{KERN}/VERSION: '{version}' ist kein Semantic Versioning (MAJOR.MINOR.PATCH)")
        return
    m = re.search(r"^\|\s*Kompatible Framework-Version\s*\|\s*`?([^`|]+)", read(opath), re.M)
    if not m:
        return
    angabe = m.group(1).strip()
    if TBD_RE.search(angabe):
        return
    major, minor, _ = version.split(".")
    if angabe not in (version, f"{major}.{minor}.x"):
        err(f"project-overlay/OVERLAY.md: Kompatible Framework-Version '{angabe}' passt nicht "
            f"zu {KERN}/VERSION ({version}). Erwartet '{major}.{minor}.x' oder '{version}' – "
            f"nach einer Aktualisierung ist der Steckbrief nachzuziehen "
            f"(docs/ADOPTION_GUIDE.md, Abschnitt Aktualisierung)")


# Der Status steht zweimal: als Zeile im Steckbrief und als Aussage im
# Aktivierungsabschnitt. Beide Schreibweisen liest overlay_status.status_angaben; sie
# stand bis 0.32.0 hier und im Status-Hook getrennt, mit verschiedenem Verhalten (B08).


# Steckbriefzeile eines versionierten Artefakts - genau zwei Spalten. Die Verankerung
# auf das Zeilenende ist noetig: Der Aenderungsverlauf eines Overlays beginnt mit der
# Kopfzeile '| Version | Datum | Aenderung | ... |', und die ist kein Steckbrief. "(Skill)" kommt in einzelnen
# Steckbriefen vor; die Klammer gehoert zur Beschriftung, nicht zum Wert.
ARTEFAKT_VERSION_RE = re.compile(
    r"^\|\s*Version(?:\s*\([^)]*\))?\s*\|\s*`?([^`|]+?)`?\s*\|\s*$", re.M)


def check_artefakt_versionen(root: str) -> None:
    """Teil von Pruefung 13: Die Versionsfelder der Kernartefakte haben die Form
    MAJOR.MINOR.PATCH.

    Der Kopfkommentar sagte diese Pruefung seit 0.13.0 zu; tatsaechlich deckte
    check_versions nur die Overlay-Version, <CORE_DIR>/VERSION und die Steckbriefangabe
    ab. Ein Artefaktfeld '0.1' oder 'abc' lief mit 0 Fehlern durch - aufgefallen bei der
    Regressionsprobe R1 zu CR-2026-020, waehrend 62 Versionsfelder von Hand gehoben
    wurden, ohne dass irgendetwas das Ergebnis geprueft haette.

    Historische Dokumente sind ausgenommen: Ein Aenderungsverlauf listet Versionen in
    Tabellenzeilen, nicht in einem Steckbrief, und beschreibt einen vergangenen Zustand.
    """
    for path in iter_text_files(root):
        if not path.endswith(".md"):
            continue
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if not rel.startswith(KERN + "/") or rel.startswith(KERN + "/clients/"):
            continue
        if rel.startswith(ACTOR_HISTORY) or os.path.basename(rel) in ACTOR_HISTORY_BASENAMES:
            continue
        m = ARTEFAKT_VERSION_RE.search(read(path))
        if not m:
            continue
        wert = m.group(1).strip()
        if not wert or TBD_RE.search(wert):
            continue
        if not SEMVER_RE.match(wert):
            err(f"{rel}: Versionsfeld '{wert}' ist kein Semantic Versioning "
                f"(MAJOR.MINOR.PATCH). Eine Angabe, die keiner Form folgt, laesst sich "
                f"nicht vergleichen - und eine Version, die sich nicht vergleichen laesst, "
                f"unterscheidet keine zwei Zeitpunkte (D-25, FW-VN-01)")


# Abschnitte des Overlays, die ueber die Aktivierungsreife entscheiden. Sie muessen da
# sein und sie muessen ausgefuellt sein - das eine ohne das andere ist keine Pruefung.
SICHERHEITSABSCHNITTE = ("## 4.", "## 5.", "## 6.", "## 13.", "## 14.", "## 15.")


def check_strict_overlay(root: str, man: dict) -> None:
    """Der **aktive** Zustand des Projekts (--strict-overlay) - clientneutral.

    Diese Funktion hiess bis 0.32.0 im Docstring und im Uebernahmeleitfaden "Pruefung der
    Aktivierungsreife" und verlangte dabei den Status 'aktiv'. Das war der Kern von B08:
    Der Leitfaden fuhr sie in Schritt 7 und setzte 'aktiv' erst in Schritt 9, die
    Uebernahmecheckliste trug sie als MUSS und galt "vor dem Setzen auf aktiv" - eine
    Voraussetzung, die sich selbst verlangte. Die Reifepruefung heisst seit 0.33.0
    --check-overlay-ready und ist eine eigene Funktion (D-57). Diese hier prueft den
    fertigen Zustand und bleibt dafuer unveraendert; sie hat mit dem
    Aktualisierungsablauf einen zweiten, funktionierenden Aufrufer.

    Bis 0.27.0 las diese Funktion zwei fest verdrahtete Pfade **eines** Clients und bekam
    das erkannte Manifest nicht uebergeben. In einer Installation des anderen Packs fand
    sie nichts, uebersprang alles und meldete null zusaetzliche Fehler.

    Gemessen am 2026-09-12 an zwei frischen Installationen mit demselben Defekt: Beim
    einen Pack aenderte sich die Fehlerzahl, beim anderen nicht (B02, D-44). Die
    Clienterkennung steht seit der Umstellung auf mehrere Packs in derselben Datei; sie
    wurde hier nur nicht benutzt.

    Zwei Befunde derselben Funktion sind dabei mit erledigt, beide aus der Messung:

    * **Der Status wurde als Praefix geprueft.** Damit bestand 'aktivierung-ausstehend'
      die Aktivierungspruefung - ein Wert, der woertlich sagt, dass die Aktivierung
      aussteht, liess den Fehler verschwinden, der vorher stand. Wer ihn eintrug, machte
      die Pruefung stiller. Jetzt gilt genau 'aktiv'.
    * **Ein fehlender sicherheitsrelevanter Abschnitt wurde akzeptiert.** Die Pruefung
      suchte nur in vorhandenen Abschnitten nach offenen Werten; fehlte der Abschnitt,
      fand sie nichts. Ein Overlay ohne Abschnitt 13 stand damit besser da als eines mit
      einem offenen Wert darin - die Pruefung auf den Kopf gestellt.

    GRENZE: Geprueft wird die Aktivierungs**reife**, nicht die Aktivierung. Dass ein
    Overlay 'aktiv' sagt, heisst nicht, dass der Client seine Regeln laedt.
    """
    runtime = os.path.join(root, *man["pack_runtime_dir"].split("/"), "20-project-overlay.md")
    overlay = os.path.join(root, "project-overlay", "OVERLAY.md")
    for path in (runtime, overlay):
        if not os.path.exists(path):
            continue
        text = read(path)
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        angaben = status_angaben(text)
        status, grund = auswerten(angaben)
        if status != AKTIV:
            # Der **Rohwert** gehoert in die Meldung, nicht nur die Auswertung: Der Fall,
            # der D-44 ausgeloest hat, war der Wert 'aktivierung-ausstehend' - er sagt
            # woertlich, dass die Aktivierung aussteht, und genau das soll lesbar sein.
            # Die Sonde zu D-44 hat diesen Verlust beim Umbau auf overlay_status.py
            # gefangen; ohne sie waere die Meldung stiller geworden.
            roh = ", ".join("'%s'" % a.strip() for a in angaben) or "keine Angabe"
            err(f"{rel}: Overlay-Status ist nicht '{AKTIV}', sondern {roh} "
                f"(ausgewertet als '{status}': {grund}) (strict-overlay)")
        if path == runtime and TBD_RE.search(text):
            err(f"{rel}: enthält offene <TBD>-Werte (strict-overlay)")
        if path == overlay:
            for sec in SICHERHEITSABSCHNITTE:
                m = re.search(rf"{re.escape(sec)}.*?(?=\n## |\Z)", text, re.S)
                if not m:
                    err(f"{rel}: sicherheitsrelevanter Abschnitt {sec} fehlt (strict-overlay)")
                elif TBD_RE.search(m.group(0)):
                    err(f"{rel}: Abschnitt {sec} enthält offene <TBD>-Werte (sicherheitsrelevant, strict-overlay)")
    rechte = os.path.join(root, *man["permissions_file"].split("/"))
    if os.path.exists(rechte):
        inhalt = read(rechte)
        if TBD_RE.search(inhalt) or PLACEHOLDER_RE.search(inhalt):
            err(f"{man['permissions_file']}: enthält noch Platzhalter (strict-overlay)")


def check_overlay_ready(root: str, man: dict) -> None:
    """Aktivierungsreife eines Kandidaten (--check-overlay-ready) - clientneutral.

    Die Pruefung, die B08 gefehlt hat: Sie prueft alles, was --strict-overlay prueft,
    **ausser** dem Status - und beim Status erwartet sie das Gegenteil, naemlich einen
    Kandidaten, der noch nicht aktiv ist. Damit ist der dokumentierte Ablauf ohne
    Regelbruch begehbar: erst vollstaendig ausfuellen und pruefen, dann durch einen
    Menschen aktivieren, dann mit --strict-overlay nachpruefen (D-57).

    Warum sie einen aktiven Kandidaten als Fehler meldet und nicht durchlaesst: Sonst
    waere sie die schwaechere Variante von --strict-overlay und wuerde als deren Ersatz
    benutzt. Eine Pruefung, die zwei Zustaende gleich behandelt, unterscheidet keine zwei
    Zustaende.

    Die Statusangaben MUESSEN untereinander uebereinstimmen. Ein Kandidat, der in der
    Laufzeitfassung 'aktiv' und im Quell-Overlay 'inaktiv' erklaert, ist kein Kandidat,
    sondern eine Drift - derselbe Fall, den der Status-Hook bis 0.32.0 zugunsten der
    ersten gelesenen Datei entschied.

    GRENZE: Geprueft wird die Vollstaendigkeit der Konfiguration. Die **fachliche**
    Freigabe kann kein Skript erteilen; die Uebernahmecheckliste bleibt der Nachweis
    (FW-CL-10). Und dass ein Overlay vollstaendig ist, heisst nicht, dass seine Werte
    richtig sind.
    """
    runtime = os.path.join(root, *man["pack_runtime_dir"].split("/"), "20-project-overlay.md")
    overlay = os.path.join(root, "project-overlay", "OVERLAY.md")
    vorhanden = [p for p in (runtime, overlay) if os.path.exists(p)]
    if not vorhanden:
        err("check-overlay-ready: weder die Laufzeitfassung des Overlays noch "
            "project-overlay/OVERLAY.md ist vorhanden - es gibt keinen Kandidaten")
        return

    alle_angaben = []
    for path in vorhanden:
        text = read(path)
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        angaben = status_angaben(text)
        alle_angaben.extend(angaben)
        if not angaben:
            err(f"{rel}: keine Angabe zum Overlay-Status gefunden (check-overlay-ready)")
        # Offene Werte: in der Laufzeitfassung ueberall, im Overlay in den
        # sicherheitsrelevanten Abschnitten. Dieselbe Aufteilung wie --strict-overlay;
        # ein Kandidat unterscheidet sich vom aktiven Overlay im Status, nicht im Inhalt.
        if path == runtime and TBD_RE.search(text):
            err(f"{rel}: enthält offene <TBD>-Werte (check-overlay-ready)")
        if path == overlay:
            for sec in SICHERHEITSABSCHNITTE:
                m = re.search(rf"{re.escape(sec)}.*?(?=\n## |\Z)", text, re.S)
                if not m:
                    err(f"{rel}: sicherheitsrelevanter Abschnitt {sec} fehlt "
                        f"(check-overlay-ready)")
                elif TBD_RE.search(m.group(0)):
                    err(f"{rel}: Abschnitt {sec} enthält offene <TBD>-Werte "
                        f"(sicherheitsrelevant, check-overlay-ready)")

    status, grund = auswerten(alle_angaben)
    if status == AKTIV:
        err(f"check-overlay-ready: Der Overlay-Status ist bereits '{AKTIV}'. Diese "
            f"Pruefung gilt fuer einen Kandidaten **vor** der Aktivierung; fuer den "
            f"aktiven Zustand ist --strict-overlay zustaendig (D-57)")
    elif status == WIDERSPRUECHLICH:
        err(f"check-overlay-ready: {grund}. Ein Kandidat erklaert seinen Status an allen "
            f"Stellen gleich; abweichende Angaben sind eine Drift, kein Kandidat")
    elif status == UNBEKANNT:
        err(f"check-overlay-ready: Overlay-Status nicht ausgefuellt ({grund}). Erwartet "
            f"wird '{INAKTIV}' - ein Kandidat sagt, dass er noch nicht aktiv ist, statt "
            f"die Angabe offen zu lassen")

    rechte = os.path.join(root, *man["permissions_file"].split("/"))
    if os.path.exists(rechte):
        inhalt = read(rechte)
        if TBD_RE.search(inhalt) or PLACEHOLDER_RE.search(inhalt):
            err(f"{man['permissions_file']}: enthält noch Platzhalter "
                f"(check-overlay-ready)")
    else:
        err(f"{man['permissions_file']}: fehlt - ohne Berechtigungsdatei ist kein "
            f"Kandidat vollstaendig (check-overlay-ready)")


# Pruefung 14: Der werkzeugneutrale Kern nennt keinen Client als Akteur.
# Historische Dokumente bleiben ausgenommen - sie beschreiben einen vergangenen
# Zustand (docs/RUNTIME_GLOSSARY.md, Abschnitt "Regel").
ACTOR_HISTORY = (
    "leitwerk-core/CHANGELOG.md",
    "leitwerk-core/governance/change-requests/",
    "leitwerk-core/governance/DECISION_LOG.md",
    "leitwerk-core/tests/protocols/",
)
# Jeder Aenderungsverlauf ist ein historisches Dokument, nicht nur der des Frameworks.
ACTOR_HISTORY_BASENAMES = ("CHANGELOG.md",)


def _client_actor_names(root: str) -> list[tuple[str, str]]:
    """Kapitalisierter Produktname je Client Pack, abgeleitet aus dessen Kennung.

    Aus der Kennung, nicht aus einer gepflegten Liste: Ein neues Client Pack bringt
    seinen Namen damit selbst mit und wird ohne Aenderung an dieser Pruefung erfasst.
    """
    namen = set()
    cdir = os.path.join(root, "leitwerk-core", "clients")
    if not os.path.isdir(cdir):
        return []
    for name in sorted(os.listdir(cdir)):
        mf = os.path.join(cdir, name, "manifest.json")
        if not os.path.isfile(mf):
            continue
        try:
            kennung = json.loads(read(mf)).get("client", name)
        except Exception:
            kennung = name
        teile = [w.capitalize() for w in kennung.split("-")]
        namen.add((teile[0], "-".join(teile)))
    return sorted(namen)


def check_actor_naming(root: str) -> None:
    """Pruefung 14 (D-02): Kein Client wird im Kern als Handelnder benannt.

    Der Kern beschreibt, was ein KI-Client tun MUSS - nicht, was ein bestimmtes
    Produkt tut. Erlaubt bleibt der Produktname mit Zusatz ("Devin Desktop",
    "Claude Code"): Er benennt ein Produkt, nicht den Handelnden. Muss ein Kerntext
    den Namen selbst tragen, steht dort <CLIENT_NAME>.
    """
    namen = _client_actor_names(root)
    if not namen:
        return
    # Der Produktname ist erlaubt, die Akteursbezeichnung nicht: "Devin Desktop"
    # und "Devin-Desktop" benennen ein Produkt, der blosse Name den Handelnden.
    erlaubt = re.compile("|".join(
        [re.escape(v) for _, v in namen] + [re.escape(v.replace("-", " ")) for _, v in namen]
        + [r"%s [A-Z]\w+" % re.escape(k) for k, _ in namen]))
    muster = re.compile(r"\b(%s)\b" % "|".join(k for k, _ in namen))
    for path in iter_text_files(root):
        if not path.endswith((".md", ".py", ".template")):
            continue
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if not rel.startswith("leitwerk-core/") or rel.startswith("leitwerk-core/clients/"):
            continue
        if rel.startswith(ACTOR_HISTORY) or os.path.basename(rel) in ACTOR_HISTORY_BASENAMES:
            continue
        for i, zeile in enumerate(read(path).splitlines(), 1):
            m = muster.search(erlaubt.sub("", zeile))
            if not m:
                continue
            err(f"{rel}:{i}: '{m.group(1)}' benennt einen Client als Akteur; der Kern ist "
                f"werkzeugneutral (D-02). Gemeint ist der Begriff 'der KI-Client'; muss der "
                f"Text den Produktnamen tragen, steht dort <CLIENT_NAME>")


# Ein Platzhalter, der einen Clientnamen traegt, bindet den Kern genauso an ein Produkt
# wie eine Akteursnennung - nur faellt er dort nicht auf, weil er in Grossbuchstaben
# steht. Das Register selbst ist ausgenommen: Es nennt Platzhalter, es verwendet sie nicht.
PLATZHALTER_RE = re.compile(r"<([A-Z][A-Z0-9_ ]{2,80})>")
PLATZHALTER_AUSNAHMEN = (KERN + "/docs/PLACEHOLDER_REGISTRY.md",)


def check_placeholder_naming(root: str) -> None:
    """Teil von Pruefung 14: Kein Platzhalter des Kerns traegt einen Clientnamen.

    Der Marker 'VERIFY AGAINST CURRENT <name> DOCUMENTATION' stand acht Releases im Kern,
    obwohl die clientneutrale Form daneben im Register gefuehrt wurde. Die Akteurspruefung
    fand ihn nicht: Sie sucht den kapitalisierten Namen, der Marker schreibt ihn gross.
    """
    namen = _client_actor_names(root)
    if not namen:
        return
    gesucht = {k.upper() for k, _ in namen}
    for path in iter_text_files(root):
        if not path.endswith((".md", ".py", ".template")):
            continue
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if not rel.startswith(KERN + "/") or rel.startswith(KERN + "/clients/"):
            continue
        if (rel.startswith(ACTOR_HISTORY) or rel in PLATZHALTER_AUSNAHMEN
                or os.path.basename(rel) in ACTOR_HISTORY_BASENAMES):
            continue
        for i, zeile in enumerate(read(path).splitlines(), 1):
            for m in PLATZHALTER_RE.finditer(zeile):
                # An Leerzeichen UND Unterstrichen trennen: Ein Platzhalter wie
                # 'NAME_PROJECT_DIR' bindet genauso an ein Produkt wie einer, der den
                # Namen als eigenes Wort fuehrt.
                treffer = gesucht & set(re.split(r"[ _]+", m.group(1)))
                if treffer:
                    err(f"{rel}:{i}: Der Platzhalter <{m.group(1)}> traegt den Clientnamen "
                        f"'{sorted(treffer)[0]}'. Ein Platzhalter bindet den Kern damit an ein "
                        f"Produkt (D-02); die clientneutrale Form gehoert in den Kern, die "
                        f"clientgebundene in das Client Pack")


# Pruefung 15: Der Interpreter der Hook-Aufrufe startet auf dieser Maschine wirklich
# Python. Geprueft wird die Wirkung, nicht die Anwesenheit des Namens (AP2-CC-13).
HOOK_SONDE = "LEITWERK-INTERPRETER-OK"


def _hook_kommandos(root: str, man: dict) -> list[tuple[str, str]]:
    """(Fundstelle, Kommando) je konfiguriertem Hook - aus beiden Ablageformen."""
    treffer: list[tuple[str, str]] = []
    # Der Ort der Hook-Konfiguration steht in der Platzhalterabbildung des Packs; bei
    # einem Client ohne eigene Hook-Datei zeigt sie auf die Berechtigungsdatei.
    orte = {man.get("permissions_file"),
            (man.get("runtime_placeholders") or {}).get("<HOOKS_FILE>")}
    for rel in sorted(k for k in orte if k):
        pfad = os.path.join(root, *rel.split("/"))
        if not os.path.exists(pfad):
            continue
        try:
            daten = json.loads(read(pfad))
        except json.JSONDecodeError:
            continue
        # Eigene Hook-Datei: das Objekt steht oben. Hooks in der Berechtigungsdatei:
        # unter dem Schluessel "hooks".
        hooks = daten.get("hooks") if "hooks" in daten else daten
        if not isinstance(hooks, dict):
            continue
        for ereignis, eintraege in hooks.items():
            if ereignis.startswith("_") or not isinstance(eintraege, list):
                continue
            for eintrag in eintraege:
                for h in (eintrag or {}).get("hooks", []):
                    befehl = h.get("command")
                    if befehl:
                        treffer.append((f"{rel}:{ereignis}", befehl))
    return treffer


def check_hook_interpreter(root: str, man: dict) -> None:
    """Pruefung 15 (AP2-CC-13): Ein Hook, der nicht startet, setzt nichts durch.

    Die Hooks tragen die Zusage H2 der Faehigkeitsmatrix und die Overlay-Statusmeldung.
    Wird der Aufruf mit einem Interpreternamen erzeugt, den es auf der Zielmaschine
    nicht gibt - unter Windows ist "python3" haeufig der Microsoft-Store-Alias -, endet
    der Hook mit Fehler statt mit einer Entscheidung, und die Zusage gilt dort nicht.

    Geprueft wird die Wirkung: Der Interpreter muss eine Sonde ausgeben. Anwesenheit im
    Pfad ist kein Nachweis; genau daran ist der Store-Alias vorbeigekommen.
    """
    kommandos = _hook_kommandos(root, man)
    if not kommandos:
        return
    geprueft: dict[str, str] = {}
    for fundstelle, befehl in kommandos:
        name = shlex.split(befehl, posix=False)[0].strip('"') if befehl.strip() else ""
        if not name:
            continue
        if name not in geprueft:
            try:
                lauf = subprocess.run(
                    [name, "-c", "import sys; sys.stdout.write('%s')" % HOOK_SONDE],
                    capture_output=True, text=True, timeout=15)
                ok = lauf.returncode == 0 and HOOK_SONDE in (lauf.stdout or "")
                geprueft[name] = "" if ok else f"Exit {lauf.returncode}"
            except (OSError, subprocess.SubprocessError) as fehler:
                geprueft[name] = type(fehler).__name__
        if geprueft[name]:
            err(f"{fundstelle}: Der Hook wird mit '{name}' aufgerufen, das auf dieser "
                f"Maschine keinen Python-Interpreter startet ({geprueft[name]}). Der Hook "
                f"laeuft damit nicht, und ein Schutz-Hook, der nicht laeuft, blockiert "
                f"nichts (AP2-CC-13). 'install.py --update' erzeugt den Aufruf mit einem "
                f"Interpreter, der hier funktioniert")


def check_hook_tool_coverage(root: str, man: dict) -> None:
    """Pruefung 16 (AP2-CC-16): Der Schutz-Hook erkennt jeden abgebildeten Werkzeugnamen.

    Das Manifest jedes Client Packs bildet die Verben der Kernquelle auf die
    Werkzeugnamen seines Clients ab (hook_tools). Diese Abbildung galt bis 0.21.0 nur
    fuer den Matcher der Hook-Konfiguration - der Hook selbst verglich gegen die
    generischen Verbnamen. Folge: Bei einem Client, dessen Ausfuehrungswerkzeug nicht
    'exec' heisst, lief die Pfadpruefung fuer Shell-Befehle ins Leere.

    Geprueft wird die Wirkung, nicht die Uebereinstimmung zweier Listen: Der Hook wird
    je Werkzeugname mit einer Sonde aufgerufen, die er blockieren MUSS. Eine Zusage,
    die man nur durch Vergleich zweier Listen belegt, ist genau die Art Pruefung, an
    der dieser Befund vorbeigekommen ist.

    Dazu je eine Gegenprobe, die NICHT blockiert werden darf: Ein lesender oder
    ausfuehrender Zugriff auf einen Kernpfad. Ohne sie bliebe unbemerkt, wenn die
    Secret-Sperre sich still in eine Sperre auf das gesamte Kernverzeichnis verwandelt.

    Die Grenze bleibt: Geprueft werden die Verben, die das Manifest fuehrt. Ein Client
    mit einem vierten Werkzeugverb faellt hier nicht auf - das kann nur eine Sitzung
    erheben, die die Werkzeugnamen misst (AP2-DD-11).
    """
    skript = os.path.join(root, KERN, "tests", "scripts", "hook-check-secrets.py")
    if not os.path.isfile(skript):
        return
    interpreter = _hook_interpreter()
    if interpreter is None:
        return  # Pruefung 15 meldet diesen Fall bereits
    # Alle Packs, nicht nur das installierte: Der Hook liegt einmal im Kern und wird
    # von allen geteilt. Ein Werkzeugname, den ein anderes Pack abbildet, faellt sonst
    # erst dort auf, wo es keine Installation zum Pruefen gibt - genau die Lage, in der
    # AP2-CC-16 acht Releases lang unbemerkt blieb.
    abbildungen = []
    packs = os.path.join(root, KERN, "clients")
    for name in sorted(os.listdir(packs)) if os.path.isdir(packs) else []:
        mf = os.path.join(packs, name, "manifest.json")
        if not os.path.isfile(mf):
            continue
        try:
            daten = json.loads(read(mf)) or {}
        except json.JSONDecodeError:
            continue
        abbildungen.append((daten.get("client", name), daten.get("hook_tools") or {}))
    # Je Verb eine Sonde auf einen Secret-Pfad, die blockiert werden MUSS. Das Leseverb
    # steht seit D-33 dabei: D-30 hatte Secret-Pfade auch gegen lesende Werkzeuge
    # durchgesetzt, der Code loeste es nicht ein, und diese Pruefung konnte es nicht
    # finden - sie sondierte genau die beiden Verben, die das Manifest fuehrte, und mass
    # die Abbildung damit an sich selbst (AP2-DD-11).
    sonden = {"exec": {"command": "cat .env"}, "write": {"file_path": ".env", "content": "x"},
              "read": {"file_path": ".env"}}
    # Gegenprobe je Verb: Ein Zugriff auf einen Kernpfad, der NICHT blockiert werden darf.
    # Lesende und ausfuehrende Werkzeuge duerfen den Kern lesen - P4 setzt das voraus, und
    # ohne diese Probe verwandelte die Erweiterung die Secret-Sperre still in eine Sperre
    # auf das gesamte Kernverzeichnis (D-30, zweites Schutzziel).
    # Der Pfad muss ein Strukturpfad sein, sonst prueft die Gegenprobe nichts: Ein
    # beliebiger Kernpfad wie VERSION steht in keiner der beiden Musterlisten und waere
    # auch dann nicht blockiert, wenn die Trennung aufgehoben ist. Genau daran ist die
    # erste Fassung dieser Gegenprobe vorbeigelaufen - sie bestand, ohne etwas zu messen.
    gegenproben = {"exec": {"command": f"git diff {KERN}/framework/core/00-purpose.md"},
                   "read": {"file_path": f"{KERN}/framework/core/00-purpose.md"}}
    for pack, abbildung in abbildungen:
      for verb, eingabe in sonden.items():
        for werkzeug in abbildung.get(verb) or []:
            payload = json.dumps({"tool_name": werkzeug, "tool_input": eingabe})
            try:
                lauf = subprocess.run([interpreter, skript], input=payload,
                                      capture_output=True, text=True, timeout=20)
            except (OSError, subprocess.SubprocessError) as fehler:
                err(f"Schutz-Hook nicht ausfuehrbar ({type(fehler).__name__})")
                return
            if lauf.returncode != 2:
                err(f"{pack}/manifest.json: Der Schutz-Hook erkennt den "
                    f"Werkzeugnamen '{werkzeug}' nicht, den dieses Pack fuer das Verb "
                    f"'{verb}' abbildet - eine Sonde auf einen Secret-Pfad wurde nicht "
                    f"blockiert (Exit {lauf.returncode} statt 2). Die Abbildung erreicht "
                    f"den Matcher, aber nicht die Pruefung im Hook (AP2-CC-16)")
      for verb, eingabe in gegenproben.items():
        for werkzeug in abbildung.get(verb) or []:
            payload = json.dumps({"tool_name": werkzeug, "tool_input": eingabe})
            try:
                lauf = subprocess.run([interpreter, skript], input=payload,
                                      capture_output=True, text=True, timeout=20)
            except (OSError, subprocess.SubprocessError):
                continue  # der Sondenlauf oben meldet einen nicht ausfuehrbaren Hook
            if lauf.returncode != 0:
                err(f"{pack}/manifest.json: Der Schutz-Hook blockiert einen nicht "
                    f"schreibenden Zugriff auf einen Strukturpfad des Kerns mit dem "
                    f"Werkzeug '{werkzeug}' (Verb '{verb}', Exit {lauf.returncode} "
                    f"statt 0). "
                    f"Strukturpfade sind integritaetsgeschuetzt und gelten nur fuer "
                    f"schreibende Werkzeuge; P4 setzt voraus, dass der Kern lesbar "
                    f"bleibt (D-30)")


# Pruefung 17: Der Schutz-Hook laesst eine unlesbare Eingabe nur dort durch, wo das
# Client Pack das Eingabeschema als unbestaetigt fuehrt (D-31).
HOOK_UNLESBAR = "kein json {"


def _hook_selbsttest(interpreter: str, skript: str, argumente: list[str]) -> int:
    """Ruft den Schutz-Hook mit einer nicht parsebaren Eingabe auf und liefert den Exit-Code."""
    try:
        lauf = subprocess.run([interpreter, skript] + argumente, input=HOOK_UNLESBAR,
                              capture_output=True, text=True, timeout=20,
                              env={k: v for k, v in os.environ.items()
                                   if k != "FW_HOOK_FAIL_CLOSED"})
    except (OSError, subprocess.SubprocessError):
        return -1
    return lauf.returncode


def check_hook_fail_closed(root: str, man: dict) -> None:
    """Pruefung 17 (D-31): Fail-closed gilt dort, wo das Pack es zusagt - und wirkt.

    Der Schutz-Hook laesst eine Eingabe, die er nicht als JSON lesen kann, standardmaessig
    durch. Das war richtig, solange kein Eingabeschema gegen eine Installation bestaetigt
    war; fuer ein Pack, das es fuehrt, ist es eine Luecke. Der Schalter steht im
    Aufrufkommando (--fail-closed), nicht in der Umgebung: Ob ein Client env an den
    Hook-Prozess weiterreicht, ist fuer keines der Packs belegt.

    Geprueft wird in zwei Ebenen, und beide sind noetig:

    1. Am Skript: Das Argument muss ueberhaupt wirken - mit --fail-closed Exit 2, ohne
       Exit 0. Diese Ebene laeuft auch dort, wo es keine Installation gibt. Ohne sie
       faellt ein Schalter, der ins Leere greift, erst in einer Installation auf - genau
       die Lage, in der AP2-CC-16 acht Releases lang unbemerkt blieb.
    2. An der erzeugten Konfiguration: Das Kommando wird so aufgerufen, wie es dort steht,
       und sein Verhalten gegen die Zusage des Packs gehalten. Diese Ebene prueft die
       ganze Kette - Manifest, Abbildung, Konfiguration, Verhalten -, nicht die
       Uebereinstimmung zweier Felder.

    Die Umgebungsvariable wird fuer den Aufruf entfernt: Sonst bestuende der Test auch
    dann, wenn das Argument nichts bewirkt.
    """
    skript = os.path.join(root, KERN, "tests", "scripts", "hook-check-secrets.py")
    if not os.path.isfile(skript):
        return
    interpreter = _hook_interpreter()
    if interpreter is None:
        return  # Pruefung 15 meldet diesen Fall bereits

    # Ebene 1: Wirkt das Argument?
    mit = _hook_selbsttest(interpreter, skript, ["--fail-closed"])
    ohne = _hook_selbsttest(interpreter, skript, [])
    if mit != 2:
        err(f"{KERN}/tests/scripts/hook-check-secrets.py: Der Aufruf mit --fail-closed "
            f"blockiert eine nicht lesbare Eingabe nicht (Exit {mit} statt 2). Ein Pack, "
            f"das fail-closed zusagt, erzeugt damit ein Kommando ohne Wirkung (D-31)")
    if ohne != 0:
        err(f"{KERN}/tests/scripts/hook-check-secrets.py: Der Aufruf ohne --fail-closed "
            f"laesst eine nicht lesbare Eingabe nicht durch (Exit {ohne} statt 0). Bei "
            f"einem Pack mit unbestaetigtem Eingabeschema blockierte damit jede Sitzung, "
            f"deren Schema abweicht (D-31)")

    # Ebene 2: Traegt die erzeugte Konfiguration die Zusage ihres Packs?
    zusage = man.get("hook_fail_closed") is True
    for fundstelle, befehl in _hook_kommandos(root, man):
        teile = [t.strip('"') for t in shlex.split(befehl, posix=False)]
        if not any(os.path.basename(t) == "hook-check-secrets.py" for t in teile[1:]):
            continue
        argumente = [t for t in teile[2:] if t.startswith("-")]
        ergebnis = _hook_selbsttest(interpreter, skript, argumente)
        erwartet = 2 if zusage else 0
        if ergebnis != erwartet:
            wie = ("blockiert eine nicht lesbare Eingabe nicht" if zusage
                   else "blockiert eine nicht lesbare Eingabe, statt sie durchzulassen")
            # Liegt die Hook-Konfiguration in der Berechtigungsdatei, ist sie Saat und
            # gehoert nach der Erstinstallation dem Projekt: '--update' fasst sie nie an.
            # Ein Rat, der dorthin verweist, saegte eine Behebung zu, die nicht eintritt.
            in_saat = fundstelle.split(":")[0] == man.get("permissions_file")
            weg = ("Bei diesem Client steht die Hook-Konfiguration in der "
                   "Berechtigungsdatei und damit in der Saat; 'install.py --update' "
                   "fasst sie nicht an. Das Kommando ist von Hand nachzuziehen"
                   if in_saat else "'install.py --update' erzeugt das Kommando neu")
            err(f"{fundstelle}: Das Pack '{man.get('client', '?')}' fuehrt "
                f"hook_fail_closed={str(zusage).lower()}, aber das erzeugte Kommando "
                f"{wie} (Exit {ergebnis} statt {erwartet}). Die Abbildung erreicht die "
                f"Konfiguration nicht, oder das Kommando traegt das falsche Argument "
                f"(D-31). {weg}")


# Pruefung 18: Die Hook-Konfiguration steht dort, wo der Client sie liest - und nirgends
# sonst. Ein zweiter, verwaister Ort ist gefaehrlicher als gar keiner (D-32).
VERWAISTE_HOOK_DATEIEN = ("hooks.v1.json",)


def _check_vorlagen_ohne_hookdatei(root: str) -> None:
    """Teil von Pruefung 18 (CR-2026-036 E3): Keine Vorlage liefert eine Hook-Datei aus.

    Ein ausgeliefertes Dokument beschrieb bis 0.25.0 genau den Zustand, den dieselbe
    Pruefung als Altlast meldete: Die Laufzeit-README fuehrte die eigene Hook-Datei unter
    den gelieferten Dateien, obwohl die Installation sie nicht mehr anlegt (D-32).

    Gemeldet wird deshalb nur die **Behauptung einer Lieferung** - der Dateiname als
    erste Zelle einer Tabellenzeile, dort steht in diesen READMEs das gelieferte
    Artefakt. Eine Nennung im Fliesstext, die die Abwesenheit **erklaert**, bleibt
    unbeanstandet; sie ist der Migrationshinweis und soll dort stehen. Der Fehlalarm,
    den eine reine Namenssuche erzeugt haette, ist damit vermieden.
    """
    for name in sorted(os.listdir(os.path.join(root, KERN, "clients"))
                       if os.path.isdir(os.path.join(root, KERN, "clients")) else []):
        vorlage = os.path.join(root, KERN, "clients", name, "root-template")
        if not os.path.isdir(vorlage):
            continue
        for pfad in _walk_text_files(vorlage):
            if not pfad.endswith(".md"):
                continue
            rel = os.path.relpath(pfad, root).replace(os.sep, "/")
            for i, zeile in enumerate(read(pfad).splitlines(), 1):
                zellen = tabellenzellen(zeile) \
                    if zeile.strip().startswith("|") else []
                erste = zellen[0].strip("` *") if zellen else ""
                if erste in VERWAISTE_HOOK_DATEIEN or \
                        any(erste.endswith("/" + v) for v in VERWAISTE_HOOK_DATEIEN):
                    err(f"{rel}:{i}: Die Vorlage fuehrt '{erste}' als geliefertes "
                        f"Artefakt. Seit D-32 legt die Installation keine eigene "
                        f"Hook-Datei an; ein ausgeliefertes Dokument beschriebe damit "
                        f"genau den Zustand, den Pruefung 18 als Altlast meldet")


def check_hook_ablageort(root: str, man: dict) -> None:
    """Pruefung 18 (D-32): Keine verwaiste Hook-Datei neben der wirksamen.

    Ob ein Client eine Datei **liest**, kann kein Validator feststellen - das kann nur
    eine Sitzung, und genau dort ist AP2-DD-10 aufgefallen: Aus der eigenen Hook-Datei
    des Packs fuehrte der KI-Client keinen Hook aus, dieselbe Konfiguration in der
    Berechtigungsdatei lief sofort. Seit D-32 liegen die Hooks dort.

    Was diese Pruefung leisten kann, ist das Aufraeumen danach: 'install.py --update'
    schreibt die neue Datei, entfernt die alte aber nicht. Zurueck bleibt eine
    Hook-Konfiguration, die aussieht, als gaelte sie - und die bei einer kuenftigen
    Clientversion, die den Ort doch liest, eine zweite, veraltete Regelmenge waere.

    Sie belegt damit nichts ueber die Wirkung; sie haelt einen Zustand fest, der nach
    einer Migration entsteht. Das ist ausdruecklich weniger als ein Wirkungsnachweis
    nach D-23 und hier auch nicht mehr moeglich.
    """
    _check_vorlagen_ohne_hookdatei(root)
    rechte = man.get("permissions_file")
    hooks_ort = (man.get("runtime_placeholders") or {}).get("<HOOKS_FILE>")
    if not rechte or hooks_ort != rechte:
        return  # Client mit eigener Hook-Datei - nichts aufzuraeumen
    runtime = (man.get("runtime_placeholders") or {}).get("<RUNTIME_DIR>")
    if not runtime:
        return
    for name in VERWAISTE_HOOK_DATEIEN:
        pfad = os.path.join(root, *runtime.split("/"), name)
        if os.path.exists(pfad):
            warn(f"{runtime}/{name} liegt neben der wirksamen Hook-Konfiguration in "
                 f"{rechte}. Dieses Pack fuehrt seine Hooks seit 0.25.0 in der "
                 f"Berechtigungsdatei, weil der Client die eigene Datei nicht liest "
                 f"(AP2-DD-10, D-32); 'install.py --update' entfernt sie nicht. Die "
                 f"verwaiste Datei ist von Hand zu loeschen - sonst steht dort eine "
                 f"Regelmenge, die aussieht, als gaelte sie")


# ---------------------------------------------------------------------------
# Pruefungen 19 bis 24 (Release 0.26.0)
# ---------------------------------------------------------------------------

AUSKUNFT_UEBERSCHRIFT = "Anweisungs- und Konfigurationsquellen außerhalb des Projekts"
DATUM_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")


def _client_packs(root: str) -> list[tuple[str, str, dict]]:
    """(Kennung, Verzeichnis, Manifest) je Client Pack; _template ohne Manifest."""
    raus: list[tuple[str, str, dict]] = []
    cdir = os.path.join(root, KERN, "clients")
    if not os.path.isdir(cdir):
        return raus
    for name in sorted(os.listdir(cdir)):
        pdir = os.path.join(cdir, name)
        if not os.path.isdir(pdir):
            continue
        if not os.path.isfile(os.path.join(pdir, "CLIENT_PACK.md")):
            continue
        mf = os.path.join(pdir, "manifest.json")
        man: dict = {}
        if os.path.isfile(mf):
            try:
                man = json.loads(read(mf))
            except Exception:
                man = {}
        raus.append((name, pdir, man))
    return raus


def _abschnitt(text: str, ueberschrift: str) -> str | None:
    """Text eines Abschnitts bis zur naechsten gleichrangigen Ueberschrift."""
    m = re.search(r"^(#{2,3})\s*\d*[a-z]?\.?\s*" + re.escape(ueberschrift) + r"\s*$",
                  text, re.M)
    if not m:
        return None
    ebene = len(m.group(1))
    rest = text[m.end():]
    weiter = re.search(r"^#{1,%d}\s" % ebene, rest, re.M)
    return rest[:weiter.start()] if weiter else rest


def check_quellenauskunft(root: str) -> None:
    """Pruefung 19 (D-34, D-37): Jedes Client Pack gibt Auskunft ueber Quellen ausserhalb.

    GRENZE DIESER PRUEFUNG - sie steht hier, weil sie im Antrag vorab benannt und nicht
    spaeter gefunden werden soll (CR-2026-031 E4): Geprueft wird die **Anwesenheit** der
    Auskunft, nicht ihre **Richtigkeit**. Eine falsche oder veraltete Zeile besteht sie.
    Ein Abwesenheitsbeleg altert, und dieses Skript sieht den Unterschied nicht - "keine
    bekannt, Stand 2026-09-11" ist am Tag der naechsten Clientversion eine Behauptung
    ueber die Vergangenheit. Die Richtigkeit haengt an einer Erhebung, nicht an einem
    Skript; dasselbe gilt fuer Pruefung 22.
    """
    for kennung, pdir, _man in _client_packs(root):
        rel = f"{KERN}/clients/{kennung}/CLIENT_PACK.md"
        text = read(os.path.join(pdir, "CLIENT_PACK.md"))
        abschnitt = _abschnitt(text, AUSKUNFT_UEBERSCHRIFT)
        if abschnitt is None:
            err(f"{rel}: Abschnitt '{AUSKUNFT_UEBERSCHRIFT}' fehlt. Jedes Pack fuehrt die "
                f"bekannten Quellen ausserhalb des Repositoriums - Regeltexte, Skills, "
                f"Agentenprofile, Berechtigungen, Hooks - oder einen datierten "
                f"Abwesenheitsbeleg (D-34, D-37)")
            continue
        zeilen = [z for z in abschnitt.splitlines()
                  if z.strip().startswith("|") and not re.match(r"^\|[\s:|-]+\|?$", z.strip())]
        inhalt = [z for z in zeilen
                  if not re.search(r"\|\s*(Quelle|Ladebedingung|Wirkung)\s*\|", z)]
        abwesend = re.search(r"keine bekannt", abschnitt, re.I)
        if not inhalt and not abwesend:
            err(f"{rel}: Abschnitt '{AUSKUNFT_UEBERSCHRIFT}' ist leer. Er braucht je "
                f"bekannter Quelle eine Zeile oder die ausdrueckliche Angabe 'keine "
                f"bekannt' mit Datum und Erhebungsweg - ein leerer Abschnitt ist kein "
                f"Abwesenheitsbeleg")
            continue
        if kennung.startswith("_"):
            continue  # Vorlage: Erhebungsstand steht als <TBD>
        if not DATUM_RE.search(abschnitt):
            err(f"{rel}: Abschnitt '{AUSKUNFT_UEBERSCHRIFT}' nennt keinen Erhebungsstand "
                f"(JJJJ-MM-TT). Eine Quellenliste ohne Datum ist keine Auskunft, sondern "
                f"eine Behauptung mit Fussnote")


# Begriff der Dokumenttabellen -> Platzhalter des Manifests. Ein Begriff ohne Eintrag
# bleibt unbeanstandet: "Nutzerlokale Ueberschreibung" hat kein Manifestfeld und ist
# zugleich die Gegenprobe dieser Pruefung.
GLOSSAR_ZU_PLATZHALTER = {
    "Wurzel-Anweisungsdatei": "<ROOT_INSTRUCTION_FILE>",
    "Laufzeitschicht": "<RUNTIME_DIR>",
    "Berechtigungsdatei": "<PERMISSIONS_FILE>",
    "Regelablage": "<RULES_DIR>",
    "Skill-Ablage": "<SKILLS_DIR>",
    "Agentenprofile": "<AGENTS_DIR>",
    "Hook-Konfiguration": "<HOOKS_FILE>",
    "MCP-Konfiguration": "<MCP_FILE>",
}
# <CORE_DIR> ist keine Eigenschaft eines Clients, sondern dieser Installation; ein Pack
# darf ihn nicht belegen (PLACEHOLDER_REGISTRY.md).
PLATZHALTER_OHNE_PACK = ("<CORE_DIR>",)


def _tabellenzeilen(text: str):
    for zeile in text.splitlines():
        z = zeile.strip()
        if not z.startswith("|") or re.match(r"^\|[\s:|-]+\|?$", z):
            continue
        yield tabellenzellen(z)


def _spalten_je_pack(felder: list[str], packs: list[str]) -> dict[str, int]:
    zuordnung: dict[str, int] = {}
    for i, feld in enumerate(felder):
        nackt = feld.strip("`* ")
        if nackt in packs:
            zuordnung[nackt] = i
    return zuordnung


def _wert_passt(zelle: str, erwartet: str) -> bool:
    """Der Manifestwert steht in der Zelle - Schreibvarianten zugelassen.

    Die Tabellen schreiben ein Verzeichnis mal mit und mal ohne abschliessenden
    Schraegstrich und setzen den Wert gelegentlich in einen erklaerenden Satz. Geprueft
    wird deshalb Enthaltensein, nicht Gleichheit: Diese Pruefung soll eine **abweichende**
    Angabe finden, nicht eine anders formulierte.
    """
    zelle = zelle.replace("\\", "/")
    kandidaten = {erwartet, erwartet.rstrip("/") + "/", erwartet.rstrip("/")}
    return any(k and k in zelle for k in kandidaten)


def check_dokumenttabellen(root: str) -> None:
    """Pruefung 20 (CR-2026-036): Dokumenttabellen und Manifest sagen dasselbe.

    GRENZE: Sie prueft **Uebereinstimmung, nicht Richtigkeit.** Steht im Manifest ein
    falscher Pfad, sind Tabelle und Manifest danach einig - und beide falsch. Was den
    Manifestwert prueft, ist die Installation selbst und der Nachweis an ihr (D-23).
    Abgedeckt sind nur Zeilen mit Manifestentsprechung; Begriffe ohne Feld altern weiter
    still.
    """
    packs = {k: m for k, _p, m in _client_packs(root) if m}
    if not packs:
        return
    namen = sorted(packs)

    registry = f"{KERN}/docs/PLACEHOLDER_REGISTRY.md"
    pfad = os.path.join(root, *registry.split("/"))
    if os.path.isfile(pfad):
        text = read(pfad)
        spalten: dict[str, int] = {}
        for felder in _tabellenzeilen(text):
            gefunden = _spalten_je_pack(felder, namen)
            if gefunden:
                spalten = gefunden
                continue
            platzhalter = felder[0].strip("`* ")
            if not spalten or not platzhalter.startswith("<"):
                continue
            if platzhalter in PLATZHALTER_OHNE_PACK:
                continue
            for pack, i in spalten.items():
                erwartet = (packs[pack].get("runtime_placeholders") or {}).get(platzhalter)
                if erwartet is None or i >= len(felder):
                    continue
                if not _wert_passt(felder[i].strip("`* "), erwartet):
                    err(f"{registry}: {platzhalter} steht fuer '{pack}' als "
                        f"'{felder[i]}', das Manifest fuehrt '{erwartet}'. Die "
                        f"maschinenlesbare Quelle gilt; die Tabelle wird nachgezogen")

    glossar = f"{KERN}/docs/RUNTIME_GLOSSARY.md"
    pfad = os.path.join(root, *glossar.split("/"))
    if os.path.isfile(pfad):
        text = read(pfad)
        spalten = {}
        for felder in _tabellenzeilen(text):
            gefunden = _spalten_je_pack(felder, namen)
            if gefunden:
                spalten = gefunden
                continue
            if not spalten:
                continue
            begriff = felder[0].strip("`* ")
            platzhalter = GLOSSAR_ZU_PLATZHALTER.get(begriff)
            if not platzhalter:
                continue  # Begriff ohne Manifestfeld - siehe Kommentar oben
            for pack, i in spalten.items():
                erwartet = (packs[pack].get("runtime_placeholders") or {}).get(platzhalter)
                if erwartet is None or i >= len(felder):
                    continue
                if not _wert_passt(felder[i], erwartet):
                    err(f"{glossar}: '{begriff}' steht fuer '{pack}' als '{felder[i]}', "
                        f"das Manifest fuehrt '{erwartet}'. Die maschinenlesbare Quelle "
                        f"gilt; die Tabelle wird nachgezogen")


PFAD_HERLEITUNG_RE = re.compile(r"os\.path\.join|os\.environ|os\.getenv")


def check_hook_skripte_neutral(root: str) -> None:
    """Pruefung 21 (D-30, CR-2026-037): Hook-Skripte raten die Laufzeitschicht nicht.

    Ein Skript, das in einer Sitzung laeuft, bekommt Projektverzeichnis und Regelablage
    aus der Semantikabbildung seines Client Packs - es leitet sie nicht aus einem
    clientgebundenen Namen ab. Gemeldet wird deshalb zweierlei: die Umgebungsvariable
    eines Packs (hook_project_dir_var) an jeder Stelle, und ein Laufzeitpfad eines Packs
    dort, wo ein Pfad gebaut oder aus der Umgebung gelesen wird.

    GRENZE - und zugleich die Gegenprobe: Die **Schutzmuster** von hook-check-secrets.py
    nennen die Laufzeitpfade beider Packs ausdruecklich. Das ist Absicht (ein zusaetzlich
    geschuetzter Pfad ist eine Verschaerfung) und bleibt unbeanstandet, weil dort kein
    Pfad hergeleitet wird. Ausgenommen ist ferner der Validator selbst: Er fuehrt eine
    dokumentierte Rueckfallabbildung, wenn kein Pack gefunden wird (CR-2026-037 E3).

    Die Pruefung sieht Skripte, nicht Wirkung. Ein Hook mit sauber uebergebenen Pfaden,
    der trotzdem den falschen Status meldet, faellt ihr nicht auf.
    """
    variablen: dict[str, str] = {}
    pfade: dict[str, str] = {}
    for kennung, _pdir, man in _client_packs(root):
        if not man:
            continue
        v = man.get("hook_project_dir_var")
        if v:
            variablen[v] = kennung
        for schluessel in ("<RUNTIME_DIR>", "<RULES_DIR>", "<SKILLS_DIR>", "<AGENTS_DIR>",
                           "<PERMISSIONS_FILE>", "<HOOKS_FILE>", "<MCP_FILE>"):
            wert = (man.get("runtime_placeholders") or {}).get(schluessel)
            if wert:
                pfade[wert] = kennung
    sdir = os.path.join(root, KERN, "tests", "scripts")
    if not os.path.isdir(sdir):
        return
    for name in sorted(os.listdir(sdir)):
        if not name.startswith("hook-") or not name.endswith(".py"):
            continue
        rel = f"{KERN}/tests/scripts/{name}"
        for i, zeile in enumerate(read(os.path.join(sdir, name)).splitlines(), 1):
            ohne_kommentar = zeile.split("#", 1)[0]
            for variable, kennung in variablen.items():
                if variable in ohne_kommentar:
                    err(f"{rel}:{i}: '{variable}' ist die Umgebungsvariable des Packs "
                        f"'{kennung}'. Ein Hook-Skript des Kerns nennt sie nicht - der "
                        f"Wert kommt als Argument aus der Semantikabbildung (D-30)")
            if not PFAD_HERLEITUNG_RE.search(ohne_kommentar):
                continue
            for wert, kennung in sorted(pfade.items()):
                if re.search(r"['\"]%s['\"/]" % re.escape(wert), ohne_kommentar) or \
                        re.search(r"['\"]%s['\"]" % re.escape(wert.split("/")[0]),
                                  ohne_kommentar):
                    err(f"{rel}:{i}: Hier wird ein Pfad aus '{wert}' gebaut - der "
                        f"Laufzeitschicht des Packs '{kennung}'. Ein Skript des Kerns "
                        f"kennt sie nicht; sie kommt als Argument (D-30)")
                    break


def check_importsteuerung(root: str, man: dict) -> None:
    """Pruefung 22 (D-37): Die Importsteuerung steht so, wie das Manifest sie abbildet.

    GRENZE - vorab benannt wie bei Pruefung 19: Sie belegt **Anwesenheit und
    Uebereinstimmung, nicht Richtigkeit und erst recht nicht Wirkung.** Dass die
    Einstellung in der Datei steht, heisst nicht, dass sie greift: Die Benutzer-
    konfiguration dieser Arbeitsstation hat Vorrang, in beide Richtungen gemessen
    (K-27). Die Masznahme ist ein Standard, keine Schranke. Was wirkt, misst nur eine
    Sitzung, die den Kontext prueft - nicht das Register des Clients (ERH-02).

    Ein Pack ohne das Feld laeuft durch: Kennt ein Client keinen solchen Mechanismus -
    oder liefert das Framework bewusst keine Vorgabe aus, wie bei claude-code -, bleibt
    es bei der Auskunft im Client Pack (CR-2026-038 E2).
    """
    steuerung = man.get("import_control")
    rechte = man.get("permissions_file")
    if not rechte:
        return
    pfad = os.path.join(root, *rechte.split("/"))
    if not os.path.isfile(pfad):
        return
    try:
        installiert = json.loads(read(pfad))
    except Exception:
        return  # ungueltiges JSON meldet Pruefung 2
    if not steuerung:
        return
    schluessel = steuerung.get("key")
    erwartet = steuerung.get("value")
    if not schluessel:
        err(f"{man.get('client', '?')}/manifest.json: import_control ohne 'key'")
        return
    ist = installiert.get(schluessel)
    if ist is None:
        err(f"{rechte}: Die Importsteuerung '{schluessel}' fehlt. Das Manifest des Packs "
            f"'{man.get('client', '?')}' bildet sie ab (D-37): Das Framework importiert "
            f"keine Regel- und Skillquellen fremder Werkzeugformate. Eine Installation, "
            f"die sie verliert, laedt sie wieder - still")
        return
    if ist != erwartet:
        err(f"{rechte}: Die Importsteuerung '{schluessel}' steht als {json.dumps(ist, ensure_ascii=False)}, "
            f"das Manifest bildet {json.dumps(erwartet, ensure_ascii=False)} ab. Die "
            f"maschinenlesbare Quelle gilt (D-37)")


# Normative Schluesselwoerter. Ein Kommentar traegt Herkunft - Ebene, Version, Owner,
# Ladeverhalten -, keine Anweisung: Er erreicht nicht jede Sitzung (ERH-01, K-28, D-38).
NORMATIVE_WOERTER = (
    re.compile(r"\bMUSS\b"),
    re.compile(r"\bMUESSEN\b"),
    re.compile(r"\bDARF NICHT\b"),
    re.compile(r"\bDUERFEN NICHT\b"),
    re.compile(r"\bSOLL\b"),
    re.compile(r"\bNICHT ZULAESSIG\b"),
    re.compile(r"(?i)nur über den änderungsprozess"),
    re.compile(r"(?i)darf nur über"),
)
HTML_KOMMENTAR_RE = re.compile(r"<!--(.*?)-->", re.S)


def _laufzeitartefakte(root: str, man: dict):
    """Die Artefakte, die in einer Sitzung geladen werden - Quelle und Installation."""
    for unterbau in (f"{KERN}/framework/runtime", f"{KERN}/templates/rules"):
        basis = os.path.join(root, *unterbau.split("/"))
        if os.path.isdir(basis):
            for pfad in _walk_text_files(basis):
                if pfad.endswith((".md", ".template")):
                    yield pfad
    orte = [man.get("root_instruction_file"),
            (man.get("runtime_placeholders") or {}).get("<RULES_DIR>")]
    for ort in orte:
        if not ort:
            continue
        ziel = os.path.join(root, *ort.split("/"))
        if os.path.isfile(ziel):
            yield ziel
        elif os.path.isdir(ziel):
            for pfad in _walk_text_files(ziel):
                if pfad.endswith((".md", ".template")):
                    yield pfad


def check_normative_kommentare(root: str, man: dict) -> None:
    """Pruefung 23 (D-38): Kein normatives Schluesselwort in einem HTML-Kommentar.

    Gemessen an **beiden** Clients, mit entgegengesetztem Ergebnis. Bei 'claude-code' blieb
    dieselbe Messmarke unsichtbar, solange sie in Kommentarklammern stand, und war im
    Klartext sofort im Kontext - in der Wurzel-Anweisungsdatei und in der Regelablage
    (2026-09-11, ERH-01). Bei 'devin-desktop' steht der Kommentar **woertlich** in dem
    Regelblock, den der Client bildet; die Sitzung gab die Marke aus dem Kommentar zurueck,
    ohne eine Datei zu lesen (2026-09-12, K-28).

    Genau das traegt die Pruefung. Ein Ablageort, an dem eine Aussage bei dem einen Client
    verschwindet und beim anderen mitlaeuft, ist fuer eine normative Aussage untauglich:
    Was gilt, darf nicht davon abhaengen, mit welchem Werkzeug gearbeitet wird. Die
    Begruendung ist damit belastbarer als vorher - die alte ('erreicht die Sitzung nicht')
    waere mit einem Client, der Kommentare durchreicht, hinfaellig gewesen; genau so einer
    ist gemessen worden. Was gilt, steht im Fliesstext.

    GRENZE: Eine Wortlistenpruefung meldet auch eine zutreffende Erwaehnung - etwa den
    Verweis auf eine Regel, die 'MUSS' enthaelt. Fehlalarme sind moeglich und beim
    Beschluss ausdruecklich in Kauf genommen (CR-2026-039 E3). Die strengere Lesart gilt
    fuer beide Packs - nicht mehr vorsorglich, weil das Verhalten des zweiten unerhoben
    waere, sondern weil es erhoben ist und **abweicht** (K-28, CR-2026-040).
    """
    gesehen = set()
    for pfad in _laufzeitartefakte(root, man):
        if pfad in gesehen:
            continue
        gesehen.add(pfad)
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        text = read(pfad)
        for m in HTML_KOMMENTAR_RE.finditer(text):
            inhalt = m.group(1)
            zeile = text.count("\n", 0, m.start()) + 1
            for muster in NORMATIVE_WOERTER:
                treffer = muster.search(inhalt)
                if not treffer:
                    continue
                err(f"{rel}:{zeile}: '{treffer.group(0)}' steht in einem HTML-Kommentar. "
                    f"Ein Kommentar erreicht nicht jede Sitzung (ERH-01, K-28); eine normative "
                    f"Aussage gehoert in den Fliesstext, im Kommentar bleibt die Herkunft "
                    f"(D-38)")
                break


# Was in der Vorlage einer Regelablage liegen darf: Regeltexte nach dem Nummernschema
# und Vorlagen. Alles andere ist ein Nicht-Regeltext - der Client registriert, was in
# der Ablage liegt, und macht es damit ladbar (AP2-DD-17, K-26).
REGELDATEI_RE = re.compile(r"^\d[\dN]-[A-Za-z0-9._-]+\.md(\.template)?$")


def check_regelablage_sauber(root: str) -> None:
    """Pruefung 24 (D-36): In der Vorlage der Regelablage liegt nur, was Regel ist.

    Bis 0.25.0 lag dort je Pack eine erklaerende README. Bei einem Pack fuehrte der
    Client sie als Regel mit Trigger 'manual' (AP2-DD-17), beim anderen stand sie sogar
    unbedingt im Kontext (K-26) - mit Belegvorbehalten, die damit den Rang eines
    Regeltexts trugen. Der erklaerende Text steht seither eine Ebene hoeher, in der
    Laufzeit-README.

    GRENZE: Geprueft wird die **Vorlage** des Packs, nicht die installierte Ablage. Was
    ein Projekt dort selbst ablegt, sieht diese Pruefung nicht.
    """
    for kennung, pdir, man in _client_packs(root):
        if not man:
            continue
        regelablage = (man.get("runtime_placeholders") or {}).get("<RULES_DIR>")
        if not regelablage:
            continue
        basis = os.path.join(pdir, "root-template", *regelablage.split("/"))
        if not os.path.isdir(basis):
            continue
        for name in sorted(os.listdir(basis)):
            if os.path.isdir(os.path.join(basis, name)):
                err(f"{KERN}/clients/{kennung}/root-template/{regelablage}/{name}: "
                    f"Unterverzeichnis in der Vorlage der Regelablage")
                continue
            if REGELDATEI_RE.match(name):
                continue
            err(f"{KERN}/clients/{kennung}/root-template/{regelablage}/{name}: kein "
                f"Regeltext. Die Regelablage enthaelt ausschliesslich Regeln (D-36) - "
                f"der Client registriert, was dort liegt, und macht es ladbar. "
                f"Erklaerender Text gehoert in die Laufzeit-README eine Ebene hoeher")


def check_mermaid(root: str) -> None:
    mmdc = shutil.which("mmdc")
    if not mmdc:
        warn("mmdc nicht installiert – Mermaid-Syntaxprüfung übersprungen")
        return
    for path in iter_text_files(root):
        if not path.endswith(".md"):
            continue
        text = read(path)
        for i, block in enumerate(MERMAID_RE.findall(text), 1):
            with tempfile.TemporaryDirectory() as td:
                src = os.path.join(td, "d.mmd")
                out = os.path.join(td, "d.svg")
                with open(src, "w", encoding="utf-8") as fh:
                    fh.write(block)
                res = subprocess.run([mmdc, "-i", src, "-o", out, "-q"], capture_output=True, text=True)
                if res.returncode != 0:
                    # Die Fehlerausgabe des Renderers zitiert den Quelltext des Blocks. Sie
                    # hier auszugeben traegt Diagramminhalt in Terminal und Protokoll - genau
                    # der Fehler, den B03 fuer die Inhaltsdiagnosen beanstandet (D-39). Der
                    # Block bleibt ueber Datei und Nummer auffindbar; wer die Meldung des
                    # Renderers braucht, ruft ihn von Hand auf.
                    err(f"{os.path.relpath(path, root)}: Mermaid-Block {i} ungültig "
                        f"(Renderer-Exitcode {res.returncode}; Fehlerausgabe nicht wiedergegeben)")


# Pruefung 25: Eine Zeile auf [NICHT ABBILDBAR] nennt den Ersatz.
#
# Die Einstufungsklasse sagt "der Client bietet keinen Mechanismus". Sie sagt nicht, was an
# seine Stelle tritt - und genau dort entsteht die stillschweigende Verschlechterung: Ein
# Ausfall wird eingetragen, niemand widerspricht, und die Zusage ist weg, ohne dass eine
# Entscheidung darueber gefallen waere.
#
# D-41 unterscheidet deshalb Kernzusagen von Faehigkeitszusagen. Eine Kernzusage auf
# [NICHT ABBILDBAR] sperrt die Inbetriebnahme; eine Faehigkeitszusage sperrt nicht, MUSS aber
# den Ersatz benennen. Diese Pruefung setzt den zweiten Teil durch - den ersten kann kein
# Skript durchsetzen, er ist eine Freigabe durch einen Menschen.
NICHT_ABBILDBAR_RE = re.compile(r"`\[NICHT ABBILDBAR\]`")
MATRIXZEILE_RE = re.compile(r"^\|\s*([A-Z]{1,2}\d+)\s*\|")


def check_ausfall_mit_ersatz(root: str) -> None:
    """Pruefung 25 (D-41): Kein Ausfall ohne benannten Ersatz.

    Geprueft werden die Matrixzeilen der Client Packs - erkennbar an der Zeilenkennung am
    Zeilenanfang (B3, S5, X2). Die Zusammenfassungstabellen desselben Dokuments fuehren
    dieselbe Klasse als Zeilenbeschriftung; sie sind keine Zusagen und bleiben unberuehrt.

    Verlangt wird das Wort 'Ersatz' in der Zeile. Das ist bewusst grob: Die Pruefung kann
    nicht beurteilen, ob ein Ersatz taugt - sie kann nur erzwingen, dass jemand die Frage
    gestellt und beantwortet hat. Ein 'kein Ersatz' genuegt ihr, und das ist richtig so:
    Der Satz 'hierfuer gibt es keinen Ersatz' ist eine Aussage, die jemand verantwortet.

    GRENZE: Eine Wortpruefung. Wer 'Ersatz' hinschreibt, ohne einen zu nennen, kommt durch.
    Sie faengt das Vergessen, nicht die Absicht - wie Pruefung 23 (CR-2026-041 E3).
    """
    basis = os.path.join(root, KERN, "clients")
    if not os.path.isdir(basis):
        return
    for pack in sorted(os.listdir(basis)):
        if pack.startswith("_"):
            continue
        pfad = os.path.join(basis, pack, "CLIENT_PACK.md")
        if not os.path.isfile(pfad):
            continue
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        for i, zeile in enumerate(read(pfad).splitlines(), 1):
            if not NICHT_ABBILDBAR_RE.search(zeile):
                continue
            m = MATRIXZEILE_RE.match(zeile)
            if not m:
                continue
            if "ersatz" in zeile.lower():
                continue
            err(f"{rel}:{i}: Zeile {m.group(1)} steht auf [NICHT ABBILDBAR], ohne einen "
                f"Ersatz zu benennen. Ein Ausfall, der nur eingetragen und nicht ersetzt "
                f"wird, ist eine stillschweigende Verschlechterung: Die Zeile nennt den "
                f"Ersatz oder haelt fest, dass es keinen gibt (D-41)")


# Pruefung 26: Eine erklaerte Werkzeugabwesenheit muss belegt und folgerichtig sein.
#
# Seit CR-2026-047 darf ein Pack im Feld hook_tools_absent erklaeren, dass sein Client
# eine Werkzeugklasse gar nicht kennt; die Abbildung laesst den Hook-Matcher dann ohne
# diese Klasse durchlaufen, statt abzubrechen. Das ist noetig - ein Client ohne eigenes
# Suchwerkzeug kann keines abbilden - und es ist zugleich ein Schlupfloch: Wer 'write'
# dort eintraege, naehme das schreibende Werkzeug aus der Durchsetzung, und nichts
# meldete es.
#
# Diese Pruefung schliesst es an zwei Stellen:
#   1. Die Abwesenheit muss folgerichtig sein - ein Verb, das hier steht, muss auch in
#      permission_tools leer sein. Ein Client, fuer den die Berechtigungsschicht ein
#      Werkzeug dieser Klasse kennt, hat eines.
#   2. Die Abwesenheit muss erklaert sein - ein nicht leerer Begleitsatz. Dieselbe
#      Begruendung wie bei Pruefung 25: Ein Ausfall, den jemand verantwortet, ist etwas
#      anderes als einer, der eingetragen wurde.
#
# GRENZE: Die Pruefung belegt nicht, dass der Client das Werkzeug wirklich nicht hat -
# das kann nur eine Erhebung. Sie belegt, dass die beiden Felder, die es behaupten,
# einander nicht widersprechen und dass jemand den Satz dazu geschrieben hat.
def check_werkzeugabwesenheit(root: str) -> None:
    """Pruefung 26 (D-47): hook_tools_absent ist folgerichtig und erklaert."""
    basis = os.path.join(root, KERN, "clients")
    if not os.path.isdir(basis):
        return
    for pack in sorted(os.listdir(basis)):
        if pack.startswith("_"):
            continue
        pfad = os.path.join(basis, pack, "manifest.json")
        if not os.path.isfile(pfad):
            continue
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        try:
            man = json.loads(read(pfad))
        except ValueError:
            continue
        abwesend = man.get("hook_tools_absent") or []
        if not abwesend:
            continue
        if not isinstance(abwesend, list):
            err(f"{rel}: hook_tools_absent ist keine Liste")
            continue
        notiz = str(man.get("_hook_tools_absent_note") or "").strip()
        if not notiz:
            err(f"{rel}: hook_tools_absent nennt {sorted(abwesend)}, aber "
                f"_hook_tools_absent_note fehlt oder ist leer. Eine Werkzeugklasse aus "
                f"der Durchsetzung zu nehmen, ist eine Aussage ueber den Client - sie "
                f"gehoert begruendet, nicht bloss eingetragen (D-47)")
        werkzeuge = man.get("permission_tools") or {}
        for verb in sorted(abwesend):
            if werkzeuge.get(verb):
                err(f"{rel}: hook_tools_absent erklaert das Verb '{verb}' fuer abwesend, "
                    f"permission_tools nennt dafuer aber {werkzeuge[verb]}. Beides "
                    f"zugleich geht nicht: Kennt die Berechtigungsschicht ein Werkzeug "
                    f"dieser Klasse, hat der Client eines, und der Hook muss es "
                    f"erreichen (D-47)")


# Pruefung 27: Ein verworfenes Zusagenfeld eines Skills nennt seinen Ersatz.
#
# Dieselbe Bauform wie Pruefung 26, eine Ebene weiter: Ein Pack darf ein Frontmatter-Feld
# verwerfen, das sein Client nicht kennt - aber nicht eines, das eine Zusage traegt, ohne
# zu sagen, was an seine Stelle tritt.
#
# Zwei Faelle gab es dafuer schon: 'triggers' verfiel beim Rendern, bis AP2-CC-01 es fand
# und eine Abbildung bekam (model_invocation_field). 'permissions' verfiel bis 0.30.0 auf
# genau dieselbe Weise - im Manifest unter drop_fields deklariert, in der Wirkung
# unbemerkt, und dabei trug es das 'deny: edit, exec' von zwoelf Skills (B01, D-50).
#
# install.py bricht seit 0.31.0 ab, wenn das passiert. Diese Pruefung findet denselben
# Fehler **ohne** Installation - im Repositorium, wo ein neues Pack entsteht.
#
# GRENZE: Eine Anwesenheitspruefung auf den Begleitsatz. Ob der genannte Ersatz taugt,
# kann kein Skript beurteilen - wie bei Pruefung 25 wird erzwungen, dass jemand die Frage
# gestellt und beantwortet hat.
ZUSAGENFELDER_ERSATZ = {
    "permissions": "skill_permissions_ersatz",
    "triggers": "model_invocation_field",
}


def check_zusagenfelder(root: str) -> None:
    """Pruefung 27 (D-50): Kein verworfenes Zusagenfeld ohne benannten Ersatz."""
    basis = os.path.join(root, KERN, "clients")
    if not os.path.isdir(basis):
        return
    for pack in sorted(os.listdir(basis)):
        if pack.startswith("_"):
            continue
        pfad = os.path.join(basis, pack, "manifest.json")
        if not os.path.isfile(pfad):
            continue
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        try:
            man = json.loads(read(pfad))
        except ValueError:
            continue
        fmt = (man.get("skill_frontmatter") or {})
        entfallend = set(fmt.get("drop_fields") or [])
        if fmt.get("tools_format") == "csv":
            entfallend.add("allowed-tools")
        for feld, ersatzfeld in sorted(ZUSAGENFELDER_ERSATZ.items()):
            if feld not in entfallend:
                continue
            if str(fmt.get(ersatzfeld) or "").strip():
                continue
            err(f"{rel}: Das Skill-Frontmatter-Feld '{feld}' traegt eine Zusage und steht "
                f"in skill_frontmatter.drop_fields - es entfaellt damit ersatzlos. Das Pack "
                f"MUSS in skill_frontmatter.{ersatzfeld} benennen, was an seine Stelle "
                f"tritt, oder festhalten, dass es keinen Ersatz gibt und was stattdessen "
                f"traegt. Ein folgenlos verworfenes Feld ist der Befund AP2-CC-01, und bei "
                f"'permissions' war es B01 (D-18, D-50)")


# Pruefung 28: Ein Strukturpfad des Frameworks gehoert nicht in <EXCLUDED_PATHS>.
#
# Zwei Schutzziele, zwei Kategorien - der Schutz-Hook unterscheidet sie seit D-30 und die
# Berechtigungsdatei ebenfalls: <EXCLUDED_PATHS> wird dort zu einer 'read'- UND einer
# 'write'-Verweigerung, die Strukturpfade stehen ausschliesslich als 'write'-Verweigerung
# bei 'read allow **'. Die Overlay-Vorlage und die Laufzeitregel fuehrten sie bis 0.31.0
# unter "weder lesen noch aendern" - genau die Pfade, die der KI-Client als
# Anweisungsquelle laden soll (B07). Wer die Vorlage woertlich ausfuellt, erzeugt damit
# eine Lesesperre auf die eigenen Regeldateien. Diese Pruefung findet den Fall im
# Repositorium, also bevor eine Installation entsteht (D-55).
STRUKTURPFAD_MARKER = (
    "<RUNTIME_DIR>", "<ROOT_INSTRUCTION_FILE>", "<CORE_DIR>", "<RULES_DIR>",
    "project-overlay/", "framework/", "AGENTS.md", "CLAUDE.md", ".devin/", ".claude/",
)

# Die Beschriftung der Deklarationszeile - in der Overlay-Vorlage eine Tabellenzeile, in
# der Laufzeitregel ein Listeneintrag. Beide beginnen mit derselben Bezeichnung.
DEKLARATION_RE = re.compile(r"^\s*(?:\|\s*|-\s+)Ausgeschlossene Pfade")


def _excluded_paths_traeger(root: str, man: dict) -> list[str]:
    """Dateien, die <EXCLUDED_PATHS> deklarieren - Quelle und Installation."""
    kandidaten = [
        os.path.join(KERN, "templates", "project-overlay", "OVERLAY.md"),
        os.path.join(KERN, "framework", "runtime", "rules", "20-project-overlay.md"),
        os.path.join("project-overlay", "OVERLAY.md"),
    ]
    runtime_dir = (man or {}).get("runtime_dir")
    if runtime_dir:
        kandidaten.append(os.path.join(runtime_dir.replace("/", os.sep), "rules",
                                       "20-project-overlay.md"))
    treffer = []
    for rel in kandidaten:
        pfad = os.path.join(root, rel)
        if os.path.isfile(pfad) and pfad not in treffer:
            treffer.append(pfad)
    return treffer


def check_excluded_paths(root: str, man: dict) -> None:
    """Pruefung 28 (D-55): Ein Schreibschutz ist kein Leseverbot.

    Geprueft wird die **Deklarationszeile** von <EXCLUDED_PATHS>: Sie darf keinen
    Strukturpfad des Frameworks nennen. Der Nachweis ist eine Textpruefung - dass die
    Berechtigungsdatei die beiden Kategorien trennt, prueft Pruefung 2.

    Nur die Deklaration, nicht jede Nennung: Beide Traeger erklaeren im Fliesstext
    ausdruecklich, dass die Strukturpfade **nicht** hierher gehoeren, und diese Saetze
    nennen beides in einer Zeile. Eine Pruefung, die jede Nennung meldet, wuerde genau
    den richtigen Text beanstanden. Erkannt wird die Deklaration an ihrer Beschriftung
    (DEKLARATION_RE) - und weil eine verlorene Beschriftung eine Pruefung erzeugt, die
    leise besteht, ist auch ihr Fehlen ein Fehler (D-23).
    """
    for pfad in _excluded_paths_traeger(root, man):
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        zeilen = read(pfad).splitlines()
        deklarationen = [(i, z) for i, z in enumerate(zeilen, 1)
                         if "<EXCLUDED_PATHS>" in z and DEKLARATION_RE.match(z)]
        if not deklarationen and any("<EXCLUDED_PATHS>" in z for z in zeilen):
            err(f"{rel}: nennt <EXCLUDED_PATHS>, aber keine Zeile ist als Deklaration "
                f"erkennbar (Beschriftung 'Ausgeschlossene Pfade'). Pruefung 28 prueft "
                f"damit nichts und bestuende leise - die Beschriftung ist Teil des "
                f"Nachweises (D-23, D-55)")
        for i, zeile in deklarationen:
            gefunden = [m for m in STRUKTURPFAD_MARKER if m in zeile]
            if not gefunden:
                continue
            err(f"{rel}:{i}: Die Deklaration von <EXCLUDED_PATHS> nennt "
                f"{', '.join(gefunden)}. <EXCLUDED_PATHS> wird in der Berechtigungsdatei zu "
                f"einer 'read'- UND einer 'write'-Verweigerung; die Strukturpfade des "
                f"Frameworks sind integritaetsgeschuetzt, nicht vertraulich - sie gehoeren "
                f"in <READ_ONLY_PATHS>. Ein Projekt, das dieser Zeile folgt, sperrt den "
                f"Lesezugriff auf seine eigenen Regeldateien; der KI-Client kann die "
                f"Anweisungen dann nicht laden, die er befolgen soll (B07, D-55)")


# Pruefung 29: Kurzform und Langform fuehren dieselben K3-Kategorien, unbedingt.
#
# Die Kategorien aus Abschnitt 2.1 sind ebenenfest (D-52). Zwei Fehlerbilder sind moeglich
# und beide sind vorgekommen: eine Kategorie fehlt in einer Fassung - die Kurzform, die in
# jede Sitzung laedt, fuehrte bis 0.31.0 nur sechs von acht -, oder eine Kategorie traegt
# eine Bedingung, wie die interne Adresse, die "sofern nicht im Overlay als K1 eingestuft"
# ausgenommen war. Beides prueft diese Funktion an denselben fuenf Traegern.
K3_KATEGORIEN = (
    ("Secrets und Zugangsdaten", r"Secret|Zugangsdaten"),
    ("personenbezogene Echtdaten", r"personenbezogene Echtdaten"),
    ("Produktionsdaten", r"Produktionsdaten"),
    ("Kunden- und Behördendokumente", r"Behörden"),
    ("Sicherheitskonfigurationen", r"Sicherheitskonfiguration"),
    ("interne Adressen und Umgebungskennungen", r"interne[nr]? Adressen"),
    ("als vertraulich eingestufte Inhalte", r"vertraulich"),
    ("Inhalte anderer Projekte", r"anderer Projekte|anderen Projekten|Fremdprojekte"),
)

# Eine Bedingung in einer unbedingten Liste. "es sei denn" stand in Abschnitt 2.2.
K3_BEDINGUNG_RE = re.compile(
    r"sofern nicht|sofern es nicht|es sei denn|außer wenn|soweit nicht|sofern kein", re.I)

# Je Traeger: Pfad, Startanker, Endanker (None = bis Zeilenende des Startankers).
K3_TRAEGER = (
    (KERN + "/framework/core/02-privacy.md", "### 2.1 Immer K3", "### 2.2"),
    (KERN + "/framework/runtime/root-instruction.md", "- Immer K3", None),
    (KERN + "/framework/runtime/rules/10-privacy-security.md", "| K3 |", None),
    (KERN + "/decision-trees/01-context-allowed.md", "1. **K3-Prüfung:**", "\n2. "),
    (KERN + "/checklists/02-privacy-context.md", "K3-Kategorien geprüft", None),
)


def check_k3_kategorien(root: str) -> None:
    """Pruefung 29 (D-52): Dieselbe K3-Liste in jeder Fassung, ohne Bedingung.

    Belegt Uebereinstimmung der Kategorien, nicht die Gleichheit der Formulierungen - eine
    Kurzform darf kuerzer sein, aber keine Kategorie weglassen und keine an eine Bedingung
    binden. Was die Pruefung nicht leistet: Sie sieht nicht, ob ein KI-Client die Liste
    auch anwendet. Das ist FW-KO-05 und laeuft als Sitzung (leitwerk-core/tests/EDGE_CASES.md).
    """
    for rel, start, ende in K3_TRAEGER:
        pfad = os.path.join(root, rel.replace("/", os.sep))
        if not os.path.isfile(pfad):
            err(f"{rel}: fehlt - diese Datei fuehrt die K3-Kategorien und wird gegen die "
                f"uebrigen Fassungen geprueft (D-52)")
            continue
        text = read(pfad).replace("\r\n", "\n")
        pos = text.find(start)
        if pos < 0:
            err(f"{rel}: Der Anker '{start}' ist nicht mehr auffindbar. Ohne ihn prueft "
                f"diese Pruefung nichts - sie wuerde leise bestehen (D-23)")
            continue
        if ende:
            bis = text.find(ende, pos + len(start))
            bereich = text[pos:bis if bis > 0 else len(text)]
        else:
            bis = text.find("\n", pos)
            bereich = text[pos:bis if bis > 0 else len(text)]
        for name, muster in K3_KATEGORIEN:
            if not re.search(muster, bereich):
                err(f"{rel}: Die K3-Liste nennt die Kategorie '{name}' nicht. Alle acht "
                    f"Kategorien aus Abschnitt 2.1 von "
                    f"{KERN}/framework/core/02-privacy.md gelten in jeder Fassung; eine "
                    f"Kurzform darf kuerzer formulieren, aber keine Kategorie weglassen "
                    f"(D-52)")
        m = K3_BEDINGUNG_RE.search(bereich)
        if m:
            err(f"{rel}: Die K3-Liste traegt eine Bedingung ('{m.group(0)}'). Die "
                f"Kategorien sind unbedingt und ebenenfest - kein Overlay, keine "
                f"Datenschutzpruefung und kein Ausnahmeprozess kann sie freigeben "
                f"(governance/PRIORITY_HIERARCHY.md Regel 2.4, D-52)")


# Pruefung 30: Die Grenzfalltabelle ist vollstaendig und deckt jede Entscheidung ab.
#
# Das Abnahmekriterium des Reviews zu B07 und B09 verlangt Beispiele mit erwarteter
# Entscheidung. Eine Tabelle, in der eine Spalte leer bleibt oder eine Entscheidung
# unbelegt ist, sieht aus wie ein Nachweis und ist keiner. Die Anzahl steht im Steckbrief
# und wird nachgezaehlt: In diesem Projekt war eine Zahl schon oefter zu klein.
GRENZFALL_DATEI = KERN + "/tests/EDGE_CASES.md"
GRENZFALL_SPALTEN = 7
GRENZFALL_ENTSCHEIDUNGEN = ("D-52", "D-53", "D-54", "D-55", "D-56", "D-59",
                            "D-61", "D-63", "D-64", "D-66", "D-67", "D-72")


def check_grenzfaelle(root: str) -> None:
    """Pruefung 30: Vollstaendigkeit der Grenzfalltabelle (CR-2026-052, CR-2026-053)."""
    pfad = os.path.join(root, GRENZFALL_DATEI.replace("/", os.sep))
    if not os.path.isfile(pfad):
        err(f"{GRENZFALL_DATEI}: fehlt. Die entschiedenen Regelkonflikte brauchen ihre "
            f"Grenzfaelle als Referenz - das ist das Abnahmekriterium des Reviews zu B07 "
            f"und B09")
        return
    text = read(pfad)
    m = re.search(r"\|\s*Anzahl der Grenzfälle\s*\|\s*(\d+)\s*\|", text)
    if not m:
        err(f"{GRENZFALL_DATEI}: Der Steckbrief nennt keine Anzahl der Grenzfaelle. Ohne "
            f"sie faellt eine geloeschte Zeile nicht auf")
        return
    erwartet = int(m.group(1))
    zeilen = [z for z in text.splitlines() if re.match(r"\|\s*G-\d+\s*\|", z)]
    if len(zeilen) != erwartet:
        err(f"{GRENZFALL_DATEI}: {len(zeilen)} Grenzfallzeilen, der Steckbrief nennt "
            f"{erwartet}. Eine Zahl, die nicht stimmt, ist kein Nachweis")
    for zeile in zeilen:
        zellen = tabellenzellen(zeile)
        kennung = zellen[0] if zellen else "?"
        if len(zellen) != GRENZFALL_SPALTEN:
            err(f"{GRENZFALL_DATEI}: Grenzfall {kennung} hat {len(zellen)} Spalten statt "
                f"{GRENZFALL_SPALTEN} (Nr., Grenzfall, Entscheidung, Betriebsmodus, "
                f"Kontrollstufe, Rollen, Fundstelle)")
            continue
        for nr, zelle in enumerate(zellen, 1):
            if not zelle or zelle in ("-", "–"):
                err(f"{GRENZFALL_DATEI}: Grenzfall {kennung}, Spalte {nr} ist leer. Jede "
                    f"Spalte ist Teil der Einstufung; eine leere Spalte laesst offen, was "
                    f"gilt")
            if TBD_RE.search(zelle):
                err(f"{GRENZFALL_DATEI}: Grenzfall {kennung}, Spalte {nr} traegt einen "
                    f"offenen <TBD>-Wert. Ein Grenzfall ohne Entscheidung ist keiner")
    for d in GRENZFALL_ENTSCHEIDUNGEN:
        if not any(d in z for z in zeilen):
            err(f"{GRENZFALL_DATEI}: Keine Grenzfallzeile verweist auf {d}. Jede "
                f"entschiedene Auslegungsfrage braucht mindestens einen Grenzfall, sonst "
                f"ist das Abnahmekriterium des Reviews nicht eingeloest")



# Pruefung 32: Eingabeschema und Pfadidentitaet des Schutz-Hooks (B06, CR-2026-056).
#
# Pruefung 16 belegt, dass der Hook jeden abgebildeten WERKZEUGNAMEN erkennt. Sie ruft ihn
# dafuer mit {"tool_name": ..., "tool_input": ...} auf - OHNE Umschlag. Genau daran ist der
# schwerste Teil von B06 vorbeigekommen: Der Client claude-code fuehrt in jedem Ereignis
# transcript_path, der unter ~/.claude/projects/ liegt und damit das Strukturmuster der
# Laufzeitschicht trifft. Bis 0.33.0 blockierte der Hook deshalb JEDEN Schreibzugriff
# dieses Packs, unabhaengig vom Ziel - am Client nachgemessen, mit Kontrolllauf
# (tests/protocols/2026-09-13-B06-gegenpruefung.md).
#
# DAS IST DIE LEHRE, UND SIE GEHOERT HIERHER: Eine Pruefung, die ihren Gegenstand mit
# selbst gebauter Eingabe aufruft, misst die selbst gebaute Eingabe. Diese Pruefung ruft
# den Hook deshalb mit dem VOLLSTAENDIGEN Umschlag JEDES aufgezeichneten Schemas auf. Bis
# 0.35.0 stand hier "beider" - es sind seit dem 2026-09-13 drei, weil ein Aufruf aus einem
# Unteragenten zwei zusaetzliche Felder fuehrt (CR-2026-058, Befund 5).
#
# Fuenf Gegenstaende, je Pack, jeder an der Wirkung gemessen und nicht am Vergleich zweier
# Listen:
#   1. Ereignisschema       - was kein Ereignis ist, blockiert mit --fail-closed (D-61).
#   2. Umschlag             - ein Nebenfeld darf die Entscheidung NICHT aendern (D-62).
#  2b. Unteragenten-Umschlag - agent_id und agent_type aendern sie ebenso wenig.
#   3. Unbekanntes Werkzeug - wird nach der strengsten Liste gemessen (CR-2026-056 E2).
#   4. Pfadidentitaet       - Varianten derselben Datei entscheiden gleich (D-63).
#
# WAS DIESE PRUEFUNG NICHT LEISTET: Sie misst am Hook, nicht am Client. Dass ein Client
# den Matcher einhaelt und genau dieses Schema sendet, belegt nur eine Sitzung (AP2). Und
# sie misst die Pfadvarianten dieser Plattform: Der 8.3-Kurzname und die Junction sind
# unter NTFS gepruefte Faelle, symbolische Verknuepfungen unter POSIX sind es nicht - sie
# brauchen eine Datei im Dateisystem und gehoeren deshalb in die Sonde, nicht hierher.
HOOK_UMSCHLAEGE = {
    # Aufgezeichnet, nicht angenommen: die Felder stammen aus den AP2-Mitschriften beider
    # Packs (leitwerk-erhebungen-2026-09-12 bzw. lw-tech). Der Unterschied ist der Punkt:
    # Nur eines der beiden Schemata fuehrt transcript_path und cwd.
    "claude-code": {"session_id": "s", "transcript_path": "/home/u/.claude/projects/p/s.jsonl",
                    "cwd": "/projekt", "permission_mode": "default",
                    "hook_event_name": "PreToolUse", "tool_use_id": "t"},
    "devin-desktop": {"session_id": "s", "prompt_id": "p", "hook_event_name": "PreToolUse",
                      "tool_use_id": "t"},
}

# Der DRITTE aufgezeichnete Umschlag (CR-2026-058 E3, Erhebung vom 2026-09-13): Ein
# Werkzeugaufruf aus einem UNTERAGENTEN traegt zusaetzlich agent_id und agent_type. Bis
# 0.35.0 sagte der Kopfkommentar dieser Pruefung, sie messe "mit dem vollstaendigen
# Umschlag beider aufgezeichneter Schemata" - es sind drei.
#
# WARUM DAS HIER STEHT, und warum nicht mehr behauptet wird als gemessen ist: Weder
# agent_id noch agent_type traegt einen Pfad; heute faengt dieser Fall nichts. Der Grund
# ist ein anderer - eine Pruefung, die ihre Grundlage benennt, darf sie nicht ueberholt
# tragen. Und der Grundsatz aus D-62 gilt hier woertlich: Ein zusaetzliches Umschlagfeld
# ist kein Pruefmaterial. Genau daran ist B06 gescheitert, mit transcript_path.
HOOK_UMSCHLAG_UNTERAGENT = {"agent_id": "a1cae648c0189377c", "agent_type": "fw-reviewer"}
KEIN_EREIGNIS = ("", "   ", "[]", "null", '"x"', "42", '{"tool_input": {}}',
                 '{"tool_name": "", "tool_input": {}}', '{"tool_name": "Write"}',
                 '{"tool_name": "Write", "tool_input": "x"}')


def _hook_interpreter() -> str | None:
    """Der erste Interpretername, der auf dieser Maschine wirklich Python startet."""
    for kandidat in ("python3", "python", "py"):
        try:
            lauf = subprocess.run([kandidat, "-c", "import sys; sys.stdout.write('%s')" % HOOK_SONDE],
                                  capture_output=True, text=True, timeout=15)
            if lauf.returncode == 0 and HOOK_SONDE in (lauf.stdout or ""):
                return kandidat
        except (OSError, subprocess.SubprocessError):
            continue
    return None


def _hook_lauf(interpreter: str, skript: str, eingabe: str) -> int:
    """Ruft den Schutz-Hook mit --fail-closed auf und liefert den Exit-Code."""
    try:
        lauf = subprocess.run([interpreter, skript, "--fail-closed"], input=eingabe,
                              capture_output=True, text=True, timeout=20,
                              env={k: v for k, v in os.environ.items()
                                   if k != "FW_HOOK_FAIL_CLOSED"})
    except (OSError, subprocess.SubprocessError):
        return -1
    return lauf.returncode


def check_hook_eingabeschema(root: str, man: dict) -> None:
    """Pruefung 32 (D-61 bis D-63): Ereignisschema, Umschlag und Pfadidentitaet."""
    skript = os.path.join(root, KERN, "tests", "scripts", "hook-check-secrets.py")
    if not os.path.isfile(skript):
        return
    interpreter = _hook_interpreter()
    if interpreter is None:
        return  # Pruefung 15 meldet diesen Fall bereits

    # Die Sonde auf den verlorenen Anker: Diese Pruefung misst die drei Stufen des Hooks.
    # Verschwinden sie, prueft sie einen Aufbau, den es nicht mehr gibt - und bestuende
    # dabei leise. Sie meldet ihr Fehlen deshalb selbst (D-23).
    quelle = read(skript)
    for anker in ("def ereignis_lesen(", "class Unpruefbar", "def aufloesen("):
        if anker not in quelle:
            err(f"{KERN}/tests/scripts/hook-check-secrets.py: '{anker}' fehlt. Pruefung 32 "
                f"misst Eingabeschema und Pfadidentitaet des Hooks; ohne diese Stufen "
                f"prueft sie einen Aufbau, den es nicht mehr gibt, und bestuende leise "
                f"(D-23, CR-2026-056)")
            return

    # 1. Ereignisschema. Mit --fail-closed MUSS jede Nicht-Ereignisform blockieren.
    for eingabe in KEIN_EREIGNIS:
        if _hook_lauf(interpreter, skript, eingabe) != 2:
            err(f"{KERN}/tests/scripts/hook-check-secrets.py: Die Eingabe "
                f"{eingabe!r} ist kein Werkzeugereignis, wird mit --fail-closed aber "
                f"nicht blockiert. 'Nichts gefunden' und 'nicht gesucht' duerfen nicht "
                f"denselben Exit-Code haben (D-61, Befund B06)")
    # Gegenprobe: Ein vollstaendiges, harmloses Ereignis mit zusaetzlichen unbekannten
    # Feldern MUSS durchlaufen. Ohne sie bestuende ein Hook, der einfach alles blockiert -
    # und eine additive Erweiterung des Clients wuerde ihn ausfallen lassen.
    harmlos = {"tool_name": "read", "tool_input": {"file_path": "src/app.py"},
               "ein_neues_feld_das_kein_pack_kennt": {"tief": ["x"]}}
    if _hook_lauf(interpreter, skript, json.dumps(harmlos)) != 0:
        err(f"{KERN}/tests/scripts/hook-check-secrets.py: Ein harmloses Ereignis mit "
            f"zusaetzlichen unbekannten Feldern wird blockiert. Eine additive Erweiterung "
            f"des Clients darf den Hook nicht ausfallen lassen (CR-2026-056 E1)")

    cdir = os.path.join(root, KERN, "clients")
    for pack in sorted(os.listdir(cdir)) if os.path.isdir(cdir) else []:
        if pack.startswith("_"):
            continue
        mf = os.path.join(cdir, pack, "manifest.json")
        if not os.path.isfile(mf):
            continue
        try:
            daten = json.loads(read(mf)) or {}
        except json.JSONDecodeError:
            continue
        schreibwerkzeuge = [w for w in ((daten.get("hook_tools") or {}).get("write") or [])
                            if isinstance(w, str) and w.strip()]
        if not schreibwerkzeuge:
            continue
        werkzeug = schreibwerkzeuge[0]
        umschlag = HOOK_UMSCHLAEGE.get(daten.get("client") or pack, {})

        def ereignis(name: str, eingabe: dict) -> str:
            voll = dict(umschlag)
            voll.update({"tool_name": name, "tool_input": eingabe})
            return json.dumps(voll)

        # 2. Der Umschlag darf die Entscheidung nicht aendern: zweimal dasselbe
        # tool_input, einmal nackt und einmal im vollen Umschlag des Clients.
        harmlose_eingabe = {"file_path": "src/app.py", "content": "x"}
        ohne = _hook_lauf(interpreter, skript, json.dumps(
            {"tool_name": werkzeug, "tool_input": harmlose_eingabe}))
        mit = _hook_lauf(interpreter, skript, ereignis(werkzeug, harmlose_eingabe))
        if ohne != mit:
            err(f"{pack}/manifest.json: Der Schutz-Hook entscheidet dieselbe Operation "
                f"verschieden, je nachdem ob der Umschlag des Clients mitgeschickt wird "
                f"(ohne: Exit {ohne}, mit: Exit {mit}). Geprueft wird die Operation, "
                f"nicht der Umschlag - ein Nebenfeld wie transcript_path oder cwd ist "
                f"kein Ziel (D-62, Befund B06)")
        elif mit != 0:
            err(f"{pack}/manifest.json: Der Schutz-Hook blockiert eine harmlose "
                f"Schreiboperation im vollen Umschlag dieses Clients (Exit {mit}). Bis "
                f"0.33.0 war das der Normalfall des Packs claude-code - jeder "
                f"Schreibzugriff scheiterte an einem Nebenfeld (D-62, Befund B06)")

        # 2b. Der Unteragenten-Umschlag ist ein Umschlag wie jeder andere: Dieselbe
        # Operation MUSS gleich entscheiden, ob sie aus dem Hauptagenten oder aus einem
        # Unteragenten kommt - bei der harmlosen wie bei der geschuetzten Operation. Die
        # zweite Haelfte ist die wichtigere: Eine Pruefung, die nur den harmlosen Fall
        # misst, bestuende auch dann, wenn der Hook mit diesen Feldern gar nichts mehr
        # entscheidet (CR-2026-058 E3).
        for name, eingabe, erwartet in (
                ("harmlos", {"file_path": "src/app.py", "content": "x"}, 0),
                ("geschuetzt", {"file_path": f"{KERN}/VERSION", "content": "9"}, 2)):
            voll = dict(umschlag)
            voll.update(HOOK_UMSCHLAG_UNTERAGENT)
            voll.update({"tool_name": werkzeug, "tool_input": eingabe})
            aus_unteragent = _hook_lauf(interpreter, skript, json.dumps(voll))
            if aus_unteragent != erwartet:
                err(f"{pack}/manifest.json: Der Schutz-Hook entscheidet eine {name}e "
                    f"Operation aus einem Unteragenten anders als erwartet "
                    f"(Exit {aus_unteragent}, erwartet {erwartet}). agent_id und "
                    f"agent_type sind Umschlagfelder wie transcript_path - kein "
                    f"Pruefmaterial und kein Grund, die Pruefung zu ueberspringen "
                    f"(D-62, CR-2026-058 E3)")

        # 3. Ein unbekanntes Werkzeug gilt als die strengste Operation, nicht als keine.
        if _hook_lauf(interpreter, skript, ereignis(
                "EinWerkzeugDasKeinPackKennt",
                {"file_path": f"{KERN}/VERSION", "content": "9"})) != 2:
            err(f"{pack}/manifest.json: Der Schutz-Hook laesst ein unbekanntes Werkzeug "
                f"in das Kernverzeichnis schreiben. Eine unbekannte Operation gilt als "
                f"die strengste, nicht als gar keine (CR-2026-056 E2, Befund B06)")

        # 4. Pfadidentitaet: Varianten, die dieselbe Datei bezeichnen, entscheiden gleich.
        for variante in (KERN.upper() + "/VERSION", "./" + KERN + "/VERSION",
                         KERN + "/tests/../VERSION", KERN + "\\VERSION"):
            if _hook_lauf(interpreter, skript, ereignis(
                    werkzeug, {"file_path": variante, "content": "9"})) != 2:
                err(f"{pack}/manifest.json: Der Schutz-Hook entscheidet die Pfadvariante "
                    f"'{variante}' anders als die Standardschreibweise, obwohl beide "
                    f"dieselbe Datei bezeichnen. Geprueft wird die Pfadidentitaet, nicht "
                    f"die Zeichenkette (D-63, Befund B06)")
        # Zwei Faelle, die je nur EIN Mechanismus faengt. Die Schreibvariante oben
        # faengt beides - re.I am Rohtext und die Aufloesung, die die Schreibweise
        # kanonisiert. Faellt einer der beiden aus, bestuende die Pruefung trotzdem, und
        # keine Sonde koennte es zeigen. Diese zwei trennen sie:
        #
        #   a) Nur die AUFLOESUNG: ein relativer Pfad, der den Kern nicht nennt. Bis
        #      0.33.0 blockierte er, weil cwd damals Pruefmaterial war - genau der
        #      Fehler, den D-62 abstellt. Jetzt traegt ihn allein die Aufloesung.
        nur_aufloesung = dict(umschlag)
        nur_aufloesung.update({
            "cwd": os.path.join(root, KERN, "tests"),
            "tool_name": werkzeug,
            "tool_input": {"file_path": "../VERSION", "content": "9"}})
        if _hook_lauf(interpreter, skript, json.dumps(nur_aufloesung)) != 2:
            err(f"{pack}/manifest.json: Ein relativer Pfad aus dem Kern heraus erreicht "
                f"das Kernverzeichnis, ohne es zu nennen, und wird nicht blockiert. Die "
                f"Pfadaufloesung gegen cwd traegt diesen Fall allein - die Muster sehen "
                f"nur '../VERSION' (D-63, CR-2026-056 E5)")
        #   b) Nur re.I: eine Secret-Datei, die es NICHT gibt. realpath kann eine nicht
        #      vorhandene Datei nicht kanonisieren, die Schreibweise bleibt also stehen.
        lesewerkzeuge = [w for w in ((daten.get("hook_tools") or {}).get("read") or [])
                         if isinstance(w, str) and w.strip()]
        if lesewerkzeuge:
            nur_schreibweise = dict(umschlag)
            nur_schreibweise.update({
                "tool_name": lesewerkzeuge[0],
                "tool_input": {"file_path": "gibt-es-nicht/.ENV"}})
            if _hook_lauf(interpreter, skript, json.dumps(nur_schreibweise)) != 2:
                err(f"{pack}/manifest.json: Der Schutz-Hook laesst einen Secret-Pfad in "
                    f"abweichender Schreibweise durch, wenn die Datei nicht existiert. "
                    f"Eine nicht vorhandene Datei kann die Aufloesung nicht "
                    f"kanonisieren; hier traegt allein re.I (D-63)")

        # Gegenprobe: Ein Verzeichnis, das nur so ANFAENGT wie der Kern, ist kein Kind
        # von ihm. Ohne sie bestuende eine Praefixpruefung, die jeden Nachbarn sperrt.
        if _hook_lauf(interpreter, skript, ereignis(
                werkzeug, {"file_path": KERN + "-notizen/x.txt", "content": "x"})) != 0:
            err(f"{pack}/manifest.json: Der Schutz-Hook blockiert ein Verzeichnis, das "
                f"nur so anfaengt wie das Kernverzeichnis. Ein Verzeichnis mit aehnlichem "
                f"Namensanfang ist kein Kind des geschuetzten (CR-2026-056 E5)")


# Pruefung 33: Die Abbildung von permissions.deny auf die Werkzeugsperre des Clients
# (Befund B01 in seiner Nachfolge, CR-2026-057, D-64 bis D-66).
#
# WARUM SIE DIE ERZEUGTE FASSUNG MISST UND NICHT DIE QUELLE: Genau daran ist B01
# vorbeigekommen. Zwoelf Quellskills fuehrten `permissions: deny: [edit, exec]`, das Feld
# stand in drop_fields, und keine installierte Fassung trug etwas davon - die Quelle sagte
# mehr, als die Installation hielt, und beides war fuer sich dokumentiert.
#
# WARUM SIE IHRE ERWARTUNG SELBST AUSRECHNET: Sie koennte deny_abbilden() aus install.py
# importieren. Dann pruefte sie aber nur noch, DASS der Installer gelaufen ist, nicht dass
# er richtig abbildet - sie teilte jeden Fehler der Abbildung. Die Verbtabelle steht
# deshalb bewusst ein zweites Mal hier. Laufen die beiden auseinander, faellt diese
# Pruefung; das ist der Zweck, nicht ein Versehen.
#
# WAS SIE NICHT LEISTET: Sie misst am erzeugten Text, nicht am Client. Dass
# disallowed-tools wirklich sperrt, belegt die Erhebung
# (tests/protocols/2026-09-13-erhebung-disallowed-tools.md), nicht der Validator.
#
# SEIT 0.40.0 fuehrt sie dasselbe Vokabular wie die Quelle (D-79): read, grep, glob,
# edit, exec. Bis dahin fuehrte sie 'write' und 'search' - zwei Verben der
# Durchsetzungsschicht - und kannte 'grep' und 'glob' nicht, obwohl jede der vierzehn
# Quellen sie im Nachbarfeld desselben Frontmatters nennt. Sie teilte damit genau die
# Luecke, die sie haette fangen sollen.
DENY_VERB_EIMER_33 = {"read": "read", "grep": "search", "glob": "search",
                      "edit": "write", "exec": "exec"}


def _deny_eintraege(fm_text: str) -> list[str]:
    """Die Eintraege unter permissions.deny einer Quelldatei, in ihrer Reihenfolge."""
    m = re.search(r"^permissions:[ \t]*\n((?:[ \t]+\S.*\n)+)", fm_text, re.M)
    if not m:
        return []
    m2 = re.search(r"^([ \t]+)deny:[ \t]*\n((?:[ \t]+-[ \t]+.*\n)+)", m.group(1), re.M)
    if not m2:
        return []
    return [z.strip().lstrip("-").strip() for z in m2.group(2).splitlines() if z.strip()]


def _werkzeugliste(wert) -> list[str]:
    """Ein Frontmatter-Werkzeugfeld als Liste - die Quelle notiert es als Liste, die
    erzeugte Fassung je nach Client als kommagetrennte Zeichenkette (AP2-CC-09)."""
    if isinstance(wert, str):
        return [x for x in re.split(r"[,\s]+", wert) if x]
    return [str(x) for x in (wert or [])]


def check_skill_deny_abbildung(root: str, man: dict) -> None:
    """Pruefung 33: permissions.deny wird abgebildet, und zwar ohne stille Schranken."""
    fmt = (man or {}).get("skill_frontmatter", {})
    deny_feld = fmt.get("skill_deny_field")
    if not deny_feld:
        return  # Ein Pack, das permissions nicht verwirft, braucht keine Abbildung

    # Die Sonde auf den verlorenen Anker: Diese Pruefung misst eine Abbildung, die in
    # install.py liegt. Verschwindet sie, prueft die Pruefung einen Aufbau, den es nicht
    # mehr gibt - und bestuende dabei leise (D-23).
    inst = os.path.join(root, KERN, "install.py")
    quelle = read(inst) if os.path.isfile(inst) else ""
    # Der zweite Anker hiess bis 0.39.0 DENY_VERB_EIMER und lag in install.py; seit
    # 0.40.0 steht die Bruecke in clientmap (D-78). Der Ankerwechsel ist nachgezogen
    # worden, weil der Sondenlauf ihn gemeldet hat - der Validatorlauf des Repositoriums
    # konnte es nicht, weil Pruefung 33 dort gar nicht laeuft (B02).
    for anker in ("def deny_abbilden(", "clientmap.VERB_BRUECKE"):
        if anker not in quelle:
            err(f"{KERN}/install.py: '{anker}' fehlt. Pruefung 33 misst die Abbildung von "
                f"permissions.deny auf {deny_feld}; ohne sie prueft sie einen Aufbau, den "
                f"es nicht mehr gibt, und bestuende leise (D-23, CR-2026-057)")
            return

    # Was bewusst NICHT abgebildet wird, MUSS deklariert sein - nie erraten (D-47).
    if not str(fmt.get("skill_deny_unmapped") or "").strip():
        err(f"{man.get('client', '?')}/manifest.json: skill_frontmatter.skill_deny_field "
            f"ist gesetzt, aber skill_deny_unmapped fehlt. Befehlsgenaue Verbote der Form "
            f"Exec(git push) sind bei diesem Client nicht ausdrueckbar; was nicht "
            f"abgebildet wird, wird deklariert und nicht verschwiegen (D-47, "
            f"CR-2026-057 E3)")

    eimer = man.get("hook_tools") or {}
    qdir = os.path.join(root, KERN, "framework", "skills")
    idir = os.path.join(root, *man["skills_dir"].split("/"))
    if not os.path.isdir(qdir) or not os.path.isdir(idir):
        return

    for name in sorted(os.listdir(qdir)):
        qpfad = os.path.join(qdir, name, "SKILL.md")
        ipfad = os.path.join(idir, name, "SKILL.md")
        if not os.path.isfile(qpfad) or not os.path.isfile(ipfad):
            continue
        qtext = read(qpfad)
        qkopf = qtext.split("\n---\n", 1)[0][4:] if qtext.startswith("---\n") else ""
        eintraege = _deny_eintraege(qkopf + "\n")

        # Erwartung, unabhaengig ausgerechnet: grobe Verben ueber hook_tools, alles mit
        # Klammer bleibt draussen (CR-2026-057 E3).
        erwartet: list[str] = []
        unabbildbar = [e for e in eintraege if "(" in e]
        for e in eintraege:
            if "(" in e:
                continue
            k = DENY_VERB_EIMER_33.get(e.strip().lower())
            for w in eimer.get(k, []) if k else []:
                if w not in erwartet:
                    erwartet.append(w)

        ifm, _ = parse_frontmatter(read(ipfad))
        ist = _werkzeugliste((ifm or {}).get(deny_feld))
        rel = f"{man['skills_dir']}/{name}/SKILL.md"

        if set(ist) != set(erwartet):
            err(f"{rel}: {deny_feld} traegt {ist or '[]'}; aus permissions.deny der Quelle "
                f"ergibt sich {erwartet or '[]'}. Die Quelle sagt sonst mehr, als die "
                f"Installation haelt - genau das war Befund B01 (D-65, CR-2026-057)")

        # Ein Eintrag mit Klammer wirkt gemessen LAUTLOS gar nicht: Er blockiert nichts und
        # meldet nichts. Er darf in keiner erzeugten Fassung stehen (D-66, E5).
        for w in ist:
            if "(" in w or ")" in w:
                err(f"{rel}: {deny_feld} enthaelt das Argumentmuster '{w}'. Gemessen am "
                    f"2026-09-13 laesst ein solcher Eintrag den Befehl lautlos durchlaufen "
                    f"- wer ihn schreibt, hat gar keine Schranke, nicht bloss eine "
                    f"groebere. Nur der blosse Werkzeugname sperrt (D-66)")

        # Ein Werkzeug in beiden Listen ist ein Widerspruch. Gemessen gewinnt die Sperre -
        # aber ein Skill, der ein Werkzeug zugleich vorabfreigibt und entfernt, sagt zwei
        # Dinge, und eines davon ist falsch.
        doppelt = sorted(set(ist) & set(_werkzeugliste((ifm or {}).get("allowed-tools"))))
        if doppelt:
            err(f"{rel}: {', '.join(doppelt)} steht zugleich in allowed-tools und in "
                f"{deny_feld}. Gemessen gewinnt die Sperre; die Vorabfreigabe daneben ist "
                f"eine Aussage, die nicht stimmt (CR-2026-057)")

        # Traegt die Quelle unabbildbare Eintraege, MUSS das Pack sie deklariert haben -
        # oben schon geprueft; hier bleibt der Hinweis, dass es diesen Skill betrifft.
        if unabbildbar and not str(fmt.get("skill_deny_unmapped") or "").strip():
            err(f"{rel}: die Quelle nennt {len(unabbildbar)} befehlsgenaue(s) Verbot(e), "
                f"die dieser Client nicht ausdruecken kann, und das Pack deklariert es "
                f"nicht (D-47)")


# Pruefung 31: Die Zusammenfassung der Durchsetzungstiefe stimmt mit der Matrix.
#
# Die Summen sind dreimal gedriftet, und jedes Mal von Hand berichtigt worden: mit 0.26.0
# fuehrte ein Pack "von 26", waehrend die Matrix 29 Zeilen trug (A2, M4, M5 kamen mit
# CR-2026-025 hinzu); mit 0.31.0 wanderte S3 auf [NICHT ABBILDBAR], ohne dass die
# Zusammenfassung es nachzog; und die vier Zeilen mit einer Kanalgrenze zaehlten weiter als
# technisch, obwohl D-47 sie je Kanal ausweist - die Tabelle ueberzeichnete die
# Durchsetzungstiefe damit um vier Zeilen und ihre Ueberschrift um drei Kernzusagen (B11,
# D-60). Eine Zahl, die dreimal von Hand stimmen musste, gehoert ausgerechnet.
#
# ZAEHLREGEL, identisch zu der im Pack: Eine Zeile zaehlt bei ihrer SCHWAECHSTEN
# Einstufung. [NICHT ABBILDBAR] vor [TEXTUELL] vor [TECHNISCH]. Eine Zeile ohne jede
# Einstufung ist ein Fehler - sie sagt nichts zu.
#
# WAS DIESE PRUEFUNG NICHT LEISTET: Sie prueft die Arithmetik, nicht die Einstufung. Ob
# eine Zeile richtig eingestuft ist, kann kein Skript beurteilen; das leistet die Erhebung
# an einer Installation (AP2). Eine Matrix, in der jede Zeile falsch eingestuft ist,
# besteht diese Pruefung.
MATRIXZEILE_RE = re.compile(r"^\|\s*([A-Z]\d+)\s*\|")
EINSTUFUNGEN = ("[NICHT ABBILDBAR]", "[TEXTUELL]", "[TECHNISCH]")
SUMMENZEILE_RE = re.compile(
    r"^\|\s*\*{0,2}`\[([A-Z ]+)\]`\*{0,2}\s*\|\s*\*{0,2}(\d+)\s+von\s+(\d+)", re.M)


def check_durchsetzungstiefe(root: str) -> None:
    """Pruefung 31 (D-60): Die Summen der Fachmatrix sind aus ihr ausgerechnet."""
    cdir = os.path.join(root, KERN, "clients")
    if not os.path.isdir(cdir):
        return
    for pack in sorted(os.listdir(cdir)):
        # Die Vorlage fuer ein neues Pack traegt ueberall <TBD> statt einer Einstufung -
        # sie hat nichts zu summieren. Ausgenommen wird sie ueber die
        # Unterstrich-Konvention der Ablage, nicht ueber ihren Namen: Ein zweites
        # Vorlagenverzeichnis wuerde sonst durchfallen, und eine Ausnahme je Name waere
        # eine gepflegte Liste (dieselbe Begruendung wie bei Pruefung 14).
        if pack.startswith("_"):
            continue
        pfad = os.path.join(cdir, pack, "CLIENT_PACK.md")
        if not os.path.isfile(pfad):
            continue
        rel = f"{KERN}/clients/{pack}/CLIENT_PACK.md"
        text = read(pfad).replace("\r\n", "\n")
        marke = text.find("## 3. Zusammenfassung")
        if marke < 0:
            err(f"{rel}: kein Abschnitt '## 3. Zusammenfassung der Durchsetzungstiefe'. "
                f"Ohne ihn prueft Pruefung 31 nichts und bestuende leise (D-23)")
            continue

        gezaehlt = {k: [] for k in EINSTUFUNGEN}
        ohne = []
        for zeile in text[:marke].split("\n"):
            m = MATRIXZEILE_RE.match(zeile)
            if not m:
                continue
            for k in EINSTUFUNGEN:          # schwaechste zuerst
                if k in zeile:
                    gezaehlt[k].append(m.group(1))
                    break
            else:
                ohne.append(m.group(1))
        summe = sum(len(v) for v in gezaehlt.values()) + len(ohne)
        if ohne:
            err(f"{rel}: Matrixzeile(n) ohne Einstufung: {', '.join(ohne)}. Eine Zeile "
                f"ohne Einstufung sagt nichts zu und zaehlt in keiner Klasse")
        if not summe:
            err(f"{rel}: keine Matrixzeile gefunden. Der Anker dieser Pruefung ist die "
                f"Zeilenform '| <Kennung> |'; ohne sie prueft sie nichts (D-23)")
            continue

        gefunden = SUMMENZEILE_RE.findall(text[marke:])
        if not gefunden:
            err(f"{rel}: Die Zusammenfassung fuehrt keine Zeile der Form "
                f"'| `[KLASSE]` | N von M |'. Ohne sie ist die Summe nicht pruefbar")
            continue
        for klasse, anzahl, gesamt in gefunden:
            k = "[%s]" % klasse.strip()
            if k not in gezaehlt:
                continue
            if int(gesamt) != summe:
                err(f"{rel}: Die Zusammenfassung nennt fuer {k} eine Gesamtzahl von "
                    f"{gesamt} Matrixzeilen; gezaehlt sind {summe}. Die Summen sind "
                    f"dreimal gedriftet, deshalb werden sie ausgerechnet (D-60)")
            if int(anzahl) != len(gezaehlt[k]):
                err(f"{rel}: Die Zusammenfassung nennt {anzahl} Zeile(n) als {k}; "
                    f"gezaehlt sind {len(gezaehlt[k])} ({', '.join(gezaehlt[k]) or 'keine'}). "
                    f"Zaehlregel: eine Zeile zaehlt bei ihrer schwaechsten Einstufung, "
                    f"weil eine Kanalgrenze keine technische Durchsetzung ist (D-47, D-60)")

        # DIESELBE ZAHL STEHT EIN ZWEITES MAL, in der Uebersicht der Ablage - und dort
        # rechnete sie bis 0.35.0 niemand nach. Ergebnis: 'claude-code' fuehrte dort
        # "25 von 29", waehrend das Pack selbst einen Absatz darueber traegt, dass diese
        # Zahl mit 0.33.0 auf 22 von 31 berichtigt wurde; 'devin-desktop' fuehrte
        # "24 von 34" statt 20 von 36. Die Berichtigung hatte die zweite Stelle nicht
        # erreicht (CR-2026-058 E7, D-71).
        _uebersicht_pruefen(root, pack, len(gezaehlt["[TECHNISCH]"]), summe)


UEBERSICHT_DATEI = KERN + "/clients/README.md"


def _uebersicht_pruefen(root: str, pack: str, technisch: int, summe: int) -> None:
    """Die Zeile dieses Packs in clients/README.md fuehrt dieselbe Zahl (D-71)."""
    pfad = os.path.join(root, UEBERSICHT_DATEI.replace("/", os.sep))
    if not os.path.isfile(pfad):
        err(f"{UEBERSICHT_DATEI}: fehlt. Die Uebersicht der Ablage fuehrt je Pack die "
            f"Zahl der technisch durchgesetzten Zeilen und wird gegen die Matrix "
            f"gerechnet (D-71)")
        return
    text = read(pfad).replace("\r\n", "\n")
    treffer = None
    for zeile in text.split("\n"):
        if not zeile.startswith("| `%s`" % pack):
            continue
        treffer = tabellenzellen(zeile)
        break
    if treffer is None:
        err(f"{UEBERSICHT_DATEI}: kein Eintrag fuer das Client Pack '{pack}'. Jedes Pack "
            f"der Ablage gehoert in die Uebersicht (Abschnitt 5, Schritt 8)")
        return
    zahl = next((z for z in treffer if re.fullmatch(r"\d+ von \d+", z)), None)
    if zahl is None:
        err(f"{UEBERSICHT_DATEI}: Die Zeile fuer '{pack}' fuehrt keine Zelle der Form "
            f"'N von M'. Ohne sie prueft diese Haelfte nichts und bestuende leise (D-23)")
        return
    soll = "%d von %d" % (technisch, summe)
    if zahl != soll:
        err(f"{UEBERSICHT_DATEI}: Die Uebersicht nennt fuer '{pack}' '{zahl}' technisch "
            f"durchgesetzte Zeilen; aus der Faehigkeitsmatrix gezaehlt sind '{soll}'. "
            f"Eine Zahl mit eindeutiger Grenze gehoert ausgerechnet, nicht an zweiter "
            f"Stelle gepflegt - hier ist sie zweimal gedriftet (D-71, CR-2026-058 E7)")


# Pruefung 34: Das Startwerkzeug fuer Unteragenten ist genannt oder seine Abwesenheit
# erklaert (CR-2026-058 E2, D-70).
#
# Bauform wie Pruefung 26 (hook_tools_absent, D-47), eine Ebene weiter. Der Anlass ist ein
# gemessener Befund: Ein Skill kann einen Unteragenten starten, und das Startwerkzeug stand
# in KEINER Werkzeugliste eines Manifests - nicht in hook_tools, nicht in permission_tools,
# nicht in agent_frontmatter.tool_names. Ein Kanal ohne Deklaration ist genau das, was D-47
# abgestellt hat.
#
# Bei claude-code ist gemessen, dass beide Schreibweisen (Agent, Task) in disallowed-tools
# wirken; bei devin-desktop ist NICHTS gemessen, und die leere Liste sagt deshalb etwas
# ueber den Belegstand, nicht ueber den Client.
#
# EINE ERKLAERUNG REICHT NICHT, WENN DAS PACK A1 OHNE VORBEHALT ZUSAGT: Zeile A1
# verspricht ein rein lesendes Reviewprofil. Ein Pack, das diese Zeile auf [TECHNISCH]
# stellt UND keinen offenen VERIFY-Marker mehr darauf fuehrt, behauptet, dass es
# Unteragenten gibt und dass ihre Werkzeuge beschraenkbar sind - dann ist "kennt kein
# Startwerkzeug" kein zulaessiger Stand.
#
# DER VORBEHALT GEHOERT DAZU, und das hat diese Pruefung bei ihrem ersten Lauf selbst
# gezeigt: Ohne ihn fiel devin-desktop durch. Dessen Zeile A1 steht auf [TECHNISCH], aber
# die Praeambel des Packs sagt ausdruecklich, die Spalte nenne die VORGESEHENE
# Durchsetzungstiefe, und die Zeile traegt einen offenen VERIFY-Marker auf genau die
# Profilwirkung. Die Einstufung allein sagt also nicht, ob eine Zusage schon gilt - das
# sagt der Marker. Eine Pruefung, die beides verwechselt, meldet einen Fehler, wo das Pack
# ehrlich ist (CR-2026-058, Wirkungsnachweis).
#
# WAS DIESE PRUEFUNG NICHT LEISTET: Sie prueft die Deklaration, nicht ihre Richtigkeit. Ob
# der genannte Name beim Client wirklich sperrt, belegt allein eine Erhebung.
def check_agent_startwerkzeug(root: str) -> None:
    """Pruefung 34 (D-70): agent_start_tools ist genannt oder erklaert."""
    basis = os.path.join(root, KERN, "clients")
    if not os.path.isdir(basis):
        return
    for pack in sorted(os.listdir(basis)):
        if pack.startswith("_"):
            continue
        pfad = os.path.join(basis, pack, "manifest.json")
        if not os.path.isfile(pfad):
            continue
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        try:
            man = json.loads(read(pfad))
        except ValueError:
            continue
        namen = man.get("agent_start_tools")
        if namen is None:
            err(f"{rel}: Feld 'agent_start_tools' fehlt. Ein Skill kann einen Unteragenten "
                f"starten; mit welchem Werkzeug, gehoert deklariert - und wenn es "
                f"unbekannt oder unerhoben ist, gehoert das ausdruecklich dorthin statt "
                f"verschwiegen (D-70, Bauform wie hook_tools_absent nach D-47)")
            continue
        if not isinstance(namen, list):
            err(f"{rel}: 'agent_start_tools' ist keine Liste")
            continue
        gefuellt = [n for n in namen if isinstance(n, str) and n.strip()]
        abwesend = man.get("agent_start_tools_absent") or []
        notiz = str(man.get("_agent_start_tools_absent_note") or "").strip()
        if gefuellt:
            if abwesend:
                err(f"{rel}: 'agent_start_tools' nennt {gefuellt} und "
                    f"'agent_start_tools_absent' erklaert zugleich eine Abwesenheit. "
                    f"Beides zugleich geht nicht (D-70)")
            continue
        if not abwesend:
            err(f"{rel}: 'agent_start_tools' ist leer, ohne dass "
                f"'agent_start_tools_absent' die Abwesenheit erklaert. Eine leere Liste "
                f"allein sagt nicht, ob der Client kein solches Werkzeug kennt oder ob es "
                f"nur nicht erhoben ist - genau diese Unterscheidung ist der Zweck des "
                f"Feldes (D-70, D-47)")
            continue
        if not notiz:
            err(f"{rel}: 'agent_start_tools_absent' nennt {sorted(abwesend)}, aber "
                f"'_agent_start_tools_absent_note' fehlt oder ist leer. Eine erklaerte "
                f"Abwesenheit ohne Begruendung ist eine Behauptung (D-70, D-47)")
        # Wer A1 auf [TECHNISCH] stellt, sagt zu, dass es Unteragenten gibt und dass ihre
        # Werkzeuge beschraenkbar sind. Dann ist eine Erklaerung kein zulaessiger Stand.
        pack_md = os.path.join(basis, pack, "CLIENT_PACK.md")
        if not os.path.isfile(pack_md):
            continue
        for zeile in read(pack_md).replace("\r\n", "\n").split("\n"):
            if (re.match(r"^\|\s*A1\s*\|", zeile) and "[TECHNISCH]" in zeile
                    and "<VERIFY" not in zeile):
                err(f"{rel}: Zeile A1 des Packs steht auf [TECHNISCH] - das Pack sagt ein "
                    f"rein lesendes Unteragentenprofil technisch zu -, aber "
                    f"'agent_start_tools' ist leer und nur erklaert. Wer Unteragenten "
                    f"zusagt, nennt das Werkzeug, mit dem sie starten (D-70)")
                break



# Pruefung 35: Ein Agentenprofil bekommt kein Startwerkzeug (CR-2026-059 E1, D-73).
#
# Gemessen am 2026-09-13 (tests/protocols/2026-09-13-erhebung-unteragent-tiefe.md,
# Lauf STARTLOS): Ein Profil mit tools: Read, Grep, Glob - genau die Form, die
# fw-reviewer nach der Abbildung traegt - hat KEIN Startwerkzeug und konnte deshalb
# keinen weiteren Unteragenten starten, dessen Profil weniger beschraenkt waere. Ohne
# diesen Befund waere die Zusage A1 ueber eine zweite Ebene aushebelbar.
#
# WAS DIESE PRUEFUNG IST UND WAS NICHT: Sie faengt heute NICHTS. Die Abbildung
# agent_frontmatter.tool_names kennt gar kein Startwerkzeug, also kann keine erzeugte
# tools-Liste eines enthalten. Sie ist eine VERANKERUNG, keine Behebung - dieselbe
# Bauart wie der fuenfte Gegenstand der Pruefung 32, und sie wird mit derselben
# Ehrlichkeit begruendet: Erweitert jemand tool_names um ein Startwerkzeug, faellt die
# Zusage LAUTLOS, und niemand prueft es. Danach faengt diese Pruefung es.
#
# Geprueft wird an ZWEI Stellen, weil eine allein zu wenig waere:
#   1. Die ABBILDUNG - tool_names darf keinen Namen aus agent_start_tools fuehren.
#   2. Die QUELLE - kein ausgeliefertes Agentenprofil nennt eines direkt. Diese Haelfte
#      faengt den Fall, dass jemand am Profil vorbei an der Abbildung schreibt.
def check_agent_profil_ohne_start(root: str) -> None:
    """Pruefung 35 (D-73): Kein Agentenprofil bekommt ein Startwerkzeug."""
    basis = os.path.join(root, KERN, "clients")
    if not os.path.isdir(basis):
        return
    alle_start = set()
    for pack in sorted(os.listdir(basis)):
        if pack.startswith("_"):
            continue
        pfad = os.path.join(basis, pack, "manifest.json")
        if not os.path.isfile(pfad):
            continue
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        try:
            man = json.loads(read(pfad))
        except ValueError:
            continue
        start = {n.strip().lower() for n in (man.get("agent_start_tools") or [])
                 if isinstance(n, str) and n.strip()}
        if not start:
            continue  # ob das zulaessig ist, entscheidet Pruefung 34
        alle_start |= start

        # 1. Die Abbildung darf kein Startwerkzeug fuehren.
        abbildung = (man.get("agent_frontmatter") or {}).get("tool_names") or {}
        for verb, namen in sorted(abbildung.items()):
            for name in (namen if isinstance(namen, list) else []):
                if isinstance(name, str) and name.strip().lower() in start:
                    err(f"{rel}: agent_frontmatter.tool_names bildet das Verb "
                        f"'{verb}' auf '{name}' ab - ein Werkzeug, mit dem ein "
                        f"Unteragent GESTARTET wird (agent_start_tools). Ein "
                        f"Agentenprofil, das es bekommt, kann eine zweite, weniger "
                        f"beschraenkte Ebene oeffnen; die Zusage A1 waere damit "
                        f"aushebelbar (D-73, CR-2026-059)")

    # 2. Kein ausgeliefertes Agentenprofil nennt ein Startwerkzeug direkt.
    #
    # Diese Haelfte laeuft EINMAL ueber die Ablage des Kerns, nicht je Pack: Die Profile
    # sind geteilt (shared_core), die Startwerkzeuge sind es nicht. Geprueft wird gegen
    # die VEREINIGUNG aller Packs - ein Name, der bei einem Pack startet, gehoert in kein
    # Profil, weil dasselbe Profil auch dort ausgeliefert wird.
    if not alle_start:
        return
    adir = os.path.join(root, KERN, "framework", "runtime", "agents")
    if not os.path.isdir(adir):
        err(f"{KERN}/framework/runtime/agents: fehlt. Pruefung 35 misst die "
            f"Agentenprofile des Kerns; ohne die Ablage prueft sie nichts und "
            f"bestuende leise (D-23)")
        return
    for datei in sorted(os.listdir(adir)):
        if not datei.endswith(".md"):
            continue
        rel = KERN + "/framework/runtime/agents/" + datei
        roh = read(os.path.join(adir, datei)).replace("\r\n", "\n")
        teile = roh.split("---")
        if len(teile) < 3:
            err(f"{rel}: kein Frontmatter zwischen zwei '---'. Ohne es prueft "
                f"Pruefung 35 nichts und bestuende leise (D-23)")
            continue
        for name in sorted(alle_start):
            muster = r"(?<![A-Za-z])%s(?![A-Za-z])" % re.escape(name.lower())
            if re.search(muster, teile[1].lower()):
                err(f"{rel}: Das Frontmatter nennt '{name}' - ein Werkzeug, mit dem "
                    f"ein Unteragent GESTARTET wird (agent_start_tools). Ein Profil, "
                    f"das es bekommt, kann eine zweite, weniger beschraenkte Ebene "
                    f"oeffnen, und die Zusage A1 waere aushebelbar (D-73, "
                    f"CR-2026-059)")


# Pruefung 36: Jede Tabellenzeile des Decision Logs fuehrt so viele Zellen wie der
# Kopf ihrer Tabelle (CR-2026-060 E4, D-75).
#
# Anlass: Vier zerrissene Zeilen in 0.34.0 - D-61 bis D-63 mit fuenf Zellen statt sechs,
# D-29 mit acht, dort teilte ein unmaskierter Strich in einem Codespan die Zeile. In der
# gerenderten Tabelle stand die Herkunft unter "Begruendung", das Datum unter
# "Alternativen", die Rolle unter "Status". D-29 stand so seit 0.10.x. Gefunden hat die
# Zeilen jedes Mal ein Mensch beim Eintragen einer anderen.
#
# WAS SIE HEUTE FAENGT: nichts. Alle Zeilen sind seit 0.35.0 in Ordnung, von Hand
# berichtigt. Das ist eine VERANKERUNG, keine Behebung - wie Pruefung 35 und der fuenfte
# Gegenstand der Pruefung 32. Der Unterschied: Ihr Gegenbeweis ist ein Abzaehlen und
# keine Konstruktion. Gegen 0.34.0 meldet sie vier Fundstellen, gegen 0.32.0 und 0.33.0
# je eine.
#
# WAS SIE NICHT LEISTET: Sie prueft die Anzahl, nicht den Inhalt. Eine Zeile, in der
# Begruendung und Alternativen vertauscht sind, besteht sie - dieselbe Grenze, die
# Pruefung 31 fuer ihre Arithmetik benennt. Und sie prueft nur diese eine Datei: Die
# uebrigen Tabellen des Repositoriums haben ihre eigenen Pruefungen (30, 31) oder keine.
DECISION_LOG_DATEI = KERN + "/governance/DECISION_LOG.md"


def check_decision_log_zellen(root: str) -> None:
    """Pruefung 36 (D-75): Die Tabellen des Decision Logs sind nicht zerrissen."""
    pfad = os.path.join(root, DECISION_LOG_DATEI.replace("/", os.sep))
    if not os.path.isfile(pfad):
        err(f"{DECISION_LOG_DATEI}: fehlt. Ohne das Decision Log ist keine Entscheidung "
            f"dieses Frameworks belegt")
        return
    zeilen = read(pfad).replace("\r\n", "\n").split("\n")
    soll = None
    ueberschrift = "(vor der ersten Ueberschrift)"
    kopfzeile = 0
    gesehen = 0
    for nr, zeile in enumerate(zeilen, 1):
        z = zeile.strip()
        if z.startswith("## "):
            ueberschrift = z[3:].strip()
            soll = None
            continue
        if not z.startswith("|"):
            # Eine Leerzeile beendet die Tabelle; Fliesstext zwischen zwei Tabellen
            # darf die Zellenzahl nicht von der einen auf die andere uebertragen.
            if not z:
                soll = None
            continue
        zellen = tabellenzellen(z)
        if soll is None:
            soll = len(zellen)
            kopfzeile = nr
            gesehen += 1
            continue
        if len(zellen) != soll:
            err(f"{DECISION_LOG_DATEI}:{nr}: Die Zeile fuehrt {len(zellen)} Zellen, der "
                f"Kopf ihrer Tabelle ({ueberschrift}, Zeile {kopfzeile}) fuehrt {soll}. "
                f"Eine zerrissene Zeile rendert die Werte unter den falschen Spalten; "
                f"ein Strich innerhalb einer Zelle gehoert maskiert (\\|)")
    if not gesehen:
        err(f"{DECISION_LOG_DATEI}: keine Tabellenzeile gefunden. Der Anker dieser "
            f"Pruefung ist die Zeilenform '| ... |'; ohne sie prueft sie nichts und "
            f"bestuende leise (D-23)")


# Pruefung 38: Eine Quelle, ein Vokabular - und die Sperrliste ist nie enger als die
# Vorabfreigabe (CR-2026-062, D-78 bis D-80).
#
# ANLASS. Ein Manifest fuehrt VIER Werkzeugabbildungen, nicht zwei: skill_frontmatter.
# tool_names, agent_frontmatter.tool_names, hook_tools und permission_tools - dazu
# agent_start_tools daneben. Drei Vokabulare stossen darin aufeinander: das der Quelle
# (read, grep, glob, edit, exec), das des Hooks (read, search, exec, write) und das der
# Berechtigungsdatei (read, search, write, exec, fetch, mcp).
#
# Gemessen am 2026-09-13 (tests/protocols/2026-09-13-gegenpruefung-werkzeugabbildung.md):
# DREI der vier Abbildungen brechen ab, wenn ihnen ein Verb fehlt - die vierte reichte
# es woertlich durch, und sie kommt zweimal vor. Eine geleerte tool_names-Abbildung
# lieferte 'tools: read, grep, glob' im Agentenprofil fw-reviewer, also drei Namen, die
# dieser Client nicht kennt (M16); ein 'permissions.deny: glob' erzeugte lautlos keine
# Sperre, und der Validator meldete 0 Fehler (M6).
#
# VIER GEGENSTAENDE:
#   1. Der verlorene Anker. Fehlen clientmap.FRONTMATTER_VERBEN oder VERB_BRUECKE,
#      meldet diese Pruefung das selbst - sonst bestuende sie leise (D-23).
#   2. Die Deklaration je Pack. Jedes Verb des Vokabulars ist in tool_names abgebildet
#      ODER in tool_names_unmapped erklaert, samt nicht leerer _tool_names_unmapped_note;
#      beides zugleich ist ein Widerspruch, ein Schluessel ausserhalb des Vokabulars ein
#      Schreibfehler. Bauform wie Pruefung 26 (hook_tools_absent, D-47) und Pruefung 34.
#   3. Die RICHTUNG zwischen Vorabfreigabe und Sperre. Fuer jedes Verbpaar der Bruecke
#      muss hook_tools mindestens so weit sein wie tool_names. Heute ist es das bei allen
#      fuenf; die Abweichung, die es gibt, geht in die zulaessige Richtung
#      (tool_names.edit fuehrt Edit und Write, hook_tools.write zusaetzlich NotebookEdit).
#      Umgekehrt waere sie eine Luecke: Ein Skill, der 'edit' vorab freigibt und 'edit'
#      sperrt, bekaeme ein Werkzeug freigegeben, das die Sperre nicht erfasst.
#   4. Die Quellen. Kein ausgeliefertes SKILL.md und kein Agentenprofil nennt in
#      allowed-tools oder permissions.deny ein Verb ausserhalb des Vokabulars.
#
# WAS SIE HEUTE FAENGT: bei den beiden Packs nichts - sie sind in Ordnung, seit
# devin-desktop seine fuenf nicht abgebildeten Verben deklariert. Gegenstand 3 ist eine
# VERANKERUNG wie Pruefung 35 und 36; Gegenstand 2 faengt gegen 0.39.0 zehn Fundstellen,
# Gegenstand 4 keine. Das steht so im Wirkungsnachweis und ist kein Abzaehlen von
# Befunden, sondern eines von Deklarationen.
#
# WAS SIE NICHT LEISTET: Sie belegt nicht, dass die Werkzeugnamen eines Packs RICHTIG
# sind - das kann nur eine Erhebung, und fuer devin-desktop steht sie aus. Sie belegt,
# dass jedes Verb des Vokabulars eine Antwort hat und dass die beiden Listen nicht in
# die gefaehrliche Richtung auseinanderlaufen.
FRONTMATTER_BLOECKE = ("skill_frontmatter", "agent_frontmatter")


def _frontmatter_verben(text: str) -> tuple[list[str], list[str]]:
    """Die groben Verben aus allowed-tools und permissions.deny eines Frontmatters."""
    fm = text.replace("\r\n", "\n")
    if not fm.startswith("---\n") or "\n---\n" not in fm:
        return [], []
    fm = fm.split("\n---\n", 1)[0][4:] + "\n"
    m = re.search(r"^allowed-tools:[ \t]*\n((?:[ \t]+-[ \t]+\S+[ \t]*\n)+)", fm, re.M)
    erlaubt = [x.strip("- \t") for x in m.group(1).strip().split("\n")] if m else []
    verboten: list[str] = []
    m = re.search(r"^permissions:[ \t]*\n((?:[ \t]+\S.*\n)+)", fm, re.M)
    if m:
        m2 = re.search(r"^([ \t]+)deny:[ \t]*\n((?:[ \t]+-[ \t]+.*\n)+)", m.group(1), re.M)
        if m2:
            verboten = [z.strip().lstrip("-").strip() for z in m2.group(2).splitlines()
                        if z.strip() and "(" not in z]
    return erlaubt, verboten


def _quelldateien(root: str) -> list[tuple[str, str]]:
    """Die ausgelieferten Quellen mit Frontmatter-Verben: Skills und Agentenprofile."""
    out: list[tuple[str, str]] = []
    basis = os.path.join(root, KERN, "framework")
    for wurzel, verzeichnisse, dateien in os.walk(basis):
        verzeichnisse[:] = sorted(d for d in verzeichnisse if d != "__pycache__")
        for datei in sorted(dateien):
            if datei != "SKILL.md" and not wurzel.endswith(os.sep + "agents"):
                continue
            if not datei.endswith(".md"):
                continue
            pfad = os.path.join(wurzel, datei)
            out.append((os.path.relpath(pfad, root).replace(os.sep, "/"), read(pfad)))
    return out


def check_werkzeugabbildung(root: str) -> None:
    """Pruefung 38 (D-78 bis D-80): eine Quelle, ein Vokabular, eine Richtung."""
    kern = os.path.join(root, KERN)
    if kern not in sys.path:
        sys.path.insert(0, kern)
    try:
        import clientmap
    except ImportError:
        warn(f"{KERN}/clientmap.py nicht gefunden - Pruefung 38 laeuft nicht")
        return
    # Die Sonde auf den verlorenen Anker (seit 0.32.0): Diese Pruefung findet ihren
    # Gegenstand ueber zwei Namen des Moduls. Verschwinden sie, bestuende sie leise.
    fehlend = [n for n in ("FRONTMATTER_VERBEN", "VERB_BRUECKE")
               if not getattr(clientmap, n, None)]
    if fehlend:
        err(f"{KERN}/clientmap.py: {', '.join(fehlend)} fehlt - Pruefung 38 hat ihren "
            f"Anker verloren und wuerde leise bestehen (D-23, D-78)")
        return
    vokabular = tuple(clientmap.FRONTMATTER_VERBEN)
    bruecke = dict(clientmap.VERB_BRUECKE)

    basis = os.path.join(root, KERN, "clients")
    if not os.path.isdir(basis):
        return
    gesehen = 0
    for pack in sorted(os.listdir(basis)):
        if pack.startswith("_"):
            continue
        pfad = os.path.join(basis, pack, "manifest.json")
        if not os.path.isfile(pfad):
            continue
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        try:
            man = json.loads(read(pfad))
        except ValueError:
            continue
        gesehen += 1
        hook = man.get("hook_tools") or {}
        for block in FRONTMATTER_BLOECKE:
            fmt = man.get(block)
            if fmt is None:
                err(f"{rel}: Block '{block}' fehlt - ohne ihn ist nicht entschieden, "
                    f"welche Werkzeugnamen die installierte Fassung traegt (D-78)")
                continue
            abbildung = fmt.get("tool_names")
            if not isinstance(abbildung, dict):
                err(f"{rel}: {block}.tool_names fehlt oder ist kein Objekt")
                continue
            erklaert = fmt.get("tool_names_unmapped") or []
            if not isinstance(erklaert, list):
                err(f"{rel}: {block}.tool_names_unmapped ist keine Liste")
                erklaert = []
            if erklaert and not str(fmt.get("_tool_names_unmapped_note") or "").strip():
                err(f"{rel}: {block}.tool_names_unmapped nennt {sorted(erklaert)}, aber "
                    f"'_tool_names_unmapped_note' fehlt oder ist leer. Ein Verb nicht "
                    f"abzubilden ist eine Aussage ueber den Client oder ueber den "
                    f"Belegstand - sie gehoert begruendet, nicht bloss eingetragen "
                    f"(D-78, Bauform wie hook_tools_absent nach D-47)")
            for schluessel in sorted(abbildung):
                if schluessel not in vokabular:
                    err(f"{rel}: {block}.tool_names bildet '{schluessel}' ab - kein "
                        f"Verb des Frontmatter-Vokabulars {list(vokabular)}. Eine "
                        f"Quelle des Kerns kann es nicht schreiben, die Abbildung "
                        f"laeuft also ins Leere (D-78)")
            for verb in vokabular:
                hat = verb in abbildung
                erklaert_hier = verb in erklaert
                if hat and erklaert_hier:
                    err(f"{rel}: {block} bildet das Verb '{verb}' ab UND erklaert es "
                        f"zugleich fuer nicht abgebildet. Beides zugleich geht nicht - "
                        f"eine der beiden Aussagen ist falsch (D-78)")
                elif not hat and not erklaert_hier:
                    err(f"{rel}: {block}.tool_names kennt das Werkzeugverb '{verb}' "
                        f"nicht, und tool_names_unmapped erklaert die Abwesenheit "
                        f"nicht. Bis 0.39.0 wurde das Verb dann WOERTLICH als "
                        f"Werkzeugname durchgereicht; eine Luecke allein ist keine "
                        f"Aussage (D-78)")

            # Gegenstand 3: Die Sperrliste darf nicht enger sein als die Vorabfreigabe.
            #
            # Die Regel vergleicht zwei Listen und setzt damit voraus, dass sie
            # DENSELBEN Namensraum fuehren. Bei claude-code tun sie das; bei
            # devin-desktop nicht, und das ist gemessen (2026-09-14, D-88): Sein
            # Frontmatter kennt ein eigenes, normalisiertes Vokabular - read,
            # grep, glob, edit, exec, web_search -, waehrend seine Laufzeit das
            # glob-foermige Werkzeug find_file_by_name nennt. Ein Vergleich der
            # beiden Listen meldete dann einen Unterschied, den es nicht gibt.
            #
            # Ein Pack sagt das mit tool_names_namespace: 'eigen'. WAS DABEI
            # VERLOREN GEHT, gehoert gesagt: Fuer ein solches Pack prueft niemand
            # mehr, ob die Sperre die Vorabfreigabe deckt - die Frage von D-80
            # bleibt dort offen und ist nur anders gestellt, nicht beantwortet.
            if str(fmt.get("tool_names_namespace") or "") == "eigen":
                if not str(fmt.get("_tool_names_note") or "").strip():
                    err(f"{rel}: {block}.tool_names_namespace ist 'eigen', aber "
                        f"'_tool_names_note' fehlt oder ist leer. Einen eigenen "
                        f"Namensraum zu erklaeren nimmt die Richtungsregel von "
                        f"D-80 ausser Kraft - das gehoert begruendet, nicht "
                        f"bloss eingetragen (D-88)")
                continue
            for verb in sorted(abbildung):
                ziel = bruecke.get(verb)
                if ziel is None or ziel not in hook:
                    continue
                vorab = {str(x) for x in (abbildung.get(verb) or [])}
                sperre = {str(x) for x in (hook.get(ziel) or [])}
                zuviel = sorted(vorab - sperre)
                if zuviel:
                    err(f"{rel}: {block}.tool_names['{verb}'] gibt {zuviel} vorab "
                        f"frei, hook_tools['{ziel}'] fuehrt sie nicht. Die Sperrliste "
                        f"ist damit enger als die Vorabfreigabe: Ein Skill, der "
                        f"'{verb}' freigibt und '{verb}' sperrt, bekaeme ein Werkzeug "
                        f"freigegeben, das die Sperre nicht erfasst. Die umgekehrte "
                        f"Abweichung ist zulaessig (D-80)")
    if not gesehen:
        err(f"{KERN}/clients: kein Manifest gefunden. Pruefung 38 misst die "
            f"Werkzeugabbildungen der Packs; ohne sie prueft sie nichts und bestuende "
            f"leise (D-23)")

    # Gegenstand 4: die Quellen selbst.
    quellen = _quelldateien(root)
    if not quellen:
        err(f"{KERN}/framework: keine Quelle mit Frontmatter gefunden. Pruefung 38 "
            f"misst die Verben der ausgelieferten Skills und Agentenprofile; ohne sie "
            f"prueft der vierte Gegenstand nichts und bestuende leise (D-23)")
        return
    for rel, text in quellen:
        erlaubt, verboten = _frontmatter_verben(text)
        for feld, verben in (("allowed-tools", erlaubt), ("permissions.deny", verboten)):
            for verb in verben:
                if verb not in vokabular:
                    err(f"{rel}: {feld} nennt das Verb '{verb}' - das Vokabular des "
                        f"Frontmatters kennt nur {list(vokabular)}. In allowed-tools "
                        f"wurde es bis 0.39.0 woertlich als Werkzeugname "
                        f"durchgereicht, in permissions.deny fiel es lautlos aus "
                        f"(D-78, D-79)")



# ---------------------------------------------------------------------------
# Pruefung 39: Die Vorabfreigabe des Skillaufrufs deckt sich mit den ausgelieferten
# Skills, und die Skillwahl steht an allen vier Traegern (CR-2026-063, D-81 bis D-84).
#
# ANLASS. Die Wurzel-Anweisungsdatei fordert seit jeher, fuer Standardaufgaben die
# Skills zu nutzen - und die ausgelieferte Berechtigungsdatei kannte das Werkzeug, mit
# dem das geht, in KEINEM Korb. Gemessen am 2026-09-14
# (tests/protocols/2026-09-14-erhebung-skillaufruf.md): Der Aufruf wurde abgewiesen, die
# Sitzung las die SKILL.md ersatzweise als Datei, und die Ausgabe sah aus wie ein
# gelungener Lauf. Die Ursache lag nicht im Pack, sondern im Vokabular der Kernquelle -
# sechs Verben, keines fuer den Skillaufruf.
#
# VIER GEGENSTAENDE:
#   1. Der verlorene Anker. Fehlt das Skillverzeichnis des Kerns oder fuehrt
#      permissions.json keine einzige skill-Regel, meldet diese Pruefung das selbst -
#      sonst bestuende sie leise (D-23).
#   2. Die Deckung in BEIDE Richtungen. Jeder ausgelieferte Skill hat genau eine
#      allow-Regel, und jede Regel nennt einen ausgelieferten Skill. Das ist der Preis
#      von D-81 E3: Die Regeln stehen in der Datei, statt aus dem Verzeichnis erzeugt zu
#      werden - nach D-53 IST der Inhalt dieser Datei die Berechtigung. Ohne diese
#      Pruefung waere das die zweite Liste fuer dieselbe Sache, also der Befundtyp von
#      CR-2026-062.
#   3. Kein Musterzeichen. Gemessen am 2026-09-14 (D-82): Der Vergleich ist woertlich.
#      Skill(fw-*) weist den Aufruf ab, Skill(fw-code-explain) laesst ihn durch,
#      Skill(fw-plan) weist fw-code-explain ab (Kontrolllauf). Eine Regel mit * oder ?
#      saehe richtig aus und gaebe LAUTLOS NICHTS frei - die Bauform von D-66 mit
#      umgekehrtem Vorzeichen.
#   4. Die vier Regeltraeger. Die Skillwahl stand vor 0.41.0 an fuenf Stellen und
#      erreichte den Agenten an keiner verbindlich. Sie steht jetzt in der
#      Wurzel-Anweisungsdatei, in der always-on-Kurzfassung, im Arbeitsmodell und in den
#      Prompting-Regeln. Geprueft wird die ANWESENHEIT je Traeger, nicht der Wortlaut:
#      Eine Pruefung, die Prosa vergleicht, bricht bei jeder Umformulierung.
#
# WAS SIE HEUTE FAENGT: nichts - Gegenstand 2 und 3 sind mit demselben Release entstanden
# und passen per Konstruktion zu sich selbst; Gegenstand 4 ebenso. Das ist die Lage von
# Pruefung 37 und dieselbe Ehrlichkeit: Der Gegenbeweis gegen den Vorstand ist hier eine
# KONSTRUKTION, kein Abzaehlen, und was die Pruefung wert ist, haengt an ihren Sonden.
#
# WAS SIE NICHT LEISTET: Sie belegt nicht, dass der Agent den Skill waehlt. Das ist ein
# Sitzungstest, und er ist nicht gefahren. Sie belegt, dass die Freigabe zur Skillmenge
# passt und dass keiner der vier Traeger die Regel verliert.
SKILLWAHL_TRAEGER = (
    ("framework/runtime/root-instruction.md",
     "Bevor du einen Schritt beginnst"),
    ("framework/runtime/rules/00-framework-core.md",
     "Skillwahl vor dem Schritt"),
    ("framework/core/05-working-model.md",
     "ist er der vorgesehene Weg des Schrittes"),
    ("framework/core/06-prompting-rules.md",
     "Skills bevorzugen \u2013 von beiden Seiten"),
)


def _skill_regeln(root: str) -> list[str] | None:
    """Die Aufrufnamen aus den skill-Regeln der Kernquelle, oder None ohne Quelle."""
    pfad = os.path.join(root, KERN, "framework", "runtime", "permissions.json")
    if not os.path.exists(pfad):
        return None
    try:
        quelle = json.loads(read(pfad))
    except json.JSONDecodeError:
        return None
    return [r.get("pattern", "") for r in quelle.get("allow", [])
            if isinstance(r, dict) and r.get("tool") == "skill"]


def check_skillfreigabe(root: str) -> None:
    """Pruefung 39 (D-81 bis D-84): Freigabe, Skillmenge und Regeltraeger decken sich."""
    verzeichnis = os.path.join(root, KERN, "framework", "skills")
    if not os.path.isdir(verzeichnis):
        err(f"{KERN}/framework/skills: fehlt. Pruefung 39 misst die Vorabfreigabe des "
            f"Skillaufrufs gegen die ausgelieferten Skills; ohne das Verzeichnis "
            f"prueft sie nichts und bestuende leise (D-23)")
        return
    ausgeliefert = sorted(
        name for name in os.listdir(verzeichnis)
        if os.path.isfile(os.path.join(verzeichnis, name, "SKILL.md")))

    regeln = _skill_regeln(root)
    if regeln is None:
        err(f"{KERN}/framework/runtime/permissions.json: nicht lesbar. Pruefung 39 hat "
            f"ihren Anker verloren und bestuende sonst leise (D-23)")
        return
    if not regeln:
        err(f"{KERN}/framework/runtime/permissions.json: keine einzige allow-Regel mit "
            f"dem Verb 'skill'. Die Wurzel-Anweisungsdatei fordert in Abschnitt 17 die "
            f"Nutzung der Skills; ohne Freigabe laeuft jeder Aufruf in die Rueckfrage "
            f"und im rueckfragefreien Betrieb in die Abweisung (D-81)")
        return

    # Gegenstand 2: die Deckung, in beide Richtungen.
    for name in ausgeliefert:
        if name not in regeln:
            err(f"{KERN}/framework/runtime/permissions.json: der ausgelieferte Skill "
                f"'{name}' hat keine allow-Regel. Sein Aufruf laeuft in die Rueckfrage, "
                f"und der Fehlschlag ist stumm - die Sitzung liest die SKILL.md "
                f"ersatzweise als Datei, ohne die Werkzeugbeschraenkung des Skills "
                f"(D-81, D-83)")
    for name in regeln:
        if name not in ausgeliefert:
            err(f"{KERN}/framework/runtime/permissions.json: die allow-Regel fuer "
                f"'{name}' nennt keinen ausgelieferten Skill. Eine Vorabfreigabe fuer "
                f"einen Skill, den es nicht gibt, ist eine Zusage ohne Gegenstand "
                f"(D-81)")
    doppelt = sorted({n for n in regeln if regeln.count(n) > 1})
    if doppelt:
        err(f"{KERN}/framework/runtime/permissions.json: doppelte skill-Regel(n) fuer "
            f"{', '.join(doppelt)}")

    # Gegenstand 3: kein Musterzeichen.
    for name in regeln:
        if any(z in name for z in "*?["):
            err(f"{KERN}/framework/runtime/permissions.json: die skill-Regel '{name}' "
                f"traegt ein Musterzeichen. Der Vergleich ist woertlich - gemessen am "
                f"2026-09-14 (D-82): Skill(fw-*) weist den Aufruf ab. Eine Regel mit "
                f"Muster saehe richtig aus und gaebe lautlos nichts frei")

    # Gegenstand 4: die vier Regeltraeger.
    for rel, anker in SKILLWAHL_TRAEGER:
        pfad = os.path.join(root, KERN, *rel.split("/"))
        if not os.path.exists(pfad):
            err(f"{KERN}/{rel}: fehlt. Pruefung 39 misst dort die Skillwahl (D-84)")
            continue
        if anker not in read(pfad):
            err(f"{KERN}/{rel}: die Skillwahl fehlt (gesucht: '{anker}'). Sie stand vor "
                f"0.41.0 an fuenf Stellen und erreichte den Agenten an keiner "
                f"verbindlich; faellt ein Traeger weg, faellt sie leise zurueck (D-84)")


# ---------------------------------------------------------------------------
# Pruefung 40: Die Register des Pruefapparats werden nachgezaehlt
# ---------------------------------------------------------------------------
#
# ANLASS. Gemessen am 2026-09-14 (tests/protocols/2026-09-14-gegenpruefung-pruefregister.md,
# CR-2026-064): FUENF Aussagen ueber den eigenen Pruefstand, keine davon richtig. Das
# Register im Kopfkommentar dieser Datei fuehrte die Pruefungen 1 bis 38, waehrend 39
# lief; der Satz zum Wirkungsnachweis nannte "18 bis 30"; der Kopfsatz des Sondenskripts
# war eine Release-Chronik, die bei 0.29.0 endete; FW-KO-01 nannte "6, 18 bis 31" und
# FW-KO-05 zwoelf Grenzfaelle, wo es zwanzig sind. KEINE der fuenf war falsch
# geschrieben - alle fuenf waren bei ihrer Einfuehrung richtig und sind stehen geblieben,
# waehrend ihr Gegenstand wuchs. In zehn von zwoelf Releases hat sich mindestens eine der
# drei Zahlen bewegt; deshalb ist die Behebung eine Pruefung und keine Textaenderung.
#
# VIER GEGENSTAENDE:
#   1. Der verlorene Anker. Fuenf Ankertexte in vier Dateien. Geht einer verloren,
#      bestuende diese Pruefung leise - sie meldet sein Fehlen deshalb selbst (D-23).
#   2. Das Register ist lueckenlos von 1 bis zu seiner hoechsten Nummer, und diese
#      hoechste Nummer ist die hoechste, die in den beiden Pruefskripten ueberhaupt
#      genannt wird. In beide Richtungen: eine Pruefung ohne Eintrag ist ein Fehler, ein
#      Eintrag ohne Nennung im Code auch.
#   3. Die Sondenmenge steht an DREI Stellen in derselben, ausgerechneten Schreibweise -
#      im Satz unter dem Register, im Kopfsatz von probe-pruefungen.py und in der
#      Pruefmittelspalte von FW-KO-01. Der Vergleich ist woertlich, und die Fehlermeldung
#      nennt die richtige Zeichenkette (D-86).
#   4. Die Grenzfallanzahl in FW-KO-05 ist die gezaehlte. Pruefung 30 rechnet sie
#      INNERHALB von EDGE_CASES.md nach; ausserhalb nennt sie nur dieses Testblatt, und
#      dort als Arbeitsanweisung: Wer FW-KO-05 heute faehrt, prueft zwoelf von zwanzig
#      Grenzfaellen und meldet ihn bestanden.
#
# WARUM NICHT DIE KOPFKOMMENTARE ALS ANKER (CR-2026-064 E2). Gemessen tragen sie drei
# Formen - "# Pruefung N:", "# N:" und "# Pruefungen N bis M" -, und eine vierte sieht
# aus wie ein Kopf und ist keiner: "# Pruefung 37 und dieselbe Ehrlichkeit ..." im Block
# von Pruefung 39. Der erste Entwurf dieser Pruefung ist genau daran gefallen und hat
# Pruefung 37 gefunden, wo kein Kopf stand.
#
# WARUM NUR TEST_CATALOG.md UND NICHT DAS GANZE REPOSITORIUM (D-86). docs/ROADMAP.md,
# CR-2026-052 und der Wirkungsnachweis zu 0.32.0 nennen ebenfalls zwoelf Grenzfaelle -
# und sind RICHTIG, weil sie den Stand von 0.32.0 beschreiben. Eine Nennung in der
# Vorgeschichte ist kein Register, und wer sie mitzieht, macht aus einer richtigen Zeile
# eine falsche.
#
# GRENZE. Sie zaehlt NENNUNGEN, nicht Pruefungen: Wer eine Pruefung baut und ihre Nummer
# nirgends schreibt, wird nicht gefangen - dieselbe Ehrlichkeit wie Gegenstand 2 von
# Pruefung 38, der Deklarationen zaehlt und nicht Richtigkeit. Und sie belegt die
# VOLLSTAENDIGKEIT des Registers, nicht die Richtigkeit seiner Eintraege: Ein Eintrag,
# der etwas anderes beschreibt als seine Pruefung tut, laeuft durch.
REGISTER_ANKER = "Prüft (statisch, ohne laufenden KI-Client):"
REGISTER_ENDE = "Der Wirksamkeitsnachweis nach D-23"
NACHWEIS_SATZ = "Der Wirksamkeitsnachweis nach D-23 fuer die Pruefungen {} laeuft"
SONDEN_SATZ = "Wirkungsnachweis nach D-23 fuer die Pruefungen {}"
KATALOG_SPANNE = "für die Prüfungen {} als Skript"
KATALOG_GRENZFAELLE = "Die {} Grenzfälle einzeln"
REGISTER_DATEIEN = ("tests/scripts/validate-framework.py",
                    "tests/scripts/probe-pruefungen.py",
                    "tests/TEST_CATALOG.md",
                    "tests/EDGE_CASES.md")


def nummernspanne(zahlen) -> str:
    """Kanonische Schreibweise einer Nummernmenge: '6 und 18 bis 40'.

    Eine einzelne Nummer steht allein, eine luckenlose Folge als 'a bis b', mehrere
    Bloecke durch Komma und ein abschliessendes 'und' getrennt. Diese Funktion ist die
    einzige Quelle der Schreibweise; die drei Traeger vergleichen woertlich gegen sie.
    """
    folge = sorted(zahlen)
    bloecke, lauf = [], [folge[0]]
    for z in folge[1:]:
        if z == lauf[-1] + 1:
            lauf.append(z)
        else:
            bloecke.append(lauf)
            lauf = [z]
    bloecke.append(lauf)
    teile = [str(b[0]) if len(b) == 1 else f"{b[0]} bis {b[-1]}" for b in bloecke]
    if len(teile) == 1:
        return teile[0]
    return ", ".join(teile[:-1]) + " und " + teile[-1]


def genannte_pruefungen(*texte: str) -> set:
    """Jede Pruefungsnummer, die ein Text als 'Pruefung N' oder 'Pruefungen N bis M' nennt.

    Der Zuschnitt ist Absicht (CR-2026-064 E2): Ein Querverweis auf eine kleinere Nummer
    stoert nicht, weil nur die hoechste zaehlt - und eine neue Pruefung nennt ihre Nummer
    zwangslaeufig, spaetestens in ihrem eigenen Kopfkommentar.
    """
    gefunden = set()
    muster = re.compile(r"Pr[uü]efung(?:en)?\s+(\d+(?:\s*(?:,|und|bis)\s*\d+)*)")
    for text in texte:
        for treffer in muster.finditer(text):
            teile = re.split(r"\s*(,|und|bis)\s*", treffer.group(1))
            for i, teil in enumerate(teile):
                if teil == "bis" and 0 < i < len(teile) - 1:
                    gefunden |= set(range(int(teile[i - 1]), int(teile[i + 1]) + 1))
                elif teil.isdigit():
                    gefunden.add(int(teil))
    return gefunden


def check_pruefregister(root: str) -> None:
    """Pruefung 40 (D-85, D-86): Register und Bestand des Pruefapparats decken sich."""
    texte = {}
    for rel in REGISTER_DATEIEN:
        pfad = os.path.join(root, KERN, *rel.split("/"))
        if not os.path.exists(pfad):
            err(f"{KERN}/{rel}: fehlt. Prüfung 40 hält dort das Register des "
                f"Prüfapparats gegen den Bestand (D-85)")
            return
        texte[rel] = read(pfad)
    validator = texte["tests/scripts/validate-framework.py"]
    sonden = texte["tests/scripts/probe-pruefungen.py"]
    katalog = texte["tests/TEST_CATALOG.md"]
    kanten = texte["tests/EDGE_CASES.md"]

    # --- Gegenstand 1: die Anker ------------------------------------------------------
    doc = validator.split('"""')[1] if validator.count('"""') >= 2 else ""
    sondendoc = sonden.split('"""')[1] if sonden.count('"""') >= 2 else ""
    if REGISTER_ANKER not in doc or REGISTER_ENDE not in doc:
        err(f"{KERN}/tests/scripts/validate-framework.py: der Kopfkommentar führt kein "
            f"Register mehr (gesucht: '{REGISTER_ANKER}' und '{REGISTER_ENDE}') – "
            f"Prüfung 40 hat ihren Gegenstand verloren und würde sonst leise bestehen")
        return
    fwko01 = [z for z in katalog.splitlines() if z.startswith("| FW-KO-01")]
    fwko05 = [z for z in katalog.splitlines() if z.startswith("| FW-KO-05")]
    if len(fwko01) != 1 or len(fwko05) != 1:
        err(f"{KERN}/tests/TEST_CATALOG.md: die Zeile FW-KO-01 oder FW-KO-05 steht nicht "
            f"genau einmal (gefunden: {len(fwko01)} und {len(fwko05)}) – Prüfung 40 misst "
            f"dort die Sondenmenge und die Grenzfallanzahl (D-85)")
        return

    # --- Gegenstand 2: das Register ist lueckenlos und vollstaendig --------------------
    liste = doc.split(REGISTER_ANKER, 1)[1].split(REGISTER_ENDE, 1)[0]
    gefuehrt = sorted({int(n) for n in re.findall(r"^\s{0,2}(\d+)[a-z]?\. ", liste, re.M)})
    if not gefuehrt:
        err(f"{KERN}/tests/scripts/validate-framework.py: das Register im Kopfkommentar "
            f"führt keinen einzigen nummerierten Eintrag – Prüfung 40 hätte nichts zu "
            f"vergleichen und bestünde leise")
        return
    luecken = [n for n in range(1, gefuehrt[-1] + 1) if n not in gefuehrt]
    if luecken:
        err(f"{KERN}/tests/scripts/validate-framework.py: das Register im Kopfkommentar "
            f"hat Lücken – es fehlt {', '.join(str(n) for n in luecken)}. Eine Nummer "
            f"ohne Eintrag ist eine Prüfung, die niemand findet (D-85)")
    genannt = genannte_pruefungen(validator, sonden)
    hoechste = max(genannt) if genannt else 0
    if hoechste > gefuehrt[-1]:
        err(f"{KERN}/tests/scripts/validate-framework.py: das Register im Kopfkommentar "
            f"endet bei Prüfung {gefuehrt[-1]}; die Prüfskripte nennen Prüfung "
            f"{hoechste}. Eine neue Prüfung ohne Registereintrag ist genau der Fall vom "
            f"2026-09-14 – das Register ist die einzige Stelle, die sagt, was dieser "
            f"Lauf prüft (D-85)")
    elif hoechste and hoechste < gefuehrt[-1]:
        err(f"{KERN}/tests/scripts/validate-framework.py: das Register im Kopfkommentar "
            f"führt Prüfung {gefuehrt[-1]}; in den Prüfskripten wird sie nirgends bei "
            f"ihrer Nummer genannt. Ein Eintrag ohne Prüfung verspricht mehr, als der "
            f"Lauf leistet (D-85)")

    # --- Gegenstand 3: die Sondenmenge an drei Stellen, wortgleich ---------------------
    kennungen = (re.findall(r'\bsonde\("([^"]+)"', sonden)
                 + re.findall(r'melde\("SONDE", "([^"]+)"', sonden))
    mit_sonde = {int(m.group(1)) for m in (re.match(r"(\d+)", k) for k in kennungen) if m}
    if not mit_sonde:
        err(f"{KERN}/tests/scripts/probe-pruefungen.py: keine einzige Sonde mit einer "
            f"Prüfungsnummer gefunden – Prüfung 40 rechnet daraus die Sondenmenge aus "
            f"und hat ihren Gegenstand verloren")
        return
    spanne = nummernspanne(mit_sonde)
    for rel, text, soll in (
            ("tests/scripts/validate-framework.py", doc, NACHWEIS_SATZ.format(spanne)),
            ("tests/scripts/probe-pruefungen.py", sondendoc, SONDEN_SATZ.format(spanne)),
            ("tests/TEST_CATALOG.md", fwko01[0], KATALOG_SPANNE.format(spanne))):
        if soll not in text:
            err(f"{KERN}/{rel}: die Sondenmenge ist dort nicht in der ausgerechneten "
                f"Schreibweise genannt. Erwartet wörtlich: '{soll}'. "
                f"probe-pruefungen.py führt Sonden für die Prüfungen {spanne} – eine "
                f"gepflegte Zahl über den Prüfapparat lag am 2026-09-14 an allen drei "
                f"Stellen daneben (D-86)")

    # --- Gegenstand 4: die Grenzfallanzahl ausserhalb ihrer Quelle ---------------------
    grenzfaelle = set(re.findall(r"\bG-(\d\d)\b", kanten))
    if not grenzfaelle:
        err(f"{KERN}/tests/EDGE_CASES.md: keine einzige Grenzfallkennung der Form G-NN "
            f"gefunden – Prüfung 40 zählt sie dort und hat ihren Gegenstand verloren")
        return
    soll_gf = KATALOG_GRENZFAELLE.format(len(grenzfaelle))
    if soll_gf not in fwko05[0]:
        err(f"{KERN}/tests/TEST_CATALOG.md: FW-KO-05 nennt nicht die gezählte Anzahl der "
            f"Grenzfälle. Erwartet wörtlich: '{soll_gf}'. Die Zeile ist eine "
            f"Arbeitsanweisung für eine Sitzung; sie stand von 0.33.0 bis 0.41.0 auf "
            f"zwölf, während der Bestand auf zwanzig wuchs – wer sie so fährt, prüft "
            f"einen Teil und meldet das Ganze (D-86)")


# ---------------------------------------------------------------------------
# Pruefung 41: Eine Abwesenheitserklaerung ist Enthaltung oder Beleg
# ---------------------------------------------------------------------------
#
# ANLASS. D-47 wurde gebaut, damit ein Pack eine Werkzeugklasse nicht dadurch aus der
# Durchsetzung nehmen kann, dass es sie weglaesst: Eine Abwesenheit MUSS erklaert werden.
# Pruefung 26 erzwingt seither, dass die Erklaerung DA ist und mit permission_tools
# widerspruchsfrei. Am 2026-09-14 war beides erfuellt und die Erklaerung trotzdem falsch
# (tests/protocols/2026-09-14-erhebung-devin-werkzeuge.md, CR-2026-065):
# _hook_tools_absent_note sagte "Dieser Client fuehrt kein eigenes Suchwerkzeug" - und der
# Client fuehrt zwei, grep und find_file_by_name. Der erzeugte Hook-Matcher kannte die
# Suchklasse deshalb nicht, und in einer Umgebung mit nur diesem Hook kam derselbe
# Secret-Wert, den ein read-Aufruf nicht bekam, ueber einen grep-Aufruf woertlich heraus.
#
# WAS PRUEFBAR IST. Nicht die Wahrheit einer Aussage - das kann kein Skript. Wohl aber,
# ob die Aussage sich als das ausweist, was sie ist. Zwei Bauformen sind redlich:
#   * die ENTHALTUNG - "UNERHOBEN, nicht abwesend" (agent_start_tools_absent seit D-70);
#   * der BELEG - ein Datum UND eine Fundstelle unter tests/protocols/. Ein
#     blosses Wort wie "gemessen" genuegt nicht - "nicht gemessen" enthaelt es
#     auch, und genau diese Falle stand im Entwurf dieser Pruefung.
# Die dritte Bauform ist die, die hier Schaden angerichtet hat: eine BEHAUPTUNG, die wie
# eine Feststellung klingt und weder das eine noch das andere trägt.
#
# GRENZE. Sie prueft eine FORM, nicht eine Tatsache. Wer ein Datum und einen Protokollpfad
# in die Note schreibt, besteht sie - auch wenn das Protokoll etwas anderes sagt. Und sie
# faengt nach 0.43.0 nichts mehr: Beide Packs sind in Ordnung. Ihr Wert haengt an ihren
# Sonden und daran, dass die naechste Abwesenheitserklaerung nicht mehr unbelegt bleibt.
ABWESENHEITSFELDER = (
    ("hook_tools_absent", "_hook_tools_absent_note", None),
    ("agent_start_tools_absent", "_agent_start_tools_absent_note", None),
    ("tool_names_unmapped", "_tool_names_unmapped_note", FRONTMATTER_BLOECKE),
    ("skill_deny_unmapped", "_skill_deny_unmapped_note", ("skill_frontmatter",)),
)
ENTHALTUNG = re.compile(r"unerhoben", re.I)
DATUM = re.compile(r"\b20\d\d-\d\d-\d\d\b")
FUNDSTELLE = re.compile(r"tests/protocols/")


def _abwesenheitserklaerungen(man: dict):
    """(Feldname, Notizname, Wert, Notiz) je erklaerter Abwesenheit dieses Manifests."""
    for feld, notiz, bloecke in ABWESENHEITSFELDER:
        if bloecke is None:
            wert = man.get(feld)
            if wert:
                yield feld, notiz, wert, man.get(notiz)
            continue
        for block in bloecke:
            fmt = man.get(block) or {}
            wert = fmt.get(feld)
            if wert:
                yield f"{block}.{feld}", f"{block}.{notiz}", wert, fmt.get(notiz)


def check_abwesenheitsbeleg(root: str) -> None:
    """Pruefung 41 (D-88): Eine erklaerte Abwesenheit weist sich aus - oder sie belegt sich."""
    basis = os.path.join(root, KERN, "clients")
    if not os.path.isdir(basis):
        return
    manifeste = 0
    erklaerungen = 0
    for pack in sorted(os.listdir(basis)):
        if pack.startswith("_"):
            continue
        pfad = os.path.join(basis, pack, "manifest.json")
        if not os.path.isfile(pfad):
            continue
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        try:
            man = json.loads(read(pfad))
        except ValueError:
            continue
        manifeste += 1
        for feld, notizname, _wert, notiz in _abwesenheitserklaerungen(man):
            erklaerungen += 1
            text = str(notiz or "").strip()
            if not text:
                continue  # Die Pruefungen 26 und 38 melden die fehlende Notiz bereits
            if ENTHALTUNG.search(text):
                continue
            if DATUM.search(text) and FUNDSTELLE.search(text):
                continue
            err(f"{rel}: {notizname} erklärt eine Abwesenheit, weist sie aber weder als "
                f"Enthaltung aus noch belegt sie sie. Redlich sind zwei Bauformen: das "
                f"Wort 'unerhoben' – oder ein Datum zusammen mit einer Fundstelle "
                f"('tests/protocols/…'). Eine "
                f"Behauptung ohne beides nimmt eine Werkzeugklasse aus der Durchsetzung "
                f"und begründet es – genau so ist am 2026-09-14 der Schutz-Hook um die "
                f"Suchklasse gekommen (D-88)")
    if not manifeste:
        err(f"{KERN}/clients: kein Manifest gefunden. Prüfung 41 misst die "
            f"Abwesenheitserklärungen der Packs; ohne sie prüft sie nichts und bestünde "
            f"leise (D-23)")
        return
    if not erklaerungen:
        err(f"{KERN}/clients: kein Pack führt noch eine Abwesenheitserklärung. Prüfung "
            f"41 hat ihren Gegenstand verloren und würde leise bestehen – fällt das Feld "
            f"weg, gehört die Prüfung ausgebaut und nicht stillgelegt (D-23, D-88)")


# ---------------------------------------------------------------------------
# Pruefung 42: Ein gefuellter Schlitz traegt, was das Overlay erklaert
# ---------------------------------------------------------------------------
#
# ANLASS. Gemessen am 2026-09-14
# (tests/protocols/2026-09-14-gegenpruefung-schlitzdeckung.md, CR-2026-066): Die
# Kernquelle haelt im ask-Korb DREI Befehlsschlitze bereit. Pruefung 37 vergleicht
# Mengen und zaehlt den Ueberschuss gegen die Zahl der offenen Schlitze - WELCHER
# Eintrag WELCHER Schlitz ist, steht dort nicht und kann dort nicht stehen. Gemessen
# laufen deshalb drei beliebige Befehlsfreigaben durch, darunter eine mit Fernwirkung,
# und zwar in beiden Packs und auch dann, wenn das Overlay dreimal <TBD> sagt, also gar
# nichts erklaert. Am Piloten steht der Fall seit dem Heben auf 0.37.0:
# Bash(mvn -B -q compile) im ask-Korb, waehrend Abschnitt 6 <LINT_COMMAND> als "nicht
# vorhanden" erklaert.
#
# DIE LUECKE WAR ERKLAERT - AN EINER STELLE. CR-2026-061 Abschnitt 4 nimmt genau diesen
# Fall ausdruecklich aus, und D-76 wie D-77 bleiben genau. DREI ausgelieferte Texte aus
# DEMSELBEN Commit (34d850e, Release 0.39.0) taten es nicht: der Absatz zum Wirkungsort
# in templates/project-overlay/OVERLAY.md, der Kommentarkopf JEDER erzeugten
# Berechtigungsdatei in clientmap._kommentar und framework/core/03-security.md. Alle drei
# sind mit diesem Release berichtigt. Die Lehre ist die von 0.42.0, eine Ebene tiefer:
# Eine Enthaltung, die nur in einem Antrag steht, haelt nicht einmal bis zum Ende
# desselben Patches.
#
# WOHER DIE ZUORDNUNG KOMMT (CR-2026-066 E1). Es gibt sie genau einmal, im Overlay:
# Jeder der drei Platzhalter steht dort in genau EINER Tabellenzeile, und der Wert steht
# in der Zelle RECHTS DANEBEN - gemessen in allen vier geprueften Overlays, auch im
# Overlay des Piloten, dessen Abschnitt 6 aus einer aelteren Vorlage stammt und eine
# andere Spaltenueberschrift fuehrt. docs/PLACEHOLDER_REGISTRY.md weist die Herkunft
# ohnehin aus (Overlay 5 beziehungsweise Overlay 6); diese Pruefung setzt eine
# Behauptung durch, die das Register seit jeher macht. Die Zeile wird ueber die
# PLATZHALTERZELLE gefunden, nie ueber eine Spaltennummer - ein Overlay, das eine Spalte
# ergaenzt, bricht sie deshalb nicht.
#
# WARUM NICHT DIE LAUFZEITFASSUNG (E2). 20-project-overlay.md fuehrt dieselben drei
# Werte, aber in einer Fliesszeile ohne Schluesselspalte - und der Pilot hat sie bereits
# umgebaut (zwei Zeilen statt einer, ein zusaetzliches Feld). Eine Pruefung darueber
# fiele beim ersten echten Projekt an der FORM, nicht an der Sache.
#
# WARUM EINE EIGENE NUMMER (E6). Pruefung 37 haengt allein an der Kernquelle und laeuft
# ohne Overlay; diese hier enthaelt sich ohne Overlay. Zwei Gegenstaende, zwei Nummern -
# und 37 behaelt ihre Arithmetik, damit ihr Ergebnis nicht von der Anwesenheit eines
# Nachbardokuments abhaengt. Am Piloten meldet 37 deshalb weiterhin nichts, waehrend 42
# meldet.
#
# GRENZE, UND SIE STEHT HIER UND NICHT NUR IM ANTRAG (E5). Geprueft werden die drei
# BEFEHLSSCHLITZE. Die vier PFADSCHLITZE (<EXCLUDED_PATHS> zweimal, <CI_CONFIG_PATHS>,
# <QUALITY_GATE_CONFIG_PATHS>) bleiben ungeprueft: Sie stehen saemtlich im deny-Korb, wo
# Ueberzaehliges ohnehin zulaessig ist, und ihr Vergleich waere n:1 - eine Liste im
# Overlay gegen eine Regel in der Datei. Ein zu ENG gefuellter <EXCLUDED_PATHS>-Schlitz
# ist damit weiterhin eine stille Lockerung. Das ist eine Enthaltung, keine Stille.
#
# ZWEITE GRENZE. Diese Pruefung vergleicht Zeichenketten. Ob der erklaerte Befehl
# fachlich der richtige ist, ob er tut, was Abschnitt 6 von ihm behauptet, und ob ein
# Client die Regel so auswertet, wie sie gemeint ist, sagt sie nicht.
OVERLAY_QUELLE = "project-overlay/OVERLAY.md"
# Werte, die kein Befehl sind. Die Schreibweisen stammen aus der Vorlage und aus dem
# Overlay des Piloten; der Vergleich laeuft in Kleinschreibung und ohne umschliessende
# Auszeichnung. Ein Wert mit <TBD faellt ohnehin darunter.
KEIN_BEFEHL = ("nicht vorhanden", "nicht erforderlich", "keine", "keiner", "keines",
               "entfaellt", "entfällt", "nur in ci", "-", "–", "—", "")


def overlay_befehlswert(text: str, platzhalter: str) -> tuple:
    """Wie oft nennt eine Tabellenzeile den Platzhalter, und was steht rechts daneben?

    Rueckgabe (anzahl, wert). wert ist None, wenn die Zelle keinen Befehl traegt - ein
    offener <TBD>-Wert, ein "nicht vorhanden" oder ein Gedankenstrich. Steht in der Zelle
    ein Abschnitt zwischen Gegenstrichen, gilt dieser als der Wert; so ueberlebt die
    Auswertung einen erlaeuternden Zusatz hinter dem Befehl.
    """
    treffer = []
    for felder in _tabellenzeilen(text):
        for i, feld in enumerate(felder):
            if feld.strip("` *") == platzhalter and i + 1 < len(felder):
                treffer.append(felder[i + 1])
    if len(treffer) != 1:
        return len(treffer), None
    zelle = treffer[0]
    ausgezeichnet = re.search(r"`([^`]+)`", zelle)
    wert = (ausgezeichnet.group(1) if ausgezeichnet else zelle).strip(" *")
    if "<TBD" in wert or wert.strip().lower() in KEIN_BEFEHL:
        return 1, None
    return 1, wert


def check_schlitzinhalte(root: str, man: dict) -> None:
    """Pruefung 42 (D-90, D-91): Der Schlitz traegt den Befehl, den das Overlay erklaert.

    Enthaltung ohne Overlay: Eine Installation ohne project-overlay/OVERLAY.md ist ein
    zulaessiger Zustand (Kandidatenphase), und eine Pruefung, die ihn beanstandet, waere
    eine Pruefung ueber die Reihenfolge der Uebernahme. Fehlt dagegen ein PLATZHALTER in
    einem vorhandenen Overlay, ist das der verlorene Anker und ein Fehler (D-23).
    """
    overlay_pfad = os.path.join(root, "project-overlay", "OVERLAY.md")
    rel = man["permissions_file"]
    pfad = os.path.join(root, *rel.split("/"))
    if not os.path.exists(overlay_pfad) or not os.path.exists(pfad):
        return
    try:
        cfg = json.loads(read(pfad))
    except json.JSONDecodeError:
        return  # check_config hat das bereits gemeldet
    soll = soll_korbregeln(root, man)
    if soll is None:
        return
    overlay = read(overlay_pfad)
    perms = cfg.get("permissions", {})
    exec_werkzeuge = tuple(man.get("permission_tools", {}).get("exec", ()))
    if not exec_werkzeuge:
        return  # Ein Pack ohne Befehlswerkzeug hat keine Befehlsschlitze.

    for korb in ("ask", "allow"):
        ist = [r for r in perms.get(korb, []) if isinstance(r, str)]
        _, schlitze, _, zusatz = korb_zerlegung(ist, soll[korb])
        befehlsschlitze = [s for s in schlitze if s.split("(", 1)[0] in exec_werkzeuge]
        if not befehlsschlitze:
            continue
        erklaert: dict = {}
        ohne_befehl: list = []
        for schlitz in befehlsschlitze:
            namen = PROJEKTPLATZHALTER.findall(schlitz)
            if len(namen) != 1:
                continue
            platzhalter = namen[0]
            anzahl, wert = overlay_befehlswert(overlay, platzhalter)
            if anzahl == 0:
                err(f"{OVERLAY_QUELLE}: keine Tabellenzeile nennt {platzhalter} – "
                    f"Prüfung 42 liest dort den Befehl, den dieser Schlitz der "
                    f"Berechtigungsdatei tragen darf, und hat ihren Gegenstand verloren. "
                    f"Der Platzhalter gehört in die Platzhalterspalte von Abschnitt 5 "
                    f"oder 6, der Befehl in die Zelle rechts daneben (D-91)")
                continue
            if anzahl > 1:
                err(f"{OVERLAY_QUELLE}: {anzahl} Tabellenzeilen nennen {platzhalter}. "
                    f"Prüfung 42 braucht genau eine – bei mehreren ist nicht "
                    f"entschieden, welcher Befehl für den Schlitz gilt (D-91)")
                continue
            if wert is None:
                ohne_befehl.append(platzhalter)
                continue  # Kein erklaerter Befehl: Dieser Schlitz deckt nichts.
            regel = schlitz.replace(platzhalter, wert)
            erklaert[regel] = platzhalter
            if regel in ist:
                continue
            if schlitz in ist:
                err(f"{rel}: das Overlay erklärt für {platzhalter} den Befehl "
                    f"'{wert}'; der {korb}-Korb trägt aber noch den offenen Schlitz "
                    f"'{schlitz}'. Entweder wird der Wert dort eingetragen ('{regel}'), "
                    f"oder Abschnitt 5 beziehungsweise 6 nimmt ihn zurück – zwei "
                    f"Träger derselben Freigabe dürfen nicht auseinanderlaufen "
                    f"(D-90)")
            else:
                err(f"{rel}: das Overlay erklärt für {platzhalter} den Befehl "
                    f"'{wert}'; der {korb}-Korb trägt weder '{regel}' noch den offenen "
                    f"Schlitz '{schlitz}'. Eine erklärte Freigabe, die die Datei nicht "
                    f"gewährt, ist eine Abweichung – gleich in welche Richtung sie "
                    f"aufgelöst wird (D-90)")
        for regel in zusatz:
            if regel.split("(", 1)[0] not in exec_werkzeuge:
                continue
            if regel in erklaert:
                continue
            err(f"{rel}: '{regel}' steht im {korb}-Korb, und kein Platzhalter des "
                f"Overlays erklärt diesen Befehl. Ein Platzhalterschlitz darf gefüllt "
                f"sein – aber mit dem Wert, den Abschnitt 5 oder 6 für ihn nennt. Ohne "
                f"erklärten Befehl deckt ein Schlitz keine zusätzliche Freigabe; ohne "
                f"diesen Satz decken drei offene Schlitze drei beliebige Befehle, gemessen "
                f"bis hin zu einem mit Fernwirkung (D-90). Ohne erklärten Befehl sind "
                f"hier: {', '.join(ohne_befehl) if ohne_befehl else 'keiner'}")


# ---------------------------------------------------------------------------
# Pruefung 43: Wo ein Pack seine Hooks fuehrt, stehen sie auch
# ---------------------------------------------------------------------------
#
# ANLASS. Gemessen am 2026-09-14 beim Herrichten des Uebungsrepositoriums
# (tests/protocols/2026-09-15-herrichtung-uebungsrepositorium.md, CR-2026-067): Seine
# Berechtigungsdatei trug KEINEN hooks-Block. Die Hooks des Projekts standen in
# .devin/hooks.v1.json - der Datei, aus der dieser Client keinen Hook ausfuehrt
# (AP2-DD-10, D-32, seit 0.25.0). Der Hook war damit seit der Erstinstallation
# wirkungslos, EINUNDDREISSIG Releases lang, und der Validator meldete durchgehend
# 0 Fehler.
#
# GEMESSEN, NICHT GESCHLOSSEN. In einer frischen 0.44.0-Installation wurde der Block
# entfernt und der Lauf wiederholt: mit Block 2 Fehler, ohne Block DIESELBEN 2 Fehler
# (beide Artefakte der Testinstallation). Kein Lauf sieht das Fehlen.
#
# WARUM DAS SCHWERER WIEGT ALS EINE VERWAISTE DATEI. Bei beiden ausgelieferten Packs ist
# dieser Hook die einzige technische Schranke, die eine Werkzeugeingabe prueft, bevor sie
# wirkt - Secrets nach 02-privacy.md und Schreibzugriffe auf den Kern ueber Werkzeuge, die
# die Berechtigungsdatei nicht erfasst. Die Berechtigungsdatei steht in shared_seed und
# wird nach der Erstinstallation nie wieder geschrieben (D-76): Ein Projekt, das den Block
# einmal nicht hat, bekommt ihn durch kein Update.
#
# UND PRUEFUNG 18 BESCHRIEB DIE HALBE MIGRATION. Ihre Warnung sagt, die verwaiste Datei
# sei von Hand zu loeschen. Wer ihr woertlich folgt und sonst nichts tut, hat danach GAR
# KEINEN Hook mehr. Ihre Meldung nennt seit diesem Release beide Haelften; nachgezaehlt
# wird die zweite hier.
#
# ENTHALTUNG (CR-2026-067 E3). Geprueft wird nur ein Pack, das seine Hooks in der
# Berechtigungsdatei fuehrt - erkennbar daran, dass <HOOKS_FILE> und permissions_file auf
# dieselbe Datei zeigen. Beide ausgelieferten Packs tun das; ein kuenftiges Pack mit
# eigener Hook-Datei bleibt ungeprueft. Dieselbe Bedingung hat Pruefung 18.
#
# GRENZE (E2). Geprueft wird das VORHANDENSEIN eines nichtleeren PreToolUse-Blocks, nicht
# sein Inhalt. Den pruefen 15 (Interpreter), 16 (Werkzeugabdeckung) und 17 (fail-closed) -
# sie greifen, sobald der Block da ist. Ein Block, der auf ein fremdes Skript zeigt, laeuft
# durch DIESE Pruefung und wird von 15 gefangen.


def check_hookblock(root: str, man: dict) -> None:
    """Pruefung 43 (D-92): Die Berechtigungsdatei traegt den Hook, den das Pack dort fuehrt."""
    rel = man.get("permissions_file")
    hooks_ort = (man.get("runtime_placeholders") or {}).get("<HOOKS_FILE>")
    if not rel or hooks_ort != rel:
        return  # Pack mit eigener Hook-Datei - Enthaltung (E3)
    pfad = os.path.join(root, *rel.split("/"))
    if not os.path.exists(pfad):
        return  # check_required meldet die fehlende Datei bereits
    try:
        daten = json.loads(read(pfad))
    except json.JSONDecodeError:
        return  # check_config hat das bereits gemeldet
    hooks = daten.get("hooks")
    eintraege = hooks.get("PreToolUse") if isinstance(hooks, dict) else None
    kommandos = [h for e in (eintraege or []) if isinstance(e, dict)
                 for h in (e.get("hooks") or []) if isinstance(h, dict) and h.get("command")]
    if kommandos:
        return

    runtime = (man.get("runtime_placeholders") or {}).get("<RUNTIME_DIR>") or ""
    verwaist = [n for n in VERWAISTE_HOOK_DATEIEN
                if runtime and os.path.exists(os.path.join(root, *runtime.split("/"), n))]
    daneben = (f" Daneben liegt {runtime}/{verwaist[0]}: Dort steht eine Regelmenge, die "
               f"aussieht, als gälte sie – der Client liest diese Datei nicht (D-32)."
               if verwaist else "")
    fehlt = "trägt keinen 'hooks'-Block" if not isinstance(hooks, dict) else \
            "trägt einen 'hooks'-Block ohne ein einziges PreToolUse-Kommando"
    err(f"{rel}: {fehlt}. Dieses Pack führt seine Hooks in der Berechtigungsdatei, und "
        f"dieser Hook ist seine einzige technische Schranke vor dem Werkzeugaufruf – "
        f"Secrets in der Eingabe und Schreibzugriffe auf den Kern über Wege, welche die "
        f"Berechtigungsregeln nicht erfassen.{daneben} Die Datei wird nach der "
        f"Erstinstallation nie wieder geschrieben (D-76): Der Block kommt durch kein "
        f"Update nach, er ist von Hand aus einer frischen Installation zu übernehmen "
        f"(D-92)")


# ---------------------------------------------------------------------------
# Pruefung 44: Das Register der Uebungspraeparationen und die Vorbedingungen des
# Testkatalogs decken sich
# ---------------------------------------------------------------------------
#
# ANLASS. Gemessen am 2026-09-14 (CR-2026-067, Befund 2): onboarding/exercises/README.md
# verlangte DREI Koeder. Abgezaehlt gegen die Vorbedingungen des Testkatalogs braucht ein
# fahrbares Uebungsrepositorium SIEBEN Praeparationen fuer NEUN Testfaelle - dazu eine
# .env-Testdatei (FW-DS-02), einen praeparierten Codekommentar (FW-PI-02), eine Injektion
# in einer Testdatei (SK-006-N04) und einen Regeltext mit bewusstem Widerspruch
# (FW-KO-03). Keine der vier stand in der Liste, und der Katalog fuehrte alle neun Faelle
# als 'offen', also als fahrbar. EINE ZUSAGE OHNE DEN MECHANISMUS DAHINTER - der
# wiederkehrende Befundtyp dieses Projekts, diesmal an seinem eigenen Pruefstand.
#
# WIE DIE ZUORDNUNG ENTSTEHT (E5). Jede Praeparation traegt eine Kennung UEB-NN. Sie steht
# im Register in der ersten Spalte und in der Vorbedingungszelle jedes Testfalls, der sie
# braucht. Der Vergleich laeuft ueber die Kennung und ist damit exakt - nicht ueber
# Stichwoerter wie "Koeder" oder "praepariert", die Pruefung 29 als Bauform schon einmal
# teuer bezahlt hat: Sie erkennt nur bekannte Bedingungswoerter.
#
# WARUM UEB- UND NICHT P1 (E5). P1 und P3 sind im Kern als Prinzipienkennungen vergeben
# (framework/core/05-working-model.md). Eine zweite Bedeutung desselben Zeichens in
# derselben Dokumentfamilie ist ein Fehler, den dieses Projekt schon gemacht hat: Am
# 2026-09-13 trug eine Gegenprobe die synthetische Kennung G-18 - dieselbe, die 0.36.0
# wirklich vergeben hat.
#
# BEIDE RICHTUNGEN (E6). Eine Kennung im Katalog ohne Registereintrag ist ein Tippfehler
# oder eine unregistrierte Praeparation; eine Kennung im Register, die kein Testfall
# braucht, ist eine tote Praeparation, die jemand pflegt. Die dezentralen TESTS.md zaehlen
# mit - Verfahren Nr. 6 des Katalogs erklaert sie zu seinem Teil.
#
# GRENZE, UND SIE IST DIE WICHTIGE. Diese Pruefung faengt NICHT den Fall, der sie
# ausgeloest hat: einen Testfall, der eine Praeparation braucht und keine Kennung nennt.
# Sie verhindert seine WIEDERHOLUNG nur, soweit die Kennung gesetzt wird - dieselbe
# Ehrlichkeit wie Gegenstand 2 von Pruefung 38 (er zaehlt Deklarationen, nicht
# Richtigkeit) und wie Pruefung 40 (sie zaehlt Nennungen, nicht Pruefungen).
#
# ZWEITE GRENZE. Sie gleicht zwei Register ab, nicht ein Register gegen die Wirklichkeit.
# Ob die Praeparation UEB-02 im Uebungsrepositorium wirklich liegt, kann kein Validator
# DIESES Repositoriums feststellen: Das Uebungsrepositorium liegt ausserhalb. Das ist eine
# Enthaltung, keine Stille.
UEB_REGISTER = "onboarding/exercises/README.md"
UEB_ANKER = "### Register der Präparationen"
UEB_KENNUNG = re.compile(r"\bUEB-\d{2}\b")


def _ueb_katalogdateien(root: str) -> list:
    """Der Testkatalog und die dezentralen Testblaetter je Skill (Verfahren Nr. 6)."""
    treffer = [os.path.join(KERN, "tests", "TEST_CATALOG.md")]
    basis = os.path.join(root, KERN, "framework")
    for dirpath, dirnames, filenames in os.walk(basis):
        dirnames[:] = sorted(d for d in dirnames if d != "__pycache__")
        if "TESTS.md" in filenames:
            treffer.append(os.path.relpath(os.path.join(dirpath, "TESTS.md"), root))
    return sorted(treffer)


def check_praeparationsregister(root: str) -> None:
    """Pruefung 44 (D-93): Registrierte Praeparationen und gebrauchte decken sich."""
    pfad = os.path.join(root, KERN, *UEB_REGISTER.split("/"))
    if not os.path.exists(pfad):
        err(f"{KERN}/{UEB_REGISTER}: fehlt. Prüfung 44 hält dort das Register der "
            f"Übungspräparationen gegen die Vorbedingungen des Testkatalogs (D-93)")
        return
    text = read(pfad)
    if UEB_ANKER not in text:
        err(f"{KERN}/{UEB_REGISTER}: führt kein Register mehr (gesucht: "
            f"'{UEB_ANKER}'). Prüfung 44 hat ihren Gegenstand verloren und bestünde "
            f"sonst leise – die Überschrift ist Teil des Nachweises (D-23, D-93)")
        return
    registriert = set(UEB_KENNUNG.findall(text.split(UEB_ANKER, 1)[1]))
    if not registriert:
        err(f"{KERN}/{UEB_REGISTER}: das Register führt keine einzige Kennung der Form "
            f"UEB-NN – Prüfung 44 hätte nichts zu vergleichen (D-93)")
        return

    gebraucht: dict = {}
    for rel in _ueb_katalogdateien(root):
        pfad_k = os.path.join(root, *rel.split(os.sep))
        if not os.path.exists(pfad_k):
            continue
        for kennung in UEB_KENNUNG.findall(read(pfad_k)):
            gebraucht.setdefault(kennung, set()).add(rel.replace(os.sep, "/"))

    for kennung in sorted(set(gebraucht) - registriert):
        stellen = ", ".join(sorted(gebraucht[kennung]))
        err(f"{stellen}: nennt die Präparation {kennung}, die das Register in "
            f"{KERN}/{UEB_REGISTER} nicht führt. Eine Vorbedingung, die auf eine "
            f"unregistrierte Präparation zeigt, ist eine Zusage ohne den Mechanismus "
            f"dahinter – der Testfall gilt als fahrbar, und niemand weiß, was "
            f"herzustellen ist (D-93)")
    for kennung in sorted(registriert - set(gebraucht)):
        err(f"{KERN}/{UEB_REGISTER}: führt die Präparation {kennung}, die kein Testfall "
            f"nennt – weder der Testkatalog noch ein dezentrales Testblatt. Eine "
            f"Präparation, die niemand braucht, wird gepflegt und nicht benutzt; "
            f"entweder trägt ein Testfall sie in seine Vorbedingung ein, oder sie fällt "
            f"aus dem Register (D-93)")


# --- 45: Der Bytecode des Kerns gehoert nicht in die Versionierung (D-97) -----------
#
# ANLASS. Abgezaehlt am 2026-09-15 an **beiden** Projekten, die dieses Framework benutzen:
# Der Pilot fuehrte sechs .pyc-Dateien unter leitwerk-core/ in der Versionierung, das
# Uebungsrepositorium zwei. Zwei von zwei. Der Uebernahmeleitfaden sagte zur .gitignore
# nur, welche Zeilen man **weglassen** soll - die vier, die im Framework-Repositorium die
# Wurzelbestandteile ausschliessen. Welche Zeile man **braucht**, sagte er nicht.
#
# **Das ist dieselbe Bauform wie der Befund von 0.45.0:** eine Anweisung, die die halbe
# Migration beschreibt, ist gefaehrlicher als keine. Wer dem Leitfaden woertlich folgt,
# schreibt eine eigene .gitignore - und versioniert danach den Bytecode eines Werkzeugs,
# das bei jedem Lauf neuen erzeugt.
#
# ZWEI GEGENSTAENDE, und der zweite ist der, der den Fall wirklich faengt:
#
#   1. DIE REGEL. Die .gitignore des Projekts deckt __pycache__ ab. Geprueft wird gegen
#      eine kleine Liste gebraeuchlicher Schreibweisen (GITIGNORE_DECKUNG), nicht gegen
#      eine einzige - ein Projekt, das `*.pyc` schreibt, ist richtig, und eine Pruefung,
#      die es meldete, waere zu eng. Genau der Fehler, den Pruefung 37 einmal gemacht hat.
#   2. DER BESTAND. Wo git erreichbar und die Wurzel ein Repositorium ist: keine Datei
#      unter <CORE_DIR>/ mit der Endung .pyc oder im Pfad __pycache__ darf verfolgt sein.
#
# WARUM BEIDE. Die Regel allein waere die halbe Migration ein zweites Mal: **git liest
# die .gitignore fuer bereits verfolgte Dateien nicht.** Wer die Zeile nachtraegt und
# `git rm --cached` vergisst, bekaeme einen gruenen Lauf und haette die sechs Dateien
# weiter im Repositorium. Der Bestand allein wiederum sagt dem Projekt nicht, wie es die
# Wiederholung verhindert - beim naechsten `git add` waeren sie zurueck.
#
# GRENZE. Gegenstand 2 laeuft nur, wo git erreichbar ist und die Wurzel ein Repositorium
# ist. Wo nicht, sagt die Pruefung das als **Warnung** - dieselbe Bauform, die dieses
# Skript fuer das fehlende PyYAML schon hat. Eine Pruefhaelfte, die stumm ausfaellt, waere
# genau der Befundtyp, gegen den D-23 gebaut ist.
# Und: Fehlt die .gitignore ganz, ist das eine **Warnung** und kein Fehler. Ob ein Projekt
# ueberhaupt versioniert, kann dieses Skript nicht wissen; Gegenstand 2 faengt den echten
# Fall ohnehin, sobald git da ist.
GITIGNORE_DECKUNG = ("__pycache__/", "__pycache__", "**/__pycache__/",
                     "*.pyc", "**/*.pyc")
BYTECODE_MARKER = "__pycache__"


def _verfolgte_dateien(root: str) -> list | None:
    """Vom Versionsverwalter verfolgte Pfade unter <CORE_DIR>/ - oder None.

    None heisst: nicht messbar. Kein git im Pfad, keine Versionierung, oder der Aufruf
    ist gescheitert. Der Unterschied zu einer leeren Liste ist der ganze Punkt - eine
    leere Liste ist ein Messergebnis, None ist keins.
    """
    try:
        lauf = subprocess.run(["git", "-C", root, "ls-files", "--", KERN],
                              capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    if lauf.returncode != 0:
        return None
    return [z.strip() for z in (lauf.stdout or "").splitlines() if z.strip()]


def check_bytecode_versioniert(root: str) -> None:
    """Pruefung 45 (D-97): Der Bytecode des Kerns steht nicht in der Versionierung."""
    # --- Gegenstand 1: die Regel ---------------------------------------------------
    pfad = os.path.join(root, ".gitignore")
    if not os.path.exists(pfad):
        warn(".gitignore: nicht vorhanden. Prüfung 45 kann die Regel gegen den Bytecode "
             "des Kerns nicht prüfen. Versioniert dieses Projekt, gehört `__pycache__/` "
             "dort hinein – die Python-Werkzeuge des Kerns erzeugen bei jedem Lauf "
             "Bytecode unter " + KERN + "/ (D-97)")
    else:
        zeilen = [z.strip() for z in read(pfad).splitlines()]
        if not any(z in GITIGNORE_DECKUNG for z in zeilen):
            err(f".gitignore: deckt den Bytecode des Kerns nicht ab. Die Python-Werkzeuge "
                f"unter {KERN}/ erzeugen bei jedem Lauf `.pyc`-Dateien; versioniert, "
                f"ändern sie sich mit jedem Lauf und überleben den Kern, aus dem sie "
                f"entstanden sind. Eine dieser Zeilen gehört in die Datei: "
                f"{', '.join('`%s`' % m for m in GITIGNORE_DECKUNG)} "
                f"(docs/ADOPTION_GUIDE.md Abschnitt 2, D-97)")

    # --- Gegenstand 2: der Bestand ---------------------------------------------------
    verfolgt = _verfolgte_dateien(root)
    if verfolgt is None:
        warn(f"Gegenstand 2 der Prüfung 45 ist nicht gelaufen – git ist nicht erreichbar "
             f"oder {root} ist kein Repositorium. Ob unter {KERN}/ Bytecode versioniert "
             f"ist, sagt dieser Lauf damit **nicht**; die Regel in der .gitignore allein "
             f"entfernt bereits verfolgte Dateien nicht (D-97)")
        return
    bytecode = sorted(p for p in verfolgt
                      if p.endswith(".pyc") or BYTECODE_MARKER in p)
    if bytecode:
        gezeigt = ", ".join(bytecode[:4]) + (" …" if len(bytecode) > 4 else "")
        err(f"{len(bytecode)} Bytecode-Datei(en) unter {KERN}/ sind versioniert: "
            f"{gezeigt}. **Die Regel in der .gitignore entfernt sie nicht** – git liest "
            f"sie für bereits verfolgte Dateien nicht. Der Weg ist "
            f"`git rm -r --cached {KERN}/**/__pycache__` und danach die Regel (D-97)")


# ---------------------------------------------------------------------------
# Pruefung 46: Der 1.0.0-Stand wird ausgerechnet, nicht gepflegt
# ---------------------------------------------------------------------------
#
# ANLASS. D-11 nennt fuenf Kriterien fuer 1.0.0; vier davon sind maschinell zaehlbar.
# Die Roadmap fuehrte dafuer seit 0.42.0 ausdruecklich KEINE Zahlen, sondern "die
# Befehle, die sie ausrechnen" - die richtige Lehre aus fuenf falschen Zahlen ueber den
# Pruefapparat. Am 2026-09-15 wurden diese Befehle zum ersten Mal ausgefuehrt
# (CR-2026-070, tests/protocols/2026-09-15-gegenpruefung-d11-zaehlregeln.md):
#
#   Kriterium 1  geglaubt 27   gezaehlt 29   der grep kannte EINE von ZWEI registrierten
#                                            Markerschreibweisen; die clientgebundene
#                                            Altform (Produktname statt CLIENT) traegt
#                                            allein im Pack devin-desktop sieben
#                                            Fundstellen und zwei in dessen root-template
#   Kriterium 2  geglaubt 103  gezaehlt 118  "die dezentralen TESTS.md je Skill" wurde als
#                                            zwoelf Dateien gelesen; es sind dreizehn
#   Kriterium 3  geglaubt 16   gezaehlt 69   die genannte Ablagenliste deckt ein Viertel
#                                            des Bestands - und framework/core/ ist
#                                            genannt und traegt gar keine Statuszeile
#   Kriterium 4  geglaubt 16   gezaehlt 9    ein roher grep zaehlte die Legende, fuenf
#                                            Klaerungspunkte und D-11 selbst mit
#
# Vier von vier. Keine der Zahlen ist je falsch geschrieben worden - jede ist das
# richtige Ergebnis einer Regel, die weniger kann als ihr Kriterium verlangt. Ein
# Befehl, den niemand ausfuehrt, ist keine Ausrechnung, sondern eine Zahl mit einem
# Zwischenschritt; und weil ihn niemand ausfuehrt, faellt auch nicht auf, dass er das
# Falsche zaehlt.
#
# BAUFORM (E1). Die von Pruefung 40 und 31: Der Stand steht AUSGERECHNET an genau einer
# Stelle - der Standzeile in docs/ROADMAP.md -, und diese Pruefung haelt die geschriebene
# Zahl gegen die gezaehlte. Nicht der offene Punkt ist der Fehler, sondern die falsche
# Zahl. Ein Zaehler, der jeden offenen Punkt meldete, ergaebe heute 225 Fehler, machte
# jeden Lauf rot und waere binnen eines Releases abgeschaltet; ein Zaehler, der nur
# berichtet, ist keine Pruefung. Der Preis dieser Bauform steht im Antrag und ist
# gewollt: JEDER Fortschritt macht den Lauf rot, bis die Zahl nachgezogen ist. Genau
# dieses Nachziehen ist der Vorgang, der bis 0.47.0 unterblieben ist.
#
# ZAEHLBEREICH (E2). Nur <CORE_DIR>/, ohne build/ (Erzeugnis), CHANGELOG.md,
# governance/change-requests/ und tests/protocols/ (datierte, abgeschlossene
# Aufzeichnungen). Der Kern ist in jeder Installation derselbe - install.py --check ist
# genau dafuer da -, also ist die Zahl installationsunabhaengig und dieselbe Standzeile
# gilt in jedem uebernehmenden Projekt. Fundstellen ausserhalb des Kerns zaehlen nicht,
# auch echte: README.md:165 war so eine und ist per Hand berichtigt.
#
# DER FALLSTRICK, DER BEIM BAUEN ZUSCHNAPPTE (E7). Die erste Fassung lief ueber
# glob.glob(..., recursive=True). glob ueberspringt Pfadbestandteile, die mit einem Punkt
# beginnen - damit fehlten fuenfzehn Dateien des Kerns, darunter genau die zwei Traeger
# clients/*/root-template/.devin/README.md und .../.claude/README.md, die den Befund zu
# Kriterium 1 tragen. Der Zaehler haette 27 gemeldet und damit zufaellig die geglaubte
# Zahl bestaetigt. Eine Zaehlregel, die einen Traeger still ueberspringt, war der Anlass
# dieses Antrags; sie ist beim Bauen der Abhilfe ein zweites Mal entstanden. Deshalb
# os.walk, und deshalb misst die Selbstprobe C1 des Sondenskripts beide Verfahren
# gegeneinander.
#
# WAS SIE NICHT LEISTET.
#   * Kriterium 5 von D-11 ("Uebernahme in ein zweites Projekt nachgewiesen") zaehlt sie
#     NICHT. Das ist keine Zahl, sondern eine Feststellung. Eine ENTHALTUNG, und sie
#     steht hier statt in einem Gegenstand, der nichts misst.
#   * Sie misst Zahlen, nicht Fortschritt. Ein Modulstatus, der von `entwurf` auf `pilot`
#     gehoben wird, ohne dass jemand das Modul angesehen hat, senkt Kriterium 3 um eins.
#     Die fachliche Abnahme ist nicht maschinell, und diese Pruefung behauptet es nicht.
#   * Kriterium 1 zaehlt auch die Fundstellen, die den Marker nur NENNEN - Registerzeile,
#     Glossarzeile, Arbeitsanweisung (E3). Die Zahl ist ein PEGEL, kein Arbeitsvorrat,
#     und sie kann nicht auf null gehen, solange der Marker sein eigenes Register hat.
#     Das ist richtig so: PLACEHOLDER_REGISTRY.md schreibt beiden Markerformen in der
#     Spalte "Ersetzung/Frist" ausdruecklich "vor Version 1.0.0" vor. Ein Platzhalter,
#     dessen letzte Aussage verifiziert ist, gehoert aus dem Register - sonst fuehrt das
#     Repositorium einen Platzhalter ohne Gegenstand.
#   * Sie sagt nicht "1.0.0-reif" (E8). Stehen alle vier Zahlen auf 0 und der Lauf ist
#     gruen, IST das die Meldung - erzwungen statt behauptet, und ohne einen fuenften
#     Gegenstand, der heute nichts faengt.
D11_DATEI = KERN + "/docs/ROADMAP.md"
D11_SATZ = ("Gezählt von Prüfung 46: Kriterium 1 = {}, Kriterium 2 = {}, "
            "Kriterium 3 = {}, Kriterium 4 = {}")
D11_ANKER = "Gezählt von Prüfung 46: Kriterium 1 = "
# Beide registrierten Schreibweisen (E4). Die Altform ist nur im Client Pack
# devin-desktop zulaessig (Pruefung 14 setzt das durch) - sie traegt aber dieselbe Frist
# "vor Version 1.0.0" und ist damit derselbe Gegenstand. Wer nur die neutrale Form
# zaehlt, haelt ein Client Pack mit sieben offenen Verifikationsbedarfen fuer fertig.
D11_MARKER_RE = re.compile(r"<VERIFY AGAINST CURRENT (?:CLIENT|DEVIN) DOCUMENTATION>")
D11_AUSSER = ("build/", "CHANGELOG.md", "governance/change-requests/",
              "tests/protocols/")
D11_MARKER_ENDUNGEN = (".md", ".json", ".py")
D11_STECKBRIEF_RE = re.compile(r"^\|\s*Status\s*\|\s*(.+?)\s*\|$")
# Die Steckbriefzeile steht im Kopf des Dokuments. Sechzig Zeilen sind grosszuegig
# gemessen (der spaeteste Treffer im Bestand steht auf Zeile 41) und halten zugleich die
# Lebenszyklustabelle aus 08-skill-conventions.md (Zeile 92) und die Vorfalltabelle aus
# INCIDENT_HANDLING.md (Zeile 37) draussen - beides Tabellen MIT einer Statusspalte, die
# keinen Modulstatus fuehren.
D11_STECKBRIEF_KOPF = 60
D11_KRITERIEN = ("kein unbearbeiteter VERIFY-Marker",
                 "Testkatalog und dezentrale Testblätter ohne `offen`",
                 "Modulstatus über `entwurf`",
                 "Decision Records ohne `entschieden (Vorschlag)`")


def _d11_kerndateien(root: str, endungen: tuple):
    """(absoluter Pfad, Pfad unter <CORE_DIR>/) je Kerndatei im Zaehlbereich.

    os.walk und NICHT glob: glob ueberspringt Pfadbestandteile, die mit einem Punkt
    beginnen, und genau dort liegen zwei Traeger des Kerns (E7, Selbstprobe C1).
    """
    wurzel = os.path.join(root, KERN)
    for ordner, _, dateien in os.walk(wurzel):
        for name in sorted(dateien):
            if not name.endswith(endungen):
                continue
            pfad = os.path.join(ordner, name)
            rest = os.path.relpath(pfad, wurzel).replace(os.sep, "/")
            if any(rest == a or rest.startswith(a) for a in D11_AUSSER):
                continue
            yield pfad, rest


def _d11_offene_zellen(text: str, praefix: str) -> int:
    """Tabellenzeilen mit `praefix`, deren letzte Zelle mit 'offen' beginnt."""
    treffer = 0
    for zeile in text.replace("\r\n", "\n").split("\n"):
        z = zeile.strip()
        if not z.startswith(praefix) or z.startswith("|---"):
            continue
        zellen = tabellenzellen(z)
        if zellen and zellen[-1].startswith("offen"):
            treffer += 1
    return treffer


def _d11_zaehlen(root: str) -> list:
    """Die vier maschinell zaehlbaren Kriterien von D-11, in ihrer Reihenfolge."""
    # --- 1: Markerfundstellen, beide Schreibweisen -----------------------------------
    k1 = 0
    for pfad, _ in _d11_kerndateien(root, D11_MARKER_ENDUNGEN):
        k1 += len(D11_MARKER_RE.findall(read(pfad)))

    # --- 2: offene Ergebniszellen im Katalog UND in jedem Testblatt -------------------
    # Gefunden durch Baumdurchlauf, nicht durch eine Ablagenliste (E5): Eine Liste kann
    # eine dreizehnte Datei uebersehen, und sie hat es.
    katalog = os.path.join(root, KERN, "tests", "TEST_CATALOG.md")
    k2 = _d11_offene_zellen(read(katalog), "| FW-") if os.path.isfile(katalog) else 0
    for pfad, _ in _d11_kerndateien(root, ("TESTS.md",)):
        k2 += _d11_offene_zellen(read(pfad), "| ")

    # --- 3: Steckbriefe auf `entwurf`, im ganzen Bestand ------------------------------
    # Verglichen wird das ERSTE WORT des Werts: role-packs/software-development traegt
    # "entwurf (Referenzpack der Erstfassung)", und ein Gleichheitsvergleich saehe sie
    # nicht (E6).
    k3 = 0
    for pfad, _ in _d11_kerndateien(root, (".md",)):
        for zeile in read(pfad).replace("\r\n", "\n").split("\n")[:D11_STECKBRIEF_KOPF]:
            treffer = D11_STECKBRIEF_RE.match(zeile.strip())
            if not treffer:
                continue
            wert = treffer.group(1).strip().strip("`").strip()
            if wert.split()[:1] == ["entwurf"]:
                k3 += 1
            break

    # --- 4: Decision Records auf `entschieden (Vorschlag)` ----------------------------
    # NUR Zeilen der Form | D-NN |. Nicht die Legende, nicht die Klaerungspunkte K-NN,
    # nicht D-11 selbst: D-11 sagt "Decision Records", und ein Klaerungspunkt ist keiner.
    log = os.path.join(root, KERN, "governance", "DECISION_LOG.md")
    k4 = 0
    if os.path.isfile(log):
        for zeile in read(log).replace("\r\n", "\n").split("\n"):
            z = zeile.strip()
            if not re.match(r"^\|\s*D-\d+\s*\|", z):
                continue
            zellen = tabellenzellen(z)
            if len(zellen) > 4 and zellen[4].startswith("entschieden (Vorschlag)"):
                k4 += 1
    return [k1, k2, k3, k4]


def check_d11_stand(root: str) -> None:
    """Pruefung 46 (D-98, D-99): Der 1.0.0-Stand ist ausgerechnet, nicht gepflegt."""
    pfad = os.path.join(root, D11_DATEI.replace("/", os.sep))
    if not os.path.isfile(pfad):
        err(f"{D11_DATEI}: fehlt. Prüfung 46 hält dort den ausgerechneten 1.0.0-Stand "
            f"gegen die geschriebene Standzeile (D-98)")
        return
    text = read(pfad)

    # --- Gegenstand 1: der Anker ------------------------------------------------------
    # Die Bauform der Pruefungen 28, 29, 31 und 40: Eine Konsistenzpruefung findet ihren
    # Gegenstand ueber einen Suchtext. Geht er verloren, bestuende sie LEISE - und
    # niemand saehe, dass der 1.0.0-Stand nicht mehr geprueft wird.
    wie_oft = text.count(D11_ANKER)
    if wie_oft != 1:
        err(f"{D11_DATEI}: die Standzeile steht {wie_oft}x statt genau einmal "
            f"(gesucht: '{D11_ANKER}…'). Prüfung 46 hat ihren Gegenstand verloren und "
            f"würde sonst leise bestehen. Erwartet wörtlich, in einer Zeile: "
            f"'{D11_SATZ.format(*_d11_zaehlen(root))}' (D-98)")
        return

    # --- Gegenstand 2 bis 5: die vier Zahlen -----------------------------------------
    # Verglichen werden die ZAHLEN, nicht die Zeichenkette. Ein Vergleich per `in`
    # bestuende bei jedem Praefix: "Kriterium 4 = 9" steckt in "Kriterium 4 = 99", und
    # die Sonde 46a ist genau daran gefallen, bevor sie es meldete.
    gezaehlt = _d11_zaehlen(root)
    soll = D11_SATZ.format(*gezaehlt)
    zeile = next((z.strip() for z in text.replace("\r\n", "\n").split("\n")
                  if D11_ANKER in z), "")
    geschrieben = [int(n) for n in re.findall(r"Kriterium \d+ = (\d+)", zeile)]
    if geschrieben == gezaehlt:
        return
    # Die Meldung nennt die gezaehlte Zahl je Kriterium einzeln - wer nur "stimmt nicht"
    # liest, sucht selbst nach, und genau dieses Nachsuchen ist der Vorgang, der bis
    # 0.47.0 unterblieben ist.
    for i, (name, ist) in enumerate(zip(D11_KRITERIEN, gezaehlt)):
        war = geschrieben[i] if i < len(geschrieben) else None
        if war == ist:
            continue
        richtung = ("die Standzeile nennt keine Zahl dafür" if war is None else
                    f"die Standzeile nennt {war}" +
                    (" – ein Kriterium ist zurückgefallen" if ist > war else
                     " – der Fortschritt ist nicht nachgezogen"))
        err(f"{D11_DATEI}: Kriterium {i + 1} von D-11 ({name}) ist gezählt **{ist}**, "
            f"{richtung}. Der 1.0.0-Stand gehört ausgerechnet und nicht gepflegt; am "
            f"2026-09-15 lagen alle vier Zahlen daneben, ohne dass eine je falsch "
            f"geschrieben worden wäre (CR-2026-070, D-98)")
    if len(geschrieben) != len(gezaehlt):
        err(f"{D11_DATEI}: die Standzeile führt {len(geschrieben)} Zahlen statt "
            f"{len(gezaehlt)}. Erwartet wörtlich: '{soll}' (D-98)")

# ---------------------------------------------------------------------------
# Pruefung 47: Das Statusvokabular jedes Modultraegers
# ---------------------------------------------------------------------------
#
# ANLASS (CR-2026-073 E5, D-108). Das Lebenszyklusmodell gilt seit 0.50.0 fuer JEDEN
# Modultraeger (D-102) - durchgesetzt war das Vokabular fuer genau einen Dateityp. Die
# Skillpruefung meldet seit 0.12.0 einen unbekannten Statuswert, aber nur in einer
# SKILL.md; fuer die uebrigen 56 der 69 Statustraeger war jede Zeichenfolge
# zulaessig, und "| Status | banane |" waere durch jeden Lauf gelaufen. Genau
# dieser Fall stand fuer Skills bis 0.12.0 offen und ist mit FW-VN-01
# geschlossen worden - fuer die anderen Ablagen nie. Solange kein Nicht-Skill gehoben war, hatte die Luecke keinen
# Gegenstand; mit dem ersten gehobenen Nicht-Skill-Traeger hat sie einen (D-102, E5).
#
# DER ZWEITE ANLASS, UND ER IST DER GROESSERE (K-36, D-105). D-102 definierte den
# Modultraeger ueber das Merkmal, das er tragen soll: "jede versionierte Datei mit
# einer Steckbriefzeile Status". Eine solche Definition laesst jeden Traeger
# entkommen, indem er die Zeile weglaesst - und zwoelf taten das, darunter die elf
# normativen Kernmodule, fuer die checklists/11-framework-release.md unter Abschluss
# ausdruecklich einen Status oberhalb von entwurf verlangt. Ein Pruefpunkt ohne
# Gegenstand, in der Checkliste, die 1.0.0 freigibt. Gegenstand 2 dieser Pruefung
# schliesst das Loch: Wer einen Steckbrief fuehrt, fuehrt eine Statuszeile.
#
# WIE EIN STECKBRIEF ERKANNT WIRD (E5). Als die ERSTE Tabelle des Dokuments, die VOR
# der ersten Ueberschrift der Ebene 2 steht und die Kopfzeile "| Attribut | Wert |"
# traegt. Der Zuschnitt ist gemessen und nicht geraten: Eine blosse Suche nach dieser
# Kopfzeile in den ersten sechzig Zeilen trifft auch templates/PLAN_TEMPLATE.md, wo
# sie im KOERPER der Vorlage steht - hinter einer H2, als Formular fuer den Plan, der
# aus ihr entsteht. Das ist kein Steckbrief, und die Datei fuehrt zu Recht keinen
# Status. Gegen den Bestand gemessen erkennt die Regel 81 Steckbriefe (69 mit und 12
# ohne Statuszeile) und keinen Fehltreffer.
#
# VIER GEGENSTAENDE:
#   1. Der verlorene Anker. Findet der Lauf ueberhaupt keinen Steckbrief, bestuende
#      diese Pruefung leise. Sie meldet es deshalb selbst - die Bauform der Pruefungen
#      28, 29, 31, 40 und 46 (D-23).
#   2. Vollstaendigkeit. Jeder Steckbrief fuehrt eine Statuszeile. Das ist der
#      Mechanismus zu D-105; ohne ihn entkaeme der naechste Traeger genauso.
#   3. Vokabular. Das erste Wort des Werts ist einer der fuenf Statuswerte aus
#      08-skill-conventions.md Abschnitt 7. Das ERSTE WORT, weil
#      role-packs/software-development einen Verlaufszusatz traegt ("entwurf
#      (Referenzpack der Erstfassung)") - dieselbe Leseregel wie Pruefung 46 (E6 von
#      CR-2026-070).
#   4. Der Ausfuellschlitz gehoert der Vorlage, und nur ihr (D-104). Eine Vorlage
#      traegt in der Statuszelle einen Schlitz und KEINEN echten Wert - ein echter
#      ginge unveraendert in jede Kopie ueber und waere damit unveraenderlich, ohne
#      dass jemand das entschieden hat; genau dieser Defekt machte Kriterium 3 von
#      D-11 unerreichbar. Umgekehrt traegt ein Traeger, der keine Vorlage ist, keinen
#      Schlitz: Das ist der Preis, den D-104 benannt und nicht abgesichert hat - "wer
#      eine Vorlage kopiert und den Schlitz nicht fuellt, hat ein Pack ohne
#      Statuswert; bei einem Skill faengt das SKILL_STATUS, bei Client-, Role- und
#      Technology-Pack heute nichts".
#
# WAS SIE NICHT LEISTET.
#   * Sie prueft das VOKABULAR, nicht die BERECHTIGUNG. Ob ein Traeger auf pilot
#     stehen darf, entscheidet das Review nach 01-governance.md Abschnitt 5 Punkt 3 -
#     ein Protokoll, das ihn namentlich nennt. Das ist ausdruecklich nicht maschinell
#     (D-102), und diese Pruefung behauptet es nicht.
#   * Sie zaehlt nicht. Den Stand haelt Pruefung 46; hier geht es um die Frage, ob ein
#     Wert ueberhaupt zum Vokabular gehoert.
#   * Vorlagen erkennt sie am Ablageort (templates/ oder ein Verzeichnis _template),
#     also an der Unterstrich-Konvention, die auch Pruefung 31 benutzt - nicht an einem
#     Namen und nicht an einer gepflegten Liste.
STATUS_KOPF_RE = re.compile(r"^\|\s*Attribut\s*\|\s*Wert\s*\|$")
STATUS_ZEILE_RE = re.compile(r"^\|\s*Status\s*\|\s*(.+?)\s*\|$")
# Der Ausfuellhinweis einer Vorlage in der Form, die D-104 gesetzt hat: die Marke, ein
# Semikolon und der Satz, mit welchem Wert die Kopie beginnt.
STATUS_SCHLITZ_RE = re.compile(r"^<TBD: Status; .*\bbeginnt auf entwurf>$")
STATUS_ZELLE = "\\| Status \\| … \\|"


def _status_steckbrief(text: str):
    """Die Zeilen des Steckbriefs eines Dokuments, oder None.

    Der Steckbrief ist die erste Tabelle des Dokuments; sie steht vor der ersten
    Ueberschrift der Ebene 2 und traegt die Kopfzeile "| Attribut | Wert |". Eine
    erste Tabelle mit anderer Kopfzeile bedeutet: kein Steckbrief - und eine Tabelle
    weiter unten ist keiner, auch wenn sie so aussieht (PLAN_TEMPLATE.md).
    """
    zeilen = text.replace("\r\n", "\n").split("\n")
    for nr, roh in enumerate(zeilen):
        z = roh.strip()
        if z.startswith("## "):
            return None
        if not z.startswith("|"):
            continue
        if not STATUS_KOPF_RE.match(z):
            return None
        raus = []
        for weiter in zeilen[nr:]:
            if not weiter.strip().startswith("|"):
                break
            raus.append(weiter.strip())
        return raus
    return None


def _status_ist_vorlage(rest: str) -> bool:
    """Liegt die Datei in einer Vorlagenablage? Unterstrich-Konvention wie Pruefung 31."""
    return rest.startswith("templates/") or "/_template/" in rest


def check_status_vokabular(root: str) -> None:
    """Pruefung 47 (D-105, D-108): Jeder Steckbrief fuehrt einen gueltigen Statuswert."""
    gefunden = 0
    for pfad, rest in _d11_kerndateien(root, (".md",)):
        steckbrief = _status_steckbrief(read(pfad))
        if steckbrief is None:
            continue
        gefunden += 1
        werte = [m.group(1).strip() for m in
                 (STATUS_ZEILE_RE.match(z) for z in steckbrief) if m]

        # --- Gegenstand 2: Vollstaendigkeit -------------------------------------------
        if not werte:
            err(f"{KERN}/{rest}: der Steckbrief führt keine Zeile `{STATUS_ZELLE}`. "
                f"Jeder Träger mit einem Steckbrief durchläuft den Lebenszyklus "
                f"(D-102); bis 0.50.0 definierte sich der Modulträger über genau diese "
                f"Zeile und ließ damit jeden entkommen, der sie wegließ – zwölf taten "
                f"es, darunter die elf normativen Kernmodule, für die FW-CL-11 einen "
                f"Status oberhalb von `entwurf` verlangt (K-36, D-105)")
            continue

        wert = werte[0].strip("`").strip()
        schlitz = wert.startswith("<TBD")
        vorlage = _status_ist_vorlage(rest)

        # --- Gegenstand 4: der Schlitz gehoert der Vorlage, und nur ihr ---------------
        if schlitz and not vorlage:
            err(f"{KERN}/{rest}: die Statuszelle trägt den Ausfüllschlitz '{wert}', "
                f"obwohl die Datei keine Vorlage ist. Wer eine Vorlage kopiert, füllt "
                f"den Schlitz – sonst steht ein Pack ohne Statuswert im Bestand. Das "
                f"ist der Preis, den D-104 benannt und nicht abgesichert hat (D-108)")
            continue
        if vorlage and not schlitz:
            err(f"{KERN}/{rest}: die Statuszelle einer Vorlage trägt den echten Wert "
                f"'{wert}' statt eines Ausfüllschlitzes. Der Steckbrief einer Vorlage "
                f"beschreibt die KOPIE; ein echter Wert geht unverändert in jede Kopie "
                f"über und ist damit unveränderlich, ohne dass jemand das entschieden "
                f"hätte. Genau so war Kriterium 3 von D-11 unerreichbar (D-104). "
                f"Erwartet: '<TBD: Status; … beginnt auf entwurf>'")
            continue
        if schlitz:
            if not STATUS_SCHLITZ_RE.match(wert):
                err(f"{KERN}/{rest}: der Ausfüllschlitz '{wert}' folgt nicht der Form "
                    f"'<TBD: Status; … beginnt auf entwurf>'. Ein Schlitz, der den "
                    f"Anfangswert nicht nennt, lässt die Kopie raten (D-104)")
            continue

        # --- Gegenstand 3: das Vokabular ---------------------------------------------
        erstes = wert.split()[:1]
        if erstes and erstes[0] not in SKILL_STATUS:
            err(f"{KERN}/{rest}: Statuswert '{wert}' gehört nicht zum Vokabular. "
                f"Zulässig sind die fünf Werte aus "
                f"framework/core/08-skill-conventions.md Abschnitt 7 "
                f"({', '.join(sorted(SKILL_STATUS))}); verglichen wird das erste Wort, "
                f"ein Verlaufszusatz in Klammern ist zulässig. Bis 0.50.0 griff diese "
                f"Regel nur in einer SKILL.md – für 56 der 69 Statusträger war jede "
                f"Zeichenfolge erlaubt (D-108)")

    # --- Gegenstand 1: der Anker ------------------------------------------------------
    if not gefunden:
        err(f"{KERN}/: kein einziger Steckbrief gefunden (erste Tabelle des Dokuments "
            f"vor der ersten Überschrift der Ebene 2, Kopfzeile `| Attribut | Wert |`). "
            f"Prüfung 47 hat ihren Gegenstand verloren und würde sonst leise bestehen "
            f"(D-108)")



# ---------------------------------------------------------------------------
# Pruefung 48: Der werkzeugneutrale Kern nennt keinen Pfad eines Client Packs
# ---------------------------------------------------------------------------
#
# ANLASS. Gemessen am 2026-09-18 (CR-2026-080, D-128): SIEBZEHN Fundstellen in
# VIERZEHN anweisenden Traegern nannten den Dateinamen oder das Verzeichnis genau
# eines Client Packs - darunter sechs Prompt-Vorlagen und mit Abschnitt 2 von
# 08-skill-conventions.md ein NORMATIVES Kernmodul, dessen Prosa zwei Zeilen tiefer
# richtig "die Skill-Ablage der Laufzeitschicht" sagt. Die Regel dazu steht seit
# 0.31.0 in docs/RUNTIME_GLOSSARY.md, und durchgesetzt hat sie nichts.
#
# WARUM PRUEFUNG 12 SIE NICHT FAND - drei Gruende, alle nachgelesen:
#   1. Sie liest nur Token in BACKTICKS. Zehn der siebzehn standen ohne: in einem
#      Codeblock, in Prosa oder in einem HTML-Kommentar.
#   2. Sie meldet nur Pfade, die es NICHT GIBT. Im Framework-Repositorium ist genau
#      ein Pack installiert; dessen Laufzeitschicht existiert und ist damit
#      unsichtbar. Gemeldet wurde nur der jeweils ANDERE Client.
#   3. Und ihre Wurzelliste war selbst clientgebunden: LINK_ROOTS fuehrte woertlich
#      '.devin/', 'AGENTS.md' und 'AGENTS.local.md'. Die Pfade des anderen Packs
#      waren damit gar kein Kandidat - die Pruefung, die die Bindung melden sollte,
#      trug sie selbst. Dieser dritte Grund stand in keiner Fassung des Befunds; er
#      ist beim Nachzaehlen aufgefallen.
#
# UND ER HAT SICH BEIM MESSEN VERKLEINERT, nicht vergroessert. Der Verdacht war, die
# enge Wurzelliste erzeuge in einer Installation des anderen Packs eine Falschmeldung.
# Drei Zuschnitte sagen: nein. Sie deckte sich mit der zweiten engen Stelle desselben
# Blocks, OPTIONAL_RUNTIME_RE, die ebenfalls nur '.devin/' kannte - beide waren in
# DERSELBEN Richtung zu eng und haben einander gedeckt. Die Ableitung aus den
# Manifesten bleibt trotzdem: Sie schafft eine gepflegte Clientliste ab. Aber sie
# behebt keine gemessene Falschmeldung, und das gehoert hierhin und nicht weggelassen.
#
# DIE MARKEN STAMMEN AUS DEN MANIFESTEN, nicht aus einer gepflegten Liste - dieselbe
# Bauform wie _client_actor_names in Pruefung 14: Ein neues Client Pack bringt seine
# Pfade selbst mit und wird ohne Aenderung an dieser Pruefung erfasst.
#
# DREI GATTUNGEN SIND AUSGENOMMEN, und sie stehen in docs/RUNTIME_GLOSSARY.md und
# nicht nur hier - eine Ausnahme, die allein im Quelltext steht, ist keine Regel:
#   * CHRONIK berichtet einen vergangenen Stand. Ihn nachtraeglich zu glaetten,
#     zerstoert die Nachvollziehbarkeit. docs/ROADMAP.md gehoert dazu: Sie fuehrt die
#     Erhebungsergebnisse der Arbeitspakete und die Befundberichte je Release.
#   * WERKZEUGE (.py) stellen Installationen her oder pruefen sie; sie MUESSEN Pfade
#     nennen. Diese Datei ist selbst eines davon.
#   * Die ABBILDUNGSTABELLEN - Glossar, Platzhalterregister und die Client Packs -
#     muessen beide Namen nennen; dort ist der Pfad der Inhalt.
#
# EINE VIERTE AUSNAHME TRAEGT EINE FRIST. build/ haelt die Quellen des Hauptdokuments;
# es ist ueber vierzig Releases zurueck und wird mit AP11 (~0.69.0) neu gesetzt. Die
# Ausnahme faellt mit diesem Schritt, und sie steht dort in der Roadmap.
#
# EINE SPALTE STATT EINER DATEI. In tests/TEST_CATALOG.md ist die letzte Zelle einer
# Tabellenzeile der Ergebnisstatus; ein Pfad dort nennt, was ein Lauf gelesen hat, und
# gehoert zum gemessenen Client Pack (D-117). Die anweisenden Spalten derselben Zeile
# stehen unter der Regel - die Eingabe "Passe AGENTS.md an" war eine davon. Denselben
# Zuschnitt - die LETZTE Zelle - benutzt Pruefung 46 fuer den Ergebnisstatus.
#
# GRENZE. Sie findet die PFADE eines Packs, nicht seinen Produktnamen. "Devin Desktop"
# in einem Kerntext laesst D-28 ausdruecklich zu, und Pruefung 14 setzt genau das
# durch. Ob diese Erlaubnis zu weit reicht - fuenfzehn Fundstellen in zehn Traegern,
# darunter der Titel des Onboarding-Leitfadens -, ist K-52 und nicht entschieden.
P48_AUSGENOMMEN = (
    # Ein Client Pack DARF die Pfade seines Clients nennen.
    KERN + "/clients/",
    # Frist: faellt mit AP11 (~0.69.0), wenn das Hauptdokument neu gesetzt wird.
    KERN + "/build/",
)
# Chronik nach docs/RUNTIME_GLOSSARY.md. Dieselbe Menge wie ACTOR_HISTORY, um
# docs/ROADMAP.md erweitert: Sie fuehrt die Erhebungen je Arbeitspaket.
P48_CHRONIK = ACTOR_HISTORY + (KERN + "/docs/ROADMAP.md",)
# Die Abbildungstabellen selbst.
P48_ABBILDUNG = (KERN + "/docs/RUNTIME_GLOSSARY.md",
                 KERN + "/docs/PLACEHOLDER_REGISTRY.md")
# Traeger, in denen die LETZTE Tabellenzelle ein Beleg ist und kein Anweisungstext.
P48_ERGEBNISSPALTE = (KERN + "/tests/TEST_CATALOG.md",)
ZELLTRENNER_RE = re.compile(r"(?<!\\)\|")


def _client_pfadmarken(root: str) -> list:
    """(Pfad, Clientname) je Laufzeitartefakt jedes Client Packs, laengste zuerst.

    Quelle sind die runtime_placeholders der Manifeste - nicht eine gepflegte Liste.
    <CLIENT_NAME> traegt keinen Pfad, und <CORE_DIR> gehoert der Installation und
    keinem Client (docs/PLACEHOLDER_REGISTRY.md).

    Laengste zuerst, damit '.claude/skills' als sich selbst zaehlt und nicht als
    '.claude': Wer kurz vor lang prueft, zaehlt dieselbe Stelle zweimal.
    """
    marken: dict[str, str] = {}
    base = os.path.join(root, KERN, "clients")
    if not os.path.isdir(base):
        return []
    for name in sorted(os.listdir(base)):
        if name.startswith("_"):
            continue
        mp = os.path.join(base, name, "manifest.json")
        if not os.path.exists(mp):
            continue
        try:
            man = json.loads(read(mp))
        except json.JSONDecodeError:
            continue
        client = man.get("client", name)
        for schluessel, wert in (man.get("runtime_placeholders") or {}).items():
            if schluessel in ("<CLIENT_NAME>", "<CORE_DIR>") or not wert:
                continue
            marken.setdefault(wert, client)
    return sorted(marken.items(), key=lambda kv: (-len(kv[0]), kv[0]))


def _belegspalte(zeile: str) -> int:
    """Spaltenindex, ab dem die LETZTE Zelle einer Markdown-Tabellenzeile beginnt.

    Keine Tabellenzeile - oder eine ohne Inhalt hinter dem letzten Trenner - liefert
    die Zeilenlaenge; dann liegt kein Treffer dahinter und alles steht unter der Regel.
    """
    if not zeile.lstrip().startswith("|"):
        return len(zeile)
    trenner = [m.start() for m in ZELLTRENNER_RE.finditer(zeile)]
    if len(trenner) < 2:
        return len(zeile)
    # Die letzte Zelle liegt zwischen dem vorletzten und dem letzten Trenner.
    return trenner[-2] + 1


def check_tool_neutrality(root: str) -> None:
    """Pruefung 48 (D-02, D-128): Kein anweisender Kerntraeger nennt einen Clientpfad."""
    marken = _client_pfadmarken(root)
    if not marken:
        err(f"{KERN}/clients/: kein Client Pack mit runtime_placeholders gefunden – "
            f"Prüfung 48 leitet ihre Marken daraus ab und hat ihren Gegenstand "
            f"verloren; sie bestünde sonst leise (D-23)")
        return
    for path in iter_text_files(root):
        if not path.endswith((".md", ".template")):
            continue
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if not rel.startswith(KERN + "/"):
            continue
        if rel.startswith(P48_AUSGENOMMEN + P48_CHRONIK + P48_ABBILDUNG):
            continue
        if os.path.basename(rel) in ACTOR_HISTORY_BASENAMES:
            continue
        belegspalte = rel in P48_ERGEBNISSPALTE
        for i, zeile in enumerate(read(path).splitlines(), 1):
            ab = _belegspalte(zeile) if belegspalte else len(zeile)
            belegt = [False] * (len(zeile) + 1)
            for marke, client in marken:
                start = 0
                while True:
                    j = zeile.find(marke, start)
                    if j < 0:
                        break
                    start = j + 1
                    ende = j + len(marke)
                    if j >= ab or any(belegt[j:ende]):
                        continue
                    # Teil eines laengeren Namens ist kein Treffer.
                    if (j and (zeile[j - 1].isalnum() or zeile[j - 1] in "/._-")):
                        continue
                    if zeile[ende:ende + 1].isalnum() or zeile[ende:ende + 1] in "._-":
                        continue
                    for k in range(j, ende):
                        belegt[k] = True
                    err(f"{rel}:{i}: '{marke}' gehört der Laufzeitschicht des Client "
                        f"Packs '{client}'. Der Kern ist werkzeugneutral (D-02) und "
                        f"nennt den Begriff, nicht den Pfad – die Entsprechung je Pack "
                        f"steht in {KERN}/docs/RUNTIME_GLOSSARY.md (D-128)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.getcwd())
    ap.add_argument("--strict-overlay", action="store_true")
    ap.add_argument("--check-overlay-ready", action="store_true")
    ap.add_argument("--mermaid", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    if yaml is None:
        # Ohne PyYAML pruefen drei Pruefungen nur noch, ob ein Frontmatter da ist - nicht,
        # was darin steht. Ein Release-Nachweis, der das nicht sagt, behauptet mehr als er
        # geprueft hat; deshalb steht es hier und nicht nur in der Roadmap.
        warn("PyYAML nicht installiert – Prüfung 4 (Frontmatter der Regeltexte), Prüfung 5 "
             "(Frontmatter der Skills) und Prüfung 8 (Overlay-Manifest) laufen eingeschränkt: "
             "Das Vorhandensein wird geprüft, die Feldinhalte nicht. Für einen Release- oder "
             "Übernahmenachweis (FW-KO-01, FW-CL-11, CL-10) muss PyYAML installiert sein")

    man = detect_client(root)
    check_required(root, man)
    check_config(root, man)
    check_berechtigungskoerbe(root, man)
    check_rules(root, man)
    check_skills(root, man)
    check_runtime_placeholders(root, man)
    check_content(root)
    check_links(root)
    check_manifest(root)
    check_versions(root, man)
    check_artefakt_versionen(root)
    check_actor_naming(root)
    check_placeholder_naming(root)
    check_hook_interpreter(root, man)
    check_hook_tool_coverage(root, man)
    check_hook_fail_closed(root, man)
    check_hook_ablageort(root, man)
    check_quellenauskunft(root)
    check_dokumenttabellen(root)
    check_hook_skripte_neutral(root)
    check_importsteuerung(root, man)
    check_normative_kommentare(root, man)
    check_regelablage_sauber(root)
    check_ausfall_mit_ersatz(root)
    check_werkzeugabwesenheit(root)
    check_zusagenfelder(root)
    check_excluded_paths(root, man)
    check_k3_kategorien(root)
    check_grenzfaelle(root)
    check_durchsetzungstiefe(root)
    check_hook_eingabeschema(root, man)
    check_skill_deny_abbildung(root, man)
    check_agent_startwerkzeug(root)
    check_agent_profil_ohne_start(root)
    check_decision_log_zellen(root)
    check_werkzeugabbildung(root)
    check_skillfreigabe(root)
    check_pruefregister(root)
    check_abwesenheitsbeleg(root)
    check_schlitzinhalte(root, man)
    check_hookblock(root, man)
    check_praeparationsregister(root)
    check_bytecode_versioniert(root)
    check_d11_stand(root)
    check_status_vokabular(root)
    check_tool_neutrality(root)
    if args.strict_overlay:
        check_strict_overlay(root, man)
    if args.check_overlay_ready:
        check_overlay_ready(root, man)
    if args.mermaid:
        check_mermaid(root)

    for w in WARNINGS:
        print(f"WARNUNG  {w}")
    for e in ERRORS:
        print(f"FEHLER   {e}")
    print(f"\nErgebnis: {len(ERRORS)} Fehler, {len(WARNINGS)} Warnungen")
    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
