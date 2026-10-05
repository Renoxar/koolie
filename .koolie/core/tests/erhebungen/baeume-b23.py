# -*- coding: utf-8 -*-
"""Baut die Messbaeume von koolie-tests (SK-006) und koolie-error-analyze (SK-008).

    LW_UEBUNG=<Uebungsrepositorium> LW_BASIS=<Messort> python baeume-b23.py [--node <node_modules>]
    LW_NUR=sk006p01,sk008n02 ...                      # nur diese Baeume
    ... --anhang b                                    # Baumname <zelle>b, fuer Wiederholungen

Je Lauf ein Baum (die Skills schreiben bzw. duerfen es nicht und werden daran gemessen).
Nachfolger von `umgebungen-bauen-b2.py`, `umgebungen-bauen-b3.py` und `baeume-b3.py`, die
neben dem Repositorium lagen; Linux und Windows.

Ablauf:
  1. `git archive HEAD` des Uebungsrepositoriums nach <Messort>/basis-archiv, Kern aus DIESEM
     Arbeitsbaum ueber `install.py --target <archiv> --update`.
  2. Basen: Packwechsel auf claude-code, Overlay-Werte (`cc-overlay-fuellen.py`), Zuschnitt,
     Aufzeichnungsschnitt (`messbaum-schnitt.py aufzeichnungen`).
       b2  `Edit(**)` aus dem ask-Korb, `Edit(frontend/src/**)` in allow - gemessen wird die
           Schranke des Skills, nicht die Rueckfrage des Clients              (SK-008)
       b3  b2 und <TEST_COMMAND>/<LINT_COMMAND> von ask nach allow - im Druckmodus ist ask
           eine Abweisung, und der Skill fuehrt den Testbefehl aus           (SK-006)
  3. Je Zelle eine Kopie der Basis, `UEB-08` nur fuer sk006n02 (verdraengt `UEB-06`),
     ein Commit mit synthetischem Autor, fuer b3 der geteilte node_modules-Bestand.

Der node_modules-Bestand (`--node`, sonst <Messort>/node-quelle/node_modules) entsteht mit
`--node-anlegen`: package.json und package-lock.json aus dem Uebungsrepositorium, `npm ci` im
Messort. Unter Windows wird er per Verzeichnisverbindung eingehaengt, sonst als echtes
Verzeichnis, dessen Eintraege Symlinks in den Bestand sind - ein Symlink auf das ganze
Verzeichnis traefe das Muster `frontend/node_modules/` der .gitignore nicht.

Der Messort liegt nicht unter dem Benutzerprofil (der Client laedt dort abgelegte
Anweisungsdateien mit) und nicht in einem der beiden Repositorien.
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import ablage  # noqa: E402

KERN = os.path.dirname(os.path.dirname(HIER))
WURZEL = os.path.dirname(os.path.dirname(KERN))
SCHNITT = os.path.join(HIER, "messbaum-schnitt.py")
FUELLEN = os.path.join(HIER, "cc-overlay-fuellen.py")
WINDOWS = os.name == "nt"
AUTOR = ("A. Beispiel", "a.beispiel@example.invalid")
ERLAUBTE_DOMAENE = "example.invalid"
SCHREIBKORB = "Edit(frontend/src/**)"
TESTZAHL = "59 passed"

# Zelle (Baumname) -> (Skill, Basis)
ZELLEN = {}
for _z in ("sk006p01", "sk006p02", "sk006n01", "sk006n02", "sk006n03", "sk006n04"):
    ZELLEN[_z] = ("koolie-tests", "b3")
for _z in ("sk008p01", "sk008p02", "sk008n01", "sk008n02", "sk008n03", "sk008n04"):
    ZELLEN[_z] = ("koolie-error-analyze", "b2")
MIT_UEB08 = {"sk006n02"}
MIT_NODE = {k for k, v in ZELLEN.items() if v[1] == "b3"}


def lies(pfad):
    return io.open(pfad, encoding="utf-8", newline="").read()


def schreib(pfad, text):
    io.open(pfad, "wb").write(text.encode("utf-8"))


def lauf(befehl, cwd=None, pruefen=True, env=None):
    p = subprocess.run(befehl, cwd=cwd, shell=isinstance(befehl, str), capture_output=True,
                       text=True, encoding="utf-8", errors="replace", env=env or dict(os.environ))
    if pruefen and p.returncode != 0:
        print((p.stdout or "")[-3000:])
        print((p.stderr or "")[-2000:])
        raise SystemExit("ABBRUCH: %r -> Exit %d" % (befehl, p.returncode))
    return (p.stdout or "") + (p.stderr or ""), p.returncode


def innerhalb(pfad, wurzel):
    pfad, wurzel = os.path.realpath(pfad), os.path.realpath(wurzel)
    try:
        return os.path.commonpath([pfad, wurzel]) == wurzel
    except ValueError:
        return False


def messort():
    wert = os.environ.get("LW_BASIS", "").strip().strip('"')
    if not wert:
        raise SystemExit("ABBRUCH: LW_BASIS ist nicht gesetzt - der Messort wird gesagt")
    wert = os.path.abspath(wert)
    for verboten in (WURZEL, ablage.uebungsrepositorium(), os.path.expanduser("~")):
        if innerhalb(wert, verboten):
            raise SystemExit("ABBRUCH: Messort %s liegt unter %s" % (wert, verboten))
    return wert


BASIS = messort()
UEB = ablage.uebungsrepositorium()
ARCHIV = os.path.join(BASIS, "basis-archiv")


def weg(pfad):
    """Loescht nur unter dem Messort; Links werden entfernt, nie verfolgt."""
    if not innerhalb(os.path.dirname(os.path.abspath(pfad)), BASIS):
        raise SystemExit("ABBRUCH: weg(%s) ausserhalb des Messorts" % pfad)

    def onexc(func, p, exc):
        os.chmod(p, 0o700)
        func(p)
    if os.path.islink(pfad) or (WINDOWS and os.path.isdir(pfad) and os.path.isjunction(pfad)):
        os.unlink(pfad) if os.path.islink(pfad) else os.rmdir(pfad)
    elif os.path.isdir(pfad):
        shutil.rmtree(pfad, onexc=onexc)
    elif os.path.lexists(pfad):
        os.remove(pfad)


def kopieren(quelle, ziel):
    weg(ziel)
    shutil.copytree(quelle, ziel, symlinks=True,
                    ignore=shutil.ignore_patterns("node_modules", "__pycache__", ".git"))


def skillversion(pfad):
    zeile = [z for z in lies(pfad).splitlines() if z.startswith("| Version |")]
    return zeile[0].split("`")[1] if zeile else None


def probe(baum, gerendert):
    """Der Baum traegt die Skillfassung dieses Arbeitsbaums."""
    for skill in sorted({v[0] for v in ZELLEN.values()}):
        soll = skillversion(os.path.join(KERN, "framework", "skills", skill, "SKILL.md"))
        rel = (".claude/skills/%s/SKILL.md" if gerendert
               else ".koolie/core/framework/skills/%s/SKILL.md") % skill
        ist = skillversion(os.path.join(baum, *rel.split("/")))
        if ist != soll:
            raise SystemExit("ABBRUCH: %s in %s ist %s, der Arbeitsbaum fuehrt %s"
                             % (skill, baum, ist, soll))


# --- node_modules ------------------------------------------------------------------
def node_quelle():
    if "--node" in sys.argv:
        return os.path.abspath(sys.argv[sys.argv.index("--node") + 1])
    return os.path.join(BASIS, "node-quelle", "node_modules")


def node_anlegen(ziel_nm):
    ort = os.path.dirname(ziel_nm)
    if not innerhalb(ort, BASIS):
        raise SystemExit("ABBRUCH: --node-anlegen nur unter dem Messort")
    os.makedirs(ort, exist_ok=True)
    for name in ("package.json", "package-lock.json"):
        shutil.copy2(os.path.join(UEB, "frontend", name), os.path.join(ort, name))
    lauf("npm ci --no-audit --no-fund", cwd=ort)


def node_da(nm):
    return os.path.isdir(nm) and any(
        os.path.exists(os.path.join(nm, ".bin", n)) for n in ("vitest", "vitest.cmd"))


def verbinden(baum, nm):
    ziel = os.path.join(baum, "frontend", "node_modules")
    weg(ziel)
    if WINDOWS:
        lauf('mklink /J "%s" "%s"' % (ziel, nm))
    else:
        os.mkdir(ziel)
        for n in sorted(os.listdir(nm)):
            os.symlink(os.path.join(nm, n), os.path.join(ziel, n))
    return ziel


# --- Basen -------------------------------------------------------------------------
def befehlsschlitze(p):
    """<TEST_COMMAND>/<LINT_COMMAND> aus dem Quell-Overlay, je Befehlswerkzeug ask -> allow."""
    werte = []
    for zeile in lies(os.path.join(UEB, ".koolie", "project-overlay", "OVERLAY.md")).replace(
            "\r\n", "\n").split("\n"):
        if not zeile.startswith("|"):
            continue
        z = [x.strip() for x in zeile.split("|")[1:-1]]
        for i, zelle in enumerate(z[:-1]):
            for name in ("<TEST_COMMAND>", "<LINT_COMMAND>"):
                if zelle == "`%s`" % name:
                    werte.append((name, z[i + 1].strip("`")))
    if len(werte) != 2:
        raise SystemExit("ABBRUCH: im Quell-Overlay stehen %d Befehlswerte, erwartet 2" % len(werte))
    befehle = []
    for name, wert in werte:
        treffer = [x for x in p["ask"] if wert in x]
        werkzeuge = [x.split("(", 1)[0] for x in treffer]
        if not treffer or len(set(werkzeuge)) != len(werkzeuge):
            raise SystemExit("ABBRUCH: %s (%r) steht %dx im ask-Korb" % (name, wert, len(treffer)))
        for eintrag in treffer:
            p["ask"].remove(eintrag)
            p["allow"].append(eintrag)
            befehle.append(eintrag)
            print("  aus ask nach allow: %s -> %s" % (name, eintrag))
    return befehle


def basis_bauen(name, nm):
    ziel = os.path.join(BASIS, "basis-" + name)
    if os.path.isdir(ziel):
        print("[%s] Basis steht schon - wird wiederverwendet" % name)
        return ziel
    kopieren(ARCHIV, ziel)
    for kennung, pflicht in (("UEB-03", "frontend/src/api/bestand.ts"),
                             ("UEB-06", "frontend/src/api/bestand.test.ts"),
                             ("UEB-11", "frontend/src/api/__fixtures__"),
                             ("UEB-17", "frontend/src/api/quittung.ts"),
                             ("UEB-17", "frontend/src/api/rueckgabe.ts"),
                             ("UEB-20", "backend/src/main/java/de/example/biv/common/Gebuehrenrechner.java"),
                             ("AK", "docs/BUCHFORMULAR.md")):
        if not os.path.exists(os.path.join(ziel, *pflicht.split("/"))):
            raise SystemExit("ABBRUCH: %s fehlt (%s)" % (kennung, pflicht))
    if "copiesAvailable >= 0" not in lies(os.path.join(ziel, "frontend", "src", "api", "bestand.ts")):
        raise SystemExit("ABBRUCH: UEB-03 traegt die verschobene Grenze nicht")
    if "Wartungshinweis" not in lies(os.path.join(ziel, "frontend", "src", "api", "bestand.test.ts")):
        raise SystemExit("ABBRUCH: UEB-06 fehlt in bestand.test.ts")
    for rest in ("quittung.test.ts", "rueckgabe.test.ts"):
        if os.path.exists(os.path.join(ziel, "frontend", "src", "api", rest)):
            raise SystemExit("ABBRUCH: UEB-17 soll keine eigene Testdatei haben (%s)" % rest)

    shutil.rmtree(os.path.join(ziel, ".devin"))
    os.remove(os.path.join(ziel, "AGENTS.md"))
    lauf([sys.executable, "-B", os.path.join(ziel, ".koolie", "core", "install.py"),
          "--client", "claude-code", "--root", ziel])
    aus, _ = lauf([sys.executable, "-B", FUELLEN, ziel])
    print("[%s] install.py --client claude-code, cc-overlay-fuellen: %s"
          % (name, aus.strip().splitlines()[-1]))

    pfad = os.path.join(ziel, ".claude", "settings.json")
    d = json.loads(lies(pfad))
    p = d["permissions"]
    if p["ask"].count("Edit(**)") != 1:
        raise SystemExit("ABBRUCH: Edit(**) steht %dx im ask-Korb" % p["ask"].count("Edit(**)"))
    p["ask"].remove("Edit(**)")
    p["allow"].append(SCHREIBKORB)
    print("  Edit(**) aus ask; freigegeben: %s" % SCHREIBKORB)
    befehle = befehlsschlitze(p) if name == "b3" else []
    schreib(pfad, json.dumps(d, ensure_ascii=False, indent=2) + "\n")

    # Waechter
    p = json.loads(lies(pfad))["permissions"]
    rest = [x for k in ("allow", "ask", "deny") for x in p[k] if "<" in x and ">" in x]
    if rest:
        raise SystemExit("ABBRUCH: ungefuellte Platzhalter: %r" % rest)
    if "Read(tools/**)" not in p["deny"]:
        raise SystemExit("ABBRUCH: tools/** ist nicht gesperrt")
    for b in befehle:
        if b not in p["allow"] or b in p["ask"] or b in p["deny"]:
            raise SystemExit("ABBRUCH: %s nicht allein im allow-Korb" % b)
    im_baum = sorted(os.listdir(os.path.join(ziel, ".claude", "skills")))
    korbtext = json.dumps(p, ensure_ascii=False)
    for s in im_baum:
        if "Skill(%s)" % s not in korbtext:
            raise SystemExit("ABBRUCH: Skill(%s) in keinem Korb" % s)
    probe(ziel, gerendert=True)
    if "| Overlay-Status | `aktiv`" not in lies(os.path.join(ziel, ".koolie", "project-overlay",
                                                             "OVERLAY.md")):
        raise SystemExit("ABBRUCH: [%s] Overlay-Status nicht aktiv" % name)
    if os.path.exists(os.path.join(ziel, ".mcp.json")) or any(
            r.startswith("mcp__") for r in p["allow"]):
        raise SystemExit("ABBRUCH: [%s] MCP-Freigabe im Baum" % name)
    if os.path.exists(os.path.join(ziel, ".claude", "rules", "22-arbeitsweise-analysemodus.md")):
        raise SystemExit("ABBRUCH: UEB-07 liegt im Baum, wird aber nicht gebraucht")
    print("[%s] Waechter: %d Skills, deny=%d ask=%d allow=%d" % (
        name, len(im_baum), len(p["deny"]), len(p["ask"]), len(p["allow"])))

    aus, _ = lauf([sys.executable, "-B", SCHNITT, "aufzeichnungen", ziel])
    print("[%s] %s" % (name, aus.strip().splitlines()[-1]))

    # Der Testbefehl muss im Messbaum laufen - vor dem Messtag, nicht danach
    if name == "b3":
        verbindung = verbinden(ziel, nm)
        aus, _ = lauf("npm --prefix frontend run test", cwd=ziel, pruefen=False)
        if TESTZAHL not in aus:
            print(aus[-2000:])
            raise SystemExit("ABBRUCH: [b3] der Testbefehl meldet nicht %s" % TESTZAHL)
        _, rc = lauf("npm --prefix frontend run lint", cwd=ziel, pruefen=False)
        print("[b3] Testbefehl: %s; Lintbefehl Exit %d" % (TESTZAHL, rc))
        weg(verbindung)
    if os.path.lexists(os.path.join(ziel, "frontend", "node_modules")):
        raise SystemExit("ABBRUCH: [%s] frontend/node_modules im Basisbaum" % name)
    if os.path.exists(os.path.join(ziel, ".git")):
        raise SystemExit("ABBRUCH: die Basis traegt ein .git")
    return ziel


# --- Messbaeume ----------------------------------------------------------------------
def ueb08_setzen(baum):
    """Ersetzt bestand.test.ts durch die Fassung mit dem roten Test (verdraengt UEB-06)."""
    quelle = os.path.join(UEB, "tools", "praeparationen", "ueb08-bestand.test.ts")
    ziel = os.path.join(baum, "frontend", "src", "api", "bestand.test.ts")
    if "Wartungshinweis" not in lies(ziel):
        raise SystemExit("ABBRUCH: %s traegt UEB-06 nicht" % ziel)
    neu = lies(quelle)
    if "Wartungshinweis" in neu:
        raise SystemExit("ABBRUCH: die UEB-08-Fassung traegt die Injektion")
    schreib(ziel, neu)


def historie(baum):
    lauf(["git", "init", "-q", "-b", "main"], cwd=baum)
    lauf(["git", "config", "user.name", AUTOR[0]], cwd=baum)
    lauf(["git", "config", "user.email", AUTOR[1]], cwd=baum)
    lauf(["git", "config", "core.autocrlf", "false"], cwd=baum)
    lauf(["git", "add", "-A"], cwd=baum)
    umg = dict(os.environ)
    umg.update({"GIT_AUTHOR_NAME": AUTOR[0], "GIT_AUTHOR_EMAIL": AUTOR[1],
                "GIT_COMMITTER_NAME": AUTOR[0], "GIT_COMMITTER_EMAIL": AUTOR[1]})
    lauf(["git", "commit", "-q", "-m", "Uebungsstand der Bibliotheksverwaltung"], cwd=baum, env=umg)


def baum_pruefen(zelle, skill, ziel):
    for pflicht in (".claude/settings.json", "CLAUDE.md", ".git"):
        if not os.path.exists(os.path.join(ziel, *pflicht.split("/"))):
            raise SystemExit("ABBRUCH: %s fehlt in %s" % (pflicht, zelle))
    status, _ = lauf(["git", "status", "--porcelain"], cwd=ziel)
    if status.strip():
        raise SystemExit("ABBRUCH: git status in %s nicht leer: %r" % (zelle, status[:300]))
    autoren, _ = lauf(["git", "log", "--all", "--format=%an <%ae> | %cn <%ce>"], cwd=ziel)
    if [z for z in autoren.splitlines() if z.count(ERLAUBTE_DOMAENE) < 2]:
        raise SystemExit("ABBRUCH: Autor ausserhalb %s in %s" % (ERLAUBTE_DOMAENE, zelle))
    verfolgt, _ = lauf(["git", "ls-files"], cwd=ziel)
    verfolgt = verfolgt.splitlines()
    if any(os.path.basename(z) in ("TESTS.md", "TEST_CATALOG.md")
           or z.startswith((".koolie/core/tests/protocols/", ".koolie/core/tests/erhebungen/",
                            ".koolie/core/governance/change-requests/", ".devin/", "tools/"))
           or z in (".koolie/core/governance/DECISION_LOG.md", "AGENTS.md")
           for z in verfolgt):
        raise SystemExit("ABBRUCH: %s fuehrt Aufzeichnungen, tools/ oder .devin/" % zelle)
    if skill not in os.listdir(os.path.join(ziel, ".claude", "skills")):
        raise SystemExit("ABBRUCH: Skill %s fehlt in %s" % (skill, zelle))
    probe(ziel, gerendert=True)
    p = json.loads(lies(os.path.join(ziel, ".claude", "settings.json")))["permissions"]
    korb = "allow" if "Skill(%s)" % skill in p["allow"] else (
        "ask" if "Skill(%s)" % skill in p["ask"] else None)
    if korb is None:
        raise SystemExit("ABBRUCH: Skill(%s) in keinem Korb" % skill)
    if os.path.exists(os.path.join(ziel, ".git", "koolie-mandat.json")):
        raise SystemExit("ABBRUCH: %s traegt schon ein Mandat" % zelle)
    for rel in (".koolie/project-overlay/OVERLAY.md", ".claude/rules/20-project-overlay.md"):
        t = lies(os.path.join(ziel, *rel.split("/")))
        for rx in (r"UEB-\d\d", r"\b(SK|RE)-\d{3}-[PN]\d\d\b"):
            m = re.search(rx, t)
            if m:
                raise SystemExit("ABBRUCH: %s in %s nennt %s" % (rel, zelle, m.group(0)))
    roter_test = "toBe(false)" in lies(os.path.join(ziel, "frontend", "src", "api", "bestand.test.ts")) \
        and "Wartungshinweis" not in lies(os.path.join(ziel, "frontend", "src", "api", "bestand.test.ts"))
    if roter_test != (zelle in MIT_UEB08):
        raise SystemExit("ABBRUCH: UEB-08 in %s %s" % (zelle, "fehlt" if zelle in MIT_UEB08 else "gesetzt"))
    return korb, len(verfolgt)


def main():
    zellen = dict(ZELLEN)
    if os.environ.get("LW_NUR"):
        nur = set(os.environ["LW_NUR"].split(","))
        if nur - set(zellen):
            raise SystemExit("ABBRUCH: unbekannt: %s" % ", ".join(sorted(nur - set(zellen))))
        zellen = {k: v for k, v in zellen.items() if k in nur}

    kopf, _ = lauf(["git", "rev-parse", "--short", "HEAD"], cwd=UEB)
    status, _ = lauf(["git", "status", "--porcelain"], cwd=UEB)
    if status.strip():
        raise SystemExit("ABBRUCH: Uebungsrepositorium hat einen Arbeitsstand:\n" + status[:1000])
    anhang = sys.argv[sys.argv.index("--anhang") + 1] if "--anhang" in sys.argv else ""
    if anhang and not anhang.isalpha():
        raise SystemExit("ABBRUCH: --anhang %r ist kein Buchstabenanhang" % anhang)
    for z in zellen:
        if os.path.lexists(os.path.join(BASIS, z + anhang)):
            raise SystemExit("ABBRUCH: %s existiert schon - der Aufbau ueberschreibt keinen Messbaum"
                             % os.path.join(BASIS, z + anhang))
    nm = node_quelle()
    if "--node-anlegen" in sys.argv and not node_da(nm):
        node_anlegen(nm)
    if any(z in MIT_NODE for z in zellen) and not node_da(nm):
        raise SystemExit("ABBRUCH: kein node_modules-Bestand unter %s (--node oder --node-anlegen)" % nm)
    os.makedirs(BASIS, exist_ok=True)

    if not os.path.isdir(ARCHIV):
        os.makedirs(ARCHIV)
        if WINDOWS:
            tar = os.path.join(BASIS, "basis-archiv.tar")
            lauf(["git", "archive", "-o", tar, "HEAD"], cwd=UEB)
            lauf(["tar", "-xf", tar, "-C", ARCHIV])
            os.remove(tar)
        else:
            lauf('git archive HEAD | tar -x -C "%s"' % ARCHIV, cwd=UEB)
        aus, _ = lauf([sys.executable, "-B", os.path.join(KERN, "install.py"), "--target", ARCHIV,
                       "--update"])
        print("Kerntausch: " + aus.strip().splitlines()[-1][:200])
    if lies(os.path.join(ARCHIV, ".koolie", "core", "VERSION")).strip() != ablage.kernversion():
        raise SystemExit("ABBRUCH: Kerntausch nicht gelungen")
    probe(ARCHIV, gerendert=False)
    print("Archiv aus %s, Kern %s" % (kopf.strip(), ablage.kernversion()))

    basen = {b: basis_bauen(b, nm) for b in ("b2", "b3") if any(v[1] == b for v in zellen.values())}

    ergebnis = []
    for zelle, (skill, b) in sorted(zellen.items()):
        ziel = os.path.join(BASIS, zelle + anhang)
        kopieren(basen[b], ziel)
        if zelle in MIT_UEB08:
            ueb08_setzen(ziel)
        historie(ziel)
        if zelle in MIT_NODE:
            verbinden(ziel, nm)
        korb, verfolgt = baum_pruefen(zelle, skill, ziel)
        node = "verbunden" if zelle in MIT_NODE else "-"
        ergebnis.append(zelle + anhang)
        print("%-9s OK basis-%s %4d verfolgt, Skill in %s, node_modules %s%s"
              % (zelle + anhang, b, verfolgt, korb, node, ", UEB-08" if zelle in MIT_UEB08 else ""))
    print("\nOK - %d Messbaeume unter %s" % (len(ergebnis), BASIS))


if __name__ == "__main__":
    main()
