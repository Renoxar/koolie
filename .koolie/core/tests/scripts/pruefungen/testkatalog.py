"""Testkatalog und Testblaetter: K3-Kategorien, Grenzfaelle, Praeparationsregister,
Skillaufruf, Pruefmittel, Skillversion, Nummernverweise, Ausgabemarken, Ergebnisstatus,
Belegquelle, Aenderungsart und Ergebnisstand.

Pruefungen 29, 30, 44, 49, 61, 62, 63, 64, 65, 73, 95 und 103. Teil des Validators
validate-framework.py, seit 1.19.1 nach Gegenstand in Module geteilt (K-174). Das
Register aller Pruefungen steht im Kopfkommentar des Einstiegs, die Grenze jeder
einzelnen in ihrem Kopfkommentar hier."""
from __future__ import annotations

import os
import re

from .gemeinsam import (
    _client_packs, _tabellenspalte, _ueb_katalogdateien, err, iter_text_files, KERN,
    NEUTRAL_CHRONIK, NEUTRAL_CHRONIK_BASENAMES, NEUTRAL_DOKUMENT, P73_ZEILE_RE, read,
    skill_dirs, tabellenzellen, TBD_RE, warn)


# Pruefung 29: Kurzform und Langform fuehren dieselben K3-Kategorien, unbedingt.
#
# Die Kategorien aus Abschnitt 2.1 sind ebenenfest (D-52). Zwei Fehlerbilder sind moeglich
# und beide sind vorgekommen: eine Kategorie fehlt in einer Fassung - die Kurzform, die in
# jede Sitzung laedt, fuehrte bis 0.31.0 nur sechs von acht -, oder eine Kategorie traegt
# eine Bedingung, wie die interne Adresse, die "sofern nicht im Overlay als K1 eingestuft"
# ausgenommen war. Beides prueft diese Funktion an denselben fuenf Traegern.
K3_KATEGORIEN = (
    ("Secrets und Zugangsdaten", r"Secret|Zugangsdaten"),
    ("personenbezogene Echtdaten", r"personenbezogene Echtdaten"),
    ("Produktionsdaten", r"Produktionsdaten"),
    ("Kunden- und Behördendokumente", r"Behörden"),
    ("Sicherheitskonfigurationen", r"Sicherheitskonfiguration"),
    ("interne Adressen und Umgebungskennungen", r"interne[nr]? Adressen"),
    ("als vertraulich eingestufte Inhalte", r"vertraulich"),
    ("Inhalte anderer Projekte", r"anderer Projekte|anderen Projekten|Fremdprojekte"),
)

# Eine Bedingung in einer unbedingten Liste. "es sei denn" stand in Abschnitt 2.2.
K3_BEDINGUNG_RE = re.compile(
    r"sofern nicht|sofern es nicht|es sei denn|außer wenn|soweit nicht|sofern kein", re.I)

# Je Traeger: Pfad, Startanker, Endanker (None = bis Zeilenende des Startankers).
K3_TRAEGER = (
    (KERN + "/framework/core/02-privacy.md", "### 2.1 Immer K3", "### 2.2"),
    (KERN + "/framework/runtime/root-instruction.md", "- Immer K3", None),
    (KERN + "/framework/runtime/rules/10-privacy-security.md", "| K3 |", None),
    (KERN + "/decision-trees/01-context-allowed.md", "1. **K3-Prüfung:**", "\n2. "),
    (KERN + "/checklists/02-privacy-context.md", "K3-Kategorien geprüft", None),
)


def check_k3_kategorien(root: str) -> None:
    """Pruefung 29 (D-52): Dieselbe K3-Liste in jeder Fassung, ohne Bedingung.

    Belegt Uebereinstimmung der Kategorien, nicht die Gleichheit der Formulierungen - eine
    Kurzform darf kuerzer sein, aber keine Kategorie weglassen und keine an eine Bedingung
    binden. Was die Pruefung nicht leistet: Sie sieht nicht, ob ein KI-Client die Liste
    auch anwendet. Das ist FW-KO-05, ein Dokumentenreview ueber die Fassungen
    (.koolie/core/tests/EDGE_CASES.md); ob ein KI-Client die Liste anwendet, misst
    kein Testfall des Katalogs - das ist K-60 (D-148).
    """
    for rel, start, ende in K3_TRAEGER:
        pfad = os.path.join(root, rel.replace("/", os.sep))
        if not os.path.isfile(pfad):
            err(f"{rel}: fehlt - diese Datei fuehrt die K3-Kategorien und wird gegen die "
                f"uebrigen Fassungen geprueft (D-52)")
            continue
        text = read(pfad).replace("\r\n", "\n")
        pos = text.find(start)
        if pos < 0:
            err(f"{rel}: Der Anker '{start}' ist nicht mehr auffindbar. Ohne ihn prueft "
                f"diese Pruefung nichts - sie wuerde leise bestehen (D-23)")
            continue
        if ende:
            bis = text.find(ende, pos + len(start))
            bereich = text[pos:bis if bis > 0 else len(text)]
        else:
            bis = text.find("\n", pos)
            bereich = text[pos:bis if bis > 0 else len(text)]
        for name, muster in K3_KATEGORIEN:
            if not re.search(muster, bereich):
                err(f"{rel}: Die K3-Liste nennt die Kategorie '{name}' nicht. Alle acht "
                    f"Kategorien aus Abschnitt 2.1 von "
                    f"{KERN}/framework/core/02-privacy.md gelten in jeder Fassung; eine "
                    f"Kurzform darf kuerzer formulieren, aber keine Kategorie weglassen "
                    f"(D-52)")
        m = K3_BEDINGUNG_RE.search(bereich)
        if m:
            err(f"{rel}: Die K3-Liste traegt eine Bedingung ('{m.group(0)}'). Die "
                f"Kategorien sind unbedingt und ebenenfest - kein Overlay, keine "
                f"Datenschutzpruefung und kein Ausnahmeprozess kann sie freigeben "
                f"(governance/PRIORITY_HIERARCHY.md Regel 2.4, D-52)")


# Pruefung 30: Die Grenzfalltabelle ist vollstaendig und deckt jede Entscheidung ab.
#
# Das Abnahmekriterium des Reviews zu B07 und B09 verlangt Beispiele mit erwarteter
# Entscheidung. Eine Tabelle, in der eine Spalte leer bleibt oder eine Entscheidung
# unbelegt ist, sieht aus wie ein Nachweis und ist keiner. Die Anzahl steht im Steckbrief
# und wird nachgezaehlt: In diesem Projekt war eine Zahl schon oefter zu klein.
GRENZFALL_DATEI = KERN + "/tests/EDGE_CASES.md"
GRENZFALL_SPALTEN = 7
GRENZFALL_ENTSCHEIDUNGEN = ("D-52", "D-53", "D-54", "D-55", "D-56", "D-59",
                            "D-61", "D-63", "D-64", "D-66", "D-67", "D-72")


def check_grenzfaelle(root: str) -> None:
    """Pruefung 30: Vollstaendigkeit der Grenzfalltabelle (CR-2026-052, CR-2026-053)."""
    pfad = os.path.join(root, GRENZFALL_DATEI.replace("/", os.sep))
    if not os.path.isfile(pfad):
        err(f"{GRENZFALL_DATEI}: fehlt. Die entschiedenen Regelkonflikte brauchen ihre "
            f"Grenzfaelle als Referenz - das ist das Abnahmekriterium des Reviews zu B07 "
            f"und B09")
        return
    text = read(pfad)
    m = re.search(r"\|\s*Anzahl der Grenzfälle\s*\|\s*(\d+)\s*\|", text)
    if not m:
        err(f"{GRENZFALL_DATEI}: Der Steckbrief nennt keine Anzahl der Grenzfaelle. Ohne "
            f"sie faellt eine geloeschte Zeile nicht auf")
        return
    erwartet = int(m.group(1))
    zeilen = [z for z in text.splitlines() if re.match(r"\|\s*G-\d+\s*\|", z)]
    if len(zeilen) != erwartet:
        err(f"{GRENZFALL_DATEI}: {len(zeilen)} Grenzfallzeilen, der Steckbrief nennt "
            f"{erwartet}. Eine Zahl, die nicht stimmt, ist kein Nachweis")
    for zeile in zeilen:
        zellen = tabellenzellen(zeile)
        kennung = zellen[0] if zellen else "?"
        if len(zellen) != GRENZFALL_SPALTEN:
            err(f"{GRENZFALL_DATEI}: Grenzfall {kennung} hat {len(zellen)} Spalten statt "
                f"{GRENZFALL_SPALTEN} (Nr., Grenzfall, Entscheidung, Betriebsmodus, "
                f"Kontrollstufe, Rollen, Fundstelle)")
            continue
        for nr, zelle in enumerate(zellen, 1):
            if not zelle or zelle in ("-", "–"):
                err(f"{GRENZFALL_DATEI}: Grenzfall {kennung}, Spalte {nr} ist leer. Jede "
                    f"Spalte ist Teil der Einstufung; eine leere Spalte laesst offen, was "
                    f"gilt")
            if TBD_RE.search(zelle):
                err(f"{GRENZFALL_DATEI}: Grenzfall {kennung}, Spalte {nr} traegt einen "
                    f"offenen <TBD>-Wert. Ein Grenzfall ohne Entscheidung ist keiner")
    for d in GRENZFALL_ENTSCHEIDUNGEN:
        if not any(d in z for z in zeilen):
            err(f"{GRENZFALL_DATEI}: Keine Grenzfallzeile verweist auf {d}. Jede "
                f"entschiedene Auslegungsfrage braucht mindestens einen Grenzfall, sonst "
                f"ist das Abnahmekriterium des Reviews nicht eingeloest")


