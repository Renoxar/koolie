#!/usr/bin/env python3
"""
Das Mandat fuer Modus M6 (CR-2026-156, D-446, D-447) - erteilen, anzeigen, beenden,
und der Abgleich des Overlays (D-452).

Ein Mandat ist die Erlaubnis eines MENSCHEN, dass der KI-Client fuer eine begrenzte Zeit
Entscheidungen in das Project Overlay eintraegt, die der Mensch in der Sitzung getroffen
hat. Die Entscheidung bleibt beim Menschen (V3, V10); das Eintragen darf der Client
uebernehmen. Die Pruefung ist der Merge Request, den der Mensch ohnehin freigibt (V1).

    python .koolie/core/mandat.py erteilen --rolle Architekt --umfang overlay --minuten 60
    python .koolie/core/mandat.py status
    python .koolie/core/mandat.py beenden      (gleicht danach die Laufzeitfassung ab)
    python .koolie/core/mandat.py abgleichen
    python .koolie/core/mandat.py modus M2 --ablage docs/plaene --minuten 120
    python .koolie/core/mandat.py modus M1
    python .koolie/core/mandat.py modus aus

DIE MODUSBINDUNG (D-501, K-179). Bis 1.20.1 galten die Modusgrenzen ausser M6 nur
normativ. 'modus M1' bindet den Nur-Lese-Modus an den Schutz-Hook: Er sperrt jeden
Schreibaufruf. 'modus M2 --ablage <pfad>' laesst nur das Schreiben unter der Plan-Ablage
zu. Die Bindung liegt neben dem Mandat (.git/koolie-modus.json), ist befristet und nur
vom Menschen zu setzen. Grenze: Ein Shell-Befehl, der schreibt, entgeht ihr (D-30).

WARUM EIN BEFEHL IM EIGENEN TERMINAL: Der Schutz-Hook sperrt diese Datei und die
Mandatsdatei fuer jede nicht lesende Operation des Clients - bis auf 'status'. Ein Satz
im Chat ("ich erteile dir ein Mandat") erreicht den Hook nicht, und ein Client, der sich
das Mandat selbst geben koennte, haette keines.

WO ES LIEGT: im Git-Verzeichnis des Projekts (.git/koolie-mandat.json), nicht im
Arbeitsbaum. So kann es nicht eingecheckt werden und auf einem anderen Arbeitsplatz
gelten. Ohne Git-Verzeichnis gibt es kein Mandat.

DER ABGLEICH (D-452). Ein Overlay-Wert steht in bis zu vier Traegern: OVERLAY.md, dem
Manifest, der immer geladenen Laufzeitfassung (<RULES_DIR>/20-project-overlay.md) und der
Berechtigungsdatei. Die beiden letzten liegen in der Laufzeitschicht, die der Client nie
schreibt - auch nicht mit Mandat. Bis 1.16.0 zog sie der Mensch von Hand nach, und genau
dort liefen die Werte auseinander (Befund A3 aus dem ersten Projekteinsatz: die Version
im Steckbrief ersetzt statt geaendert, die Laufzeitfassung mit einem anderen Wert). Der
Abgleich uebernimmt Status, Version und die fuenf Pfadlisten aus OVERLAY.md in die
Laufzeitfassung und die Version ins Manifest. Die Berechtigungsdatei SCHREIBT er nicht:
Er nennt die Regeln, die dort fehlen (Pruefungen 59 und 89) - eine Aenderung an ihr ist
eine Aenderung der Berechtigung selbst (V6), und ihre Form ist je Pack verschieden.

Die Werte (Dateiname, Umfaenge, Hoechstdauer) stehen gleichlautend im Schutz-Hook;
Pruefung 99 haelt beide gleich.
"""
import argparse
import datetime
import io
import json
import os
import re
import subprocess
import sys

CORE_REL = ".koolie/core"
MANDAT_DATEI = "koolie-mandat.json"
MANDAT_HOECHSTDAUER_MIN = 480
MANDAT_UMFAENGE = {
    "overlay": ".koolie/project-overlay/",
    "dokumente": ".koolie/project-overlay/documents/",
}
# Die Modusbindung (CR-2026-164, D-501, K-179): M1 oder M2 fuer eine begrenzte Zeit an den
# Schutz-Hook binden. Dieselbe Hoechstdauer und derselbe Ort wie das Mandat.
MODUS_DATEI = "koolie-modus.json"
MODUS_GEBUNDEN = ("M1", "M2")

