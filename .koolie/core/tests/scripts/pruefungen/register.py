"""Die Register der Governance: Decision-Log-Zellen, Pruefregister, 1.0.0-Stand,
Statusvokabular, Klaerungsregister und seine Form, Releaseplan, Decision-Register und
Roadmapstand.

Pruefungen 36, 40, 46, 47, 50, 53, 58, 91 und 102. Teil des Validators validate-
framework.py, seit 1.19.1 nach Gegenstand in Module geteilt (K-174). Das Register aller
Pruefungen steht im Kopfkommentar des Einstiegs, die Grenze jeder einzelnen in ihrem
Kopfkommentar hier."""
from __future__ import annotations

import os
import re

from .gemeinsam import (
    err, iter_text_files, KERN, read, REGISTER_ANKER, REGISTER_ENDE, SKILL_STATUS,
    tabellenzellen)


# Seit 1.19.1 liegt der Code der beiden Pruefskripte in einem Paket neben seinem
# Einstieg (K-174). Wer ihren Quelltext liest - Pruefung 40 das Register und
# die Sondenmenge -, liest den Einstieg UND sein Paket, den Einstieg zuerst: Sein
# Kopfkommentar ist das Register.
PAKET_JE_SKRIPT = {"tests/scripts/validate-framework.py": "tests/scripts/pruefungen",
                   "tests/scripts/probe-pruefungen.py": "tests/scripts/sonden"}


def paketquelltext(root: str, rel: str) -> str:
    """Der Quelltext des Pakets zu einem Einstieg, Modul fuer Modul nach Namen."""
    paket = PAKET_JE_SKRIPT.get(rel)
    ordner = os.path.join(root, KERN, *paket.split("/")) if paket else ""
    if not ordner or not os.path.isdir(ordner):
        return ""
    return "".join("\n" + read(os.path.join(ordner, name))
                   for name in sorted(os.listdir(ordner)) if name.endswith(".py"))


# Pruefung 36: Jede Tabellenzeile des Decision Logs fuehrt so viele Zellen wie der
# Kopf ihrer Tabelle (CR-2026-060 E4, D-75).
#
# Anlass: Vier zerrissene Zeilen in 0.34.0 - D-61 bis D-63 mit fuenf Zellen statt sechs,
# D-29 mit acht, dort teilte ein unmaskierter Strich in einem Codespan die Zeile. In der
# gerenderten Tabelle stand die Herkunft unter "Begruendung", das Datum unter
# "Alternativen", die Rolle unter "Status". D-29 stand so seit 0.10.x. Gefunden hat die
# Zeilen jedes Mal ein Mensch beim Eintragen einer anderen.
#
# WAS SIE HEUTE FAENGT: nichts. Alle Zeilen sind seit 0.35.0 in Ordnung, von Hand
# berichtigt. Das ist eine VERANKERUNG, keine Behebung - wie Pruefung 35 und der fuenfte
# Gegenstand der Pruefung 32. Der Unterschied: Ihr Gegenbeweis ist ein Abzaehlen und
# keine Konstruktion. Gegen 0.34.0 meldet sie vier Fundstellen, gegen 0.32.0 und 0.33.0
# je eine.
#
# WAS SIE NICHT LEISTET: Sie prueft die Anzahl, nicht den Inhalt. Eine Zeile, in der
# Begruendung und Alternativen vertauscht sind, besteht sie - dieselbe Grenze, die
# Pruefung 31 fuer ihre Arithmetik benennt. Und sie prueft nur diese eine Datei: Die
# uebrigen Tabellen des Repositoriums haben ihre eigenen Pruefungen (30, 31) oder keine.
DECISION_LOG_DATEI = KERN + "/governance/DECISION_LOG.md"


def check_decision_log_zellen(root: str) -> None:
    """Pruefung 36 (D-75): Die Tabellen des Decision Logs sind nicht zerrissen."""
    pfad = os.path.join(root, DECISION_LOG_DATEI.replace("/", os.sep))
    if not os.path.isfile(pfad):
        err(f"{DECISION_LOG_DATEI}: fehlt. Ohne das Decision Log ist keine Entscheidung "
            f"dieses Frameworks belegt")
        return
    zeilen = read(pfad).replace("\r\n", "\n").split("\n")
    soll = None
    ueberschrift = "(vor der ersten Ueberschrift)"
    kopfzeile = 0
    gesehen = 0
    for nr, zeile in enumerate(zeilen, 1):
        z = zeile.strip()
        if z.startswith("## "):
            ueberschrift = z[3:].strip()
            soll = None
            continue
        if not z.startswith("|"):
            # Eine Leerzeile beendet die Tabelle; Fliesstext zwischen zwei Tabellen
            # darf die Zellenzahl nicht von der einen auf die andere uebertragen.
            if not z:
                soll = None
            continue
        zellen = tabellenzellen(z)
        if soll is None:
            soll = len(zellen)
            kopfzeile = nr
            gesehen += 1
            continue
        if len(zellen) != soll:
            err(f"{DECISION_LOG_DATEI}:{nr}: Die Zeile fuehrt {len(zellen)} Zellen, der "
                f"Kopf ihrer Tabelle ({ueberschrift}, Zeile {kopfzeile}) fuehrt {soll}. "
                f"Eine zerrissene Zeile rendert die Werte unter den falschen Spalten; "
                f"ein Strich innerhalb einer Zelle gehoert maskiert (\\|)")
    if not gesehen:
        err(f"{DECISION_LOG_DATEI}: keine Tabellenzeile gefunden. Der Anker dieser "
            f"Pruefung ist die Zeilenform '| ... |'; ohne sie prueft sie nichts und "
            f"bestuende leise (D-23)")
NACHWEIS_SATZ = "Der Wirksamkeitsnachweis nach D-23 fuer die Pruefungen {} laeuft"
SONDEN_SATZ = "Wirkungsnachweis nach D-23 fuer die Pruefungen {}"
KATALOG_SPANNE = "für die Prüfungen {} als Skript"
KATALOG_GRENZFAELLE = "Die {} Grenzfälle einzeln"
REGISTER_DATEIEN = ("tests/scripts/validate-framework.py",
                    "tests/scripts/probe-pruefungen.py",
                    "tests/TEST_CATALOG.md",
                    "tests/EDGE_CASES.md")


def nummernspanne(zahlen) -> str:
    """Kanonische Schreibweise einer Nummernmenge: '6 und 18 bis 40'.

    Eine einzelne Nummer steht allein, eine luckenlose Folge als 'a bis b', mehrere
    Bloecke durch Komma und ein abschliessendes 'und' getrennt. Diese Funktion ist die
    einzige Quelle der Schreibweise; die drei Traeger vergleichen woertlich gegen sie.
    """
    folge = sorted(zahlen)
    bloecke, lauf = [], [folge[0]]
    for z in folge[1:]:
        if z == lauf[-1] + 1:
            lauf.append(z)
        else:
            bloecke.append(lauf)
            lauf = [z]
    bloecke.append(lauf)
    teile = [str(b[0]) if len(b) == 1 else f"{b[0]} bis {b[-1]}" for b in bloecke]
    if len(teile) == 1:
        return teile[0]
    return ", ".join(teile[:-1]) + " und " + teile[-1]


