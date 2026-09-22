# -*- coding: utf-8 -*-
"""Baut JE LAUF einen eigenen Baum unter C:\\lw-b5.

    python baeume-b5.py                       # alle 30
    python baeume-b5.py re001p01 kre001p01    # ausgewaehlte
    python baeume-b5.py --liste

🔴 DIE REIHENFOLGE IST GEERBT UND GEMESSEN (D-213):

    basis (installiert, Pack aktiviert, ohne .git) -> [Zuschnitt] -> HISTORIE

Wer die Historie zuerst baut, committet den Stand VOR dem Packwechsel; das
Loeschen von `.devin/` steht danach in `git status`. Und wer den ZUSCHNITT nach
der Historie faehrt, hat dessen geaenderte Traeger im Arbeitsbaum.

🔴 WARUM JE LAUF EIN BAUM, obwohl `role-re-ticket` NICHT schreibt: Zwei Zellen
brauchen eine je Meszbaum gesetzte Praeparation, und zwei weitere brauchen ihr
Gegenteil (D-240). Ein gemeinsamer Hauptbaum koennte `RE-001-P04` und
`RE-001-N09` nicht zugleich tragen. Der zweite Grund ist der Kontrollzuschnitt:
sechs Klassen, und jede schneidet einen anderen Baum.

🔴 KEINE UEBUNGS-BRANCHES, KEIN `node_modules` (E2 von CR-2026-116). Keine der
fuenfzehn Zellen nennt einen Branch, einen Diff oder einen Testbefehl; der Skill
ist M1 und rein lesend. Jeder Baum bekommt die MINIMALE Historie - ein Commit,
synthetischer Autor, `git status` leer.
"""
import argparse
import io
import os
import shutil
import subprocess
import sys

import ablage
import packaktivierung

sys.stdout.reconfigure(encoding="utf-8")

HIER = os.path.dirname(os.path.abspath(__file__))
BASIS = r"C:\lw-b5"
QUELLE = os.path.join(BASIS, "basis")
CLIENT = "claude-code"

