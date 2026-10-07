#!/usr/bin/env python3
"""
Framework-Hook: PreToolUse-Pruefung auf Secrets und geschuetzte Pfade.

Status: entwurf (Belegstatus des Hook-Mechanismus: [DOK]; Eingabeschema gegen die
Aufzeichnungen beider Packs belegt, siehe unten).

AUFBAU IN DREI STUFEN (seit 0.34.0, CR-2026-056, Befund B06):

  1. EREIGNIS    - ist die Eingabe ueberhaupt ein Werkzeugaufruf?
  2. OPERATION   - welches Verb, und welche Pfade nennt die Eingabe wirklich?
  3. REGELN      - die Musterlisten, unveraendert in ihrem Inhalt.

Bis 0.33.0 gab es Stufe 1 und 2 nicht. Das Skript nannte sich "bewusst schema-agnostisch"
und durchsuchte alle Zeichenketten der gelieferten JSON-Struktur. Daraus folgten ZWEI
entgegengesetzte Fehler mit derselben Ursache (gemessen, tests/protocols/
2026-09-13-B06-gegenpruefung.md):

  - ES LIESS ZU VIEL DURCH. Sechs Eingabeformen passierten auch mit --fail-closed: leere
    Eingabe, nur Weissraum, [], null, eine Zeichenkette, eine Zahl. Ein unbekannter, nicht
    leerer Werkzeugname uebersprang beide Pfadbloecke. Und der Rueckfall fuer die
    unbekannte Operation nahm ausdruecklich fuer sich in Anspruch, "die strengere Liste"
    zu sein - er war die einzige Stelle, an der das Kernverzeichnis UNGESCHUETZT war.
  - ES BLOCKIERTE ZU VIEL, und das wog schwerer. Der Client claude-code fuehrt im
    Umschlag jedes Ereignisses transcript_path, und der liegt unter ~/.claude/projects/.
    Damit traf das Strukturmuster fuer die Laufzeitschicht bei JEDEM Schreibzugriff -
    unabhaengig vom Ziel. Am Client nachgemessen: In einer Umgebung ohne Regeltexte
    blockierte der Hook eine harmlose Schreibprobe; der Kontrolllauf ohne Hook legte
    dieselbe Datei an. Dasselbe gilt fuer cwd, wenn die Sitzung im Kernverzeichnis
    startet. Es war kein Feld, es war eine Gattung.

Geprueft wird deshalb die OPERATION, nicht der Umschlag: ausschliesslich tool_input.
cwd dient als Aufloesungsbasis fuer relative Pfade und ist nie Pruefmaterial (D-62).

Verhalten:
- Fund eines Secret-Musters oder eines geschuetzten Pfads in der Werkzeugeingabe
  -> Ausgabe {"decision": "block", "reason": "..."} und Exit-Code 2 (blockiert laut Doku).
- Schreibende Werkzeuge zusaetzlich: jeder Pfad im Kernverzeichnis. Ausfuehrende Werkzeuge
  sind davon ausgenommen, damit die Skripte des Kerns (Validator, install.py --check)
  weiterhin aufrufbar bleiben; dort greift die deny-Regel der Berechtigungsdatei.
- UNPRUEFBARE Eingabe (kein Ereignis, kein aufloesbarer Pfad) -> Exit-Code 0 mit Warnung
  auf stderr (fail-open) oder, mit --fail-closed, Blockade. Das ist ein eigener dritter
  Ausgang neben "sauber" und "gefunden" (D-61): Er sagt nicht, dass nichts gefunden wurde,
  sondern dass nicht gesucht werden konnte.
  Wo --fail-closed steht, entscheidet das Client Pack: Das Manifest fuehrt
  hook_fail_closed, und clientmap.py haengt das Argument beim Rendern an das
  Hook-Kommando. Das Argument steht damit in der Konfiguration, die der Client ohnehin
  ausfuehrt - laeuft der Hook, kommt es an. Eine Umgebungsvariable haette die Zusage an
  eine zweite, unbestaetigte Clientzusage gehaengt (D-31).
  FW_HOOK_FAIL_CLOSED=1 wirkt weiterhin und bleibt der Weg fuer eine Installation, die
  fail-closed ohne Neuinstallation erproben will.
- Kein Fund -> Exit-Code 0.

SEIT 1.17.0 (CR-2026-156) ZWEI AENDERUNGEN AM SCHREIBWEG:
- DAS ZIEL, NICHT DER INHALT (D-449). Bei einem Schreibwerkzeug werden die Pfadmuster
  nur noch gegen die ZIELE der Operation gehalten - die Pfadfelder und die Dateikoepfe
  eines Patchtextes -, nicht mehr gegen den Dateiinhalt. Gemessen am 2026-09-27 in einem
  Projekt mit devin-desktop: Ein Aenderungsantrag unter docs/, der Overlay- und
  Kernpfade NENNT, wurde gesperrt, als schriebe er in sie. Ein unbekanntes Werkzeug
  bleibt bei der strengsten Lesart (alle Zeichenketten); ein Schreibwerkzeug ohne
  Pfadfeld ist unpruefbar. Die Muster fuer Secrets IM Inhalt gelten unveraendert.
- DAS MANDAT (D-447, D-448). Das Overlay ist nicht mehr durch die Berechtigungsdatei
  gesperrt, sondern allein durch diesen Hook - und der laesst ein Schreiben dorthin
  zu, solange ein gueltiges Mandat es deckt. Das Mandat legt nur der Mensch an
  (mandat.py im Kern, im eigenen Terminal); Datei und Befehl sind fuer jede nicht
  lesende Operation gesperrt.
- Jede Sperre nennt in vier Zeilen, was gesperrt ist, warum, was der Mensch tun kann
  und was daraus folgt (Blockade-Hinweis, D-450).

SEIT 1.20.0 (CR-2026-162) ZWEI ERWEITERUNGEN:
- MCP-WERKZEUGE (K-184, D-486). Ein MCP-Aufruf lief an allen fuenf Matchern vorbei, sein
  Inhalt verliess das Haus ungeprueft. Er traegt jetzt das Verb 'mcp', erkannt am
  Namenspraefix aus hook_mcp_prefixes der Manifeste (die Namen selbst waehlt der Server).
  Geprueft werden der Inhalt gegen die Secret-Muster und die Pfadfelder gegen die
  Secret-Pfadmuster - ein Dateisystem-Server liest sonst .env. Die Struktur- und
  Kernpfade gelten NICHT: Eine Doku-Seite, die .claude/ oder den Kern nennt, schreibt
  nicht dorthin. Grenze: Ein MCP-Server, der selbst lokal schreibt, ist ueber die
  Strukturmuster nicht gesperrt; Schreibwerkzeuge stehen nie auf allow (D-459).
- DAS ENTSCHEIDUNGSPROTOKOLL (K-192, D-487). Jede Entscheidung auf ein Ereignis eines
  Clients (erkennbar an hook_event_name) wird als eine JSON-Zeile in
  <git-verzeichnis>/koolie-hook.jsonl festgehalten: Zeit, Werkzeug, Verb, Ergebnis und
  die erste Zeile des Grundes. NIE der Inhalt und nie ein Pfadwert - der Grund nennt
  eine Kategorie (D-39). Abschalten: 'hook_protokoll: aus' im overlay-manifest.yaml.
  Ohne Git-Verzeichnis kein Protokoll (wie beim Mandat). Ein Fehler beim Schreiben
  aendert keine Entscheidung. Grenze: Das Protokoll ist nicht manipulationsgeschuetzt.

SEIT 1.20.2 (CR-2026-164) ZWEI SPERREN MEHR:
- DIE MODUSBINDUNG (K-179, D-501; K-201). Bindet der Mensch einen Modus im eigenen
  Terminal ('mandat.py modus'), sperrt der Hook jeden Schreibaufruf (M1), jeden ausserhalb
  der Plan-Ablage (M2) oder jeden ausserhalb der Pfade des Modus aus dem Overlay, die beim
  Binden kopiert wurden (M3 bis M5). Datei und Befehl sind wie das Mandat fuer den Client gesperrt. Ohne
  Bindung aendert sich nichts. Grenze: Ein Shell-Befehl, der schreibt, entgeht ihr.
- DIE UEBERTRAGUNG VON SECRETS NACH AUSSEN (K-94, D-503). 'cloud drs secret-create' - der
  Weg des eingebauten Skills 'upload-secrets' von devin-desktop - ist fuer jedes
  ausfuehrende Werkzeug gesperrt, weil die CLI die Werte selbst liest.

Das Skript gibt gefundene Secrets niemals aus; es nennt nur die Musterkategorie. Dasselbe
gilt fuer einen unpruefbaren Pfadwert: Genannt wird die Position, nicht der Wert (D-39).
Alle Muster sind generisch; sie enthalten keine realen Werte.
"""
import datetime
import io
import json
import os
import re
import sys

