"""Das Project Overlay: aktiver Zustand, Aktivierungsreife, ausgeschlossene Pfade,
Schlitze, Freigabefolge, Pflichtplatzhalter, Platzhalterbindung, Vorbedingungen,
Befehlsschlitz, Wert- und Pfadabgleich.

Pruefungen 9, 9a, 28, 51, 52, 55a, 55b, 56, 57, 59, 60 und 89. Teil des Validators
validate-framework.py, seit 1.19.1 nach Gegenstand in Module geteilt (K-174). Das
Register aller Pruefungen steht im Kopfkommentar des Einstiegs, die Grenze jeder
einzelnen in ihrem Kopfkommentar hier."""
from __future__ import annotations

import json
import os
import re

from overlay_status import (
    AKTIV, auswerten, INAKTIV, status_angaben, UNBEKANNT, WIDERSPRUECHLICH)

from .gemeinsam import (
    _tabellenspalte, _ueb_katalogdateien, err, formatgebunden, KERN, PLACEHOLDER_RE,
    PROJEKTPLATZHALTER, read, regeldatei, tabellenzellen, TBD_RE)


# Abschnitte des Overlays, die ueber die Aktivierungsreife entscheiden. Sie muessen da
# sein und sie muessen ausgefuellt sein - das eine ohne das andere ist keine Pruefung.
SICHERHEITSABSCHNITTE = ("## 4.", "## 5.", "## 6.", "## 13.", "## 14.", "## 15.")


def check_strict_overlay(root: str, man: dict) -> None:
    """Der **aktive** Zustand des Projekts (--strict-overlay) - clientneutral.

    Diese Funktion hiess bis 0.32.0 im Docstring und im Uebernahmeleitfaden "Pruefung der
    Aktivierungsreife" und verlangte dabei den Status 'aktiv'. Das war der Kern von B08:
    Der Leitfaden fuhr sie in Schritt 7 und setzte 'aktiv' erst in Schritt 9, die
    Uebernahmecheckliste trug sie als MUSS und galt "vor dem Setzen auf aktiv" - eine
    Voraussetzung, die sich selbst verlangte. Die Reifepruefung heisst seit 0.33.0
    --check-overlay-ready und ist eine eigene Funktion (D-57). Diese hier prueft den
    fertigen Zustand und bleibt dafuer unveraendert; sie hat mit dem
    Aktualisierungsablauf einen zweiten, funktionierenden Aufrufer.

    Bis 0.27.0 las diese Funktion zwei fest verdrahtete Pfade **eines** Clients und bekam
    das erkannte Manifest nicht uebergeben. In einer Installation des anderen Packs fand
    sie nichts, uebersprang alles und meldete null zusaetzliche Fehler.

    Gemessen am 2026-09-12 an zwei frischen Installationen mit demselben Defekt: Beim
    einen Pack aenderte sich die Fehlerzahl, beim anderen nicht (B02, D-44). Die
    Clienterkennung steht seit der Umstellung auf mehrere Packs in derselben Datei; sie
    wurde hier nur nicht benutzt.

    Zwei Befunde derselben Funktion sind dabei mit erledigt, beide aus der Messung:

    * **Der Status wurde als Praefix geprueft.** Damit bestand 'aktivierung-ausstehend'
      die Aktivierungspruefung - ein Wert, der woertlich sagt, dass die Aktivierung
      aussteht, liess den Fehler verschwinden, der vorher stand. Wer ihn eintrug, machte
      die Pruefung stiller. Jetzt gilt genau 'aktiv'.
    * **Ein fehlender sicherheitsrelevanter Abschnitt wurde akzeptiert.** Die Pruefung
      suchte nur in vorhandenen Abschnitten nach offenen Werten; fehlte der Abschnitt,
      fand sie nichts. Ein Overlay ohne Abschnitt 13 stand damit besser da als eines mit
      einem offenen Wert darin - die Pruefung auf den Kopf gestellt.

    GRENZE: Geprueft wird die Aktivierungs**reife**, nicht die Aktivierung. Dass ein
    Overlay 'aktiv' sagt, heisst nicht, dass der Client seine Regeln laedt.
    """
    runtime = os.path.join(root, *man["pack_runtime_dir"].split("/"), regeldatei(man, "20-project-overlay.md"))
    overlay = os.path.join(root, ".koolie/project-overlay", "OVERLAY.md")
    for path in (runtime, overlay):
        if not os.path.exists(path):
            continue
        text = read(path)
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        angaben = status_angaben(text)
        status, grund = auswerten(angaben)
        if status != AKTIV:
            # Der **Rohwert** gehoert in die Meldung, nicht nur die Auswertung: Der Fall,
            # der D-44 ausgeloest hat, war der Wert 'aktivierung-ausstehend' - er sagt
            # woertlich, dass die Aktivierung aussteht, und genau das soll lesbar sein.
            # Die Sonde zu D-44 hat diesen Verlust beim Umbau auf overlay_status.py
            # gefangen; ohne sie waere die Meldung stiller geworden.
            roh = ", ".join("'%s'" % a.strip() for a in angaben) or "keine Angabe"
            err(f"{rel}: Overlay-Status ist nicht '{AKTIV}', sondern {roh} "
                f"(ausgewertet als '{status}': {grund}) (strict-overlay)")
        if path == runtime and TBD_RE.search(text):
            err(f"{rel}: enthält offene <TBD>-Werte (strict-overlay)")
        if path == overlay:
            for sec in SICHERHEITSABSCHNITTE:
                m = re.search(rf"{re.escape(sec)}.*?(?=\n## |\Z)", text, re.S)
                if not m:
                    err(f"{rel}: sicherheitsrelevanter Abschnitt {sec} fehlt (strict-overlay)")
                elif TBD_RE.search(m.group(0)):
                    err(f"{rel}: Abschnitt {sec} enthält offene <TBD>-Werte (sicherheitsrelevant, strict-overlay)")
    rechte = os.path.join(root, *man["permissions_file"].split("/"))
    if os.path.exists(rechte):
        inhalt = read(rechte)
        if TBD_RE.search(inhalt) or PLACEHOLDER_RE.search(inhalt):
            err(f"{man['permissions_file']}: enthält noch Platzhalter (strict-overlay)")


def check_overlay_ready(root: str, man: dict) -> None:
    """Aktivierungsreife eines Kandidaten (--check-overlay-ready) - clientneutral.

    Die Pruefung, die B08 gefehlt hat: Sie prueft alles, was --strict-overlay prueft,
    **ausser** dem Status - und beim Status erwartet sie das Gegenteil, naemlich einen
    Kandidaten, der noch nicht aktiv ist. Damit ist der dokumentierte Ablauf ohne
    Regelbruch begehbar: erst vollstaendig ausfuellen und pruefen, dann durch einen
    Menschen aktivieren, dann mit --strict-overlay nachpruefen (D-57).

    Warum sie einen aktiven Kandidaten als Fehler meldet und nicht durchlaesst: Sonst
    waere sie die schwaechere Variante von --strict-overlay und wuerde als deren Ersatz
    benutzt. Eine Pruefung, die zwei Zustaende gleich behandelt, unterscheidet keine zwei
    Zustaende.

    Die Statusangaben MUESSEN untereinander uebereinstimmen. Ein Kandidat, der in der
    Laufzeitfassung 'aktiv' und im Quell-Overlay 'inaktiv' erklaert, ist kein Kandidat,
    sondern eine Drift - derselbe Fall, den der Status-Hook bis 0.32.0 zugunsten der
    ersten gelesenen Datei entschied.

    GRENZE: Geprueft wird die Vollstaendigkeit der Konfiguration. Die **fachliche**
    Freigabe kann kein Skript erteilen; die Uebernahmecheckliste bleibt der Nachweis
    (FW-CL-10). Und dass ein Overlay vollstaendig ist, heisst nicht, dass seine Werte
    richtig sind.
    """
    runtime = os.path.join(root, *man["pack_runtime_dir"].split("/"), regeldatei(man, "20-project-overlay.md"))
    overlay = os.path.join(root, ".koolie/project-overlay", "OVERLAY.md")
    vorhanden = [p for p in (runtime, overlay) if os.path.exists(p)]
    if not vorhanden:
        err("check-overlay-ready: weder die Laufzeitfassung des Overlays noch "
            ".koolie/project-overlay/OVERLAY.md ist vorhanden - es gibt keinen Kandidaten")
        return

    alle_angaben = []
    for path in vorhanden:
        text = read(path)
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        angaben = status_angaben(text)
        alle_angaben.extend(angaben)
        if not angaben:
            err(f"{rel}: keine Angabe zum Overlay-Status gefunden (check-overlay-ready)")
        # Offene Werte: in der Laufzeitfassung ueberall, im Overlay in den
        # sicherheitsrelevanten Abschnitten. Dieselbe Aufteilung wie --strict-overlay;
        # ein Kandidat unterscheidet sich vom aktiven Overlay im Status, nicht im Inhalt.
        if path == runtime and TBD_RE.search(text):
            err(f"{rel}: enthält offene <TBD>-Werte (check-overlay-ready)")
        if path == overlay:
            for sec in SICHERHEITSABSCHNITTE:
                m = re.search(rf"{re.escape(sec)}.*?(?=\n## |\Z)", text, re.S)
                if not m:
                    err(f"{rel}: sicherheitsrelevanter Abschnitt {sec} fehlt "
                        f"(check-overlay-ready)")
                elif TBD_RE.search(m.group(0)):
                    err(f"{rel}: Abschnitt {sec} enthält offene <TBD>-Werte "
                        f"(sicherheitsrelevant, check-overlay-ready)")

    status, grund = auswerten(alle_angaben)
    if status == AKTIV:
        err(f"check-overlay-ready: Der Overlay-Status ist bereits '{AKTIV}'. Diese "
            f"Pruefung gilt fuer einen Kandidaten **vor** der Aktivierung; fuer den "
            f"aktiven Zustand ist --strict-overlay zustaendig (D-57)")
    elif status == WIDERSPRUECHLICH:
        err(f"check-overlay-ready: {grund}. Ein Kandidat erklaert seinen Status an allen "
            f"Stellen gleich; abweichende Angaben sind eine Drift, kein Kandidat")
    elif status == UNBEKANNT:
        err(f"check-overlay-ready: Overlay-Status nicht ausgefuellt ({grund}). Erwartet "
            f"wird '{INAKTIV}' - ein Kandidat sagt, dass er noch nicht aktiv ist, statt "
            f"die Angabe offen zu lassen")

    rechte = os.path.join(root, *man["permissions_file"].split("/"))
    if os.path.exists(rechte):
        inhalt = read(rechte)
        if TBD_RE.search(inhalt) or PLACEHOLDER_RE.search(inhalt):
            err(f"{man['permissions_file']}: enthält noch Platzhalter "
                f"(check-overlay-ready)")
    else:
        err(f"{man['permissions_file']}: fehlt - ohne Berechtigungsdatei ist kein "
            f"Kandidat vollstaendig (check-overlay-ready)")