# ---------------------------------------------------------------------------
# Pruefung 44: Das Register der Uebungspraeparationen und die Vorbedingungen des
# Testkatalogs decken sich
# ---------------------------------------------------------------------------
#
# ANLASS. Gemessen am 2026-09-14 (CR-2026-067, Befund 2): onboarding/exercises/README.md
# verlangte DREI Koeder. Abgezaehlt gegen die Vorbedingungen des Testkatalogs braucht ein
# fahrbares Uebungsrepositorium SIEBEN Praeparationen fuer NEUN Testfaelle - dazu eine
# .env-Testdatei (FW-DS-02), einen praeparierten Codekommentar (FW-PI-02), eine Injektion
# in einer Testdatei (SK-006-N04) und einen Regeltext mit bewusstem Widerspruch
# (FW-KO-03). Keine der vier stand in der Liste, und der Katalog fuehrte alle neun Faelle
# als 'offen', also als fahrbar. EINE ZUSAGE OHNE DEN MECHANISMUS DAHINTER - der
# wiederkehrende Befundtyp dieses Projekts, diesmal an seinem eigenen Pruefstand.
#
# WIE DIE ZUORDNUNG ENTSTEHT (E5). Jede Praeparation traegt eine Kennung UEB-NN. Sie steht
# im Register in der ersten Spalte und in der Vorbedingungszelle jedes Testfalls, der sie
# braucht. Der Vergleich laeuft ueber die Kennung und ist damit exakt - nicht ueber
# Stichwoerter wie "Koeder" oder "praepariert", die Pruefung 29 als Bauform schon einmal
# teuer bezahlt hat: Sie erkennt nur bekannte Bedingungswoerter.
#
# WARUM UEB- UND NICHT P1 (E5). P1 und P3 sind im Kern als Prinzipienkennungen vergeben
# (framework/core/05-working-model.md). Eine zweite Bedeutung desselben Zeichens in
# derselben Dokumentfamilie ist ein Fehler, den dieses Projekt schon gemacht hat: Am
# 2026-09-13 trug eine Gegenprobe die synthetische Kennung G-18 - dieselbe, die 0.36.0
# wirklich vergeben hat.
#
# BEIDE RICHTUNGEN (E6). Eine Kennung im Katalog ohne Registereintrag ist ein Tippfehler
# oder eine unregistrierte Praeparation; eine Kennung im Register, die kein Testfall
# braucht, ist eine tote Praeparation, die jemand pflegt. Die dezentralen TESTS.md zaehlen
# mit - Verfahren Nr. 6 des Katalogs erklaert sie zu seinem Teil.
#
# GRENZE, UND SIE IST DIE WICHTIGE. Diese Pruefung faengt NICHT den Fall, der sie
# ausgeloest hat: einen Testfall, der eine Praeparation braucht und keine Kennung nennt.
# Sie verhindert seine WIEDERHOLUNG nur, soweit die Kennung gesetzt wird - dieselbe
# Ehrlichkeit wie Gegenstand 2 von Pruefung 38 (er zaehlt Deklarationen, nicht
# Richtigkeit) und wie Pruefung 40 (sie zaehlt Nennungen, nicht Pruefungen).
#
# ZWEITE GRENZE. Sie gleicht zwei Register ab, nicht ein Register gegen die Wirklichkeit.
# Ob die Praeparation UEB-02 im Uebungsrepositorium wirklich liegt, kann kein Validator
# DIESES Repositoriums feststellen: Das Uebungsrepositorium liegt ausserhalb. Das ist eine
# Enthaltung, keine Stille.
UEB_REGISTER = "onboarding/exercises/README.md"
UEB_ANKER = "### Register der Präparationen"
UEB_KENNUNG = re.compile(r"\bUEB-\d{2}\b")
# Gegenstand 3 (D-131). Die Spalte wird ueber ihre UEBERSCHRIFT gefunden, nicht ueber
# ihre Nummer: Eine Erkennungsregel fuer eine Dokumentstruktur gehoert an die Stellung,
# nicht an eine Zaehlung, die die naechste eingeschobene Spalte verschiebt.
UEB_BELEGSPALTE = "Wie sie belegt ist"
# Gegenstand 4 (D-173). Die Spalten werden ueber ihre UEBERSCHRIFT gefunden, die
# Testfallspalte des Registers ist die LETZTE. Der Zuschnitt trennt die Vorbedingung
# von ihrer Geschichte am ersten Vermerkzeichen: Was davor steht, ist die Bedingung;
# was dahinter steht, ist ihre Herkunft. FW-NE-02 nennt UEB-06 hinter dem Vermerk
# ("UEB-08 verdraengt UEB-06"), ohne es zu verlangen - wer die ganze Zelle liest,
# meldet diese Zeile mit.
UEB_VORBEDINGUNGSSPALTE = "Vorbedingung"
UEB_VERMERK_RE = re.compile("[\U0001F534\U0001F7E2\U0001F195⚠]")
UEB_FALL_RE = re.compile(r"\b(?:FW|SK|RE)-[A-Z0-9-]+\b")


def _vor_dem_vermerk(zelle: str) -> str:
    """Der Teil einer Tabellenzelle vor dem ersten Vermerkzeichen."""
    treffer = UEB_VERMERK_RE.search(zelle)
    return zelle[:treffer.start()] if treffer else zelle


def _ueb_gebraucht_je_vorbedingung(root: str) -> dict:
    """{UEB-NN: {Testfallkennung}} - nur aus der Vorbedingungsspalte, vor dem Vermerk."""
    raus: dict = {}
    for rel in _ueb_katalogdateien(root):
        pfad = os.path.join(root, *rel.split(os.sep))
        if not os.path.exists(pfad):
            continue
        i_vb = -1
        for zeile in read(pfad).splitlines():
            if not zeile.lstrip().startswith("|"):
                continue
            if UEB_VORBEDINGUNGSSPALTE in zeile and "Prüfmethode" in zeile:
                i_vb = _tabellenspalte(zeile, UEB_VORBEDINGUNGSSPALTE)
                continue
            if i_vb < 0:
                continue
            zellen = tabellenzellen(zeile)
            if len(zellen) <= i_vb:
                continue
            fall = UEB_FALL_RE.match(zellen[0].strip("`* "))
            if not fall:
                continue
            for kennung in UEB_KENNUNG.findall(_vor_dem_vermerk(zellen[i_vb])):
                raus.setdefault(kennung, set()).add(fall.group(0))
    return raus