def genannte_pruefungen(*texte: str) -> set:
    """Jede Pruefungsnummer, die ein Text als 'Pruefung N' oder 'Pruefungen N bis M' nennt.

    Der Zuschnitt ist Absicht (CR-2026-064 E2): Ein Querverweis auf eine kleinere Nummer
    stoert nicht, weil nur die hoechste zaehlt - und eine neue Pruefung nennt ihre Nummer
    zwangslaeufig, spaetestens in ihrem eigenen Kopfkommentar.
    """
    gefunden = set()
    muster = re.compile(r"Pr[uü]efung(?:en)?\s+(\d+(?:\s*(?:,|und|bis)\s*\d+)*)")
    for text in texte:
        for treffer in muster.finditer(text):
            teile = re.split(r"\s*(,|und|bis)\s*", treffer.group(1))
            for i, teil in enumerate(teile):
                if teil == "bis" and 0 < i < len(teile) - 1:
                    gefunden |= set(range(int(teile[i - 1]), int(teile[i + 1]) + 1))
                elif teil.isdigit():
                    gefunden.add(int(teil))
    return gefunden


def check_pruefregister(root: str) -> None:
    """Pruefung 40 (D-85, D-86): Register und Bestand des Pruefapparats decken sich."""
    texte = {}
    for rel in REGISTER_DATEIEN:
        pfad = os.path.join(root, KERN, *rel.split("/"))
        if not os.path.exists(pfad):
            err(f"{KERN}/{rel}: fehlt. Prüfung 40 hält dort das Register des "
                f"Prüfapparats gegen den Bestand (D-85)")
            return
        texte[rel] = read(pfad) + paketquelltext(root, rel)
    validator = texte["tests/scripts/validate-framework.py"]
    sonden = texte["tests/scripts/probe-pruefungen.py"]
    katalog = texte["tests/TEST_CATALOG.md"]
    kanten = texte["tests/EDGE_CASES.md"]

    # --- Gegenstand 1: die Anker ------------------------------------------------------
    doc = validator.split('"""')[1] if validator.count('"""') >= 2 else ""
    sondendoc = sonden.split('"""')[1] if sonden.count('"""') >= 2 else ""
    if REGISTER_ANKER not in doc or REGISTER_ENDE not in doc:
        err(f"{KERN}/tests/scripts/validate-framework.py: der Kopfkommentar führt kein "
            f"Register mehr (gesucht: '{REGISTER_ANKER}' und '{REGISTER_ENDE}') – "
            f"Prüfung 40 hat ihren Gegenstand verloren und würde sonst leise bestehen")
        return
    fwko01 = [z for z in katalog.splitlines() if z.startswith("| FW-KO-01")]
    fwko05 = [z for z in katalog.splitlines() if z.startswith("| FW-KO-05")]
    if len(fwko01) != 1 or len(fwko05) != 1:
        err(f"{KERN}/tests/TEST_CATALOG.md: die Zeile FW-KO-01 oder FW-KO-05 steht nicht "
            f"genau einmal (gefunden: {len(fwko01)} und {len(fwko05)}) – Prüfung 40 misst "
            f"dort die Sondenmenge und die Grenzfallanzahl (D-85)")
        return

    # --- Gegenstand 2: das Register ist lueckenlos und vollstaendig --------------------
    liste = doc.split(REGISTER_ANKER, 1)[1].split(REGISTER_ENDE, 1)[0]
    gefuehrt = sorted({int(n) for n in re.findall(r"^\s{0,2}(\d+)[a-z]?\. ", liste, re.M)})
    if not gefuehrt:
        err(f"{KERN}/tests/scripts/validate-framework.py: das Register im Kopfkommentar "
            f"führt keinen einzigen nummerierten Eintrag – Prüfung 40 hätte nichts zu "
            f"vergleichen und bestünde leise")
        return
    luecken = [n for n in range(1, gefuehrt[-1] + 1) if n not in gefuehrt]
    if luecken:
        err(f"{KERN}/tests/scripts/validate-framework.py: das Register im Kopfkommentar "
            f"hat Lücken – es fehlt {', '.join(str(n) for n in luecken)}. Eine Nummer "
            f"ohne Eintrag ist eine Prüfung, die niemand findet (D-85)")
    genannt = genannte_pruefungen(validator, sonden)
    hoechste = max(genannt) if genannt else 0
    if hoechste > gefuehrt[-1]:
        err(f"{KERN}/tests/scripts/validate-framework.py: das Register im Kopfkommentar "
            f"endet bei Prüfung {gefuehrt[-1]}; die Prüfskripte nennen Prüfung "
            f"{hoechste}. Eine neue Prüfung ohne Registereintrag ist genau der Fall vom "
            f"2026-09-14 – das Register ist die einzige Stelle, die sagt, was dieser "
            f"Lauf prüft (D-85)")
    elif hoechste and hoechste < gefuehrt[-1]:
        err(f"{KERN}/tests/scripts/validate-framework.py: das Register im Kopfkommentar "
            f"führt Prüfung {gefuehrt[-1]}; in den Prüfskripten wird sie nirgends bei "
            f"ihrer Nummer genannt. Ein Eintrag ohne Prüfung verspricht mehr, als der "
            f"Lauf leistet (D-85)")

    # --- Gegenstand 3: die Sondenmenge an drei Stellen, wortgleich ---------------------
    kennungen = (re.findall(r'\bsonde\("([^"]+)"', sonden)
                 + re.findall(r'melde\("SONDE", "([^"]+)"', sonden))
    mit_sonde = {int(m.group(1)) for m in (re.match(r"(\d+)", k) for k in kennungen) if m}
    if not mit_sonde:
        err(f"{KERN}/tests/scripts/probe-pruefungen.py: keine einzige Sonde mit einer "
            f"Prüfungsnummer gefunden – Prüfung 40 rechnet daraus die Sondenmenge aus "
            f"und hat ihren Gegenstand verloren")
        return
    spanne = nummernspanne(mit_sonde)
    for rel, text, soll in (
            ("tests/scripts/validate-framework.py", doc, NACHWEIS_SATZ.format(spanne)),
            ("tests/scripts/probe-pruefungen.py", sondendoc, SONDEN_SATZ.format(spanne)),
            ("tests/TEST_CATALOG.md", fwko01[0], KATALOG_SPANNE.format(spanne))):
        if soll not in text:
            err(f"{KERN}/{rel}: die Sondenmenge ist dort nicht in der ausgerechneten "
                f"Schreibweise genannt. Erwartet wörtlich: '{soll}'. "
                f"probe-pruefungen.py führt Sonden für die Prüfungen {spanne} – eine "
                f"gepflegte Zahl über den Prüfapparat lag am 2026-09-14 an allen drei "
                f"Stellen daneben (D-86)")

    # --- Gegenstand 4: die Grenzfallanzahl ausserhalb ihrer Quelle ---------------------
    grenzfaelle = set(re.findall(r"\bG-(\d\d)\b", kanten))
    if not grenzfaelle:
        err(f"{KERN}/tests/EDGE_CASES.md: keine einzige Grenzfallkennung der Form G-NN "
            f"gefunden – Prüfung 40 zählt sie dort und hat ihren Gegenstand verloren")
        return
    soll_gf = KATALOG_GRENZFAELLE.format(len(grenzfaelle))
    if soll_gf not in fwko05[0]:
        err(f"{KERN}/tests/TEST_CATALOG.md: FW-KO-05 nennt nicht die gezählte Anzahl der "
            f"Grenzfälle. Erwartet wörtlich: '{soll_gf}'. Die Zeile ist eine "
            f"Arbeitsanweisung für eine Sitzung; sie stand von 0.33.0 bis 0.41.0 auf "
            f"zwölf, während der Bestand auf zwanzig wuchs – wer sie so fährt, prüft "
            f"einen Teil und meldet das Ganze (D-86)")