SECRET_PATTERNS = [
    ("privater Schluessel", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("Bearer-Token", re.compile(r"\bBearer\s+[A-Za-z0-9\-_\.=]{20,}", re.I)),
    ("Zugangsdaten-Zuweisung", re.compile(r"(?i)\b(password|passwd|pwd|secret|api[_-]?key|access[_-]?key|token)\b\s*[:=]\s*['\"]?[^\s'\"]{8,}")),
    ("Verbindungszeichenfolge mit Anmeldedaten", re.compile(r"(?i)\b[a-z][a-z0-9+\-.]*://[^/\s:]+:[^@\s]+@")),
    ("Cloud-Zugangsschluessel (generisches Muster)", re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
]

# Zwei Schutzziele, zwei Listen. Sie standen bisher in einer, und das verwischte den
# Unterschied: Ein Secret-Pfad ist vertraulich - er darf auch nicht GELESEN werden. Ein
# Strukturpfad ist integritaetsgeschuetzt - er darf nicht GESCHRIEBEN werden, gelesen
# aber sehr wohl. Zusammengelegt blockierte die Liste auch ein 'git diff' auf einen
# Kernpfad - eine Operation, die das Framework an anderer Stelle ausdruecklich
# voraussetzt (Befunde mit Fundstellen, P4).
#
# ALLE Pfadmuster laufen mit re.I (D-63). Bis 0.33.0 taten es zwei von neun - die
# Endungsliste und secrets/ -, die uebrigen sieben nicht. Das war keine Entscheidung fuer
# POSIX-Semantik, sondern eine Ungleichbehandlung innerhalb derselben Datei: Unter Windows
# bezeichnen .KOOLIE/CORE/VERSION und .koolie/core/VERSION dieselbe Datei, und der Hook
# entschied sie verschieden (gemessen mit os.path.samefile als Vorpruefung). Auf POSIX ist
# re.I eine Verschaerfung - dieselbe Begruendung, mit der ein Muster schon bisher AGENTS
# und CLAUDE gemeinsam fuehrt: Ein zusaetzlich geschuetzter Pfad ist keine Lockerung.
# DIE GRENZE VOR EINEM PFAD - UND WARUM SIE SEIT 1.4.0 AUCH EIN LEERZEICHEN IST
# (CR-2026-133, D-347). Bis 1.3.0 hiess sie `(^|[\\/])`: Ein Pfad musste am Anfang der
# Zeichenkette stehen oder auf einen Schraegstrich folgen. Das traegt, solange der Pfad
# in einem eigenen Feld oder als eigenes Befehlstoken steht - und genau das ist beim
# dritten Client Pack nicht mehr der Fall. Gemessen am 2026-09-23 an einer realen
# Installation: Das Schreibwerkzeug von openai-codex fuehrt keinen Pfad in einem Feld;
# es fuehrt einen PATCHTEXT, und der Pfad steht darin hinter einem Leerzeichen
# ("*** Add File: .koolie/core/notiz.txt"). Der Hook lief, sah den Text - und die
# Musterpruefung traf nicht. Die Datei wurde angelegt.
#   ➡️ Eine Grenze, die nur den Schraegstrich kennt, misst die Schreibweise und nicht
#      die Sache.
# Die Erweiterung ist eine VERSCHAERFUNG und gilt fuer alle drei Packs: Es kommen
# Treffer hinzu, es faellt keiner weg.
_GRENZE = r"(^|[\s\\/])"

SECRET_PATH_PATTERNS = [
    re.compile(_GRENZE + r"\.env(\.|$)", re.I),
    re.compile(r"\.(pem|key|p12|pfx|jks|keystore)$", re.I),
    re.compile(_GRENZE + r"id_(rsa|ed25519|ecdsa)", re.I),
    # SEIT 1.16.0 AUCH OHNE NACHFOLGENDEN TRENNER (CR-2026-155, D-442): Ein
    # Suchwerkzeug nennt das VERZEICHNIS - "secrets", nicht "secrets/pw.txt" -, und ein
    # Befehl wie "grep -r KOEDER secrets" ebenso. Gemessen am 2026-09-26 an cursor-agent:
    # Das Muster mit Pflicht-Trenner liess die Suche ueber den Ordner durch. Das gilt fuer
    # jeden Client mit einem Suchwerkzeug; die Erweiterung ist eine Verschaerfung.
    re.compile(_GRENZE + r"secrets?([\\/]|$)", re.I),
]

STRUCTURE_PATH_PATTERNS = [
    # Wurzel-Anweisungsdatei und Laufzeitschicht heissen je nach Client anders. Bewusst
    # alle Formen: Das Skript wird von allen Client Packs geteilt, und ein zusaetzlich
    # geschuetzter Pfad ist eine Verschaerfung, keine Lockerung.
    #
    # AGENTS.override.md STEHT SEIT 1.4.0 MIT, und der Grund ist gemessen: Bei
    # openai-codex verdraengt diese Datei die Wurzel-Anweisung VOLLSTAENDIG - liegt sie
    # im Projekt, steht die Anweisung des Frameworks in keiner Nachricht der Sitzung.
    # Eine Datei, die Ebene 1 lautlos ersetzt, ist mindestens so schutzwuerdig wie die
    # Ebene selbst.
    re.compile(_GRENZE + r"(AGENTS|CLAUDE)(\.[A-Za-z0-9_-]+)?\.md$", re.I),
    # .cursor SEIT 1.16.0 (CR-2026-155): Laufzeitschicht, Berechtigungsdatei
    # (.cursor/cli.json) und Hook-Datei des Packs cursor liegen dort.
    re.compile(_GRENZE + r"\.(devin|claude|codex|cursor)[\\/]", re.I),
    # .kiro SEIT 1.13.0 (CR-2026-150, D-414, D-415) - mit EINER Ausnahme: .kiro/specs/
    # ist bei diesem Client die Ablage seines Planartefakts, und das ist nach D-415 der
    # Traeger des Plans, kein Artefakt des Frameworks. Das Agentenprofil nimmt denselben
    # Teilbaum ueber das Feld exclude aus seinem Schreibverbot aus; ohne die Ausnahme
    # hier sperrte der Hook in der interaktiven Sitzung, was die Berechtigungen zulassen.
    re.compile(_GRENZE + r"\.kiro[\\/](?!specs[\\/])", re.I),
    # Das Overlay steht als EIGENES Objekt in der Liste (OVERLAY_MUSTER unten): Seit
    # 1.17.0 kann ein Mandat genau dieses eine Muster fuer ein gedecktes Ziel aufheben
    # (D-447) - und nur dieses.
    re.compile(_GRENZE + r"\.koolie[\\/]project-overlay[\\/]", re.I),
    re.compile(_GRENZE + r"framework[\\/]core[\\/]", re.I),
]
OVERLAY_MUSTER = STRUCTURE_PATH_PATTERNS[-2]

# Fuer schreibende Werkzeuge gelten beide Ziele. Die Zusatzmuster aus der Umgebung
# haengen an dieser Summe: Ein Projekt meint sie als Verbot, nicht als Leseerlaubnis.
PROTECTED_PATH_PATTERNS = SECRET_PATH_PATTERNS + STRUCTURE_PATH_PATTERNS

# Das Kernverzeichnis als Ganzes. Es steht bewusst in einer zweiten Liste: Die Muster
# oben gelten auch fuer 'exec', und ein Befehl, der lediglich einen Kernpfad nennt -
# der Validator, install.py --check, ein git diff - muss weiterhin laufen koennen. Fuer
# schreibende Werkzeuge gilt das Verbot vollstaendig. Die Liste ist damit rein additiv:
# Sie verschaerft, ohne eine bisher blockierte Operation freizugeben.
#
# WAS SIE NICHT LEISTET, und das stand hier bis 0.29.0 falsch: Ein Shell-Befehl, der in
# das Kernverzeichnis schreibt, wird von dieser Liste nicht erfasst - und auch nicht von
# der Berechtigungsdatei, auf die der Kommentar dafuer verwies. Diese fuehrt fuer 'exec'
# ausschliesslich Befehlsverbote und keine einzige Pfadregel. Gemessen am 2026-09-12
# (B04, Laeufe B04-1 bis B04-3): "sed -i ... <kern>/VERSION" passiert den Hook. Was den
# Shell-Schreibweg aufhaelt, ist die Regelschicht - also Modellverhalten, [TEXTUELL].
# Die Fachmatrizen beider Packs weisen das bei B4 und B5 je Zugriffskanal aus
# (CR-2026-047, D-47); eine technische Durchsetzung braucht eine Isolationsschicht des
# Betriebssystems und ist unerhoben. CR-2026-056 aendert daran NICHTS - K-32 bleibt offen.
#
# Die LAGE des Kernverzeichnisses ist keine Eigenschaft eines Clients, sondern dieser
# Installation (<CORE_DIR>, docs/PLACEHOLDER_REGISTRY.md).
#
# 0.88.0: Bis dahin stand hier os.path.basename() ueber drei dirname-Aufrufe, mit der
# Begruendung, eine Umbenennung des Kerns erreiche den Hook damit von selbst. Sie tat
# es nicht: Der Kern liegt seit diesem Release unter `.koolie/core`, und basename()
# liefert davon "core". Der Schreibschutz des Kernverzeichnisses haette dann auf ein
# Verzeichnis `core/` in der Projektwurzel gezeigt, das es nicht gibt - eine Schranke,
# die nichts mehr schuetzt und dabei aussieht wie eine (D-299).
#
# Die Lage steht deshalb als Zeichenkette hier. Der Hook importiert bewusst nichts aus
# dem Kern: Er muss auch dann entscheiden, wenn eine Installation unvollstaendig ist.
# Pruefung 75 haelt diesen Wert gegen clientmap.CORE_REL und den KERN des Validators.
CORE_REL = ".koolie/core"
CORE_TIEFE = CORE_REL.count("/") + 1

# Die Projektwurzel aus demselben Ort: <WURZEL>/<CORE_DIR>/tests/scripts/dieses_skript.
# Die Zahl der Ebenen wird aus CORE_TIEFE gerechnet und NICHT im Quelltext gezaehlt:
# Bis 0.87.0 standen hier vier dirname-Aufrufe, und mit dem zweiten Segment des Kerns
# waeren es fuenf - vier haetten `.koolie/` als Projektwurzel geliefert, also die obere
# Freigabegrenze der Pfadaufloesung um eine Ebene zu tief gesetzt (D-299).
# Sie ist die obere Freigabegrenze der Pfadaufloesung und die Basis fuer relative Pfade,
# wenn das Ereignis kein cwd fuehrt. Bewusst aus dem eigenen Ort und NICHT aus einer
# Umgebungsvariablen: Ob ein Client <CLIENT>_PROJECT_DIR an den Hook-Prozess
# weiterreicht, ist dieselbe unbelegte Clientzusage, an der AP2-CC-13 haengen blieb
# (D-31). realpath, damit eine Installation hinter einer Verknuepfung vergleichbar bleibt.
_KERN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_wurzel = _KERN
for _ in range(CORE_TIEFE):
    _wurzel = os.path.dirname(_wurzel)
PROJEKTWURZEL = os.path.realpath(_wurzel)

# Werkzeugnamen je Verb. Der Hook darf sie nicht festschreiben: Das Manifest jedes
# Client Packs bildet die Verben der Kernquelle auf die Werkzeugnamen seines Clients ab
# (hook_tools), und diese Abbildung galt bisher nur fuer den Matcher der
# Hook-Konfiguration - nicht fuer die Pruefungen in diesem Skript. Folge: Bei einem
# Client, dessen Ausfuehrungswerkzeug nicht "exec" heisst, lief die Pfadpruefung fuer
# Shell-Befehle ins Leere (AP2-CC-16). Die Namen werden deshalb aus den Manifesten
# gelesen, wie Pruefung 14 die Clientnamen aus den Pack-Kennungen liest (D-28).
#
# Gelesen werden ALLE Packs, nicht nur das installierte: Das Skript wird von allen
# geteilt, und ein zusaetzlich erkannter Werkzeugname ist eine Verschaerfung, keine
# Lockerung - dieselbe Begruendung wie bei den Pfadmustern oben.
BASIS_WRITE_TOOLS = ("edit", "write", "notebookedit")
BASIS_EXEC_TOOLS = ("exec",)
# Lesende Werkzeuge werden allein an den Secret-Pfaden gemessen. D-30 hatte das bereits
# entschieden - "Secret-Pfade sind vertraulich und werden auch gegen lesende Werkzeuge
# durchgesetzt" -, der Code loeste es nicht ein: Ein Leseverb stand weder in der
# Hook-Quelle noch in einer Werkzeugliste, und ein Zugriff mit tool_name "read" lief
# mit Exit 0 durch. Beobachtet in AP2, als ein blockiertes "cat .env" den Agenten dazu
# brachte, dieselbe Datei mit dem Lesewerkzeug zu oeffnen (AP2-DD-11, D-33).
BASIS_READ_TOOLS = ("read",)
# Suchende Werkzeuge werden wie lesende an den Secret-Pfaden gemessen. Sie standen bis
# 0.29.0 in keiner Liste und in keinem hook_tools-Eintrag: Eine Suche ueber einen
# Secret-Pfad erreichte den Hook nicht einmal. Gemessen am 2026-09-12 (B04,
# tests/protocols/2026-09-12-B04-B05-gegenpruefung.md, Lauf B04-5); dieselbe Luecke wie
# AP2-DD-11, ein Werkzeug weiter, und derselbe Anspruch aus D-30.
#
# Eine Berechtigungsregel traegt hier nicht: Bei claude-code werten die Suchwerkzeuge
# keine Pfadregeln aus (AP2-CC-02), eine solche Regel waere angenommen und nie
# konsultiert. Der Hook ist fuer diesen Kanal die einzige technische Schranke
# (CR-2026-047 E3, D-47).
BASIS_SEARCH_TOOLS = ("search",)
# MCP-Werkzeuge haben keine festen Namen: Der Server waehlt sie, der Client stellt ein
# Praefix voran (claude-code: mcp__<server>__<werkzeug>). Erkannt wird deshalb am
# Praefix, das jedes Pack in hook_mcp_prefixes fuehrt (K-184, D-486). Die Basisliste ist
# leer: Ein Praefix, das kein Pack gemessen hat, waere eine Zusage ohne Mechanismus.
BASIS_MCP_PREFIXES = ()

# Die Felder von tool_input, die einen Pfad tragen. Sie entscheiden, welcher Wert
# zusaetzlich AUFGELOEST und dann noch einmal gegen die Muster gehalten wird - das ist
# die Pfadidentitaet aus D-63. Wie die Werkzeugnamen kommen sie aus den Manifesten
# (hook_path_fields), ueber dieser Basisliste und ueber alle Packs vereinigt.
#
# Die Basisliste muss gut sein: Ein Pack ohne den Eintrag faellt auf sie zurueck. Sie
# fuehrt deshalb die Feldnamen beider aufgezeichneter Schemata und die gaengigen Formen
# daneben. Ein zusaetzlich erkanntes Feld ist eine Verschaerfung.
BASIS_PATH_FIELDS = ("file_path", "filepath", "path", "paths", "file_paths",
                     "notebook_path", "target_file", "old_path", "new_path",
                     "source", "destination", "directory", "dir")


def _aus_manifesten() -> tuple:
    """(write-, exec-, read-, search-Namen, Pfadfelder) aus den Manifesten aller Packs.

    Faellt auf die Basisnamen zurueck, wenn kein Manifest lesbar ist: Ein Hook, der
    wegen einer fehlenden Datei gar nichts mehr blockiert, waere die schlechtere Lage.
    """
    schreiben = set(BASIS_WRITE_TOOLS)
    ausfuehren = set(BASIS_EXEC_TOOLS)
    lesen = set(BASIS_READ_TOOLS)
    suchen = set(BASIS_SEARCH_TOOLS)
    pfadfelder = set(BASIS_PATH_FIELDS)
    praefixe = set(BASIS_MCP_PREFIXES)

    def fertig():
        return (tuple(sorted(schreiben)), tuple(sorted(ausfuehren)),
                tuple(sorted(lesen)), tuple(sorted(suchen)), frozenset(pfadfelder),
                tuple(sorted(praefixe)))

    kern = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    packs = os.path.join(kern, "clients")
    try:
        eintraege = sorted(os.listdir(packs))
    except OSError:
        return fertig()
    for name in eintraege:
        pfad = os.path.join(packs, name, "manifest.json")
        if not os.path.isfile(pfad):
            continue
        try:
            with io.open(pfad, encoding="utf-8") as fh:
                daten = json.load(fh) or {}
        except (OSError, ValueError):
            continue
        abbildung = daten.get("hook_tools") or {}
        for verb, ziel in (("write", schreiben), ("exec", ausfuehren),
                           ("read", lesen), ("search", suchen)):
            for werkzeug in abbildung.get(verb) or []:
                if isinstance(werkzeug, str) and werkzeug.strip():
                    ziel.add(werkzeug.strip().lower())
        for feld in daten.get("hook_path_fields") or []:
            if isinstance(feld, str) and feld.strip():
                pfadfelder.add(feld.strip().lower())
        for praefix in daten.get("hook_mcp_prefixes") or []:
            if isinstance(praefix, str) and praefix.strip():
                praefixe.add(praefix.strip().lower())
    return fertig()


(WRITE_TOOLS, EXEC_TOOLS, READ_TOOLS, SEARCH_TOOLS, PATH_FIELDS,
 MCP_PREFIXES) = _aus_manifesten()

# Ein Shell-Befehl ist keine Pfadangabe: In "cat .env" steht der Pfad mitten im String,
# und die Pfadmuster verlangen einen Zeilenanfang oder ein Trennzeichen davor. Fuer
# ausfuehrende Werkzeuge wird die Eingabe deshalb zusaetzlich in Tokens zerlegt und
# jedes Token wie eine Pfadangabe geprueft (AP2-CC-15).
SHELL_TRENNER = re.compile(r"[\s;|&()<>\"'`,=]+")

# Wie viele Tokens eines Befehls hoechstens AUFGELOEST werden. Die Musterpruefung selbst
# ist unbegrenzt; gedeckelt ist nur der Teil, der das Dateisystem anfasst. Ohne Deckel
# koennte eine sehr lange Befehlszeile den Hook in den Zeitablauf laufen lassen - und ein
# Hook, der in den Zeitablauf laeuft, entscheidet nichts (AP2-CC-13).
TOKEN_DECKEL = 64

# Der Kernpfad hat seit 0.88.0 MEHRERE Segmente. re.escape() laesst den Schraegstrich
# stehen, und ein so gebautes Muster traefe unter Windows die Schreibweise mit
# Gegenschraegstrich nicht mehr - eine Schranke, an der man vorbeigeht, indem man
# anders tippt (D-277, die Lehre von B3). Die Segmente werden deshalb einzeln
# maskiert und mit einem Trenner verbunden, der beide Formen nimmt.
_CORE_MUSTER = r"[\\/]".join(re.escape(_s) for _s in CORE_REL.split("/"))

PROTECTED_WRITE_PATH_PATTERNS = [
    re.compile(_GRENZE + _CORE_MUSTER + r"[\\/]", re.I),
]

# DAS MANDAT (CR-2026-156, D-447). Ein Mandat ist die Erlaubnis eines Menschen, dass der
# Agent fuer eine begrenzte Zeit Entscheidungen in das Overlay eintraegt (Modus M6). Es
# liegt im Git-Verzeichnis des Projekts und NICHT im Arbeitsbaum: Es kann so nie
# versehentlich eingecheckt werden und damit auf einem anderen Arbeitsplatz gelten.
# Ohne Git-Verzeichnis gibt es kein Mandat - der Merge Request ist die Pruefung, die das
# Mandat voraussetzt. Die Werte stehen hier und in mandat.py; Pruefung 99 haelt sie
# gleich (der Hook importiert bewusst nichts aus dem Kern, siehe CORE_REL).
MANDAT_DATEI = "koolie-mandat.json"
MANDAT_HOECHSTDAUER_MIN = 480
MANDAT_UMFAENGE = {
    "overlay": ".koolie/project-overlay/",
    "dokumente": ".koolie/project-overlay/documents/",
}
# Datei und Befehl des Mandats sind fuer jede NICHT lesende Operation gesperrt - auch
# fuer einen Shell-Befehl, der sie nur nennt. Ein Agent, der sich sein Mandat selbst
# gibt, haette keines. Die Grenze ist dieselbe wie bei K-32: Ein Befehl, der den Namen
# verschleiert, entgeht dem Muster; getragen wird der Rest von der Regelschicht.
MANDATS_MUSTER = [
    re.compile(r"koolie-mandat", re.I),
    re.compile(r"koolie-modus", re.I),
    re.compile(r"(^|[\s\\/])mandat\.py", re.I),
]

# DIE MODUSBINDUNG (CR-2026-164, D-501, K-179). Dieselbe Bauform wie das Mandat, fuer die
# Modi, deren Schreibgrenze sich ohne Overlay-Pfadliste festmachen laesst: M1 schreibt
# nichts, M2 nur in die Plan-Ablage, die der Mensch beim Binden nennt. Der Mensch bindet
# im eigenen Terminal ('mandat.py modus'); ohne Bindung aendert sich nichts. Die Bindung
# trifft Schreibwerkzeuge - ein Shell-Befehl, der schreibt, entgeht ihr wie dem
# Kernschutz (D-30, K-32). Diese Grenze ist benannt, nicht verschwiegen.
#
# M3 BIS M5 (CR-2026-169, K-201). Ihre Schreibgrenze steht im Overlay: M3 <ALLOWED_PATHS>,
# M4 <TEST_PATHS>, M5 <DOC_PATHS>. Der Hook liest das Overlay trotzdem nicht - 'mandat.py
# modus' kopiert die Globs beim Binden in die Bindungsdatei ("pfade", bei M3 optional
# "umfang"), dazu <READ_ONLY_PATHS> ("nur_lesen"). Ein Ziel ist frei, wenn JEDE Lesart im
# Projekt liegt, auf ein Muster von "pfade" (und "umfang") passt und auf keines von
# "nur_lesen". Aendert sich das Overlay, gilt das erst nach neuem Binden.
MODUS_DATEI = "koolie-modus.json"
MODUS_GEBUNDEN = ("M1", "M2", "M3", "M4", "M5")
MODUS_MIT_PFADEN = ("M3", "M4", "M5")

# DIE UEBERTRAGUNG VON SECRETS NACH AUSSEN (CR-2026-164, D-503, K-94). Der eingebaute
# Skill 'upload-secrets' von devin-desktop liest eine Secret-Datei nicht mit einem
# Dateiwerkzeug: Er ruft die CLI des Clients, und die liest die Werte selbst und schickt
# sie an den Secrets-Speicher des Anbieters (erhoben am 2026-09-30 mit 'devin skills show
# upload-secrets', 3000.11.3). Ein Leseverbot der Berechtigungsschicht trifft diesen Weg
# nicht, und mit '--from-env <VAR>' steht nicht einmal ein Pfad im Befehl. Gesperrt wird
# deshalb der Befehl selbst - fuer jedes ausfuehrende Werkzeug, auch als Probelauf.
UEBERTRAGUNGS_MUSTER = [
    re.compile(r"\bcloud\s+drs\s+secret-create\b", re.I),
]
MANDAT_BEFEHL = ("python " + CORE_REL + "/mandat.py erteilen --rolle <Rolle> "
                 "--umfang overlay --minuten 60")


# Die eine Ausnahme: die Auskunft. 'mandat.py status' schreibt nichts, und der Client soll
# vor einer Arbeit in M6 selbst nachsehen koennen, statt es auf eine Sperre ankommen zu
# lassen. Genau diese Form und nichts dahinter - kein Semikolon, keine Verkettung.
MANDATSAUSKUNFT = re.compile(r"^\s*(python3?|py(\s+-3)?)\s+(\.[\\/])?\.koolie[\\/]core[\\/]mandat\.py\s+status\s*$", re.I)


def nur_mandatsauskunft(tool_input) -> bool:
    """Ist der Befehl allein 'mandat.py status'?

    Gemessen wird das Befehlsfeld, nicht jede Zeichenkette der Eingabe: claude-code
    schickt neben dem Befehl eine Beschreibung ("Mandatsstatus abfragen"), und die erste
    Fassung verlangte, dass JEDE Zeichenkette mit "mandat" genau der Befehl sei - sie
    sperrte damit die Auskunft, die sie freigeben sollte (gemessen am 2026-09-27 im Lauf
    sk013n01 der Messung zu 1.17.0). Die uebrigen Felder bleiben Pruefmaterial: Nennt die
    Beschreibung mandat.py, sperrt das Muster darunter wie bisher.
    """
    befehl = tool_input.get("command") if isinstance(tool_input, dict) else None
    return isinstance(befehl, str) and bool(MANDATSAUSKUNFT.match(befehl))


def git_verzeichnis():
    """Das Git-Verzeichnis des Projekts - oder None.

    '.git' ist ein Verzeichnis oder, bei einem zusaetzlichen Arbeitsbaum, eine Datei
    mit 'gitdir: <pfad>'. Der Hook ruft git bewusst nicht auf: Ein Prozessstart je
    Werkzeugaufruf kostet Zeit, und ein Hook im Zeitablauf entscheidet nichts.
    """
    punkt_git = os.path.join(PROJEKTWURZEL, ".git")
    if os.path.isdir(punkt_git):
        return punkt_git
    if os.path.isfile(punkt_git):
        try:
            with io.open(punkt_git, encoding="utf-8") as fh:
                inhalt = fh.read().strip()
        except OSError:
            return None
        if inhalt.lower().startswith("gitdir:"):
            ziel = inhalt[len("gitdir:"):].strip()
            if not os.path.isabs(ziel):
                ziel = os.path.join(PROJEKTWURZEL, ziel)
            return os.path.realpath(ziel)
    return None


def mandat_lesen():
    """Das gueltige Mandat als dict - oder None.

    Gueltig heisst: lesbar, eine Rolle, nur bekannte Umfaenge, ein Ende in der Zukunft
    und nicht weiter entfernt als die Hoechstdauer, und dieses Projekt. Jede Abweichung
    gilt als KEIN Mandat - ein kaputtes Mandat oeffnet nichts.
    """
    gd = git_verzeichnis()
    if not gd:
        return None
    try:
        with io.open(os.path.join(gd, MANDAT_DATEI), encoding="utf-8") as fh:
            daten = json.load(fh)
    except (OSError, ValueError):
        return None
    if not isinstance(daten, dict):
        return None
    rolle, umfang, bis = daten.get("rolle"), daten.get("umfang"), daten.get("bis")
    if not isinstance(rolle, str) or not rolle.strip():
        return None
    if (not isinstance(umfang, list) or not umfang
            or not all(isinstance(u, str) and u in MANDAT_UMFAENGE for u in umfang)):
        return None
    try:
        ende = datetime.datetime.strptime(str(bis), "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None
    jetzt = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    if ende <= jetzt or ende - jetzt > datetime.timedelta(minutes=MANDAT_HOECHSTDAUER_MIN + 1):
        return None
    projekt = daten.get("projekt")
    if (not isinstance(projekt, str)
            or os.path.normcase(os.path.realpath(projekt)) != os.path.normcase(PROJEKTWURZEL)):
        return None
    return daten


def mandat_deckt(rel: str, mandat) -> bool:
    """Deckt das Mandat den projektrelativen Pfad rel?"""
    if not mandat:
        return False
    rel = rel.replace("\\", "/")
    return any(rel.lower().startswith(MANDAT_UMFAENGE[u].lower()) for u in mandat["umfang"])


def modus_lesen():
    """Die gueltige Modusbindung als dict - oder None.

    Dieselben Bedingungen wie beim Mandat: lesbar, bekannter Modus, ein Ende in der
    Zukunft und nicht weiter als die Hoechstdauer, dieses Projekt. M2 braucht zusaetzlich
    eine projektrelative Plan-Ablage ausserhalb von .koolie/. Eine kaputte Bindung gilt
    als KEINE - sie sperrt dann nichts, und die Regelschicht traegt den Modus wie vor
    1.20.2. Das ist die schwaechere Seite, und sie ist gewaehlt: Eine Bindung ist eine
    zusaetzliche Sperre, kein Schutz, von dem etwas anderes abhaengt.
    """
    gd = git_verzeichnis()
    if not gd:
        return None
    try:
        with io.open(os.path.join(gd, MODUS_DATEI), encoding="utf-8") as fh:
            daten = json.load(fh)
    except (OSError, ValueError):
        return None
    if not isinstance(daten, dict) or daten.get("modus") not in MODUS_GEBUNDEN:
        return None
    try:
        ende = datetime.datetime.strptime(str(daten.get("bis")), "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None
    jetzt = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    if ende <= jetzt or ende - jetzt > datetime.timedelta(minutes=MANDAT_HOECHSTDAUER_MIN + 1):
        return None
    projekt = daten.get("projekt")
    if (not isinstance(projekt, str)
            or os.path.normcase(os.path.realpath(projekt)) != os.path.normcase(PROJEKTWURZEL)):
        return None
    if daten["modus"] == "M2":
        ablage = daten.get("ablage")
        if not isinstance(ablage, str) or not ablage.strip():
            return None
        ablage = ablage.replace("\\", "/").strip().strip("/") + "/"
        if (os.path.isabs(ablage) or ablage.startswith(("../", "./", ".koolie/"))
                or "/../" in "/" + ablage):
            return None
        daten["ablage"] = ablage
    if daten["modus"] in MODUS_MIT_PFADEN:
        for feld, pflicht in (("pfade", True), ("umfang", False), ("nur_lesen", False)):
            wert = daten.get(feld)
            if wert is None and not pflicht:
                daten[feld] = []
                continue
            if (not isinstance(wert, list) or (pflicht and not wert)
                    or not all(isinstance(g, str) and g.strip() for g in wert)):
                return None
    return daten


def glob_muster(glob: str):
    """Ein Glob des Overlays als regulaerer Ausdruck ueber den projektrelativen Pfad.

    '**' steht fuer beliebig viele Segmente (auch keines), '*' und '?' bleiben in einem
    Segment, ein Muster ohne Joker ist genau diese Datei. Klammern und Mengen kennt das
    Overlay nicht; sie gelten woertlich - ein Muster, das dadurch nichts trifft, sperrt
    mehr, nicht weniger. Ohne Gross- und Kleinschreibung wie jeder Pfadvergleich des
    Hooks (D-492). Dieselbe Funktion steht in mandat.py; Pruefung 99 haelt beide gleich.
    """
    g = glob.replace("\\", "/").strip()
    while g.startswith("./"):
        g = g[2:]
    g = g.lstrip("/")
    raus, i = "", 0
    while i < len(g):
        if g.startswith("**/", i):
            raus, i = raus + "(?:[^/]*/)*", i + 3
        elif g.startswith("**", i):
            raus, i = raus + ".*", i + 2
        elif g[i] == "*":
            raus, i = raus + "[^/]*", i + 1
        elif g[i] == "?":
            raus, i = raus + "[^/]", i + 1
        else:
            raus, i = raus + re.escape(g[i]), i + 1
    return re.compile("^" + raus + "$", re.I)


def glob_trifft(rel: str, globs: list) -> bool:
    """Passt der projektrelative Pfad (mit '/') auf eines der Muster?"""
    return any(glob_muster(g).match(rel) for g in globs)


def modus_erlaubt(rel: str, bindung: dict) -> bool:
    """Darf im gebundenen Modus unter diesem projektrelativen Pfad geschrieben werden?"""
    modus = bindung["modus"]
    if modus == "M1":
        return False
    if modus == "M2":
        return rel.lower().startswith(bindung["ablage"].lower())
    if not glob_trifft(rel, bindung["pfade"]):
        return False
    if bindung["umfang"] and not glob_trifft(rel, bindung["umfang"]):
        return False
    return not glob_trifft(rel, bindung["nur_lesen"])


# Die Dateikoepfe eines Patchtextes (openai-codex, apply_patch). Nur sie sind Ziele;
# was darunter steht, ist Inhalt.
PATCH_KOPF = re.compile(r"^\*\*\* (?:(?:Add|Update|Delete) File|Move to): (.+?)\s*$", re.M)


def ziele_der_schreiboperation(tool_input) -> list:
    """Die Ziele eines Schreibwerkzeugs: Pfadfelder, ein Patchtext durch seine Koepfe.

    Ein Pfadfeld mit Zeilenumbruch ist kein Pfad, sondern ein Patchtext. Traegt er
    keinen Kopf, bleibt er als Ganzes stehen - die strengere Lesart (D-449).
    """
    ziele = []
    for wert in pfadwerte(tool_input):
        if "\n" in wert:
            koepfe = PATCH_KOPF.findall(wert)
            ziele.extend(koepfe if koepfe else [wert])
        else:
            ziele.append(wert)
    return ziele


def hinweis(gesperrt: str, warum: str, loesung: str, folge: str) -> str:
    """Der Blockade-Hinweis (D-450): vier Zeilen, damit niemand nachfragen muss."""
    return (f"Gesperrt: {gesperrt}\nWarum: {warum}\nLoesung: {loesung}\n"
            f"Folge: {folge}")


# Zusätzliche projektspezifische Muster können über die Umgebungsvariable
# FW_HOOK_EXTRA_PATH_PATTERNS (durch ';' getrennte reguläre Ausdrücke) ergänzt werden.
# Auch sie laufen mit re.I: Ein Projekt meint sie als Verbot, und ein Verbot, das an der
# Schreibweise scheitert, ist keines (D-63).
for _nr, extra in enumerate(
        filter(None, os.environ.get("FW_HOOK_EXTRA_PATH_PATTERNS", "").split(";")), 1):
    try:
        PROTECTED_PATH_PATTERNS.append(re.compile(extra, re.I))
    except re.error:
        # Der Wert wird nicht wiedergegeben: Projektspezifische Pfadmuster tragen Projekt-,
        # Kunden- und Hostnamen - dieselbe Datenart wie die Sperrbegriffe (B03, D-39). Die
        # Position macht das Muster in der Umgebungsvariablen auffindbar.
        print(f"[koolie-hook] Ungueltiges Zusatzmuster an Position {_nr} ignoriert "
              f"(Wert nicht wiedergegeben).", file=sys.stderr)


def iter_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from iter_strings(k)
            yield from iter_strings(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from iter_strings(v)


def shell_tokens(strings):
    for s in strings:
        for token in SHELL_TRENNER.split(s):
            if token:
                yield token


def fail_closed() -> bool:
    """Wahr, wenn eine unpruefbare Eingabe blockiert statt durchgelassen wird.

    Der Schalter steht im Aufrufargument, nicht in der Umgebung. Das Argument ist Teil
    des Kommandos, das die Hook-Konfiguration fuehrt und der Client ohnehin ausfuehrt:
    Laeuft der Hook - was Pruefung 15 an seiner Wirkung belegt -, dann kommt es an. Eine
    Umgebungsvariable haette die Zusage zusaetzlich davon abhaengig gemacht, dass der
    Client sie an den Hook-Prozess weiterreicht; das ist eine Clientzusage, die fuer
    keines der Packs belegt ist, und genau die Art unbelegter Annahme, an der AP2-CC-13
    acht Releases lang hing (D-31).

    Die Umgebungsvariable bleibt zusaetzlich wirksam, damit eine bestehende Installation
    fail-closed erproben kann, ohne neu installiert zu werden.
    """
    return "--fail-closed" in sys.argv[1:] or os.environ.get("FW_HOOK_FAIL_CLOSED") == "1"


# DIE SPERRFORMEN, UND WARUM ES MEHR ALS EINE GIBT (CR-2026-133, D-347).
# Eine Sperre ist eine Aussage an den Client, und ihre Form ist clientgebunden. Bis
# 1.3.0 kannte dieses Skript genau eine: das Objekt {"decision": "block"} auf stdout
# und Exit-Code 2. Am 2026-09-23 ist an einer realen Installation von openai-codex
# gemessen worden, was diese Form dort bewirkt: NICHTS. Der Client meldet den Hook als
# fehlgeschlagen und fuehrt die Operation aus - im Lauf kam der Koederinhalt woertlich
# heraus. Dieselbe Sperre in der Form, die dieser Client liest, blockiert; und sie
# blockiert auch in dem Modus, der Rueckfragen und Sandkasten abschaltet.
#   ➡️ Ein Hook, der laeuft, dessen Sperrform der Client aber nicht liest, ist eine
#      Zusage ohne Mechanismus - und nichts meldet es.
# Welche Form gilt, sagt das Client Pack (hook_block_form im Manifest); die Abbildung
# haengt sie als --sperrform an das Kommando, aus demselben Grund wie --fail-closed
# (D-31). Ohne Angabe bleibt es bei der bisherigen Form - ein Pack erbt die neue Form
# nicht durch Schweigen.
#
# DIE DRITTE FORM (CR-2026-150, D-417), gemessen am 2026-09-26 an kiro-cli 2.24.1 in
# einer interaktiven Sitzung: Der Client wertet bei PreToolUse den Exit-Code 2 als
# Sperre - aber er uebergibt dem Aufrufer als Grund allein stderr, und ein LEERER Grund
# laesst die Operation laufen. Mit der Standardform (Grund nur auf stdout) endete der
# Hook mit Exit 2, und der Koederinhalt kam heraus; derselbe Lauf mit dem Grund auf
# stderr wurde abgewiesen. Dieselbe Bauform wie D-347: ein Hook, der laeuft und sperrt,
# und ein Client, der die Sperre nicht liest.
#
# DIE VIERTE FORM (CR-2026-155, D-441), gemessen am 2026-09-26 an cursor-agent
# 2026.09.26: Der Client sperrt bei Exit 2 - aber mit failClosed wertet er einen Hook,
# der OHNE AUSGABE endet, als fehlgeschlagen und sperrt die Operation. Der saubere
# Durchlass muss hier also etwas sagen. Er sagt "{}": eine gueltige Antwort ohne
# Entscheidung. Ein "allow" waere mehr, als der Hook weiss - der Client fuehrt die
# Antworten aller Hooks zusammen, und eine Freigabe koennte eine Rueckfrage uebergehen,
# die die Berechtigungsschicht verlangt. Gesperrt wird mit permission deny UND Exit 2.
SPERRFORMEN = ("decision-block", "hook-specific-output", "stderr-grund", "permission-json")


# DAS ENTSCHEIDUNGSPROTOKOLL (K-192, D-487). Der Zustand der laufenden Entscheidung -
# gesetzt in main(), sobald das Ereignis gelesen ist; bis dahin ist nichts zu protokollieren
# ausser dem unpruefbaren Fall, und der steht ohne Werkzeugnamen.
PROTOKOLL_DATEI = "koolie-hook.jsonl"
PROTOKOLL_HOECHSTGROESSE = 5 * 1024 * 1024
OVERLAY_MANIFEST = ".koolie/project-overlay/overlay-manifest.yaml"
PROTOKOLL_SCHALTER = re.compile(r"^hook_protokoll:\s*[\"']?([A-Za-z]+)[\"']?\s*(#.*)?$",
                                re.M)
_ENTSCHEIDUNG = {"ereignis": False, "werkzeug": "", "verb": "", "probe": False}


def protokoll_an() -> bool:
    """Nur fuer ein Ereignis eines Clients, und nur, wenn das Overlay es nicht abschaltet.

    Ein Aufruf ohne hook_event_name ist eine Sonde des Validators oder ein Handaufruf -
    er gehoert nicht in das Protokoll des Projekts (und der Validator schriebe sonst bei
    jedem Lauf in das Git-Verzeichnis, das er prueft).
    """
    if not _ENTSCHEIDUNG["ereignis"]:
        return False
    try:
        with io.open(os.path.join(PROJEKTWURZEL, OVERLAY_MANIFEST), encoding="utf-8-sig") as fh:
            m = PROTOKOLL_SCHALTER.search(fh.read())
    except OSError:
        m = None
    return not (m and m.group(1).lower() == "aus")


def protokollieren(ergebnis: str, grund: str = "") -> None:
    """Eine Zeile - nie der Inhalt, nie ein Pfadwert. Ein Fehler aendert nichts."""
    try:
        if not protokoll_an():
            return
        gitdir = git_verzeichnis()
        if not gitdir:
            return
        ziel = os.path.join(gitdir, PROTOKOLL_DATEI)
        if os.path.isfile(ziel) and os.path.getsize(ziel) > PROTOKOLL_HOECHSTGROESSE:
            os.replace(ziel, ziel + ".1")
        erste = grund.strip().splitlines()[0] if grund.strip() else ""
        if erste.startswith("Gesperrt: "):
            erste = erste[len("Gesperrt: "):]
        zeile = {"zeit": datetime.datetime.now(datetime.timezone.utc).strftime(
                     "%Y-%m-%dT%H:%M:%SZ"),
                 "werkzeug": _ENTSCHEIDUNG["werkzeug"], "verb": _ENTSCHEIDUNG["verb"],
                 "ergebnis": ergebnis, "grund": erste[:200]}
        if _ENTSCHEIDUNG["probe"]:
            zeile["probe"] = True
        with io.open(ziel, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(zeile, ensure_ascii=False) + "\n")
    except Exception:  # noqa: BLE001 - das Protokoll entscheidet nichts
        return


def durchlassen(ergebnis: str = "durchgelassen", grund: str = "") -> None:
    """Sauberer Ausgang: kein Fund. Bei permission-json mit einer leeren Antwort.

    Auch der unpruefbare Fall ohne --fail-closed endet hier - mit seinem eigenen Ergebnis
    im Protokoll (D-487), aber durch dieselbe Antwort an den Client.
    """
    protokollieren(ergebnis, grund)
    if sperrform() == "permission-json":
        print("{}")
    sys.exit(0)


def sperrform() -> str:
    argv = sys.argv[1:]
    if "--sperrform" in argv:
        i = argv.index("--sperrform")
        if i + 1 < len(argv) and argv[i + 1] in SPERRFORMEN:
            return argv[i + 1]
    return "decision-block"


def block(reason: str) -> None:
    protokollieren("gesperrt", reason)
    form = sperrform()
    if form == "hook-specific-output":
        # Diese Form traegt ihren Grund IM Objekt und endet mit Exit 0: Der Client
        # liest die Entscheidung, nicht den Exit-Code. Ein Exit 2 waere hier ein
        # fehlgeschlagener Hook und damit eine durchgelassene Operation.
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason}}, ensure_ascii=False))
        sys.exit(0)
    if form == "permission-json":
        # Beide Signale: die Entscheidung im Objekt und Exit 2. Der Client wertet Exit 2
        # als Sperre; der Grund erreicht Nutzer und Modell ueber die beiden Meldungsfelder.
        print(json.dumps({"permission": "deny", "user_message": reason,
                          "agent_message": reason}, ensure_ascii=False))
        sys.exit(2)
    if form == "stderr-grund":
        # Der Grund steht auf stderr und ist NIE leer - ein leerer Grund ist bei diesem
        # Client eine durchgelassene Operation (D-417). stdout bleibt leer.
        sys.stderr.write(reason.strip() or "Framework-Regel: gesperrt.")
        sys.stderr.write("\n")
        sys.exit(2)
    print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
    sys.exit(2)


class Unpruefbar(Exception):
    """Die Eingabe laesst sich nicht pruefen - der dritte Ausgang neben sauber und Fund.

    Der Unterschied ist die ganze Sache an D-61: 'Nichts gefunden' und 'nicht gesucht'
    sahen bis 0.33.0 gleich aus (Exit 0), und das war der Weg, auf dem sechs
    Eingabeformen an --fail-closed vorbeikamen.

    Der Grund nennt eine KATEGORIE, nie einen Wert: Eine unpruefbare Eingabe kann
    Projekt-, Kunden- und Hostnamen tragen, und ein Schutzlauf, der sie ausgibt, ist
    genau der Befund, den D-39 abgestellt hat.
    """


def unpruefbar(grund: str) -> None:
    """fail-closed: blockieren. Sonst: warnen und durchlassen."""
    if fail_closed():
        block(hinweis(
            f"eine Werkzeugeingabe, die der Schutz-Hook nicht pruefen kann ({grund}).",
            "Ungeprueft laesst der Hook nichts durch (fail-closed); moeglicherweise hat "
            "sich das Eingabeschema des Clients geaendert.",
            "Denselben Schritt mit einem anderen Werkzeug versuchen (etwa dem "
            "Dateiwerkzeug statt der Shell); bleibt es gesperrt, die Fundstelle dem "
            f"Framework Owner melden ({CORE_REL}/governance/FEEDBACK_PROCESS.md).",
            "Die Operation laeuft nicht; am Projekt aendert sich nichts."))
    print(f"[koolie-hook] Eingabe nicht pruefbar ({grund}); Schema gegen aktuelle "
          f"Clientdokumentation pruefen.", file=sys.stderr)
    durchlassen("unpruefbar-durchgelassen", "Gesperrt: " + grund)


# ---------------------------------------------------------------- Stufe 1: Ereignis

def ereignis_lesen(raw: str) -> tuple:
    """(tool_name klein, tool_input) - oder Unpruefbar.

    Ein Ereignis ist ein JSON-OBJEKT mit einem nicht leeren tool_name vom Typ
    Zeichenkette und einem tool_input, das vorhanden und ein Objekt ist. Zusaetzliche,
    unbekannte Felder bleiben ausdruecklich zulaessig: Eine additive Erweiterung des
    Clients darf den Hook nicht ausfallen lassen (CR-2026-056 E1).

    Warum tool_input Pflicht ist: Geprueft wird seit D-62 nur noch die Operation. Fehlt
    das Feld, in dem sie steht, kann der Hook nicht wissen, ob die Eingabe harmlos ist
    oder ihre Pfade woanders fuehrt. Genau das ist ein unpruefbarer Fall.
    """
    if not raw.strip():
        raise Unpruefbar("leere Eingabe")
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        raise Unpruefbar("nicht als JSON lesbar")
    if not isinstance(payload, dict):
        raise Unpruefbar(f"JSON-Wurzel ist kein Objekt, sondern {type(payload).__name__}")
    tool_name = payload.get("tool_name")
    if not isinstance(tool_name, str) or not tool_name.strip():
        raise Unpruefbar("tool_name fehlt, ist leer oder keine Zeichenkette")
    if "tool_input" not in payload:
        raise Unpruefbar("tool_input fehlt")
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        raise Unpruefbar(f"tool_input ist kein Objekt, sondern "
                         f"{type(tool_input).__name__}")
    basis = payload.get("cwd")
    if not isinstance(basis, str) or not basis.strip():
        basis = PROJEKTWURZEL
    _ENTSCHEIDUNG["ereignis"] = isinstance(payload.get("hook_event_name"), str)
    _ENTSCHEIDUNG["probe"] = payload.get("koolie_probe") is True
    _ENTSCHEIDUNG["werkzeug"] = tool_name.strip().lower()[:120]
    return tool_name.strip().lower(), tool_input, basis


# --------------------------------------------------------------- Stufe 2: Operation

def verb_von(tool_name: str) -> str:
    """Das Verb der Operation - oder 'unbekannt'.

    'unbekannt' wird nach der STRENGSTEN Liste gemessen, einschliesslich
    Kernverzeichnis. Bis 0.33.0 uebersprang ein unbekannter Name die Pfadpruefung ganz,
    und der Fall ohne Namen bekam zwar die mittlere Liste, aber nicht die strengste -
    obwohl der Kommentar daneben genau das behauptete.

    Blockiert wird ein unbekannter Name NICHT (CR-2026-056 E2). Das haenge den Hook
    daran, dass der Client seinen Matcher einhaelt; der Matcher wird zwar aus hook_tools
    erzeugt, aber dass ein Client ihn befolgt, ist eine Clientzusage - dieselbe Art
    unbelegter Annahme wie bei AP2-CC-13 (D-31).
    """
    if tool_name in WRITE_TOOLS:
        return "write"
    if tool_name in EXEC_TOOLS:
        return "exec"
    if tool_name in READ_TOOLS:
        return "read"
    if tool_name in SEARCH_TOOLS:
        return "search"
    if any(tool_name.startswith(p) for p in MCP_PREFIXES):
        return "mcp"
    return "unbekannt"


def pfadwerte(obj) -> list:
    """Die Werte aus tool_input, deren Feldname einen Pfad ankuendigt - rekursiv."""
    treffer = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str) and k.strip().lower() in PATH_FIELDS:
                treffer.extend(s for s in iter_strings(v) if s.strip())
            else:
                treffer.extend(pfadwerte(v))
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            treffer.extend(pfadwerte(v))
    return treffer


