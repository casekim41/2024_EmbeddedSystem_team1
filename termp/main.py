from gpioController import GPIOController
from motorController import StepperMotorController, ServoController
from plotter import Plotter
from fileReader import FileReader
from imageServer import ImageServer
import threading
import time

def get_current_ip():
      with socket.socket(socket.AF_INET, socket.SOCK_DGRAM)as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]

if __name__ == "__main__":
    step_L = [17, 18, 27, 22]
    step_R = [23, 24, 5, 6]
    XSW = 21
    YSW = 20
    SERVO = 26
    SERVER_HOST = get_current_ip()
    SERVER_PORT = 51313

    try:
        with GPIOController() as gpio_controller:
            stepper = StepperMotorController(step_L, step_R, XSW, YSW)
            servo = ServoController(SERVO)
            plotter = Plotter(stepper, servo)
            

            def run_server():
                server = ImageServer(SERVER_HOST, SERVER_PORT)
                while True:
                      conn, addr = server.server_socket.accept()
                      print(f"connection with {addr}")
                      reader = FileReader(plotter, client_socket=conn)
                      image_file = "./gcode/1.gcode"
                      reader.draw(image_file)
                      conn.close()
            
            server_thread = threading.Thread(target=run_server)
            server_thread.daemon = True
            server_thread.start()

            stepper.INIT_STEPPER()

            while True:
                time.sleep(1)

    except KeyboardInterrupt:
        print("\nProgram interrupted")



"""from gpioController import GPIOController
from motorController import StepperMotorController,ServoController
from plotter import Plotter
from fileReader import FileReader
import time

if __name__ == "__main__":
    step_L = [17,18,27,22]
    step_R = [23,24,5,6]
    XSW = 21
    YSW = 20
    SERVO = 26
    try:
        with GPIOController() as gpio_controller:
            stepper = StepperMotorController(step_L,step_R,XSW,YSW)
            servo = ServoController(SERVO)
            plotter = Plotter(stepper, servo)
            
            reader = FileReader(plotter)
            
            stepper.INIT_STEPPER()
            
            
            reader.draw("./img/real_sponge.ngc")
            
            

    except KeyboardInterrupt:
        print("\ninterrupted")"""
