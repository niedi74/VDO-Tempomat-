# Software-Konzept – ESP32-S3 Tempomat-Box

## Grundprinzip: eigenständig & ausfallsicher
- Die **Tempomat-/Sicherheitslogik läuft 100 % standalone** auf dem ESP.
- **WLAN, Webinterface und CAN sind optional** (Konfig, Anzeige, Integration) —
  sie dürfen für die sichere Grundfunktion **niemals** erforderlich sein.
- Fällt WLAN/CAN/Web aus → Tempomat funktioniert unverändert weiter (Tasten,
  Geschwindigkeit halten, Brems-Reset). Reine „darüberliegende" Schicht.

## WLAN / Netzwerk (Logik wie Spartan Hub) — AP+STA
- **STA (Client):** Tempomat verbindet sich mit dem **Spartan-Hub-AP** (`192.168.4.1`)
  → Touchdisplay & Hub erreichen ihn, Geschwindigkeit kommt über dieses Netz.
- **AP (Fallback, immer an):** eigener AP **`192.168.6.1`** (fix) zum Testen unterwegs,
  wenn der Hub nicht da ist. (AP+STA gleichzeitig.)
- **Erreichbarkeit im Hub-Netz:** dort vergibt der Hub die IP (DHCP) → für das Display
  nicht fix. Lösung: **feste STA-IP** (z. B. `192.168.4.50`) **oder mDNS** (`tempomat.local`).
- **Boot:** ESP wird mit dem physischen Schalter eingeschaltet, bootet in ~1–2 s;
  manuelle VDO-Funktion ist sofort da, ESP-Page/Anzeige nach dem Boot.

## Webinterface (einfach) — Stil wie Spartan Hub
- **Nur das Devboard-/Setup-Gerüst vom Spartan übernehmen** (Optik/Struktur,
  Board-/Pin-Setup, variable Parameter) — **nicht** die Spartan-spezifischen
  Felder (Lambda etc.).
- **„Live"-Seite = die Tempomat-Page** (bewusst einfach gehalten):
  Ist-/Soll-Geschwindigkeit, Tempomat aktiv, Bremse erkannt, LED-Status; plus
  Bedienung Resume/ACC/DEC.
- Konfiguration: Hysterese, Tastimpuls-Timing, Netzwerk (IP/AP), CAN-Parameter,
  Geschwindigkeitsquelle (Hub vs. lokaler Reed).

## On/Off — implizit über den physischen Schalter
- **Kein Software-On/Off.** Der physische Ein/Aus-Kippschalter **versorgt den ESP
  erst mit Strom**: Schalter aus → ESP stromlos/aus; Schalter an → ESP bootet,
  System bereit.
- Heißt: **ESP läuft = Tempomat-System „an"**. Die GUI muss kein On/Off bieten;
  „erreichbar" = „an".

## Geschwindigkeitsquelle & Integration ins Spartan-Ökosystem
- **Die Geschwindigkeit kommt primär vom Spartan Hub** (der liest den Reed-Sensor,
  vgl. Spartan-Repo „GPIO27 Speed reed sensor"). Der Tempomat-ESP **konsumiert**
  die Geschwindigkeit → es geht primär ums **Auslesen/Telemetrie**.
- **Kopplung aktuell: WiFi-only** (kein ESP-NOW — verworfen). Der Tempomat-ESP stellt
  eine **HTTP/JSON-API** bereit; das **Spartan-Touchdisplay (Cockpit-Frontend)** holt
  sich darüber Status und kann Kommandos senden. **CAN kommt später** dazu.
- **Touchdisplay-Tempomat-Page:** zusätzliche Seite im vorhandenen Spartan-Frontend
  → **primär Status anzeigen**; **Setzen (Resume/ACC/DEC) auch ohne Schalter** möglich
  (Display-Befehl → ESP feuert die Relais).
- **Wichtig (Sicherheit):** Die **manuelle VDO-Funktion läuft immer standalone**
  (Halten/Set/Resume macht das VDO-Gerät; Reed geht hardwareseitig direkt ans VDO).
  Nur die **automatische Zielanfahr-Logik des ESP** braucht einen Geschwindigkeitswert
  → kommt vom Hub. Fällt der Hub/Link aus, entfällt nur die ESP-Automatik, **nicht**
  der Tempomat selbst.
- **Optionaler lokaler Fallback:** ESP kann den Reed zusätzlich selbst mitlesen
  (GPIO4), falls man die Zielanfahr-Automatik unabhängig vom Hub haben will.

## CAN – gemeinsam mit dem Ökosystem
Referenz: `niedi74/spartan3v2-can-adapter` (gleicher Bus, gleiche Konventionen).
- **Bitrate: 500 kbit/s**, **11-bit Standard-IDs** (wie Spartan).
- **Transceiver: SN65HVD230** (3,3 V). TWAI auf ESP32-S3 frei wählbar → GPIO17 (TX) / GPIO18 (RX)
  (S3 hat kein GPIO25/26 wie der klassische ESP32 – Pins sind beim S3 remappbar, daher andere Nummern, gleicher Bus).
- **Belegte ID (nicht verwenden):** `0x400` = Spartan-Lambda (50 Hz, 4 Byte big-endian).
- **Vorschlag Tempomat-IDs (bitte gegen Gesamt-ID-Map bestätigen):**
  - `0x420` = Tempomat-Status senden (Ist/Soll-Geschwindigkeit, aktiv, Bremse)
  - `0x421` = Tempomat-Kommando empfangen (Set/Resume/+/− von außen, z. B. Cockpit)
- [ ] Vollständige **ID-Allokation der 3 Projekte** bestätigen, damit nichts kollidiert.

## Framework & Ökosystem-Konventionen (vom Spartan übernommen)
- **PlatformIO + Arduino-ESP32** (gleich wie Spartan).
- **Kein ESP-NOW** (verworfen). Cockpit-Anbindung **jetzt per WiFi**, **CAN später**.
- Web-GUI-Stil analog Spartan halten.

## Funktionsumfang Firmware (Erstausbau)
1. **Eingänge:** Geschwindigkeit (Frequenz, Interrupt), Bremse (Priorität),
   LED-Status, optional physische Taster.
2. **Ausgänge = die einzige aktive ESP-Funktion:** **Set / Resume / Plus / Minus**
   (Geschwindigkeit). Realisierung über **3 Relais-Kanäle**: Plus = ACC, Minus = DEC,
   Resume = RESUME; **Set = kurzer ACC-Tipp** (eigene Wire dafür nicht nötig).
   Tastimpulse mit definiertem Timing.
3. **Zielanfahr-Logik:** Sollwert per ACC/DEC anfahren, Hysterese, nicht gegen
   den VDO-Regler arbeiten (siehe `architektur.md`).
4. **Bremssicherheit:** Bremse = sofortiger Abbruch jeder Automatik, Sperrzeit,
   kein Auto-Wiedereinkuppeln.
5. **Telemetrie/Config:** Web + CAN (nicht funktionskritisch).

## Offene Punkte
- [ ] Tempomat-CAN-IDs bestätigen (`0x420`/`0x421`?) gegen Gesamt-ID-Map der 3 Projekte.
- [ ] CAN-Message-Layout Tempomat festlegen (Byte-Belegung Status/Kommando).
- [ ] WiFi-STA-Logik (Reconnect, Credentials-Handling) — Detail später.
- [ ] HTTP/JSON-API definieren (Status-Felder + Kommandos Resume/ACC/DEC) fürs Touchdisplay.
