import socket
import threading
import os
from datetime import datetime
import numpy as np
from PIL import Image
import cv2
from scipy.spatial import distance

class ImageServer:
    def __init__(self, host, port, save_directory="received_images", gcode_directory="gcode"):
        self.host = host
        self.port = port
        self.save_directory = save_directory
        self.gcode_directory = gcode_directory
        self.server_socket = None
        os.makedirs(self.save_directory, exist_ok=True)
        os.makedirs(self.gcode_directory, exist_ok=True)
        self.start_server()

    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"Server listening on {self.host}:{self.port}")
            while True:
                conn, addr = self.server_socket.accept()
                print(f"Connection established with {addr}")
                client_thread = threading.Thread(target=self.handle_client, args=(conn,))
                client_thread.start()
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()
                print("Server socket closed.")

    def handle_client(self, conn):
        try:
            while True:
                filename_length = conn.recv(64).decode('utf-8').strip()
                if not filename_length.isdigit():
                    break
                filename = conn.recv(int(filename_length)).decode('utf-8')
                print(f"Receiving file: {filename}")
                file_size = conn.recv(64).decode('utf-8').strip()
                if not file_size.isdigit():
                    break
                file_size = int(file_size)
                file_data = b""
                while len(file_data) < file_size:
                    packet = conn.recv(file_size - len(file_data))
                    if not packet:
                        raise ConnectionError("Socket connection lost")
                    file_data += packet
                timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
                cropped_image_path = os.path.join(self.save_directory, f"{timestamp}_cropped.png")
                self.save_and_crop_image(file_data, cropped_image_path, 50)
                print(f"Cropped image saved as {cropped_image_path}")
                gcode_path = os.path.join(self.gcode_directory, f"{timestamp}.gcode")
                self.convert_to_gcode(cropped_image_path, gcode_path)
                print(f"G-code saved as {gcode_path}")
        except ConnectionError:
            print("Socket connection lost")
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            conn.close()
            print("Client connection closed.")

    def save_and_crop_image(self, file_data, output_path, pixels_to_crop):
        nparr = np.frombuffer(file_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        height, width = image.shape[:2]
        cropped_image = image[:height - pixels_to_crop, :]
        cv2.imwrite(output_path, cropped_image)

    def convert_to_gcode(self, image_path, gcode_path, scale=1.0):
        image = Image.open(image_path).convert('L')
        image_array = np.array(image)
        _, binary_image = cv2.threshold(image_array, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = self.optimize_contour_order(contours)
        with open(gcode_path, 'w') as f:
            f.write("G21\n")
            f.write("G90\n")
            f.write("M3 S255\n")
            for contour in contours:
                start_x, start_y = contour[0][0]
                scaled_start_x = start_x * scale
                scaled_start_y = start_y * scale
                f.write(f"G0 X{scaled_start_x:.3f} Y{scaled_start_y:.3f}\n")
                f.write("G1\n")
                for point in contour:
                    x, y = point[0]
                    scaled_x = x * scale
                    scaled_y = y * scale
                    f.write(f"G1 X{scaled_x:.3f} Y{scaled_y:.3f}\n")
            f.write("M3 S0\n")
            f.write("G0 X0 Y0\n")

    def optimize_contour_order(self, contours):
        reordered_contours = []
        current_position = (0, 0)
        remaining_contours = contours.copy()
        while remaining_contours:
            nearest_contour_idx = min(
                range(len(remaining_contours)),
                key=lambda i: distance.euclidean(current_position, remaining_contours[i][0][0])
            )
            nearest_contour = remaining_contours.pop(nearest_contour_idx)
            reordered_contours.append(nearest_contour)
            current_position = nearest_contour[-1][0]
        return reordered_contours

if __name__ == "__main__":
    server = ImageServer('203.252.136.226', 51313)
