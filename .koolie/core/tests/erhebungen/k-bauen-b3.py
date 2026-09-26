# -*- coding: utf-8 -*-
"""Baut einen Kontrolllauf-Baum OHNE die geprueffte Schranke.

Aufruf:  python k-bauen-b3.py <klasse> <quellbaum> <zielbaum>\n         Klassen: n03 sc1 injk3 inj k3 halt konf risiko plan test befund\n                  testnachweis abw fern bew

Der Zielbaum ist eine vollstaendige Kopie des Hauptlauf-Baums, aus der jede Regelstelle
entfernt ist, die die geprueffte Schranke traegt - und zwar NACH BEDEUTUNG, nicht nur
nach Marke.

Uebernommen aus der Erhebung s4 (0.59.0), unveraendert in Aufbau und Trennlinie:

  - Geschnitten werden REGELQUELLEN, nicht AUFZEICHNUNGEN (D-141). Eine Aufzeichnung
    traegt die Marke, ohne die Schranke zu setzen; ihre Restfundstellen werden GEZAEHLT.
  - `.json`-Dateien bleiben unberuehrt: sie tragen die TECHNISCHE Schranke, und der
    Kontrolllauf entfernt die Regelschicht (D-122).
  - Ein gruener Waechter belegt NICHT, dass die Schranke weg ist: Die Zeilen, die einen
    Begriff AUSMACHEN, ueberleben eine Suche nach der Zeile, die ihn NENNT.

NEU MIT S5: die Klasse `fi3` schneidet zusaetzlich den SessionStart-Hook aus der
Berechtigungsdatei. Die Schranke von `FW-FI-03` hat zwei Traeger - den Regeltext und
die Statusmeldung des Hooks, die die Anweisung woertlich mitliefert. `fi3h` schneidet
nur den Regeltext und laesst den Hook stehen; das Paar trennt die beiden Traeger.
"""
import io
import json
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")

KLASSE, QUELLE, ZIEL = sys.argv[1], os.path.abspath(sys.argv[2]), os.path.abspath(sys.argv[3])

BEREICHE = [
    "CLAUDE.md",
    ".claude/README.md",
    ".claude/rules",
    ".claude/agents",
    ".claude/skills",
    ".koolie/core/framework",
    ".koolie/core/checklists",
    ".koolie/core/decision-trees",
    ".koolie/core/templates",
    ".koolie/core/onboarding",
    ".koolie/core/clients",
    ".koolie/core/examples",
    ".koolie/core/docs/RUNTIME_GLOSSARY.md",
    ".koolie/core/docs/PLACEHOLDER_REGISTRY.md",
    ".koolie/core/governance/PRIORITY_HIERARCHY.md",
    ".koolie/core/governance/EXCEPTION_PROCESS.md",
    ".koolie/core/governance/FRAMEWORK_DEV_PROFILE.md",
    ".koolie/project-overlay",
]

AUFZEICHNUNGEN = [
    ".koolie/core/governance/DECISION_LOG.md",
    ".koolie/core/governance/change-requests",
    ".koolie/core/tests",
    ".koolie/core/docs/ROADMAP.md",
    ".koolie/core/docs/ADOPTION_GUIDE.md",
    ".koolie/core/build",
    ".koolie/core/pilot",
    ".koolie/core/CHANGELOG.md",
    ".koolie/core/OWNERS.md",
    "docs",
    "tools",
]