# ---------------------------------------------------------------------------
# Pruefung 46: Der 1.0.0-Stand wird ausgerechnet, nicht gepflegt
# ---------------------------------------------------------------------------
#
# ANLASS. D-11 nennt fuenf Kriterien fuer 1.0.0; vier davon sind maschinell zaehlbar.
# Die Roadmap fuehrte dafuer seit 0.42.0 ausdruecklich KEINE Zahlen, sondern "die
# Befehle, die sie ausrechnen" - die richtige Lehre aus fuenf falschen Zahlen ueber den
# Pruefapparat. Am 2026-09-15 wurden diese Befehle zum ersten Mal ausgefuehrt
# (CR-2026-070, tests/protocols/2026-09-15-gegenpruefung-d11-zaehlregeln.md):
#
#   Kriterium 1  geglaubt 27   gezaehlt 29   der grep kannte EINE von ZWEI registrierten
#                                            Markerschreibweisen; die clientgebundene
#                                            Altform (Produktname statt CLIENT) traegt
#                                            allein im Pack devin-desktop sieben
#                                            Fundstellen und zwei in dessen root-template
#   Kriterium 2  geglaubt 103  gezaehlt 118  "die dezentralen TESTS.md je Skill" wurde als
#                                            zwoelf Dateien gelesen; es sind dreizehn
#   Kriterium 3  geglaubt 16   gezaehlt 69   die genannte Ablagenliste deckt ein Viertel
#                                            des Bestands - und framework/core/ ist
#                                            genannt und traegt gar keine Statuszeile
#   Kriterium 4  geglaubt 16   gezaehlt 9    ein roher grep zaehlte die Legende, fuenf
#                                            Klaerungspunkte und D-11 selbst mit
#
# Vier von vier. Keine der Zahlen ist je falsch geschrieben worden - jede ist das
# richtige Ergebnis einer Regel, die weniger kann als ihr Kriterium verlangt. Ein
# Befehl, den niemand ausfuehrt, ist keine Ausrechnung, sondern eine Zahl mit einem
# Zwischenschritt; und weil ihn niemand ausfuehrt, faellt auch nicht auf, dass er das
# Falsche zaehlt.
#
# BAUFORM (E1). Die von Pruefung 40 und 31: Der Stand steht AUSGERECHNET an genau einer
# Stelle - der Standzeile in docs/ROADMAP.md -, und diese Pruefung haelt die geschriebene
# Zahl gegen die gezaehlte. Nicht der offene Punkt ist der Fehler, sondern die falsche
# Zahl. Ein Zaehler, der jeden offenen Punkt meldete, ergaebe heute 225 Fehler, machte
# jeden Lauf rot und waere binnen eines Releases abgeschaltet; ein Zaehler, der nur
# berichtet, ist keine Pruefung. Der Preis dieser Bauform steht im Antrag und ist
# gewollt: JEDER Fortschritt macht den Lauf rot, bis die Zahl nachgezogen ist. Genau
# dieses Nachziehen ist der Vorgang, der bis 0.47.0 unterblieben ist.
#
# ZAEHLBEREICH (E2). Nur <CORE_DIR>/, ohne build/ (Erzeugnis), CHANGELOG.md,
# governance/change-requests/ und tests/protocols/ (datierte, abgeschlossene
# Aufzeichnungen). Der Kern ist in jeder Installation derselbe - install.py --check ist
# genau dafuer da -, also ist die Zahl installationsunabhaengig und dieselbe Standzeile
# gilt in jedem uebernehmenden Projekt. Fundstellen ausserhalb des Kerns zaehlen nicht,
# auch echte: README.md:165 war so eine und ist per Hand berichtigt.
#
# DER FALLSTRICK, DER BEIM BAUEN ZUSCHNAPPTE (E7). Die erste Fassung lief ueber
# glob.glob(..., recursive=True). glob ueberspringt Pfadbestandteile, die mit einem Punkt
# beginnen - damit fehlten fuenfzehn Dateien des Kerns, darunter genau die zwei Traeger
# clients/*/root-template/.devin/README.md und .../.claude/README.md, die den Befund zu
# Kriterium 1 tragen. Der Zaehler haette 27 gemeldet und damit zufaellig die geglaubte
# Zahl bestaetigt. Eine Zaehlregel, die einen Traeger still ueberspringt, war der Anlass
# dieses Antrags; sie ist beim Bauen der Abhilfe ein zweites Mal entstanden. Deshalb
# os.walk, und deshalb misst die Selbstprobe C1 des Sondenskripts beide Verfahren
# gegeneinander.
#
# WAS SIE NICHT LEISTET.
#   * Kriterium 5 von D-11 ("Uebernahme in ein zweites Projekt nachgewiesen") zaehlt sie
#     NICHT. Das ist keine Zahl, sondern eine Feststellung. Eine ENTHALTUNG, und sie
#     steht hier statt in einem Gegenstand, der nichts misst.
#   * Sie misst Zahlen, nicht Fortschritt. Ein Modulstatus, der von `entwurf` auf `pilot`
#     gehoben wird, ohne dass jemand das Modul angesehen hat, senkt Kriterium 3 um eins.
#     Die fachliche Abnahme ist nicht maschinell, und diese Pruefung behauptet es nicht.
#   * Kriterium 1 zaehlt auch die Fundstellen, die den Marker nur NENNEN - Registerzeile,
#     Glossarzeile, Arbeitsanweisung (E3). Die Zahl ist ein PEGEL, kein Arbeitsvorrat,
#     und sie kann nicht auf null gehen, solange der Marker sein eigenes Register hat.
#     Das ist richtig so: PLACEHOLDER_REGISTRY.md schreibt beiden Markerformen in der
#     Spalte "Ersetzung/Frist" ausdruecklich "vor Version 1.0.0" vor. Ein Platzhalter,
#     dessen letzte Aussage verifiziert ist, gehoert aus dem Register - sonst fuehrt das
#     Repositorium einen Platzhalter ohne Gegenstand.
#   * Sie sagt nicht "1.0.0-reif" (E8). Stehen alle vier Zahlen auf 0 und der Lauf ist
#     gruen, IST das die Meldung - erzwungen statt behauptet, und ohne einen fuenften
#     Gegenstand, der heute nichts faengt.
D11_DATEI = KERN + "/docs/ROADMAP.md"
D11_SATZ = ("Gezählt von Prüfung 46: Kriterium 1 = {}, Kriterium 2 = {}, "
            "Kriterium 3 = {}, Kriterium 4 = {}")
D11_ANKER = "Gezählt von Prüfung 46: Kriterium 1 = "
# Beide Schreibweisen (E4). Bis 0.86.1 waren sie registriert; die Altform war nur im
# Client Pack devin-desktop zulaessig (Pruefung 14 setzte das durch) und trug dieselbe
# Frist "vor Version 1.0.0". Wer nur die neutrale Form zaehlt, haelt ein Client Pack mit
# sieben offenen Verifikationsbedarfen fuer fertig.
#
# MIT 0.87.0 SIND BEIDE FORMEN ABGESCHAFFT (CR-2026-121, D-291), und dieser Ausdruck
# bleibt unveraendert stehen. Was er zaehlt, hat sich nicht geaendert; wozu die Zahl
# dient, schon: Sie war ein Arbeitsvorrat und ist jetzt eine RUECKFALLSPERRE. Ausgebaut
# wird sie nicht - D-11 verloere damit seinen einzigen maschinellen Zaehler fuer
# Kriterium 1, die Standzeile fiele von vier Zahlen auf drei, und eine Wiedereinfuehrung
# der Form fiele niemandem auf. DER PREIS IST BENANNT: Eine Zahl, die dauerhaft auf null
# steht, wird nicht mehr gelesen; sie traegt nur, solange ihre Sonde laeuft.
D11_MARKER_RE = re.compile(r"<VERIFY AGAINST CURRENT (?:CLIENT|DEVIN) DOCUMENTATION>")
D11_AUSSER = ("build/", "CHANGELOG.md", "governance/change-requests/",
              "tests/protocols/")
