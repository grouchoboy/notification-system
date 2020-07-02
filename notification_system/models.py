from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from notification_system.events import Event, dispatcher


class UserRepository:
    def __init__(self):
        self.items = []

    def find(self, id_: UUID) -> Optional["User"]:
        for u in self.items:
            if u.id == id_:
                return u
        return None

    def add(self, user: "User") -> "User":
        if self._exists(user.id):
            return user
        self.items.append(user)
        return user

    def _exists(self, user_id: UUID) -> bool:
        for u in self.items:
            if u.id == user_id:
                return True
        return False

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)


class MessageRepository:
    def __init__(self):
        self.items = []

    def find(self, id_: UUID) -> Optional["Message"]:
        for m in self.items:
            if m.id == id_:
                return m
        return None

    def add(self, message: "Message") -> "Message":
        self.items.append(message)
        return message

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)


MESSAGE_READ_EVENT = "READ_MESSAGE"


def _dispatch_message_read(message_id: UUID, user_id: UUID):
    dispatcher.dispatch(
        Event(
            name=MESSAGE_READ_EVENT, data={"message_id": message_id, "user_id": user_id}
        )
    )


MESSAGE_RECEIVED_EVENT = "MESSAGE_RECEIVED"


def _dispatch_message_received(message_id: UUID, user_id: UUID):
    dispatcher.dispatch(
        Event(
            name=MESSAGE_RECEIVED_EVENT,
            data={"message_id": message_id, "user_id": user_id},
        )
    )


class InboxItem:
    def __init__(self, message: "Message"):
        self.message = message
        self.read: bool = False


class Inbox:
    def __init__(self):
        self.items: List[InboxItem] = []

    def add(self, message: "Message"):
        self.items.append(InboxItem(message))

    def read(self, message_id: UUID) -> bool:
        for item in self.items:
            if item.message.id == message_id and not item.read:
                item.read = True
                return True
        return False

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, item):
        return self.items[item]

    def __iter__(self):
        return iter(self.items)


@dataclass
class User:
    name: str
    id: UUID
    inbox: Inbox = field(default_factory=Inbox)

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def receive(self, message: "Message"):
        self.inbox.add(message)
        _dispatch_message_received(message.id, self.id)

    def read(self, message_id: UUID):
        if self.inbox.read(message_id):
            _dispatch_message_read(message_id, self.id)


@dataclass
class Message:
    body: str
    id: UUID
    has_been_sent_to: List[User] = field(default_factory=list)
    has_been_received_by: List[User] = field(default_factory=list)
    has_been_opened_by: List[User] = field(default_factory=list)

    def sent_to(self, user: User):
        self.has_been_sent_to.append(user)

    def received_by(self, user: User):
        self.has_been_received_by.append(user)

    def opened_by(self, user: User):
        self.has_been_opened_by.append(user)

    @property
    def stats(self):
        times_sent = len(self.has_been_sent_to)
        times_received = len(self.has_been_received_by)
        times_opened = len(self.has_been_opened_by)

        return {
            "sent": times_sent,
            "received": times_received,
            "opened": times_opened,
            "received_ratio": str(
                Decimal(times_received / times_sent).quantize(Decimal("0.00"))
            ),
            "opened_ratio": str(
                Decimal(times_opened / times_received).quantize(Decimal("0.00"))
            ),
        }

    def __str__(self) -> str:
        return self.body

    def __eq__(self, other) -> bool:
        return self.id == other.id
