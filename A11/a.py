import cv2
import sys
import numpy as np
import math
import time
import uinput
import speech_recognition as sr
#from sniff_x import Sniffer
from Tkinter import *
from thread import start_new_thread
from multiprocessing import Process
class UbiComp():
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.cascPath = "haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascPath)
        self.playPauseTimer = False
        self.isZero = False
        self.gestureArray = []
        self.timerProcess = Process(target=self.stopwatch, args=(2,))
        self.timerProcess_2 = Process(target=self.stopwatch, args=(3,))
        self.timerProcess_3 = Process(target=self.gestureWatch, args=(2,))
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
        try:
            while True:
                self.ret, self.img = self.video_capture.read()
                #if str(self.getCurrentWindow()).endswith(self.VLC_KEY):
                self.faceDetector()
                self.gestureRecognizer()

                #if self.playPauseTimer == False:
                    #    self.gestureRecognizer()
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                k = cv2.waitKey(10)
                if k == 27:
                    break
        except KeyboardInterrupt:
            pass
            #time.sleep(0.05)
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
        start = time.time()
        time.clock()
        elapsed = 0
        while elapsed < seconds:
            elapsed = time.time() - start

        if elapsed == seconds:
            print "Play/Pause because of zero faces"
            self.device.emit_click(uinput.KEY_SPACE)
        #print self.playPauseTimer

    def gestureWatch (self, seconds, gesture):

        start = time.time()
        time.clock()
        elapsed = 0
        while elapsed < seconds:
            elapsed = time.time() - start

        if elapsed == seconds:
            print "Gesture done"
            if gesture == "volumeUp":
                self.device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_UP])
            elif gesture ==  "volumeDown":
                self.device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_DOWN])
            elif gesture == "PlayPause":
                self.device.emit_click(uinput.KEY_SPACE)
            print gesture
            return

    def infoTextBox(self):
        root = Tk()
        root.title("Instructions")
        T = Text(root, height=20, width=150)
        T.pack()
        T.insert(END, "VLC Controller is a simple controller for the popular VLC Media Player using face detection and finger recognition with you webcam.\nFunctions\nFace Detection: \n- pause video when no face is detected after three seconds\n- play when face is detected again\n\nFinger Recognition in the appropriate rectangle on the right of the opening webcam window:\n- two fingers: volume down\n- three fingers: volume up\n- four/five fingers: play/pause\n\nSteps\n1: start script ubicomp.py with sudo python ubicomp.py\n2: open VLC Media Player\n3: Drag and Drop Video in VLC\n4: use rectangle box to recognize finger count \n5: use face detection\n\nCLOSE INSTRUCTIONS TO START! Have fun!\nKill application: CTRL + C")
        mainloop()
    def faceDetector(self):

        #print self.playPauseTimer

         # Capture frame-by-frame

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(self.img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        if len(faces) == 0 and self.isZero == False:
            if self.playPauseTimer == False:
                self.isZero = True

                if self.timerProcess.is_alive():
                    self.timerProcess.terminate()
                    self.timerProcess  = Process(target=self.stopwatch, args=(2,))
                    self.playPauseTimer = False
                if self.timerProcess.is_alive() == False & self.playPauseTimer == False:
                    self.timerProcess  = Process(target=self.stopwatch, args=(2,))
                    self.timerProcess.start()
                    self.playPauseTimer = True


        elif len(faces) > 0:
            self.isZero = False
            if self.timerProcess.is_alive():
                #print("TERMINATE")
                self.timerProcess.terminate()
                self.timerProcess = Process(target=self.stopwatch, args=(2,))
                self.playPauseTimer = False


            if self.playPauseTimer == True:
                 self.timerProcess_2  = Process(target=self.stopwatch, args=(3,))
                 #self.device.emit_click(uinput.KEY_SPACE)
                 self.timerProcess_2.start()

                 self.playPauseTimer = False

        # Display the resulting frame

    def gestureRecognizer(self):

        # When everything is done, release the capture
        cv2.rectangle(self.img,(300,300),(100,100),(0,255,0),0)
        crop_img = self.img[100:300, 100:300]
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
        if count_defects == 2:
            cv2.putText(self.img,"Volume Down", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            self.volumeDown(2)
        elif count_defects == 3:
            cv2.putText(self.img, "Volume Up", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            self.volumeUp(2)
        elif count_defects == 4:
            cv2.putText(self.img,"Play/Pause", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            self.pauseAndStartVideo(2)
        else:
            cv2.putText(self.img,"Finger Control", (50,50),\
                        cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        #cv2.imshow('drawing', drawing)
        #cv2.imshow('end', crop_self.img)
        cv2.imshow('Gesture', self.img)
        all_img = np.hstack((drawing, crop_img))
        cv2.imshow('Contours', all_img)

    def volumeUp(self, sec):
        gesture = "volumeUp"
        #self.device.emi  t_combo([uinput.KEY_LEFTCTRL, uinput.KEY_UP])
        self.runGestureTimer(sec, gesture)
        #print "volume up"

    def volumeDown(self, sec):
        gesture = "volumeDown"
        #self.device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_DOWN])
        self.runGestureTimer(sec, gesture)
        #print "volume down"

    def pauseAndStartVideo(self, sec):
        gesture = "PlayPause"
        #self.device.emit_click(uinput.KEY_SPACE)
        #if self.playPauseTimer == True:
            #self.playPauseTimer = False
        #else:
            #self.playPauseTimer = True

        self.runGestureTimer(sec, gesture)
        #print "pause/play"

    def runGestureTimer(self, seconds, gesture):

        self.gestureArray.append(gesture)
        #print self.gestureArray
        if self.timerProcess_3.is_alive():
            if self.gestureArray[-2] != gesture:
                    self.timerProcess_3.terminate()
                    self.timerProcess_3  = Process(target=self.gestureWatch, args=(seconds,))
                    print "gesture terminated"

        if self.timerProcess_3.is_alive() == False:
                self.timerProcess_3  = Process(target=self.gestureWatch, args=(seconds, gesture,))
                self.timerProcess_3.start()


    def getCurrentWindow(self):
        return Sniffer.get_cur_window(Sniffer())[2]

if __name__ == '__main__':
    uc = UbiComp()