def check_praeparationsregister(root: str) -> None:
    """Pruefung 44 (D-93): Registrierte Praeparationen und gebrauchte decken sich."""
    pfad = os.path.join(root, KERN, *UEB_REGISTER.split("/"))
    if not os.path.exists(pfad):
        err(f"{KERN}/{UEB_REGISTER}: fehlt. Prüfung 44 hält dort das Register der "
            f"Übungspräparationen gegen die Vorbedingungen des Testkatalogs (D-93)")
        return
    text = read(pfad)
    if UEB_ANKER not in text:
        err(f"{KERN}/{UEB_REGISTER}: führt kein Register mehr (gesucht: "
            f"'{UEB_ANKER}'). Prüfung 44 hat ihren Gegenstand verloren und bestünde "
            f"sonst leise – die Überschrift ist Teil des Nachweises (D-23, D-93)")
        return
    registriert = set(UEB_KENNUNG.findall(text.split(UEB_ANKER, 1)[1]))
    if not registriert:
        err(f"{KERN}/{UEB_REGISTER}: das Register führt keine einzige Kennung der Form "
            f"UEB-NN – Prüfung 44 hätte nichts zu vergleichen (D-93)")
        return

    gebraucht: dict = {}
    for rel in _ueb_katalogdateien(root):
        pfad_k = os.path.join(root, *rel.split(os.sep))
        if not os.path.exists(pfad_k):
            continue
        for kennung in UEB_KENNUNG.findall(read(pfad_k)):
            gebraucht.setdefault(kennung, set()).add(rel.replace(os.sep, "/"))

    for kennung in sorted(set(gebraucht) - registriert):
        stellen = ", ".join(sorted(gebraucht[kennung]))
        err(f"{stellen}: nennt die Präparation {kennung}, die das Register in "
            f"{KERN}/{UEB_REGISTER} nicht führt. Eine Vorbedingung, die auf eine "
            f"unregistrierte Präparation zeigt, ist eine Zusage ohne den Mechanismus "
            f"dahinter – der Testfall gilt als fahrbar, und niemand weiß, was "
            f"herzustellen ist (D-93)")
    for kennung in sorted(registriert - set(gebraucht)):
        err(f"{KERN}/{UEB_REGISTER}: führt die Präparation {kennung}, die kein Testfall "
            f"nennt – weder der Testkatalog noch ein dezentrales Testblatt. Eine "
            f"Präparation, die niemand braucht, wird gepflegt und nicht benutzt; "
            f"entweder trägt ein Testfall sie in seine Vorbedingung ein, oder sie fällt "
            f"aus dem Register (D-93)")

    # --- Gegenstand 4: die zeilenweise Deckung (D-173) ------------------------------
    # Gegenstand 1 und 2 vergleichen MENGEN ueber die ganze Datei. Sie bestehen auch
    # dann, wenn die Kennung in der Ergebniszelle statt in der Vorbedingung steht -
    # und dann sagt genau die Spalte, die dem Laufenden sagt, was herzustellen ist,
    # es nicht. 0.64.0 hat fuenfzehn Blattzellen hergerichtet und die Kennung dreimal
    # nur in den gruenen Vermerk der Ergebniszelle geschrieben; die Gegenrichtung
    # fehlte zweimal, und das vollstaendigere Register lag AUSSERHALB des
    # Repositoriums (im Mentorenblatt des Uebungsrepositoriums).
    zeilen_reg = [z for z in text.split(UEB_ANKER, 1)[1].split("\n")
                  if z.strip().startswith("|")]
    gebraucht_vb = _ueb_gebraucht_je_vorbedingung(root)
    for zeile in zeilen_reg:
        zellen = tabellenzellen(zeile)
        treffer = UEB_KENNUNG.findall(zellen[0]) if zellen else []
        if not treffer:
            continue
        kennung = treffer[0]
        genannt = set(UEB_FALL_RE.findall(zellen[-1])) if len(zellen) > 1 else set()
        misst = gebraucht_vb.get(kennung, set())
        for fall in sorted(genannt - misst):
            err(f"{KERN}/{UEB_REGISTER}: die Zeile {kennung} nennt den Testfall {fall}, "
                f"dessen Vorbedingungszelle {kennung} nicht führt. Die Spalte, die sagt, "
                f"was vor dem Lauf herzustellen ist, sagt es damit nicht – eine Nennung "
                f"in der Ergebniszelle erreicht den Laufenden zu spät (D-93, D-173)")
        for fall in sorted(misst - genannt):
            err(f"{KERN}/{UEB_REGISTER}: der Testfall {fall} nennt {kennung} in seiner "
                f"Vorbedingung, die Registerzeile {kennung} führt ihn aber nicht. Ein "
                f"Register, das seinen Gegenstand nicht führt, ist eine Auswahl – und "
                f"sie ist immer zu klein, nie zu groß (D-93, D-173)")

    # --- Gegenstand 3: die Belegzelle (D-131) --------------------------------------
    # UEB-06 stand dreizehn Releases lang im Register und stellte seinen Gegenstand
    # nicht her. Der Eintrag behauptete, der Testbefehl gebe die Anweisung aus; gemessen
    # hat das niemand, und er tut es nicht. Ein Vorhandensein belegt sich selbst, ein
    # Fehlen nicht - und eine Praeparation, deren Gegenstand erst durch einen Lauf
    # entsteht, ist ein Fehlen, solange niemand den Lauf gefahren hat.
    zeilen = [z for z in text.split(UEB_ANKER, 1)[1].split("\n") if z.strip().startswith("|")]
    kopf = next((z for z in zeilen if UEB_BELEGSPALTE in z), None)
    if kopf is None:
        err(f"{KERN}/{UEB_REGISTER}: die Registertabelle führt keine Spalte "
            f"'{UEB_BELEGSPALTE}'. Gegenstand 3 der Prüfung 44 hat seinen Anker verloren "
            f"und bestünde sonst leise – die Spaltenüberschrift ist Teil des Nachweises "
            f"(D-23, D-131)")
        return
    spalte = tabellenzellen(kopf).index(UEB_BELEGSPALTE)
    for zeile in zeilen:
        zellen = tabellenzellen(zeile)
        treffer = UEB_KENNUNG.findall(zellen[0]) if zellen else []
        if not treffer:
            continue
        if len(zellen) <= spalte or not zellen[spalte]:
            err(f"{KERN}/{UEB_REGISTER}: die Zeile {treffer[0]} führt keine Belegzelle "
                f"('{UEB_BELEGSPALTE}'). Ein Registereintrag ohne Beleg ist eine Zusage "
                f"über einen Mechanismus, den niemand ausgeführt hat – genau der Fall "
                f"von UEB-06, der dreizehn Releases lang einen Testfall unfahrbar "
                f"gehalten hat (D-131)")



# --- Pruefung 49 -------------------------------------------------------------------
# Die Marken stammen aus den Skillquellen des Kerns, nicht aus einer gepflegten Liste.
# 'triggers' ist ein Kernbegriff; die Abbildung auf das Clientfeld leistet install.py
# (bei claude-code 'disable-model-invocation'). Diese Pruefung fragt nach der QUELLE,
# damit sie unabhaengig vom installierten Pack dasselbe sagt.
SKILL_TRIGGER_RE = re.compile(r"^triggers:\s*$(.*?)(?=^\S|\Z)", re.M | re.S)


def _skills_ohne_modellaufruf(root: str) -> list:
    """Namen der Kernskills, deren Quelle 'triggers' ohne '- model' fuehrt, sortiert.

    Ein solcher Skill ist nur ueber den ausdruecklichen Aufruf einer Person erreichbar;
    das Modell darf ihn nicht von sich aus waehlen. Gemessen am 2026-09-18: neun von
    zwoelf (CR-2026-085, D-146).
    """
    namen = []
    for basis in (os.path.join(root, KERN, "framework", "skills"),):
        if not os.path.isdir(basis):
            continue
        for name in sorted(os.listdir(basis)):
            pfad = os.path.join(basis, name, "SKILL.md")
            if not os.path.isfile(pfad):
                continue
            text = read(pfad)
            if not text.startswith("---"):
                continue
            ende = text.find("---", 3)
            if ende < 0:
                continue
            m = SKILL_TRIGGER_RE.search(text[3:ende])
            if m and "- model" not in m.group(1):
                namen.append(name)
    return namen


# Gegenstand 2 (D-172). Die Uebungen und ihre Skills stammen aus der Uebungsdatei,
# nicht aus einer gepflegten Liste: Wer eine Uebung um einen Schritt erweitert, soll
# nicht daran denken muessen, eine Liste im Validator nachzuziehen.
P49_UEBUNGSDATEI = KERN + "/onboarding/exercises/EXERCISES.md"
P49_UEBUNG_RE = re.compile("Ü\\d[a-z]?")
P49_UEBUNG_KOPF_RE = re.compile(r"^##\s+(Ü\d)\b")


def _uebungsskills(root: str) -> dict:
    """{UEn: [Skillnamen]} - abgeleitet aus den Abschnitten der Uebungsdatei.

    Gelesen werden die Skillaufrufe der Form /name im Abschnitt einer Uebung. Die
    Uebungsdatei schreibt sie durchgaengig so - sie beschreibt den Ablauf, den eine
    PERSON geht, und genau das ist der Grund, aus dem ein Ausloeser, der sich auf sie
    beruft, den Aufruf nicht verschweigen darf.
    """
    pfad = os.path.join(root, *P49_UEBUNGSDATEI.split("/"))
    if not os.path.isfile(pfad):
        err(f"{P49_UEBUNGSDATEI}: fehlt. Gegenstand 2 der Prüfung 49 leitet die Skills "
            f"jeder Übung von dort ab und hat seinen Gegenstand verloren; er bestünde "
            f"sonst leise (D-23, D-172)")
        return {}
    raus: dict = {}
    aktuell = None
    for zeile in read(pfad).splitlines():
        kopf = P49_UEBUNG_KOPF_RE.match(zeile.strip())
        if kopf:
            aktuell = kopf.group(1)
            raus.setdefault(aktuell, [])
            continue
        if aktuell is None:
            continue
        for treffer in re.findall(r"/(koolie-[a-z0-9-]+)", zeile):
            if treffer not in raus[aktuell]:
                raus[aktuell].append(treffer)
    if not raus:
        err(f"{P49_UEBUNGSDATEI}: führt keinen Abschnitt der Form '## Ü<n> …'. "
            f"Gegenstand 2 der Prüfung 49 hat seinen Anker verloren und bestünde sonst "
            f"leise (D-23, D-172)")
    return raus


