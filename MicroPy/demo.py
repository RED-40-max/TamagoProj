# RP2040 Pico + SH1107 128x128 OLED (I2C) rotating wireframe cubes


# OG: https://wokwi.com/projects/362799539846585345
#Modified To SH1107: https://wokwi.com/projects/457135064713530369


import math
import utime
from machine import I2C, Pin
from SH1107 import SH1107_I2C  # <-- correct

W = 128
H = 128

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400_000)
utime.sleep_ms(50)

OLED_ADDR = 0x3C
oled = SH1107_I2C(W, H, i2c, address=OLED_ADDR, rotate=90)
oled.sleep(False)


class Cube:
    def __init__(self, size, center):
        self.size = size
        self.center = center  # <-- use the passed center

        self.base = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
        self.edges = [
            (0, 1), (1, 3), (3, 2), (2, 0),
            (4, 5), (5, 7), (7, 6), (6, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

        self.ax = 0.0
        self.ay = 0.0
        self.az = 0.0

    def step_rot(self, dax, day, daz):
        self.ax += dax
        self.ay += day
        self.az += daz

    def rotated(self):
        ax, ay, az = self.ax, self.ay, self.az
        sinx, cosx = math.sin(ax), math.cos(ax)
        siny, cosy = math.sin(ay), math.cos(ay)
        sinz, cosz = math.sin(az), math.cos(az)

        out = []
        for x, y, z in self.base:
            # Z
            x, y = (x * cosz - y * sinz), (y * cosz + x * sinz)
            # X
            y, z = (y * cosx - z * sinx), (z * cosx + y * sinx)
            # Y
            x, z = (x * cosy + z * siny), (z * cosy - x * siny)
            out.append((x, y, z))

        return out  # <-- correct: AFTER the loop

    def draw(self, oled, dist=6.0):
        cx, cy = self.center
        pts = []

        for x, y, z in self.rotated():
            # push cube forward + clip near plane to avoid projection blow-ups
            z += 4.0
            if z < -5.0:
                z = -5.0

            denom = dist + z
            if denom < 0.5:
                denom = 0.5

            px = x * dist / denom
            py = y * dist / denom

            sx = int(px * self.size + cx)
            sy = int(py * self.size + cy)
            pts.append((sx, sy))

        for a, b in self.edges:
            x1, y1 = pts[a]
            x2, y2 = pts[b]
            oled.line(x1, y1, x2, y2, 1)


# center down a bit because of 2 lines of text
center = (W // 2 - 25, H // 2 + 10)

cubes = [
    Cube(40, center),
    Cube(25, center),
    Cube(12, center),
]

while True:
    oled.fill(0)
    oled.text("SH1107 demo", 0, 0, 1)
    oled.text("addr 0x3c", 0, 10, 1)

    cubes[0].step_rot(0.03, 0.06, 0.09)
    cubes[1].step_rot(0.09, 0.03, 0.06)
    cubes[2].step_rot(0.06, 0.09, 0.03)

    for c in cubes:
        c.draw(oled, dist=6.0)

    oled.show()
    utime.sleep_ms(20)