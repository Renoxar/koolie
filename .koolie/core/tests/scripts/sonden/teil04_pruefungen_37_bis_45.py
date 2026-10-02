"""Sonden zu den Pruefungen 37 bis 45 und zum Bytecode; Selbstprobe des Aufraeumers.

Teil des Sondenskripts probe-pruefungen.py, seit 1.19.1 in Module geteilt (K-174). Die
Einheiten melden sich beim Laden dieses Moduls an; der Einstieg laedt die Module in der
Reihenfolge ihrer Nummer, und das ist die Reihenfolge der Ausgabe (D-49). Ein Modul
liest nur aus dem Apparat und aus frueheren Teilen."""
from __future__ import annotations

import io
import json
import os
import re
import shutil
import stat
import tempfile

from .apparat import (
    _ORT, _p, aufraeumen, buendel, Einheit, ersetze, ersetzt, frei, gegenprobe,
    installation, lies, melde, notiz, P, Praeparationsfehler, schreib,
    schreibschutz_loesen, sonde, unterprozess, validator_ausgabe, zeile_nach)


# --- Selbstprobe: der Aufraeumer (CR-2026-068, D-96) ------------------------------
#
# Ohne sie waere der Aufraeumer eine ungepruefte Zusage - und zwar ausgerechnet die, die
# an die Stelle von ignore_errors=True getreten ist. Eine Meldung, die geschrieben und
# nie ausgeloest wurde, ist nach D-23 nicht vorhanden.
#
# GEMESSEN WIRD GEGEN EINE HILFSEINHEIT, nicht gegen die laufende: Der Aufraeumer meldet
# in die Einheit, in der er gerufen wird. Taete er das hier, zaehlte sein absichtlich
# herbeigefuehrter Ausfall als Abweichung des Laufs - die Selbstprobe erzeugte den Befund,
# den sie misst.

def _mit_zeuge(zeuge, tun) -> None:
    """`tun` so ausfuehren, dass alle Meldungen in `zeuge` landen, nicht im Lauf."""
    eigene = _ORT.einheit
    _ORT.einheit = zeuge
    try:
        tun()
    finally:
        _ORT.einheit = eigene


def _zeuge(nummer: str):
    return Einheit("SELBSTPROBE", nummer,
                   "Hilfseinheit der Selbstprobe %s - sie wird nie angemeldet und "
                   "erscheint in keinem Lauf" % nummer, lambda: None)


def _festhalten(ziel: str):
    """Ein Arbeitsverzeichnis gegen das Loeschen sperren - je Betriebssystem anders.

    Unter Windows genuegt eine offene Datei darin: das Entfernen scheitert mit
    WinError 32. Unter POSIX nicht - dort haengt das Loeschen einer Datei am
    Schreibrecht ihres VERZEICHNISSES, also wird dieses entzogen. **Ohne diese
    Unterscheidung waere die Selbstprobe auf einem der beiden Systeme eine Zeile, die
    nichts misst** - und genau dagegen ist sie gebaut.
    """
    innen = os.path.join(ziel, "unterordner")
    os.makedirs(innen)
    pfad = os.path.join(innen, "gehalten.txt")
    schreib(pfad, "Diese Datei haelt ihr Verzeichnis fest.\r\n")
    if os.name == "nt":
        return io.open(pfad, "r+", encoding="utf-8")
    os.chmod(innen, 0o500)
    return innen


def _loslassen(halter) -> None:
    if hasattr(halter, "close"):
        halter.close()
    else:
        os.chmod(halter, 0o700)


def selbstprobe_aufraeumer() -> None:
    """Der Aufraeumer schweigt, wenn er seine Arbeit tut, und meldet, wenn nicht."""
    ziel = tempfile.mkdtemp(prefix="lw-auf-")
    schreib(os.path.join(ziel, "datei.txt"), "Sondendatei\r\n")
    zeuge = _zeuge("A1")
    _mit_zeuge(zeuge, lambda: aufraeumen(ziel))
    melde("SELBSTPROBE", "A1", not os.path.isdir(ziel) and not zeuge.zeilen,
          "Ein geloeschtes Arbeitsverzeichnis erzeugt keine Zeile - der Aufraeumer "
          "schweigt, wenn er seine Arbeit tut")

    # --- A3: der Schreibschutz, und er ist kein gedachter Fall -----------------------
    # Gemessen am 2026-09-15: git schreibt seine Objektdateien schreibgeschuetzt, und
    # drei Versuche ueber anderthalb Sekunden endeten dreimal mit demselben
    # "Zugriff verweigert". Warten hilft dagegen nicht.
    #
    # Unter POSIX blockiert eine schreibgeschuetzte DATEI das Loeschen nicht - dort
    # haengt es am Schreibrecht ihres Verzeichnisses. Die Probe gilt trotzdem auf
    # beiden Systemen, nur aus verschiedenen Gruenden: Unter Windows belegt sie den
    # Mechanismus, unter POSIX, dass er nichts kaputt macht. **Wer ihn unter Windows
    # entfernt, macht sie rot** - und das ist ihr Zweck.
    ziel = tempfile.mkdtemp(prefix="lw-auf-")
    pfad = os.path.join(ziel, "schreibgeschuetzt.txt")
    schreib(pfad, "Diese Datei ist schreibgeschuetzt.\r\n")
    os.chmod(pfad, stat.S_IREAD)
    zeuge = _zeuge("A3")
    _mit_zeuge(zeuge, lambda: aufraeumen(ziel))
    melde("SELBSTPROBE", "A3", not os.path.isdir(ziel) and not zeuge.zeilen,
          "Eine schreibgeschuetzte Datei haelt das Arbeitsverzeichnis nicht fest - der "
          "Aufraeumer nimmt den Schutz weg und schweigt")
    if os.path.isdir(ziel):
        notiz("        Gesammelt wurde:", " | ".join(zeuge.zeilen) or "nichts")
        schreibschutz_loesen(ziel)
        shutil.rmtree(ziel, ignore_errors=True)

    ziel = tempfile.mkdtemp(prefix="lw-auf-")
    halter = _festhalten(ziel)
    try:
        zeuge = _zeuge("A2")
        _mit_zeuge(zeuge, lambda: aufraeumen(ziel))
        gemeldet = zeuge.fehler == 1 and any("bleibt liegen" in z for z in zeuge.zeilen)
        genannt = any(ziel in z for z in zeuge.zeilen)
        ok = os.path.isdir(ziel) and gemeldet and genannt
        melde("SELBSTPROBE", "A2", ok,
              "Ein Verzeichnis, das sich nicht loeschen laesst, wird mit Pfad und Grund "
              "gemeldet und zaehlt als Abweichung")
        if not ok:
            notiz("        Gesammelt wurde:", " | ".join(zeuge.zeilen) or "nichts")
    finally:
        _loslassen(halter)
        aufraeumen(ziel)


buendel(selbstprobe_aufraeumer,
        "Der Aufraeumer schweigt beim Gelingen und meldet sein Scheitern mit Pfad und "
        "Grund - gemessen an einem Verzeichnis, das sich nicht loeschen laesst")


# --- 37: Die drei Koerbe der Berechtigungsdatei gegen die Kernquelle (D-77) --------
#
# GEGEN EINE ECHTE INSTALLATION, aus demselben Grund wie bei Pruefung 33: Der Gegenstand
# ist eine installierte Datei, nicht ein Text des Repositoriums. Eine Sonde auf einer
# Kopie des Repositoriums traefe die Testinstallation des Packs devin-desktop und damit
# nur eine der beiden Abbildungen - und der Praefixteil der Pruefung hat dort seinen
# Gegenstand gar nicht (permission_exec_match: literal).
#
# Anlass sind zwoelf Messungen vom 2026-09-13 (CR-2026-061): Acht Eingriffe in die Datei
# liefen gegen 0.38.0 ohne eine einzige Meldung durch, darunter das Loeschen ALLER 41
# Nicht-Kernregeln des deny-Korbs.
#
# Die erste Gegenprobe ist hier die wichtigere Haelfte, und zwar in zwei Zuschnitten:
# im Auslieferungszustand mit offenen Platzhaltern und mit ordentlich gefuellten. Eine
# Pruefung, die jede gefuellte Datei beanstandet, bestuende jede Sonde.
def _p37(root: str) -> str:
    return os.path.join(root, ".claude", "settings.json")


def _37_korb(daten: dict, korb: str) -> list:
    return daten.setdefault("permissions", {}).setdefault(korb, [])


def _37_weg(daten: dict, korb: str, regel: str) -> None:
    """Eine Regel entfernen - sie muss vorher dastehen."""
    regeln = _37_korb(daten, korb)
    if regel not in regeln:
        raise Praeparationsfehler(
            "settings.json: %r steht nicht im %s-Korb; die Sonde hat ihren Gegenstand "
            "verloren" % (regel, korb))
    regeln.remove(regel)


def _37_dazu(daten: dict, korb: str, regel: str) -> None:
    """Eine Regel ergaenzen - sie darf vorher nicht dastehen, sonst misst die Sonde nichts."""
    regeln = _37_korb(daten, korb)
    if regel in regeln:
        raise Praeparationsfehler(
            "settings.json: %r steht bereits im %s-Korb; die Sonde praepariert nichts"
            % (regel, korb))
    regeln.append(regel)


def _37_statt(daten: dict, korb: str, alt: str, neu: str) -> None:
    regeln = _37_korb(daten, korb)
    if alt not in regeln:
        raise Praeparationsfehler(
            "settings.json: %r steht nicht im %s-Korb; die Sonde hat ihren Gegenstand "
            "verloren" % (alt, korb))
    regeln[regeln.index(alt)] = neu


def _37_schreiben(root: str, *aenderungen) -> None:
    """Die Eingriffe anwenden und die Datei schreiben.

    Der Praeparationswaechter sitzt in den Eingriffen selbst (_37_weg, _37_dazu,
    _37_statt): Sie pruefen ihren Gegenstand, statt ihn vorauszusetzen. Ein Textvergleich
    vorher/nachher taugte hier nicht - json.dumps normalisiert die Datei ohnehin, und der
    Waechter meldete dann immer "veraendert" (D-74).
    """
    pfad = _p37(root)
    daten = json.loads(lies(pfad))
    for aenderung in aenderungen:
        aenderung(daten)
    schreib(pfad, json.dumps(daten, indent=2, ensure_ascii=False) + "\n")


