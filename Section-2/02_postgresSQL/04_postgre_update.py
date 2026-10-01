import psycopg

conn=psycopg.connect(
    host="ai-200-raj.postgres.database.azure.com",
    port=6432,
    dbname="appdb",
    user="sqladmin",
    password="Rathore@1811",
    sslmode="require"
)

product_id = "p6"
new_price = 229.99
new_stock_quantity = 25

with conn.cursor() as cursor:
    cursor.execute("""
            UPDATE products
            SET
                price = %s,
                stock_quantity = %s
            WHERE id = %s;
        """, (
            new_price,
            new_stock_quantity,
            product_id
        ))
    conn.commit()
print("Product updated")