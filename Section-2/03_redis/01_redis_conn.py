import redis

redis_host="ai-200-raj.centralindia.redis.azure.net"
redis_port=10000
redis_key=""

r=redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_key,
    ssl=True,
    decode_responses=True
)

response=r.ping()

print("Connected to Azure Managed Redis")
print("PING:", response)

