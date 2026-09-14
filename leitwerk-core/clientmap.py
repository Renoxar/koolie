#!/usr/bin/env python3
"""
clientmap.py - Semantikabbildung der Berechtigungs- und Hook-Konfiguration.

Alle uebrigen Laufzeitartefakte unterscheiden sich zwischen zwei Client Packs nur in
der Form: ein Frontmatter-Feld heisst anders, eine Werkzeugliste ist kommagetrennt
statt eingerueckt. Berechtigungen und Hooks sind der Fall darueber hinaus. Hier
unterscheiden sich die Werkzeugnamen selbst, ein Client trennt Aendern und Anlegen in
zwei Werkzeuge, und Befehlsverbote greifen bei dem einen woertlich, bei dem anderen
ueber ein Praefix. Eine reine Formtransformation wuerde das nicht tragen.

Die Regelmenge ist Framework-Gut (Ebene 3) und liegt deshalb einmal unter
framework/runtime/permissions.json und framework/runtime/hooks.json. Wie sie beim
jeweiligen Client aussieht, steht in clients/<pack>/manifest.json.

Weil an dieser Abbildung die Kernzusagen B1 bis B6 haengen, erzwingt dieses Modul drei
Zusicherungen, statt sie nur zu behaupten:

  1. Eine deny- oder ask-Regel, fuer die ein Client kein Werkzeug kennt, ist ein
     Fehler. Sie stillschweigend wegzulassen waere eine Lockerung. Bei allow ist das
     Weglassen zulaessig - es faellt dann auf den strengeren Standard zurueck.
  2. Die Praefixform eines Befehlsverbots muss ein Praefix seiner woertlichen Form
     sein. Damit ist die Praefixform nachweislich mindestens so breit; die Abweichung
     ist eine Verschaerfung und keine Luecke.
  3. Bei allow ist jede Verbreiterung unzulaessig: dort muessen beide Formen
     uebereinstimmen.
  4. Ein Werkzeugverb des Frontmatters, das ein Pack weder abbildet noch ausdruecklich
     als nicht abgebildet deklariert, ist ein Fehler. Bis 0.39.0 wurde es woertlich
     durchgereicht und fiel in permissions.deny lautlos aus (D-78).

_core_rules_integrity.deny_must_contain wird aus denselben Quellregeln erzeugt
(Kennzeichnung "core": true). Der Validator vergleicht die installierte Datei damit -
eine geloeschte Kernregel faellt dadurch auf, auch wenn das Projekt zugleich die
Integritaetsliste gekuerzt hat.

Seit 0.26.0 traegt die Berechtigungsdatei zusaetzlich die Importsteuerung des Clients
(D-37): Das Framework importiert keine Regel- und Skillquellen fremder Werkzeugformate.
Das Manifest fuehrt sie unter "import_control" als Schluessel und Wert; kennt ein Client
keinen solchen Mechanismus, fehlt das Feld und es bleibt bei der Auskunft im Client Pack.
Die Masznahme ist ein Standard, keine Schranke - die Benutzerkonfiguration hat Vorrang
(K-27 gemessen 2026-09-11). Pruefung 22 haelt die Abbildung fest, nicht ihre Wirkung.
"""
from __future__ import annotations

import json
import os
import subprocess


class AbbildungsFehler(ValueError):
    """Die Quellregeln lassen sich nicht verlustfrei auf diesen Client abbilden."""


# ---------------------------------------------------------------------------
# Platzhalter
# ---------------------------------------------------------------------------

def resolve_placeholders(text: str, man: dict) -> str:
    """Loest die Laufzeit-Platzhalter des Kerns in die Pfade dieses Client Packs auf.

    Projektplatzhalter (<EXCLUDED_PATHS>, <TEST_COMMAND>, ...) bleiben unberuehrt - die
    fuellt der Overlay Owner. Hier werden nur die Platzhalter aufgeloest, deren Wert
    vom Client abhaengt und die deshalb im Manifest stehen.
    """
    for platzhalter, pfad in man.get("runtime_placeholders", {}).items():
        text = text.replace(platzhalter, pfad)
    return text


