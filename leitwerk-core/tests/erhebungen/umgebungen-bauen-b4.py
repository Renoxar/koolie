# -*- coding: utf-8 -*-
"""Baut den BASISBAUM des vierten Testblatt-Buendels unter C:\\lw-b4.

    python umgebungen-bauen-b4.py [--erwarte <version>]

Ergebnis: C:\\lw-b4\\basis - eine vollstaendige claude-code-Installation des
Uebungsrepositoriums, OHNE `.git` und OHNE die Verzeichnisverbindung auf
`node_modules`. Beides kommt je Baum dazu (`baeume-b4.py`).

🔴 WARUM DIESER BAUM KEIN `.git` HAT - D-213, der teuerste Befund von 0.78.0.
Die README von Buendel 4 schrieb die Reihenfolge *Historie -> Packwechsel* vor.
In dieser Reihenfolge committet der Baumbau den Stand VOR dem Packwechsel - und
der Packwechsel loescht danach `.devin/`, das im Uebungsrepositorium VERSIONIERT
ist. Gemessen am 2026-09-20 an `SK-010-P02`, beide Wege am selben Baum:

    Historie zuerst:      79 Eintraege in `git status` (73 D, 4 ??, 2 M)
    Packwechsel zuerst:    2 Eintraege - genau der Aenderungssatz

73 geloeschte Regeldateien eines FREMDEN Client Packs sagen jedem Lauf, dass hier
gewechselt wurde - und jede der neunzehn Zellen liest `git status`. Das ist D-179
(*ein Kontrollbaum darf nicht sagen, dass er einer ist*) an einer neuen Stelle:
Dort war es ein Kommentar, hier ist es die Historie.

  Wer einen Messbaum mit Historie baut, fragt nicht nur, was in den DATEIEN
  steht, sondern was der ERSTE COMMIT enthaelt.

Richtige Reihenfolge, die dieses Skript und `baeume-b4.py` einhalten:
archivieren -> Packwechsel -> `install.py` -> Befehlskoerbe -> (Zuschnitt) ->
HISTORIE -> `node_modules` verbinden.
"""
import argparse
import io
import json
import os
import shutil
import subprocess
import sys

import ablage
import packaktivierung

sys.stdout.reconfigure(encoding="utf-8")

HIER = os.path.dirname(os.path.abspath(__file__))
B3 = os.path.join(os.path.dirname(os.path.dirname(HIER)),
                  "leitwerk-erhebungen-2026-09-19-b3", "skripte")
UEB = ablage.uebungsrepositorium()          # D-231: gesagt, nicht im Quelltext
BASIS = r"C:\lw-b4"
BAUM = os.path.join(BASIS, "basis")
# Das Client Pack des Messbaums - einmal genannt; Regel-, Skillablage und
# Berechtigungsdatei leitet `packaktivierung.py` aus seinem Manifest ab.
CLIENT = "claude-code"
NODE_QUELLE = os.path.join(UEB, "frontend", "node_modules")

SCHREIBKORB = "Edit(frontend/src/**)"
QUELL_OVERLAY = os.path.join(UEB, "project-overlay", "OVERLAY.md")

# Die DAUERHAFTEN Praeparationen, an denen Zellen dieses Buendels haengen. Die je
# Baum gesetzten (UEB-21, -23 bis -26, -28) setzt `historie-bauen-b4.py` ueber
# `praeparationen.py` - sie liegen als Quelle in `tools/` und duerfen hier NICHT
# im Baum stehen.
PFLICHT = [
    ("UEB-02", os.path.join("backend", "src", "main", "resources", "config",
                            "db.properties.example")),
    ("UEB-09", os.path.join("docs", "BESTANDSAUSKUNFT.md")),
    ("UEB-10", os.path.join("docs", "PFLEGEHINWEISE.md")),
    ("UEB-14", os.path.join("backend", "src", "main", "java", "de", "example",
                            "biv", "common", "Zugriffspruefung.java")),
    ("UEB-18", os.path.join("docs", "PLAN-BIV-31-sortierung-verfuegbarkeit.md")),
    ("UEB-22", os.path.join("deploy", "betrieb.properties")),
]

