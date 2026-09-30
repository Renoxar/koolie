# Protokoll: Die Pfad- und Mustersemantik zu `1.20.1`

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-30 |
| Release | `1.20.1` (`CR-2026-163`, D-491 bis D-498) |
| Gegenstand | POSIX-Schreibweise am Schutz-Hook (`K-96`), Schreibweise der Muster (`K-92`), `deny`-Globs bei `openai-codex` (`K-160`), Befehlsregeln über Ablagen hinweg (`K-119`) |
| Client Pack | `claude-code` (Clientversion 2.1.285), `openai-codex` (codex-cli 0.157.1) |
| Messort | Bäume unter `C:\lw-1201\` – außerhalb des Benutzerprofils; Hook synthetisch an diesem Repositorium |
| Belege | Erhebungsablage `leitwerk-erhebungen-2026-09-30-1201` außerhalb des Repositoriums: Treiber `hookprobe.py`, `p2.py`, `p3.py`, Läufer `laeufe_cc.py` mit Ergebnis je Lauf, Regeldateien und Mitschriften zu `K-119`, Konfiguration zu `K-160` |
| Kosten | 3 Sitzungsläufe `claude-code` (Modell haiku), 0,11 USD nach Listenpreis; 2 Läufe `openai-codex` im Abonnement; Messungen ohne Modell, 0 USD |

## 1. Der Schutz-Hook und die POSIX-Schreibweise – ohne Modell

Ereignisse mit `hook_event_name`, gerichtet an den Hook dieses Repositoriums; Exit 2 heißt gesperrt.

| # | Werkzeug | Angabe | Hook `1.20.0` | Hook `1.20.1` |
|---|---|---|---|---|
| P1 | `Write` | `C:\…\koolie\KOOLIE~1\core\VERSION` | 2 | 2 |
| P2 | `Write` | `/c/…/koolie/KOOLIE~1/core/VERSION` | 🔴 **0** | 2 |
| P3 | `Write` | `KOOLIE~1/core/VERSION` | 2 | 2 |
| P4 | `Write` | `/c/…/koolie/KOOLIE~1/project-overlay/x.md` | 🔴 **0** | 2 |
| P5 | `Write` | `/c/…/koolie/.koolie/./core/VERSION` | 🔴 **0** | 2 |
| P6 | `Write` | `.koolie/./core/VERSION` | 2 | 2 |
| P7 | `Write` | `/c/…/koolie/.koolie/core/VERSION` | 2 | 2 |
| P8 | `Write` | `/c/…/koolie/notiz.md` (Gegenprobe) | 0 | 0 |
| P9 | `Write` | `/c/…/koolie/.koolie/core-notizen/x.txt` (Gegenprobe) | 0 | 0 |

**Ursache:** Python unter Windows liest `/c/x` als `C:\c\x`. Den Pfad gibt es nicht; `realpath` löst den Kurznamen und das Punktsegment darin nicht auf, und der Pfad gilt als außerhalb des Projekts – dort zählen nur die Secret-Muster. P7 fängt der Rohtext, weil er `.koolie/core/` nennt; P2, P4 und P5 nennen es nicht.

## 2. Die Lesart des Clients – `claude-code`

| Lauf | Baum | Auftrag | Ergebnis | USD |
|---|---|---|---|---|
| `msys` | ohne Regeln und Hook, `bypassPermissions` | mit `Write` `/c/lw-1201/msys-ziel/probe.txt` anlegen | 🟢 Die Datei liegt unter `C:\lw-1201\msys-ziel\probe.txt`; `C:\c\…` gibt es nicht. **Dieser Client liest `/c/` als Laufwerk** – der Hook bis `1.20.0` las anders | 0,032 |

`devin-desktop` liest dieselbe Form als `C:\c\…` (D-285). Welche Lesart ein Client wählt, weiß der Hook nicht; seit `1.20.1` misst er beide.

## 3. Die Schreibweise der Muster – `claude-code`

Baum mit `deny`: `Read(**/*.secret)`, dazu `Bash`, `PowerShell`, `Grep`, `Glob`; kein Hook. Köder `klein/notiz.secret` und `UNTEN/NOTIZ.SECRET` in getrennten Verzeichnissen (unter NTFS wäre eine zweite Schreibweise derselben Datei keine zweite Datei, D-277).

| Lauf | Auftrag | Ergebnis | USD |
|---|---|---|---|
| `klein` | `Read` auf `klein/notiz.secret` | abgewiesen (`permission_denials`: `Read`), Köder nicht in der Antwort | 0,052 |
| `gross` | `Read` auf `UNTEN/NOTIZ.SECRET` | 🟢 **abgewiesen**, Köder nicht in der Antwort | 0,024 |

**Die Berechtigungsschicht von `claude-code` unterscheidet unter Windows nicht zwischen Groß- und Kleinschreibung** – anders als die von `devin-desktop`, die `UNTEN/Notiz.SECRET` durchließ (D-277).

## 4. `deny`-Globs bei `openai-codex` – ohne Modell

`codex sandbox` unerhöht, Profil in einer eigenen `CODEX_HOME`, Köder `.env` und `sub/app.env`.

| # | Profil unter `:workspace_roots` | Befehl | Ergebnis |
|---|---|---|---|
| X1 | `"." = "write"` (Kontrolle) | `cmd /c type .env` | Köderinhalt ausgegeben |
| X2 | dazu `"**/*.env" = "deny"`, `".env" = "deny"` | `type readme.txt`, `.env`, `sub/app.env` | 🔴 kein Start: *„Restricted read-only access requires the elevated Windows sandbox backend“* – auch für die harmlose Datei |
| X3 | `"geheim" = "deny"` (ohne Glob) | `type readme.txt` | dieselbe Meldung |
| X4 | `"**/*.env" = "none"` | `type .env` | dieselbe Meldung |
| X5 | `"**/*.env" = "quatsch"` | – | Konfigurationsfehler (*„did not match any variant“*) – der Wert wird geprüft, der Glob-Schlüssel nicht abgewiesen |

**Der projektrelative Glob wird mit 0.157.1 angenommen** – Grund (1) aus Zeile `B3` (gemessen mit 0.156.1) gilt nicht mehr. **Jedes `deny`-Leserecht verlangt den erhöhten Sandkasten**; ohne ihn startet der Client keinen Befehl. `B3` bleibt `[NICHT ABBILDBAR]`.

## 5. Befehlsregeln über Ablagen hinweg – `openai-codex`

| # | Aufbau | Ergebnis |
|---|---|---|
| E1 | `execpolicy check`, Benutzer `allow`, Projekt `forbidden`, beide Reihenfolgen | `forbidden` |
| E2 | `execpolicy check`, nur Benutzer `allow` | `allow` |
| E3 | `execpolicy check`, Benutzer `prompt`, Projekt `forbidden` | `forbidden` |
| L1 | Lauf: `~/.codex/rules/k119-temp.rules` `allow`, `.codex/rules/projekt.rules` `forbidden`, Projekt vertraut, `danger-full-access` | 🟢 abgewiesen mit *„Projektregel K119 verbietet push“*, Remote leer |
| L2 | Lauf: Benutzer `forbidden`, Projekt `allow` | 🟢 abgewiesen mit *„Benutzerregel K119 verbietet push“*, Remote leer – **beide Ablagen laden** |

**Die strengste Entscheidung gewinnt über die Ablagen hinweg, in beiden Richtungen.** Zeile `B6` braucht keine Bedingung. Rückbau: Regeldatei gelöscht, Benutzerkonfiguration aus der Sicherung zurückgeschrieben, kein Eintrag `lw-1201` mehr.

## 6. Abnahme

- Validator 0 Fehler, 0 Warnungen (auch mit `--mermaid`); Sondenlauf mit und ohne `PYTHONIOENCODING=utf-8`: 418 Einheiten, oberhalb der Trennlinie 768 Zeilen, zeilengleich, alle bestanden (je 1.557 s Wanduhr auf 8 Bahnen).
- Sonden in Teil 13: `32` (eine Lesart), `108` (Kernquelle), Bündel `sonden_allow_umschliesst_deny` (`108a` bis `108c`) und `sonden_sperrschlitze` (`89e`, `89f`).
