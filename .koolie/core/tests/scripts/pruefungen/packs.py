"""Die Client Packs als Dokumente: Quellenauskunft, Dokumenttabellen, normative Kommentare,
Regelablage, Ausfall mit Ersatz, Werkzeugabwesenheit, Zusagenfelder, Abwesenheitsbeleg,
Schlitzinhalte, Zusatzschluessel, Matrixzeilen, Vorlage und formatgebundene Pruefungen.

Pruefungen 19, 20, 23, 24, 25, 26, 27, 41, 42, 54, 74, 84 und 87. Teil des Validators
validate-framework.py, seit 1.19.1 nach Gegenstand in Module geteilt (K-174). Das
Register aller Pruefungen steht im Kopfkommentar des Einstiegs, die Grenze jeder
einzelnen in ihrem Kopfkommentar hier."""
from __future__ import annotations

import json
import os
import re

from .gemeinsam import (
    _client_packs, _walk_text_files, err, formatgebunden, FORMATGEBUNDENE_PRUEFUNGEN,
    FRONTMATTER_BLOECKE, KERN, korb_zerlegung, MATRIXZEILE_RE, P73_ZEILE_RE,
    PROJEKTPLATZHALTER, read, soll_korbregeln, tabellenzellen)


def nicht_erreicht(man: dict) -> set:
    """Die Nummern, die die Ausgabeform dieses Packs nicht erreichen (Pruefung 87)."""
    form = man.get("permissions_format", "json")
    return {n for n, (_, formen) in FORMATGEBUNDENE_PRUEFUNGEN.items() if form not in formen}


# ---------------------------------------------------------------------------
# Pruefungen 19 bis 24 (Release 0.26.0)
# ---------------------------------------------------------------------------

AUSKUNFT_UEBERSCHRIFT = "Anweisungs- und Konfigurationsquellen außerhalb des Projekts"
DATUM_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")


def _abschnitt(text: str, ueberschrift: str) -> str | None:
    """Text eines Abschnitts bis zur naechsten gleichrangigen Ueberschrift."""
    m = re.search(r"^(#{2,3})\s*\d*[a-z]?\.?\s*" + re.escape(ueberschrift) + r"\s*$",
                  text, re.M)
    if not m:
        return None
    ebene = len(m.group(1))
    rest = text[m.end():]
    weiter = re.search(r"^#{1,%d}\s" % ebene, rest, re.M)
    return rest[:weiter.start()] if weiter else rest


def check_quellenauskunft(root: str) -> None:
    """Pruefung 19 (D-34, D-37): Jedes Client Pack gibt Auskunft ueber Quellen ausserhalb.

    GRENZE DIESER PRUEFUNG - sie steht hier, weil sie im Antrag vorab benannt und nicht
    spaeter gefunden werden soll (CR-2026-031 E4): Geprueft wird die **Anwesenheit** der
    Auskunft, nicht ihre **Richtigkeit**. Eine falsche oder veraltete Zeile besteht sie.
    Ein Abwesenheitsbeleg altert, und dieses Skript sieht den Unterschied nicht - "keine
    bekannt, Stand 2026-09-11" ist am Tag der naechsten Clientversion eine Behauptung
    ueber die Vergangenheit. Die Richtigkeit haengt an einer Erhebung, nicht an einem
    Skript; dasselbe gilt fuer Pruefung 22.
    """
    for kennung, pdir, _man in _client_packs(root):
        rel = f"{KERN}/clients/{kennung}/CLIENT_PACK.md"
        text = read(os.path.join(pdir, "CLIENT_PACK.md"))
        abschnitt = _abschnitt(text, AUSKUNFT_UEBERSCHRIFT)
        if abschnitt is None:
            err(f"{rel}: Abschnitt '{AUSKUNFT_UEBERSCHRIFT}' fehlt. Jedes Pack fuehrt die "
                f"bekannten Quellen ausserhalb des Repositoriums - Regeltexte, Skills, "
                f"Agentenprofile, Berechtigungen, Hooks - oder einen datierten "
                f"Abwesenheitsbeleg (D-34, D-37)")
            continue
        zeilen = [z for z in abschnitt.splitlines()
                  if z.strip().startswith("|") and not re.match(r"^\|[\s:|-]+\|?$", z.strip())]
        inhalt = [z for z in zeilen
                  if not re.search(r"\|\s*(Quelle|Ladebedingung|Wirkung)\s*\|", z)]
        abwesend = re.search(r"keine bekannt", abschnitt, re.I)
        if not inhalt and not abwesend:
            err(f"{rel}: Abschnitt '{AUSKUNFT_UEBERSCHRIFT}' ist leer. Er braucht je "
                f"bekannter Quelle eine Zeile oder die ausdrueckliche Angabe 'keine "
                f"bekannt' mit Datum und Erhebungsweg - ein leerer Abschnitt ist kein "
                f"Abwesenheitsbeleg")
            continue
        if kennung.startswith("_"):
            continue  # Vorlage: Erhebungsstand steht als <TBD>
        if not DATUM_RE.search(abschnitt):
            err(f"{rel}: Abschnitt '{AUSKUNFT_UEBERSCHRIFT}' nennt keinen Erhebungsstand "
                f"(JJJJ-MM-TT). Eine Quellenliste ohne Datum ist keine Auskunft, sondern "
                f"eine Behauptung mit Fussnote")


# Begriff der Dokumenttabellen -> Platzhalter des Manifests. Ein Begriff ohne Eintrag
# bleibt unbeanstandet: "Nutzerlokale Ueberschreibung" hat kein Manifestfeld und ist
# zugleich die Gegenprobe dieser Pruefung.
GLOSSAR_ZU_PLATZHALTER = {
    "Wurzel-Anweisungsdatei": "<ROOT_INSTRUCTION_FILE>",
    "Laufzeitschicht": "<RUNTIME_DIR>",
    "Berechtigungsdatei": "<PERMISSIONS_FILE>",
    "Regelablage": "<RULES_DIR>",
    "Skill-Ablage": "<SKILLS_DIR>",
    "Agentenprofile": "<AGENTS_DIR>",
    "Hook-Konfiguration": "<HOOKS_FILE>",
    "MCP-Konfiguration": "<MCP_FILE>",
}
# <CORE_DIR> ist keine Eigenschaft eines Clients, sondern dieser Installation; ein Pack
# darf ihn nicht belegen (PLACEHOLDER_REGISTRY.md).
PLATZHALTER_OHNE_PACK = ("<CORE_DIR>",)


def _tabellenzeilen(text: str):
    for zeile in text.splitlines():
        z = zeile.strip()
        if not z.startswith("|") or re.match(r"^\|[\s:|-]+\|?$", z):
            continue
        yield tabellenzellen(z)


def _spalten_je_pack(felder: list[str], packs: list[str]) -> dict[str, int]:
    zuordnung: dict[str, int] = {}
    for i, feld in enumerate(felder):
        nackt = feld.strip("`* ")
        if nackt in packs:
            zuordnung[nackt] = i
    return zuordnung


def _wert_passt(zelle: str, erwartet: str) -> bool:
    """Der Manifestwert steht in der Zelle - Schreibvarianten zugelassen.

    Die Tabellen schreiben ein Verzeichnis mal mit und mal ohne abschliessenden
    Schraegstrich und setzen den Wert gelegentlich in einen erklaerenden Satz. Geprueft
    wird deshalb Enthaltensein, nicht Gleichheit: Diese Pruefung soll eine **abweichende**
    Angabe finden, nicht eine anders formulierte.
    """
    zelle = zelle.replace("\\", "/")
    kandidaten = {erwartet, erwartet.rstrip("/") + "/", erwartet.rstrip("/")}
    return any(k and k in zelle for k in kandidaten)