def check_skillaufruf_im_katalog(root: str) -> None:
    """Pruefung 49 (D-146): Ein nicht modellaufrufbarer Skill steht als /name im Ausloeser."""
    namen = _skills_ohne_modellaufruf(root)
    if not namen:
        err(f"{KERN}/framework/skills/: kein Skill mit 'triggers' ohne '- model' gefunden – "
            f"Prüfung 49 leitet ihre Marken daraus ab und hat ihren Gegenstand verloren; "
            f"sie bestünde sonst leise (D-23)")
        return
    uebungsskills = _uebungsskills(root)
    alle_skills = sorted({s for liste in uebungsskills.values() for s in liste} | set(namen))
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
        i_ein = i_pm = -1
        for nr, zeile in enumerate(read(pfad).splitlines(), 1):
            if not zeile.lstrip().startswith("|"):
                continue
            if "Prüfmethode" in zeile and "Eingabe" in zeile:
                i_ein = _tabellenspalte(zeile, "Eingabe")
                i_pm = _tabellenspalte(zeile, "Prüfmethode")
                continue
            if i_ein < 0 or i_pm < 0:
                continue
            zellen = [z.strip() for z in zeile.strip().strip("|").split("|")]
            if len(zellen) <= max(i_ein, i_pm):
                continue
            if "sitzung" not in zellen[i_pm]:
                continue
            ausloeser = zellen[i_ein]
            for skill in namen:
                # Nur die nackte Nennung ist ein Befund: '/name' ist der Aufruf selbst.
                for m in re.finditer(r"(?<![/\w-])" + re.escape(skill) + r"(?![\w-])", ausloeser):
                    err(f"{rel}:{nr}: Der Auslöser nennt '{skill}' ohne den ausdrücklichen "
                        f"Aufruf. Die Quelle des Skills führt 'triggers' ohne '- model' – "
                        f"das Modell darf ihn nicht von sich aus wählen, und ein "
                        f"nicht-interaktiver Lauf bekommt eine Abweisung statt des Ablaufs. "
                        f"Schreibe '/{skill}' (D-146)")
                    break
            # --- Gegenstand 2 (D-172): der Ausloeser, der eine UEBUNG nennt ---------
            # Er nennt keinen Skill und erbt doch welche. FW-PO-02 verweist auf UE3,
            # und UE3 geht durch vier Skills, die das Modell nicht waehlen darf.
            # SCHMAL, und das ist Absicht: Gefragt wird, ob UEBERHAUPT ein
            # ausdruecklicher Aufruf dasteht - nicht, ob es der richtige oder ob es
            # alle sind. FW-SC-01 nennt UE3 und ruft bewusst nur deren dritten Schritt
            # auf; eine Pruefung kann Zuschnitt nicht von Vergesslichkeit
            # unterscheiden. Der erste Entwurf haette FW-SC-01 dreimal gemeldet.
            # Ein ausdruecklicher Aufruf ist '/<skillname>', nicht irgendein Schraegstrich:
            # Der Ausloeser von FW-PO-02 nennt einen PFAD, und der erste Entwurf hat
            # '/onboarding' fuer einen Aufruf gehalten und nichts gemeldet.
            if any(f"/{s}" in ausloeser for s in alle_skills):
                continue
            # Ue6c ist ein Teil von Ue6 - die Abschnittsueberschrift traegt nur die
            # Ziffer, der Verweis zusaetzlich einen Buchstaben.
            for uebung in sorted({t[:2] for t in P49_UEBUNG_RE.findall(ausloeser)}):
                geerbt = sorted(set(uebungsskills.get(uebung, ())) & set(namen))
                if not geerbt:
                    continue
                err(f"{rel}:{nr}: Der Auslöser nennt die Übung {uebung} und damit "
                    f"deren Ablauf, der durch {', '.join(geerbt)} geht – Skills, deren "
                    f"Quelle 'triggers' ohne '- model' führt. Der Auslöser enthält "
                    f"keinen einzigen ausdrücklichen Aufruf; ein nicht-interaktiver "
                    f"Lauf bekommt eine Abweisung statt des Ablaufs. Nenne den "
                    f"Einstiegsschritt als '/name' (D-172)")


# --- Pruefung 103: der Stand einer Ergebniszelle (CR-2026-160, D-472, K-61) --------------
# ANLASS, GEMESSEN am 2026-09-18: FW-KO-02 stand seit dem 10.09. auf 'bestanden', und drei
# der vier Befunde, die FW-KO-05 danach fand, lagen genau in seinem Gegenstand - entstanden
# NACH der Abnahme. Der Testfall war nicht falsch; sein Belegstand war veraltet, und nichts
# meldete es.
#
# DIE FORM: Eine Ergebniszelle kann ihren Stand tragen - '[Stand: ' + zwoelf Hexziffern +
# '; ' + die Pfade ihres Gegenstands relativ zum Kern, durch Komma getrennt + ']'. Der Wert
# ist sha256 ueber Pfad und Inhalt jeder Datei in der genannten Reihenfolge, Zeilenenden auf
# LF gebracht; der Messapparat schreibt ihn beim Eintragen (tests/erhebungen/apparat).
#
# WAS SIE LEISTET: Weicht der Gegenstand vom Stand ab, WARNT sie - eine Aenderung ist kein
# Fehler, sie verlangt eine Entscheidung (neu erheben oder den Stand bestaetigen). Nennt die
# Marke einen Pfad, den es nicht gibt, ist das ein FEHLER: ein Stand ohne Gegenstand belegt
# nichts. WAS SIE NICHT LEISTET: Eine Zelle ohne Marke bleibt ungeprueft; der Altbestand
# traegt keine, und ihn mit geratenen Gegenstaenden nachzutragen saehe wie ein Beleg aus.
P103_MARKE_RE = re.compile(r"\[Stand: ([0-9a-f]{12}); ([^\]]+)\]")


def stand_wert(kern: str, pfade: list) -> str | None:
    """Der Stand ueber die Dateien eines Gegenstands - None, wenn eine fehlt."""
    import hashlib
    h = hashlib.sha256()
    for pfad in pfade:
        voll = os.path.join(kern, *pfad.split("/"))
        if not os.path.isfile(voll):
            return None
        with open(voll, "rb") as fh:
            inhalt = fh.read().replace(b"\r\n", b"\n")
        h.update(pfad.encode("utf-8") + b"\n" + inhalt + b"\n")
    return h.hexdigest()[:12]


def _p103_traeger(root: str) -> list:
    kern = os.path.join(root, KERN)
    dateien = [os.path.join(kern, "tests", "TEST_CATALOG.md")]
    for basis in (os.path.join(kern, "framework", "skills"),
                  os.path.join(kern, "framework", "role-packs")):
        for wurzel, _, files in os.walk(basis):
            if "TESTS.md" in files:
                dateien.append(os.path.join(wurzel, "TESTS.md"))
    return [d for d in sorted(dateien) if os.path.exists(d)]


def check_ergebnisstand(root: str) -> None:
    """Pruefung 103 (D-472): der Stand einer Ergebniszelle gegen ihren heutigen Gegenstand."""
    kern = os.path.join(root, KERN)
    for pfad in _p103_traeger(root):
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        for nr, zeile in enumerate(read(pfad).splitlines(), 1):
            for m in P103_MARKE_RE.finditer(zeile):
                gegenstand = [p.strip().strip("`") for p in m.group(2).split(",") if p.strip()]
                wert = stand_wert(kern, gegenstand)
                if wert is None:
                    err(f"{rel}:{nr}: die Standmarke nennt einen Gegenstand, den es nicht gibt "
                        f"({', '.join(gegenstand)}) – ein Stand ohne Gegenstand belegt nichts (D-472)")
                elif wert != m.group(1):
                    warn(f"{rel}:{nr}: Belegstand veraltet – der Gegenstand "
                         f"({', '.join(gegenstand)}) hat sich seit der Messung geändert "
                         f"(Stand {m.group(1)}, heute {wert}); neu erheben oder den Stand "
                         f"bestätigen (D-472, K-61)")


# --- Pruefung 61: Das Pruefmittelwort stammt aus dem Vokabular ----------------------
#
# ANLASS (D-181). Die dreizehn Testblaetter fuehrten bis 0.67.0 das Wort `manuell` -
# 87 von 87 Zellen. Im Vokabular von TEST_CATALOG.md Punkt 3 steht es nicht; es ist das
# ADJEKTIV aus der Definition von `sitzung` ("manuelle KI-Testsitzung nach Testblatt"),
# zum Methodennamen befoerdert. Jedes Blatt erklaerte es in seinem eigenen Vorspann -
# und damit war es fuer jeden Leser richtig und fuer jeden Zaehler unsichtbar.
#
# WAS DAS GEKOSTET HAT, IST GEMESSEN. Zwei Pruefungen laufen ausdruecklich ueber die
# dreizehn Blaetter und filtern auf `sitzung`: Pruefung 49 (D-146, seit 0.60.0) und
# Pruefung 60 (D-178, seit 0.66.0). Beide hatten dort NULL Gegenstand. Nach der
# Umstellung meldete Pruefung 60 beim ersten Lauf ZWANZIG Zellen - in genau den drei
# Blaettern, deren Skill einen Befehl ausfuehrt (koolie-change-small, koolie-refactor, koolie-tests).
# Das ist die Bauform "Die Regel als Ausfuellschlitz" (0.61.0) eine Ebene hoeher: Nicht
# die Regel stand in zwei Ausdrucksformen, sondern ihr GEGENSTAND.
#
# GRENZE, UND SIE STEHT HIER. Geprueft wird das ERSTE WORT der Zelle gegen eine feste
# Menge. Ein Zusatz dahinter bleibt zulaessig - der zentrale Katalog fuehrt
# "sitzung + `validate-output.py`" und "skript+sitzung", die Blaetter
# "sitzung + Skript `validate-output.py --skill ...`". Nicht geprueft wird, ob das Wort
# das RICHTIGE ist; die Pruefung faengt ein fremdes Vokabular, nicht einen Irrtum.
P61_VOKABULAR = ("skript", "sitzung", "review")


def check_pruefmittel_vokabular(root: str) -> None:
    """Pruefung 61 (D-181): Das Pruefmittelwort stammt aus dem Vokabular des Katalogs."""
    dateien = [os.path.join(root, KERN, "tests", "TEST_CATALOG.md")]
    for basis in (os.path.join(root, KERN, "framework", "skills"),
                  os.path.join(root, KERN, "framework", "role-packs")):
        for wurzel, _, files in os.walk(basis):
            if "TESTS.md" in files:
                dateien.append(os.path.join(wurzel, "TESTS.md"))
    gesehen = 0
    for pfad in sorted(dateien):
        if not os.path.isfile(pfad):
            continue
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        i_pm = -1
        for nr, zeile in enumerate(read(pfad).splitlines(), 1):
            if not zeile.lstrip().startswith("|"):
                continue
            if "Prüfmethode" in zeile and "Eingabe" in zeile:
                i_pm = _tabellenspalte(zeile, "Prüfmethode")
                continue
            if i_pm < 0:
                continue
            zellen = [z.strip() for z in zeile.strip().strip("|").split("|")]
            if len(zellen) <= i_pm or not zellen[0]:
                continue
            if set(zellen[0]) <= set("-:"):
                continue
            wert = zellen[i_pm]
            if not wert:
                continue
            gesehen += 1
            # Das erste Wort, abgeschnitten an Leerzeichen und am Pluszeichen.
            kopf = wert.split(" ")[0].split("+")[0].strip()
            if kopf in P61_VOKABULAR:
                continue
            err(f"{rel}:{nr}: Prüfmittel '{kopf}' steht nicht im Vokabular "
                f"({', '.join(P61_VOKABULAR)}). Zwei Prüfungen filtern auf `sitzung` und "
                f"verlieren mit einem fremden Wort ihren Gegenstand, ohne es zu melden "
                f"(D-146, D-178, D-181)")
    if gesehen == 0:
        err(f"{KERN}/tests/: keine Zelle mit Prüfmethode gefunden – Prüfung 61 hat ihren "
            f"Gegenstand verloren; sie bestünde sonst leise (D-23)")


