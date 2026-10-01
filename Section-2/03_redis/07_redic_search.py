import redis
from openai import OpenAI
import numpy as np
from redis.commands.search.query import Query

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

query_text = (
    "I need shoes for running on mountain trails"
)

response = client.embeddings.create(
    model=deployment_name,
    input=query_text
)

query_embedding = response.data[0].embedding

query_vector = np.array(
    query_embedding,
    dtype=np.float32
).tobytes()

query = (
    Query(
        "*=>[KNN 3 @embedding $vec AS vector_distance]"
    )
    .return_fields(
        "name",
        "category",
        "description",
        "price",
        "vector_distance"
    )
    .sort_by("vector_distance")
    .dialect(2)
)

results = r.ft(
    "idx:products"
).search(
    query,
    query_params={
        "vec": query_vector
    }
)

print()
print("Search results")
print("==============")

for position, result in enumerate(
    results.docs,
    start=1
):

    print()
    print(f"Result {position}")
    print("--------------------------")

    print("Key:", result.id)

    print(
        "Name:",
        result.name.decode()
        if isinstance(result.name, bytes)
        else result.name
    )

    print(
        "Category:",
        result.category.decode()
        if isinstance(result.category, bytes)
        else result.category
    )

    print(
        "Price:",
        result.price.decode()
        if isinstance(result.price, bytes)
        else result.price
    )

    print(
        "Vector distance:",
        float(result.vector_distance)
    )