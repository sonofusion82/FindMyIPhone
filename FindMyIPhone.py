import RPi.GPIO as GPIO
import signal
import sys
from time import sleep

GPIO_LED = 23
GPIO_SWITCH = 24
LED_OFF = 1
LED_ON = 0
SWITCH_ON = 0
SWITCH_OFF = 1

def initGpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_LED, GPIO.OUT)
    GPIO.setup(GPIO_SWITCH, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.output(GPIO_LED, LED_OFF)

def setLedOn():
    GPIO.output(GPIO_LED, LED_ON)

def setLedOff():
    GPIO.output(GPIO_LED, LED_OFF)

def isSwitchPressed():
    return True if GPIO.input(GPIO_SWITCH) == SWITCH_ON else False

def sigterm_handler(_signo, _stack_frame):
    sys.exit(0)

def main():
    initGpio()
    signal.signal(signal.SIGTERM, sigterm_handler)
    try:
        while True:
            if isSwitchPressed():
                sleep(0.1)
                if isSwitchPressed():
                    setLedOn()
                    sleep(1)
                    setLedOff()
            sleep(0.1)
    finally:
        GPIO.cleanup()
        print 'Goodbye'


if __name__ == '__main__':
    main()
