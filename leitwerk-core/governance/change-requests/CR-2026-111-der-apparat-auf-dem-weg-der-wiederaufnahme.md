# Änderungsantrag `CR-2026-111`

| Feld | Inhalt |
|---|---|
| Titel | Der Apparat lag tot auf dem Weg der Wiederaufnahme – Befehl 1 von 4 startete nicht, und Befehl 4 hätte keinen einzigen Lauf gefahren |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-21 |
| Betroffene Artefakte | `tests/erhebungen/stand-b4.py`, `reihe-b4.py`, `ablage.py` (`sollmenge()`, `laeufe()` **neu**), `tests/scripts/validate-framework.py` (**Prüfung 70**), `tests/scripts/probe-pruefungen.py` (fünf Einheiten), `tests/TEST_CATALOG.md`, `tests/erhebungen/README.md`, `governance/DECISION_LOG.md` (**D-229**, **D-230** neu), `tests/protocols/2026-09-21-wiederaufnahme-nachlauf-b4.md` (neu), `docs/ROADMAP.md`, `CHANGELOG.md`, `VERSION`, `UEBERGABE.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind der Meßapparat und der Prüfapparat |
| Art | Befunde auf dem Weg der Wiederaufnahme – **kein Kontingent, kein Lauf am Client** |
| Dringlichkeit | **Regulär**, unmittelbar vor der Wiederaufnahme des Nachlaufs |

## 1. Anlass

Der Nachlauf von Bündel 4 ist am 2026-09-20 mitten zwischen Haupt- und Kontrolläufen
abgebrochen, weil das Wochenkontingent ausging. Der Wiederaufnahmepunkt
(`WIEDERAUFNAHME.md`) nennt **vier Befehle**. Am 2026-09-21 hat sich vor dem ersten
bezahlten Kontrollauf gezeigt: **zwei davon tragen nicht.**

**Beide Befunde kosteten nichts, weil sie vor dem Lauf kamen.** Damit fiel bei den
letzten **zwanzig** Durchgängen in Folge der billigste Befund vor dem ersten Lauf.

### 🔴 Befund 1: Befehl 1 von 4 startete seit `0.79.0` nicht

```
python leitwerk-core\tests\erhebungen\stand-b4.py
→ NameError: name 'S' is not defined
```

Das Skript, dessen Kopfkommentar sagt *„EINE ZAHL IN EINER UEBERGABE IST EINE
MOMENTAUFNAHME, dieses Skript ist der Stand"*, bricht **beim Import** ab:

```python
PROMPTS = os.path.join(os.path.dirname(S), "prompts")
```

**`S` trug bis D-222 den Ablageort neben dem Skript.** Der Umzug in den Kern hat den
Namen entfernt und **zwei** Lesestellen stehen lassen – eine im Modulrumpf, eine in
`main()`. Seit `0.79.0` war das Werkzeug tot, und der Tag seiner Wiederaufnahme war der
Tag, an dem es auffiel.

> *Ein Werkzeug, das niemand fährt, verfällt lautlos – und der Tag, an dem es gebraucht
> wird, ist der Tag, an dem es fehlt.*

🔴 **Und das ist der eigentliche Befund: keine der 69 Prüfungen konnte es sehen.**

| Prüfung | Was sie über den Apparat sagt |
|---|---|
| **45** | unter `leitwerk-core/` ist **kein Bytecode** versioniert – die **Abwesenheit** einer Datei |
| **69** | in der Erhebungsablage liegen nur `.py` und `.md` – die **Art** der Dateien |
| *keine* | ob eines dieser `.py` **läuft** |

Der Apparat hatte zwei Wächter über seinen **Ablageort** und keinen einzigen darüber,
ob seine Werkzeuge **starten**.

### 🔴 Befund 2: Der nächste Befehl hätte keinen einzigen Lauf gefahren

`stand-b4.py` schließt mit `NAECHSTER BEFEHL: python reihe-b4.py`. Genau dieser Aufruf
**ohne Argumente** bricht ab:

```
ABBRUCH: der Baum C:\lw-b4\sk011n01 fehlt - erst baeume-b4.py
```

Der Nachlauf mißt **vierzehn Zellen / 28 Läufe**. Sein Promptverzeichnis trägt die
**fünfzig** Prompts des Meßtags, weil `prompts-schreiben-b4.py` alle schreibt und keine
Zelle kennt. Beide Skripte leiteten ihre Sollmenge **aus diesem Verzeichnis** ab:

| | gemeldet | fällig |
|---|---|---|
| `stand-b4.py`: Sollmenge | **50 Läufe / 19 Zellen** | 28 Läufe / 14 Zellen |
| `stand-b4.py`: Fehlbestand | **35** | 15 |
| `stand-b4.py`: Restkosten | **rund 37 USD** | rund 18 USD |
| `reihe-b4.py` ohne Argumente | **Abbruch, 0 Läufe** | 15 Läufe |

🔴 **Gerettet hat den Nachlauf allein die Kennungsliste im Wiederaufnahmepunkt – und
sie weist sich selbst als *„Vorsicht, keine Pflicht"* aus.** Wer dem Apparat gefolgt
wäre statt der Liste, hätte einen Abbruch bekommen; wer der Zahl gefolgt wäre, hätte
das Doppelte veranschlagt.

> *Ein Verzeichnis ist kein Zuschnitt. Es ist der Zuschnitt von gestern.*

Das ist dieselbe Bauform wie D-224 (`LW_ERHEBUNG`) und D-218 (`--ziel`), eine Ebene
weiter: **Ein Ort, der aus der Umgebung erschlossen wird, gehört dem, der ihn zuletzt
gefüllt hat.**

## 2. Was gemessen wurde, bevor entschieden wurde

- **Der Defekt selbst, an beiden Stellen:** `stand-b4.py` bricht zuerst im Modulrumpf
  ab; nach der ersten Berichtigung bricht es in `main()` erneut ab. **Ein Wächter, der
  nur die erste Fundstelle meldet, hätte hier zweimal gebraucht werden müssen.**
- **Die neue Prüfung gegen den gesamten Kern, vor der Berichtigung:** **ein** Befund
  (`stand-b4.py`, zwei Fundstellen), sonst nichts – aus **zwanzig** `.py`-Dateien.
  Zwölf davon nennen Modulglobale wie `__file__`; sie laufen, und die Prüfung schweigt
  über sie. *Ein Wächter, der bei jedem Lauf meldet, wird abgeschaltet.*
- **Die berichtigte Sollmenge gegen den Zuschnitt der Erhebung:** `stand-b4.py` meldet
  jetzt **28 Läufe, 14 Zellen, 1 davon mit zweitem Turn** – Zahl für Zahl das, was die
  README dieser Erhebung als ihren Gegenstand nennt, und **13 von 28 gültig** zum
  Zeitpunkt der Wiederaufnahme, wie es der Wiederaufnahmepunkt sagt. Die elf Prompts
  ohne Meßbaum stehen ab sofort **namentlich** unter *„Nicht im Zuschnitt dieser
  Erhebung"*.
- **Die drei Sonden und die zwei Gegenproben zu Prüfung 70** laufen (`70a` bis `70c`,
  `70a` und `70b`). Sonde `70a` setzt den Defekt **wörtlich** so, wie er gefunden wurde.
- **Der Nachlauf ist wieder angefahren und vollständig:** 28 von 28 Belegen gültig, `is_error` bei keinem, zusammen **28,38 USD**; die fünfzehn Kontrolläufe dieses Tages kosteten **15,85 USD** gegen rund 18,40 gerechnet. Kein Beleg des ersten Teils ist angefaßt worden.
- **Wirkungsnachweis zu E2 nach dem Nachlauf, ohne einen Lauf:** `reihe-b4.py` **ohne Argumente** geht jetzt den ganzen Zuschnitt durch – 27 Kennungen, alle übersprungen, **gefahren: 0 | Kosten dieser Reihe: 0.00 USD** – und nennt die elf Prompts ohne Baum. **Vorher brach er beim ersten dieser elf ab.**

## 3. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Wer bemerkt, daß ein Werkzeug des Kerns nicht mehr startet?** | **Prüfung 70.** Zu jeder `.py` unter `<CORE_DIR>/` wird die **Symboltabelle** gebaut, die der Interpreter selbst anlegt; gemeldet wird jeder global gelesene Name, den weder der Modulrumpf noch die eingebauten Namen binden – und jede Quelle, die er nicht übersetzt | **Verworfen: die Module zu importieren** – das führt den Modulrumpf aus; `ablage.py` bricht ohne `LW_ERHEBUNG` mit Absicht ab, `lauf.py` legt sein Belegverzeichnis an: **genau das, was D-222 verworfen hat.** *Eine Prüfung, die ihren Gegenstand verändert, mißt ihn nicht.* **Verworfen: `compile()`** – es übersetzt und kennt keine Bindung; der gemessene Fall wäre durchgelaufen. **Verworfen: ein Zähler über den Quelltext** (dieselbe Bauform, die D-223 verworfen hat). **Verworfen: den Anker an *keine `.py` im Kern* zu hängen** – der Validator ist selbst eine, der Anker wäre **durch Konstruktion** nie erreichbar (`0.59.1`); er hängt am Meßapparat, dessen Ablage nachweislich leer sein kann. **Preis, benannt:** Geprüft wird der **Name**, nicht der **Wert**; `S = None` und `os.path.dirname(S)` läuft durch – dieselbe Enthaltung wie bei Prüfung 68, und Gegenprobe `70b` hält sie fest |
| **E2** | **Woher kommt die Sollmenge einer Erhebung?** | **Aus ihren Meßbäumen.** `baeume-b4.py` legt genau die Bäume an, die der Zuschnitt nennt; `ablage.sollmenge()` leitet daraus **einmal** ab, und `stand-b4.py` wie `reihe-b4.py` benutzen dieselbe Ableitung. Ein Prompt **ohne** Baum ist die Zelle einer anderen Erhebung und wird **genannt** | **Verworfen: die Sollmenge zu pflegen** – *eine Zahl, die gepflegt werden muß, wird nicht gepflegt* (D-153), und derselbe Apparat hat es mit drei `--erwarte`-Werten vorgeführt (D-225). **Verworfen: das Promptverzeichnis je Erhebung zu beschneiden** – dann entschiede der Schreiber der Prompts über den Zuschnitt, und der Trockenlauf verlöre die Prompts, gegen die er prüft. **Verworfen: fehlende Bäume stillschweigend zu überspringen** – dann sähe *der Baum wurde nie gebaut* aus wie *die Zelle gehört nicht dazu*. **Preis, benannt:** Der Zuschnitt hängt an einem Zustand **außerhalb** des Repositoriums. Nach `baeume_loeschen.py` ist die Sollmenge leer – `stand-b4.py` sagt an dieser Stelle ausdrücklich, daß sein Stand dann **keine Aussage** über die Vollständigkeit ist, und `reihe-b4.py` bricht bei **null** Bäumen ab |
| **E3** | **Wird der Nachlauf vor oder nach der Abhilfe wieder angefahren?** | **Vor der Abhilfe, mit der Kennungsliste des Wiederaufnahmepunkts.** Die fünfzehn Kontrolläufe hängen an Bäumen, Vertrauenseinträgen und einer Zustandsaufnahme *vorher*, die seit dem 2026-09-20 stehen; jede Stunde Verzug ist eine Stunde, in der etwas davon verlorengehen kann | **Verworfen: erst die Abhilfe, dann fahren** – die Abhilfe berührt `reihe-b4.py`, und ein laufender Prozeß hat sein Modul bereits geladen; die Änderung hätte **auf den nächsten Lauf gewartet** und bis dahin nichts belegt. **Preis, benannt:** Die fünfzehn Kontrolläufe dieses Nachlaufs sind mit der **alten** Fassung gefahren – was sie messen, ändert das nicht (die Kennungen waren genannt), aber der Wirkungsnachweis zu E2 steht am **Stand**, nicht an der Reihe |

## 4. Entscheidung

**E1 bis E3 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-21). Decision
Records **D-229** und **D-230**. **Kriterium 2 unverändert bei 32** – dieser Durchgang
schließt keine Zelle und öffnet keine.

## 5. Abnahme

- `validate-framework.py --root .`: **0 Fehler, 0 Warnungen**.
- `probe-pruefungen.py`: **voller Lauf in beiden Kodierungsumgebungen, 283 Einheiten, 410 Meldezeilen, keine ohne `OK`** – oberhalb der Trennlinie **zeilengleich** (324,6 s und 324,4 s), darunter die fünf neuen Einheiten zu Prüfung 70.
- `zaehlen46.py`: **Katalog 4 | Testblätter 28 | Summe 32** – unverändert.
- Protokoll: `leitwerk-core/tests/protocols/2026-09-21-wiederaufnahme-nachlauf-b4.md`.
- **Kein Lauf am Client für die Befunde selbst, kein Kontingent verbraucht.**