def core_dir_name(man: dict) -> str:
    return man.get("runtime_placeholders", {}).get("<CORE_DIR>", "leitwerk-core")

# ---------------------------------------------------------------------------
# Werkzeugverben des Frontmatters
# ---------------------------------------------------------------------------

# Das Vokabular, das ein Skill oder ein Agentenprofil des Kerns in seinem Frontmatter
# schreiben darf - in allowed-tools wie in permissions.deny. Es steht hier und nicht in
# install.py, weil drei Stellen es brauchen: die Abbildung beim Installieren, die
# Abbildung von permissions.deny auf die Werkzeugsperre je Skill (D-65) und Pruefung 38.
#
# WARUM ES UEBERHAUPT EINES BRAUCHT. Bis 0.39.0 hatte die Quelle kein deklariertes
# Vokabular, und der unbekannte Fall war an beiden Stellen STILL - gemessen am
# 2026-09-13 (tests/protocols/2026-09-13-gegenpruefung-werkzeugabbildung.md):
#   * allowed-tools: ein Verb ohne Abbildung wurde WOERTLICH durchgereicht. Aus
#     'allowed-tools: banane' wurde in der installierten Fassung der Werkzeugname
#     'banane'; aus einer geleerten Abbildung wurde 'tools: read, grep, glob' im
#     Agentenprofil fw-reviewer - drei Namen, die dieser Client nicht kennt (M16).
#   * permissions.deny: dasselbe Verb fiel lautlos ganz aus. 'deny: glob' erzeugte
#     keine Werkzeugsperre, und der Validator meldete 0 Fehler (M6).
# Die drei uebrigen Werkzeugabbildungen desselben Manifests - hook_tools,
# permission_tools und der Hook-Matcher - brechen im selben Fall ab (M17 bis M19).
# Diese eine war die unbewachte, und sie kommt zweimal vor.
FRONTMATTER_VERBEN = ("read", "grep", "glob", "edit", "exec")

# Die Bruecke zwischen dem Vokabular der Quelle und dem der Durchsetzungsschichten
# (hook_tools, permission_tools, framework/runtime/*.json). Die beiden Vokabulare sind
# getrennt gewachsen und nicht deckungsgleich: Die Quelle trennt das Suchen in 'grep'
# und 'glob', die Durchsetzung fasst beides als 'search'; die Quelle sagt 'edit', die
# Durchsetzung 'write'.
#
# DIE BRUECKE WIRD BEWACHT, NICHT AUFGELOEST (D-78). Die beiden Listen gleichzuziehen
# hiesse, eine der Seiten zu aendern - und die Vorabfreigabe auf die Sperrliste zu heben
# waere eine AUSWEITUNG: Aus 'allowed-tools: Edit, Write' wuerde 'Edit, Write,
# NotebookEdit'. Verlangt wird deshalb allein die RICHTUNG: Die Sperrliste darf fuer
# kein Verbpaar enger sein als die Vorabfreigabe. Heute ist sie es bei keinem
# (gemessen, M4); Pruefung 38 haelt es fest.
VERB_BRUECKE = {"read": "read", "grep": "search", "glob": "search",
                "edit": "write", "exec": "exec"}


