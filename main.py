"""
@author : Léo Imbert
@created : 31/07/2025 10:18
@updated : 02/08/2025 12:16

* Sounds :
0. Button click
1. Shoot
2. Explosion
3. Player Hurt
4. Player Death
5. Enemy Attack
6. Bassline 1
7. Melody 1
8. Harmony 1
9. Bassline 2
10. Melody 2
11. Harmony 2
12. Dialog
13. Enemy Hurt

* Channels :
0. Button click / Player Shoot
1. Explosion / Dialog / Enemy Hurt
2. Player Hurt / Player Death
3. Enemy Attack
4. Bassline
5. Melody
6. Harmony
"""

import random
import pyxel
import math
import sys
import os

PALETTE = [0x000000, 0xEEEEEE, 0x202840, 0X273E82, 0x0032C4, 0xA9C1FF, 0xA3A3A3, 0x19959C, 0x70C6A9, 0xE9C35B, 0xD38441, 0xD4186C, 0x7E2072, 0x8B4852, 0xFF9798, 0xEDC7B0]

characters_matrices = {
    " ":[[0,0,0,0]],
    "A":[[0,0,0,0,0,0],[0,0,1,1,0,0],[0,1,1,1,1,0],[1,1,0,0,1,1],[1,1,0,0,1,1],[1,1,1,1,1,1],[1,1,0,0,1,1],[1,1,0,0,1,1]],
    "B":[[0,0,0,0,0,0,0],[1,1,1,1,1,1,0],[0,1,1,0,0,1,1],[0,1,1,0,0,1,1],[0,1,1,1,1,1,0],[0,1,1,0,0,1,1],[0,1,1,0,0,1,1],[1,1,1,1,1,1,0]],
    "C":[[0,0,0,0,0,0,0],[0,0,1,1,1,1,0],[0,1,1,0,0,1,1],[1,1,0,0,0,0,0],[1,1,0,0,0,0,0],[1,1,0,0,0,0,0],[0,1,1,0,0,1,1],[0,0,1,1,1,1,0]],
    "D":[[0,0,0,0,0,0,0],[1,1,1,1,1,0,0],[0,1,1,0,1,1,0],[0,1,1,0,0,1,1],[0,1,1,0,0,1,1],[0,1,1,0,0,1,1],[0,1,1,0,1,1,0],[1,1,1,1,1,0,0]],
    "E":[[0,0,0,0,0,0,0],[1,1,1,1,1,1,1],[0,1,1,0,0,0,1],[0,1,1,0,1,0,0],[0,1,1,1,1,0,0],[0,1,1,0,1,0,0],[0,1,1,0,0,0,1],[1,1,1,1,1,1,1]],
    "F":[[0,0,0,0,0,0,0],[1,1,1,1,1,1,1],[0,1,1,0,0,0,1],[0,1,1,0,1,0,0],[0,1,1,1,1,0,0],[0,1,1,0,1,0,0],[0,1,1,0,0,0,0],[1,1,1,1,0,0,0]],
    "G":[[0,0,0,0,0,0,0],[0,0,1,1,1,1,0],[0,1,1,0,0,1,1],[1,1,0,0,0,0,0],[1,1,0,0,0,0,0],[1,1,0,0,1,1,1],[0,1,1,0,0,1,1],[0,0,1,1,1,1,1]],
    "H":[[0,0,0,0,0,0],[1,1,0,0,1,1],[1,1,0,0,1,1],[1,1,0,0,1,1],[1,1,1,1,1,1],[1,1,0,0,1,1],[1,1,0,0,1,1],[1,1,0,0,1,1]],
    "I":[[0,0,0,0,0,0],[1,1,1,1,1,1],[0,0,1,1,0,0],[0,0,1,1,0,0],[0,0,1,1,0,0],[0,0,1,1,0,0],[0,0,1,1,0,0],[1,1,1,1,1,1]],
    "J":[[0,0,0,0,0,0,0],[0,0,0,1,1,1,1],[0,0,0,0,1,1,0],[0,0,0,0,1,1,0],[0,0,0,0,1,1,0],[1,1,0,0,1,1,0],[1,1,0,0,1,1,0],[0,1,1,1,1,0,0]],
    "K":[[0,0,0,0,0,0,0],[1,1,1,0,0,1,1],[0,1,1,0,0,1,1],[0,1,1,0,1,1,0],[0,1,1,1,1,0,0],[0,1,1,0,1,1,0],[0,1,1,0,0,1,1],[1,1,1,0,0,1,1]],
    "L":[[0,0,0,0,0,0,0],[1,1,1,1,0,0,0],[0,1,1,0,0,0,0],[0,1,1,0,0,0,0],[0,1,1,0,0,0,0],[0,1,1,0,0,0,1],[0,1,1,0,0,1,1],[1,1,1,1,1,1,1]],
    "M":[[0,0,0,0,0,0,0],[1,1,0,0,0,1,1],[1,1,1,0,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,0,1,0,1,1],[1,1,0,0,0,1,1],[1,1,0,0,0,1,1]],
    "N":[[0,0,0,0,0,0,0],[1,1,0,0,0,1,1],[1,1,1,0,0,1,1],[1,1,1,1,0,1,1],[1,1,0,1,1,1,1],[1,1,0,0,1,1,1],[1,1,0,0,0,1,1],[1,1,0,0,0,1,1]],
    "O":[[0,0,0,0,0,0,0],[0,0,1,1,1,0,0],[0,1,1,0,1,1,0],[1,1,0,0,0,1,1],[1,1,0,0,0,1,1],[1,1,0,0,0,1,1],[0,1,1,0,1,1,0],[0,0,1,1,1,0,0]],
    "P":[[0,0,0,0,0,0,0],[1,1,1,1,1,1,0],[0,1,1,0,0,1,1],[0,1,1,0,0,1,1],[0,1,1,1,1,1,0],[0,1,1,0,0,0,0],[0,1,1,0,0,0,0],[1,1,1,1,0,0,0]],
    "Q":[[0,0,0,0,0,0,0],[0,0,1,1,1,0,0],[0,1,1,0,1,1,0],[1,1,0,0,0,1,1],[1,1,0,0,0,1,1],[1,1,0,1,1,0,1],[1,1,0,0,1,1,0],[0,1,1,1,0,1,1]],
    "R":[[0,0,0,0,0,0,0],[1,1,1,1,1,1,0],[0,1,1,0,0,1,1],[0,1,1,0,0,1,1],[0,1,1,1,1,1,0],[0,1,1,0,1,1,0],[0,1,1,0,0,1,1],[1,1,1,0,0,1,1]],
    "S":[[0,0,0,0,0,0],[0,1,1,1,1,0],[1,1,0,0,1,1],[1,1,0,0,0,0],[0,1,1,1,1,0],[0,0,0,0,1,1],[1,1,0,0,1,1],[0,1,1,1,1,0]],
    "T":[[0,0,0,0,0,0],[1,1,1,1,1,1],[1,0,1,1,0,1],[0,0,1,1,0,0],[0,0,1,1,0,0],[0,0,1,1,0,0],[0,0,1,1,0,0],[0,1,1,1,1,0]],
    "U":[[0,0,0,0,0,0],[1,1,0,0,1,1],[1,1,0,0,1,1],[1,1,0,0,1,1],[1,1,0,0,1,1],[1,1,0,0,1,1],[1,1,0,0,1,1],[0,1,1,1,1,0]],
    "V":[[0,0,0,0,0,0],[1,1,0,0,1,1],[1,1,0,0,1,1],[1,1,0,0,1,1],[1,1,0,0,1,1],[1,1,0,0,1,1],[0,1,1,1,1,0],[0,0,1,1,0,0]],
    "W":[[0,0,0,0,0,0,0],[1,1,0,0,0,1,1],[1,1,0,0,0,1,1],[1,1,0,0,0,1,1],[1,1,0,1,0,1,1],[1,1,1,1,1,1,1],[1,1,1,0,1,1,1],[1,1,0,0,0,1,1]],
    "X":[[0,0,0,0,0,0,0],[1,1,0,0,0,1,1],[0,1,1,0,1,1,0],[0,0,1,1,1,0,0],[0,0,1,1,1,0,0],[0,1,1,0,1,1,0],[1,1,0,0,0,1,1],[1,1,0,0,0,1,1]],
    "Y":[[0,0,0,0,0,0],[1,1,0,0,1,1],[1,1,0,0,1,1],[1,1,0,0,1,1],[0,1,1,1,1,0],[0,0,1,1,0,0],[0,0,1,1,0,0],[0,1,1,1,1,0]],
    "Z":[[0,0,0,0,0,0,0],[1,1,1,1,1,1,1],[1,1,0,0,0,1,1],[1,0,0,0,1,1,0],[0,0,0,1,1,0,0],[0,0,1,1,0,0,1],[0,1,1,0,0,1,1],[1,1,1,1,1,1,1]],
    "a":[[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,1,1,1,1,0,0],[0,0,0,0,1,1,0],[0,1,1,1,1,1,0],[1,1,0,0,1,1,0],[0,1,1,1,0,1,1]],
    "b":[[0,0,0,0,0,0,0],[1,1,1,0,0,0,0],[0,1,1,0,0,0,0],[0,1,1,1,1,1,0],[0,1,1,0,0,1,1],[0,1,1,0,0,1,1],[0,1,1,0,0,1,1],[1,1,0,1,1,1,0]],
    "c":[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,1,1,1,1,0],[1,1,0,0,1,1],[1,1,0,0,0,0],[1,1,0,0,1,1],[0,1,1,1,1,0]],
    "d":[[0,0,0,0,0,0,0],[0,0,0,1,1,1,0],[0,0,0,0,1,1,0],[0,1,1,1,1,1,0],[1,1,0,0,1,1,0],[1,1,0,0,1,1,0],[1,1,0,0,1,1,0],[0,1,1,1,0,1,1]],
    "e":[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,1,1,1,1,0],[1,1,0,0,1,1],[1,1,1,1,1,1],[1,1,0,0,0,0],[0,1,1,1,1,0]],
    "f":[[0,0,0,0,0,0],[0,0,1,1,1,0],[0,1,1,0,1,1],[0,1,1,0,0,0],[1,1,1,1,0,0],[0,1,1,0,0,0],[0,1,1,0,0,0],[1,1,1,1,0,0]],
    "g":[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,1,1,1,1,1],[1,1,0,0,1,1],[1,1,0,0,1,1],[0,1,1,1,1,1],[0,0,0,0,1,1],[1,1,1,1,1,0]],
    "h":[[0,0,0,0,0,0,0],[1,1,1,0,0,0,0],[0,1,1,0,0,0,0],[0,1,1,0,1,1,0],[0,1,1,1,0,1,1],[0,1,1,0,0,1,1],[0,1,1,0,0,1,1],[1,1,1,0,0,1,1]],
    "i":[[0,0,0,0],[0,1,1,0],[0,0,0,0],[1,1,1,0],[0,1,1,0],[0,1,1,0],[0,1,1,0],[1,1,1,1]],
    "j":[[0,0,0,0,0,0],[0,0,0,0,1,1],[0,0,0,0,0,0],[0,0,0,1,1,1],[0,0,0,0,1,1],[1,1,0,0,1,1],[1,1,0,0,1,1],[0,1,1,1,1,0]],
    "k":[[0,0,0,0,0,0,0],[1,1,1,0,0,0,0],[0,1,1,0,0,0,0],[0,1,1,0,0,1,1],[0,1,1,0,1,1,0],[0,1,1,1,1,0,0],[0,1,1,0,1,1,0],[1,1,1,0,0,1,1]],
    "l":[[0,0,0,0],[1,1,1,0],[0,1,1,0],[0,1,1,0],[0,1,1,0],[0,1,1,0],[0,1,1,0],[1,1,1,1]],
    "m":[[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,1,1,0,1,1,0],[1,1,1,1,1,1,1],[1,1,0,1,0,1,1],[1,1,0,1,0,1,1],[1,1,0,0,0,1,1]],
    "n":[[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[1,1,0,1,1,1,0],[0,1,1,0,0,1,1],[0,1,1,0,0,1,1],[0,1,1,0,0,1,1],[0,1,1,0,0,1,1]],
    "o":[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,1,1,1,1,0],[1,1,0,0,1,1],[1,1,0,0,1,1],[1,1,0,0,1,1],[0,1,1,1,1,0]],
    "p":[[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[1,1,0,1,1,1,0],[0,1,1,0,0,1,1],[0,1,1,0,0,1,1],[0,1,1,1,1,1,0],[0,1,1,0,0,0,0],[1,1,1,1,0,0,0]],
    "q":[[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,1,1,1,0,1,1],[1,1,0,0,1,1,0],[1,1,0,0,1,1,0],[0,1,1,1,1,1,0],[0,0,0,0,1,1,0],[0,0,0,1,1,1,1]],
    "r":[[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[1,1,0,1,1,1,0],[0,1,1,1,0,1,1],[0,1,1,0,0,0,0],[0,1,1,0,0,0,0],[1,1,1,1,0,0,0]],
    "s":[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,1,1,1,1,0],[1,1,0,0,0,0],[0,1,1,1,1,0],[0,0,0,0,1,1],[1,1,1,1,1,0]],
    "t":[[0,0,0,0,0,0],[0,1,1,0,0,0],[0,1,1,0,0,0],[1,1,1,1,1,0],[0,1,1,0,0,0],[0,1,1,0,0,0],[0,1,1,0,1,1],[0,0,1,1,1,0]],
    "u":[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[1,1,0,0,1,1],[1,1,0,0,1,1],[1,1,0,0,1,1],[1,1,0,0,1,1],[0,1,1,1,1,1]],
    "v":[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[1,1,0,0,1,1],[1,1,0,0,1,1],[1,1,0,0,1,1],[0,1,1,1,1,0],[0,0,1,1,0,0]],
    "w":[[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[1,1,0,0,0,1,1],[1,1,0,1,0,1,1],[1,1,0,1,0,1,1],[1,1,1,1,1,1,1],[0,1,1,0,1,1,0]],
    "x":[[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[1,1,0,0,0,1,1],[0,1,1,0,1,1,0],[0,0,1,1,1,0,0],[0,1,1,0,1,1,0],[1,1,0,0,0,1,1]],
    "y":[[0,0,0,0,0,0],[0,0,0,0,0,0],[1,1,0,0,1,1],[1,1,0,0,1,1],[1,1,0,0,1,1],[0,1,1,1,1,1],[0,0,0,0,1,1],[1,1,1,1,1,0]],
    "z":[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[1,1,1,1,1,1],[1,0,0,1,1,0],[0,0,1,1,0,0],[0,1,1,0,0,1],[1,1,1,1,1,1]],
    "1":[[0,0,0,0,0,0],[0,0,1,1,0,0],[0,1,1,1,0,0],[0,0,1,1,0,0],[0,0,1,1,0,0],[0,0,1,1,0,0],[0,0,1,1,0,0],[1,1,1,1,1,1]],
    "2":[[0,0,0,0,0,0],[0,1,1,1,1,0],[1,1,0,0,1,1],[0,0,0,0,1,1],[0,1,1,1,1,0],[1,1,0,0,0,0],[1,1,0,0,1,1],[1,1,1,1,1,1]],
    "3":[[0,0,0,0,0,0],[0,1,1,1,1,0],[1,1,0,0,1,1],[0,0,0,0,1,1],[0,0,1,1,1,0],[0,0,0,0,1,1],[1,1,0,0,1,1],[0,1,1,1,1,0]],
    "4":[[0,0,0,0,0,0,0],[0,0,0,1,1,1,0],[0,0,1,1,1,1,0],[0,1,1,0,1,1,0],[1,1,0,0,1,1,0],[1,1,1,1,1,1,1],[0,0,0,0,1,1,0],[0,0,0,1,1,1,1]],
    "5":[[0,0,0,0,0,0],[1,1,1,1,1,1],[1,1,0,0,0,1],[1,1,0,0,0,0],[1,1,1,1,1,0],[0,0,0,0,1,1],[1,1,0,0,1,1],[0,1,1,1,1,0]],
    "6":[[0,0,0,0,0,0],[0,1,1,1,1,0],[1,1,0,0,1,1],[1,1,0,0,0,0],[1,1,1,1,1,0],[1,1,0,0,1,1],[1,1,0,0,1,1],[0,1,1,1,1,0]],
    "7":[[0,0,0,0,0,0],[1,1,1,1,1,1],[1,1,0,0,1,1],[0,0,0,0,1,1],[0,0,0,1,1,0],[0,0,1,1,0,0],[0,0,1,1,0,0],[0,0,1,1,0,0]],
    "8":[[0,0,0,0,0,0],[0,1,1,1,1,0],[1,1,0,0,1,1],[1,1,0,0,1,1],[0,1,1,1,1,0],[1,1,0,0,1,1],[1,1,0,0,1,1],[0,1,1,1,1,0]],
    "9":[[0,0,0,0,0,0],[0,1,1,1,1,0],[1,1,0,0,1,1],[1,1,0,0,1,1],[0,1,1,1,1,1],[0,0,0,0,1,1],[1,1,0,0,1,1],[0,1,1,1,1,0]],
    "0":[[0,0,0,0,0,0,0],[0,1,1,1,1,1,0],[1,1,0,0,0,1,1],[1,1,0,0,1,1,1],[1,1,0,1,0,1,1],[1,1,1,0,0,1,1],[1,1,0,0,0,1,1],[0,1,1,1,1,1,0]],
    "?":[[0,0,0,0],[1,1,1,0],[1,0,1,1],[0,0,1,1],[0,1,1,0],[0,0,0,0],[0,1,1,0],[0,1,1,0]],
    ",":[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,1,1,0],[0,1,1,0],[1,1,0,0]],
    ".":[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[1,1,0],[1,1,0]],
    ";":[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0],[0,1,1,0],[0,1,1,0],[1,1,0,0]],
    "/":[[0,0,0,0,0,0],[0,0,0,0,1,1],[0,0,0,0,1,0],[0,0,0,1,1,0],[0,0,1,1,0,0],[0,0,1,0,0,0],[0,1,1,0,0,0],[1,1,0,0,0,0]],
    ":":[[0,0],[0,0],[1,1],[1,1],[0,0],[1,1],[1,1],[0,0]],
    "!":[[0,0],[1,1],[1,1],[1,1],[1,1],[0,0],[1,1],[1,1]],
    "&":[[0,1,1,1,0,0,0],[1,0,0,0,1,0,0],[1,0,0,0,1,0,0],[0,1,1,1,0,0,0],[1,1,0,1,1,0,0],[1,0,0,0,1,0,1],[1,1,0,0,0,1,0],[0,1,1,1,1,0,1]],
    "é":[[0,0,0,1,1,0],[0,1,1,0,0,0],[0,0,0,0,0,0],[0,1,1,1,1,0],[1,1,0,0,1,1],[1,1,1,1,1,1],[1,1,0,0,0,0],[0,1,1,1,1,0]],
    "~":[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,1,1,0,1],[1,0,0,1,0]],
    '"':[[0,0,0,0],[0,1,0,1],[0,1,0,1],[1,0,1,0],[1,0,1,0]],
    "#":[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,1,0,1,0],[1,1,1,1,1],[0,1,0,1,0],[1,1,1,1,1],[0,1,0,1,0]],
    "'":[[0,0,0,0,0],[0,0,1,1,0],[0,0,1,1,0],[0,1,1,0,0],[0,1,1,0,0]],
    "{":[[0,0,0],[0,0,1],[0,1,0],[0,1,0],[1,0,0],[0,1,0],[0,1,0],[0,0,1]],
    "(":[[0,0,0],[0,0,1],[0,1,0],[1,0,0],[1,0,0],[1,0,0],[0,1,0],[0,0,1]],
    "[":[[0,0,0],[1,1,1],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,1]],
    "-":[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[1,1,1,1],[1,1,1,1],[0,0,0,0],[0,0,0,0]],
    "|":[[1],[1],[1],[1],[1],[1],[1],[1]],
    "è":[[0,1,1,0,0,0],[0,0,0,1,1,0],[0,0,0,0,0,0],[0,1,1,1,1,0],[1,1,0,0,1,1],[1,1,1,1,1,1],[1,1,0,0,0,0],[0,1,1,1,1,0]],
    "_":[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[1,1,1,1,1,1]],
    "ç":[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,1,1,1,1,0],[1,1,0,0,1,1],[1,1,0,0,0,0],[1,1,0,0,1,1],[0,1,1,1,1,0],[0,0,0,1,0,0],[0,0,1,0,0,0]],
    "à":[[0,0,1,1,0,0,0],[0,0,0,0,1,1,0],[0,0,0,0,0,0,0],[0,1,1,1,1,0,0],[0,0,0,0,1,1,0],[0,1,1,1,1,1,0],[1,1,0,0,1,1,0],[0,1,1,1,0,1,1]],
    "@":[[0,0,0,0,0,0,0],[0,0,1,1,1,1,0],[0,1,0,0,0,0,1],[1,0,0,1,1,0,1],[1,0,1,0,0,1,1],[1,0,1,0,0,1,1],[1,0,0,1,1,0,0],[0,1,0,0,0,0,1],[0,0,1,1,1,1,0]],
    "°":[[1,1,1],[1,0,1],[1,1,1]],
    ")":[[0,0,0],[1,0,0],[0,1,0],[0,0,1],[0,0,1],[0,0,1],[0,1,0],[1,0,0]],
    "]":[[0,0,0],[1,1,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[1,1,1]],
    "+":[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,1,0,0],[0,0,1,0,0],[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0]],
    "=":[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[1,1,1,1,1,1],[0,0,0,0,0,0],[0,0,0,0,0,0],[1,1,1,1,1,1],[0,0,0,0,0,0]],
    "}":[[0,0,0],[1,0,0],[0,1,0],[0,1,0],[0,0,1],[0,1,0],[0,1,0],[1,0,0]],
    "*":[[0,0,0],[1,0,1],[0,1,0],[1,0,1]],
    "%":[[0,1,0,0,0,0,0],[1,0,1,0,1,1,0],[0,1,0,0,1,0,0],[0,0,0,1,1,0,0],[0,0,1,1,0,0,0],[0,0,1,0,0,1,0],[0,1,1,0,1,0,1],[1,1,0,0,0,1,0]],
    "€":[[0,0,0,0,0,0],[0,0,1,1,1,0],[0,1,0,0,0,1],[0,1,1,1,0,0],[1,0,0,0,0,0],[0,1,1,1,0,0],[0,1,0,0,0,1],[0,0,1,1,1,0]],
    "$":[[0,0,1,0,0],[0,1,1,1,0],[1,0,1,0,1],[1,0,1,0,0],[0,1,1,1,0],[0,0,1,0,1],[1,0,1,0,1],[0,1,1,1,0],[0,0,1,0,0]]
}

