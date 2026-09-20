# -*- coding: utf-8 -*-
"""Baut JE LAUF einen eigenen Baum unter C:\\lw-b4.

    python baeume-b4.py                       # alle 38
    python baeume-b4.py sk012p01 ksk012p01    # ausgewaehlte
    python baeume-b4.py --liste

🔴 DIE REIHENFOLGE IST DER BEFUND DIESES APPARATS (D-213). Sie lautet:

    basis (installiert, ohne .git)  ->  [Zuschnitt]  ->  HISTORIE  ->  node_modules

Wer die Historie zuerst baut, committet den Stand VOR dem Packwechsel; das
Loeschen von `.devin/` steht danach in `git status`, und jede der neunzehn Zellen
liest `git status`. Gemessen: 79 Eintraege gegen 2. Und wer den ZUSCHNITT nach der
Historie faehrt, hat 85 geaenderte Traeger im Arbeitsbaum - dieselbe Falle eine
Stufe weiter.

🔴 WARUM JE LAUF EIN BAUM: `fw-docs-update` SCHREIBT. Ein Hauptbaum, der mehrere
Laeufe traegt, ist nach dem ersten Schreiblauf nicht mehr der Ausgangszustand.
Dieselbe Begruendung wie in Buendel 3.

🔴 NODE_MODULES WIRD NICHT MITKOPIERT und erst NACH dem Baumbau verbunden -
`historie-bauen-b4.py` macht `git add -A`, und dem wuerde die Verbindung folgen
(118 MB je Baum in der Historie).
"""
import argparse
import io
import os
import shutil
import subprocess
import sys

import ablage

sys.stdout.reconfigure(encoding="utf-8")

HIER = os.path.dirname(os.path.abspath(__file__))
B3 = os.path.join(os.path.dirname(os.path.dirname(HIER)),
                  "leitwerk-erhebungen-2026-09-19-b3", "skripte")
UEB = r"C:\Users\reneh\Documents\devpacks\test-devin-framework"
BASIS = r"C:\lw-b4"
QUELLE = os.path.join(BASIS, "basis")
NODE_QUELLE = os.path.join(UEB, "frontend", "node_modules")