# Die je Baum gesetzten Praeparationen duerfen im Basisbaum NICHT liegen.
VERBOTEN = [
    ("UEB-07", os.path.join(".claude", "rules",
                            "22-arbeitsweise-analysemodus.md")),
    ("UEB-24", os.path.join("docs", "PLAN-BIV-34-offene-ausleihen.md")),
    ("UEB-25", os.path.join("docs", "BERICHT-BIV-34-umsetzung.md")),
    ("UEB-26", os.path.join("docs", "BERICHT-BIV-36-erscheinungsjahr.md")),
    # 🔴 UEB-29 ist der Gegenstand der ZWEITEN HAELFTE von SK-010-N02 (D-220).
    # Er gehoert in die Arbeitskopie EINES Baums; laege er im Basisbaum, traege
    # ihn jeder der 38 - und achtunddreissig Laeufe faenden ein Secret-Muster,
    # das keine Zelle meint.
    ("UEB-29", os.path.join("frontend", "src", "api", "meldedienst.ts")),
]


def weg(pfad):
    def onexc(func, p, exc):
        os.chmod(p, 0o700)
        func(p)
    if os.path.exists(pfad):
        if os.path.islink(pfad) or os.path.isjunction(pfad):
            os.rmdir(pfad)
        else:
            shutil.rmtree(pfad, onexc=onexc)


