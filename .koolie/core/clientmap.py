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


# ---------------------------------------------------------------------------
# DIE LAGE DES KERNS UNTER DER PROJEKTWURZEL - ZWEI SEGMENTE SEIT 0.88.0
# ---------------------------------------------------------------------------
# Bis 0.87.0 hiess der Kern `leitwerk-core` und war EIN Verzeichnissegment. Vier
# Werkzeuge haben <CORE_DIR> deshalb mit os.path.basename() aus dem eigenen Ort
# gebunden - und genau dort steht in install.py der Satz, das stehe dort, "damit
# eine spaetere Umbenennung nur eine Stelle beruehrt".
#
# Mit `.koolie/core` liefert os.path.basename() den Wert "core". Jede gerendete
# Regeldatei truege dann einen Pfad, den es nicht gibt - und der Validator saehe
# es nicht, weil er denselben falschen Wert bindet (D-299).
#
# Deshalb steht die Lage hier als ZEICHENKETTE und wird nicht abgeleitet. Wer den
# Kern woanders hinlegt, bricht ohnehin die Hook-Kommandos und die Pruefungen 45,
# 59 und 75; ein Wert, der sich still anpasst, verdeckt das nur.
CORE_REL = ".koolie/core"
#: Wieviele Verzeichnisebenen zwischen Kern und Projektwurzel liegen.
CORE_TIEFE = CORE_REL.count("/") + 1


def projektwurzel(kern: str) -> str:
    """Die Projektwurzel aus dem Pfad des Kerns - ueber CORE_TIEFE, nicht ueber
    eine im Quelltext gezaehlte Zahl von dirname-Aufrufen."""
    pfad = os.path.abspath(kern)
    for _ in range(CORE_TIEFE):
        pfad = os.path.dirname(pfad)
    return pfad


def core_dir_name(man: dict) -> str:
    return man.get("runtime_placeholders", {}).get("<CORE_DIR>", CORE_REL)


# ---------------------------------------------------------------------------
# DER LIEFERUMFANG EINER INSTALLATION (D-367, CR-2026-141)
# ---------------------------------------------------------------------------
# Ein Projekt waehlt beim Installieren den ganzen Kern ("voll") oder nur das zur
# Nutzung Noetige ("nutzung"). Die Liste des Noetigen wird NICHT aufgezaehlt - sie
# fehlte nach dem ersten neuen Traeger (D-366). Aufgezaehlt ist das Gegenteil, und es
# ist nach seinem ABLAGEORT geschlossen: die Nachweisschicht aus Aenderungsantraegen,
# Abnahmeprotokollen, Erhebungen und dem Bau des Hauptdokuments. Ein neuer Traeger zur
# Nutzung ist damit von selbst dabei, ein neuer Nachweis von selbst draussen.
#
# ZWEI ABLEITUNGEN SIND GEMESSEN GESCHEITERT (2026-09-25, sechs frische
# Installationen): Die Lesespur taugt nicht - der Validator liest im Projekt alle 549
# Kerndateien. Die transitive Verweishuelle taugt nicht - mit Verzeichnisverweisen
# umfasst sie alles, ohne sie behaelt sie 39 Protokolle und verliert die Skillquellen,
# die --update braucht. OB die Nutzung ohne die Nachweisschicht auskommt, entscheidet
# deshalb der Validator an einer reduzierten Installation (Sonde L367).
#
# Die Wahl steht im Projekt in LIEFERUMFANG neben VERSION; install.py schreibt sie bei
# jedem --target. Fehlt die Datei, gilt "voll" - so liegt jede Installation vor 1.8.0.
LIEFERUMFANG_DATEI = "LIEFERUMFANG"
LIEFERUMFAENGE = ("voll", "nutzung")
NACHWEIS_ABLAGEN = (
    "governance/change-requests",
    "tests/protocols",
    "tests/erhebungen",
    "build",
)


def ist_nachweis(rel: str) -> bool:
    """Liegt der Pfad (relativ zum Kern, mit Schraegstrichen) in der Nachweisschicht?"""
    return any(rel == a or rel.startswith(a + "/") for a in NACHWEIS_ABLAGEN)


