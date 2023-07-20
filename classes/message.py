from typing import Literal


class Message:
    def __init__(self, user_name: str, text: str, message_type: Literal["chat_message", "login_message"]):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type
