"""Der Schutz-Hook: Interpreter, Werkzeugabdeckung, fail-closed, Ablageort, neutrale
Skripte, Eingabeschema, Durchsetzungstiefe, Hookblock, Sperrform und Ziel statt Inhalt.

Pruefungen 15, 16, 17, 18, 21, 31, 32, 43, 86 und 98. Teil des Validators validate-
framework.py, seit 1.19.1 nach Gegenstand in Module geteilt (K-174). Das Register aller
Pruefungen steht im Kopfkommentar des Einstiegs, die Grenze jeder einzelnen in ihrem
Kopfkommentar hier."""
from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys

from .gemeinsam import (
    _client_packs, _hook_interpreter, _hook_lauf, _walk_text_files, err,
    formatgebunden, HOOK_SONDE, KERN, read, tabellenzellen, warn)


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
        # Dritte Ablageform (seit 1.13.0, D-414): eine LISTE von Hooks mit Ausloeser je
        # Eintrag und dem Kommando unter action. Bis dahin las diese Funktion nur
        # Objekte je Ereignis - und brach an einer Liste mit einer Ausnahme ab.
        if isinstance(daten, dict) and isinstance(daten.get("hooks"), list):
            for h in daten["hooks"]:
                if not isinstance(h, dict):
                    continue
                befehl = (h.get("action") or {}).get("command")
                if befehl:
                    treffer.append((f"{rel}:{h.get('trigger', '?')}", befehl))
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
                if not isinstance(eintrag, dict):
                    continue  # eine Liste ohne Hook-Eintraege, etwa "tools" eines Profils
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
    "claude-code": {"session_id": "s", "transcript_path": "/home/u/.claude/projects/p/s.jsonl",  # SYNTHETISCH: Sondeneingabe, kein Arbeitsplatz (D-231)
                    "cwd": "/projekt", "permission_mode": "default",
                    "hook_event_name": "PreToolUse", "tool_use_id": "t"},
    "devin-desktop": {"session_id": "s", "prompt_id": "p", "hook_event_name": "PreToolUse",
                      "tool_use_id": "t"},
    # Aufgezeichnet am 2026-09-26 in einer interaktiven Sitzung (CR-2026-150): fuenf
    # Felder, cwd ist die Projektwurzel.
    "kiro": {"session_id": "s", "hook_event_name": "PreToolUse", "cwd": "/projekt"},
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
    if formatgebunden(man, 43):
        return  # D-346, D-416: diese Ausgabeform erreicht die Pruefung nicht
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
# PRUEFUNG 86: DIE SPERRFORM DES SCHUTZ-HOOKS
# ---------------------------------------------------------------------------
# ANLASS, UND ER IST GEMESSEN (CR-2026-133, D-347). Ein Hook, der laeuft, ist nicht
# dasselbe wie ein Hook, der sperrt. Am 2026-09-23 ist an einer realen Installation von
# openai-codex gemessen worden, was die bis dahin einzige Sperrform des Schutz-Hooks -
# das Objekt {"decision": "block"} und Exit-Code 2 - bei diesem Client bewirkt: NICHTS.
# Der Client meldet den Hook als fehlgeschlagen und fuehrt die Operation aus; im
# Gegenlauf kam der Koederinhalt woertlich heraus. Dieselbe Sperre in der Form, die
# dieser Client liest, blockiert - und zwar auch in dem Betriebsmodus, der Rueckfragen
# und Sandkasten abschaltet.
#   ➡️ Eine Sperre ist eine AUSSAGE AN DEN CLIENT, und ihre Form ist clientgebunden.
#      Ein Pack, das die falsche nennt, liefert einen Schutz-Hook aus, der laeuft,
#      etwas ausgibt und nichts verhindert - und nichts meldet es.
#
# GEPRUEFT WIRD DIE KETTE, NICHT DAS MANIFESTFELD - dieselbe Bauform wie Pruefung 17:
#   (1) die vom Pack genannte Form steht in der Formenliste des Skripts,
#   (2) das Skript gibt fuer sie wirklich eine Sperre dieser Form aus (Aufruf mit einer
#       Eingabe, die es blockieren muss),
#   (3) die erzeugte Hook-Konfiguration reicht die Form am Kommando durch.
# Ohne (2) bliebe es bei einem Listenvergleich, und ein Listenvergleich belegt
# Uebereinstimmung, nicht Wirkung.
def check_sperrform(root: str, man: dict) -> None:
    """Pruefung 86 (D-347): Die Sperrform des Schutz-Hooks wirkt beim genannten Client."""
    kern = os.path.join(root, KERN)
    skript = os.path.join(kern, "tests", "scripts", "hook-check-secrets.py")
    if not os.path.exists(skript):
        return
    quelle = read(skript)
    m = re.search(r"^SPERRFORMEN\s*=\s*\(([^)]*)\)", quelle, re.M)
    if not m:
        err(f"{KERN}/tests/scripts/hook-check-secrets.py: keine Liste SPERRFORMEN. "
            f"Ohne sie kann kein Pack seine Sperrform nennen, und Prüfung 86 hätte "
            f"keinen Gegenstand (D-23)")
        return
    bekannt = set(re.findall(r'"([^"]+)"', m.group(1)))

    form = man.get("hook_block_form")
    if form and form not in bekannt:
        err(f"clients/{man.get('client', '?')}/manifest.json: hook_block_form "
            f"'{form}' kennt das Skript des Schutz-Hooks nicht. Bekannt sind "
            f"{', '.join(sorted(bekannt))}. Eine Sperrform, die das Skript nicht kennt, "
            f"fällt auf die Standardform zurück – und die ist bei diesem Client "
            f"gemessen wirkungslos (D-347)")
        return

    # (2) Wirkung: Das Skript blockiert eine Eingabe, die es blockieren MUSS, und gibt
    # dabei die verlangte Form aus.
    eingabe = json.dumps({
        "hook_event_name": "PreToolUse", "cwd": root,
        "tool_name": "Write", "tool_input": {"file_path": ".env"}})
    argumente = [sys.executable, skript]
    if form:
        argumente += ["--sperrform", form]
    try:
        lauf = subprocess.run(argumente, input=eingabe, capture_output=True,
                              text=True, timeout=30)
    except (OSError, subprocess.SubprocessError) as exc:
        err(f"{KERN}/tests/scripts/hook-check-secrets.py: nicht ausführbar ({exc}); "
            f"Prüfung 86 kann die Sperrform nicht an ihrer Wirkung messen")
        return
    try:
        ausgabe = json.loads(lauf.stdout.strip() or "{}")
    except json.JSONDecodeError:
        ausgabe = {}
    if form == "stderr-grund":
        # D-417: Exit 2 UND ein nicht leerer Grund auf stderr - mit leerem Grund laesst
        # dieser Client die Operation laufen, gemessen am 2026-09-26.
        if lauf.returncode != 2 or not (lauf.stderr or "").strip():
            err(f"{KERN}/tests/scripts/hook-check-secrets.py: Sperrform 'stderr-grund' "
                f"verlangt Exit 2 und einen Grund auf stderr; gemessen wurden Exit "
                f"{lauf.returncode} und {len((lauf.stderr or '').strip())} Zeichen auf "
                f"stderr. Ohne Grund lässt der Client die Operation laufen (D-417)")
    elif form == "permission-json":
        # D-441: Sperre mit permission deny UND Exit 2 - und, das ist die zweite Haelfte,
        # ein DURCHLASS mit gueltigem JSON. Mit failClosed wertet dieser Client einen
        # Hook ohne Ausgabe als gescheitert und sperrt jede Operation, gemessen am
        # 2026-09-26. Die Durchlassprobe ist eine harmlose Leseoperation.
        if ausgabe.get("permission") != "deny" or lauf.returncode != 2:
            err(f"{KERN}/tests/scripts/hook-check-secrets.py: Sperrform 'permission-json' "
                f"verlangt permission 'deny' und Exit 2; gemessen wurden "
                f"'{ausgabe.get('permission')}' und Exit {lauf.returncode} (D-441)")
        harmlos = json.dumps({"hook_event_name": "preToolUse", "tool_name": "Read",
                              "tool_input": {"file_path": "README.md"}})
        try:
            durch = subprocess.run(argumente + ["--fail-closed"], input=harmlos,
                                   capture_output=True, text=True, timeout=30, cwd=root)
        except (OSError, subprocess.SubprocessError):
            durch = None
        try:
            antwort = json.loads(durch.stdout.strip()) if durch else None
        except ValueError:
            antwort = None
        if durch is None or durch.returncode != 0 or not isinstance(antwort, dict) \
                or antwort.get("permission") == "deny":
            err(f"{KERN}/tests/scripts/hook-check-secrets.py: Sperrform 'permission-json' "
                f"verlangt beim Durchlass Exit 0 und ein JSON-Objekt ohne deny; gemessen "
                f"wurde {('Exit ' + str(durch.returncode)) if durch else 'kein Lauf'} mit "
                f"{(durch.stdout or '').strip()[:40]!r}. Ohne Antwort wertet der Client den "
                f"Hook mit failClosed als gescheitert und sperrt JEDE Operation (D-441)")
    elif form == "hook-specific-output":
        entscheidung = (ausgabe.get("hookSpecificOutput") or {}).get("permissionDecision")
        if entscheidung != "deny" or lauf.returncode != 0:
            err(f"{KERN}/tests/scripts/hook-check-secrets.py: Sperrform "
                f"'hook-specific-output' verlangt permissionDecision 'deny' und "
                f"Exit 0; gemessen wurden '{entscheidung}' und Exit {lauf.returncode}. "
                f"Ein Exit ungleich 0 ist bei diesem Client ein FEHLGESCHLAGENER Hook, "
                f"und ein fehlgeschlagener Hook lässt die Operation laufen (D-347)")
    else:
        if ausgabe.get("decision") != "block" or lauf.returncode != 2:
            err(f"{KERN}/tests/scripts/hook-check-secrets.py: Standard-Sperrform "
                f"verlangt decision 'block' und Exit 2; gemessen wurden "
                f"'{ausgabe.get('decision')}' und Exit {lauf.returncode}")

    # (3) Die erzeugte Konfiguration reicht die Form durch.
    if not form:
        return
    hooks_rel = (man.get("runtime_placeholders") or {}).get("<HOOKS_FILE>")
    if not hooks_rel:
        return
    pfad = os.path.join(root, *hooks_rel.split("/"))
    if not os.path.exists(pfad):
        return
    text = read(pfad)
    if "hook-check-secrets.py" in text and f"--sperrform {form}" not in text:
        err(f"{hooks_rel}: das Kommando des Schutz-Hooks trägt die Sperrform "
            f"'{form}' nicht. Das Pack nennt sie, die erzeugte Datei reicht sie nicht "
            f"durch – der Hook liefe mit der Standardform und sperrte bei diesem "
            f"Client nichts (D-347)")


