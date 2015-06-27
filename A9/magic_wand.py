#!/usr/bin/env python3

import wiimote_node as wmn
import time
import sys

from wiimote_node import *

class IrNode(Node):

    nodeName = "IR"

    def __init__(self, name):

        terminals = {
            'IrX': dict(io='out'),
            'IrY': dict(io='out'),
        }
        # Array for data in
        self.gestureRunning = False
        self.x = []
        self.y = []
        self.wm = an.getWiimote()

        Node.__init__(self, name, terminals=terminals)



    # process data and calculate fft
    def process(self, **kwds):
        self.irData = self.wm.ir
        #print(self.wiimoteNode.wiimote.ir)
        while self.wm.buttons["A"]:
            print("A")
            self.gestureRunning = True
            self.saveIrData(self.wmir)
        if self.wm.buttons["A"] == False and self.gestureRunning == True:
            self.gestureRunning = False
            print(self.x)
            print(self.y)
            print("gestureEnd")


        time.sleep(0.05)

        self.saveIrData(self.irData)
        # return frequency and absolute of x
        return {'IrX': 0, 'IrY': 0}

    def saveIrData(self, ir_data):
        #print("GESTURERUNNING")
        if len(ir_data) == 0:
            return
        for ir_obj in ir_data:
            #print("%4d %4d %2d     " % (ir_obj["x"],ir_obj["y"],ir_obj["size"]), end=' ')
            #print("%4d %4d %2d     " % (ir_obj["x"],ir_obj["y"],ir_obj["size"]))
            self.x.append(self.irData["x"])
            self.y.append(self.irData["y"])

fclib.registerNodeType(IrNode, [('Data',)])

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
        self.IrNode()


        self.win.show()


        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()



        self.wiimoteNode.wiimote.ir.register_callback(self.print_ir)


    # create plotwidgets
    def createWidgets(self):
        self.pw1 = pg.PlotWidget()
        self.layout.addWidget(self.pw1, 0, 1)
        self.pw1.setYRange(0, 1024)
        self.pw1Node = self.fc.createNode('PlotWidget', pos=(150, -150))
        self.pw1Node.setPlot(self.pw1)

        self.pw2 = pg.PlotWidget()
        self.layout.addWidget(self.pw2, 0, 2)
        self.pw2.setYRange(0, 1024)
        self.pw2Node = self.fc.createNode('PlotWidget', pos=(300, -150))
        self.pw2Node.setPlot(self.pw2)

    # create node for wiimote
    def wiimoteNode(self):
        self.wiimoteNode = self.fc.createNode('Wiimote', pos=(0, 0), )
        self.wiimoteNode.text.setText(self.btaddr)
        self.wiimoteNode.btaddr = self.btaddr  # set wiimote bluetooth adress

        self.wiimoteNode.connect_wiimote()  # use module function to connect to wiimote

    def getWiimote(self):
        return self.wiimoteNode.wiimote

    # plot the buffers for the accelerometer data
    def bufferPlots(self):
        # buffers for x, y and z-Axis
        bufferNodeX = self.fc.createNode('Buffer', pos=(150, 0))
        bufferNodeY = self.fc.createNode('Buffer', pos=(300, 0))
        bufferNodeZ = self.fc.createNode('Buffer', pos=(450, 0))

        # connect buffers to the plots
        self.fc.connectTerminals(self.wiimoteNode['accelX'], bufferNodeX['dataIn'])
        self.fc.connectTerminals(self.wiimoteNode['accelY'], bufferNodeY['dataIn'])
        self.fc.connectTerminals(self.wiimoteNode['accelZ'], bufferNodeZ['dataIn'])

        # display buffer data in the plots
        self.fc.connectTerminals(bufferNodeX['dataOut'], self.pw1Node['In'])
        self.fc.connectTerminals(bufferNodeY['dataOut'], self.pw2Node['In'])
        self.fc.connectTerminals(bufferNodeZ['dataOut'], self.pw3Node['In'])

    def IrNode(self):
        bufferNodeX = self.fc.createNode('Buffer', pos=(150, 0))
        bufferNodeY = self.fc.createNode('Buffer', pos=(300, 0))

        self.IrNode = self.fc.createNode('IR', pos=(150, 0))
        self.fc.connectTerminals(self.IrNode['IrX'], bufferNodeX['dataIn'])
        self.fc.connectTerminals(self.IrNode['IrY'], bufferNodeY['dataIn'])



if __name__ == '__main__':
    an = Analyze()