def _spalten_vollstaendig(traeger: str, gefunden: dict, namen: list) -> None:
    """Jedes Pack mit Manifest hat in der Tabelle eine Spalte (1.14.0, D-421).

    ANLASS: Die Pruefung verglich nur die Spalten, die es gab. Ein Pack ohne Spalte
    fiel still heraus - mit 1.13.0 fuehrten beide Tabellen kiro nicht, und keine
    Meldung sagte es. Eine Uebereinstimmung ueber die Haelfte der Packs ist keine.
    """
    for pack in sorted(set(namen) - set(gefunden)):
        err(f"{traeger}: die Tabelle fuehrt keine Spalte fuer '{pack}' - ein Pack ohne "
            f"Spalte faellt aus dem Abgleich mit seinem Manifest still heraus (D-421)")


def check_dokumenttabellen(root: str) -> None:
    """Pruefung 20 (CR-2026-036): Dokumenttabellen und Manifest sagen dasselbe.

    GRENZE: Sie prueft **Uebereinstimmung, nicht Richtigkeit.** Steht im Manifest ein
    falscher Pfad, sind Tabelle und Manifest danach einig - und beide falsch. Was den
    Manifestwert prueft, ist die Installation selbst und der Nachweis an ihr (D-23).
    Abgedeckt sind nur Zeilen mit Manifestentsprechung; Begriffe ohne Feld altern weiter
    still.
    """
    packs = {k: m for k, _p, m in _client_packs(root) if m}
    if not packs:
        return
    namen = sorted(packs)

    registry = f"{KERN}/docs/PLACEHOLDER_REGISTRY.md"
    pfad = os.path.join(root, *registry.split("/"))
    if os.path.isfile(pfad):
        text = read(pfad)
        spalten: dict[str, int] = {}
        for felder in _tabellenzeilen(text):
            gefunden = _spalten_je_pack(felder, namen)
            if gefunden:
                spalten = gefunden
                _spalten_vollstaendig(registry, gefunden, namen)
                continue
            platzhalter = felder[0].strip("`* ")
            if not spalten or not platzhalter.startswith("<"):
                continue
            if platzhalter in PLATZHALTER_OHNE_PACK:
                continue
            for pack, i in spalten.items():
                erwartet = (packs[pack].get("runtime_placeholders") or {}).get(platzhalter)
                if erwartet is None or i >= len(felder):
                    continue
                if not _wert_passt(felder[i].strip("`* "), erwartet):
                    err(f"{registry}: {platzhalter} steht fuer '{pack}' als "
                        f"'{felder[i]}', das Manifest fuehrt '{erwartet}'. Die "
                        f"maschinenlesbare Quelle gilt; die Tabelle wird nachgezogen")

    glossar = f"{KERN}/docs/RUNTIME_GLOSSARY.md"
    pfad = os.path.join(root, *glossar.split("/"))
    if os.path.isfile(pfad):
        text = read(pfad)
        spalten = {}
        for felder in _tabellenzeilen(text):
            gefunden = _spalten_je_pack(felder, namen)
            if gefunden:
                spalten = gefunden
                _spalten_vollstaendig(glossar, gefunden, namen)
                continue
            if not spalten:
                continue
            begriff = felder[0].strip("`* ")
            platzhalter = GLOSSAR_ZU_PLATZHALTER.get(begriff)
            if not platzhalter:
                continue  # Begriff ohne Manifestfeld - siehe Kommentar oben
            for pack, i in spalten.items():
                erwartet = (packs[pack].get("runtime_placeholders") or {}).get(platzhalter)
                if erwartet is None or i >= len(felder):
                    continue
                if not _wert_passt(felder[i], erwartet):
                    err(f"{glossar}: '{begriff}' steht fuer '{pack}' als '{felder[i]}', "
                        f"das Manifest fuehrt '{erwartet}'. Die maschinenlesbare Quelle "
                        f"gilt; die Tabelle wird nachgezogen")


# Normative Schluesselwoerter. Ein Kommentar traegt Herkunft - Ebene, Version, Owner,
# Ladeverhalten -, keine Anweisung: Er erreicht nicht jede Sitzung (ERH-01, K-28, D-38).
NORMATIVE_WOERTER = (
    re.compile(r"\bMUSS\b"),
    re.compile(r"\bMUESSEN\b"),
    re.compile(r"\bDARF NICHT\b"),
    re.compile(r"\bDUERFEN NICHT\b"),
    re.compile(r"\bSOLL\b"),
    re.compile(r"\bNICHT ZULAESSIG\b"),
    re.compile(r"(?i)nur über den änderungsprozess"),
    re.compile(r"(?i)darf nur über"),
)
HTML_KOMMENTAR_RE = re.compile(r"<!--(.*?)-->", re.S)


def _laufzeitartefakte(root: str, man: dict):
    """Die Artefakte, die in einer Sitzung geladen werden - Quelle und Installation."""
    for unterbau in (f"{KERN}/framework/runtime", f"{KERN}/templates/rules"):
        basis = os.path.join(root, *unterbau.split("/"))
        if os.path.isdir(basis):
            for pfad in _walk_text_files(basis):
                if pfad.endswith((".md", ".template")):
                    yield pfad
    orte = [man.get("root_instruction_file"),
            (man.get("runtime_placeholders") or {}).get("<RULES_DIR>")]
    for ort in orte:
        if not ort:
            continue
        ziel = os.path.join(root, *ort.split("/"))
        if os.path.isfile(ziel):
            yield ziel
        elif os.path.isdir(ziel):
            for pfad in _walk_text_files(ziel):
                if pfad.endswith((".md", ".template")):
                    yield pfad


def check_normative_kommentare(root: str, man: dict) -> None:
    """Pruefung 23 (D-38): Kein normatives Schluesselwort in einem HTML-Kommentar.

    Gemessen an **beiden** Clients, mit entgegengesetztem Ergebnis. Bei 'claude-code' blieb
    dieselbe Messmarke unsichtbar, solange sie in Kommentarklammern stand, und war im
    Klartext sofort im Kontext - in der Wurzel-Anweisungsdatei und in der Regelablage
    (2026-09-11, ERH-01). Bei 'devin-desktop' steht der Kommentar **woertlich** in dem
    Regelblock, den der Client bildet; die Sitzung gab die Marke aus dem Kommentar zurueck,
    ohne eine Datei zu lesen (2026-09-12, K-28).

    Genau das traegt die Pruefung. Ein Ablageort, an dem eine Aussage bei dem einen Client
    verschwindet und beim anderen mitlaeuft, ist fuer eine normative Aussage untauglich:
    Was gilt, darf nicht davon abhaengen, mit welchem Werkzeug gearbeitet wird. Die
    Begruendung ist damit belastbarer als vorher - die alte ('erreicht die Sitzung nicht')
    waere mit einem Client, der Kommentare durchreicht, hinfaellig gewesen; genau so einer
    ist gemessen worden. Was gilt, steht im Fliesstext.

    GRENZE: Eine Wortlistenpruefung meldet auch eine zutreffende Erwaehnung - etwa den
    Verweis auf eine Regel, die 'MUSS' enthaelt. Fehlalarme sind moeglich und beim
    Beschluss ausdruecklich in Kauf genommen (CR-2026-039 E3). Die strengere Lesart gilt
    fuer beide Packs - nicht mehr vorsorglich, weil das Verhalten des zweiten unerhoben
    waere, sondern weil es erhoben ist und **abweicht** (K-28, CR-2026-040).
    """
    gesehen = set()
    for pfad in _laufzeitartefakte(root, man):
        if pfad in gesehen:
            continue
        gesehen.add(pfad)
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        text = read(pfad)
        for m in HTML_KOMMENTAR_RE.finditer(text):
            inhalt = m.group(1)
            zeile = text.count("\n", 0, m.start()) + 1
            for muster in NORMATIVE_WOERTER:
                treffer = muster.search(inhalt)
                if not treffer:
                    continue
                err(f"{rel}:{zeile}: '{treffer.group(0)}' steht in einem HTML-Kommentar. "
                    f"Ein Kommentar erreicht nicht jede Sitzung (ERH-01, K-28); eine normative "
                    f"Aussage gehoert in den Fliesstext, im Kommentar bleibt die Herkunft "
                    f"(D-38)")
                break


