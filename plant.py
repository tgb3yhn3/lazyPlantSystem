import adafruit_dht
import time
import RPi.GPIO as GPIO
def isDay():
    print(time.localtime().tm_hour)
    if time.localtime().tm_hour>8 and time.localtime().tm_hour<17:
        return True
    
    return False
def test():
    while True:
        
        #pwmOut.stop(0)
        if ~GPIO.input(BUTTON_PIN):
            GPIO.output(MOTOR_RELAY_PIN,True)
            GPIO.output(LED_PIN,True)
            #pwmOut.stop(0)
        else:
            GPIO.output(MOTOR_RELAY_PIN,False)
            GPIO.output(LED_PIN,False)

                
        

DHT_PIN=16
PWM_PIN=20
DIR_PIN=21
LED_PIN=1
BUTTON_PIN=7
MOTOR_RELAY_PIN=12
targetTemp=25
RELAY_ON=False
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)#use BCM mode
GPIO.setup(PWM_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(MOTOR_RELAY_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN)
device=adafruit_dht.DHT11(DHT_PIN)

pwmOut = GPIO.PWM(PWM_PIN, 50)#inA control Fan speed
GPIO.output(DIR_PIN,False)#inB control fan direction
# setup
#--------------------------------------------------


# while True:
#         print(GPIO.input(BUTTON_PIN))
#         #pwmOut.stop(0)
#         if GPIO.input(BUTTON_PIN)==0:
#             print("push")
#             GPIO.output(MOTOR_RELAY_PIN,True)
#             GPIO.output(LED_PIN,True)
#             #pwmOut.stop(0)
#         else:
#             print("out")
#             GPIO.output(MOTOR_RELAY_PIN,False)
#             GPIO.output(LED_PIN,False)
#         time.sleep(60)
pwmOut.start(75)#control pwm speed

time.sleep(1)
pwmOut.stop(0)#NEED!!!!!
while True:
    try:
        # test()
        if isDay:
            GPIO.output(LED_PIN,True)
        else:
            GPIO.output(LED_PIN,False)
        #RELAY_ON=~RELAY_ON
        GPIO.output(MOTOR_RELAY_PIN,RELAY_ON)
        t=device.temperature
        h=device.humidity
        if(t>=targetTemp):
            pwmOut.start(50)
        else:
            pwmOut.stop(0)
        print(t)
        print(h)
        time.sleep(5)
    except KeyboardInterrupt:
        device.exit()
        GPIO.output(MOTOR_RELAY_PIN,False)
        GPIO.output(LED_PIN,False)
        pwmOut.stop(0)
        print("KI")
        break
        
    except RuntimeError:
        print("runtimeError retry 5 second later")
        time.sleep(5)
        continue
    except OverflowError:
        print("OverflowError retry 5 second later")
        time.sleep(5)
        continue
