from flask import Flask, render_template, url_for, redirect, jsonify

import Adafruit_DHT
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

app = Flask(__name__)

# 거리센서
trig_pin = 17
echo_pin = 18
cal_dis = 0

# 터치센서
touch_state = 0
touch_pin = 19

# led
ledPins = [16, 20, 21]
ledStates = [0, 0, 0]

# 온습도
sensor = Adafruit_DHT.DHT11
HT_pin = 2

# 부저
buzzer_pin = 27
buzzer_state = 0


GPIO.setmode(GPIO.BCM)

GPIO.setup(echo_pin, GPIO.IN)
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(ledPins[0],GPIO.OUT)
GPIO.setup(ledPins[1],GPIO.OUT)
GPIO.setup(ledPins[2],GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(touch_pin, GPIO.IN)


def cal_distance():
    
    GPIO.output(trig_pin, True)
    time.sleep(0.001)
    GPIO.output(trig_pin, False)
    print('good1')    
    

    while GPIO.input(echo_pin) == False:
        
        start = time.time()
 
    while GPIO.input(echo_pin) == True:
        stop = time.time()
    print('good2')        
    cal_time = stop - start
    cal_dis = cal_time*34300/2
    
    # print("distance : {:.2f}".format(cal_dis))
    return cal_dis


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_distance')
def get_distance():
    
    distance_data = int(cal_distance())
    print(distance_data)
    if distance_data < 30:
        GPIO.output(buzzer_pin, True)
    else:
        GPIO.output(buzzer_pin, False)

    return jsonify({'distance' : distance_data,
                    'buzzer_state' : buzzer_pin})
    # distance_data = 1111
    # return jsonify({'distance' : distance_data})

@app.route('/touch_state')
def touch():
    global touch_state
    if GPIO.input(touch_pin) == True:
        touch_state = not touch_state

    return jsonify({'state' : touch_state})


@app.route('/temp_humid')
def adafruit():
    humid, temp = Adafruit_DHT.read_retry(sensor, HT_pin)
    return jsonify({'temp' : temp,
                    'humid' : humid
                    })

if __name__ == "__main__":    
    app.run(port=5028, host='127.0.0.1')
