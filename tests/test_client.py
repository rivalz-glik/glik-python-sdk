import os
import time
import unittest

from glik_sdk.client import (
    GlikChat,
    GlikCompletion,
    GlikDataset,
    GlikSdk,
    GlikWorkflow,
)

API_KEY = os.environ.get("API_KEY")
APP_ID = os.environ.get("APP_ID")
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.glik.ai/v1")
FILE_PATH_BASE = os.path.dirname(__file__)


class TestKnowledgeBaseClient(unittest.TestCase):
    def setUp(self):
        self.glik_dataset = GlikDataset(API_KEY, base_url=API_BASE_URL)
        self.README_FILE_PATH = os.path.abspath(
            os.path.join(FILE_PATH_BASE, "../README.md")
        )
        self.dataset_id = None
        self.document_id = None
        self.segment_id = None
        self.batch_id = None

    def _get_dataset_kb_client(self):
        self.assertIsNotNone(self.dataset_id)
        return GlikDataset(
            API_KEY, base_url=API_BASE_URL, dataset_id=self.dataset_id
        )

    def test_001_create_dataset(self):
        response = self.glik_dataset.create_dataset(name="test_dataset")
        data = response.json()
        self.assertIn("id", data)
        self.dataset_id = data["id"]
        self.assertEqual("test_dataset", data["name"])

        # the following tests require to be executed in order because they use
        # the dataset/document/segment ids from the previous test
        self._test_002_list_datasets()
        self._test_003_create_document_by_text()
        time.sleep(1)
        self._test_004_update_document_by_text()
        # self._test_005_batch_indexing_status()
        time.sleep(1)
        self._test_006_update_document_by_file()
        time.sleep(1)
        self._test_007_list_documents()
        self._test_008_delete_document()
        self._test_009_create_document_by_file()
        time.sleep(1)
        self._test_010_add_segments()
        self._test_011_query_segments()
        self._test_012_update_document_segment()
        self._test_013_delete_document_segment()
        self._test_014_delete_dataset()

    def _test_002_list_datasets(self):
        response = self.glik_dataset.list_datasets()
        data = response.json()
        self.assertIn("data", data)
        self.assertIn("total", data)

    def _test_003_create_document_by_text(self):
        client = self._get_dataset_kb_client()
        response = client.create_document_by_text("test_document", "test_text")
        data = response.json()
        self.assertIn("document", data)
        self.document_id = data["document"]["id"]
        self.batch_id = data["batch"]

    def _test_004_update_document_by_text(self):
        client = self._get_dataset_kb_client()
        self.assertIsNotNone(self.document_id)
        response = client.update_document_by_text(
            self.document_id, "test_document_updated", "test_text_updated"
        )
        data = response.json()
        self.assertIn("document", data)
        self.assertIn("batch", data)
        self.batch_id = data["batch"]

    def _test_005_batch_indexing_status(self):
        client = self._get_dataset_kb_client()
        response = client.batch_indexing_status(self.batch_id)
        response.json()
        self.assertEqual(response.status_code, 200)

    def _test_006_update_document_by_file(self):
        client = self._get_dataset_kb_client()
        self.assertIsNotNone(self.document_id)
        response = client.update_document_by_file(
            self.document_id, self.README_FILE_PATH
        )
        data = response.json()
        self.assertIn("document", data)
        self.assertIn("batch", data)
        self.batch_id = data["batch"]

    def _test_007_list_documents(self):
        client = self._get_dataset_kb_client()
        response = client.list_documents()
        data = response.json()
        self.assertIn("data", data)

    def _test_008_delete_document(self):
        client = self._get_dataset_kb_client()
        self.assertIsNotNone(self.document_id)
        response = client.delete_document(self.document_id)
        data = response.json()
        self.assertIn("result", data)
        self.assertEqual("success", data["result"])

    def _test_009_create_document_by_file(self):
        client = self._get_dataset_kb_client()
        response = client.create_document_by_file(self.README_FILE_PATH)
        data = response.json()
        self.assertIn("document", data)
        self.document_id = data["document"]["id"]
        self.batch_id = data["batch"]

    def _test_010_add_segments(self):
        client = self._get_dataset_kb_client()
        response = client.add_segments(
            self.document_id, [{"content": "test text segment 1"}]
        )
        data = response.json()
        self.assertIn("data", data)
        self.assertGreater(len(data["data"]), 0)
        segment = data["data"][0]
        self.segment_id = segment["id"]

    def _test_011_query_segments(self):
        client = self._get_dataset_kb_client()
        response = client.query_segments(self.document_id)
        data = response.json()
        self.assertIn("data", data)
        self.assertGreater(len(data["data"]), 0)

    def _test_012_update_document_segment(self):
        client = self._get_dataset_kb_client()
        self.assertIsNotNone(self.segment_id)
        response = client.update_document_segment(
            self.document_id,
            self.segment_id,
            {"content": "test text segment 1 updated"},
        )
        data = response.json()
        self.assertIn("data", data)
        self.assertGreater(len(data["data"]), 0)
        segment = data["data"]
        self.assertEqual("test text segment 1 updated", segment["content"])

    def _test_013_delete_document_segment(self):
        client = self._get_dataset_kb_client()
        self.assertIsNotNone(self.segment_id)
        response = client.delete_document_segment(self.document_id, self.segment_id)
        data = response.json()
        self.assertIn("result", data)
        self.assertEqual("success", data["result"])

    def _test_014_delete_dataset(self):
        client = self._get_dataset_kb_client()
        response = client.delete_dataset()
        self.assertEqual(204, response.status_code)