keys_to_representation = {
    pyxel.KEY_SPACE: "space",
    pyxel.KEY_A: "a",
    pyxel.KEY_B: "b",
    pyxel.KEY_C: "c",
    pyxel.KEY_D: "d",
    pyxel.KEY_E: "e",
    pyxel.KEY_F: "f",
    pyxel.KEY_G: "g",
    pyxel.KEY_H: "h",
    pyxel.KEY_I: "i",
    pyxel.KEY_J: "j",
    pyxel.KEY_K: "k",
    pyxel.KEY_L: "l",
    pyxel.KEY_M: "m",
    pyxel.KEY_N: "n",
    pyxel.KEY_O: "o",
    pyxel.KEY_P: "p",
    pyxel.KEY_Q: "q",
    pyxel.KEY_R: "r",
    pyxel.KEY_S: "s",
    pyxel.KEY_T: "t",
    pyxel.KEY_U: "u",
    pyxel.KEY_V: "v",
    pyxel.KEY_W: "w",
    pyxel.KEY_X: "x",
    pyxel.KEY_Y: "y",
    pyxel.KEY_Z: "z",
    pyxel.KEY_0: "0",
    pyxel.KEY_1: "1",
    pyxel.KEY_2: "2",
    pyxel.KEY_3: "3",
    pyxel.KEY_4: "4",
    pyxel.KEY_5: "5",
    pyxel.KEY_6: "6",
    pyxel.KEY_7: "7",
    pyxel.KEY_8: "8",
    pyxel.KEY_9: "9",
    pyxel.KEY_MINUS: "-",
    pyxel.KEY_EQUALS: "=",
    pyxel.KEY_LEFTBRACKET: "[",
    pyxel.KEY_RIGHTBRACKET: "]",
    pyxel.KEY_SEMICOLON: ";",
    pyxel.KEY_COMMA: ",",
    pyxel.KEY_PERIOD: ".",
    pyxel.KEY_SLASH: "/",
    pyxel.KEY_BACKSPACE: "backspace",
    pyxel.KEY_TAB: "tab",
    pyxel.KEY_RETURN: "enter",
    pyxel.KEY_SHIFT: "shift",
    pyxel.KEY_LCTRL: "ctrl",
    pyxel.KEY_ALT: "alt",
    pyxel.KEY_ESCAPE: "escape",
    pyxel.KEY_UP: "up",
    pyxel.KEY_DOWN: "down",
    pyxel.KEY_LEFT: "left",
    pyxel.KEY_RIGHT: "right"
}

