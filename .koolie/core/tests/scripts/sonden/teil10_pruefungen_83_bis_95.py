"""Sonden zu den Pruefungen 83 bis 95 und 4 (Zeichengrenze der Wurzel-Anweisung) und zu den
Einstiegsdokumenten der Wurzel.

Teil des Sondenskripts probe-pruefungen.py, seit 1.19.1 in Module geteilt (K-174). Die
Einheiten melden sich beim Laden dieses Moduls an; der Einstieg laedt die Module in der
Reihenfolge ihrer Nummer, und das ist die Reihenfolge der Ausgabe (D-49). Ein Modul
liest nur aus dem Apparat und aus frueheren Teilen."""
from __future__ import annotations

import json
import os
import re
import shutil

from .apparat import (
    aufraeumen, baumhash, buendel, installation, kopie, lies, melde, notiz, P,
    Praeparationsfehler, QUELLE, schreib, validator_ausgabe)


# --- Pruefung 83: die Chronik zaehlt ihr eigenes Release zu Ende (CR-2026-131) -----
#
# FUENF EINHEITEN, UND DIE ZWEITE GEGENPROBE IST DIE, DIE MAN WEGLASSEN WUERDE.
#   83a (Gegenprobe) - die berichtigte Chronik laeuft durch, und die Pruefung ist
#                      dabei nachweislich gelaufen (keine Ankermeldung).
#   83b (Gegenprobe) - 🔴 DIE, DIE DEN ZUSCHNITT TRAEGT. Die Releasetabelle ist NICHT
#                      sortiert: gemessen am 2026-09-23 stand `1.0.1` VOR `1.0.0`
#                      (D-337). Eine Spanne, die NICHT die hoechste ist, wird hinter
#                      die hoechste gestellt - die Pruefung muss GRUEN bleiben, weil
#                      sie die hoechste Obergrenze nimmt und nicht die zuletzt
#                      geschriebene. Ohne diese Gegenprobe waere die Reihenfolgefestig-
#                      keit eine Behauptung im Kopfkommentar statt eine gemessene
#                      Eigenschaft - genau die Bauform, die 0.90.0 zweimal gekostet
#                      hat (D-326, D-299).
#   83a (Sonde)      - eine Entscheidung wird ins Register gehaengt, ohne die Spanne
#                      zu heben: der gemessene Fall aus 1.1.0 wird gemeldet, und die
#                      Meldung nennt die fehlende Kennung.
#   83b (Sonde)      - die Spannenschreibweise entfernt: der verlorene Anker wird als
#                      Fehler gemeldet, statt leise zu bestehen (D-23).
#   83c (Sonde)      - eine Spanne ueber die hoechste Kennung hinaus: die Chronik
#                      nennt eine Entscheidung, die es nicht gibt.
#
# KEINE EINHEIT HAELT EINE KENNUNG WOERTLICH. Sie lesen die hoechste aus dem Register
# und rechnen daran - dieselbe Lehre wie bei Pruefung 78, 81 und 82: Eine Sonde, die
# einen Wert mitpflegen muss, faellt beim naechsten Release aus, und zwar als
# scheinbarer Befund.
M83_FEHLEND = "In der Chronik fehlen"
M83_UEBER = "das Register fuehrt hoechstens"
M83_ANKER = "keine Release-Spanne der Form"
M83_REGISTER = "keine Registerzeile '| D-NNN |' gefunden - Pruefung 83"

P83_ROADMAP = ".koolie/core/docs/ROADMAP.md"
P83_REGISTER = ".koolie/core/governance/DECISION_LOG.md"


def _83_hoechste(root: str) -> int:
    """Die hoechste vergebene D-Kennung - ausgerechnet, nicht gewusst."""
    text = lies(P(root, *P83_REGISTER.split("/")))
    return max(int(n) for n in re.findall(r"^\|\s*(?:\*\*)?D-(\d+)", text, re.M))


def _83_spanne(root: str) -> tuple:
    """(Volltext, Untergrenze, Obergrenze) der hoechsten Spanne in der ROADMAP."""
    text = lies(P(root, *P83_ROADMAP.split("/")))
    treffer = re.findall(r"\*\*D-(\d+)\*\*\s*bis\s*\*\*D-(\d+)\*\*", text)
    a, b = max(treffer, key=lambda t: int(t[1]))
    return text, int(a), int(b)


def sonden_chronikspanne() -> None:
    """Wirkungsnachweis zu Pruefung 83."""
    root = kopie()
    try:
        rpfad = P(root, *P83_ROADMAP.split("/"))
        dpfad = P(root, *P83_REGISTER.split("/"))
        rtext, unten, oben = _83_spanne(root)
        dtext = lies(dpfad)
        hoechste = _83_hoechste(root)
        woertlich = "**D-%d** bis **D-%d**" % (unten, oben)

        # --- Gegenprobe 83a: die berichtigte Chronik laeuft durch -------------------
        aus = validator_ausgabe(root)
        ok = (M83_FEHLEND not in aus and M83_UEBER not in aus
              and M83_ANKER not in aus and M83_REGISTER not in aus)
        melde("GEGENPROBE", "83a", ok,
              "Die berichtigte Chronik laeuft durch - die hoechste Release-Spanne "
              "endet bei der hoechsten vergebenen Kennung, und die Pruefung ist dabei "
              "nachweislich gelaufen")
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "83" in z or "Spanne" in z)[:400])

        # --- Gegenprobe 83b: DIE REIHENFOLGEPROBE (D-337) ---------------------------
        # Eine NIEDRIGERE Spanne wird HINTER die hoechste gestellt. Die Pruefung nimmt
        # die hoechste Obergrenze, nicht die zuletzt geschriebene - genau deshalb ist
        # sie gegen eine unsortierte Releasetabelle fest.
        nachzuegler = "\n| **PROBE** | **D-%d** bis **D-%d** | Probe 83b |\n" % (
            unten, max(unten, oben - 1))
        schreib(rpfad, rtext + nachzuegler)
        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "83b", M83_FEHLEND not in aus and M83_UEBER not in aus,
              "Eine niedrigere Spanne HINTER der hoechsten laeuft durch - die Pruefung "
              "nimmt die hoechste Obergrenze, nicht die zuletzt geschriebene. Gemessen "
              "stand `1.0.1` vor `1.0.0` (D-337)")
        if M83_FEHLEND in aus or M83_UEBER in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "ROADMAP" in z)[:400])
        schreib(rpfad, rtext)

        # --- Sonde 83a: eine Entscheidung ohne Hebung der Spanne --------------------
        vorher = baumhash(root)
        neue = hoechste + 1
        zeile = ("| D-%d | **Probe 83a.** | Probe | Probe | Probe | 2026-01-01 |"
                 % neue)
        anker = "| D-%d |" % hoechste
        if anker not in dtext:
            raise Praeparationsfehler(
                "Sonde 83a: keine Registerzeile `%s` - die Sonde hat ihren "
                "Gegenstand verloren" % anker)
        stelle = dtext.index("\n", dtext.index(anker))
        schreib(dpfad, dtext[:stelle] + "\n" + zeile + dtext[stelle:])
        if baumhash(root) == vorher:
            raise Praeparationsfehler("Sonde 83a hat nichts geschrieben")
        aus = validator_ausgabe(root)
        ok = M83_FEHLEND in aus and ("D-%d" % neue) in aus
        melde("SONDE", "83a", ok,
              "Eine Entscheidung, die ins Register faellt, ohne dass die Spanne "
              "nachgezogen wird, wird gemeldet - und die Meldung nennt die fehlende "
              "Kennung. Der gemessene Fall aus 1.1.0")
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
        schreib(dpfad, dtext)

        # --- Sonde 83b: der verlorene Anker -----------------------------------------
        if woertlich not in rtext:
            raise Praeparationsfehler(
                "Sonde 83b: die Spanne `%s` steht nicht woertlich in %s - die Sonde "
                "hat ihren Gegenstand verloren" % (woertlich, P83_ROADMAP))
        ohne = rtext.replace("** bis **D-", "** und **D-")
        schreib(rpfad, ohne)
        aus = validator_ausgabe(root)
        melde("SONDE", "83b", M83_ANKER in aus,
              "Geht die Spannenschreibweise verloren, meldet die Pruefung es - eine "
              "Konsistenzpruefung ohne Anker bestuende sonst leise (D-23)")
        if M83_ANKER not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
        schreib(rpfad, rtext)

        # --- Gegenprobe 83c: DIE SYNTHETISCHE KENNUNG GEHOERT HERAUS ---------------
        # 🔴 DIESE EINHEIT IST EIN GEMESSENER BEFUND, NICHT EINE VORSICHTSMASSNAHME.
        # Die Gegenprobe 58b legt eine Registerzeile mit die Sondenkennung von Prüfung 58 an - der Kennung, die
        # den Sonden gehoert. Beim ersten Abnahmelauf von 1.2.0 las diese Pruefung sie
        # als hoechste vergebene und meldete 654 fehlende Entscheidungen. Der Befund
        # dahinter war groesser: die Sondenkennung von Prüfung 58 stand in KEINER Liste der belegten
        # synthetischen Kennungen, obwohl der Apparat sie seit 0.70.0 benutzt - und
        # Pruefung 50 wie 58 konnten es nie sehen, weil sie eine GENANNTE Kennung ohne
        # Registerzeile melden und diese hier ihre Zeile selbst anlegt.
        # ➡️ Erst eine Pruefung, die die OBERGRENZE misst statt der Zugehoerigkeit,
        # trifft sie. Diese Einheit haelt fest, dass sie herausgenommen bleibt.
        synth = "D-" + "993"
        zeile_s = ("| %s | Sondenentscheidung | Sondenbegruendung | Sondenalternative "
                   "| entschieden | 2026-01-01 |" % synth)
        stelle = dtext.index("\n", dtext.index(anker))
        schreib(dpfad, dtext[:stelle] + "\n" + zeile_s + dtext[stelle:])
        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "83c", M83_FEHLEND not in aus and M83_UEBER not in aus,
              "Die synthetische Kennung des Pruefapparats hebt die Obergrenze NICHT - "
              "sie gehoert den Sonden und wird nie echt vergeben. Gemessen als Befund "
              "am ersten Abnahmelauf von 1.2.0 (D-335)")
        if M83_FEHLEND in aus or M83_UEBER in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "ROADMAP" in z)[:400])
        schreib(dpfad, dtext)

        # --- Sonde 83c: eine Spanne ueber die hoechste Kennung hinaus ---------------
        zuweit = rtext.replace(woertlich,
                               "**D-%d** bis **D-%d**" % (unten, hoechste + 5), 1)
        if zuweit == rtext:
            raise Praeparationsfehler("Sonde 83c hat nichts geaendert")
        schreib(rpfad, zuweit)
        aus = validator_ausgabe(root)
        melde("SONDE", "83c", M83_UEBER in aus,
              "Eine Spanne ueber die hoechste vergebene Kennung hinaus wird gemeldet - "
              "die Chronik nennt sonst eine Entscheidung, die es nicht gibt")
        if M83_UEBER not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_chronikspanne,
        "Pruefung 83 haelt die Chronik gegen das Register und ist gegen eine "
        "unsortierte Releasetabelle fest, ohne eine Kennung woertlich zu kennen")


