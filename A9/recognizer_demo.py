#!/usr/bin/env python
#
# Simple demo of the $1 gesture recognizer.
# Requires WxPython.
#

import wx
from dollar import Recognizer

# Raw points for the three example gestures.
circlePoints = [(269, 84), (263, 86), (257, 92), (253, 98), (249, 104), (245, 114), (243, 122), (239, 132), (237, 142), (235, 152), (235, 162), (235, 172), (235, 180), (239, 190), (245, 198), (251, 206), (259, 212), (267, 216), (275, 218), (281, 222), (287, 224), (295, 224), (301, 226), (311, 226), (319, 226), (329, 226), (339, 226), (349, 226), (352, 226), (360, 226), (362, 225), (366, 219), (367, 217), (367, 209), (367, 206), (367, 198), (367, 190), (367, 182), (367, 174), (365, 166), (363, 158), (359, 152), (355, 146), (353, 138), (349, 134), (345, 130), (341, 124), (340, 122), (338, 121), (337, 119), (336, 117), (334, 116), (332, 115), (331, 114), (327, 110), (325, 109), (323, 109), (321, 108), (320, 108), (318, 107), (316, 107), (315, 107), (314, 107), (313, 107), (312, 107), (311, 107), (310, 107), (309, 106), (308, 106), (307, 105), (306, 105), (305, 105), (304, 105), (303, 104), (302, 104), (301, 104), (300, 104), (299, 103), (298, 103), (296, 102), (295, 101), (293, 101), (292, 100), (291, 100), (290, 100), (289, 100), (288, 100), (288, 99), (287, 99), (287, 99)]
squarePoints = [(193, 123), (193, 131), (193, 139), (195, 151), (197, 161), (199, 175), (201, 187), (205, 201), (207, 213), (209, 225), (213, 235), (213, 243), (215, 251), (215, 254), (217, 262), (217, 264), (217, 266), (217, 267), (218, 267), (219, 267), (221, 267), (224, 267), (227, 267), (237, 267), (247, 265), (259, 263), (273, 261), (287, 261), (303, 259), (317, 257), (331, 255), (347, 255), (361, 253), (375, 253), (385, 253), (395, 251), (403, 249), (406, 249), (408, 249), (408, 248), (409, 248), (409, 246), (409, 245), (409, 242), (409, 234), (409, 226), (409, 216), (407, 204), (407, 194), (405, 182), (403, 172), (403, 160), (401, 150), (399, 140), (399, 130), (397, 122), (397, 119), (397, 116), (396, 114), (396, 112), (396, 111), (396, 110), (396, 109), (396, 108), (396, 107), (396, 106), (396, 105), (394, 105), (392, 105), (384, 105), (376, 105), (364, 105), (350, 107), (334, 109), (318, 111), (306, 113), (294, 115), (286, 117), (278, 117), (272, 119), (269, 119), (263, 121), (260, 121), (254, 123), (251, 123), (245, 125), (243, 125), (242, 125), (241, 126), (240, 126), (238, 127), (236, 127), (232, 128), (231, 128), (231, 129), (230, 129), (228, 129), (227, 129), (226, 129), (225, 129), (224, 129), (223, 129), (222, 129), (221, 130), (221, 130)]
trianglePoints = [(282, 83), (281, 85), (277, 91), (273, 97), (267, 105), (261, 113), (253, 123), (243, 133), (235, 141), (229, 149), (221, 153), (217, 159), (216, 160), (215, 161), (214, 162), (216, 162), (218, 162), (221, 162), (227, 164), (233, 166), (241, 166), (249, 166), (259, 166), (271, 166), (283, 166), (297, 166), (309, 164), (323, 164), (335, 162), (345, 162), (353, 162), (361, 160), (363, 159), (365, 159), (366, 158), (367, 158), (368, 157), (369, 157), (370, 156), (371, 156), (371, 155), (372, 155), (372, 153), (372, 152), (372, 151), (372, 149), (372, 147), (371, 145), (367, 141), (363, 137), (359, 133), (353, 129), (349, 125), (343, 121), (337, 119), (333, 115), (327, 111), (325, 110), (324, 109), (320, 105), (318, 104), (314, 100), (312, 99), (310, 98), (306, 94), (305, 93), (303, 92), (301, 91), (300, 90), (298, 89), (297, 88), (296, 88), (295, 87), (294, 87), (293, 87), (293, 87)]

class RecognizerDemoWindow(wx.Frame):
   def __init__(self, parent, id, title, width, height):
      self.frame = wx.Frame.__init__(self, parent, id, title, size = wx.Size(width, height))
      self.SetMinSize((width, height))
      self.SetMaxSize((width, height))

      self.Bind(wx.EVT_PAINT, self.OnPaint)
      self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
      self.Bind(wx.EVT_MOTION, self.OnMouseMove)
      self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)

      self.mouseDown = False
      self.positions = []

      self.recognizer = Recognizer()
      self.recognizer.addTemplate('circle', circlePoints)
      self.recognizer.addTemplate('square', squarePoints)
      self.recognizer.addTemplate('triangle', trianglePoints)

      self.last_name = None
      self.last_accuracy = 0.0

   def OnPaint(self, event):
      dc = wx.BufferedPaintDC(self)
      dc.Clear()
      for position in self.positions:
         (x, y, type) = position

         if type == "start":
            r = 10
         elif type == "stop":
            r = 1

            points = [(p[0], p[1]) for p in self.positions]
            if len(points) > 10:
               (name, score) = self.recognizer.recognize(points)
               self.last_name = name
               self.last_accuracy = score
            else:
               self.last_name = '(Not enough points - try again!)'
               self.last_accuracy = 0.0
         else:
            r = 3

         dc.DrawCircle(x, y, r)

      dc.DrawText("$1 gesture recognizer demo", 10, 10)
      dc.DrawText("Gestures: circle, square, triangle", 20, 30)

      dc.DrawText("Last drawn gesture: %s" % self.last_name, 20, 60)
      dc.DrawText("Gesture accuracy: %2.2f%%" % (self.last_accuracy * 100), 20, 80)

   def OnMouseDown(self, event):
      self.mouseDown = True
      (x, y) = event.GetPosition()
      self.positions = [(x, y, 'start')]
      self.OnPaint(None)

   def OnMouseMove(self, event):
      if self.mouseDown:
         (x, y) = event.GetPosition()
         self.positions.append((x, y, 'move'))
         self.OnPaint(None)

   def OnMouseUp(self, event):
      self.mouseDown = False
      (x, y) = event.GetPosition()
      self.positions.append((x, y, 'stop'))
      self.OnPaint(None)

class RecognizerDemo(wx.App):
   def OnInit(self):
      self.frame = RecognizerDemoWindow(None, -1, "$1 gesture recognizer demo", 600, 400)
      self.frame.Show(True)
      self.SetTopWindow(self.frame)
      return True

demo = RecognizerDemo()
demo.MainLoop()