# 7a Client Packs: die Abbildungsschicht

## 7a.1 Das Problem, das diese Schicht löst

Ein Framework, dessen Datenschutz- und Sicherheitszusagen bei einem KI-Client von der Engine erzwungen werden und bei einem anderen nur als Prosa im Prompt stehen, muss diesen Unterschied sichtbar machen. Sonst erzeugt es falsche Sicherheit – genau dort, wo es am meisten schadet.

Die Erstfassung dieses Frameworks bezeichnete ihre kanonische Ebene als werkzeugneutral, nannte aber an 63 Stellen die Laufzeitpfade genau eines Clients. Wer mit einem anderen Werkzeug installierte, las durchgehend Pfade, die bei ihm nicht existieren. Die **Abbildungsschicht** macht diese Bindung explizit und austauschbar.

Ein **Client Pack** beantwortet für genau einen Client zwei Fragen:

1. **Wohin** gehören die Laufzeitartefakte – Wurzel-Anweisungsdatei, Regeldateien, Skills, Berechtigungen, Hooks, Subagentenprofile?
2. **Welche Zusagen setzt dieser Client technisch durch** – und welche bleiben eine Anweisung, der das Modell folgen kann oder auch nicht?

Die zweite Frage ist der eigentliche Grund für die Schicht.

## 7a.2 Keine Regelebene

Die achtstufige Prioritätshierarchie (Kap. 7) bleibt **unverändert**. Ein Client Pack führt keine Verhaltensregel ein, lockert keine bestehende und steht in keiner Konfliktbeziehung zu Core, Overlay oder Packs. Es übersetzt die Ebenen 3 bis 7 in die Artefakte eines konkreten Clients und dokumentiert die Durchsetzungstiefe. Entsteht ein Widerspruch zwischen einem Client Pack und der kanonischen Langform, gilt die Langform; das Pack wird korrigiert.

{{EMBED-RAW:leitwerk-core/clients/README.md:1}}
## 7a.3 Die Fähigkeitsmatrix

Kern jedes Client Packs. Sie stuft jede der 26 technischen Zusagen des Frameworks in eine von drei Klassen ein – `[TECHNISCH]` (die Engine erzwingt sie), `[TEXTUELL]` (nur Anweisung im Kontext) oder `[NICHT ABBILDBAR]` – und macht damit messbar, was zuvor Behauptung war.

Sechs dieser Zusagen sind **Kernzusagen** (B1 bis B6) und entsprechen dem Integritätsblock der Berechtigungsdatei. Weicht eine von `[TECHNISCH]` ab, ist sie im Pack einzeln zu begründen, im Overlay als Ausnahme zu führen und durch `<SECURITY_CONTACT>` freizugeben.

Dieses Dokument verwendet `devin-desktop` als durchgehendes Beispiel; seine Matrix steht in Kap. 15.1. Zum Vergleich das zweite Pack – derselbe Kern, ein anderer Client:

{{EMBED-RAW:leitwerk-core/clients/claude-code/CLIENT_PACK.md:1}}
Der Vergleich beider Matrizen ist die Probe aufs Exempel: Beide Packs bilden alle sechs Kernzusagen `[TECHNISCH]` ab. Ein Vergleich der Gesamtzahlen trägt allerdings nicht: Bei `devin-desktop` sind 24 von 34 Zusagen als `[TECHNISCH]` **vorgesehen**, und nur fünf Zeilen sind in einer Sitzung beobachtet; bei `claude-code` sind es nach AP2 25 von 29, und keine steht mehr auf `[NICHT ABBILDBAR]` – dafür ist dort keine Zeile in einer Sitzung beobachtet. Die Zahlen messen bis zum Abschluss von AP2 Verschiedenes. Die Matrizen sind seit 0.26.0 unterschiedlich lang, weil `devin-desktop` fünf Zusagen mehr führt, die nur dort einen Mechanismus haben.

