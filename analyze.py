#!/usr/bin/env python3

import wiimote_node as wmn
import time
import sys

from wiimote_node import *

class Analyze():
    def __init__(self):
        self.name = "Wiimote"
        if len(sys.argv) > 1:
            self.btaddr = sys.argv[1]

if __name__ == '__main__':
    import sys


    an = Analyze()
    app = QtGui.QApplication([])
    win = QtGui.QMainWindow()
    win.setWindowTitle('WiimoteNode demo')
    cw = QtGui.QWidget()
    win.setCentralWidget(cw)
    layout = QtGui.QGridLayout()
    cw.setLayout(layout)

    ## Create an empty flowchart with a single input and output
    fc = Flowchart(terminals={
    })
    w = fc.widget()

    layout.addWidget(fc.widget(), 0, 0, 2, 1)

    pw1 = pg.PlotWidget()
    layout.addWidget(pw1, 0, 1)
    pw1.setYRange(0,1024)
    pw1Node = fc.createNode('PlotWidget', pos=(0, -150))
    pw1Node.setPlot(pw1)

    pw2 = pg.PlotWidget()
    layout.addWidget(pw2, 0, 2)
    pw2.setYRange(0,1024)
    pw2Node = fc.createNode('PlotWidget', pos=(0, -150))
    pw2Node.setPlot(pw2)

    pw3 = pg.PlotWidget()
    layout.addWidget(pw3, 0, 3)
    pw3.setYRange(0,1024)
    pw3Node = fc.createNode('PlotWidget', pos=(0, -150))
    pw3Node.setPlot(pw3)


    wiimoteNode = fc.createNode('Wiimote', pos=(0, 0), )
    wiimoteNode.text.setText(an.btaddr)
    wiimoteNode.btaddr = an.btaddr

    wiimoteNode.connect_wiimote()
    """
    fNode = fc.createNode('GaussianFilter', pos=(0, 0))
    fNode.ctrls['sigma'].setValue(5)
    fc.connectTerminals(pw1Node['dataOut'], fNode['dataIn'])
    fc.connectTerminals(fNode['dataOut'], pw2Node['In'])
    """

    bufferNodeX = fc.createNode('Buffer', pos=(150, 0))
    bufferNodeY = fc.createNode('Buffer', pos=(150, 0))
    bufferNodeZ = fc.createNode('Buffer', pos=(150, 0))

    fc.connectTerminals(wiimoteNode['accelX'], bufferNodeX['dataIn'])
    fc.connectTerminals(wiimoteNode['accelY'], bufferNodeY['dataIn'])
    fc.connectTerminals(wiimoteNode['accelZ'], bufferNodeZ['dataIn'])

    fc.connectTerminals(bufferNodeX['dataOut'], pw1Node['In'])
    fc.connectTerminals(bufferNodeY['dataOut'], pw2Node['In'])
    fc.connectTerminals(bufferNodeZ['dataOut'], pw3Node['In'])


    win.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()