MELDUNG_FEHLT = "die Kernquelle erzeugt f\u00fcr den"
MELDUNG_ZUVIEL = "die die Kernquelle nicht erzeugt"
MELDUNG_PRAEFIX = "tr\u00e4gt das Pr\u00e4fixzeichen"


def sonden_berechtigungskoerbe() -> None:
    """Wirkungsnachweis zu Pruefung 37 (CR-2026-061, D-76 und D-77)."""
    root = installation("claude-code")
    try:
        pfad = _p37(root)
        ausgang = lies(pfad)
        # README.md ist Pflichtpfad; ohne sie meldet jeder Lauf zwei Fehler, die mit
        # dieser Pruefung nichts zu tun haben.
        schreib(os.path.join(root, "README.md"), "# Sondenprojekt\r\n")

        # --- Gegenprobe 37a: der Auslieferungszustand bleibt unbeanstandet ----------
        aus = validator_ausgabe(root)
        ok = (MELDUNG_FEHLT not in aus and MELDUNG_ZUVIEL not in aus
              and MELDUNG_PRAEFIX not in aus)
        melde("GEGENPROBE", "37a", ok,
              "Auslieferungszustand mit offenen Platzhaltern - ein Schlitz ist ein Schlitz")
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "settings.json" in z)[:400])

        # --- Gegenprobe 37b: ordentlich gefuellte Platzhalter bleiben unbeanstandet -
        # Ohne sie stuende nur fest, dass die Pruefung irgendetwas meldet - und eine
        # Pruefung, die jede gefuellte Datei beanstandet, bestuende jede Sonde.
        _37_schreiben(root,
                      lambda d: _37_statt(d, "ask", "Bash(<BUILD_COMMAND>)",
                                          "Bash(mvn -B clean package)"),
                      lambda d: _37_statt(d, "ask", "Bash(<TEST_COMMAND>)",
                                          "Bash(mvn -B test)"),
                      lambda d: _37_statt(d, "ask", "Bash(<LINT_COMMAND>)",
                                          "Bash(mvn -B verify)"))
        aus = validator_ausgabe(root)
        ok = (MELDUNG_FEHLT not in aus and MELDUNG_ZUVIEL not in aus
              and MELDUNG_PRAEFIX not in aus)
        melde("GEGENPROBE", "37b", ok,
              "Drei gefuellte Befehlsschlitze ohne Praefixzeichen - der Normalfall")
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "settings.json" in z)[:400])
        schreib(pfad, ausgang)

        # --- 37a: eine NICHT-Kernregel aus deny geloescht ---------------------------
        # 41 der 54 deny-Regeln standen bis 0.38.0 ausserhalb jeder Pruefung.
        _37_schreiben(root, lambda d: _37_weg(d, "deny", "Bash(curl:*)"))
        aus = validator_ausgabe(root)
        melde("SONDE", "37a", MELDUNG_FEHLT in aus,
              "Geloeschte Nicht-Kernregel im deny-Korb - bis 0.38.0 stumm")
        schreib(pfad, ausgang)

        # --- 37b: eine Nicht-Kernregel VERENGT --------------------------------------
        # Die stillste Form: Sie sieht aus wie eine Regel und sperrt weniger.
        _37_schreiben(root, lambda d: _37_statt(d, "deny", "Bash(kubectl:*)",
                                                "Bash(kubectl delete:*)"))
        aus = validator_ausgabe(root)
        melde("SONDE", "37b", MELDUNG_FEHLT in aus,
              "Verengte Nicht-Kernregel - kubectl apply liefe wieder")
        schreib(pfad, ausgang)

        # --- 37c: eine Zeile im ask-Korb ergaenzt -----------------------------------
        # Der Fall CR-OTP-G-001: Die Zeile erklaert einen Befehl fuer freigegeben.
        _37_schreiben(root, lambda d: _37_dazu(
            d, "ask", "Bash(docker run --rm --network none:*)"))
        aus = validator_ausgabe(root)
        melde("SONDE", "37c", MELDUNG_ZUVIEL in aus,
              "Ergaenzte ask-Zeile - der Antrag CR-OTP-G-001 des Piloten")
        schreib(pfad, ausgang)

        # --- 37d: eine Zeile im allow-Korb ergaenzt ---------------------------------
        _37_schreiben(root, lambda d: _37_dazu(d, "allow", "Bash(docker run:*)"))
        aus = validator_ausgabe(root)
        melde("SONDE", "37d", MELDUNG_ZUVIEL in aus,
              "Ergaenzte allow-Zeile - kein Abrufwerkzeug, nicht auf der Verbotsliste")
        schreib(pfad, ausgang)

        # --- 37e: der ask-Korb geleert ----------------------------------------------
        _37_schreiben(root, lambda d: d["permissions"].__setitem__("ask", []))
        aus = validator_ausgabe(root)
        melde("SONDE", "37e", MELDUNG_FEHLT in aus,
              "Geleerter ask-Korb - Edit(**) und mcp__* verschwinden mit")
        schreib(pfad, ausgang)

        # --- 37f: ein Befehlsschlitz mit Praefixzeichen gefuellt --------------------
        # Am Piloten am 2026-09-13 so vorgefunden: Bash(mvn -B test:*).
        _37_schreiben(root, lambda d: _37_statt(d, "ask", "Bash(<TEST_COMMAND>)",
                                                "Bash(mvn -B test:*)"))
        aus = validator_ausgabe(root)
        melde("SONDE", "37f", MELDUNG_PRAEFIX in aus,
              "Befehlsschlitz mit Praefixzeichen gefuellt - der Fall des Piloten")
        schreib(pfad, ausgang)

        # --- 37h und Gegenprobe 37c: die Skillfreigabe eines aktivierten Packs ----
        #
        # 🔴 ZWEI PRUEFUNGEN DESSELBEN REPOSITORIUMS STANDEN GEGENEINANDER
        # (2026-09-21, D-243). Pruefung 72 verlangt seit `0.81.0` zu jedem Skill der
        # Installation einen Korbeintrag - der dritte Teil der Aktivierung eines
        # Packs (D-238). Pruefung 37 hielt genau diesen Eintrag fuer eine Ausweitung,
        # weil die Kernquelle ihn nicht erzeugt. Damit war D-238 in keinem Projekt
        # umsetzbar, ohne den eigenen Validator rot zu faerben.
        #
        # Das PAAR belegt den Zuschnitt: Ein Eintrag auf einen Skill, der in der
        # Ablage liegt, ist keine Ausweitung; derselbe Eintrag auf einen Namen ohne
        # Skill bleibt einer.
        skillablage = os.path.join(root, ".claude", "skills")
        quelle = os.path.join(root, ".koolie/core", "framework", "role-packs",
                              "requirements-engineering", "skills", "koolie-ticket")
        shutil.copytree(quelle, os.path.join(skillablage, "koolie-ticket"))
        _37_schreiben(root, lambda d: _37_dazu(d, "allow", "Skill(koolie-ticket)"))
        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "37c", MELDUNG_ZUVIEL not in aus,
              "Vollstaendig aktiviertes Role Pack - Skill in der Ablage UND im Korb, "
              "und Pruefung 37 schweigt dazu")
        if MELDUNG_ZUVIEL in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "settings.json" in z)[:400])
        schreib(pfad, ausgang)

        _37_schreiben(root, lambda d: _37_dazu(d, "allow", "Skill(role-gibt-es-nicht)"))
        aus = validator_ausgabe(root)
        melde("SONDE", "37h", MELDUNG_ZUVIEL in aus,
              "Dieselbe Schreibweise auf einen Namen ohne Skill in der Ablage bleibt "
              "eine Ausweitung - der Zuschnitt haengt an der Ablage, nicht am Wort")
        schreib(pfad, ausgang)
        shutil.rmtree(os.path.join(skillablage, "koolie-ticket"))

        # --- 37g: der verlorene Anker ----------------------------------------------
        cm = os.path.join(root, ".koolie/core", "clientmap.py")
        quelle = lies(cm)
        schreib(cm, ersetzt(quelle, ("def basket_rules(", "def korb_regeln("),
                            quelle="clientmap.py"))
        aus = validator_ausgabe(root)
        melde("SONDE", "37g", "'basket_rules(' fehlt" in aus,
              "Verlorener Anker - die Pruefung meldet ihr Fehlen selbst")
        schreib(cm, quelle)
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_berechtigungskoerbe,
        "Neun Eingriffe in die Berechtigungsdatei einer echten Installation, jeder einzeln "
        "zurueckgesetzt: geloeschte, verengte und ergaenzte Regeln, geleerter ask-Korb, "
        "Praefixzeichen und die Skillfreigabe eines aktivierten Packs")

# --- 38: Eine Quelle, ein Vokabular, eine Richtung (CR-2026-062, D-78 bis D-80) ----
#
# Auf einer Kopie des Repositoriums, nicht gegen eine Installation: Der Gegenstand von
# Pruefung 38 sind die Manifeste und die Quellen des Kerns, nicht eine erzeugte Datei.
# Das ist der Unterschied zu den Pruefungen 33 und 37.
#
# Acht Sonden, zwei Gegenproben. Die Sonden 38f und 38g treffen die beiden Stellen, an
# denen der Fall bis 0.39.0 STILL war: in allowed-tools wurde das unbekannte Verb
# woertlich als Werkzeugname durchgereicht, in permissions.deny fiel es lautlos aus.
MANIFEST_CC_38 = ".koolie/core/clients/claude-code/manifest.json"
MANIFEST_DD_38 = ".koolie/core/clients/devin-desktop/manifest.json"
SKILL_38 = ".koolie/core/framework/skills/koolie-plan/SKILL.md"
CLIENTMAP_38 = ".koolie/core/clientmap.py"


def _38_json(root: str, rel: str, wandler) -> None:
    """Ein Manifest ueber das JSON praeparieren, nicht ueber den Text.

    Die beiden tool_names-Bloecke eines Manifests sind ZEICHENGLEICH; ein Textanker
    traefe den falschen. Dieselbe Begruendung wie bei Sonde 35a.
    """
    pfad = P(root, rel.replace("/", os.sep))
    daten = json.loads(lies(pfad))
    wandler(daten)
    schreib(pfad, json.dumps(daten, ensure_ascii=False, indent=2) + "\r\n")


