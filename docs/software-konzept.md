# Software-Konzept – ESP32-S3 Tempomat-Box

## Grundprinzip: eigenständig & ausfallsicher
- Die **Tempomat-/Sicherheitslogik läuft 100 % standalone** auf dem ESP.
- **WLAN, Webinterface und CAN sind optional** (Konfig, Anzeige, Integration) —
  sie dürfen für die sichere Grundfunktion **niemals** erforderlich sein.
- Fällt WLAN/CAN/Web aus → Tempomat funktioniert unverändert weiter (Tasten,
  Geschwindigkeit halten, Brems-Reset). Reine „darüberliegende" Schicht.

## WLAN / Netzwerk (Logik wie Spartan Hub)
- **Dauerhafter AP als Fallback** (immer erreichbar, auch wenn STA verbunden ist
  → AP+STA-Modus), damit man immer „draufkommt".
- **Feste/konfigurierbare IP** (nicht dynamisch). Vorschlag passend zum Schema:
  **AP-IP `192.168.6.1`** (jedes Projekt eigenes Subnetz; bitte bestätigen).
- STA-Anbindung (Verbindung ins vorhandene Netz) — **Detail-Logik später**.
- Zugang per Browser über die feste IP.

## Webinterface (einfach)
- Status: Ist-/Soll-Geschwindigkeit, Tempomat aktiv/aus, Bremse erkannt, LED-Status.
- Konfiguration: Tacho-Impulskonstante (Hz↔km/h), Hysterese, Tastimpuls-Timing,
  Netzwerk (IP/AP), CAN-Parameter.
- Bewusst schlank (wenige Seiten), wie beim Spartan Hub.

## CAN – gemeinsam mit dem Ökosystem
- **Gleicher CAN-Bus wie alle anderen Projekte** (Spartan Hub + die 3 Projekte) →
  spätere Integration in den „ESP/Bulli-CAN".
- **Muss zum Spartan Hub passen** (gleiche Bitrate, gleiches ID-Schema/Framing).
- Transceiver: SN65HVD230 (3,3 V) an GPIO17 (TX) / GPIO18 (RX), TWAI.
- **Noch von der Spartan-Hub-Seite zu übernehmen:**
  - [ ] **Bitrate** (z. B. 250 k / 500 kbit/s?)
  - [ ] **CAN-ID-Bereich / Message-Layout** (welche IDs sendet/empfängt der Tempomat?)
  - [ ] Standard- oder Extended-IDs?

## Funktionsumfang Firmware (Erstausbau)
1. **Eingänge:** Geschwindigkeit (Frequenz, Interrupt), Bremse (Priorität),
   LED-Status, optional physische Taster.
2. **Ausgänge:** RESUME / ACC / DEC als Tastimpulse (Relais), mit Timing.
3. **Zielanfahr-Logik:** Sollwert per ACC/DEC anfahren, Hysterese, nicht gegen
   den VDO-Regler arbeiten (siehe `architektur.md`).
4. **Bremssicherheit:** Bremse = sofortiger Abbruch jeder Automatik, Sperrzeit,
   kein Auto-Wiedereinkuppeln.
5. **Telemetrie/Config:** Web + CAN (nicht funktionskritisch).

## Offene Punkte
- [ ] AP-IP bestätigen (`192.168.6.1`?) + Subnetz-Schema der 3 Projekte.
- [ ] Spartan-Hub CAN-Parameter (Bitrate, IDs, Framing).
- [ ] WiFi-STA-Logik (Reconnect, Credentials-Handling) — Detail später.
- [ ] Framework: Arduino-ESP32 oder ESP-IDF? (Spartan Hub gleich halten.)
