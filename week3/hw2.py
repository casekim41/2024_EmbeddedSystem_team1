from flask import Flask, jsonify, render_template_string
import RPi.GPIO as GPIO
import time
import threading

app = Flask(__name__)

sig = 18
touch_state = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(sig, GPIO.IN)

def touch():
    global touch_state
    while True:
        touch_state = GPIO.input(sig)
        print(touch_state)
        time.sleep(1)

html_text = '''
<html>
    <head>
        <meta charset="UTF-8">
        <title>Touch Control</title>
        <script>
            function updateTouchState() {
                fetch('/touch_state')
                    .then(response => response.json())
                    .then(data => {
                        const touchDisplay = document.getElementById('touchDisplay');
                        if (data.state === 1) {
                            touchDisplay.innerHTML = '<p>Touch State : Detected</p>';
                        } else {
                            touchDisplay.innerHTML = '<p>Touch State : Nothing</p>';
                        }
                    });
            }
            setInterval(updateTouchState, 1000);
        </script>
    </head>
    <body>
        <h1>Embedded System Touch Control</h1>
        <hr>
        <div style="padding-left:20px;" id="touchDisplay">
        </div>
    </body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html_text)

@app.route('/touch_state')
def touch_state_endpoint():
    return jsonify(state=touch_state)

if __name__ == "__main__":
    thread = threading.Thread(target=touch)
    thread.daemon = True
    thread.start()
    
    app.run(port=8080, host='0.0.0.0')