# ---------------------------------------------------------------------------
# PRUEFUNGEN 98 BIS 100 (CR-2026-156): DER ERSTE PROJEKTEINSATZ
# ---------------------------------------------------------------------------
# ANLASS: Befunde aus dem Einsatz von 1.16.0 in einem Projekt mit devin-desktop
# (2026-09-27): Der Schutz-Hook sperrte einen Aenderungsantrag nach seinem INHALT (A2),
# drei rein lesende Skills waren dem Client verwehrt (A1), und besprochene Entscheidungen
# liessen sich nur als Vorlage zum Abschreiben liefern (Modus M6, D-446).
P98_ANKER = "def ziele_der_schreiboperation("
P98_INHALT = ("siehe .koolie/core/VERSION, .koolie/project-overlay/OVERLAY.md, AGENTS.md "
              "und .devin/rules/00-framework-core.md")


def _p98_werkzeuge(root: str) -> list:
    """(Pack, erstes Schreibwerkzeug) je Manifest."""
    out = []
    packs = os.path.join(root, KERN, "clients")
    for name in sorted(os.listdir(packs)) if os.path.isdir(packs) else []:
        mf = os.path.join(packs, name, "manifest.json")
        if not os.path.isfile(mf):
            continue
        try:
            daten = json.loads(read(mf)) or {}
        except json.JSONDecodeError:
            continue
        schreiben = [w for w in ((daten.get("hook_tools") or {}).get("write") or [])
                     if isinstance(w, str) and w.strip()]
        if schreiben:
            out.append((daten.get("client", name), schreiben))
    return out


