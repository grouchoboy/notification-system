import pytest

from notification_system.events import Event, EventDispatcher


@pytest.fixture
def dispatcher():
    return EventDispatcher()


class ListenerDouble:
    def __init__(self):
        self.call = False

    def __call__(self, event: Event):
        self.call = True


def test_add_listener(dispatcher: EventDispatcher):
    listener = ListenerDouble()
    dispatcher.add_listener("example", listener)

    assert 1 == len(dispatcher.listeners["example"])


def test_dispatch_event(dispatcher: EventDispatcher):
    listener = ListenerDouble()
    dispatcher.add_listener("example", listener)
    dispatcher.dispatch(Event(name="example", data={}))
    assert listener.call