# --- Pruefung 84: die Vorlage ist kein Client Pack (CR-2026-131) -------------------
#
# VIER EINHEITEN, UND DIE GEGENPROBE IST HIER DIE HAELFTE DES BEFUNDES.
#   84a (Gegenprobe) - 🔴 DIE MESSUNG, DIE D-336 AUSGELOEST HAT, ALS DAUERHAFTE
#                      EINHEIT. Die Vorlage mit einem Probemanifest laeuft NICHT mehr
#                      als drittes Pack mit: `_client_packs()` nimmt sie seit D-336
#                      nicht auf. Gemessen am 2026-09-23 war genau das der Befund -
#                      drei Packs mit Manifest und 0 Fehler. Diese Einheit haelt fest,
#                      dass die Ausnahme greift, und nicht nur, dass Pruefung 84
#                      meldet.
#   84b (Gegenprobe) - die unveraenderte Vorlage laeuft durch, und die Pruefung ist
#                      dabei nachweislich gelaufen.
#   84a (Sonde)      - ein manifest.json in der Vorlage wird gemeldet.
#   84b (Sonde)      - ein root-template/ in der Vorlage wird gemeldet.
#   84c (Sonde)      - die fehlende CLIENT_PACK.md wird gemeldet, statt leise zu
#                      bestehen (D-23).
M84_BESTANDTEIL = "die Vorlage traegt einen Bestandteil"
M84_FEHLT = "Sie ist der einzige Bestandteil, den die Vorlage traegt"
M84_VERZEICHNIS = "nimmt sie seit D-336 ausdruecklich NICHT auf"

P84_VORLAGE = ".koolie/core/clients/_template"
P84_VORBILD = ".koolie/core/clients/claude-code"


def sonden_vorlage_kein_pack() -> None:
    """Wirkungsnachweis zu Pruefung 84."""
    root = kopie()
    try:
        vdir = P(root, *P84_VORLAGE.split("/"))
        vorbild = P(root, *P84_VORBILD.split("/"))
        mpfad = os.path.join(vdir, "manifest.json")
        cpfad = os.path.join(vdir, "CLIENT_PACK.md")
        ctext = lies(cpfad)

        # --- Gegenprobe 84b: die unveraenderte Vorlage laeuft durch -----------------
        aus = validator_ausgabe(root)
        ok = (M84_BESTANDTEIL not in aus and M84_FEHLT not in aus
              and M84_VERZEICHNIS not in aus)
        melde("GEGENPROBE", "84b", ok,
              "Die unveraenderte Vorlage laeuft durch - sie traegt genau eine "
              "CLIENT_PACK.md, und die Pruefung ist dabei nachweislich gelaufen")
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "_template" in z)[:400])

        # --- Gegenprobe 84a: DIE MESSUNG, DIE D-336 AUSGELOEST HAT ------------------
        # Ein Probemanifest in der Vorlage - eine Kopie des Manifests eines ECHTEN
        # Clients. Vor D-336 lief die Vorlage damit als drittes Pack durch alle
        # Pruefungen, und der Validator meldete NULL. Danach meldet Pruefung 84 den
        # Bestandteil, und KEINE andere Pruefung nimmt die Vorlage als Pack auf.
        schreib(mpfad, lies(os.path.join(vorbild, "manifest.json")))
        aus = validator_ausgabe(root)
        fremd = [z for z in aus.splitlines()
                 if "_template" in z and M84_BESTANDTEIL not in z]
        melde("GEGENPROBE", "84a", not fremd,
              "Die Vorlage mit Probemanifest loest KEINE Packpruefung aus - "
              "`_client_packs()` nimmt sie seit D-336 nicht auf. Vor D-336 lief sie "
              "als drittes Pack durch, und der Validator meldete null")
        if fremd:
            notiz("        Ausgabe:", " | ".join(fremd)[:400])

        # --- Sonde 84a: ein manifest.json in der Vorlage ----------------------------
        melde("SONDE", "84a", M84_BESTANDTEIL in aus,
              "Ein manifest.json in der Vorlage wird gemeldet - eine Vorlage, die nur "
              "durch ihre Unvollstaendigkeit ungeprueft bleibt, ist nicht ausgenommen")
        if M84_BESTANDTEIL not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
        os.remove(mpfad)

        # --- Sonde 84b: ein root-template/ in der Vorlage ---------------------------
        rt = os.path.join(vdir, "root-template")
        os.makedirs(rt, exist_ok=True)
        schreib(os.path.join(rt, "README.md"), "# Probe 84b\n")
        aus = validator_ausgabe(root)
        melde("SONDE", "84b", M84_BESTANDTEIL in aus,
              "Ein root-template/ in der Vorlage wird gemeldet - derselbe Zuschnitt "
              "wie beim Manifest, und beide stehen in clients/README.md Abschnitt 3")
        if M84_BESTANDTEIL not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
        shutil.rmtree(rt)

        # --- Sonde 84c: die fehlende CLIENT_PACK.md ---------------------------------
        os.remove(cpfad)
        aus = validator_ausgabe(root)
        melde("SONDE", "84c", M84_FEHLT in aus,
              "Geht die CLIENT_PACK.md der Vorlage verloren, meldet die Pruefung es - "
              "ohne ihren Gegenstand bestuende sie leise (D-23)")
        if M84_FEHLT not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
        schreib(cpfad, ctext)
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_vorlage_kein_pack,
        "Pruefung 84 haelt die Vorlage aus der Packmenge heraus, und die Gegenprobe "
        "misst die Ausnahme selbst und nicht nur die Meldung")


