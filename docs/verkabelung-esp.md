# Verkabelungsplan – ESP-Box (Inline / parallel)

Fertige Module, lötfrei: **ESP32-S3 (44P) auf Terminal-Adapter**, **12 V→5 V Step-down**,
**Relais-Modul (≥3 Kanal)**, **Optokoppler-Modul (≥3 Kanal)**, später **CAN SN65HVD230**.

Pins: siehe `esp32-pinbelegung.md`. Klemmen am VDO: `klemmenliste.md`.
Bedienteil-Adern (Set/Resume/+/−): `bedienteil-verdrahtung.md`.

## Übersicht

```
  Bedienteil-/VDO-Kabel              ESP-BOX                         VDO-Steuergerät
  ─────────────────────   ┌────────────────────────────────┐   ───────────────────
                          │                                 │
  Kl.15 +12V ───[Si 2A]──►│ Step-down 12V→5V ──► ESP 5V     │
  Masse ─────────────────►│ gemeinsame Masse ──► ESP GND    │
                          │                                 │
  Taster-Adern  ◄────────►│ Relais (3x)  COM/NO parallel    │◄──── selbe Adern gehen
  (RESUME/ACC/DEC)        │   zum jeweiligen Taster          │      1:1 weiter zum VDO
                          │                                 │
  Bremse (Kl.81) ────────►│ Optokoppler ──► GPIO15          │
  LED-Signal ────────────►│ Optokoppler ──► GPIO16          │
  (Geschwindigkeit kommt vom Spartan-Hub per WiFi – kein lokaler Reed)
                          │                                 │
                          │ GPIO17/18 ──► SN65HVD230 ──► CANH/CANL (später)
                          └────────────────────────────────┘
```
> **Wired-OR-Prinzip:** Alle Original-Adern laufen **unverändert** zum VDO weiter.
> Die ESP-Box **zapft nur parallel an** – Original bleibt voll funktionsfähig.

## 1) Stromversorgung
```
Kl.15 +12V (am Bedienteil) ──[Sicherung 2 A]──[TVS 15–18V ↯GND]──► Step-down  IN+
Masse ───────────────────────────────────────────────────────────► Step-down  IN−
Step-down OUT 5V ──► ESP "5V"   und  ► Relais-Modul VCC  und ► Opto-Modul VCC(Logik)
Step-down OUT GND ─► ESP "GND"  +  alle Modul-GND  +  Fahrzeugmasse  (GEMEINSAM!)
ESP "3V3" (vom Board) ─► optional Logikseite Opto/CAN
```
- **GEWÄHLT: 12 V von rohem Kl. 15** (Dauer-Zündungsplus, am Bedienteil) → der **ESP
  läuft immer, wenn die Zündung an ist** (Display/WiFi immer erreichbar).
