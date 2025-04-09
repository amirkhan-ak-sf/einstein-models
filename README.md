# Einstein Models Python SDK

A Python SDK for interacting with Salesforce Einstein Models API.

## Prerequisites
### Retrieving Salesforce Credentials

Einstein AI can be easily configured by providing the Salesforce external app or connected app client credentials.

In order to create client credentials, follow these instructions (Step 1 only): [Salesforce Developer Guide](https://developer.salesforce.com/docs/einstein/genai/guide/access-models-api-with-rest.html)

Once the external app or connected app is created, get the client credentials for consumer ID and secret. You will also need your Salesforce organization name, which you can extract from the Salesforce URL.


## Installation

```bash
pip install einstein-models
```

## Usage

```python
from einstein_models import ModelsAI

# Get model list
from einstein_models.models.models import get_models

# Initialize the client
sfModelsAI = ModelsAI()

# Save available models
Models = get_models()

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

# Generate content with model list
response = sfModelsAI.generate(
    model=Model.OPENAI_GPT_4_OMNI.value,
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