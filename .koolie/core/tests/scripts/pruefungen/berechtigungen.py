"""Die Berechtigungsschicht: Koerbe, Importsteuerung, Skill-Sperren, Agentenprofile,
Werkzeugabbildung, Skillfreigaben, Mandat, Modellaufruf und MCP-Freigaben.

Pruefungen 22, 33, 34, 35, 37, 38, 39, 72, 88, 96, 97, 99, 100 und 101. Teil des
Validators validate-framework.py, seit 1.19.1 nach Gegenstand in Module geteilt (K-174).
Das Register aller Pruefungen steht im Kopfkommentar des Einstiegs, die Grenze jeder
einzelnen in ihrem Kopfkommentar hier."""
from __future__ import annotations

import ast
import json
import os
import re
import sys

from .gemeinsam import (
    _hook_interpreter, _hook_lauf, err, formatgebunden, fremde_praefixe, FRONTMATTER_BLOECKE,
    KERN,
    korb_zerlegung, parse_frontmatter, read, skill_dirs, soll_korbregeln,
    tabellenzellen, TBD_RE, warn, yaml)


def installierte_skills(root: str, man: dict) -> set:
    """Die Skills, die in DIESER Installation liegen - abgeleitet aus der Ablage."""
    rel = man.get("skills_dir")
    if not rel:
        return set()
    ablage = os.path.join(root, *rel.split("/"))
    if not os.path.isdir(ablage):
        return set()
    return {n for n in os.listdir(ablage)
            if os.path.isfile(os.path.join(ablage, n, "SKILL.md"))}


def skillfreigaben(root: str, man: dict) -> set:
    """Die Korbeintraege, die einen Skill DIESER Installation beim Namen nennen.

    \U0001F534 ZWEI PRUEFUNGEN DESSELBEN REPOSITORIUMS STANDEN GEGENEINANDER, UND DAS
    IST GEMESSEN (2026-09-21, Herrichtung von Buendel 5). Pruefung 72 verlangt seit
    `0.81.0` zu jedem Skill der Installation einen Eintrag der Berechtigungsdatei -
    das ist der dritte Teil der Aktivierung eines Packs (D-238). Pruefung 37 hielt
    denselben Eintrag fuer eine AUSWEITUNG, weil die Kernquelle ihn nicht erzeugt:
    Am Messbaum von Buendel 5 meldete sie `Skill(koolie-ticket)` als eine Regel zu
    viel im allow-Korb.

    Damit war die Abhilfe von D-238 in keinem Projekt umsetzbar, ohne den eigenen
    Validator rot zu faerben - und `0.81.0` hat das nicht gesehen, weil es den
    Korbeintrag beim Messen noch gar nicht gab.

      Wer eine Pruefung baut, die etwas VERLANGT, fragt, ob eine andere desselben
      Repositoriums es VERBIETET.

    Ein solcher Eintrag ist keine Ausweitung: Pruefung 72 deckt beide Richtungen ab -
    ein Skill ohne Eintrag und ein Eintrag ohne Skill werden beide gemeldet. Was
    bleibt, ist genau die Menge, die das Projekt durch seine Aktivierung entschieden
    hat, und die Menge wird aus der Skillablage ABGELEITET, nicht gepflegt.
    """
    werkzeuge = tuple(w for w in (man.get("permission_tools") or {}).get("skill") or ()
                      if isinstance(w, str))
    if not werkzeuge:
        return set()
    namen = installierte_skills(root, man)
    return {f"{w}({n})" for w in werkzeuge for n in namen}


def _fremder_skilleintrag(regel: str, man: dict, fremd) -> bool:
    """Der Korbeintrag eines deklarierten fremden Skills (1.21.0, K-31, D-514), auch als Muster."""
    if not fremd:
        return False
    m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\(([^()]*)\)$", regel.strip())
    namen = [w for w in (man.get("permission_tools", {}).get("skill") or []) if isinstance(w, str)]
    return bool(m and m.group(1) in namen and any(m.group(2).startswith(p) for p in fremd))


def check_berechtigungskoerbe(root: str, man: dict) -> None:
    """Pruefung 37: Was die Kernquelle erzeugt, steht in der installierten Datei.

    Warum nicht einfach _core_rules_integrity auf alle Regeln erweitern: Das faengt die
    geloeschte und die verengte Regel, aber weder die ergaenzte allow-Zeile noch den
    geleerten ask-Korb. Die Liste sagt, was fehlen darf - nicht, was zuviel sein darf.

    Ein Platzhalterschlitz (Bash(<TEST_COMMAND>) und die drei Pfadschlitze) ist der
    einzige Teil dieser Datei, der dem Projekt gehoert. Er darf gefuellt sein, gefuellt
    zaehlt er gegen den Ueberschuss - und er darf das Praefixzeichen des Clients nicht
    tragen: clientmap._befehl haengt es an einen offenen Projektplatzhalter bewusst nicht
    an, weil der Overlay Owner dort den vollstaendigen Befehl eintraegt. Von Hand
    nachgetragen macht es aus der Freigabe eines Befehls die Freigabe einer
    Befehlsfamilie - am Piloten am 2026-09-13 so vorgefunden.
    """
    if formatgebunden(man, 37):
        return  # D-346, D-416: diese Ausgabeform erreicht die Pruefung nicht
    rel = man["permissions_file"]
    path = os.path.join(root, *rel.split("/"))
    if not os.path.exists(path):
        return
    try:
        cfg = json.loads(read(path))
    except json.JSONDecodeError:
        return  # check_config hat das bereits gemeldet
    soll = soll_korbregeln(root, man)
    if soll is None:
        return
    if not any(soll.values()):
        err(f"{KERN}/framework/runtime/permissions.json: die Abbildung erzeugt für das "
            f"Client Pack {man.get('client', '?')} keine einzige Regel – Prüfung 37 hätte "
            f"nichts zu vergleichen und bestünde leise")
        return

    perms = cfg.get("permissions", {})
    exec_werkzeuge = tuple(man.get("permission_tools", {}).get("exec", ()))
    praefixzeichen = (man.get("permission_exec_suffix", ":*")
                      if man.get("permission_exec_match") == "prefix" else None)
    skillkorb = skillfreigaben(root, man)

    for korb in ("deny", "ask", "allow"):
        ist = [r for r in perms.get(korb, []) if isinstance(r, str)]
        pflicht, schlitze, ungefuellt, zusatz = korb_zerlegung(ist, soll[korb])
        for regel in pflicht:
            if regel not in ist:
                err(f"{rel}: die Kernquelle erzeugt für den {korb}-Korb die Regel "
                    f"'{regel}'; dort steht sie nicht. Eine fehlende Regel ist eine "
                    f"Lockerung, gleich in welchem Korb – Änderungen an der Regelmenge "
                    f"laufen über einen Änderungsantrag (V10, D-77)")
        if korb == "deny":
            # Eine zusaetzliche deny-Regel ist eine Verschaerfung und deshalb zulaessig.
            continue
        # Der Korbeintrag eines aktivierten Pack- oder Projektskills ist keine
        # Ausweitung, sondern der dritte Teil seiner Aktivierung - Pruefung 72
        # verlangt ihn und deckt beide Richtungen ab (D-238, D-243).
        zusatz = [r for r in zusatz if r not in skillkorb]
        # Ebenso der Eintrag eines deklarierten fremden Skills (1.21.0, K-31, D-514):
        # Pruefung 72 verlangt ihn, Pruefung 111 haelt die Deklaration.
        zusatz = [r for r in zusatz if not _fremder_skilleintrag(r, man, fremde_praefixe(root))]
        # Gedeckt wird ein Ueberschuss nur von den Schlitzen, die NICHT mehr
        # woertlich dastehen - ein woertlich vorhandener Schlitz ist ungefuellt.
        offen = [s for s in schlitze if s not in ungefuellt]
        if len(zusatz) > len(offen):
            err(f"{rel}: der {korb}-Korb führt {len(zusatz)} Regel(n), die die Kernquelle "
                f"nicht erzeugt, bei {len(offen)} gefüllten Platzhalterschlitz(en): "
                f"{', '.join(zusatz)}. Eine zusätzliche Freigabe ist eine Ausweitung und "
                f"nicht Sache des Overlays; ein weiterer freigegebener Befehl gehört in "
                f"Abschnitt 6 des Overlays und damit in die Regelschicht (D-76)")
        if not praefixzeichen or len(zusatz) > len(offen):
            # Kein Praefixzeichen: Dieser Client sperrt Befehle woertlich.
            # Ueberschuss groesser als die offenen Schlitze: Dann ist nicht entschieden,
            # welche Zeile ein gefuellter Schlitz ist und welche eine hinzugefuegte
            # Freigabe - und eine Meldung, die "gefuellter Platzhalterschlitz" sagt, wo
            # keiner ist, sagt etwas anderes als der Fall hergibt. Die Meldung darueber
            # benennt den Ueberschuss bereits richtig.
            continue
        for regel in zusatz:
            teile = regel.split("(", 1)
            if len(teile) != 2 or teile[0] not in exec_werkzeuge:
                continue
            inhalt = teile[1][:-1] if teile[1].endswith(")") else teile[1]
            if inhalt.endswith(praefixzeichen):
                err(f"{rel}: '{regel}' im {korb}-Korb trägt das Präfixzeichen "
                    f"'{praefixzeichen}'. Die Abbildung hängt es an einen gefüllten "
                    f"Projektplatzhalter bewusst nicht an – von Hand nachgetragen macht "
                    f"es aus der Freigabe eines Befehls die Freigabe einer "
                    f"Befehlsfamilie (D-77)")


def check_importsteuerung(root: str, man: dict) -> None:
    """Pruefung 22 (D-37): Die Importsteuerung steht so, wie das Manifest sie abbildet.

    GRENZE - vorab benannt wie bei Pruefung 19: Sie belegt **Anwesenheit und
    Uebereinstimmung, nicht Richtigkeit und erst recht nicht Wirkung.** Dass die
    Einstellung in der Datei steht, heisst nicht, dass sie greift: Die Benutzer-
    konfiguration dieser Arbeitsstation hat Vorrang, in beide Richtungen gemessen
    (K-27). Die Masznahme ist ein Standard, keine Schranke. Was wirkt, misst nur eine
    Sitzung, die den Kontext prueft - nicht das Register des Clients (ERH-02).

    Ein Pack ohne das Feld laeuft durch: Kennt ein Client keinen solchen Mechanismus -
    oder liefert das Framework bewusst keine Vorgabe aus, wie bei claude-code -, bleibt
    es bei der Auskunft im Client Pack (CR-2026-038 E2).
    """
    steuerung = man.get("import_control")
    rechte = man.get("permissions_file")
    if not rechte:
        return
    pfad = os.path.join(root, *rechte.split("/"))
    if not os.path.isfile(pfad):
        return
    try:
        installiert = json.loads(read(pfad))
    except Exception:
        return  # ungueltiges JSON meldet Pruefung 2
    if not steuerung:
        return
    schluessel = steuerung.get("key")
    erwartet = steuerung.get("value")
    if not schluessel:
        err(f"{man.get('client', '?')}/manifest.json: import_control ohne 'key'")
        return
    ist = installiert.get(schluessel)
    if ist is None:
        err(f"{rechte}: Die Importsteuerung '{schluessel}' fehlt. Das Manifest des Packs "
            f"'{man.get('client', '?')}' bildet sie ab (D-37): Das Framework importiert "
            f"keine Regel- und Skillquellen fremder Werkzeugformate. Eine Installation, "
            f"die sie verliert, laedt sie wieder - still")
        return
    if ist != erwartet:
        err(f"{rechte}: Die Importsteuerung '{schluessel}' steht als {json.dumps(ist, ensure_ascii=False)}, "
            f"das Manifest bildet {json.dumps(erwartet, ensure_ascii=False)} ab. Die "
            f"maschinenlesbare Quelle gilt (D-37)")


