#!/usr/bin/env python3
"""
Framework-Hook: PreToolUse-Prüfung auf Secrets und geschützte Pfade.

Status: entwurf (Belegstatus des Hook-Mechanismus: [DOK]; Eingabeschema des Hooks:
<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>). Das Skript ist bewusst schema-agnostisch:
Es durchsucht alle Zeichenketten der über stdin gelieferten JSON-Struktur.

Verhalten:
- Fund eines Secret-Musters oder eines geschützten Pfads in der Werkzeugeingabe
  -> Ausgabe {"decision": "block", "reason": "..."} und Exit-Code 2 (blockiert laut Dokumentation).
- Schreibende Werkzeuge zusätzlich: jeder Pfad im Kernverzeichnis. Ausführende Werkzeuge
  sind davon ausgenommen, damit die Skripte des Kerns (Validator, install.py --check)
  weiterhin aufrufbar bleiben; dort greift die deny-Regel der Berechtigungsdatei.
- Kein Fund -> Exit-Code 0.
- Nicht parsebare Eingabe -> standardmäßig Exit-Code 0 mit Warnung auf stderr (fail-open),
  weil das Eingabeschema noch nicht in einer Zielinstallation validiert wurde.
  Mit Umgebungsvariable FW_HOOK_FAIL_CLOSED=1 wird stattdessen blockiert (fail-closed).
  Nach erfolgreicher Validierung im Arbeitspaket "Validierung der Clientfunktionalitäten"
  SOLL fail-closed zum Standard gemacht werden (Secure by Default).

Das Skript gibt gefundene Secrets niemals aus; es nennt nur die Musterkategorie.
Alle Muster sind generisch; sie enthalten keine realen Werte.
"""
import json
import os
import re
import sys

