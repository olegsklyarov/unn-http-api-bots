from mock import Mock


def test_callable_via_lambda():
    obj = Mock({
        "greet": lambda name: f"Hello, {name}",
    })

    assert obj.greet("Alice") == "Hello, Alice"


def test_callable_via_def():
    def add(a: int, b: int) -> int:
        return a + b

    obj = Mock({
        "add": add,
    })

    assert obj.add(2, 3) == 5


if __name__ == "__main__":
    test_callable_via_lambda()
    test_callable_via_def()