# Pruefung 28: Ein Strukturpfad des Frameworks gehoert nicht in <EXCLUDED_PATHS>.
#
# Zwei Schutzziele, zwei Kategorien - der Schutz-Hook unterscheidet sie seit D-30 und die
# Berechtigungsdatei ebenfalls: <EXCLUDED_PATHS> wird dort zu einer 'read'- UND einer
# 'write'-Verweigerung, die Strukturpfade stehen ausschliesslich als 'write'-Verweigerung
# bei 'read allow **'. Die Overlay-Vorlage und die Laufzeitregel fuehrten sie bis 0.31.0
# unter "weder lesen noch aendern" - genau die Pfade, die der KI-Client als
# Anweisungsquelle laden soll (B07). Wer die Vorlage woertlich ausfuellt, erzeugt damit
# eine Lesesperre auf die eigenen Regeldateien. Diese Pruefung findet den Fall im
# Repositorium, also bevor eine Installation entsteht (D-55).
STRUKTURPFAD_MARKER = (
    "<RUNTIME_DIR>", "<ROOT_INSTRUCTION_FILE>", "<CORE_DIR>", "<RULES_DIR>",
    ".koolie/project-overlay/", "framework/", "AGENTS.md", "CLAUDE.md", ".devin/", ".claude/",
)

# Die Beschriftung der Deklarationszeile - in der Overlay-Vorlage eine Tabellenzeile, in
# der Laufzeitregel ein Listeneintrag. Beide beginnen mit derselben Bezeichnung.
DEKLARATION_RE = re.compile(r"^\s*(?:\|\s*|-\s+)Ausgeschlossene Pfade")


def _excluded_paths_traeger(root: str, man: dict) -> list[str]:
    """Dateien, die <EXCLUDED_PATHS> deklarieren - Quelle und Installation."""
    kandidaten = [
        os.path.join(KERN, "templates", "project-overlay", "OVERLAY.md"),
        os.path.join(KERN, "framework", "runtime", "rules", "20-project-overlay.md"),
        os.path.join(".koolie/project-overlay", "OVERLAY.md"),
    ]
    runtime_dir = (man or {}).get("runtime_dir")
    if runtime_dir:
        kandidaten.append(os.path.join(runtime_dir.replace("/", os.sep), "rules",
                                       regeldatei(man, "20-project-overlay.md")))
    treffer = []
    for rel in kandidaten:
        pfad = os.path.join(root, rel)
        if os.path.isfile(pfad) and pfad not in treffer:
            treffer.append(pfad)
    return treffer


def check_excluded_paths(root: str, man: dict) -> None:
    """Pruefung 28 (D-55): Ein Schreibschutz ist kein Leseverbot.

    Geprueft wird die **Deklarationszeile** von <EXCLUDED_PATHS>: Sie darf keinen
    Strukturpfad des Frameworks nennen. Der Nachweis ist eine Textpruefung - dass die
    Berechtigungsdatei die beiden Kategorien trennt, prueft Pruefung 2.

    Nur die Deklaration, nicht jede Nennung: Beide Traeger erklaeren im Fliesstext
    ausdruecklich, dass die Strukturpfade **nicht** hierher gehoeren, und diese Saetze
    nennen beides in einer Zeile. Eine Pruefung, die jede Nennung meldet, wuerde genau
    den richtigen Text beanstanden. Erkannt wird die Deklaration an ihrer Beschriftung
    (DEKLARATION_RE) - und weil eine verlorene Beschriftung eine Pruefung erzeugt, die
    leise besteht, ist auch ihr Fehlen ein Fehler (D-23).
    """
    for pfad in _excluded_paths_traeger(root, man):
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        zeilen = read(pfad).splitlines()
        deklarationen = [(i, z) for i, z in enumerate(zeilen, 1)
                         if "<EXCLUDED_PATHS>" in z and DEKLARATION_RE.match(z)]
        if not deklarationen and any("<EXCLUDED_PATHS>" in z for z in zeilen):
            err(f"{rel}: nennt <EXCLUDED_PATHS>, aber keine Zeile ist als Deklaration "
                f"erkennbar (Beschriftung 'Ausgeschlossene Pfade'). Pruefung 28 prueft "
                f"damit nichts und bestuende leise - die Beschriftung ist Teil des "
                f"Nachweises (D-23, D-55)")
        for i, zeile in deklarationen:
            gefunden = [m for m in STRUKTURPFAD_MARKER if m in zeile]
            if not gefunden:
                continue
            err(f"{rel}:{i}: Die Deklaration von <EXCLUDED_PATHS> nennt "
                f"{', '.join(gefunden)}. <EXCLUDED_PATHS> wird in der Berechtigungsdatei zu "
                f"einer 'read'- UND einer 'write'-Verweigerung; die Strukturpfade des "
                f"Frameworks sind integritaetsgeschuetzt, nicht vertraulich - sie gehoeren "
                f"in <READ_ONLY_PATHS>. Ein Projekt, das dieser Zeile folgt, sperrt den "
                f"Lesezugriff auf seine eigenen Regeldateien; der KI-Client kann die "
                f"Anweisungen dann nicht laden, die er befolgen soll (B07, D-55)")


# --- Pruefung 51 -------------------------------------------------------------------
# Eine Regel kann als SATZ oder als AUSFUELLSCHLITZ ausgedrueckt sein, und ein Sweep nach
# einer Marke findet nur den Satz. 0.33.0 hat die Domain-Ausnahme in sechzehn Traegern
# angefasst, davon acht anweisenden - darunter eine Datei im selben Verzeichnis; die
# Overlay-Laufzeitfassung war nicht darunter, weil dort kein Satz stand. Dreiunddreissig
# Releases lang bot die Overlay-Laufzeitfassung damit an, was ihre eigene Quelle
# ausdruecklich ausschliesst (D-150, Grenzfall G-13).
#
# ABGELEITET, NICHT GEPFLEGT: Die Feldmenge stammt aus der Kontextquellentabelle der
# Overlay-Vorlage. Traegt eine Zeile dort einen FESTEN Wert in der Freigabespalte - also
# keinen <TBD> -, dann ist der Wert entschieden, und die Laufzeitfassung darf fuer
# dasselbe Feld keinen Schlitz fuehren. Traegt die Quelle selbst einen Schlitz, bleibt er
# in beiden zulaessig; die Zeile der MCP-Server belegt das als Gegenprobe.
#
# WAS SIE NICHT LEISTET: Sie vergleicht Feldnamen, nicht Werte. Ob der eingetragene feste
# Wert derselbe ist, sieht sie nicht - das ist FW-KO-05 und laeuft als Durchsicht.
P51_QUELLE = KERN + "/templates/project-overlay/OVERLAY.md"
P51_LAUFZEIT = KERN + "/framework/runtime/rules/20-project-overlay.md"
P51_TABELLENKOPF = "| Kontextquelle | Kontextklasse | Freigabe | Bedingungen |"
P51_KLAMMER_RE = re.compile(r"\s*\([^)]*\)\s*$")


