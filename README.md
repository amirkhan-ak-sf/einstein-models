# Einstein Models Python SDK

A Python SDK for interacting with Salesforce Einstein Models API.

## Installation

```bash
pip install einstein-models
```

## Usage

```python
from einstein_models import ModelsAI

# Initialize the client
sfModelsAI = ModelsAI()

# Authenticate
sfModelsAI.authenticate(
    salesforceDomain="your-domain.my.salesforce.com",
    clientId="your-client-id",
    clientSecret="your-client-secret"
)

# Generate content
response = sfModelsAI.generate(
    model="sfdc_ai__DefaultOpenAIGPT4Omni",
    prompt="What is the capital of Switzerland?",
    probability=0.8,
    locale="en_US"
)

# Chat generation
messages = Messages()
messages.add_user_message("What is the capital of Switzerland?")
response = sfModelsAI.chat_generate(
    model="sfdc_ai__DefaultOpenAIGPT4Omni",
    messages=messages
)
```

## License

MIT 