# --- Pruefung 85: eine Zielangabe ueberlebt ihr Release nicht (CR-2026-132) --------
#
# VIER EINHEITEN, UND DIE ZWEITE GEGENPROBE IST DIE, DIE MAN WEGLASSEN WUERDE.
#   85a (Gegenprobe) - die berichtigte ROADMAP laeuft durch, und die Pruefung ist dabei
#                      nachweislich gelaufen.
#   85b (Gegenprobe) - 🔴 EINE ZIELANGABE IN DER ZUKUNFT MUSS DURCHLAUFEN. Ohne diese
#                      Einheit koennte die Pruefung jede Ueberschrift melden und saehe
#                      dabei genauso gruen aus wie eine, die die Sache misst. Sie
#                      traegt zugleich die benannte Grenze: Ein Abschnitt, dessen Ziel
#                      in der Zukunft liegt, kann laengst erledigt sein und kommt durch
#                      (K-116).
#   85a (Sonde)      - eine Zielangabe, die VERSION erreicht hat, wird gemeldet - der
#                      gemessene Fall aus dem Vorbedingungsdurchgang von 1.3.0.
#   85b (Sonde)      - der verlorene Anker: verschwindet die Zielangabe aus der
#                      Ueberschrift, meldet die Pruefung es, statt leise zu bestehen
#                      (D-23). Das ist zugleich die Probe auf D-124: Ein Posten ohne
#                      Zahl bleibt liegen - und entzoege sich dieser Pruefung.
M85_ERREICHT = "ist erreicht. Entweder ist der Posten"
M85_OHNE_ZIEL = "nennen kein Ziel-Release"
M85_ANKER = "keine Ueberschrift '### Geplant: …' gefunden"

P85_ROADMAP = ".koolie/core/docs/ROADMAP.md"
P85_VERSION = ".koolie/core/VERSION"


def _85_ueberschrift(text: str) -> str:
    """Die erste Planueberschrift mit Zielangabe - ausgerechnet, nicht gewusst."""
    for zeile in text.splitlines():
        if zeile.startswith("### Geplant:") and "Ziel-Release" in zeile:
            return zeile
    raise Praeparationsfehler(
        "Sonden zu 85: keine Ueberschrift '### Geplant: … Ziel-Release …' in %s - die "
        "Sonden haben ihren Gegenstand verloren" % P85_ROADMAP)


def sonden_zielangabe() -> None:
    """Wirkungsnachweis zu Pruefung 85."""
    root = kopie()
    try:
        rpfad = P(root, *P85_ROADMAP.split("/"))
        rtext = lies(rpfad)
        stand = lies(P(root, *P85_VERSION.split("/"))).strip()
        kopf = _85_ueberschrift(rtext)

        # --- Gegenprobe 85a: die berichtigte ROADMAP laeuft durch ------------------
        aus = validator_ausgabe(root)
        ok = (M85_ERREICHT not in aus and M85_OHNE_ZIEL not in aus
              and M85_ANKER not in aus)
        melde("GEGENPROBE", "85a", ok,
              "Die berichtigte ROADMAP laeuft durch - jede Zielangabe eines "
              "Planabschnitts liegt ueber %s, und die Pruefung ist dabei nachweislich "
              "gelaufen" % stand)
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "Ziel-Release" in z)[:400])

        # --- Gegenprobe 85b: EINE ZIELANGABE IN DER ZUKUNFT LAEUFT DURCH -----------
        # 🔴 DIE EINHEIT, DIE MAN WEGLASSEN WUERDE. Ohne sie waere nicht gemessen, dass
        # die Pruefung die SACHE prueft und nicht die Schreibweise - eine Pruefung, die
        # jede Planueberschrift meldet, saehe an Sonde 85a genauso gruen aus.
        haupt = int(stand.split(".")[0])
        zukunft = re.sub(r"Ziel-Release\s*\**\s*`?~?[\d.]+`?\**",
                         "Ziel-Release **%d.0.0**" % (haupt + 1), kopf, count=1)
        if zukunft == kopf:
            raise Praeparationsfehler("Gegenprobe 85b hat nichts geaendert")
        schreib(rpfad, rtext.replace(kopf, zukunft, 1))
        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "85b", M85_ERREICHT not in aus,
              "Eine Zielangabe in der ZUKUNFT laeuft durch - die Pruefung misst die "
              "Zahl gegen VERSION und nicht die Schreibweise. Sie traegt damit ihre "
              "benannte Grenze: ein Abschnitt, dessen Ziel noch aussteht, kann laengst "
              "erledigt sein und kommt durch (K-116)")
        if M85_ERREICHT in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "Ziel-Release" in z)[:400])

        # --- Sonde 85a: eine Zielangabe, die VERSION erreicht hat ------------------
        vorher = baumhash(root)
        erreicht = re.sub(r"Ziel-Release\s*\**\s*`?~?[\d.]+`?\**",
                          "Ziel-Release **0.1.0**", kopf, count=1)
        schreib(rpfad, rtext.replace(kopf, erreicht, 1))
        if baumhash(root) == vorher:
            raise Praeparationsfehler("Sonde 85a hat nichts geschrieben")
        aus = validator_ausgabe(root)
        melde("SONDE", "85a", M85_ERREICHT in aus,
              "Ein Planabschnitt, dessen Ziel-Release erreicht ist, wird gemeldet - der "
              "gemessene Fall: ALLE DREI Abschnitte standen so da, einer davon seit "
              "fuenfzehn Releases (D-342)")
        if M85_ERREICHT not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])

        # --- Sonde 85b: der verlorene Anker ----------------------------------------
        ohne = re.sub(r"\s*–?\s*Ziel-Release\s*\**\s*`?~?[\d.]+`?\**", "", kopf, count=1)
        if ohne == kopf:
            raise Praeparationsfehler("Sonde 85b hat nichts geaendert")
        schreib(rpfad, rtext.replace(kopf, ohne, 1))
        aus = validator_ausgabe(root)
        melde("SONDE", "85b", M85_OHNE_ZIEL in aus,
              "Eine Planueberschrift OHNE Zielangabe wird gemeldet - sonst waere das "
              "Streichen der Zahl der billigste Weg, diese Pruefung loszuwerden, und "
              "ein Posten ohne Zahl bleibt in diesem Projekt liegen (D-124, D-342)")
        if M85_OHNE_ZIEL not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
        schreib(rpfad, rtext)
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_zielangabe,
        "Pruefung 85 haelt die Zielangabe eines Planabschnitts gegen VERSION, und die "
        "zweite Gegenprobe belegt, dass sie die Zahl misst und nicht die Schreibweise")



# --- Pruefung 86: die Sperrform des Schutz-Hooks (CR-2026-133) ----------------------
#
# VIER EINHEITEN, UND DIE ZWEITE GEGENPROBE IST DIE, DIE MAN WEGLASSEN WUERDE.
#   86a (Gegenprobe) - der ausgelieferte Bestand laeuft durch: Das Pack nennt eine
#                      Sperrform, das Skript kennt sie, das Kommando reicht sie durch.
#   86b (Gegenprobe) - 🔴 EIN PACK OHNE EIGENE SPERRFORM MUSS DURCHLAUFEN. Ohne diese
#                      Einheit koennte die Pruefung jedes Pack melden und saehe an 86a
#                      genauso gruen aus. Zwei der drei Packs fuehren kein
#                      hook_block_form, und fuer sie gilt die Standardform.
#   86a (Sonde)      - eine Sperrform, die das Skript nicht kennt, wird gemeldet. Das
#                      ist der gemessene Fall in seiner gefaehrlichen Richtung: Der
#                      Hook laeuft, gibt etwas aus und sperrt nichts.
#   86b (Sonde)      - der verlorene Durchreich: Verschwindet die Form aus dem Kommando
#                      der erzeugten Hook-Datei, meldet die Pruefung es. Ohne diese
#                      Einheit waere die dritte Stufe der Kette ungemessen - und genau
#                      sie ist die, die im Projekt ankommt.
M86_UNBEKANNT = "kennt das Skript des Schutz-Hooks nicht"
M86_KOMMANDO = "das Kommando des Schutz-Hooks trägt die Sperrform"

P86_PACK = "openai-codex"


