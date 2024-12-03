import socket
import threading

class ImageServer:
    def __init__(self, host, port, save_directory="received_images"):
        self.host = host
        self.port = port
        self.save_directory = save_directory
        self.server_socket = None
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
                # Receive the file name length
                filename_length = conn.recv(64).decode('utf-8').strip()
                if not filename_length.isdigit():
                    print(f"Invalid filename length received: {filename_length}")
                    break

                # Receive the file name
                filename = conn.recv(int(filename_length)).decode('utf-8')
                print(f"Receiving file: {filename}")

                # Receive the file size
                file_size = conn.recv(64).decode('utf-8').strip()
                if not file_size.isdigit():
                    print(f"Invalid file size received: {file_size}")
                    break

                # Receive the file data
                file_size = int(file_size)
                file_data = b""
                while len(file_data) < file_size:
                    packet = conn.recv(file_size - len(file_data))
                    if not packet:
                        raise ConnectionError("Socket connection lost")
                    file_data += packet

                # Save the file
                save_path = f"{self.save_directory}/{filename}"
                with open(save_path, 'wb') as f:
                    f.write(file_data)

                print(f"File saved as {save_path}")

        except ConnectionError:
            print("Socket connection lost")
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            conn.close()
            print("Client connection closed.")

if __name__ == "__main__":
    server = ImageServer('203.252.136.226', 51313)
