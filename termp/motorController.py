from gpioController import GPIOController
import time
from math import cos, sin, radians, degrees
import RPi.GPIO as GPIO


class StepperMotorController(GPIOController):
    step_sequence = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1]
    ]

    def __init__(self, STEPL:list, STEPR:list, xSW:int, ySW:int):
        super().__init__()
        self.STEPL = STEPL
        self.STEPR = STEPR
        self.xSW = xSW
        self.ySW = ySW
        self.seqL = 0
        self.seqR = 0
        self.x = 0.0
        self.y = 0.0
        self.xSW_CLICKED = 0
        self.ySW_CLICKED = 0
        self.setup_pins(STEPL+STEPR, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.xSW,GPIO.IN,pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.ySW,GPIO.IN,pull_up_down=GPIO.PUD_UP)

    def move_vec(self, x=0.0, y=0.0, delay=0.00095):
        self.x += x
        self.y += y
        print("{:8.2f} {:8.2f}".format(self.x, self.y))
        
        L_step = abs(x + y) + self.seqL
        R_step = abs(x - y) + self.seqR
        L_dir = -1 if x + y > 0 else 1
        R_dir = -1 if x - y > 0 else 1
        L_counter, R_counter = self.seqL, self.seqR

        last_time = time.perf_counter()
        while L_counter < L_step or R_counter < R_step:
            current_time = time.perf_counter()
            if current_time - last_time >= delay:
                last_time = current_time

                if L_counter < L_step and L_counter * R_step // L_step <= R_counter:
                    for pin in range(4):
                        GPIO.output(self.STEPL[L_dir * pin], self.step_sequence[L_counter % len(self.step_sequence)][pin])
                    L_counter += 1

                if R_counter < R_step and R_counter * L_step // R_step <= L_counter:
                    for pin in range(4):
                        GPIO.output(self.STEPR[R_dir * pin], self.step_sequence[R_counter % len(self.step_sequence)][pin])
                    R_counter += 1
        ## save sequence for not jittering
        self.seqL, self.seqR = L_counter % len(self.step_sequence), R_counter % len(self.step_sequence)

    def circle(self, r, start_angle=0, end_angle=360, cw=0):
        last_x, last_y = self.x, self.y
        m, n = last_x - r * cos(radians(start_angle)), last_y - r * sin(radians(start_angle))
        increase = -1 if cw else 1
        ## move if (angle gap > 10)
        for angle in range(int(start_angle), int(end_angle), increase * 10):
            rad_angle = radians(angle)
            next_x = m + r * cos(rad_angle)
            next_y = n + r * sin(rad_angle)
            delta_x, delta_y = next_x - last_x, next_y - last_y
            self.move_vec(delta_x, delta_y, 0.0017)
            last_x, last_y = next_x, next_y
        ## move if (0 < angle gap < 10)
        if int(start_angle) != int(end_angle):
            if angle != end_angle:
                rad_angle = radians(end_angle)
                next_x = m + r * cos(rad_angle)
                next_y = n + r * sin(rad_angle)
                delta_x, delta_y = next_x - last_x, next_y - last_y
                self.move_vec(delta_x, delta_y, 0.0017)
        ## move if int(start angle) == int(end angle)
        else:
            rad_angle = radians(end_angle)
            next_x = m+r*cos(rad_angle)
            next_y = n+r*sin(rad_angle)
            delta_x,delta_y = next_x-last_x, next_y-last_y
            self.move_vec(delta_x,delta_y,0.0017)
            
    def INIT_STEPPER(self):
        while 1:								# x
            if GPIO.input(self.xSW): self.xSW_CLICKED = 1
            if not self.xSW_CLICKED:
                self.move_vec(-8,0,0.0015)	
            else:
                break
        while 1:								# y
            if GPIO.input(self.ySW): self.ySW_CLICKED = 1 
            if not self.ySW_CLICKED:
                self.move_vec(0,-8,0.0015)
            else:
                break
        time.sleep(0.1)
        self.move_vec(80,80,0.0022)
        time.sleep(0.2)
        self.move_vec(-80,-80,0.0024)
        ## init xy
        self.x,self.y = 0.0,0.0
        self.xSW_CLICKED, self.ySW_CLICKED = 0, 0
        print("=={:8.2f} {:8.2f}".format(self.x, self.y))
        

class ServoController(GPIOController):
    def __init__(self, servo_pin):
        super().__init__()
        self.servo_pin = servo_pin
        self.setup_pins([servo_pin], GPIO.OUT)
        self.pwm = GPIO.PWM(servo_pin, 50)
        self.pwm.start(0)

    def move_pen(self, down=True):
        angle = 180 if down else 0
        duty_cycle = 2.5 + (angle / 180) * 10
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.15)  # waiting for change
