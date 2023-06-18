import socket
import time
import threading
import struct

class NetworkManager:
    def __init__(self, name):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = name
        self.log("Im " + self.name)
        self.port = 5001

    def connect(self, peer_ip, peer_port):
        self.log("Connecting to " + peer_ip + ":" + str(peer_port))
        try:
            self.sock.connect((peer_ip, peer_port))
            self.log("Connected to " + str(peer_ip) + ":" + str(peer_port))
        except Exception as e:
            print(e)

    def listen(self, addr, port):
        self.sock.bind((addr, port))
        self.sock.listen(1)
        self.log("Listening on " + str(addr) + ":" + str(port))
        while True:
            self.conn, address = self.sock.accept()
            self.log("Accepted connection from " + str(address))
            break

    def send(self, data_type, data=""):
        self.log("Sending data")
        if data_type == 't':
            self.log("Sending text message")
            packet_type = b't'                                  # t for text
            packet_len = struct.pack('H', len(data))
            packet_data = data.encode()
            packet = packet_type + packet_len + packet_data
            self.sock.sendall(packet)
        elif data_type == 'f':
            self.log("Sending file")
            self.sock.sendall(b'f')
        elif data_type == 'x':
            self.log("Sending exit message")
            self.sock.sendall(b'x')
        return


        # total_sent = 0
        # while total_sent < len(data):
        #     sent = self.sock.send(data[total_sent:])
        #     if sent == 0:
        #         raise RuntimeError("socket connection broken")
        #     total_sent = total_sent + sent

    def receive(self):
        while True:
            mess_type = self.conn.recv(1)
            #self.log("Received message type: " + str(mess_type))
            if not mess_type:
                pass
                #self.log("Connection lost")
            if mess_type == b't':
                self.log("Message type: text")

                mess_len_raw = self.conn.recv(2)
                mess_len = struct.unpack('H', mess_len_raw)[0]
                self.log("Message length: " + str(mess_len))

                mess_data = self.conn.recv(mess_len).decode()

                self.log("Message data: " + str(mess_data))

            elif mess_type == b'f':
                self.log("Received file")
            elif mess_type == b'p':
                self.log("Received picture")
            elif mess_type == b'x':
                self.log("Received exit message")
                break
            else:
                pass
                #self.log("Received unknown message type")
        return

    def log(self, message):
        print(self.name + ": " + message)

if __name__ == "__main__":
    network_manager1 = NetworkManager("ALICE")
    network_manager2 = NetworkManager("BOB  ")

    listening_thread = threading.Thread(target=network_manager1.listen, args=('127.0.0.1', 5001))
    listening_thread.start()

    time.sleep(0.5)

    network_manager2.connect('127.0.0.1', 5001)
    listening_thread.join()


    receiving_thread1 = threading.Thread(target=network_manager1.receive)
    receiving_thread2 = threading.Thread(target=network_manager2.receive)
    #receiving_thread1.start()
    receiving_thread2.start()

    time.sleep(0.5)

    network_manager1.send('t')
    #network_manager2.send(b't')

    #receiving_thread1.join()
    receiving_thread2.join()





    #menu_choice = input("1: listen on 5001\n2: connect to 5001\n")
    # if menu_choice == '1':
    #     network_manager.listen(5001)
    # else:
    #     network_manager.connect('localhost', 5001)
