import time

from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError


endpoint="https://customerportal-account.documents.azure.com:443/"
account_key=""
database_name = "CustomerPortalDB"
container_name = "SupportTickets"


client=CosmosClient(url=endpoint,credential=account_key)

database = client.get_database_client(database_name)

container = database.get_container_client(container_name)

continuation_token = None


while True:

    try:

        if continuation_token is None:

            # First request:
            # Monitor changes from this point forward
            change_feed = container.query_items_change_feed(
                start_time="Now",
                mode="LatestVersion"
            )

        else:

            # Continue from the previous position
            change_feed = container.query_items_change_feed(
                continuation=continuation_token
            )


        changes_found = False


        for item in change_feed:

            changes_found = True

            print("Change detected")
            print("-----------------------------")
            print(f"Ticket ID: {item.get('id')}")
            print(f"Customer:  {item.get('customerId')}")
            print(f"Subject:   {item.get('subject')}")
            print(f"Priority:  {item.get('priority')}")
            print(f"Status:    {item.get('status')}")
            print("-----------------------------")
            print()


        # Save our new position in the Change Feed
        new_token = container.client_connection.last_response_headers.get(
            "etag"
        )

        if new_token:
            continuation_token = new_token


        if not changes_found:
            print("No new changes. Checking again...")


        time.sleep(5)


    except CosmosHttpResponseError as error:

        print("Cosmos DB error:")
        print(error)

        time.sleep(5)