# Architektur – VDO Tempomat: Parallel-Ansatz (ESP-Brücke)

> **Entscheidung:** Parallel-Ansatz. Die originale VDO-Tempomat-Einheit
> bleibt erhalten und regelt/sichert wie bisher. Ein ESP32 wird als
> **reversible Inline-Box** dazwischengesteckt, hört Signale mit und kann
> die Bedien-Taster „mitdrücken". Steuerung/Anzeige über Touch-Display
> via eigenem CAN-Bus.
>
> Der Komplett-Neubau (ESP ersetzt VDO, treibt Stellglied direkt) bleibt
> als mögliche Ausbaustufe 2 offen, ist aber **nicht** der aktuelle Weg.

## Grundprinzip: Wired-OR, nicht ersetzen

Die Original-Bedientaster bleiben. Parallel dazu sitzt je ein elektronischer
„Schalter", den der ESP ansteuert. Beide wirken auf denselben Eingang →
**egal ob Finger oder Touch-Display, der Tempomat bekommt denselben Impuls.**
Der Ein/Aus-Hauptschalter (Dauerplus) wird **nicht** angefasst.

## Reversible Inline-Box („Stecker rein, Stecker raus")

Kabelbaum/Schalter → Box → VDO-Einheit. Alle Pins werden **1:1 durchgereicht**,
nur die benötigten Signale werden **parallel angezapft**. Box abziehen =
Originalzustand.

```
Kabelbaum/Schalter ──►┌───────── Zwischenbox ─────────┐──► VDO-Einheit
                      │  alle Pins 1:1 durchgereicht   │
                      │                                │
                      │  Abgriffe an den ESP:          │
                      │   • Plus/Minus  (parallel = mitschalten)
                      │   • Set/Resume  (parallel = mitschalten)
                      │   • Speed (Reed) → Eingang (mitlesen)
                      │   • Bremse x2   → Eingang (mitlesen, read-only)
                      │   • 12V + GND   → 3,3V-Regler für ESP
                      │                                │
                      │   ESP32 ── CAN-Transceiver ───┼──► CAN (Touch-Display)
                      └────────────────────────────────┘
```

## I/O-Übersicht

| Signal            | Richtung ESP | Beschaltung                          |
|-------------------|--------------|--------------------------------------|
| Plus / Minus      | Ausgang      | Optokoppler bzw. PhotoMOS, parallel zum Kippschalter |
| Set / Resume      | Ausgang      | Optokoppler bzw. PhotoMOS, parallel zum Taster       |
| Geschwindigkeit (Reed) | Eingang | Optokoppler + Pulszählung (Frequenz) |
| Bremssignal x2    | Eingang      | Optokoppler, **read-only**           |
| Taster mitlesen (optional) | Eingang | Optokoppler                       |
| 12V / GND         | Versorgung   | 12V → 3,3V Regler                    |

## Bauteilwahl: Optokoppler vs. PhotoMOS

Hängt davon ab, **wogegen die Taster-Kontakte schalten** (erst messen / Schaltplan):

- **Normaler Optokoppler** (Fototransistor, z. B. PC817/4N35): leitet nur in
  einer Richtung, schaltet sauber **gegen Masse**. Für **alle Eingänge (Lesen)**
  immer die richtige Wahl.
- **PhotoMOS** (MOSFET-Ausgang, z. B. AQY212): echter Schaltkontakt,
  **bidirektional / polaritätsunabhängig** – egal ob gegen Masse oder +12 V.

**Regel:**
1. Pro Kontakt messen: schaltet gegen **Masse** oder **+12 V**?
2. Alles gegen Masse → komplett **normale Optokoppler** (lesen *und* setzen).
3. Etwas gegen +12 V / unsicher / bulletproof → für diese Ausgänge **PhotoMOS**.

PhotoMOS ist also kein Muss, sondern die „egal-welche-Polarität"-Versicherung.

## Geschwindigkeits-Mithören & Zielanfahr-Logik

Der ESP liest den Reed-/Tacho-Impuls (Frequenz ∝ km/h) **hochohmig parallel**
(nur mithören, Signal für VDO nicht belasten), Eingang über Optokoppler
geschützt, entprellt. **Kalibrieren:** bei bekannter Geschwindigkeit Hz messen.

Damit kann der ESP eine **Zielgeschwindigkeit anfahren** – ohne selbst zu regeln:

1. Der **VDO bleibt der Regler** und behält alle Sicherheitsabschaltungen.
   Der ESP **verstellt nur den Sollwert** über Plus/Minus-Impulse (wie ein Finger).
2. Tempomat aktiv → einmal **Set**.
3. **Plus halten**, bis gemessene Geschwindigkeit ≈ Ziel → loslassen, VDO hält den Wert.
4. Feinkorrektur nur mit kurzen Einzel-Tipps und **Hysterese** (z. B. ±1 km/h Totband).
5. Nach jedem Tipp kurz warten (VDO rampt selbst), erst dann neu vergleichen –
   **nicht gegen den VDO-Regler arbeiten**. Sollwert nur ändern, wenn eingekuppelt.

## Bremssicherheit (kritisch)

- Der **Brems-Reset bleibt fest verdrahtet und unabhängig vom ESP.** Der VDO
  macht den Reset selbst. Der ESP **sitzt nicht im Bremspfad**, er liest nur mit.
  Fällt der ESP aus → Bremse kuppelt den Tempomat trotzdem aus.
- Es liegen **2 redundante Bremssignale** vor (typisch: Schließer fürs Bremslicht
  + Öffner, der beim Bremsen den Tempomat killt). Erst messen, was im Ruhezustand
  anliegt und was sich beim Treten ändert; ggf. invertierte Logik. Beide getrennt
  einlesen erlaubt Diagnose eines defekten Bremsschalters.
- **ESP-Logik:** Bremse = höchste Priorität (Interrupt). Bremse erkannt →
  **sofort jede automatische Plus/Minus-Ausgabe abbrechen**, Status „disengaged",
  Display aktualisieren, **kein automatisches Wiedereinkuppeln** (nur über bewusstes
  Set/Resume). Kurze Sperrzeit nach der Bremse.

## CAN / Touch-Display

- ESP32 hat CAN-Controller (TWAI) integriert, braucht zusätzlich einen
  **CAN-Transceiver** (z. B. SN65HVD230 / TJA1051).
- Das Fahrzeug (alter Transporter/LKW) hat **selbst keinen CAN-Bus** → der CAN ist
  der **eigene Bus** zwischen Box und Touch-Display (und evtl. weiteren Eigenbau-Modulen).
- Display zeigt Ist-/Soll-Geschwindigkeit und Tempomat-Status.

## Offene Punkte / TODO

- [ ] **Schaltplan** beschaffen/hochladen → Pinbelegung S/T → Funktion zuordnen
- [ ] Pro Bedien-Kontakt **messen**: gegen Masse oder +12 V? (Bauteilwahl Opto/PhotoMOS)
- [ ] **Steckertyp** der VDO-Einheit identifizieren (oranger Steckverbinder: Pinzahl, Raster, Hersteller) → Gegenstecker beschaffen
- [ ] **Reed/Speed-Signal** identifizieren (separater Tacho-Ausgang oder gemeinsamer Impuls?) + kalibrieren
- [ ] **Bremssignale** ausmessen (Ruhe-/Bremszustand, Polarität)
- [ ] Bauteilliste finalisieren (Optokoppler/PhotoMOS-Mix, CAN-Transceiver, 3,3V-Regler)
- [ ] ESP32-Firmware-Struktur (Touch-UI → Kanäle, Tastimpuls-Timing, Status-Sync)
