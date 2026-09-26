# -*- coding: utf-8 -*-
"""Zwei Schnitte an einem Messbaum, je mit Waechter (seit 1.14.1, K-167, D-425).

Aufruf:  python messbaum-schnitt.py aufzeichnungen <baum>
         python messbaum-schnitt.py ohneskill <baum> <skill> [<skill> ...]

`aufzeichnungen` - fuer JEDEN Messbaum, Haupt- wie Kontrolllauf, und vor jedem
    Zuschnitt. Nimmt heraus, was die Praeparationen und die Erwartungen der Zellen
    beschreibt: Antraege, Protokolle, Testblaetter, Testkatalog, Koederregister,
    Chronik, Mentorenblatt. 🔴 Gemessen im Nachlauf von 1.14.0: Eine Suche ueber das
    Repositorium fand in einem Aenderungsantrag die Beschreibung des Koeders `UEB-05`,
    und der Lauf stuetzte seine Einstufung darauf. Bei der Vorpruefung von 1.14.1 lag
    das Koederregister vollstaendig in `onboarding/exercises/README.md`, und jedes
    `TESTS.md` nannte die Erwartung der Zelle, die gerade lief.
    Die Trennlinie ist die von D-141: geschnitten wird AUFZEICHNUNG, nicht Regel. Ein
    Messbaum braucht die Regelschicht; er braucht nicht die Geschichte, wie sie
    gemessen wurde.

`ohneskill` - der Kontrollzuschnitt ohne den Skill. 🔴 Bis 1.14.0 leerte er nur die
    Laufzeitablage `.claude/skills/`; die Kernfassung unter
    `.koolie/core/framework/skills/` blieb lesbar, und `ksk004p01` baute den Plan
    aus ihr nach. Jetzt faellt beides. Der Waechter prueft nicht, ob die Verzeichnisse
    fehlen - das belegt sich selbst -, sondern ob ein Satz, der NUR in diesem Skill
    steht, irgendwo im Baum ueberlebt hat (dieselbe Lehre wie der Stammwaechter von
    D-205: gesucht wird nach dem, was die Schranke AUSMACHT).

Beide Schnitte brechen mit Exit 1 ab, wenn ihr Waechter etwas findet - ein Messbaum
mit Rest ist kein Messbaum (D-205).
"""
import io
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.dont_write_bytecode = True

# --- aufzeichnungen ------------------------------------------------------------------
WEG = [
    ".koolie/core/governance/change-requests",
    ".koolie/core/governance/DECISION_LOG.md",
    # Aus `tests/` nur, was Aufzeichnung oder Werkzeug der Framework-Entwicklung ist.
    # 🔴 Die Hook-Skripte der Laufzeitschicht liegen in `tests/scripts/` und bleiben -
    # gemessen am 2026-09-26: Der erste Schnitt nahm `tests/` ganz, und der Waechter des
    # Aufbaus fand zwei Hook-Befehle ohne Skript. Ein Messbaum ohne Schutz-Hook misst
    # einen anderen Client.
    ".koolie/core/tests/protocols",
    ".koolie/core/tests/erhebungen",
    ".koolie/core/tests/TEST_CATALOG.md",
    ".koolie/core/tests/scripts/probe-pruefungen.py",
    ".koolie/core/tests/scripts/validate-framework.py",
    ".koolie/core/tests/scripts/validate-output.py",
    ".koolie/core/build",
    ".koolie/core/CHANGELOG.md",
    ".koolie/core/docs/ROADMAP.md",
    ".koolie/core/onboarding/exercises/README.md",
    "tools/mentorenblatt",
    "tools/messbaum-b4",
    "tools/praeparationen",
    "tools/praeparationen.py",
]
# Jedes Testblatt, wo immer es liegt (Kern, Role Packs, gerenderte Ablage).
WEG_NAME = {"TESTS.md"}