NORMAL_COLOR_MODE = 0
ROTATING_COLOR_MODE = 1
RANDOM_COLOR_MODE = 2

ANCHOR_TOP_LEFT = 0
ANCHOR_TOP_RIGHT = 1
ANCHOR_BOTTOM_LEFT = 2
ANCHOR_BOTTOM_RIGHT = 3
ANCHOR_LEFT = 4
ANCHOR_RIGHT = 5
ANCHOR_TOP = 6
ANCHOR_BOTTOM = 7
ANCHOR_CENTER = 8

class PyxelManager:

    def __init__(self, width:int, height:int, scenes:list, default_scene_id:int=0, fps:int=60, fullscreen:bool=False, mouse:bool=False, quit_key:int=pyxel.KEY_ESCAPE, camera_x:int=0, camera_y:int=0):
        
        self.__fps = fps
        self.__scenes_dict = {scene.id:scene for scene in scenes}
        self.__current_scene = self.__scenes_dict.get(default_scene_id, 0)
        self.__transition = {}

        self.__cam_x = self.__cam_tx = camera_x
        self.__cam_y = self.__cam_ty = camera_y
        self.__shake_amount = 0
        self.__sub_shake_amount = 0

        pyxel.init(width, height, fps=self.__fps, quit_key=quit_key)
        pyxel.fullscreen(fullscreen)
        pyxel.mouse(mouse)

        if self.__current_scene.pyxres_path:
            pyxel.load(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), self.__current_scene.pyxres_path))
        pyxel.title(self.__current_scene.title)
        pyxel.screen_mode(self.__current_scene.screen_mode)
        pyxel.colors.from_list(self.__current_scene.palette)

    @property
    def camera_x(self)-> int:
        return self.__cam_x
    
    @property
    def camera_y(self)-> int:
        return self.__cam_y

    @property
    def mouse_x(self)-> int:
        return self.__cam_x + pyxel.mouse_x
    
    @property
    def mouse_y(self)-> int:
        return self.__cam_y + pyxel.mouse_y
    
    @property
    def fps(self)-> int:
        return self.__fps
    
    def set_camera(self, new_camera_x:int, new_camera_y:int):
        self.__cam_x = self.__cam_tx = new_camera_x
        self.__cam_y = self.__cam_ty = new_camera_y

    def move_camera(self, new_camera_x:int, new_camera_y:int):
        self.__cam_tx = new_camera_x
        self.__cam_ty = new_camera_y

    def shake_camera(self, amount:int, sub_amount:float):
        self.__shake_amount = amount
        self.__sub_shake_amount = sub_amount

    def change_scene(self, new_scene_id:int, new_camera_x:int=0, new_camera_y:int=0):
        self.set_camera(new_camera_x, new_camera_y)

        if self.__current_scene.on_exit:
            self.__current_scene.on_exit()
        self.__current_scene = self.__scenes_dict.get(new_scene_id, 0)
        if self.__current_scene.on_enter:
            self.__current_scene.on_enter()

        if self.__current_scene.pyxres_path:
            pyxel.load(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), self.__current_scene.pyxres_path))
        pyxel.title(self.__current_scene.title)
        pyxel.screen_mode(self.__current_scene.screen_mode)
        pyxel.colors.from_list(self.__current_scene.palette)

    def change_scene_dither(self, new_scene_id:int, speed:float, transition_color:int, new_camera_x:int=0, new_camera_y:int=0):
        self.__transition = {
            "type":"dither",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "dither":0
        }

    def change_scene_circle(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0):
        self.__transition = {
            "type":"circle",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "radius":0,
            "max_radius":((pyxel.width ** 2 + pyxel.height ** 2) ** 0.5) / 2
        }

    def change_scene_closing_doors(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0):
        self.__transition = {
            "type":"closing_doors",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "w":0,
            "x":self.__cam_x + pyxel.width
        }

    def change_scene_rectangle_right_left(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0):
        self.__transition = {
            "type":"rectangle_right_left",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "x":self.__cam_x + pyxel.width,
            "w":0
        }

    def change_scene_rectangle_left_right(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0):
        self.__transition = {
            "type":"rectangle_left_right",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "x":self.__cam_x,
            "w":0
        }

    def change_scene_outer_circle(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0):
        self.__transition = {
            "type":"outer_circle",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "start_end":int(((pyxel.width ** 2 + pyxel.height ** 2) ** 0.5) / 2) + 1,
            "end":int(((pyxel.width ** 2 + pyxel.height ** 2) ** 0.5) / 2) + 1
        }

    def change_scene_triangle(self, new_scene_id:int, speed:int, transition_color:int, rotation_speed:int, new_camera_x:int=0, new_camera_y:int=0):
        self.__transition = {
            "type":"triangle",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "rotation_speed":rotation_speed,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "size":0,
            "angle":270
        }

    def apply_palette_effect(self, effect_function, **kwargs):
        pyxel.colors.from_list(effect_function(self.__current_scene.palette, kwargs))

    def reset_palette(self):
        pyxel.colors.from_list(self.__current_scene.palette)

    def handle_transitions(self):

        if self.__transition.get("type") == "dither":
            self.__transition["dither"] += self.__transition["speed"] * self.__transition["direction"]

            if self.__transition["dither"] > 1 and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"])
            if self.__transition["dither"] < 0 and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            pyxel.dither(self.__transition["dither"])
            pyxel.rect(self.__cam_x, self.__cam_y, pyxel.width, pyxel.height, self.__transition["transition_color"])
            pyxel.dither(1)

        elif self.__transition.get("type") == "circle":
            self.__transition["radius"] += self.__transition["speed"] * self.__transition["direction"]

            if self.__transition["radius"] > self.__transition["max_radius"] and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"])
            if self.__transition["radius"] < 0 and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            pyxel.circ(self.__cam_x + pyxel.width / 2, self.__cam_y + pyxel.height / 2, self.__transition["radius"], self.__transition["transition_color"])

        elif self.__transition.get("type") == "closing_doors":
            self.__transition["w"] += self.__transition["speed"] * self.__transition["direction"]
            self.__transition["x"] -= self.__transition["speed"] * self.__transition["direction"]

            if self.__transition["w"] > pyxel.width // 2 and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"])
            if self.__transition["w"] < 0 and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            pyxel.rect(self.__cam_x, self.__cam_y, self.__transition["w"], pyxel.height, self.__transition["transition_color"])
            pyxel.rect(self.__transition["x"], self.__cam_y, self.__transition["w"], pyxel.height, self.__transition["transition_color"])

        elif self.__transition.get("type") == "rectangle_right_left":
            self.__transition["w"] += self.__transition["speed"] * self.__transition["direction"]
            if self.__transition["direction"] == 1:
                self.__transition["x"] -= self.__transition["speed"]

            if self.__transition["w"] > pyxel.width and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"])
            if self.__transition["w"] < 0 and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            pyxel.rect(self.__transition["x"], self.__cam_y, self.__transition["w"], pyxel.height, self.__transition["transition_color"])

        elif self.__transition.get("type") == "rectangle_left_right":
            self.__transition["w"] += self.__transition["speed"] * self.__transition["direction"]
            if self.__transition["direction"] == -1:
                self.__transition["x"] += self.__transition["speed"]

            if self.__transition["w"] > pyxel.width and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"])
            if self.__transition["w"] < 0 and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            pyxel.rect(self.__transition["x"], self.__cam_y, self.__transition["w"], pyxel.height, self.__transition["transition_color"])

        elif self.__transition.get("type") == "outer_circle":
            self.__transition["end"] -= self.__transition["speed"] * self.__transition["direction"]

            if self.__transition["end"] < 0 and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"])
            if self.__transition["end"] > self.__transition["start_end"] and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            
            for radius in range(self.__transition["start_end"], self.__transition["end"], -1):
                pyxel.ellib(self.__cam_x + pyxel.width / 2 - radius, self.__cam_y + pyxel.height / 2 - radius, radius * 2, radius * 2, self.__transition["transition_color"])
                pyxel.ellib(self.__cam_x + pyxel.width / 2 - radius + 1, self.__cam_y + pyxel.height / 2 - radius, radius * 2, radius * 2, self.__transition["transition_color"])

        elif self.__transition.get("type") == "triangle":
            self.__transition["size"] += self.__transition["speed"] * self.__transition["direction"]
            self.__transition["angle"] += self.__transition["rotation_speed"] * self.__transition["direction"]

            if self.__transition["size"] / 2.5 > max(pyxel.width, pyxel.height) and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"])
            if self.__transition["size"] < 0 and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            d = math.sqrt(3) / 3 * self.__transition["size"]
            x1, y1 = self.__cam_x + pyxel.width / 2 + d * math.cos(math.radians(0 + self.__transition["angle"])), self.__cam_y + pyxel.height / 2 + d * math.sin(math.radians(0 + self.__transition["angle"]))
            x2, y2 = self.__cam_x + pyxel.width / 2 + d * math.cos(math.radians(120 + self.__transition["angle"])), self.__cam_y + pyxel.height / 2 + d * math.sin(math.radians(120 + self.__transition["angle"]))
            x3, y3 = self.__cam_x + pyxel.width / 2 + d * math.cos(math.radians(240 + self.__transition["angle"])), self.__cam_y + pyxel.height / 2 + d * math.sin(math.radians(240 + self.__transition["angle"]))
            pyxel.tri(x1, y1, x2, y2, x3, y3, self.__transition["transition_color"])

    def update(self):
        self.__cam_x += (self.__cam_tx - self.__cam_x) * 0.1
        self.__cam_y += (self.__cam_ty - self.__cam_y) * 0.1

        if self.__shake_amount > 0:
            amount = int(self.__shake_amount)
            pyxel.camera(self.__cam_x + random.randint(-amount, amount), self.__cam_y + random.randint(-amount, amount))
            self.__shake_amount -= self.__sub_shake_amount
        else:
            pyxel.camera(self.__cam_x, self.__cam_y)

        if not self.__transition.get("type"):
            self.__current_scene.update()

    def draw(self):
        self.__current_scene.draw()
        if self.__transition:
            self.handle_transitions()

    def run(self):
        pyxel.run(self.update, self.draw)

