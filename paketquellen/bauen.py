#!/usr/bin/env python3
"""
bauen.py - Die Pakete der Paketquellen aus einem Release-Archiv bauen (CR-2026-168, D-520).

Hintergrund: Das Release-Archiv entsteht aus der signierten Marke (RELEASE_PROCESS.md 4.1,
Schritt 5) und traegt genau `git ls-tree` der Marke. Dieses Skript baut daraus - und aus
nichts anderem - vier Erzeugnisse, damit jede Paketquelle denselben Inhalt liefert:

    koolie-<V>-py3-none-any.whl   PyPI (pip, pipx, uv): der Baum unter koolie/baum/,
                                  der Befehl `koolie` als Einstiegspunkt
    koolie-<V>.tgz                npm: der Baum unter package/, der Befehl ueber
                                  paketquellen/npm/koolie.js, KEIN Installationsskript
    scoop/koolie.json             Scoop: laedt das Archiv von der Download-Adresse und
                                  prueft seine SHA-256
    homebrew/koolie.rb            Homebrew: ebenso

dazu SHA256SUMS ueber alle vier und das Archiv. Erzeugt wird nur, was sich aus Archiv und
Download-Adresse ableiten laesst: Metadaten, zwei Einstiegsdateien des Wheels, die
Manifeste. Die Version kommt aus .koolie/core/VERSION im Archiv - nie aus diesem Skript.

Die Erzeugnisse sind bytegleich wiederholbar (feste Zeitstempel, sortierte Eintraege,
feste Modi); bauen.py prueft nach dem Bau selbst nach: Dateimenge von Wheel und
npm-Paket = Dateimenge des Archivs, Version, Pruefsumme in beiden Manifesten, RECORD.

Veroeffentlicht wird hier NICHTS (D-521): Das ist ein eigener Schritt mit ausdruecklicher
Freigabe des Owners je Paketquelle.

Aufruf:

    python paketquellen/bauen.py --archiv <koolie-V.tar.gz> --aus <verzeichnis>
                                 [--url-basis <adresse>]

--url-basis ist die Adresse, unter der das Archiv liegt; Standard ist das GitHub-Release
der Marke. Fuer eine Messung ohne Veroeffentlichung darf es eine lokale Adresse sein.

Exit-Code: 0 ohne Befund, 1 mit Befund, 2 bei falschem Aufruf.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import io
import json
import os
import sys
import tarfile
import zipfile

REPO = "https://github.com/Renoxar/koolie"
ZEIT_ZIP = (1980, 1, 1, 0, 0, 0)
ZEIT_TAR = 315532800  # 1980-01-01, wie im Wheel
BESCHREIBUNG = ("Rules, skills and a protective hook for AI coding assistants - "
                "one rule source, installed per project.")
HINWEIS = ("Koolie {v} ist installiert. Ins Projekt kommt es mit dem Befehl 'koolie' "
           "im Projektverzeichnis (Dialog mit Banner) oder 'koolie --target <projekt>'.")

INIT_PY = '''"""Koolie aus dem Wheel (CR-2026-168). Der Baum des Releases liegt unter baum/."""
'''

MAIN_PY = '''"""Der Befehl koolie aus dem Wheel (CR-2026-168, D-520): startet
baum/paketquellen/koolie_befehl.py im mitgelieferten Baum."""
import os
import runpy
import sys

BEFEHL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "baum", "paketquellen",
                      "koolie_befehl.py")


def main():
    return runpy.run_path(BEFEHL, run_name="koolie_befehl")["main"]()


if __name__ == "__main__":
    sys.exit(main())
'''


class Befund(Exception):
    pass


# --- Archiv lesen -------------------------------------------------------------------
def archiv_lesen(pfad: str) -> tuple[str, str, dict]:
    """(Version, Praefix, {relativer Pfad: Bytes}) - nur Dateien, ohne Praefix."""
    dateien = {}
    with tarfile.open(pfad, "r:gz") as tf:
        mitglieder = [m for m in tf.getmembers() if m.isfile()]
        praefixe = {m.name.split("/", 1)[0] for m in mitglieder}
        if len(praefixe) != 1:
            raise Befund(f"Archiv ohne einheitliches Praefix: {sorted(praefixe)[:3]}")
        praefix = praefixe.pop()
        for m in mitglieder:
            dateien[m.name[len(praefix) + 1:]] = tf.extractfile(m).read()
    if ".koolie/core/VERSION" not in dateien:
        raise Befund("Archiv ohne .koolie/core/VERSION")
    version = dateien[".koolie/core/VERSION"].decode("utf-8").strip()
    if praefix != f"koolie-{version}":
        raise Befund(f"Praefix {praefix} passt nicht zu VERSION {version}")
    for pflicht in ("paketquellen/koolie_befehl.py", "paketquellen/koolie.cmd",
                    "paketquellen/npm/koolie.js", "LICENSE", "README.en.md"):
        if pflicht not in dateien:
            raise Befund(f"Archiv ohne {pflicht}")
    return version, praefix, dateien


def sha256(daten: bytes) -> str:
    return hashlib.sha256(daten).hexdigest()


# --- Wheel ---------------------------------------------------------------------------
def _record_hash(daten: bytes) -> str:
    return "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(daten).digest()).decode().rstrip("=")


def metadaten(version: str, dateien: dict) -> str:
    kopf = [
        "Metadata-Version: 2.1",
        "Name: koolie",
        f"Version: {version}",
        f"Summary: {BESCHREIBUNG}",
        "License: GPL-3.0-only",
        f"Project-URL: Repository, {REPO}",
        "Classifier: License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Classifier: Programming Language :: Python :: 3",
        "Classifier: Environment :: Console",
        "Requires-Python: >=3.8",
        "Description-Content-Type: text/markdown",
    ]
    text = dateien["README.en.md"].decode("utf-8").replace("\r\n", "\n")
    return "\n".join(kopf) + "\n\n" + text


def wheel_bauen(version: str, dateien: dict) -> tuple[str, bytes]:
    di = f"koolie-{version}.dist-info"
    inhalt = {"koolie/__init__.py": INIT_PY.encode(), "koolie/__main__.py": MAIN_PY.encode()}
    for rel, daten in dateien.items():
        inhalt["koolie/baum/" + rel] = daten
    inhalt[f"{di}/METADATA"] = metadaten(version, dateien).encode("utf-8")
    inhalt[f"{di}/WHEEL"] = (b"Wheel-Version: 1.0\nGenerator: koolie-bauen\n"
                             b"Root-Is-Purelib: true\nTag: py3-none-any\n")
    inhalt[f"{di}/entry_points.txt"] = b"[console_scripts]\nkoolie = koolie.__main__:main\n"
    inhalt[f"{di}/LICENSE"] = dateien["LICENSE"]
    zeilen = [f"{n},{_record_hash(d)},{len(d)}" for n, d in sorted(inhalt.items())]
    zeilen.append(f"{di}/RECORD,,")
    inhalt[f"{di}/RECORD"] = ("\n".join(zeilen) + "\n").encode()
    puffer = io.BytesIO()
    with zipfile.ZipFile(puffer, "w", zipfile.ZIP_DEFLATED) as zf:
        # dist-info zuletzt, RECORD als letzte Datei (PEP 427 empfiehlt es)
        namen = sorted(n for n in inhalt if not n.startswith(di)) + \
            sorted(n for n in inhalt if n.startswith(di) and not n.endswith("RECORD")) + \
            [f"{di}/RECORD"]
        for n in namen:
            zi = zipfile.ZipInfo(n, ZEIT_ZIP)
            zi.external_attr = (0o100644 << 16)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(zi, inhalt[n])
    return f"koolie-{version}-py3-none-any.whl", puffer.getvalue()


# --- npm -----------------------------------------------------------------------------
def package_json(version: str) -> bytes:
    daten = {
        "name": "koolie",
        "version": version,
        "description": BESCHREIBUNG,
        "license": "GPL-3.0-only",
        "homepage": REPO,
        "repository": {"type": "git", "url": f"git+{REPO}.git"},
        "bin": {"koolie": "paketquellen/npm/koolie.js"},
        "engines": {"node": ">=16"},
    }
    return (json.dumps(daten, indent=2, ensure_ascii=True) + "\n").encode()


def _tar_eintrag(tf: tarfile.TarFile, name: str, daten: bytes) -> None:
    ti = tarfile.TarInfo(name)
    ti.size, ti.mtime, ti.mode = len(daten), ZEIT_TAR, 0o644
    ti.uid = ti.gid = 0
    ti.uname = ti.gname = ""
    tf.addfile(ti, io.BytesIO(daten))


def npm_bauen(version: str, dateien: dict) -> tuple[str, bytes]:
    roh = io.BytesIO()
    with tarfile.open(fileobj=roh, mode="w", format=tarfile.PAX_FORMAT) as tf:
        _tar_eintrag(tf, "package/package.json", package_json(version))
        for rel in sorted(dateien):
            _tar_eintrag(tf, "package/" + rel, dateien[rel])
    gz = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=gz, mtime=0, compresslevel=9) as g:
        g.write(roh.getvalue())
    return f"koolie-{version}.tgz", gz.getvalue()


# --- Manifeste -----------------------------------------------------------------------
def scoop_bauen(version: str, url: str, hashwert: str) -> bytes:
    daten = {
        "version": version,
        "description": BESCHREIBUNG,
        "homepage": REPO,
        "license": "GPL-3.0-only",
        "suggest": {"Python 3.8+": "python"},
        "url": url,
        "hash": hashwert,
        "extract_dir": f"koolie-{version}",
        "bin": [["paketquellen\\koolie.cmd", "koolie"]],
        "notes": HINWEIS.format(v=version),
        "checkver": "github",
        "autoupdate": {
            "url": f"{REPO}/releases/download/v$version/koolie-$version.tar.gz",
            "extract_dir": "koolie-$version",
            "hash": {"url": "$url.sha256"},
        },
    }
    return (json.dumps(daten, indent=4, ensure_ascii=True) + "\n").encode()


def homebrew_bauen(version: str, url: str, hashwert: str) -> bytes:
    text = f'''# Koolie {version} - Formel fuer einen eigenen Tap (CR-2026-168, D-520).
# Erzeugt von paketquellen/bauen.py; nicht von Hand aendern.
class Koolie < Formula
  desc "{BESCHREIBUNG}"
  homepage "{REPO}"
  url "{url}"
  sha256 "{hashwert}"
  license "GPL-3.0-only"

  depends_on "python@3.13"

  def install
    libexec.install Dir["*"], ".koolie"
    (bin/"koolie").write <<~EOS
      #!/bin/sh
      exec "#{{Formula["python@3.13"].opt_bin}}/python3.13" "#{{libexec}}/paketquellen/koolie_befehl.py" "$@"
    EOS
  end

  def caveats
    "{HINWEIS.format(v=version)}"
  end

  test do
    assert_match "koolie #{{version}}", shell_output("#{{bin}}/koolie --version")
  end
end
'''
    return text.encode()


# --- Nachpruefen ---------------------------------------------------------------------
def nachpruefen(version: str, dateien: dict, whl: bytes, tgz: bytes,
                scoop: bytes, brew: bytes, hashwert: str) -> list:
    befunde = []
    soll = set(dateien)
    with zipfile.ZipFile(io.BytesIO(whl)) as zf:
        namen = zf.namelist()
        baum = {n[len("koolie/baum/"):] for n in namen if n.startswith("koolie/baum/")}
        if baum != soll:
            befunde.append(f"Wheel: {len(baum ^ soll)} Dateien weichen vom Archiv ab")
        di = f"koolie-{version}.dist-info/"
        record = zf.read(di + "RECORD").decode().splitlines()
        for zeile in record:
            name, h, groesse = zeile.rsplit(",", 2)
            if name == di + "RECORD":
                continue
            d = zf.read(name)
            if h != _record_hash(d) or int(groesse) != len(d):
                befunde.append(f"Wheel: RECORD stimmt nicht fuer {name}")
        if len(record) != len(namen):
            befunde.append("Wheel: RECORD zaehlt nicht jede Datei")
        if f"Version: {version}\n" not in zf.read(di + "METADATA").decode("utf-8"):
            befunde.append("Wheel: Version in METADATA")
    with tarfile.open(fileobj=io.BytesIO(tgz), mode="r:gz") as tf:
        namen = {m.name[len("package/"):] for m in tf.getmembers() if m.isfile()}
        pj = json.loads(tf.extractfile("package/package.json").read())
    if namen - {"package.json"} != soll:
        befunde.append("npm: Dateimenge weicht vom Archiv ab")
    if pj.get("version") != version or "scripts" in pj:
        befunde.append("npm: Version oder Installationsskript in package.json")
    if pj["bin"]["koolie"] not in soll:
        befunde.append("npm: bin zeigt auf keine Datei des Baums")
    sc = json.loads(scoop)
    if sc["hash"] != hashwert or sc["version"] != version:
        befunde.append("Scoop: Hash oder Version")
    if sc["bin"][0][0].replace("\\", "/") not in soll:
        befunde.append("Scoop: bin zeigt auf keine Datei des Baums")
    if f'sha256 "{hashwert}"' not in brew.decode():
        befunde.append("Homebrew: Hash")
    return befunde


def main(argv: list | None = None) -> int:
    ap = argparse.ArgumentParser(description="Pakete der Paketquellen aus einem Release-Archiv bauen.")
    ap.add_argument("--archiv", required=True)
    ap.add_argument("--aus", required=True)
    ap.add_argument("--url-basis", default=None,
                    help="Adresse des Archivs ohne Dateinamen (Standard: GitHub-Release der Marke)")
    a = ap.parse_args(argv)
    try:
        version, praefix, dateien = archiv_lesen(a.archiv)
    except (Befund, OSError, tarfile.TarError) as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 1
    with open(a.archiv, "rb") as fh:
        archivdaten = fh.read()
    hashwert = sha256(archivdaten)
    basis = (a.url_basis or f"{REPO}/releases/download/v{version}").rstrip("/")
    url = f"{basis}/{praefix}.tar.gz"

    whl_name, whl = wheel_bauen(version, dateien)
    tgz_name, tgz = npm_bauen(version, dateien)
    scoop = scoop_bauen(version, url, hashwert)
    brew = homebrew_bauen(version, url, hashwert)
    befunde = nachpruefen(version, dateien, whl, tgz, scoop, brew, hashwert)
    # bytegleich wiederholbar - ein zweiter Bau muss dieselben Bytes liefern
    if (wheel_bauen(version, dateien)[1], npm_bauen(version, dateien)[1]) != (whl, tgz):
        befunde.append("zweiter Bau nicht bytegleich")

    os.makedirs(os.path.join(a.aus, "scoop"), exist_ok=True)
    os.makedirs(os.path.join(a.aus, "homebrew"), exist_ok=True)
    erzeugt = {whl_name: whl, tgz_name: tgz, "scoop/koolie.json": scoop,
               "homebrew/koolie.rb": brew}
    for rel, daten in erzeugt.items():
        with open(os.path.join(a.aus, rel), "wb") as fh:
            fh.write(daten)
    summen = {os.path.basename(a.archiv): hashwert}
    summen.update({rel: sha256(d) for rel, d in erzeugt.items()})
    with open(os.path.join(a.aus, "SHA256SUMS"), "w", encoding="utf-8", newline="\n") as fh:
        for rel in sorted(summen):
            fh.write(f"{summen[rel]}  {rel}\n")

    print(f"Koolie {version}: {len(dateien)} Dateien aus {os.path.basename(a.archiv)} "
          f"(SHA-256 {hashwert[:8]}...{hashwert[-8:]})")
    for rel, daten in erzeugt.items():
        print(f"  {rel:34} {len(daten):>10} Bytes")
    print(f"  Download-Adresse: {url}")
    if befunde:
        print("BEFUNDE:", *befunde, sep="\n  ")
        return 1
    print("Nachpruefung ohne Befund (Wheel, npm, Scoop, Homebrew; zweimal bytegleich)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