# Was in der Vorlage einer Regelablage liegen darf: Regeltexte nach dem Nummernschema
# und Vorlagen. Alles andere ist ein Nicht-Regeltext - der Client registriert, was in
# der Ablage liegt, und macht es damit ladbar (AP2-DD-17, K-26).
REGELDATEI_RE = re.compile(r"^\d[\dN]-[A-Za-z0-9._-]+\.md(\.template)?$")


def check_regelablage_sauber(root: str) -> None:
    """Pruefung 24 (D-36): In der Vorlage der Regelablage liegt nur, was Regel ist.

    Bis 0.25.0 lag dort je Pack eine erklaerende README. Bei einem Pack fuehrte der
    Client sie als Regel mit Trigger 'manual' (AP2-DD-17), beim anderen stand sie sogar
    unbedingt im Kontext (K-26) - mit Belegvorbehalten, die damit den Rang eines
    Regeltexts trugen. Der erklaerende Text steht seither eine Ebene hoeher, in der
    Laufzeit-README.

    GRENZE: Geprueft wird die **Vorlage** des Packs, nicht die installierte Ablage. Was
    ein Projekt dort selbst ablegt, sieht diese Pruefung nicht.
    """
    for kennung, pdir, man in _client_packs(root):
        if not man:
            continue
        regelablage = (man.get("runtime_placeholders") or {}).get("<RULES_DIR>")
        if not regelablage:
            continue
        basis = os.path.join(pdir, "root-template", *regelablage.split("/"))
        if not os.path.isdir(basis):
            continue
        for name in sorted(os.listdir(basis)):
            if os.path.isdir(os.path.join(basis, name)):
                err(f"{KERN}/clients/{kennung}/root-template/{regelablage}/{name}: "
                    f"Unterverzeichnis in der Vorlage der Regelablage")
                continue
            if REGELDATEI_RE.match(name):
                continue
            err(f"{KERN}/clients/{kennung}/root-template/{regelablage}/{name}: kein "
                f"Regeltext. Die Regelablage enthaelt ausschliesslich Regeln (D-36) - "
                f"der Client registriert, was dort liegt, und macht es ladbar. "
                f"Erklaerender Text gehoert in die Laufzeit-README eine Ebene hoeher")


# Pruefung 25: Eine Zeile auf [NICHT ABBILDBAR] nennt den Ersatz.
#
# Die Einstufungsklasse sagt "der Client bietet keinen Mechanismus". Sie sagt nicht, was an
# seine Stelle tritt - und genau dort entsteht die stillschweigende Verschlechterung: Ein
# Ausfall wird eingetragen, niemand widerspricht, und die Zusage ist weg, ohne dass eine
# Entscheidung darueber gefallen waere.
#
# D-41 unterscheidet deshalb Kernzusagen von Faehigkeitszusagen. Eine Kernzusage auf
# [NICHT ABBILDBAR] sperrt die Inbetriebnahme; eine Faehigkeitszusage sperrt nicht, MUSS aber
# den Ersatz benennen. Diese Pruefung setzt den zweiten Teil durch - den ersten kann kein
# Skript durchsetzen, er ist eine Freigabe durch einen Menschen.
NICHT_ABBILDBAR_RE = re.compile(r"`\[NICHT ABBILDBAR\]`")


def check_ausfall_mit_ersatz(root: str) -> None:
    """Pruefung 25 (D-41): Kein Ausfall ohne benannten Ersatz.

    Geprueft werden die Matrixzeilen der Client Packs - erkennbar an der Zeilenkennung am
    Zeilenanfang (B3, S5, X2). Die Zusammenfassungstabellen desselben Dokuments fuehren
    dieselbe Klasse als Zeilenbeschriftung; sie sind keine Zusagen und bleiben unberuehrt.

    Verlangt wird das Wort 'Ersatz' in der Zeile. Das ist bewusst grob: Die Pruefung kann
    nicht beurteilen, ob ein Ersatz taugt - sie kann nur erzwingen, dass jemand die Frage
    gestellt und beantwortet hat. Ein 'kein Ersatz' genuegt ihr, und das ist richtig so:
    Der Satz 'hierfuer gibt es keinen Ersatz' ist eine Aussage, die jemand verantwortet.

    GRENZE: Eine Wortpruefung. Wer 'Ersatz' hinschreibt, ohne einen zu nennen, kommt durch.
    Sie faengt das Vergessen, nicht die Absicht - wie Pruefung 23 (CR-2026-041 E3).
    """
    basis = os.path.join(root, KERN, "clients")
    if not os.path.isdir(basis):
        return
    for pack in sorted(os.listdir(basis)):
        if pack.startswith("_"):
            continue
        pfad = os.path.join(basis, pack, "CLIENT_PACK.md")
        if not os.path.isfile(pfad):
            continue
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        for i, zeile in enumerate(read(pfad).splitlines(), 1):
            if not NICHT_ABBILDBAR_RE.search(zeile):
                continue
            m = MATRIXZEILE_RE.match(zeile)
            if not m:
                continue
            if "ersatz" in zeile.lower():
                continue
            err(f"{rel}:{i}: Zeile {m.group(1)} steht auf [NICHT ABBILDBAR], ohne einen "
                f"Ersatz zu benennen. Ein Ausfall, der nur eingetragen und nicht ersetzt "
                f"wird, ist eine stillschweigende Verschlechterung: Die Zeile nennt den "
                f"Ersatz oder haelt fest, dass es keinen gibt (D-41)")


# Pruefung 26: Eine erklaerte Werkzeugabwesenheit muss belegt und folgerichtig sein.
#
# Seit CR-2026-047 darf ein Pack im Feld hook_tools_absent erklaeren, dass sein Client
# eine Werkzeugklasse gar nicht kennt; die Abbildung laesst den Hook-Matcher dann ohne
# diese Klasse durchlaufen, statt abzubrechen. Das ist noetig - ein Client ohne eigenes
# Suchwerkzeug kann keines abbilden - und es ist zugleich ein Schlupfloch: Wer 'write'
# dort eintraege, naehme das schreibende Werkzeug aus der Durchsetzung, und nichts
# meldete es.
#
# Diese Pruefung schliesst es an zwei Stellen:
#   1. Die Abwesenheit muss folgerichtig sein - ein Verb, das hier steht, muss auch in
#      permission_tools leer sein. Ein Client, fuer den die Berechtigungsschicht ein
#      Werkzeug dieser Klasse kennt, hat eines.
#   2. Die Abwesenheit muss erklaert sein - ein nicht leerer Begleitsatz. Dieselbe
#      Begruendung wie bei Pruefung 25: Ein Ausfall, den jemand verantwortet, ist etwas
#      anderes als einer, der eingetragen wurde.
#
# GRENZE: Die Pruefung belegt nicht, dass der Client das Werkzeug wirklich nicht hat -
# das kann nur eine Erhebung. Sie belegt, dass die beiden Felder, die es behaupten,
# einander nicht widersprechen und dass jemand den Satz dazu geschrieben hat.
def check_werkzeugabwesenheit(root: str) -> None:
    """Pruefung 26 (D-47): hook_tools_absent ist folgerichtig und erklaert."""
    basis = os.path.join(root, KERN, "clients")
    if not os.path.isdir(basis):
        return
    for pack in sorted(os.listdir(basis)):
        if pack.startswith("_"):
            continue
        pfad = os.path.join(basis, pack, "manifest.json")
        if not os.path.isfile(pfad):
            continue
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        try:
            man = json.loads(read(pfad))
        except ValueError:
            continue
        abwesend = man.get("hook_tools_absent") or []
        if not abwesend:
            continue
        if not isinstance(abwesend, list):
            err(f"{rel}: hook_tools_absent ist keine Liste")
            continue
        notiz = str(man.get("_hook_tools_absent_note") or "").strip()
        if not notiz:
            err(f"{rel}: hook_tools_absent nennt {sorted(abwesend)}, aber "
                f"_hook_tools_absent_note fehlt oder ist leer. Eine Werkzeugklasse aus "
                f"der Durchsetzung zu nehmen, ist eine Aussage ueber den Client - sie "
                f"gehoert begruendet, nicht bloss eingetragen (D-47)")
        werkzeuge = man.get("permission_tools") or {}
        for verb in sorted(abwesend):
            if werkzeuge.get(verb):
                err(f"{rel}: hook_tools_absent erklaert das Verb '{verb}' fuer abwesend, "
                    f"permission_tools nennt dafuer aber {werkzeuge[verb]}. Beides "
                    f"zugleich geht nicht: Kennt die Berechtigungsschicht ein Werkzeug "
                    f"dieser Klasse, hat der Client eines, und der Hook muss es "
                    f"erreichen (D-47)")


