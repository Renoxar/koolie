"""Die Werkzeuge des Kerns und ihre Lieferung: Bytecode, Erzeugnisse in .gitignore,
Praefixerfassung, Erhebungsablage, Werkzeugnamen, Arbeitsplatzpfade, Kernlage,
Lieferumfang und die Paketquellen.

Pruefungen 45, 68, 69, 70, 71, 76, 90, 107 und 112. Teil des Validators validate-framework.py,
seit 1.19.1 nach Gegenstand in Module geteilt (K-174). Das Register aller Pruefungen
steht im Kopfkommentar des Einstiegs, die Grenze jeder einzelnen in ihrem Kopfkommentar
hier."""
from __future__ import annotations

import ast
import builtins
import json
import os
import re
import symtable
import sys

from .gemeinsam import (
    _clientmap, _verfolgte_dateien, err, hinweis, ist_quellrepositorium,
    iter_text_files, KERN, nicht_geliefert, PAKET_JE_SKRIPT, read, warn, yaml)


# --- 45: Der Bytecode des Kerns gehoert nicht in die Versionierung (D-97) -----------
#
# ANLASS. Abgezaehlt am 2026-09-15 an **beiden** Projekten, die dieses Framework benutzen:
# Der Pilot fuehrte sechs .pyc-Dateien unter .koolie/core/ in der Versionierung, das
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



# --- 45, Gegenstand 3: Die Erzeugnisse der Packs im Quellrepositorium (D-383, K-124) --
#
# Im Quellrepositorium sind Wurzel-Anweisungsdatei, Laufzeitschicht und Overlay
# ERZEUGNISSE von install.py und werden nicht versioniert (README, Abschnitt "Arbeiten an
# diesem Repository"). Bis 1.9.0 schloss die .gitignore nur die Erzeugnisse EINES Packs
# aus; nach `install.py --client` mit einem der anderen beiden waeren deren Dateien
# versionierbar gewesen (K-124).
#
# ABGELEITET, NICHT AUFGEZAEHLT: Was ein Pack in die Wurzel schreibt, steht in seinem
# Manifest (shared_core, shared_seed). Verlangt wird je Ziel der erste Pfadbestandteil
# (unter .koolie/ die ersten zwei - der Kern selbst ist versioniert). Ein neues Pack
# bringt seine Zeilen damit als Befund mit, statt still versionierbar zu sein.
# Nur im Quellrepositorium: In einem Projekt gilt das Gegenteil (D-383).
GITIGNORE_ERZEUGNIS_LISTEN = ("shared_core", "shared_seed")


def _erzeugnis_wurzeln(root: str) -> dict:
    """{Wurzelbestandteil: [Packs]} aller Ziele, die install.py im Quellrepositorium anlegt."""
    kern = os.path.join(root, KERN)
    if kern not in sys.path:
        sys.path.insert(0, kern)
    try:
        import clientmap
    except ImportError:
        warn("clientmap.py nicht gefunden – Gegenstand 3 der Prüfung 45 ist nicht "
             "gelaufen (D-383)")
        return {}
    wurzeln: dict = {}
    clients = os.path.join(root, KERN, "clients")
    for pack in sorted(os.listdir(clients)):
        pfad = os.path.join(clients, pack, "manifest.json")
        if pack.startswith("_") or not os.path.isfile(pfad):
            continue
        man = json.loads(read(pfad))
        for liste in GITIGNORE_ERZEUGNIS_LISTEN:
            for eintrag in man.get(liste, []):
                ziel = clientmap.resolve_placeholders(eintrag["dst"], man).strip("/")
                teile = ziel.split("/")
                if teile[0] == ".koolie":
                    if len(teile) < 2 or teile[1] == "core":
                        continue
                    teile = teile[:2]
                else:
                    teile = teile[:1]
                wurzeln.setdefault("/".join(teile), []).append(pack)
    return wurzeln


def check_gitignore_erzeugnisse(root: str) -> None:
    """Pruefung 45, Gegenstand 3 (D-383): Die .gitignore des Quellrepositoriums schliesst
    die Wurzelerzeugnisse jedes Packs aus."""
    if not ist_quellrepositorium(root):
        return
    pfad = os.path.join(root, ".gitignore")
    if not os.path.isfile(pfad):
        return  # Gegenstand 1 meldet die fehlende Datei
    zeilen = {z.strip().strip("/") for z in read(pfad).splitlines()
              if z.strip() and not z.strip().startswith(("#", "!"))}
    for wurzel, packs in sorted(_erzeugnis_wurzeln(root).items()):
        if wurzel not in zeilen:
            err(f".gitignore: schließt das Erzeugnis `/{wurzel}` nicht aus "
                f"({', '.join(sorted(set(packs)))}). Im Quellrepositorium sind "
                f"Wurzel-Anweisungsdatei, Laufzeitschicht und Overlay Erzeugnisse von "
                f"install.py und werden nicht versioniert (Prüfung 45, D-383)")


def check_lieferumfang(root: str) -> None:
    """Pruefung 90 (D-367): Die Angabe des Lieferumfangs stimmt."""
    cm = _clientmap(root)
    if cm is None:
        return  # ohne clientmap.py meldet Pruefung 1 die fehlende Pflichtdatei
    kern = os.path.join(root, KERN)
    datei = f"{KERN}/{cm.LIEFERUMFANG_DATEI}"
    vorhanden = os.path.isfile(os.path.join(kern, cm.LIEFERUMFANG_DATEI))
    if ist_quellrepositorium(root):
        if vorhanden:
            err(f"{datei}: liegt im Quellrepositorium. Die Datei schreibt install.py in "
                f"ein Projekt; hier behauptete sie eine Installation, und eine Quelle mit "
                f"'nutzung' lieferte keinen vollen Kern mehr (D-367)")
        return
    wert = cm.lieferumfang(kern)
    if wert not in cm.LIEFERUMFAENGE:
        err(f"{datei}: trägt '{wert}' – bekannt sind {', '.join(cm.LIEFERUMFAENGE)}. "
            f"Das nächste Heben hält daran an (D-367)")
        return
    if wert != "nutzung":
        return
    da = [a for a in cm.NACHWEIS_ABLAGEN if os.path.exists(os.path.join(kern, *a.split("/")))]
    if da:
        err(f"{datei}: sagt 'nutzung', aber {', '.join(f'{KERN}/{a}/' for a in da)} "
            f"liegt da. Das nächste Heben mit diesem Umfang löscht es; wer den ganzen "
            f"Kern will, hebt mit --lieferumfang voll (D-367)")
        return
    hinweis(f"Lieferumfang 'nutzung' ({datei}): ohne die Nachweisschicht "
            f"({', '.join(cm.NACHWEIS_ABLAGEN)}). Verweise dorthin sind Herkunftsangaben "
            f"und werden nicht gemeldet; Belege stehen im Release-Archiv (D-367)")