# --- Pruefung 62: die Version der Ausgabevorlage (D-185) ---------------------------
#
# ANLASS. Der erste Buendellauf der Testblaetter (0.68.0) hat elf Sitzungslaeufe
# gefahren; einer davon meldete in einer Nebenbemerkung, die Attributtabelle seines
# Skills nenne Version 0.1.3 und der Kopf der Ausgabevorlage v0.1.1 - er hat die
# hoehere genommen und es dazugeschrieben. Nachgezaehlt: 13 Traeger mit woertlicher
# Version, 10 davon abweichend, 15 Fundstellen.
#
# DER ZUSCHNITT IST DIE GANZE DATEI, nicht nur Abschnitt 5. Die zweite Fundstelle
# zweier Skills steht in der Zeile "| Erstellt mit | <skill> vX.Y.Z |" - derselbe
# Fehler an einer Stelle, die ein Zuschnitt auf die Ueberschrift verfehlt haette.
# Die Steckbriefzeile selbst traegt ihre Version OHNE das fuehrende `v` und faellt
# deshalb nicht unter das Muster; sie ist die Quelle, nicht die Kopie.
def check_skillversion_vorlage(root: str) -> None:
    """Pruefung 62 (D-185): Keine SKILL.md nennt eine Version woertlich."""
    dateien = []
    for basis in (os.path.join(root, KERN, "framework", "skills"),
                  os.path.join(root, KERN, "framework", "role-packs")):
        for wurzel, _, files in os.walk(basis):
            if "SKILL.md" in files:
                dateien.append(os.path.join(wurzel, "SKILL.md"))
    gesehen = 0
    for pfad in sorted(dateien):
        gesehen += 1
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        text = read(pfad)
        for nr, zeile in enumerate(text.splitlines(), 1):
            for treffer in re.finditer(r"\bv\d+\.\d+\.\d+\b", zeile):
                err(f"{rel}:{nr}: nennt die Version wörtlich ({treffer.group(0)}). Eine "
                    f"Zahl, die gepflegt werden muss, wird nicht gepflegt – gemessen "
                    f"waren zehn von dreizehn Trägern von ihrem eigenen Steckbrief "
                    f"abgewichen. Die Vorlage verweist auf den Steckbrief (D-185)")
    if gesehen == 0:
        err(f"{KERN}/framework/: keine SKILL.md gefunden – Prüfung 62 hat ihren "
            f"Gegenstand verloren; sie bestünde sonst leise (D-23)")


# --- Pruefung 63: der Nummernverweis, der ins Leere zeigt (D-193) ------------------
#
# ANLASS. Der Vorbedingungsdurchgang von Buendel 2 (0.70.0) hat die achtzehn Zellen
# gegen den Bestand gehalten. Drei davon erwarten eine Bereinigung "nach
# 02-privacy.md Abschnitt 3.3" - und Abschnitt 3 jener Datei fuehrte zehn nummerierte
# REGELN und keine einzige Unterueberschrift. Nachgezaehlt gegen den unberuehrten
# Vorstand: 30 Verweise in 15 anweisenden Traegern auf vier Nummern (1.3, 3.3, 3.4,
# 3.5), die es als Abschnitt nicht gab.
#
# DIE FORM HATTE IN DERSELBEN DATEI ZWEI BEDEUTUNGEN. `Abschnitt 2.1` zeigte auf eine
# Ueberschrift, `Abschnitt 3.3` auf eine Listennummer, und 05-working-model.md fuehrt
# seine Querschnittsregeln laengst als `### 3.1` bis `### 3.6`. Das ZIELMODUL war der
# Ausreisser, nicht die dreissig Verweise: 0.70.0 hat die Ueberschriften nachgezogen
# und keinen der fuenfzehn Traeger angefasst. Eine Marke mit zwei Bedeutungen taugt
# weder als Bedingung noch als Entlastung.
#
# ZWEI AUSDRUCKSFORMEN, UND DIE ERSTE ZAEHLUNG KANNTE NUR EINE. Vier Testblaetter
# nennen das Ziel als blossen Dateinamen (`02-privacy.md`), nicht mit vollem Pfad -
# wer nur den vollen Pfad sucht, zaehlt 25 statt 30. Ein blosser Dateiname wird
# aufgeloest, wenn er im Kern GENAU EINMAL vorkommt; bei mehreren Treffern
# (README.md, TESTS.md, SKILL.md) wird nicht geraten.
#
# EINE bis-SPANNE IST MEHR ALS IHRE ENDEN. "Abschnitt 3.3 bis 3.5" nennt auch 3.4;
# wer nur die genannten Zahlen prueft, uebersieht die Mitte.
#
# AUFZEICHNUNGEN SIND AUSGENOMMEN (D-141), und die Liste dafuer ist keine neue:
# NEUTRAL_CHRONIK und NEUTRAL_FRIST. Ein Protokoll nennt den Stand seines Tages, und
# ein Aenderungsantrag den Gegenstand seines Eingriffs; beide nachtraeglich zu
# glaetten, zerstoerte die Nachvollziehbarkeit.
P63_VERWEIS = re.compile(
    r"`(?P<pfad>[A-Za-z0-9_./-]*\.md)`[^`\n]{0,90}?Abschnitt\s+"
    r"(?P<nummern>\d+(?:\.\d+)?(?:\s*(?:und|bis|,)\s*\d+(?:\.\d+)?)*)")
P63_UEBERSCHRIFT = re.compile(r"^#{2,6}\s+(\d+(?:\.\d+)*)\.?\s", re.M)
P63_AUSNAHMEN = NEUTRAL_CHRONIK + NEUTRAL_DOKUMENT


def _p63_nummern(roh: str) -> list:
    """Die genannten Nummern, bis-Spannen innerhalb desselben Abschnitts aufgeloest."""
    teile = re.split(r"\s*(und|bis|,)\s*", roh)
    werte, i = [teile[0]], 1
    while i + 1 < len(teile):
        verbinder, naechste = teile[i], teile[i + 1]
        a, b = werte[-1].split("."), naechste.split(".")
        if verbinder == "bis" and len(a) == 2 and len(b) == 2 and a[0] == b[0] \
                and int(b[1]) > int(a[1]):
            werte += ["%s.%d" % (a[0], k) for k in range(int(a[1]) + 1, int(b[1]) + 1)]
        else:
            werte.append(naechste)
        i += 2
    return werte


def check_nummernverweis(root: str) -> None:
    """Pruefung 63 (D-193): Ein Nummernverweis zeigt auf eine Ueberschrift des Ziels."""
    kopf: dict = {}
    nach_name: dict = {}
    for path in iter_text_files(root):
        if not path.endswith(".md"):
            continue
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if not rel.startswith(KERN + "/"):
            continue
        nach_name.setdefault(os.path.basename(rel), []).append(rel)
        kopf[rel] = {m.group(1) for m in P63_UEBERSCHRIFT.finditer(read(path))}
    if not kopf:
        err(f"{KERN}/: keine Markdown-Traeger gefunden - Pruefung 63 hat ihren "
            f"Gegenstand verloren; sie bestuende sonst leise (D-23)")
        return
    for rel in sorted(kopf):
        if rel.startswith(P63_AUSNAHMEN) or os.path.basename(rel) in NEUTRAL_CHRONIK_BASENAMES:
            continue
        pfad = os.path.join(root, rel.replace("/", os.sep))
        for i, zeile in enumerate(read(pfad).splitlines(), 1):
            for m in P63_VERWEIS.finditer(zeile):
                genannt = m.group("pfad")
                if genannt.startswith(KERN + "/"):
                    ziel = genannt if genannt in kopf else None
                else:
                    kandidaten = nach_name.get(os.path.basename(genannt), [])
                    ziel = kandidaten[0] if len(kandidaten) == 1 else None
                if ziel is None:
                    continue
                for num in _p63_nummern(m.group("nummern")):
                    if num in kopf[ziel]:
                        continue
                    err(f"{rel}:{i}: verweist auf '{ziel}' Abschnitt {num} - diese "
                        f"Nummer fuehrt dort keine Ueberschrift. Ein Nummernverweis "
                        f"zeigt auf einen Abschnitt, nicht auf eine Listennummer; "
                        f"dieselbe Form bedeutete in 02-privacy.md einmal das eine und "
                        f"einmal das andere, und dreissig Verweise in fuenfzehn "
                        f"anweisenden Traegern zeigten ins Leere (D-193)")