_KERN = os.path.dirname(os.path.abspath(__file__))
PROJEKTWURZEL = os.path.realpath(os.path.dirname(os.path.dirname(_KERN)))
ZEITFORMAT = "%Y-%m-%dT%H:%M:%SZ"
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
PFADPLATZHALTER = ("<ALLOWED_PATHS>", "<EXCLUDED_PATHS>", "<READ_ONLY_PATHS>",
                   "<TEST_PATHS>", "<DOC_PATHS>")


def jetzt() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)


def git_verzeichnis():
    """Wie im Schutz-Hook: '.git' als Verzeichnis oder als Datei mit 'gitdir:'."""
    punkt_git = os.path.join(PROJEKTWURZEL, ".git")
    if os.path.isdir(punkt_git):
        return punkt_git
    if os.path.isfile(punkt_git):
        with io.open(punkt_git, encoding="utf-8") as fh:
            inhalt = fh.read().strip()
        if inhalt.lower().startswith("gitdir:"):
            ziel = inhalt[len("gitdir:"):].strip()
            if not os.path.isabs(ziel):
                ziel = os.path.join(PROJEKTWURZEL, ziel)
            return os.path.realpath(ziel)
    return None


def mandatspfad():
    gd = git_verzeichnis()
    return os.path.join(gd, MANDAT_DATEI) if gd else None


def lesen(pfad):
    try:
        with io.open(pfad, encoding="utf-8") as fh:
            daten = json.load(fh)
        return daten if isinstance(daten, dict) else None
    except (OSError, ValueError):
        return None


