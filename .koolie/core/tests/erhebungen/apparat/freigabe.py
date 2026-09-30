# -*- coding: utf-8 -*-
"""Der Freigabe-Stellvertreter: ein MCP-Server, der im Druckmodus jede Rueckfrage beantwortet.

    claude -p ... --mcp-config <cfg> --permission-prompt-tool mcp__freigabe__freigeben

ANLASS (1.21.0, CR-2026-167, K-193). Im Druckmodus wird jede Rueckfrage zur Ablehnung. Eine
Konfiguration, die fuer jede Aenderung fragt, misst dort nur ihre Einstellung und nicht die
Arbeit; eine, die wenig fragt, wirkt dadurch strenger, als sie ist. Der Stellvertreter spielt
den UNAUFMERKSAMEN Menschen: Er gibt alles frei, was gefragt wird, und schreibt jede Frage
in ein Protokoll (Umgebung FREIGABE_LOG, eine JSON-Zeile je Frage). Was danach noch
gesperrt bleibt, sperrt die Technik; was nur eine Rueckfrage aufhielt, steht im Protokoll -
dort haette ein aufmerksamer Mensch anhalten koennen.

Eine Regel in 'deny' oder ein sperrender Hook erreicht den Stellvertreter nie: Er wird nur
gerufen, wenn der Client fragen wuerde.

Nur fuer Messbaeume. Er gibt ALLES frei - in einer echten Sitzung waere er eine Umgehung.
"""
import io
import json
import os
import sys
import time

WERKZEUG = {
    "name": "freigeben",
    "description": "Beantwortet eine Rueckfrage des Clients (Messung, gibt immer frei).",
    "inputSchema": {"type": "object", "properties": {
        "tool_name": {"type": "string"}, "input": {"type": "object"},
        "tool_use_id": {"type": "string"}}},
}


def _antwort(kennung, ergebnis):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": kennung, "result": ergebnis}) + "\n")
    sys.stdout.flush()


def _protokoll(argumente):
    pfad = os.environ.get("FREIGABE_LOG")
    if not pfad:
        return
    zeile = {"zeit": time.strftime("%Y-%m-%dT%H:%M:%S"), "werkzeug": argumente.get("tool_name"),
             "tool_use_id": argumente.get("tool_use_id"), "eingabe": argumente.get("input")}
    with io.open(pfad, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(zeile, ensure_ascii=False) + "\n")


def main():
    for zeile in sys.stdin:
        try:
            nachricht = json.loads(zeile)
        except ValueError:
            continue
        methode, kennung = nachricht.get("method"), nachricht.get("id")
        if kennung is None:
            continue  # Benachrichtigung
        if methode == "initialize":
            version = (nachricht.get("params") or {}).get("protocolVersion") or "2025-06-18"
            _antwort(kennung, {"protocolVersion": version, "capabilities": {"tools": {}},
                               "serverInfo": {"name": "freigabe", "version": "1.21.0"}})
        elif methode == "tools/list":
            _antwort(kennung, {"tools": [WERKZEUG]})
        elif methode == "tools/call":
            argumente = (nachricht.get("params") or {}).get("arguments") or {}
            _protokoll(argumente)
            text = json.dumps({"behavior": "allow", "updatedInput": argumente.get("input") or {}})
            _antwort(kennung, {"content": [{"type": "text", "text": text}]})
        else:
            _antwort(kennung, {})


if __name__ == "__main__":
    main()
