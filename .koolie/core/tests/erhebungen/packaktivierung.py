# -*- coding: utf-8 -*-
"""Aktiviert ein Pack im Messbaum - und nimmt es fuer den Kontrollzuschnitt heraus.

🔴 DER ANLASS IST GEMESSEN (2026-09-21, D-237). `role-re-ticket` ist der einzige
Skill dieses Frameworks ausserhalb des Kerns. Im Uebungsrepositorium IST das Pack
aktiviert, `git archive HEAD` bringt es mit - und dann:

    Packwechsel (rm -rf .devin)          das Pack ist weg
    install.py --client claude-code      legt ZWOELF Skills an, die des Kerns
    cc-overlay-fuellen.py                beruehrt Skills nicht

Alle fuenfzehn Zellen von Buendel 5 waeren gegen einen Baum gelaufen, in dem ihr
Gegenstand nicht existiert - gerechnet rund 30 Laeufe und 30 bis 37 USD. 🔴 Und
der Waechter haette geschwiegen, weil er die drei Skills von Buendel 4 BEIM NAMEN
fuehrte und alle drei auch hier lagen.

    Vier Buendel lang war "installiert" dasselbe wie "vorhanden". Beim fuenften
    nicht mehr - und der Waechter prueft die Namen des vierten.

🟢 DAS FRAMEWORK IST NICHT IM UNRECHT. `framework/role-packs/README.md` sagt
ausdruecklich, dass `install.py` die Aktivierung "bewusst nicht vorwegnimmt": Sie
ist eine Projektentscheidung. Dieses Modul tut deshalb GENAU DAS, WAS EIN
UEBERNEHMENDES PROJEKT TUT - die drei Schritte aus `ROLE_PACK.md` Abschnitt 9,
nicht ein Schalter an `install.py`, der eine Frage entschiede, die die README dem
Projekt zuweist.

DIE AKTIVIERUNG HAT DREI TEILE, NICHT ZWEI (D-238, Pruefung 72):

    1. Laufzeitfassung  <pack>/runtime/30-*.md  ->  <RULES_DIR>/
    2. Skillablage      <pack>/skills/<skill>/  ->  <SKILLS_DIR>/
    3. Korbeintrag      Skill(<skill>)          ->  Berechtigungsdatei

Der dritte fiel beim Beheben des ersten an: Nach der Aktivierung wortgetreu nach
der README trug der Baum 13 Skills gegen 12 Korbeintraege, bei 0 Fehlern des
Validators.

DIE UMKEHRUNG IST DER KONTROLLZUSCHNITT `ohnepack` (K-87, D-242). Sie nimmt
dieselben drei Teile wieder heraus - und zusaetzlich das kanonische
Packverzeichnis unter `framework/`, weil der Messbaum das Framework traegt und
ein Lauf die kanonische Fassung dort findet (D-234).
"""
import importlib.util
import io
import json
import os
import shutil


ARTEN = ("role-packs", "tech-packs")


def _lies(pfad):
    return io.open(pfad, encoding="utf-8", newline="").read()


def _schreib(pfad, text):
    """Erst kodieren, dann oeffnen - und zwar in eine Variable.

    `io.open(..., "wb").write(text.encode(...))` schneidet die Zieldatei beim
    Oeffnen auf null Bytes; scheitert danach das Kodieren, ist die Datei weg.
    """
    daten = text.encode("utf-8")
    io.open(pfad, "wb").write(daten)


def _weg(pfad):
    def onexc(func, p, exc):
        os.chmod(p, 0o700)
        func(p)
    if os.path.exists(pfad):
        if os.path.islink(pfad) or os.path.isjunction(pfad):
            os.rmdir(pfad)
        elif os.path.isdir(pfad):
            shutil.rmtree(pfad, onexc=onexc)
        else:
            os.remove(pfad)


