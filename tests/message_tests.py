import unittest
from classes.message import Message


class MessageTests(unittest.TestCase):

    def test_username(self):
        message = Message("user_name", "text_message", "chat_message")

        self.assertEqual(message.user_name, "user_name")
        self.assertNotEqual(message.user_name, "name")

    def test_text(self):
        message = Message("user_name", "text_message", "chat_message")

        self.assertEqual(message.text, "text_message")
        self.assertNotEqual(message.text, "text")

    def test_message_type(self):
        message1 = Message("user_name", "text_message", "chat_message")

        self.assertEqual(message1.message_type, "chat_message")
        self.assertNotEqual(message1.message_type, "login_message")

        message2 = Message("user_name", "text_message", "login_message")

        self.assertEqual(message2.message_type, "login_message")
        self.assertNotEqual(message2.message_type, "chat_message")


if __name__ == '__main__':
    unittest.main()