def sieht_nach_pfad_aus(token: str) -> bool:
    r"""Grobfilter fuer Befehlstokens - er entscheidet nur, was AUFGELOEST wird.

    Die Musterpruefung sieht jedes Token; hier geht es allein darum, welche davon das
    Dateisystem anfassen. Ausgenommen bleiben Netz- und Geraeteformen (\\\\server\\share,
    //host/pfad, schema://...): Eine Aufloesung darauf kann in eine Netzabfrage laufen,
    und ein Hook, der in den Zeitablauf laeuft, entscheidet nichts (AP2-CC-13). Ihr
    Rohtext wird weiterhin gegen die Muster gehalten.
    """
    if token.startswith("\\\\") or token.startswith("//") or "://" in token:
        return False
    return ("/" in token or "\\" in token or token.startswith(".")
            or bool(re.match(r"^[A-Za-z]:", token)))


def aufloesen(wert: str, basis: str) -> str:
    r"""Der reale Pfad hinter einer Angabe - oder Unpruefbar.

    Gemessen (tests/protocols/2026-09-13-B06-gegenpruefung.md, Abschnitt 4):
    os.path.realpath fuehrt Grossschreibung, den 8.3-Kurznamen, eine Junction,
    Punktsegmente, einen Punkt oder ein Leerzeichen am Ende und den Datenstrom-Zusatz
    ::$DATA auf die Standardschreibweise zurueck - auch fuer ein nicht existierendes
    Ziel ueber seinen existierenden Elternpfad. Jede dieser Varianten bezeichnete
    dieselbe Datei (mit os.path.samefile vorgeprueft) und wurde bis 0.33.0 anders
    entschieden.

    NICHT aufgeloest wird der Geraetepfad-Praefix: \\?\ ueberlebt realpath und wird
    deshalb vorher entfernt; der Geraetenamensraum \\.\ bezeichnet keine Projektdatei
    und gilt als unpruefbar (CR-2026-056 E5).
    """
    w = wert.strip()
    if not w:
        raise Unpruefbar("leerer Pfadwert")
    if w.startswith("\\\\.\\") or w.startswith("//./"):
        raise Unpruefbar("Geraetepfad im \\\\.\\-Namensraum")
    if w[:8].upper() == "\\\\?\\UNC\\":
        w = "\\\\" + w[8:]
    elif w.startswith("\\\\?\\"):
        w = w[4:]
    try:
        if not os.path.isabs(w):
            w = os.path.join(basis, w)
        return os.path.realpath(w)
    except (OSError, ValueError):
        raise Unpruefbar("Pfadwert nicht aufloesbar")


