from mock import Mock


def test_keys_become_attributes():
    user = Mock({"id": 7, "name": "John", "surname": "Doe"})

    assert user.id == 7
    assert user.name == "John"
    assert user.surname == "Doe"


if __name__ == "__main__":
    test_keys_become_attributes()