D11_MARKER_ENDUNGEN = (".md", ".json", ".py")
D11_STECKBRIEF_RE = re.compile(r"^\|\s*Status\s*\|\s*(.+?)\s*\|$")
# Die Steckbriefzeile steht im Kopf des Dokuments. Sechzig Zeilen sind grosszuegig
# gemessen (der spaeteste Treffer im Bestand steht auf Zeile 41) und halten zugleich die
# Lebenszyklustabelle aus 08-skill-conventions.md (Zeile 92) und die Vorfalltabelle aus
# INCIDENT_HANDLING.md (Zeile 37) draussen - beides Tabellen MIT einer Statusspalte, die
# keinen Modulstatus fuehren.
D11_STECKBRIEF_KOPF = 60
D11_KRITERIEN = ("kein unbearbeiteter VERIFY-Marker",
                 "Testkatalog und dezentrale Testblätter ohne `offen`",
                 "Modulstatus über `entwurf`",
                 "Decision Records ohne `entschieden (Vorschlag)`")


def _d11_kerndateien(root: str, endungen: tuple):
    """(absoluter Pfad, Pfad unter <CORE_DIR>/) je Kerndatei im Zaehlbereich.

    os.walk und NICHT glob: glob ueberspringt Pfadbestandteile, die mit einem Punkt
    beginnen, und genau dort liegen zwei Traeger des Kerns (E7, Selbstprobe C1).
    """
    wurzel = os.path.join(root, KERN)
    for ordner, _, dateien in os.walk(wurzel):
        for name in sorted(dateien):
            if not name.endswith(endungen):
                continue
            pfad = os.path.join(ordner, name)
            rest = os.path.relpath(pfad, wurzel).replace(os.sep, "/")
            if any(rest == a or rest.startswith(a) for a in D11_AUSSER):
                continue
            yield pfad, rest


def _d11_offene_zellen(text: str, praefix: str) -> int:
    """Tabellenzeilen mit `praefix`, deren letzte Zelle mit 'offen' beginnt."""
    treffer = 0
    for zeile in text.replace("\r\n", "\n").split("\n"):
        z = zeile.strip()
        if not z.startswith(praefix) or z.startswith("|---"):
            continue
        zellen = tabellenzellen(z)
        if zellen and zellen[-1].startswith("offen"):
            treffer += 1
    return treffer


def _d11_zaehlen(root: str) -> list:
    """Die vier maschinell zaehlbaren Kriterien von D-11, in ihrer Reihenfolge."""
    # --- 1: Markerfundstellen, beide Schreibweisen -----------------------------------
    k1 = 0
    for pfad, _ in _d11_kerndateien(root, D11_MARKER_ENDUNGEN):
        k1 += len(D11_MARKER_RE.findall(read(pfad)))

    # --- 2: offene Ergebniszellen im Katalog UND in jedem Testblatt -------------------
    # Gefunden durch Baumdurchlauf, nicht durch eine Ablagenliste (E5): Eine Liste kann
    # eine dreizehnte Datei uebersehen, und sie hat es.
    katalog = os.path.join(root, KERN, "tests", "TEST_CATALOG.md")
    k2 = _d11_offene_zellen(read(katalog), "| FW-") if os.path.isfile(katalog) else 0
    for pfad, _ in _d11_kerndateien(root, ("TESTS.md",)):
        k2 += _d11_offene_zellen(read(pfad), "| ")

    # --- 3: Steckbriefe auf `entwurf`, im ganzen Bestand ------------------------------
    # Verglichen wird das ERSTE WORT des Werts: role-packs/software-development traegt
    # "entwurf (Referenzpack der Erstfassung)", und ein Gleichheitsvergleich saehe sie
    # nicht (E6).
    k3 = 0
    for pfad, _ in _d11_kerndateien(root, (".md",)):
        for zeile in read(pfad).replace("\r\n", "\n").split("\n")[:D11_STECKBRIEF_KOPF]:
            treffer = D11_STECKBRIEF_RE.match(zeile.strip())
            if not treffer:
                continue
            wert = treffer.group(1).strip().strip("`").strip()
            if wert.split()[:1] == ["entwurf"]:
                k3 += 1
            break

    # --- 4: Decision Records auf `entschieden (Vorschlag)` ----------------------------
    # NUR Zeilen der Form | D-NN |. Nicht die Legende, nicht die Klaerungspunkte K-NN,
    # nicht D-11 selbst: D-11 sagt "Decision Records", und ein Klaerungspunkt ist keiner.
    log = os.path.join(root, KERN, "governance", "DECISION_LOG.md")
    k4 = 0
    if os.path.isfile(log):
        for zeile in read(log).replace("\r\n", "\n").split("\n"):
            z = zeile.strip()
            if not re.match(r"^\|\s*D-\d+\s*\|", z):
                continue
            zellen = tabellenzellen(z)
            if len(zellen) > 4 and zellen[4].startswith("entschieden (Vorschlag)"):
                k4 += 1
    return [k1, k2, k3, k4]


def check_d11_stand(root: str) -> None:
    """Pruefung 46 (D-98, D-99): Der 1.0.0-Stand ist ausgerechnet, nicht gepflegt."""
    pfad = os.path.join(root, D11_DATEI.replace("/", os.sep))
    if not os.path.isfile(pfad):
        err(f"{D11_DATEI}: fehlt. Prüfung 46 hält dort den ausgerechneten 1.0.0-Stand "
            f"gegen die geschriebene Standzeile (D-98)")
        return
    text = read(pfad)

    # --- Gegenstand 1: der Anker ------------------------------------------------------
    # Die Bauform der Pruefungen 28, 29, 31 und 40: Eine Konsistenzpruefung findet ihren
    # Gegenstand ueber einen Suchtext. Geht er verloren, bestuende sie LEISE - und
    # niemand saehe, dass der 1.0.0-Stand nicht mehr geprueft wird.
    wie_oft = text.count(D11_ANKER)
    if wie_oft != 1:
        err(f"{D11_DATEI}: die Standzeile steht {wie_oft}x statt genau einmal "
            f"(gesucht: '{D11_ANKER}…'). Prüfung 46 hat ihren Gegenstand verloren und "
            f"würde sonst leise bestehen. Erwartet wörtlich, in einer Zeile: "
            f"'{D11_SATZ.format(*_d11_zaehlen(root))}' (D-98)")
        return

    # --- Gegenstand 2 bis 5: die vier Zahlen -----------------------------------------
    # Verglichen werden die ZAHLEN, nicht die Zeichenkette. Ein Vergleich per `in`
    # bestuende bei jedem Praefix: "Kriterium 4 = 9" steckt in "Kriterium 4 = 99", und
    # die Sonde 46a ist genau daran gefallen, bevor sie es meldete.
    gezaehlt = _d11_zaehlen(root)
    soll = D11_SATZ.format(*gezaehlt)
    zeile = next((z.strip() for z in text.replace("\r\n", "\n").split("\n")
                  if D11_ANKER in z), "")
    geschrieben = [int(n) for n in re.findall(r"Kriterium \d+ = (\d+)", zeile)]
    if geschrieben == gezaehlt:
        return
    # Die Meldung nennt die gezaehlte Zahl je Kriterium einzeln - wer nur "stimmt nicht"
    # liest, sucht selbst nach, und genau dieses Nachsuchen ist der Vorgang, der bis
    # 0.47.0 unterblieben ist.
    for i, (name, ist) in enumerate(zip(D11_KRITERIEN, gezaehlt)):
        war = geschrieben[i] if i < len(geschrieben) else None
        if war == ist:
            continue
        richtung = ("die Standzeile nennt keine Zahl dafür" if war is None else
                    f"die Standzeile nennt {war}" +
                    (" – ein Kriterium ist zurückgefallen" if ist > war else
                     " – der Fortschritt ist nicht nachgezogen"))
        err(f"{D11_DATEI}: Kriterium {i + 1} von D-11 ({name}) ist gezählt **{ist}**, "
            f"{richtung}. Der 1.0.0-Stand gehört ausgerechnet und nicht gepflegt; am "
            f"2026-09-15 lagen alle vier Zahlen daneben, ohne dass eine je falsch "
            f"geschrieben worden wäre (CR-2026-070, D-98)")
    if len(geschrieben) != len(gezaehlt):
        err(f"{D11_DATEI}: die Standzeile führt {len(geschrieben)} Zahlen statt "
            f"{len(gezaehlt)}. Erwartet wörtlich: '{soll}' (D-98)")

