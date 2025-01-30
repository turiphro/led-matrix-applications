# led-matrix-applications
Software to control large low-resolution pixel art displays

This repository is meant to be run on a Linux device (like a Raspberry Pi Zero 2 or a laptop/desktop PC).

The display should be connected to an ESP32 which runs the
[WLED library](https://kno.wled.ge/), connected to the same
internet and with UDP enabled.

    Linux [THIS REPO] --wifi--> ESP32 [WLED] ---> LED matrix
