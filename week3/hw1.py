from flask import Flask, render_template_string, redirect, url_for
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
ledPins = [17, 27, 22]
ledStates = [0, 0, 0]

GPIO.setup(ledPins[0],GPIO.OUT)
GPIO.setup(ledPins[1],GPIO.OUT)
GPIO.setup(ledPins[2],GPIO.OUT) 

def update_leds():
	for idx, val in enumerate(ledStates):
		GPIO.output(ledPins[idx], val)
		

html_text = '''
<html>
	<head>
		<title> LED Control </title>
	</head>
	<body>
		<h1> LED1  LED2  LED3 </h1>
		<hr>
		
		<div style = "padding-left:20px;">
			<h3>LED1 LED2 LED3</h3>
			<p>
				<b>LED1 : {% if ledStates[0] == 1 %} ON {% else %} OFF {%endif%}</b>
				<a href="{{url_for("ledControl",ledNum=0,ledState=1)}}"> <input type="button" value="ON"></a>
				<a href="{{url_for("ledControl",ledNum=0,ledState=0)}}"> <input type="button" value="OFF"></a>
			</p>
			<p>
				<b>LED2 : {% if ledStates[1] == 1 %} ON {% else %} OFF {%endif%}</b>
				<a href="{{url_for("ledControl",ledNum=1,ledState=1)}}"> <input type="button" value="ON"></a>
				<a href="{{url_for("ledControl",ledNum=1,ledState=0)}}"> <input type="button" value="OFF"></a>
			</p>
			<p>
				<b>LED3 : {% if ledStates[2] == 1 %} ON {% else %} OFF {%endif%}</b>
				<a href="{{url_for("ledControl",ledNum=2,ledState=1)}}"> <input type="button" value="ON"></a>
				<a href="{{url_for("ledControl",ledNum=2,ledState=0)}}"> <input type="button" value="OFF"></a>
			</p>
		</div>
	</body>
</html>
'''


app = Flask(__name__)


@app.route('/')
def index():
	return render_template_string(html_text,ledStates = ledStates)

@app.route("/<int:ledNum>/<int:ledState>")
def ledControl(ledNum, ledState):
	ledStates[ledNum] = ledState
	update_leds()
	return redirect(url_for("index"))



if __name__ == "__main__":
	app.run(port=8080, host="0.0.0.0")