def sonden_sperrform() -> None:
    """Wirkungsnachweis zu Pruefung 86."""
    root = installation(P86_PACK)
    try:
        mpfad = P(root, ".koolie/core", "clients", P86_PACK, "manifest.json")
        mtext = lies(mpfad)
        man = json.loads(mtext)
        form = man.get("hook_block_form")
        if not form:
            raise Praeparationsfehler(
                "Sonden zu 86: %s fuehrt kein hook_block_form - die Sonden haben "
                "ihren Gegenstand verloren" % P86_PACK)
        hpfad = P(root, *man["runtime_placeholders"]["<HOOKS_FILE>"].split("/"))
        htext = lies(hpfad)

        # --- Gegenprobe 86a: der ausgelieferte Bestand laeuft durch ----------------
        aus = validator_ausgabe(root)
        ok = M86_UNBEKANNT not in aus and M86_KOMMANDO not in aus
        melde("GEGENPROBE", "86a", ok,
              "Das ausgelieferte Pack laeuft durch: Es nennt die Sperrform '%s', das "
              "Skript kennt sie und gibt sie aus, und das erzeugte Kommando reicht sie "
              "durch" % form)
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "Sperrform" in z)[:400])

        # --- Gegenprobe 86b: ein Pack OHNE eigene Sperrform laeuft durch -----------
        # 🔴 DIE EINHEIT, DIE MAN WEGLASSEN WUERDE. Zwei der drei Packs fuehren kein
        # hook_block_form; fuer sie gilt die Standardform, und die Pruefung darf sie
        # nicht melden. Ohne diese Einheit waere nicht gemessen, dass sie die SACHE
        # prueft und nicht die Anwesenheit eines Feldes.
        schreib(mpfad, mtext.replace('"hook_block_form": "%s",' % form, "", 1))
        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "86b", M86_UNBEKANNT not in aus,
              "Ein Pack ohne eigene Sperrform laeuft durch - es faellt auf die "
              "Standardform zurueck, und die pruefen dieselben drei Stufen")
        if M86_UNBEKANNT in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "Sperrform" in z)[:400])
        schreib(mpfad, mtext)

        # --- Sonde 86a: eine Sperrform, die das Skript nicht kennt -----------------
        vorher = baumhash(root)
        schreib(mpfad, mtext.replace('"hook_block_form": "%s"' % form,
                                     '"hook_block_form": "gibt-es-nicht"', 1))
        if baumhash(root) == vorher:
            raise Praeparationsfehler("Sonde 86a hat nichts geschrieben")
        aus = validator_ausgabe(root)
        melde("SONDE", "86a", M86_UNBEKANNT in aus,
              "Eine Sperrform, die das Skript nicht kennt, wird gemeldet - sonst liefe "
              "der Hook mit der Standardform, und die ist bei diesem Client gemessen "
              "wirkungslos (D-347)")
        if M86_UNBEKANNT not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
        schreib(mpfad, mtext)

        # --- Sonde 86b: der verlorene Durchreich -----------------------------------
        schreib(hpfad, htext.replace(" --sperrform " + form, "", 1))
        aus = validator_ausgabe(root)
        melde("SONDE", "86b", M86_KOMMANDO in aus,
              "Faellt die Sperrform aus dem erzeugten Kommando, wird es gemeldet - das "
              "Manifest allein belegt nichts, im Projekt ankommt das Kommando")
        if M86_KOMMANDO not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
        schreib(hpfad, htext)
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_sperrform,
        "Pruefung 86 misst die Sperrform an ihrer Wirkung und an ihrem Durchreich, und "
        "die zweite Gegenprobe belegt, dass ein Pack ohne eigene Form durchlaeuft")


# --- Pruefung 87: die formatgebundenen Pruefungen stehen im Pack (CR-2026-133) ------
#
#   87a (Gegenprobe) - das ausgelieferte Pack nennt alle Nummern und laeuft durch.
#   87b (Gegenprobe) - 🔴 EIN PACK MIT DER FORM 'json' WIRD NICHT GEFRAGT. Ohne diese
#                      Einheit koennte die Pruefung von jedem Pack die Liste verlangen
#                      und saehe an 87a genauso gruen aus - zwei der drei Packs haben
#                      keine Luecke zu erklaeren.
#   87a (Sonde)      - fehlt eine Nummer, wird sie gemeldet. Der eigentliche Zweck:
#                      Eine Pruefung, die ein Pack nicht erreicht, steht dort.
#   87b (Sonde)      - steht eine Nummer zuviel, wird sie gemeldet. Eine behauptete
#                      Luecke, die es nicht gibt, ist so falsch wie eine verschwiegene.
M87_FEHLEND = "sind an die Ausgabeform 'json'"
M87_ZUVIEL = "werden als formatgebunden"


# Die Menge steht seit 1.19.1 im gemeinsamen Modul des Validators (K-174).
P87_GEMEINSAM = ".koolie/core/tests/scripts/pruefungen/gemeinsam.py"


def sonden_formatgebunden() -> None:
    """Wirkungsnachweis zu Pruefung 87."""
    root = kopie()
    try:
        ppfad = P(root, ".koolie/core", "clients", P86_PACK, "CLIENT_PACK.md")
        ptext = lies(ppfad)
        nummern = sorted(re.findall(r"^ *(\d+): ", lies(
            P(root, *P87_GEMEINSAM.split("/"))).split("FORMATGEBUNDENE_PRUEFUNGEN = {")[1]
            .split("}")[0], re.M), key=int)
        if not nummern:
            raise Praeparationsfehler(
                "Sonden zu 87: FORMATGEBUNDENE_PRUEFUNGEN ist leer - die Sonden haben "
                "ihren Gegenstand verloren")

        # --- Gegenprobe 87a: das ausgelieferte Pack laeuft durch -------------------
        aus = validator_ausgabe(root)
        ok = M87_FEHLEND not in aus and M87_ZUVIEL not in aus
        melde("GEGENPROBE", "87a", ok,
              "Das ausgelieferte Pack nennt alle %d formatgebundenen Pruefungen in "
              "Abschnitt 5 und laeuft durch" % len(nummern))
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "formatgebunden" in z
                or "Ausgabeform" in z)[:400])

        # --- Gegenprobe 87b: ein Pack mit der Form 'json' wird nicht gefragt -------
        # 🔴 DIE EINHEIT, DIE MAN WEGLASSEN WUERDE.
        cc = P(root, ".koolie/core", "clients", "claude-code", "CLIENT_PACK.md")
        ccalt = lies(cc)
        melde("GEGENPROBE", "87b",
              ("clients/claude-code/CLIENT_PACK.md Abschnitt 5" not in aus
               and "clients/devin-desktop/CLIENT_PACK.md Abschnitt 5" not in aus),
              "Die beiden Packs mit der Ausgabeform 'json' werden nicht gefragt - sie "
              "haben keine Luecke zu erklaeren, und die Pruefung verlangt von ihnen "
              "keine Liste")
        del ccalt, cc

        # --- Sonde 87a: eine fehlende Nummer ---------------------------------------
        vorher = baumhash(root)
        weg = "Prüfung " + nummern[0]
        if weg not in ptext:
            raise Praeparationsfehler(
                "Sonde 87a: '%s' steht nicht in Abschnitt 5 des Packs" % weg)
        schreib(ppfad, ptext.replace(weg, "Pruefung " + nummern[0], 1))
        if baumhash(root) == vorher:
            raise Praeparationsfehler("Sonde 87a hat nichts geschrieben")
        aus = validator_ausgabe(root)
        melde("SONDE", "87a", M87_FEHLEND in aus,
              "Eine formatgebundene Pruefung, die das Pack nicht nennt, wird gemeldet - "
              "eine Luecke, die nirgends steht, ist ein blinder Fleck (D-346)")
        if M87_FEHLEND not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])

        # --- Sonde 87b: eine Nummer zuviel ------------------------------------------
        schreib(ppfad, ptext.replace("## 6.", "Prüfung 999 erreicht dieses Pack "
                                     "ebenfalls nicht.\n\n## 6.", 1))
        aus = validator_ausgabe(root)
        melde("SONDE", "87b", M87_ZUVIEL in aus,
              "Eine behauptete Luecke, die es nicht gibt, wird gemeldet - sonst waere "
              "die Liste eine Erzaehlung und kein Abbild des Pruefapparats")
        if M87_ZUVIEL not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
        schreib(ppfad, ptext)
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_formatgebunden,
        "Pruefung 87 verlangt die Liste der formatgebundenen Pruefungen nur von dem "
        "Pack, das eine andere Ausgabeform fuehrt - und in beide Richtungen")


