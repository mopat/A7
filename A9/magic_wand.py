#!/usr/bin/env python3

import time
import sys
import svmutil


from wiimote_node_extended import *
from pymouse import PyMouse
from dollar import Recognizer
from pyqtgraph.GraphicsScene import GraphicsScene

circlePoints = [(269, 84), (263, 86), (257, 92), (253, 98), (249, 104), (245, 114), (243, 122), (239, 132), (237, 142), (235, 152), (235, 162), (235, 172), (235, 180), (239, 190), (245, 198), (251, 206), (259, 212), (267, 216), (275, 218), (281, 222), (287, 224), (295, 224), (301, 226), (311, 226), (319, 226), (329, 226), (339, 226), (349, 226), (352, 226), (360, 226), (362, 225), (366, 219), (367, 217), (367, 209), (367, 206), (367, 198), (367, 190), (367, 182), (367, 174), (365, 166), (363, 158), (359, 152), (355, 146), (353, 138), (349, 134), (345, 130), (341, 124), (340, 122), (338, 121), (337, 119), (336, 117), (334, 116), (332, 115), (331, 114), (327, 110), (325, 109), (323, 109), (321, 108), (320, 108), (318, 107), (316, 107), (315, 107), (314, 107), (313, 107), (312, 107), (311, 107), (310, 107), (309, 106), (308, 106), (307, 105), (306, 105), (305, 105), (304, 105), (303, 104), (302, 104), (301, 104), (300, 104), (299, 103), (298, 103), (296, 102), (295, 101), (293, 101), (292, 100), (291, 100), (290, 100), (289, 100), (288, 100), (288, 99), (287, 99), (287, 99)]



class RecognizerNode(Node):
    nodeName = "Recognizer"

    def __init__(self, name):
        terminals = {
            #'IrX': dict(io='in'),
            #'IrY': dict(io='in'),
            'tupelIn': dict(io='in'),
            'onePressed': dict(io='in')
        }

        self.recognizer = Recognizer()
        self.recognizer.addTemplate('circle', circlePoints)
        self.positions = []

        self.last_name = None
        self.last_accuracy = 0.0

        self.win2 = pg.GraphicsView()
        #self.win2.setGeometry(300, 300, 350, 100)
        self.vb = pg.ViewBox()
        self.win2.setCentralItem(self.vb)

        self.win2.show()

        #self.paintWidget = QtGui.QWidget()
        #self.paintWidget.setGeometry(800, 600, 800, 600)
        #self.paintWidget.setWindowTitle('Paint Widget')
        #self.paintWidget.show()



        Node.__init__(self, name, terminals=terminals)

    def process(self, **kwds):
        if kwds['onePressed']:
                #x = kwds['IrX']
                #y = kwds['IrY']
                tupel = kwds['tupelIn']
                self.positions = tupel

                points = [(p[0], p[1]) for p in self.positions]
                if len(points) > 10:
                    (name, score) = self.recognizer.recognize(points)
                    self.last_name = name
                    self.last_accuracy = score

                    self.printGesture()
                else:
                    self.last_name = '(Not enough points - try again!)'
                    self.last_accuracy = 0.0
                    print (self.last_name)

    def printGesture(self):
        print(self.last_name)
        print(self.last_accuracy)

        self.paintEvent()

    def paintEvent(self):
        print("painting")

        obj = Obj()
        self.vb.addItem(obj)



fclib.registerNodeType(RecognizerNode, [('Data',)])

class PointerNode(Node):
    nodeName = "Pointer"

    def __init__(self, name):
        terminals = {
            'irXIn': dict(io='in'),
            'irYIn': dict(io='in'),
            'bPressed': dict(io='in'),
            'aPressed': dict(io='in'),
        }

        self.mouse = PyMouse()
        self.screenSize = self.mouse.screen_size()
        self.dragging = False

        Node.__init__(self, name, terminals=terminals)

    def process(self, **kwds):
        self.irX = kwds['irXIn']
        self.irY = kwds['irYIn']
        self.isBPressed = kwds['bPressed']
        self.isAPressed = kwds['aPressed']

        if self.isBPressed and self.irX != 0 and self.irY != 0:

            xScreen = self.screenSize[0] - int((self.screenSize[0] / 1024) * self.irX)
            yScreen = int((self.screenSize[1] / 760) * self.irY)

            if xScreen <= self.screenSize[0] and xScreen >= 0 and yScreen <= self.screenSize[1] and yScreen >= 0:
                self.mouse.move(xScreen, yScreen)

        if self.isAPressed and self.isBPressed == False:
            xMousePos = self.mouse.position()[0]
            yMousePos = self.mouse.position()[1]
            self.mouse.click(xMousePos, yMousePos)
        elif self.isAPressed and self.isBPressed:
            self.mouse.press(self.mouse.position()[0], self.mouse.position()[1])


