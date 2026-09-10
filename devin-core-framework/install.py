#!/usr/bin/env python3
"""
install.py - Legt die Wurzeldateien des Devin Desktop Frameworks in einem Projekt an.

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

    python devin-core-framework/install.py                        # Erstinstallation, Standard-Client
    python devin-core-framework/install.py --client <name>        # anderer Client
    python devin-core-framework/install.py --list-clients         # verfuegbare Client Packs
    python devin-core-framework/install.py --update               # Core aktualisieren
    python devin-core-framework/install.py --check                # nur pruefen, nichts schreiben
    python devin-core-framework/install.py --dry-run              # zeigen, was passieren wuerde

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
import sys

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
#                 (devin-core-framework/governance/FEEDBACK_PROCESS.md).
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


def load_manifest(client: str) -> dict:
    path = os.path.join(CLIENT_PACKS, client, "manifest.json")
    with open(path, encoding="utf-8") as fh:
        m = json.load(fh)
    fehlend = [f for f in MANIFEST_PFLICHTFELDER if f not in m]
    if fehlend:
        raise ValueError(f"{client}/manifest.json: Pflichtfelder fehlen: {', '.join(fehlend)}")
    # <CORE_DIR> steht in keinem Manifest: Der Name des Kernverzeichnisses ist keine
    # Eigenschaft eines Clients, sondern dieser Installation. Er wird hier gesetzt,
    # damit eine spaetere Umbenennung (Roadmap P3) nur eine Stelle beruehrt.
    m.setdefault("runtime_placeholders", {})["<CORE_DIR>"] = os.path.basename(HERE)
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
    Projekteigene Packs (etwa unter project-overlay/tech-packs/) bleiben unberuehrt.
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


def render_skill_frontmatter(text: str, man: dict) -> str:
    """Bringt das Frontmatter eines Skills in die Form, die dieser Client erwartet.

    Quellformat ist die reichere Listenform: allowed-tools als Liste, dazu permissions
    und triggers. Ein Client, der nur eine kommagetrennte Werkzeugliste kennt, bekommt
    sie umgeformt; Felder, die er nicht kennt, entfallen (K-18: Frontmatter nur mit
    dokumentierten Feldern).
    """
    fmt = man.get("skill_frontmatter", {})
    if not text.startswith("---\n") or "\n---\n" not in text:
        return text
    kopf, rumpf = text.split("\n---\n", 1)
    fm = kopf[4:].rstrip("\n") + "\n"

    if fmt.get("tools_format") == "csv":
        m = re.search(r"^allowed-tools:[ \t]*\n((?:[ \t]+-[ \t]+\S+[ \t]*\n)+)", fm, re.M)
        werkzeuge = [x.strip("- \t") for x in m.group(1).strip().split("\n")] if m else []
        abbildung = fmt.get("tool_names", {})
        ziel: list[str] = []
        for w in werkzeuge:
            for y in abbildung.get(w, [w]):
                if y not in ziel:
                    ziel.append(y)
        for feld in ["allowed-tools"] + list(fmt.get("drop_fields", [])):
            fm = re.sub(rf"^{feld}:.*\n(?:[ \t]+\S.*\n)*", "", fm, flags=re.M)
        if ziel:
            fm = fm.rstrip("\n") + f"\nallowed-tools: {', '.join(ziel)}\n"
    else:
        for feld in fmt.get("drop_fields", []):
            fm = re.sub(rf"^{feld}:.*\n(?:[ \t]+\S.*\n)*", "", fm, flags=re.M)

    return "---\n" + fm + "---\n" + rumpf


def render_rule(text: str, man: dict) -> str:
    """Bringt einen Regeltext in die Form, die dieser Client erwartet.

    Quellformat ist das YAML-Frontmatter mit description und trigger - die reichere Form.
    Ein Client ohne Ladetrigger kann damit nichts anfangen (K-18: Frontmatter nur mit
    dokumentierten Feldern); fuer ihn wird daraus ein Kommentar, der Zweck und
    Ladeverhalten festhaelt. Der Regeltext selbst bleibt in beiden Faellen identisch.
    """
    if man.get("rule_frontmatter", "yaml") == "yaml":
        return text
    if not text.startswith("---\n") or "\n---\n" not in text:
        return text
    kopf, rumpf = text.split("\n---\n", 1)
    fm = kopf[4:]
    desc = re.search(r"^description:\s*(.+)$", fm, re.M)
    trig = re.search(r"^trigger:\s*(\S+)\s*$", fm, re.M)
    desc = desc.group(1).strip() if desc else ""
    trig = trig.group(1).strip() if trig else "unbekannt"
    hinweis = ("Wird über den Import in der Wurzel-Anweisungsdatei immer geladen."
               if trig != "always_on" else
               "Wird über den Import in der Wurzel-Anweisungsdatei geladen.")
    if trig not in ("always_on",):
        hinweis += (" Bei Clients mit Ladetriggern lädt diese Datei nur bei Relevanz;"
                    " immer zu laden ist eine Verschärfung, keine Lockerung.")
    kommentar = (f"<!-- Laufzeitregel. Inhaltlich identisch zur Fassung anderer Client Packs;\n"
                 f"     abweichend ist nur der Lademechanismus.\n"
                 f"     Zweck: {desc}\n"
                 f"     Ladeverhalten: {hinweis}\n"
                 f"     Entsprechung bei Clients mit Ladetriggern: trigger: {trig}. -->\n\n")
    return kommentar + rumpf.lstrip("\n")


def render_root_instruction(text: str, man: dict) -> str:
    """Setzt an der Marke RUNTIME_IMPORTS die Einbindungen dieses Clients ein.

    Ein Client ohne Ladetrigger laedt Regeldateien nicht von sich aus; sie wirken erst
    durch eine Einbindung in der Wurzel-Anweisung. Welche das sind, steht im Manifest.
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
    abbildung = fmt.get("tool_names", {})
    ziel: list[str] = []
    for w in werkzeuge:
        for y in abbildung.get(w, [w]):
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


