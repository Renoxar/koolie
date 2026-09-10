# Organisationsweite Vorgaben (Ebene 2 der Prioritätshierarchie) – Einbindungspunkt

Dieses Verzeichnis ist **kein** Bestandteil des Framework Core. Es ist der definierte Ort, an dem eine Organisation ihre verbindlichen Richtlinien für den Einsatz von KI-Werkzeugen einbindet, ohne den Core zu ändern.

## Was hier eingebunden wird

| Dokumenttyp | Beispiel (generisch) | Einbindung |
|---|---|---|
| KI-Nutzungsrichtlinie der Organisation | zulässige Werkzeuge, Freigabeprozess, Meldewege | Verweisblatt oder bereinigter Auszug |
| Informationssicherheitsrichtlinie (relevante Auszüge) | Klassifizierungsschema, Umgang mit Secrets, Meldefristen | Verweisblatt |
| Datenschutzvorgaben (relevante Auszüge) | Umgang mit personenbezogenen Daten in Entwicklung und Test | Verweisblatt |
| Nachweis der Werkzeugfreigabe | Freigabe von Devin Desktop mit Auflagen (Plan, Einstellungen, Vertragsstand) | Verweisblatt mit Referenz |
| Erzwungene Team-Einstellungen | Dokumentation der administrativ gesetzten Einstellungen (Berechtigungen, Sandbox, MCP, Modelle, Websuche) | Auszug ohne interne Adressen |

## Regeln

1. Organisationsweite Vorgaben haben Vorrang vor dem Framework Core (`leitwerk-core/governance/PRIORITY_HIERARCHY.md`). Enthält eine Vorgabe eine strengere Regel, gilt sie unmittelbar; das Framework wird im nächsten Release angepasst, wenn die strengere Regel dauerhaft ist.
2. Enthält eine Vorgabe eine **weniger** strenge Regel als der Core, bleibt der Core maßgeblich, bis der Framework Owner die Lockerung nach dokumentierter Prüfung in den Core übernimmt (P9 Secure by Default).
3. Dokumente hier tragen Kontextklasse K1 oder werden nur als Verweisblatt geführt. Sie werden für den KI-Client nur geladen, wenn das Projekt sie im Overlay-Manifest registriert (Typ `ai-governance` oder `other`).
4. Abgleich: Das Klassifizierungsschema der Organisation wird auf die Kontextklassen K0–K3 abgebildet (`leitwerk-core/framework/core/02-privacy.md`); die Abbildung wird hier dokumentiert: `<TBD: Abbildungstabelle Organisationsklassifizierung → K0–K3>`.

## Ablage

```text
org-policies/
├── README.md                 # diese Datei
├── MAPPING_CLASSIFICATION.md # <TBD: Abbildung des Klassifizierungsschemas auf K0–K3>
└── <TBD: Verweisblätter>
```