# ---------------------------------------------------------------------------
# Pruefung 47: Das Statusvokabular jedes Modultraegers
# ---------------------------------------------------------------------------
#
# ANLASS (CR-2026-073 E5, D-108). Das Lebenszyklusmodell gilt seit 0.50.0 fuer JEDEN
# Modultraeger (D-102) - durchgesetzt war das Vokabular fuer genau einen Dateityp. Die
# Skillpruefung meldet seit 0.12.0 einen unbekannten Statuswert, aber nur in einer
# SKILL.md; fuer die uebrigen 56 der 69 Statustraeger war jede Zeichenfolge
# zulaessig, und "| Status | banane |" waere durch jeden Lauf gelaufen. Genau
# dieser Fall stand fuer Skills bis 0.12.0 offen und ist mit FW-VN-01
# geschlossen worden - fuer die anderen Ablagen nie. Solange kein Nicht-Skill gehoben war, hatte die Luecke keinen
# Gegenstand; mit dem ersten gehobenen Nicht-Skill-Traeger hat sie einen (D-102, E5).
#
# DER ZWEITE ANLASS, UND ER IST DER GROESSERE (K-36, D-105). D-102 definierte den
# Modultraeger ueber das Merkmal, das er tragen soll: "jede versionierte Datei mit
# einer Steckbriefzeile Status". Eine solche Definition laesst jeden Traeger
# entkommen, indem er die Zeile weglaesst - und zwoelf taten das, darunter die elf
# normativen Kernmodule, fuer die checklists/11-framework-release.md unter Abschluss
# ausdruecklich einen Status oberhalb von entwurf verlangt. Ein Pruefpunkt ohne
# Gegenstand, in der Checkliste, die 1.0.0 freigibt. Gegenstand 2 dieser Pruefung
# schliesst das Loch: Wer einen Steckbrief fuehrt, fuehrt eine Statuszeile.
#
# WIE EIN STECKBRIEF ERKANNT WIRD (E5). Als die ERSTE Tabelle des Dokuments, die VOR
# der ersten Ueberschrift der Ebene 2 steht und die Kopfzeile "| Attribut | Wert |"
# traegt. Der Zuschnitt ist gemessen und nicht geraten: Eine blosse Suche nach dieser
# Kopfzeile in den ersten sechzig Zeilen trifft auch templates/PLAN_TEMPLATE.md, wo
# sie im KOERPER der Vorlage steht - hinter einer H2, als Formular fuer den Plan, der
# aus ihr entsteht. Das ist kein Steckbrief, und die Datei fuehrt zu Recht keinen
# Status. Gegen den Bestand gemessen erkennt die Regel 81 Steckbriefe (69 mit und 12
# ohne Statuszeile) und keinen Fehltreffer.
#
# VIER GEGENSTAENDE:
#   1. Der verlorene Anker. Findet der Lauf ueberhaupt keinen Steckbrief, bestuende
#      diese Pruefung leise. Sie meldet es deshalb selbst - die Bauform der Pruefungen
#      28, 29, 31, 40 und 46 (D-23).
#   2. Vollstaendigkeit. Jeder Steckbrief fuehrt eine Statuszeile. Das ist der
#      Mechanismus zu D-105; ohne ihn entkaeme der naechste Traeger genauso.
#   3. Vokabular. Das erste Wort des Werts ist einer der fuenf Statuswerte aus
#      08-skill-conventions.md Abschnitt 7. Das ERSTE WORT, weil
#      role-packs/software-development einen Verlaufszusatz traegt ("entwurf
#      (Referenzpack der Erstfassung)") - dieselbe Leseregel wie Pruefung 46 (E6 von
#      CR-2026-070).
#   4. Der Ausfuellschlitz gehoert der Vorlage, und nur ihr (D-104). Eine Vorlage
#      traegt in der Statuszelle einen Schlitz und KEINEN echten Wert - ein echter
#      ginge unveraendert in jede Kopie ueber und waere damit unveraenderlich, ohne
#      dass jemand das entschieden hat; genau dieser Defekt machte Kriterium 3 von
#      D-11 unerreichbar. Umgekehrt traegt ein Traeger, der keine Vorlage ist, keinen
#      Schlitz: Das ist der Preis, den D-104 benannt und nicht abgesichert hat - "wer
#      eine Vorlage kopiert und den Schlitz nicht fuellt, hat ein Pack ohne
#      Statuswert; bei einem Skill faengt das SKILL_STATUS, bei Client-, Role- und
#      Technology-Pack heute nichts".
#
# WAS SIE NICHT LEISTET.
#   * Sie prueft das VOKABULAR, nicht die BERECHTIGUNG. Ob ein Traeger auf pilot
#     stehen darf, entscheidet das Review nach 01-governance.md Abschnitt 5 Punkt 3 -
#     ein Protokoll, das ihn namentlich nennt. Das ist ausdruecklich nicht maschinell
#     (D-102), und diese Pruefung behauptet es nicht.
#   * Sie zaehlt nicht. Den Stand haelt Pruefung 46; hier geht es um die Frage, ob ein
#     Wert ueberhaupt zum Vokabular gehoert.
#   * Vorlagen erkennt sie am Ablageort (templates/ oder ein Verzeichnis _template),
#     also an der Unterstrich-Konvention, die auch Pruefung 31 benutzt - nicht an einem
#     Namen und nicht an einer gepflegten Liste.
STATUS_KOPF_RE = re.compile(r"^\|\s*Attribut\s*\|\s*Wert\s*\|$")
STATUS_ZEILE_RE = re.compile(r"^\|\s*Status\s*\|\s*(.+?)\s*\|$")
# Der Ausfuellhinweis einer Vorlage in der Form, die D-104 gesetzt hat: die Marke, ein
# Semikolon und der Satz, mit welchem Wert die Kopie beginnt.
STATUS_SCHLITZ_RE = re.compile(r"^<TBD: Status; .*\bbeginnt auf entwurf>$")
STATUS_ZELLE = "\\| Status \\| … \\|"


def _status_steckbrief(text: str):
    """Die Zeilen des Steckbriefs eines Dokuments, oder None.

    Der Steckbrief ist die erste Tabelle des Dokuments; sie steht vor der ersten
    Ueberschrift der Ebene 2 und traegt die Kopfzeile "| Attribut | Wert |". Eine
    erste Tabelle mit anderer Kopfzeile bedeutet: kein Steckbrief - und eine Tabelle
    weiter unten ist keiner, auch wenn sie so aussieht (PLAN_TEMPLATE.md).
    """
    zeilen = text.replace("\r\n", "\n").split("\n")
    for nr, roh in enumerate(zeilen):
        z = roh.strip()
        if z.startswith("## "):
            return None
        if not z.startswith("|"):
            continue
        if not STATUS_KOPF_RE.match(z):
            return None
        raus = []
        for weiter in zeilen[nr:]:
            if not weiter.strip().startswith("|"):
                break
            raus.append(weiter.strip())
        return raus
    return None