# Zeilen, die fallen, ohne dass ihre Datei faellt: der Hinweis der Projekt-README auf
# das Mentorenblatt und die Zeilen des Overlay-Aenderungsverlaufs, die von Messungen
# erzaehlen. Das Overlay selbst ist Regelschicht und bleibt.
ZEILEN = {
    "README.md": [r"registrierte Präparationen", r"mentorenblatt"],
    ".koolie/project-overlay/OVERLAY.md": [
        r"^\|.*(UEB-\d\d|\b(SK|RE)-\d{3}-[PN]\d\d\b|Me(ß|ss)tag|Bündel|Nachlauf|Präparation)"],
}

# Was im geschnittenen Baum nicht mehr stehen darf: die Kennung einer Praeparation und
# die Kennung einer Zelle. ⚠️ Gemessen am 2026-09-26, bevor der Waechter so eng wurde:
# Die Woerter "Koeder", "Praeparation" und "Mentorenblatt" trafen 39 Zeilen - das
# Onboarding (drei allgemeine Koeder der Uebung Ü6), Code-Kommentare des
# Uebungsrepositoriums, die auf das gesperrte Mentorenblatt verweisen, und
# Hook-Beschreibungen der Client Packs. Keine nannte eine Praeparation oder eine Zelle,
# alle standen in jeder frueheren Messung; ein Waechter, der sie meldet, meldet Rauschen.
VERRAT = [
    re.compile(r"UEB-\d\d"),
    re.compile(r"\b(SK|RE)-\d{3}-[PN]\d\d\b"),
]
# `.env` IST die Praeparation `UEB-04` (Gegenstand der `deny`-Regel auf Secret-Dateien)
# und fuer den Lauf gesperrt; ihr Kopfkommentar nennt sich selbst.
AUSGENOMMEN = {".env"}
UEBERSPRINGEN = {".git", "node_modules"}


def dateien(wurzel):
    for d, unter, namen in os.walk(wurzel):
        unter[:] = [u for u in unter if u not in UEBERSPRINGEN]
        for n in namen:
            yield os.path.join(d, n)


def rel(wurzel, pfad):
    return os.path.relpath(pfad, wurzel).replace(os.sep, "/")


def weg(pfad):
    def onexc(func, p, exc):
        os.chmod(p, 0o700)
        func(p)
    if os.path.isdir(pfad):
        shutil.rmtree(pfad, onexc=onexc)
    elif os.path.lexists(pfad):
        os.remove(pfad)


def lies(pfad):
    try:
        return io.open(pfad, encoding="utf-8", newline="").read()
    except (UnicodeDecodeError, OSError):
        return None


def aufzeichnungen(baum):
    entfernt = 0
    for r in WEG:
        p = os.path.join(baum, *r.split("/"))
        if os.path.lexists(p):
            weg(p)
            entfernt += 1
            print("entfernt:", r)
    for p in list(dateien(baum)):
        if os.path.basename(p) in WEG_NAME:
            os.remove(p)
            entfernt += 1
    print("entfernt: %d Testblaetter und Ablagen insgesamt" % entfernt)

    for r, muster in ZEILEN.items():
        p = os.path.join(baum, *r.split("/"))
        text = lies(p)
        if text is None:
            continue
        nl = "\r\n" if "\r\n" in text else "\n"
        rx = [re.compile(m, re.IGNORECASE) for m in muster]
        alt = text.split(nl)
        neu = [z for z in alt if not any(x.search(z) for x in rx)]
        if len(neu) != len(alt):
            io.open(p, "wb").write(nl.join(neu).encode("utf-8"))
            print("Zeilen: %s - %d entfernt" % (r, len(alt) - len(neu)))

    # --- Waechter: nichts, was eine Praeparation oder eine Zelle verraet -------------
    rest = []
    for p in dateien(baum):
        r = rel(baum, p)
        if r in AUSGENOMMEN:
            continue
        text = lies(p)
        if text is None:
            continue
        for i, z in enumerate(text.splitlines(), 1):
            for x in VERRAT:
                if x.search(z):
                    rest.append("%s:%d  %s" % (r, i, z.strip()[:110]))
                    break
    if rest:
        print("Waechter: %d Fundstellen, die eine Praeparation oder Zelle verraten:" % len(rest))
        for z in rest[:40]:
            print("  " + z)
        raise SystemExit("ABBRUCH: der Baum verraet noch Praeparationen (%d Fundstellen)" % len(rest))
    print("Waechter aufzeichnungen: 0 Fundstellen (Kennung einer Praeparation "
          "oder einer Zelle)")


