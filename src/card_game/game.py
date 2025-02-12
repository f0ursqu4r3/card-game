import pygame as pg
import sys

from card_game.scenes import SceneManager, MainMenuScene, GameScene, PauseMenuScene


# Constants
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 60
FIXED_UPDATE_FPS = 50  # For physics/logic updates


# Game state class
class Game:
    def __init__(self):
        # Initialize Pygame
        pg.init()

        self.clock = pg.time.Clock()
        self.is_running = True
        self.fixed_time_step = 1000 / FIXED_UPDATE_FPS  # in milliseconds
        self.accumulated_time = 0

        # Setup display
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption("Retro Card Table")

        self.scene_manager = SceneManager(
            main_menu=MainMenuScene(),
            game=GameScene(),
            pause=PauseMenuScene(),
        )

        self.scene_manager.set_scene("game")

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
            self.scene_manager.handle_event(event)

    def fixed_update(self):
        # Update game logic/physics here
        # This runs at a fixed time step (20ms by default)
        pass

    def update(self, dt: float):
        self.scene_manager.update(dt)

    def render(self):
        # Clear screen
        self.screen.fill((0, 0, 0))  # Black background

        # Add rendering code here
        self.scene_manager.render(self.screen)

        # Flip display
        pg.display.flip()

    def run(self):
        prev_time = pg.time.get_ticks()

        while self.is_running:
            # Calculate delta time
            current_time = pg.time.get_ticks()
            delta_time = current_time - prev_time
            prev_time = current_time

            # Accumulate time for fixed updates
            self.accumulated_time += delta_time

            # Handle events
            self.handle_events()

            # Fixed update loop
            while self.accumulated_time >= self.fixed_time_step:
                self.fixed_update()
                self.accumulated_time -= self.fixed_time_step

            # Regular update
            self.update(delta_time / 1000.0)  # Convert to seconds

            # Render
            self.render()

            # Cap the frame rate
            self.clock.tick(FPS)

        # Cleanup
        pg.quit()
        sys.exit()

    def sync_game_state(self):
        state = {
            "cards": [card.to_network_state() for card in self.cards],
            "game_phase": self.current_phase,
            "active_player": self.active_player,
        }
        self.network_manager.send_game_state(state)
