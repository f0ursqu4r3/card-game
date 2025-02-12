from enum import IntEnum
import pygame as pg

from card_game.game_objects import Card


class EventType(IntEnum):
    PICKUP_CARD = pg.event.custom_type()
    DROP_CARD = pg.event.custom_type()
    PLAY_CARD = pg.event.custom_type()
    END_TURN = pg.event.custom_type()
    CHANGE_SCENE = pg.event.custom_type()
    QUIT = pg.event.custom_type()


EventTypeUnion = EventType | pg.event.Event


class Event:
    def __init__(self, event_type: EventType, **kwargs):
        self.type = event_type
        self._dict = kwargs

    def post(self):
        event = pg.event.Event(self.type, **self._dict)
        pg.event.post(event)


class PickupCardEvent(Event):
    def __init__(self, card: Card):
        super().__init__(EventType.PICKUP_CARD, card=card)


class DropCardEvent(Event):
    def __init__(self, card: Card):
        super().__init__(EventType.DROP_CARD, card=card)


class PlayCardEvent(Event):
    def __init__(self, card: Card):
        super().__init__(EventType.PLAY_CARD, card=card)


class EndTurnEvent(Event):
    def __init__(self):
        super().__init__(EventType.END_TURN)


class ChangeSceneEvent(Event):
    def __init__(self, scene_name: str):
        super().__init__(EventType.CHANGE_SCENE, scene_name=scene_name)
