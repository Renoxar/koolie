# Bestandsliste der übernehmenden Projekte

| Attribut | Wert |
|---|---|
| ID | `FW-GOV-REG` |
| Version | `0.2.3` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Gilt für | alle Projekte, die den Framework-Kern übernommen haben |
| Entstehung | `CR-2026-128`, **D-322** (2026-09-23); Verfahren und Prüfung mit `CR-2026-130`, **D-330** / **D-331** |
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
| `devpacks/otp-generator` | **Pilot** – ein echtes Projekt, keine Spielwiese | `claude-code` | **1.4.3** | `0.3.8` | 2026-09-24 |
| `devpacks/test-devin-framework` | **Übungsrepositorium** – Meßgegenstand der Sitzungstests, 31 Präparationen | `devin-desktop` | **1.4.3** | `1.4.2` | 2026-09-24 |

🟢 **STAND 2026-09-24: BEIDE PROJEKTE TRAGEN `1.4.3`, UND DIE HEBUNG IST DORT COMMITTET.** `1.4.3` ordnet ein und ändert nichts, was ein Projekt erreicht (D-353); **die beiden Berechtigungsdateien dieser Liste sind zugleich sein Meßgegenstand** – 37 Projekteinträge, die ein Erzeugen bei `--update` überschrieben hätte. `1.4.2` berichtigt die Auskunft über ignorierte Kerndateien (D-352); im Pilotprojekt ist sie der erste Lauf der berichtigten Fassung gegen die projekteigene Zeile `build/`. Die Hebung auf `1.4.0` war auf Entscheidung des Framework Owners verschoben; sie ist mit `1.4.1` nachgeholt, in einem Schritt über beide Releases. ⚠️ **Die Spalte `Overlay-Version` stand bis dahin auf `0.3.3` und `1.1.0`, während die Projekte seit `1.3.0` `0.3.5` und `1.3.0` trugen** – Prüfung 82 hält nur die Spalte `Framework-Version` (`CR-2026-134`). *Eine Spalte, die niemand zählt, ist eine, die niemand veralten sieht.*

🟢 **DIE FRAGE IST MIT `1.1.0` ENTSCHIEDEN: JA ZU BEIDEM** (`CR-2026-130`, D-330).
Das Heben steht seit diesem Release **vor** dem Freigabe-Commit, `RELEASE_PROCESS.md`
Abschnitt 4.1 nennt die Reihenfolge, `FW-CL-11` führt dafür einen eigenen Prüfpunkt
(D-329) – und **Prüfung 82** hält die Spalte `Framework-Version` gegen
`.koolie/core/VERSION` (D-331).

🔴 **Die Herleitung, und sie war teurer als gebucht.** Diese Zeilen standen nach `1.0.1`
einen halben Tag auf `1.0.0`, während die Projekte `1.0.1` trugen – und das war nur die
erste von **zwei** Stellen. Gemessen am 2026-09-23 im Vorbedingungsdurchgang von
`1.1.0`: Das Framework hatte seine Liste berichtigt, die **ausgelieferten Kopien** in
beiden übernehmenden Projekten trugen weiter `1.0.0` neben einer `VERSION` `1.0.1`.
➡️ ***Wer eine Liste nach dem Heben fortschreibt, schreibt sie an einer Stelle fort und
liefert sie an zwei.***

🔴 **UND DAS HEBEN ENDETE BIS `1.3.0`, BEVOR SEIN ERGEBNIS DAUERHAFT WAR** (D-343).
Die vier Handgriffe von Schritt 2 nannten das **Committen im übernehmenden Projekt**
nicht. Gemessen beim Abschluß von `1.2.0`: In **beiden** Projekten trug der jüngste
Commit `VERSION` `1.0.1`; die Hebung auf `1.1.0` ist nie committet worden. ➡️ ***Ein
Verfahrensschritt, der endet, bevor sein Ergebnis dauerhaft ist, liefert einen Zustand
und keinen Stand.*** Schritt 2 trägt seither einen fünften Handgriff.

🟢 **Deshalb nennt diese Liste den ZIELSTAND, bevor gehoben wird.** Schritt 1 des
Verfahrens schreibt sie fort, Schritt 2 hebt – die Kopie trägt dann denselben Stand wie
das Original. ⚠️ **Und genau darin liegt die Grenze von Prüfung 82:** Sie mißt die
**Behauptung** dieser Zeile und nicht den Stand des Projekts. Wer die Zeile ändert, ohne
zu heben, kommt durch (D-331).

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
