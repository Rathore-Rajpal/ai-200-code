import redis

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

r.set("product:p1:name", "Trail Runner Pro")

print(
    "String:",
    r.get("product:p1:name")
)

r.hset(
    "product:p1",
    mapping={
        "name": "Trail Runner Pro",
        "category": "footwear",
        "description": "Lightweight running shoes designed for mountain trails.",
        "price": "89.99"
    }
)

print(
    "Hash:",
    r.hgetall("product:p1")
)

r.rpush(
    "recent:products",
    "p1",
    "p2",
    "p3"
)

print(
    "List:",
    r.lrange("recent:products", 0, -1)
)