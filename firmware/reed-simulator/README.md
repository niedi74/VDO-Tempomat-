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
- Erscheint im Boot-Log `[E] ... Invalid pin: X` / `is not set as GPIO` →
  der konfigurierte `PIN_OUT` existiert auf diesem Chip nicht (z. B. GPIO25
  gibt es nur auf dem klassischen ESP32, nicht auf S3). Sketch läuft dann
  scheinbar normal weiter, der MOSFET-Ausgang schaltet aber **nie** — Pin
  gegen die aktuelle Board-Pinbelegung prüfen.

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

## Falls später WiFi dazukommt (aktuell nicht vorhanden)
Aus dem Nachbarprojekt `spartan3v2-can-adapter` (gleiche Board-Familie,
ESP32-S3-DevKitC-Klone) sind zwei Stolpersteine bereits gelöst — als Vorlage,
falls der Reed-Simulator später Netzwerkfunktionen bekommt:
- **Nicht-eindeutige Werks-MAC bei billigen S3-Klon-Chips** → manuelle
  MAC-Override via `esp_wifi_set_mac()`. Referenz: `spartan3v2-can-adapter/
  src/main.cpp`, Marker `WIFI-MAC-OVR`.
- **Statische IP je WLAN-Profil** (sonst wechselt IP bei jedem Boot) →
  `applyStaticIpIfNeeded()` in `spartan3v2-can-adapter/src/main.cpp`.

## ⚠️ Sicherheit
Startet immer mit 0 Hz. Vor dem Testen: Handbremse an, Leerlauf/Parkstellung,
Räder unterlegt — ein simuliertes Speed-Signal lässt den VDO glauben, das
Fahrzeug fährt, und zieht bei Set/Resume am Gaszug. Details: `test-ohne-reed.md`.