## 7a.4 Form und Semantik

Ein Client Pack enthält vier Dateien. Alles Übrige liegt einmal im Kern und wird bei der Installation übersetzt. Dabei sind zwei Fälle zu unterscheiden, und der Unterschied ist wesentlich:

**Formtransformation.** Der Inhalt ist derselbe, nur die Schreibweise unterscheidet sich – ein Frontmatter-Feld heißt anders, eine Werkzeugliste ist kommagetrennt statt eingerückt. Das betrifft Regeltexte, Wurzel-Anweisung, Agentenprofil, Skills und die Vorlagen.

Die Ladebedingung einer Regel ist dagegen **keine** Formfrage, sondern eine zweite Semantikabbildung (D-27): Die Kernquelle kennt fünf Ladetrigger, ein Client kennt seine eigene Bedingungssprache. Bei `claude-code` heißt sie `paths` und bindet eine Regel an Glob-Muster; `always_on` und `model_decision` bilden dort auf unbedingtes Laden ab – eine Verschärfung. Ein Ladetrigger ohne Eintrag in der Abbildung lässt die Installation scheitern; er wird nicht verworfen.

**Semantikabbildung.** Die Werkzeuge selbst unterscheiden sich. Ein Client trennt Ändern und Anlegen in zwei Werkzeuge, ein anderer nicht; Befehlsverbote greifen hier wörtlich (`Exec(git reset --hard)`) und dort präfixbasiert (`Bash(git reset:*)`); Netzzugriff ist einmal ein Werkzeug mit Muster und einmal zwei ohne. Das betrifft Berechtigungen und Hooks – und damit genau die Regeln, an denen die Kernzusagen hängen.

Für den zweiten Fall genügt Sorgfalt nicht. Eine beim Nachziehen vergessene Regel wäre eine stille Lücke, während die Fähigkeitsmatrix weiterhin `[TECHNISCH]` behauptet. Die Abbildung erzwingt deshalb drei Eigenschaften und bricht die Installation ab, wenn eine verletzt ist:

| Zusicherung | Warum |
|---|---|
| Keine `deny`- oder `ask`-Regel ohne Zielwerkzeug beim Client | Sie wegzulassen wäre eine Lockerung. Bei `allow` ist Weglassen zulässig – es fällt auf den strengeren Standard zurück |
| Die Präfixform eines Befehlsverbots muss ein Präfix der wörtlichen Form sein | Damit ist die Präfixform nachweislich mindestens so breit; die Abweichung ist belegbar eine Verschärfung |
| Bei `allow` müssen wörtliche und Präfixform übereinstimmen | Dort wäre jede Verbreiterung eine Lockerung |

Der Integritätsblock der Berechtigungsdatei wird aus derselben Quelle erzeugt; der Validator gleicht die installierte Datei dagegen ab. Eine entfernte Kernregel fällt dadurch auf, auch wenn das Projekt zugleich die Integritätsliste gekürzt hat.

Die werkzeugneutrale Regelmenge, aus der beide Packs entstehen:

{{EMBED:leitwerk-core/framework/runtime/permissions.json:json}}
## 7a.5 Was das für ein Projekt bedeutet

Die Wahl des Client Packs fällt bei der Erstinstallation (`install.py --client`) und wird im Overlay dokumentiert. Sie ist keine Geschmacksfrage: Bevor ein Pack in Betrieb geht, ist seine Fähigkeitsmatrix zu lesen und jede Kernzusage ohne technische Durchsetzung freizugeben. Ein Wechsel des Clients ist ein eigener Vorgang mit erneuter Bewertung – nicht ein Schalter.

Für ein weiteres Client Pack ist Roadmap-AP2 mit der Fähigkeitsmatrix des neuen Packs zu wiederholen. Solange dessen Zielversion nicht festgelegt und geprüft ist, gilt das Pack als **unbelegt**.