# Pruefung 33: Die Abbildung von permissions.deny auf die Werkzeugsperre des Clients
# (Befund B01 in seiner Nachfolge, CR-2026-057, D-64 bis D-66).
#
# WARUM SIE DIE ERZEUGTE FASSUNG MISST UND NICHT DIE QUELLE: Genau daran ist B01
# vorbeigekommen. Zwoelf Quellskills fuehrten `permissions: deny: [edit, exec]`, das Feld
# stand in drop_fields, und keine installierte Fassung trug etwas davon - die Quelle sagte
# mehr, als die Installation hielt, und beides war fuer sich dokumentiert.
#
# WARUM SIE IHRE ERWARTUNG SELBST AUSRECHNET: Sie koennte deny_abbilden() aus install.py
# importieren. Dann pruefte sie aber nur noch, DASS der Installer gelaufen ist, nicht dass
# er richtig abbildet - sie teilte jeden Fehler der Abbildung. Die Verbtabelle steht
# deshalb bewusst ein zweites Mal hier. Laufen die beiden auseinander, faellt diese
# Pruefung; das ist der Zweck, nicht ein Versehen.
#
# WAS SIE NICHT LEISTET: Sie misst am erzeugten Text, nicht am Client. Dass
# disallowed-tools wirklich sperrt, belegt die Erhebung
# (tests/protocols/2026-09-13-erhebung-disallowed-tools.md), nicht der Validator.
#
# SEIT 0.40.0 fuehrt sie dasselbe Vokabular wie die Quelle (D-79): read, grep, glob,
# edit, exec. Bis dahin fuehrte sie 'write' und 'search' - zwei Verben der
# Durchsetzungsschicht - und kannte 'grep' und 'glob' nicht, obwohl jede der vierzehn
# Quellen sie im Nachbarfeld desselben Frontmatters nennt. Sie teilte damit genau die
# Luecke, die sie haette fangen sollen.
DENY_VERB_EIMER_33 = {"read": "read", "grep": "search", "glob": "search",
                      "edit": "write", "exec": "exec"}


def _deny_eintraege(fm_text: str) -> list[str]:
    """Die Eintraege unter permissions.deny einer Quelldatei, in ihrer Reihenfolge."""
    m = re.search(r"^permissions:[ \t]*\n((?:[ \t]+\S.*\n)+)", fm_text, re.M)
    if not m:
        return []
    m2 = re.search(r"^([ \t]+)deny:[ \t]*\n((?:[ \t]+-[ \t]+.*\n)+)", m.group(1), re.M)
    if not m2:
        return []
    return [z.strip().lstrip("-").strip() for z in m2.group(2).splitlines() if z.strip()]


def _werkzeugliste(wert) -> list[str]:
    """Ein Frontmatter-Werkzeugfeld als Liste - die Quelle notiert es als Liste, die
    erzeugte Fassung je nach Client als kommagetrennte Zeichenkette (AP2-CC-09)."""
    if isinstance(wert, str):
        return [x for x in re.split(r"[,\s]+", wert) if x]
    return [str(x) for x in (wert or [])]


def _flaches_feld(fm, schluessel: str):
    """Ein einzeiliges Frontmatter-Feld - auch ohne PyYAML (D-364).

    Ohne PyYAML liefert parse_frontmatter nur den Rohtext. Bis 1.6.0 las Pruefung 33
    daraus mit .get() NICHTS und meldete an jeder claude-code-Installation neun Skills
    mit leerem disallowed-tools - falsche Fehler, waehrend die Warnung zu PyYAML
    behauptete, es werde nur "eingeschraenkt" geprueft. Gemessen am 2026-09-25 mit
    Python 3.8 ohne PyYAML; die anderen Packs blieben still. Das Feld ist in der
    erzeugten Fassung eine einzeilige, kommagetrennte Zeichenkette (AP2-CC-09), und
    genau diese Form liest der Rueckfall - eine Listenform bleibt PyYAML vorbehalten.
    """
    fm = fm or {}
    if "_raw" not in fm:
        return fm.get(schluessel)
    for zeile in fm["_raw"].splitlines():
        if zeile.startswith(schluessel + ":"):
            wert = zeile[len(schluessel) + 1:].strip()
            if len(wert) >= 2 and wert[0] == wert[-1] and wert[0] in "\"'":
                wert = wert[1:-1]
            return wert
    return None


def check_skill_deny_abbildung(root: str, man: dict) -> None:
    """Pruefung 33: permissions.deny wird abgebildet, und zwar ohne stille Schranken."""
    fmt = (man or {}).get("skill_frontmatter", {})
    deny_feld = fmt.get("skill_deny_field")
    if not deny_feld:
        return  # Ein Pack, das permissions nicht verwirft, braucht keine Abbildung

    # Die Sonde auf den verlorenen Anker: Diese Pruefung misst eine Abbildung, die in
    # install.py liegt. Verschwindet sie, prueft die Pruefung einen Aufbau, den es nicht
    # mehr gibt - und bestuende dabei leise (D-23).
    inst = os.path.join(root, KERN, "install.py")
    quelle = read(inst) if os.path.isfile(inst) else ""
    # Der zweite Anker hiess bis 0.39.0 DENY_VERB_EIMER und lag in install.py; seit
    # 0.40.0 steht die Bruecke in clientmap (D-78). Der Ankerwechsel ist nachgezogen
    # worden, weil der Sondenlauf ihn gemeldet hat - der Validatorlauf des Repositoriums
    # konnte es nicht, weil Pruefung 33 dort gar nicht laeuft (B02).
    for anker in ("def deny_abbilden(", "clientmap.VERB_BRUECKE"):
        if anker not in quelle:
            err(f"{KERN}/install.py: '{anker}' fehlt. Pruefung 33 misst die Abbildung von "
                f"permissions.deny auf {deny_feld}; ohne sie prueft sie einen Aufbau, den "
                f"es nicht mehr gibt, und bestuende leise (D-23, CR-2026-057)")
            return

    # Was bewusst NICHT abgebildet wird, MUSS deklariert sein - nie erraten (D-47).
    if not str(fmt.get("skill_deny_unmapped") or "").strip():
        err(f"{man.get('client', '?')}/manifest.json: skill_frontmatter.skill_deny_field "
            f"ist gesetzt, aber skill_deny_unmapped fehlt. Befehlsgenaue Verbote der Form "
            f"Exec(git push) sind bei diesem Client nicht ausdrueckbar; was nicht "
            f"abgebildet wird, wird deklariert und nicht verschwiegen (D-47, "
            f"CR-2026-057 E3)")

    eimer = man.get("hook_tools") or {}
    qdir = os.path.join(root, KERN, "framework", "skills")
    idir = os.path.join(root, *man["skills_dir"].split("/"))
    if not os.path.isdir(qdir) or not os.path.isdir(idir):
        return

    for name in sorted(os.listdir(qdir)):
        qpfad = os.path.join(qdir, name, "SKILL.md")
        ipfad = os.path.join(idir, name, "SKILL.md")
        if not os.path.isfile(qpfad) or not os.path.isfile(ipfad):
            continue
        qtext = read(qpfad)
        qkopf = qtext.split("\n---\n", 1)[0][4:] if qtext.startswith("---\n") else ""
        eintraege = _deny_eintraege(qkopf + "\n")

        # Erwartung, unabhaengig ausgerechnet: grobe Verben ueber hook_tools, alles mit
        # Klammer bleibt draussen (CR-2026-057 E3).
        erwartet: list[str] = []
        unabbildbar = [e for e in eintraege if "(" in e]
        for e in eintraege:
            if "(" in e:
                continue
            k = DENY_VERB_EIMER_33.get(e.strip().lower())
            for w in eimer.get(k, []) if k else []:
                if w not in erwartet:
                    erwartet.append(w)

        ifm, _ = parse_frontmatter(read(ipfad))
        ist = _werkzeugliste(_flaches_feld(ifm, deny_feld))
        rel = f"{man['skills_dir']}/{name}/SKILL.md"

        if set(ist) != set(erwartet):
            err(f"{rel}: {deny_feld} traegt {ist or '[]'}; aus permissions.deny der Quelle "
                f"ergibt sich {erwartet or '[]'}. Die Quelle sagt sonst mehr, als die "
                f"Installation haelt - genau das war Befund B01 (D-65, CR-2026-057)")

        # Ein Eintrag mit Klammer wirkt gemessen LAUTLOS gar nicht: Er blockiert nichts und
        # meldet nichts. Er darf in keiner erzeugten Fassung stehen (D-66, E5).
        for w in ist:
            if "(" in w or ")" in w:
                err(f"{rel}: {deny_feld} enthaelt das Argumentmuster '{w}'. Gemessen am "
                    f"2026-09-13 laesst ein solcher Eintrag den Befehl lautlos durchlaufen "
                    f"- wer ihn schreibt, hat gar keine Schranke, nicht bloss eine "
                    f"groebere. Nur der blosse Werkzeugname sperrt (D-66)")

        # Ein Werkzeug in beiden Listen ist ein Widerspruch. Gemessen gewinnt die Sperre -
        # aber ein Skill, der ein Werkzeug zugleich vorabfreigibt und entfernt, sagt zwei
        # Dinge, und eines davon ist falsch.
        doppelt = sorted(set(ist) & set(_werkzeugliste((ifm or {}).get("allowed-tools"))))
        if doppelt:
            err(f"{rel}: {', '.join(doppelt)} steht zugleich in allowed-tools und in "
                f"{deny_feld}. Gemessen gewinnt die Sperre; die Vorabfreigabe daneben ist "
                f"eine Aussage, die nicht stimmt (CR-2026-057)")

        # Traegt die Quelle unabbildbare Eintraege, MUSS das Pack sie deklariert haben -
        # oben schon geprueft; hier bleibt der Hinweis, dass es diesen Skill betrifft.
        if unabbildbar and not str(fmt.get("skill_deny_unmapped") or "").strip():
            err(f"{rel}: die Quelle nennt {len(unabbildbar)} befehlsgenaue(s) Verbot(e), "
                f"die dieser Client nicht ausdruecken kann, und das Pack deklariert es "
                f"nicht (D-47)")


