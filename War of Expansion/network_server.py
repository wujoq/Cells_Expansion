import socket
import threading
import json
from PySide6.QtCore import QObject, Signal


class NetworkServer(QObject):
    move_received = Signal(dict)
    connected = Signal()

    def __init__(self, port=12345):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("::", port))
        self.sock.listen(1)
        self.client_conn = None
        self.thread = threading.Thread(target=self.wait_for_client, daemon=True)

    def start(self):
        self.thread.start()

    def wait_for_client(self):
        self.client_conn, _ = self.sock.accept()
        self.connected.emit()
        while True:
            try:
                data = self.client_conn.recv(4096)
                if not data:
                    break
                move = json.loads(data.decode())
                self.move_received.emit(move)
            except Exception as e:
                print(f"[Server] Connection error: {e}")
                break

    def send(self, move):
        try:
            if self.client_conn:
                self.client_conn.sendall(json.dumps(move).encode())
        except Exception as e:
            print(f"[Server] Send error: {e}")
