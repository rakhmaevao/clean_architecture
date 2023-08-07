from .message import Message


def parse_message(raw_str: str) -> Message:
    return Message(raw_str.split("."))