class TestGlikChat(unittest.TestCase):
    def setUp(self):
        self.glik_chat = GlikChat(API_KEY)

    def test_create_chat_message(self):
        response = self.glik_chat.create_chat_message(
            {}, "Hello, World!", "test_user"
        )
        self.assertIn("answer", response.text)

    def test_create_chat_message_with_vision_model_by_remote_url(self):
        files = [
            {"type": "image", "transfer_method": "remote_url", "url": "your_image_url"}
        ]
        response = self.glik_chat.create_chat_message(
            {}, "Describe the picture.", "test_user", files=files
        )
        self.assertIn("answer", response.text)

    def test_create_chat_message_with_vision_model_by_local_file(self):
        files = [
            {
                "type": "image",
                "transfer_method": "local_file",
                "upload_file_id": "your_file_id",
            }
        ]
        response = self.glik_chat.create_chat_message(
            {}, "Describe the picture.", "test_user", files=files
        )
        self.assertIn("answer", response.text)

    def test_get_conversation_messages(self):
        response = self.glik_chat.get_conversation_messages(
            "test_user", "your_conversation_id"
        )
        self.assertIn("answer", response.text)

    def test_get_conversations(self):
        response = self.glik_chat.get_conversations("test_user")
        self.assertIn("data", response.text)


class TestCompletionClient(unittest.TestCase):
    def setUp(self):
        self.glik_completion = GlikCompletion(API_KEY)

    def test_create_completion_message(self):
        response = self.glik_completion.create_completion_message(
            {"query": "What's the weather like today?"}, "blocking", "test_user"
        )
        self.assertIn("answer", response.text)

    def test_create_completion_message_with_vision_model_by_remote_url(self):
        files = [
            {"type": "image", "transfer_method": "remote_url", "url": "your_image_url"}
        ]
        response = self.glik_completion.create_completion_message(
            {"query": "Describe the picture."}, "blocking", "test_user", files
        )
        self.assertIn("answer", response.text)

    def test_create_completion_message_with_vision_model_by_local_file(self):
        files = [
            {
                "type": "image",
                "transfer_method": "local_file",
                "upload_file_id": "your_file_id",
            }
        ]
        response = self.glik_completion.create_completion_message(
            {"query": "Describe the picture."}, "blocking", "test_user", files
        )
        self.assertIn("answer", response.text)


class TestGlikSdk(unittest.TestCase):
    def setUp(self):
        self.glik_sdk = GlikSdk(API_KEY)

    def test_message_feedback(self):
        response = self.glik_sdk.message_feedback(
            "your_message_id", "like", "test_user"
        )
        self.assertIn("success", response.text)

    def test_get_application_parameters(self):
        response = self.glik_sdk.get_application_parameters("test_user")
        self.assertIn("user_input_form", response.text)

    def test_file_upload(self):
        file_path = "your_image_file_path"
        file_name = "panda.jpeg"
        mime_type = "image/jpeg"

        with open(file_path, "rb") as file:
            files = {"file": (file_name, file, mime_type)}
            response = self.glik_sdk.file_upload("test_user", files)
            self.assertIn("name", response.text)


class TestGlikWorkflow(unittest.TestCase):
    def setUp(self):
        self.glik_workflow = GlikWorkflow(API_KEY, base_url=API_BASE_URL)
        self.workflow_run_id = None
        self.task_id = None

    def test_001_run_workflow(self):
        # Test running a workflow in blocking mode
        response = self.glik_workflow.run(
            inputs={"task": "test_task"},
            response_mode="blocking",
            user="test_user"
        )
        data = response.json()
        self.assertIn("result", data)
        self.workflow_run_id = data.get("id")
        self.task_id = data.get("task_id")

    def test_002_run_workflow_streaming(self):
        # Test running a workflow in streaming mode
        response = self.glik_workflow.run(
            inputs={"task": "test_task"},
            response_mode="streaming",
            user="test_user"
        )
        self.assertEqual(response.status_code, 200)
        # For streaming, we expect a generator
        self.assertTrue(hasattr(response, 'iter_lines'))

    def test_003_stop_workflow(self):
        # First run a workflow to get a task_id
        response = self.glik_workflow.run(
            inputs={"task": "test_task"},
            response_mode="blocking",
            user="test_user"
        )
        data = response.json()
        task_id = data.get("task_id")
        
        # Test stopping the workflow
        if task_id:
            response = self.glik_workflow.stop(task_id, "test_user")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("result", data)

    def test_004_get_workflow_result(self):
        # First run a workflow to get a workflow_run_id
        response = self.glik_workflow.run(
            inputs={"task": "test_task"},
            response_mode="blocking",
            user="test_user"
        )
        data = response.json()
        workflow_run_id = data.get("id")
        
        # Test getting the workflow result
        if workflow_run_id:
            response = self.glik_workflow.get_result(workflow_run_id)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("result", data)


if __name__ == "__main__":
    unittest.main()