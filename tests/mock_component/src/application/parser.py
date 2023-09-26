from src.application.message import Message
from src.application import models


some_variable = "asdf"


def parse_message(raw_str: str) -> Message:
    return Message(raw_str.split("."))


def get_model():
    return models.SomeModel()