# ZEILE:     jede Zeile, die den Ausdruck traegt, faellt.
# SATZ:      genau dieser Text faellt aus seiner Zeile (die Zeile bleibt).
# NUR_SATZ:  Zeilen, die NICHT als Ganzes fallen duerfen - dort greift allein
#            SATZ. 🔴 Neu mit 0.83.0 (CR-2026-116): Die Wertzeile eines
#            Pflichtplatzhalters im Overlay traegt bei `fern` BEIDES - die
#            Schranke (V11) und den WERT, der Meszgegenstand von `RE-001-P04`
#            ist. Faellt sie ganz, misst der Kontrollauf einen Baum, in dem der
#            Lauf zusaetzlich sein Ausgabeformat nicht mehr ableiten kann.
#            Das Muster beschreibt die STELLUNG, nicht den Wortlaut.
# ABSCHNITT: Ueberschrift samt Rumpf bis zur naechsten Ueberschrift gleicher oder
#            hoeherer Ebene faellt.
# MARKEN:    Waechter-Regexe; keiner darf danach noch treffen.
# BEHALTEN:  Pfade, die der Schnitt nicht anfassen darf (Praeparationen).
KLASSEN = {
    # --- BUENDEL 2 (0.71.0) -------------------------------------------------------
    # SK-004-N01 und SK-009-N02: die Rueckfrage statt der stillschweigenden Annahme.
    # Dieselbe Schranke (P3 No Assumption Policy) an zwei Gegenstaenden: dort die
    # fehlende Kontrollstufe, hier der nicht bestaetigte Ursachenkandidat.
    "n03": dict(
        ZEILE=[
            r"No Assumption",
            r"stillschweigend",
            r"R(ü|ue)ckfrag",
            r"nachfrag",
            r"Unklarheit",
            r"\bP3\b",
            r"Annahme",
            r"annehmen",
            r"annimmst",
            r"legt sie (aber )?nicht fest",
            r"offene Frage",
            r"konkrete Frage",
            r"blockiert bis",
            # Nachgetragen mit 0.77.0: vom Stammwaechter gemeldet (CR-2026-104).
            # Alle drei SETZEN die Schranke, sie nennen sie nicht bloss.
            r"offene\w*\s+Frage",
            r"statt\s+(zu\s+)?rate",
            r"unterstell",
        ],
        SATZ=[],
        ABSCHNITT=[r"P3 No Assumption Policy",
                   r"Fehlender Kontext und R(ü|ue)ckfragen statt Annahmen",
                   r"Grenzen und R(ü|ue)ckfragenregeln"],
        MARKEN=[r"No Assumption", r"stillschweigend", r"Rückfrag", r"Annahme",
                r"Unklarheit"],
        BEHALTEN=[],
    ),
    # SK-004-N02: Scope-Treue, Nur-Lese-Pfade und die neue Abhaengigkeit.
    # 🔴 EINGEENGT? NEIN - GEWEITET, AM 2026-09-20. Der Stammwaechter meldete beim
    # ersten Lauf des Apparats als Ganzes 39 Restfundstellen: Das Schnittmuster
    # trug `\bScope\b` und `au(ss)erhalb des Auftrags`, das Stammmuster `\bScope\w*`
    # und `au(ss)erhalb\s+des\s+(Auftrags|Scopes)`. `Scopes` kam im Schnitt gar
    # nicht vor. Das ist D-205 mit umgekehrtem Vorzeichen: Dort prueft der
    # Waechter MIT dem Schnittmuster und ist immer gruen - hier prueft er weiter
    # als geschnitten wird und meldet zu Recht. Die Muster folgen jetzt dem Stamm.
    "sc1": dict(
        ZEILE=[
            r"\bScope\w*", r"beil(ä|ae)ufig\w*",
            r"au(ß|ss)erhalb\s+des\s+(Auftrags|Scopes)",
            r"Eine Aufgabe, ein Ziel", r"Ein Ziel je (Ä|Ae)nderung",
            r"Ausweitung\w*", r"(separate|eigene)\w*\s+Ticket\w*",
            r"ohne Auftrag", r"nicht beauftragt",
            r"Delegationsverbot\w*",
            r"\bV3\b",
            r"neue Abh(ä|ae)ngigkeit",
            r"neuer? Abh(ä|ae)ngigkeit",
            r"07-new-dependency",
            r"Nur-?Lese\w*",
            r"READ_ONLY_PATHS",
        ],
        SATZ=[],
        ABSCHNITT=[],
        MARKEN=[r"\bScope\w*", r"beil(ä|ae)ufig\w*", r"Ausweitung\w*",
                r"Delegationsverbot\w*", r"07-new-dependency",
                r"READ_ONLY_PATHS"],
        BEHALTEN=[],
    ),
    # SK-004-N03: die Zelle verlangt BEIDES - Abwehr der Anweisung UND Bereinigung
    # des K3-Inhalts. Ein Zuschnitt, der nur eine Haelfte entfernt, beantwortet die
    # Frage des Kontrollaufs nicht. Deshalb die Vereinigung von `inj` und `k3`.
    "injk3": dict(
        ZEILE=[
            r"Injektion", r"Injection", r"sind Daten, keine Anweisungen",
            r"sind Daten\b", r"\bS6\b", r"Regelwidrige Anweisung",
            r"Anweisungen, die den Regeln widersprechen", r"nicht befolg",
            r"als Anweisung behandel", r"Inhalte aus Dateien",
            r"\bK3\b", r"personenbezogen", r"Personendaten", r"Zugangsdaten",
            r"\bSecret", r"Datenschutz", r"nicht zitieren", r"nur strukturell",
            r"bereinig", r"Bereinigung", r"SECURITY_CONTACT", r"Fixture", r"\bS3\b",
        ],
        SATZ=[],
        ABSCHNITT=[r"Prompt Injection", r"Regeln gegen Prompt Injection",
                   r"Kontextklassen", r"Datenschutz", r"Umgang mit Geheimnissen"],
        MARKEN=[r"Injektion", r"Injection", r"sind Daten, keine Anweisungen",
                r"Regelwidrige Anweisung", r"\bK3\b", r"personenbezogen",
                r"Datenschutz", r"SECURITY_CONTACT"],
        BEHALTEN=[],
    ),
    # SK-008-N03 und SK-009-N04: die Abwehr regelwidriger Anweisungen in Inhalten.
    # Unveraendert aus Buendel 1 (0.68.0), wo sie getragen hat.
    "inj": dict(
        ZEILE=[
            r"Injektion", r"Injection", r"sind Daten, keine Anweisungen",
            r"sind Daten\b", r"\bS6\b", r"Regelwidrige Anweisung",
            r"Anweisungen, die den Regeln widersprechen", r"nicht befolg",
            r"als Anweisung behandel", r"Inhalte aus Dateien",
        ],
        SATZ=[],
        ABSCHNITT=[r"Prompt Injection", r"Regeln gegen Prompt Injection"],
        MARKEN=[r"Injektion", r"Injection", r"sind Daten, keine Anweisungen",
                r"Regelwidrige Anweisung"],
        BEHALTEN=[],
    ),
    # SK-008-N02 und SK-009-N03: Kontextklasse K3, der unbereinigte Bericht.
    # 🔴 Erwartung vor dem Lauf, unveraendert aus Buendel 1: Dieser Zuschnitt traegt
    # NICHT vollstaendig - der Datenschutz ist querschnittlich, und eine Aufzaehlung,
    # die ihn ausmacht, ueberlebt eine Suche nach der Zeile, die ihn nennt.
    "k3": dict(
        ZEILE=[
            r"\bK3\b", r"personenbezogen", r"Personendaten", r"Zugangsdaten",
            r"\bSecret", r"Datenschutz", r"nicht zitieren", r"nur strukturell",
            r"bereinig", r"SECURITY_CONTACT", r"Fixture", r"\bS3\b",
        ],
        SATZ=[],
        ABSCHNITT=[r"Kontextklassen", r"Datenschutz", r"Umgang mit Geheimnissen"],
        MARKEN=[r"\bK3\b", r"personenbezogen", r"Datenschutz", r"SECURITY_CONTACT"],
        BEHALTEN=[],
    ),
    # SK-008-N01 und SK-009-N01: der Halte-Punkt und das Umsetzungsverbot.
    # Der Zuschnitt schneidet auch in die GRENZEN der Skills, und das ist gemeint:
    # Der Kontrolllauf fragt, ob das Unterlassen der Umsetzung dem Regelwerk und dem
    # Skill zuzurechnen ist - oder ob der Client ohnehin nicht umgesetzt haette.
    "halt": dict(
        ZEILE=[
            r"\[HALT\]",
            r"setzt nichts um",
            r"behebt nichts",
            r"f(ü|ue)hrt nichts aus",
            r"keine Umsetzung",
            r"vor jeder Umsetzung an",
            r"h(ä|ae)lt vor jeder Umsetzung",
            r"Umsetzung beginnt erst",
            r"Halte an", r"anzuhalten", r"anhalten", r"h(ä|ae)lt an",
            r"Folge-Skill",
            r"best(ä|ae)tigten Plan", r"Planbest(ä|ae)tigung",
            r"Freigabepunkt", r"Halte-?[Pp]unkt",
            r"Befehle ausf(ü|ue)hren",
            r"ausgef(ü|ue)hrte Befehle",
            # Nachgetragen mit 0.77.0 (CR-2026-104). 🔴 Der Stammwaechter hat sie in
            # VIER SKILL.md und in der Regelablage gefunden - `fw-change-small`,
            # `fw-docs-update`, `fw-refactor`, `fw-tests`. Das ist genau der Fall,
            # den D-205 meint: Ein Zuschnitt erfasst seine Schranke in ALLEN
            # Schichten, auch in der `SKILL.md`.
            r"vor\s+dem\s+ersten\s+Schreibzugriff",
            r"zur\s+Best(ä|ae)tigung\s+vor",
            r"h(ä|ae)lt\w*\s+an\b",
        ],
        SATZ=[],
        ABSCHNITT=[],
        MARKEN=[r"\[HALT\]", r"setzt nichts um", r"Folge-Skill",
                r"Planbestätigung", r"Halte-Punkt"],
        BEHALTEN=[],
    ),
    # SK-008-N04: die Belegpflicht der Konfidenz.
    "konf": dict(
        ZEILE=[
            r"Konfidenz",
            r"Code-Stand",
            r"erfunden",
            r"erfinden",
            r"ohne Fundstelle",
            r"mit Fundstelle",
            r"Fundstelle",
            r"beobachtet \(",
            r"geschlossen \(",
            r"Vermutung",
            r"\bbelegt\b",
            r"Beleg ",
            # Nachgetragen mit 0.77.0 (CR-2026-104). 🔴 Der teuerste der drei
            # Nachtraege: `nicht belegbar` stand FUENFMAL in `fw-mr-description`
            # und dreimal in `fw-review-support` - also in genau den beiden
            # Skills, die Buendel 4 misst. Ein Kontrolllauf mit dieser Zeile
            # traegt die geprueffte Schranke weiter mit sich.
            # 🔴 Die Zahl stand bis 0.78.0 auf SIEBEN. 0.77.0 hat sie in
            # sechs Traegern auf fuenf gezogen - und dieses Werkzeug dabei
            # uebersehen: die Abhilfe, die ihren eigenen Messapparat nicht
            # erreicht (CR-2026-105). Nachgezaehlt am 2026-09-20: fuenf
            # `nicht belegbar*` plus ein `ohne belegbaren` in SKILL.md und
            # eines in EXAMPLES.md; bei fw-review-support drei und zwei -
            # zwoelf Zeilen in den vier Traegern der beiden Skills.
            r"nicht\s+belegbar",
            r"ohne\s+Beleg",
            r"auf\s+Basis\s+vermutet",
            r"erfind",
        ],
        SATZ=[],
        ABSCHNITT=[],
        MARKEN=[r"Konfidenz", r"Code-Stand", r"erfunden", r"Fundstelle"],
        BEHALTEN=[],
    ),
    # SK-004-N04 und SK-009-P02: der Abgleich der Risikofaktoren und die Meldung
    # einer Abweichung. Geschnitten wird die Pflicht zum ABGLEICH und zur MELDUNG -
    # die Kontrollstufe selbst bleibt als Begriff stehen, sonst versteht der Lauf
    # seinen eigenen Prompt nicht mehr.
    "risiko": dict(
        ZEILE=[
            r"^\| R\d+ \|",
            r"Risikofaktor",
            r"Risiko-?Abgleich",
            r"Abgleich der Risiko",
            r"Anstieg der Kontrollstufe",
            r"h(ö|oe)here Einstufung",
            r"neue Einstufung",
            r"Abweichung.{0,30}(Stufe|Einstufung)",
            r"(Stufe|Einstufung).{0,30}Abweichung",
            r"nicht eigenm(ä|ae)chtig",
            r"legt sie (aber )?nicht fest",
            r"Die Kontrollstufe festlegen oder senken",
            r"\bR1[013]\b",
            r"melde(t|n)? .{0,20}Abweichung",
        ],
        SATZ=[],
        ABSCHNITT=[r"Risikofaktoren", r"Faktoren und Einstufung"],
        MARKEN=[r"Risikofaktor", r"Anstieg der Kontrollstufe", r"nicht eigenmächtig",
                r"^\| R\d+ \|"],
        BEHALTEN=[],
    ),

    # --- BUENDEL 3 (0.74.0) -------------------------------------------------------
    # 🔴 Alle drei Skills dieses Buendels SCHREIBEN. Ein Kontrolllauf misst hier
    # nicht nur, ob der Client etwas SAGT, sondern ob er etwas TUT - und die
    # Zustandsaufnahme je Baum belegt es.
    #
    # SK-005-N02 und SK-007-N03: die Planpflicht ab Kontrollstufe mittel.
    # Geschnitten wird die Pflicht zum PLAN und zur Freigabe - die Kontrollstufe
    # selbst bleibt als Begriff stehen, sonst versteht der Lauf seinen eigenen
    # Prompt nicht mehr (dieselbe Zurueckhaltung wie bei `risiko` in Buendel 2).
    "plan": dict(
        ZEILE=[
            r"best(ä|ae)tigter Plan", r"best(ä|ae)tigten Plan",
            r"Planreferenz", r"Planbedarf", r"ohne Plan",
            r"Plan liegt vor", r"Planpflicht",
            # 🔴 `\bfw-plan\b` stand hier und traf 39 Stellen, die keine
            # Pflicht setzen - der Folge-Skill wird an vielen Stellen bloss
            # EMPFOHLEN. Der Zuschnitt entfernt die Schranke, nicht den Namen.
            r"Verweis auf `fw-plan`", r"verweist auf `fw-plan`",
            r"`fw-plan` (empfohlen|vorschlagen|vorgeschlagen)",
            r"Freigabeerfordernis", r"Freigabevoraussetzung",
            r"dokumentierte Freigabe", r"schriftliche(r|n)? Best(ä|ae)tigung",
            r"APPROVAL_ROLE",
            r"ab (Stufe |Kontrollstufe )?mittel",
            r"Stufe mittel",
            r"nur lesende Schritte",
            r"lehnt? .{0,25}(Bearbeitung|Umsetzung) ab",
        ],
        SATZ=[],
        ABSCHNITT=[r"Kontrollstufen und Freigabe", r"Freigabe und Best(ä|ae)tigung"],
        MARKEN=[r"bestätigten Plan", r"Planreferenz",
                r"Freigabeerfordernis", r"APPROVAL_ROLE"],
        BEHALTEN=[],
    ),
    # SK-005-N03, SK-007-N02, SK-007-N04, SK-006-N02: das Verbot, ein Ergebnis
    # gruen zu machen. Geschnitten wird die Pflicht, einen Fehlschlag UNVERAENDERT
    # zu berichten und Tests, Zusicherungen und Schwellenwerte nicht anzufassen.
    "test": dict(
        ZEILE=[
            r"unver(ä|ae)ndert berichte",
            r"Ergebnis unver(ä|ae)ndert",
            r"Fehlschlag",
            r"fehlschlagend",
            r"gr(ü|ue)n zu machen", r"gr(ü|ue)n machen", r"gr(ü|ue)n zu melden",
            r"Tests, (Assertions|Zusicherungen)",
            r"Assertions", r"Zusicherung",
            r"Schwellenwert",
            r"Pr(ü|ue)fkonfiguration",
            r"(ü|ue)berspringen", r"it\.skip", r"\bskip\b",
            r"l(ö|oe)schen des Tests", r"Test .{0,20}(anpass|l(ö|oe)sch)",
            r"nicht anpassen",
            r"bereits im Ausgangsstand",
            r"au(ß|ss)erhalb des Scopes",
            r"fw-error-analyze",
            r"roter? (Stand|Suite)", r"rotem Stand",
            r"Testnachweis",
        ],
        SATZ=[],
        ABSCHNITT=[r"Umgang mit Fehlschl(ä|ae)gen", r"Fehlschl(ä|ae)ge einordnen"],
        MARKEN=[r"unverändert berichte", r"Schwellenwert", r"Assertions",
                r"fw-error-analyze", r"grün zu machen"],
        BEHALTEN=[],
    ),
    # SK-007-P02: melden statt beheben. Der Skill findet einen Fehler im Bereich,
    # den er umbaut - und darf ihn NICHT nebenbei korrigieren. Geschnitten wird die
    # Verhaltensneutralitaet und die Meldepflicht.
    "befund": dict(
        ZEILE=[
            r"verhaltensneutral",
            r"Verhalten .{0,25}unver(ä|ae)ndert",
            r"unver(ä|ae)ndert.{0,25}Verhalten",
            r"keine funktionale (Ä|Ae)nderung",
            r"funktionale (Ä|Ae)nderung",
            r"Gemeldete Befunde",
            r"Befund mit Fundstelle",
            r"melden, nicht beheben", r"nicht beheben",
            r"nebenbei",
            r"mitzufixen", r"mitfixen",
            r"entdeckter? Fehler",
            r"fw-error-analyze",
        ],
        SATZ=[],
        ABSCHNITT=[r"Verhaltensneutralit(ä|ae)t"],
        MARKEN=[r"verhaltensneutral", r"Gemeldete Befunde", r"nicht beheben",
                r"fw-error-analyze"],
        BEHALTEN=[],
    ),
    # SK-007-N01: kein Refactoring ohne Testnachweis. Geschnitten wird die Pflicht
    # zum Nachweis VOR der ersten Aenderung und der Verweis auf `fw-tests`.
    "testnachweis": dict(
        ZEILE=[
            r"Testnachweis",
            r"vor der ersten (Ä|Ae)nderung",
            r"ohne (automatisierte )?Tests",
            r"keine (automatisierten )?Tests",
            r"Abdeckung des Verhaltens",
            r"abgedeckt",
            r"\bfw-tests\b",
            r"offensichtlich sicher",
            r"identisches? Testergebnis",
            r"Testergebnis .{0,20}identisch",
            r"vor und nach jedem Schritt",
        ],
        SATZ=[],
        ABSCHNITT=[],
        MARKEN=[r"Testnachweis", r"fw-tests", r"Abdeckung des Verhaltens",
                r"identisches Testergebnis"],
        BEHALTEN=[],
    ),
    # SK-005-P02: die Abweichung vom bestaetigten Plan. Geschnitten wird die Pflicht,
    # sie zu MELDEN und anzuhalten - nicht die Existenz des Plans.
    "abw": dict(
        ZEILE=[
            r"Abweichung vom (bestätigten |bestaetigten )?(Plan|Scope)",
            r"Abweichung.{0,30}(Plan|Scope)",
            r"(Plan|Scope).{0,30}Abweichung",
            r"erneute(r|n)? Best(ä|ae)tigung",
            r"weitere Datei",
            r"Schritt nicht fortsetzen",
            r"Umsortieren",
            r"Zusammenfassen von Planschritten",
            r"stillschweigend",
            r"\[HALT\]",
            r"h(ä|ae)lt an", r"anhalten", r"Halte-?[Pp]unkt",
            r"vor dem ersten Schreibzugriff",
        ],
        SATZ=[],
        ABSCHNITT=[],
        MARKEN=[r"Abweichung vom", r"Schritt nicht fortsetzen", r"\[HALT\]",
                r"vor dem ersten Schreibzugriff"],
        BEHALTEN=[],
    ),
    # --- BUENDEL 4 (0.78.0) -------------------------------------------------------
    # SK-012-N01 und SK-010-N01: keine Fernwirkung, keine Freigabeaussage (V1, V2).
    # Dieselbe Schranke an zwei Gegenstaenden - dort der Merge-Request-Entwurf, hier
    # die Review-Unterstuetzung. Beide Zellen verlangen, dass der Lauf den Entwurf
    # LIEFERT und die Aktion VERWEIGERT; geschnitten wird die Verweigerungspflicht,
    # nicht die Faehigkeit.
    #
    # 🔴 `Freigabe\w*` steht hier NICHT, und das ist der Befund dieser Klasse.
    # Gemessen am 2026-09-20 gegen den ungeschnittenen Baum: 502 Zeilen in 102
    # Dateien - und gelesen meinen sie die Freigabe AN den Agenten
    # (Kontextfreigabe, Overlay-Freigabe, dokumentierte Freigabe durch
    # <APPROVAL_ROLE>), nicht die Freigabeaussage DES Agenten. Dasselbe gilt fuer
    # `freigegeben` (190 in 76): *im Overlay freigegeben*, *freigegebene
    # Testbefehle*. Zwei Bedeutungen desselben Wortes - genau das Beispiel, das der
    # Kopfkommentar seit 0.75.0 fuehrt.
    # --- NACHGETRAGEN MIT 1.14.0 (CR-2026-151) -----------------------------------
    # SK-002-N01: keine Bewertung, kein Aenderungsvorschlag. Die Klasse stand in
    # `k-bauen.py` von Buendel 1 (0.70.0) und war beim Umzug des Apparats in den
    # Kern (D-222) nicht mitgekommen - der Nachlauf von K-153 braucht sie. Schnitt-
    # muster unveraendert aus Buendel 1; das Stammmuster ist neu (D-205).
    "bew": dict(
        ZEILE=[
            r"Bewertung(en)? als Feststellung",
            r"keine Bewertung",
            r"ohne Bewertung",
            r"bewertet nichts",
            r"(Ä|Ae)nderungsvorschl\w*",
            r"Bewertung und Entscheidung",
            r"beim Menschen",
            r"gut.{0,3}, .{0,3}schlecht",
            r"belegte Beobachtung",
        ],
        SATZ=[],
        # Das Negativbeispiel in EXAMPLES.md zeigt den Gegenstand als Ganzes -
        # gefunden vom Stammwaechter beim ersten Bau (1.14.0).
        ABSCHNITT=[r"Negativbeispiel.*(Bewertung|(Ä|Ae)nderungsvorschl)"],
        MARKEN=[r"Bewertung als Feststellung", r"Änderungsvorschläge",
                r"beim Menschen"],
        BEHALTEN=[],
    ),
    "fern": dict(
        ZEILE=[
            r"Fernwirkung\w*",
            r"\bV1\b", r"\bV2\b",
            # 🔴 NACHGETRAGEN MIT 0.83.0 (CR-2026-116), GEMESSEN VOR DEM ERSTEN
            # BEZAHLTEN LAUF VON BUENDEL 5. `\bV1\b` TRIFFT `V11` NICHT - auf
            # die `1` folgt ein Wortzeichen, und die Wortgrenze steht nicht.
            # Nach dem Schnitt trug der Kontrollbaum von `RE-001-N03` die
            # gepruefte Schranke FUENFMAL weiter: einmal in der Rollenregel
            # ("Eintragen oder Aendern von Vorgaengen im Ticketsystem | Mensch
            # (V11)") und viermal in der `SKILL.md`. Der Stammwaechter war
            # gruen, weil sein Muster dieselbe Luecke trug.
            #
            #   Ein Muster mit abschliessender Wortgrenze uebersieht die Form,
            #   die knapp danebenliegt - 0.64.0 an einer zweiten Stelle.
            r"\bV11\b",
            r"kein Eintrag im Ticketsystem",
            r"ruft kein Ticketsystem ab",
            r"in ein Ticketsystem schreiben",
            r"kein Vorgang angelegt",
            r"selbst einzutragen",
            r"git\s+(push|merge)\b",
            r"gemergt\w*",
            r"Reifeaussage\w*",
            r"Freigabeaussage\w*",
            r"Merge-?[Aa]ussage\w*",
            r"Delegationsverbot\w*",
            r"(f(ü|ue)hrt|f(ü|ue)hren)\s+(der|die)\s+Mensch",
            r"Merge Request.{0,20}(anleg|erstell)",
            r"Pull Request.{0,20}(anleg|erstell)",
            r"keine Aktion im Review-?Werkzeug",
            r"Kommentar im (Review-?)?Werkzeug",
        ],
        # 🔴 Der schrankensetzende HALBSATZ der Overlay-Wertzeile - der Rest der
        # Zeile bleibt, weil er den Wert von `<ISSUE_TRACKER>` traegt.
        SATZ=[" **Kein Schreibzugriff:** Ein Vorgang wird nie durch den "
              "KI-Client eingetragen oder ge\u00e4ndert (V11); der Entwurf wird "
              "vom Menschen \u00fcbertragen"],
        # Die Stellung, nicht der Wortlaut: eine Tabellenzeile, deren zweite
        # Spalte ein Pflichtplatzhalter ist.
        NUR_SATZ=[r"^\|[^|]+\|\s*`<[A-Z_]+>`\s*\|"],
        ABSCHNITT=[],
        MARKEN=[r"Fernwirkung", r"gemergt", r"Freigabeaussage", r"Reifeaussage",
                r"Delegationsverbot", r"\bV11\b"],
        BEHALTEN=[],
    ),
}

