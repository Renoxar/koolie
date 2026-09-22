# -*- coding: utf-8 -*-
"""Baut den BASISBAUM des fuenften Testblatt-Buendels unter C:\\lw-b5.

    python umgebungen-bauen-b5.py [--erwarte <version>]

Ergebnis: C:\\lw-b5\\basis - eine vollstaendige claude-code-Installation des
Uebungsrepositoriums MIT AKTIVIERTEM Role Pack `requirements-engineering`, ohne
`.git`. Die Historie kommt je Baum dazu (`baeume-b5.py`).

🔴 ABGELEITET AUS `umgebungen-bauen-b4.py` (CR-2026-116). Die MECHANIK ist geerbt
und mit 0.82.0 gemessen - Packwechsel, Overlay-Fuellung, Packaktivierung in drei
Teilen, abgeleiteter Skillwaechter. Neu ist der ZUSCHNITT, und er ist an vier
Stellen anders:

  1. KEIN `node_modules`. `historie-bauen-b4.py` und die Verzeichnisverbindung
     gibt es, weil zwoelf Zellen von Buendel 4 einen DIFF verlangen und drei
     Skills SCHREIBEN. `role-re-ticket` ist M1 und rein lesend; keine der
     fuenfzehn Zellen nennt einen Branch, einen Diff oder einen Testbefehl.
     Damit entfaellt auch die Loeschfalle von 0.74.1 - ein rekursives Loeschen,
     das der Verbindung folgt, kann hier gar nicht entstehen.
  2. LEERE ABWEICHUNGSLISTE. Buendel 4 nimmt `Edit(**)` aus dem `ask`-Korb und
     gibt zwei Schreibkoerbe frei (D-178), weil sechs Zellen sonst den Korb statt
     den Skill messen. `RE-001-N03` misst das GEGENTEIL: dass der Lauf nichts
     eintraegt. Der Korb bleibt, wie `install.py` ihn erzeugt - und ein Waechter
     belegt, dass er es tut.
  3. DIE VORBEDINGUNGEN SIND ANDERE. Nicht Plaene und Berichte, sondern
     Schnittstellenvertrag, Migration, Glossar und die WERTZEILE von
     `<ISSUE_TRACKER>` in Abschnitt 13 des Overlays.
  4. DAS PRUEFMITTEL IST `validate-output.py`, nicht `npm test`. Es wird VOR dem
     Messtag einmal im Messbaum gefahren (Lehre aus 0.68.0) - und gelesen wird
     seine AUSGABE, nicht sein Exitwert: Alle drei Faelle geben denselben
     (Befund von 0.81.0).

🔴 DIE REIHENFOLGE IST GEERBT UND GEMESSEN (D-213):
archivieren -> Packwechsel -> `install.py` -> Overlay fuellen -> Packaktivierung
-> (Zuschnitt) -> HISTORIE. Wer die Historie zuerst baut, committet den Stand VOR
dem Packwechsel, und das Loeschen von `.devin/` steht danach in `git status`.
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
UEB = ablage.uebungsrepositorium()          # D-231: gesagt, nicht im Quelltext
BASIS = r"C:\lw-b5"
BAUM = os.path.join(BASIS, "basis")
# Das Client Pack des Messbaums - einmal genannt; Regel-, Skillablage und
# Berechtigungsdatei leitet `packaktivierung.py` aus seinem Manifest ab.
CLIENT = "claude-code"

QUELL_OVERLAY = os.path.join(UEB, ".koolie/project-overlay", "OVERLAY.md")

# Die WERTZEILE, an der `RE-001-P04` und `RE-001-N09` mit entgegengesetztem
# Vorzeichen haengen (D-240). Sie steht hier woertlich, weil sie der Gegenstand
# zweier Zellen ist - und `UEB-30` sucht exakt denselben Text.
WERTZEILE = "| `<ISSUE_TRACKER>` | `GitHub Issues` |"

# Die DAUERHAFTEN Vorbedingungen, an denen Zellen dieses Buendels haengen. Anders
# als bei Buendel 4 sind es keine Praeparationen, sondern Traeger des
# Uebungsrepositoriums: der Skill RECHERCHIERT, und was er finden soll, muss da
# sein.
PFLICHT = [
    ("Schnittstellenvertrag (P03, N08)",
     os.path.join("api-contracts", "openapi.yaml")),
    ("Migration und Schema (P03, N08)",
     os.path.join("backend", "src", "main", "resources", "db", "migration",
                  "V1__init.sql")),
    ("Glossar (P01, Manifest-Typ glossary)",
     os.path.join(".koolie/project-overlay", "documents", "glossary", "biv-glossar.md")),
    ("Quell-Overlay mit Abschnitt 13 (P04)",
     os.path.join(".koolie/project-overlay", "OVERLAY.md")),
    ("Komponente mit teilweise vorhandenem Verhalten (P01, P02)",
     os.path.join("frontend", "src", "api", "bestand.ts")),
]

# Die je Meszbaum gesetzten Praeparationen duerfen im Basisbaum NICHT liegen.
# 🔴 `UEB-30` IST EIN TEXTERSATZ UND HAT DESHALB KEINEN EIGENEN PFAD. Sein
# Verbot ist ein INHALT: Solange die Wertzeile ihren Wert traegt, ist er nicht
# gesetzt. Laege er im Basisbaum, traegen ihn alle dreissig Baeume - und
# `RE-001-P04`, die denselben Platzhalter MIT Wert verlangt, waere in keinem
# einzigen fahrbar (D-240).
VERBOTEN_DATEI = [
    ("UEB-31", os.path.join("frontend", "src", "api", "fernleihe.ts")),
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

    `baeume-b5.py` traegt die Zuordnung Zelle -> Kontrollklasse und ist damit die
    einzige Stelle, die den Zuschnitt kennt. Sie wird gefragt, nicht nachgebaut.
    """
    p = subprocess.run([sys.executable,
                        os.path.join(HIER, "baeume-b5.py"), "--zellen"],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    if p.returncode != 0:
        raise SystemExit("ABBRUCH: baeume-b5.py --zellen -> Exit %d\n%s"
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

    # --- 1. Der Messbaum entsteht aus dem COMMITTETEN Stand ----------------------
    lauf('git archive HEAD | tar -x -C "%s"' % BAUM.replace("\\", "/"), cwd=UEB)
    print("archiviert:", sum(len(f) for _, _, f in os.walk(BAUM)), "Dateien")

    # --- 2. Waechter auf die VORBEDINGUNGEN, vor jedem Schreibzugriff ------------
    version = lies(os.path.join(BAUM, ".koolie/core", "VERSION")).strip()
    if version != args.erwarte:
        raise SystemExit(
            "ABBRUCH: der Messbaum traegt Framework %s, erwartet %s - das "
            "Uebungsrepositorium ist nicht gehoben. Ein Baum aus dem ungehobenen "
            "Stand traegt die alte Erwartung." % (version, args.erwarte))
    print("Framework im Messbaum:", version)

    for was, pflicht in PFLICHT:
        if not os.path.isfile(os.path.join(BAUM, pflicht)):
            raise SystemExit("ABBRUCH: %s fehlt (%s) - eine Vorbedingung dieses "
                             "Buendels ist nicht im Messbaum" % (pflicht, was))
    print("Vorbedingungen im Messbaum: %s" % "; ".join(w for w, _ in PFLICHT))

    # --- 2b. Die INHALTE der Vorbedingungen ------------------------------------
    # Ein Vorhandensein belegt sich selbst, ein INHALT nicht.
    overlay = lies(os.path.join(BAUM, ".koolie/project-overlay", "OVERLAY.md"))
    if overlay.count(WERTZEILE) != 1:
        raise SystemExit("ABBRUCH: die Wertzeile von <ISSUE_TRACKER> steht %dx im "
                         "Overlay, erwartet genau einmal - RE-001-P04 haette "
                         "keinen Gegenstand, und UEB-30 keinen Ausgangszustand"
                         % overlay.count(WERTZEILE))
    print("Abschnitt 13: <ISSUE_TRACKER> gebunden und mit Wert (P04)")

    schema = lies(os.path.join(BAUM, "backend", "src", "main", "resources", "db",
                               "migration", "V1__init.sql"))
    if "NOT NULL UNIQUE" not in schema:
        raise SystemExit("ABBRUCH: das Schema fuehrt keine Eindeutigkeitsbedingung "
                         "- RE-001-N08 haette keine Randbedingung, der sie "
                         "widersprechen koennte")
    vertrag = lies(os.path.join(BAUM, "api-contracts", "openapi.yaml"))
    if "pattern:" not in vertrag or "required:" not in vertrag:
        raise SystemExit("ABBRUCH: der Schnittstellenvertrag fuehrt weder Muster "
                         "noch Pflichtfelder - RE-001-P03 haette keinen Beleg")
    print("Schema: Eindeutigkeitsbedingung; Vertrag: Muster und Pflichtfelder "
          "(P03, N08)")

    manifest_overlay = lies(os.path.join(BAUM, ".koolie/project-overlay",
                                         "overlay-manifest.yaml"))
    if "glossary" not in manifest_overlay:
        raise SystemExit("ABBRUCH: im Overlay-Manifest ist kein Dokument vom Typ "
                         "`glossary` registriert - die Vorbedingung von RE-001-P01 "
                         "traegt nicht")
    print("Overlay-Manifest: ein Dokument vom Typ `glossary` registriert (P01)")

    # --- 3. Packwechsel ---------------------------------------------------------
    shutil.rmtree(os.path.join(BAUM, ".devin"))
    os.remove(os.path.join(BAUM, "AGENTS.md"))
    lauf([sys.executable, os.path.join(BAUM, ".koolie/core", "install.py"),
          "--client", CLIENT, "--root", BAUM])
    lauf([sys.executable, os.path.join(HIER, "cc-overlay-fuellen.py"), BAUM])
    print("Packwechsel auf %s, Overlay gefuellt" % CLIENT)

    # --- 3b. DIE AKTIVIERUNG DES PACKS (D-237, D-238, D-244) --------------------
    # 🔴 FUER BUENDEL 4 WAR DIESER BLOCK LEER, WEIL ALLE DREI GEMESSENEN SKILLS IM
    # KERN LIEGEN. Buendel 5 misst den einzigen, der es nicht tut: `install.py`
    # legt zwoelf Skills an, und `role-re-ticket` ist keiner davon.
    skills, packs = ablage.skillmenge(zuschnitt())
    if not packs:
        raise SystemExit("ABBRUCH: der Zuschnitt nennt kein Pack - bei Buendel 5 "
                         "liegt der gemessene Skill AUSSERHALB des Kerns, und ein "
                         "leerer Block waere der Befund von D-237 zum zweiten Mal")
    for _art, pack in packs:
        bericht = packaktivierung.aktivieren(BAUM, CLIENT, pack)
        print("Pack aktiviert: %s - Laufzeitfassung %s, Skills %s, Korb %s"
              % (pack, ", ".join(bericht["regeln"]) or "keine",
                 ", ".join(bericht["skills"]) or "keine",
                 ", ".join(bericht["nachgetragen"]) or "unveraendert"))

    # --- 4. Die Abweichungen des Zuschnitts: KEINE ------------------------------
    # 🔴 UND DAS IST EIN WAECHTER, KEINE ZUSAGE (E3 von CR-2026-116). Der Korb
    # bleibt, wie `install.py` ihn erzeugt hat. Wer ihn spaeter doch anfasst,
    # bricht hier ab - eine leere Abweichungsliste, die niemand prueft, ist eine
    # Behauptung.
    pfad = os.path.join(BAUM, ".claude", "settings.json")
    d = json.loads(lies(pfad))
    p = d["permissions"]
    if p["ask"].count("Edit(**)") != 1:
        raise SystemExit("ABBRUCH: Edit(**) steht %dx im ask-Korb, erwartet genau "
                         "einmal. Buendel 5 misst einen M1-Skill mit `deny` auf "
                         "`edit` und `exec`; ein freigegebener Schreibkorb waere "
                         "eine Abweichung ohne Anlass" % p["ask"].count("Edit(**)"))
    print("Abweichungsliste dieses Buendels: LEER - Edit(**) bleibt im ask-Korb")

    # --- 5. Waechter auf den fertigen Baum --------------------------------------
    rest = [x for k in p for x in p[k] if "<" in x and ">" in x]
    if rest:
        raise SystemExit("ABBRUCH: ungefuellte Platzhalter: %r" % rest)
    if "Read(tools/**)" not in p["deny"]:
        raise SystemExit("ABBRUCH: tools/** ist nicht gesperrt - das Mentorenblatt "
                         "waere lesbar, und es traegt die Aufloesung jeder "
                         "Negativuebung")
    if not any(x.startswith("Skill") for k in p for x in p[k]):
        raise SystemExit("ABBRUCH: kein Skill-Eintrag in der Berechtigungsdatei")

    # 🔴 DER WAECHTER NENNT DIE SKILLS NICHT BEIM NAMEN (D-237). Die Sollmenge
    # kommt aus dem Zuschnitt ueber die Testblaetter des Frameworks.
    im_baum = sorted(os.listdir(os.path.join(BAUM, ".claude", "skills")))
    for name in skills:
        if name not in im_baum:
            raise SystemExit("ABBRUCH: Skill %s fehlt im Messbaum - er ist der "
                             "Gegenstand dieser Erhebung, abgeleitet aus dem "
                             "Zuschnitt (D-237)" % name)
    # Der DRITTE Teil der Aktivierung: der Korbeintrag (D-238, Pruefung 72).
    korbtext = lies(pfad)
    for name in im_baum:
        if "Skill(%s)" % name not in korbtext:
            raise SystemExit("ABBRUCH: Skill(%s) fehlt in der Berechtigungsdatei - "
                             "%d Skills im Baum, und dieser steht in keinem Korb "
                             "(D-238)" % (name, len(im_baum)))
    print("Skills im Baum: %d, alle im Korb genannt; gemessen wird: %s"
          % (len(im_baum), ", ".join(skills)))

    # 🔴 DIE LAUFZEITFASSUNG DES PACKS IST GERENDERT, NICHT KOPIERT (D-244).
    # `claude-code` wertet fuer Regeldateien nur `paths` aus (K-18); das
    # Quellfrontmatter traegt `description` und `trigger`, und ein `cp` hat am
    # Messbaum von Buendel 5 ZWEI Validatorfehler erzeugt.
    rolle = os.path.join(BAUM, ".claude", "rules",
                         "30-role-requirements-engineering.md")
    if not os.path.isfile(rolle):
        raise SystemExit("ABBRUCH: die Rollenregel steht nicht in der Regelablage")
    kopf = lies(rolle)[:400]
    if "trigger:" in kopf or "description:" in kopf:
        raise SystemExit("ABBRUCH: die Laufzeitfassung traegt noch das "
                         "Quellfrontmatter - sie ist KOPIERT statt gerendert "
                         "(D-244)")
    print("Rollenregel: gerendert, kein Quellfrontmatter (D-244)")

    for kennung, verboten in VERBOTEN_DATEI:
        if os.path.exists(os.path.join(BAUM, verboten)):
            raise SystemExit("ABBRUCH: %s liegt im Basisbaum (%s). Die je Meszbaum "
                             "gesetzten Praeparationen gehoeren in den Baum der "
                             "Zelle, die sie braucht - eine, die stehen bleibt, "
                             "ist ab dem naechsten Lauf ein unerklaerter Befund"
                             % (kennung, verboten))
    print("UEB-30 nicht gesetzt (Wertzeile traegt ihren Wert), UEB-31 nicht im "
          "Basisbaum")

    # --- 6. Das Pruefmittel muss im Messbaum LAUFEN - vor dem Messtag -----------
    # 🔴 GELESEN WIRD DIE AUSGABE, NICHT DER EXITWERT. `validate-output.py` gibt
    # in allen drei Faellen denselben - "die Ausgabe ist falsch", "der Skill ist
    # nicht installiert" und "kein Pack im Baum" sind daran nicht zu
    # unterscheiden (Befund von 0.81.0). Der Waechter liest deshalb die
    # Ergebniszeile und schliesst eine FEHLER-Zeile aus.
    pruef = subprocess.run(
        [sys.executable,
         os.path.join(BAUM, ".koolie/core", "tests", "scripts",
                      "validate-output.py"),
         "--skill", "role-re-ticket", "--root", BAUM],
        input="", capture_output=True, text=True, encoding="utf-8",
        errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    aus = (pruef.stdout or "") + (pruef.stderr or "")
    if "FEHLER" in aus:
        print(aus[-1500:])
        raise SystemExit("ABBRUCH: das Pruefmittel findet den Skill im Messbaum "
                         "nicht - es ist das zweite Pruefmittel von RE-001-P01, "
                         "und es gehoert VOR den Messtag gefahren (0.68.0)")
    if "(Skill role-re-ticket)" not in aus:
        print(aus[-1500:])
        raise SystemExit("ABBRUCH: das Pruefmittel hat keine Ergebniszeile "
                         "geliefert - ohne sie ist sein Exitwert keine Aussage")
    ergebniszeile = [z for z in aus.splitlines() if z.startswith("Ergebnis:")]
    print("Pruefmittel im Messbaum: %s (Exit %d, gegen leere Eingabe - die "
          "Befunde sind erwartet, die Ergebniszeile ist der Messwert)"
          % (ergebniszeile[0] if ergebniszeile else "?", pruef.returncode))

    # --- 7. Die WERKZEUGAUSSTATTUNG gegen das Overlay (K-89, D-256) -------------
    # 🔴 DER WAECHTER NENNT, ER BRICHT NICHT AB. Die Quelle der Abweichung liegt
    # ausserhalb jedes Baums - in der Benutzerkonfiguration des Arbeitsplatzes -,
    # und ein Messaufbau, der sie abschaltet, misst eine Umgebung, die es sonst
    # nicht gibt. Gemessen am Messtag von Buendel 5: 19 von 30 Laeufen melden den
    # Widerspruch, NULL ruft ein MCP-Werkzeug auf.
    mcp = subprocess.run(
        [sys.executable, os.path.join(HIER, "mcp-waechter.py"), "vorher", BAUM],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    print()
    print((mcp.stdout or "").rstrip())
    if mcp.returncode != 0:
        print((mcp.stderr or "")[-800:])
        raise SystemExit("ABBRUCH: der MCP-Waechter selbst ist gescheitert - ein "
                         "Waechter, der nicht laeuft, sagt nicht 'kein Befund' "
                         "(D-229)")
    print()

    if os.path.exists(os.path.join(BAUM, ".git")):
        raise SystemExit("ABBRUCH: der Basisbaum traegt ein .git - die Historie "
                         "gehoert je Zelle gebaut, NACH dem Packwechsel (D-213)")
    if os.path.isdir(os.path.join(BAUM, "frontend", "node_modules")):
        raise SystemExit("ABBRUCH: node_modules im Basisbaum - Buendel 5 misst "
                         "einen rein lesenden Skill ohne Testbefehl (E2)")

    print("basis  deny=%d ask=%d allow=%d | Skills: %d | kein .git, kein "
          "node_modules" % (len(p["deny"]), len(p["ask"]), len(p["allow"]),
                            len(im_baum)))
    print("OK")


if __name__ == "__main__":
    main()