def skillorte(baum):
    """Jede Ablage, in der eine Skillfassung liegen kann - ABGELEITET (D-239).

    Neben der Skill- und der Agentenablage der Laufzeitschicht und `framework/skills/`
    kommt jede `skills/`-Ablage unter `framework/role-packs/` und
    `framework/tech-packs/` hinzu, ermittelt beim Bau des Zuschnitts.

    🔴 BIS 0.79.4 WAREN ES DREI GENANNTE ORTE, UND DAS WAR ZWEIMAL ZU WENIG. D-234
    hat den Zuschnitt vom Kommando auf den Skill umgestellt - der Messbaum traegt das
    Framework, und dort steht die kanonische Fassung. D-239 hat drei Tage spaeter
    gemessen, dass dieselbe Stelle noch immer zu eng war: Wortgleich auf den Baum von
    Buendel 5 angewandt blieb GENAU EINE `SKILL.md` stehen, und es war die des
    gemessenen Skills. Ein gepflegter Ort ist eine gepflegte Zahl (D-153).
    """
    orte = [os.path.join(".claude", "skills"),
            os.path.join(".claude", "agents"),
            os.path.join(".koolie/core", "framework", "skills")]
    for art in ARTEN:
        basis = os.path.join(baum, ".koolie/core", "framework", art)
        if not os.path.isdir(basis):
            continue
        for pack in sorted(os.listdir(basis)):
            if os.path.isdir(os.path.join(basis, pack, "skills")):
                orte.append(os.path.join(".koolie/core", "framework", art, pack,
                                         "skills"))
    return orte


def skillschnitt(baum):
    """Der Zuschnitt `ohneskill`: keine Skillfassung mehr im Baum, an keiner Stelle.

    Die Regelschicht bleibt stehen - das ist die Trennlinie des Zuschnitts und wird
    hier gegen drei Pflichttraeger geprueft. Gibt die Zahl der geleerten Ablagen
    zurueck.
    """
    orte = skillorte(baum)
    for unter in orte:
        ablage = os.path.join(baum, unter)
        if not os.path.isdir(ablage):
            raise SystemExit("ABBRUCH: %s fehlt im Zuschnitt ohneskill - der "
                             "Gegenstand ist nicht da, wo er sein muesste (D-234)"
                             % unter)
        for name in sorted(os.listdir(ablage)):
            _weg(os.path.join(ablage, name))
        if os.listdir(ablage):
            raise SystemExit("ABBRUCH: %s ist nicht leer" % unter)
    # Der Stammwaechter: ein Praefixvergleich auf `.claude/` haette `.koolie/core/`
    # nie gesehen - deshalb sucht er ueber den ganzen Baum.
    rest = []
    for basis, ordner, dateien in os.walk(baum):
        ordner[:] = [o for o in ordner if o != ".git"]
        for d in dateien:
            if d == "SKILL.md":
                rest.append(os.path.relpath(os.path.join(basis, d), baum))
    if rest:
        raise SystemExit("ABBRUCH: %d Skillfassung(en) stehen noch im Zuschnitt "
                         "ohneskill: %s (D-234)"
                         % (len(rest), ", ".join(sorted(rest)[:5])))
    for pflicht in ("CLAUDE.md",
                    os.path.join(".claude", "rules", "00-framework-core.md"),
                    os.path.join(".koolie/core", "checklists",
                                 "04-review-ai-code.md")):
        if not os.path.isfile(os.path.join(baum, pflicht)):
            raise SystemExit("ABBRUCH: %s fehlt - die Regelschicht ist mitgefallen"
                             % pflicht)
    return len(orte)


def _installer(baum):
    """Das `install.py` DIESES Baums - fuer `render_rule` und `resolve_placeholders`.

    🔴 EINE LAUFZEITFASSUNG WIRD GERENDERT, NICHT KOPIERT (gemessen 2026-09-21).
    `framework/role-packs/README.md` schrieb zur Aktivierung ein `cp` vor. Fuer
    `devin-desktop` ist das richtig - Quellform ist dort Zielform. Fuer
    `claude-code` nicht: Er wertet fuer Regeldateien nur `paths` aus (K-18), und
    das Quellfrontmatter traegt `description` und `trigger`. Gemessen am Messbaum
    von Buendel 5 meldete der Validator danach ZWEI Fehler an genau dieser Datei.

    `install.py` kann es laengst - `ist_regelquelle()` fuehrt die Laufzeitfassungen
    aktivierter Packs seit 0.14.0 ausdruecklich auf, und `--update` bringt sie in
    Form. Nur der Weg dorthin fuehrte ueber einen zweiten Befehl, den die Anleitung
    nicht nannte.

      Ein Werkzeug, das eine Abbildung kann, und eine Anleitung, die kopieren sagt:
      Die Anleitung gewinnt, weil sie gelesen wird.
    """
    pfad = os.path.join(baum, ".koolie/core", "install.py")
    if not os.path.isfile(pfad):
        raise SystemExit("ABBRUCH: %s fehlt - ohne ihn ist die Abbildung der "
                         "Laufzeitfassung nicht zu haben" % pfad)
    spec = importlib.util.spec_from_file_location("lw_install_baum", pfad)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    for name in ("render_rule", "resolve_placeholders"):
        if not hasattr(modul, name):
            raise SystemExit("ABBRUCH: %s fuehrt %s nicht - die Abbildung haette "
                             "ihren Gegenstand verloren" % (pfad, name))
    return modul