# --- Pruefung 64: Die Ausgabemarke, die der Skill nicht verlangt --------------------
#
# ANLASS (D-197). `K-74` hat am 2026-09-19 gezaehlt, dass `[HALT]` und `[RUECKFRAGE]`
# mit 145 Fundstellen im Kern stehen und in keinem Glossar erklaert sind. Die
# Entscheidung dazu hat einen groesseren Befund freigelegt, und zwar durch eine
# Frage, die die Zaehlung nicht gestellt hatte: In WELCHEM Abschnitt steht die Marke?
#
#     `[RUECKFRAGE]` steht in KEINEM Abschnitt 5 und in KEINEM Abschnitt 6 der
#     zwoelf Skills. Sie ist durchgehend HANDLUNGSMARKE - "Fall X | [RUECKFRAGE]"
#     heisst `frage zurueck`, nicht `schreibe die Zeichenfolge`.
#
# `[HALT]` ist beides, je nach Skill: Ausgabemarke in `koolie-plan`, `koolie-bugfix-prepare`
# und `koolie-change-small` (Abschnitt 5 UND 6), Handlungsmarke in den uebrigen neun.
# Und wo sie Abnahmekriterium ist, sagt Abschnitt 6 "ist ERKENNBAR", nicht "woertlich".
#
# GEMESSEN HAT ES EIN LAUF. `sk004n01` (Buendel 2, 2026-09-19) schrieb `[HALT]`
# woertlich - Abschnitt 6 von `koolie-plan` sagt "der Skill endet mit [HALT]" - und
# `[RUECKFRAGE]` nicht. Der Lauf hat sich richtig verhalten; die Zelle verlangte mehr,
# als ihr Skill vorschreibt. Ueber alle dreizehn Blaetter: 18 Nennungen in 17 Zellen
# ungedeckt, 10 gedeckt.
#
# GEGENSTAND. Nennt die Spalte "Erwartetes Verhalten" oder "Unzulaessiges Verhalten"
# einer Zelle eine Ausgabemarke, fuehrt der im Ausloeser aufgerufene Skill sie in
# Abschnitt 5 (Ausgabeformat) oder Abschnitt 6 (Qualitaetskriterien).
#
# WARUM ABSCHNITT 5 UND 6 UND NICHT 3 ODER 7. Abschnitt 3 (Arbeitsschritte) und
# Abschnitt 7 (Fehlerbehandlung) sagen, WAS ZU TUN IST; Abschnitt 5 und 6 sagen, WAS
# IN DER ANTWORT STEHEN MUSS. Ein Zuschnitt ueber die ganze Datei haette jede Zelle
# durchgelassen und nichts gemessen - die Marke steht ja irgendwo in jedem Skill.
# Das ist die Trennlinie von Pruefung 60 an einer zweiten Stelle: Dort sagt das
# FRONTMATTER, was der Skill tut, und der Fliesstext, wovon er redet.
#
# GRENZE, UND SIE STEHT HIER. Geprueft wird die DECKUNG, nicht die Formulierung.
# Eine Zelle, die die Sache umschreibt und dabei etwas Falsches sagt, laeuft durch.
# ZWEITE GRENZE: Die LETZTE Zelle einer Zeile ist der Ergebnisstatus und damit eine
# Aufzeichnung (D-117, D-141) - ein Lauf, der die Marke geschrieben HAT, darf das
# dort berichten. Dieselbe Spalten-Ausnahme, die Pruefung 48 zieht.
P64_MARKEN = {
    "[HALT]": re.compile(r"\[HALT\]"),
    "[RÜCKFRAGE]": re.compile(r"\[R(?:Ü|UE)CKFRAGE\]"),
}


def _p64_skillabschnitte(root: str) -> dict:
    """Skillname -> Menge der Marken, die Abschnitt 5 oder 6 seiner SKILL.md fuehrt.

    Abgeleitet aus den Skillquellen, nicht gepflegt (dieselbe Regel wie bei
    Pruefung 60 und 48): Wer eine Marke in ein Ausgabeformat aufnimmt, soll nicht
    daran denken muessen, eine Liste im Validator nachzuziehen.
    """
    raus = {}
    for basis in (os.path.join(root, KERN, "framework", "skills"),
                  os.path.join(root, KERN, "framework", "role-packs")):
        if not os.path.isdir(basis):
            continue
        for wurzel, _, files in os.walk(basis):
            if "SKILL.md" not in files:
                continue
            text = read(os.path.join(wurzel, "SKILL.md")).replace("\r\n", "\n")
            rumpf, aktuell = [], None
            for zeile in text.split("\n"):
                m = re.match(r"^##\s+(\d+)\.\s", zeile)
                if m:
                    aktuell = int(m.group(1))
                elif aktuell in (5, 6):
                    rumpf.append(zeile)
            gefuehrt = {n for n, mu in P64_MARKEN.items() if mu.search("\n".join(rumpf))}
            raus[os.path.basename(wurzel)] = gefuehrt
    return raus


def check_ausgabemarke_gedeckt(root: str) -> None:
    """Pruefung 64 (D-197): Die Zelle verlangt nur, was ihr Skill als Ausgabe fuehrt."""
    skills = _p64_skillabschnitte(root)
    if not any(skills.values()):
        err(f"{KERN}/framework/skills/: keine SKILL.md fuehrt eine Ausgabemarke in "
            f"Abschnitt 5 oder 6 - Pruefung 64 leitet ihren Gegenstand daraus ab und "
            f"hat ihn verloren; sie bestuende sonst leise (D-23)")
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
        i_ein = i_erw = i_unz = -1
        for nr, zeile in enumerate(read(pfad).splitlines(), 1):
            if not zeile.lstrip().startswith("|"):
                continue
            if "Erwartetes Verhalten" in zeile and "Eingabe" in zeile:
                i_ein = _tabellenspalte(zeile, "Eingabe")
                i_erw = _tabellenspalte(zeile, "Erwartetes Verhalten")
                i_unz = _tabellenspalte(zeile, "Unzulässiges Verhalten")
                continue
            if min(i_ein, i_erw, i_unz) < 0:
                continue
            zellen = [z.strip() for z in zeile.strip().strip("|").split("|")]
            if len(zellen) <= max(i_ein, i_erw, i_unz):
                continue
            # Die letzte Zelle ist der Ergebnisstatus - eine Aufzeichnung (D-117)
            pruefbar = " ".join(z for i, z in enumerate(zellen)
                               if i in (i_erw, i_unz) and i != len(zellen) - 1)
            gefuehrt = set()
            for skill, marken in skills.items():
                if f"/{skill}" in zellen[i_ein]:
                    gefuehrt |= marken
            for name, muster in P64_MARKEN.items():
                if muster.search(pruefbar) and name not in gefuehrt:
                    err(f"{rel}:{nr}: verlangt die Ausgabemarke {name}, die der "
                        f"aufgerufene Skill weder im Ausgabeformat (Abschnitt 5) noch "
                        f"in den Qualitaetskriterien (Abschnitt 6) fuehrt. Dort steht "
                        f"sie als Anweisung, nicht als Ausgabe - die Zelle verlangt "
                        f"damit mehr, als der Skill vorschreibt, und ein Lauf, der "
                        f"anhaelt ohne die Zeichenfolge zu schreiben, faellt zu "
                        f"Unrecht durch (D-197). Die Sache statt der Marke verlangen "
                        f"- oder die Marke in Abschnitt 5 beziehungsweise 6 aufnehmen")

# --- Pruefung 65: Der Ergebnisstatus ohne Beleg -------------------------------------
#
# ANLASS. TEST_CATALOG.md Punkt 4 sagt: "Ein Ergebnisstatus ausser `offen` MUSS auf ein
# Protokoll verweisen." D-117 sagt: "Ein Ergebnisstatus nennt das gemessene Client Pack
# und dessen Produktversion." Beides steht normativ da - und KEINE der vierundsechzig
# Pruefungen setzte es durch. Gezaehlt am 2026-09-19 ueber alle 125 Ergebniszellen des
# zentralen Katalogs und der dreizehn Testblaetter: NULL Verstoesse. Die Regel trug
# bisher allein durch die Sorgfalt derer, die sie eingetragen haben.
#
# WARUM SIE IN EINEM RELEASE GEBAUT WIRD, IN DEM SIE NICHTS FINDET. Dieses Release
# traegt in einem Zug ACHTZEHN neue `bestanden` ein - der Zeitpunkt, an dem eine
# ungezaehlte Belegpflicht rutscht. Die Bewegung ist die Umkehrung von Pruefung 60:
# Dort hatte eine Pruefung zwei Releases lang keinen Gegenstand und meldete dann zwanzig
# Zellen; hier ist der Gegenstand vollstaendig und soll es bleiben.
#
# DREI GEGENSTAENDE:
#   (a) Das Statuswort stammt aus dem Vokabular von Punkt 4 - ABGELEITET aus jener
#       Zeile, nicht gepflegt (dieselbe Regel wie bei Pruefung 61, 64 und 48).
#   (b) Ein Status ausser `offen` nennt ein Protokoll unter tests/protocols/.
#   (c) Ein Status ausser `offen` nennt bei Pruefmethode `sitzung` ein Client Pack mit
#       Produktversion. Die Packkennungen kommen aus .koolie/core/clients/, nicht aus
#       einer Handliste - ein neues Pack bringt seine Kennung selbst mit (D-117).
#
# WARUM (c) NUR BEI `sitzung`. D-117 spricht von DYNAMISCHEN Tests. Ein Validatorlauf
# (`skript`) misst das Repositorium und keinen Client, ein Dokumentenreview (`review`)
# ebenso; beide brauchen kein Pack. Der Zusatz hinter dem Wort bleibt zulaessig
# (`sitzung + validate-output.py`), deshalb wird auf ENTHALTENSEIN geprueft und nicht
# auf das erste Wort - `skript+sitzung` traegt beide Methoden und damit beide Pflichten.
#
# GRENZE, UND SIE STEHT HIER. Geprueft wird die NENNUNG, nicht ihre Richtigkeit: Ein
# Verweis auf ein Protokoll, das den Fall gar nicht behandelt, laeuft durch, und eine
# Version, die nicht die gemessene ist, ebenso. Das bleibt review-Gegenstand (D-23) -
# dieselbe Enthaltung, die Pruefung 61 fuer das RICHTIGE Pruefmittelwort zieht.
P65_MARKE = "**Ergebnisstatus:**"
P65_PROTOKOLL = re.compile(r"tests/protocols/[^\s`)]+\.md")


