#!/usr/bin/env python3
"""Wirkungsnachweis nach D-23 fuer die Pruefungen 6 und 18 bis 46, dazu fuer
install.py (Clientwahl, Aktivierungspruefung, --list-skills, Schutz vorhandener
Projektdateien bei der Erstinstallation) und fuer den Praeparationswaechter dieses
Skripts selbst.

Die Aufzaehlung der Pruefungen steht hier in der Schreibweise, die Pruefung 40 aus den
Sondenkennungen dieses Skripts ausrechnet und woertlich vergleicht (D-86). Bis 0.41.0
stand an dieser Stelle eine Release-Chronik, die bei 0.29.0 endete: ein Register, das
mit jedem Release falscher wurde, ohne dass ein Lauf davon Notiz nahm. Welches Release
welche Sonde gebracht hat, steht im Aenderungsverlauf und nicht mehr hier.

Aufruf (im Wurzelverzeichnis des Repositoriums):
    python3 leitwerk-core/tests/scripts/probe-pruefungen.py [PFAD] [--bahnen N]

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
    while rest:
        wort = rest.pop(0)
        if wort == "--bahnen":
            if not rest or not rest[0].isdigit() or int(rest[0]) < 1:
                sys.exit("--bahnen erwartet eine Zahl ab 1")
            bahnen = int(rest.pop(0))
        elif wort.startswith("--"):
            sys.exit("Unbekannter Schalter: %s (bekannt ist nur --bahnen N)" % wort)
        else:
            pfad = wort
    return os.path.abspath(pfad), bahnen


QUELLE, BAHNEN = argumente(sys.argv[1:])
VALIDATOR = "leitwerk-core/tests/scripts/validate-framework.py"


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
    """
    text = lies(pfad)
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
        for zeile in self.zeilen:
            print(zeile)


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

# --- 18: verwaister Hook-Dateiname in einer root-template-Vorlage -----------------
sonde("18b", "Verwaiste Hook-Datei als geliefertes Artefakt in der Vorlage",
      lambda r: schreib(
          P(r, "leitwerk-core/clients/devin-desktop/root-template/.devin/README.md".replace("/", os.sep)),
          lies(P(r, "leitwerk-core/clients/devin-desktop/root-template/.devin/README.md".replace("/", os.sep)))
          .replace("| `config.json` |", "| `hooks.v1.json` | Lebenszyklus-Hooks | `[DOK]` |\r\n| `config.json` |", 1)),
      "hooks.v1.json")

gegenprobe("18b", "Erklaerende Nennung im Fliesstext bleibt unbeanstandet", None, "FEHLER")

# --- 19: Auskunftsabschnitt ------------------------------------------------------
def _entferne_abschnitt(root: str) -> None:
    pfad = P(root, "leitwerk-core/clients/devin-desktop/CLIENT_PACK.md".replace("/", os.sep))
    text = lies(pfad)
    start = text.index("## 7. Anweisungs- und Konfigurationsquellen")
    ende = text.index("## 8. Änderungsverlauf")
    schreib(pfad, text[:start] + text[ende:])


sonde("19", "Ein Pack ohne den Abschnitt ueber Anweisungs- und Konfigurationsquellen "
     "ausserhalb des Projekts wird gemeldet", _entferne_abschnitt,
      "Anweisungs- und Konfigurationsquellen außerhalb des Projekts' fehlt")


def _datum_entfernen(root: str) -> None:
    pfad = P(root, "leitwerk-core/clients/claude-code/CLIENT_PACK.md".replace("/", os.sep))
    text = lies(pfad)
    start = text.index("## 8. Anweisungs- und Konfigurationsquellen")
    ende = text.index("## 9. Änderungsverlauf")
    mitte = re.sub(r"\d{4}-\d{2}-\d{2}", "neulich", text[start:ende])
    schreib(pfad, text[:start] + mitte + text[ende:])


sonde("19", "Eine Auskunft ohne Erhebungsdatum ist eine Behauptung ohne Stand und wird gemeldet", _datum_entfernen, "nennt keinen Erhebungsstand")
gegenprobe("19", "Vorlage mit <TBD>-Erhebungsstand laeuft durch", None, "Erhebungsstand")