def _51_feldname(zelle: str) -> str:
    """Der blosse Feldname einer Zeile - ohne Fettmarkierung und ohne Klammerzusatz.

    'Freigegebene externe Domains (Fetch)' und 'Freigegebene externe Domains' sind
    dasselbe Feld; die Klammer sagt, ueber welches Werkzeug es wirkt.
    """
    name = zelle.replace("**", "").strip()
    return P51_KLAMMER_RE.sub("", name).strip()


def check_overlay_schlitze(root: str) -> None:
    """Pruefung 51 (D-150): Kein Schlitz fuer einen Wert, den die Overlay-Vorlage festlegt."""
    qpfad = os.path.join(root, P51_QUELLE.replace("/", os.sep))
    lpfad = os.path.join(root, P51_LAUFZEIT.replace("/", os.sep))
    if not os.path.isfile(qpfad) or not os.path.isfile(lpfad):
        err(f"{P51_QUELLE} oder {P51_LAUFZEIT} fehlt – Prüfung 51 hat ihren Gegenstand "
            f"verloren; sie bestünde sonst leise (D-23)")
        return
    quelle = read(qpfad).replace("\r\n", "\n")
    if P51_TABELLENKOPF not in quelle:
        err(f"{P51_QUELLE}: die Kontextquellentabelle mit dem Kopf "
            f"'{P51_TABELLENKOPF}' ist nicht mehr auffindbar. Prüfung 51 leitet ihre "
            f"Feldmenge daraus ab und hätte ohne sie nichts zu prüfen (D-23)")
        return
    rest = quelle.split(P51_TABELLENKOPF, 1)[1]
    festgelegt = []
    for zeile in rest.split("\n")[1:]:
        if not zeile.startswith("|"):
            break
        zellen = tabellenzellen(zeile)
        if len(zellen) < 3:
            continue
        if TBD_RE.search(zellen[2]):
            continue
        festgelegt.append((_51_feldname(zellen[0]), zellen[2].replace("**", "").strip()))
    if not festgelegt:
        err(f"{P51_QUELLE}: keine Zeile der Kontextquellentabelle trägt einen festen "
            f"Freigabewert. Prüfung 51 hätte damit keinen Gegenstand mehr (D-23)")
        return
    laufzeit = read(lpfad).replace("\r\n", "\n")
    for name, wert in festgelegt:
        for zeile in laufzeit.split("\n"):
            roh = zeile.lstrip("-* ").strip()
            if not roh.startswith(name + ":"):
                continue
            if TBD_RE.search(roh):
                err(f"{P51_LAUFZEIT}: Das Feld '{name}' trägt einen Ausfüllschlitz, "
                    f"obwohl {P51_QUELLE} seinen Wert auf '{wert}' festlegt. Eine Regel "
                    f"kann als Satz oder als Schlitz ausgedrückt sein – ein Sweep nach "
                    f"der Formulierung findet nur den Satz, und die Laufzeitfassung ist "
                    f"die, die in jede Sitzung lädt (D-150, Grenzfall G-13)")


# --- Pruefung 52 -------------------------------------------------------------------
# Eine Kurzfassung, die den einschraenkenden Halbsatz der Langform weglaesst, kehrt ihre
# Aussage um. Die Wurzel-Anweisungsdatei trennt seit D-53 zwei Saetze: Anwendungslogik mit
# Sicherheitsbezug ist Kontrollstufe hoch und nach Freigabe umsetzbar - tatsaechliche
# Berechtigungen und Betriebs-, Infrastruktur- und Sicherheitskonfigurationen sind V6 und
# auch nach Freigabe nicht delegierbar. Zwei Fassungen fuehrten beides in EINER
# Aufzaehlung, deren Rechtsfolge die Freigabe war, und stellten damit ein
# Delegationsverbot auf die freigebbare Seite - sechzig Releases lang (D-151,
# Grenzfaelle G-05 und G-06).
#
# ABGELEITET: Die Begriffe stammen aus der V6-Zeile der Delegationsverbotsliste. Die
# Schreibvarianten stehen daneben, wie bei Pruefung 29 - das Projekt fuehrt
# 'Sicherheitskonfiguration' und 'Security-Konfiguration' synonym, und eine Pruefung, die
# nur eine Schreibweise kennt, findet die Haelfte.
#
# AUSGENOMMEN ist die Langform, aus der die Begriffe stammen: Dort steht die Abgrenzung
# zu V6, und sie MUSS beide Seiten in einem Absatz nennen. Die Ausnahme ist abgeleitet -
# es ist die Datei, aus der gelesen wurde, nicht ein gepflegter Name.
#
# WAS SIE NICHT LEISTET: Sie liest Woerter, keine Bedeutung. Ein Text, der dieselbe
# Aussage ohne diese Begriffe trifft, entgeht ihr - dieselbe Grenze wie bei Pruefung 29.
P52_RISIKO = KERN + "/framework/core/09-risk-model.md"
P52_V6_RE = re.compile(r"^\|\s*V6\s*\|([^|]*)\|", re.M)
# Schreibvarianten je Begriff der V6-Zeile. Links der Wortstamm, wie er dort steht.
P52_VARIANTEN = {
    "Produktionssystem": r"Produktionssystem",
    "Infrastruktur": r"Infrastruktur",
    "Berechtigung": r"Berechtigung",
    "Sicherheitskonfiguration": r"Sicherheitskonfiguration|Security-Konfiguration",
}
P52_STUFE_RE = re.compile(r"Kontrollstufe\s+\*{0,2}hoch")
P52_FOLGE_RE = re.compile(r"Umsetzung[^.;]{0,120}Freigabe")
P52_EINZELN_RE = re.compile(r"^\s*(?:[-*+]\s|\d+\.\s|\|)")


def _52_v6_begriffe(root: str) -> list:
    """Die Begriffe der V6-Zeile, auf ihren Stamm gebracht - abgeleitet, nicht gepflegt."""
    pfad = os.path.join(root, P52_RISIKO.replace("/", os.sep))
    if not os.path.isfile(pfad):
        return []
    m = P52_V6_RE.search(read(pfad).replace("\r\n", "\n"))
    if not m:
        return []
    treffer = []
    for stamm, muster in P52_VARIANTEN.items():
        if re.search(stamm, m.group(1)):
            treffer.append((stamm, re.compile(muster)))
    return treffer


def _52_einheiten(text: str):
    """Liefert die Pruefeinheiten: Listenpunkte und Tabellenzeilen einzeln, Prosa als Absatz.

    Die Einheit muss die des Lesers sein. Wer einen Listenpunkt liest, liest ihn allein;
    wer einen Absatz liest, liest ihn ganz. Eine Pruefung ueber die ganze Datei fände in
    jeder normativen Datei beides und meldete ueberall.
    """
    absatz = []
    for zeile in text.replace("\r\n", "\n").split("\n"):
        if not zeile.strip() or P52_EINZELN_RE.match(zeile):
            if absatz:
                yield "\n".join(absatz)
                absatz = []
            if zeile.strip():
                yield zeile
            continue
        absatz.append(zeile)
    if absatz:
        yield "\n".join(absatz)


def check_v6_freigabefolge(root: str) -> None:
    """Pruefung 52 (D-151): Kein V6-Gegenstand in einer Aufzaehlung mit Freigabefolge."""
    begriffe = _52_v6_begriffe(root)
    if not begriffe:
        err(f"{P52_RISIKO}: die Zeile 'V6' der Delegationsverbotsliste ist nicht mehr "
            f"auffindbar oder nennt keinen der bekannten Begriffe. Prüfung 52 leitet "
            f"ihren Gegenstand daraus ab und hätte ohne sie nichts zu prüfen (D-23)")
        return
    ausgenommen = os.path.join(root, P52_RISIKO.replace("/", os.sep))
    for pfad in _normative_traeger(root):
        if os.path.abspath(pfad) == os.path.abspath(ausgenommen):
            continue
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        for einheit in _52_einheiten(read(pfad)):
            if not P52_STUFE_RE.search(einheit) or not P52_FOLGE_RE.search(einheit):
                continue
            for stamm, muster in begriffe:
                if muster.search(einheit):
                    err(f"{rel}: '{stamm}' steht in einer Aufzählung, deren Rechtsfolge "
                        f"eine Freigabe ist ('…{P52_FOLGE_RE.search(einheit).group(0)[:60]}…'). "
                        f"V6 ist auch nach Freigabe nicht delegierbar; die Abgrenzung "
                        f"trennt Anwendungslogik von Betrieb (D-53, D-151, Grenzfälle "
                        f"G-05 und G-06)")
                    break


