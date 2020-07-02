from notification_system.events import Event
from notification_system.listeners import MessageReadListener, MessageReceivedListener
from notification_system.models import Message, MessageRepository, User, UserRepository


def test_message_received_listener(
    user_repository: UserRepository,
    message_repository: MessageRepository,
    user: User,
    message: Message,
):
    user_repository.add(user)
    message_repository.add(message)

    listener = MessageReceivedListener(user_repository, message_repository)
    event = Event(name="RECEIVED", data={"message_id": message.id, "user_id": user.id})

    assert 0 == len(message.has_been_received_by)
    listener(event)

    assert 1 == len(message.has_been_received_by)
    assert user in message.has_been_received_by


def test_do_nothing_if_received_message_does_not_exists(
    user_repository: UserRepository,
    message_repository: MessageRepository,
    user: User,
    message: Message,
):
    user_repository.add(user)

    listener = MessageReceivedListener(user_repository, message_repository)
    event = Event(name="RECEIVED", data={"message_id": message.id, "user_id": user.id})

    listener(event)
    assert 0 == len(message.has_been_received_by)


def test_do_nothing_if_user_does_not_exist_while_receiving_a_message(
    user_repository: UserRepository,
    message_repository: MessageRepository,
    user: User,
    message: Message,
):
    message_repository.add(message)

    listener = MessageReceivedListener(user_repository, message_repository)
    event = Event(name="RECEIVED", data={"message_id": message.id, "user_id": user.id})

    listener(event)
    assert 0 == len(message.has_been_received_by)


def test_message_read_listener(
    user_repository: UserRepository,
    message_repository: MessageRepository,
    user: User,
    message: Message,
):
    user_repository.add(user)
    message_repository.add(message)

    listener = MessageReadListener(user_repository, message_repository)
    event = Event(name="READ", data={"message_id": message.id, "user_id": user.id})

    assert 0 == len(message.has_been_opened_by)
    listener(event)

    assert 1 == len(message.has_been_opened_by)
    assert user in message.has_been_opened_by


def test_do_nothing_if_the_message_does_not_exist(
    user_repository: UserRepository,
    message_repository: MessageRepository,
    user: User,
    message: Message,
):
    user_repository.add(user)
    listener = MessageReadListener(user_repository, message_repository)
    event = Event(name="READ", data={"message_id": message.id, "user_id": user.id})

    listener(event)

    assert 0 == len(message.has_been_opened_by)


def test_do_nothing_if_the_user_does_not_exist(
    user_repository: UserRepository,
    message_repository: MessageRepository,
    user: User,
    message: Message,
):
    message_repository.add(message)
    listener = MessageReadListener(user_repository, message_repository)
    event = Event(name="READ", data={"message_id": message.id, "user_id": user.id})

    listener(event)

    assert 0 == len(message.has_been_opened_by)
