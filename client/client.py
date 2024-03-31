import socket
import json

# HOST = '0.tcp.ap.ngrok.io'
HOST = 'localhost'
# HOST = '192.168.153.128'
PORT = 4000


class Client:
    def __init__(self) -> None:
        self.client = None
        self.data = None

    def connect_to_server(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))

    def receive_data(self):
        while True:
            data = self.client.recv(1024)
            if data:
                self.data = json.loads(data.decode())
                print(f"Data: {json.loads(data.decode())}")

    def send_data(self, data):
        if self.client is not None:
            # print(f"Send: {data}")
            self.client.sendall(json.dumps(data).encode())

    def close_connection(self):
        self.client.close()

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data


if __name__ == '__main__':
    server = Client()
    server.connect_to_server()
    # server.receive_data()
    server.send_data({"column": 1, "row": 2})