def frontmatter_werkzeuge(man: dict, block: str, verb: str) -> list[str]:
    """Die Werkzeugnamen dieses Clients fuer ein Verb aus dem Frontmatter der Quelle.

    `block` ist "skill_frontmatter" oder "agent_frontmatter" - die beiden Stellen, an
    denen dasselbe Vokabular abgebildet wird.

    Drei Ausgaenge, und keiner davon ist still:

      * in tool_names abgebildet -> die Werkzeugnamen dieses Clients;
      * in tool_names_unmapped deklariert -> das Verb unveraendert. Ein Client, dessen
        Frontmatter die Verben selbst als Werkzeugnamen fuehrt - oder fuer den das
        unerhoben ist -, sagt das ausdruecklich. Bauform wie hook_tools_absent nach
        D-47: Eine Abwesenheit wird erklaert, nie aus einer Luecke erraten;
      * weder noch -> AbbildungsFehler.

    Der dritte Ausgang ist die Aenderung gegenueber 0.39.0. Dort reichte derselbe Fall
    das Verb woertlich durch, und niemand erfuhr davon.
    """
    if verb not in FRONTMATTER_VERBEN:
        raise AbbildungsFehler(
            f"{man.get('client', '?')}: Das Werkzeugverb '{verb}' gehoert nicht zum "
            f"Vokabular des Frontmatters {list(FRONTMATTER_VERBEN)}. Ein Skill oder "
            f"Agentenprofil des Kerns nennt nur diese Verben - alles andere ist ein "
            f"Schreibfehler oder ein Verb der Durchsetzungsschicht, das hier nicht "
            f"hingehoert (D-78)")
    fmt = man.get(block) or {}
    abbildung = fmt.get("tool_names") or {}
    if verb in abbildung:
        return list(abbildung[verb])
    if verb in (fmt.get("tool_names_unmapped") or []):
        return [verb]
    raise AbbildungsFehler(
        f"{man.get('client', '?')}/manifest.json: {block}.tool_names kennt das "
        f"Werkzeugverb '{verb}' nicht. Fuehrt dieser Client die Werkzeugnamen des "
        f"Frontmatters unveraendert - oder sind sie unerhoben -, gehoert das Verb in "
        f"{block}.tool_names_unmapped samt _tool_names_unmapped_note; eine Luecke "
        f"allein ist keine Aussage (D-78, Bauform wie hook_tools_absent nach D-47)")


# ---------------------------------------------------------------------------
# Berechtigungen
# ---------------------------------------------------------------------------

def _werkzeuge(man: dict, verb: str) -> list[str]:
    abbildung = man.get("permission_tools")
    if abbildung is None:
        raise AbbildungsFehler(
            f"{man.get('client', '?')}/manifest.json: Feld permission_tools fehlt")
    if verb not in abbildung:
        raise AbbildungsFehler(
            f"{man.get('client', '?')}/manifest.json: permission_tools kennt das "
            f"Werkzeugverb '{verb}' nicht")
    return list(abbildung[verb])


def _muster(rohmuster: str, man: dict) -> str:
    """Pfadmuster in der Schreibweise dieses Clients.

    Manche Clients verlangen fuer einen Namen ohne Verzeichnisanteil eine ausdrueckliche
    Wurzelangabe, weil ein blosser Name sonst mehrdeutig ist. Aufgeloeste Muster mit
    Verzeichnisanteil, Globs und offene Projektplatzhalter bleiben unberuehrt.
    """
    muster = resolve_placeholders(rohmuster, man)
    vorsatz = man.get("permission_path_prefix", "")
    if not vorsatz or "/" in muster or muster.startswith(("<", "*")):
        return muster
    return vorsatz + muster


def _befehl(regel: dict, man: dict, korb: str) -> str:
    """Befehlsverbot in der Schreibweise dieses Clients (woertlich oder praefixbasiert)."""
    woertlich = regel["command"]
    praefix = regel.get("prefix", woertlich.strip())
    if not woertlich.strip().startswith(praefix):
        raise AbbildungsFehler(
            f"permissions.json: prefix '{praefix}' ist kein Praefix von command "
            f"'{woertlich.strip()}' - die Praefixform waere nicht nachweislich breiter "
            f"als die woertliche")
    if man.get("permission_exec_match", "literal") != "prefix":
        return resolve_placeholders(woertlich, man)
    if korb == "allow" and praefix != woertlich.strip():
        raise AbbildungsFehler(
            f"permissions.json: allow-Regel '{woertlich.strip()}' hat eine kuerzere "
            f"prefix-Form - bei allow waere das eine Lockerung")
    praefix = resolve_placeholders(praefix, man)
    if praefix.startswith("<"):
        # Offener Projektplatzhalter: Der Overlay Owner traegt den vollstaendigen Befehl
        # ein; ein angehaengtes Praefixzeichen wuerde ihn verfaelschen.
        return praefix
    return praefix + man.get("permission_exec_suffix", ":*")


