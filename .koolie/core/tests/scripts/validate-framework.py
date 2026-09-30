#!/usr/bin/env python3
"""
validate-framework.py – Strukturelle Validierung des Frameworks und eines Project Overlays.

Aufruf (im Wurzelverzeichnis des Repositorys):
    python3 .koolie/core/tests/scripts/validate-framework.py [--strict-overlay]
        [--check-overlay-ready] [--mermaid] [--root PFAD]

Prüft (statisch, ohne laufenden KI-Client):
  1. Pflichtdateien und -verzeichnisse
  2. Berechtigungsdatei: gültiges JSON, Kernregeln vollständig (Abgleich gegen die
     Kernquelle framework/runtime/permissions.json), keine Kernverbote in allow
  3. weitere JSON-Dateien der Laufzeitschicht (Hooks, mcp-Vorlage): gültiges JSON
  4. .devin/rules/*.md: Frontmatter (description, trigger, globs), Zeichenlimits
  5. Skills (.devin/skills/ und die Quellablagen der Packs): Pflichtdateien, Frontmatter,
     Metadatenblock, Pflichtabschnitte,
     Trigger-Regel (schreibende Skills nur user-getriggert), Beispiele und Testfälle
  6. Verbotene Inhalte (ohne erzeugte Lockdateien): Secret-Muster – dieselben Kategorien,
     die der Schutz-Hook in einer Werkzeugeingabe blockiert –, E-Mail-Adressen, IP-Adressen,
     interne Hostnamen, URLs außerhalb der Quellen-Allowlist, projektspezifische Sperrbegriffe
     (.koolie/project-overlay/forbidden-terms.txt)
  7. Platzhalter: nur registrierte Platzhalter (.koolie/core/docs/PLACEHOLDER_REGISTRY.md)
  8. Overlay-Manifest: Kopfschlüssel, Pflichtfelder je Dokumenteintrag, Aufzählungswerte;
     seit 1.6.0 auch, dass `path` und – bei `load: rule` – `rule_file` existieren (D-360)
  9. --strict-overlay: der **aktive** Zustand - keine offenen <TBD> in
     sicherheitsrelevanten Overlay-Feldern; Status aktiv an *jeder* Stelle, an der das
     Overlay ihn erklärt (Steckbrief und Aktivierung)
 9a. --check-overlay-ready: die **Aktivierungsreife eines Kandidaten** - derselbe Inhalt,
     aber der Status ist noch nicht aktiv und an allen Stellen gleich. Ohne diese Pruefung
     verlangte der dokumentierte Ablauf, was er herstellen sollte (B08, D-57)
 10. --mermaid: Syntaxprüfung aller Mermaid-Blöcke mit mmdc (falls installiert)
 11. Codeblöcke mit vier oder mehr Backticks (brechen die Dokumentassemblierung) –
     einschließlich der Quellen unter <CORE_DIR>/build/doc, aus denen sie entsteht
 12. Querverweise (FW-KO-04): Markdown-Links und in Backticks genannte Framework-Pfade
     zeigen auf existierende Dateien oder Verzeichnisse
 13. Versionskette (FW-VN-01): Overlay-Version an allen drei Ablageorten gleich, Steckbrief-
     angabe zur kompatiblen Framework-Version passend zu <CORE_DIR>/VERSION, und das
     Versionsfeld jedes Kernartefakts in der Form MAJOR.MINOR.PATCH
 14. Clientname im Kern (D-02, D-28, D-129): Der Kern nennt keinen Client - weder als
     Handelnden noch als Produkt, und kein Platzhalter traegt den Namen. Die Namen
     stammen aus den Pack-Kennungen, die Ausnahmen aus NEUTRAL_AUSNAHMEN (dieselbe
     Menge wie Pruefung 48). Bis 0.57.0 war der Produktname MIT ZUSATZ zulaessig; die
     Ausnahme hatte in ihrem Geltungsbereich keinen einzigen berechtigten Fall -
     fuenfzehn Fundstellen in zwoelf Traegern, jede mit einer Aussage ueber das Produkt
 15. Hook-Interpreter (AP2-CC-13, D-29): Der Interpreter der Hook-Aufrufe startet auf
     dieser Maschine wirklich Python. Geprueft wird die Wirkung, nicht die Anwesenheit
     des Namens - unter Windows ist 'python3' haeufig ein Alias ohne Interpreter
 16. Hook-Abdeckung (AP2-CC-16, D-30): Der Schutz-Hook erkennt jeden Werkzeugnamen,
     den ein Client Pack in hook_tools abbildet. Geprueft durch Aufruf mit einer Sonde,
     die er blockieren muss - ein Listenvergleich belegt Uebereinstimmung, nicht Wirkung
 17. Fail-closed (D-31): Der durchsetzende Hook verhaelt sich so, wie das Pack es zusagt -
     geprueft am Skript und an der erzeugten Konfiguration, nicht am Manifestfeld
 18. Hook-Ablageort (D-32): keine verwaiste Hook-Datei neben der wirksamen, und keine
     root-template-Vorlage, die eine solche Datei als geliefertes Artefakt fuehrt
 19. Quellenauskunft (D-34, D-37): Jedes Client Pack fuehrt den Abschnitt
     "Anweisungs- und Konfigurationsquellen ausserhalb des Projekts", mit mindestens einer
     Quellenzeile oder einem datierten Abwesenheitsbeleg. Belegt Anwesenheit, nicht
     Richtigkeit - siehe Kopfkommentar der Pruefung
 20. Dokumenttabellen (CR-2026-036): Die Client-Spalten von PLACEHOLDER_REGISTRY.md und
     RUNTIME_GLOSSARY.md stimmen je Pack mit dessen manifest.json ueberein. Belegt
     Uebereinstimmung, nicht Richtigkeit; seit 1.14.0 hat jedes Pack eine Spalte (D-421)
 21. Hook-Skripte (D-30, CR-2026-037): Ein Hook-Skript des Kerns leitet seine Pfade nicht
     aus einer clientgebundenen Umgebungsvariablen oder Laufzeitschicht ab; es bekommt sie
     als Argumente aus der Semantikabbildung
 22. Importsteuerung (D-37): Die installierte Berechtigungsdatei fuehrt sie so, wie das
     Manifest sie abbildet. Belegt Anwesenheit und Uebereinstimmung, nicht Wirkung -
     die Benutzerkonfiguration der Arbeitsstation hat Vorrang (K-27)
 23. Normative Kommentare (D-38): kein normatives Schluesselwort in einem HTML-Kommentar
     der Laufzeitartefakte - ein Kommentar erreicht nicht jede Sitzung (ERH-01, K-28)
 24. Regelablage (D-36): In der Vorlage der Regelablage liegt nur, was dem Nummernschema
     der Regeltexte folgt; erklaerender Text steht in der Laufzeit-README eine Ebene hoeher
 25. Ausfall mit Ersatz (D-41): Eine Matrixzeile eines Client Packs auf [NICHT ABBILDBAR]
     benennt den Ersatz - oder haelt ausdruecklich fest, dass es keinen gibt
 26. Werkzeugabwesenheit (D-47): Eine erklaerte Abwesenheit in hook_tools_absent ist
     belegt und folgerichtig - sie darf keine Werkzeugklasse aus der Durchsetzung nehmen
 27. Zusagenfelder (D-50): Verwirft ein Pack das Skill-Frontmatter-Feld permissions oder
     triggers, benennt es den Ersatz - ein zusagentragendes Feld entfaellt nicht ersatzlos
 28. Lesesperre gegen Schreibsperre (D-55, B07): Die Deklaration von <EXCLUDED_PATHS>
     nennt keinen Strukturpfad des Frameworks. Diese Pfade sind schreibgeschuetzt, nicht
     lesegesperrt - als Ausschluss erzeugen sie eine Lesesperre auf die eigenen Regeln
 29. K3-Kategorien (D-52, B09): Kurzform, Langform, Laufzeitregel, Entscheidungsbaum und
     Checkliste fuehren dieselben acht Kategorien, und keine traegt eine Bedingung
 30. Grenzfaelle (B07, B09): Die Grenzfalltabelle ist vollstaendig, jede Spalte gefuellt,
     jede entschiedene Auslegungsfrage durch mindestens einen Grenzfall gedeckt
 31. Durchsetzungstiefe (D-60): Die Summen der Fachmatrix eines Client Packs sind aus ihr
     ausgerechnet - Zeilenzahl und Anzahl je Einstufung. Eine Zeile zaehlt bei ihrer
     schwaechsten Einstufung; eine Kanalgrenze ist keine technische Durchsetzung (D-47)
 32. Hook-Eingabeschema (D-62, B06): Der Schutz-Hook wird mit dem VOLLSTAENDIGEN
     Umschlag jedes aufgezeichneten Schemas aufgerufen, nicht mit selbst gebauter
     Eingabe - und er darf an einem Feld des Umschlags nicht haengenbleiben
 33. Werkzeugsperre je Skill (D-64 bis D-66): Die erzeugte Fassung bildet
     permissions.deny ab, und kein Eintrag traegt ein Argumentmuster - ein solcher
     wirkt gemessen LAUTLOS gar nicht
 34. Startwerkzeug fuer Unteragenten (D-70): Ein Pack nennt es in agent_start_tools
     oder erklaert seine Abwesenheit ausdruecklich; wer Zeile A1 ohne offenen
     Beleg zusagt, muss nennen statt erklaeren. Der Vorbehalt steht seit 0.87.0
     auf der Nachfolgeform BELEG OFFEN - die Markerform ist abgeschafft (D-291)
 35. Agentenprofil ohne Startwerkzeug (D-73): Weder agent_frontmatter.tool_names
     bildet eines ab, noch nennt ein ausgeliefertes Profil eines. Eine Verankerung -
     sie faengt heute nichts
 36. Zellen des Decision Logs (D-75): Jede Tabellenzeile fuehrt so viele Zellen wie
     der Kopf ihrer Tabelle; ein maskierter Strich zaehlt als Inhalt
 37. Berechtigungskoerbe (D-77): Die drei Koerbe der installierten Datei werden gegen
     die aus der Kernquelle erzeugte Regelmenge gehalten. Fehlen ist immer ein Fehler,
     Ueberzaehliges nur in ask und allow; ein gefuellter Befehlsschlitz traegt das
     Praefixzeichen des Clients nicht
 38. Werkzeugabbildung des Frontmatters (D-78 bis D-80): Jedes Verb des
     Frontmatter-Vokabulars ist je Pack abgebildet oder ausdruecklich als nicht
     abgebildet erklaert; die Sperrliste hook_tools ist fuer kein Verbpaar enger als
     die Vorabfreigabe tool_names; keine Quelle nennt ein Verb ausserhalb des Vokabulars
 39. Vorabfreigabe des Skillaufrufs (D-81 bis D-84): Jeder ausgelieferte Skill des
     Kerns hat genau eine allow-Regel und jede Regel nennt einen ausgelieferten Skill;
     kein Musterzeichen in einer Skill-Regel - gemessen gaebe es lautlos nichts frei;
     die Skillwahl steht an allen vier Regeltraegern
 40. Register des Pruefapparats (D-85, D-86): Dieses Register ist lueckenlos und endet
     bei der hoechsten Nummer, die die beiden Pruefskripte nennen; die Sondenmenge steht
     im Satz darunter, im Kopfsatz von probe-pruefungen.py und in FW-KO-01 in derselben
     ausgerechneten Schreibweise; die Grenzfallanzahl in FW-KO-05 ist die gezaehlte
 41. Abwesenheitsbeleg (D-88): Eine erklaerte Werkzeugabwesenheit weist sich als
     Enthaltung aus oder belegt sich mit Datum und Fundstelle - eine blosse Behauptung
     nimmt eine Werkzeugklasse aus der Durchsetzung und begruendet es
 42. Schlitzinhalte (D-90, D-91): Ein gefuellter Befehlsschlitz der Berechtigungsdatei
     traegt den Befehl, den Abschnitt 5 oder 6 des Overlays fuer seinen Platzhalter
     erklaert; ein Schlitz ohne erklaerten Befehl deckt keinen Ueberschuss. Geprueft
     werden die drei BEFEHLSSCHLITZE, nicht die vier Pfadschlitze des deny-Korbs - die
     stehen dort, wo Ueberzaehliges ohnehin zulaessig ist, und ihr Vergleich waere n:1.
     Ohne Overlay enthaelt sie sich; fehlt dort ein Platzhalter, meldet sie es
 43. Hook-Block der Berechtigungsdatei (D-92): Fuehrt ein Pack seine Hooks dort - und
     beide ausgelieferten tun das -, traegt die Datei einen nichtleeren
     PreToolUse-Block. Eine Konfiguration in der eigenen Hook-Datei des Packs ist keine,
     weil der Client sie nicht liest; gemessen war der Hook eines Projekts so
     einunddreissig Releases lang stumm, bei 0 Fehlern im Lauf. Geprueft wird das
     VORHANDENSEIN - den Inhalt pruefen 15, 16 und 17
 44. Register der Uebungspraeparationen (D-93, D-131): Jede Kennung UEB-NN, die eine
     Vorbedingung des Testkatalogs oder eines dezentralen Testblatts nennt, steht im
     Register in onboarding/exercises/README.md - und jede registrierte Kennung wird von
     mindestens einem Testfall gebraucht. DRITTER GEGENSTAND seit 0.58.0: Jede
     registrierte Zeile fuehrt eine nichtleere Belegzelle. Sie gleicht ZWEI REGISTER ab,
     nicht ein Register gegen das Uebungsrepositorium: Das liegt ausserhalb dieses
     Repositoriums, und ob eine Praeparation dort wirklich liegt, sieht kein Validator
 45. Bytecode des Kerns (D-97): Die .gitignore des Projekts deckt __pycache__ ab,
     und unter <CORE_DIR>/ ist kein Bytecode versioniert. Zwei Gegenstaende, weil
     einer nicht reicht: git liest die .gitignore fuer bereits verfolgte Dateien
     nicht. Gegenstand 2 laeuft nur, wo git erreichbar ist - sonst sagt die
     Pruefung das als Warnung, statt stumm auszufallen. Gegenstand 3 (D-383), nur
     im Quellrepositorium: Die .gitignore schliesst jedes Wurzelerzeugnis aller
     Client Packs aus - abgeleitet aus shared_core und shared_seed der Manifeste
 46. Der 1.0.0-Stand (D-98, D-99): Die vier maschinell zaehlbaren Kriterien
     aus D-11 werden ausgerechnet und gegen die Standzeile in docs/ROADMAP.md
     gehalten - Markerfundstellen, offene Ergebniszellen, Modulstatus auf
     `entwurf`, Decision Records auf `entschieden (Vorschlag)`. Abweichung in
     BEIDE Richtungen ist ein Fehler. Am 2026-09-15 lagen alle vier Zahlen
     daneben, ohne dass eine je falsch geschrieben worden waere: Jede war das
     richtige Ergebnis einer Zaehlregel, die weniger kann als ihr Kriterium
     verlangt. Kriterium 5 zaehlt sie nicht - das ist eine Enthaltung.
     SEIT 0.87.0 IST KRITERIUM 1 EINE RUECKFALLSPERRE UND KEIN ARBEITSVORRAT
     (D-291): Die Markerform ist abgeschafft, die Zahl steht auf null, und was
     der Zaehler ab jetzt meldet, ist ihre WIEDEREINFUEHRUNG. Die Null ist
     gemessen und nicht konstruiert, und das ist belegt: Sonde 46c legt einen
     Marker in den Kern und verlangt die Meldung, Gegenprobe 46c legt einen in
     ein datiertes Protokoll und verlangt ihr Ausbleiben - beide bringen ihren
     Gegenstand SELBST mit und sind vom Schnitt nicht betroffen (D-23)
 47. Statusvokabular jedes Modultraegers (D-105, D-108): Jeder Steckbrief des Kerns
     fuehrt eine Statuszeile, und ihr Wert gehoert zum Vokabular aus
     08-skill-conventions.md Abschnitt 7. Der Ausfuellschlitz einer Vorlage gehoert
     ihr allein - in beide Richtungen. Bis 0.50.0 griff die Vokabularregel nur in
     einer SKILL.md, und der Modultraeger war ueber die Zeile definiert, die er
     tragen soll: Wer sie weglaesst, entkommt dem Lebenszyklus. Zwoelf taten es
 48. Werkzeugneutralitaet des Kerns (D-02, D-128): Kein anweisender Traeger des Kerns
     nennt einen Pfad oder Dateinamen, der genau einem Client Pack gehoert. Die Marken
     stammen aus den runtime_placeholders der Manifeste, nicht aus einer gepflegten
     Liste. Ausgenommen sind Chronik, Werkzeuge und die Abbildungstabellen; die
     Gattungen stehen in docs/RUNTIME_GLOSSARY.md. In tests/TEST_CATALOG.md steht die
     Regel nur vor der letzten Zelle - dort ist ein Pfad der Beleg einer Messung. Die
     Regel galt seit 0.31.0 und wurde von nichts durchgesetzt: Pruefung 12 liest nur
     Token in Backticks, meldet nur Pfade, die es NICHT GIBT, und fuehrte ihre eigenen
     Wurzeln clientgebunden. Siebzehn Fundstellen in vierzehn Traegern
 49. Ausdruecklicher Skill-Aufruf im Testkatalog (D-146): Nennt der Ausloeser eines
     Testfalls mit Pruefmethode `sitzung` einen Kernskill, dessen Quelle `triggers`
     ohne `- model` fuehrt, muss er ihn als `/name` nennen. Ein solcher Skill ist nur
     ueber den ausdruecklichen Aufruf einer Person erreichbar - das Client Pack
     `claude-code` bildet die fehlende Modellzulassung auf `disable-model-invocation`
     ab. Ein nicht-interaktiver Messlauf bekommt sonst eine Abweisung statt des
     Ablaufs, und der Testfall misst etwas anderes als seinen Gegenstand. Gemessen am
     2026-09-18 an `FW-SC-01`: Der Hauptlauf rief `fw-change-small` auf, wurde
     abgewiesen, arbeitete den Ablauf nicht nach - und damit fiel Schritt 3 des Skills
     aus, der die Verwender der geaenderten Einheit erhebt. Neun von zwoelf Skills
     betroffen, vier Fundstellen im Katalog
 50. Vollstaendigkeit des Klaerungspunktregisters (D-147): Jede im Kern genannte
     Kennung `K-NN` steht als Zeile im Register des Decision Logs. Ausgenommen sind
     allein die belegten synthetischen Kennungen des Pruefapparats; ihre Menge steht in
     dem Dokument, das die Regel traegt, und wird von dort abgeleitet. Am 2026-09-18
     fehlten zwei: `K-34` seit 0.32.0 in sieben Traegern (Stand vor der Behebung) - darunter ein Manifest und
     eine Faehigkeitsmatrix -, `K-55` von CR-2026-083 in drei Traegern als neu
     angekuendigt und nie eingetragen. Die Uebersicht der offenen Punkte war beide Male
     zu klein, und nichts hat es gemeldet
 51. Ausfuellschlitz fuer einen festgelegten Overlay-Wert (D-150): Traegt die
     Kontextquellentabelle der Overlay-Vorlage fuer ein Feld einen FESTEN Wert, darf die
     Overlay-Laufzeitfassung fuer dasselbe Feld keinen <TBD>-Schlitz fuehren. Die
     Feldmenge ist aus der Vorlage ABGELEITET. Eine Regel kann als Satz oder als Schlitz
     ausgedrueckt sein, und ein Sweep nach der Formulierung findet nur den Satz: 0.33.0
     hat die Domain-Ausnahme in sechzehn Traegern angefasst, davon acht anweisenden -
     darunter eine Datei im selben Verzeichnis; rules/20-project-overlay.md war nicht
     darunter, weil dort kein Satz stand. Die
     Laufzeitfassung bot dreiunddreissig Releases lang an, was ihre eigene Quelle
     ausschliesst (Grenzfall G-13)
 52. V6-Gegenstand mit Freigabefolge (D-151): In keiner anweisenden Fassung steht ein
     Gegenstand der V6-Zeile in einer Einheit, die zugleich `Kontrollstufe hoch` und eine
     Umsetzungsfreigabe traegt. V6 ist auch nach Freigabe nicht delegierbar; die
     Abgrenzung trennt Anwendungslogik vom Betrieb (D-53). Die Begriffe stammen aus der
     V6-Zeile selbst, ausgenommen ist die Langform, die sie traegt - sie MUSS beide
     Seiten nennen. Zwei Fassungen fuehrten beides in EINER Aufzaehlung, sechzig Releases
     lang (Grenzfaelle G-05 und G-06)
 53. Kriterium-2-Kette des Releaseplans (D-153): Was ein Posten des Releaseplans in
     docs/ROADMAP.md erreicht, ist der Ausgangswert des naechsten, und der letzte Wert ist
     null - Kriterium 2 muss dort ankommen. Sie beurteilt NICHT, ob eine Vorhersage
     stimmt; sie prueft, ob die Tabelle mit sich selbst uebereinstimmt. Das Protokoll zu
     0.56.0 hatte ausdruecklich entschieden, die Vorhersagen ungeprueft zu lassen - mit
     0.60.0 ist eingetreten, was eine Pruefung verhindert haette: Eine Zelle wurde aus
     einem Posten genommen, seine Zahl nachgezogen, die des Folgepostens nicht. Die Kette
     riss um eins und wurde so gemergt
 54. Zusatzschluessel auf der deklarierten Ebene (D-155): Jeder Schluessel aus
     settings_extra steht in der erzeugten Berechtigungsdatei auf der OBERSTEN Ebene,
     jeder aus permissions_extra INNERHALB von permissions - je mit dem deklarierten
     Wert. Ein Pack fuehrt beide Felder, notfalls leer: Der Unterschied zwischen "nicht
     abgebildet" und "gibt es nicht" gehoert deklariert, nicht aus einem fehlenden Feld
     erraten. Die Ebene ist keine Kosmetik - ein Schluessel auf der falschen Ebene wird
     stillschweigend nicht gelesen, und nichts meldet es. Anlass ist eine FREMDE Messung
     (FW-AK-01, CR-2026-087, 2026-09-18): Beim Client des Schwesterpacks ist genau diese
     Bauform als CVE-2026-81376 aufgetreten - der Restricted Mode setzte eine
     eingeschraenkte Arbeitsbereichseinstellung in gepunkteter Schreibweise durch und
     dieselbe in verschachtelter nicht. Behoben in 3.10.31 vom 2026-09-16; die
     verbindliche Zielspanne des Packs devin-desktop liegt vollstaendig davor
 55. Pflichtplatzhalter, gebunden statt ersetzt (D-160): ZWEI GEGENSTAENDE. (a) Jeder
     Platzhalter, den docs/PLACEHOLDER_REGISTRY.md als "Pflicht vor Aktivierung" fuehrt
     und im Overlay verortet, kommt in der Overlay-Vorlage mindestens einmal vor - sonst
     bietet die Vorlage ihn nie zum Ausfuellen an. (b) Unter --strict-overlay: Jeder
     solche Platzhalter, den ein Traeger der geladenen Laufzeitschicht NENNT, ist im
     aktiven Overlay GEBUNDEN, also dort beim Namen genannt. Ein Overlay, das den
     Platzhalter durch seinen WERT ERSETZT statt ihn zu binden, ist fuer sich stimmig und
     laesst jeden Kerntext unaufloesbar, der denselben Platzhalter traegt. Gemessen am
     2026-09-18 am Uebungsrepositorium: acht Pflichtplatzhalter ungebunden, davon fuenf
     mit zusammen 65 Fundstellen in der geladenen Schicht - <ISSUE_TRACKER> allein in
     vierzehn Traegern. Der Validator meldete 0 Fehler
 56. Kein ausgeschlossener Traeger als Vorbedingung (D-161): Keine Vorbedingung des
     Testkatalogs und keines Testblatts verlangt einen Traeger, den dasselbe Overlay
     unter <EXCLUDED_PATHS> fuehrt - weder lesen noch aendern. Aufgeloest wird ueber die
     Bindungszeile des genannten Platzhalters. Gemessen am 2026-09-18: SK-012-P01
     verlangt <MR_TEMPLATE_PATH>, und dessen Wert liegt unter .github/**, das im selben
     Overlay ausgeschlossen ist; drei weitere Zellen erben es ueber "wie P01"
 57. Kein ungebundener Pflichtplatzhalter als Vorbedingung (D-166): Keine
     Vorbedingung des Testkatalogs und keines Testblatts verlangt einen Pflichtplatzhalter
     als NICHT GESETZT oder UNGEBUNDEN. Sie ist die Kehrseite von 55b: Was 55b im aktiven
     Overlay als Fehler meldet, darf eine Testzelle nicht als Vorbedingung fordern - sonst
     stehen eine Pruefung und ein Testfall desselben Repositoriums gegeneinander, und der
     Testfall ist nur in einem Baum fahrbar, den der Validator beanstandet. Gemessen am
     2026-09-18: RE-001-N09 verlangte das Uebungs-Overlay "ohne gesetztes
     <ISSUE_TRACKER>", und Pruefung 55b war im SELBEN Release entstanden. Gegen den Skill
     gehalten trifft die Zelle etwas anderes: role-re-ticket nennt den Fall
     "<ISSUE_TRACKER> unbekannt", also Bindung OHNE Wert - ein Ausfuellschlitz, kein
     fehlender Platzhalter. Der Zuschnitt arbeitet auf TEILSAETZEN, nicht auf Zellen: Eine
     Vorbedingung, die den Platzhalter in einem Teilsatz fordert und in einem anderen eine
     Verneinung traegt, ist zulaessig. Die Pflichtmenge wird aus dem Platzhalterregister
     ABGELEITET, nicht gepflegt
 58. Vollstaendigkeit des Decision-Record-Registers (D-169): Jede im Kern genannte
     Zeichenfolge `D-` mit folgender Ziffer ist eine Kennung der Form D-NNN, und sie
     steht als Zeile im Register des Decision Logs. Ausgenommen sind allein die belegten
     synthetischen Kennungen des Pruefapparats - dieselbe Menge und derselbe
     Ableitungsweg wie bei Pruefung 50. Sie ist deren Schwester eine Kennungsfamilie
     weiter: Pruefung 50 gilt fuer K-, und ihr Muster wuerde den gemessenen Fall auch
     dann nicht treffen, wenn man es auf D- umstellte. Gemessen am 2026-09-18: Die
     Registereintraege der Pruefungen 55 und 56 verwiesen seit 0.63.0 auf zwei Kennungen
     mit einem PLATZHALTER statt einer Zahl; die Meldungen derselben Pruefungen nannten
     die richtigen. Zwischen Ziffer und Platzhalter steht keine Wortgrenze - eine
     Kennung, die die Form knapp verfehlt, ist fuer jeden Zaehler unsichtbar
 59. Der Overlay-Wert in der Schicht, die ihn durchsetzt (D-171): Unter
     --strict-overlay drei Gegenstaende. (a) Die Laufzeitfassung des Overlays NENNT
     <EXCLUDED_PATHS>, bindet ihn also, statt seinen Wert einzusetzen - das ist 55b eine
     Schicht tiefer. (b) Die Zeile, die ihn nennt, traegt dieselbe Globmenge wie die
     Bindungszeile des Quell-Overlays; massgeblich ist die Quelle. (c) Jeder Glob der
     Quelle hat im deny-Korb der Berechtigungsdatei eine Lese- UND eine Schreibsperre.
     ANLASS: 0.63.0 hat die Sperre eines Overlays von .github/** auf .github/workflows/**
     eingeengt, weil sie sonst die Merge-Request-Vorlage mitsperrt (D-161). Die Einengung
     steht in der QUELLE; die beiden Traeger, die den Client wirklich binden, tragen
     weiterhin den alten, weiteren Wert - unveraendert seit dem ersten Commit jenes
     Repositoriums. Pruefung 56 sah es nicht, weil sie ueber die Bindungszeile der Quelle
     aufloest; 55b nicht, weil sie die BINDUNG prueft und nicht den WERT; --strict-overlay
     nicht, weil es allein den Status vergleicht (CR-2026-044 E4). GRENZE: geprueft wird
     EIN Platzhalter - der einzige mit maschinell vergleichbarer Wertgestalt, der
     zugleich zwei Schichten bindet. Und (c) prueft nur die Richtung Quelle -> Korb:
     Ueberzaehliges bleibt zulaessig, wie schon bei Pruefung 42

 60. Der Befehlsschlitz, den der Ausloeser braucht (D-178): Eine sitzung-Zelle, deren
     Ausloeser einen Skill als /name aufruft, dessen Frontmatter einen Befehlsschlitz
     AUSFUEHRT (Exec(<..._COMMAND>) unter permissions), nennt diesen Schlitz in ihrer
     VORBEDINGUNG. ANLASS: FW-SC-01 ist am 2026-09-18 zum dritten Mal gefahren worden
     und zum dritten Mal nicht abnehmbar gewesen - der Lauf hat NICHTS geaendert, weil
     fw-change-small den Testbefehl VOR dem ersten Schreibzugriff verlangt und der
     Befehl im Messbaum im ask-Korb stand; ask ist nicht-interaktiv eine Abweisung
     (D-134). Derselbe Fehler kostete FW-PO-02 einen Durchgang. GRENZE: Geprueft wird
     die NENNUNG des Schlitzes, nicht die Aussage darueber - die Pruefung faengt das
     Vergessen, nicht den Irrtum. Und sie gilt nur fuer sitzung-Zellen
 61. Das Pruefmittelwort stammt aus dem Vokabular (D-181): Das erste Wort der Spalte
     Pruefmethode ist skript, sitzung oder review - im zentralen Katalog und in den
     dreizehn Testblaettern. ANLASS: Die Blaetter fuehrten bis 0.67.0 das Wort manuell,
     87 von 87 Zellen. Es steht in keinem Vokabular; es ist das ADJEKTIV aus der
     Definition von sitzung, zum Methodennamen befoerdert, und jedes Blatt erklaerte es
     im eigenen Vorspann. Die Pruefungen 49 und 60 laufen ausdruecklich ueber die
     Blaetter und filtern auf sitzung - beide hatten dort NULL Gegenstand. Nach der
     Umstellung meldete Pruefung 60 sofort ZWANZIG Zellen. GRENZE: Geprueft wird das
     erste Wort gegen eine feste Menge; ein Zusatz dahinter bleibt zulaessig. Nicht
     geprueft wird, ob das Wort das RICHTIGE ist
 62. Version der Ausgabevorlage (D-185): Keine SKILL.md nennt eine Versionsnummer
     woertlich. Die Ausgabevorlage verweist auf den Steckbrief ("v<Version aus dem
     Steckbrief>"), und der Client setzt sie beim Rendern ein. ANLASS: Gemessen am
     2026-09-19 im ersten Buendellauf - dreizehn Traeger fuehrten eine woertliche
     Version, ZEHN davon eine andere als ihr eigener Steckbrief. Die drei, die
     uebereinstimmten, sind die drei, deren Version seit der Erstfassung nicht
     gestiegen ist: Die Uebereinstimmung war Stillstand, nicht Pflege. Gefunden hat es
     ein gemessener Lauf selbst, in einer Nebenbemerkung seines Ergebnisberichts
 63. Der Nummernverweis, der ins Leere zeigt (D-193): Nennt ein anweisender
     Traeger des Kerns eine Datei und dahinter `Abschnitt N` oder `Abschnitt N.M`,
     fuehrt das Ziel eine Ueberschrift mit genau dieser Nummer. ANLASS: Der
     Vorbedingungsdurchgang von Buendel 2 hat gemessen, dass drei Zellen eine
     Bereinigung "nach 02-privacy.md Abschnitt 3.3" erwarten - und dass Abschnitt 3
     jener Datei zehn nummerierte REGELN fuehrte und keine einzige Unterueberschrift.
     Gegen den unberuehrten Vorstand: 30 Verweise in 15 anweisenden Traegern auf vier
     Nummern, die es als Abschnitt nicht gab. Dieselbe Form bedeutete in DERSELBEN
     Datei zweierlei - `Abschnitt 2.1` war eine Ueberschrift. Aufzeichnungen sind
     ausgenommen (D-141); ihre Liste ist keine neue, sondern NEUTRAL_CHRONIK
 64. Die Ausgabemarke, die der Skill nicht verlangt (D-197): Nennt die Spalte
     Erwartetes oder Unzulaessiges Verhalten einer Zelle eine Ausgabemarke
     ([HALT], [RUECKFRAGE]), fuehrt der im Ausloeser aufgerufene Skill sie in
     Abschnitt 5 (Ausgabeformat) oder Abschnitt 6 (Qualitaetskriterien). ANLASS:
     Ausgezaehlt am 2026-09-19 nach dem ABSCHNITT, in dem die Marke steht -
     [RUECKFRAGE] steht in KEINEM Abschnitt 5 und KEINEM Abschnitt 6 der zwoelf
     Skills und ist durchgehend Handlungsmarke; [HALT] ist Ausgabemarke in genau
     dreien. 18 Nennungen in 17 Zellen verlangten mehr, als ihr Skill vorschreibt,
     und ein gemessener Lauf hatte es vorgefuehrt: sk004n01 schrieb [HALT] und
     [RUECKFRAGE] nicht - richtig, denn nur die erste ist verlangt. GRENZE:
     Geprueft wird die Deckung, nicht die Formulierung; die LETZTE Zelle ist
     Ergebnisstatus und damit Aufzeichnung (D-117), dieselbe Spalten-Ausnahme wie
     bei Pruefung 48
 65. Der Ergebnisstatus ohne Beleg (D-202): Ein Ergebnisstatus ausserhalb von
     `offen` nennt ein Protokoll unter tests/protocols/, und bei Pruefmethode
     `sitzung` zusaetzlich das gemessene Client Pack mit Produktversion (D-117).
     Das Statuswort selbst stammt aus dem Vokabular von TEST_CATALOG.md Punkt 4 -
     abgeleitet aus jener Zeile, nicht gepflegt. ANLASS: Punkt 4 sagt "Ein
     Ergebnisstatus ausser `offen` MUSS auf ein Protokoll verweisen", D-117
     verlangt Pack und Version - und keine der vierundsechzig Pruefungen setzte es
     durch. Gezaehlt am 2026-09-19 ueber alle 125 Ergebniszellen: NULL Verstoesse,
     die Regel trug allein durch Sorgfalt. Gebaut wird sie in dem Release, das
     achtzehn neue `bestanden` in einem Zug eintraegt. GRENZE: Geprueft wird die
     NENNUNG, nicht ihre Richtigkeit - ein Verweis auf das falsche Protokoll und
     eine Version, die nicht die gemessene ist, laufen durch
 66. Das verirrte Steuerzeichen (D-217): Kein Textraeger traegt einen
     Wagenruecklauf ohne folgenden Zeilenvorschub. Er ist im Text unsichtbar - und
     er nimmt git die Normalisierung der Zeilenenden: Ein Traeger mit einem
     einzelnen CR gilt als BINAER und wird weder von core.autocrlf noch von einem
     text=auto einer .gitattributes angefasst. ANLASS: Der Nachtrag zur Uebergabe
     vom 2026-09-20 setzte ein echtes CR dorthin, wo die zwei Zeichen einer
     Escape-Folge gemeint waren - in genau dem Satz, der den CRLF-Befund von 0.78.1
     beschreibt. Der Blob stand danach auf CRLF gegen 426 von 440 LF-Traegern, und
     der Commit schrieb 1981 von 1983 Zeilen neu. Ausgezaehlt ueber den Bestand: 14
     Traeger mit verirrtem CR - und genau diese 14 sind die 14, die git nicht
     normalisiert hat, die Deckung ist vollstaendig. 🔴 KEINE DER 65 AELTEREN
     PRUEFUNGEN KONNTE ES SEHEN: `read` oeffnet im Universal-Newline-Modus, dort ist
     jedes CR schon ein Zeilenvorschub, bevor eine Pruefung hinsieht. Diese liest
     Bytes. GRENZE: Gemessen wird das Zeichen, nicht die Zeilenende-Form eines
     Traegers - welche Form gilt, entscheidet kein Validator (K-81)
 67. ENTFALLEN mit 1.4.1 (D-350). Sie hielt die Titelzeile der Uebergabe
     gegen <CORE_DIR>/VERSION und wies eine Merge-Request-Nummer ab (D-216).
     Seit 1.4.1 ist UEBERGABE.md ein lokales Arbeitsdokument und nicht mehr
     versioniert; eine frische Auscheckung fuehrt sie nicht, und eine Pruefung
     darauf liefe nur an einem Arbeitsplatz. Die Nummer bleibt stehen, damit
     das Register lueckenlos bleibt (Pruefung 40) und keine andere Pruefung
     sie erbt. PREIS, benannt: Stand und Zahlen der Uebergabe prueft seither
     niemand - sie sind wieder Zahlen, die gepflegt werden muessen
 68. Das Praefix, das mehr sperrt als sein Befehl (D-219): Jede exec-Regel in
     framework/runtime/permissions.json, deren `prefix` kuerzer ist als ihr
     `command`, traegt ein Feld `_uebererfasst` mit der Begruendung. ANLASS, und er
     ist gemessen: Der Eintrag { command: "git branch -D", prefix: "git branch" }
     nennt als Gegenstand das LOESCHEN eines Branches und sperrt ueber sein Praefix
     auch das blosse AUFLISTEN. Das erklaert alle 25 Abweisungen des Messtags vom
     2026-09-20 (23 von 50 Laeufen; elf davon tragen `git branch`) - und es macht zwei
     Skills eine Zusage unmoeglich, die sie in Arbeitsschritt 1 und in ihrer
     Fehlerbehandlung selbst vorschreiben: eine Kandidatenliste vorhandener
     Branches. Vier der 29 exec-Regeln erfassen ueber, und KEINE hat es bisher
     gesagt. 🔴 Der Waechter in clientmap.py prueft nur, ob das Praefix ein Praefix
     des Befehls IST - nicht, ob es mehr trifft. GRENZE, und sie steht hier:
     Geprueft wird die NENNUNG, nicht ihre Richtigkeit; eine Begruendung, die nicht
     traegt, laeuft durch. Dieselbe Enthaltung wie bei Pruefung 65
 69. Der Messapparat schreibt nicht in das Repositorium (D-222): In
     <CORE_DIR>/tests/erhebungen/ liegen Werkzeuge - Skripte und eine README -,
     sonst nichts. ANLASS, und er kostete nichts, weil er vor dem Lauf kam: D-222
     hat die Skripte mit 0.79.0 hierher geholt und ihre Belege ausdruecklich
     draussen gelassen; fuenf von ihnen legten ihre Belege aber neben SICH ab
     (os.path.dirname(os.path.abspath(__file__)) + "belege"). Solange sie daneben
     lagen, war das richtig - seither zeigt derselbe Ausdruck HINEIN, und lauf.py
     legt das Verzeichnis selbst an. Der Nachlauf haette seine Sitzungsmitschriften
     versioniert, ohne dass jemand es entschieden haette. Geprueft wird nicht der
     Quelltext, sondern das ERGEBNIS: eine Belegdatei oder Zustandsaufnahme an
     diesem Ort ist der Befund, gleich welcher Ausdruck sie erzeugt hat. GRENZE,
     und sie steht hier: Diese Pruefung sieht nur, was schon geschrieben IST; den
     Waechter davor traegt ablage.py, der die Erhebungsablage als Angabe verlangt
     und einen Pfad im Repositorium abweist
 70. Jedes Werkzeug des Kerns nennt nur Namen, die es gibt (D-229): Jede .py-Datei
     unter <CORE_DIR>/ laedt als Symboltabelle, und kein Name wird gelesen, der
     nirgends gebunden ist - weder als Zuweisung noch als Import, Parameter oder
     eingebauter Name. ANLASS, und er kostete nichts, weil er vor dem Lauf kam: Der
     Wiederaufnahmepunkt des Nachlaufs fuehrte stand-b4.py als Befehl 1 von 4. Das
     Skript brach beim Import mit NameError ab - zwei Vorkommen eines Namens S, der
     mit dem Umzug nach D-222 verschwunden war, weil er den Ablageort NEBEN dem
     Skript trug. Seit 0.79.0 war es damit tot, und keine der 69 Pruefungen sah es:
     Pruefung 45 prueft den Bytecode auf Abwesenheit, Pruefung 69 die ART der
     Dateien in der Erhebungsablage - dass eine davon LAEUFT, prueft keine.
     GRENZE, und sie steht hier: Geprueft wird der Name, nicht der Wert. Ein Modul,
     das einen Namen bindet und ihn falsch belegt, laeuft durch - dieselbe
     Enthaltung, die Pruefung 68 zur Begruendung sagt. Ein Lauf des Werkzeugs
     bliebe der staerkere Nachweis; er kostet Kontingent und legt Dateien an,
     diese Pruefung nicht
 71. Kein Traeger des Kerns nennt einen Arbeitsplatz (D-231): Ein absoluter Pfad in
     ein Benutzerprofil - C:\\Users\\<konto>, /home/<konto>, /Users/<konto> - wird
     gemeldet, sofern das Kontosegment kein Platzhalter ist und die Zeile keine
     Begruendung traegt. ANLASS, und er ist gemessen: Neun Werkzeuge des
     Messapparats fuehrten
     C:\\Users\\<konto>\\Documents\\devpacks\\test-devin-framework im Quelltext -
     mit dem Kontonamen einer natuerlichen Person. Solange der Apparat NEBEN dem
     Repositorium lag, stand das in einer unversionierten Ablage; mit D-222 ist er
     hineingewandert und hat den Pfad mitgebracht - in genau das Repositorium, fuer
     das 0.78.1 eigens UEBERGABE.local.md eingefuehrt hat, weil eine Uebergabe mit
     Servername und Konto den Validator mit drei Fehlern beantwortet. Keine der
     siebzig Pruefungen sah es: Pruefung 6 kennt Secret-Muster, E-Mail-Adressen,
     IP-Adressen und Hostnamen - keinen Benutzerprofilpfad. GRENZE, und sie steht
     hier: Aufzeichnungen sind ausgenommen - tests/protocols/ und
     governance/change-requests/ halten fest, WO gemessen wurde, und ein Protokoll,
     das man umschreibt, ist keines mehr (D-141). Zehn von ihnen tragen den
     Kontonamen weiter; was daraus folgt, ist als K-85 geführt und hier nicht
     entschieden
 72. Ein aktiviertes Pack steht auch im Berechtigungskorb (D-238): In einer
     Installation deckt sich die Skillablage des Client Packs mit den
     Namenseintraegen der Berechtigungsdatei - in beide Richtungen. ANLASS, und er
     ist gemessen: Der Messbaum von Buendel 5 trug nach der Aktivierung WORTGETREU
     nach framework/role-packs/README.md dreizehn Skillverzeichnisse und zwoelf
     Skill(...)-Eintraege; role-re-ticket fehlte, und der Validator meldete 0 Fehler.
     Ein nicht genannter Aufruf faellt in den Rueckfragekorb und im
     rueckfragefreien Betrieb in die Abweisung - die Sitzung liest die SKILL.md dann
     ersatzweise als Datei, OHNE die Werkzeugbeschraenkung des Skills (D-81).
     WARUM PRUEFUNG 39 ES NICHT SIEHT, obwohl sie dafuer gebaut ist: Sie haelt
     framework/runtime/permissions.json gegen framework/skills/ - Regelmenge des
     Kerns gegen Skills des Kerns, beides Ebene 3, und dort deckt es sich. Ein
     Packskill ist Ebene 6 und kommt in keiner der beiden Mengen vor. GRENZE, und
     sie ist deklariert: Die Schreibweise des Skillaufrufs steht je Client als
     permission_tools.skill im Manifest; ist sie leer (devin-desktop, D-89), schweigt
     die Pruefung - fehlt das FELD, meldet sie es (D-155)
 73. Jede [DOK]-Matrixzeile nennt ihre Quelle (D-263): In der Faehigkeitsmatrix
     jedes Client Packs nennt der BELEGKOPF jeder mit [DOK] belegten Zeile eine
     Quellenkennung der Liste in Anhang 31.4 (QC-n/QD-n/QK-n/QU-n); ein Verweisbeleg
     ("wie B3") wird aufgeloest. ANLASS, und er ist gezaehlt: Anhang 31.4 sagt
     ueber sich selbst, die massgebliche Zuordnung stehe je Zeile in der Matrix -
     das traf am 2026-09-18 fuer 14 von 43 Zeilen zu (K-62, D-156). DER PREIS IST
     GEMESSEN: Der Durchgang von FW-AK-01 musste alle 22 Quellen abrufen, weil ohne
     Zuordnung je Zeile nicht zu sagen ist, welche Seite welche Zusage traegt.
     DIE KOPFREGEL ist der Grund, weshalb die Pruefung ueberhaupt etwas sagt:
     Geprueft wird die Zelle bis zum ersten Satzbruch; was danach steht, ist
     Erlaeuterung. Ohne sie zaehlte jede NENNUNG der Marke mit - Zeile R5 des Packs
     claude-code erklaert, "ein Dokumentenabgleich belegt [DOK], nicht
     [TECHNISCH]", und das ist eine Aussage ueber die Marke, kein Beleg. Dieselbe
     Trennlinie, die der VERIFY-Marker am Ende braucht (CR-2026-070 E3).
     WARUM DIE KENNUNG UND NICHT DER SEITENPFAD: Nur die Kennung laesst sich gegen
     die Liste halten; ein Pfad kann eine Seite nennen, die die Liste nicht fuehrt.
     GRENZE, und sie ist deklariert: Gibt der Bestand keine Seite her, sagt die
     Zeile QUELLE NICHT ZUGEORDNET - geraten wird nicht, eine geratene Zuordnung
     saehe wie ein Beleg aus (D-156). Die zugelassenen Luecken stehen als MENGE in
     P73_OFFEN, in beide Richtungen geprueft: eine neue faellt auf, eine
     geschlossene ebenso
 74. Eine Matrixzeile steht in ihrer Tabelle (D-264): Zwischen einer Zeile der
     Faehigkeitsmatrix und der Trennzeile ihrer Tabelle liegt keine Leerzeile und
     kein Fremdtext. ANLASS, und er stand 73 Releases da: Das Pack devin-desktop
     fuehrt sieben Modus-Zeilen, und zwischen M5 und M6 stand seit 0.26.0 eine
     Leerzeile - eingefuegt von genau dem Release, das M6 und M7 anlegte, weil
     AP2-DD-03 gefunden hatte, dass zwei geregelte Modi keine Matrixzeile haben.
     Nach einer Leerzeile beginnt in Markdown ein neuer Block, und ein Block aus
     Datenzeilen ohne Kopf- und Trennzeile ist ein ABSATZ: Beide Zeilen erscheinen
     im Pack wie im Hauptdokument als Fliesstext mit Strichen. Die Zusammenfassung
     desselben Packs zaehlt sie dagegen mit ("20 von 36"). WARUM EINE EIGENE
     PRUEFUNG: 73 fragt, WAS in einer Zeile steht, 74, ob sie ueberhaupt eine ist -
     eine gebrochene Tabelle laesst 73 unberuehrt, weil sie die Zeile am Muster
     erkennt und nicht am Block. Genau deshalb hat es 73 Releases lang niemand
     gemerkt
 75. Kein Restbestand des alten Namens (D-271): Kein verfolgter Traeger nennt
     `leitwerk` in irgendeiner Schreibweise - ausser den DEKLARIERTEN Ausnahmen.
     ANLASS: Mit 0.88.0 heisst das Framework Koolie und der Kern liegt unter
     .koolie/core. Ohne diese Pruefung ist "der Name ist weg" eine Behauptung
     ohne Pruefung, und genau das ist der wiederkehrende Befundtyp dieses
     Repositoriums. ZAEHLBEREICH: jeder verfolgte Traeger, NICHT nur der Kern -
     die Lehre von D-295, wonach der Zaehlbereich von Kriterium 1 kleiner war
     als die Wirkungsflaeche. AUSGENOMMEN in drei Klassen, alle als MENGE:
     (a) die Chronik, die einen vergangenen Zustand beschreibt (D-273);
     (b) die Namen datierter Belegablagen ausserhalb des Repositoriums, die
     NICHT umbenannt werden, weil eine Reihe mit wechselnder Namenskonvention
     nicht mehr als Reihe auffindbar ist (D-300); (c) Aussagen UEBER den alten
     Namen, die ein Sweep ins Sinnlose kehrt (D-301). IN BEIDE RICHTUNGEN
     GEPRUEFT: eine neue Fundstelle faellt auf, eine leer gewordene Ausnahme
     ebenso. PREIS, benannt: Die Ausnahme gilt je TRAEGER, nicht je Zeile
 76. Die Lage des Kerns steht an vier Stellen - und ueberall gleich (D-299):
     clientmap.py, dieser Validator, der Schutz-Hook und ablage.py fuehren
     dieselbe Lageangabe, und KEINE leitet sie ueber os.path.basename ab.
     ANLASS: Bis 0.87.0 taten es alle vier, weil der Kern EIN Verzeichnis-
     segment war - in install.py mit dem Satz, die Zeile stehe dort, "damit
     eine spaetere Umbenennung nur eine Stelle beruehrt". Sie haette die
     Umbenennung nicht ueberlebt: basename(".koolie/core") ist "core". UND ES
     WAERE KEIN VALIDATORFEHLER GEWESEN - dieser Validator band denselben Wert
     auf dieselbe Weise und haette ihn bestaetigt. Zwei Stellen, die einander
     decken (0.57.0), ueber Werkzeuggrenzen hinweg. Der zweite Gegenstand
     traegt den ersten: Gleichheit allein waere erfuellbar, indem alle vier
     denselben Fehler machen
 77. Der Stand des Hauptdokuments (D-312): Die Zeile `| Dokumentversion | X.Y.Z
     (entspricht Framework-Release X.Y.Z) |` in build/doc/00-kopf.md nennt beide Male
     denselben Wert, und dieser Wert ist der aus <CORE_DIR>/VERSION. ANLASS: Das
     Hauptdokument stand am 2026-09-22 auf Dokumentversion 0.9.0 vom 2026-09-10 -
     ZWEIUNDVIERZIG Releases zurueck. Es behauptete dort "Alle Module im Status
     entwurf", waehrend seit 0.53.0 kein einziger Traeger darauf steht; es nannte
     einen Produktstand, den das Pack zwei Zielspannen weiter hinter sich gelassen
     hatte; und es fuehrte eine Client-Pack-Groesse, die seit 0.26.0 nicht mehr
     stimmte. KEINE dieser Zahlen war falsch geschrieben - alle waren bei ihrer
     Einfuehrung richtig und sind stehen geblieben, waehrend ihr Gegenstand weiterlief.
     Das ist die Bauform von Pruefung 40 an einem groesseren Gegenstand. ZWEI
     GEGENSTAENDE: (1) Der Anker - fehlt die Zeile, bestuende die Pruefung leise, und
     sie meldet sein Fehlen deshalb selbst (D-23). (2) Beide Werte gleich und gleich
     VERSION - die Gleichheit der beiden untereinander traegt den Vergleich mit
     VERSION, denn eine Zeile, die zwei verschiedene Staende nennt, laesst offen,
     welcher gemeint ist. PREIS, benannt: Jedes Release fasst diese Zeile an. Das ist
     derselbe Preis, den bis 1.4.0 Pruefung 67 fuer die Uebergabe verlangt hat,
     und er hat dort getragen. GRENZE: Sie misst die VERSION, nicht den INHALT. Ein Dokument, dessen
     Zahlen veralten, waehrend jemand die Versionszeile mitzieht, laeuft durch - was
     dagegen hilft, ist der Durchgang vor dem Commit und keine Pruefung.
 78. Die zaehlbaren Aussagen des Hauptdokuments (D-315): Der Satz ueber den
     Pruefapparat in build/doc/26-qs-test.md nennt die GEZAEHLTE Zahl der
     Pruefungen, der versionierten Dateien des Kerns und der Markdown-Dateien
     darunter. ANLASS: 0.89.0 hat das Dokument nach 42 Releases auf den Stand
     gesetzt und geschrieben, die Behebung brauche eine PRUEFUNG und nicht nur
     eine Textaenderung. Gebaut wurde Pruefung 77, und die misst die VERSION.
     EIN Release spaeter standen dort "76 Pruefungen ueber 502 versionierte
     Dateien, davon 450 Markdown" - richtig waren 77, 504 und 452, und die
     beiden fehlenden Dateien waren der Antrag und das Protokoll DESSELBEN
     Releases. ZUSCHNITT (D-318): nur die GEGENWARTSFORM. Datierte Zahlen in
     den ausgewiesenen Zeitdokumenten veralten nicht und werden nicht geprueft.
     Die Abnahmezeile der Uebergabe, seit 1.0.0 ihr zweiter Gegenstand (D-325),
     ist mit 1.4.1 entfallen (D-350)
 79. Die Lizenz liegt an zwei Stellen und ist dieselbe (D-317): LICENSE in der
     Wurzel (dort suchen die Hostingdienste sie) und <CORE_DIR>/LICENSE (dort
     wandert sie mit, wenn ein uebernehmendes Projekt den Kern als Ganzes
     kopiert) tragen byteweise denselben Inhalt, und dieser Inhalt ist die
     GPL-3.0. ANLASS: Zwei Stellen mit demselben Inhalt laufen auseinander,
     sobald eine angefasst wird - der haeufigste Befundtyp dieses
     Repositoriums, und die Antwort darauf ist dieselbe wie bei Pruefung 76
 80. Jedes Abnahmeprotokoll traegt seine Gegenzeichnung (D-319): Ein Protokoll
     des Testkatalogs (Dateiname JJJJ-MM-TT-FW-<Klasse>-<NN>.md) fuehrt einen
     Abschnitt `Gegenzeichnung` ohne offenes <TBD>. ANLASS: AP11 verlangte sie,
     und 0.89.0 hat sie als ABGRENZUNG stehen gelassen - eine Gegenzeichnung ist
     die Handlung einer ZWEITEN Rolle, und ein Werkzeug, das sie ausfuellt,
     faelscht sie. Die Folge hatte niemand benannt: An diesem Framework arbeitet
     EINE Person, die Pflicht war konstruktiv unerfuellbar - die Bauform der
     Regel mit leerer Schnittmenge an einer Governance-Regel. ZUSCHNITT: nur
     Abnahmeprotokolle. Gemessen ueber BEIDE Zaehlregeln ergibt der Gesamtbestand
     17/47/61 oder 13/45/64; die zehn Abnahmeprotokolle ergeben 3/2/5 unter
     beiden - ein Gegenstand, der unter zwei Regeln derselbe ist, ist der
     richtige. GRENZE: Sie verlangt eine Unterschrift und erzeugt keine. Die
     Zeile sagt, WAS gegengezeichnet wurde; der Commit sagt, WER
 81. Eine Zeilenendeform je Repositorium (D-320, schliesst K-81): Alle versionierten
     Texttraeger des Arbeitsbaums tragen DIESELBE Form, und keiner mischt beide in
     sich. ANLASS: Eine Sitzung hat 28 LF-Zeilen in einen durchgehenden CRLF-Bestand
     eingeschleppt; gefunden hat es keine der 80 Pruefungen, sondern ein Suchtext, der
     danach nicht mehr traf. Pruefung 66 prueft die GEGENRICHTUNG und greift nicht.
     🔴 UND DER AUSLOESENDE BEFUND WAR AM FALSCHEN GEGENSTAND GEMESSEN: "kein
     versionierter Traeger traegt reine LF" gilt fuer den ARBEITSBAUM (515 CRLF); im
     BLOB, also im Versionierten, liegen dieselben 515 auf reinem LF. Ursache ist
     core.autocrlf, eine Einstellung des Arbeitsplatzes - genau die Frage, die K-81
     seit 0.78.2 offen fuehrte. ZUSCHNITT: der Arbeitsbaum; den Blob setzt seit D-320
     die .gitattributes mit `text=auto`, und die aendert gemessen null Blobs. SIE
     SCHREIBT KEINE FORM VOR, sondern verlangt, dass es eine ist - Einheitlichkeit ist
     in jeder Installation richtig, eine bestimmte Form nur an einem Arbeitsplatz.
     GRENZE: Sie liest Bytes und misst den Arbeitsbaum; ohne Git-Bestand meldet sie
     eine Warnung und KEIN Messergebnis
 82. Die Bestandsliste steht auf dem Stand des Releases (D-331): Jede Zeile von
     governance/ADOPTION_REGISTRY.md nennt in der Spalte `Framework-Version` den
     Inhalt von VERSION. ANLASS: zweimal in zwei Releases. 1.0.0 hat die Liste
     angelegt, und ihr erster Eintrag war ihr erster Befund - beide uebernehmenden
     Projekte standen drei Releases zurueck; 1.0.1 hat es wiederholt. Ursache ist die
     REIHENFOLGE: Gehoben wurde nach dem Merge, und damit war FW-CL-11 Pruefpunkt 20
     zum Merge-Zeitpunkt nicht erfuellt. 🔴 UND SIE WAR AN ZWEI STELLEN FALSCH: Das
     Framework hatte seine Liste berichtigt, die AUSGELIEFERTEN Kopien in beiden
     Projekten trugen weiter den alten Stand - wer eine Liste nach dem Heben
     fortschreibt, schreibt sie an einer Stelle fort und liefert sie an zwei.
     D-299-PROBE BESTANDEN: In einem uebernehmenden Projekt sind Liste und VERSION
     byte-gleich aus demselben Release ausgeliefert, also gleich - auch mehrere
     Releases zurueck. 🔴 GRENZE: Sie misst die BEHAUPTUNG der Zeile, nicht den Stand
     des Projekts; wer die Zeile aendert ohne zu heben, kommt durch. Dieselbe Bauform
     wie Pruefung 77 (Version, nicht Inhalt). PREIS: Jedes Release fasst diese Tabelle
 an - wie bei Pruefung 67 und 77
 83. Die Chronik zaehlt ihr eigenes Release zu Ende (D-335): Die hoechste
     Release-Spanne "**D-NNN** bis **D-NNN**" in docs/ROADMAP.md endet bei der
     hoechsten vergebenen Kennung des Decision Logs. ANLASS: 1.1.0 stand auf
     "D-329 bis D-332", vergeben sind D-329 bis D-334. URSACHE GEMESSEN: D-333 und
     D-334 sind BEIM UMSETZEN gefallen, die Zeile war da laengst geschrieben - eine
     Zahl, die vor ihrem Gegenstand geschrieben wird, ist danach nicht mehr richtig.
     🔴 DER SCHWERERE TEIL: Von vier beschreibenden Traegern nennt keiner alle sechs,
     und D-333 steht in keinem - nur die MARKE nennt die Menge vollstaendig, und sie
     ist der einzige Traeger, den keine Pruefung erreichen kann (K-111, K-113).
     WARUM PRUEFUNG 58 ES NICHT FAENGT: Sie haelt die Gegenrichtung (jede genannte
     Kennung steht im Register); hier fehlt die Nennung einer vergebenen Kennung.
     D-299-PROBE BESTANDEN: Beide Traeger liegen im Kern und werden byte-gleich
     ausgeliefert. 🔴 GRENZE: Sie misst die OBERGRENZE, nicht die Vollstaendigkeit der
     Nennungen - dieselbe Bauform wie 77 und 82 (K-112). PREIS: Jedes Release fasst
     diese Zeile an - wie bei Pruefung 67, 77 und 82
 84. Die Client-Pack-Vorlage ist kein Client Pack (D-336): clients/_template traegt
     genau eine CLIENT_PACK.md und weder manifest.json noch root-template/. ANLASS:
     `_client_packs()` nahm jedes Verzeichnis mit CLIENT_PACK.md auf, und _template
     erfuellt das - was die Vorlage vor allen Pruefungen schuetzte, war allein ihr
     fehlendes Manifest. GEMESSEN am 2026-09-23 mit einem Probemanifest (Kopie des
     Manifests von claude-code, also eines FREMDEN Clients): drei Packs mit Manifest,
     Validator 0 Fehler, 0 Warnungen. Und clients/README.md Schritt 5 verlangt genau
     dieses Manifest fuer jedes neue Pack. ➡️ EINE VORLAGE, DIE NUR DESHALB KEINE
     PRUEFUNG AUSLOEST, WEIL IHR EIN BESTANDTEIL FEHLT, IST NICHT AUSGENOMMEN - SIE IST
     UNVOLLSTAENDIG. 🔴 Die Bauform "zwei Stellen, die einander decken" (0.57.0).
     ⚠️ Die Ausnahme existierte an zwei anderen Stellen (Pruefung 73,
     LINK_PATH_EXCEPTIONS) und nicht dort, wo die Packmenge ENTSTEHT; seit D-336 steht
     sie in `_client_packs()`. 🔴 GRENZE: Sie prueft die ANWESENHEIT von Bestandteilen,
     nicht deren Inhalt
 85. Eine Zielangabe ueberlebt ihr eigenes Release nicht (D-342): Jede Ueberschrift
     "### Geplant: … – Ziel-Release <Version>" in docs/ROADMAP.md nennt eine Version,
     die groesser ist als .koolie/core/VERSION. ANLASS, gemessen im
     Vorbedingungsdurchgang von 1.3.0: ALLE DREI vorhandenen Abschnitte nannten eine
     Version, die die Gegenwart ueberholt hatte - die Umbenennung auf ~0.68.0
     (erledigt mit 0.88.0, seit fuenfzehn Releases "Geplant"), openai-codex auf 1.1.0
     (die Releasetabelle DERSELBEN Datei fuehrt ihn auf 1.3.0) und die Projekt-Overlays
     auf 1.2.0 (ausgeliefert, Posten nicht gefahren). ➡️ EINE ZIELANGABE IST EINE ZAHL,
     DIE VOR IHREM GEGENSTAND GESCHRIEBEN WIRD - die Bauform von Pruefung 83, hier an
     der PLANSEITE derselben Datei statt an der Chronikseite. URSACHE GEMESSEN: Die
     Verschiebungen sind je einzeln ausgewiesen worden (D-127, D-339), und keine hat
     die Ueberschrift angefasst - wer eine Zahl an zwei Stellen fuehrt, pflegt eine.
     D-299-PROBE BESTANDEN: Beide Traeger liegen im Kern und werden byte-gleich
     ausgeliefert; ein uebernehmendes Projekt traegt dieselbe ROADMAP und dieselbe
     VERSION aus demselben Release. 🔴 GRENZE: Sie misst die ZIELANGABE, nicht den
     STAND des Postens - ein Abschnitt, dessen Ziel in der Zukunft liegt, kann laengst
     erledigt sein und kommt durch; dieselbe Bauform wie 77 (Version, nicht Inhalt) und
     82 (Behauptung, nicht Tatsache), K-116. PREIS: Wer einen Posten verschiebt, fasst
     die Ueberschrift an - und genau das ist der Zweck
 86. Die Sperrform des Schutz-Hooks wirkt beim genannten Client (D-347): Ein Pack, das
     eine eigene Sperrform nennt (hook_block_form), bekommt sie nur, wenn das Skript
     sie kennt, fuer sie WIRKLICH eine Sperre dieser Form ausgibt und die erzeugte
     Hook-Konfiguration sie am Kommando durchreicht. ANLASS, gemessen am 2026-09-23 an
     einer realen Installation von openai-codex: Die bis dahin einzige Sperrform -
     {"decision": "block"} und Exit 2 - bewirkt bei diesem Client NICHTS. Der Client
     meldet den Hook als fehlgeschlagen und FUEHRT DIE OPERATION AUS; im Gegenlauf kam
     der Koederinhalt woertlich heraus. Dieselbe Sperre in seiner Form blockiert, und
     zwar auch im Betriebsmodus ohne Rueckfragen und ohne Sandkasten.
     ➡️ EIN HOOK, DER LAEUFT UND DESSEN SPERRFORM DER CLIENT NICHT LIEST, IST EINE
     ZUSAGE OHNE MECHANISMUS - und nichts meldet es. Geprueft wird die Kette und nicht
     das Manifestfeld, dieselbe Bauform wie Pruefung 17
 87. Die formatgebundenen Pruefungen stehen im Pack (D-346): Ein Client Pack, dessen
     Berechtigungsdatei eine andere Ausgabeform hat als JSON (permissions_format),
     nennt in Abschnitt 5 seines CLIENT_PACK.md jede Nummer aus
     FORMATGEBUNDENE_PRUEFUNGEN, die seine Form nicht erreicht - und keine andere
     (seit 1.13.0 je Form, D-416). ANLASS: Mit dem
     dritten Pack gibt es zum ersten Mal zwei Ausgabeformen; sechs Pruefungen lesen die
     eine und haben fuer die andere keinen Gegenstand. Sie still zu ueberspringen waere
     die Bauform von 0.57.0 - zwei Stellen, die einander decken: Der Validator liefe
     gruen, und niemand wuesste, dass sechs Pruefungen dieses Pack nicht erreichen.
     ➡️ EINE LUECKE, DIE ERKLAERT IST, IST EINE AUSSAGE; EINE, DIE NUR BESTEHT, IST EIN
     BLINDER FLECK. ⚠️ GRENZE: Sie prueft die NENNUNG, nicht die Richtigkeit der
     Begruendung - dieselbe Bauform wie Pruefung 19
 88. Keine Datei, die die Wurzel-Anweisung verdraengt (D-341): Bei einem Client, dessen
     Pack root_instruction_override fuehrt, darf die Datei aus
     <ROOT_INSTRUCTION_LOCAL> nicht im Projektbaum liegen. ANLASS, gemessen mit
     Gegenprobe in der Erhebung von 1.3.0: Liegt AGENTS.override.md im Projekt, steht
     die Wurzel-Anweisung des Frameworks in KEINER Nachricht der Sitzung; ohne sie
     steht sie darin. Ein Projekt, das die Datei in sein .gitignore schreibt - der
     naheliegende Ort fuer eine persoenliche Fassung -, haette eine unversionierte
     Ebene 1 je Arbeitsplatz. ➡️ EINE WURZEL-ANWEISUNG, DIE EINE UNGEPRUEFTE DATEI IM
     SELBEN VERZEICHNIS ERSETZEN KANN, IST KEINE EBENE 1 - SIE IST EIN STANDARD. Der
     Schutz hat drei Teile: Der deny-Korb stellt die Datei schreibgeschuetzt, der
     Schutz-Hook fuehrt sie in seinen Mustern, und diese Pruefung meldet sie, wenn sie
     trotzdem da ist - ein Mensch kann sie weiterhin anlegen, und dann soll es nicht
     still bleiben
 89. Die uebrigen Pfadplatzhalter in den Schichten, die sie tragen (K-69, D-357): Unter
     --strict-overlay fuer <ALLOWED_PATHS>, <TEST_PATHS>, <DOC_PATHS> und
     <READ_ONLY_PATHS> dieselben drei Gegenstaende wie Pruefung 59 fuer
     <EXCLUDED_PATHS>: (a) die Laufzeitfassung NENNT den Platzhalter, (b) ihr Wert ist
     dieselbe Menge wie in der dreispaltigen Zeile von Abschnitt 4 des Quell-Overlays,
     (c) jeder Nur-Lese-Pfad hat im deny-Korb eine Schreibsperre - seit 1.20.1 auch
     jeder Glob von <CI_CONFIG_PATHS> und <QUALITY_GATE_CONFIG_PATHS> (K-35, D-493). ANLASS: Laufzeitfassung
     und Berechtigungsdatei bleiben Saat (D-353), die Handpflege an drei Stellen bleibt -
     und nur eine Pruefung faengt sie auf; von sechs Werten des Uebungs-Overlays wich am
     2026-09-18 einer ab. Ein Overlay, das anders bindet, bekommt eine eigene Meldung und
     wird nicht uebergangen. "Kein Wert" hat gemessen mehrere Schreibweisen
     (`nicht vorhanden`, `keine`) und ist die leere Menge. GRENZE: (c) prueft nur die
     Richtung Quelle -> Korb, und (c) ist wie bei 59 an die Ausgabeform 'json' gebunden
 90. Der Lieferumfang einer Installation (D-367): (a) .koolie/core/LIEFERUMFANG traegt
     einen bekannten Wert, (b) "nutzung" stimmt mit dem Bestand - keine Ablage der
     Nachweisschicht (clientmap.NACHWEIS_ABLAGEN) liegt da, (c) das Quellrepositorium
     fuehrt keine solche Datei. In einer Installation mit "nutzung" meldet Pruefung 12
     Verweise in die Nachweisschicht nicht, und 76, 77 und 80 pruefen nur, was geliefert
     ist - jeweils mit einer HINWEIS-Zeile, die weder als Fehler noch als Warnung zaehlt.
     GRENZE: Ob die Nutzung ohne die Nachweisschicht auskommt, belegt nicht diese
     Pruefung, sondern der zeilengleiche Vergleich mit einer vollen Installation (L367)
 91. Die Standueberschrift der Roadmap (D-372): "## Stand nach Release X.Y.Z" steht in
     docs/ROADMAP.md genau einmal und nennt .koolie/core/VERSION. ANLASS: Bei 1.8.0 stand
     sie auf 1.4.4, direkt ueber "Wird mit jedem Release fortgeschrieben"; bis 0.88.1
     zweiunddreissig Releases lang auf 0.56.0. GRENZE: Sie prueft die Zahl der
     Ueberschrift, nicht den Abschnitt darunter - dieselbe Bauform wie 77
 92. Die Rechtschreibung (D-373): Dokumente der Klassen A, B und D (D-371) enthalten
     ausserhalb von Code kein Wort der Schreibung vor 1996 aus einer festen Stammliste
     (dass, muss, misst, Messbaum ...). ANLASS: 603 alte gegen 1.192 geltende
     Schreibungen, neunzehn Dokumente mischten beide. Register (C) bleiben, wie sie
     geschrieben wurden; die Einstiegsdokumente der Wurzel (README, Quickstart und ihre
     englischen Fassungen, D-437) nur im Quellrepositorium. GRENZE: Ein Wort,
     das nicht auf der Liste steht, kommt durch
 93. Die Form (D-374): In jedem Dokument der Klassen A bis D ist jeder Codeblock
     geschlossen, es gibt genau eine Hauptueberschrift (mit Frontmatter hoechstens eine),
     keine uebersprungene Ueberschriftenebene, und jede Tabellenzeile hat die Spaltenzahl
     ihrer Kopfzeile. Ein Waechter: Der Bestand war bis auf eine Datei sauber. GRENZE:
     Gestalt, nicht Gliederung
 94. Der Steckbrief (D-375): Dokumente der Klassen A und B tragen vor dem ersten
     Abschnitt eine Tabelle "| Attribut | Wert |" mit Kennung (ID oder <Art>-ID),
     Version und Status. Ausgenommen mit Grund: README-Verzeichnisse und die
     Einstiegsdokumente der Wurzel (D-437), die
     Laufzeitschicht, Ausfuellvorlagen und Beispielausgaben. GRENZE: Anwesenheit der
     Zeilen; ihren Wert pruefen 13 und 55
 95. Die Art einer Skill-Aenderung (D-403): Die Zeile der aktuellen Version im
     Aenderungsverlauf eines Skills und jede Zeile nach dem 2026-09-22 nennt, ob sie
     eine Anweisung beruehrt (D-303). ANLASS: K-146 - die Einordnung entscheidet, ob
     die Zellen des Testblatts offen sind, und keine Pruefung sah, ob sie dasteht.
     Nur die Skills des Kerns; projekteigene Skills bleiben aussen vor.
     GRENZE: die Nennung, nicht ihre Richtigkeit
 96. Das Agentenprofil, das die Berechtigungen traegt, ist auch das aktive (D-414):
     Bei einem Pack mit permissions_format 'kiro-agent' traegt die Einstellungsdatei
     des Arbeitsbereichs die Werte des Manifests (Agent, Engine), das Profil ist
     gueltiges JSON mit dem gewaehlten Namen, jede Regel hat eine bekannte Faehigkeit,
     und jedes deny- und ask-Muster der Kernquelle steht darin, kein fremdes allow.
     ANLASS, gemessen am 2026-09-26: Fehlt das Profil oder ist es kaputt, faellt der
     Client STILL auf seinen eingebauten Agenten zurueck, und .env war lesbar; eine
     unbekannte Faehigkeit ueberspringt er regelweise. GRENZE: die Dateien, nicht der
     Start - wer mit --agent einen anderen Agenten waehlt, entgeht ihr
 97. Die Berechtigungsdatei, mit der der Client startet und die trifft (D-440): Bei
     einem Pack mit permissions_format 'cursor-json' traegt die Datei NUR den
     Schluessel permissions mit allow und deny, jeder Eintrag hat einen Regeltyp des
     Clients, jedes deny-Muster der Kernquelle steht darin (die Kernzusagen einzeln
     benannt), kein fremdes allow. Ein Pfadverbot, das der Client nie trifft, weil
     es nicht mit '*' oder einem absoluten Pfad beginnt, ist eine Warnung. ANLASS,
     gemessen am 2026-09-26: Mit einem weiteren Schluessel startet der Client nicht;
     'Read(.env)' und 'Read(**/.env)' liessen den Koeder unter Windows durch. GRENZE:
     die Datei, nicht die Wirkung auf einem anderen Betriebssystem
 98. Das Ziel, nicht der Inhalt (D-449): Der Schutz-Hook laesst ein Schreibwerkzeug
     durch, dessen ZIEL frei ist, auch wenn sein Inhalt Kern-, Overlay- oder
     Laufzeitpfade nennt; er sperrt dasselbe Werkzeug mit einem Ziel im Kern. Bei einem
     Patchtext (apply_patch) zaehlen nur die Dateikoepfe. ANLASS, gemessen am
     2026-09-27 in einem Projekt mit devin-desktop: Ein Aenderungsantrag unter docs/,
     der Overlay- und Kernpfade nannte, wurde gesperrt. GRENZE: die Werkzeugnamen der
     Manifeste, nicht jede Eingabeform eines Clients
 99. Das Mandat gibt sich der Client nicht selbst (D-447, D-448): Der Hook sperrt
     mandat.py und die Mandatsdatei fuer Schreiben und Ausfuehren, laesst nur die
     Auskunft 'mandat.py status' durch und sperrt das Overlay ohne Mandat; Hook und
     mandat.py fuehren dieselben Werte (Dateiname, Umfaenge, Hoechstdauer); die
     Kernquelle der Berechtigungen sperrt das Overlay nicht statisch, sonst hebt kein
     Mandat die Sperre auf. Seit 1.20.2 ebenso die Modusbindung (D-501, K-179):
     'mandat.py modus' und die Datei koolie-modus.json sind fuer den Client gesperrt,
     Hook und mandat.py fuehren denselben Dateinamen und dieselben Modi. GRENZE: Ein
     Befehl, der den Namen verschleiert, entgeht dem Muster - wie bei K-32
100. Der Modellaufruf nur fuer rein lesende Skills (D-451): Ein Skill des Kerns oder
     eines Packs mit dem Trigger 'model' sperrt in permissions.deny 'edit' und 'exec'
     (08-skill-conventions.md, Zeile triggers). ANLASS: Drei rein lesende Skills trugen
     nur 'user', und die Wurzelanweisung trug dem Client zugleich auf, sie aufzurufen
     (Befund A1 aus dem ersten Projekteinsatz). GRENZE: die Richtung model -> lesend;
     ob ein rein lesender Skill 'model' tragen soll, entscheidet der Skill
101. Die MCP-Freigaben (D-459): Die Kernquelle der Berechtigungen gibt kein MCP-Werkzeug
     frei. In einer Installation, deren Pack die Regelform seiner MCP-Werkzeuge kennt
     (mcp_permission_rule), steht in allow nur ein Lesewerkzeug, das Overlay Abschnitt
     13.2 einem Server mit dem Zweck 'lesen fuer Planung' zuweist - kein
     Schreibwerkzeug, kein Muster fuer einen ganzen Server. Mit --strict-overlay
     zusaetzlich: jedes freigegebene Lesewerkzeug steht in allow, und bei einem Client,
     bei dem eine Rueckfrage die Freigabe schlaegt, steht die pauschale MCP-Rueckfrage
     nicht mehr im ask-Korb. ANLASS, GEMESSEN: Mit 'mcp__*' im ask-Korb wies claude-code
     das einzeln freigegebene Lesewerkzeug ab (Vorpruefung zu 1.18.0, V5). GRENZE: Ein
     Pack ohne erhobene Regelform wird nicht abgeglichen; ob die Werkzeugliste des
     Overlays zum Server passt, sieht die Pruefung nicht
102. Die Form des Klaerungsregisters (D-465): Jeder Klaerungspunkt steht in der
     Klaerungstabelle (Abschnitt 1 des Decision Logs), seine Statuszelle beginnt mit
     einem Wert der Legende, und ein zusammengelegter Punkt zeigt auf einen bestehenden,
     der nicht selbst zusammengelegt ist. Das Vokabular leitet sie aus der Legende ab.
     ANLASS: 114 von 184 Punkten standen in der Entscheidungstabelle, elf erledigte
     trugen 'offen' (Triage 2026-09-29). GRENZE: der Anfang der Zelle, nicht ihre
     Richtigkeit
103. Der Stand einer Ergebniszelle (D-472, K-61): Traegt eine Ergebniszelle eines
     Testblatts oder des Testkatalogs eine Standmarke, rechnet die Pruefung den Stand
     ihres Gegenstands nach; weicht er ab, warnt sie, nennt die Marke einen Pfad, den
     es nicht gibt, ist es ein Fehler. ANLASS: FW-KO-02 stand auf 'bestanden', waehrend
     drei spaetere Befunde in seinem Gegenstand lagen. GRENZE: Zellen ohne Marke
     bleiben ungeprueft
104. Die Verdrahtung der Pruefwerkzeuge (D-481): Jede Funktion check_* des Pakets
     pruefungen/ wird gerufen - von main() genau einmal oder im Paket -, und der
     Sondenlauf laedt jeden Teil unter sonden/ in der Reihenfolge seiner Nummer.
     ANLASS: die Aufteilung in 1.19.1 (D-479); eine verschobene, nicht gerufene
     Pruefung liefe nie. GRENZE: die Verdrahtung, nicht, was eine Pruefung tut
105. Die gepruefte Clientversion in der Zielspanne (D-482, K-40): Je Client Pack
     liegt die erste Punktversion der Zeile 'Gepruefte Clientversion' in einer
     Spanne der Zeile 'Verbindliche Zielversion', und jede Spanne ist durch eine
     Punktversion belegt. WARNUNG, kein Fehler. GRENZE: ein Praefixvergleich der
     Schreibweise, kein Beleg fuer gleiches Verhalten in der Spanne
106. Das Entscheidungsprotokoll des Schutz-Hooks (D-487, K-192): In einem Wegwerfbaum
     haelt der Hook eine Sperre und einen Durchlass auf Client-Ereignisse als je eine
     JSON-Zeile mit genau fuenf Feldern fest, nie Inhalt oder Pfadwert; ein Aufruf ohne
     hook_event_name steht nicht darin, 'hook_protokoll: aus' schaltet es ab. ANLASS:
     Sperren hinterliessen keine Spur ausserhalb der Mitschrift. GRENZE: nicht
     manipulationsgeschuetzt; ob ein Client so aufruft, belegt die Messung
107. Die Gegenfaelle der Wirksamkeitsprobe (D-488, D-490, K-195): An einem Wegwerfbaum mit
     der erzeugten Hook-Konfiguration von claude-code meldet wirksamkeit.pruefe_hook
     nichts, ohne Hook-Skript H3 und H4, mit einem Matcher ohne mcp H2. ANLASS: Die
     Hook-Vorpruefung des Messapparats bestand seit 1.19.0 auch einen Baum ohne Hook,
     weil Exit 2 als Sperre galt. GRENZE: der Hook-Teil der Probe an einem Pack
108. Ein allow-Befehl, der ein deny-Praefix umschliesst (D-494, K-47): Warnung, wenn
     in der Kernquelle oder im installierten JSON-Korb eines Packs mit Praefixabgleich
     der Befehl eines allow-Eintrags ein echtes Wortpraefix eines deny-Befehls desselben
     Werkzeugs ist. ANLASS: Bei Bash(git:*) lief 'git -C <pfad> push' an
     Bash(git push:*) vorbei (D-123). GRENZE: die Schreibweise, nicht die
     Befehlsaequivalenz; nur Befehlsregeln, keine Pfadmuster
109. Die beiden Werkzeugfelder eines Skills (D-505, K-93): Fuehrt ein Skill in einer
     Ablage, die das Feld 'permissions' behaelt, 'allowed-tools' oder 'permissions',
     dann fuehrt er beide. ANLASS: Bei devin-desktop wirkt die Beschraenkung nur mit
     beiden Feldern, eines allein bleibt ohne Meldung folgenlos (D-287). GRENZE: die
     Anwesenheit, nicht die Wirkung
110. Die aktivierten Packs gegen die Regelablage (D-504, K-44), nur --strict-overlay:
     Die Zeilen 'Aktivierte Role Packs' und 'Aktivierte Technology Packs' des Overlays
     und die Laufzeitfassungen 30-role-* und 40-tech-* stimmen in beide Richtungen
     ueberein; fehlt die Zeile bei vorhandenen Fassungen, gibt es eine Warnung. ANLASS:
     Vier Regeldateien entfernt, und --strict-overlay meldete dasselbe wie vorher
     (2026-09-17). GRENZE: die Laufzeitfassung und die Nennung, nicht Skills und Version
Der Wirksamkeitsnachweis nach D-23 fuer die Pruefungen 4, 6, 8, 14, 18 bis 66 und 68 bis 110 laeuft als eigenes
Skript: .koolie/core/tests/scripts/probe-pruefungen.py (je Pruefung eine Sonde und eine
Gegenprobe, auf einer Kopie des Repositoriums).

Ohne PyYAML laufen die Prüfungen 4, 5 und 8 eingeschränkt; das Skript sagt es dann als
Warnung. Für einen Release- oder Übernahmenachweis ist PyYAML erforderlich.

Exit-Code 0 = keine Fehler (Warnungen möglich), 1 = Fehler.
Status des Skripts: entwurf. Es prüft Struktur, nicht Semantik; die semantische Prüfung
(Widerspruchsfreiheit, Verhalten des KI-Clients) erfolgt über .koolie/core/tests/TEST_CATALOG.md.
"""
from __future__ import annotations

