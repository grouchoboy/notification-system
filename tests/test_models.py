from uuid import uuid4

from notification_system.models import Message, User, UserRepository


def test_add_user(user_repository: UserRepository):
    harry = User(name="Harry", id=uuid4())
    result = user_repository.add(harry)
    assert 1 == len(user_repository)
    assert harry.id is not None
    assert result.id is not None
    assert result.name == "Harry"


def test_attempt_to_register_registered_user_does_nothing(
    user_repository: UserRepository, user: User
):
    user_repository.add(user)
    assert 1 == len(user_repository)
    user_repository.add(user)
    assert 1 == len(user_repository)


def test_read_message(user: User, message: Message):
    user.inbox.add(message)
    if message.id is not None:
        user.read(message.id)
    assert user.inbox[0].read


def test_message_stats(message: Message):
    for i in range(0, 10):
        message.sent_to(User(name="", id=uuid4()))
    for i in range(0, 8):
        message.received_by(User(name="", id=uuid4()))
    for i in range(0, 4):
        message.opened_by(User(name="", id=uuid4()))

    stats = message.stats
    assert 10 == stats["sent"]
    assert 8 == stats["received"]
    assert "0.80" == stats["received_ratio"]
    assert 4 == stats["opened"]
    assert "0.50" == stats["opened_ratio"]