def render_for_client(text: str, man: dict, src_rel: str) -> str:
    """Waehlt die Transformation anhand der Quelle und loest danach die Platzhalter auf."""
    if src_rel == "framework/runtime/permissions.json":
        # Kennt der Client keine eigene Hook-Datei, wandern die Hooks hier mit hinein.
        hooks = (clientmap.load_source(HERE, "hooks.json")
                 if clientmap.hooks_in_permissions(man) else None)
        return clientmap.render_permissions(text, man, hooks)
    if src_rel == "framework/runtime/hooks.json":
        return clientmap.render_hooks(text, man)
    if os.path.basename(src_rel) == "SKILL.md":
        text = render_skill_frontmatter(text, man)
    elif src_rel.startswith("framework/runtime/rules/"):
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


def write_rendered(src: str, dst: str, man: dict, dry: bool) -> None:
    if dry:
        return
    text = render_for_client(read_text(src), man, quell_kennung(src))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def read_text(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def quell_kennung(src: str) -> str:
    """Pfad der Quelle relativ zum Kern - er entscheidet ueber die Formtransformation."""
    return os.path.relpath(src, HERE).replace(os.sep, "/")


def rendered_matches(src: str, dst: str, man: dict) -> bool:
    if not os.path.exists(dst):
        return False
    soll = render_for_client(read_text(src), man, quell_kennung(src))
    return read_text(dst) == soll


def copy_file(src: str, dst: str, dry: bool) -> None:
    if dry:
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)


