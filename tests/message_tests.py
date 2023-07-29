import unittest
from classes.message import Message


class MessageTests(unittest.TestCase):

    def test_user_name(self):
        message = Message("user_name", "text_message", "chat_message")

        self.assertEqual(message.user_name, "user_name")
        self.assertNotEqual(message.user_name, "name")

    def test_text(self):
        message = Message("user_name", "text_message", "chat_message")

        self.assertEqual(message.text, "text_message")
        self.assertNotEqual(message.text, "text")

    def test_login_message(self):
        message = Message("user_name", "text_message", "login_message")
        self.assertEqual(message.message_type, "login_message")
        self.assertNotEqual(message.message_type, "chat_message")

    def test_chat_message(self):
        message = Message("user_name", "text_message", "chat_message")
        self.assertEqual(message.message_type, "chat_message")
        self.assertNotEqual(message.message_type, "login_message")

if __name__ == '__main__':
    unittest.main()
