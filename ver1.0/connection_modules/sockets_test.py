import socket

class SocketManager:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, send_ip, send_port, receive_ip, receive_port):
        try:
            self.sock.connect((send_ip, send_port))
        except Exception as e:
            print(e)



    def send(self, data):
        self.sock.sendall(data)

    def receive(self):
        return self.sock.recv(1024)

    def close(self):
        self.sock.close()