import pygame as pg

from card_game.events import ChangeSceneEvent, EventTypeUnion
from card_game.scenes.scene import Scene


class MainMenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.buttons = [
            {
                "text": "Play Game",
                "rect": pg.Rect(100, 100, 200, 50),
                "action": self.start_game,
            },
            {
                "text": "Options",
                "rect": pg.Rect(100, 200, 200, 50),
                "action": self.open_options,
            },
            {
                "text": "Quit",
                "rect": pg.Rect(100, 300, 200, 50),
                "action": self.quit_game,
            },
        ]
        self.font = pg.font.Font(None, 36)  # Default font, size 36
        self.selected = None

    def start_game(self):
        print("Start game")  # Replace with actual game start logic
        ChangeSceneEvent("game").post()

    def open_options(self):
        print("Open options")  # Replace with options menu logic

    def quit_game(self):
        pg.quit()
        exit()

    def update(self, delta_time: float):
        mouse_pos = pg.mouse.get_pos()
        self.selected = None

        # Check for button hover
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                self.selected = button

    def handle_event(self, event: EventTypeUnion):
        if event.type == pg.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    button["action"]()

    def render(self, screen: pg.Surface):
        screen.fill((40, 40, 40))  # Dark gray background
        pg.display.set_caption("Retro Card Table - Main Menu")

        for button in self.buttons:
            # Draw button background
            color = (100, 100, 100) if button == self.selected else (70, 70, 70)
            pg.draw.rect(screen, color, button["rect"])

            # Draw button border
            pg.draw.rect(screen, (200, 200, 200), button["rect"], 2)

            # Render button text
            text = self.font.render(button["text"], True, (255, 255, 255))
            text_rect = text.get_rect(center=button["rect"].center)
            screen.blit(text, text_rect)

        pg.display.flip()