import argparse
import os
import sys

# Die Pruefungen liegen seit 1.19.1 im Paket pruefungen/ neben diesem Skript, nach
# Gegenstand geteilt (K-174). Dieses Skript ist der Einstieg: oben das
# Register, unten main(). Daneben liegen zwei geteilte Module, die das Paket
# importiert:
#   - overlay_status: Die Auswertung des Overlay-Status liegt seit 0.33.0 in einem
#     eigenen Modul, weil der Status-Hook sie ebenso braucht und sie dort anders
#     umgesetzt war (B08, D-58). Der Hook importiert dieses Modul; er importiert
#     nicht dieses Skript.
#   - mermaid_renderer: Browsersuche und Puppeteer-Konfiguration des Mermaid-
#     Renderers teilt der Validator mit dem Bau der Word-Fassung (K-145, D-398).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pruefungen.gemeinsam import (  # noqa: E402
    detect_client, ERRORS, HINWEISE, warn, WARNINGS, yaml)
from pruefungen.bestand import (  # noqa: E402
    check_actor_naming, check_artefakt_versionen, check_config, check_content,
    check_links, check_manifest, check_mermaid, check_placeholder_naming,
    check_required, check_rules, check_runtime_placeholders, check_skills,
    check_tool_neutrality, check_versions)
