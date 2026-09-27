# Protokoll: Die Messung zu `1.17.0` – das Mandat und die Reibung des ersten Projekteinsatzes

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-27 |
| Release | `1.17.0` (`CR-2026-156`, D-445 bis D-455) |
| Gegenstand | Die Zellen von `fw-plan` 0.1.7, `fw-change-analyze` 0.1.5 und `fw-bugfix-prepare` 0.1.6 (Anweisung berührt, D-303), die neue Zelle `SK-003-P03` und die sechs Zellen von `fw-overlay-pflege` 0.1.1 – 24 Zellen |
| Client Pack | `claude-code`, Claude Code 2.1.283, Modell claude-opus-5-5 – **kein anderes Pack gemessen** (D-117) |
| Messort | Übungsrepositorium, Messstände `580b2cc`, `6c229a7`, `1a3a307`; Bäume `C:\lw-1170`, `C:\lw-1170b`, `C:\lw-1170c` außerhalb des Benutzerprofils |
| Kosten | 40 Sitzungsläufe, 27,33 USD nach Listenpreis; davon 10 verworfen (6,56 USD) |

## 1. Aufbau

Messbäume aus `git archive` des Übungsrepositoriums, Packwechsel auf `claude-code`, `install.py`, Füllschritt, Aufzeichnungsschnitt (D-425) – Skripte `aufbau-1170.py` und `reihe-1170.py` in der Erhebungsablage außerhalb des Repositoriums. Basis `b12` für die lesenden Skills; Basis `b13` für `fw-overlay-pflege` mit `Edit`/`Write(.koolie/project-overlay/**)` im `allow`-Korb, ohne die Rückfrage auf `Edit(**)` und mit dem Validator nach dem Schnitt. Das **Mandat** setzte das Messgerüst unmittelbar vor jeder Kette (`.git/koolie-mandat.json`, 60 Minuten, Umfang `overlay`) – der Handgriff, den im Projekt der Mensch im eigenen Terminal tut –, außer für `SK-013-N01`. **Kein Kontrolllauf:** Die Änderung an den drei bestehenden Skills berührt Trigger und K3-Zeile; ihre Zurechenbarkeit aus den Bündeln 1 und 2 und aus `1.14.x` gilt fort. Für `fw-overlay-pflege` ist sie nicht erhoben.

## 2. Befunde, die den Aufbau oder den Kern geändert haben

| # | Befund | Folge |
|---|---|---|
| 1 | 🔴 **Der Hook sperrte die Auskunft `mandat.py status`**: claude-code schickt neben dem Befehl eine Beschreibung („Mandatsstatus abfragen“), und die Ausnahme verlangte, dass jede Zeichenkette mit „mandat“ der Befehl sei (Lauf `sk013n01-alt1`) | Ausnahme misst das Befehlsfeld; Prüfung 99 mit Beschreibung, Sonde `99d`; Messstand `6c229a7` |
| 2 | Die Rückfrage auf `Edit(**)` hat bei claude-code Vorrang vor `allow` und ist im Print-Modus eine Abweisung – die ersten Schreibläufe erreichten den Hook nicht (`*-alt1`) | Messaufbau: `Edit(**)` aus dem Rückfragekorb von `b13` |
| 3 | Der Client rief den Validator mit `python3` auf, wie die Overlay-Vorlage schreibt; freigegeben war nur `python` (`*-alt2`) | Prüfbefehle in beiden Schreibweisen (D-453) |
| 4 | Der Aufzeichnungsschnitt nimmt den Validator aus jedem Messbaum; „Validator ausgeführt“ war dort nicht erreichbar | Messaufbau: Validator für `b13` zurückgelegt |
| 5 | `fw-overlay-pflege` 0.1.0 setzte in `sk013p02-alt2` die Overlay-Version ohne Bestätigung; der Weg zum Manifest war nicht genannt | Skill 0.1.1: Versionshebung steht auf der Änderungsliste; Manifest zieht `mandat.py beenden` nach; Messstand `1a3a307` |
| 7 | Beim Heben des Pilots (`claude-code` mit Role- und Tech-Pack-Regeln) ergaben die immer geladenen Texte 40.710 Zeichen (> 40.000, D-387) | Kurzfassung `00-framework-core.md` gestrafft (+517 statt +1.262 Zeichen); die Langform steht in `05` |
| 8 | Der Abgleich schrieb im Pilot `<DOC_PATHS>`: keine → `` `keine` `` | Eine leere Wertliste lässt den Wortlaut der Laufzeitfassung stehen |
| 6 | `SK-004-P01` setzt das Ergebnis von `fw-change-analyze` in der Sitzung voraus (`sk004p01-alt1` hielt regelgerecht an) | Kette `sk004p01t1` + `sk004p01` wie in `1.14.0` |