def lieferumfang(kern: str) -> str:
    """Der Lieferumfang, den der Kern unter diesem Pfad fuehrt - roh gelesen.

    Ohne Datei "voll". Einen unbekannten Wert gibt die Funktion unveraendert zurueck;
    ihn zu melden ist Sache des Aufrufers (Pruefung 90, install.py).
    """
    try:
        with open(os.path.join(kern, LIEFERUMFANG_DATEI), encoding="utf-8") as fh:
            return fh.read().strip()
    except OSError:
        return "voll"

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
    teile.append(
        "Ein Befehlsschlitz traegt den Befehl, den Abschnitt 5 oder 6 des Overlays fuer "
        "seinen Platzhalter erklaert - ein anderer Befehl an dieser Stelle ist ein "
        "Fehler, auch wenn die Zahl der Zeilen stimmt. Bis 0.43.0 stand der Satz "
        "darueber hier ohne diese Bedingung und versprach zu viel: Ein offener Schlitz "
        "deckte eine hinzugefuegte Zeile (CR-2026-066, D-90). Ungeprueft bleiben die "
        "Pfadlisten - ihr Inhalt wird mit keinem Overlaytext verglichen.")
    if import_control(man) is not None:
        teile.append(
            "Die Importsteuerung schaltet Regel- und Skillquellen fremder "
            "Werkzeugformate ab (D-37). Das eigene Format der Wurzel-Anweisungsdatei "
            "bleibt eingeschaltet. Sie ist ein Standard, keine Schranke: Die "
            "Benutzerkonfiguration dieser Arbeitsstation hat Vorrang.")
    hinweis = man.get("permissions_note")
    if hinweis:
        teile.append(hinweis)
    teile.append("Exakte Mustersemantik: siehe Zeile B3 der Faehigkeitsmatrix "
                 "dieses Client Packs.")
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
    # Zusatzschluessel auf der OBERSTEN Ebene der Einstellungsdatei - nicht innerhalb
    # von permissions. Der Unterschied ist keine Kosmetik: Ein Schluessel auf der
    # falschen Ebene wird von diesem Client stillschweigend nicht gelesen, und nichts
    # meldet es. permissions_extra deckt die eine Ebene, settings_extra die andere
    # (CR-2026-087, D-155). Pruefung 54 haelt beide gegen die erzeugte Datei.
    for schluessel, wert in man.get("settings_extra", {}).items():
        ergebnis[schluessel] = wert
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
_SONDE = "KOOLIE-INTERPRETER-OK"
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
    ausdruck = man.get("hook_project_dir_expr")
    if not variable and not ausdruck:
        raise AbbildungsFehler(
            f"{man.get('client', '?')}/manifest.json: Feld hook_project_dir_var fehlt")
    # WARUM ES DANEBEN EINEN AUSDRUCK GIBT (CR-2026-133, D-347). Eine Variable ist
    # nur eine der Formen, in denen ein Client dem Hook sein Projektverzeichnis sagt -
    # und bei openai-codex ist es keine: Am 2026-09-23 ist der Hook-Prozess
    # aufgezeichnet worden, und seine Umgebung fuehrt AUSSER CODEX_HOME nichts; sein
    # ARBEITSVERZEICHNIS ist das Projektverzeichnis. Eine Variable, die es nicht gibt,
    # haette das Kommando auf einen Pfad unterhalb der Wurzel zeigen lassen - der Hook
    # waere gestartet worden und haette nichts gefunden.
    wurzel = ausdruck if ausdruck else "$" + variable
    befehl = (python_interpreter() + ' "' + wurzel + '/'
              + core_dir_name(man) + '/' + script + '"')
    if enforcing and man.get("hook_fail_closed") is True:
        befehl += " --fail-closed"
    if enforcing:
        # DIE SPERRFORM GEHOERT IN DAS KOMMANDO, UND DER GRUND IST GEMESSEN
        # (CR-2026-133, D-347). Ein durchsetzender Hook sagt seinem Client, dass er
        # sperrt - und die Form dieser Aussage ist clientgebunden. Am 2026-09-23 an
        # einer realen Installation von openai-codex gemessen: Die bisherige Form
        # ({"decision": "block"} und Exit 2) meldet der Client als FEHLGESCHLAGENEN
        # Hook und FUEHRT DIE OPERATION AUS - im Gegenlauf kam der Koederinhalt
        # woertlich heraus. Dieselbe Sperre in der Form, die dieser Client liest,
        # blockiert - auch im Modus, der Rueckfragen und Sandkasten abschaltet.
        # ➡️ Ein Hook, der laeuft und dessen Sperrform der Client nicht liest, ist
        #    eine Zusage ohne Mechanismus, und nichts meldet es.
        # Der Standard bleibt die bisherige Form; ein Pack, das eine andere braucht,
        # SAGT sie. Pruefung 86 verlangt von jedem Pack mit durchsetzendem Hook, dass
        # das Skript die genannte Form kennt.
        form = man.get("hook_block_form")
        if form:
            befehl += " --sperrform " + form
    if needs_project_paths:
        regelablage = man.get("runtime_placeholders", {}).get("<RULES_DIR>")
        if not regelablage:
            raise AbbildungsFehler(
                f"{man.get('client', '?')}/manifest.json: <RULES_DIR> fehlt in "
                f"runtime_placeholders; der meldende Hook braucht die Regelablage")
        befehl += ' "' + wurzel + '" "' + regelablage + '"'
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
            # Zusatzfelder, die dieser Client je Hook-Eintrag verlangt. Bei
            # openai-codex ist das "enabled": true - gemessen am 2026-09-23: ohne
            # dieses Feld laeuft der Eintrag nicht, und der Client meldet es nicht.
            # Ein Pack, das kein solches Feld braucht, fuehrt das Manifestfeld nicht.
            neu.update(man.get("hook_handler_extra") or {})
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
    """Eigenstaendige Hook-Datei fuer Clients, die eine kennen.

    Manche Clients erwarten die Ereignisse unter einem Schluessel der obersten Ebene
    statt unmittelbar in der Datei. Welcher das ist, sagt das Pack in
    hooks_file_wrapper - gemessen, nicht geraten: Bei openai-codex meldet der Client
    eine Datei ohne diesen Schluessel mit *unknown field `PreToolUse`* und LAEDT SIE
    NICHT; er startet trotzdem, und ohne die Meldung im Blick haette man einen
    ausgelieferten Schutz-Hook gehabt, der nie laeuft (D-347).
    """
    objekt = _hooks_objekt(quelltext, man)
    schluessel = man.get("hooks_file_wrapper")
    if schluessel:
        objekt = {schluessel: objekt}
    return json.dumps(objekt, indent=2, ensure_ascii=False) + "\n"


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


