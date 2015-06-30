#!/usr/bin/env python3
# coding: utf-8
# -*- coding: utf-8 -*-

from pyqtgraph.flowchart import Flowchart, Node
from pyqtgraph.flowchart.library.common import CtrlNode
import pyqtgraph.flowchart.library as fclib
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import wiimote


class BufferNode(CtrlNode):
    """
    Buffers the last n samples provided on input and provides them as a list of
    length n on output.
    A spinbox widget allows for setting the size of the buffer. 
    Default size is 32 samples.
    """
    nodeName = "Buffer"
    uiTemplate = [
        ('size',  'spin', {'value': 32.0, 'step': 1.0, 'range': [0.0, 128.0]}),
    ]

    def __init__(self, name):
        terminals = {
            'dataIn': dict(io='in'),  
            'dataOut': dict(io='out'), 
        }
        self._buffer = np.array([])
        CtrlNode.__init__(self, name, terminals=terminals)
        
    def process(self, **kwds):
        size = int(self.ctrls['size'].value())
        self._buffer = np.append(self._buffer, kwds['dataIn'])
        self._buffer = self._buffer[-size:]
        output = self._buffer
        return {'dataOut': output}

fclib.registerNodeType(BufferNode, [('Data',)])
        
class WiimoteNode(Node):
    """
    Outputs sensor data from a Wiimote.
    
    Supported sensors: accelerometer (3 axis)
    Text input box allows for setting a Bluetooth MAC address. 
    Pressing the "connect" button tries connecting to the Wiimote.
    Update rate can be changed via a spinbox widget. Setting it to "0" 
    activates callbacks every time a new sensor value arrives (which is
    quite often -> performance hit)
    """
    nodeName = "Wiimote"
    
    def __init__(self, name):
        terminals = {
            'accelX': dict(io='out'),  
            'accelY': dict(io='out'), 
            'accelZ': dict(io='out'),
            'irX': dict(io='out'),
            'irY': dict(io='out'),
            'irS': dict(io='out'),
            'a': dict(io='out'),
        }
        self.wiimote = None
        self._acc_vals = []

        # Configuration UI
        self.ui = QtGui.QWidget()
        self.layout = QtGui.QGridLayout()
        
        label = QtGui.QLabel("Bluetooth MAC address:")
        self.layout.addWidget(label)
        
        self.text = QtGui.QLineEdit()
        self.btaddr = "B8:AE:6E:1B:AD:A0" # set some example
        self.text.setText(self.btaddr)
        self.layout.addWidget(self.text)
        
        label2 = QtGui.QLabel("Update rate (Hz)")
        self.layout.addWidget(label2)
        self._ir_vals = []

        self.irXVals = []
        self.irYVals = []
        self.irSVals = []
        self.irX = 1
        self.irY = 1
        self.irS = 1

        self.update_rate_input = QtGui.QSpinBox()
        self.update_rate_input.setMinimum(0)
        self.update_rate_input.setMaximum(60)
        self.update_rate_input.setValue(20)
        self.update_rate_input.valueChanged.connect(self.set_update_rate)
        self.layout.addWidget(self.update_rate_input)

        self.connect_button = QtGui.QPushButton("connect")
        self.connect_button.clicked.connect(self.connect_wiimote)
        self.layout.addWidget(self.connect_button)
        self.ui.setLayout(self.layout)
       
        # update timer
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_all_sensors)
        self.isAPressed = False


        # super()

        Node.__init__(self, name, terminals=terminals)
        

    def update_all_sensors(self):
        if self.wiimote == None:
            return
        self._acc_vals = self.wiimote.accelerometer
        self._ir_vals = self.wiimote.ir
        self.update()

    def update_accel(self, acc_vals):
        self._acc_vals = acc_vals
        self.update()

    def update_ir(self, ir_vals):
        if len(ir_vals) == 0:
            return
        self._ir_vals = ir_vals
        self.update()

    def ctrlWidget(self):
        return self.ui

        
    def connect_wiimote(self):
        self.btaddr = str(self.text.text()).strip()
        if self.wiimote is not None:
            self.wiimote.disconnect()
            self.wiimote = None
            self.connect_button.setText("connect")
            return 
        if len(self.btaddr) == 17 :
            self.connect_button.setText("connecting...")
            self.wiimote = wiimote.connect(self.btaddr)
            if self.wiimote == None:
                self.connect_button.setText("try again")
            else:
                self.connect_button.setText("disconnect")
                self.set_update_rate(self.update_rate_input.value())

    def set_update_rate(self, rate):
        if rate == 0: # use callbacks for max. update rate
            self.update_timer.stop()
            self.wiimote.accelerometer.register_callback(self.update_accel)
            self.wiimote.ir.register_callback(self.update_ir)
        else:
            self.wiimote.accelerometer.unregister_callback(self.update_accel)
            self.wiimote.ir.unregister_callback(self.update_ir)
            self.update_timer.start(1000.0/rate)

    def process(self, **kwdargs):
        if(len(self._ir_vals) != 0):
            for ir_obj in self._ir_vals:
                #print("%4d %4d %2d     " % (ir_obj["x"],ir_obj["y"],ir_obj["size"]), end=' ')
                #print("%4d %4d %2d     " % (ir_obj["x"],ir_obj["y"],ir_obj["size"]))
                self.irX = ir_obj["x"]
                self.irY = ir_obj["y"]
                self.irS = ir_obj["size"]
        if self.wiimote.buttons["A"] and self.isAPressed == False:
            self.isAPressed = True
            self.irXVals = []
            self.irYVals = []
            self.irSVals = []
        if self.wiimote.buttons["A"] and self.isAPressed:
            self.isAPressed = True
            self.irXVals.append(self.irX)
            self.irYVals.append(self.irY)
            self.irSVals.append(self.irS)
            print(self.irXVals)
            print(self.irYVals)
            print(self.irSVals)
        else:
            self.isAPressed = False

        if(self.isAPressed):

            print("gestureRunning")
        else:
            self.irX = 0
            self.irY = 0
            self.irS = 0
            print("gestureNotRunning")

        x,y,z = self._acc_vals

        return {'accelX': np.array([x]), 'accelY': np.array([y]), 'accelZ': np.array([z]), 'irX': self.irX, 'irY': self.irY, 'irS': self.irS, 'a': self.isAPressed}

fclib.registerNodeType(WiimoteNode, [('Sensor',)])
    
if __name__ == '__main__':
    import sys
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

    wiimoteNode = fc.createNode('Wiimote', pos=(0, 0), )
    bufferNode = fc.createNode('Buffer', pos=(150, 0))

    fc.connectTerminals(wiimoteNode['irX'], bufferNode['dataIn'])
    fc.connectTerminals(bufferNode['dataOut'], pw1Node['In'])

    win.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