# Pruefung 27: Ein verworfenes Zusagenfeld eines Skills nennt seinen Ersatz.
#
# Dieselbe Bauform wie Pruefung 26, eine Ebene weiter: Ein Pack darf ein Frontmatter-Feld
# verwerfen, das sein Client nicht kennt - aber nicht eines, das eine Zusage traegt, ohne
# zu sagen, was an seine Stelle tritt.
#
# Zwei Faelle gab es dafuer schon: 'triggers' verfiel beim Rendern, bis AP2-CC-01 es fand
# und eine Abbildung bekam (model_invocation_field). 'permissions' verfiel bis 0.30.0 auf
# genau dieselbe Weise - im Manifest unter drop_fields deklariert, in der Wirkung
# unbemerkt, und dabei trug es das 'deny: edit, exec' von zwoelf Skills (B01, D-50).
#
# install.py bricht seit 0.31.0 ab, wenn das passiert. Diese Pruefung findet denselben
# Fehler **ohne** Installation - im Repositorium, wo ein neues Pack entsteht.
#
# GRENZE: Eine Anwesenheitspruefung auf den Begleitsatz. Ob der genannte Ersatz taugt,
# kann kein Skript beurteilen - wie bei Pruefung 25 wird erzwungen, dass jemand die Frage
# gestellt und beantwortet hat.
ZUSAGENFELDER_ERSATZ = {
    "permissions": "skill_permissions_ersatz",
    "triggers": "model_invocation_field",
}


def check_zusagenfelder(root: str) -> None:
    """Pruefung 27 (D-50): Kein verworfenes Zusagenfeld ohne benannten Ersatz."""
    basis = os.path.join(root, KERN, "clients")
    if not os.path.isdir(basis):
        return
    for pack in sorted(os.listdir(basis)):
        if pack.startswith("_"):
            continue
        pfad = os.path.join(basis, pack, "manifest.json")
        if not os.path.isfile(pfad):
            continue
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        try:
            man = json.loads(read(pfad))
        except ValueError:
            continue
        fmt = (man.get("skill_frontmatter") or {})
        entfallend = set(fmt.get("drop_fields") or [])
        if fmt.get("tools_format") == "csv":
            entfallend.add("allowed-tools")
        for feld, ersatzfeld in sorted(ZUSAGENFELDER_ERSATZ.items()):
            if feld not in entfallend:
                continue
            if str(fmt.get(ersatzfeld) or "").strip():
                continue
            err(f"{rel}: Das Skill-Frontmatter-Feld '{feld}' traegt eine Zusage und steht "
                f"in skill_frontmatter.drop_fields - es entfaellt damit ersatzlos. Das Pack "
                f"MUSS in skill_frontmatter.{ersatzfeld} benennen, was an seine Stelle "
                f"tritt, oder festhalten, dass es keinen Ersatz gibt und was stattdessen "
                f"traegt. Ein folgenlos verworfenes Feld ist der Befund AP2-CC-01, und bei "
                f"'permissions' war es B01 (D-18, D-50)")


# ---------------------------------------------------------------------------
# Pruefung 41: Eine Abwesenheitserklaerung ist Enthaltung oder Beleg
# ---------------------------------------------------------------------------
#
# ANLASS. D-47 wurde gebaut, damit ein Pack eine Werkzeugklasse nicht dadurch aus der
# Durchsetzung nehmen kann, dass es sie weglaesst: Eine Abwesenheit MUSS erklaert werden.
# Pruefung 26 erzwingt seither, dass die Erklaerung DA ist und mit permission_tools
# widerspruchsfrei. Am 2026-09-14 war beides erfuellt und die Erklaerung trotzdem falsch
# (tests/protocols/2026-09-14-erhebung-devin-werkzeuge.md, CR-2026-065):
# _hook_tools_absent_note sagte "Dieser Client fuehrt kein eigenes Suchwerkzeug" - und der
# Client fuehrt zwei, grep und find_file_by_name. Der erzeugte Hook-Matcher kannte die
# Suchklasse deshalb nicht, und in einer Umgebung mit nur diesem Hook kam derselbe
# Secret-Wert, den ein read-Aufruf nicht bekam, ueber einen grep-Aufruf woertlich heraus.
#
# WAS PRUEFBAR IST. Nicht die Wahrheit einer Aussage - das kann kein Skript. Wohl aber,
# ob die Aussage sich als das ausweist, was sie ist. Zwei Bauformen sind redlich:
#   * die ENTHALTUNG - "UNERHOBEN, nicht abwesend" (agent_start_tools_absent seit D-70);
#   * der BELEG - ein Datum UND eine Fundstelle unter tests/protocols/. Ein
#     blosses Wort wie "gemessen" genuegt nicht - "nicht gemessen" enthaelt es
#     auch, und genau diese Falle stand im Entwurf dieser Pruefung.
# Die dritte Bauform ist die, die hier Schaden angerichtet hat: eine BEHAUPTUNG, die wie
# eine Feststellung klingt und weder das eine noch das andere trägt.
#
# GRENZE. Sie prueft eine FORM, nicht eine Tatsache. Wer ein Datum und einen Protokollpfad
# in die Note schreibt, besteht sie - auch wenn das Protokoll etwas anderes sagt. Und sie
# faengt nach 0.43.0 nichts mehr: Beide Packs sind in Ordnung. Ihr Wert haengt an ihren
# Sonden und daran, dass die naechste Abwesenheitserklaerung nicht mehr unbelegt bleibt.
ABWESENHEITSFELDER = (
    ("hook_tools_absent", "_hook_tools_absent_note", None),
    ("agent_start_tools_absent", "_agent_start_tools_absent_note", None),
    ("tool_names_unmapped", "_tool_names_unmapped_note", FRONTMATTER_BLOECKE),
    ("skill_deny_unmapped", "_skill_deny_unmapped_note", ("skill_frontmatter",)),
)
ENTHALTUNG = re.compile(r"unerhoben", re.I)
DATUM = re.compile(r"\b20\d\d-\d\d-\d\d\b")
FUNDSTELLE = re.compile(r"tests/protocols/")


def _abwesenheitserklaerungen(man: dict):
    """(Feldname, Notizname, Wert, Notiz) je erklaerter Abwesenheit dieses Manifests."""
    for feld, notiz, bloecke in ABWESENHEITSFELDER:
        if bloecke is None:
            wert = man.get(feld)
            if wert:
                yield feld, notiz, wert, man.get(notiz)
            continue
        for block in bloecke:
            fmt = man.get(block) or {}
            wert = fmt.get(feld)
            if wert:
                yield f"{block}.{feld}", f"{block}.{notiz}", wert, fmt.get(notiz)


