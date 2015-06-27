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
        app = QtGui.QApplication([])
        # create layout
        self.win = QtGui.QMainWindow()
        self.win.setWindowTitle('Wiimote Analayzer')
        self.cw = QtGui.QWidget()
        self.win.setCentralWidget(self.cw)
        self.layout = QtGui.QGridLayout()
        self.cw.setLayout(self.layout)

        #create flowchart with data in and out properties
        self.fc = Flowchart(terminals={
            'dataIn': {'io': 'in'},
            'dataOut': {'io': 'out'}
        })
        self.w = self.fc.widget()

        # add flowchart to layout
        self.layout.addWidget(self.fc.widget(), 0, 0, 2, 1)

        # use bottom defined functions to create widgets, plotting and nodes
        #self.createWidgets()
        self.wiimoteNode()
        #self.bufferPlots()
        #self.filterNodes()

        self.gestureRunning = False
        self.x = []
        self.y = []
        self.checkButtons()
        #self.win.show()





        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()


    def checkButtons(self):
        while True:

            # print(self.wiimoteNode.wiimote.ir)
            while self.wiimoteNode.wiimote.buttons["A"]:
                    self.gestureRunning = True
                    self.saveIrData(self.wiimoteNode.wiimote.ir)
            if self.wiimoteNode.wiimote.buttons["A"] == False and self.gestureRunning == True:
                self.gestureRunning = False
                print(self.x)
                print(self.y)
                print("gestureEnd")
                pg.plot(self.x, self.y, pen=None, symbol='o')
        time.sleep(0.05)


    def saveIrData(self, ir_data):
        if len(ir_data) == 0:
            return
        for ir_obj in ir_data:
            #print("%4d %4d %2d     " % (ir_obj["x"],ir_obj["y"],ir_obj["size"]), end=' ')
            print("%4d %4d %2d     " % (ir_obj["x"],ir_obj["y"],ir_obj["size"]))
            self.x.append(ir_obj["x"])
            self.y.append(ir_obj["y"])


    # create plotwidgets
    def createWidgets(self):
        self.pw1 = pg.PlotWidget()
        self.layout.addWidget(self.pw1, 0, 1)
        self.pw1.setYRange(0, 1024)
        self.pw1Node = self.fc.createNode('PlotWidget', pos=(150, -150))
        self.pw1Node.setPlot(self.pw1)


    # create node for wiimote
    def wiimoteNode(self):
        self.wiimoteNode = self.fc.createNode('Wiimote', pos=(0, 0), )
        self.wiimoteNode.text.setText(self.btaddr)
        self.wiimoteNode.btaddr = self.btaddr  # set wiimote bluetooth adress

        self.wiimoteNode.connect_wiimote()  # use module function to connect to wiimote


if __name__ == '__main__':
    an = Analyze()