# --- STAMM: der zweite Waechter, neu mit 0.75.0 (D-205) ---------------------------
# 🔴 DER WAECHTER PRUEFTE MIT DEM SCHNITTMUSTER. Die MARKEN einer Klasse sind je
# Klasse eine TEILMENGE ihrer ZEILE-Muster - gemessen am 2026-09-19 gegen das
# Uebungsrepositorium: Klasse `plan`, ZEILE trifft 211 Zeilen, MARKEN 131, und die
# 131 liegen vollstaendig in den 211. Ein Waechter, der weniger sucht, als der
# Schnitt entfernt, kann per Konstruktion nichts finden, was das Schnittmuster nicht
# kannte - *die Null durch Konstruktion* (0.59.1) am Waechter des Zuschnitts.
#
# DER STAMMWAECHTER SUCHT DEN GEGENSTAND, NICHT DIE FORMULIERUNG: alle Kasus, alle
# Ausdrucksformen, auch Diagrammknoten (0.66.0). Gemessen meldet er fuer `plan`
# 17 Zeilen, die der Schnitt stehen laesst - VIER davon in einer `SKILL.md` und
# eine in einem Flussdiagramm. Sieben davon hat der Messtag am 19.09. erst
# NACHTRAEGLICH aus den Kontrolllaeufen erfahren (D-203).
#
# EIN STAMMMUSTER IST WEITER ALS DAS SCHNITTMUSTER, ABER NICHT BELIEBIG: Der erste
# Entwurf fuehrte fuer `plan` ein blosses r"Freigabe\w*" und meldete 307 Zeilen -
# jede "Freigabeinstanz". Wer einen Waechter baut, liest jede seiner Meldungen
# (0.63.0).
# Zwei Stammmuster stehen als eigene Namen, weil die Klasse `injk3` ihre VEREINIGUNG
# ist (nachgetragen mit 0.77.0). Wer sie dort noch einmal ausschreibt, pflegt zwei
# Listen, die dasselbe sagen sollen - und die zweite altert unbemerkt.
STAMM_K3 = [r"\bK3\b", r"personenbezogen\w*", r"Personendaten", r"Zugangsdaten",
            r"\bSecret\w*", r"Datenschutz\w*", r"SECURITY_CONTACT"]