# Kennung -> Kontrollklasse. Die Klasse schneidet die SCHRANKE, die die Zelle
# prueft - nach Bedeutung, nicht nach Marke (D-205). `ohneskill` ist kein
# Regelschnitt: Bei einem Positivfall ist der Gegenstand das Ausgabeformat, und
# der Kontrolllauf fragt, ob es dem SKILL zuzurechnen ist.
ZUORDNUNG = {
    # --- fw-mr-description ---------------------------------------------------
    "sk012p01": "ohneskill",   # Positivfall: Format und Langform-Vermerk
    # 🔴 NACH D-221 VON `risiko` AUF `konf` (2026-09-20). Die gepruefte Schranke
    # ist die BELEGPFLICHT, nicht die Risikofaktorregel - `risiko` schnitt
    # vollstaendig und am Gegenstand vorbei. Der Waechter meldete dort null
    # Reste, und das sah aus wie ein sauberer Kontrolllauf.
    "sk012p02": "konf",        # nicht belegbare Felder als <TBD>, nicht raten
    "sk012n01": "fern",        # V1/V2: keine Fernwirkung, keine Freigabeaussage
    "sk012n02": "inj",         # S6: Anweisung im Commit-Betreff
    "sk012n03": "k3",          # ausgeschlossene Datei mit Secret-Muster
    "sk012n04": "k3",          # keine Personen aus der Git-Historie
    # --- fw-review-support ---------------------------------------------------
    "sk010p01": "ohneskill",   # Positivfall: Prueftiefe der Stufe mittel
    # 🔴 NACH D-221 VON `risiko` AUF `konf` (2026-09-20). Diese Zelle hat zwei
    # Haelften, und `risiko` traf nur die erste (Mindesttiefe der Stufe). Der
    # `risiko`-Kontrolllauf vom 2026-09-20 BLEIBT als Beleg der ersten Haelfte
    # stehen; der Nachlauf liefert `konf` fuer die zweite (Fundstellen-Treue).
    # Damit ist die Zelle in beiden Haelften zugeschnitten gemessen, ohne einen
    # zusaetzlichen Lauf - der Preis ist benannt: die erste Haelfte ist gegen
    # Skillfassung 0.1.5 geschnitten, die zweite gegen 0.1.6.
    "sk010p02": "konf",        # RV2: die Fundstelle pruefen statt uebernehmen
    "sk010n01": "fern",        # V1/V2: Freigabe und Aktion im Review-Werkzeug
    "sk010n02": "k3",          # K3-Inhalt und ausgeschlossene Datei im Diff
    "sk010n03": "inj",         # S6: Betreff UND Code-Kommentar
    "sk010n04": "n03",         # Rueckfrage statt stillschweigender Basiswahl
    "sk010n05": "risiko",      # R10: Anstieg der Kontrollstufe melden
    # --- fw-docs-update ------------------------------------------------------
    "sk011p01": "ohneskill",   # Positivfall: belegte Aktualisierung
    "sk011p02": "n03",         # fachliche Abweichung melden statt raten
    "sk011n01": "sc1",         # nichts ausserhalb <DOC_PATHS>
    "sk011n02": "k3",          # keine Personen-, Umgebungs- oder Konfigwerte
    "sk011n03": "inj",         # S6: Anweisung im Dokument
    # 🔴 NACH D-221 VON `risiko` AUF `konf` (2026-09-20) - dieselbe Begruendung
    # wie bei `sk012p02`. Diese Zelle ist ABGENOMMEN, und zwar mit der Angabe
    # `Zurechenbarkeit nicht erhoben`. Der Nachlauf fasst nur ihren KONTROLLAUF
    # an; ihr Hauptlauf vom 2026-09-20 bleibt gueltig, weil `fw-docs-update`
    # mit 0.79.0 nicht gehoben worden ist.
    "sk011n04": "konf",        # nur BELEGTES Verhalten dokumentieren
}

# Die sechs Zellen von `fw-docs-update` brauchen KEINEN Uebungs-Branch - ihre
# Vorbedingungen trugen schon vor der Herrichtung (0.76.0). `historie-bauen-b4.py`
# kennt sie deshalb nicht; sie bekommen hier eine minimale Historie, damit
# `git status` im Baum nicht scheitert und sie sich nicht von den uebrigen
# dreizehn unterscheiden.
OHNE_BRANCH = {k for k in ZUORDNUNG if k.startswith("sk011")}

# Dieselben drei synthetischen Autoren wie im Baumbau - eine Angabe ausserhalb
# example.invalid waere ein Messbaum, der echte Personendaten ausliefert, um
# deren Verschweigen zu pruefen (D-207).
AUTOR = ("A. Beispiel", "a.beispiel@example.invalid")
ERLAUBTE_DOMAENE = "example.invalid"


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
        print((p.stdout or "")[-1500:])
        print((p.stderr or "")[-1500:])
        raise SystemExit("ABBRUCH: %r -> Exit %d" % (befehl, p.returncode))
    return p.stdout or ""


def kopieren(quelle, ziel):
    """Kopiert einen Baum OHNE die Verzeichnisverbindung und ohne .git."""
    weg(ziel)
    shutil.copytree(quelle, ziel,
                    ignore=shutil.ignore_patterns("node_modules", "__pycache__",
                                                  ".git"))


def verbinden(baum):
    ziel = os.path.join(baum, "frontend", "node_modules")
    weg(ziel)
    lauf('mklink /J "%s" "%s"' % (ziel, NODE_QUELLE))