def _status_ist_vorlage(rest: str) -> bool:
    """Liegt die Datei in einer Vorlagenablage? Unterstrich-Konvention wie Pruefung 31."""
    return rest.startswith("templates/") or "/_template/" in rest


def check_status_vokabular(root: str) -> None:
    """Pruefung 47 (D-105, D-108): Jeder Steckbrief fuehrt einen gueltigen Statuswert."""
    gefunden = 0
    for pfad, rest in _d11_kerndateien(root, (".md",)):
        steckbrief = _status_steckbrief(read(pfad))
        if steckbrief is None:
            continue
        gefunden += 1
        werte = [m.group(1).strip() for m in
                 (STATUS_ZEILE_RE.match(z) for z in steckbrief) if m]

        # --- Gegenstand 2: Vollstaendigkeit -------------------------------------------
        if not werte:
            err(f"{KERN}/{rest}: der Steckbrief führt keine Zeile `{STATUS_ZELLE}`. "
                f"Jeder Träger mit einem Steckbrief durchläuft den Lebenszyklus "
                f"(D-102); bis 0.50.0 definierte sich der Modulträger über genau diese "
                f"Zeile und ließ damit jeden entkommen, der sie wegließ – zwölf taten "
                f"es, darunter die elf normativen Kernmodule, für die FW-CL-11 einen "
                f"Status oberhalb von `entwurf` verlangt (K-36, D-105)")
            continue

        wert = werte[0].strip("`").strip()
        schlitz = wert.startswith("<TBD")
        vorlage = _status_ist_vorlage(rest)

        # --- Gegenstand 4: der Schlitz gehoert der Vorlage, und nur ihr ---------------
        if schlitz and not vorlage:
            err(f"{KERN}/{rest}: die Statuszelle trägt den Ausfüllschlitz '{wert}', "
                f"obwohl die Datei keine Vorlage ist. Wer eine Vorlage kopiert, füllt "
                f"den Schlitz – sonst steht ein Pack ohne Statuswert im Bestand. Das "
                f"ist der Preis, den D-104 benannt und nicht abgesichert hat (D-108)")
            continue
        if vorlage and not schlitz:
            err(f"{KERN}/{rest}: die Statuszelle einer Vorlage trägt den echten Wert "
                f"'{wert}' statt eines Ausfüllschlitzes. Der Steckbrief einer Vorlage "
                f"beschreibt die KOPIE; ein echter Wert geht unverändert in jede Kopie "
                f"über und ist damit unveränderlich, ohne dass jemand das entschieden "
                f"hätte. Genau so war Kriterium 3 von D-11 unerreichbar (D-104). "
                f"Erwartet: '<TBD: Status; … beginnt auf entwurf>'")
            continue
        if schlitz:
            if not STATUS_SCHLITZ_RE.match(wert):
                err(f"{KERN}/{rest}: der Ausfüllschlitz '{wert}' folgt nicht der Form "
                    f"'<TBD: Status; … beginnt auf entwurf>'. Ein Schlitz, der den "
                    f"Anfangswert nicht nennt, lässt die Kopie raten (D-104)")
            continue

        # --- Gegenstand 3: das Vokabular ---------------------------------------------
        erstes = wert.split()[:1]
        if erstes and erstes[0] not in SKILL_STATUS:
            err(f"{KERN}/{rest}: Statuswert '{wert}' gehört nicht zum Vokabular. "
                f"Zulässig sind die fünf Werte aus "
                f"framework/core/08-skill-conventions.md Abschnitt 7 "
                f"({', '.join(sorted(SKILL_STATUS))}); verglichen wird das erste Wort, "
                f"ein Verlaufszusatz in Klammern ist zulässig. Bis 0.50.0 griff diese "
                f"Regel nur in einer SKILL.md – für 56 der 69 Statusträger war jede "
                f"Zeichenfolge erlaubt (D-108)")

    # --- Gegenstand 1: der Anker ------------------------------------------------------
    if not gefunden:
        err(f"{KERN}/: kein einziger Steckbrief gefunden (erste Tabelle des Dokuments "
            f"vor der ersten Überschrift der Ebene 2, Kopfzeile `| Attribut | Wert |`). "
            f"Prüfung 47 hat ihren Gegenstand verloren und würde sonst leise bestehen "
            f"(D-108)")


# --- Pruefung 50 -------------------------------------------------------------------
# Die Ausnahmemenge steht in dem Dokument, das die REGEL traegt - nicht hier. Eine
# Ausnahme im Kopfkommentar einer Pruefung findet niemand, der die Regel liest (0.57.0).
SYNTH_ANKER = "**Belegte synthetische Kennungen"
KLAERUNG_RE = re.compile(r"\bK-\d+\b")
KLAERUNG_ZEILE_RE = re.compile(r"^\|\s*(K-\d+)\s*\|", re.M)


def _synthetische_kennungen(logtext: str) -> set:
    """Die belegten synthetischen Kennungen - aus dem Absatz des Decision Logs.

    Sie gehoeren keinem Klaerungspunkt: Sonden und Gegenproben des Pruefapparats
    brauchen Kennungen, die nie echt vergeben werden (D-23-Nachweis ohne Kollision).
    Leere Menge heisst: der Anker ist verloren - der Aufrufer meldet das.
    """
    for zeile in logtext.splitlines():
        if zeile.lstrip().startswith(SYNTH_ANKER):
            return set(re.findall(r"`([A-Z]+-\d+)`", zeile))
    return set()


def check_klaerungsregister(root: str) -> None:
    """Pruefung 50 (D-147): Jede im Kern genannte Klaerungspunktkennung steht im Register."""
    logpfad = os.path.join(root, KERN, "governance", "DECISION_LOG.md")
    if not os.path.exists(logpfad):
        err(f"{KERN}/governance/DECISION_LOG.md fehlt – Prüfung 50 hat ihren Gegenstand "
            f"verloren; sie bestünde sonst leise (D-23)")
        return
    logtext = read(logpfad)
    synth = _synthetische_kennungen(logtext)
    if not synth:
        err(f"{KERN}/governance/DECISION_LOG.md: der Absatz '{SYNTH_ANKER}…' fehlt oder "
            f"nennt keine Kennung in Backticks – Prüfung 50 leitet ihre Ausnahmemenge "
            f"daraus ab und hat ihren Anker verloren (D-23)")
        return
    gefuehrt = set(KLAERUNG_ZEILE_RE.findall(logtext))
    if not gefuehrt:
        err(f"{KERN}/governance/DECISION_LOG.md: keine Registerzeile '| K-NN |' gefunden – "
            f"Prüfung 50 hat ihren Gegenstand verloren (D-23)")
        return
    fundorte: dict = {}
    for path in iter_text_files(root):
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if not rel.startswith(KERN + "/"):
            continue
        if not path.endswith((".md", ".py", ".json", ".template")):
            continue
        for kennung in set(KLAERUNG_RE.findall(read(path))):
            fundorte.setdefault(kennung, set()).add(rel)
    for kennung in sorted(set(fundorte) - gefuehrt - synth,
                          key=lambda k: int(k.split("-")[1])):
        traeger = sorted(fundorte[kennung])
        err(f"{KERN}/governance/DECISION_LOG.md: '{kennung}' wird in "
            f"{len(traeger)} Träger(n) genannt ({', '.join(traeger[:3])}"
            f"{' …' if len(traeger) > 3 else ''}) und steht in keiner Registerzeile. "
            f"Ein Register, das seinen Gegenstand nicht führt, ist keine Liste offener "
            f"Punkte, sondern eine Auswahl (D-147)")