- **On/Off NICHT über den Strom**: der ESP erkennt „Tempomat an/aus" am **LED-Signal (GPIO16)**.
- **TVS-Diode** (z. B. SMBJ16A) + **Verpolschutz** (Serien-Diode/P-FET) am Eingang empfohlen.
- ⚠️ **Reglerwahl:** Das vorhandene AMS1117-Board (Aufdruck „Eingang < 12 V") ist **linear**
  und **nicht für Kl.15 geeignet** (Bordnetz ~14,4 V + Spitzen → Überspannung; zudem Hitze).
  Nur für **Bench-Test** nutzen. Für den **Festeinbau: echter Schalt-Buck mit weitem Eingang**
  (z. B. **MP1584EN / LM2596**, 8–40 V → 5 V) direkt von Kl.15.

## 2) Tasten „drücken" – parallel zu den Tastern
> **Gewählt: MOSFET (IRLZ44N), siehe „Modul-Zuordnung" unten.** Relais ist die
> galvanisch getrennte Alternative (gleiche Logik: Ader 4/5/6 ↔ Masse). Beschreibung unten gilt analog.

Jeder Relais-Kontakt **COM/NO** liegt **parallel über den jeweiligen Taster**
(Signalader ↔ gemeinsame Taster-Masse). ESP zieht GPIO HIGH → Relais zu → „gedrückt".
```
ESP GPIO5 ──► Relais IN1 ;  Relais1 COM/NO ── parallel über RESUME-Taster
ESP GPIO6 ──► Relais IN2 ;  Relais2 COM/NO ── parallel über ACC/PLUS-Kontakt  (Set = kurzer Tipp)
ESP GPIO7 ──► Relais IN3 ;  Relais3 COM/NO ── parallel über DEC/MINUS-Kontakt
Relais-Modul: VCC=5V, GND=gemeinsam, IN aktiv-HIGH/-LOW je nach Board (in Firmware setzen)
```
> Exakte Bedienteil-Adern je Funktion erst per Multimeter bestätigen
> (siehe `bedienteil-verdrahtung.md`), dann Relais dort parallel klemmen.

## 3) Signale lesen – Optokoppler (EL817/PC817, 1 Kanal, **12-V-Version**)
Modul-Pinout: **INPUT (+ / −)** = Signalseite · **OUTPUT (VCC / OUT / GND)** = ESP-Seite.
**2 Module Pflicht** (Bremse, LED) **+ 1 optional** (lokaler Reed). Teile reichlich vorhanden.
```
OUTPUT-Seite (immer):  VCC→3V3 ,  GND→gemeinsame Masse ,  OUT→ESP-GPIO (interner Pull-up AN)
INPUT-Seite:
  Bremse (Kl.81,+12V)  → INPUT+ ;  Masse → INPUT−   ;  OUT → GPIO15
  LED "bereit" (Ader3) → INPUT+ ;  Masse → INPUT−   ;  OUT → GPIO16   (Polarität prüfen)
  Reed/Speed (G, opt.) → INPUT+ ;  Masse → INPUT−   ;  OUT → GPIO4    (Frequenz, Interrupt)
```
- **Active-LOW:** Signal an → Opto leuchtet → OUT = LOW (in Firmware invertieren).
- **12-V-Version** → Eingang direkt für 12 V ausgelegt, **kein Zusatzwiderstand nötig**.
- **Bremse = höchste Priorität:** erkannt → ESP bricht jede Automatik sofort ab (Sperrzeit).
- **Geschwindigkeit:** primär vom **Spartan-Hub (WiFi)**; **optional lokaler Reed an GPIO4**
  (read-only mitgehört) als Redundanz → Automatik läuft dann auch ohne Hub.
  PC817 ist schnell genug für die Reed-Frequenz.

### Reed-Doppelnutzung (VDO + ESP) – 3 Wege (siehe auch `review.md` E1)
Der Reed ist nur ein Kontakt; die Spannung kommt aus dem **VDO-Pull-up** (G1; G2 = Masse).
Ein 12-V-Opto (~1 kΩ Eingang) kann den Pegel einbrechen lassen → 65-Hz-Erkennung tot.
- **A) Test zuerst:** Opto testweise parallel (IN+→G1, IN−→G2). G1-Pegel bei offenem
  Reed > ~8 V? Tempomat noch ab ~30 km/h setzbar? → ok, fertig.
- **B) Hochohmig:** größerer Serienwiderstand vor dem Opto **oder** ohne Opto:
  G1 → 100 kΩ → GPIO4 (+ 3,3-V-Klemmung); Last ~0,1 mA, für VDO unsichtbar
  (gemeinsame Masse besteht ohnehin).
- **C) Rückwirkungsfrei: zweiter Reed nur für den ESP** an denselben Magneten
  (z. B. **Littelfuse/Hamlin 59140-Serie**, 1 NO, 10 W, Gewindezylinder mit
  Kontermuttern → einfache Montage am Blechwinkel, Abstand einstellbar).
  **Anschluss dann OHNE Opto:** `GPIO4 (interner Pull-up) ── Reed ── GND` —
  kein 12 V im Spiel, nur SW-Entprellung. Elektrisch komplett getrennt vom VDO.
Empfehlung: A testen → falls Pegel einbricht, C (Reed direkt an GPIO4).

**Bestellt: MC-38 Tür-/Fensterkontakt** als 2. Reed (Plan C):
- Anschluss: `GPIO4 (interner Pull-up) ── MC-38 ── GND`, kein Opto, SW-Entprellung.
- ⚠️ **Mitgelieferten Magnetblock NICHT an die Welle** (Fliehkraft/Unwucht) —
  nur den Reed-Block nutzen, mit den vorhandenen VDO-Kit-Magneten.
- Schaltabstand mit Kit-Magnet auf Werkbank testen (~5–10 mm statt Tür-25 mm).
- Kabelaustritt versiegeln (Spritzwasser), vibrationsfest montieren.
- Lebensdauer bei ~8000 Imp/km unbekannt (Billigteil) → als Verschleißteil
  betrachten, Ersatz bevorraten; Langzeit-Alternative: 59140 / Hall.

