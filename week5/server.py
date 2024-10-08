from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulate LED states (0 = OFF, 1 = ON)
led_states = [0, 0, 0]

# Control LED
@app.route('/led/<int:led_num>/<int:state>', methods=['GET'])
def control_led(led_num, state):
    if 0 <= led_num < len(led_states):
        led_states[led_num] = state
        return jsonify({"status": "success", "led_num": led_num, "state": state})
    return jsonify({"status": "error", "message": "Invalid LED number"}), 400

# Get current LED status
@app.route('/led_status', methods=['GET'])
def get_led_status():
    return jsonify({"led_states": led_states})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