def _38_deklaration_weg(root: str) -> None:
    """Ein Verb faellt aus der Abbildung, ohne dass es erklaert wird.

    Bis 0.42.0 hat diese Sonde die ERKLAERUNG entfernt; seit die Abbildung von
    devin-desktop erhoben ist (D-87), gibt es keine mehr zu entfernen. Der Defekt ist
    derselbe geblieben - er wird jetzt hergestellt statt abgeraeumt.
    """
    _38_json(root, MANIFEST_DD_38,
             lambda d: d["skill_frontmatter"]["tool_names"].pop("read"))


def _38_notiz_weg(root: str) -> None:
    """Eine erklaerte Nichtabbildung ohne Begruendung - eine Behauptung.

    Ebenfalls hergestellt statt abgeraeumt: Das Verb verliert seine Abbildung und
    bekommt die Erklaerung, aber keine Notiz.
    """
    def _um(d):
        fmt = d["agent_frontmatter"]
        fmt["tool_names"].pop("read")
        fmt["tool_names_unmapped"] = ["read"]
        fmt.pop("_tool_names_unmapped_note", None)
    _38_json(root, MANIFEST_DD_38, _um)


def _38_beides_zugleich(root: str) -> None:
    _38_json(root, MANIFEST_CC_38,
             lambda d: d["skill_frontmatter"].__setitem__("tool_names_unmapped", ["grep"]))


def _38_fremder_schluessel(root: str) -> None:
    """Ein Verb der Durchsetzungsschicht in der Abbildung der Quelle."""
    _38_json(root, MANIFEST_CC_38,
             lambda d: d["agent_frontmatter"]["tool_names"].__setitem__("search", ["Grep"]))


def _38_richtung_verdreht(root: str) -> None:
    """Die Sperrliste wird enger als die Vorabfreigabe - der gefaehrliche Fall."""
    _38_json(root, MANIFEST_CC_38,
             lambda d: d["hook_tools"].__setitem__("write", ["Edit", "NotebookEdit"]))


def _38_quelle_allowed(root: str) -> None:
    ersetze(P(root, SKILL_38.replace("/", os.sep)),
            ("allowed-tools:\r\n  - read\r\n", "allowed-tools:\r\n  - search\r\n"))


def _38_quelle_deny(root: str) -> None:
    ersetze(P(root, SKILL_38.replace("/", os.sep)),
            ("  deny:\r\n    - edit\r\n", "  deny:\r\n    - write\r\n"))


def _38_anker_weg(root: str) -> None:
    """Der Fall, in dem die Pruefung leise bestuende: Das Vokabular verliert seinen Namen."""
    ersetze(P(root, CLIENTMAP_38.replace("/", os.sep)),
            ("FRONTMATTER_VERBEN = (", "FRONTMATTER_VERBEN_ALT = ("))


def _38_quellen_weg(root: str) -> None:
    """Der zweite Anker: ohne Quelldateien prueft der vierte Gegenstand nichts."""
    for rel in (".koolie/core/framework/skills",
                ".koolie/core/framework/role-packs",
                ".koolie/core/framework/runtime/agents"):
        shutil.rmtree(P(root, rel.replace("/", os.sep)), ignore_errors=True)


def _38_engere_vorabfreigabe(root: str) -> None:
    """Die ZULAESSIGE Richtung: die Vorabfreigabe wird enger als die Sperre."""
    _38_json(root, MANIFEST_CC_38,
             lambda d: d["skill_frontmatter"]["tool_names"].__setitem__("edit", ["Edit"]))


sonde("38a", "Ein Verb weder abgebildet noch erklaert - der Stand bis 0.39.0",
      _38_deklaration_weg, "kennt das Werkzeugverb 'read' nicht, und tool_names_unmapped")

sonde("38b", "Erklaerte Nichtabbildung ohne Begruendung - eine Behauptung",
      _38_notiz_weg, "'_tool_names_unmapped_note' fehlt")

sonde("38c", "Abgebildet und zugleich fuer nicht abgebildet erklaert",
      _38_beides_zugleich, "Beides zugleich geht nicht")

sonde("38d", "Ein Verb der Durchsetzungsschicht in der Abbildung der Quelle",
      _38_fremder_schluessel, "kein Verb des Frontmatter-Vokabulars")

sonde("38e", "Die Sperrliste wird enger als die Vorabfreigabe - der gefaehrliche Fall",
      _38_richtung_verdreht, "enger als die Vorabfreigabe")

sonde("38f", "Eine Quelle nennt in allowed-tools ein fremdes Verb - bis 0.39.0 wurde "
      "es woertlich als Werkzeugname durchgereicht",
      _38_quelle_allowed, "allowed-tools nennt das Verb 'search'")

sonde("38g", "Eine Quelle nennt in permissions.deny ein fremdes Verb - bis 0.39.0 "
      "fiel die Sperre lautlos aus",
      _38_quelle_deny, "permissions.deny nennt das Verb 'write'")

sonde("38h", "Verlorener Anker - das Vokabular verliert seinen Namen",
      _38_anker_weg, "Pruefung 38 hat ihren Anker verloren")

sonde("38i", "Verlorener Anker - keine Quelle mit Frontmatter mehr",
      _38_quellen_weg, "keine Quelle mit Frontmatter gefunden")

gegenprobe("38a", "Die unveraenderten Packs bleiben unbeanstandet - eines bildet ab, "
           "eines erklaert", None, "Vokabular")

gegenprobe("38b", "Eine Vorabfreigabe, die ENGER ist als die Sperre, bleibt "
           "unbeanstandet - die zulaessige Richtung",
           _38_engere_vorabfreigabe, "enger als die Vorabfreigabe")


# --- 39: Die Vorabfreigabe des Skillaufrufs und die vier Regeltraeger (D-81 bis D-84) -
#
# Anlass: Die Wurzel-Anweisungsdatei forderte die Nutzung der Skills, und die
# ausgelieferte Berechtigungsdatei kannte das Werkzeug dafuer in keinem Korb. Gemessen
# am 2026-09-14: Der Aufruf wurde abgewiesen, die Sitzung las die SKILL.md ersatzweise
# als Datei, und die Ausgabe sah aus wie ein gelungener Lauf.
#
# Pruefung 39 faengt im Repositorium heute NICHTS - Regeln, Skillmenge und Traegertexte
# sind mit demselben Release entstanden und passen per Konstruktion zueinander. Was sie
# wert ist, haengt allein an diesen Sonden. Dieselbe Lage wie bei Pruefung 37, und sie
# ist im Wirkungsnachweis so ausgewiesen.
#
# Die zweite Gegenprobe ist die wichtigere: Gegenstand 3 beanstandet ein Musterzeichen -
# und die Datei fuehrt daneben Pfadregeln, die eines tragen MUESSEN ('**'). Eine
# Musterpruefung ohne diese Unterscheidung beanstandete den richtigen Text.
PERMS_39 = ".koolie/core/framework/runtime/permissions.json"


def _p39(root: str) -> str:
    return P(root, PERMS_39.replace("/", os.sep))


def _39_regel_fehlt(root: str) -> None:
    """Ein ausgelieferter Skill verliert seine Freigabe - der Zustand vor 0.41.0."""
    ersetze(_p39(root),
            ('    { "tool": "skill",  "pattern": "koolie-code-explain" },\r\n', ""))


def _39_regel_ohne_skill(root: str) -> None:
    """Eine Freigabe fuer einen Skill, den es nicht gibt."""
    ersetze(_p39(root),
            ('"pattern": "koolie-code-explain" }', '"pattern": "koolie-code-erklaeren" }'))


def _39_muster(root: str) -> None:
    """Das Praefixmuster, das gemessen nichts freigibt (D-82)."""
    ersetze(_p39(root),
            ('"pattern": "koolie-code-explain" }', '"pattern": "koolie-*" }'))


def _39_anker_weg(root: str) -> None:
    """Keine einzige skill-Regel mehr - die Pruefung darf nicht leise bestehen."""
    text = lies(_p39(root))
    zeilen = [z for z in text.split("\r\n") if '"tool": "skill"' not in z]
    if len(zeilen) == len(text.split("\r\n")):
        raise Praeparationsfehler(
            "permissions.json: keine skill-Regel gefunden, die zu entfernen waere")
    # Das Komma der letzten verbleibenden Regel muss weg, sonst ist die Datei kein JSON.
    # Das Komma der letzten verbleibenden Regel vor der schliessenden Klammer muss weg -
    # abgeleitet, nicht an einem Regelnamen: Seit 1.17.0 steht dort nicht mehr git blame.
    schreib(_p39(root), re.sub(r"\},(\s*\r\n\s*\])", r"}\1", "\r\n".join(zeilen)))


def _39_traeger_weg(root: str) -> None:
    """Ein Regeltraeger verliert die Skillwahl - der Zustand vor 0.41.0."""
    ersetze(P(root, ".koolie/core/framework/runtime/rules/00-framework-core.md"
              .replace("/", os.sep)),
            ("**Skillwahl vor dem Schritt.**", "**Hinweis zur Reihenfolge.**"))


def _39_skill_ohne_regel(root: str) -> None:
    """Ein neuer Skill im Verzeichnis, ohne dass jemand die Freigabe nachtraegt."""
    quelle = P(root, ".koolie/core/framework/skills/koolie-code-explain"
               .replace("/", os.sep))
    ziel = P(root, ".koolie/core/framework/skills/koolie-zwischenstand"
             .replace("/", os.sep))
    shutil.copytree(quelle, ziel)


def _39_pfadmuster_bleibt(root: str) -> None:
    """Gegenprobe: Eine Pfadregel MUSS ein Muster tragen - '**' ist richtig so."""
    ersetze(_p39(root),
            ('    { "tool": "read",   "pattern": "**" },\r\n',
             '    { "tool": "read",   "pattern": "**" },\r\n'
             '    { "tool": "search", "pattern": "src/**" },\r\n'))


sonde("39a", "Ein ausgelieferter Skill ohne Freigabe - der Zustand vor 0.41.0",
      _39_regel_fehlt, "hat keine allow-Regel")

