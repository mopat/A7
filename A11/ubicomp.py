import cv2
import sys
import numpy as np
import math
import time
from threading import Timer
import uinput
from sniff_x import Sniffer


class UbiComp():
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.cascPath = sys.argv[1]
        self.faceCascade = cv2.CascadeClassifier(self.cascPath)

        self.device = uinput.Device([
            uinput.KEY_SPACE,
            uinput.KEY_LEFTCTRL,
            uinput.KEY_UP,
            uinput.KEY_DOWN
        ])

        self.VLC_KEY = "VLC media player"

        self.sn = Sniffer()

        while True:
            print(self.getCurrentWindow())
            if str(self.getCurrentWindow()).endswith(self.VLC_KEY):
                self.faceDetector()
                self.gestureRecognizer()
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                k = cv2.waitKey(10)
                if k == 27:
                    break
        self.print_some_times()


    def faceDetector(self):
        # Capture frame-by-frame
        ret, frame = self.video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )


        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            #if len(faces) >= 2:
                #print (str(len(faces)) + " faces detected")
        # Display the resulting frame
        cv2.imshow('Video', frame)



        # When everything is done, release the capture


    def gestureRecognizer(self):
        ret, img = self.video_capture.read()
        cv2.rectangle(img,(300,300),(100,100),(0,255,0),0)
        crop_img = img[100:300, 100:300]
        grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        value = (35, 35)
        blurred = cv2.GaussianBlur(grey, value, 0)
        _, thresh1 = cv2.threshold(blurred, 127, 255,
                                   cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        cv2.imshow('Thresholded', thresh1)
        contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
                cv2.CHAIN_APPROX_NONE)
        max_area = -1
        for i in range(len(contours)):
            cnt=contours[i]
            area = cv2.contourArea(cnt)
            if(area>max_area):
                max_area=area
                ci=i
        cnt=contours[ci]
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0)
        hull = cv2.convexHull(cnt)
        drawing = np.zeros(crop_img.shape,np.uint8)
        cv2.drawContours(drawing,[cnt],0,(0,255,0),0)
        cv2.drawContours(drawing,[hull],0,(0,0,255),0)
        hull = cv2.convexHull(cnt,returnPoints = False)
        defects = cv2.convexityDefects(cnt,hull)
        count_defects = 0
        cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
            if angle <= 90:
                count_defects += 1
                cv2.circle(crop_img,far,1,[0,0,255],-1)
            #dist = cv2.pointPolygonTest(cnt,far,True)
            cv2.line(crop_img,start,end,[0,255,0],2)
            #cv2.circle(crop_img,far,5,[0,0,255],-1)
        if count_defects == 1:
            cv2.putText(img,"Volume Down", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            self.device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_DOWN])
        elif count_defects == 2:
            str = "Volume Up"
            print str
            cv2.putText(img, str, (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            self.device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_UP])
        elif count_defects == 3:
            cv2.putText(img,"Play/Pause", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            #self.device.emit_click(uinput.KEY_L)
            self.device.emit_click(uinput.KEY_SPACE)
        elif count_defects == 4:
            cv2.putText(img,"Play/Pause", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            self.device.emit_click(uinput.KEY_SPACE)
        else:
            cv2.putText(img,"Hello World!!!", (50,50),\
                        cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        #cv2.imshow('drawing', drawing)
        #cv2.imshow('end', crop_img)
        cv2.imshow('Gesture', img)
        all_img = np.hstack((drawing, crop_img))
        cv2.imshow('Contours', all_img)

    def getCurrentWindow(self):
        return Sniffer.get_cur_window(Sniffer())[2]


if __name__ == '__main__':
    uc = UbiComp()