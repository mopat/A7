#!/usr/bin/env python3

import wiimote_node as wmn
import time
import sys
import numpy as np
from wiimote_node import *


class StdDevNode(Node):
    nodeName = "StdDev"

    def __init__(self, name):

        terminals = {
            'dataIn': dict(io='in'),
            'dataOut': dict(io='out')
        }

        self.stdDevArray = np.array([])

        Node.__init__(self, name, terminals=terminals)

    def process(self, **kwds):

        self.stdDevArray = np.append(self.stdDevArray, kwds['dataIn'])

        stdDev = np.std(self.stdDevArray, dtype=np.float64)

        #print (stdDev)

        return {'dataOut': stdDev}


fclib.registerNodeType(StdDevNode, [('Data')])

class NumberDisplayNode(Node):
    nodeName = "NumberDisplay"

    def __init__(self, name):

        terminals = {
            'dataIn': dict(io='in'),
            'dataOut': dict(io='out')
        }

        Node.__init__(self, name, terminals=terminals)

    def process(self, **kwds):
        values = 1

        Analyze.getLcdValues(self, kwds['dataIn'])





fclib.registerNodeType(NumberDisplayNode, [('Data')])

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
        self.bufferPlots()

        self.lcdWidget = QtGui.QLCDNumber()
        self.layout.addWidget(self.lcdWidget, 0, 0)

        self.stdDevNode()
        self.numberDisplayNode()

        self.win.show()
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    # create plotwidgets
    def createWidgets(self):

        #self.lcdWidget = QtGui.QLCDNumber()
        #self.layout.addWidget(self.lcdWidget, 0, 0)

        print ("test")

    def getLcdValues(self, values):
        print(values)

        self.layout.addWidget(self.lcdWidget, 0, 0)


        #Analyze.displayLcd(values)
        #self.lcdWidget.display(values)

    def displayLcd(self, values):


        self.lcdWidget.display(values)

    # create node for wiimote
    def wiimoteNode(self):
        self.wiimoteNode = self.fc.createNode('Wiimote', pos=(0, 0), )
        self.wiimoteNode.text.setText(self.btaddr)
        self.wiimoteNode.btaddr = self.btaddr  # set wiimote bluetooth adress

        self.wiimoteNode.connect_wiimote()  # use module function to connect to wiimote

    # plot the buffers for the accelerometer data
    def bufferPlots(self):
        # buffers for x, y and z-Axis
        self.bufferNodeX = self.fc.createNode('Buffer', pos=(150, 0))

        # connect buffers to the plots
        self.fc.connectTerminals(self.wiimoteNode['accelX'], self.bufferNodeX['dataIn'])

        # display buffer data in the plots
        #self.fc.connectTerminals(bufferNodeX['dataOut'], self.pw1Node['In'])

    def stdDevNode(self):
        self.stdDevNode = self.fc.createNode('StdDev', pos=(0, 0), )

        self.fc.connectTerminals(self.bufferNodeX['dataOut'], self.stdDevNode['dataIn'])
        #self.fc.connectTerminals(self.stdDevNode['dataOut'], self.pw1Node['In'])

    def numberDisplayNode(self):
        self.numberDisplayNode = self.fc.createNode('NumberDisplay', pos=(0, 0), )

        self.fc.connectTerminals(self.stdDevNode['dataOut'], self.numberDisplayNode['dataIn'])

if __name__ == '__main__':
    an = Analyze()
