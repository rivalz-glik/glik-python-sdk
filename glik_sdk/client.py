import json

import requests


class GlikSdk:
    """
    Base class for interacting with the Glik API.

    This class provides the core functionality for making HTTP requests to the Glik API,
    including authentication and request handling. It serves as the parent class for
    more specialized API clients.

    Attributes:
        api_key (str): The API key used for authentication with the Glik API.
        base_url (str): The base URL for the Glik API. Defaults to "https://api.glik.ai/v1".

    Example:
        >>> sdk = GlikSdk(api_key="your-api-key")
        >>> response = sdk.get_meta(user="user123")
    """

    def __init__(self, api_key, base_url: str = "https://api.glik.ai/v1"):
        """
        Initialize the GlikSdk instance.

        Args:
            api_key (str): The API key for authentication.
            base_url (str, optional): The base URL for the API. Defaults to "https://api.glik.ai/v1".
        """
        self.api_key = api_key
        self.base_url = base_url

    def _send_request(self, method, endpoint, json=None, params=None, stream=False):
        """
        Send a generic HTTP request to the Glik API.

        Args:
            method (str): The HTTP method (GET, POST, etc.).
            endpoint (str): The API endpoint to call.
            json (dict, optional): JSON data to send in the request body.
            params (dict, optional): Query parameters to include in the URL.
            stream (bool, optional): Whether to stream the response. Defaults to False.

        Returns:
            requests.Response: The response from the API.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        url = f"{self.base_url}{endpoint}"
        response = requests.request(
            method, url, json=json, params=params, headers=headers, stream=stream
        )

        return response

    def _send_request_with_files(self, method, endpoint, data, files):
        """
        Send a request with file attachments to the Glik API.

        Args:
            method (str): The HTTP method (POST, PUT, etc.).
            endpoint (str): The API endpoint to call.
            data (dict): Form data to send with the request.
            files (dict): Files to upload with the request.

        Returns:
            requests.Response: The response from the API.
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}

        url = f"{self.base_url}{endpoint}"
        response = requests.request(
            method, url, data=data, headers=headers, files=files
        )

        return response

    def message_feedback(self, message_id, rating, user):
        """
        Submit feedback for a specific message.

        Args:
            message_id (str): The ID of the message to provide feedback for.
            rating (int): The rating to give the message.
            user (str): The user ID submitting the feedback.

        Returns:
            requests.Response: The response from the API.
        """
        data = {"rating": rating, "user": user}
        return self._send_request("POST", f"/messages/{message_id}/feedbacks", data)

    def get_application_parameters(self, user):
        """
        Retrieve application parameters for a specific user.

        Args:
            user (str): The user ID to get parameters for.

        Returns:
            requests.Response: The response containing application parameters.
        """
        params = {"user": user}
        return self._send_request("GET", "/parameters", params=params)

    def file_upload(self, user, files):
        """
        Upload files to the Glik API.

        Args:
            user (str): The user ID uploading the files.
            files (dict): Files to upload, where keys are field names and values are file objects.

        Returns:
            requests.Response: The response from the API.
        """
        data = {"user": user}
        return self._send_request_with_files(
            "POST", "/files/upload", data=data, files=files
        )

    def text_to_audio(self, text: str, user: str, streaming: bool = False):
        """
        Convert text to audio.

        Args:
            text (str): The text to convert to audio.
            user (str): The user ID making the request.
            streaming (bool, optional): Whether to stream the audio response. Defaults to False.

        Returns:
            requests.Response: The response containing the audio data.
        """
        data = {"text": text, "user": user, "streaming": streaming}
        return self._send_request("POST", "/text-to-audio", data=data)

    def get_meta(self, user):
        """
        Retrieve metadata for a specific user.

        Args:
            user (str): The user ID to get metadata for.

        Returns:
            requests.Response: The response containing user metadata.
        """
        params = {"user": user}
        return self._send_request("GET", "/meta", params=params)


