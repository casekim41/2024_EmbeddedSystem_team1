import RPi.GPIO as GPIO

class GPIOController:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        
    def setup_pins(self, pins:list, direction, initial=GPIO.LOW):
        for pin in pins:
            GPIO.setup(pin, direction, initial=initial)

    # def INIT_PINS(self):
    #     GPIO.setup(self.xSW,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    #     GPIO.setup(self.xSW,GPIO.IN,pull_up_down=GPIO.PUD_UP)

    
    def cleanup(self):
        GPIO.cleanup()
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()