def _p65_vokabular(root: str) -> list:
    """Die zulaessigen Statuswoerter, abgeleitet aus TEST_CATALOG.md Punkt 4.

    Nicht gepflegt: Wer das Vokabular dort erweitert, soll nicht daran denken muessen,
    eine Liste im Validator nachzuziehen. Der Klammerzusatz ("(Referenz auf Befund)")
    gehoert zur Erlaeuterung und nicht zum Wort.
    """
    pfad = os.path.join(root, KERN, "tests", "TEST_CATALOG.md")
    if not os.path.isfile(pfad):
        return []
    for zeile in read(pfad).splitlines():
        if P65_MARKE not in zeile:
            continue
        rest = zeile.split(P65_MARKE, 1)[1]
        m = re.match(r"\s*(`[^`]+`(?:\s*/\s*`[^`]+`)*)", rest)
        if not m:
            return []
        return [t.strip("` ").split("(")[0].strip() for t in m.group(1).split("/")]
    return []


def _p65_packkennungen(root: str) -> list:
    """Die Kennungen der Client Packs - aus dem Verzeichnis, nicht aus einer Liste."""
    return [k for k, _d, _m in _client_packs(root)]


def check_ergebnisstatus_beleg(root: str) -> None:
    """Pruefung 65 (D-202): Ein Ergebnisstatus ausser `offen` traegt seinen Beleg."""
    vokabular = _p65_vokabular(root)
    if not vokabular:
        err(f"{KERN}/tests/TEST_CATALOG.md: das Vokabular des Ergebnisstatus ist unter "
            f"Punkt 4 nicht mehr auffindbar - Pruefung 65 leitet es von dort ab und hat "
            f"ihren Gegenstand verloren; sie bestuende sonst leise (D-23)")
        return
    packs = _p65_packkennungen(root)
    pack_re = re.compile("(" + "|".join(re.escape(k) for k in packs) +
                         r")[^|]{0,60}?\d+\.\d+\.\d+") if packs else None
    dateien = [os.path.join(root, KERN, "tests", "TEST_CATALOG.md")]
    for basis in (os.path.join(root, KERN, "framework", "skills"),
                  os.path.join(root, KERN, "framework", "role-packs")):
        for wurzel, _, files in os.walk(basis):
            if "TESTS.md" in files:
                dateien.append(os.path.join(wurzel, "TESTS.md"))
    gesehen = 0
    for pfad in sorted(dateien):
        if not os.path.isfile(pfad):
            continue
        rel = os.path.relpath(pfad, root).replace(os.sep, "/")
        i_pm = i_st = -1
        for nr, zeile in enumerate(read(pfad).splitlines(), 1):
            if not zeile.lstrip().startswith("|"):
                continue
            if "Ergebnisstatus" in zeile and "Prüfmethode" in zeile:
                i_pm = _tabellenspalte(zeile, "Prüfmethode")
                i_st = _tabellenspalte(zeile, "Ergebnisstatus")
                continue
            if min(i_pm, i_st) < 0:
                continue
            zellen = [z.strip() for z in zeile.strip().strip("|").split("|")]
            if len(zellen) <= max(i_pm, i_st) or not zellen[0]:
                continue
            if set(zellen[0]) <= set("-: "):
                continue
            # Die Betonung gehoert der Darstellung, nicht dem Wort.
            status = zellen[i_st].lstrip("* ").strip()
            if not status:
                continue
            gesehen += 1
            wort = next((w for w in vokabular if status.startswith(w)), None)
            if wort is None:
                err(f"{rel}:{nr}: Ergebnisstatus beginnt nicht mit einem Wort des "
                    f"Vokabulars ({', '.join(vokabular)}) - TEST_CATALOG.md Punkt 4 "
                    f"fuehrt es abschliessend (D-202)")
                continue
            if wort == "offen":
                continue
            if not P65_PROTOKOLL.search(status):
                err(f"{rel}:{nr}: Ergebnisstatus '{wort}' nennt kein Protokoll unter "
                    f"{KERN}/tests/protocols/. TEST_CATALOG.md Punkt 4: 'Ein "
                    f"Ergebnisstatus ausser offen MUSS auf ein Protokoll verweisen' - "
                    f"ohne den Verweis ist die Abnahme eine Behauptung (D-202)")
            if pack_re is not None and "sitzung" in zellen[i_pm] \
                    and not pack_re.search(status):
                err(f"{rel}:{nr}: Ergebnisstatus '{wort}' einer sitzung-Zelle nennt kein "
                    f"Client Pack mit Produktversion. Ein Ergebnisstatus deckt kein "
                    f"anderes Pack, und ohne die Version sagt er nicht, gegen welchen "
                    f"Produktstand gemessen wurde (D-117, D-202)")
    if gesehen == 0:
        err(f"{KERN}/tests/: keine Zelle mit Ergebnisstatus gefunden - Pruefung 65 hat "
            f"ihren Gegenstand verloren; sie bestuende sonst leise (D-23)")




# --- Pruefung 73: Jede [DOK]-Matrixzeile nennt ihre Quelle --------------------------
#
# ANLASS, UND ER IST GEZAEHLT (K-62, D-156, seit 0.62.0 offen, gemessen 2026-09-22).
# Anhang 31.4 des Hauptdokuments sagt ueber sich selbst, die MASSGEBLICHE Zuordnung
# stehe in der Faehigkeitsmatrix: "Dort nennt die Belegspalte je Zeile die Seite, auf
# die sie sich stuetzt." Das traf am 2026-09-18 fuer 14 von 43 Zeilen zu - die Bauform
# "eine Zusage, die mehr verspricht, als sie leistet", in ihrer Grundform.
#
# DER PREIS IST GEMESSEN, NICHT GESCHAETZT: Der Durchgang von FW-AK-01 musste ALLE 22
# Quellen abrufen, weil ohne Zuordnung je Zeile nicht zu sagen ist, welche Seite welche
# Zusage traegt. Eine Quellenliste ohne Zuordnung macht ihre eigene
# Wiederholungspruefung so teuer wie die erste.
#
# DIE KOPFREGEL, UND SIE IST DER GRUND, WESHALB DIESE PRUEFUNG UEBERHAUPT ETWAS SAGT.
# Geprueft wird der BELEGKOPF - die Zelle bis zum ersten Satzbruch (Punkt-Leerzeichen,
# Semikolon, Doppelpunkt). Was danach steht, ist Erlaeuterung. Ohne diese Trennung
# zaehlte jede Nennung der Marke mit: Zeile R5 des Packs claude-code erklaert, "ein
# Dokumentenabgleich belegt [DOK], nicht [TECHNISCH]" - das ist eine Aussage UEBER die
# Marke und kein Beleg. Dieselbe Trennlinie, die der VERIFY-Marker am Ende braucht
# (CR-2026-070 E3): die nur nennende Fundstelle zaehlt nicht wie die tragende.
#
# WARUM DIE KENNUNG UND NICHT DER SEITENPFAD. Das Pack devin-desktop nannte QD-6, das
# Pack claude-code `docs/en/memory` - dieselbe Sache in zwei Schreibweisen. Nur die
# Kennung laesst sich gegen die Liste halten; ein Pfad kann eine Seite nennen, die die
# Liste gar nicht fuehrt, und dann behauptet die Liste wieder mehr, als sie leistet.
# Der Pfad darf danebenstehen, er ist Lesehilfe.
#
# WARUM DER VERWEIS AUFGELOEST WIRD. Vier Zeilen des Packs devin-desktop belegen mit
# "wie B3", eine davon ueber zwei Glieder ("wie B4" -> "wie B3"). Solange B3 keine
# Kennung trug, trugen FUENF Zeilen keine - und keine Zaehlung, die den Verweis nicht
# aufloest, sieht das. Die Zusammenfassung des Packs zaehlt sie umgekehrt sehr wohl mit
# ("neun der 36 Zeilen tragen einen offenen VERIFY-Marker - ... B4, B5, B6 und B8 ueber
# den Verweis"): Wer sie beim Marker mitzaehlt und beim Beleg nicht, hat zwei
# Zaehlregeln fuer dieselbe Spalte.
#
# WARUM EINE AUSGESPROCHENE LUECKE ZULAESSIG IST UND TROTZDEM NICHT WACHSEN KANN.
# D-156 sagt: "Eine Zuordnung zu raten waere schlimmer als keine: Sie saehe wie ein
# Beleg aus." Fuer Zeile M3 des Packs claude-code gibt der Bestand keine Seite her -
# keine der sechs Seiten fuehrt die Sitzungs-Grant-Stufen, waehrend sie beim
# Schwesterpack in QD-11 stehen. Die Zeile sagt das mit der Marke
# QUELLE NICHT ZUGEORDNET. Damit das keine Hintertuer ist, fuehrt diese Pruefung die
# zugelassenen Luecken als MENGE: eine neue faellt auf, und eine geschlossene ebenso -
# dieselbe Bauform wie das leer DEKLARIERTE Feld von Pruefung 72 (D-155).
P73_KENNUNG_RE = re.compile(r"Q[CDKU]-\d+")  # QK- seit 1.13.0 (kiro, D-414), QU- seit 1.16.0 (cursor, D-440)
P73_BRUCH_RE = re.compile(r"\.\s|;\s|:\s|:$")
P73_VERWEIS_RE = re.compile(r"^(?:wie|dito)\b[^A-Z]*([RSBHAMX]\d+)")
P73_OFFEN_MARKE = "QUELLE NICHT ZUGEORDNET"
# Die ausgesprochenen Luecken, je Pack. Wer eine neue braucht, traegt sie hier ein -
# und begruendet sie im Aenderungsantrag. Wer eine schliesst, nimmt sie hier heraus.
P73_OFFEN = {"claude-code": {"M3"}}
P73_SELBSTPROBE = ("`[DOK]` **`QC-9`** (synthetisch)", "`[DOK]` ohne Kennung")


