from abc import ABC, abstractmethod
from typing import Optional

import pygame as pg


class GameObject(ABC):
    """Base class for all game objects in the tabletop card game."""

    def __init__(
        self,
        object_id: int,
        x: int,
        y: int,
        z: int,
        width: int,
        height: int,
        rotation: int,
        scale: float,
        visible: bool,
        layer: int,
        parent: Optional["GameObject"] = None,
    ):
        """
        Initialize a new game object.

        Args:
            x (int): X-coordinate position
            y (int): Y-coordinate position
            z (int): Z-coordinate position
        """
        self.id = object_id
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.rotation = rotation
        self.scale = scale
        self.visible = visible
        self.layer = layer
        self.parent = parent

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(
            self.x, self.y, self.width * self.scale, self.height * self.scale
        )

    def move(self, dx: int, dy: int, dz: int) -> None:
        """
        Move the object by the given amount.

        Args:
            dx (int): Amount to move in x direction
            dy (int): Amount to move in y direction
            dz (int): Amount to move in z direction
        """
        self.x = self.x + dx
        self.y = self.y + dy
        self.z = self.z + dz

    @property
    def position(self) -> tuple[int, int, int]:
        """
        Get the current position of the object.

        Returns:
            tuple[int, int, int]: Current (x, y, z) coordinates
        """
        return (self.x, self.y, self.z)

    @abstractmethod
    def update(self) -> None:
        """Update the game object's state. Must be implemented by derived classes."""
        pass
