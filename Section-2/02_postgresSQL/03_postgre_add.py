import psycopg

conn=psycopg.connect(
    host="ai-200-raj.postgres.database.azure.com",
    port=6432,
    dbname="appdb",
    user="sqladmin",
    password="Rathore@1811",
    sslmode="require"
)

product = {
    "id": "p6",
    "name": "Adventure Tent",
    "category": "equipment",
    "description": "Lightweight two-person tent for hiking trips.",
    "price": 249.99,
    "stock_quantity": 15
}

with conn.cursor() as cursor:
    cursor.execute("""
            INSERT INTO products
                (id, name, category, description, price, stock_quantity)
            VALUES
                (%s, %s, %s, %s, %s, %s);
        """, (
            product["id"],
            product["name"],
            product["category"],
            product["description"],
            product["price"],
            product["stock_quantity"]
        ))

    conn.commit()

print("Product added successfully.")