# --- 20: Dokumenttabellen gegen Manifest -----------------------------------------
sonde("20", "Verfaelschter Wert in der Registrierungstabelle",
      lambda r: schreib(P(r, "leitwerk-core/docs/PLACEHOLDER_REGISTRY.md".replace("/", os.sep)),
                        lies(P(r, "leitwerk-core/docs/PLACEHOLDER_REGISTRY.md".replace("/", os.sep)))
                        .replace("| `<SKILLS_DIR>` | Skill-Ablage | `.devin/skills`",
                                 "| `<SKILLS_DIR>` | Skill-Ablage | `.devin/faehigkeiten`", 1)),
      "<SKILLS_DIR> steht fuer 'devin-desktop'")

sonde("20", "Ein verfaelschter Pfad im Laufzeitglossar weicht vom Manifest des Packs ab und "
      "wird gemeldet",
      lambda r: schreib(P(r, "leitwerk-core/docs/RUNTIME_GLOSSARY.md".replace("/", os.sep)),
                        lies(P(r, "leitwerk-core/docs/RUNTIME_GLOSSARY.md".replace("/", os.sep)))
                        .replace("| **Agentenprofile** | Verzeichnis der Subagentenprofile | `.devin/agents/`",
                                 "| **Agentenprofile** | Verzeichnis der Subagentenprofile | `.devin/profile/`", 1)),
      "'Agentenprofile' steht fuer 'devin-desktop'")

gegenprobe("20", "Begriff ohne Manifestfeld und eingebettete Hook-Datei bleiben unbeanstandet",
           None, "das Manifest fuehrt")

# --- 21: Hook-Skripte neutral ----------------------------------------------------
sonde("21", "Eine clientgebundene Umgebungsvariable im gemeinsamen Hook-Skript bindet es an "
      "ein Pack und wird gemeldet",
      lambda r: schreib(P(r, "leitwerk-core/tests/scripts/hook-overlay-status.py".replace("/", os.sep)),
                        lies(P(r, "leitwerk-core/tests/scripts/hook-overlay-status.py".replace("/", os.sep)))
                        .replace("root = argumente[0] if argumente else os.getcwd()",
                                 'root = argumente[0] if argumente else os.environ.get("DEVIN_PROJECT_DIR", os.getcwd())', 1)),
      "ist die Umgebungsvariable des Packs")