def _regel_rendern(regel: dict, man: dict, korb: str) -> list[str]:
    verb = regel["tool"]
    ziele = _werkzeuge(man, verb)
    if not ziele:
        if korb in ("deny", "ask"):
            raise AbbildungsFehler(
                f"{man.get('client', '?')}: kein Werkzeug fuer '{verb}', die "
                f"{korb}-Regel {regel} liesse sich nur durch Weglassen abbilden - das "
                f"waere eine Lockerung")
        return []
    ohne_muster = set(man.get("permission_tools_bare", []))
    if verb == "exec":
        argument = _befehl(regel, man, korb)
    elif verb == "skill":
        # Ein Aufrufname, kein Pfad: weder Wurzelpraefix noch Praefixzeichen, und
        # keine Musterausweitung. Gemessen am 2026-09-14 (D-82): Das Argument wird
        # woertlich verglichen - Skill(fw-*) laesst den Aufruf von fw-code-explain
        # NICHT durch. Wer hier ein Muster erzeugte, erzeugte eine Freigabe, die
        # lautlos nichts freigibt - der Befundtyp von D-66, mit umgekehrtem
        # Vorzeichen.
        argument = regel["pattern"]
    else:
        argument = _muster(regel["pattern"], man)
    return [name if name in ohne_muster else f"{name}({argument})" for name in ziele]


def _korb_rendern(quelle: dict, man: dict, korb: str) -> list[str]:
    raus: list[str] = []
    for regel in quelle.get(korb, []):
        for gerendert in _regel_rendern(regel, man, korb):
            if gerendert not in raus:
                raus.append(gerendert)
    return raus


def basket_rules(quelle: dict, man: dict, korb: str) -> list[str]:
    """Die Regeln eines Korbes in der Schreibweise dieses Clients.

    Dieselbe Bauart wie core_rules, nur ohne die Einschraenkung auf 'core': true. Der
    Validator haelt die installierte Datei damit gegen die Kernquelle (Pruefung 37,
    CR-2026-061, D-77): Was hier erzeugt wird, muss dort stehen; was dort zusaetzlich
    steht, ist nur im deny-Korb zulaessig - dort ist es eine Verschaerfung, in ask und
    allow eine Ausweitung.

    Oeffentlich und nicht _korb_rendern, weil eine Pruefung, die auf eine private
    Funktion greift, beim naechsten Umbau still ausfaellt.
    """
    return _korb_rendern(quelle, man, korb)


def core_rules(quelle: dict, man: dict) -> list[str]:
    """Die Kernzusagen B1 bis B6 in der Schreibweise dieses Clients."""
    raus: list[str] = []
    for regel in quelle.get("deny", []):
        if not regel.get("core"):
            continue
        for gerendert in _regel_rendern(regel, man, "deny"):
            if gerendert not in raus:
                raus.append(gerendert)
    return raus


def import_control(man: dict) -> tuple[str, object] | None:
    """Importsteuerung dieses Clients als (Schluessel, Wert) - oder None.

    Ein Client ohne solchen Mechanismus traegt das Feld nicht; dann bleibt es bei der
    Auskunft im Abschnitt "Anweisungs- und Konfigurationsquellen ausserhalb des
    Projekts" seines Client Packs (D-37). Dasselbe Feld liest Pruefung 22.
    """
    steuerung = man.get("import_control")
    if not steuerung:
        return None
    schluessel = steuerung.get("key")
    if not schluessel or "value" not in steuerung:
        raise AbbildungsFehler(
            f"{man.get('client', '?')}/manifest.json: import_control braucht 'key' "
            f"und 'value'")
    return schluessel, steuerung["value"]