class Scene:

    def __init__(self, id:int, title:str, update, draw, pyxres_path:str=None, palette:list=PALETTE, screen_mode:int=0, on_exit=None, on_enter=None):
        self.id = id
        self.title = title
        self.update = update
        self.draw = draw
        self.pyxres_path = pyxres_path
        self.palette = palette
        self.screen_mode = screen_mode
        self.on_exit = on_exit
        self.on_enter = on_enter

class Sprite:

    def __init__(self, img:int, u:int, v:int, w:int, h:int, colkey:int=None):
        self.img = img
        self.u, self.v = u, v
        self.w, self.h = w, h
        self.colkey = 0 if colkey == 0 else colkey
        self.flip_horizontal = False
        self.flip_vertical = False

class Animation:

    def __init__(self, sprite:Sprite, total_frames:int=1, frame_duration:int=20, loop:bool=True):
        self.sprite = sprite
        self.__total_frames = total_frames
        self.frame_duration = frame_duration
        self.__loop = loop
        self.__start_frame = pyxel.frame_count
        self.current_frame = 0
        self.__is_finished = False

    def is_finished(self)-> bool:
        return self.__is_finished and not self.__loop
    
    def is_looped(self)-> bool:
        return self.__loop
    
    def reset(self):
        self.__start_frame = pyxel.frame_count
        self.current_frame = 0
        self.__is_finished = False

    def update(self):
        if self.is_finished():
            return
        
        if pyxel.frame_count - self.__start_frame >= self.frame_duration:
            self.__start_frame = pyxel.frame_count
            self.current_frame += 1
            if self.current_frame >= self.__total_frames:
                if self.__loop:
                    self.current_frame = 0
                else:
                    self.__is_finished = True
                    self.current_frame = self.__total_frames - 1

    def draw(self, x:int, y:int):
        w = -self.sprite.w if self.sprite.flip_horizontal else self.sprite.w
        h = -self.sprite.h if self.sprite.flip_vertical else self.sprite.h
        pyxel.blt(x, y, self.sprite.img, self.sprite.u + self.current_frame * abs(self.sprite.w), self.sprite.v, w, h, self.sprite.colkey)

class Text:

    def __init__(self, text:str, x:int, y:int, text_colors:list|int, font_size:int=0, anchor:int=ANCHOR_TOP_LEFT, color_mode:int=NORMAL_COLOR_MODE, color_speed:int|float=5, relative:bool=False, wavy:bool=False, wave_speed:int|float=10, wave_height:int=3, shadow:bool=False, shadow_color:int=0, shadow_offset:int=1, glitch_intensity:int=0, underline:bool=False, underline_color:int=0, blinking:bool=False, blinking_frames:int=30)-> None:
        self.text = text
        self.x = x
        self.y = y
        self.__font_size = font_size
        self.__text_width, self.__text_height = text_size(text, font_size)
        self.__anchor = anchor
        self.__relative = relative
        self.__wavy = wavy
        self.__wave_speed = wave_speed
        self.__wave_height = wave_height
        self.__shadow = shadow
        self.__shadow_color = shadow_color
        self.__shadow_x = self.x + shadow_offset
        self.__shadow_y = self.y + shadow_offset
        self.__shadow_offset = shadow_offset
        self.__glitch_intensity = glitch_intensity
        self.__underline = underline
        self.__underline_color = underline_color
        self.__blinking = blinking
        self.__blinking_frames = blinking_frames

        self.__text_colors = [text_colors] if isinstance(text_colors, int) else text_colors
        self.__original_text_colors = [x for x in self.__text_colors]
        self.__color_mode = color_mode
        self.__color_speed = color_speed
        self.__last_change_color_time = pyxel.frame_count

        if "\n" not in self.text:
            if anchor in [ANCHOR_TOP_RIGHT, ANCHOR_BOTTOM_RIGHT, ANCHOR_RIGHT]:
                self.x -= self.__text_width
            if anchor in [ANCHOR_BOTTOM_LEFT, ANCHOR_BOTTOM_RIGHT, ANCHOR_BOTTOM]:
                self.y -= self.__text_height
            if anchor in [ANCHOR_TOP, ANCHOR_BOTTOM, ANCHOR_CENTER]:
                self.x -= self.__text_width // 2
            if anchor in [ANCHOR_LEFT, ANCHOR_RIGHT, ANCHOR_CENTER]:
                self.y -= self.__text_height // 2

    def __draw_line(self, text:str, y:int, camera_x:int=0, camera_y:int=0)-> None:
        x = self.x
        text_width, text_height = text_size(text, self.__font_size)

        if self.__shadow:
            Text(text, x + self.__shadow_offset, y + self.__shadow_offset, self.__shadow_color, self.__font_size, self.__anchor, relative=self.__relative, underline=self.__underline, underline_color=self.__shadow_color, wavy=self.__wavy, wave_height=self.__wave_height, wave_speed=self.__wave_speed).draw(camera_x, camera_y)

        if self.__anchor in [ANCHOR_TOP_RIGHT, ANCHOR_BOTTOM_RIGHT, ANCHOR_RIGHT]:
            x -= text_width
        if self.__anchor in [ANCHOR_BOTTOM_LEFT, ANCHOR_BOTTOM_RIGHT, ANCHOR_BOTTOM]:
            y -= self.__text_height
        if self.__anchor in [ANCHOR_TOP, ANCHOR_BOTTOM, ANCHOR_CENTER]:
            x -= text_width // 2
        if self.__anchor in [ANCHOR_LEFT, ANCHOR_RIGHT, ANCHOR_CENTER]:
            y -= self.__text_height // 2

        if self.__relative:
            x += camera_x
            y += camera_y

        char_x = x

        if self.__font_size > 0:
            for char_index, char in enumerate(text):
                char_y = y + math.cos(pyxel.frame_count / self.__wave_speed + char_index * 0.3) * self.__wave_height if self.__wavy else y

                if char in characters_matrices:
                    char_matrix = characters_matrices[char]
                    char_width = len(char_matrix[0]) * self.__font_size

                    x += random.uniform(-self.__glitch_intensity, self.__glitch_intensity)
                    char_y += random.uniform(-self.__glitch_intensity, self.__glitch_intensity)
                    
                    for row_index, row in enumerate(char_matrix):
                        for col_index, pixel in enumerate(row):
                            if pixel:
                                pyxel.rect(x + col_index * self.__font_size, char_y + row_index * self.__font_size + (1 * self.__font_size if char in "gjpqy" else 0), self.__font_size, self.__font_size, self.__text_colors[char_index % len(self.__text_colors)])
                    
                    x += char_width + self.__font_size

            if self.__underline:
                pyxel.rect(char_x, y + text_height - self.__font_size, text_width, self.__font_size, self.__underline_color)
        else:
            for char_index, char in enumerate(text):
                char_y = y + math.cos(pyxel.frame_count / self.__wave_speed + char_index * 0.3) * self.__wave_height if self.__wavy else y
                x += random.uniform(-self.__glitch_intensity, self.__glitch_intensity)
                char_y += random.uniform(-self.__glitch_intensity, self.__glitch_intensity)
                pyxel.text(x, char_y, char, self.__text_colors[char_index % len(self.__text_colors)])
                x += 4

    def update(self)-> None:
        if self.__color_mode and pyxel.frame_count - self.__last_change_color_time >= self.__color_speed:
            if self.__color_mode == ROTATING_COLOR_MODE:
                self.__last_change_color_time = pyxel.frame_count
                self.__text_colors = [self.__text_colors[-1]] + self.__text_colors[:-1]
            elif self.__color_mode == RANDOM_COLOR_MODE:
                self.__last_change_color_time = pyxel.frame_count
                self.__text_colors = [random.choice(self.__original_text_colors) for _ in range(len(self.text))]

    def draw(self, camera_x:int=0, camera_y:int=0)-> None:
        if self.__blinking and pyxel.frame_count % (self.__blinking_frames) >= self.__blinking_frames // 2:
            return

        x = self.x
        y = self.y

        if "\n" in self.text:
            lines = self.text.split("\n")
            for i, line in enumerate(lines):
                if self.__font_size > 0:
                    self.__draw_line(line, y + i * (9 * self.__font_size), camera_x, camera_y)
                else:
                    self.__draw_line(line, y + i * 6, camera_x, camera_y)
            return
        
        if self.__relative:
            x += camera_x
            y += camera_y

        if self.__shadow:
            Text(self.text, self.__shadow_x, self.__shadow_y, self.__shadow_color, self.__font_size, self.__anchor, relative=self.__relative, underline=self.__underline, underline_color=self.__shadow_color, wavy=self.__wavy, wave_height=self.__wave_height, wave_speed=self.__wave_speed).draw(camera_x, camera_y)

        if self.__font_size > 0:
            for char_index, char in enumerate(self.text):
                char_y = y + math.cos(pyxel.frame_count / self.__wave_speed + char_index * 0.3) * self.__wave_height if self.__wavy else y

                if char in characters_matrices:
                    char_matrix = characters_matrices[char]
                    char_width = len(char_matrix[0]) * self.__font_size

                    x += random.uniform(-self.__glitch_intensity, self.__glitch_intensity)
                    char_y += random.uniform(-self.__glitch_intensity, self.__glitch_intensity)
                    
                    for row_index, row in enumerate(char_matrix):
                        for col_index, pixel in enumerate(row):
                            if pixel:
                                pyxel.rect(x + col_index * self.__font_size, char_y + row_index * self.__font_size + (1 * self.__font_size if char in "gjpqy" else 0), self.__font_size, self.__font_size, self.__text_colors[char_index % len(self.__text_colors)])
                    
                    x += char_width + self.__font_size

            if self.__underline:
                pyxel.rect(self.x, y + self.__text_height - self.__font_size, self.__text_width, self.__font_size, self.__underline_color)
        else:
            for char_index, char in enumerate(self.text):
                char_y = y + math.cos(pyxel.frame_count / self.__wave_speed + char_index * 0.3) * self.__wave_height if self.__wavy else y
                x += random.uniform(-self.__glitch_intensity, self.__glitch_intensity)
                char_y += random.uniform(-self.__glitch_intensity, self.__glitch_intensity)
                pyxel.text(x, char_y, char, self.__text_colors[char_index % len(self.__text_colors)])
                x += 4

