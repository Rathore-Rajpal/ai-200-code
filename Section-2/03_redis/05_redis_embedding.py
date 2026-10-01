import redis
from openai import OpenAI
import numpy as np

redis_host="redis-dev-eus.eastus.redis.azure.net"
redis_port=10000
redis_key=""

r=redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_key,
    ssl=True,
    decode_responses=True
)

endpoint = "https://foundry-dev-eus-10010.openai.azure.com/openai/v1"
deployment_name = "text-embedding-3-small"
openai_key = ""

client = OpenAI(
    base_url=endpoint,
    api_key=openai_key
)

products = [
    {
        "id": "p1",
        "name": "Trail Runner Pro",
        "category": "footwear",
        "description": "Lightweight running shoes designed for mountain trails.",
        "price": "89.99"
    },
    {
        "id": "p2",
        "name": "Explorer Hiking Boots",
        "category": "footwear",
        "description": "Waterproof boots designed for long hiking trips.",
        "price": "129.99"
    },
    {
        "id": "p3",
        "name": "City Walking Shoes",
        "category": "footwear",
        "description": "Comfortable shoes designed for everyday urban walking.",
        "price": "69.99"
    },
    {
        "id": "p4",
        "name": "Mountain Backpack",
        "category": "outdoor",
        "description": "Durable backpack designed for hiking and outdoor adventures.",
        "price": "99.99"
    }
]

for product in products:

    response = client.embeddings.create(
        model=deployment_name,
        input=product["description"]
    )

    embedding = response.data[0].embedding

    embedding_bytes = np.array(
        embedding,
        dtype=np.float32
    ).tobytes()

    redis_key = f"product:{product['id']}"

    r.hset(
        redis_key,
        mapping={
            "id": product["id"],
            "name": product["name"],
            "category": product["category"],
            "description": product["description"],
            "price": product["price"],
            "embedding": embedding_bytes
        }
    )

    print(
        f"Stored {redis_key} | "
        f"Dimensions: {len(embedding)}"
    )