from pruefungen.hooks import (  # noqa: E402
    check_durchsetzungstiefe, check_hook_ablageort, check_hook_eingabeschema,
    check_hook_fail_closed, check_hook_interpreter, check_hook_skripte_neutral,
    check_hook_protokoll, check_hook_tool_coverage, check_hook_ziel_statt_inhalt,
    check_hookblock, check_sperrform)
from pruefungen.berechtigungen import (  # noqa: E402
    check_agent_profil_ohne_start, check_agent_startwerkzeug, check_agentenprofil,
    check_berechtigungskoerbe, check_cursor_berechtigungen, check_importsteuerung,
    check_mandatsschutz, check_mcp_freigaben, check_modellaufruf_nur_lesend,
    check_pack_im_korb, check_skill_deny_abbildung, check_skillfreigabe,
    check_verdraengende_wurzelanweisung, check_werkzeugabbildung)
from pruefungen.packs import (  # noqa: E402
    check_abwesenheitsbeleg, check_allow_umschliesst_deny, check_ausfall_mit_ersatz,
    check_clientversion_in_spanne, check_dokumenttabellen, check_formatgebundene_pruefungen,
    check_matrixzeile_in_tabelle, check_normative_kommentare, check_quellenauskunft,
    check_regelablage_sauber, check_schlitzinhalte, check_vorlage_kein_pack,
    check_skill_werkzeugfelder, check_werkzeugabwesenheit, check_zusagenfelder,
    check_zusatzschluessel)