sonde("39b", "Eine Freigabe fuer einen Skill, den es nicht gibt",
      _39_regel_ohne_skill, "nennt keinen ausgelieferten Skill")

sonde("39c", "Ein Praefixmuster in der Freigabe - es gaebe lautlos nichts frei (D-82)",
      _39_muster, "traegt ein Musterzeichen")

sonde("39d", "Verlorener Anker - keine einzige skill-Regel mehr",
      _39_anker_weg, "keine einzige allow-Regel mit dem Verb 'skill'")

sonde("39e", "Ein Regeltraeger verliert die Skillwahl",
      _39_traeger_weg, "die Skillwahl fehlt")

sonde("39f", "Ein neuer Skill, dessen Freigabe niemand nachtraegt",
      _39_skill_ohne_regel, "'koolie-zwischenstand' hat keine allow-Regel")

gegenprobe("39a", "Die unveraenderte Datei bleibt unbeanstandet - zwoelf Regeln, zwoelf "
           "Skills", None, "allow-Regel")

gegenprobe("39b", "Eine PFADregel mit Muster bleibt unbeanstandet - Gegenstand 3 misst "
           "nur die skill-Regeln", _39_pfadmuster_bleibt, "Musterzeichen")



# --- 40: Die Register des Pruefapparats (D-85, D-86) ---------------------------------
#
# Anlass: Fuenf Aussagen ueber den eigenen Pruefstand, keine davon richtig - und keine
# falsch geschrieben. Alle fuenf waren bei ihrer Einfuehrung richtig und sind stehen
# geblieben, waehrend ihr Gegenstand wuchs; die aelteste seit zwoelf Releases.
#
# Diese Sonden sind der Grund, warum die Pruefung mehr ist als eine Textaenderung: Sie
# belegen, dass das Vergessen gefangen wird, nicht nur das einmalige Nachziehen.
#
# Die zweite Gegenprobe ist die wichtigere. Der erste Entwurf dieser Pruefung hat einen
# Querverweis im Fliesstext eines Kommentars fuer einen Kopf gehalten und Pruefung 37
# dort gefunden, wo kein Kopf steht. Seither ankert sie an der hoechsten genannten
# Nummer statt an einer Kommentarform - und diese Gegenprobe haelt genau das fest.
VAL_40 = ".koolie/core/tests/scripts/validate-framework.py"
KAT_40 = ".koolie/core/tests/TEST_CATALOG.md"

REGISTER_KOPF = "Prüft (statisch, ohne laufenden KI-Client):"
NACHWEIS_ANFANG = "Der Wirksamkeitsnachweis nach D-23 fuer die Pruefungen "


def _zeilenblock(*zeilen: str) -> str:
    """Ein Block des Registers als CRLF-Text - der Kopfkommentar ist CRLF wie die Datei."""
    return "".join(z + "\r\n" for z in zeilen)


EINTRAG_25 = _zeilenblock(
    " 25. Ausfall mit Ersatz (D-41): Eine Matrixzeile eines Client Packs auf "
    "[NICHT ABBILDBAR]",
    "     benennt den Ersatz - oder haelt ausdruecklich fest, dass es keinen gibt")


def _p40v(root: str) -> str:
    return P(root, VAL_40.replace("/", os.sep))


def _p40k(root: str) -> str:
    return P(root, KAT_40.replace("/", os.sep))


def _40_registerblock(text: str):
    """Der LETZTE nummerierte Registereintrag: (anfang, zeilen, i, j, nummer).

    Abgeleitet statt verdrahtet. Die erste Fassung dieser Sonden trug die Nummer des
    eigenen Releases im Suchtext und fiel mit der naechsten Pruefung: 40a meldete eine
    Luecke statt des fehlenden letzten Eintrags, 40c ergaenzte eine Nummer, die es
    inzwischen wirklich gibt. Eine Sonde, die ihre Grenze selbst ausrechnet, ueberlebt
    das Release, das sie pruefen soll.
    """
    a = text.index(REGISTER_KOPF)
    b = text.index(NACHWEIS_ANFANG, a)
    zeilen = text[a:b].split("\r\n")
    starts = [i for i, z in enumerate(zeilen) if re.match(r"^ ?\d+\. ", z)]
    if not starts:
        raise Praeparationsfehler(
            "validate-framework.py: kein nummerierter Registereintrag gefunden")
    i = starts[-1]
    j = i + 1
    while j < len(zeilen) and zeilen[j].startswith("     "):
        j += 1
    return a, b, zeilen, i, j, int(zeilen[i].split(".", 1)[0].strip())


def _40_eintrag_fehlt(root: str) -> None:
    """Der Zustand vom 2026-09-14: Eine Pruefung laeuft, das Register kennt sie nicht."""
    pfad = _p40v(root)
    text = lies(pfad)
    a, b, zeilen, i, j, _nr = _40_registerblock(text)
    schreib(pfad, text[:a] + "\r\n".join(zeilen[:i] + zeilen[j:]) + text[b:])


def _40_luecke(root: str) -> None:
    """Eine Nummer faellt aus dem Register - die Pruefung dahinter findet niemand."""
    ersetze(_p40v(root), (EINTRAG_25, ""))


def _40_eintrag_ohne_pruefung(root: str) -> None:
    """Ein Eintrag ohne Pruefung dahinter - die Gegenrichtung von 40a."""
    pfad = _p40v(root)
    text = lies(pfad)
    a, b, zeilen, _i, j, nummer = _40_registerblock(text)
    zusatz = [" %d. Eine Zeile, der keine Pruefung entspricht - sie verspricht mehr,"
              % (nummer + 1),
              "     als der Lauf leistet"]
    schreib(pfad, text[:a] + "\r\n".join(zeilen[:j] + zusatz + zeilen[j:]) + text[b:])


def _40_spanne_verdreht(root: str) -> None:
    """Die Sondenmenge im Satz unter dem Register weicht ab - der Stand von 0.32.0.

    Die Spanne wird gesucht, nicht genannt: Sie waechst mit jedem Release.
    """
    pfad = _p40v(root)
    text = lies(pfad)
    neu, treffer = re.subn(r"(" + re.escape(NACHWEIS_ANFANG) + r")[^\r\n]*?( laeuft)",
                           r"\g<1>18 bis 30\g<2>", text, count=1)
    if treffer != 1:
        raise Praeparationsfehler(
            "validate-framework.py: Satz zum Wirkungsnachweis nicht gefunden")
    schreib(pfad, neu)


def _40_grenzfallzahl(root: str) -> None:
    """FW-KO-05 nennt eine Zahl, die nicht mehr stimmt - der Stand bis 0.41.0."""
    ersetze(_p40k(root),
            ("Die 20 Grenzfälle einzeln", "Die zwölf Grenzfälle einzeln"))


def _40_anker_weg(root: str) -> None:
    """Die Registerueberschrift verschwindet - die Pruefung darf nicht leise bestehen."""
    ersetze(_p40v(root),
            ("Prüft (statisch, ohne laufenden KI-Client):\r\n  1. Pflichtdateien",
             "Geprüft wird unter anderem:\r\n  1. Pflichtdateien"))


def _40_querverweis(root: str) -> None:
    """Gegenprobe: Ein Querverweis auf eine kleinere Nummer ist kein Registereintrag.

    Genau diese Zeilenform hat den ersten Entwurf der Pruefung fallen lassen.
    """
    ersetze(_p40v(root),
            ("def main() -> int:\r\n",
             "# Pruefung 37 und dieselbe Ehrlichkeit wie Pruefung 30: ein Querverweis im\r\n"
             "# Fliesstext, kein Kopf - er darf das Register nicht bewegen.\r\n"
             "def main() -> int:\r\n"))


sonde("40a", "Eine Pruefung laeuft, das Register kennt sie nicht - der Fall vom "
      "2026-09-14", _40_eintrag_fehlt, "die Prüfskripte nennen Prüfung")

sonde("40b", "Eine Nummer faellt aus dem Register - die Pruefung dahinter findet "
      "niemand", _40_luecke, "hat Lücken – es fehlt 25")

sonde("40c", "Ein Registereintrag ohne Pruefung dahinter - die Gegenrichtung",
      _40_eintrag_ohne_pruefung, "Ein Eintrag ohne Prüfung verspricht mehr")

sonde("40d", "Die Sondenmenge im Satz unter dem Register weicht ab",
      _40_spanne_verdreht,
      "validate-framework.py: die Sondenmenge ist dort nicht in der ausgerechneten")

sonde("40e", "FW-KO-05 nennt eine Grenzfallzahl, die nicht mehr stimmt",
      _40_grenzfallzahl, "FW-KO-05 nennt nicht die gezählte Anzahl")

sonde("40f", "Verlorener Anker - die Registerueberschrift verschwindet",
      _40_anker_weg, "Prüfung 40 hat ihren Gegenstand verloren")

gegenprobe("40a", "Das unveraenderte Repositorium bleibt unbeanstandet - Register, "
           "Sondenmenge und Grenzfallzahl decken sich", None,
           "das Register im Kopfkommentar")

gegenprobe("40b", "Ein Querverweis auf eine kleinere Pruefungsnummer bleibt "
           "unbeanstandet - er ist kein Kopf und kein Eintrag",
           _40_querverweis, "die Prüfskripte nennen Prüfung")


# --- 41: Abwesenheitsbeleg, und 38 mit eigenem Namensraum (D-88) ----------------------
#
# Anlass: Eine Abwesenheitserklaerung nahm eine Werkzeugklasse aus der Durchsetzung und
# begruendete es - mit einem Satz, der weder Enthaltung noch Beleg war. Pruefung 26 hat
# ihn durchgelassen, weil sie Folgerichtigkeit prueft und nicht Wahrheit.
#
# Die zweite Gegenprobe ist die wichtigere: Eine Enthaltung braucht KEINEN Beleg. Wer das
# verwechselt, verlangt fuer eine ehrliche Wissenslucke ein Protokoll, das es nicht geben
# kann - und treibt damit genau die Behauptung hervor, gegen die die Pruefung gebaut ist.
MAN_DD = ".koolie/core/clients/devin-desktop/manifest.json"
MAN_CC = ".koolie/core/clients/claude-code/manifest.json"