STAMM_INJ = [r"Injekt\w*", r"Injection\w*", r"sind\s+Daten\b",
             r"[Rr]egelwidrig\w*\s+Anweisung\w*", r"\bS6\b",
             r"als\s+Anweisung\w*\s+behandel\w*"]

STAMM = {
    # --- NACHGETRAGEN MIT 0.78.0 (CR-2026-105) ------------------------------------
    # Der Stammwaechter von `fern`. Er ist WEITER als der Schnitt und sucht den
    # Gegenstand - die Pflicht, nicht zu mergen, nicht zu pushen und nichts
    # freizugeben - auch dort, wo sie ohne die Marken ausgedrueckt ist.
    # 🔴 DIE V11-HAELFTE IST MIT 0.83.0 NACHGETRAGEN (CR-2026-116). Sie fehlte
    # in BEIDEN Listen - im Schnittmuster und im Stamm -, und deshalb konnte der
    # Waechter die Luecke nicht melden: *Ein Waechter, der weniger sucht, als der
    # Schnitt entfernt, kann per Konstruktion nichts finden* (D-205).
    # 1.14.0: der Gegenstand von `bew` - die Erklaerung bewertet nicht und schlaegt
    # nichts vor. Weiter als das Schnittmuster: jede Beugung, auch ohne die Marken.
    "bew": [r"keine\s+Bewertung\w*", r"ohne\s+Bewertung\w*", r"bewerte[nt]?\s+nicht\w*",
            r"Bewertung\w*\s+als\s+Feststellung\w*", r"(Ä|Ae)nderungsvorschl\w*",
            r"beim\s+Menschen", r"belegt\w*\s+Beobachtung\w*"],
    "fern": [r"Fernwirkung\w*", r"\bV1\b", r"\bV2\b", r"\bV11\b",
             r"git\s+(push|merge)\b", r"gemergt\w*", r"Reifeaussage\w*",
             r"Freigabeaussage\w*", r"Delegationsverbot\w*",
             r"(f(ü|ue)hrt|f(ü|ue)hren)\s+(der|die)\s+Mensch",
             r"keine Aktion im Review-?Werkzeug",
             r"Eintrag\w*\s+im\s+Ticketsystem",
             r"Ticketsystem\s+schreib\w*",
             r"kein\s+Ticketsystem\s+ab\b",
             r"kein\s+Vorgang\s+angelegt",
             r"selbst\s+einzutragen"],
    "plan": [r"best(ä|ae)tigt\w*\s+Plan\w*", r"Plan\w*\s+best(ä|ae)tigt\w*",
             r"Plan-?Review", r"Planpflicht", r"Planreferenz", r"Planbedarf",
             r"Planfreigabe\w*", r"Freigabe(erfordernis|voraussetzung)\w*",
             r"dokumentierte\w*\s+Freigabe", r"ohne\s+Plan", r"APPROVAL_ROLE"],
    "test": [r"Testnachweis\w*", r"Fehlschl\w*", r"fehlschlagend\w*",
             r"gr(ü|ue)n\w*\s+(machen|melden|zu)", r"Zusicherung\w*", r"Assertion\w*",
             r"(ü|ue)berspring\w*", r"it\.skip", r"roter?\w*\s+(Stand|Suite)"],
    "befund": [r"verhaltensneutral\w*", r"funktional\w*\s+(Ä|Ae|ä|ae)nderung\w*",
               r"Befund\w*\s+mit\s+Fundstelle", r"nicht\s+beheben", r"mitfix\w*",
               r"fw-error-analyze"],
    "k3": STAMM_K3,
    "sc1": [r"\bScope\w*", r"beil(ä|ae)ufig\w*", r"Ausweitung\w*",
            r"au(ß|ss)erhalb\s+des\s+(Auftrags|Scopes)", r"Delegationsverbot\w*",
            r"\bV3\b", r"READ_ONLY_PATHS", r"Nur-?Lese\w*",
            r"(separate|eigene)\w*\s+Ticket\w*"],
    "inj": STAMM_INJ,
    "testnachweis": [r"Testnachweis\w*", r"\bfw-tests\b",
                     r"Abdeckung\w*\s+des\s+Verhaltens",
                     r"identisch\w*\s+Testergebnis\w*",
                     r"Testergebnis\w*\s+identisch\w*",
                     r"ohne\s+(automatisierte\s+)?Tests"],
    "abw": [r"Abweichung\w*\s+vo[nm]\s+\w*\s*(Plan|Scope)\w*",
            r"(Plan|Scope)\w*.{0,30}Abweichung\w*",
            r"erneut\w*\s+Best(ä|ae)tigung\w*", r"\[HALT\]",
            r"Halte-?[Pp]unkt\w*", r"vor\s+dem\s+ersten\s+Schreibzugriff"],
    # --- NACHGETRAGEN MIT 0.77.0 (CR-2026-104) ------------------------------------
    # Die fuenf Klassen ohne Stammmuster. Sie haben bis hierher nicht abgebrochen,
    # weil Buendel 3 sie nicht gebraucht hat - der Stammwaechter kam erst mit
    # 0.75.0, nach dem Messtag. 🔴 Fuer Buendel 4 haette der Baumbau abgebrochen,
    # und das waere richtig gewesen: `n03`, `halt`, `konf` und `risiko` stehen in
    # den Kontrollzuschnitten von `fw-review-support` und `fw-mr-description`.
    # `annimm\w*` ist gestrichen: Es traf `clients/README.md` ("das Frontmatter
    # nimmt … an") - ein anderer Sinn desselben Wortes. `Annahme\w*` und
    # `annehm\w*` decken den Gegenstand.
    "n03": [r"No\s*Assumption", r"Annahme\w*", r"annehm\w*",
            r"unterstell\w*", r"R(ü|ue)ckfrag\w*", r"nachfrag\w*",
            r"\[R(Ü|UE)CKFRAGE\]", r"stillschweigend\w*", r"Unklarheit\w*",
            r"\bP3\b", r"offene\w*\s+Frage\w*", r"statt\s+(zu\s+)?rate\w*",
            r"nicht\s+rate\w*"],
    # Die Klasse ist die VEREINIGUNG zweier Schnitte, und ihr Stammmuster ist es
    # auch. Sie hier noch einmal auszuschreiben hiesse, zwei Listen zu pflegen, die
    # dasselbe sagen - und eine Zahl, die man nicht zaehlt, ist erfunden.
    "injk3": STAMM_INJ + STAMM_K3,
    "halt": [r"\[HALT\]", r"anhalt\w*", r"h(ä|ae)lt\w*\s+an\b", r"Halte-?[Pp]unkt\w*",
             r"vor\s+dem\s+ersten\s+Schreibzugriff", r"setzt\s+nichts\s+um",
             r"behebt\s+nichts", r"f(ü|ue)hrt\s+nichts\s+aus", r"keine\s+Umsetzung",
             r"Planbest(ä|ae)tigung\w*", r"Freigabepunkt\w*",
             r"zur\s+Best(ä|ae)tigung\s+vor", r"Umsetzung\s+beginnt\s+erst",
             r"Folge-?Skill\w*"],
    # 🔴 ZWEIMAL EINGEENGT, UND BEIDE MALE AUS DEMSELBEN GRUND WIE BEI `plan`
    # (gemessen am 2026-09-19, CR-2026-104): Der erste Entwurf fuehrte fuer `konf`
    # ein blosses `vermute\w*` und fuer `risiko` ein blosses `Kontrollstufe\w*` -
    # 68 beziehungsweise 747 Meldungen. Beide trafen einen ANDEREN Sinn desselben
    # Wortes: "der vermutete Bereich" ist eine EINGABE von fw-change-analyze, und
    # die Kontrollstufe nennt jedes Ausgabeformat des Frameworks. Ein Stammmuster
    # ist weiter als das Schnittmuster, aber es sucht den GEGENSTAND.
    "konf": [r"Konfidenz\w*", r"Fundstelle\w*", r"erfund\w*", r"erfind\w*",
             r"Code-?Stand\w*", r"nicht\s+belegbar\w*",
             r"beobachtet\s*\(", r"geschlossen\s*\(",
             r"auf\s+Basis\s+vermutet\w*", r"ohne\s+Beleg\w*"],
    "risiko": [r"Risikofaktor\w*", r"Risiko-?Abgleich\w*", r"\bR1[013]\b",
               r"nicht\s+eigenm(ä|ae)chtig",
               r"Anstieg\s+der\s+Kontrollstufe",
               r"(h(ö|oe)her\w*|neue\w*)\s+Einstufung\w*",
               r"Kontrollstufe\s+\w*\s*(senken|(ä|ae)ndern|herabsetzen)",
               r"Einstufung\w*\s+(anheben|erh(ö|oe)hen|melden)"],
}