# Pruefung 34: Das Startwerkzeug fuer Unteragenten ist genannt oder seine Abwesenheit
# erklaert (CR-2026-058 E2, D-70).
#
# Bauform wie Pruefung 26 (hook_tools_absent, D-47), eine Ebene weiter. Der Anlass ist ein
# gemessener Befund: Ein Skill kann einen Unteragenten starten, und das Startwerkzeug stand
# in KEINER Werkzeugliste eines Manifests - nicht in hook_tools, nicht in permission_tools,
# nicht in agent_frontmatter.tool_names. Ein Kanal ohne Deklaration ist genau das, was D-47
# abgestellt hat.
#
# Bei claude-code ist gemessen, dass beide Schreibweisen (Agent, Task) in disallowed-tools
# wirken; bei devin-desktop ist NICHTS gemessen, und die leere Liste sagt deshalb etwas
# ueber den Belegstand, nicht ueber den Client.
#
# EINE ERKLAERUNG REICHT NICHT, WENN DAS PACK A1 OHNE VORBEHALT ZUSAGT: Zeile A1
# verspricht ein rein lesendes Reviewprofil. Ein Pack, das diese Zeile auf [TECHNISCH]
# stellt UND keinen offenen Beleg mehr darauf fuehrt, behauptet, dass es
# Unteragenten gibt und dass ihre Werkzeuge beschraenkbar sind - dann ist "kennt kein
# Startwerkzeug" kein zulaessiger Stand.
#
# DER VORBEHALT GEHOERT DAZU, und das hat diese Pruefung bei ihrem ersten Lauf selbst
# gezeigt: Ohne ihn fiel devin-desktop durch. Dessen Zeile A1 steht auf [TECHNISCH], aber
# die Praeambel des Packs sagt ausdruecklich, die Spalte nenne die VORGESEHENE
# Durchsetzungstiefe, und die Zeile trug einen offenen Beleg auf genau die
# Profilwirkung. Die Einstufung allein sagt also nicht, ob eine Zusage schon gilt - das
# sagt die Belegzelle. Eine Pruefung, die beides verwechselt, meldet einen Fehler, wo das
# Pack ehrlich ist (CR-2026-058, Wirkungsnachweis).
#
# SEIT 0.87.0 STEHT DER VORBEHALT AUF DER NACHFOLGEFORM (CR-2026-121 E5, D-291). Die
# Markerform ist abgeschafft; der Nachweisstand steht in der Belegspalte, und eine Zeile
# ohne Beleg sagt BELEG OFFEN mit Grund und Datum. Haette der Vorbehalt den alten
# Suchtext behalten, waere seine Bedingung dauerhaft wahr - eine Ausnahme, die nichts
# mehr ausnimmt (0.57.1), und sie saehe wie Sorgfalt aus. HEUTE HAT SIE KEINEN FALL:
# Beide Packs fuehren agent_start_tools gefuellt, und der Zweig wird nicht erreicht.
# Sie ist Vorsorge fuer das naechste Pack, und Sonde 34e praepariert sie.
#
# WAS DIESE PRUEFUNG NICHT LEISTET: Sie prueft die Deklaration, nicht ihre Richtigkeit. Ob
# der genannte Name beim Client wirklich sperrt, belegt allein eine Erhebung.
def check_agent_startwerkzeug(root: str) -> None:
    """Pruefung 34 (D-70): agent_start_tools ist genannt oder erklaert."""
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
        namen = man.get("agent_start_tools")
        if namen is None:
            err(f"{rel}: Feld 'agent_start_tools' fehlt. Ein Skill kann einen Unteragenten "
                f"starten; mit welchem Werkzeug, gehoert deklariert - und wenn es "
                f"unbekannt oder unerhoben ist, gehoert das ausdruecklich dorthin statt "
                f"verschwiegen (D-70, Bauform wie hook_tools_absent nach D-47)")
            continue
        if not isinstance(namen, list):
            err(f"{rel}: 'agent_start_tools' ist keine Liste")
            continue
        gefuellt = [n for n in namen if isinstance(n, str) and n.strip()]
        abwesend = man.get("agent_start_tools_absent") or []
        notiz = str(man.get("_agent_start_tools_absent_note") or "").strip()
        if gefuellt:
            if abwesend:
                err(f"{rel}: 'agent_start_tools' nennt {gefuellt} und "
                    f"'agent_start_tools_absent' erklaert zugleich eine Abwesenheit. "
                    f"Beides zugleich geht nicht (D-70)")
            continue
        if not abwesend:
            err(f"{rel}: 'agent_start_tools' ist leer, ohne dass "
                f"'agent_start_tools_absent' die Abwesenheit erklaert. Eine leere Liste "
                f"allein sagt nicht, ob der Client kein solches Werkzeug kennt oder ob es "
                f"nur nicht erhoben ist - genau diese Unterscheidung ist der Zweck des "
                f"Feldes (D-70, D-47)")
            continue
        if not notiz:
            err(f"{rel}: 'agent_start_tools_absent' nennt {sorted(abwesend)}, aber "
                f"'_agent_start_tools_absent_note' fehlt oder ist leer. Eine erklaerte "
                f"Abwesenheit ohne Begruendung ist eine Behauptung (D-70, D-47)")
        # Wer A1 auf [TECHNISCH] stellt, sagt zu, dass es Unteragenten gibt und dass ihre
        # Werkzeuge beschraenkbar sind. Dann ist eine Erklaerung kein zulaessiger Stand.
        pack_md = os.path.join(basis, pack, "CLIENT_PACK.md")
        if not os.path.isfile(pack_md):
            continue
        for zeile in read(pack_md).replace("\r\n", "\n").split("\n"):
            if (re.match(r"^\|\s*A1\s*\|", zeile) and "[TECHNISCH]" in zeile
                    and "BELEG OFFEN" not in zeile):
                err(f"{rel}: Zeile A1 des Packs steht auf [TECHNISCH] - das Pack sagt ein "
                    f"rein lesendes Unteragentenprofil technisch zu -, aber "
                    f"'agent_start_tools' ist leer und nur erklaert. Wer Unteragenten "
                    f"zusagt, nennt das Werkzeug, mit dem sie starten (D-70)")
                break



# Pruefung 35: Ein Agentenprofil bekommt kein Startwerkzeug (CR-2026-059 E1, D-73).
#
# Gemessen am 2026-09-13 (tests/protocols/2026-09-13-erhebung-unteragent-tiefe.md,
# Lauf STARTLOS): Ein Profil mit tools: Read, Grep, Glob - genau die Form, die
# koolie-reviewer nach der Abbildung traegt - hat KEIN Startwerkzeug und konnte deshalb
# keinen weiteren Unteragenten starten, dessen Profil weniger beschraenkt waere. Ohne
# diesen Befund waere die Zusage A1 ueber eine zweite Ebene aushebelbar.
#
# WAS DIESE PRUEFUNG IST UND WAS NICHT: Sie faengt heute NICHTS. Die Abbildung
# agent_frontmatter.tool_names kennt gar kein Startwerkzeug, also kann keine erzeugte
# tools-Liste eines enthalten. Sie ist eine VERANKERUNG, keine Behebung - dieselbe
# Bauart wie der fuenfte Gegenstand der Pruefung 32, und sie wird mit derselben
# Ehrlichkeit begruendet: Erweitert jemand tool_names um ein Startwerkzeug, faellt die
# Zusage LAUTLOS, und niemand prueft es. Danach faengt diese Pruefung es.
#
# Geprueft wird an ZWEI Stellen, weil eine allein zu wenig waere:
#   1. Die ABBILDUNG - tool_names darf keinen Namen aus agent_start_tools fuehren.
#   2. Die QUELLE - kein ausgeliefertes Agentenprofil nennt eines direkt. Diese Haelfte
#      faengt den Fall, dass jemand am Profil vorbei an der Abbildung schreibt.
def check_agent_profil_ohne_start(root: str) -> None:
    """Pruefung 35 (D-73): Kein Agentenprofil bekommt ein Startwerkzeug."""
    basis = os.path.join(root, KERN, "clients")
    if not os.path.isdir(basis):
        return
    alle_start = set()
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
        start = {n.strip().lower() for n in (man.get("agent_start_tools") or [])
                 if isinstance(n, str) and n.strip()}
        if not start:
            continue  # ob das zulaessig ist, entscheidet Pruefung 34
        alle_start |= start

        # 1. Die Abbildung darf kein Startwerkzeug fuehren.
        abbildung = (man.get("agent_frontmatter") or {}).get("tool_names") or {}
        for verb, namen in sorted(abbildung.items()):
            for name in (namen if isinstance(namen, list) else []):
                if isinstance(name, str) and name.strip().lower() in start:
                    err(f"{rel}: agent_frontmatter.tool_names bildet das Verb "
                        f"'{verb}' auf '{name}' ab - ein Werkzeug, mit dem ein "
                        f"Unteragent GESTARTET wird (agent_start_tools). Ein "
                        f"Agentenprofil, das es bekommt, kann eine zweite, weniger "
                        f"beschraenkte Ebene oeffnen; die Zusage A1 waere damit "
                        f"aushebelbar (D-73, CR-2026-059)")

    # 2. Kein ausgeliefertes Agentenprofil nennt ein Startwerkzeug direkt.
    #
    # Diese Haelfte laeuft EINMAL ueber die Ablage des Kerns, nicht je Pack: Die Profile
    # sind geteilt (shared_core), die Startwerkzeuge sind es nicht. Geprueft wird gegen
    # die VEREINIGUNG aller Packs - ein Name, der bei einem Pack startet, gehoert in kein
    # Profil, weil dasselbe Profil auch dort ausgeliefert wird.
    if not alle_start:
        return
    adir = os.path.join(root, KERN, "framework", "runtime", "agents")
    if not os.path.isdir(adir):
        err(f"{KERN}/framework/runtime/agents: fehlt. Pruefung 35 misst die "
            f"Agentenprofile des Kerns; ohne die Ablage prueft sie nichts und "
            f"bestuende leise (D-23)")
        return
    for datei in sorted(os.listdir(adir)):
        if not datei.endswith(".md"):
            continue
        rel = KERN + "/framework/runtime/agents/" + datei
        roh = read(os.path.join(adir, datei)).replace("\r\n", "\n")
        teile = roh.split("---")
        if len(teile) < 3:
            err(f"{rel}: kein Frontmatter zwischen zwei '---'. Ohne es prueft "
                f"Pruefung 35 nichts und bestuende leise (D-23)")
            continue
        for name in sorted(alle_start):
            muster = r"(?<![A-Za-z])%s(?![A-Za-z])" % re.escape(name.lower())
            if re.search(muster, teile[1].lower()):
                err(f"{rel}: Das Frontmatter nennt '{name}' - ein Werkzeug, mit dem "
                    f"ein Unteragent GESTARTET wird (agent_start_tools). Ein Profil, "
                    f"das es bekommt, kann eine zweite, weniger beschraenkte Ebene "
                    f"oeffnen, und die Zusage A1 waere aushebelbar (D-73, "
                    f"CR-2026-059)")


def _frontmatter_verben(text: str) -> tuple[list[str], list[str]]:
    """Die groben Verben aus allowed-tools und permissions.deny eines Frontmatters."""
    fm = text.replace("\r\n", "\n")
    if not fm.startswith("---\n") or "\n---\n" not in fm:
        return [], []
    fm = fm.split("\n---\n", 1)[0][4:] + "\n"
    m = re.search(r"^allowed-tools:[ \t]*\n((?:[ \t]+-[ \t]+\S+[ \t]*\n)+)", fm, re.M)
    erlaubt = [x.strip("- \t") for x in m.group(1).strip().split("\n")] if m else []
    verboten: list[str] = []
    m = re.search(r"^permissions:[ \t]*\n((?:[ \t]+\S.*\n)+)", fm, re.M)
    if m:
        m2 = re.search(r"^([ \t]+)deny:[ \t]*\n((?:[ \t]+-[ \t]+.*\n)+)", m.group(1), re.M)
        if m2:
            verboten = [z.strip().lstrip("-").strip() for z in m2.group(2).splitlines()
                        if z.strip() and "(" not in z]
    return erlaubt, verboten


def _quelldateien(root: str) -> list[tuple[str, str]]:
    """Die ausgelieferten Quellen mit Frontmatter-Verben: Skills und Agentenprofile."""
    out: list[tuple[str, str]] = []
    basis = os.path.join(root, KERN, "framework")
    for wurzel, verzeichnisse, dateien in os.walk(basis):
        verzeichnisse[:] = sorted(d for d in verzeichnisse if d != "__pycache__")
        for datei in sorted(dateien):
            if datei != "SKILL.md" and not wurzel.endswith(os.sep + "agents"):
                continue
            if not datei.endswith(".md"):
                continue
            pfad = os.path.join(wurzel, datei)
            out.append((os.path.relpath(pfad, root).replace(os.sep, "/"), read(pfad)))
    return out