def _normative_traeger(root: str):
    """Die anweisenden Fassungen: Wurzel-Anweisungsdatei, Regelablage, Langform,
    Overlay-Vorlage, Skills und Checklisten - die sechs, die FW-KO-05 gegeneinander hält."""
    pfade = []
    p = os.path.join(root, KERN, "framework", "runtime", "root-instruction.md")
    if os.path.isfile(p):
        pfade.append(p)
    for teil in (("framework", "runtime", "rules"), ("framework", "core"),
                 ("checklists",), ("templates", "project-overlay")):
        verz = os.path.join(root, KERN, *teil)
        if not os.path.isdir(verz):
            continue
        for name in sorted(os.listdir(verz)):
            if name.endswith(".md"):
                pfade.append(os.path.join(verz, name))
    skills = os.path.join(root, KERN, "framework", "skills")
    if os.path.isdir(skills):
        for name in sorted(os.listdir(skills)):
            p = os.path.join(skills, name, "SKILL.md")
            if os.path.isfile(p):
                pfade.append(p)
    return pfade


# --- Pruefung 55 und 56 --------------------------------------------------------------
# ANLASS: der Durchgang durch die Vorbedingungen der dreizehn Testblaetter (2026-09-18).
# Er hat zwei Dinge gefunden, die nichts gemeldet hat.
#
# ERSTENS: Ein Overlay darf einen Platzhalter durch seinen WERT ERSETZEN statt ihn zu
# BINDEN. Fuer das Overlay selbst ist das folgenlos - es nennt ja den Wert. Fuer jeden
# KERNTEXT, der denselben Platzhalter traegt, ist es das nicht: Im Uebungsrepositorium
# standen 65 Fundstellen von fuenf Pflichtplatzhaltern in der geladenen Laufzeitschicht,
# die kein Leser aufloesen konnte - <ISSUE_TRACKER> allein in vierzehn Traegern.
# Der Validator meldete 0 Fehler, 0 Warnungen.
#
# ZWEITENS: Eine Vorbedingung darf einen Traeger verlangen, den dasselbe Overlay sperrt.
# SK-012-P01 verlangt die Merge-Request-Vorlage; ihr Pfad liegt unter .github/**, und das
# steht im Uebungs-Overlay unter <EXCLUDED_PATHS>. Die Zelle war damit nie fahrbar.
#
# WAS 55 NICHT LEISTET: (b) prueft, ob der Platzhalter GENANNT wird, nicht ob der Wert
# daneben richtig ist. Eine Bindung an den falschen Wert laeuft durch.
# WAS 56 NICHT LEISTET: Sie loest ueber die Bindungszeile auf. Eine Vorbedingung, die
# einen ausgeschlossenen Pfad WOERTLICH nennt statt ueber einen Platzhalter, entgeht ihr.
P55_REGISTER = KERN + "/docs/PLACEHOLDER_REGISTRY.md"
P55_VORLAGE = KERN + "/templates/project-overlay/OVERLAY.md"
P55_LAUFZEIT = (KERN + "/framework/runtime/rules", KERN + "/framework/skills")
P55_ZEILE_RE = re.compile(r"^\|\s*`<([A-Z][A-Z0-9_]*)>`\s*\|")


def _p55_pflicht(root: str) -> list:
    """(Name, Ort) je Platzhalter mit 'Pflicht vor Aktivierung' = ja - abgeleitet."""
    pfad = os.path.join(root, P55_REGISTER.replace("/", os.sep))
    if not os.path.isfile(pfad):
        err(f"{P55_REGISTER} fehlt - Prüfung 55 hat ihren Gegenstand verloren; sie "
            f"bestünde sonst leise (D-23)")
        return []
    raus = []
    for zeile in read(pfad).replace("\r\n", "\n").split("\n"):
        z = zeile.strip()
        treffer = P55_ZEILE_RE.match(z)
        if not treffer:
            continue
        zellen = tabellenzellen(z)
        if len(zellen) > 4 and zellen[4].startswith("ja"):
            raus.append((treffer.group(1), zellen[2]))
    if not raus:
        err(f"{P55_REGISTER}: keine Zeile trägt 'Pflicht vor Aktivierung' = ja. Prüfung "
            f"55 leitet ihre Menge von dort ab und hätte damit nichts zu prüfen (D-23)")
    return raus


def check_pflichtplatzhalter(root: str) -> None:
    """Pruefung 55a: Die Overlay-Vorlage bietet jeden Pflichtplatzhalter an."""
    pfad = os.path.join(root, P55_VORLAGE.replace("/", os.sep))
    if not os.path.isfile(pfad):
        return
    vorlage = read(pfad)
    for name, ort in _p55_pflicht(root):
        if not ort.lower().startswith("overlay"):
            continue  # anderswo gesetzt - die Vorlage muss ihn nicht anbieten
        if name not in vorlage:
            err(f"{P55_VORLAGE}: Der Platzhalter <{name}> ist im Register als 'Pflicht "
                f"vor Aktivierung' geführt und dort in '{ort}' verortet, kommt in der "
                f"Vorlage aber nicht vor. Ein Projekt, das die Vorlage ausfüllt, "
                f"begegnet ihm nie (D-160)")


def check_platzhalterbindung(root: str, man: dict) -> None:
    """Pruefung 55b (--strict-overlay): Das aktive Overlay BINDET, statt zu ersetzen.

    🔴 SIE PRUEFT SEIT 0.84.0 DIE BINDUNG UND NICHT MEHR DIE NENNUNG (K-88, D-257).
    Bis 0.83.0 fragte sie `if name in text`, also die BUCHSTABEN des Platzhalternamens
    irgendwo im Overlay - und meldete am Uebungsrepositorium NULL, waehrend 14 von 26
    Pflichtplatzhaltern dort nirgends mit spitzen Klammern standen. Ihr eigener
    Meldungstext sagte dabei "ist im Overlay aber nirgends gebunden".

      Eine Bindung, die eine Teilzeichenkette ist, sagt nichts ueber einen Wert.

    🔴 Und die Gegenprobe deckte es mit: `BINDUNGEN` in `probe-pruefungen.py` schrieb
    `ISSUE_TRACKER` ohne Klammern und nannte das eine Bindung. Zwei Stellen, die
    einander decken - derselbe Befundtyp wie bei `LINK_ROOTS` und `OPTIONAL_RUNTIME_RE`
    (0.57.0). Die Sonde `55d` misst jetzt genau den Unterschied.
    """
    overlay = os.path.join(root, ".koolie/project-overlay", "OVERLAY.md")
    if not os.path.isfile(overlay):
        return
    text = read(overlay)
    genannt = {}
    for basis in P55_LAUFZEIT:
        wurzel = os.path.join(root, basis.replace("/", os.sep))
        if not os.path.isdir(wurzel):
            continue
        for ordner, _, dateien in os.walk(wurzel):
            for n in sorted(dateien):
                if not n.endswith(".md"):
                    continue
                p = os.path.join(ordner, n)
                inhalt = read(p)
                rel = os.path.relpath(p, root).replace(os.sep, "/")
                for name, _ in _p55_pflicht(root):
                    if f"<{name}>" in inhalt:
                        genannt.setdefault(name, []).append(rel)
    for name, traeger in sorted(genannt.items()):
        # Der Name IN SPITZEN KLAMMERN - die Schreibweise, die den Kerntext aufloest.
        # Ein blosses Vorkommen der Buchstaben ist eine Nennung, keine Bindung (D-257).
        if f"<{name}>" in text:
            continue
        err(f".koolie/project-overlay/OVERLAY.md: Der Pflichtplatzhalter <{name}> wird von "
            f"{len(traeger)} Träger(n) der geladenen Schicht genannt (z. B. "
            f"{traeger[0]}), ist im Overlay aber nirgends gebunden. Ein Overlay, das den "
            f"Platzhalter durch seinen Wert ersetzt statt ihn zu binden, lässt jeden "
            f"Kerntext unauflösbar, der ihn trägt (D-160)")


P56_KATALOG = KERN + "/tests/TEST_CATALOG.md"


