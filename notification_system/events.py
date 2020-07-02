from dataclasses import dataclass
from typing import Callable


class EventDispatcher:
    def __init__(self):
        self.listeners = {}

    def add_listener(self, event_name, listener: Callable):
        listeners = self.listeners.get(event_name, [])
        listeners.append(listener)
        self.listeners[event_name] = listeners

    def dispatch(self, event: "Event"):
        listeners = self.listeners.get(event.name, [])
        for listener in listeners:
            listener(event)


dispatcher = EventDispatcher()


@dataclass
class Event:
    name: str
    data: dict