## 4) CAN (später)
```
ESP GPIO17 (TX) ──► SN65HVD230 TXD
ESP GPIO18 (RX) ──◄ SN65HVD230 RXD
SN65HVD230 VCC=3V3, GND gemeinsam ;  CANH/CANL ──► Fahrzeug-CAN (500 kbit/s, 11-bit)
```

## Sicherheits-/Bau-Regeln
- **Bremse bleibt hardwareverdrahtet** zum VDO – ESP liest nur mit, sitzt **nicht** im Bremspfad.
- **Eine gemeinsame Masse** für ESP + alle Module + Step-down + VDO – sonst schaltet nichts.
- Relais-Variante = galvanisch getrennt (empfohlen). MOSFET-Variante: zusätzlich TVS je Signal.
- Alles parallel → **jederzeit rückrüstbar** (ESP-Box abziehen = Originalzustand).

## Modul-Zuordnung & Stückzahl (vorhanden: 8 Opto, 10 MOSFET)

**Ausgänge „drücken" → 3 MOSFET-Module** (von 10):
| MOSFET | schaltet (Drain/OUT) | nach (Source) | Trigger ← ESP |
|--------|----------------------|---------------|----------------|
| 1 | Ader 4 = RESUME (B4) | Ader 2 = Masse | GPIO5 |
| 2 | Ader 5 = ACC/+  (B5) | Ader 2 = Masse | GPIO6 |
| 3 | Ader 6 = DEC/−  (B6) | Ader 2 = Masse | GPIO7 |
> **MOSFET-Modul (Trigger-Switch) – exakte Klemmen:**
> `VIN+` → +12 V (Kl.15) · `VIN−` → Masse · `OUT−` → **Signalader (Ader 4/5/6)** ·
> `OUT+` → **frei** · `TRIG/PWM` → ESP-GPIO (5/6/7) · Header-`GND` → Masse.
> Getriggert → OUT− wird mit VIN− (Masse) verbunden = „gedrückt".
> Gemeinsame Masse Pflicht; pro Signal eine **TVS** empfohlen.

**Eingänge „lesen" → 2 Optokoppler Pflicht + 1 optional** (EL817/PC817 12-V, von 5):
| Opto | INPUT+ | INPUT− | OUTPUT → ESP |
|------|--------|--------|--------------|
| 1 | Bremse (Kl.81, +12 V) | Masse | OUT→GPIO15, VCC→3V3, GND→Masse |
| 2 | LED „bereit" (Ader 3) | Masse | OUT→GPIO16, VCC→3V3, GND→Masse |
| 3 *(optional)* | Reed/Speed (G, read-only) | Masse | OUT→GPIO4, VCC→3V3, GND→Masse |
> Active-LOW (Signal an → OUT LOW, in SW invertieren). 12-V-Version → kein Zusatzwiderstand.
> Reed lokal = Redundanz zum Hub; hochohmig anzapfen (VDO-Signal nicht belasten), Pegel messen.

**Summe:** 3 MOSFET + 2 Optokoppler (Pflicht) + 1 Opto (optional Reed). Reserve reichlich (10 MOSFET / 5 Opto).

## Schaltplan-Bild

![ESP-Box Verkabelung](images/verkabelung-esp.png)

> Generiert mit `verkabelung-esp-diagram.py` (matplotlib) – editierbar/regenerierbar.

## Gesamtschaltplan (Bild)

![Gesamtschaltplan](images/verkabelung-gesamt.png)

Komplett: 6 Adern + B1–B6, MOSFETs (RESUME/ACC/DEC ← G5/6/7), Optokoppler (Bremse→G15, LED→G16), Buck-Versorgung (Kl.15→5V), ESP-Pins, CAN (G17/18). Generiert mit `verkabelung-gesamt-diagram.py`.

## Optokoppler-Anschluss (Bild)

![Optokoppler-Anschluss](images/anschluss-optokoppler.png)

Klemme-für-Klemme: INPUT+ = Signal (Bremse/LED), INPUT− = Masse; OUTPUT VCC→3,3V, OUT→GPIO15/16, GND→Masse. Generiert mit `anschluss-optokoppler-diagram.py`.

## MOSFET-Anschluss (Bild)

![MOSFET-Anschluss](images/anschluss-mosfet.png)

Klemme-für-Klemme (Trigger-Switch): VIN+→+12V, VIN−→Masse, OUT−→Signalader (Ader 4/5/6), OUT+ frei, TRIG/PWM→GPIO5/6/7, GND→Masse. Generiert mit `anschluss-mosfet-diagram.py`.
