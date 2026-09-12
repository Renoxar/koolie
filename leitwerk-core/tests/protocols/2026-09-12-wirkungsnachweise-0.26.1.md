# Testprotokoll – Wirkungsnachweis der Prüfung 6 (Release 0.26.1, Befund B03)

| Feld | Inhalt |
|---|---|
| Test-ID | `FW-KO-01` (Basis), Teilnachweis für die mit 0.26.1 geänderte Prüfung 6 |
| Framework-Version | 0.26.1 |
| Datum | 2026-09-12 |
| Prüfmethode | skript |
| Prüfgegenstand | Framework-Repository; je Sonde eine vollständige Kopie in einem Temporärverzeichnis |
| Werkzeug | `leitwerk-core/tests/scripts/probe-pruefungen.py` |
| Umgebung | Windows 11, Python 3.14.4, PyYAML 6.0.3 |
| Ergebnis | **alle Sonden gemeldet, keine Gegenprobe beanstandet; gegen die Vorfassung 0.26.0 fallen sieben von sieben** |

## 1. Warum dieses Protokoll

Befund **B03** des unabhängigen Reviews vom 2026-09-12: Prüfung 6 gab die gefundenen Werte im
Klartext aus – E-Mail-Adressen, IP-Adressen, interne Hostnamen, URLs samt Parametern und
Sperrbegriffe. Die Korrektur steht in `CR-2026-043` und D-39.

**Dieser Nachweis hat eine Eigenheit, die ihn von allen bisherigen unterscheidet.** Die üblichen
Sonden belegen, dass eine Prüfung etwas **meldet**. Hier genügt das nicht: Die alte Fassung meldete
ebenfalls – sie meldete sogar mehr, nämlich den Wert dazu. Jede Sonde dieses Blocks prüft deshalb
**zwei Bedingungen**:

1. Der Befund wird gemeldet, erkennbar an der neutralen Kennung der Kategorie.
2. **Der Markerwert steht nirgends in der Ausgabe** – weder in der Standard- noch in der
   Fehlerausgabe des Laufs.

Die zweite Bedingung ist die eigentliche. Die erste hätte die alte Fassung ebenfalls bestanden.

## 2. Ausgeführte Befehle und Ergebnis

```text
python leitwerk-core/tests/scripts/validate-framework.py
→ Ergebnis: 0 Fehler, 0 Warnungen

python leitwerk-core/tests/scripts/probe-pruefungen.py .
→ alle Sonden und Gegenproben bestanden   (Exit 0)
```

## 3. Der Lauf, der den Nachweis trägt

Bedingung 2 ist ein **Abwesenheitsnachweis**: Etwas steht nicht in der Ausgabe. Ein solcher Nachweis
belegt sich nicht selbst – er braucht einen Lauf, in dem dieselbe Sonde denselben Wert **findet**
(Verfahren Punkt 7 des Testkatalogs). Dieser Lauf ist hier nicht konstruiert, sondern liegt vor:
**derselbe Sondenblock gegen die Vorfassung 0.26.0.**

Aufbau: eine Kopie des Arbeitsbaums, in der allein `validate-framework.py` und
`hook-check-secrets.py` auf den Stand `HEAD` (0.26.0) zurückgesetzt sind. Der Sondenblock ist
derselbe.

```text
python <kopie>/leitwerk-core/tests/scripts/probe-pruefungen.py <kopie>
→ Ergebnis: 7 Abweichung(en)   (Exit 1)
```

| Lauf | Sonden der Prüfung 6 | Ergebnis |
|---|---|---|
| gegen 0.26.0 (Vorfassung) | 7 | **alle sieben fallen** |
| gegen 0.26.1 (diese Fassung) | 7 | alle sieben bestehen |
| Gegenprobe, beide Fassungen | 1 | besteht in beiden – die Prüfung ist nicht breiter geworden |

**Damit misst der Block die Änderung und nicht sich selbst.** Eine Sonde, die gegen beide Fassungen
besteht, belegt nichts; das ist die Auflage der Entscheidung zu `CR-2026-043`.

Sechs der sieben fallen an Bedingung 2 – der Wert stand in der Ausgabe. Die Secret-Sonde fällt
allein an Bedingung 1: Diese Diagnose gab den Wert **nie** aus, ihr fehlte die Fundstelle. Auch das
ist ein Messergebnis und kein Mangel der Sonde.

## 4. Sonden und Gegenproben im Einzelnen

Die gesetzten Marker sind synthetisch und stehen ausschließlich in `probe-pruefungen.py`; dieses
Verzeichnis ist von Prüfung 6 ausgenommen. **Sie werden hier nicht wiedergegeben** – aus demselben
Grund, aus dem dieser Antrag gestellt wurde.

