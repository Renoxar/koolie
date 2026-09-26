#!/usr/bin/env python3
"""
install.py - Legt die Wurzeldateien des Koolie-Frameworks in einem Projekt an.

Hintergrund: Zwei Dinge muessen im Wurzelverzeichnis des Projekts liegen, weil der
KI-Client sie nur dort findet - die Wurzel-Anweisungsdatei und die Laufzeitschicht mit
Regeln, Skills, Agentenprofilen, Berechtigungen und Hooks. Alles Uebrige des Frameworks
liegt gebuendelt im Kernverzeichnis und wird nur kopiert, nicht installiert.

Die wenigsten dieser Dateien liegen noch je Client Pack: Regeltexte, Skills, Overlay,
Berechtigungen und Hooks liegen einmal im Kern und werden bei der Installation in die
Form des gewaehlten Clients gebracht. Wie, steht im Manifest des Packs; die
Semantikabbildung der Berechtigungen und Hooks in clientmap.py.

Dieses Skript loest das auf: Es kopiert die Wurzelbestandteile aus dem
root-template/ des gewaehlten Client Packs an ihren Platz und unterscheidet dabei
sauber zwischen Core (wird bei einem Update ueberschrieben) und Projektbestandteilen
(werden nie ueberschrieben).

Welcher KI-Client verwendet wird, entscheidet --client. Die Wurzelartefakte jedes
Clients liegen unter clients/<client>/root-template/; welche Zusagen
des Frameworks ein Client technisch durchsetzt, steht in seiner CLIENT_PACK.md
(clients/README.md).

Aufruf (aus dem Wurzelverzeichnis des Projekts):

    python .koolie/core/install.py                        # Erstinstallation, Standard-Client
    python .koolie/core/install.py --client <name>        # anderer Client
    python .koolie/core/install.py --list-clients         # verfuegbare Client Packs
    python .koolie/core/install.py --overlay general      # Erstinstallation mit Overlay-Muster
    python .koolie/core/install.py --overlay              # verfuegbare Overlay-Muster
    python .koolie/core/install.py --update               # Core aktualisieren
    python .koolie/core/install.py --check                # nur pruefen, nichts schreiben
    python .koolie/core/install.py --dry-run              # zeigen, was passieren wuerde

Aufruf aus dem Framework (Klon oder entpacktes Release-Archiv) in ein anderes Projekt -
kopiert nur den Kern und installiert danach dort (D-362):

    python .koolie/core/install.py --target <projekt> [--client <name>] [--overlay <name>]
    python .koolie/core/install.py --target <projekt> --update      # Projekt heben
    python .koolie/core/install.py --target <projekt> --lieferumfang nutzung
                                           # ohne Nachweisschicht (D-367); gilt beim Heben weiter

Die Starter install.cmd (Windows) und install.command (macOS) in der Wurzel des
Frameworks fragen diese Angaben ab (install_dialog.py) und rufen genau das auf.

Exit-Code 0 = in Ordnung, 1 = Abweichungen gefunden (bei --check) oder Fehler.
"""
from __future__ import annotations

import argparse
import filecmp
import json
import re
import hashlib
import os
import shutil
import subprocess
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clientmap  # noqa: E402  (liegt neben dieser Datei)

CLIENT_PACKS = os.path.join(HERE, "clients")
# Der Standard bleibt der Client, fuer den das Framework urspruenglich gebaut wurde.
# Ein Projekt waehlt bei der Erstinstallation, danach steht die Wahl im Overlay.
DEFAULT_CLIENT = "devin-desktop"


def available_clients() -> list[str]:
    """Client Packs mit Wurzelartefakten. Ein Pack ohne root-template/ ist nicht installierbar."""
    if not os.path.isdir(CLIENT_PACKS):
        return []
    return sorted(
        name for name in os.listdir(CLIENT_PACKS)
        if not name.startswith("_")
        and os.path.isdir(os.path.join(CLIENT_PACKS, name, "root-template"))
        and os.path.exists(os.path.join(CLIENT_PACKS, name, "manifest.json"))
    )


def client_template(client: str) -> str:
    return os.path.join(CLIENT_PACKS, client, "root-template")

# ---------------------------------------------------------------------------
# Welche Datei Core ist und welche dem Projekt gehoert, steht im Manifest des
# Client Packs (clients/<client>/manifest.json). Frueher standen diese Listen hier
# fest verdrahtet - das ging nur, solange es genau einen Client gab.
#
# Core          = gehoert zum Framework, wird bei --update ueberschrieben.
#                 Aenderungswuensche laufen als Aenderungsantrag an den Framework Owner
#                 (.koolie/core/governance/FEEDBACK_PROCESS.md).
# Saat (seed)   = wird nur bei der Erstinstallation angelegt. Danach gehoert es dem
#                 Projekt und wird nie ueberschrieben - hier stehen die Projektwerte.
#
# Laufzeitfassungen von Packs stehen absichtlich in keiner der beiden Listen: Ein Pack
# wird im Overlay aktiviert (framework/role-packs/README.md Punkt 4), nicht durch die
# Installation. Wer ein Pack aktiviert hat, bekommt seine Bestandteile ueber
# activated_pack_relpaths() aktualisiert.
# ---------------------------------------------------------------------------
MANIFEST_PFLICHTFELDER = ("client", "skills_dir", "pack_runtime_dir",
                          "core_skill_prefix", "core_paths", "seed_paths")


def nachschritte(schritte: list, ab: int) -> None:
    """Gibt die packeigenen Schritte nach Installation oder Hebung numeriert aus.

    Sie stehen im Manifest (post_install_steps, post_update_steps), weil sie nur ein Pack
    betreffen - bei openai-codex die Vertrauensbedingung, ohne die Konfiguration und
    Schutz-Hook nicht laden (K-123, D-395). Lange Saetze werden umbrochen.
    """
    for i, schritt in enumerate(schritte, ab):
        zeilen = textwrap.wrap(schritt, width=80)
        for j, zeile in enumerate(zeilen):
            print(f"  {i}. {zeile}" if j == 0 else f"     {zeile}")


def load_manifest(client: str) -> dict:
    path = os.path.join(CLIENT_PACKS, client, "manifest.json")
    with open(path, encoding="utf-8") as fh:
        m = json.load(fh)
    fehlend = [f for f in MANIFEST_PFLICHTFELDER if f not in m]
    if fehlend:
        raise ValueError(f"{client}/manifest.json: Pflichtfelder fehlen: {', '.join(fehlend)}")
    # <CORE_DIR> steht in keinem Manifest: Die Lage des Kernverzeichnisses ist keine
    # Eigenschaft eines Clients, sondern dieser Installation. Sie wird hier gesetzt,
    # damit eine spaetere Umbenennung (Roadmap P3) nur eine Stelle beruehrt.
    #
    # 0.88.0: Bis dahin stand hier os.path.basename(HERE) - und genau diese Zeile,
    # die eine Umbenennung billig machen sollte, waere an ihr zerbrochen: Der Kern
    # liegt seit 0.88.0 unter `.koolie/core`, und basename() liefert davon "core".
    # Die Lage steht deshalb in clientmap.CORE_REL (D-299).
    m.setdefault("runtime_placeholders", {})["<CORE_DIR>"] = clientmap.CORE_REL
    return m


class Report:
    def __init__(self) -> None:
        self.created: list[str] = []
        self.updated: list[str] = []
        self.unchanged: list[str] = []
        self.kept: list[str] = []
        self.drifted: list[str] = []
        self.missing: list[str] = []


