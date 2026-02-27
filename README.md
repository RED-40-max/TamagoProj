# TamagoProj
ANNNEEEE
A Raspberry Pi Pico Tamagotchi-style project with an SH1107 OLED display.
Includes:
- MicroPython demo + display driver
- Arduino/C++ experiments (`.ino`, `.cpp`)
- 3D-printable case parts (`.stl`)


## Demo simulation
    OG: https://wokwi.com/projects/362799539846585345

Modified To SH1107: https://wokwi.com/projects/457135064713530369

## Repo Structure

```txt
.
├── 3DPrint(took)/ --> sourced from [Picotamachibi]
│   ├── Bottom.stl
│   └── Top.stl
├── InC/
│   ├── pico_oled_hello.ino
│   ├── tamo.cpp --> Anne's OG code
│   └── tamo3.cpp
├── MicroPy/
│   ├── demo.py --> spinning cubes
│   ├── main.py --> tamo.ccp translate to python
│   └── SH1107.py --> MicroPy OLED driver for I2C from [SH1107]
└── README.md

```

## Sources

[Picotamachibi](https://github.com/kevinmcaleer/picotamachibi): https://github.com/kevinmcaleer/picotamachibi

[SH1107](https://github.com/peter-l5/SH1107): https://github.com/peter-l5/SH1107
