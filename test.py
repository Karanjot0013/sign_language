import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import tensorflow
import numpy as np
import math
import time
import os
import pyttsx3

cap=cv2.VideoCapture(0)
classifier=Classifier("Model/keras_model.h5","Model/labels.txt")
detector = HandDetector(maxHands=1)
offset=20
imgSize=300
text_speech = pyttsx3.init()
text_speech.setProperty("rate", 60)

# karan=input("enter the name for your sign ")
folder='Data/A'
# folder=folder+karan
# counter=0
words=[]
sentence=""
labels = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","stop","space"]
temp_letter=""
ctr=0


while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands , img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x , y , w , h = hand['bbox']

        imgWhite = np.ones((imgSize,imgSize,3),np.uint8)*255
        imgCrop = img[y-offset:y+h+offset,x-offset:x+w+offset]
        
        imgCropShape = imgCrop.shape
        

        aspectRatio = h/w

        if aspectRatio>1:
            k=imgSize/h
            wCal=math.ceil(k*w)
            imgResize = cv2.resize(imgCrop,(wCal,imgSize))
            imgResizeShape = imgResize.shape
            wGap=math.ceil((imgSize-wCal)/2)
            imgWhite[:,wGap:wCal+wGap] = imgResize
            prediction , index = classifier.getPrediction(imgWhite)
            #print(labels[index])
            if temp_letter == "":
                temp_letter=labels[index]
                ctr += 1
            elif temp_letter == labels[index]:
                ctr +=1
                if ctr>=12:
                    if temp_letter=='stop':
                        print(''.join([str(elem) for elem in words]))
                        text_speech.say(''.join([str(elem) for elem in words]))
                        text_speech.runAndWait()
                        text_speech.say(''.join([str(elem) for elem in words]))
                        text_speech.runAndWait()

                        words=[]
                        temp_letter=""
                        ctr=0
                    if len(words)==0:
                        words.append(temp_letter)
                        ctr=0
                    elif len(words)==1 and temp_letter==words[-1]:
                        ctr=1
                    elif len(words)>1 and temp_letter==words[-1]:
                        ctr=1
                    else:
                        words.append(temp_letter)

            else:
                ctr=1
                temp_letter=labels[index]
            print(words)    

                







        else:
            k=imgSize/w
            hCal=math.ceil(k*h)
            imgResize = cv2.resize(imgCrop,(imgSize,hCal))
            imgResizeShape = imgResize.shape
            hGap=math.ceil((imgSize-hCal)/2)
            imgWhite[hGap:hCal+hGap,:] = imgResize
            prediction , index = classifier.getPrediction(imgWhite)
            print(labels[index])
            if temp_letter == (-1):
                temp_letter=labels[index]
                ctr += 1
            elif temp_letter == labels[index]:
                ctr +=1
                if ctr>=24:
                    if temp_letter=='stop':
                        text_speech.say(''.join([str(elem) for elem in words]))
                        text_speech.runAndWait()
                        words=[]
                        temp_letter=-1
                        ctr=0
                    if len(words)==0:
                        words.append(temp_letter)
                        ctr=0
                    elif len(words)==1 and temp_letter==words[-1]:
                        ctr=1
                    elif len(words)>1 and temp_letter==words[-1]:
                        ctr=1
                    else:
                        words.append(temp_letter)

            else:
                ctr=1
                temp_letter=labels[index]
            print(words)  

        cv2.putText(imgOutput,labels[index],(x,y-20),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),2)



        cv2.imshow("ImageCrop",imgCrop)
        cv2.imshow("ImageWhite",imgWhite)
    
    
    cv2.imshow("Image",img)
    cv2.waitKey(1)




