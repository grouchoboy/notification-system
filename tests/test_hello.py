from notification_system import say_hello


def test_say_hello():
    assert "Hello Potter" == say_hello("Potter")