class GlikChat(GlikSdk):
    """
    Client for interacting with Glik's chat functionality.

    This class extends GlikSdk to provide specialized methods for chat-related operations,
    including creating messages, managing conversations, and handling chat-specific features.

    Example:
        >>> chat = GlikChat(api_key="your-api-key")
        >>> response = chat.create_chat_message(
        ...     inputs={"context": "Hello"},
        ...     query="How are you?",
        ...     user="user123"
        ... )
    """

    def create_chat_message(
        self,
        inputs,
        query,
        user,
        response_mode="blocking",
        conversation_id=None,
        files=None,
    ):
        """
        Create a new chat message.

        Args:
            inputs (dict): Input parameters for the chat message.
            query (str): The user's query or message.
            user (str): The user ID sending the message.
            response_mode (str, optional): The response mode ("blocking" or "streaming"). Defaults to "blocking".
            conversation_id (str, optional): ID of the conversation to continue. Defaults to None.
            files (dict, optional): Files to include with the message. Defaults to None.

        Returns:
            requests.Response: The response from the API.
        """
        data = {
            "inputs": inputs,
            "query": query,
            "user": user,
            "response_mode": response_mode,
            "files": files,
        }
        if conversation_id:
            data["conversation_id"] = conversation_id

        return self._send_request(
            "POST",
            "/chat-messages",
            data,
            stream=True if response_mode == "streaming" else False,
        )

    def get_suggested(self, message_id, user: str):
        """
        Get suggested responses for a message.

        Args:
            message_id (str): The ID of the message to get suggestions for.
            user (str): The user ID making the request.

        Returns:
            requests.Response: The response containing suggested responses.
        """
        params = {"user": user}
        return self._send_request(
            "GET", f"/messages/{message_id}/suggested", params=params
        )

    def stop_message(self, task_id, user):
        """
        Stop a running message generation task.

        Args:
            task_id (str): The ID of the task to stop.
            user (str): The user ID making the request.

        Returns:
            requests.Response: The response from the API.
        """
        data = {"user": user}
        return self._send_request("POST", f"/chat-messages/{task_id}/stop", data)

    def get_conversations(self, user, last_id=None, limit=None, pinned=None):
        """
        Get a list of conversations for a user.

        Args:
            user (str): The user ID to get conversations for.
            last_id (str, optional): ID of the last conversation to start from. Defaults to None.
            limit (int, optional): Maximum number of conversations to return. Defaults to None.
            pinned (bool, optional): Whether to only return pinned conversations. Defaults to None.

        Returns:
            requests.Response: The response containing the list of conversations.
        """
        params = {"user": user, "last_id": last_id, "limit": limit, "pinned": pinned}
        return self._send_request("GET", "/conversations", params=params)

    def get_conversation_messages(
        self, user, conversation_id=None, first_id=None, limit=None
    ):
        """
        Get messages from a conversation.

        Args:
            user (str): The user ID to get messages for.
            conversation_id (str, optional): ID of the conversation to get messages from. Defaults to None.
            first_id (str, optional): ID of the first message to start from. Defaults to None.
            limit (int, optional): Maximum number of messages to return. Defaults to None.

        Returns:
            requests.Response: The response containing the conversation messages.
        """
        params = {"user": user}

        if conversation_id:
            params["conversation_id"] = conversation_id
        if first_id:
            params["first_id"] = first_id
        if limit:
            params["limit"] = limit

        return self._send_request("GET", "/messages", params=params)

    def rename_conversation(
        self, conversation_id, name, auto_generate: bool, user: str
    ):
        """
        Rename a conversation.

        Args:
            conversation_id (str): The ID of the conversation to rename.
            name (str): The new name for the conversation.
            auto_generate (bool): Whether to auto-generate the name.
            user (str): The user ID making the request.

        Returns:
            requests.Response: The response from the API.
        """
        data = {"name": name, "auto_generate": auto_generate, "user": user}
        return self._send_request(
            "POST", f"/conversations/{conversation_id}/name", data
        )

    def delete_conversation(self, conversation_id, user):
        """
        Delete a conversation.

        Args:
            conversation_id (str): The ID of the conversation to delete.
            user (str): The user ID making the request.

        Returns:
            requests.Response: The response from the API.
        """
        data = {"user": user}
        return self._send_request("DELETE", f"/conversations/{conversation_id}", data)

    def audio_to_text(self, audio_file, user):
        """
        Convert audio to text.

        Args:
            audio_file (file): The audio file to convert.
            user (str): The user ID making the request.

        Returns:
            requests.Response: The response containing the transcribed text.
        """
        data = {"user": user}
        files = {"audio_file": audio_file}
        return self._send_request_with_files("POST", "/audio-to-text", data, files)