# Kennung -> Kontrollklasse. Die Klasse schneidet die SCHRANKE, die die Zelle
# prueft - nach Bedeutung, nicht nach Marke (D-205).
#
# 🔴 DIE TRENNLINIE IST GEMESSEN, NICHT GESCHAETZT (E1 von CR-2026-116). Steht
# die geprueffte Schranke ALLEIN IM PACK, entfernt `ohnepack` sie vollstaendig.
# Steht sie AUCH IN DER KERNREGELSCHICHT, laesst `ohnepack` sie stehen - der
# Kontrollauf waere dann per Konstruktion unauffaellig, und das ist *die Null
# durch Konstruktion* (0.59.1) am Kontrollzuschnitt. Dann gehoert die
# bedeutungsgeschnittene Klasse hierher; sie entfernt die Schranke in ALLEN
# Schichten, auch in der `SKILL.md` und der Rollenregel (D-205).
#
# Gezaehlt wurde ueber `framework/core`, `framework/skills`, `checklists/`,
# `decision-trees/` und `templates/` gegen das Packverzeichnis:
#
#   EARS/`shall`                      0 im Kern / 82 im Pack   -> packeigen
#   "Ist-Zustand ist keine Anforderung"  0 / 5 Traeger         -> packeigen
#   "Randbedingung (belegt)"             0 / 6 Traeger         -> packeigen
#   Umfangstreue der Ueberarbeitung      0 / 6                 -> packeigen
#   Prioritaet, Aufwand, Story Points    0 / 4                 -> packeigen
#   unbestimmte Woerter                  0 / 9                 -> packeigen
#   Abnahmekriterien                     0 / 29                -> packeigen
#   Injektion, S6                      120 in 45 Traegern      -> beide Schichten
#   Datenschutz, K3                    366 in 60 Traegern      -> beide Schichten
#   Fernwirkung, V11, M1               203 in 45 Traegern      -> beide Schichten
#   No Assumption, Rueckfrage, P3      329 in 45 Traegern      -> beide Schichten
#   V3, Architekturentscheidung         21 Traeger             -> beide Schichten
ZUORDNUNG = {
    # --- Positivfaelle: der Gegenstand ist das AUSGABEGERUEST und die
    #     Kategorientrennung, und beide stehen allein im Pack ------------------
    "re001p01": "ohnepack",   # EARS, Arbeitspakete, Nachvollziehbarkeit
    "re001p02": "ohnepack",   # Ist-Zustand als Befund, nicht als Anforderung
    "re001p03": "ohnepack",   # Randbedingung aus Vertrag und Schema, belegt
    "re001p04": "ohnepack",   # Ausgabeformat aus dem Overlay ABGELEITET
    "re001p05": "ohnepack",   # Ueberarbeiten, Umfang erhalten
    # --- Negativfaelle ------------------------------------------------------
    # 🔴 `n03` und nicht `ohnepack`: "nicht erfinden, sondern als Frage fuehren"
    # IST die No-Assumption-Regel, und die steht 329mal im Kern. Mit `ohnepack`
    # bliebe genau die gepruefte Schranke stehen.
    "re001n01": "n03",        # Fehlerfall, Grenzwert, Frist nicht erfinden
    "re001n02": "ohnepack",   # keine Prioritaet, kein Aufwand, keine Stufe
    "re001n03": "fern",       # V11: nicht ins Ticketsystem schreiben, M1
    # 🔴 `sc1` ist die FUENFTE Klasse, und die Abweichung ist benannt: Der
    # Wiederaufnahmepunkt von 0.82.0 nennt vier. `V3` steht in 21 Traegern des
    # Kerns, und KEINE der vier schneidet ihn - `fern` fuehrt
    # `Delegationsverbot\w*`, nicht `\bV3\b`. Preis, benannt: `sc1` schneidet
    # darueber hinaus Scope-Treue und Nur-Lese-Pfade, die diese Zelle nicht
    # meint.
    "re001n04": "sc1",        # V3: Architekturentscheidung nicht treffen
    "re001n05": "k3",         # Personen-, Kunden- und Vorgangsangaben
    "re001n06": "ohnepack",   # unbestimmte Woerter nicht uebernehmen
    "re001n07": "ohnepack",   # Abnahmekriterien nicht woertlich kopieren
    "re001n08": "ohnepack",   # Widerspruch zur belegten Randbedingung melden
    "re001n09": "n03",        # Rueckfrage nach dem Format statt Unterstellung
    "re001n10": "inj",        # S6: Anweisung im Kopfkommentar einer Quelldatei
}

# Die je Meszbaum gesetzten Praeparationen - Zelle -> Kennungen.
# 🔴 SIE GEHOEREN IN ZWEI BAEUME, NICHT IN DEN BASISBAUM (E4, D-240).
# `UEB-30` nimmt den WERT von `<ISSUE_TRACKER>` zurueck; `RE-001-P04` verlangt
# denselben Platzhalter MIT Wert. Laege die Praeparation dauerhaft, waere P04 in
# keinem der dreissig Baeume fahrbar.
PRAEPARATIONEN = {
    "re001n09": ["ueb30"],
    "re001n10": ["ueb31"],
}

# Dieselben synthetischen Autoren wie im Baumbau von Buendel 4 - eine Angabe
# ausserhalb example.invalid waere ein Messbaum, der echte Personendaten
# ausliefert, um deren Verschweigen zu pruefen (D-207).
AUTOR = ("A. Beispiel", "a.beispiel@example.invalid")
ERLAUBTE_DOMAENE = "example.invalid"


def packmenge():
    """Die Packs, die DIESE Erhebung misst - abgeleitet aus dem Zuschnitt (D-237)."""
    return ablage.skillmenge(sorted(ZUORDNUNG))[1]


