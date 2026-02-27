#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

// Common SH1107 sizes:
// 128x64  -> use Adafruit_SH1107(128, 64, &Wire)
// 128x128 -> use Adafruit_SH1107(128, 128, &Wire)

Adafruit_SH1107 display = Adafruit_SH1107(128, 64, &Wire);

void setup() {
  Serial.begin(115200);
  delay(200);

  // If your display is 0x3C (common). If not, try 0x3D.
  if (!display.begin(0x3C, true)) {
    Serial.println("SH1107 init failed. Check wiring / address.");
    while (1) delay(10);
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SH110X_WHITE);
  display.setCursor(0, 0);
  display.println("Hello world!");
  display.println("Pico + SH1107");
  display.display();

  Serial.println("Displayed Hello world");
}

void loop() {
  // nothing
}