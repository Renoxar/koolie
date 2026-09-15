# Framework Core 01 – Governance-Grundsätze

| Attribut | Wert |
|---|---|
| Modul-ID | FW-CORE-01 |
| Ebene | 1 – Framework Core |
| Verbindlichkeit | normativ |
| Owner | `<FRAMEWORK_OWNER>` |
| Version | 0.2.0 |
| Status | `pilot` |

## 1. Gegenstand und Geltung (normativ)

1. Das Framework regelt den Einsatz von Devin Desktop (und strukturell weiterer KI-gestützter Entwicklungswerkzeuge) in Softwareentwicklungsprojekten. Es gilt für alle Personen, die im Geltungsbereich eines Project Overlays mit dem KI-Client arbeiten.
2. Das Framework ergänzt bestehende Entwicklungs-, Review- und Freigabeprozesse. Es ersetzt sie nicht und hat im Konfliktfall keinen Vorrang vor rechtlichen, regulatorischen oder organisationsweiten Vorgaben (`leitwerk-core/governance/PRIORITY_HIERARCHY.md`).
3. Ohne ein freigegebenes Project Overlay (Status `aktiv` im Overlay-Steckbrief) DARF der KI-Client in einem Projekt NICHT produktiv eingesetzt werden; zulässig sind nur Onboarding-Übungen auf synthetischen Übungsrepositorys.

## 2. Rollen des Frameworks (normativ)

| Rolle | Verantwortung | Besetzung |
|---|---|---|
| Framework Owner | Gesamtverantwortung für Core, Release, Prioritätshierarchie, Testkatalog, Produktbeobachtung | `<FRAMEWORK_OWNER>` (generische Rolle, keine Person) |
| Modul-Owner | Fachliche und technische Verantwortung für ein Role Pack, Technology Pack oder eine Skill-Gruppe | je Modul im `leitwerk-core/OWNERS.md` |
| Project Overlay Owner | Pflege und Freigabe des Overlays eines Projekts | `<APPROVAL_ROLE>` des Projekts |
| Security-Kontakt | Sicherheitsfreigaben, Vorfallbehandlung | `<SECURITY_CONTACT>` |
| Datenschutzkontakt | Datenschutzfreigaben, Prüfung von Kontextklassen | `<DATA_PROTECTION_CONTACT>` |
| Mentorin oder Mentor | Begleitung des Onboardings, Freigabe zur selbstständigen Nutzung | vom Projekt benannt |
| Anwenderin oder Anwender | Einhaltung der Regeln, Meldung von Abweichungen, Feedback | alle Entwicklerinnen und Entwickler |

Die detaillierte RACI-Zuordnung liegt in `leitwerk-core/governance/RACI.md`.

## 3. Änderungsgrundsätze (normativ)

1. Änderungen am Framework Core erfolgen ausschließlich über Änderungsanträge (`leitwerk-core/governance/CHANGE_REQUEST_TEMPLATE.md`) und Releases (`leitwerk-core/governance/RELEASE_PROCESS.md`).
2. Änderungen am Project Overlay erfolgen über den Prozess des Projekts, MÜSSEN aber die Validierung (`leitwerk-core/tests/scripts/validate-framework.py`) bestehen und DÜRFEN NICHT Core-Dateien verändern.
3. Jede Änderung ist im `leitwerk-core/CHANGELOG.md` (Framework) beziehungsweise im Overlay-Änderungsverlauf dokumentiert.
4. **Jeder Modulträger durchläuft den Lebenszyklus `entwurf → pilot → aktiv → veraltet → zurückgezogen`.** Die Statuswerte und die Übergangsbedingungen für Skills stehen in `08-skill-conventions.md` Abschnitt 7, die Bedingungen für alle übrigen Modulträger in Abschnitt 5 dieses Moduls (D-102).

## 4. Auditierbarkeit (normativ)

Für jeden Zeitpunkt MUSS nachvollziehbar sein: welche Framework-Version, welches Overlay (Version), welche Skills (Version) und welche Berechtigungskonfiguration galten. Dies wird erreicht durch Versionierung im Repository, `leitwerk-core/VERSION`-Datei, Overlay-Steckbrief mit Version und den KI-Nutzungsvermerk je Merge Request.


## 5. Lebenszyklus der Modulträger (normativ)

