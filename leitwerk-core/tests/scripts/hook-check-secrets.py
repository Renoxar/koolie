#!/usr/bin/env python3
"""
Framework-Hook: PreToolUse-Prüfung auf Secrets und geschützte Pfade.

Status: entwurf (Belegstatus des Hook-Mechanismus: [DOK]; Eingabeschema des Hooks:
<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>). Das Skript ist bewusst schema-agnostisch:
Es durchsucht alle Zeichenketten der über stdin gelieferten JSON-Struktur.

Verhalten:
- Fund eines Secret-Musters oder eines geschützten Pfads in der Werkzeugeingabe
  -> Ausgabe {"decision": "block", "reason": "..."} und Exit-Code 2 (blockiert laut Dokumentation).
- Schreibende Werkzeuge zusätzlich: jeder Pfad im Kernverzeichnis. Ausführende Werkzeuge
  sind davon ausgenommen, damit die Skripte des Kerns (Validator, install.py --check)
  weiterhin aufrufbar bleiben; dort greift die deny-Regel der Berechtigungsdatei.
- Kein Fund -> Exit-Code 0.
- Nicht parsebare Eingabe -> Exit-Code 0 mit Warnung auf stderr (fail-open), solange das
  Eingabeschema des Clients nicht in einer Zielinstallation bestaetigt ist.
  Mit dem Aufrufargument --fail-closed wird stattdessen blockiert (fail-closed).
  Wo es steht, entscheidet das Client Pack: Das Manifest fuehrt hook_fail_closed, und
  clientmap.py haengt das Argument beim Rendern an das Hook-Kommando. Das Argument steht
  damit in der Konfiguration, die der Client ohnehin ausfuehrt - laeuft der Hook, kommt es
  an. Eine Umgebungsvariable haette die Zusage an eine zweite, unbestaetigte Clientzusage
  gehaengt: dass der Client sie an den Hook-Prozess weiterreicht (D-31).
  FW_HOOK_FAIL_CLOSED=1 wirkt weiterhin und bleibt der Weg fuer eine Installation, die
  fail-closed ohne Neuinstallation erproben will.

Das Skript gibt gefundene Secrets niemals aus; es nennt nur die Musterkategorie.
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
SECRET_PATH_PATTERNS = [
    re.compile(r"(^|[\\/])\.env(\.|$)"),
    re.compile(r"\.(pem|key|p12|pfx|jks|keystore)$", re.I),
    re.compile(r"(^|[\\/])id_(rsa|ed25519|ecdsa)"),
    re.compile(r"(^|[\\/])secrets?[\\/]", re.I),
]

STRUCTURE_PATH_PATTERNS = [
    # Wurzel-Anweisungsdatei und Laufzeitschicht heissen je nach Client anders. Bewusst
    # beide Formen: Das Skript wird von allen Client Packs geteilt, und ein zusaetzlich
    # geschuetzter Pfad ist eine Verschaerfung, keine Lockerung.
    re.compile(r"(^|[\\/])(AGENTS|CLAUDE)\.md$"),
    re.compile(r"(^|[\\/])\.(devin|claude)[\\/]"),
    re.compile(r"(^|[\\/])project-overlay[\\/]"),
    re.compile(r"(^|[\\/])framework[\\/]core[\\/]"),
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
# Betriebssystems und ist unerhoben.
#
# Der Name des Kernverzeichnisses ist keine Eigenschaft eines Clients, sondern dieser
# Installation (<CORE_DIR>, docs/PLACEHOLDER_REGISTRY.md). Dieses Skript liegt unter
# <CORE_DIR>/tests/scripts/ und leitet ihn deshalb aus dem eigenen Ort ab, statt ihn
# festzuschreiben - eine Umbenennung des Kerns erreicht den Hook damit von selbst.
CORE_DIR_NAME = os.path.basename(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

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


def _werkzeugnamen() -> tuple:
    """(write-, exec-, read-, search-Namen) aus den Manifesten aller Packs, klein geschrieben.

    Faellt auf die Basisnamen zurueck, wenn kein Manifest lesbar ist: Ein Hook, der
    wegen einer fehlenden Datei gar nichts mehr blockiert, waere die schlechtere Lage.
    """
    schreiben = set(BASIS_WRITE_TOOLS)
    ausfuehren = set(BASIS_EXEC_TOOLS)
    lesen = set(BASIS_READ_TOOLS)
    suchen = set(BASIS_SEARCH_TOOLS)
    kern = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    packs = os.path.join(kern, "clients")
    try:
        eintraege = sorted(os.listdir(packs))
    except OSError:
        return (tuple(sorted(schreiben)), tuple(sorted(ausfuehren)),
                tuple(sorted(lesen)), tuple(sorted(suchen)))
    for name in eintraege:
        pfad = os.path.join(packs, name, "manifest.json")
        if not os.path.isfile(pfad):
            continue
        try:
            with io.open(pfad, encoding="utf-8") as fh:
                abbildung = (json.load(fh) or {}).get("hook_tools") or {}
        except (OSError, ValueError):
            continue
        for verb, ziel in (("write", schreiben), ("exec", ausfuehren),
                           ("read", lesen), ("search", suchen)):
            for werkzeug in abbildung.get(verb) or []:
                if isinstance(werkzeug, str) and werkzeug.strip():
                    ziel.add(werkzeug.strip().lower())
    return (tuple(sorted(schreiben)), tuple(sorted(ausfuehren)),
            tuple(sorted(lesen)), tuple(sorted(suchen)))


WRITE_TOOLS, EXEC_TOOLS, READ_TOOLS, SEARCH_TOOLS = _werkzeugnamen()

# Ein Shell-Befehl ist keine Pfadangabe: In "cat .env" steht der Pfad mitten im String,
# und die Pfadmuster verlangen einen Zeilenanfang oder ein Trennzeichen davor. Fuer
# ausfuehrende Werkzeuge wird die Eingabe deshalb zusaetzlich in Tokens zerlegt und
# jedes Token wie eine Pfadangabe geprueft (AP2-CC-15).
SHELL_TRENNER = re.compile(r"[\s;|&()<>\"'`,=]+")


def shell_tokens(strings):
    for s in strings:
        for token in SHELL_TRENNER.split(s):
            if token:
                yield token

PROTECTED_WRITE_PATH_PATTERNS = [
    re.compile(r"(^|[\\/])" + re.escape(CORE_DIR_NAME) + r"[\\/]"),
]

# Zusätzliche projektspezifische Muster können über die Umgebungsvariable
# FW_HOOK_EXTRA_PATH_PATTERNS (durch ';' getrennte reguläre Ausdrücke) ergänzt werden.
for _nr, extra in enumerate(
        filter(None, os.environ.get("FW_HOOK_EXTRA_PATH_PATTERNS", "").split(";")), 1):
    try:
        PROTECTED_PATH_PATTERNS.append(re.compile(extra))
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


def fail_closed() -> bool:
    """Wahr, wenn eine nicht lesbare Eingabe blockiert statt durchgelassen wird.

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


