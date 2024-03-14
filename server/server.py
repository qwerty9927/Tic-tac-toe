import socket 
import threading

HOST = 'localhost'
# HOST = '192.168.153.1'
PORT = 4000
CONNECTIONS = 2

class Server:
  def __init__(self) -> None:
    self.server = None
    self.clients = []
    
  def start_server(self):
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server.bind((HOST, PORT))
    self.server.listen(CONNECTIONS)
    print("Waiting for connection...")
    while True:
      connection, addr = self.server.accept()
      threading.Thread(target=self.handle_connection, args=(connection, addr)).start()

  def handle_connection(self, socket, addr):
    print(f"Accepted connection from {addr}")
    self.clients.append(socket)
    while True:
      data = socket.recv(1024)
      if data:
        self.broadcast(data, socket)

  def broadcast(self, data, sender):
    for client in self.clients:
      if client != sender:
          client.send(data)

if __name__ == '__main__':
  server = Server()
  server.start_server()