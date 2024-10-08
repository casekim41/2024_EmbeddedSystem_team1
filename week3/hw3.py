from flask import Flask, jsonify, render_template_string
import RPi.GPIO as GPIO
import time
import threading

app = Flask(__name__)

trig = 17
echo = 18

cal_dis = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(echo, GPIO.IN)
GPIO.setup(trig, GPIO.OUT)

def measure():
    global cal_dis
    GPIO.output(trig, False)
    time.sleep(2) 
    while True:
        GPIO.output(trig, True)
        time.sleep(0.00001)
        GPIO.output(trig, False)

        while not GPIO.input(echo):
            start = time.time()
            
        while GPIO.input(echo):
            stop = time.time()
            
        cal_time = stop - start
        cal_dis = cal_time * 34300 / 2
        print("Distance: {:.2f} cm".format(cal_dis))
        time.sleep(0.1)
        
            function updateDistance() {
                fetch('/distance')
                    .then(response => response.json())
                    .then(data => {
                        const distanceDisplay = document.getElementById('distanceDisplay');
                        if (data.distance < 10){
							distanceDisplay.innerHTML = '<p>Distance: ' + data.distance.toFixed(2) + ' cm<br>Too Close</p>';
						}
						else {
							distanceDisplay.innerHTML = '<p>Distance: ' + data.distance.toFixed(2) + ' cm</p>';
						}
                    });
            }
            setInterval(updateDistance, 1000);
        </script>
    </head>
    <body>
        <h1>Embedded System Distance Measurement</h1>
        <hr>
        <div style="padding-left:20px;" id="distanceDisplay">
            <p>Distance: Waiting...</p>
        </div>
    </body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html_text)

@app.route('/distance')
def distance():
    return jsonify(distance=cal_dis)

if __name__ == "__main__":
    thread = threading.Thread(target=measure)
    thread.daemon = True
    thread.start()
    
    app.run(port=8080, host='0.0.0.0')