fclib.registerNodeType(PointerNode, [('Data',)])

class Obj(QtGui.QGraphicsObject):
    def __init__(self):
        QtGui.QGraphicsObject.__init__(self)
        GraphicsScene.registerObject(self)

    def paint(self, p, *args):
        #p.setPen(pg.mkPen(200,200,200))
        p.setBrush(QtGui.QColor(200, 0, 0))
        #p.setBackground(QtCore.Qt.red)
        p.drawEllipse(self.boundingRect())

    def boundingRect(self):
        newRect = QtCore.QRectF(10, 15, 50, 40)

        return newRect



    def mouseClickEvent(self, ev):
        if ev.double():
            print("double click")
        else:
            print("click")
        ev.accept()

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



        #obj2 = Obj()
        #win.addItem(obj2)

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
        self.createWidgets()
        self.bufferPlots()

        self.recognizerNode()
        self.pointerNode()

        self.win.show()

        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    # create plotwidgets
    def createWidgets(self):
        self.pw1 = pg.PlotWidget()
        self.layout.addWidget(self.pw1, 0, 1)
        self.pw1.setYRange(0, 1024)
        self.pw1Node = self.fc.createNode('PlotWidget', pos=(150, -150))
        self.pw1.setBackground('w')
        self.pw1Node.setPlot(self.pw1)

        self.pw2 = pg.PlotWidget()
        self.layout.addWidget(self.pw2, 0, 2)
        self.pw2.setYRange(0, 1024)
        self.pw2Node = self.fc.createNode('PlotWidget', pos=(300, -150))
        self.pw2Node.setPlot(self.pw2)


        #l = pg.GraphicsLayout(border=(100,100,100))

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
        self.bufferNodeY = self.fc.createNode('Buffer', pos=(300, 0))

        self.plotCurve = self.fc.createNode('PlotCurve', pos=(300, 0))

        self.fc.connectTerminals(self.wiimoteNode['irX'], self.bufferNodeX['dataIn'])
        self.fc.connectTerminals(self.wiimoteNode['irY'], self.bufferNodeY['dataIn'])

        # display buffer data in the plots
        self.fc.connectTerminals(self.bufferNodeX['dataOut'], self.plotCurve['x'])
        self.fc.connectTerminals(self.bufferNodeY['dataOut'], self.plotCurve['y'])


        self.fc.connectTerminals(self.plotCurve['plot'], self.pw1Node['In'])

    def recognizerNode(self):
        self.recognizer = self.fc.createNode('Recognizer', pos=(400, 0))

        #self.fc.connectTerminals(self.bufferNodeX['dataOut'], self.recognizer['IrX'])
        #self.fc.connectTerminals(self.bufferNodeY['dataOut'], self.recognizer['IrY'])
        self.fc.connectTerminals(self.wiimoteNode['irXirYTup'], self.recognizer['tupelIn'])
        self.fc.connectTerminals(self.wiimoteNode['oneRel'], self.recognizer['onePressed'])



    def pointerNode(self):
        self.pointerNode = self.fc.createNode('Pointer', pos=(400, 0))

        self.fc.connectTerminals(self.wiimoteNode['irX'], self.pointerNode['irXIn'])
        self.fc.connectTerminals(self.wiimoteNode['irY'], self.pointerNode['irYIn'])
        self.fc.connectTerminals(self.wiimoteNode['b'], self.pointerNode['bPressed'])
        self.fc.connectTerminals(self.wiimoteNode['a'], self.pointerNode['aPressed'])
if __name__ == '__main__':
    an = Analyze()