# ---------------------------------------------------------------------------
# Zweite Ausgabeform: Rechteprofil (TOML) und Befehlsregeln (eigene Regelsprache)
# ---------------------------------------------------------------------------
#
# WARUM ES SIE GIBT, UND DER GRUND IST GEMESSEN (CR-2026-133, D-346). Die erste
# Ausgabeform rendert Koerbe aus Regeln der Gestalt Werkzeug(Muster) in EINE Datei.
# Der Client openai-codex kennt diese Gestalt nicht. Er bindet Pfade an eine
# Zugriffsart (read / write / deny) in einem Rechteprofil seiner Konfigurationsdatei,
# und Befehle an eigene Regeldateien in einer eigenen Sprache. Die Regelmenge des
# Kerns zerfaellt damit in ZWEI Erzeugnisse, und keines davon ist eine Liste von
# Werkzeug(Muster)-Zeilen.
#
# WAS DABEI AUSFAELLT, FAELLT NICHT LAUTLOS AUS. Gemessen am 2026-09-23
# (tests/protocols/2026-09-23-bau-openai-codex.md):
#   * Ein Musterausdruck ist als Schluessel nur mit ABSOLUTEM oder ~/-Vorsatz
#     zulaessig - und dann nur fuer die Zugriffsart deny. Ein projektrelativer
#     Schluessel (":workspace/<pfad>") nimmt KEIN Muster. Musterform und
#     Versionierbarkeit schliessen einander damit aus, und B3 faellt an beiden Enden.
#   * Ein deny-Leserecht verlangt ausserdem den erhoehten Windows-Sandkasten; auf
#     einem unerhoehten Arbeitsplatz LAEUFT DER CLIENT DANN NICHT (fail-closed).
# Diese Ausgabeform rendert den Lesekorb deshalb NICHT und fuehrt seine Regeln in
# nicht_abgebildete_pfadregeln() auf. Pruefung 87 haelt die Zahl gegen das Pack; das
# Pack traegt B3 als [NICHT ABBILDBAR] mit Begruendung, Ersatz und Freigabe nach
# clients/README.md Abschnitt 4. Eine Regel, die den Client am Starten hindert, waere
# keine Schranke, sondern ein Ausfall.


