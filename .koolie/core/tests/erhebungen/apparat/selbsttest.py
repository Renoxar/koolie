# -*- coding: utf-8 -*-
"""Der Apparat gegen einen Attrappen-Client - ohne Modell, ohne Kontingent (K-174, Frage b).

Bis 1.18.2 hatte kein Messskript einen Test (D-436). Jeder Fall hier hat einen Anlass,
der schon einmal Geld oder einen Befund gekostet hat; der Fall misst, dass der Apparat
ihn heute abfaengt. Ein Fall, der nicht faellt, wenn sein Gegenstand fehlt, waere keiner:
Die Gegenfaelle (T4, T5, T6) praeparieren genau den Fehler und verlangen die Meldung.

Aufruf: python messen.py selbsttest   (Exit 0 = alle Faelle tragen)
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import tempfile

from . import baum as baum_mod
from . import belege as belege_mod
from . import kontingent, laeufer, stand, vorpruefung
from .clients import AdapterUnerhoben, Unerhoben, adapter
from .reihe import Reihe, Reihenfehler, pruefen as reihe_pruefen

FAELLE = []


def fall(nummer, was):
    def deko(f):
        FAELLE.append((nummer, was, f))
        return f
    return deko


def _basis(wurzel: str) -> str:
    b = os.path.join(wurzel, "basis")
    os.makedirs(b)
    baum_mod.git(b, "init", "-q", "-b", "main")
    baum_mod.git(b, "config", "core.autocrlf", "false")
    io.open(os.path.join(b, "README.md"), "w", encoding="utf-8", newline="\n").write("Basis\n")
    io.open(os.path.join(b, ".gitignore"), "w", encoding="utf-8", newline="\n").write(".env\n")
    io.open(os.path.join(b, ".env"), "w", encoding="utf-8", newline="\n").write("SONDE=synthetisch\n")
    baum_mod.git(b, "add", "-A")
    baum_mod.git(b, *baum_mod.AUTOR, "commit", "-q", "-m", "Basis")
    return b


def _reihe(wurzel: str, basis: str, laeufe: list, usd=5.0, laeufe_max=10, reserve=0.0) -> Reihe:
    ablage = os.path.join(wurzel, "ablage")
    os.makedirs(ablage, exist_ok=True)
    d = {"name": "selbsttest", "client": "attrappe", "wurzel": os.path.join(wurzel, "baeume"),
         "kontingent": {"laeufe": laeufe_max, "usd": usd, "reserve_usd": reserve},
         "baum": {"modus": "fest", "basis": basis}, "laeufe": laeufe}
    r = Reihe(d, ablage)
    fehler = reihe_pruefen(r, ("attrappe",))
    assert not fehler, fehler
    return r


def _antworten(wurzel: str, antworten: dict) -> None:
    pfad = os.path.join(wurzel, "attrappe.json")
    io.open(pfad, "w", encoding="utf-8").write(json.dumps(antworten))
    os.environ["LW_ATTRAPPE"] = pfad


def _still(*_a, **_k):
    pass


@fall("T1", "eine kaputte Reihe meldet ALLE Schemafehler vor dem ersten Lauf")
def t1(w):
    r = Reihe({"name": "x", "client": "attrappe", "kontingent": {},
               "baum": {"modus": "fest", "basis": "b"}, "wurzel": "w",
               "laeufe": [{"kennung": "a", "prompt": "p", "erwartung": "e", "folgeturns": [" "]},
                          {"kennung": "a", "prompt": "p", "erwartung": "e"}]}, w)
    f = " | ".join(reihe_pruefen(r, ("attrappe",)))
    for teil in ("kontingent", "doppelt", "Folgeturn ist leer"):
        assert teil in f, f"'{teil}' nicht gemeldet: {f}"


@fall("T2", "fester Baum: ein Lauf schreibt, aendert eine ignorierte Datei und legt eine an - "
            "der naechste startet trotzdem auf dem Sollstand")
def t2(w):
    b = _basis(w)
    _antworten(w, {"schreib": {"schreibe": {"neu.txt": "x", ".env": "VERAENDERT", "README.md": "y",
                                            "tief/ordner/z.txt": "z"}},
                   "lies": {"antwort": "gelesen"}})
    r = _reihe(w, b, [{"kennung": "a1", "prompt": "schreib", "erwartung": "e"},
                      {"kennung": "a2", "prompt": "lies", "erwartung": "e"},
                      {"kennung": "a3", "prompt": "lies", "erwartung": "e"}])
    laeufer.aufbau(r)
    assert laeufer.fahren(r, ausgabe=_still) == 3
    n, usd = kontingent.summe(r.belege)
    assert (n, round(usd, 2)) == (3, 0.3), (n, usd)
    pfad = r.baumpfad(r.laeufe[0])
    assert io.open(os.path.join(pfad, ".env"), encoding="utf-8").read() == "SONDE=synthetisch\n"
    assert not os.path.exists(os.path.join(pfad, "tief"))


@fall("T3", "Arbeitsbranch (K-172): der Baum steht auf arbeit/..., der naechste Lauf wieder auf main")
def t3(w):
    b = _basis(w)
    _antworten(w, {"": {}})
    r = _reihe(w, b, [{"kennung": "b1", "prompt": "p", "erwartung": "e", "branch": "arbeit/b1"},
                      {"kennung": "b2", "prompt": "p", "erwartung": "e"}])
    laeufer.aufbau(r)
    laeufer.fahren(r, ["b1"], ausgabe=_still)
    pfad = r.baumpfad(r.laeufe[0])
    assert baum_mod.git(pfad, "symbolic-ref", "--short", "HEAD") == "arbeit/b1"
    laeufer.fahren(r, ["b2"], ausgabe=_still)
    assert baum_mod.git(pfad, "symbolic-ref", "--short", "HEAD") == "main"


@fall("T4", "Gegenfall HEAD: steht der Baum auf dem falschen Branch, meldet die Vorpruefung es (D-218)")
def t4(w):
    b = _basis(w)
    _antworten(w, {"": {}})
    r = _reihe(w, b, [{"kennung": "c1", "prompt": "p", "erwartung": "e", "branch": "arbeit/c1"}])
    laeufer.aufbau(r)
    pfad, soll = laeufer._herrichten(r, r.laeufe[0])
    baum_mod.git(pfad, "checkout", "-q", "main")
    befunde = vorpruefung.pruefen(r, r.laeufe[0], adapter("attrappe"), soll, pfad)
    assert any(x.startswith("head: Branch") for x in befunde), befunde


@fall("T5", "Gegenfall Zustand: ein Rest im Baum aendert den Baum-Hash, und die Vorpruefung meldet ihn")
def t5(w):
    b = _basis(w)
    _antworten(w, {"": {}})
    r = _reihe(w, b, [{"kennung": "d1", "prompt": "p", "erwartung": "e"}])
    laeufer.aufbau(r)
    pfad, soll = laeufer._herrichten(r, r.laeufe[0])
    assert not vorpruefung.pruefen(r, r.laeufe[0], adapter("attrappe"), soll, pfad)
    io.open(os.path.join(pfad, "rest.txt"), "w").write("vom vorigen Lauf")
    befunde = vorpruefung.pruefen(r, r.laeufe[0], adapter("attrappe"), soll, pfad)
    assert any(x.startswith("zustand:") for x in befunde), befunde


@fall("T6", "Gegenfall Deckel: der Lauf, der das Kontingent reissen koennte, faehrt nicht")
def t6(w):
    b = _basis(w)
    _antworten(w, {"": {"usd": 0.1}})
    r = _reihe(w, b, [{"kennung": "e%d" % i, "prompt": "p", "erwartung": "e"} for i in range(4)],
               usd=0.25, reserve=0.1)  # Reserve = was ein Lauf hoechstens kostet
    laeufer.aufbau(r)
    try:
        laeufer.fahren(r, ausgabe=_still)
        raise AssertionError("kein Abbruch")
    except SystemExit as e:
        assert "Kontingent" in str(e), e
    assert kontingent.summe(r.belege)[0] == 2


@fall("T7", "ein Lauf wird nicht doppelt gebucht, und eine gefahrene Kennung faehrt nicht noch einmal")
def t7(w):
    b = _basis(w)
    _antworten(w, {"": {}})
    r = _reihe(w, b, [{"kennung": "f1", "prompt": "p", "erwartung": "e"}])
    laeufer.aufbau(r)
    laeufer.fahren(r, ausgabe=_still)
    assert laeufer.fahren(r, ausgabe=_still) == 0
    try:
        kontingent.eintragen(r.belege, "f1", {"usd": 1})
        raise AssertionError("doppelt gebucht")
    except RuntimeError:
        pass


@fall("T8", "Belege im Repositorium sind ein Abbruch (D-222)")
def t8(w):
    try:
        belege_mod.ablage_pruefen(os.path.join(belege_mod.KERN, "tests", "erhebungen", "belege"))
        raise AssertionError("kein Abbruch")
    except RuntimeError:
        pass


@fall("T9", "die Standmarke ist gegen Zeilenenden fest und meldet einen fehlenden Gegenstand")
def t9(w):
    kern = os.path.join(w, "kern")
    os.makedirs(kern)
    io.open(os.path.join(kern, "a.md"), "wb").write(b"eins\r\nzwei\r\n")
    m1 = stand.marke(["a.md"], kern)
    io.open(os.path.join(kern, "a.md"), "wb").write(b"eins\nzwei\n")
    assert stand.marke(["a.md"], kern) == m1
    io.open(os.path.join(kern, "a.md"), "wb").write(b"eins\ndrei\n")
    assert stand.marke(["a.md"], kern) != m1
    try:
        stand.marke(["fehlt.md"], kern)
        raise AssertionError("kein Abbruch")
    except RuntimeError:
        pass


@fall("T10", "ein unerhobener Client sagt es - als Befund der Vorpruefung, nie als Erfolg (D-276)")
def t10(w):
    b = _basis(w)
    r = _reihe(w, b, [{"kennung": "g1", "prompt": "p", "erwartung": "e"}])
    laeufer.aufbau(r)
    pfad, soll = laeufer._herrichten(r, r.laeufe[0])
    befunde = vorpruefung.pruefen(r, r.laeufe[0], AdapterUnerhoben("kiro"), soll, pfad)
    assert any("hook: nicht pruefbar" in x for x in befunde), befunde
    assert any("vertrauen: nicht pruefbar" in x for x in befunde), befunde
    try:
        AdapterUnerhoben("kiro").lauf("p", pfad, None, "default")
        raise AssertionError("gefahren")
    except Unerhoben:
        pass


@fall("T11", "Referenzgruppe (1.21.0): Einstellungen im Messbaum, ein Startverzeichnis ausserhalb "
             "und Remote-Hooks ohne Remote sind Schemafehler")
def t11(w):
    b = _basis(w)
    innen = os.path.join(w, "baeume", "settings.json")
    os.makedirs(os.path.dirname(innen))
    io.open(innen, "w", encoding="utf-8").write("{}")
    r = Reihe({"name": "x", "client": "attrappe", "wurzel": os.path.join(w, "baeume"),
               "kontingent": {"laeufe": 1, "usd": 1}, "einstellungen": innen,
               "baum": {"modus": "fest", "basis": b, "remote_hooks": w},
               "laeufe": [{"kennung": "a", "prompt": "p", "erwartung": "e",
                           "unterverzeichnis": "../nachbar"}]}, w)
    f = " | ".join(reihe_pruefen(r, ("attrappe",)))
    for teil in ("unter der wurzel", "muss im Baum liegen", "remote_hooks ohne remote"):
        assert teil in f, f"'{teil}' nicht gemeldet: {f}"


@fall("T12", "Referenzgruppe (1.21.0): der Lauf startet im Unterverzeichnis mit der Einstellungsdatei, "
             "die Verbindung uebersteht das Zuruecksetzen und zaehlt nicht im Baum-Hash")
def t12(w):
    b = _basis(w)
    os.makedirs(os.path.join(b, "frontend"))
    io.open(os.path.join(b, "frontend", "a.ts"), "w", encoding="utf-8", newline="\n").write("x\n")
    baum_mod.git(b, "add", "-A")
    baum_mod.git(b, *baum_mod.AUTOR, "commit", "-q", "-m", "frontend")
    quelle = os.path.join(w, "geteilt")
    os.makedirs(quelle)
    io.open(os.path.join(quelle, "paket.js"), "w").write("geteilt")
    aussen = os.path.join(w, "referenz-settings.json")
    io.open(aussen, "w", encoding="utf-8").write("{}")
    _antworten(w, {"": {}})
    r = Reihe({"name": "selbsttest", "client": "attrappe", "wurzel": os.path.join(w, "baeume"),
               "kontingent": {"laeufe": 5, "usd": 5}, "einstellungen": aussen,
               "baum": {"modus": "fest", "basis": b,
                        "verbindungen": {"frontend/node_modules": quelle}},
               "laeufe": [{"kennung": "h1", "prompt": "p", "erwartung": "e",
                           "unterverzeichnis": "frontend", "gruppe": "referenz"},
                          {"kennung": "h2", "prompt": "p", "erwartung": "e"}]},
              os.path.join(w, "ablage"))
    assert not reihe_pruefen(r, ("attrappe",)), reihe_pruefen(r, ("attrappe",))
    laeufer.aufbau(r)
    assert laeufer.fahren(r, ausgabe=_still) == 2
    pfad = r.baumpfad(r.laeufe[0])
    assert io.open(os.path.join(pfad, "frontend", "node_modules", "paket.js")).read() == "geteilt"
    assert baum_mod.baumhash(pfad) == baum_mod.baumhash(b)
    e = json.loads(io.open(os.path.join(r.belege, "h1-ergebnis.json"), encoding="utf-8").read())
    assert os.path.normcase(e["start"]) == os.path.normcase(os.path.join(pfad, "frontend")), e
    assert e["einstellungen"] == aussen, e


def main() -> int:
    schlecht = 0
    for nummer, was, f in FAELLE:
        with tempfile.TemporaryDirectory(prefix="lw-selbsttest-") as w:
            try:
                f(w)
                print(f"trägt   {nummer}  {was}")
            except Exception as e:  # jeder Fehler ist ein Befund dieses Falls
                schlecht += 1
                print(f"FÄLLT   {nummer}  {was}\n        {type(e).__name__}: {e}")
            finally:
                subprocess.run(["git", "gc", "--quiet"], cwd=w, capture_output=True)
                for wurzel, _, files in os.walk(w):
                    for fn in files:
                        try:
                            os.chmod(os.path.join(wurzel, fn), 0o666)
                        except OSError:
                            pass
    print(f"\n{len(FAELLE) - schlecht} von {len(FAELLE)} Fällen tragen")
    return 1 if schlecht else 0