# --- Pruefung 68: Das Praefix, das mehr sperrt als sein Befehl ----------------------
#
# ANLASS, UND ER IST GEMESSEN. permissions.json fuehrt je exec-Regel einen `command`
# (die woertliche Form) und optional einen `prefix` (die Form fuer Clients, die ueber
# ein Praefix sperren). Ist der `prefix` kuerzer, sperrt die Regel MEHR, als ihr
# Befehl nennt. Am 2026-09-20 hat genau das gekostet: Der Eintrag mit dem command
# "git branch -D" traegt den prefix "git branch" und sperrt damit auch das blosse
# Auflisten. Gemessen ueber 50 Laeufe des vierten Testblattbuendels: 25 Abweisungen
# in 23 Laeufen, elf davon auf "git branch" - und zwei Skills schreiben in
# Arbeitsschritt 1 und in ihrer Fehlerbehandlung eine Kandidatenliste vorhandener
# Branches vor, die sie damit nicht liefern koennen (D-219).
#
# WARUM DIE SPERRE TROTZDEM BLEIBT, UND WARUM DAS EINE PRUEFUNG BRAUCHT. Der
# allow-Korb dieser Datei ist praefixbasiert, und clientmap.py verbietet dort ein
# kuerzeres Praefix als der Befehl ("bei allow waere das eine Lockerung"). Er traegt
# deshalb bisher ausschliesslich Verben OHNE schreibende Form - git status, diff,
# log, show, blame. `git branch` waere das erste mit einer. Die Uebererfassung ist
# hier also GEWOLLT; was fehlte, war, dass sie irgendwo steht. Eine Schranke, die
# mehr sperrt als sie sagt, ist die Schwester des wiederkehrenden Befundtyps dieses
# Projekts mit umgekehrtem Vorzeichen - und sie faellt niemandem auf, weil ein
# ueberschiessendes Verbot wie Sorgfalt aussieht.
#
# DER WAECHTER, DER ES NICHT SAH. clientmap.py prueft, ob der prefix ein Praefix des
# command IST - sonst waere die Praefixform "nicht nachweislich breiter als die
# woertliche". Er prueft die Richtung, nicht das Mass. Das ist D-205 an vierter
# Stelle: ein Muster, das seinen Gegenstand enthaelt und mehr.
#
# GRENZE, UND SIE STEHT HIER. Geprueft wird die NENNUNG, nicht ihre Richtigkeit: Eine
# Begruendung, die nicht traegt, laeuft durch - dieselbe Enthaltung, die Pruefung 65
# fuer den Protokollverweis zieht und Pruefung 61 fuer das Pruefmittelwort.
P68_FELD = "_uebererfasst"


def check_praefix_uebererfassung(root: str) -> None:
    """Pruefung 68 (D-219): Ein Praefix, das mehr sperrt als sein Befehl, sagt es."""
    rel = f"{KERN}/framework/runtime/permissions.json"
    pfad = os.path.join(root, KERN, "framework", "runtime", "permissions.json")
    if not os.path.isfile(pfad):
        return  # Pruefung 1 und 39 melden die fehlende Kernquelle bereits
    try:
        quelle = json.loads(read(pfad))
    except ValueError:
        return  # Pruefung 39 meldet die unlesbare Datei bereits
    exec_regeln = 0
    for korb in ("deny", "ask", "allow"):
        eintraege = quelle.get(korb)
        if not isinstance(eintraege, list):
            continue
        for regel in eintraege:
            if not isinstance(regel, dict) or regel.get("tool") != "exec":
                continue
            exec_regeln += 1
            befehl = str(regel.get("command", "")).strip()
            praefix = str(regel.get("prefix", befehl)).strip()
            if not befehl or praefix == befehl:
                continue
            if str(regel.get(P68_FELD, "")).strip():
                continue
            err(f"{rel}: die {korb}-Regel `{befehl}` sperrt über das Präfix "
                f"`{praefix}` mehr, als ihr Befehl nennt – und sagt es nicht. Ein "
                f"Feld `{P68_FELD}` mit der Begründung gehört dazu: Genau diese "
                f"Bauform hat am 2026-09-20 fünfundzwanzig Abweisungen erzeugt und "
                f"zwei Skills eine Zusage unmöglich gemacht, die sie selbst "
                f"vorschreiben. Eine Schranke, die mehr sperrt als sie sagt, ist "
                f"nicht weniger ein Befund als eine, die weniger hält (D-219)")
    if exec_regeln == 0:
        err(f"{rel}: keine einzige exec-Regel gefunden – Prüfung 68 rechnet ihre "
            f"Präfixe gegen ihre Befehle und hat ihren Gegenstand verloren; sie "
            f"bestünde sonst leise (D-23)")


# --- Pruefung 69: Der Messapparat schreibt nicht in das Repositorium ----------------
#
# ANLASS, UND ER IST GEMESSEN - ER KOSTETE NICHTS, WEIL ER VOR DEM LAUF KAM. D-222
# hat die Skripte der Erhebungen mit 0.79.0 ins Repositorium geholt und ihre Belege
# ausdruecklich DRAUSSEN gelassen: "203 Dateien, darunter fuenfzig
# Sitzungstranskripte mit Werkzeugeingaben; sie sind AUFZEICHNUNG, nicht Anweisung".
# Fuenf dieser Skripte legten ihre Belege aber schlicht NEBEN SICH ab:
#
#     BELEGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "belege")
#
# Solange das Skript daneben lag, war das richtig. Seit es im Kern liegt, zeigt
# derselbe Ausdruck HINEIN - und lauf.py legt das Verzeichnis selbst an. Ein
# Nachlauf haette die Mitschriften seiner Laeufe versioniert, ohne dass jemand es
# entschieden haette. Gefunden am 2026-09-20 im Vorbedingungsdurchgang des
# Nachlaufs, vor dem ersten bezahlten Lauf.
#
#   Wer einen Apparat umzieht, zieht seine relativen Pfade mit um - oder er
#   verschiebt ihr Ziel, ohne es zu merken.
#
# WAS GEPRUEFT WIRD, UND WARUM SO. Nicht die Quelltexte (ein Zaehler, der Ausdruecke
# liest, prueft die Schreibweise statt der Sache, D-223), sondern das ERGEBNIS: In
# <CORE_DIR>/tests/erhebungen/ liegen Skripte und eine README - sonst nichts. Eine
# Belegdatei, eine Zustandsaufnahme oder ein Promptverzeichnis dort ist der Befund
# selbst, unabhaengig davon, welcher Ausdruck sie erzeugt hat.
#
# GRENZE, UND SIE STEHT HIER. Die Pruefung sieht nur, was schon geschrieben IST.
# Den Wächter davor traegt `ablage.py`: Er verlangt die Erhebungsablage als Angabe
# und weist einen Pfad im Repositorium ab. Zwei Haelften desselben Gegenstands -
# dieselbe Aufteilung wie bei D-205 zwischen Schnitt und Waechter.
#
# SEIT 1.19.0 EIN VERZEICHNIS, BENANNT (D-473): Der Messapparat ist ein Paket
# (`apparat/`). Zugelassen ist genau dieser Name, und darin nur Python-Quelltext - ein
# Beleg, eine Reihe oder ein Unterverzeichnis dort ist derselbe Befund wie daneben.
P69_ERLAUBT_DATEI = (".py", ".md")
P69_PAKETE = ("apparat",)


def _p69_paket_rest(pfad: str) -> list:
    """Was in einem zugelassenen Paket liegt und kein Python-Quelltext ist."""
    rest = []
    for name in sorted(os.listdir(pfad)):
        voll = os.path.join(pfad, name)
        if name == "__pycache__" and os.path.isdir(voll):
            continue
        if os.path.isdir(voll) or not name.endswith(".py"):
            rest.append(name)
    return rest