def gueltiges_mandat():
    """Das gueltige Mandat - dieselben Bedingungen wie im Schutz-Hook - oder None."""
    pfad = mandatspfad()
    daten = lesen(pfad) if pfad else None
    if not daten:
        return None
    umfang = daten.get("umfang")
    if (not isinstance(daten.get("rolle"), str) or not daten["rolle"].strip()
            or not isinstance(umfang, list) or not umfang
            or not all(isinstance(u, str) and u in MANDAT_UMFAENGE for u in umfang)):
        return None
    try:
        ende = datetime.datetime.strptime(str(daten.get("bis")), ZEITFORMAT)
    except ValueError:
        return None
    rest = ende - jetzt()
    if (rest.total_seconds() <= 0
            or rest > datetime.timedelta(minutes=MANDAT_HOECHSTDAUER_MIN + 1)):
        return None
    projekt = daten.get("projekt")
    if (not isinstance(projekt, str) or os.path.normcase(os.path.realpath(projekt))
            != os.path.normcase(PROJEKTWURZEL)):
        return None
    daten["_rest_min"] = int(rest.total_seconds() // 60) + 1
    return daten


# ------------------------------------------------------------------ Abgleich (D-452)

def _validator():
    """Das Validatormodul. Seine Leseroutinen sind dieselben, mit denen die Pruefungen
    13, 59 und 89 die Traeger vergleichen - ein zweiter Parser hier waere eine zweite
    Meinung darueber, was ein Wert ist."""
    import importlib.util
    pfad = os.path.join(_KERN, "tests", "scripts", "validate-framework.py")
    spec = importlib.util.spec_from_file_location("koolie_validator", pfad)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


def _tabellenwert(text: str, feld: str):
    # Dieselbe Lesart wie overlay_status.py und Pruefung 13: das erste Token der Zelle,
    # auch wenn ihm ein Zusatz folgt ("`aktiv` (siehe Abschnitt 21)").
    m = re.search(r"^\|\s*" + re.escape(feld) + r"\s*\|\s*`?([^`|]+)", text, re.M)
    return m.group(1).strip() if m else None


def _zeile_setzen(text: str, token: str, werte: list) -> tuple:
    """Den Wert hinter `token` in der ersten Zeile, die ihn nennt, ersetzen.

    Die Zeile behaelt Anfang und Nachsatz (' · ' oder ' – '); ersetzt wird nur, was
    Pruefung 89 als Wert liest. Rueckgabe: (neuer Text, geaendert?)."""
    zeilen = text.split("\n")
    for i, zeile in enumerate(zeilen):
        if token not in zeile:
            continue
        vor, rest = zeile.split(token, 1)
        m = re.match(r"(\)?:?\s*)(.*?)((?: · | – ).*)?$", rest)
        if not m:
            return text, False
        neu_wert = ", ".join("`%s`" % w for w in werte) if werte else "`keine`"
        neu = vor + token + m.group(1) + neu_wert + (m.group(3) or "")
        if neu == zeile:
            return text, False
        zeilen[i] = neu
        return "\n".join(zeilen), True
    return text, False


def _listenwert_setzen(text: str, feld: str, wert: str) -> tuple:
    """'- <feld>: `alt`' -> '- <feld>: `wert`' (erste Fundstelle)."""
    muster = re.compile(r"^(-?\s*" + re.escape(feld) + r":\s*)`[^`]*`", re.M)
    m = muster.search(text)
    if not m or m.group(0) == m.group(1) + "`%s`" % wert:
        return text, False
    return text[:m.start()] + m.group(1) + "`%s`" % wert + text[m.end():], True


def abgleichen(_args=None) -> int:
    """Overlay-Werte in Laufzeitfassung und Manifest uebernehmen (D-452)."""
    V = _validator()
    man = V.detect_client(PROJEKTWURZEL)
    overlay_pfad = os.path.join(PROJEKTWURZEL, ".koolie", "project-overlay", "OVERLAY.md")
    if not os.path.isfile(overlay_pfad):
        print("Kein Overlay unter .koolie/project-overlay/OVERLAY.md - nichts abzugleichen.")
        return 1
    rel_rt = "%s/%s" % (man["pack_runtime_dir"], V.regeldatei(man, "20-project-overlay.md"))
    rt_pfad = os.path.join(PROJEKTWURZEL, *rel_rt.split("/"))
    if not os.path.isfile(rt_pfad):
        print("Keine Laufzeitfassung unter %s - nichts abzugleichen." % rel_rt)
        return 1
    quelle = V.read(overlay_pfad)
    roh = io.open(rt_pfad, encoding="utf-8", newline="").read()
    crlf = "\r\n" in roh
    text = roh.replace("\r\n", "\n")
    geaendert, offen = [], []

    status = _tabellenwert(quelle, "Overlay-Status")
    if status in ("aktiv", "inaktiv"):
        text, ja = _listenwert_setzen(text, "Overlay-Status", status)
        if ja:
            geaendert.append("Overlay-Status -> %s" % status)
    else:
        offen.append("Overlay-Status im Steckbrief ist nicht 'aktiv' oder 'inaktiv' (%r)"
                     % status)
    version = _tabellenwert(quelle, "Overlay-Version")
    if version and SEMVER.match(version):
        text, ja = _listenwert_setzen(text, "Overlay-Version", version)
        if ja:
            geaendert.append("Overlay-Version -> %s" % version)
    else:
        offen.append("Overlay-Version im Steckbrief ist keine Version der Form x.y.z (%r) - "
                     "steht dort vielleicht eine Zeile des Aenderungsverlaufs?" % version)

    for ph in PFADPLATZHALTER:
        if ph == "<EXCLUDED_PATHS>":
            werte = V._p59_globs(V._p56_ausgeschlossen(quelle))
            if not werte or any(V.TBD_RE.search(w) for w in werte):
                werte = None
        else:
            _gefunden, werte = V._p89_quelle(quelle, ph)
        # Kein Wert (leer oder "keine"): die Laufzeitfassung behaelt ihren Wortlaut -
        # gemessen am Pilot, dessen "keine" sonst zu `keine` wurde.
        if not werte:
            continue
        text, ja = _zeile_setzen(text, "`%s`" % ph, werte)
        if ja:
            geaendert.append("%s -> %s" % (ph, ", ".join(werte) or "keine"))

    if any(not g.startswith("overlay-manifest") for g in geaendert):
        io.open(rt_pfad, "w", encoding="utf-8", newline="").write(
            text.replace("\n", "\r\n") if crlf else text)

    mpfad = os.path.join(PROJEKTWURZEL, ".koolie", "project-overlay", "overlay-manifest.yaml")
    if version and SEMVER.match(version) and os.path.isfile(mpfad):
        mroh = io.open(mpfad, encoding="utf-8", newline="").read()
        mneu = re.sub(r'^(overlay_version:\s*)"?[^"\r\n]*"?', r'\g<1>"%s"' % version, mroh,
                      count=1, flags=re.M)
        if mneu != mroh:
            io.open(mpfad, "w", encoding="utf-8", newline="").write(mneu)
            geaendert.append("overlay-manifest.yaml: overlay_version -> %s" % version)

    print("Abgleich des Overlays (%s):" % rel_rt)
    for g in geaendert:
        print("  geaendert: %s" % g)
    if not geaendert:
        print("  nichts zu aendern - die Traeger stimmen ueberein.")
    for o in offen:
        print("  offen:     %s" % o)
    lauf = subprocess.run([sys.executable,
                           os.path.join(_KERN, "tests", "scripts", "validate-framework.py"),
                           "--root", PROJEKTWURZEL, "--strict-overlay"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace",
                          env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    rechte = [z for z in lauf.stdout.splitlines()
              if z.startswith("FEHLER") and man["permissions_file"] in z]
    if rechte:
        print("Die Berechtigungsdatei %s schreibt der Abgleich nicht (V6). Dort fehlt:"
              % man["permissions_file"])
        for z in rechte:
            print("  " + z)
    letzte = [z for z in lauf.stdout.splitlines() if z.startswith("Ergebnis:")]
    print("Validator --strict-overlay: %s" % (letzte[-1] if letzte else "ohne Ergebnis"))
    return 1 if offen else 0


# ------------------------------------------------------------------ Befehle

def erteilen(args) -> int:
    pfad = mandatspfad()
    if not pfad:
        print("Gesperrt: Mandat ohne Git-Repositorium.\n"
              "Warum: Das Mandat setzt voraus, dass jede Aenderung im Merge Request geprueft "
              "wird - ohne Git gibt es diese Pruefung nicht.\n"
              "Loesung: Das Projekt als Git-Repositorium fuehren (git init) und erneut "
              "erteilen.\n"
              "Folge: Bis dahin bleibt das Overlay fuer den KI-Client gesperrt.")
        return 1
    umfang = [u.strip() for u in args.umfang.split(",") if u.strip()]
    falsch = [u for u in umfang if u not in MANDAT_UMFAENGE]
    if not umfang or falsch:
        print("Unbekannter Umfang: %s. Moeglich: %s."
              % (", ".join(falsch) or "(leer)", ", ".join(sorted(MANDAT_UMFAENGE))))
        return 2
    if not 1 <= args.minuten <= MANDAT_HOECHSTDAUER_MIN:
        print("Die Dauer liegt zwischen 1 und %d Minuten." % MANDAT_HOECHSTDAUER_MIN)
        return 2
    if not args.rolle.strip():
        print("Die Rolle darf nicht leer sein (zum Beispiel Architekt, Technische "
              "Projektleitung).")
        return 2
    ende = jetzt() + datetime.timedelta(minutes=args.minuten)
    daten = {
        "rolle": args.rolle.strip(),
        "umfang": umfang,
        "bis": ende.strftime(ZEITFORMAT),
        "erteilt": jetzt().strftime(ZEITFORMAT),
        "anlass": (args.anlass or "").strip(),
        "projekt": PROJEKTWURZEL,
    }
    with io.open(pfad, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(daten, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    pfade = ", ".join(MANDAT_UMFAENGE[u] for u in umfang)
    print("Mandat erteilt: Rolle %s, bis %s UTC (%d Minuten)." % (daten["rolle"], daten["bis"],
                                                                 args.minuten))
    print("Der KI-Client darf jetzt schreiben in: %s" % pfade)
    print("Weiter gesperrt: Kern, Laufzeitschicht, Wurzel-Anweisungsdatei, "
          "Berechtigungsdatei, Secrets.")
    print("Folge: Jede Aenderung steht im Diff und wird im Merge Request geprueft. Die "
          "Laufzeitfassung gleicht 'mandat.py beenden' ab; fehlende Regeln der "
          "Berechtigungsdatei nennt es, schreibt sie aber nicht.")
    print("Beenden: python %s/mandat.py beenden" % CORE_REL)
    return 0


def status(_args) -> int:
    bindung = modusbindung()
    if bindung:
        print("Modus %s gebunden, noch %d Minuten (bis %s UTC)%s." % (
            bindung["modus"], bindung["_rest_min"], bindung["bis"],
            ", Plan-Ablage %s" % bindung["ablage"] if bindung.get("ablage") else ""))
    pfad = mandatspfad()
    daten = lesen(pfad) if pfad else None
    if not daten:
        print("Kein Mandat. Das Overlay ist fuer den KI-Client gesperrt.")
        print("Erteilen (Mensch, eigenes Terminal): python %s/mandat.py erteilen --rolle "
              "<Rolle> --umfang overlay --minuten 60" % CORE_REL)
        return 0
    gueltig = gueltiges_mandat()
    if not gueltig:
        print("Mandat abgelaufen oder ungueltig (bis %s UTC) - es gilt nicht mehr. "
              "Neu erteilen oder mit 'mandat.py beenden' aufraeumen." % daten.get("bis"))
        return 0
    print("Mandat aktiv: Rolle %s, Umfang %s, noch %d Minuten (bis %s UTC)."
          % (gueltig["rolle"], ", ".join(gueltig["umfang"]), gueltig["_rest_min"],
             gueltig["bis"]))
    if gueltig.get("anlass"):
        print("Anlass: %s" % gueltig["anlass"])
    return 0


def modusbindung():
    """Die gueltige Modusbindung - dieselben Bedingungen wie im Schutz-Hook - oder None."""
    gd = git_verzeichnis()
    daten = lesen(os.path.join(gd, MODUS_DATEI)) if gd else None
    if not daten or daten.get("modus") not in MODUS_GEBUNDEN:
        return None
    try:
        ende = datetime.datetime.strptime(str(daten.get("bis")), ZEITFORMAT)
    except ValueError:
        return None
    rest = ende - jetzt()
    if (rest.total_seconds() <= 0
            or rest > datetime.timedelta(minutes=MANDAT_HOECHSTDAUER_MIN + 1)):
        return None
    projekt = daten.get("projekt")
    if (not isinstance(projekt, str) or os.path.normcase(os.path.realpath(projekt))
            != os.path.normcase(PROJEKTWURZEL)):
        return None
    daten["_rest_min"] = int(rest.total_seconds() // 60) + 1
    return daten


def _ablage_pruefen(roh: str):
    """Die Plan-Ablage projektrelativ mit '/' am Ende - oder None mit Grund."""
    ablage = (roh or "").replace("\\", "/").strip().strip("/")
    if not ablage or ablage == ".":
        return None, "Die Plan-Ablage fehlt (zum Beispiel --ablage docs/plaene)."
    if os.path.isabs(roh) or re.match(r"^[A-Za-z]:", ablage):
        return None, "Die Plan-Ablage ist projektrelativ anzugeben, nicht absolut."
    teile = ablage.split("/")
    if ".." in teile or teile[0] == "." or teile[0].lower() == ".koolie":
        return None, ("Die Plan-Ablage liegt im Projekt und ausserhalb von .koolie/ - "
                      "Kern und Overlay sind kein Ort fuer Plaene.")
    return ablage + "/", None


def modus(args) -> int:
    gd = git_verzeichnis()
    pfad = os.path.join(gd, MODUS_DATEI) if gd else None
    wahl = args.modus.strip()
    if wahl.lower() == "aus":
        if pfad and os.path.exists(pfad):
            os.remove(pfad)
            print("Modusbindung aufgehoben. Die Modusgrenze gilt wieder nur normativ.")
        else:
            print("Es bestand keine Modusbindung.")
        return 0
    wahl = wahl.upper()
    if wahl not in MODUS_GEBUNDEN:
        print("Binden lassen sich %s (oder 'aus'). M3 bis M5 brauchen Pfadlisten aus dem "
              "Overlay und gelten weiter normativ; M6 ist das Mandat ('erteilen')."
              % " und ".join(MODUS_GEBUNDEN))
        return 2
    if not pfad:
        print("Gesperrt: Modusbindung ohne Git-Repositorium.\n"
              "Warum: Die Bindung liegt wie das Mandat im Git-Verzeichnis.\n"
              "Loesung: Das Projekt als Git-Repositorium fuehren (git init).\n"
              "Folge: Bis dahin gilt die Modusgrenze nur normativ.")
        return 1
    if not 1 <= args.minuten <= MANDAT_HOECHSTDAUER_MIN:
        print("Die Dauer liegt zwischen 1 und %d Minuten." % MANDAT_HOECHSTDAUER_MIN)
        return 2
    ablage = None
    if wahl == "M2":
        ablage, grund = _ablage_pruefen(args.ablage)
        if grund:
            print(grund)
            return 2
    elif args.ablage:
        print("Hinweis: M1 schreibt nichts - die Plan-Ablage wird nicht verwendet.")
    ende = jetzt() + datetime.timedelta(minutes=args.minuten)
    daten = {"modus": wahl, "bis": ende.strftime(ZEITFORMAT),
             "erteilt": jetzt().strftime(ZEITFORMAT), "projekt": PROJEKTWURZEL}
    if ablage:
        daten["ablage"] = ablage
    with io.open(pfad, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(daten, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("Modus %s gebunden bis %s UTC (%d Minuten)." % (wahl, daten["bis"], args.minuten))
    if wahl == "M1":
        print("Der KI-Client kann mit keinem Schreibwerkzeug schreiben.")
    else:
        print("Der KI-Client schreibt nur unter %s." % ablage)
    print("Grenze: Ein Shell-Befehl, der schreibt, entgeht der Bindung (Rueckfrage und "
          "Regelschicht tragen dort).")
    print("Aufheben: python %s/mandat.py modus aus" % CORE_REL)
    return 0


def beenden(args) -> int:
    pfad = mandatspfad()
    if pfad and os.path.exists(pfad):
        os.remove(pfad)
        print("Mandat beendet. Das Overlay ist fuer den KI-Client wieder gesperrt.")
    else:
        print("Es bestand kein Mandat.")
    if getattr(args, "ohne_abgleich", False):
        return 0
    return abgleichen()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Mandat fuer Modus M6 (Koolie)")
    sub = ap.add_subparsers(dest="befehl")
    e = sub.add_parser("erteilen", help="Mandat erteilen")
    e.add_argument("--rolle", required=True, help="Ihre Rolle, z. B. Architekt")
    e.add_argument("--umfang", default="overlay",
                   help="overlay (ganzes Overlay) oder dokumente (nur documents/)")
    e.add_argument("--minuten", type=int, default=60,
                   help="Dauer, hoechstens %d" % MANDAT_HOECHSTDAUER_MIN)
    e.add_argument("--anlass", default="", help="kurzer Anlass, landet im Nachweis")
    sub.add_parser("status", help="Mandat anzeigen")
    b = sub.add_parser("beenden", help="Mandat beenden und das Overlay abgleichen")
    b.add_argument("--ohne-abgleich", action="store_true",
                   help="nur beenden, die Laufzeitfassung nicht abgleichen")
    sub.add_parser("abgleichen",
                   help="Overlay-Werte in Laufzeitfassung und Manifest uebernehmen")
    m = sub.add_parser("modus", help="M1 oder M2 an den Schutz-Hook binden, 'aus' hebt auf")
    m.add_argument("modus", help="M1, M2 oder aus")
    m.add_argument("--ablage", default="", help="M2: projektrelative Plan-Ablage")
    m.add_argument("--minuten", type=int, default=120,
                   help="Dauer, hoechstens %d" % MANDAT_HOECHSTDAUER_MIN)
    args = ap.parse_args(argv)
    if args.befehl == "modus":
        return modus(args)
    if args.befehl == "erteilen":
        return erteilen(args)
    if args.befehl == "beenden":
        return beenden(args)
    if args.befehl == "abgleichen":
        return abgleichen(args)
    return status(args)


if __name__ == "__main__":
    for strom in (sys.stdout, sys.stderr):
        try:
            strom.reconfigure(errors="backslashreplace")
        except (AttributeError, ValueError):
            pass
    sys.exit(main())