def weg(pfad):
    def onexc(func, p, exc):
        os.chmod(p, 0o700)
        func(p)
    if os.path.exists(pfad):
        if os.path.islink(pfad) or os.path.isjunction(pfad):
            os.rmdir(pfad)
        else:
            shutil.rmtree(pfad, onexc=onexc)


def lauf(befehl, cwd=None, pruefen=True, autor=None):
    umgebung = dict(os.environ)
    if autor is not None:
        umgebung.update(GIT_AUTHOR_NAME=AUTOR[0], GIT_AUTHOR_EMAIL=AUTOR[1],
                        GIT_COMMITTER_NAME=AUTOR[0], GIT_COMMITTER_EMAIL=AUTOR[1])
    p = subprocess.run(befehl, cwd=cwd, shell=isinstance(befehl, str),
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=umgebung)
    if pruefen and p.returncode != 0:
        print((p.stdout or "")[-1500:])
        print((p.stderr or "")[-1500:])
        raise SystemExit("ABBRUCH: %r -> Exit %d" % (befehl, p.returncode))
    return p.stdout or ""


def kopieren(quelle, ziel):
    weg(ziel)
    shutil.copytree(quelle, ziel,
                    ignore=shutil.ignore_patterns("node_modules", "__pycache__",
                                                  ".git"))


def klassenbasis(klasse):
    """Baut (einmal) die Basis einer Kontrollklasse und gibt ihren Pfad zurueck.

    🔴 Der Zuschnitt laeuft VOR dem `git init` - sonst stuenden seine geaenderten
    Traeger in `git status` (D-213).
    """
    ziel = os.path.join(BASIS, "basis-" + klasse)
    if os.path.isdir(ziel):
        return ziel
    print("--- Kontrollbasis %s ---" % klasse)
    if klasse in ("ohneskill", "ohnepack"):
        kopieren(QUELLE, ziel)
        # 🔴 `ohnepack` GEHT VORAN, NICHT HINTERHER (K-87, D-242). Die drei Teile
        # der Aktivierung werden aus dem PACKVERZEICHNIS abgeleitet. Liefe der
        # Skillschnitt zuerst, waere es leer und der Korbeintrag bliebe stehen.
        if klasse == "ohnepack":
            for _art, pack in packmenge():
                bericht = packaktivierung.entfernen(ziel, CLIENT, pack)
                print("  Pack %s: %d Traeger entfernt, %d Korbeintrag(e) "
                      "gestrichen" % (pack, len(bericht["entfernt"]),
                                      len(bericht["gestrichen"])))
        anzahl = packaktivierung.skillschnitt(ziel)
        print("  keine SKILL.md mehr im Baum (%d Ablagen geleert), Regelschicht "
              "und Checklisten stehen" % anzahl)
    else:
        zwischen = ziel + "-roh"
        kopieren(QUELLE, zwischen)
        aus = lauf([sys.executable, os.path.join(HIER, "k-bauen-b3.py"),
                    klasse, zwischen, ziel])
        print("  " + "\n  ".join(aus.strip().split("\n")[-6:]))
        weg(zwischen)
        # 🔴 DER WAECHTER, DEN BUENDEL 4 NICHT BRAUCHTE. Ein bedeutungs-
        # geschnittener Kontrollbaum muss den SKILL WEITER TRAGEN - geschnitten
        # ist die Schranke, nicht der Gegenstand. Faellt der Skill mit, misst der
        # Kontrollauf sein Fehlen statt das Fehlen der Schranke, und die Zelle
        # bekaeme eine Zurechnung, die aus etwas anderem folgt.
        skills, _packs = ablage.skillmenge(sorted(ZUORDNUNG))
        for name in skills:
            pfad = os.path.join(ziel, ".claude", "skills", name, "SKILL.md")
            if not os.path.isfile(pfad):
                raise SystemExit(
                    "ABBRUCH: der Zuschnitt %s hat %s mitgenommen. Ein "
                    "bedeutungsgeschnittener Kontrollauf misst das Fehlen der "
                    "SCHRANKE, nicht das Fehlen des Skills." % (klasse, name))
        print("  Waechter: der gemessene Skill steht weiter im Baum (%s)"
              % ", ".join(skills))
    if os.path.exists(os.path.join(ziel, ".git")):
        raise SystemExit("ABBRUCH: die Kontrollbasis traegt ein .git")
    return ziel