1. **Modulträger** ist jede versionierte Datei des Frameworks, die einen **Steckbrief** führt: die erste Tabelle des Dokuments, vor der ersten Überschrift der Ebene 2, mit der Kopfzeile `\| Attribut \| Wert \|`. Dazu gehören die Module unter `leitwerk-core/framework/core/`, Checklisten, Prompts, Entscheidungsbäume, Governance-Dokumente, Register, Onboarding- und Pilotdokumente, die Steckbriefe der Client-, Role- und Technology-Packs sowie Skills. **Jeder Modulträger MUSS in seinem Steckbrief eine Zeile `\| Status \| … \|` führen**; Prüfung 47 des Validators setzt das durch. **Bis 0.50.0 war der Modulträger über eben diese Zeile definiert** – eine Definition, die ihren Gegenstand entkommen lässt, indem er die Zeile weglässt, und zwölf Träger taten genau das, darunter die elf normativen Kernmodule (`K-36`, D-105). **Vorlagen sind keine Modulträger:** Ihr Steckbrief beschreibt die Kopie, die aus ihnen entsteht; seine Statuszelle ist ein Ausfüllschlitz (D-104).
2. Die fünf Statuswerte und ihre Bedeutung stehen in `leitwerk-core/framework/core/08-skill-conventions.md` Abschnitt 7 und gelten für **jeden** Modulträger. Die dort genannten Übergangsbedingungen gelten für Skills; für alle übrigen Modulträger gilt die Tabelle in Punkt 3 (D-102).
3. Übergangsbedingungen für Modulträger, die keine Skills sind:

| Übergang | Voraussetzung |
|---|---|
| `entwurf` → `pilot` | (a) Der Träger ist inhaltlich vollständig: Jeder Abschnitt, den sein Zweck verlangt, ist ausgefüllt. (b) Der Validatorlauf ist ohne Fehler. (c) Offene `VERIFY`-Marker des Trägers sind benannt; sie sperren den Übergang **nicht** – gezählt werden sie in Kriterium 1 von D-11. (d) Ein offener Ausfüllwert (`<TBD…>`) sperrt den Übergang nicht, wenn er einen Wert der aufnehmenden Organisation bezeichnet; er sperrt ihn, wenn er eine Aussage des Frameworks offenlässt. (e) **Review durch den Modul-Owner mit Fundstelle:** ein Protokoll unter `leitwerk-core/tests/protocols/`, das den Träger namentlich nennt und (a) bis (d) je Träger festhält |
| `pilot` → `aktiv` | (a) bis (e) wie oben; zusätzlich: alle Testfälle des Trägers im Testkatalog auf `bestanden`, Anwendung in mindestens einem Projekt außerhalb des Frameworks mit ausgewerteter Rückmeldung (`leitwerk-core/governance/FEEDBACK_PROCESS.md`), Freigabe durch den Framework Owner |
| `aktiv` → `veraltet` → `zurückgezogen` | wie in `08-skill-conventions.md` Abschnitt 7; die Ankündigungsfrist des Release-Prozesses gilt unverändert (`leitwerk-core/governance/RELEASE_PROCESS.md`) |

4. **Ein Statuswert ist keine Aussage über das Verhalten eines KI-Clients.** Ob ein Client einem Träger folgt, belegt allein ein Sitzungstest des Testkatalogs. Ein Träger auf `pilot` ist strukturell abgenommen, nicht erprobt.
5. **Ein Statuswechsel ist keine Versionsänderung.** Er ändert keine Anweisung des Trägers; eine angehobene Version behauptete eine Inhaltsänderung, die es nicht gibt, und löste bei einem Skill nach `08-skill-conventions.md` Abschnitt 7 die erneute Ausführung aller Testfälle aus. Auch der Änderungsverlauf des einzelnen Trägers verzeichnet ihn nicht; festgehalten ist er im Abnahmeprotokoll und im Änderungsverzeichnis des Frameworks (D-103, D-106).
6. Der Stand aller Modulstatus ist Kriterium 3 von D-11. Prüfung 46 des Validators rechnet ihn bei jedem Lauf aus und hält ihn gegen die Standzeile in `leitwerk-core/docs/ROADMAP.md`; **eine Abweichung in beide Richtungen ist ein Fehler.** Ein Statuswechsel ohne nachgezogene Standzeile lässt den Lauf scheitern.