def manifest(baum, client):
    """Das Manifest des Client Packs - aus dem Kern DIESES Baums."""
    pfad = os.path.join(baum, ".koolie/core", "clients", client, "manifest.json")
    if not os.path.isfile(pfad):
        raise SystemExit("ABBRUCH: %s fehlt - ohne Manifest ist keine Ablage "
                         "ableitbar" % pfad)
    return json.loads(_lies(pfad))


def _ablagen(baum, man):
    """(Regelablage, Skillablage, Berechtigungsdatei) - abgeleitet, nicht gepflegt."""
    platz = man.get("runtime_placeholders") or {}
    regeln = man.get("pack_runtime_dir") or platz.get("<RULES_DIR>")
    skills = man.get("skills_dir")
    rechte = man.get("permissions_file")
    for name, wert in (("pack_runtime_dir/<RULES_DIR>", regeln),
                       ("skills_dir", skills), ("permissions_file", rechte)):
        if not wert:
            raise SystemExit("ABBRUCH: das Manifest von %r fuehrt %s nicht - die "
                             "Aktivierung haette keinen Ort" % (man.get("client"), name))
    return (os.path.join(baum, *regeln.split("/")),
            os.path.join(baum, *skills.split("/")),
            os.path.join(baum, *rechte.split("/")))


def packverzeichnis(baum, pack):
    """(Art, absoluter Pfad) des Packs im Kern dieses Baums - gesucht, nicht genannt."""
    for art in ARTEN:
        p = os.path.join(baum, ".koolie/core", "framework", art, pack)
        if os.path.isdir(p):
            return art, p
    raise SystemExit("ABBRUCH: das Pack %r liegt weder unter role-packs/ noch unter "
                     "tech-packs/ im Kern dieses Baums" % pack)


def packskills(baum, pack):
    """Die Skillnamen des Packs - aus seinem Verzeichnis, nicht aus einer Liste."""
    _, wurzel = packverzeichnis(baum, pack)
    ablage = os.path.join(wurzel, "skills")
    if not os.path.isdir(ablage):
        return []
    return sorted(n for n in os.listdir(ablage)
                  if os.path.isfile(os.path.join(ablage, n, "SKILL.md")))


def packregeln(baum, pack):
    """Die Laufzeitfassungen des Packs - jede .md unter seinem runtime/."""
    _, wurzel = packverzeichnis(baum, pack)
    ablage = os.path.join(wurzel, "runtime")
    if not os.path.isdir(ablage):
        return []
    return sorted(n for n in os.listdir(ablage) if n.endswith(".md"))


def _korbname(man):
    """Die Schreibweise des Skillaufrufs - oder None, wenn das Pack keine kennt.

    Bei `devin-desktop` ist `permission_tools.skill` DEKLARIERT LEER (D-89): Der
    Aufruf ist dort ein Werkzeugaufruf, aber keine Schreibweise ist bekannt, mit
    der eine Regel ihn beim Namen nennt. Ein FEHLENDES Feld ist etwas anderes und
    ein Befund - dieselbe Trennlinie wie bei D-155, und Pruefung 72 meldet ihn.
    """
    werkzeuge = man.get("permission_tools")
    if not isinstance(werkzeuge, dict) or "skill" not in werkzeuge:
        raise SystemExit("ABBRUCH: das Manifest von %r fuehrt permission_tools.skill "
                         "nicht. Der Unterschied zwischen 'nicht abgebildet' und 'gibt "
                         "es nicht' gehoert deklariert (D-155, D-238)" % man.get("client"))
    namen = [w for w in (werkzeuge.get("skill") or []) if isinstance(w, str)]
    return namen[0] if namen else None