class GlikCompletion(GlikSdk):
    """
    Client for interacting with Glik's completion functionality.

    This class extends GlikSdk to provide methods for generating text completions
    using the Glik API.

    Example:
        >>> completion = GlikCompletion(api_key="your-api-key")
        >>> response = completion.create_completion_message(
        ...     inputs={"prompt": "Hello"},
        ...     response_mode="blocking",
        ...     user="user123"
        ... )
    """

    def create_completion_message(self, inputs, response_mode, user, files=None):
        """
        Create a new completion message.

        Args:
            inputs (dict): Input parameters for the completion.
            response_mode (str): The response mode ("blocking" or "streaming").
            user (str): The user ID making the request.
            files (dict, optional): Files to include with the completion. Defaults to None.

        Returns:
            requests.Response: The response from the API.
        """
        data = {
            "inputs": inputs,
            "response_mode": response_mode,
            "user": user,
            "files": files,
        }
        return self._send_request(
            "POST",
            "/completion-messages",
            data,
            stream=True if response_mode == "streaming" else False,
        )


class GlikWorkflow(GlikSdk):
    """
    Client for interacting with Glik's workflow functionality.

    This class extends GlikSdk to provide methods for running and managing workflows
    using the Glik API.

    Example:
        >>> workflow = GlikWorkflow(api_key="your-api-key")
        >>> response = workflow.run(
        ...     inputs={"task": "process_data"},
        ...     response_mode="streaming",
        ...     user="user123"
        ... )
    """

    def run(
        self, inputs: dict, response_mode: str = "streaming", user: str = "abc-123"
    ):
        """
        Run a workflow.

        Args:
            inputs (dict): Input parameters for the workflow.
            response_mode (str, optional): The response mode ("blocking" or "streaming"). Defaults to "streaming".
            user (str, optional): The user ID running the workflow. Defaults to "abc-123".

        Returns:
            requests.Response: The response from the API.
        """
        data = {"inputs": inputs, "response_mode": response_mode, "user": user}
        return self._send_request("POST", "/workflows/run", data)

    def stop(self, task_id, user):
        """
        Stop a running workflow task.

        Args:
            task_id (str): The ID of the task to stop.
            user (str): The user ID making the request.

        Returns:
            requests.Response: The response from the API.
        """
        data = {"user": user}
        return self._send_request("POST", f"/workflows/tasks/{task_id}/stop", data)

    def get_result(self, workflow_run_id):
        """
        Get the result of a workflow run.

        Args:
            workflow_run_id (str): The ID of the workflow run to get results for.

        Returns:
            requests.Response: The response containing the workflow results.
        """
        return self._send_request("GET", f"/workflows/run/{workflow_run_id}")


