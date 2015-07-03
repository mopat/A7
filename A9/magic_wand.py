#!/usr/bin/env python3

import time
import sys
import svmutil
import random


from wiimote_node_extended import *
from pymouse import PyMouse
from dollar import Recognizer
from pyqtgraph.GraphicsScene import GraphicsScene

circlePoints = [(269, 84), (263, 86), (257, 92), (253, 98), (249, 104), (245, 114), (243, 122), (239, 132), (237, 142), (235, 152), (235, 162), (235, 172), (235, 180), (239, 190), (245, 198), (251, 206), (259, 212), (267, 216), (275, 218), (281, 222), (287, 224), (295, 224), (301, 226), (311, 226), (319, 226), (329, 226), (339, 226), (349, 226), (352, 226), (360, 226), (362, 225), (366, 219), (367, 217), (367, 209), (367, 206), (367, 198), (367, 190), (367, 182), (367, 174), (365, 166), (363, 158), (359, 152), (355, 146), (353, 138), (349, 134), (345, 130), (341, 124), (340, 122), (338, 121), (337, 119), (336, 117), (334, 116), (332, 115), (331, 114), (327, 110), (325, 109), (323, 109), (321, 108), (320, 108), (318, 107), (316, 107), (315, 107), (314, 107), (313, 107), (312, 107), (311, 107), (310, 107), (309, 106), (308, 106), (307, 105), (306, 105), (305, 105), (304, 105), (303, 104), (302, 104), (301, 104), (300, 104), (299, 103), (298, 103), (296, 102), (295, 101), (293, 101), (292, 100), (291, 100), (290, 100), (289, 100), (288, 100), (288, 99), (287, 99), (287, 99)]
squarePoints = [(193, 123), (193, 131), (193, 139), (195, 151), (197, 161), (199, 175), (201, 187), (205, 201), (207, 213), (209, 225), (213, 235), (213, 243), (215, 251), (215, 254), (217, 262), (217, 264), (217, 266), (217, 267), (218, 267), (219, 267), (221, 267), (224, 267), (227, 267), (237, 267), (247, 265), (259, 263), (273, 261), (287, 261), (303, 259), (317, 257), (331, 255), (347, 255), (361, 253), (375, 253), (385, 253), (395, 251), (403, 249), (406, 249), (408, 249), (408, 248), (409, 248), (409, 246), (409, 245), (409, 242), (409, 234), (409, 226), (409, 216), (407, 204), (407, 194), (405, 182), (403, 172), (403, 160), (401, 150), (399, 140), (399, 130), (397, 122), (397, 119), (397, 116), (396, 114), (396, 112), (396, 111), (396, 110), (396, 109), (396, 108), (396, 107), (396, 106), (396, 105), (394, 105), (392, 105), (384, 105), (376, 105), (364, 105), (350, 107), (334, 109), (318, 111), (306, 113), (294, 115), (286, 117), (278, 117), (272, 119), (269, 119), (263, 121), (260, 121), (254, 123), (251, 123), (245, 125), (243, 125), (242, 125), (241, 126), (240, 126), (238, 127), (236, 127), (232, 128), (231, 128), (231, 129), (230, 129), (228, 129), (227, 129), (226, 129), (225, 129), (224, 129), (223, 129), (222, 129), (221, 130), (221, 130)]
trianglePoints = [(282, 83), (281, 85), (277, 91), (273, 97), (267, 105), (261, 113), (253, 123), (243, 133), (235, 141), (229, 149), (221, 153), (217, 159), (216, 160), (215, 161), (214, 162), (216, 162), (218, 162), (221, 162), (227, 164), (233, 166), (241, 166), (249, 166), (259, 166), (271, 166), (283, 166), (297, 166), (309, 164), (323, 164), (335, 162), (345, 162), (353, 162), (361, 160), (363, 159), (365, 159), (366, 158), (367, 158), (368, 157), (369, 157), (370, 156), (371, 156), (371, 155), (372, 155), (372, 153), (372, 152), (372, 151), (372, 149), (372, 147), (371, 145), (367, 141), (363, 137), (359, 133), (353, 129), (349, 125), (343, 121), (337, 119), (333, 115), (327, 111), (325, 110), (324, 109), (320, 105), (318, 104), (314, 100), (312, 99), (310, 98), (306, 94), (305, 93), (303, 92), (301, 91), (300, 90), (298, 89), (297, 88), (296, 88), (295, 87), (294, 87), (293, 87), (293, 87)]


