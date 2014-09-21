#!/usr/bin/python
import RPi.GPIO as GPIO
import signal
import sys
from time import sleep
from pyicloud import PyiCloudService
import json

GPIO_LED = 23
GPIO_SWITCH = 24
LED_OFF = 1
LED_ON = 0
SWITCH_ON = 0
SWITCH_OFF = 1

iCloudUsername = None
iCloudPassword = None

def initGpio():
    print 'Init GPIOs'
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_LED, GPIO.OUT)
    GPIO.setup(GPIO_SWITCH, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.output(GPIO_LED, LED_OFF)

def iCloudPlaySound():
    if (iCloudUsername is not None) and (iCloudPassword is not None):
        api = PyiCloudService(iCloudUsername, iCloudPassword)
        #print api.iphone.location()
        #print api.iphone.status()
        api.iphone.play_sound()

def setLedOn():
    GPIO.output(GPIO_LED, LED_ON)

def setLedOff():
    GPIO.output(GPIO_LED, LED_OFF)

def isSwitchPressed():
    return True if GPIO.input(GPIO_SWITCH) == SWITCH_ON else False

def sigterm_handler(_signo, _stack_frame):
    sys.exit(0)

def loadUsernamePassword(filename):
    global iCloudUsername
    global iCloudPassword
    print 'Loading %s' % filename
    with open(filename, 'r') as f:
        data = json.load(f)
        iCloudUsername = str(data['username'])
        iCloudPassword = str(data['password'])

def main():
    loadUsernamePassword(sys.argv[1])
    initGpio()
    signal.signal(signal.SIGTERM, sigterm_handler)
    print 'FindMyIPhone started'
    try:
        while True:
            if isSwitchPressed():
                sleep(0.1)
                if isSwitchPressed():
                    print 'Button pressed'
                    setLedOn()
                    iCloudPlaySound()
                    setLedOff()
                    sleep(0.25)
                    setLedOn()
                    sleep(1)
                    setLedOff()
            sleep(0.1)
    except KeyboardInterrupt:
        print
        print 'KeyboardInterrupt received. Exiting...'
    finally:
        for i in range(0, 3):
            setLedOff()
            sleep(0.25)
            setLedOn()
            sleep(0.25)
        else:
            setLedOff()
        GPIO.cleanup()
        print 'Goodbye'


if __name__ == '__main__':
    main()