def aktivieren(baum, client, pack):
    """Die drei Teile der Aktivierung - wortgetreu nach ROLE_PACK.md Abschnitt 9.

    Gibt einen Bericht als dict zurueck. Jeder Teil hat seinen Waechter, und
    geschrieben wird erst, wenn alle drei ihren Gegenstand gefunden haben.
    """
    man = manifest(baum, client)
    regelablage, skillablage, rechtedatei = _ablagen(baum, man)
    art, wurzel = packverzeichnis(baum, pack)
    regeln = packregeln(baum, pack)
    skills = packskills(baum, pack)
    if not regeln and not skills:
        raise SystemExit("ABBRUCH: das Pack %r traegt weder eine Laufzeitfassung noch "
                         "einen Skill - es gaebe nichts zu aktivieren" % pack)
    for ablage in (regelablage, skillablage):
        if not os.path.isdir(ablage):
            raise SystemExit("ABBRUCH: %s fehlt - in diesem Baum ist kein Client Pack "
                             "installiert, und die Aktivierung gehoert DANACH"
                             % os.path.relpath(ablage, baum))

    # --- 1. Laufzeitfassung - GERENDERT, nicht kopiert ---------------------------
    inst = _installer(baum) if regeln else None
    for name in regeln:
        # 🔴 FLACHGELEGT, SONST TUT DIE ABBILDUNG NICHTS - und zwar lautlos.
        # `render_rule` steigt aus, wenn der Text nicht mit drei Strichen und
        # einem Zeilenvorschub beginnt, und gibt ihn dann UNVERAENDERT zurueck.
        # Die Quelle im Repositorium ist CRLF; mit newline='' gelesen beginnt sie
        # mit einem Wagenruecklauf davor, und der Aufruf war eine Zusage ohne
        # Wirkung. `install.py` selbst liest im Universal-Newline-Modus und merkt
        # davon nichts.
        #
        #   Ein auf eine Zeilenform verankerter Vergleich trifft nie, wenn der
        #   Text nicht flachgelegt ist - hier einmal ohne regulaeren Ausdruck.
        quelle = io.open(os.path.join(wurzel, "runtime", name),
                         encoding="utf-8", newline="").read()
        quelle = quelle.replace("\r\n", "\n")
        text = inst.resolve_placeholders(inst.render_rule(quelle, man), man)
        # Waechter: hat die Abbildung ueberhaupt gegriffen? Ein Client mit eigener
        # Bedingungssprache MUSS den Kopf umschreiben; bleibt der Anfang gleich,
        # ist sie stillschweigend ausgestiegen (D-23: eine Zusage ohne Wirkung).
        if man.get("rule_triggers") and text[:400] == quelle[:400]:
            raise SystemExit("ABBRUCH: die Laufzeitfassung %s ist unveraendert aus "
                             "der Abbildung gekommen, obwohl %r eine eigene "
                             "Bedingungssprache fuehrt - gerendert wurde nicht, "
                             "kopiert schon" % (name, man.get("client")))
        _schreib(os.path.join(regelablage, name), text)
    # --- 2. Skillablage -----------------------------------------------------------
    for name in skills:
        ziel = os.path.join(skillablage, name)
        _weg(ziel)
        shutil.copytree(os.path.join(wurzel, "skills", name), ziel)

    # --- 3. Korbeintrag (D-238) ---------------------------------------------------
    korb = _korbname(man)
    nachgetragen = []
    if korb and skills:
        cfg = json.loads(_lies(rechtedatei))
        rechte = cfg.setdefault("permissions", {})
        allow = rechte.setdefault("allow", [])
        vorhanden = set()
        for eintraege in rechte.values():
            if isinstance(eintraege, list):
                vorhanden.update(x for x in eintraege if isinstance(x, str))
        for name in skills:
            eintrag = "%s(%s)" % (korb, name)
            if eintrag not in vorhanden:
                allow.append(eintrag)
                nachgetragen.append(eintrag)
        if nachgetragen:
            _schreib(rechtedatei, json.dumps(cfg, ensure_ascii=False, indent=2) + "\n")

    # --- Waechter ueber ALLE DREI Teile -------------------------------------------
    for name in regeln:
        if not os.path.isfile(os.path.join(regelablage, name)):
            raise SystemExit("ABBRUCH: die Laufzeitfassung %s steht nicht in %s"
                             % (name, os.path.relpath(regelablage, baum)))
    for name in skills:
        if not os.path.isfile(os.path.join(skillablage, name, "SKILL.md")):
            raise SystemExit("ABBRUCH: der Skill %s steht nicht in %s"
                             % (name, os.path.relpath(skillablage, baum)))
    if korb and skills:
        text = _lies(rechtedatei)
        for name in skills:
            if "%s(%s)" % (korb, name) not in text:
                raise SystemExit("ABBRUCH: %s(%s) fehlt in der Berechtigungsdatei - "
                                 "das ist der DRITTE Teil der Aktivierung, und ohne "
                                 "ihn faellt der Aufruf in die Abweisung (D-238)"
                                 % (korb, name))
    return {"art": art, "regeln": regeln, "skills": skills,
            "korb": korb, "nachgetragen": nachgetragen}


