import cv2
import pyttsx3
text_speech = pyttsx3.init()


hello=['h','e','l','l','o',' ','p','e','e','p','s']
listToStr = ''.join([str(elem) for elem in hello])
print(listToStr)
key1=0
key1=cv2.waitKey(1000000000)
if key1 == ord('c'):
    text_speech.say(''.join([str(elem) for elem in hello]))
    text_speech.runAndWait()
    