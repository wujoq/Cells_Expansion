import socket
import threading
import json
from PySide6.QtCore import QObject, Signal


class NetworkClient(QObject):
    move_received = Signal(dict)
    connected = Signal()

    def __init__(self, ip, port=12345):
        super().__init__()
        self.server_ip = ip
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.thread = threading.Thread(target=self.connect_to_server, daemon=True)

    def start(self):
        self.thread.start()

    def connect_to_server(self):
        try:
            self.sock.connect((self.server_ip, self.server_port))
            self.connected.emit()
            while True:
                data = self.sock.recv(4096)
                if not data:
                    break
                move = json.loads(data.decode())
                self.move_received.emit(move)
        except Exception as e:
            print(f"[Client] Connection error: {e}")

    def send(self, move):
        try:
            self.sock.sendall(json.dumps(move).encode())
        except Exception as e:
            print(f"[Client] Send error: {e}")