class Button:

    def __init__(self, text:str, x:int, y:int, background_color:int, text_colors:list|int, hover_background_color:int, hover_text_colors:list|int, font_size:int=1, border:bool=False, border_color:int=0, color_mode:int=NORMAL_COLOR_MODE, color_speed:int=10, relative:bool=True, anchor:int=ANCHOR_TOP_LEFT, command=None):
        self.__x = x
        self.__y = y
        self.__width, self.__height = text_size(text, font_size)
        self.__width += 4 if border else 2
        self.__height += 4 if border else 2
        self.__background_color = background_color
        self.__hover_background_color = hover_background_color
        self.__border = border
        self.__border_color = border_color
        self.__relative = relative
        self.__command = command

        self.__x, self.__y = get_anchored_position(self.__x, self.__y, self.__width, self.__height, anchor)

        self.__text = Text(text, self.__x + 2 if border else self.__x + 1, self.__y + 2 if border else self.__y + 1, text_colors, font_size, color_mode=color_mode, color_speed=color_speed, relative=relative)
        self.__hover_text = Text(text, self.__x + 2 if border else self.__x + 1, self.__y + 2 if border else self.__y + 1, hover_text_colors, font_size, color_mode=color_mode, color_speed=color_speed, relative=relative)

    def is_hovered(self, camera_x:int=0, camera_y:int=0)-> bool:
        if self.__x <= pyxel.mouse_x < self.__x + self.__width and self.__y <= pyxel.mouse_y < self.__y + self.__height and self.__relative:
            return True
        if self.__x <= camera_x + pyxel.mouse_x < self.__x + self.__width and self.__y <= camera_y + pyxel.mouse_y < self.__y + self.__height and not self.__relative:
            return True
        
    def update(self, camera_x:int=0, camera_y:int=0):
        self.__text.update()
        self.__hover_text.update()
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.is_hovered(camera_x, camera_y) and self.__command:
            self.__command()

    def draw(self, camera_x:int=0, camera_y:int=0):
        x = camera_x + self.__x if self.__relative else self.__x
        y = camera_y + self.__y if self.__relative else self.__y
        if self.is_hovered(camera_x, camera_y):
            pyxel.rect(x, y, self.__width, self.__height, self.__hover_background_color)
            self.__hover_text.draw(camera_x, camera_y)
        else:
            pyxel.rect(x, y, self.__width, self.__height, self.__background_color)
            self.__text.draw(camera_x, camera_y)
        if self.__border:
            pyxel.rectb(x, y, self.__width, self.__height, self.__border_color)

class IconButton:

    def __init__(self, x:int, y:int, background_color:int, hover_background_color:int, sprite:Sprite, border:bool=False, border_color:int=0, relative:bool=True, anchor:int=ANCHOR_TOP_LEFT, command=None):
        self.__x = x + 1 if not border else x + 2
        self.__y = y + 1 if not border else y + 2
        self.__width = sprite.w + 2 if not border else sprite.w + 4
        self.__height = sprite.h + 2 if not border else sprite.h + 4
        self.__background_color = background_color
        self.__hover_background_color = hover_background_color
        self.__sprite = sprite
        self.__border = border
        self.__border_color = border_color
        self.__relative = relative
        self.__command = command

        self.__x, self.__y = get_anchored_position(self.__x, self.__y, self.__width, self.__height, anchor)

    def is_hovered(self, camera_x:int=0, camera_y:int=0)-> bool:
        if self.__x - 2 < pyxel.mouse_x < self.__x + self.__sprite.w + 1 and self.__y - 2 < pyxel.mouse_y < self.__y + self.__sprite.h + 1 and self.__relative:
            return True
        elif self.__x - 2 < camera_x + pyxel.mouse_x < self.__x + self.__sprite.w + 1 and self.__y - 2 < camera_y + pyxel.mouse_y < self.__y + self.__sprite.h + 1 and not self.__relative:
            return True
        
    def update(self, camera_x:int=0, camera_y:int=0):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.is_hovered(camera_x, camera_y) and self.__command:
            self.__command()

    def draw(self, camera_x:int=0, camera_y:int=0):
        x = camera_x + self.__x if self.__relative else self.__x
        y = camera_y + self.__y if self.__relative else self.__y

        if self.__border:
            pyxel.rectb(x - 2, y - 2, self.__sprite.w + 4, self.__sprite.h + 4, self.__border_color)
        if self.is_hovered(camera_x, camera_y):
            pyxel.rect(x - 1, y - 1, self.__sprite.w + 2, self.__sprite.h + 2, self.__hover_background_color)
        else:
            pyxel.rect(x - 1, y - 1, self.__sprite.w + 2, self.__sprite.h + 2, self.__background_color)
        pyxel.blt(x, y, self.__sprite.img, self.__sprite.u, self.__sprite.v, self.__sprite.w, self.__sprite.h, self.__sprite.colkey)

class UIBar:

    def __init__(self, x:int, y:int, width:int, height:int, border_color:int, bar_color:int, starting_value:int, max_value:int, relative:bool=True, horizontal:bool=True, regen:bool=False, speed_regen:int=0.5, value_regen:int=1, anchor:int=ANCHOR_TOP_LEFT):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__border_color = border_color
        self.__bar_color = bar_color

        self.current_value = starting_value
        self.__max_value = max_value
        self.__relative = relative
        self.__horizontal = horizontal

        self.__regen = regen
        self.__speed_regen = speed_regen
        self.__regen_timer = 0
        self.__value_regen = value_regen
        self.__bar_width = 0
        self.__bar_height = 0

        self.__x, self.__y = get_anchored_position(self.__x, self.__y, self.__width + 2, self.__height + 2, anchor)

    def update(self):
        self.__regen_timer += 1
        if self.current_value < 0:
            self.current_value = 0
        if self.current_value < self.__max_value and self.__regen and self.__regen_timer >= self.__speed_regen:
            self.__regen_timer = 0
            self.current_value += self.__value_regen
        while self.current_value > self.__max_value:
            self.current_value -= 1
        self.__bar_width = self.__width * self.current_value / self.__max_value
        self.__bar_height = self.__height * self.current_value / self.__max_value

    def draw(self, camera_x:int=0, camera_y:int=0):
        if self.__relative:
            if self.__horizontal:
                pyxel.rect(camera_x + self.__x + 1, camera_y + self.__y + 1, self.__bar_width, self.__height, self.__bar_color)
                pyxel.rectb(camera_x + self.__x, camera_y + self.__y, self.__width + 2, self.__height + 2, self.__border_color)
            else:
                pyxel.rect(camera_x + self.__x + 1, camera_y + self.__y + self.__height - self.__bar_height + 1, self.__width, self.__bar_height, self.__bar_color)
                pyxel.rectb(camera_x + self.__x, camera_y + self.__y, self.__width + 2, self.__height + 2, self.__border_color)
        else:
            if self.__horizontal:
                pyxel.rect(self.__x + 1, self.__y + 1, self.__bar_width, self.__height, self.__bar_color)
                pyxel.rectb(self.__x, self.__y, self.__width + 2, self.__height + 2, self.__border_color)
            else:
                pyxel.rect(self.__x + 1, self.__y + self.__height - self.__bar_height + 1, self.__width, self.__bar_height, self.__bar_color)
                pyxel.rectb(self.__x, self.__y, self.__width + 2, self.__height + 2, self.__border_color)

