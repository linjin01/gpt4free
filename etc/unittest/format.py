import unittest

from g4f.providers.helper import format_alternating_prompt


class TestFormatAlternatingPrompt(unittest.TestCase):

    def test_empty_messages(self):
        self.assertEqual(format_alternating_prompt([]), [{"role": "user", "content": ""}])

    def test_single_user_message(self):
        messages = [{"role": "user", "content": "Hello"}]
        expected = [{"role": "user", "content": "Hello"}]
        self.assertEqual(format_alternating_prompt(messages), expected)

    def test_single_assistant_message(self):
        messages = [{"role": "assistant", "content": "Hi"}]
        expected = [{"role": "user", "content": ""}, {"role": "assistant", "content": "Hi"},
                    {"role": "user", "content": ""}]
        self.assertEqual(format_alternating_prompt(messages), expected)

    def test_alternating_messages(self):
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
            {"role": "user", "content": "How are you?"},
        ]
        expected = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
            {"role": "user", "content": "How are you?"},
        ]
        self.assertEqual(format_alternating_prompt(messages), expected)

    def test_consecutive_messages_same_role(self):
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "user", "content": "How are you?"},
            {"role": "assistant", "content": "Hi"},
            {"role": "assistant", "content": "I'm good"},
        ]
        expected = [
            {"role": "user", "content": "Hello\nHow are you?"},
            {"role": "assistant", "content": "Hi\nI'm good"},
            {"role": "user", "content": ""},
        ]
        self.assertEqual(format_alternating_prompt(messages), expected)

    def test_system_prompt(self):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
        ]
        expected = [
            {"role": "user", "content": "You are a helpful assistant.\nHello"},
            {"role": "assistant", "content": "Hi"},
            {"role": "user", "content": ""},
        ]
        self.assertEqual(format_alternating_prompt(messages), expected)

    def test_system_prompt_with_no_user_message(self):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "assistant", "content": "Hi"},
        ]
        expected = [
            {"role": "user", "content": "You are a helpful assistant.\n"},
            {"role": "assistant", "content": "Hi"},
            {"role": "user", "content": ""},
        ]
        self.assertEqual(format_alternating_prompt(messages), expected)

    def test_empty_system_prompt(self):
        messages = [
            {"role": "system", "content": ""},
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
        ]
        expected = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
            {"role": "user", "content": ""},
        ]
        self.assertEqual(format_alternating_prompt(messages), expected)

    def test_empty_user_message(self):
        messages = [
            {"role": "user", "content": ""},
            {"role": "assistant", "content": "Hi"},
        ]
        expected = [
            {"role": "user", "content": ""},
            {"role": "assistant", "content": "Hi"},
            {"role": "user", "content": ""},
        ]
        self.assertEqual(format_alternating_prompt(messages), expected)

    def test_empty_assistant_message(self):
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": ""},
        ]
        expected = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": ""},
            {"role": "user", "content": ""},
        ]
        self.assertEqual(format_alternating_prompt(messages), expected)

    def test_multiple_empty_messages(self):
        messages = [
            {"role": "user", "content": ""},
            {"role": "assistant", "content": ""},
            {"role": "user", "content": ""},
            {"role": "assistant", "content": "Hi"},
        ]
        expected = [
            {"role": "user", "content": ""},
            {"role": "assistant", "content": ""},
            {"role": "user", "content": ""},
            {"role": "assistant", "content": "Hi"},
            {"role": "user", "content": ""},
        ]
        self.assertEqual(format_alternating_prompt(messages), expected)
