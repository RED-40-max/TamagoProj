/*
 * Project: Tamagotchi Pico
 * Author: Anne T (modified for Raspberry Pi Pico)
 * Date: 1/20/26
 */

#include <Arduino.h>

// ---------- ENUM ----------
enum Mood {
  MOOD_HAPPY,
  MOOD_HUNGRY,
  MOOD_SAD,
  MOOD_SICK
};

// ---------- STRUCT ----------
struct Pet {
  int fullness;
  int happiness;
  int energy;
  Mood mood;

  unsigned long lastUpdate;
};

Pet pet;

// ---------- CONSTANTS ----------
const unsigned long TICK_INTERVAL = 60000; // 1 min

// ---------- FUNCTION DECLARATIONS ----------
void handleTime();
void updatePet();
void clampStats();
void render();

// ---------- SETUP ----------
void setup() {
  Serial.begin(115200);
  delay(1000);

  pet.fullness = 50;
  pet.happiness = 80;
  pet.energy = 80;
  pet.mood = MOOD_HAPPY;
  pet.lastUpdate = millis();

  Serial.println("Tamagotchi started");
}

// ---------- LOOP ----------
void loop() {
  handleTime();
  updatePet();
  render();
}

// ---------- TIME LOGIC ----------
void handleTime() {
  unsigned long now = millis();

  if (now - pet.lastUpdate >= TICK_INTERVAL) {
    pet.lastUpdate = now;

    pet.fullness -= 3;
    pet.happiness -= 2;
    pet.energy -= 1;

    clampStats();
  }
}

// ---------- STATE UPDATE ----------
void updatePet() {
  if (pet.fullness < 30) {
    pet.mood = MOOD_HUNGRY;
  }
  else if (pet.happiness < 30) {
    pet.mood = MOOD_SAD;
  }
  else if (pet.energy < 20) {
    pet.mood = MOOD_SICK;
  }
  else {
    pet.mood = MOOD_HAPPY;
  }
}

// ---------- CLAMP ----------
void clampStats() {
  pet.fullness = constrain(pet.fullness, 0, 100);
  pet.happiness = constrain(pet.happiness, 0, 100);
  pet.energy = constrain(pet.energy, 0, 100);
}

// ---------- RENDER ----------
void render() {
  static unsigned long lastPrint = 0;

  if (millis() - lastPrint < 2000) return;
  lastPrint = millis();

  Serial.println("-----");
  Serial.print("Fullness: "); Serial.println(pet.fullness);
  Serial.print("Happiness: "); Serial.println(pet.happiness);
  Serial.print("Energy: "); Serial.println(pet.energy);
  Serial.print("Mood: "); Serial.println(pet.mood);
}