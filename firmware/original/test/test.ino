#include <SoftwareSerial.h>
#include <MP3Player_KT403A.h>

SoftwareSerial mp3(2, 3);

const uint8_t kStableReadCount = 5;
const uint8_t kSampleIntervalMs = 2;
const unsigned long kMonitorIntervalMs = 1000;

int dPass = 0;
int count = 0;

// outputs
const uint8_t outWindowPin = 18;
const uint8_t outHintPin = 17;

const uint8_t outLinearDir1Pin = 4;
const uint8_t outLinearDir2Pin = 5;
const uint8_t outLinearSpeedPin = 16;

const uint8_t outEmMoldPin = 12;
const uint8_t outEmBookPin = 9;
const uint8_t outEmSlidePin = 10;
const uint8_t outEmGunPin = 11;

// inputs
const uint8_t inFrameMagPullupPin = 8;
const uint8_t inLightSensorPin = A0;
const uint8_t inKeySensorPin = A1;
const uint8_t inRfidSensorPin = A5;
const uint8_t inIrSensorPullupPin = 6;

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
StableTrigger irTrigger = {0, false};

uint8_t lightLowCount = 0;
uint8_t lightHighCount = 0;
unsigned long lastSampleMs = 0;
unsigned long lastMonitorMs = 0;
uint8_t evFrameMag = 0;
uint8_t evLight = 0;
uint8_t evKey = 0;
uint8_t evRfid = 0;
uint8_t evIr = 0;

bool shouldSampleNow() {
  unsigned long now = millis();
  if (now - lastSampleMs < kSampleIntervalMs) {
    return false;
  }
  lastSampleMs = now;
  return true;
}

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

void applyOutputsForPass(int p) {
  if (p >= 1) {
    digitalWrite(outEmMoldPin, HIGH);
  }
  if (p >= 2) {
    digitalWrite(outEmSlidePin, HIGH);
  }
  if (p >= 3) {
    digitalWrite(outLinearDir1Pin, HIGH);
    digitalWrite(outLinearDir2Pin, LOW);
    analogWrite(outLinearSpeedPin, 255);
  }
  if (p >= 4) {
    digitalWrite(outWindowPin, HIGH);
  }
  if (p >= 5) {
    digitalWrite(outEmBookPin, HIGH);
  }
}

void clearEventFlags() {
  evFrameMag = 0;
  evLight = 0;
  evKey = 0;
  evRfid = 0;
  evIr = 0;
}

void printSensorSnapshot(bool resetEventFlags) {
  int frameMag = digitalRead(inFrameMagPullupPin);
  int ir = digitalRead(inIrSensorPullupPin);
  int light = analogRead(inLightSensorPin);
  int key = analogRead(inKeySensorPin);
  int rfid = analogRead(inRfidSensorPin);

  Serial.println("----- SNAPSHOT -----");
  Serial.print("pass=");
  Serial.print(pass);
  Serial.print(" count=");
  Serial.print(count);
  Serial.print(" lightState=");
  Serial.println(lightState ? 1 : 0);

  Serial.println("Sensor      | Trig | Raw");
  Serial.print("frame(D8)   |  ");
  Serial.print(evFrameMag);
  Serial.print("   | ");
  Serial.println(frameMag);

  Serial.print("light(A0)   |  ");
  Serial.print(evLight);
  Serial.print("   | ");
  Serial.println(light);

  Serial.print("key(A1)     |  ");
  Serial.print(evKey);
  Serial.print("   | ");
  Serial.println(key);

  Serial.print("rfid(A5)    |  ");
  Serial.print(evRfid);
  Serial.print("   | ");
  Serial.println(rfid);

  Serial.print("ir(D6)      |  ");
  Serial.print(evIr);
  Serial.print("   | ");
  Serial.println(ir);
  Serial.println("--------------------");

  if (resetEventFlags) {
    clearEventFlags();
  }
}

void monitorSensorsEverySecond() {
  unsigned long now = millis();
  if (now - lastMonitorMs >= kMonitorIntervalMs) {
    lastMonitorMs = now;
    printSensorSnapshot(true);
  }
}

void advancePassManual() {
  if (pass >= 5) {
    Serial.println("[CMD] already at max pass(5)");
    return;
  }
  pass++;
  applyOutputsForPass(pass);
  Serial.print("[CMD] manual pass -> ");
  Serial.println(pass);
}

void handleSerialCommand() {
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == 'n' || c == 'N') {
      advancePassManual();
    } else if (c == 's' || c == 'S') {
      printSensorSnapshot(false);
    }
  }
}

void setup() {
  pinMode(inFrameMagPullupPin, INPUT_PULLUP);
  pinMode(inIrSensorPullupPin, INPUT_PULLUP);

  pinMode(outEmSlidePin, OUTPUT);
  pinMode(outEmMoldPin, OUTPUT);
  pinMode(outEmBookPin, OUTPUT);
  pinMode(outEmGunPin, OUTPUT);

  digitalWrite(outEmSlidePin, LOW);
  digitalWrite(outEmMoldPin, LOW);
  digitalWrite(outEmBookPin, LOW);
  digitalWrite(outEmGunPin, LOW);

  pinMode(outLinearDir1Pin, OUTPUT);
  pinMode(outLinearDir2Pin, OUTPUT);
  pinMode(outLinearSpeedPin, OUTPUT);

  digitalWrite(outLinearDir1Pin, LOW);
  digitalWrite(outLinearDir2Pin, HIGH);
  analogWrite(outLinearSpeedPin, 255);

  pinMode(outWindowPin, OUTPUT);
  pinMode(outHintPin, OUTPUT);

  digitalWrite(outWindowPin, LOW);
  digitalWrite(outHintPin, HIGH);

  delay(500);

  mp3.begin(9600);
  Serial.begin(9600);

  delay(500);

  SelectPlayerDevice(0x02);
  SetVolume(0x19);
  SpecifyMusicPlay(0, 1);

  Serial.println("Start(TEST)");
  Serial.println("cmd: n=next pass, s=print sensor now");
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

  delay(1000);

  digitalWrite(outEmSlidePin, HIGH);
  delay(10);
  PlayNext();
}

void last() {
  pass = 5;
  delay(100);

  PlayNext();
  delay(100);

  digitalWrite(outEmBookPin, HIGH);
  delay(1000);
}

void loop() {
  handleSerialCommand();
  monitorSensorsEverySecond();

  bool sampleNow = shouldSampleNow();

  switch (pass) {
    case 0:
      if (sampleNow && updateStableTrigger(frameMagTrigger, digitalRead(inFrameMagPullupPin) == LOW)) {
        evFrameMag = 1;
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
          evLight = 1;
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
        evKey = 1;
        pass = 3;
        digitalWrite(outLinearDir1Pin, HIGH);
        digitalWrite(outLinearDir2Pin, LOW);
        analogWrite(outLinearSpeedPin, 255);
      }
      break;

    case 3:
      if (sampleNow && updateStableTrigger(rfidTrigger, analogRead(inRfidSensorPin) < 400)) {
        evRfid = 1;
        pass = 4;
        digitalWrite(outWindowPin, HIGH);
        delay(1000);
      }
      break;

    case 4:
      if (sampleNow && updateStableTrigger(irTrigger, digitalRead(inIrSensorPullupPin) == LOW)) {
        evIr = 1;
        last();
      }
      break;
  }

  if (dPass != pass) {
    Serial.print("dPass : ");
    Serial.print(dPass);
    Serial.print("->");
    Serial.println(pass);
    dPass = pass;
  }
}