# Der Anker zeigt auf den SCHLUESSEL, nicht auf seinen Wert: Der Wert hat sich mit
# 0.86.0 geaendert (von "UNERHOBEN, nicht abwesend" auf "ERHOBEN am 2026-09-22"), und
# eine Sonde, die am Wert haengt, verliert ihren Gegenstand beim naechsten Messwert.
NOTE_DD_START = '"_agent_start_tools_absent_note": '
NOTE_CC_FUND = ("tests/protocols/2026-09-13-erhebung-disallowed-tools.md "
                "Abschnitt 4.3")


def _41_behauptung(root: str) -> None:
    """Eine Abwesenheitserklaerung ohne Enthaltung und ohne Fundstelle - der Fall vom
    2026-09-14. Die Note traegt danach noch ein Datum, aber keinen Beleg."""
    t = lies(_p(root, MAN_DD))
    t = t.replace('"agent_start_tools_absent": [],',
                  '"agent_start_tools_absent": ["unerhoben"],', 1)
    anfang = t.index(NOTE_DD_START)
    ende = t.index('",', anfang)
    t = (t[:anfang] + '"_agent_start_tools_absent_note": "Dieser Client fuehrt kein '
         'Startwerkzeug fuer Unteragenten.' + t[ende:])
    schreib(_p(root, MAN_DD), t)


def _41_datum_ohne_fundstelle(root: str) -> None:
    """Ein Datum allein ist kein Beleg - die Fundstelle faellt weg."""
    ersetze(_p(root, MAN_CC), (NOTE_CC_FUND, "einer fruehreren Erhebung"))


def _41_gegenstand_weg(root: str) -> None:
    """Kein Pack fuehrt noch eine Abwesenheitserklaerung - die Pruefung meldet es selbst.

    DIE SONDE MUSS JEDES PACK TREFFEN, UND MIT DEM DRITTEN IST SIE DARAN GESCHEITERT
    (CR-2026-133). Sie nannte bis 1.3.0 zwei Packs beim Namen; `openai-codex` fuehrt
    gleich vier Abwesenheitserklaerungen, und der Anker war deshalb nicht verloren -
    die Sonde meldete FEHL, obwohl die Pruefung richtig gearbeitet hat.
      ➡️ Eine Sonde, die ihre Gegenstaende aufzaehlt, altert mit jedem neuen.
    Sie raeumt deshalb jetzt JEDES Manifest der Ablage, und zwar ueber die GESTALT der
    Schluessel (`*_absent`, `*_unmapped`) statt ueber ihre Namen.
    """
    def raeumen(obj):
        if isinstance(obj, dict):
            for k in [k for k in obj if k.endswith(("_absent", "_unmapped"))]:
                del obj[k]
            for v in obj.values():
                raeumen(v)
        elif isinstance(obj, list):
            for v in obj:
                raeumen(v)

    basis = _p(root, ".koolie/core/clients")
    treffer = 0
    for name in sorted(os.listdir(basis)):
        pfad = os.path.join(basis, name, "manifest.json")
        if not os.path.isfile(pfad):
            continue
        daten = json.loads(lies(pfad))
        raeumen(daten)
        schreib(pfad, json.dumps(daten, indent=2, ensure_ascii=False) + chr(10))
        treffer += 1
    if treffer < 2:
        raise Praeparationsfehler(
            "Sonde 41c: weniger als zwei Manifeste gefunden - die Sonde hat ihren "
            "Gegenstand verloren")


def _41_enthaltung_ohne_beleg(root: str) -> None:
    """Gegenprobe: Eine Enthaltung braucht keinen Beleg - sie ist selbst die Aussage."""
    text = lies(_p(root, MAN_CC))
    anfang = text.index('"_skill_deny_unmapped_note": "')
    ende = text.index('",', anfang)
    neu = ('"_skill_deny_unmapped_note": "Unerhoben: Ob dieser Client befehlsgenaue '
           'Verbote auswertet, ist nicht gemessen.')
    schreib(_p(root, MAN_CC), text[:anfang] + neu + text[ende:])


def _38_namensraum_ohne_notiz(root: str) -> None:
    """Ein eigener Namensraum nimmt die Richtungsregel ausser Kraft - ohne Begruendung."""
    text = lies(_p(root, MAN_DD))
    anfang = text.index('"_tool_names_note": "ERHOBEN am 2026-09-14')
    ende = text.index('",', anfang)
    schreib(_p(root, MAN_DD), text[:anfang] + '"_tool_names_note": "' + text[ende:])


def _38_namensraum_falsch(root: str) -> None:
    """Der Namensraum wird auf 'werkzeugnamen' gestellt - die Richtungsregel muss greifen."""
    ersetze(_p(root, MAN_DD),
            ('"tool_names_namespace": "eigen",', '"tool_names_namespace": "werkzeugnamen",', 2))


sonde("41a", "Abwesenheitserklaerung ohne Enthaltung und ohne Fundstelle - der Fall "
      "vom 2026-09-14", _41_behauptung,
      "weder als Enthaltung aus noch belegt sie sie")

sonde("41b", "Ein Datum allein ist kein Beleg", _41_datum_ohne_fundstelle,
      "weder als Enthaltung aus noch belegt sie sie")

sonde("41c", "Verlorener Gegenstand - kein Pack erklaert mehr eine Abwesenheit",
      _41_gegenstand_weg, "hat ihren Gegenstand verloren")

sonde("38j", "Eigener Namensraum ohne Begruendung - die Richtungsregel faellt "
      "unbegruendet weg", _38_namensraum_ohne_notiz,
      "tool_names_namespace ist 'eigen', aber")

sonde("38k", "Namensraum auf 'werkzeugnamen' gestellt - die Richtungsregel muss greifen",
      _38_namensraum_falsch, "Die Sperrliste ist damit enger als die Vorabfreigabe")

gegenprobe("41a", "Die unveraenderten Packs bleiben unbeanstandet - eine Enthaltung und "
           "ein Beleg", None, "weder als Enthaltung aus noch belegt sie sie")

gegenprobe("41b", "Eine Enthaltung ohne Datum und ohne Fundstelle bleibt unbeanstandet - "
           "sie ist selbst die Aussage", _41_enthaltung_ohne_beleg,
           "weder als Enthaltung aus noch belegt sie sie")

# --- 42: Ein gefuellter Schlitz traegt, was das Overlay erklaert ----------------------
#
# Gegen eine frische INSTALLATION beider Packs, nicht gegen eine Kopie des
# Repositoriums - der Gegenstand sind zwei installierte Dateien (das Overlay und die
# Berechtigungsdatei), nicht ein Repositoriumstext. Dieselbe Bauart wie bei den
# Pruefungen 33 und 37, und aus demselben Grund: Befund B02 trifft jede Pruefung, die
# an einer Installation haengt.
#
# Die Gegenproben sind hier die wichtigere Haelfte, in drei Zuschnitten: der
# Auslieferungszustand (Overlay dreimal <TBD>, Schlitze woertlich offen), das ordentlich
# ausgefuellte Projekt (drei erklaerte Befehle, drei passende Regeln) und das Projekt
# OHNE Lintbefehl, das seinen Schlitz streicht. Eine Pruefung, die einen dieser drei
# beanstandet, beanstandet jedes echte Projekt.
#
# Die Meldungstexte sind umlautfrei gewaehlt, damit sie hier so stehen koennen, wie sie
# im Validator stehen.
M42_UNERKLAERT = "und kein Platzhalter des Overlays"
M42_OFFEN = "aber noch den offenen Schlitz"
M42_ABWEICHUNG = "ist eine Abweichung"
M42_ANKER = "keine Tabellenzeile nennt"
M42_MEHRDEUTIG = "Tabellenzeilen nennen"
M42_ALLE = (M42_UNERKLAERT, M42_OFFEN, M42_ABWEICHUNG, M42_ANKER, M42_MEHRDEUTIG)


def _42_overlay_pfad(root: str) -> str:
    return os.path.join(root, ".koolie/project-overlay", "OVERLAY.md")


def _42_zeile(root: str, platzhalter: str) -> tuple:
    """Index und Zeilen des Overlays - der Platzhalter muss in genau einer Zeile stehen."""
    zeilen = lies(_42_overlay_pfad(root)).splitlines(True)
    treffer = [i for i, z in enumerate(zeilen)
               if z.lstrip().startswith("|") and ("`%s`" % platzhalter) in z]
    if len(treffer) != 1:
        raise Praeparationsfehler(
            "OVERLAY.md: %s steht in %d Tabellenzeilen, erwartet genau eine - die "
            "Sonde hat ihren Gegenstand verloren" % (platzhalter, len(treffer)))
    return treffer[0], zeilen


def _42_erklaert(root: str, platzhalter: str, wert: str) -> None:
    """Den Befehl neben einem Platzhalter setzen - der Wert muss sich aendern."""
    i, zeilen = _42_zeile(root, platzhalter)
    roh = zeilen[i]
    ende = roh[len(roh.rstrip("\r\n")):]
    felder = roh.rstrip("\r\n").split("|")
    for k, feld in enumerate(felder):
        if feld.strip("` *") == platzhalter and k + 1 < len(felder):
            if felder[k + 1].strip("` *") == wert:
                raise Praeparationsfehler(
                    "OVERLAY.md: %s erklaert bereits %r - die Sonde praepariert nichts"
                    % (platzhalter, wert))
            felder[k + 1] = " `%s` " % wert
            break
    else:
        raise Praeparationsfehler(
            "OVERLAY.md: keine Zelle rechts neben %s - die Tabellenform hat sich "
            "geaendert" % platzhalter)
    zeilen[i] = "|".join(felder) + ende
    schreib(_42_overlay_pfad(root), "".join(zeilen))


def _42_platzhalter_weg(root: str, platzhalter: str) -> None:
    """Den Platzhalter aus seiner Zelle nehmen - der verlorene Anker."""
    i, zeilen = _42_zeile(root, platzhalter)
    zeilen[i] = zeilen[i].replace("`%s`" % platzhalter, "keiner")
    schreib(_42_overlay_pfad(root), "".join(zeilen))


def _42_zeile_doppeln(root: str, platzhalter: str) -> None:
    """Die Zeile ein zweites Mal anlegen - zwei Zeilen, zwei moegliche Befehle."""
    i, zeilen = _42_zeile(root, platzhalter)
    zeilen.insert(i + 1, zeilen[i])
    schreib(_42_overlay_pfad(root), "".join(zeilen))


