#!/usr/bin/env python3
"""
Framework-Hook: SessionStart - Overlay-Status als Zusatzkontext melden.

Status: entwurf. Hook-Mechanismus [DOK]; Ausgabeschema "hookSpecificOutput.additionalContext"
laut Dokumentation [DOK]. Was die Nutzlast im einzelnen traegt, ist nicht
dokumentiert - dieselbe benannte Grenze wie bei Zeile R5 der Faehigkeitsmatrix.

Aufruf:

    hook-overlay-status.py <projektverzeichnis> <regelablage>

Beide Werte kommen aus der Semantikabbildung des Client Packs: das Projektverzeichnis aus
hook_project_dir_var, die Regelablage aus runtime_placeholders["<RULES_DIR>"]. Der Kern
nennt weder die eine Variable noch den einen Pfad - er ist werkzeugneutral (D-02, D-30).

Warum als Argumente und nicht ueber die Umgebung: Der Wert steht damit in dem Kommando,
das der Client ohnehin ausfuehrt. Ob ein Client Umgebungsvariablen an den Hook-Prozess
weiterreicht, ist fuer kein Pack belegt - dieselbe Begruendung, aus der D-31 den Schalter
--fail-closed ins Kommando gelegt hat.

Ohne Argumente bleibt ein Notweg: das Arbeitsverzeichnis und ausschliesslich
.koolie/project-overlay/OVERLAY.md. Der Notweg ist nicht der vorgesehene Pfad. Ob das
Arbeitsverzeichnis beim Sitzungsstart das Projektverzeichnis ist, ist unbelegt, und ohne
Regelablage entfaellt der zweite Kandidat - die gerenderte Overlay-Regeldatei traegt den
Status ebenso wie das Overlay selbst.

Seit 0.33.0 wertet dieser Hook **alle** lesbaren Traeger aus, nicht den ersten mit Treffer,
und er benutzt dafuer dieselbe Funktion wie der Validator (overlay_status.py). Vorher
hatte er drei Defekte, alle drei gemessen (B08): Er verglich als Praefix - 'aktivierung-
ausstehend' galt damit als aktiv, genau der Wert, den D-44 im Validator ausgeschlossen hat;
sein Suchmuster verlangte einen Doppelpunkt und traf damit die Steckbriefzeile
'| Overlay-Status | ... |' nie; und er brach beim ersten Treffer ab, sodass eine aktive
Laufzeitregel gegen ein inaktives Quell-Overlay gewann. Ein Widerspruch wird jetzt als
solcher gemeldet, nicht als 'inaktiv' - die Folge ist dieselbe, der Grund nicht.

Das Skript blockiert nie; es informiert.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from overlay_status import (AKTIV, auswerten, status_angaben,  # noqa: E402
                            version_angaben, versionen_auswerten)

argumente = [a for a in sys.argv[1:] if not a.startswith("-")]
root = argumente[0] if argumente else os.getcwd()
regelablage = argumente[1] if len(argumente) > 1 else None

candidates = []
if regelablage:
    # Die Laufzeitregel heisst bei cursor 20-project-overlay.mdc (CR-2026-155): Der
    # Client laedt nur diese Endung. Das Skript kennt kein Manifest und nimmt die
    # Datei, die in der Regelablage liegt.
    for endung in (".md", ".mdc"):
        kandidat = os.path.join(root, *regelablage.replace("\\", "/").split("/"),
                                "20-project-overlay" + endung)
        if os.path.exists(kandidat) or endung == ".md":
            candidates.append(kandidat)
candidates.append(os.path.join(root, ".koolie/project-overlay", "OVERLAY.md"))

# Alle lesbaren Traeger, nicht der erste mit Treffer: Zwei Dateien, die verschiedene
# Staende erklaeren, sind der Befund - nicht eine Fundstelle, die man auswaehlt.
angaben = []
versionen = []
gelesen = []
for path in candidates:
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        continue
    gelesen.append(os.path.relpath(path, root).replace(os.sep, "/"))
    angaben.extend(status_angaben(text))
    versionen.extend(version_angaben(text))

status, begruendung = auswerten(angaben)

version = "unbekannt"
try:
    with open(os.path.join(root, ".koolie/core", "VERSION"), encoding="utf-8") as fh:
        version = fh.read().strip()
except OSError:
    pass

herkunft = ("gelesen: " + ", ".join(gelesen)) if gelesen else "keine Overlay-Datei lesbar"
context = (
    f"Framework-Statusmeldung: Framework-Version {version}; "
    f"Project-Overlay-Status: {status} ({begruendung}; {herkunft}). "
    + ("" if status == AKTIV else
       "Da das Overlay nicht als aktiv erklaert ist, arbeite ausschliesslich im Modus M1 "
       "Read-only Analysis und weise die Nutzerin oder den Nutzer darauf hin "
       "(Wurzel-Anweisungsdatei, Abschnitt 3) - ausgenommen M6 mit Mandat, um das "
       "Overlay einzurichten (Skill fw-overlay-pflege).")
)

# Seit 1.17.0 (CR-2026-156, D-452): der Versionswiderspruch und das Mandat. Beide nennen,
# was zu tun ist - der Blockade-Hinweis gilt auch fuer eine Meldung, die nichts sperrt.
befund_version = versionen_auswerten(versionen)
if befund_version:
    context += (" Overlay-Version: " + befund_version + ". Weise darauf hin und nenne den "
                "Weg: den Wert im Steckbrief von OVERLAY.md berichtigen (M6) und danach "
                "'python .koolie/core/mandat.py abgleichen' im eigenen Terminal.")
try:
    sys.path.insert(0, os.path.join(root, ".koolie", "core"))
    import mandat  # noqa: E402
    if os.path.normcase(mandat.PROJEKTWURZEL) == os.path.normcase(os.path.realpath(root)):
        aktiv = mandat.gueltiges_mandat()
        if aktiv:
            context += (" Mandat fuer M6 aktiv: Rolle %s, Umfang %s, noch %d Minuten - du "
                        "darfst Entscheidungen des Menschen in diesen Teil des Overlays "
                        "eintragen." % (aktiv["rolle"], ", ".join(aktiv["umfang"]),
                                        aktiv["_rest_min"]))
except Exception:  # noqa: BLE001 - der Hook informiert nur und darf nie scheitern
    pass

print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                         "additionalContext": context}}, ensure_ascii=False))
sys.exit(0)
