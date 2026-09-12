#!/usr/bin/env python3
"""
install.py - Legt die Wurzeldateien des Leitwerk-Frameworks in einem Projekt an.

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

    python leitwerk-core/install.py                        # Erstinstallation, Standard-Client
    python leitwerk-core/install.py --client <name>        # anderer Client
    python leitwerk-core/install.py --list-clients         # verfuegbare Client Packs
    python leitwerk-core/install.py --update               # Core aktualisieren
    python leitwerk-core/install.py --check                # nur pruefen, nichts schreiben
    python leitwerk-core/install.py --dry-run              # zeigen, was passieren wuerde

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
#                 (leitwerk-core/governance/FEEDBACK_PROCESS.md).
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
    feld = fmt.get("model_invocation_field")
    nur_nutzer = False
    if feld:
        m = re.search(r"^triggers:[ \t]*\n((?:[ \t]+-[ \t]+\S+[ \t]*\n)+)", fm, re.M)
        ausloeser = [x.strip("- \t") for x in m.group(1).strip().split("\n")] if m else []
        nur_nutzer = bool(ausloeser) and "model" not in ausloeser

    if fmt.get("tools_format") == "csv":
        m = re.search(r"^allowed-tools:[ \t]*\n((?:[ \t]+-[ \t]+\S+[ \t]*\n)+)", fm, re.M)
        werkzeuge = [x.strip("- \t") for x in m.group(1).strip().split("\n")] if m else []
        abbildung = fmt.get("tool_names", {})
        ziel: list[str] = []
        for w in werkzeuge:
            for y in abbildung.get(w, [w]):
                if y not in ziel:
                    ziel.append(y)
        for f in ["allowed-tools"] + list(fmt.get("drop_fields", [])):
            fm = re.sub(rf"^{f}:.*\n(?:[ \t]+\S.*\n)*", "", fm, flags=re.M)
        if ziel:
            fm = fm.rstrip("\n") + f"\nallowed-tools: {', '.join(ziel)}\n"
    else:
        for f in fmt.get("drop_fields", []):
            fm = re.sub(rf"^{f}:.*\n(?:[ \t]+\S.*\n)*", "", fm, flags=re.M)

    if nur_nutzer:
        fm = fm.rstrip("\n") + f"\n{feld}: true\n"

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
        kopfzeilen = "---\n" + f"{feld}:\n" + "".join(f'  - "{w}"\n' for w in muster) + "---\n\n"
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


def pruefe_abbildung(root: str, man: dict) -> None:
    """Rendert jede abzubildende Quelle einmal, bevor die erste Datei geschrieben wird.

    D-26 verlangt, dass die Installation scheitert, wenn eine Aussage der Quelle sich
    nicht abbilden laesst. Ohne diesen Vorlauf scheiterte sie mitten im Schreiben und
    hinterliess ein halb angelegtes Projekt - gescheitert ist das eine, halb gelungen
    das andere. Der Vorlauf kostet einen zweiten Rendervorgang und keine Schreiboperation.
    """
    quellen = [s for s, _ in activated_pack_relpaths(root, man)]
    quellen += [s for s, _ in framework_skill_files(man)]
    for schluessel in ("shared_core", "shared_seed"):
        quellen += [s for s, _ in shared_files(man, schluessel)]
    for src_rel in quellen:
        src = os.path.join(HERE, *src_rel.split("/"))
        render_for_client(read_text(src), man, quell_kennung(src))


def run(root: str, template: str, man: dict, mode: str, dry: bool) -> Report:
    rep = Report()
    pruefe_abbildung(root, man)

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


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Installiert die Wurzeldateien des Leitwerk-Frameworks in ein Projekt.")
    ap.add_argument("--root", default=os.getcwd(),
                    help="Wurzelverzeichnis des Projekts (Standard: aktuelles Verzeichnis)")
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
        print("leitwerk-core/clients/<name>/CLIENT_PACK.md.")
        return 0

    # Das Ziel steht vor der Clientwahl fest - denn es entscheidet sie.
    root = os.path.abspath(args.root)
    if os.path.abspath(HERE) == root:
        print("FEHLER: --root zeigt auf leitwerk-core/ selbst. Gemeint ist das "
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
                  "project-overlay/OVERLAY.md,\nprojektspezifische Regeln in eine Regeldatei "
                  "2N-overlay-<name>.md. Danach die\nDatei entfernen und erneut aufrufen "
                  "(leitwerk-core/docs/ADOPTION_GUIDE.md, Abschnitt 2).", file=sys.stderr)
            return 1
    version_file = os.path.join(HERE, "VERSION")
    version = open(version_file, encoding="utf-8").read().strip() if os.path.exists(version_file) else "unbekannt"

    print(f"Framework {version}")
    print(f"Client:  {args.client}")
    print(f"Vorlage: {os.path.relpath(template, root) if root in template else template}")
    print(f"Ziel:    {root}")
    print(f"Modus:   {mode}{'  (dry-run, es wird nichts geschrieben)' if args.dry_run else ''}")
    print()

    try:
        rep = run(root, template, man, mode, args.dry_run)
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
            print(f"Core-Aenderungen gehoeren in leitwerk-core/{tpl_rel}/ und laufen")
            print("als Aenderungsantrag (leitwerk-core/governance/FEEDBACK_PROCESS.md).")
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
        print("  4. leitwerk-core/checklists/10-project-adoption.md abarbeiten.")
        print("  5. python leitwerk-core/tests/scripts/validate-framework.py --strict-overlay")
    if mode == "update":
        print()
        print(f"Hinweis: {man['permissions_file']} wurde nicht angefasst, weil sie Projektwerte enthaelt.")
        print("Pruefe nach einem Release-Wechsel, ob die Kernregeln noch vollstaendig sind:")
        print("  python leitwerk-core/tests/scripts/validate-framework.py --strict-overlay")

    print()
    print("Diese Pfade gehoeren dem Projekt und werden von install.py nie geschrieben:")
    for hint in man.get("project_owned_hint", []):
        print(f"  {hint}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