# --- Pruefung 102: die Form des Klaerungsregisters (CR-2026-158, D-465) -------------------
# ANLASS, NACHGEZAEHLT am 2026-09-29: 114 von 184 Klaerungspunkten standen in der
# Entscheidungstabelle (K-100 nannte 27), eine Leerzeile teilte die Klaerungstabelle, und elf
# erledigte Punkte trugen weiter "offen". Pruefung 50 fragt nur, OB eine Kennung eine Zeile
# hat - nicht, wo sie steht und womit ihr Status beginnt.
#
# ABGELEITET, NICHT GEPFLEGT: Das Vokabular steht in der Legende des Decision Logs, hinter
# '*Klärungspunkte:*' bis zum Satz 'Diese Aufzählung ist vollständig', je Wert in Backticks.
# Ein Wert mit Auslassungszeichen ('eingeplant (…)', 'zusammengelegt mit K-…') gilt als
# Praefix bis dorthin.
#
# WAS SIE NICHT LEISTET: Sie sieht den ANFANG der Statuszelle, nicht, ob er stimmt. Ein
# erledigter Punkt, der "offen" traegt, bleibt eine Frage der Durchsicht (D-465).
# AUSGENOMMEN wie in Pruefung 50: die belegten synthetischen Kennungen des Pruefapparats. Die
# Gegenprobe 46b braucht einen Klaerungspunkt mit dem Wert eines Decision Records - ein
# Sondenfall, kein Registerfall; der erste Abnahmelauf von 1.18.1 hat ihn gemeldet.
P102_LEGENDE = "*Klärungspunkte:*"
P102_LEGENDE_ENDE = "Diese Aufzählung ist vollständig"
P102_ABSCHNITT = "## 1. "
P102_ZUSAMMEN_RE = re.compile(r"^zusammengelegt mit (K-\d+)")


def _p102_vokabular(logtext: str) -> list:
    for zeile in logtext.splitlines():
        if P102_LEGENDE in zeile:
            teil = zeile.split(P102_LEGENDE, 1)[1].split(P102_LEGENDE_ENDE, 1)[0]
            return [w.split("…", 1)[0] for w in re.findall(r"`([^`]+)`", teil)]
    return []


def _p102_kopf(zelle: str) -> str:
    """Der Anfang einer Statuszelle ohne Auszeichnung und ohne vorangestellte Zeichen."""
    return re.sub(r"^[^\w(]+", "", re.sub(r"[*`]", "", zelle))


def check_klaerungsregister_form(root: str) -> None:
    """Pruefung 102 (D-465): Lage und Statusanfang jedes Klaerungspunkts."""
    logpfad = os.path.join(root, KERN, "governance", "DECISION_LOG.md")
    if not os.path.exists(logpfad):
        return  # Pruefung 50 meldet das bereits
    rel = f"{KERN}/governance/DECISION_LOG.md"
    logtext = read(logpfad).replace("\r\n", "\n")
    vokabular = _p102_vokabular(logtext)
    synth = _synthetische_kennungen(logtext)
    if not vokabular:
        err(f"{rel}: die Legende nennt hinter '{P102_LEGENDE}' keinen Statuswert in Backticks – "
            f"Prüfung 102 leitet ihr Vokabular daraus ab und hat ihren Anker verloren (D-23)")
        return
    abschnitt = ""
    status = {}
    for nr, zeile in enumerate(logtext.split("\n"), 1):
        if zeile.startswith("## "):
            abschnitt = zeile
            continue
        m = KLAERUNG_ZEILE_RE.match(zeile)
        if not m:
            continue
        kennung = m.group(1)
        if kennung in synth:
            continue
        if not abschnitt.startswith(P102_ABSCHNITT):
            err(f"{rel}:{nr}: '{kennung}' steht unter '{abschnitt[3:].strip() or 'keiner Überschrift'}' "
                f"statt in der Klärungstabelle (Abschnitt 1). Dort rendert die Zeile unter fremden "
                f"Spaltenköpfen, und wer die offenen Punkte zählt, zählt eine Tabelle zu wenig (D-465)")
        zellen = tabellenzellen(zeile.strip())
        kopf = _p102_kopf(zellen[-1]) if zellen else ""
        status[kennung] = (nr, kopf)
        if not any(kopf.startswith(w) for w in vokabular):
            err(f"{rel}:{nr}: die Statuszelle von '{kennung}' beginnt mit „{kopf[:40]}“ – kein Wert "
                f"der Legende ({', '.join(vokabular)}). Ein Status außerhalb des Vokabulars "
                f"zählt niemand richtig: bis 1.18.1 trugen elf erledigte Punkte „offen“ (D-465)")
        elif re.match(r"^eingeplant \(\s*\)", kopf):
            err(f"{rel}:{nr}: '{kennung}' ist eingeplant, nennt aber kein Ziel in der Klammer (D-465)")
    for kennung, (nr, kopf) in status.items():
        m = P102_ZUSAMMEN_RE.match(kopf)
        if not m:
            continue
        ziel = m.group(1)
        if ziel not in status:
            err(f"{rel}:{nr}: '{kennung}' ist mit '{ziel}' zusammengelegt, das keine Registerzeile "
                f"hat – der Gegenstand wird nirgends geführt (D-465)")
        elif P102_ZUSAMMEN_RE.match(status[ziel][1]):
            err(f"{rel}:{nr}: '{kennung}' ist mit '{ziel}' zusammengelegt, das selbst "
                f"zusammengelegt ist – eine Kette statt eines Ortes (D-465)")


# --- Pruefung 53 -------------------------------------------------------------------
# Der Releaseplan sagt je Posten voraus, wohin Kriterium 2 geht. Die Vorhersagen bilden
# eine KETTE: Was ein Posten erreicht, ist der Ausgangswert des naechsten. Bis 0.60.0 hat
# niemand sie nachgerechnet - und das Protokoll zu 0.56.0 hatte ausdruecklich entschieden,
# das nicht zu tun ("die Zwischenstaende sind Vorhersagen und tragen keinen Anspruch, den
# eine Pruefung einloesen muesste").
#
# DIE ENTSCHEIDUNG IST MIT 0.61.0 UMGEKEHRT, UND DER GRUND IST GEMESSEN (D-153): 0.60.0 hat
# eine Zelle aus einem Posten herausgenommen, die Zahl des Postens nachgezogen und die des
# FOLGEPOSTENS stehen lassen. Die Kette riss um eins, der Plan war in sich widerspruechlich,
# und er ist so gemergt worden.
#
# DIE PRUEFUNG BEURTEILT NICHT, OB EINE VORHERSAGE STIMMT - das kann sie nicht. Sie prueft,
# ob die Tabelle mit sich selbst uebereinstimmt: Kette geschlossen, und der letzte Wert ist
# null, weil Kriterium 2 dort ankommen muss (D-11).
#
# WAS SIE NICHT LEISTET: Die zweite Haelfte desselben Befundes war PROSA - die Zeile nannte
# weiter eine Klasse, die ihre eigene Zahl nicht mehr enthielt. Das ist nicht mechanisch zu
# finden und bleibt Gegenstand des Durchgangs vor dem Commit.
P53_ROADMAP = KERN + "/docs/ROADMAP.md"
P53_UEBERSCHRIFT = "#### Der Releaseplan bis 1.0.0 und darüber hinaus"
P53_KETTE_RE = re.compile(r"Kriterium 2:\s*\*\*(\d+)\s*→\s*(\d+)\*\*")


