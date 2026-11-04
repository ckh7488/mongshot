#include <Arduino.h>
void last();
// REVIEW CANDIDATE, NOT DEPLOYED TO HARDWARE.
// Existing puzzle pins and output actions are preserved. D11/D13/D7 drive
// 74HC595 status LEDs; A3 is a 2-second manual-next button.
// D11/A3 must first be disconnected from the removed Gun/Hint circuits.
// MP3 legacy two-argument API still requires the original installed library.
#include <SoftwareSerial.h>
#include <MP3Player_KT403A.h>

SoftwareSerial mp3(2, 3);
const uint8_t kLedData = 11, kLedClock = 13, kLedLatch = 7;
const uint8_t kManualButton = A3;
const uint8_t kFrame = 8, kLight = A0, kKey = A1, kRfid = A5, kBook = 6;
const uint8_t kMold = 12, kSlide = 10, kBookOut = 9, kWindow = A4;
const uint8_t kDir1 = 4, kDir2 = 5, kEnable = A2;
const unsigned long kSampleMs = 10, kButtonDebounceMs = 30, kHoldMs = 2000;
const uint8_t kStableSamples = 5;

// Keep diagnostic symbols readable by the simulator; pass = current puzzle.
int pass = 0;
int count = 0;
int phase = 1;
int manualCount = 0;
unsigned long phaseAt = 0, lastSampleMs = 0;
uint8_t stableCount = 0, lightLowCount = 0, lightHighCount = 0;
bool lightState = false;
bool buttonRaw = HIGH, buttonStable = HIGH, buttonFired = false;
unsigned long buttonChangedAt = 0, buttonPressedAt = 0;
uint8_t previousLedMask = 255;

// phase: 0 active; 1/2 boot; 3 slide 20s; 4 slide 10ms;
// 5 window 1s; 6/7 final 100+100ms; 8 final 10s; 9 complete.
void beginPhase(int value, unsigned long now) { phase = value; phaseAt = now; }

void setStage(int value) {
  pass = value;
  stableCount = 0;
  lightLowCount = lightHighCount = 0;
  lightState = false;
}

void updateLeds(unsigned long now) {
  uint8_t mask = uint8_t(1u << pass);
  if (phase != 0 && phase != 9 && ((now / 500) & 1u)) mask = 0;
  if (mask == previousLedMask) return;
  digitalWrite(kLedLatch, LOW);
  shiftOut(kLedData, kLedClock, MSBFIRST, mask);
  digitalWrite(kLedLatch, HIGH);
  previousLedMask = mask;
}

bool manualEvent(unsigned long now) {
  const bool raw = digitalRead(kManualButton);
  if (raw != buttonRaw) { buttonRaw = raw; buttonChangedAt = now; }
  if (raw != buttonStable && now - buttonChangedAt >= kButtonDebounceMs) {
    buttonStable = raw;
    if (raw == LOW) { buttonPressedAt = now; buttonFired = false; }
    else buttonFired = false;
  }
  if (buttonStable == LOW && !buttonFired && now - buttonPressedAt >= kHoldMs) {
    buttonFired = true;
    return true;
  }
  return false;
}

bool stableInput(bool active) {
  if (!active) { stableCount = 0; return false; }
  if (stableCount < kStableSamples) ++stableCount;
  return stableCount >= kStableSamples;
}

void completeCurrent(bool manual, unsigned long now) {
  if (phase != 0 || pass >= 5) return;
  if (manual) ++manualCount;
  Serial.print(manual ? F("MANUAL stage ") : F("AUTO stage "));
  Serial.println(pass);
  switch (pass) {
    case 0:
      digitalWrite(kMold, HIGH);
      PlayNext();
      setStage(1);
      break;
    case 1:
      PlayNext();
      beginPhase(3, now);  // Preserve the original 20-second audio wait.
      break;
    case 2:
      digitalWrite(kDir1, HIGH);
      digitalWrite(kDir2, LOW);
      analogWrite(kEnable, 255);
      setStage(3);
      break;
    case 3:
      digitalWrite(kWindow, HIGH);
      setStage(4);
      beginPhase(5, now);
      break;
    case 4:
      setStage(5);
      beginPhase(6, now);
      break;
  }
}

