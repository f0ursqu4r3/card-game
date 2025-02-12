from typing import Protocol, Dict, Any, Tuple


class NetworkSerializable(Protocol):
    """Protocol for objects that can be serialized for network transmission."""

    def to_network_state(self) -> Dict[str, Any]:
        """Convert object to a network-friendly dictionary state."""
        ...

    @classmethod
    def from_network_state(cls, state: Dict[str, Any]) -> "NetworkSerializable":
        """Create an instance from a network state dictionary."""
        ...


class NetworkMessageHandler(Protocol):
    """Protocol for objects that can handle network messages."""

    def handle_game_state_update(self, state: Dict[str, Any]) -> None:
        """Handle incoming game state updates."""
        ...

    def handle_card_movement(
        self, card_id: str, position: Tuple[int, int, int]
    ) -> None:
        """Handle card movement updates."""
        ...

    def handle_card_flip(self, card_id: str, face_up: bool) -> None:
        """Handle card flip updates."""
        ...

    def handle_player_action(
        self, player_id: int, action_type: str, data: Dict[str, Any]
    ) -> None:
        """Handle player action updates."""
        ...


class NetworkManager(Protocol):
    """Protocol for network management functionality."""

    def send_game_state(self, state: Dict[str, Any]) -> None:
        """Send complete game state to other players."""
        ...

    def send_card_update(
        self, card_id: str, position: Tuple[int, int, int], state: Dict[str, Any]
    ) -> None:
        """Send card update to other players."""
        ...

    def broadcast_message(self, message_type: str, data: Dict[str, Any]) -> None:
        """Broadcast a message to all connected players."""
        ...

    def register_message_handler(self, handler: NetworkMessageHandler) -> None:
        """Register a handler for incoming network messages."""
        ...
