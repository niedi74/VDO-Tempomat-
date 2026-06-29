# ESP32-S3 (44P) – Pinbelegung der Inline-Box

Board: **ESP32-S3 44P** auf Schraubklemmen-Terminal-Adapter (lötfrei).
Konzept: Original-Leitungen rein → ESP-Box (Taps + Relais/Opto) → wieder raus
zum Original-Steuergerät. CAN-Transceiver für Touch-Display.

```
Kabelbaum/Bedienteil ─► [ Terminal-Adapter + ESP32-S3 ] ─► VDO-Steuergerät
                          • Relais parallel zu Tastern (drücken)
                          • Optokoppler lesen (LED/Bremse/Speed)
                          • CAN-Transceiver ◄─► Touch-Display
```

## Sichere GPIO-Wahl (ESP32-S3)
**Vermieden:** GPIO0/3/45/46 (Strapping/Boot), 19/20 (USB), 43/44 (UART0-Konsole),
26–37 (Flash/Octal-PSRAM). Benutzte Pins sind alle frei nutzbar.

## Ausgänge – Taster „drücken" (→ Relais-/MOSFET-Modul)
| Funktion | GPIO (Klemme) | wirkt auf |
|----------|---------------|-----------|
| **RESUME** | **GPIO5** | Relais 1 → COM/NO parallel zum RESUME-Taster |
| **ACC** (schneller) | **GPIO6** | Relais 2 → parallel zum ACC-Kontakt |
| **DEC** (langsamer) | **GPIO7** | Relais 3 → parallel zum DEC-Kontakt |

> Ein/Aus-Kippschalter bleibt **manuell** (kein ESP-Kanal).

## Eingänge – mitlesen (über Optokoppler-Modul)
| Signal | GPIO (Klemme) | Hinweis |
|--------|---------------|---------|
| **Geschwindigkeit (Reed G)** | **GPIO4** | Frequenz, Interrupt/Pulszählung; min. 65 Hz |
| **Bremssignal (V1 / Kl.81)** | **GPIO15** | +12 V = gebremst → Opto → 3,3 V; höchste Priorität |
| **LED „bereit"** | **GPIO16** | Status vom Bedienteil mitlesen |

## CAN (TWAI) → Touch-Display
| Signal | GPIO (Klemme) | an Transceiver (z. B. SN65HVD230 / TJA1051) |
|--------|---------------|---------------------------------------------|
| **CAN TX** | **GPIO17** | TXD |
| **CAN RX** | **GPIO18** | RXD |

## Optional (falls gewünscht)
| Zweck | GPIO |
|-------|------|
| physische Taster mitlesen (RESUME/ACC/DEC-Stellung) | GPIO8 / GPIO9 / GPIO10 |
| Touch-Display direkt per I²C statt CAN | SDA=GPIO11, SCL=GPIO12 |

## Stromversorgung
- **12 V (V3 / Kl.15)** → 12 V→5 V Step-down → **5V-Klemme** des Adapters.
- **Masse (V2)** → **GND-Klemme** (gemeinsame Masse für ESP + Module + Steuergerät).
- 3,3 V erzeugt das ESP-Board selbst (für Optokoppler-Logikseite nutzbar).

## Wichtige Regeln (aus dem Projekt)
- **Bremse bleibt hardwareverdrahtet** (VDO-Reset unabhängig vom ESP); ESP liest nur mit.
- ESP **niemals** ACC/RESUME senden, solange Bremssignal aktiv/gerade war.
- Relais-Lösung = galvanisch getrennt; bei MOSFET-Variante: gemeinsame Masse + TVS.
- Original-Funktion bleibt erhalten (Box nur parallel) → jederzeit rückrüstbar.

## Noch festzulegen
- [ ] An welchen **Bedienteil-Adern** liegen RESUME/ACC/DEC genau (per Multimeter, vgl. `bedienteil-verdrahtung.md`).
- [ ] Display: über CAN (eigener Bus) oder direkt I²C/SPI?
- [ ] Modulwahl final: Relais-Modul (empfohlen) vs. MOSFET-Modul.