def run(root: str, template: str, man: dict, mode: str, dry: bool) -> Report:
    rep = Report()

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
        if rendered_matches(src, dst, man):
            rep.unchanged.append(dst_rel)
        elif mode == "check":
            rep.drifted.append(f"{dst_rel}  (Pack-Quelle: {src_rel})")
        else:
            write_rendered(src, dst, man, dry)
            rep.updated.append(f"{dst_rel}  (aus dem Pack aktualisiert)")

    # Framework-Skills: eine Quelle, je Client gerendert.
    for src_rel, dst_rel in framework_skill_files(man):
        src = os.path.join(HERE, src_rel)
        dst = os.path.join(root, dst_rel)
        if not os.path.exists(dst):
            if mode == "check":
                rep.missing.append(dst_rel)
            else:
                write_rendered(src, dst, man, dry)
                rep.created.append(dst_rel)
        elif rendered_matches(src, dst, man):
            rep.unchanged.append(dst_rel)
        elif mode == "check":
            rep.drifted.append(f"{dst_rel}  (Quelle: {src_rel})")
        else:
            write_rendered(src, dst, man, dry)
            rep.updated.append(dst_rel)

    # Geteilte Core-Bestandteile aus dem Kern (Vorlagen, spaeter weitere).
    for src_rel, dst_rel in shared_files(man, "shared_core"):
        src = os.path.join(HERE, *src_rel.split("/"))
        dst = os.path.join(root, *dst_rel.split("/"))
        if not os.path.exists(dst):
            if mode == "check":
                rep.missing.append(dst_rel)
            else:
                write_rendered(src, dst, man, dry)
                rep.created.append(dst_rel)
        elif rendered_matches(src, dst, man):
            rep.unchanged.append(dst_rel)
        elif mode == "check":
            rep.drifted.append(f"{dst_rel}  (Quelle: {src_rel})")
        else:
            write_rendered(src, dst, man, dry)
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

    # Geteilte Saat aus dem Kern: einmal angelegt, danach Eigentum des Projekts.
    for src_rel, dst_rel in shared_files(man, "shared_seed"):
        src = os.path.join(HERE, *src_rel.split("/"))
        dst = os.path.join(root, *dst_rel.split("/"))
        if os.path.exists(dst):
            rep.kept.append(dst_rel)
        elif mode == "check":
            rep.missing.append(dst_rel)
        else:
            write_rendered(src, dst, man, dry)
            rep.created.append(dst_rel)

    return rep


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Installiert die Wurzeldateien des Devin Desktop Frameworks in ein Projekt.")
    ap.add_argument("--root", default=os.getcwd(),
                    help="Wurzelverzeichnis des Projekts (Standard: aktuelles Verzeichnis)")
    ap.add_argument("--update", action="store_true",
                    help="Core-Dateien auf den Stand dieses Releases bringen; Projektdateien bleiben unberuehrt")
    ap.add_argument("--check", action="store_true",
                    help="Nur pruefen: meldet fehlende und abweichende Core-Dateien, schreibt nichts")
    ap.add_argument("--dry-run", action="store_true",
                    help="Zeigen, was geschehen wuerde, ohne zu schreiben")
    ap.add_argument("--client", default=DEFAULT_CLIENT,
                    help=f"Client Pack, aus dem installiert wird (Standard: {DEFAULT_CLIENT})")
    ap.add_argument("--list-clients", action="store_true",
                    help="Verfuegbare Client Packs auflisten und beenden")
    args = ap.parse_args()

    clients = available_clients()

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
        print("devin-core-framework/clients/<name>/CLIENT_PACK.md.")
        return 0

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

    root = os.path.abspath(args.root)
    if os.path.abspath(HERE) == root:
        print("FEHLER: --root zeigt auf devin-core-framework/ selbst. Gemeint ist das "
              "Wurzelverzeichnis des Projekts, also eine Ebene darueber.", file=sys.stderr)
        return 1

    mode = "check" if args.check else ("update" if args.update else "install")
    version_file = os.path.join(HERE, "VERSION")
    version = open(version_file, encoding="utf-8").read().strip() if os.path.exists(version_file) else "unbekannt"

    print(f"Framework {version}")
    print(f"Client:  {args.client}")
    print(f"Vorlage: {os.path.relpath(template, root) if root in template else template}")
    print(f"Ziel:    {root}")
    print(f"Modus:   {mode}{'  (dry-run, es wird nichts geschrieben)' if args.dry_run else ''}")
    print()

    rep = run(root, template, man, mode, args.dry_run)

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
            print(f"Core-Aenderungen gehoeren in devin-core-framework/{tpl_rel}/ und laufen")
            print("als Aenderungsantrag (devin-core-framework/governance/FEEDBACK_PROCESS.md).")
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
        print("  1. project-overlay/OVERLAY.md ausfuellen (Platzhalter und <TBD>-Felder).")
        print(f"  2. Werte in {man['permissions_file']} eintragen - die Kernregeln unter")
        print("     _core_rules_integrity nicht entfernen.")
        print("  3. project-overlay/forbidden-terms.txt mit den realen Projekt- und")
        print("     Kundennamen fuellen (bleibt projektlokal).")
        print("  4. devin-core-framework/checklists/10-project-adoption.md abarbeiten.")
        print("  5. python devin-core-framework/tests/scripts/validate-framework.py --strict-overlay")
    if mode == "update":
        print()
        print(f"Hinweis: {man['permissions_file']} wurde nicht angefasst, weil sie Projektwerte enthaelt.")
        print("Pruefe nach einem Release-Wechsel, ob die Kernregeln noch vollstaendig sind:")
        print("  python devin-core-framework/tests/scripts/validate-framework.py --strict-overlay")

    print()
    print("Diese Pfade gehoeren dem Projekt und werden von install.py nie geschrieben:")
    for hint in man.get("project_owned_hint", []):
        print(f"  {hint}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
