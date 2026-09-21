# -*- coding: utf-8 -*-
"""Sagt den Skripten dieser Ablage, WOHIN ihre Belege und Prompts gehoeren.

🔴 DER ANLASS IST D-222 SELBST. Bis zum Meßtag von Buendel 4 lag der Apparat in
`devpacks/leitwerk-erhebungen-2026-09-19-b4/skripte/`, und fuenf Skripte legten
ihre Belege schlicht *neben sich*:

    BELEGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "belege")

Das war richtig, solange das Skript daneben lag. **Mit 0.79.0 ist der Apparat ins
Repositorium gewandert - und derselbe Ausdruck zeigt seither HINEIN.** Ein
Nachlauf haette 44 Belegdateien samt Sitzungsmitschriften mit Werkzeugeingaben
unter `<CORE_DIR>/tests/erhebungen/belege/` angelegt; `lauf.py` erzeugt das
Verzeichnis selbst. Genau das hat D-222 verworfen:

    "Verworfen: auch die Belege zu versionieren (203 Dateien, darunter fuenfzig
    Sitzungstranskripte mit Werkzeugeingaben; sie sind AUFZEICHNUNG, nicht
    Anweisung - dieselbe Trennlinie, die D-141 fuer den Kontrollzuschnitt zieht)."

  Wer einen Apparat umzieht, zieht seine relativen Pfade mit um - oder er
  verschiebt ihr Ziel, ohne es zu merken.

DIE ABLAGE WIRD GESAGT, NICHT ABGELEITET - dieselbe Lehre wie `--ziel` beim
Baumbau (D-218). Ein Standardwert im Quelltext waere eine gepflegte Zahl: Er
stimmt fuer die Erhebung, fuer die er geschrieben wurde, und fuer keine danach.

    set LW_ERHEBUNG=C:\\Users\\...\\devpacks\\leitwerk-erhebungen-2026-09-20-b4n   # SYNTHETISCH

Fehlt die Angabe, bricht jedes Skript ab, das eine Belegablage braucht. Ein
Abbruch ist billiger als ein Beleg am falschen Ort.
"""
import io
import os
import re
import sys

UMGEBUNG = "LW_ERHEBUNG"

# Die Kennung einer Blattzelle, ausgeschrieben und zusammengezogen. Sie steht
# seit 0.82.0 an EINER Stelle; bis dahin uebersetzte `baeume-b4.py` sie mit
# `kern[:2].upper()` und `dossier-b4.py` gar nicht zurueck.
_KENNUNG_RE = re.compile(r"^([A-Z]{2,3}-[0-9]{3})-[PN][0-9]{2}$")
_KURZ_RE = re.compile(r"^([a-z]{2,3})([0-9]{3})([pn][0-9]{2})$")

# Die Wurzel des Repositoriums: dieses Modul liegt in
# <wurzel>/leitwerk-core/tests/erhebungen/.
_HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(_HIER)))


def _innerhalb(pfad, wurzel):
    """True, wenn `pfad` unter `wurzel` liegt - ohne Praefixvergleich auf Text.

    Ein Praefixvergleich auf der Zeichenkette nimmt `...\\leitwerk-erhebungen`
    faelschlich als Kind von `...\\leitwerk`. Das ist genau die Bauform von
    D-219, eine Ebene tiefer: ein Praefix, das mehr erfasst als sein Gegenstand.
    """
    try:
        gemeinsam = os.path.commonpath([os.path.abspath(pfad),
                                        os.path.abspath(wurzel)])
    except ValueError:          # verschiedene Laufwerke
        return False
    return gemeinsam == os.path.abspath(wurzel)


def erhebung():
    """Der Wurzelpfad der Erhebungsablage - mit zwei Waechtern."""
    wert = os.environ.get(UMGEBUNG, "").strip().strip('"')
    if not wert:
        raise SystemExit(
            "ABBRUCH: %s ist nicht gesetzt.\n"
            "Die Belege einer Erhebung sind AUFZEICHNUNG und liegen ausserhalb\n"
            "des Repositoriums (D-222). Seit der Apparat im Kern liegt, gibt es\n"
            "keinen ableitbaren Ort mehr - er wird gesagt:\n"
            "    set %s=<Pfad der Erhebungsablage>" % (UMGEBUNG, UMGEBUNG))
    wert = os.path.abspath(wert)
    if _innerhalb(wert, WURZEL):
        raise SystemExit(
            "ABBRUCH: %s zeigt mit %r INS Repositorium (%s).\n"
            "Belege und Prompts einer Erhebung gehoeren daneben, nicht hinein\n"
            "(D-222)." % (UMGEBUNG, wert, WURZEL))
    return wert


