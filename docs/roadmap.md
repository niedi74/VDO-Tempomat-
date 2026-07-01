# Roadmap / Umsetzung

## Phase 1 – Prototyp (klobig ist ok)
Aufbau mit fertigen Modulen (lötfrei, Schraubklemmen):
- ESP32-S3 (44P) auf Terminal-Adapter
- 3× MOSFET-Modul (IRLZ44N) – RESUME/ACC/DEC
- 2–3× Optokoppler (EL817 12 V) – Bremse, LED, optional Reed
- Weitbereichs-Buck (MP1584/LM2596) 12 V→5 V + TVS/Verpolschutz/2 A
- (später) CAN-Transceiver SN65HVD230
- Verkabelung/Belegung: siehe `verkabelung-esp.md`, `esp32-pinbelegung.md`,
  `klemmenliste.md`, `bedienteil-verdrahtung.md`.

Ziel: Funktion am Fahrzeug testen (nach Urlaub, wenn Zeit ist).

## Phase 2 – Custom-PCB nach Maß
Eine integrierte Platine statt Modul-Sammlung.
- **Assembliert bestellen (PCBA, z. B. JLCPCB/PCBWay)** → SMD wird bestückt,
  **kein Eigenlöten nötig** (wichtig: Nutzer lötet nicht).
- Onboard integrieren:
  - ESP32-S3-Modul (oder Sockel/Stiftleisten)
  - Weitbereichs-Buck 12 V→5 V (+ ESP macht 3,3 V) + **Verpolschutz + TVS + Sicherung**
  - 3× Logic-Level-MOSFET (Low-Side) für RESUME/ACC/DEC
  - 3× Optokoppler (Bremse, LED, Reed)
  - CAN-Transceiver (SN65HVD230)
  - **Schraubklemmen** für: Kl.15/Masse, Bedienteil 6-adrig (B1–B6),
    Bremse (Kl.81), Reed (G), CAN (H/L)
- Grundlage = diese Doku (Pinbelegung → Netzliste, Modul-Zuordnung → Bauteile).

## Firmware (parallel, jederzeit)
- PlatformIO + Arduino-ESP32 (wie Spartan-Hub).
- Reihenfolge: Standalone-Tempomatlogik → WLAN/AP + Web-GUI → WiFi-Anbindung
  Touchdisplay → CAN. Details: `software-konzept.md`.

## Status
- Hardware-/Verkabelungs-Planung: **abgeschlossen & dokumentiert.**
- Nächster aktiver Schritt (wenn es weitergeht): Prototyp verdrahten **oder**
  Firmware-Gerüst / PCB-Schaltplan starten.