class Dialog:

    def __init__(self, lines:list, background_color:int, names_colors:list|int, text_colors:list|int, border:bool=False, border_color:int=0, sound:bool=False, channel:int=0, sound_number:int=0):
        self.lines = lines
        self.background_color = background_color
        self.names_colors = names_colors
        self.text_colors = text_colors
        self.border = border
        self.border_color = border_color
        self.sound = sound
        self.channel = channel
        self.sound_number = sound_number

class DialogManager:

    def __init__(self, relative_start_x:int, relative_start_y:int, relative_end_x:int, relative_end_y:int, width:int, height:int, char_speed:int=3, next_key:int=pyxel.KEY_SPACE):
        self.__start_x = relative_start_x
        self.__start_y = relative_start_y
        self.__end_x = relative_end_x
        self.__end_y = relative_end_y
        self.__x = relative_start_x
        self.__y = relative_start_y
        self.__width = width
        self.__height = height
        self.__background_color = 0
        self.__names_colors = 0
        self.__text_colors = []
        self.__border = False
        self.__border_color = 0
        self.__next_key = next_key

        self.__started = False
        self.__open = False
        self.__dialog = None

        self.__current_line = 0
        self.__char_index = 0
        self.__char_speed = char_speed
        self.__frame_count = 0

    def is_dialog(self)-> bool:
        return self.__started

    def start_dialog(self, dialog:Dialog):
        if not self.__started:
            self.__background_color = dialog.background_color
            self.__names_colors = dialog.names_colors
            self.__text_colors = dialog.text_colors
            self.__border = dialog.border
            self.__border_color = dialog.border_color

            self.__started = True
            self.__dialog = dialog
            self.__current_line = 0
            self.__char_index = 0
            self.__frame_count = 0

    def stop_dialog(self):
        self.__started = False
        self.__open = False
        self.__dialog = None

    def update(self):
        if self.__started:
            self.__x = lerp(self.__x, self.__end_x, 0.15)
            self.__y = lerp(self.__y, self.__end_y, 0.15)

            if abs(self.__x - self.__end_x) < 1 and abs(self.__y - self.__end_y) < 1:
                self.__open = True

            if self.__open:
                if self.__char_index < len(self.__dialog.lines[self.__current_line][1]):
                    if pyxel.btnp(self.__next_key):
                        self.__char_index = len(self.__dialog.lines[self.__current_line][1])
                        if self.__dialog.sound:
                            pyxel.play(self.__dialog.channel, self.__dialog.sound_number)
                    self.__frame_count += 1
                    if self.__frame_count % self.__char_speed == 0:
                        if self.__dialog.sound:
                            pyxel.play(self.__dialog.channel, self.__dialog.sound_number)
                        self.__char_index += 1
                else:
                    if pyxel.btnp(self.__next_key):
                        if self.__current_line < len(self.__dialog.lines) - 1:
                            self.__current_line += 1
                            self.__char_index = 0
                            self.__frame_count = 0
                        else:
                            self.__started = False
                            self.__open = False

        else:
            self.__x = lerp(self.__x, self.__start_x, 0.15)
            self.__y = lerp(self.__y, self.__start_y, 0.15)

    def draw(self, camera_x:int=0, camera_y:int=0):
        if abs(self.__x - self.__start_x) < 1 and abs(self.__y - self.__start_y) < 1:
            return

        pyxel.rect(camera_x + self.__x, camera_y + self.__y, self.__width, self.__height, self.__background_color)
        if pyxel.frame_count % (30 * 2) < 50:
            pyxel.text(camera_x + self.__x + self.__width - len(keys_to_representation.get(self.__next_key, "") * 4) - 1, 
                    camera_y + self.__y + self.__height - 7, 
                    keys_to_representation.get(self.__next_key, ""), 
                    self.__text_colors if isinstance(self.__text_colors, int) else self.__text_colors[0])
        if self.__border:
            pyxel.rectb(camera_x + self.__x, camera_y + self.__y, self.__width, self.__height, self.__border_color)
        if self.__open:
            Text(self.__dialog.lines[self.__current_line][0], camera_x + self.__x + 2, camera_y + self.__y + 2, self.__names_colors, 1).draw()
        if self.__dialog:
            visible_text = self.__dialog.lines[self.__current_line][1][:self.__char_index]
            Text(visible_text, camera_x + self.__x + 2, camera_y + self.__y + 14, self.__text_colors, 1).draw()

class Bullet:

    def __init__(self, x:int, y:int, tx:int, ty:int):
        self.x, self.y = x, y
        self.w, self.h = 6, 6
        self.speed = 1.5
        self.lifetime = 500
        self.dither = 1

        mag = ((tx - x) ** 2 + (ty - y) ** 2) ** 0.5
        self.vx = (tx - x) / mag * self.speed
        self.vy = (ty - y) / mag * self.speed

        self.animation = Animation(Sprite(0, 32, 48, self.w, self.h, 14), 3, 15, False)

    def update(self):
        self.lifetime -= 1

        self.x += self.vx
        self.y += self.vy

        if self.x > pyxel.width:
            self.x = -self.w
        elif self.x + self.w < 0:
            self.x = pyxel.width

        if self.y > pyxel.height:
            self.y = -self.h
        elif self.y + self.h < 0:
            self.y = pyxel.height

        self.animation.update()

        if self.lifetime <= 10:
            self.dither = self.lifetime / 10

    def draw(self):
        pyxel.dither(self.dither)
        self.animation.draw(self.x, self.y)
        pyxel.dither(1)

class Player:
    
    def __init__(self, x:int, y:int):
        self.x, self.y = x, y
        self.w, self.h = 16, 16

        self.vx, self.vy = 0, 0
        self.max_vx, self.max_vy = 1.5, 1.5
        self.speed = 0.8
        self.friction = 0.85

        self.bullets = []
        self.shoot_timer = 0

        self.idle = Animation(Sprite(0, 0, 16, 16, 16, 14), 2, 20, True)
        self.walk = Animation(Sprite(0, 0, 32, 16, 16, 14), 2, 10, True)
        self.current_animation = self.idle

        self.health_bar = UIBar(2, 2, 20, 4, 0, 11, 100, 100)

        self.facing_right = True
        self.dead = False
        self.hit = False
        self.shoot = False

    def update_velocity_x(self):
        if self.vx != 0:
            step_x = 1 if self.vx > 0 else -1
            for _ in range(int(abs(self.vx))):
                if True:
                    self.x += step_x
                else:
                    self.vx = 0
                    break

    def update_velocity_y(self):
        if self.vy != 0:
            step_y = 1 if self.vy > 0 else -1
            for _ in range(int(abs(self.vy))):
                if True:
                    self.y += step_y
                else:
                    self.vy = 0
                    break

    def update(self, pyxel_manager:PyxelManager):
        if self.dead:
            self.current_animation.update()
            pyxel_manager.apply_palette_effect(grayscaled_palette)
            return
        else:
            pyxel_manager.reset_palette()
        
        if self.hit:
            self.current_animation.update()
            self.health_bar.update()
            if self.current_animation.is_finished():
                self.hit = False
            return
        
        self.shoot_timer -= 1
        
        if self.shoot and self.current_animation.is_finished():
            self.shoot = False
            self.current_animation = self.idle

        for bullet in self.bullets:
            bullet.update()
            if collision_rect_rect(self.x + 3, self.y + 1, 11, 12, bullet.x, bullet.y, bullet.w, bullet.h) and 0 < bullet.lifetime < 460:
                self.health_bar.current_value -= 10
                bullet.lifetime = 0
                pyxel.play(2, 3)
                self.hit = True
                self.current_animation = Animation(Sprite(0, 0, 64, 16, 16, 14), 3, 10, False)
                self.bullets = [bullet for bullet in self.bullets if bullet.lifetime > 0]
                return
        self.bullets = [bullet for bullet in self.bullets if bullet.lifetime > 0]

        if self.health_bar.current_value <= 0:
            pyxel.play(2, 4)
            self.dead = True
            self.current_animation = Animation(Sprite(0, 0, 80, 16, 16, 14), 5, 25, False)
            return

        self.vx *= self.friction
        self.vy *= self.friction

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_A):
            self.vx = max(self.vx - self.speed, -self.max_vx)
            self.facing_right = False
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.vx = min(self.vx + self.speed, self.max_vx)
            self.facing_right = True
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_W):
            self.vy = max(self.vy - self.speed, -self.max_vy)
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            self.vy = min(self.vy + self.speed, self.max_vy)

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.shoot_timer <= 0:
            self.shoot_timer = 30
            self.bullets.append(Bullet(self.x + 5, self.y + 5, pyxel.mouse_x, pyxel.mouse_y))
            pyxel.play(0, 1)
            self.shoot = True
            self.current_animation = Animation(Sprite(0, 0, 48, 16, 16, 14), 2, 10, False)
            self.facing_right = not pyxel.mouse_x < self.x + 8
            return

        if not self.shoot:
            if abs(self.vx) > 0.1 or abs(self.vy) > 0.1:
                self.current_animation = self.walk
            else:
                self.current_animation = self.idle

        self.update_velocity_x()
        self.update_velocity_y()

        if self.x > pyxel.width:
            self.x = -self.w
        elif self.x + self.w < 0:
            self.x = pyxel.width

        if self.y > pyxel.height:
            self.y = -self.h
        elif self.y + self.h < 0:
            self.y = pyxel.height

        self.current_animation.update()
        self.health_bar.update()

    def draw(self):
        for bullet in self.bullets:
            bullet.draw()

        self.current_animation.sprite.flip_horizontal = not self.facing_right
        self.current_animation.draw(self.x, self.y)

