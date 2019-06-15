import RPi.GPIO as GPIO
import time
import curses
import os

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)


GPIO.setmode(GPIO.BOARD)
servo1Pin=7
servo2Pin=11
Led1=12
Led2=13
GPIO.setup(Led1,GPIO.OUT)
GPIO.setup(Led2,GPIO.OUT)
GPIO.setup(servo1Pin,GPIO.OUT)
GPIO.setup(servo2Pin,GPIO.OUT)

GPIO.output(Led1,True)
GPIO.output(Led2,True)
time.sleep(0.5)
GPIO.output(Led1,False)
GPIO.output(Led2,False)
time.sleep(0.5)
GPIO.output(Led1,True)
GPIO.output(Led2,True)
time.sleep(0.5)
GPIO.output(Led1,False)
GPIO.output(Led2,False)
time.sleep(0.5)
GPIO.output(Led1,True)
GPIO.output(Led2,True)


pwm1=GPIO.PWM(servo1Pin,50)
pwm2=GPIO.PWM(servo2Pin,50)
pwm1.start(00)
pwm2.start(0)

#Ultrasound sensor HC-SR04
PIN_trigger = 38
PIN_echo = 40
GPIO.setup(PIN_trigger, GPIO.OUT)
GPIO.setup(PIN_echo, GPIO.IN)

GPIO.output(PIN_trigger, GPIO.LOW)
print "waiting for sensor to settle "
time.sleep(2)

tank_moving=False   # Tank not in movement

try:
    while True:

        if tank_moving==True:
            print "Calculating distance"
            GPIO.output(PIN_trigger, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(PIN_trigger, GPIO.LOW)

            while GPIO.input(PIN_echo)==0:
                pulse_start_time = time.time()
            while GPIO.input(PIN_echo)==1:
                pulse_end_time = time.time()
            pulse_duration = pulse_end_time - pulse_start_time
            distance = round(pulse_duration * 17150, 2)
            print "distance:",distance,"cm"
            if distance < 10:
                print "Object detected below 10cm: stopped"
                pwm1.ChangeDutyCycle(0)
                pwm2.ChangeDutyCycle(0)
                tank_moving=False
            
        char=screen.getch()
        
        if char==ord('q'):
            break
        if char==ord('S'):
            os.system('sudo shutdown now')
        elif char==curses.KEY_UP:
            print "Forward"
            pwm1.ChangeDutyCycle(15)
            pwm2.ChangeDutyCycle(1)
            tank_moving=True
            #pwm1.start(1)
            #pwm2.start(15)
            #time.sleep(0.5)
            #pwm1.stop()
            #pwm2.stop()
            #time.sleep(0.5)
        elif char==curses.KEY_DOWN:
            print "Backward"
            pwm1.ChangeDutyCycle(1)
            pwm2.ChangeDutyCycle(15)
            tank_moving=True
            #pwm1.start(15)
            #pwm2.start(1)
            #time.sleep(0.5)
            #pwm1.stop()
            #pwm2.stop()
            #time.sleep(0.5)
        elif char==curses.KEY_RIGHT:
            print "Right"
            pwm1.ChangeDutyCycle(1)
            pwm2.ChangeDutyCycle(1)
            tank_moving=True
            #pwm1.start(1)
            #pwm2.start(1)
            #time.sleep(0.5)
            #pwm1.stop()
            #pwm2.stop()
            #time.sleep(0.5)
        elif char==curses.KEY_LEFT:
            print "Left"
            pwm1.ChangeDutyCycle(15)
            pwm2.ChangeDutyCycle(15)
            tank_moving=True
            #pwm1.start(15)
            #pwm2.start(15)
            #time.sleep(0.5)
            #pwm1.stop()
            #pwm2.stop()
        elif char== 10: #ENTER key
            print "Stop"
            pwm1.ChangeDutyCycle(0)
            pwm2.ChangeDutyCycle(0)
            tank_moving=False
            #pwm1.start(6)
            ##pwm2.start(6)
            #time.sleep(0.5)
            #pwm1.start(1)
            #pwm2.start(1)
            #pwm1.stop()
            #pwm2.stop()
            #time.sleep(0.5)
        
finally:
    time.sleep(1)
    GPIO.cleanup()
    # Close down curses properly, inc turn echo back on!
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    
