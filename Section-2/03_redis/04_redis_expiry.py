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

r.set(
    "ai:summary:p1",
    "Trail Runner Pro is designed for mountain trail running.",
    ex=60
)