class Spider:

    def __init__(self, x:int, y:int):
        self.x, self.y = x, y
        self.w, self.h = 16, 16
        self.speed = 0.3
        self.dead = False
        self.health = random.choice([50, 60, 70])
        self.attack = False

        self.idle = Animation(Sprite(0, 80, 16, self.w, self.h, 14), 2, 20)
        self.walk = Animation(Sprite(0, 80, 32, self.w, self.h, 14), 4, 10)
        self.current_animation = self.idle

    def update(self, player_x:int, player_y:int, player_bullets:list):
        for bullet in player_bullets:
            if collision_rect_rect(self.x, self.y, self.w, self.h, bullet.x, bullet.y, bullet.w, bullet.h):
                self.health -= 10
                pyxel.play(1, 13)
                bullet.lifetime = 0
                return
            
        if self.health <= 0:
            self.dead = True

        if self.attack:
            self.current_animation.update()
            if self.current_animation.is_finished():
                self.attack = False
                self.current_animation = self.idle
            return

        dx = player_x - self.x
        dy = player_y - self.y
        mag = (dx ** 2 + dy ** 2) ** 0.5

        if mag < 10:
            self.attack = True
            pyxel.play(3, 5)
            self.current_animation = Animation(Sprite(0, 80, 48, self.w, self.h, 14), 5, 10, False)
            self.current_animation.sprite.flip_horizontal = dx < 0
        elif mag < 150:
            self.current_animation = self.walk
            self.current_animation.sprite.flip_horizontal = dx < 0
            self.x += dx / mag * self.speed
            self.y += dy / mag * self.speed
        else:
            self.current_animation = self.idle

        self.current_animation.update()

    def draw(self):
        self.current_animation.draw(self.x, self.y)

class Scarab:

    def __init__(self, x:int, y:int):
        self.x, self.y = x, y
        self.w, self.h = 16, 16
        self.speed = 0.6
        self.dead = False
        self.health = random.choice([20, 30])
        self.attack = False

        self.idle = Animation(Sprite(0, 0, 112, self.w, self.h, 14), 2, 20)
        self.walk = Animation(Sprite(0, 0, 128, self.w, self.h, 14), 4, 10)
        self.current_animation = self.idle

    def update(self, player_x:int, player_y:int, player_bullets:list):
        for bullet in player_bullets:
            if collision_rect_rect(self.x + 3, self.y + 3, 13, 10, bullet.x, bullet.y, bullet.w, bullet.h):
                self.health -= 10
                pyxel.play(1, 13)
                bullet.lifetime = 0
                return
            
        if self.health <= 0:
            self.dead = True

        if self.attack:
            self.current_animation.update()
            if self.current_animation.is_finished():
                self.attack = False
                self.current_animation = self.idle
            return

        dx = player_x - self.x
        dy = player_y - self.y

        if abs(dx) > pyxel.width / 2:
            dx -= pyxel.width * (1 if dx > 0 else -1)
        if abs(dy) > pyxel.height / 2:
            dy -= pyxel.height * (1 if dy > 0 else -1)

        mag = (dx ** 2 + dy ** 2) ** 0.5

        if mag < 10:
            self.attack = True
            pyxel.play(3, 5)
            self.current_animation = Animation(Sprite(0, 0, 144, self.w, self.h, 14), 5, 10, False)
            self.current_animation.sprite.flip_horizontal = dx < 0
        elif mag < 80:
            self.current_animation = self.walk
            self.current_animation.sprite.flip_horizontal = dx < 0
            self.x += dx / mag * self.speed
            self.y += dy / mag * self.speed
        else:
            self.current_animation = self.idle

        if self.x > pyxel.width:
            self.x = -self.w
        elif self.x + self.w < 0:
            self.x = pyxel.width

        if self.y > pyxel.height:
            self.y = -self.h
        elif self.y + self.h < 0:
            self.y = pyxel.height

        self.current_animation.update()

    def draw(self):
        self.current_animation.draw(self.x, self.y)

class Hornet:

    def __init__(self, x:int, y:int):
        self.x, self.y = x, y
        self.w, self.h = 24, 24
        self.speed = 0.4
        self.health = random.choice([40, 50, 60])
        self.dead = False

        self.idle = Animation(Sprite(0, 0, 176, self.w, self.h, 14), 8, 10)
        self.attack = Animation(Sprite(0, 0, 200, self.w, self.h, 14), 8, 10)
        self.current_animation = self.idle

        self.shoot_timer = random.randint(100, 240)
        self.wander_timer = 0

    def update(self, player_x:int, player_y:int, player_bullets:list):
        for bullet in player_bullets:
            if collision_rect_rect(self.x + 6, self.y + 2, 12, 15, bullet.x, bullet.y, bullet.w, bullet.h) and bullet.lifetime < 480:
                self.health -= 10
                pyxel.play(1, 13)
                bullet.lifetime = 0
                return
            
        if self.health <= 0:
            self.dead = True

        mag = ((player_x - self.x) ** 2 + (player_y - self.y) ** 2) ** 0.5

        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            if mag < 80:
                pyxel.play(3, 5)
                player_bullets.append(Bullet(self.x + 9, self.y + 9, player_x, player_y))
            self.shoot_timer = random.randint(100, 240)

        if mag < 80:
            self.current_animation = self.attack
            self.current_animation.sprite.flip_horizontal = player_x - self.x < 0
        else:
            self.current_animation = self.idle

        self.wander_timer -= 1
        if self.wander_timer <= 0:

            mag_tp = 0
            while mag_tp < 50:
                self.tx, self.ty = random.randint(0, 228), random.randint(0, 128)
                mag_tp = ((self.tx - player_x) ** 2 + (self.ty - player_y) ** 2) ** 0.5

            self.wander_timer = 120

        dx = self.tx - self.x
        dy = self.ty - self.y

        if abs(dx) > pyxel.width / 2:
            dx -= pyxel.width * (1 if dx > 0 else -1)
        if abs(dy) > pyxel.height / 2:
            dy -= pyxel.height * (1 if dy > 0 else -1)

        mag = (dx ** 2 + dy ** 2) ** 0.5

        self.x += dx / mag * self.speed
        self.y += dy / mag * self.speed

        if self.x > pyxel.width:
            self.x = -self.w
        elif self.x + self.w < 0:
            self.x = pyxel.width

        if self.y > pyxel.height:
            self.y = -self.h
        elif self.y + self.h < 0:
            self.y = pyxel.height

        self.current_animation.update()

    def draw(self):
        self.current_animation.draw(self.x, self.y)

class WaveManager:

    def __init__(self):
        self.waves = [
            # Intro waves
            [Scarab(100, 64)],
            [Spider(50, 50), Scarab(150, 70)],
            [Spider(40, 60), Spider(180, 80), Scarab(110, 30)],
            [Hornet(114, 64)],
            [Scarab(30, 30), Scarab(190, 90), Hornet(114, 64)],

            # Increasing challenge
            [Spider(20, 20), Spider(200, 100), Hornet(114, 64)],
            [Scarab(50, 20), Scarab(150, 100), Hornet(114, 30)],
            [Spider(80, 30), Scarab(140, 80), Hornet(114, 64)],
            [Spider(50, 50), Spider(160, 60), Hornet(114, 64), Scarab(100, 100)],
            [Hornet(100, 40), Hornet(120, 80)],

            # Mid-game swarm style
            [Spider(10, 10), Spider(200, 10), Spider(10, 100), Spider(200, 100)],
            [Scarab(50, 64), Scarab(170, 64), Hornet(114, 30)],
            [Spider(40, 30), Spider(160, 90), Hornet(114, 64), Hornet(114, 100)],
            [Spider(20, 20), Spider(114, 64), Spider(200, 100), Scarab(114, 20)],
            [Hornet(60, 40), Hornet(160, 40), Hornet(110, 90)],

            # Escalation with mixed enemies
            [Scarab(50, 64), Scarab(170, 64), Scarab(114, 30)],
            [Spider(40, 40), Spider(190, 90), Hornet(114, 64)],
            [Hornet(40, 40), Hornet(190, 90), Scarab(114, 64)],
            [Spider(20, 60), Spider(200, 60), Scarab(114, 20), Scarab(114, 100)],
            [Hornet(80, 40), Hornet(140, 40), Hornet(114, 80)],

            # High-pressure late waves
            [Spider(30, 30), Spider(200, 30), Spider(30, 100), Spider(200, 100), Scarab(114, 64)],
            [Hornet(90, 40), Hornet(130, 40), Scarab(80, 80), Scarab(140, 80)],
            [Spider(20, 20), Spider(200, 20), Scarab(114, 30), Hornet(114, 64), Hornet(114, 100)],
            [Hornet(60, 30), Hornet(160, 30), Hornet(60, 100), Hornet(160, 100)],
            [Spider(50, 50), Spider(170, 50), Scarab(114, 20), Scarab(114, 100), Hornet(114, 64)],

            # Final gauntlet
            [Hornet(50, 30), Hornet(170, 30), Hornet(50, 100), Hornet(170, 100)],
            [Spider(30, 30), Spider(190, 30), Spider(30, 90), Spider(190, 90), Hornet(114, 64)],
            [Scarab(50, 40), Scarab(170, 40), Scarab(50, 90), Scarab(170, 90), Hornet(114, 64)],
            [Hornet(80, 40), Hornet(140, 40), Hornet(80, 90), Hornet(140, 90), Hornet(114, 64)],
            [Spider(20, 20), Spider(200, 20), Scarab(50, 64), Scarab(170, 64), Hornet(114, 64), Hornet(114, 100)],
        ]
        self.wave = -1
        self.transition_timer = 180
        self.enemies = []
        self.explosions = []
        self.win = False

    def update(self, player:Player):
        if not player.hit and not player.dead:
            for enemy in self.enemies:
                enemy.update(player.x, player.y, player.bullets)

                if isinstance(enemy, Spider) and enemy.attack and enemy.current_animation.current_frame == 2 and collision_rect_rect(player.x, player.y, player.w, player.h, enemy.x, enemy.y, enemy.w, enemy.h):
                    player.health_bar.current_value -= 20
                    pyxel.play(2, 3)
                    player.hit = True
                    player.current_animation = Animation(Sprite(0, 0, 64, 16, 16, 14), 3, 10, False)

                if isinstance(enemy, Scarab) and enemy.attack and enemy.current_animation.current_frame == 2 and collision_rect_rect(player.x, player.y, player.x, player.h, enemy.x + 3, enemy.y + 3, 13, 10):
                    player.health_bar.current_value -= 5
                    pyxel.play(2, 3)
                    player.hit = True
                    player.current_animation = Animation(Sprite(0, 0, 64, 16, 16, 14), 3, 10, False)

                if enemy.dead:
                    pyxel.play(1, 2)
                    off = 0 if isinstance(enemy, Hornet) else 4
                    self.explosions.append((Animation(Sprite(0, 24, 224, 24, 24, 14), 8, 5, False), enemy.x - off, enemy.y - off))
            self.enemies = [enemy for enemy in self.enemies if not enemy.dead]

            for anim, x, y in self.explosions:
                anim.update()

        if len(self.enemies) == 0:
            if self.transition_timer == 180:
                player.health_bar.current_value += 10
                self.wave += 1
                if self.wave >= len(self.waves):
                    self.win = True
            self.transition_timer -= 1

        if self.transition_timer <= 0:
            self.transition_timer = 180
            if self.wave < len(self.waves):
                self.enemies = self.waves[self.wave]

    def draw(self):
        for enemy in self.enemies:
            enemy.draw()

        for anim, x, y in self.explosions:
            anim.draw(x, y)
        self.explosions = [(anim, x, y) for anim, x, y in self.explosions if not anim.is_finished()]

        if not self.win:
            pyxel.text(2, 10, f"Wave:{self.wave + 1}", 1)

        if 0 < self.transition_timer < 180 and len(self.enemies) == 0 and self.wave < len(self.waves):
            Text(f"Wave {self.wave + 1} loading...", 114, 64, 1, 1, ANCHOR_CENTER, shadow=True, shadow_color=4).draw()
        if self.win:
            Text("You won !", 114, 64, 1, 2, ANCHOR_CENTER, shadow=True, shadow_color=4).draw()
            Text("Press ESC", 114, 80, 1, 1, ANCHOR_CENTER, shadow=True, shadow_color=4).draw()