def _p73_kopf(zelle: str) -> str:
    """Der Belegkopf: die Zelle bis zum ersten Satzbruch."""
    m = P73_BRUCH_RE.search(zelle)
    return zelle[:m.start() + 1] if m else zelle


def _p73_matrixzeilen(root: str, pack: str) -> dict:
    """{Kennung: Belegzelle} der Faehigkeitsmatrix eines Packs, in Lesereihenfolge."""
    pfad = os.path.join(root, KERN, "clients", pack, "CLIENT_PACK.md")
    if not os.path.isfile(pfad):
        return {}
    aus = {}
    drin = False
    for zeile in read(pfad).replace("\r\n", "\n").split("\n"):
        if zeile.startswith("## 2. "):
            drin = True
            continue
        if drin and re.match(r"^## \d", zeile):
            drin = False
        if not drin:
            continue
        m = P73_ZEILE_RE.match(zeile)
        if not m:
            continue
        zellen = tabellenzellen(zeile)
        if zellen:
            aus[m.group(1)] = zellen[-1]
    return aus


def _p73_aufgeloest(zellen: dict, kennung: str) -> tuple:
    """Der Belegkopf einer Zeile, Verweise aufgeloest. (Kopf, Kette)."""
    ziel, kette = kennung, []
    for _ in range(5):
        kopf = _p73_kopf(zellen[ziel])
        m = P73_VERWEIS_RE.match(kopf)
        if not m or m.group(1) not in zellen or m.group(1) in kette:
            return kopf, kette
        kette.append(m.group(1))
        ziel = m.group(1)
    err(f"Faehigkeitsmatrix, Zeile {ziel}: der Belegverweis laeuft ueber mehr als "
        f"fuenf Glieder. Eine Belegkette, die niemand bis zum Ende liest, ist kein "
        f"Beleg (D-266)")
    return "", kette


def check_belegquelle(root: str) -> None:
    """Pruefung 73 (D-263): Jede `[DOK]`-Matrixzeile nennt ihre Quellenkennung."""
    gut, schlecht = P73_SELBSTPROBE
    if not P73_KENNUNG_RE.search(_p73_kopf(gut)) or P73_KENNUNG_RE.search(_p73_kopf(schlecht)):
        err("Pruefung 73: die eigene Selbstprobe traegt nicht mehr - die Pruefung "
            "haette ihren Gegenstand verloren und bestuende leise (D-23)")
        return
    verz = os.path.join(root, KERN, "clients")
    if not os.path.isdir(verz):
        err(f"{KERN}/clients/ fehlt - Pruefung 73 haette keinen Gegenstand (D-23)")
        return
    packs = sorted(n for n in os.listdir(verz)
                   if n != "_template"
                   and os.path.isfile(os.path.join(verz, n, "CLIENT_PACK.md")))
    if not packs:
        err(f"{KERN}/clients/: kein Client Pack mit CLIENT_PACK.md gefunden - "
            f"Pruefung 73 haette keinen Gegenstand (D-23)")
        return
    for pack in packs:
        zellen = _p73_matrixzeilen(root, pack)
        if not zellen:
            err(f"clients/{pack}/CLIENT_PACK.md: unter '## 2.' steht keine "
                f"Matrixzeile. Pruefung 73 liest die Faehigkeitsmatrix dort und "
                f"haette ohne sie nichts zu pruefen (D-23)")
            continue
        erwartet = set(P73_OFFEN.get(pack, ()))
        gefunden = set()
        for kennung in zellen:
            kopf, kette = _p73_aufgeloest(zellen, kennung)
            if "[DOK]" not in kopf:
                continue
            ueber = f" (ueber den Verweis {' → '.join(kette)})" if kette else ""
            if P73_OFFEN_MARKE in kopf:
                gefunden.add(kette[-1] if kette else kennung)
                continue
            if not P73_KENNUNG_RE.search(kopf):
                err(f"clients/{pack}/CLIENT_PACK.md: Zeile {kennung} ist mit `[DOK]` "
                    f"belegt und nennt im Belegkopf keine Quellenkennung "
                    f"(`QC-n`/`QD-n`){ueber}. Anhang 31.4 sagt zu, die Zuordnung "
                    f"stehe je Zeile in der Matrix; eine Zeile ohne sie macht jede "
                    f"Wiederholung von `FW-AK-01` so teuer wie die erste (K-62, "
                    f"D-156). Gibt der Bestand keine Seite her, sagt die Zeile "
                    f"`{P73_OFFEN_MARKE}` - geraten wird nicht, eine geratene "
                    f"Zuordnung saehe wie ein Beleg aus (D-263)")
        for offen in sorted(gefunden - erwartet):
            err(f"clients/{pack}/CLIENT_PACK.md: Zeile {offen} sagt "
                f"`{P73_OFFEN_MARKE}`, steht aber nicht in P73_OFFEN. Eine "
                f"ausgesprochene Luecke ist zulaessig und wird DEKLARIERT - sonst "
                f"waere sie eine Hintertuer, durch die die Zusage von Anhang 31.4 "
                f"still wieder kleiner wird (D-263)")
        for offen in sorted(erwartet - gefunden):
            err(f"clients/{pack}/CLIENT_PACK.md: P73_OFFEN fuehrt Zeile {offen} als "
                f"ausgesprochene Luecke, die Zeile sagt es aber nicht (mehr). Ist die "
                f"Quelle nachgetragen, gehoert der Eintrag heraus; eine Ausnahme ohne "
                f"Gegenstand sieht wie Sorgfalt aus und ist tot (0.57.1, D-263)")


# ---------------------------------------------------------------------------
# PRUEFUNG 95: DER AENDERUNGSVERLAUF EINES SKILLS NENNT DIE ART (CR-2026-147, D-403)
# ---------------------------------------------------------------------------
#
# ANLASS. D-303 oeffnet die Zellen eines Testblatts nur, wenn eine Aenderung eine
# ANWEISUNG des Skills beruehrt - und die Grenze zieht ein Mensch. Seit D-303 nennt jede
# neue Zeile eines Skill-Aenderungsverlaufs diese Einordnung ("Keine Anweisung beruehrt"
# oder "Anweisung beruehrt"), aber keine Pruefung sah, ob sie dasteht (K-146).
# GEGENSTAND: die Zeile der Version, die der Steckbrief der SKILL.md nennt, und jede
# Zeile mit einem Datum nach dem Stichtag. Aeltere Zeilen bleiben, wie sie geschrieben
# wurden (Klasse C). NUR DIE SKILLS DES KERNS: D-303 regelt die Testblaetter des
# Frameworks; ein projekteigener Skill fuehrt seinen Verlauf nach eigener Regel. Beim
# ersten Update mit dieser Pruefung meldete sie im Uebungsrepositorium die Erstfassung
# eines prj-Skills. Die installierten Kopien der Kernskills sind Kopien der Quelle,
# die hier geprueft wird.
# GRENZE: Die Pruefung sieht die NENNUNG, nicht ihre Richtigkeit. Ob eine Aenderung eine
# Anweisung beruehrt, entscheidet weiter ein Mensch (Preis von D-303, benannt).
P95_STICHTAG = "2026-09-22"
P95_ART_RE = re.compile(r"Anweisung\s+ber(?:ü|ue)hrt", re.I)
P95_ZEILE_RE = re.compile(r"^\|\s*(\d+\.\d+\.\d+)\s*\|\s*(\d{4}-\d\d-\d\d)\s*\|", re.M)


def check_skill_aenderungsart(root: str, man: dict) -> None:
    """Pruefung 95 (D-403): der Aenderungsverlauf eines Skills nennt die Art der Aenderung."""
    for skills_dir, prefix in skill_dirs(root, man):
        if not prefix.startswith(KERN + "/"):
            continue
        for name in sorted(os.listdir(skills_dir)):
            sdir = os.path.join(skills_dir, name)
            skill_path = os.path.join(sdir, "SKILL.md")
            cl_path = os.path.join(sdir, "CHANGELOG.md")
            if not (os.path.exists(skill_path) and os.path.exists(cl_path)):
                continue
            m = re.search(r"^\|\s*Version\s*\|\s*`?([^`|]+?)`?\s*\|", read(skill_path), re.M)
            aktuell = m.group(1).strip() if m else None
            for zeile in read(cl_path).splitlines():
                z = P95_ZEILE_RE.match(zeile)
                if not z or not (z.group(1) == aktuell or z.group(2) > P95_STICHTAG):
                    continue
                if not P95_ART_RE.search(zeile):
                    err(f"{prefix}/{name}/CHANGELOG.md: die Zeile {z.group(1)} nennt nicht, "
                        f"ob sie eine Anweisung berührt ('Keine Anweisung berührt' oder "
                        f"'Anweisung berührt') – davon hängt ab, ob die Zellen des "
                        f"Testblatts offen sind (D-303, D-403)")
