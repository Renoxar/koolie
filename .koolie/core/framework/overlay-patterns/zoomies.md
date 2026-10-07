# Overlay-Muster „zoomies“

| Attribut | Wert |
|---|---|
| ID | `FW-OVL-ZOOMIES` |
| Name | `zoomies` |
| Version | `0.1.0` |
| Status | `pilot` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Baut auf | `general` |
| Kennzeichen | 🎉 Party-Overlay – ändert keine Pflicht |
| Im Dialog | 🎉 Party-Overlay mit Augenzwinkern, baut auf general auf, ändert keine Pflicht |
| Gewählt über | `python .koolie/core/install.py --overlay zoomies` – **nur bei der Erstinstallation**, nie Vorgabe im Dialog |
| Wirkung | alles aus `general`; dazu eine immer geladene Regeldatei `21-overlay-zoomies.md` (rund 1.000 Zeichen) und ein Dokument mit den Bausteinen |

## Zweck

Ein Koolie ist ein australischer Hütehund, und „Zoomies“ sind sein wilder Freudensprint. Dieses
Muster bringt ein Augenzwinkern in Dokumente, Commit-Texte, Testnamen, Log- und Merge-Request-Texte –
dort, wo es passt, und nirgends sonst.

## Der Grundsatz: Humor ändert keine Pflicht

`zoomies` gibt nichts frei. Werte und Berechtigungen sind dieselben wie bei `general`; die
Regeldatei konkretisiert nur den Ton. Kontrollstufen, Freigaben, Sperren, K3 und Review gelten
unverändert, und wo eine Pflicht berührt ist, unterbleibt der Witz. Die Sonde zu diesem Muster
vergleicht die Berechtigungsdatei mit der aus `general` und verlangt Gleichheit.

## Die Werte

Keine eigenen; es gelten die Werte von `general`.

## Die Regel

`rules/21-overlay-zoomies.md` wird bei der Erstinstallation für den Client gerendert und in die
Regelablage geschrieben. Sie lädt immer, damit der Ton auch ohne Nachschlagen gilt, und bleibt
deshalb kurz: Grundsatz, Grenzen und die elf Bausteine mit Schalter. Danach gehört sie dem
Projekt; ein Baustein wird dort abgeschaltet.

## Die Dokumente

| Typ | Was das Dokument enthält | Was bewusst fehlt |
|---|---|---|
| `coding-guidelines` | die elf Bausteine mit Beispielen und Grenzen, Abschalten, Kater-Modus | jede Lockerung einer Pflicht |

## Kennzeichnung

Das Kennzeichen „🎉 Party-Overlay – ändert keine Pflicht“ steht in diesem Steckbrief, in der
Ausgabe von `install.py`, im Änderungsverlauf des Overlays und als Zeile „Overlay-Muster“ in der
Laufzeitfassung `20-project-overlay.md`.

## Änderungsverlauf

| Version | Datum | Änderung |
|---|---|---|
| `0.1.0` | 2026-10-06 | Erstfassung mit elf Bausteinen |
