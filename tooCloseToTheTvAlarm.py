#!/usr/bin/python3

import cv2
import numpy as np
from gtts import gTTS
import os

import threading
from threading import Thread
import time
tooCloseToTheTvAlarmEnable = 0;

def tooCloseToTheTvAlarm():
    global tooCloseToTheTvAlarmEnable
    while 1:
        if tooCloseToTheTvAlarmEnable == 1:
            # What to make the function do
            string='Hello Daniel, I\'m your home assistant'
            print("%s\n",string);
            tts = gTTS(text=string, lang='en')
            tts.save('speech.mp3')
            os.system('play speech.mp3')
            string='Attention! Attention! Too close to the TV.'
            print("%s\n",string);
            tts = gTTS(text=string, lang='en')
            tts.save('speech.mp3')
            os.system('play speech.mp3')
            tooCloseToTheTvAlarmEnable=0;
    
def captureCamera():
    global tooCloseToTheTvAlarmEnable
    face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    capCamera = cv2.VideoCapture(5) 
    windowName = "cv tranforms"
    while capCamera.isOpened():
        isRead, frame = capCamera.read()
        dispFrame = cv2.resize(frame, (640,360))
        grey = cv2.cvtColor(dispFrame, cv2.COLOR_BGR2GRAY) 
        faces = face_detector.detectMultiScale(grey, 1.3, 5)
        x=0;
        y=0;
        w=0;
        h=0;
        for (x, y, w, h) in faces:
            cv2.rectangle(dispFrame, (x, y), (x + w, y + h), (0, 255, 0))    
        if w > 55 :
            tooCloseToTheTvAlarmEnable=1;
            print("%d %d\n",w,h);
        cv2.imshow(windowName, dispFrame)
        if cv2.waitKey(10) == 27:
            break
    camera.release()
    cv2.destroyAllWindows()

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print("Starting " + self.name)
        if self.threadID==1 :
            tooCloseToTheTvAlarm();
        else:
            captureCamera()
            
# Create new threads
# Thread for flask
thread1 = myThread(1, "Thread-Alarm", 1)
# Thread for mqtt
thread2 = myThread(2, "Thread-CaptureCamera", 2)

# Start new Threads
thread1.start()
thread2.start()
