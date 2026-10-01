import os

from azure.cosmos import CosmosClient

endpoint = os.environ["COSMOS_ENDPOINT"]
account_key = os.environ["COSMOS_KEY"]

client=CosmosClient(url=endpoint,credential=account_key)

database=client.get_database_client("CustomerPortalDB")

container=database.get_container_client("SupportTickets")

container_properties=container.read()

print("Successfully connected to Azure Cosmos DB.")
print(f"Database: CustomerPortalDB")
print(f"Container: {container_properties['id']}")

