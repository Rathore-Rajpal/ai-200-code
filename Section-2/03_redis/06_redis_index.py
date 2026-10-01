import redis

from redis.commands.search.field import (
    TextField,
    TagField,
    NumericField,
    VectorField
)

from redis.commands.search.index_definition import (
    IndexDefinition,
    IndexType
)

redis_host="redis-dev-eus.eastus.redis.azure.net"
redis_port=10000
redis_key="="

r=redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_key,
    ssl=True,
    decode_responses=True
)

schema = (

    TextField("name"),

    TagField("category"),

    NumericField("price"),

    VectorField(
        "embedding",
        "HNSW",
        {
            "TYPE": "FLOAT32",
            "DIM": 1536,
            "DISTANCE_METRIC": "COSINE"
        }
    )
)

r.ft("idx:products").create_index(

    schema,

    definition=IndexDefinition(
        prefix=["product:"],
        index_type=IndexType.HASH
    )
)


print(
    "Vector index created successfully."
)