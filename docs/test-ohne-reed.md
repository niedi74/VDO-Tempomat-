# Erster Funktionstest ohne montierten Reed

Status: ESP-Box + MOSFETs + Optos installiert, **Reed (Kardanwelle) noch nicht
montiert**. Trotzdem End-to-End-Test möglich, indem ein MOSFET-Kanal den Reed
elektronisch simuliert.

## Frequenz-Anforderung (Erinnerung)
- VDO braucht **min. 65 Hz kontinuierlich** an G1/G2, sonst lässt sich „Set"
  nicht betätigen (Original-Schaltplan, siehe `schaltplan.md`).
- Mit dem geplanten Kardanwellen-Reed (4 Magnete, ~8000 Imp/km) entspricht das
  **~29–30 km/h** — passt zum Handbuch („ab ca. 30–40 km/h setzbar").
- Handbuch-Bench-Test-Alternative: 4 Magnete + Bohrmaschine ≥1000 U/min
  → 1000/60 × 4 = 66,7 Hz (knapp über Schwelle).

## Reed-Simulator (elektronisch, kein Drehen nötig)
**Fertige Firmware:** `firmware/reed-simulator/` (eigenständiger, zweiter ESP32
+ 1 MOSFET-Modul, separat von der Tempomat-Box). Serial-Befehle `f<Hz>`,
`v<km/h>`, `stop`, `sweep`, `status` — siehe README dort.
```
MOSFET VIN+ → +12 V (Kl.15)      MOSFET OUT− → G1 (VDO-Geschwindigkeitseingang,
MOSFET VIN− → Masse                            statt echtem Reed-Kontakt)
MOSFET TRIG ← ESP32 GPIO25 (Reed-Simulator-Sketch)
```
Elektrisch identisch zu einem schließenden Reed-Kontakt — VDO kann nicht
unterscheiden. Testfrequenz z. B. **100 Hz** (≈ 45 km/h simuliert).

## ⚠️ Sicherheit vor dem Test
Ein simuliertes Speed-Signal lässt den VDO glauben, das Fahrzeug fährt — bei
Set/Resume zieht die Unterdruckpumpe am Gaszug, **auch im Stand**:
- Handbremse an, Leerlauf/Parkstellung, Räder unterlegt.
- Falls Bowdenzug zum Gas schon mechanisch verbunden ist: besonders vorsichtig.
- Guter Nebentest: **Bremspedal drücken**, während „aktiv" simuliert wird →
  muss sofort auskuppeln (testet gleich die Bremssicherheit mit).

## Testablauf
1. Reed-Simulator-Kanal wie oben verkabeln (an G1/G2, nicht an die
   Bedienteil-Adern).
2. `firmware/reed-simulator/reed-simulator.ino` auf den zweiten ESP32 flashen,
   Serial Monitor öffnen (115200 Baud). Startet mit 0 Hz (sicher).
3. Zündung an, Tempomat-Kippschalter an → LED „bereit"?
4. Serial-Befehl `v45` (≈45 km/h, weit über 65-Hz-Schwelle) → Frequenz auf
   ≥65 Hz stellen.
5. RESUME/ACC/DEC-Kanäle einzeln testen (Set, Halten, Loslassen) — reagiert
   der VDO wie erwartet?
6. Bremstest: Bremssignal aktivieren → Tempomat muss sofort deaktivieren.
7. Danach: `stop` (0 Hz) → Set darf nicht mehr funktionieren (Plausibilitätscheck).
8. Optional: `sweep` für eine Rampe 0→100 km/h über 20 s (Hysterese-Verhalten
   beobachten).

## Danach
Reed-Simulator-Kanal wieder abklemmen bzw. per Firmware-Flag deaktivieren,
sobald der echte Reed (Kardanwelle + MC-38/WEDER) montiert ist.
