/*
  Reed-Signal-Simulator fuer VDO-Tempomat-Test
  ---------------------------------------------
  Board: ESP32-S3 (Xtensa LX7). Separates Devboard + 1x MOSFET-Modul
  (IRLZ44N-Typ, wie im Hauptprojekt).
  Erzeugt ein Rechtecksignal, das das MOSFET-Modul auf G1 (VDO-
  Geschwindigkeitseingang) schaltet -- elektrisch identisch zu einem
  schliessenden Reed-Kontakt. Siehe docs/test-ohne-reed.md im Hauptrepo.

  Verkabelung:
    MOSFET-Modul VIN+  -> +12V (Kl.15)
    MOSFET-Modul VIN-  -> Masse
    MOSFET-Modul OUT-  -> G1 (VDO Geschwindigkeitseingang, statt Reed)
    MOSFET-Modul TRIG  -> PIN_OUT (siehe unten)
    ESP32-GND          -> gemeinsame Masse mit MOSFET-Modul + VDO

  Bedienung ueber Serial Monitor, 115200 Baud:
    f<Hz>     Frequenz direkt setzen, z.B.  f100
    v<km/h>   Frequenz aus Geschwindigkeit, z.B.  v45
    0 / stop  Ausgang abschalten (0 Hz) -- sicherer Ruhezustand
    sweep     Rampe 0 -> 100 km/h ueber 20 Sekunden
    status    aktuellen Zustand erneut ausgeben

  Sicherheit: Startet immer mit 0 Hz. Vor jedem Test: Handbremse an,
  Leerlauf/Parkstellung, Raeder unterlegt (siehe docs/test-ohne-reed.md).
*/

#include <Arduino.h>

// ---- Konfiguration ----
const int PIN_OUT = 8;               // GPIO an MOSFET-TRIG (ESP32-S3: sicherer Pin,
                                      // NICHT 26-37 nutzen -> Octal-PSRAM/Flash)
const double IMP_PER_KM = 8000.0;    // Kalibrierung: 4 Magnete x ~2000 U/km Kardanwelle
const double MIN_HZ_VDO = 65.0;      // VDO-Mindestfrequenz zum Setzen der Geschwindigkeit

// ---- Zustand ----
double targetHz = 0.0;
bool outputState = false;
unsigned long lastToggleUs = 0;
unsigned long halfPeriodUs = 0;

bool sweepActive = false;
unsigned long sweepStartMs = 0;
unsigned long lastSweepPrintMs = 0;
const unsigned long SWEEP_DURATION_MS = 20000;
const double SWEEP_MAX_KMH = 100.0;

double hzFromKmh(double kmh) {
  return kmh * IMP_PER_KM / 3600.0;
}

double kmhFromHz(double hz) {
  return hz * 3600.0 / IMP_PER_KM;
}

void printStatus() {
  Serial.print("[SIM] f=");
  Serial.print(targetHz, 1);
  Serial.print(" Hz  (~");
  Serial.print(kmhFromHz(targetHz), 1);
  Serial.print(" km/h)  VDO-Schwelle 65Hz: ");
  Serial.println(targetHz >= MIN_HZ_VDO ? "ERREICHT" : "zu niedrig");
}

void setFrequency(double hz) {
  targetHz = hz;
  if (hz <= 0.0) {
    halfPeriodUs = 0;
    digitalWrite(PIN_OUT, LOW);
    outputState = false;
  } else {
    halfPeriodUs = (unsigned long)(500000.0 / hz); // halbe Periode in µs
  }
  printStatus();
}

void processCommand(String cmd) {
  cmd.toLowerCase();
  sweepActive = false; // jeder manuelle Befehl bricht eine laufende Rampe ab

  if (cmd == "0" || cmd == "stop") {
    setFrequency(0);
  } else if (cmd == "status") {
    printStatus();
  } else if (cmd == "sweep") {
    sweepActive = true;
    sweepStartMs = millis();
    lastSweepPrintMs = 0;
    Serial.println("[SIM] Sweep 0 -> 100 km/h ueber 20s gestartet");
  } else if (cmd.startsWith("f")) {
    setFrequency(cmd.substring(1).toDouble());
  } else if (cmd.startsWith("v")) {
    setFrequency(hzFromKmh(cmd.substring(1).toDouble()));
  } else {
    Serial.println("[SIM] Unbekannter Befehl. f<Hz> / v<km/h> / stop / sweep / status");
  }
}

void handleSerial() {
  static String buf;
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      buf.trim();
      if (buf.length() > 0) processCommand(buf);
      buf = "";
    } else {
      buf += c;
    }
  }
}

void updateSweep() {
  if (!sweepActive) return;
  unsigned long elapsed = millis() - sweepStartMs;
  if (elapsed >= SWEEP_DURATION_MS) {
    sweepActive = false;
    setFrequency(hzFromKmh(SWEEP_MAX_KMH));
    Serial.println("[SIM] Sweep beendet");
    return;
  }
  double kmh = SWEEP_MAX_KMH * (double)elapsed / (double)SWEEP_DURATION_MS;
  targetHz = hzFromKmh(kmh);
  halfPeriodUs = targetHz > 0 ? (unsigned long)(500000.0 / targetHz) : 0;
  if (millis() - lastSweepPrintMs > 1000) {
    printStatus();
    lastSweepPrintMs = millis();
  }
}

void updateOutput() {
  if (halfPeriodUs == 0) return; // 0 Hz: Ausgang bleibt LOW
  unsigned long now = micros();
  if (now - lastToggleUs >= halfPeriodUs) {
    outputState = !outputState;
    digitalWrite(PIN_OUT, outputState ? HIGH : LOW);
    lastToggleUs = now;
  }
}

void setup() {
  pinMode(PIN_OUT, OUTPUT);
  digitalWrite(PIN_OUT, LOW); // sicherer Startzustand: kein Signal
  Serial.begin(115200);
  delay(200);
  Serial.println();
  Serial.println("=== VDO-Tempomat Reed-Simulator ===");
  Serial.println("Befehle: f<Hz>  v<km/h>  stop  sweep  status");
  printStatus();
}

void loop() {
  handleSerial();
  updateSweep();
  updateOutput();
}
