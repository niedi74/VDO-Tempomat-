# Flash-Anleitung – Reed-Simulator

- **Repo:** `niedi74/VDO-Tempomat-`
- **Branch:** `claude/schaltplan-upload-bum30q`
- **Datei:** `firmware/reed-simulator/reed-simulator.ino`
- **Chip:** ESP32-**S3** (Xtensa LX7) — nicht der klassische ESP32!
- **Board (Arduino IDE):** „ESP32S3 Dev Module"
- **FQBN (arduino-cli):** `esp32:esp32:esp32s3`
- **Port:** COM16
- **Baudrate Serial Monitor:** 115200
- **PIN_OUT:** GPIO8 (nicht GPIO26–37 nutzen → Octal-PSRAM/Flash auf S3)

## Schritte
1. Branch pullen/klonen.
2. `reed-simulator.ino` in Arduino IDE öffnen.
3. Werkzeuge → Board → **ESP32S3 Dev Module**.
4. Werkzeuge → Port → **COM16**.
5. Hochladen (Pfeil-Symbol).
   - Falls Verbindungsfehler: beim Start des Uploads BOOT-Taster am Board
     gedrückt halten, bis „Connecting..." erscheint.
6. Serial Monitor öffnen, **115200 Baud** einstellen.
   - Bleibt es stumm: „USB CDC On Boot" im Tools-Menü umschalten.

## Erwartete Ausgabe nach dem Boot
```
=== VDO-Tempomat Reed-Simulator ===
Befehle: f<Hz>  v<km/h>  stop  sweep  status
[SIM] f=0.0 Hz  (~0.0 km/h)  VDO-Schwelle 65Hz: zu niedrig
```

Details/Verkabelung: `README.md` in diesem Ordner. Sicherheitshinweise/
Testablauf: `../../docs/test-ohne-reed.md`.
