import os
from dotenv import load_dotenv
from einstein_models import ModelsAI
from einstein_models.models.embedding_models import EmbeddingModel


# Load environment variables
load_dotenv()

# Get credentials from environment variables
salesforce_domain = os.getenv("SF_ORG")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

if not all([salesforce_domain, client_id, client_secret]):
    print("Error: Please set SALESFORCE_DOMAIN, CLIENT_ID, and CLIENT_SECRET in your .env file")
    

# Initialize the ModelsAI client
client = ModelsAI()

# Authenticate
print("Authenticating...")
auth_data = client.authenticate(salesforce_domain, client_id, client_secret)
print(f"Authentication successful! Token type: {auth_data.get('token_type')}")

# Example text to generate embeddings for
texts = [
    "Every day, once a day, give yourself a present",
    "The best way to predict the future is to create it"
]

# Generate embeddings using OpenAI Ada 002 model
print("\nGenerating embeddings with OpenAI Ada 002...")
response = client.generate_embedding(
    model=EmbeddingModel.OPENAI_ADA_002.value,
    input_texts=texts
)

# Print the embeddings
print("\nEmbeddings:")
for embedding in response.embeddings:
    print(f"\nText {embedding.index + 1}:")
    print(f"Embedding vector (first 5 values): {embedding.embedding[:5]}...")

# Print usage information
print("\nUsage:")
print(f"Prompt tokens: {response.parameters.usage.prompt_tokens}")
print(f"Total tokens: {response.parameters.usage.total_tokens}")
print(f"Model: {response.parameters.model}")
