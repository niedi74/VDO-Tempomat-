# Flash-Anleitung – Reed-Simulator

- **Repo:** `niedi74/VDO-Tempomat-`
- **Branch:** `claude/schaltplan-upload-bum30q`
- **Datei:** `firmware/reed-simulator/reed-simulator.ino`
- **Board:** ESP32 Dev Module
- **Port:** COM16
- **Baudrate Serial Monitor:** 115200

## Schritte
1. Branch pullen/klonen.
2. `reed-simulator.ino` in Arduino IDE öffnen.
3. Werkzeuge → Board → **ESP32 Dev Module**.
4. Werkzeuge → Port → **COM16**.
5. Hochladen (Pfeil-Symbol).
   - Falls Verbindungsfehler: beim Start des Uploads BOOT-Taster am Board
     gedrückt halten, bis „Connecting..." erscheint.
6. Serial Monitor öffnen, **115200 Baud** einstellen.

## Erwartete Ausgabe nach dem Boot
```
=== VDO-Tempomat Reed-Simulator ===
Befehle: f<Hz>  v<km/h>  stop  sweep  status
[SIM] f=0.0 Hz  (~0.0 km/h)  VDO-Schwelle 65Hz: zu niedrig
```

Details/Verkabelung: `README.md` in diesem Ordner. Sicherheitshinweise/
Testablauf: `../../docs/test-ohne-reed.md`.
