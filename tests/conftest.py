from uuid import uuid4

import pytest

from notification_system import message_delivery, models
from notification_system.listeners import MessageReadListener


@pytest.fixture
def user():
    return models.User(name="Harry", id=uuid4())


@pytest.fixture()
def message():
    return models.Message(body="Hello", id=uuid4())


@pytest.fixture
def user_repository():
    return models.UserRepository()


@pytest.fixture
def message_repository():
    return models.MessageRepository()


@pytest.fixture
def failure_simulator():
    return message_delivery.FailureSimulator(0)


@pytest.fixture
def publish_message(user_repository, message_repository, failure_simulator):
    return message_delivery.PublishMessage(
        user_repository, message_repository, failure_simulator
    )


@pytest.fixture
def listener(user_repository, message_repository):
    return MessageReadListener(user_repository, message_repository)