def praeparation(baum, kennung):
    """Setzt eine registrierte Praeparation ueber tools/praeparationen.py IM BAUM.

    🔴 Nicht von Hand: Das Skript traegt den Waechter gegen den Loesungsverrat
    (D-142) - und seit 0.82.0 kennt dieser Waechter die Kennungsfamilie `RE-` als
    FORM, nicht als Aufzaehlung (D-246).
    """
    skript = os.path.join(baum, "tools", "praeparationen.py")
    p = subprocess.run([sys.executable, skript, "--setzen", kennung], cwd=baum,
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace",
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    if p.returncode != 0:
        raise SystemExit("ABBRUCH praeparationen.py --setzen %s:\n%s%s"
                         % (kennung, p.stdout, p.stderr))
    # Die Sicherung einer `textersatz`- oder `ersetzen`-Praeparation darf nicht im
    # Baum bleiben: Sie stuende in `git status` und waere ein Fund, den keine
    # Zelle meint.
    weg(os.path.join(baum, "tools", "praeparationen", "vorher"))
    for zeile in p.stdout.splitlines():
        if zeile.startswith("gesetzt: "):
            return zeile.split("  ")[0][len("gesetzt: "):].strip().replace(os.sep, "/")
    raise SystemExit("ABBRUCH: praeparationen.py hat kein Ziel gemeldet (%s)" % kennung)


def minimale_historie(baum):
    """`git init`, ein Commit, synthetischer Autor - fuer jeden Baum dieses Buendels."""
    weg(os.path.join(baum, ".git"))
    lauf(["git", "init", "-q", "-b", "main"], cwd=baum)
    lauf(["git", "config", "user.name", AUTOR[0]], cwd=baum)
    lauf(["git", "config", "user.email", AUTOR[1]], cwd=baum)
    lauf(["git", "config", "core.autocrlf", "false"], cwd=baum)
    lauf(["git", "add", "-A"], cwd=baum)
    lauf(["git", "commit", "-q", "-m", "Uebungsstand der Bibliotheksverwaltung"],
         cwd=baum, autor=0)
    zeilen = lauf(["git", "log", "--all", "--format=%an <%ae> | %cn <%ce>"],
                  cwd=baum).splitlines()
    fremd = [z for z in zeilen if z.count(ERLAUBTE_DOMAENE) < 2]
    if fremd:
        raise SystemExit("ABBRUCH: Angabe ausserhalb %s: %r"
                         % (ERLAUBTE_DOMAENE, fremd))
    status = lauf(["git", "status", "--short"], cwd=baum).strip()
    if status:
        raise SystemExit("ABBRUCH: `git status` ist nicht leer (%d Zeilen) - eine "
                         "Zelle ohne Aenderungssatz darf keinen Fund zeigen, den "
                         "sie nicht meint:\n%s" % (len(status.split("\n")), status))
    return lauf(["git", "rev-parse", "--short", "HEAD"], cwd=baum).strip()


def baum_bauen(kennung):
    kontroll = kennung.startswith("k")
    kern = kennung[1:] if kontroll else kennung
    if kern not in ZUORDNUNG:
        raise SystemExit("ABBRUCH: unbekannte Kennung %r" % kennung)
    klasse = ZUORDNUNG[kern]
    quelle = klassenbasis(klasse) if kontroll else QUELLE
    ziel = os.path.join(BASIS, kennung)
    kopieren(quelle, ziel)

    # --- Die je Meszbaum gesetzten Praeparationen, VOR dem ersten Commit ------
    gesetzt = []
    for kenn in PRAEPARATIONEN.get(kern, []):
        gesetzt.append(praeparation(ziel, kenn))

    kurz = minimale_historie(ziel)

    # --- Waechter je Baum ----------------------------------------------------
    for pflicht in (os.path.join(".claude", "settings.json"), "CLAUDE.md", ".git"):
        if not os.path.exists(os.path.join(ziel, pflicht)):
            raise SystemExit("ABBRUCH: %s fehlt in %s" % (pflicht, ziel))
    # .devin darf in KEINER Referenz vorkommen - sonst sagt die Historie, dass
    # hier das Client Pack gewechselt wurde (D-213). Geprueft wird der
    # PFADANFANG, nicht das Vorkommen: `leitwerk-core/clients/devin-desktop/`
    # gehoert dem Kern und hat mit dem Packwechsel nichts zu tun.
    verfolgt = lauf(["git", "ls-files"], cwd=ziel)
    if any(z.startswith(".devin/") for z in verfolgt.splitlines()):
        raise SystemExit("ABBRUCH: die Historie von %s fuehrt .devin/ - der "
                         "Packwechsel lief NACH dem git init (D-213)" % kennung)
    # 🔴 DIE PRAEPARATION MUSS IM COMMIT STEHEN, nicht nur auf der Platte: Der
    # Lauf recherchiert den Stand, und `git status` soll leer sein.
    for pfad in gesetzt:
        if pfad not in verfolgt.replace(os.sep, "/"):
            raise SystemExit("ABBRUCH: die Praeparation %s steht nicht in der "
                             "Historie von %s" % (pfad, kennung))
    print("%-12s aus %-20s Klasse %-9s %s%s"
          % (kennung, os.path.basename(quelle), klasse, kurz,
             "  Praeparation: " + ", ".join(gesetzt) if gesetzt else ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("kennungen", nargs="*")
    ap.add_argument("--liste", action="store_true")
    ap.add_argument("--zellen", action="store_true",
                    help="nur die Kennungen des Zuschnitts, eine je Zeile - die "
                         "Quelle, aus der der Baumbau seine Skillmenge ableitet "
                         "(D-237)")
    args = ap.parse_args()

    if args.zellen:
        for k in sorted(ZUORDNUNG):
            print(k)
        return 0

    if args.liste:
        for k in sorted(ZUORDNUNG):
            print("%-10s %-10s %s" % (k, ZUORDNUNG[k],
                                      ", ".join(PRAEPARATIONEN.get(k, []))))
        klassen = sorted(set(ZUORDNUNG.values()))
        print("\n%d Zellen, %d Kontrollklassen (%s)"
              % (len(ZUORDNUNG), len(klassen), " ".join(klassen)))
        print("%d Baeume: %d Hauptlaeufe + %d Kontrollaeufe"
              % (2 * len(ZUORDNUNG), len(ZUORDNUNG), len(ZUORDNUNG)))
        skills, packs = ablage.skillmenge(sorted(ZUORDNUNG))
        print("gemessene Skills (abgeleitet): %s" % ", ".join(skills))
        print("dafuer zu aktivierende Packs:  %s"
              % (", ".join("%s/%s" % p for p in packs) or "keine"))
        print("je Meszbaum gesetzte Praeparationen: %s"
              % ", ".join(sorted({x for v in PRAEPARATIONEN.values() for x in v})))
        return 0

    if not os.path.isdir(QUELLE):
        raise SystemExit("ABBRUCH: %s fehlt - erst umgebungen-bauen-b5.py" % QUELLE)
    gewuenscht = args.kennungen
    if not gewuenscht:
        gewuenscht = sorted(ZUORDNUNG) + ["k" + k for k in sorted(ZUORDNUNG)]
    for kennung in gewuenscht:
        baum_bauen(kennung)
    print("OK -", len(gewuenscht), "Baeume")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
