

import time
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

SCREEN_WIDTH = 128
SCREEN_HIGH = 64

# ---------- 'ENUM' CONSTANTS ----------
MOOD_HAPPY  = "HAPPY"
MOOD_HUNGRY = "HUNGRY"
MOOD_SAD    = "SAD"
MOOD_SICK   = "SICK"

# ---------- DEFAULT PET STATE ----------
pet = {
    "fullness":   50,
    "happiness":  80,
    "energy":     80,
    "mood":       MOOD_HAPPY,
    "lastUpdate": time.ticks_ms()
}

# ---------- CONSTANTS ----------
TICK_INTERVAL = 60000  # 1 min in ms


# ---------- HELPERS ----------
def clamp(value, lo, hi):
    return max(lo, min(hi, value))

# ---------- TIME LOGIC ----------
def handle_time():
    now = time.ticks_ms()
    if time.ticks_diff(now, pet["lastUpdate"]) >= TICK_INTERVAL:
        pet["lastUpdate"] = now
        pet["fullness"]  -= 3
        pet["happiness"] -= 2
        pet["energy"]    -= 1
        clamp_stats()

# ---------- STATE UPDATE ----------
def update_pet():
    if pet["fullness"] < 30:
        pet["mood"] = MOOD_HUNGRY
    elif pet["happiness"] < 30:
        pet["mood"] = MOOD_SAD
    elif pet["energy"] < 20:
        pet["mood"] = MOOD_SICK
    else:
        pet["mood"] = MOOD_HAPPY

# ---------- CLAMP ----------
def clamp_stats():
    pet["fullness"]  = clamp(pet["fullness"],  0, 100)
    pet["happiness"] = clamp(pet["happiness"], 0, 100)
    pet["energy"]    = clamp(pet["energy"],    0, 100)

# ---------- RENDER ----------
_last_print = 0

def render():
    global _last_print
    now = time.ticks_ms()
    if time.ticks_diff(now, _last_print) < 2000:
        return
    _last_print = now

    print("-----")
    print("Fullness: ",  pet["fullness"])
    print("Happiness: ", pet["happiness"])
    print("Energy: ",    pet["energy"])
    print("Mood: ",      pet["mood"])

# ---------- MAIN ----------
print("Tamagotchi started")

while True:
    handle_time()
    update_pet()
    render()