def check_erhebungen_sauber(root: str) -> None:
    """Pruefung 69 (D-222): In der Erhebungsablage des Kerns liegen nur Werkzeuge."""
    rel = f"{KERN}/tests/erhebungen"
    ordner = os.path.join(root, KERN, "tests", "erhebungen")
    if not os.path.isdir(ordner):
        return  # ein uebernehmendes Projekt bekommt diese Ablage nicht ausgeliefert
    gesehen = 0
    for name in sorted(os.listdir(ordner)):
        pfad = os.path.join(ordner, name)
        if os.path.isdir(pfad):
            if name == "__pycache__":
                continue
            if name in P69_PAKETE:
                for fremd in _p69_paket_rest(pfad):
                    err(f"{rel}/{name}/{fremd}: im Werkzeugpaket der Erhebungsablage des "
                        f"Kerns liegt nur Python-Quelltext - Belege, Reihen und Prompts sind "
                        f"Aufzeichnung und gehoeren neben das Repositorium (D-222, D-473)")
                continue
            err(f"{rel}/{name}/: ein VERZEICHNIS in der Erhebungsablage des Kerns. "
                f"Hier liegen Werkzeuge; Belege, Prompts und Zustandsaufnahmen sind "
                f"Aufzeichnung und gehoeren neben das Repositorium (D-222). Die "
                f"Ablage wird ueber LW_ERHEBUNG gesagt, nicht abgeleitet")
            continue
        gesehen += 1
        if not name.endswith(P69_ERLAUBT_DATEI):
            err(f"{rel}/{name}: keine Datei der zugelassenen Art "
                f"({', '.join(P69_ERLAUBT_DATEI)}) in der Erhebungsablage des "
                f"Kerns. Eine Belegdatei, ein Ergebnis-JSON oder eine "
                f"Zustandsaufnahme ist hier der Befund selbst - unabhaengig davon, "
                f"welcher Ausdruck sie erzeugt hat (D-222)")
    if gesehen == 0:
        err(f"{rel}: kein einziges Werkzeug gefunden – Prüfung 69 zaehlt den Inhalt "
            f"dieser Ablage und hat ihren Gegenstand verloren; sie bestuende sonst "
            f"leise (D-23)")


# --- Pruefung 70: Jedes Werkzeug des Kerns nennt nur Namen, die es gibt -------------
#
# ANLASS, UND ER IST GEMESSEN - ER KOSTETE NICHTS, WEIL ER VOR DEM LAUF KAM. Der
# Wiederaufnahmepunkt des halb gefahrenen Messtags fuehrte `stand-b4.py` als Befehl 1
# von 4 auf: das Skript, dessen Kopfkommentar sagt "EINE ZAHL IN EINER UEBERGABE IST
# EINE MOMENTAUFNAHME, DIESES SKRIPT IST DER STAND". Es brach beim Import ab:
#
#     PROMPTS = os.path.join(os.path.dirname(S), "prompts")
#
# `S` trug bis D-222 den Ablageort NEBEN dem Skript. Der Umzug in den Kern hat ihn
# entfernt und zwei Lesestellen stehen lassen - eine im Modulrumpf, eine in `main()`.
# Seit 0.79.0 war das Werkzeug damit tot, und der Befund lag genau auf dem Weg der
# Wiederaufnahme. Gefunden am 2026-09-21, vor dem ersten bezahlten Kontrollauf.
#
#   Ein Werkzeug, das niemand faehrt, verfaellt lautlos - und der Tag, an dem es
#   gebraucht wird, ist der Tag, an dem es fehlt.
#
# WARUM KEINE DER 69 ES SAH, UND DAS IST DER EIGENTLICHE BEFUND. Pruefung 45 prueft,
# dass KEIN Bytecode versioniert ist - also die Abwesenheit einer Datei. Pruefung 69
# prueft die ART der Dateien in der Erhebungsablage - .py und .md, sonst nichts. Der
# Apparat hatte damit zwei Waechter ueber seinen Ablageort und keinen einzigen
# darueber, ob seine Werkzeuge laufen.
#
# WAS GEPRUEFT WIRD, UND WARUM SO. Nicht `import` - das fuehrt den Modulrumpf aus,
# und Werkzeuge dieses Kerns brechen dabei mit Absicht ab (`ablage.py` ohne
# LW_ERHEBUNG), waehrend `lauf.py` sein Belegverzeichnis anlegen wuerde: genau das,
# was D-222 verworfen hat. Eine Pruefung, die ihren Gegenstand veraendert, misst ihn
# nicht. Geprueft wird deshalb die SYMBOLTABELLE, die der Interpreter selbst baut:
# Sie kennt jede Bindung und jeden Gueltigkeitsbereich - Modul, Funktion, Klasse,
# Komprehension - und sagt je Name, ob er zugewiesen, importiert, Parameter, frei
# oder global ist. Ein global gelesener Name, den weder der Modulrumpf noch die
# eingebauten Namen binden, ist ein NameError, der auf seinen Lauf wartet.
#
# GRENZE, UND SIE STEHT HIER. Geprueft wird der NAME, nicht der WERT. Wer `S = None`
# schreibt und `os.path.dirname(S)` aufruft, laeuft durch - dieselbe Enthaltung wie
# bei Pruefung 68. Und ein Lauf des Werkzeugs bliebe der staerkere Nachweis; er
# kostet Kontingent und legt Dateien an, diese Pruefung nicht.
P70_EINGEBAUT = frozenset(dir(builtins))


def _p70_offene_namen(quelle: str, name: str) -> list:
    """Die global gelesenen Namen einer Quelle, die nirgends gebunden sind."""
    top = symtable.symtable(quelle, name, "exec")
    modul = {sym.get_name() for sym in top.get_symbols()
             if sym.is_assigned() or sym.is_imported() or sym.is_parameter()}
    offen = []

    def geh(tab) -> None:
        for sym in tab.get_symbols():
            n = sym.get_name()
            if not sym.is_referenced():
                continue
            if sym.is_assigned() or sym.is_imported() or sym.is_parameter():
                continue
            # Die Modulglobalen, die der Interpreter selbst setzt (__file__,
            # __name__, und was eine Python-Fassung sonst hinzufuegt). Ohne diese
            # Ausnahme meldete die Pruefung zwoelf Werkzeuge dieses Kerns, und alle
            # zwoelf laufen - ein Waechter, der bei jedem Lauf meldet, wird
            # abgeschaltet.
            if n.startswith("__") and n.endswith("__"):
                continue
            if n in P70_EINGEBAUT or n in modul:
                continue
            # Nur, was im Modulrumpf steht oder ausdruecklich global gelesen wird.
            # Eine freie Variable aus einer umschliessenden Funktion ist gebunden,
            # nur nicht hier - `is_global()` unterscheidet das.
            if tab is top or sym.is_global():
                offen.append((tab.get_name(), n))
        for kind in tab.get_children():
            geh(kind)

    geh(top)
    return offen


