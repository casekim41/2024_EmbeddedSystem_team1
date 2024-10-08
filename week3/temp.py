import time
from flask import Flask, render_template, url_for, redirect, jsonify

app = Flask(__name__)

# 0 : auto, 1 : manu
touch_state = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/distance')
def distance():
    
    distance_data = 1111
    return jsonify({'distance' : distance_data})

@app.route('/touch_state')
def touch():
    touch_state = 1
    return jsonify({'state' : touch_state})

@app.route('/temp_humid')
def adafruit():
    return jsonify({'humid' : 1, 'temp' : 2})
    

if __name__ == "__main__":    
    app.run(port=8080, host='localhost')