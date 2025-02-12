import pygame as pg

from card_game.events import ChangeSceneEvent, EventTypeUnion
from card_game.scenes.scene import Scene


class PauseMenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.buttons = [
            {
                "text": "Resume",
                "rect": pg.Rect(220, 140, 200, 50),
                "action": self.resume_game,
            },
            {
                "text": "Options",
                "rect": pg.Rect(220, 220, 200, 50),
                "action": self.open_options,
            },
            {
                "text": "Main Menu",
                "rect": pg.Rect(220, 300, 200, 50),
                "action": self.return_to_main_menu,
            },
        ]
        self.font = pg.font.Font(None, 36)
        self.selected = None
        self.overlay = pg.Surface((640, 480))  # Match window size
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(128)  # Semi-transparent overlay

    def resume_game(self):
        ChangeSceneEvent("game").post()

    def open_options(self):
        print("Open options")  # Implement options menu logic

    def return_to_main_menu(self):
        ChangeSceneEvent("main_menu").post()

    def update(self, delta_time: float):
        mouse_pos = pg.mouse.get_pos()
        self.selected = None

        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                self.selected = button

    def handle_event(self, event: EventTypeUnion):
        if event.type == pg.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    button["action"]()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.resume_game()

    def render(self, screen: pg.Surface):
        # Draw semi-transparent overlay
        screen.blit(self.overlay, (0, 0))

        # Draw "PAUSED" text
        pause_text = self.font.render("PAUSED", True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(320, 80))
        screen.blit(pause_text, text_rect)

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