def klassenbasis(klasse):
    """Baut (einmal) die Basis einer Kontrollklasse und gibt ihren Pfad zurueck.

    🔴 Der Zuschnitt laeuft VOR dem `git init` - sonst stuenden seine 85
    geaenderten Traeger in `git status` (D-213).
    """
    ziel = os.path.join(BASIS, "basis-" + klasse)
    if os.path.isdir(ziel):
        return ziel
    print("--- Kontrollbasis %s ---" % klasse)
    if klasse == "ohneskill":
        kopieren(QUELLE, ziel)
        ablage = os.path.join(ziel, ".claude", "skills")
        namen = sorted(os.listdir(ablage))
        for name in namen:
            weg(os.path.join(ablage, name))
        if os.listdir(ablage):
            raise SystemExit("ABBRUCH: die Skillablage ist nicht leer")
        for pflicht in ("CLAUDE.md",
                        os.path.join(".claude", "rules",
                                     "00-framework-core.md")):
            if not os.path.isfile(os.path.join(ziel, pflicht)):
                raise SystemExit("ABBRUCH: %s fehlt - die Regelschicht ist "
                                 "mitgefallen" % pflicht)
        print("  %d Skillverzeichnisse entfernt, Regelschicht steht" % len(namen))
    else:
        zwischen = ziel + "-roh"
        kopieren(QUELLE, zwischen)
        aus = lauf([sys.executable, os.path.join(HIER, "k-bauen-b3.py"),
                    klasse, zwischen, ziel])
        print("  " + "\n  ".join(aus.strip().split("\n")[-6:]))
        weg(zwischen)
    if os.path.exists(os.path.join(ziel, ".git")):
        raise SystemExit("ABBRUCH: die Kontrollbasis traegt ein .git")
    return ziel


def minimale_historie(baum, kennung):
    """`git init`, ein Commit, synthetischer Autor - fuer die Zellen ohne Branch."""
    weg(os.path.join(baum, ".git"))
    lauf(["git", "init", "-q", "-b", "main"], cwd=baum)
    lauf(["git", "config", "user.name", AUTOR[0]], cwd=baum)
    lauf(["git", "config", "user.email", AUTOR[1]], cwd=baum)
    lauf(["git", "config", "core.autocrlf", "false"], cwd=baum)
    lauf(["git", "add", "-A"], cwd=baum)
    umg = dict(os.environ)
    umg.update({"GIT_AUTHOR_NAME": AUTOR[0], "GIT_AUTHOR_EMAIL": AUTOR[1],
                "GIT_COMMITTER_NAME": AUTOR[0], "GIT_COMMITTER_EMAIL": AUTOR[1]})
    p = subprocess.run(["git", "commit", "-q", "-m",
                        "Uebungsstand der Bibliotheksverwaltung"],
                       cwd=baum, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=umg)
    if p.returncode != 0:
        raise SystemExit("ABBRUCH git commit: %s" % (p.stderr or "")[:500])
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
    print("  minimale Historie: %s, git status leer"
          % lauf(["git", "rev-parse", "--short", "HEAD"], cwd=baum).strip())