# Die POSIX-Schreibweise eines Laufwerks: /c/... (MSYS, Git Bash). Nur unter Windows ein
# Doppelsinn - unter POSIX ist /c/ ein gewoehnlicher Pfad.
MSYS_LAUFWERK_RE = re.compile(r"^/([A-Za-z])(?=/|$)")


def lesarten(wert: str, basis: str) -> list:
    r"""Alle realen Pfade, die eine Angabe bezeichnen kann - die strengere gewinnt.

    ZWEI LESARTEN VON /c/... (CR-2026-163, D-491, K-96). Python unter Windows liest
    /c/x als C:\c\x, und so liest es auch devin-desktop (D-285). Eine Shell unter MSYS
    und ein Client, der ihre Ausgabe weiterreicht, meinen C:\x. Gemessen am 2026-09-30:
    Ein Schreibwerkzeug auf /c/<projekt>/KOOLIE~1/core/VERSION ging mit Exit 0 durch,
    dieselbe Angabe in Windows-Form sperrte. Der Pfad C:\c\... existiert nicht, realpath
    loeste den Kurznamen deshalb nicht auf, und der Pfad galt als ausserhalb des
    Projekts. Der Ort ist die Aufloesung (D-63), nicht die Musterliste: Welche Lesart der
    Client waehlt, weiss der Hook nicht - er misst beide.

    GRENZE, BENANNT: /cygdrive/c/ und /mnt/c/ sind nicht gemessen und bleiben bei der
    einen Lesart.
    """
    echt = aufloesen(wert, basis)
    m = MSYS_LAUFWERK_RE.match(wert.strip()) if os.name == "nt" else None
    if not m:
        return [echt]
    msys = aufloesen(m.group(1) + ":" + (wert.strip()[2:] or "/"), basis)
    return [msys] if os.path.normcase(msys) == os.path.normcase(echt) else [msys, echt]


