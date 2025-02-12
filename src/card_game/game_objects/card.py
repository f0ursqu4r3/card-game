import pygame as pg

from card_game.game_objects.game_object import GameObject
from card_game.networking.protocol import NetworkSerializable


class Card(GameObject, NetworkSerializable):
    # Standard card dimensions and colors
    CARD_WIDTH = 42
    CARD_HEIGHT = 60
    CARD_COLOR = (255, 255, 255)
    BACK_COLOR = (40, 80, 160)
    SELECTED_COLOR = (255, 0, 0)
    RED_COLOR = (255, 0, 0)
    BLACK_COLOR = (0, 0, 0)
    FONT_SIZE = 24

    font = None

    def __init__(
        self,
        x: int,
        y: int,
        z: int,
        value: int,
        suit: str,
    ):
        super().__init__(
            object_id=z,
            x=x,
            y=y,
            z=z,
            width=self.CARD_WIDTH,
            height=self.CARD_HEIGHT,
            rotation=0,
            scale=1.0,
            visible=True,
            layer=0,
            parent=None,
        )
        self.value = value
        self.suit = suit
        self.face_up = False
        self.selected = False

        if Card.font is None:
            Card.font = pg.font.SysFont("Arial", self.FONT_SIZE)

    def update(self) -> None:
        pass

    def render(self, screen: pg.Surface) -> None:
        if not self.visible:
            return

        # Draw card rectangle
        color = self.CARD_COLOR if self.face_up else self.BACK_COLOR
        pg.draw.rect(screen, color, self.rect, 0, 4)
        pg.draw.rect(screen, (0, 0, 0), self.rect, 2, 4)  # Border

        if self.face_up:
            # Render card value and suit
            text = f"{self.value}{self.suit}"
            if self.suit in ["♥", "♦"]:
                text_color = self.RED_COLOR
            else:
                text_color = self.BLACK_COLOR
            text_surface = Card.font.render(text, True, text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def to_network_state(self) -> dict:
        return {
            "id": self.id,
            "position": (self.x, self.y, self.z),
            "value": self.value,
            "suit": self.suit,
            "face_up": self.face_up,
        }

    @classmethod
    def from_network_state(cls, state: dict) -> "Card":
        card = cls(
            x=state["position"][0],
            y=state["position"][1],
            z=state["position"][2],
            value=state["value"],
            suit=state["suit"],
        )
        card.face_up = state["face_up"]
        return card
