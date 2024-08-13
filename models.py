import os

from llama_index.core import Settings
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.llms.gemini import Gemini
from dotenv import load_dotenv

load_dotenv()

# keys
az_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
az_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
az_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# models
embed_model = OpenAIEmbedding(embed_batch_size=10)
llm = AzureOpenAI(
    engine="gpt-4o",
    model="gpt-4o",
    temperature=0.0,
    api_key=az_openai_api_key,
    azure_endpoint=az_openai_endpoint,
    api_version=az_openai_api_version,
)
# llm = Gemini(model="models/gemini-1.5-pro")
# embed_model = GeminiEmbedding("models/text-embedding-004")

# Configurations
Settings.embed_model = embed_model
Settings.llm = llm

# tests
# print(llm.complete("why is the sky blue?"))
# print(embed_model.get_text_embedding("why is the sky blue?"))
