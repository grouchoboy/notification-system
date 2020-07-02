from notification_system.message_delivery import PublishMessage
from notification_system.models import Message, User, UserRepository


def test_publish_message(
    user_repository: UserRepository,
    publish_message: PublishMessage,
    user: User,
    message: Message,
):
    user_repository.add(user)
    publish_message(message)
    for user in user_repository:
        assert 1 == len(user.inbox)
        assert 1 == len(message.has_been_sent_to)
        assert 0 == len(message.has_been_received_by)
        assert 0 == len(message.has_been_opened_by)
