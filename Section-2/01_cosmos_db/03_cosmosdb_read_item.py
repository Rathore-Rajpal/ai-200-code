import os

from azure.cosmos import CosmosClient

endpoint = os.environ["COSMOS_ENDPOINT"]
account_key = os.environ["COSMOS_KEY"]
client=CosmosClient(url=endpoint,credential=account_key)

database=client.get_database_client("CustomerPortalDB")

container=database.get_container_client("SupportTickets")

ticket=container.read_item(item="ticket-1005",partition_key="customer-1004")

print(ticket)
