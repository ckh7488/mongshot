#include <Arduino.h>
void last();
// **DRAFT / NOT DEPLOYED**: confirm 4CH relay actual wiring and boot safety first.
// Preserves the original MP3 SpecifyMusicPlay(0,1) call pending installed library check.
// 2026-11-03: 2ms->10ms, IR->Book Reed, remove unused D11/D17 symbols.

#include <SoftwareSerial.h>
#include <MP3Player_KT403A.h>

SoftwareSerial mp3(2, 3);

const uint8_t kStableReadCount = 5;
const uint8_t kSampleIntervalMs = 10;  // field request: 10 ms

int dPass = 0;
int count = 0;

// outputs
const uint8_t outWindowPin = 18;

const uint8_t outLinearDir1Pin = 4;
const uint8_t outLinearDir2Pin = 5;
const uint8_t outLinearSpeedPin = 16;

const uint8_t outEmMoldPin = 12;
const uint8_t outEmBookPin = 9;
const uint8_t outEmSlidePin = 10;

// inputs
const uint8_t inFrameMagPullupPin = 8;
const uint8_t inLightSensorPin = A0;
const uint8_t inKeySensorPin = A1;
const uint8_t inRfidSensorPin = A5;
const uint8_t inBookReedPullupPin = 6;

// state
int pass = 0;
bool lightState = false;

struct StableTrigger {
  uint8_t count;
  bool latched;
};

StableTrigger frameMagTrigger = {0, false};
StableTrigger keyTrigger = {0, false};
StableTrigger rfidTrigger = {0, false};
StableTrigger bookReedTrigger = {0, false};

uint8_t lightLowCount = 0;
uint8_t lightHighCount = 0;
unsigned long lastSampleMs = 0;

bool shouldSampleNow() {
  unsigned long now = millis();
  if (now - lastSampleMs < kSampleIntervalMs) {
    return false;
  }
  lastSampleMs = now;
  return true;
}

// Triggers once when active signal is stable for kStableReadCount samples.
bool updateStableTrigger(StableTrigger &trigger, bool active) {
  if (active) {
    if (trigger.count < kStableReadCount) {
      trigger.count++;
    }
    if (trigger.count >= kStableReadCount && !trigger.latched) {
      trigger.latched = true;
      return true;
    }
  } else {
    trigger.count = 0;
    trigger.latched = false;
  }
  return false;
}

void setup() {
  pinMode(inFrameMagPullupPin, INPUT_PULLUP);
  pinMode(inBookReedPullupPin, INPUT_PULLUP);

  pinMode(outEmSlidePin, OUTPUT);
  pinMode(outEmMoldPin, OUTPUT);
  pinMode(outEmBookPin, OUTPUT);

  digitalWrite(outEmSlidePin, LOW);
  digitalWrite(outEmMoldPin, LOW);
  digitalWrite(outEmBookPin, LOW);

  pinMode(outLinearDir1Pin, OUTPUT);
  pinMode(outLinearDir2Pin, OUTPUT);
  pinMode(outLinearSpeedPin, OUTPUT);

  digitalWrite(outLinearDir1Pin, LOW);
  digitalWrite(outLinearDir2Pin, HIGH);
  analogWrite(outLinearSpeedPin, 255);

  pinMode(outWindowPin, OUTPUT);

  digitalWrite(outWindowPin, LOW);

  delay(500);

  mp3.begin(9600);
  Serial.begin(9600);

  delay(500);

  SelectPlayerDevice(0x02);
  SetVolume(0x19);
  SpecifyMusicPlay(0, 1);

  Serial.println("Start");
}

void switching() {
  pass = 1;
  digitalWrite(outEmMoldPin, HIGH);
  Serial.println("Molding Open");
  PlayNext();
}

void lamping() {
  pass = 2;
  PlayNext();
  Serial.println("lamping");

  delay(20000);

  digitalWrite(outEmSlidePin, HIGH);
  delay(10);
  PlayNext();
}

void loop() {
  bool sampleNow = shouldSampleNow();

  switch (pass) {
    case 0:
      if (sampleNow && updateStableTrigger(frameMagTrigger, digitalRead(inFrameMagPullupPin) == LOW)) {
        switching();
      }
      break;

    case 1:
      if (sampleNow) {
        int lightValue = analogRead(inLightSensorPin);

        if (lightValue < 500) {
          if (lightLowCount < kStableReadCount) {
            lightLowCount++;
          }
          lightHighCount = 0;
        } else {
          if (lightHighCount < kStableReadCount) {
            lightHighCount++;
          }
          lightLowCount = 0;
        }

        if (!lightState && lightLowCount >= kStableReadCount) {
          lightState = true;
          count++;
        } else if (lightState && lightHighCount >= kStableReadCount) {
          lightState = false;
        }
      }

      if (count >= 3) {
        lamping();
      }
      break;

    case 2:
      if (sampleNow && updateStableTrigger(keyTrigger, analogRead(inKeySensorPin) < 100)) {
        pass = 3;
        digitalWrite(outLinearDir1Pin, HIGH);
        digitalWrite(outLinearDir2Pin, LOW);
        analogWrite(outLinearSpeedPin, 255);
      }
      break;

    case 3:
      if (sampleNow && updateStableTrigger(rfidTrigger, analogRead(inRfidSensorPin) < 400)) {
        pass = 4;
        digitalWrite(outWindowPin, HIGH);
        delay(1000);
      }
      break;

    case 4:
      if (sampleNow && updateStableTrigger(bookReedTrigger, digitalRead(inBookReedPullupPin) == LOW)) {
        last();
        while (1) {
        }
      }
      break;
  }

  if (dPass != pass) {
    Serial.print("dPass : ");
    Serial.print(dPass);
    Serial.print("->");
    Serial.print(pass);
    dPass = pass;
  }
}

void last() {
  pass = 5;
  delay(100);

  PlayNext();
  delay(100);

  digitalWrite(outEmBookPin, HIGH);
  delay(10000);
}
