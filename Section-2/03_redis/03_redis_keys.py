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

print("Keys currently stored in Redis:")
print("--------------------------------")

for key in r.scan_iter("*"):
    print(key)