sonde("21", "Laufzeitpfad eines Packs in der Pfadbildung",
      lambda r: schreib(P(r, "leitwerk-core/tests/scripts/hook-overlay-status.py".replace("/", os.sep)),
                        lies(P(r, "leitwerk-core/tests/scripts/hook-overlay-status.py".replace("/", os.sep)))
                        .replace('candidates.append(os.path.join(root, "project-overlay", "OVERLAY.md"))',
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
      lambda r: schreib(P(r, "leitwerk-core/framework/runtime/root-instruction.md".replace("/", os.sep)),
                        lies(P(r, "leitwerk-core/framework/runtime/root-instruction.md".replace("/", os.sep)))
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
    basis = P(root, "leitwerk-core/clients/devin-desktop/root-template/.devin/rules".replace("/", os.sep))
    os.makedirs(basis, exist_ok=True)
    schreib(os.path.join(basis, "README.md"), "# Erklaerender Text\r\n")


sonde("24", "Erklaerender Text in der Vorlage der Regelablage", _fremddatei, "kein Regeltext")


def _echte_regel(root: str) -> None:
    basis = P(root, "leitwerk-core/clients/devin-desktop/root-template/.devin/rules".replace("/", os.sep))
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

B03_ZIEL = "leitwerk-core/docs/ROADMAP.md".replace("/", os.sep)
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
    liste = P(root, "project-overlay", "forbidden-terms.txt")
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


def sonde_hook_zusatzmuster() -> None:
    """Dieselbe Regel im ausgelieferten Hook - ohne Validatorlauf, weil keiner noetig ist.

    Ein ungueltiges Zusatzmuster wurde bis 0.26.0 mitsamt seinem Wert nach stderr
    geschrieben. Projektspezifische Pfadmuster tragen Projekt-, Kunden- und Hostnamen.
    """
    marker = "b03hookmarke.internal"
    umgebung = dict(os.environ, FW_HOOK_EXTRA_PATH_PATTERNS=marker + "/[")
    p = unterprozess(
        [sys.executable, os.path.join(QUELLE, "leitwerk-core", "tests", "scripts",
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
    pfad = P(root, "leitwerk-core/clients/claude-code/CLIENT_PACK.md".replace("/", os.sep))
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

        p = unterprozess([sys.executable, os.path.join(root, "leitwerk-core", "install.py"),
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
    unterprozess([sys.executable, os.path.join(QUELLE, "leitwerk-core", "install.py"),
                  "--client", pack, "--root", root])
    shutil.copytree(os.path.join(QUELLE, "leitwerk-core"),
                    os.path.join(root, "leitwerk-core"),
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
            man = json.loads(lies(os.path.join(QUELLE, "leitwerk-core", "clients", pack,
                                               "manifest.json")))
            regel = os.path.join(root, *man["pack_runtime_dir"].split("/"),
                                 "20-project-overlay.md")
            rechte = os.path.join(root, *man["permissions_file"].split("/"))
            overlay = os.path.join(root, "project-overlay", "OVERLAY.md")

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
            werkzeug = os.path.join(root, "leitwerk-core", "install.py")

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
    werkzeug = os.path.join(QUELLE, "leitwerk-core", "install.py")
    man = json.loads(lies(os.path.join(QUELLE, "leitwerk-core", "clients", "claude-code",
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


# --- Pruefung 26 und der Suchkanal (CR-2026-047, D-47) ----------------------------
#
# Zwei Gegenstaende in einem Block, weil sie dieselbe Entscheidung tragen: Der Suchkanal
# wird vom Schutz-Hook durchgesetzt (nicht von der Berechtigungsdatei), und ein Client
# ohne Suchwerkzeug darf das erklaeren, ohne dass daraus ein Schlupfloch wird.

def _manifest_pfad(root: str, pack: str) -> str:
    return os.path.join(root, "leitwerk-core", "clients", pack, "manifest.json")


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
    hook = os.path.join(QUELLE, "leitwerk-core", "tests", "scripts",
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
          hooklauf("Grep", {"pattern": "x", "path": "leitwerk-core/framework/core/"}) == 0,
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
        werkzeug = os.path.join(quelle, "leitwerk-core", "install.py")

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
VORLAGE_28 = "leitwerk-core/templates/project-overlay/OVERLAY.md"
REGEL_28 = "leitwerk-core/framework/runtime/rules/20-project-overlay.md"


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
        "Hinweis: `<RUNTIME_DIR>/`, `<ROOT_INSTRUCTION_FILE>` und `project-overlay/` "
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
KURZFORM_29 = "leitwerk-core/framework/runtime/root-instruction.md"
LANGFORM_29 = "leitwerk-core/framework/core/02-privacy.md"


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
EDGE_30 = "leitwerk-core/tests/EDGE_CASES.md"
KATALOG_30 = "leitwerk-core/tests/TEST_CATALOG.md"


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
        "niedrig | keine | `leitwerk-core/tests/EDGE_CASES.md` Abschnitt 1 (D-52) |")
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
                      os.path.join(root, "leitwerk-core", "tests", "scripts",
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
            man = json.loads(lies(os.path.join(QUELLE, "leitwerk-core", "clients", pack,
                                               "manifest.json")))
            regelablage = man["pack_runtime_dir"]
            regel = os.path.join(root, *regelablage.split("/"), "20-project-overlay.md")
            overlay = os.path.join(root, "project-overlay", "OVERLAY.md")
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
PACK_31 = "leitwerk-core/clients/claude-code/CLIENT_PACK.md"
UEBERSICHT_31 = "leitwerk-core/clients/README.md"


def _summe_verfaelschen(root: str) -> None:
    pfad = P(root, PACK_31.replace("/", os.sep))
    schreib(pfad, lies(pfad).replace("| `[TECHNISCH]` | 22 von 31 |",
                                     "| `[TECHNISCH]` | 23 von 31 |", 1))


def _gesamtzahl_verfaelschen(root: str) -> None:
    pfad = P(root, PACK_31.replace("/", os.sep))
    schreib(pfad, lies(pfad).replace("| 22 von 31 |", "| 22 von 32 |", 1))


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
    schreib(pfad, t[:ende] + "\r\n| Z9 | Sonde ohne Einstufung | - | - | - | - |" + t[ende:])


def _zeile_mit_summe(root: str) -> None:
    """Gegenprobe: eine zusaetzliche Zeile samt nachgezogenen Summen."""
    pfad = P(root, PACK_31.replace("/", os.sep))
    frei(pfad, "| Z9 |")
    zeile_nach(pfad, "| X2 |",
               "| Z9 | Sonde mit Einstufung | - | - | `[TECHNISCH]` | `[DOK]` |")
    ersetze(pfad,
            ("| `[TECHNISCH]` | 22 von 31 |", "| `[TECHNISCH]` | 23 von 32 |"),
            ("| 7 von 31 (", "| 7 von 32 ("),
            ("| **2 von 31** (", "| **2 von 32** ("),
            ("| 0 von 31 |", "| 0 von 32 |"))
    # Seit 0.36.0 rechnet Pruefung 31 dieselbe Zahl auch in der Uebersicht der Ablage nach
    # (D-71). Eine Gegenprobe, die nur das Pack nachzieht, faellt seither an der zweiten
    # Stelle - und genau das ist der Zweck der Erweiterung.
    u = P(root, UEBERSICHT_31.replace("/", os.sep))
    ersetze(u, ("| entwurf | 22 von 31 |", "| entwurf | 23 von 32 |"))


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
    schreib(pfad, lies(pfad).replace("| entwurf | 22 von 31 |",
                                     "| entwurf | 25 von 29 |", 1))


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
# Bei LEITWERK-CORE/VERSION decken die Aufloesung und re.I einander gegenseitig zu -
# faellt einer von beiden aus, bestuende die Pruefung, und die Sonde zeigte nichts.
# 32a und 32e treffen deshalb je einen Fall, den nur ein Mechanismus faengt.
HOOK_32 = "leitwerk-core/tests/scripts/hook-check-secrets.py"


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
        pfad = P(root, ("leitwerk-core/clients/%s/manifest.json" % pack).replace("/", os.sep))
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
    pfad = P(root, "leitwerk-core/tests/scripts/hook-check-secrets.py".replace("/", os.sep))
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
        inst = os.path.join(root, "leitwerk-core", "install.py")
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
# devin-desktop durch, obwohl es ehrlich ist - seine Zeile A1 traegt einen offenen
# VERIFY-Marker, und die Praeambel des Packs sagt, die Einstufung nenne die VORGESEHENE
# Tiefe. Die Einstufung allein sagt nicht, ob eine Zusage schon gilt.
MANIFEST_CC_34 = "leitwerk-core/clients/claude-code/manifest.json"
MANIFEST_DD_34 = "leitwerk-core/clients/devin-desktop/manifest.json"
PACK_DD_34 = "leitwerk-core/clients/devin-desktop/CLIENT_PACK.md"


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
    pfad = P(root, MANIFEST_DD_34.replace("/", os.sep))
    schreib(pfad, lies(pfad).replace('"_agent_start_tools_absent_note"',
                                     '"_agent_start_tools_absent_hinweis"', 1))


def _34_beides_zugleich(root: str) -> None:
    pfad = P(root, MANIFEST_CC_34.replace("/", os.sep))
    schreib(pfad, lies(pfad).replace(
        '"agent_start_tools": ["Agent", "Task"],',
        '"agent_start_tools": ["Agent", "Task"],\r\n'
        '  "agent_start_tools_absent": ["unerhoben"],\r\n'
        '  "_agent_start_tools_absent_note": "Sonde.",', 1))


def _34_a1_ohne_vorbehalt(root: str) -> None:
    """devin-desktop sagt A1 ohne VERIFY-Marker zu, kann das Werkzeug aber nicht nennen."""
    pfad = P(root, PACK_DD_34.replace("/", os.sep))
    t = lies(pfad)
    i = t.index("| A1 |")
    ende = t.index("\r\n", i)
    # Den Vorbehalt generisch entfernen, nicht woertlich: Pruefung 14 meldet jeden
    # Clientnamen, auch in einer Sonde - und der Marker traegt ihn.
    zeile = re.sub(r"<VERIFY[^>]*>", "(Sonde: Vorbehalt entfernt)", t[i:ende])
    schreib(pfad, t[:i] + zeile + t[ende:])


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
MANIFEST_CC_35 = "leitwerk-core/clients/claude-code/manifest.json"
PROFIL_35 = "leitwerk-core/framework/runtime/agents/fw-reviewer.md"


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
    shutil.rmtree(P(root, "leitwerk-core/framework/runtime/agents".replace("/", os.sep)))


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
DECISION_LOG_36 = "leitwerk-core/governance/DECISION_LOG.md"


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

        # --- 37g: der verlorene Anker ----------------------------------------------
        cm = os.path.join(root, "leitwerk-core", "clientmap.py")
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
        "Sieben Eingriffe in die Berechtigungsdatei einer echten Installation, jeder einzeln "
        "zurueckgesetzt: geloeschte, verengte und ergaenzte Regeln, geleerter ask-Korb, "
        "Praefixzeichen")

# --- 38: Eine Quelle, ein Vokabular, eine Richtung (CR-2026-062, D-78 bis D-80) ----
#
# Auf einer Kopie des Repositoriums, nicht gegen eine Installation: Der Gegenstand von
# Pruefung 38 sind die Manifeste und die Quellen des Kerns, nicht eine erzeugte Datei.
# Das ist der Unterschied zu den Pruefungen 33 und 37.
#
# Acht Sonden, zwei Gegenproben. Die Sonden 38f und 38g treffen die beiden Stellen, an
# denen der Fall bis 0.39.0 STILL war: in allowed-tools wurde das unbekannte Verb
# woertlich als Werkzeugname durchgereicht, in permissions.deny fiel es lautlos aus.
MANIFEST_CC_38 = "leitwerk-core/clients/claude-code/manifest.json"
MANIFEST_DD_38 = "leitwerk-core/clients/devin-desktop/manifest.json"
SKILL_38 = "leitwerk-core/framework/skills/fw-plan/SKILL.md"
CLIENTMAP_38 = "leitwerk-core/clientmap.py"


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
    for rel in ("leitwerk-core/framework/skills",
                "leitwerk-core/framework/role-packs",
                "leitwerk-core/framework/runtime/agents"):
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
PERMS_39 = "leitwerk-core/framework/runtime/permissions.json"


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
    ersetze(P(root, "leitwerk-core/framework/runtime/rules/00-framework-core.md"
              .replace("/", os.sep)),
            ("**Skillwahl vor dem Schritt.**", "**Hinweis zur Reihenfolge.**"))


def _39_skill_ohne_regel(root: str) -> None:
    """Ein neuer Skill im Verzeichnis, ohne dass jemand die Freigabe nachtraegt."""
    quelle = P(root, "leitwerk-core/framework/skills/fw-code-explain"
               .replace("/", os.sep))
    ziel = P(root, "leitwerk-core/framework/skills/fw-zwischenstand"
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
VAL_40 = "leitwerk-core/tests/scripts/validate-framework.py"
KAT_40 = "leitwerk-core/tests/TEST_CATALOG.md"

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
MAN_DD = "leitwerk-core/clients/devin-desktop/manifest.json"
MAN_CC = "leitwerk-core/clients/claude-code/manifest.json"

NOTE_DD_START = '"_agent_start_tools_absent_note": "UNERHOBEN, nicht abwesend'
NOTE_CC_FUND = ("tests/protocols/2026-09-13-erhebung-disallowed-tools.md "
                "Abschnitt 4.3")


def _41_behauptung(root: str) -> None:
    """Eine Abwesenheitserklaerung ohne Enthaltung und ohne Fundstelle - der Fall vom
    2026-09-14. Die Note traegt danach noch ein Datum, aber keinen Beleg."""
    ersetze(_p(root, MAN_DD),
            (NOTE_DD_START,
             '"_agent_start_tools_absent_note": "Dieser Client fuehrt kein Startwerkzeug'))


def _41_datum_ohne_fundstelle(root: str) -> None:
    """Ein Datum allein ist kein Beleg - die Fundstelle faellt weg."""
    ersetze(_p(root, MAN_CC), (NOTE_CC_FUND, "einer fruehreren Erhebung"))


def _41_gegenstand_weg(root: str) -> None:
    """Kein Pack fuehrt noch eine Abwesenheitserklaerung - die Pruefung meldet es selbst."""
    ersetze(_p(root, MAN_DD), ('  "agent_start_tools_absent": ["unerhoben"],\r\n', ""))
    ersetze(_p(root, MAN_CC), ('    "skill_deny_unmapped": "argumentmuster",\r\n', ""))


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
    return os.path.join(root, "project-overlay", "OVERLAY.md")


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
P44_REGISTER = "leitwerk-core/onboarding/exercises/README.md"
P44_KATALOG = "leitwerk-core/tests/TEST_CATALOG.md"
M44_UNREGISTRIERT = "das Register in"
M44_TOT = "die kein Testfall nennt"
M44_ANKER = "führt kein Register mehr"
# Jede Meldung der Pruefung 44 endet auf ihren Decision Record. Die generische
# gegenprobe() nimmt genau einen Suchtext - dieser faengt alle drei und jede kuenftige.
M44_JEDE = "(D-93)"

# Synthetische Kennungen. UEB-08 waere die naechste echte - deshalb nehmen die beiden
# Defektsonden 98 und 99, und nur die Gegenprobe, die einen ZULAESSIGEN Zustand
# herstellt, nimmt 08. Die Lehre von G-18 (2026-09-13): Eine synthetische Kennung, die
# mit einer echten kollidieren kann, misst nicht mehr ihren Fall.
P44_UNREG = "UEB-99"
P44_TOT = "UEB-98"
P44_NEU = "UEB-08"

P44_VORBEDINGUNG_ALT = "| FW-NE-01 (Basis) | Delegationsverbot | Übungsrepo |"
P44_REGISTERZEILE = ("| `%s` | **Synthetisch:** Eintrag der Gegenprobe | nirgends | "
                     "nichts | `FW-NE-01` |")


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

gegenprobe("44a", "Auslieferungszustand: sieben registrierte, sieben gebrauchte "
                  "Praeparationen", None, M44_JEDE)

gegenprobe("44b", "Eine achte Praeparation, registriert UND von einem Testfall "
                  "gebraucht - der zulaessige Weg",
           lambda root: (_44_register_zeile(root, P44_NEU),
                         _44_katalog_nennt(root, P44_NEU)),
           M44_JEDE)


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


def _45_repo(root: str) -> bool:
    """Aus dem Installationsverzeichnis ein Repositorium machen. False = kein git."""
    p = unterprozess(["git", "init", "-q", root])
    return p.returncode == 0


def _45_bytecodedatei(root: str) -> str:
    """Eine .pyc an den Ort legen, an dem der Kern seinen Bytecode erzeugt."""
    ablage = os.path.join(root, "leitwerk-core", "__pycache__")
    os.makedirs(ablage, exist_ok=True)
    pfad = os.path.join(ablage, "clientmap.cpython-314.pyc")
    io.open(pfad, "wb").write(b"\x00\x00\x00\x00Sondenbytecode")
    return "leitwerk-core/__pycache__/clientmap.cpython-314.pyc"


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
P46_ROADMAP = "leitwerk-core/docs/ROADMAP.md".replace("/", os.sep)
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
    pfad = P(root, "leitwerk-core/framework/core/03-security.md".replace("/", os.sep))
    schreib(pfad, lies(pfad) + "\r\n> Sondenzeile: Wirkung der Sandbox je "
                               "Betriebssystem " + P46_MARKER + ".\r\n")


def _46_testblatt_dazu(root: str) -> None:
    """Ein Testblatt an einem Ort, den eine Ablagenliste uebersaehe.

    Genau der Befund, der Pruefung 46 ausgeloest hat: Die alte Regel las "die dezentralen
    TESTS.md je Skill" als zwoelf Dateien, und die dreizehnte lag unter role-packs/.
    Diese Sonde legt eine vierzehnte unter tech-packs/ an - eine Ablagenliste, die die
    dreizehnte uebersah, uebersaehe sie ebenso.
    """
    ordner = P(root, "leitwerk-core/framework/tech-packs/_template".replace("/", os.sep))
    schreib(os.path.join(ordner, "TESTS.md"),
            "# Sondentestblatt\r\n\r\n"
            "| Test-ID | Ziel | Prüfmethode | Ergebnisstatus |\r\n"
            "|---|---|---|---|\r\n"
            "| SO-001 | Sondenfall | sitzung | offen |\r\n")


def _46_steckbrief_dazu(root: str) -> None:
    """Ein neues Modul auf `entwurf` - Kriterium 3 steigt um eins."""
    schreib(P(root, "leitwerk-core/prompts/13-sondenprompt.md".replace("/", os.sep)),
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
    pfad = P(root, "leitwerk-core/governance/DECISION_LOG.md".replace("/", os.sep))
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
    pfad = P(root, "leitwerk-core/governance/DECISION_LOG.md".replace("/", os.sep))
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
    ordner = P(root, "leitwerk-core/tests/protocols".replace("/", os.sep))
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
    kern = os.path.join(QUELLE, "leitwerk-core")
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


_beginn = time.perf_counter()
fehler = fahren(EINHEITEN, BAHNEN)
_wanduhr = time.perf_counter() - _beginn

print()
print("Ergebnis:", "alle Sonden und Gegenproben bestanden" if not fehler
      else f"{fehler} Abweichung(en)")
auswertung(EINHEITEN, _wanduhr, BAHNEN)
sys.exit(1 if fehler else 0)