def check_abwesenheitsbeleg(root: str) -> None:
    """Pruefung 41 (D-88): Eine erklaerte Abwesenheit weist sich aus - oder sie belegt sich."""
    basis = os.path.join(root, KERN, "clients")
    if not os.path.isdir(basis):
        return
    manifeste = 0
    erklaerungen = 0
    for pack in sorted(os.listdir(basis)):
        if pack.startswith("_"):
            continue
        pfad = os.path.join(basis, pack, "manifest.json")
        if not os.path.isfile(pfad):
            continue
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        try:
            man = json.loads(read(pfad))
        except ValueError:
            continue
        manifeste += 1
        for feld, notizname, _wert, notiz in _abwesenheitserklaerungen(man):
            erklaerungen += 1
            text = str(notiz or "").strip()
            if not text:
                continue  # Die Pruefungen 26 und 38 melden die fehlende Notiz bereits
            if ENTHALTUNG.search(text):
                continue
            if DATUM.search(text) and FUNDSTELLE.search(text):
                continue
            err(f"{rel}: {notizname} erklärt eine Abwesenheit, weist sie aber weder als "
                f"Enthaltung aus noch belegt sie sie. Redlich sind zwei Bauformen: das "
                f"Wort 'unerhoben' – oder ein Datum zusammen mit einer Fundstelle "
                f"('tests/protocols/…'). Eine "
                f"Behauptung ohne beides nimmt eine Werkzeugklasse aus der Durchsetzung "
                f"und begründet es – genau so ist am 2026-09-14 der Schutz-Hook um die "
                f"Suchklasse gekommen (D-88)")
    if not manifeste:
        err(f"{KERN}/clients: kein Manifest gefunden. Prüfung 41 misst die "
            f"Abwesenheitserklärungen der Packs; ohne sie prüft sie nichts und bestünde "
            f"leise (D-23)")
        return
    if not erklaerungen:
        err(f"{KERN}/clients: kein Pack führt noch eine Abwesenheitserklärung. Prüfung "
            f"41 hat ihren Gegenstand verloren und würde leise bestehen – fällt das Feld "
            f"weg, gehört die Prüfung ausgebaut und nicht stillgelegt (D-23, D-88)")


# ---------------------------------------------------------------------------
# Pruefung 42: Ein gefuellter Schlitz traegt, was das Overlay erklaert
# ---------------------------------------------------------------------------
#
# ANLASS. Gemessen am 2026-09-14
# (tests/protocols/2026-09-14-gegenpruefung-schlitzdeckung.md, CR-2026-066): Die
# Kernquelle haelt im ask-Korb DREI Befehlsschlitze bereit. Pruefung 37 vergleicht
# Mengen und zaehlt den Ueberschuss gegen die Zahl der offenen Schlitze - WELCHER
# Eintrag WELCHER Schlitz ist, steht dort nicht und kann dort nicht stehen. Gemessen
# laufen deshalb drei beliebige Befehlsfreigaben durch, darunter eine mit Fernwirkung,
# und zwar in beiden Packs und auch dann, wenn das Overlay dreimal <TBD> sagt, also gar
# nichts erklaert. Am Piloten steht der Fall seit dem Heben auf 0.37.0:
# Bash(mvn -B -q compile) im ask-Korb, waehrend Abschnitt 6 <LINT_COMMAND> als "nicht
# vorhanden" erklaert.
#
# DIE LUECKE WAR ERKLAERT - AN EINER STELLE. CR-2026-061 Abschnitt 4 nimmt genau diesen
# Fall ausdruecklich aus, und D-76 wie D-77 bleiben genau. DREI ausgelieferte Texte aus
# DEMSELBEN Commit (34d850e, Release 0.39.0) taten es nicht: der Absatz zum Wirkungsort
# in templates/project-overlay/OVERLAY.md, der Kommentarkopf JEDER erzeugten
# Berechtigungsdatei in clientmap._kommentar und framework/core/03-security.md. Alle drei
# sind mit diesem Release berichtigt. Die Lehre ist die von 0.42.0, eine Ebene tiefer:
# Eine Enthaltung, die nur in einem Antrag steht, haelt nicht einmal bis zum Ende
# desselben Patches.
#
# WOHER DIE ZUORDNUNG KOMMT (CR-2026-066 E1). Es gibt sie genau einmal, im Overlay:
# Jeder der drei Platzhalter steht dort in genau EINER Tabellenzeile, und der Wert steht
# in der Zelle RECHTS DANEBEN - gemessen in allen vier geprueften Overlays, auch im
# Overlay des Piloten, dessen Abschnitt 6 aus einer aelteren Vorlage stammt und eine
# andere Spaltenueberschrift fuehrt. docs/PLACEHOLDER_REGISTRY.md weist die Herkunft
# ohnehin aus (Overlay 5 beziehungsweise Overlay 6); diese Pruefung setzt eine
# Behauptung durch, die das Register seit jeher macht. Die Zeile wird ueber die
# PLATZHALTERZELLE gefunden, nie ueber eine Spaltennummer - ein Overlay, das eine Spalte
# ergaenzt, bricht sie deshalb nicht.
#
# WARUM NICHT DIE LAUFZEITFASSUNG (E2). 20-project-overlay.md fuehrt dieselben drei
# Werte, aber in einer Fliesszeile ohne Schluesselspalte - und der Pilot hat sie bereits
# umgebaut (zwei Zeilen statt einer, ein zusaetzliches Feld). Eine Pruefung darueber
# fiele beim ersten echten Projekt an der FORM, nicht an der Sache.
#
# WARUM EINE EIGENE NUMMER (E6). Pruefung 37 haengt allein an der Kernquelle und laeuft
# ohne Overlay; diese hier enthaelt sich ohne Overlay. Zwei Gegenstaende, zwei Nummern -
# und 37 behaelt ihre Arithmetik, damit ihr Ergebnis nicht von der Anwesenheit eines
# Nachbardokuments abhaengt. Am Piloten meldet 37 deshalb weiterhin nichts, waehrend 42
# meldet.
#
# GRENZE, UND SIE STEHT HIER UND NICHT NUR IM ANTRAG (E5). Geprueft werden die drei
# BEFEHLSSCHLITZE. Die vier PFADSCHLITZE (<EXCLUDED_PATHS> zweimal, <CI_CONFIG_PATHS>,
# <QUALITY_GATE_CONFIG_PATHS>) bleiben ungeprueft: Sie stehen saemtlich im deny-Korb, wo
# Ueberzaehliges ohnehin zulaessig ist, und ihr Vergleich waere n:1 - eine Liste im
# Overlay gegen eine Regel in der Datei. Ein zu ENG gefuellter <EXCLUDED_PATHS>-Schlitz
# ist damit weiterhin eine stille Lockerung. Das ist eine Enthaltung, keine Stille.
#
# ZWEITE GRENZE. Diese Pruefung vergleicht Zeichenketten. Ob der erklaerte Befehl
# fachlich der richtige ist, ob er tut, was Abschnitt 6 von ihm behauptet, und ob ein
# Client die Regel so auswertet, wie sie gemeint ist, sagt sie nicht.
OVERLAY_QUELLE = ".koolie/project-overlay/OVERLAY.md"
# Werte, die kein Befehl sind. Die Schreibweisen stammen aus der Vorlage und aus dem
# Overlay des Piloten; der Vergleich laeuft in Kleinschreibung und ohne umschliessende
# Auszeichnung. Ein Wert mit <TBD faellt ohnehin darunter.
KEIN_BEFEHL = ("nicht vorhanden", "nicht erforderlich", "keine", "keiner", "keines",
               "entfaellt", "entfällt", "nur in ci", "-", "–", "—", "")


def overlay_befehlswert(text: str, platzhalter: str) -> tuple:
    """Wie oft nennt eine Tabellenzeile den Platzhalter, und was steht rechts daneben?

    Rueckgabe (anzahl, wert). wert ist None, wenn die Zelle keinen Befehl traegt - ein
    offener <TBD>-Wert, ein "nicht vorhanden" oder ein Gedankenstrich. Steht in der Zelle
    ein Abschnitt zwischen Gegenstrichen, gilt dieser als der Wert; so ueberlebt die
    Auswertung einen erlaeuternden Zusatz hinter dem Befehl.
    """
    treffer = []
    for felder in _tabellenzeilen(text):
        for i, feld in enumerate(felder):
            if feld.strip("` *") == platzhalter and i + 1 < len(felder):
                treffer.append(felder[i + 1])
    if len(treffer) != 1:
        return len(treffer), None
    zelle = treffer[0]
    ausgezeichnet = re.search(r"`([^`]+)`", zelle)
    wert = (ausgezeichnet.group(1) if ausgezeichnet else zelle).strip(" *")
    if "<TBD" in wert or wert.strip().lower() in KEIN_BEFEHL:
        return 1, None
    return 1, wert


