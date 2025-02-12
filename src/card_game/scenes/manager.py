from __future__ import annotations

import pygame as pg

from card_game.events import EventType, EventTypeUnion
from card_game.scenes.scene import Scene


class SceneManager:
    def __init__(self, **scenes: dict[str, Scene]):
        self.scenes = scenes
        self.current_scene = None

    def add_scene(self, scene_name: str, scene: Scene):
        self.scenes[scene_name] = scene

    def set_scene(self, scene_name: str):
        self.current_scene = self.scenes[scene_name]

    def update(self, delta_time: float):
        self.current_scene.update(delta_time)

    def render(self, screen: pg.Surface):
        self.current_scene.render(screen)

    def handle_event(self, event: EventTypeUnion):
        if event.type == EventType.CHANGE_SCENE:
            return self.set_scene(event.scene_name)
        self.current_scene.handle_event(event)

    def on_enter(self):
        self.current_scene.on_enter()

    def on_exit(self):
        self.current_scene.on_exit()
