from einstein_models import ModelsAI
from einstein_models.models.models import get_models
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
sf_org = os.getenv('SF_ORG')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

# Initialize the ModelsAI class
sfModelsAI = ModelsAI()

# Authenticate
print("Authenticating...")
auth_response = sfModelsAI.authenticate(
    salesforce_domain=sf_org,
    client_id=client_id,
    client_secret=client_secret
)
# print(f"Authentication response: {auth_response}")

# Get the Model enum
Model = get_models()

# List available models from the API
print("\nFetching available models from your org...")
available_models = sfModelsAI.list_models()
print("Available models in your org:")
for model in available_models:
    print(f"- {model.name} ({model.value})")

# Use the first available model for demonstration
if available_models:
    model_id = "sfdc_ai__DefaultGPT4Omni"
    print(f"\nUsing model: {model_id}")
    
    #Example 1 - generate text
    # Generate content
    print("\nGenerating content...")
    response = sfModelsAI.generate(
        model=model_id,
        prompt="What is the capital of Switzerland?",
        probability=0.8,
        locale="en_US"
    )
    
    # Print the response
    print("\nGenerated text:")
    print(response.generation.generatedText)
else:
    print("No models available in your org. Please check your permissions and model availability.")




def print_response_details(response, example_num):
    print(f"\n=== Example {example_num} Response Details ===")
    print(f"Response ID: {response.id}")
    
    print("\nGeneration:")
    print(f"  ID: {response.generation.id}")
    print(f"  Generated Text: {response.generation.generatedText}")
    
    print("\nContent Quality:")
    print(f"  Toxicity Detected: {response.generation.contentQuality.scanToxicity.isDetected}")
    print("  Categories:")
    for category in response.generation.contentQuality.scanToxicity.categories:
        print(f"    - {category.categoryName}: {category.score}")
    
    print("\nParameters:")
    print(f"  Provider: {response.parameters.provider}")
    print(f"  Model: {response.parameters.model}")
    print(f"  Created: {response.parameters.created}")
    
    print("\nUsage:")
    print(f"  Total Tokens: {response.parameters.usage.total_tokens}")
    print(f"  Prompt Tokens: {response.parameters.usage.prompt_tokens}")
    print(f"  Completion Tokens: {response.parameters.usage.completion_tokens}")
    print("=" * 50)


# Example 2: Using GPT-4 Turbo
print("\nGenerating with GPT-4 Turbo...")
model_id = "sfdc_ai__DefaultOpenAIGPT4"
response = sfModelsAI.generate(
    model=model_id,
    prompt="Create a detailed analysis of the impact of AI on healthcare",
)

print(response.generation.generatedText)
print_response_details(response, 2)


# Example 3: Using GPT-3.5 Turbo
print("\nGenerating with GPT-3.5 Turbo...")
model_id = "sfdc_ai__DefaultOpenAIGPT35Turbo"
response = sfModelsAI.generate(
    model=model_id,
    prompt="Write a short story about a robot learning to paint",
    probability=0.8,
)
print(response.generation.generatedText)
print_response_details(response, 3)


