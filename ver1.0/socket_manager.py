import socket
import struct
import threading

BUFFER_SIZE_FILE = 1024*32

class SocketManager:
    def __init__(self, conversation_handler, address, port, receive_callback):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.port = port

        self.conversation_handler = conversation_handler
        self.receive_callback = receive_callback

        self.conn = None
        self.listening_thread = None
        self.receiving_thread = None
        self.lock = threading.Lock()

    def connect(self):
        self.log("Connecting to " + self.address + ":" + str(self.port))
        try:
            self.sock.connect((self.address, self.port))
            self.conn = self.sock
            self.log("Connected to " + str(self.address) + ":" + str(self.port))
            self.receiving_thread = threading.Thread(target=self.thread_receive)
            self.receiving_thread.start()
        except Exception as e:
            print(e)

    def listen(self):
        self.sock.bind((self.address, self.port))
        self.sock.listen(1)
        self.log("Listening on " + str(self.address) + ":" + str(self.port))
        listen_thread = threading.Thread(target=self.thread_listen)
        listen_thread.start()

    def thread_listen(self):
        self.lock.acquire()
        self.conn, address = self.sock.accept()
        self.log("Accepted connection from " + str(address))
        self.lock.release()
        self.receiving_thread = threading.Thread(target=self.thread_receive)
        self.receiving_thread.start()


    def send_text(self, data=""):
        send_thread = threading.Thread(target=self.thread_send_text, args=(data,))
        send_thread.start()

    def send_file(self, file, message):
        send_thread = threading.Thread(target=self.thread_send_file, args=(file, message))
        send_thread.start()


    def thread_send_text(self, text):
        self.update_conn()
        self.log("Sending text message")
        packet_type = b't'
        packet_len = struct.pack('H', len(text))
        packet_data = text.encode()
        packet = packet_type + packet_len + packet_data
        self.conn.sendall(packet)

    def thread_send_file(self, data, message):
        self.update_conn()
        self.log("Sending file")

        packet_type = b'f'
        packet_len = struct.pack('I', len(data))
        self.log("File length: " + str(len(data)))
        packet = packet_type + packet_len
        self.conn.sendall(packet)

        message.set_progressbar()
        total_sent = 0

        while total_sent < len(data):
            sent = self.sock.send(data[total_sent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            total_sent = total_sent + sent
            # update the progress bar
            message.set_progressbar_value(sent/len(data))

        message.finish_progressbar()

    def thread_receive(self):
        self.lock.acquire()
        self.conn = self.conn
        self.lock.release()

        while True:
            mess_type = self.conn.recv(1)
            if not mess_type:
                pass
            if mess_type == b't':
                self.thread_receive_text()

            elif mess_type == b'f':
                self.thread_receive_file()

            elif mess_type == b'x':
                self.log("Received exit message")
                break
            else:
                pass
        return

    def thread_receive_text(self):
        self.log("Message type: text")

        mess_len_raw = self.conn.recv(2)
        mess_len = struct.unpack('H', mess_len_raw)[0]
        self.log("Message length: " + str(mess_len))

        mess_data = self.conn.recv(mess_len).decode()

        self.log("Message data: " + str(mess_data))
        self.receive_callback('t', mess_data)

    def thread_receive_file(self):
        self.log("Received file")

        mess_len_raw = self.conn.recv(4)
        mess_len = struct.unpack('I', mess_len_raw)[0]
        self.log("File length: " + str(mess_len))

        message = self.receive_callback('f', mess_len)
        message.set_progressbar()
        chunks = []
        bytes_recd = 0

        while bytes_recd < mess_len:
            chunk = self.conn.recv(min(mess_len - bytes_recd, BUFFER_SIZE_FILE))
            if not chunk:
                break

            chunks.append(chunk)
            message.set_progressbar_value(bytes_recd/mess_len)
            bytes_recd = bytes_recd + len(chunk)

        self.log("File received")
        message.file = b''.join(chunks)
        message.finish_progressbar()



    def update_conn(self):
        self.lock.acquire()
        self.conn = self.conn
        self.lock.release()

    def log(self, text):
        self.conversation_handler.log(text)