def check_hook_ziel_statt_inhalt(root: str, man: dict) -> None:
    """Pruefung 98 (D-449): Der Hook misst das Ziel einer Schreiboperation, nicht ihren Inhalt."""
    skript = os.path.join(root, KERN, "tests", "scripts", "hook-check-secrets.py")
    if not os.path.isfile(skript):
        return
    if P98_ANKER not in read(skript):
        err(f"{KERN}/tests/scripts/hook-check-secrets.py: '{P98_ANKER}' fehlt. Pruefung 98 "
            f"misst, dass eine Schreiboperation an ihren Zielen gemessen wird; ohne diese "
            f"Stufe bestuende sie leise (D-23, D-449)")
        return
    interpreter = _hook_interpreter()
    if interpreter is None:
        return
    for pack, werkzeuge in _p98_werkzeuge(root):
        for werkzeug in werkzeuge:
            if werkzeug.lower() == "apply_patch":
                frei = {"command": "*** Begin Patch\n*** Add File: docs/p98.md\n+"
                                   + P98_INHALT + "\n*** End Patch"}
                kern = {"command": "*** Begin Patch\n*** Add File: " + KERN
                                   + "/p98.txt\n+x\n*** End Patch"}
            else:
                frei = {"file_path": "docs/p98.md", "content": P98_INHALT}
                kern = {"file_path": KERN + "/p98.txt", "content": "x"}
            ergebnis = _hook_lauf(interpreter, skript, json.dumps(
                {"tool_name": werkzeug, "tool_input": frei}))
            if ergebnis != 0:
                err(f"{pack}/manifest.json: Der Schutz-Hook sperrt das Werkzeug '{werkzeug}' mit "
                    f"einem freien Ziel (docs/), weil sein Inhalt geschuetzte Pfade NENNT "
                    f"(Exit {ergebnis}). Gemessen wird das Ziel, nicht der Inhalt - sonst kann "
                    f"kein Aenderungsantrag die Pfade nennen, um die es geht (D-449)")
            ergebnis = _hook_lauf(interpreter, skript, json.dumps(
                {"tool_name": werkzeug, "tool_input": kern}))
            if ergebnis != 2:
                err(f"{pack}/manifest.json: Der Schutz-Hook laesst das Werkzeug '{werkzeug}' in "
                    f"das Kernverzeichnis schreiben (Exit {ergebnis} statt 2) - die Messung am "
                    f"Ziel darf das Ziel nicht verlieren (D-449)")