def _kommentar(man: dict, mit_hooks: bool) -> str:
    kern = core_dir_name(man)
    pack = man.get("client", "?")
    teile = [
        f"Berechtigungsvorlage des Frameworks (Ebene 3), erzeugt fuer das Client "
        f"Pack {pack}.",
        f"Regelmenge: {kern}/framework/runtime/permissions.json. Abbildung auf die "
        f"Werkzeuge dieses Clients: {kern}/clients/{pack}/manifest.json. Inhaltliche "
        f"Aenderungen gehoeren dorthin und laufen als Aenderungsantrag.",
        "Mechanismus: deny vor ask vor allow.",
    ]
    if mit_hooks:
        teile.append("Dieser Client kennt keine eigene Hook-Datei; die Hooks stehen "
                     "deshalb hier unter 'hooks'.")
    teile.append(
        "Platzhalter in spitzen Klammern traegt der Overlay Owner hier ein - das ist der "
        "einzige Teil dieser Datei, der dem Projekt gehoert.")
    teile.append(
        "Die unter _core_rules_integrity aufgefuehrten Regeln duerfen vom Projekt nicht "
        f"entfernt werden; {kern}/tests/scripts/validate-framework.py prueft sie gegen "
        "die Kernquelle.")
    teile.append(
        "Derselbe Lauf haelt alle drei Koerbe gegen die Kernquelle: Was dort erzeugt "
        "wird, muss hier stehen. Eine zusaetzliche Regel ist nur unter 'deny' zulaessig "
        "- dort ist sie eine Verschaerfung; unter 'ask' und 'allow' waere sie eine "
        "Ausweitung und ist ein Fehler. Ein zusaetzlicher freigegebener Befehl gehoert "
        "deshalb nicht hierher, sondern in Abschnitt 6 des Overlays und damit in die "
        "Regelschicht.")
    if import_control(man) is not None:
        teile.append(
            "Die Importsteuerung schaltet Regel- und Skillquellen fremder "
            "Werkzeugformate ab (D-37). Das eigene Format der Wurzel-Anweisungsdatei "
            "bleibt eingeschaltet. Sie ist ein Standard, keine Schranke: Die "
            "Benutzerkonfiguration dieser Arbeitsstation hat Vorrang.")
    hinweis = man.get("permissions_note")
    if hinweis:
        teile.append(hinweis)
    teile.append("Exakte Mustersemantik: <VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>.")
    return " ".join(teile)


def render_permissions(quelltext: str, man: dict, hooks_quelltext: str | None = None) -> str:
    """Berechtigungsdatei dieses Client Packs aus der neutralen Regelmenge.

    hooks_quelltext wird nur uebergeben, wenn der Client keine eigene Hook-Datei kennt;
    die Hooks werden dann in dieselbe Datei eingebettet.
    """
    quelle = json.loads(quelltext)
    rechte: dict = {}
    rechte.update(man.get("permissions_extra", {}))
    for korb in ("deny", "ask", "allow"):
        rechte[korb] = _korb_rendern(quelle, man, korb)

    ergebnis: dict = {"_comment": _kommentar(man, hooks_quelltext is not None),
                      "permissions": rechte}
    steuerung = import_control(man)
    if steuerung is not None:
        ergebnis[steuerung[0]] = steuerung[1]
    if hooks_quelltext is not None:
        ergebnis["hooks"] = _hooks_objekt(hooks_quelltext, man)
    ergebnis["_core_rules_integrity"] = {"deny_must_contain": core_rules(quelle, man)}
    return json.dumps(ergebnis, indent=2, ensure_ascii=False) + "\n"


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------