# --- Pruefung 88: die verdraengende Wurzel-Anweisung (CR-2026-133) ------------------
#
#   88a (Gegenprobe) - die frische Installation laeuft durch; die Datei gibt es nicht.
#   88b (Gegenprobe) - 🔴 EIN PACK OHNE VERDRAENGUNG WIRD NICHT GEFRAGT. Bei den beiden
#                      aelteren Packs ERGAENZT die nutzerlokale Datei, sie ersetzt
#                      nicht - dort waere ihre Anwesenheit kein Befund. Ohne diese
#                      Einheit koennte die Pruefung jede nutzerlokale Datei melden und
#                      saehe an 88a genauso gruen aus.
#   88a (Sonde)      - liegt die Datei im Projekt, wird sie gemeldet.
#   88b (Sonde)      - der verlorene Anker: Faellt das Feld root_instruction_override
#                      weg, prueft die Pruefung nichts mehr - und sagt es, statt leise
#                      zu bestehen (D-23).
M88_VERDRAENGT = "VERDRÄNGT bei diesem Client die"
M88_ANKER = "ist gesetzt, aber <ROOT_INSTRUCTION_LOCAL> fehlt"


def sonden_verdraengung() -> None:
    """Wirkungsnachweis zu Pruefung 88."""
    root = installation(P86_PACK)
    try:
        mpfad = P(root, ".koolie/core", "clients", P86_PACK, "manifest.json")
        mtext = lies(mpfad)
        man = json.loads(mtext)
        lokal = man["runtime_placeholders"]["<ROOT_INSTRUCTION_LOCAL>"]
        lpfad = P(root, *lokal.split("/"))

        # --- Gegenprobe 88a: die frische Installation laeuft durch ----------------
        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "88a", M88_VERDRAENGT not in aus,
              "Die frische Installation laeuft durch - das Framework legt die "
              "verdraengende Datei nicht an, und es liefert auch keine Vorlage dafuer")

        # --- Gegenprobe 88b: ein Pack ohne Verdraengung wird nicht gefragt ---------
        # 🔴 DIE EINHEIT, DIE MAN WEGLASSEN WUERDE.
        schreib(lpfad, "# Persoenliche Fassung\n")
        schreib(mpfad, mtext.replace('"root_instruction_override": true,', "", 1))
        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "88b", M88_VERDRAENGT not in aus,
              "Dieselbe Datei bei einem Pack OHNE Verdraengung ist kein Befund - dort "
              "ergaenzt sie, und eine Ergaenzung ist der dokumentierte Weg")
        if M88_VERDRAENGT in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "VERDR" in z)[:400])
        schreib(mpfad, mtext)

        # --- Sonde 88a: die Datei liegt im Projekt ---------------------------------
        aus = validator_ausgabe(root)
        melde("SONDE", "88a", M88_VERDRAENGT in aus,
              "Liegt die verdraengende Datei im Projekt, wird sie gemeldet - sonst "
              "ersetzt eine ungepruefte Datei die Ebene 1, und nichts sagt es (D-341)")
        if M88_VERDRAENGT not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])

        # --- Sonde 88b: der verlorene Anker ----------------------------------------
        ohne = json.loads(mtext)
        ohne["runtime_placeholders"].pop("<ROOT_INSTRUCTION_LOCAL>", None)
        schreib(mpfad, json.dumps(ohne, indent=2, ensure_ascii=False) + "\n")
        aus = validator_ausgabe(root)
        melde("SONDE", "88b", M88_ANKER in aus,
              "Verschwindet die Angabe, welche Datei verdraengt, meldet die Pruefung "
              "das selbst - eine Pruefung ohne Gegenstand besteht sonst leise (D-23)")
        if M88_ANKER not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
        schreib(mpfad, mtext)
        os.remove(lpfad)
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_verdraengung,
        "Pruefung 88 meldet die Datei, die die Wurzel-Anweisung verdraengt - und die "
        "zweite Gegenprobe belegt, dass sie nur dort fragt, wo sie verdraengt")


# --- Pruefungen 91 bis 94: die Dokumentation (CR-2026-142) --------------------------
#
# Je Pruefung ein Buendel auf EINER Kopie. Die Gegenproben tragen das Gewicht: Jede der
# vier Pruefungen liest ueber zweihundert Dokumente, und eine, die zu breit greift,
# meldete Zitate, Register oder Vorlagen - und saehe an ihrer Sonde genauso gruen aus.
M91_STAND = "die Standüberschrift nennt Release"
M91_ANKER = "Prüfung 91 hält sie gegen"
M92 = "in der Schreibung vor 1996"
M93_ZAUN = "ein Codeblock ist bis zum Dateiende nicht geschlossen"
M93_H1 = "Hauptüberschriften ('# ')"
M93_EBENE = "eine Ebene ist übersprungen"
M93_TABELLE = "Spalten – ein ungeschützter senkrechter Strich"
M94_OHNE_ID = "Steckbrief ohne ID"
M94_KEINER = "kein Steckbrief vor dem ersten Abschnitt"

P91_ROADMAP = ".koolie/core/docs/ROADMAP.md"
P92_REGEL = ".koolie/core/governance/RELEASE_PROCESS.md"
P92_KAPITEL = ".koolie/core/build/doc/29-grenzen.md"
P92_REGISTER = ".koolie/core/CHANGELOG.md"
P92_KENNZEICHEN = ".koolie/QUELLREPOSITORIUM.md"
P93_REGEL = ".koolie/core/framework/core/05-working-model.md"
P94_REGEL = ".koolie/core/governance/RACI.md"


def _anhaengen(pfad: str, *zeilen: str) -> None:
    schreib(pfad, lies(pfad).rstrip("\r\n") + "\r\n\r\n" + "\r\n".join(zeilen) + "\r\n")


def _zeilen_mit(aus: str, marke: str) -> str:
    return " | ".join(z for z in aus.splitlines() if marke in z)[:400]


def sonden_roadmapstand() -> None:
    """Wirkungsnachweis zu Pruefung 91."""
    root = kopie()
    try:
        pfad = P(root, *P91_ROADMAP.split("/"))
        text = lies(pfad)
        kopf = next((z for z in text.split("\r\n") if z.startswith("## Stand nach Release ")), None)
        if kopf is None:
            raise Praeparationsfehler("Sonden zu 91: keine Standueberschrift in %s" % P91_ROADMAP)

        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "91a", M91_STAND not in aus and M91_ANKER not in aus,
              "Die Standueberschrift der ausgelieferten Roadmap nennt VERSION und laeuft "
              "durch")

        alt = re.sub(r"Release `?\d+\.\d+\.\d+`?", "Release 1.4.4", kopf, count=1)
        if alt == kopf:
            raise Praeparationsfehler("Sonde 91a hat nichts geaendert")
        schreib(pfad, text.replace(kopf, alt, 1))
        aus = validator_ausgabe(root)
        melde("SONDE", "91a", M91_STAND in aus,
              "Eine Standueberschrift, die ein frueheres Release nennt, wird gemeldet - "
              "der gemessene Fall von 1.8.0: vier Releases zurueck")
        if M91_STAND not in aus:
            notiz("        Ausgabe:", _zeilen_mit(aus, "FEHLER"))

        schreib(pfad, text.replace(kopf, "## Stand der Dinge", 1))
        aus = validator_ausgabe(root)
        melde("SONDE", "91b", M91_ANKER in aus,
              "Der verlorene Anker: ohne Standueberschrift meldet die Pruefung es, statt "
              "leise zu bestehen (D-23)")
        if M91_ANKER not in aus:
            notiz("        Ausgabe:", _zeilen_mit(aus, "FEHLER"))
        schreib(pfad, text)
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_roadmapstand,
        "Pruefung 91 haelt die Standueberschrift der Roadmap gegen VERSION und meldet "
        "den verlorenen Anker")