# --- ohneskill ---------------------------------------------------------------------------
SKILL_ABLAGEN = [".claude/skills", ".koolie/core/framework/skills"]
MINDESTLAENGE = 50


def stammsaetze(baum, skill):
    """Die Zeilen des Skills, die NIRGENDS SONST im Baum stehen.

    ⚠️ Gemessen am 2026-09-26: `fw-plan` zitiert die Kopfzeile der Planvorlage woertlich.
    Wer nur gegen die anderen Skills abgleicht, haelt sie fuer einen Stammsatz, und der
    Waechter meldet die Vorlage - Regelschicht, die der Kontrollbaum behalten muss.
    """
    kern = os.path.join(baum, ".koolie", "core", "framework", "skills")
    eigen = lies(os.path.join(kern, skill, "SKILL.md"))
    if eigen is None:
        raise SystemExit("ABBRUCH: %s/SKILL.md fehlt im Kern - nichts zu schneiden" % skill)
    eigene_ablagen = [os.path.join(baum, *r.split("/"), skill) for r in SKILL_ABLAGEN]
    fremd = set()
    for p in dateien(baum):
        if any(p.startswith(a + os.sep) for a in eigene_ablagen):
            continue
        t = lies(p)
        if t:
            fremd.update(z.strip() for z in t.splitlines())
    return [z.strip() for z in eigen.splitlines()
            if len(z.strip()) >= MINDESTLAENGE and z.strip() not in fremd]


def ohneskill(baum, skills):
    stamm = {}
    for skill in skills:
        stamm[skill] = stammsaetze(baum, skill)
        if not stamm[skill]:
            raise SystemExit("ABBRUCH: kein Stammsatz fuer %s - der Waechter haette nichts zu suchen" % skill)
    for r in SKILL_ABLAGEN:
        ablage = os.path.join(baum, *r.split("/"))
        if not os.path.isdir(ablage):
            continue
        for n in sorted(os.listdir(ablage)):
            weg(os.path.join(ablage, n))
        print("entfernt: %s/* (alle Skills)" % r)
    for pflicht in ("CLAUDE.md", ".claude/rules/00-framework-core.md"):
        if not os.path.isfile(os.path.join(baum, *pflicht.split("/"))):
            raise SystemExit("ABBRUCH: %s fehlt - die Regelschicht ist mitgefallen" % pflicht)

    rest = []
    for p in dateien(baum):
        text = lies(p)
        if not text:
            continue
        for skill, saetze in stamm.items():
            for s in saetze:
                if s in text:
                    rest.append("%s  %s  %s" % (skill, rel(baum, p), s[:80]))
    if rest:
        print("Waechter: %d Stammsaetze ueberleben:" % len(rest))
        for z in rest[:20]:
            print("  " + z)
        raise SystemExit("ABBRUCH: %d Stammsaetze im Baum" % len(rest))
    for skill, saetze in stamm.items():
        print("Waechter ohneskill: %d Stammsaetze von %s, keiner im Baum" % (len(saetze), skill))
    print("Regelschicht steht (CLAUDE.md, 00-framework-core.md)")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "aufzeichnungen":
        aufzeichnungen(os.path.abspath(sys.argv[2]))
    elif len(sys.argv) >= 4 and sys.argv[1] == "ohneskill":
        ohneskill(os.path.abspath(sys.argv[2]), sys.argv[3:])
    else:
        raise SystemExit(__doc__.split("\n\n")[1])