def _p56_ausgeschlossen(text: str) -> list:
    """Die Globs aus der <EXCLUDED_PATHS>-Zeile des aktiven Overlays."""
    for zeile in text.replace("\r\n", "\n").split("\n"):
        if "<EXCLUDED_PATHS>" not in zeile:
            continue
        zellen = tabellenzellen(zeile.strip())
        for zelle in zellen:
            if "<EXCLUDED_PATHS>" in zelle:
                continue
            treffer = re.findall(r"`([^`]+)`", zelle)
            if treffer:
                return treffer
    return []


def _p56_deckt(glob: str, pfad: str) -> bool:
    """Deckt das Glob-Muster den Pfad? Segmentweise, nicht nach Pfadanfang.

    DER ERSTE ENTWURF VERGLICH NUR DAS ERSTE SEGMENT, und das hat in EINEM Release
    zweimal falsch gemeldet: erst bei drei Zellen, die <EXCLUDED_PATHS> selbst zum
    Gegenstand haben, dann bei `.github/pull_request_template.md` gegen
    `.github/workflows/**` - derselbe Anfang, verschiedene Pfade. Eine Pruefung, die
    Pfadanfaenge vergleicht, meldet jede Nachbardatei mit.
    """
    muster = re.escape(glob).replace(r"\*\*", "\x00").replace(r"\*", "[^/]*")
    muster = muster.replace("\x00", ".*")
    return re.fullmatch(muster, pfad) is not None


def _p56_bindung(text: str, name: str) -> str:
    """Der Wert, den die Bindungszeile des Platzhalters traegt - in BEIDEN Schreibweisen.

    🔴 GEFUNDEN DURCH DIE ABHILFE ZU K-88, AM SELBEN TAG (D-261). Pruefung 55b
    verlangt seit 0.84.0 den Platzhalternamen IN SPITZEN KLAMMERN; diese Funktion suchte
    ihn OHNE - `f"`{name}`"`. Nach der Bindung der vierzehn Platzhalter im
    Uebungs-Overlay haette Pruefung 56 ihre Zeilen nicht mehr gefunden und waere leise
    gruen geblieben; Sonde 56a ist genau daran gefallen.

      Zwei Pruefungen, die dieselbe Zeile lesen, muessen sie gleich lesen - oder jede
      fuer ihren eigenen Gegenstand, und das ausdruecklich.

    Hier gilt das Zweite: **55b prueft die SCHREIBWEISE der Bindung, 56 den WERT
    daneben.** Fuer den Wert ist gleichgueltig, wie der Name geschrieben steht - und ein
    Overlay aus dem Bestand traegt ihn weiter ohne Klammern. Die Funktion nimmt deshalb
    beide Formen; eine Pruefung, die einen Wert nicht mehr findet, meldet keinen Fehler,
    sondern schweigt - und das ist die Bauform "die Null durch Konstruktion".

    **Dieselbe Bauform wie D-248 und D-243:** Die Meldung entsteht durch die Abhilfe,
    und zwei Pruefungen standen gegeneinander.
    """
    offen = None
    for zeile in text.replace("\r\n", "\n").split("\n"):
        z = zeile.strip()
        if not z.startswith("|"):
            continue
        if f"`<{name}>`" not in z and f"`{name}`" not in z:
            continue
        zellen = tabellenzellen(z)
        wert = " ".join(zellen[1:])
        # \U0001f534 EINE ZEILE MIT `<TBD...>` BINDET NICHTS (D-261, zweiter Teil). Die
        # Overlay-VORLAGE traegt zu jedem Pflichtplatzhalter eine Zeile mit offenem
        # Wert; wer sie stehen laesst und den Wert weiter unten bindet, wurde bis
        # 0.83.0 mit dem `<TBD>` der Vorlage gemessen - und die Pruefung schwieg.
        # Aufgefallen ist es erst, als 55b die spitzen Klammern verlangte und diese
        # Funktion dieselbe Schreibweise lesen musste: Die Enge der einen Stelle hat
        # verhindert, dass die zweite auffaellt (die Bauform von 0.57.0).
        if re.search(r"<TBD[:>]", wert):
            offen = offen or wert
            continue
        return wert
    # Keine gebundene Zeile - der offene Wert ist die ehrlichere Auskunft als "".
    return offen or ""


def check_ausgeschlossene_vorbedingung(root: str, man: dict) -> None:
    """Pruefung 56 (--strict-overlay): Keine Vorbedingung verlangt einen gesperrten Traeger."""
    overlay = os.path.join(root, ".koolie/project-overlay", "OVERLAY.md")
    if not os.path.isfile(overlay):
        return
    otext = read(overlay)
    globs = _p56_ausgeschlossen(otext)
    if not globs:
        err(f".koolie/project-overlay/OVERLAY.md: Die Zeile zu <EXCLUDED_PATHS> führt keine "
            f"Pfade in Backticks. Prüfung 56 leitet ihre Menge von dort ab und hätte "
            f"damit nichts zu prüfen (D-23)")
        return
    dateien = [os.path.join(root, P56_KATALOG.replace("/", os.sep))]
    for ordner, _, namen in os.walk(os.path.join(root, KERN.replace("/", os.sep),
                                                 "framework")):
        for n in sorted(namen):
            if n == "TESTS.md":
                dateien.append(os.path.join(ordner, n))
    for pfad in dateien:
        if not os.path.isfile(pfad):
            continue
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        for zeile in read(pfad).replace("\r\n", "\n").split("\n"):
            z = zeile.strip()
            if not z.startswith("| ") or z.startswith("|---"):
                continue
            zellen = tabellenzellen(z)
            if len(zellen) < 4:
                continue
            vorbed = zellen[2]
            for name in re.findall(r"<([A-Z][A-Z0-9_]*)>", vorbed):
                # DER ZUSCHNITT, UND ER IST BEIM ERSTEN LAUF NOETIG GEWORDEN: Eine Zelle,
                # die <EXCLUDED_PATHS> SELBST nennt, hat die Sperre zum Gegenstand - sie
                # prueft, ob der Client sie achtet. Ohne diese Ausnahme meldete die
                # Pruefung am 2026-09-18 drei solche Zellen (SK-001-N01, SK-010-N02,
                # SK-012-N03) als nicht fahrbar, und alle drei sind es. Eine Pruefung,
                # die ihren eigenen Gegenstand beanstandet, behauptet mehr als ihr Fall
                # hergibt.
                if name == "EXCLUDED_PATHS":
                    continue
                wert = _p56_bindung(otext, name)
                if not wert:
                    continue
                for pfadangabe in re.findall(r"`([^`]+)`", wert):
                    for g in globs:
                        if _p56_deckt(g, pfadangabe):
                            err(f"{rel}: Die Vorbedingung von '{zellen[0]}' verlangt "
                                f"<{name}>; der Wert '{pfadangabe}' liegt unter "
                                f"'{g}', das dasselbe Overlay unter <EXCLUDED_PATHS> "
                                f"führt - weder lesen noch ändern. Die Zelle ist damit "
                                f"nicht fahrbar (D-161)")
                            break


# --- Pruefung 57: kein ungebundener Pflichtplatzhalter als Vorbedingung -------------
#
# DIE KEHRSEITE VON 55b. Pruefung 55b meldet ein aktives Overlay, das einen
# Pflichtplatzhalter nicht bindet. Eine Testzelle, die genau diesen Zustand als
# Vorbedingung verlangt, ist damit nur in einem Baum fahrbar, den der Validator
# beanstandet - eine Pruefung und ein Testfall desselben Repositoriums stehen
# gegeneinander, und keiner von beiden sagt es.
#
# WARUM TEILSAETZE UND NICHT ZELLEN. Eine Vorbedingung nennt haeufig mehrere Zustaende
# in einer Zelle. Wer die ganze Zelle nach einer Verneinung durchsucht, meldet jede
# Zelle mit, die irgendwo ein "ohne" traegt - die Bauform, an der Pruefung 56 beim
# ersten Lauf zweimal zu breit gemeldet hat. Getrennt wird an Semikolon und Punkt.
#
# WAS SIE NICHT LEISTET. Sie erkennt die AUFGEZAEHLTEN Wendungen, nicht jede moegliche.
# "Ein Overlay, in dem der Platzhalter fehlt" entgeht ihr - dieselbe Grenze, die
# Pruefung 29 bei Bedingungswoertern hat. Die Aufzaehlung steht hier und nirgends sonst.
P57_VERNEINUNG = (
    "ohne gesetzt",
    "ohne gebunden",
    "ohne belegt",
    "nicht gesetzt",
    "nicht gebunden",
    "nicht belegt",
    "ungebunden",
)


def _p57_teilsaetze(text: str) -> list:
    """Die Vorbedingung in Teilsaetze zerlegen - Semikolon und Punkt trennen."""
    return [t.strip() for t in re.split(r"[;.]", text) if t.strip()]


