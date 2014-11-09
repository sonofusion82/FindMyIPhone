#!/usr/bin/python
#
# The MIT License (MIT)
#
# Copyright (c) 2014 Chen Yew Ming
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
import RPi.GPIO as GPIO
import signal
import sys
from time import sleep
from pyicloud import PyiCloudService
import json
import daemon

GPIO_LED = 23
GPIO_SWITCH = 24
LED_OFF = 1
LED_ON = 0
SWITCH_ON = 0
SWITCH_OFF = 1

iCloudUsername = None
iCloudPassword = None

def iCloudPlaySound():
    if (iCloudUsername is not None) and (iCloudPassword is not None):
        api = PyiCloudService(iCloudUsername, iCloudPassword)
        #print api.iphone.location()
        #print api.iphone.status()
        api.iphone.play_sound("Raspberry Pi Greetings")

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

def buttonEventHandler(pin):
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

def initGpio():
    print 'Init GPIOs'
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_LED, GPIO.OUT)
    GPIO.setup(GPIO_SWITCH, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.output(GPIO_LED, LED_OFF)
    GPIO.add_event_detect(GPIO_SWITCH, GPIO.FALLING, callback=buttonEventHandler, bouncetime=100)


def main(filename):
    loadUsernamePassword(filename)
    initGpio()
    signal.signal(signal.SIGTERM, sigterm_handler)
    print 'FindMyIPhone started'
    try:
        while True:
           setLedOn();
           sleep(0.01)
           setLedOff();
           sleep(5)
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

def daemon_run():
    with daemon.DaemonContext():
        main(sys.argv[1])

if __name__ == '__main__':
    daemon_run()