def kernversion():
    """Die Version, die das Uebungsrepositorium tragen MUSS.

    🔴 DREI WAECHTER DERSELBEN VORBEDINGUNG, DREI SOLLWERTE, KEINER STIMMTE
    (2026-09-20, Vorbedingungsdurchgang des Nachlaufs). `umgebungen-bauen-b4.py`
    und `baeume-b4.py` fuehrten `--erwarte 0.78.0`, `historie-bauen-b4.py`
    fuehrte `0.77.0` - waehrend das Uebungsrepositorium auf `0.78.2` stand und
    der Kern auf `0.79.1`. Ein Sollwert im Quelltext ist eine gepflegte Zahl,
    und eine Zahl, die gepflegt werden muss, wird nicht gepflegt (D-153).

    Er wird deshalb ABGELEITET: Sollstand ist die Version DIESES Kerns. Damit
    beantwortet der Waechter zugleich die erste Frage jedes
    Vorbedingungsdurchgangs - hat ein Release den Gegenstand der Messung
    angefasst? -, statt sie einem gepflegten Wert zu ueberlassen.
    `--erwarte` bleibt als Uebersteuerung erhalten.
    """
    p = os.path.join(WURZEL, "leitwerk-core", "VERSION")
    with open(p, encoding="utf-8") as f:
        return f.read().strip()


UMGEBUNG_UEBUNG = "LW_UEBUNG"


def uebungsrepositorium():
    """Der Pfad des Uebungsrepositoriums - GESAGT, nicht im Quelltext.

    🔴 DER ANLASS IST GEMESSEN (2026-09-21, D-231). Acht Werkzeuge dieses Kerns
    trugen einen Arbeitsplatzpfad im Quelltext, und der Pfad enthaelt den
    Kontonamen einer natuerlichen Person:

        UEB = r"C:\\Users\\<konto>\\Documents\\devpacks\\test-devin-framework"   # SYNTHETISCH

    Solange der Apparat NEBEN dem Repositorium lag, stand das in einer
    unversionierten Ablage. **Mit D-222 ist er hineingewandert und hat den Pfad
    mitgebracht** - in genau das Repositorium, dessen Overlay-Manifest *"keine
    Secrets, keine Personen, keine internen Adressen"* verlangt und fuer das
    `0.78.1` eigens `UEBERGABE.local.md` eingefuehrt hat. **Keine der siebzig
    Pruefungen sah es**: Pruefung 6 kennt Secret-Muster, E-Mail-Adressen,
    IP-Adressen und Hostnamen - keinen Benutzerprofilpfad.

      Wer einen Apparat umzieht, zieht seine Arbeitsplatzpfade mit um - und
      veroeffentlicht sie, ohne es zu entscheiden.

    Dieselbe Loesung wie bei D-224: Der Ort wird gesagt. Ein Standardwert waere
    wieder ein Arbeitsplatz im Quelltext.
    """
    wert = os.environ.get(UMGEBUNG_UEBUNG, "").strip().strip('"')
    if not wert:
        raise SystemExit(
            "ABBRUCH: %s ist nicht gesetzt.\n"
            "Das Uebungsrepositorium liegt NEBEN diesem Repositorium, und sein\n"
            "Pfad gehoert keinem Quelltext - er wird gesagt (D-231):\n"
            "    set %s=<Pfad des Uebungsrepositoriums>"
            % (UMGEBUNG_UEBUNG, UMGEBUNG_UEBUNG))
    wert = os.path.abspath(wert)
    if not os.path.isdir(wert):
        raise SystemExit(
            "ABBRUCH: %s zeigt mit %r auf kein Verzeichnis." % (UMGEBUNG_UEBUNG, wert))
    return wert


def belege(anlegen=True):
    """`<Erhebungsablage>/belege` - der Ort aller Belegquellen eines Laufs."""
    p = os.path.join(erhebung(), "belege")
    if anlegen:
        os.makedirs(p, exist_ok=True)
    return p


def prompts(anlegen=True):
    """`<Erhebungsablage>/prompts` - der Ort der Promptdateien."""
    p = os.path.join(erhebung(), "prompts")
    if anlegen:
        os.makedirs(p, exist_ok=True)
    return p