def _42_rechte(root: str, rel: str, *aenderungen) -> None:
    """Die Berechtigungsdatei eines beliebigen Packs praeparieren.

    Die Waechter sitzen in den Eingriffen selbst (_37_weg, _37_dazu, _37_statt), die
    hier wiederverwendet werden - ein Textvergleich taugte fuer eine JSON-Datei nicht
    (D-74).
    """
    pfad = os.path.join(root, *rel.split("/"))
    daten = json.loads(lies(pfad))
    for aenderung in aenderungen:
        aenderung(daten)
    schreib(pfad, json.dumps(daten, indent=2, ensure_ascii=False) + "\n")


def _42_trifft(root: str, erwartet) -> bool:
    """Ein Validatorlauf gegen die erwartete Meldung.

    erwartet als Zeichenkette: Die Meldung MUSS vorkommen (Sonde).
    erwartet als Tupel: KEINE der Meldungen darf vorkommen (Gegenprobe).

    Ohne Ergebniszeile ist der Lauf kein Messwert, sondern ein Abbruch - dann gilt er
    als nicht bestanden (Arbeitswissen vom 2026-09-14).
    """
    aus = validator_ausgabe(root)
    if "Ergebnis:" not in aus:
        notiz("        Kein Messwert: der Lauf hat keine Ergebniszeile geliefert.")
        return False
    if isinstance(erwartet, str):
        if erwartet not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
            return False
        return True
    uebrig = [m for m in erwartet if m in aus]
    if uebrig:
        notiz("        Unerwartet gemeldet:", ", ".join(uebrig))
        notiz("        Ausgabe:", " | ".join(
            z for z in aus.splitlines() if "FEHLER" in z)[:400])
        return False
    return True


def sonden_schlitzinhalte() -> None:
    """Wirkungsnachweis zu Pruefung 42 (CR-2026-066, D-90 und D-91)."""
    # Seit 1.18.2 fuehrt claude-code ZWEI Befehlswerkzeuge (D-469): Jeder Befehlsschlitz steht
    # als Bash(...) und PowerShell(...) in der Datei, und ein ordentlich gefuelltes Projekt fuellt
    # beide. Die Sonden fuellen nur den ersten - ihr Befund liegt dort.
    for pack, rechte, werkzeuge in (("claude-code", ".claude/settings.json", ("Bash", "PowerShell")),
                                    ("devin-desktop", ".devin/config.json", ("Exec",))):
        werkzeug = werkzeuge[0]
        root = installation(pack)
        try:
            pfad_r = os.path.join(root, *rechte.split("/"))
            pfad_o = _42_overlay_pfad(root)
            ausgang_r, ausgang_o = lies(pfad_r), lies(pfad_o)
            schreib(os.path.join(root, "README.md"), "# Sondenprojekt\r\n")

            def zurueck():
                schreib(pfad_r, ausgang_r)
                schreib(pfad_o, ausgang_o)

            def sch(name):
                return "%s(<%s>)" % (werkzeug, name)

            def rg(befehl):
                return "%s(%s)" % (werkzeug, befehl)

            # --- Gegenprobe 42a: der Auslieferungszustand -----------------------
            melde("GEGENPROBE", "42a", _42_trifft(root, M42_ALLE),
                  "Auslieferungszustand: Overlay dreimal <TBD>, drei offene Schlitze "
                  "(%s)" % pack)

            # --- Gegenprobe 42b: das ordentlich ausgefuellte Projekt ------------
            for name, befehl in (("BUILD_COMMAND", "mvn -B clean package"),
                                 ("TEST_COMMAND", "mvn -B test"),
                                 ("LINT_COMMAND", "mvn -B verify")):
                _42_erklaert(root, "<%s>" % name, befehl)
                for w in werkzeuge:
                    _42_rechte(root, rechte, lambda d, n=name, b=befehl, w=w: _37_statt(
                        d, "ask", "%s(<%s>)" % (w, n), "%s(%s)" % (w, b)))
            melde("GEGENPROBE", "42b", _42_trifft(root, M42_ALLE),
                  "Drei erklaerte Befehle, drei passende Regeln - der Normalfall "
                  "(%s)" % pack)
            zurueck()

            # --- Gegenprobe 42c: kein Lintbefehl, Schlitz gestrichen ------------
            # Der zulaessige Weg fuer ein Projekt ohne Formatpruefung. Er darf nicht
            # teurer sein als der unzulaessige.
            _42_erklaert(root, "<BUILD_COMMAND>", "mvn -B clean package")
            _42_erklaert(root, "<TEST_COMMAND>", "mvn -B test")
            _42_erklaert(root, "<LINT_COMMAND>", "nicht vorhanden")
            for w in werkzeuge:
                _42_rechte(root, rechte,
                           lambda d, w=w: _37_statt(d, "ask", "%s(<BUILD_COMMAND>)" % w,
                                                    "%s(mvn -B clean package)" % w),
                           lambda d, w=w: _37_statt(d, "ask", "%s(<TEST_COMMAND>)" % w,
                                                    "%s(mvn -B test)" % w),
                           lambda d, w=w: _37_weg(d, "ask", "%s(<LINT_COMMAND>)" % w))
            melde("GEGENPROBE", "42c", _42_trifft(root, M42_ALLE),
                  "Kein Lintbefehl, Schlitz gestrichen - der zulaessige Weg "
                  "(%s)" % pack)
            zurueck()

            # --- Sonde 42a: der Fall des Piloten --------------------------------
            # Das Overlay sagt "nicht vorhanden", die Datei gewaehrt einen dritten
            # Befehl. Pruefung 37 schweigt dazu, weil drei Schlitze drei Zeilen decken.
            _42_erklaert(root, "<BUILD_COMMAND>", "mvn -B clean package")
            _42_erklaert(root, "<TEST_COMMAND>", "mvn -B test")
            _42_erklaert(root, "<LINT_COMMAND>", "nicht vorhanden")
            _42_rechte(root, rechte,
                       lambda d: _37_statt(d, "ask", sch("BUILD_COMMAND"),
                                           rg("mvn -B clean package")),
                       lambda d: _37_statt(d, "ask", sch("TEST_COMMAND"),
                                           rg("mvn -B test")),
                       lambda d: _37_statt(d, "ask", sch("LINT_COMMAND"),
                                           rg("mvn -B -q compile")))
            melde("SONDE", "42a", _42_trifft(root, M42_UNERKLAERT),
                  "Der Fall des Piloten: Overlay sagt 'nicht vorhanden', die Datei "
                  "gewaehrt einen dritten Befehl (%s)" % pack)
            zurueck()

            # --- Sonde 42b: das Overlay erklaert gar nichts ---------------------
            # Der Lauf M10 der Gegenpruefung: drei <TBD> decken drei Freigaben,
            # darunter eine mit Fernwirkung.
            _42_rechte(root, rechte,
                       lambda d: _37_statt(d, "ask", sch("BUILD_COMMAND"),
                                           rg("mvn -B clean package")),
                       lambda d: _37_statt(d, "ask", sch("TEST_COMMAND"),
                                           rg("mvn -B test")),
                       lambda d: _37_statt(d, "ask", sch("LINT_COMMAND"),
                                           rg("mvn -B deploy")))
            melde("SONDE", "42b", _42_trifft(root, M42_UNERKLAERT),
                  "Overlay erklaert dreimal <TBD>, die Datei gewaehrt drei Befehle - "
                  "einer davon mit Fernwirkung (%s)" % pack)
            zurueck()

            # --- Sonde 42c: der Schlitz traegt einen anderen Befehl -------------
            _42_erklaert(root, "<TEST_COMMAND>", "mvn -B test")
            _42_rechte(root, rechte, lambda d: _37_statt(
                d, "ask", sch("TEST_COMMAND"), rg("mvn -B verify")))
            melde("SONDE", "42c", _42_trifft(root, M42_ABWEICHUNG),
                  "Gefuellter Schlitz mit fremdem Befehl - der Fall, den Kandidat 2 "
                  "beschrieb (%s)" % pack)
            zurueck()

            # --- Sonde 42d: erklaert, aber der Schlitz steht noch offen ---------
            _42_erklaert(root, "<TEST_COMMAND>", "mvn -B test")
            melde("SONDE", "42d", _42_trifft(root, M42_OFFEN),
                  "Das Overlay erklaert einen Befehl, die Datei traegt noch den "
                  "offenen Schlitz (%s)" % pack)
            zurueck()

            # --- Sonde 42e: der verlorene Anker ---------------------------------
            _42_platzhalter_weg(root, "<LINT_COMMAND>")
            melde("SONDE", "42e", _42_trifft(root, M42_ANKER),
                  "Verlorener Anker - keine Tabellenzeile nennt den Platzhalter mehr "
                  "(%s)" % pack)
            zurueck()

            # --- Sonde 42f: zwei Zeilen fuer denselben Platzhalter --------------
            _42_zeile_doppeln(root, "<TEST_COMMAND>")
            melde("SONDE", "42f", _42_trifft(root, M42_MEHRDEUTIG),
                  "Zwei Tabellenzeilen nennen denselben Platzhalter - welcher Befehl "
                  "gilt? (%s)" % pack)
            zurueck()
        finally:
            aufraeumen(os.path.dirname(root))


buendel(sonden_schlitzinhalte,
        "Der Inhalt der drei Befehlsschlitze gegen die Berechtigungsdatei, je Pack: "
        "unerklaerter Befehl, fremder Befehl, offener Schlitz, verlorener Anker, doppelte Zeile")

M43_FEHLT = "trägt keinen 'hooks'-Block"
M43_LEER = "ohne ein einziges PreToolUse-Kommando"
M43_ALLE = (M43_FEHLT, M43_LEER)

# Dieselbe Lagepruefung wie bei Pruefung 42: Ein String MUSS in der Ausgabe stehen, eine
# Liste von Strings darf NICHT darin stehen. Sie ist nicht an 42 gebunden.
_43_trifft = _42_trifft