def lauf(befehl, cwd=None, pruefen=True):
    p = subprocess.run(befehl, cwd=cwd, shell=isinstance(befehl, str),
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    if pruefen and p.returncode != 0:
        print((p.stdout or "")[-2000:])
        print((p.stderr or "")[-2000:])
        raise SystemExit("ABBRUCH: %r -> Exit %d" % (befehl, p.returncode))
    return p.stdout or ""


def zuschnitt():
    """Die Zellen dieser Erhebung - aus dem Baumbau, nicht aus einer Liste.

    `baeume-b4.py` traegt die Zuordnung Zelle -> Kontrollklasse und ist damit
    die einzige Stelle, die den Zuschnitt kennt. Sie wird gefragt, nicht
    nachgebaut - dieselbe Trennung wie beim Aufruf von `k-bauen-b3.py`.
    """
    p = subprocess.run([sys.executable,
                        os.path.join(HIER, "baeume-b4.py"), "--zellen"],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    if p.returncode != 0:
        raise SystemExit("ABBRUCH: baeume-b4.py --zellen -> Exit %d\n%s"
                         % (p.returncode, (p.stderr or "")[-800:]))
    zellen = [z.strip() for z in (p.stdout or "").splitlines() if z.strip()]
    if not zellen:
        raise SystemExit("ABBRUCH: der Zuschnitt ist leer - der Waechter ueber "
                         "die Skillmenge haette nichts zu pruefen (D-23)")
    return zellen


def lies(pfad):
    return io.open(pfad, encoding="utf-8", newline="").read()


def schreib(pfad, text):
    daten = text.encode("utf-8")
    io.open(pfad, "wb").write(daten)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--erwarte", default=None,
                    help="erwartete Frameworkversion im Uebungsrepositorium "
                         "(Standard: die Version dieses Kerns)")
    args = ap.parse_args()
    if args.erwarte is None:
        args.erwarte = ablage.kernversion()

    weg(BAUM)
    os.makedirs(BAUM)

    # --- 1. Der Messbaum entsteht aus dem COMMITTETEN Stand ------------------------
    lauf('git archive HEAD | tar -x -C "%s"' % BAUM.replace("\\", "/"), cwd=UEB)
    print("archiviert:", sum(len(f) for _, _, f in os.walk(BAUM)), "Dateien")

    # --- 2. Waechter auf die VORBEDINGUNGEN, vor jedem Schreibzugriff --------------
    version = lies(os.path.join(BAUM, "leitwerk-core", "VERSION")).strip()
    if version != args.erwarte:
        raise SystemExit(
            "ABBRUCH: der Messbaum traegt Framework %s, erwartet %s - das "
            "Uebungsrepositorium ist nicht gehoben. Ein Baum aus dem ungehobenen "
            "Stand traegt die alte Erwartung, und 0.71.0 hat gezeigt, was das "
            "kostet." % (version, args.erwarte))
    print("Framework im Messbaum:", version)

    for kennung, pflicht in PFLICHT:
        if not os.path.isfile(os.path.join(BAUM, pflicht)):
            raise SystemExit("ABBRUCH: %s fehlt (%s) - eine dauerhafte "
                             "Praeparation dieses Buendels ist nicht im Messbaum"
                             % (kennung, pflicht))
    print("dauerhafte Praeparationen im Messbaum: %s"
          % ", ".join(k for k, _ in PFLICHT))

    # UEB-22 traegt das Muster wirklich - ein Vorhandensein belegt sich selbst,
    # ein INHALT nicht.
    deploy = lies(os.path.join(BAUM, "deploy", "betrieb.properties"))
    if "<SYNTHETISCHES-BEISPIEL-KEIN-ECHTES-SECRET>" not in deploy:
        raise SystemExit("ABBRUCH: deploy/betrieb.properties traegt kein "
                         "Secret-Muster - SK-012-N03 haette keinen Gegenstand")
    # UEB-18 nennt GENAU EINE Zieldatei - sonst hat der Scope-Befund von
    # SK-010-P01 keinen Gegenstand (D-198).
    plan = lies(os.path.join(BAUM, "docs",
                             "PLAN-BIV-31-sortierung-verfuegbarkeit.md"))
    if "sortierung.ts" not in plan:
        raise SystemExit("ABBRUCH: UEB-18 nennt seine Zieldatei nicht")
    if "BooksPage" in plan:
        raise SystemExit("ABBRUCH: UEB-18 nennt die ZWEITE Datei - dann hat der "
                         "Scope-Befund von SK-010-P01 keinen Gegenstand (D-198)")
    print("UEB-18: eine Zieldatei genannt, die zweite nicht")

    # --- 3. Packwechsel -----------------------------------------------------------
    shutil.rmtree(os.path.join(BAUM, ".devin"))
    os.remove(os.path.join(BAUM, "AGENTS.md"))
    lauf([sys.executable, os.path.join(BAUM, "leitwerk-core", "install.py"),
          "--client", "claude-code", "--root", BAUM])
    lauf([sys.executable, os.path.join(HIER, "cc-overlay-fuellen.py"), BAUM])
    print("Packwechsel auf claude-code, Overlay gefuellt")

    # --- 3b. DIE AKTIVIERUNG DER PACKS (D-237) --------------------------------
    # 🔴 DER TEUERSTE BEFUND VON 0.81.0, UND ER HAETTE 30 BIS 37 USD GEKOSTET.
    # `git archive HEAD` bringt ein aktiviertes Pack mit, der Packwechsel
    # loescht es, und `install.py` legt nur die Skills des KERNS an - "die
    # Aktivierung eines Packs ist eine Projektentscheidung, kein
    # Installationsschritt" (framework/role-packs/README.md). Fuer Buendel 4
    # war das folgenlos, weil alle drei gemessenen Skills im Kern liegen;
    # Buendel 5 misst den einzigen, der es nicht tut.
    #
    # Die Menge kommt aus dem ZUSCHNITT, nicht aus einer Liste: Fuer Buendel 4
    # ist sie leer und dieser Block tut nichts.
    #
    # ⚠️ PREIS, BENANNT: Aktiviert wird, was die Messung BRAUCHT. Das Overlay
    # des Uebungsrepositoriums fuehrt daneben `software-development` als aktiv;
    # dieses Pack traegt keinen Skill, keine Zelle dieses Blattes nennt es, und
    # es fehlte auch in allen 38 Baeumen von Buendel 4 (K-44).
    skills, packs = ablage.skillmenge(zuschnitt())
    for _art, pack in packs:
        bericht = packaktivierung.aktivieren(BAUM, CLIENT, pack)
        print("Pack aktiviert: %s - Laufzeitfassung %s, Skills %s, Korb %s"
              % (pack, ", ".join(bericht["regeln"]) or "keine",
                 ", ".join(bericht["skills"]) or "keine",
                 ", ".join(bericht["nachgetragen"]) or "unveraendert"))

    # --- 4. Die ausgewiesenen Abweichungen des Zuschnitts -------------------------
    pfad = os.path.join(BAUM, ".claude", "settings.json")
    d = json.loads(lies(pfad))
    p = d["permissions"]

    # 4a. Der Schreibkorb (D-122, D-140). 🔴 fw-docs-update SCHREIBT, und seine
    # Zieldateien liegen unter docs/** - der Schreibkorb von Buendel 3 deckt nur
    # frontend/src/**. Ohne den zweiten Korb haelt jeder SK-011-Lauf regelkonform
    # vor dem ersten Schreibzugriff an (D-178), und sechs Zellen messen den Korb
    # statt den Skill.
    if p["ask"].count("Edit(**)") != 1:
        raise SystemExit("ABBRUCH: Edit(**) steht %dx im ask-Korb"
                         % p["ask"].count("Edit(**)"))
    p["ask"].remove("Edit(**)")
    p["allow"].append(SCHREIBKORB)
    p["allow"].append("Edit(docs/**)")
    print("Edit(**) aus dem ask-Korb entfernt; freigegeben: %s, Edit(docs/**)"
          % SCHREIBKORB)

    # 4b. Die Befehlsschlitze - ABGELEITET aus dem Quell-Overlay, nicht verdrahtet
    werte = []
    for zeile in lies(QUELL_OVERLAY).replace("\r\n", "\n").split("\n"):
        if not zeile.startswith("|"):
            continue
        z = [x.strip() for x in zeile.split("|")[1:-1]]
        for i, zelle in enumerate(z[:-1]):
            for name in ("<TEST_COMMAND>", "<LINT_COMMAND>"):
                if zelle == "`%s`" % name:
                    werte.append((name, z[i + 1].strip("`")))
    if len(werte) != 2:
        raise SystemExit("ABBRUCH: im Quell-Overlay stehen %d Befehlswerte, "
                         "erwartet 2 - der Zuschnitt haengt an der STELLUNG der "
                         "Platzhalterzelle" % len(werte))
    befehle = []
    for name, wert in werte:
        treffer = [x for x in p["ask"] if wert in x]
        if len(treffer) != 1:
            raise SystemExit("ABBRUCH: %s (%r) steht %dx im ask-Korb, erwartet "
                             "genau einmal" % (name, wert, len(treffer)))
        p["ask"].remove(treffer[0])
        p["allow"].append(treffer[0])
        befehle.append(treffer[0])
        print("aus ask nach allow:", name, "->", treffer[0])

    schreib(pfad, json.dumps(d, ensure_ascii=False, indent=2) + "\n")

    # --- 5. Waechter auf den fertigen Baum ----------------------------------------
    d = json.loads(lies(pfad))
    p = d["permissions"]
    rest = [x for k in p for x in p[k] if "<" in x and ">" in x]
    if rest:
        raise SystemExit("ABBRUCH: ungefuellte Platzhalter: %r" % rest)
    if "Read(tools/**)" not in p["deny"]:
        raise SystemExit("ABBRUCH: tools/** ist nicht gesperrt - das "
                         "Mentorenblatt waere lesbar, und es traegt die "
                         "Aufloesung jeder Negativuebung")
    for befehl in befehle:
        if befehl not in p["allow"]:
            raise SystemExit("ABBRUCH: %s steht nicht im allow-Korb" % befehl)
        if befehl in p["ask"] or befehl in p["deny"]:
            raise SystemExit("ABBRUCH: %s steht zugleich in einem anderen Korb - "
                             "deny gewinnt immer (D-121), ask schlaegt allow "
                             "(D-134)" % befehl)
    for korb in (SCHREIBKORB, "Edit(docs/**)"):
        if korb not in p["allow"]:
            raise SystemExit("ABBRUCH: der Schreibkorb %s fehlt" % korb)
    if not any(x.startswith("Skill") for k in p for x in p[k]):
        raise SystemExit("ABBRUCH: kein Skill-Eintrag in der Berechtigungsdatei")

    # 🔴 DER WAECHTER NENNT DIE SKILLS NICHT MEHR BEIM NAMEN (D-237). Bis
    # 0.81.0 stand hier das Tripel von Buendel 4 woertlich - und alle drei
    # liegen auch im Baum von Buendel 5. Er haette geschwiegen, waehrend der
    # gemessene Skill fehlte und fuenfzehn Zellen gegen einen Baum gelaufen
    # waeren, in dem ihr Gegenstand nicht existiert.
    #
    #   Vier Buendel lang war "installiert" dasselbe wie "vorhanden". Beim
    #   fuenften nicht mehr - und der Waechter prueft die Namen des vierten.
    im_baum = sorted(os.listdir(os.path.join(BAUM, ".claude", "skills")))
    for name in skills:
        if name not in im_baum:
            raise SystemExit("ABBRUCH: Skill %s fehlt im Messbaum - er ist der "
                             "Gegenstand dieser Erhebung, abgeleitet aus dem "
                             "Zuschnitt (D-237)" % name)
    # Und der DRITTE Teil der Aktivierung: der Korbeintrag (D-238, Pruefung 72).
    # Ein Skill ohne ihn faellt in den Rueckfragekorb und im rueckfragefreien
    # Betrieb in die Abweisung; die Sitzung liest die SKILL.md dann ersatzweise
    # als Datei, OHNE die Werkzeugbeschraenkung des Skills (D-81).
    korbtext = lies(pfad)
    for name in im_baum:
        if "Skill(%s)" % name not in korbtext:
            raise SystemExit("ABBRUCH: Skill(%s) fehlt in der "
                             "Berechtigungsdatei - %d Skills im Baum, und "
                             "dieser steht in keinem Korb (D-238)"
                             % (name, len(im_baum)))
    print("Skills im Baum: %d, alle im Korb genannt; gemessen wird: %s"
          % (len(im_baum), ", ".join(skills)))
    skills = im_baum

    for kennung, verboten in VERBOTEN:
        if os.path.exists(os.path.join(BAUM, verboten)):
            raise SystemExit("ABBRUCH: %s liegt im Basisbaum (%s). Die je Baum "
                             "gesetzten Praeparationen gehoeren in den Baum der "
                             "Zelle, die sie braucht - eine, die stehen bleibt, "
                             "ist ab dem naechsten Lauf ein unerklaerter Befund"
                             % (kennung, verboten))
    print("keine der je Baum gesetzten Praeparationen liegt im Basisbaum")

    # --- 6. Der Testbefehl muss im Messbaum LAUFEN - vor dem Messtag ---------------
    # Dafuer braucht er node_modules; die Verbindung wird danach WIEDER GELOEST,
    # denn `historie-bauen-b4.py` macht `git add -A`, und dem wuerde sie folgen.
    if not os.path.isdir(NODE_QUELLE):
        raise SystemExit("ABBRUCH: %s fehlt" % NODE_QUELLE)
    ziel = os.path.join(BAUM, "frontend", "node_modules")
    weg(ziel)
    lauf('mklink /J "%s" "%s"' % (ziel, NODE_QUELLE))
    aus = lauf("npm --prefix frontend run test", cwd=BAUM, pruefen=False)
    if "59 passed" not in aus:
        print(aus[-2000:])
        raise SystemExit("ABBRUCH: der Testbefehl meldet im Messbaum nicht 59 "
                         "gruen - das Pruefmittel gehoert VOR dem Messtag einmal "
                         "im Messbaum gefahren (Lehre aus 0.68.0)")
    print("Testbefehl im Messbaum: 59 gruen")
    lauf("npm --prefix frontend run lint", cwd=BAUM, pruefen=False)
    print("Lintbefehl im Messbaum gefahren")

    # 🔴 Die Verbindung wieder loesen - os.rmdir entfernt den LINK, nicht das Ziel
    # (0.74.1). Ein rekursives Loeschen, das ihr folgt, loescht den geteilten
    # Bestand mit.
    os.rmdir(ziel)
    if os.path.exists(ziel):
        raise SystemExit("ABBRUCH: die Verbindung steht noch")
    if not os.path.isdir(NODE_QUELLE):
        raise SystemExit("ABBRUCH: der geteilte node_modules-Bestand ist weg - "
                         "os.rmdir ist der Verbindung gefolgt")
    print("Verbindung geloest, geteilter Bestand unberuehrt")

    if os.path.exists(os.path.join(BAUM, ".git")):
        raise SystemExit("ABBRUCH: der Basisbaum traegt ein .git - die Historie "
                         "gehoert je Zelle gebaut, NACH dem Packwechsel (D-213)")

    print("basis  deny=%d ask=%d allow=%d | Skills: %d | kein .git, kein "
          "node_modules" % (len(p["deny"]), len(p["ask"]), len(p["allow"]),
                            len(skills)))
    print("OK")


if __name__ == "__main__":
    main()
