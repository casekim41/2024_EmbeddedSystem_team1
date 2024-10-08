import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

class MainScreen(BoxLayout):
    def toggle_led(self, led_num, state):
        try:
            # Send request to toggle the LED on the server
            response = requests.get(f'http://192.168.0.172:5000/led/{led_num}/{state}')  # Replace with your server's IP
            if response.status_code == 200:
                self.update_led_status()
        except requests.RequestException as e:
            print(f"Error toggling LED {led_num}: {e}")

    def update_led_status(self, *args):
        try:
            # Send request to get the current LED status from the server
            response = requests.get(f'http://192.168.0.172:5000/led_status')  # Replace with your server's IP
            if response.status_code == 200:
                data = response.json()
                # Update the UI with the current LED statuses
                self.ids.led1_status.text = f"LED1: {'ON' if data['led_states'][0] else 'OFF'}"
                self.ids.led2_status.text = f"LED2: {'ON' if data['led_states'][1] else 'OFF'}"
                self.ids.led3_status.text = f"LED3: {'ON' if data['led_states'][2] else 'OFF'}"
        except requests.RequestException as e:
            print(f"Error fetching LED status: {e}")

class PiControlApp(App):
    def build(self):
        root = MainScreen()
        Clock.schedule_once(root.update_led_status, 0.1)  # Update LED statuses after 0.1s
        return root

if __name__ == "__main__":
    PiControlApp().run()