def check_ungebundene_vorbedingung(root: str) -> None:
    """Pruefung 57: Keine Vorbedingung verlangt einen ungebundenen Pflichtplatzhalter."""
    pflicht = {name for name, _ in _p55_pflicht(root)}
    if not pflicht:
        return  # _p55_pflicht hat den verlorenen Gegenstand bereits gemeldet
    for rel in _ueb_katalogdateien(root):
        pfad = os.path.join(root, *rel.split(os.sep))
        if not os.path.isfile(pfad):
            continue
        anzeige = rel.replace(os.sep, "/")
        for zeile in read(pfad).replace("\r\n", "\n").split("\n"):
            z = zeile.strip()
            if not z.startswith("| ") or z.startswith("|---"):
                continue
            zellen = tabellenzellen(z)
            if len(zellen) < 4:
                continue
            for teil in _p57_teilsaetze(zellen[2]):
                namen = [n for n in re.findall(r"<([A-Z][A-Z0-9_]*)>", teil)
                         if n in pflicht]
                if not namen:
                    continue
                klein = teil.lower()
                marke = next((m for m in P57_VERNEINUNG if m in klein), None)
                if marke is None:
                    continue
                err(f"{anzeige}: Die Vorbedingung von '{zellen[0]}' verlangt "
                    f"<{namen[0]}> als nicht gesetzt ('{marke}'). Der Platzhalter ist "
                    f"im Register 'Pflicht vor Aktivierung', und Pruefung 55b meldet "
                    f"genau diesen Zustand im aktiven Overlay als Fehler - die Zelle "
                    f"waere nur in einem Baum fahrbar, den der Validator beanstandet. "
                    f"Gemeint ist in aller Regel ein gebundener Platzhalter OHNE Wert, "
                    f"also ein Ausfuellschlitz (D-166)")
                break

# --- Pruefung 60: Der Befehlsschlitz, den der Ausloeser braucht ---------------------
#
# ANLASS. Gemessen am 2026-09-18 im fuenften Sitzungstest (CR-2026-091). `FW-SC-01`
# ist zum dritten Mal gefahren worden und zum dritten Mal nicht abnehmbar gewesen -
# diesmal aus einem neuen Grund: Der Lauf hat NICHTS geaendert. `fw-change-small`
# verlangt in Schritt 4, den Testbefehl VOR dem ersten Schreibzugriff auszufuehren;
# im Messbaum stand `<TEST_COMMAND>` im `ask`-Korb, und `ask` ist im
# nicht-interaktiven Betrieb eine Abweisung (D-134). Der Lauf hat angehalten und
# gefragt - regelkonform. Gemessen war der Korb, nicht die Scope-Treue.
#
#     Der Schreibzuschnitt deckt das SCHREIBEN, nicht das AUSFUEHREN.
#
# Derselbe Fehler hat im selben Release `FW-PO-02` einen Durchgang gekostet, und er
# wiederholt sich bei jeder Wiederholung, weil die Zelle ihn nicht nennt. `FW-SC-02`
# ist mit 0.59.0 abgenommen worden, weil sein Messbaum den Befehl freigab - seine
# Zelle sagt es nicht, und wer sie ohne dieses Wissen wiederholt, faellt hinein.
#
# GEGENSTAND. Eine `sitzung`-Zelle, deren Ausloeser einen Skill als `/name` aufruft,
# dessen Frontmatter einen Befehlsschlitz AUSFUEHRT (`Exec(<..._COMMAND>)` unter
# `permissions`), muss diesen Schlitz in ihrer VORBEDINGUNG nennen.
#
# WARUM DAS FRONTMATTER UND NICHT DER FLIESSTEXT. `fw-plan` nennt `<TEST_COMMAND>`
# in seinen Vorbedingungen und in seiner Teststrategie - es fuehrt den Befehl aber
# nicht aus, sondern plant ihn. Ein Zuschnitt ueber den Fliesstext haette `FW-FI-02`
# mitgemeldet, dessen Lauf am 2026-09-18 keinen einzigen Befehl gebraucht hat. Das
# Frontmatter sagt, was der Skill TUT; der Fliesstext, wovon er redet.
#
# GRENZE, UND SIE STEHT HIER. Geprueft wird die NENNUNG des Schlitzes, nicht die
# Aussage darueber. Eine Vorbedingung, die `<TEST_COMMAND>` nennt und etwas Falsches
# darueber sagt, laeuft durch. Die Pruefung faengt das Vergessen, nicht den Irrtum.
# ZWEITE GRENZE: Sie gilt nur fuer `sitzung`-Zellen. Ein `review` braucht keinen
# Messbaum, und ein `skript` fuehrt seine Befehle selbst.
P60_EXEC_RE = re.compile(r"Exec\((<[A-Z_]+_COMMAND>)\)")


def _skills_mit_befehlsschlitz(root: str) -> dict:
    """Skillname -> Liste der Befehlsschlitze, die sein Frontmatter ausfuehrt.

    Abgeleitet aus den Skillquellen, nicht gepflegt: Wer einem Skill einen Befehl
    hinzufuegt, soll nicht daran denken muessen, eine Liste im Validator nachzuziehen.
    """
    raus = {}
    basen = [os.path.join(root, KERN, "framework", "skills"),
             os.path.join(root, KERN, "framework", "role-packs")]
    for basis in basen:
        if not os.path.isdir(basis):
            continue
        for wurzel, _, files in os.walk(basis):
            if "SKILL.md" not in files:
                continue
            text = read(os.path.join(wurzel, "SKILL.md"))
            if not text.startswith("---"):
                continue
            ende = text.find("---", 3)
            if ende < 0:
                continue
            schlitze = sorted(set(P60_EXEC_RE.findall(text[3:ende])))
            if schlitze:
                raus[os.path.basename(wurzel)] = schlitze
    return raus


def check_befehlsschlitz_in_vorbedingung(root: str) -> None:
    """Pruefung 60 (D-178): Der Ausloeser braucht einen Befehl - die Zelle sagt es."""
    skills = _skills_mit_befehlsschlitz(root)
    if not skills:
        err(f"{KERN}/framework/skills/: kein Skill mit 'Exec(<..._COMMAND>)' im "
            f"Frontmatter gefunden – Prüfung 60 leitet ihren Gegenstand daraus ab und "
            f"hat ihn verloren; sie bestünde sonst leise (D-23)")
        return
    dateien = [os.path.join(root, KERN, "tests", "TEST_CATALOG.md")]
    for basis in (os.path.join(root, KERN, "framework", "skills"),
                  os.path.join(root, KERN, "framework", "role-packs")):
        for wurzel, _, files in os.walk(basis):
            if "TESTS.md" in files:
                dateien.append(os.path.join(wurzel, "TESTS.md"))
    for pfad in sorted(dateien):
        if not os.path.isfile(pfad):
            continue
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        i_vor = i_ein = i_pm = -1
        for nr, zeile in enumerate(read(pfad).splitlines(), 1):
            if not zeile.lstrip().startswith("|"):
                continue
            if "Prüfmethode" in zeile and "Eingabe" in zeile:
                i_vor = _tabellenspalte(zeile, "Vorbedingung")
                i_ein = _tabellenspalte(zeile, "Eingabe")
                i_pm = _tabellenspalte(zeile, "Prüfmethode")
                continue
            if min(i_vor, i_ein, i_pm) < 0:
                continue
            zellen = [z.strip() for z in zeile.strip().strip("|").split("|")]
            if len(zellen) <= max(i_vor, i_ein, i_pm):
                continue
            if "sitzung" not in zellen[i_pm]:
                continue
            ausloeser, vorbedingung = zellen[i_ein], zellen[i_vor]
            gebraucht = []
            for skill, schlitze in skills.items():
                if f"/{skill}" in ausloeser:
                    gebraucht += schlitze
            fehlend = sorted({s for s in gebraucht if s not in vorbedingung})
            if fehlend:
                err(f"{rel}:{nr}: Der Auslöser ruft einen Skill auf, der "
                    f"{', '.join(fehlend)} ausführt – die Vorbedingung nennt den "
                    f"Schlitz nicht. Steht der Befehl im Meßbaum im `ask`-Korb, hält "
                    f"der Lauf regelkonform an, und gemessen ist der Korb statt des "
                    f"Gegenstands (D-134, D-178)")


