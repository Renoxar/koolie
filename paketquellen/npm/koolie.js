#!/usr/bin/env node
// Koolie - der Befehl koolie aus dem npm-Paket (CR-2026-168, D-520).
//
// Koolie ist Python; dieses Skript sucht ein Python ab 3.8 und reicht alle Argumente an
// paketquellen/koolie_befehl.py weiter. stdio wird geerbt: Das Banner sieht dasselbe
// Terminal wie der Nutzer (gemessen 2026-09-30: npx/bin mit Terminal, postinstall ohne).
// Bewusst KEIN Installationsskript im Paket (D-519).
"use strict";
const { spawnSync } = require("child_process");
const path = require("path");

const befehl = path.join(__dirname, "..", "koolie_befehl.py");
const kandidaten = process.platform === "win32"
  ? [["py", ["-3"]], ["python3", []], ["python", []]]
  : [["python3", []], ["python", []]];
const probe = "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)";

for (const [exe, vorab] of kandidaten) {
  const p = spawnSync(exe, [...vorab, "-c", probe], { stdio: "ignore" });
  if (p.status === 0) {
    const lauf = spawnSync(exe, [...vorab, befehl, ...process.argv.slice(2)], { stdio: "inherit" });
    process.exit(lauf.status === null ? 1 : lauf.status);
  }
}
console.error("Koolie braucht Python 3.8 oder neuer - gefunden wurde keines.");
process.exit(9009);