SECRET_PATTERNS = [
    ("privater Schluessel", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("Bearer-Token", re.compile(r"\bBearer\s+[A-Za-z0-9\-_\.=]{20,}", re.I)),
    ("Zugangsdaten-Zuweisung", re.compile(r"(?i)\b(password|passwd|pwd|secret|api[_-]?key|access[_-]?key|token)\b\s*[:=]\s*['\"]?[^\s'\"]{8,}")),
    ("Verbindungszeichenfolge mit Anmeldedaten", re.compile(r"(?i)\b[a-z][a-z0-9+\-.]*://[^/\s:]+:[^@\s]+@")),
    ("Cloud-Zugangsschluessel (generisches Muster)", re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
]

PROTECTED_PATH_PATTERNS = [
    re.compile(r"(^|[\\/])\.env(\.|$)"),
    re.compile(r"\.(pem|key|p12|pfx|jks|keystore)$", re.I),
    re.compile(r"(^|[\\/])id_(rsa|ed25519|ecdsa)"),
    re.compile(r"(^|[\\/])secrets?[\\/]", re.I),
    # Wurzel-Anweisungsdatei und Laufzeitschicht heissen je nach Client anders. Bewusst
    # beide Formen: Das Skript wird von allen Client Packs geteilt, und ein zusaetzlich
    # geschuetzter Pfad ist eine Verschaerfung, keine Lockerung.
    re.compile(r"(^|[\\/])(AGENTS|CLAUDE)\.md$"),
    re.compile(r"(^|[\\/])\.(devin|claude)[\\/]"),
    re.compile(r"(^|[\\/])project-overlay[\\/]"),
    re.compile(r"(^|[\\/])framework[\\/]core[\\/]"),
]

# Das Kernverzeichnis als Ganzes. Es steht bewusst in einer zweiten Liste: Die Muster
# oben gelten auch fuer 'exec', und ein Befehl, der lediglich einen Kernpfad nennt -
# der Validator, install.py --check, ein git diff - muss weiterhin laufen koennen. Fuer
# schreibende Werkzeuge gilt das Verbot vollstaendig; bei exec traegt die deny-Regel der
# Berechtigungsdatei. Die Liste ist damit rein additiv: Sie verschaerft, ohne eine
# bisher blockierte Operation freizugeben.
#
# Der Name des Kernverzeichnisses ist keine Eigenschaft eines Clients, sondern dieser
# Installation (<CORE_DIR>, docs/PLACEHOLDER_REGISTRY.md). Dieses Skript liegt unter
# <CORE_DIR>/tests/scripts/ und leitet ihn deshalb aus dem eigenen Ort ab, statt ihn
# festzuschreiben - eine Umbenennung des Kerns erreicht den Hook damit von selbst.
CORE_DIR_NAME = os.path.basename(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

WRITE_TOOLS = ("edit", "write", "notebookedit")

PROTECTED_WRITE_PATH_PATTERNS = [
    re.compile(r"(^|[\\/])" + re.escape(CORE_DIR_NAME) + r"[\\/]"),
]

# Zusätzliche projektspezifische Muster können über die Umgebungsvariable
# FW_HOOK_EXTRA_PATH_PATTERNS (durch ';' getrennte reguläre Ausdrücke) ergänzt werden.
for extra in filter(None, os.environ.get("FW_HOOK_EXTRA_PATH_PATTERNS", "").split(";")):
    try:
        PROTECTED_PATH_PATTERNS.append(re.compile(extra))
    except re.error:
        print(f"[fw-hook] Ungueltiges Zusatzmuster ignoriert: {extra!r}", file=sys.stderr)


def iter_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from iter_strings(k)
            yield from iter_strings(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from iter_strings(v)


def block(reason: str) -> None:
    print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
    sys.exit(2)


def main() -> None:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        msg = "[fw-hook] Eingabe nicht als JSON lesbar; Schema gegen aktuelle Clientdokumentation pruefen."
        if os.environ.get("FW_HOOK_FAIL_CLOSED") == "1":
            block(msg)
        print(msg, file=sys.stderr)
        sys.exit(0)

    tool_name = str(payload.get("tool_name", "")).lower() if isinstance(payload, dict) else ""
    strings = list(iter_strings(payload))

    for label, pattern in SECRET_PATTERNS:
        if any(pattern.search(s) for s in strings):
            block(f"Framework-Regel: Werkzeugeingabe enthaelt ein Muster der Kategorie '{label}'. "
                  f"Secrets duerfen nicht verarbeitet werden. Fundstelle melden, Sitzung anhalten "
                  f"(leitwerk-core/framework/core/02-privacy.md, Abschnitt 5).")

    # Schreib- und Ausfuehrungsoperationen auf geschuetzte Pfade blockieren. WRITE_TOOLS
    # steht auch hier, damit kein schreibendes Werkzeug an dieser Liste vorbeilaeuft -
    # 'notebookedit' tat das bisher.
    if tool_name in WRITE_TOOLS + ("exec",) or not tool_name:
        for s in strings:
            for pattern in PROTECTED_PATH_PATTERNS:
                if pattern.search(s):
                    block("Framework-Regel: Operation betrifft einen geschuetzten Pfad "
                          "(Secrets, Wurzel-Anweisungsdatei, Laufzeitschicht, project-overlay/, framework/core/). "
                          "Aenderungen daran erfolgen nur ueber den Aenderungsprozess "
                          "(leitwerk-core/governance/CHANGE_REQUEST_TEMPLATE.md).")

    # Schreiboperationen zusaetzlich auf das gesamte Kernverzeichnis blockieren. Das
    # Kernverzeichnis gehoert dem Framework Owner und wird ausschliesslich ueber ein
    # Release ausgetauscht - auch die Skripte darin, die genau diese Zusagen durchsetzen.
    if tool_name in WRITE_TOOLS:
        for s in strings:
            for pattern in PROTECTED_WRITE_PATH_PATTERNS:
                if pattern.search(s):
                    block(f"Framework-Regel: Schreiboperation betrifft das Kernverzeichnis "
                          f"({CORE_DIR_NAME}/). Es gehoert dem Framework Owner und wird nur "
                          f"ueber ein Release ausgetauscht; Aenderungen laufen als "
                          f"Aenderungsantrag ({CORE_DIR_NAME}/governance/CHANGE_REQUEST_TEMPLATE.md).")
    sys.exit(0)


if __name__ == "__main__":
    main()