def main() -> None:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        msg = "[fw-hook] Eingabe nicht als JSON lesbar; Schema gegen aktuelle Clientdokumentation pruefen."
        if fail_closed():
            block("Framework-Regel: Die Werkzeugeingabe ist nicht als JSON lesbar. Der "
                  "Schutz-Hook kann sie deshalb nicht auf Secrets und geschuetzte Pfade "
                  "pruefen und blockiert die Operation, statt sie ungeprueft durchzulassen "
                  "(fail-closed). Moegliche Ursache: Das Eingabeschema des Clients hat sich "
                  "geaendert. Fundstelle melden, Schema gegen die aktuelle "
                  "Clientdokumentation pruefen und als Aenderungsantrag aufnehmen.")
        print(msg, file=sys.stderr)
        sys.exit(0)

    tool_name = str(payload.get("tool_name", "")).lower() if isinstance(payload, dict) else ""
    strings = list(iter_strings(payload))

    for label, pattern in SECRET_PATTERNS:
        if any(pattern.search(s) for s in strings):
            block(f"Framework-Regel: Werkzeugeingabe enthaelt ein Muster der Kategorie '{label}'. "
                  f"Secrets duerfen nicht verarbeitet werden. Fundstelle melden, Sitzung anhalten "
                  f"(leitwerk-core/framework/core/02-privacy.md, Abschnitt 5).")

    # Schreib-, Ausfuehrungs- und Leseoperationen auf geschuetzte Pfade blockieren.
    # WRITE_TOOLS steht auch hier, damit kein schreibendes Werkzeug an dieser Liste
    # vorbeilaeuft - 'notebookedit' tat das bisher.
    if tool_name in WRITE_TOOLS + EXEC_TOOLS + READ_TOOLS + SEARCH_TOOLS or not tool_name:
        # Bei einem ausfuehrenden Werkzeug steht der Pfad mitten im Befehl; die
        # Pfadmuster verlangen davor einen Zeilenanfang oder ein Trennzeichen. Die
        # Eingabe wird deshalb zusaetzlich tokenisiert (AP2-CC-15).
        zu_pruefen = list(strings)
        # Ohne Werkzeugnamen ist die Art der Operation unbekannt; dann gilt die
        # strengere Liste. Eine unbekannte Operation als lesend zu behandeln, waere
        # die Annahme zugunsten des Zugriffs.
        schreibend = tool_name in WRITE_TOOLS or not tool_name
        if tool_name in EXEC_TOOLS or not tool_name:
            zu_pruefen += list(shell_tokens(strings))
        # Zwei Schutzziele, zwei Listen (D-30): Ein ausfuehrendes, lesendes oder
        # suchendes Werkzeug wird an den Secret-Pfaden gemessen, nicht an den
        # Strukturpfaden - ein Befehl darf den Kern lesen, ein Secret nie. Fuer
        # schreibende Werkzeuge gelten beide Listen. Ohne die Trennung blockierte ein
        # 'git diff' auf einen Kernpfad oder das Lesen einer Regeldatei, also
        # Operationen, die das Framework voraussetzt.
        muster = PROTECTED_PATH_PATTERNS if schreibend else SECRET_PATH_PATTERNS
        for s in zu_pruefen:
            for pattern in muster:
                if pattern.search(s):
                    block("Framework-Regel: Operation betrifft einen geschuetzten Pfad "
                          "(Secrets, Wurzel-Anweisungsdatei, Laufzeitschicht, project-overlay/, framework/core/). "
                          "Aenderungen daran erfolgen nur ueber den Aenderungsprozess "
                          "(leitwerk-core/governance/CHANGE_REQUEST_TEMPLATE.md).")

    # Schreiboperationen zusaetzlich auf das gesamte Kernverzeichnis blockieren. Das
    # Kernverzeichnis gehoert dem Framework Owner und wird ausschliesslich ueber ein
    # Release ausgetauscht - auch die Skripte darin, die genau diese Zusagen durchsetzen.
    if tool_name in WRITE_TOOLS:
        for s in strings:
            for pattern in PROTECTED_WRITE_PATH_PATTERNS:
                if pattern.search(s):
                    block(f"Framework-Regel: Schreiboperation betrifft das Kernverzeichnis "
                          f"({CORE_DIR_NAME}/). Es gehoert dem Framework Owner und wird nur "
                          f"ueber ein Release ausgetauscht; Aenderungen laufen als "
                          f"Aenderungsantrag ({CORE_DIR_NAME}/governance/CHANGE_REQUEST_TEMPLATE.md).")
    sys.exit(0)


if __name__ == "__main__":
    main()