def sonden_rechtschreibung() -> None:
    """Wirkungsnachweis zu Pruefung 92."""
    root = kopie()
    try:
        regel, kapitel, register = (P(root, *x.split("/")) for x in (P92_REGEL, P92_KAPITEL,
                                                                     P92_REGISTER))
        texte = {p: lies(p) for p in (regel, kapitel, register)}

        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "92a", M92 not in aus,
              "Der ausgelieferte Bestand der Klassen A, B und D laeuft durch - ohne "
              "Schreibung vor 1996")
        if M92 in aus:
            notiz("        Ausgabe:", _zeilen_mit(aus, M92))

        # --- Gegenprobe 92b: Zitat und Register ------------------------------------
        # 🔴 DIE EINHEIT, DIE MAN WEGLASSEN WUERDE. Code ist Zitat - ein Befehl, eine
        # Meldung, die woertlich so lautet -, und ein Register wird nicht umgeschrieben
        # (D-371). Eine Pruefung, die beides meldete, verlangte eine Faelschung.
        _anhaengen(regel, "Zitat einer alten Meldung: `daß der Lauf mißt`", "",
                   "```text", "Meßbaum muß bleiben, weil es ein Zitat ist", "```")
        _anhaengen(register, "Sondenzeile im Register: daß, muß, Meßbaum")
        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "92b", M92 not in aus,
              "Alte Schreibung im Inline-Code, im Codeblock und im CHANGELOG wird NICHT "
              "gemeldet - Zitat und Register bleiben, wie sie sind")
        if M92 in aus:
            notiz("        Ausgabe:", _zeilen_mit(aus, M92))
        for p, t in texte.items():
            schreib(p, t)

        # --- Sonde 92a: Klasse B -----------------------------------------------------
        _anhaengen(regel, "Sondenzeile: Der Schritt mißt, daß nichts fehlt.")
        aus = validator_ausgabe(root)
        treffer = [z for z in aus.splitlines() if M92 in z and "RELEASE_PROCESS.md" in z]
        melde("SONDE", "92a", bool(treffer) and "mißt" in treffer[0] and "daß" in treffer[0],
              "Alte Schreibung im Fliesstext eines Regeldokuments wird gemeldet, mit "
              "Zeile und Wort")
        if not treffer:
            notiz("        Ausgabe:", _zeilen_mit(aus, "FEHLER"))
        schreib(regel, texte[regel])

        # --- Sonde 92b: Klasse D -----------------------------------------------------
        _anhaengen(kapitel, "Sondenzeile: der Meßbaum.")
        aus = validator_ausgabe(root)
        ok = any(M92 in z and "29-grenzen.md" in z for z in aus.splitlines())
        melde("SONDE", "92b", ok,
              "Alte Schreibung in einer Kapitelquelle des Hauptdokuments wird gemeldet - "
              "build/doc gehoert zu Klasse D, obwohl build/ Nachweisschicht ist")
        if not ok:
            notiz("        Ausgabe:", _zeilen_mit(aus, "FEHLER"))
        schreib(kapitel, texte[kapitel])

        # --- Gegenprobe 92c: die Wurzel eines Projekts gehoert dem Projekt -----------
        # D-299: Ohne das Kennzeichen des Quellrepositoriums ist dieser Baum ein
        # Projekt, und dessen README.md ist nicht Gegenstand dieser Pruefung.
        readme = P(root, "README.md")
        rtext = lies(readme)
        _anhaengen(readme, "Sondenzeile im Projekt: daß.")
        os.remove(P(root, *P92_KENNZEICHEN.split("/")))
        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "92c",
              not any(M92 in z and z.split()[1].startswith("README.md") for z in aus.splitlines()
                      if z.startswith("FEHLER")),
              "In einem Projekt ohne Kennzeichen des Quellrepositoriums wird die "
              "Wurzel-README nicht geprueft - sie gehoert dem Projekt (D-299)")
        schreib(readme, rtext)
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_rechtschreibung,
        "Pruefung 92 meldet alte Schreibung in Regel- und Kapiteltexten und laesst Zitat, "
        "Register und die Wurzel eines Projekts stehen")


def sonden_dokumentform() -> None:
    """Wirkungsnachweis zu Pruefung 93."""
    root = kopie()
    try:
        pfad = P(root, *P93_REGEL.split("/"))
        text = lies(pfad)
        alle = (M93_ZAUN, M93_H1, M93_EBENE, M93_TABELLE)

        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "93a", not any(m in aus for m in alle),
              "Der ausgelieferte Bestand aller vier Klassen ist formal sauber")
        if any(m in aus for m in alle):
            notiz("        Ausgabe:", _zeilen_mit(aus, "(D-374)"))

        # --- Gegenprobe 93b: was wie ein Formfehler aussieht und keiner ist ----------
        _anhaengen(pfad,
                   "| Befehl | Wirkung |", "|---|---|",
                   "| `a | b` | ein senkrechter Strich im Code |",
                   "| a \\| b | ein geschuetzter Strich |", "",
                   "```text", "# keine Ueberschrift, sondern eine Zeile im Codeblock",
                   "#### auch keine", "```")
        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "93b", not any(m in aus for m in alle),
              "Senkrechter Strich im Code und geschuetzt sowie Rautenzeilen im Codeblock "
              "werden NICHT gemeldet")
        if any(m in aus for m in alle):
            notiz("        Ausgabe:", _zeilen_mit(aus, "(D-374)"))
        schreib(pfad, text)

        def _sonde_93(zeilen: tuple, marke: str) -> tuple:
            _anhaengen(pfad, *zeilen)
            aus = validator_ausgabe(root)
            schreib(pfad, text)
            ok = any(marke in z and "05-working-model.md" in z for z in aus.splitlines())
            return ok, aus

        ok, aus = _sonde_93(("```text", "offen bis zum Ende"), M93_ZAUN)
        melde("SONDE", "93a", ok,
              "Ein Codeblock, der bis zum Dateiende offen bleibt, wird gemeldet (D-374)")
        if not ok:
            notiz("        Ausgabe:", _zeilen_mit(aus, "FEHLER"))

        ok, aus = _sonde_93(("# Zweite Hauptueberschrift",), M93_H1)
        melde("SONDE", "93b", ok, "Eine zweite Hauptueberschrift wird gemeldet (D-374)")
        if not ok:
            notiz("        Ausgabe:", _zeilen_mit(aus, "FEHLER"))

        ok, aus = _sonde_93(("## Sondenabschnitt", "", "#### Sprung ueber eine Ebene"),
                            M93_EBENE)
        melde("SONDE", "93c", ok,
              "Eine uebersprungene Ueberschriftenebene wird gemeldet (D-374)")
        if not ok:
            notiz("        Ausgabe:", _zeilen_mit(aus, "FEHLER"))

        ok, aus = _sonde_93(("| A | B |", "|---|---|", "| eins | zwei | drei |"),
                            M93_TABELLE)
        melde("SONDE", "93d", ok,
              "Eine Tabellenzeile mit mehr Spalten als ihre Kopfzeile wird gemeldet (D-374)")
        if not ok:
            notiz("        Ausgabe:", _zeilen_mit(aus, "FEHLER"))
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_dokumentform,
        "Pruefung 93 meldet offenen Codeblock, zweite Hauptueberschrift, Ebenensprung und "
        "verschobene Tabellenspalten - nicht aber Striche und Rauten im Code")


def sonden_steckbrief() -> None:
    """Wirkungsnachweis zu Pruefung 94."""
    root = kopie()
    try:
        pfad = P(root, *P94_REGEL.split("/"))
        text = lies(pfad)
        idzeile = next((z for z in text.split("\r\n") if re.match(r"\|\s*ID\s*\|", z)), None)
        kopf = next((z for z in text.split("\r\n") if re.sub(r"\s+", " ", z) == "| Attribut | Wert |"),
                    None)
        if idzeile is None or kopf is None:
            raise Praeparationsfehler("Sonden zu 94: %s hat keinen Steckbrief mit ID" % P94_REGEL)

        aus = validator_ausgabe(root)
        ausgenommen = ("framework/runtime/rules/", "templates/", "checklists/README.md",
                       "examples/")
        ok = M94_OHNE_ID not in aus and M94_KEINER not in aus
        melde("GEGENPROBE", "94a", ok,
              "Der ausgelieferte Bestand laeuft durch - Laufzeitregeln, Vorlagen, "
              "Beispiele und README-Verzeichnisse ohne Steckbrief sind ausgenommen")
        if not ok:
            notiz("        Ausgabe:", _zeilen_mit(aus, "(D-375)"))
        # Die Gegenprobe ist nur dann eine, wenn es die Ausgenommenen wirklich gibt.
        fehlend = [a for a in ausgenommen
                   if not os.path.exists(P(root, ".koolie", "core", *a.rstrip("/").split("/")))]
        if fehlend:
            raise Praeparationsfehler("Gegenprobe 94a: Ausnahmen ohne Gegenstand: %s" % fehlend)

        schreib(pfad, text.replace(idzeile + "\r\n", "", 1))
        aus = validator_ausgabe(root)
        ok = any(M94_OHNE_ID in z and "RACI.md" in z for z in aus.splitlines())
        melde("SONDE", "94a", ok,
              "Ein Steckbrief ohne Kennungszeile wird gemeldet (D-375)")
        if not ok:
            notiz("        Ausgabe:", _zeilen_mit(aus, "FEHLER"))

        schreib(pfad, text.replace(kopf, "| Eigenschaft | Wert |", 1))
        aus = validator_ausgabe(root)
        ok = any(M94_KEINER in z and "RACI.md" in z for z in aus.splitlines())
        melde("SONDE", "94b", ok,
              "Ein Regeldokument ohne Tabelle 'Attribut | Wert' vor dem ersten Abschnitt "
              "wird gemeldet (D-375)")
        if not ok:
            notiz("        Ausgabe:", _zeilen_mit(aus, "FEHLER"))
        schreib(pfad, text)
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_steckbrief,
        "Pruefung 94 verlangt Kennung, Version und Status im Steckbrief der Klassen A "
        "und B und laesst Laufzeit, Vorlagen und Verzeichnisse aus")


