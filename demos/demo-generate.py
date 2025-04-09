from einstein_models import ModelsAI
from einstein_models.models.models import get_models

# Initialize the ModelsAI class
sfModelsAI = ModelsAI()

# Authenticate with your Salesforce credentials
sfOrg = "copilot-425-689-demo.my.salesforce.com"
clientId = "3MVG9slge.VWGNwkP7YMZBclFZ9tFroHKux8jXQAgZN89DeQO4PXtFW5qj2zYkgbVPRWIsmzSxIihEKqElieT"
clientSecret = "BBEB656BEFE0E73EAA33A0F2B2E80BADB1CEB8DCD96FF80BABF9632D0DF3AD5C"

print("Authenticating...")
auth_response = sfModelsAI.authenticate(sfOrg, clientId, clientSecret)
#print(f"Authentication response: {auth_response}")

# Get the Model enum
Model = get_models()

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

# Example 1: Using the enum to select a model
print("\nGenerating with GPT-4o...")
response = sfModelsAI.generate(
    model=Model.OPENAI_GPT_4_OMNI.value,
    prompt="What is the capital of Switzerland?",
    probability=0.8,
    locale="en_US"
)
print_response_details(response, 1)

# Example 2: Using a different model from the enum
print("\nGenerating with Claude 3 Haiku...")
response = sfModelsAI.generate(
    model=Model.ANTHROPIC_CLAUDE_3_HAIKU.value,
    prompt="Explain quantum computing in simple terms",
    probability=0.8,
    locale="en_US"
)
print_response_details(response, 2)

# Example 3: Using GPT-4 Turbo
print("\nGenerating with GPT-4 Turbo...")
response = sfModelsAI.generate(
    model=Model.OPENAI_GPT_4_TURBO.value,
    prompt="Create a detailed analysis of the impact of AI on healthcare",
    probability=0.8,
    locale="en_US"
)
print_response_details(response, 3)

# Example 4: Using GPT-3.5 Turbo
print("\nGenerating with GPT-3.5 Turbo...")
response = sfModelsAI.generate(
    model=Model.OPENAI_GPT_35_TURBO.value,
    prompt="Write a short story about a robot learning to paint",
    probability=0.8,
    locale="en_US"
)
print_response_details(response, 4)