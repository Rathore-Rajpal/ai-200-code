import os

from azure.cosmos import CosmosClient

endpoint = os.environ["COSMOS_ENDPOINT"]
account_key = os.environ["COSMOS_KEY"]

client=CosmosClient(url=endpoint,credential=account_key)

database=client.get_database_client("CustomerPortalDB")

container=database.get_container_client("SupportTickets")

query="""SELECT * FROM SupportTickets st WHERE st.customerId=@customerId"""

results=container.query_items(
    query=query,
    parameters=[
        {
            "name":"@customerId",
            "value":"customer-1001"
        }
    ],
    enable_cross_partition_query=False
)

for ticket in results:
    print(ticket["id"],ticket["subject"],ticket["status"])