def check_werkzeugabbildung(root: str) -> None:
    """Pruefung 38 (D-78 bis D-80): eine Quelle, ein Vokabular, eine Richtung."""
    kern = os.path.join(root, KERN)
    if kern not in sys.path:
        sys.path.insert(0, kern)
    try:
        import clientmap
    except ImportError:
        warn(f"{KERN}/clientmap.py nicht gefunden - Pruefung 38 laeuft nicht")
        return
    # Die Sonde auf den verlorenen Anker (seit 0.32.0): Diese Pruefung findet ihren
    # Gegenstand ueber zwei Namen des Moduls. Verschwinden sie, bestuende sie leise.
    fehlend = [n for n in ("FRONTMATTER_VERBEN", "VERB_BRUECKE")
               if not getattr(clientmap, n, None)]
    if fehlend:
        err(f"{KERN}/clientmap.py: {', '.join(fehlend)} fehlt - Pruefung 38 hat ihren "
            f"Anker verloren und wuerde leise bestehen (D-23, D-78)")
        return
    vokabular = tuple(clientmap.FRONTMATTER_VERBEN)
    bruecke = dict(clientmap.VERB_BRUECKE)

    basis = os.path.join(root, KERN, "clients")
    if not os.path.isdir(basis):
        return
    gesehen = 0
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
        gesehen += 1
        hook = man.get("hook_tools") or {}
        for block in FRONTMATTER_BLOECKE:
            fmt = man.get(block)
            if fmt is None:
                err(f"{rel}: Block '{block}' fehlt - ohne ihn ist nicht entschieden, "
                    f"welche Werkzeugnamen die installierte Fassung traegt (D-78)")
                continue
            abbildung = fmt.get("tool_names")
            if not isinstance(abbildung, dict):
                err(f"{rel}: {block}.tool_names fehlt oder ist kein Objekt")
                continue
            erklaert = fmt.get("tool_names_unmapped") or []
            if not isinstance(erklaert, list):
                err(f"{rel}: {block}.tool_names_unmapped ist keine Liste")
                erklaert = []
            if erklaert and not str(fmt.get("_tool_names_unmapped_note") or "").strip():
                err(f"{rel}: {block}.tool_names_unmapped nennt {sorted(erklaert)}, aber "
                    f"'_tool_names_unmapped_note' fehlt oder ist leer. Ein Verb nicht "
                    f"abzubilden ist eine Aussage ueber den Client oder ueber den "
                    f"Belegstand - sie gehoert begruendet, nicht bloss eingetragen "
                    f"(D-78, Bauform wie hook_tools_absent nach D-47)")
            for schluessel in sorted(abbildung):
                if schluessel not in vokabular:
                    err(f"{rel}: {block}.tool_names bildet '{schluessel}' ab - kein "
                        f"Verb des Frontmatter-Vokabulars {list(vokabular)}. Eine "
                        f"Quelle des Kerns kann es nicht schreiben, die Abbildung "
                        f"laeuft also ins Leere (D-78)")
            for verb in vokabular:
                hat = verb in abbildung
                erklaert_hier = verb in erklaert
                if hat and erklaert_hier:
                    err(f"{rel}: {block} bildet das Verb '{verb}' ab UND erklaert es "
                        f"zugleich fuer nicht abgebildet. Beides zugleich geht nicht - "
                        f"eine der beiden Aussagen ist falsch (D-78)")
                elif not hat and not erklaert_hier:
                    err(f"{rel}: {block}.tool_names kennt das Werkzeugverb '{verb}' "
                        f"nicht, und tool_names_unmapped erklaert die Abwesenheit "
                        f"nicht. Bis 0.39.0 wurde das Verb dann WOERTLICH als "
                        f"Werkzeugname durchgereicht; eine Luecke allein ist keine "
                        f"Aussage (D-78)")

            # Gegenstand 3: Die Sperrliste darf nicht enger sein als die Vorabfreigabe.
            #
            # Die Regel vergleicht zwei Listen und setzt damit voraus, dass sie
            # DENSELBEN Namensraum fuehren. Bei claude-code tun sie das; bei
            # devin-desktop nicht, und das ist gemessen (2026-09-14, D-88): Sein
            # Frontmatter kennt ein eigenes, normalisiertes Vokabular - read,
            # grep, glob, edit, exec, web_search -, waehrend seine Laufzeit das
            # glob-foermige Werkzeug find_file_by_name nennt. Ein Vergleich der
            # beiden Listen meldete dann einen Unterschied, den es nicht gibt.
            #
            # Ein Pack sagt das mit tool_names_namespace: 'eigen'. WAS DABEI
            # VERLOREN GEHT, gehoert gesagt: Fuer ein solches Pack prueft niemand
            # mehr, ob die Sperre die Vorabfreigabe deckt - die Frage von D-80
            # bleibt dort offen und ist nur anders gestellt, nicht beantwortet.
            if str(fmt.get("tool_names_namespace") or "") == "eigen":
                if not str(fmt.get("_tool_names_note") or "").strip():
                    err(f"{rel}: {block}.tool_names_namespace ist 'eigen', aber "
                        f"'_tool_names_note' fehlt oder ist leer. Einen eigenen "
                        f"Namensraum zu erklaeren nimmt die Richtungsregel von "
                        f"D-80 ausser Kraft - das gehoert begruendet, nicht "
                        f"bloss eingetragen (D-88)")
                continue
            for verb in sorted(abbildung):
                ziel = bruecke.get(verb)
                if ziel is None or ziel not in hook:
                    continue
                vorab = {str(x) for x in (abbildung.get(verb) or [])}
                sperre = {str(x) for x in (hook.get(ziel) or [])}
                zuviel = sorted(vorab - sperre)
                if zuviel:
                    err(f"{rel}: {block}.tool_names['{verb}'] gibt {zuviel} vorab "
                        f"frei, hook_tools['{ziel}'] fuehrt sie nicht. Die Sperrliste "
                        f"ist damit enger als die Vorabfreigabe: Ein Skill, der "
                        f"'{verb}' freigibt und '{verb}' sperrt, bekaeme ein Werkzeug "
                        f"freigegeben, das die Sperre nicht erfasst. Die umgekehrte "
                        f"Abweichung ist zulaessig (D-80)")
    if not gesehen:
        err(f"{KERN}/clients: kein Manifest gefunden. Pruefung 38 misst die "
            f"Werkzeugabbildungen der Packs; ohne sie prueft sie nichts und bestuende "
            f"leise (D-23)")

    # Gegenstand 4: die Quellen selbst.
    quellen = _quelldateien(root)
    if not quellen:
        err(f"{KERN}/framework: keine Quelle mit Frontmatter gefunden. Pruefung 38 "
            f"misst die Verben der ausgelieferten Skills und Agentenprofile; ohne sie "
            f"prueft der vierte Gegenstand nichts und bestuende leise (D-23)")
        return
    for rel, text in quellen:
        erlaubt, verboten = _frontmatter_verben(text)
        for feld, verben in (("allowed-tools", erlaubt), ("permissions.deny", verboten)):
            for verb in verben:
                if verb not in vokabular:
                    err(f"{rel}: {feld} nennt das Verb '{verb}' - das Vokabular des "
                        f"Frontmatters kennt nur {list(vokabular)}. In allowed-tools "
                        f"wurde es bis 0.39.0 woertlich als Werkzeugname "
                        f"durchgereicht, in permissions.deny fiel es lautlos aus "
                        f"(D-78, D-79)")



# ---------------------------------------------------------------------------
# Pruefung 39: Die Vorabfreigabe des Skillaufrufs deckt sich mit den ausgelieferten
# Skills, und die Skillwahl steht an allen vier Traegern (CR-2026-063, D-81 bis D-84).
#
# ANLASS. Die Wurzel-Anweisungsdatei fordert seit jeher, fuer Standardaufgaben die
# Skills zu nutzen - und die ausgelieferte Berechtigungsdatei kannte das Werkzeug, mit
# dem das geht, in KEINEM Korb. Gemessen am 2026-09-14
# (tests/protocols/2026-09-14-erhebung-skillaufruf.md): Der Aufruf wurde abgewiesen, die
# Sitzung las die SKILL.md ersatzweise als Datei, und die Ausgabe sah aus wie ein
# gelungener Lauf. Die Ursache lag nicht im Pack, sondern im Vokabular der Kernquelle -
# sechs Verben, keines fuer den Skillaufruf.
#
# VIER GEGENSTAENDE:
#   1. Der verlorene Anker. Fehlt das Skillverzeichnis des Kerns oder fuehrt
#      permissions.json keine einzige skill-Regel, meldet diese Pruefung das selbst -
#      sonst bestuende sie leise (D-23).
#   2. Die Deckung in BEIDE Richtungen. Jeder ausgelieferte Skill hat genau eine
#      allow-Regel, und jede Regel nennt einen ausgelieferten Skill. Das ist der Preis
#      von D-81 E3: Die Regeln stehen in der Datei, statt aus dem Verzeichnis erzeugt zu
#      werden - nach D-53 IST der Inhalt dieser Datei die Berechtigung. Ohne diese
#      Pruefung waere das die zweite Liste fuer dieselbe Sache, also der Befundtyp von
#      CR-2026-062.
#   3. Kein Musterzeichen. Gemessen am 2026-09-14 (D-82): Der Vergleich ist woertlich.
#      Skill(koolie-*) weist den Aufruf ab, Skill(koolie-code-explain) laesst ihn durch,
#      Skill(koolie-plan) weist koolie-code-explain ab (Kontrolllauf). Eine Regel mit * oder ?
#      saehe richtig aus und gaebe LAUTLOS NICHTS frei - die Bauform von D-66 mit
#      umgekehrtem Vorzeichen.
#   4. Die vier Regeltraeger. Die Skillwahl stand vor 0.41.0 an fuenf Stellen und
#      erreichte den Agenten an keiner verbindlich. Sie steht jetzt in der
#      Wurzel-Anweisungsdatei, in der always-on-Kurzfassung, im Arbeitsmodell und in den
#      Prompting-Regeln. Geprueft wird die ANWESENHEIT je Traeger, nicht der Wortlaut:
#      Eine Pruefung, die Prosa vergleicht, bricht bei jeder Umformulierung.
#
# WAS SIE HEUTE FAENGT: nichts - Gegenstand 2 und 3 sind mit demselben Release entstanden
# und passen per Konstruktion zu sich selbst; Gegenstand 4 ebenso. Das ist die Lage von
# Pruefung 37 und dieselbe Ehrlichkeit: Der Gegenbeweis gegen den Vorstand ist hier eine
# KONSTRUKTION, kein Abzaehlen, und was die Pruefung wert ist, haengt an ihren Sonden.
#
# WAS SIE NICHT LEISTET: Sie belegt nicht, dass der Agent den Skill waehlt. Das ist ein
# Sitzungstest, und er ist nicht gefahren. Sie belegt, dass die Freigabe zur Skillmenge
# passt und dass keiner der vier Traeger die Regel verliert.
SKILLWAHL_TRAEGER = (
    ("framework/runtime/root-instruction.md",
     "Bevor du einen Schritt beginnst"),
    ("framework/runtime/rules/00-framework-core.md",
     "Skillwahl vor dem Schritt"),
    ("framework/core/05-working-model.md",
     "ist er der vorgesehene Weg des Schrittes"),
    ("framework/core/06-prompting-rules.md",
     "Skills bevorzugen \u2013 von beiden Seiten"),
)


def _skill_regeln(root: str) -> list[str] | None:
    """Die Aufrufnamen aus den skill-Regeln der Kernquelle, oder None ohne Quelle."""
    pfad = os.path.join(root, KERN, "framework", "runtime", "permissions.json")
    if not os.path.exists(pfad):
        return None
    try:
        quelle = json.loads(read(pfad))
    except json.JSONDecodeError:
        return None
    return [r.get("pattern", "") for r in quelle.get("allow", [])
            if isinstance(r, dict) and r.get("tool") == "skill"]