def sha(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def iter_files(base: str, rel: str):
    """Liefert alle Dateien unter rel (Datei oder Verzeichnis), relativ zu base."""
    full = os.path.join(base, rel)
    if os.path.isfile(full):
        yield rel
    elif os.path.isdir(full):
        for dirpath, dirnames, filenames in os.walk(full):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            for fn in sorted(filenames):
                yield os.path.relpath(os.path.join(dirpath, fn), base).replace(os.sep, "/")


def core_relpaths(template: str, man: dict) -> list[str]:
    """Alle Core-Dateien des Templates, inklusive der Framework-Skills."""
    out: list[str] = []
    for rel in man["core_paths"]:
        out.extend(iter_files(template, rel))
    # Die Framework-Skills stehen seit 0.5.0 nicht mehr im Template, sondern einmal
    # unter framework/skills/; sie werden ueber framework_skill_files() gerendert.
    return out


def activated_pack_relpaths(root: str, man: dict) -> list[str]:
    """Bestandteile von Packs, die dieses Projekt aktiviert hat.

    Ein Pack wird aktiviert, indem seine Skills nach .devin/skills/ und seine Laufzeitfassung
    nach .devin/rules/ kopiert werden. Ob ein Pack aktiv ist, entscheidet das Projekt
    (Overlay Abschnitt 1) - was in einem aktivierten Pack-Skill steht, ist dagegen
    Framework-Inhalt und gehoert damit zum Core-Aktualisierungsumfang. Ohne diese Funktion
    behielte ein Projekt seine Kopie aus dem Release der Aktivierung, stillschweigend und
    ohne Hinweis.

    Nur was in einer Pack-Quellablage dieses Kerns eine Entsprechung hat, wird erfasst.
    Projekteigene Packs (etwa unter .koolie/project-overlay/tech-packs/) bleiben unberuehrt.
    """
    out: list[str] = []
    for kind in ("role-packs", "tech-packs"):
        base = os.path.join(HERE, "framework", kind)
        if not os.path.isdir(base):
            continue
        for pack in sorted(os.listdir(base)):
            src_skills = os.path.join(base, pack, "skills")
            if os.path.isdir(src_skills):
                for skill in sorted(os.listdir(src_skills)):
                    if not os.path.isdir(os.path.join(src_skills, skill)):
                        continue
                    # Nur wenn im Ziel aktiviert
                    if not os.path.isdir(os.path.join(root, *man["skills_dir"].split("/"), skill)):
                        continue
                    for dirpath, dirnames, filenames in os.walk(os.path.join(src_skills, skill)):
                        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
                        for fn in sorted(filenames):
                            src = os.path.join(dirpath, fn)
                            innen = os.path.relpath(src, os.path.join(src_skills, skill))
                            out.append((os.path.relpath(src, HERE).replace(os.sep, "/"),
                                        f"{man['skills_dir']}/{skill}/{innen}".replace(os.sep, "/")))
            src_runtime = os.path.join(base, pack, "runtime")
            if os.path.isdir(src_runtime):
                for fn in sorted(os.listdir(src_runtime)):
                    if not fn.endswith(".md"):
                        continue
                    # Nur wenn im Ziel aktiviert
                    if not os.path.exists(os.path.join(root, *man["pack_runtime_dir"].split("/"), fn)):
                        continue
                    src = os.path.join(src_runtime, fn)
                    out.append((os.path.relpath(src, HERE).replace(os.sep, "/"),
                                f"{man['pack_runtime_dir']}/{fn}"))
    return out


def seed_relpaths(template: str, man: dict) -> list[str]:
    out: list[str] = []
    for rel in man["seed_paths"]:
        out.extend(iter_files(template, rel))
    return out


# Die Platzhalteraufloesung liegt in clientmap, weil der Validator sie ebenfalls braucht.
resolve_placeholders = clientmap.resolve_placeholders


# Frontmatter-Felder eines Skills, die eine Zusage tragen. Sie duerfen beim Rendern
# nicht einfach entfallen: Wer sie verwirft, verwirft eine Schutzaussage, und genau
# dieser Befundtyp zieht sich durch dieses Projekt - AP2-CC-01 fuer 'triggers', B01 fuer
# 'permissions'. Ein Pack darf ein solches Feld nur dann in drop_fields fuehren, wenn es
# den Ersatz benennt: entweder als Abbildung auf ein eigenes Feld oder als
# ausdruecklichen Begleitsatz, dass es keinen gibt und was stattdessen traegt.
#
# 'triggers' hat seit AP2-CC-01 eine Abbildung (model_invocation_field). 'permissions'
# hatte keine. Gemessen am 2026-09-12: 'allowed-tools' ist bei claude-code eine
# Vorabfreigabe und keine Beschraenkung (B01,
# tests/protocols/2026-09-12-B01-allowed-tools.md) - und das Feld 'permissions', das die
# Beschraenkung wirklich trug, stand in drop_fields. Die Zusage fiel damit doppelt aus,
# und beides war fuer sich genommen dokumentiert. Der Ersatz ist die globale
# Berechtigungsschicht samt Schutz-Hook; das ist weniger als eine Beschraenkung je Skill,
# und es gehoert hingeschrieben statt verschwiegen (CR-2026-050, D-50).
#
# Die Bauform ist dieselbe wie bei hook_tools_absent aus 0.30.0: Eine Abwesenheit wird
# deklariert, nie erraten.
ZUSAGENTRAGENDE_SKILLFELDER = {
    "permissions": "skill_permissions_ersatz",
    "triggers": "model_invocation_field",
}


# Welchen Eimer in hook_tools ein Verb der Quelle trifft, sagt clientmap.VERB_BRUECKE.
# Die Werkzeugnamen kommen aus hook_tools und NICHT aus skill_frontmatter.tool_names:
# Das fuehrt fuer 'edit' nur Edit und Write, hook_tools.write fuehrt zusaetzlich
# NotebookEdit. Fuer eine Vorabfreigabe ist der Unterschied harmlos, fuer eine SPERRE
# ist er eine Luecke - und eine Luecke in der Liste ist ausnutzbar (CR-2026-057 E2,
# D-28). Seit 0.40.0 steht die Bruecke an EINER Stelle: Bis dahin fuehrte sie hier
# 'edit', 'write', 'exec', 'read' und 'search' - drei Verben des Vokabulars der Quelle
# und zwei der Durchsetzungsschicht - und kannte 'grep' und 'glob' NICHT, obwohl jede
# der vierzehn Quellen sie im Nachbarfeld desselben Frontmatters fuehrt. Ein
# 'deny: glob' erzeugte deshalb lautlos keine Sperre (D-78, D-79).


def _deny_der_quelle(fm: str) -> list[str]:
    """Die Eintraege unter permissions.deny, in der Reihenfolge der Quelle.

    Gelesen wird nur der deny-Block unterhalb von permissions. Der allow-Block bleibt
    ungelesen und wird nicht abgebildet: 'allowed-tools' ist bei den Clients dieses
    Projekts eine Vorabfreigabe und keine Zusage (B01, CR-2026-057 E4).
    """
    m = re.search(r"^permissions:[ \t]*\n((?:[ \t]+\S.*\n)+)", fm, re.M)
    if not m:
        return []
    block = m.group(1)
    m2 = re.search(r"^([ \t]+)deny:[ \t]*\n((?:[ \t]+-[ \t]+.*\n)+)", block, re.M)
    if not m2:
        return []
    return [z.strip().lstrip("-").strip() for z in m2.group(2).splitlines() if z.strip()]


def deny_abbilden(fm: str, man: dict) -> list[str]:
    """Die Werkzeugnamen, die dieser Client fuer permissions.deny sperren kann.

    Zwei Bauformen stehen in der Quelle, und nur eine ist abbildbar:

      - GROBE VERBEN ('edit', 'exec') werden ueber hook_tools auf Werkzeugnamen
        abgebildet. Sieben der zwoelf Quellskills tragen ausschliesslich diese Form.
      - BEFEHLSGENAUE EINTRAEGE ('Exec(git push)') werden NICHT abgebildet. Gemessen am
        2026-09-13: Ein disallowed-tools-Eintrag mit Klammer laesst den Befehl LAUTLOS
        durchlaufen - keine Verweigerung, keine Fehlermeldung. Wer ihn schreibt, hat gar
        keine Schranke, nicht bloss eine groebere. Das ganze Werkzeug zu sperren waere
        strenger als gemeint und machte die allow-Eintraege derselben Skills wirkungslos.
        Die Nicht-Abbildung ist im Manifest deklariert, nicht verschwiegen
        (skill_deny_unmapped, CR-2026-057 E3; Bauart wie hook_tools_absent, D-47).

    Ein Verb AUSSERHALB des Vokabulars bricht seit 0.40.0 ab, statt lautlos
    auszufallen (D-79). Bis dahin kannte die Bruecke 'grep' und 'glob' nicht - die
    beiden meistgenannten Verben des Vokabulars, vierzehn Fundstellen je im
    Nachbarfeld desselben Frontmatters -, und ein 'deny: glob' erzeugte gar keine
    Sperre: keine Verweigerung, keine Meldung, der Validator 0 Fehler. Gemessen am
    2026-09-13 (tests/protocols/2026-09-13-gegenpruefung-werkzeugabbildung.md, M6).
    """
    eimer = man.get("hook_tools") or {}
    ziel: list[str] = []
    for eintrag in _deny_der_quelle(fm):
        if "(" in eintrag:
            continue  # befehlsgenau - nicht ausdrueckbar, siehe Docstring
        verb = eintrag.strip().lower()
        if verb not in clientmap.VERB_BRUECKE:
            raise clientmap.AbbildungsFehler(
                f"{man.get('client', '?')}: permissions.deny nennt das Verb "
                f"'{verb}', das Vokabular des Frontmatters kennt nur "
                f"{list(clientmap.FRONTMATTER_VERBEN)}. Bis 0.39.0 fiel ein solcher "
                f"Eintrag LAUTLOS aus: Der Skill trug eine Sperre im Quelltext und "
                f"keine in der installierten Fassung (D-79)")
        name = clientmap.VERB_BRUECKE[verb]
        for w in eimer.get(name, []):
            if w not in ziel:
                ziel.append(w)
    return ziel


def _zusagenfelder_pruefen(fm: str, fmt: dict, man: dict) -> None:
    """Bricht ab, wenn ein zusagentragendes Feld ohne benannten Ersatz entfiele.

    Geprueft wird nur, was die Quelle wirklich fuehrt: Ein Pack, dessen Skills das Feld
    gar nicht tragen, wird nicht zur Erklaerung von etwas gezwungen, das es nicht gibt.
    """
    entfallend = set(fmt.get("drop_fields", []))
    if fmt.get("tools_format") == "csv":
        entfallend.add("allowed-tools")
    for feld, ersatzfeld in sorted(ZUSAGENTRAGENDE_SKILLFELDER.items()):
        if feld not in entfallend:
            continue
        if not re.search(rf"^{feld}:", fm, re.M):
            continue
        if str(fmt.get(ersatzfeld) or "").strip():
            continue
        raise clientmap.AbbildungsFehler(
            f"{man.get('client', '?')}: Das Skill-Frontmatter-Feld '{feld}' traegt eine "
            f"Zusage und steht in drop_fields - es entfiele ersatzlos. Das Pack MUSS in "
            f"skill_frontmatter.{ersatzfeld} benennen, was an seine Stelle tritt, oder "
            f"ausdruecklich festhalten, dass es keinen Ersatz gibt und was stattdessen "
            f"traegt (D-18, D-50). Ein folgenloses Verwerfen ist der Befund AP2-CC-01"
        )


def render_skill_frontmatter(text: str, man: dict) -> str:
    """Bringt das Frontmatter eines Skills in die Form, die dieser Client erwartet.

    Quellformat ist die reichere Listenform: allowed-tools als Liste, dazu permissions
    und triggers. Ein Client, der nur eine kommagetrennte Werkzeugliste kennt, bekommt
    sie umgeformt; Felder, die er nicht kennt, entfallen (K-18: Frontmatter nur mit
    dokumentierten Feldern).

    `triggers` faellt dabei nicht ersatzlos: Nennt das Manifest ein
    `model_invocation_field`, wird die Aussage "dieser Skill ist nicht modellgetriggert"
    in das Feld dieses Clients uebersetzt. Ohne diese Abbildung verfiel die Zusage S4 beim
    Rendern - der Validator erzwang `triggers: [user]` in der Quelle, und die installierte
    Fassung trug nichts davon (AP2-CC-01, D-26).

    Seit 0.31.0 gilt das fuer **jedes** zusagentragende Feld: Steht es in drop_fields und
    fuehrt die Quelle es, muss das Pack den Ersatz benennen - sonst scheitert die
    Installation. Das Feld `permissions` fiel bis dahin genau so weg, wie `triggers` es
    vor AP2-CC-01 tat: im Manifest deklariert, in der Wirkung unbemerkt (B01, D-50).
    """
    fmt = man.get("skill_frontmatter", {})
    if not text.startswith("---\n") or "\n---\n" not in text:
        return text
    kopf, rumpf = text.split("\n---\n", 1)
    fm = kopf[4:].rstrip("\n") + "\n"

    # Vor jeder Umformung: Was entfiele hier, ohne dass ein Ersatz benannt ist?
    _zusagenfelder_pruefen(fm, fmt, man)

    # Vor dem Verwerfen lesen: die Quelle nennt triggers als Liste.
    # Dasselbe gilt seit 0.35.0 fuer permissions.deny - auch das ist ein zusagentragendes
    # Feld, und auch es stand bis dahin in drop_fields ohne Abbildung (CR-2026-057, D-65).
    deny_feld = fmt.get("skill_deny_field")
    verbotene = deny_abbilden(fm, man) if deny_feld else []
    feld = fmt.get("model_invocation_field")
    nur_nutzer = False
    if feld:
        m = re.search(r"^triggers:[ \t]*\n((?:[ \t]+-[ \t]+\S+[ \t]*\n)+)", fm, re.M)
        ausloeser = [x.strip("- \t") for x in m.group(1).strip().split("\n")] if m else []
        nur_nutzer = bool(ausloeser) and "model" not in ausloeser

    m = re.search(r"^allowed-tools:[ \t]*\n((?:[ \t]+-[ \t]+\S+[ \t]*\n)+)", fm, re.M)
    werkzeuge = [x.strip("- \t") for x in m.group(1).strip().split("\n")] if m else []
    # Die Verben werden in BEIDEN Zweigen geprueft UND in beiden umgeschrieben. Bis
    # 0.42.0 liess der Listen-Zweig das Feld unberuehrt, waehrend der Agenten-Renderer
    # daneben immer umschrieb - dieselbe Abbildung desselben Manifests mit zwei
    # Ergebnissen. Aufgefallen ist es am 2026-09-14, als devin-desktop seine gemessene
    # Abbildung bekam: Das Agentenprofil trug danach find_file_by_name, die Skilldatei
    # weiter glob - also weiter einen Namen, den dieser Client nicht fuehrt
    # (CR-2026-065, D-87). Ein Schreibfehler im Frontmatter faellt weiterhin beim
    # Installieren auf und nicht erst im uebernehmenden Projekt (D-78).
    ziel: list[str] = []
    for w in werkzeuge:
        for y in clientmap.frontmatter_werkzeuge(man, "skill_frontmatter", w):
            if y not in ziel:
                ziel.append(y)

    if fmt.get("tools_format") == "csv":
        for f in ["allowed-tools"] + list(fmt.get("drop_fields", [])):
            fm = re.sub(rf"^{f}:.*\n(?:[ \t]+\S.*\n)*", "", fm, flags=re.M)
        if ziel:
            fm = fm.rstrip("\n") + f"\nallowed-tools: {', '.join(ziel)}\n"
    else:
        for f in fmt.get("drop_fields", []):
            fm = re.sub(rf"^{f}:.*\n(?:[ \t]+\S.*\n)*", "", fm, flags=re.M)
        if ziel:
            # An Ort und Stelle ersetzen, nicht ans Ende haengen: Bei einer
            # Abbildung, die die Namen nicht aendert, bleibt die Datei dann
            # zeichengleich, und der Diff eines Releases zeigt nur, was sich
            # wirklich geaendert hat.
            eintraege = "allowed-tools:\n" + "".join(f"  - {y}\n" for y in ziel)
            fm = re.sub(r"^allowed-tools:[ \t]*\n(?:[ \t]+-[ \t]+\S+[ \t]*\n)+",
                        lambda _m: eintraege, fm, count=1, flags=re.M)

    if nur_nutzer:
        fm = fm.rstrip("\n") + f"\n{feld}: true\n"

    if verbotene:
        fm = fm.rstrip("\n") + f"\n{deny_feld}: {', '.join(verbotene)}\n"

    return "---\n" + fm + "---\n" + rumpf


def _globs_lesen(fm: str) -> list[str]:
    """Dateimuster der Quelle - als Liste oder als einzelne Zeichenkette notiert."""
    m = re.search(r"^globs:[ \t]*\n((?:[ \t]+-[ \t]+.*\n)+)", fm, re.M)
    if m:
        return [z.strip().lstrip("-").strip().strip("\"'") for z in m.group(1).splitlines() if z.strip()]
    m = re.search(r"^globs:[ \t]*(\S.*?)[ \t]*$", fm, re.M)
    return [m.group(1).strip().strip("\"'")] if m else []


def ist_regelquelle(src_rel: str) -> bool:
    """Wahr fuer jede Quelle, die als Regeldatei in der Regelablage landet.

    Drei Herkuenfte mit demselben Quellfrontmatter: die Core-Regeltexte, die beiden
    Regelvorlagen und die Laufzeitfassungen aktivierter Role- und Technology Packs.
    Alle drei muessen dieselbe Abbildung durchlaufen - eine Pack-Regel, deren
    Ladebedingung beim Rendern verfaellt, waere derselbe Befund wie AP2-CC-03, nur
    eine Ebene tiefer. Bis 0.14.0 lief nur die erste Herkunft durch render_rule.
    """
    if src_rel.startswith(("framework/runtime/rules/", "templates/rules/")):
        return True
    return bool(re.match(r"framework/(role|tech)-packs/[^/]+/runtime/[^/]+\.md$", src_rel))


def _regel_kommentar(desc: str, hinweis: str, herkunft: str) -> str:
    return ("<!-- Laufzeitregel. Inhaltlich identisch zur Fassung anderer Client Packs;\n"
            "     abweichend ist nur die Ladebedingung.\n"
            f"     Zweck: {desc}\n"
            f"     Ladeverhalten: {hinweis}\n"
            f"     Entsprechung in der Kernquelle: {herkunft}. -->\n\n")


def render_rule(text: str, man: dict) -> str:
    """Bringt einen Regeltext in die Form, die dieser Client erwartet.

    Quellformat ist das YAML-Frontmatter mit `description`, `trigger` und - bei
    `trigger: glob` - `globs`; das ist die reichere Form. Drei Bauarten:

    1. Der Client kennt dieselben Ladetrigger (`devin-desktop`): Quellform ist
       Zielform, es ist nichts zu tun.
    2. Der Client kennt eine **eigene** Bedingungssprache (`rule_triggers` im
       Manifest, bei `claude-code` das Feld `paths` mit Glob-Mustern): Jeder
       Ladetrigger der Quelle wird darauf abgebildet. Ein Trigger ohne Eintrag in
       der Abbildung laesst die Installation scheitern - ersatzloses Verwerfen waere
       ein Verlust der Zusage (D-26, D-27). Felder, die der Client fuer Regeldateien
       nicht dokumentiert, entfallen im Frontmatter (K-18) und stehen im Kommentar.
    3. Der Client kennt keine Ladebedingung (`rule_frontmatter: "comment"`): Aus dem
       Frontmatter wird ein Kommentar, die Datei wirkt erst durch eine Einbindung.
       Kein Pack nutzt diese Bauart derzeit.

    Der Regeltext selbst bleibt in allen drei Faellen identisch.
    """
    bauart = man.get("rule_frontmatter", "yaml")
    trigger_map = man.get("rule_triggers")
    if bauart == "yaml" and not trigger_map:
        return text
    if not text.startswith("---\n") or "\n---\n" not in text:
        return text
    kopf, rumpf = text.split("\n---\n", 1)
    fm = kopf[4:]
    m = re.search(r"^description:\s*(.+)$", fm, re.M)
    desc = m.group(1).strip() if m else ""
    m = re.search(r"^trigger:\s*(\S+)\s*$", fm, re.M)
    trig = m.group(1).strip() if m else ""

    if bauart == "comment":
        # Ohne Ladebedingung wirkt eine Regel nur ueber die Einbindung - und dann
        # ausnahmslos. Fuer eine Regel, die auch in der Quelle always_on ist, aendert
        # das nichts; fuer jede andere ist es eine Verschaerfung, die hier benannt wird.
        hinweis = "Wird über den Import in der Wurzel-Anweisungsdatei immer geladen."
        if trig != "always_on":
            hinweis += (" Bei Clients mit Ladebedingungen lädt diese Datei nur bei Relevanz;"
                        " immer zu laden ist eine Verschärfung, keine Lockerung.")
        return _regel_kommentar(desc, hinweis, f"trigger: {trig or 'unbekannt'}") + rumpf.lstrip("\n")

    # Bauart 2: eigene Bedingungssprache des Clients.
    abbildung = trigger_map.get("map", {})
    if trig not in abbildung:
        raise clientmap.AbbildungsFehler(
            f"{man.get('client', '?')}: Ladetrigger '{trig or '(fehlt)'}' hat keinen Eintrag in "
            f"rule_triggers.map - die Regel liesse sich nur durch Weglassen der Ladebedingung "
            f"abbilden, und das waere ein Verlust der Zusage (D-27). Bekannt: "
            f"{', '.join(sorted(abbildung)) or '(keine)'}")
    eintrag = abbildung[trig] or {}
    feld = eintrag.get("condition")
    herkunft = f"trigger: {trig}"
    kopfzeilen = ""
    # Feste Frontmatter-Felder je Ladetrigger (seit 1.13.0, D-414): Der Client kiro
    # verlangt neben dem Musterfeld den Lademodus als eigenes Feld - ohne
    # "inclusion: fileMatch" laedt eine Datei mit fileMatchPattern IMMER.
    fest = "".join(f"{k}: {v}\n" for k, v in (eintrag.get("fixed") or {}).items())
    if feld:
        quellfeld = eintrag.get("from", "globs")
        if quellfeld != "globs":
            raise clientmap.AbbildungsFehler(
                f"{man.get('client', '?')}/manifest.json: rule_triggers.map['{trig}'].from nennt "
                f"'{quellfeld}'; die Kernquelle fuehrt Dateimuster nur unter 'globs'")
        muster = _globs_lesen(fm)
        if not muster:
            raise clientmap.AbbildungsFehler(
                f"{man.get('client', '?')}: Ladetrigger '{trig}' bildet auf '{feld}' ab, die Quelle "
                f"nennt aber keine Dateimuster - die Ladebedingung waere leer")
        for wert in muster:
            if '"' in wert:
                raise clientmap.AbbildungsFehler(
                    f"{man.get('client', '?')}: Dateimuster '{wert}' enthaelt ein "
                    f"Anfuehrungszeichen und laesst sich nicht als {feld}-Eintrag notieren")
        kopfzeilen = ("---\n" + fest + f"{feld}:\n" + "".join(f'  - "{w}"\n' for w in muster)
                      + "---\n\n")
        hinweis = (f"Lädt, sobald der Client eine Datei liest, die auf eines der Muster in "
                   f"`{feld}` passt.")
        herkunft += f", globs: {', '.join(muster)}"
    elif trig == "always_on":
        hinweis = (f"Wird bei jedem Sitzungsstart geladen – eine Regeldatei ohne `"
                   f"{trigger_map.get('condition_field', 'Bedingungsfeld')}`-Feld lädt unbedingt "
                   f"und braucht keine Einbindung.")
    else:
        hinweis = (f"Wird bei jedem Sitzungsstart geladen. Dieser Client kennt für Regeldateien "
                   f"nur die Bedingung über Dateimuster; gegenüber `{trig}` ist unbedingtes Laden "
                   f"eine Verschärfung, keine Lockerung.")
    if fest and not feld:
        kopfzeilen = "---\n" + fest + "---\n\n"
    # Ein Pack, dessen Client mehr Lademodi kennt, als es nutzt, sagt den Grund selbst
    # (rule_triggers.map[...].hint) - der Standardsatz oben behauptete sonst, der Client
    # kenne nur Dateimuster (D-414).
    hinweis = eintrag.get("hint") or hinweis
    return kopfzeilen + _regel_kommentar(desc, hinweis, herkunft) + rumpf.lstrip("\n")


def render_root_instruction(text: str, man: dict) -> str:
    """Setzt an der Marke RUNTIME_IMPORTS die Einbindungen dieses Clients ein.

    Ein Client, der Regeldateien nicht von sich aus laedt, braucht eine Einbindung in
    der Wurzel-Anweisung; welche das sind, steht im Manifest. Beide ausgelieferten Packs
    laden ihre Regelablage seit 0.15.0 selbst und lassen die Liste leer - dann faellt die
    Marke ersatzlos weg. Die Mechanik bleibt fuer ein kuenftiges Pack erhalten und ist
    damit von keinem Pack mehr erprobt (ROADMAP, "Bewusst offen gelassen").
    """
    marke = "<!-- RUNTIME_IMPORTS -->"
    if marke not in text:
        return text
    imports = man.get("root_instruction_imports", []) or []
    if not imports:
        # Marke samt umgebender Leerzeile entfernen, damit die Datei genauso aussieht
        # wie ohne Marke - sonst meldet --check bei jedem Projekt eine Scheindrift.
        return text.replace(marke + "\n\n", "")
    block = (man.get("root_instruction_imports_intro",
                     "Die folgenden Regeldateien sind Bestandteil dieser Anweisung "
                     "und werden mit ihr geladen:")
             + "\n\n" + "\n".join(imports))
    return text.replace(marke, block)


def render_agent(text: str, man: dict) -> str:
    """Formt das Frontmatter eines Agentenprofils um (Feldname und Werkzeugformat)."""
    fmt = man.get("agent_frontmatter")
    if not fmt or not text.startswith("---\n") or "\n---\n" not in text:
        return text
    kopf, rumpf = text.split("\n---\n", 1)
    fm = kopf[4:].rstrip("\n") + "\n"
    m = re.search(r"^allowed-tools:[ \t]*\n((?:[ \t]+-[ \t]+\S+[ \t]*\n)+)", fm, re.M)
    werkzeuge = [x.strip("- \t") for x in m.group(1).strip().split("\n")] if m else []
    ziel: list[str] = []
    for w in werkzeuge:
        for y in clientmap.frontmatter_werkzeuge(man, "agent_frontmatter", w):
            if y not in ziel:
                ziel.append(y)
    fm = re.sub(r"^allowed-tools:.*\n(?:[ \t]+\S.*\n)*", "", fm, flags=re.M)
    feld = fmt.get("tools_field", "allowed-tools")
    if ziel:
        if fmt.get("tools_format") == "csv":
            fm = fm.rstrip("\n") + f"\n{feld}: {', '.join(ziel)}\n"
        else:
            fm = fm.rstrip("\n") + f"\n{feld}:\n" + "".join(f"  - {t}\n" for t in ziel)
    return "---\n" + fm + "---\n" + rumpf


def render_for_client(text: str, man: dict, src_rel: str, dst_rel: str = "") -> str:
    """Waehlt die Transformation anhand der Quelle und loest danach die Platzhalter auf.

    DAS ZIEL ENTSCHEIDET MIT, SEIT ES EINE QUELLE MIT ZWEI ZIELEN GIBT (CR-2026-133,
    D-346). Bei einem Client, dessen Berechtigungsschicht in zwei Traeger zerfaellt -
    Pfade in der Konfigurationsdatei, Befehle in einer eigenen Regeldatei -, wird
    dieselbe Kernquelle zweimal gerendert. Die Quelle allein traegt die Auskunft
    darueber nicht mehr.
    """
    if src_rel == "framework/runtime/permissions.json":
        policy = clientmap.exec_policy_file(man)
        if policy and dst_rel == resolve_placeholders(policy, man):
            return clientmap.render_exec_policy(text, man)
        if clientmap.permissions_format(man) == "toml":
            return clientmap.render_permissions_toml(text, man)
        if clientmap.permissions_format(man) == "kiro-agent":
            return clientmap.render_permissions_kiro(text, man)
        # Kennt der Client keine eigene Hook-Datei, wandern die Hooks hier mit hinein.
        hooks = (clientmap.load_source(HERE, "hooks.json")
                 if clientmap.hooks_in_permissions(man) else None)
        return clientmap.render_permissions(text, man, hooks)
    if src_rel == "framework/runtime/hooks.json":
        return clientmap.render_hooks(text, man)
    if src_rel == "framework/runtime/client-settings.json":
        # Die Quelle erklaert nur; den Inhalt traegt das Manifest (D-414).
        return clientmap.render_client_settings(man)
    if os.path.basename(src_rel) == "SKILL.md":
        text = render_skill_frontmatter(text, man)
    elif ist_regelquelle(src_rel):
        text = render_rule(text, man)
    elif src_rel == "framework/runtime/root-instruction.md":
        text = render_root_instruction(text, man)
    elif src_rel.startswith("framework/runtime/agents/"):
        text = render_agent(text, man)
    return resolve_placeholders(text, man)


def shared_files(man: dict, schluessel: str) -> list[tuple[str, str]]:
    """(Quelle relativ zu HERE, Ziel relativ zum Projekt) fuer geteilte Kernbestandteile.

    Geteilt heisst: Der Inhalt gehoert dem Framework, nur der Zielpfad - und mitunter die
    Form - haengt vom Client ab. Frueher lagen diese Dateien in jedem root-template
    erneut; identische Dateien mussten doppelt gepflegt werden.

    Das Manifest fuehrt sie unter shared_core (wird bei --update ueberschrieben) und
    shared_seed (nur bei der Erstinstallation angelegt). Ein Eintrag ist
    {"src": <Pfad relativ zu HERE>, "dst": <Zielpfad, darf Laufzeit-Platzhalter enthalten>};
    ist src ein Verzeichnis, wird es rekursiv abgebildet.
    """
    out: list[tuple[str, str]] = []
    for eintrag in man.get(schluessel, []) or []:
        src_rel = eintrag["src"]
        dst_rel = resolve_placeholders(eintrag["dst"], man)
        voll = os.path.join(HERE, *src_rel.split("/"))
        if os.path.isfile(voll):
            out.append((src_rel, dst_rel))
        elif os.path.isdir(voll):
            for dirpath, dirnames, filenames in os.walk(voll):
                dirnames[:] = [d for d in dirnames if d != "__pycache__"]
                for fn in sorted(filenames):
                    src = os.path.join(dirpath, fn)
                    innen = os.path.relpath(src, voll).replace(os.sep, "/")
                    out.append((f"{src_rel}/{innen}", f"{dst_rel}/{innen}"))
    return sorted(out, key=lambda x: x[1])


def framework_skill_files(man: dict) -> list[tuple[str, str]]:
    """(Quelle relativ zu HERE, Ziel relativ zum Projekt) fuer alle Framework-Skills.

    Die Skills liegen seit 0.5.0 einmal unter framework/skills/ und werden bei der
    Installation in die Form des gewaehlten Clients gebracht. Vorher lagen sie je
    Client Pack im root-template - identischer Rumpf, abweichendes Frontmatter,
    doppelte Pflege.
    """
    quelle = os.path.join(HERE, "framework", "skills")
    if not os.path.isdir(quelle):
        return []
    out: list[tuple[str, str]] = []
    for skill in sorted(os.listdir(quelle)):
        if not os.path.isdir(os.path.join(quelle, skill)):
            continue
        if not skill.startswith(man["core_skill_prefix"]):
            continue
        for dirpath, dirnames, filenames in os.walk(os.path.join(quelle, skill)):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            for fn in sorted(filenames):
                src = os.path.join(dirpath, fn)
                innen = os.path.relpath(src, os.path.join(quelle, skill)).replace(os.sep, "/")
                out.append((os.path.relpath(src, HERE).replace(os.sep, "/"),
                            f"{man['skills_dir']}/{skill}/{innen}"))
    return out


def write_rendered(src: str, dst: str, man: dict, dry: bool, dst_rel: str = "") -> None:
    if dry:
        return
    text = render_for_client(read_text(src), man, quell_kennung(src), dst_rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def read_text(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def quell_kennung(src: str) -> str:
    """Pfad der Quelle relativ zum Kern - er entscheidet ueber die Formtransformation."""
    return os.path.relpath(src, HERE).replace(os.sep, "/")


def rendered_matches(src: str, dst: str, man: dict, dst_rel: str = "") -> bool:
    if not os.path.exists(dst):
        return False
    soll = render_for_client(read_text(src), man, quell_kennung(src), dst_rel)
    return read_text(dst) == soll


def copy_file(src: str, dst: str, dry: bool) -> None:
    if dry:
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)


def pruefe_abbildung(root: str, man: dict, muster: dict | None = None) -> None:
    """Rendert jede abzubildende Quelle einmal, bevor die erste Datei geschrieben wird.

    D-26 verlangt, dass die Installation scheitert, wenn eine Aussage der Quelle sich
    nicht abbilden laesst. Ohne diesen Vorlauf scheiterte sie mitten im Schreiben und
    hinterliess ein halb angelegtes Projekt - gescheitert ist das eine, halb gelungen
    das andere. Der Vorlauf kostet einen zweiten Rendervorgang und keine Schreiboperation.

    Mit einem Overlay-Muster laeuft der Fuellschritt hier mit: Ein Muster, dessen Anker
    in einer der drei Saatquellen fehlt, bricht vor dem ersten Schreibvorgang ab
    (MusterFehler) und nicht nach der Haelfte.
    """
    quellen = list(activated_pack_relpaths(root, man))
    quellen += framework_skill_files(man)
    quellen += shared_files(man, "shared_core")
    for src_rel, dst_rel in quellen:
        src = os.path.join(HERE, *src_rel.split("/"))
        render_for_client(read_text(src), man, quell_kennung(src), dst_rel)
    for src_rel, dst_rel in shared_files(man, "shared_seed"):
        render_mit_muster(os.path.join(HERE, *src_rel.split("/")), man, dst_rel, muster)


def ignorierte_kerndateien(root: str) -> list[str]:
    """Die geschriebenen Kerndateien, die das aufnehmende Projekt ignoriert.

    ANLASS, UND ER IST GEMESSEN (`K-117`, CR-2026-133, D-349). Beim Heben auf `1.3.0`
    lagen in einem der beiden aufnehmenden Projekte 525 Kerndateien im Arbeitsbaum und
    483 im Versionierten: Die projekteigene `.gitignore`-Zeile `build/` trifft auch
    `<CORE_DIR>/build/`, und damit die gesamte Quelle des Hauptdokuments.
      ➡️ Ein Kern, der ausgeliefert, aber nicht versioniert wird, ist beim naechsten
         Klonen dieses Projekts unvollstaendig.
    Der Validator sieht es nicht, weil er den ARBEITSBAUM misst; Pruefung 81 sieht es
    nicht, weil sie die Zeilenendeform der VERFOLGTEN Traeger misst - also gerade
    derer, die noch da sind.

    DIES IST EINE AUSKUNFT UND KEINE SCHRANKE, und das ist die Entscheidung
    (D-349, Bauform von D-34): Das `.gitignore` gehoert dem Projekt. Das Framework
    sagt, was es beobachtet, und ueberlaesst dem Projekt, was daraus folgt; der
    Uebernahmeleitfaden nennt die Negativregel.

    Ohne Git - oder ausserhalb eines Repositoriums - gibt die Funktion eine leere
    Liste zurueck. Eine Auskunft, die nicht erhoben werden kann, wird nicht behauptet.

    DIE PFADE GEHEN ALS BYTES MIT NUL-TRENNUNG HIN UND ZURUECK (`-z`, CR-2026-135,
    D-352). Bis 1.4.1 gingen sie mit `text=True` als Zeilen hin: Unter Windows wird
    daraus `\\r\\n`, git bekam jeden Pfad mit angehaengtem `\\r`, verglich ihn so gegen
    die Muster und gab ihn gequotet zurueck. Ein Verzeichnismuster (`build/`) traf
    trotzdem, weil es am Elternverzeichnis greift; ein DATEImuster (`*.md`) traf nie -
    gemessen: git meldet zwei ignorierte Dateien, die Funktion null. Und ohne `-z`
    quotet git jeden Pfad mit Nicht-ASCII-Zeichen (`core.quotePath`); die Ausgabe ist
    dann kein Pfad mehr. `-z` schaltet beides ab.
    """
    kern = os.path.join(root, *clientmap.CORE_REL.split("/"))
    if not os.path.isdir(kern):
        return []
    dateien: list[str] = []
    for dirpath, dirnames, filenames in os.walk(kern):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in filenames:
            rel = os.path.relpath(os.path.join(dirpath, fn), root).replace(os.sep, "/")
            dateien.append(rel)
    if not dateien:
        return []
    try:
        proc = subprocess.run(["git", "-C", root, "check-ignore", "-z", "--stdin"],
                              input=b"\0".join(d.encode("utf-8") for d in dateien) + b"\0",
                              capture_output=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return []
    # Exit 0 = mindestens einer ignoriert, 1 = keiner, alles andere ist kein Ergebnis.
    if proc.returncode not in (0, 1):
        return []
    return sorted(z.decode("utf-8", "replace").replace("\\", "/")
                  for z in proc.stdout.split(b"\0") if z)


# Das Kennzeichen des Framework-Repositoriums (D-351). Der Validator liest dieselbe
# Datei unter demselben Pfad (QUELLREPO_KENNZEICHEN); Sonde D354 haelt beide Stellen
# an einer echten Installation gegeneinander.
QUELLREPO_KENNZEICHEN = ".koolie/QUELLREPOSITORIUM.md"


def belegte_importkanaele(root: str, man: dict) -> list[tuple[str, str]]:
    """Die Importkanaele aus dem Manifest, die auf diesem Arbeitsplatz belegt sind.

    ANLASS, UND ER IST GEMESSEN (K-156, D-411). Bei devin-desktop schaltet die
    Importsteuerung, die fremde Windsurf-Quellen fernhaelt, zugleich die eigene
    Regelablage ab. Das Pack laesst sie deshalb seit 1.12.1 zu - und damit auch eine
    Regel aus dem Benutzerprofil, die in jeder Sitzung laedt (D-290). Das Manifest nennt
    diese Kanaele (import_channels_report); dieses Werkzeug meldet, welche davon belegt
    sind: eine nicht leere Datei, eine vorhandene Datei, ein vorhandenes Verzeichnis.

    DIES IST EINE AUSKUNFT UND KEINE SCHRANKE: Was im Kanal steht, beurteilt der Mensch,
    und die Benutzerkonfiguration des Clients hat ohnehin Vorrang (K-27).
    """
    belegt: list[tuple[str, str]] = []
    for kanal in man.get("import_channels_report") or []:
        rel = kanal.get("path", "")
        if kanal.get("scope") == "user":
            pfad = os.path.expanduser(rel)
        else:
            pfad = os.path.join(root, *rel.split("/"))
        wann = kanal.get("when", "exists")
        if wann == "nonempty":
            treffer = os.path.isfile(pfad) and os.path.getsize(pfad) > 0
        elif wann == "entries":
            # Ein Verzeichnis mit mindestens einem Eintrag - ein leeres legt der
            # Client selbst an und traegt nichts (D-414).
            treffer = os.path.isdir(pfad) and bool(os.listdir(pfad))
        else:
            treffer = os.path.exists(pfad)
        if treffer:
            belegt.append((rel, kanal.get("what", "")))
    return belegt


def traegt_quellrepo_kennzeichen(root: str) -> bool:
    """Liegt im Ziel das Kennzeichen des Framework-Repositoriums?

    ANLASS, UND ER IST GEMESSEN (CR-2026-137, D-354). Das Kennzeichen liegt NEBEN dem
    Kern, und wer ganz `.koolie/` statt nur `.koolie/core/` kopiert, nimmt es mit - aus
    dem Arbeitsbaum des Frameworks ebenso wie aus dem Release-Archiv, denn es ist
    versioniert. Danach haelt der Validator das Projekt fuer das Quellrepositorium:
    Pruefung 79 verlangt die Lizenz in der Projektwurzel, und sobald das Projekt die
    Datei committet, misst Pruefung 81 die Zeilenenden jedes Projekttraegers. Keine der
    Meldungen nennt die Ursache. Aus dem Arbeitsbaum kommt zugleich das Overlay des
    Frameworks mit und ersetzt das des Projekts - still, weil install.py das Overlay
    nie anfasst und es deshalb als unberuehrt meldet.

    DIES IST EINE AUSKUNFT UND KEINE SCHRANKE (D-354, Bauform von D-349). Ein Abbruch
    traefe das Framework-Repositorium selbst, das seine Wurzeldateien mit demselben
    Aufruf erzeugt; kein Merkmal trennt beide Faelle sicher - auch nicht, ob git die
    Datei verfolgt, denn ein Projekt, das die Kopie committet hat, sieht dann genauso
    aus.
    """
    return os.path.isfile(os.path.join(root, *QUELLREPO_KENNZEICHEN.split("/")))


# ---------------------------------------------------------------------------
# Overlay-Muster (--overlay <name>, D-126) und der Fuellschritt (D-353, D-355)
# ---------------------------------------------------------------------------
# ANLASS, UND ER IST GEMESSEN (CR-2026-136, 2.3). Ein Muster, das nur OVERLAY.md
# vorbefuellt, erreicht die Schicht nicht, die sperrt: An einer Wegwerf-Installation
# stand Read(<EXCLUDED_PATHS>) danach woertlich im deny-Korb, und Pruefung 59 enthielt
# sich. Der Fuellschritt schreibt deshalb DREI Traeger aus EINER Quelle - der
# Wertetabelle des Musters -, und zwar genau einmal, bei der Erstinstallation.
#
# ABGRENZUNG ZU D-76. Gelesen wird ein Traeger des KERNS, nicht des Projekts, und
# zugesagt ist der ANFANGSZUSTAND, kein Kanal. --update liest das Muster nie.
#
# DIE GRENZE STEHT IM WERKZEUG, NICHT NUR IM MUSTER (CR-2026-138 E1). Ein Muster darf
# ausschliesslich Platzhalter fuellen, deren Wert in einem deny-Eintrag steht - es
# SPERRT, es gibt nichts frei. Fuehrt eine Wertedatei einen anderen Platzhalter, bricht
# die Installation ab, bevor die erste Datei geschrieben ist.
MUSTER_ABLAGE = os.path.join(HERE, "framework", "overlay-patterns")
MUSTER_PLATZHALTER = ("<CI_CONFIG_PATHS>", "<QUALITY_GATE_CONFIG_PATHS>", "<EXCLUDED_PATHS>")
MUSTER_QUELLE_RECHTE = "framework/runtime/permissions.json"
MUSTER_QUELLE_LAUFZEIT = "framework/runtime/rules/20-project-overlay.md"
MUSTER_QUELLE_OVERLAY = "templates/project-overlay/OVERLAY.md"
MUSTER_WERTEABSCHNITT = "Die Werte"
# DER ZWEITE GEGENSTAND: DOKUMENTE (CR-2026-139, D-359, D-360). Ein Muster darf neben
# den Werten Dokumente mitliefern - allgemeine Praktiken, die auf jedes Projekt passen.
# Sie liegen unter <muster>/documents/<typ>/, werden bei der Erstinstallation nach
# .koolie/project-overlay/documents/<typ>/ geschrieben und im Manifest registriert:
# K1, Status entwurf, Laden on-demand. Sie geben nichts frei - die Liste der
# freigegebenen K1-Dokumente in der Laufzeitfassung bleibt ein Ausfuellschlitz, bis
# der Overlay Owner sie fuellt.
#
# EIN REGISTER, NICHT ZWEI. Welche Dokumente es gibt, sagt die Ablage; die Tabelle im
# Abschnitt "Die Dokumente" der Musterdatei beschreibt sie, und install.py haelt beide
# gegeneinander. Ein Typ ist gueltig, wenn die Dokumentablage der Overlay-Vorlage ein
# Verzeichnis dieses Namens fuehrt - dieselbe Ablage, in die geschrieben wird.
MUSTER_DOKUMENTABSCHNITT = "Die Dokumente"
MUSTER_DOKUMENTVERMERK = "Muster – vom Overlay Owner zu prüfen und anzupassen."
MUSTER_QUELLE_MANIFEST = "templates/project-overlay/overlay-manifest.yaml"
MUSTER_DOKUMENTZIEL = ".koolie/project-overlay/documents"
MUSTER_TYPABLAGE = os.path.join(HERE, "templates", "project-overlay", "documents")


class MusterFehler(Exception):
    """Ein Muster laesst sich nicht vollstaendig anwenden - die Installation bricht ab."""


def verfuegbare_muster() -> list[str]:
    """Die Namen der mitgelieferten Overlay-Muster (Dateiname ohne .md)."""
    if not os.path.isdir(MUSTER_ABLAGE):
        return []
    return sorted(fn[:-3] for fn in os.listdir(MUSTER_ABLAGE)
                  if fn.endswith(".md") and fn != "README.md")


def muster_laden(name: str) -> dict:
    """Liest Name, Version und Wertetabelle eines Musters und prueft seine Grenze.

    Die Werte stehen je in einer Codespanne der Spalte "Werte"; die Zeile wird ueber
    die Platzhalterzelle gefunden, nie ueber eine Spaltennummer - dieselbe Lesart wie
    Pruefung 42 und 59.
    """
    if name not in verfuegbare_muster():
        raise MusterFehler(f"Unbekanntes Overlay-Muster '{name}'. Verfuegbar: "
                           f"{', '.join(verfuegbare_muster()) or 'keines'}")
    pfad = os.path.join(MUSTER_ABLAGE, name + ".md")
    version = None
    werte: dict[str, list[str]] = {}
    abschnitt = ""
    for zeile in read_text(pfad).split("\n"):
        if zeile.startswith("## "):
            abschnitt = zeile[3:].strip()
            continue
        zellen = [z.strip() for z in zeile.strip().strip("|").split("|")]
        if zellen and zellen[0] == "Version" and version is None and len(zellen) >= 2:
            version = zellen[1].strip("`")
            continue
        # Nur die Wertetabelle zaehlt. Eine andere Tabelle derselben Datei darf einen
        # Platzhalter in der ersten Spalte nennen - etwa den Traeger <PERMISSIONS_FILE> -,
        # ohne dass er zum Musterwert wird (gefunden beim ersten Lauf, CR-2026-138).
        if abschnitt != MUSTER_WERTEABSCHNITT:
            continue
        if len(zellen) < 2:
            continue
        m = re.fullmatch(r"`(<[A-Z_]+>)`", zellen[0])
        if not m:
            continue
        platzhalter = m.group(1)
        if platzhalter not in MUSTER_PLATZHALTER:
            raise MusterFehler(
                f"Das Muster '{name}' fuellt {platzhalter}. Ein Muster darf nur sperren: "
                f"zulaessig sind {', '.join(MUSTER_PLATZHALTER)} (CR-2026-138 E1)")
        liste = re.findall(r"`([^`]+)`", zellen[1])
        if not liste or any("<" in w or ">" in w for w in liste):
            raise MusterFehler(f"Das Muster '{name}' fuehrt fuer {platzhalter} keinen "
                               f"gueltigen Wert: {zellen[1]}")
        werte[platzhalter] = liste
    if not werte or not version:
        raise MusterFehler(f"Das Muster '{name}' traegt keine Version oder keine Werte "
                           f"(Abschnitt '## {MUSTER_WERTEABSCHNITT}')")
    return {"name": name, "version": version, "werte": werte,
            "dokumente": muster_dokumente(name)}


def muster_dokumente(name: str) -> list[dict]:
    """Die Dokumente eines Musters, gegen die Beschreibung in seiner Musterdatei gehalten.

    Jedes Dokument liegt unter <muster>/documents/<typ>/<datei>.md, traegt als erste
    Zeile eine Ueberschrift der Ebene 1 (sie wird der Titel im Manifest) und den
    Vorschlagsvermerk. Die Tabelle im Abschnitt "Die Dokumente" nennt in ihrer ersten
    Spalte genau die Typen, fuer die ein Dokument da ist - nicht mehr und nicht weniger.
    Jede Abweichung bricht ab, bevor die erste Datei geschrieben ist.
    """
    ablage = os.path.join(MUSTER_ABLAGE, name, "documents")
    beschrieben: set[str] = set()
    abschnitt = ""
    for zeile in read_text(os.path.join(MUSTER_ABLAGE, name + ".md")).split("\n"):
        # Jede Ueberschrift beendet den Abschnitt, auch eine der Ebene 3: Darunter steht
        # eine Feldtabelle (`status`, `load`), deren erste Spalte sonst als Typ gelaese.
        if zeile.startswith("#"):
            abschnitt = zeile.lstrip("#").strip()
            continue
        if abschnitt != MUSTER_DOKUMENTABSCHNITT:
            continue
        zellen = [z.strip() for z in zeile.strip().strip("|").split("|")]
        m = re.fullmatch(r"`([a-z][a-z-]*)`", zellen[0]) if zellen else None
        if m:
            beschrieben.add(m.group(1))
    dokumente: list[dict] = []
    if os.path.isdir(ablage):
        for typ in sorted(os.listdir(ablage)):
            verz = os.path.join(ablage, typ)
            if not os.path.isdir(verz):
                continue
            if not os.path.isdir(os.path.join(MUSTER_TYPABLAGE, typ)):
                raise MusterFehler(f"Das Muster '{name}' liefert ein Dokument vom Typ "
                                   f"'{typ}', den die Dokumentablage der Overlay-Vorlage "
                                   f"nicht kennt")
            for fn in sorted(os.listdir(verz)):
                if not fn.endswith(".md"):
                    continue
                text = read_text(os.path.join(verz, fn))
                kopf = text.split("\n", 1)[0].strip()
                if not kopf.startswith("# ") or MUSTER_DOKUMENTVERMERK not in text:
                    raise MusterFehler(f"Das Muster '{name}': {typ}/{fn} traegt keine "
                                       f"Ueberschrift der Ebene 1 in der ersten Zeile oder "
                                       f"nicht den Vermerk '{MUSTER_DOKUMENTVERMERK}'")
                dokumente.append({"typ": typ, "datei": fn, "titel": kopf[2:].strip(),
                                  "quelle": os.path.join(verz, fn)})
    geliefert = {d["typ"] for d in dokumente}
    if geliefert != beschrieben:
        raise MusterFehler(
            f"Das Muster '{name}': Ablage und Beschreibung stimmen nicht ueberein - "
            f"nur abgelegt: {', '.join(sorted(geliefert - beschrieben)) or 'nichts'}; "
            f"nur beschrieben: {', '.join(sorted(beschrieben - geliefert)) or 'nichts'} "
            f"(Abschnitt '## {MUSTER_DOKUMENTABSCHNITT}')")
    return dokumente


def muster_manifest(text: str, muster: dict) -> str:
    """Ersetzt die Beispieleintraege der Manifestvorlage durch die Dokumente des Musters.

    Die Vorlage fuehrt unter `documents:` drei Beispiele mit Ausfuellschlitzen. Neben
    echten Eintraegen waeren sie ein Register mit Eintraegen, die auf nichts zeigen;
    sie werden deshalb ersetzt, nicht ergaenzt (D-360).
    """
    if not muster["dokumente"]:
        return text
    anker = "\ndocuments:\n"
    if text.count(anker) != 1:
        raise MusterFehler("overlay-manifest.yaml: der Schluessel 'documents:' steht nicht "
                           "genau einmal am Zeilenanfang - die Eintraege des Musters haetten "
                           "keinen Ort")
    eintraege = []
    for nr, dok in enumerate(muster["dokumente"], start=1):
        titel = dok["titel"].replace('"', "'")
        eintraege.append(
            f'  - id: "DOC-{nr:03d}"\n'
            f'    type: "{dok["typ"]}"\n'
            f'    title: "{titel}"\n'
            f'    path: "{MUSTER_DOKUMENTZIEL}/{dok["typ"]}/{dok["datei"]}"\n'
            f'    context_class: "K1"\n'
            f'    status: "entwurf"\n'
            f'    load: "on-demand"\n'
            f'    approved_by: "<APPROVAL_ROLE>"\n'
            f'    approved_on: "<TBD: Datum der Freigabe durch den Overlay Owner>"\n'
            f'    sanitization: "nicht erforderlich"\n'
            f'    notes: "Aus dem Overlay-Muster {muster["name"]} {muster["version"]} - vom '
            f'Overlay Owner zu pruefen und anzupassen; erst nach Freigabe in der '
            f'Laufzeitfassung als K1-Dokument fuehren"\n')
    return text[:text.index(anker)] + anker + "\n".join(eintraege)


def muster_berechtigungen(quelltext: str, muster: dict) -> str:
    """Die Kernquelle der Berechtigungen, jeder Schlitz des Musters je Wert entfaltet.

    Entfaltet wird VOR dem Rendern, also in der neutralen Regelmenge - damit gilt fuer
    jeden Wert dieselbe Abbildung auf das Client Pack wie fuer jede andere Regel, und
    ein Pack, das eine Musterform nicht abbilden kann, sagt es auf demselben Weg.
    """
    quelle = json.loads(quelltext)
    gefunden: set[str] = set()
    for korb in ("deny", "ask", "allow"):
        neu = []
        for regel in quelle.get(korb, []):
            platzhalter = regel.get("pattern")
            if platzhalter in muster["werte"]:
                if korb != "deny":
                    raise MusterFehler(f"permissions.json fuehrt {platzhalter} im {korb}-Korb;"
                                       f" ein Musterwert dort waere eine Freigabe")
                gefunden.add(platzhalter)
                for wert in muster["werte"][platzhalter]:
                    neu.append({k: (wert if k == "pattern" else v) for k, v in regel.items()})
            else:
                neu.append(regel)
        quelle[korb] = neu
    fehlt = [p for p in muster["werte"] if p not in gefunden]
    if fehlt:
        raise MusterFehler(f"permissions.json fuehrt keinen Schlitz fuer {', '.join(fehlt)}")
    return json.dumps(quelle, indent=2, ensure_ascii=False) + "\n"


def _werte_spannen(werte: list[str]) -> str:
    return ", ".join(f"`{w}`" for w in werte)


def muster_laufzeitfassung(text: str, muster: dict) -> str:
    """Setzt den Wert hinter jeden gebundenen Platzhalter der Laufzeitfassung.

    Die Bindung bleibt stehen (D-160): ersetzt wird der Ausfuellschlitz HINTER
    die Klammer mit dem Platzhalter in Codespanne, nicht der Platzhalter selbst. Die Laufzeitfassung fuehrt von den
    drei Platzhaltern nur <EXCLUDED_PATHS>; die beiden anderen stehen nur in OVERLAY.md
    und der Berechtigungsdatei.
    """
    for platzhalter, werte in muster["werte"].items():
        anker = f"(`{platzhalter}`): "
        if anker not in text:
            if platzhalter == "<EXCLUDED_PATHS>":
                raise MusterFehler(f"20-project-overlay.md bindet {platzhalter} nicht mehr "
                                   f"in der Form {anker.strip()} - der Wert kaeme nicht an")
            continue
        text, n = re.subn(re.escape(anker) + r"`<TBD[^`]*>`",
                          lambda _m: anker + _werte_spannen(werte), text, count=1)
        if n != 1:
            raise MusterFehler(f"20-project-overlay.md: hinter {anker.strip()} steht kein "
                               f"Ausfuellschlitz")
    return text


def muster_overlay(text: str, muster: dict) -> str:
    """Fuellt die Spalte "Wert" der drei Zeilen in Abschnitt 4 und vermerkt das Muster."""
    zeilen = text.split("\n")
    offen = set(muster["werte"])
    for i, zeile in enumerate(zeilen):
        zellen = zeile.split("|")
        for j, zelle in enumerate(zellen[:-1]):
            platzhalter = zelle.strip().strip("`")
            if platzhalter in offen and zelle.strip() == f"`{platzhalter}`" \
                    and zellen[j + 1].strip().startswith("`<TBD"):
                zellen[j + 1] = f" {_werte_spannen(muster['werte'][platzhalter])} "
                zeilen[i] = "|".join(zellen)
                offen.discard(platzhalter)
                break
    if offen:
        raise MusterFehler(f"OVERLAY.md: keine Wertzeile mit Ausfuellschlitz fuer "
                           f"{', '.join(sorted(offen))}")
    text = "\n".join(zeilen)
    alt = "| Overlay angelegt |"
    if alt not in text:
        raise MusterFehler("OVERLAY.md: die Zeile 'Overlay angelegt' im Aenderungsverlauf "
                           "fehlt - der Vermerk des Musters haette keinen Ort")
    dokumente = ""
    if muster["dokumente"]:
        dokumente = (f"; {len(muster['dokumente'])} Musterdokumente unter `documents/` im "
                     f"Manifest registriert (Status `entwurf`, erst nach Prüfung und "
                     f"Freigabe durch den Overlay Owner verbindlich)")
    return text.replace(alt, f"| Overlay angelegt aus dem Muster `{muster['name']}` "
                             f"`{muster['version']}` – vorbefüllt: "
                             f"{', '.join(f'`{p}`' for p in muster['werte'])}{dokumente} |", 1)


def render_mit_muster(src: str, man: dict, dst_rel: str, muster: dict | None) -> str:
    """render_for_client, dazu der Fuellschritt fuer die drei Saattraeger."""
    kennung = quell_kennung(src)
    quelle = read_text(src)
    if muster and kennung == MUSTER_QUELLE_RECHTE:
        quelle = muster_berechtigungen(quelle, muster)
    text = render_for_client(quelle, man, kennung, dst_rel)
    if muster and kennung == MUSTER_QUELLE_LAUFZEIT:
        text = muster_laufzeitfassung(text, muster)
    if muster and kennung == MUSTER_QUELLE_OVERLAY:
        text = muster_overlay(text, muster)
    if muster and kennung == MUSTER_QUELLE_MANIFEST:
        text = muster_manifest(text, muster)
    return text


def muster_dokumentziele(muster: dict | None) -> list[tuple[str, str]]:
    """(Quelle absolut, Ziel relativ zum Projekt) fuer die Dokumente eines Musters."""
    if not muster:
        return []
    return [(d["quelle"], f"{MUSTER_DOKUMENTZIEL}/{d['typ']}/{d['datei']}")
            for d in muster["dokumente"]]


def run(root: str, template: str, man: dict, mode: str, dry: bool,
        muster: dict | None = None) -> Report:
    rep = Report()
    pruefe_abbildung(root, man, muster)

    for rel in core_relpaths(template, man):
        src = os.path.join(template, rel)
        dst = os.path.join(root, rel)
        if not os.path.exists(dst):
            if mode == "check":
                rep.missing.append(rel)
            else:
                copy_file(src, dst, dry)
                rep.created.append(rel)
            continue
        if filecmp.cmp(src, dst, shallow=False):
            rep.unchanged.append(rel)
        elif mode == "check":
            rep.drifted.append(rel)
        elif mode in ("install", "update"):
            copy_file(src, dst, dry)
            rep.updated.append(rel)

    # Aktivierte Pack-Bestandteile: Quelle liegt im Pack, Ziel in der Laufzeitschicht.
    # Werden nie neu angelegt - die Aktivierung bleibt Projektentscheidung -, aber
    # aktualisiert, sobald sie vorhanden sind.
    for src_rel, dst_rel in activated_pack_relpaths(root, man):
        src = os.path.join(HERE, src_rel)
        dst = os.path.join(root, dst_rel)
        if not os.path.exists(dst):
            continue
        if rendered_matches(src, dst, man, dst_rel):
            rep.unchanged.append(dst_rel)
        elif mode == "check":
            rep.drifted.append(f"{dst_rel}  (Pack-Quelle: {src_rel})")
        else:
            write_rendered(src, dst, man, dry, dst_rel)
            rep.updated.append(f"{dst_rel}  (aus dem Pack aktualisiert)")

    # Framework-Skills: eine Quelle, je Client gerendert.
    for src_rel, dst_rel in framework_skill_files(man):
        src = os.path.join(HERE, src_rel)
        dst = os.path.join(root, dst_rel)
        if not os.path.exists(dst):
            if mode == "check":
                rep.missing.append(dst_rel)
            else:
                write_rendered(src, dst, man, dry, dst_rel)
                rep.created.append(dst_rel)
        elif rendered_matches(src, dst, man, dst_rel):
            rep.unchanged.append(dst_rel)
        elif mode == "check":
            rep.drifted.append(f"{dst_rel}  (Quelle: {src_rel})")
        else:
            write_rendered(src, dst, man, dry, dst_rel)
            rep.updated.append(dst_rel)

    # Geteilte Core-Bestandteile aus dem Kern (Vorlagen, spaeter weitere).
    for src_rel, dst_rel in shared_files(man, "shared_core"):
        src = os.path.join(HERE, *src_rel.split("/"))
        dst = os.path.join(root, *dst_rel.split("/"))
        if not os.path.exists(dst):
            if mode == "check":
                rep.missing.append(dst_rel)
            else:
                write_rendered(src, dst, man, dry, dst_rel)
                rep.created.append(dst_rel)
        elif rendered_matches(src, dst, man, dst_rel):
            rep.unchanged.append(dst_rel)
        elif mode == "check":
            rep.drifted.append(f"{dst_rel}  (Quelle: {src_rel})")
        else:
            write_rendered(src, dst, man, dry, dst_rel)
            rep.updated.append(dst_rel)

    for rel in seed_relpaths(template, man):
        src = os.path.join(template, rel)
        dst = os.path.join(root, rel)
        if os.path.exists(dst):
            rep.kept.append(rel)
        elif mode == "check":
            rep.missing.append(rel)
        else:
            copy_file(src, dst, dry)
            rep.created.append(rel)

    # Geteilte Saat aus dem Kern: einmal angelegt, danach Eigentum des Projekts. Mit
    # einem Overlay-Muster fuellt dieser Schritt die Schlitze des Musters (D-355).
    for src_rel, dst_rel in shared_files(man, "shared_seed"):
        src = os.path.join(HERE, *src_rel.split("/"))
        dst = os.path.join(root, *dst_rel.split("/"))
        if os.path.exists(dst):
            rep.kept.append(dst_rel)
        elif mode == "check":
            rep.missing.append(dst_rel)
        else:
            if not dry:
                text = render_mit_muster(src, man, dst_rel, muster)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                with open(dst, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(text)
            rep.created.append(dst_rel)

    # Die Dokumente eines Musters (D-359): nur bei der Erstinstallation, nie ueber
    # ein vorhandenes Dokument, danach Eigentum des Projekts wie jede Saat.
    if mode == "install":
        for src, dst_rel in muster_dokumentziele(muster):
            dst = os.path.join(root, *dst_rel.split("/"))
            if os.path.exists(dst):
                rep.kept.append(dst_rel)
                continue
            if not dry:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                with open(dst, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(read_text(src))
            rep.created.append(dst_rel)

    return rep


def skill_herkunft() -> dict[str, str]:
    """Welcher Teil des Kerns liefert welchen Skill.

    Grundlage von --list-skills. Der Kern liefert unter framework/skills/, die Rollen- und
    Technologiepacks unter framework/<art>/<pack>/skills/. Was in einer Installation liegt
    und in keiner dieser Quellen vorkommt, stammt aus dem Projekt.
    """
    herkunft: dict[str, str] = {}
    kern = os.path.join(HERE, "framework", "skills")
    if os.path.isdir(kern):
        for name in sorted(os.listdir(kern)):
            if os.path.isdir(os.path.join(kern, name)):
                herkunft[name] = "Kern"
    for art in ("role-packs", "tech-packs"):
        basis = os.path.join(HERE, "framework", art)
        if not os.path.isdir(basis):
            continue
        for pack in sorted(os.listdir(basis)):
            quelle = os.path.join(basis, pack, "skills")
            if not os.path.isdir(quelle):
                continue
            for name in sorted(os.listdir(quelle)):
                if os.path.isdir(os.path.join(quelle, name)):
                    herkunft.setdefault(name, f"{art[:-1]} {pack}")
    return herkunft


def list_skills(root: str, man: dict, client: str) -> int:
    """Zaehlt die Skills dieser Installation auf: Name, Herkunft, Aufrufbarkeit, Pfad.

    Warum das Framework eine Auskunft gibt, die eigentlich der Client geben sollte: Zusage
    S5 sagt zu, dass die geladenen Skills vollstaendig aufzaehlbar sind, samt Herkunft und
    Aufrufbarkeit. Bei 'claude-code' ist sie am 2026-09-12 als [NICHT ABBILDBAR] gemessen
    worden - es gibt kein Aufzaehlungskommando, und die Sitzung erhaelt Skills als Name und
    Kurzbeschreibung ohne Pfad; auf die Frage nach der Herkunft antwortete sie "Herkunft
    unbekannt - fuer alle 84".

    Ein Ausfall, der nur eingetragen und nicht ersetzt wird, ist eine stillschweigende
    Verschlechterung. Aufzaehlbarkeit ist das einzige Mittel, das einen unbemerkten Skill
    ueberhaupt bemerkt (AP2-DD-16, K-24) - deshalb Ersatz statt Abbuchung (CR-2026-041 E3,
    D-42).

    GRENZE, und sie steht auch in der Ausgabe: Diese Funktion sieht die Installation, nicht
    die Sitzung. Skills aus Ablagen ausserhalb des Projektverzeichnisses fuehrt sie nicht -
    genau die also, die niemand bemerkt. Eine Teilauskunft, die sich fuer eine vollstaendige
    ausgibt, waere der Befundtyp, gegen den dieses Projekt seine Sonden baut.
    """
    ablage = man["skills_dir"]
    basis = os.path.join(root, *ablage.split("/"))
    print(f"Skills in {root}")
    print(f"Client Pack: {client}; Ablage: {ablage}")
    print()
    if not os.path.isdir(basis):
        print(f"Keine Skill-Ablage unter {ablage}.")
        print("Ist in dieses Wurzelverzeichnis installiert worden?")
        return 1

    herkunft = skill_herkunft()
    feld = man.get("skill_frontmatter", {}).get("model_invocation_field")
    zeilen: list[tuple[str, str, str, str]] = []
    for name in sorted(os.listdir(basis)):
        pfad = os.path.join(basis, name, "SKILL.md")
        if not os.path.isfile(pfad):
            continue
        fm = ""
        try:
            text = read_text(pfad).replace("\r\n", "\n")
            if text.startswith("---\n") and "\n---\n" in text:
                fm = text.split("\n---\n", 1)[0][4:]
        except OSError:
            pass
        if feld and re.search(rf"^{re.escape(feld)}:[ \t]*true\b", fm, re.M):
            aufruf = "nur Nutzer"
        elif feld:
            aufruf = "Nutzer+Modell"
        else:
            # Ein Client ohne eigenes Feld traegt die Aussage weiter als triggers-Liste
            # der Quelle. Dann ist sie dort zu lesen und nicht "unbekannt" (K-18).
            m = re.search(r"^triggers:[ \t]*\n((?:[ \t]+-[ \t]+\S+[ \t]*\n)+)",
                          fm + "\n", re.M)
            ausloeser = [x.strip("- \t") for x in m.group(1).strip().split("\n")] if m else []
            aufruf = ("Nutzer+Modell" if "model" in ausloeser
                      else "nur Nutzer" if ausloeser else "unbekannt")
        zeilen.append((name, herkunft.get(name, "Projekt"), aufruf,
                       f"{ablage}/{name}/SKILL.md"))

    if not zeilen:
        print("Kein Skill gefunden.")
    else:
        b1 = max([len("Name")] + [len(z[0]) for z in zeilen])
        b2 = max([len("Herkunft")] + [len(z[1]) for z in zeilen])
        b3 = max([len("Aufrufbar")] + [len(z[2]) for z in zeilen])
        print(f"{'Name':<{b1}}  {'Herkunft':<{b2}}  {'Aufrufbar':<{b3}}  Pfad")
        for z in zeilen:
            print(f"{z[0]:<{b1}}  {z[1]:<{b2}}  {z[2]:<{b3}}  {z[3]}")
        print()
        print(f"{len(zeilen)} Skills in dieser Installation.")
    print()
    print("GRENZE DIESER AUSKUNFT: Sie fuehrt die Skills dieser Installation. Skills aus")
    print("Ablagen ausserhalb des Projektverzeichnisses - Benutzerprofil, andere Werkzeuge -")
    print("sieht auch das Framework nicht; ob der Client sie in die Sitzung mitfuehrt, steht")
    print("im Client Pack unter S5. Diese Liste ist Ersatz fuer eine fehlende Clientauskunft,")
    print("kein vollstaendiger Ersatz.")
    return 0


def installierte_clients(root: str) -> list[str]:
    """Welche Client Packs in diesem Projekt installiert sind - an ihrer Laufzeitschicht.

    Dieselbe Regel wie im Validator: Das Pack, dessen runtime_dir im Zielverzeichnis
    tatsaechlich liegt. Eine Aktualisierung richtet sich an etwas Vorhandenes; was
    vorhanden ist, ist ablesbar, und ein Vorgabewert ist dort eine Vermutung, die niemand
    braucht.

    Bis 0.27.0 gab es diese Erkennung hier nicht. `--update` ohne `--client` fiel auf die
    Vorgabe zurueck und legte in einer Installation des anderen Packs eine **zweite**
    Laufzeitschicht an - gemessen am 2026-09-12: 60 Dateien, und dabei "0 aktualisiert".
    Der Aufruf tat nicht zu viel, er tat das Falsche (B10, D-45).

    Liegen bereits zwei Schichten da, meldet die Funktion beide. Der Schaden ist dann
    schon eingetreten; die Aufgabe der Erkennung ist es, ihn zu zeigen statt ihn
    fortzuschreiben.
    """
    treffer = []
    for name in available_clients():
        try:
            man = load_manifest(name)
        except (OSError, ValueError, json.JSONDecodeError):
            continue
        if os.path.isdir(os.path.join(root, *man["runtime_dir"].split("/"))):
            treffer.append(name)
    return treffer


def kollisionen(root: str, template: str, man: dict) -> list[str]:
    """Vorhandene Dateien, die das Framework beansprucht und die von seiner Fassung abweichen.

    Bei einer **Erstinstallation** ist jede davon eine Datei des Projekts: Das Framework hat
    in dieses Verzeichnis noch nie geschrieben. Bis 0.28.0 wurden sie kommentarlos
    ueberschrieben - in der Zusammenfassung ausgewiesen als "1 aktualisiert", ein Wort, das
    nach Pflege klingt und hier Verlust bedeutet.

    Der wahrscheinliche Fall ist die Wurzel-Anweisungsdatei. Ihr Name ist keine Erfindung
    des Frameworks, sondern die Konvention des Clients - deshalb belegt ein Projekt ihn
    oft schon. Gemessen am 2026-09-12 im Trockenlauf gegen ein reales Projekt: Der erste
    Befehl des Uebernahmeleitfadens haette eine versionierte Datei von 34 Kilobyte ersetzt
    (CR-2026-046, D-46).

    Unterschieden wird am **Modus**, nicht an der Herkunft der Datei: Eine Erkennung ueber
    den Kopfkommentar waere feiner und wuerde bei .example- und JSON-Artefakten versagen,
    die keinen tragen. Fuer `--update` bleibt das Ueberschreiben richtig - dort ist das
    Pack bereits installiert, und genau dafuer ist der Modus da.
    """
    out: list[str] = []
    for rel in core_relpaths(template, man):
        dst = os.path.join(root, rel)
        if os.path.exists(dst) and not filecmp.cmp(os.path.join(template, rel), dst,
                                                   shallow=False):
            out.append(rel.replace(os.sep, "/"))
    for src_rel, dst_rel in framework_skill_files(man):
        dst = os.path.join(root, dst_rel)
        if os.path.exists(dst) and not rendered_matches(os.path.join(HERE, src_rel), dst, man):
            out.append(dst_rel)
    for src_rel, dst_rel in shared_files(man, "shared_core"):
        dst = os.path.join(root, *dst_rel.split("/"))
        if os.path.exists(dst) and not rendered_matches(
                os.path.join(HERE, *src_rel.split("/")), dst, man):
            out.append(dst_rel)
    return sorted(set(out))


# --- Der Kopierweg in ein Projekt (D-362, CR-2026-140) ------------------------------
#
# Bis 1.6.0 stand der Kopierweg nur im Leitfaden: den Kern von Hand ins Projekt
# kopieren, dann install.py dort aufrufen. An genau diesem Handgriff sind zwei Befunde
# entstanden - wer ganz .koolie/ kopiert, nimmt das Kennzeichen und aus dem Arbeitsbaum
# das Overlay des Frameworks mit (D-354), und wer mit `git archive HEAD` hebt, liefert
# den Stand von vorhin (D-333). --target geht denselben Weg als Werkzeug: Es kopiert NUR
# den Kern, aus einem Klon NUR das Verfolgte, und ruft danach die Installation IM
# Projekt auf - mit dem kopierten install.py, denn die Hook-Kommandos zeigen auf den
# Kern im Zielprojekt.
#
# WAS ES NICHT TUT: Es zieht keinen Overlay-Wert nach und es committet nicht. Das
# bleiben Handgriffe des Projekts.
#
# DER LIEFERUMFANG (D-367, seit 1.8.0): --lieferumfang nutzung laesst die
# Nachweisschicht weg (clientmap.NACHWEIS_ABLAGEN - dort steht, warum sie aufgezaehlt
# ist und nicht das Noetige). Die Wahl steht danach in LIEFERUMFANG neben VERSION und
# gilt beim naechsten Heben weiter: Das Heben ersetzt das Verzeichnis, und ohne diese
# Datei wuechse ein reduziertes Projekt beim ersten --update auf den ganzen Kern. Ein
# Wechsel geschieht nur, wenn --lieferumfang ihn ausdruecklich nennt.

# Die Mindestversion ist GEMESSEN, nicht gesetzt (D-363): Installation, Validator und
# Hooks laufen unter 3.8.20 zeilengleich zu 3.14, alle Python-Traeger des Repositoriums
# kompilieren dort. 3.7 war auf dem Messplatz nicht beschaffbar. Die beiden Starter
# pruefen dieselbe Zahl - eine Sonde haelt die drei Stellen gegeneinander.
PYTHON_MINDEST = (3, 8)

ZIEL_NEU = "core.koolie-neu"
ZIEL_ALT = "core.koolie-alt"

# Windows begrenzt ohne Langpfad-Freigabe einen Dateipfad auf 259 und einen
# Verzeichnispfad beim Anlegen auf 247 Zeichen (MAX_PATH). Gemessen am 2026-09-25
# (D-368): --target in ein Projekt unter dem Ablagebereich einer Sitzung brach beim
# Kopieren ab. Der Rueckbau hielt, aber die Meldung fragte, ob eine Datei geoeffnet sei
# - den Grund nannte sie nicht. Geprueft wird deshalb VOR der ersten Kopie, gegen den
# laengsten Pfad unter dem Zwischenverzeichnis, das laenger heisst als der Kern.
# Auch mit Freigabe bleibt die Grenze: git und die Clients halten sich nicht alle daran.
PFAD_GRENZE_DATEI = 259
PFAD_GRENZE_VERZEICHNIS = 247


def zu_langer_pfad(basis: str, dateien: list[str]) -> tuple[str, int]:
    """Der erste Pfad unter basis, der unter Windows seine Grenze reisst, und diese
    Grenze - sonst ('', 0)."""
    if os.name != "nt":
        return "", 0
    for rel in dateien:
        datei = os.path.join(basis, *rel.split("/"))
        if len(datei) > PFAD_GRENZE_DATEI:
            return datei, PFAD_GRENZE_DATEI
        if len(os.path.dirname(datei)) > PFAD_GRENZE_VERZEICHNIS:
            return os.path.dirname(datei), PFAD_GRENZE_VERZEICHNIS
    return "", 0


def quellwurzel() -> str:
    """Das Verzeichnis, in dem der Kern dieses install.py liegt: zwei Ebenen hoeher."""
    return os.path.dirname(os.path.dirname(HERE))


def _gleicher_pfad(a: str, b: str) -> bool:
    return os.path.normcase(os.path.abspath(a)) == os.path.normcase(os.path.abspath(b))


def _git(*argv: str):
    try:
        return subprocess.run(["git", *argv], capture_output=True)
    except OSError:
        return None


def quelle_kerndateien() -> tuple[list[str], str]:
    """Die Dateien des Kerns, relativ zu HERE, und woher die Liste stammt.

    Aus einem Klon des Frameworks nur das Verfolgte, gelesen aus dem Arbeitsbaum (D-333)
    - sonst kaemen Bytecode, build/out/ und liegengebliebene Entwuerfe mit. Ohne Klon
    (entpacktes Release-Archiv) alles ausser den Erzeugnissen, die ein Lauf dort
    hinterlaesst. 🔴 Der Klon wird nur anerkannt, wenn seine Wurzel GENAU die Quellwurzel
    ist: Ein Archiv, das in einem fremden Repositorium entpackt wurde, ist dort
    unverfolgt, und `git ls-files` lieferte eine leere Liste.
    """
    wurzel = quellwurzel()
    top = _git("-C", wurzel, "rev-parse", "--show-toplevel")
    if top is not None and top.returncode == 0 and _gleicher_pfad(
            top.stdout.decode("utf-8", "replace").strip(), wurzel):
        p = _git("-C", wurzel, "ls-files", "-z", "--", clientmap.CORE_REL)
        if p is not None and p.returncode == 0:
            praefix = clientmap.CORE_REL + "/"
            rel = sorted(n[len(praefix):] for n in p.stdout.decode("utf-8").split("\0")
                         if n.startswith(praefix))
            if "install.py" in rel:
                return rel, "Klon - nur Verfolgtes, aus dem Arbeitsbaum"
    rel = []
    ausgabe = os.path.join(HERE, "build", "out")
    for dirpath, dirnames, filenames in os.walk(HERE):
        dirnames[:] = sorted(d for d in dirnames
                             if d not in ("__pycache__", ".git")
                             and not _gleicher_pfad(os.path.join(dirpath, d), ausgabe))
        for fn in sorted(filenames):
            if fn.endswith((".pyc", ".pyo")):
                continue
            rel.append(os.path.relpath(os.path.join(dirpath, fn), HERE).replace(os.sep, "/"))
    return rel, "Verzeichnis - ohne __pycache__ und build/out"


def _loesche_baum(pfad: str) -> None:
    """Einen Baum loeschen, auch mit schreibgeschuetzten Dateien.

    Ohne onerror/onexc von shutil.rmtree: Die beiden Namen haben sich zwischen den
    Python-Fassungen abgeloest, und dieses Werkzeug laeuft ab 3.8 (D-363).
    """
    for dirpath, dirnames, filenames in os.walk(pfad, topdown=False):
        for fn in filenames:
            f = os.path.join(dirpath, fn)
            try:
                os.chmod(f, 0o666)
            except OSError:
                pass
            os.remove(f)
        for d in dirnames:
            os.rmdir(os.path.join(dirpath, d))
    os.rmdir(pfad)


def kern_version(kern: str) -> str:
    try:
        with open(os.path.join(kern, "VERSION"), encoding="utf-8") as fh:
            return fh.read().strip() or "unbekannt"
    except OSError:
        return "unbekannt"


def in_projekt_installieren(args) -> int:
    """--target: den Kern ins Projekt kopieren, dann dort install.py aufrufen."""
    ziel = os.path.abspath(args.target)
    if args.check or args.list_skills:
        print("FEHLER: --target kopiert und installiert. --check und --list-skills "
              "gehoeren an das install.py im Projekt.", file=sys.stderr)
        return 1
    if args.root is not None:
        print("FEHLER: --target und --root schliessen einander aus - das Ziel ist das "
              "Projekt, das --target nennt.", file=sys.stderr)
        return 1
    if not os.path.isdir(ziel):
        print(f"FEHLER: Das Projektverzeichnis gibt es nicht: {ziel}", file=sys.stderr)
        return 1
    wurzel = quellwurzel()
    if _gleicher_pfad(ziel, wurzel):
        print("FEHLER: Quelle und Ziel sind dasselbe Verzeichnis. --target nennt das "
              "Projekt, in das installiert wird - nicht das, aus dem kopiert wird.",
              file=sys.stderr)
        return 1
    if os.path.normcase(ziel + os.sep).startswith(os.path.normcase(HERE + os.sep)):
        print("FEHLER: Das Ziel liegt im Kern selbst.", file=sys.stderr)
        return 1

    zielkern = os.path.join(ziel, *clientmap.CORE_REL.split("/"))
    ablage = os.path.dirname(zielkern)
    vorhanden = os.path.isdir(zielkern)
    if vorhanden and not args.update:
        print(f"FEHLER: In {ziel} liegt bereits ein Kern (Stand "
              f"{kern_version(zielkern)}). Eine Erstinstallation wuerde ihn ersetzen.\n"
              f"Heben auf diesen Stand: --update.", file=sys.stderr)
        return 1
    if args.update and not vorhanden:
        print(f"FEHLER: --update hebt eine vorhandene Installation - in {ziel} liegt "
              f"kein {clientmap.CORE_REL}/. Fuer eine Erstinstallation --update "
              f"weglassen.", file=sys.stderr)
        return 1
    if vorhanden and not os.path.isfile(os.path.join(zielkern, "install.py")):
        # Nur ein Verzeichnis, das wie ein Kern aussieht, wird ersetzt - nie ein fremdes.
        print(f"FEHLER: {zielkern} traegt kein install.py und ist deshalb kein Kern "
              f"dieses Frameworks. Es wird nicht ersetzt.", file=sys.stderr)
        return 1

    # Der Lieferumfang (D-367): ausdruecklich genannt, sonst der bisherige des Projekts,
    # sonst voll. Eine reduzierte Quelle kann keinen vollen Kern liefern.
    quellumfang = clientmap.lieferumfang(HERE)
    bisher = clientmap.lieferumfang(zielkern) if vorhanden else ""
    for wert, wo in ((quellumfang, f"der Quelle ({HERE})"),
                     (bisher or "voll", f"des Projekts ({zielkern})")):
        if wert not in clientmap.LIEFERUMFAENGE:
            print(f"FEHLER: {clientmap.LIEFERUMFANG_DATEI} {wo} traegt '{wert}' - bekannt "
                  f"sind {', '.join(clientmap.LIEFERUMFAENGE)}. Kopiert wird nichts.",
                  file=sys.stderr)
            return 1
    umfang = args.lieferumfang or bisher or "voll"
    if umfang == "voll" and quellumfang != "voll":
        print(f"FEHLER: Die Quelle ist selbst eine Installation mit Lieferumfang "
              f"'{quellumfang}' - ihr fehlt die Nachweisschicht, und einen vollen Kern kann "
              f"sie nicht liefern. Quelle ist ein Klon oder das Release-Archiv.",
              file=sys.stderr)
        return 1

    dateien, herkunft = quelle_kerndateien()
    # Die Datei der Wahl wird nie mitkopiert, sondern fuer das Ziel geschrieben.
    dateien = [rel for rel in dateien if rel != clientmap.LIEFERUMFANG_DATEI]
    fehlen = [rel for rel in dateien if not os.path.isfile(os.path.join(HERE, *rel.split("/")))]
    if fehlen:
        print(f"FEHLER: {len(fehlen)} verfolgte Datei(en) des Kerns fehlen im Arbeitsbaum "
              f"der Quelle, etwa {fehlen[0]}. Kopiert wird nichts.", file=sys.stderr)
        return 1
    weg = [rel for rel in dateien if clientmap.ist_nachweis(rel)] if umfang == "nutzung" else []
    if weg:
        dateien = [rel for rel in dateien if not clientmap.ist_nachweis(rel)]

    quellstand = kern_version(HERE)
    print(f"Quelle:  {wurzel}  (Stand {quellstand})")
    print(f"Ziel:    {ziel}")
    if vorhanden:
        print(f"Modus:   Heben von {kern_version(zielkern)} auf {quellstand}")
    else:
        print("Modus:   Erstinstallation")
    print(f"Kern:    {len(dateien)} Dateien ({herkunft}); nur {clientmap.CORE_REL}/, "
          f"nie ganz .koolie/")
    wechsel = f" (bisher {bisher})" if bisher and bisher != umfang else ""
    if umfang == "nutzung":
        print(f"Umfang:  nutzung{wechsel} - ohne die Nachweisschicht, {len(weg)} Dateien "
              f"weniger: {', '.join(clientmap.NACHWEIS_ABLAGEN)}")
    else:
        print(f"Umfang:  voll{wechsel} - der ganze Kern")

    lang, grenze = zu_langer_pfad(os.path.join(ablage, ZIEL_NEU),
                                  dateien + [clientmap.LIEFERUMFANG_DATEI])
    if lang:
        print(f"FEHLER: Der Pfad zum Projekt ist fuer Windows zu lang. Beim Kopieren "
              f"entstuende ein Pfad mit {len(lang)} Zeichen, erlaubt sind {grenze}:\n"
              f"  {lang}\nDas Projekt braucht einen um mindestens {len(lang) - grenze} "
              f"Zeichen kuerzeren Pfad. Kopiert wird nichts (D-368).", file=sys.stderr)
        return 1
    if args.dry_run:
        print()
        print("dry-run: Es wird nichts geschrieben. Die Installation im Projekt folgt "
              "erst nach dem Kopieren und wird deshalb hier nicht vorgefuehrt.")
        return 0

    neu = os.path.join(ablage, ZIEL_NEU)
    alt = os.path.join(ablage, ZIEL_ALT)
    for rest in (neu, alt):
        if os.path.isdir(rest):
            # Ein Rest eines abgebrochenen Laufs dieses Werkzeugs, an seinem Namen erkannt.
            _loesche_baum(rest)
    os.makedirs(ablage, exist_ok=True)
    try:
        for rel in dateien:
            dst = os.path.join(neu, *rel.split("/"))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(os.path.join(HERE, *rel.split("/")), dst)
        with open(os.path.join(neu, clientmap.LIEFERUMFANG_DATEI), "w", encoding="utf-8",
                  newline="\n") as fh:
            fh.write(umfang + "\n")
        if vorhanden:
            os.replace(zielkern, alt)
        try:
            os.replace(neu, zielkern)
        except OSError:
            if vorhanden:
                os.replace(alt, zielkern)
            raise
    except OSError as exc:
        if os.path.isdir(neu):
            _loesche_baum(neu)
        print(f"FEHLER: Der Kern liess sich nicht nach {zielkern} kopieren: {exc}\n"
              f"Ist eine Datei darin geoeffnet? Das Projekt ist unveraendert.",
              file=sys.stderr)
        return 1

    print()
    print(f"--- Installation im Projekt, mit {clientmap.CORE_REL}/install.py des Ziels ---")
    print()
    argv = [sys.executable, os.path.join(zielkern, "install.py"), "--root", ziel]
    if args.update:
        argv.append("--update")
    if args.client:
        argv += ["--client", args.client]
    if args.overlay:
        argv += ["--overlay", args.overlay]
    sys.stdout.flush()
    rc = subprocess.run(argv).returncode
    if rc != 0:
        # Die Installation bricht vor ihrem ersten Schreibvorgang ab (Kollisionen,
        # Muster, Abbildung). Der kopierte Kern gehoert dann niemandem - zurueck damit.
        _loesche_baum(zielkern)
        if vorhanden:
            os.replace(alt, zielkern)
            print(f"\nDie Installation im Projekt ist gescheitert; der bisherige Kern "
                  f"(Stand {kern_version(zielkern)}) liegt wieder an seinem Platz.",
                  file=sys.stderr)
        else:
            print(f"\nDie Installation im Projekt ist gescheitert; der kopierte Kern ist "
                  f"wieder entfernt.", file=sys.stderr)
        return rc
    if vorhanden:
        _loesche_baum(alt)
        print()
        print("Das Heben ist erst mit diesen Handgriffen ein Stand "
              "(RELEASE_PROCESS.md 4.1, Schritt 2):")
        print("  1. geaenderte Overlay-Werte in allen drei Traegern nachziehen,")
        print("  2. python .koolie/core/tests/scripts/validate-framework.py "
              "--strict-overlay,")
        print("  3. im Projekt committen.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Installiert die Wurzeldateien des Koolie-Frameworks in ein Projekt.")
    ap.add_argument("--root", default=None,
                    help="Wurzelverzeichnis des Projekts (Standard: aktuelles Verzeichnis)")
    ap.add_argument("--target", default=None, metavar="PROJEKT",
                    help="Den Kern dieses install.py in PROJEKT kopieren und dort installieren; "
                         "mit --update ein vorhandenes Projekt heben (D-362)")
    ap.add_argument("--lieferumfang", choices=clientmap.LIEFERUMFAENGE, default=None,
                    help="Nur mit --target: den ganzen Kern (voll) oder ohne die "
                         "Nachweisschicht (nutzung) kopieren. Ohne Angabe bleibt es beim "
                         "Heben beim bisherigen Umfang, sonst voll (D-367)")
    ap.add_argument("--update", action="store_true",
                    help="Core-Dateien auf den Stand dieses Releases bringen; Projektdateien bleiben unberuehrt")
    ap.add_argument("--check", action="store_true",
                    help="Nur pruefen: meldet fehlende und abweichende Core-Dateien, schreibt nichts")
    ap.add_argument("--dry-run", action="store_true",
                    help="Zeigen, was geschehen wuerde, ohne zu schreiben")
    ap.add_argument("--client", default=None,
                    help=f"Client Pack, aus dem installiert wird. Ohne Angabe wird das installierte Pack erkannt; bei einer Erstinstallation gilt {DEFAULT_CLIENT}")
    ap.add_argument("--list-clients", action="store_true",
                    help="Verfuegbare Client Packs auflisten und beenden")
    ap.add_argument("--list-skills", action="store_true",
                    help="Skills dieser Installation auflisten: Name, Herkunft, Aufrufbarkeit, Pfad")
    ap.add_argument("--overlay", nargs="?", const="", default=None, metavar="NAME",
                    help="Nur bei der Erstinstallation: ein mitgeliefertes Overlay-Muster statt "
                         "des leeren Overlays (D-126). Ohne NAME: verfuegbare Muster auflisten")
    args = ap.parse_args()

    if sys.version_info < PYTHON_MINDEST:
        print(f"FEHLER: Koolie braucht Python {'.'.join(map(str, PYTHON_MINDEST))} oder "
              f"neuer; dieses ist {sys.version.split()[0]} (D-363).", file=sys.stderr)
        return 1

    clients = available_clients()

    if args.overlay == "":
        muster_namen = verfuegbare_muster()
        if not muster_namen:
            print(f"Keine Overlay-Muster unter {MUSTER_ABLAGE} gefunden.")
            return 1
        print("Verfuegbare Overlay-Muster (nur bei der Erstinstallation, --overlay <name>):")
        for name in muster_namen:
            try:
                m = muster_laden(name)
            except MusterFehler as exc:
                print(f"  {name}  (nicht verwendbar: {exc})")
                continue
            print(f"  {name}  {m['version']}  - fuellt {', '.join(m['werte'])}")
        print()
        print("Ohne --overlay beginnt das Projekt mit dem leeren Overlay. Was ein Muster")
        print("fuellt und was nicht, steht in .koolie/core/framework/overlay-patterns/<name>.md.")
        return 0

    if args.list_clients:
        if not clients:
            print("Keine installierbaren Client Packs gefunden.")
            print(f"Erwartet: {CLIENT_PACKS}/<name>/root-template/")
            return 1
        print("Verfuegbare Client Packs:")
        for name in clients:
            mark = "  (Standard)" if name == DEFAULT_CLIENT else ""
            print(f"  {name}{mark}")
        print()
        print("Welche Zusagen des Frameworks ein Client technisch durchsetzt, steht in")
        print(".koolie/core/clients/<name>/CLIENT_PACK.md.")
        return 0

    if args.target is not None:
        return in_projekt_installieren(args)
    if args.lieferumfang is not None:
        # Nur --target kopiert den Kern; ohne Kopie gibt es nichts wegzulassen.
        print("FEHLER: --lieferumfang gehoert zu --target - nur dort wird der Kern "
              "kopiert.", file=sys.stderr)
        return 1

    # Das Ziel steht vor der Clientwahl fest - denn es entscheidet sie.
    root = os.path.abspath(args.root or os.getcwd())
    if os.path.abspath(HERE) == root:
        print("FEHLER: --root zeigt auf .koolie/core/ selbst. Gemeint ist das "
              "Wurzelverzeichnis des Projekts, also eine Ebene darueber.", file=sys.stderr)
        return 1

    erkannt = installierte_clients(root)
    if len(erkannt) > 1:
        print(f"FEHLER: In {root} liegen bereits mehrere Laufzeitschichten: "
              f"{', '.join(erkannt)}. Welche gilt, entscheidet der Client - und die "
              f"Packs kennen einander nicht. Entferne die nicht gewollte Schicht und "
              f"rufe erneut auf.", file=sys.stderr)
        return 1

    if args.client is None:
        # Erkanntes Pack vor Vorgabe. Die Vorgabe gilt nur, wo es nichts zu erkennen
        # gibt - bei einer Erstinstallation.
        args.client = erkannt[0] if erkannt else DEFAULT_CLIENT
    elif erkannt and args.client not in erkannt:
        print(f"FEHLER: In {root} ist das Client Pack '{erkannt[0]}' installiert, "
              f"angefordert ist '{args.client}'. Eine Aktualisierung wuerde hier keine "
              f"Datei aktualisieren, sondern eine zweite Laufzeitschicht anlegen. Ein "
              f"Wechsel des Packs ist eine Entscheidung: Entferne dazu die vorhandene "
              f"Laufzeitschicht und rufe erneut auf.", file=sys.stderr)
        return 1

    if args.client not in clients:
        print(f"FEHLER: Unbekanntes Client Pack: {args.client}", file=sys.stderr)
        if clients:
            print(f"Verfuegbar: {', '.join(clients)}", file=sys.stderr)
        else:
            print(f"Kein Pack mit root-template/ unter {CLIENT_PACKS} gefunden.", file=sys.stderr)
        return 1

    template = client_template(args.client)
    try:
        man = load_manifest(args.client)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FEHLER: Manifest des Client Packs {args.client} nicht lesbar: {exc}", file=sys.stderr)
        return 1

    if args.list_skills:
        return list_skills(root, man, args.client)

    mode = "check" if args.check else ("update" if args.update else "install")

    muster = None
    if args.overlay:
        # Ein Muster ist ein Anfangszustand, kein Kanal (D-76, D-355): Es wirkt nur, wo
        # die Saat noch nicht liegt. Wer es bei --update erwartet, erwartet einen
        # Fuellschritt ueber Projektwerte - und genau den gibt es nicht.
        if mode != "install":
            print(f"FEHLER: --overlay gilt nur bei der Erstinstallation, nicht mit "
                  f"--{mode}. Die Saat gehoert nach der Erstinstallation dem Projekt "
                  f"(D-76).", file=sys.stderr)
            return 1
        try:
            muster = muster_laden(args.overlay)
        except MusterFehler as exc:
            print(f"FEHLER: {exc}", file=sys.stderr)
            return 1
        vorhanden = [dst_rel for _src, dst_rel in
                     shared_files(man, "shared_seed") + muster_dokumentziele(muster)
                     if os.path.exists(os.path.join(root, *dst_rel.split("/")))]
        if vorhanden:
            print(f"FEHLER: --overlay {args.overlay} fuellt die Saat bei der "
                  f"Erstinstallation - hier liegt sie schon ({len(vorhanden)} Datei(en)):",
                  file=sys.stderr)
            for rel in vorhanden[:6]:
                print(f"  {rel}", file=sys.stderr)
            print("Vorhandene Saat gehoert dem Projekt und wird nie ueberschrieben. Werte "
                  "aus dem Muster von Hand uebernehmen:", file=sys.stderr)
            print(f"  .koolie/core/framework/overlay-patterns/{args.overlay}.md",
                  file=sys.stderr)
            return 1

    if mode == "install":
        # Vor dem ersten Schreibvorgang, nicht waehrenddessen: Ein Abbruch nach der
        # Haelfte der Dateien waere schlimmer als keiner.
        belegt = kollisionen(root, template, man)
        if belegt:
            print(f"FEHLER: In {root} liegen bereits Dateien, die das Framework "
                  f"beansprucht:", file=sys.stderr)
            for rel in belegt:
                print(f"  {rel}", file=sys.stderr)
            print("", file=sys.stderr)
            print("Eine Erstinstallation wuerde sie ueberschreiben. Das Framework hat in "
                  "dieses\nVerzeichnis noch nie geschrieben - diese Dateien gehoeren also "
                  "dem Projekt.", file=sys.stderr)
            print("", file=sys.stderr)
            print("Stammen sie aus einer frueheren Installation: --update verwenden.",
                  file=sys.stderr)
            print("Sonst den Inhalt vorher uebernehmen - Projektwissen nach "
                  ".koolie/project-overlay/OVERLAY.md,\nprojektspezifische Regeln in eine Regeldatei "
                  "2N-overlay-<name>.md. Danach die\nDatei entfernen und erneut aufrufen "
                  "(.koolie/core/docs/ADOPTION_GUIDE.md, Abschnitt 2).", file=sys.stderr)
            return 1
    version_file = os.path.join(HERE, "VERSION")
    version = open(version_file, encoding="utf-8").read().strip() if os.path.exists(version_file) else "unbekannt"

    print(f"Framework {version}")
    print(f"Client:  {args.client}")
    print(f"Vorlage: {os.path.relpath(template, root) if root in template else template}")
    print(f"Ziel:    {root}")
    print(f"Modus:   {mode}{'  (dry-run, es wird nichts geschrieben)' if args.dry_run else ''}")
    if muster:
        print(f"Overlay: Muster {muster['name']} {muster['version']}")
    print()

    try:
        rep = run(root, template, man, mode, args.dry_run, muster)
    except MusterFehler as exc:
        print(f"FEHLER: Das Overlay-Muster laesst sich nicht vollstaendig anwenden; es "
              f"wurde nichts geschrieben.", file=sys.stderr)
        print(f"  {exc}", file=sys.stderr)
        return 1
    except clientmap.AbbildungsFehler as exc:
        # D-26/D-27: Eine Aussage der Quelle, die dieser Client nicht tragen kann, wird
        # abgebildet oder die Installation scheitert. Sie stillschweigend wegzulassen
        # waere ein Verlust der Zusage - deshalb hier ein Abbruch und keine Warnung.
        print(f"FEHLER: Die Quellen lassen sich nicht verlustfrei auf das Client Pack "
              f"{args.client} abbilden.\n  {exc}", file=sys.stderr)
        return 1

    def block(title: str, items: list[str], limit: int = 12) -> None:
        if not items:
            return
        print(f"{title} ({len(items)}):")
        for rel in items[:limit]:
            print(f"  {rel}")
        if len(items) > limit:
            print(f"  ... und {len(items) - limit} weitere")
        print()

    if mode == "check":
        block("Core-Dateien fehlen", rep.missing)
        block("Core-Dateien weichen von der Vorlage ab", rep.drifted)
        print(f"Unveraendert: {len(rep.unchanged)} | Projektdateien vorhanden: {len(rep.kept)}")
        if rep.drifted:
            print()
            print("Abweichende Core-Dateien bedeuten: Es wurde an der falschen Stelle bearbeitet.")
            tpl_rel = os.path.relpath(template, HERE).replace(os.sep, "/")
            print(f"Core-Aenderungen gehoeren in .koolie/core/{tpl_rel}/ und laufen")
            print("als Aenderungsantrag (.koolie/core/governance/FEEDBACK_PROCESS.md).")
            print("Mit --update wird der Release-Stand wiederhergestellt; lokale Aenderungen gehen dabei verloren.")
        if rep.missing or rep.drifted:
            return 1
        print("\nErgebnis: Core ist auf dem Stand des Releases.")
        return 0

    block("Angelegt", rep.created)
    block("Core aktualisiert", rep.updated)
    if rep.kept:
        print(f"Projektdateien unberuehrt gelassen: {len(rep.kept)}")
        for rel in rep.kept[:6]:
            print(f"  {rel}")
        if len(rep.kept) > 6:
            print(f"  ... und {len(rep.kept) - 6} weitere")
        print()

    print(f"Zusammenfassung: {len(rep.created)} angelegt, {len(rep.updated)} aktualisiert, "
          f"{len(rep.unchanged)} unveraendert, {len(rep.kept)} Projektdateien behalten.")

    if mode == "install" and rep.created:
        print()
        print("Naechste Schritte:")
        print("  1. .koolie/project-overlay/OVERLAY.md ausfuellen (Platzhalter und <TBD>-Felder).")
        if muster:
            print(f"     Vorbefuellt aus dem Muster {muster['name']}: "
                  f"{', '.join(muster['werte'])} - in allen drei Traegern.")
            print("     Die Werte sind Vorschlaege: pruefen, anpassen, und eine Aenderung in")
            print(f"     OVERLAY.md, der Laufzeitfassung und {man['permissions_file']} nachziehen.")
            if muster["dokumente"]:
                print(f"     Dazu {len(muster['dokumente'])} Musterdokumente unter "
                      f"{MUSTER_DOKUMENTZIEL}/, im Manifest mit")
                print("     Status entwurf registriert. Sie wirken erst, wenn der Overlay Owner "
                      "sie prueft,")
                print("     freigibt und in der Laufzeitfassung als K1-Dokumente fuehrt.")
        # Den Integritaetsblock fuehrt nur eine Berechtigungsdatei im JSON-Format - auch
        # das Agentenprofil von kiro (D-414); die TOML-Datei eines Packs kennt ihn nicht
        # (K-123, D-395).
        if clientmap.permissions_format(man) in ("json", "kiro-agent"):
            print(f"  2. Werte in {man['permissions_file']} eintragen - die Kernregeln unter")
            print("     _core_rules_integrity nicht entfernen.")
        else:
            print(f"  2. Werte in {man['permissions_file']} eintragen.")
        print("  3. .koolie/project-overlay/forbidden-terms.txt mit den realen Projekt- und")
        print("     Kundennamen fuellen (bleibt projektlokal).")
        print("  4. .koolie/core/checklists/10-project-adoption.md abarbeiten.")
        print("  5. python .koolie/core/tests/scripts/validate-framework.py --strict-overlay")
        nachschritte(man.get("post_install_steps", []), 6)
    if mode == "update":
        print()
        print(f"Hinweis: {man['permissions_file']} wurde nicht angefasst, weil sie Projektwerte enthaelt.")
        print("Pruefe nach einem Release-Wechsel, ob die Kernregeln noch vollstaendig sind:")
        print("  python .koolie/core/tests/scripts/validate-framework.py --strict-overlay")
        if man.get("post_update_steps"):
            print()
            print("Fuer dieses Client Pack ausserdem:")
            nachschritte(man["post_update_steps"], 1)

    ignoriert = ignorierte_kerndateien(root)
    if ignoriert:
        print()
        print(f"HINWEIS ({len(ignoriert)}): Dieses Projekt IGNORIERT Kerndateien, die "
              f"soeben geschrieben wurden.")
        for rel in ignoriert[:8]:
            print(f"  {rel}")
        if len(ignoriert) > 8:
            print(f"  ... und {len(ignoriert) - 8} weitere")
        print("Sie liegen im Arbeitsbaum, aber nicht im Versionierten - beim naechsten")
        print("Klonen dieses Projekts fehlen sie. Abhilfe: eine Negativregel im")
        print(f"'.gitignore' des Projekts, etwa '!{clientmap.CORE_REL}/**'. Das '.gitignore'")
        print("gehoert dem Projekt; dies ist eine Auskunft und keine Schranke.")

    kanaele = belegte_importkanaele(root, man)
    if kanaele:
        print()
        # Die Einleitung sagt seit 1.13.0 das Pack selbst (import_channels_intro): Bei
        # kiro sind es keine Quellen eines fremden Werkzeugs, sondern die eigenen
        # Ablagen des Clients im Benutzerprofil (D-414).
        einleitung = man.get("import_channels_intro") or (
            "Die Importsteuerung dieses Client Packs laesst Quellen eines fremden "
            "Werkzeugs zu,")
        print(f"HINWEIS ({len(kanaele)}): {einleitung}")
        print("und auf diesem Arbeitsplatz sind davon belegt:")
        for rel, was in kanaele:
            print(f"  {rel}")
            for zeile in textwrap.wrap(was, width=76):
                print(f"    {zeile}")
        print("Was dort steht, erreicht die Sitzung neben den Regeln des Frameworks. Pruefen,")
        print("ob es dorthin gehoert (CLIENT_PACK.md, Zeile R6). Dies ist eine Auskunft und")
        print("keine Schranke.")

    if traegt_quellrepo_kennzeichen(root):
        print()
        print(f"HINWEIS: In diesem Verzeichnis liegt {QUELLREPO_KENNZEICHEN} - das "
              f"Kennzeichen des Framework-Repositoriums selbst.")
        print("Ist dies ein Projekt, wurde beim Kopieren zu viel mitgenommen: Kopiert wird")
        print(f"nur {clientmap.CORE_REL}/, nie ganz .koolie/. Solange die Datei hier liegt, haelt")
        print("der Validator das Projekt fuer das Quellrepositorium und prueft Projektdateien")
        print("mit (Pruefungen 75, 78, 79 und 81). Abhilfe: die Datei entfernen und pruefen, ob")
        print(".koolie/project-overlay/ noch der Stand des Projekts ist - eine Kopie aus dem")
        print("Arbeitsbaum des Frameworks bringt dessen Overlay mit.")
        print("Im Framework-Repositorium selbst ist nichts zu tun. Dies ist eine Auskunft und")
        print("keine Schranke.")

    print()
    print("Diese Pfade gehoeren dem Projekt und werden von install.py nie geschrieben:")
    for hint in man.get("project_owned_hint", []):
        print(f"  {hint}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