def innerhalb(pfad: str, wurzel: str) -> bool:
    """Ist pfad ein Kind von wurzel? Kein Praefixvergleich.

    Ein Verzeichnis mit aehnlichem Namensanfang ist kein Kind des erlaubten
    Verzeichnisses - deshalb commonpath und nicht startswith.
    """
    try:
        return os.path.commonpath([os.path.normcase(pfad),
                                   os.path.normcase(wurzel)]) == os.path.normcase(wurzel)
    except ValueError:
        return False  # verschiedene Laufwerke


def aufgeloestes_material(werte, basis: str) -> tuple:
    """(Material fuer alle Muster, Material nur fuer die Secret-Muster).

    Ein aufgeloester Pfad INNERHALB der Projektwurzel wird projektrelativ gemessen -
    in der Form also, fuer die die Muster geschrieben sind. Ein Pfad AUSSERHALB wird
    absolut gemessen und nur gegen die Secret-Muster: Ein Secret bleibt ausserhalb ein
    Secret, ein '.koolie/project-overlay/' ausserhalb der Projektwurzel ist nicht unseres.
    """
    voll, nur_secret = [], []
    for nr, wert in enumerate(werte, 1):
        try:
            alle = lesarten(wert, basis)
        except Unpruefbar as fehler:
            raise Unpruefbar(f"{fehler.args[0]} an Position {nr} der Pfadfelder")
        for echt in alle:
            if innerhalb(echt, PROJEKTWURZEL):
                rel = os.path.relpath(echt, PROJEKTWURZEL)
                voll.append(rel)
            else:
                nur_secret.append(echt)
    return voll, nur_secret


