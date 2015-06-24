#!/usr/bin/env python3

import wiimote_node as wmn
import time
import sys
import numpy as np
from wiimote_node import *
#from PyQt5 import QtCore, QtWidgets
#from PyQt5.QtCore import Qt
#from PyQt5.QtWidgets import (QLCDNumber, QSlider, QVBoxLayout)


# Creating node for standard deviation
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

        # Calculating standard deviation
        stdDev = np.std(self.stdDevArray, dtype=np.float64)

        return {'dataOut': stdDev}


fclib.registerNodeType(StdDevNode, [('Data')])


# Creating node for displaying standard deviation
class NumberDisplayNode(Node):
    nodeName = "NumberDisplay"

    def __init__(self, name):

        terminals = {
            'dataIn': dict(io='in'),
            'dataOut': dict(io='out')
        }
        # Creating LCD widget
        self.lcdWidget = QtGui.QLCDNumber()
        self.lcdWidget.setGeometry(300, 300, 250, 150)
        self.lcdWidget.setWindowTitle('Standard Deviation')
        Node.__init__(self, name, terminals=terminals)

    def process(self, **kwds):
        values = 1
        self.values = kwds['dataIn']
        # Updating LCD widget with data in
        self.lcdWidget.display(self.values)
        self.lcdWidget.show()

fclib.registerNodeType(NumberDisplayNode, [('Data')])


class Noisalyze():
    def __init__(self):
        self.name = "Wiimote"
        if len(sys.argv) > 1:
            self.btaddr = sys.argv[1]
        app = QtGui.QApplication([])
        # create layout
        self.win = QtGui.QMainWindow()
        self.win.setWindowTitle('Wiimote Noisalyzer')
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
        self.wiimoteNode()
        self.bufferPlots()

        self.stdDevNode()
        self.numberDisplayNode()

        self.win.show()
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

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

    def stdDevNode(self):
        self.stdDevNode = self.fc.createNode('StdDev', pos=(300, 150), )

        self.fc.connectTerminals(self.bufferNodeX['dataOut'], self.stdDevNode['dataIn'])

    def numberDisplayNode(self):

        self.numberDisplayNode = self.fc.createNode('NumberDisplay', pos=(450, 150), )

        self.fc.connectTerminals(self.stdDevNode['dataOut'], self.numberDisplayNode['dataIn'])

if __name__ == '__main__':
    an = Noisalyze()