def check_schlitzinhalte(root: str, man: dict) -> None:
    """Pruefung 42 (D-90, D-91): Der Schlitz traegt den Befehl, den das Overlay erklaert.

    Enthaltung ohne Overlay: Eine Installation ohne .koolie/project-overlay/OVERLAY.md ist ein
    zulaessiger Zustand (Kandidatenphase), und eine Pruefung, die ihn beanstandet, waere
    eine Pruefung ueber die Reihenfolge der Uebernahme. Fehlt dagegen ein PLATZHALTER in
    einem vorhandenen Overlay, ist das der verlorene Anker und ein Fehler (D-23).
    """
    if formatgebunden(man, 42):
        return  # D-346, D-416: diese Ausgabeform erreicht die Pruefung nicht
    overlay_pfad = os.path.join(root, ".koolie/project-overlay", "OVERLAY.md")
    rel = man["permissions_file"]
    pfad = os.path.join(root, *rel.split("/"))
    if not os.path.exists(overlay_pfad) or not os.path.exists(pfad):
        return
    try:
        cfg = json.loads(read(pfad))
    except json.JSONDecodeError:
        return  # check_config hat das bereits gemeldet
    soll = soll_korbregeln(root, man)
    if soll is None:
        return
    overlay = read(overlay_pfad)
    perms = cfg.get("permissions", {})
    exec_werkzeuge = tuple(man.get("permission_tools", {}).get("exec", ()))
    if not exec_werkzeuge:
        return  # Ein Pack ohne Befehlswerkzeug hat keine Befehlsschlitze.

    for korb in ("ask", "allow"):
        ist = [r for r in perms.get(korb, []) if isinstance(r, str)]
        _, schlitze, _, zusatz = korb_zerlegung(ist, soll[korb])
        befehlsschlitze = [s for s in schlitze if s.split("(", 1)[0] in exec_werkzeuge]
        if not befehlsschlitze:
            continue
        erklaert: dict = {}
        ohne_befehl: list = []
        for schlitz in befehlsschlitze:
            namen = PROJEKTPLATZHALTER.findall(schlitz)
            if len(namen) != 1:
                continue
            platzhalter = namen[0]
            anzahl, wert = overlay_befehlswert(overlay, platzhalter)
            if anzahl == 0:
                err(f"{OVERLAY_QUELLE}: keine Tabellenzeile nennt {platzhalter} – "
                    f"Prüfung 42 liest dort den Befehl, den dieser Schlitz der "
                    f"Berechtigungsdatei tragen darf, und hat ihren Gegenstand verloren. "
                    f"Der Platzhalter gehört in die Platzhalterspalte von Abschnitt 5 "
                    f"oder 6, der Befehl in die Zelle rechts daneben (D-91)")
                continue
            if anzahl > 1:
                err(f"{OVERLAY_QUELLE}: {anzahl} Tabellenzeilen nennen {platzhalter}. "
                    f"Prüfung 42 braucht genau eine – bei mehreren ist nicht "
                    f"entschieden, welcher Befehl für den Schlitz gilt (D-91)")
                continue
            if wert is None:
                ohne_befehl.append(platzhalter)
                continue  # Kein erklaerter Befehl: Dieser Schlitz deckt nichts.
            regel = schlitz.replace(platzhalter, wert)
            erklaert[regel] = platzhalter
            if regel in ist:
                continue
            if schlitz in ist:
                err(f"{rel}: das Overlay erklärt für {platzhalter} den Befehl "
                    f"'{wert}'; der {korb}-Korb trägt aber noch den offenen Schlitz "
                    f"'{schlitz}'. Entweder wird der Wert dort eingetragen ('{regel}'), "
                    f"oder Abschnitt 5 beziehungsweise 6 nimmt ihn zurück – zwei "
                    f"Träger derselben Freigabe dürfen nicht auseinanderlaufen "
                    f"(D-90)")
            else:
                err(f"{rel}: das Overlay erklärt für {platzhalter} den Befehl "
                    f"'{wert}'; der {korb}-Korb trägt weder '{regel}' noch den offenen "
                    f"Schlitz '{schlitz}'. Eine erklärte Freigabe, die die Datei nicht "
                    f"gewährt, ist eine Abweichung – gleich in welche Richtung sie "
                    f"aufgelöst wird (D-90)")
        for regel in zusatz:
            if regel.split("(", 1)[0] not in exec_werkzeuge:
                continue
            if regel in erklaert:
                continue
            err(f"{rel}: '{regel}' steht im {korb}-Korb, und kein Platzhalter des "
                f"Overlays erklärt diesen Befehl. Ein Platzhalterschlitz darf gefüllt "
                f"sein – aber mit dem Wert, den Abschnitt 5 oder 6 für ihn nennt. Ohne "
                f"erklärten Befehl deckt ein Schlitz keine zusätzliche Freigabe; ohne "
                f"diesen Satz decken drei offene Schlitze drei beliebige Befehle, gemessen "
                f"bis hin zu einem mit Fernwirkung (D-90). Ohne erklärten Befehl sind "
                f"hier: {', '.join(ohne_befehl) if ohne_befehl else 'keiner'}")


# --- Pruefung 54 -------------------------------------------------------------------
# Das Framework liefert die Berechtigungsdatei eines Packs erzeugt aus, und ein Pack darf
# darin Schluessel setzen, die nicht aus der neutralen Regelmenge stammen. Bis 0.61.0 gab
# es dafuer genau ein Feld: permissions_extra - und es landet INNERHALB des
# permissions-Objekts. Fuer einen Schluessel, den der Client auf der obersten Ebene liest,
# war das die falsche Stelle, und es gab keine richtige.
#
# DIE EBENE IST KEINE KOSMETIK. Ein Schluessel an der falschen Stelle wird nicht gelesen,
# die Datei bleibt gueltiges JSON, der Validator meldete nichts - und die Verschaerfung,
# die das Pack auszuliefern glaubt, wirkt nicht. Das ist die Bauform "die Zusage, die mehr
# verspricht als ihr Mechanismus haelt", angewandt auf eine Dateiebene.
#
# ANLASS IST EINE FREMDE MESSUNG, KEINE EIGENE (FW-AK-01, CR-2026-087, 2026-09-18): Beim
# Client des Schwesterpacks ist genau das als CVE-2026-81376 aufgetreten - der Restricted
# Mode setzte eine eingeschraenkte Arbeitsbereichseinstellung in GEPUNKTETER Schreibweise
# durch und dieselbe Einstellung in VERSCHACHTELTER Form nicht. Behoben in 3.10.31 vom
# 2026-09-16; die verbindliche Zielspanne des Packs devin-desktop (3.9.x) liegt
# vollstaendig davor. Dieselbe Regel, zwei Ausdrucksformen, durchgesetzt nur in einer -
# die Bauform von Pruefung 51, diesmal im Produkt statt im eigenen Bestand.
#
# WAS SIE NICHT LEISTET: Sie prueft, ob ein DEKLARIERTER Schluessel ankommt, nicht ob er
# der richtige ist. Ob autoMemoryEnabled der Schluessel ist, den dieser Client liest, sagt
# die Herstellerdokumentation - und dafuer gibt es FW-AK-01, nicht den Validator.
P54_FELDER = ("settings_extra", "permissions_extra")