def check_releaseplan_kette(root: str) -> None:
    """Pruefung 53 (D-153): Die Kriterium-2-Kette des Releaseplans schliesst und endet bei 0."""
    pfad = os.path.join(root, P53_ROADMAP.replace("/", os.sep))
    if not os.path.isfile(pfad):
        err(f"{P53_ROADMAP} fehlt – Prüfung 53 hat ihren Gegenstand verloren; sie bestünde "
            f"sonst leise (D-23)")
        return
    text = read(pfad).replace("\r\n", "\n")
    if P53_UEBERSCHRIFT not in text:
        err(f"{P53_ROADMAP}: die Überschrift '{P53_UEBERSCHRIFT}' ist nicht mehr "
            f"auffindbar. Prüfung 53 liest den Releaseplan darunter und hätte ohne sie "
            f"nichts zu prüfen (D-23)")
        return
    rest = text.split(P53_UEBERSCHRIFT, 1)[1]
    glieder = []
    for zeile in rest.split("\n"):
        if not zeile.startswith("|"):
            if glieder and not zeile.strip():
                continue
        m = P53_KETTE_RE.search(zeile)
        if m:
            glieder.append((int(m.group(1)), int(m.group(2)), zeile.split("|")[1].strip()))
    if len(glieder) < 2:
        err(f"{P53_ROADMAP}: der Releaseplan führt weniger als zwei Vorhersagen zu "
            f"Kriterium 2. Prüfung 53 rechnet eine Kette nach und hätte damit keinen "
            f"Gegenstand mehr (D-23)")
        return
    for (_, ende, posten), (start, _, folge) in zip(glieder, glieder[1:]):
        if ende != start:
            err(f"{P53_ROADMAP}: Die Kriterium-2-Kette des Releaseplans reißt zwischen "
                f"{posten} (endet bei {ende}) und {folge} (beginnt bei {start}). Was ein "
                f"Posten erreicht, ist der Ausgangswert des nächsten; eine Tabelle, die "
                f"sich selbst widerspricht, ist keine Vorhersage (D-153)")
    if glieder[-1][1] != 0:
        err(f"{P53_ROADMAP}: Die Kriterium-2-Kette des Releaseplans endet bei "
            f"{glieder[-1][1]} statt bei 0 ({glieder[-1][2]}). Kriterium 2 von D-11 ist "
            f"erfüllt, wenn der Testkatalog keine offene Zelle mehr führt – ein Plan, der "
            f"nicht dort ankommt, führt nicht bis 1.0.0 (D-153)")

# --- Pruefung 58: Vollstaendigkeit des Decision-Record-Registers -------------------
#
# DIE SCHWESTER VON PRUEFUNG 50, eine Kennungsfamilie weiter. Der gemessene Fall stammt
# aus dem eigenen Pruefapparat: Die Registereintraege der Pruefungen 55 und 56 trugen
# seit 0.63.0 einen Platzhalter an der Stelle der Nummer, waehrend die Meldungen
# derselben Pruefungen die richtige Kennung nannten.
#
# WARUM DAS MUSTER EINEN SCHWANZ HAT. Ein Muster der Form D-\d+ mit abschliessender
# Wortgrenze findet den gemessenen Fall NICHT: Zwischen der letzten Ziffer und dem
# Platzhalterzeichen steht keine Wortgrenze. Deshalb wird alles gelesen, was auf die
# erste Ziffer folgt - und danach geprueft, ob die Form ueberhaupt stimmt. Eine Kennung,
# die die Form knapp verfehlt, ist fuer einen Zaehler sonst unsichtbar, und das ist die
# gefaehrlichere Haelfte: Sie sieht im Fliesstext wie eine Kennung aus.
D58_ERWAEHNUNG_RE = re.compile(r"(?<![\w-])D-\d[\w+]*")
D58_ZEILE_RE = re.compile(r"^\|\s*(D-\d+)\s*\|", re.M)


def check_decisionregister(root: str) -> None:
    """Pruefung 58 (D-169): Jede genannte D-Kennung steht im Register des Decision Logs."""
    logpfad = os.path.join(root, KERN, "governance", "DECISION_LOG.md")
    if not os.path.exists(logpfad):
        return  # Pruefung 50 meldet den fehlenden Traeger bereits
    logtext = read(logpfad)
    synth = _synthetische_kennungen(logtext)
    gefuehrt = set(D58_ZEILE_RE.findall(logtext))
    if not gefuehrt:
        err(f"{KERN}/governance/DECISION_LOG.md: keine Registerzeile '| D-NNN |' "
            f"gefunden - Prüfung 58 hat ihren Gegenstand verloren; sie bestünde sonst "
            f"leise (D-23, D-169)")
        return
    fundorte: dict = {}
    for path in iter_text_files(root):
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if not rel.startswith(KERN + "/"):
            continue
        if not path.endswith((".md", ".py", ".json", ".template")):
            continue
        for kennung in set(D58_ERWAEHNUNG_RE.findall(read(path))):
            fundorte.setdefault(kennung, set()).add(rel)
    for kennung in sorted(set(fundorte) - gefuehrt - synth):
        traeger = sorted(fundorte[kennung])
        ort = (f"{len(traeger)} Träger(n) ({', '.join(traeger[:3])}"
               f"{' …' if len(traeger) > 3 else ''})")
        if re.fullmatch(r"D-\d+", kennung) is None:
            err(f"{KERN}/governance/DECISION_LOG.md: '{kennung}' wird in {ort} genannt "
                f"und ist keine Kennung der Form D-NNN. Eine Kennung, die die Form knapp "
                f"verfehlt, ist für jeden Zähler unsichtbar und liest sich im Fließtext "
                f"trotzdem wie eine (D-169)")
        else:
            err(f"{KERN}/governance/DECISION_LOG.md: '{kennung}' wird in {ort} genannt "
                f"und steht in keiner Registerzeile. Ein Register, das seinen Gegenstand "
                f"nicht führt, ist keine Liste, sondern eine Auswahl (D-169)")


# --- Pruefung 91: die Standueberschrift der Roadmap (D-372) -------------------------
#
# ANLASS, gemessen beim Bau von 1.8.0: "## Stand nach Release 1.4.4" - vier Releases
# alt, direkt ueber "Wird mit jedem Release fortgeschrieben". Bis 0.88.1 stand sie auf
# 0.56.0, zweiunddreissig Releases lang. Eine Ueberschrift, die sagt, von wann sie ist,
# ist eine Zahl mit einem Gegenstand - und der liegt in VERSION.
# GRENZE: Sie prueft die ZAHL der Ueberschrift, nicht den Abschnitt darunter - dieselbe
# Bauform wie 77 (Version, nicht Inhalt). Das Datum in Klammern prueft sie nicht.
P91_ROADMAP = KERN + "/docs/ROADMAP.md"
P91_ANKER = "## Stand nach Release "
P91_RE = re.compile(r"^## Stand nach Release `?(\d+\.\d+\.\d+)`?", re.M)


def check_roadmapstand(root: str) -> None:
    """Pruefung 91 (D-372): Die Standueberschrift der Roadmap nennt VERSION."""
    rpfad = os.path.join(root, *P91_ROADMAP.split("/"))
    vpfad = os.path.join(root, KERN, "VERSION")
    if not os.path.isfile(rpfad) or not os.path.isfile(vpfad):
        return  # Pruefungen 1 und 85 melden den fehlenden Traeger bereits
    text = read(rpfad)
    treffer = P91_RE.findall(text)
    if len(treffer) != 1:
        err(f"{P91_ROADMAP}: die Überschrift '{P91_ANKER}X.Y.Z' steht "
            f"{len(treffer)}-mal statt genau einmal. Prüfung 91 hält sie gegen "
            f"{KERN}/VERSION und bestünde ohne sie leise (D-23, D-372)")
        return
    stand = read(vpfad).strip()
    if treffer[0] != stand:
        err(f"{P91_ROADMAP}: die Standüberschrift nennt Release {treffer[0]}, "
            f"{KERN}/VERSION führt {stand}. Die Überschrift sagt, von wann der Abschnitt "
            f"darunter ist – bei 1.8.0 stand sie vier Releases zurück, direkt über dem "
            f"Satz 'Wird mit jedem Release fortgeschrieben' (D-372)")
