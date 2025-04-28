# Glik Python SDK

A Python client library for interacting with the Glik App Service API. This SDK provides a simple and intuitive interface for building applications that communicate with Glik's AI services.

## Installation

Install the package using pip:

```bash
pip install glik-sdk
```

## Quick Start

### Basic Completion

```python
from glik_sdk import CompletionClient

# Initialize the client with your API key
client = CompletionClient(api_key="your_api_key")

# Create a completion request
response = client.create_completion_message(
    inputs={"query": "What's the weather like today?"},
    response_mode="blocking",
    user="user_id"
)
response.raise_for_status()

# Get the response
result = response.json()
print(result.get('answer'))
```

### Vision Model Usage

#### Using Remote Images

```python
from glik_sdk import CompletionClient

client = CompletionClient(api_key="your_api_key")

# Define image files
files = [{
    "type": "image",
    "transfer_method": "remote_url",
    "url": "your_image_url"
}]

# Create completion with image
response = client.create_completion_message(
    inputs={"query": "Describe the picture."},
    response_mode="blocking",
    user="user_id",
    files=files
)
response.raise_for_status()

result = response.json()
print(result.get('answer'))
```

#### Using Local Images

```python
from glik_sdk import GlikClient

# Initialize client
client = GlikClient(api_key="your_api_key")

# Upload local file
file_path = "path/to/image.jpg"
file_name = "image.jpg"
mime_type = "image/jpeg"

with open(file_path, "rb") as file:
    files = {
        "file": (file_name, file, mime_type)
    }
    upload_response = client.file_upload("user_id", files)
    upload_response.raise_for_status()
    
    file_id = upload_response.json().get("id")
    
    # Use the uploaded file
    files = [{
        "type": "image",
        "transfer_method": "local_file",
        "upload_file_id": file_id
    }]
    
    # Create completion with uploaded image
    response = client.create_completion_message(
        inputs={"query": "Describe the picture."},
        response_mode="blocking",
        user="user_id",
        files=files
    )
    response.raise_for_status()
    
    result = response.json()
    print(result.get('answer'))
```

### Streaming Chat

```python
import json
from glik_sdk import GlikChat

client = GlikChat(api_key="your_api_key")

# Create streaming chat message
response = client.create_chat_message(
    inputs={},
    query="Hello",
    user="user_id",
    response_mode="streaming"
)
response.raise_for_status()

# Process streaming response
for line in response.iter_lines(decode_unicode=True):
    line = line.split('data:', 1)[-1]
    if line.strip():
        line = json.loads(line.strip())
        print(line.get('answer'))
```

## Advanced Usage

### Chat Management

```python
from glik_sdk import GlikChat

client = GlikChat(api_key="your_api_key")

# Get application parameters
parameters = client.get_application_parameters(user="user_id")
parameters.raise_for_status()
print(parameters.json())

# Get conversation list
conversations = client.get_conversations(user="user_id")
conversations.raise_for_status()
print(conversations.json())

# Get messages from a conversation
messages = client.get_conversation_messages(
    user="user_id",
    conversation_id="conversation_id"
)
messages.raise_for_status()
print(messages.json())

# Rename a conversation
rename_response = client.rename_conversation(
    conversation_id="conversation_id",
    name="new_name",
    user="user_id"
)
rename_response.raise_for_status()
print(rename_response.json())
```

## Features

- Support for both completion and chat modes
- Vision model integration with local and remote image support
- Streaming response handling
- Conversation management
- File upload capabilities
- Simple and intuitive API

## Requirements

- Python 3.6+
- requests library
