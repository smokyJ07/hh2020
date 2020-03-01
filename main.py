from pyzbar.pyzbar import decode
from PIL import Image
from gtts import gTTS
import os
from playsound import playsound
import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.HIGH)

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


def ReadImage(InputImage, message2):

    x = decode(Image.open(InputImage))
    if (x!=[]):
        message = x[0].data.decode()
        if (message2 != message):
            message2 = message
            print(message)
            return message
    else:
        print("blank")
        return "blank"

    x = []




try:
    message2 = "blank"
    while(True):
        os.system('raspistill -t 600 -o qrCode.jpg')
        # ultrasound sensor distance measuring
        #dist = distance()
        dist = 40
        print ("Measured Distance = %.1f cm" % dist)
        if dist < 30:
            os.system("sudo omxplayer -o local beep1.mp3")
            print("To close!")

        # check whether on track
        if GPIO.input(25):
            os.system("sudo omxplayer -o local beep2.mp3")
            print("on track")
        else:
            print("off track")
        #time.sleep(0.5)

        message2 = ReadImage('qrCode.jpg', message2)

        if (message2 != "blank"):
            language = 'en'
            myobj = gTTS(text=message2, lang=language, slow=False)
            myobj.save('audio.mp3')
            #playsound('audio.mp3')
            os.system('sudo omxplayer -o local audio.mp3')
            print("this worked")
            message2 = "blank"

except KeyboardInterrupt:
    print("\n")

finally:
    GPIO.cleanup()
