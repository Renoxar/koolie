# Bestandsliste der übernehmenden Projekte

| Attribut | Wert |
|---|---|
| ID | `FW-GOV-REG` |
| Version | `0.3.0` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Gilt für | alle Projekte, die den Framework-Kern übernommen haben |
| Pflicht aus | `.koolie/core/governance/RELEASE_PROCESS.md` Abschnitt 4 Punkt 4 (Auditierbarkeit) |

## 1. Wozu diese Liste da ist

Sie beantwortet eine Frage: Welches Projekt läuft auf welchem Stand, und wann wurde es zuletzt
gehoben? Ein Projekt, das mehrere Releases zurückliegt, fällt hier auf.

## 2. Der Bestand

| Projekt | Rolle | Client Pack | Framework-Version | Overlay-Version | zuletzt gehoben |
|---|---|---|---|---|---|
| `devpacks/otp-generator` | **Pilot** – ein echtes Projekt, keine Spielwiese | `claude-code` | **2.1.0** | `0.3.45` | 2026-10-05 |
| `devpacks/test-devin-framework` | **Übungsrepositorium** – Meßgegenstand der Sitzungstests, 34 Präparationen | `devin-desktop` | **2.1.0** | `1.4.40` | 2026-10-05 |

Beide Projekte haben den Lieferumfang `voll` und werden mit
`install.py --target <projekt> --update` gehoben. Was ein Release in einem Projekt geändert hat,
steht im Änderungsverlauf seines Overlays und im `CHANGELOG.md`.

Die Liste nennt den **Zielstand**, bevor gehoben wird: Schritt 1 des Verfahrens in
`RELEASE_PROCESS.md` Abschnitt 4.1 schreibt sie fort, Schritt 2 hebt die Projekte und committet
die Hebung dort. So trägt die ausgelieferte Kopie denselben Stand wie das Original. Prüfung 82
hält die Spalte `Framework-Version` gegen `.koolie/core/VERSION`; sie prüft die Zeile, nicht den
Stand des Projekts.

Die Pfadspalte sagt nur, wo ein Projekt auf diesem Rechner liegt. Für den Nachweis zählt sein
Repositorium.

## 3. Was ein Eintrag aussagt – und was nicht

| Aussage | trifft zu | trifft **nicht** zu |
|---|---|---|
| Der Kern dieses Projekts steht auf der genannten Version | ✅ gemessen an `.koolie/core/VERSION` | – |
| Die Laufzeitschicht ist mit dieser Version erzeugt | ✅ über `install.py --update` | – |
| Das Projekt **nutzt** das Framework im Alltag | – | Nein. Eine Übernahme ist kein Betriebsnachweis; dafür sind `AP8` bis `AP10` zuständig, und die sind projektseitig |
| Das Overlay ist aktiv | – | Nein. Das prüft `validate-framework.py --strict-overlay` je Projekt |

## 4. Wann sie fortgeschrieben wird

Bei jedem Release, als Teil von `FW-CL-11` (Prüfpunkt *„Release-Archiv erzeugt und abgelegt;
übernehmende Projekte informiert"*). Der Ablauf steht in `RELEASE_PROCESS.md` Abschnitt 4.1. Die
Archive liegen mit Prüfsumme als Anhang am signierten Release des Hostingdienstes.

Keine Prüfung hält diese Liste gegen die Projekte: Die liegen außerhalb dieses Repositoriums,
und eine solche Prüfung wäre auf jedem anderen Arbeitsplatz rot.