def check_werkzeugnamen(root: str) -> None:
    """Pruefung 70 (D-229): Kein Werkzeug des Kerns liest einen Namen, den es nicht gibt."""
    kern = os.path.join(root, KERN)
    if not os.path.isdir(kern):
        return
    apparat = os.path.join(kern, "tests", "erhebungen")
    im_apparat = 0
    for basis, ordner, dateien in os.walk(kern):
        ordner[:] = [o for o in ordner if o != "__pycache__"]
        for name in sorted(dateien):
            if not name.endswith(".py"):
                continue
            pfad = os.path.join(basis, name)
            rel = os.path.relpath(pfad, root).replace(os.sep, "/")
            if basis == apparat:
                im_apparat += 1
            try:
                with open(pfad, encoding="utf-8") as f:
                    quelle = f.read()
            except (OSError, UnicodeDecodeError) as e:
                err(f"{rel}: nicht lesbar ({e}) - ein Werkzeug des Kerns, das sich "
                    f"nicht lesen laesst, laeuft auch nicht (D-229)")
                continue
            try:
                offen = _p70_offene_namen(quelle, name)
            except SyntaxError as e:
                err(f"{rel}: laedt nicht - {e.msg} (Zeile {e.lineno}). Ein Werkzeug "
                    f"des Kerns, das der Interpreter nicht uebersetzt, ist tot, und "
                    f"es faellt erst an dem Tag auf, an dem es gebraucht wird (D-229)")
                continue
            for bereich, offener in offen:
                wo = "im Modulrumpf" if bereich == name else f"in `{bereich}`"
                err(f"{rel}: der Name `{offener}` wird {wo} gelesen und nirgends "
                    f"gebunden - weder als Zuweisung noch als Import, Parameter "
                    f"oder eingebauter Name. Das ist ein NameError, der auf seinen "
                    f"Lauf wartet; genau so war `stand-b4.py` seit dem Umzug nach "
                    f"D-222 tot (D-229)")
    # DER ANKER, UND ER HAENGT AM MESSAPPARAT, NICHT AM KERN. Ein Anker `keine
    # einzige .py-Datei im Kern` waere durch Konstruktion nie erreichbar: Dieses
    # Skript ist selbst eine, und ohne es laeuft keine Pruefung. Eine Null durch
    # Konstruktion sieht aus wie eine gemessene Null (0.59.1). Erreichbar - und der
    # Gegenstand, um den es geht - ist der Messapparat: Steht seine Ablage und ist
    # kein Werkzeug mehr darin, hat diese Pruefung den Anlass verloren, aus dem sie
    # entstanden ist, und bestuende leise.
    if os.path.isdir(apparat) and im_apparat == 0:
        err(f"{KERN}/tests/erhebungen/: kein einziges Werkzeug geprueft - Pruefung "
            f"70 hat den Gegenstand verloren, aus dem sie entstanden ist; sie "
            f"bestuende sonst leise (D-23, D-229)")


# --- Pruefung 71: Kein Traeger des Kerns nennt einen Arbeitsplatz -------------------
#
# ANLASS, UND ER IST GEMESSEN. Am 2026-09-21, beim Bauen der Dossiers des Nachlaufs,
# brach `dossier-b4.py` ab - und im selben Blick fiel auf, was in seiner Zeile 33 stand:
#
#     KERN = os.path.join(r"C:\Users\<konto>\Documents\devpacks\koolie", ...)
#
# Neun Werkzeuge des Messapparats fuehrten einen Pfad dieses Arbeitsplatzes, acht davon
# mit dem Ziel `...\devpacks\test-devin-framework`. Solange der Apparat NEBEN dem
# Repositorium lag, stand das in einer unversionierten Ablage. Mit D-222 ist er
# HINEINgewandert und hat die Pfade mitgebracht - in dasselbe Repositorium, fuer das
# `0.78.1` eigens `UEBERGABE.local.md` eingefuehrt hat, weil eine Uebergabe mit
# Servername und Konto den Validator mit drei Fehlern und drei Warnungen beantwortet.
#
#   Wer einen Apparat umzieht, zieht seine Arbeitsplatzpfade mit um - und
#   veroeffentlicht sie, ohne es zu entscheiden.
#
# WARUM KEINE DER SIEBZIG ES SAH. Pruefung 6 kennt Secret-Muster, E-Mail-Adressen,
# IP-Adressen, interne Hostnamen und URLs ausserhalb der Allowlist. Ein Pfad in ein
# Benutzerprofil ist nichts davon - und er traegt trotzdem den Namen eines Menschen.
#
# WAS GEPRUEFT WIRD, UND WARUM SO. Ein absoluter Pfad in ein Benutzerprofil, dessen
# Kontosegment KEIN Platzhalter ist. `<KONTO>`, `%USERNAME%` und `$HOME` laufen durch -
# sie nennen niemanden. Eine Zeile mit der Marke `SYNTHETISCH` laeuft ebenso durch:
# Dieselbe Bauform wie das Feld `_uebererfasst` von Pruefung 68 - wer einen solchen
# Pfad braucht, sagt es in derselben Zeile, statt dass die Pruefung raet.
#
# GRENZE, UND SIE STEHT HIER: DER BESTAND DER AUFZEICHNUNGEN IST AUSGENOMMEN, NICHT DIE
# GATTUNG (seit 1.20.3, D-508, `K-85`). `tests/protocols/` und
# `governance/change-requests/` halten fest, WO gemessen wurde; ein Protokoll, das man
# umschreibt, ist keines mehr (D-141). Zehn von ihnen tragen den Kontonamen des Owners
# weiter, und dabei bleibt es - der Name steht nach D-323 ohnehin im Lizenzhinweis.
# Bis 1.20.2 nahm die Pruefung aber die ganzen beiden Ordner aus und liess damit jede
# KUENFTIGE Aufzeichnung ungeprueft. Seither ist die Ausnahme eine geschlossene Liste:
# Wer eine neue Aufzeichnung schreibt, schreibt `<konto>` oder die Marke.
P71_MUSTER = re.compile(
    r"(?:[A-Za-z]:[\\/]{1,2}Users|/home|/Users)[\\/]{1,2}([A-Za-z0-9._-]+)")
P71_AUSNAHME_ORDNER = (f"{KERN}/tests/protocols/",
                       f"{KERN}/governance/change-requests/")
P71_BESTAND = frozenset(f"{KERN}/{rel}" for rel in (
    "governance/change-requests/CR-2026-076-erster-sitzungstest.md",
    "governance/change-requests/CR-2026-077-sitzungstest-schranken.md",
    "tests/protocols/2026-09-11-erhebungen-K21-K26.md",
    "tests/protocols/2026-09-13-B06-gegenpruefung.md",
    "tests/protocols/2026-09-17-sitzungstest-pi-ds.md",
    "tests/protocols/2026-09-17-sitzungstest-schranken.md",
    "tests/protocols/2026-09-18-sitzungstest-5.md",
    "tests/protocols/2026-09-18-sitzungstest-ne-sc.md",
    "tests/protocols/2026-09-18-sitzungstest-pi-ds-2.md",
    "tests/protocols/2026-09-19-testblaetter-buendel-1.md"))
P71_MARKE = "SYNTHETISCH"
# Die Selbstprobe des Musters: Ohne sie koennte ein Ausdruck, der nichts mehr trifft,
# still bestehen - eine Null durch Konstruktion sieht aus wie eine gemessene Null
# (0.59.1). Der Anker haengt deshalb am MUSTER, nicht am Bestand: Der Bestand kann
# nicht verschwinden, solange dieses Skript selbst im Kern liegt.
P71_SELBSTPROBE = ("C:" + chr(92) + "Users" + chr(92) + "kontoname" + chr(92) + "x",  # SYNTHETISCH
                   "/home/kontoname/x",  # SYNTHETISCH
                   "/Users/kontoname/x")  # SYNTHETISCH


def check_arbeitsplatzpfad(root: str) -> None:
    """Pruefung 71 (D-231): Kein Traeger des Kerns nennt einen Arbeitsplatz."""
    kern = os.path.join(root, KERN)
    if not os.path.isdir(kern):
        return
    for probe in P71_SELBSTPROBE:
        if not P71_MUSTER.search(probe):
            err(f"Pruefung 71: das eigene Muster trifft {probe!r} nicht mehr - sie "
                f"haette ihren Gegenstand verloren und bestuende leise (D-23, D-231)")
            return
    for pfad in iter_text_files(root):
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        if not rel.startswith(f"{KERN}/"):
            continue
        if rel.startswith(P71_AUSNAHME_ORDNER) and rel in P71_BESTAND:
            continue
        text = read(pfad)
        for zeile in text.splitlines():
            if P71_MARKE in zeile:
                continue
            for m in P71_MUSTER.finditer(zeile):
                konto = m.group(1)
                # Ein Platzhalter nennt niemanden. Die drei Schreibweisen, die
                # dieses Repositorium und die beiden Betriebssysteme kennen.
                davor = zeile[:m.start(1)]
                if (konto.startswith(("<", "%", "$"))
                        or davor.endswith(("<", "%", "$", "{"))
                        or konto.upper() in ("USER", "USERNAME", "USERPROFILE")):
                    continue
                err(f"{rel}: der Pfad {m.group(0)!r} nennt ein Benutzerprofil mit "
                    f"dem Kontosegment {konto!r}. Ein Arbeitsplatz gehoert nicht in "
                    f"den Kern - der Ort wird gesagt (LW_ERHEBUNG, LW_UEBUNG) oder "
                    f"abgeleitet (ablage.WURZEL). Ein Platzhalter oder die Marke "
                    f"{P71_MARKE} in derselben Zeile laeuft durch (D-231)")


