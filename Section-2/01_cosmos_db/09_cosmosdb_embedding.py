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

products = [
    {
        "id": "p1",
        "name": "Trail Runner Pro",
        "category": "footwear",
        "description":
            "Lightweight running shoes designed for mountain trails."
    },
    {
        "id": "p2",
        "name": "Explorer Hiking Boots",
        "category": "footwear",
        "description":
            "Waterproof boots designed for long hiking trips."
    },
    {
        "id": "p3",
        "name": "QuietSound Headphones",
        "category": "electronics",
        "description":
            "Wireless headphones with active noise cancellation."
    },
    {
        "id": "p4",
        "name": "StormShield Jacket",
        "category": "clothing",
        "description":
            "Waterproof outdoor jacket for rainy weather."
    }
]

for product in products:

    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=product["description"]
    )

    embedding = response.data[0].embedding

    print(
        f"{product['name']} - "
        f"Embedding dimensions: {len(embedding)}"
    )

    product["embedding"] = embedding

    container.upsert_item(product)

    print(f"Stored {product['id']} in Cosmos DB")