from random import randint, random

from faker import Faker

from notification_system.listeners import MessageReadListener
from notification_system.message_delivery import (
    DeliverySystem,
    FailureSimulator,
    PublishMessage,
)
from notification_system.models import MessageRepository, UserRepository

if __name__ == "__main__":
    Faker.seed(0)
    fake = Faker()

    user_repository = UserRepository()
    message_repository = MessageRepository()
    failure_simulator = FailureSimulator(0.1)
    publish_message = PublishMessage(
        user_repository, message_repository, failure_simulator
    )
    read_message_listener = MessageReadListener(user_repository, message_repository)
    delivery_system = DeliverySystem(
        user_repository, message_repository, publish_message
    )

    for i in range(0, 1000):
        delivery_system.register_user(fake.name())

    for i in range(0, 5):
        delivery_system.deliver_message(fake.sentence())

    for u in delivery_system.users:
        n = randint(0, 100)
        if n == 0 or n == 100:
            continue
        if n % 3 == 0:
            for item in u.inbox:
                u.read(item.message.id)
            continue

        probability = 0.4
        for item in u.inbox:
            r = random()
            if r > probability:
                u.read(item.message.id)

    for m in delivery_system.messages:
        print(f"Message: {m.id}")
        print(f"Body: {m.body}")
        print(m.stats)
        print()