# --- Pruefung 76: Die Lage des Kerns steht an vier Stellen - und ueberall gleich ----
#
# ANLASS (D-299). Bis 0.87.0 war der Kern EIN Verzeichnissegment, und vier Werkzeuge
# haben <CORE_DIR> deshalb mit os.path.basename() aus dem eigenen Ort gebunden -
# install.py, build/assemble.py, dieser Validator und der Schutz-Hook. In install.py
# stand dabei woertlich, die Zeile stehe dort, "damit eine spaetere Umbenennung nur
# eine Stelle beruehrt". Sie haette die Umbenennung nicht ueberlebt: os.path.basename
# liefert fuer ".koolie/core" den Wert "core".
#
# WARUM DAS KEIN VALIDATORFEHLER GEWESEN WAERE: Dieser Validator bindet <CORE_DIR> an
# derselben Stelle auf dieselbe Weise. Er haette denselben falschen Wert eingesetzt wie
# install.py - und deshalb nichts gemeldet. Zwei Stellen, die einander decken (0.57.0),
# diesmal ueber Werkzeuggrenzen hinweg.
#
# ZWEI GEGENSTAENDE, und sie sind dieselbe Frage aus zwei Richtungen:
#   (1) Alle vier Angaben der Lage tragen denselben Wert.
#   (2) Keine von ihnen leitet ihn ueber os.path.basename ab.
# Ohne (2) waere (1) erfuellbar, indem alle vier denselben Fehler machen - und genau
# das war der Zustand bis 0.87.0.
#
# WARUM VIER STELLEN UND NICHT EINE: Der Schutz-Hook darf nichts aus dem Kern
# importieren - er muss auch dann entscheiden, wenn eine Installation unvollstaendig
# ist (D-31). ablage.py laeuft ausserhalb des Kerns gegen fremde Messbaeume. Die
# Doppelung ist gewollt; diese Pruefung ist ihr Preis.
P76_WERT_RE = re.compile(r"^(?:CORE_REL|KERN)\s*=\s*\"([^\"]+)\"", re.M)

P76_STELLEN = (
    "clientmap.py",
    "tests/scripts/pruefungen/gemeinsam.py",
    "tests/scripts/hook-check-secrets.py",
    "tests/erhebungen/ablage.py",
)

P76_BASENAME_RE = re.compile(r"<CORE_DIR>\"\]\s*=\s*os\.path\.basename")


def check_kernlage(root: str) -> None:
    """Pruefung 76 (D-299): Die Lage des Kerns steht ueberall gleich - und nirgends
    als basename eines Pfades."""
    if not P76_WERT_RE.search("CORE_REL = \"x/y\"\n"):
        err("Prüfung 76: das eigene Muster liest keine Lageangabe mehr – sie bestünde "
            "leise, während die vier Werkzeuge auseinanderlaufen (D-23)")
        return
    werte = {}
    for rel in P76_STELLEN:
        pfad = os.path.join(root, KERN, *rel.split("/"))
        if not os.path.isfile(pfad) and nicht_geliefert(root, f"{KERN}/{rel}"):
            hinweis(f"Prüfung 76 hält die Kernlage an drei statt vier Stellen: "
                    f"{KERN}/{rel} gehört zur Nachweisschicht und ist nicht geliefert (D-367)")
            continue
        if not os.path.isfile(pfad):
            err(f"{KERN}/{rel}: fehlt – Prüfung 76 hätte dort einen ihrer vier "
                f"Gegenstände verloren (D-23)")
            continue
        text = read(pfad)
        treffer = P76_WERT_RE.search(text)
        if not treffer:
            err(f"{KERN}/{rel}: führt keine Angabe der Kernlage mehr. Prüfung 76 hat "
                f"dort ihren Anker verloren und bestünde sonst leise (D-23)")
        else:
            werte[rel] = treffer.group(1)
        if P76_BASENAME_RE.search(text):
            err(f"{KERN}/{rel}: bindet <CORE_DIR> über os.path.basename(). Der Kern "
                f"liegt seit 0.88.0 zwei Segmente tief; basename() liefert davon nur "
                f"das letzte, und jede gerenderte Regeldatei trüge einen Pfad, den es "
                f"nicht gibt – ohne dass eine Prüfung es meldete (D-299)")
    if len(set(werte.values())) > 1:
        zeilen = ", ".join(f"{r} = '{w}'" for r, w in sorted(werte.items()))
        err(f"Die Lage des Kerns steht in {len(werte)} Werkzeugen und nicht überall "
            f"gleich: {zeilen}. Eine Installation läge dann je nach aufrufendem "
            f"Werkzeug an einem anderen Ort (D-299)")


# ---------------------------------------------------------------------------
# Pruefung 104: Die Verdrahtung der Pruefwerkzeuge (CR-2026-161, D-481)
# ---------------------------------------------------------------------------
#
# ANLASS. Seit 1.19.1 liegen die Pruefungen in einem Paket, und der Einstieg ruft sie;
# die Sonden liegen in Teilen, die der Einstieg des Sondenlaufs laedt (D-479). Eine
# Pruefung, die in ein Modul wandert und von niemandem gerufen wird, laeuft nie - und
# der Lauf endet mit "0 Fehler". Ein Sondenteil, den niemand laedt, meldet seine
# Einheiten nie an - und der Sondenlauf endet mit "alle bestanden". Beides ist die
# Null durch Konstruktion (0.59.1).
#
# WAS SIE PRUEFT, AM SYNTAXBAUM, OHNE ETWAS AUSZUFUEHREN:
#   (1) Jede Funktion check_* der obersten Ebene eines Moduls unter pruefungen/ wird
#       gerufen - von main() im Einstieg oder von einer anderen Funktion des Pakets
#       (check_skills ruft check_skills_in) -, und main() ruft keine zweimal und keine,
#       die es nicht gibt.
#   (2) Jeder Teil unter sonden/ wird vom Einstieg des Sondenlaufs geladen, und zwar in
#       der Reihenfolge seiner Nummer: Die Reihenfolge des Ladens ist die der Ausgabe
#       (D-49).
#
# GRENZE: Sie prueft die Verdrahtung, nicht, was eine Pruefung tut - das tun ihre
# Sonden. Sie sieht nur Funktionen mit dem Praefix check_ und Teile mit dem Praefix
# teil; eine Pruefung unter anderem Namen faellt durch.
P104_VALIDATOR = "tests/scripts/validate-framework.py"
P104_SONDEN = "tests/scripts/probe-pruefungen.py"
P104_TEIL_RE = re.compile(r"^teil(\d+)_\w+\.py$")


def _p104_baum(root: str, rel: str):
    """Der Syntaxbaum einer Datei unter dem Kern - oder None, dann ist gemeldet."""
    pfad = os.path.join(root, KERN, *rel.split("/"))
    if not os.path.isfile(pfad):
        err(f"{KERN}/{rel}: fehlt - Pruefung 104 haelt dort die Verdrahtung der "
            f"Pruefwerkzeuge (D-481)")
        return None
    try:
        return ast.parse(read(pfad))
    except SyntaxError as e:
        err(f"{KERN}/{rel}: laedt nicht - {e.msg} (Zeile {e.lineno}); Pruefung 104 kann "
            f"die Verdrahtung dort nicht lesen (D-481)")
        return None


