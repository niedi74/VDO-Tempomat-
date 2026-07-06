# Konzept-Review (Mehrfach-Durchlauf, Juli 2026)

Review über alle Docs (`architektur`, `software-konzept`, `esp32-pinbelegung`,
`verkabelung-esp`, `klemmenliste`, `schaltplan`, `handbuch`, `roadmap`).
Vier Schleifen: Sicherheit → Elektrik → Software → Perspektiven.

## Schleife 1 – Sicherheit

**Stark:** Bremse hardwareverdrahtet (ESP nie im Bremspfad), Parallel-Prinzip
rückrüstbar, VDO bleibt Regler + Sicherheitsinstanz. Fundament korrekt.

- 🔴 **S1 „klemmender ACC":** ESP-Absturz während gehaltenem ACC-MOSFET =
  Fahrzeug beschleunigt weiter; nach Brems-Auskupplung könnte gehaltener ACC
  wieder eingreifen. Maßnahmen:
  - Firmware: **MAX_PULSE_MS** (Halten ≤ 5–10 s, Tipp ≤ 300 ms), Task-Watchdog.
  - Hardware: **Pull-downs an allen TRIG-Leitungen** (Module prüfen, ob onboard
    vorhanden; sonst 10 kΩ extern) → „ESP tot = losgelassen".
  - Phase-2-PCB: Hardware-Impulsbegrenzer (Monoflop) und/oder **Brems-Inhibit
    in Hardware** (Bremse trennt TRIG-Versorgung) = zweiter Kanal.
- 🟠 **S2 Boot-Glitches:** GPIOs können beim Boot floaten → Phantom-Tastendruck
  bei Zündung an. Fix: Pull-downs + GPIO-Init (LOW/OUTPUT) als Erstes im Setup.
- 🟠 **S3 Web-Kommandos = Taster im fahrenden Auto:** AP-Passwort ordentlich,
  `POST /api/cmd` mit Token + Rate-Limit absichern.

## Schleife 2 – Elektrik/Hardware

- 🔴 **E1 Reed-Abgriff nicht automatisch hochohmig:** 12-V-EL817-Module ziehen
  am Eingang ~10 mA (≈1 kΩ). Kann das Reed-Signal fürs VDO (65-Hz-Erkennung!)
  verfälschen. **Vor Festverdrahtung messen**, ob Signal am VDO einbricht;
  ggf. größerer Serienwiderstand oder Puffer (Transistor/Komparator).
- 🟡 **E2 Doku-Inkonsistenz Relais↔MOSFET:** behoben mit diesem Commit
  (MOSFET ist der gewählte Weg; Relais = Alternative).
- 🟡 **E3 MOSFET-Module:** VIN+ (12 V) muss angeschlossen sein, sonst schaltet
  TRIG nichts (Treiberstufe wird aus VIN+ versorgt). Im Plan korrekt.
- 🟢 **E4 Frequenz-Mathe bestätigt Kardan-Reed:** ~2000 U/km × 4 Magnete
  ≈ 8000 Imp/km → 65 Hz bei ~29 km/h, ~220 Hz bei 100 km/h. Passt exakt zum
  Handbuch („ab 30–40 km/h"). Louis-Tachowellen-Adapter unnötig (zudem kein
  Pass-Through → Nadel stünde).
- 🟢 **E5 Versorgung:** rohes Kl.15 + Weitbereichs-Buck + TVS/Sicherung/
  Verpolschutz korrekt entschieden. PCB-Detail: Sicherung nah am Abgriff.

## Schleife 3 – Software/Architektur

- 🟠 **W1 Stale-Data-Guard:** Hub-Geschwindigkeit (WiFi) mit Zeitstempel
  versehen; **älter als ~500 ms → Zielanfahr-Automatik pausiert** (VDO hält
  weiter; ungefährlich, aber sauber).
- 🟡 **W2 Ehrliche Grenze:** ESP kennt echten VDO-Zustand nicht (nur LED +
  Geschwindigkeit). Manuell gesetzte Sollwerte/Einkupplung unsichtbar →
  GUI soll „Soll (ESP)" anzeigen, nicht „Soll"; Einkupplung höchstens
  heuristisch.
- 🟢 **W3 Schichtung richtig:** Standalone-Kern → Web/WiFi → CAN als Aufsätze;
  On/Off via LED-Signal.
- 🟡 **W4 OTA von Anfang an** (Web-/ArduinoOTA) — Box ist später verbaut.

## Schleife 4 – Perspektiven

Ohne neue Hardware (nur Firmware):
1. **Limiter-Modus** (Maximaltempo → DEC-Tipp/Warnung).
2. **±1-km/h-Nudge** am Touchdisplay (kurzer ACC/DEC-Tipp).
3. **Selbsttest-Modus:** freier GPIO erzeugt 65-Hz-PWM ins Reed-Opto →
   komplette Kette auf der Werkbank testbar („Trockenübung" wie im Handbuch).
4. **Fahrten-/Ereignis-Logging** (Engage, Brems-Abbrüche, Speed-Profil) im
   Flash-Ringpuffer, abrufbar per Web-GUI.
5. **CAN-Ökosystem:** Status auf `0x420` → nutzbar für künftige Module;
   Hub-Display vereint Lambda + Speed + Cruise.

Mit kleinen Erweiterungen (später):
6. **GPS als dritte Speed-Quelle** (Plausibilisierung Reed↔Hub↔GPS).
7. **Phase-2-PCB mit Hardware-Sicherheitsstufe** (Brems-Inhibit +
   Impulsbegrenzer) → abgestürzter ESP physikalisch harmlos.
8. Kupplungssignal: **N/A** (Automatik, T9-Brücke).

## Priorisierte Merkliste vor dem ersten Einbau

| Prio | Punkt | Aufwand |
|---|---|---|
| 1 | Pull-downs an TRIG prüfen/nachrüsten + MAX_PULSE_MS in Firmware | klein |
| 2 | Reed-Abgriff auf Signalbelastung prüfen (65 Hz am VDO!) | Messung |
| 3 | API-Token/Passwort für Kommando-Endpoint | klein |
| 4 | Stale-Data-Guard (Speed-Zeitstempel) | klein |
| 5 | OTA einbauen | klein |
| 6 | Doku Relais→MOSFET vereinheitlicht | ✅ erledigt |
