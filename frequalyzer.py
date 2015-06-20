#!/usr/bin/env python3

import wiimote_node as wmn
import time
import sys

from wiimote_node import *



class FFTNode(Node):

    nodeName = "FFT"

    def __init__(self, name):
        """self.nSamples = nSamples    # Number of Sample must be a 2^n power
        self.aData = aData          # Amplitude data array
        self.sRate = sRate          # Sample Rate
        self.wFunction = wFunction  # Windowing Function
        self.zStart = zStart        # Start of Zoom Window if Used
        self.zStop = nSamples/2     # End of Zoom Window if Used
        # Instantiate a plot window within an existing pyQtGraph window.
        self.plot = win.addPlot(title="FFT")"""

        terminals = {
            'dataIn': dict(io='in'),
            'dataOutX': dict(io='out'),
            'dataOutY': dict(io='out'),
        }

        self.fftArray = np.array([])

        #push

        Node.__init__(self, name, terminals=terminals)

    def process(self, **kwds):
        # kwds will have one keyword argument per input terminal.

        self.fftArray = np.append(self.fftArray, kwds['dataIn'])

        n = len(self.fftArray)
        k = np.arange(n)

        x = np.fft.fft(self.fftArray)/n

        T = n/10

        frq = k/T

        amplitude = abs(x)

        # intFrq = fl(frq)
        #intAmp = int(amplitude)


        #self.pw1.plot(x = frq, y = amplitude, pen={'color': (200, 200, 100), 'width': 2})

        #self.pw1.setData(y=frq, x=amplitude)

        return {'dataOutX': frq, 'dataOutY': amplitude}


    """def update(self, fftArray):
        x = np.fft.fft(fftArray)
        amplitude = np.absolute(x)
        fScale = np.linspace(0 , 50000, self.nSamples)
        self.plot.plot(amplitude)
        # Calculate and set-up X axis
        self.plot.setXRange(SampleSize/2, 0)"""


fclib.registerNodeType(FFTNode, [('Data',)])