def _p104_aufrufe(knoten) -> dict:
    """{Name: Anzahl} der Aufrufe von check_* unterhalb eines Knotens."""
    anzahl: dict = {}
    for n in ast.walk(knoten):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and \
                n.func.id.startswith("check_"):
            anzahl[n.func.id] = anzahl.get(n.func.id, 0) + 1
    return anzahl


def check_verdrahtung(root: str) -> None:
    """Pruefung 104 (D-481): Jede Pruefung wird gerufen, jeder Sondenteil geladen."""
    # --- Gegenstand 1: die Pruefungen -------------------------------------------------
    einstieg = _p104_baum(root, P104_VALIDATOR)
    paket = PAKET_JE_SKRIPT[P104_VALIDATOR]
    ordner = os.path.join(root, KERN, *paket.split("/"))
    definiert, im_paket = {}, {}
    for name in sorted(os.listdir(ordner)) if os.path.isdir(ordner) else []:
        if not name.endswith(".py"):
            continue
        modul = _p104_baum(root, f"{paket}/{name}")
        if modul is None:
            continue
        for n in modul.body:
            if isinstance(n, ast.FunctionDef) and n.name.startswith("check_"):
                definiert[n.name] = f"{paket}/{name}"
        for name_, zahl in _p104_aufrufe(modul).items():
            im_paket[name_] = im_paket.get(name_, 0) + zahl
    haupt = None if einstieg is None else next(
        (n for n in einstieg.body if isinstance(n, ast.FunctionDef) and n.name == "main"),
        None)
    if not definiert or haupt is None:
        err(f"Pruefung 104: {'keine Funktion check_* unter ' + KERN + '/' + paket + '/' if not definiert else 'keine Funktion main() in ' + KERN + '/' + P104_VALIDATOR} - "
            f"sie hat ihren Gegenstand verloren und bestuende sonst leise (D-23, D-481)")
    else:
        in_main = _p104_aufrufe(haupt)
        for name, wo in sorted(definiert.items()):
            if not in_main.get(name) and not im_paket.get(name):
                err(f"{KERN}/{wo}: {name}() wird von niemandem gerufen - weder von main() "
                    f"in {P104_VALIDATOR} noch im Paket. Eine Pruefung, die niemand ruft, "
                    f"laeuft nie, und der Lauf endet trotzdem mit 0 Fehlern (D-481)")
            elif in_main.get(name, 0) > 1:
                err(f"{KERN}/{P104_VALIDATOR}: main() ruft {name}() {in_main[name]}mal - "
                    f"jede Pruefung laeuft genau einmal, sonst meldet sie jeden Befund "
                    f"doppelt (D-481)")
        for name in sorted(set(in_main) - set(definiert)):
            err(f"{KERN}/{P104_VALIDATOR}: main() ruft {name}(), und kein Modul unter "
                f"{paket}/ definiert sie (D-481)")

    # --- Gegenstand 2: die Sondenteile ------------------------------------------------
    einstieg = _p104_baum(root, P104_SONDEN)
    paket = PAKET_JE_SKRIPT[P104_SONDEN]
    ordner = os.path.join(root, KERN, *paket.split("/"))
    teile = sorted((n[:-3] for n in (os.listdir(ordner) if os.path.isdir(ordner) else [])
                    if P104_TEIL_RE.match(n)),
                   key=lambda t: int(P104_TEIL_RE.match(t + ".py").group(1)))
    if not teile:
        err(f"Pruefung 104: kein Sondenteil teil<Nummer>_*.py unter {KERN}/{paket}/ - sie "
            f"hat ihren Gegenstand verloren und bestuende sonst leise (D-23, D-481)")
        return
    if einstieg is None:
        return
    geladen = [a.name for n in einstieg.body if isinstance(n, ast.ImportFrom)
               and n.module == os.path.basename(paket) for a in n.names]
    for teil in teile:
        if teil not in geladen:
            err(f"{KERN}/{paket}/{teil}.py: wird von {P104_SONDEN} nicht geladen - seine "
                f"Einheiten melden sich nie an, und der Sondenlauf endet trotzdem mit "
                f"'alle bestanden' (D-481)")
    for teil in geladen:
        if teil not in teile:
            err(f"{KERN}/{P104_SONDEN}: laedt {teil}, und unter {paket}/ gibt es keinen "
                f"Teil dieses Namens (D-481)")
    reihe = [t for t in geladen if t in teile]
    if reihe != [t for t in teile if t in reihe]:
        err(f"{KERN}/{P104_SONDEN}: laedt die Sondenteile nicht in der Reihenfolge ihrer "
            f"Nummer. Die Reihenfolge des Ladens ist die Reihenfolge der Ausgabe, und die "
            f"ist die zeilengleiche Abnahmeform (D-49, D-481)")


# Pruefung 107: Die Wirksamkeitsprobe haelt ihre Gegenfaelle (K-195, D-488, D-490).
#
# ANLASS. Die Hook-Vorpruefung des Messapparats hat seit 1.19.0 jeden Baum bestanden -
# auch einen ohne Hook-Skript: Unter Windows loeste 'cmd' $CLAUDE_PROJECT_DIR nicht auf,
# Python endete mit Exit 2, und Exit 2 galt als Sperre (D-490). Eine Probe, die auch das
# Fehlen ihres Gegenstands bestaetigt, ist die Null durch Konstruktion. Die Pruefung baut
# deshalb einen Wegwerfbaum mit der erzeugten Hook-Konfiguration von claude-code und
# verlangt von wirksamkeit.pruefe_hook drei Urteile:
#   (a) intakter Baum: keine fehlende Muss-Kontrolle;
#   (b) ohne Hook-Skript: H3 und H4 fehlen - Exit 2 ohne Sperrhinweis ist keine Sperre;
#   (c) Matcher ohne die Klasse mcp: H2 fehlt.
# GRENZE: der Hook-Teil der Probe am Pack claude-code. Startmeldung und Vertrauen braucht
# einen Client und sind an der Messung belegt (Protokoll 2026-09-29-schutzschicht).
def check_wirksamkeitsprobe(root: str) -> None:
    """Pruefung 107 (K-195, D-488, D-490): Die Probe unterscheidet Wirkung von Fehlen."""
    import importlib.util
    import shutil
    import tempfile
    kern = os.path.join(root, *KERN.split("/"))
    modul = os.path.join(kern, "wirksamkeit.py")
    skript = os.path.join(kern, "tests", "scripts", "hook-check-secrets.py")
    manifest = os.path.join(kern, "clients", "claude-code", "manifest.json")
    if not all(os.path.isfile(p) for p in (modul, skript, manifest)):
        return
    try:
        cm = _clientmap(root)
        spec = importlib.util.spec_from_file_location("koolie_wirksamkeit_p107", modul)
        wk = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(wk)
        man = json.loads(read(manifest))
        quelle = cm.load_source(kern, "hooks.json")
        hooks = cm._hooks_objekt(quelle, man)
        verben = [v for e in json.loads(quelle).get("PreToolUse", []) for v in e.get("on", [])
                  if any(h.get("enforcing") for h in e.get("hooks", []))]
    except Exception as fehler:  # noqa: BLE001 - jeder Ladefehler ist der Befund
        err(f"Pruefung 107: Die Wirksamkeitsprobe laesst sich nicht laden "
            f"({type(fehler).__name__}) - install.py --probe liefe nicht (K-195)")
        return

    def urteil(ohne_skript: bool = False, matcher_ohne_mcp: bool = False) -> set:
        with tempfile.TemporaryDirectory(prefix="koolie-p107-") as w:
            ziel = os.path.join(w, *KERN.split("/"), "tests", "scripts")
            os.makedirs(ziel)
            if not ohne_skript:
                shutil.copy2(skript, ziel)
            pack = os.path.join(w, *KERN.split("/"), "clients", "claude-code")
            os.makedirs(pack)
            shutil.copy2(manifest, pack)
            h = json.loads(json.dumps(hooks))
            if matcher_ohne_mcp:
                for e in h.get("PreToolUse", []):
                    e["matcher"] = "|".join(x for x in e["matcher"].split("|")
                                            if not x.startswith("mcp"))
            os.makedirs(os.path.join(w, ".claude"))
            with open(os.path.join(w, ".claude", "settings.json"), "w", encoding="utf-8") as fh:
                json.dump({"hooks": h}, fh)
            with open(os.path.join(w, "README.md"), "w", encoding="utf-8") as fh:
                fh.write("# Wegwerfbaum\n")
            erg = wk.Ergebnis()
            wk.pruefe_hook(w, man, verben, erg)
            return {k.split()[0] for _, k, _ in erg.verletzt}

    intakt = urteil()
    if intakt:
        err(f"Pruefung 107: Die Wirksamkeitsprobe meldet an einem intakten Baum fehlende "
            f"Kontrollen ({', '.join(sorted(intakt))}) - sie truege keinen Befund (K-195)")
    ohne = urteil(ohne_skript=True)
    if not {"H3", "H4"} <= ohne:
        err(f"Pruefung 107: Die Wirksamkeitsprobe besteht einen Baum ohne Hook-Skript "
            f"(gemeldet: {', '.join(sorted(ohne)) or 'nichts'}) - ein Exit 2 ohne "
            f"Sperrhinweis ist keine Sperre (D-490)")
    alt = urteil(matcher_ohne_mcp=True)
    if "H2" not in alt:
        err("Pruefung 107: Die Wirksamkeitsprobe erkennt einen Matcher ohne die "
            "Werkzeugklasse mcp nicht - ein veralteter Matcher fiele nicht auf (K-184, D-488)")


