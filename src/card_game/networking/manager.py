import pickle
import socket
import threading
from typing import Any, Callable, Dict

from card_game.networking.protocol import NetworkManager as BaseNetworkManager


class NetworkManager(BaseNetworkManager):
    def __init__(self, host: str = "localhost", port: int = 5555):
        self.host = host
        self.port = port
        self.socket = None
        self.clients = {}  # For server: client_id -> connection
        self.handlers: Dict[str, Callable] = {}
        self.is_server = False
        self.client_id = None

    def start_server(self):
        """Initialize and start the game server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.is_server = True

        # Start accepting clients in a separate thread
        threading.Thread(target=self._accept_clients, daemon=True).start()

    def start_client(self):
        """Initialize and connect client to server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.is_server = False

        # Start receiving messages in a separate thread
        threading.Thread(target=self._receive_messages, daemon=True).start()

    def _accept_clients(self):
        """Accept incoming client connections"""
        while True:
            client_socket, address = self.socket.accept()
            client_id = len(self.clients)
            self.clients[client_id] = client_socket

            # Send client their ID
            self._send_to_client(
                client_socket,
                {"type": "connection_established", "client_id": client_id},
            )

            # Start a thread to handle this client's messages
            threading.Thread(
                target=self._handle_client, args=(client_socket, client_id), daemon=True
            ).start()

    def _handle_client(self, client_socket: socket.socket, client_id: int):
        """Handle messages from a specific client"""
        while True:
            try:
                data = self._receive_from_client(client_socket)
                if data:
                    # Process the message and broadcast to other clients
                    self._broadcast(data, exclude_client=client_id)
            except Exception as e:
                print(f"Error handling client {client_id}: {e}")
                # Client disconnected
                del self.clients[client_id]
                break

    def _receive_messages(self):
        """Receive messages for client"""
        while True:
            try:
                data = self._receive_from_server()
                if data.get("type") == "connection_established":
                    self.client_id = data.get("client_id")
                else:
                    self._handle_message(data)
            except Exception as e:
                print(f"Error receiving messages: {e}")
                # Server disconnected
                break

    def _handle_message(self, data: Dict[str, Any]):
        """Process received messages based on their type"""
        msg_type = data.get("type")
        if msg_type in self.handlers:
            self.handlers[msg_type](data)

    def register_handler(self, msg_type: str, handler: Callable):
        """Register a callback for a specific message type"""
        self.handlers[msg_type] = handler

    def send_game_object_update(
        self, game_object_id: str, position: tuple, state: Dict[str, Any]
    ):
        """Send game object updates to other players"""
        message = {
            "type": "game_object_update",
            "object_id": game_object_id,
            "position": position,
            "state": state,
        }
        self._send_message(message)

    def _send_message(self, message: Dict[str, Any]):
        """Send a message to the server or broadcast to clients"""
        if self.is_server:
            self._broadcast(message)
        else:
            self._send_to_server(message)

    def _broadcast(self, message: Dict[str, Any], exclude_client: int = None):
        """Broadcast message to all connected clients"""
        for client_id, client_socket in self.clients.items():
            if client_id != exclude_client:
                self._send_to_client(client_socket, message)

    def _send_to_client(self, client_socket: socket.socket, data: Dict[str, Any]):
        """Send data to a specific client"""
        serialized_data = pickle.dumps(data)
        client_socket.send(serialized_data)

    def _send_to_server(self, data: Dict[str, Any]):
        """Send data to the server"""
        serialized_data = pickle.dumps(data)
        self.socket.send(serialized_data)

    def _receive_from_client(self, client_socket: socket.socket) -> Dict[str, Any]:
        """Receive data from a specific client"""
        data = client_socket.recv(4096)
        return pickle.loads(data) if data else None

    def _receive_from_server(self) -> Dict[str, Any]:
        """Receive data from the server"""
        data = self.socket.recv(4096)
        return pickle.loads(data) if data else None