def check_zusatzschluessel(root: str, man: dict) -> None:
    """Pruefung 54 (D-155): Deklarierte Zusatzschluessel stehen auf ihrer Ebene."""
    if formatgebunden(man, 54):
        return  # D-346, D-416: diese Ausgabeform erreicht die Pruefung nicht
    rel = man.get("permissions_file")
    if not rel:
        return
    pfad = os.path.join(root, *rel.split("/"))
    if not os.path.isfile(pfad):
        return
    try:
        cfg = json.loads(read(pfad))
    except json.JSONDecodeError:
        return  # Pruefung 3 meldet das bereits; hier waere es eine zweite Meldung
    if not isinstance(cfg, dict):
        return
    pack = man.get("client", "?")
    for feld in P54_FELDER:
        erklaert = man.get(feld)
        if erklaert is None:
            err(f"clients/{pack}/manifest.json: Feld {feld} fehlt. Ein Pack führt "
                f"beide Felder, notfalls leer - der Unterschied zwischen „nicht "
                f"abgebildet“ und „gibt es nicht“ gehört "
                f"deklariert und nicht aus einem fehlenden Feld erraten (D-155)")
            continue
        if not isinstance(erklaert, dict):
            err(f"clients/{pack}/manifest.json: Feld {feld} ist kein Objekt (D-155)")
            continue
        eigen = cfg if feld == "settings_extra" else cfg.get("permissions", {})
        fremd = cfg.get("permissions", {}) if feld == "settings_extra" else cfg
        ebene = ("der obersten Ebene" if feld == "settings_extra"
                 else "dem Objekt permissions")
        gegen = ("dem Objekt permissions" if feld == "settings_extra"
                 else "der obersten Ebene")
        if not isinstance(eigen, dict):
            continue
        for schluessel, wert in erklaert.items():
            if schluessel in eigen:
                if eigen[schluessel] != wert:
                    err(f"{rel}: Schlüssel „{schluessel}“ trägt "
                        f"{json.dumps(eigen[schluessel], ensure_ascii=False)}, das "
                        f"Manifest deklariert in {feld} aber "
                        f"{json.dumps(wert, ensure_ascii=False)} (D-155)")
                continue
            if isinstance(fremd, dict) and schluessel in fremd:
                err(f"{rel}: Schlüssel „{schluessel}“ steht in {gegen} "
                    f"statt in {ebene}. Das Manifest deklariert ihn in {feld}; auf der "
                    f"falschen Ebene wird er stillschweigend nicht gelesen (D-155)")
                continue
            err(f"{rel}: Schlüssel „{schluessel}“ aus {feld} fehlt in "
                f"{ebene}. Das Pack liefert eine Verschärfung aus, die in der "
                f"erzeugten Datei nicht ankommt (D-155)")


# --- Pruefung 74: Eine Matrixzeile steht in ihrer Tabelle ---------------------------
#
# ANLASS, UND ER STAND 73 RELEASES DA (gemessen 2026-09-22, D-264). Das Pack
# devin-desktop fuehrt sieben Modus-Zeilen. Zwischen M5 und M6 stand eine LEERZEILE -
# seit 0.26.0, dem Release, das M6 und M7 ueberhaupt erst angelegt hat, weil AP2-DD-03
# gefunden hatte, dass zwei geregelte Modi keine Matrixzeile haben. Die Abhilfe gab
# ihnen eine Zeile, die KEINE Tabellenzeile ist: Nach einer Leerzeile beginnt in
# Markdown ein neuer Block, und ein Block aus "| M6 | ... |" ohne Kopf- und Trennzeile
# ist ein Absatz. Beide Zeilen erscheinen im Hauptdokument als Fliesstext mit Strichen.
#
# UND DIE BUCHFUEHRUNG ZAEHLT SIE MIT: Die Zusammenfassung desselben Packs fuehrt
# "20 von 36" - 36 ist die Zeilenzahl EINSCHLIESSLICH M6 und M7. Die Zahl stimmte, die
# Tabelle zeigte sie nicht. Das ist der wiederkehrende Befundtyp mit umgekehrtem
# Vorzeichen: nicht der Text verspricht mehr als der Mechanismus haelt, sondern die
# Buchfuehrung sagt etwas ueber eine Zeile, die der Leser gar nicht als Zeile sieht.
#
# WARUM EINE EIGENE PRUEFUNG UND NICHT EIN TEIL VON 73. Der Gegenstand ist ein anderer:
# 73 fragt, WAS in einer Zeile steht, 74 fragt, ob sie ueberhaupt eine ist. Eine
# gebrochene Tabelle laesst 73 unberuehrt - sie liest die Zeile weiterhin, weil sie sie
# am Muster erkennt und nicht am Block. Genau deshalb hat 73 Releases lang niemand
# etwas gemerkt.
P74_TRENNZEILE_RE = re.compile(r"^\|\s*:?-{3,}")


def check_matrixzeile_in_tabelle(root: str) -> None:
    """Pruefung 74 (D-264): Jede Matrixzeile steht in ihrer Tabelle."""
    if P74_TRENNZEILE_RE.match("| M6 | synthetisch |"):
        err("Pruefung 74: das eigene Muster haelt eine Datenzeile fuer eine "
            "Trennzeile - sie meldete nichts mehr und bestuende leise (D-23)")
        return
    verz = os.path.join(root, KERN, "clients")
    if not os.path.isdir(verz):
        return
    packs = sorted(n for n in os.listdir(verz)
                   if os.path.isfile(os.path.join(verz, n, "CLIENT_PACK.md")))
    if not packs:
        err(f"{KERN}/clients/: kein Client Pack mit CLIENT_PACK.md - Pruefung 74 "
            f"haette keinen Gegenstand (D-23)")
        return
    for pack in packs:
        rel = f"clients/{pack}/CLIENT_PACK.md"
        zeilen = read(os.path.join(verz, pack, "CLIENT_PACK.md")) \
            .replace("\r\n", "\n").split("\n")
        drin = False
        for i, zeile in enumerate(zeilen):
            if zeile.startswith("## 2. "):
                drin = True
                continue
            if drin and re.match(r"^## \d", zeile):
                drin = False
            if not drin or not P73_ZEILE_RE.match(zeile):
                continue
            # Rueckwaerts bis zur Trennzeile - ohne Leerzeile und ohne Fremdzeile.
            j, getragen = i - 1, False
            while j >= 0:
                vor = zeilen[j].strip()
                if not vor or not vor.startswith("|"):
                    break
                if P74_TRENNZEILE_RE.match(vor):
                    getragen = True
                    break
                j -= 1
            if not getragen:
                kennung = P73_ZEILE_RE.match(zeile).group(1)
                err(f"{rel}:{i + 1}: Zeile {kennung} sieht aus wie eine Matrixzeile "
                    f"und steht in keiner Tabelle - zwischen ihr und der Trennzeile "
                    f"liegt eine Leerzeile oder Fremdtext. Markdown rendert sie als "
                    f"Absatz mit Strichen, im Pack wie im Hauptdokument, waehrend die "
                    f"Zusammenfassung desselben Packs sie mitzaehlt (D-264)")


