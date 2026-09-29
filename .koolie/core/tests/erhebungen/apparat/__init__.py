# -*- coding: utf-8 -*-
"""Der Messapparat als Paket (CR-2026-160, D-473, K-174).

Bis 1.18.2 entstand je Release eine Handvoll kopierter Skripte in der Erhebungsablage -
67 Stueck in elf Ablagen, ohne einen einzigen Test (D-436). Dieses Paket ersetzt sie fuer
jede NEUE Reihe:

  * reihe.py        die Reihe als DATEN (eine JSON-Datei in der Erhebungsablage) - Laeufe,
                    Prompts, Erwartungen, Client, Modell, Gruppe, Kontingent
  * baum.py         Messbaum: bauen, herrichten, auf den Sollstand zuruecksetzen, Baum-Hash
  * vorpruefung.py  deterministisch VOR jedem bezahlten Lauf - Abbruch statt Lauf
  * kontingent.py   ein Buch je Lauf, die Summe wird gerechnet (Falle 8 aus 1.17.0)
  * clients.py      je Client ein Adapter; was nicht erhoben ist, sagt es
  * belege.py       sichern und auswerten
  * stand.py        die Standmarke einer Ergebniszelle (Pruefung 103, K-61)
  * selbsttest.py   der Apparat gegen einen Attrappen-Client - ohne Kontingent

Aufruf: python tests/erhebungen/messen.py REIHE.json BEFEHL (siehe messen.py).

Die Skripte der Buendel 4 und 5 bleiben liegen: Sie sind Beleg vergangener Protokolle und
bauen weiterhin deren Messbaeume; eine neue Reihe faehrt mit diesem Paket (D-473).
"""