def _toml_zeichenkette(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _toml_wert(wert: object) -> str:
    if wert is True:
        return "true"
    if wert is False:
        return "false"
    if isinstance(wert, int):
        return str(wert)
    return _toml_zeichenkette(str(wert))


def _profil_schluessel(rohmuster: str, man: dict) -> str | None:
    """Projektrelativer Schluessel des Rechteprofils - oder None, wenn nicht abbildbar.

    Abbildbar ist genau, was nach dem Aufloesen der Platzhalter KEIN Muster mehr
    enthaelt: Die Schluesselsyntax dieses Clients nimmt Muster nur mit absolutem oder
    ~/-Vorsatz an, und ein absoluter Pfad in einem versionierten Traeger waere ein Wert
    dieser Arbeitsstation. Ein offener Projektplatzhalter bleibt ebenfalls aus - er
    traegt eine Liste, die der Overlay Owner fuellt, und die Schluesselseite einer
    TOML-Tabelle kennt keinen Schlitz.
    """
    muster = resolve_placeholders(rohmuster, man)
    if muster.startswith("<"):
        return None
    # Ein Teilbaummuster ist die eine Musterform, die dieser Client projektrelativ
    # nimmt - gemessen am 2026-09-23: ":workspace/.koolie/**" wird angenommen und
    # steht danach als Teilbaum ":workspace/.koolie" im wirksamen Profil. Alles
    # andere - ein Namensmuster wie **/*.lock - bleibt aus.
    if muster.endswith("/**"):
        muster = muster[:-3]
    if any(z in muster for z in ("*", "?", "[")):
        return None
    vorsatz = man.get("permission_path_special", ":workspace")
    if muster.startswith("./"):
        muster = muster[2:]
    return vorsatz + "/" + muster


def _profil_eintraege(quelle: dict, man: dict) -> tuple[dict, list[str]]:
    """Die Pfadregeln des Kerns als Eintraege des Rechteprofils.

    Rueckgabe: (Eintraege, nicht abgebildete Rohregeln). Die zweite Haelfte ist der
    Grund, warum dieser Ausgabeform eine Zeile im Pack gehoert.
    """
    eintraege: dict[str, str] = {}
    offen: list[str] = []
    for schluessel, wert in (man.get("permission_path_base") or {}).items():
        eintraege[schluessel] = wert
    for regel in quelle.get("deny", []):
        verb = regel.get("tool")
        if verb == "write":
            schluessel = _profil_schluessel(regel["pattern"], man)
            if schluessel is None:
                offen.append("write " + regel["pattern"])
                continue
            # Schreibverbot auf einem Teilbaum heisst hier: lesbar, nicht schreibbar.
            eintraege[schluessel] = "read"
        elif verb == "read":
            offen.append("read " + regel["pattern"])
    return eintraege, offen


def nicht_abgebildete_pfadregeln(quelltext: str, man: dict) -> list[str]:
    """Die Pfadregeln, die diese Ausgabeform nicht traegt - oeffentlich fuer Pruefung 87."""
    return _profil_eintraege(json.loads(quelltext), man)[1]


def _toml_kommentar(man: dict) -> list[str]:
    kern = core_dir_name(man)
    pack = man.get("client", "?")
    return [
        "Berechtigungsvorlage des Frameworks (Ebene 3), erzeugt fuer das Client Pack "
        + pack + ".",
        "Regelmenge: " + kern + "/framework/runtime/permissions.json. Abbildung auf die",
        "Form dieses Clients: " + kern + "/clients/" + pack + "/manifest.json.",
        "Inhaltliche Aenderungen gehoeren dorthin und laufen als Aenderungsantrag.",
        "Diese Datei traegt die PFADSEITE. Die Befehlsseite steht in der Regeldatei, die",
        "dasselbe Werkzeug erzeugt; beide zusammen sind die Berechtigungsschicht dieses",
        "Packs.",
        "Was diese Datei NICHT traegt, steht in Zeile B3 der Faehigkeitsmatrix des Packs:",
        "Der Lesekorb des Kerns ist hier nicht abbildbar - ein Muster verlangt einen",
        "absoluten Vorsatz und waere damit ein Wert dieser Arbeitsstation, und ein",
        "deny-Leserecht verlangt den erhoehten Windows-Sandkasten.",
        "Die projektlokale Schicht laedt NUR, wenn dieses Projekt in der Benutzer-",
        "konfiguration des Clients als vertraut eingetragen ist. Ohne diesen Eintrag",
        "traegt diese Datei nichts.",
        "Diese Datei traegt ausschliesslich Schluessel, die der Client kennt: Ein",
        "unbekannter Schluessel wird gemeldet und mit --strict-config zum Fehler. Die",
        "Kernregeln haelt deshalb der Validator gegen die Kernquelle und nicht eine",
        "zweite Liste in dieser Datei.",
    ]


def render_permissions_toml(quelltext: str, man: dict) -> str:
    """Rechteprofil dieses Client Packs aus der neutralen Regelmenge."""
    quelle = json.loads(quelltext)
    profil = man.get("permission_profile_name")
    if not profil:
        raise AbbildungsFehler(
            man.get("client", "?") + "/manifest.json: Feld permission_profile_name "
            "fehlt - ohne Profilnamen gibt es keine Tabelle, in die die Pfadregeln "
            "gehoeren")
    eintraege, _ = _profil_eintraege(quelle, man)

    zeilen = ["# " + teil for teil in _toml_kommentar(man)]
    zeilen.append("")
    zeilen.append("default_permissions = " + _toml_zeichenkette(profil))
    zeilen.append("")
    zeilen.append("[permissions." + profil + "]")
    beschreibung = man.get("permission_profile_description")
    if beschreibung:
        zeilen.append("description = " + _toml_zeichenkette(beschreibung))
    zeilen.append("")
    zeilen.append("[permissions." + profil + ".filesystem]")
    for schluessel in sorted(eintraege):
        zeilen.append(_toml_zeichenkette(schluessel) + " = "
                      + _toml_zeichenkette(eintraege[schluessel]))
    netz = man.get("permission_profile_network")
    if netz:
        zeilen.append("")
        zeilen.append("[permissions." + profil + ".network]")
        for schluessel in sorted(netz):
            zeilen.append(schluessel + " = " + _toml_wert(netz[schluessel]))
    for tabelle in sorted(man.get("permissions_toml_extra") or {}):
        inhalt = man["permissions_toml_extra"][tabelle]
        zeilen.append("")
        zeilen.append("[" + tabelle + "]")
        for schluessel in sorted(inhalt):
            zeilen.append(schluessel + " = " + _toml_wert(inhalt[schluessel]))
    return "\n".join(zeilen) + "\n"


def _policy_zeile(regel: dict, man: dict, decision: str) -> str | None:
    """Eine Befehlsregel in der Regelsprache dieses Clients - oder None bei Schlitz."""
    woertlich = regel["command"].strip()
    praefix = regel.get("prefix", woertlich).strip()
    if not woertlich.startswith(praefix):
        raise AbbildungsFehler(
            "permissions.json: prefix '" + praefix + "' ist kein Praefix von command '"
            + woertlich + "' - die Praefixform waere nicht nachweislich breiter als "
            "die woertliche")
    if decision == "allow" and praefix != woertlich:
        raise AbbildungsFehler(
            "permissions.json: allow-Regel '" + woertlich + "' hat eine kuerzere "
            "prefix-Form - bei allow waere das eine Lockerung")
    aufgeloest = resolve_placeholders(praefix, man)
    if aufgeloest.startswith("<"):
        # Offener Projektplatzhalter: Sein Wert gehoert dem Projekt, und diese
        # Regelsprache kennt keinen Schlitz. Der Befehl bleibt aus - das ist bei
        # 'prompt' eine Verschaerfung (er laeuft in die Rueckfrage) und bei 'allow'
        # ebenfalls (er ist nicht vorab freigegeben).
        return None
    tokens = ", ".join(_toml_zeichenkette(t) for t in aufgeloest.split())
    grund = regel.get("justification") or ("Framework-Regel (" + decision + ")")
    return ("prefix_rule(pattern = [" + tokens + "], decision = "
            + _toml_zeichenkette(decision) + ", justification = "
            + _toml_zeichenkette(grund) + ")")


#: Korb der Kernquelle -> Entscheidung der Regelsprache dieses Clients.
POLICY_ENTSCHEIDUNG = {"deny": "forbidden", "ask": "prompt", "allow": "allow"}


def _policy_kommentar(man: dict) -> list[str]:
    kern = core_dir_name(man)
    pack = man.get("client", "?")
    return [
        "Befehlsregeln des Frameworks (Ebene 3), erzeugt fuer das Client Pack " + pack + ".",
        "Regelmenge: " + kern + "/framework/runtime/permissions.json, Regeln mit tool=exec.",
        "Reihenfolge der Koerbe: deny vor ask vor allow - forbidden vor prompt vor allow.",
        "Die Praefixform ist nachweislich mindestens so breit wie die woertliche Form;",
        "ihre benannte Grenze ist eine andere Schreibweise desselben Befehls.",
        "Ein Befehlsschlitz des Overlays steht NICHT hier: Sein Wert gehoert dem Projekt,",
        "und diese Regelsprache kennt keinen Platzhalter. Sein Ausbleiben ist in beiden",
        "Koerben eine Verschaerfung.",
    ]


def render_exec_policy(quelltext: str, man: dict) -> str:
    """Befehlsregeln dieses Client Packs aus der neutralen Regelmenge.

    Die Regeldatei liegt projektlokal und ist damit versioniert - das ist die Haelfte
    von B1, die dieser Client traegt. Gemessen am 2026-09-23 an einer realen
    Installation: Ein Befehl, den diese Datei verbietet, wird abgewiesen, und der
    Client nennt dabei die Begruendung dieser Datei woertlich.
    """
    quelle = json.loads(quelltext)
    zeilen = ["# " + teil for teil in _policy_kommentar(man)]
    zeilen.append("")
    for korb in ("deny", "ask", "allow"):
        entscheidung = POLICY_ENTSCHEIDUNG[korb]
        raus: list[str] = []
        for regel in quelle.get(korb, []):
            if regel.get("tool") != "exec":
                continue
            gerendert = _policy_zeile(regel, man, entscheidung)
            if gerendert and gerendert not in raus:
                raus.append(gerendert)
        if not raus:
            continue
        zeilen.append("# --- " + korb + " -> " + entscheidung + " ---")
        zeilen.extend(raus)
        zeilen.append("")
    return "\n".join(zeilen).rstrip("\n") + "\n"


def permissions_format(man: dict) -> str:
    """Ausgabeform der Berechtigungsdatei dieses Packs ('json' oder 'toml').

    Der Standard ist 'json': Zwei der drei Packs fuehren ihn, und ein fehlendes Feld
    darf nicht die neue Form bedeuten - ein Pack soll seine Form SAGEN und sie nicht
    durch Schweigen erben.
    """
    return man.get("permissions_format", "json")


def exec_policy_file(man: dict) -> str | None:
    """Zielpfad der Befehlsregeldatei - oder None, wenn das Pack keine fuehrt."""
    return man.get("exec_policy_file")
