#!/usr/bin/python


import RPi.GPIO as GPIO
import time
import sys


FAN_PIN = 21            # BCM pin used to drive transistor's base
WAIT_TIME = 1           # [s] Time to wait between each refresh
FAN_MIN = 55            # [%] Fan minimum speed.
PWM_FREQ = 25           # [Hz] Change this value if fan has strange behavior


tempSteps = [45,50, 52, 56]
speedSteps = [55, 65, 75, 100]
#speedSteps = [100, 100, 100, 100]

hyst = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)
fan=GPIO.PWM(FAN_PIN,PWM_FREQ)
fan.start(0);


i = 0
cpuTempOld=0
fanSpeedOld=0


if(len(speedSteps) != len(tempSteps)):
    print("Numbers of temp steps and speed steps are different")
    exit(0)

try:
    while (1):

        cpuTempFile=open("/sys/class/thermal/thermal_zone0/temp","r")
        cpuTemp=float(cpuTempFile.read())/1000
        cpuTempFile.close()


        if(abs(cpuTemp-cpuTempOld > hyst)):
            

            if(cpuTemp < tempSteps[0]):
               fanSpeed = speedSteps[0]


            elif(cpuTemp >= tempSteps[len(tempSteps)-1]):
               fanSpeed = speedSteps[len(tempSteps)-1]

            else:       
                for i in range(0,len(tempSteps)-1):
                    if((cpuTemp >= tempSteps[i]) and (cpuTemp < tempSteps[i+1])):
                        fanSpeed = round((speedSteps[i+1]-speedSteps[i])\
                                   /(tempSteps[i+1]-tempSteps[i])\
                                   *(cpuTemp-tempSteps[i])\
                                   +speedSteps[i],1)

            if((fanSpeed != fanSpeedOld) ):
                if((fanSpeed != fanSpeedOld)\
                   and ((fanSpeed >= FAN_MIN) or (fanSpeed == 0))):
                    fan.ChangeDutyCycle(fanSpeed)
                    fanSpeedOld = fanSpeed                


        time.sleep(WAIT_TIME)


except(KeyboardInterrupt):
    print("Fan ctrl interrupted by keyboard")
    GPIO.cleanup()
    sys.exit()