def check_skillfreigabe(root: str) -> None:
    """Pruefung 39 (D-81 bis D-84): Freigabe, Skillmenge und Regeltraeger decken sich."""
    verzeichnis = os.path.join(root, KERN, "framework", "skills")
    if not os.path.isdir(verzeichnis):
        err(f"{KERN}/framework/skills: fehlt. Pruefung 39 misst die Vorabfreigabe des "
            f"Skillaufrufs gegen die ausgelieferten Skills; ohne das Verzeichnis "
            f"prueft sie nichts und bestuende leise (D-23)")
        return
    ausgeliefert = sorted(
        name for name in os.listdir(verzeichnis)
        if os.path.isfile(os.path.join(verzeichnis, name, "SKILL.md")))

    regeln = _skill_regeln(root)
    if regeln is None:
        err(f"{KERN}/framework/runtime/permissions.json: nicht lesbar. Pruefung 39 hat "
            f"ihren Anker verloren und bestuende sonst leise (D-23)")
        return
    if not regeln:
        err(f"{KERN}/framework/runtime/permissions.json: keine einzige allow-Regel mit "
            f"dem Verb 'skill'. Die Wurzel-Anweisungsdatei fordert in Abschnitt 17 die "
            f"Nutzung der Skills; ohne Freigabe laeuft jeder Aufruf in die Rueckfrage "
            f"und im rueckfragefreien Betrieb in die Abweisung (D-81)")
        return

    # Gegenstand 2: die Deckung, in beide Richtungen.
    for name in ausgeliefert:
        if name not in regeln:
            err(f"{KERN}/framework/runtime/permissions.json: der ausgelieferte Skill "
                f"'{name}' hat keine allow-Regel. Sein Aufruf laeuft in die Rueckfrage, "
                f"und der Fehlschlag ist stumm - die Sitzung liest die SKILL.md "
                f"ersatzweise als Datei, ohne die Werkzeugbeschraenkung des Skills "
                f"(D-81, D-83)")
    for name in regeln:
        if name not in ausgeliefert:
            err(f"{KERN}/framework/runtime/permissions.json: die allow-Regel fuer "
                f"'{name}' nennt keinen ausgelieferten Skill. Eine Vorabfreigabe fuer "
                f"einen Skill, den es nicht gibt, ist eine Zusage ohne Gegenstand "
                f"(D-81)")
    doppelt = sorted({n for n in regeln if regeln.count(n) > 1})
    if doppelt:
        err(f"{KERN}/framework/runtime/permissions.json: doppelte skill-Regel(n) fuer "
            f"{', '.join(doppelt)}")

    # Gegenstand 3: kein Musterzeichen.
    for name in regeln:
        if any(z in name for z in "*?["):
            err(f"{KERN}/framework/runtime/permissions.json: die skill-Regel '{name}' "
                f"traegt ein Musterzeichen. Der Vergleich ist woertlich - gemessen am "
                f"2026-09-14 (D-82): Skill(koolie-*) weist den Aufruf ab. Eine Regel mit "
                f"Muster saehe richtig aus und gaebe lautlos nichts frei")

    # Gegenstand 4: die vier Regeltraeger.
    for rel, anker in SKILLWAHL_TRAEGER:
        pfad = os.path.join(root, KERN, *rel.split("/"))
        if not os.path.exists(pfad):
            err(f"{KERN}/{rel}: fehlt. Pruefung 39 misst dort die Skillwahl (D-84)")
            continue
        if anker not in read(pfad):
            err(f"{KERN}/{rel}: die Skillwahl fehlt (gesucht: '{anker}'). Sie stand vor "
                f"0.41.0 an fuenf Stellen und erreichte den Agenten an keiner "
                f"verbindlich; faellt ein Traeger weg, faellt sie leise zurueck (D-84)")


# --- Pruefung 72: Ein aktiviertes Pack steht auch im Berechtigungskorb -------------
#
# ANLASS, UND ER IST GEMESSEN (2026-09-21, Vorbedingungsdurchgang von Buendel 5,
# D-238). Bundel 5 misst `koolie-ticket`, den einzigen Skill dieses Frameworks, der
# nicht im Kern liegt. Nach der Aktivierung WORTGETREU nach
# `framework/role-packs/README.md` - Laufzeitfassung kopiert, Skillverzeichnis kopiert -
# und nach `install.py --update` stand im Messbaum:
#
#     Skillverzeichnisse in .claude/skills/        13
#     Skill(...)-Eintraege im allow-Korb           12
#     Skill(koolie-ticket)                        fehlt
#     validate-framework.py --strict-overlay       0 Fehler, 0 Warnungen
#
# DIE REGELSCHICHT DES PACKS WAR VOLLSTAENDIG, DIE TECHNISCHE KANNTE ES NICHT. Und
# `defaultMode` steht auf `default`: Ein nicht genannter Aufruf faellt in den
# Rueckfragekorb, im nicht-interaktiven Betrieb also in die Abweisung. D-81 hat genau
# diesen Ausgang beschrieben - "der Fehlschlag ist stumm; die Sitzung liest die
# SKILL.md ersatzweise als Datei, OHNE die Werkzeugbeschraenkung des Skills".
#
# WARUM PRUEFUNG 39 ES NICHT SIEHT, OBWOHL SIE DAFUER GEBAUT IST. Sie haelt
# `framework/runtime/permissions.json` gegen `framework/skills/` - Regelmenge des Kerns
# gegen Skills des Kerns, beides Ebene 3, und dort deckt es sich (12 zu 12). Ein
# Packskill ist Ebene 6 und kommt in keiner der beiden Mengen vor. Derselbe Zuschnitt,
# der D-234 drei Tage zuvor unterlaufen ist: eine Stelle, die `framework/skills` sagt
# und `framework/role-packs/<pack>/skills` meint.
#
# WARUM DIE ABHILFE NICHT IN permissions.json LIEGT. Eine allow-Regel dort traegt JEDE
# Installation - auch die, die das Pack nicht aktiviert hat. Das waere "eine
# Vorabfreigabe fuer einen Skill, den es nicht gibt", und genau das verbietet
# Pruefung 39 in ihrer Gegenrichtung. Die Aktivierung ist eine Projektentscheidung
# (README Punkt 4) und hat deshalb DREI Teile, nicht zwei; diese Pruefung setzt den
# dritten durch, und zwar dort, wo er hingehoert: in der Installation.
#
# WARUM SIE BEI EINEM CLIENT SCHWEIGT, UND WARUM DAS KEINE STILLE NULL IST. Das
# Manifest fuehrt die Schreibweise des Skillaufrufs als `permission_tools.skill`. Bei
# `claude-code` steht dort `["Skill"]`, bei `devin-desktop` eine LEERE Liste - erhoben
# am 2026-09-14 (D-89): Der Aufruf ist dort zwar ein Werkzeugaufruf, aber es ist keine
# Schreibweise bekannt, mit der eine Regel ihn beim Namen nennt. Eine leere Liste ist
# deklariert; ein FEHLENDES Feld ist ein Befund, und den meldet sie - dieselbe
# Trennlinie zwischen "nicht abgebildet" und "gibt es nicht", die D-155 zieht.
P72_MUSTER = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\(([^()]*)\)$")
P72_SELBSTPROBE = "Skill(role-beispiel)"  # SYNTHETISCH


def _p72_eintraege(cfg) -> list:
    """Jeder Regeleintrag der Berechtigungsdatei, ueber alle Koerbe.

    Ueber die Koerbe zu laufen statt `allow` zu nennen ist Absicht: Ein Eintrag in
    `ask` oder `deny` NENNT den Skill ebenso, und wer nur `allow` liest, meldet ein
    ausdrueckliches Verbot als fehlenden Eintrag.
    """
    aus: list = []

    def rein(o) -> None:
        if isinstance(o, dict):
            for v in o.values():
                rein(v)
        elif isinstance(o, list):
            for x in o:
                rein(x)
        elif isinstance(o, str):
            aus.append(o)

    rein(cfg.get("permissions", cfg) if isinstance(cfg, dict) else cfg)
    return aus


def check_pack_im_korb(root: str, man: dict) -> None:
    """Pruefung 72 (D-238): Jeder Skill der Installation steht im Berechtigungskorb."""
    if formatgebunden(man, 72):
        return  # D-346, D-416: diese Ausgabeform erreicht die Pruefung nicht
    if not P72_MUSTER.match(P72_SELBSTPROBE):
        err(f"Pruefung 72: das eigene Muster trifft {P72_SELBSTPROBE!r} nicht mehr - "
            f"sie haette ihren Gegenstand verloren und bestuende leise (D-23, D-238)")
        return
    pack = man.get("client", "?")
    werkzeuge = man.get("permission_tools")
    if not isinstance(werkzeuge, dict) or "skill" not in werkzeuge:
        err(f"clients/{pack}/manifest.json: Feld permission_tools.skill fehlt. Ein "
            f"Pack fuehrt es, notfalls leer - der Unterschied zwischen „nicht "
            f"abgebildet“ und „gibt es nicht“ gehoert deklariert und nicht aus einem "
            f"fehlenden Feld erraten (D-155, D-238)")
        return
    namen = [w for w in (werkzeuge.get("skill") or []) if isinstance(w, str)]
    if not namen:
        return  # Deklariert leer (devin-desktop, D-89) - keine Schreibweise bekannt
    rel_skills = man.get("skills_dir")
    rel_perm = man.get("permissions_file")
    if not rel_skills or not rel_perm:
        return
    ablage = os.path.join(root, *rel_skills.split("/"))
    pfad = os.path.join(root, *rel_perm.split("/"))
    if not os.path.isdir(ablage) or not os.path.isfile(pfad):
        return  # Keine Installation an dieser Wurzel - hier gibt es nichts zu decken
    try:
        cfg = json.loads(read(pfad))
    except json.JSONDecodeError:
        return  # Pruefung 3 meldet das bereits
    im_baum = sorted(n for n in os.listdir(ablage)
                     if os.path.isfile(os.path.join(ablage, n, "SKILL.md")))
    genannt = []
    if man.get("permissions_format") == "kiro-agent":
        # Das Agentenprofil nennt einen Skill nicht als Werkzeug(Name), sondern als
        # Muster einer Regel mit der Faehigkeit des Skillaufrufs (D-414, D-416).
        regeln = ((cfg.get("permissions") or {}).get("rules") or []
                  if isinstance(cfg, dict) else [])
        for regel in regeln:
            if isinstance(regel, dict) and regel.get("capability") in namen:
                genannt.extend(m for m in (regel.get("match") or [])
                               if isinstance(m, str) and m.strip())
    for eintrag in ([] if genannt else _p72_eintraege(cfg)):
        m = P72_MUSTER.match(eintrag.strip())
        if m and m.group(1) in namen and m.group(2):
            genannt.append(m.group(2))
    # Ein deklarierter fremder Skill (1.21.0, K-31) ist auch durch ein Muster seines
    # Praefixes genannt, etwa Skill(openspec-*) - der Korb bleibt Pflicht, nur die
    # Schreibweise ist die des fremden Rahmenwerks.
    fremd = fremde_praefixe(root)
    muster = [g[:-1] for g in genannt if g.endswith("*")]
    for name in im_baum:
        if name not in genannt and not (
                any(name.startswith(p) for p in fremd)
                and any(m and name.startswith(m) for m in muster)):
            err(f"{rel_perm}: der Skill '{name}' liegt in {rel_skills}/, wird aber "
                f"von keinem Eintrag der Berechtigungsdatei genannt. Sein Aufruf "
                f"faellt in den Rueckfragekorb und im rueckfragefreien Betrieb in die "
                f"Abweisung; die Sitzung liest die SKILL.md dann ersatzweise als "
                f"Datei, ohne die Werkzeugbeschraenkung des Skills (D-81). Bei einem "
                f"Pack-Skill ist das der dritte Teil der Aktivierung "
                f"(framework/role-packs/README.md), nicht ein Schritt von install.py "
                f"(D-238)")
    for name in sorted(set(genannt)):
        if name not in im_baum and not name.endswith("*"):
            err(f"{rel_perm}: der Eintrag fuer '{name}' nennt keinen Skill in "
                f"{rel_skills}/. Eine Freigabe fuer einen Skill, den diese "
                f"Installation nicht hat, ist eine Zusage ohne Gegenstand (D-81, "
                f"D-238)")