def _hook_matcher(verben: list[str], man: dict) -> str:
    abbildung = man.get("hook_tools")
    if abbildung is None:
        raise AbbildungsFehler(
            f"{man.get('client', '?')}/manifest.json: Feld hook_tools fehlt")
    # Ein Pack darf eine Werkzeugklasse nicht dadurch aus der Durchsetzung nehmen, dass
    # es sie leer laesst - deshalb ist eine leere Liste ein Fehler. Fuehrt der Client
    # aber tatsaechlich kein Werkzeug dieser Art, muss es einen Weg geben, das zu sagen:
    # hook_tools_absent erklaert die Abwesenheit ausdruecklich. Der Unterschied ist der
    # zwischen "nicht abgebildet" und "gibt es nicht", und er muss deklariert werden,
    # nicht aus einer leeren Liste erraten (CR-2026-047 E3, D-47). Pruefung 26 prueft,
    # dass eine so erklaerte Abwesenheit auch in permission_tools steht.
    erklaert_abwesend = set(man.get("hook_tools_absent") or [])
    namen: list[str] = []
    for verb in verben:
        if verb not in abbildung:
            raise AbbildungsFehler(
                f"{man.get('client', '?')}/manifest.json: hook_tools kennt das "
                f"Werkzeugverb '{verb}' nicht")
        if not abbildung[verb]:
            if verb in erklaert_abwesend:
                continue
            raise AbbildungsFehler(
                f"{man.get('client', '?')}: kein Hook-Werkzeug fuer '{verb}' - der Hook "
                f"wuerde fuer diese Werkzeugklasse nicht ausloesen. Fuehrt der Client "
                f"kein solches Werkzeug, gehoert das Verb in hook_tools_absent")
        for name in abbildung[verb]:
            if name not in namen:
                namen.append(name)
    return man.get("hook_matcher_separator", "|").join(namen)


# Kandidaten in der Reihenfolge, in der sie geprueft werden. "python3" steht vorn,
# weil es auf POSIX-Systemen der verlaessliche Name ist; "py" ist der Windows-Launcher.
INTERPRETER_KANDIDATEN = ("python3", "python", "py")
_SONDE = "LEITWERK-INTERPRETER-OK"
_interpreter_gemerkt: list[str] = []


def python_interpreter() -> str:
    """Ermittelt einen Interpreternamen, der auf dieser Maschine wirklich Python startet.

    Nicht "python3" fest verdrahten: Unter Windows ist das haeufig der
    Microsoft-Store-Alias, der nur eine Fehlermeldung ausgibt und mit Exit-Code 49
    endet, ohne dass ein Interpreter startet. Ein Hook, der so aufgerufen wird, laeuft
    nie - und ein Schutz-Hook, der nicht laeuft, blockiert nichts (AP2-CC-13).

    Geprueft wird deshalb nicht die Anwesenheit des Namens, sondern seine Wirkung:
    Der Kandidat muss eine Sonde ausgeben. Das ist dieselbe Unterscheidung, die D-23
    fuer Pruefungen verlangt - Anwesenheit ist kein Nachweis.
    """
    if _interpreter_gemerkt:
        return _interpreter_gemerkt[0]
    versucht = []
    for kandidat in INTERPRETER_KANDIDATEN:
        try:
            lauf = subprocess.run(
                [kandidat, "-c", "import sys; sys.stdout.write('%s')" % _SONDE],
                capture_output=True, text=True, timeout=15)
        except (OSError, subprocess.SubprocessError) as fehler:
            versucht.append("%s (%s)" % (kandidat, type(fehler).__name__))
            continue
        if lauf.returncode == 0 and _SONDE in (lauf.stdout or ""):
            _interpreter_gemerkt.append(kandidat)
            return kandidat
        versucht.append("%s (Exit %s)" % (kandidat, lauf.returncode))
    raise AbbildungsFehler(
        "Kein funktionsfaehiger Python-Interpreter fuer die Hook-Aufrufe gefunden. "
        "Geprueft: " + ", ".join(versucht) + ". Die Hooks des Frameworks setzen die "
        "Zusagen H2 und die Overlay-Statusmeldung durch; ohne Interpreter liefen sie "
        "nicht, und ein Schutz-Hook, der nicht laeuft, blockiert nichts (AP2-CC-13). "
        "Installation abgebrochen, statt eine Zusage zu erzeugen, die nicht traegt (D-26)")


