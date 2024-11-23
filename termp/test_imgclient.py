import socket
import cv2
import base64
import numpy as np

class ImageClient:
    def __init__(self, host, port, image_path):
        self.host = host
        self.port = port
        self.image_path = image_path
        self.connect_to_server()

    def connect_to_server(self):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")

            self.send_image(client_socket)

            response = client_socket.recv(1024).decode('utf-8')
            print(f"Server response: {response}")

            client_socket.close()
        except Exception as e:
            print(f"Client error: {e}")

    def send_image(self, client_socket):
        try:
            # Read the image
            image = cv2.imread(self.image_path)
            if image is None:
                print(f"Image not found: {self.image_path}")
                return

            # Encode the image to base64
            _, buffer = cv2.imencode('.jpg', image)
            string_data = base64.b64encode(buffer).decode('utf-8')

            # Send the length of the encoded image data
            length = str(len(string_data))
            client_socket.sendall(length.encode('utf-8').ljust(64))

            # Send the actual image data
            client_socket.sendall(string_data.encode('utf-8'))
            print("Image sent successfully!")
        except Exception as e:
            print(f"Error sending image: {e}")

if __name__ == "__main__":
    client = ImageClient('203.252.136.226', 51313, 'a.jpeg')
