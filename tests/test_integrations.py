from notification_system.listeners import MessageReadListener
from notification_system.message_delivery import DeliverySystem, PublishMessage
from notification_system.models import MessageRepository, UserRepository


def test_register_users_and_publish_messages(
    user_repository: UserRepository,
    message_repository: MessageRepository,
    publish_message: PublishMessage,
    listener: MessageReadListener,
):
    delivery_system = DeliverySystem(
        user_repository, message_repository, publish_message
    )
    user = delivery_system.register_user("Harry")
    user2 = delivery_system.register_user("Moon")
    message = delivery_system.deliver_message("This is a test")

    assert 2 == len(message.has_been_sent_to)
    assert 2 == len(message.has_been_received_by)
    assert 0 == len(message.has_been_opened_by)

    assert message.id is not None
    user.read(message.id)
    assert 1 == len(message.has_been_opened_by)
    assert user in message.has_been_opened_by

    user2.read(message.id)
    assert 2 == len(message.has_been_opened_by)
    assert user2 in message.has_been_opened_by
