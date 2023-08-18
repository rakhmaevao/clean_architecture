from abc import ABC


class Message:
    def __init__(self, raw_message: list[str]) -> None:
        self.__content = "".join(raw_message)

    @property
    def content(self) -> str:
        return self.__content


class SomeInterface(ABC):
    pass
