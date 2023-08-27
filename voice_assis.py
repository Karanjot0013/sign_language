import pyttsx3
text_speech = pyttsx3.init()

answer=input("what you want to convert to speech")



#text_speech.getProperty('voices')
text_speech.setProperty("rate", 80)
text_speech.say(answer)
text_speech.runAndWait()