class Game:

    def __init__(self):
        #? Scenes
        main_menu_scene = Scene(0, "Loop Shot - Main Menu", self.update_main_menu, self.draw_main_menu, "assets.pyxres")
        credits_scene = Scene(1, "Loop Shot - Credits", self.update_credits, self.draw_credits, "assets.pyxres")
        game_scene = Scene(2, "Loop Shot - Game", self.update_game, self.draw_game, "assets.pyxres", on_enter=self.on_enter_game)
        scenes = [main_menu_scene, credits_scene, game_scene]

        #? Pyxel Init
        self.pyxel_manager = PyxelManager(228, 128, scenes, 0, 60, True, quit_key=pyxel.KEY_NONE)
        pyxel.channels.from_list([pyxel.Channel() for _ in range(7)])
        self.setup_music()

        #? Functions
        def play_action():
            if self.tutorial_done and not self.dialog_manager.is_dialog():
                pyxel.play(0, 0)
                self.pyxel_manager.change_scene_closing_doors(2, 2, 4)
            else:
                self.dialog_manager.start_dialog(self.dialog)
                self.tutorial_done = True

        def credits_action():
            if not self.dialog_manager.is_dialog():
                pyxel.play(0, 0)
                self.pyxel_manager.change_scene_closing_doors(1, 2, 4)

        def back_action():
            pyxel.play(0, 0)
            self.pyxel_manager.change_scene_closing_doors(0, 2, 4)

        #? Main Menu Variables
        self.title = Text("Loop\nShot", 114, 10, 1, 2, ANCHOR_TOP, shadow=True, shadow_color=4, wavy=True)
        self.play_button = Button("Play", 114, 60, 1, 4, 6, 4, 1, True, 4, anchor=ANCHOR_TOP, command=play_action)
        self.credits_button = Button("Credits", 114, 80, 1, 4, 6, 4, 1, True, 4, anchor=ANCHOR_TOP, command=credits_action)
        self.quit_button = Button("Quit", 114, 100, 1, 4, 6, 4, 1, True, 4, anchor=ANCHOR_TOP, command=pyxel.quit)
        self.sound_button = IconButton(2, 112, 1, 4, Sprite(0, 0, 8, 8, 8, 14), True, 4, anchor=ANCHOR_BOTTOM_LEFT, command=self.setup_music)
        self.mute_button = IconButton(2, 126, 1, 4, Sprite(0, 8, 8, 8, 8, 14), True, 4, anchor=ANCHOR_BOTTOM_LEFT, command=self.mute_music)

        self.tutorial_done = False
        self.dialog_manager = DialogManager(5, 130, 5, 126-56, 218, 56)
        self.dialog = Dialog([("Léo", "Hey, welcome to Loop Shot !"),
                              ("Léo", "Use W, A, S, D (or ZQSD) to move.\nYou can move in any direction,\nbut there's no escape."),
                              ("Léo", "Aim and shoot with the mouse.\nYour bullets move fast and go\noff-screen..."),
                              ("Léo", "...but they loop back from the\nopposite side !\nIf you're not careful, you can\nshoot yourself."),
                              ("Léo", "Enemies come in waves and\nthey loop too.\nSome chase. Some shoot.\nAll want you gone."),
                              ("Léo", "Survive as long as you can.\nUse the loop to your advantage..."),
                              ("Léo", "Good Luck !")], 1, 4, 4, True, 4, True, 1, 12)

        #? Credits Variables
        self.credits_title = Text("Credits", 114, 10, 1, 2, ANCHOR_TOP, shadow=True, shadow_color=4, wavy=True)
        self.credits_text = Text('This game was made for the\n2025 GMTK game jam\nusing pyxel and mostly the\n"Robot Warfare" asset pack from\nMattWalkden', 114, 52, 1, 1, ANCHOR_TOP, shadow=True, shadow_color=4)
        self.back_button = Button("Back", 5, 123, 1, 4, 6, 4, 1, True, 4, anchor=ANCHOR_BOTTOM_LEFT, command=back_action)

        #? Game Variables
        self.tlm_u, self.tlm_v = 0, 0
        self.player = Player(0, 0)
        self.wave_manager = WaveManager()

        #? Run
        self.pyxel_manager.run()

    def setup_music(self):
        pyxel.sounds[6].set("c1d#1d#1c1 g0g0a#0a#0 f0f0d#0d#0 d1d1c1c1","0","1","nfnfnfvn",24)
        pyxel.sounds[9].set("a#0g0f0d#0 c1d#1f1g1 a#0a#0g0g0 f0f0c1c1","0","1","nfvnfnfv",24)

        pyxel.sounds[7].set("d#2f2g2a#2 g2f2d#2c2 d#2f2g2f2 d#2c2a#1g1","1","1","vnnvnfnn",24)
        pyxel.sounds[10].set("c2d#2f2g2 a#2g2f2d#2 g2a#2c3d#3 c3a#2g2f2","1","1","nvnvvnvn",24)

        pyxel.sounds[8].set("g1a#1c2d#2 f1a#1d#2f2 c2d#2g2a#2 g1g1a#1a#1","2","2","nnvnfvnf",24)
        pyxel.sounds[11].set("d2f2g2a#2 g2f2d#2c2 a#1c2d#2f2 d#2c2a#1g1","2","2","nfvnfnvn",24)

        pyxel.musics[0].set([], [], [], [], [6, 9], [7, 10], [8, 11])
        pyxel.playm(0, loop=True)

    def mute_music(self):
        for channel in [4, 5, 6]:
            pyxel.stop(channel)

    def on_enter_game(self):
        self.tlm_u, self.tlm_v = random.choice([(0, 0), (0, 24*8), (0, 48*8)])
        self.player = Player(random.randint(0, 228), random.randint(0, 128))
        self.wave_manager = WaveManager()

    def update_main_menu(self):
        self.title.update()
        self.play_button.update()
        self.credits_button.update()
        self.quit_button.update()
        self.sound_button.update()
        self.mute_button.update()
        self.dialog_manager.update()

    def draw_main_menu(self):
        pyxel.cls(0)

        pyxel.bltm(0, 0, 0, 0, 24*8, 228, 128, 0)

        self.title.draw()
        self.play_button.draw()
        self.credits_button.draw()
        self.quit_button.draw()
        self.sound_button.draw()
        self.mute_button.draw()
        self.dialog_manager.draw()

        pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 0, 0, 0, 8, 8, 14)

    def update_credits(self):
        self.credits_title.update()
        self.credits_text.update()
        self.back_button.update()

    def draw_credits(self):
        pyxel.cls(0)

        pyxel.bltm(0, 0, 0, 0, 0, 228, 128, 0)

        self.credits_title.draw()
        self.credits_text.draw()
        self.back_button.draw()

        pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 0, 0, 0, 8, 8, 14)

    def update_game(self):
        self.player.update(self.pyxel_manager)
        if self.player.hit:
            self.pyxel_manager.shake_camera(2, 0.5)
        self.wave_manager.update(self.player)

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.play(0, 0)
            self.pyxel_manager.change_scene_closing_doors(0, 2, 4)

    def draw_game(self):
        pyxel.cls(6)
        pyxel.bltm(0, 0, 0, self.tlm_u, self.tlm_v, 228, 128, 0)

        if self.player.dead and self.player.current_animation.is_finished():
            self.pyxel_manager.change_scene_closing_doors(0, 2, 4)
            self.player.current_animation = Animation(Sprite(0, 64, 80, 16, 16, 14), 1, 20)

        self.player.draw()
        self.wave_manager.draw()

        self.player.health_bar.draw()
        pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 0, 0, 0, 8, 8, 14)

def lerp(start:float, end:float, speed:float=0.1)-> float:
    return start + (end - start) * speed

def text_size(text:str, font_size:int=1)-> tuple:
    lines = text.split("\n")
    if font_size == 0:
        return (max(len(line) * 4 for line in lines), 6 * len(lines))
    text_width = max(sum(len(characters_matrices[char][0]) * font_size + font_size for char in line) - font_size for line in lines)
    text_height = (9 * font_size + 1) * len(lines)

    return (text_width, text_height)

def get_anchored_position(x:int, y:int, w:int, h:int, anchor:int)-> tuple:
    if anchor in [ANCHOR_TOP_RIGHT, ANCHOR_BOTTOM_RIGHT, ANCHOR_RIGHT]:
        x -= w
    if anchor in [ANCHOR_BOTTOM_LEFT, ANCHOR_BOTTOM_RIGHT, ANCHOR_BOTTOM]:
        y -= h
    if anchor in [ANCHOR_TOP, ANCHOR_BOTTOM, ANCHOR_CENTER]:
        x -= w // 2
    if anchor in [ANCHOR_LEFT, ANCHOR_RIGHT, ANCHOR_CENTER]:
        y -= h // 2
        
    return x, y

def collision_rect_rect(x1:int, y1:int, w1:int, h1:int, x2:int, y2:int, w2:int, h2:int)-> bool:
    return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)

def hex_to_rgb(hex_val:int)-> tuple:
    r = (hex_val >> 16) & 0xFF
    g = (hex_val >> 8) & 0xFF
    b = hex_val & 0xFF
    return r, g, b

def rgb_to_hex(r:int, g:int, b:int)-> int:
    return int(f"0x{r:02X}{g:02X}{b:02X}", 16)

def grayscaled_palette(original_palette:list, kwargs:dict)-> list:
    palette = []
    for color in original_palette:
        r, g, b = hex_to_rgb(color)
        gray = int((r + g + b) / 3)
        palette.append(rgb_to_hex(gray, gray, gray))

    return palette

if __name__ == "__main__":
    Game()