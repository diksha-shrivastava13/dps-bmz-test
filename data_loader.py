import json
import os
import re

from dotenv import load_dotenv
import asyncio

from llama_index.core import Document, SimpleDirectoryReader, Settings, VectorStoreIndex, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from common import extract_metadata
from models import llm, embed_model


# Configurations
load_dotenv()
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)

# Models
Settings.embed_model = embed_model
Settings.llm = llm


async def attach_metadata(docs: list[Document]) -> list[Document]:
    metadata_string = await extract_metadata(docs)
    print(metadata_string)
    # json_string = re.search(r'```json\n(.*)\n```', metadata_string.fixed_data, re.DOTALL).group(1)
    json_content = re.search(r'```\n{(.*)}\n```', metadata_string.fixed_data, re.DOTALL).group(1)
    key_value_pairs = re.findall(r'"([^"]+)":\s*"([^"]*)"', json_content)
    metadata = dict(key_value_pairs)
    # metadata = json.loads(json_string)

    for doc in docs:
        doc.metadata["country"] = metadata["country"]
        doc.metadata["project"] = metadata["project"]
        doc.metadata["program"] = metadata["program"]
        doc.metadata["theme"] = metadata["theme"]
        doc.metadata["year"] = metadata["year"]
        doc.metadata["risk"] = metadata["risk"]
        doc.metadata["severity"] = metadata["severity"]
        doc.metadata["status"] = metadata["status"]
    return docs


# data
directory = "/Users/DELL/Desktop/raw_data/"
file_paths = []
for root, _, files in os.walk(directory):
    for file in files:
        file_path = os.path.join(root, file)
        file_paths.append(file_path)


# data parser
def ingest_data(file_: str):
    document_init = SimpleDirectoryReader(input_files=[file_]).load_data()
    document_data = asyncio.run(attach_metadata(document_init))
    documents_metadata.extend(document_data)


documents_metadata = list()
for file_path in file_paths:
    print(file_path)
    ingest_data(file_path)


# store data
pinecone_indexes = pc.list_indexes().names()
if "dps-bmz-test" not in pinecone_indexes:
    pc.create_index(
        name="dps-bmz-test",
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

pinecone_index = pc.Index("dps-bmz-test")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents_metadata, storage_context=storage_context)

# document_initial = SimpleDirectoryReader(input_dir=directory).load_data()
# document_metadata = asyncio.run(attach_metadata(document_initial))
# index = VectorStoreIndex.from_documents(document_metadata)
# query_engine = index.as_query_engine()
# answer = query_engine.query("what is the laufzeit of this project?")
# for node in answer.source_nodes:
#     print("first: --", node.text)
#     print(node.metadata)