# ---------------------------------------------------------------------------
# PRUEFUNG 88: DIE DATEI, DIE DIE WURZEL-ANWEISUNG VERDRAENGT
# ---------------------------------------------------------------------------
# ANLASS, UND ER IST DER SCHWERSTE BEFUND DER ERHEBUNG VON 1.3.0 (D-341, hier
# durchgesetzt mit CR-2026-133). Bei einem Client kann eine Datei NEBEN der
# Wurzel-Anweisung diese vollstaendig ersetzen: Liegt sie im Projekt, steht die
# Wurzel-Anweisung des Frameworks in KEINER Nachricht der Sitzung - gemessen mit
# Gegenprobe. Ein aufnehmendes Projekt, das die Datei in sein `.gitignore` schreibt -
# der naheliegende Ort fuer eine persoenliche Fassung -, haette damit eine
# unversionierte Ebene 1 je Arbeitsplatz.
#   ➡️ Eine Wurzel-Anweisung, die eine ungepruefte Datei im selben Verzeichnis ersetzen
#      kann, ist keine Ebene 1 - sie ist ein Standard.
# Welches Pack eine solche Datei kennt, sagt das Manifest (root_instruction_override).
# Der Schutz besteht aus drei Teilen, und dies ist der dritte: Der deny-Korb stellt die
# Datei schreibgeschuetzt, der Schutz-Hook fuehrt sie in seinen Mustern - und diese
# Pruefung MELDET SIE, wenn sie trotzdem da ist. Die ersten beiden verhindern, dass der
# Agent sie anlegt; ein Mensch kann es weiterhin, und dann soll es nicht still bleiben.
def check_verdraengende_wurzelanweisung(root: str, man: dict) -> None:
    """Pruefung 88 (D-341, D-347): Keine Datei, die die Wurzel-Anweisung verdraengt."""
    if not man.get("root_instruction_override"):
        return
    rel = (man.get("runtime_placeholders") or {}).get("<ROOT_INSTRUCTION_LOCAL>")
    if not rel:
        err(f"clients/{man.get('client', '?')}/manifest.json: root_instruction_override "
            f"ist gesetzt, aber <ROOT_INSTRUCTION_LOCAL> fehlt in runtime_placeholders – "
            f"Prüfung 88 wüsste nicht, welche Datei sie meldet (D-23)")
        return
    if os.path.exists(os.path.join(root, *rel.split("/"))):
        err(f"{rel}: liegt im Projekt und VERDRÄNGT bei diesem Client die "
            f"Wurzel-Anweisung {man.get('root_instruction_file', '?')} vollständig – "
            f"deren Text steht dann in keiner Nachricht der Sitzung. Ebene 1 der "
            f"Prioritätshierarchie wäre damit durch eine ungeprüfte Datei ersetzt, und "
            f"bis 1.4.0 meldete es nichts (D-341)")


# ---------------------------------------------------------------------------
# PRUEFUNG 96: DAS AGENTENPROFIL, DAS DIE BERECHTIGUNGEN TRAEGT, IST AUCH DAS AKTIVE
# ---------------------------------------------------------------------------
# ANLASS, GEMESSEN AM 2026-09-26 (CR-2026-150, D-414). Beim Client kiro stehen die
# Berechtigungen des Frameworks in einem Agentenprofil, und sie wirken NUR, wenn es der
# aktive Agent ist. Die Einstellungsdatei des Arbeitsbereichs waehlt es. Drei Befunde
# machen daraus eine Pruefung:
#   * Zeigt die Einstellung auf ein Profil, das es nicht gibt, oder ist das Profil kein
#     gueltiges JSON, faellt der Client STILL auf seinen eingebauten Agenten zurueck -
#     eine Warnung auf stderr, und .env war lesbar (K15, K16).
#   * Eine Regel mit unbekannter Faehigkeit ueberspringt er und meldet es nur in seinem
#     Protokoll (K23). Sein eigenes Pruefkommando `agent validate` endet auch bei
#     kaputtem JSON mit Exit 0 und prueft keine Faehigkeit (K22).
#   * Die Pruefungen der Koerbe (37 und Verwandte) lesen deny/ask/allow und erreichen
#     diese Form nicht (D-416). Diese Pruefung tritt fuer das Agentenprofil an ihre
#     Stelle.
# GEPRUEFT: (a) die Einstellungsdatei traegt die Werte des Manifests; (b) das Profil ist
# ein JSON-Objekt mit dem Namen, den die Einstellung waehlt; (c) jede Regel hat eine
# bekannte Faehigkeit, einen bekannten Effekt und eine Liste von Mustern; (d) jedes
# deny- und ask-Muster der Kernquelle steht mit seinem Effekt (und seiner Ausnahme) im
# Profil, und kein allow-Muster steht darin, das die Kernquelle nicht erzeugt - ausser
# dem Namen eines installierten Skills (Bauform von Pruefung 72, D-238).
# ⚠️ GRENZEN, BENANNT: Ein Muster mit offenem Platzhalter (<EXCLUDED_PATHS> ...) gehoert
# dem Projekt und wird nicht verglichen. Und die Pruefung misst die Dateien, nicht den
# Start: Wer den Client mit --agent auf einen anderen Agenten stellt, arbeitet ohne diese
# Regeln, und keine Pruefung sieht es.
P96_EFFEKTE = ("deny", "ask", "allow")


def _p96_regeln(cfg: dict) -> list:
    return ((cfg.get("permissions") or {}).get("rules") or []) if isinstance(cfg, dict) else []


def check_agentenprofil(root: str, man: dict) -> None:
    """Pruefung 96 (D-414): Die Einstellung waehlt das Profil, und das Profil traegt."""
    if man.get("permissions_format") != "kiro-agent":
        return
    pack = man.get("client", "?")
    kern = os.path.join(root, KERN)
    if kern not in sys.path:
        sys.path.insert(0, kern)
    try:
        import clientmap
    except ImportError:
        return  # check_config meldet das fehlende Abbildungsmodul bereits
    if not hasattr(clientmap, "kiro_regeln") or not hasattr(clientmap, "KIRO_FAEHIGKEITEN"):
        err(f"{KERN}/clientmap.py: 'kiro_regeln' oder 'KIRO_FAEHIGKEITEN' fehlt – Prüfung "
            f"96 hat ihren Gegenstand verloren und bestünde sonst leise (D-23)")
        return
    # (a) Die Einstellungsdatei.
    einst_rel = man.get("client_settings_file")
    soll = man.get("client_settings") or {}
    profil_rel = man.get("permissions_file")
    if not einst_rel or not soll or not profil_rel:
        err(f"clients/{pack}/manifest.json: client_settings_file, client_settings und "
            f"permissions_file gehören zusammen – ohne sie weiß Prüfung 96 nicht, welche "
            f"Datei das Profil wählt (D-414)")
        return
    einst_pfad = os.path.join(root, *einst_rel.split("/"))
    profil_pfad = os.path.join(root, *profil_rel.split("/"))
    if not os.path.exists(einst_pfad) and not os.path.exists(profil_pfad):
        return  # keine Installation dieses Packs an dieser Wurzel
    if not os.path.isfile(einst_pfad):
        err(f"{einst_rel}: fehlt. Ohne diese Datei startet der Client mit seinem "
            f"eingebauten Agenten und seiner Standard-Engine – die Berechtigungen in "
            f"{profil_rel} wirken dann nicht, und nichts meldet es (D-414)")
    else:
        try:
            einst = json.loads(read(einst_pfad))
        except json.JSONDecodeError:
            einst = None
        if not isinstance(einst, dict):
            err(f"{einst_rel}: kein JSON-Objekt. Der Client läse daraus weder Agent noch "
                f"Engine (D-414)")
        else:
            for schluessel, wert in soll.items():
                if einst.get(schluessel) != wert:
                    err(f"{einst_rel}: '{schluessel}' ist {einst.get(schluessel)!r}, das "
                        f"Pack verlangt {wert!r}. Mit einem anderen Wert wählt der Client "
                        f"einen anderen Agenten oder eine Engine, die das Profilfeld "
                        f"permissions nicht kennt – und fällt dabei still zurück (D-414)")
    # (b) Das Profil.
    if not os.path.isfile(profil_pfad):
        err(f"{profil_rel}: fehlt. Die Einstellung wählt ein Profil, das es nicht gibt – "
            f"der Client fällt STILL auf seinen eingebauten Agenten zurück, gemessen: "
            f".env war danach lesbar (D-414)")
        return
    try:
        cfg = json.loads(read(profil_pfad))
    except json.JSONDecodeError as exc:
        err(f"{profil_rel}: kein gültiges JSON ({exc.msg}, Zeile {exc.lineno}). Der Client "
            f"fällt dann STILL auf seinen eingebauten Agenten zurück – sein eigenes "
            f"Prüfkommando 'agent validate' endet dabei mit Exit 0 (D-414)")
        return
    name = man.get("permission_profile_name")
    if not isinstance(cfg, dict) or cfg.get("name") != name:
        err(f"{profil_rel}: das Profil heißt {cfg.get('name') if isinstance(cfg, dict) else '?'!r}, "
            f"die Einstellung wählt {name!r}. Ein Name, den kein Profil trägt, ist der "
            f"stille Rückfall aus D-414")
        return
    # (c) Jede Regel ist eine, die der Client ausführt.
    regeln = _p96_regeln(cfg)
    if not regeln:
        err(f"{profil_rel}: keine einzige Regel unter permissions.rules – das Profil wäre "
            f"aktiv und sperrte nichts (D-414)")
        return
    ist: dict = {e: {} for e in P96_EFFEKTE}
    for nr, regel in enumerate(regeln, 1):
        if not isinstance(regel, dict):
            err(f"{profil_rel}: Regel {nr} ist kein Objekt (D-414)")
            continue
        faehigkeit, effekt = regel.get("capability"), regel.get("effect")
        muster = regel.get("match")
        if faehigkeit not in clientmap.KIRO_FAEHIGKEITEN:
            err(f"{profil_rel}: Regel {nr} nennt die Fähigkeit {faehigkeit!r}, die der "
                f"Client nicht kennt. Er überspringt die Regel und meldet es nur in seinem "
                f"Protokoll – gemessen (D-414)")
            continue
        if effekt not in P96_EFFEKTE:
            err(f"{profil_rel}: Regel {nr} hat den Effekt {effekt!r}; bekannt sind "
                f"{', '.join(P96_EFFEKTE)} (D-414)")
            continue
        if not isinstance(muster, list) or not all(isinstance(m, str) for m in muster):
            err(f"{profil_rel}: Regel {nr} führt 'match' nicht als Liste von Mustern (D-414)")
            continue
        ausnahme = tuple(regel.get("exclude") or ())
        for m in muster:
            ist[effekt].setdefault((faehigkeit, m), set()).add(ausnahme)
    # (d) Gegen die Kernquelle.
    try:
        quelle = json.loads(clientmap.load_source(kern, "permissions.json"))
        erzeugt = clientmap.kiro_regeln(quelle, man)
    except (OSError, ValueError) as exc:
        err(f"Kernquelle der Berechtigungen nicht auswertbar: {exc}")
        return
    soll_regeln: dict = {e: {} for e in P96_EFFEKTE}
    for regel in erzeugt:
        for m in regel["match"]:
            soll_regeln[regel["effect"]].setdefault((regel["capability"], m), set()).add(
                tuple(regel.get("exclude") or ()))
    for effekt in ("deny", "ask"):
        for (faehigkeit, m), ausnahmen in soll_regeln[effekt].items():
            if m.startswith("<"):
                continue  # Projektschlitz - gehört dem Overlay
            vorhanden = ist[effekt].get((faehigkeit, m))
            if not vorhanden:
                err(f"{profil_rel}: die Kernquelle erzeugt '{effekt} {faehigkeit} {m}'; im "
                    f"Profil steht es nicht. Eine fehlende Regel ist eine Lockerung (D-77, "
                    f"D-414)")
            elif not ausnahmen <= vorhanden:
                err(f"{profil_rel}: '{effekt} {faehigkeit} {m}' steht im Profil mit einer "
                    f"anderen Ausnahme als in der Abbildung {sorted(ausnahmen)} – eine "
                    f"breitere Ausnahme ist eine Lockerung (D-415)")
    skills = {f"skill {n}" for n in installierte_skills(root, man)}
    for (faehigkeit, m) in ist["allow"]:
        if (faehigkeit, m) in soll_regeln["allow"] or m.startswith("<"):
            continue
        if faehigkeit == "skill" and f"skill {m}" in skills:
            continue  # aktivierter Pack-Skill, Bauform von Prüfung 72 (D-238)
        err(f"{profil_rel}: 'allow {faehigkeit} {m}' erzeugt die Kernquelle nicht. Eine "
            f"zusätzliche Freigabe ist eine Ausweitung und nicht Sache des Profils (D-77)")


# ---------------------------------------------------------------------------
# PRUEFUNGEN 91 BIS 94: DIE DOKUMENTATION (CR-2026-142, D-371 bis D-375)