class Frequalyzer():
    def __init__(self):
        self.name = "Wiimote"
        if len(sys.argv) > 1:
            self.btaddr = sys.argv[1]
        app = QtGui.QApplication([])
        # create layout
        self.win = QtGui.QMainWindow()
        self.win.setWindowTitle('Wiimote Frequalyzer')
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
        self.createWidgets()
        self.wiimoteNode()
        self.bufferPlots()

        self.fftNode()
        self.plotCurveNode()

        self.win.show()
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    # create plotwidgets
    def createWidgets(self):
        """self.pw1 = pg.PlotWidget()
        self.layout.addWidget(self.pw1, 0, 1)
        self.pw1.setYRange(0, 1024)
        self.pw1Node = self.fc.createNode('PlotWidget', pos=(150, -150))
        self.pw1Node.setPlot(self.pw1)

        self.pw2 = pg.PlotWidget()
        self.layout.addWidget(self.pw2, 0, 2)
        self.pw2.setYRange(0, 1024)
        self.pw2Node = self.fc.createNode('PlotWidget', pos=(300, -150))
        self.pw2Node.setPlot(self.pw2)

        self.pw3 = pg.PlotWidget()
        self.layout.addWidget(self.pw3, 0, 3)
        self.pw3.setYRange(0, 1024)
        self.pw3Node = self.fc.createNode('PlotWidget', pos=(450, -150))
        self.pw3Node.setPlot(self.pw3)"""

        #self.pw1 = pg.PlotWidget(name='Plot1')
        #self.layout.addWidget(self.pw1, 0, 1)
        print ("test")
        #self.p1 = self.pw1.plot()
        #self.p1.setPen((200,200,100))
        #self.pw1Node = self.fc.createNode('PlotWidget', pos=(150, -150))
        #self.pw1Node.setPlot(self.p1)
        self.pwX = pg.PlotWidget()
        self.layout.addWidget(self.pwX, 0, 1)
        self.pwX.setYRange(0, 50)
        self.pwXNode = self.fc.createNode('PlotWidget', pos=(450, -150))
        self.pwXNode.setPlot(self.pwX)

        self.pwY = pg.PlotWidget()
        self.layout.addWidget(self.pwY, 0, 2)
        self.pwY.setYRange(0, 50)
        self.pwYNode = self.fc.createNode('PlotWidget', pos=(450, 0))
        self.pwYNode.setPlot(self.pwY)

        self.pwZ = pg.PlotWidget()
        self.layout.addWidget(self.pwZ, 0, 3)
        self.pwZ.setYRange(0, 50)
        self.pwZNode = self.fc.createNode('PlotWidget', pos=(450, 150))
        self.pwZNode.setPlot(self.pwZ)

    # create node for wiimote
    def wiimoteNode(self):
        self.wiimoteNode = self.fc.createNode('Wiimote', pos=(-150, 0), )
        self.wiimoteNode.text.setText(self.btaddr)
        self.wiimoteNode.btaddr = self.btaddr  # set wiimote bluetooth adress

        self.wiimoteNode.connect_wiimote()  # use module function to connect to wiimote

    # plot the buffers for the accelerometer data
    def bufferPlots(self):
        # buffers for x, y and z-Axis
        self.bufferNodeX = self.fc.createNode('Buffer', pos=(0, -150))
        self.bufferNodeY = self.fc.createNode('Buffer', pos=(0, 0))
        self.bufferNodeZ = self.fc.createNode('Buffer', pos=(0, 150))

        # connect buffers to the plots
        self.fc.connectTerminals(self.wiimoteNode['accelX'], self.bufferNodeX['dataIn'])
        self.fc.connectTerminals(self.wiimoteNode['accelY'], self.bufferNodeY['dataIn'])
        self.fc.connectTerminals(self.wiimoteNode['accelZ'], self.bufferNodeZ['dataIn'])

        # display buffer data in the plots
        #self.fc.connectTerminals(self.bufferNodeX['dataOut'], self.pw1Node['In'])
        #self.fc.connectTerminals(self.bufferNodeY['dataOut'], self.pw2Node['In'])
        #self.fc.connectTerminals(self.bufferNodeZ['dataOut'], self.pw3Node['In'])

    def fftNode(self):
        self.fftNodeX = self.fc.createNode('FFT', pos=(150, -150), )
        self.fftNodeY = self.fc.createNode('FFT', pos=(150, 0), )
        self.fftNodeZ = self.fc.createNode('FFT', pos=(150, 150), )
        self.fc.connectTerminals(self.bufferNodeX['dataOut'], self.fftNodeX['dataIn'])
        self.fc.connectTerminals(self.bufferNodeY['dataOut'], self.fftNodeY['dataIn'])
        self.fc.connectTerminals(self.bufferNodeZ['dataOut'], self.fftNodeZ['dataIn'])



        #self.fc.connectTerminals(self.fftNode['dataOutX'], self.pw1Node['In'])
        #self.fc.connectTerminals(self.fftNode['dataOutY'], self.pw1Node['In'])

    def plotCurveNode(self):
        # create PlotCurves and connect to fftNode outputs
        self.plotCurveX = self.fc.createNode('PlotCurve', pos=(300, -150), )
        self.fc.connectTerminals(self.fftNodeX['dataOutX'], self.plotCurveX['x'])
        self.fc.connectTerminals(self.fftNodeX['dataOutY'], self.plotCurveX['y'])

        self.plotCurveY = self.fc.createNode('PlotCurve', pos=(300, 0), )
        self.fc.connectTerminals(self.fftNodeY['dataOutX'], self.plotCurveY['x'])
        self.fc.connectTerminals(self.fftNodeY['dataOutY'], self.plotCurveY['y'])

        self.plotCurveZ = self.fc.createNode('PlotCurve', pos=(300, 150), )
        self.fc.connectTerminals(self.fftNodeZ['dataOutX'], self.plotCurveZ['x'])
        self.fc.connectTerminals(self.fftNodeZ['dataOutY'], self.plotCurveZ['y'])

        # connect plotcurves to their widgets
        self.fc.connectTerminals(self.plotCurveX['plot'], self.pwXNode['In'])
        self.fc.connectTerminals(self.plotCurveY['plot'], self.pwYNode['In'])
        self.fc.connectTerminals(self.plotCurveZ['plot'], self.pwZNode['In'])

if __name__ == '__main__':
    f = Frequalyzer()



