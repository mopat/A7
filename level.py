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

while True:
    if wm.buttons["Left"] or wm.buttons["Right"]:
        isXaxis = True
        isYaxis = False
        print ("X-Axis now enabled")

    if wm.buttons["Up"] or wm.buttons["Down"]:
        isXaxis = False
        isYaxis = True
        print ("Y-Axis now enabled")

    if isYaxis:
        if wm.accelerometer[1] == 410 or wm.accelerometer[1] == 610:
            wm.rumble(0.5)
            for i in range(4):
                wm.leds[i] = True
            time.sleep(0.5)
    if isXaxis:
        if wm.accelerometer[1] == 510:
            wm.rumble(0.5)
            for i in range(4):
                wm.leds[i] = True
            time.sleep(0.5)

    if wm.buttons["A"]:
        wm.leds[1] = True
        wm.rumble(0.1)
        print((wm.accelerometer))
    else:
        for i in range(4):
                wm.leds[i] = False
        if isXaxis:
            if wm.accelerometer[1] > 585:
                wm.leds[3] = True
            if wm.accelerometer[1] < 585 and wm.accelerometer[1] > 560:
                wm.leds[3] = True
                wm.leds[2] = True
            if wm.accelerometer[1] < 560 and wm.accelerometer[1] > 510:
                wm.leds[3] = True
                wm.leds[2] = True
                wm.leds[1] = True
            if wm.accelerometer[1] < 435:
                wm.leds[0] = True
            if wm.accelerometer[1] > 435 and wm.accelerometer[1] < 460:
                wm.leds[0] = True
                wm.leds[1] = True
            if wm.accelerometer[1] > 460 and wm.accelerometer[1] < 510:
                wm.leds[0] = True
                wm.leds[1] = True
                wm.leds[2] = True
        if isYaxis:
            if wm.accelerometer[1] < 610 and wm.accelerometer[1] > 560:
                wm.leds[0] = True
                wm.leds[1] = True
                wm.leds[2] = True
            if wm.accelerometer[1] < 560 and wm.accelerometer[1] > 535:
                wm.leds[0] = True
                wm.leds[1] = True
            if wm.accelerometer[1] < 535 and wm.accelerometer[1] > 510:
                wm.leds[0] = True
            if wm.accelerometer[1] < 510 and wm.accelerometer[1] > 485:
                wm.leds[3] = True
            if wm.accelerometer[1] < 485 and wm.accelerometer[1] > 460:
                wm.leds[3] = True
                wm.leds[2] = True
            if wm.accelerometer[1] < 460 and wm.accelerometer[1] > 410:
                wm.leds[3] = True
                wm.leds[2] = True
                wm.leds[1] = True
        pass
    time.sleep(0.05)