void servicePhase(unsigned long now) {
  const unsigned long elapsed = now - phaseAt;
  switch (phase) {
    case 1:
      if (elapsed >= 500) {
        mp3.begin(9600);
        Serial.begin(9600);
        beginPhase(2, now);
      }
      break;
    case 2:
      if (elapsed >= 500) {
        SelectPlayerDevice(0x02);
        SetVolume(0x19);
        SpecifyMusicPlay(0, 1);
        Serial.println(F("Start / front panel"));
        beginPhase(0, now);
      }
      break;
    case 3:
      if (elapsed >= 20000) {
        digitalWrite(kSlide, HIGH);
        beginPhase(4, now);
      }
      break;
    case 4:
      if (elapsed >= 10) { PlayNext(); setStage(2); beginPhase(0, now); }
      break;
    case 5:
      if (elapsed >= 1000) beginPhase(0, now);
      break;
    case 6:
      if (elapsed >= 100) { PlayNext(); beginPhase(7, now); }
      break;
    case 7:
      if (elapsed >= 100) { digitalWrite(kBookOut, HIGH); beginPhase(8, now); }
      break;
    case 8:
      if (elapsed >= 10000) { beginPhase(9, now); Serial.println(F("Complete")); }
      break;
  }
}

void setup() {
  pinMode(kLedData, OUTPUT); pinMode(kLedClock, OUTPUT); pinMode(kLedLatch, OUTPUT);
  digitalWrite(kLedLatch, LOW); shiftOut(kLedData, kLedClock, MSBFIRST, 0); digitalWrite(kLedLatch, HIGH);
  pinMode(kManualButton, INPUT_PULLUP);
  pinMode(kFrame, INPUT_PULLUP); pinMode(kBook, INPUT_PULLUP);
  pinMode(kMold, OUTPUT); pinMode(kSlide, OUTPUT); pinMode(kBookOut, OUTPUT); pinMode(kWindow, OUTPUT);
  digitalWrite(kMold, LOW); digitalWrite(kSlide, LOW); digitalWrite(kBookOut, LOW); digitalWrite(kWindow, LOW);
  pinMode(kDir1, OUTPUT); pinMode(kDir2, OUTPUT); pinMode(kEnable, OUTPUT);
  // Preserve original motor startup; verify the actual mechanism before use.
  digitalWrite(kDir1, LOW); digitalWrite(kDir2, HIGH); analogWrite(kEnable, 255);
  phaseAt = millis();
}

void loop() {
  const unsigned long now = millis();
  const bool forced = manualEvent(now);
  servicePhase(now);
  updateLeds(now);
  if (phase != 0) {
    // A hold during a programmed wait is consumed, never queued into a later stage.
    if (forced && phase != 1 && phase != 2) Serial.println(F("MANUAL ignored: timed wait / complete"));
    return;
  }
  if (forced) { completeCurrent(true, now); return; }
  if (now - lastSampleMs < kSampleMs) return;
  lastSampleMs = now;
  bool complete = false;
  switch (pass) {
    case 0: complete = stableInput(digitalRead(kFrame) == LOW); break;
    case 1: {
      const bool low = analogRead(kLight) < 500;
      if (low) { if (lightLowCount < kStableSamples) ++lightLowCount; lightHighCount = 0; }
      else { if (lightHighCount < kStableSamples) ++lightHighCount; lightLowCount = 0; }
      if (!lightState && lightLowCount >= kStableSamples) { lightState = true; ++count; }
      else if (lightState && lightHighCount >= kStableSamples) lightState = false;
      complete = count >= 3;
      break;
    }
    case 2: complete = stableInput(analogRead(kKey) < 100); break;
    case 3: complete = stableInput(analogRead(kRfid) < 400); break;
    case 4: complete = stableInput(digitalRead(kBook) == LOW); break;
  }
  if (complete) completeCurrent(false, now);
}
