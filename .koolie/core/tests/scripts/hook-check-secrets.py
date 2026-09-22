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

Das Skript gibt gefundene Secrets niemals aus; es nennt nur die Musterkategorie. Dasselbe
gilt fuer einen unpruefbaren Pfadwert: Genannt wird die Position, nicht der Wert (D-39).
Alle Muster sind generisch; sie enthalten keine realen Werte.
"""
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
SECRET_PATH_PATTERNS = [
    re.compile(r"(^|[\\/])\.env(\.|$)", re.I),
    re.compile(r"\.(pem|key|p12|pfx|jks|keystore)$", re.I),
    re.compile(r"(^|[\\/])id_(rsa|ed25519|ecdsa)", re.I),
    re.compile(r"(^|[\\/])secrets?[\\/]", re.I),
]

STRUCTURE_PATH_PATTERNS = [
    # Wurzel-Anweisungsdatei und Laufzeitschicht heissen je nach Client anders. Bewusst
    # beide Formen: Das Skript wird von allen Client Packs geteilt, und ein zusaetzlich
    # geschuetzter Pfad ist eine Verschaerfung, keine Lockerung.
    re.compile(r"(^|[\\/])(AGENTS|CLAUDE)\.md$", re.I),
    re.compile(r"(^|[\\/])\.(devin|claude)[\\/]", re.I),
    re.compile(r"(^|[\\/])\.koolie[\\/]project-overlay[\\/]", re.I),
    re.compile(r"(^|[\\/])framework[\\/]core[\\/]", re.I),
]

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

    def fertig():
        return (tuple(sorted(schreiben)), tuple(sorted(ausfuehren)),
                tuple(sorted(lesen)), tuple(sorted(suchen)), frozenset(pfadfelder))

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
    return fertig()


WRITE_TOOLS, EXEC_TOOLS, READ_TOOLS, SEARCH_TOOLS, PATH_FIELDS = _aus_manifesten()

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
    re.compile(r"(^|[\\/])" + _CORE_MUSTER + r"[\\/]", re.I),
]

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
        print(f"[fw-hook] Ungueltiges Zusatzmuster an Position {_nr} ignoriert "
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


def block(reason: str) -> None:
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
        block(f"Framework-Regel: Der Schutz-Hook kann diese Werkzeugeingabe nicht "
              f"pruefen ({grund}). Er blockiert die Operation, statt sie ungeprueft "
              f"durchzulassen (fail-closed). Moegliche Ursache: Das Eingabeschema des "
              f"Clients hat sich geaendert. Fundstelle melden, Schema gegen die aktuelle "
              f"Clientdokumentation pruefen und als Aenderungsantrag aufnehmen "
              f"({CORE_REL}/governance/CHANGE_REQUEST_TEMPLATE.md).")
    print(f"[fw-hook] Eingabe nicht pruefbar ({grund}); Schema gegen aktuelle "
          f"Clientdokumentation pruefen.", file=sys.stderr)
    sys.exit(0)


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
            echt = aufloesen(wert, basis)
        except Unpruefbar as fehler:
            raise Unpruefbar(f"{fehler.args[0]} an Position {nr} der Pfadfelder")
        if innerhalb(echt, PROJEKTWURZEL):
            rel = os.path.relpath(echt, PROJEKTWURZEL)
            voll.append(rel)
        else:
            nur_secret.append(echt)
    return voll, nur_secret


# ------------------------------------------------------------------ Stufe 3: Regeln

def main() -> None:
    try:
        tool_name, tool_input, basis = ereignis_lesen(sys.stdin.read())
    except Unpruefbar as fehler:
        unpruefbar(fehler.args[0])
        return

    verb = verb_von(tool_name)
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
            block(f"Framework-Regel: Werkzeugeingabe enthaelt ein Muster der Kategorie '{label}'. "
                  f"Secrets duerfen nicht verarbeitet werden. Fundstelle melden, Sitzung anhalten "
                  f"({CORE_REL}/framework/core/02-privacy.md, Abschnitt 5).")

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

    kandidaten += pfadwerte(tool_input)

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
    for s in zu_pruefen + aufgeloest_voll:
        for pattern in muster:
            if pattern.search(s):
                block("Framework-Regel: Operation betrifft einen geschuetzten Pfad "
                      "(Secrets, Wurzel-Anweisungsdatei, Laufzeitschicht, .koolie/project-overlay/, framework/core/). "
                      "Aenderungen daran erfolgen nur ueber den Aenderungsprozess "
                      f"({CORE_REL}/governance/CHANGE_REQUEST_TEMPLATE.md).")
    for s in aufgeloest_secret:
        for pattern in SECRET_PATH_PATTERNS:
            if pattern.search(s):
                block("Framework-Regel: Operation betrifft einen Secret-Pfad ausserhalb "
                      "der Projektwurzel. Secrets duerfen nicht verarbeitet werden "
                      f"({CORE_REL}/framework/core/02-privacy.md, Abschnitt 5).")

    # Schreiboperationen zusaetzlich auf das gesamte Kernverzeichnis blockieren. Das
    # Kernverzeichnis gehoert dem Framework Owner und wird ausschliesslich ueber ein
    # Release ausgetauscht - auch die Skripte darin, die genau diese Zusagen durchsetzen.
    #
    # 'unbekannt' steht hier mit, und darin liegt die Berichtigung aus B06: Bis 0.33.0
    # haengte diese Pruefung an 'tool_name in WRITE_TOOLS', waehrend der Kommentar drei
    # Zeilen darueber die unbekannte Operation zur strengeren erklaerte. Sie war die
    # einzige, bei der der Kern ungeschuetzt blieb.
    if schreibend:
        for s in strings + aufgeloest_voll:
            for pattern in PROTECTED_WRITE_PATH_PATTERNS:
                if pattern.search(s):
                    block(f"Framework-Regel: Schreiboperation betrifft das Kernverzeichnis "
                          f"({CORE_REL}/). Es gehoert dem Framework Owner und wird nur "
                          f"ueber ein Release ausgetauscht; Aenderungen laufen als "
                          f"Aenderungsantrag ({CORE_REL}/governance/CHANGE_REQUEST_TEMPLATE.md).")
    sys.exit(0)


if __name__ == "__main__":
    main()
