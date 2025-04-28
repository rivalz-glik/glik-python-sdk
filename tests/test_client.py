import os
import unittest

from glik_sdk.client import GlikChat, GlikCompletion, GlikSdk

API_KEY = os.environ.get("API_KEY")
APP_ID = os.environ.get("APP_ID")


class TestGlikChat(unittest.TestCase):
    def setUp(self):
        self.glik_chat = GlikChat(API_KEY)

    def test_create_chat_message(self):
        response = self.glik_chat.create_chat_message({}, "Hello, World!", "test_user")
        self.assertIn("answer", response.text)

    def test_create_chat_message_with_vision_model_by_remote_url(self):
        files = [{
            "type": "image",
            "transfer_method": "remote_url",
            "url": "your_image_url"
        }]
        response = self.glik_chat.create_chat_message({}, "Describe the picture.", "test_user", files=files)
        self.assertIn("answer", response.text)

    def test_create_chat_message_with_vision_model_by_local_file(self):
        files = [{
            "type": "image",
            "transfer_method": "local_file",
            "upload_file_id": "your_file_id"
        }]
        response = self.glik_chat.create_chat_message({}, "Describe the picture.", "test_user", files=files)
        self.assertIn("answer", response.text)

    def test_get_conversation_messages(self):
        response = self.glik_chat.get_conversation_messages("test_user", "your_conversation_id")
        self.assertIn("answer", response.text)

    def test_get_conversations(self):
        response = self.glik_chat.get_conversations("test_user")
        self.assertIn("data", response.text)


class TestGlikCompletion(unittest.TestCase):
    def setUp(self):
        self.glik_completion = GlikCompletion(API_KEY)

    def test_create_completion_message(self):
        response = self.glik_completion.create_completion_message({"query": "What's the weather like today?"},
                                                                    "blocking", "test_user")
        self.assertIn("answer", response.text)

    def test_create_completion_message_with_vision_model_by_remote_url(self):
        files = [{
            "type": "image",
            "transfer_method": "remote_url",
            "url": "your_image_url"
        }]
        response = self.glik_completion.create_completion_message(
            {"query": "Describe the picture."}, "blocking", "test_user", files)
        self.assertIn("answer", response.text)

    def test_create_completion_message_with_vision_model_by_local_file(self):
        files = [{
            "type": "image",
            "transfer_method": "local_file",
            "upload_file_id": "your_file_id"
        }]
        response = self.glik_completion.create_completion_message(
            {"query": "Describe the picture."}, "blocking", "test_user", files)
        self.assertIn("answer", response.text)


class TestGlikClient(unittest.TestCase):
    def setUp(self):
        self.glik_sdk = GlikSdk(API_KEY)

    def test_message_feedback(self):
        response = self.glik_sdk.message_feedback("your_message_id", 'like', "test_user")
        self.assertIn("success", response.text)

    def test_get_application_parameters(self):
        response = self.glik_sdk.get_application_parameters("test_user")
        self.assertIn("user_input_form", response.text)

    def test_file_upload(self):
        file_path = "your_image_file_path"
        file_name = "panda.jpeg"
        mime_type = "image/jpeg"

        with open(file_path, "rb") as file:
            files = {
                "file": (file_name, file, mime_type)
            }
            response = self.glik_sdk.file_upload("test_user", files)
            self.assertIn("name", response.text)


if __name__ == "__main__":
    unittest.main()