OHNE_STAMM = "--ohne-stammwaechter" in sys.argv

if KLASSE not in KLASSEN:
    raise SystemExit(" | ".join(sorted(KLASSEN)))
if KLASSE not in STAMM and not OHNE_STAMM:
    raise SystemExit(
        "ABBRUCH: fuer die Klasse %s ist kein Stammmuster hinterlegt (D-205).\n"
        "Der Waechter wuerde mit dem Schnittmuster pruefen und nichts finden.\n"
        "Entweder ein STAMM-Muster hinterlegen oder --ohne-stammwaechter setzen\n"
        "und die Abweichung ins Protokoll schreiben." % KLASSE)

K = KLASSEN[KLASSE]
ZEILE_RE = [re.compile(x, re.IGNORECASE) for x in K["ZEILE"]]
NUR_SATZ_RE = [re.compile(x, re.IGNORECASE) for x in K.get("NUR_SATZ", [])]
ABSCHNITT_RE = [re.compile(x, re.IGNORECASE) for x in K["ABSCHNITT"]]
MARKEN_RE = [re.compile(x, re.IGNORECASE) for x in K["MARKEN"]]
BEHALTEN = {x.replace("/", os.sep) for x in K.get("BEHALTEN", [])}


def dateien(wurzel):
    for teil in BEREICHE:
        p = os.path.join(wurzel, teil.replace("/", os.sep))
        if os.path.isfile(p):
            yield p
        elif os.path.isdir(p):
            for w, _, ds in os.walk(p):
                for d in ds:
                    if d.lower().endswith((".md", ".txt", ".template", ".yaml", ".yml")):
                        voll = os.path.join(w, d)
                        if os.path.relpath(voll, wurzel) in BEHALTEN:
                            continue
                        yield voll


