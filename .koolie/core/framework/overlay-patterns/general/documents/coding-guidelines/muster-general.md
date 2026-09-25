# Coding Guidelines – allgemeine Grundsätze

> **Muster – vom Overlay Owner zu prüfen und anzupassen.** Mitgeliefert mit dem
> Overlay-Muster `general` und im Manifest mit Status `entwurf` registriert. Verbindlich
> wird das Dokument erst, wenn der Overlay Owner es freigibt und in der Laufzeitfassung
> als K1-Dokument führt; bis dahin ist es ein Vorschlag.
>
> Es enthält nur, was auf jedes Softwareprojekt passt: keine Werkzeuge, keine
> Schwellenwerte, keine Vorgaben zu Sprache, Plattform oder Teamgröße. Was das Projekt
> konkret festlegt – Formatierer, Benennungsschema, verbotene Muster –, gehört in
> `OVERLAY.md` Abschnitt 9 oder als Ergänzung in dieses Dokument.

## Verhältnis zum Framework

Dieses Dokument gilt für **jeden** Code des Projekts, unabhängig davon, wer ihn schreibt.
Was speziell für KI-unterstützte Änderungen gilt, steht im Kern und wird hier nicht
wiederholt: `.koolie/core/framework/core/04-quality.md` Abschnitt 2 (unter anderem ein
Ziel je Änderung, Vorrang der Conventions vor dem KI-Vorschlag, Entfernen von
Generierungsresten) und `.koolie/core/framework/core/07-review-rules.md`. Bei Widerspruch
gilt der Kern.

## 1. Lesbarkeit

1. Code wird öfter gelesen als geschrieben. Bei der Wahl zwischen kurz und verständlich
   gewinnt verständlich.
2. Namen sagen, was etwas ist oder tut, in der Sprache des Fachgebiets. Abkürzungen nur,
   wenn sie im Projekt allgemein bekannt sind.
3. Eine Funktion arbeitet auf einer Abstraktionsebene. Wer beim Lesen zwischen Fachlogik
   und technischen Details springen muss, braucht eine weitere Funktion.
4. Einheitlicher Stil ist wichtiger als der Stil selbst. Die Formatierung übernimmt ein
   Werkzeug, wo das Projekt eines führt; Stilfragen sind dann kein Review-Thema.

## 2. Aufbau

1. Jede Einheit – Funktion, Klasse, Modul – hat **eine** Verantwortung und damit einen
   Grund, sich zu ändern.
2. Einfachheit vor Vorratshaltung: gebaut wird, was die Anforderung verlangt, nicht was
   sie vielleicht einmal verlangt (KISS, YAGNI).
3. Wissen steht an genau einer Stelle (DRY). Gleich aussehender Code, der aus
   verschiedenen Gründen existiert, ist keine Duplikation und wird nicht zwangsweise
   zusammengelegt.
4. Abhängigkeiten zeigen von Details zu Abstraktionen, nicht umgekehrt. Fachlogik kennt
   keine Einzelheiten von Speicherung, Oberfläche oder Transport.
5. Seiteneffekte sind sichtbar: Eine Funktion, die Zustand ändert, sagt es im Namen oder
   in der Signatur. Globaler veränderlicher Zustand wird vermieden.
6. Code ist testbar gebaut: Abhängigkeiten werden übergeben, nicht versteckt erzeugt.

## 3. Werte und Fehler

1. Keine magischen Werte: Zahlen und Zeichenketten mit Bedeutung bekommen einen Namen.
2. Fehler werden behandelt oder bewusst weitergegeben, nie stillschweigend verschluckt.
   Eine leere Fehlerbehandlung braucht eine Begründung im Code.
3. Fehlermeldungen nennen, was schiefging und in welchem Zusammenhang – für den, der sie
   lesen muss.
4. Ungültige Zustände werden früh abgewiesen, nicht tief im Ablauf entdeckt.
5. Ressourcen werden auf jedem Pfad freigegeben, auch im Fehlerfall.

## 4. Kommentare und Dokumentation

1. Kommentare erklären das **Warum** – eine Entscheidung, eine Einschränkung, einen
   Umweg. Das **Was** sagt der Code.
2. Ein veralteter Kommentar ist schlimmer als keiner. Wer Code ändert, ändert den
   Kommentar mit.
3. Öffentliche Schnittstellen sind dokumentiert: Zweck, Eingaben, Ergebnis, Fehlerfälle.
4. Auskommentierter Code wird gelöscht; die Versionsverwaltung bewahrt ihn.

## 5. Veränderung

1. Kleine, in sich geschlossene Schritte sind leichter zu prüfen und zurückzunehmen als
   große.
2. Refaktorisierung und Verhaltensänderung werden getrennt, damit jede für sich
   nachvollziehbar bleibt.
3. Wer beim Arbeiten auf Mängel außerhalb der Aufgabe stößt, **benennt** sie – als
   offenen Punkt oder Folgeaufgabe – und behebt sie nicht nebenbei. Die
   „Pfadfinderregel“ gilt nur innerhalb des Scopes der Änderung.
4. Warnungen von Übersetzer und Analyse werden behoben, nicht unterdrückt. Eine
   Unterdrückung braucht eine Begründung an der Stelle.

## Projektspezifische Ergänzungen

`<TBD: Festlegungen des Projekts, zum Beispiel Benennungsschema, Sprache von Bezeichnern
und Kommentaren, verbotene Muster, Formatierer als Quelle der Wahrheit>`