def sollmenge(promptordner, baumordner):
    """Die Kennungen, die DIESE Erhebung schuldet - und die, die sie nicht schuldet.

    🔴 DER ANLASS IST GEMESSEN (2026-09-21, D-230). Der Nachlauf von Buendel 4 misst
    vierzehn Zellen. Sein Promptverzeichnis traegt die **fuenfzig** Prompts des
    Messtags, weil `prompts-schreiben-b4.py` sie alle schreibt und keine Zelle
    kennt. `stand-b4.py` leitete seine Sollmenge daraus ab und meldete am halb
    gefahrenen Nachlauf **35 fehlende Laeufe und rund 37 USD** - faellig waren
    fuenfzehn und rund achtzehn. Und `reihe-b4.py` ohne Argumente - der Befehl, den
    `stand-b4.py` selbst als naechsten nennt - brach am ersten Baum ab, den es in
    dieser Erhebung nie gab, und fuhr **keinen einzigen** Lauf.

    Die Sollmenge kommt deshalb aus den **Messbaeumen**: `baeume-b4.py` legt genau
    die Baeume an, die der Zuschnitt dieser Erhebung nennt. Ein Prompt ohne Baum ist
    eine Zelle einer anderen Erhebung - derselbe Grund, aus dem `LW_ERHEBUNG` gesagt
    wird (D-224) und `--ziel` beim Baumbau (D-218): **Ein Ort, der aus der Umgebung
    erschlossen wird, gehoert dem, der ihn zuletzt gefuellt hat.**

      Ein Verzeichnis ist kein Zuschnitt. Es ist der Zuschnitt von gestern.

    Gibt zwei sortierte Listen zurueck: die Kennungen mit Baum (ein `-t2.txt` ist
    kein eigener Eintrag - er ist der zweite Turn seiner Zelle) und die Prompts ohne
    Baum, die die Aufrufer NENNEN muessen, statt sie stillschweigend zu uebergehen.
    """
    einfach, zwei = set(), set()
    for x in sorted(os.listdir(promptordner)):
        if not x.endswith(".txt"):
            continue
        n = x[:-4]
        # 🔴 Eine NACHMESSUNG (`n<kennung>`) gehoert nicht zur Sollmenge. Sie faehrt
        # einen weiteren Turn im Baum ihrer Zelle und hat keinen eigenen Baum; wer
        # sie mitzaehlt, meldet einen Fehlbestand, den es nicht gibt. Praezedenz:
        # `nsk004p01` und `nsk009p01` aus Buendel 2.
        if n.startswith("n"):
            continue
        if n.endswith("-t2"):
            zwei.add(n[:-3])
        else:
            einfach.add(n)
    vorhanden = set()
    if os.path.isdir(baumordner):
        vorhanden = {x for x in os.listdir(baumordner)
                     if os.path.isdir(os.path.join(baumordner, x))}
    mit, ohne = [], []
    for k in sorted(einfach):
        (mit if k in vorhanden else ohne).append(k)
    return mit, zwei, ohne