from pruefungen.overlay import (  # noqa: E402
    check_aktivierte_packs, check_ausgeschlossene_vorbedingung, check_befehlsschlitz_in_vorbedingung,
    check_excluded_paths, check_overlay_pfadabgleich, check_overlay_ready,
    check_overlay_schlitze, check_overlay_wertabgleich, check_pflichtplatzhalter,
    check_platzhalterbindung, check_strict_overlay, check_ungebundene_vorbedingung,
    check_v6_freigabefolge)
from pruefungen.testkatalog import (  # noqa: E402
    check_ausgabemarke_gedeckt, check_belegquelle, check_ergebnisstand,
    check_ergebnisstatus_beleg, check_grenzfaelle, check_k3_kategorien,
    check_nummernverweis, check_praeparationsregister, check_pruefmittel_vokabular,
    check_skill_aenderungsart, check_skillaufruf_im_katalog,
    check_skillversion_vorlage)
from pruefungen.register import (  # noqa: E402
    check_d11_stand, check_decision_log_zellen, check_decisionregister,
    check_klaerungsregister, check_klaerungsregister_form, check_pruefregister,
    check_releaseplan_kette, check_roadmapstand, check_status_vokabular)
from pruefungen.dokumente import (  # noqa: E402
    check_altname_restbestand, check_bestandsliste_stand, check_chronikspanne,
    check_dokumentform, check_dokumentstand, check_dokumentzahlen,
    check_gegenzeichnung, check_lizenz, check_rechtschreibung, check_steckbrief,
    check_verirrtes_steuerzeichen, check_zeilenendeform, check_zielangabe)