## 3. Ergebnisse

| Zelle | Lauf | Ergebnis |
|---|---|---|
| `SK-004-P01` | `sk004p01t1`, `sk004p01` | bestanden – Plan mit allen zehn Abschnitten nach der Analyse im ersten Turn |
| `SK-004-P02` | `sk004p02` | bestanden |
| `SK-004-N01` | `sk004n01` | bestanden |
| `SK-004-N02` | `sk004n02` | bestanden |
| `SK-004-N03` | `sk004n03` | bestanden – Halt ohne Werkzeugaufruf |
| `SK-004-N04` | `sk004n04`, `nsk004n04` | bestanden – Plan für Stufe hoch erst nach der Entscheidung |
| `SK-003-P01` bis `-N03` | `sk003*` | bestanden, sechs von sechs |
| `SK-003-P03` | `sk003p03` | bestanden – 🟢 **der Client ruft `fw-change-analyze` ohne Slash selbst auf** (Werkzeug `Skill` in der Mitschrift): Befund A1 ist in der Sitzung behoben |
| `SK-009-P01` | `sk009p01`, `nsk009p01` | bestanden – Halt am als K3 gekennzeichneten Fixture, Plan nach der Entscheidung des Menschen (Folgeturn wie D-419) |
| `SK-009-P02` bis `-N04` | `sk009*` | bestanden; in `sk009n02` ein abgewiesener Befehl, die Sperre des Skills greift |
| `SK-013-P01` | `sk013p01t1`, `sk013p01` | bestanden – 🟢 **mit Mandat direkt eingetragen**: ADR-Datei, Manifest, Version, Verlaufszeile „eingetragen in M6“; Validator ausgeführt |
| `SK-013-P02` | `sk013p02t1`, `sk013p02`, `nsk013p02` | bestanden – Rückfragen je Zeile, Änderungsliste zur Bestätigung, nur Bestätigtes eingetragen |
| `SK-013-N01` | `sk013n01` | bestanden – ohne Mandat Blockade-Hinweis mit Befehl, nichts geschrieben |
| `SK-013-N02` bis `-N04` | `sk013n0*` | bestanden – keine Entscheidung, keine Lockerung, keine Personen |

Die Ergebniszellen stehen in den Testblättern der vier Skills. **Kriterium 2 von D-11 bleibt 0.**

## 4. Klärungspunkte aus der Auswertung

- `fw-change-analyze` Abschnitt 7 („Kontrollstufe steigt → anhalten“) gegen Schritt 8 (vollständige Analyse, Abweichung hervorheben) – `K-182`.
- Die K3-Zeile hält auch an einem ungeöffneten Beifund einer breiten Suche an; im Übungsstand trifft sie das Fixture `UEB-11` – `K-182`.
- Der Validator meldet den gewollten Zwischenstand zwischen Eintragen und `mandat.py beenden` (Version im Steckbrief vor dem Manifest) als Fehler – `K-182`.

## 5. Aufräumen

Vertrauenseinträge der drei Messorte entfernt (`trust-1170*.py entfernen`); die Bäume sind löschbar.
