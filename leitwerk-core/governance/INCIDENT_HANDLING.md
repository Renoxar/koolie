# Behandlung von Sicherheits- und Datenschutzvorfällen mit KI-Bezug

| Attribut | Wert |
|---|---|
| ID | `FW-GOV-INC` |
| Version | `0.1.1` |
| Status | `entwurf` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` in Abstimmung mit `<SECURITY_CONTACT>` |

## 1. Geltung und Vorrang (normativ)

1. Für alle Vorfälle gelten **zuerst** die Melde- und Behandlungsprozesse der Organisation (Ebene 2). Dieses Modul ergänzt sie um die KI-spezifische Erfassung und den Rückfluss in das Framework; es ersetzt keine Meldepflichten und keine Fristen der Organisation.
2. KI-Bezug liegt vor, wenn KI-Nutzung Ursache, Weg oder Verstärker eines Vorfalls war – insbesondere: Bereitstellung von K3-Inhalten (S2/S3), ausgeführte oder versuchte Injektion (S6), durch den KI-Client veranlasste unerwünschte Aktionen, Abfluss über MCP/Web, sicherheitsrelevante Fehler in übernommenem KI-Code.

## 2. Sofortmaßnahmen (normativ)

| Situation | Sofort | Danach |
|---|---|---|
| K3-Inhalt an den KI-Client gelangt | Sitzung beenden; keine weiteren Eingaben | `leitwerk-core/framework/core/02-privacy.md` Abschnitt 5: Secrets rotieren lassen; Meldung `<SECURITY_CONTACT>`, bei Personenbezug `<DATA_PROTECTION_CONTACT>`; Löschverfahren laut Vertrag (`<TBD: Löschverfahren laut Vertrag>`) |
| Injektionsversuch mit Wirkung (Aktion ausgeführt oder Daten preisgegeben) | Sitzung beenden; betroffene Artefakte sichern (Ergebnisbericht, Sitzungsverlauf) | Meldung `<SECURITY_CONTACT>`; betroffene Änderungen nicht mergen; Quelle des Inhalts identifizieren |
| Sicherheitsrelevanter Fehler in bereits übernommenem KI-Code | Prozess der Organisation für Schwachstellen | zusätzlich Erfassung nach Abschnitt 3 (Review-/Gate-Lücke analysieren) |
| Verdacht auf kompromittierte Erweiterung, Skill-Quelle oder MCP-Server | Nutzung stoppen; Framework Owner und `<SECURITY_CONTACT>` informieren | Freigaben widerrufen (Overlay/Konfiguration), Hotfix prüfen |

## 3. Erfassung (normativ)

Jeder Vorfall mit KI-Bezug erhält einen Eintrag im Vorfallregister des Projekts (`<TBD: Ablageort des Registers, außerhalb des Frameworks-Repositorys möglich>`):

| Feld | Inhalt |
|---|---|
| ID | `INC-<PROJECT_CODE>-<JJJJ>-<NNN>` |
| Datum, meldende Rolle | ohne Personennennung über die Rolle hinaus |
| Kategorie | K3-Bereitstellung / Injektion / unerwünschte Aktion / Code-Schwachstelle / Werkzeugkette |
| Hergang (bereinigt) | Ablauf ohne vertrauliche Inhalte; betroffene Artefakte als Referenz |
| Auslösende Lücke | Verhalten / Regel fehlte / Regel unklar / technische Sperre fehlte / Produktverhalten |
| Sofortmaßnahmen und Meldungen | mit Zeitpunkten |
| Folgemaßnahmen | Änderungsanträge (CR-…), Testkatalog-Ergänzungen, Onboarding-Anpassungen |
| Status | offen / in Umsetzung / geschlossen |

## 4. Rückfluss in das Framework (normativ)

1. Jeder geschlossene Vorfall wird im Review-Zyklus ausgewertet (Lessons Learned): Welche Regel, Sperre oder Übung hätte ihn verhindert?
2. Ergebnis ist mindestens eines von: Änderungsantrag, neuer Negativtest im Testkatalog (Klassen PI/DS/SC), Köder- oder Übungsanpassung im Onboarding, Klarstellung in Checklisten – oder eine dokumentierte Begründung, warum keine Maßnahme folgt.
3. Häufungen gleicher Kategorien sind ein Eskalationssignal an Projektleitung und Organisation (Werkzeugfreigabe überprüfen).

## 5. Erläuterung

Das Register misst nicht Schuld, sondern Lückendichte. Ein Team, das Beinahe-Vorfälle meldet (der Köder aus dem Onboarding in freier Wildbahn), härtet Regeln und Hooks schneller, als es ein Audit je könnte.
