from abc import ABC, abstractmethod

import pygame as pg

from card_game.events import EventTypeUnion


class Scene(ABC):
    """Abstract base class for game scenes."""

    def __init__(self) -> None:
        """Initialize the scene."""
        super().__init__()

    def on_enter(self) -> None:
        """Called when the scene becomes active."""
        return

    def on_exit(self) -> None:
        """Called when the scene becomes inactive."""
        return

    def handle_event(self, event: EventTypeUnion) -> None:
        """Handle pygame events.

        Args:
            event: The pygame event to process
        """
        return

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Update the scene state.

        Args:
            delta_time: Time elapsed since last update in seconds
        """
        pass

    @abstractmethod
    def render(self, screen: pg.Surface) -> None:
        """Render the scene.

        Args:
            screen: The pygame surface to render to
        """
        pass