# --- D-437: die Einstiegsdokumente der Wurzel (CR-2026-154) ---------------------------
#
# Bis 1.14.2 kannte dokumentklasse() ausserhalb des Kerns nur README.md. Mit 1.15.0 liegen
# daneben README.en.md, QUICKSTART.md und QUICKSTART.en.md - ohne die Erweiterung waeren
# sie fuer die Pruefungen 92 und 93 unsichtbar gewesen, und ein offener Codeblock im
# englischen Quickstart haette den Rest der Seite verschluckt, ohne dass etwas meldet.
# Die Gegenproben halten die beiden Ausnahmen: kein Steckbrief (94) und keine Pruefung
# in einem Projekt, dem die Wurzel gehoert (D-299).
P437_EN = "QUICKSTART.en.md"
P437_README_EN = "README.en.md"
P437_DE = "QUICKSTART.md"
P437_KENNZEICHEN = ".koolie/QUELLREPOSITORIUM.md"


def sonden_wurzeldokumente() -> None:
    """Wirkungsnachweis zu D-437: README, Quickstart und ihre englischen Fassungen."""
    root = kopie()
    try:
        pfade = {r: P(root, r) for r in (P437_EN, P437_README_EN, P437_DE)}
        fehlend = [r for r, p in pfade.items() if not os.path.isfile(p)]
        if fehlend:
            raise Praeparationsfehler("Sonden zu D-437: Einstiegsdokumente fehlen: %s" % fehlend)
        texte = {r: lies(p) for r, p in pfade.items()}

        # --- Gegenprobe D437a: der ausgelieferte Stand, ohne Steckbrief --------------
        aus = validator_ausgabe(root)
        stoert = [z for z in aus.splitlines() if z.startswith("FEHLER")
                  and z.split()[1].rstrip(":") in pfade]
        melde("GEGENPROBE", "D437a", not stoert and M94_KEINER not in aus,
              "Die vier Einstiegsdokumente laufen durch - ohne Steckbrief, weil sie von "
              "Pruefung 94 ausgenommen sind wie die README")
        if stoert:
            notiz("        Ausgabe:", " | ".join(stoert)[:400])

        # --- Sonde D437b: ein offener Codeblock im englischen Quickstart ------------
        _anhaengen(pfade[P437_EN], "```bash", "echo offen")
        aus = validator_ausgabe(root)
        ok = any(M93_ZAUN in z and P437_EN in z for z in aus.splitlines())
        melde("SONDE", "D437b", ok,
              "Ein offener Codeblock in QUICKSTART.en.md wird von Pruefung 93 gemeldet")
        if not ok:
            notiz("        Ausgabe:", _zeilen_mit(aus, "FEHLER"))
        schreib(pfade[P437_EN], texte[P437_EN])

        # --- Sonde D437c: alte Schreibung im deutschen Quickstart -------------------
        _anhaengen(pfade[P437_DE], "Sondenzeile: Der Schritt zeigt, daß nichts fehlt.")
        aus = validator_ausgabe(root)
        ok = any(M92 in z and z.split()[1].startswith(P437_DE) for z in aus.splitlines())
        melde("SONDE", "D437c", ok,
              "Alte Schreibung in QUICKSTART.md wird von Pruefung 92 gemeldet")
        if not ok:
            notiz("        Ausgabe:", _zeilen_mit(aus, "FEHLER"))
        schreib(pfade[P437_DE], texte[P437_DE])

        # --- Sonde D437d: zwei Hauptueberschriften in der englischen README ---------
        _anhaengen(pfade[P437_README_EN], "# Zweite Hauptueberschrift")
        aus = validator_ausgabe(root)
        ok = any(M93_H1 in z and P437_README_EN in z for z in aus.splitlines())
        melde("SONDE", "D437d", ok,
              "Eine zweite Hauptueberschrift in README.en.md wird von Pruefung 93 gemeldet")
        if not ok:
            notiz("        Ausgabe:", _zeilen_mit(aus, "FEHLER"))

        # --- Gegenprobe D437e: in einem Projekt gehoert die Wurzel dem Projekt ------
        _anhaengen(pfade[P437_EN], "```bash", "echo offen")
        os.remove(P(root, *P437_KENNZEICHEN.split("/")))
        aus = validator_ausgabe(root)
        stoert = [z for z in aus.splitlines() if z.startswith("FEHLER")
                  and z.split()[1].rstrip(":") in pfade]
        melde("GEGENPROBE", "D437e", not stoert,
              "Ohne Kennzeichen des Quellrepositoriums werden die Einstiegsdokumente der "
              "Wurzel nicht geprueft - sie gehoeren dem Projekt (D-299)")
        if stoert:
            notiz("        Ausgabe:", " | ".join(stoert)[:400])
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_wurzeldokumente,
        "Die Einstiegsdokumente der Wurzel sind Klasse A: 92 und 93 pruefen sie im "
        "Quellrepositorium, 94 laesst sie aus, im Projekt bleiben sie unberuehrt (D-437)")


# --- Pruefung 4: die Zeichengrenze der Wurzel-Anweisung (D-381, CR-2026-143) ---------
#
# Die Grenze von 12.000 Zeichen ist eine Vorgabe des Frameworks, keine Eigenschaft eines
# Clients (CR-2026-027 E3). Sie gilt fuer die INSTALLIERTE Fassung, und die ist je Pack
# verschieden lang: Dieselbe Quelle ergab am 2026-09-25 11.894 Zeichen bei claude-code,
# 11.887 bei devin-desktop und 12.516 bei openai-codex. Dort gilt sie nicht, weil der
# Client Regeldateien nicht von sich aus laedt (has_rule_triggers = false); die Summe
# des stets Geladenen haelt eine Warnung bei 40.000.
# Bis 1.9.0 hatte die Pruefung keine Sonde - eine Durchsicht der Laufzeitschicht, die
# die Wurzel-Anweisung um hundert Zeichen verlaengert, waere erst im Projekt aufgefallen.
M4_GRENZE = "Zeichen (> 12.000, SOLL-Grenze je Datei)"
M4_BUDGET = "Zeichen, die in jeder Sitzung geladen werden (> 40.000"


def _regel_mit_trigger(root: str, man: dict, trigger: str) -> str:
    rd = os.path.join(root, *man["pack_runtime_dir"].split("/"))
    for fn in sorted(os.listdir(rd)):
        p = os.path.join(rd, fn)
        if fn.endswith(".md") and re.search(r"^trigger:\s*%s\s*$" % trigger, lies(p), re.M):
            return p
    raise Praeparationsfehler("Sonden zu 4: keine Regel mit trigger %s" % trigger)


