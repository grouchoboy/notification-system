from notification_system.events import Event
from notification_system.models import MessageRepository, UserRepository


class MessageReadListener:
    def __init__(
        self, user_repository: UserRepository, message_repository: MessageRepository
    ):
        self.message_repository = message_repository
        self.user_repository = user_repository

    def __call__(self, event: Event):
        message = self.message_repository.find(event.data["message_id"])
        if message is None:
            return
        user = self.user_repository.find(event.data["user_id"])
        if user is None:
            return
        message.opened_by(user)


class MessageReceivedListener:
    def __init__(
        self, user_repository: UserRepository, message_repository: MessageRepository
    ):
        self.message_repository = message_repository
        self.user_repository = user_repository

    def __call__(self, event: Event):
        message = self.message_repository.find(event.data["message_id"])
        if message is None:
            return
        user = self.user_repository.find(event.data["user_id"])
        if user is None:
            return
        message.received_by(user)
