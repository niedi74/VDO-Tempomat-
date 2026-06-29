# Bedienteil – Verdrahtung (Eigenbau) & ESP-Anbindung

> ⚠️ **REVISION / IN KLÄRUNG:** Der Plan arbeitet mit **Versorgungs-Schienen
> mit Verteiler-Knoten**, nicht mit reinen 1-Ader-zu-1-Klemme-Verbindungen:
> - 🔴 **Rot = +12 V (Kl. 15)** – mit **Knoten/Verteilpunkt**, zweigt auf
>   mehrere Klemmen ab (u. a. B1/Schalter, kommt an B2 raus, P2 …).
> - 🔵 **Blau = Masse** – mit **mehreren Knoten/Verteilern** auf viele Klemmen.
> - **B3** geht in einen Schalter.
> - **Automatik:** **weiß (w) an T9 gebrückt** → durchverbunden auf Steuergerät
>   **Klemme 9** (Plan: „bei autom. Getriebe w + m verbinden").
>
> Die frühere Behauptung „B2 = Reed/G1" war ein Trace-Fehler (die rote Ader an
> B2 ist der **+12-V-Abzweig**, nicht das Reed). Die untenstehende Tabelle
> (pin2=Masse usw.) ist **überholt**. **Endgültige Belegung erst per Multimeter
> festlegen** (Box-Pins ↔ Plan-Klemmen, Schienen/Knoten beachten), bevor etwas
> angeschlossen wird.

Eigenbau-Bedienteil: schwarzes Gehäuse mit **3 Kippschaltern + grüner LED**.
Fotos unter [`images/bedienteil/`](images/bedienteil).

![Front](images/bedienteil/front-3schalter-led.jpg)

## Schaltprinzip

**Geschaltete Masse** (vom Nutzer ermittelt): jeder Schalter verbindet seine
Signalader mit der gemeinsamen Masse-Ader. Das Steuergerät hat interne Pull-ups;
gedrückt = Ader auf Masse gezogen.

➡️ **Konsequenz für die ESP-Box: normale Optokoppler genügen, kein PhotoMOS nötig.**

## Adernbelegung (6-adriges Kabel)

| Ader | Funktion | angeschlossen an |
|------|----------|------------------|
| **1** | Kippschalter **ein/aus** | Schalter 1 |
| **2** | **gemeinsame Masse** (alle 3 Schalter + LED-Rückleiter) | — |
| **3** | **LED** (Status „bereit") | direkt an LED |
| **4** | **RESUME** | mittlerer Taster |
| **5** | **ACC** (hoch / schneller) | Taster mit Mittelstellung |
| **6** | **DEC** (runter / langsamer) | Taster mit Mittelstellung |

> Quelle: Beschreibung des Nutzers + Innenfotos. **Noch mit Multimeter zu bestätigen:**
> (1) Ader 2 = wirklich Fahrzeugmasse? (2) ACC/DEC-Richtung (Ader 5 ↔ 6 ggf. tauschen).

## ESP-Parallelbox – Anbindung

Der ESP paralleliert die Taster, indem er die jeweilige Signalader gegen Ader 2
(Masse) zieht – je ein **Optokoppler** pro Kanal:

| ESP-Kanal | schaltet/liest | Wirkung |
|-----------|----------------|---------|
| Ausgang (Opto) | Ader 4 ↔ Ader 2 | RESUME |
| Ausgang (Opto) | Ader 5 ↔ Ader 2 | ACC (schneller) |
| Ausgang (Opto) | Ader 6 ↔ Ader 2 | DEC (langsamer) |
| Eingang (Opto) | Ader 3 ↔ Ader 2 | LED mitlesen → Status „bereit" |
| — | Ader 1 (ein/aus) | bleibt manuell (ESP fasst nicht an) |

**Vorteil:** Die exakte S/T-Klemmenzuordnung am Steuergerät wird für den
Parallel-Betrieb **nicht** benötigt – der ESP klemmt direkt an die 6
Bedienteil-Adern und ahmt die Taster nach. Brems-/Geschwindigkeitssignal liest
der ESP wie in [`architektur.md`](architektur.md) beschrieben zusätzlich mit.