# ---------------------------------------------------------------------------
# PRUEFUNG 97: DIE BERECHTIGUNGSDATEI, MIT DER DER CLIENT STARTET UND DIE TRIFFT
# ---------------------------------------------------------------------------
# ANLASS, UND ER IST GEMESSEN (CR-2026-155, D-440). Am 2026-09-26 an cursor-agent
# 2026.09.26 unter Windows:
#   * Mit den Schluesseln _comment und _core_rules_integrity in .cursor/cli.json brach
#     der Client mit Exit 1 ab ("Unrecognized key(s) in object") - ebenso bei kaputtem
#     JSON. Die Kernregeln koennen deshalb nicht in der Datei selbst stehen wie bei der
#     ersten Ausgabeform; diese Pruefung haelt sie gegen die Kernquelle.
#   * Ein Pfadmuster vergleicht der Client verankert mit dem ABSOLUTEN Pfad. 'Read(.env)'
#     und 'Read(**/.env)' liessen den Koeder durch, 'Read(*\.env)' nicht. Ein Verbot,
#     das so nie trifft, sieht aus wie eines.
#   * Die Pruefungen der Koerbe (37 und Verwandte) erreichen diese Form nicht (D-416).
# GEPRUEFT: (a) gueltiges JSON, ein Objekt mit genau dem Schluessel permissions, darin nur
# allow und deny als Listen von Zeichenketten; (b) jeder Eintrag hat die Gestalt
# Typ(Argument) mit einem Regeltyp des Clients; (c) jedes deny der Kernquelle steht darin,
# eine Kernzusage mit eigenem Wortlaut; kein allow, das die Kernquelle nicht erzeugt;
# (d) Warnung fuer ein Pfadverbot ohne fuehrendes '*' und ohne absoluten Pfad.
# GRENZE, BENANNT: Gemessen ist Windows. Die Schreibweise mit '/' fuer POSIX folgt aus dem
# Programmcode des Clients, nicht aus einer Messung auf macOS oder Linux.
P97_TYPEN = ("Shell", "Bash", "Read", "Write", "WebFetch", "Mcp")
P97_EINTRAG_RE = re.compile(r"^\s*([A-Za-z]+)\s*\((.*)\)\s*$")


def check_cursor_berechtigungen(root: str, man: dict) -> None:
    """Pruefung 97 (D-440): Die Datei laesst den Client starten, und ihre Verbote treffen."""
    if man.get("permissions_format") != "cursor-json":
        return
    rel = man.get("permissions_file") or ""
    pfad = os.path.join(root, *rel.split("/"))
    if not os.path.isfile(pfad):
        return  # keine Installation dieses Packs an dieser Wurzel; Pflichtpfade melden es
    kern = os.path.join(root, KERN)
    if kern not in sys.path:
        sys.path.insert(0, kern)
    try:
        import clientmap
    except ImportError:
        return  # check_config meldet das fehlende Abbildungsmodul bereits
    if not hasattr(clientmap, "cursor_koerbe") or not hasattr(clientmap, "cursor_kernregeln"):
        err(f"{KERN}/clientmap.py: 'cursor_koerbe' oder 'cursor_kernregeln' fehlt – Prüfung "
            f"97 hat ihren Gegenstand verloren und bestünde sonst leise (D-23)")
        return
    # (a) Die Gestalt, mit der der Client startet.
    try:
        cfg = json.loads(read(pfad))
    except json.JSONDecodeError as exc:
        err(f"{rel}: kein gültiges JSON ({exc.msg}, Zeile {exc.lineno}). Der Client startet "
            f"damit nicht – gemessen: Exit 1 (D-440)")
        return
    if not isinstance(cfg, dict) or set(cfg) != {"permissions"}:
        fremd = sorted(set(cfg) - {"permissions"}) if isinstance(cfg, dict) else ["?"]
        err(f"{rel}: die Datei trägt {', '.join(fremd) or 'keinen Schlüssel permissions'}. "
            f"Der Client nimmt auf Projektebene nur 'permissions' an und startet mit einem "
            f"weiteren Schlüssel nicht – gemessen mit _comment und _core_rules_integrity: "
            f"Exit 1, 'Unrecognized key(s)' (D-440)")
        return
    rechte = cfg["permissions"]
    if not isinstance(rechte, dict) or not set(rechte) <= {"allow", "deny"}:
        err(f"{rel}: 'permissions' darf nur allow und deny führen – dieser Client kennt "
            f"keinen Rückfragekorb (D-440)")
        return
    ist: dict = {}
    for korb in ("allow", "deny"):
        liste = rechte.get(korb, [])
        if not isinstance(liste, list) or not all(isinstance(e, str) for e in liste):
            err(f"{rel}: permissions.{korb} ist keine Liste von Zeichenketten (D-440)")
            return
        ist[korb] = set(liste)
        # (b) Jeder Eintrag ist eine Regel, die der Client kennt.
        for eintrag in liste:
            m = P97_EINTRAG_RE.match(eintrag)
            if not m or m.group(1) not in P97_TYPEN:
                err(f"{rel}: '{eintrag}' in permissions.{korb} ist keine Regel der Gestalt "
                    f"Typ(Argument) mit einem Typ dieses Clients ({', '.join(P97_TYPEN)}). "
                    f"Eine solche Zeile wertet der Client nicht aus (D-440)")
                continue
            # (d) Ein Pfadverbot, das nie trifft.
            argument = m.group(2).strip()
            if korb == "deny" and m.group(1) in ("Read", "Write") \
                    and not argument.startswith(("*", "<", "/", "~")) \
                    and not re.match(r"^[A-Za-z]:[\\/]", argument):
                warn(f"{rel}: '{eintrag}' trifft bei diesem Client nie. Er vergleicht das "
                     f"Muster mit dem ABSOLUTEN Pfad – gemessen: 'Read(.env)' und "
                     f"'Read(**/.env)' ließen den Köder durch. Die Schreibweise mit "
                     f"führendem '*' in beiden Trennern: 'Read(*/<pfad>)' und "
                     f"'Read(*\\<pfad>)' (D-440)")
    # (c) Gegen die Kernquelle.
    try:
        quelle = json.loads(clientmap.load_source(kern, "permissions.json"))
        soll = clientmap.cursor_koerbe(quelle, man)
        kernregeln = set(clientmap.cursor_kernregeln(quelle, man))
    except (OSError, ValueError) as exc:
        err(f"Kernquelle der Berechtigungen nicht auswertbar: {exc}")
        return
    for eintrag in soll["deny"]:
        if "<" in eintrag or eintrag in ist["deny"]:
            continue  # Projektschlitz gehört dem Overlay
        if eintrag in kernregeln:
            err(f"{rel}: die Kernzusage '{eintrag}' fehlt in permissions.deny. Kernregeln "
                f"darf das Projekt nicht entfernen; diese Datei kann sie nicht selbst "
                f"auflisten, deshalb hält diese Prüfung sie gegen die Kernquelle (D-440)")
        else:
            err(f"{rel}: '{eintrag}' aus der Kernquelle fehlt in permissions.deny. Eine "
                f"Regel des Kerns zu streichen ist eine Lockerung (D-77, D-440)")
    for eintrag in sorted(ist["allow"] - set(soll["allow"])):
        err(f"{rel}: '{eintrag}' in permissions.allow erzeugt die Kernquelle nicht. Eine "
            f"zusätzliche Freigabe ist eine Ausweitung; ein freigegebener Befehl gehört in "
            f"Abschnitt 6 des Overlays und damit in die Regelschicht (D-77, D-440)")
    # (e) Die Ausschlussdatei (D-443): die zweite Lesesperre, und die einzige, die das
    # Suchwerkzeug beachtet - gemessen am 2026-09-26.
    ign_rel = man.get("ignore_file")
    if not ign_rel or not hasattr(clientmap, "cursor_ignore_muster"):
        return
    ign_pfad = os.path.join(root, *ign_rel.split("/"))
    if not os.path.isfile(ign_pfad):
        err(f"{ign_rel}: fehlt. Ohne sie wertet das Suchwerkzeug dieses Clients kein "
            f"Leseverbot aus – gemessen: der Köder aus secrets/ kam heraus (D-443)")
        return
    zeilen = {z.strip() for z in read(ign_pfad).splitlines()}
    for muster in clientmap.cursor_ignore_muster(quelle, man):
        if muster not in zeilen:
            err(f"{ign_rel}: das Leseverbot '{muster}' der Kernquelle fehlt. Das "
                f"Suchwerkzeug fände dort wieder, was die Berechtigungsdatei nur dem "
                f"Lesewerkzeug verbietet (D-443)")
P99_ANKER = ("MANDAT_DATEI = ", "MANDATS_MUSTER = ", "def mandat_lesen(")
P99_WERTE_RE = (re.compile(r'^MANDAT_DATEI = "([^"]+)"', re.M),
                re.compile(r"^MANDAT_HOECHSTDAUER_MIN = (\d+)", re.M),
                re.compile(r"^MANDAT_UMFAENGE = \{(.*?)\n\}", re.M | re.S),
                # Die Modusbindung liegt neben dem Mandat (D-501, K-179)
                re.compile(r'^MODUS_DATEI = "([^"]+)"', re.M),
                re.compile(r"^MODUS_GEBUNDEN = (\(.*?\))", re.M))


def _p99_werte(text: str) -> tuple:
    return tuple((r.search(text).group(1).strip() if r.search(text) else None)
                 for r in P99_WERTE_RE)


# Seit 1.23.0 (CR-2026-169, K-201): M3 bis M5 binden Globs aus dem Overlay. mandat.py
# zeigt sie an, der Hook wertet sie aus - mit je einer Funktion 'glob_muster'. Zwei
# Lesarten desselben Globs hiessen: Der Mensch sieht eine Grenze, der Hook zieht eine
# andere. Verglichen wird der Rumpf ohne Docstring, als Syntaxbaum.
def _p99_glob_rumpf(text: str):
    try:
        baum = ast.parse(text)
    except SyntaxError:
        return None
    for knoten in baum.body:
        if isinstance(knoten, ast.FunctionDef) and knoten.name == "glob_muster":
            rumpf = list(knoten.body)
            if (rumpf and isinstance(rumpf[0], ast.Expr)
                    and isinstance(getattr(rumpf[0], "value", None), ast.Constant)
                    and isinstance(rumpf[0].value.value, str)):
                rumpf = rumpf[1:]
            return "".join(ast.dump(k) for k in rumpf)
    return None