# Pruefung 84: die Vorlage ist keine Client Pack (CR-2026-131, D-336)
# ---------------------------------------------------------------------------
#
# ANLASS, GEMESSEN MIT EINEM PROBEMANIFEST UND WIEDER ENTFERNT. `clients/README.md`
# Abschnitt 5 Schritt 1 sagt "`_template/` nach `<client-name>/` kopieren", Schritt 5
# sagt "`manifest.json` anlegen", und Abschnitt 3 sagt "Ohne Manifest ist ein Pack nicht
# installierbar". Die Vorlage traegt EINES VON DREI Bestandteilen.
#
# 🔴 UND SIE STEHT IN DER PACKMENGE DES PRUEFAPPARATS. `_client_packs()` nimmt jedes
# Verzeichnis unter `clients/` auf, das eine CLIENT_PACK.md traegt - `_template` erfuellt
# das. Der Docstring der Funktion hielt die Annahme fest, die sie trug: "_template ohne
# Manifest".
#
# GEMESSEN am 2026-09-23: Ein Probemanifest angelegt (eine Kopie des Manifests von
# `claude-code`, also eines, das einen FREMDEN Client beschreibt), Validator gefahren,
# Probemanifest entfernt. `_client_packs()` lieferte drei Packs MIT Manifest, und der
# Validator meldete 0 Fehler, 0 Warnungen.
# ➡️ EINE VORLAGE, DIE NUR DESHALB KEINE PRUEFUNG AUSLOEST, WEIL IHR EIN BESTANDTEIL
# FEHLT, IST NICHT AUSGENOMMEN - SIE IST UNVOLLSTAENDIG. Und der Tag, an dem jemand sie
# nach der eigenen Anleitung vervollstaendigt, ist der Tag, an dem sie geprueft wird,
# ohne dass es jemand entschieden hat.
#
# 🔴 DIE BAUFORM "ZWEI STELLEN, DIE EINANDER DECKEN" (0.57.0): Die unvollstaendige
# Vorlage verhindert, dass die fehlende Ausnahme je auffaellt. Einzeln waere jede
# aufgefallen; zusammen sahen sie aus wie ein Lauf ohne Befund.
#
# ⚠️ UND DIE AUSNAHME EXISTIERTE BEREITS - AN ZWEI ANDEREN STELLEN. Pruefung 73 schliesst
# `_template` ausdruecklich aus, und LINK_PATH_EXCEPTIONS fuehrt den Pfad mit Begruendung.
# Der zentrale Iterator tat es nicht.
# ➡️ WER EINE AUSNAHME AN ZWEI STELLEN FUEHRT UND AN DER DRITTEN VERGISST, HAT SIE NICHT
# VERGESSEN - ER HAT KEINE STELLE, AN DER SIE STEHT. Seit D-336 steht sie in
# `_client_packs()`, also dort, wo die Packmenge ENTSTEHT.
#
# ZUSCHNITT: Diese Pruefung haelt fest, was die Ausnahme voraussetzt - dass die Vorlage
# eine Vorlage BLEIBT. Traegt sie die Bestandteile eines vollstaendigen Packs, ist
# entweder die Ausnahme falsch oder die Vorlage ein Pack; beides gehoert entschieden und
# nicht stillschweigend gefahren.
#
# 🔴 GRENZE, BENANNT: Sie prueft die ANWESENHEIT von Bestandteilen, nicht deren Inhalt.
# Eine `CLIENT_PACK.md`, die einen echten Client beschreibt statt Platzhalter zu fuehren,
# kommt durch - das faengt Pruefung 7 ueber die Markerform.
P84_VORLAGE = "_template"
P84_VERBOTEN = ("manifest.json", "root-template")


def check_vorlage_kein_pack(root: str) -> None:
    """Pruefung 84 (D-336): Die Client-Pack-Vorlage traegt keine Packbestandteile."""
    vdir = os.path.join(root, KERN, "clients", P84_VORLAGE)
    if not os.path.isdir(vdir):
        err(f"{KERN}/clients/{P84_VORLAGE}/: fehlt. `clients/README.md` Abschnitt 5 "
            f"Schritt 1 baut jedes neue Client Pack aus ihr, und `_client_packs()` "
            f"nimmt sie seit D-336 ausdruecklich NICHT auf - ohne den Gegenstand "
            f"bestuende Pruefung 84 leise (D-23, D-336)")
        return
    if not os.path.isfile(os.path.join(vdir, "CLIENT_PACK.md")):
        err(f"{KERN}/clients/{P84_VORLAGE}/CLIENT_PACK.md: fehlt. Sie ist der einzige "
            f"Bestandteil, den die Vorlage traegt (D-336)")
    for name in P84_VERBOTEN:
        pfad = os.path.join(vdir, name)
        if not os.path.exists(pfad):
            continue
        err(f"{KERN}/clients/{P84_VORLAGE}/{name}: die Vorlage traegt einen Bestandteil, "
            f"den nur ein vollstaendiges Client Pack traegt. `_client_packs()` nimmt "
            f"`{P84_VORLAGE}` seit D-336 nicht auf - damit liefe dieser Bestandteil "
            f"ungeprueft mit, waehrend er in jedem echten Pack geprueft wird. Gemessen "
            f"am 2026-09-23 mit einem Probemanifest: alle Pruefungen blieben gruen. "
            f"Entweder ist die Ausnahme falsch oder die Vorlage ein Pack - beides "
            f"gehoert entschieden (D-336)")


# ---------------------------------------------------------------------------
# PRUEFUNG 87: DIE FORMATGEBUNDENEN PRUEFUNGEN STEHEN IM PACK
# ---------------------------------------------------------------------------
# ANLASS (CR-2026-133, D-346). Mit dem dritten Client Pack gibt es zum ersten Mal zwei
# Ausgabeformen der Berechtigungsdatei. Zwoelf Pruefungen lesen die eine; fuer die
# andere haben sie keinen Gegenstand. Sie still zu ueberspringen, waere die Bauform von
# 0.57.0 - "zwei Stellen, die einander decken": Der Validator liefe gruen, und niemand
# wuesste, dass sechs Pruefungen dieses Pack nicht erreichen.
#   ➡️ Eine Luecke, die erklaert ist, ist eine Aussage; eine, die nur besteht, ist ein
#      blinder Fleck.
# Diese Pruefung verlangt deshalb: Ein Pack mit einer anderen Ausgabeform nennt in
# Abschnitt 5 seines CLIENT_PACK.md JEDE Nummer aus FORMATGEBUNDENE_PRUEFUNGEN - und
# keine Nummer mehr, die dort nicht steht.
# ⚠️ GRENZE, BENANNT: Sie prueft die NENNUNG, nicht die Richtigkeit der Begruendung -
#    dieselbe Bauform wie Pruefung 19. Und sie haengt daran, dass jemand eine neu
#    guardete Pruefung in die Menge eintraegt; die Funktion `formatgebunden` erzwingt
#    das, indem sie eine unbekannte Nummer als Fehler wirft.
def check_formatgebundene_pruefungen(root: str) -> None:
    """Pruefung 87 (D-346): Ein Pack mit eigener Ausgabeform nennt die Pruefungen,
    die es damit nicht erreichen."""
    packs = os.path.join(root, KERN, "clients")
    if not os.path.isdir(packs):
        return
    for name in sorted(os.listdir(packs)):
        mf = os.path.join(packs, name, "manifest.json")
        if not os.path.exists(mf):
            continue
        try:
            man = json.loads(read(mf))
        except (OSError, ValueError):
            continue
        if man.get("permissions_format", "json") == "json":
            continue
        pack = os.path.join(packs, name, "CLIENT_PACK.md")
        if not os.path.exists(pack):
            continue
        text = read(pack)
        abschnitt = re.split(r"^## 5\.", text, maxsplit=1, flags=re.M)
        if len(abschnitt) < 2:
            err(f"{KERN}/clients/{name}/CLIENT_PACK.md: Abschnitt 5 fehlt; dort gehört "
                f"die Liste der Prüfungen, die dieses Pack wegen seiner Ausgabeform "
                f"'{man['permissions_format']}' nicht erreichen (D-346)")
            continue
        rumpf = re.split(r"^## 6\.", abschnitt[1], maxsplit=1, flags=re.M)[0]
        genannt = {int(n) for n in re.findall(r"Prüfung\s+(\d+)", rumpf)}
        erwartet = nicht_erreicht(man)
        fehlend = sorted(erwartet - genannt)
        if fehlend:
            err(f"{KERN}/clients/{name}/CLIENT_PACK.md Abschnitt 5: die Prüfung(en) "
                f"{', '.join(str(n) for n in fehlend)} sind an die Ausgabeform 'json' "
                f"gebunden und erreichen dieses Pack nicht – der Abschnitt nennt sie "
                f"nicht. Eine Lücke, die nirgends steht, ist ein blinder Fleck (D-346)")
        # Gegenrichtung, seit 1.13.0 je Form (D-416): Genannt werden darf nur, was
        # DIESE Form nicht erreicht - auch eine Nummer der Menge, die das Pack doch
        # erreicht, ist eine behauptete Luecke.
        zuviel = sorted(genannt - erwartet)
        if zuviel:
            err(f"{KERN}/clients/{name}/CLIENT_PACK.md Abschnitt 5: die Prüfung(en) "
                f"{', '.join(str(n) for n in zuviel)} werden als formatgebunden "
                f"genannt, erreichen die Ausgabeform '{man['permissions_format']}' "
                f"aber (FORMATGEBUNDENE_PRUEFUNGEN). Eine behauptete Lücke, die es nicht "
                f"gibt, ist so falsch wie eine verschwiegene (D-346, D-416)")