def sonden_zeichengrenze() -> None:
    """Wirkungsnachweis zur Zeichengrenze der Pruefung 4, je Pack gegen die Installation.

    Seit D-387 ist die Summe des stets Geladenen verbindlich (40.000, Fehler) und die
    Grenze je Datei eine Warnung (12.000)."""
    ergebnisse = {}
    for pack in ("claude-code", "devin-desktop", "openai-codex"):
        root = installation(pack)
        try:
            man = json.loads(lies(os.path.join(QUELLE, ".koolie/core", "clients", pack,
                                               "manifest.json")))
            wurzel = os.path.join(root, *man["root_instruction_file"].split("/"))
            if not os.path.isfile(wurzel):
                raise Praeparationsfehler("Sonden zu 4: %s fehlt in der Installation (%s)"
                                          % (man["root_instruction_file"], pack))
            # Von install.py erzeugt, auf jedem Baum LF - roh, sonst zaehlten auf einem
            # LF-Baum die CR der Uebersetzung mit (K-216).
            laenge = len(lies(wurzel, roh=True))
            aus = validator_ausgabe(root)
            ergebnisse[pack] = (laenge, M4_GRENZE not in aus and M4_BUDGET not in aus)
            if pack == "claude-code":
                schreib(wurzel, lies(wurzel, roh=True) + "\r\n" + "x" * (12001 - laenge) + "\r\n",
                        roh=True)
                aus = validator_ausgabe(root)
                ok = any(z.startswith("WARNUNG") and M4_GRENZE in z
                         and man["root_instruction_file"] in z for z in aus.splitlines())
                als_fehler = any(z.startswith("FEHLER") and M4_GRENZE in z
                                 for z in aus.splitlines())
                melde("SONDE", "4a", ok and not als_fehler,
                      "Eine installierte Wurzel-Anweisung ueber 12.000 Zeichen wird als "
                      "Warnung gemeldet, nicht als Fehler (D-387)")
                if not ok:
                    notiz("        Ausgabe:", _zeilen_mit(aus, "WARNUNG"))
            if pack == "devin-desktop":
                bedingt = _regel_mit_trigger(root, man, "model_decision")
                schreib(bedingt, lies(bedingt) + "\r\n" + "x" * 30000 + "\r\n")
                aus = validator_ausgabe(root)
                melde("GEGENPROBE", "4d", M4_BUDGET not in aus,
                      "Eine Regel mit trigger model_decision zaehlt nicht zur Summe des stets "
                      "Geladenen")
                if M4_BUDGET in aus:
                    notiz("        Ausgabe:", _zeilen_mit(aus, "FEHLER"))
                immer = _regel_mit_trigger(root, man, "always_on")
                schreib(immer, lies(immer) + "\r\n" + "x" * 30000 + "\r\n")
                aus = validator_ausgabe(root)
                ok = any(z.startswith("FEHLER") and M4_BUDGET in z for z in aus.splitlines())
                melde("SONDE", "4b", ok,
                      "Wurzel-Anweisung und Regeln mit trigger always_on ueber 40.000 Zeichen "
                      "werden als Fehler gemeldet (D-387)")
                if not ok:
                    notiz("        Ausgabe:", _zeilen_mit(aus, "FEHLER"))
        finally:
            aufraeumen(os.path.dirname(root))

    laenge, ok = ergebnisse["claude-code"]
    melde("GEGENPROBE", "4a", ok and laenge <= 12000,
          "Die ausgelieferte Installation des Packs claude-code meldet weder Budget noch "
          "Grenze (Wurzel-Anweisung %d Zeichen)" % laenge)
    laenge, ok = ergebnisse["devin-desktop"]
    melde("GEGENPROBE", "4b", ok and laenge <= 12000,
          "Die ausgelieferte Installation des Packs devin-desktop meldet weder Budget noch "
          "Grenze (Wurzel-Anweisung %d Zeichen)" % laenge)
    laenge, ok = ergebnisse["openai-codex"]
    melde("GEGENPROBE", "4c", ok,
          "Beim Pack openai-codex meldet die Grenze je Datei nichts, weil die Regeln ueber "
          "die Wurzel-Anweisung eingebunden werden, und das Budget haelt (%d Zeichen)" % laenge)
    notiz("        Zeichen je Pack: " + ", ".join(
        "%s %d" % (p, ergebnisse[p][0]) for p in sorted(ergebnisse)))


buendel(sonden_zeichengrenze,
        "Pruefung 4 haelt das stets Geladene je Pack unter 40.000 Zeichen und warnt ueber "
        "12.000 Zeichen je Datei (D-387)")


# --- Pruefung 95: der Aenderungsverlauf eines Skills nennt die Art (D-403, CR-2026-147) --
#
# Gegenstand ist die Zeile der aktuellen Version und jede Zeile nach dem Stichtag. Die
# Gegenprobe ist der ausgelieferte Bestand: Er fuehrt aeltere Zeilen ohne die Nennung, und
# die duerfen nicht gemeldet werden - sonst schriebe die Pruefung Register um (Klasse C).
M95 = "nennt nicht, ob sie eine Anweisung berührt"
P95_SKILL = ".koolie/core/framework/skills/koolie-docs-update"


def sonden_aenderungsart() -> None:
    """Wirkungsnachweis zu Pruefung 95."""
    root = kopie()
    try:
        cl = P(root, *(P95_SKILL + "/CHANGELOG.md").split("/"))
        sk = P(root, *(P95_SKILL + "/SKILL.md").split("/"))
        text = lies(cl)
        m = re.search(r"^\|\s*Version\s*\|\s*`?([^`|]+?)`?\s*\|", lies(sk), re.M)
        if m is None:
            raise Praeparationsfehler("Sonden zu 95: %s/SKILL.md ohne Version" % P95_SKILL)
        zeilen = text.split("\r\n")
        aktuell = [z for z in zeilen if re.match(r"\|\s*%s\s*\|" % re.escape(m.group(1)), z)]
        alt = [z for z in zeilen if re.match(r"\|\s*\d+\.\d+\.\d+\s*\|\s*2026-09-1\d\s*\|", z)
               and not re.search(r"Anweisung\s+ber(?:ü|ue)hrt", z, re.I)]
        if len(aktuell) != 1 or not alt:
            raise Praeparationsfehler("Sonden zu 95: aktuelle Zeile %d-mal, alte Zeile ohne "
                                      "Nennung %d-mal" % (len(aktuell), len(alt)))

        aus = validator_ausgabe(root)
        ok = M95 not in aus
        melde("GEGENPROBE", "95a", ok,
              "Der ausgelieferte Bestand laeuft durch - aeltere Zeilen ohne Nennung "
              "werden nicht gemeldet")
        if not ok:
            notiz("        Ausgabe:", _zeilen_mit(aus, "(D-403)"))

        ohne = re.sub(r"\*{0,2}Keine Anweisung ber(?:ü|ue)hrt\*{0,2}", "Berichtigt",
                      aktuell[0], flags=re.I)
        if ohne == aktuell[0]:
            raise Praeparationsfehler("Sonde 95a: die aktuelle Zeile traegt keine Nennung")
        schreib(cl, text.replace(aktuell[0], ohne, 1))
        aus = validator_ausgabe(root)
        ok = any(M95 in z and "koolie-docs-update" in z for z in aus.splitlines())
        melde("SONDE", "95a", ok,
              "Die Zeile der aktuellen Version ohne Nennung der Art wird gemeldet (D-403)")
        if not ok:
            notiz("        Ausgabe:", _zeilen_mit(aus, "FEHLER"))

        # Gegenprobe 95b: ein projekteigener Skill in der Laufzeitablage mit einer Zeile
        # ohne Nennung - beim ersten Heben meldete die Pruefung genau das im
        # Uebungsrepositorium (die Erstfassung eines prj-Skills).
        ablage = P(root, ".devin", "skills")
        if not os.path.isdir(ablage):
            raise Praeparationsfehler("Gegenprobe 95b: keine Laufzeitablage .devin/skills "
                                      "in der Kopie - ohne sie hat die Gegenprobe keinen Gegenstand")
        prj = os.path.join(ablage, "prj-sonde95")
        shutil.copytree(P(root, *P95_SKILL.split("/")), prj)
        schreib(os.path.join(prj, "CHANGELOG.md"),
                "# prj-sonde95\r\n\r\n| Version | Datum | Änderung | Autor (Rolle) |\r\n"
                "|---|---|---|---|\r\n| 0.1.0 | 2026-09-24 | Erstfassung | Projekt |\r\n")
        aus = validator_ausgabe(root)
        ok = not any(M95 in z and "prj-sonde95" in z for z in aus.splitlines())
        melde("GEGENPROBE", "95b", ok,
              "Ein projekteigener Skill wird nicht gemeldet - D-303 regelt die Testblaetter "
              "des Kerns")
        if not ok:
            notiz("        Ausgabe:", _zeilen_mit(aus, "prj-sonde95"))
        shutil.rmtree(prj)

        spaet = re.sub(r"2026-09-1\d", "2026-09-24", alt[0], count=1)
        schreib(cl, text.replace(alt[0], spaet, 1))
        aus = validator_ausgabe(root)
        ok = any(M95 in z and "koolie-docs-update" in z for z in aus.splitlines())
        melde("SONDE", "95b", ok,
              "Eine Zeile nach dem Stichtag ohne Nennung wird gemeldet, auch wenn sie "
              "nicht die aktuelle Version ist (D-403)")
        if not ok:
            notiz("        Ausgabe:", _zeilen_mit(aus, "FEHLER"))
        schreib(cl, text)
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_aenderungsart,
        "Pruefung 95 verlangt im Aenderungsverlauf eines Skills die Nennung, ob eine "
        "Anweisung beruehrt ist - fuer die aktuelle Version und nach dem Stichtag")