def _hook_befehl(script: str, man: dict, enforcing: bool = False,
                 needs_project_paths: bool = False) -> str:
    """Aufrufkommando eines Hooks fuer diesen Client.

    Bei einem durchsetzenden Hook (enforcing in der Kernquelle) haengt die Abbildung
    --fail-closed an, sobald das Pack das Eingabeschema seines Clients als bestaetigt
    fuehrt. Der Schalter steht damit im Kommando, das der Client ohnehin ausfuehrt, und
    nicht in einer Umgebungsvariablen: Ob ein Client env an den Hook-Prozess weiterreicht,
    ist fuer keines der Packs belegt, und eine Sperre, die auf einer unbelegten
    Clientzusage steht, ist genau die Lage, aus der AP2-CC-13 kam (D-31).

    Dieselbe Begruendung traegt needs_project_paths: Ein Hook, der Projektverzeichnis und
    Regelablage braucht, bekommt sie als Argumente aus dieser Abbildung - nicht aus der
    Umgebung und schon gar nicht geraten. Ein Skript des Kerns kennt die Laufzeitschicht
    eines Packs nicht (D-30, fortgeschrieben mit CR-2026-037).
    """
    variable = man.get("hook_project_dir_var")
    if not variable:
        raise AbbildungsFehler(
            f"{man.get('client', '?')}/manifest.json: Feld hook_project_dir_var fehlt")
    befehl = (python_interpreter() + ' "$' + variable + '/'
              + core_dir_name(man) + '/' + script + '"')
    if enforcing and man.get("hook_fail_closed") is True:
        befehl += " --fail-closed"
    if needs_project_paths:
        regelablage = man.get("runtime_placeholders", {}).get("<RULES_DIR>")
        if not regelablage:
            raise AbbildungsFehler(
                f"{man.get('client', '?')}/manifest.json: <RULES_DIR> fehlt in "
                f"runtime_placeholders; der meldende Hook braucht die Regelablage")
        befehl += ' "$' + variable + '" "' + regelablage + '"'
    return befehl


def _hooks_objekt(quelltext: str, man: dict) -> dict:
    quelle = json.loads(quelltext)
    ergebnis: dict = {}
    for ereignis, eintraege in quelle.items():
        if ereignis.startswith("_"):
            continue
        gerendert = []
        for eintrag in eintraege:
            neu: dict = {}
            if "on" in eintrag:
                neu["matcher"] = _hook_matcher(eintrag["on"], man)
            # "enforcing" und "needs_project_paths" sind Steuerinformation der
            # Kernquelle und keine Felder des Clients; sie steuern nur, ob das Kommando
            # --fail-closed traegt und ob ihm Projektverzeichnis und Regelablage folgen.
            neu["hooks"] = [
                {"type": h["type"],
                 "command": _hook_befehl(h["script"], man,
                                         h.get("enforcing") is True,
                                         h.get("needs_project_paths") is True),
                 "timeout": h["timeout"]}
                for h in eintrag["hooks"]
            ]
            gerendert.append(neu)
        ergebnis[ereignis] = gerendert
    return ergebnis


def render_hooks(quelltext: str, man: dict) -> str:
    """Eigenstaendige Hook-Datei fuer Clients, die eine kennen."""
    return json.dumps(_hooks_objekt(quelltext, man), indent=2, ensure_ascii=False) + "\n"


# ---------------------------------------------------------------------------
# Hilfsfunktionen fuer die Aufrufer
# ---------------------------------------------------------------------------

def hooks_in_permissions(man: dict) -> bool:
    """Wahr, wenn dieser Client keine eigene Hook-Datei kennt.

    Erkennbar daran, dass Hook- und Berechtigungsdatei auf denselben Pfad zeigen; eine
    zusaetzliche Angabe im Manifest waere eine zweite Wahrheit ueber dieselbe Tatsache.
    """
    p = man.get("runtime_placeholders", {})
    hooks, rechte = p.get("<HOOKS_FILE>"), p.get("<PERMISSIONS_FILE>")
    return hooks is not None and hooks == rechte


def load_source(core_dir: str, name: str) -> str:
    with open(os.path.join(core_dir, "framework", "runtime", name), encoding="utf-8") as fh:
        return fh.read()
