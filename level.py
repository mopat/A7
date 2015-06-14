#!/usr/bin/env python3

import wiimote
import time
import sys

input("Press the 'sync' button on the back of your Wiimote Plus " + "or buttons (1) and (2) on your classic Wiimote.\n" + "Press <return> once the Wiimote's LEDs start blinking.")

if len(sys.argv) == 1:
    addr, name = wiimote.find()[0]
elif len(sys.argv) == 2:
    addr = sys.argv[1]
    name = None
elif len(sys.argv) == 3:
    addr, name = sys.argv[1:3]
print(("Connecting to %s (%s)" % (name, addr)))
wm = wiimote.connect(addr, name)

isXaxis = True
isYaxis = False

patterns = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
for i in range(5):
    for p in patterns:
        wm.leds = p
        time.sleep(0.05)


# function to light up leds given as paramaneter
def lightUpLEDs(arr):
    # deactivate all leds
    for i in range(4):
        wm.leds[i] = False
    # actiate given leds
    for i in range(len(arr)):
        c = arr[i]
        wm.leds[c] = True


# function to check if wiimote is horizontal
def checkHorizontal(bubVal):
    # check different values vor x and y axis, light up leds and rumble
    # when specific horizontal value is reached
    if isYaxis:
        if bubVal == 410 or bubVal == 610:
            wm.rumble(0.2)
            lightUpLEDs([0, 1, 2, 3])
            time.sleep(0.5)
    elif isXaxis:
        if bubVal == 510:
            wm.rumble(0.2)
            lightUpLEDs([0, 1, 2, 3])
            time.sleep(0.5)


while True:
    wm.isHorizontal = False
    # read out bubble value from wiimote accelerometer
    bubVal = wm.accelerometer[1]
    # check if wiimote is horizontal
    checkHorizontal(bubVal)

    # switch mode to x axis bubble value
    if wm.buttons["Left"] or wm.buttons["Right"]:
        isXaxis = True
        isYaxis = False

    # switch mode to y axis bubble value
    if wm.buttons["Up"] or wm.buttons["Down"]:
        isXaxis = False
        isYaxis = True

    # print accelerometer values
    if wm.buttons["A"]:
        wm.leds[1] = True
        print((wm.accelerometer))
    else:
        leds = []  # array for the leds to light up

        # steps for the different leds to light up
        # depending on the maximum values for x (510) or y axis (410, 610)
        if isXaxis:
            if bubVal > 577:
                leds = [3]
            elif bubVal <= 577 and bubVal > 544:
                leds = [3, 2]
            elif bubVal <= 544 and bubVal > 510:
                leds = [3, 2, 1]
            elif bubVal < 443:
                leds = [0]
            elif bubVal >= 443 and bubVal < 476:
                leds = [0,  1]
            elif bubVal >= 476 and bubVal < 510:
                leds = [0, 1, 2]
        elif isYaxis:
            if bubVal < 610 and bubVal > 577:
                leds = [0, 1, 2]
            elif bubVal <= 577 and bubVal > 544:
                leds = [0, 1]
            elif bubVal <= 544 and bubVal > 511:
                leds = [0]
            elif bubVal <= 511 and bubVal > 478:
                leds = [3]
            elif bubVal <= 478 and bubVal > 445:
                leds = [3, 2]
            elif bubVal <= 445 and bubVal > 410:
                leds = [3, 2, 1]
        lightUpLEDs(leds)  # light up the determined leds
        pass
    time.sleep(0.05)
