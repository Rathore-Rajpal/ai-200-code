import os

from openai import OpenAI
from azure.cosmos import CosmosClient


AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]

AZURE_OPENAI_KEY = os.environ["AZURE_OPENAI_KEY"]

EMBEDDING_MODEL = "text-embedding-3-small"

COSMOS_ENDPOINT = os.environ["COSMOS_ENDPOINT"]
COSMOS_KEY = os.environ["COSMOS_KEY"]

DATABASE_NAME = "CustomerPortalDB"
CONTAINER_NAME = "products"

openai_client = OpenAI(
    base_url=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY
)

cosmos_client = CosmosClient(
    COSMOS_ENDPOINT,
    credential=COSMOS_KEY
)

database = cosmos_client.get_database_client(DATABASE_NAME)

container = database.get_container_client(CONTAINER_NAME)

search_text = "shoes for running on mountain trails"

response = openai_client.embeddings.create(
    model=EMBEDDING_MODEL,
    input=search_text
)

query_embedding = response.data[0].embedding

query = """
SELECT TOP 3
    c.id,
    c.name,
    c.category,
    c.description,
    VectorDistance(c.embedding, @embedding) AS SimilarityScore
FROM c
ORDER BY VectorDistance(c.embedding, @embedding)
"""

results = container.query_items(
    query=query,
    parameters=[
        {
            "name": "@embedding",
            "value": query_embedding
        }
    ],
    enable_cross_partition_query=True
)

for item in results:
    print(
        item["name"],
        "-",
        item["SimilarityScore"]
    )