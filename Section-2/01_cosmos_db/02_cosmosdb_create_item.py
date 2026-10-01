import os

from azure.cosmos import CosmosClient

endpoint = os.environ["COSMOS_ENDPOINT"]
account_key = os.environ["COSMOS_KEY"]

client=CosmosClient(url=endpoint,credential=account_key)

database=client.get_database_client("CustomerPortalDB")

container=database.get_container_client("SupportTickets")

ticket = {
    "id": "ticket-1006",
    "customerId": "customer-1004",
    "subject": "Application crashes during checkout",
    "description": (
        "The mobile application closes when the customer "
        "tries to complete checkout."
    ),
    "category": "Technical",
    "priority": "High",
    "status": "Open",
    "createdAt": "2026-09-02T10:00:00Z",
}

container.create_item(body=ticket)

print("Ticket created")