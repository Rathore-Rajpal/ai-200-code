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

conn=psycopg.connect(
    host="ai-200-raj.postgres.database.azure.com",
    port=6432,
    dbname="appdb",
    user="sqladmin",
    password="Rathore@1811",
    sslmode="require"
)


products = [
    {
        "id": "p1",
        "name": "Trail Runner Pro",
        "category": "footwear",
        "description": "Lightweight running shoes designed for mountain trails."
    },
    {
        "id": "p2",
        "name": "Explorer Hiking Boots",
        "category": "footwear",
        "description": "Waterproof boots designed for long hiking trips."
    },
    {
        "id": "p3",
        "name": "City Walking Shoes",
        "category": "footwear",
        "description": "Comfortable casual shoes designed for walking around the city."
    },
    {
        "id": "p4",
        "name": "Alpine Backpack",
        "category": "outdoor",
        "description": "Durable backpack designed for hiking and mountain adventures."
    },
    {
        "id": "p5",
        "name": "Rain Shell Jacket",
        "category": "outdoor",
        "description": "Lightweight waterproof jacket for wet and windy outdoor conditions."
    }
]

with conn:

    with conn.cursor() as cursor:

        for product in products:

            response = client.embeddings.create(
                model=deployment_name,
                input=product["description"]
            )

            embedding = response.data[0].embedding

            embedding_string = "[" + ",".join(
                str(value) for value in embedding
            ) + "]"


            cursor.execute(
                """
                INSERT INTO products
                (
                    id,
                    name,
                    category,
                    description,
                    embedding
                )
                VALUES (%s, %s, %s, %s, %s::vector)
                ON CONFLICT (id)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    category = EXCLUDED.category,
                    description = EXCLUDED.description,
                    embedding = EXCLUDED.embedding;
                """,
                (
                    product["id"],
                    product["name"],
                    product["category"],
                    product["description"],
                    embedding_string
                )
            )


            print(
                f"Inserted: {product['name']} "
                f"({len(embedding)} dimensions)"
            )


conn.close()