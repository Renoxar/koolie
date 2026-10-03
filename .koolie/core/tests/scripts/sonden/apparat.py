"""Der Apparat des Sondenlaufs: Befehlszeile, Kopien, Einheiten und ihre Anmeldung,
Praeparationswaechter, Aufraeumer, nebenlaeufige Bahnen und Auswertung.

Teil des Sondenskripts probe-pruefungen.py, seit 1.19.1 in Module geteilt (K-174). Die
Einheiten melden sich beim Laden dieses Moduls an; der Einstieg laedt die Module in der
Reihenfolge ihrer Nummer, und das ist die Reihenfolge der Ausgabe (D-49). Ein Modul
liest nur aus dem Apparat und aus frueheren Teilen."""
from __future__ import annotations

import hashlib
import io
import os
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
    kodierung = kw.pop("kodierung", "utf-8")
    umgebung = dict(kw.pop("env", None) or os.environ, PYTHONIOENCODING=kodierung)
    return subprocess.run(argv, capture_output=True, text=True, encoding=kodierung,
                          errors="replace", env=umgebung, **kw)


def lauf(root: str) -> str:
    p = unterprozess([sys.executable, os.path.join(root, *VALIDATOR.split("/")),
                      "--root", root])
    return (p.stdout or "") + (p.stderr or "")


# --- Zeilenenden: die Sonden sprechen CRLF, der Baum darf beides tragen (K-216) ------
#
# Die Suchtexte der Sonden sind unter Windows entstanden und tragen `\r\n` fest - rund
# 210 Stellen. Auf einem LF-Arbeitsbaum traf keiner davon: gemessen am 2026-10-03 in
# WSL, 101 Abweichungen.
#
# Statt jede Stelle umzuschreiben, uebersetzen lies() und schreib() an der Grenze: Im
# Speicher ist der Text immer CRLF, auf der Platte traegt er die Form des Baums. Auf
# einem CRLF-Baum reichen beide die Bytes unveraendert durch - der Lauf unter Windows
# ist bytegleich zu dem vor dieser Aenderung.
#
# GRENZE, benannt: Auf einem LF-Baum ist ein einzelnes CR vor dem Zeilenende nicht von
# einem CRLF zu unterscheiden; schreib() macht aus "\r\r\n" ein "\r\n". Eine Sonde,
# die genau das braucht, schreibt ihre Bytes selbst.


def _zeilenende(quelle: str) -> str:
    """Die Form des Baums, gelesen an diesem Modul in der Quelle - es liegt in jedem
    Koolie-Baum und wird mit ihm ausgecheckt."""
    pfad = os.path.join(quelle, ".koolie", "core", "tests", "scripts", "sonden",
                        "apparat.py")
    try:
        with open(pfad, "rb") as fh:
            return "\r\n" if b"\r\n" in fh.read() else "\n"
    except OSError:
        return "\r\n"


ZEILENENDE = _zeilenende(QUELLE)


def lies(pfad: str) -> str:
    text = io.open(pfad, encoding="utf-8", newline="").read()
    if ZEILENENDE == "\n":
        text = text.replace("\r\n", "\n").replace("\n", "\r\n")
    return text


def schreib(pfad: str, text: str) -> None:
    if ZEILENENDE == "\n":
        text = text.replace("\r\n", "\n")
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
        self.ausgelassen = 0
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


def nur_unter_windows(art: str, nummer: str, was: str, anmelden) -> None:
    """Eine Einheit, die nur unter Windows misst - anderswo AUSGELASSEN, nicht bestanden.

    `anmelden` ist der Aufruf, der sie unter Windows anmeldet. Anderswo steht an ihrer
    Stelle eine Zeile mit AUSG, und die Ergebniszeile zaehlt sie mit: Ein Lauf, der eine
    Sonde nicht faehrt, darf nicht aussehen wie einer, in dem sie bestanden hat (D-23).
    """
    if os.name == "nt":
        anmelden()
        return

    def arbeit() -> None:
        einheit = _ORT.einheit
        einheit.ausgelassen += 1
        einheit.zeilen.append(f"{art:10s} {nummer:4s} AUSG  {was}  [nur unter Windows messbar]")

    eintragen(art, nummer, was, arbeit)


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


def fehlerfrei(ausgabe: str) -> bool:
    """Endet der Validatorlauf ohne Fehler? Gelesen an der Ergebniszeile.

    Bis 1.21.0 stand hier `"0 Fehler" in ausgabe` - das trifft auch "10 Fehler" und
    "20 Fehler". Gemessen am 2026-09-30: Die Gegenprobe zu Pruefung 112 bestand an einem
    Baum mit zehn offenen Fehlern (D-522). Sonde 112f haelt die Unterscheidung fest."""
    return "Ergebnis: 0 Fehler," in ausgabe


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
            ok = verboten not in ausgabe and fehlerfrei(ausgabe)
            melde("GEGENPROBE", nummer, ok, was)
            if not ok:
                notiz("        Ausgabe:", " | ".join(ausgabe.splitlines()[:6]))
        finally:
            aufraeumen(os.path.dirname(root))

    eintragen("GEGENPROBE", nummer, was, arbeit)


P = lambda root, *teile: os.path.join(root, *teile)


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


def _p(root, rel):
    return P(root, rel.replace("/", os.sep))


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