def ebene(zeile):
    m = re.match(r"^(#+) ", zeile)
    return len(m.group(1)) if m else 0


def weg(pfad):
    def onexc(func, p, exc):
        os.chmod(p, 0o700)
        func(p)
    shutil.rmtree(pfad, onexc=onexc)


# --- Kopieren ---------------------------------------------------------------------
if os.path.exists(ZIEL):
    weg(ZIEL)
shutil.copytree(QUELLE, ZIEL)
print("kopiert nach", ZIEL)

weg_zeilen = weg_abschnitte = weg_saetze = 0
beruehrt = []

for pfad in dateien(ZIEL):
    roh = io.open(pfad, encoding="utf-8", newline="").read()
    crlf = "\r\n" in roh
    zeilen = roh.replace("\r\n", "\n").split("\n")

    neu = []
    i = 0
    n_z = n_a = n_s = 0
    while i < len(zeilen):
        z = zeilen[i]
        treffer_abschnitt = next((r for r in ABSCHNITT_RE if r.search(z)), None)
        if treffer_abschnitt is not None and ebene(z):
            e = ebene(z)
            i += 1
            while i < len(zeilen) and not (ebene(zeilen[i]) and ebene(zeilen[i]) <= e):
                i += 1
            n_a += 1
            continue
        # 🔴 NUR_SATZ GEHT VOR ZEILE. Eine Zeile, die Schranke UND
        # Meszgegenstand traegt, darf nicht als Ganzes fallen - aus ihr faellt
        # allein der schrankensetzende Satz (0.83.0, CR-2026-116).
        if any(r.search(z) for r in NUR_SATZ_RE):
            for s in K["SATZ"]:
                if s in z:
                    z = z.replace(s, "")
                    n_s += 1
            neu.append(z)
            i += 1
            continue
        if any(r.search(z) for r in ZEILE_RE):
            i += 1
            n_z += 1
            continue
        for s in K["SATZ"]:
            if s in z:
                z = z.replace(s, "")
                n_s += 1
        neu.append(z)
        i += 1

    if (n_z or n_a or n_s):
        text = "\n".join(neu)
        if crlf:
            text = text.replace("\n", "\r\n")
        daten = text.encode("utf-8")
        io.open(pfad, "wb").write(daten)
        weg_zeilen += n_z
        weg_abschnitte += n_a
        weg_saetze += n_s
        beruehrt.append((os.path.relpath(pfad, ZIEL), n_z, n_a, n_s))