# --- Pruefung 59: Der Overlay-Wert in der Schicht, die ihn durchsetzt ---------------
#
# ANLASS. Gemessen am 2026-09-18 am Uebungsrepositorium (CR-2026-090, Befund 3): 0.63.0
# hat die Sperre von .github/** auf .github/workflows/** EINGEENGT, weil sie sonst die
# Merge-Request-Vorlage mitsperrt - einen Traeger, den fw-mr-description ausdruecklich
# als zulaessige Kontextquelle fuehrt (D-161). Die Einengung steht in
# .koolie/project-overlay/OVERLAY.md. Die beiden Traeger, die den Client WIRKLICH binden - die
# Laufzeitfassung des Overlays und der deny-Korb der Berechtigungsdatei - tragen
# weiterhin den alten, weiteren Wert. git log -S sagt: seit dem ersten Commit des
# Repositoriums unveraendert.
#
# DREI PRUEFUNGEN SAHEN ES NICHT, JEDE AUS EINEM EIGENEN GRUND. Pruefung 56 loest ueber
# die BINDUNGSZEILE DER QUELLE auf - sie liest genau den Traeger, der richtig ist.
# Pruefung 55b fragt, ob der Platzhalter GEBUNDEN ist, nicht welchen WERT er traegt; ihr
# eigener Kopfkommentar sagt seit 0.63.0 "Eine Bindung an den falschen Wert laeuft
# durch." Und --strict-overlay vergleicht Quelle und Laufzeitfassung allein im STATUS -
# der Abgleich der uebrigen Werte ist seit CR-2026-044 E4 offen.
#
# DREI GEGENSTAENDE:
#   (a) Die Laufzeitfassung des Overlays NENNT <EXCLUDED_PATHS>. Ein Traeger, der den
#       Wert nur einsetzt, ist fuer sich stimmig - und faellt niemandem auf. Das ist
#       55b eine Schicht tiefer.
#   (b) Die Zeile, die ihn nennt, traegt DIESELBE Globmenge wie die Bindungszeile der
#       Quelle. Abweichung in beide Richtungen ist ein Fehler; die Quelle ist massgeblich.
#   (c) Jeder Glob der Quelle hat im deny-Korb eine Lese- UND eine Schreibsperre.
#
# GRENZE, UND SIE IST GENANNT. Geprueft wird EIN Platzhalter. <EXCLUDED_PATHS> ist der
# einzige, dessen Wert eine maschinell vergleichbare Gestalt hat - eine Globliste - und
# der zugleich zwei Schichten bindet. Das ist eine Enthaltung, keine Stille.
# ZWEITE GRENZE. (c) prueft nur die Richtung Quelle -> Korb. Ein ueberzaehliger Eintrag
# bleibt zulaessig - dasselbe Argument, mit dem Pruefung 42 die vier Pfadschlitze
# ausnimmt: dort ist Ueberzaehliges ohnehin erlaubt. Der gemessene Fall wird trotzdem
# gefangen, weil .github/workflows/** im Korb FEHLT.
P59_PLATZHALTER = "<EXCLUDED_PATHS>"


def _p59_globs(zellentext: list) -> list:
    """Die Globs einer Wertangabe - je Backtick-Token, an Kommas getrennt.

    Die beiden uebernehmenden Projekte schreiben den Wert verschieden: eines als drei
    Backtick-Token, das andere als eines mit Kommas darin. Wer nur das eine kennt,
    vergleicht Zeichenketten statt Mengen.
    """
    raus = []
    for token in zellentext:
        for teil in token.split(","):
            t = teil.strip()
            if t and t not in raus:
                raus.append(t)
    return raus


def check_overlay_wertabgleich(root: str, man: dict) -> None:
    """Pruefung 59 (D-171): Der Overlay-Wert gilt in der Schicht, die ihn durchsetzt."""
    overlay_pfad = os.path.join(root, ".koolie/project-overlay", "OVERLAY.md")
    if not os.path.isfile(overlay_pfad):
        return  # Kandidatenphase - dieselbe Enthaltung wie Pruefung 42
    quelle = _p59_globs(_p56_ausgeschlossen(read(overlay_pfad)))
    if not quelle or any(TBD_RE.search(g) for g in quelle):
        return  # noch nicht ausgefuellt - das meldet --check-overlay-ready
    rel_rt = f"{man['pack_runtime_dir']}/{regeldatei(man, '20-project-overlay.md')}"
    runtime_pfad = os.path.join(root, *rel_rt.split("/"))
    if os.path.isfile(runtime_pfad):
        text = read(runtime_pfad)
        zeilen = [z for z in text.split("\n") if P59_PLATZHALTER in z]
        if not zeilen:
            err(f"{rel_rt}: nennt {P59_PLATZHALTER} nicht. Die Laufzeitfassung setzt den "
                f"Wert damit ein, statt den Platzhalter zu binden – sie ist für sich "
                f"stimmig, und niemand sieht, ob ihr Wert noch der des Quell-Overlays "
                f"ist. Genau so hat eine Einengung aus 0.63.0 die Schicht nie erreicht, "
                f"die sie durchsetzt (D-171)")
        elif not TBD_RE.search(zeilen[0]):
            # Ein Ausfuellschlitz in der Laufzeitfassung ist Sache von --strict-overlay,
            # das ihn schon meldet - zwei Meldungen fuer einen Zustand sind eine zuviel.
            ist = _p59_globs([t for t in re.findall(r"`([^`]+)`", zeilen[0])
                              if t != P59_PLATZHALTER])
            fehlt = [g for g in quelle if g not in ist]
            zuviel = [g for g in ist if g not in quelle]
            if fehlt or zuviel:
                err(f"{rel_rt}: die ausgeschlossenen Pfade weichen vom Quell-Overlay ab – "
                    f"dort fehlend: {', '.join(fehlt) or 'keine'}; dort nicht vorgesehen: "
                    f"{', '.join(zuviel) or 'keine'}. Maßgeblich ist "
                    f".koolie/project-overlay/OVERLAY.md; die Laufzeitfassung ist die Schicht, die "
                    f"der Client lädt (D-171)")
    # Gegenstand (c) liest den deny-Korb einer JSON-Datei. Bis 1.4.4 stand er nicht in
    # FORMATGEBUNDENE_PRUEFUNGEN und kehrte bei einem Pack mit TOML an json.loads still
    # zurueck - gemessen mit CR-2026-138 an einer Wegwerf-Installation von openai-codex:
    # <EXCLUDED_PATHS> in Quelle und Laufzeitfassung gefuellt, in der Berechtigungsdatei
    # keine Sperre, und diese Pruefung meldete nichts. Die Luecke ist dieselbe; sie ist
    # jetzt erklaert (D-346) statt verschwiegen.
    if formatgebunden(man, 59):
        return
    rel_perm = man["permissions_file"]
    perm_pfad = os.path.join(root, *rel_perm.split("/"))
    if not os.path.isfile(perm_pfad):
        return
    try:
        cfg = json.loads(read(perm_pfad))
    except json.JSONDecodeError:
        return  # check_config hat das bereits gemeldet
    deny = [r for r in cfg.get("permissions", {}).get("deny", []) if isinstance(r, str)]
    if any(P59_PLATZHALTER in r for r in deny):
        return  # Schlitz noch ungefuellt - das ist Sache von --check-overlay-ready
    praefix = man.get("permission_path_prefix", "")
    werkzeuge = man.get("permission_tools", {})
    for art in ("read", "write"):
        for werkzeug in werkzeuge.get(art, ()):
            for glob in quelle:
                if any(f"{werkzeug}({p}{glob})" in deny for p in ("", praefix)):
                    continue
                err(f"{rel_perm}: der ausgeschlossene Pfad `{glob}` des Quell-Overlays hat "
                    f"keine Regel {werkzeug}({glob}) im deny-Korb. Die Berechtigungsdatei "
                    f"ist die Schicht, die technisch sperrt – ein Wert, der nur im Overlay "
                    f"steht, sperrt nichts (D-171)")