def entfernen(baum, client, pack, mit_quelle=True):
    """Die Umkehrung der Aktivierung - der Kontrollzuschnitt `ohnepack` (D-242, K-87).

    `mit_quelle` nimmt auch das kanonische Packverzeichnis unter `framework/` mit.
    🔴 DAS IST DER PUNKT VON D-234: Der Messbaum traegt das Framework, und ein Lauf,
    der in der Laufzeitablage nichts findet, liest die kanonische Fassung dort. Ein
    Zuschnitt, der davon abhaengt, wohin der Lauf schaut, ist keiner.
    """
    man = manifest(baum, client)
    regelablage, skillablage, rechtedatei = _ablagen(baum, man)
    art, wurzel = packverzeichnis(baum, pack)
    regeln = packregeln(baum, pack)
    skills = packskills(baum, pack)
    korb = _korbname(man)

    entfernt = []
    for name in regeln:
        p = os.path.join(regelablage, name)
        if os.path.exists(p):
            _weg(p)
            entfernt.append(os.path.relpath(p, baum))
    for name in skills:
        p = os.path.join(skillablage, name)
        if os.path.exists(p):
            _weg(p)
            entfernt.append(os.path.relpath(p, baum))

    gestrichen = []
    if korb and skills and os.path.isfile(rechtedatei):
        cfg = json.loads(_lies(rechtedatei))
        rechte = cfg.get("permissions", {})
        marken = {"%s(%s)" % (korb, n) for n in skills}
        for name, eintraege in rechte.items():
            if not isinstance(eintraege, list):
                continue
            rest = [x for x in eintraege if x not in marken]
            if len(rest) != len(eintraege):
                gestrichen += [x for x in eintraege if x in marken]
                rechte[name] = rest
        if gestrichen:
            _schreib(rechtedatei, json.dumps(cfg, ensure_ascii=False, indent=2) + "\n")

    if mit_quelle:
        _weg(wurzel)
        entfernt.append(os.path.relpath(wurzel, baum))

    # --- Waechter: KEIN Traeger des Packs mehr im Baum, an keiner Stelle ----------
    # Ein Praefixvergleich auf der Laufzeitablage haette `.koolie/core/` nie
    # gesehen; er geht deshalb ueber den ganzen Baum (D-234, D-239).
    rest = []
    gesucht = set(regeln)
    for basis, ordner, dateien in os.walk(baum):
        ordner[:] = [o for o in ordner if o != ".git"]
        if os.path.basename(basis) in skills and "SKILL.md" in dateien:
            rest.append(os.path.relpath(os.path.join(basis, "SKILL.md"), baum))
        for d in dateien:
            if d in gesucht:
                rest.append(os.path.relpath(os.path.join(basis, d), baum))
    if rest:
        raise SystemExit("ABBRUCH: %d Traeger des Packs %r stehen noch im Zuschnitt: "
                         "%s (D-242)" % (len(rest), pack, ", ".join(sorted(rest)[:5])))
    return {"art": art, "entfernt": entfernt, "gestrichen": gestrichen}
