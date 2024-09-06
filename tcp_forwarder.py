import socket
import threading

class TCPForwarder:
    def __init__(self, host='0.0.0.0', port=10113):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_sockets = []
        self.running = False

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        print(f"TCP server listening on {self.host}:{self.port}")

        accept_thread = threading.Thread(target=self.accept_connections)
        accept_thread.start()

    def accept_connections(self):
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f"New connection from {addr}")
                self.client_sockets.append(client_socket)
            except Exception as e:
                if self.running:
                    print(f"Error accepting connection: {e}")

    def send_data(self, data):
        if self.running:
            disconnected_clients = []
            for client_socket in self.client_sockets:
                try:
                    client_socket.sendall(data)
                except socket.error:
                    disconnected_clients.append(client_socket)

            for client_socket in disconnected_clients:
                self.client_sockets.remove(client_socket)
                client_socket.close()

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        for client_socket in self.client_sockets:
            client_socket.close()
        self.client_sockets.clear()
        print("TCP server stopped")
