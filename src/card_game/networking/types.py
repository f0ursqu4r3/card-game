from dataclasses import dataclass
from typing import Dict, Any, Tuple, List


@dataclass
class GameStateMessage:
    """Complete game state update message."""

    cards: List[Dict[str, Any]]
    game_phase: str
    active_player: int


@dataclass
class CardUpdateMessage:
    """Card state update message."""

    card_id: str
    position: Tuple[int, int, int]
    face_up: bool
    state: Dict[str, Any]


@dataclass
class PlayerActionMessage:
    """Player action message."""

    player_id: int
    action_type: str
    data: Dict[str, Any]


@dataclass
class ConnectionMessage:
    """Connection status message."""

    client_id: int
    status: str  # "connected" or "disconnected"


@dataclass
class ErrorMessage:
    """Error message."""

    error_type: str
    message: str