# --- Pruefung 89: die uebrigen Pfadplatzhalter in den Schichten, die sie tragen ------
#
# ANLASS (K-69, CR-2026-136 E4, CR-2026-138 E6). Pruefung 59 vergleicht EINEN
# Pfadplatzhalter. <ALLOWED_PATHS>, <TEST_PATHS>, <DOC_PATHS> und <READ_ONLY_PATHS> haben
# dieselbe Gestalt - eine Globliste - und waren ungeprueft, nicht geprueft-und-gut:
# Gezaehlt am 2026-09-18 wich von sechs Werten des Uebungs-Overlays einer ab. Weil
# Laufzeitfassung und Berechtigungsdatei Saat bleiben (D-353), faengt nur eine Pruefung
# die Handpflege an drei Stellen auf.
#
# DREI GEGENSTAENDE, dieselben wie bei 59:
#   (a) Die Laufzeitfassung NENNT jeden der vier Platzhalter. Ein Traeger, der den Wert
#       nur einsetzt, ist fuer sich stimmig - und niemand sieht, ob sein Wert noch der
#       der Quelle ist (D-160).
#   (b) Der Wert hinter dem Platzhalter ist dieselbe Menge wie in der Quelle.
#   (c) Jeder Nur-Lese-Pfad hat im deny-Korb eine Schreibsperre. Seit 1.5.0 fuehrt die
#       Kernquelle den Schlitz dafuer (D-356); bis dahin trugen beide uebernehmenden
#       Projekte die Sperre von Hand - auf dieselbe Weise.
#       Seit 1.20.1 ebenso jeder Glob von <CI_CONFIG_PATHS> und
#       <QUALITY_GATE_CONFIG_PATHS> (CR-2026-163, D-493, K-35). Beide stehen nur im
#       deny-Korb, und ein zu ENG gefuellter Schlitz ist eine stille Lockerung.
#       "Deckungsgleich" heisst: Jeder Glob der Quelle hat seine eigene Regel - so
#       entfaltet install.py den Schlitz auch. Die Laufzeitfassung fuehrt die beiden
#       nicht; (a) und (b) gelten fuer sie deshalb nicht.
#
# DIE QUELLE IST DIE DREISPALTIGE ZEILE VON ABSCHNITT 4, gefunden ueber die
# Platzhalterzelle. Ein Overlay, das anders bindet, ENTGEHT der Pruefung nicht still: Es
# bekommt eine eigene Meldung (CR-2026-136 E4, "melden, nicht verschweigen").
#
# "KEIN WERT" HAT MEHRERE SCHREIBWEISEN, und sie sind gemessen: Der Pilot fuehrt fuer
# <DOC_PATHS> in der Quelle `nicht vorhanden`, in der Laufzeitfassung `keine`. Beides
# ist die leere Menge; wer Zeichenketten vergleicht, meldet einen Unterschied, den es
# nicht gibt.
#
# GRENZE. Der Wert in der Laufzeitfassung endet am ersten " · " oder " – " der Zeile;
# was danach steht ("zusaetzlich immer ...") ist Erlaeuterung und gehoert nicht zur
# Menge. Und (c) prueft wie 59 nur die Richtung Quelle -> Korb.
P89_PLATZHALTER = ("<ALLOWED_PATHS>", "<TEST_PATHS>", "<DOC_PATHS>", "<READ_ONLY_PATHS>")
P89_SPERRPLATZHALTER = ("<READ_ONLY_PATHS>", "<CI_CONFIG_PATHS>", "<QUALITY_GATE_CONFIG_PATHS>")
P89_KEIN_WERT = {"nicht vorhanden", "keine", "keiner", "kein", "–", "-"}


def _p89_menge(werte: list) -> list:
    """Die Globs einer Wertangabe ohne die Schreibweisen fuer "kein Wert"."""
    return [g for g in _p59_globs(werte) if g.lower() not in P89_KEIN_WERT]


def _p89_quelle(text: str, platzhalter: str):
    """(Zeile gefunden, Werte oder None bei Ausfuellschlitz) aus Abschnitt 4 des Overlays."""
    for zeile in text.replace("\r\n", "\n").split("\n"):
        zellen = tabellenzellen(zeile.strip())
        for i, zelle in enumerate(zellen[:-1]):
            if zelle.strip() != f"`{platzhalter}`":
                continue
            wert = zellen[i + 1]
            if TBD_RE.search(wert):
                return True, None
            treffer = re.findall(r"`([^`]+)`", wert)
            return True, _p89_menge(treffer or [wert.strip()])
    return False, None


def _p89_laufzeit(text: str, platzhalter: str):
    """(Zeile gefunden, Werte oder None bei Ausfuellschlitz) aus der Laufzeitfassung."""
    token = f"`{platzhalter}`"
    for zeile in text.replace("\r\n", "\n").split("\n"):
        if token not in zeile:
            continue
        rest = zeile.split(token, 1)[1].lstrip(")").lstrip(":").strip()
        rest = re.split(r" · | – ", rest, maxsplit=1)[0]
        if TBD_RE.search(rest):
            return True, None
        treffer = [t for t in re.findall(r"`([^`]+)`", rest)
                   if not PROJEKTPLATZHALTER.fullmatch(t)]
        return True, _p89_menge(treffer or [rest.strip().rstrip(".")])
    return False, None


def check_overlay_pfadabgleich(root: str, man: dict) -> None:
    """Pruefung 89 (K-69, D-357): die vier uebrigen Pfadplatzhalter in allen Schichten."""
    overlay_pfad = os.path.join(root, ".koolie/project-overlay", "OVERLAY.md")
    if not os.path.isfile(overlay_pfad):
        return  # Kandidatenphase - dieselbe Enthaltung wie Pruefung 59
    quelltext = read(overlay_pfad)
    rel_rt = f"{man['pack_runtime_dir']}/{regeldatei(man, '20-project-overlay.md')}"
    runtime_pfad = os.path.join(root, *rel_rt.split("/"))
    laufzeit = read(runtime_pfad) if os.path.isfile(runtime_pfad) else None
    sperren: dict = {}
    for platzhalter in P89_PLATZHALTER:
        da, quelle = _p89_quelle(quelltext, platzhalter)
        if not da:
            err(f".koolie/project-overlay/OVERLAY.md: keine Zeile mit der Platzhalterzelle "
                f"`{platzhalter}` in Abschnitt 4. Prüfung 89 liest den Wert aus der "
                f"dreispaltigen Zeile der Vorlage; ein Overlay, das anders bindet, wird "
                f"gemeldet und nicht übergangen (K-69, CR-2026-136 E4)")
            continue
        if quelle is None:
            continue  # noch nicht ausgefuellt - das meldet --check-overlay-ready
        if platzhalter == "<READ_ONLY_PATHS>":
            sperren[platzhalter] = quelle
        if laufzeit is None:
            continue
        da, ist = _p89_laufzeit(laufzeit, platzhalter)
        if not da:
            err(f"{rel_rt}: nennt {platzhalter} nicht. Die Laufzeitfassung setzt den Wert "
                f"damit ein, statt den Platzhalter zu binden – sie ist für sich stimmig, und "
                f"niemand sieht, ob ihr Wert noch der des Quell-Overlays ist (D-160, K-69)")
            continue
        if ist is None:
            continue  # Ausfuellschlitz in der Laufzeitfassung - Sache von --strict-overlay
        fehlt = [g for g in quelle if g not in ist]
        zuviel = [g for g in ist if g not in quelle]
        if fehlt or zuviel:
            err(f"{rel_rt}: der Wert von {platzhalter} weicht vom Quell-Overlay ab – dort "
                f"fehlend: {', '.join(fehlt) or 'keine'}; dort nicht vorgesehen: "
                f"{', '.join(zuviel) or 'keine'}. Maßgeblich ist "
                f".koolie/project-overlay/OVERLAY.md (K-69)")
    for platzhalter in P89_SPERRPLATZHALTER[1:]:
        da, quelle = _p89_quelle(quelltext, platzhalter)
        if da and quelle:
            sperren[platzhalter] = quelle  # fehlende Zeile: dasselbe Schweigen wie --strict
    if not sperren or formatgebunden(man, 89):
        return
    rel_perm = man["permissions_file"]
    perm_pfad = os.path.join(root, *rel_perm.split("/"))
    if not os.path.isfile(perm_pfad):
        return
    try:
        cfg = json.loads(read(perm_pfad))
    except json.JSONDecodeError:
        return  # check_config hat das bereits gemeldet
    deny = [r for r in cfg.get("permissions", {}).get("deny", []) if isinstance(r, str)]
    praefix = man.get("permission_path_prefix", "")
    for platzhalter, globs in sperren.items():
        if any(platzhalter in r for r in deny):
            continue  # Schlitz noch ungefuellt - das ist Sache von --strict-overlay
        for werkzeug in man.get("permission_tools", {}).get("write", ()):
            for glob in globs:
                if any(f"{werkzeug}({p}{glob})" in deny for p in ("", praefix)):
                    continue
                if platzhalter == "<READ_ONLY_PATHS>":
                    err(f"{rel_perm}: der Nur-Lese-Pfad `{glob}` des Quell-Overlays hat keine "
                        f"Regel {werkzeug}({glob}) im deny-Korb. Ein Integritätsschutz, der nur "
                        f"im Overlay steht, sperrt nichts (K-69, D-356)")
                else:
                    err(f"{rel_perm}: der Pfad `{glob}` aus {platzhalter} des Quell-Overlays "
                        f"hat keine Regel {werkzeug}({glob}) im deny-Korb. Ein zu eng "
                        f"gefüllter Schlitz ist eine stille Lockerung (K-35, D-493)")
