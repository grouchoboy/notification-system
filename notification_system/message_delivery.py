import random
from typing import Iterable
from uuid import uuid4

from notification_system.events import dispatcher
from notification_system.listeners import MessageReadListener, MessageReceivedListener
from notification_system.models import (
    MESSAGE_READ_EVENT,
    MESSAGE_RECEIVED_EVENT,
    Message,
    MessageRepository,
    User,
    UserRepository,
)


class FailureSimulator:
    def __init__(self, loss_ratio: float):
        self.loss_ratio = loss_ratio

    @property
    def is_fail(self) -> bool:
        return random.random() < self.loss_ratio


class PublishMessage:
    def __init__(
        self,
        user_repository: UserRepository,
        message_repository: MessageRepository,
        failure_simulator: FailureSimulator,
    ):
        self.failure_simulator = failure_simulator
        self.message_repository = message_repository
        self.user_repository = user_repository

    def __call__(self, message: Message) -> Message:
        self.message_repository.add(message)
        for user in self.user_repository:
            message.sent_to(user)
            if not self.failure_simulator.is_fail:
                user.receive(message)
        return message


class DeliverySystem:
    def __init__(
        self,
        user_repository: UserRepository,
        message_repository: MessageRepository,
        publish_message: PublishMessage,
    ):
        self._publish_message = publish_message
        self._message_repository = message_repository
        self._user_repository = user_repository
        listener_received = MessageReceivedListener(user_repository, message_repository)
        listener_read = MessageReadListener(user_repository, message_repository)

        dispatcher.add_listener(MESSAGE_RECEIVED_EVENT, listener_received)
        dispatcher.add_listener(MESSAGE_READ_EVENT, listener_read)

    def register_user(self, name: str) -> User:
        return self._user_repository.add(User(name=name, id=uuid4()))

    def deliver_message(self, body: str) -> Message:
        return self._publish_message(Message(body=body, id=uuid4()))

    @property
    def users(self) -> Iterable[User]:
        return self._user_repository.items

    @property
    def messages(self) -> Iterable[Message]:
        return self._message_repository.items
