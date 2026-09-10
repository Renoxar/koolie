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

_core_rules_integrity.deny_must_contain wird aus denselben Quellregeln erzeugt
(Kennzeichnung "core": true). Der Validator vergleicht die installierte Datei damit -
eine geloeschte Kernregel faellt dadurch auf, auch wenn das Projekt zugleich die
Integritaetsliste gekuerzt hat.
"""
from __future__ import annotations

import json
import os


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
    argument = _befehl(regel, man, korb) if verb == "exec" else _muster(regel["pattern"], man)
    return [name if name in ohne_muster else f"{name}({argument})" for name in ziele]


def _korb_rendern(quelle: dict, man: dict, korb: str) -> list[str]:
    raus: list[str] = []
    for regel in quelle.get(korb, []):
        for gerendert in _regel_rendern(regel, man, korb):
            if gerendert not in raus:
                raus.append(gerendert)
    return raus


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


def _kommentar(man: dict, mit_hooks: bool) -> str:
    kern = core_dir_name(man)
    pack = man.get("client", "?")
    teile = [
        f"Berechtigungsvorlage des Frameworks (Ebene 3 + Overlay-Erweiterungen), erzeugt "
        f"fuer das Client Pack {pack}.",
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
    namen: list[str] = []
    for verb in verben:
        if verb not in abbildung:
            raise AbbildungsFehler(
                f"{man.get('client', '?')}/manifest.json: hook_tools kennt das "
                f"Werkzeugverb '{verb}' nicht")
        if not abbildung[verb]:
            raise AbbildungsFehler(
                f"{man.get('client', '?')}: kein Hook-Werkzeug fuer '{verb}' - der Hook "
                f"wuerde fuer diese Werkzeugklasse nicht ausloesen")
        for name in abbildung[verb]:
            if name not in namen:
                namen.append(name)
    return man.get("hook_matcher_separator", "|").join(namen)


def _hook_befehl(script: str, man: dict) -> str:
    variable = man.get("hook_project_dir_var")
    if not variable:
        raise AbbildungsFehler(
            f"{man.get('client', '?')}/manifest.json: Feld hook_project_dir_var fehlt")
    return 'python3 "$' + variable + '/' + core_dir_name(man) + '/' + script + '"'


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
            neu["hooks"] = [
                {"type": h["type"],
                 "command": _hook_befehl(h["script"], man),
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
