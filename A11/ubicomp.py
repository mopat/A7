import cv2
import sys
import numpy as np
import math
import time
import uinput
import speech_recognition as sr
from sniff_x import Sniffer
from Tkinter import *
from thread import start_new_thread


class UbiComp():
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.cascPath = "haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascPath)
        self.playPauseTimer = False
        self.isZero = False
        self.timerRunning = False
        self.device = uinput.Device([
            uinput.KEY_SPACE,
            uinput.KEY_LEFTCTRL,
            uinput.KEY_UP,
            uinput.KEY_DOWN
        ])

        self.VLC_KEY = "VLC media player"
        self.infoTextBox()

        #start_new_thread(self.speechRecognition, (2,))
        #self.sn = Sniffer()
        while True:

            if str(self.getCurrentWindow()).endswith(self.VLC_KEY):
                #self.faceDetector()
            #if self.playPauseTimer == False:
                self.gestureRecognizer()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            k = cv2.waitKey(10)
            if k == 27:
                break

            time.sleep(0.05)

    def speechRecognition(self, i):
        while True:
            r = sr.Recognizer()
            with sr.Microphone() as source:                # use the default microphone as the audio source
                audio = r.listen(source)                   # listen for the first phrase and extract it into audio data

            try:
                voice = r.recognize(audio)
                if voice == "play" or voice == "stop":
                    self.device.emit_click(uinput.KEY_SPACE)
                elif voice == "volume up":
                    for i in range(5):
                        self.device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_UP])
                elif voice == "volume down":
                    for i in range(5):
                        self.device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_DOWN])
                print("You said: " + voice)    # recognize speech using Google Speech Recognition
            except LookupError:                            # speech is unintelligible
                print("Could not understand audio")

    def stopwatch(self, seconds):
        if self.timerRunning == True:
            start = time.time()
            time.clock()
            elapsed = 0
            while elapsed < seconds:
                elapsed = time.time() - start
                #print "loop cycle time: %f, seconds count: %02d" % (time.clock() , elapsed)
            if elapsed == seconds:
                print "Pause"
                self.isZero = False
                self.timerRunning = False
                self.pauseVideo(2)


    def infoTextBox(self):
        root = Tk()
        root.title("Instructions")
        T = Text(root, height=20, width=150)
        T.pack()
        T.insert(END, "VLC CONTROLLER\nStep 1: Open VLC Media Player\nStep 2: Use rectangle box to detect hand gestures\n1 Finger: ...\nClose Instructions to start")
        mainloop()

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

        if len(faces) == 0 & self.isZero == False:
            if self.playPauseTimer == False:
                self.isZero = True
                self.timerRunning = True
                self.stopwatch(3)

        if len(faces) > 0:
            self.timerRunning = False
            if self.playPauseTimer == True:
                self.startVideo(2)

        # Display the resulting frame
        #cv2.imshow('Video', frame)

        # When everything is done, release the capture


    def gestureRecognizer(self):
        ret, img = self.video_capture.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30), 
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )


        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #if len(faces) >= 2:
            #print (str(len(faces)) + " faces detected")

        if len(faces) == 0 & self.isZero == False:
            if self.playPauseTimer == False:
                self.isZero = True
                self.timerRunning = True
                self.stopwatch(3)

        if len(faces) > 0:
            self.timerRunning = False
            if self.playPauseTimer == True:
                self.startVideo(2)

        # Display the resulting frame

        # When everything is done, release the capture
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
            cv2.putText(img, "Volume Up", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            self.device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_UP])
        elif count_defects == 3:
            cv2.putText(img,"Play/Pause", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            self.pauseAndStartVideo(2)
        elif count_defects == 4:
            cv2.putText(img,"Play/Pause", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            self.pauseAndStartVideo(2)
        else:
            cv2.putText(img,"Finger Control", (50,50),\
                        cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        #cv2.imshow('drawing', drawing)
        #cv2.imshow('end', crop_img)
        cv2.imshow('Gesture', img)
        all_img = np.hstack((drawing, crop_img))
        cv2.imshow('Contours', all_img)

    def pauseAndStartVideo(self, sec):
        self.device.emit_click(uinput.KEY_SPACE)
        self.playPauseTimer = True
        self.video_capture.release()
        time.sleep(sec)
        self.video_capture = cv2.VideoCapture(0)
        self.playPauseTimer = False

    def pauseVideo(self, sec):
        self.device.emit_click(uinput.KEY_SPACE)
        self.playPauseTimer = True
        self.video_capture.release()
        time.sleep(sec)
        self.video_capture = cv2.VideoCapture(0)

    def startVideo(self, sec):
        self.device.emit_click(uinput.KEY_SPACE)
        self.playPauseTimer = False
        #self.video_capture.release()
        time.sleep(sec)
        #self.video_capture = cv2.VideoCapture(0)

    def getCurrentWindow(self):
        return Sniffer.get_cur_window(Sniffer())[2]


if __name__ == '__main__':
    uc = UbiComp()