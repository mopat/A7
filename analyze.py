#!/usr/bin/env python3

import wiimote_node as wmn
import time
import sys

class Analyze():
    def __init__(self):
        self.name = "Wiimote"
        if len(sys.argv) > 1:
            self.btaddr = sys.argv[1]
        print(self.btaddr)

if __name__ == '__main__':
    an = Analyze()
    wmn = wmn.WiimoteNode("Wiimote")