from pruefungen.werkzeuge import (  # noqa: E402
    check_arbeitsplatzpfad, check_bytecode_versioniert, check_erhebungen_sauber,
    check_gitignore_erzeugnisse, check_kernlage, check_lieferumfang,
    check_praefix_uebererfassung, check_verdrahtung, check_werkzeugnamen,
    check_wirksamkeitsprobe)

# Die Schnittstelle fuer die Werkzeuge, die dieses Skript als Modul laden:
#   mandat.py
#   tests/erhebungen/apparat/stand.py
#   tests/erhebungen/mcp-waechter.py und zaehlen46.py
# Sie bleibt hier, damit kein Lader sich aendern muss (1.19.1, K-174).
from pruefungen.gemeinsam import read, regeldatei, tabellenzellen, TBD_RE  # noqa: E402,F401
from pruefungen.overlay import _p56_ausgeschlossen, _p59_globs, _p89_quelle  # noqa: E402,F401
from pruefungen.testkatalog import stand_wert  # noqa: E402,F401


def main() -> int:
    # 🔴 DER BERICHTSWEG IN BEIDEN KODIERUNGSUMGEBUNGEN (K-168, Bauform D-223). Mehrere
    # Meldungen tragen Zeichen ausserhalb von cp1252 (⚠️, ➡️, 🔴). Feuerte eine davon in
    # der cp1252-Umgebung, die D-49 verlangt, endete der Lauf mit UnicodeEncodeError statt
    # mit der Liste der Befunde - gemessen am 2026-09-26 an Pruefung 82. Ein Zeichen, das
    # die Konsole nicht kennt, erscheint jetzt als Escape-Folge; der Befund bleibt lesbar.
    for strom in (sys.stdout, sys.stderr):
        try:
            strom.reconfigure(errors="backslashreplace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.getcwd())
    ap.add_argument("--strict-overlay", action="store_true")
    ap.add_argument("--check-overlay-ready", action="store_true")
    ap.add_argument("--mermaid", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    if yaml is None:
        # Ohne PyYAML pruefen drei Pruefungen nur noch, ob ein Frontmatter da ist - nicht,
        # was darin steht. Ein Release-Nachweis, der das nicht sagt, behauptet mehr als er
        # geprueft hat; deshalb steht es hier und nicht nur in der Roadmap.
        warn("PyYAML nicht installiert – Prüfung 4 (Frontmatter der Regeltexte), Prüfung 5 "
             "(Frontmatter der Skills) und Prüfung 8 (Overlay-Manifest) laufen eingeschränkt: "
             "Das Vorhandensein wird geprüft, die Feldinhalte nicht. Für einen Release- oder "
             "Übernahmenachweis (FW-KO-01, FW-CL-11, CL-10) muss PyYAML installiert sein")

    man = detect_client(root)
    check_required(root, man)
    check_config(root, man)
    check_berechtigungskoerbe(root, man)
    check_rules(root, man)
    check_skills(root, man)
    check_runtime_placeholders(root, man)
    check_content(root)
    check_links(root)
    check_manifest(root)
    check_versions(root, man)
    check_artefakt_versionen(root)
    check_actor_naming(root)
    check_placeholder_naming(root)
    check_hook_interpreter(root, man)
    check_hook_tool_coverage(root, man)
    check_hook_fail_closed(root, man)
    check_hook_ablageort(root, man)
    check_quellenauskunft(root)
    check_dokumenttabellen(root)
    check_hook_skripte_neutral(root)
    check_importsteuerung(root, man)
    check_normative_kommentare(root, man)
    check_regelablage_sauber(root)
    check_ausfall_mit_ersatz(root)
    check_werkzeugabwesenheit(root)
    check_zusagenfelder(root)
    check_excluded_paths(root, man)
    check_k3_kategorien(root)
    check_grenzfaelle(root)
    check_durchsetzungstiefe(root)
    check_hook_eingabeschema(root, man)
    check_skill_deny_abbildung(root, man)
    check_agent_startwerkzeug(root)
    check_agent_profil_ohne_start(root)
    check_decision_log_zellen(root)
    check_werkzeugabbildung(root)
    check_skillfreigabe(root)
    check_pruefregister(root)
    check_abwesenheitsbeleg(root)
    check_schlitzinhalte(root, man)
    check_hookblock(root, man)
    check_praeparationsregister(root)
    check_bytecode_versioniert(root)
    check_gitignore_erzeugnisse(root)
    check_d11_stand(root)
    check_status_vokabular(root)
    check_tool_neutrality(root)
    check_skillaufruf_im_katalog(root)
    check_klaerungsregister(root)
    check_klaerungsregister_form(root)
    check_ergebnisstand(root)
    check_overlay_schlitze(root)
    check_v6_freigabefolge(root)
    check_releaseplan_kette(root)
    check_zusatzschluessel(root, man)
    check_pflichtplatzhalter(root)
    check_erhebungen_sauber(root)
    check_ungebundene_vorbedingung(root)
    check_decisionregister(root)
    check_befehlsschlitz_in_vorbedingung(root)
    check_skillversion_vorlage(root)
    check_pruefmittel_vokabular(root)
    check_nummernverweis(root)
    check_ausgabemarke_gedeckt(root)
    check_ergebnisstatus_beleg(root)
    check_verirrtes_steuerzeichen(root)
    check_praefix_uebererfassung(root)
    check_werkzeugnamen(root)
    check_arbeitsplatzpfad(root)
    check_pack_im_korb(root, man)
    check_belegquelle(root)
    check_matrixzeile_in_tabelle(root)
    check_altname_restbestand(root, man)
    check_kernlage(root)
    check_dokumentstand(root)
    check_dokumentzahlen(root)
    check_lizenz(root)
    check_gegenzeichnung(root)
    check_lieferumfang(root)
    check_zeilenendeform(root)
    check_bestandsliste_stand(root)
    check_chronikspanne(root)
    check_vorlage_kein_pack(root)
    check_zielangabe(root)
    check_sperrform(root, man)
    check_formatgebundene_pruefungen(root)
    check_verdraengende_wurzelanweisung(root, man)
    check_agentenprofil(root, man)
    check_cursor_berechtigungen(root, man)
    check_roadmapstand(root)
    check_rechtschreibung(root)
    check_dokumentform(root)
    check_steckbrief(root)
    check_skill_aenderungsart(root, man)
    check_hook_ziel_statt_inhalt(root, man)
    check_mandatsschutz(root, man)
    check_modellaufruf_nur_lesend(root, man)
    check_mcp_freigaben(root, man, args.strict_overlay)
    check_verdrahtung(root)
    check_clientversion_in_spanne(root)
    check_hook_protokoll(root)
    check_wirksamkeitsprobe(root)
    check_allow_umschliesst_deny(root, man)
    check_skill_werkzeugfelder(root, man)
    if args.strict_overlay:
        check_strict_overlay(root, man)
        check_platzhalterbindung(root, man)
        check_ausgeschlossene_vorbedingung(root, man)
        check_overlay_wertabgleich(root, man)
        check_overlay_pfadabgleich(root, man)
        check_aktivierte_packs(root, man)
    if args.check_overlay_ready:
        check_overlay_ready(root, man)
    if args.mermaid:
        check_mermaid(root)

    for h in HINWEISE:
        print(f"HINWEIS  {h}")
    for w in WARNINGS:
        print(f"WARNUNG  {w}")
    for e in ERRORS:
        print(f"FEHLER   {e}")
    print(f"\nErgebnis: {len(ERRORS)} Fehler, {len(WARNINGS)} Warnungen")
    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
