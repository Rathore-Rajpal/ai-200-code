import os

import psycopg
from openai import OpenAI

api_key = os.environ["AZURE_OPENAI_KEY"]
endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment_name = "text-embedding-3-small"

client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)


query = "I need shoes for running on mountain trails"


# Generate an embedding for the search query
response = client.embeddings.create(
    model=deployment_name,
    input=query
)

query_embedding = response.data[0].embedding


# Convert the embedding into pgvector format
query_vector = "[" + ",".join(
    str(value) for value in query_embedding
) + "]"

# ---------------------------------------------------------
# Connect to PostgreSQL
# ---------------------------------------------------------

conn=psycopg.connect(
    host="ai-200-raj.postgres.database.azure.com",
    port=6432,
    dbname="appdb",
    user="sqladmin",
    password="Rathore@1811",
    sslmode="require"
)


with conn:

    with conn.cursor() as cursor:

        cursor.execute(
            """
            SELECT
                id,
                name,
                category,
                description,
                embedding <=> %s::vector AS distance
            FROM products
            ORDER BY distance
            LIMIT 3;
            """,
            (
                query_vector,
                )
        )

        results = cursor.fetchall()

for product in results:

    print(
        f"Product: {product[1]}\n"
        f"Category: {product[2]}\n"
        f"Description: {product[3]}\n"
        f"Distance: {product[4]:.4f}\n"
    )


conn.close()