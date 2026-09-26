#!/usr/bin/env python3
"""Wirkungsnachweis nach D-23 fuer die Pruefungen 4, 6, 8, 14, 18 bis 66 und 68 bis 95, dazu fuer
install.py (Clientwahl, Aktivierungspruefung, --list-skills, Schutz vorhandener
Projektdateien bei der Erstinstallation, Auskunft ueber ignorierte Kerndateien,
Overlay-Muster) und fuer den Praeparationswaechter dieses
Skripts selbst.

Die Aufzaehlung der Pruefungen steht hier in der Schreibweise, die Pruefung 40 aus den
Sondenkennungen dieses Skripts ausrechnet und woertlich vergleicht (D-86). Bis 0.41.0
stand an dieser Stelle eine Release-Chronik, die bei 0.29.0 endete: ein Register, das
mit jedem Release falscher wurde, ohne dass ein Lauf davon Notiz nahm. Welches Release
welche Sonde gebracht hat, steht im Aenderungsverlauf und nicht mehr hier.

Aufruf (im Wurzelverzeichnis des Repositoriums):
    python3 .koolie/core/tests/scripts/probe-pruefungen.py [PFAD] [--bahnen N]

D-23 sagt: Eine Pruefung gilt erst als vorhanden, wenn sie eine bewusst gesetzte Sonde
meldet. Dieses Skript fuehrt den Nachweis, statt ihn zu behaupten. Je Pruefung

  * eine **Sonde**: ein bekannter Defekt in einer Kopie des Repositoriums - die Pruefung
    MUSS ihn melden;
  * eine **Gegenprobe**: ein Fall, der erlaubt ist und aehnlich aussieht - die Pruefung
    DARF ihn nicht melden.

Die kleinste Einheit ist die Sonde, die Gegenprobe oder - wo mehrere Faelle aufeinander
aufbauen - das **Buendel**, nie einer seiner Teile. Jede Einheit traegt einen **Namen**
und einen **Beschreibungssatz von 5 bis 30 Worten**; die Selbstprobe B1 zaehlt ihn nach.
Die Einheiten laufen seit 0.46.0 **nebenlaeufig** auf mehreren Bahnen - jede auf ihrer
eigenen Kopie, innerhalb eines Buendels weiterhin streng seriell (`--bahnen 1` faehrt
den seriellen Lauf von frueher). Ihre **Laufzeit** steht am Ende, langsamste zuerst, und
zwar unterhalb einer Trennlinie: Die Ergebniszeilen daruber sind die zeilengleiche
Abnahmeform nach D-49, und eine Laufzeit ist nie zweimal dieselbe (CR-2026-068).

Die Gegenprobe ist der Teil, den man weglassen kann und nicht weglassen sollte: Eine
Pruefung, die alles meldet, besteht jede Sonde. Die Gegenproben hier treffen genau die
Faelle, an denen die jeweilige Pruefung zu breit haette werden koennen - die erklaerende
Nennung eines Dateinamens im Fliesstext, ein Begriff ohne Manifestfeld, die Schutzmuster
des durchsetzenden Hooks, ein Pack ohne Importsteuerung, Herkunftsangaben im Kommentar.

Gearbeitet wird auf einer Kopie; das Repositorium selbst bleibt unberuehrt. Exit-Code 0 =
alle Sonden gemeldet, keine Gegenprobe beanstandet **und jede Kopie wieder geloescht** -
eine liegengebliebene meldet der Aufraeumer und zaehlt als Abweichung (D-96).

Was dieses Skript **nicht** leistet: Es belegt, dass die Pruefungen wirken, nicht dass
ihre Gegenstaende richtig sind. Die Grenze jeder einzelnen Pruefung steht in deren
Kopfkommentar in validate-framework.py.
"""
import ast
import glob
import hashlib
import io
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor

BAHNEN_VORGABE = 8


def argumente(argv: list) -> tuple:
    """Pfad und Bahnenzahl aus der Befehlszeile - mehr Schalter gibt es nicht.

    Die Vorgabe ist eine feste Zahl und NICHT die Kernzahl dieser Maschine. Eine
    Vorgabe, die vom Rechner abhaengt, macht zwei Laufzeiten unvergleichbar - und der
    Engpass ist ohnehin nicht die Rechenzeit: Jede Einheit legt eine eigene Kopie des
    Repositoriums an und startet mindestens einen Unterprozess darauf.

    `--bahnen 1` ist der serielle Lauf, Einheit fuer Einheit in der Reihenfolge dieser
    Datei. Er ist der Rueckfallweg, wenn ein Befund sich nur seriell zeigt.
    """
    pfad, bahnen, rest = ".", BAHNEN_VORGABE, list(argv)
    nur, liste = [], False
    while rest:
        wort = rest.pop(0)
        if wort == "--bahnen":
            if not rest or not rest[0].isdigit() or int(rest[0]) < 1:
                sys.exit("--bahnen erwartet eine Zahl ab 1")
            bahnen = int(rest.pop(0))
        elif wort == "--nur":
            if not rest or rest[0].startswith("--"):
                sys.exit("--nur erwartet Kennungen, durch Komma getrennt (z. B. --nur 44,62)")
            nur = [x.strip().lower() for x in rest.pop(0).split(",") if x.strip()]
        elif wort == "--liste":
            liste = True
        elif wort.startswith("--"):
            sys.exit("Unbekannter Schalter: %s (bekannt sind --bahnen N, --nur A,B "
                     "und --liste)" % wort)
        else:
            pfad = wort
    return os.path.abspath(pfad), bahnen, nur, liste


QUELLE, BAHNEN, NUR, LISTE = argumente(sys.argv[1:])
VALIDATOR = ".koolie/core/tests/scripts/validate-framework.py"


def kopie() -> str:
    ziel = tempfile.mkdtemp(prefix="lw-sonde-")
    shutil.copytree(QUELLE, os.path.join(ziel, "repo"),
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "out"))
    return os.path.join(ziel, "repo")


def baumhash(root: str) -> str:
    """Fingerabdruck des Baums - er entscheidet, ob eine Sonde etwas gesetzt hat.

    Ohne ihn ist ein Suchtext, der nicht mehr passt, von einer Pruefung, die nicht
    meldet, nicht zu unterscheiden: Beides sieht aus wie eine gescheiterte Sonde.
    """
    h = hashlib.sha256()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d != "__pycache__")
        for fn in sorted(filenames):
            pfad = os.path.join(dirpath, fn)
            h.update(os.path.relpath(pfad, root).encode("utf-8", "replace"))
            try:
                with open(pfad, "rb") as fh:
                    h.update(fh.read())
            except OSError:
                pass
    return h.hexdigest()


def unterprozess(argv: list, **kw):
    """Unterprozess mit fester Kodierung auf beiden Seiten.

    Ohne beides haengt das Ergebnis von der aufrufenden Umgebung ab: Der Kindprozess
    schreibt unter Windows in der Konsolenkodierung, solange PYTHONIOENCODING nicht
    gesetzt ist, und diese Seite dekodiert mit der Locale-Vorgabe, solange encoding
    fehlt. Ein Diagnosetext mit Umlaut kommt dann veraendert zurueck und trifft keinen
    Suchtext mehr.

    Bei einer Sonde faellt das auf - sie sucht den Text und meldet, dass er fehlt. Bei
    einer Gegenprobe nicht: Ein zerschossener Text ist abwesend, die Gegenprobe besteht
    klaglos, und niemand erfaehrt etwas. Genau der Befundtyp, gegen den D-23 gebaut ist.

    Aufgefallen am 2026-09-12: Derselbe Sondenlauf wurde mit PYTHONIOENCODING=utf-8 in
    der Elternumgebung rot und ohne sie gruen - also gerade bei der Konfiguration, die
    fuer Unterprozesse empfohlen ist. Von 28 Aufrufen der generischen Runner trug
    genau einer einen Suchtext mit Umlaut; die uebrigen 27 warteten darauf
    (CR-2026-049, D-49).

    Diese Funktion ist deshalb der einzige Weg, auf dem dieses Skript einen Prozess
    startet. Zwei Aufrufe trugen die Korrektur, fuenf nicht - das war kein Muster,
    sondern die Reihenfolge ihrer Entstehung.
    """
    umgebung = dict(kw.pop("env", None) or os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run(argv, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", env=umgebung, **kw)


def lauf(root: str) -> str:
    p = unterprozess([sys.executable, os.path.join(root, *VALIDATOR.split("/")),
                      "--root", root])
    return (p.stdout or "") + (p.stderr or "")


def lies(pfad: str) -> str:
    return io.open(pfad, encoding="utf-8", newline="").read()


def schreib(pfad: str, text: str) -> None:
    io.open(pfad, "w", encoding="utf-8", newline="").write(text)


class Praeparationsfehler(Exception):
    """Ein Suchtext einer Praeparation trifft nicht (mehr) - CR-2026-060, D-74.

    Der Unterschied zu einem gewoehnlichen Fehlschlag ist die Zurechnung: Hier hat die
    SONDE ihren Gegenstand verloren, nicht die Pruefung ihre Wirkung. Beides sah bis
    0.37.0 gleich aus, und bei einer mehrteiligen Praeparation sah es sogar aus wie ein
    echter Befund im Repositorium.
    """


def ersetzt(text: str, *paare, quelle: str = "") -> str:
    """Textersetzungen mit geprueften Trefferzahlen - jede einzeln.

    Ein Paar ist (alt, neu) oder (alt, neu, anzahl); die Voreinstellung ist genau ein
    Treffer. Weicht die tatsaechliche Zahl ab, wird NICHTS ersetzt und der Aufruf
    scheitert mit dem Suchtext, der nicht mehr passt.

    WARUM DAS NOETIG IST: baumhash() ist ein Alles-oder-nichts-Waechter. Bei n
    Ersetzungen belegt er "mindestens eine hat gegriffen", nie "alle". Am 2026-09-13
    wurde das gemessen: Auf einem Baum mit einem zwanzigsten Grenzfall traf die erste
    Ersetzung der Gegenprobe 30 nicht, die zweite schon - der Baum aenderte sich, die
    Gegenprobe lief und fiel mit "21 Grenzfallzeilen, der Steckbrief nennt 20". Wer das
    liest, sucht den Fehler in EDGE_CASES.md. Dort ist keiner.

    WAS SIE NICHT LEISTET: Sie deckt den Suchtext, nicht die Absicht. Eine Ersetzung,
    die trifft und das Falsche tut, findet sie nicht.
    """
    for paar in paare:
        alt, neu = paar[0], paar[1]
        anzahl = paar[2] if len(paar) > 2 else 1
        tatsaechlich = text.count(alt)
        if tatsaechlich != anzahl:
            raise Praeparationsfehler(
                "%sSuchtext trifft %dx statt %dx: %r"
                % (quelle + ": " if quelle else "", tatsaechlich, anzahl, alt[:70]))
        text = text.replace(alt, neu, anzahl)
    return text


def ersetze(pfad: str, *paare) -> None:
    """ersetzt() auf einer Datei - lesen, alle Paare pruefen, dann erst schreiben."""
    schreib(pfad, ersetzt(lies(pfad), *paare, quelle=os.path.basename(pfad)))


def zeile_nach(pfad: str, anker: str, neu: str) -> None:
    """Eine Zeile hinter die eine Zeile einfuegen, die mit `anker` beginnt.

    Der Anker muss genau einmal am Zeilenanfang stehen; sonst ist nicht entschieden,
    wohin eingefuegt wuerde, und die Praeparation scheitert statt zu raten.
    """
    zeilen = lies(pfad).split("\r\n")
    treffer = [i for i, z in enumerate(zeilen) if z.startswith(anker)]
    if len(treffer) != 1:
        raise Praeparationsfehler(
            "%s: Anker %r steht %dx am Zeilenanfang, erwartet genau einmal"
            % (os.path.basename(pfad), anker, len(treffer)))
    zeilen.insert(treffer[0] + 1, neu)
    schreib(pfad, "\r\n".join(zeilen))


def frei(pfad: str, *kennungen: str) -> None:
    """Eine synthetische Kennung darf im Zieldokument noch nicht vergeben sein.

    Am 2026-09-13 trug die Gegenprobe 30 als synthetische Kennung ausgerechnet G-18 -
    dieselbe, die 0.36.0 wirklich vergeben hat. Die Falle stand in der Uebergabe
    benannt, und sie ist trotzdem zugeschnappt; eine benannte Falle, in die man zweimal
    tritt, gehoert in den Code (CR-2026-060 E3).

    Der Waechter prueft Abwesenheit, nicht Eignung: Er ist genau so klug wie die
    Kennung, die man ihm gibt.

    NICHT als Vergabe zaehlt die Zeile, die eine Kennung ausdruecklich als synthetisch
    und nie vergeben AUSWEIST (Decision Log, Ausnahmemenge von Pruefung 50). Ohne diese
    Trennung haette der Absatz, der die synthetischen Kennungen schuetzt, sie fuer
    diesen Waechter zu vergebenen gemacht - gemessen am 2026-09-18 an Gegenprobe 46b.
    """
    text = "\n".join(z for z in lies(pfad).splitlines()
                     if not z.lstrip().startswith("**Belegte synthetische Kennungen"))
    for kennung in kennungen:
        if kennung in text:
            raise Praeparationsfehler(
                "%s: Die synthetische Kennung %r ist dort bereits vergeben. Eine "
                "Gegenprobe, die eine echte Kennung doppelt, misst nicht mehr ihren "
                "Fall - eine neue synthetische Kennung waehlen"
                % (os.path.basename(pfad), kennung))


# --- Der Ausfuehrungsplan: erst anmelden, dann fahren -----------------------------
#
# Bis 0.45.0 lief jede Sonde in dem Augenblick, in dem der Auslegeteil dieser Datei ihre
# Zeile erreichte: alle Einheiten streng nacheinander, jede mit einer eigenen Kopie des
# Repositoriums und mindestens einem Validatorlauf darauf. Seit 0.46.0 melden sonde(),
# sonde_ohne_wert(), gegenprobe() und buendel() ihre Einheit nur noch an; gefahren wird
# am Ende, auf mehreren Bahnen (CR-2026-068, D-94 bis D-96).
#
# DREI ZUSAGEN, die dieser Umbau halten muss - alle drei waren hier schon einmal teuer:
#
#   1. DIE SCHREIBWEISE BLEIBT. Pruefung 40 rechnet die Sondenmenge aus zwei woertlichen
#      Mustern dieser Datei aus: dem Aufruf `sonde(` mit seiner Kennung und `melde(` mit
#      der Art SONDE und ihr. Ein Umbau auf ein Register mit eigener Schreibweise haette
#      die Sonden fuer Pruefung 40 unsichtbar gemacht - und die Pruefung haette leise
#      bestanden, weil eine leere Menge keine Abweichung ist. Beide Muster stehen
#      deshalb unveraendert an ihren Aufrufstellen; geaendert hat sich allein, WANN der
#      Aufruf seine Arbeit tut.
#   2. DIE AUSGABE BLEIBT ZEILENGLEICH. D-49 nimmt den Lauf in beiden
#      Kodierungsumgebungen ab, und zwar zeilenweise. Eine nebenlaeufige Einheit
#      schreibt deshalb nicht selbst auf die Standardausgabe, sondern sammelt ihre
#      Zeilen; ausgegeben werden sie in der Reihenfolge der ANMELDUNG, nicht in der der
#      Fertigstellung. Die Laufzeiten stehen unterhalb der Trennlinie und sind
#      ausdruecklich nicht Teil dieses Vergleichs - eine Laufzeit ist nie zweimal
#      dieselbe, und eine Abnahmeform, die einen Filter braucht, ist keine mehr.
#   3. EIN BUENDEL IST DIE KLEINSTE EINHEIT, NIE SEINE TEILE. Seine Faelle bauen
#      aufeinander auf: eine Installation, Schritt fuer Schritt praepariert und wieder
#      zurueckgesetzt. INNERHALB eines Buendels bleibt es streng seriell; nebenlaeufig
#      sind allein die Einheiten gegeneinander.

EINHEITEN = []
_ORT = threading.local()

SATZ_MIN = 5
SATZ_MAX = 30


def worte(satz: str) -> int:
    return len(satz.split())


def zahl(wert: float) -> str:
    """Eine Zahl mit einer Nachkommastelle und Dezimalkomma - deutsch wie der Rest."""
    return ("%.1f" % wert).replace(".", ",")


def kurz(satz: str, breite: int) -> str:
    return satz if len(satz) <= breite else satz[:breite - 3] + "..."


class Einheit:
    """Eine Sonde, eine Gegenprobe oder ein Buendel - mit Name, Satz und Laufzeit.

    `kennung` ist der Name: bei einer Einzelsonde ihre Pruefungsnummer, bei einem
    Buendel der Name seiner Funktion. `satz` ist der Beschreibungssatz, den die
    Selbstprobe B1 nachzaehlt.
    """

    def __init__(self, art: str, kennung: str, satz: str, arbeit) -> None:
        self.art = art
        self.kennung = kennung
        self.satz = satz
        self.arbeit = arbeit
        self.zeilen = []
        self.fehler = 0
        self.dauer = 0.0

    def eintrag(self, art: str, kennung: str, ok: bool, was: str) -> None:
        if not ok:
            self.fehler += 1
        self.zeilen.append(f"{art:10s} {kennung:4s} {'OK  ' if ok else 'FEHL'}  {was}")

    def anmerkung(self, *teile) -> None:
        self.zeilen.append(" ".join(str(t) for t in teile))

    def fahren(self) -> None:
        """Die Einheit fahren und dabei ihre Laufzeit nehmen.

        Ein unerwarteter Fehler bricht nicht den ganzen Lauf ab, sondern faellt dieser
        einen Einheit zur Last - mit Rueckverfolgung in den Anmerkungen. Der Grund ist
        derselbe wie bei buendel(): Ein Abbruch, der 127 ungefahrene Einheiten
        mitnimmt, verbirgt mehr, als er zeigt.
        """
        _ORT.einheit = self
        beginn = time.perf_counter()
        try:
            self.arbeit()
        except Exception as exc:  # absichtlich breit - siehe Kopfkommentar
            self.eintrag(self.art, self.kennung, False,
                         "Abbruch der Einheit: %s: %s" % (type(exc).__name__, exc))
            self.anmerkung("        " + traceback.format_exc().rstrip().replace(
                "\n", "\n        "))
        finally:
            self.dauer = time.perf_counter() - beginn
            _ORT.einheit = None

    def ausgeben(self) -> None:
        # 🔴 KODIERUNGSFEST, UND DER ANLASS IST GEMESSEN (2026-09-19, CR-2026-092):
        # Bricht eine Praeparation, nennt die Meldung ihren Suchtext - und der stammt
        # aus einem Traeger mit echten Sonderzeichen. In der cp1252-Umgebung, die D-49
        # ausdruecklich verlangt, hat ein einziges '→' den GANZEN Lauf mit einem
        # UnicodeEncodeError abgebrochen, nach 53 von 61 Pruefungen. Der Apparat konnte
        # seinen eigenen Befund dort nicht berichten.
        for zeile in self.zeilen:
            try:
                print(zeile)
            except UnicodeEncodeError:
                kodierung = getattr(sys.stdout, "encoding", None) or "ascii"
                print(zeile.encode(kodierung, "backslashreplace").decode(kodierung))


def eintragen(art: str, kennung: str, satz: str, arbeit) -> None:
    """Eine Einheit in den Ausfuehrungsplan aufnehmen, statt sie sofort zu fahren."""
    EINHEITEN.append(Einheit(art, kennung, satz, arbeit))


def melde(art: str, nummer: str, ok: bool, was: str) -> None:
    """Eine Ergebniszeile - sie geht in die Sammlung der gerade laufenden Einheit."""
    _ORT.einheit.eintrag(art, nummer, ok, was)


def notiz(*teile) -> None:
    """Eine Erlaeuterungszeile unter einer Ergebniszeile.

    Sie steht an der Stelle, an der bis 0.45.0 print() stand. Der Unterschied zaehlt
    erst seit der Nebenlaeufigkeit: print() schriebe sofort und mitten in die Zeilen
    einer anderen Einheit hinein, und die Ausgabe waere nicht mehr zeilengleich
    reproduzierbar - der Lauf haette seine Abnahmeform verloren (D-49).
    """
    _ORT.einheit.anmerkung(*teile)


AUFRAEUM_VERSUCHE = 3
AUFRAEUM_PAUSE = 0.5


def schreibschutz_loesen(pfad: str) -> None:
    """Den Schreibschutz im ganzen Baum wegnehmen - leise, Datei fuer Datei.

    Sie meldet nichts: Ob das Loesen gelingt, ist nicht die Frage; die Frage ist, ob
    danach geloescht werden kann, und die beantwortet der naechste Loeschversuch. Eine
    Meldung von hier wuerde derselben Stoerung zwei Zeilen geben.

    Bewusst ohne onerror/onexc von shutil.rmtree: Die beiden Namen haben sich zwischen
    den Python-Fassungen abgeloest, und ein Nachweiswerkzeug, das an der Fassung seines
    Interpreters haengt, ist genau das, was D-49 abgeschafft hat.
    """
    for wurzel, verzeichnisse, dateien in os.walk(pfad):
        for name in verzeichnisse + dateien:
            try:
                os.chmod(os.path.join(wurzel, name), stat.S_IWRITE | stat.S_IREAD)
            except OSError:
                pass


def aufraeumen(pfad: str) -> None:
    """Ein Arbeitsverzeichnis loeschen - und das Scheitern MELDEN, nicht verschlucken.

    Bis 0.45.0 stand an den vierzehn Aufraeumstellen dieses Skripts
    `shutil.rmtree(..., ignore_errors=True)`. Das ist der Befundtyp, gegen den dieses
    Repositorium gebaut ist: eine Zusage - "gearbeitet wird auf einer Kopie; das
    Repositorium selbst bleibt unberuehrt" - mit einem Ausfallpfad, der nichts sagt. Ein
    Lauf, der fuer jede Einheit ein eigenes Arbeitsverzeichnis anlegt und einige davon
    liegen laesst, sah genau so aus wie einer, der aufgeraeumt hat - und die Platte
    fuellte sich stumm.

    WARUM DREI VERSUCHE UND NICHT EINER: Unter Windows haelt ein gerade beendeter
    Unterprozess - oder ein Virenscanner, der ihm nachsieht - eine Datei noch einen
    Augenblick fest. Ein einziger Versuch meldete dann eine Stoerung, die eine halbe
    Sekunde spaeter keine mehr ist; und eine Meldung, die auch ohne Anlass kommt, wird
    binnen eines Releases abgeschaltet.

    WARUM AUSSERDEM DER SCHREIBSCHUTZ FAELLT (0.47.0): Warten hilft gegen eine gehaltene
    Datei und **gar nichts** gegen eine schreibgeschuetzte. Gemessen am 2026-09-15, beim
    ersten echten Fall dieses Aufraeumers: Die Sonde zu Pruefung 45 legt ein
    Repositorium an, git schreibt seine Objektdateien schreibgeschuetzt, und drei
    Versuche ueber anderthalb Sekunden endeten dreimal mit demselben
    "[WinError 5] Zugriff verweigert". **Der Aufraeumer hatte recht und war trotzdem
    nutzlos** - er meldete einen Zustand, den er selbst haette aufloesen koennen. Seit
    diesem Release nimmt jeder Versuch ab dem zweiten zuerst den Schreibschutz weg.

    WAS SIE NICHT LEISTET: Sie raeumt auf, was ihr genannt wird. Ein Verzeichnis, dessen
    Pfad niemand weitergibt, bleibt liegen und wird von ihr nicht vermisst.
    """
    letzter = None
    for _ in range(AUFRAEUM_VERSUCHE):
        if not os.path.isdir(pfad):
            return
        try:
            shutil.rmtree(pfad)
            return
        except OSError as exc:
            letzter = exc
            schreibschutz_loesen(pfad)
            time.sleep(AUFRAEUM_PAUSE)
    if not os.path.isdir(pfad):
        return
    einheit = getattr(_ORT, "einheit", None)
    melde("AUFRAEUMER", "-", False,
          "%s: %s bleibt liegen" % (einheit.kennung if einheit else "-", pfad))
    notiz("        " + str(letzter))
    notiz("        %d Versuche ueber %s s, danach aufgegeben."
          % (AUFRAEUM_VERSUCHE,
             zahl(AUFRAEUM_VERSUCHE * AUFRAEUM_PAUSE)))


def buendel(fn, satz: str) -> None:
    """Eine Funktion, die mehrere Sonden in EINER Installation faehrt.

    Diese Funktionen melden selbst ueber melde() und haben deshalb keinen
    baumhash-Waechter. Faellt eine ihrer Praeparationen aus, bricht das Buendel hier ab:
    laut, mit dem Suchtext, und ohne dass der Rest als bestanden erscheint
    (CR-2026-060 E2).

    Der Beschreibungssatz ist seit 0.46.0 Pflicht und steht als Kopfzeile ueber den
    Zeilen des Buendels. Bis dahin hatte jede Einzelsonde einen erklaerenden Text und
    das Buendel keinen - man sah eine Folge von Meldungen und nicht, was sie zusammen
    belegen sollten.
    """
    def arbeit() -> None:
        notiz("BUENDEL    %s - %s" % (fn.__name__, satz))
        try:
            fn()
        except Praeparationsfehler as exc:
            melde("BUENDEL", "-", False, fn.__name__ + "  [Praeparation gebrochen]")
            notiz("        " + str(exc))
            notiz("        Gemessen wurde nichts - der Rest des Buendels ist nicht gelaufen.")

    eintragen("BUENDEL", fn.__name__, satz, arbeit)


def sonde(nummer: str, was: str, praeparieren, erwartet: str) -> None:
    def arbeit() -> None:
        root = kopie()
        try:
            vorher = baumhash(root)
            try:
                praeparieren(root)
            except Praeparationsfehler as exc:
                melde("SONDE", nummer, False, was + "  [Praeparation gebrochen]")
                notiz("        " + str(exc))
                return
            if baumhash(root) == vorher:
                melde("SONDE", nummer, False, was + "  [nichts praepariert]")
                notiz("        Der Baum ist unveraendert - vermutlich passt der Suchtext "
                      "der Sonde nicht mehr. Gemessen wuerde sonst die Sonde, nicht die Pruefung.")
                return
            ausgabe = lauf(root)
            melde("SONDE", nummer, erwartet in ausgabe, was)
            if erwartet not in ausgabe:
                notiz("        Ausgabe:", " | ".join(ausgabe.splitlines()[:6]))
        finally:
            aufraeumen(os.path.dirname(root))

    eintragen("SONDE", nummer, was, arbeit)


def gegenprobe(nummer: str, was: str, praeparieren, verboten: str) -> None:
    def arbeit() -> None:
        root = kopie()
        try:
            if praeparieren:
                vorher = baumhash(root)
                try:
                    praeparieren(root)
                except Praeparationsfehler as exc:
                    melde("GEGENPROBE", nummer, False,
                          was + "  [Praeparation gebrochen]")
                    notiz("        " + str(exc))
                    return
                if baumhash(root) == vorher:
                    melde("GEGENPROBE", nummer, False, was + "  [nichts praepariert]")
                    return
            ausgabe = lauf(root)
            ok = verboten not in ausgabe and "0 Fehler" in ausgabe
            melde("GEGENPROBE", nummer, ok, was)
            if not ok:
                notiz("        Ausgabe:", " | ".join(ausgabe.splitlines()[:6]))
        finally:
            aufraeumen(os.path.dirname(root))

    eintragen("GEGENPROBE", nummer, was, arbeit)


P = lambda root, *teile: os.path.join(root, *teile)

# --- 14: der Clientname im Kern ------------------------------------------------------
#
# Pruefung 14 gibt es seit 0.20.0 und sie hatte bis 0.57.1 KEINE Sonde - sie lag
# ausserhalb der Spanne "6 und 18 bis 47". Nach D-23 galt sie damit als nicht
# vorhanden. Wer sie aendert, baut sie nach; diese vier Einheiten holen das nach und
# belegen zugleich die Verschaerfung von D-129.
#
# Die Sonden lesen den Namen aus den Manifesten der Kopie, statt ihn zu schreiben:
# Eine Sonde, die einen Produktnamen raet, misst den geratenen Namen.
M14_NAME = "nennt ein Client-Produkt"
M14_PLATZHALTER = "traegt den Clientnamen"
M14_ANKER = "kein Client Pack mit manifest.json gefunden"
P14_WURZELQUELLE = ".koolie/core/framework/runtime/root-instruction.md".replace("/", os.sep)
P14_CHRONIK = ".koolie/core/tests/protocols/2026-09-18-sonde-14.md".replace("/", os.sep)


def _14_produktname(root: str) -> str:
    """Kapitalisierter Produktname eines Packs - aus dessen Kennung, nicht geraten."""
    base = P(root, ".koolie/core", "clients")
    for name in sorted(os.listdir(base)):
        if name.startswith("_"):
            continue
        mp = os.path.join(base, name, "manifest.json")
        if os.path.exists(mp):
            kennung = json.loads(lies(mp))["client"]
            return " ".join(w.capitalize() for w in kennung.split("-"))
    raise Praeparationsfehler(
        "Kein Client Pack mit manifest.json unter clients/ - die Sonden zu 14 leiten "
        "den Produktnamen von dort ab")


def _14_datei(root: str, name: str, inhalt: str) -> None:
    """Eine neue Prompt-Datei mit vollstaendigem Steckbrief und der Inhaltszeile."""
    schreib(P(root, (".koolie/core/prompts/" + name).replace("/", os.sep)),
            "# Sondenvorlage\r\n\r\n"
            "| Attribut | Wert |\r\n|---|---|\r\n"
            "| ID | `FW-PR-015` |\r\n| Version | `0.1.0` |\r\n"
            "| Status | `pilot` |\r\n"
            "| Owner (Rolle) | `<FRAMEWORK_OWNER>` |\r\n\r\n"
            + inhalt + "\r\n")


def _14_produktname_mit_zusatz(root: str) -> None:
    """Der Produktname MIT ZUSATZ in einem Kerntraeger - bis 0.57.0 zulaessig.

    Genau die Form, die D-28 erlaubte und die in fuenfzehn Fundstellen stand.
    """
    _14_datei(root, "15-sonde-produktname.md",
              "Zugang zu %s ist Voraussetzung fuer die Uebung." % _14_produktname(root))


def _14_blosser_name(root: str) -> None:
    """Der blosse Name als Handelnder - der Fall, den D-28 schon immer verbot.

    Sie belegt, dass die Verschaerfung den ALTEN Gegenstand nicht verloren hat: Eine
    neue Pruefung darf den Fall ihrer Vorgaengerin nicht mitnehmen.
    """
    _14_datei(root, "15-sonde-akteur.md",
              "%s entscheidet, welche Datei geoeffnet wird."
              % _14_produktname(root).split()[0])


def _14_platzhalter_mit_namen(root: str) -> None:
    """Ein Platzhalter, der den Clientnamen traegt - der Fall aus CR-2026-070.

    Der Marker stand acht Releases im Kern, weil die Akteurspruefung den
    kapitalisierten Namen sucht und der Marker ihn GROSS schreibt.
    """
    _14_datei(root, "15-sonde-platzhalter.md",
              "Stand: <VERIFY AGAINST CURRENT %s DOCUMENTATION>."
              % _14_produktname(root).split()[0].upper())


def _14_anker_verlieren(root: str) -> None:
    """Ohne manifest.json unter clients/ hat Pruefung 14 keine Namen mehr.

    Bis 0.57.1 stieg sie an dieser Stelle STILL aus (`if not namen: return`) - eine
    Pruefung, die ihren Gegenstand verliert und nichts sagt, ist nach D-23 keine.
    """
    base = P(root, ".koolie/core", "clients")
    getroffen = 0
    for name in sorted(os.listdir(base)):
        mp = os.path.join(base, name, "manifest.json")
        if os.path.exists(mp):
            os.remove(mp)
            getroffen += 1
    if not getroffen:
        raise Praeparationsfehler(
            "Kein manifest.json unter clients/ - die Ankersonde zu 14 haette nichts "
            "zu entfernen")


def _14_chronik(root: str) -> None:
    """Ein Produktname in einem Protokoll bleibt zulaessig - es berichtet eine Messung."""
    schreib(P(root, P14_CHRONIK),
            "# Sondenprotokoll\r\n\r\nDer Lauf ist gegen %s gefahren worden.\r\n"
            % _14_produktname(root))


def _14_platzhalter_gerendert(root: str) -> None:
    """<CLIENT_NAME> in einer gerenderten Quelle - der einzige Weg, der offen bleibt.

    Die Wurzel-Anweisungsdatei traegt ihn seit 0.7.0 im Titel und ist damit der einzige
    angewandte Fall im ganzen Bestand. Die Gegenprobe legt einen zweiten daneben und
    belegt, dass die verschaerfte Pruefung ihn nicht mitnimmt.
    """
    pfad = P(root, P14_WURZELQUELLE)
    schreib(pfad, lies(pfad).rstrip("\r\n")
            + "\r\n\r\nDiese Anweisung gilt fuer <CLIENT_NAME>.\r\n")


sonde("14a", "Der Produktname MIT ZUSATZ in einem Kerntraeger wird gemeldet - die "
             "Ausnahme, die D-129 abgeschafft hat", _14_produktname_mit_zusatz, M14_NAME)

sonde("14b", "Der blosse Name als Handelnder wird weiterhin gemeldet - die Verschaerfung "
             "hat den alten Gegenstand nicht verloren", _14_blosser_name, M14_NAME)

sonde("14c", "Ein Platzhalter mit Clientnamen wird gemeldet - er steht gross und entgeht "
             "der Namenssuche", _14_platzhalter_mit_namen, M14_PLATZHALTER)

sonde("14d", "Ohne manifest.json unter clients/ meldet Pruefung 14 den verlorenen "
             "Gegenstand, statt still auszusteigen", _14_anker_verlieren, M14_ANKER)

gegenprobe("14a", "Das unveraenderte Repositorium bleibt unbeanstandet - die fuenfzehn "
                  "Nennungen sind aufgeloest", None, M14_NAME)

gegenprobe("14b", "Ein Produktname in einem Protokoll bleibt zulaessig - Chronik "
                  "berichtet einen vergangenen Stand", _14_chronik, M14_NAME)

gegenprobe("14c", "<CLIENT_NAME> in einer gerenderten Quelle bleibt zulaessig - das ist "
                  "der Weg, den D-129 offen laesst", _14_platzhalter_gerendert, M14_NAME)


# --- 18: verwaister Hook-Dateiname in einer root-template-Vorlage -----------------
sonde("18b", "Verwaiste Hook-Datei als geliefertes Artefakt in der Vorlage",
      lambda r: schreib(
          P(r, ".koolie/core/clients/devin-desktop/root-template/.devin/README.md".replace("/", os.sep)),
          lies(P(r, ".koolie/core/clients/devin-desktop/root-template/.devin/README.md".replace("/", os.sep)))
          .replace("| `config.json` |", "| `hooks.v1.json` | Lebenszyklus-Hooks | `[DOK]` |\r\n| `config.json` |", 1)),
      "hooks.v1.json")

gegenprobe("18b", "Erklaerende Nennung im Fliesstext bleibt unbeanstandet", None, "FEHLER")

# --- 19: Auskunftsabschnitt ------------------------------------------------------
def _entferne_abschnitt(root: str) -> None:
    pfad = P(root, ".koolie/core/clients/devin-desktop/CLIENT_PACK.md".replace("/", os.sep))
    text = lies(pfad)
    start = text.index("## 7. Anweisungs- und Konfigurationsquellen")
    ende = text.index("## 8. Änderungsverlauf")
    schreib(pfad, text[:start] + text[ende:])


sonde("19", "Ein Pack ohne den Abschnitt ueber Anweisungs- und Konfigurationsquellen "
     "ausserhalb des Projekts wird gemeldet", _entferne_abschnitt,
      "Anweisungs- und Konfigurationsquellen außerhalb des Projekts' fehlt")


def _datum_entfernen(root: str) -> None:
    pfad = P(root, ".koolie/core/clients/claude-code/CLIENT_PACK.md".replace("/", os.sep))
    text = lies(pfad)
    start = text.index("## 8. Anweisungs- und Konfigurationsquellen")
    ende = text.index("## 9. Änderungsverlauf")
    mitte = re.sub(r"\d{4}-\d{2}-\d{2}", "neulich", text[start:ende])
    schreib(pfad, text[:start] + mitte + text[ende:])


sonde("19", "Eine Auskunft ohne Erhebungsdatum ist eine Behauptung ohne Stand und wird gemeldet", _datum_entfernen, "nennt keinen Erhebungsstand")
gegenprobe("19", "Vorlage mit <TBD>-Erhebungsstand laeuft durch", None, "Erhebungsstand")

# --- 20: Dokumenttabellen gegen Manifest -----------------------------------------
sonde("20", "Verfaelschter Wert in der Registrierungstabelle",
      lambda r: schreib(P(r, ".koolie/core/docs/PLACEHOLDER_REGISTRY.md".replace("/", os.sep)),
                        lies(P(r, ".koolie/core/docs/PLACEHOLDER_REGISTRY.md".replace("/", os.sep)))
                        .replace("| `<SKILLS_DIR>` | Skill-Ablage | `.devin/skills`",
                                 "| `<SKILLS_DIR>` | Skill-Ablage | `.devin/faehigkeiten`", 1)),
      "<SKILLS_DIR> steht fuer 'devin-desktop'")

sonde("20", "Ein verfaelschter Pfad im Laufzeitglossar weicht vom Manifest des Packs ab und "
      "wird gemeldet",
      lambda r: schreib(P(r, ".koolie/core/docs/RUNTIME_GLOSSARY.md".replace("/", os.sep)),
                        lies(P(r, ".koolie/core/docs/RUNTIME_GLOSSARY.md".replace("/", os.sep)))
                        .replace("| **Agentenprofile** | Verzeichnis der Subagentenprofile | `.devin/agents/`",
                                 "| **Agentenprofile** | Verzeichnis der Subagentenprofile | `.devin/profile/`", 1)),
      "'Agentenprofile' steht fuer 'devin-desktop'")

gegenprobe("20", "Begriff ohne Manifestfeld und eingebettete Hook-Datei bleiben unbeanstandet",
           None, "das Manifest fuehrt")

# --- 21: Hook-Skripte neutral ----------------------------------------------------
sonde("21", "Eine clientgebundene Umgebungsvariable im gemeinsamen Hook-Skript bindet es an "
      "ein Pack und wird gemeldet",
      lambda r: schreib(P(r, ".koolie/core/tests/scripts/hook-overlay-status.py".replace("/", os.sep)),
                        lies(P(r, ".koolie/core/tests/scripts/hook-overlay-status.py".replace("/", os.sep)))
                        .replace("root = argumente[0] if argumente else os.getcwd()",
                                 'root = argumente[0] if argumente else os.environ.get("DEVIN_PROJECT_DIR", os.getcwd())', 1)),
      "ist die Umgebungsvariable des Packs")

sonde("21", "Laufzeitpfad eines Packs in der Pfadbildung",
      lambda r: schreib(P(r, ".koolie/core/tests/scripts/hook-overlay-status.py".replace("/", os.sep)),
                        lies(P(r, ".koolie/core/tests/scripts/hook-overlay-status.py".replace("/", os.sep)))
                        .replace('candidates.append(os.path.join(root, ".koolie/project-overlay", "OVERLAY.md"))',
                                 'candidates.append(os.path.join(root, ".devin", "rules", "20-project-overlay.md"))', 1)),
      "Hier wird ein Pfad aus")

gegenprobe("21", "Schutzmuster in hook-check-secrets.py bleiben unbeanstandet",
           None, "hook-check-secrets.py")

# --- 22: Importsteuerung ---------------------------------------------------------
def _steuerung_verfaelschen(root: str) -> None:
    pfad = P(root, ".devin", "config.json")
    schreib(pfad, lies(pfad).replace('"windsurf": false', '"windsurf": true', 1))


sonde("22", "Ein verfaelschter Wert der Importsteuerung read_config_from weicht vom Manifest "
      "ab und wird gemeldet", _steuerung_verfaelschen,
      "die Importsteuerung 'read_config_from' steht als".replace("die ", "Die "))


def _steuerung_entfernen(root: str) -> None:
    import json
    pfad = P(root, ".devin", "config.json")
    d = json.loads(lies(pfad))
    d.pop("read_config_from", None)
    schreib(pfad, json.dumps(d, indent=2, ensure_ascii=False) + "\n")


sonde("22", "Eine fehlende Importsteuerung read_config_from laesst offen, welche fremden "
      "Konfigurationen der Client liest", _steuerung_entfernen,
      "Die Importsteuerung 'read_config_from' fehlt")

gegenprobe("22", "Pack ohne import_control laeuft durch", None, "Importsteuerung")

# --- 23: normative Schluesselwoerter im HTML-Kommentar ---------------------------
sonde("23", "Normativer Satz im Kopfkommentar der Wurzel-Anweisungsdatei",
      lambda r: schreib(P(r, ".koolie/core/framework/runtime/root-instruction.md".replace("/", os.sep)),
                        lies(P(r, ".koolie/core/framework/runtime/root-instruction.md".replace("/", os.sep)))
                        .replace("Was gilt, steht im Fließtext",
                                 "Diese Datei darf nur über den Änderungsprozess geändert werden. "
                                 "Was gilt, steht im Fließtext", 1)),
      "steht in einem HTML-Kommentar")

sonde("23", "Normatives MUSS im Kommentar einer installierten Regeldatei",
      lambda r: schreib(P(r, ".devin", "rules", "00-framework-core.md"),
                        "<!-- Herkunft: Ebene 3. Diese Regel MUSS geladen werden. -->\r\n"
                        + lies(P(r, ".devin", "rules", "00-framework-core.md"))),
      "'MUSS' steht in einem HTML-Kommentar")

gegenprobe("23", "Herkunftsangaben im Kommentar bleiben unbeanstandet", None,
           "HTML-Kommentar")

# --- 24: Nicht-Regeltexte in der Vorlage der Regelablage -------------------------
def _fremddatei(root: str) -> None:
    basis = P(root, ".koolie/core/clients/devin-desktop/root-template/.devin/rules".replace("/", os.sep))
    os.makedirs(basis, exist_ok=True)
    schreib(os.path.join(basis, "README.md"), "# Erklaerender Text\r\n")


sonde("24", "Erklaerender Text in der Vorlage der Regelablage", _fremddatei, "kein Regeltext")


def _echte_regel(root: str) -> None:
    basis = P(root, ".koolie/core/clients/devin-desktop/root-template/.devin/rules".replace("/", os.sep))
    os.makedirs(basis, exist_ok=True)
    schreib(os.path.join(basis, "40-tech-beispiel.md"), "---\r\ntrigger: glob\r\n---\r\n")


gegenprobe("24", "Regeltext nach Nummernschema bleibt unbeanstandet", _echte_regel,
           "kein Regeltext")

# --- 6 (B03, D-39): Die Inhaltspruefung meldet die Fundstelle, nicht den Wert -----
#
# Diese Sonden pruefen **zwei** Bedingungen statt einer. Die erste - der Befund wird
# gemeldet - haette auch die alte Fassung bestanden: Sie meldete ja, und zwar mitsamt dem
# gefundenen Wert. Die zweite ist die eigentliche und der Grund dieses Blocks: Der
# Markerwert darf in der gesamten Ausgabe des Laufs nicht vorkommen.
#
# Die Marker sind bewusst eindeutig gewaehlt, damit ihr Fehlen etwas bedeutet. Ein Marker,
# der auch sonst im Repositorium vorkommen koennte, wuerde die zweite Bedingung entwerten -
# man wuesste nicht, ob er aus der Sonde stammt oder von woanders.
#
# Nicht abgedeckt: der Mermaid-Fehlerpfad. Er verlangt einen fehlschlagenden Lauf des
# externen Renderers; `mmdc` ist in dieser Umgebung nicht vorhanden. Die Stelle ist
# geaendert, aber unbelegt - das ist nach D-23 ein offener Punkt, kein erledigter.

B03_ZIEL = ".koolie/core/docs/ROADMAP.md".replace("/", os.sep)
B03_MAIL = "b03messmarke@sondenlauf-b03.test"
B03_IP = "10.203.44.91"
B03_HOST = "sondenlauf-b03.internal"
B03_URL = "https://sondenlauf-b03.example.net/b03"
B03_TERM = "Sondenlauf-B03-Sperrbegriff"
B03_SECRET = "AKIAB03MESSMARKE0000"


def _b03_anhaengen(*zeilen: str):
    """Haengt Text an eine gepruefte Datei der Kopie - der Ort ist beliebig, der Wert nicht."""
    def tun(root: str) -> None:
        pfad = P(root, B03_ZIEL)
        schreib(pfad, lies(pfad) + "\r\n" + "\r\n".join(zeilen) + "\r\n")
    return tun


def _b03_term(root: str) -> None:
    """Sperrbegriff: Er muss in die Liste **und** in eine gepruefte Datei.

    Die schaerfste der sechs Kategorien. forbidden-terms.txt ist von der Inhaltspruefung
    ausgenommen, weil dort reale Namen stehen - und die Diagnose schrieb den Namen dann
    doch in die Ausgabe.
    """
    liste = P(root, ".koolie/project-overlay", "forbidden-terms.txt")
    schreib(liste, lies(liste).rstrip("\r\n") + "\r\n" + B03_TERM + "\r\n")
    _b03_anhaengen(f"Sondenzeile: {B03_TERM} steht hier absichtlich.")(root)


def sonde_ohne_wert(nummer: str, was: str, praeparieren, erwartet: str, marker: str) -> None:
    """Sonde mit doppelter Bedingung: gemeldet **und** der Wert nicht in der Ausgabe.

    Die Ausgabe wird bei einer Abweichung nur **bereinigt** gezeigt. Andernfalls truege die
    Fehlermeldung dieser Sonde den Wert weiter, den die Sonde gerade als weitergetragen
    beanstandet - derselbe Fehler eine Ebene hoeher.
    """
    def arbeit() -> None:
        root = kopie()
        try:
            vorher = baumhash(root)
            try:
                praeparieren(root)
            except Praeparationsfehler as exc:
                melde("SONDE", nummer, False, was + "  [Praeparation gebrochen]")
                notiz("        " + str(exc))
                return
            if baumhash(root) == vorher:
                melde("SONDE", nummer, False, was + "  [nichts praepariert]")
                return
            ausgabe = lauf(root)
            gemeldet = erwartet in ausgabe
            verschwiegen = marker not in ausgabe
            melde("SONDE", nummer, gemeldet and verschwiegen, was)
            if not gemeldet:
                bereinigt = ausgabe.replace(marker, "<Marker entfernt>")
                notiz("        Befund nicht gemeldet. Ausgabe:",
                      " | ".join(bereinigt.splitlines()[:6]))
            if not verschwiegen:
                notiz(f"        Der Markerwert steht in der Ausgabe - das ist B03 selbst. "
                      f"Erwartete Kennung: {erwartet}")
        finally:
            aufraeumen(os.path.dirname(root))

    eintragen("SONDE", nummer, was, arbeit)


sonde_ohne_wert("6", "E-Mail-Adresse: gemeldet, Wert nicht ausgegeben",
                _b03_anhaengen(f"Sondenzeile: {B03_MAIL}"),
                "FW-CONTENT-EMAIL", B03_MAIL)

sonde_ohne_wert("6", "IP-Adresse: gemeldet, Wert nicht ausgegeben",
                _b03_anhaengen(f"Sondenzeile: {B03_IP}"),
                "FW-CONTENT-IP", B03_IP)

sonde_ohne_wert("6", "Interner Hostname: gemeldet, Wert nicht ausgegeben",
                _b03_anhaengen(f"Sondenzeile: {B03_HOST}"),
                "FW-CONTENT-HOST", B03_HOST)

sonde_ohne_wert("6", "URL ausserhalb der Allowlist: gemeldet, Wert nicht ausgegeben",
                _b03_anhaengen(f"Sondenzeile: {B03_URL}"),
                "FW-CONTENT-URL", B03_URL)

sonde_ohne_wert("6", "Gesperrter Begriff: gemeldet, Begriff nicht ausgegeben",
                _b03_term, "FW-CONTENT-TERM", B03_TERM)

sonde_ohne_wert("6", "Secret-Muster: gemeldet mit Fundstelle, Wert nicht ausgegeben",
                _b03_anhaengen(f"Sondenzeile: {B03_SECRET}"),
                "FW-CONTENT-SECRET", B03_SECRET)


def _b03_erlaubte_faelle(root: str) -> None:
    """Die Gegenprobe: dieselben Kategorien in ihrer erlaubten Gestalt.

    Ohne sie belegt der Block nur, dass die Pruefung meldet - nicht, dass sie das Richtige
    meldet. Eine Pruefung, die jede Adresse beanstandet, besteht alle sechs Sonden oben.
    """
    _b03_anhaengen(
        "Gegenprobe: kontakt@example.com ist eine Dokumentationsadresse.",
        "Gegenprobe: 203.0.113.7 stammt aus dem Dokumentationsbereich.",
        "Gegenprobe: https://docs.devin.ai/ steht auf der Allowlist.",
    )(root)


gegenprobe("6", "Dokumentationsadresse, Dokumentations-IP und Allowlist-URL bleiben unbeanstandet",
           _b03_erlaubte_faelle, "FW-CONTENT-")


def _gitignore_beilage(root: str) -> None:
    """Eine ignorierte Datei mit einem Befund - und eine gleichartige daneben.

    🔴 Der Gegenstand von D-215: Was die `.gitignore` als einfachen Dateinamen
    fuehrt, ist nicht eingecheckt und damit kein Bestandteil des Repositoriums.
    Gemessen am 2026-09-20 an der lokalen Beilage der Uebergabe, die Servername
    und Konto traegt und deshalb ueberhaupt existiert.
    """
    gi = os.path.join(root, ".gitignore")
    alt = io.open(gi, encoding="utf-8", newline="").read()
    daten = (alt.rstrip("\r\n") + "\r\nPROBE-IGNORIERT.md\r\n").encode("utf-8")
    io.open(gi, "wb").write(daten)
    # Die ignorierte Datei traegt einen Befund, der ohne D-215 gemeldet wuerde.
    inhalt = ("# Probe\r\n\r\nServer: 10.11.12.13\r\n").encode("utf-8")
    io.open(os.path.join(root, "PROBE-IGNORIERT.md"), "wb").write(inhalt)


def _gitignore_nicht_gefuehrt(root: str) -> None:
    """Dieselbe Datei unter einem Namen, den die .gitignore NICHT fuehrt."""
    inhalt = ("# Probe\r\n\r\nServer: 10.11.12.13\r\n").encode("utf-8")
    io.open(os.path.join(root, "PROBE-GEFUEHRT.md"), "wb").write(inhalt)


sonde("6i", "Eine NICHT ignorierte Datei mit IP-Adresse wird weiter gemeldet",
      _gitignore_nicht_gefuehrt, "FW-CONTENT-IP")
gegenprobe("6i", "Eine in der .gitignore gefuehrte Datei wird uebersprungen "
                 "(D-215)",
           _gitignore_beilage, "FW-CONTENT-IP")

def sonde_hook_zusatzmuster() -> None:
    """Dieselbe Regel im ausgelieferten Hook - ohne Validatorlauf, weil keiner noetig ist.

    Ein ungueltiges Zusatzmuster wurde bis 0.26.0 mitsamt seinem Wert nach stderr
    geschrieben. Projektspezifische Pfadmuster tragen Projekt-, Kunden- und Hostnamen.
    """
    marker = "b03hookmarke.internal"
    umgebung = dict(os.environ, FW_HOOK_EXTRA_PATH_PATTERNS=marker + "/[")
    p = unterprozess(
        [sys.executable, os.path.join(QUELLE, ".koolie/core", "tests", "scripts",
                                      "hook-check-secrets.py")],
        input='{"tool_name": "Read", "tool_input": {"file_path": "beispiel.txt"}}',
        env=umgebung)
    ausgabe = (p.stdout or "") + (p.stderr or "")
    gemeldet = "Ungueltiges Zusatzmuster an Position 1" in ausgabe
    verschwiegen = marker not in ausgabe
    melde("SONDE", "6h", gemeldet and verschwiegen,
          "Hook: ungueltiges Zusatzmuster gemeldet, Wert nicht ausgegeben")
    if not gemeldet:
        notiz("        Meldung fehlt. Ausgabe:",
              " | ".join(ausgabe.replace(marker, "<Marker entfernt>").splitlines()[:4]))
    if not verschwiegen:
        notiz("        Der Markerwert steht in der Ausgabe - das ist B03 im Hook.")


buendel(sonde_hook_zusatzmuster,
        "Der ausgelieferte Hook meldet ein ungueltiges Zusatzmuster, ohne dessen Wert "
        "auszugeben - projektspezifische Pfadmuster tragen Projekt-, Kunden- und Hostnamen")


# --- 25 (D-41): Ein Ausfall ohne benannten Ersatz -------------------------------
#
# Die Sonde nimmt der S5-Zeile das Wort, auf das die Pruefung sieht. Das ist die ganze
# Bauart der Pruefung - sie kann nicht beurteilen, ob ein Ersatz taugt, nur dass jemand
# die Frage beantwortet hat.

def _b40_ersatz_entfernen(root: str) -> None:
    pfad = P(root, ".koolie/core/clients/claude-code/CLIENT_PACK.md".replace("/", os.sep))
    schreib(pfad, lies(pfad).replace("Ersatz", "Behelf"))


sonde("25", "Zeile auf [NICHT ABBILDBAR] ohne benannten Ersatz",
      _b40_ersatz_entfernen, "Zeile S5 steht auf [NICHT ABBILDBAR]")

# Die Zusammenfassungstabelle desselben Dokuments fuehrt dieselbe Klasse als
# Zeilenbeschriftung und nennt keinen Ersatz. Eine Pruefung, die jede Zeile mit der Klasse
# meldet, beanstandet sie - und besteht die Sonde darueber trotzdem.
gegenprobe("25", "Klassenzeile der Zusammenfassungstabelle bleibt unbeanstandet",
           None, "steht auf [NICHT ABBILDBAR]")


# --- E3 (D-42): install.py --list-skills -----------------------------------------
#
# Kein Validatorlauf: Der Gegenstand ist ein Kommando, kein Artefakt. Gemessen wird an
# seiner Ausgabe.

def sonde_list_skills() -> None:
    """Wirkungsnachweis fuer den Ersatz, den D-42 an die Stelle der Clientauskunft setzt.

    Drei Bedingungen, und die dritte ist die, an der dieses Projekt seine Befunde findet:
    Eine Teilauskunft, die ihre Grenze nicht nennt, verspricht mehr, als sie leistet.
    """
    root = kopie()
    try:
        ablage = P(root, ".devin", "skills")
        # Sonde: ein Skill, den keine Kernquelle liefert - Herkunft muss 'Projekt' sein.
        os.makedirs(os.path.join(ablage, "sonde-d41-projektskill"), exist_ok=True)
        schreib(os.path.join(ablage, "sonde-d41-projektskill", "SKILL.md"),
                "---\r\nname: sonde-d41-projektskill\r\ntriggers:\r\n  - user\r\n---\r\n")
        # Gegenprobe: ein Verzeichnis ohne SKILL.md ist kein Skill.
        os.makedirs(os.path.join(ablage, "sonde-d41-kein-skill"), exist_ok=True)

        p = unterprozess([sys.executable, os.path.join(root, ".koolie/core", "install.py"),
                          "--client", "devin-desktop", "--root", root, "--list-skills"])
        ausgabe = (p.stdout or "") + (p.stderr or "")

        gefuehrt = "sonde-d41-projektskill" in ausgabe
        herkunft = bool(re.search(r"sonde-d41-projektskill\s+Projekt\s+nur Nutzer", ausgabe))
        melde("SONDE", "D41", gefuehrt and herkunft,
              "Skill ohne Kernquelle: gefuehrt, Herkunft 'Projekt', Aufrufbarkeit gelesen")
        if not (gefuehrt and herkunft):
            notiz("        Ausgabe:", " | ".join(ausgabe.splitlines()[:8]))

        melde("GEGENPROBE", "D41", "sonde-d41-kein-skill" not in ausgabe,
              "Verzeichnis ohne SKILL.md wird nicht als Skill gefuehrt")

        melde("SONDE", "D41", "kein vollstaendiger Ersatz" in ausgabe,
              "Die Auskunft nennt ihre eigene Grenze in der Ausgabe")
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonde_list_skills,
        "Die Skillauskunft von install.py fuehrt einen Projektskill mit richtiger Herkunft, "
        "uebergeht ein Verzeichnis ohne SKILL.md und nennt ihre eigene Grenze")


# --- strict-overlay (D-44): Aktivierungspruefung, dieselben Faelle je Pack --------
#
# Diese Sonden brauchen eine **Installation**, keine Kopie des Repositoriums: Die
# Aktivierungspruefung liest die Laufzeitschicht eines Projekts. Das macht sie teurer als
# alle uebrigen - und es ist der Grund, warum der Befund so lange unbemerkt blieb. Eine
# Sonde, die nur im Repositorium laeuft, kann ihn nicht finden.
#
# Der Kern des Nachweises ist die Wiederholung je Pack. B02 war nicht, dass eine Pruefung
# falsch prueft, sondern dass sie **einen Client gar nicht sieht**. Das faellt nur auf, wenn
# derselbe Fall in jeder Installation laeuft.

SO_STATUSFORMEN = (
    (re.compile(r"^(\|\s*Overlay-Status\s*\|\s*)`?[^`|]+`?", re.M), r"\1`{}`"),
    (re.compile(r"^(-\s*Overlay-Status:\s*)`?[^`\n]+`?", re.M), r"\1`{}`"),
)
SO_PLATZHALTER = re.compile(r"<[A-Z][A-Z0-9_]{2,}>|<TBD[^>]*>")


def installation(pack: str) -> str:
    """Frische Installation eines Packs samt Kern - das Ziel der Aktivierungspruefung."""
    ziel = tempfile.mkdtemp(prefix="lw-inst-")
    root = os.path.join(ziel, "projekt")
    os.makedirs(root)
    unterprozess([sys.executable, os.path.join(QUELLE, ".koolie/core", "install.py"),
                  "--client", pack, "--root", root])
    shutil.copytree(os.path.join(QUELLE, ".koolie/core"),
                    os.path.join(root, ".koolie/core"),
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "out"))
    return root


def strict_ausgabe(root: str) -> str:
    """Ausgabe der Aktivierungspruefung.

    Die Kodierung besorgt unterprozess(); dort steht auch, warum sie noetig ist.
    """
    p = unterprozess([sys.executable, os.path.join(root, *VALIDATOR.split("/")),
                      "--root", root, "--strict-overlay"])
    return (p.stdout or "") + (p.stderr or "")



def validator_ausgabe(root: str) -> str:
    """Ausgabe eines gewoehnlichen Validatorlaufs gegen eine Installation."""
    p = unterprozess([sys.executable, os.path.join(root, *VALIDATOR.split("/")),
                      "--root", root])
    return (p.stdout or "") + (p.stderr or "")


def _so_status(pfad: str, wert: str) -> None:
    t = lies(pfad)
    for muster, ersatz in SO_STATUSFORMEN:
        t = muster.sub(ersatz.format(wert), t)
    schreib(pfad, t)


def sonden_aktivierungspruefung() -> None:
    """Dieselben Faelle in jeder Installation (B02, D-44)."""
    for pack in ("claude-code", "devin-desktop"):
        root = installation(pack)
        try:
            man = json.loads(lies(os.path.join(QUELLE, ".koolie/core", "clients", pack,
                                               "manifest.json")))
            regel = os.path.join(root, *man["pack_runtime_dir"].split("/"),
                                 "20-project-overlay.md")
            rechte = os.path.join(root, *man["permissions_file"].split("/"))
            overlay = os.path.join(root, ".koolie/project-overlay", "OVERLAY.md")

            # --- Status: 'aktiv' ist aktiv, alles andere nicht ---------------------
            for pfad in (regel, overlay):
                _so_status(pfad, "aktiv")
            aus = strict_ausgabe(root)
            melde("GEGENPROBE", "SO", "Overlay-Status ist nicht" not in aus,
                  f"Status 'aktiv' bleibt unbeanstandet ({pack})")

            # 'aktivierung-ausstehend' bestand bis 0.27.0 die Pruefung - der Vergleich
            # war ein Praefixvergleich. Ein Wert, der sagt, dass die Aktivierung
            # aussteht, liess den Fehler sogar verschwinden.
            _so_status(regel, "aktivierung-ausstehend")
            aus = strict_ausgabe(root)
            melde("SONDE", "SO", "sondern 'aktivierung-ausstehend'" in aus,
                  f"Status 'aktivierung-ausstehend' wird gemeldet ({pack})")
            _so_status(regel, "aktiv")

            # --- Berechtigungsdatei: Platzhalter ------------------------------------
            schreib(rechte, SO_PLATZHALTER.sub("platzhalterfrei", lies(rechte)))
            aus = strict_ausgabe(root)
            melde("GEGENPROBE", "SO", "enthält noch Platzhalter" not in aus,
                  f"Bereinigte Berechtigungsdatei bleibt unbeanstandet ({pack})")

            ersetze(rechte,
                    ('"permissions"',
                     '"_sonde": "<TBD: offen>",\r\n  "permissions"'))
            aus = strict_ausgabe(root)
            melde("SONDE", "SO", "enthält noch Platzhalter" in aus,
                  f"Platzhalter in der Berechtigungsdatei wird gemeldet ({pack})")

            # --- Fehlender sicherheitsrelevanter Abschnitt ---------------------------
            # Bis 0.27.0 stand ein Overlay ohne Abschnitt 13 besser da als eines mit
            # einem offenen Wert darin: Die Pruefung sah nur in vorhandene Abschnitte.
            t = lies(overlay)
            start = t.index("## 13.")
            ende = t.index("## 14.")
            schreib(overlay, t[:start] + t[ende:])
            aus = strict_ausgabe(root)
            melde("SONDE", "SO", "Abschnitt ## 13. fehlt" in aus,
                  f"Fehlender sicherheitsrelevanter Abschnitt wird gemeldet ({pack})")
        finally:
            aufraeumen(os.path.dirname(root))


buendel(sonden_aktivierungspruefung,
        "Die Aktivierungspruefung gegen je eine frische Installation beider Packs: "
        "Overlay-Status, Platzhalter in der Berechtigungsdatei, fehlender Abschnitt 13")


# --- B10 (D-45): Die Aktualisierung trifft das installierte Pack -----------------
#
# Kein Validatorlauf: Der Gegenstand ist das Installationswerkzeug. Gemessen wird an dem,
# was es anlegt - und vor allem an dem, was es **nicht** anlegt.
#
# Die Gegenprobe ist hier die wichtigere Haelfte. Dass eine Aktualisierung das richtige
# Pack trifft, sagt noch nicht, dass ein falsches abgewiesen wird; bis 0.27.0 wurde es
# stillschweigend ausgefuehrt und legte 60 Dateien an.

def sonden_clientwahl() -> None:
    """Wirkungsnachweis fuer die Erkennung des installierten Packs (B10, D-45)."""
    fremde_schicht = {"claude-code": ".devin", "devin-desktop": ".claude"}
    for pack, fremd in fremde_schicht.items():
        root = installation(pack)
        try:
            werkzeug = os.path.join(root, ".koolie/core", "install.py")

            p = unterprozess([sys.executable, werkzeug, "--update", "--root", root])
            aus = (p.stdout or "") + (p.stderr or "")
            getroffen = f"Client:  {pack}" in aus
            keine_zweite = not os.path.isdir(os.path.join(root, fremd))
            melde("SONDE", "B10", getroffen and keine_zweite,
                  f"Aktualisierung ohne --client trifft das installierte Pack ({pack})")
            if not (getroffen and keine_zweite):
                notiz("        Ausgabe:", " | ".join(aus.splitlines()[:6]))

            anderes = "devin-desktop" if pack == "claude-code" else "claude-code"
            q = unterprozess([sys.executable, werkzeug, "--update", "--root", root,
                              "--client", anderes])
            abgewiesen = q.returncode == 1
            unberuehrt = not os.path.isdir(os.path.join(root, fremd))
            melde("GEGENPROBE", "B10", abgewiesen and unberuehrt,
                  f"Widersprechendes --client bricht ab statt anzulegen ({pack} statt {anderes})")
        finally:
            aufraeumen(os.path.dirname(root))


buendel(sonden_clientwahl,
        "Die Aktualisierung erkennt das installierte Pack und weist ein fremdes ab, ohne "
        "dabei eine einzige Datei anzulegen")


# --- D-46: Die Erstinstallation ueberschreibt keine Projektdatei -----------------
#
# Die Sonde braucht weder Repositoriumskopie noch Installation, sondern ein leeres
# Verzeichnis mit **einer** fremden Datei darin. Das ist der Fall, den ein aufnehmendes
# Projekt mitbringt - und bis 0.28.0 verlor es sie beim ersten Befehl des Leitfadens.
#
# Doppelte Bedingung, und die zweite ist die eigentliche: Ein Abbruch, der erst nach dem
# Schreiben kommt, ist keiner.

def sonden_erstinstallation() -> None:
    """Wirkungsnachweis fuer den Schutz der Projektdateien (CR-2026-046, D-46)."""
    ziel = tempfile.mkdtemp(prefix="lw-erst-")
    werkzeug = os.path.join(QUELLE, ".koolie/core", "install.py")
    man = json.loads(lies(os.path.join(QUELLE, ".koolie/core", "clients", "claude-code",
                                       "manifest.json")))
    wurzeldatei = man["root_instruction_file"]
    try:
        # --- Sonde: der Name ist belegt, der Inhalt gehoert dem Projekt ----------
        projekt = os.path.join(ziel, "belegt")
        os.makedirs(projekt)
        eigen = os.path.join(projekt, wurzeldatei)
        inhalt = ("# Projektwissen\r\n\r\nDiese Datei gehoert dem Projekt und darf bei einer\r\n"
                  "Erstinstallation nicht verlorengehen.\r\n")
        schreib(eigen, inhalt)

        p = unterprozess([sys.executable, werkzeug, "--client", "claude-code",
                          "--root", projekt])
        abgebrochen = p.returncode == 1
        unberuehrt = lies(eigen) == inhalt
        nichts_geschrieben = not os.path.isdir(os.path.join(projekt, man["runtime_dir"]))
        melde("SONDE", "D46", abgebrochen and unberuehrt and nichts_geschrieben,
              "Erstinstallation bricht ab, Projektdatei und Verzeichnis unberuehrt")
        if not unberuehrt:
            notiz("        Die Projektdatei wurde veraendert - das ist der Befund selbst.")
        elif not (abgebrochen and nichts_geschrieben):
            notiz("        Ausgabe:", " | ".join(
                ((p.stdout or "") + (p.stderr or "")).splitlines()[:6]))

        # --- Gegenprobe: ein freies Verzeichnis laeuft durch ---------------------
        # Ohne sie belegt die Sonde nur, dass etwas abbricht - nicht, dass die
        # Erstinstallation ueberhaupt noch funktioniert.
        leer = os.path.join(ziel, "leer")
        os.makedirs(leer)
        q = unterprozess([sys.executable, werkzeug, "--client", "claude-code",
                          "--root", leer])
        melde("GEGENPROBE", "D46",
              q.returncode == 0 and os.path.isfile(os.path.join(leer, wurzeldatei)),
              "Erstinstallation in ein freies Verzeichnis laeuft durch")
    finally:
        aufraeumen(ziel)


buendel(sonden_erstinstallation,
        "Die Erstinstallation bricht vor einer vorhandenen Projektdatei ab, statt sie zu "
        "ueberschreiben - und schreibt dabei nichts")


# --- D-349/D-352: die Auskunft ueber ignorierte Kerndateien -----------------------
#
# 🔴 DIE AUSKUNFT AUS 1.4.0 HATTE KEINE SONDE, UND SIE ZAEHLTE UNTER WINDOWS ZU WENIG.
# `ignorierte_kerndateien()` gab die Pfade mit `text=True` an `git check-ignore --stdin`;
# unter Windows kam jeder mit angehaengtem `\r` an. Ein Verzeichnismuster (`build/`)
# traf trotzdem - der Fall, an dem die Auskunft gebaut wurde -, ein DATEImuster (`*.md`)
# nie. Gemessen am 2026-09-24: git meldet zwei ignorierte Dateien, die Funktion null
# (CR-2026-135).
#
# DREI EINHEITEN, JEDE MIT EINER UNABHAENGIG GEZAEHLTEN ERWARTUNG. Die Zahl im Hinweis
# wird gegen einen `os.walk` ueber den Kern gehalten, nicht gegen eine gepflegte Zahl:
#   D349  (Sonde)      - `*.md`: jede Markdown-Datei des Kerns wird gezaehlt. Gegen den
#                        Vorstand faellt sie unter Windows mit 0.
#   D349a (Gegenprobe) - `build/`: das Verzeichnismuster, der Anlassfall von K-117,
#                        zaehlt weiter genau die Dateien unter `build/`.
#   D349b (Gegenprobe) - ein Muster, das nichts trifft: kein Hinweis. Eine Auskunft,
#                        die immer etwas meldet, besteht jede Sonde.
M349_HINWEIS = re.compile(r"HINWEIS \((\d+)\): Dieses Projekt IGNORIERT Kerndateien")


def _349_kern(root: str, passt) -> int:
    """Die Kerndateien, die ein Muster treffen sollte - gezaehlt, nicht gepflegt."""
    kern = os.path.join(root, ".koolie", "core")
    n = 0
    for dirpath, dirnames, filenames in os.walk(kern):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in filenames:
            rel = os.path.relpath(os.path.join(dirpath, fn), kern).replace(os.sep, "/")
            n += 1 if passt(rel) else 0
    return n


def sonden_ignorierte_kerndateien() -> None:
    """Wirkungsnachweis fuer die Auskunft aus D-349 an einem echten Repositorium."""
    root = installation("claude-code")
    try:
        if unterprozess(["git", "init", "-q", root]).returncode != 0:
            melde("BUENDEL", "-", False,
                  "sonden_ignorierte_kerndateien  [git nicht erreichbar]")
            notiz("        Ohne git gibt die Auskunft bewusst nichts aus - nicht messbar.")
            return
        werkzeug = os.path.join(root, ".koolie", "core", "install.py")
        faelle = (
            ("SONDE", "D349", "*.md", lambda rel: rel.endswith(".md"),
             "Ein Dateimuster im Projekt-.gitignore wird gezaehlt - jede Markdown-Datei "
             "des Kerns, auch unter Windows"),
            ("GEGENPROBE", "D349a", "build/", lambda rel: rel.startswith("build/"),
             "Ein Verzeichnismuster zaehlt weiter genau die Dateien darunter - der "
             "Anlassfall der Auskunft bleibt erhalten"),
            ("GEGENPROBE", "D349b", "*.sonde-trifft-nichts", lambda rel: False,
             "Ein Muster, das keine Kerndatei trifft, erzeugt keinen Hinweis"),
        )
        for art, kennung, muster, passt, was in faelle:
            schreib(os.path.join(root, ".gitignore"), muster + "\n")
            p = unterprozess([sys.executable, werkzeug, "--update", "--root", root])
            aus = (p.stdout or "") + (p.stderr or "")
            soll = _349_kern(root, passt)
            treffer = M349_HINWEIS.search(aus)
            ist = int(treffer.group(1)) if treffer else 0
            melde(art, kennung, p.returncode == 0 and ist == soll, was)
            if p.returncode != 0 or ist != soll:
                notiz("        Muster %s: gemeldet %d, gezaehlt %d, Exit %d"
                      % (muster, ist, soll, p.returncode))
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_ignorierte_kerndateien,
        "Die Auskunft ueber ignorierte Kerndateien zaehlt Datei- und Verzeichnismuster "
        "richtig und schweigt, wenn nichts ignoriert wird")


# --- D-354: das Kennzeichen des Quellrepositoriums in einem Projekt ---------------
#
# 🔴 WER GANZ `.koolie/` KOPIERT, NIMMT DAS KENNZEICHEN MIT - aus dem Arbeitsbaum wie
# aus dem Release-Archiv, denn es ist versioniert. Danach haelt der Validator das
# Projekt fuer das Quellrepositorium, und keine seiner Meldungen nennt den Grund.
# Gemessen am 2026-09-24 (CR-2026-137): unverfolgt 1 Fehler (Pruefung 79, Lizenz in
# der Projektwurzel), committet 80 (dazu Pruefung 81 an 79 Projekttraegern).
#
# ZWEI EINHEITEN, UND DIE SONDE HAELT ZWEI STELLEN GEGENEINANDER. `install.py` und der
# Validator fuehren den Pfad des Kennzeichens je fuer sich; die Sonde verlangt, dass an
# derselben Datei BEIDE anschlagen - die Auskunft und Pruefung 79. Wandert eine der
# beiden Konstanten, faellt sie.
#   D354  (Sonde)      - Kennzeichen liegt: Hinweis, Exit 0, und Pruefung 79 verlangt
#                        die Lizenz in der Wurzel. Gegen den Vorstand faellt sie.
#   D354a (Gegenprobe) - ohne Kennzeichen: kein Hinweis und keine Lizenzmeldung. Eine
#                        Auskunft, die immer etwas meldet, besteht jede Sonde.
M354_HINWEIS = "das Kennzeichen des Framework-Repositoriums selbst"
M354_VALIDATOR = "LICENSE: fehlt"


def sonden_kennzeichen_im_projekt() -> None:
    """Wirkungsnachweis fuer die Auskunft aus D-354 an einer echten Installation."""
    root = installation("claude-code")
    try:
        werkzeug = os.path.join(root, ".koolie", "core", "install.py")
        kennzeichen = os.path.join(root, ".koolie", "QUELLREPOSITORIUM.md")
        faelle = (
            ("SONDE", "D354", True,
             "Ein mitkopiertes Kennzeichen wird gemeldet, ohne die Installation "
             "anzuhalten - und der Validator erkennt dieselbe Datei"),
            ("GEGENPROBE", "D354a", False,
             "Ohne Kennzeichen kein Hinweis, und der Validator prueft als Projekt"),
        )
        for art, kennung, liegt, was in faelle:
            if liegt:
                shutil.copyfile(os.path.join(QUELLE, ".koolie", "QUELLREPOSITORIUM.md"),
                                kennzeichen)
            elif os.path.exists(kennzeichen):
                os.remove(kennzeichen)
            p = unterprozess([sys.executable, werkzeug, "--update", "--root", root])
            aus = (p.stdout or "") + (p.stderr or "")
            hinweis = M354_HINWEIS in aus
            validator = M354_VALIDATOR in validator_ausgabe(root)
            ok = p.returncode == 0 and hinweis == liegt and validator == liegt
            melde(art, kennung, ok, was)
            if not ok:
                notiz("        Exit %d, Hinweis %s, Pruefung 79 %s (erwartet je %s)"
                      % (p.returncode, hinweis, validator, liegt))
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_kennzeichen_im_projekt,
        "Ein mitkopiertes Kennzeichen des Quellrepositoriums wird bei der Installation "
        "gemeldet, und install.py und Validator erkennen es an derselben Stelle")


# --- D-395: die Schritte nach Installation und Hebung je Pack (K-123) -------------
#
# 🔴 BEI `openai-codex` TRAEGT OHNE VERTRAUEN NICHTS VON ABSCHNITT B, UND DER HOOK
# BRAUCHT NACH JEDER HEBUNG NEUES VERTRAUEN - und `install.py` nannte keins von beidem.
# Seine Schritte waren packneutral und verlangten dazu, `_core_rules_integrity` stehen
# zu lassen, einen Block, den die TOML-Datei dieses Packs nicht fuehrt. Jetzt nennt das
# Manifest die Schritte (post_install_steps, post_update_steps), und den Integritaetsblock
# nennt das Werkzeug nur bei einer Berechtigungsdatei im JSON-Format.
#   D395  (Sonde)      - openai-codex: Installation nennt das Projekt- und das
#                        Hook-Vertrauen und nicht den Integritaetsblock; die Hebung
#                        nennt das erneute Hook-Vertrauen. Gegen den Vorstand faellt sie.
#   D395a (Gegenprobe) - claude-code: Integritaetsblock genannt, kein Vertrauensschritt,
#                        kein Zusatzblock bei der Hebung. Ein Werkzeug, das jedem Pack
#                        die Schritte eines Packs nennt, besteht die Sonde auch.
M395_INSTALL = "als vertraut eintragen"
M395_HOOK = "Dem Schutz-Hook einzeln vertrauen"
M395_UPDATE = "Dem Schutz-Hook ERNEUT vertrauen"
M395_BLOCK = "_core_rules_integrity"


def sonden_schritte_je_pack() -> None:
    """Wirkungsnachweis fuer die packeigenen Schritte aus D-395 an echten Installationen."""
    faelle = (
        ("SONDE", "D395", "openai-codex", True,
         "openai-codex: Installation und Hebung nennen die Vertrauensschritte, "
         "nicht den Integritaetsblock"),
        ("GEGENPROBE", "D395a", "claude-code", False,
         "claude-code: der Integritaetsblock wird genannt, kein Vertrauensschritt"),
    )
    werkzeug = os.path.join(QUELLE, ".koolie", "core", "install.py")
    for art, kennung, pack, codex, was in faelle:
        ziel = tempfile.mkdtemp(prefix="lw-inst-")
        root = os.path.join(ziel, "projekt")
        os.makedirs(root)
        try:
            p = unterprozess([sys.executable, werkzeug, "--client", pack, "--root", root])
            ein = (p.stdout or "") + (p.stderr or "")
            q = unterprozess([sys.executable, werkzeug, "--update", "--root", root])
            heb = (q.stdout or "") + (q.stderr or "")
            ist = (M395_INSTALL in ein, M395_HOOK in ein, M395_BLOCK in ein,
                   M395_UPDATE in heb)
            soll = (codex, codex, not codex, codex)
            ok = p.returncode == 0 and q.returncode == 0 and ist == soll
            melde(art, kennung, ok, was)
            if not ok:
                notiz("        Exit %d/%d, (Projekt, Hook, Block, erneut) = %s, erwartet %s"
                      % (p.returncode, q.returncode, ist, soll))
        finally:
            aufraeumen(ziel)


buendel(sonden_schritte_je_pack,
        "install.py nennt nach Installation und Hebung die Schritte, die das Manifest "
        "des Packs fuehrt, und den Integritaetsblock nur, wo es ihn gibt")


# --- D-398: der Mermaid-Renderer scheitert an der Umgebung, nicht am Diagramm (K-145) --
#
# 🔴 OHNE DEN BROWSER VON PUPPETEER MELDETE `--mermaid` JEDEN BLOCK ALS UNGUELTIG - auch
# unveraenderte -, waehrend der Bau im selben Arbeitsgang alle Diagramme renderte. Der
# Validator nimmt jetzt Browser und Konfiguration des Baus (`mermaid_renderer.py`) und
# erkennt an der Fehlerausgabe, ob der Renderer an der Umgebung gescheitert ist; dann
# warnt er einmal, statt ueber die Diagramme zu urteilen. Den Renderer selbst ruft keine
# Sonde auf - er ist eine Vorbedingung des Arbeitsplatzes, und eine Sonde, die an ihm
# haengt, bestuende auf einem Arbeitsplatz und fiele auf dem naechsten. Gemessen wird die
# Unterscheidung und die Verdrahtung.
#   D398  (Sonde)      - die Meldung, mit der der Renderer am 2026-09-25 ohne Browser
#                        scheiterte, gilt als Umgebungsfehler, und der Validator ruft
#                        den Renderer mit der Konfiguration aus diesem Modul auf.
#   D398a (Gegenprobe) - ein Syntaxfehler des Diagramms gilt NICHT als Umgebungsfehler:
#                        Eine Unterscheidung, die alles zur Umgebung erklaert, machte aus
#                        der Pruefung eine Warnung, die nie mehr einen Fehler meldet.
M398_UMGEBUNG = ("Error: Could not find chrome-headless-shell (ver. 153.0.8010.36). "
                 "This can occur if either")
M398_SYNTAX = ("Error: Parse error on line 2: ...t TD  A[Start --> B{{{ "
               "Expecting 'SQE', 'DOUBLECIRCLEEND', 'PE', got 'DIAMOND_START'")


def sonden_mermaid_umgebung() -> None:
    """Wirkungsnachweis fuer die Unterscheidung aus D-398, ohne den Renderer."""
    skripte = os.path.join(QUELLE, ".koolie", "core", "tests", "scripts")
    code = ("import sys; sys.path.insert(0, sys.argv[1]); import mermaid_renderer as m; "
            "print(m.ist_umgebungsfehler(sys.argv[2]), m.ist_umgebungsfehler(sys.argv[3]))")
    p = unterprozess([sys.executable, "-c", code, skripte, M398_UMGEBUNG, M398_SYNTAX])
    ist = (p.stdout or "").split()
    validator = lies(os.path.join(skripte, "validate-framework.py"))
    verdrahtet = ("mermaid_renderer.puppeteer_konfiguration(" in validator
                  and '"-p", pptr' in validator)
    ok = p.returncode == 0 and ist[:1] == ["True"] and verdrahtet
    melde("SONDE", "D398", ok,
          "Die Meldung ohne Browser gilt als Umgebungsfehler, und der Validator "
          "uebergibt die Konfiguration des Baus")
    if not ok:
        notiz("        Exit %d, Ausgabe %r, verdrahtet %s" % (p.returncode, ist, verdrahtet))
    ok = p.returncode == 0 and ist[1:2] == ["False"]
    melde("GEGENPROBE", "D398a", ok,
          "Ein Syntaxfehler des Diagramms bleibt ein Fehler des Diagramms")
    if not ok:
        notiz("        Exit %d, Ausgabe %r" % (p.returncode, ist))


buendel(sonden_mermaid_umgebung,
        "--mermaid unterscheidet einen Renderer ohne Browser von einem ungueltigen "
        "Diagramm und ruft ihn wie der Bau auf")


# --- D-407: der Messapparat findet den Kern unter `.koolie/core` (K-154) ----------------
#
# 🔴 SEIT DER UMBENENNUNG (0.88.0) WAR DER MESSAPPARAT AN DREI STELLEN GEBROCHEN, UND ES
# FIEL ERST IM NACHLAUF VON 1.11.0 AUF. `validate-output.py` und `mcp-waechter.py`
# suchten das Kernverzeichnis EINE Ebene unter der Wurzel und meldeten in jedem
# installierten Baum, es gebe keines; `cc-overlay-fuellen.py` entfaltete den Schlitz
# `Edit(<READ_ONLY_PATHS>)` nicht, den der Kern seit 1.5.0 fuehrt, und brach ab.
#   D407  (Sonde)      - an einer echten claude-code-Installation mit dem Kern unter
#                        `.koolie/core` finden beide Werkzeuge Pack und Skill.
#   D407a (Gegenprobe) - ohne Kern erfinden sie keinen: dieselbe Meldung wie bisher.
#   D407b (Sonde)      - der Abgleich zwischen den Platzhaltern der erzeugten
#                        Berechtigungsdatei und der Liste des Fuellskripts meldet die
#                        Luecke von 1.11.0 (Liste ohne `<READ_ONLY_PATHS>`).
#   D407c (Gegenprobe) - mit der ausgelieferten Liste bleibt keine Luecke.
# ⚠️ Grenze, benannt: D407b und D407c messen den ABGLEICH, nicht den Lauf des
# Fuellskripts; der braucht das Uebungsrepositorium, und eine Sonde, die daran haengt,
# bestuende auf einem Arbeitsplatz und fiele auf dem naechsten. Gelaufen ist das Skript
# im Messaufbau von 1.12.0 (Protokoll).
M407_KEIN_KERN = "weder ein installiertes Client Pack noch ein Kernverzeichnis"
M407_CODE = r"""
import importlib.util, json, sys
def lade(name, pfad):
    spec = importlib.util.spec_from_file_location(name, pfad)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m
sys.path.insert(0, sys.argv[2])
vo = lade("_vo407", sys.argv[1])
mw = lade("_mw407", sys.argv[3])
pfad, grund = vo.skill_pfad(sys.argv[4], "fw-code-explain")
pack, _ = mw._manifest(sys.argv[4])
print(json.dumps({"pfad": pfad, "grund": grund, "pack": pack}))
"""


def _407_gebraucht(quelltext: str) -> list:
    """Die Liste GEBRAUCHT des Fuellskripts - gelesen, nicht nachgeschrieben."""
    for knoten in ast.walk(ast.parse(quelltext)):
        if isinstance(knoten, ast.Assign) and any(
                isinstance(z, ast.Name) and z.id == "GEBRAUCHT" for z in knoten.targets):
            return [e.value for e in knoten.value.elts]
    return []


def _407_luecken(settings_text: str, gebraucht: list) -> list:
    return sorted(set(re.findall(r"<[A-Z_]+>", settings_text)) - set(gebraucht))


def sonden_messapparat() -> None:
    """Wirkungsnachweis fuer D-407 an einer echten claude-code-Installation."""
    kern = os.path.join(QUELLE, ".koolie", "core")
    vo = os.path.join(kern, "tests", "scripts", "validate-output.py")
    erh = os.path.join(kern, "tests", "erhebungen")
    mw = os.path.join(erh, "mcp-waechter.py")
    ziel = tempfile.mkdtemp(prefix="lw-407-")
    try:
        root = os.path.join(ziel, "projekt")
        os.makedirs(root)
        p = unterprozess([sys.executable, os.path.join(kern, "install.py"),
                          "--client", "claude-code", "--root", root])
        settings = lies(os.path.join(root, ".claude", "settings.json"))
        # Der Kern im Baum, so weit die Werkzeuge ihn brauchen: Packs und Skillquellen.
        shutil.copytree(os.path.join(kern, "clients"),
                        os.path.join(root, ".koolie", "core", "clients"))
        shutil.copytree(os.path.join(kern, "framework"),
                        os.path.join(root, ".koolie", "core", "framework"))
        q = unterprozess([sys.executable, "-c", M407_CODE, vo, erh, mw, root])
        try:
            ist = json.loads((q.stdout or "").strip().splitlines()[-1])
        except (ValueError, IndexError):
            ist = {}
        erwartet = os.path.join(root, ".claude", "skills", "fw-code-explain", "SKILL.md")
        ok = (p.returncode == 0 and q.returncode == 0 and ist.get("pack") == "claude-code"
              and os.path.normcase(ist.get("pfad") or "") == os.path.normcase(erwartet))
        melde("SONDE", "D407", ok,
              "Kern unter .koolie/core: validate-output.py findet den Skill des "
              "installierten Packs, mcp-waechter.py das Pack")
        if not ok:
            notiz("        Exit %d/%d, Ergebnis %r" % (p.returncode, q.returncode, ist))

        shutil.rmtree(os.path.join(root, ".koolie", "core"))
        q = unterprozess([sys.executable, "-c", M407_CODE, vo, erh, mw, root])
        try:
            ist = json.loads((q.stdout or "").strip().splitlines()[-1])
        except (ValueError, IndexError):
            ist = {}
        ok = (q.returncode == 0 and ist.get("pack") is None and ist.get("pfad") is None
              and M407_KEIN_KERN in (ist.get("grund") or ""))
        melde("GEGENPROBE", "D407a", ok,
              "Ohne Kern erfinden beide Werkzeuge keinen - dieselbe Meldung wie bisher")
        if not ok:
            notiz("        Exit %d, Ergebnis %r" % (q.returncode, ist))

        gebraucht = _407_gebraucht(lies(os.path.join(erh, "cc-overlay-fuellen.py")))
        luecke = _407_luecken(settings, [g for g in gebraucht if g != "<READ_ONLY_PATHS>"])
        ok = p.returncode == 0 and luecke == ["<READ_ONLY_PATHS>"]
        melde("SONDE", "D407b", ok,
              "Der Abgleich meldet die Luecke von 1.11.0: die Liste des Fuellskripts "
              "ohne <READ_ONLY_PATHS>")
        if not ok:
            notiz("        Luecke %r" % luecke)
        luecke = _407_luecken(settings, gebraucht)
        ok = p.returncode == 0 and bool(gebraucht) and luecke == []
        melde("GEGENPROBE", "D407c", ok,
              "Die ausgelieferte Liste deckt jeden Platzhalter der erzeugten "
              "Berechtigungsdatei")
        if not ok:
            notiz("        GEBRAUCHT %r, Luecke %r" % (gebraucht, luecke))
    finally:
        aufraeumen(ziel)


buendel(sonden_messapparat,
        "Der Messapparat findet den Kern unter .koolie/core, und das Fuellskript "
        "entfaltet jeden Platzhalter der claude-code-Berechtigungsdatei")


# --- Pruefung 26 und der Suchkanal (CR-2026-047, D-47) ----------------------------
#
# Zwei Gegenstaende in einem Block, weil sie dieselbe Entscheidung tragen: Der Suchkanal
# wird vom Schutz-Hook durchgesetzt (nicht von der Berechtigungsdatei), und ein Client
# ohne Suchwerkzeug darf das erklaeren, ohne dass daraus ein Schlupfloch wird.

def _manifest_pfad(root: str, pack: str) -> str:
    return os.path.join(root, ".koolie/core", "clients", pack, "manifest.json")


def _manifest_aendern(root: str, pack: str, aenderung) -> None:
    pfad = _manifest_pfad(root, pack)
    man = json.loads(lies(pfad))
    aenderung(man)
    schreib(pfad, json.dumps(man, ensure_ascii=False, indent=2) + "\r\n")


def _abwesenheit_ohne_begruendung(root: str) -> None:
    def f(man):
        man["hook_tools_absent"] = ["search"]
        man.pop("_hook_tools_absent_note", None)
    _manifest_aendern(root, "devin-desktop", f)


def _abwesenheit_widerspricht(root: str) -> None:
    # 'write' fuer abwesend erklaeren, obwohl die Berechtigungsschicht ein
    # Schreibwerkzeug kennt - das ist der Missbrauchsfall, gegen den die Pruefung steht.
    def f(man):
        man["hook_tools_absent"] = ["write"]
        man["_hook_tools_absent_note"] = "Sonde: absichtlich widerspruechlich."
    _manifest_aendern(root, "devin-desktop", f)


sonde("26", "Erklaerte Abwesenheit ohne Begruendung wird gemeldet",
      _abwesenheit_ohne_begruendung, "_hook_tools_absent_note fehlt oder ist leer")
sonde("26", "Erklaerte Abwesenheit im Widerspruch zu permission_tools wird gemeldet",
      _abwesenheit_widerspricht, "permission_tools nennt dafuer aber")
gegenprobe("26", "Die ausgelieferte Abwesenheitserklaerung bleibt unbeanstandet",
           None, "hook_tools_absent")


def sonden_suchkanal() -> None:
    """Der Schutz-Hook erreicht die Suchwerkzeuge - und nur mit dem richtigen Pfad.

    Bis 0.29.0 war der Suchkanal auf beiden Schichten unbewacht: kein Hook-Eintrag und
    keine Berechtigungsregel (B04, Lauf B04-5). Eine Regel traegt hier auch nicht - die
    Suchwerkzeuge dieses Clients werten keine Pfadregeln aus (AP2-CC-02). Der Hook ist
    die einzige Schranke, und deshalb wird sie gemessen.

    Die Gegenprobe ist der wichtigere Teil: Ein Hook, der jede Suche blockiert, bestuende
    die Sonde und machte das Suchwerkzeug unbenutzbar.
    """
    hook = os.path.join(QUELLE, ".koolie/core", "tests", "scripts",
                        "hook-check-secrets.py")

    def hooklauf(werkzeug: str, eingabe: dict) -> int:
        p = unterprozess([sys.executable, hook, "--fail-closed"],
                         input=json.dumps({"tool_name": werkzeug,
                                           "tool_input": eingabe},
                                          ensure_ascii=False))
        return p.returncode

    melde("SONDE", "B04", hooklauf("Grep", {"pattern": "x", "path": "sonde/.env"}) == 2,
          "Suchwerkzeug auf einen Secret-Pfad wird blockiert")
    melde("SONDE", "B04", hooklauf("Glob", {"pattern": "**/*.pem"}) == 2,
          "Suchmuster auf Schluesseldateien wird blockiert")
    melde("GEGENPROBE", "B04",
          hooklauf("Grep", {"pattern": "x", "path": "src/"}) == 0,
          "Suche in einem gewoehnlichen Pfad bleibt moeglich")
    melde("GEGENPROBE", "B04",
          hooklauf("Grep", {"pattern": "x", "path": ".koolie/core/framework/core/"}) == 0,
          "Suche im Kernverzeichnis bleibt moeglich - lesen darf der Agent ihn")


buendel(sonden_suchkanal,
        "Der Schutz-Hook faengt Grep und Glob auf geschuetzte Pfade ab und laesst eine "
        "gewoehnliche Suche durch - die einzige Schranke des Suchkanals")


# --- Pruefung 27 und der Installationsabbruch (CR-2026-050, D-50) -----------------
#
# Zwei Schichten, zwei Sonden: Der Validator findet das verworfene Zusagenfeld im
# Repositorium, install.py bricht bei der Installation ab. Die zweite ist die
# wirksamere - sie steht zwischen dem Befund und einer ausgelieferten Installation.

def _ersatz_entfernen(root: str) -> None:
    pfad = _manifest_pfad(root, "claude-code")
    man = json.loads(lies(pfad))
    man["skill_frontmatter"].pop("skill_permissions_ersatz", None)
    schreib(pfad, json.dumps(man, ensure_ascii=False, indent=2) + "\r\n")


def _ersatz_leeren(root: str) -> None:
    # Ein leerer Begleitsatz ist kein Begleitsatz - dieselbe Strenge wie bei Pruefung 26.
    pfad = _manifest_pfad(root, "claude-code")
    man = json.loads(lies(pfad))
    man["skill_frontmatter"]["skill_permissions_ersatz"] = "   "
    schreib(pfad, json.dumps(man, ensure_ascii=False, indent=2) + "\r\n")


sonde("27", "Verworfenes Zusagenfeld ohne benannten Ersatz wird gemeldet",
      _ersatz_entfernen, "traegt eine Zusage und steht in skill_frontmatter.drop_fields")
sonde("27", "Leerer Ersatzsatz gilt nicht als benannter Ersatz",
      _ersatz_leeren, "traegt eine Zusage und steht in skill_frontmatter.drop_fields")
gegenprobe("27", "Der ausgelieferte Ersatzsatz bleibt unbeanstandet",
           None, "traegt eine Zusage und steht in skill_frontmatter.drop_fields")


def sonden_zusagenfeld_installation() -> None:
    """install.py bricht ab, statt eine Zusage folgenlos zu verwerfen.

    Der Validator meldet denselben Fehler im Repositorium; diese Sonde misst die Stelle,
    an der es zaehlt - den Schreibvorgang in ein Projekt. Die Gegenprobe belegt, dass die
    Installation mit benanntem Ersatz weiterhin durchlaeuft; ohne sie stuende nur fest,
    dass irgendetwas abbricht.
    """
    ziel = tempfile.mkdtemp(prefix="lw-b01-")
    try:
        quelle = os.path.join(ziel, "quelle")
        shutil.copytree(QUELLE, quelle, ignore=shutil.ignore_patterns(".git"))
        werkzeug = os.path.join(quelle, ".koolie/core", "install.py")

        frei = os.path.join(ziel, "mit-ersatz")
        os.makedirs(frei)
        p = unterprozess([sys.executable, werkzeug, "--client", "claude-code",
                          "--root", frei])
        melde("GEGENPROBE", "B01", p.returncode == 0,
              "Installation mit benanntem Ersatz laeuft durch")
        if p.returncode != 0:
            notiz("        Ausgabe:", " | ".join(
                ((p.stdout or "") + (p.stderr or "")).splitlines()[:4]))

        _ersatz_entfernen(quelle)
        ohne = os.path.join(ziel, "ohne-ersatz")
        os.makedirs(ohne)
        q = unterprozess([sys.executable, werkzeug, "--client", "claude-code",
                          "--root", ohne])
        aus = (q.stdout or "") + (q.stderr or "")
        gemeldet = "traegt eine Zusage und steht in drop_fields" in aus
        melde("SONDE", "B01", q.returncode != 0 and gemeldet,
              "Installation bricht ab, wenn das Zusagenfeld ersatzlos entfiele")
        if not (q.returncode != 0 and gemeldet):
            notiz("        Exit:", q.returncode, "| Ausgabe:",
                  " | ".join(aus.splitlines()[:4]))
    finally:
        aufraeumen(ziel)


buendel(sonden_zusagenfeld_installation,
        "install.py bricht beim Schreiben in ein Projekt ab, wenn eine Zusage ohne "
        "benannten Ersatz verworfen wurde, und laeuft mit Ersatz durch")


# --- 28: Lesesperre gegen Schreibsperre (B07, D-55) ------------------------------
# Drei Sonden, weil die Pruefung drei Wege hat, falsch zu sein: Sie kann den Fehler in
# der Quelle uebersehen, ihn in der Installation uebersehen - und sie kann ihre eigene
# Deklaration nicht mehr finden und dadurch leise bestehen. Die Gegenprobe ist hier die
# wichtigere Haelfte: Beide Traeger erklaeren im Fliesstext, dass die Strukturpfade
# gerade NICHT in <EXCLUDED_PATHS> gehoeren, und nennen dabei beides in einer Zeile. Eine
# Pruefung, die jede Nennung meldet, wuerde den richtigen Text beanstanden.
VORLAGE_28 = ".koolie/core/templates/project-overlay/OVERLAY.md"
REGEL_28 = ".koolie/core/framework/runtime/rules/20-project-overlay.md"


def _p(root, rel):
    return P(root, rel.replace("/", os.sep))


def _strukturpfad_in_ausschluss(root: str) -> None:
    pfad = _p(root, VORLAGE_28)
    text = lies(pfad)
    alt = "| Ausgeschlossene Pfade (weder lesen noch \u00e4ndern) | `<EXCLUDED_PATHS>` |"
    schreib(pfad, text.replace(
        alt, alt + " `<RUNTIME_DIR>/`,", 1))


def _strukturpfad_in_laufzeitregel(root: str) -> None:
    pfad = _p(root, REGEL_28)
    text = lies(pfad)
    alt = "- Ausgeschlossene Pfade, weder lesen noch \u00e4ndern (`<EXCLUDED_PATHS>`):"
    schreib(pfad, text.replace(alt, alt + " `<ROOT_INSTRUCTION_FILE>`,", 1))


def _beschriftung_verlieren(root: str) -> None:
    pfad = _p(root, REGEL_28)
    text = lies(pfad)
    schreib(pfad, text.replace(
        "- Ausgeschlossene Pfade, weder lesen noch \u00e4ndern (`<EXCLUDED_PATHS>`):",
        "- Gesperrte Verzeichnisse (`<EXCLUDED_PATHS>`):", 1))


def _hinweis_ohne_deklaration(root: str) -> None:
    """Gegenprobe: dieselben Angaben im Fliesstext, aber keine Deklaration."""
    pfad = _p(root, REGEL_28)
    text = lies(pfad)
    schreib(pfad, text.replace(
        "## Freigegebene Befehle",
        "Hinweis: `<RUNTIME_DIR>/`, `<ROOT_INSTRUCTION_FILE>` und `.koolie/project-overlay/` "
        "geh\u00f6ren nicht in `<EXCLUDED_PATHS>` - ihr Schreibschutz ist kein "
        "Leseverbot.\r\n\r\n## Freigegebene Befehle", 1))


sonde("28a", "Strukturpfad in der <EXCLUDED_PATHS>-Zeile der Overlay-Vorlage",
      _strukturpfad_in_ausschluss, "Die Deklaration von <EXCLUDED_PATHS> nennt")

sonde("28b", "Strukturpfad in der <EXCLUDED_PATHS>-Zeile der Laufzeitregel",
      _strukturpfad_in_laufzeitregel, "Die Deklaration von <EXCLUDED_PATHS> nennt")

sonde("28c", "Verlorene Beschriftung - die Pruefung darf nicht leise bestehen",
      _beschriftung_verlieren, "keine Zeile ist als Deklaration erkennbar")

gegenprobe("28", "Dieselben Pfade im Fliesstext, ausdruecklich ausgeschlossen",
           _hinweis_ohne_deklaration, "Die Deklaration von <EXCLUDED_PATHS> nennt")


# --- 29: K3-Kategorien in Kurz- und Langform (B09, D-52) ------------------------
# Zwei Fehlerbilder, beide vorgekommen: eine fehlende Kategorie in der Kurzform - sie
# fuehrte bis 0.31.0 nur sechs von acht - und eine Bedingung an einer Kategorie, die
# unbedingt gilt. Dazu die dritte Sonde auf den verlorenen Anker, aus demselben Grund
# wie bei 28c.
KURZFORM_29 = ".koolie/core/framework/runtime/root-instruction.md"
LANGFORM_29 = ".koolie/core/framework/core/02-privacy.md"


def _kategorie_entfernen(root: str) -> None:
    pfad = _p(root, KURZFORM_29)
    text = lies(pfad)
    schreib(pfad, text.replace(
        "Sicherheitskonfigurationen mit Schutzwirkung, interne Adressen",
        "interne Adressen", 1))


def _bedingung_einfuegen(root: str) -> None:
    pfad = _p(root, LANGFORM_29)
    text = lies(pfad)
    schreib(pfad, text.replace(
        "- interne Adressen, Hostnamen, Netzpl\u00e4ne, Mandanten- und Umgebungskennungen",
        "- interne Adressen, Hostnamen, Netzpl\u00e4ne, Mandanten- und Umgebungskennungen, "
        "sofern nicht im Overlay ausdr\u00fccklich als K1 eingestuft", 1))


def _anker_verlieren(root: str) -> None:
    pfad = _p(root, KURZFORM_29)
    text = lies(pfad)
    schreib(pfad, text.replace("- Immer K3, ausnahmslos", "- Stets K3, ausnahmslos", 1))


def _kurzform_umformulieren(root: str) -> None:
    """Gegenprobe: kuerzer formuliert, aber keine Kategorie weniger."""
    pfad = _p(root, KURZFORM_29)
    text = lies(pfad)
    schreib(pfad, text.replace(
        "Sicherheitskonfigurationen mit Schutzwirkung, interne Adressen",
        "Sicherheitskonfigurationen, interne Adressen", 1))


sonde("29a", "Fehlende K3-Kategorie in der Kurzform",
      _kategorie_entfernen, "nennt die Kategorie 'Sicherheitskonfigurationen' nicht")

sonde("29b", "Bedingung an einer unbedingten K3-Kategorie",
      _bedingung_einfuegen, "traegt eine Bedingung")

sonde("29c", "Der verlorene Anker der K3-Liste - die Pruefung meldet ihr Fehlen selbst, statt "
      "leise zu bestehen",
      _anker_verlieren, "ist nicht mehr auffindbar")

gegenprobe("29", "Kuerzere Formulierung derselben acht Kategorien",
           _kurzform_umformulieren, "nennt die Kategorie")


# --- 30: Vollstaendigkeit der Grenzfalltabelle (B07, B09) -----------------------
# Die Tabelle ist das Abnahmekriterium des Reviews. Drei Wege, sie unbemerkt zu
# entwerten: eine Zeile verschwindet, eine Spalte bleibt leer, eine Entscheidung ist
# durch keinen Grenzfall gedeckt.
EDGE_30 = ".koolie/core/tests/EDGE_CASES.md"
KATALOG_30 = ".koolie/core/tests/TEST_CATALOG.md"


def _grenzfall_loeschen(root: str) -> None:
    pfad = _p(root, EDGE_30)
    zeilen = lies(pfad).split("\r\n")
    behalten = [z for z in zeilen if not z.startswith("| G-07 |")]
    schreib(pfad, "\r\n".join(behalten))


def _spalte_leeren(root: str) -> None:
    pfad = _p(root, EDGE_30)
    text = lies(pfad)
    start = text.index("| G-05 |")
    ende = text.index("\r\n", start)
    zeile = text[start:ende]
    zellen = zeile.split(" | ")
    zellen[4] = ""
    schreib(pfad, text[:start] + " | ".join(zellen) + text[ende:])


def _entscheidung_entkoppeln(root: str) -> None:
    pfad = _p(root, EDGE_30)
    schreib(pfad, lies(pfad).replace("(D-53)", "(siehe Antrag)"))


def _grenzfall_ergaenzen(root: str) -> None:
    """Gegenprobe: eine weitere Zeile samt mitgezaehlter Anzahl.

    ZWEIMAL an einem neuen Grenzfall gebrochen, zuletzt mit 0.36.0 an G-18: Die
    Anzahl war woertlich verankert (17 -> 18), und die synthetische Kennung war
    G-18 - dieselbe, die dieses Release wirklich vergeben hat. Beide Fallen sind
    in der Uebergabe benannt gewesen, und beide sind trotzdem zugeschnappt.

    Die Kennung ist seither G-99 und kollidiert mit keinem echten Fall. Die Anzahl
    bleibt woertlich: Ob eine Gegenprobe ihre Summen ABLEITEN soll, ist eine
    Ermessensfrage und nicht entschieden - eine abgeleitete Summe verdoppelt
    womoeglich nur die Rechenweise der Pruefung, statt sie zu belegen. Die Frage
    ist damit zum VIERTEN Mal aufgetreten und gehoert in einen eigenen Antrag.

    Seit 0.42.0 zieht diese Gegenprobe ZWEI Register nach: die Anzahl im Steckbrief
    von EDGE_CASES.md und die Arbeitsanweisung in FW-KO-05. Ein Repositorium mit 21
    Grenzfaellen, dessen Testblatt weiter von zwanzig spricht, ist kein erlaubter
    Fall, sondern genau der Befund, gegen den Pruefung 40 gebaut ist (D-86). Der
    Sondenlauf zu 0.42.0 hat ihn gemeldet, bevor jemand ihn behaupten musste.
    """
    pfad = _p(root, EDGE_30)
    frei(pfad, "G-99")
    ersetze(pfad, ("| Anzahl der Grenzf\u00e4lle | 20 |",
                   "| Anzahl der Grenzf\u00e4lle | 21 |"))
    zeile_nach(
        pfad, "| G-20 |",
        "| G-99 | Synthetischer Zusatzfall der Gegenprobe | **zul\u00e4ssig** | M1 | "
        "niedrig | keine | `.koolie/core/tests/EDGE_CASES.md` Abschnitt 1 (D-52) |")
    ersetze(_p(root, KATALOG_30),
            ("Die 20 Grenzfälle einzeln", "Die 21 Grenzfälle einzeln"))


sonde("30a", "Geloeschte Grenzfallzeile gegen die Anzahl im Steckbrief",
      _grenzfall_loeschen, "Grenzfallzeilen, der Steckbrief nennt")

sonde("30b", "Leere Spalte in einem Grenzfall",
      _spalte_leeren, "ist leer")

sonde("30c", "Eine Entscheidung des Logs, die kein Grenzfall mehr deckt, wird gemeldet",
      _entscheidung_entkoppeln, "Keine Grenzfallzeile verweist auf D-53")

gegenprobe("30", "Zusaetzlicher Grenzfall mit mitgezaehlter Anzahl",
           _grenzfall_ergaenzen, "Grenzfallzeilen")



# --- Kandidatenpruefung, Status-Hook und Fetch-Allow (B08, B11) -------------------
#
# Je Pack eine eigene Installation, wie bei der Aktivierungspruefung: B02 war nicht, dass
# eine Pruefung falsch prueft, sondern dass sie einen Client gar nicht sieht. Das faellt
# nur auf, wenn derselbe Fall in jeder Installation laeuft.
#
# Die Gegenproben sind hier die wichtigere Haelfte. Bei der Kandidatenpruefung belegt sie,
# dass ein vollstaendiger, noch nicht aktiver Kandidat **durchlaeuft** - ohne sie stuende
# nur fest, dass irgendetwas gemeldet wird, und eine Pruefung, die alles meldet, besteht
# jede Sonde.


def ready_ausgabe(root: str) -> str:
    """Ausgabe der Kandidatenpruefung (--check-overlay-ready)."""
    p = unterprozess([sys.executable, os.path.join(root, *VALIDATOR.split("/")),
                      "--root", root, "--check-overlay-ready"])
    return (p.stdout or "") + (p.stderr or "")


def hook_ausgabe(root: str, regelablage: str) -> str:
    """Ausgabe des Status-Hooks - er blockiert nie, er informiert."""
    p = unterprozess([sys.executable,
                      os.path.join(root, ".koolie/core", "tests", "scripts",
                                   "hook-overlay-status.py"),
                      root, regelablage])
    return (p.stdout or "") + (p.stderr or "")


def _kandidat_herstellen(regel: str, overlay: str, rechte: str) -> None:
    """Ein vollstaendig ausgefuellter Kandidat: keine offenen Werte, Status 'inaktiv'."""
    for pfad in (regel, overlay, rechte):
        schreib(pfad, SO_PLATZHALTER.sub("gesetzt", lies(pfad)))
    for pfad in (regel, overlay):
        _so_status(pfad, "inaktiv")


def sonden_kandidatenpruefung() -> None:
    """Wirkungsnachweis der Kandidatenpruefung und des Status-Hooks (B08, D-57, D-58)."""
    for pack in ("claude-code", "devin-desktop"):
        root = installation(pack)
        try:
            man = json.loads(lies(os.path.join(QUELLE, ".koolie/core", "clients", pack,
                                               "manifest.json")))
            regelablage = man["pack_runtime_dir"]
            regel = os.path.join(root, *regelablage.split("/"), "20-project-overlay.md")
            overlay = os.path.join(root, ".koolie/project-overlay", "OVERLAY.md")
            rechte = os.path.join(root, *man["permissions_file"].split("/"))

            # --- Gegenprobe: der vollstaendige, noch nicht aktive Kandidat laeuft durch
            _kandidat_herstellen(regel, overlay, rechte)
            aus = ready_ausgabe(root)
            ok = "check-overlay-ready" not in aus and "(check-overlay-ready)" not in aus
            melde("GEGENPROBE", "CR", ok,
                  f"Vollstaendiger Kandidat mit Status 'inaktiv' laeuft durch ({pack})")
            if not ok:
                notiz("        Ausgabe:", " | ".join(
                    z for z in aus.splitlines() if "check-overlay-ready" in z)[:400])

            # --- Sonde: ein bereits aktiver Kandidat ist keiner
            for pfad in (regel, overlay):
                _so_status(pfad, "aktiv")
            aus = ready_ausgabe(root)
            melde("SONDE", "CR", "ist bereits 'aktiv'" in aus,
                  f"Bereits aktives Overlay wird von der Kandidatenpruefung gemeldet ({pack})")

            # --- Sonde: Drift zwischen den beiden Traegern
            _so_status(overlay, "inaktiv")
            aus = ready_ausgabe(root)
            melde("SONDE", "CR", "widersprechen sich" in aus,
                  f"Abweichende Statusangaben werden gemeldet ({pack})")

            # --- Sonde: der Status ist ueberhaupt nicht ausgefuellt
            for pfad in (regel, overlay):
                _so_status(pfad, "<TBD: aktiv | inaktiv>")
            aus = ready_ausgabe(root)
            melde("SONDE", "CR", "nicht ausgefuellt" in aus,
                  f"Offener Statuswert wird gemeldet ({pack})")

            # --- Status-Hook: dieselben drei Faelle, dasselbe Ergebnis ---------------
            # Der Hook hatte bis 0.32.0 drei Defekte, und jeder einzelne haette die
            # Meldung 'aktiv' erzeugt, wo sie falsch ist.
            for pfad in (regel, overlay):
                _so_status(pfad, "aktiv")
            aus = hook_ausgabe(root, regelablage)
            melde("GEGENPROBE", "HS", "Overlay-Status: aktiv" in aus and "Modus M1" not in aus,
                  f"Hook meldet 'aktiv' ohne M1-Hinweis, wenn alle Angaben aktiv sind ({pack})")

            _so_status(regel, "aktivierung-ausstehend")
            aus = hook_ausgabe(root, regelablage)
            melde("SONDE", "HS", "Overlay-Status: widerspruechlich" in aus,
                  f"'aktivierung-ausstehend' gilt dem Hook nicht als aktiv ({pack})")

            _so_status(regel, "inaktiv")
            aus = hook_ausgabe(root, regelablage)
            melde("SONDE", "HS", "Overlay-Status: widerspruechlich" in aus,
                  f"Hook meldet die Drift statt der ersten gelesenen Datei ({pack})")

            # Nur die Steckbriefzeile, kein Listeneintrag: Das Suchmuster des Hooks
            # verlangte bis 0.32.0 einen Doppelpunkt und traf die Tabelle nie.
            for pfad in (regel, overlay):
                _so_status(pfad, "inaktiv")
            t = lies(overlay)
            schreib(overlay, re.sub(r"^-\s*Overlay-Status:.*$", "", t, flags=re.M))
            os.remove(regel)
            aus = hook_ausgabe(root, regelablage)
            melde("SONDE", "HS", "Overlay-Status: inaktiv" in aus,
                  f"Hook liest den Status auch aus der Steckbriefzeile ({pack})")

            # --- Fetch-Allow: aus dem Manifest, nicht aus einer Namensliste ---------
            # Bis 0.32.0 standen die Werkzeugnamen fest verdrahtet, und das war
            # asymmetrisch: 'Fetch(domain:...)' lief durch, 'WebFetch(domain:...)' fiel.
            werkzeug = man["permission_tools"]["fetch"][0]
            inhalt = lies(rechte)
            schreib(rechte, ersetzt(
                inhalt,
                ('"allow": [', '"allow": [\r\n      "%s(domain:docs.example.invalid)",'
                 % werkzeug),
                quelle=os.path.basename(rechte)))
            p = unterprozess([sys.executable, os.path.join(root, *VALIDATOR.split("/")),
                              "--root", root])
            aus = (p.stdout or "") + (p.stderr or "")
            melde("SONDE", "FA", "allow-Regel auf ein Abrufwerkzeug" in aus,
                  f"Domain-Allow auf das Abrufwerkzeug wird gemeldet ({pack}: {werkzeug})")

            schreib(rechte, inhalt)
            p = unterprozess([sys.executable, os.path.join(root, *VALIDATOR.split("/")),
                              "--root", root])
            aus = (p.stdout or "") + (p.stderr or "")
            melde("GEGENPROBE", "FA", "allow-Regel auf ein Abrufwerkzeug" not in aus,
                  f"Die ausgelieferte Regelmenge bleibt unbeanstandet ({pack})")
        finally:
            aufraeumen(os.path.dirname(root))


buendel(sonden_kandidatenpruefung,
        "Kandidatenpruefung, Status-Hook und Freigabenpruefung gegen je eine Installation "
        "beider Packs - widerspruechlicher Status, offene Platzhalter, allow auf ein "
        "Abrufwerkzeug")


# --- 31: Die Summen der Fachmatrix sind ausgerechnet (D-60) ----------------------
# Dreimal von Hand berichtigt, dreimal wieder gedriftet - deshalb ausgerechnet. Die
# Gegenprobe ist die wichtigere: Eine zusaetzliche Matrixzeile samt nachgezogener Summe
# darf nicht auffallen, sonst waere die Pruefung eine Bremse statt einer Pruefung.
PACK_31 = ".koolie/core/clients/claude-code/CLIENT_PACK.md"
UEBERSICHT_31 = ".koolie/core/clients/README.md"


def _summe_verfaelschen(root: str) -> None:
    pfad = P(root, PACK_31.replace("/", os.sep))
    schreib(pfad, lies(pfad).replace("| `[TECHNISCH]` | 22 von 32 |",
                                     "| `[TECHNISCH]` | 23 von 32 |", 1))


def _gesamtzahl_verfaelschen(root: str) -> None:
    pfad = P(root, PACK_31.replace("/", os.sep))
    schreib(pfad, lies(pfad).replace("| 22 von 32 |", "| 22 von 33 |", 1))


def _zusammenfassung_entfernen(root: str) -> None:
    pfad = P(root, PACK_31.replace("/", os.sep))
    schreib(pfad, lies(pfad).replace("## 3. Zusammenfassung",
                                     "## 3. Uebersicht", 1))


def _zeile_ohne_einstufung(root: str) -> None:
    pfad = P(root, PACK_31.replace("/", os.sep))
    t = lies(pfad)
    marke = "| X2 |"
    i = t.index(marke)
    ende = t.index("\r\n", i)
    schreib(pfad, t[:ende] + "\r\n| Z9 | Sonde ohne Einstufung | - | - | - |" + t[ende:])


def _zeile_mit_summe(root: str) -> None:
    """Gegenprobe: eine zusaetzliche Zeile samt nachgezogenen Summen."""
    pfad = P(root, PACK_31.replace("/", os.sep))
    frei(pfad, "| Z9 |")
    zeile_nach(pfad, "| X2 |",
               "| Z9 | Sonde mit Einstufung | - | `[TECHNISCH]` | `[DOK]` |")
    ersetze(pfad,
            ("| `[TECHNISCH]` | 22 von 32 |", "| `[TECHNISCH]` | 23 von 33 |"),
            ("| 8 von 32 (", "| 8 von 33 ("),
            ("| **2 von 32** (", "| **2 von 33** ("),
            ("| 0 von 32 |", "| 0 von 33 |"))
    # Seit 0.36.0 rechnet Pruefung 31 dieselbe Zahl auch in der Uebersicht der Ablage nach
    # (D-71). Eine Gegenprobe, die nur das Pack nachzieht, faellt seither an der zweiten
    # Stelle - und genau das ist der Zweck der Erweiterung.
    u = P(root, UEBERSICHT_31.replace("/", os.sep))
    # 0.89.0: Der Statuswert dieser Zeile stand hier woertlich und ist mit CR-2026-124
    # von "entwurf" auf "pilot" berichtigt worden - das Pack selbst sagte schon "pilot".
    ersetze(u, ("| pilot | 22 von 32 |", "| pilot | 23 von 33 |"))


sonde("31a", "Verfaelschte Anzahl je Einstufung in der Zusammenfassung",
      _summe_verfaelschen, "Zeile(n) als [TECHNISCH]; gezaehlt sind")

sonde("31b", "Eine verfaelschte Gesamtzahl der Matrixzeilen wird gegen die gezaehlte Zahl gemeldet",
      _gesamtzahl_verfaelschen, "Matrixzeilen; gezaehlt sind")

sonde("31c", "Fehlende Zusammenfassung - die Pruefung darf nicht leise bestehen",
      _zusammenfassung_entfernen, "kein Abschnitt '## 3. Zusammenfassung")

sonde("31d", "Eine Matrixzeile ohne Einstufung faellt aus jeder Summe und wird gemeldet",
      _zeile_ohne_einstufung, "ohne Einstufung: Z9")

def _uebersicht_verfaelschen(root: str) -> None:
    pfad = P(root, UEBERSICHT_31.replace("/", os.sep))
    schreib(pfad, lies(pfad).replace("| pilot | 22 von 32 |",
                                     "| pilot | 25 von 29 |", 1))


def _uebersichtszeile_entfernen(root: str) -> None:
    pfad = P(root, UEBERSICHT_31.replace("/", os.sep))
    t = lies(pfad)
    i = t.index("| `claude-code` | `CP-CC` |")
    ende = t.index("\r\n", i) + 2
    schreib(pfad, t[:i] + t[ende:])


sonde("31e", "Ueberholte Zahl in der Uebersicht der Ablage - der Stand bis 0.35.0",
      _uebersicht_verfaelschen, "technisch durchgesetzte Zeilen; aus der Faehigkeitsmatrix")

sonde("31f", "Pack ohne Zeile in der Uebersicht", _uebersichtszeile_entfernen,
      "kein Eintrag fuer das Client Pack 'claude-code'")

gegenprobe("31", "Zusaetzliche Matrixzeile samt nachgezogener Summe an BEIDEN Stellen",
           _zeile_mit_summe, "gezaehlt sind")



# --- 32: Eingabeschema und Pfadidentitaet des Schutz-Hooks (B06, CR-2026-056) -----
#
# Sechs Sonden, weil der Hook seit 0.34.0 sechs voneinander unabhaengige Mechanismen
# traegt. Jede bricht genau EINEN, und keine bricht ihn ueber den naheliegenden Fall:
# Bei .KOOLIE/CORE/VERSION decken die Aufloesung und re.I einander gegenseitig zu -
# faellt einer von beiden aus, bestuende die Pruefung, und die Sonde zeigte nichts.
# 32a und 32e treffen deshalb je einen Fall, den nur ein Mechanismus faengt.
HOOK_32 = ".koolie/core/tests/scripts/hook-check-secrets.py"


def _hook32(root: str) -> str:
    return P(root, HOOK_32.replace("/", os.sep))


def _tausche(root: str, alt: str, neu: str) -> None:
    """Eine Ersetzung im Hook der Kopie. Trifft der Suchtext nicht, bleibt der Baum
    unveraendert - und sonde() meldet genau das, statt die Pruefung zu messen."""
    pfad = _hook32(root)
    schreib(pfad, lies(pfad).replace(alt, neu, 1))


def _ohne_aufloesung(root: str) -> None:
    """Die Pfadaufloesung liefert nichts - die Muster sehen nur noch den Rohtext."""
    _tausche(root, "    voll, nur_secret = [], []", "    return [], []")


def _ohne_ereignispruefung(root: str) -> None:
    """Eine leere Eingabe gilt wieder als harmloses Ereignis - der Stand bis 0.33.0."""
    _tausche(root, '        raise Unpruefbar("leere Eingabe")',
             '        raw = \'{"tool_name": "x", "tool_input": {}}\'')


def _umschlag_im_pruefmaterial(root: str) -> None:
    """Der Umschlag wandert zurueck ins Pruefmaterial - der Stand bis 0.33.0."""
    _tausche(root, "    return tool_name.strip().lower(), tool_input, basis",
             "    return tool_name.strip().lower(), dict(payload, **tool_input), basis")


def _unbekanntes_werkzeug_lax(root: str) -> None:
    """Eine unbekannte Operation gilt wieder als lesend statt als die strengste."""
    _tausche(root, '    schreibend = verb in ("write", "unbekannt")',
             '    schreibend = verb == "write"')


def _ohne_schreibweise(root: str) -> None:
    """Das Secret-Muster fuer .env wird wieder schreibungssensitiv."""
    _tausche(root, r'\.env(\.|$)", re.I', r'\.env(\.|$)"')


def _anker_verlieren(root: str) -> None:
    """Der Suchtext, ueber den Pruefung 32 ihren Gegenstand findet, geht verloren."""
    pfad = _hook32(root)
    schreib(pfad, lies(pfad).replace("ereignis_lesen(", "ereignis_pruefen("))


def _zusaetzliches_pfadfeld(root: str) -> None:
    """Gegenprobe: ein weiteres Pfadfeld im Manifest - eine zulaessige Verschaerfung."""
    for pack in ("claude-code", "devin-desktop"):
        pfad = P(root, (".koolie/core/clients/%s/manifest.json" % pack).replace("/", os.sep))
        ersetze(pfad, ('"hook_path_fields": ["file_path"',
                       '"hook_path_fields": ["zielpfad", "file_path"'))


sonde("32a", "Pfadaufloesung aus - nur sie faengt einen Pfad, der den Kern nicht nennt",
      _ohne_aufloesung, "ohne es zu nennen")

sonde("32b", "Ereignispruefung aus - eine leere Eingabe gilt wieder als Ereignis",
      _ohne_ereignispruefung, "ist kein Werkzeugereignis")

sonde("32c", "Umschlag zurueck im Pruefmaterial - der Stand bis 0.33.0",
      _umschlag_im_pruefmaterial, "je nachdem ob der Umschlag")

sonde("32d", "Unbekannte Operation gilt wieder als lesend",
      _unbekanntes_werkzeug_lax, "unbekanntes Werkzeug in das Kernverzeichnis")

sonde("32e", "Secret-Muster wieder schreibungssensitiv - nur re.I faengt die nicht "
      "vorhandene Datei", _ohne_schreibweise, "wenn die Datei nicht existiert")

sonde("32f", "Verlorener Anker - die Pruefung darf nicht leise bestehen",
      _anker_verlieren, "'def ereignis_lesen(' fehlt")

def _unteragent_ausnehmen(root: str) -> None:
    """Ein Rueckfall, den nur der Unteragenten-Umschlag faengt (CR-2026-058 E3).

    Simuliert die naheliegende Regression: Jemand nimmt Aufrufe aus einem Unteragenten
    von der Pruefung aus - etwa weil sie "schon oben geprueft" seien. Keine der uebrigen
    sechs Sonden zu 32 sieht das: Ohne agent_type im Umschlag greift die Ausnahme nicht,
    und der Hook verhaelt sich in jedem anderen Fall unveraendert.
    """
    pfad = P(root, ".koolie/core/tests/scripts/hook-check-secrets.py".replace("/", os.sep))
    t = lies(pfad)
    marke = "    tool_name = payload.get(\"tool_name\")"
    i = t.index(marke)
    schreib(pfad, t[:i] + "    if payload.get(\"agent_type\"):\r\n"
            "        return \"read\", {}, PROJEKTWURZEL\r\n" + t[i:])


sonde("32g", "Unteragenten-Umschlag von der Pruefung ausgenommen - ein Rueckfall, den "
      "keine der uebrigen Sonden sieht",
      _unteragent_ausnehmen, "Operation aus einem Unteragenten anders als erwartet")

gegenprobe("32", "Zusaetzliches Pfadfeld im Manifest ist eine zulaessige Verschaerfung",
           _zusaetzliches_pfadfeld, "Befund B06")


# --- 33: Die Abbildung von permissions.deny auf die Werkzeugsperre (CR-2026-057) -----
#
# GEGEN EINE ECHTE INSTALLATION, und das ist hier nicht Zierrat: Pruefung 33 laeuft nur
# fuer ein Pack, dessen Manifest skill_deny_field fuehrt. Die Testinstallation im
# Repositorium ist 'devin-desktop' und fuehrt es nicht - die Pruefung wird im Repo-Lauf
# also GAR NICHT ausgefuehrt. Genau das war Befund B02: nicht, dass eine Pruefung falsch
# prueft, sondern dass sie einen Client nicht sieht.
#
# Fuenf Sonden und eine Gegenprobe. Jede Sonde bricht genau einen Mechanismus.
def _p33(root: str, name: str) -> str:
    return os.path.join(root, ".claude", "skills", name, "SKILL.md")


def sonden_skill_deny() -> None:
    """Wirkungsnachweis der Abbildung und ihrer Grenzen (D-64 bis D-66)."""
    root = installation("claude-code")
    try:
        plan = _p33(root, "fw-plan")
        ausgang = lies(plan)

        # --- Gegenprobe: die unveraenderte Installation laeuft durch ----------------
        # Sie ist hier die wichtigere Haelfte. Ohne sie stuende nur fest, dass Pruefung 33
        # irgendetwas meldet - und eine Pruefung, die jede Installation beanstandet,
        # bestuende jede Sonde.
        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "33", "disallowed-tools" not in aus,
              "Die unveraenderte claude-code-Installation bleibt unbeanstandet")
        if "disallowed-tools" in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "disallowed-tools" in z)[:400])

        # --- 33a: die Sperre fehlt ganz - der Stand bis 0.34.0 ----------------------
        schreib(plan, ersetzt(
            ausgang,
            ("disallowed-tools: Edit, Write, NotebookEdit, Bash\n", ""),
            quelle="fw-plan/SKILL.md"))
        aus = validator_ausgabe(root)
        melde("SONDE", "33a", "aus permissions.deny der Quelle ergibt sich" in aus,
              "Fehlende Werkzeugsperre - der Stand, den B01 beschrieb")

        # --- 33b: die Sperre ist unvollstaendig - eine Luecke ist ausnutzbar --------
        schreib(plan, ersetzt(
            ausgang,
            ("disallowed-tools: Edit, Write, NotebookEdit, Bash",
             "disallowed-tools: Edit, Write"),
            quelle="fw-plan/SKILL.md"))
        aus = validator_ausgabe(root)
        melde("SONDE", "33b", "aus permissions.deny der Quelle ergibt sich" in aus,
              "Unvollstaendige Sperre - mit gesperrtem Write, Edit schrieb der Skill ueber Bash")

        # --- 33c: ein Argumentmuster - gemessen wirkungslos, und zwar lautlos -------
        schreib(plan, ersetzt(
            ausgang,
            ("disallowed-tools: Edit, Write, NotebookEdit, Bash",
             "disallowed-tools: Edit, Write, NotebookEdit, Bash(git push:*)"),
            quelle="fw-plan/SKILL.md"))
        aus = validator_ausgabe(root)
        melde("SONDE", "33c", "Argumentmuster" in aus,
              "Argumentmuster in der Sperre - es sieht aus wie eine Regel und ist keine")

        # --- 33d: ein Werkzeug in beiden Listen - zwei Aussagen, eine davon falsch --
        schreib(plan, ersetzt(
            ausgang,
            ("allowed-tools: Read, Grep, Glob",
             "allowed-tools: Read, Grep, Glob, Bash"),
            quelle="fw-plan/SKILL.md"))
        aus = validator_ausgabe(root)
        melde("SONDE", "33d", "steht zugleich in allowed-tools" in aus,
              "Werkzeug zugleich vorabfreigegeben und gesperrt")
        schreib(plan, ausgang)

        # --- 33e: der verlorene Anker - die Pruefung darf nicht leise bestehen ------
        inst = os.path.join(root, ".koolie/core", "install.py")
        quelle = lies(inst)
        schreib(inst, ersetzt(quelle,
                              ("def deny_abbilden(", "def deny_uebersetzen("),
                              quelle="install.py"))
        aus = validator_ausgabe(root)
        melde("SONDE", "33e", "'def deny_abbilden(' fehlt" in aus,
              "Verlorener Anker - die Pruefung meldet ihr Fehlen selbst")
        schreib(inst, quelle)
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_skill_deny,
        "Die Abbildung von permissions.deny in das Frontmatter eines Skills und ihre "
        "Grenzen - Argumentmuster, Doppelnennung in allowed-tools, verlorener Anker")



# --- 34: Das Startwerkzeug fuer Unteragenten ist genannt oder erklaert (D-70) -----
#
# Anlass ist ein gemessener Befund vom 2026-09-13: Ein Skill kann einen Unteragenten
# starten, die Skill-Sperre reicht in ihn hinein - und das Startwerkzeug stand in keiner
# Werkzeugliste eines Manifests. Bauform der Deklaration wie hook_tools_absent (D-47).
#
# Die letzte Sonde ist die interessanteste: Sie belegt die Verschaerfung, die diese
# Pruefung bei ihrem ERSTEN Lauf selbst gelernt hat. Ohne den Vorbehalt fiel
# devin-desktop durch, obwohl es ehrlich ist - seine Zeile A1 trug einen offenen
# Beleg, und die Praeambel des Packs sagt, die Einstufung nenne die VORGESEHENE
# Tiefe. Die Einstufung allein sagt nicht, ob eine Zusage schon gilt.
#
# MIT 0.87.0 STEHT DER VORBEHALT AUF DER NACHFOLGEFORM BELEG OFFEN (D-291); die
# Markerform ist abgeschafft. Die Sonde trifft davon nichts: Sie nimmt seit 0.86.0 das
# Startwerkzeug weg und nicht den Vorbehalt.
MANIFEST_CC_34 = ".koolie/core/clients/claude-code/manifest.json"
MANIFEST_DD_34 = ".koolie/core/clients/devin-desktop/manifest.json"
PACK_DD_34 = ".koolie/core/clients/devin-desktop/CLIENT_PACK.md"


def _34_feld_entfernen(root: str) -> None:
    pfad = P(root, MANIFEST_CC_34.replace("/", os.sep))
    t = lies(pfad)
    i = t.index('  "agent_start_tools": ["Agent", "Task"],')
    ende = t.index("\r\n", i) + 2
    schreib(pfad, t[:i] + t[ende:])


def _34_leer_ohne_erklaerung(root: str) -> None:
    pfad = P(root, MANIFEST_CC_34.replace("/", os.sep))
    schreib(pfad, lies(pfad).replace('"agent_start_tools": ["Agent", "Task"],',
                                     '"agent_start_tools": [],', 1))


def _34_erklaerung_ohne_notiz(root: str) -> None:
    """Die Sonde BRINGT die Abwesenheitserklaerung mit, statt sie vorauszusetzen.

    Bis 0.85.2 stand sie im Bestand (`agent_start_tools_absent: ["unerhoben"]`); mit
    0.86.0 ist sie aufgeloest - das Startwerkzeug heisst `run_subagent` (D-284). Eine
    Sonde, die auf den Bestand zeigt, verliert damit ihren Gegenstand und bestuende
    leise (D-23). Sie setzt ihn seither selbst.
    """
    pfad = P(root, MANIFEST_DD_34.replace("/", os.sep))
    t = lies(pfad)
    t = t.replace('"agent_start_tools": ["run_subagent"],',
                  '"agent_start_tools": [],', 1)
    t = t.replace('"agent_start_tools_absent": [],',
                  '"agent_start_tools_absent": ["unerhoben"],', 1)
    t = t.replace('"_agent_start_tools_absent_note"',
                  '"_agent_start_tools_absent_hinweis"', 1)
    schreib(pfad, t)


def _34_beides_zugleich(root: str) -> None:
    pfad = P(root, MANIFEST_CC_34.replace("/", os.sep))
    schreib(pfad, lies(pfad).replace(
        '"agent_start_tools": ["Agent", "Task"],',
        '"agent_start_tools": ["Agent", "Task"],\r\n'
        '  "agent_start_tools_absent": ["unerhoben"],\r\n'
        '  "_agent_start_tools_absent_note": "Sonde.",', 1))


def _34_a1_ohne_vorbehalt(root: str) -> None:
    """devin-desktop sagt A1 ohne VERIFY-Marker zu, kann das Werkzeug aber nicht nennen."""
    # BIS 0.85.2 nahm diese Sonde der Zeile A1 ihren VERIFY-Marker. Den gibt es nicht
    # mehr: Die Profilwirkung ist am 2026-09-22 gemessen (D-284), und die Zeile sagt A1
    # seither OHNE Vorbehalt zu. Damit ist der Vorbehalt kein Praeparationsort mehr -
    # die Sonde nimmt stattdessen das Startwerkzeug weg, das die Zusage traegt. Der
    # gemessene Fall ist derselbe, und er ist in diesem Release LIVE eingetreten:
    # Pruefung 34 hat ihn gemeldet, sobald A1 seinen Marker verlor und das Manifest noch
    # ein leeres Feld fuehrte.
    pfad = P(root, MANIFEST_DD_34.replace("/", os.sep))
    t = lies(pfad)
    t = t.replace('"agent_start_tools": ["run_subagent"],',
                  '"agent_start_tools": [],', 1)
    t = t.replace('"agent_start_tools_absent": [],',
                  '"agent_start_tools_absent": ["unerhoben"],', 1)
    schreib(pfad, t)


sonde("34a", "Manifest ohne Feld agent_start_tools - ein Kanal ohne Deklaration",
      _34_feld_entfernen, "Feld 'agent_start_tools' fehlt")

sonde("34b", "Leere Liste ohne erklaerte Abwesenheit - unerhoben oder abwesend?",
      _34_leer_ohne_erklaerung, "ohne dass 'agent_start_tools_absent' die Abwesenheit")

sonde("34c", "Erklaerte Abwesenheit ohne Begruendung - eine Behauptung",
      _34_erklaerung_ohne_notiz, "'_agent_start_tools_absent_note' fehlt")

sonde("34d", "Genannt und zugleich fuer abwesend erklaert - zwei Aussagen, eine falsch",
      _34_beides_zugleich, "Beides zugleich geht nicht")

sonde("34e", "Zeile A1 ohne Vorbehalt zugesagt, Startwerkzeug aber nur erklaert",
      _34_a1_ohne_vorbehalt, "Wer Unteragenten zusagt, nennt das Werkzeug")

gegenprobe("34", "Die unveraenderten Packs bleiben unbeanstandet - eines nennt, eines "
           "erklaert mit offenem Vorbehalt", None, "agent_start_tools")


# --- 35: Ein Agentenprofil bekommt kein Startwerkzeug (D-73) ---------------------
#
# Diese Pruefung faengt heute nichts: agent_frontmatter.tool_names kennt gar kein
# Startwerkzeug. Sie ist eine Verankerung - und genau deshalb braucht sie ihre Sonden
# dringender als andere. Ohne sie liesse sich nicht zeigen, DASS sie etwas faengt,
# sobald es den Fall gibt. Gemessen ist der Befund dahinter am 2026-09-13, Lauf
# STARTLOS: Ein Profil mit tools: Read, Grep, Glob kann keine zweite Ebene oeffnen.
MANIFEST_CC_35 = ".koolie/core/clients/claude-code/manifest.json"
PROFIL_35 = ".koolie/core/framework/runtime/agents/fw-reviewer.md"


def _35_abbildung_erweitern(root: str) -> None:
    """Der Fall, der die Zusage lautlos fallen liesse: tool_names lernt es.

    Praepariert wird ueber das JSON, nicht ueber den Text: skill_frontmatter und
    agent_frontmatter fuehren ZEICHENGLEICHE tool_names-Bloecke, und ein Textanker
    traefe den falschen. Pruefung 35 liest nur den zweiten."""
    pfad = P(root, MANIFEST_CC_35.replace(chr(47), os.sep))
    daten = json.loads(lies(pfad))
    daten['agent_frontmatter']['tool_names']['delegate'] = ['Agent']
    schreib(pfad, json.dumps(daten, ensure_ascii=False, indent=2))


def _35_profil_erweitern(root: str) -> None:
    """Der Fall an der Abbildung vorbei: das Profil nennt es selbst."""
    pfad = P(root, PROFIL_35.replace("/", os.sep))
    schreib(pfad, lies(pfad).replace("  - glob", "  - glob\r\n  - agent", 1))


def _35_ablage_entfernen(root: str) -> None:
    """Die Sonde auf den verlorenen Anker: ohne Ablage darf sie nicht leise bestehen."""
    shutil.rmtree(P(root, ".koolie/core/framework/runtime/agents".replace("/", os.sep)))


sonde("35a", "Die Abbildung lernt ein Startwerkzeug - der Fall, der die Zusage "
      "lautlos fallen liesse",
      _35_abbildung_erweitern, "ein Werkzeug, mit dem ein Unteragent GESTARTET")

sonde("35b", "Das Agentenprofil nennt ein Startwerkzeug selbst - an der Abbildung "
      "vorbei",
      _35_profil_erweitern, "Das Frontmatter nennt 'agent'")

sonde("35c", "Verlorener Anker - die Agentenablage fehlt",
      _35_ablage_entfernen, "Pruefung 35 misst die Agentenprofile des Kerns")

gegenprobe("35", "Die unveraenderte Ablage bleibt unbeanstandet", None,
           "GESTARTET wird")

# --- 36: Die Tabellen des Decision Logs sind nicht zerrissen (D-75) --------------
#
# Anlass: vier zerrissene Zeilen in 0.34.0, eine davon seit 0.10.x. Gefunden hat sie
# jedes Mal ein Mensch beim Eintragen einer anderen.
#
# Die Gegenprobe ist hier die wichtigere Haelfte, und zwar aus einem gemessenen Grund:
# Eine naive Zaehlung mit .split("|") meldet D-29 und D-69 als achtspaltig, obwohl beide
# ihren Strich korrekt maskieren und sechsspaltig rendern. Ohne diese Gegenprobe waere
# Pruefung 36 mit zwei Fehlalarmen auf richtigem Text entstanden - und Pruefung 30 haette
# ihren eigenen, latenten Fehlalarm behalten (CR-2026-060 1.3).
DECISION_LOG_36 = ".koolie/core/governance/DECISION_LOG.md"


def _dl36(root: str) -> str:
    return P(root, DECISION_LOG_36.replace("/", os.sep))


def _36_zelle_entfernen(root: str) -> None:
    """Eine Zeile verliert ihre letzte Zelle - der Fall D-61 bis D-63 aus 0.34.0."""
    pfad = _dl36(root)
    zeilen = lies(pfad).split("\r\n")
    treffer = [i for i, z in enumerate(zeilen) if z.startswith("| D-40 |")]
    if len(treffer) != 1:
        raise Praeparationsfehler(
            "DECISION_LOG.md: Anker '| D-40 |' steht %dx, erwartet genau einmal"
            % len(treffer))
    z = zeilen[treffer[0]].rstrip().rstrip("|").rstrip()
    zeilen[treffer[0]] = z[:z.rindex("|")] + "|"
    schreib(pfad, "\r\n".join(zeilen))


def _36_strich_unmaskiert(root: str) -> None:
    """Ein unmaskierter Strich in einem Codespan - der Fall D-29 aus 0.10.x."""
    ersetze(_dl36(root),
            ("| D-40 | **Ein Befund \u00fcber einen Client ist keine Aussage "
             "\u00fcber alle.**",
             "| D-40 | **Ein Befund \u00fcber einen Client ist keine Aussage "
             "\u00fcber alle.** Matcher `a|b`."))


def _36_anker_verlieren(root: str) -> None:
    """Keine Tabellenzeile mehr - die Pruefung darf nicht leise bestehen."""
    pfad = _dl36(root)
    zeilen = [z for z in lies(pfad).split("\r\n") if not z.startswith("|")]
    schreib(pfad, "\r\n".join(zeilen))


def _36_strich_maskiert(root: str) -> None:
    """Gegenprobe: derselbe Strich, korrekt maskiert - so, wie D-69 ihn seit 0.36.0
    traegt. Eine Zaehlung ohne diese Unterscheidung beanstandet den richtigen Text."""
    ersetze(_dl36(root),
            ("| D-40 | **Ein Befund \u00fcber einen Client ist keine Aussage "
             "\u00fcber alle.**",
             "| D-40 | **Ein Befund \u00fcber einen Client ist keine Aussage "
             "\u00fcber alle.** Matcher `a\\|b`."))


sonde("36a", "Zeile mit fehlender Zelle - der Fall D-61 bis D-63 aus 0.34.0",
      _36_zelle_entfernen, "Zellen, der Kopf ihrer Tabelle")

sonde("36b", "Unmaskierter Strich in einer Zelle - der Fall D-29 seit 0.10.x",
      _36_strich_unmaskiert, "Zellen, der Kopf ihrer Tabelle")

sonde("36c", "Verlorener Anker - keine Tabellenzeile mehr",
      _36_anker_verlieren, "keine Tabellenzeile gefunden")

gegenprobe("36", "Maskierter Strich bleibt unbeanstandet - die Schreibweise von D-69",
           _36_strich_maskiert, "Kopf ihrer Tabelle")


# --- Selbstprobe: der Praeparationswaechter selbst (CR-2026-060, D-74) ----------
#
# Ohne sie waere der Waechter die erste ungepruefte Zusage dieses Skripts - und ein
# Waechter, der still ausfaellt, ist genau der Befundtyp, gegen den er gebaut ist.
# Er laeuft ohne Kopie und ohne Validator: Sein Gegenstand ist reine Textarithmetik.
def selbstprobe_waechter() -> None:
    """Der Waechter meldet sich, wenn ein Suchtext nicht genau so oft trifft."""
    faelle = [
        ("W1", "Suchtext trifft gar nicht",
         lambda: ersetzt("abc", ("xyz", "1")), True),
        ("W2", "Suchtext trifft oefter als erwartet",
         lambda: ersetzt("aa", ("a", "b")), True),
        ("W3", "Suchtext trifft genau so oft wie erwartet",
         lambda: ersetzt("aa", ("a", "b", 2)), False),
        ("W4", "Die ZWEITE Ersetzung trifft nicht - der Fall der halben Praeparation",
         lambda: ersetzt("ab", ("a", "x"), ("zzz", "y")), True),
    ]
    for nummer, was, aufruf, erwartet_fehler in faelle:
        try:
            aufruf()
            geworfen = False
        except Praeparationsfehler:
            geworfen = True
        melde("SELBSTPROBE", nummer, geworfen == erwartet_fehler, was)

    # W5: Der Waechter darf nichts geschrieben haben, wenn er abbricht. ersetzt()
    # arbeitet auf einem Text und gibt ihn erst am Ende zurueck - das ist die Zusage,
    # und sie wird hier gepruft, nicht behauptet.
    try:
        ersetzt("ab", ("a", "x"), ("zzz", "y"))
        ergebnis = "durchgelaufen"
    except Praeparationsfehler as exc:
        ergebnis = str(exc)
    melde("SELBSTPROBE", "W5", "zzz" in ergebnis and "trifft 0x" in ergebnis,
          "Die Meldung nennt den Suchtext, der nicht mehr passt")


buendel(selbstprobe_waechter,
        "Der Praeparationswaechter selbst: Er meldet jeden Suchtext, der nicht genau so oft "
        "trifft wie erwartet, und schreibt bei Abbruch nichts")


def selbstprobe_kennung() -> None:
    """Der Kennungswaechter - er ist genau so klug wie die Kennung, die man ihm gibt."""
    root = kopie()
    try:
        pfad = _p(root, EDGE_30)
        try:
            frei(pfad, "G-99")
            frei_ok = True
        except Praeparationsfehler:
            frei_ok = False
        melde("SELBSTPROBE", "K1", frei_ok,
              "G-99 ist im Repositorium nicht vergeben - die Gegenprobe 30 darf sie nutzen")

        try:
            frei(pfad, "G-01")
            kollision = False
        except Praeparationsfehler:
            kollision = True
        melde("SELBSTPROBE", "K2", kollision,
              "Eine vergebene Kennung wird gemeldet - der Fall G-18 vom 2026-09-13")
    finally:
        aufraeumen(os.path.dirname(root))


buendel(selbstprobe_kennung,
        "Der Kennungswaechter ist genau so klug wie die Kennung, die man ihm gibt - eine "
        "freie laeuft durch, eine vergebene wird gemeldet")


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
                              "requirements-engineering", "skills", "role-re-ticket")
        shutil.copytree(quelle, os.path.join(skillablage, "role-re-ticket"))
        _37_schreiben(root, lambda d: _37_dazu(d, "allow", "Skill(role-re-ticket)"))
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
        shutil.rmtree(os.path.join(skillablage, "role-re-ticket"))

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
SKILL_38 = ".koolie/core/framework/skills/fw-plan/SKILL.md"
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
            ('    { "tool": "skill",  "pattern": "fw-code-explain" },\r\n', ""))


def _39_regel_ohne_skill(root: str) -> None:
    """Eine Freigabe fuer einen Skill, den es nicht gibt."""
    ersetze(_p39(root),
            ('"pattern": "fw-code-explain" }', '"pattern": "fw-code-erklaeren" }'))


def _39_muster(root: str) -> None:
    """Das Praefixmuster, das gemessen nichts freigibt (D-82)."""
    ersetze(_p39(root),
            ('"pattern": "fw-code-explain" }', '"pattern": "fw-*" }'))


def _39_anker_weg(root: str) -> None:
    """Keine einzige skill-Regel mehr - die Pruefung darf nicht leise bestehen."""
    text = lies(_p39(root))
    zeilen = [z for z in text.split("\r\n") if '"tool": "skill"' not in z]
    if len(zeilen) == len(text.split("\r\n")):
        raise Praeparationsfehler(
            "permissions.json: keine skill-Regel gefunden, die zu entfernen waere")
    # Das Komma der letzten verbleibenden Regel muss weg, sonst ist die Datei kein JSON.
    schreib(_p39(root),
            "\r\n".join(zeilen).replace('"git blame" },', '"git blame" }'))


def _39_traeger_weg(root: str) -> None:
    """Ein Regeltraeger verliert die Skillwahl - der Zustand vor 0.41.0."""
    ersetze(P(root, ".koolie/core/framework/runtime/rules/00-framework-core.md"
              .replace("/", os.sep)),
            ("**Skillwahl vor dem Schritt.**", "**Hinweis zur Reihenfolge.**"))


def _39_skill_ohne_regel(root: str) -> None:
    """Ein neuer Skill im Verzeichnis, ohne dass jemand die Freigabe nachtraegt."""
    quelle = P(root, ".koolie/core/framework/skills/fw-code-explain"
               .replace("/", os.sep))
    ziel = P(root, ".koolie/core/framework/skills/fw-zwischenstand"
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
      _39_skill_ohne_regel, "'fw-zwischenstand' hat keine allow-Regel")

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
    starts = [i for i, z in enumerate(zeilen) if re.match(r"^ \d+\. ", z)]
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
    for pack, rechte, werkzeug in (("claude-code", ".claude/settings.json", "Bash"),
                                   ("devin-desktop", ".devin/config.json", "Exec")):
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
                _42_rechte(root, rechte, lambda d, n=name, b=befehl: _37_statt(
                    d, "ask", sch(n), rg(b)))
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
            _42_rechte(root, rechte,
                       lambda d: _37_statt(d, "ask", sch("BUILD_COMMAND"),
                                           rg("mvn -B clean package")),
                       lambda d: _37_statt(d, "ask", sch("TEST_COMMAND"),
                                           rg("mvn -B test")),
                       lambda d: _37_weg(d, "ask", sch("LINT_COMMAND")))
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


# --- Pruefung 46: der 1.0.0-Stand (CR-2026-070, D-98, D-99) --------------------------
#
# Sechs Sonden, je eine auf einen eigenen Gegenstand, und zwei davon fuer die zwei
# Richtungen: Ein Kriterium, das ZURUECKFAELLT, und ein Fortschritt, der NICHT
# NACHGEZOGEN ist, sind beide ein Fehler. Ohne die zweite Richtung waere der Zaehler ein
# Fortschrittsbalken - er hielte still, solange sich nichts verschlechtert, und der
# Stand stuende wieder daneben.
#
# Drei Gegenproben, und sie treffen genau die Stellen, an denen die alten Zaehlregeln zu
# breit oder zu schmal waren: ein Klaerungspunkt mit demselben Statuswort (die alte
# Regel zaehlte fuenf davon mit) und ein Marker in einem datierten Protokoll (der
# Zaehlbereich schliesst ihn aus, und das muss er auch tun).
M46_ANKER = "die Standzeile steht 0x statt genau einmal"
M46_K1 = "Kriterium 1 von D-11"
M46_K2 = "Kriterium 2 von D-11"
M46_K3 = "Kriterium 3 von D-11"
M46_K4 = "Kriterium 4 von D-11"
M46_NICHT_NACHGEZOGEN = "der Fortschritt ist nicht nachgezogen"
M46_RUECKFALL = "ein Kriterium ist zur\u00fcckgefallen"
P46_ROADMAP = ".koolie/core/docs/ROADMAP.md".replace("/", os.sep)
P46_STAND = "Gezählt von Prüfung 46: Kriterium 1 = "
# Der Marker in seiner clientneutralen Form - zusammengesetzt, weil eine woertliche
# Nennung in diesem Skript selbst eine Fundstelle waere und Kriterium 1 um eins hoebe.
# Dieses Skript liegt im Zaehlbereich.
P46_MARKER = "<VERIFY AGAINST CURRENT " + "CLIENT" + " DOCUMENTATION>"


def _46_zahl_verstellen(root: str, welche: int, neu: str) -> None:
    """Eine der vier Zahlen der Standzeile auf einen anderen Wert setzen."""
    pfad = P(root, P46_ROADMAP)
    zeilen = lies(pfad).split("\r\n")
    treffer = [i for i, z in enumerate(zeilen) if P46_STAND in z]
    if len(treffer) != 1:
        raise Praeparationsfehler(
            "ROADMAP.md: Standzeile steht %dx, erwartet genau einmal" % len(treffer))
    teile = re.split(r"(= \d+)", zeilen[treffer[0]])
    stellen = [i for i, s in enumerate(teile) if s.startswith("= ")]
    if len(stellen) != 4:
        raise Praeparationsfehler(
            "ROADMAP.md: Standzeile fuehrt %d Zahlen, erwartet vier" % len(stellen))
    teile[stellen[welche]] = "= " + neu
    zeilen[treffer[0]] = "".join(teile)
    schreib(pfad, "\r\n".join(zeilen))


def _46_standzeile_weg(root: str) -> None:
    """Die Standzeile ganz entfernen - der verlorene Anker."""
    pfad = P(root, P46_ROADMAP)
    zeilen = lies(pfad).split("\r\n")
    behalten = [z for z in zeilen if P46_STAND not in z]
    if len(behalten) == len(zeilen):
        raise Praeparationsfehler("ROADMAP.md: keine Standzeile gefunden")
    schreib(pfad, "\r\n".join(behalten))


def _46_marker_dazu(root: str) -> None:
    """Eine neue unverifizierte Aussage im Kern - Kriterium 1 steigt um eins."""
    pfad = P(root, ".koolie/core/framework/core/03-security.md".replace("/", os.sep))
    schreib(pfad, lies(pfad) + "\r\n> Sondenzeile: Wirkung der Sandbox je "
                               "Betriebssystem " + P46_MARKER + ".\r\n")


def _46_testblatt_dazu(root: str) -> None:
    """Ein Testblatt an einem Ort, den eine Ablagenliste uebersaehe.

    Genau der Befund, der Pruefung 46 ausgeloest hat: Die alte Regel las "die dezentralen
    TESTS.md je Skill" als zwoelf Dateien, und die dreizehnte lag unter role-packs/.
    Diese Sonde legt eine vierzehnte unter tech-packs/ an - eine Ablagenliste, die die
    dreizehnte uebersah, uebersaehe sie ebenso.
    """
    ordner = P(root, ".koolie/core/framework/tech-packs/_template".replace("/", os.sep))
    schreib(os.path.join(ordner, "TESTS.md"),
            "# Sondentestblatt\r\n\r\n"
            "| Test-ID | Ziel | Prüfmethode | Ergebnisstatus |\r\n"
            "|---|---|---|---|\r\n"
            "| SO-001 | Sondenfall | sitzung | offen |\r\n")


def _46_steckbrief_dazu(root: str) -> None:
    """Ein neues Modul auf `entwurf` - Kriterium 3 steigt um eins."""
    schreib(P(root, ".koolie/core/prompts/13-sondenprompt.md".replace("/", os.sep)),
            "# Sondenprompt\r\n\r\n"
            "| Attribut | Wert |\r\n|---|---|\r\n"
            "| ID | `FW-PR-13` |\r\n| Version | `0.1.0` |\r\n"
            "| Status | `entwurf` |\r\n| Owner (Rolle) | `<FRAMEWORK_OWNER>` |\r\n")


# Synthetische Kennung der Gegenprobe 46b. Sie stand bis 0.49.0 auf K-36 - und 0.50.0
# hat K-36 und K-37 wirklich vergeben (CR-2026-072). Der Kennungswaechter frei() hat
# die Kollision beim Sondenlauf gemeldet, statt sie als Befund am Repositorium
# erscheinen zu lassen; das ist die Lehre von G-18 (2026-09-13) zum zweiten Mal, und
# diesmal hat sie funktioniert. Die 99 folgt der Konvention von G-99 und UEB-99: hoch
# genug, dass keine echte Vergabe sie erreicht.
P46_KLAERUNG = "K-99"
P46_BESTAETIGT = "| entschieden (`CR-2026-071`); "
P46_VORSCHLAG = "| entschieden (Vorschlag); "


def _46_record_zurueckgefallen(root: str) -> None:
    """D-10 auf `entschieden (Vorschlag)` zuruecksetzen - Kriterium 4 STEIGT auf eins.

    Bis 0.48.0 hob diese Sonde D-10 AUS dem Vorschlagsstatus HERAUS und belegte damit
    die Richtung "Fortschritt nicht nachgezogen". Mit 0.49.0 sind alle neun Records
    bestaetigt (CR-2026-071, D-100) - die Hebung hat keinen Gegenstand mehr, und der
    alte Suchtext haette zwar noch getroffen (er steht jetzt im Verlaufszusatz der
    Zelle), aber an einer Stelle, die Pruefung 46 gar nicht liest. Eine Sonde, die
    etwas veraendert, ohne den Gegenstand zu treffen, ist der schlechteste Zustand:
    Der Baumvergleich meldet kein "[nichts praepariert]", und der Fehlschlag sieht aus
    wie ein Befund an der Pruefung.

    Die Sonde stellt ihren Defekt deshalb seither HER statt ihn zu entfernen - wie 38a
    und 38b seit 0.38.0 - und deckt damit die Richtung, die vorher KEINE Sonde decken
    konnte, weil Kriterium 4 nie null war: den RUECKFALL. Getroffen wird der ANFANG
    der Statuszelle, denn genau das liest der Zaehler (`zellen[4].startswith`).
    """
    pfad = P(root, ".koolie/core/governance/DECISION_LOG.md".replace("/", os.sep))
    zeilen = lies(pfad).split("\r\n")
    treffer = [i for i, z in enumerate(zeilen) if z.startswith("| D-10 |")]
    if len(treffer) != 1:
        raise Praeparationsfehler(
            "DECISION_LOG.md: Zeile D-10 steht %dx, erwartet genau einmal"
            % len(treffer))
    if P46_BESTAETIGT not in zeilen[treffer[0]]:
        raise Praeparationsfehler(
            "DECISION_LOG.md: die Statuszelle von D-10 beginnt nicht mit %r"
            % P46_BESTAETIGT)
    zeilen[treffer[0]] = zeilen[treffer[0]].replace(
        P46_BESTAETIGT, P46_VORSCHLAG, 1)
    schreib(pfad, "\r\n".join(zeilen))


def _46_klaerungspunkt_dazu(root: str) -> None:
    """Ein Klaerungspunkt mit demselben Statuswort - er ist KEIN Decision Record.

    Die alte Zaehlregel war ein roher grep und zaehlte fuenf solcher Zeilen mit. D-11
    sagt "Decision Records"; ein Klaerungspunkt ist keiner.
    """
    pfad = P(root, ".koolie/core/governance/DECISION_LOG.md".replace("/", os.sep))
    frei(pfad, P46_KLAERUNG)
    zeile_nach(pfad, "| K-35 |",
               "| " + P46_KLAERUNG + " | Sondenklärungspunkt | niedrig | Sondenlauf | "
               "Framework Owner | entschieden (Vorschlag): Sondenauflösung |")


def _46_protokollmarker(root: str) -> None:
    """Ein Marker in einem datierten Protokoll - ausserhalb des Zaehlbereichs.

    Die Gattungsausnahme aus E2. Ein Bericht von gestern ist nicht bearbeitbar; zaehlte
    er mit, stiege Kriterium 1 mit jedem Protokoll, das den Marker erwaehnt, und koennte
    nie sinken.
    """
    ordner = P(root, ".koolie/core/tests/protocols".replace("/", os.sep))
    schreib(os.path.join(ordner, "2026-09-15-sondenprotokoll.md"),
            "# Sondenprotokoll\r\n\r\nGemessen: Mustersemantik " + P46_MARKER + ".\r\n")


sonde("46a", "Eine Zahl der Standzeile steht zu hoch - der Zaehler meldet den nicht "
             "nachgezogenen Fortschritt", lambda r: _46_zahl_verstellen(r, 3, "99"),
      M46_NICHT_NACHGEZOGEN)

sonde("46b", "Ohne Standzeile hat Pruefung 46 ihren Gegenstand verloren und sagt es, "
             "statt leise zu bestehen", _46_standzeile_weg, M46_ANKER)

sonde("46c", "Eine neue unverifizierte Aussage im Kern hebt Kriterium 1, ohne dass "
             "jemand die Standzeile anfasst", _46_marker_dazu, M46_K1)

sonde("46d", "Ein Testblatt an einer Ablage, die keine Liste kennt, hebt Kriterium 2 - "
             "der Befund dieses Antrags", _46_testblatt_dazu, M46_K2)

sonde("46e", "Ein neues Modul auf entwurf hebt Kriterium 3, auch ausserhalb der vier "
             "frueher genannten Ablagen", _46_steckbrief_dazu, M46_K3)

sonde("46f", "Ein zurueckgefallener Decision Record hebt Kriterium 4 - die Standzeile "
             "steht dann zu niedrig", _46_record_zurueckgefallen, M46_RUECKFALL)

gegenprobe("46a", "Das unveraenderte Repositorium bleibt unbeanstandet - alle vier "
                  "Zahlen der Standzeile stimmen", None, "D-11")

gegenprobe("46b", "Ein Klaerungspunkt mit demselben Statuswort bleibt ungezaehlt - "
                  "die alte Regel zaehlte fuenf davon mit", _46_klaerungspunkt_dazu,
           M46_K4)

gegenprobe("46c", "Ein Marker in einem datierten Protokoll bleibt ungezaehlt - ein "
                  "Bericht von gestern ist nicht bearbeitbar", _46_protokollmarker,
           M46_K1)


# --- Selbstprobe C1: der Baumdurchlauf sieht mehr als die Mustersuche ----------------
#
# ANLASS: Die erste Fassung des Zaehlers lief ueber glob.glob(..., recursive=True).
# glob ueberspringt Pfadbestandteile, die mit einem Punkt beginnen - damit fehlten
# fuenfzehn Dateien des Kerns, darunter genau die zwei Traeger
# clients/*/root-template/.devin/README.md und .../.claude/README.md, die den Befund zu
# Kriterium 1 tragen. Der Zaehler haette 27 gemeldet und damit zufaellig die geglaubte
# Zahl bestaetigt.
#
# Eine Zaehlregel, die einen Traeger still ueberspringt, war der ANLASS dieses Antrags.
# Sie ist beim Bauen der Abhilfe ein zweites Mal entstanden - und eine benannte Falle,
# in die man zweimal tritt, gehoert in den Code (D-74). Diese Probe zaehlt beide
# Verfahren auf dem echten Baum gegeneinander ab: Findet glob genauso viel wie os.walk,
# ist entweder der Bestand ohne versteckte Traeger - dann sagt sie das - oder jemand hat
# den Zaehler zurueckgebaut.
#
# GRENZE: Sie misst den Bestand dieses Repositoriums, nicht den eines beliebigen. In
# einem Projekt ohne versteckte Kerndateien ist der Unterschied null, und dann belegt
# sie nichts - das steht dann in ihrer eigenen Meldung.
def selbstprobe_baumdurchlauf() -> None:
    """glob gegen os.walk auf dem echten Kern - der Fallstrick aus CR-2026-070 E7."""
    kern = os.path.join(QUELLE, ".koolie/core")
    mit_glob = {p for p in glob.glob(os.path.join(kern, "**", "*"), recursive=True)
                if os.path.isfile(p)}
    mit_walk = set()
    for ordner, _, dateien in os.walk(kern):
        for name in dateien:
            mit_walk.add(os.path.join(ordner, name))
    versteckt = sorted(mit_walk - mit_glob)
    melde("SELBSTPROBE", "C1", bool(versteckt),
          "Der Baumdurchlauf des Zaehlers findet %d Kerndateien, die eine Mustersuche "
          "ueberspringt" % len(versteckt))
    if not versteckt:
        notiz("        glob und os.walk finden dasselbe. Entweder traegt der Kern keine "
              "versteckte Datei mehr - dann belegt diese Probe nichts -, oder der "
              "Zaehler ist auf glob zurueckgebaut worden (CR-2026-070 E7).")
    else:
        for pfad in versteckt[:3]:
            notiz("        " + os.path.relpath(pfad, QUELLE).replace(os.sep, "/"))


buendel(selbstprobe_baumdurchlauf,
        "Zaehlt Mustersuche gegen Baumdurchlauf auf dem echten Kern - der Fallstrick, "
        "der beim Bauen von Pruefung 46 zuschnappte")

# --- 47: das Statusvokabular jedes Modultraegers ------------------------------------
#
# Die vier Gegenstaende der Pruefung, je eine Sonde - und dazu die Sonde auf den
# verlorenen Anker. Drei der vier Sonden legen eine NEUE Datei an, statt eine
# bestehende zu verstellen: Der Statuswert des Bestands bewegt sich mit jedem Release,
# und eine Sonde, die einen Wert woertlich sucht, misst ab dem naechsten Statuswechsel
# den Suchtext statt die Pruefung (die Lehre von 46f, 0.49.0).
M47_FEHLT = "der Steckbrief führt keine Zeile"
M47_VOKABULAR = "gehört nicht zum Vokabular"
M47_VORLAGE_ECHT = "die Statuszelle einer Vorlage trägt den echten Wert"
M47_SCHLITZ_FREMD = "trägt den Ausfüllschlitz"
M47_ANKER = "kein einziger Steckbrief gefunden"
P47_STECKBRIEFKOPF = "| Attribut | Wert |"
P47_SKILLVORLAGE = ".koolie/core/templates/SKILL_TEMPLATE.md".replace("/", os.sep)
P47_SCHLITZ = "<TBD: Status; ein neuer Skill beginnt auf entwurf>"


def _47_datei(root: str, name: str, statuszeile: str) -> None:
    """Eine neue Prompt-Datei mit Steckbrief und der uebergebenen Statuszeile.

    Eine leere Statuszeile heisst: kein Status im Steckbrief.
    """
    schreib(P(root, (".koolie/core/prompts/" + name).replace("/", os.sep)),
            "# Sondenvorlage\r\n\r\n"
            + P47_STECKBRIEFKOPF + "\r\n|---|---|\r\n"
            "| ID | `FW-PR-013` |\r\n| Version | `0.1.0` |\r\n"
            + (statuszeile + "\r\n" if statuszeile else "")
            + "| Owner (Rolle) | `<FRAMEWORK_OWNER>` |\r\n")


def _47_ohne_statuszeile(root: str) -> None:
    """Ein Steckbrief ohne Statuszeile - genau die zwoelf Traeger aus K-36."""
    _47_datei(root, "13-sonde-ohne-status.md", "")


def _47_fremdes_wort(root: str) -> None:
    """Ein Statuswert ausserhalb des Vokabulars - bis 0.50.0 nur in einer SKILL.md gefangen."""
    _47_datei(root, "13-sonde-vokabular.md", "| Status | `banane` |")


def _47_schlitz_ausserhalb(root: str) -> None:
    """Ein Ausfuellschlitz in einer Datei, die keine Vorlage ist - der Preis aus D-104."""
    _47_datei(root, "13-sonde-schlitz.md",
              "| Status | `<TBD: Status; ein neuer Prompt beginnt auf entwurf>` |")


def _47_vorlage_mit_echtem_wert(root: str) -> None:
    """Der Defekt von 0.50.0, wiederhergestellt: eine Vorlage traegt `entwurf`.

    Die Statuszelle der Skillvorlage gab diesen Wert an jede Kopie weiter und durfte
    sich deshalb nie aendern; genau daran war Kriterium 3 von D-11 unerreichbar
    (D-104). Die Sonde stellt den Zustand HER statt ihn zu entfernen - wie 38a, 38b
    und 46f.
    """
    ersetze(P(root, P47_SKILLVORLAGE), (P47_SCHLITZ, "entwurf"))


def _47_steckbriefkopf_umbenennen(root: str) -> None:
    """Die Kopfzeile jedes Steckbriefs umbenennen - die Pruefung findet keinen mehr.

    Anders als bei den Pruefungen 28, 29, 31, 40 und 46 ist der Anker hier keine
    einzelne Zeichenkette in einer Datei, sondern eine KONVENTION ueber den ganzen
    Bestand. Verliert sie sich, faende die Pruefung nichts mehr und bestuende leise -
    deshalb benennt diese Sonde sie ueberall um und belegt, dass der Lauf das meldet.
    """
    getroffen = 0
    for ordner, _, dateien in os.walk(P(root, ".koolie/core")):
        for name in sorted(dateien):
            if not name.endswith(".md"):
                continue
            pfad = os.path.join(ordner, name)
            text = lies(pfad)
            if P47_STECKBRIEFKOPF not in text:
                continue
            schreib(pfad, text.replace(P47_STECKBRIEFKOPF, "| Merkmal | Wert |"))
            getroffen += 1
    if getroffen < 50:
        raise Praeparationsfehler(
            "nur %d Dateien mit der Steckbriefkopfzeile gefunden, erwartet mindestens "
            "50 - die Konvention hat sich geaendert" % getroffen)


def _47_verlaufszusatz(root: str) -> None:
    """Einem gehobenen Traeger einen Verlaufszusatz in Klammern anhaengen.

    `entwurf (Referenzpack der Erstfassung)` steht seit der Erstfassung im Bestand;
    verglichen wird deshalb das ERSTE WORT. Die Gegenprobe belegt, dass ein solcher
    Zusatz zulaessig bleibt - und dass Pruefung 46 ihn weiterhin richtig einordnet.
    """
    ersetze(P(root, ".koolie/core/checklists/01-preflight.md".replace("/", os.sep)),
            ("| Status | `pilot` |", "| Status | `pilot (Abnahme CR-2026-073)` |"))


def _47_tabelle_hinter_ueberschrift(root: str) -> None:
    """Eine Steckbriefkopfzeile im KOERPER einer Datei ist kein Steckbrief.

    Der Fall von templates/PLAN_TEMPLATE.md: Dort steht die Tabelle hinter einer
    Ueberschrift der Ebene 2 und ist das Formular fuer die Kopie, nicht der Steckbrief
    der Datei. Eine Erkennungsregel, die bloss nach der Kopfzeile sucht, verlangte dort
    einen Statuswert - und die Datei fuehrt zu Recht keinen.
    """
    schreib(P(root, ".koolie/core/examples/example-sondenformular.md"
              .replace("/", os.sep)),
            "# Beispielformular (synthetisch)\r\n\r\n"
            "Ein Formular, das die Kopie ausfuellt - kein Steckbrief.\r\n\r\n"
            "## Formular\r\n\r\n"
            + P47_STECKBRIEFKOPF + "\r\n|---|---|\r\n"
            "| Erstellt mit | `<Skill>` |\r\n| Bestaetigt durch | `<Rolle>` |\r\n")


sonde("47a", "Ein Steckbrief ohne Statuszeile wird gemeldet - das Loch, durch das bis "
             "0.50.0 zwoelf Traeger entkamen", _47_ohne_statuszeile, M47_FEHLT)

sonde("47b", "Ein Statuswert ausserhalb des Vokabulars faellt auf, auch weit weg von "
             "einer SKILL.md", _47_fremdes_wort, M47_VOKABULAR)

sonde("47c", "Eine Vorlage mit echtem Statuswert wird gemeldet - der Defekt, der "
             "Kriterium 3 unerreichbar machte", _47_vorlage_mit_echtem_wert,
      M47_VORLAGE_ECHT)

sonde("47d", "Ein Ausfuellschlitz ausserhalb einer Vorlage wird gemeldet - die "
             "kopierte und nicht gefuellte Vorlage", _47_schlitz_ausserhalb,
      M47_SCHLITZ_FREMD)

sonde("47e", "Ohne die Steckbriefkonvention hat Pruefung 47 ihren Gegenstand verloren "
             "und sagt es, statt leise zu bestehen", _47_steckbriefkopf_umbenennen,
      M47_ANKER)

gegenprobe("47a", "Das unveraenderte Repositorium bleibt unbeanstandet - jeder "
                  "Steckbrief traegt einen gueltigen Statuswert", None, "Vokabular")

gegenprobe("47b", "Ein Verlaufszusatz in Klammern bleibt zulaessig - verglichen wird "
                  "das erste Wort des Werts", _47_verlaufszusatz, M47_VOKABULAR)

gegenprobe("47c", "Eine Steckbriefkopfzeile hinter einer Ueberschrift ist kein "
                  "Steckbrief und verlangt keinen Status", _47_tabelle_hinter_ueberschrift,
           M47_FEHLT)


# --- 48: die Werkzeugneutralitaet des Kerns -----------------------------------------
#
# Die drei Gruende, aus denen Pruefung 12 die siebzehn Fundstellen nicht fand, sind hier
# je eine Sonde: der Pfad des INSTALLIERTEN Packs (Grund 2 - er existiert und war damit
# unsichtbar), der Pfad OHNE Backticks (Grund 1) und die anweisende Spalte des
# Testkatalogs, deren letzte Zelle bewusst ausgenommen ist. Dazu die Sonde auf den
# verlorenen Anker und drei Gegenproben - die Belegspalte, die Chronik und der
# unberuehrte Bestand.
#
# Die Sonden legen NEUE Dateien an, statt bestehende zu verstellen: Ein Suchtext im
# Bestand misst ab dem naechsten Release den Suchtext statt die Pruefung (die Lehre von
# 46f). Welchen Pfad sie schreiben, LESEN sie aus den Manifesten - eine Sonde, die einen
# Pfad raet, misst den geratenen Pfad.
M48_PFAD = "gehört der Laufzeitschicht des Client Packs"
M48_ANKER = "kein Client Pack mit runtime_placeholders gefunden"
P48_KATALOG = ".koolie/core/tests/TEST_CATALOG.md".replace("/", os.sep)
P48_ROADMAP = ".koolie/core/docs/ROADMAP.md".replace("/", os.sep)
P48_KATALOGANKER = "| FW-AK-02 (Basis) |"
P48_ROADMAPANKER = "#### Der Releaseplan bis 1.0.0 und darüber hinaus"


def _48_marken(root: str) -> tuple:
    """(Laufzeitschicht des installierten Packs, die des anderen) - aus den Manifesten.

    Installiert ist das Pack, dessen Laufzeitverzeichnis im Baum wirklich liegt; genau
    darauf beruht der zweite Grund, aus dem Pruefung 12 blind war.
    """
    base = P(root, ".koolie/core", "clients")
    verzeichnisse = []
    for name in sorted(os.listdir(base)):
        if name.startswith("_"):
            continue
        mp = os.path.join(base, name, "manifest.json")
        if os.path.exists(mp):
            verzeichnisse.append(json.loads(lies(mp))["runtime_dir"])
    if len(verzeichnisse) < 2:
        raise Praeparationsfehler(
            "Weniger als zwei Client Packs mit manifest.json - die Sonden zu 48 "
            "brauchen ein installiertes und ein nicht installiertes Pack")
    installiert = [v for v in verzeichnisse if os.path.isdir(P(root, *v.split("/")))]
    fremd = [v for v in verzeichnisse if v not in installiert]
    if not installiert or not fremd:
        raise Praeparationsfehler(
            "Im Baum liegt keine oder jede Laufzeitschicht (%s) - die Sonden zu 48 "
            "unterscheiden das installierte vom nicht installierten Pack"
            % ", ".join(verzeichnisse))
    return installiert[0], fremd[0]


def _48_datei(root: str, name: str, inhalt: str) -> None:
    """Eine neue Prompt-Datei mit vollstaendigem Steckbrief und der Inhaltszeile."""
    schreib(P(root, (".koolie/core/prompts/" + name).replace("/", os.sep)),
            "# Sondenvorlage\r\n\r\n"
            "| Attribut | Wert |\r\n|---|---|\r\n"
            "| ID | `FW-PR-014` |\r\n| Version | `0.1.0` |\r\n"
            "| Status | `pilot` |\r\n"
            "| Owner (Rolle) | `<FRAMEWORK_OWNER>` |\r\n\r\n"
            + inhalt + "\r\n")


def _48_installiertes_pack(root: str) -> None:
    """Der Pfad des INSTALLIERTEN Packs in einem Kerntraeger - Grund 2 der Blindheit.

    Pruefung 12 meldet nur Pfade, die es NICHT GIBT. Dieser hier existiert im Baum und
    lief deshalb sechsundfuenfzig Releases lang durch.
    """
    installiert, _ = _48_marken(root)
    _48_datei(root, "14-sonde-installiert.md",
              "Ausgabeformat: Analyse nach `%s/skills/fw-repo-analyze/SKILL.md`."
              % installiert)


def _48_ohne_backticks(root: str) -> None:
    """Derselbe Befund ohne Backticks - Grund 1 der Blindheit.

    Zehn der siebzehn Fundstellen standen so: im Codeblock, in Prosa oder im
    HTML-Kommentar. Die Heuristik von Pruefung 12 sieht nur Token in Backticks.
    """
    _, fremd = _48_marken(root)
    _48_datei(root, "14-sonde-prosa.md",
              "Die Regeln liegen unter %s/rules und werden bei Sitzungsbeginn geladen."
              % fremd)


def _48_anweisende_spalte(root: str) -> None:
    """Ein Clientpfad in einer ANWEISENDEN Spalte des Testkatalogs wird gemeldet.

    Die Ausnahme dieses Traegers gilt der LETZTEN Zelle (Ergebnisstatus, D-117). Wer
    sie auf die Zeile ausdehnt, nimmt genau die Eingabezelle mit heraus, in der bis
    0.56.2 'Passe AGENTS.md an' stand - der Zuschnitt, der den Gegenstand mitentfernt.
    """
    installiert, _ = _48_marken(root)
    zeile_nach(P(root, P48_KATALOG), P48_KATALOGANKER,
               "| FW-SO-01 | Sondenzeile | Sondenvorbedingung | Anweisung: lies %s/config "
               "| Ablehnung | Zugriff | sitzung | offen |" % installiert)


def _48_anker_verlieren(root: str) -> None:
    """Ohne runtime_placeholders in den Manifesten hat die Pruefung keine Marken mehr.

    Sie leitet sie von dort ab; geht der Schluessel verloren, faende sie nichts und
    bestuende leise. Die Sonde belegt, dass sie das Fehlen selbst meldet (D-23).
    """
    base = P(root, ".koolie/core", "clients")
    getroffen = 0
    for name in sorted(os.listdir(base)):
        mp = os.path.join(base, name, "manifest.json")
        if not os.path.exists(mp):
            continue
        ersetze(mp, ('"runtime_placeholders"', '"runtime_placeholders_alt"'))
        getroffen += 1
    if not getroffen:
        raise Praeparationsfehler(
            "Kein manifest.json unter clients/ - die Ankersonde zu 48 haette nichts "
            "zu verstellen")


def _48_belegspalte(root: str) -> None:
    """Ein Clientpfad in der LETZTEN Zelle einer Testkatalogzeile bleibt zulaessig.

    Der Ergebnisstatus nennt, was ein Lauf gelesen hat, und das gemessene Client Pack
    (D-117). Ein Begriff statt des Pfads waere dort kein Beleg mehr.
    """
    _, fremd = _48_marken(root)
    zeile_nach(P(root, P48_KATALOG), P48_KATALOGANKER,
               "| FW-SO-02 | Sondenzeile | Sondenvorbedingung | Anweisung | Ablehnung "
               "| Zugriff | sitzung | bestanden (`.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278 - der Lauf benennt `%s/rules/00-framework-core.md`) |"
               % fremd)


def _48_chronik(root: str) -> None:
    """Ein Clientpfad in der Roadmap bleibt zulaessig - sie berichtet Erhebungen.

    Dieselbe Begruendung wie bei den Protokollen: Wer einen Befundbericht glaettet,
    macht aus einer richtigen Zeile eine unbelegbare.
    """
    installiert, fremd = _48_marken(root)
    pfad = P(root, P48_ROADMAP)
    schreib(pfad, lies(pfad).rstrip("\r\n") + "\r\n\r\n"
            + "Sondennachtrag zur Erhebung: Der Lauf las %s/rules und legte seine "
              "Ausgabe unter %s/skills ab.\r\n" % (installiert, fremd))


sonde("48a", "Der Pfad des INSTALLIERTEN Packs in einem Kerntraeger wird gemeldet - "
             "genau der Fall, den Pruefung 12 nie sah", _48_installiertes_pack, M48_PFAD)

sonde("48b", "Ein Clientpfad ohne Backticks wird gemeldet - zehn der siebzehn "
             "Fundstellen standen so", _48_ohne_backticks, M48_PFAD)

sonde("48c", "Ein Clientpfad in einer anweisenden Spalte des Testkatalogs wird "
             "gemeldet, obwohl die letzte Zelle ausgenommen ist", _48_anweisende_spalte,
      M48_PFAD)

sonde("48d", "Ohne runtime_placeholders in den Manifesten meldet Pruefung 48 den "
             "verlorenen Gegenstand, statt leise zu bestehen", _48_anker_verlieren,
      M48_ANKER)

gegenprobe("48a", "Das unveraenderte Repositorium bleibt unbeanstandet - die siebzehn "
                  "Fundstellen sind aufgeloest", None, M48_PFAD)

gegenprobe("48b", "Ein Clientpfad in der Ergebnisstatuszelle des Testkatalogs bleibt "
                  "zulaessig - dort ist er der Beleg", _48_belegspalte, M48_PFAD)

gegenprobe("48c", "Ein Clientpfad in der Roadmap bleibt zulaessig - sie fuehrt die "
                  "Erhebungen je Arbeitspaket", _48_chronik, M48_PFAD)


# --- Pruefung 49: ausdruecklicher Skill-Aufruf im Testkatalog (D-146) --------------
#
# Der Befund, der sie veranlasst hat, ist am 2026-09-18 an FW-SC-01 gemessen worden: Der
# Hauptlauf rief `fw-change-small` auf, wurde abgewiesen - neun von zwoelf Kernskills
# fuehren `triggers` ohne `- model`, und das Pack claude-code bildet das auf
# `disable-model-invocation: true` ab - und arbeitete den Ablauf nicht nach. Damit fiel
# Schritt 3 des Skills aus, der die Verwender der geaenderten Einheit erhebt; die
# Scope-Falle konnte nicht zuschnappen. Die Zelle stand danach als `offen`, und die
# Ursache wurde einer Regelkollision zugeschrieben, die es nicht gibt (CR-2026-085).
M49_AUFRUF = "ohne den ausdrücklichen Aufruf"
M49_ANKER = "kein Skill mit 'triggers' ohne '- model' gefunden"
P49_KATALOG = ".koolie/core/tests/TEST_CATALOG.md".replace("/", os.sep)
P49_KATALOGANKER = "| FW-AK-02 (Basis) |"
P49_SKILLS = ".koolie/core/framework/skills".replace("/", os.sep)


def _49_skill_ohne_modell(root: str) -> str:
    """Ein Kernskill, dessen Quelle `triggers` ohne `- model` fuehrt - abgeleitet.

    Die Sonde raet den Namen nicht: Waere er gepflegt, prueften Sonde und Pruefung
    verschiedene Mengen, und die Sonde bestuende an einem Skill, den es nicht mehr gibt.
    """
    basis = P(root, *P49_SKILLS.split(os.sep))
    for name in sorted(os.listdir(basis)):
        pfad = os.path.join(basis, name, "SKILL.md")
        if not os.path.isfile(pfad):
            continue
        text = lies(pfad)
        i = text.find("triggers:")
        if i < 0:
            continue
        block = text[i:text.find("---", 3)] if text.startswith("---") else text[i:i + 200]
        if "- model" not in block:
            return name
    raise Praeparationsfehler(
        "Kein Kernskill mit `triggers` ohne `- model` - die Sonden zu 49 brauchen einen")


def _49_skill_mit_modell(root: str) -> str:
    """Das Gegenstueck: ein Skill, den das Modell von sich aus waehlen darf."""
    basis = P(root, *P49_SKILLS.split(os.sep))
    for name in sorted(os.listdir(basis)):
        pfad = os.path.join(basis, name, "SKILL.md")
        if not os.path.isfile(pfad):
            continue
        text = lies(pfad)
        i = text.find("triggers:")
        if i < 0:
            continue
        block = text[i:text.find("---", 3)] if text.startswith("---") else text[i:i + 200]
        if "- model" in block:
            return name
    raise Praeparationsfehler(
        "Kein Kernskill mit `- model` - die Gegenprobe zu 49 braucht einen")


def _49_katalogzeile(root: str, zeile: str) -> None:
    zeile_nach(P(root, P49_KATALOG), P49_KATALOGANKER, zeile)


def _49_nackte_nennung(root: str) -> None:
    """Der Skillname ohne Schraegstrich im Ausloeser eines `sitzung`-Testfalls.

    Genau die Schreibweise, in der vier Katalogzeilen ihn bis 0.59.1 fuehrten - und in
    der der Prompt zu FW-SC-01 ihn gar nicht fuehrte.
    """
    _49_katalogzeile(root,
        "| FW-SO-03 | Sondenzeile | Sondenvorbedingung | %s mit Sondenaufgabe "
        "| Ablehnung | Zugriff | sitzung | offen |" % _49_skill_ohne_modell(root))


def _49_anker_verlieren(root: str) -> None:
    """Ohne `triggers` in den Skillquellen hat Pruefung 49 keine Marken mehr.

    Sie leitet sie von dort ab; geht der Schluessel verloren, faende sie nichts und
    bestuende leise. Die Sonde belegt, dass sie das Fehlen selbst meldet (D-23).
    """
    basis = P(root, *P49_SKILLS.split(os.sep))
    getroffen = 0
    for name in sorted(os.listdir(basis)):
        pfad = os.path.join(basis, name, "SKILL.md")
        if not os.path.isfile(pfad):
            continue
        if "triggers:" in lies(pfad):
            ersetze(pfad, ("triggers:", "ladeausloeser:"))
            getroffen += 1
    if not getroffen:
        raise Praeparationsfehler(
            "Keine SKILL.md mit `triggers` - die Ankersonde zu 49 haette nichts zu "
            "verstellen")


def _49_ausdruecklicher_aufruf(root: str) -> None:
    """Derselbe Skill als `/name` bleibt zulaessig - das ist der Aufruf selbst."""
    _49_katalogzeile(root,
        "| FW-SO-04 | Sondenzeile | Sondenvorbedingung | `/%s` mit Sondenaufgabe "
        "| Ablehnung | Zugriff | sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |"
        % _49_skill_ohne_modell(root))


def _49_modellaufrufbar(root: str) -> None:
    """Ein Skill MIT `- model` bleibt nackt zulaessig - der Zuschnitt ist nicht zu breit.

    Ohne dieses Paar meldete die Pruefung jeden Skillnamen und waere eine Stilregel.
    """
    _49_katalogzeile(root,
        "| FW-SO-05 | Sondenzeile | Sondenvorbedingung | %s mit Sondenaufgabe "
        "| Ablehnung | Zugriff | sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |"
        % _49_skill_mit_modell(root))


def _49_andere_spalte(root: str) -> None:
    """Derselbe Name in einer ANDEREN Spalte bleibt zulaessig - die Regel gilt dem Ausloeser.

    Das Gegenstueck zur Spaltenaufloesung: Wer die Zeile statt der Spalte nimmt, meldet
    auch die Zelle, die das erwartete Verhalten beschreibt - und dort ist die Nennung
    eine Aussage ueber den Lauf, keine Anweisung an ihn.
    """
    _49_katalogzeile(root,
        "| FW-SO-06 | Sondenzeile | Sondenvorbedingung | Sondenaufgabe "
        "| Der Lauf nennt %s als zustaendig | Zugriff | sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |"
        % _49_skill_ohne_modell(root))


def _49_andere_pruefmethode(root: str) -> None:
    """Eine nackte Nennung bei Pruefmethode `review` bleibt zulaessig.

    Die Regel gilt dem Lauf, nicht dem Lesen: Eine Durchsicht ruft keinen Skill auf.
    """
    _49_katalogzeile(root,
        "| FW-SO-07 | Sondenzeile | Sondenvorbedingung | %s mit Sondenaufgabe "
        "| Ablehnung | Zugriff | review | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |"
        % _49_skill_ohne_modell(root))


sonde("49a", "Ein Kernskill ohne Modellzulassung, im Ausloeser eines sitzung-Testfalls "
             "nackt genannt, wird gemeldet", _49_nackte_nennung, M49_AUFRUF)

sonde("49b", "Ohne `triggers` in den Skillquellen meldet Pruefung 49 den verlorenen "
             "Gegenstand, statt leise zu bestehen", _49_anker_verlieren, M49_ANKER)

gegenprobe("49a", "Das unveraenderte Repositorium bleibt unbeanstandet - die vier "
                  "Fundstellen sind auf `/name` gestellt", None, M49_AUFRUF)

gegenprobe("49b", "Derselbe Skill als `/name` bleibt zulaessig - das ist der Aufruf",
           _49_ausdruecklicher_aufruf, M49_AUFRUF)

gegenprobe("49c", "Ein Skill MIT Modellzulassung bleibt nackt zulaessig - der Zuschnitt "
                  "ist nicht zu breit", _49_modellaufrufbar, M49_AUFRUF)

gegenprobe("49d", "Derselbe Name in einer anderen Spalte bleibt zulaessig - die Regel "
                  "gilt dem Ausloeser", _49_andere_spalte, M49_AUFRUF)

gegenprobe("49e", "Eine nackte Nennung bei Pruefmethode `review` bleibt zulaessig - "
                  "eine Durchsicht ruft keinen Skill auf", _49_andere_pruefmethode,
           M49_AUFRUF)


# --- Gegenstand 2: der Ausloeser, der eine UEBUNG nennt (D-172) ----------------------
#
# FW-PO-02 nennt keinen Skill und erbt doch vier: Sein Ausloeser verweist auf UE3. Der
# Zuschnitt ist SCHMAL - gefragt wird, ob UEBERHAUPT ein ausdruecklicher Aufruf
# dasteht. Die beiden Gegenproben belegen genau das: eine fuer den bewussten Zuschnitt
# (FW-SC-01 nennt UE3 und ruft nur den dritten Schritt auf), eine fuer die Uebung ohne
# gesperrten Skill.
M49_UEBUNG = "und damit deren Ablauf"
M49_UEBUNGSANKER = "führt keinen Abschnitt der Form"
P49_UEBUNGSDATEI = ".koolie/core/onboarding/exercises/EXERCISES.md".replace("/", os.sep)


def _49_uebung_ohne_aufruf(root: str) -> None:
    """Ein Ausloeser, der eine Uebung mit gesperrten Skills nennt und keinen Aufruf."""
    _49_katalogzeile(root,
        "| FW-SO-08 | Sondenzeile | Sondenvorbedingung | Ü3 aus "
        "`.koolie/core/onboarding/exercises/EXERCISES.md` | Ablehnung | Zugriff "
        "| sitzung | offen |")


def _49_uebung_mit_einem_aufruf(root: str) -> None:
    """Dieselbe Uebung, aber ein Schritt ausdruecklich aufgerufen - der Fall FW-SC-01."""
    _49_katalogzeile(root,
        "| FW-SO-09 | Sondenzeile | Sondenvorbedingung | Ü3-Änderung, ausgelöst über "
        "`/%s` | Ablehnung | Zugriff | sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |"
        % _49_skill_ohne_modell(root))


def _49_uebung_ohne_gesperrten_skill(root: str) -> None:
    """Eine Uebung, deren Abschnitt nur modellaufrufbare Skills fuehrt - UE1/UE2."""
    _49_katalogzeile(root,
        "| FW-SO-10 | Sondenzeile | Sondenvorbedingung | Ü1 aus "
        "`.koolie/core/onboarding/exercises/EXERCISES.md` | Ablehnung | Zugriff "
        "| sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _49_uebungsanker_verlieren(root: str) -> None:
    """Ohne die Abschnittsueberschriften hat Gegenstand 2 keine Uebungen mehr."""
    pfad = P(root, P49_UEBUNGSDATEI)
    text = lies(pfad)
    if "\n## Ü" not in text:
        raise Praeparationsfehler(
            "EXERCISES.md fuehrt keinen Abschnitt '## Ü<n>' - die Ankersonde zu 49 "
            "haette nichts zu entfernen")
    schreib(pfad, text.replace("\n## Ü", "\n## Uebung "))


sonde("49c", "Ein Ausloeser nennt eine Uebung mit vier gesperrten Skills und keinen "
             "einzigen ausdruecklichen Aufruf - der Fall FW-PO-02",
      _49_uebung_ohne_aufruf, M49_UEBUNG)

sonde("49d", "Ohne die Abschnittsueberschriften der Uebungsdatei meldet Gegenstand 2 "
             "den verlorenen Anker, statt leise zu bestehen", _49_uebungsanker_verlieren,
      M49_UEBUNGSANKER)

gegenprobe("49f", "Dieselbe Uebung mit EINEM ausdruecklichen Aufruf bleibt zulaessig - "
                  "der bewusste Zuschnitt von FW-SC-01", _49_uebung_mit_einem_aufruf,
           M49_UEBUNG)

gegenprobe("49g", "Eine Uebung, deren Abschnitt keinen gesperrten Skill fuehrt, bleibt "
                  "ohne Aufruf zulaessig", _49_uebung_ohne_gesperrten_skill, M49_UEBUNG)


# --- Pruefung 50: Vollstaendigkeit des Klaerungspunktregisters (D-147) -------------
M50_FEHLT = "steht in keiner Registerzeile"
M50_ANKER = "hat ihren Anker verloren"
P50_LOG = ".koolie/core/governance/DECISION_LOG.md".replace("/", os.sep)
P50_ROADMAP = ".koolie/core/docs/ROADMAP.md".replace("/", os.sep)
# Eine Kennung, die es im Register nicht gibt und nie geben wird - die Sonde vergibt
# keine echte. 'Eine synthetische Kennung nimmt nie die naechste freie' (0.59.0).
#
# ZUSAMMENGESETZT, und das ist kein Trick, sondern der Gegenstand: Dieses Skript liegt
# im Kern, und Pruefung 50 meldet jede dort GENANNTE Kennung ohne Registerzeile. Stuende
# sie woertlich hier, muesste sie in die Ausnahmemenge - und dann meldete die Sonde
# nichts mehr. Eine Sonde, deren Gegenstand die eigene Nennung ist, darf sich nicht
# selbst nennen - auch nicht in dem Kommentar, der das erklaert. Der erste Entwurf
# dieses Absatzes tat es, und Pruefung 50 hat ihn gemeldet.
K50_SYNTH = "K-" + "95"


def _50_freie_kennung(root: str) -> str:
    """Belegt, dass die Sondenkennung im Register wirklich fehlt - sonst misst sie nichts."""
    if ("| " + K50_SYNTH + " |") in lies(P(root, P50_LOG)):
        raise Praeparationsfehler(
            "%s steht bereits im Register - die Sonde zu 50 braucht eine freie Kennung"
            % K50_SYNTH)
    return K50_SYNTH


def _50_nennung_ohne_register(root: str) -> None:
    """Eine Kennung wird in einem Kerntraeger genannt und steht in keiner Registerzeile.

    Genau der Fall von K-34 (sieben Traeger, seit 0.32.0) und K-55 (drei Traeger, als
    'neu' angekuendigt und nie eingetragen).
    """
    kennung = _50_freie_kennung(root)
    pfad = P(root, P50_ROADMAP)
    schreib(pfad, lies(pfad).rstrip("\r\n") + "\r\n\r\n"
            + "Sondennachtrag: Offen bleibt die Frage nach dem Sondengegenstand (%s).\r\n"
            % kennung)


def _50_anker_verlieren(root: str) -> None:
    """Ohne den Absatz mit den synthetischen Kennungen hat Pruefung 50 keine Ausnahme mehr.

    Sie leitet sie von dort ab; geht der Absatz verloren, meldete sie jede Sondenkennung
    des Pruefapparats als Befund - oder, schlimmer, man naehme die Liste in den Code.
    """
    ersetze(P(root, P50_LOG),
            ("**Belegte synthetische Kennungen", "**Frueher belegte Kennungen"))


def _50_nennung_mit_register(root: str) -> None:
    """Dieselbe Nennung MIT Registerzeile bleibt zulaessig - das ist der erlaubte Fall."""
    kennung = _50_freie_kennung(root)
    _50_nennung_ohne_register(root)
    zeile_nach(P(root, P50_LOG), "| K-56 | Ein dezentrales Testblatt",
               "| %s | Sondenfrage? | niedrig | Sondenbegruendung | Sondenweg | offen |"
               % kennung)


def _50_synthetische_kennung(root: str) -> None:
    """Eine synthetische Kennung des Pruefapparats bleibt ohne Registerzeile zulaessig.

    Ohne dieses Paar meldete die Pruefung ihre eigenen Sonden - der Zuschnitt waere zu
    breit, und die Ausnahme haette keinen belegten Gegenstand.
    """
    pfad = P(root, P50_ROADMAP)
    schreib(pfad, lies(pfad).rstrip("\r\n") + "\r\n\r\n"
            + "Sondennachtrag: Die Gegenprobe benutzt die synthetische Kennung K-99.\r\n")


sonde("50a", "Eine Kennung, die ein Kerntraeger nennt und das Register nicht fuehrt, "
             "wird gemeldet - der Fall von K-34 und K-55", _50_nennung_ohne_register,
      M50_FEHLT)

sonde("50b", "Ohne den Absatz mit den synthetischen Kennungen meldet Pruefung 50 den "
             "verlorenen Anker, statt leise zu bestehen", _50_anker_verlieren, M50_ANKER)

gegenprobe("50a", "Das unveraenderte Repositorium bleibt unbeanstandet - K-34 und K-55 "
                  "sind nachgetragen", None, M50_FEHLT)

gegenprobe("50b", "Dieselbe Nennung MIT Registerzeile bleibt zulaessig",
           _50_nennung_mit_register, M50_FEHLT)

gegenprobe("50c", "Eine synthetische Kennung des Pruefapparats bleibt ohne Registerzeile "
                  "zulaessig - der Zuschnitt ist nicht zu breit", _50_synthetische_kennung,
           M50_FEHLT)


# --- Pruefung 51: Ausfuellschlitz fuer einen festgelegten Overlay-Wert (D-150) -----
M51_SCHLITZ = "trägt einen Ausfüllschlitz, obwohl"
M51_ANKER = "Kontextquellentabelle mit dem Kopf"
P51_QUELLE = ".koolie/core/templates/project-overlay/OVERLAY.md".replace("/", os.sep)
P51_LAUFZEIT = (".koolie/core/framework/runtime/rules/20-project-overlay.md"
                .replace("/", os.sep))
# Der Stand VOR 0.61.0, woertlich. Die Sonde stellt ihn wieder her: Sie misst genau den
# Befund, den dieses Release behoben hat, und nicht einen nachgebauten.
P51_ALTZEILE = '- Freigegebene externe Domains: `<TBD: Liste oder „keine">`'


def _zeile_ersetzen(pfad: str, praefix: str, neu: str) -> None:
    """Die eine Zeile, die mit `praefix` beginnt, ganz ersetzen.

    Fuer eine Praeparation, deren Gegenstand eine ganze Zeile ist, taugt kein Suchtext
    ueber den Zeileninhalt: Er waere die Zeile selbst und muesste bei jeder Umformulierung
    nachgezogen werden. Der Praefix ist der Feldname, und der ist der Gegenstand.
    """
    zeilen = lies(pfad).split("\r\n")
    treffer = [i for i, z in enumerate(zeilen) if z.startswith(praefix)]
    if len(treffer) != 1:
        raise Praeparationsfehler(
            "%s: Praefix %r steht %dx am Zeilenanfang, erwartet genau einmal"
            % (os.path.basename(pfad), praefix, len(treffer)))
    zeilen[treffer[0]] = neu
    schreib(pfad, "\r\n".join(zeilen))


def _51_schlitz_zurueck(root: str) -> None:
    """Der Stand vor 0.61.0: die Laufzeitfassung bietet an, was die Quelle ausschliesst."""
    _zeile_ersetzen(P(root, P51_LAUFZEIT), "- Freigegebene externe Domains:", P51_ALTZEILE)


def _51_anker_verlieren(root: str) -> None:
    """Ohne die Kontextquellentabelle hat Pruefung 51 keine Feldmenge mehr.

    Sie leitet sie von dort ab; geht der Kopf verloren, pruefte sie nichts und bestuende
    leise - genau die Bauform, die D-23 ausschliesst.
    """
    ersetze(P(root, P51_QUELLE),
            ("| Kontextquelle | Kontextklasse | Freigabe | Bedingungen |",
             "| Quelle | Klasse | Freigabe | Bedingungen |"))


def _51_quelle_oeffnet(root: str) -> None:
    """Legt die QUELLE den Wert nicht fest, ist der Schlitz zulaessig - beides zusammen.

    Das Paar belegt, dass die Pruefung die Quelle liest und nicht ein verdrahtetes Feld:
    Derselbe Schlitz, der eben gemeldet wurde, bleibt unbeanstandet, sobald die Vorlage
    ihn selbst offen laesst.
    """
    _51_schlitz_zurueck(root)
    ersetze(P(root, P51_QUELLE),
            ("| Freigegebene externe Domains (Fetch) | K0 | **„keine\"** |",
             "| Freigegebene externe Domains (Fetch) | K0 | `<TBD: Liste oder "
             "„keine\">` |"))


def _51_fremdes_feld(root: str) -> None:
    """Ein Schlitz fuer ein Feld, das die Quellentabelle nicht fuehrt, bleibt zulaessig."""
    zeile_nach(P(root, P51_LAUFZEIT), "- Freigegebene externe Domains:",
               "- Freigegebene Sondenquellen: `<TBD: Liste oder „keine\">`")


sonde("51a", "Ein Ausfuellschlitz in der Laufzeitfassung fuer einen Wert, den die "
             "Overlay-Vorlage festlegt, wird gemeldet", _51_schlitz_zurueck, M51_SCHLITZ)

sonde("51b", "Ohne den Kopf der Kontextquellentabelle meldet Pruefung 51 die verlorene "
             "Feldmenge, statt leise zu bestehen", _51_anker_verlieren, M51_ANKER)

gegenprobe("51a", "Das unveraenderte Repositorium bleibt unbeanstandet - die Domainzeile "
                  "traegt seit 0.61.0 den festen Wert", None, M51_SCHLITZ)

gegenprobe("51b", "Laesst die Quelle den Wert selbst offen, bleibt derselbe Schlitz "
                  "zulaessig - die Pruefung liest die Vorlage", _51_quelle_oeffnet,
           M51_SCHLITZ)

gegenprobe("51c", "Ein Schlitz fuer ein Feld ausserhalb der Quellentabelle bleibt "
                  "zulaessig - der Zuschnitt ist nicht zu breit", _51_fremdes_feld,
           M51_SCHLITZ)


# --- Pruefung 52: V6-Gegenstand mit Freigabefolge (D-151) --------------------------
M52_FOLGE = "deren Rechtsfolge eine Freigabe ist"
M52_ANKER = "Delegationsverbotsliste ist nicht mehr auffindbar"
P52_LAUFZEIT = (".koolie/core/framework/runtime/rules/10-privacy-security.md"
                .replace("/", os.sep))
P52_RISIKO = ".koolie/core/framework/core/09-risk-model.md".replace("/", os.sep)
P52_CL06 = ".koolie/core/checklists/06-security.md".replace("/", os.sep)
# Woertlich der Stand vor 0.61.0 - sechzig Releases lang stand er so.
P52_ALTSATZ = (
    "Authentifizierung, Autorisierung, Sitzungsverwaltung, Kryptografie, "
    "Security-Konfiguration, Eingabevalidierung an Systemgrenzen, Verarbeitung "
    "personenbezogener Daten: Kontrollstufe hoch. Nur analysieren und planen; Umsetzung "
    "ausschließlich nach dokumentierter Freigabe durch `<APPROVAL_ROLE>` und "
    "`<SECURITY_CONTACT>`."
)


def _52_altsatz_zurueck(root: str) -> None:
    """Der Stand vor 0.61.0: ein Delegationsverbot in der Aufzaehlung mit Freigabefolge."""
    _zeile_ersetzen(P(root, P52_LAUFZEIT),
                    "Stufe hoch: Authentifizierung, Autorisierung, Sitzungsverwaltung,",
                    P52_ALTSATZ)


def _52_anker_verlieren(root: str) -> None:
    """Ohne die V6-Zeile hat Pruefung 52 keine Begriffe mehr - sie leitet sie von dort ab."""
    ersetze(P(root, P52_RISIKO),
            ("| V6 | Änderungen an Produktionssystemen",
             "| V6-alt | Änderungen an Produktionssystemen"))


def _52_nur_anwendungslogik(root: str) -> None:
    """Dieselbe Freigabefolge OHNE V6-Gegenstand bleibt zulaessig - das ist G-04."""
    zeile_nach(P(root, P52_CL06),
               "## Abbruch- und Eskalationskriterien",
               "\r\nSondennachtrag: Eine Änderung an Kryptografie oder "
               "Sitzungsverwaltung ist Kontrollstufe hoch; die Umsetzung erfolgt nach "
               "dokumentierter Freigabe durch `<APPROVAL_ROLE>`.")


def _52_ohne_freigabefolge(root: str) -> None:
    """Ein V6-Gegenstand OHNE Freigabefolge bleibt zulaessig - die Regel gilt dem Paar."""
    zeile_nach(P(root, P52_CL06),
               "## Abbruch- und Eskalationskriterien",
               "\r\nSondennachtrag: Eine Sicherheitskonfiguration mit Schutzwirkung ist "
               "Kontrollstufe hoch und nicht delegierbar; zulässig sind Analyse und "
               "Planvorschlag.")


def _52_langform_ausgenommen(root: str) -> None:
    """Die Langform, aus der die Begriffe stammen, darf beide Seiten in einem Absatz nennen.

    Ohne diese Ausnahme meldete die Pruefung ausgerechnet den Text, der die Abgrenzung
    ZIEHT - und die Ausnahme ist abgeleitet: es ist die Datei, aus der gelesen wurde.
    """
    zeile_nach(P(root, P52_RISIKO),
               "## 5. Anwendungshinweise (Erläuterung)",
               "\r\nSondennachtrag zur Abgrenzung: Eine Sicherheitskonfiguration bleibt "
               "V6; eine Berechtigungsprüfung in der Anwendungslogik ist Kontrollstufe "
               "hoch, und ihre Umsetzung erfolgt nach dokumentierter Freigabe.")


sonde("52a", "Ein Gegenstand von V6 in einer Aufzaehlung mit Freigabefolge wird gemeldet "
             "- der Stand vor 0.61.0", _52_altsatz_zurueck, M52_FOLGE)

sonde("52b", "Ohne die V6-Zeile der Delegationsverbotsliste meldet Pruefung 52 den "
             "verlorenen Gegenstand, statt leise zu bestehen", _52_anker_verlieren,
      M52_ANKER)

gegenprobe("52a", "Das unveraenderte Repositorium bleibt unbeanstandet - beide Fassungen "
                  "trennen seit 0.61.0 Anwendungslogik vom Betrieb", None, M52_FOLGE)

gegenprobe("52b", "Dieselbe Freigabefolge ohne einen Gegenstand von V6 bleibt zulaessig - "
                  "das ist der erlaubte Fall", _52_nur_anwendungslogik, M52_FOLGE)

gegenprobe("52c", "Ein Gegenstand von V6 ohne Freigabefolge bleibt zulaessig - die Regel "
                  "gilt dem Paar, nicht dem Wort", _52_ohne_freigabefolge, M52_FOLGE)

gegenprobe("52d", "Die Langform, aus der die Begriffe stammen, bleibt ausgenommen - sie "
                  "zieht die Abgrenzung und nennt beide Seiten", _52_langform_ausgenommen,
           M52_FOLGE)


# --- Pruefung 53: Die Kriterium-2-Kette des Releaseplans (D-153) -------------------
M53_KETTE = "Kette des Releaseplans reißt zwischen"
M53_NULL = "Kette des Releaseplans endet bei"
M53_ANKER = "liest den Releaseplan darunter"
P53_ROADMAP = ".koolie/core/docs/ROADMAP.md".replace("/", os.sep)
P53_UEBERSCHRIFT = "#### Der Releaseplan bis 1.0.0 und darüber hinaus"
# Genau der Fehler, den 0.60.0 gemergt hat: Die Zelle wurde aus dem Posten genommen, seine
# Zahl nachgezogen - und die des Folgepostens blieb stehen.
P53_KETTE_SUCH = "Kriterium 2: **"
P53_GLIED_RE = re.compile(r"Kriterium 2: \*\*(\d+) → (\d+)\*\*")


# 🔴 DER ANKER IST ABGELEITET, NICHT GEPFLEGT - UND DAS ZUM DRITTEN MAL IN DREI
# RELEASES. Bis 0.67.0 stand er hier als feste Zeichenkette ("**85 → 0**"), also auf
# dem Inhalt EINES Postens. 0.63.0 hat dieselbe Bauform schon einmal an Gegenprobe 53b
# behoben und den Fall im Kopfkommentar dort beschrieben - die beiden SONDEN blieben
# gepflegt. Der Umbau des Releaseplans in 0.67.0 (ein Posten wird zu sieben) hat 53a
# prompt fallen lassen: "Praeparation gebrochen".
#     Eine Abhilfe gilt fuer die Stelle, an der sie eingetragen wird, nicht fuer die
#     Bauform. Wer eine findet, sucht ihre Geschwister im selben Block.
def _53_letztes_glied(root: str) -> str:
    """Die LETZTE Kettenzeile des Plans - sie schliesst die Kette und endet bei null."""
    text = lies(P(root, P53_ROADMAP))
    kette = [z for z in text.replace("\r\n", "\n").split("\n")
             if P53_KETTE_SUCH in z and P53_GLIED_RE.search(z)]
    if not kette:
        raise Praeparationsfehler(
            "ROADMAP.md: keine Zeile mit einer Kriterium-2-Kette gefunden - die Sonde "
            "zu 53 haette keinen Anker")
    return kette[-1]


def _53_kette_reissen(root: str) -> None:
    """Der Stand vor 0.61.0: Der Folgeposten beginnt um eins unter dem Vorgaengerende."""
    glied = _53_letztes_glied(root)
    m = P53_GLIED_RE.search(glied)
    kaputt = P53_GLIED_RE.sub(
        "Kriterium 2: **%d → %s**" % (int(m.group(1)) - 1, m.group(2)), glied)
    ersetze(P(root, P53_ROADMAP), (glied, kaputt))


def _53_null_verfehlen(root: str) -> None:
    """Ein Plan, der nicht bei null ankommt, fuehrt nicht bis 1.0.0."""
    glied = _53_letztes_glied(root)
    m = P53_GLIED_RE.search(glied)
    kaputt = P53_GLIED_RE.sub(
        "Kriterium 2: **%s → %d**" % (m.group(1), int(m.group(2)) + 1), glied)
    ersetze(P(root, P53_ROADMAP), (glied, kaputt))


def _53_anker_verlieren(root: str) -> None:
    """Ohne die Ueberschrift liest Pruefung 53 keinen Plan - und sagt es."""
    ersetze(P(root, P53_ROADMAP),
            (P53_UEBERSCHRIFT, "#### Der Plan bis 1.0.0"))


def _53_glied_anfuegen(root: str) -> None:
    """Ein weiterer Posten, der die Kette fortsetzt, bleibt zulaessig.

    Die Pruefung rechnet eine Kette nach und zaehlt keine Posten; ohne dieses Paar waere
    nicht belegt, dass sie dem Plan folgt statt einer festen Laenge.
    """
    # DER ANKER IST ABGELEITET, NICHT GEPFLEGT - und das ist mit 0.63.0 noetig
    # geworden: Er stand zweimal in zwei Releases auf einer Postennummer, und beide
    # Male hat die Verschiebung des Releaseplans die Gegenprobe fallen lassen
    # ("Praeparation gebrochen"). Gesucht wird die LETZTE Zeile der Kette; dahinter
    # gehoert der Sondenposten, damit die Kette geschlossen bleibt.
    text = lies(P(root, P53_ROADMAP))
    kette = [z for z in text.replace("\r\n", "\n").split("\n")
             if P53_KETTE_SUCH in z]
    if not kette:
        raise Praeparationsfehler(
            "ROADMAP.md: keine Zeile mit einer Kriterium-2-Kette gefunden - die "
            "Gegenprobe haette keinen Anker")
    zeile_nach(P(root, P53_ROADMAP), kette[-1].strip(),
               "| **~0.99.0** | Sondenposten | Kriterium 2: **0 → 0** | nein |")


def _53_nennung_vor_dem_plan(root: str) -> None:
    """Eine Kriterium-2-Angabe VOR der Ueberschrift bleibt zulaessig - der Zuschnitt beginnt dort."""
    ersetze(P(root, P53_ROADMAP),
            (P53_UEBERSCHRIFT,
             "Sondennachtrag: Eine Vorhersage ausserhalb des Plans, Kriterium 2: "
             "**99 → 1**.\r\n\r\n" + P53_UEBERSCHRIFT))


sonde("53a", "Ein Folgeposten, der unter dem Ende seines Vorgaengers beginnt, wird "
             "gemeldet - genau der Fehler, den 0.60.0 gemergt hat", _53_kette_reissen,
      M53_KETTE)

sonde("53b", "Ein Plan, dessen Kette nicht bei null ankommt, wird gemeldet - Kriterium 2 "
             "muss dort ankommen", _53_null_verfehlen, M53_NULL)

sonde("53c", "Ohne die Ueberschrift des Releaseplans meldet Pruefung 53 den verlorenen "
             "Gegenstand, statt leise zu bestehen", _53_anker_verlieren, M53_ANKER)

gegenprobe("53a", "Das unveraenderte Repositorium bleibt unbeanstandet - die Kette "
                  "schliesst und endet bei null", None, M53_KETTE)

gegenprobe("53b", "Ein weiterer Posten, der die Kette fortsetzt, bleibt zulaessig - "
                  "gerechnet wird die Kette, nicht die Laenge", _53_glied_anfuegen,
           M53_KETTE)

gegenprobe("53c", "Eine Kriterium-2-Angabe vor der Ueberschrift bleibt zulaessig - der "
                  "Zuschnitt beginnt am Plan", _53_nennung_vor_dem_plan, M53_KETTE)


# --- Pruefung 54: Zusatzschluessel auf der deklarierten Ebene (D-155) --------------
#
# ZWEI ZUSCHNITTE, UND DER ZWEITE IST DER WICHTIGERE. Das Repositorium traegt eine
# devin-desktop-Testinstallation, und dieses Pack fuehrt settings_extra ABSICHTLICH leer.
# Eine Sonde auf der Kopie des Repositoriums belegt deshalb nur die Deklarationspflicht.
# Was der Befund von 0.62.0 verlangt - dass ein Schluessel mit WERT auf der richtigen
# EBENE ankommt -, ist nur an einer claude-code-Installation zu messen. Das ist B02: nicht,
# dass eine Pruefung falsch prueft, sondern dass sie einen Client nicht sieht.
M54_FEHLT_FELD = "Feld settings_extra fehlt"
M54_FEHLT_KEY = "aus settings_extra fehlt in der obersten Ebene"
M54_EBENE = "steht in dem Objekt permissions statt in der obersten Ebene"
M54_WERT = "das Manifest deklariert in settings_extra aber"
MAN_DD_54 = ".koolie/core/clients/devin-desktop/manifest.json".replace("/", os.sep)


def _54_deklaration_fehlt(root: str) -> None:
    """Das Pack fuehrt das Feld gar nicht - der Stand jedes Packs bis 0.61.0."""
    ersetze(P(root, MAN_DD_54), ('  "settings_extra": {},\r\n', ""))


def _54_leeres_feld_bleibt(root: str) -> None:
    """Gegenprobe: Ein leeres settings_extra ist eine Deklaration und bleibt zulaessig.

    Ohne dieses Paar stuende nur fest, dass die Pruefung ein fehlendes Feld meldet - nicht,
    dass sie die ausdrueckliche Abwesenheit von der Luecke unterscheidet. Genau diese
    Unterscheidung ist ihr Zweck.
    """
    ersetze(P(root, MAN_DD_54),
            ('  "settings_extra": {},\r\n',
             '  "settings_extra": {},\r\n  "_sonde_54": "leer ist eine Deklaration",\r\n'))


def _cc_manifest_54(root: str) -> str:
    return os.path.join(root, ".koolie/core", "clients", "claude-code", "manifest.json")


def sonden_zusatzschluessel() -> None:
    """Wirkungsnachweis an einer claude-code-Installation (D-155).

    Gemessen wird an der ERZEUGTEN Datei, nicht am Manifest: Die Pruefung fragt, ob die
    Verschaerfung ankommt, und das entscheidet die Abbildung, nicht die Deklaration.
    """
    root = installation("claude-code")
    try:
        rechte = os.path.join(root, ".claude", "settings.json")
        ausgang = lies(rechte)

        # --- Gegenprobe: die frische Installation traegt den Schluessel --------------
        # Sie ist hier die wichtigere Haelfte: Sie belegt, dass die Abbildung aus
        # 0.62.0 ueberhaupt etwas ausliefert. Ohne sie bewiese jede Sonde nur, dass die
        # Pruefung irgendetwas meldet.
        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "54c", "autoMemoryEnabled" not in aus,
              "Die frische claude-code-Installation traegt autoMemoryEnabled auf der "
              "obersten Ebene und bleibt unbeanstandet")
        if "autoMemoryEnabled" in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "autoMemoryEnabled" in z)[:400])

        # --- 54a: der Schluessel fehlt ganz - der Stand bis 0.61.0 ------------------
        # Die erzeugte Datei ist LF: install.py schreibt LF, git normalisiert. Ein
        # Suchtext mit \r\n traefe hier NICHT - anders als in den Manifest-Sonden, die
        # gegen das CRLF des Repositoriums laufen.
        schreib(rechte, ersetzt(
            ausgang,
            ('  "autoMemoryEnabled": false,\n', ""),
            quelle=".claude/settings.json"))
        melde("SONDE", "54b", M54_FEHLT_KEY in validator_ausgabe(root),
              "Ein deklarierter Zusatzschluessel fehlt in der erzeugten Datei - die "
              "Verschaerfung kommt nicht an")

        # --- 54b: der Schluessel steht auf der FALSCHEN Ebene -----------------------
        # Der eigentliche Gegenstand: Die Datei bleibt gueltiges JSON, der Schluessel ist
        # da, er wird nur nicht gelesen. Bis 0.61.0 haette nichts es gemeldet.
        schreib(rechte, ersetzt(
            ausgang,
            ('  "autoMemoryEnabled": false,\n', ""),
            ('"permissions": {\n    "defaultMode": "default",',
             '"permissions": {\n    "autoMemoryEnabled": false,\n    '
             '"defaultMode": "default",'),
            quelle=".claude/settings.json"))
        melde("SONDE", "54c", M54_EBENE in validator_ausgabe(root),
              "Derselbe Schluessel INNERHALB von permissions - gueltiges JSON, vom "
              "Client nicht gelesen, und die Pruefung nennt die Ebene")

        # --- 54c: der Wert ist ein anderer als der deklarierte ----------------------
        schreib(rechte, ersetzt(
            ausgang,
            ('  "autoMemoryEnabled": false,\n', '  "autoMemoryEnabled": true,\n'),
            quelle=".claude/settings.json"))
        melde("SONDE", "54d", M54_WERT in validator_ausgabe(root),
              "Der Schluessel steht auf der richtigen Ebene und traegt den "
              "entgegengesetzten Wert - eine Verschaerfung, die keine ist")

        schreib(rechte, ausgang)
    finally:
        aufraeumen(os.path.dirname(root))


sonde("54a", "Ein Pack fuehrt settings_extra gar nicht - der Stand jedes Packs bis "
             "0.61.0, und die Abwesenheit war nicht von der Luecke zu unterscheiden",
      _54_deklaration_fehlt, M54_FEHLT_FELD)

gegenprobe("54a", "Das unveraenderte Repositorium bleibt unbeanstandet - beide Packs "
                  "fuehren beide Felder", None, M54_FEHLT_FELD)

gegenprobe("54b", "Ein LEERES settings_extra ist eine Deklaration und bleibt zulaessig - "
                  "die Pruefung trennt die ausdrueckliche Abwesenheit von der Luecke",
           _54_leeres_feld_bleibt, M54_FEHLT_FELD)

buendel(sonden_zusatzschluessel,
        "Pruefung 54 an einer claude-code-Installation: fehlend, falsche Ebene und "
        "falscher Wert je eigens gemessen, dazu die unveraenderte Installation")


# --- Pruefung 55 und 56: Pflichtplatzhalter und gesperrte Traeger (D-160, D-161) ---
#
# ZWEI ZUSCHNITTE, AUS EINEM GRUND: Teil (a) von Pruefung 55 liest die VORLAGE und laeuft
# im gewoehnlichen Lauf. Teil (b) und Pruefung 56 lesen ein GEFUELLTES Overlay - und das
# Repositorium traegt nur die unausgefuellte Vorlage, in der jeder Wert <TBD> ist.
# Deshalb baut das Buendel eine frische Installation und schreibt genau die zwei
# Bindungszeilen hinein, um die es geht. Alles andere an --strict-overlay meldet dort
# ohnehin, und die Sonden pruefen je auf IHRE Meldung, nicht auf die Fehlerzahl.
M55_VORLAGE = "kommt in der Vorlage aber nicht vor"
M55_ANKER = "keine Zeile trägt 'Pflicht vor Aktivierung' = ja"
M55_BINDUNG = "<ISSUE_TRACKER> wird von"
M56_GESPERRT = "das dasselbe Overlay unter <EXCLUDED_PATHS> führt"
P55_REG = ".koolie/core/docs/PLACEHOLDER_REGISTRY.md".replace("/", os.sep)
P55_VOR = ".koolie/core/templates/project-overlay/OVERLAY.md".replace("/", os.sep)


def _55_vorlage_luecke(root: str) -> None:
    """Ein Pflichtplatzhalter verschwindet aus der Vorlage - der Fall vom 2026-09-18."""
    ersetze(P(root, P55_VOR),
            ("| Änderungsschwelle (`CHANGE_SIZE_THRESHOLD`) |",
             "| Änderungsschwelle |"))


def _55_anker_weg(root: str) -> None:
    """Ohne die Pflichtspalte hat Pruefung 55 keinen Gegenstand - und sagt es."""
    p = P(root, P55_REG)
    text = lies(p)
    # NICHT "| ja |": Eine der 29 Zeilen traegt 'ja (oder „keine")', bliebe stehen,
    # und die Pflichtmenge waere nicht leer - die Sonde maesse dann nichts.
    schreib(p, text.replace("| ja", "| spaeter"))


def _55_ohne_overlayort(root: str) -> None:
    """Gegenprobe: Ein Pflichtplatzhalter, den das Register NICHT im Overlay verortet,
    muss in der Vorlage nicht vorkommen. `<FRAMEWORK_OWNER>` wird in OWNERS.md gesetzt -
    ohne diesen Zuschnitt meldete die Pruefung ihn bei jedem Lauf."""
    p = P(root, P55_VOR)
    text = lies(p)
    schreib(p, text.replace("<FRAMEWORK_OWNER>", "<FRAMEWORK-EIGNER>"))


# 🔴 DIE SPITZEN KLAMMERN GEHOEREN HINEIN (K-88, D-257). Bis 0.83.0 schrieb dieser
# Block `ISSUE_TRACKER` OHNE sie und nannte das eine Bindung - er kam damit durch, weil
# Pruefung 55b `if name in text` fragte. **Die Gegenprobe deckte die Luecke der Pruefung,
# und die Pruefung die der Gegenprobe.** Mit der geschaerften Pruefung faellt die alte
# Form, und genau das ist ihr Wirkungsnachweis.
BINDUNGEN = (
    "\n## Sondenabschnitt (nur fuer den Wirkungsnachweis)\n\n"
    "| Element | Platzhalter | Wert |\n|---|---|---|\n"
    "| Ticketsystem | `<ISSUE_TRACKER>` | Beispiel-Ticketsystem |\n"
    "| Merge-Request-Vorlage | `<MR_TEMPLATE_PATH>` | `%s` |\n"
)

# Dieselbe Tabelle in der Form von 0.83.0: der Name OHNE Klammern. Sie ist der
# Gegenstand der Sonde 55d - ein Overlay, das den Platzhalter nennt und nicht bindet.
BINDUNGEN_NUR_GENANNT = BINDUNGEN.replace("`<ISSUE_TRACKER>`", "`ISSUE_TRACKER`")


def _ov(root: str) -> str:
    return os.path.join(root, ".koolie/project-overlay", "OVERLAY.md")


def sonden_platzhalterbindung() -> None:
    """Wirkungsnachweis fuer Pruefung 55b und 56 an einer gefuellten Installation."""
    root = installation("claude-code")
    try:
        pfad = _ov(root)
        ausgang = lies(pfad)
        # Eine ausgeschlossene Pfadmenge, die nicht <TBD> ist - sonst hat 56 keinen Anker.
        gefuellt = ersetzt(
            ausgang,
            ("`<TBD: z. B. deploy/**, infra/**, config/prod/**, **/fixtures/real/**>`",
             "`deploy/**`, `infra/**`"),
            quelle=".koolie/project-overlay/OVERLAY.md")

        # --- Gegenprobe 55: der gebundene Platzhalter wird nicht beanstandet ---------
        schreib(pfad, gefuellt + BINDUNGEN % ".mr/pull_request_template.md")
        aus = strict_ausgabe(root)
        melde("GEGENPROBE", "55c", M55_BINDUNG not in aus,
              "Ein Overlay, das <ISSUE_TRACKER> BINDET, bleibt unbeanstandet - die "
              "Pruefung misst die Bindung, nicht das Vorhandensein eines Werts")

        # --- Gegenprobe 56: derselbe Baum, Vorlage ausserhalb der Sperre -------------
        melde("GEGENPROBE", "56a", M56_GESPERRT not in aus,
              "Liegt der Wert von <MR_TEMPLATE_PATH> ausserhalb von <EXCLUDED_PATHS>, "
              "bleibt die Vorbedingung zulaessig")

        # --- 55b: die Bindung fehlt, der Kerntext nennt den Platzhalter weiter -------
        # Der gemessene Fall ist die ERSETZUNG: Das Overlay nennt den Wert und den
        # Platzhalter nirgends mehr. In einer frischen Installation steht er noch in
        # der Prosa der Vorlage - die muss die Sonde mit entfernen, sonst gilt er als
        # gebunden und sie maesse nichts.
        ohne = gefuellt.replace("`<ISSUE_TRACKER>`", "Beispiel-Ticketsystem")
        schreib(pfad, ohne + (BINDUNGEN % ".mr/pull_request_template.md").replace(
            "| Ticketsystem | `<ISSUE_TRACKER>` | Beispiel-Ticketsystem |\n", ""))
        melde("SONDE", "55c", M55_BINDUNG in strict_ausgabe(root),
              "Das Overlay nennt den Wert, bindet den Platzhalter aber nicht - genau der "
              "Fall, der am 2026-09-18 fuenf Platzhalter in 65 Fundstellen unaufloesbar "
              "liess")

        # --- 56: die Vorbedingung verlangt einen gesperrten Traeger ------------------
        schreib(pfad, gefuellt + BINDUNGEN % "deploy/pull_request_template.md")
        melde("SONDE", "56a", M56_GESPERRT in strict_ausgabe(root),
              "Eine Vorbedingung verlangt <MR_TEMPLATE_PATH>, und dessen Wert liegt "
              "unter einem ausgeschlossenen Pfad - die Zelle ist nicht fahrbar")

        # --- Gegenprobe 56b: die NACHBARDATEI im selben Verzeichnis ---------------
        # Der erste Entwurf von Pruefung 56 verglich nur das erste Pfadsegment und
        # meldete `.github/pull_request_template.md` gegen `.github/workflows/**`.
        # Ohne dieses Paar stuende nur fest, dass die Pruefung einen gesperrten Pfad
        # findet - nicht, dass sie den ungesperrten Nachbarn in Ruhe laesst.
        nachbar = ersetzt(gefuellt, ("`deploy/**`, `infra/**`",
                                     "`deploy/gen/**`, `infra/**`"),
                          quelle=".koolie/project-overlay/OVERLAY.md")
        schreib(pfad, nachbar + BINDUNGEN % "deploy/pull_request_template.md")
        melde("GEGENPROBE", "56b", M56_GESPERRT not in strict_ausgabe(root),
              "Derselbe Pfadanfang, ein anderer Pfad: `deploy/pull_request_template.md` gegen `deploy/gen/**` bleibt zulaessig - die Pruefung vergleicht Pfade, nicht Anfaenge")

        # --- 55d: GENANNT ist nicht GEBUNDEN (K-88, D-257) --------------------------
        # 🔴 DER GEGENBEWEIS GEGEN DEN VORSTAND. Bis 0.83.0 fragte Pruefung 55b
        # `if name in text`; gegen diesen Baum haette sie GESCHWIEGEN, weil die
        # Buchstaben `ISSUE_TRACKER` im Overlay stehen - nur eben ohne die spitzen
        # Klammern, die den Kerntext aufloesen. Am Uebungsrepositorium waren es 14
        # von 26 Pflichtplatzhaltern, und die Pruefung meldete null.
        ohne_klammern = gefuellt.replace("`<ISSUE_TRACKER>`", "Beispiel-Ticketsystem")
        schreib(pfad, ohne_klammern
                + BINDUNGEN_NUR_GENANNT % ".mr/pull_request_template.md")
        melde("SONDE", "55d", M55_BINDUNG in strict_ausgabe(root),
              "Das Overlay NENNT <ISSUE_TRACKER> (ohne spitze Klammern) und bindet ihn "
              "nicht - bis 0.83.0 blieb genau das unbeanstandet (K-88, D-257)")

        # --- Gegenprobe 55d: dieselbe Tabelle MIT Klammern --------------------------
        schreib(pfad, ohne_klammern + BINDUNGEN % ".mr/pull_request_template.md")
        melde("GEGENPROBE", "55d", M55_BINDUNG not in strict_ausgabe(root),
              "Dieselbe Tabelle mit spitzen Klammern bleibt unbeanstandet - die "
              "Pruefung misst die SCHREIBWEISE der Bindung und nicht den Wert daneben")

        schreib(pfad, ausgang)
    finally:
        aufraeumen(os.path.dirname(root))


sonde("55a", "Ein Pflichtplatzhalter fehlt in der Overlay-Vorlage - ein Projekt, das sie "
             "ausfuellt, begegnet ihm nie", _55_vorlage_luecke, M55_VORLAGE)

sonde("55b", "Ohne die Spalte 'Pflicht vor Aktivierung' meldet Pruefung 55 den "
             "verlorenen Gegenstand, statt leise zu bestehen", _55_anker_weg, M55_ANKER)

gegenprobe("55a", "Das unveraenderte Repositorium bleibt unbeanstandet - die Vorlage "
                  "bietet jeden Pflichtplatzhalter an", None, M55_VORLAGE)

gegenprobe("55b", "Ein Pflichtplatzhalter, den das Register NICHT im Overlay verortet, "
                  "muss in der Vorlage nicht stehen", _55_ohne_overlayort, M55_VORLAGE)

buendel(sonden_platzhalterbindung,
        "Pruefung 55b und 56 an einer gefuellten claude-code-Installation: fehlende "
        "Bindung und gesperrter Traeger je eigens gemessen, dazu beide Gegenproben")


# --- Pruefung 57: kein ungebundener Pflichtplatzhalter als Vorbedingung -------------
#
# Der gemessene Fall stammt aus dem Blatt des Role Packs: RE-001-N09 verlangte das
# Uebungs-Overlay "ohne gesetztes <ISSUE_TRACKER>" - genau den Zustand, den Pruefung 55b
# im aktiven Overlay als Fehler meldet. Beide entstanden im SELBEN Release.
#
# WARUM ZWEI GEGENPROBEN. Eine Pruefung, die auf einen Suchtext anschlaegt, belegt mit
# einer Sonde nur, DASS sie meldet. Der Zuschnitt - Teilsatz statt Zelle - wird erst
# durch das Paar belegt: 57b traegt dieselbe Verneinung in einem ANDEREN Teilsatz und
# muss unbeanstandet bleiben. Ohne dieses Paar meldete die Pruefung jede Zelle mit, die
# irgendwo ein "ohne" fuehrt, und niemand saehe es.
M57_UNGEBUNDEN = "als nicht gesetzt ("

P57_BLATT = (".koolie/core/framework/role-packs/requirements-engineering/skills/"
             "role-re-ticket/TESTS.md").replace("/", os.sep)

# Die berichtigte Fassung der Zelle - Anker beider Eingriffe.
P57_HEUTE = "Übungs-Overlay, dessen `<ISSUE_TRACKER>` **gebunden** ist"


def _57_ungebunden(root: str) -> None:
    """Die Vorbedingung verlangt den Pflichtplatzhalter als nicht gesetzt."""
    ersetze(P(root, P57_BLATT),
            (P57_HEUTE, "Übungs-Overlay ohne gesetztes `<ISSUE_TRACKER>`, das"))


def _57_anderer_teilsatz(root: str) -> None:
    """Gegenprobe: dieselbe Verneinung, aber in einem anderen Teilsatz.

    Sie belegt den Zuschnitt. Eine Pruefung, die die ganze Zelle durchsucht, meldet
    diesen Fall mit - und waere damit zu breit.
    """
    ersetze(P(root, P57_BLATT),
            (P57_HEUTE,
             "Übungs-Overlay ohne gesetzte Kontrollstufe; `<ISSUE_TRACKER>` **gebunden**"))


sonde("57a", "Eine Vorbedingung verlangt einen Pflichtplatzhalter als nicht gesetzt - "
             "genau den Zustand, den Pruefung 55b im aktiven Overlay als Fehler meldet",
      _57_ungebunden, M57_UNGEBUNDEN)

gegenprobe("57a", "Das unveraenderte Repositorium bleibt unbeanstandet - keine "
                  "Vorbedingung fordert einen ungebundenen Pflichtplatzhalter",
           None, M57_UNGEBUNDEN)

gegenprobe("57b", "Dieselbe Verneinung in einem anderen Teilsatz bleibt zulaessig - die "
                  "Pruefung arbeitet auf Teilsaetzen und nicht auf ganzen Zellen",
           _57_anderer_teilsatz, M57_UNGEBUNDEN)


# --- Pruefung 58: Vollstaendigkeit des Decision-Record-Registers (D-169) -----------
M58_FEHLT = "steht in keiner Registerzeile. Ein Register, das seinen Gegenstand"
M58_FORM = "ist keine Kennung der Form D-NNN"
M58_ANKER = "Prüfung 58 hat ihren Gegenstand verloren"
P58_LOG = ".koolie/core/governance/DECISION_LOG.md".replace("/", os.sep)
P58_ROADMAP = ".koolie/core/docs/ROADMAP.md".replace("/", os.sep)
# ZUSAMMENGESETZT, aus demselben Grund wie bei der Sonde zu Pruefung 50: Dieses Skript
# liegt im Kern, und die Pruefung meldet jede dort GENANNTE Kennung ohne Registerzeile.
# Stuende eine der beiden woertlich hier, muesste sie in die Ausnahmemenge - und dann
# maesse die Sonde nichts. Auch der Kommentar nennt sie nicht.
D58_SYNTH = "D-" + "993"
D58_VERFEHLT = "D-" + "16" + "n"


def _58_freie_kennung(root: str) -> None:
    """Belegt, dass beide Sondenkennungen wirklich fehlen - sonst messen sie nichts."""
    text = lies(P(root, P58_LOG))
    for kennung in (D58_SYNTH, D58_VERFEHLT):
        if ("| " + kennung + " |") in text:
            raise Praeparationsfehler(
                "%s steht bereits im Register - die Sonde zu 58 braucht eine freie "
                "Kennung" % kennung)


def _58_nennung_ohne_register(root: str) -> None:
    """Eine Kennung wird in einem Kerntraeger genannt und steht in keiner Registerzeile."""
    _58_freie_kennung(root)
    pfad = P(root, P58_ROADMAP)
    schreib(pfad, lies(pfad).rstrip("\r\n") + "\r\n\r\n"
            + "Sondennachtrag: Die Begruendung steht im Entscheidungssatz (%s).\r\n"
            % D58_SYNTH)


def _58_form_verfehlt(root: str) -> None:
    """Der gemessene Fall: eine Kennung mit Platzhalter statt Nummer.

    Genau die Bauform, mit der die Registereintraege der Pruefungen 55 und 56
    ausgeliefert worden sind - und die ein Muster mit abschliessender Wortgrenze
    uebersieht.
    """
    _58_freie_kennung(root)
    pfad = P(root, P58_ROADMAP)
    schreib(pfad, lies(pfad).rstrip("\r\n") + "\r\n\r\n"
            + "Sondennachtrag: Die Begruendung steht im Entscheidungssatz (%s).\r\n"
            % D58_VERFEHLT)


def _58_anker_verlieren(root: str) -> None:
    """Ohne Registerzeilen hat Pruefung 58 keinen Gegenstand - und sagt es."""
    pfad = P(root, P58_LOG)
    text = lies(pfad)
    neu = re.sub(r"(?m)^\|(\s*)D-(\d+)(\s*)\|", r"|\1DR-\2\3|", text)
    if neu == text:
        raise Praeparationsfehler(
            "Keine Registerzeile der Form '| D-NNN |' gefunden - die Sonde zum "
            "verlorenen Anker haette nichts entfernt")
    schreib(pfad, neu)


def _58_nennung_mit_register(root: str) -> None:
    """Dieselbe Nennung MIT Registerzeile bleibt zulaessig - der erlaubte Fall."""
    _58_nennung_ohne_register(root)
    zeile_nach(P(root, P58_LOG), "| D-162 |",
               "| %s | Sondenentscheidung | Sondenbegruendung | 2026-09-18 | "
               "entschieden | Sondenweg |" % D58_SYNTH)


sonde("58a", "Eine D-Kennung, die ein Kerntraeger nennt und das Register nicht fuehrt, "
             "wird gemeldet - die Schwester des Falls von K-34 und K-55",
      _58_nennung_ohne_register, M58_FEHLT)

sonde("58b", "Eine Kennung mit Platzhalter statt Nummer wird gemeldet - genau die "
             "Bauform, mit der zwei Registereintraege ausgeliefert worden sind",
      _58_form_verfehlt, M58_FORM)

sonde("58c", "Ohne Registerzeilen meldet Pruefung 58 den verlorenen Gegenstand, statt "
             "leise zu bestehen", _58_anker_verlieren, M58_ANKER)

gegenprobe("58a", "Das unveraenderte Repositorium bleibt unbeanstandet - jede genannte "
                  "D-Kennung steht im Register", None, M58_FEHLT)

gegenprobe("58b", "Dieselbe Nennung MIT Registerzeile bleibt zulaessig - gemessen wird "
                  "das Fehlen der Zeile und nicht die Nennung", _58_nennung_mit_register,
           M58_FEHLT)


# --- Pruefung 60: der Befehlsschlitz, den der Ausloeser braucht (D-178) -----------
#
# Die Marken sind die Meldungstexte der Pruefung, nicht ihre Nummer: Eine Sonde, die
# auf eine Nummer ankert, bricht bei der naechsten Umnummerierung.
M60_FEHLT = "die Vorbedingung nennt den Schlitz nicht"
M60_ANKER = "kein Skill mit 'Exec(<..._COMMAND>)' im Frontmatter gefunden"
P60_KATALOG = ".koolie/core/tests/TEST_CATALOG.md".replace("/", os.sep)
P60_KATALOGANKER = "| FW-AK-02 (Basis) |"
P60_SKILLS = ".koolie/core/framework/skills".replace("/", os.sep)


# 🔴 Die eingefuegten Zeilen tragen `bestanden (Sondenbeleg, <Protokoll>; Client Pack <Kennung> <Version>)`, nicht `offen`. Eine
# Zeile mit `offen` hebt Kriterium 2 um eins, und Pruefung 46 meldet dann einen
# Rueckfall - die Gegenprobe saehe einen Fehler, den sie nicht gemeint hat.
# Gemessen am 2026-09-18: drei Abweichungen im ersten Sondenlauf zu 60.
#     Wer einen erlaubten Fall herstellt, muss ihn VOLLSTAENDIG herstellen.
def _60_katalogzeile(root: str, zeile: str) -> None:
    zeile_nach(P(root, P60_KATALOG), P60_KATALOGANKER, zeile)


def _60_ohne_schlitz(root: str) -> None:
    """Ein sitzung-Testfall ruft `/fw-change-small` und nennt keinen Befehlsschlitz.

    Genau die Gestalt, in der FW-SC-01 zwei Releases lang dastand - und die zwei
    Laeufe gekostet hat.
    """
    _60_katalogzeile(root,
        "| FW-SO-08 | Sondenzeile | Sondenvorbedingung ohne Befehlsangabe "
        "| `/fw-change-small \"<Sondenaufgabe>\"` | Ablehnung | Zugriff "
        "| sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _60_mit_schlitz(root: str) -> None:
    """Gegenprobe: dieselbe Zeile, aber die Vorbedingung nennt beide Schlitze."""
    _60_katalogzeile(root,
        "| FW-SO-09 | Sondenzeile | Sondenvorbedingung; `<TEST_COMMAND>` und "
        "`<LINT_COMMAND>` im `allow`-Korb | `/fw-change-small \"<Sondenaufgabe>\"` "
        "| Ablehnung | Zugriff | sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _60_andere_pruefmethode(root: str) -> None:
    """Gegenprobe: derselbe Ausloeser bei Pruefmethode `review`.

    Eine Durchsicht braucht keinen Messbaum; die Regel gilt dem Lauf.
    """
    _60_katalogzeile(root,
        "| FW-SO-10 | Sondenzeile | Sondenvorbedingung ohne Befehlsangabe "
        "| `/fw-change-small \"<Sondenaufgabe>\"` | Ablehnung | Zugriff "
        "| review | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _60_skill_ohne_schlitz(root: str) -> None:
    """Gegenprobe: ein Skill, dessen Frontmatter keinen Befehl ausfuehrt.

    Sie belegt, dass der Zuschnitt nicht zu breit ist. `fw-repo-analyze` ist rein
    lesend und fuehrt keinen Befehlsschlitz.
    """
    _60_katalogzeile(root,
        "| FW-SO-11 | Sondenzeile | Sondenvorbedingung ohne Befehlsangabe "
        "| `/fw-repo-analyze <Sondenmodul>` | Ablehnung | Zugriff "
        "| sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _60_anker_verlieren(root: str) -> None:
    """Ohne `Exec(<..._COMMAND>)` in den Skillquellen hat Pruefung 60 keinen Gegenstand.

    Sie leitet ihn von dort ab; geht der Schluessel verloren, faende sie nichts und
    bestuende leise. Die Sonde belegt, dass sie das Fehlen selbst meldet (D-23).
    """
    basis = P(root, *P60_SKILLS.split(os.sep))
    getroffen = 0
    for name in sorted(os.listdir(basis)):
        pfad = os.path.join(basis, name, "SKILL.md")
        if not os.path.isfile(pfad):
            continue
        text = lies(pfad)
        neu = text.replace("Exec(<TEST_COMMAND>)", "Exec(kein-schlitz)")
        neu = neu.replace("Exec(<LINT_COMMAND>)", "Exec(kein-schlitz)")
        neu = neu.replace("Exec(<BUILD_COMMAND>)", "Exec(kein-schlitz)")
        if neu != text:
            schreib(pfad, neu)
            getroffen += 1
    if not getroffen:
        raise Praeparationsfehler(
            "Kein Skill fuehrt 'Exec(<..._COMMAND>)' im Frontmatter - die Sonde zu 60 "
            "haette keinen Anker")


sonde("60a", "Ein sitzung-Testfall ruft einen Skill auf, der einen Befehlsschlitz "
             "ausfuehrt, und nennt ihn in seiner Vorbedingung nicht - genau die "
             "Gestalt, die FW-SC-01 zwei Laeufe gekostet hat",
      _60_ohne_schlitz, M60_FEHLT)

sonde("60b", "Ohne 'Exec(<..._COMMAND>)' in den Skillquellen meldet Pruefung 60 den "
             "verlorenen Gegenstand, statt leise zu bestehen",
      _60_anker_verlieren, M60_ANKER)

gegenprobe("60a", "Das unveraenderte Repositorium bleibt unbeanstandet - die drei "
                  "betroffenen Zellen nennen ihren Schlitz seit 0.66.0",
           None, M60_FEHLT)

gegenprobe("60b", "Dieselbe Zeile mit beiden Schlitzen in der Vorbedingung bleibt "
                  "zulaessig - das ist die Abhilfe", _60_mit_schlitz, M60_FEHLT)

gegenprobe("60c", "Derselbe Ausloeser bei Pruefmethode `review` bleibt zulaessig - "
                  "eine Durchsicht braucht keinen Messbaum", _60_andere_pruefmethode,
           M60_FEHLT)

gegenprobe("60d", "Ein Skill, dessen Frontmatter keinen Befehl ausfuehrt, bleibt ohne "
                  "Befehlsangabe zulaessig - der Zuschnitt ist nicht zu breit",
           _60_skill_ohne_schlitz, M60_FEHLT)


# --- Pruefung 61: das Pruefmittelwort stammt aus dem Vokabular (D-181) ------------
#
# ANLASS. Die dreizehn Testblaetter trugen bis 0.67.0 das Wort `manuell` - 87 von 87
# Zellen -, und es steht in keinem Vokabular. Die Pruefungen 49 und 60 filtern auf
# `sitzung` und hatten dort NULL Gegenstand; nach der Umstellung meldete 60 zwanzig
# Zellen. Die Sonden treffen beide Orte, an denen das Wort steht: den zentralen
# Katalog und ein Blatt. Die Gegenproben belegen den zulaessigen Zusatz - ohne sie
# stuende nur fest, dass die Pruefung etwas meldet, nicht dass sie den richtigen
# Zuschnitt hat.
M61_FREMD = "steht nicht im Vokabular"
M61_ANKER = "keine Zelle mit Prüfmethode gefunden"
P61_KATALOG = ".koolie/core/tests/TEST_CATALOG.md".replace("/", os.sep)
P61_KATALOGANKER = "| FW-AK-02 (Basis) |"
P61_BLATT = ".koolie/core/framework/skills/fw-repo-analyze/TESTS.md".replace("/", os.sep)
P61_BLATTANKER = "| SK-001-N03 |"


def _61_katalogzeile(root: str, zeile: str) -> None:
    zeile_nach(P(root, P61_KATALOG), P61_KATALOGANKER, zeile)


def _61_fremdes_wort(root: str) -> None:
    """Eine Katalogzeile mit dem Wort `manuell` - genau der Stand vor 0.67.0."""
    _61_katalogzeile(root,
        "| FW-SO-12 | Sondenzeile | Sondenvorbedingung "
        "| `/fw-repo-analyze <Sondenmodul>` | Ablehnung | Zugriff "
        "| manuell | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _61_fremdes_wort_im_blatt(root: str) -> None:
    """Dasselbe Wort in einem der dreizehn Blaetter - dort stand es 87-mal."""
    zeile_nach(P(root, P61_BLATT), P61_BLATTANKER,
        "| SK-001-S99 | Sondenzeile | Sondenvorbedingung "
        "| `/fw-repo-analyze <Sondenmodul>` | Ablehnung | Zugriff "
        "| manuell | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _61_zulaessiger_zusatz(root: str) -> None:
    """Gegenprobe: `sitzung` mit Zusatz - die Schreibweise beider Bestaende."""
    _61_katalogzeile(root,
        "| FW-SO-13 | Sondenzeile | Sondenvorbedingung "
        "| `/fw-repo-analyze <Sondenmodul>` | Ablehnung | Zugriff "
        "| sitzung + Skript `validate-output.py --skill fw-repo-analyze` "
        "| bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _61_skript_und_review(root: str) -> None:
    """Gegenprobe: die beiden uebrigen Woerter des Vokabulars bleiben zulaessig.

    Ohne sie belegte der Lauf nur, dass `sitzung` durchkommt - der Zuschnitt waere
    dann zu eng, und niemand saehe es.
    """
    _61_katalogzeile(root,
        "| FW-SO-14 | Sondenzeile | Sondenvorbedingung | Sondeneingabe "
        "| Ablehnung | Zugriff | skript+sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")
    _61_katalogzeile(root,
        "| FW-SO-15 | Sondenzeile | Sondenvorbedingung | Sondeneingabe "
        "| Ablehnung | Zugriff | review | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


sonde("61a", "Eine Katalogzeile mit dem Wort `manuell` - dem Wort, das 87 Blattzellen "
             "trugen und das zwei Pruefungen ihren Gegenstand kostete",
      _61_fremdes_wort, M61_FREMD)

sonde("61b", "Dasselbe Wort in einem der dreizehn Testblaetter: Die Pruefung liest "
             "beide Bestaende, nicht nur den zentralen Katalog",
      _61_fremdes_wort_im_blatt, M61_FREMD)

gegenprobe("61a", "Das unveraenderte Repositorium bleibt unbeanstandet - alle 125 "
                  "Zellen tragen seit 0.67.0 ein Wort des Vokabulars",
           None, M61_FREMD)

gegenprobe("61b", "`sitzung` mit Zusatz bleibt zulaessig - geprueft wird das erste "
                  "Wort, nicht die ganze Zelle", _61_zulaessiger_zusatz, M61_FREMD)

gegenprobe("61c", "`skript+sitzung` und `review` bleiben zulaessig - der Zuschnitt ist "
                  "nicht auf `sitzung` verengt", _61_skript_und_review, M61_FREMD)


# --- Pruefung 62: die Version der Ausgabevorlage (D-185) --------------------------
#
# Die Pruefung ist entstanden, weil ein GEMESSENER LAUF sie veranlasst hat: Im ersten
# Buendellauf der Testblaetter meldete ein Lauf in einer Nebenbemerkung, die
# Attributtabelle seines Skills nenne 0.1.3 und der Kopf der Ausgabevorlage v0.1.1.
#
# ZWEI SONDEN, WEIL DIE FUNDSTELLE ZWEI GESTALTEN HAT: die Kopfzeile der Vorlage und
# die Zeile "Erstellt mit". Eine Sonde auf die Ueberschrift allein haette die zweite
# nicht getroffen - und genau sie trugen zwei Skills doppelt.
M62_WOERTLICH = "nennt die Version wörtlich"

P62_SKILL = ".koolie/core/framework/skills/fw-code-explain/SKILL.md".replace("/", os.sep)
P62_PLAN = ".koolie/core/framework/skills/fw-plan/SKILL.md".replace("/", os.sep)
P62_SCHLITZ = "v<Version aus dem Steckbrief>"


def _62_kopfzeile(root: str) -> None:
    """Die Kopfzeile der Ausgabevorlage traegt wieder eine woertliche Version."""
    ersetze(P(root, P62_SKILL),
            ("## Code-Erklärung – fw-code-explain " + P62_SCHLITZ,
             "## Code-Erklärung – fw-code-explain v9.9.9", 1))


def _62_erstellt_mit(root: str) -> None:
    """Die zweite Gestalt: die Zeile `Erstellt mit` im Ergebnisbericht."""
    ersetze(P(root, P62_PLAN),
            ("| Erstellt mit | fw-plan " + P62_SCHLITZ + " |",
             "| Erstellt mit | fw-plan v9.9.9 |", 1))


def _62_zweiter_schlitz(root: str) -> None:
    """Gegenprobe: der Schlitz darf mehrfach stehen - geprueft wird die ZAHL."""
    ersetze(P(root, P62_SKILL),
            ("## Code-Erklärung – fw-code-explain " + P62_SCHLITZ,
             "## Code-Erklärung – fw-code-explain " + P62_SCHLITZ
             + " (Vorlage " + P62_SCHLITZ + ")", 1))


sonde("62a", "Die Kopfzeile der Ausgabevorlage traegt wieder eine woertliche Version - "
             "genau der Stand vor 0.68.0 in zehn von dreizehn Traegern",
      _62_kopfzeile, M62_WOERTLICH)

sonde("62b", "Dieselbe Zahl in der Zeile `Erstellt mit` - die zweite Gestalt, die ein "
             "Zuschnitt auf die Ueberschrift verfehlt haette",
      _62_erstellt_mit, M62_WOERTLICH)

gegenprobe("62a", "Das unveraenderte Repositorium bleibt unbeanstandet - dreizehn "
                  "Traeger verweisen seit 0.68.0 auf ihren Steckbrief",
           None, M62_WOERTLICH)

gegenprobe("62b", "Der Schlitz darf mehrfach in einer Zeile stehen - geprueft wird die "
                  "woertliche ZAHL, nicht der Buchstabe v",
           _62_zweiter_schlitz, M62_WOERTLICH)


# --- Pruefung 63: der Nummernverweis, der ins Leere zeigt (D-193) ------------------
#
# Drei Sonden, weil der Gegenstand drei Gestalten hat: der Verweis mit vollem Pfad,
# der Verweis mit blossem Dateinamen (vier Testblaetter nennen ihr Ziel so - wer nur
# den vollen Pfad sucht, zaehlt 25 statt 30) und die MITTE einer bis-Spanne.
#
# Die zweite Gegenprobe ist die wichtigere: Eine Aufzeichnung darf denselben Verweis
# tragen, ohne gemeldet zu werden. Ein Protokoll nennt den Stand seines Tages (D-141).
M63_INS_LEERE = "diese Nummer fuehrt dort keine Ueberschrift"

P63_PROMPT = ".koolie/core/prompts/02-impact-analysis.md".replace("/", os.sep)
P63_BLATT = ".koolie/core/framework/skills/fw-error-analyze/TESTS.md".replace("/", os.sep)
P63_ZIEL = ".koolie/core/framework/core/02-privacy.md".replace("/", os.sep)
P63_PROTOKOLL = (".koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-1.md"
                 .replace("/", os.sep))


def _63_voller_pfad(root: str) -> None:
    """Ein anweisender Traeger nennt eine Nummer, die das Ziel nicht fuehrt."""
    ersetze(P(root, P63_PROMPT),
            ("02-privacy.md` Abschnitt 3.3 und 3.4",
             "02-privacy.md` Abschnitt 3.3 und 3.11", 1))


def _63_blosser_name(root: str) -> None:
    """Dieselbe Luecke in der zweiten Ausdrucksform - ohne Pfad, nur Dateiname."""
    ersetze(P(root, P63_BLATT),
            ("`02-privacy.md` Abschnitt 3.3 angefordert",
             "`02-privacy.md` Abschnitt 3.11 angefordert", 1))


def _63_spannenmitte(root: str) -> None:
    """Die MITTE einer bis-Spanne: `3.3 bis 3.5` nennt auch 3.4."""
    ersetze(P(root, P63_ZIEL), ("### 3.4 Tickets", "### 3.4a Tickets", 1))


def _63_aufzeichnung(root: str) -> None:
    """Eine Aufzeichnung traegt denselben Verweis - und bleibt unbeanstandet."""
    zeile_nach(P(root, P63_PROTOKOLL), "# Protokoll",
               "\nGemessen gegen `.koolie/core/framework/core/02-privacy.md` "
               "Abschnitt 3.11 - der Stand jenes Tages.")


sonde("63a", "Ein anweisender Traeger nennt `02-privacy.md` Abschnitt 3.11 - die "
             "Nummer fuehrt dort keine Ueberschrift",
      _63_voller_pfad, M63_INS_LEERE)

sonde("63b", "Dieselbe Luecke im blossen Dateinamen: vier Testblaetter nennen ihr Ziel "
             "ohne Pfad, und wer nur den Pfad sucht, zaehlt 25 statt 30",
      _63_blosser_name, M63_INS_LEERE)

sonde("63c", "Die MITTE einer bis-Spanne: faellt die Ueberschrift 3.4 weg, muss "
             "`Abschnitt 3.3 bis 3.5` sie trotzdem vermissen",
      _63_spannenmitte, M63_INS_LEERE)

gegenprobe("63a", "Das unveraenderte Repositorium bleibt unbeanstandet - seit 0.70.0 "
                  "loesen alle dreissig Nummernverweise auf",
           None, M63_INS_LEERE)

gegenprobe("63b", "Eine Aufzeichnung darf denselben Verweis tragen: Ein Protokoll "
                  "nennt den Stand seines Tages und wird nicht geglaettet (D-141)",
           _63_aufzeichnung, M63_INS_LEERE)

# --- Pruefung 64: die Ausgabemarke, die der Skill nicht verlangt (D-197) ----------
#
# Drei Sonden und drei Gegenproben, und die dritte Gegenprobe ist die wichtigere
# Haelfte: Die LETZTE Zelle einer Zeile ist der Ergebnisstatus und damit eine
# Aufzeichnung (D-117). Ein Lauf, der die Marke geschrieben HAT, darf das dort
# berichten - wer die Zeile statt der Spalte nimmt, entfernt den Gegenstand mit
# (dieselbe Trennlinie, die Pruefung 48 zieht).
#
# 🔴 Die eingefuegten Zeilen tragen `bestanden (Sondenbeleg, <Protokoll>; Client Pack <Kennung> <Version>)`, nicht `offen` - eine
# Zeile mit `offen` hebt Kriterium 2 um eins, und Pruefung 46 meldete dann einen
# Rueckfall (0.66.0). Und sie nennen die Befehlsschlitze in ihrer Vorbedingung,
# sonst meldete Pruefung 60 sie nebenbei mit.
M64_UNGEDECKT = "weder im Ausgabeformat (Abschnitt 5) noch"
M64_ANKER = "keine SKILL.md fuehrt eine Ausgabemarke in Abschnitt 5 oder 6"

P64_KATALOG = ".koolie/core/tests/TEST_CATALOG.md".replace("/", os.sep)
P64_KATALOGANKER = "| FW-AK-02 (Basis) |"
P64_SKILLS = ".koolie/core/framework/skills".replace("/", os.sep)
P64_SCHLITZE = "`<TEST_COMMAND>` und `<LINT_COMMAND>` im `allow`-Korb"


def _64_katalogzeile(root: str, zeile: str) -> None:
    zeile_nach(P(root, P64_KATALOG), P64_KATALOGANKER, zeile)


def _64_rueckfrage_ungedeckt(root: str) -> None:
    """Eine Zelle verlangt [RUECKFRAGE] - die steht in KEINEM Abschnitt 5 oder 6.

    Genau die Gestalt, in der siebzehn Zellen bis 0.73.0 dastanden. `sk004n01` hat
    am 2026-09-19 vorgefuehrt, was sie kostet: Der Lauf hat angehalten und
    zurueckgefragt und die Zeichenfolge nicht geschrieben - weil sie nirgends
    verlangt ist.
    """
    _64_katalogzeile(root,
        "| FW-SO-12 | Sondenzeile | Sondenvorbedingung; " + P64_SCHLITZE +
        " | `/fw-change-small \"<Sondenaufgabe>\"` | [RÜCKFRAGE] zur Aufteilung "
        "| Zugriff | sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _64_halt_ungedeckt(root: str) -> None:
    """Eine Zelle verlangt [HALT] von einem Skill, der sie nur als Anweisung fuehrt.

    `fw-refactor` nennt [HALT] elfmal - in Arbeitsschritten und Fehlerbildern, und
    in keinem Ausgabeformat. Fuenf seiner sieben Zellen standen so da.
    """
    _64_katalogzeile(root,
        "| FW-SO-13 | Sondenzeile | Sondenvorbedingung; " + P64_SCHLITZE +
        " | `/fw-refactor <Sondenmodul> \"<Sondenziel>\"` | [HALT] nach dem "
        "Testnachweis | Zugriff | sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _64_unzulaessig_ungedeckt(root: str) -> None:
    """Dieselbe Luecke in der zweiten gepruefen Spalte: Unzulaessiges Verhalten.

    Wer nur die Erwartungsspalte liest, uebersieht sie - `SK-011-P01` trug die
    Marke in beiden.
    """
    _64_katalogzeile(root,
        "| FW-SO-14 | Sondenzeile | Sondenvorbedingung; " + P64_SCHLITZE +
        " | `/fw-refactor <Sondenmodul> \"<Sondenziel>\"` | Ablehnung "
        "| Änderungen vor dem [HALT] | sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _64_gedeckt(root: str) -> None:
    """Gegenprobe: dieselbe Marke bei einem Skill, der sie in Abschnitt 5 und 6 fuehrt.

    Das ist die Abhilfe - und zugleich der Beleg, dass der Zuschnitt nicht zu breit
    ist. `fw-change-small` fuehrt [HALT] in beiden Abschnitten.
    """
    _64_katalogzeile(root,
        "| FW-SO-15 | Sondenzeile | Sondenvorbedingung; " + P64_SCHLITZE +
        " | `/fw-change-small \"<Sondenaufgabe>\"` | [HALT] vor dem ersten "
        "Schreibzugriff | Zugriff | sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _64_letzte_zelle(root: str) -> None:
    """Gegenprobe: die Marke in der LETZTEN Zelle - dem Ergebnisstatus.

    Ein Lauf, der [HALT] geschrieben HAT, darf das berichten. Die letzte Zelle ist
    eine Aufzeichnung (D-117, D-141); wer die Zeile statt der Spalte nimmt,
    entfernt den Gegenstand mit. Dieselbe Spalten-Ausnahme wie bei Pruefung 48.
    """
    _64_katalogzeile(root,
        "| FW-SO-16 | Sondenzeile | Sondenvorbedingung; " + P64_SCHLITZE +
        " | `/fw-refactor <Sondenmodul> \"<Sondenziel>\"` | Anhalten nach dem "
        "Testnachweis | Zugriff | sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278): der Lauf hat "
        "[HALT] wörtlich geschrieben |")


def _64_anker_verlieren(root: str) -> None:
    """Ohne Marke in Abschnitt 5 oder 6 hat Pruefung 64 keinen Gegenstand.

    Sie leitet ihn von dort ab; geht er verloren, faende sie nichts und bestuende
    leise. Die Sonde belegt, dass sie das Fehlen selbst meldet (D-23).
    """
    basis = P(root, *P64_SKILLS.split(os.sep))
    getroffen = 0
    for name in sorted(os.listdir(basis)):
        pfad = os.path.join(basis, name, "SKILL.md")
        if not os.path.isfile(pfad):
            continue
        text = lies(pfad)
        teile = text.split("## 5. Ausgabeformat")
        if len(teile) != 2:
            continue
        neu = teile[0] + "## 5. Ausgabeformat" + teile[1].replace(
            "[HALT]", "[SONDENMARKE]").replace("[RÜCKFRAGE]", "[SONDENMARKE]")
        if neu != text:
            schreib(pfad, neu)
            getroffen += 1
    if not getroffen:
        raise Praeparationsfehler(
            "Keine SKILL.md fuehrt eine Ausgabemarke ab Abschnitt 5 - die Sonde zu 64 "
            "haette keinen Anker")


sonde("64a", "Eine Zelle verlangt [RUECKFRAGE] - die Marke steht in KEINEM Abschnitt 5 "
             "und KEINEM Abschnitt 6 der zwoelf Skills und ist durchgehend "
             "Handlungsmarke",
      _64_rueckfrage_ungedeckt, M64_UNGEDECKT)

sonde("64b", "Eine Zelle verlangt [HALT] von fw-refactor, das die Marke nur in "
             "Arbeitsschritten und Fehlerbildern fuehrt - fuenf seiner sieben Zellen "
             "standen so da",
      _64_halt_ungedeckt, M64_UNGEDECKT)

sonde("64c", "Dieselbe Luecke in der Spalte Unzulaessiges Verhalten - wer nur die "
             "Erwartungsspalte liest, uebersieht sie",
      _64_unzulaessig_ungedeckt, M64_UNGEDECKT)

sonde("64d", "Ohne Ausgabemarke in Abschnitt 5 oder 6 meldet Pruefung 64 den "
             "verlorenen Gegenstand, statt leise zu bestehen",
      _64_anker_verlieren, M64_ANKER)

gegenprobe("64a", "Das unveraenderte Repositorium bleibt unbeanstandet - seit 0.73.0 "
                  "ist jede der zehn verbliebenen Markennennungen gedeckt",
           None, M64_UNGEDECKT)

gegenprobe("64b", "Dieselbe Marke bei einem Skill, der sie in Abschnitt 5 UND 6 "
                  "fuehrt, bleibt zulaessig - der Zuschnitt ist nicht zu breit",
           _64_gedeckt, M64_UNGEDECKT)

gegenprobe("64c", "Die Marke in der LETZTEN Zelle bleibt zulaessig: Der "
                  "Ergebnisstatus ist eine Aufzeichnung, und ein Lauf, der sie "
                  "geschrieben HAT, darf das berichten (D-117)",
           _64_letzte_zelle, M64_UNGEDECKT)

# --- Pruefung 65: der Ergebnisstatus ohne Beleg (D-202) ---------------------------
#
# Vier Sonden und drei Gegenproben. Die zweite Gegenprobe traegt die Trennlinie: Eine
# `review`-Zelle braucht KEIN Client Pack. D-117 spricht von DYNAMISCHEN Tests; ein
# Dokumentenreview misst keinen Client, und wer die Pflicht auf jede Zelle zieht,
# verlangt eine Angabe, die es nicht gibt.
#
# 🔴 Die eingefuegten Zeilen tragen `bestanden (Sondenbeleg, <Protokoll>; Client Pack
# <Kennung> <Version>)`, nicht `offen` - eine Zeile mit `offen` hebt Kriterium 2 um
# eins, und Pruefung 46 meldete dann einen Rueckfall (0.66.0). Und sie nennen die
# Befehlsschlitze in ihrer Vorbedingung, sonst meldete Pruefung 60 sie nebenbei mit.
M65_KEIN_PROTOKOLL = "nennt kein Protokoll unter"
M65_KEIN_PACK = "nennt kein Client Pack mit Produktversion"
M65_VOKABULAR = "beginnt nicht mit einem Wort des Vokabulars"
M65_ANKER = "das Vokabular des Ergebnisstatus ist unter Punkt 4 nicht mehr auffindbar"

P65_KATALOG = ".koolie/core/tests/TEST_CATALOG.md".replace("/", os.sep)
P65_KATALOGANKER = "| FW-AK-02 (Basis) |"
P65_SCHLITZE = "`<TEST_COMMAND>` und `<LINT_COMMAND>` im `allow`-Korb"
P65_PROTOKOLL = "`.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`"
P65_PACK = "Client Pack `claude-code` 2.1.278"


def _65_katalogzeile(root: str, zeile: str) -> None:
    zeile_nach(P(root, P65_KATALOG), P65_KATALOGANKER, zeile)


def _65_ohne_protokoll(root: str) -> None:
    """Ein `bestanden` ohne Protokollverweis - die Gestalt, die Punkt 4 verbietet.

    Punkt 4 sagt das seit der Erstfassung des Katalogs, und keine Pruefung hat es
    bis 0.74.0 durchgesetzt. Eine Abnahme ohne Beleg ist eine Behauptung.
    """
    _65_katalogzeile(root,
        "| FW-SO-17 | Sondenzeile | Sondenvorbedingung; " + P65_SCHLITZE +
        " | `/fw-refactor <Sondenmodul> \"<Sondenziel>\"` | Anhalten | Zugriff "
        "| sitzung | bestanden (Sondenbeleg ohne Protokollverweis) |")


def _65_ohne_pack(root: str) -> None:
    """Ein `bestanden` einer sitzung-Zelle mit Protokoll, aber ohne Pack und Version.

    Das ist die Haelfte, die D-117 traegt: Ein Ergebnisstatus DECKT KEIN ANDERES
    PACK. Ohne die Version sagt er nicht, gegen welchen Produktstand gemessen wurde -
    und genau das ist am 2026-09-18 an einer vierzig Releases alten Zelle
    aufgefallen (D-113).
    """
    _65_katalogzeile(root,
        "| FW-SO-18 | Sondenzeile | Sondenvorbedingung; " + P65_SCHLITZE +
        " | `/fw-refactor <Sondenmodul> \"<Sondenziel>\"` | Anhalten | Zugriff "
        "| sitzung | bestanden (" + P65_PROTOKOLL + ") |")


def _65_fremdes_wort(root: str) -> None:
    """Ein Statuswort, das im Vokabular von Punkt 4 nicht steht.

    Dieselbe Bauform wie beim Pruefmittelwort `manuell` (D-181): ein Wort, das fuer
    jeden Leser richtig aussieht und fuer jeden Zaehler ein Fremdwort ist.
    """
    _65_katalogzeile(root,
        "| FW-SO-19 | Sondenzeile | Sondenvorbedingung; " + P65_SCHLITZE +
        " | `/fw-refactor <Sondenmodul> \"<Sondenziel>\"` | Anhalten | Zugriff "
        "| sitzung | geprüft (" + P65_PROTOKOLL + "; " + P65_PACK + ") |")


def _65_anker_verlieren(root: str) -> None:
    """Ohne die Vokabularzeile von Punkt 4 hat Pruefung 65 keinen Gegenstand.

    Sie leitet es von dort ab statt es zu pflegen; geht die Zeile verloren, faende
    sie nichts und bestuende leise. Die Sonde belegt, dass sie das Fehlen selbst
    meldet (D-23).
    """
    pfad = P(root, P65_KATALOG)
    text = lies(pfad)
    if "**Ergebnisstatus:**" not in text:
        raise Praeparationsfehler(
            "TEST_CATALOG.md fuehrt die Marke '**Ergebnisstatus:**' nicht mehr - die "
            "Sonde zu 65 haette keinen Anker")
    schreib(pfad, text.replace("**Ergebnisstatus:**", "**Status des Ergebnisses:**", 1))


def _65_review_ohne_pack(root: str) -> None:
    """Gegenprobe: eine review-Zelle mit Protokoll, aber ohne Pack - zulaessig.

    Das ist die Trennlinie, und sie belegt, dass der Zuschnitt nicht zu breit ist:
    D-117 spricht von dynamischen Tests. Ein Dokumentenreview misst keinen Client.
    """
    _65_katalogzeile(root,
        "| FW-SO-20 | Sondenzeile | Sondenvorbedingung | Abgleich zweier Fassungen "
        "| keine Abweichung | Abweichung | review | bestanden (" +
        P65_PROTOKOLL + ") |")


def _65_vollstaendig(root: str) -> None:
    """Gegenprobe: der vollstaendige Fall - Protokoll, Pack und Version.

    Er belegt, dass die Pruefung einen richtig belegten Status durchlaesst; ohne
    ihn wuesste niemand, ob sie ueberhaupt etwas durchlaesst.
    """
    _65_katalogzeile(root,
        "| FW-SO-21 | Sondenzeile | Sondenvorbedingung; " + P65_SCHLITZE +
        " | `/fw-refactor <Sondenmodul> \"<Sondenziel>\"` | Anhalten | Zugriff "
        "| sitzung | bestanden (" + P65_PROTOKOLL + "; " + P65_PACK + ") |")


sonde("65a", "Ein `bestanden` ohne Protokollverweis - Punkt 4 verlangt ihn seit der "
             "Erstfassung, und keine Pruefung hat es durchgesetzt",
      _65_ohne_protokoll, M65_KEIN_PROTOKOLL)

sonde("65b", "Ein `bestanden` einer sitzung-Zelle ohne Client Pack und Produktversion "
             "- ein Ergebnisstatus deckt kein anderes Pack (D-117)",
      _65_ohne_pack, M65_KEIN_PACK)

sonde("65c", "Ein Statuswort ausserhalb des Vokabulars von Punkt 4 - dieselbe Bauform "
             "wie das Pruefmittelwort `manuell` (D-181)",
      _65_fremdes_wort, M65_VOKABULAR)

sonde("65d", "Ohne die Vokabularzeile unter Punkt 4 meldet Pruefung 65 den verlorenen "
             "Gegenstand, statt leise zu bestehen",
      _65_anker_verlieren, M65_ANKER)

gegenprobe("65a", "Das unveraenderte Repositorium bleibt unbeanstandet - alle 125 "
                  "Ergebniszellen tragen ihren Beleg",
           None, M65_KEIN_PROTOKOLL)

gegenprobe("65b", "Eine review-Zelle ohne Client Pack bleibt zulaessig: D-117 spricht "
                  "von DYNAMISCHEN Tests, ein Dokumentenreview misst keinen Client",
           _65_review_ohne_pack, M65_KEIN_PACK)

gegenprobe("65c", "Der vollstaendige Fall - Protokoll, Pack und Version - laeuft durch",
           _65_vollstaendig, M65_KEIN_PROTOKOLL)

# --- Pruefung 59: der Overlay-Wert in der Schicht, die ihn durchsetzt (D-171) ------
#
# Sie braucht eine GEFUELLTE Installation: Im Framework-Repositorium traegt das
# Beispiel-Overlay Ausfuellschlitze, und die Pruefung enthaelt sich dort - richtigerweise,
# denn ein offener Schlitz ist Sache von --check-overlay-ready. Die drei Sonden treffen
# die drei Gegenstaende; die Gegenprobe belegt den vollstaendig nachgezogenen Zustand,
# und sie ist der eigentliche Nachweis: Ohne sie stuende nur fest, dass die Pruefung
# etwas meldet, nicht dass ein richtiger Baum sie schweigen laesst.
M59_BINDUNG = "nennt <EXCLUDED_PATHS> nicht"
M59_WERT = "weichen vom Quell-Overlay ab"
M59_KORB = "keine Regel"
P59_QUELLGLOBS = ["deploy/**", "infra/**"]
P59_SCHLITZ = ("`<TBD: z. B. deploy/**, infra/**, config/prod/**, "
               "**/fixtures/real/**>`")
_59_KORBSTAND: dict = {}


def _59_pfade(root: str) -> tuple:
    return (os.path.join(root, ".koolie/project-overlay", "OVERLAY.md"),
            os.path.join(root, ".claude", "rules", "20-project-overlay.md"),
            os.path.join(root, ".claude", "settings.json"))


def _59_quelle_fuellen(root: str) -> None:
    """Den Ausfuellschlitz des Quell-Overlays einmal durch die Globmenge ersetzen."""
    quelle, _, _ = _59_pfade(root)
    schreib(quelle, ersetzt(lies(quelle),
                            (P59_SCHLITZ, ", ".join("`%s`" % g for g in P59_QUELLGLOBS)),
                            quelle=".koolie/project-overlay/OVERLAY.md"))


def _59_fuellen(root: str, globs: list, im_korb: list = None) -> None:
    """Laufzeitfassung und deny-Korb auf eine Globmenge stellen - mehrfach aufrufbar.

    Die Quelle bleibt unberuehrt: Ihr Ausfuellschlitz gibt es nur einmal, und eine
    Praeparation, die ihn ein zweites Mal sucht, bricht ab. Das ist am 2026-09-18
    zugeschnappt.
    """
    _, laufzeit, korb = _59_pfade(root)
    text = lies(laufzeit)
    treffer = [z for z in text.split("\n") if "<EXCLUDED_PATHS>" in z]
    if len(treffer) != 1:
        raise Praeparationsfehler(
            "Die Laufzeitfassung nennt <EXCLUDED_PATHS> %dx statt 1x - die Sonden zu 59 "
            "haetten keinen Anker" % len(treffer))
    neu = treffer[0].split(":")[0] + ": " + ", ".join("`%s`" % g for g in globs)
    schreib(laufzeit, text.replace(treffer[0], neu))
    cfg = json.loads(lies(korb))
    # Der Korb wird aus dem UNBERUEHRTEN Stand neu aufgebaut, nicht aus dem der
    # vorigen Sonde: Ein Baum, der mehrere Laeufe traegt, ist nach dem ersten
    # Schreiblauf nicht mehr der Ausgangszustand. Ohne diesen Merker stand ein Glob
    # der vorigen Sonde noch im Korb, und 59c mass nichts - zugeschnappt am 2026-09-18.
    urstand = _59_KORBSTAND.setdefault(
        korb, [r for r in cfg["permissions"]["deny"] if "<EXCLUDED_PATHS>" not in r])
    deny = list(urstand)
    for g in (P59_QUELLGLOBS if im_korb is None else im_korb):
        deny += ["Read(%s)" % g, "Edit(%s)" % g]
    cfg["permissions"]["deny"] = deny
    schreib(korb, json.dumps(cfg, ensure_ascii=False, indent=2))


def sonden_overlay_wertabgleich() -> None:
    """Wirkungsnachweis fuer Pruefung 59 an einer gefuellten claude-code-Installation."""
    root = installation("claude-code")
    try:
        # --- Gegenprobe: alle drei Schichten tragen denselben Wert ------------------
        _59_quelle_fuellen(root)
        _59_fuellen(root, P59_QUELLGLOBS)
        aus = strict_ausgabe(root)
        for nummer, marke, satz in (
                ("59a", M59_BINDUNG, "Die Laufzeitfassung bindet den Platzhalter"),
                ("59b", M59_WERT, "Ihre Globmenge ist die der Quelle"),
                ("59c", M59_KORB, "Der deny-Korb fuehrt jeden Glob zweimal")):
            melde("GEGENPROBE", nummer, marke not in aus,
                  "Ein vollstaendig nachgezogener Baum bleibt unbeanstandet - %s" % satz)

        # --- Sonde 59b: derselbe Platzhalter, ein anderer Wert ---------------------
        # Vor 59a, weil 59a den Platzhalter aus der Laufzeitfassung entfernt und
        # _59_fuellen ihn danach als Anker nicht mehr faende.
        _59_fuellen(root, ["deploy/**", "infra/gen/**"])
        melde("SONDE", "59b", M59_WERT in strict_ausgabe(root),
              "Die Laufzeitfassung traegt einen Glob, den die Quelle nicht kennt - genau "
              "die Drift, die eine Einengung aus 0.63.0 nie erreicht hat")

        # --- Sonde 59c: der deny-Korb fuehrt einen Glob der Quelle nicht ------------
        _59_fuellen(root, P59_QUELLGLOBS, im_korb=["deploy/**"])
        melde("SONDE", "59c", M59_KORB in strict_ausgabe(root),
              "Ein ausgeschlossener Pfad der Quelle hat keine Regel im deny-Korb - die "
              "Schicht, die technisch sperrt, kennt ihn nicht")

        # --- Sonde 59a: die Laufzeitfassung ERSETZT statt zu BINDEN -----------------
        _59_fuellen(root, P59_QUELLGLOBS)
        _, laufzeit, _ = _59_pfade(root)
        schreib(laufzeit, lies(laufzeit).replace("(`<EXCLUDED_PATHS>`)", "").replace(
            "<EXCLUDED_PATHS>", "die Liste unten"))
        melde("SONDE", "59a", M59_BINDUNG in strict_ausgabe(root),
              "Die Laufzeitfassung setzt den Wert ein, statt den Platzhalter zu binden - "
              "niemand sieht dann, ob ihr Wert noch der der Quelle ist")
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_overlay_wertabgleich,
        "Pruefung 59 an einer gefuellten claude-code-Installation: Bindung, Wert und "
        "deny-Korb je eigens gemessen, dazu die Gegenprobe des nachgezogenen Baums")


# --- Pruefung 89: die uebrigen Pfadplatzhalter (K-69, D-357) ----------------------
#
# Dieselbe Bauform wie das Buendel zu 59: eine GEFUELLTE claude-code-Installation, je
# Gegenstand eine Sonde, und die Gegenprobe des vollstaendig nachgezogenen Baums ist der
# eigentliche Nachweis. Jede Einheit baut die drei Traeger aus dem UNBERUEHRTEN Stand
# neu auf (_89_URSTAND) - ein Baum, der mehrere Laeufe traegt, ist nach dem ersten
# Schreiblauf nicht mehr der Ausgangszustand (dieselbe Falle wie 59c am 2026-09-18).
#   89   (Gegenprobe) - alle vier Werte in Quelle, Laufzeitfassung und Korb gleich
#   89k  (Gegenprobe) - "kein Wert" in zwei Schreibweisen: `nicht vorhanden` in der
#                       Quelle, `keine` in der Laufzeitfassung - gemessen am Piloten
#   89a  (Sonde)      - die Laufzeitfassung ersetzt <ALLOWED_PATHS>, statt zu binden
#   89b  (Sonde)      - <TEST_PATHS> traegt in der Laufzeitfassung einen anderen Wert
#   89c  (Sonde)      - ein Nur-Lese-Pfad fehlt im deny-Korb
#   89d  (Sonde)      - die Quelle bindet <DOC_PATHS> nicht in der dreispaltigen Zeile
M89_BINDUNG = "nennt <ALLOWED_PATHS> nicht"
M89_WERT = "der Wert von <TEST_PATHS> weicht vom Quell-Overlay ab"
M89_KORB = "hat keine Regel Edit(api-contracts/**)"
M89_QUELLE = "keine Zeile mit der Platzhalterzelle `<DOC_PATHS>`"
M89_ALLE = ("nennt <", "weicht vom Quell-Overlay ab", "Nur-Lese-Pfad",
            "keine Zeile mit der Platzhalterzelle")
P89_WERTE = {"<ALLOWED_PATHS>": ["src/**", "test/**", "docs/**"],
             "<TEST_PATHS>": ["test/**"],
             "<DOC_PATHS>": ["docs/**"],
             "<READ_ONLY_PATHS>": ["api-contracts/**", "db/migrations/**"]}
_89_URSTAND: dict = {}


def _89_pfade(root: str) -> tuple:
    return (os.path.join(root, ".koolie/project-overlay", "OVERLAY.md"),
            os.path.join(root, ".claude", "rules", "20-project-overlay.md"),
            os.path.join(root, ".claude", "settings.json"))


def _89_fuellen(root: str, quelle: dict, laufzeit: dict, korb: list) -> None:
    """Quelle, Laufzeitfassung und deny-Korb aus dem Urstand auf die Werte stellen.

    quelle und laufzeit bilden den Platzhalter auf den eingesetzten TEXT ab (fertig mit
    Codespannen); korb nennt die Nur-Lese-Globs, die eine Schreibsperre bekommen. Jeder
    Ausfuellschlitz muss genau einmal getroffen werden, sonst bricht die Praeparation ab.
    """
    for pfad in _89_pfade(root):
        _89_URSTAND.setdefault(pfad, lies(pfad))
    q_pfad, l_pfad, k_pfad = _89_pfade(root)
    text = _89_URSTAND[q_pfad]
    for platzhalter, ersatz in quelle.items():
        text, n = re.subn(r"(\| `%s` \| )`<TBD[^`]*>`" % re.escape(platzhalter),
                          lambda m: m.group(1) + ersatz, text)
        if n != 1:
            raise Praeparationsfehler("OVERLAY.md: Wertzeile von %s %dx statt 1x"
                                      % (platzhalter, n))
    schreib(q_pfad, text)
    text = _89_URSTAND[l_pfad]
    for platzhalter, ersatz in laufzeit.items():
        text, n = re.subn(r"(\(`%s`\): )`<TBD[^`]*>`" % re.escape(platzhalter),
                          lambda m: m.group(1) + ersatz, text)
        if n != 1:
            raise Praeparationsfehler("20-project-overlay.md: Schlitz von %s %dx statt 1x"
                                      % (platzhalter, n))
    schreib(l_pfad, text)
    cfg = json.loads(_89_URSTAND[k_pfad])
    deny = [r for r in cfg["permissions"]["deny"] if "<READ_ONLY_PATHS>" not in r]
    if len(deny) != len(cfg["permissions"]["deny"]) - 1:
        raise Praeparationsfehler("settings.json: der Schlitz Edit(<READ_ONLY_PATHS>) steht "
                                  "nicht genau einmal im deny-Korb (D-356)")
    cfg["permissions"]["deny"] = deny + ["Edit(%s)" % g for g in korb]
    schreib(k_pfad, json.dumps(cfg, ensure_ascii=False, indent=2))


def _89_spannen(werte: list) -> str:
    return ", ".join("`%s`" % w for w in werte)


def _89_voll() -> tuple:
    werte = {p: _89_spannen(w) for p, w in P89_WERTE.items()}
    return werte, dict(werte), list(P89_WERTE["<READ_ONLY_PATHS>"])


def sonden_overlay_pfadabgleich() -> None:
    """Wirkungsnachweis fuer Pruefung 89 an einer gefuellten claude-code-Installation."""
    root = installation("claude-code")
    try:
        # --- Gegenprobe 89: alle drei Schichten tragen dieselben vier Werte ---------
        _89_fuellen(root, *_89_voll())
        aus = strict_ausgabe(root)
        treffer = [m for m in M89_ALLE if m in aus]
        melde("GEGENPROBE", "89", not treffer,
              "Ein vollstaendig nachgezogener Baum bleibt unbeanstandet - vier Werte in "
              "Quelle, Laufzeitfassung und deny-Korb gleich")
        if treffer:
            notiz("        gemeldet: %s" % ", ".join(treffer))

        # --- Gegenprobe 89k: zwei Schreibweisen fuer "kein Wert" -------------------
        quelle, laufzeit, korb = _89_voll()
        quelle["<DOC_PATHS>"] = "`nicht vorhanden`"
        laufzeit["<DOC_PATHS>"] = "keine"
        _89_fuellen(root, quelle, laufzeit, korb)
        melde("GEGENPROBE", "89k", "<DOC_PATHS>" not in strict_ausgabe(root),
              "Kein Wert in zwei Schreibweisen - nicht vorhanden in der Quelle, keine in "
              "der Laufzeitfassung - ist dieselbe leere Menge")

        # --- Sonde 89a: die Laufzeitfassung ersetzt statt zu binden -----------------
        _89_fuellen(root, *_89_voll())
        _, l_pfad, _ = _89_pfade(root)
        schreib(l_pfad, ersetzt(lies(l_pfad), (" (`<ALLOWED_PATHS>`)", ""),
                                quelle="20-project-overlay.md"))
        melde("SONDE", "89a", M89_BINDUNG in strict_ausgabe(root),
              "Die Laufzeitfassung setzt die erlaubten Pfade ein, statt den Platzhalter zu "
              "binden - ihr Wert ist dann gegen nichts mehr gehalten")

        # --- Sonde 89b: ein anderer Wert in der Laufzeitfassung --------------------
        quelle, laufzeit, korb = _89_voll()
        laufzeit["<TEST_PATHS>"] = "`test/**`, `src/**`"
        _89_fuellen(root, quelle, laufzeit, korb)
        melde("SONDE", "89b", M89_WERT in strict_ausgabe(root),
              "Die Laufzeitfassung erlaubt Schreiben in M4 auf einem Pfad, den die Quelle "
              "nicht nennt - genau die Drift aus K-69")

        # --- Sonde 89c: ein Nur-Lese-Pfad ohne Schreibsperre -----------------------
        quelle, laufzeit, _ = _89_voll()
        _89_fuellen(root, quelle, laufzeit, ["db/migrations/**"])
        melde("SONDE", "89c", M89_KORB in strict_ausgabe(root),
              "Ein Nur-Lese-Pfad der Quelle hat keine Schreibsperre im deny-Korb - der "
              "Integritaetsschutz steht nur im Overlay")

        # --- Sonde 89d: die Quelle bindet anders ------------------------------------
        _89_fuellen(root, *_89_voll())
        q_pfad, _, _ = _89_pfade(root)
        schreib(q_pfad, ersetzt(lies(q_pfad), ("| `<DOC_PATHS>` |", "| DOC_PATHS |"),
                                quelle="OVERLAY.md"))
        melde("SONDE", "89d", M89_QUELLE in strict_ausgabe(root),
              "Ein Overlay, das einen Pfadplatzhalter nicht in der dreispaltigen Zeile "
              "bindet, wird gemeldet und nicht still uebergangen")
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_overlay_pfadabgleich,
        "Pruefung 89 an einer gefuellten claude-code-Installation: Bindung, Wert, deny-Korb "
        "und Lesbarkeit der Quelle, dazu zwei Gegenproben")


# --- D-355: das Overlay-Muster und der Fuellschritt --------------------------------
#
# ANLASS (CR-2026-136, 2.3; CR-2026-138). Ein Muster, das nur OVERLAY.md vorbefuellt,
# sperrt nichts: Read(<EXCLUDED_PATHS>) stand danach woertlich im deny-Korb. Diese
# Einheiten messen den Fuellschritt an einer echten Erstinstallation - und die vier
# Stellen, an denen er sich verweigern MUSS.
#   M355  (Sonde)      - --overlay general fuellt Overlay, Laufzeitfassung und deny-Korb
#                        aus derselben Tabelle; Pruefung 59 schweigt. Gegen install.py
#                        aus 1.4.4 faellt sie (die Option gibt es dort nicht)
#   M355a (Gegenprobe) - ohne --overlay bleibt alles wie vorher: der Schlitz steht
#                        woertlich im Korb, dazu seit D-356 der Nur-Lese-Schlitz
#   M355b (Sonde)      - ein Overlay aus dem Muster ist NICHT aktivierungsreif (D-57)
#   M355c (Sonde)      - vorhandene Saat: Abbruch, nichts ueberschrieben
#   M355d (Sonde)      - ein Muster, das einen freigebenden Platzhalter fuellt: Abbruch
#                        vor dem ersten Schreibvorgang
#   M355e (Sonde)      - --overlay mit --update und ein unbekannter Name: Abbruch
M355_MUSTER = os.path.join(".koolie", "core", "framework", "overlay-patterns", "general.md")
M355_59 = ("nennt <EXCLUDED_PATHS> nicht", "weichen vom Quell-Overlay ab",
           "der ausgeschlossene Pfad")


def _355_install(ziel: str, *argumente) -> subprocess.CompletedProcess:
    return unterprozess([sys.executable, os.path.join(QUELLE, ".koolie/core", "install.py"),
                         "--client", "claude-code", "--root", ziel] + list(argumente))


#   M359  (Sonde)      - die Dokumente des Musters: angelegt, mit Vermerk, im Manifest
#                        als K1/entwurf/on-demand registriert, die Beispiele der Vorlage
#                        ersetzt, die K1-Liste der Laufzeitfassung offen (D-359, D-360)
#   M359a (Sonde)      - Ablage und Beschreibung laufen auseinander: Abbruch vor dem
#                        ersten Schreibvorgang
#   M359b (Sonde)      - ein Dokument ohne Vorschlagsvermerk: Abbruch
#   M359c (Gegenprobe) - ohne --overlay bleibt die Manifestvorlage mit ihren drei
#                        Beispielen, und kein Musterdokument liegt im Projekt
M359_VERMERK = "Muster – vom Overlay Owner zu prüfen und anzupassen."


def _359_dokumente() -> list:
    """Die Dokumente des Musters, gelesen mit dem Werkzeug selbst - nicht nachgepflegt."""
    sys.path.insert(0, os.path.join(QUELLE, ".koolie", "core"))
    try:
        import install as _install  # noqa: E402
        return _install.muster_laden("general")["dokumente"]
    finally:
        sys.path.pop(0)


def _359_kern(basis: str, name: str) -> str:
    """Eine Kopie des Kerns, deren install.py das Muster aus IHREM Kern liest."""
    kern = os.path.join(basis, name, ".koolie", "core")
    shutil.copytree(os.path.join(QUELLE, ".koolie/core"), kern,
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "out"))
    return kern


def _355_werte() -> dict:
    """Die Werte des Musters, gelesen mit dem Werkzeug selbst - nicht nachgepflegt."""
    sys.path.insert(0, os.path.join(QUELLE, ".koolie", "core"))
    try:
        import install as _install  # noqa: E402
        return _install.muster_laden("general")["werte"]
    finally:
        sys.path.pop(0)


def sonden_overlay_muster() -> None:
    """Wirkungsnachweis fuer --overlay general, seine Dokumente und seine sechs Verweigerungen."""
    basis = tempfile.mkdtemp(prefix="lw-muster-")
    try:
        werte = _355_werte()
        # --- M355: die Fuellung ---------------------------------------------------
        root = os.path.join(basis, "mit")
        os.makedirs(root)
        p = _355_install(root, "--overlay", "general")
        deny = json.loads(lies(os.path.join(root, ".claude", "settings.json")))[
            "permissions"]["deny"]
        fehlt = []
        for platzhalter, liste in werte.items():
            if any(platzhalter in r for r in deny):
                fehlt.append("%s noch als Schlitz" % platzhalter)
            for w in liste:
                if not any(r in deny for r in ("Edit(%s)" % w, "Edit(./%s)" % w)):
                    fehlt.append("Edit(%s)" % w)
        for w in werte["<EXCLUDED_PATHS>"]:
            if "Read(%s)" % w not in deny and "Read(./%s)" % w not in deny:
                fehlt.append("Read(%s)" % w)
        laufzeit = lies(os.path.join(root, ".claude", "rules", "20-project-overlay.md"))
        if "(`<EXCLUDED_PATHS>`): " + ", ".join(
                "`%s`" % w for w in werte["<EXCLUDED_PATHS>"]) not in laufzeit:
            fehlt.append("Laufzeitfassung")
        overlay = lies(os.path.join(root, ".koolie", "project-overlay", "OVERLAY.md"))
        for platzhalter, liste in werte.items():
            if "| `%s` | %s |" % (platzhalter, ", ".join("`%s`" % w for w in liste)) \
                    not in overlay:
                fehlt.append("OVERLAY.md %s" % platzhalter)
        if "Overlay angelegt aus dem Muster `general`" not in overlay:
            fehlt.append("Aenderungsverlauf")
        shutil.copytree(os.path.join(QUELLE, ".koolie/core"),
                        os.path.join(root, ".koolie/core"),
                        ignore=shutil.ignore_patterns(".git", "__pycache__", "out"))
        aus59 = [m for m in M355_59 if m in strict_ausgabe(root)]
        melde("SONDE", "M355", p.returncode == 0 and not fehlt and not aus59,
              "Das Muster fuellt Overlay, Laufzeitfassung und deny-Korb aus einer Tabelle, "
              "und Pruefung 59 findet keine Abweichung")
        if p.returncode != 0 or fehlt or aus59:
            notiz("        Exit %d; fehlt: %s; Pruefung 59: %s"
                  % (p.returncode, ", ".join(fehlt) or "nichts", ", ".join(aus59) or "still"))

        # --- M359: die Dokumente des Musters (D-359, D-360) ---------------------------
        dokumente = _359_dokumente()
        fehlt = []
        manifest = lies(os.path.join(root, ".koolie", "project-overlay",
                                     "overlay-manifest.yaml"))
        for dok in dokumente:
            ziel = os.path.join(root, ".koolie", "project-overlay", "documents",
                                dok["typ"], dok["datei"])
            if not os.path.isfile(ziel):
                fehlt.append("%s/%s fehlt" % (dok["typ"], dok["datei"]))
            elif M359_VERMERK not in lies(ziel):
                fehlt.append("%s ohne Vermerk" % dok["typ"])
            eintrag = 'path: ".koolie/project-overlay/documents/%s/%s"' % (
                dok["typ"], dok["datei"])
            if eintrag not in manifest:
                fehlt.append("%s nicht registriert" % dok["typ"])
        for erwartet in ('status: "entwurf"', 'load: "on-demand"', 'context_class: "K1"'):
            if manifest.count(erwartet) != len(dokumente):
                fehlt.append("%s %dx statt %dx" % (erwartet, manifest.count(erwartet),
                                                   len(dokumente)))
        if manifest.count('- id: "DOC-') != len(dokumente):
            fehlt.append("%d Eintraege statt %d - ein Beispiel der Vorlage steht noch"
                         % (manifest.count('- id: "DOC-'), len(dokumente)))
        if "- Dokumente der Klasse K1 (frei nutzbar): `<TBD" not in laufzeit:
            fehlt.append("K1-Liste der Laufzeitfassung gefuellt")
        if "Musterdokumente unter `documents/`" not in overlay:
            fehlt.append("Aenderungsverlauf ohne Dokumente")
        aus8 = [z for z in validator_ausgabe(root).splitlines()
                if z.startswith("FEHLER") and "overlay-manifest.yaml" in z]
        melde("SONDE", "M359", p.returncode == 0 and len(dokumente) == 6 and not fehlt
              and not aus8,
              "Das Muster legt seine sechs Dokumente an, registriert sie als Entwurf und "
              "gibt keines frei; Pruefung 8 bleibt still")
        if fehlt or aus8 or len(dokumente) != 6:
            notiz("        %d Dokumente; fehlt: %s; Pruefung 8: %s"
                  % (len(dokumente), ", ".join(fehlt) or "nichts",
                     " | ".join(aus8) or "still"))

        # --- M355b: nicht aktivierungsreif -----------------------------------------
        q = unterprozess([sys.executable, os.path.join(root, *VALIDATOR.split("/")),
                          "--root", root, "--check-overlay-ready"])
        reif = (q.stdout or "") + (q.stderr or "")
        melde("SONDE", "M355b", q.returncode != 0 and "offene <TBD>-Werte" in reif,
              "Ein Overlay aus dem Muster besteht die Pruefung der Aktivierungsreife nicht - "
              "es laesst die Pflichtwerte offen (D-57)")

        # --- M355c: vorhandene Saat -------------------------------------------------
        vorher = lies(os.path.join(root, ".claude", "settings.json"))
        c = _355_install(root, "--overlay", "general")
        melde("SONDE", "M355c", c.returncode == 1 and "hier liegt sie schon" in
              (c.stderr or "") and lies(os.path.join(root, ".claude", "settings.json"))
              == vorher,
              "Liegt die Saat schon, bricht das Muster ab und ueberschreibt nichts - "
              "vorhandene Saat gehoert dem Projekt")

        # --- M355e: --update und unbekannter Name ----------------------------------
        u = _355_install(root, "--overlay", "general", "--update")
        leer = os.path.join(basis, "unbekannt")
        os.makedirs(leer)
        n = _355_install(leer, "--overlay", "gibt-es-nicht")
        melde("SONDE", "M355e", u.returncode == 1 and "nur bei der Erstinstallation"
              in (u.stderr or "") and n.returncode == 1 and not os.listdir(leer),
              "Das Muster verweigert sich bei --update und bei einem unbekannten Namen, "
              "ohne eine Datei zu schreiben")

        # --- M355a: ohne --overlay unveraendert -------------------------------------
        ohne = os.path.join(basis, "ohne")
        os.makedirs(ohne)
        o = _355_install(ohne)
        deny = json.loads(lies(os.path.join(ohne, ".claude", "settings.json")))[
            "permissions"]["deny"]
        erwartet = ["Read(<EXCLUDED_PATHS>)", "Edit(<CI_CONFIG_PATHS>)",
                    "Edit(<QUALITY_GATE_CONFIG_PATHS>)", "Edit(<READ_ONLY_PATHS>)"]
        melde("GEGENPROBE", "M355a", o.returncode == 0 and all(r in deny for r in erwartet),
              "Ohne Muster bleibt jeder Pfadschlitz woertlich stehen, dazu der Schlitz fuer "
              "die Nur-Lese-Pfade aus D-356")

        # --- M355d: ein Muster, das freigibt ----------------------------------------
        # Gemessen am eigenen Werkzeug einer Kopie: Deren install.py liest das Muster
        # aus IHREM Kern - die Quelle bleibt unberuehrt.
        kopie_kern = os.path.join(basis, "kern", ".koolie", "core")
        shutil.copytree(os.path.join(QUELLE, ".koolie/core"), kopie_kern,
                        ignore=shutil.ignore_patterns(".git", "__pycache__", "out"))
        muster = os.path.join(basis, "kern", M355_MUSTER)
        text = lies(muster)
        anker = "| `<EXCLUDED_PATHS>` |"
        if text.count(anker) != 1:
            raise Praeparationsfehler("general.md: Zeile %s %dx statt 1x"
                                      % (anker, text.count(anker)))
        schreib(muster, text.replace(anker, "| `<ALLOWED_PATHS>` | `**` | Sonde |\r\n"
                                     + anker, 1))
        frei = os.path.join(basis, "frei")
        os.makedirs(frei)
        d = unterprozess([sys.executable, os.path.join(kopie_kern, "install.py"),
                          "--client", "claude-code", "--root", frei,
                          "--overlay", "general"])
        melde("SONDE", "M355d", d.returncode == 1 and "darf nur sperren" in (d.stderr or "")
              and not os.listdir(frei),
              "Ein Muster, das erlaubte Pfade fuellen will, bricht die Installation ab, "
              "bevor die erste Datei geschrieben ist")

        # --- M359a: Ablage und Beschreibung laufen auseinander -----------------------
        kern_a = _359_kern(basis, "kern-a")
        weg = os.path.join(kern_a, "framework", "overlay-patterns", "general", "documents",
                           "security")
        if not os.path.isdir(weg):
            raise Praeparationsfehler("general/documents/security fehlt - M359a haette "
                                      "nichts zu entfernen")
        shutil.rmtree(weg)
        ziel_a = os.path.join(basis, "ziel-a")
        os.makedirs(ziel_a)
        a = unterprozess([sys.executable, os.path.join(kern_a, "install.py"),
                          "--client", "claude-code", "--root", ziel_a, "--overlay", "general"])
        melde("SONDE", "M359a", a.returncode == 1 and "stimmen nicht ueberein" in
              (a.stderr or "") and not os.listdir(ziel_a),
              "Fehlt ein beschriebenes Musterdokument in der Ablage, bricht die Installation "
              "ab, bevor die erste Datei geschrieben ist")

        # --- M359b: ein Dokument ohne Vorschlagsvermerk ------------------------------
        kern_b = _359_kern(basis, "kern-b")
        dok = os.path.join(kern_b, "framework", "overlay-patterns", "general", "documents",
                           "quality", "muster-general.md")
        text = lies(dok)
        if text.count(M359_VERMERK) != 1:
            raise Praeparationsfehler("quality/muster-general.md fuehrt den Vermerk %dx "
                                      "statt 1x" % text.count(M359_VERMERK))
        schreib(dok, text.replace(M359_VERMERK, "Allgemeine Grundsaetze.", 1))
        ziel_b = os.path.join(basis, "ziel-b")
        os.makedirs(ziel_b)
        b = unterprozess([sys.executable, os.path.join(kern_b, "install.py"),
                          "--client", "claude-code", "--root", ziel_b, "--overlay", "general"])
        melde("SONDE", "M359b", b.returncode == 1 and "nicht den Vermerk" in (b.stderr or "")
              and not os.listdir(ziel_b),
              "Ein Musterdokument ohne Vorschlagsvermerk bricht die Installation ab - ein "
              "ungeprueft mitgelieferter Text darf nicht wie eine Projektvorgabe aussehen")

        # --- M359c: ohne --overlay ---------------------------------------------------
        manifest_ohne = lies(os.path.join(ohne, ".koolie", "project-overlay",
                                          "overlay-manifest.yaml"))
        musterdoks = glob.glob(os.path.join(ohne, ".koolie", "project-overlay", "documents",
                                            "*", "muster-general.md"))
        melde("GEGENPROBE", "M359c", manifest_ohne.count('- id: "DOC-') == 3
              and not musterdoks,
              "Ohne Muster bleibt die Manifestvorlage mit ihren drei Beispielen, und kein "
              "Musterdokument liegt im Projekt")
    finally:
        aufraeumen(basis)


buendel(sonden_overlay_muster,
        "Der Fuellschritt aus --overlay general an echten Erstinstallationen, dazu seine "
        "Dokumente, sechs Verweigerungen und der unveraenderte Weg ohne Muster")


# --- D-362: der Kopierweg in ein Projekt, der Dialog und die Starter (CR-2026-140) ---
#
# `install.py --target` kopiert NUR den Kern in ein Projekt und ruft danach das kopierte
# install.py dort auf. Die Sonden fahren es an echten Verzeichnissen, aus BEIDEN
# Quellformen: einer Kopie ohne Git (so liegt ein entpacktes Release-Archiv da) und
# einem Klon, aus dem nur Verfolgtes kommen darf (D-333).
#   T362  (Sonde) - Erstinstallation aus der Archivform: der Kern vollstaendig, ohne
#                   Bytecode und build/out, ohne Kennzeichen und ohne das Overlay der
#                   Quelle (D-354), Wurzeldateien angelegt
#   T362a (Sonde) - ein zweiter Aufruf ohne --update haelt an und veraendert nichts
#   T362b (Sonde) - --update hebt: Stand der Quelle, Altlast weg, Overlay unberuehrt,
#                   keine Zwischenverzeichnisse
#   T362c (Sonde) - scheitert die Installation im Projekt (Kollision), ist der kopierte
#                   Kern wieder weg und die Projektdatei unveraendert
#   T362d (Sonde) - --update ohne vorhandenen Kern haelt an, ohne zu schreiben
#   T362e (Sonde) - Quelle und Ziel dasselbe Verzeichnis: Abbruch
#   T362f (Sonde) - aus einem Klon kommt eine unverfolgte Datei des Kerns NICHT mit
#   T362g (Sonde) - der Dialog sammelt die Angaben ein und installiert
#   T362h (Sonde) - der Dialog bricht mit q ab und schreibt nichts
#   T363  (Sonde) - die Mindestversion steht in install.py und beiden Startern gleich
#   T365  (Sonde) - install.cmd traegt keine Sprungmarke (LF im Archiv), und
#                   install.command ist im Repositorium ausfuehrbar (100755)
T362_ANTWORTEN = "%s\n1\n1\n1\nj\n"


def _362_lauf(kern: str, *argv: str, eingabe=None, werkzeug: str = "install.py"):
    return unterprozess([sys.executable, os.path.join(kern, werkzeug), *argv],
                        input=eingabe)


def _362_kerndateien(kern: str) -> set:
    out = set()
    for dirpath, dirnames, filenames in os.walk(kern):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in filenames:
            out.add(os.path.relpath(os.path.join(dirpath, fn), kern).replace(os.sep, "/"))
    return out


def sonden_kopierweg() -> None:
    """Wirkungsnachweis fuer install.py --target, den Dialog und die Starter (D-362)."""
    basis = tempfile.mkdtemp(prefix="lw-kopierweg-")
    quelle = kopie()
    try:
        qkern = os.path.join(quelle, ".koolie", "core")
        # Erzeugnisse, die ein Lauf in einem entpackten Archiv hinterlaesst - sie
        # duerfen nicht mitkommen.
        os.makedirs(os.path.join(qkern, "__pycache__"), exist_ok=True)
        schreib(os.path.join(qkern, "__pycache__", "sonde.cpython-38.pyc"), "x")
        os.makedirs(os.path.join(qkern, "build", "out"), exist_ok=True)
        schreib(os.path.join(qkern, "build", "out", "sonde.docx"), "x")
        # Seit 1.8.0 schreibt --target die Wahl des Lieferumfangs in den Kern (D-367).
        erwartet = {r for r in _362_kerndateien(qkern) if not r.startswith("build/out/")}
        erwartet.add("LIEFERUMFANG")

        # --- T362: Erstinstallation aus der Archivform -------------------------------
        erst = os.path.join(basis, "erst")
        os.makedirs(erst)
        p = _362_lauf(qkern, "--target", erst, "--client", "claude-code")
        zkern = os.path.join(erst, ".koolie", "core")
        ist = _362_kerndateien(zkern)
        qoverlay = os.path.join(quelle, ".koolie", "project-overlay", "OVERLAY.md")
        zoverlay = os.path.join(erst, ".koolie", "project-overlay", "OVERLAY.md")
        fehlt = []
        if ist != erwartet:
            fehlt.append("Kern: %d zu viel, %d fehlen"
                         % (len(ist - erwartet), len(erwartet - ist)))
        if os.path.exists(os.path.join(erst, ".koolie", "QUELLREPOSITORIUM.md")):
            fehlt.append("Kennzeichen mitkopiert")
        if _367_umfang(erst) != "voll":
            fehlt.append("LIEFERUMFANG " + _367_umfang(erst))
        if not os.path.isfile(zoverlay):
            fehlt.append("kein Overlay")
        elif os.path.isfile(qoverlay) and lies(qoverlay) == lies(zoverlay):
            fehlt.append("Overlay der Quelle mitkopiert")
        if not os.path.isfile(os.path.join(erst, "CLAUDE.md")):
            fehlt.append("keine Wurzel-Anweisungsdatei")
        melde("SONDE", "T362", p.returncode == 0 and not fehlt,
              "Aus der Archivform kommt der ganze Kern ohne Erzeugnisse, ohne Kennzeichen "
              "und ohne das Overlay der Quelle, und das Projekt ist installiert")
        if p.returncode != 0 or fehlt:
            notiz("        Exit %d; %s" % (p.returncode, "; ".join(fehlt) or "-"))

        # --- T362a: zweiter Aufruf ohne --update --------------------------------------
        vorher = baumhash(erst)
        p = _362_lauf(qkern, "--target", erst)
        ok = (p.returncode == 1 and "Heben auf diesen Stand: --update" in p.stderr
              and baumhash(erst) == vorher)
        melde("SONDE", "T362a", ok,
              "Ein vorhandener Kern wird ohne --update nicht ersetzt")
        if not ok:
            notiz("        Exit %d, Baum %s" % (p.returncode,
                  "unveraendert" if baumhash(erst) == vorher else "VERAENDERT"))

        # --- T362b: Heben ----------------------------------------------------------
        schreib(os.path.join(zkern, "VERSION"), "0.0.0\n")
        schreib(os.path.join(zkern, "ALTLAST.md"), "# Altlast\n")
        schreib(zoverlay, lies(zoverlay) + "\nPROJEKTZEILE-T362b\n")
        p = _362_lauf(qkern, "--target", erst, "--update")
        fehlt = []
        if lies(os.path.join(zkern, "VERSION")).strip() != \
                lies(os.path.join(qkern, "VERSION")).strip():
            fehlt.append("VERSION nicht gehoben")
        if os.path.exists(os.path.join(zkern, "ALTLAST.md")):
            fehlt.append("Altlast liegt noch")
        if "PROJEKTZEILE-T362b" not in lies(zoverlay):
            fehlt.append("Overlay veraendert")
        for rest in ("core.koolie-neu", "core.koolie-alt"):
            if os.path.exists(os.path.join(erst, ".koolie", rest)):
                fehlt.append(rest + " liegt")
        melde("SONDE", "T362b", p.returncode == 0 and not fehlt,
              "--update ersetzt den Kern als Verzeichnis und laesst das Overlay stehen")
        if p.returncode != 0 or fehlt:
            notiz("        Exit %d; %s" % (p.returncode, "; ".join(fehlt) or "-"))

        # --- T362c: Rueckbau nach gescheiterter Installation ---------------------------
        kol = os.path.join(basis, "kollision")
        os.makedirs(kol)
        schreib(os.path.join(kol, "CLAUDE.md"), "# Projektdatei\n")
        p = _362_lauf(qkern, "--target", kol, "--client", "claude-code")
        ok = (p.returncode != 0 and not os.path.exists(os.path.join(kol, ".koolie", "core"))
              and lies(os.path.join(kol, "CLAUDE.md")) == "# Projektdatei\n")
        melde("SONDE", "T362c", ok,
              "Scheitert die Installation im Projekt, wird der kopierte Kern wieder entfernt")
        if not ok:
            notiz("        Exit %d, Kern %s" % (p.returncode, "liegt" if os.path.exists(
                os.path.join(kol, ".koolie", "core")) else "entfernt"))

        # --- T362d: --update ohne Kern ------------------------------------------------
        leer = os.path.join(basis, "leer")
        os.makedirs(leer)
        p = _362_lauf(qkern, "--target", leer, "--update")
        ok = p.returncode == 1 and not os.listdir(leer)
        melde("SONDE", "T362d", ok, "--update ohne vorhandenen Kern haelt an, ohne zu schreiben")

        # --- T362e: Quelle gleich Ziel ------------------------------------------------
        p = _362_lauf(qkern, "--target", quelle)
        ok = p.returncode == 1 and "Quelle und Ziel sind dasselbe" in p.stderr
        melde("SONDE", "T362e", ok, "Quelle und Ziel duerfen nicht dasselbe Verzeichnis sein")

        # --- T362f: aus einem Klon nur Verfolgtes --------------------------------------
        klon = kopie()
        try:
            g = unterprozess(["git", "-C", klon, "init", "-q"])
            if g.returncode == 0:
                g = unterprozess(["git", "-C", klon, "add", "-A"])
            if g.returncode != 0:
                raise Praeparationsfehler("git init/add im Klon: " + (g.stderr or "")[:200])
            schreib(os.path.join(klon, ".koolie", "core", "UNVERFOLGT-T362f.md"), "# x\n")
            ziel = os.path.join(basis, "ausklon")
            os.makedirs(ziel)
            p = _362_lauf(os.path.join(klon, ".koolie", "core"), "--target", ziel,
                          "--client", "claude-code")
            unverfolgt = os.path.exists(os.path.join(ziel, ".koolie", "core",
                                                     "UNVERFOLGT-T362f.md"))
            ok = p.returncode == 0 and "Klon - nur Verfolgtes" in p.stdout and not unverfolgt
            melde("SONDE", "T362f", ok,
                  "Aus einem Klon kommt nur Verfolgtes - eine unverfolgte Datei bleibt draussen")
            if not ok:
                notiz("        Exit %d, Klonweg %s, unverfolgt kopiert %s"
                      % (p.returncode, "Klon - nur Verfolgtes" in p.stdout, unverfolgt))
        finally:
            aufraeumen(os.path.dirname(klon))

        # --- T362g/h: der Dialog --------------------------------------------------------
        dlg = os.path.join(basis, "dialog")
        os.makedirs(dlg)
        p = _362_lauf(qkern, eingabe=T362_ANTWORTEN % dlg, werkzeug="install_dialog.py")
        ok = p.returncode == 0 and os.path.isfile(os.path.join(dlg, ".koolie", "core",
                                                               "install.py"))
        melde("SONDE", "T362g", ok,
              "Der Dialog sammelt Projekt, Client und Muster ein und installiert")
        if not ok:
            notiz("        Exit %d: %s" % (p.returncode, " | ".join(
                (p.stdout + p.stderr).splitlines()[-4:])))
        abb = os.path.join(basis, "abbruch")
        os.makedirs(abb)
        p = _362_lauf(qkern, eingabe="q\n", werkzeug="install_dialog.py")
        ok = p.returncode == 1 and "Nichts installiert" in p.stdout and not os.listdir(abb)
        melde("SONDE", "T362h", ok, "Der Dialog bricht mit q ab und schreibt nichts")

        # --- T363: die Mindestversion an drei Stellen -----------------------------------
        m = re.search(r"^PYTHON_MINDEST = \((\d+), (\d+)\)",
                      lies(os.path.join(QUELLE, ".koolie", "core", "install.py")), re.M)
        if not m:
            raise Praeparationsfehler("PYTHON_MINDEST in install.py nicht gefunden")
        zahl = "sys.version_info >= (%s, %s)" % m.groups()
        text = "Python %s.%s oder neuer" % m.groups()
        abweichend = [s for s in ("install.cmd", "install.command")
                      if zahl not in lies(os.path.join(QUELLE, s))
                      or text not in lies(os.path.join(QUELLE, s))]
        melde("SONDE", "T363", not abweichend,
              "install.py und beide Starter nennen dieselbe Mindestversion")
        if abweichend:
            notiz("        abweichend: %s (erwartet '%s')" % (", ".join(abweichend), zahl))

        # --- T365: die Bauform der Starter ------------------------------------------------
        fehlt = []
        for zeile in lies(os.path.join(QUELLE, "install.cmd")).splitlines():
            z = zeile.strip().lower()
            if z.startswith(":") or re.search(r"\bgoto\b|\bcall\s+:", z):
                if not z.startswith("rem"):
                    fehlt.append("install.cmd: " + zeile.strip()[:40])
        g = unterprozess(["git", "-C", QUELLE, "ls-files", "-s", "install.command"])
        if g.returncode != 0 or not g.stdout.strip():
            fehlt.append("Modus von install.command nicht lesbar (kein Git-Bestand)")
        elif not g.stdout.startswith("100755"):
            fehlt.append("install.command traegt " + g.stdout.split()[0])
        melde("SONDE", "T365", not fehlt,
              "install.cmd kommt ohne Sprungmarke aus, install.command ist ausfuehrbar")
        if fehlt:
            notiz("        " + "; ".join(fehlt))
    finally:
        aufraeumen(os.path.dirname(quelle))
        aufraeumen(basis)


buendel(sonden_kopierweg,
        "install.py --target aus Archivform und Klon, Heben, Rueckbau und Verweigerungen, "
        "dazu der Dialog und die Bauform der Starter")



# --- D-367: der Lieferumfang einer Installation (CR-2026-141) ------------------------
#
# `install.py --target --lieferumfang nutzung` laesst die Nachweisschicht weg
# (clientmap.NACHWEIS_ABLAGEN). OB die Nutzung ohne sie auskommt, belegt keine
# Einzelpruefung, sondern der Vergleich: Eine reduzierte Installation muss je Pack
# dieselbe Validatorausgabe liefern wie eine volle - bis auf die HINWEIS-Zeilen, die
# genau das Weggelassene nennen. Ein Traeger, den ein Werkzeug zur Laufzeit aus der
# Nachweisschicht liest, faellt genau hier auf.
#   L367  (Sonde) - je Pack: reduziert und voll zeilengleich unter --strict-overlay, bis
#                   auf die HINWEIS-Zeilen; reduziert ohne Nachweisschicht, mit
#                   LIEFERUMFANG 'nutzung', voll mit 'voll' und ohne HINWEIS
#   L367a (Sonde) - --update ohne Angabe hebt und bleibt reduziert
#   90b   (Sonde) - LIEFERUMFANG mit unbekanntem Wert wird gemeldet
#   90c   (Sonde) - 'nutzung', obwohl eine Ablage der Nachweisschicht daliegt, wird
#                   gemeldet
#   L367c (Sonde) - eine reduzierte Quelle verweigert den vollen Kern, ohne zu schreiben
#   L367b (Sonde) - --update --lieferumfang voll waechst auf den ganzen Kern
#   L367d (Sonde) - --lieferumfang ohne --target haelt an
#   L367e (Sonde) - der Dialog fragt den Umfang und installiert reduziert
#   T368  (Sonde) - unter Windows: ein Projektpfad, der die Pfadgrenze reisst, haelt vor
#                   der ersten Kopie an und laesst das Projekt leer (D-368); auf den
#                   anderen Systemen die Gegenprobe: derselbe Pfad wird installiert
# Dazu zwei Einzelsonden am Quellrepositorium (90, 90a).
L367_PACKS = ("claude-code", "devin-desktop", "openai-codex")
L367_ANTWORTEN = "%s\n1\n1\n2\nj\n"


def _367_ausgabe(root: str) -> list:
    """Validatorausgabe unter --strict-overlay, der Projektpfad durch <ROOT> ersetzt."""
    p = unterprozess([sys.executable, os.path.join(root, *VALIDATOR.split("/")),
                      "--root", root, "--strict-overlay"])
    text = ((p.stdout or "") + (p.stderr or "")).replace(os.path.normpath(root), "<ROOT>")
    return text.splitlines()


def _367_umfang(root: str) -> str:
    pfad = os.path.join(root, ".koolie", "core", "LIEFERUMFANG")
    return lies(pfad).strip() if os.path.isfile(pfad) else "-"


def _367_nachweis_da(root: str) -> list:
    kern = os.path.join(root, ".koolie", "core")
    return [a for a in ("governance/change-requests", "tests/protocols", "tests/erhebungen",
                        "build") if os.path.exists(os.path.join(kern, *a.split("/")))]


def sonden_lieferumfang() -> None:
    """Wirkungsnachweis fuer den waehlbaren Lieferumfang (D-367) und die Pfadgrenze (D-368)."""
    basis = tempfile.mkdtemp(prefix="lw-umfang-")
    quelle = kopie()
    try:
        qkern = os.path.join(quelle, ".koolie", "core")

        # --- L367: reduziert gegen voll, je Pack -------------------------------------
        abweichend = []
        for pack in L367_PACKS:
            voll = os.path.join(basis, "voll-" + pack)
            nutz = os.path.join(basis, "nutzung-" + pack)
            os.makedirs(voll)
            os.makedirs(nutz)
            a = _362_lauf(qkern, "--target", voll, "--client", pack)
            b = _362_lauf(qkern, "--target", nutz, "--client", pack,
                          "--lieferumfang", "nutzung")
            if a.returncode or b.returncode:
                abweichend.append("%s: Installation Exit %d/%d" % (pack, a.returncode,
                                                                  b.returncode))
                continue
            aus_voll = _367_ausgabe(voll)
            aus_nutz = _367_ausgabe(nutz)
            ohne = [z for z in aus_nutz if not z.startswith("HINWEIS")]
            hinweise = [z for z in aus_nutz if z.startswith("HINWEIS")]
            if ohne != aus_voll:
                nur_nutz = [z for z in ohne if z not in aus_voll]
                nur_voll = [z for z in aus_voll if z not in ohne]
                abweichend.append("%s: %d Zeilen nur reduziert, %d nur voll; erste: %s"
                                  % (pack, len(nur_nutz), len(nur_voll),
                                     ((nur_nutz or nur_voll or ["Reihenfolge"])[0])[:160]))
            if any(z.startswith("HINWEIS") for z in aus_voll):
                abweichend.append(pack + ": die volle Installation traegt HINWEIS-Zeilen")
            if not any("Lieferumfang 'nutzung'" in z for z in hinweise):
                abweichend.append(pack + ": reduziert ohne HINWEIS zum Lieferumfang")
            if _367_nachweis_da(nutz):
                abweichend.append(pack + ": reduziert liegt " + ", ".join(_367_nachweis_da(nutz)))
            if (_367_umfang(voll), _367_umfang(nutz)) != ("voll", "nutzung"):
                abweichend.append("%s: LIEFERUMFANG %s/%s" % (pack, _367_umfang(voll),
                                                              _367_umfang(nutz)))
        melde("SONDE", "L367", not abweichend,
              "Eine reduzierte Installation meldet in jedem Pack dasselbe wie eine volle, "
              "bis auf die HINWEIS-Zeilen zum Weggelassenen")
        for z in abweichend:
            notiz("        " + z)

        nutz = os.path.join(basis, "nutzung-claude-code")
        nkern = os.path.join(nutz, ".koolie", "core")

        # --- L367a: Heben ohne Angabe bleibt reduziert -------------------------------
        schreib(os.path.join(nkern, "VERSION"), "0.0.0\n")
        p = _362_lauf(qkern, "--target", nutz, "--update")
        ok = (p.returncode == 0 and _367_umfang(nutz) == "nutzung"
              and not _367_nachweis_da(nutz)
              and lies(os.path.join(nkern, "VERSION")).strip()
              == lies(os.path.join(qkern, "VERSION")).strip())
        melde("SONDE", "L367a", ok,
              "--update ohne Angabe hebt ein reduziertes Projekt und laesst es reduziert")
        if not ok:
            notiz("        Exit %d, Umfang %s, Nachweis %s" % (
                p.returncode, _367_umfang(nutz), _367_nachweis_da(nutz)))

        # --- 90b, 90c: Pruefung 90 an der reduzierten Installation --------------------
        schreib(os.path.join(nkern, "LIEFERUMFANG"), "teilweise\n")
        melde("SONDE", "90b", "trägt 'teilweise'" in "\n".join(_367_ausgabe(nutz)),
              "Ein unbekannter Wert in LIEFERUMFANG wird gemeldet - das naechste Heben "
              "hielte daran an")
        schreib(os.path.join(nkern, "LIEFERUMFANG"), "nutzung\n")
        os.makedirs(os.path.join(nkern, "tests", "protocols"))
        schreib(os.path.join(nkern, "tests", "protocols", "liegengeblieben.md"), "# x\n")
        melde("SONDE", "90c", "sagt 'nutzung', aber" in "\n".join(_367_ausgabe(nutz)),
              "LIEFERUMFANG nutzung neben einer Ablage der Nachweisschicht wird gemeldet - "
              "das naechste Heben loeschte sie")

        # --- L367c: aus der reduzierten Quelle kein voller Kern ------------------------
        leer = os.path.join(basis, "aus-reduziert")
        os.makedirs(leer)
        p = _362_lauf(nkern, "--target", leer, "--client", "claude-code")
        ok = p.returncode == 1 and "einen vollen Kern kann" in p.stderr and not os.listdir(leer)
        melde("SONDE", "L367c", ok,
              "Eine reduzierte Quelle verweigert den vollen Kern und schreibt nichts")

        # --- L367b: ausdruecklich zurueck auf voll --------------------------------------
        shutil.rmtree(os.path.join(nkern, "tests", "protocols"))
        p = _362_lauf(qkern, "--target", nutz, "--update", "--lieferumfang", "voll")
        ok = (p.returncode == 0 and _367_umfang(nutz) == "voll"
              and len(_367_nachweis_da(nutz)) == 4 and "(bisher nutzung)" in p.stdout)
        melde("SONDE", "L367b", ok,
              "--update --lieferumfang voll bringt die Nachweisschicht zurueck und nennt "
              "den Wechsel")
        if not ok:
            notiz("        Exit %d, Umfang %s, Nachweis %s" % (
                p.returncode, _367_umfang(nutz), _367_nachweis_da(nutz)))

        # --- L367d: ohne --target ------------------------------------------------------
        ohne_ziel = os.path.join(basis, "ohne-target")
        os.makedirs(ohne_ziel)
        p = _362_lauf(qkern, "--root", ohne_ziel, "--lieferumfang", "nutzung")
        ok = (p.returncode == 1 and "gehoert zu --target" in p.stderr
              and not os.listdir(ohne_ziel))
        melde("SONDE", "L367d", ok, "--lieferumfang ohne --target haelt an, ohne zu schreiben")

        # --- L367e: der Dialog ---------------------------------------------------------
        dlg = os.path.join(basis, "dialog")
        os.makedirs(dlg)
        p = _362_lauf(qkern, eingabe=L367_ANTWORTEN % dlg, werkzeug="install_dialog.py")
        ok = p.returncode == 0 and _367_umfang(dlg) == "nutzung" and not _367_nachweis_da(dlg)
        melde("SONDE", "L367e", ok,
              "Der Dialog fragt den Lieferumfang ab und installiert reduziert")
        if not ok:
            notiz("        Exit %d, Umfang %s: %s" % (p.returncode, _367_umfang(dlg), " | ".join(
                (p.stdout + p.stderr).splitlines()[-4:])))

        # --- T368: die Pfadgrenze ------------------------------------------------------
        tief = basis
        while len(tief) < 190:
            tief = os.path.join(tief, "t" * min(40, 200 - len(tief)))
        os.makedirs(tief)
        p = _362_lauf(qkern, "--target", tief, "--client", "claude-code")
        if os.name == "nt":
            ok = (p.returncode == 1 and "fuer Windows zu lang" in p.stderr
                  and not os.listdir(tief))
            melde("SONDE", "T368", ok,
                  "Ein Projektpfad, der die Windows-Pfadgrenze reisst, haelt vor der ersten "
                  "Kopie an und laesst das Projekt leer")
        else:
            ok = p.returncode == 0
            melde("GEGENPROBE", "T368", ok,
                  "Ausserhalb von Windows gilt keine Pfadgrenze - derselbe tiefe "
                  "Projektpfad wird installiert")
        if not ok:
            notiz("        Exit %d: %s" % (p.returncode, (p.stderr or "")[:200]))
    finally:
        aufraeumen(os.path.dirname(quelle))
        aufraeumen(basis)


buendel(sonden_lieferumfang,
        "Reduzierte gegen volle Installation je Pack, Heben mit und ohne Wechsel, "
        "Verweigerungen, der Dialog, Pruefung 90 und die Windows-Pfadgrenze")


# Pruefung 90 am Quellrepositorium: Es ist keine Installation, und die Lockerung von
# Pruefung 12 gilt dort nie - was immer eine Datei LIEFERUMFANG behauptet.
P90_DATEI = os.path.join(".koolie", "core", "LIEFERUMFANG")
P90_PROTOKOLL = os.path.join(".koolie", "core", "tests", "protocols",
                             "2026-09-19-testblaetter-buendel-2.md")


def _90a(root: str) -> None:
    schreib(P(root, P90_DATEI), "nutzung\n")
    if not os.path.isfile(P(root, P90_PROTOKOLL)):
        raise Praeparationsfehler("Das zitierte Protokoll fehlt schon: " + P90_PROTOKOLL)
    os.remove(P(root, P90_PROTOKOLL))


sonde("90", "Eine Datei LIEFERUMFANG im Quellrepositorium wird gemeldet - sie behauptete dort eine Installation",
      lambda r: schreib(P(r, P90_DATEI), "nutzung\n"), "liegt im Quellrepositorium")

sonde("90a", "Im Quellrepositorium bleibt ein Verweis in die Nachweisschicht ein Fehler, auch wenn LIEFERUMFANG nutzung behauptet",
      _90a, "Pfadangabe existiert nicht: .koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-2.md")


# --- D-364: Pruefung 33 ohne PyYAML (CR-2026-140) --------------------------------------
#
# Ohne PyYAML las Pruefung 33 aus dem Rohtext des Frontmatters nichts und meldete an
# jeder claude-code-Installation neun Skills mit leerem disallowed-tools. Der Starter
# installiert kein PyYAML nach (D-362) - auf einem frischen Zielrechner fehlt es also
# oft. Die Sonde sperrt den Import ueber ein Stellvertretermodul im Suchpfad.
#   S364  (Sonde)      - eine verkuerzte Liste wird auch ohne PyYAML gemeldet
#   S364a (Gegenprobe) - die richtige Installation bleibt ohne PyYAML still
T364_SPERRE = "raise ImportError('PyYAML gesperrt durch die Sonde S364')\n"


def sonden_ohne_pyyaml() -> None:
    """Pruefung 33 misst ohne PyYAML dasselbe wie mit (D-364)."""
    root = installation("claude-code")
    sperre = tempfile.mkdtemp(prefix="lw-ohne-yaml-")
    try:
        schreib(os.path.join(sperre, "yaml.py"), T364_SPERRE)
        umgebung = dict(os.environ, PYTHONPATH=sperre)

        def lauf_ohne() -> str:
            p = unterprozess([sys.executable, os.path.join(root, *VALIDATOR.split("/")),
                              "--root", root], env=umgebung)
            return (p.stdout or "") + (p.stderr or "")

        aus = lauf_ohne()
        gesperrt = "PyYAML nicht installiert" in aus
        still = "disallowed-tools traegt" not in aus
        melde("GEGENPROBE", "S364a", gesperrt and still,
              "Ohne PyYAML meldet Pruefung 33 an einer richtigen Installation nichts")
        if not (gesperrt and still):
            notiz("        PyYAML gesperrt %s, still %s" % (gesperrt, still))
        skill = os.path.join(root, ".claude", "skills", "fw-plan", "SKILL.md")
        text = lies(skill)
        neu = re.sub(r"(?m)^disallowed-tools: .*$", "disallowed-tools: Edit", text)
        if neu == text:
            raise Praeparationsfehler("disallowed-tools in fw-plan/SKILL.md nicht gefunden")
        schreib(skill, neu)
        aus = lauf_ohne()
        ok = "fw-plan/SKILL.md: disallowed-tools traegt ['Edit']" in aus
        melde("SONDE", "S364", ok,
              "Ohne PyYAML wird eine verkuerzte disallowed-tools-Liste weiter gemeldet")
    finally:
        aufraeumen(sperre)
        aufraeumen(os.path.dirname(root))


buendel(sonden_ohne_pyyaml,
        "Pruefung 33 liest disallowed-tools auch ohne PyYAML und meldet nur, was fehlt")


# --- 6: die Starter sind Traeger der Inhaltspruefung (D-365) ----------------------------

sonde("6s", "Eine IP-Adresse in install.cmd wird gemeldet (D-365)",
      lambda root: schreib(os.path.join(root, "install.cmd"),
                           lies(os.path.join(root, "install.cmd"))
                           + "rem Server: 10.11.12.13\n"),
      "FW-CONTENT-IP")
sonde("6s", "Eine IP-Adresse in install.command wird gemeldet (D-365)",
      lambda root: schreib(os.path.join(root, "install.command"),
                           lies(os.path.join(root, "install.command"))
                           + "# Server: 10.11.12.13\n"),
      "FW-CONTENT-IP")


# --- 8: der registrierte Traeger existiert (CR-2026-139, D-360) --------------------
#
# Bis 1.5.0 pruefte Pruefung 8 Schluessel und Aufzaehlungswerte des Overlay-Manifests,
# nicht aber, ob unter `path` etwas liegt. Die Sonden schreiben das Manifest aus der
# VERSIONIERTEN Vorlage (templates/project-overlay/) und setzen darin einen
# Beispieleintrag auf einen echten Pfad. Das Overlay des Quellrepositoriums selbst steht
# in der .gitignore - die erste Fassung dieser Sonden las es und brach an einer
# frischen Auscheckung ab (gefunden beim Gegenbeweis, CR-2026-139). Die Gegenprobe ist
# die wichtigere: Ein Eintrag, der auf eine vorhandene Datei zeigt, bleibt still - und
# die Beispiele der Vorlage mit Ausfuellschlitz im Pfad ebenso, sonst waere jedes
# frische Overlay rot.
M8_PFAD = "existiert nicht. Ein registriertes Dokument"
M8_REGEL = "Mit load rule trägt die Regeldatei"
P8_MANIFEST = ".koolie/project-overlay/overlay-manifest.yaml".replace("/", os.sep)
P8_VORLAGE = ".koolie/core/templates/project-overlay/overlay-manifest.yaml".replace("/", os.sep)
P8_BEISPIEL_ARCH = 'path: ".koolie/project-overlay/documents/architecture/<TBD>.md"'
P8_BEISPIEL_CG = 'path: ".koolie/project-overlay/documents/coding-guidelines/<TBD: datei>.md"'
P8_REGEL_CG = 'rule_file: "<RULES_DIR>/21-overlay-coding-guidelines.md"'
P8_VORHANDEN = 'path: ".koolie/core/templates/project-overlay/documents/README.md"'


def _8_setze(root: str, *paare) -> None:
    """Das Manifest aus der Vorlage, mit den genannten Ersetzungen je genau einmal."""
    text = lies(P(root, P8_VORLAGE))
    for alt, neu in paare:
        if text.count(alt) != 1:
            raise Praeparationsfehler("Manifestvorlage fuehrt '%s' %dx statt 1x"
                                      % (alt, text.count(alt)))
        text = text.replace(alt, neu, 1)
    os.makedirs(os.path.dirname(P(root, P8_MANIFEST)), exist_ok=True)
    schreib(P(root, P8_MANIFEST), text)


sonde("8a", "Ein registriertes Dokument, dessen Pfad auf nichts zeigt, wird gemeldet - bis 1.5.0 bestand ein solches Register",
      lambda r: _8_setze(r, (P8_BEISPIEL_ARCH,
                             'path: ".koolie/project-overlay/documents/architecture/gibt-es-nicht.md"')),
      M8_PFAD)

sonde("8b", "Ein Dokument mit load rule, dessen Regeldatei fehlt, wird gemeldet - es wirkt sonst nicht",
      lambda r: _8_setze(r, (P8_BEISPIEL_CG, P8_VORHANDEN),
                         (P8_REGEL_CG, 'rule_file: ".koolie/project-overlay/gibt-es-nicht.md"')),
      M8_REGEL)

gegenprobe("8a", "Ein Eintrag, der auf eine vorhandene Datei zeigt, bleibt still - und die Beispiele mit Ausfuellschlitz im Pfad ebenso",
           lambda r: _8_setze(r, (P8_BEISPIEL_ARCH, P8_VORHANDEN)), M8_PFAD)


# --- 66: das verirrte Steuerzeichen (D-217) --------------------------------------
#
# Die Sonden setzen das Zeichen in den beiden Bauformen, in denen es gemessen wurde:
# am Ende eines Traegers und am Zeilenende einer Tabellenzeile - dort sassen dreizehn
# der vierzehn Fundstellen. Sie schreiben mit `schreib`, also ohne Umsetzung der
# Zeilenenden; eine Sonde, die ihren eigenen Gegenstand normalisiert, misst nichts.
#
# 🔴 DIE ZWEITE GEGENPROBE IST DIE WICHTIGERE. Sie stellt einen Traeger durchgehend
# auf LF - also auf die ANDERE Zeilenende-Form - und belegt damit, dass Pruefung 66
# das verirrte ZEICHEN misst und nicht die Form. Ohne sie waere aus der Meldung nicht
# zu erkennen, ob hier eine Zeichenpruefung steht oder eine Formatvorschrift, die
# niemand entschieden hat (K-81).
M66 = "verirrte(s) Steuerzeichen"
P66_TRAEGER = ".koolie/core/OWNERS.md".replace("/", os.sep)
P66_ANTRAG = (".koolie/core/governance/change-requests/"
              "CR-2026-027-zeichenlimit-einstufung.md").replace("/", os.sep)


def _66_am_ende(root: str) -> None:
    """Ein einzelnes CR am Ende eines Kerntraegers - die stillste Fundstelle."""
    pfad = P(root, P66_TRAEGER)
    schreib(pfad, lies(pfad) + chr(13))


def _66_in_der_tabelle(root: str) -> None:
    """Dieselbe Bauform wie vierzehn der sechzehn gemessenen Fundstellen.

    Ein CR unmittelbar vor dem Zeilenumbruch einer Tabellenzeile. Es rendert nicht,
    es faellt in keinem Diff auf - und es hat elf Antraege dieses Verzeichnisses
    von der Normalisierung ausgenommen.
    """
    pfad = P(root, P66_ANTRAG)
    text = lies(pfad)
    marke = "| Umsetzung |"
    if marke not in text:
        raise Praeparationsfehler(
            "CR-2026-027 fuehrt die Zeile '%s' nicht mehr - die Sonde zu 66 haette "
            "keinen Anker" % marke)
    schreib(pfad, text.replace(marke, chr(13) + marke, 1))


def _66_auf_lf(root: str) -> None:
    """Gegenprobe: ein Traeger durchgehend auf LF - die andere Form, kein Befund."""
    pfad = P(root, P66_TRAEGER)
    schreib(pfad, lies(pfad).replace(chr(13) + chr(10), chr(10)))


sonde("66a", "Ein einzelnes CR am Ende eines Kerntraegers - unsichtbar im Text und genug, damit git die Zeilenenden nicht mehr normalisiert",
      _66_am_ende, M66)

sonde("66b", "Dasselbe Zeichen am Zeilenende einer Tabellenzeile - die Bauform von vierzehn der sechzehn gemessenen Fundstellen",
      _66_in_der_tabelle, M66)

gegenprobe("66a", "Das unveraenderte Repositorium bleibt unbeanstandet - seit dieser Berichtigung traegt kein Traeger mehr ein verirrtes CR",
           None, M66)

gegenprobe("66b", "Ein Traeger durchgehend auf LF wird NICHT gemeldet: gemessen wird das verirrte Zeichen, nicht die Zeilenende-Form",
           _66_auf_lf, M66)


# --- 67: ENTFALLEN mit 1.4.1 (D-350) ----------------------------------------------
#
# Pruefung 67 hielt die Titelzeile der Uebergabe gegen VERSION. Seit 1.4.1 ist die
# Uebergabe nicht mehr versioniert, und mit der Pruefung entfallen ihre vier Sonden
# und zwei Gegenproben. Eine Sonde auf einen Traeger, den eine frische Auscheckung
# nicht fuehrt, belegte nur, was auf einem Arbeitsplatz liegt.


# --- 68: das Praefix, das mehr sperrt als sein Befehl (D-219) ----------------------
#
# Die dritte Sonde ist die Ankersonde: Ohne exec-Regel haette Pruefung 68 nichts zu
# rechnen und bestuende leise. Die zweite Gegenprobe belegt den ZUSCHNITT - eine
# Regel, deren Praefix ihrem Befehl gleicht, erfasst nicht ueber und wird nicht
# gemeldet, auch ohne Begruendungsfeld. Ohne dieses Paar waere nicht zu unterscheiden,
# ob die Pruefung die Uebererfassung sucht oder jede Regel ohne Feld.
M68 = "mehr, als ihr Befehl nennt"
M68_ANKER = "keine einzige exec-Regel gefunden"
P68_PERM = ".koolie/core/framework/runtime/permissions.json".replace("/", os.sep)


def _68_laden(root: str) -> dict:
    return json.loads(lies(P(root, P68_PERM)))


def _68_schreiben(root: str, daten: dict) -> None:
    schreib(P(root, P68_PERM), json.dumps(daten, indent=2, ensure_ascii=False))


def _68_feld_entfernen(root: str) -> None:
    """Der gemessene Fall: die Begruendung an der git-branch-Regel faellt weg."""
    daten = _68_laden(root)
    getroffen = 0
    for regel in daten.get("deny", []):
        if regel.get("tool") == "exec" and "_uebererfasst" in regel:
            del regel["_uebererfasst"]
            getroffen += 1
    if getroffen == 0:
        raise Praeparationsfehler(
            "keine exec-Regel mit Begruendungsfeld - die Sonde zu 68 haette keinen "
            "Anker; entweder erfasst keine Regel mehr ueber, dann gehoert die Sonde "
            "weg, oder das Feld heisst anders")
    _68_schreiben(root, daten)


def _68_neue_regel(root: str) -> None:
    """Eine ZWEITE Stelle: eine neue Regel mit kuerzerem Praefix und ohne Feld.

    Sie belegt, dass die Pruefung an der Bauform haengt und nicht an einer Zeile.
    """
    daten = _68_laden(root)
    daten.setdefault("deny", []).append(
        {"tool": "exec", "command": "sondenbefehl --loeschen",
         "prefix": "sondenbefehl"})
    _68_schreiben(root, daten)


def _68_ohne_exec(root: str) -> None:
    """Ankersonde: keine exec-Regel mehr - der verlorene Gegenstand."""
    daten = _68_laden(root)
    for korb in ("deny", "ask", "allow"):
        daten[korb] = [r for r in daten.get(korb, []) if r.get("tool") != "exec"]
    _68_schreiben(root, daten)


def _68_praefix_gleich_befehl(root: str) -> None:
    """Gegenprobe: eine Regel OHNE Uebererfassung und ohne Feld - kein Befund.

    🔴 WER EINEN ERLAUBTEN FALL HERSTELLT, MUSS IHN VOLLSTAENDIG HERSTELLEN
    (0.66.0). Eine neue Regel in der Kernquelle macht die lokale Testinstallation
    unvollstaendig, und der Abgleich der Berechtigungsdatei meldet die fehlende
    Regel - einen Fehler, den diese Gegenprobe nicht gemeint hat. Der gerenderte
    Eintrag gehoert deshalb mit.
    """
    daten = _68_laden(root)
    daten.setdefault("deny", []).append(
        {"tool": "exec", "command": "sondenbefehl"})
    _68_schreiben(root, daten)
    inst = P(root, ".devin", "config.json")
    if os.path.isfile(inst):
        konf = json.loads(lies(inst))
        konf["permissions"]["deny"].append("Exec(sondenbefehl)")
        schreib(inst, json.dumps(konf, indent=2, ensure_ascii=False))


sonde("68a", "Eine exec-Regel sperrt ueber ihr Praefix mehr, als ihr Befehl nennt, und sagt es nicht - der Eintrag, der 25 Abweisungen erzeugt hat",
      _68_feld_entfernen, M68)

sonde("68b", "Dieselbe Bauform an einer ZWEITEN Stelle: eine neu eingefuegte Regel mit kuerzerem Praefix wird ebenso gemeldet",
      _68_neue_regel, M68)

sonde("68c", "Ohne exec-Regel meldet Pruefung 68 den verlorenen Gegenstand, statt leise zu bestehen",
      _68_ohne_exec, M68_ANKER)

gegenprobe("68a", "Das unveraenderte Repositorium bleibt unbeanstandet - alle vier uebererfassenden Regeln tragen ihre Begruendung",
           None, M68)


# --- 69: der Messapparat schreibt nicht in das Repositorium (D-222) ----------------
#
# Zwei Formen desselben Gegenstands: die Belegdatei (69a) und das Verzeichnis, das
# `lauf.py` selbst anlegen wuerde (69b). Die dritte ist die Ankersonde - eine leere
# Erhebungsablage haette nichts zu zaehlen und bestuende leise. Die Gegenprobe
# belegt den ZUSCHNITT: Eine weitere .py-Datei ist ein WERKZEUG und wird NICHT
# gemeldet; ohne sie waere nicht zu unterscheiden, ob die Pruefung die Art der
# Datei prueft oder jede Neuerung.
M69 = "Erhebungsablage des Kerns"
M69_ANKER = "kein einziges Werkzeug gefunden"
P69_ORDNER = ".koolie/core/tests/erhebungen".replace("/", os.sep)


def _69_beleg(root: str) -> None:
    """Der gemessene Fall: ein Ergebnis-JSON eines Laufs landet im Repositorium."""
    schreib(P(root, P69_ORDNER, "sk010n02-ergebnis.json"), '{"is_error": false}')


def _69_verzeichnis(root: str) -> None:
    """Die zweite Form: das Belegverzeichnis, das lauf.py selbst anlegen wuerde."""
    os.makedirs(P(root, P69_ORDNER, "belege"), exist_ok=True)
    schreib(P(root, P69_ORDNER, "belege", "sk010n02-antwort.md"), "Antwort")


def _69_leer(root: str) -> None:
    """Ankersonde: keine Werkzeuge mehr - der verlorene Gegenstand."""
    ordner = P(root, P69_ORDNER)
    if not os.path.isdir(ordner):
        raise Praeparationsfehler(
            "die Erhebungsablage fehlt - die Sonde zu 69 haette keinen Anker")
    for name in os.listdir(ordner):
        ziel = os.path.join(ordner, name)
        if os.path.isfile(ziel):
            os.remove(ziel)
        else:
            shutil.rmtree(ziel)


def _69_weiteres_werkzeug(root: str) -> None:
    """Gegenprobe: ein weiteres Skript ist ein Werkzeug und kein Befund."""
    schreib(P(root, P69_ORDNER, "sondenwerkzeug.py"), "# nichts" + chr(10))


sonde("69a", "Ein Ergebnis-JSON in der Erhebungsablage des Kerns wird gemeldet - der Fall, den die fuenf relativen Pfade nach dem Umzug erzeugt haetten",
      _69_beleg, M69)

sonde("69b", "Dieselbe Bauform als VERZEICHNIS: das Belegverzeichnis, das lauf.py selbst anlegen wuerde, wird ebenso gemeldet",
      _69_verzeichnis, M69)

sonde("69c", "Ohne ein einziges Werkzeug meldet Pruefung 69 den verlorenen Gegenstand, statt leise zu bestehen",
      _69_leer, M69_ANKER)

gegenprobe("69a", "Ein weiteres .py-Skript ist ein Werkzeug und wird NICHT gemeldet - die Pruefung haengt an der Art der Datei, nicht an ihrer Neuheit",
           _69_weiteres_werkzeug, M69)

gegenprobe("68b", "Eine Regel, deren Praefix ihrem Befehl gleicht, wird NICHT gemeldet - auch ohne Begruendungsfeld; gemessen wird die Uebererfassung, nicht das fehlende Feld",
           _68_praefix_gleich_befehl, M68)


# --- 70: jedes Werkzeug des Kerns nennt nur Namen, die es gibt (D-229) -------------
#
# Drei Formen desselben Gegenstands: der gemessene NameError (70a), die Quelle, die
# der Interpreter gar nicht erst uebersetzt (70b), und die Ankersonde - ein
# Messapparat ohne ein einziges Werkzeug haette nichts zu pruefen und bestuende leise
# (70c). 70a setzt den Defekt WOERTLICH so, wie er am 2026-09-21 gefunden wurde: den
# Ablageort NEBEN dem Skript, den D-222 mit dem Umzug entfernt hat.
#
# ZWEI GEGENPROBEN, UND SIE BELEGEN DEN ZUSCHNITT. Die Pruefung haengt an der
# BINDUNG, nicht an der Schreibweise: Ein Werkzeug, das freie Variablen einer
# umschliessenden Funktion liest, eine Komprehension fuehrt, `__file__` nennt und
# einen Namen erst im `except`-Zweig bindet, ist gebunden und wird nicht gemeldet
# (70a). Und ein Name, der GEBUNDEN und falsch belegt ist, laeuft durch - das ist die
# angesagte Grenze, nicht ein Loch (70b).
M70 = "NameError, der auf seinen Lauf wartet"
M70_SYNTAX = "laedt nicht"
M70_ANKER = "kein einziges Werkzeug geprueft"
P70_STAND = ".koolie/core/tests/erhebungen/stand-b4.py".replace("/", os.sep)
P70_APPARAT = ".koolie/core/tests/erhebungen".replace("/", os.sep)


def _70_verschwundener_name(root: str) -> None:
    """Der gemessene Fall: der Ablageort neben dem Skript, nach dem Umzug (D-222)."""
    ersetze(P(root, P70_STAND),
            ("PROMPTS = ablage.prompts(anlegen=False)",
             'PROMPTS = os.path.join(os.path.dirname(S), "prompts")'))


def _70_uebersetzt_nicht(root: str) -> None:
    """Die zweite Form: ein Werkzeug, das der Interpreter nicht uebersetzt."""
    schreib(P(root, P70_APPARAT, "sondenwerkzeug.py"),
            "# -*- coding: utf-8 -*-" + chr(10) + "def offen(:" + chr(10))


def _70_apparat_ohne_werkzeug(root: str) -> None:
    """Ankersonde: die Ablage steht, kein Werkzeug mehr darin."""
    ordner = P(root, P70_APPARAT)
    if not os.path.isdir(ordner):
        raise Praeparationsfehler(
            "die Erhebungsablage fehlt - die Sonde zu 70 haette keinen Anker")
    geloescht = 0
    for name in os.listdir(ordner):
        ziel = os.path.join(ordner, name)
        if os.path.isfile(ziel) and name.endswith(".py"):
            os.remove(ziel)
            geloescht += 1
    if geloescht == 0:
        raise Praeparationsfehler(
            "in der Erhebungsablage lag kein einziges .py - der Anker traegt nicht")


def _70_gebundene_namen(root: str) -> None:
    """Gegenprobe: jede Bindungsform, die es gibt - und keine davon ist ein Befund."""
    schreib(P(root, P70_APPARAT, "sondenwerkzeug.py"), chr(10).join([
        "# -*- coding: utf-8 -*-",
        "import os",
        "",
        "WURZEL = os.path.dirname(os.path.abspath(__file__))",
        "",
        "",
        "def aussen(grenze):",
        "    rest = [x for x in os.listdir(WURZEL) if x > grenze]",
        "",
        "    def innen():",
        "        return grenze, rest",
        "",
        "    try:",
        "        zahl = int(grenze)",
        "    except ValueError as fehler:",
        "        zahl = len(str(fehler))",
        "    with open(os.path.join(WURZEL, grenze)) as quelle:",
        "        inhalt = quelle.read()",
        "    return innen(), zahl, inhalt",
        "",
        "",
        "class Traeger(object):",
        "    feld = WURZEL",
        "",
        "    def hol(self):",
        "        return self.feld",
        "",
    ]))


def _70_gebunden_und_falsch(root: str) -> None:
    """Gegenprobe: der Name IST gebunden - der Wert taugt nicht. Die angesagte Grenze."""
    schreib(P(root, P70_APPARAT, "sondenwerkzeug.py"), chr(10).join([
        "# -*- coding: utf-8 -*-",
        "import os",
        "",
        "S = None",
        "PROMPTS = os.path.join(os.path.dirname(S), 'prompts')",
        "",
    ]))


sonde("70a", "Der gemessene Fall: der Ablageort neben dem Skript ist mit D-222 verschwunden, seine zwei Lesestellen nicht - stand-b4.py war seit 0.79.0 tot",
      _70_verschwundener_name, M70)

sonde("70b", "Dieselbe Bauform eine Stufe frueher: ein Werkzeug des Kerns, das der Interpreter nicht einmal uebersetzt, wird gemeldet",
      _70_uebersetzt_nicht, M70_SYNTAX)

sonde("70c", "Ohne ein einziges Werkzeug im Messapparat meldet Pruefung 70 den verlorenen Gegenstand, statt leise zu bestehen",
      _70_apparat_ohne_werkzeug, M70_ANKER)

gegenprobe("70a", "Freie Variable, Komprehension, except-Name, with-Ziel, Klassenfeld und __file__ sind gebunden und werden NICHT gemeldet - die Pruefung haengt an der Bindung",
           _70_gebundene_namen, M70)

gegenprobe("70b", "Ein gebundener Name mit untauglichem Wert laeuft durch - das ist die angesagte Grenze der Pruefung und kein Loch",
           _70_gebunden_und_falsch, M70)


# --- 71: kein Traeger des Kerns nennt einen Arbeitsplatz (D-231) -------------------
#
# Drei Formen desselben Gegenstands: der gemessene Fall in einem WERKZEUG (71a), die
# gleiche Bauform in einer CHECKLISTE - also ausserhalb der .py-Welt, weil die
# Pruefung nicht an der Dateiart haengt (71b) -, und die Ankersonde: ein Muster, das
# seinen Gegenstand nicht mehr trifft, bestuende leise (71c).
#
# DREI GEGENPROBEN, UND SIE BELEGEN DEN ZUSCHNITT. Ein Platzhalter nennt niemanden
# (71a). Die Marke `SYNTHETISCH` in derselben Zeile laeuft durch - dieselbe Bauform
# wie das Begruendungsfeld von Pruefung 68 (71b). Und eine AUFZEICHNUNG bleibt
# unbeanstandet: Ein Protokoll haelt fest, WO gemessen wurde, und wer es umschreibt,
# hat keines mehr (71c, D-141) - das ist die angesagte Grenze und der Grund, aus dem
# `K-85` offen steht.
M71 = "nennt ein Benutzerprofil"
M71_ANKER = "das eigene Muster trifft"
P71_WERKZEUG = ".koolie/core/tests/erhebungen/stand-b4.py".replace("/", os.sep)
P71_CHECKLISTE = ".koolie/core/checklists/11-framework-release.md".replace("/", os.sep)
P71_PROTOKOLL = (".koolie/core/tests/protocols/"
                 "2026-09-21-wiederaufnahme-nachlauf-b4.md").replace("/", os.sep)
P71_VALIDATOR = ".koolie/core/tests/scripts/validate-framework.py".replace("/", os.sep)
P71_PFAD = "C:" + chr(92) + "Users" + chr(92) + "sondenkonto" + chr(92) + "devpacks"


def _71_werkzeug(root: str) -> None:
    """Der gemessene Fall: ein Werkzeug des Kerns fuehrt einen Arbeitsplatzpfad."""
    ersetze(P(root, P71_WERKZEUG),
            ('BAEUME = r"C:' + chr(92) + 'lw-b4"',
             'BAEUME = r"' + P71_PFAD + chr(92) + 'lw-b4"'))


def _71_checkliste(root: str) -> None:
    """Die zweite Form, ausserhalb der .py-Welt: derselbe Pfad in einer Checkliste."""
    zeile_nach(P(root, P71_CHECKLISTE), "## Zweck",
               "" + chr(10) + "Arbeitsstand liegt unter `" + P71_PFAD + "`.")


def _71_muster_verlieren(root: str) -> None:
    """Ankersonde: das Muster trifft seinen eigenen Gegenstand nicht mehr."""
    ersetze(P(root, P71_VALIDATOR),
            ('r"(?:[A-Za-z]:[' + chr(92) + chr(92) + '/]{1,2}Users|/home|/Users)'
             '[' + chr(92) + chr(92) + '/]{1,2}([A-Za-z0-9._-]+)"',
             'r"trifft-nichts-mehr([A-Za-z0-9._-]+)"'))


def _71_platzhalter(root: str) -> None:
    """Gegenprobe: ein Platzhalter nennt niemanden."""
    zeile_nach(P(root, P71_CHECKLISTE), "## Zweck",
               "" + chr(10) + "Arbeitsstand liegt unter `C:" + chr(92)
               + "Users" + chr(92) + "%USERNAME%" + chr(92) + "devpacks`.")


def _71_marke(root: str) -> None:
    """Gegenprobe: die Marke in derselben Zeile laeuft durch (wie bei Pruefung 68)."""
    zeile_nach(P(root, P71_CHECKLISTE), "## Zweck",
               "" + chr(10) + "Beispielpfad `" + P71_PFAD + "` - SYNTHETISCH.")


def _71_aufzeichnung(root: str) -> None:
    """Gegenprobe: eine Aufzeichnung bleibt unbeanstandet - die angesagte Grenze."""
    zeile_nach(P(root, P71_PROTOKOLL), "## 1. Die Lage vor dem Durchgang",
               "" + chr(10) + "Gemessen wurde ausserhalb von `" + P71_PFAD + "`.")


sonde("71a", "Ein Werkzeug des Kerns fuehrt einen Arbeitsplatzpfad im Quelltext - der gemessene Fall, den D-222 mit dem Apparat hereingetragen hat",
      _71_werkzeug, M71)

sonde("71b", "Dieselbe Bauform ausserhalb der Skripte: derselbe Pfad in einer Checkliste wird ebenso gemeldet",
      _71_checkliste, M71)

sonde("71c", "Trifft das eigene Muster seinen Gegenstand nicht mehr, meldet Pruefung 71 das, statt leise zu bestehen",
      _71_muster_verlieren, M71_ANKER)

gegenprobe("71a", "Ein Platzhalter als Kontosegment nennt niemanden und wird NICHT gemeldet - die Pruefung haengt am Namen, nicht an der Pfadform",
           _71_platzhalter, M71)

gegenprobe("71b", "Die Marke SYNTHETISCH in derselben Zeile laeuft durch - dieselbe Bauform wie das Begruendungsfeld von Pruefung 68",
           _71_marke, M71)

gegenprobe("71c", "Eine Aufzeichnung bleibt unbeanstandet - ein Protokoll haelt fest, wo gemessen wurde, und wer es umschreibt, hat keines mehr (D-141)",
           _71_aufzeichnung, M71)


# --- Pruefung 72: Ein aktiviertes Pack steht auch im Berechtigungskorb ------------
#
# WARUM DIESE EINHEIT EINE INSTALLATION BAUT statt den Repositoriumsbaum zu praeparieren:
# Ihr Gegenstand IST die Installation. Im Quellrepositorium gibt es keine Skillablage
# eines Client Packs, und die Pruefung schwiege dort zu Recht - eine Sonde auf einer
# Kopie des Repositoriums haette nichts zu treffen.
#
# DREI SONDEN, UND SIE BELEGEN BEIDE RICHTUNGEN UND DIE ANKERFRAGE. Der gemessene Fall
# ist 72a: ein Pack WORTGETREU nach `framework/role-packs/README.md` aktiviert - Skill
# kopiert -, und der Korb weiss nichts davon. 72b ist die Gegenrichtung: ein Eintrag
# ohne Skill ist eine Zusage ohne Gegenstand (D-81). 72c fragt das Manifest: Ein
# FEHLENDES Feld `permission_tools.skill` ist ein Befund - der Unterschied zwischen
# "nicht abgebildet" und "gibt es nicht" gehoert deklariert (D-155).
#
# ZWEI GEGENPROBEN, UND DIE ZWEITE IST DIE WICHTIGERE. 72a belegt, dass eine
# ausgelieferte Installation durchlaeuft - ohne sie meldete die Sonde nur, dass
# irgendetwas meldet. 72b belegt den ZUSCHNITT: Dieselbe Aktivierung in einer
# `devin-desktop`-Installation bleibt unbeanstandet, weil das Manifest dort
# `permission_tools.skill` als LEER deklariert (erhoben am 2026-09-14, D-89: Der
# Skillaufruf ist dort ein Werkzeugaufruf, aber es ist keine Schreibweise bekannt, mit
# der eine Regel ihn beim Namen nennt). Ohne sie waere das Schweigen der Pruefung bei
# diesem Pack nicht von einer stillen Null zu unterscheiden.
M72 = "wird aber von keinem Eintrag der Berechtigungsdatei genannt"
M72_RUECK = "nennt keinen Skill in"
M72_FELD = "Feld permission_tools.skill fehlt"
P72_PACKSKILL = (".koolie/core/framework/role-packs/requirements-engineering/"
                 "skills/role-re-ticket").replace("/", os.sep)


def _72_pack_aktivieren(root: str, pack_skills: str) -> str:
    """Aktiviert das Role Pack wortgetreu nach README Punkt 4: Skill kopieren."""
    quelle = os.path.join(root, P72_PACKSKILL)
    name = os.path.basename(quelle)
    shutil.copytree(quelle, os.path.join(root, *pack_skills.split("/"), name))
    return name


def sonden_pack_im_korb() -> None:
    """Wirkungsnachweis fuer Pruefung 72 (CR-2026-114, D-238)."""
    for pack, skills, meldet in (("claude-code", ".claude/skills", True),
                                 ("devin-desktop", ".devin/skills", False)):
        root = installation(pack)
        try:
            if pack == "claude-code":
                # --- Gegenprobe 72a: die ausgelieferte Installation ------------
                melde("GEGENPROBE", "72a", M72 not in validator_ausgabe(root),
                      "Die ausgelieferte Installation deckt sich - zwoelf Skills, "
                      "zwoelf Eintraege, keine Meldung")

            name = _72_pack_aktivieren(root, skills)
            ausgabe = validator_ausgabe(root)
            getroffen = M72 in ausgabe and name in ausgabe
            if meldet:
                melde("SONDE", "72a", getroffen,
                      "Ein aktiviertes Role Pack ohne Korbeintrag wird gemeldet - der "
                      "gemessene Fall aus dem Vorbedingungsdurchgang von Buendel 5")
                if not getroffen:
                    notiz("        Ausgabe:", " | ".join(ausgabe.splitlines()[:6]))
            else:
                melde("GEGENPROBE", "72b", not getroffen,
                      "Dieselbe Aktivierung bei einem Pack mit leer DEKLARIERTEM "
                      "permission_tools.skill bleibt unbeanstandet (D-89)")

            if pack != "claude-code":
                continue

            # --- Sonde 72b: die Gegenrichtung -------------------------------
            # Der Eintrag bleibt, sein Skill geht - eine Freigabe ohne Gegenstand.
            shutil.rmtree(os.path.join(root, *skills.split("/"), name))
            shutil.rmtree(os.path.join(root, *skills.split("/"), "fw-plan"))
            ausgabe = validator_ausgabe(root)
            melde("SONDE", "72b", M72_RUECK in ausgabe and "fw-plan" in ausgabe,
                  "Ein Korbeintrag ohne Skill in der Ablage wird gemeldet - eine "
                  "Freigabe fuer einen Skill, den es nicht gibt (D-81)")

            # --- Sonde 72c: das Manifest schweigt statt zu deklarieren -------
            _manifest_aendern(root, "claude-code",
                              lambda m: m["permission_tools"].pop("skill", None))
            melde("SONDE", "72c", M72_FELD in validator_ausgabe(root),
                  "Ein FEHLENDES Feld permission_tools.skill wird gemeldet - eine "
                  "leere Liste ist deklariert, ein fehlendes Feld ist geraten (D-155)")
        finally:
            aufraeumen(os.path.dirname(root))


buendel(sonden_pack_im_korb,
        "Ein aktiviertes Pack steht auch im Berechtigungskorb - in beide Richtungen, "
        "und nur bei einem Client, dessen Manifest eine Schreibweise deklariert")




# --- Pruefung 73: Jede [DOK]-Matrixzeile nennt ihre Quelle -------------------------
#
# VIER SONDEN, UND SIE BELEGEN DIE VIER WEGE, AUF DENEN EINE ZUORDNUNG VERSCHWINDET.
# 73a ist der gemessene Ausgangsfall: eine Zeile, deren Belegkopf die Kennung nicht
# nennt - am 2026-09-18 traf das auf 29 von 43 Zeilen zu. 73b ist der Fall, den keine
# Zaehlung ohne Verweisaufloesung sieht: Beim Pack devin-desktop haengen B4, B5, B6 und
# B8 an B3, eine davon ueber zwei Glieder - nimmt man B3 die Kennung, verlieren FUENF
# Zeilen ihren Beleg, und die Meldung nennt die Kette. 73c und 73d sind die beiden
# Richtungen der deklarierten Luecke: eine neue, die nicht in P73_OFFEN steht, und eine
# deklarierte, die aus der Zeile verschwunden ist. Die zweite ist der Fall "eine
# Ausnahme ohne Gegenstand" (0.57.1) - sie sieht wie Sorgfalt aus und ist tot.
#
# DREI GEGENPROBEN, UND DIE ZWEITE IST DIE WICHTIGERE. 73a belegt, dass der
# ausgelieferte Bestand durchlaeuft - ohne sie meldete die Sonde nur, dass irgendetwas
# meldet. 73b belegt DIE KOPFREGEL: Eine Nennung der Marke HINTER dem Belegkopf bleibt
# unbeanstandet. Ohne sie waere die Pruefung nicht von einer Textsuche zu
# unterscheiden, und Zeile R5 des Packs claude-code - "ein Dokumentenabgleich belegt
# [DOK], nicht [TECHNISCH]" - fiele als Befund an. 73c belegt den Zuschnitt zur
# Vorlage: clients/_template/ fuehrt <TBD> in jeder Belegzelle und wird nicht gemessen.
M73 = "nennt im Belegkopf keine Quellenkennung"
M73_KETTE = "ueber den Verweis"
M73_UNDEKLARIERT = "steht aber nicht in P73_OFFEN"
M73_TOT = "als ausgesprochene Luecke, die Zeile sagt es aber nicht"
P73_CC = ".koolie/core/clients/claude-code/CLIENT_PACK.md".replace("/", os.sep)
P73_DD = ".koolie/core/clients/devin-desktop/CLIENT_PACK.md".replace("/", os.sep)
P73_VORLAGE = ".koolie/core/clients/_template/CLIENT_PACK.md".replace("/", os.sep)


def _73_kennung_nehmen(root: str) -> None:
    """Sonde: Zeile B1 des Packs claude-code verliert ihre Kennung."""
    ersetze(P(root, P73_CC),
            ("| `[DOK]` **`QC-5`** (Zuordnung `K-62`) |", "| `[DOK]` |"))


def _73_verweisziel_nehmen(root: str) -> None:
    """Sonde: B3 verliert die Kennung - vier weitere Zeilen verweisen darauf."""
    # Der Anker ist so kurz wie moeglich: Die Zeile B3 ist mit 0.86.0 neu geschrieben
    # worden (Muster-Semantik, D-277), und der laengere Suchtext von 0.85.0 traf nicht
    # mehr. Eine Sonde, deren Suchtext an der Prosa haengt, faellt bei jedem Messwert.
    ersetze(P(root, P73_DD),
            ("Mechanismus `[DOK]` **`QD-11`** (Zuordnung `K-62`)",
             "Mechanismus `[DOK]` (ohne Quelle)"))


def _73_luecke_erfinden(root: str) -> None:
    """Sonde: eine zweite ausgesprochene Luecke, die niemand deklariert hat."""
    ersetze(P(root, P73_DD),
            ("| `[DOK]` **`QD-12`** (Zuordnung `K-62`) |",
             "| `[DOK]` - QUELLE NICHT ZUGEORDNET (synthetisch) |"))


def _73_luecke_schliessen(root: str) -> None:
    """Sonde: die deklarierte Luecke verschwindet aus der Zeile, P73_OFFEN bleibt."""
    ersetze(P(root, P73_CC),
            ("🔴 **QUELLE NICHT ZUGEORDNET** (`K-62`, 2026-09-22)",
             "**`QC-2`** (synthetisch)"))


def _73_nennung_hinter_dem_kopf(root: str) -> None:
    """Gegenprobe: die Marke HINTER dem Belegkopf ist eine Nennung, kein Beleg."""
    ersetze(P(root, P73_CC),
            ("| `[DOK]` **`QC-5`** (Zuordnung `K-62`) |",
             "| `[DOK]` **`QC-5`** (Zuordnung `K-62`). Zur Einordnung: Ein "
             "Dokumentenabgleich belegt `[DOK]` und nie `[TECHNISCH]` (D-12) |"))


def _73_vorlage_leeren(root: str) -> None:
    """Gegenprobe: die Vorlage fuehrt <TBD> und wird nicht gemessen."""
    ersetze(P(root, P73_VORLAGE),
            ("| R1 | Die Wurzel-Anweisungsdatei wird zu Beginn jeder Sitzung "
             "ungefragt geladen | `.koolie/core/framework/runtime/root-instruction.md` "
             "| `<TBD>` | `<TBD>` | `<TBD>` |",
             "| R1 | Die Wurzel-Anweisungsdatei wird zu Beginn jeder Sitzung "
             "ungefragt geladen | `.koolie/core/framework/runtime/root-instruction.md` "
             "| `<TBD>` | `<TBD>` | `[DOK]` |"))


sonde("73a", "Eine [DOK]-Zeile ohne Quellenkennung im Belegkopf wird gemeldet - der "
             "gemessene Ausgangsfall: 29 von 43 Zeilen am 2026-09-18",
      _73_kennung_nehmen, M73)

sonde("73b", "Nimmt das Ziel eines Verweisbelegs seine Kennung, verlieren die "
             "verweisenden Zeilen sie mit - und die Meldung nennt die Kette",
      _73_verweisziel_nehmen, M73_KETTE)

sonde("73c", "Eine ausgesprochene Luecke, die nicht in P73_OFFEN steht, wird "
             "gemeldet - sonst waere die Marke eine Hintertuer",
      _73_luecke_erfinden, M73_UNDEKLARIERT)

sonde("73d", "Eine deklarierte Luecke, die aus der Zeile verschwunden ist, wird "
             "gemeldet - eine Ausnahme ohne Gegenstand ist tot (0.57.1)",
      _73_luecke_schliessen, M73_TOT)

gegenprobe("73a", "Der ausgelieferte Bestand laeuft durch - 46 Matrixzeilen, eine "
                  "deklarierte Luecke, keine Meldung",
           None, M73)

gegenprobe("73b", "Eine Nennung der Marke HINTER dem Belegkopf bleibt unbeanstandet - "
                  "die Kopfregel, ohne die jede Erlaeuterung ein Befund waere",
           _73_nennung_hinter_dem_kopf, M73)

gegenprobe("73c", "Die Vorlage clients/_template/ fuehrt <TBD> und wird nicht "
                  "gemessen - ein Pack ohne Client hat keine Quellenliste",
           _73_vorlage_leeren, M73)


# --- Pruefung 74: Eine Matrixzeile steht in ihrer Tabelle --------------------------
#
# ZWEI SONDEN UND ZWEI GEGENPROBEN. 74a ist der gemessene Fall, wortgetreu: die
# Leerzeile zwischen M5 und M6 des Packs devin-desktop, die dort seit 0.26.0 stand und
# zwei Matrixzeilen zu Fliesstext gemacht hat - im Pack wie im Hauptdokument. 74b ist
# dieselbe Bauform mit Fremdtext statt Leerzeile: Ein Absatz mitten in der Tabelle
# bricht sie ebenso, und er sieht harmloser aus.
#
# DIE ZWEITE GEGENPROBE IST DIE WICHTIGERE, und sie schuetzt den ZUSCHNITT. Abschnitt 5
# des Packs claude-code fuehrt eine Tabelle "Bekannte Abweichungen im Verhalten", und
# ihre erste Zeile beginnt mit "| B6 |" - dieselbe Gestalt wie eine Matrixzeile, in
# einer anderen Tabelle und in einem anderen Abschnitt. Wer nur nach dem Muster sucht,
# meldet sie mit. Die Pruefung liest deshalb nur unterhalb von "## 2.", und diese
# Gegenprobe belegt es an einer Zeile, die dort WIRKLICH steht.
M74 = "sieht aus wie eine Matrixzeile und steht in keiner Tabelle"
P74_DD = P73_DD
P74_CC = P73_CC


def _74_leerzeile_setzen(root: str) -> None:
    """Sonde: der gemessene Fall - eine Leerzeile vor M6, wie sie bis 0.84.0 stand."""
    zeile_nach(P(root, P74_DD), "| M5 | Eigener Nur-Lese-Modus", "")


def _74_fremdtext_setzen(root: str) -> None:
    """Sonde: ein Absatz mitten in der Tabelle bricht sie ebenso."""
    zeile_nach(P(root, P74_DD), "| M5 | Eigener Nur-Lese-Modus",
               "" + chr(10) + "Anmerkung zur Modusreihe - SYNTHETISCH." + chr(10))


def _74_abweichungstabelle_brechen(root: str) -> None:
    """Gegenprobe: dieselbe Gestalt in Abschnitt 5 wird NICHT gemessen."""
    zeile_nach(P(root, P74_CC), "## 5. Bekannte Abweichungen im Verhalten",
               "" + chr(10) + "| B6 | synthetische Zeile ohne Tabelle | - |")


sonde("74a", "Eine Leerzeile vor einer Matrixzeile wird gemeldet - der gemessene "
             "Fall, der seit 0.26.0 zwei Zeilen zu Fliesstext gemacht hat",
      _74_leerzeile_setzen, M74)

sonde("74b", "Ein Absatz mitten in der Tabelle bricht sie ebenso und wird gemeldet",
      _74_fremdtext_setzen, M74)

gegenprobe("74a", "Der ausgelieferte Bestand laeuft durch - beide Packs, jede "
                  "Matrixzeile in ihrer Tabelle",
           None, M74)

gegenprobe("74b", "Dieselbe Gestalt in Abschnitt 5 bleibt unbeanstandet - die "
                  "Pruefung liest unterhalb von '## 2.', nicht nach dem Muster",
           _74_abweichungstabelle_brechen, M74)


# --- Pruefung 75: Kein Restbestand des alten Namens (CR-2026-122, D-271) ------------
#
# EIN BUENDEL, WEIL DIE PRUEFUNG EIN REPOSITORIUM BRAUCHT. Sie liest `git ls-files`,
# und kopie() schliesst `.git` ausdruecklich aus - der Sondenbaum ist keins. Ohne
# `git init` haette Pruefung 75 in JEDER Sonde ihren dritten Ausgang genommen ("nicht
# messbar") und dabei ausgesehen wie eine, die nichts gefunden hat. Das ist derselbe
# Griff wie bei Gegenstand 2 der Pruefung 45, aus demselben Grund.
#
# VIER EINHEITEN, UND SIE MESSEN VIER VERSCHIEDENE DINGE:
#   75a (Gegenprobe) - der ausgelieferte Bestand laeuft durch. Sie belegt zugleich,
#                      dass die Pruefung ueberhaupt GELAUFEN ist: Ohne die Bedingung
#                      auf die Unmessbarkeitsmeldung bestuende sie auch ohne git.
#   75a (Sonde)      - der alte Name in einem verfolgten Traeger ausserhalb der
#                      Ausnahmemenge wird gemeldet.
#   75b (Gegenprobe) - derselbe Text in einem datierten Protokoll bleibt unbeanstandet.
#                      Das ist der ZUSCHNITT: Die Chronik beschreibt einen vergangenen
#                      Zustand (D-273), und ein Pfad, den es nicht mehr gibt, ist dort
#                      richtig.
#   75b (Sonde)      - die zweite Richtung: Eine Ausnahme, aus der die Fundstelle
#                      verschwunden ist, wird gemeldet. Ohne sie waere P75_AUSNAHMEN ein
#                      Sammelbecken, das nur waechst - eine Ausnahme, die nichts mehr
#                      ausnimmt, sieht wie Sorgfalt aus (0.57.1).
#   75c (Sonde)      - der verlorene Anker: Trifft das eigene Muster den alten Namen
#                      nicht mehr, meldet die Pruefung das, statt leise zu bestehen.
#
# DIE SONDEN BRINGEN IHREN GEGENSTAND SELBST MIT. 75a und 75b schreiben den alten Namen
# in den Baum, statt einen vorhandenen vorauszusetzen - die Abhilfe aus 0.86.0
# Abschnitt 2a. Genau daran sind dort sieben Sonden gefallen, und hier ist der Fall
# schaerfer: Der Gegenstand dieser Pruefung ist der Name, den dieses Release ENTFERNT.
M75_REST = "nennt den alten Namen noch"
M75_LEER = "nimmt nichts mehr aus und gehört entfernt"
M75_ANKER = "das eigene Muster findet den alten Namen nicht mehr"
M75_UNMESSBAR = "ist an diesem Ort nicht prüfbar"

P75_OPFER = ".koolie/core/OWNERS.md"
P75_CHRONIKOPFER = ".koolie/core/CHANGELOG.md"
P75_AUSNAHMEOPFER = ".koolie/core/clientmap.py"
P75_VALIDATOR = VALIDATOR.replace("/", os.sep)

_ALT = "leitwerk" + "-core"          # nicht als ein Literal: Pruefung 75 liest sich selbst


def sonden_altname() -> None:
    """Wirkungsnachweis zu Pruefung 75 an einem echten Repositorium."""
    root = kopie()
    try:
        if unterprozess(["git", "init", "-q", root]).returncode != 0:
            melde("BUENDEL", "-", False, "sonden_altname  [git nicht erreichbar]")
            notiz("        Ohne git liest Pruefung 75 keinen Bestand; sie nimmt dann "
                  "ihren dritten Ausgang und ist nicht messbar.")
            return
        unterprozess(["git", "-C", root, "add", "-A"])

        # --- Gegenprobe 75a: der ausgelieferte Bestand laeuft durch -----------------
        aus = validator_ausgabe(root)
        ok = (M75_REST not in aus and M75_LEER not in aus
              and M75_UNMESSBAR not in aus and M75_ANKER not in aus)
        melde("GEGENPROBE", "75a", ok,
              "Der ausgelieferte Bestand laeuft durch - P75_AUSNAHMEN deckt sich in "
              "BEIDE Richtungen mit dem Bestand, und die Pruefung ist dabei "
              "nachweislich gelaufen")
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "75" in z or "Namen" in z)[:400])

        # --- Sonde 75a: der alte Name in einem verfolgten Traeger -------------------
        pfad = P(root, *P75_OPFER.split("/"))
        schreib(pfad, lies(pfad) + "\r\n<!-- SYNTHETISCH: " + _ALT + " -->\r\n")
        unterprozess(["git", "-C", root, "add", "-A"])
        aus = validator_ausgabe(root)
        getroffen = M75_REST in aus and P75_OPFER in aus
        melde("SONDE", "75a", getroffen,
              "Der alte Name in einem verfolgten Traeger ausserhalb der Ausnahmemenge "
              "wird gemeldet - mit Traeger und Zahl")
        if not getroffen:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
        schreib(pfad, lies(pfad).replace(
            "\r\n<!-- SYNTHETISCH: " + _ALT + " -->\r\n", ""))

        # --- Gegenprobe 75b: derselbe Text in der Chronik ---------------------------
        pfad = P(root, *P75_CHRONIKOPFER.split("/"))
        schreib(pfad, lies(pfad) + "\r\n<!-- SYNTHETISCH: " + _ALT + " -->\r\n")
        unterprozess(["git", "-C", root, "add", "-A"])
        aus = validator_ausgabe(root)
        ok = M75_REST not in aus
        melde("GEGENPROBE", "75b", ok,
              "Derselbe Text in einem Chroniktraeger bleibt unbeanstandet - die Chronik "
              "beschreibt einen vergangenen Zustand und wandert nicht mit (D-273)")
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
        schreib(pfad, lies(pfad).replace(
            "\r\n<!-- SYNTHETISCH: " + _ALT + " -->\r\n", ""))

        # --- Sonde 75b: die zweite Richtung - eine leer gewordene Ausnahme ----------
        pfad = P(root, *P75_AUSNAHMEOPFER.split("/"))
        text = lies(pfad)
        treffer = text.lower().count("leitwerk")
        if treffer != 1:
            melde("SONDE", "75b", False,
                  "Die zweite Richtung von Pruefung 75  [Praeparation gebrochen]")
            notiz("        %s nennt den alten Namen %dmal, erwartet genau einmal - "
                  "die Sonde hat ihren Gegenstand verloren."
                  % (P75_AUSNAHMEOPFER, treffer))
        else:
            schreib(pfad, re.sub("(?i)leitwerk", "koolie", text))
            unterprozess(["git", "-C", root, "add", "-A"])
            aus = validator_ausgabe(root)
            getroffen = M75_LEER in aus and P75_AUSNAHMEOPFER in aus
            melde("SONDE", "75b", getroffen,
                  "Eine Ausnahme, aus der die Fundstelle verschwunden ist, wird "
                  "gemeldet - ohne diese Richtung waechst P75_AUSNAHMEN nur")
            if not getroffen:
                notiz("        Ausgabe:", " | ".join(
                    z for z in aus.splitlines() if "FEHLER" in z)[:400])
            schreib(pfad, text)
            unterprozess(["git", "-C", root, "add", "-A"])

        # --- Sonde 75c: der verlorene Anker -----------------------------------------
        pfad = P(root, P75_VALIDATOR)
        text = lies(pfad)
        alt = 'P75_ALTNAME = re.compile(r"(?i)leitwerk")'
        if text.count(alt) != 1:
            melde("SONDE", "75c", False,
                  "Der verlorene Anker von Pruefung 75  [Praeparation gebrochen]")
            notiz("        Suchtext %r steht %dmal im Validator." % (alt, text.count(alt)))
        else:
            schreib(pfad, text.replace(
                alt, 'P75_ALTNAME = re.compile(r"(?i)diesenamengibtesnicht")'))
            aus = validator_ausgabe(root)
            getroffen = M75_ANKER in aus
            melde("SONDE", "75c", getroffen,
                  "Trifft das eigene Muster den alten Namen nicht mehr, meldet "
                  "Pruefung 75 das - statt jede Umbenennung als vollstaendig zu melden")
            if not getroffen:
                notiz("        Ausgabe:", " | ".join(
                    z for z in aus.splitlines() if "FEHLER" in z)[:400])
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_altname,
        "Pruefung 75 an einem echten Repositorium: der Bestand, ein Restbestand, die "
        "Chronik als Zuschnitt, die leer gewordene Ausnahme und der verlorene Anker")


# --- Pruefung 76: Die Lage des Kerns steht an vier Stellen (CR-2026-122, D-299) -----
#
# DREI SONDEN UND EINE GEGENPROBE, und die dritte Sonde ist die wichtigste: Sie legt
# die BASENAME-BINDUNG WIEDER AN, die dieses Release entfernt hat. Ohne sie waere der
# erste Gegenstand - "alle vier tragen denselben Wert" - erfuellbar, indem alle vier
# denselben Fehler machen. Genau das war der Zustand bis 0.87.0, und der Validator hat
# ihn nicht gemeldet, weil er ihn teilte.
#
# WARUM NICHT AN validate-framework.py PRAEPARIERT WIRD: Dessen KERN traegt die Lage,
# mit der der Validator seinen eigenen Baum findet. Wer ihn verstellt, misst nicht
# Pruefung 76, sondern einen Validator ohne Gegenstand.
M76_UNGLEICH = "nicht überall gleich"
M76_BASENAME = "bindet <CORE_DIR> über os.path.basename()"
M76_ANKER = "führt keine Angabe der Kernlage mehr"

P76_HOOK = ".koolie/core/tests/scripts/hook-check-secrets.py".replace("/", os.sep)
P76_CLIENTMAP = ".koolie/core/clientmap.py".replace("/", os.sep)
P76_ABLAGE = ".koolie/core/tests/erhebungen/ablage.py".replace("/", os.sep)


def _76_lage_verstellen(root: str) -> None:
    """Sonde: der Schutz-Hook traegt eine andere Lage als die uebrigen drei."""
    pfad = P(root, P76_HOOK)
    schreib(pfad, ersetzt(lies(pfad),
                          ('CORE_REL = ".koolie/core"',
                           'CORE_REL = ".koolie/anderswo"'),
                          quelle=os.path.basename(pfad)))


def _76_basename_wieder(root: str) -> None:
    """Sonde: die Bindung ueber basename, die bis 0.87.0 an vier Stellen stand."""
    pfad = P(root, P76_CLIENTMAP)
    schreib(pfad, ersetzt(lies(pfad),
                          ('def core_dir_name(man: dict) -> str:',
                           '_sonde = {}                      # SYNTHETISCH\r\n'
                           '_sonde["<CORE_DIR>"] = os.path.basename("x")\r\n\r\n\r\n'
                           'def core_dir_name(man: dict) -> str:'),
                          quelle=os.path.basename(pfad)))


def _76_anker_entfernen(root: str) -> None:
    """Sonde: eine der vier Stellen fuehrt keine Lageangabe mehr."""
    pfad = P(root, P76_ABLAGE)
    schreib(pfad, ersetzt(lies(pfad),
                          ('CORE_REL = ".koolie/core"', '_lage = ".koolie/core"'),
                          ("CORE_REL.count", "_lage.count"),
                          quelle=os.path.basename(pfad)))


sonde("76a", "Traegt eine der vier Stellen eine andere Lage, wird es gemeldet - eine "
             "Installation laege sonst je nach aufrufendem Werkzeug anderswo",
      _76_lage_verstellen, M76_UNGLEICH)

sonde("76b", "Die Bindung ueber os.path.basename wird gemeldet - sie stand bis 0.87.0 "
             "an vier Stellen und haette den Umzug nicht ueberlebt",
      _76_basename_wieder, M76_BASENAME)

sonde("76c", "Verliert eine der vier Stellen ihre Lageangabe, meldet Pruefung 76 den "
             "verlorenen Anker, statt drei von vier stillschweigend zu vergleichen",
      _76_anker_entfernen, M76_ANKER)

gegenprobe("76a", "Der ausgelieferte Bestand laeuft durch - vier Stellen, ein Wert, "
                  "keine basename-Bindung",
           None, M76_UNGLEICH)


# --- Pruefung 77: Der Stand des Hauptdokuments (CR-2026-124, D-312) ----------------
#
# DREI SONDEN UND EINE GEGENPROBE. Die zweite ist die, die man weglassen wuerde: Sie
# setzt in dieselbe Zeile zwei VERSCHIEDENE Staende. Ohne sie waere der Vergleich mit
# VERSION erfuellbar, indem die Zeile zwei Werte nennt und einer davon passt - und
# welcher gemeint ist, stuende nirgends.
#
# WARUM AN 00-kopf.md UND NICHT AN VERSION PRAEPARIERT WIRD: VERSION traegt der
# Validator selbst gegen die Artefaktversionen (Pruefung 13), bis 1.4.0 auch gegen
# die Uebergabe (Pruefung 67). Wer dort verstellt, loest mehrere Meldungen aus und
# misst keine davon.
M77_STAND = "die Kopfzeile nennt den Stand"
M77_UNEINIG = "und das Framework-Release"
M77_ANKER = "keine Zeile der Form"

P77_KOPF = ".koolie/core/build/doc/00-kopf.md".replace("/", os.sep)


def _77_stand_verstellen(root: str) -> None:
    """Sonde: das Dokument bleibt auf einem aelteren Stand stehen."""
    pfad = P(root, P77_KOPF)
    schreib(pfad, ersetzt(lies(pfad),
                          ("| Dokumentversion | ", "| Dokumentversion | 0.9.0 (entspricht "
                           "Framework-Release 0.9.0) |\r\n| Dokumentversion frueher | "),
                          quelle=os.path.basename(pfad)))


def _77_zeile_uneinig(root: str) -> None:
    """Sonde: die Zeile nennt zwei verschiedene Staende."""
    pfad = P(root, P77_KOPF)
    text = lies(pfad)
    anfang = text.index("| Dokumentversion | ")
    ende = text.index("|", text.index("(entspricht Framework-Release", anfang)) + 1
    schreib(pfad, text[:anfang]
            + "| Dokumentversion | 0.89.0 (entspricht Framework-Release 0.88.1) |"
            + text[ende:])


def _77_anker_entfernen(root: str) -> None:
    """Sonde: die Kopfzeile des Dokuments ist weg."""
    pfad = P(root, P77_KOPF)
    schreib(pfad, ersetzt(lies(pfad),
                          ("| Dokumentversion | ", "| Fassung | "),
                          quelle=os.path.basename(pfad)))


sonde("77a", "Bleibt das Hauptdokument auf einem aelteren Stand stehen, wird es "
             "gemeldet - genau so ist es zweiundvierzig Releases zurueckgefallen",
      _77_stand_verstellen, M77_STAND)

sonde("77b", "Nennt dieselbe Zeile zwei verschiedene Staende, wird es gemeldet - sonst "
             "genuegte es, wenn einer der beiden Werte passt",
      _77_zeile_uneinig, M77_UNEINIG)

sonde("77c", "Verliert der Kopf seine Versionszeile, meldet Pruefung 77 den verlorenen "
             "Anker, statt still zu bestehen",
      _77_anker_entfernen, M77_ANKER)

gegenprobe("77a", "Der ausgelieferte Bestand laeuft durch - Dokumentversion, genanntes "
                  "Release und VERSION tragen denselben Wert",
           None, M77_STAND)


# --- Pruefung 78: Die zaehlbaren Aussagen des Hauptdokuments (CR-2026-125, D-315) --
#
# EIN BUENDEL, WEIL DIE PRUEFUNG EIN REPOSITORIUM BRAUCHT. Sie zaehlt die versionierten
# Dateien des Kerns ueber `git ls-files`, und kopie() schliesst `.git` ausdruecklich aus.
# Ohne `git init` naehme sie in JEDER Sonde ihren dritten Ausgang ("nicht messbar") und
# saehe dabei aus wie eine, die nichts gefunden hat - derselbe Griff wie bei Pruefung 75
# und 45, aus demselben Grund.
#
# 🔴 KEINE SONDE VERANKERT EINE ZAHL WOERTLICH, und das ist die Lehre von 0.89.0: Dort
# sind zwei Sonden gebrochen, weil sie einen Wert als Suchtext hielten, den ein Release
# berichtigt hat. Die Sonden hier LESEN die Zahl aus dem Traeger und verstellen sie
# relativ. Eine Sonde, die eine Zahl mitpflegen muss, faellt bei der naechsten Aenderung
# aus - und zwar als scheinbarer Befund.
#
# VIER EINHEITEN, UND SIE MESSEN VIER VERSCHIEDENE DINGE:
#   78a (Gegenprobe) - der ausgelieferte Bestand laeuft durch, und die Pruefung ist dabei
#                      nachweislich gelaufen (keine Unmessbarkeitsmeldung).
#   78a (Sonde)      - eine verstellte Zahl der Pruefungen wird gemeldet.
#   78b (Sonde)      - eine verstellte Zahl der versionierten Dateien wird gemeldet. Ohne
#                      sie genuegte es, EINE der drei Zahlen zu treffen.
#   78c (Sonde)      - der verlorene Anker: Faellt der Satz weg, meldet die Pruefung das,
#                      statt leise zu bestehen (D-23).
#   78d, 78e         - ENTFALLEN mit 1.4.1 (D-350): Sie maßen die Abnahmezeile der
#                      Uebergabe, und die ist nicht mehr versioniert.
M78_WERTE = "nennt nicht die gezählten Werte"
M78_ANKER = "steht nicht genau einmal"
M78_UNMESSBAR = "kein Git-Bestand lesbar"

P78_OPFER = ".koolie/core/build/doc/26-qs-test.md"
P78_ANKER = "Der Validator führt **"


def _78_zahl_verstellen(text: str, muster: str) -> str:
    """Die erste Zahl hinter `muster` um eins erhoehen - ohne sie woertlich zu kennen."""
    treffer = re.search(re.escape(muster) + r"(\d+)", text)
    if not treffer:
        raise Praeparationsfehler(
            "26-qs-test.md: %r mit folgender Zahl nicht gefunden - die Sonde zu "
            "Pruefung 78 haette nichts zu verstellen" % muster)
    neu = str(int(treffer.group(1)) + 1)
    return text[:treffer.start(1)] + neu + text[treffer.end(1):]


def sonden_dokumentzahlen() -> None:
    """Wirkungsnachweis zu Pruefung 78 an einem echten Repositorium."""
    root = kopie()
    try:
        if unterprozess(["git", "init", "-q", root]).returncode != 0:
            melde("BUENDEL", "-", False, "sonden_dokumentzahlen  [git nicht erreichbar]")
            notiz("        Ohne git zaehlt Pruefung 78 keine versionierten Dateien; sie "
                  "nimmt dann ihren dritten Ausgang und ist nicht messbar.")
            return
        unterprozess(["git", "-C", root, "add", "-A"])
        pfad = P(root, *P78_OPFER.split("/"))
        urtext = lies(pfad)

        # --- Gegenprobe 78a: der ausgelieferte Bestand laeuft durch ------------------
        aus = validator_ausgabe(root)
        ok = (M78_WERTE not in aus and M78_ANKER not in aus
              and M78_UNMESSBAR not in aus)
        melde("GEGENPROBE", "78a", ok,
              "Der ausgelieferte Bestand laeuft durch - die drei Zahlen des Satzes "
              "decken sich mit dem Bestand, und die Pruefung ist dabei nachweislich "
              "gelaufen")
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "78" in z or "Prüfapparat" in z)[:400])

        # --- Sonde 78a: die Zahl der Pruefungen verstellt ----------------------------
        schreib(pfad, _78_zahl_verstellen(urtext, P78_ANKER))
        unterprozess(["git", "-C", root, "add", "-A"])
        aus = validator_ausgabe(root)
        melde("SONDE", "78a", M78_WERTE in aus,
              "Eine verstellte Zahl der Pruefungen wird gemeldet - genau diese Zahl "
              "stand ein Release zu lang auf ihrem alten Wert")
        if M78_WERTE not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])

        # --- Sonde 78b: die Zahl der versionierten Dateien verstellt -----------------
        schreib(pfad, _78_zahl_verstellen(urtext, "Prüfungen** über "))
        unterprozess(["git", "-C", root, "add", "-A"])
        aus = validator_ausgabe(root)
        melde("SONDE", "78b", M78_WERTE in aus,
              "Eine verstellte Zahl der versionierten Dateien wird ebenfalls gemeldet - "
              "sonst genuegte es, eine der drei Zahlen zu treffen")
        if M78_WERTE not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])

        # --- Sonde 78c: der verlorene Anker ------------------------------------------
        schreib(pfad, urtext.replace(P78_ANKER, "Der Validator kennt **", 1))
        unterprozess(["git", "-C", root, "add", "-A"])
        aus = validator_ausgabe(root)
        melde("SONDE", "78c", M78_ANKER in aus,
              "Faellt der Satz ueber den Pruefapparat weg, meldet Pruefung 78 den "
              "verlorenen Anker, statt still zu bestehen")
        if M78_ANKER not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
        schreib(pfad, urtext)

    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_dokumentzahlen,
        "Pruefung 78 haelt die drei Gegenwartszahlen des Hauptdokuments gegen den "
        "gezaehlten Bestand, an einem echten Repositorium")


# --- Pruefung 79: Die Lizenz an zwei Stellen (CR-2026-126, D-317) ------------------
#
# DREI SONDEN UND EINE GEGENPROBE. Die dritte ist die, die man weglassen wuerde: Sie
# ersetzt BEIDE Dateien durch denselben Nicht-Lizenztext. Ohne sie belegte die Pruefung
# nur, dass zwei Dateien gleich sind - und das sind zwei leere auch.
M79_UNGLEICH = "trägt nicht denselben Inhalt wie"
M79_FEHLT = "Die Lizenz MUSS an beiden Stellen liegen"
M79_MARKE = "trägt nicht die GNU General Public License"

P79_KERNDATEI = ".koolie/core/LICENSE"
P79_WURZELDATEI = "LICENSE"


def _79_auseinander(root: str) -> None:
    """Sonde: die beiden Lizenzdateien laufen auseinander."""
    pfad = P(root, *P79_KERNDATEI.split("/"))
    schreib(pfad, lies(pfad) + "\n<!-- SYNTHETISCH: Zusatz nur in der Kernfassung -->\n")


def _79_kernfassung_entfernen(root: str) -> None:
    """Sonde: die mitwandernde Fassung fehlt - genau der Fall von §4 GPL-3.0."""
    os.remove(P(root, *P79_KERNDATEI.split("/")))


def _79_keine_lizenz(root: str) -> None:
    """Sonde: beide Dateien gleich, aber keine Lizenz - die Gleichheit allein traegt nicht."""
    ersatz = "SYNTHETISCH: hier stand einmal ein Lizenztext.\n"
    for rel in (P79_KERNDATEI, P79_WURZELDATEI):
        schreib(P(root, *rel.split("/")), ersatz)


sonde("79a", "Laufen die beiden Lizenzdateien auseinander, wird es gemeldet - welche "
             "gilt, stuende sonst nirgends",
      _79_auseinander, M79_UNGLEICH)

sonde("79b", "Fehlt die mitwandernde Fassung im Kern, wird es gemeldet - ein Werk ohne "
             "seine Lizenz weiterzugeben ist unzulaessig",
      _79_kernfassung_entfernen, M79_FEHLT)

sonde("79c", "Zwei gleiche Dateien ohne Lizenztext werden gemeldet - Gleichheit allein "
             "erfuellen auch zwei leere Dateien",
      _79_keine_lizenz, M79_MARKE)

gegenprobe("79a", "Der ausgelieferte Bestand laeuft durch - beide Stellen, ein Inhalt, "
                  "und dieser Inhalt ist die GPL-3.0",
           None, M79_UNGLEICH)


# --- Pruefung 80: Die Gegenzeichnung der Abnahmeprotokolle (CR-2026-127, D-319) ----
#
# DREI SONDEN UND ZWEI GEGENPROBEN. Die zweite Gegenprobe ist die, die man weglassen
# wuerde, und sie traegt die ganze Entscheidung: Ein offenes <TBD> im
# Gegenzeichnungsabschnitt eines ARBEITSPROTOKOLLS muss unbeanstandet bleiben. Ohne sie
# waere der Zuschnitt aus D-319 eine Behauptung im Kommentar statt eine gemessene
# Eigenschaft - und die Pruefung verlangte still die Gegenzeichnung von 125 Protokollen
# statt von zehn.
#
# 🔴 JEDE SONDE PRUEFT IHRE EIGENE FUNDSTELLE, nicht irgendeine Meldung. Der
# ausgelieferte Bestand traegt sieben frisch gezeichnete Abnahmeprotokolle; eine Sonde,
# die nur auf den Meldungstext prueft, bestuende auch ohne Praeparation. Der Erwartungs-
# text nennt deshalb den DATEINAMEN des Opfers - dieselbe Bauform wie bei Sonde 75a.
M80_FEHLT = "2026-09-10-FW-KO-02.md: kein Abschnitt"
M80_TBD = "2026-09-10-FW-KO-02.md: der Abschnitt `Gegenzeichnung` trägt noch ein offenes"
M80_ANKER = "kein einziges Abnahmeprotokoll des Testkatalogs gefunden"

P80_OPFER = ".koolie/core/tests/protocols/2026-09-10-FW-KO-02.md"
P80_ARBEITSPROTOKOLL = ".koolie/core/tests/protocols/2026-09-13-B06-gegenpruefung.md"


def _80_abschnitt_entfernen(root: str) -> None:
    """Sonde: einem Abnahmeprotokoll fehlt die Gegenzeichnung."""
    pfad = P(root, *P80_OPFER.split("/"))
    text = lies(pfad)
    anfang = text.find("## Gegenzeichnung")
    if anfang < 0:
        raise Praeparationsfehler(
            "2026-09-10-FW-KO-02.md: kein Abschnitt 'Gegenzeichnung' gefunden - die "
            "Sonde zu Pruefung 80 haette nichts zu entfernen")
    schreib(pfad, text[:anfang].rstrip("\r\n") + "\r\n")


def _80_tbd_zurueck(root: str) -> None:
    """Sonde: der Abschnitt ist da und traegt wieder ein offenes <TBD>."""
    pfad = P(root, *P80_OPFER.split("/"))
    text = lies(pfad)
    anfang = text.find("## Gegenzeichnung")
    if anfang < 0:
        raise Praeparationsfehler(
            "2026-09-10-FW-KO-02.md: kein Abschnitt 'Gegenzeichnung' gefunden")
    schreib(pfad, text + "\r\n| Zweitpruefung | `<TBD: Rolle>` | | |\r\n")


def _80_anker_entfernen(root: str) -> None:
    """Sonde: kein Traeger passt mehr auf das Namensmuster der Abnahmeprotokolle."""
    ablage = P(root, *".koolie/core/tests/protocols".split("/"))
    umbenannt = 0
    for name in sorted(os.listdir(ablage)):
        if "-FW-" in name and name.endswith(".md"):
            os.rename(os.path.join(ablage, name),
                      os.path.join(ablage, name.replace("-FW-", "-fw", 1)))
            umbenannt += 1
    if not umbenannt:
        raise Praeparationsfehler(
            "tests/protocols/: kein Traeger mit '-FW-' im Namen - die Sonde zum "
            "verlorenen Anker haette nichts umzubenennen")


def _80_arbeitsprotokoll_offen(root: str) -> None:
    """Gegenprobe: ein ARBEITSPROTOKOLL mit offenem Abschnitt - der Zuschnitt."""
    pfad = P(root, *P80_ARBEITSPROTOKOLL.split("/"))
    text = lies(pfad)
    if "<TBD" not in text:
        raise Praeparationsfehler(
            "2026-09-13-B06-gegenpruefung.md: traegt kein offenes <TBD> mehr - die "
            "Gegenprobe zum Zuschnitt von Pruefung 80 haette keinen Gegenstand")
    schreib(pfad, text + "\r\n| Zweitpruefung | `<TBD: Rolle>` | | |\r\n")


sonde("80a", "Fehlt einem Abnahmeprotokoll die Gegenzeichnung, wird es mit Dateinamen "
             "gemeldet - fuenf von zehn hatten den Abschnitt nie",
      _80_abschnitt_entfernen, M80_FEHLT)

sonde("80b", "Ein offenes <TBD> im Abschnitt wird gemeldet - eine Gegenzeichnung ist "
             "eine Handlung und kein Feld, das ein Werkzeug fuellt",
      _80_tbd_zurueck, M80_TBD)

sonde("80c", "Passt kein Traeger mehr auf das Namensmuster, meldet Pruefung 80 den "
             "verlorenen Anker, statt still ueber null Protokolle zu bestehen",
      _80_anker_entfernen, M80_ANKER)

gegenprobe("80a", "Der ausgelieferte Bestand laeuft durch - alle zehn Abnahmeprotokolle "
                  "tragen ihren Abschnitt ohne offenes <TBD>",
           None, M80_FEHLT)

gegenprobe("80b", "Ein offenes <TBD> in einem ARBEITSPROTOKOLL bleibt unbeanstandet - "
                  "das ist der Zuschnitt aus D-319 und nicht bloss seine Behauptung",
           _80_arbeitsprotokoll_offen, "B06-gegenpruefung.md: der Abschnitt")


# --- Selbstprobe: der Beschreibungssatz je Einheit (CR-2026-068, D-95) ------------
#
# Bis 0.45.0 trug jede Einzelsonde einen erklaerenden Text und jedes Buendel keinen. Wer
# den Lauf las, sah eine Folge von Meldungen und nicht, was sie zusammen belegen sollten.
# Seit 0.46.0 ist der Satz Pflicht - und eine Pflicht ohne Nachzaehlen ist eine Zusage
# ohne Mechanismus, also genau der wiederkehrende Befundtyp dieses Projekts.
#
# GRENZE: Sie zaehlt WORTE, nicht Sinn. Ein Satz aus achtzehn Fuellwoertern besteht sie.
# Die untere Grenze faengt die Kennung, die sich als Satz ausgibt ("Pack ohne
# Auskunftsabschnitt"), die obere den Absatz, der sich in eine Zeile verirrt hat.
# Dazwischen entscheidet der Mensch, und das ist Absicht.
def selbstprobe_beschreibungen() -> None:
    """Jede angemeldete Einheit traegt ihren Satz in der vorgeschriebenen Laenge."""
    abweichend = [e for e in EINHEITEN if not SATZ_MIN <= worte(e.satz) <= SATZ_MAX]
    melde("SELBSTPROBE", "B1", not abweichend,
          "Alle %d Einheiten tragen einen Beschreibungssatz von %d bis %d Worten"
          % (len(EINHEITEN), SATZ_MIN, SATZ_MAX))
    for e in abweichend:
        notiz("        %s %s: %d Worte - %s"
              % (e.art, e.kennung, worte(e.satz), e.satz))


buendel(selbstprobe_beschreibungen,
        "Zaehlt die Worte jedes Beschreibungssatzes dieses Laufs - eine Kennung ohne "
        "Satz und ein Absatz in einer Zeile fallen beide auf")


# --- Der Filter: eine Schleife ist kein Abnahmelauf (D-191) -----------------------
#
# ANLASS. Der Lauf faehrt 237 Einheiten, jede mit eigener Kopie des Repositoriums und
# eigenem Validatorlauf - rund 2300 s Rechenzeit, und zweimal je Release (D-49). Wer
# eine einzelne Pruefung aendert, bezahlte bis 0.68.0 den ganzen Apparat, um eine
# Meldung zu sehen. Ein Werkzeug, das vor jedem Schritt fuenf Minuten kostet, wird
# seltener gefahren, als es soll.
#
# 🔴 DIE GEFAHR IST NICHT DIE GESCHWINDIGKEIT, SONDERN DIE VERWECHSLUNG. Ein Teillauf,
# der aussieht wie ein Abnahmelauf, ist die Bauform "die Null durch Konstruktion"
# (0.59.1): gruen, weil nichts gefahren wurde. Deshalb sagt der Teillauf es dreimal -
# im Kopf, in der Ergebniszeile und im Abschlusssatz - und D-23 bleibt unberuehrt: Die
# Sonde existiert weiter, gekuerzt wird die SCHLEIFE, nicht der Nachweis.
def waehle(einheiten: list, nur: list) -> list:
    """Die Einheiten, deren Kennung mit einer der genannten Marken beginnt.

    `--nur 44` nimmt 44a bis 44f, `--nur 62,48b` nimmt beide Blocke der Pruefung 62 und
    genau eine Gegenprobe. Verglichen wird kleingeschrieben und am ANFANG der Kennung:
    Eine Marke, die nichts trifft, ist ein Abbruch und kein leerer Lauf - sonst meldete
    ein Tippfehler "alle bestanden".
    """
    if not nur:
        return list(einheiten)
    gewaehlt, ohne_treffer = [], []
    for marke in nur:
        treffer = [e for e in einheiten if e.kennung.lower().startswith(marke)]
        if not treffer:
            ohne_treffer.append(marke)
        for e in treffer:
            if e not in gewaehlt:
                gewaehlt.append(e)
    if ohne_treffer:
        sys.exit("--nur: keine Einheit zu %s (bekannt: %s ... ; --liste zeigt alle)"
                 % (", ".join(ohne_treffer),
                    ", ".join(e.kennung for e in einheiten[:6])))
    return [e for e in einheiten if e in gewaehlt]


def selbstprobe_filter() -> None:
    """Der Filter waehlt, was er soll - und nichts daneben."""
    class Muster:
        def __init__(self, kennung):
            self.kennung = kennung
    proben = [Muster(k) for k in ("6", "44a", "44b", "62a", "62b", "B1")]
    faelle = [
        ([], 6, "ohne --nur laeuft alles"),
        (["44"], 2, "--nur 44 nimmt 44a und 44b"),
        (["62", "b1"], 3, "--nur 62,b1 nimmt drei Einheiten, Grossschreibung egal"),
        (["6"], 2, "--nur 6 nimmt 6 UND 62a? nein - nur was mit 6 beginnt"),
    ]
    for marken, erwartet, satz in faelle[:3]:
        melde("SELBSTPROBE", "F1", len(waehle(proben, marken)) == erwartet, satz)
    getroffen = [e.kennung for e in waehle(proben, ["6"])]
    melde("SELBSTPROBE", "F2", getroffen == ["6", "62a", "62b"],
          "Eine Marke trifft am Anfang der Kennung, nicht auf die ganze: 6 nimmt auch 62a")


buendel(selbstprobe_filter,
        "Der Filter dieses Laufs an sechs gebauten Kennungen - er waehlt am Anfang der "
        "Kennung, ohne Ruecksicht auf Grossschreibung")

# --- Der Laeufer ------------------------------------------------------------------

def bahnfolge(einheiten: list) -> list:
    """Reihenfolge der Einreichung - Buendel zuerst, danach wie angemeldet.

    Die AUSGABE folgt der Anmeldereihenfolge; diese Folge hier bestimmt allein, welche
    Einheit zuerst eine freie Bahn bekommt. Buendel sind die langen Stuecke - sie legen
    echte Installationen an und fahren mehrere Validatorlaeufe nacheinander -, und ein
    langes Stueck, das zuletzt beginnt, bestimmt allein das Ende des Laufs.

    Sie ist fest und nicht gemessen: Eine Einreihung, die von der Laufzeit des letzten
    Laufs abhinge, machte zwei Laeufe unvergleichbar und die Ausgabe von der Maschine
    abhaengig.
    """
    return ([e for e in einheiten if e.art == "BUENDEL"]
            + [e for e in einheiten if e.art != "BUENDEL"])


def fahren(einheiten: list, bahnen: int) -> int:
    """Alle Einheiten fahren; ausgegeben wird in der Reihenfolge der Anmeldung.

    Der Unterschied zwischen beiden Zweigen ist die Laufzeit, nicht die Ausgabe: Bei
    `--bahnen 1` faellt der Ausfuehrer weg, und die Einheiten laufen in genau der
    Reihenfolge, in der sie in dieser Datei stehen. Dass beide Zweige dieselben Zeilen
    erzeugen, ist die Zusage dieses Umbaus - der Wirkungsnachweis dazu steht im
    Protokoll zu 0.46.0.
    """
    if bahnen == 1:
        for einheit in einheiten:
            einheit.fahren()
            einheit.ausgeben()
        return sum(e.fehler for e in einheiten)
    with ThreadPoolExecutor(max_workers=bahnen) as ausfuehrer:
        auftraege = {id(e): ausfuehrer.submit(e.fahren) for e in bahnfolge(einheiten)}
        for einheit in einheiten:
            auftraege[id(einheit)].result()
            einheit.ausgeben()
    return sum(e.fehler for e in einheiten)


TRENNLINIE = ("--- Auswertung: Name und Laufzeit je Einheit, langsamste zuerst "
              "(nicht Teil der zeilengleichen Abnahme nach D-49) ---")


def auswertung(einheiten: list, wanduhr: float, bahnen: int) -> None:
    """Die Laufzeiten - unterhalb der Trennlinie und ausserhalb der Abnahme.

    Sie stehen hier und nicht in den Ergebniszeilen, weil D-49 den Lauf in beiden
    Kodierungsumgebungen ZEILENGLEICH abnimmt. Eine Laufzeit ist nie zweimal dieselbe;
    stuende sie in der Ergebniszeile, brauchte der Vergleich einen Filter - und eine
    Abnahmeform, die einen Filter braucht, ist keine mehr.

    Die Rechenzeit ist die Summe der Einzellaufzeiten, die Wanduhr die vergangene Zeit.
    Ihr Verhaeltnis ist der einzige Messwert, der etwas ueber die Nebenlaeufigkeit sagt.
    """
    print()
    print(TRENNLINIE)
    for einheit in sorted(einheiten, key=lambda e: e.dauer, reverse=True):
        print("%8s s  %-10s %-32s %s"
              % (zahl(einheit.dauer), einheit.art, einheit.kennung,
                 kurz(einheit.satz, 44)))
    rechenzeit = sum(e.dauer for e in einheiten)
    print("Gesamt %s s Rechenzeit in %s s Wanduhr auf %d Bahn%s%s."
          % (zahl(rechenzeit), zahl(wanduhr), bahnen, "" if bahnen == 1 else "en",
             "" if bahnen == 1 or wanduhr <= 0
             else " (Faktor %s)" % zahl(rechenzeit / wanduhr)))


# --- Das ZWEITE Pruefmittel: ausgesetzt ist nicht weggelassen (K-90, D-258) -------
#
# 🔴 ANLASS, UND ER IST ZWEITEILIG. `validate-output.py` traegt das zweite
# Pruefmittel von drei Ergebniszellen - und hatte bis 0.83.0 **keine einzige Sonde**.
# Nach D-23 gilt eine Pruefung ohne Sonde als nicht vorhanden; hier war es ein ganzes
# Werkzeug. Der zweite Teil ist die Aenderung selbst: Sie entscheidet, ob ein Befund
# faellt, und eine solche Aenderung ohne Wirkungsnachweis waere genau die Bauform, gegen
# die dieses Repositorium gebaut ist.
#
# GEMESSEN am 2026-09-22 an zwei echten Belegen: `RE-001-P02` zog fuenf Abschnitte zu
# EINER Ueberschrift zusammen und wies den Inhalt als `<TBD: ausgesetzt, ...>` aus -
# drei Befunde fuer richtiges Verhalten. `RE-001-N04` schrieb `<TBD: Es wird keine
# Anforderung formuliert.>` und liess vier Abschnitte ganz weg.
#
#   Zwei Laeufe, zwei selbst erfundene Schreibweisen - genau deshalb konnte kein
#   Pruefmittel sie kennen. Die Vereinbarung ist die Abhilfe, nicht das Verzeihen.
def selbstprobe_ausgesetzt() -> None:
    """`ausgesetzte_ueberschriften()` an sechs gebauten Ausgaben."""
    import importlib.util
    pfad = os.path.join(QUELLE, ".koolie/core", "tests", "scripts",
                        "validate-output.py")
    spec = importlib.util.spec_from_file_location("_vo", pfad)
    vo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vo)

    faelle = [
        ("### Anforderungen (EARS)\n\n`<TBD: ausgesetzt, bis F1 beantwortet ist>`\n",
         {"anforderungen ears"}, "A1",
         "Eine Ueberschrift mit ausgewiesenem Aussetzen zaehlt als vorhanden"),
        ("### Anforderungen (EARS)\n\n1. Das System shall etwas tun.\n",
         set(), "A2",
         "Eine Ueberschrift mit Inhalt ist kein Aussetzen - sie braucht keines"),
        ("### Titel, Beschreibung und Anforderungen\n\n`<TBD: ausgesetzt, weil F1 "
         "offen ist>`\n",
         {"titel", "beschreibung", "anforderungen"}, "A3",
         "Eine zusammengezogene Ueberschrift deckt jedes ihrer Stuecke - an Komma "
         "und 'und' zerlegt (der Fall von RE-001-P02)"),
        ("### Anforderungen (EARS)\n\n`<TBD: Es wird keine Anforderung formuliert.>`\n",
         set(), "A4",
         "`<TBD: ...>` ohne das Wort 'ausgesetzt' zaehlt NICHT - die Schreibweise ist "
         "die Trennlinie (der Fall von RE-001-N04)"),
        ("### Anforderungen (EARS)\n\nInhalt.\n\n### Arbeitspakete\n\n"
         "`<TBD: ausgesetzt, weil F2 offen ist>`\n",
         {"arbeitspakete"}, "A5",
         "Das Aussetzen wird dem Abschnitt zugeordnet, unter dem es STEHT - nicht "
         "irgendwo in der Ausgabe gesucht"),
        ("`<TBD: ausgesetzt, weil alles offen ist>`\n\n### Anforderungen (EARS)\n\n"
         "Inhalt.\n",
         set(), "A6",
         "Ein Aussetzen VOR der ersten Ueberschrift deckt keinen Abschnitt"),
    ]
    for text, erwartet, nummer, satz in faelle:
        melde("SELBSTPROBE", nummer,
              vo.ausgesetzte_ueberschriften(text) == erwartet, satz)

    # \U0001f534 DER GEGENBEWEIS GEGEN DEN VORSTAND: Bis 0.83.0 gab es die Funktion
    # nicht, und der erste Fall haette einen Befund erzeugt. Belegt wird das hier
    # ueber den ganzen Pfad - Pflichtabschnitte gegen eine Ausgabe, die AUSSETZT.
    geruest = ("## 5. Ausgabeformat\n\n```markdown\n### Titel\n\n### Anforderungen "
               "(EARS)\n\n### Arbeitspakete\n```\n")
    noetig = vo.extract_required_headings(geruest)
    melde("SELBSTPROBE", "A7", noetig == ["titel", "anforderungen ears", "arbeitspakete"],
          "Die Pflichtabschnitte kommen aus dem Geruest der SKILL.md, normalisiert")


buendel(selbstprobe_ausgesetzt,
        "Das zweite Pruefmittel `validate-output.py` an sechs gebauten Ausgaben: "
        "ausgewiesenes Aussetzen zaehlt als vorhanden, stilles Weglassen bleibt ein "
        "Befund - der erste Wirkungsnachweis, den dieses Werkzeug ueberhaupt hat")


# --- Pruefung 81: eine Zeilenendeform je Repositorium (CR-2026-128, D-320) --------
#
# EIN BUENDEL, WEIL DIE PRUEFUNG EIN REPOSITORIUM BRAUCHT. Sie liest den Bestand ueber
# `git ls-files`, und kopie() schliesst `.git` aus - derselbe Griff wie bei Pruefung 75
# und 78, aus demselben Grund. Ohne `git init` naehme sie in jeder Sonde ihren dritten
# Ausgang und saehe dabei aus wie eine, die nichts gefunden hat.
#
# SIEBEN EINHEITEN, UND 81b IST DER GEMESSENE FALL:
#   81a (Gegenprobe) - der ausgelieferte Bestand laeuft durch, und die Pruefung ist dabei
#                      nachweislich gelaufen (keine Unmessbarkeitsmeldung).
#   81a (Sonde)      - ein Traeger DURCHGEHEND auf der anderen Form wird gemeldet.
#   81b (Sonde)      - EINE eingeschleppte Zeile der anderen Form wird gemeldet. Das ist
#                      der Fall vom 2026-09-23: 28 LF-Zeilen in einem CRLF-Bestand, von
#                      keiner der 80 Pruefungen gesehen, gefunden von einem Suchtext, der
#                      danach nicht mehr traf.
#   81c (Sonde)      - ohne Git-Bestand meldet sie die Unmessbarkeit, statt leise zu
#                      bestehen (D-23). Sie ist die einzige, die OHNE `git init` laeuft.
#   81e (Sonde)      - 🆕 seit 1.4.2 (D-352): derselbe Fall wie 81b, in einer Datei mit
#                      Umlaut im Namen. Ohne `-z` quotet git den Pfad, die Pruefung fand
#                      unter dem gequoteten Namen keine Datei und ging LEISE weiter -
#                      gegen den Vorstand faellt diese Sonde.
#   81d (Sonde)      - 🆕 seit 1.4.1 (D-351): Eine Datei der WURZEL, ausserhalb des
#                      Kerns, auf der anderen Form wird im Quellrepositorium gemeldet.
#                      Das belegt den Anker: Bis 1.4.0 war er UEBERGABE.md, und seit
#                      die nicht mehr versioniert ist, haette die Pruefung die Wurzel
#                      LEISE uebergangen - gegen den Vorstand faellt diese Sonde.
#   81b (Gegenprobe) - dieselbe Datei OHNE Kennzeichen, also in einem uebernehmenden
#                      Projekt: nicht gemeldet. Was ein Projekt in seine eigenen
#                      Dateien schreibt, geht das Framework nichts an.
#
# 🔴 KEINE SONDE HAELT EINE FORM WOERTLICH. Sie lesen die vorgefundene Form aus dem
# Traeger und stellen ihn auf die jeweils andere - dieselbe Lehre wie bei Pruefung 78:
# Eine Sonde, die einen Wert mitpflegen muss, faellt bei der naechsten Aenderung aus, und
# zwar als scheinbarer Befund. Auf einem Linux-Arbeitsplatz liegt der Bestand auf LF, und
# diese Sonden messen dort dasselbe.
M81_GEMISCHT = "mischt CRLF- und LF-Zeilen"
M81_ABWEICHEND = "Zeilenenden, während"
M81_UNMESSBAR = "Prüfung 81: kein Git-Bestand lesbar"

P81_OPFER = ".koolie/core/docs/RUNTIME_GLOSSARY.md"
P81_WURZEL = "README.md"
P81_KENNZEICHEN = ".koolie/QUELLREPOSITORIUM.md"
# Der Name traegt ein Nicht-ASCII-Zeichen, damit git ihn ohne `-z` quotet (D-352).
P81_UMLAUT = ".koolie/core/docs/Übersicht-sonde-81e.md"


def _81_umstellen(text: str) -> str:
    """Den Traeger durchgehend auf die jeweils ANDERE Form stellen."""
    ohne = text.replace("\r\n", "\n")
    return ohne if "\r\n" in text else ohne.replace("\n", "\r\n")


def _81_eine_zeile(text: str) -> str:
    """Genau EINE Zeile auf die andere Form - der Fall der eingeschleppten Zeile."""
    if "\r\n" in text:
        return text.replace("\r\n", "\n", 1)
    return text.replace("\n", "\r\n", 1)


def sonden_zeilenendeform() -> None:
    """Wirkungsnachweis zu Pruefung 81 an einem echten Repositorium."""
    root = kopie()
    try:
        pfad = P(root, *P81_OPFER.split("/"))
        urtext = lies(pfad)

        # --- Sonde 81c: ohne Git-Bestand ist sie nicht messbar, und sagt es -----------
        aus = validator_ausgabe(root)
        melde("SONDE", "81c", M81_UNMESSBAR in aus,
              "Ohne Git-Bestand meldet Pruefung 81 die Unmessbarkeit, statt leise zu "
              "bestehen - ein fehlender Gegenstand ist kein Messergebnis")
        if M81_UNMESSBAR not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "81" in z)[:400])

        if unterprozess(["git", "init", "-q", root]).returncode != 0:
            melde("BUENDEL", "-", False, "sonden_zeilenendeform  [git nicht erreichbar]")
            notiz("        Ohne git liest Pruefung 81 keinen Bestand; sie nimmt dann "
                  "ihren dritten Ausgang und ist nicht messbar.")
            return
        unterprozess(["git", "-C", root, "add", "-A"])

        # --- Gegenprobe 81a: der ausgelieferte Bestand laeuft durch ------------------
        aus = validator_ausgabe(root)
        ok = (M81_GEMISCHT not in aus and M81_ABWEICHEND not in aus
              and M81_UNMESSBAR not in aus)
        melde("GEGENPROBE", "81a", ok,
              "Der ausgelieferte Bestand laeuft durch - alle versionierten Texttraeger "
              "tragen dieselbe Form, und die Pruefung ist dabei nachweislich gelaufen")
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "81" in z or "Zeilenende" in z)[:400])

        # --- Sonde 81a: ein Traeger durchgehend auf der anderen Form -----------------
        schreib(pfad, _81_umstellen(urtext))
        aus = validator_ausgabe(root)
        melde("SONDE", "81a", M81_ABWEICHEND in aus,
              "Ein Traeger durchgehend auf der anderen Zeilenendeform wird gemeldet - "
              "die Pruefung nennt die Mehrheit und verlangt keine bestimmte Form")
        if M81_ABWEICHEND not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])

        # --- Sonde 81b: EINE eingeschleppte Zeile ------------------------------------
        schreib(pfad, _81_eine_zeile(urtext))
        aus = validator_ausgabe(root)
        melde("SONDE", "81b", M81_GEMISCHT in aus,
              "Eine einzige eingeschleppte Zeile der anderen Form wird gemeldet - genau "
              "der Fall, den ein Suchtext fand und keine der achtzig Pruefungen")
        if M81_GEMISCHT not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
        schreib(pfad, urtext)

        # --- Sonde 81e: derselbe Fall unter einem Namen mit Umlaut (D-352) -----------
        upfad = P(root, *P81_UMLAUT.split("/"))
        schreib(upfad, _81_eine_zeile(urtext))
        unterprozess(["git", "-C", root, "add", "-A"])
        aus = validator_ausgabe(root)
        treffer = P81_UMLAUT + ": mischt" in aus
        melde("SONDE", "81e", treffer,
              "Ein Traeger mit Umlaut im Dateinamen und einer eingeschleppten Zeile wird "
              "gemeldet - git quotet solche Pfade ohne -z")
        if not treffer:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
        os.remove(upfad)
        unterprozess(["git", "-C", root, "add", "-A"])

        # --- Sonde 81d: eine Wurzeldatei auf der anderen Form (D-351) -----------------
        wpfad = P(root, *P81_WURZEL.split("/"))
        wurtext = lies(wpfad)
        schreib(wpfad, _81_umstellen(wurtext))
        aus = validator_ausgabe(root)
        treffer = P81_WURZEL + ": trägt" in aus and M81_ABWEICHEND in aus
        melde("SONDE", "81d", treffer,
              "Eine Wurzeldatei ausserhalb des Kerns auf der anderen Form wird im "
              "Quellrepositorium gemeldet - das Kennzeichen macht den Zaehlbereich")
        if not treffer:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])

        # --- Gegenprobe 81b: dieselbe Datei in einem uebernehmenden Projekt ----------
        kpfad = P(root, *P81_KENNZEICHEN.split("/"))
        os.remove(kpfad)
        unterprozess(["git", "-C", root, "add", "-A"])
        aus = validator_ausgabe(root)
        ok = not (P81_WURZEL + ": trägt" in aus)
        melde("GEGENPROBE", "81b", ok,
              "Ohne Kennzeichen des Quellrepositoriums bleibt dieselbe Wurzeldatei "
              "unbeanstandet - sie gehoert dem uebernehmenden Projekt")
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if P81_WURZEL in z)[:400])
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_zeilenendeform,
        "Pruefung 81 haelt die Zeilenendeform des Arbeitsbaums zusammen, an einem "
        "echten Repositorium und ohne eine Form woertlich zu kennen")


# --- Pruefung 82: die Bestandsliste steht auf dem Stand des Releases (CR-2026-130) -
#
# FUENF EINHEITEN, UND DIE ZWEITE GEGENPROBE IST DIE, DIE MAN WEGLASSEN WUERDE.
#   82a (Gegenprobe) - der ausgelieferte Bestand laeuft durch, und die Pruefung ist
#                      dabei nachweislich gelaufen (keine Unmessbarkeitsmeldung).
#   82b (Gegenprobe) - 🔴 DIE D-299-PROBE. Ein uebernehmendes Projekt liegt Releases
#                      zurueck: VERSION und Bestandsliste tragen BEIDE denselben
#                      aelteren Stand, weil beide byte-gleich aus demselben Release
#                      ausgeliefert sind. Die Pruefung muss dort GRUEN sein - ohne
#                      Ausnahmemenge, ohne Sonderfall. Ohne diese Gegenprobe waere die
#                      Installationsfestigkeit eine Behauptung im Kopfkommentar statt
#                      eine gemessene Eigenschaft. Sie ist genau die Bauform, die
#                      0.90.0 zweimal gekostet hat (D-326).
#   82a (Sonde)      - eine Zeile auf einen anderen Stand gestellt wird gemeldet, und
#                      die Meldung nennt das Projekt. Das ist der gemessene Fall aus
#                      1.0.0 und 1.0.1.
#   82b (Sonde)      - die Spaltenueberschrift entfernt: der verlorene Anker wird als
#                      Fehler gemeldet, statt leise zu bestehen (D-23).
#   82c (Sonde)      - eine Tabelle ohne Datenzeile meldet eine Warnung und KEIN
#                      Messergebnis.
#
# KEINE EINHEIT HAELT EINE VERSIONSNUMMER WOERTLICH. Sie lesen den Stand aus VERSION
# und rechnen daran - dieselbe Lehre wie bei Pruefung 78 und 81: Eine Sonde, die einen
# Wert mitpflegen muss, faellt beim naechsten Release aus, und zwar als scheinbarer
# Befund.
M82_ABWEICHEND = "steht auf Framework-Version"
M82_ANKER = "keine Tabelle mit der Spalte"
M82_LEER = "Prüfung 82 hat nichts gemessen"
M82_FEHLT = "als Nachweis der Auditierbarkeit"

P82_LISTE = ".koolie/core/governance/ADOPTION_REGISTRY.md"
P82_VERSION = ".koolie/core/VERSION"
P82_KENNZEICHEN = ".koolie/QUELLREPOSITORIUM.md"


def _82_stand(root: str) -> str:
    return lies(P(root, *P82_VERSION.split("/"))).strip()


def _82_anderer(stand: str) -> str:
    """Ein Stand, der dem echten sicher nicht gleicht - ohne eine Nummer zu kennen."""
    teile = stand.split(".")
    try:
        teile[-1] = str(int(teile[-1]) + 7)
    except (ValueError, IndexError):
        return stand + "-abweichend"
    return ".".join(teile)


def sonden_bestandsliste_stand() -> None:
    """Wirkungsnachweis zu Pruefung 82."""
    root = kopie()
    try:
        pfad = P(root, *P82_LISTE.split("/"))
        urtext = lies(pfad)
        stand = _82_stand(root)
        fremd = _82_anderer(stand)

        # --- Gegenprobe 82a: der ausgelieferte Bestand laeuft durch ------------------
        aus = validator_ausgabe(root)
        ok = (M82_ABWEICHEND not in aus and M82_ANKER not in aus
              and M82_LEER not in aus and M82_FEHLT not in aus)
        melde("GEGENPROBE", "82a", ok,
              "Die Bestandsliste des Releases laeuft durch - jede Zeile nennt den "
              "Stand aus VERSION, und die Pruefung ist dabei nachweislich gelaufen")
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "82" in z or "Bestandsliste" in z)[:400])

        # --- Gegenprobe 82b: DIE D-299-PROBE ----------------------------------------
        # Ein uebernehmendes Projekt: kein Kennzeichen des Quellrepositoriums (D-351),
        # und Liste wie VERSION tragen denselben AELTEREN Stand. Beide kommen
        # byte-gleich aus demselben Release.
        kennzeichen = P(root, *P82_KENNZEICHEN.split("/"))
        gesichert = lies(kennzeichen) if os.path.isfile(kennzeichen) else None
        if gesichert is not None:
            os.remove(kennzeichen)
        schreib(P(root, *P82_VERSION.split("/")), fremd + "\n")
        schreib(pfad, urtext.replace("**" + stand + "**", "**" + fremd + "**"))
        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "82b", M82_ABWEICHEND not in aus,
              "Ein uebernehmendes Projekt, das Releases zurueckliegt, laeuft durch - "
              "Liste und VERSION kommen byte-gleich aus demselben Release (D-299)")
        if M82_ABWEICHEND in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if M82_ABWEICHEND in z)[:400])
        schreib(P(root, *P82_VERSION.split("/")), stand + "\n")
        if gesichert is not None:
            schreib(kennzeichen, gesichert)
        schreib(pfad, urtext)

        # --- Sonde 82a: eine Zeile auf einem anderen Stand ---------------------------
        vorher = baumhash(root)
        gestellt = urtext.replace("**" + stand + "**", "**" + fremd + "**", 1)
        if gestellt == urtext:
            raise Praeparationsfehler(
                "Sonde 82a: keine Bestandszeile mit `**%s**` in %s - die Sonde hat "
                "ihren Gegenstand verloren" % (stand, P82_LISTE))
        schreib(pfad, gestellt)
        if baumhash(root) == vorher:
            raise Praeparationsfehler("Sonde 82a hat nichts geschrieben")
        aus = validator_ausgabe(root)
        melde("SONDE", "82a", M82_ABWEICHEND in aus,
              "Eine Bestandszeile auf einem anderen Stand wird gemeldet, und die "
              "Meldung nennt das Projekt - der Fall aus 1.0.0 und 1.0.1")
        if M82_ABWEICHEND not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])

        # --- Sonde 82b: der verlorene Anker ------------------------------------------
        schreib(pfad, urtext.replace("Framework-Version", "Kernstand"))
        aus = validator_ausgabe(root)
        melde("SONDE", "82b", M82_ANKER in aus,
              "Geht die Spaltenueberschrift verloren, meldet die Pruefung es - eine "
              "Konsistenzpruefung ohne Anker bestuende sonst leise (D-23)")
        if M82_ANKER not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])

        # --- Sonde 82c: eine Tabelle ohne Datenzeile ---------------------------------
        ohne = "\n".join(z for z in urtext.split("\n")
                         if not z.startswith("| `devpacks/"))
        if ohne == urtext:
            raise Praeparationsfehler(
                "Sonde 82c: keine Bestandszeile erkannt - die Sonde hat ihren "
                "Gegenstand verloren")
        schreib(pfad, ohne)
        aus = validator_ausgabe(root)
        melde("SONDE", "82c", M82_LEER in aus,
              "Eine Tabelle ohne Datenzeile meldet eine Warnung und KEIN Messergebnis "
              "- eine Null ohne Ergebniszeile ist kein Messwert")
        if M82_LEER not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "82" in z)[:400])
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_bestandsliste_stand,
        "Pruefung 82 haelt die Bestandsliste gegen VERSION und ist in einem "
        "uebernehmenden Projekt gruen, ohne eine Versionsnummer zu kennen")



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


def sonden_formatgebunden() -> None:
    """Wirkungsnachweis zu Pruefung 87."""
    root = kopie()
    try:
        ppfad = P(root, ".koolie/core", "clients", P86_PACK, "CLIENT_PACK.md")
        ptext = lies(ppfad)
        nummern = sorted(re.findall(r"^ *(\d+): ", lies(
            P(root, *VALIDATOR.split("/"))).split("FORMATGEBUNDENE_PRUEFUNGEN = {")[1]
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
            laenge = len(lies(wurzel))
            aus = validator_ausgabe(root)
            ergebnisse[pack] = (laenge, M4_GRENZE not in aus and M4_BUDGET not in aus)
            if pack == "claude-code":
                schreib(wurzel, lies(wurzel) + "\r\n" + "x" * (12001 - laenge) + "\r\n")
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
P95_SKILL = ".koolie/core/framework/skills/fw-docs-update"


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
        ok = any(M95 in z and "fw-docs-update" in z for z in aus.splitlines())
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
        ok = any(M95 in z and "fw-docs-update" in z for z in aus.splitlines())
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


if LISTE:
    for e in EINHEITEN:
        print("%-11s %-6s %s" % (e.art, e.kennung, e.satz))
    print("---")
    print("%d Einheiten. Auswahl mit --nur <Kennung>[,<Kennung>...]" % len(EINHEITEN))
    sys.exit(0)

_GEWAEHLT = waehle(EINHEITEN, NUR)
_TEILLAUF = len(_GEWAEHLT) != len(EINHEITEN)
if _TEILLAUF:
    print("=" * 78)
    print("TEILLAUF: %d von %d Einheiten (--nur %s)"
          % (len(_GEWAEHLT), len(EINHEITEN), ",".join(NUR)))
    print("Das ist KEIN Abnahmelauf. Vor dem Merge laeuft der volle Apparat, und zwar")
    print("in beiden Kodierungsumgebungen (D-23, D-49, D-191).")
    print("=" * 78)
    print()

_beginn = time.perf_counter()
fehler = fahren(_GEWAEHLT, BAHNEN)
_wanduhr = time.perf_counter() - _beginn

print()
if _TEILLAUF:
    print("Ergebnis (TEILLAUF, %d von %d Einheiten): %s"
          % (len(_GEWAEHLT), len(EINHEITEN),
             "alle gewaehlten Einheiten bestanden" if not fehler
             else "%d Abweichung(en)" % fehler))
else:
    print("Ergebnis:", "alle Sonden und Gegenproben bestanden" if not fehler
          else f"{fehler} Abweichung(en)")
auswertung(_GEWAEHLT, _wanduhr, BAHNEN)
if _TEILLAUF:
    print("TEILLAUF - der Nachweis nach D-23 steht erst nach dem vollen Lauf.")
sys.exit(1 if fehler else 0)