def blaetter(wurzel=None):
    """Je Kennungspraefix eines Testblatts (`SK-012`, `RE-001`) sein Skill und sein Ort.

    🔴 ABGELEITET, NICHT GEPFLEGT - und der Anlass ist derselbe zum dritten Mal.
    `umgebungen-bauen-b4.py` fuehrte die drei Skills von Buendel 4 BEIM NAMEN, und
    alle drei lagen auch im Baum von Buendel 5: Der Waechter haette geschwiegen,
    waehrend der gemessene Skill fehlte (D-237). `dossier-b4.py` fuehrte dieselbe
    Zuordnung ein zweites Mal als Handliste.

      Marken, Wurzeln und Namenslisten gehoeren abgeleitet, nicht gepflegt.

    Gesucht wird jede `TESTS.md` unter `framework/skills/` und unter
    `framework/<art>/<pack>/skills/`; der Praefix kommt aus der ersten Spalte ihrer
    Tabellenzeilen, also aus dem Blatt selbst und nicht aus seinem Dateinamen.
    Rueckgabe: Praefix -> dict(skill, blatt, pack, art).
    """
    wurzel = wurzel or WURZEL
    rahmen = os.path.join(wurzel, "leitwerk-core", "framework")
    orte = [(os.path.join(rahmen, "skills"), None, None)]
    for art in ("role-packs", "tech-packs"):
        basis = os.path.join(rahmen, art)
        if not os.path.isdir(basis):
            continue
        for pack in sorted(os.listdir(basis)):
            unter = os.path.join(basis, pack, "skills")
            if os.path.isdir(unter):
                orte.append((unter, pack, art))
    aus = {}
    for ablage, pack, art in orte:
        if not os.path.isdir(ablage):
            continue
        for skill in sorted(os.listdir(ablage)):
            blatt = os.path.join(ablage, skill, "TESTS.md")
            if not os.path.isfile(blatt):
                continue
            with io.open(blatt, encoding="utf-8", newline="") as fh:
                text = fh.read()
            for zeile in text.replace("\r\n", "\n").split("\n"):
                if not zeile.startswith("| "):
                    continue
                kennung = zeile.split("|")[1].strip()
                treffer = _KENNUNG_RE.match(kennung)
                if not treffer:
                    continue
                praefix = treffer.group(1)
                fruehere = aus.get(praefix)
                if fruehere and fruehere["skill"] != skill:
                    raise SystemExit(
                        "ABBRUCH: der Kennungspraefix %s steht in zwei Blaettern "
                        "(%s und %s) - eine Zelle laesst sich dann keinem Skill "
                        "zuordnen" % (praefix, fruehere["skill"], skill))
                aus[praefix] = {
                    "skill": skill,
                    "blatt": os.path.relpath(blatt, wurzel).replace(os.sep, "/"),
                    "pack": pack,
                    "art": art,
                }
    if not aus:
        raise SystemExit("ABBRUCH: kein Testblatt unter framework/ gefunden - die "
                         "Ableitung haette ihren Gegenstand verloren und bliebe "
                         "leise leer (D-23)")
    return aus


def zellkennung(kurz):
    """`sk012p01` -> `SK-012-P01`, `re001n09` -> `RE-001-N09`.

    Der Apparat fuehrt die Kennung einer Zelle zusammengezogen und klein; das
    Testblatt fuehrt sie ausgeschrieben. Die Ruecknahme stand bis 0.81.0 an zwei
    Stellen im Quelltext.
    """
    treffer = _KURZ_RE.match(kurz)
    if not treffer:
        raise SystemExit("ABBRUCH: %r ist keine Zellkennung des Apparats" % kurz)
    a, b, c = treffer.groups()
    return "%s-%s-%s" % (a.upper(), b, c.upper())


def skillmenge(zellen, wurzel=None):
    """Welche Skills eine Zellmenge misst - und welche Packs dafuer aktiv sein muessen.

    Rueckgabe: (skills, packs). `skills` ist die sortierte Namensliste, `packs` die
    sortierte Liste der (Art, Packname) - leer, wenn alle gemessenen Skills im Kern
    liegen. Genau diese beiden Listen ersetzen die Handliste des Waechters (D-237).
    """
    karte = blaetter(wurzel)
    skills, packs, unbekannt = set(), set(), []
    for kurz in zellen:
        voll = zellkennung(kurz) if "-" not in kurz else kurz
        praefix = "-".join(voll.split("-")[:2])
        eintrag = karte.get(praefix)
        if not eintrag:
            unbekannt.append(voll)
            continue
        skills.add(eintrag["skill"])
        if eintrag["pack"]:
            packs.add((eintrag["art"], eintrag["pack"]))
    if unbekannt:
        raise SystemExit("ABBRUCH: zu %d Zelle(n) traegt kein Testblatt des Frameworks "
                         "den Kennungspraefix: %s" % (len(unbekannt),
                                                      ", ".join(sorted(unbekannt))))
    return sorted(skills), sorted(packs)


def laeufe(zellen, zwei):
    """Die Laufkennungen einer Zellmenge - eine Zelle mit zweitem Turn hat ZWEI."""
    aus = []
    for k in zellen:
        if k in zwei:
            aus += [k + "t1", k]
        else:
            aus.append(k)
    return aus


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("Kernversion:    ", kernversion())
    print("Erhebungsablage:", erhebung())
    print("Belege:         ", belege(anlegen=False))
    print("Prompts:        ", prompts(anlegen=False))
    karte = blaetter()
    print("Testblaetter:   %d (%s)"
          % (len(karte), ", ".join("%s=%s" % (k, v["skill"])
                                   for k, v in sorted(karte.items()))))
