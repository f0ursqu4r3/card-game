import pygame as pg

from card_game.events import EventTypeUnion, ChangeSceneEvent
from card_game.game_objects import Card
from card_game.scenes.scene import Scene
from card_game.networking import (
    NetworkMessageHandler,
    GameStateMessage,
    CardUpdateMessage,
    PlayerActionMessage,
    ConnectionMessage,
    ErrorMessage,
)


class GameScene(Scene, NetworkMessageHandler):
    def __init__(self):
        super().__init__()
        self.cards = []
        self.selected_card = None
        self.setup_initial_cards()

    def setup_initial_cards(self):
        # Create a few test cards
        suits = ["♠", "♥", "♦", "♣"]
        values = [2, 3, 4, 5]  # Just a few cards for testing

        x, y = 10, 10
        for suit in suits:
            for value in values:
                card = Card(x, y, len(self.cards), value, suit)
                card.face_up = True  # Make cards visible for testing
                self.cards.append(card)
                x += 42  # Offset each card horizontally
            x = 10  # Reset x position for next row
            y += 60  # Move to next row

    def handle_event(self, event: EventTypeUnion):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()

            # Check for card clicks (in reverse order to select top card first)
            for card in reversed(self.cards):
                card_rect = pg.Rect(card.x, card.y, card.width, card.height)
                if card_rect.collidepoint(mouse_pos):
                    if event.button == 1:  # Left click
                        self.selected_card = card
                    elif event.button == 3:  # Right click
                        card.face_up = not card.face_up
                    break

        elif event.type == pg.MOUSEBUTTONUP:
            self.selected_card = None

        elif event.type == pg.MOUSEMOTION and self.selected_card:
            # Move the selected card with the mouse
            dx, dy = event.rel
            self.selected_card.move(dx, dy, 0)

        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            ChangeSceneEvent("pause").post()

    def update(self, delta_time: float):
        # Add any game logic updates here
        pass

    def render(self, screen: pg.Surface):
        screen.fill((34, 139, 34))  # Green felt table color
        pg.display.set_caption("Retro Card Table - Game")

        # Render all cards
        for card in self.cards:
            card.render(screen)

        pg.display.flip()

    def handle_game_state_update(self, state: GameStateMessage):
        """Handle complete game state updates from the server."""
        # Clear existing cards
        self.cards.clear()

        # Recreate cards from network state
        for card_state in state.cards:
            card = Card.from_network_state(card_state)
            self.cards.append(card)

    def handle_card_update(self, message: CardUpdateMessage):
        """Handle updates for individual card movements/states."""
        # Find the card with matching ID
        for card in self.cards:
            if card.id == message.card_id:
                # Update card position
                card.x, card.y, card.z = message.position
                # Update other card properties
                card.face_up = message.face_up
                break

    def handle_player_action(self, message: PlayerActionMessage):
        """Handle actions performed by other players."""
        if message.action_type == "card_move":
            # Handle card movement
            card_id = message.data["card_id"]
            new_pos = message.data["position"]
            for card in self.cards:
                if card.id == card_id:
                    card.x, card.y, card.z = new_pos
                    break
        elif message.action_type == "card_flip":
            # Handle card flipping
            card_id = message.data["card_id"]
            face_up = message.data["face_up"]
            for card in self.cards:
                if card.id == card_id:
                    card.face_up = face_up
                    break

    def handle_connection_message(self, message: ConnectionMessage):
        """Handle player connection/disconnection messages."""
        if message.event_type == "player_joined":
            print(f"Player {message.player_id} joined the game")
        elif message.event_type == "player_left":
            print(f"Player {message.player_id} left the game")

    def handle_error_message(self, message: ErrorMessage):
        """Handle error messages from the server."""
        print(f"Network Error: {message.error_type} - {message.error_message}")
        # Could trigger UI feedback here, like a popup message