class RecognizerNode(Node):
    nodeName = "Recognizer"

    def __init__(self, name):
        terminals = {
            'irX': dict(io='in'),
            'irY': dict(io='in'),
            'tupelIn': dict(io='in'),
            'onePressed': dict(io='in')
        }

        self.recognizer = Recognizer()
        self.recognizer.addTemplate('circle', circlePoints)
        self.recognizer.addTemplate('square', squarePoints)
        self.recognizer.addTemplate('triangle', trianglePoints)
        self.positions = []

        self.last_name = None
        self.last_accuracy = 0.0

        self.win2 = pg.GraphicsView()
        #self.win2.setGeometry(300, 300, 350, 100)

        self.win2.setBackgroundBrush(QtGui.QColor(255, 255, 255))
        self.win2.setWindowTitle('Paint Widget')
        self.win2.setGeometry(1200, 1000, 1200, 1000)

        self.vb = pg.ViewBox()

        self.win2.setCentralItem(self.vb)
        self.oneRel = False
        self.win2.show()
        self.count = 0

        # counter to prevent multiple execution when one button is released, because for each terminal input code is executed -> now every 4th step it will be executed
        self.exCount = 0


        Node.__init__(self, name, terminals=terminals)


    def process(self, **kwds):
        self.oneRel = kwds['onePressed']

        if(self.oneRel and self.exCount == 4):
            self.exCount = 0
        if self.oneRel:
                tupel = kwds['tupelIn']


                if self.exCount == 0:
                    self.positions = self.resample(tupel)
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
                self.exCount += 1


    def printGesture(self):
        print(self.last_name)
        print(self.last_accuracy)

        if self.last_accuracy > 0.4:
            if self.last_name == 'circle':
                self.paintCircle()
            elif self.last_name == 'square':
                self.paintRect()
            elif self.last_name == 'triangle':
                self.paintTriangle()
        else:
            print ("Gesture accuracy was too low, try again please")


    def paintCircle(self):
        # random pos
        xPos = random.randint(0, 1200)
        yPos = random.randint(0, 1000)
        ellipse = QtGui.QGraphicsEllipseItem(QtCore.QRectF(xPos, yPos, 50, 50))

        ellipse.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)

        # random colors
        rc = self.randomColor()
        ellipse.setBrush(QtGui.QColor(rc[0], rc[1], rc[2]))

        self.vb.addItem(ellipse)

    def paintRect(self):
        # random pos
        xPos = random.randint(0, 1200)
        yPos = random.randint(0, 1000)
        rect = QtGui.QGraphicsRectItem(QtCore.QRectF(xPos, yPos, 50, 50))

        rect.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        # random colors
        rc = self.randomColor()
        rect.setBrush(QtGui.QColor(rc[0], rc[1], rc[2]))

        self.vb.addItem(rect)

    def paintTriangle(self):
        # random pos
        print ("painting triangle")
        xPos = random.randint(0, 1200)
        yPos = random.randint(0, 1000)

        self.polygon = QtGui.QPolygonF([
                    QtCore.QPointF(-50, 0), QtCore.QPointF(0, 50),
                    QtCore.QPointF(50, 0)])
        self.polygon.translate(xPos, yPos)

        triangle = QtGui.QGraphicsPolygonItem(self.polygon)

        triangle.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        # random colors
        rc = self.randomColor()
        triangle.setBrush(QtGui.QColor(rc[0], rc[1], rc[2]))

        self.vb.addItem(triangle)

    def resample(self, point_list,step_count=64):
        newpoints = []
        length = len(point_list)
        stepsize = length/step_count
        curpos = 0
        newpoints.append(point_list[0])
        i = 1
        while i < len(point_list):

            p1 = point_list[i-1]

            d = self.distance(p1,point_list[i])

            if curpos+d >= stepsize:
                nx = p1[0] + ((stepsize-curpos)/d)*(point_list[i][0]-p1[0])
                ny = p1[1] + ((stepsize-curpos)/d)*(point_list[i][1]-p1[1])
                newpoints.append([nx,ny])
                point_list.insert(i,[nx,ny])
                curpos = 0
            else:
                curpos += d
            i += 1
        return newpoints

    def distance(self, p1, p2):
        d = p2[0] - p1[0]
        if(d < 0):
            d *= -1

        return d

    def randomColor(self):
        return [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
fclib.registerNodeType(RecognizerNode, [('Data',)])

class PointerNode(Node):
    nodeName = "Pointer"

    def __init__(self, name):
        terminals = {
            'irXIn': dict(io='in'),
            'irYIn': dict(io='in'),
            'bPressed': dict(io='in'),
            'aPressed': dict(io='in'),
            'bRel': dict(io='in'),
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
        self.isBReleased = kwds['bRel']

        if self.isBPressed and self.irX != 0 and self.irY != 0:
            xScreen = self.screenSize[0] - int((self.screenSize[0] / 1024) * self.irX)
            yScreen = int((self.screenSize[1] / 760) * self.irY)

            if xScreen <= self.screenSize[0] and xScreen >= 0 and yScreen <= self.screenSize[1] and yScreen >= 0:
                self.mouse.move(xScreen, yScreen)

        # when b is released and object is dragged, object is released
        if self.isBReleased and self.dragging == True:
            self.mouse.click(self.mouse.position()[0], self.mouse.position()[1])
            self.dragging = False
        # when b is not pressed and a is pressed, do a single click
        if self.isAPressed and self.isBPressed == False:
            self.mouse.click(self.mouse.position()[0], self.mouse.position()[1])
            self.dragging = False
        # when b and a are pressed, do drag
        elif self.isAPressed and self.isBPressed:
            self.mouse.press(self.mouse.position()[0], self.mouse.position()[1])
            self.dragging = True


fclib.registerNodeType(PointerNode, [('Data',)])

class MagicWand():
    def __init__(self):
        self.name = "Wiimote"
        if len(sys.argv) > 1:
            self.btaddr = sys.argv[1]
        app = QtGui.QApplication([])
        # create layout
        self.win = QtGui.QMainWindow()
        self.win.setWindowTitle('Wiimote MagicWand')
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
        self.pw1.setBackground('w')
        self.pw1Node = self.fc.createNode('PlotWidget', pos=(450, 150))
        self.pw1Node.setPlot(self.pw1)

        self.pw2 = pg.PlotWidget()
        self.layout.addWidget(self.pw2, 0, 2)
        self.pw2.setYRange(0, 1024)
        self.pw2Node = self.fc.createNode('PlotWidget', pos=(300, 0))
        self.pw2.setBackground('w')
        self.pw2Node.setPlot(self.pw2)

        self.pw3 = pg.PlotWidget()
        self.layout.addWidget(self.pw3, 0, 3)
        self.pw3.setYRange(0, 1024)
        self.pw3Node = self.fc.createNode('PlotWidget', pos=(300, 300))
        self.pw3Node.setPlot(self.pw3)
        self.pw3.setBackground('w')

    # create node for wiimote
    def wiimoteNode(self):
        self.wiimoteNode = self.fc.createNode('Wiimote', pos=(0, 0), )
        self.wiimoteNode.text.setText(self.btaddr)
        self.wiimoteNode.btaddr = self.btaddr  # set wiimote bluetooth adress

        self.wiimoteNode.connect_wiimote()  # use module function to connect to wiimote

    # plot the buffers for the accelerometer data
    def bufferPlots(self):
        # buffers for x, y and z-Axis
        self.bufferNodeX = self.fc.createNode('Buffer', pos=(150, 150))
        self.bufferNodeY = self.fc.createNode('Buffer', pos=(150, 300))

        self.plotCurve = self.fc.createNode('PlotCurve', pos=(300, 150))

        self.fc.connectTerminals(self.wiimoteNode['irX'], self.bufferNodeX['dataIn'])
        self.fc.connectTerminals(self.wiimoteNode['irY'], self.bufferNodeY['dataIn'])

        # display buffer x y data as plotcourve
        self.fc.connectTerminals(self.bufferNodeX['dataOut'], self.plotCurve['x'])
        self.fc.connectTerminals(self.bufferNodeY['dataOut'], self.plotCurve['y'])

        # display buffer x y data as curves
        self.fc.connectTerminals(self.bufferNodeX['dataOut'], self.pw2Node['In'])
        self.fc.connectTerminals(self.bufferNodeY['dataOut'], self.pw3Node['In'])

        self.fc.connectTerminals(self.plotCurve['plot'], self.pw1Node['In'])

    def recognizerNode(self):
        self.recognizer = self.fc.createNode('Recognizer', pos=(150, -150))

        self.fc.connectTerminals(self.wiimoteNode['irX'], self.recognizer['irX'])
        self.fc.connectTerminals(self.wiimoteNode['irY'], self.recognizer['irY'])
        self.fc.connectTerminals(self.wiimoteNode['irXirYTup'], self.recognizer['tupelIn'])
        self.fc.connectTerminals(self.wiimoteNode['oneRel'], self.recognizer['onePressed'])


    def pointerNode(self):
        self.pointerNode = self.fc.createNode('Pointer', pos=(150, 0))

        self.fc.connectTerminals(self.wiimoteNode['irX'], self.pointerNode['irXIn'])
        self.fc.connectTerminals(self.wiimoteNode['irY'], self.pointerNode['irYIn'])
        self.fc.connectTerminals(self.wiimoteNode['b'], self.pointerNode['bPressed'])
        self.fc.connectTerminals(self.wiimoteNode['bRel'], self.pointerNode['bRel'])
        self.fc.connectTerminals(self.wiimoteNode['a'], self.pointerNode['aPressed'])
if __name__ == '__main__':
    mw = MagicWand()