def _43_block_weg(pfad: str) -> None:
    """Den hooks-Block entfernen - der Fall des Uebungsrepositoriums.

    Der Waechter sitzt im Eingriff, nicht in einem Textvergleich: json.dumps
    normalisiert die Datei ohnehin (dieselbe Zusage wie D-74, siehe _37_schreiben).
    """
    daten = json.loads(lies(pfad))
    if "hooks" not in daten:
        raise Praeparationsfehler(
            "%s: es gibt keinen hooks-Block zu entfernen; die Sonde hat ihren "
            "Gegenstand verloren" % os.path.basename(pfad))
    del daten["hooks"]
    schreib(pfad, json.dumps(daten, indent=2, ensure_ascii=False) + "\n")


def _43_block_leeren(pfad: str) -> None:
    """Den hooks-Block behalten, PreToolUse leeren - die halbe Migration."""
    daten = json.loads(lies(pfad))
    hooks = daten.get("hooks")
    if not isinstance(hooks, dict) or not hooks.get("PreToolUse"):
        raise Praeparationsfehler(
            "%s: kein PreToolUse-Eintrag zum Leeren vorhanden" % os.path.basename(pfad))
    hooks["PreToolUse"] = []
    schreib(pfad, json.dumps(daten, indent=2, ensure_ascii=False) + "\n")


def sonden_hookblock() -> None:
    """Wirkungsnachweis zu Pruefung 43 (CR-2026-067, D-92)."""
    # Der verwaiste Dateiname ist fuer beide Packs derselbe: VERWAISTE_HOOK_DATEIEN
    # im Validator fuehrt genau einen. Die erste Fassung dieser Sonde riet fuer
    # claude-code "hooks.json" und fiel - an der Sonde, nicht an der Pruefung.
    for pack, rechte in (("claude-code", ".claude/settings.json"),
                         ("devin-desktop", ".devin/config.json")):
        verwaist = "hooks.v1.json"
        root = installation(pack)
        try:
            pfad = os.path.join(root, *rechte.split("/"))
            ausgang = lies(pfad)
            schreib(os.path.join(root, "README.md"), "# Sondenprojekt\r\n")

            # --- Gegenprobe 43a: der Auslieferungszustand ------------------------
            melde("GEGENPROBE", "43a", _43_trifft(root, M43_ALLE),
                  "Auslieferungszustand: der Block steht in der Berechtigungsdatei "
                  "(%s)" % pack)

            # --- Sonde 43a: der Fall des Uebungsrepositoriums --------------------
            # Einunddreissig Releases lang so gemessen: Hooks in der eigenen Datei des
            # Packs, die der Client nicht liest, und kein Block in der wirksamen.
            _43_block_weg(pfad)
            melde("SONDE", "43a", _43_trifft(root, M43_FEHLT),
                  "Kein hooks-Block in der Berechtigungsdatei - der Hook ist stumm "
                  "(%s)" % pack)

            # --- Sonde 43b: dieselbe Lage mit verwaister Datei daneben -----------
            # Wer der Warnung der Pruefung 18 woertlich folgt, loescht die alte Datei
            # und hat danach gar keinen Hook. Die Meldung muss beide Haelften nennen.
            runtime = os.path.dirname(pfad)
            schreib(os.path.join(runtime, verwaist), "{}\n")
            aus = validator_ausgabe(root)
            ok = M43_FEHLT in aus and verwaist in aus
            melde("SONDE", "43b", ok,
                  "Kein Block, aber die verwaiste Hook-Datei daneben - die Meldung "
                  "nennt beide (%s)" % pack)
            if not ok:
                notiz("        Ausgabe:", " | ".join(
                    z for z in aus.splitlines() if "FEHLER" in z)[:400])
            os.remove(os.path.join(runtime, verwaist))
            schreib(pfad, ausgang)

            # --- Sonde 43c: der Block steht da und ist leer ----------------------
            _43_block_leeren(pfad)
            melde("SONDE", "43c", _43_trifft(root, M43_LEER),
                  "hooks-Block ohne PreToolUse-Kommando - vorhanden und wirkungslos "
                  "(%s)" % pack)
            schreib(pfad, ausgang)
        finally:
            aufraeumen(os.path.dirname(root))


buendel(sonden_hookblock,
        "Vier echte Installationen: ein fehlender, ein leerer und ein verwaister hooks-Block "
        "je Pack - der Fall des Uebungsrepositoriums")


# --- Pruefung 44: das Praeparationsregister ------------------------------------------
P44_REGISTER = ".koolie/core/onboarding/exercises/README.md"
P44_KATALOG = ".koolie/core/tests/TEST_CATALOG.md"
M44_UNREGISTRIERT = "das Register in"
M44_TOT = "die kein Testfall nennt"
M44_ANKER = "führt kein Register mehr"
M44_OHNE_BELEG = "führt keine Belegzelle"
M44_SPALTE_WEG = "führt keine Spalte"
# Jede Meldung der Pruefung 44 endet auf ihren Decision Record. Die generische
# gegenprobe() nimmt genau einen Suchtext - dieser faengt alle drei und jede kuenftige.
M44_JEDE = "(D-93)"

# Synthetische Kennungen - alle drei hoch, und der Grund steht in der Geschichte dieser
# Zeile: Bis 0.58.0 nahm die Gegenprobe "UEB-08", weil das die naechste FREIE Kennung
# war. Mit 0.59.0 ist sie VERGEBEN worden (der rote Test, D-136) - und die Gegenprobe
# haette eine zweite Registerzeile derselben Kennung erzeugt. `frei()` faengt das, aber
# erst im Lauf. Die Lehre von G-18 (2026-09-13) gilt damit auch fuer die Kennung, die
# heute noch frei ist: **Eine synthetische Kennung nimmt nie die naechste freie.**
P44_UNREG = "UEB-99"
P44_TOT = "UEB-98"
P44_NEU = "UEB-97"

# Der Anker ist mit 0.59.0 von `FW-NE-01` auf `FW-NE-03` gewandert: Die Vorbedingung
# von `FW-NE-01` nennt seither die Gegenstelle (D-135) und passt nicht mehr. Gesucht
# wird eine Vorbedingung OHNE Kennung - genau das ist der Fall, den 44a herstellt.
P44_VORBEDINGUNG_ALT = "| FW-NE-03 | Bypass-Aufforderung | Übungsrepo |"
# Sechs Spalten seit 0.58.0 - die Belegzelle ist die vierte (D-131). Eine neue Pruefung
# kann eine bestehende Gegenprobe unvollstaendig machen; nachgezogen wird die GEGENPROBE.
P44_REGISTERZEILE = ("| `%s` | **Synthetisch:** Eintrag der Gegenprobe | nirgends | "
                     "Vorhandensein der Datei | nichts | `FW-NE-03` |")


def _44_pfad(root: str, rel: str) -> str:
    return os.path.join(root, *rel.split("/"))


def _44_katalog_nennt(root: str, kennung: str) -> None:
    """Eine Vorbedingung ohne Kennung nennt eine - FW-NE-01 hat heute keine."""
    ersetze(_44_pfad(root, P44_KATALOG),
            (P44_VORBEDINGUNG_ALT,
             P44_VORBEDINGUNG_ALT[:-1] + "; Präparation `%s` |" % kennung))


def _44_register_zeile(root: str, kennung: str) -> None:
    """Eine Zeile ans Ende der Registertabelle - hinter UEB-07."""
    pfad = _44_pfad(root, P44_REGISTER)
    frei(pfad, kennung)
    zeile_nach(pfad, "| `UEB-07` |", P44_REGISTERZEILE % kennung)


sonde("44a", "Eine Vorbedingung nennt eine Praeparation, die das Register nicht fuehrt",
      lambda root: (frei(_44_pfad(root, P44_KATALOG), P44_UNREG),
                    _44_katalog_nennt(root, P44_UNREG)),
      M44_UNREGISTRIERT)

sonde("44b", "Das Register fuehrt eine Praeparation, die kein Testfall braucht",
      lambda root: _44_register_zeile(root, P44_TOT),
      M44_TOT)

sonde("44c", "Der verlorene Anker - die Registerueberschrift ist umbenannt",
      lambda root: ersetze(_44_pfad(root, P44_REGISTER),
                           ("### Register der Präparationen",
                            "### Übersicht der Präparationen")),
      M44_ANKER)

gegenprobe("44a", "Auslieferungszustand: acht registrierte, acht gebrauchte "
                  "Praeparationen", None, M44_JEDE)

gegenprobe("44b", "Eine NEUNTE Praeparation, registriert MIT Belegzelle UND von "
                  "einem Testfall gebraucht - der zulaessige Weg",
           lambda root: (_44_register_zeile(root, P44_NEU),
                         _44_katalog_nennt(root, P44_NEU)),
           M44_JEDE)


# --- Gegenstand 3: die Belegzelle (D-131) --------------------------------------------
#
# UEB-06 stand dreizehn Releases lang im Register und stellte seinen Gegenstand nicht
# her. Die beiden Sonden treffen die zwei Wege, auf denen das wieder geschehen kann: eine
# Zeile ohne Beleg, und eine Spaltenueberschrift, die sich aendert. Die zweite ist die
# Sonde auf den verlorenen Anker - ohne sie bestuende Gegenstand 3 leise.
def _44_beleg_leeren(root: str) -> None:
    """Die Belegzelle einer echten Registerzeile leeren - UEB-04 hat die kuerzeste."""
    ersetze(_44_pfad(root, P44_REGISTER),
            ("| Wurzelverzeichnis | Vorhandensein der Datei |",
             "| Wurzelverzeichnis |  |"))


sonde("44d", "Eine registrierte Praeparation ohne Belegzelle - der Fall UEB-06",
      _44_beleg_leeren,
      M44_OHNE_BELEG)

sonde("44e", "Der verlorene Anker der Belegspalte - die Ueberschrift ist umbenannt",
      lambda root: ersetze(_44_pfad(root, P44_REGISTER),
                           ("| Wie sie belegt ist |", "| Wie belegt |")),
      M44_SPALTE_WEG)


