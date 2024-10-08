import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.togglebutton import ToggleButton

class MainScreen(BoxLayout):
    is_auto_mode = False  # 자동 모드 여부를 추적

    def toggle_led(self, led_num, state):
        if not self.is_auto_mode:  # 자동 모드가 아닐 때만 수동 제어 허용
            try:
                response = requests.get(f'http://192.168.0.228:5000/led/{led_num}/{state}')
                if response.status_code == 200:
                    print(f"LED {led_num} {'ON' if state == 1 else 'OFF'}")
                    self.update_led_status()  # LED 상태를 바로 업데이트
                else:
                    print(f"Failed to toggle LED {led_num}")
            except requests.RequestException as e:
                print(f"Error toggling LED {led_num}: {e}")
        else:
            print("Cannot manually toggle LEDs in auto mode.")

    def update_led_status(self, *args):
        try:
            response = requests.get(f'http://192.168.0.228:5000/led_status')
            if response.status_code == 200:
                data = response.json()
                self.ids.led1_status.text = f"LED1: {'ON' if data['led_states'][0] else 'OFF'}"
                self.ids.led2_status.text = f"LED2: {'ON' if data['led_states'][1] else 'OFF'}"
                self.ids.led3_status.text = f"LED3: {'ON' if data['led_states'][2] else 'OFF'}"
        except requests.RequestException as e:
            print(f"Error fetching LED status: {e}")

    def update_sensor_data(self, *args):
        try:
            # 온습도 센서 데이터 가져오기
            response = requests.get(f'http://192.168.0.228:5000/dht_data')
            if response.status_code == 200:
                data = response.json()
                temperature = data['temperature']
                humidity = data['humidity']

                self.ids.temperature_label.text = f"Temperature: {temperature} °C"
                self.ids.humidity_label.text = f"Humidity: {humidity} %"

                if self.is_auto_mode:  # 자동 모드일 때만 LED 제어
                    # 첫 번째 LED: 온도가 18도보다 낮으면 켜지고, 높으면 꺼짐
                    if temperature < 18:
                        self.control_led_automatically(0, 1)
                    else:
                        self.control_led_automatically(0, 0)

                    # 두 번째 LED: 습도가 70% 이상이면 켜지고, 낮으면 꺼짐
                    if humidity >= 70:
                        self.control_led_automatically(1, 1)
                    else:
                        self.control_led_automatically(1, 0)

                    # 세 번째 LED: 온도가 26도보다 높으면 켜지고, 낮으면 꺼짐
                    if temperature > 26:
                        self.control_led_automatically(2, 1)
                    else:
                        self.control_led_automatically(2, 0)

            # 초음파 센서 데이터 가져오기 및 부저 제어
            response = requests.get(f'http://192.168.0.228:5000/ultrasonic_data')
            if response.status_code == 200:
                data = response.json()
                distance = data['distance']
                self.ids.distance_label.text = f"Distance: {distance:.2f} cm"  # 소수점 2자리로 제한

                if self.is_auto_mode and distance < 20:  # 거리가 20cm보다 가까우면 부저를 울림
                    self.control_buzzer(1)
                else:
                    self.control_buzzer(0)

        except requests.RequestException as e:
            print(f"Error fetching sensor data: {e}")

    def control_led_automatically(self, led_num, state):
        try:
            response = requests.get(f'http://192.168.0.228:5000/led/{led_num}/{state}')
            if response.status_code == 200:
                print(f"LED {led_num} {'ON' if state == 1 else 'OFF'} (Automatic Mode)")
                self.update_led_status()
            else:
                print(f"Failed to control LED {led_num} in automatic mode.")
        except requests.RequestException as e:
            print(f"Error controlling LED {led_num}: {e}")

    def control_buzzer(self, state):
        try:
            response = requests.get(f'http://192.168.0.228:5000/buzzer/{state}')
            if response.status_code == 200:
                print(f"Buzzer {'ON' if state == 1 else 'OFF'}")
            else:
                print("Failed to control buzzer.")
        except requests.RequestException as e:
            print(f"Error controlling buzzer: {e}")

    def toggle_auto_mode(self, instance):
        self.is_auto_mode = instance.state == 'down'
        print(f"Auto Mode {'Enabled' if self.is_auto_mode else 'Disabled'}")

class PiControlApp(App):
    def build(self):
        root = MainScreen()
        Clock.schedule_once(root.update_led_status, 0.1)
        Clock.schedule_interval(root.update_sensor_data, 1)  # 1초마다 센서 데이터 업데이트
        return root

if __name__ == "__main__":
    PiControlApp().run()