class GlikDataset(GlikSdk):
    """
    Client for interacting with Glik's dataset functionality.

    This class extends GlikSdk to provide methods for managing datasets,
    including creating, updating, and querying documents and segments.

    Example:
        >>> dataset = GlikDataset(api_key="your-api-key", dataset_id="dataset123")
        >>> response = dataset.create_document_by_text(
        ...     name="example",
        ...     text="This is an example document"
        ... )
    """

    def __init__(
        self,
        api_key,
        base_url: str = "https://api.glik.ai/v1",
        dataset_id: str | None = None,
    ):
        """
        Initialize the GlikDataset instance.

        Args:
            api_key (str): The API key for authentication.
            base_url (str, optional): The base URL for the API. Defaults to "https://api.glik.ai/v1".
            dataset_id (str, optional): The ID of the dataset to work with. Defaults to None.
        """
        super().__init__(api_key=api_key, base_url=base_url)
        self.dataset_id = dataset_id

    def _get_dataset_id(self):
        """
        Get the dataset ID, raising an error if not set.

        Returns:
            str: The dataset ID.

        Raises:
            ValueError: If dataset_id is not set.
        """
        if self.dataset_id is None:
            raise ValueError("dataset_id is not set")
        return self.dataset_id

    def create_dataset(self, name: str, **kwargs):
        """
        Create a new dataset.

        Args:
            name (str): The name of the dataset to create.
            **kwargs: Additional parameters to pass to the API.

        Returns:
            requests.Response: The response from the API.
        """
        return self._send_request("POST", "/datasets", {"name": name}, **kwargs)

    def list_datasets(self, page: int = 1, page_size: int = 20, **kwargs):
        """
        List available datasets.

        Args:
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 20.
            **kwargs: Additional parameters to pass to the API.

        Returns:
            requests.Response: The response containing the list of datasets.
        """
        return self._send_request(
            "GET", f"/datasets?page={page}&limit={page_size}", **kwargs
        )

    def create_document_by_text(
        self, name, text, extra_params: dict | None = None, **kwargs
    ):
        """
        Create a document by providing text content.

        Args:
            name (str): The name of the document.
            text (str): The text content of the document.
            extra_params (dict, optional): Additional parameters for document creation.
                Example:
                {
                    'indexing_technique': 'high_quality',
                    'process_rule': {
                        'rules': {
                            'pre_processing_rules': [
                                {'id': 'remove_extra_spaces', 'enabled': True},
                                {'id': 'remove_urls_emails', 'enabled': True}
                            ],
                            'segmentation': {
                                'separator': '\n',
                                'max_tokens': 500
                            }
                        },
                        'mode': 'custom'
                    }
                }
            **kwargs: Additional parameters to pass to the API.

        Returns:
            requests.Response: The response from the API.
        """
        data = {
            "indexing_technique": "high_quality",
            "process_rule": {"mode": "automatic"},
            "name": name,
            "text": text,
        }
        if extra_params is not None and isinstance(extra_params, dict):
            data.update(extra_params)
        url = f"/datasets/{self._get_dataset_id()}/document/create_by_text"
        return self._send_request("POST", url, json=data, **kwargs)

    def update_document_by_text(
        self, document_id, name, text, extra_params: dict | None = None, **kwargs
    ):
        """
        Update a document by providing new text content.

        Args:
            document_id (str): The ID of the document to update.
            name (str): The new name of the document.
            text (str): The new text content of the document.
            extra_params (dict, optional): Additional parameters for document update.
                See create_document_by_text for example structure.
            **kwargs: Additional parameters to pass to the API.

        Returns:
            requests.Response: The response from the API.
        """
        data = {"name": name, "text": text}
        if extra_params is not None and isinstance(extra_params, dict):
            data.update(extra_params)
        url = (
            f"/datasets/{self._get_dataset_id()}/documents/{document_id}/update_by_text"
        )
        return self._send_request("POST", url, json=data, **kwargs)

    def create_document_by_file(
        self, file_path, original_document_id=None, extra_params: dict | None = None
    ):
        """
        Create a document by uploading a file.

        Args:
            file_path (str): Path to the file to upload.
            original_document_id (str, optional): ID of the original document to replace.
            extra_params (dict, optional): Additional parameters for document creation.
                See create_document_by_text for example structure.

        Returns:
            requests.Response: The response from the API.
        """
        files = {"file": open(file_path, "rb")}
        data = {
            "process_rule": {"mode": "automatic"},
            "indexing_technique": "high_quality",
        }
        if extra_params is not None and isinstance(extra_params, dict):
            data.update(extra_params)
        if original_document_id is not None:
            data["original_document_id"] = original_document_id
        url = f"/datasets/{self._get_dataset_id()}/document/create_by_file"
        return self._send_request_with_files(
            "POST", url, {"data": json.dumps(data)}, files
        )

    def update_document_by_file(
        self, document_id, file_path, extra_params: dict | None = None
    ):
        """
        Update a document by uploading a new file.

        Args:
            document_id (str): The ID of the document to update.
            file_path (str): Path to the new file to upload.
            extra_params (dict, optional): Additional parameters for document update.
                See create_document_by_text for example structure.

        Returns:
            requests.Response: The response from the API.
        """
        files = {"file": open(file_path, "rb")}
        data = {}
        if extra_params is not None and isinstance(extra_params, dict):
            data.update(extra_params)
        url = (
            f"/datasets/{self._get_dataset_id()}/documents/{document_id}/update_by_file"
        )
        return self._send_request_with_files(
            "POST", url, {"data": json.dumps(data)}, files
        )

    def batch_indexing_status(self, batch_id: str, **kwargs):
        """
        Get the status of a batch indexing operation.

        Args:
            batch_id (str): The ID of the batch indexing operation.
            **kwargs: Additional parameters to pass to the API.

        Returns:
            requests.Response: The response containing the indexing status.
        """
        url = f"/datasets/{self._get_dataset_id()}/documents/{batch_id}/indexing-status"
        return self._send_request("GET", url, **kwargs)

    def delete_dataset(self):
        """
        Delete the current dataset.

        Returns:
            requests.Response: The response from the API.
        """
        url = f"/datasets/{self._get_dataset_id()}"
        return self._send_request("DELETE", url)

    def delete_document(self, document_id):
        """
        Delete a document from the dataset.

        Args:
            document_id (str): The ID of the document to delete.

        Returns:
            requests.Response: The response from the API.
        """
        url = f"/datasets/{self._get_dataset_id()}/documents/{document_id}"
        return self._send_request("DELETE", url)

    def list_documents(
        self,
        page: int | None = None,
        page_size: int | None = None,
        keyword: str | None = None,
        **kwargs,
    ):
        """
        List documents in the dataset.

        Args:
            page (int, optional): The page number to retrieve.
            page_size (int, optional): The number of items per page.
            keyword (str, optional): Keyword to filter documents by.
            **kwargs: Additional parameters to pass to the API.

        Returns:
            requests.Response: The response containing the list of documents.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["limit"] = page_size
        if keyword is not None:
            params["keyword"] = keyword
        url = f"/datasets/{self._get_dataset_id()}/documents"
        return self._send_request("GET", url, params=params, **kwargs)

    def add_segments(self, document_id, segments, **kwargs):
        """
        Add segments to a document.

        Args:
            document_id (str): The ID of the document to add segments to.
            segments (list): List of segments to add.
                Example: [{"content": "1", "answer": "1", "keyword": ["a"]}]
            **kwargs: Additional parameters to pass to the API.

        Returns:
            requests.Response: The response from the API.
        """
        data = {"segments": segments}
        url = f"/datasets/{self._get_dataset_id()}/documents/{document_id}/segments"
        return self._send_request("POST", url, json=data, **kwargs)

    def query_segments(
        self,
        document_id,
        keyword: str | None = None,
        status: str | None = None,
        **kwargs,
    ):
        """
        Query segments in a document.

        Args:
            document_id (str): The ID of the document to query segments from.
            keyword (str, optional): Keyword to filter segments by.
            status (str, optional): Status to filter segments by (e.g., "completed").
            **kwargs: Additional parameters to pass to the API.

        Returns:
            requests.Response: The response containing the matching segments.
        """
        url = f"/datasets/{self._get_dataset_id()}/documents/{document_id}/segments"
        params = {}
        if keyword is not None:
            params["keyword"] = keyword
        if status is not None:
            params["status"] = status
        if "params" in kwargs:
            params.update(kwargs["params"])
        return self._send_request("GET", url, params=params, **kwargs)

    def delete_document_segment(self, document_id, segment_id):
        """
        Delete a segment from a document.

        Args:
            document_id (str): The ID of the document containing the segment.
            segment_id (str): The ID of the segment to delete.

        Returns:
            requests.Response: The response from the API.
        """
        url = f"/datasets/{self._get_dataset_id()}/documents/{document_id}/segments/{segment_id}"
        return self._send_request("DELETE", url)

    def update_document_segment(self, document_id, segment_id, segment_data, **kwargs):
        """
        Update a segment in a document.

        Args:
            document_id (str): The ID of the document containing the segment.
            segment_id (str): The ID of the segment to update.
            segment_data (dict): The new data for the segment.
                Example: {"content": "1", "answer": "1", "keyword": ["a"], "enabled": True}
            **kwargs: Additional parameters to pass to the API.

        Returns:
            requests.Response: The response from the API.
        """
        data = {"segment": segment_data}
        url = f"/datasets/{self._get_dataset_id()}/documents/{document_id}/segments/{segment_id}"
        return self._send_request("POST", url, json=data, **kwargs)