# --- Gegenstand 4: die zeilenweise Deckung (D-173) -----------------------------------
#
# Gegenstand 1 und 2 vergleichen MENGEN ueber die ganze Datei und bestehen auch dann,
# wenn die Kennung in der Ergebniszelle statt in der Vorbedingung steht. Die beiden
# Sonden treffen die zwei Richtungen; die Gegenprobe belegt den ZUSCHNITT, und sie ist
# der wichtigere Teil: FW-NE-02 nennt UEB-06 HINTER dem Vermerk, ohne es zu verlangen,
# und eine Pruefung, die die ganze Zelle liest, meldete diese Zeile mit.
M44_VORBEDINGUNG_FEHLT = "dessen Vorbedingungszelle"
M44_REGISTER_FEHLT = "die Registerzeile"


def _44_kennung_nur_im_ergebnis(root: str) -> None:
    """Die Kennung aus der Vorbedingung in die ERGEBNISZELLE verschieben.

    Genau der Zustand, den 0.64.0 an drei Blattzellen hinterlassen hat: Die Menge
    stimmt, die Spalte nicht.
    """
    pfad = _44_pfad(root, P44_KATALOG)
    ersetze(pfad, ("Übungsrepo; zwei gleichnamige Module in verschiedenen "
                   "Verzeichnissen (Präparation `UEB-12`)",
                   "Übungsrepo; zwei gleichnamige Module in verschiedenen "
                   "Verzeichnissen"))


def _44_registerzeile_kuerzen(root: str) -> None:
    """Einen Testfall aus der Testfallspalte einer Registerzeile entfernen."""
    ersetze(_44_pfad(root, P44_REGISTER),
            ("| `FW-SC-01` (Ü6c), `FW-SC-02` |", "| `FW-SC-01` (Ü6c) |"))


def _44_kennung_hinter_vermerk(root: str) -> None:
    """Die Kennung steht hinter dem Vermerk - der Fall FW-NE-02.

    Sie wird dort GENANNT, nicht VERLANGT. Ohne diesen Zuschnitt meldete die Pruefung
    jede Zeile mit, die die Geschichte ihrer Vorbedingung erzaehlt.
    """
    pfad = _44_pfad(root, P44_KATALOG)
    ersetze(pfad, ("| FW-NE-03 | Bypass-Aufforderung | Übungsrepo |",
                   "| FW-NE-03 | Bypass-Aufforderung | Übungsrepo. \U0001F534 "
                   "**Sondenvermerk:** `UEB-04` wird hier genannt, nicht verlangt |"))


sonde("44f", "Die Kennung steht nur in der Ergebniszelle - die Spalte, die sagt, was "
             "herzustellen ist, sagt es nicht", _44_kennung_nur_im_ergebnis,
      M44_VORBEDINGUNG_FEHLT)

sonde("44g", "Die Registerzeile fuehrt einen Testfall nicht, dessen Vorbedingung sie "
             "nennt - die Gegenrichtung", _44_registerzeile_kuerzen,
      M44_REGISTER_FEHLT)

gegenprobe("44c", "Eine Kennung HINTER dem Vermerk bleibt zulaessig - der Fall "
                  "FW-NE-02, der UEB-06 nennt, ohne es zu verlangen",
           _44_kennung_hinter_vermerk, M44_JEDE)


# --- Pruefung 45: der Bytecode des Kerns (CR-2026-069, D-97) -------------------------
#
# Zwei Gegenstaende, zwei Bauarten. Gegenstand 1 ist ein Textvergleich und laeuft auf
# einer Kopie wie jede gewoehnliche Sonde. Gegenstand 2 braucht ein **echtes
# Repositorium** - kopie() laesst .git bewusst weg, und ohne .git ist der Gegenstand
# nicht herstellbar. Er steht deshalb im Buendel und legt sich seins selbst an.
M45_REGEL = "deckt den Bytecode des Kerns nicht ab"
M45_OHNE_DATEI = ".gitignore: nicht vorhanden"
M45_BESTAND = "sind versioniert"
M45_NICHT_GELAUFEN = "ist nicht gelaufen"
P45_ZEILE = "__pycache__/"


def _45_regel_weg(root: str) -> None:
    """Die Deckungszeile aus der .gitignore nehmen - und nur sie."""
    ersetze(P(root, ".gitignore"), (P45_ZEILE + "\r\n", ""))


def _45_datei_weg(root: str) -> None:
    os.remove(P(root, ".gitignore"))


def _45_andere_schreibweise(root: str) -> None:
    """`*.pyc` statt `__pycache__/` - eine andere Schreibweise, dieselbe Wirkung."""
    ersetze(P(root, ".gitignore"), (P45_ZEILE, "*.pyc"))


sonde("45a", "Die .gitignore deckt den Bytecode des Kerns nicht mehr ab - jeder Lauf "
             "legte dann versionierbaren Bytecode an", _45_regel_weg, M45_REGEL)

sonde("45b", "Ohne .gitignore kann die Regel nicht geprueft werden, und die Pruefung "
             "sagt es als Warnung statt zu schweigen", _45_datei_weg, M45_OHNE_DATEI)

gegenprobe("45a", "Eine andere, ebenso wirksame Schreibweise bleibt unbeanstandet - "
                  "eine zu enge Pruefung meldete hier den richtigen Text",
           _45_andere_schreibweise, M45_REGEL)


# Gegenstand 3 (D-383, K-124): Im Quellrepositorium schliesst die .gitignore die
# Wurzelerzeugnisse JEDES Packs aus. Die Kopie ist ein Quellrepositorium - sie traegt
# das Kennzeichen -, deshalb laeuft der Gegenstand hier und in keiner Installation.
M45_ERZEUGNIS = "schließt das Erzeugnis `/.codex` nicht aus"
P45_CODEX = "/.codex/"


def _45_erzeugnis_weg(root: str) -> None:
    """Die Zeile eines Packs, das das Quellrepositorium nicht selbst installiert."""
    ersetze(P(root, ".gitignore"), (P45_CODEX + "\r\n", ""))


def _45_erzeugnis_andere_schreibweise(root: str) -> None:
    """`.codex` statt `/.codex/` - git schliesst damit dasselbe Verzeichnis aus."""
    ersetze(P(root, ".gitignore"), (P45_CODEX + "\r\n", ".codex\r\n"))


sonde("45e", "Die .gitignore des Quellrepositoriums schliesst das Erzeugnis eines Packs "
             "nicht mehr aus - es waere nach dessen Installation versionierbar",
      _45_erzeugnis_weg, M45_ERZEUGNIS)

gegenprobe("45c", "Dieselbe Zeile ohne Schraegstriche bleibt unbeanstandet - git schliesst "
                  "damit dasselbe Verzeichnis aus",
           _45_erzeugnis_andere_schreibweise, "schließt das Erzeugnis")


def _45_repo(root: str) -> bool:
    """Aus dem Installationsverzeichnis ein Repositorium machen. False = kein git."""
    p = unterprozess(["git", "init", "-q", root])
    return p.returncode == 0


def _45_bytecodedatei(root: str) -> str:
    """Eine .pyc an den Ort legen, an dem der Kern seinen Bytecode erzeugt."""
    ablage = os.path.join(root, ".koolie/core", "__pycache__")
    os.makedirs(ablage, exist_ok=True)
    pfad = os.path.join(ablage, "clientmap.cpython-314.pyc")
    io.open(pfad, "wb").write(b"\x00\x00\x00\x00Sondenbytecode")
    return ".koolie/core/__pycache__/clientmap.cpython-314.pyc"


def sonden_bytecode() -> None:
    """Wirkungsnachweis zu Gegenstand 2 der Pruefung 45 (CR-2026-069, D-97)."""
    root = installation("claude-code")
    try:
        schreib(os.path.join(root, "README.md"), "# Sondenprojekt\r\n")
        schreib(os.path.join(root, ".gitignore"), P45_ZEILE + "\r\n")

        # --- Sonde 45d: kein Repositorium - die Haelfte faellt NICHT stumm aus -------
        # Sie steht vor dem git init, weil genau dieser Zustand der Normalfall jeder
        # anderen Sonde dieses Skripts ist: eine Kopie ohne .git.
        aus = validator_ausgabe(root)
        melde("SONDE", "45d", M45_NICHT_GELAUFEN in aus,
              "Ohne Repositorium meldet Gegenstand 2, dass er nicht gelaufen ist - "
              "eine Pruefhaelfte, die stumm ausfaellt, waere der Befundtyp selbst")

        if not _45_repo(root):
            melde("BUENDEL", "-", False,
                  "sonden_bytecode  [git nicht erreichbar]")
            notiz("        Ohne git ist Gegenstand 2 der Pruefung 45 nicht messbar.")
            return

        # --- Gegenprobe 45b: ein Repositorium ohne verfolgten Bytecode ---------------
        # Sie belegt zweierlei: dass der Auslieferungszustand durchlaeuft UND dass
        # Gegenstand 2 ueberhaupt gelaufen ist. Ohne die zweite Bedingung bestuende sie
        # auch dann, wenn git fehlte - und meldete dann nichts ueber die Pruefung.
        unterprozess(["git", "-C", root, "add", "-A"])
        aus = validator_ausgabe(root)
        ok = M45_BESTAND not in aus and M45_NICHT_GELAUFEN not in aus
        melde("GEGENPROBE", "45b", ok,
              "Ein Repositorium ohne verfolgten Bytecode bleibt unbeanstandet, und "
              "Gegenstand 2 ist dabei nachweislich gelaufen")
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "45" in z or "Bytecode" in z)[:400])

        # --- Sonde 45c: eine verfolgte .pyc unter <CORE_DIR>/ ------------------------
        # Der Fall des Piloten, abgezaehlt am 2026-09-15: sechs Dateien. Die Regel in
        # der .gitignore steht dabei da - git liest sie fuer verfolgte Dateien nicht,
        # und genau deshalb reicht Gegenstand 1 allein nicht.
        rel = _45_bytecodedatei(root)
        unterprozess(["git", "-C", root, "add", "-f", rel])
        aus = validator_ausgabe(root)
        getroffen = M45_BESTAND in aus and rel in aus
        melde("SONDE", "45c", getroffen,
              "Eine verfolgte Bytecodedatei wird gemeldet, obwohl die Regel in der "
              "Datei steht - der Fall des Piloten vom 2026-09-15")
        if not getroffen:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_bytecode,
        "Gegenstand 2 der Pruefung 45 an einem echten Repositorium: ohne git, ohne "
        "verfolgten Bytecode, und mit dem Fall des Piloten")
