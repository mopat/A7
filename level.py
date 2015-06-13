#!/usr/bin/env python3

import wiimote
import time
import sys
    
input("Press the 'sync' button on the back of your Wiimote Plus " +
          "or buttons (1) and (2) on your classic Wiimote.\n" +
          "Press <return> once the Wiimote's LEDs start blinking.")

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

# Demo Time!
patterns = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]]
for i in range(5):
    for p in patterns:
        wm.leds = p
        time.sleep(0.05)


"""def print_ir(ir_data):
    if len(ir_data) == 0:
        return
    for ir_obj in ir_data:
        #print("%4d %4d %2d     " % (ir_obj["x"],ir_obj["y"],ir_obj["size"]), end=' ')
        #print("%4d %4d %2d     " % (ir_obj["x"],ir_obj["y"],ir_obj["size"]))
    #print()

wm.ir.register_callback(print_ir)"""

def lightUpLEDs(arr):
    for i in range(4):
        wm.leds[i] = False
    for i in range(len(arr)):
        c = arr[i]
        wm.leds[c] = True

def checkHorizontal(bubVal):
    if isYaxis:
        if bubVal == 410 or bubVal == 610:
            wm.rumble(0.5)
            for i in range(4):
                wm.leds[i] = True
            time.sleep(0.5)
    if isXaxis:
        if bubVal == 510:
            wm.rumble(0.5)
            for i in range(4):
                wm.leds[i] = True
            time.sleep(0.5)
while True:
    bubVal = wm.accelerometer[1]
    checkHorizontal(bubVal)

    if wm.buttons["Left"] or wm.buttons["Right"]:
        isXaxis = True
        isYaxis = False
        print ("X-Axis now enabled")

    if wm.buttons["Up"] or wm.buttons["Down"]:
        isXaxis = False
        isYaxis = True
        print ("Y-Axis now enabled")


    if wm.buttons["A"]:
        wm.leds[1] = True
        wm.rumble(0.1)
        print((wm.accelerometer))
    else:
        if isXaxis:
            if bubVal > 577:
                leds = [3]
            if bubVal <= 577 and bubVal > 544:
                leds = [3,2]
            if bubVal <= 544 and bubVal > 510:
                leds = [3,2,1]
            if bubVal < 443:
                leds = [0]
            if bubVal >= 443 and bubVal < 476:
                leds = [0, 1]
            if bubVal >= 476 and bubVal < 510:
                leds = [0,1,2]
        if isYaxis:
            if bubVal < 610 and bubVal > 577:
                leds = [0,1,2]
            if bubVal <= 577 and bubVal > 544:
                leds = [0,1]
            if bubVal <= 544 and bubVal > 511:
                leds = [0]
            if bubVal <= 511 and bubVal > 478:
                leds = [3]
            if bubVal <= 478 and bubVal > 445:
                leds = [3,2]
            if bubVal <= 445 and bubVal > 410:
                leds = [3,2,1]
        lightUpLEDs(leds)
        pass
    time.sleep(0.05)
