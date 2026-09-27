#!/usr/bin/env python3
"""
Gemeinsame Auswertung des Overlay-Status - fuer Validator und Status-Hook.

Status: entwurf.

Warum dieses Modul existiert: Der Status stand in zwei Werkzeugen und wurde zweimal
verschieden ausgewertet. Der Validator vergleicht seit 0.28.0 **exakt** auf 'aktiv', weil
ein Praefixvergleich den Wert 'aktivierung-ausstehend' als Aktivierung durchliess (B02,
D-44) - ein Wert, der woertlich sagt, dass die Aktivierung aussteht. Der Hook prueft
weiterhin als Praefix, kennt die Steckbriefzeile nicht und nimmt die erste Datei mit
Treffer. Die Lehre war gezogen, aber nur in einer der beiden Funktionen; dasselbe Muster
wie bei D-49.

Der Hook importiert dieses Modul, **nicht** den Validator: Ein Hook, der bei jedem
Sitzungsstart ein 2300-Zeilen-Skript laedt, waere ein Leistungs- und ein Fehlerrisiko, und
er wuerde dessen Abhaengigkeiten mitschleppen. Dieses Modul hat keine Abhaengigkeit ausser
're'.

WAS DIESES MODUL NICHT LEISTET: Es liest Erklaerungen, es prueft keine Wirkung. Dass ein
Overlay 'aktiv' erklaert, heisst nicht, dass der Client seine Regeln laedt - das ist
Gegenstand der Fachmatrix des jeweiligen Client Packs, nicht einer Textauswertung.
"""
from __future__ import annotations

import re

# Die beiden Schreibweisen, in denen eine Overlay-Datei ihren Status *erklaert*: als Zeile
# im Steckbrief (Tabelle) und als Aussage im Aktivierungsabschnitt (Liste). Beide nur am
# Zeilenanfang - eine Erwaehnung im Fliesstext oder in einem Ausnahmeregister ist keine
# Erklaerung. Der Hook suchte bisher ohne Anker und ohne die Tabellenform; damit traf er
# die Steckbriefzeile nie, weil dort kein Doppelpunkt steht.
_TABELLE_RE = re.compile(r"^\|\s*Overlay-Status\s*\|\s*`?([^`|]+)", re.M)
_LISTE_RE = re.compile(r"^-?\s*Overlay-Status:\s*`?([^`\n]+)", re.M)
# Die Version, in denselben zwei Formen wie der Validator sie liest (Pruefung 13). Seit
# 1.17.0 meldet der SessionStart-Hook einen Widerspruch sofort (CR-2026-156, D-452):
# Im ersten Projekteinsatz stand an der Stelle der Version eine Zeile des
# Aenderungsverlaufs, und die Statusmeldung der Sitzung sagte "aktiv" - der Schaden blieb
# unsichtbar, bis jemand den Validator startete (Befund A3).
_VERSION_TABELLE_RE = re.compile(r"^\|\s*Overlay-Version\s*\|\s*`?([^`|]+)", re.M)
_VERSION_LISTE_RE = re.compile(r"^-?\s*Overlay-Version:\s*`?([^`\n·]+)", re.M)
_SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")

# Zulaessige Statuswerte. Alles andere ist 'unbekannt' - auch ein nicht ausgefuellter
# Platzhalter, und das ist der haeufigste Fall in einer frischen Installation.
AKTIV = "aktiv"
INAKTIV = "inaktiv"
UNBEKANNT = "unbekannt"
# ASCII-Umschrift wie im uebrigen Skripttext: Der Wert erscheint in der Hook-Meldung, und
# die Nachbarsaetze dort sind ebenso geschrieben.
WIDERSPRUECHLICH = "widerspruechlich"


def status_angaben(text: str) -> list[str]:
    """Alle Stellen, an denen ein Text den Overlay-Status erklaert - in Lesereihenfolge."""
    werte = []
    for regex in (_TABELLE_RE, _LISTE_RE):
        for m in regex.finditer(text):
            werte.append(m.group(1).strip())
    return werte


def version_angaben(text: str) -> list[str]:
    """Alle Stellen, an denen ein Text die Overlay-Version erklaert."""
    werte = []
    for regex in (_VERSION_TABELLE_RE, _VERSION_LISTE_RE):
        for m in regex.finditer(text):
            werte.append(m.group(1).strip())
    return werte


def versionen_auswerten(angaben: list[str]) -> str:
    """Leerer Text, wenn die Versionsangaben uebereinstimmen - sonst der Befund.

    Ein offener Platzhalter (<TBD: ...>) ist kein Befund: Er ist der Stand vor dem
    Ausfuellen und Sache der Aktivierungspruefung.
    """
    werte = [a for a in angaben if not a.startswith("<")]
    if not werte:
        return ""
    ungueltig = [w for w in werte if not _SEMVER_RE.match(w)]
    if ungueltig:
        return "keine Version der Form x.y.z: '%s'" % ungueltig[0][:60]
    if len(set(werte)) > 1:
        return "die Versionsangaben widersprechen sich: " + ", ".join(sorted(set(werte)))
    return ""


def normalisieren(wert: str) -> str:
    """Ein einzelner erklaerter Wert, auf einen der vier Statuswerte abgebildet.

    Exakter Vergleich, kein Praefix: 'aktivierung-ausstehend' ist keine Aktivierung
    (D-44). Auszeichnungen und Anfuehrungszeichen fallen weg, der Wortlaut nicht.
    """
    w = wert.strip().strip("`*_ ").strip().lower()
    if w == AKTIV:
        return AKTIV
    if w == INAKTIV:
        return INAKTIV
    return UNBEKANNT


def auswerten(angaben: list[str]) -> tuple[str, str]:
    """Gesamtstatus aus allen Erklaerungen. Rueckgabe: (status, begruendung).

    Regeln, und jede hat einen Befund hinter sich:

    * **Keine Erklaerung** -> 'unbekannt'. Eine fehlende Angabe ist keine Inaktivitaet;
      sie ist eine unvollstaendige Konfiguration, und der Unterschied gehoert in die
      Meldung.
    * **Widerspruch** -> 'widersprüchlich', nicht 'inaktiv' und nicht 'unbekannt'. Beide
      wuerden verschweigen, dass eine Erklaerung da ist und nicht stimmt; wer die Meldung
      liest, suchte dann einen fehlenden Eintrag und faende einen widerspruechlichen
      (B08). Die Folge ist dieselbe wie bei 'inaktiv' - nur lesend -, der Grund nicht.
    * **Ein unbekannter Wert neben einem bekannten** ist ebenfalls ein Widerspruch: Eine
      Datei mit ausgefuelltem Status und eine mit offenem Platzhalter erklaeren nicht
      dasselbe.
    """
    if not angaben:
        return UNBEKANNT, "keine Angabe zum Overlay-Status gefunden"
    werte = [normalisieren(a) for a in angaben]
    eindeutig = set(werte)
    if len(eindeutig) > 1:
        return (WIDERSPRUECHLICH,
                "die Statusangaben widersprechen sich: "
                + ", ".join("'%s'" % a.strip() for a in angaben))
    status = werte[0]
    if status == UNBEKANNT:
        return UNBEKANNT, "Statuswert nicht ausgefuellt oder unbekannt: '%s'" % angaben[0].strip()
    return status, "%d Angabe(n), alle '%s'" % (len(angaben), status)
