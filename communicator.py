import socket
import time

class Communicator:
    def __init__(self, host="localhost", port=1000):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host,port))
        name = "HumanAPI"
        self.s.send(name.encode() + b'\x00')

    def send_message(self, message):
        [X, Y, S] = message
        if X < 0 or X >= 640 or Y < 0 or Y >= 480:
            return

        payload = bytearray()
        payload.append(X >> 8 & 0xff)
        payload.append(X >> 0 & 0xff)
        payload.append(Y >> 8 & 0xff)
        payload.append(Y >> 0 & 0xff)
        payload.append(S & 0xff)
        self.s.send(payload)
        time.sleep(0.05)