def check_mandatsschutz(root: str, man: dict) -> None:
    """Pruefung 99 (D-447, D-448): Das Mandat erteilt nur der Mensch, und es wirkt."""
    skript = os.path.join(root, KERN, "tests", "scripts", "hook-check-secrets.py")
    mandat = os.path.join(root, KERN, "mandat.py")
    if not os.path.isfile(skript):
        return
    hook = read(skript)
    fehlend = [a for a in P99_ANKER if a not in hook]
    if fehlend:
        err(f"{KERN}/tests/scripts/hook-check-secrets.py: {', '.join(fehlend)} fehlt. Pruefung "
            f"99 misst den Schutz des Mandats; ohne ihn bestuende sie leise (D-23, D-447)")
        return
    if not os.path.isfile(mandat):
        err(f"{KERN}/mandat.py fehlt. Der Hook kennt ein Mandat, das niemand erteilen kann - "
            f"Modus M6 waere eine Zusage ohne Werkzeug (D-447)")
        return
    if _p99_werte(hook) != _p99_werte(read(mandat)):
        err(f"{KERN}/mandat.py und hook-check-secrets.py fuehren verschiedene Werte fuer "
            f"Dateiname, Hoechstdauer oder Umfaenge des Mandats: Hook {_p99_werte(hook)}, "
            f"mandat.py {_p99_werte(read(mandat))}. Ein Mandat, das das Werkzeug schreibt und "
            f"der Hook nicht liest, gibt nichts frei (D-447)")
    glob_hook, glob_mandat = _p99_glob_rumpf(hook), _p99_glob_rumpf(read(mandat))
    if glob_hook is None or glob_hook != glob_mandat:
        err(f"{KERN}/mandat.py und hook-check-secrets.py werten die Globs der Modusbindung "
            f"nicht gleich aus: Die Funktion glob_muster fehlt in einer der beiden Dateien "
            f"oder ihr Rumpf weicht ab. Der Mensch saehe beim Binden eine andere Grenze, als "
            f"der Hook zieht (K-201)")
    quelle = os.path.join(root, KERN, "framework", "runtime", "permissions.json")
    if os.path.isfile(quelle):
        try:
            regeln = json.loads(read(quelle)).get("deny", [])
        except (json.JSONDecodeError, AttributeError):
            regeln = []
        if any(isinstance(r, dict) and r.get("tool") == "write"
               and "project-overlay" in str(r.get("pattern", "")) for r in regeln):
            err(f"{KERN}/framework/runtime/permissions.json: sperrt das Overlay im deny-Korb. "
                f"Eine statische Sperre hebt kein Mandat auf; das Overlay sperrt der "
                f"Schutz-Hook (D-448)")
    interpreter = _hook_interpreter()
    if interpreter is None:
        return
    faelle = [
        ("Aufruf von mandat.py erteilen",
         {"tool_name": "exec", "tool_input": {"command":
          f"python {KERN}/mandat.py erteilen --rolle P99 --umfang overlay --minuten 5"}}, 2),
        ("Schreiben der Mandatsdatei",
         {"tool_name": "write", "tool_input": {"file_path": ".git/koolie-mandat.json",
                                               "content": "{}"}}, 2),
        ("die Auskunft mandat.py status",
         {"tool_name": "exec", "tool_input": {"command": f"python {KERN}/mandat.py status"}}, 0),
        # claude-code schickt eine Beschreibung mit - sie darf die Auskunft nicht sperren
        # (gemessen am 2026-09-27, Lauf sk013n01)
        ("die Auskunft mit einer Beschreibung daneben",
         {"tool_name": "exec", "tool_input": {"command": f"python {KERN}/mandat.py status",
                                              "description": "Mandatsstatus abfragen"}}, 0),
        ("die Auskunft mit einem zweiten Befehl dahinter",
         {"tool_name": "exec", "tool_input": {"command":
          f"python {KERN}/mandat.py status; python {KERN}/mandat.py erteilen --rolle P99"}}, 2),
        # Die Modusbindung setzt wie das Mandat nur der Mensch (D-501, K-179)
        ("Aufruf von mandat.py modus",
         {"tool_name": "exec", "tool_input": {"command": f"python {KERN}/mandat.py modus aus"}},
         2),
        ("Schreiben der Modusdatei",
         {"tool_name": "write", "tool_input": {"file_path": ".git/koolie-modus.json",
                                               "content": "{}"}}, 2),
    ]
    # Das Overlay ohne Mandat - nur, wenn im gepruefen Baum gerade keines erteilt ist: Ein
    # erteiltes Mandat ist ein gueltiger Zustand, kein Befund.
    if not os.path.exists(os.path.join(root, ".git", "koolie-mandat.json")):
        faelle.append(("Schreiben in das Overlay ohne Mandat",
                       {"tool_name": "write", "tool_input": {
                           "file_path": ".koolie/project-overlay/OVERLAY.md", "content": "x"}}, 2))
    for was, ereignis, erwartet in faelle:
        ergebnis = _hook_lauf(interpreter, skript, json.dumps(ereignis))
        if ergebnis != erwartet:
            err(f"{KERN}/tests/scripts/hook-check-secrets.py: {was} endet mit Exit {ergebnis}, "
                f"erwartet {erwartet}. Das Mandat erteilt nur der Mensch im eigenen Terminal; "
                f"der Client darf es weder anlegen noch aufrufen, nur nachsehen (D-447)")


def check_modellaufruf_nur_lesend(root: str, man: dict) -> None:
    """Pruefung 100 (D-451, CR-2026-175 E4): Ein Skill mit Trigger 'model' schreibt nicht
    und gibt keinen Befehl vorab frei.

    Bis 2.1.0 sperrte er auch exec. Seit 2.2.0 darf er die lesenden Git-Befehle nutzen -
    aber nur nach den Regeln der Sitzung: exec steht weder in allowed-tools noch in
    permissions.allow. Bei claude-code ist allowed-tools eine Vorabfreigabe, die keine
    Befehle unterscheidet; ein Skill, den das Modell selbst aufruft, oeffnete sonst jede
    Shell ohne Rueckfrage.
    """
    if yaml is None:
        return  # ohne PyYAML kein Frontmatter - die Warnung dazu gibt main()
    for skills_dir, prefix in skill_dirs(root, man):
        if not prefix.startswith(KERN + "/"):
            continue  # die installierte Fassung traegt das Feld nicht in jedem Pack
        for name in sorted(os.listdir(skills_dir)):
            pfad = os.path.join(skills_dir, name, "SKILL.md")
            if not os.path.isfile(pfad):
                continue
            fm, _ = parse_frontmatter(read(pfad))
            if not isinstance(fm, dict) or "model" not in (fm.get("triggers") or []):
                continue
            rechte = fm.get("permissions") or {}
            deny = [str(d).strip().lower() for d in (rechte.get("deny") or [])]
            if "edit" not in deny:
                err(f"{prefix}/{name}/SKILL.md: traegt den Trigger 'model', sperrt aber "
                    f"edit nicht in permissions.deny. Den Modellaufruf erlaubt "
                    f"08-skill-conventions.md nur einem Skill, der nicht schreibt (D-451)")
            werkzeuge = [str(w).strip().lower() for w in (fm.get("allowed-tools") or [])]
            vorab = [str(a).strip() for a in (rechte.get("allow") or [])
                     if str(a).strip().lower() == "exec"
                     or str(a).strip().lower().startswith("exec(")]
            if "exec" in werkzeuge or vorab:
                err(f"{prefix}/{name}/SKILL.md: traegt den Trigger 'model' und gibt Befehle "
                    f"vorab frei ({', '.join((['exec in allowed-tools'] if 'exec' in werkzeuge else []) + vorab)}). "
                    f"Ein Skill, den das Modell selbst aufruft, nutzt die Shell nur nach den "
                    f"Regeln der Sitzung (08-skill-conventions.md, D-451)")


# --- Pruefung 101: die MCP-Freigaben (CR-2026-157, D-459) ------------------------------
P101_ABSCHNITT = "### 13.2 MCP-Server"
P101_NAME_RE = re.compile(r"`([A-Za-z0-9_.-]+)`")
P101_KERNQUELLE = "framework/runtime/permissions.json"


def _p101_freigaben(text: str) -> list:
    """Die Zeilen der Tabelle in Overlay Abschnitt 13.2 - Server, Zweck, Werkzeuge."""
    if P101_ABSCHNITT not in text:
        return []
    teil = text.replace("\r\n", "\n").split(P101_ABSCHNITT, 1)[1]
    teil = re.split(r"\n#{1,3} ", teil, maxsplit=1)[0]
    zeilen = []
    for z in teil.split("\n"):
        if not z.strip().startswith("|"):
            continue
        zellen = tabellenzellen(z)
        if len(zellen) < 5 or zellen[0].startswith("Server") or not zellen[0].strip("-: "):
            continue
        server = zellen[0].strip().strip("`").strip()
        if not server or TBD_RE.search(zellen[0]) or server in ("–", "-", "keine"):
            continue
        zeilen.append({"server": server, "zweck": zellen[2].lower(),
                       "lesen": P101_NAME_RE.findall(zellen[3]),
                       "schreiben": P101_NAME_RE.findall(zellen[4])})
    return zeilen


def check_mcp_freigaben(root: str, man: dict, strikt: bool) -> None:
    """Pruefung 101 (D-459): MCP-Werkzeuge stehen einzeln und nur lesend in allow."""
    kq = os.path.join(root, KERN, *P101_KERNQUELLE.split("/"))
    if os.path.isfile(kq):
        try:
            quelle = json.loads(read(kq))
        except json.JSONDecodeError:
            quelle = {}
        for regel in quelle.get("allow") or []:
            if isinstance(regel, dict) and regel.get("tool") == "mcp":
                err(f"{KERN}/{P101_KERNQUELLE}: gibt ein MCP-Werkzeug im allow-Korb frei "
                    f"({json.dumps(regel, ensure_ascii=False)}). Eine MCP-Freigabe gehört dem "
                    f"Projekt: Sie nennt Server, Zweck und Werkzeuge im Overlay Abschnitt 13.2, "
                    f"und der Kern gibt nichts vorab frei (02-privacy.md 3.8, D-459)")

    regelform = (man or {}).get("mcp_permission_rule")
    overlay = os.path.join(root, ".koolie", "project-overlay", "OVERLAY.md")
    rel = (man or {}).get("permissions_file")
    if not isinstance(regelform, dict) or not rel or not os.path.isfile(overlay):
        return
    pfad = os.path.join(root, *rel.split("/"))
    if not os.path.isfile(pfad):
        return
    try:
        cfg = json.loads(read(pfad))
    except json.JSONDecodeError:
        return  # Pruefung 3 meldet das bereits
    rechte = cfg.get("permissions") if isinstance(cfg, dict) else None
    if not isinstance(rechte, dict):
        return
    allow = [r for r in rechte.get("allow") or [] if isinstance(r, str)]
    ask = [r for r in rechte.get("ask") or [] if isinstance(r, str)]
    form = str(regelform.get("werkzeug", ""))
    praefix = form.split("{server}", 1)[0]
    if not praefix:
        return
    freigaben = _p101_freigaben(read(overlay))
    lesen = {form.format(server=f["server"], werkzeug=w)
             for f in freigaben if "lesen" in f["zweck"] for w in f["lesen"]}
    schreiben = {form.format(server=f["server"], werkzeug=w)
                 for f in freigaben for w in f["schreiben"]}
    # Der Serveranteil der Regelform ('mcp__atlassian', 'Mcp(atlassian') - eine Regel, die nur
    # ihn nennt, gilt fuer jedes Werkzeug des Servers.
    serverteil = form.split("{werkzeug}", 1)[0]
    ganze_server = {serverteil.format(server=f["server"]).rstrip("_:(") for f in freigaben}
    for regel in allow:
        if not regel.startswith(praefix) or regel in lesen:
            continue
        if regel in schreiben:
            grund = "ein Schreibwerkzeug – es verlangt bei jedem Aufruf die Bestätigung des Menschen"
        elif "*" in regel or regel.rstrip("_:()") in ganze_server:
            grund = "ein Muster für mehrere Werkzeuge – es gäbe auch die Schreibwerkzeuge frei"
        else:
            grund = "ein Werkzeug, das Overlay Abschnitt 13.2 keinem Server zum Lesen zuweist"
        err(f"{rel}: „{regel}“ steht in allow – {grund}. In allow stehen nur die "
            f"Lesewerkzeuge der Freigabe, einzeln; Schreibwerkzeuge gehören einzeln in ask "
            f"(02-privacy.md 3.8, D-459)")
    if not strikt:
        return
    for regel in sorted(lesen - set(allow)):
        err(f"{rel}: das freigegebene Lesewerkzeug „{regel}“ fehlt in allow. Overlay "
            f"Abschnitt 13.2 gibt es zum Lesen frei; ohne die Regel fragt der Client bei "
            f"jedem Aufruf nach, und ein nicht-interaktiver Lauf wird abgewiesen (D-459)")
    pauschal = regelform.get("pauschal")
    if lesen and pauschal in ask and regelform.get("rueckfrage_schlaegt_freigabe"):
        err(f"{rel}: „{pauschal}“ steht im ask-Korb, während Overlay Abschnitt 13.2 Werkzeuge "
            f"zum Lesen freigibt. Bei diesem Client schlägt die Rückfrage die Freigabe – "
            f"auch das einzeln freigegebene Lesewerkzeug wird abgewiesen (gemessen, D-459). "
            f"Die Pauschale durch die Einzelregeln ersetzen: Lesewerkzeuge in allow, "
            f"Schreibwerkzeuge in ask")