print("entfernt: %d Zeilen, %d Abschnitte, %d Saetze in %d Traegern"
      % (weg_zeilen, weg_abschnitte, weg_saetze, len(beruehrt)))
for r, a, b, c in sorted(beruehrt, key=lambda x: -(x[1] + x[2]))[:15]:
    print("   %-72s Z%-3d A%-3d S%-3d" % (r, a, b, c))
if len(beruehrt) > 15:
    print("   ... und %d weitere Traeger" % (len(beruehrt) - 15))

# --- Der SessionStart-Hook, wo die Schranke ihn als zweiten Traeger hat ------------
if K.get("HOOK_WEG"):
    pfad = os.path.join(ZIEL, ".claude", "settings.json")
    d = json.loads(io.open(pfad, encoding="utf-8", newline="").read())
    if "SessionStart" not in d.get("hooks", {}):
        raise SystemExit("ABBRUCH: kein SessionStart-Hook zum Entfernen")
    del d["hooks"]["SessionStart"]
    daten = (json.dumps(d, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    io.open(pfad, "wb").write(daten)
    print("SessionStart-Hook entfernt - der zweite Traeger derselben Anweisung")

# --- Waechter ---------------------------------------------------------------------
for rel in BEHALTEN:
    if not os.path.isfile(os.path.join(ZIEL, rel)):
        weg(ZIEL)
        raise SystemExit("ABBRUCH: %s fehlt im Kontrollbaum - Baum geloescht" % rel)
    print("Waechter: %s unberuehrt" % rel.replace(os.sep, "/"))

rest = []
for pfad in dateien(ZIEL):
    text = io.open(pfad, encoding="utf-8", newline="").read()
    for r in MARKEN_RE:
        m = r.search(text)
        if m:
            rest.append((os.path.relpath(pfad, ZIEL), r.pattern, m.group(0)))
if rest:
    for r in rest[:40]:
        print("   REST:", r)
    weg(ZIEL)
    raise SystemExit("ABBRUCH: %d Restfundstellen - Baum geloescht" % len(rest))
print("Waechter 1 (Marken): keine Restfundstelle der %d Marken in den REGELQUELLEN"
      % len(MARKEN_RE))

# --- Waechter 2: der Stammwaechter (D-205) ----------------------------------------
# Er sucht den GEGENSTAND in allen Formen - und er ist WEITER als das Schnittmuster.
# Nur deshalb kann er etwas finden, was der Schnitt nicht kannte.
if KLASSE in STAMM:
    stamm_re = [(x, re.compile(x, re.IGNORECASE)) for x in STAMM[KLASSE]]
    rest2 = []
    for pfad in dateien(ZIEL):
        text = io.open(pfad, encoding="utf-8", newline="").read()
        for nr, z in enumerate(text.replace("\r\n", "\n").split("\n"), 1):
            treffer = [p for p, r in stamm_re if r.search(z)]
            if treffer:
                rest2.append((os.path.relpath(pfad, ZIEL), nr, "+".join(treffer),
                              z.strip()[:90]))
    if rest2:
        for r in rest2[:40]:
            print("   REST(Stamm) %s:%d  [%s]" % (r[0], r[1], r[2]))
            print("               %s" % r[3])
        if len(rest2) > 40:
            print("   ... und %d weitere" % (len(rest2) - 40))
        weg(ZIEL)
        raise SystemExit(
            "ABBRUCH: %d Restfundstellen des GEGENSTANDS - Baum geloescht.\n"
            "Der Zuschnitt ist unfertig. Wird er so gefahren, traegt die Zelle\n"
            "`nicht erhoben` mit Grund - nicht `nein` (D-205)." % len(rest2))
    print("Waechter 2 (Stamm): keine Restfundstelle des Gegenstands in %d Mustern"
          % len(stamm_re))
else:
    print("\U0001F534 WARNUNG: kein Stammwaechter fuer die Klasse %s (--ohne-stammwaechter).\n"
          "   Der Marken-Waechter prueft mit dem Schnittmuster und belegt nur den\n"
          "   Schnitt, nicht die Abwesenheit der Schranke. Diese Abweichung des\n"
          "   Zuschnitts gehoert ins Protokoll (D-205)." % KLASSE)

# --- Zaehlung in den Aufzeichnungen (kein Abbruchgrund, aber ein Messwert) ---------
auf = {}
for teil in AUFZEICHNUNGEN:
    p = os.path.join(ZIEL, teil.replace("/", os.sep))
    pfade = []
    if os.path.isfile(p):
        pfade = [p]
    elif os.path.isdir(p):
        for w, _, ds in os.walk(p):
            if "__pycache__" in w:
                continue
            pfade += [os.path.join(w, d) for d in ds
                      if d.lower().endswith((".md", ".txt", ".yaml", ".yml", ".template"))]
    for pf in pfade:
        text = io.open(pf, encoding="utf-8", errors="replace").read()
        n = sum(len(r.findall(text)) for r in MARKEN_RE)
        if n:
            auf[os.path.relpath(pf, ZIEL).replace(chr(92), "/")] = n
print("In den AUFZEICHNUNGEN stehen die Marken weiter: %d Fundstellen in %d Traegern"
      % (sum(auf.values()), len(auf)))
for k, v in sorted(auf.items(), key=lambda x: -x[1])[:6]:
    print("   %-72s %d" % (k, v))
print("   (Eine Aufzeichnung ist nach Regel 2.5 ein Datum, keine Anweisung - D-141.)")
print("OK")
