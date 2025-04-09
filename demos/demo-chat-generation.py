from einstein_models import ModelsAI, Messages
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

def print_chat_response_details(response, example_num):
    print(f"\n=== Example {example_num} Chat Response Details ===")
    print(f"Response ID: {response.id}")
    
    print("\nGeneration Details:")
    for i, generation in enumerate(response.generationDetails.generations):
        print(f"\n  Generation {i + 1}:")
        print(f"    ID: {generation.id}")
        print(f"    Role: {generation.role}")
        print(f"    Content: {generation.content}")
        print(f"    Timestamp: {generation.timestamp}")
        
        print("\n    Parameters:")
        print(f"      Finish Reason: {generation.parameters.finish_reason}")
        print(f"      Refusal: {generation.parameters.refusal}")
        print(f"      Index: {generation.parameters.index}")
        
        print("\n    Content Quality:")
        print(f"      Toxicity Detected: {generation.contentQuality.scanToxicity.isDetected}")
        print("      Categories:")
        for category in generation.contentQuality.scanToxicity.categories:
            print(f"        - {category.categoryName}: {category.score}")
    
    print("\nGeneration Parameters:")
    params = response.generationDetails.parameters
    print(f"  Provider: {params.provider}")
    print(f"  Created: {params.created}")
    print(f"  Model: {params.model}")
    print(f"  System Fingerprint: {params.system_fingerprint}")
    print(f"  Object: {params.object}")
    
    print("\nUsage:")
    usage = params.usage
    print(f"  Total Tokens: {usage.total_tokens}")
    print(f"  Prompt Tokens: {usage.prompt_tokens}")
    print(f"  Completion Tokens: {usage.completion_tokens}")
    
    print("\n  Completion Tokens Details:")
    comp_details = usage.completion_tokens_details
    print(f"    Reasoning Tokens: {comp_details.reasoning_tokens}")
    print(f"    Audio Tokens: {comp_details.audio_tokens}")
    print(f"    Accepted Prediction Tokens: {comp_details.accepted_prediction_tokens}")
    print(f"    Rejected Prediction Tokens: {comp_details.rejected_prediction_tokens}")
    
    print("\n  Prompt Tokens Details:")
    prompt_details = usage.prompt_tokens_details
    print(f"    Cached Tokens: {prompt_details.cached_tokens}")
    print(f"    Audio Tokens: {prompt_details.audio_tokens}")
    
    print("=" * 50)

# Example 1: Simple chat about capitals
print("\nExample 1: Chat about capitals")
messages = Messages()
messages.add_assistant_message("You only answer questions about capital of countries.")
messages.add_user_message("Can you give me a recipe for cherry pie?")
messages.add_assistant_message("I'm sorry, but I can only answer questions about capital of countries.")
messages.add_user_message("What is the capital of Switzerland?")

response = sfModelsAI.chat_generate(
    model=Model.OPENAI_GPT_4_OMNI.value,
    messages=messages
)
print_chat_response_details(response, 1)

# Example 2: Technical discussion
print("\nExample 2: Technical discussion")
messages = Messages()
messages.add_assistant_message("You are a technical expert in quantum computing.")
messages.add_user_message("Can you explain quantum superposition in simple terms?")
messages.add_assistant_message("Quantum superposition is when a quantum system exists in multiple states simultaneously until measured.")
messages.add_user_message("How does this differ from classical computing?")

response = sfModelsAI.chat_generate(
    model=Model.OPENAI_GPT_4_OMNI.value,
    messages=messages
)
print_chat_response_details(response, 2)

# Example 3: Creative writing
print("\nExample 3: Creative writing")
messages = Messages()
messages.add_assistant_message("You are a creative writing assistant.")
messages.add_user_message("Write a short story about a robot learning to paint.")
messages.add_assistant_message("Once upon a time, there was a robot named ArtBot who wanted to learn to paint...")
messages.add_user_message("Continue the story, focusing on ArtBot's first painting exhibition.")

response = sfModelsAI.chat_generate(
    model=Model.OPENAI_GPT_4_OMNI.value,
    messages=messages
)
print_chat_response_details(response, 3) 