# --- Pruefung 112: Die Paketquellen und das Banner (CR-2026-168, D-518 bis D-521, K-155) --
#
# ANLASS, GEMESSEN (2026-09-30): Eine Paketquelle legt Koolie auf den Rechner, ins Projekt
# kommt es erst durch den Befehl `koolie` - und nur dieser Aufruf laeuft bei jeder
# Paketquelle im Terminal des Nutzers. pip fuehrt beim Installieren eines Wheels nichts
# aus, npm verschluckt die Ausgabe eines Installationsskripts, Chocolatey gibt ihm kein
# Terminal. Das Banner, das der Owner auf diesen Wegen verlangt, steht deshalb im Befehl
# (D-519), und die Pakete entstehen aus dem Release-Archiv mit paketquellen/bauen.py
# (D-520). Beides kann still brechen: ein Befehl, der install.py ohne Banner startet, und
# ein Bau, dessen Paket auf eine Datei zeigt, die es nicht traegt.
#
# GEPRUEFT, nur im Quellrepositorium (Projekte bekommen paketquellen/ nicht):
#   (a) die vier Dateien unter paketquellen/ liegen da;
#   (b) der Befehl: `--version` nennt die Version aus VERSION; ueber eine Pipe steht vor
#       der Ausgabe von install.py die Textvariante des Banners mit dieser Version; mit
#       KOOLIE_NO_BANNER=1 steht sie nicht da; ohne Argumente nimmt der Dialog das
#       Verzeichnis des Aufrufs mit Enter als Projekt (seit 1.24.1, D-532);
#   (c) der Bau: bauen.py baut aus einem Wegwerfarchiv mit den Dateien unter
#       paketquellen/ ohne Befund - seine Nachpruefung haelt Dateimenge, Version, RECORD,
#       die Ziele der Befehle, das Fehlen eines npm-Installationsskripts und die
#       Pruefsumme in beiden Manifesten; seit 1.24.0 auch die Beschreibung fuer PyPI und
#       npm ohne relativen Link (D-528) - und dasselbe fuer die Vorabversion --vorab 1 (D-529);
#   (d) die Veroeffentlichung ueber Trusted Publishing (2.0.0, K-210): .github/workflows/
#       publish.yml laeuft nur an einer Marke v*, gibt dem Workflow nur Leserecht, heftet jede
#       Action an einen Commit, prueft Signatur und VERSION der Marke im ersten Job, gibt
#       id-token nur Jobs mit Umgebung und laesst PyPI und npm (Umgebung release) erst nach
#       TestPyPI (Umgebung testpypi) laufen; seit 2.1.0 wartet der Job release auf die
#       Paketdatei von npm und vergleicht sie mit dem Hochgeladenen - npm traegt die Version
#       zuerst nur in die Metadaten ein, und der erste Lauf (2.0.0) scheiterte daran.
# GRENZE: Ob eine Paketquelle dem Befehl ein Terminal gibt, prueft keine Pruefung - das ist
# gemessen (Protokoll 2026-09-30-paketquellen: pip, uv, npm, Scoop). Die Homebrew-Formel ist
# gebaut, nicht gemessen. Die Veroeffentlichung erreicht keine Pruefung (D-521); ob die
# Paketseite die Beschreibung darstellt, ist gemessen (Protokoll 2026-10-01-erste-veroeffentlichung).
P112_DATEIEN = ("paketquellen/bauen.py", "paketquellen/koolie_befehl.py",
                "paketquellen/koolie.cmd", "paketquellen/npm/koolie.js")


P112_WORKFLOW = ".github/workflows/publish.yml"
P112_ACTION_RE = re.compile(r"^[\w.-]+/[\w./-]+@[0-9a-f]{40}$")


