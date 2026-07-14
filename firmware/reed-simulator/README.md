# Reed-Simulator (separates Testgerät)

Eigenständiger ESP32 + 1 MOSFET-Modul, simuliert den Geschwindigkeits-Reed
elektronisch, damit der VDO-Tempomat ohne montierte Kardanwellen-Sensorik
getestet werden kann. Details/Sicherheitshinweise: `../../docs/test-ohne-reed.md`.

## Verkabelung

```
MOSFET-Modul VIN+  ── +12 V (Kl.15)
MOSFET-Modul VIN−  ── Masse
MOSFET-Modul OUT−  ── G1 (VDO-Geschwindigkeitseingang, statt Reed)
MOSFET-Modul TRIG  ── ESP32 GPIO8 (PIN_OUT im Sketch)
ESP32 GND          ── gemeinsame Masse mit MOSFET-Modul + VDO
```

## Flashen
- Board: **ESP32-S3** (Xtensa LX7) — Arduino IDE: Werkzeuge → Board →
  **„ESP32S3 Dev Module"**. arduino-cli FQBN: `esp32:esp32:esp32s3`.
- Keine zusätzlichen Libraries nötig — nur ESP32-Board-Package installiert.
- `reed-simulator.ino` hochladen, Serial Monitor auf **115200 Baud**.
- Falls Serial Monitor stumm bleibt: **„USB CDC On Boot"** im Tools-Menü
  umschalten (Enabled/Disabled), je nachdem ob das Board natives USB oder
  einen UART-Brückenchip nutzt.

## Bedienung (Serial Monitor)
| Befehl | Wirkung |
|--------|---------|
| `f100` | Frequenz direkt setzen (Hz), z. B. 100 Hz |
| `v45`  | Frequenz aus simulierter Geschwindigkeit (km/h) berechnen |
| `stop` bzw. `0` | Ausgang abschalten — sicherer Ruhezustand |
| `sweep` | Rampe 0 → 100 km/h über 20 Sekunden |
| `status` | aktuellen Zustand erneut ausgeben |

Kalibrierung `IMP_PER_KM = 8000.0` im Sketch entspricht 4 Magneten an der
Kardanwelle (~2000 U/km). Bei Bedarf anpassen. VDO-Schwelle: **65 Hz**.

## ⚠️ Sicherheit
Startet immer mit 0 Hz. Vor dem Testen: Handbremse an, Leerlauf/Parkstellung,
Räder unterlegt — ein simuliertes Speed-Signal lässt den VDO glauben, das
Fahrzeug fährt, und zieht bei Set/Resume am Gaszug. Details: `test-ohne-reed.md`.