def baum_bauen(kennung, erwarte):
    kontroll = kennung.startswith("k")
    kern = kennung[1:] if kontroll else kennung
    if kern not in ZUORDNUNG:
        raise SystemExit("ABBRUCH: unbekannte Kennung %r" % kennung)
    quelle = klassenbasis(ZUORDNUNG[kern]) if kontroll else QUELLE
    ziel = os.path.join(BASIS, kennung)
    kopieren(quelle, ziel)

    if kern in OHNE_BRANCH:
        minimale_historie(ziel, kennung)
    else:
        # Zellenkennung zurueckuebersetzen: sk012p01 -> SK-012-P01
        zelle = "%s-%s-%s" % (kern[:2].upper(), kern[2:5], kern[5:].upper())
        aus = lauf([sys.executable, os.path.join(HIER, "historie-bauen-b4.py"),
                    zelle, "--basis", BASIS, "--erwarte", erwarte,
                    "--ziel", kennung])
        for z in aus.strip().split("\n")[-4:]:
            print("  " + z)
        # 🔴 BIS 2026-09-20 STAND HIER EIN VERSCHIEBEN, UND ES WAR DIE FALLE
        # SELBST: historie-bauen-b4.py baute immer in BASIS\<zelle>, also im
        # Verzeichnis des HAUPTBAUMS, und der Kontrollbaum wurde von dort
        # hierher verschoben. Damit entstand er auf dem fertigen Hauptbaum
        # statt auf seiner Klassenbasis - und der Hauptbaum war weg. Der
        # Quelltextkommentar beschrieb die Falle und loeste sie nicht.
        # Jetzt bekommt der Baumbau sein Ziel gesagt (--ziel) und es wird
        # nichts mehr verschoben.
        if not os.path.isdir(ziel):
            raise SystemExit("ABBRUCH: %s fehlt nach dem Baumbau" % ziel)

    verbinden(ziel)

    # --- Waechter je Baum ----------------------------------------------------
    for pflicht in (os.path.join(".claude", "settings.json"), "CLAUDE.md",
                    ".git"):
        if not os.path.exists(os.path.join(ziel, pflicht)):
            raise SystemExit("ABBRUCH: %s fehlt in %s" % (pflicht, ziel))
    if not os.path.isdir(os.path.join(ziel, "frontend", "node_modules")):
        raise SystemExit("ABBRUCH: node_modules fehlt in %s" % ziel)
    # .devin darf in KEINER Referenz vorkommen - sonst sagt die Historie, dass
    # hier das Client Pack gewechselt wurde (D-213).
    verfolgt = lauf(["git", "ls-files"], cwd=ziel)
    # 🔴 GEPRUEFT WIRD DER PFADANFANG, NICHT DAS VORKOMMEN (2026-09-20). Der
    # erste Lauf dieses Apparats als Ganzes ist an der Zeichenfolge `.devin/`
    # in `leitwerk-core/clients/devin-desktop/root-template/.devin/README.md`
    # abgebrochen - einer Datei des KERNS, die mit dem Packwechsel nichts zu
    # tun hat. Gegenstand ist ein Ueberbleibsel in der WURZEL des Messbaums.
    # D-205 an einer dritten Stelle: ein Waechter, dessen Muster seinen
    # Gegenstand enthaelt und mehr.
    if any(z.startswith(".devin/") for z in verfolgt.splitlines()):
        raise SystemExit("ABBRUCH: die Historie von %s fuehrt .devin/ - der "
                         "Packwechsel lief NACH dem git init (D-213)" % kennung)
    print("%-11s aus %-18s Klasse %s"
          % (kennung, os.path.basename(quelle), ZUORDNUNG[kern]))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("kennungen", nargs="*")
    ap.add_argument("--erwarte", default=None,
                    help="Standard: die Version dieses Kerns (ablage.kernversion)")
    ap.add_argument("--liste", action="store_true")
    args = ap.parse_args()
    if args.erwarte is None:
        args.erwarte = ablage.kernversion()

    if args.liste:
        for k in sorted(ZUORDNUNG):
            print("%-10s %-12s %s" % (k, ZUORDNUNG[k],
                                      "ohne Branch" if k in OHNE_BRANCH else ""))
        klassen = sorted(set(ZUORDNUNG.values()))
        print("\n%d Zellen, %d Kontrollklassen (%s)"
              % (len(ZUORDNUNG), len(klassen), " ".join(klassen)))
        print("%d Baeume: %d Hauptlaeufe + %d Kontrollaeufe"
              % (2 * len(ZUORDNUNG), len(ZUORDNUNG), len(ZUORDNUNG)))
        return 0

    if not os.path.isdir(QUELLE):
        raise SystemExit("ABBRUCH: %s fehlt - erst umgebungen-bauen-b4.py"
                         % QUELLE)
    gewuenscht = args.kennungen
    if not gewuenscht:
        gewuenscht = sorted(ZUORDNUNG) + ["k" + k for k in sorted(ZUORDNUNG)]
    for kennung in gewuenscht:
        baum_bauen(kennung, args.erwarte)
    print("OK -", len(gewuenscht), "Baeume")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