def eingabe_lesen() -> str:
    """Die Hook-Eingabe als Text - UTF-8, JEDES vorangestellte BOM entfernt.

    WARUM NICHT sys.stdin.read() (CR-2026-155, D-441). Gemessen am 2026-09-26 an
    cursor-agent 2026.09.26 unter Windows: Der Client reicht die Eingabe durch eine
    PowerShell-Huelle weiter, und die stellt ihr ein UTF-8-BOM voran. sys.stdin.read()
    dekodiert unter Windows ausserdem mit der Codepage des Systems - aus dem BOM wurden
    drei Zeichen vor der oeffnenden Klammer, json.loads scheiterte, und der Hook sperrte
    fail-closed JEDE Operation, auch das Lesen einer harmlosen Datei. JSON ist UTF-8; die
    Codepage ist nur der Rueckfall fuer eine Eingabe, die kein gueltiges UTF-8 ist.

    ZWEI BOM (CR-2026-157, D-463). Gemessen am 2026-09-28 an derselben Clientversion: Die
    Eingabe kam mit ZWEI vorangestellten BOM an ('EF BB BF EF BB BF'). 'utf-8-sig' nimmt
    genau eines weg; das zweite blieb als Zeichen vor der Klammer, und der Hook sperrte
    wieder fail-closed jede Operation. Ein BOM ist an dieser Stelle nie Inhalt - weg mit
    allen.
    """
    puffer = getattr(sys.stdin, "buffer", None)
    if puffer is None:
        return sys.stdin.read().lstrip("﻿")
    roh = puffer.read()
    try:
        return roh.decode("utf-8-sig").lstrip("﻿")
    except UnicodeDecodeError:
        return roh.decode(sys.getfilesystemencoding() or "utf-8", errors="replace").lstrip("﻿")


