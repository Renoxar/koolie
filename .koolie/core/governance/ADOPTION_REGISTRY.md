# Bestandsliste der übernehmenden Projekte

| Attribut | Wert |
|---|---|
| ID | `FW-GOV-REG` |
| Version | `0.1.1` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Gilt für | alle Projekte, die den Framework-Kern übernommen haben |
| Entstehung | `CR-2026-128`, **D-322** (2026-09-23) |
| Pflicht aus | `.koolie/core/governance/RELEASE_PROCESS.md` Abschnitt 4 Punkt 4 (Auditierbarkeit) |

## 1. Wozu diese Liste da ist

`RELEASE_PROCESS.md` verlangt sie seit der Erstfassung, und `AP12` führt
*„Bestandsliste initialisieren"* als Aktivität. **Sie beantwortet eine Frage, die sonst
niemand stellt:** *Welches Projekt läuft gerade auf welchem Stand, und wann wurde es
zuletzt gehoben?*

🔴 **Sie ist mit `1.0.0` angelegt worden, und ihr erster Eintrag ist zugleich ihr erster
Befund.** Beide übernehmenden Projekte standen am 2026-09-23 auf `0.88.0` – **drei
Releases hinter `main`**, während Kriterium 5 von D-11 (*„Übernahme in ein zweites Projekt
nachgewiesen"*) als erfüllt geführt wurde. Kriterium 5 ist die einzige der fünf Aussagen,
die **Prüfung 46 ausdrücklich nicht nachrechnet** (eine Enthaltung, D-11). ➡️ *Ein
Nachweis, den niemand zählt, ist einer, den niemand veralten sieht.*

## 2. Der Bestand

| Projekt | Rolle | Client Pack | Framework-Version | Overlay-Version | zuletzt gehoben |
|---|---|---|---|---|---|
| `devpacks/otp-generator` | **Pilot** – ein echtes Projekt, keine Spielwiese | `claude-code` | **1.0.1** | `0.3.2` | 2026-09-23 |
| `devpacks/test-devin-framework` | **Übungsrepositorium** – Meßgegenstand der Sitzungstests, 31 Präparationen | `devin-desktop` | **1.0.1** | `1.0.1` | 2026-09-23 |

🔴 **Diese Zeilen standen nach `1.0.1` einen halben Tag lang auf `1.0.0`, während die
Projekte `1.0.1` trugen.** Ursache: Sie wurden **nach** dem Merge gehoben statt davor –
und damit war `FW-CL-11` Prüfpunkt 20 (*„übernehmende Projekte informiert"*) zum
Merge-Zeitpunkt nicht erfüllt. ➡️ *Eine Liste, die erst nach dem Release fortgeschrieben
wird, ist beim Release falsch.* ⚠️ **Zu entscheiden: Gehört das Heben vor den
Release-Commit, und muß `RELEASE_PROCESS.md` Abschnitt 4.1 die Reihenfolge nennen?**

⚠️ **Der Pfad ist der des Arbeitsplatzes und keine Adresse.** Was ein Projekt für den
Nachweis identifiziert, ist sein Repositorium; die Pfadspalte sagt nur, wo es auf diesem
Rechner liegt.

## 3. Was ein Eintrag aussagt – und was nicht

| Aussage | trifft zu | trifft **nicht** zu |
|---|---|---|
| Der Kern dieses Projekts steht auf der genannten Version | ✅ gemessen an `.koolie/core/VERSION` | – |
| Die Laufzeitschicht ist mit dieser Version erzeugt | ✅ über `install.py --update` | – |
| Das Projekt **nutzt** das Framework im Alltag | – | 🔴 **Nein.** Eine Übernahme ist kein Betriebsnachweis; dafür sind `AP8` bis `AP10` zuständig, und die sind **projektseitig** |
| Das Overlay ist aktiv | – | 🔴 **Nein.** Das prüft `validate-framework.py --strict-overlay` je Projekt, nicht diese Liste |

## 4. Wann sie fortgeschrieben wird

**Bei jedem Release, als Teil von `FW-CL-11`** – Prüfpunkt *„Release-Archiv erzeugt und
abgelegt; übernehmende Projekte informiert"*. Der Ablauf steht in `RELEASE_PROCESS.md`
Abschnitt 4.1.

🟢 **Die Archive liegen seit `1.0.0` als Anhang am Release des Hostingdienstes**, je mit
Prüfsumme – das ist die *„Ablage außerhalb des Repositoriums"* aus Abschnitt 4.1 in ihrer
natürlichen Form: am **signierten** Stand, nicht daneben.

⚠️ **Keine Prüfung hält diese Liste gegen die Projekte.** Sie kann es nicht: Die Projekte
liegen außerhalb dieses Repositoriums, und eine Prüfung, die sie sucht, wäre auf jedem
anderen Arbeitsplatz rot (D-299). **Das ist eine benannte Grenze und kein Versehen** –
dieselbe Lage wie bei `K-105`, dem Vortragsmittel.