| Kategorie | Art | Gesetzter Defekt beziehungsweise erlaubter Fall | gegen 0.26.0 | gegen 0.26.1 |
|---|---|---|---|---|
| E-Mail-Adresse | Sonde | synthetische Adresse außerhalb der Dokumentationsdomänen in einer geprüften Datei | Wert in der Ausgabe | Kennung `FW-CONTENT-EMAIL`, kein Wert |
| IP-Adresse | Sonde | Adresse außerhalb der Dokumentations- und Loopback-Bereiche | Wert in der Ausgabe | Kennung `FW-CONTENT-IP`, kein Wert |
| interner Hostname | Sonde | Name auf einer als intern geführten Endung | Wert in der Ausgabe | Kennung `FW-CONTENT-HOST`, kein Wert |
| URL | Sonde | URL außerhalb der Allowlist, mit Pfadangabe | vollständige URL in der Ausgabe | Kennung `FW-CONTENT-URL`, kein Wert |
| Sperrbegriff | Sonde | Begriff in die Sperrliste **und** in eine geprüfte Datei eingetragen | Begriff in der Ausgabe | Kennung `FW-CONTENT-TERM`, kein Wert |
| Secret-Muster | Sonde | Zeichenkette im Format eines Cloud-Zugangsschlüssels | Kategorie ohne Wert, **aber ohne Fundstelle** | Kennung `FW-CONTENT-SECRET` mit Zeile und Spalte |
| Hook-Zusatzmuster | Sonde | ungültiger regulärer Ausdruck in der Umgebungsvariablen für projektspezifische Pfadmuster | Muster in der Fehlerausgabe | Position statt Wert |
| alle Kategorien | Gegenprobe | Dokumentationsadresse, IP aus dem Dokumentationsbereich, URL von der Allowlist | unbeanstandet | unbeanstandet |

**Die Gegenprobe ist der Teil, den man weglassen kann und nicht weglassen sollte.** Ohne sie
belegte der Block nur, dass die Prüfung meldet – nicht, dass sie das Richtige meldet. Eine Prüfung,
die jede Adresse beanstandet, besteht alle sieben Sonden darüber.

## 5. Die Sonde schwärzt ihre eigene Ausgabe

Meldet eine Sonde eine Abweichung, zeigt sie zur Diagnose einige Zeilen der Validatorausgabe. Genau
dort stünde bei einem Fehlschlag der Wert, dessen Weitertragen die Sonde beanstandet. Der
Markerwert wird deshalb vor der Ausgabe ersetzt. Im Lauf gegen 0.26.0 ist das zu sehen:

```text
SONDE      6    FEHL  Gesperrter Begriff: gemeldet, Begriff nicht ausgegeben
        Befund nicht gemeldet. Ausgabe: FEHLER   <datei>: gesperrter Begriff '<Marker entfernt>'
        Der Markerwert steht in der Ausgabe - das ist B03 selbst.
```

Ohne diese Schwärzung hätte der Nachweis den Befund reproduziert, den er führt – eine Ebene höher.

## 6. Grenzen dieses Nachweises

- **Der Mermaid-Fehlerpfad ist geändert, aber unbelegt.** Er verlangt einen fehlschlagenden Lauf des
  externen Renderers; dieser fehlt in der Umgebung. Nach D-23 ist das ein **offener** Nachweis, kein
  erledigter – die Auflage der Entscheidung weist ihn ausdrücklich so aus.
- **`FW-DS-01` bleibt offen.** Der Sitzungstest prüft, ob das **Modell** einen Fund nur über die
  Fundstelle meldet. Dieses Protokoll prüft das Werkzeug. Dass beide dieselbe Regel tragen, war der
  Anlass des Befunds – eingelöst ist damit nur die eine Hälfte.
- **Der Block prüft die Diagnosen der Prüfung 6 und zwei Fehlerpfade, nicht jede Ausgabe des
  Validators.** Ob weitere Stellen fremden Inhalt weitertragen, ist eine Frage der Durchsicht, nicht
  dieses Laufs. Geprüft und unauffällig: die Diagnosen, die Werte aus dem eigenen Vokabular des
  Frameworks nennen – Platzhalternamen, Versionsangaben, Verweisziele.

## 7. Bewertung

**Bestanden.** Prüfung 6 meldet nach 0.26.1 Pfad, Zeile, Spalte und Kategorie; der gefundene Wert
erscheint in keiner Ausgabe. Der Nachweis ist wiederholbar und trägt seine eigene Positivkontrolle
in Gestalt des Laufs gegen die Vorfassung.

| Feld | Inhalt |
|---|---|
| Gegenzeichnung | `<TBD>` |