def _p112_workflow(root: str) -> None:
    """Gegenstand (d): Die Workflow-Datei veroeffentlicht nur eine signierte Marke, nach TestPyPI."""
    pfad = os.path.join(root, *P112_WORKFLOW.split("/"))
    if not os.path.isfile(pfad):
        err(f"{P112_WORKFLOW}: fehlt - ohne sie veroeffentlicht keine Marke auf PyPI und npm "
            f"(Pruefung 112)")
        return
    if yaml is None:
        hinweis(f"{P112_WORKFLOW}: PyYAML fehlt, Gegenstand (d) der Pruefung 112 nicht geprueft")
        return
    try:
        wf = yaml.safe_load(read(pfad)) or {}
    except yaml.YAMLError as fehler:
        err(f"{P112_WORKFLOW}: kein gueltiges YAML ({type(fehler).__name__}) (Pruefung 112)")
        return
    # YAML 1.1 liest den Schluessel 'on' als True.
    ausloeser = wf.get("on", wf.get(True))
    if ausloeser != {"push": {"tags": ["v*"]}}:
        err(f"{P112_WORKFLOW}: laeuft nicht nur an einer Marke v* ({ausloeser!r}) - jeder andere "
            f"Ausloeser veroeffentlichte ohne signierte Marke (Pruefung 112)")
    if wf.get("permissions") != {"contents": "read"}:
        err(f"{P112_WORKFLOW}: die Rechte des Workflows sind nicht auf 'contents: read' "
            f"beschraenkt (Pruefung 112)")
    jobs = wf.get("jobs") or {}
    umgebung = {}
    for name, job in jobs.items():
        u = job.get("environment")
        umgebung[name] = u.get("name") if isinstance(u, dict) else u
        for schritt in job.get("steps") or []:
            uses = schritt.get("uses")
            if uses and not P112_ACTION_RE.match(uses):
                err(f"{P112_WORKFLOW}: Job '{name}' nutzt '{uses}' ohne festen Commit - ein "
                    f"bewegliches Tag kann den Code der Veroeffentlichung aendern (Pruefung 112)")
        if (job.get("permissions") or {}).get("id-token") and not umgebung[name]:
            err(f"{P112_WORKFLOW}: Job '{name}' darf ein id-token holen, hat aber keine Umgebung "
                f"(Pruefung 112)")

    def vorgaenger(name: str, gesehen: set) -> set:
        needs = jobs.get(name, {}).get("needs") or []
        for n in [needs] if isinstance(needs, str) else needs:
            if n not in gesehen:
                gesehen.add(n)
                vorgaenger(n, gesehen)
        return gesehen

    def skript(name: str) -> str:
        return "\n".join(s.get("run", "") for s in jobs[name].get("steps") or [])

    pruef = [n for n in jobs if "git tag -v" in skript(n) and "KOOLIE_ALLOWED_SIGNERS"
             in str(jobs[n]) and ".koolie/core/VERSION" in skript(n)]
    test = [n for n, u in umgebung.items() if u == "testpypi"]
    frei = [n for n, u in umgebung.items() if u == "release"]
    if not pruef:
        err(f"{P112_WORKFLOW}: kein Job prueft Signatur und VERSION der Marke ('git tag -v' gegen "
            f"KOOLIE_ALLOWED_SIGNERS) (Pruefung 112)")
    if not test or not frei:
        err(f"{P112_WORKFLOW}: es fehlt ein Job mit Umgebung 'testpypi' oder 'release' "
            f"(Pruefung 112)")
        return
    for n in test:
        if pruef and not set(pruef) & vorgaenger(n, set()):
            err(f"{P112_WORKFLOW}: Job '{n}' (TestPyPI) haengt nicht an der Pruefung der Marke "
                f"(Pruefung 112)")
    for n in frei:
        if not set(test) & vorgaenger(n, set()):
            err(f"{P112_WORKFLOW}: Job '{n}' (PyPI und npm) laeuft nicht erst nach TestPyPI - "
                f"die Probe muss vor der Veroeffentlichung abbrechen koennen (Pruefung 112)")
        if not ("registry.npmjs.org/@renoxar/koolie/-/" in skript(n) and "cmp -s" in skript(n)):
            err(f"{P112_WORKFLOW}: Job '{n}' wartet nicht auf die Paketdatei von npm und "
                f"vergleicht sie nicht mit dem Hochgeladenen - npm zeigt die Version in den "
                f"Metadaten, bevor die Datei abrufbar ist (Pruefung 112)")


def _p112_befehl(root: str, *argv: str, ohne_banner: bool = False, cwd: str | None = None,
                 eingabe: str | None = None) -> str:
    import subprocess
    umgebung = {k: v for k, v in os.environ.items()
                if k not in ("KOOLIE_NO_BANNER", "NO_COLOR", "COLUMNS")}
    umgebung["PYTHONIOENCODING"] = "utf-8"
    if ohne_banner:
        umgebung["KOOLIE_NO_BANNER"] = "1"
    p = subprocess.run([sys.executable, os.path.join(root, "paketquellen", "koolie_befehl.py"),
                        *argv], capture_output=True, encoding="utf-8", errors="replace",
                       env=umgebung, timeout=120, cwd=cwd, input=eingabe)
    return p.stdout or ""


def check_paketquellen(root: str) -> None:
    """Pruefung 112 (D-519, D-520, K-155): Der Befehl gibt das Banner aus, der Bau traegt."""
    if not ist_quellrepositorium(root):
        return
    fehlend = [rel for rel in P112_DATEIEN if not os.path.isfile(os.path.join(root, *rel.split("/")))]
    if fehlend:
        err(f"{fehlend[0]}: fehlt - ohne diese Datei baut keine Paketquelle den Befehl "
            f"'koolie' (Pruefung 112, D-520)")
        return
    _p112_workflow(root)
    version = read(os.path.join(root, *KERN.split("/"), "VERSION")).strip()
    try:
        aus = _p112_befehl(root, "--version")
        if aus.strip() != f"koolie {version}":
            err(f"paketquellen/koolie_befehl.py: '--version' liefert {aus.strip()[:40]!r} statt "
                f"'koolie {version}' (Pruefung 112)")
        aus = _p112_befehl(root, "--help")
        b, u = aus.find(f"KOOLIE v{version}"), aus.find("usage:")
        if b < 0 or u < 0 or b > u:
            err("paketquellen/koolie_befehl.py: startet install.py ohne das Banner davor - auf "
                "den Wegen der Paketquellen erschiene es nicht (Pruefung 112, D-519)")
        aus = _p112_befehl(root, "--help", ohne_banner=True)
        if "KOOLIE v" in aus or "usage:" not in aus:
            err("paketquellen/koolie_befehl.py: KOOLIE_NO_BANNER=1 schaltet das Banner nicht ab "
                "oder unterdrueckt install.py mit (Pruefung 112, D-506)")
        import tempfile as _tf
        with _tf.TemporaryDirectory(prefix="koolie-p112-hier-") as hier:
            aus = _p112_befehl(root, ohne_banner=True, cwd=hier, eingabe="\nq\n")
            if "Welcher KI-Client" not in aus:
                err("paketquellen/koolie_befehl.py: der Dialog nimmt das Verzeichnis des Aufrufs "
                    "nicht mit Enter als Projekt - uvx, pipx run und npx starten ihn dort "
                    "(Pruefung 112, D-532)")
    except Exception as fehler:  # noqa: BLE001 - jeder Startfehler ist der Befund
        err(f"paketquellen/koolie_befehl.py: laesst sich nicht starten ({type(fehler).__name__}) "
            f"(Pruefung 112)")
    import contextlib
    import importlib.util
    import io
    import tarfile
    import tempfile
    with tempfile.TemporaryDirectory(prefix="koolie-p112-") as w:
        archiv = os.path.join(w, f"koolie-{version}.tar.gz")
        with tarfile.open(archiv, "w:gz") as tf:
            for rel in P112_DATEIEN + (f"{KERN}/VERSION", "LICENSE", "README.en.md"):
                tf.add(os.path.join(root, *rel.split("/")), arcname=f"koolie-{version}/{rel}")
        # einmal die Version der Marke, einmal die Vorabversion fuer TestPyPI (D-529)
        for art, zusatz in (("", []), (", als Vorabversion gebaut", ["--vorab", "1"])):
            puffer = io.StringIO()
            try:
                spec = importlib.util.spec_from_file_location(
                    "koolie_bauen_p112", os.path.join(root, "paketquellen", "bauen.py"))
                bauen = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(bauen)
                with contextlib.redirect_stdout(puffer), contextlib.redirect_stderr(puffer):
                    rc = bauen.main(["--archiv", archiv, "--aus", os.path.join(w, "aus"), *zusatz])
            except Exception as fehler:  # noqa: BLE001
                rc, puffer = 1, io.StringIO(f"{type(fehler).__name__}: {fehler}")
            if rc != 0:
                text = puffer.getvalue()
                befunde = ([z.strip() for z in text.split("BEFUNDE:", 1)[1].splitlines()
                            if z.strip()]
                           if "BEFUNDE:" in text else text.strip().splitlines()[-1:])[:3]
                err(f"paketquellen/bauen.py: baut aus einem Wegwerfarchiv nicht ohne Befund{art} "
                    f"({' | '.join(befunde)}) (Pruefung 112, D-520)")
                return
