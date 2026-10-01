from azure.cosmos import CosmosClient

endpoint="https://customerportal-account.documents.azure.com:443/"
account_key=""

client=CosmosClient(url=endpoint,credential=account_key)

database=client.get_database_client("CustomerPortalDB")

container=database.get_container_client("SupportTickets")

container.delete_item(
    item="ticket-1005",
    partition_key="customer-1004"
)

print("Ticket deleted")