# ------------------------------------------------------------------ Stufe 3: Regeln

def main() -> None:
    try:
        tool_name, tool_input, basis = ereignis_lesen(eingabe_lesen())
    except Unpruefbar as fehler:
        unpruefbar(fehler.args[0])
        return

    verb = verb_von(tool_name)
    _ENTSCHEIDUNG["verb"] = verb
    # 'unbekannt' zaehlt bei jeder Frage zur strengeren Seite: schreibend wie ein
    # Schreibwerkzeug, tokenisiert wie ein Befehl. Eine unbekannte Operation als lesend
    # zu behandeln, waere die Annahme zugunsten des Zugriffs.
    schreibend = verb in ("write", "unbekannt")
    tokenisieren = verb in ("exec", "unbekannt")

    # Geprueft wird die OPERATION, nicht der Umschlag (D-62). cwd ist Aufloesungsbasis
    # und niemals Pruefmaterial: Bis 0.33.0 lief transcript_path als Pruefmaterial mit
    # und blockierte bei claude-code jeden Schreibzugriff.
    strings = list(iter_strings(tool_input))

    for label, pattern in SECRET_PATTERNS:
        if any(pattern.search(s) for s in strings):
            block(hinweis(
                f"eine Werkzeugeingabe mit einem Muster der Kategorie '{label}'.",
                "Secrets duerfen nicht verarbeitet werden "
                f"({CORE_REL}/framework/core/02-privacy.md, Abschnitt 5).",
                "Den Wert entfernen oder durch einen Platzhalter ersetzen. Ist es ein "
                "echtes Secret: Sitzung anhalten und die Fundstelle der Sicherheitsrolle "
                "des Projekts melden.",
                "Die Operation laeuft nicht; ohne das Muster geht sie durch."))

    # Das Mandat gibt sich der Agent nicht selbst (D-447): Datei und Befehl sind fuer
    # jede nicht lesende Operation gesperrt, gemessen am Rohtext UND an den Tokens.
    auskunft = verb == "exec" and nur_mandatsauskunft(tool_input)
    if verb not in ("read", "search"):
        # Bei einem MCP-Werkzeug zaehlen nur die Pfadfelder: Eine Doku-Seite, die den
        # Mandatsbefehl beschreibt, erteilt keines; ein Dateisystem-Server, der die
        # Mandatsdatei schreibt, nennt sie in einem Pfadfeld (D-486).
        mandatsmaterial = (pfadwerte(tool_input) if verb == "mcp" else
                           strings + (list(shell_tokens(strings)) if tokenisieren else []))
        for s in mandatsmaterial:
            if auskunft and s in (tool_input["command"],) + tuple(
                    shell_tokens([tool_input["command"]])):
                continue
            if any(p.search(s) for p in MANDATS_MUSTER):
                block(hinweis(
                    "das Anlegen, Aendern oder Aufrufen eines Mandats "
                    f"({CORE_REL}/mandat.py, {MANDAT_DATEI}).",
                    "Ein Mandat erteilt nur der Mensch - ein Agent, der es sich selbst "
                    "gibt, haette keines (Modus M6).",
                    f"Die Person fuehrt im eigenen Terminal aus: {MANDAT_BEFEHL}",
                    "Danach darf der Agent im Umfang des Mandats in das Overlay "
                    "schreiben; 'mandat.py beenden' hebt es auf. Die Auskunft darf auch "
                    f"der Agent einholen, als einzelner Befehl ohne Verkettung: python "
                    f"{CORE_REL}/mandat.py status"))

    if tokenisieren and any(p.search(s) for p in UEBERTRAGUNGS_MUSTER for s in strings):
        block(hinweis(
            "das Hochladen von Secrets zu einem Dienst ausserhalb des Projekts "
            "(cloud drs secret-create).",
            "Secrets verlassen das Projekt nie ueber den KI-Client - auch nicht verschluesselt "
            f"und auch nicht als Probelauf ({CORE_REL}/framework/core/02-privacy.md, K3).",
            "Die Person laedt Secrets selbst hoch, im eigenen Terminal und nach den Regeln "
            "der Organisation.",
            "Die Operation laeuft nicht; nichts wird uebertragen."))

    # Das Material der Pfadpruefung. Ein Schreibwerkzeug wird an seinen ZIELEN gemessen,
    # nicht an seinem Inhalt (D-449); ein unbekanntes Werkzeug an allem.
    if verb == "write":
        ziele = ziele_der_schreiboperation(tool_input)
        if not ziele:
            unpruefbar("Schreibwerkzeug ohne erkanntes Pfadfeld")
            return
        zu_pruefen = list(ziele)
    elif verb == "mcp":
        # Nur die Pfadfelder, nicht der Inhalt: Eine Notiz, die '.env' als Wort nennt,
        # liest keine Datei (D-486). Die Secret-Muster fuer den INHALT liefen oben.
        ziele = []
        zu_pruefen = pfadwerte(tool_input)
    else:
        ziele = []
        zu_pruefen = list(strings)
    if tokenisieren:
        # Bei einem ausfuehrenden Werkzeug steht der Pfad mitten im Befehl; die
        # Pfadmuster verlangen davor einen Zeilenanfang oder ein Trennzeichen. Die
        # Eingabe wird deshalb zusaetzlich tokenisiert (AP2-CC-15).
        tokens = list(shell_tokens(strings))
        zu_pruefen += tokens
        kandidaten = [t for t in tokens if sieht_nach_pfad_aus(t)][:TOKEN_DECKEL]
    else:
        kandidaten = []

    kandidaten += ziele if verb == "write" else pfadwerte(tool_input)

    try:
        aufgeloest_voll, aufgeloest_secret = aufgeloestes_material(kandidaten, basis)
    except Unpruefbar as fehler:
        unpruefbar(fehler.args[0])
        return

    # Zwei Schutzziele, zwei Listen (D-30): Ein ausfuehrendes, lesendes oder suchendes
    # Werkzeug wird an den Secret-Pfaden gemessen, nicht an den Strukturpfaden - ein
    # Befehl darf den Kern lesen, ein Secret nie. Fuer schreibende und unbekannte
    # Operationen gelten beide Listen. Ohne die Trennung blockierte ein 'git diff' auf
    # einen Kernpfad oder das Lesen einer Regeldatei, also Operationen, die das
    # Framework voraussetzt.
    muster = PROTECTED_PATH_PATTERNS if schreibend else SECRET_PATH_PATTERNS

    # Die Ziele, die ein gueltiges Mandat deckt - nur fuer ein ERKANNTES
    # Schreibwerkzeug. Gedeckt ist ein Ziel, dessen aufgeloester Pfad im Umfang liegt;
    # aufgehoben wird fuer dieses Ziel allein das Overlay-Muster (D-447).
    mandat = mandat_lesen() if verb == "write" else None
    gedeckt = set()
    if mandat:
        for roh in ziele:
            try:
                alle = lesarten(roh, basis)
            except Unpruefbar:
                continue
            for echt in alle:
                if innerhalb(echt, PROJEKTWURZEL):
                    rel = os.path.relpath(echt, PROJEKTWURZEL)
                    if mandat_deckt(rel, mandat):
                        gedeckt.update((roh, rel))

    for s in zu_pruefen + aufgeloest_voll:
        for pattern in muster:
            if pattern is OVERLAY_MUSTER and s in gedeckt:
                continue
            if not pattern.search(s):
                continue
            if pattern is OVERLAY_MUSTER:
                deckung = (" Das bestehende Mandat deckt dieses Ziel nicht (Umfang: %s)."
                           % ", ".join(mandat["umfang"])) if mandat else ""
                block(hinweis(
                    "Schreiben in .koolie/project-overlay/.",
                    "Overlay-Aenderungen entscheidet der Mensch; der Agent traegt sie "
                    "nur mit Mandat ein (Modus M6, V10)." + deckung,
                    f"Die Person fuehrt im eigenen Terminal aus: {MANDAT_BEFEHL} "
                    "(nur die Projektdokumente: --umfang dokumente).",
                    "Fuer die Dauer des Mandats schreibt der Agent dort direkt; jede "
                    "Aenderung steht im Diff und wird im Merge Request geprueft. Das "
                    "Mandat endet von selbst oder mit 'mandat.py beenden'."))
            if pattern in SECRET_PATH_PATTERNS:
                block(hinweis(
                    "ein Zugriff auf einen Secret-Pfad.",
                    "Secrets duerfen nicht verarbeitet werden "
                    f"({CORE_REL}/framework/core/02-privacy.md, Abschnitt 5).",
                    "Mit einer Beispieldatei ohne echte Werte arbeiten (etwa .env.example "
                    "mit Platzhaltern) oder die Aufgabe ohne diese Datei loesen.",
                    "Die Operation laeuft nicht; die Datei bleibt unberuehrt."))
            block(hinweis(
                "Schreiben auf einen geschuetzten Pfad (Wurzel-Anweisungsdatei, "
                "Laufzeitschicht oder framework/core/).",
                "Diese Dateien erzeugt der Installer aus Kern und Overlay; eine Aenderung "
                "von Hand ginge beim naechsten Update verloren.",
                "Projektwerte im Overlay eintragen (Modus M6) und danach im eigenen "
                f"Terminal 'python {CORE_REL}/install.py --update --target .' ausfuehren; "
                "eine Regelaenderung als Rueckmeldung an den Framework Owner "
                f"({CORE_REL}/governance/FEEDBACK_PROCESS.md).",
                "Die Operation laeuft nicht; die Laufzeitschicht bleibt die erzeugte."))
    for s in aufgeloest_secret:
        for pattern in SECRET_PATH_PATTERNS:
            if pattern.search(s):
                block(hinweis(
                    "ein Zugriff auf einen Secret-Pfad ausserhalb der Projektwurzel.",
                    "Secrets duerfen nicht verarbeitet werden "
                    f"({CORE_REL}/framework/core/02-privacy.md, Abschnitt 5).",
                    "Die Aufgabe ohne diese Datei loesen; einen benoetigten Wert gibt "
                    "die Person selbst ein.",
                    "Die Operation laeuft nicht; die Datei bleibt unberuehrt."))

    # Schreiboperationen zusaetzlich auf das gesamte Kernverzeichnis blockieren. Das
    # Kernverzeichnis gehoert dem Framework Owner und wird ausschliesslich ueber ein
    # Release ausgetauscht - auch die Skripte darin, die genau diese Zusagen durchsetzen.
    #
    # 'unbekannt' steht hier mit, und darin liegt die Berichtigung aus B06: Bis 0.33.0
    # haengte diese Pruefung an 'tool_name in WRITE_TOOLS', waehrend der Kommentar drei
    # Zeilen darueber die unbekannte Operation zur strengeren erklaerte. Sie war die
    # einzige, bei der der Kern ungeschuetzt blieb.
    if schreibend:
        for s in zu_pruefen + aufgeloest_voll:
            for pattern in PROTECTED_WRITE_PATH_PATTERNS:
                if pattern.search(s):
                    block(hinweis(
                        f"Schreiben in das Kernverzeichnis {CORE_REL}/.",
                        "Der Kern gehoert dem Framework Owner und wird nur ueber ein "
                        "Release ausgetauscht; eine lokale Aenderung macht die "
                        "Installation ungleich ihrem Release.",
                        "Den Befund als Rueckmeldung an den Framework Owner geben "
                        f"({CORE_REL}/governance/FEEDBACK_PROCESS.md); projekteigene "
                        "Regeln gehoeren ins Overlay (Modus M6).",
                        f"Die Operation laeuft nicht; 'install.py --check' bleibt gruen."))

    # Die Modusbindung (K-179, D-501) - nach allen Sperren oben, damit deren Grund zuerst
    # steht. Ein Ziel ausserhalb der Projektwurzel liegt nie in der Plan-Ablage.
    if schreibend:
        bindung = modus_lesen()
        if bindung:
            modus = bindung["modus"]
            ablage = bindung.get("ablage")
            fremd = []
            if modus == "M1" or verb == "unbekannt":
                fremd = list(ziele) or ["(Ziel unbekannt)"]
            else:
                for roh in ziele:
                    try:
                        alle = lesarten(roh, basis)
                    except Unpruefbar:
                        alle = []
                    rels = [os.path.relpath(e, PROJEKTWURZEL).replace("\\", "/")
                            for e in alle if innerhalb(e, PROJEKTWURZEL)]
                    if (not rels or len(rels) < len(alle)
                            or not all(modus_erlaubt(r, bindung) for r in rels)):
                        fremd.append(roh)
            if fremd:
                if modus == "M2":
                    wo, tun = f" ausserhalb der Plan-Ablage {ablage}.",                         f"Den Plan unter {ablage} ablegen. "
                elif modus in MODUS_MIT_PFADEN:
                    wo = (" ausserhalb der gebundenen Pfade "
                          + ", ".join(bindung["umfang"] or bindung["pfade"]) + ".")
                    tun = "Nur unter den gebundenen Pfaden schreiben. "
                else:
                    wo, tun = ".", ""
                block(hinweis(
                    f"ein Schreibaufruf im gebundenen Modus {modus}" + wo,
                    f"Der Mensch hat {modus} gebunden: M1 schreibt nichts, M2 nur den Plan, "
                    "M3 bis M5 nur in ihre Pfade aus dem Overlay "
                    f"({CORE_REL}/framework/core/05-working-model.md, Abschnitt 2).",
                    tun + "Fuer einen anderen Modus bittet der Agent die Person, im eigenen "
                    f"Terminal auszufuehren: python {CORE_REL}/mandat.py modus aus",
                    f"Die Operation laeuft nicht; die Bindung endet von selbst um "
                    f"{bindung['bis']} UTC."))
    durchlassen()


if __name__ == "__main__":
    main()
