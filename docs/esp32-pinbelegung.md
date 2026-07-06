# ESP32-S3 (44P) – Pinbelegung der Inline-Box (final)

Board: **ESP32-S3 44P** auf Schraubklemmen-Terminal-Adapter (lötfrei).
Konzept: Original-Leitungen rein → ESP-Box (Relais/Opto + WiFi) → wieder raus
zum VDO-Steuergerät. Original-Funktion bleibt parallel erhalten (rückrüstbar).

```
Kabelbaum/Bedienteil ─► [ Terminal-Adapter + ESP32-S3 ] ─► VDO-Steuergerät
                          • 3 MOSFET-Module parallel zu Tastern (Set/Resume/+/−)
                          • Optokoppler lesen (Bremse / LED / optional Reed)
                          • WiFi (AP 192.168.6.1 + STA am Spartan-Hub)
                          • CAN-Transceiver (später)
```

## Master-Pinbelegung

| GPIO | Klemme | Richtung | Funktion | Angeschlossen an | Status |
|------|--------|----------|----------|------------------|--------|
| **5**  | 5  | OUT | **RESUME** (Reset) | MOSFET M1 (TRIG) → OUT− parallel zum RESUME-Taster (Ader 4/B4) | fest |
| **6**  | 6  | OUT | **PLUS / ACC** (schneller; Set = kurzer Tipp) | MOSFET M2 (TRIG) → OUT− parallel zum ACC-Kontakt (Ader 5/B5) | fest |
| **7**  | 7  | OUT | **MINUS / DEC** (langsamer) | MOSFET M3 (TRIG) → OUT− parallel zum DEC-Kontakt (Ader 6/B6) | fest |
| **15** | 15 | IN  | **Bremssignal** (V1 / Kl.81, +12 V = gebremst) | Optokoppler → 3,3 V; höchste Priorität | fest |
| **16** | 16 | IN  | **LED „bereit"** mitlesen | Optokoppler vom Bedienteil-LED-Signal | fest |
| **4**  | 4  | IN  | **Geschwindigkeit (Reed)** – lokal mithören (hochohmig, read-only), redundant zum Hub | Optokoppler + Pulszählung (Interrupt) | optional |
| **17** | 17 | OUT | **CAN TX** | SN65HVD230 TXD | später |
| **18** | 18 | IN  | **CAN RX** | SN65HVD230 RXD | später |
| **8**  | 8  | IN  | Taster RESUME mitlesen | parallel zum phys. Taster (für Display-Status) | Reserve |
| **9**  | 9  | IN  | Taster ACC mitlesen | parallel zum phys. Taster | Reserve |
| **10** | 10 | IN  | Taster DEC mitlesen | parallel zum phys. Taster | Reserve |
| **48** | 48 | OUT | Status-LED (onboard RGB, falls vorhanden) | — | optional |

## Stromversorgung
| Klemme | Anschluss |
|--------|-----------|
| **5V** | von 12 V→5 V Step-down, **gespeist von rohem Kl. 15** (Dauer-Zündungsplus, am Bedienteil) |
| **GND** | gemeinsame Masse (ESP + Relais/Opto + Step-down + VDO-Steuergerät) |
| 3V3 | erzeugt das Board selbst (für Optokoppler-Logikseite nutzbar) |

- **ESP läuft immer, wenn Zündung an** (Display/WiFi immer erreichbar).
- **On/Off NICHT über den Strom:** der ESP erkennt „Tempomat an/aus" am **LED-Signal (GPIO16)**.
- **Config persistent in NVS/Flash** (ESP geht mit Zündung aus).

## Sichere-GPIO-Hinweise (ESP32-S3)
- **Vermieden:** GPIO0/3/45/46 (Strapping/Boot), 19/20 (USB), 43/44 (UART0-Konsole),
  26–37 (Flash/Octal-PSRAM). Alle oben genutzten Pins sind frei verwendbar.
- TWAI/CAN ist auf dem S3 frei zuweisbar → GPIO17/18 (kein GPIO25/26 wie beim klass. ESP32).

## Wichtige Regeln
- **Bremse bleibt hardwareverdrahtet** (VDO-Reset unabhängig vom ESP); ESP liest nur mit.
- ESP **niemals** Set/Resume/Plus senden, solange Bremssignal aktiv/gerade war (Sperrzeit).
- **Gewählt: MOSFET-Module** (gemeinsame Masse Pflicht, TVS pro Signalleitung empfohlen,
  **Pull-down an jeder TRIG-Leitung** → „ESP tot = losgelassen"). Relais bleibt die
  galvanisch getrennte Alternative.
- Original-Bedienteil bleibt voll funktionsfähig (ESP nur parallel).

## Bezug zu anderen Docs
- Adern→Klemmen am VDO-Gerät: `klemmenliste.md`
- Bedienteil-Adern (Set/Resume/+/−): `bedienteil-verdrahtung.md`
- Netzwerk/CAN/GUI: `software-konzept.md`
